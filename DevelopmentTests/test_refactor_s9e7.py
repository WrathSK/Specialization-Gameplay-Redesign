"""R04 existing D0040/D0058 Tradition owner resume; no new ownership policy."""
from contextlib import contextmanager,nullcontext
from pathlib import Path
from hashlib import sha256
from unittest.mock import patch
import subprocess,unittest
from refactor_harness import ROOT,TrackedLua51,SOURCES,legacy_source_observation,measure
from test_refactor_s5d4c7 import fixture
import test_refactor_s7c as previous


@contextmanager
def baseline():
 rows={ROOT/'Mod'/(n+'.lua'):subprocess.check_output(['git','show','7c47fa5:Mod/'+n+'.lua'],cwd=ROOT,text=True)for n in ('ResearchTradition','CityProgressionStore')}
 read,execute=Path.read_text,TrackedLua51.execute
 hashes={sha256(s.encode()).hexdigest():'historical/7c47fa5/'+str(p.relative_to(ROOT))for p,s in rows.items()}
 def run(vm,s,*a,**kw):
  h=sha256(s.encode()if isinstance(s,str)else s).hexdigest()
  if h in hashes:SOURCES[h]=hashes[h]
  return execute(vm,s,*a,**kw)
 with patch.object(Path,'read_text',lambda p,*a,**kw:rows[p]if p in rows else read(p,*a,**kw)),patch.object(TrackedLua51,'execute',run):yield


def prepared():
 v=fixture();v.execute("""
 origin=c:GetID();for i=1,10 do T.turn(1);pp()end
 receipt=T.snapshot(c).researchTradition.receipt;assert(T.snapshot(c).researchTradition.age==10 and current(c)==10)
 function back()c.s.ref.owner=0;c.s.ref.cityID=origin;Events.CityTransfered.Fire(0,origin,9)end
 T.loss(c,9,900);pp();assert(T.record(c).stage=='HELD_TRANSFER'and current(c)==0)
 T.turn(20);pp();assert(T.record(c).researchTradition.age==10)
 """);return v


def cold_reload(v):
 # This fixture's boot starts Store only. Reattach the actual effect owner and
 # its native doubles before the original confirmed-exit recovery boundary.
 v.execute("""
 local has,create,remove=P.HasBuilding,P.CreateBuilding,P.RemoveBuilding
 T.reload();local info=P.Info;P.Info=function(kind,k)return kind=='Buildings'and meta[k]or info(kind,k)end
 P.HasBuilding=has;P.CreateBuilding=create;P.RemoveBuilding=remove
 SPCNativeFacts.New(P,shared);SPCFactConsumerBindings.New(shared);SPCResearchTraditionEffects.Start(P,shared);effects=shared.ResearchTraditionEffects
 shared.CityProgressionStore.ExitConfirmed();pp()
 """)


class Model(unittest.TestCase):
 def test_resume_never_credits_held_time_and_preserves_entire_valid_origin(self):
  v=previous.pure();v.execute("""
  local R=SPCResearchTradition
  for _,state in ipairs({'COUNTING','PAUSED_IDENTITY','OWNER_POLICY_UNRESOLVED','UNKNOWN_INTERVAL'})do
   local t=R.Begin(5,'P4');t.cursor=15;t.age=10;t.state=state;local receipt=t.receipt
   local n=R.ResumeOwner(t,50,'RESEARCH');assert(n.age==10 and n.cursor==50 and n.state=='COUNTING'and n.receipt==receipt and n.start==5)
   assert(t.cursor==15 and t.state==state);n=R.Advance(n,51,'RESEARCH');assert(n.age==11)
   n=R.ResumeOwner(t,50,'CULTURE');assert(n.age==10 and n.state=='PAUSED_IDENTITY');n=R.Advance(n,51,'CULTURE');assert(n.age==10)
  end
  """)
 def test_invalid_or_unreadable_input_does_not_mutate_the_old_record(self):
  v=previous.pure();v.execute("local R=SPCResearchTradition;local t=R.Begin(5,'P4');assert(not pcall(R.ResumeOwner,t,4,'RESEARCH')and not pcall(R.ResumeOwner,t,9,nil));assert(t.cursor==5 and t.age==0 and t.state=='COUNTING');t.age=-1;assert(not pcall(R.ResumeOwner,t,9,'RESEARCH')and t.age==-1)")
 def test_old_active_owner_hold_rebases_without_backfill_and_next_full_turn_counts(self):
  v=previous.pure();v.execute("local R=SPCResearchTradition;local t=R.Begin(5,'P4');t.cursor=15;t.age=10;t.state='OWNER_POLICY_UNRESOLVED';local n,skipped=R.Advance(t,50,'RESEARCH');assert(skipped and n.age==10 and n.cursor==50 and n.state=='COUNTING');n=R.Advance(n,51,'RESEARCH');assert(n.age==11 and n.receipt=='P4')")


