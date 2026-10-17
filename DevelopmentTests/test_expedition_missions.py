"""B212 actual Gate: three Design missions, archive-city Insight history, Spy-like
city-centre execution, target invalidation and entry-city travel.
Native arrival/UI and Gameplay great-work reads
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
  SPCGreatWorkCatalog={Resolve=function(adapter,kind)if kind=='GREATWORK_TEST' then return {type=kind}end;return nil,'UNSUPPORTED_TYPE' end}
  has={[5]=true,[6]=true};slotWork=12;locations={[5]=8*100+16,[6]=9*100+15}
  slotReads=0
  P.HasBuilding=function(b,index)return has[index] end
  function targetCity:GetBuildings()return {
    GetBuildingLocation=function(self,index)if locationError then error('unavailable')end;return locations[index]end,
    GetGreatWorkInSlot=function(self,index,slot)
     slotReads=slotReads+1;if slotError then error('unavailable')end;if slotNil then return nil end
     if (index==5 or index==6) and slot==0 and slotWork then return slotWork end;return -1 end,
    GetGreatWorkTypeFromIndex=function(self,id)if typeError then error('unavailable')end;if typeNil then return nil end
     if id==12 or id==13 then return workType or 77 end end}end
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
        # B214: the observed game rejects a table in assert's message slot,
        # even on success. Stock Lupa accepts it; model this native signature.
        l.execute("""
          local originalAssert=assert
          assert=function(value,message,...)
            if message~=nil and type(message)~='string' and type(message)~='number' then
              error("bad argument #2 to 'assert' (string expected, got "..type(message)..")",2)
            end
            return originalAssert(value,message,...)
          end
        """)
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
          targetCities.GetCapitalCity=function()return city end;local r=startMission('p',PEOPLE)
          assert(r.error=='MISSION_TARGET_INVALID' and req('READ','r').phase=='ARRIVED' and insightWrites==0)
        """)

    def test_works_retains_site_evidence_while_staying_at_centre(self):
        self.ready().execute("""
          local r=startMission('w',WORKS);assert(r.phase=='TASK_RUNNING' and placeCalls==0)
          assert(units[41].x==15 and units[41].y==8 and req('READ','at').missionCategory=='WORKS' and req('READ','site').missionX==16)
          currentTurn=85;ownTurn(2);r=release('rel')
          assert(r.phase=='ARRIVED' and units[41].x==15 and units[41].y==8 and placeCalls==0)
          assert(insightRecords['CIVILIZATION_TARGET:WORKS'] and insightWrites==1)
        """)

    def test_occupied_sites_never_call_movement_and_preserve_other_units(self):
        for category in ['WORKS','PLACES']:
            with self.subTest(category=category):
                l=self.ready();l.execute("""
                  foreignUnits[7]=unit(7,101,3,15,9);foreignUnits[8]=unit(8,101,3,15,8)
                  UnitManager.PlaceUnit=function()error('MOVEMENT_MUST_NOT_RUN')end
                """)
                l.execute("local r=startMission('m',"+category+");assert(r.phase=='TASK_RUNNING' and units[41].x==15 and units[41].y==8)")
                l.execute("""
                  currentTurn=85;ownTurn(2);local r=release('release')
                  assert(r.phase=='ARRIVED' and insightWrites==1 and placeCalls==0)
                  assert(foreignUnits[7].y==9 and foreignUnits[8].y==8 and destroys==0)
                """)

    def test_displacement_during_site_mission_still_stops_without_award(self):
        l=self.ready();l.execute("""
          startMission('m',PLACES);units[41].x=16;currentTurn=85;ownTurn(2)
          local r=req('READ','drift');assert(r.phase=='HELD' and r.stop=='TEAM_DISPLACED_STOP' and insightWrites==0)
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

    def test_places_stays_at_centre_and_records_selected_wonder(self):
        self.ready().execute("""
          local r=startMission('pl',PLACES);assert(r.phase=='TASK_RUNNING' and units[41].y==8 and r.missionY==9 and placeCalls==0)
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

    def test_eligible_work_in_a_wonder_uses_the_wonder_location(self):
        self.ready().execute("""
          WORKS.Building='BUILDING_PYRAMIDS';WORKS.MissionX=15;WORKS.MissionY=9
          local r=startMission('wonder-work',WORKS)
          assert(r.phase=='TASK_RUNNING' and units[41].y==8 and r.missionY==9 and placeCalls==0 and r.missionWorkID==12)
          currentTurn=85;ownTurn(2);release('rel')
          assert(insightWrites==1 and insightRecords['CIVILIZATION_TARGET:WORKS'])
          assert(not insightRecords['CIVILIZATION_TARGET:PLACES'] and units[41].y==8)
        """)

    def test_selected_work_replacement_cancels_even_when_new_work_has_same_type(self):
        self.ready().execute("""
          startMission('w',WORKS);slotWork=13;currentTurn=84;ownTurn(2)
          local r=req('READ','cancelled')
          assert(r.phase=='TASK_COMPLETE' and r.taskOutcome=='CANCELLED' and insightWrites==0)
          assert(r.missionWorkID==12)
          r=release('rel');assert(r.phase=='ARRIVED')
          r=startMission('replacement',WORKS);assert(r.phase=='TASK_RUNNING' and r.missionWorkID==13)
        """)

    def test_slot_type_and_location_unknown_reject_start_without_native_mutation(self):
        for change in ['slotError=true', 'slotNil=true', 'typeError=true', 'typeNil=true',
                       'SPCGreatWorkCatalog=nil', "SPCGreatWorkCatalog.Resolve=function()return nil,'ERA_UNAVAILABLE' end",
                       'locationError=true', 'locations[5]=nil', 'has[5]=nil',
                       "local buildings=targetCity:GetBuildings();buildings.GetGreatWorkTypeFromIndex=nil;targetCity.GetBuildings=function()return buildings end",
                       "local buildings=targetCity:GetBuildings();buildings.GetBuildingLocation=nil;targetCity.GetBuildings=function()return buildings end"]:
            with self.subTest(change=change):
                self.ready().execute(change + ";local r=startMission('w',WORKS);assert(r.error and r.missionStatus=='UNKNOWN' and r.phase=='ARRIVED' and not r.activityKey and placeCalls==0 and insightWrites==0)")

    def test_unknown_before_due_keeps_progress_and_retries_without_false_cancellation(self):
        for change, restore in [('slotError=true', 'slotError=false'), ('typeError=true', 'typeError=false'),
                                ('typeNil=true', 'typeNil=false'), ('locationError=true', 'locationError=false'),
                                ('has[5]=nil', 'has[5]=true')]:
            with self.subTest(change=change):
                self.ready().execute("""
                  startMission('w',WORKS);currentTurn=84;
                """ + change + """;ownTurn(2)
                  local r=req('READ','pending')
                  assert(r.phase=='TASK_RUNNING' and r.missionStatus=='UNKNOWN' and r.taskStart==83 and r.taskDue==85)
                  assert(not r.taskOutcome and insightWrites==0 and not r.missionCompletionUnknownTurn)
                """ + restore + """;currentTurn=85;ownTurn(2)
                  r=req('READ','done');assert(r.phase=='TASK_COMPLETE' and r.taskOutcome=='SUCCESS' and insightWrites==1)
                """)

    def test_unknown_reads_are_bounded_per_attempt_turn_and_target_event_reopens_check(self):
        self.ready().execute("""
          startMission('w',WORKS);slotError=true;currentTurn=84;slotReads=0
          for i=1,20 do ownTurn(2);req('READ','pending'..i)end
          assert(slotReads==3 and insightWrites==0)
          slotError=false;transfer();assert(slotReads==4)
          currentTurn=85;ownTurn(2);assert(insightWrites==1)
        """)

    def test_same_due_turn_recheck_confirms_current_facts_without_read_award(self):
        self.ready().execute("""
          startMission('w',WORKS);typeError=true;currentTurn=85;ownTurn(2)
          assert(gameProperties.SPC_EXPEDITION_TEAM_P2.state.missionCompletionUnknownTurn==85 and insightWrites==0)
          typeError=false;local r=req('READ','restored')
          assert(r.phase=='TASK_RUNNING' and r.missionStatus=='VALID' and insightWrites==0)
          assert(not gameProperties.SPC_EXPEDITION_TEAM_P2.state.missionCompletionUnknownTurn)
          ownTurn(2);r=req('READ','completed')
          assert(r.taskOutcome=='SUCCESS' and insightWrites==1)
        """)

    def test_unknown_civilization_at_due_cannot_be_cleared_by_partial_read(self):
        self.ready().execute("""
          startMission('w',WORKS)
          local original=PlayerConfigurations[3].GetCivilizationTypeName
          PlayerConfigurations[3].GetCivilizationTypeName=function()return nil end
          currentTurn=85;ownTurn(2)
          local r=req('READ','still-unknown')
          assert(r.phase=='TASK_RUNNING' and r.missionStatus=='UNKNOWN' and r.missionReason=='TARGET_CIVILIZATION_UNAVAILABLE')
          assert(r.missionCompletionUnknownTurn==85 and insightWrites==0)
          PlayerConfigurations[3].GetCivilizationTypeName=original;currentTurn=86;ownTurn(2)
          r=req('READ','later-known')
          assert(r.phase=='HELD' and r.stop=='MISSION_COMPLETION_UNCONFIRMED' and insightWrites==0)
          assert(r.missionCompletionUnknownTurn==85)
        """)

    def test_same_turn_full_civilization_recovery_can_clear_unknown_and_complete(self):
        self.ready().execute("""
          startMission('w',WORKS)
          local original=PlayerConfigurations[3].GetCivilizationTypeName
          PlayerConfigurations[3].GetCivilizationTypeName=function()return nil end
          currentTurn=85;ownTurn(2)
          local r=req('READ','still-unknown');assert(r.missionCompletionUnknownTurn==85 and insightWrites==0)
          PlayerConfigurations[3].GetCivilizationTypeName=original;ownTurn(2)
          r=req('READ','same-turn-known')
          assert(r.phase=='TASK_COMPLETE' and r.taskOutcome=='SUCCESS' and insightWrites==1 and not r.missionCompletionUnknownTurn)
        """)

    def test_same_type_replacement_since_ui_selection_is_rejected_before_admission(self):
        self.ready().execute("""
          WORKS.WorkID=12;slotWork=13
          local r=startMission('stale-work-selection',WORKS)
          assert(r.phase=='ARRIVED' and r.error=='MISSION_TARGET_INVALID' and placeCalls==0 and insightWrites==0)
          assert(not r.activityKey and not r.missionWorkID)
          WORKS.WorkID=13;r=startMission('current-work-selection',WORKS)
          assert(r.phase=='TASK_RUNNING' and r.missionWorkID==13)
        """)

    def test_nil_current_capital_preserves_unknown_and_no_target_cancellation(self):
        self.ready().execute("""
          startMission('p',PEOPLE);capital=false;currentTurn=84;ownTurn(2)
          local r=req('READ','nil-capital')
          assert(r.phase=='TASK_RUNNING' and r.missionStatus=='UNKNOWN' and r.missionReason=='MISSION_CAPITAL_UNKNOWN')
          assert(not r.taskOutcome and insightWrites==0)
          capital=true;currentTurn=85;ownTurn(2)
          r=req('READ','known-capital');assert(r.taskOutcome=='SUCCESS' and insightWrites==1)
        """)

    def test_later_valid_facts_cannot_fill_a_missing_completion_sample(self):
        self.ready().execute("""
          startMission('w',WORKS);typeError=true;currentTurn=85;ownTurn(2)
          typeError=false;currentTurn=86;ownTurn(2)
          local r=req('READ','held')
          assert(r.phase=='HELD' and r.stop=='MISSION_COMPLETION_UNCONFIRMED')
          assert(r.missionStatus=='UNKNOWN' and r.missionCompletionUnknownTurn==85 and r.missionWorkID==12)
          assert(r.taskStart==83 and r.taskDue==85 and insightWrites==0)
        """)

    def test_saved_pending_work_without_instance_evidence_is_not_adopted(self):
        l=self.ready()
        l.execute("""
          startMission('w',WORKS);gameProperties.SPC_EXPEDITION_TEAM_P2.state.missionWorkID=nil
          SPCExpeditionSpyGate.Start(P,shared)
          local v=ExposedMembers.SPC_ExpeditionActivity
          handler(2,{Action='ACTIVITY',Token='recover',UnitID=41,ActivityKey=v.activityKey,Result='RECOVERED',Owned=true,
            Sleeping=true,Awake=false,SampleTurn=currentTurn,NativeOperation=-1})
          local r=req('READ','missing-proof')
          assert(r.phase=='TASK_RUNNING' and r.missionStatus=='UNKNOWN' and r.missionReason=='MISSION_WORK_ID_UNAVAILABLE')
          assert(insightWrites==0 and r.missionWorkID==nil)
        """)

    def test_unreadable_current_capital_is_unknown_not_confirmed_invalidation(self):
        self.ready().execute("""
          startMission('p',PEOPLE)
          local old=targetCity.GetID;targetCity.GetID=function()return nil end
          currentTurn=84;ownTurn(2)
          local r=req('READ','unknown');assert(r.phase=='TASK_RUNNING' and r.missionStatus=='UNKNOWN' and insightWrites==0)
          targetCity.GetID=old;currentTurn=85;ownTurn(2);assert(insightWrites==1)
        """)

    def test_changed_native_type_cancels_and_never_trusts_saved_type(self):
        self.ready().execute("""
          startMission('w',WORKS);workType=99;currentTurn=84;ownTurn(2)
          local r=req('READ','changed')
          assert(r.phase=='TASK_COMPLETE' and r.taskOutcome=='CANCELLED' and insightWrites==0)
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
