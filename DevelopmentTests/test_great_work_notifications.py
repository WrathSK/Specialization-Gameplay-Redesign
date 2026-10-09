"""B173: real GreatWorkFacts named delivery, three actual Culture consumers.
LOCAL only. No native engine proof, persistent writes, global scan rewrite or GC.
Use the maintained read-only external DB/Lupa setup for integration cases.
"""
from pathlib import Path
import unittest
import xml.etree.ElementTree as ET
from test_p0_k import Fixture, PRODUCER
import test_p0_k as k
import test_culture_inspiration_automatic as inspiration
import test_culture_meaning_automatic as meaning
import test_culture_aesthetic as aesthetic
import test_culture_meaning_probe as legacy
R=Path(__file__).resolve().parents[1]

class NotificationTests(unittest.TestCase):
 def test_each_position_failure_isolated_and_identical_new_sample_retries_only_failure(self):
  for failing in ['A','B','C']:
   with self.subTest(failing=failing):
    fx=Fixture();fx.lua.globals().failing=failing
    fx.check(r"""
     calls={A=0,B=0,C=0};fail=true
     for _,name in ipairs({'A','B','C'})do
      local n=name;shared.GreatWorkFacts.RegisterConsumer(n,function(pid,ids)
       calls[n]=calls[n]+1;assert(pid==0 and #ids==3)
       if n==failing and fail then error('NOTIFY_FAILED')end
      end)
     end
     assert(receive(1,sampleRows()));assert(shared.GreatWorkFacts.ack==1)
     assert(calls.A==1 and calls.B==1 and calls.C==1)
     local s=shared.GreatWorkFacts.ConsumerStatus(failing);assert(s.pending==3 and s.error)
     assert(not receive(1,sampleRows()));assert(calls[failing]==1)
     fail=false;assert(receive(2,sampleRows()));assert(calls[failing]==2)
     for n,v in pairs(calls)do if n~=failing then assert(v==1)end end
     assert(not shared.GreatWorkFacts.consumerError)
     assert(receive(3,sampleRows()));assert(calls[failing]==2)
     assert(propertyWrites==0 and carrierWrites==0)
    """)
 def test_latest_facts_not_failed_snapshot_and_other_city_isolated(self):
  fx=Fixture();fx.check(r"""
   local f=shared.GreatWorkFacts;calls={};fail=false
   f.RegisterConsumer('A',function(pid,ids)
    calls[#calls+1]={ids=ids,eras=f.Summary(pid,7).eraCount}
    if fail then error('ONCE')end
   end)
   receive(1,{{7,10,0,100,'GREATWORK_BHASA_1'}})
   fail=true;receive(2,{{7,10,0,100,'GREATWORK_BHASA_1'},{7,10,1,102,'GREATWORK_YING_1'}})
   assert(#calls[2].ids==1 and calls[2].ids[1]==7 and calls[2].eras==2)
   fail=false;receive(3,{{7,10,0,100,'GREATWORK_BHASA_1'}})
   assert(#calls[3].ids==1 and calls[3].ids[1]==7 and calls[3].eras==1)
   assert(f.ConsumerStatus('A').pending==0)
  """)
 def test_invalid_duplicate_foreign_and_stale_packets_do_not_retry(self):
  fx=Fixture();fx.check(r"""
   local f=shared.GreatWorkFacts;calls=0
   f.RegisterConsumer('A',function()calls=calls+1;error('FAIL')end)
   assert(receive(1,sampleRows()));local p=packet(2,sampleRows());p.FactsEpoch=p.FactsEpoch+1
   assert(not f.Receive(0,p));p=packet(2,sampleRows());assert(not f.Receive(3,p))
   assert(not receive(1,sampleRows()));p=packet(2,sampleRows());p.FactsInput=-1;assert(not f.Receive(0,p))
   assert(calls==1 and f.ConsumerStatus('A').pending==3)
   assert(receive(3,sampleRows()));assert(calls==2)
  """)
 def test_callback_arguments_and_diagnostic_status_are_isolated(self):
  fx=Fixture();fx.check(r"""
   local f=shared.GreatWorkFacts;seen=0
   f.RegisterConsumer('A',function(pid,ids)ids[1]=999;table.remove(ids);error(string.rep('x',1000))end)
   f.RegisterConsumer('B',function(pid,ids)assert(#ids==3 and ids[1]==7);seen=seen+1 end)
   assert(receive(1,sampleRows()));local s=f.ConsumerStatus('A');assert(#s.error==180)
   s.pending=0;s.error=nil;assert(f.ConsumerStatus('A').pending==3 and f.ConsumerStatus('A').error)
   assert(seen==1 and f.Describe(0,7):find('馆藏通知待重试'))
   assert(not f.ConsumerStatus('not_registered'))
   assert(not pcall(f.RegisterConsumer,'A',function()end))
  """)
 def test_repeated_failure_remains_bounded_and_error_not_erased_by_sibling(self):
  fx=Fixture();fx.check(r"""
   local f=shared.GreatWorkFacts;calls=0;other=0
   f.RegisterConsumer('A',function()calls=calls+1;error('FAIL')end)
   f.RegisterConsumer('B',function()other=other+1 end)
   for seq=1,12 do assert(receive(seq,sampleRows()));assert(f.ConsumerStatus('A').pending==3 and f.consumerError)end
   assert(calls==12 and other==1 and f.ConsumerStatus('B').pending==0)
   local p=packet(13,{});assert(f.Receive(0,p));assert(f.ConsumerStatus('A').pending==3)
   assert(propertyWrites==0 and carrierWrites==0)
  """)
 def test_unknown_sample_preserves_unknown_and_defers_business_decision(self):
  fx=Fixture();fx.check(r"""
   local f=shared.GreatWorkFacts;states={}
   f.RegisterConsumer('A',function(pid,ids)states[#states+1]=f.Summary(pid,7).availability end)
   receive(1,{{7,10,0,100,'GREATWORK_BHASA_1'}})
   receive(2,{}, {[7]=false});assert(states[2]=='UNKNOWN' and f.Summary(0,7).eraCount==1)
   receive(3,{{7,10,0,100,'GREATWORK_BHASA_1'}});assert(states[3]=='KNOWN')
  """)
 def test_reset_shutdown_and_replacement_session_do_not_replay_pending(self):
  fx=Fixture();fx.check(r"""
   local old=shared.GreatWorkFacts;calls=0
   old.RegisterConsumer('A',function()calls=calls+1;error('FAIL')end);receive(1,sampleRows())
   old.Reset();assert(old.ConsumerStatus('A').pending==0 and not old.consumerError)
   exits={};returns={};SPCGreatWorkFacts.Start(P,shared)
   assert(not old.ConsumerStatus('A'));assert(not old.Receive(0,packet(2,sampleRows())))
   assert(not pcall(old.RegisterConsumer,'B',function()end))
   shared.GreatWorkFacts.RegisterConsumer('Fresh',function()end);receive(1,sampleRows());assert(calls==1)
  """)
 def test_confirmed_loss_prunes_failed_reference_and_does_not_touch_permanent_state(self):
  fx=Fixture();fx.check(r"""
   local f=shared.GreatWorkFacts;fail=false;calls=0
   f.RegisterConsumer('A',function()calls=calls+1;if fail then error('FAIL')end end)
   receive(1,{});fail=true;receive(2,{{7,10,0,100,'GREATWORK_BHASA_1'}})
   assert(f.ConsumerStatus('A').pending==1)
   assert(not pcall(exits.GreatWorkFacts,a,{confirmed=false,targetID=7,origin={owner=0}}))
   assert(f.ConsumerStatus('A').pending==1)
   local before=encode(permanentStore);exits.GreatWorkFacts(a,{confirmed=true,targetID=7,origin={owner=0}})
   assert(f.ConsumerStatus('A').pending==0 and encode(permanentStore)==before and propertyWrites==0)
  """)
 def test_reference_change_never_reuses_failed_city_reference(self):
  fx=Fixture();fx.check(r"""
   local f=shared.GreatWorkFacts;refs={};fail=true
   f.RegisterConsumer('A',function(pid,ids)refs[#refs+1]=f.Summary(pid,7).reference;if fail then error('FAIL')end end)
   receive(1,sampleRows());local old=refs[1];a.properties.SPC_DEV_BINDING_B013_TOKEN='replacement'
   fail=false;receive(2,sampleRows());assert(refs[2]~=old and refs[2]==SPCNetworkInput.Reference(a))
   assert(f.ConsumerStatus('A').pending==0)
  """)
 def test_owner_changes_during_delivery_skip_stale_target_for_next_consumer(self):
  fx=Fixture();fx.check(r"""
   local f=shared.GreatWorkFacts;seen={}
   f.RegisterConsumer('First',function()a.owner=3 end)
   f.RegisterConsumer('Second',function(pid,ids)seen=ids end)
   receive(1,sampleRows());assert(#seen==2 and seen[1]==8 and seen[2]==9)
   assert(f.ConsumerStatus('Second').pending==0)
  """)
 def test_temporary_owner_read_failure_keeps_only_unconfirmed_target_pending(self):
  fx=Fixture();fx.check(r"""
   local f=shared.GreatWorkFacts;seen={}
   f.RegisterConsumer('First',function()a.failOwner=true end)
   f.RegisterConsumer('Second',function(pid,ids)seen[#seen+1]=ids end)
   receive(1,sampleRows());assert(#seen[1]==2 and f.ConsumerStatus('Second').pending==1)
   a.failOwner=false;receive(2,sampleRows());assert(#seen==2 and #seen[2]==1 and seen[2][1]==7)
   assert(not f.ConsumerStatus('Second').error)
  """)
 def test_reentrant_new_sample_catches_up_without_recursive_delivery(self):
  fx=Fixture();fx.check(r"""
   local f=shared.GreatWorkFacts;callsA=0;callsB=0;depth=0;maxDepth=0
   f.RegisterConsumer('A',function(pid,ids)
    depth=depth+1;maxDepth=math.max(depth,maxDepth);callsA=callsA+1
    if callsA==1 then assert(receive(2,{{7,10,0,100,'GREATWORK_BHASA_1'}}))end
    depth=depth-1
   end)
   f.RegisterConsumer('B',function(pid,ids)callsB=callsB+1;assert(f.Summary(pid,7).count==1)end)
   assert(receive(1,{}));assert(callsA==2 and callsB==1 and maxDepth==1)
   assert(f.ConsumerStatus('A').pending==0 and f.ConsumerStatus('B').pending==0 and f.ack==2)
  """)
 def test_reentrant_burst_stops_after_one_catchup_and_retains_latest(self):
  fx=Fixture();fx.check(r"""
   local f=shared.GreatWorkFacts;calls=0;loop=true;nextSeq=1
   f.RegisterConsumer('A',function()
    calls=calls+1
    if loop then nextSeq=nextSeq+1;receive(nextSeq,nextSeq%2==0 and {{7,10,0,100,'GREATWORK_BHASA_1'}} or {})end
   end)
   assert(receive(1,{}));assert(calls==2 and f.ConsumerStatus('A').pending==1)
   loop=false;nextSeq=nextSeq+1;assert(receive(nextSeq,{}));assert(calls==3 and f.ConsumerStatus('A').pending==0)
  """)
 def test_reset_inside_callback_cancels_old_epoch_delivery(self):
  fx=Fixture();fx.check(r"""
   local f=shared.GreatWorkFacts;second=0
   f.RegisterConsumer('First',function()f.Reset()end)
   f.RegisterConsumer('Second',function()second=second+1 end)
   receive(1,sampleRows());assert(second==0 and f.ConsumerStatus('Second').pending==0)
  """)
 def test_ui_ack_does_not_retry_consumers_on_idle_pulse(self):
  fx=Fixture();fx.check(PRODUCER);fx.check(r"""
   calls=0;fail=true
   shared.GreatWorkFacts.RegisterConsumer('A',function()calls=calls+1;if fail then error('FAIL')end end)
  """)
  fx.lua.execute((R/'Mod/UI/DialogueRefresh.lua').read_text())
  fx.check(r"""
   init();local ui=ExposedMembers.SPC_DialogueBackground;local scans=ui.scans;local sends=ui.sends
   assert(calls==1 and ui.state=='IDLE' and shared.GreatWorkFacts.consumerError)
   for i=1,12 do fire('SystemUpdateUI')end
   assert(calls==1 and ui.scans==scans and ui.sends==sends and ui.retries==0)
   fail=false;turn=turn+1;fire('PlayerTurnActivated',0);fire('SystemUpdateUI')
   assert(calls==2 and not shared.GreatWorkFacts.consumerError)
  """)

class CultureIntegrationTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  inspiration.InspirationAutomaticTests.setUpClass();cls.sql=inspiration.InspirationAutomaticTests.sql
 @classmethod
 def tearDownClass(cls):cls.sql.close()
 def runtime(self):
  h=inspiration.InspirationAutomaticTests();h.sql=self.sql;return h.runtime(real=True)
 def test_each_real_consumer_failure_does_not_suppress_siblings_then_recovers(self):
  for name in ['CultureAesthetic','CultureMeaning','CultureInspiration']:
   with self.subTest(consumer=name):
    l=self.runtime();l.globals().name=name;l.execute(r"""
     sample(1,1,1);local original=shared[name].Audit
     shared[name].Audit=function()error('INJECTED_NOTIFICATION_FAILURE')end
     sample(2,0,1)
     if name~='CultureAesthetic'then assert(total(a)==0)end
     if name~='CultureMeaning'then assert(meaningCount(a)==0)end
     if name~='CultureInspiration'then assert(inspiration(a)==0)end
     assert(shared.GreatWorkFacts.ConsumerStatus(name).pending==1)
     assert(inspiration(b)==3 and meaningCount(b)>0 and total(b)>0)
     shared[name].Audit=original;sample(3,0,1)
     assert(total(a)==0 and meaningCount(a)==0 and inspiration(a)==0)
     assert(not shared.GreatWorkFacts.consumerError)
    """)
 def test_three_real_consumers_move_new_era_duplicate_and_unknown(self):
  l=self.runtime();l.execute(r"""
   sample(1,1,1);local before=writes;sample(2,1,1);assert(writes==before)
   local p=packet(3,2,0);local n=0;p.FactsData=p.FactsData:gsub('GREATWORK_BHASA_1',function()n=n+1;return n==2 and 'GREATWORK_CHAUCER_1' or 'GREATWORK_BHASA_1'end)
   meaningRequest(0,p)
   assert(inspiration(a)==6 and meaning.records['0:1'].count==2 and total(a)>0)
   assert(inspiration(b)==0 and meaningCount(b)==0 and total(b)==0)
   local value=total(a);p=packet(4,0,0);p.Valid=0;p.FactsRefs=p.FactsRefs:gsub(',1;',',0;');meaningRequest(0,p)
   assert(inspiration(a)==6 and total(a)==value and meaning.records['0:1'].count==2)
   assert(ins.errors['0:1'] and meaning.errors['0:1'] and data.errors['0:1'])
   sample(5,0,1);assert(inspiration(a)==0 and meaningCount(a)==0 and total(a)==0)
  """)
 def test_initial_failure_is_not_retried_by_gameplay_fallback_same_packet(self):
  h=inspiration.InspirationAutomaticTests();h.sql=self.sql;l=h.runtime(real=True,ready=False)
  l.execute(r"""
   local audit=meaning.Audit;calls=0
   meaning.Audit=function()calls=calls+1;error('READY_CALLBACK_FAIL')end
   assert(pcall(sample,1,1,1));assert(calls==1 and inspiration(a)==3 and total(a)>0)
   assert(dialogue.seq[0]==1 and shared.GreatWorkFacts.ConsumerStatus('CultureMeaning').pending==2)
   meaning.Audit=audit;sample(2,1,1);assert(meaning.ready and finalAmount(a,'SCIENCE')==3)
   assert(not shared.GreatWorkFacts.ConsumerStatus('CultureMeaning').error)
  """)
 def test_unexpected_readiness_failure_cannot_abort_other_ready_or_pair(self):
  l=self.runtime();l.execute(r"""
   sample(1,1,1);local calls=0
   meaning.CollectionConfirmed=function()error('READY_FAIL')end
   ins.CollectionConfirmed=function()calls=calls+1 end
   assert(pcall(sample,2,1,1));assert(calls==1 and dialogue.seq[0]==2)
   assert(meaning.error=='GW_CONSUMER_READY_FAILED' and inspiration(a)==3)
  """)
 def test_callback_completion_does_not_claim_business_or_native_success(self):
  l=self.runtime();l.execute(r"""
   sample(1,1,1);failRemove=GameInfo.Buildings.BUILDING_SPC_INSPIRATION_ERA_1.Index
   sample(2,0,1)
   assert(ins.errors['0:1'] and inspiration(a)==3)
   assert(shared.GreatWorkFacts.ConsumerStatus('CultureInspiration').pending==0)
   assert(not shared.GreatWorkFacts.consumerError) -- dispatch returned; business failure remains owned/visible
   failRemove=nil;refresh();assert(inspiration(a)==0 and not ins.errors['0:1'])
  """)
 def test_current_package_api_and_no_new_persistence_or_ui_collector(self):
  from lupa.lua55 import LuaRuntime
  lua=LuaRuntime();xml=ET.parse(R/'Mod/SpecializationP0.modinfo').getroot()
  self.assertEqual(xml.get('version'),'200')
  for name in ['GreatWorkFacts','CultureAesthetic','CultureMeaning','CultureInspiration','Probe']:
   text=(R/'Mod'/f'{name}.lua').read_text();lua.execute('assert(load(...))',text)
   self.assertNotIn('.OnConfirmed',text)
  for name in ['CultureAesthetic','CultureMeaning','CultureInspiration']:
   self.assertIn(f"RegisterConsumer('{name}'",(R/'Mod'/f'{name}.lua').read_text())
  facts=(R/'Mod/GreatWorkFacts.lua').read_text();self.assertNotIn('SetProperty(',facts)
  files=[e.text for e in xml.find('Files')];self.assertEqual(len(files),len(set(files)))


