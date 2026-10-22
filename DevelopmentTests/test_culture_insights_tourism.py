"""B216 actual projection Lua and owned SQL; no native Tourism settlement claim."""
import unittest, sqlite3, json, os, zlib
from pathlib import Path
from lupa.lua55 import LuaRuntime
R=Path(__file__).resolve().parents[1]

def fixture():
    l=LuaRuntime(unpack_returned_tuples=True)
    l.execute("""
      include=function()end
      function event()local e={};function e.Add(f)e[#e+1]=f end;return setmetatable(e,{__call=function(s,...)for _,f in ipairs(s)do f(...)end end})end
      Events={};for _,n in ipairs({'LoadScreenClose','GovernorAssigned','GovernorChanged','GovernorPromoted','GovernorEstablished','PlayerTurnActivated','CityBuildingsChanged'})do Events[n]=event()end
      function city(id,owner)
       local c={id=id,owner=owner,token='city'..id,present={},pillaged={},records={},active=4,specialization='CULTURE',potential=4}
       function c:GetOwner()return self.owner end;function c:GetID()return self.id end
       function c:GetX()return self.id end;function c:GetY()return 8 end;function c:GetProperty()return self.token end
       function c:GetBuildings()return self end;function c:GetBuildQueue()return self end
       function c:IsPillaged(id)return self.pillaged[id]==true end
       return c
      end
      a=city(1,0);b=city(2,0);foreign=city(3,3);cities={a,b};foreignCities={foreign}
      function player(list)return {GetCities=function()return {
       Members=function()local i=0;return function()i=i+1;if list[i]then return i,list[i]end end end,
       FindID=function(self,id)for _,c in ipairs(list)do if c.id==id then return c end end end}end}end
      Players={[0]=player(cities),[3]=player(foreignCities)}
      ownCiv='CIVILIZATION_HOME';PlayerConfigurations={[0]={GetCivilizationTypeName=function()return ownCiv end}}
      creates=0;removes=0;reads=0;facts=0;args={};links={};info={Buildings={},Modifiers={},DynamicModifiers={}}
      info.DynamicModifiers.MODIFIER_SINGLE_CITY_ADJUST_TOURISM_LATE_ERAS={CollectionType='COLLECTION_OWNER',EffectType='EFFECT_ADJUST_CITY_TOURISM_LATE_ERAS'}
      for n=1,192 do local bn='BUILDING_SPC_INSIGHT_TOURISM_'..n;local mid='SPC_INSIGHT_TOURISM_'..n
       info.Buildings[bn]={Index=n,InternalOnly=1,PrereqDistrict='DISTRICT_CITY_CENTER',CitizenSlots=0,Housing=0}
       info.Modifiers[mid]={ModifierType='MODIFIER_SINGLE_CITY_ADJUST_TOURISM_LATE_ERAS'}
       args[#args+1]={ModifierId=mid,Name='Modifier',Value=tostring(n*2)};args[#args+1]={ModifierId=mid,Name='MinimumEra',Value='ERA_ANCIENT'}
       links[#links+1]={BuildingType=bn,ModifierId=mid}
      end
      P={Info=function(t,k)return info[t][k]end,Rows=function(t)return t=='ModifierArguments' and args or links end,
       Field=function(t,k)return t[k]end,IsTestPlayer=function(pid)return pid==0 end,
       HasBuilding=function(c,n)reads=reads+1;if unreadable then return nil end;return c.present[n]==true end,
       RemoveBuilding=function(c,n)if failRemove then error('remove failed')end;c.present[n]=nil;removes=removes+1;Events.CityBuildingsChanged(c.owner,c.id)end,
       CreateBuilding=function(c,n)creates=creates+1;if not failCreate then c.present[n]=true;c.pillaged[n]=nil end;Events.CityBuildingsChanged(c.owner,c.id)end}
      shared={EffectiveFacts={Read=function(pid,c)
       facts=facts+1;if c.unknown then error('unknown')end
       return {specialization=c.specialization,potential=c.potential,active=c.active,activeStatus='KNOWN',token=c.token}
      end}}
      exits={};returns={};store={Owns=function(c)return c.owner==0 end,
       ExpeditionInsights=function(pid,c)if historyError then error('history unknown')end;return c.records end,
       RegisterExit=function(n,f)exits[n]=f end,RegisterReturn=function(n,f)returns[n]=f end,
       IsExitTarget=function(c,loss)return loss.confirmed==true end,
       RemoveOwned=function(c,loss,names)assert(loss.confirmed);for n=1,#names do c.present[n]=nil end end}
      shared.CityProgressionStore=store;SPCDistrictCompleteness={Clone=function(x)return x end}
      Locale={Lookup=function(k,v)return k..':'..tostring(v)end}
      function insight(c,civ,category)c.records[civ..':'..category]={civ=civ,category=category,turn=1}end
    """)
    for f in ['NetworkInput.lua','CurrentSpecializationFacts.lua','CultureInsightsTourism.lua']:l.execute((R/'Mod'/f).read_text())
    l.execute('d=SPCCultureInsightsTourism.Start(P,shared)')
    return l

