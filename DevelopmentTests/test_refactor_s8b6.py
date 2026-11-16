"""Claim timer isolation keeps independent identity/lifecycle and native exceptions intact."""
from pathlib import Path
from unittest.mock import patch
import json,unittest
from refactor_harness import ROOT,measure
from test_refactor_s8b2 import fixture
import test_refactor_s8b3 as history_source
import test_refactor_s8b5 as prior
from test_refactor_s7d1 import profile

BASE='e789909'
SUPERSEDED='test_refactor_s8b5.Groups.test_remaining_core_and_unreviewed_history_errors_still_hold_everything'


def isolated(extra=''):
 v=fixture();v.execute("local n=seed();n.claimTimer={version=1,stage='CALLING',unknown='preserve'};"+extra+"frozen=install(n);testReload();s=shared.CityProgressionStore");return v


def claim():
 path=ROOT/'DevelopmentTests/test_b140_templates.py';source=path.read_text();ns={'__file__':str(path)}
 exec(compile(source[:source.index('extra=r'+chr(39)*3)],str(path),'exec'),ns)
 header=ns['header'].replace('l=LuaRuntime()', 'l=LuaRuntime()\nl.globals().print=lambda *parts:None')
 body="""
 start();c=conquered(1,'DISTRICT_CAMPUS');request(c,'RESEARCH')
 function corruptClaim(stage)
  local n=M.Copy(record(c));n.claimTimer.stage=stage;n.claimTimer.reference.cityID=99999
  props[PREFIX..c.s.values.TOKEN]=n;return encode(n.claimTimer)
 end
 function corruptCore(mode)
  local n=M.Copy(record(c));n.claimTimer={version=1};if mode=='receipt'then n.claim={}else n.acquisition={}end
  props[PREFIX..c.s.values.TOKEN]=n;return encode(n)
 end
 function clearTimer()props[PREFIX..c.s.values.TOKEN].claimTimer=nil end
 function claimedKind()return record(c).base.specialization end
 function loadClaim()saved=true;boot();flush();s=shared.CityProgressionStore end
 function rawClaim()return encode(record(c).claimTimer)end
 function currentStage()return record(c).stage end
 function newTurn()turn=turn+1;Events.PlayerTurnActivated.Fire(0);flush()end
 function counters()return finishCalls,writes end
 function pulse()flush()end
 function recordBytes()return encode(record(c))end
 """
 with profile():exec(compile(header+ns['helpers']+ns['claim_setup']+body+'\n'+chr(39)*3+')',str(path),'exec'),ns)
 return ns['l']