def load_tests(loader,tests,pattern):
 # Current exact implementation assertions; B172's pinned version199 assertion is
 # preserved in its original runner. Current version200/API is checked above.
 for name in loader.getTestCaseNames(inspiration.InspirationAutomaticTests):
  if name!='test_package_ui_and_localization_complete':tests.addTest(inspiration.InspirationAutomaticTests(name))
 # Existing current-context/transport and scoped lifecycle coverage; no old broad wrappers.
 tests.addTests(loader.loadTestsFromModule(k))
 for name in ['test_real_facts_callback_move_both_endpoints_and_duplicate_ack',
  'test_active_downgrade_and_same_turn_governor_restoration','test_cold_unknown_and_missed_load_ready_on_real_sample',
  'test_confirmed_loss_exit_unknown_no_clear_and_recapture_current_gate','test_actual_positive_dialogue_has_no_meaning_override']:
  tests.addTest(meaning.AutomaticMeaningTests(name))
 class AestheticFixture(aesthetic.AestheticTests):
  @classmethod
  def setUpClass(cls):cls.sql=legacy.database()
  @classmethod
  def tearDownClass(cls):cls.sql.close()
 for name in ['test_formula_and_two_cities','test_current_buildings_and_d_separation',
  'test_unknown_reference_load_and_gate','test_confirmed_loss_recapture_only_current',
  'test_missed_load_confirmed_sample_starts_without_panel','test_unknown_or_stale_notification_does_not_open_ready']:
  tests.addTest(AestheticFixture(name))
 return tests

if __name__=='__main__':unittest.main(verbosity=2)
