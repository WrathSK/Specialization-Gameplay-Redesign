"""Aesthetic exact health and real confirmed-work delivery recovery; local only."""
import unittest
from unittest.mock import patch
from refactor_harness import ROOT,TrackedLua51,legacy_source_observation,measure
from refactor_defect_fixtures import fact_publication_profile
import test_culture_aesthetic as ae
import test_culture_meaning_probe as legacy
import test_culture_meaning_automatic as automatic

EXTRA="""
Events.GameCoreEventPublishComplete={list={}};Events.GameCoreEventPublishComplete.Add=function(f)table.insert(Events.GameCoreEventPublishComplete.list,f)end
GameEvents.BuildingPillageStateChanged={list={}};GameEvents.BuildingPillageStateChanged.Add=function(f)table.insert(GameEvents.BuildingPillageStateChanged.list,f)end
function gp(n,...)for _,f in ipairs(GameEvents[n]and GameEvents[n].list or{})do f(...)end end
"""

class AestheticHealth(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        ae.LuaRuntime=TrackedLua51;automatic.LuaRuntime=TrackedLua51;cls.sql=legacy.database()
    @classmethod
    def tearDownClass(cls):cls.sql.close()
    def fixture(self,real=False,ready=True):
        helper=automatic.AutomaticMeaningTests() if real else ae.AestheticTests();helper.sql=self.sql
        with legacy_source_observation(),patch.object(ae,'FIX',ae.FIX+EXTRA):
            l=helper.runtime(real=True,ready=ready) if real else helper.runtime(ready=ready)
        with legacy_source_observation():fact_publication_profile(l,False)
        l.execute("""
        local create=P.CreateBuilding
        P.CreateBuilding=function(q,id)create(q,id);gp('BuildingPillageStateChanged',q.city.owner,q.city.id,id,false)end
        function pp()shared.FactChanges.Flush();shared.FactBindings.Flush();fire('GameCoreEventPublishComplete')end
        carrier=GameInfo.Buildings.BUILDING_SPC_CULTURE_AESTHETIC.Index
        function loss(c)P.RemoveBuilding(c:GetBuildings(),carrier)end
        function resetAudits()audits={};P.Observe=function(kind,name)if kind=='audit'then audits[name]=(audits[name]or 0)+1 end end end
        """);return l
    def test_external_exact_loss_one_city_D_unchanged_and_idle_zero(self):
        l=self.fixture();l.execute("local cap=counts.dc_capture;resetAudits();local expected=total(a);loss(a);assert(total(a)==0);pp();assert(total(a)==expected and total(b)==12 and audits.CultureAesthetic==1 and counts.dc_capture==cap);local w,sc=writes,counts.city_scan;for i=1,1000 do pp()end;assert(writes==w and counts.city_scan==sc)")
        measure('S5d4c4_Aesthetic_health',{'city_visits':1,'D_recaptures':0,'thousand_idle_extra_visits':0})
    def test_live_true_damage_restores_existing_configuration(self):
        l=self.fixture();l.execute("a.pillaged[carrier]=true;gp('BuildingPillageStateChanged',0,1,carrier,true);pp();assert(not a.pillaged[carrier] and total(a)==12 and not data.errors['0:1']);local w=writes;for i=1,1000 do pp()end;assert(writes==w)")
    def test_other_city_loss_inside_write_survives_next_snapshot(self):
        l=self.fixture();l.execute("local create=P.CreateBuilding;local once=true;P.CreateBuilding=function(q,id)create(q,id);if once and q.city==a and id==carrier then once=false;loss(b)end end;loss(a);pp();assert(total(a)==12 and total(b)==0);pp();assert(total(b)==12)")
    def test_damage_during_create_is_not_suppressed(self):
        l=self.fixture();l.execute("local create=P.CreateBuilding;local once=true;P.CreateBuilding=function(q,id)create(q,id);if once and q.city==a and id==carrier then once=false;a.pillaged[carrier]=true;gp('BuildingPillageStateChanged',0,1,carrier,true)end end;loss(a);pp();assert(a.pillaged[carrier]);pp();assert(not a.pillaged[carrier] and total(a)==12)")
    def test_UNKNOWN_keeps_confirmed_same_reference_new_fact_restores(self):
        l=self.fixture();l.execute("a.worksUnknown=true;gp('BuildingPillageStateChanged',0,1,carrier,false);pp();assert(total(a)==12 and data.errors['0:1']);a.worksUnknown=false;a.eras=3;local w=writes;for i=1,1000 do pp()end;assert(writes==w);gp('BuildingPillageStateChanged',0,1,carrier,false);pp();assert(total(a)==18 and not data.errors['0:1'])")
    def test_create_failure_dormant_then_new_external_evidence(self):
        l=self.fixture();l.execute("failCreate=true;loss(a);pp();assert(total(a)==0 and data.errors['0:1']);failCreate=false;local w=writes;for i=1,1000 do pp()end;assert(writes==w);gp('BuildingPillageStateChanged',0,1,carrier,false);pp();assert(total(a)==12 and not data.errors['0:1'])")
    def test_foreign_or_other_internal_carrier_zero_work(self):
        l=self.fixture();l.execute("resetAudits();gp('BuildingPillageStateChanged',3,1,carrier,true);gp('BuildingPillageStateChanged',0,1,GameInfo.Buildings.BUILDING_SPC_DEV_LV2_HOUSING_0.Index,true);pp();assert(not next(audits))")
    def test_real_ordinary_D_once_keeps_sibling_and_second_same_turn(self):
        l=self.fixture();l.execute("resetAudits();building(a,'BUILDING_MARKET',a.ds[3],false);fire('BuildingRemovedFromMap',a.ds[3].x,0,GameInfo.Buildings.BUILDING_MARKET.Index,0);pp();assert(total(a)==10 and total(b)==12 and audits.CultureAesthetic==1);building(a,'BUILDING_MARKET',a.ds[3]);gp('BuildingPillageStateChanged',0,1,GameInfo.Buildings.BUILDING_MARKET.Index,false);pp();assert(total(a)==12 and audits.CultureAesthetic==2 and turn==10)")
    def test_real_provider_failed_projection_keeps_pending_until_equal_fresh_sample(self):
        l=self.fixture(real=True);l.execute("sample(1,1,1);assert(shared.GreatWorkFacts.ConsumerStatus('CultureAesthetic').pending==0);failCreate=true;loss(a);sample(2,2,1);assert(total(a)==0 and data.errors['0:1'] and shared.GreatWorkFacts.ConsumerStatus('CultureAesthetic').pending==1);pp();failCreate=false;local w=writes;for i=1,1000 do pp()end;assert(writes==w and total(a)==0);sample(3,2,1);assert(total(a)>0 and not data.errors['0:1'] and shared.GreatWorkFacts.ConsumerStatus('CultureAesthetic').pending==0)")
    def test_real_provider_busy_delivery_unacknowledged_no_idle_spin(self):
        l=self.fixture(real=True);l.execute("sample(1,1,1);data.busy=true;sample(2,2,1);assert(shared.GreatWorkFacts.ConsumerStatus('CultureAesthetic').pending==1);data.busy=false;pp();assert(total(a)>0);local w=writes;for i=1,1000 do pp()end;assert(writes==w and shared.GreatWorkFacts.ConsumerStatus('CultureAesthetic').pending==1);sample(3,2,1);assert(shared.GreatWorkFacts.ConsumerStatus('CultureAesthetic').pending==0)")
    def test_confirmed_city_removal_cleans_absent_session_records(self):
        l=self.fixture();l.execute("data.errors['0:1']='OLD_ERROR';local expected=total(b);table.remove(cities,1);fire('CityRemovedFromMap',0,1);pp();assert(not data.records['0:1'] and not data.errors['0:1'] and data.records['0:2'] and total(b)==expected)")
    def test_missed_load_confirmed_current_sample_keeps_readiness_boundary(self):
        l=self.fixture(real=True,ready=False);l.execute("assert(not data.ready);sample(1,1,1);assert(data.ready and total(a)>0 and total(b)>0 and shared.GreatWorkFacts.ConsumerStatus('CultureAesthetic').pending==0)")

if __name__=='__main__':unittest.main()
