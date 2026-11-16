"""S5d4a sole D native producer/live repair and real dependent closure."""
import unittest
from refactor_harness import ROOT,legacy_source_observation,measure
from test_refactor_s5c1 import depth
from test_refactor_s5propagation import investment


class NativeDepth(unittest.TestCase):
    def test_measured_dead_events_absent_live_building_pillage_and_repair_same_turn(self):
        c=depth();c.execute("""
        for _,n in ipairs({'CityBuildingsChanged','BuildingPillaged','BuildingRepaired','DistrictRepaired'})do assert(Events[n].Count()==0);Events[n]=false end
        local get=cities[1].GetBuildings;local pillaged=false;cities[1].GetBuildings=function()local b=get();b.IsPillaged=function()return pillaged end;return b end
        assert(sample(1).value.domains.DISTRICT_CAMPUS.value==1);sample(2);resetCounts()
        pillaged=true;GameEvents.BuildingPillageStateChanged.Fire(0,1,1,true);sample(2);assert(not counts.dc_capture);assert(sample(1).value.domains.DISTRICT_CAMPUS.value==0 and counts.dc_capture==1)
        pillaged=false;GameEvents.BuildingPillageStateChanged.Fire(0,1,1,false);assert(sample(1).value.domains.DISTRICT_CAMPUS.value==1 and counts.dc_capture==2 and turn==1)
        """)
    def test_district_removal_preserves_known_city_scope(self):
        c=depth();c.execute("sample(1);sample(2);resetCounts();Events.DistrictRemovedFromMap.Fire(0,99,1,10,20,3);sample(2);assert(not counts.dc_capture);sample(1);assert(counts.dc_capture==1)")
    def test_state_bearing_live_district_hook_handles_false_repair(self):
        c=depth();c.execute("sample(1);sample(2);resetCounts();Events.DistrictPillaged.Fire(0,99,1,10,20,3,100,true);sample(1);Events.DistrictPillaged.Fire(0,99,1,10,20,3,100,false);sample(1);sample(2);assert(counts.dc_capture==2)")
    def test_gameplay_constructed_city_and_district_type_not_misread(self):
        c=depth();c.execute("sample(1);sample(2);resetCounts();GameEvents.BuildingConstructed.Fire(0,1,1,100,true);sample(2);assert(not counts.dc_capture);sample(1);assert(counts.dc_capture==1);GameEvents.CityBuilt.Fire(0,2,2,0);sample(1);assert(counts.dc_capture==1);sample(2);assert(counts.dc_capture==2);GameEvents.OnDistrictConstructed.Fire(0,999,1,0);sample(1);sample(2);assert(counts.dc_capture==4)")
    def test_pillage_actor_and_victim_scope_are_not_confused(self):
        c=depth();c.execute("sample(1);sample(2);resetCounts();Map.GetPlotByIndex=function()return {GetOwner=function()return 1 end}end;GameEvents.OnPillage.Fire(0,1,0,0,0,99);sample(1);sample(2);assert(not counts.dc_capture);Map.GetPlotByIndex=function()return {GetOwner=function()return 0 end}end;GameEvents.OnPillage.Fire(1,1,0,0,0,99);sample(1);sample(2);assert(counts.dc_capture==2)")
    def test_internal_carrier_state_cannot_redirty_ordinary_depth(self):
        c=depth();c.execute("sample(1);local seq=fc.sequence;local info=P.Info;P.Info=function(t,k)if k==99 then return {BuildingType='BUILDING_SPC_OWNED'}end;return info(t,k)end;GameEvents.BuildingPillageStateChanged.Fire(0,1,99,true);GameEvents.BuildingConstructed.Fire(0,1,99,100,true);Events.BuildingRemovedFromMap.Fire(1,0,99,0);sample(1);assert(fc.sequence==seq and counts.dc_capture==1)")
    def test_district_building_coordinate_resolution_uses_single_city(self):
        c=depth();c.execute("sample(1);sample(2);resetCounts();CityManager={GetDistrictAt=function()return {GetCity=function()return cities[1]end}end,GetCityAt=function()error('CENTER_ONLY_FORBIDDEN')end};Events.BuildingRemovedFromMap.Fire(1,0,1,0);sample(2);assert(not counts.dc_capture);sample(1);assert(counts.dc_capture==1)")
    def test_current_resolved_owner_does_not_drop_reliable_former_event_owner(self):
        c=depth();c.execute("sample(1);sample(2);resetCounts();CityManager={GetDistrictAt=function()return {GetCity=function()return {GetOwner=function()return 1 end,GetID=function()return 900 end}end}end};Events.BuildingRemovedFromMap.Fire(1,0,1,0);sample(1);sample(2);assert(counts.dc_capture==2 and fc.pending==1)")
    def test_reliable_foreign_event_owner_cannot_create_local_coordinate_work(self):
        c=depth();c.execute("sample(1);sample(2);resetCounts();CityManager={GetDistrictAt=function()return {GetCity=function()return cities[1]end}end};local seq=fc.sequence;Events.BuildingAddedToMap.Fire(1,0,1,1);sample(1);sample(2);assert(not counts.dc_capture and fc.sequence==seq)")
    def test_pillage_mixed_internal_building_field_does_not_hide_district_change(self):
        c=depth();c.execute("sample(1);sample(2);resetCounts();local info=P.Info;P.Info=function(t,k)if k==99 then return {BuildingType='BUILDING_SPC_OWNED'}end;return info(t,k)end;Map.GetPlotByIndex=function()return {GetOwner=function()return 0 end}end;GameEvents.OnPillage.Fire(1,1,0,99,7,100);sample(1);sample(2);assert(counts.dc_capture==2)")
    def test_unknown_owner_fallback_and_known_foreign_no_native_mark(self):
        c=depth();c.execute("sample(1);sample(2);resetCounts();GameEvents.BuildingPillageStateChanged.Fire(1,1,1,true);sample(1);sample(2);assert(not counts.dc_capture);GameEvents.BuildingPillageStateChanged.Fire(nil,nil,1,true);assert(not counts.dc_capture);sample(1);sample(2);assert(counts.dc_capture==2)")