class Projection(unittest.TestCase):
    def test_final_value_replacement_and_other_city_isolation(self):
        fixture().execute("""
         insight(a,'CIVILIZATION_A','PEOPLE');d.Audit();assert(a.present[1] and not b.present[1])
         insight(a,'CIVILIZATION_B','PEOPLE');d.Audit({player=0,city=1});assert(a.present[2] and not a.present[1] and not b.present[2])
         assert(creates==2 and removes==1)
        """)
    def test_unchanged_projection_does_not_scan_all_carriers_or_write(self):
        fixture().execute("insight(a,'CIVILIZATION_A','PEOPLE');d.Audit();reads=0;facts=0;d.Audit({player=0,city=1});assert(reads==1 and facts==1 and creates==1 and removes==0 and not d.pending)")
    def test_active_and_identity_exit_retain_history(self):
        fixture().execute("""
         insight(a,'CIVILIZATION_A','PEOPLE');d.Audit();a.active=3;Events.GovernorChanged(0);assert(not a.present[1] and next(a.records))
         a.active=4;Events.GovernorEstablished(0);assert(a.present[1]);a.specialization='RESEARCH';d.Audit({player=0,city=1});assert(not a.present[1] and next(a.records))
        """)
    def test_own_civilization_filter_and_restore(self):
        fixture().execute("""
         insight(a,'CIVILIZATION_A','PEOPLE');insight(a,'CIVILIZATION_HOME','WORKS');d.Audit();assert(a.present[1])
         ownCiv='CIVILIZATION_OTHER';d.Audit({player=0,city=1});assert(a.present[2] and not a.present[1])
        """)
    def test_load_removes_stale_foreign_and_rebuilds_from_history(self):
        fixture().execute("""
         a.present[88]=true;foreign.present[12]=true;insight(a,'CIVILIZATION_A','PEOPLE');Events.LoadScreenClose()
         assert(a.present[1] and not a.present[88] and not foreign.present[12]);Events.LoadScreenClose();assert(a.present[1])
        """)
    def test_unknown_holds_only_same_reference_projection(self):
        fixture().execute("""
         insight(a,'CIVILIZATION_A','PEOPLE');d.Audit();a.unknown=true;d.Audit({player=0,city=1});assert(a.present[1] and d.errors['0:1'])
         a.token='replacement';d.Audit({player=0,city=1});assert(not a.present[1])
        """)
    def test_unknown_history_does_not_become_zero_or_native_pass(self):
        fixture().execute("insight(a,'CIVILIZATION_A','PEOPLE');d.Audit();historyError=true;d.Audit({player=0,city=1});assert(a.present[1] and d.Describe(0,a):find('UNKNOWN'))")
    def test_failed_projection_recovery_and_no_stacked_values(self):
        fixture().execute("""
         insight(a,'CIVILIZATION_A','PEOPLE');d.Audit();insight(a,'CIVILIZATION_B','PEOPLE');failCreate=true
         d.Audit({player=0,city=1});assert(not a.present[1] and not a.present[2] and d.errors['0:1'])
         failCreate=false;d.Audit({player=0,city=1});assert(a.present[2] and not a.present[1])
        """)
    def test_removed_or_pillaged_carrier_repairs_current_value(self):
        fixture().execute("""
         insight(a,'CIVILIZATION_A','PEOPLE');d.Audit();a.present[1]=nil;Events.CityBuildingsChanged(0,1);assert(a.present[1])
         a.pillaged[1]=true;Events.CityBuildingsChanged(0,1);assert(a.present[1] and not a.pillaged[1])
        """)
    def test_confirmed_exit_and_return(self):
        fixture().execute("""
         insight(a,'CIVILIZATION_A','PEOPLE');d.Audit();local loss={confirmed=true,origin={owner=0}}
         a.owner=3;exits.CultureInsightsTourism(a,loss);assert(not a.present[1] and next(a.records) and not d.records['0:1'])
         a.owner=0;returns.CultureInsightsTourism(0,a);assert(a.present[1])
        """)
    def test_unconfirmed_exit_rejected(self):
        fixture().execute("insight(a,'CIVILIZATION_A','PEOPLE');d.Audit();assert(not pcall(exits.CultureInsightsTourism,a,{confirmed=false,origin={owner=0}}));assert(a.present[1])")
    def test_destroyed_city_does_not_accumulate_session_records(self):
        fixture().execute("d.Audit();table.remove(cities,1);d.Audit({player=0});assert(not d.records['0:1'])")
    def test_owned_definition_mismatch_stops_without_write(self):
        fixture().execute("args[1].Value='999';d.Audit();assert(d.error and creates==0 and removes==0)")
    def test_failed_remove_does_not_create_new_value_and_can_recover(self):
        fixture().execute("""
         insight(a,'CIVILIZATION_A','PEOPLE');d.Audit();insight(a,'CIVILIZATION_B','PEOPLE');failRemove=true
         d.Audit({player=0,city=1});assert(a.present[1] and not a.present[2] and d.errors['0:1'])
         failRemove=false;d.Audit({player=0,city=1});assert(not a.present[1] and a.present[2])
        """)
    def test_report_is_read_only_and_logs_existing_collector_prefix(self):
        fixture().execute("insight(a,'CIVILIZATION_A','PEOPLE');d.Audit();local before=creates;d.Describe(0,a);assert(creates==before and removes==0)")
    def test_destroyed_error_only_city_does_not_accumulate_errors(self):
        fixture().execute("historyError=true;d.Audit();assert(d.errors['0:1']);table.remove(cities,1);d.Audit({player=0});assert(not d.errors['0:1'])")

    def test_max_existing_history_boundary(self):
        fixture().execute("""
         for n=1,64 do for _,cat in ipairs({'PEOPLE','WORKS','PLACES'})do insight(a,'CIVILIZATION_'..n,cat)end end
         d.Audit();assert(a.present[192]);insight(a,'CIVILIZATION_EXTRA','PEOPLE');d.Audit({player=0,city=1});assert(d.errors['0:1'])
        """)

