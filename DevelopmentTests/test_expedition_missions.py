"""B212 actual Gate: three Design missions, archive-city Insight history, Spy-like
mission movement and return, target invalidation and entry-city travel.
Native placement on foreign district/wonder plots and Gameplay great-work reads
remain USER_GAME_TEST gates; fixtures model the documented API shapes only.
"""
import unittest
import test_expedition_spy_task as base

MISSION_FIXTURE = """
  plotOwner=3
  Map={GetPlot=function(x,y)return {GetIndex=function()return y*100+x end,GetOwner=function()return plotOwner end}end}
  info.BUILDING_AMPHITHEATER={Index=5,BuildingType='BUILDING_AMPHITHEATER',IsWonder=false}
  info.BUILDING_PYRAMIDS={Index=6,BuildingType='BUILDING_PYRAMIDS',IsWonder=true}
  info.GREATWORK_TEST={Index=77,GreatWorkType='GREATWORK_TEST'}
  SPCGreatWorkCatalog={Resolve=function(adapter,kind)if kind=='GREATWORK_TEST' then return {type=kind}end end}
  has={[5]=true,[6]=true};slotWork=12;locations={[5]=8*100+16,[6]=9*100+15}
  P.HasBuilding=function(b,index)return has[index]==true end
  function targetCity:GetBuildings()return {
    GetBuildingLocation=function(self,index)return locations[index]end,
    GetGreatWorkInSlot=function(self,index,slot)if index==5 and slot==0 and slotWork then return slotWork end;return -1 end,
    GetGreatWorkTypeFromIndex=function(self,id)if id==12 then return 77 end end}end
  function startMission(token,mission,unit)
   local p={Action='TASK',Token=token,UnitID=unit or 41,SampleTurn=currentTurn,NativeOperation=-1}
   for k,v in pairs(mission)do p[k]=v end
   handler(2,p);local r=ExposedMembers.SPC_ExpeditionGateReply
   if r.phase=='TASK_PREPARING' and not r.error then
    local key=ExposedMembers.SPC_ExpeditionActivity.activityKey
    handler(2,{Action='ACTIVITY',Token=token..':arm',UnitID=unit or 41,ActivityKey=key,Result='ARMED',Owned=true,Awake=true,Sleeping=false,SampleTurn=currentTurn,NativeOperation=-1})
    handler(2,{Action='ACTIVITY',Token=token..':sleep',UnitID=unit or 41,ActivityKey=key,Result='ASLEEP',Owned=true,SampleTurn=currentTurn,NativeOperation=-1})
    return ExposedMembers.SPC_ExpeditionActivityReply
   end
   return r
  end
  function release(token,unit)
   local v=ExposedMembers.SPC_ExpeditionActivity
   handler(2,{Action='ACTIVITY',Token=token,UnitID=unit or 41,ActivityKey=v.activityKey,Result='RELEASED',Owned=true,SampleTurn=currentTurn,NativeOperation=-1})
   return req('READ',token..':read')
  end
  PEOPLE={Mission='PEOPLE',MissionX=15,MissionY=8}
  WORKS={Mission='WORKS',MissionX=16,MissionY=8,Building='BUILDING_AMPHITHEATER',Slot=0,Work='GREATWORK_TEST'}
  PLACES={Mission='PLACES',MissionX=15,MissionY=9,Building='BUILDING_PYRAMIDS'}
"""


