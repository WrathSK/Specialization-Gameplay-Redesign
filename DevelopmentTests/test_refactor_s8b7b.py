"""D6/D7 partial reputation: valid config remains usable, raw history never becomes R0."""
from pathlib import Path
from unittest.mock import patch
import ast,json,unittest
from refactor_harness import ROOT,TrackedLua51,legacy_source_observation,measure
from test_refactor_s8b2 import fixture
import test_refactor_s8b3 as history_source
import test_refactor_s8b6 as claim_cases
import test_refactor_s7c as commerce_cases
from test_refactor_s6f import combined

BASE='c589f5b'
SUPERSEDED={
 'test_refactor_s8b6.ClaimIsolation.test_core_claim_receipt_and_unreviewed_Commerce_or_template_failure_stay_strict',
 'test_refactor_s7c.RetainedStore.test_missing_known_or_corrupt_history_not_reconstructed'}


def partial(extra='',level=4):
 v=fixture();v.execute("""
 c=T.fresh(3);T.register(c);T.complete(c,'DISTRICT_COMMERCIAL_HUB');T.governor(4)
 GameConfiguration.GetGameSpeedType=function()return 'GAMESPEED_STANDARD'end;GameInfo.GameSpeeds={GAMESPEED_STANDARD={GameSpeedType='GAMESPEED_STANDARD',CostMultiplier=100}}
 a=shared.InvestmentAction;for i=1,(...)-1 do T.invest(c,88000+i)end
 local n=M.Copy(T.record(c));n.commerce=n.commerce or SPCCommerceModel.New(0);n.commerce.selected={'DISTRICT_CAMPUS'};n.commerce.reputation={version=1,start=0,age=99,cursor=0,state='COUNTING',receipt='UNKNOWN',extension={keep=true}}
 """+extra+"original=M.Copy(n);frozen=T.encode(n);beforeWrites=T.writes();T.propsSet(T.key(c),n);testReload();s=shared.CityProgressionStore;function rawRep()return T.encode(T.record(c).commerce.reputation)end",level);return v


def gold(cold=False):
 v=combined();v.execute("for i=1,20 do T.turn(1);auditCommerce()end;assert(gold()==16);local n=M.Copy(T.record(source));n.commerce.reputation.age=99;rawHistory=T.encode(n.commerce.reputation);T.propsSet(T.key(source),n);local dc=shared.DistrictCompleteness;local speed=GameConfiguration.GetGameSpeedType;T.reload();GameConfiguration.GetGameSpeedType=speed;shared.DistrictCompleteness=dc;shared.NetworkBridge={};SPCFactChanges.New(shared);f=shared.EffectiveFacts;beforeWrites=T.writes()")
 tree=ast.parse((ROOT/'DevelopmentTests/test_refactor_s6f.py').read_text());fn=next(n for n in tree.body if isinstance(n,ast.FunctionDef)and n.name=='combined')
 adapters=next(n.value.args[0].value for n in fn.body if isinstance(n,ast.Expr)and isinstance(n.value,ast.Call)and isinstance(n.value.func,ast.Attribute)and n.value.func.attr=='execute')
 if cold:
  # Keep the native doubles, remove only fixture's automatic first verified audit.
  a=adapters.index('      local v=auditCommerce()');adapters=adapters[:a]
 with legacy_source_observation():v.globals().include('Commerce')
 v.execute(adapters)
 if cold:v.execute("shared.NetworkBridge.CurrentEffectPartners=function()return {validity='UNKNOWN',reason='NETWORK_PENDING'}end;com.Audit({player=0,city=source:GetID()})")
 return v


