"""D0059 lawful Commerce exit is a business transition, not history repair."""
from unittest.mock import patch
from contextlib import contextmanager
from pathlib import Path
import subprocess,unittest
from refactor_harness import ROOT,legacy_source_observation,measure
from test_refactor_s8b7b import partial
BASE='cc70f79'
TEAM="{owner=0,id=777,uid='TEAM:777'}"
def begin(v):v.execute("s.BeginRestructuring(0,c,"+TEAM+",'PU06_EXIT')")
@contextmanager
def before():
 p=ROOT/'Mod/CityProgressionStore.lua';read=Path.read_text
 source=subprocess.check_output(['git','show',BASE+':Mod/CityProgressionStore.lua'],cwd=ROOT,text=True)
 with patch.object(Path,'read_text',lambda f,*a,**kw:source if f==p else read(f,*a,**kw)),legacy_source_observation():yield

class Exit(unittest.TestCase):
 def test_actual_exit_releases_bad_leaf_only_after_lawful_transition(self):
  v=partial('n.commerceKnown=false;');begin(v);v.execute("assert(T.record(c).restructuring.phase=='REALLOCATING');assert(T.record(c).commerce.reputation==nil,'OLD_REPUTATION_REMERGED_AT_LAWFUL_EXIT');assert(T.record(c).commerceKnown==true and #T.record(c).commerce.selected==0);assert(not s.Status(c).reputationIsolation and T.writes()==beforeWrites+1)")
 def test_unknown_capital_and_other_isolated_siblings_preserved_exact(self):
  v=partial("n.capitalKnown=false;n.capital='UNKNOWN_NATIVE_RECEIPT';n.dialogueKnown=false;n.dialogue={unknown='KEEP'};n.expeditionInsights={version=1,records={WRONG={value='KEEP'}}};")
  v.execute("capBefore=T.encode(T.record(c).capital);dialogueBefore=T.encode(T.record(c).dialogue);insightsBefore=T.encode(T.record(c).expeditionInsights)");begin(v)
  v.execute("assert(not T.record(c).commerce.reputation,'SIBLING_ISOLATION_PREVENTED_LAWFUL_EXIT');assert(T.encode(T.record(c).capital)==capBefore and T.record(c).capitalKnown==false and T.encode(T.record(c).dialogue)==dialogueBefore and T.encode(T.record(c).expeditionInsights)==insightsBefore);assert(s.Status(c).subrecordIsolation.capital and s.Status(c).subrecordIsolation.dialogue and s.Status(c).subrecordIsolation.expeditionInsights)")
 def test_ordinary_private_save_cannot_forge_reputation_reset(self):
  v=partial();v.execute("local n=M.Copy(T.record(c));n.commerce.reputation=nil;n.commerceKnown=true;n.revision=n.revision+1;assert(not saveCandidate(c,n));assert(T.writes()==beforeWrites and T.encode(T.record(c))==frozen)")
 def test_configuration_write_cannot_reset_or_replace_reputation(self):
  for replacement in ('nil',"{version=1,start=0,cursor=0,age=0,state='COUNTING',receipt='FAKE'}"):
   v=partial();v.execute("local old=s.CommerceState(0,c).value;local n=SPCCommerceModel.Select(old,'DISTRICT_HARBOR',true);n.reputation="+replacement+";local ok=pcall(s.WriteCommerce,0,c,old,n);assert(T.encode(T.record(c).commerce.reputation)==T.encode(original.commerce.reputation));assert("+('ok'if replacement=='nil'else'not ok')+")")
 def test_governor_and_owner_changes_do_not_grant_reset(self):
  v=partial();v.execute("local raw=rawRep();T.governor(1);T.turn(1);assert(rawRep()==raw);local id=c:GetID();s.RegisterExit('Fixture',function()end);T.loss(c,9,900);assert(rawRep()==raw);c.s.ref.owner=0;c.s.ref.cityID=id;Events.CityTransfered.Fire(0,id,9);assert(rawRep()==raw and s.Status(c).reputationIsolation)")
 def test_parent_reference_and_transition_failures_never_reset(self):
  for change in ("n.base.token='FORGED'","n.schema=99","n.restructuring={}"):
   v=partial(change+';');v.execute("assert(not pcall(s.BeginRestructuring,0,c,"+TEAM+",'BAD'));assert(T.writes()==beforeWrites and T.encode(T.record(c))==frozen)")
  v=partial();v.execute("c.s.ref.x=c.s.ref.x+1;assert(not pcall(s.BeginRestructuring,0,c,"+TEAM+",'BAD'));assert(T.writes()==beforeWrites and T.encode(T.record(c))==frozen)")
 def test_write_failure_does_not_release_or_repeat(self):
  v=partial();v.execute("local key=T.key(c);local set=Game.SetProperty;attempts=0;Game.SetProperty=function(o,k,n)if k==key then attempts=attempts+1;error('INJECTED_WRITE_FAILURE')end;return set(o,k,n)end;assert(not pcall(s.BeginRestructuring,0,c,"+TEAM+",'FAIL'));assert(attempts==1 and T.encode(T.record(c))==frozen and s.Status(c).reputationIsolation);assert(not pcall(s.BeginRestructuring,0,c,"+TEAM+",'FAIL')and attempts==1)")
 def test_successful_reset_survives_reload_and_does_not_resurrect_age(self):
  v=partial();begin(v);v.execute("local writes=T.writes();testReload();s=shared.CityProgressionStore;assert(not T.record(c).commerce.reputation,'OLD_REPUTATION_RESURRECTED_ON_LOAD');assert(not s.Status(c).reputationIsolation);T.turn(5);assert(not T.record(c).commerce.reputation);assert(T.record(c).restructuring.phase=='REALLOCATING');local old=T.encode(T.record(c));s.BeginRestructuring(0,c,"+TEAM+",'PU06_EXIT');assert(T.encode(T.record(c))==old)")
 def test_deferred_reputation_only_duty_is_superseded_not_other_duties(self):
  v=partial("n.capitalKnown=false;n.capital='UNKNOWN_CAPITAL_RECEIPT';");v.execute("local id=c:GetID();s.RegisterExit('Fixture',function()end);T.loss(c,9,900);c.s.ref.owner=0;c.s.ref.cityID=id;Events.CityTransfered.Fire(0,id,9);local n=T.record(c);assert(n.deferredLifecycle.entries.commerce.scope=='REPUTATION'and n.deferredLifecycle.entries.capital);capitalDuty=T.encode(n.deferredLifecycle.entries.capital);capBefore=T.encode(n.capital)");begin(v)
  v.execute("local n=T.record(c);assert(not n.commerce.reputation,'DEFERRED_REPUTATION_SURVIVED_LAWFUL_EXIT');assert(not n.deferredLifecycle.entries.commerce and T.encode(n.deferredLifecycle.entries.capital)==capitalDuty and T.encode(n.capital)==capBefore);testReload();s=shared.CityProgressionStore;assert(not s.Status(c).reputationIsolation and s.Status(c).subrecordIsolation.capital)")
 def test_whole_configuration_isolation_is_not_a_leaf_exception(self):
  v=partial("n.commerce.selected='UNKNOWN_CONFIGURATION';");begin(v);v.execute("assert(s.Status(c).subrecordIsolation.commerce and T.encode(T.record(c).commerce)==T.encode(original.commerce));assert(T.record(c).restructuring.phase=='REALLOCATING')")
 def test_first_exit_only_one_write_no_idle_retry_or_native_call(self):
  v=partial();begin(v);v.execute("local writes=T.writes();assert(writes==beforeWrites+1);for i=1,1000 do Events.GameCoreEventPublishComplete.Fire()end;assert(T.writes()==writes)")
 def test_restricted_lua_uses_no_debug_or_raw_helpers(self):
  v=partial();v.execute('debug=nil;rawget=nil;rawset=nil;rawequal=nil;collectgarbage=nil;os=nil;io=nil;package=nil');begin(v);v.execute("assert(not T.record(c).commerce.reputation and not s.Status(c).reputationIsolation)")