class Missions(unittest.TestCase):
    def ready(self):
        l = base.Timer().ready()
        l.execute(MISSION_FIXTURE)
        return l

    def test_people_success_records_once_returns_and_cannot_repeat(self):
        self.ready().execute("""
          local r=startMission('p',PEOPLE);assert(r.phase=='TASK_RUNNING' and placeCalls==0)
          currentTurn=85;ownTurn(2);r=req('READ','done')
          assert(r.phase=='TASK_COMPLETE' and r.taskOutcome=='SUCCESS' and insightWrites==1)
          assert(insightRecords['CIVILIZATION_TARGET:PEOPLE'].turn==85)
          r=release('rel');assert(r.phase=='ARRIVED' and r.missionCategory==nil and r.taskStart==nil)
          assert(r.insightHistory==1 and r.insightEffective==1 and r.insightKeys[1]=='CIVILIZATION_TARGET:PEOPLE')
          r=startMission('again',PEOPLE);assert(r.error=='MISSION_ALREADY_COMPLETED' and insightWrites==1)
          assert(req('READ','still').phase=='ARRIVED' and destroys==0)
        """)

    def test_people_requires_current_capital(self):
        self.ready().execute("""
          capital=false;local r=startMission('p',PEOPLE)
          assert(r.error=='MISSION_TARGET_INVALID' and req('READ','r').phase=='ARRIVED' and insightWrites==0)
        """)

    def test_works_moves_to_work_plot_then_returns_to_centre(self):
        self.ready().execute("""
          local r=startMission('w',WORKS);assert(r.phase=='TASK_RUNNING' and placeCalls==1)
          assert(units[41].x==16 and units[41].y==8 and req('READ','at').missionCategory=='WORKS')
          currentTurn=85;ownTurn(2);r=release('rel')
          assert(r.phase=='ARRIVED' and units[41].x==15 and units[41].y==8 and placeCalls==2)
          assert(insightRecords['CIVILIZATION_TARGET:WORKS'] and insightWrites==1)
        """)

    def test_works_rejects_ineligible_or_empty_slot(self):
        for change, code in [("WORKS.Work='GREATWORK_RELIC'", 'MISSION_WORK_INELIGIBLE'),
                             ('slotWork=nil', 'MISSION_TARGET_INVALID'),
                             ('has[5]=false', 'MISSION_TARGET_INVALID'),
                             ('WORKS.MissionX=17', 'MISSION_PLOT_CHANGED')]:
            with self.subTest(change=change):
                l = self.ready()
                l.execute(change + ";local r=startMission('w',WORKS);assert(r.error=='" + code + "' and placeCalls==0 and insightWrites==0)")

    def test_losing_the_work_mid_mission_cancels_and_returns(self):
        self.ready().execute("""
          startMission('w',WORKS);slotWork=nil;currentTurn=84;ownTurn(2)
          local r=req('READ','c');assert(r.phase=='TASK_COMPLETE' and r.taskOutcome=='CANCELLED' and insightWrites==0)
          r=release('rel');assert(r.phase=='ARRIVED' and units[41].x==15 and units[41].y==8)
          slotWork=12;r=startMission('w2',WORKS);assert(r.phase=='TASK_RUNNING')
        """)

    def test_places_moves_to_wonder_and_records(self):
        self.ready().execute("""
          local r=startMission('pl',PLACES);assert(r.phase=='TASK_RUNNING' and units[41].y==9)
          currentTurn=85;ownTurn(2);release('rel')
          assert(insightRecords['CIVILIZATION_TARGET:PLACES'] and units[41].y==8)
          r=startMission('pl2',{Mission='PLACES',MissionX=15,MissionY=8,Building='BUILDING_AMPHITHEATER'})
          assert(r.error=='MISSION_BUILDING_UNKNOWN')
        """)

    def test_three_categories_are_independent_keys(self):
        self.ready().execute("""
          for i,m in ipairs({PEOPLE,WORKS,PLACES})do
           startMission('m'..i,m);currentTurn=currentTurn+2;ownTurn(2);release('r'..i)
          end
          local r=req('READ','all');assert(r.insightHistory==3 and insightWrites==3)
        """)

    def test_mid_mission_reload_completes_once(self):
        l = self.ready()
        l.execute("""
          startMission('w',WORKS)
          SPCExpeditionSpyGate.Start(P,shared)
          local r=req('READ','loaded');assert(r.missionCategory=='WORKS' and r.missionX==16)
        """)

    def test_repeated_completion_after_failed_save_is_idempotent(self):
        self.ready().execute("""
          startMission('p',PEOPLE)
          AddInsight=shared.CityProgressionStore.AddExpeditionInsight
          insightRecords['CIVILIZATION_TARGET:PEOPLE']={civ='CIVILIZATION_TARGET',category='PEOPLE',turn=80}
          currentTurn=85;ownTurn(2);local r=req('READ','done')
          assert(r.taskOutcome=='SUCCESS' and insightWrites==0 and insightRecords['CIVILIZATION_TARGET:PEOPLE'].turn==80)
        """)