class RealStore(unittest.TestCase):
 def test_actual_loss_return_and_age_effect_resume_counterexample(self):
  values=[]
  for old in (True,False):
   with baseline()if old else nullcontext():v=prepared()
   v.execute("local w=T.writes();back();returnWrites=T.writes()-w;assert(T.record(c).stage=='ACTIVE');pp();returned={age=T.snapshot(c).researchTradition.age,cursor=T.snapshot(c).researchTradition.cursor,state=T.snapshot(c).researchTradition.state,effect=current(c)};T.turn(1);pp()")
   values.append(dict(returned=dict(v.globals().returned),next_age=v.eval('T.snapshot(c).researchTradition.age'),return_writes=v.eval('returnWrites')))
   if not old:v.execute("assert(T.snapshot(c).researchTradition.receipt==receipt);local n=T.writes();local h=history();for i=1,1000 do pp()end;assert(T.writes()==n and history()==h)")
  self.assertEqual(values[0]['next_age'],10);self.assertEqual(values[1]['next_age'],11)
  self.assertEqual(values[1]['returned'],dict(age=10,cursor=30,state='COUNTING',effect=10))
  self.assertEqual(values[0]['return_writes'],values[1]['return_writes'])
  measure('S9e7_Tradition_confirmed_owner_return',{'baseline':'B379','foreign_interval':20,'before':values[0],'after':values[1],'foreign_interval_age_credit':0,'native_effect_CPU_save':'USER_GAME_TEST_REQUIRED'})
 def test_cold_held_record_returns_from_same_city_age_without_replay(self):
  v=prepared();cold_reload(v);v.execute("assert(T.record(c).stage=='HELD_TRANSFER'and T.record(c).researchTradition.age==10);back();assert(T.snapshot(c).researchTradition.state=='COUNTING'and T.snapshot(c).researchTradition.age==10 and T.snapshot(c).researchTradition.cursor==T.now());T.turn(1);assert(T.snapshot(c).researchTradition.age==11 and T.snapshot(c).researchTradition.receipt==receipt)")
 def test_failed_return_callback_cannot_commit_a_speculative_rebase(self):
  v=prepared();v.execute("""
  local s=shared.CityProgressionStore;local before=T.encode(T.record(c).researchTradition);local allow=false
  s.RegisterReturn('Fault',function()if not allow then error('RETURN_FACTS_UNAVAILABLE')end end)
  local w=T.writes();back();assert(T.record(c).stage=='HELD_TRANSFER'and T.writes()==w and T.encode(T.record(c).researchTradition)==before)
  allow=true;back();pp();assert(T.snapshot(c).researchTradition.age==10 and T.snapshot(c).researchTradition.state=='COUNTING'and current(c)==10)
  """)
 def test_unconfirmed_native_return_never_rebases_history(self):
  v=prepared();v.execute("""
  local before=T.encode(T.record(c).researchTradition);local get=c.GetOwner
  c.GetOwner=function()error('NATIVE_RETURN_UNREADABLE')end
  back();assert(T.record(c).stage=='HELD_TRANSFER'and T.encode(T.record(c).researchTradition)==before)
  c.GetOwner=get;back();pp();assert(T.record(c).stage=='ACTIVE'and T.snapshot(c).researchTradition.age==10 and current(c)==10)
  """)
 def test_isolated_bad_Tradition_is_not_reset_or_allowed_to_block_other_return(self):
  v=prepared();v.execute("T.record(c).researchTradition='BROKEN_PAYLOAD'");cold_reload(v);v.execute("back();assert(T.record(c).stage=='ACTIVE'and T.record(c).researchTradition=='BROKEN_PAYLOAD');assert(not pcall(shared.CityProgressionStore.ReadTradition,0,c));assert(shared.EffectiveFacts.Read(0,c).specialization=='RESEARCH')")
 def test_postcommit_history_notification_failure_does_not_rollback_or_backfill(self):
  v=prepared();v.execute("""
  local fc=shared.FactChanges;local emit=fc.Emit;fc.Emit=function(e)if e.topic=='TRADITION'then error('OBSERVER_FAILED_AFTER_RETURN')end;return emit(e)end
  back();assert(T.record(c).stage=='ACTIVE'and T.snapshot(c).researchTradition.age==10 and T.snapshot(c).researchTradition.state=='COUNTING'and shared.PermanentWriteObserverError)
  fc.Emit=emit;T.turn(1);pp();assert(T.snapshot(c).researchTradition.age==11 and current(c)==10)
  """)
 def test_return_commits_before_history_consumers_and_uses_existing_receipt(self):
  v=prepared();v.execute("""
  local fc=shared.FactChanges;local n=0
  fc.RegisterConsumer('ResumeAudit',function(e)
   if e.topic=='TRADITION'or e.topics.TRADITION then n=n+1;assert(T.record(c).stage=='ACTIVE'and T.snapshot(c).researchTradition.state=='COUNTING'and T.snapshot(c).researchTradition.receipt==receipt)end
  end,{kinds={'HISTORY'},topics={'TRADITION'}})
  back();assert(n==0 and current(c)==0);pp();assert(n==1 and current(c)==10)
  """)


