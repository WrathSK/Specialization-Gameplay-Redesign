"""Target-owner carrier recovery preserves independent policy and lifecycle; local Lua51."""
import unittest
from refactor_harness import Context,ROOT,legacy_source_observation,measure
from test_refactor_s5d4b2 import active_investment
from test_refactor_s5d4c1 import actual
from refactor_defect_fixtures import startup


def active():
    l=active_investment();l.execute("""
    for _,city in pairs(cities)do
     city.healthLocations={};for id in pairs(city.carriers)do city.healthLocations[id]=city.ds[1].plot end
     local get=city.GetBuildings
     city.GetBuildings=function()local b=get();local loc=b.GetBuildingLocation;b.GetBuildingLocation=function(_,id)if city.healthLocations[id]then return city.healthLocations[id]end;return loc(b,id)end;return b end
    end
    Map.GetPlotIndex=function(x,y)return x end
    CityManager={GetDistrictAt=function(x,y)for _,city in pairs(cities)do for _,district in ipairs(city.ds)do if district.plot==x then return district end end end end}
    P.RemoveBuilding=function(b,id)local plot=b:GetBuildingLocation(id);assert(b.city.carriers[id]);b.city.carriers[id]=nil;b.city.healthLocations[id]=nil;writes=writes+1;fire('BuildingRemovedFromMap',plot,0,id,b.city.owner)end
    P.CreateBuilding=function(q,id)assert(not q.city.carriers[id]);q.city.carriers[id]=true;q.city.healthLocations[id]=q.city.ds[1].plot;writes=writes+1;fire('GameEvents.BuildingPillageStateChanged',q.city.owner,q.city.id,id,false)end
    function pp()shared.FactChanges.Flush();shared.FactBindings.Flush();fire('GameCoreEventPublishComplete')end
    function id(name)return GameInfo.Buildings[name].Index end
    function loss(city,k)P.RemoveBuilding(city:GetBuildings(),k)end
    """);return l


def support():
    from test_b270_event_scope import make_fixture
    with legacy_source_observation():l,_,_=make_fixture(0,True)
    l.execute("""
    other=addCity(0,2,2,0);supportDistricts={};P.Families={DISTRICT_CAMPUS='RESEARCH'};P.Family=function()return 'RESEARCH'end
    for cid,city in pairs(cities[0])do
     local district={GetID=function()return cid+1 end,GetType=function()return 1 end,GetCity=function()return city end,IsComplete=function()return true end,IsPillaged=function()return city.pillaged==true end}
     supportDistricts[#supportDistricts+1]=district
     local get=city.GetBuildings;city.GetBuildings=function()local b=get();b.city=city;b.GetBuildingLocation=function()return city.x end;return b end
     local queue=city.GetBuildQueue;city.GetBuildQueue=function()local q=queue();q.city=city;return q end
    end
    Players[0].GetDistricts=function()return {Members=function()return ipairs(supportDistricts)end}end
    shared.EffectiveFacts.Read=function(pid,city)if city.badFacts then error('TEMPORARY_SUPPORT_FACTS')end;return {specialization='RESEARCH',potential=1,active=1,first={districtID=city.id+1,type='DISTRICT_CAMPUS'},token='T'}end
    Map={GetPlotIndex=function(x,y)return x end};CityManager={GetDistrictAt=function(x,y)for _,v in ipairs(supportDistricts)do if v:GetCity().x==x then return v end end end}
    local remove,create=P.RemoveBuilding,P.CreateBuilding
    P.RemoveBuilding=function(b,id)local plot=b:GetBuildingLocation(id);remove(b,id);Events.BuildingRemovedFromMap.Fire(plot,0,id,b.city.owner)end
    P.CreateBuilding=function(q,id)create(q,id);GameEvents.BuildingPillageStateChanged.Fire(q.city.owner,q.city.id,id,false)end
    s=shared.ResearchSupport;s.Audit({player=0});c=cities[0][0];sid=P.Info('Buildings','BUILDING_SPC_DEV_RESEARCH_SUPPORT').Index
    assert(c.values[sid] and other.values[sid]);function pp()Events.GameCoreEventPublishComplete.Fire()end
    function loss(city)P.RemoveBuilding(city:GetBuildings(),sid)end
    """);return l