class Store(unittest.TestCase):
 def test_only_reputation_is_unknown_and_projection_never_exports_bad_archive_or_fake_zero(self):
  v=partial();v.execute("assert(pcall(s.Base,0,c)and T.writes()==beforeWrites and T.encode(T.record(c))==frozen);local state=s.CommerceState(0,c);assert(state.reputationKnown==false and state.value.reputation==nil and state.value.selected[1]=='DISTRICT_CAMPUS');assert(s.Status(c).reputationIsolation and not s.Status(c).subrecordIsolation.commerce);state.value.selected[1]='MUTATE';assert(s.CommerceState(0,c).value.selected[1]=='DISTRICT_CAMPUS');local x=s.InstitutionSummary(0,c);assert(x.known and x.reputationKnown==false and x.reputation==nil)")
 def test_configuration_selection_can_change_but_complete_raw_reputation_and_marker_stay_exact(self):
  for flag in ('true','false','nil'):
   v=partial('n.commerceKnown='+flag+';');v.execute("local raw=rawRep();local old=s.CommerceState(0,c).value;local nextValue=SPCCommerceModel.Select(old,'DISTRICT_HARBOR',true);s.WriteCommerce(0,c,old,nextValue);assert(s.CommerceState(0,c).value.selected[2]=='DISTRICT_HARBOR'and rawRep()==raw and T.record(c).commerceKnown==("+flag+")and T.writes()==beforeWrites+1 and not s.Status(c).subrecordRecovery)")
 def test_write_cannot_supply_reputation_false_zero_or_a_replacement_history(self):
  for value in ('false','{}',"{version=1,start=0,age=0,cursor=0,state='COUNTING',receipt='FAKE'}"):
   v=partial();v.execute("local old=s.CommerceState(0,c).value;local n=SPCCommerceModel.Select(old,'DISTRICT_HARBOR',true);n.reputation="+value+";assert(not pcall(s.WriteCommerce,0,c,old,n));assert(T.writes()==beforeWrites and T.encode(T.record(c))==frozen)")
 def test_partial_only_save_mask_is_active_and_rejects_rep_or_known_marker_change(self):
  for change in ("n.commerce.reputation=nil","n.commerce.reputation.extension.keep=false","n.commerceKnown=true"):
   v=partial('n.commerceKnown=false;');v.execute("local n=M.Copy(T.record(c));n.revision=n.revision+1;"+change+";assert(not saveCandidate(c,n)and T.writes()==beforeWrites and T.encode(T.record(c))==frozen and pcall(s.Base,0,c))")
 def test_projection_old_value_and_candidate_are_bounded_copies_before_comparison(self):
  v=partial();v.execute("local old=s.CommerceState(0,c).value;local nextValue=SPCCommerceModel.Select(old,'DISTRICT_HARBOR',true);local forged=setmetatable({},{__index=old});assert(not pcall(s.WriteCommerce,0,c,forged,nextValue));assert(T.writes()==beforeWrites and T.encode(T.record(c))==frozen)")
 def test_partial_known_marker_is_not_rebuilt_alongside_independently_valid_other_flag(self):
  v=partial("n.commerceKnown=false;n.capitalKnown=false;n.capital=SPCCapitalInvestmentModel.Encode(SPCCapitalInvestmentModel.New());")
  v.execute("assert(T.writes()==beforeWrites+1 and T.record(c).commerceKnown==false and T.record(c).capitalKnown==true);local st=s.Status(c);assert(st.reputationIsolation and #st.subrecordRecovery.fields==1 and st.subrecordRecovery.fields[1].key=='capital');assert(rawRep()==T.encode(original.commerce.reputation))")
 def test_bad_configuration_is_whole_group_isolated_and_other_abilities_continue(self):
  for change in ("n.commerce='BROKEN'","n.commerce.selected='BROKEN'","n.commerce.owner=9"):
   v=partial(change+';');v.execute("assert(pcall(s.Base,0,c)and not pcall(s.CommerceState,0,c)and s.Status(c).subrecordIsolation.commerce and not s.Status(c).reputationIsolation and T.writes()==beforeWrites and T.encode(T.record(c))==frozen);local x=s.InstitutionSummary(0,c);assert(x.known and x.reputationKnown==false and x.reputation==nil)")
 def test_core_and_unreviewed_templates_still_hold_without_guessing(self):
  for change in ("n.schema=99","n.base.token='FORGED'","n.origin.x=12345","n.templates={}"):
   v=partial(change+';');v.execute("assert(not pcall(s.Base,0,c)and T.writes()==beforeWrites and T.encode(T.record(c))==frozen and not s.Status(c).reputationIsolation)")
 def test_ticks_and_first_P4_never_reconstruct_or_advance_bad_reputation(self):
  v=partial(level=3);v.execute("local raw=rawRep();local before=T.writes();T.turn(10);assert(rawRep()==raw and T.writes()==before);T.invest(c,88103);assert(shared.EffectiveFacts.Read(0,c).potential==4 and rawRep()==raw and s.CommerceState(0,c).reputationKnown==false)")
 def test_owner_loss_return_changes_only_original_configuration_not_opaque_reputation(self):
  v=partial('n.commerceKnown=false;');v.execute("local raw=rawRep();local id=c:GetID();s.RegisterExit('Fixture',function()end);T.loss(c,9,900);assert(T.record(c).stage=='HELD_TRANSFER'and T.record(c).commerce.owner==9 and #T.record(c).commerce.selected==0 and rawRep()==raw and T.record(c).commerceKnown==false);c.s.ref.owner=0;c.s.ref.cityID=id;Events.CityTransfered.Fire(0,id,9);assert(T.record(c).stage=='ACTIVE'and s.CommerceState(0,c).value.owner==0 and rawRep()==raw and T.record(c).commerceKnown==false)")
 def test_restructuring_preserves_bad_reputation_and_known_flag_while_clearing_configuration(self):
  v=partial('n.commerceKnown=false;');v.execute("local raw=rawRep();local team={owner=0,id=777,uid='TEAM:777'};s.BeginRestructuring(0,c,team,'PARTIAL_REPUTATION');assert(T.record(c).restructuring.phase=='REALLOCATING'and #T.record(c).commerce.selected==0 and rawRep()==raw and T.record(c).commerceKnown==false);T.turn(5);s.ConfigureRestructuring(0,c,team,'CULTURE',{districtID=601,type='DISTRICT_THEATER',turn=T.now()});Players[0].GetUnits=function()return {FindID=function()return nil end}end;s.ConfirmRestructuringConsumption(0,c,team);assert(s.FinishRestructuring(0,c,team)and rawRep()==raw and T.record(c).commerceKnown==false)")
 def test_healthy_state_and_write_keep_original_copy_work_and_saved_bytes(self):
  values=[]
  for old in (True,False):
   from contextlib import nullcontext
   with (patch.object(history_source,'BASE',BASE)if old else nullcontext()):
    with (history_source.before()if old else nullcontext()):
     v=partial('n.commerce.reputation=nil;');v.execute("local copy=M.Copy;M.Copy=function(...)copies=copies+1;return copy(...)end;copies=0;testReload();s=shared.CityProgressionStore;copies=0;local old=s.CommerceState(0,c).value;readCopies=copies;copies=0;local value=SPCCommerceModel.Select(old,'DISTRICT_HARBOR',true);s.WriteCommerce(0,c,old,value);writeCopies=copies;encoded=T.encode(T.record(c))")
   values.append((v.eval('readCopies'),v.eval('writeCopies'),v.eval('encoded')))
  self.assertEqual(values[0],values[1]);self.assertEqual(values[1][0],2) # fixture GetProperty copies the token once, plus the detached State projection
  measure('S8b7b_healthy_copy_work',{'state_copies':values[1][0],'write_copies':values[1][1],'same_as_B346':True,'same_saved_bytes':True})
 def test_failed_write_uses_full_raw_CAS_and_does_not_publish_sanitized_candidate(self):
  v=partial('n.commerceKnown=false;');v.execute("local raw=rawRep();local old=s.CommerceState(0,c).value;local value=SPCCommerceModel.Select(old,'DISTRICT_HARBOR',true);local key=T.key(c);local set=Game.SetProperty;local calls=0;Game.SetProperty=function(o,k,v)if k==key then calls=calls+1;error('WRITE_UNCERTAIN')end;return set(o,k,v)end;assert(not pcall(s.WriteCommerce,0,c,old,value)and not pcall(s.CommerceState,0,c)and rawRep()==raw and T.record(c).commerceKnown==false and calls==1 and T.writes()==beforeWrites)")


