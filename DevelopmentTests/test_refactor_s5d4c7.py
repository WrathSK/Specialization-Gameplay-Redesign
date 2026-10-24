"""Actual Store/investment/age authority composed with Tradition projection-only health."""
import unittest
from refactor_harness import ROOT,legacy_source_observation,measure
from test_refactor_s5a2 import actual_store


def fixture(cold_unknown=False):
    l=actual_store();l.execute("""
    T.start();c=T.research(1);other=T.research(2)
    GameConfiguration.GetGameSpeedType=function()return 'STANDARD'end;GameInfo.GameSpeeds={STANDARD={CostMultiplier=100}}
    local info=P.Info;meta={};for _,amount in ipairs({5,10,15,20,25})do
     local row={Index=900+amount,BuildingType='BUILDING_SPC_RESEARCH_TRADITION_'..amount,InternalOnly=true,PrereqDistrict='DISTRICT_CITY_CENTER',CitizenSlots=0,Housing=0}
     meta[row.Index]=row;meta[row.BuildingType]=row
    end
    P.Info=function(kind,k)return kind=='Buildings'and meta[k]or info(kind,k)end
    for _,city in ipairs({c,other})do
     city.fx={};city.damage={};local bs={city=city}
     bs.GetBuildingLocation=function()return city:GetY()*200+city:GetX()end
     bs.IsPillaged=function(_,id)return city.damage[id]==true end
     city.GetBuildings=function()return bs end;city.GetBuildQueue=function()return {city=city}end
    end
    Map.GetPlotIndex=function(x,y)return y*200+x end
    P.HasBuilding=function(b,id)fxReads=(fxReads or 0)+1;return b.city.fx[id]==true end
    P.CreateBuilding=function(q,id)if failCreate then error('NATIVE_CREATE_FAILURE')end;assert(not q.city.fx[id]);q.city.fx[id]=true;q.city.damage[id]=nil;fxWrites=(fxWrites or 0)+1;GameEvents.BuildingPillageStateChanged.Fire(q.city:GetOwner(),q.city:GetID(),id,false)end
    P.RemoveBuilding=function(b,id)if failRemove then error('NATIVE_REMOVE_FAILURE')end;assert(b.city.fx[id]);b.city.fx[id]=nil;fxWrites=(fxWrites or 0)+1;Events.BuildingRemovedFromMap.Fire(b.city:GetX(),b.city:GetY(),id,b.city:GetOwner())end
    function current(city)local total=0;for _,n in ipairs({5,10,15,20,25})do if city.fx[900+n]and not city.damage[900+n]then total=total+n end end;return total end
    function history()return T.encode({T.snapshot(c),T.snapshot(other)})end
    function loss(city,id)P.RemoveBuilding(city:GetBuildings(),id or 905)end
    """)
    for module in ('ResearchTraditionEffects','NativeFacts','FactConsumerBindings'):
        with legacy_source_observation():l.globals().include(module)
    l.execute("SPCNativeFacts.New(P,shared);SPCFactConsumerBindings.New(shared);SPCResearchTraditionEffects.Start(P,shared);effects=shared.ResearchTraditionEffects;function pp()shared.FactChanges.Flush();shared.FactBindings.Flush();Events.GameCoreEventPublishComplete.Fire()end")
    if cold_unknown:l.execute('T.governor(nil);c.fx[905]=true;other.fx[905]=true')
    l.execute('pp()')
    if not cold_unknown:l.execute('assert(current(c)==5 and current(other)==5)')
    return l


