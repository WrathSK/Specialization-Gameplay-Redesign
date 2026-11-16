"""Verified native signatures and indexed inert-retirement ownership; Lua51 only."""
import unittest
from refactor_harness import Context,legacy_source_observation,measure
from refactor_defect_fixtures import startup


def context():
    c=Context();c.load('RuntimeWork');c.execute("P={Field=function(t,k)return t and t[k]end,Count=function(k)counts[k]=(counts[k]or 0)+1 end,IsTestPlayer=function(p)return p==0 end,Info=function()return {BuildingType='BUILDING_ORDINARY'}end};seen={};function collect(s)seen[#seen+1]=s or {fallback=true}end;function bind(src,n)SPCRuntimeWork.TargetHook(P,src,n,collect)end")
    return c


class Signatures(unittest.TestCase):
    def test_gameevents_building_and_city_exact_city_not_district_type(self):
        c=context();c.execute("bind(GameEvents,'BuildingConstructed');bind(GameEvents,'BuildingPillageStateChanged');bind(GameEvents,'CityBuilt');bind(GameEvents,'OnDistrictConstructed');GameEvents.BuildingConstructed.Fire(0,7,3,100,true);GameEvents.BuildingPillageStateChanged.Fire(0,8,3,true);GameEvents.CityBuilt.Fire(0,9,1,2);GameEvents.OnDistrictConstructed.Fire(0,999,1,2);assert(seen[1].city==7 and seen[2].city==8 and seen[3].city==9 and seen[4].player==0 and seen[4].city==nil and counts.scope_gameevents==4)")
    def test_gameevent_unknown_name_does_not_inherit_events_signature(self):
        c=context();c.execute("bind(GameEvents,'DistrictPillaged');GameEvents.DistrictPillaged.Fire(0,4,7);assert(seen[1].fallback and counts.scope_fallback==1)")
    def test_startup_facades_retain_native_namespace_identity(self):
        c=context();c.load('RuntimeComposition');c.execute("local d=SPCRuntimeComposition.New(shared);assert(d.Run('Adapter',{}, {},function()bind(GameEvents,'BuildingConstructed');bind(Events,'DistrictRemovedFromMap')end));GameEvents.BuildingConstructed.Fire(0,7,3,100,true);Events.DistrictRemovedFromMap.Fire(0,3,8,1,2);assert(seen[1].city==7 and seen[2].city==8 and counts.scope_gameevents==1 and counts.scope_events==1)")
    def test_governor_assignment_both_owners_and_unknown_preserved(self):
        c=context();c.execute("bind(Events,'GovernorAssigned');bind(Events,'GovernorEstablished');bind(Events,'GovernorChanged');Events.GovernorAssigned.Fire(1,7,0,3);assert(#seen==2 and seen[1].player==1 and seen[1].city==nil and seen[2].player==0);Events.GovernorEstablished.Fire(0,8,0,3);assert(#seen==3 and seen[3].city==8);Events.GovernorChanged.Fire(-1);assert(seen[4].player==nil)")
    def test_governor_first_owner_failure_does_not_block_second_owner(self):
        c=context();c.execute("SPCRuntimeWork.TargetHook(P,Events,'GovernorAssigned',function(s)seen[#seen+1]=s;if s.player==1 then error('FIRST_OWNER_FAILURE')end end);assert(not pcall(Events.GovernorAssigned.Fire,1,7,0,3));assert(#seen==2 and seen[1].player==1 and seen[2].player==0)")
    def test_transfer_keeps_new_and_old_owner_without_inventing_old_city_id(self):
        c=context();c.execute("bind(Events,'CityTransfered');Events.CityTransfered.Fire(1,700,0);assert(seen[1].transfer.owner==1 and seen[1].transfer.city==700 and seen[1].transfer.oldOwner==0 and seen[1].city==nil)")
    def test_foreign_pillage_actor_uses_victim_plot_owner_and_unknown_fallback(self):
        c=context();c.execute("bind(GameEvents,'OnPillage');Map={GetPlotByIndex=function(id)assert(id==99);return {GetOwner=function()return 0 end}end};GameEvents.OnPillage.Fire(1,2,3,4,5,99);assert(seen[1].player==0 and seen[1].city==nil);Map.GetPlotByIndex=function()error('PLOT_UNKNOWN')end;GameEvents.OnPillage.Fire(1,2,3,4,5,99);assert(seen[2].player==nil)")
    def test_building_district_position_resolves_city_not_center_only(self):
        c=context();c.execute("bind(Events,'BuildingRemovedFromMap');CityManager={GetDistrictAt=function(x,y)assert(x==10 and y==20);return {GetCity=function()return {GetOwner=function()return 0 end,GetID=function()return 7 end}end}end,GetCityAt=function()error('CENTER_ONLY_FORBIDDEN')end};Events.BuildingRemovedFromMap.Fire(10,20,3,0);assert(seen[1].city==7)")
    def test_internal_buildings_filtered_and_unreadable_position_falls_back_owner(self):
        c=context();c.execute("bind(Events,'BuildingAddedToMap');P.Info=function()return {BuildingType='BUILDING_SPC_INTERNAL'}end;Events.BuildingAddedToMap.Fire(1,2,3,0);assert(#seen==0);P.Info=function()return nil end;CityManager={GetDistrictAt=function()error('UNKNOWN')end};Events.BuildingAddedToMap.Fire(1,2,3,0);assert(#seen==1 and seen[1].player==0 and seen[1].city==nil)")


