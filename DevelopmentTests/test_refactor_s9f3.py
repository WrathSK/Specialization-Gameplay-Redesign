"""Actual Store capture of approved bounded skipped-lifecycle evidence."""
import unittest
from contextlib import contextmanager,nullcontext
from hashlib import sha256
from pathlib import Path
from unittest.mock import patch
import subprocess
from refactor_harness import ROOT,TrackedLua51,SOURCES,measure
from test_refactor_s8b2 import fixture

@contextmanager
def before():
 p=ROOT/'Mod/CityProgressionStore.lua';text=subprocess.check_output(['git','show','71dd0ad:Mod/CityProgressionStore.lua'],cwd=ROOT,text=True)
 read,execute=Path.read_text,TrackedLua51.execute;h=sha256(text.encode()).hexdigest()
 def run(vm,s,*a,**kw):
  if sha256(s.encode()if isinstance(s,str)else s).hexdigest()==h:SOURCES[h]='historical/71dd0ad/Mod/CityProgressionStore.lua'
  return execute(vm,s,*a,**kw)
 with patch.object(Path,'read_text',lambda path,*a,**kw:text if path==p else read(path,*a,**kw)),patch.object(TrackedLua51,'execute',run):yield

SETUP="""
function unavailable(keys)
 local selected={};for key in string.gmatch(keys,'[^,]+')do selected[key]=true end
 local token=T.record(ca).base.token
 local validate,check=SPCStoreSubrecords.Validate,SPCStoreSubrecords.CheckOne
 SPCStoreSubrecords.Validate=function(r,...)
  if r.base.token==token then for key in pairs(selected)do if r[key]~=nil then error('TEMPORARY_OWNER_VALIDATOR_UNAVAILABLE')end end end
  return validate(r,...)
 end
 SPCStoreSubrecords.CheckOne=function(key,r,...)
  if r.base.token==token and selected[key]then return {status='CHECK_UNKNOWN',reason='TEMPORARY_OWNER_VALIDATOR_UNAVAILABLE'}end
  return check(key,r,...)
 end
 function readersAvailable()SPCStoreSubrecords.Validate=validate;SPCStoreSubrecords.CheckOne=check end
end
function prepare(keys)
 local n=seed();install(n);unavailable(keys);testReload();s=shared.CityProgressionStore
 s.RegisterExit('Fixture',function()end)
 originalID=ca:GetID();oldPayload=payloads(T.record(ca))
end
function lose()T.loss(ca,9,900);assert(T.record(ca).stage=='HELD_TRANSFER')end
function takeBack(id)
 ca.s.ref.owner=0;ca.s.ref.cityID=id or originalID;Events.CityTransfered.Fire(0,ca:GetID(),9)
 assert(T.record(ca).stage=='ACTIVE')
end
"""
def actual():
 v=fixture();v.execute(SETUP);return v