class TargetKernel(unittest.TestCase):
    def test_detached_bounded_transfer_and_foreign_target_policy(self):
        c=Context();c.load('RuntimeWork');c.execute("""
        P={IsTestPlayer=function(p)return p==0 end,Field=function(t,k)return t[k]end};data={ready=true};seen={}
        audit,mark,flush=SPCRuntimeWork.NewAudit(P,shared,data,'targets',function(s)seen[#seen+1]=s end,{targets=true})
        data.busy=true;local t={owner=1,city=99,oldOwner=0};audit({transfer=t});t.city=777;audit({player=1,city=5});data.busy=false;publish()
        assert(#seen==2 and seen[1].transfer.city==99 and seen[1].transfer.oldOwner==0 and seen[2].player==1 and seen[2].city==5)
        for i=1,1000 do publish()end;assert(#seen==2)
        local other={ready=true};local n=0;local ordinary=SPCRuntimeWork.NewAudit(P,shared,other,'ordinary',function()n=n+1 end);ordinary({player=1,city=5});assert(n==0)
        """)
    def test_original_foreign_cleanup_and_transfer_regressions_unchanged(self):
        from test_b270_event_scope import EventScopeTests
        case=EventScopeTests()
        with legacy_source_observation():
            case.test_cold_foreign_cleanup_unknown_then_recovery()
            case.test_unreadable_transfer_does_not_latch_audit_busy()
            case.test_nonparticipants_do_not_scale_real_events()
    def test_cold_UNKNOWN_still_registers_static_exact_health_owners(self):
        from test_b270_event_scope import make_fixture
        with legacy_source_observation():l,_,_=make_fixture(0,True,initial_load=False)
        l.execute("local good=shared.EffectiveFacts.Read;shared.EffectiveFacts.Read=function()error('COLD_NATIVE_UNKNOWN')end;Events.LoadScreenClose.Fire();shared.EffectiveFacts.Read=good;local c=cities[0][0];local get=c.GetBuildings;c.GetBuildings=function()local b=get();b.GetBuildingLocation=function()return 0 end;b.IsPillaged=function()return false end;return b end;for _,name in ipairs({'BUILDING_SPC_DEV_RESEARCH_SUPPORT','BUILDING_SPC_DEV_LV2_HOUSING_0','BUILDING_SPC_DEV_GPP_RESEARCH_0','BUILDING_SPC_RESEARCH_INFRA_0'})do local k=P.Info('Buildings',name).Index;c.values[k]=true;GameEvents.BuildingPillageStateChanged.Fire(0,0,k,false)end;Events.GameCoreEventPublishComplete.Fire();for k in pairs(c.values)do error('RETIRED_BASELINE_NOT_CLEARED:'..tostring(k))end")
    def test_original_independent_startup_without_optional_D(self):
        c=startup();c.execute("SPCDistrictCompleteness.Start=function()error('NO_D_PROVIDER')end");c.load('Gameplay');c.execute("assert(ExposedMembers.SPC_P0.StartStatus.ResearchSupport.state=='OK' and ExposedMembers.SPC_P0.StartStatus.Lv2GPP.state=='OK' and ExposedMembers.SPC_P0.StartStatus.Lv2Housing.state=='SKIPPED_DEPENDENCY' and ExposedMembers.SPC_P0.StartStatus.ResearchInfrastructure.state=='SKIPPED_DEPENDENCY')")


class SupportHealth(unittest.TestCase):
    def test_exact_loss_target_city_idle_no_ordinary_D(self):
        l=support();l.execute("resetCounts();loss(c);assert(not c.values[sid]);pp();assert(c.values[sid] and other.values[sid]);local n=counts.city_scan;assert(n==1);for i=1,1000 do pp()end;assert(counts.city_scan==n)")
    def test_other_city_loss_during_write_kept(self):
        l=support();l.execute("local create=P.CreateBuilding;local once=true;P.CreateBuilding=function(q,k)create(q,k);if once and q.city==c and k==sid then once=false;loss(other)end end;loss(c);pp();assert(c.values[sid] and not other.values[sid]);pp();assert(other.values[sid])")
    def test_UNKNOWN_holds_and_new_health_fact_recovers(self):
        l=support();l.execute("c.badFacts=true;GameEvents.BuildingPillageStateChanged.Fire(0,0,sid,false);pp();assert(c.values[sid] and s.errors['0:0']);c.badFacts=false;local n=counts.city_scan;for i=1,1000 do pp()end;assert(counts.city_scan==n);loss(c);pp();assert(c.values[sid] and not s.errors['0:0'])")
    def test_presence_only_pillaged_present_never_rebuilds(self):
        l=support();l.execute("resetCounts();GameEvents.BuildingPillageStateChanged.Fire(0,0,sid,true);pp();assert(c.values[sid] and not counts.building_create and not counts.building_remove)")
    def test_optional_D_absent_preserves_native_structural_recovery(self):
        l=support();l.execute("assert(not shared.DistrictCompleteness);c.pillaged=true;Events.DistrictPillaged.Fire(0,1,0,0,0,1,0,true);assert(not c.values[sid] and other.values[sid]);c.pillaged=false;Events.DistrictPillaged.Fire(0,1,0,0,0,1,0,false);assert(c.values[sid])")


