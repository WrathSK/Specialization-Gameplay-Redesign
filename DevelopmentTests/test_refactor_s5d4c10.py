"""Actual Commerce, native D producer, Bridge, FC and preserved output dependencies."""
import ast
import unittest
import test_culture_network as network
from refactor_harness import ROOT,TrackedLua51,legacy_source_observation,measure

def fixture():
    network.LuaRuntime=TrackedLua51
    with legacy_source_observation():l=network.fixture()
    tree=ast.parse((ROOT/'DevelopmentTests/test_b239_commerce.py').read_text())
    fn=next(n for n in tree.body if isinstance(n,ast.FunctionDef)and n.name=='fixture')
    blocks=[n.value.args[0].value for n in fn.body if isinstance(n,ast.Expr)and isinstance(n.value,ast.Call)and isinstance(n.value.func,ast.Attribute)and n.value.func.attr=='execute'and n.value.args and isinstance(n.value.args[0],ast.Constant)and isinstance(n.value.args[0].value,str)]
    assert len(blocks)==2
    with legacy_source_observation():
        l.globals().include('CommerceModel');l.execute(blocks[0])
        for n in ('FactChanges','NativeFacts','FactConsumerBindings','DistrictCompleteness'):l.globals().include(n)
    l.execute("""
    SPCFactChanges.New(shared);SPCNativeFacts.New(P,shared)
    local read=shared.DistrictCompleteness.ReadFacts
    SPCDistrictCompleteness.Start(P,shared);shared.DistrictCompleteness.ReadFacts=read
    local remove,create=P.RemoveBuilding,P.CreateBuilding
    P.RemoveBuilding=function(b,id)local plot=b:GetBuildingLocation(id);remove(b,id);Events.BuildingRemovedFromMap.Fire(plot,0,id,b.city.owner)end
    P.CreateBuilding=function(q,id)create(q,id);GameEvents.BuildingPillageStateChanged.Fire(q.city.owner,q.city.id,id,false)end
    local info=P.Info;P.Info=function(t,k)if t=='Buildings'and k=='BUILDING_SPC_OTHER_PROFESSION_YIELD'then return {Index=k,BuildingType=k}end;return info(t,k)end
    Map.GetPlotIndex=function(x,y)return x end
    CityManager.GetDistrictAt=function(x,y)local c=cities[x/100];if c then return {GetCity=function()return c end}end end
    function pulse()shared.FactChanges.Flush();shared.FactBindings.Flush();Events.GameCoreEventPublishComplete.Fire()end
    function loss(cid,bit)P.RemoveBuilding(cities[cid]:GetBuildings(),'BUILDING_SPC_COMMERCE_GOLD_'..(bit or 0))end
    """)
    with legacy_source_observation():l.globals().include('Commerce')
    l.execute(blocks[1]);l.execute("SPCFactConsumerBindings.New(shared);pulse();assert(toggle(2,'DISTRICT_CAMPUS',true));pulse();assert(ownedGold(cities[2])==15)")
    return l