class ClaimIsolation(unittest.TestCase):
 def test_bad_timer_does_not_hide_core_or_other_profession_histories(self):
  v=isolated();v.execute("assert(pcall(s.Base,0,ca)and pcall(s.Base,0,cb)and s.DialogueState(0,ca).value.total==15 and s.EngineeringState(0,ca).value.L==1);assert(s.Status(ca).subrecordIsolation.claimTimer and T.writes()==beforeWrites and T.encode(T.record(ca))==frozen)")
 def test_Claim_state_write_and_complete_reject_before_mutation(self):
  v=isolated();v.execute("assert(not pcall(s.ClaimState,0,ca)and not pcall(s.WriteClaimTimer,0,ca,nil,{})and not pcall(s.ClaimComplete,0,ca,{}));assert(T.writes()==beforeWrites and T.encode(T.record(ca))==frozen and pcall(s.Base,0,ca))")
 def test_normal_investment_and_save_preserve_timer_while_replacement_is_rejected(self):
  v=isolated();v.execute("local old=T.encode(T.record(ca).claimTimer);T.invest(ca,99901);assert(shared.EffectiveFacts.Read(0,ca).potential==2 and T.encode(T.record(ca).claimTimer)==old);local n=M.Copy(T.record(ca));local writes=T.writes();n.revision=n.revision+1;n.claimTimer=nil;assert(not saveCandidate(ca,n)and T.writes()==writes and T.encode(T.record(ca).claimTimer)==old)")
 def test_confirmed_loss_and_return_preserve_opaque_timer_without_blocking_core(self):
  v=isolated();v.execute("local old=T.encode(T.record(ca).claimTimer);local id=ca:GetID();s.RegisterExit('Fixture',function()end);T.loss(ca,9,900);assert(T.record(ca).stage=='HELD_TRANSFER'and T.encode(T.record(ca).claimTimer)==old);ca.s.ref.owner=0;ca.s.ref.cityID=id;Events.CityTransfered.Fire(0,id,9);assert(T.record(ca).stage=='ACTIVE'and pcall(s.Base,0,ca)and T.encode(T.record(ca).claimTimer)==old and not pcall(s.ClaimState,0,ca))")
 def test_core_claim_receipt_and_unreviewed_Commerce_or_template_failure_stay_strict(self):
  for bad in ("n.schema=99","n.base.token='FORGED'","n.origin.x=12345","n.commerce='BROKEN'","n.templates={}"):
   v=isolated(bad+';');v.execute("assert(not pcall(s.Base,0,ca)and pcall(s.Base,0,cb)and T.writes()==beforeWrites and T.encode(T.record(ca))==frozen and next(s.Status(ca).subrecordIsolation)==nil)")
 def test_independent_first_profession_completion_still_works_with_unrelated_bad_timer(self):
  v=fixture();v.execute("c=T.fresh(3);T.register(c);local n=M.Copy(T.record(c));n.claimTimer={version=1};T.propsSet(T.key(c),n);testReload();local s=shared.CityProgressionStore;assert(s.Base(0,c).specialization=='NONE');T.complete(c,'DISTRICT_CAMPUS');assert(s.Base(0,c).specialization=='RESEARCH'and shared.EffectiveFacts.Read(0,c).potential==1 and T.record(c).claimTimer.version==1 and s.Status(c).subrecordIsolation.claimTimer)")
 def test_healthy_native_Claim_completion_without_timer_keeps_existing_exception(self):
  v=claim();v.execute("clearTimer();loadClaim();Events.CityProjectCompleted.Fire(0,c:GetID(),101);pulse();assert(claimedKind()=='RESEARCH'and pcall(s.Base,0,c))")
 def test_real_schema3_acquisition_or_Claim_receipt_damage_still_blocks_core(self):
  for mode in ('receipt','acquisition'):
   v=claim();v.execute("local frozen=corruptCore(...);local f,w=counters();loadClaim();assert(not pcall(s.Base,0,c)and recordBytes()==frozen and select(2,counters())==w)",mode)
 def test_actual_Claim_projects_do_not_finish_or_replace_invalid_ACTIVE_or_CALLING_timer(self):
  for stage in ('ACTIVE','CALLING'):
   v=claim();v.execute("original=corruptClaim(...);local f,w=counters();loadClaim();assert(pcall(s.Base,0,c)and not pcall(s.ClaimState,0,c)and rawClaim()==original and select(2,counters())==w);for id=201,204 do assert(not c.q.buildings[id])end;for i=1,3 do newTurn()end;Events.CityProjectCompleted.Fire(0,c:GetID(),101);pulse();assert(select(1,counters())==f and select(2,counters())==w and rawClaim()==original and currentStage()=='ACTIVE');local reads=select(2,counters());for i=1,1000 do pulse()end;assert(select(2,counters())==reads)",stage)
  measure('S8b6_actual_Claim_isolation',{'new_native_completions':0,'corrupt_timer_preserved':True,'new_Claim_receipts':0,'idle_history_writes':0,'access':'existing_UNKNOWN_withdrawal'})


class FrozenBefore(unittest.TestCase):
 def test_original_unreviewed_timer_scope_matrix_kept_on_B344(self):
  with patch.object(history_source,'BASE',BASE),history_source.before():prior.Groups('test_remaining_core_and_unreviewed_history_errors_still_hold_everything').test_remaining_core_and_unreviewed_history_errors_still_hold_everything()


def load_tests(loader,standard,pattern):
 selection=json.loads((ROOT/'DevelopmentTests/refactor_selection.json').read_text())
 def flatten(suite):
  for test in suite:
   if isinstance(test,unittest.TestSuite):yield from flatten(test)
   else:yield test
 inherited=unittest.TestSuite()
 for name in selection['stages']['S8b5']:
  for test in flatten(loader.loadTestsFromName(name)):
   if test.id()!=SUPERSEDED:inherited.addTest(test)
 return unittest.TestSuite([standard,inherited])

if __name__=='__main__':unittest.main()
