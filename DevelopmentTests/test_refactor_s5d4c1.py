"""Exact carrier health, scoped structural replacement and faithful native doubles."""
import unittest
from refactor_harness import Context,ROOT,legacy_source_observation,measure
from refactor_defect_fixtures import fact_publication_profile,startup
from test_refactor_s5d1 import research,cross


def helper():
    c=Context();c.load('RuntimeWork');c.execute("""
    P={Field=function(t,k)return t and t[k]end,IsTestPlayer=function(pid)return pid==0 end,Info=function()error('HEALTH_METADATA_MUST_BE_CACHED')end};seen={};data={}
    a={GetOwner=function()return 0 end,GetID=function()return 1 end,GetBuildings=function()return {GetBuildingLocation=function()return 100 end}end,GetBuildQueue=function()return {}end}
    Map={GetPlotIndex=function(x,y)return x end};CityManager={GetDistrictAt=function()return {GetCity=function()return a end}end}
    h=SPCRuntimeWork.NativeHealth(P,shared,data,function(id)return id==7 or id==8 end,function(s)seen[#seen+1]=s end)
    P.RemoveBuilding=function(b,id)Events.BuildingRemovedFromMap.Fire(100,0,id,0);return 'REMOVED'end
    P.CreateBuilding=function(q,id)GameEvents.BuildingPillageStateChanged.Fire(0,1,id,false);return 'CREATED'end
    """);return c


def actual():
    l=research()
    with legacy_source_observation():fact_publication_profile(l,False)
    l.execute("""
    for _,city in pairs(cities)do
     city.damage={};local get=city.GetBuildings
     city.GetBuildings=function()local b=get();local pill=b.IsPillaged;b.IsPillaged=function(_,id)if city.damage[id]then return true end;return pill(b,id)end;return b end
    end
    rawRemove=P.RemoveBuilding;local create=P.CreateBuilding
    P.CreateBuilding=function(q,id)create(q,id);q.city.damage[id]=nil;fire('GameEvents.BuildingPillageStateChanged',q.city.owner,q.city.id,id,false)end
    function pp()shared.FactChanges.Flush();shared.FactBindings.Flush();fire('GameCoreEventPublishComplete')end
    function chairID(bit)return GameInfo.Buildings['BUILDING_SPC_RESEARCH_CHAIR_BUILDING_LIBRARY_'..bit].Index end
    function external(city,id)rawRemove(city:GetBuildings(),id)end
    """);return l


def actual_cross():
    l=cross();l.execute("""
    -- Supplement only native location/damage/removal callbacks; retain real BASE
    -- protocol, facts, policy, signed encoding and writer. Legacy IDs are names.
    for _,city in pairs(cities)do
     city.damage={};city.built.GetBuildingLocation=function()return facts[city.id].first.districtID end
     city.built.IsPillaged=function(_,id)return city.damage[id]==true end
    end
    Map.GetPlotIndex=function(x,y)return x end
    CityManager={GetDistrictAt=function(x,y)return districts[x]end}
    local remove,create=P.RemoveBuilding,P.CreateBuilding
    P.RemoveBuilding=function(b,id)local plot=b:GetBuildingLocation(id);remove(b,id);fire('BuildingRemovedFromMap',plot,1,id,0)end
    P.CreateBuilding=function(b,id)create(b,id);for _,city in pairs(cities)do if city.built==b then city.damage[id]=nil;fire('GameEvents.BuildingPillageStateChanged',city.owner,city.id,id,false);break end end end
    function crossID(bit)return 'BUILDING_SPC_RESEARCH_CROSS_POS_'..bit end
    function externalCross(bit)P.RemoveBuilding(cities[1].built,crossID(bit))end
    """);return l


