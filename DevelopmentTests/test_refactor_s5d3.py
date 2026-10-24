"""Independent actual Dialogue effects, native queue and real work transport. Local only."""
import unittest
from unittest.mock import patch
from refactor_harness import ROOT,TrackedLua51,legacy_source_observation,measure
from refactor_defect_fixtures import startup,greatworks
from test_refactor_a8 import reset_projection


class Dialogue(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        import test_culture_aesthetic as ae
        import test_culture_meaning_probe as legacy
        ae.LuaRuntime=TrackedLua51;cls.sql=legacy.database()
        reset_projection(cls.sql,'BUILDING_SPC_DIALOGUE_TOTAL_','SPC_DIALOGUE_TOTAL_');cls.sql.execute('DROP TABLE IF EXISTS SPC_DialogueTotals')
        cls.sql.executescript((ROOT/'Mod/Data/DialogueEffects.sql').read_text())
    @classmethod
    def tearDownClass(cls):cls.sql.close()
    def fixture(self,real=False,boot=True):
        from test_dialogue_effects import Effects
        import test_culture_aesthetic as ae
        helper=Effects();helper.sql=self.sql
        extra="\nEvents.GameCoreEventPublishComplete={list={}};Events.GameCoreEventPublishComplete.Add=function(f)table.insert(Events.GameCoreEventPublishComplete.list,f)end;GameEvents.BuildingPillageStateChanged={list={}};GameEvents.BuildingPillageStateChanged.Add=function(f)table.insert(GameEvents.BuildingPillageStateChanged.list,f)end"
        with legacy_source_observation(),patch.object(ae,'FIX',ae.FIX+extra):l=helper.runtime(real=real,boot=boot)
        l.execute("legacyCalls=0;dialogue.Audit=function()legacyCalls=legacyCalls+1;error('RETIRED_RELAY_FORBIDDEN')end;function publish()fire('GameCoreEventPublishComplete')end;function pillage(pid,cid,id,state)for _,f in ipairs(GameEvents.BuildingPillageStateChanged.list)do f(pid,cid,id,state)end end")
        return l
    def test_governor_independent_read_at_publish_without_ui_or_legacy_relay(self):
        l=self.fixture();l.execute("assert(total(a)==5 and total(b)==10);a.active=1;fire('GovernorAssigned',0,1,0);assert(total(a)==5);publish();assert(total(a)==0 and total(b)==10 and legacyCalls==0);a.active=3;fire('GovernorEstablished',0,1,0);publish();assert(total(a)==5 and a.history.total==5 and legacyCalls==0)")
    def test_local_governor_in_foreign_receiving_city_still_refreshes_old_owner(self):
        l=self.fixture();l.execute("a.active=1;fire('GovernorAssigned',1,999,0);publish();assert(total(a)==0 and total(b)==10 and legacyCalls==0)")
    def test_real_transport_ack_empty_and_recovery_do_not_need_retired_effect_forward(self):
        l=self.fixture(True);l.execute("sample(1,1,1);assert(total(a)==5 and shared.GreatWorkFacts.ack==1 and dialogue.seq[0]==1);sample(2,0,1);assert(total(a)==0 and total(b)==10);sample(3,1,1);assert(total(a)==5 and legacyCalls==0 and shared.GreatWorkFacts.ack==3 and dialogue.seq[0]==3);local n=writes;sample(3,1,1);assert(writes==n and a.history.total==5)")
    def test_real_fact_unknown_to_known_recovery_does_not_reconstruct_history(self):
        l=self.fixture(True);l.execute("sample(1,1,1);assert(total(a)==5);shared.GreatWorkFacts.Reset();one();assert(total(a)==5 and effects.errors['0:1']);sample(2,1,1);assert(total(a)==5 and not effects.errors['0:1'] and a.history.total==5 and legacyCalls==0)")
    def test_external_owned_removal_recovers_but_ordinary_building_does_no_effect_read(self):
        l=self.fixture();l.execute("local read=shared.CityProgressionStore.DialogueState;calls=0;shared.CityProgressionStore.DialogueState=function(...)calls=calls+1;return read(...)end;fire('BuildingRemovedFromMap',a.ds[1].x,0,GameInfo.Buildings.BUILDING_MONUMENT.Index,0);publish();assert(calls==0);local id=GameInfo.Buildings.BUILDING_SPC_DIALOGUE_TOTAL_5.Index;a.present[id]=nil;fire('BuildingRemovedFromMap',a.ds[1].x,0,id,0);assert(total(a)==0);publish();assert(total(a)==5 and calls==1 and a.history.total==5)")
    def test_live_gameplay_pillage_health_does_not_depend_on_dead_events(self):
        l=self.fixture();l.execute("Events.CityBuildingsChanged=nil;Events.BuildingPillaged=nil;Events.BuildingRepaired=nil;local id=GameInfo.Buildings.BUILDING_SPC_DIALOGUE_TOTAL_5.Index;a.pillaged[id]=true;local info=P.Info;P.Info=function()error('HEALTH_METADATA_ALREADY_VALIDATED')end;pillage(0,1,id,true);P.Info=info;publish();assert(total(a)==5 and not a.pillaged[id])")
    def test_self_projection_writes_cannot_arm_idle_retries(self):
        l=self.fixture();l.execute("local read=shared.CityProgressionStore.DialogueState;calls=0;shared.CityProgressionStore.DialogueState=function(...)calls=calls+1;return read(...)end;history(a,{2});one();assert(total(a)==10);local n=calls;for i=1,1000 do publish()end;assert(calls==n and not effects.busy and legacyCalls==0)")
    def test_other_city_external_loss_during_write_is_not_suppressed(self):
        l=self.fixture();l.execute("local remove=P.RemoveBuilding;local once=true;local id=GameInfo.Buildings.BUILDING_SPC_DIALOGUE_TOTAL_10.Index;P.RemoveBuilding=function(...)if once then once=false;b.present[id]=nil;fire('BuildingRemovedFromMap',b.ds[1].x,0,id,0)end;return remove(...)end;history(a,{2});one();assert(total(b)==0);publish();assert(total(a)==10 and total(b)==10)")
    def test_failure_waits_for_new_health_evidence_not_idle(self):
        l=self.fixture();l.execute("failCreate=true;history(a,{2});one();assert(total(a)==0 and effects.errors['0:1']);local n=writes;for i=1,1000 do publish()end;assert(writes==n);failCreate=false;pillage(0,1,GameInfo.Buildings.BUILDING_SPC_DIALOGUE_TOTAL_10.Index,false);publish();assert(total(a)==10 and a.history.total==10 and not effects.errors['0:1'])")
    def test_confirmed_store_exit_and_return_keep_history_and_recompute(self):
        l=self.fixture();l.execute("a.owner=3;exits.DialogueEffects(a,{confirmed=true,targetID=1,origin={owner=0}});assert(total(a)==0 and a.history.total==5);a.owner=0;returns.DialogueEffects(0,a);assert(total(a)==5 and a.history.total==5)")
    def test_same_boundary_governor_repetition_coalesces_without_idle_work(self):
        l=self.fixture();l.execute("local read=shared.CityProgressionStore.DialogueState;calls=0;shared.CityProgressionStore.DialogueState=function(...)calls=calls+1;return read(...)end;for i=1,44 do fire('GovernorChanged')end;assert(calls==0);publish();assert(calls==2);for i=1,1000 do publish()end;assert(calls==2 and legacyCalls==0)")
        measure('S5d3_dialogue_native_queue',{'notifications':44,'effect_audits':1,'city_history_reads':2,'thousand_idle_extra_reads':0})
    def test_equal_reliable_new_work_sample_retries_failed_effect_delivery(self):
        l=self.fixture(True);l.execute("failCreate=true;sample(1,1,1);assert(total(a)==0 and shared.GreatWorkFacts.ConsumerStatus('DialogueEffects').pending>0);local n=writes;for i=1,1000 do publish()end;assert(writes==n);failCreate=false;sample(2,1,1);assert(total(a)==5 and total(b)==10 and shared.GreatWorkFacts.ConsumerStatus('DialogueEffects').pending==0 and legacyCalls==0 and a.history.total==5)")
    def test_unresolved_other_city_loss_during_write_retains_owner_cause(self):
        l=self.fixture();l.execute("local remove=P.RemoveBuilding;local once=true;local id=GameInfo.Buildings.BUILDING_SPC_DIALOGUE_TOTAL_10.Index;local district=CityManager.GetDistrictAt;local center=CityManager.GetCityAt;CityManager.GetDistrictAt=function(x,y)if x==b.ds[1].x then error('TEMPORARILY_UNREADABLE_B')end;return district(x,y)end;CityManager.GetCityAt=function(x,y)if x==b.ds[1].x then return nil end;return center(x,y)end;P.RemoveBuilding=function(...)if once then once=false;b.present[id]=nil;fire('BuildingRemovedFromMap',b.ds[1].x,0,id,0)end;return remove(...)end;history(a,{2});one();assert(total(b)==0);publish();assert(total(a)==10 and total(b)==10)")
    def test_confirmed_damage_during_same_city_write_is_not_suppressed(self):
        l=self.fixture();l.execute("local create=P.CreateBuilding;local once=true;local id=GameInfo.Buildings.BUILDING_SPC_DIALOGUE_TOTAL_10.Index;P.CreateBuilding=function(q,bid)create(q,bid);if once and q.city==a and bid==id then once=false;a.pillaged[id]=true;pillage(0,1,id,true)end end;history(a,{2});one();assert(a.pillaged[id]);publish();assert(total(a)==10 and not a.pillaged[id])")
    def test_retired_transfer_still_invalidates_pair_and_preserves_sequence(self):
        l=self.fixture(True);l.execute("sample(1,1,1);assert(dialogue.samples[0] and dialogue.paired[0]);local generation=dialogue.generation;fire('CityTransfered',1,999,0);assert(next(dialogue.samples)==nil and next(dialogue.paired)==nil and dialogue.seq[0]==1 and dialogue.generation==generation);assert(dialogue.IsOwnedCarrier('BUILDING_SPC_DIALOGUE_TOTAL_10'))")
    def test_initialization_reentry_queues_actual_cause_without_restarting_cleanup(self):
        l=self.fixture(boot=False);l.execute("local original=dialogue.Init;calls=0;local once=true;dialogue.Init=function()calls=calls+1;if once then once=false;assert(not effects.Audit({player=0,city=2}))end;return original()end;boot();assert(calls==1 and effects.ready and not effects.initializing and not effects.startupError);publish();assert(calls==1 and total(a)==5 and total(b)==10)")
    def test_work_consumer_start_failure_dependency_does_not_fake_effect_ready(self):
        c=startup();c.execute("SPCGreatWorkFacts.Start=function()error('WORK_FACTS_FAILED')end");c.load('Gameplay');c.execute("local s=ExposedMembers.SPC_P0;assert(s.StartStatus.GreatWorkFacts.state=='FAILED' and s.StartStatus.DialogueEffects.state=='SKIPPED_DEPENDENCY' and s.StartStatus.Dialogue.state=='SKIPPED_DEPENDENCY' and s.Dialogue==nil and s.DialogueEffects==nil)")

class Background(unittest.TestCase):
    def fixture(self):
        c=greatworks();c.execute("local s=ExposedMembers.SPC_P0;s.Dialogue.seq[0]=packet.Seq;s.GreatWorkFacts.ack=packet.Seq;publish();p=ExposedMembers.SPC_DialogueBackground;scans=p.scans;slots=p.slotReads;sends=p.sends")
        return c
    def test_known_foreign_city_district_transfer_governor_has_zero_scan_slots_send(self):
        c=self.fixture();c.execute("Events.CityAddedToMap.Fire(1,7);Events.CityRemovedFromMap.Fire(1,7);Events.DistrictBuildProgressChanged.Fire(1,8,7);Events.DistrictRemovedFromMap.Fire(1,8,7);Events.CityTransfered.Fire(1,7,2);Events.GovernorAssigned.Fire(1,7,2);Events.GovernorChanged.Fire(1);for i=1,1000 do publish()end;assert(p.scans==scans and p.slotReads==slots and p.sends==sends)")
    def test_local_city_recollects_only_known_city_and_unknown_coalesces(self):
        c=self.fixture();c.execute("Events.DistrictBuildProgressChanged.Fire(0,9,1);publish();assert(p.scans==scans+1 and p.slotReads==slots+1);local n=p.scans;Events.CityAddedToMap.Fire();Events.DistrictRemovedFromMap.Fire();publish();assert(p.scans==n+1);n=p.scans;for i=1,1000 do publish()end;assert(p.scans==n)")
    def test_cross_owner_governor_and_parameterless_deal_keep_local_recovery(self):
        c=self.fixture();c.execute("Events.GovernorAssigned.Fire(1,7,0);publish();assert(p.scans==scans+1 and p.slotReads==slots);Events.DiplomacyDealEnacted.Fire();publish();assert(p.scans==scans+2 and p.slotReads==slots+2)")

if __name__=='__main__':unittest.main()