class Capture(unittest.TestCase):
 def test_actual_loss_return_save_keeps_all_five_opaque_payloads_and_one_episode_each(self):
  v=actual();v.execute("prepare('dialogue,engineering,capital,development,commerce');local before=T.writes();lose();local r=T.record(ca);local n=0;for key,e in pairs(r.deferredLifecycle.entries)do n=n+1;assert(e.epoch==1 and e.lossTurn==T.now()and not e.returned)end;assert(n==5 and payloads(r)==oldPayload and T.writes()==before+1);takeBack();r=T.record(ca);assert(payloads(r)==oldPayload and T.writes()==before+2);for _,e in pairs(r.deferredLifecycle.entries)do assert(e.returned.owner==0 and e.returnTurn==T.now())end;evidenceBytes=#T.encode(r.deferredLifecycle)")
  measure('S9f3_actual_saved_deferred_capture',{'actual_Store':True,'owners':5,'loss_Store_writes':1,'return_Store_writes':1,'extra_Store_writes':0,'opaque_payload_changes':0,'encoded_evidence_fixture_bytes':v.eval('evidenceBytes'),'scenario':'capture before reliable reader recovery'})
 def test_readers_available_after_return_do_not_expose_pre_loss_configuration_on_cold_load(self):
  v=actual();v.execute("prepare('commerce');lose();takeBack();readersAvailable();local bytes=T.encode(T.record(ca));local w=T.writes();testReload();s=shared.CityProgressionStore;assert(pcall(s.Base,0,ca)and pcall(s.DialogueState,0,ca)and not pcall(s.CommerceState,0,ca));assert(s.Status(ca).subrecordIsolation.commerce.status=='DEFERRED_LIFECYCLE'and T.encode(T.record(ca))==bytes and T.writes()==w)")
 def test_before_source_loses_the_skipped_episode_after_reload(self):
  with before():v=actual()
  v.execute("prepare('commerce');lose();takeBack();readersAvailable();testReload();s=shared.CityProgressionStore;assert(pcall(s.CommerceState,0,ca)and s.CommerceState(0,ca).value.selected[1]=='DISTRICT_CAMPUS'and not T.record(ca).deferredLifecycle)")
 def test_pending_owner_cannot_write_or_delete_opaque_payload(self):
  for field in ('commerce','dialogue','engineering','capital','development'):
   v=actual();v.execute("prepare(...);lose();takeBack();readersAvailable();testReload();local n=M.Copy(T.record(ca));local before=T.encode(n);local w=T.writes();n.revision=n.revision+1;n[...]=nil;assert(not saveCandidate(ca,n)and T.encode(T.record(ca))==before and T.writes()==w)",field)
 def test_pending_markers_cannot_be_repaired_before_lifecycle_transform(self):
  v=actual();v.execute("prepare('dialogue');lose();takeBack();readersAvailable();local n=M.Copy(T.record(ca));n.dialogueKnown=false;install(n);testReload();assert(T.record(ca).dialogueKnown==false and T.writes()==beforeWrites and shared.CityProgressionStore.Status(ca).subrecordIsolation.dialogue)")
 def test_second_same_turn_loss_coalesces_reference_and_epoch_without_growing_entries(self):
  v=actual();v.execute("prepare('commerce,dialogue');lose();takeBack();T.loss(ca,8,800);local r=T.record(ca);assert(r.stage=='HELD_TRANSFER'and r.ownerChanges==2);for _,e in pairs(r.deferredLifecycle.entries)do assert(e.epoch==2 and e.lossTarget.owner==8 and e.lossTarget.cityID==800 and not e.returned and e.firstTurn==0)end")
 def test_valid_sibling_still_commits_while_deferred_group_is_preserved(self):
  v=actual();v.execute("prepare('commerce');lose();takeBack();readersAvailable();testReload();s=shared.CityProgressionStore;local before=T.encode(T.record(ca).commerce);local old=s.DialogueState(0,ca).value;local n=M.Copy(old);n.serial=n.serial+1;s.WriteDialogue(0,ca,old,n);assert(T.record(ca).dialogue.serial==n.serial and T.encode(T.record(ca).commerce)==before and T.record(ca).deferredLifecycle.entries.commerce)")
 def test_insights_no_owner_mutation_has_no_spurious_deferred_duty(self):
  v=actual();v.execute("local n=seed();n.expeditionInsights={version=1,records={}};install(n);unavailable('expeditionInsights');testReload();s=shared.CityProgressionStore;s.RegisterExit('Fixture',function()end);originalID=ca:GetID();lose();takeBack();assert(not T.record(ca).deferredLifecycle)")
 def test_reputation_only_scope_keeps_valid_configuration_separate(self):
  from test_refactor_s8b7b import partial
  v=partial();v.execute(SETUP+"ca=c;s.RegisterExit('Fixture',function()end);originalID=ca:GetID();local rep=T.encode(T.record(ca).commerce.reputation);lose();assert(T.record(ca).deferredLifecycle.entries.commerce.scope=='REPUTATION');takeBack();testReload();s=shared.CityProgressionStore;local state=s.CommerceState(0,ca);assert(state.reputationKnown==false and state.value.owner==0);local old=state.value;local nextValue=SPCCommerceModel.Select(old,'DISTRICT_THEATER',true);s.WriteCommerce(0,ca,old,nextValue);assert(T.record(ca).commerce.selected[1]=='DISTRICT_THEATER'and T.encode(T.record(ca).commerce.reputation)==rep and T.record(ca).deferredLifecycle.entries.commerce.scope=='REPUTATION')")
 def test_invalid_future_reference_or_epoch_metadata_keeps_record_wholly_held(self):
  for mutation in ('n.deferredLifecycle.version=99','n.deferredLifecycle.token="OTHER"','n.deferredLifecycle.entries.commerce.epoch=2','n.deferredLifecycle.entries.commerce.lossTarget.cityID=12345','n.deferredLifecycle.entries.commerce.extra=true'):
   v=actual();v.execute("prepare('commerce');lose();takeBack();readersAvailable();local n=M.Copy(T.record(ca));"+mutation+";local frozen=install(n);testReload();s=shared.CityProgressionStore;assert(not pcall(s.Base,0,ca)and pcall(s.Base,0,cb)and T.writes()==beforeWrites and T.encode(T.record(ca))==frozen)")
 def test_failed_or_unknown_capture_write_never_blindly_retries(self):
  for mode in ('DROP','THROW_BEFORE','THROW_AFTER'):
   v=actual();v.execute("prepare('commerce');mode=...;local key=T.key(ca);local set=Game.SetProperty;attempts=0;Game.SetProperty=function(o,k,value)if k~=key then return set(o,k,value)end;attempts=attempts+1;if mode=='DROP'then return end;if mode=='THROW_BEFORE'then error('WRITE_UNKNOWN')end;set(o,k,value);error('AFTER_UNKNOWN')end;T.loss(ca,9,900);assert(attempts==1 and not pcall(s.Base,0,ca));local n=attempts;for i=1,1000 do Events.GameCoreEventPublishComplete.Fire()end;assert(attempts==n);if mode=='THROW_AFTER'then assert(T.record(ca).deferredLifecycle.entries.commerce)else assert(not T.record(ca).deferredLifecycle)end",mode)
 def test_idle_turn_publication_and_queries_do_not_add_capture_attempts(self):
  v=actual();v.execute("prepare('commerce');lose();takeBack();local w=T.writes();local bytes=T.encode(T.record(ca));for i=1,1000 do Events.GameCoreEventPublishComplete.Fire()end;for i=1,3 do T.turn(1)end;assert(T.writes()==w and T.encode(T.record(ca))==bytes)")
 def test_healthy_loss_return_keeps_no_field_write_or_extra_clock_read(self):
  values=[]
  for frozen in (True,False):
   with before()if frozen else nullcontext():v=actual()
   v.execute("local n=seed();install(n);testReload();s=shared.CityProgressionStore;s.RegisterExit('Fixture',function()end);originalID=ca:GetID();clockReads=0;local get=Game.GetCurrentGameTurn;Game.GetCurrentGameTurn=function()clockReads=clockReads+1;return get()end;local w=T.writes();lose();takeBack();assert(not T.record(ca).deferredLifecycle);extraWrites=T.writes()-w")
   values.append((v.eval('clockReads'),v.eval('extraWrites')))
  self.assertEqual(values[0],values[1]);measure('S9f3_healthy_lifecycle_budget',{'before_clock_reads':values[0][0],'after_clock_reads':values[1][0],'Store_writes_each':values[1][1],'extra_healthy_saved_fields':0})
 def test_new_clock_boundary_cannot_commit_over_a_synchronous_newer_store_root(self):
  v=actual();v.execute("prepare('commerce');local get=Game.GetCurrentGameTurn;local calls=0;Game.GetCurrentGameTurn=function()calls=calls+1;if calls==2 then local n=M.Copy(T.record(ca));n.revision=n.revision+1;assert(saveCandidate(ca,n))end;return get()end;local w=T.writes();T.loss(ca,9,900);assert(calls==2 and T.writes()==w+1 and T.record(ca).stage=='ACTIVE'and not T.record(ca).deferredLifecycle)")
 def test_actual_production_includes_only_capture_model_and_retains_Copy_limits(self):
  text=(ROOT/'Mod/CityProgressionStore.lua').read_text();self.assertIn("include('StoreDeferredLifecycle')",text);self.assertNotIn("include('StoreLifecycleRecovery')",text)
  self.assertNotIn('DEFERRED', (ROOT/'Mod/Gameplay.lua').read_text())
  text=(ROOT/'Mod/CityIdentityRead.lua').read_text();self.assertIn('8192',text);self.assertIn('65536',text)

def load_tests(loader,standard,pattern):
 # Use the existing S8b8 reviewed template profile, not superseded raw assertions.
 import test_refactor_s8b8 as templates
 import test_refactor_s8b9 as metadata
 suite=unittest.TestSuite([standard])
 for case in loader.loadTestsFromName('test_refactor_s8b7b.Store'):
  if case.id()not in templates.SUPERSEDED:suite.addTest(case)
 for case in loader.loadTestsFromName('test_refactor_s8b8.TemplateIsolation'):
  if case.id()not in metadata.SUPERSEDED:suite.addTest(case)
 for name in ('test_refactor_s8b8.FrozenBefore','test_refactor_s8b9.Metadata','test_refactor_s8b9.FrozenBefore','test_refactor_s9f1','test_refactor_s9f2'):
  suite.addTests(loader.loadTestsFromName(name))
 return suite

if __name__=='__main__':unittest.main()