class Retirement(unittest.TestCase):
    def fixture(self):
        c=context();c.execute("SPCRuntimeWork.StartRetirement(P,shared);r=shared.RuntimeRetirement;calls=0;function city(owner,id,x)local c={owner=owner,id=id,x=x,token='T'};function c:GetOwner()return self.owner end;function c:GetID()return self.id end;function c:GetX()return self.x end;function c:GetY()return 1 end;function c:GetProperty()return self.token end;return c end;function retire(c,tag)return SPCRuntimeWork.RetireOnce(P,shared,c,tag or 'test',function()calls=calls+1;return 1 end)end")
        return c
    def test_one_hook_independent_of_consumer_count_and_known_city_only(self):
        c=self.fixture();c.execute("shared.EffectiveFacts={Read=function()end};for i=1,20 do SPCRuntimeWork.NewTargets(P,shared,function()end,function()end)end;assert(Events.CityRemovedFromMap.Count()==1 and Events.LoadScreenClose.Count()==1);a=city(0,1,10);b=city(0,2,20);retire(a);retire(b);Events.CityRemovedFromMap.Fire(0,1);assert(retire(b)==0 and retire(a)==1 and calls==3)")
        measure('S5d2_twenty_consumer_invalidator',{'consumers':20,'removal_listeners':1,'unrelated_city_retire_calls':0})
    def test_reused_location_replaces_old_index_without_erasing_new_stamp(self):
        c=self.fixture();c.execute("a=city(0,1,10);b=city(1,9,10);retire(a);retire(b);assert(r.count==1);Events.CityRemovedFromMap.Fire(0,1);assert(retire(b)==0 and calls==2);Events.CityRemovedFromMap.Fire(1,9);assert(retire(b)==1 and calls==3 and r.count==1)")
    def test_failures_do_not_publish_clean_stamp_and_load_resets_all(self):
        c=self.fixture();c.execute("a=city(0,1,10);assert(not pcall(SPCRuntimeWork.RetireOnce,P,shared,a,'test',function()error('UNKNOWN')end));assert(r.count==0);retire(a);assert(r.count==1);Events.LoadScreenClose.Fire();assert(r.count==0 and next(r.index)==nil);assert(retire(a)==1)")
    def test_failed_consumer_cannot_quarantine_shared_invalidator(self):
        c=self.fixture();c.load('RuntimeComposition');c.execute("local d=SPCRuntimeComposition.New(shared);assert(not d.Run('Broken',{}, {},function()SPCRuntimeWork.NewTargets(P,shared,function()end,function()end);error('LATE_CONSUMER_FAILURE')end));a=city(0,1,10);retire(a);Events.CityRemovedFromMap.Fire(0,1);assert(retire(a)==1 and calls==2)")
    def test_real_composition_installs_owner_before_consumer_starts(self):
        c=startup();c.execute("SPCResearchSupport.Start=function(P,s)assert(s.RuntimeRetirement and s.StartStatus.RuntimeRetirement.state=='OK');error('CONSUMER_FAILED')end");c.load('Gameplay');c.execute("assert(ExposedMembers.SPC_P0.StartStatus.RuntimeRetirement.state=='OK');assert(Events.CityRemovedFromMap.Count()==1)")
    def test_owner_late_start_failure_skips_only_actual_dependencies(self):
        c=startup();include=c.globals().include
        def injected(name):
            result=include(name)
            if name=='RuntimeWork':c.execute("local start=SPCRuntimeWork.StartRetirement;SPCRuntimeWork.StartRetirement=function(...)start(...);error('RETIREMENT_LATE_FAILURE')end")
            return result
        c.globals().include=injected;c.load('Gameplay')
        c.execute("local s=ExposedMembers.SPC_P0;assert(s.StartStatus.RuntimeRetirement.state=='FAILED' and s.RuntimeRetirement==nil and s.StartStatus.NetworkBridge.state=='OK');for _,n in ipairs({'ResearchSupport','Lv2Housing','Lv2GPP','IndustrySupport','Lv3Support','Lv3Effects','ResearchInfrastructure'})do assert(s.StartStatus[n].state=='SKIPPED_DEPENDENCY',n)end;assert(Events.CityRemovedFromMap.Count()==0)")

if __name__=='__main__':unittest.main()