def support():
    from test_b270_event_scope import make_fixture
    with legacy_source_observation():
        lua, _, _ = make_fixture(0, True)
        for name in ('FactChanges', 'FactConsumerBindings'):
            lua.execute((ROOT / 'Mod' / (name + '.lua')).read_text())
    lua.execute("""
    fc=SPCFactChanges.New(shared);bindings=SPCFactConsumerBindings.New(shared)
    city=cities[0][0];pillaged=false
    P.Families={DISTRICT_CAMPUS='RESEARCH'};P.Family=function()return 'RESEARCH'end
    local district={GetID=function()return 1 end,GetType=function()return 1 end,GetCity=function()return city end,IsComplete=function()return true end,IsPillaged=function()return pillaged end}
    Players[0].GetDistricts=function()return {Members=function()return ipairs({district})end}end
    shared.EffectiveFacts.Read=function()return {specialization='RESEARCH',potential=1,active=1,first={districtID=1,type='DISTRICT_CAMPUS'},token='T'}end
    owner=shared.ResearchSupport;owner.Audit({player=0,city=0})
    carrier=P.Info('Buildings','BUILDING_SPC_DEV_RESEARCH_SUPPORT').Index
    assert(city.values[carrier])
    function emit(cause)fc.Emit({owner=0,cityID=0,kinds={'D'},cause=cause})end
    function drain()fc.Flush();bindings.Flush()end
    """)
    return lua


class Consumers(unittest.TestCase):
    def test_actual_housing_live_pillage_state_updates_from_D_subscription(self):
        l=investment();l.execute("""
        t=prepare(c,401,false);drain();confirm(c,401,t,false);drain();assert(housing(c)==1)
        setBuildings(d,{'BUILDING_LIBRARY'});svc.MarkDirty(0,1);shared.Lv2Housing.Audit({player=0,city=1});assert(housing(c)==2)
        local lib=GameInfo.Buildings.BUILDING_LIBRARY.Index;d.bs[1].pillaged=true
        fire('GameEvents.BuildingPillageStateChanged',0,1,lib,true);assert(housing(c)==2);drain();assert(housing(c)==1)
        d.bs[1].pillaged=false;fire('GameEvents.BuildingPillageStateChanged',0,1,lib,false);drain();assert(housing(c)==2 and turn==1)
        """)
    def test_actual_support_anchor_health_receives_D_without_extra_ACTIVE(self):
        l=support();l.execute("""
        pillaged=true;emit('ANCHOR_STATE_CHANGED');drain();assert(not city.values[carrier])
        pillaged=false;emit('ANCHOR_REPAIRED');drain();assert(city.values[carrier])
        """)

    def test_actual_support_refusal_preserves_only_its_receipt_until_a_named_wake(self):
        l=support();l.execute("""
        local sibling=0
        fc.RegisterConsumer('Sibling',function()sibling=sibling+1 end,{kinds={'D'}})
        local name='Binding_ResearchSupport'
        owner.busy=true;pillaged=true;emit('ANCHOR_STATE_CHANGED');drain()
        assert(city.values[carrier] and fc.errors[name] and sibling==1)
        owner.busy=false;local n=fc.delivered
        for i=1,50 do drain()end
        assert(city.values[carrier] and fc.delivered==n)
        assert(bindings.Wake('ResearchSupport','TARGET_READY',fc.sequence,{player=0,city=0}))
        drain()
        assert(not city.values[carrier] and not fc.errors[name] and sibling==1)
        """)

if __name__=='__main__':unittest.main()