class Witness(unittest.TestCase):
    def test_exact_self_operations_suppressed_but_damage_always_kept(self):
        c=helper();c.execute("assert(h.Remove(a,7,100)=='REMOVED' and #seen==0);assert(h.Create(a,7,100)=='CREATED' and #seen==0);GameEvents.BuildingPillageStateChanged.Fire(0,1,7,true);assert(#seen==1 and seen[1].city==1);GameEvents.BuildingPillageStateChanged.Fire(0,1,7,false);assert(#seen==2)")
    def test_failure_restores_witness_including_object_getter_throw(self):
        c=helper();c.execute("local get=a.GetBuildings;a.GetBuildings=function()error('GETTER_FAILED')end;assert(not pcall(h.Remove,a,7,100));a.GetBuildings=get;Events.BuildingRemovedFromMap.Fire(100,0,7,0);assert(#seen==1);P.RemoveBuilding=function()error('NATIVE_REMOVE_FAILED')end;assert(not pcall(h.Remove,a,7,100));Events.BuildingRemovedFromMap.Fire(100,0,7,0);assert(#seen==2)")
    def test_nested_removal_restores_outer_exact_witness(self):
        c=helper();c.execute("P.RemoveBuilding=function(b,id)if id==7 then assert(h.Remove(a,8,100)=='INNER');Events.BuildingRemovedFromMap.Fire(100,0,7,0);return 'OUTER'end;Events.BuildingRemovedFromMap.Fire(100,0,8,0);return 'INNER'end;assert(h.Remove(a,7,100)=='OUTER' and #seen==0);Events.BuildingRemovedFromMap.Fire(100,0,7,0);assert(#seen==1)")
    def test_unknown_position_cannot_be_guessed_as_self_removal(self):
        c=helper();c.execute("Map.GetPlotIndex=function()error('PLOT_UNAVAILABLE')end;h.Remove(a,7,100);assert(#seen==1)")
    def test_owner_conflict_and_known_foreign_are_scoped_safely(self):
        c=helper();c.execute("CityManager.GetDistrictAt=function()return {GetCity=function()return {GetOwner=function()return 1 end,GetID=function()return 900 end}end}end;Events.BuildingRemovedFromMap.Fire(100,0,7,0);assert(#seen==1 and seen[1].player==0 and seen[1].city==nil);CityManager.GetDistrictAt=function()return {GetCity=function()return a end}end;Events.BuildingRemovedFromMap.Fire(100,0,7,1);assert(#seen==1)")
    def test_ordinary_and_unowned_ids_do_no_health_work_unknown_owner_kept(self):
        c=helper();c.execute("Events.BuildingRemovedFromMap.Fire(100,0,99,0);GameEvents.BuildingPillageStateChanged.Fire(0,1,99,true);assert(#seen==0);CityManager.GetDistrictAt=function()error('CITY_UNAVAILABLE')end;Events.BuildingRemovedFromMap.Fire(100,0,7,-1);assert(#seen==1 and seen[1].player==nil)")