class GoldAndPresentation(unittest.TestCase):
 def test_actual_Store_Commerce_keeps_base_Gold_and_config_writes_without_rewriting_reputation(self):
  v=gold();v.execute("""
  local id=source:GetID();local v=com.views['0:'..id]
  assert(v.stage=='READY'and v.reputationKnown==false and v.reputation.age==nil and v.reputation.effective==0 and gold()==15)
  assert(T.encode(T.record(source).commerce.reputation)==rawHistory and T.writes()==beforeWrites)
  assert(com.Request(0,{Action='COMMERCE_SELECT',CityID=id,Domain='DISTRICT_CAMPUS',Enabled=false,Reference=v.reference,CityToken=v.token,Revision=v.revision,Token='OFF_PARTIAL'}));auditCommerce();assert(gold()==0)
  v=com.views['0:'..id];assert(com.Request(0,{Action='COMMERCE_SELECT',CityID=id,Domain='DISTRICT_CAMPUS',Enabled=true,Reference=v.reference,CityToken=v.token,Revision=v.revision,Token='ON_PARTIAL'}));auditCommerce();assert(gold()==15 and T.encode(T.record(source).commerce.reputation)==rawHistory)
  local writes,changes=T.writes(),com.writes;for i=1,1000 do Events.GameCoreEventPublishComplete.Fire()end;assert(T.writes()==writes and com.writes==changes)
  assert(com.Describe(0,source):find('商业信誉暂不可确认',1,true))
  """)
  measure('S8b7b_actual_Store_Commerce',{'prior_confirmed_gold':16,'confirmed_gold_without_unknown_bonus':15,'configuration_off_on_gold':[0,15],'raw_bad_reputation_unchanged':True,'thousand_idle_writes':0})
 def test_restructuring_unknown_reputation_is_not_displayed_as_confirmed_zero(self):
  v=gold();v.execute("local team={owner=0,id=778,uid='TEAM:778'};shared.CityProgressionStore.BeginRestructuring(0,source,team,'PARTIAL_REPUTATION');com.SourceChanged(0,source:GetID());local v=com.views['0:'..source:GetID()];assert(v.identity=='NONE'and v.reputationKnown==false and v.reputation.age==nil);assert(com.Describe(0,source):find('商业信誉暂不可确认',1,true))")
 def test_actual_cold_PENDING_keeps_installed_total_and_never_calls_it_new_R0_qualification(self):
  v=gold(cold=True);v.execute("local v=com.views['0:'..source:GetID()];assert(gold()==16 and v.stage=='HELD'and v.appliedRetained and not v.canConfigure and v.reputationKnown==false and T.writes()==beforeWrites and T.encode(T.record(source).commerce.reputation)==rawHistory);local n=com.writes;for i=1,1000 do Events.GameCoreEventPublishComplete.Fire()end;assert(com.writes==n and gold()==16)")
 def test_warm_pending_uses_existing_source_samples_and_unknown_R0_clamp(self):
  from test_refactor_s4b import commerce
  v=commerce();v.execute("""
  assert(toggle(2,'DISTRICT_CAMPUS',true));commerceStates[2].reputation={version=1,start=0,cursor=20,age=20,receipt='P4',state='COUNTING'}
  cities[2].active=4;cities[2].potential=4;com.SourceChanged(0,2);assert(ownedGold(cities[2])==16)
  net.CheckEvidence(false);local read=shared.CityProgressionStore.CommerceState
  shared.CityProgressionStore.CommerceState=function(...)local s=SPCCommerceModel.Copy(read(...));s.value.reputation=nil;s.reputationKnown=false;return s end
  local writes=commerceWrites;com.SourceChanged(0,2)
  assert(ownedGold(cities[2])==15 and view(2).stage=='RETAINED'and not view(2).canConfigure and view(2).reputationKnown==false and view(2).reputation.age==nil)
  assert(commerceStates[2].reputation.age==20 and commerceWrites==writes)
  """)
 def test_existing_panel_displays_unknown_flag_without_disabling_other_ready_configuration(self):
  import test_b261_commerce as ui
  with patch.object(ui,'LuaRuntime',TrackedLua51),legacy_source_observation():v=ui.ui()
  v.execute("view.reputationKnown=false;view.reputation={age=12,effective=0,state='COUNTING'};notify();rows.items[1].Root.click();assert(Controls.Reputation.text:find('REPUTATION_UNKNOWN',1,true)and not Controls.Confirm.disabled and #sent==0)")
 def test_partial_summary_metric_is_pending_and_signature_tracks_knownness(self):
  v=partial();v.execute("include('InstitutionPresentation');Locale={Lookup=function(k,...)return k end};local x=s.InstitutionSummary(0,c);local view={specialization='COMMERCE',potential=4,active=4,activeStatus='KNOWN',institutionSummary=x};local t=SPCInstitutionPresentation.Tooltip(4,view);assert(t:find('LOC_SPC_INST_PENDING',1,true)and not t:find('LOC_SPC_INST_NOT_STARTED',1,true)and not t:find('LOC_SPC_INST_REPUTATION_VALUE',1,true));local sig=SPCInstitutionPresentation.Signature(view);x.reputationKnown=true;x.reputation=false;assert(SPCInstitutionPresentation.Signature(view)~=sig and SPCInstitutionPresentation.Tooltip(4,view):find('LOC_SPC_INST_NOT_STARTED',1,true))")


class FrozenBefore(unittest.TestCase):
 def test_previous_Commerce_outside_isolation_and_full_bad_history_assertions_kept_exact(self):
  with patch.object(history_source,'BASE',BASE),history_source.before():
   claim_cases.ClaimIsolation('test_core_claim_receipt_and_unreviewed_Commerce_or_template_failure_stay_strict').test_core_claim_receipt_and_unreviewed_Commerce_or_template_failure_stay_strict()
   commerce_cases.RetainedStore('test_missing_known_or_corrupt_history_not_reconstructed').test_missing_known_or_corrupt_history_not_reconstructed()


def load_tests(loader,standard,pattern):
 selection=json.loads((ROOT/'DevelopmentTests/refactor_selection.json').read_text())
 def flatten(suite):
  for test in suite:
   if isinstance(test,unittest.TestSuite):yield from flatten(test)
   else:yield test
 inherited=unittest.TestSuite()
 for name in selection['stages']['S8b7a']:
  for test in flatten(loader.loadTestsFromName(name)):
   if test.id()not in SUPERSEDED:inherited.addTest(test)
 return unittest.TestSuite([standard,inherited])

if __name__=='__main__':unittest.main()