class TraditionHealth(unittest.TestCase):
    def test_external_loss_exact_city_no_history_or_age_write(self):
        l=fixture();l.execute("local before=history();local n=T.writes();fxReads=0;loss(c);pp();assert(current(c)==5 and current(other)==5 and history()==before and T.writes()==n);assert(fxReads>0);local r,w=fxReads,fxWrites;for i=1,1000 do pp()end;assert(fxReads==r and fxWrites==w and history()==before and T.writes()==n)")
        measure('S5d4c7_Tradition_health',{'permanent_writes':0,'history_changes':0,'thousand_idle_extra_reads':0})
    def test_pillage_repairs_projection_only(self):
        l=fixture();l.execute("local before=history();local n=T.writes();c.damage[905]=true;GameEvents.BuildingPillageStateChanged.Fire(0,c:GetID(),905,true);pp();assert(current(c)==5 and not c.damage[905]and history()==before and T.writes()==n)")
    def test_sibling_loss_during_health_write_survives_next_snapshot(self):
        l=fixture();l.execute("local create=P.CreateBuilding;local once=true;P.CreateBuilding=function(q,id)create(q,id);if once and q.city==c then once=false;loss(other)end end;loss(c);pp();assert(current(c)==5 and current(other)==0);pp();assert(current(other)==5)")
    def test_private_busy_and_synchronous_publish_cannot_consume_sibling_cause(self):
        l=fixture();l.execute("local before=history();local create=P.CreateBuilding;local once=true;P.CreateBuilding=function(q,id)create(q,id);if once and q.city==c then once=false;loss(other);Events.GameCoreEventPublishComplete.Fire();assert(current(other)==0)end end;c.fx[905]=nil;effects.Update(0,c);assert(current(c)==5 and current(other)==0);pp();assert(current(other)==5 and history()==before)")
    def test_damage_during_native_create_is_not_suppressed(self):
        l=fixture();l.execute("local create=P.CreateBuilding;local once=true;P.CreateBuilding=function(q,id)create(q,id);if once and q.city==c then once=false;c.damage[id]=true;GameEvents.BuildingPillageStateChanged.Fire(0,c:GetID(),id,true)end end;loss(c);pp();assert(c.damage[905]);pp();assert(current(c)==5 and not c.damage[905])")
    def test_qualification_UNKNOWN_holds_age_and_waits_new_health(self):
        l=fixture();l.execute("local before=history();local n=T.writes();T.governor(nil);GameEvents.BuildingPillageStateChanged.Fire(0,c:GetID(),905,false);pp();assert(current(c)==5 and effects.lastError);T.governor(4);local r,w=fxReads,fxWrites;for i=1,1000 do pp()end;assert(fxReads==r and fxWrites==w);GameEvents.BuildingPillageStateChanged.Fire(0,c:GetID(),905,false);pp();assert(current(c)==5 and not effects.lastError and history()==before and T.writes()==n)")
    def test_failed_create_waits_new_evidence_no_permanent_writes(self):
        l=fixture();l.execute("local before=history();local n=T.writes();failCreate=true;loss(c);pp();assert(current(c)==0 and effects.lastError);failCreate=false;local r,w=fxReads,fxWrites;for i=1,1000 do pp()end;assert(fxReads==r and fxWrites==w);GameEvents.BuildingPillageStateChanged.Fire(0,c:GetID(),905,false);pp();assert(current(c)==5 and history()==before and T.writes()==n and not effects.lastError)")
    def test_cold_UNKNOWN_keeps_exact_membership_then_health_recovers(self):
        l=fixture(cold_unknown=True);l.execute("assert(effects.ready and effects.lastError);local before=history();T.governor(4);c.fx[905]=nil;GameEvents.BuildingPillageStateChanged.Fire(0,c:GetID(),905,false);pp();assert(current(c)==5 and history()==before)")
    def test_unknown_owner_scope_expands_enabled_Store_index_not_player_zero_guess(self):
        l=fixture();l.execute("c.fx[905]=nil;other.fx[905]=nil;local district,center=CityManager.GetDistrictAt,CityManager.GetCityAt;CityManager.GetDistrictAt=function()error('TEMPORARY_CITY_LOCATION')end;CityManager.GetCityAt=function()error('TEMPORARY_CITY_LOCATION')end;Events.BuildingRemovedFromMap.Fire(9,9,905,-1);CityManager.GetDistrictAt=district;CityManager.GetCityAt=center;pp();assert(current(c)==5 and current(other)==5)")
    def test_foreign_and_unowned_health_no_reads(self):
        l=fixture();l.execute("local r,w=fxReads,fxWrites;GameEvents.BuildingPillageStateChanged.Fire(3,999,905,true);GameEvents.BuildingPillageStateChanged.Fire(0,c:GetID(),999,true);pp();assert(fxReads==r and fxWrites==w)")
    def test_Store_tick_precedes_projection_and_health_never_adds_age(self):
        l=fixture();l.execute("for i=1,10 do T.turn(1);pp()end;assert(T.snapshot(c).researchTradition.age==10 and current(c)==10);local before=history();local n=T.writes();loss(c,910);pp();assert(current(c)==10 and history()==before and T.writes()==n);local receipt=T.snapshot(c).researchTradition.receipt;T.turn(1);pp();assert(T.snapshot(c).researchTradition.age==11 and T.snapshot(c).researchTradition.receipt==receipt and current(c)==10)")

if __name__=='__main__':unittest.main()
