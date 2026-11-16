"""Standardization health tickets: actual Bridge holds and actual SQL read budget."""
import unittest
from refactor_harness import ROOT,TrackedLua51,legacy_source_observation,separate_legacy_event_namespaces,measure
from test_refactor_s4b import standard
from test_refactor_s5d4c8 import tables
from test_b235_engineering import SETUP,lua

NATIVE="""
local remove,create=P.RemoveBuilding,P.CreateBuilding
P.RemoveBuilding=function(b,id)local plot=b:GetBuildingLocation(id);remove(b,id);Events.BuildingRemovedFromMap.Fire(plot,0,id,b.city.owner)end
P.CreateBuilding=function(q,id)create(q,id);GameEvents.BuildingPillageStateChanged.Fire(q.city.owner,q.city.id,id,false)end
Map.GetPlotIndex=function(x,y)return x end
CityManager={GetDistrictAt=function(x,y)local c=cities[x/100];if c then return {GetCity=function()return c end}end end}
function loss(id)for _,n in ipairs({10,12,14})do local k='BUILDING_SPC_STD_'..n;if cities[id].present[k]then P.RemoveBuilding(cities[id]:GetBuildings(),k);return end end;error('NO_POSITIVE_STD_TO_REMOVE')end
function pulse()shared.FactChanges.Flush();shared.FactBindings.Flush();Events.GameCoreEventPublishComplete.Fire()end
"""
def fixture(ready=True,cold=False):
    l=standard(ready,cold);l.execute(NATIVE);return l

def sql_fixture():
    l=TrackedLua51(unpack_returned_tuples=True);l.globals().include=lambda n:l.execute((ROOT/'Mod'/(n+'.lua')).read_text())
    with legacy_source_observation():
        l.execute('DB='+lua(tables()));l.execute(separate_legacy_event_namespaces(SETUP))
        l.execute("""
        print=function()end;levels={};for _,f in pairs(facts)do f.activeStatus='KNOWN'end
        shared.CityProgressionStore.EngineeringState=function(pid,c)return {token=c.token,value={L=levels[c.id]or 0}}end
        CityManager={GetCityAt=function(x,y)return cities[x]end};Map={GetPlotIndex=function(x,y)return y*100+x end}
        for _,c in pairs(cities)do c.built.city=c;c.built.GetBuildingLocation=function()return c:GetY()*100+c:GetX()end end
        local remove,create=P.RemoveBuilding,P.CreateBuilding
        P.RemoveBuilding=function(b,id)remove(b,id);emit('BuildingRemovedFromMap',b.city:GetX(),b.city:GetY(),id,b.city.owner)end
        P.CreateBuilding=function(b,id)create(b,id);emit('GameEvents.BuildingPillageStateChanged',b.city.owner,b.city.id,id,false)end
        """)
        for n in ('StandardizationCatalog','StandardizationDiscount','CopyYields','StandardizationEffects'):l.globals().include(n)
        l.execute("industry(1,4);levels[1]=1;learn(1,'BUILDING_GRANARY');start();std=d;target=P.Info('Buildings','BUILDING_SPC_STD_BASE_B_BUILDING_GRANARY_L1').Index;assert(cities[1].built[target]);function pulse()emit('GameCoreEventPublishComplete')end")
    return l