class EntryTravel(unittest.TestCase):
    def test_unrevealed_target_enters_through_revealed_city_and_relocates(self):
        l = base.gate()
        l.execute(MISSION_FIXTURE)
        l.execute("""
          entryCity={id=11,owner=3,x=18,y=8}
          for k,v in pairs(targetCity)do if type(v)=='function' then entryCity[k]=v end end
          targetCities.Members=function()local list={targetCity,entryCity};local i=0;return function()i=i+1;if list[i]then return i,list[i]end end end
          PlayersVisibility={[2]={IsRevealed=function(self,x,y)return not (x==15 and y==8)end}}
          req('CREATE','a')
          local blocked=nativeDispatch('blind');assert(blocked.error=='ENTRY_UNKNOWN')
          local r=nativeDispatch('b',{EntryX=18,EntryY=8});assert(r.phase=='TRAVELLING' and not r.error and r.entryX==18)
          local old=units[40];local u=unit(41,100,2,18,8);u.name=old.name;units[40]=nil;units[41]=u
          currentTurn=83;ownTurn(2);r=req('READ','arr')
          assert(r.phase=='ARRIVED' and units[41].x==15 and units[41].y==8 and placeCalls==1 and r.entryX==nil)
        """)

    def test_entry_must_be_a_revealed_city_of_the_target_owner(self):
        l = base.gate()
        l.execute(MISSION_FIXTURE)
        l.execute("""
          req('CREATE','a')
          local r=nativeDispatch('b',{EntryX=30,EntryY=30});assert(r.error=='ENTRY_CHANGED' and req('READ','r').phase=='CREATED')
        """)


if __name__ == '__main__':
    unittest.main()


class CityInsightStore(unittest.TestCase):
    """Actual CityProgressionStore record: first-success-only, validated, readback-committed."""
    def store(self):
        from test_dialogue_projects import game
        return game()

    def test_first_success_only_and_persisted_record(self):
        self.store().execute("""
          local st=shared.CityProgressionStore
          assert(st.AddExpeditionInsight(0,c,'CIVILIZATION_X','PEOPLE',5)==true)
          assert(st.AddExpeditionInsight(0,c,'CIVILIZATION_X','PEOPLE',6)==false)
          assert(st.AddExpeditionInsight(0,c,'CIVILIZATION_X','WORKS',6)==true)
          local e=st.ExpeditionInsights(0,c)
          assert(e['CIVILIZATION_X:PEOPLE'].turn==5 and e['CIVILIZATION_X:WORKS'].turn==6)
          e['CIVILIZATION_X:PEOPLE'].turn=99;assert(st.ExpeditionInsights(0,c)['CIVILIZATION_X:PEOPLE'].turn==5)
        """)

    def test_invalid_key_is_rejected_by_record_validation(self):
        self.store().execute("""
          local st=shared.CityProgressionStore
          assert(not pcall(st.AddExpeditionInsight,0,c,'CIVILIZATION_X','RELIC',5))
          assert(not pcall(st.AddExpeditionInsight,0,c,'not-a-civ','PEOPLE',5))
          assert(next(st.ExpeditionInsights(0,c))==nil)
        """)

    def test_other_player_cannot_read_or_write(self):
        self.store().execute("""
          local st=shared.CityProgressionStore
          assert(not pcall(st.AddExpeditionInsight,3,c,'CIVILIZATION_X','PEOPLE',5))
          assert(not pcall(st.ExpeditionInsights,3,c))
        """)
