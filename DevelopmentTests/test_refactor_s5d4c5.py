"""Meaning/Inspiration explicit initialization and exact health, actual eight-era SQL/GWF."""
import unittest
from unittest.mock import patch
from refactor_harness import ROOT,TrackedLua51,legacy_source_observation,Context,measure
from refactor_defect_fixtures import fact_publication_profile
from test_refactor_s5d4c4 import EXTRA
from test_refactor_a8 import reset_projection
import test_culture_aesthetic as ae
import test_culture_meaning_probe as legacy
import test_culture_inspiration_automatic as automatic

class CultureProjection(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        ae.LuaRuntime=TrackedLua51;cls.sql=legacy.database()
        reset_projection(cls.sql,'BUILDING_SPC_INSPIRATION_ERA_','SPC_INSPIRATION_ERA_')
        cls.sql.executescript((ROOT/'Mod/Data/CultureInspiration.sql').read_text())
    @classmethod
    def tearDownClass(cls):cls.sql.close()
    def fixture(self,real=False,ready=True):
        helper=automatic.InspirationAutomaticTests();helper.sql=self.sql
        with legacy_source_observation(),patch.object(ae,'FIX',ae.FIX+EXTRA):l=helper.runtime(real=real,ready=ready)
        with legacy_source_observation():fact_publication_profile(l,False)
        l.execute("""
        local create=P.CreateBuilding
        P.CreateBuilding=function(q,id)create(q,id);gp('BuildingPillageStateChanged',q.city.owner,q.city.id,id,false)end
        P.RemoveBuilding=function(b,id)
         if failRemove==id then return end
         local plot=b.city.locations[id];b.city.present[id]=nil;b.city.locations[id]=nil;writes=writes+1
         fire('BuildingRemovedFromMap',plot,0,id,b.city.owner)
        end
        function pp()shared.FactChanges.Flush();shared.FactBindings.Flush();fire('GameCoreEventPublishComplete')end
        function resetAudits()audits={};P.Observe=function(k,n)if k=='audit'then audits[n]=(audits[n]or 0)+1 end end end
        function ownID(module,c)
         local names=module=='CultureMeaning'and SPCCultureMeaningModel.Owned or SPCCultureInspirationModel.Owned
         for _,name in ipairs(names)do local id=GameInfo.Buildings[name].Index;if c.present[id]then return id end end
        end
        function loss(c,id)P.RemoveBuilding(c:GetBuildings(),id)end
        """);return l
    def test_both_exact_losses_only_target_owner_and_city_no_D_capture(self):
        for module in ('CultureMeaning','CultureInspiration'):
            l=self.fixture();l.execute("local m=shared['"+module+"'];local id=ownID('"+module+"',a);assert(id);local cap=counts.dc_capture;resetAudits();loss(a,id);pp();assert(a.present[id] and audits['"+module+"']==1 and counts.dc_capture==cap);for n in pairs(audits)do assert(n=='"+module+"',n)end;assert(finalAmount(b,'SCIENCE')==3 and inspiration(b)==6);local w,sc=writes,counts.city_scan;for i=1,1000 do pp()end;assert(writes==w and counts.city_scan==sc)")
        measure('S5d4c5_exact_health',{'owner_audits':1,'D_recaptures':0,'thousand_idle_extra_visits':0})
    def test_live_pillage_repairs_both_existing_policies(self):
        for module in ('CultureMeaning','CultureInspiration'):
            l=self.fixture();l.execute("local id=ownID('"+module+"',a);a.pillaged[id]=true;gp('BuildingPillageStateChanged',0,1,id,true);pp();assert(a.present[id] and not a.pillaged[id]);local w=writes;for i=1,1000 do pp()end;assert(writes==w)")
    def test_other_city_loss_during_each_projection_is_retained(self):
        for module in ('CultureMeaning','CultureInspiration'):
            l=self.fixture();l.execute("local id=ownID('"+module+"',a);local other=ownID('"+module+"',b);local create=P.CreateBuilding;local once=true;P.CreateBuilding=function(q,k)create(q,k);if once and q.city==a and k==id then once=false;loss(b,other)end end;loss(a,id);pp();assert(a.present[id] and not b.present[other]);pp();assert(b.present[other])")
    def test_confirmed_damage_during_create_not_hidden(self):
        for module in ('CultureMeaning','CultureInspiration'):
            l=self.fixture();l.execute("local id=ownID('"+module+"',a);local create=P.CreateBuilding;local once=true;P.CreateBuilding=function(q,k)create(q,k);if once and q.city==a and k==id then once=false;a.pillaged[id]=true;gp('BuildingPillageStateChanged',0,1,id,true)end end;loss(a,id);pp();assert(a.pillaged[id]);pp();assert(a.present[id] and not a.pillaged[id])")
    def test_UNKNOWN_and_new_health_fact_with_no_idle_retry(self):
        for module in ('CultureMeaning','CultureInspiration'):
            l=self.fixture();l.execute("local m=shared['"+module+"'];local id=ownID('"+module+"',a);a.worksUnknown=true;gp('BuildingPillageStateChanged',0,1,id,false);pp();assert(a.present[id] and m.errors['0:1']);a.worksUnknown=false;local w,sc=writes,counts.city_scan;for i=1,1000 do pp()end;assert(writes==w and counts.city_scan==sc);loss(a,id);pp();assert(a.present[id] and not m.errors['0:1'])")
    def test_new_reference_UNKNOWN_does_not_replay_saved_projection(self):
        l=self.fixture();l.execute("a.token='REPLACED';a.worksUnknown=true;meaning.Audit({player=0,city=1});ins.Audit({player=0,city=1});assert(meaningCount(a)==0 and inspiration(a)==0 and finalAmount(b,'SCIENCE')==3 and inspiration(b)==6)")
    def test_failed_create_requires_new_evidence(self):
        for module in ('CultureMeaning','CultureInspiration'):
            l=self.fixture();l.execute("local id=ownID('"+module+"',a);failCreate=true;loss(a,id);pp();assert(not a.present[id] and shared['"+module+"'].errors['0:1']);failCreate=false;local w,sc=writes,counts.city_scan;for i=1,1000 do pp()end;assert(writes==w and counts.city_scan==sc);gp('BuildingPillageStateChanged',0,1,id,false);pp();assert(a.present[id] and not shared['"+module+"'].errors['0:1'])")
    def test_ready_initialization_reentry_does_not_repeat_cleanup(self):
        for module in ('CultureMeaning','CultureInspiration'):
            l=self.fixture(ready=False);l.execute("local m=shared['"+module+"'];local names='"+module+"'=='CultureMeaning'and SPCCultureMeaningModel.Owned or SPCCultureInspirationModel.Owned;local k=GameInfo.Buildings[names[1]].Index;a.present[k]=true;a.locations[k]=a.ds[1].x;local remove=P.RemoveBuilding;local calls=0;P.RemoveBuilding=function(b,id)if m.initializing and id==k then calls=calls+1;assert(not m.Audit({player=0,city=2}))end;return remove(b,id)end;m.Audit({player=0});assert(m.ready and not m.initializing and not m.busy and calls==1);pp();assert(m.ready and calls==1);local w=writes;for i=1,1000 do pp()end;assert(writes==w)")
    def test_failed_cold_cleanup_is_city_isolated_and_new_health_recovers(self):
        for module in ('CultureMeaning','CultureInspiration'):
            l=self.fixture();l.execute("local m=shared['"+module+"'];local id=ownID('"+module+"',a);local remove=P.RemoveBuilding;P.RemoveBuilding=function(b,k)if b.city==a and k==id then return end;return remove(b,k)end;fire('LoadScreenClose');assert(m.ready and m.errors['0:1'] and not m.errors['0:2']);P.RemoveBuilding=remove;local w=writes;for i=1,1000 do pp()end;assert(writes==w);gp('BuildingPillageStateChanged',0,1,id,false);pp();assert(not m.errors['0:1'] and finalAmount(b,'SCIENCE')==3 and inspiration(b)==6)")
    def test_real_provider_both_failed_consumers_recover_on_equal_fresh_sample(self):
        l=self.fixture(real=True);l.execute("sample(1,1,1);local m=ownID('CultureMeaning',a);local i=ownID('CultureInspiration',a);failCreate=true;loss(a,m);loss(a,i);sample(2,2,1);pp();assert(shared.GreatWorkFacts.ConsumerStatus('CultureMeaning').pending==1 and shared.GreatWorkFacts.ConsumerStatus('CultureInspiration').pending==1 and meaningCount(a)==0 and inspiration(a)==0);failCreate=false;local w=writes;for n=1,1000 do pp()end;assert(writes==w);sample(3,2,1);assert(finalAmount(a,'SCIENCE')==3 and inspiration(a)==3 and shared.GreatWorkFacts.ConsumerStatus('CultureMeaning').pending==0 and shared.GreatWorkFacts.ConsumerStatus('CultureInspiration').pending==0)")
    def test_real_provider_busy_does_not_ack_or_spin(self):
        l=self.fixture(real=True);l.execute("sample(1,1,1);meaning.busy=true;ins.busy=true;sample(2,2,1);assert(shared.GreatWorkFacts.ConsumerStatus('CultureMeaning').pending==1 and shared.GreatWorkFacts.ConsumerStatus('CultureInspiration').pending==1);meaning.busy=false;ins.busy=false;pp();local w=writes;for n=1,1000 do pp()end;assert(writes==w);sample(3,2,1);assert(shared.GreatWorkFacts.ConsumerStatus('CultureMeaning').pending==0 and shared.GreatWorkFacts.ConsumerStatus('CultureInspiration').pending==0)")
    def test_missed_load_real_sample_initializes_each_independently(self):
        l=self.fixture(real=True,ready=False);l.execute("assert(not meaning.ready and not ins.ready);sample(1,1,1);assert(meaning.ready and ins.ready and not meaning.initializing and not ins.initializing and finalAmount(a,'SCIENCE')==3 and inspiration(a)==3)")
    def test_confirmed_removed_city_cleans_session_errors(self):
        l=self.fixture();l.execute("meaning.errors['0:1']='OLD';ins.errors['0:1']='OLD';table.remove(cities,1);fire('CityRemovedFromMap',0,1);pp();assert(not meaning.records['0:1'] and not ins.records['0:1'] and not meaning.errors['0:1'] and not ins.errors['0:1'] and finalAmount(b,'SCIENCE')==3 and inspiration(b)==6)")
    def test_real_building_D_updates_three_consumers_once(self):
        l=self.fixture();l.execute("resetAudits();building(a,'BUILDING_RESEARCH_LAB',a.ds[6],false);fire('BuildingRemovedFromMap',a.ds[6].x,0,GameInfo.Buildings.BUILDING_RESEARCH_LAB.Index,0);pp();assert(finalAmount(a,'SCIENCE')==1 and finalAmount(b,'SCIENCE')==3 and inspiration(a)==6 and audits.CultureMeaning==1 and audits.CultureInspiration==1 and audits.CultureAesthetic==1)")
    def test_inspiration_has_no_business_depth_dependency(self):
        l=self.fixture();l.execute("shared.DistrictCompleteness.ReadFacts=function()error('DEPTH_MUST_NOT_BE_READ_BY_INSPIRATION')end;a.eras=8;refresh();assert(inspiration(a)==24 and not ins.errors['0:1'])")
    def test_foreign_health_and_unowned_ids_create_no_work(self):
        l=self.fixture();l.execute("resetAudits();gp('BuildingPillageStateChanged',3,1,ownID('CultureMeaning',a),true);gp('BuildingPillageStateChanged',3,1,ownID('CultureInspiration',a),true);pp();assert(not next(audits))")
    def test_inspiration_no_D_startup_keeps_structural_fallback(self):
        c=Context();c.load('CultureInspiration');c.execute("P={Field=function(t,k)return t[k]end,IsTestPlayer=function(pid)return pid==0 end};shared.CultureInspirationProbe={retired=true};shared.GreatWorkFacts={RegisterConsumer=function()end};SPCCultureInspiration.Start(P,shared);assert(not shared.DistrictCompleteness and Events.DistrictPillaged.Count()==1 and Events.DistrictBuildProgressChanged.Count()==1);P.Count=function(k)counts[k]=(counts[k]or 0)+1 end;Events.DistrictBuildProgressChanged.Fire(0,77,1);assert(counts.scope_city==1 and not shared.CultureInspiration.ready)")

if __name__=='__main__':unittest.main()
