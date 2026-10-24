"""Industry exact health and trusted structural D scope; actual BASE transport."""
import unittest
from refactor_harness import legacy_source_observation,ROOT,measure
from test_refactor_s4a import industry,load_industry_ui
from test_refactor_s5c1 import depth


def actual(load=True,two=False):
    l=industry(with_depth=True);l.execute("""
    function fire(n,...)for _,f in ipairs(hooks[n]or{})do f(...)end end
    for _,city in pairs(cities)do
     city.built.GetBuildingLocation=function()return facts[city.id].first.districtID end
    end
    Map.GetPlotIndex=function(x,y)return x end;CityManager={GetDistrictAt=function(x,y)return districts[x]end}
    local remove,create=P.RemoveBuilding,P.CreateBuilding
    P.RemoveBuilding=function(b,id)local plot=b:GetBuildingLocation(id);remove(b,id);fire('BuildingRemovedFromMap',plot,1,id,0)end
    P.CreateBuilding=function(b,id)create(b,id);for _,city in pairs(cities)do if city.built==b then fire('GameEvents.BuildingPillageStateChanged',city.owner,city.id,id,false);break end end end
    function loss(cid,bit)P.RemoveBuilding(cities[cid].built,'BUILDING_SPC_DEV_INDUSTRY_LV1_'..bit)end
    function has(cid,bit)return cities[cid].built['BUILDING_SPC_DEV_INDUSTRY_LV1_'..bit]==true end
    function structural(pid,cid,cause)shared.DistrictCompleteness.MarkDirty(pid,cid,cause)end
    function resetVisits()visits={};industryAudits=0;P.Observe=function(kind,name)if kind=='audit'and name=='IndustrySupport'then industryAudits=industryAudits+1 end end;local read=shared.EffectiveFacts.Read;shared.EffectiveFacts.Read=function(pid,c)visits[c.id]=(visits[c.id]or 0)+1;return read(pid,c)end end
    """)
    if two:l.execute("facts[1]={specialization='INDUSTRY',potential=4,active=4,first={districtID=11,type='DISTRICT_INDUSTRIAL_ZONE'}};districts[11].kind='DISTRICT_INDUSTRIAL_ZONE'")
    if load:load_industry_ui(l)
    return l


class Health(unittest.TestCase):
    def test_exact_food_and_production_loss_no_new_sample_or_idle_retry(self):
        for bit in (-1,1):
            l=actual();l.execute("assert(has(2,"+str(bit)+"));resetVisits();local sent=sends;loss(2,"+str(bit)+");pulse();assert(has(2,"+str(bit)+") and visits[2]==1 and not visits[1] and sends==sent);local w=writes;for i=1,1000 do pulse()end;assert(writes==w and visits[2]==1)")
        measure('S5d4c3_health_one_city',{'health_owner_visits':1,'sibling_visits':0,'new_BASE_requests':0,'thousand_idle_extra_visits':0})
    def test_other_industry_city_loss_while_writing_kept_next_snapshot(self):
        l=actual(two=True);l.execute("assert(has(1,-1) and has(2,-1));local create=P.CreateBuilding;local once=true;P.CreateBuilding=function(b,id)create(b,id);if once and b==cities[2].built then once=false;loss(1,-1)end end;loss(2,-1);pulse();assert(has(2,-1) and not has(1,-1));pulse();assert(has(1,-1))")
    def test_UNKNOWN_and_failed_create_wait_new_health_evidence(self):
        l=actual();l.execute("factUnknown=true;fire('GameEvents.BuildingPillageStateChanged',0,2,'BUILDING_SPC_DEV_INDUSTRY_LV1_-1',false);pulse();assert(has(2,-1) and d.errors['0:2']);factUnknown=false;local w=writes;for i=1,1000 do pulse()end;assert(writes==w);local create=P.CreateBuilding;P.CreateBuilding=function()error('NATIVE_CREATE_FAILURE')end;loss(2,-1);pulse();assert(not has(2,-1) and d.errors['0:2']);P.CreateBuilding=create;w=writes;for i=1,1000 do pulse()end;assert(writes==w);fire('GameEvents.BuildingPillageStateChanged',0,2,'BUILDING_SPC_DEV_INDUSTRY_LV1_-1',false);pulse();assert(has(2,-1) and not d.errors['0:2'])")
    def test_present_pillage_never_adds_new_repair_policy(self):
        l=actual();l.execute("local w=writes;fire('GameEvents.BuildingPillageStateChanged',0,2,'BUILDING_SPC_DEV_INDUSTRY_LV1_-1',true);pulse();assert(has(2,-1) and writes==w)")
    def test_foreign_health_zero(self):
        l=actual();l.execute("resetVisits();fire('GameEvents.BuildingPillageStateChanged',1,2,'BUILDING_SPC_DEV_INDUSTRY_LV1_-1',true);pulse();assert(not next(visits))")
    def test_cold_UNKNOWN_still_owns_exact_current_ids(self):
        l=actual(load=False);l.execute("factUnknown=true;d.Audit({player=0});factUnknown=false;facts[2].active=0;cities[2].built['BUILDING_SPC_DEV_INDUSTRY_LV1_-1']=true;fire('GameEvents.BuildingPillageStateChanged',0,2,'BUILDING_SPC_DEV_INDUSTRY_LV1_-1',false);pulse();assert(not has(2,-1));facts[2].active=1")
        load_industry_ui(l)
        l.execute("assert(has(2,-1));loss(2,-1);pulse();assert(has(2,-1))")