class StandardHealth(unittest.TestCase):
    def test_equal_value_missing_repairs_history_unchanged_and_idle_zero(self):
        l=fixture();l.execute("local h=knowledge[5].learned.BUILDING_GRANARY;local n=propertyWrites;loss(1);pulse();assert(stdValue(1)==14 and knowledge[5].learned.BUILDING_GRANARY==h and propertyWrites==n and not std.records['0:1'].healthTicket);local a,b=created,removed;local r=historyReads[4];for i=1,1000 do pulse()end;assert(created==a and removed==b and historyReads[4]==r)")
    def test_complete_pending_retains_ticket_without_positive_reconstruction(self):
        l=fixture();l.execute("net.CheckEvidence(false);pulse();loss(1);local n=created;pulse();assert(stdValue(1)==0 and created==n and std.records['0:1'].healthTicket and std.records['0:1'].retained);send('0,5,0,2,10;0,3,0,2,11;0,2,0,1,12',3);pulse();assert(stdValue(1)==14 and not std.records['0:1'].healthTicket)")
    def test_continuity_only_negative_does_not_heal_unchanged_positive(self):
        l=fixture();l.execute("units[11]=nil;net.CheckEvidence(false);pulse();assert(net.Input(0).continuityOnly and stdValue(1)==14);loss(1);local n=created;pulse();assert(stdValue(1)==0 and created==n and std.records['0:1'].healthTicket);send('0,5,0,2,10;0,2,0,1,12',2);pulse();assert(stdValue(1)==14)")
    def test_confirmed_negative_diff_still_withdraws_during_pending(self):
        l=fixture();l.execute("net.CheckEvidence(false);pulse();loss(1);pulse();cities[5].active=2;cities[3].active=2;std.SourceChanged(0,5);assert(stdValue(1)==0 and next(std.records['0:1'].applied)==nil)")
    def test_cold_Option_A_keeps_aggregate_until_reliable_history(self):
        l=fixture(False,True);l.execute("cities[3].active=2;knowledge[5]=false;send('0,5,0,2,10;0,3,0,2,11;0,2,0,1,12',3);pulse();assert(std.records['0:1'].loaded and stdValue(1)==14);loss(1);local n=created;pulse();assert(stdValue(1)==0 and created==n and std.records['0:1'].loaded and std.records['0:1'].healthTicket);knowledge[5]={learned={},districts={learned={}}};std.SourceChanged(0,5);assert(stdValue(1)==0 and not std.records['0:1'].loaded and propertyWrites==0)")
    def test_partial_source_unknown_leaves_ticket_dormant_then_history_recovers(self):
        l=fixture();l.execute("knowledge[5]=false;loss(1);local n=created;pulse();assert(stdValue(1)==0 and created==n and std.records['0:1'].healthTicket);knowledge[5]={learned={BUILDING_GRANARY={district='DISTRICT_CITY_CENTER',tier=1}},districts={learned={}}};for i=1,1000 do pulse()end;assert(created==n);std.SourceChanged(0,5);assert(stdValue(1)==14 and not std.records['0:1'].healthTicket)")
    def test_write_failure_keeps_ticket_without_idle_retry(self):
        l=fixture();l.execute("createFail=true;loss(1);pulse();assert(std.errors['0:1']and std.records['0:1'].healthTicket);createFail=false;local n=created;for i=1,1000 do pulse()end;assert(created==n);GameEvents.BuildingPillageStateChanged.Fire(0,1,'BUILDING_SPC_STD_14',false);pulse();assert(stdValue(1)==14 and not std.errors['0:1']and not std.records['0:1'].healthTicket)")
    def test_new_ticket_during_write_cannot_be_acknowledged_by_old_read(self):
        l=fixture();l.execute("local create=P.CreateBuilding;local once=true;P.CreateBuilding=function(q,id)create(q,id);if once then once=false;GameEvents.BuildingPillageStateChanged.Fire(0,q.city.id,id,true)end end;loss(1);pulse();assert(stdValue(1)==14 and std.records['0:1'].healthTicket);local n=created;pulse();assert(created==n and not std.records['0:1'].healthTicket)")
    def test_sibling_health_during_write_survives_next_snapshot(self):
        l=fixture();l.execute("assert(stdValue(2)>0);local create=P.CreateBuilding;local once=true;P.CreateBuilding=function(q,id)create(q,id);if once then once=false;loss(2)end end;loss(1);pulse();assert(stdValue(1)==14 and stdValue(2)==0);pulse();assert(stdValue(2)==14)")
    def test_created_but_readback_unknown_never_creates_twice(self):
        l=fixture();l.execute("local create,has=P.CreateBuilding,P.HasBuilding;local uncertain=false;P.CreateBuilding=function(q,id)create(q,id);if q.city.id==1 then uncertain=true end end;P.HasBuilding=function(b,id)if b.city.id==1 and id=='BUILDING_SPC_STD_14'and uncertain then return nil end;return has(b,id)end;loss(1);pulse();assert(std.errors['0:1']and std.records['0:1'].healthTicket);local n=created;uncertain=false;GameEvents.BuildingPillageStateChanged.Fire(0,1,'BUILDING_SPC_STD_14',false);pulse();assert(created==n and stdValue(1)==14 and not std.records['0:1'].healthTicket)")
    def test_present_pillage_keeps_original_presence_only_policy(self):
        l=fixture();l.execute("local n=created;cities[1].damage.BUILDING_SPC_STD_14=true;GameEvents.BuildingPillageStateChanged.Fire(0,1,'BUILDING_SPC_STD_14',true);pulse();assert(created==n and cities[1].damage.BUILDING_SPC_STD_14 and not std.records['0:1'].healthTicket)")
    def test_busy_changed_scope_preserved_without_owner_widening(self):
        l=fixture();l.execute("std.busy=true;std.Audit({player=0,changed={[1]=true}});std.busy=false;factReads={};pulse();assert(not factReads[2]and not factReads[4]and stdValue(1)==14)")
    def test_unknown_busy_scope_not_lost(self):
        l=fixture();l.execute("cities[5].active=2;std.busy=true;std.Audit();std.busy=false;pulse();assert(stdValue(1)==12)")
    def test_foreign_and_nonowned_health_zero_work(self):
        l=fixture();l.execute("local n=created;factReads={};GameEvents.BuildingPillageStateChanged.Fire(3,1,'BUILDING_SPC_STD_14',true);GameEvents.BuildingPillageStateChanged.Fire(0,1,'BUILDING_LIBRARY',true);pulse();assert(created==n and not next(factReads))")
    def test_actual_SQL_repair_checks_only_current_exact_level_not_all_definitions(self):
        l=sql_fixture();l.execute("assert(#DB.SPC_StandardizationLevels>100);local wanted=0;for _ in pairs(std.records['0:1'].applied)do wanted=wanted+1 end;assert(wanted>0 and wanted<#DB.SPC_StandardizationLevels);P.RemoveBuilding(cities[1].built,target);reads=0;pulse();assert(cities[1].built[target]and reads==wanted+2,reads);local a,b=reads,writes;for i=1,1000 do pulse()end;assert(reads==a and writes==b);reads=0;std.SourceChanged(0,1);assert(reads==0,reads)")
        measure('S5d4c11_SQL_health_budget',{'presence_reads':7,'wanted_targets':5,'all_definitions':1750,'thousand_idle_reads':0,'ordinary_equal_plan_presence_reads':0,'full_level_scan':False})

if __name__=='__main__':unittest.main()
