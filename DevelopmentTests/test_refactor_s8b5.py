"""Money-history isolation: opaque contracts are preserved, never credited/replayed/empty."""
from pathlib import Path
from unittest.mock import patch
import json,unittest
from refactor_harness import ROOT,measure
from test_refactor_s8b2 import fixture
import test_refactor_s8b3 as history_source
import test_refactor_s8b1 as flag_cases
import test_refactor_s8b2 as insight_cases
import test_refactor_s8b4 as project_cases
from test_refactor_s6e import Profile
from test_b241_capital import runtime as capital_runtime
from test_refactor_s6f import development

BASE='5701d4a'
SUPERSEDED={
 'test_refactor_s8b4.Groups.test_other_base_or_unreviewed_history_error_still_blocks_repair_and_isolation',
 'test_refactor_s8b2.Isolation.test_other_transient_model_error_is_not_blamed_on_Insights_even_if_leaf_is_bad',
 'test_refactor_s8b1.Rebuild.test_transient_decoder_exception_does_not_write_or_poll_and_fresh_load_recovers',
 'test_refactor_s8b1.Rebuild.test_unprintable_model_failure_keeps_unknown_guard_and_sibling_usable'}
OWNERS={'capital':('CapitalState','WriteCapital','VisitCapital'),'development':('DevelopmentState','WriteDevelopment','VisitDevelopment')}


def isolated(owner,extra=''):
 v=fixture();v.execute("local n=seed();n[...]= 'BROKEN';"+extra+"frozen=install(n);testReload();s=shared.CityProgressionStore",owner);return v


def capital():
 p=Profile();p.setUp()
 try:return capital_runtime()
 finally:p.tearDown()