class CompletionIntegration(unittest.TestCase):
    def test_gate_notifies_only_archive_city_after_confirmed_history(self):
        import test_expedition_spy_task as task
        l=task.Timer().ready()
        l.execute("""
         notifications=0
         shared.CultureInsightsTourism={Audit=function(scope)
          assert(insightWrites==1 and scope.player==2 and scope.city==1)
          notifications=notifications+1
         end}
         task('tourism');currentTurn=85;ownTurn(2);ownTurn(2)
         assert(notifications==1 and req('READ','done').phase=='TASK_COMPLETE')
        """)
    def test_cancelled_mission_does_not_notify_or_award(self):
        import test_expedition_spy_task as task
        l=task.Timer().ready()
        l.execute("""
         shared.CultureInsightsTourism={Audit=function()error('unexpected projection')end}
         task('cancel');targetCity.owner=4;currentTurn=85;ownTurn(2)
         assert(req('READ','done').taskOutcome=='CANCELLED' and insightWrites==0)
        """)

class SQL(unittest.TestCase):
    def test_owned_definitions_on_loaded_database(self):
        path=os.environ.get('SPC_DEBUG_GAMEPLAY_DB')
        if not path:raise RuntimeError('SPC_DEBUG_GAMEPLAY_DB required; no skipped PASS')
        src=sqlite3.connect('file:'+path+'?mode=ro',uri=True);db=sqlite3.connect(':memory:');src.backup(db);src.close();db.create_function('Make_Hash',1,lambda text:zlib.crc32(text.encode()))
        # Reapply only this module in the in-memory fixture, never the external DB.
        for n in range(1,193):
            bn=f'BUILDING_SPC_INSIGHT_TOURISM_{n}';mid=f'SPC_INSIGHT_TOURISM_{n}'
            for table,col,value in [('BuildingModifiers','BuildingType',bn),('ModifierArguments','ModifierId',mid),('Modifiers','ModifierId',mid),('Buildings','BuildingType',bn),('Types','Type',bn)]:
                db.execute(f'delete from {table} where {col}=?',(value,))
        db.executescript((R/'Mod/Data/CultureInsightsTourism.sql').read_text())
        rows=db.execute("select b.BuildingType,m.ModifierType,a.Value from BuildingModifiers b join Modifiers m on m.ModifierId=b.ModifierId join ModifierArguments a on a.ModifierId=m.ModifierId and a.Name='Modifier' where b.BuildingType like 'BUILDING_SPC_INSIGHT_TOURISM_%'").fetchall()
        self.assertEqual(len(rows),192)
        for name,kind,amount in rows:
            self.assertEqual(kind,'MODIFIER_SINGLE_CITY_ADJUST_TOURISM_LATE_ERAS');self.assertEqual(int(amount),2*int(name.rsplit('_',1)[1]))
        self.assertEqual(db.execute("select Value from ModifierArguments where ModifierId='FILMSTUDIO_ENHANCEDLATETOURISM' and Name='MinimumEra'").fetchone()[0],'ERA_ANCIENT')
        db.close()

if __name__=='__main__':unittest.main()