class Boundaries(unittest.TestCase):
 def test_healthy_exit_saved_bytes_and_writes_match_fixed_baseline(self):
  rows=[]
  from contextlib import nullcontext
  for old in (True,False):
   with before()if old else nullcontext():
    v=partial("n.commerce.reputation=SPCCommerceModel.Copy(T.record(c).commerce.reputation);");v.execute("T.turn(2);beforeWrites=T.writes()");begin(v);rows.append((v.eval('T.encode(T.record(c))'),v.eval('T.writes()-beforeWrites')))
  self.assertEqual(rows[0],rows[1]);self.assertEqual(rows[1][1],1)
  measure('PU06a_healthy_exit',{'same_as_fixed_baseline':True,'durable_writes':1})
 def test_temporary_leaf_reader_failure_does_not_prevent_confirmed_exit(self):
  v=partial();v.execute("local read=SPCCommerceModel.ValidateReputation;SPCCommerceModel.ValidateReputation=function(t,r)if t then error('DEPENDENCY_NOT_READY')end;return read(t,r)end;testReload();s=shared.CityProgressionStore;assert(s.Status(c).reputationIsolation.status=='CHECK_UNKNOWN')");begin(v);v.execute("assert(not T.record(c).commerce.reputation and not s.Status(c).reputationIsolation)")
 def test_invalid_team_never_obtains_exit_permission(self):
  v=partial();v.execute("assert(not pcall(s.BeginRestructuring,0,c,{owner=9,id=777,uid='BAD'},'BAD'));assert(T.encode(T.record(c))==frozen and T.writes()==beforeWrites and s.Status(c).reputationIsolation)")
 def test_reentry_during_write_cannot_observe_candidate_or_start_another_exit(self):
  v=partial();v.execute("local key=T.key(c);local set=Game.SetProperty;reentries=0;Game.SetProperty=function(o,k,n)if k==key then reentries=reentries+1;assert(not pcall(s.CommerceState,0,c));assert(not pcall(s.BeginRestructuring,0,c,{owner=0,id=888,uid='REENTER'},'REENTER'));assert(s.Status(c).reputationIsolation)end;return set(o,k,n)end");begin(v);v.execute("assert(reentries==1 and T.writes()==beforeWrites+1 and not s.Status(c).reputationIsolation)")
 def test_bad_native_readback_remains_held_without_release(self):
  v=partial();v.execute("local key=T.key(c);local set=Game.SetProperty;Game.SetProperty=function(o,k,n)if k==key then local changed=M.Copy(n);changed.commerceKnown=false;return set(o,k,changed)end;return set(o,k,n)end;assert(not pcall(s.BeginRestructuring,0,c,{owner=0,id=777,uid='TEAM:777'},'BAD_READBACK'));assert(not pcall(s.Base,0,c)and s.Status(c).reputationIsolation);local writes=T.writes();assert(not pcall(s.BeginRestructuring,0,c,{owner=0,id=777,uid='TEAM:777'},'BAD_READBACK')and T.writes()==writes)")
 def test_reset_known_marker_remains_valid_after_other_profession_configuration(self):
  v=partial();begin(v);v.execute("T.turn(5);s.ConfigureRestructuring(0,c,{owner=0,id=777,uid='TEAM:777'},'CULTURE',{districtID=601,type='DISTRICT_THEATER',turn=T.now()});Players[0].GetUnits=function()return {FindID=function()return nil end}end;s.ConfirmRestructuringConsumption(0,c,{owner=0,id=777,uid='TEAM:777'});s.FinishRestructuring(0,c,{owner=0,id=777,uid='TEAM:777'});testReload();s=shared.CityProgressionStore;assert(T.record(c).commerceKnown and not T.record(c).commerce.reputation and not s.Status(c).reputationIsolation and s.Base(0,c).specialization=='CULTURE')")

