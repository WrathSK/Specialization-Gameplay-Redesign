"""Actual Engineering SQL + IndustryWonder writer and native ROLE/health owner."""
from functools import lru_cache
import unittest
from refactor_harness import ROOT,TrackedLua51,legacy_source_observation,separate_legacy_event_namespaces,measure
import test_b235_engineering as historical
from test_b235_engineering import SETUP,lua
from refactor_defect_fixtures import startup

@lru_cache(maxsize=1)
def tables():
    historical.Projection.setUpClass()
    try:return historical.Projection.tables
    finally:historical.Projection.tearDownClass()

def fixture(cold=False):
    l=TrackedLua51(unpack_returned_tuples=True)
    l.globals().include=lambda n:l.execute((ROOT/'Mod'/(n+'.lua')).read_text())
    with legacy_source_observation():
        l.execute('DB='+lua(tables()));l.execute(separate_legacy_event_namespaces(SETUP))
        l.execute("""
        print=function()end;era='ERA_RENAISSANCE';P.Call=function(o,k,...)return pcall(o[k],o,...)end
        local info=P.Info;P.Info=function(t,k)if t=='Eras'then for _,r in ipairs(DB.Eras)do if r.EraType==k then return r end end end;return info(t,k)end
        Players[0].GetEra=function()if eraUnknown then error('ERA_UNAVAILABLE')end;return era end
        for _,f in pairs(facts)do f.activeStatus='KNOWN'end;industry(1,4);industry(2,4)
        CityManager={GetCityAt=function(x,y)return cities[x]end};Map={GetPlotIndex=function(x,y)return y*100+x end}
        for _,c in pairs(cities)do c.built.GetBuildingLocation=function()return c:GetY()*100+c:GetX()end end
        local remove,create=P.RemoveBuilding,P.CreateBuilding
        P.RemoveBuilding=function(b,id)remove(b,id);for _,c in pairs(cities)do if c.built==b then emit('BuildingRemovedFromMap',c:GetX(),c:GetY(),id,c:GetOwner());break end end end
        P.CreateBuilding=function(b,id)create(b,id);for _,c in pairs(cities)do if c.built==b then emit('GameEvents.BuildingPillageStateChanged',c:GetOwner(),c:GetID(),id,false);break end end end
        local read=shared.EffectiveFacts.Read;shared.EffectiveFacts.Read=function(pid,c)if c.bad then error('IW_FACTS_UNKNOWN')end;return read(pid,c)end
        function idx(s)return P.Info('Buildings','BUILDING_SPC_WONDER_'..s).Index end
        function has(id,s)return cities[id].built[idx(s)]==true end
        function loss(id,s)P.RemoveBuilding(cities[id].built,idx(s or 'ERA_ANCIENT_30'))end
        function pulse()shared.FactChanges.Flush();emit('GameCoreEventPublishComplete')end
        function resetVisits()factReads={};local coll=Players[0]:GetCities();Players[0].GetCities=function()return {Members=function()error('UNRELATED_CITY_ENUMERATION')end,FindID=coll.FindID}end end
        """)
        for n in ('FactChanges','NativeFacts','IndustryWonderEffects'):l.globals().include(n)
        l.execute('SPCFactChanges.New(shared);SPCNativeFacts.New(P,shared);SPCIndustryWonderEffects.Start(P,shared);w=shared.IndustryWonderEffects')
        if cold:l.execute("facts[1].activeStatus='UNKNOWN';cities[1].built[idx('ERA_ANCIENT_30')]=true")
        l.execute("emit('LoadScreenClose');assert(not w.error,w.error)")
    return l