class CommerceHealth(unittest.TestCase):
    def test_exact_loss_restores_one_bit_no_permanent_or_idle_writes(self):
        l=fixture();l.execute("local n=commerceWrites;loss(2);local w=com.writes;pulse();assert(ownedGold(cities[2])==15 and com.writes==w+1 and commerceWrites==n);local a,b=created,removed;local r=nativeReads['1:SCIENCE'];for i=1,1000 do pulse()end;assert(created==a and removed==b and nativeReads['1:SCIENCE']==r)")
        measure('S5d4c10_commerce_health',{'repair_writes':1,'permanent_writes':0,'thousand_idle_reads':0})
    def test_access_health_uses_same_current_qualification(self):
        l=fixture();l.execute("P.RemoveBuilding(cities[2]:GetBuildings(),'BUILDING_SPC_COMMERCIALIZATION_ACCESS');pulse();assert(cities[2].present.BUILDING_SPC_COMMERCIALIZATION_ACCESS);cities[2].active=2;Events.GovernorEstablished.Fire(0,2,0);pulse();assert(not cities[2].present.BUILDING_SPC_COMMERCIALIZATION_ACCESS and ownedGold(cities[2])==0)")
    def test_presence_only_pillaged_carrier_not_new_repair_rule(self):
        l=fixture();l.execute("local n=com.writes;cities[2].damage.BUILDING_SPC_COMMERCE_GOLD_0=true;GameEvents.BuildingPillageStateChanged.Fire(0,2,'BUILDING_SPC_COMMERCE_GOLD_0',true);pulse();assert(com.writes==n and cities[2].damage.BUILDING_SPC_COMMERCE_GOLD_0)")
    def test_pending_health_keeps_missing_positive_then_new_proof_restores(self):
        l=fixture();l.execute("net.CheckEvidence(false);pulse();loss(2);local n=com.writes;pulse();assert(ownedGold(cities[2])==14 and com.writes==n and not com.TransactionCurrent(0,2));send('0,4,0,2,10;0,2,0,1,11;0,2,0,5,12',3);pulse();assert(ownedGold(cities[2])==15)")
    def test_continuity_only_health_is_not_positive_repair_proof(self):
        l=fixture();l.execute("units[12]=nil;net.CheckEvidence(false);pulse();assert(net.Input(0).continuityOnly);loss(2);local n=com.writes;pulse();assert(ownedGold(cities[2])==14 and com.writes==n);cities[2].workers=0;Events.CityWorkerChanged.Fire(0,2);pulse();assert(ownedGold(cities[2])==0)")
    def test_UNKNOWN_qualification_and_failed_write_wait_for_new_cause(self):
        l=fixture();l.execute("cities[2].active=nil;loss(2);local n=com.writes;pulse();assert(ownedGold(cities[2])==14 and com.writes==n);cities[2].active=3;GameEvents.BuildingPillageStateChanged.Fire(0,2,'BUILDING_SPC_COMMERCE_GOLD_0',false);pulse();assert(ownedGold(cities[2])==15);createFail=true;loss(2);pulse();assert(view(2).stage=='HELD');createFail=false;local a,b=created,removed;for i=1,1000 do pulse()end;assert(created==a and removed==b);GameEvents.BuildingPillageStateChanged.Fire(0,2,'BUILDING_SPC_COMMERCE_GOLD_0',false);pulse();assert(ownedGold(cities[2])==15)")
    def test_other_output_added_inside_native_write_is_preserved_for_next_publish(self):
        l=fixture();l.execute("local create=P.CreateBuilding;local once=true;P.CreateBuilding=function(q,id)create(q,id);if once and q.city.id==2 then once=false;cities[1].yields.SCIENCE=300;Events.BuildingAddedToMap.Fire(100,0,'BUILDING_SPC_OTHER_PROFESSION_YIELD',0)end end;cities[1].yields.SCIENCE=200;com.SourceChanged(0,1);assert(ownedGold(cities[2])==30);pulse();assert(ownedGold(cities[2])==45)")
    def test_other_output_removed_at_district_coordinates_recomputes_dependency(self):
        l=fixture();l.execute("cities[1].yields.SCIENCE=200;Events.BuildingRemovedFromMap.Fire(100,0,'BUILDING_SPC_OTHER_PROFESSION_YIELD',0);pulse();assert(ownedGold(cities[2])==30)")
    def test_other_internal_pillage_is_source_event_despite_D_filter(self):
        l=fixture();l.execute("cities[1].yields.SCIENCE=300;GameEvents.BuildingPillageStateChanged.Fire(0,1,'BUILDING_SPC_OTHER_PROFESSION_YIELD',true);pulse();assert(ownedGold(cities[2])==45)")
    def test_real_D_event_reaches_commerce_without_old_structure_listener(self):
        l=fixture();l.execute("cities[2].depths.DISTRICT_CAMPUS=4;Events.DistrictBuildProgressChanged.Fire(0,2,2);pulse();assert(ownedGold(cities[2])==20)")
    def test_population_and_policy_during_write_not_blanket_suppressed(self):
        l=fixture();l.execute("local create=P.CreateBuilding;local once=true;P.CreateBuilding=function(q,id)create(q,id);if once then once=false;cities[1].yields.SCIENCE=300;Events.CityPopulationChanged.Fire(0,1)end end;cities[1].yields.SCIENCE=200;com.SourceChanged(0,1);pulse();assert(ownedGold(cities[2])==45);cities[1].yields.SCIENCE=400;Events.ResearchCompleted.Fire(0);pulse();assert(ownedGold(cities[2])==60)")
    def test_real_loss_during_own_creation_survives_next_snapshot(self):
        l=fixture();l.execute("local create=P.CreateBuilding;local once=true;P.CreateBuilding=function(q,id)create(q,id);if once then once=false;P.RemoveBuilding(q.city:GetBuildings(),id)end end;loss(2);pulse();assert(view(2).stage=='HELD');pulse();assert(ownedGold(cities[2])==15)")
    def test_other_city_health_during_creation_retained(self):
        l=fixture();l.execute("cities[3].kind='COMMERCE';cities[3].potential=3;cities[3].active=3;cities[3].depths={DISTRICT_CAMPUS=2};cities[3].yields.SCIENCE=150;com.SourceChanged(0,3);assert(toggle(3,'DISTRICT_CAMPUS',true));pulse();local old=ownedGold(cities[3]);assert(old>0);local create=P.CreateBuilding;local once=true;P.CreateBuilding=function(q,id)create(q,id);if once then once=false;loss(3)end end;loss(2);pulse();assert(ownedGold(cities[2])==15 and ownedGold(cities[3])==old-1);pulse();assert(ownedGold(cities[3])==old)")
    def test_foreign_source_events_do_not_read(self):
        l=fixture();l.execute("local n=nativeReads['1:SCIENCE'];GameEvents.BuildingPillageStateChanged.Fire(3,1,'BUILDING_SPC_OTHER_PROFESSION_YIELD',true);Events.BuildingAddedToMap.Fire(100,0,'BUILDING_SPC_OTHER_PROFESSION_YIELD',3);pulse();assert(nativeReads['1:SCIENCE']==n)")

if __name__=='__main__':unittest.main()