class MoneyReceipts(unittest.TestCase):
 def test_real_model_unknown_debit_and_credit_receipts_survive_exactly(self):
  for stage in ('DEBIT_CALLING','CREDIT_CALLING'):
   setup="""local model=SPCCapitalInvestmentModel;local source=shared.CityProgressionStore.HistoricalReference(c);source.changes=n.ownerChanges or 0;local q=model.Quote({domain='DISTRICT_CAMPUS',source=source,turn=T.now(),D=3,R=20,failureCount=0,balance=1000});local history=model.Begin(model.New(),q,'STABLE',0,'LOCKED_RECEIPT');local contract=history.contracts.DISTRICT_CAMPUS;contract.stage='STAGE';""".replace('STAGE',stage)
   if stage=='CREDIT_CALLING':setup+="contract.debitAfter=750;contract.debited=250;contract.creditBefore=750;contract.creditAfter=750+model.Payout(contract);"
   setup+="n.capitalKnown=true;n.capital=model.Encode(history);"
   v=partial(setup);v.execute("capitalBytes=T.encode(T.record(c).capital)");begin(v);v.execute("assert(T.encode(T.record(c).capital)==capitalBytes and T.record(c).capitalKnown==true and not s.Status(c).subrecordIsolation.capital);testReload();s=shared.CityProgressionStore;assert(T.encode(T.record(c).capital)==capitalBytes and s.CapitalState(0,c).value.contracts.DISTRICT_CAMPUS.stage=='"+stage+"')")

class Compatibility(unittest.TestCase):
 def test_original_signed_contract_preservation_with_explicit_quote_open(self):
  import test_b246_development as fixture
  import test_b247_restructuring as original
  runtime=fixture.runtime
  def opened():
   v=runtime();v.execute("assert(cap.Request(0,{Action='CAPITAL_OPEN',CityID=source:GetID(),Token='PU06_EXPLICIT_OPEN'}))");return v
  from test_refactor_s7d5 import profile
  with profile(),patch.object(fixture,'runtime',opened):
   original.ContractPreservation('test_signed_capital_and_development_survive_identity_exit_and_settle').test_signed_capital_and_development_survive_identity_exit_and_settle()

if __name__=='__main__':unittest.main()