class Groups(unittest.TestCase):
 def test_each_opaque_history_keeps_core_other_abilities_and_raw_marker_payload(self):
  for owner,(getter,writer,_)in OWNERS.items():
   v=isolated(owner);v.execute("owner,getter,writer=...;assert(pcall(s.Base,0,ca)and pcall(s.Base,0,cb)and s.DialogueState(0,ca).value.total==15);assert(not pcall(s[getter],0,ca)and not pcall(s[writer],0,ca,nil,{}));assert(T.writes()==beforeWrites and T.encode(T.record(ca))==frozen and s.Status(ca).subrecordIsolation[owner])",owner,getter,writer)
 def test_missing_payload_is_not_an_empty_known_history_or_an_empty_visitor_result(self):
  for owner,(_,_,visitor)in OWNERS.items():
   v=isolated(owner,'n.'+owner+'=nil;');v.execute("assert(pcall(s.Base,0,ca));local called=0;assert(not pcall(s[...],0,function()called=called+1 end));assert(called==0 and T.writes()==beforeWrites and T.encode(T.record(ca))==frozen)",visitor)
 def test_save_preserves_all_owned_fields_and_known_flag_cannot_be_repaired_over_bad_payload(self):
  for owner in OWNERS:
   for marker in ('false','nil'):
    v=isolated(owner,'n.'+owner+'Known='+marker+';');v.execute("owner=...;assert(pcall(s.Base,0,ca)and T.writes()==beforeWrites);local n=M.Copy(T.record(ca));n.revision=n.revision+1;n[owner..'Known']=true;assert(not saveCandidate(ca,n));n=M.Copy(T.record(ca));n.revision=n.revision+1;n[owner]=nil;assert(not saveCandidate(ca,n));assert(T.writes()==beforeWrites and T.encode(T.record(ca))==frozen)",owner)
 def test_visitors_report_opaque_group_but_still_visit_independent_healthy_city(self):
  for owner,(_,_,visitor)in OWNERS.items():
   v=fixture();v.execute("owner=...;local n=seed();n[owner]='BROKEN';install(n);local other=M.Copy(T.record(cb));other[owner..'Known']=true;local model=owner=='capital'and SPCCapitalInvestmentModel or SPCDevelopmentInvestmentModel;other[owner]=model.Encode(model.New());T.propsSet(T.key(cb),other);testReload();s=shared.CityProgressionStore;local calls=0;assert(not pcall(s[select(2,...)],0,function(value,reference)assert(reference.token==T.record(cb).base.token);calls=calls+1 end));assert(calls==1 and T.writes()==beforeWrites and T.record(ca)[owner]=='BROKEN')",owner,visitor)
 def test_mixed_good_marker_and_bad_money_group_only_repairs_the_good_owner(self):
  for bad,good in (('capital','development'),('development','capital'),('capital','dialogue')):
   v=isolated(bad,'n.'+bad+'Known=false;n.'+good+'Known=false;');v.execute("bad,good=...;assert(pcall(s.Base,0,ca)and T.writes()==beforeWrites+1);assert(T.record(ca)[bad]=='BROKEN'and T.record(ca)[bad..'Known']==false and T.record(ca)[good..'Known']==true);local st=s.Status(ca);assert(#st.subrecordRecovery.fields==1 and st.subrecordRecovery.fields[1].key==good and st.subrecordIsolation[bad])",bad,good)
 def test_temporary_decoder_error_isolated_without_reset_poll_or_optimistic_known_marker(self):
  for owner in OWNERS:
   v=fixture();v.execute("owner=...;local n=seed();n[owner..'Known']=false;frozen=install(n);model=owner=='capital'and SPCCapitalInvestmentModel or SPCDevelopmentInvestmentModel;local decode=model.Decode;local calls=0;model.Decode=function()calls=calls+1;error(setmetatable({},{__tostring=function()error('FORMAT_UNKNOWN')end}))end;testReload();s=shared.CityProgressionStore;assert(pcall(s.Base,0,ca)and s.Status(ca).subrecordIsolation[owner]and T.writes()==beforeWrites and T.encode(T.record(ca))==frozen);local first=calls;for i=1,1000 do Events.GameCoreEventPublishComplete.Fire()end;assert(calls==first and T.writes()==beforeWrites);model.Decode=decode;testReload();s=shared.CityProgressionStore;assert(pcall(s.Base,0,ca)and not s.Status(ca).subrecordIsolation[owner]and T.writes()==beforeWrites+1)",owner)
 def test_remaining_core_and_unreviewed_history_errors_still_hold_everything(self):
  for bad in ("n.schema=99","n.base.token='FORGED'","n.origin.x=12345","n.binding={}","n.claimTimer={}","n.commerce='BROKEN'","n.templates={}"):
   v=isolated('capital',bad+';');v.execute("assert(not pcall(s.Base,0,ca)and pcall(s.Base,0,cb)and T.writes()==beforeWrites and T.encode(T.record(ca))==frozen and next(s.Status(ca).subrecordIsolation)==nil)")
 def test_loss_return_and_restructuring_preserve_invalid_money_histories_without_termination_or_reset(self):
  v=isolated('capital',"n.development='BROKEN';");v.execute("""
  for i=1,3 do T.invest(ca,99700+i)end;local id=ca:GetID();s.RegisterExit('Fixture',function()end)
  T.loss(ca,9,900);assert(T.record(ca).stage=='HELD_TRANSFER'and T.record(ca).capital=='BROKEN'and T.record(ca).development=='BROKEN')
  ca.s.ref.owner=0;ca.s.ref.cityID=id;Events.CityTransfered.Fire(0,id,9);assert(T.record(ca).stage=='ACTIVE')
  local team={owner=0,id=777,uid='TEAM:777'};s.BeginRestructuring(0,ca,team,'REST_OPAQUE_MONEY');T.turn(5)
  s.ConfigureRestructuring(0,ca,team,'CULTURE',{districtID=601,type='DISTRICT_THEATER',turn=T.now()})
  Players[0].GetUnits=function()return {FindID=function()return nil end}end;s.ConfirmRestructuringConsumption(0,ca,team);assert(s.FinishRestructuring(0,ca,team))
  assert(shared.EffectiveFacts.Read(0,ca).specialization=='CULTURE'and T.record(ca).capital=='BROKEN'and T.record(ca).development=='BROKEN')
  """)


