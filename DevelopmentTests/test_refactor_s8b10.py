"""Only a strict completed initial Claim receipt proves obsolete timer cleanup."""
from pathlib import Path
from unittest.mock import patch
import json,unittest
from refactor_harness import ROOT,measure
from test_refactor_s8b6 import claim
from test_refactor_s8b2 import BAD
import test_refactor_s8b8 as history_source

BASE='b67de3f'


def completed(timer="{version=1,stage='CALLING',extension='obsolete'}",extra=''):
 v=claim();v.execute("Events.CityProjectCompleted.Fire(0,c:GetID(),101);pulse();assert(claimedKind()=='RESEARCH');recordKey=SPCCityProgressionStore.RECORD..c:GetProperty(M.Keys.TOKEN);local n=Game:GetProperty(recordKey);n.claimTimer="+timer+';'+(extra+';'if extra else '')+"beforeClaim=M.Copy(n.claim);Game:SetProperty(recordKey,n);originalRecord=Game:GetProperty(recordKey);beforeFinishes,beforeWrites=counters();loadClaim();s=shared.CityProgressionStore");return v


class Terminal(unittest.TestCase):
 def test_actual_completed_receipt_clears_obsolete_timer_once_without_native_completion_replay(self):
  for timer in ("{version=1,stage='CALLING',extension='obsolete'}",'false',"'BROKEN'",'{}'):
   v=completed(timer);v.execute("assert(pcall(s.Base,0,c)and claimedKind()=='RESEARCH'and rawClaim()=='nil'and s.ClaimState(0,c).eligible==false);local st=s.Status(c);assert(not st.subrecordIsolation.claimTimer and st.subrecordRecovery.kind=='COMPLETED_CLAIM_TIMER_CLEARED'and #st.subrecordRecovery.fields==1);assert(select(1,counters())==beforeFinishes and select(2,counters())==beforeWrites+1);local after=Game:GetProperty(recordKey);assert(after.claim.project==beforeClaim.project and after.claim.turn==beforeClaim.turn and after.revision==originalRecord.revision+1);local w=select(2,counters());loadClaim();Events.CityProjectCompleted.Fire(0,c:GetID(),101);pulse();for i=1,1000 do pulse()end;assert(select(1,counters())==beforeFinishes and select(2,counters())==w and not s.Status(c).subrecordRecovery)")
  measure('S8b10_terminal_Claim',{'proof':'strict initial Claim receipt and full core','restore_CAS':1,'repeat_restore_CAS':0,'native_completions_replayed':0,'queue_or_elapsed_time_proof':False})
 def test_bad_receipt_or_core_cannot_be_hidden_by_clearing_timer(self):
  for extra in ("n.claim.token='FORGED'","n.claim.project='OTHER'","n.claim.turn=n.claim.turn+1","n.acquisition.mode='FIRST_COMPLETION'","n.base.token='FORGED'","n.schema=99"):
   v=completed(extra=extra);v.execute("assert(not pcall(s.Base,0,c)and rawClaim()~='nil'and select(2,counters())==beforeWrites and not s.Status(c).subrecordRecovery)")
 def test_uncompleted_ACTIVE_CALLING_and_empty_queue_still_preserve_opaque_timer(self):
  for stage in ('ACTIVE','CALLING'):
   v=claim();v.execute("local raw=corruptClaim(...);local f,w=counters();loadClaim();for i=1,3 do newTurn()end;assert(rawClaim()==raw and select(2,counters())==w and select(1,counters())==f and not s.Status(c).subrecordRecovery)",stage)
 def test_later_restructuring_or_reference_invalidation_is_not_the_initial_receipt_episode(self):
  # The pure trigger must refuse both cases before any copy/authority request.
  v=completed('nil');v.execute("local r=Game:GetProperty(recordKey);r.claimTimer={stage='CALLING'};local copy=function()error('COPY_FORBIDDEN')end;r.restructuring={phase='UNASSIGNED'};assert(not SPCStoreSubrecords.NeedsCompletedClaimCleanup(r)and SPCStoreSubrecords.CompletedClaimCandidate(r,copy)==nil);r.restructuring=nil;r.referenceInvalidated=true;assert(not SPCStoreSubrecords.NeedsCompletedClaimCleanup(r));r.referenceInvalidated=nil;r.stage='HELD_TRANSFER';assert(not SPCStoreSubrecords.NeedsCompletedClaimCleanup(r))")
 def test_known_repair_and_timer_cleanup_merge_while_bad_sibling_stays_exact(self):
  v=completed(extra="n.capitalKnown=false;n.capital=SPCCapitalInvestmentModel.Encode(SPCCapitalInvestmentModel.New());n.expeditionInsights="+BAD)
  v.execute("local r=Game:GetProperty(recordKey);assert(r.claimTimer==nil and r.capitalKnown and r.expeditionInsights.records.WRONG.nested.extra==7 and select(2,counters())==beforeWrites+1 and s.Status(c).subrecordIsolation.expeditionInsights and #s.Status(c).subrecordRecovery.fields==2)")
 def test_uncertain_setter_never_reports_recovery_or_retries(self):
  v=claim();v.execute("Events.CityProjectCompleted.Fire(0,c:GetID(),101);pulse();local key=SPCCityProgressionStore.RECORD..c:GetProperty(M.Keys.TOKEN);local n=Game:GetProperty(key);n.claimTimer={stage='CALLING'};Game:SetProperty(key,n);local set=Game.SetProperty;attempts=0;Game.SetProperty=function(o,k,value)if k==key then attempts=attempts+1;error('UNCERTAIN')end;return set(o,k,value)end;local f,w=counters();loadClaim();assert(not pcall(s.Base,0,c)and attempts==1 and select(2,counters())==w and select(1,counters())==f and not s.Status(c).subrecordRecovery);for i=1,1000 do pulse()end;assert(attempts==1)")
 def test_prior_source_preserves_completed_but_unavailable_timer_counterexample(self):
  with patch.object(history_source,'BASE',BASE),history_source.before():v=completed()
  v.execute("assert(pcall(s.Base,0,c)and not pcall(s.ClaimState,0,c)and rawClaim()~='nil'and select(2,counters())==beforeWrites and s.Status(c).subrecordIsolation.claimTimer)")


def load_tests(loader,standard,pattern):
 selection=json.loads((ROOT/'DevelopmentTests/refactor_selection.json').read_text())
 return unittest.TestSuite([standard,unittest.TestSuite(loader.loadTestsFromName(name)for name in selection['stages']['S8b9'])])

if __name__=='__main__':unittest.main()