class UnscopedRouting(unittest.TestCase):
 def test_actual_infrastructure_unscoped_audit_still_applies_required_carrier(self):
  from test_refactor_s5d4c1 import actual
  v=actual();v.execute("infra=shared.ResearchInfrastructure;infra.Audit();assert(cities[1].carriers[GameInfo.Buildings.BUILDING_SPC_RESEARCH_INFRA_0.Index]and not infra.errors.runtime and not infra.auditError)")
 def test_nil_and_non_table_scopes_are_not_transfer_metadata(self):
  from refactor_harness import Context
  v=Context();v.load('RuntimeWork');v.execute("""
  P={IsTestPlayer=function(pid)return pid==0 end,Count=function()end};calls=0
  local c={GetOwner=function()return 0 end,GetID=function()return 7 end,GetX=function()return 1 end,GetY=function()return 2 end}
  Players={[0]={GetCities=function()return {Members=function()return ipairs({c})end}end}}
  t=SPCRuntimeWork.NewTargets(P,shared,function()calls=calls+1 end,function(_,_,why)assert(not why,why)end)
  t.Run();t.Run(false);t.Run(7);t.Run({});assert(calls==4 and not t.error)
  local seen=0;SPCRuntimeWork.LifecycleScopes(P,nil,function(s)assert(s==nil);seen=seen+1 end);assert(seen==1)
  """)
 def test_explicit_false_transfer_is_rejected_before_any_native_work(self):
  from refactor_harness import Context
  v=Context();v.load('RuntimeWork');v.execute("P={IsTestPlayer=function()error('SHOULD_NOT_READ_NATIVE')end};Players={};local why;t=SPCRuntimeWork.NewTargets(P,shared,function()error('UNEXPECTED_VISIT')end,function(_,_,e)why=e end);t.Run({transfer=false});assert(why:find('RUNTIME_TRANSFER_STRUCTURE',1,true)and next(t.transfers)==nil)")


class FrozenBefore(unittest.TestCase):
 def test_old_absorbing_owner_hold_assertion_is_retained_on_B379(self):
  with baseline():previous.Boundaries().test_old_UNKNOWN_resumes_but_owner_holds_remain_independent(resumed_tradition=False)

 def test_old_stale_writer_guards_and_original_terminal_values_preserved_on_B379(self):
  import test_refactor_s9d1b as barrier
  import test_refactor_s9d1 as publication
  with baseline():
   barrier.Witness().test_same_reference_loss_return_invalidates_old_Base_witness_before_facts_return(resumed_tradition=False)
   barrier.WriteBarrier().test_loss_return_after_remove_same_owner_ID_token_still_rejects_old_scope(resumed_tradition=False)
   publication.Exit().test_return_with_new_local_ID_then_second_loss_uses_fixed_location(resumed_tradition=False)

if __name__=='__main__':unittest.main()