class NativeOperations(unittest.TestCase):
 def test_actual_Capital_corrupt_CALLING_does_not_debit_credit_or_roll_again(self):
  for stage in ('DEBIT_CALLING','CREDIT_CALLING'):
   v=capital();v.execute("""
   assert(C.confirm());local n=M.Copy(T.record(source));local value=C.model.Decode(n.capital);local contract=value.contracts.DISTRICT_CAMPUS
   contract.stage=...;if contract.stage=='CREDIT_CALLING'then contract.creditBefore=balance;contract.creditAfter=balance+C.model.Payout(contract)else contract.debitAfter=nil;contract.debited=nil end
   contract.source.token='FORGED_SOURCE';n.capital=C.model.Encode(value);local original=T.encode(n.capital);T.propsSet(T.key(source),n)
   local key=T.key(source);local setter=Game.SetProperty;local changes=0;Game.SetProperty=function(o,k,value)if k==key and T.encode(value.capital)~=T.encode(Game:GetProperty(k).capital)then changes=changes+1 end;return setter(o,k,value)end
   local money,random,writes=moneyCalls,rolls,T.writes();C.reload();assert(T.writes()==writes);assert(pcall(shared.CityProgressionStore.Base,0,source)and not pcall(shared.CityProgressionStore.CapitalState,0,source))
   cap.Reconcile(0);T.turn(20);cap.Reconcile(0);assert(not C.confirm())
   assert(moneyCalls==money and rolls==random and changes==0 and T.encode(T.record(source).capital)==original)
   """,stage)
 def test_actual_Capital_healthy_city_can_sign_after_other_city_history_is_opaque(self):
  v=capital();v.execute("local n=M.Copy(T.record(source));n.capital='BROKEN';n.capitalKnown=true;T.propsSet(T.key(source),n);local net,dc=shared.NetworkBridge,shared.DistrictCompleteness;C.reload();shared.NetworkBridge=net;shared.DistrictCompleteness=dc;cap.Refresh(0,other:GetID());local before=moneyCalls;assert(C.confirm(nil,'STABLE','HEALTHY_SOURCE',other)and moneyCalls==before+1 and T.record(source).capital=='BROKEN')")
 def test_actual_Development_opaque_occupancy_blocks_new_signing_and_never_repeats_debit(self):
  v=development();v.execute("""
  assert(sign());local n=M.Copy(T.record(source));local model=SPCDevelopmentInvestmentModel;local value=model.Decode(n.development)
  for _,contract in pairs(value.contracts)do contract.stage='DEBIT_CALLING';contract.debitAfter=nil;contract.debited=nil;contract.source.token='FORGED_SOURCE'end
  n.development=model.Encode(value);local original=T.encode(n.development);T.invest(other,99801);T.propsSet(T.key(source),n)
  local key=T.key(source);local setter=Game.SetProperty;local changes=0;Game.SetProperty=function(o,k,value)if k==key and T.encode(value.development)~=T.encode(Game:GetProperty(k).development)then changes=changes+1 end;return setter(o,k,value)end
  local money,writes=moneyCalls,T.writes();reload();assert(T.writes()==writes);assert(pcall(shared.CityProgressionStore.Base,0,source)and not pcall(shared.CityProgressionStore.DevelopmentState,0,source))
  dev.Reconcile(0);open();assert(not view().canSign and not sign());open(other);assert(pcall(shared.CityProgressionStore.DevelopmentState,0,other)and shared.EffectiveFacts.Read(0,other).potential==4);assert(view(other).available and view(other).stage=='HELD'and not view(other).canSign and not sign(other));T.turn(3);dev.Reconcile(0)
  assert(moneyCalls==money and changes==0 and T.encode(T.record(source).development)==original)
  """)
  measure('S8b5_actual_opaque_money',{'native_operations_replayed':0,'healthy_Capital_source':'independent_signing','Development_new_signing':'held_by_existing_global_occupancy_UNKNOWN','raw_contracts_preserved':True})


class FrozenBefore(unittest.TestCase):
 def test_prior_unreviewed_money_scope_matrices_kept_exact(self):
  with patch.object(history_source,'BASE',BASE),history_source.before():
   project_cases.Groups('test_other_base_or_unreviewed_history_error_still_blocks_repair_and_isolation').test_other_base_or_unreviewed_history_error_still_blocks_repair_and_isolation()
   insight_cases.Isolation('test_other_transient_model_error_is_not_blamed_on_Insights_even_if_leaf_is_bad').test_other_transient_model_error_is_not_blamed_on_Insights_even_if_leaf_is_bad()
   flag_cases.Rebuild('test_transient_decoder_exception_does_not_write_or_poll_and_fresh_load_recovers').test_transient_decoder_exception_does_not_write_or_poll_and_fresh_load_recovers()
   flag_cases.Rebuild('test_unprintable_model_failure_keeps_unknown_guard_and_sibling_usable').test_unprintable_model_failure_keeps_unknown_guard_and_sibling_usable()


def load_tests(loader,standard,pattern):
 selection=json.loads((ROOT/'DevelopmentTests/refactor_selection.json').read_text())
 def flatten(suite):
  for test in suite:
   if isinstance(test,unittest.TestSuite):yield from flatten(test)
   else:yield test
 inherited=unittest.TestSuite()
 for name in selection['stages']['S8b4']:
  for test in flatten(loader.loadTestsFromName(name)):
   if test.id()not in SUPERSEDED:inherited.addTest(test)
 return unittest.TestSuite([standard,inherited])

if __name__=='__main__':unittest.main()