class ResearchHealth(unittest.TestCase):
    def test_external_Chair_loss_recovers_exact_city_with_no_D_capture_or_other_writer(self):
        l=actual();l.execute("auditCounts={};P.Observe=function(kind,name)if kind=='audit'then auditCounts[name]=(auditCounts[name]or 0)+1 end end;local cap=counters.dc_capture;external(cities[1],chairID(0));assert(cc('BUILDING_LIBRARY')==2);pp();assert(cc('BUILDING_LIBRARY')==3 and cc('BUILDING_LIBRARY',cities[2])==3 and auditCounts.ResearchChair==1 and not auditCounts.ResearchApply and counters.dc_capture==cap);local r,w=reads,writes;for i=1,1000 do pp()end;assert(reads==r and writes==w)")
        measure('S5d4c1_exact_health',{'changed_cities':1,'writer_audits':1,'D_recaptures':0,'other_writer_audits':0,'thousand_idle_extra_reads':0})
    def test_live_pillage_repairs_without_dead_events_and_does_not_rearm_self(self):
        l=actual();l.execute("local id=chairID(0);cities[1].damage[id]=true;fire('GameEvents.BuildingPillageStateChanged',0,1,id,true);pp();assert(not cities[1].damage[id] and cc('BUILDING_LIBRARY')==3);local r,w=reads,writes;for i=1,1000 do pp()end;assert(reads==r and writes==w)")
    def test_other_city_loss_during_health_write_survives_to_next_snapshot(self):
        l=actual();l.execute("local create=P.CreateBuilding;local once=true;P.CreateBuilding=function(q,id)create(q,id);if once and q.city==cities[1] and id==chairID(0)then once=false;external(cities[2],id)end end;external(cities[1],chairID(0));pp();assert(cc('BUILDING_LIBRARY')==3 and cc('BUILDING_LIBRARY',cities[2])==2);pp();assert(cc('BUILDING_LIBRARY',cities[2])==3)")
    def test_unlocated_other_city_loss_is_not_hidden_by_current_write(self):
        l=actual();l.execute("local create=P.CreateBuilding;local at=CityManager.GetDistrictAt;local once=true;P.CreateBuilding=function(q,id)create(q,id);if once and q.city==cities[1] and id==chairID(0)then once=false;CityManager.GetDistrictAt=function()error('B_TEMPORARILY_UNLOCATED')end;external(cities[2],id);CityManager.GetDistrictAt=at end end;external(cities[1],chairID(0));pp();assert(cc('BUILDING_LIBRARY',cities[2])==2);pp();assert(cc('BUILDING_LIBRARY')==3 and cc('BUILDING_LIBRARY',cities[2])==3)")
    def test_confirmed_damage_during_creation_is_not_suppressed(self):
        l=actual();l.execute("local create=P.CreateBuilding;local once=true;P.CreateBuilding=function(q,id)create(q,id);if once and q.city==cities[1] and id==chairID(0)then once=false;q.city.damage[id]=true;fire('GameEvents.BuildingPillageStateChanged',0,1,id,true)end end;external(cities[1],chairID(0));pp();assert(cities[1].damage[chairID(0)]);pp();assert(not cities[1].damage[chairID(0)] and cc('BUILDING_LIBRARY')==3)")
    def test_unknown_holds_and_failed_create_waits_new_external_health_evidence(self):
        l=actual();l.execute("cities[1].factsError=true;fire('GameEvents.BuildingPillageStateChanged',0,1,chairID(0),false);pp();assert(cc('BUILDING_LIBRARY')==3 and chair.errors[0][1]);cities[1].factsError=false;local r,w=reads,writes;for i=1,1000 do pp()end;assert(reads==r and writes==w);local create=P.CreateBuilding;P.CreateBuilding=function()error('CREATE_FAILED')end;external(cities[1],chairID(0));pp();assert(cc('BUILDING_LIBRARY')==2 and chair.errors[0][1]);r=reads;w=writes;for i=1,1000 do pp()end;assert(reads==r and writes==w);P.CreateBuilding=create;fire('GameEvents.BuildingPillageStateChanged',0,1,chairID(0),false);pp();assert(cc('BUILDING_LIBRARY')==3 and not chair.errors[0][1])")
    def test_actual_apply_health_uses_exact_own_ID(self):
        l=actual();l.execute("local zone=addDistrict(cities[1],99,'DISTRICT_INDUSTRIAL_ZONE');setBuildings(zone,{'BUILDING_WORKSHOP','BUILDING_FACTORY'});shared.DistrictCompleteness.MarkDirty(0,1);shared.ResearchApply.Audit({player=0,city=1});local id;for candidate in pairs(cities[1].carriers)do local row=GameInfo.Buildings[candidate];if row.BuildingType:match('^BUILDING_SPC_RESEARCH_APPLY_')then id=candidate;break end end;assert(id);external(cities[1],id);assert(not cities[1].carriers[id]);pp();assert(cities[1].carriers[id] and not shared.ResearchApply.errors[0][1])")
    def test_scoped_D_replacement_remains_one_Audit_per_writer(self):
        l=actual();l.execute("auditCounts={};P.Observe=function(kind,name)if kind=='audit'then auditCounts[name]=(auditCounts[name]or 0)+1 end end;fire('GameEvents.BuildingPillageStateChanged',0,1,GameInfo.Buildings.BUILDING_LIBRARY.Index,true);pp();assert(auditCounts.ResearchApply==1 and auditCounts.ResearchChair==1)")
    def test_actual_cross_external_loss_recovers_without_new_BASE(self):
        l=actual_cross();l.execute("local sent=sends;externalCross(0);assert(not cities[1].built[crossID(0)]);fire('GameCoreEventPublishComplete');assert(cities[1].built[crossID(0)] and not d.errors[0][1] and sends==sent);local w,rd,sc=writes,reads,total('city_scan');for i=1,1000 do fire('GameCoreEventPublishComplete')end;assert(writes==w and reads==rd and total('city_scan')==sc)")
    def test_actual_cross_pillage_repairs_through_exact_health(self):
        l=actual_cross();l.execute("local id=crossID(0);cities[1].damage[id]=true;fire('GameEvents.BuildingPillageStateChanged',0,1,id,true);fire('GameCoreEventPublishComplete');assert(cities[1].built[id] and not cities[1].damage[id] and not d.errors[0][1]);local w=writes;for i=1,1000 do fire('GameCoreEventPublishComplete')end;assert(writes==w)")
    def test_actual_cross_UNKNOWN_holds_then_reliable_sample_recovers(self):
        l=actual_cross();l.execute("local id=crossID(0);d.samples[0]=nil;cities[1].damage[id]=true;fire('GameEvents.BuildingPillageStateChanged',0,1,id,true);local w=writes;fire('GameCoreEventPublishComplete');assert(writes==w and cities[1].damage[id] and d.errors[0][1]);for i=1,1000 do fire('GameCoreEventPublishComplete')end;assert(writes==w);districts[13].base=7;fire('FeatureAddedToMap');pulse();assert(cities[1].built[id] and not cities[1].damage[id] and not d.errors[0][1])")
    def test_cross_direct_structural_fallback_only_without_D_provider(self):
        c=startup();c.execute("SPCDistrictCompleteness.Start=function()error('NO_D_PROVIDER')end");c.load('Gameplay');c.execute("assert(ExposedMembers.SPC_P0.StartStatus.ResearchCross.state=='OK')")
        l=cross();l.execute("assert(not shared.DistrictCompleteness);local before=total('city_scan');fire('DistrictBuildProgressChanged',0,11,1);fire('GameCoreEventPublishComplete');assert(total('city_scan')==before+1)")

if __name__=='__main__':unittest.main()