class Causes(unittest.TestCase):
    def test_native_owner_D_recovers_but_UI_only_does_not(self):
        l=actual();l.execute("factUnknown=true;d.Audit({player=0,city=2});factUnknown=false;facts[2].active=0;resetVisits();structural(0,nil,'UI_FACTS_DIRTY');pulse();assert(has(2,-1) and not next(visits));structural(0);pulse();assert(not has(2,-1) and visits[2]==2 and industryAudits==1);local n=visits[2];for i=1,1000 do pulse()end;assert(visits[2]==n)")
    def test_UI_owner_and_native_city_do_not_widen_either_arrival_order(self):
        for first in (True,False):
            l=actual();a="structural(0,nil,'UI_FACTS_DIRTY');structural(0,2)" if first else "structural(0,2);structural(0,nil,'UI_FACTS_DIRTY')"
            l.execute("resetVisits();"+a+";pulse();assert(visits[2]==1 and not visits[1])")
    def test_same_key_UI_and_native_owner_remain_trusted_in_both_orders(self):
        for first in (True,False):
            l=actual();a="structural(0,nil,'UI_FACTS_DIRTY');structural(0)" if first else "structural(0);structural(0,nil,'UI_FACTS_DIRTY')"
            l.execute("resetVisits();"+a+";pulse();assert(visits[1]==1 and visits[2]==1)")
    def test_true_global_dominates_owner_and_city_once(self):
        l=actual();l.execute("resetVisits();structural(0,2);structural(0);structural();pulse();assert(visits[1]==1 and visits[2]==1)")
    def test_original_UI_narrow_gate_and_strict_native_global_complement(self):
        c=depth();c.load('FactConsumerBindings');c.execute("SPCFactConsumerBindings.New(shared);seen={};shared.IndustrySupport={Audit=function(s)seen[#seen+1]=s end};d.MarkDirty(0,1);d.MarkDirty();fc.Flush();shared.FactBindings.Flush();assert(#seen==1 and seen[1].player==nil and seen[1].city==nil)")


class Construction(unittest.TestCase):
    def test_reliable_BASE_first_then_native_construction(self):
        l=actual();l.execute("facts[2].active=0;d.Audit({player=0,city=2});assert(not has(2,-1));facts[2].active=1;resetVisits();fire('GameEvents.OnDistrictConstructed',0,'DISTRICT_INDUSTRIAL_ZONE',12,1);pulse();assert(has(2,-1) and visits[2]==1 and d.ReadBase(0,cities[2])==6)")
    def test_native_construction_first_then_reliable_BASE(self):
        l=actual(load=False);l.execute("fire('GameEvents.OnDistrictConstructed',0,'DISTRICT_INDUSTRIAL_ZONE',12,1);pulse();assert(not has(2,-1) and d.errors['0:2'])")
        load_industry_ui(l)
        l.execute("assert(has(2,-1) and d.ReadBase(0,cities[2])==6 and not d.errors['0:2'])")
    def test_no_D_provider_retains_old_special_constructed_fallback(self):
        l=industry();l.execute("function fire(n,...)for _,f in ipairs(hooks[n]or{})do f(...)end end;CityManager={GetDistrictAt=function(x,y)return districts[x]end}");load_industry_ui(l)
        l.execute("facts[2].active=0;d.Audit({player=0,city=2});facts[2].active=1;fire('GameEvents.OnDistrictConstructed',0,'DISTRICT_INDUSTRIAL_ZONE',12,1);pulse();assert(cities[2].built['BUILDING_SPC_DEV_INDUSTRY_LV1_-1'] and not shared.DistrictCompleteness)")

if __name__=='__main__':unittest.main()