class WonderHealth(unittest.TestCase):
    def test_cached_projection_loss_repairs_exact_city_without_census_or_sibling_prune(self):
        l=fixture();l.execute("assert(has(1,'ERA_ANCIENT_30')and has(2,'ERA_ANCIENT_30'));resetVisits();loss(1);pulse();assert(has(1,'ERA_ANCIENT_30')and factReads[1]==1 and not factReads[2]and w.records['0:2']);local r,n=reads,writes;for i=1,1000 do pulse()end;assert(reads==r and writes==n and factReads[1]==1)")
        measure('S5d4c8_exact_health',{'city_fact_reads':1,'sibling_fact_reads':0,'thousand_idle_extra_reads':0})
    def test_UNKNOWN_retains_cached_projection_and_does_not_heal_until_new_cause(self):
        l=fixture();l.execute("facts[1].activeStatus='UNKNOWN';loss(1);pulse();assert(not has(1,'ERA_ANCIENT_30')and w.records['0:1'].applied.BUILDING_SPC_WONDER_ERA_ANCIENT_30 and w.errors['0:1']);facts[1].activeStatus='KNOWN';local r,n=reads,writes;for i=1,1000 do pulse()end;assert(reads==r and writes==n);emit('GameEvents.BuildingPillageStateChanged',0,1,idx('ERA_ANCIENT_30'),false);pulse();assert(has(1,'ERA_ANCIENT_30')and not w.errors['0:1'])")
    def test_native_failure_dormant_until_new_health(self):
        l=fixture();l.execute("local create=P.CreateBuilding;P.CreateBuilding=function()error('IW_NATIVE_CREATE_FAILURE')end;loss(1);pulse();assert(w.errors['0:1']and not has(1,'ERA_ANCIENT_30'));P.CreateBuilding=create;local n=writes;for i=1,1000 do pulse()end;assert(writes==n);emit('GameEvents.BuildingPillageStateChanged',0,1,idx('ERA_ANCIENT_30'),false);pulse();assert(has(1,'ERA_ANCIENT_30')and not w.errors['0:1'])")
    def test_sibling_loss_inside_own_create_survives_next_snapshot(self):
        l=fixture();l.execute("local create=P.CreateBuilding;local once=true;P.CreateBuilding=function(b,id)create(b,id);if once then once=false;loss(2)end end;loss(1);pulse();assert(has(1,'ERA_ANCIENT_30')and not has(2,'ERA_ANCIENT_30'));pulse();assert(has(2,'ERA_ANCIENT_30'))")
    def test_same_city_real_loss_inside_create_not_swallowed_by_witness(self):
        l=fixture();l.execute("local create=P.CreateBuilding;local once=true;P.CreateBuilding=function(b,id)create(b,id);if once then once=false;P.RemoveBuilding(b,id)end end;loss(1);pulse();assert(w.errors['0:1']);pulse();assert(has(1,'ERA_ANCIENT_30')and not w.errors['0:1'])")
    def test_present_pillage_keeps_original_presence_only_policy(self):
        l=fixture();l.execute("local n=writes;emit('GameEvents.BuildingPillageStateChanged',0,1,idx('ERA_ANCIENT_30'),true);pulse();assert(writes==n and has(1,'ERA_ANCIENT_30'))")
    def test_foreign_and_nonowned_ids_zero_work(self):
        l=fixture();l.execute("local r,n=reads,writes;factReads={};emit('GameEvents.BuildingPillageStateChanged',64,1,idx('ERA_ANCIENT_30'),true);emit('GameEvents.BuildingPillageStateChanged',0,1,-1,true);pulse();assert(reads==r and writes==n and not next(factReads))")
    def test_cold_UNKNOWN_still_registers_exact_health(self):
        l=fixture(True);l.execute("assert(w.errors['0:1']);facts[1].activeStatus='KNOWN';loss(1);pulse();assert(has(1,'ERA_ANCIENT_30')and not w.errors['0:1'])")
    def test_unknown_native_owner_expands_only_enabled_owners(self):
        l=fixture();l.execute("cities[1].built[idx('ERA_ANCIENT_30')]=nil;cities[2].built[idx('ERA_ANCIENT_30')]=nil;emit('BuildingRemovedFromMap',999,999,idx('ERA_ANCIENT_30'),-1);pulse();assert(has(1,'ERA_ANCIENT_30')and has(2,'ERA_ANCIENT_30'))")
    def test_era_unknown_keeps_projection_then_original_turn_recovers(self):
        l=fixture();l.execute("eraUnknown=true;era='ERA_INDUSTRIAL';emit('PlayerEraChanged',0);assert(has(1,'ERA_MEDIEVAL_10')and w.errors['0:1']);eraUnknown=false;emit('PlayerTurnActivated',0);assert(not has(1,'ERA_MEDIEVAL_10')and has(1,'ERA_MEDIEVAL_20')and not w.errors['0:1'])")
    def test_native_ROLE_known_city_same_turn_changes_no_direct_governor_hooks(self):
        l=fixture();l.execute("assert(#hooks.GovernorEstablished==1 and #hooks.GovernorChanged==1);resetVisits();facts[1].active=3;emit('GovernorEstablished',0,1,0);assert(has(1,'ERA_ANCIENT_30'));pulse();assert(not has(1,'ERA_ANCIENT_30')and has(2,'ERA_ANCIENT_30')and factReads[1]==1 and not factReads[2]);facts[1].active=4;emit('GovernorEstablished',0,1,0);pulse();assert(has(1,'ERA_ANCIENT_30')and factReads[1]==2)")
    def test_cross_owner_ROLE_and_owner_census_prunes_only_absent_city(self):
        l=fixture();l.execute("facts[1].active=3;emit('GovernorAssigned',64,777,0);pulse();assert(not has(1,'ERA_ANCIENT_30'));cities[2]=nil;emit('CityRemovedFromMap',0,2);pulse();assert(not w.records['0:2']and w.records['0:1'])")
    def test_confirmed_exit_exact_carriers_keeps_external(self):
        l=fixture();l.execute("cities[1].built.EXTERNAL=true;cities[1].owner=64;exits.IndustryWonderEffects(cities[1],{origin={owner=0,x=1,y=1}});assert(not w.records['0:1']and cities[1].built.EXTERNAL);for _,r in ipairs(DB.SPC_IndustryWonderEffects)do assert(not cities[1].built[P.Info('Buildings',r.CarrierType).Index])end")
    def test_startup_dependency_failure_skips_wonder_not_store(self):
        c=startup();inc=c.globals().include
        def include(n):
            out=inc(n)
            if n=='NativeFacts':c.execute("SPCNativeFacts.New=function()error('NATIVE_OWNER_FAILURE')end")
            return out
        c.globals().include=include;c.load('Gameplay');c.execute("local s=ExposedMembers.SPC_P0;assert(s.StartStatus.IndustryWonderEffects.state=='SKIPPED_DEPENDENCY'and s.StartStatus.CityProgressionStore.state=='OK')")

if __name__=='__main__':unittest.main()