class HousingGPPHealth(unittest.TestCase):
    def test_each_owner_exact_loss_repairs_only_itself_and_city(self):
        for name in ('BUILDING_SPC_DEV_LV2_HOUSING_0','BUILDING_SPC_DEV_GPP_RESEARCH_0'):
            l=active();l.execute("local k=id('"+name+"');local cap=counters.dc_capture;audits={};loss(c,k);pp();assert(c.carriers[k] and counters.dc_capture==cap);local expect='"+('Lv2Housing' if 'HOUSING' in name else 'Lv2GPP')+"';assert(audits[expect]==1);for n in pairs(audits)do assert(n==expect,n)end;local r,w=reads,writes;for i=1,1000 do pp()end;assert(reads==r and writes==w)")
    def test_presence_only_damage_does_not_add_repair_semantics(self):
        l=active();l.execute("local w=writes;fire('GameEvents.BuildingPillageStateChanged',0,1,id('BUILDING_SPC_DEV_LV2_HOUSING_0'),true);fire('GameEvents.BuildingPillageStateChanged',0,1,id('BUILDING_SPC_DEV_GPP_RESEARCH_0'),true);pp();assert(writes==w and housing(c)==1 and gpp(c,'RESEARCH')==6)")
    def test_unknown_GPP_waits_new_external_health_and_not_idle(self):
        l=active();l.execute("local k=id('BUILDING_SPC_DEV_GPP_RESEARCH_0');d.workers=nil;fire('GameEvents.BuildingPillageStateChanged',0,1,k,false);pp();assert(gpp(c,'RESEARCH')==6 and shared.Lv2GPP.errors['0:1']);d.workers=3;local r,w=reads,writes;for i=1,1000 do pp()end;assert(reads==r and writes==w);loss(c,k);pp();assert(gpp(c,'RESEARCH')==6 and not shared.Lv2GPP.errors['0:1'])")
    def test_GPP_failed_create_waits_new_evidence(self):
        l=active();l.execute("local k=id('BUILDING_SPC_DEV_GPP_RESEARCH_0');local create=P.CreateBuilding;P.CreateBuilding=function()error('CREATE_FAILURE')end;loss(c,k);pp();assert(gpp(c,'RESEARCH')==4 and shared.Lv2GPP.errors['0:1']);P.CreateBuilding=create;local r,w=reads,writes;for i=1,1000 do pp()end;assert(reads==r and writes==w);fire('GameEvents.BuildingPillageStateChanged',0,1,k,false);pp();assert(gpp(c,'RESEARCH')==6 and not shared.Lv2GPP.errors['0:1'])")
    def test_ordinary_D_one_each_and_same_turn_second_real_change(self):
        l=active();l.execute("setBuildings(d,{'BUILDING_LIBRARY'});audits={};fire('GameEvents.BuildingPillageStateChanged',0,1,id('BUILDING_LIBRARY'),false);pp();assert(housing(c)==2 and audits.Lv2Housing==1 and audits.Lv2GPP==1);d.bs[1].pillaged=true;fire('GameEvents.BuildingPillageStateChanged',0,1,id('BUILDING_LIBRARY'),true);pp();assert(housing(c)==1 and audits.Lv2Housing==2 and audits.Lv2GPP==2 and turn==1)")


class InfrastructureHealth(unittest.TestCase):
    def test_exact_loss_and_pillage_keep_existing_repair_policy(self):
        l=actual();l.execute("infra=shared.ResearchInfrastructure;infra.Audit({player=0,city=1});local k=GameInfo.Buildings.BUILDING_SPC_RESEARCH_INFRA_0.Index;assert(cities[1].carriers[k]);local cap=counters.dc_capture;external(cities[1],k);pp();assert(cities[1].carriers[k] and counters.dc_capture==cap);cities[1].damage[k]=true;fire('GameEvents.BuildingPillageStateChanged',0,1,k,true);pp();assert(cities[1].carriers[k] and not cities[1].damage[k] and not infra.errors[0][1]);local r,w=reads,writes;for i=1,1000 do pp()end;assert(reads==r and writes==w)")
    def test_other_city_loss_during_repair_survives(self):
        l=actual();l.execute("infra=shared.ResearchInfrastructure;infra.Audit();local k=GameInfo.Buildings.BUILDING_SPC_RESEARCH_INFRA_0.Index;local create=P.CreateBuilding;local once=true;P.CreateBuilding=function(q,id)create(q,id);if once and q.city==cities[1] and id==k then once=false;external(cities[2],id)end end;external(cities[1],k);pp();assert(cities[1].carriers[k] and not cities[2].carriers[k]);pp();assert(cities[2].carriers[k])")

if __name__=='__main__':unittest.main()
