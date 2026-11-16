"""Template-family unavailability preserves core identity, raw history and independent N."""
from contextlib import nullcontext,contextmanager
from pathlib import Path
from unittest.mock import patch
import json,unittest,subprocess
from hashlib import sha256
from refactor_harness import ROOT,TrackedLua51,Context,legacy_source_observation,measure,SOURCES,executed,completion
from test_refactor_s8b2 import fixture
import test_refactor_s8b3 as history_source
import test_refactor_s8b7b as commerce_cases
import test_refactor_s8a as registry_cases
import test_store_write_boundaries as store_fixture
import test_industry_history as ih

BASE='43818ad'
SUPERSEDED={
 'test_refactor_s8b7b.Store.test_core_and_unreviewed_templates_still_hold_without_guessing',
 'test_refactor_s8a.ValidationRegistry.test_exact_declared_fields_are_detached_and_not_automatic'}


@contextmanager
def before():
 original={ROOT/'Mod'/(n+'.lua'):subprocess.check_output(['git','show',BASE+':Mod/'+n+'.lua'],cwd=ROOT,text=True)for n in ('CityProgressionStore','StoreSubrecords','Standardization','IndustryHistory')}
 read,execute,load=Path.read_text,TrackedLua51.execute,Context.load
 hashes={sha256(s.encode()).hexdigest():'historical/'+BASE+'/'+str(p.relative_to(ROOT))for p,s in original.items()}
 def source(p,*a,**kw):return original[p]if p in original else read(p,*a,**kw)
 def run(vm,s,*a,**kw):
  h=sha256(s.encode()if isinstance(s,str)else s).hexdigest()
  if h in hashes:SOURCES[h]=hashes[h]
  return execute(vm,s,*a,**kw)
 def module(c,name):
  p=ROOT/'Mod'/(name if name.endswith('.lua')else name+'.lua')
  if p not in original:return load(c,name)
  text=original[p];h=sha256(text.encode()).hexdigest();key=hashes[h];executed(key,h)
  try:out=c.lua.execute(text)
  except Exception:completion(key,False);raise
  completion(key,True);return out
 with patch.object(Path,'read_text',source),patch.object(TrackedLua51,'execute',run),patch.object(Context,'load',module),legacy_source_observation():yield


def templates(change='n.templates.revision=99;'):
 v=fixture();v.execute("""
 ca=T.fresh(3);T.register(ca);T.complete(ca,'DISTRICT_INDUSTRIAL_ZONE');a=shared.InvestmentAction
 local n=seed();local token=n.base.token
 n.templateLifecycle={version=1,state='INITIALIZED',reconcilePending=false,districtsKnown=true}
 n.templatesCaptured=true;n.templates={schema=1,initialized=true,uid='STD:'..token,foundation=token,x=ca:GetX(),y=ca:GetY(),revision=2,
 learned={BUILDING_OLD={district='DISTRICT_INDUSTRIAL_ZONE',tier=1,turn=T.now(),evidence='BUILT'}},
 knowledgeVersion=1,districts={version=1,policy='D0045',initialized=true,initializedTurn=T.now(),coverage='FROM_IDENTITY',revision=1,learned={}},extension={keep='raw'}}
 """+change+"frozen=install(n);testReload();s=shared.CityProgressionStore;function family()local n=T.record(ca);return T.encode({n.templateLifecycle,n.templates,n.templatesCaptured})end");return v


def wonders():
 with patch.object(store_fixture,'LuaRuntime',TrackedLua51),legacy_source_observation():return ih.runtime()


class TemplateIsolation(unittest.TestCase):
 def test_bad_ledger_lifecycle_or_anchor_isolate_only_fixed_family_without_any_write(self):
  for change in ("n.templates.revision=99;","n.templateLifecycle='BROKEN';","n.templates.foundation='FORGED';","n.templates.x=12345;","n.templates.learned='BROKEN';"):
   v=templates(change);v.execute("assert(pcall(s.Base,0,ca)and pcall(s.Base,0,cb)and s.Status(ca).subrecordIsolation.templateLifecycle);assert(not pcall(s.ReadTemplates,ca)and T.encode(T.record(ca))==frozen and T.writes()==beforeWrites);assert(s.DialogueState(0,ca).value.total==15 and s.EngineeringState(0,ca).value.L==1 and s.CapitalState(0,ca).value and s.CommerceState(0,ca).value);local x=s.InstitutionSummary(0,ca);assert(x.known and x.templatesKnown==false and x.buildingTemplates==nil and x.districtTemplates==nil)")
  measure('S8b8_template_family',{'fields':3,'partial_owner':True,'native_reconstruction':False,'restore_writes':0,'permanent_verdict':False})
 def test_unassigned_core_invariant_not_hidden_by_mask_on_restore_or_save(self):
  v=fixture();v.execute("c=T.fresh(3);T.register(c);local n=M.Copy(T.record(c));n.templates={};T.propsSet(T.key(c),n);local before=T.writes();testReload();assert(not pcall(shared.CityProgressionStore.Base,0,c)and T.writes()==before and not shared.CityProgressionStore.Status(c).subrecordIsolation.templateLifecycle)")
  v=templates();v.execute("local n=M.Copy(T.record(ca));n.progression='UNASSIGNED';n.base.specialization='NONE';n.base.potential=0;n.base.first=nil;n.investment=nil;n.templateLifecycle=nil;n.revision=n.revision+1;local before=T.writes();assert(not saveCandidate(ca,n)and T.writes()==before and T.encode(T.record(ca))==frozen)")
 def test_complete_bad_family_is_exact_across_investment_revision_and_no_idle_retries(self):
  v=templates('n.templates.revision=99;n.templatesCaptured=false;');v.execute("local raw=family();T.invest(ca,88901);assert(shared.EffectiveFacts.Read(0,ca).potential==2 and family()==raw);local n=M.Copy(T.record(ca));n.revision=n.revision+1;assert(saveCandidate(ca,n)and family()==raw);local w=T.writes();for i=1,1000 do Events.GameCoreEventPublishComplete.Fire()end;assert(T.writes()==w)")
 def test_family_replacement_deletion_marker_change_and_metatable_forgery_rejected(self):
  for change in ("n.templates=nil","n.templateLifecycle=nil","n.templatesCaptured=nil","n.templates.extension.keep='changed'","n.templates=setmetatable({},{__index=n.templates})"):
   v=templates();v.execute("local n=M.Copy(T.record(ca));n.revision=n.revision+1;"+change+";assert(not saveCandidate(ca,n)and T.encode(T.record(ca))==frozen and T.writes()==beforeWrites and pcall(s.Base,0,ca))")
 def test_no_legacy_capture_or_display_ledger_interpretation_under_isolation(self):
  v=templates('n.templates.revision=99;n.templatesCaptured=nil;');v.execute("local get=ca.GetProperty;legacyReads=0;ca.GetProperty=function(c,k)if k==M.Keys.TEMPLATES then legacyReads=legacyReads+1;error('LEGACY_FORBIDDEN')end;return get(c,k)end;shared.Standardization={ValidateHistory=function()error('BAD_HISTORY_MUST_NOT_BE_READ')end};assert(not pcall(s.ReadTemplates,ca)and not pcall(s.WriteTemplates,ca,nil,{}));local x=s.InstitutionSummary(0,ca);assert(x.templatesKnown==false and legacyReads==0 and T.writes()==beforeWrites)")
 def test_saved_valid_ledger_with_missing_capture_marker_cannot_be_overwritten_from_legacy(self):
  v=templates('n.templatesCaptured=nil;');v.execute("local get=ca.GetProperty;legacyReads=0;ca.GetProperty=function(c,k)if k==M.Keys.TEMPLATES then legacyReads=legacyReads+1;return nil end;return get(c,k)end;assert(pcall(s.Base,0,ca)and not pcall(s.ReadTemplates,ca)and T.encode(T.record(ca))==frozen and T.writes()==beforeWrites and legacyReads==0)")
 def test_owner_loss_and_return_keep_template_family_opaque_but_identity_recovers(self):
  v=templates();v.execute("local raw=family();local id=ca:GetID();s.RegisterExit('Fixture',function()end);T.loss(ca,9,900);assert(T.record(ca).stage=='HELD_TRANSFER'and family()==raw);ca.s.ref.owner=0;ca.s.ref.cityID=id;Events.CityTransfered.Fire(0,id,9);assert(T.record(ca).stage=='ACTIVE'and pcall(s.Base,0,ca)and family()==raw and not pcall(s.ReadTemplates,ca))")
 def test_restructuring_into_industry_does_not_mutate_unavailable_lifecycle(self):
  v=templates();v.execute("local raw=family();T.invest(ca,88904);T.invest(ca,88905);local team={owner=0,id=777,uid='TEAM:777'};Players[0].GetUnits=function()return {FindID=function()return nil end}end;for i,kind in ipairs({'CULTURE','INDUSTRY'})do s.BeginRestructuring(0,ca,team,'BAD_TEMPLATES:'..i);T.turn(5);s.ConfigureRestructuring(0,ca,team,kind,{districtID=700+i,type=kind=='CULTURE'and'DISTRICT_THEATER'or'DISTRICT_INDUSTRIAL_ZONE',turn=T.now()});s.ConfirmRestructuringConsumption(0,ca,team);assert(s.FinishRestructuring(0,ca,team)and family()==raw)end;assert(shared.EffectiveFacts.Read(0,ca).specialization=='INDUSTRY')")
 def test_first_completion_and_claim_preserve_unavailable_preexisting_lifecycle(self):
  for claim in (False,True):
   v=fixture();v.execute("c=T.fresh(4);"+("T.ai(c);T.district(c,'DISTRICT_INDUSTRIAL_ZONE',601,true);T.take(c);"if claim else 'T.register(c);')+"local n=M.Copy(T.record(c));n.templateLifecycle={version=1,state='BROKEN',extension='keep'};T.propsSet(T.key(c),n);testReload();s=shared.CityProgressionStore;raw=T.encode(T.record(c).templateLifecycle);assert(pcall(s.Base,0,c))")
   if claim:v.execute("local x=s.ClaimState(0,c);assert(s.ClaimComplete(0,c,{reference=x.reference,token=x.token,kind='INDUSTRY',project='PROJECT_SPC_CLAIM_INDUSTRY',turn=T.now(),districtID=601,type='DISTRICT_INDUSTRIAL_ZONE'}))")
   else:v.execute("T.complete(c,'DISTRICT_INDUSTRIAL_ZONE')")
   v.execute("assert(s.Base(0,c).specialization=='INDUSTRY'and T.encode(T.record(c).templateLifecycle)==raw and s.Status(c).subrecordIsolation.templateLifecycle and not pcall(s.ReadTemplates,c))")
 def test_transient_template_validator_error_preserves_original_and_recovers_on_reload(self):
  v=templates('');v.execute("local validate=M.ValidateTemplates;M.ValidateTemplates=function()error('TEMPORARY_TEMPLATE_READ')end;testReload();s=shared.CityProgressionStore;assert(pcall(s.Base,0,ca)and s.Status(ca).subrecordIsolation.templateLifecycle and T.encode(T.record(ca))==frozen and T.writes()==beforeWrites);M.ValidateTemplates=validate;testReload();s=shared.CityProgressionStore;assert(s.ReadTemplates(ca).learned.BUILDING_OLD and not s.Status(ca).subrecordIsolation.templateLifecycle and T.writes()==beforeWrites)")
 def test_structural_copy_and_core_errors_remain_whole_held(self):
  for change in ("n.schema=99;","n.origin.x=12345;","n.base.token='FORGED';"):
   v=templates(change);v.execute("assert(not pcall(s.Base,0,ca)and T.encode(T.record(ca))==frozen and T.writes()==beforeWrites and not s.Status(ca).subrecordIsolation.templateLifecycle)")
 def test_over_limit_native_read_stays_whole_held_before_any_isolation(self):
  v=templates('');v.execute("local get=Game.GetProperty;local key=T.key(ca);Game.GetProperty=function(o,k)local r=get(o,k);if k==key then r.templates.huge=string.rep('x',70000)end;return r end;testReload();s=shared.CityProgressionStore;assert(not pcall(s.Base,0,ca)and T.writes()==beforeWrites and not s.Status(ca).subrecordIsolation.templateLifecycle);Game.GetProperty=get;testReload();assert(shared.CityProgressionStore.ReadTemplates(ca).learned.BUILDING_OLD)")
 def test_registry_fields_detached_and_inspection_uses_trusted_parent_anchor(self):
  v=templates('');v.execute("local f=SPCStoreSubrecords.Fields('templateLifecycle');assert(#f==3);f[2]='MUTATE';assert(SPCStoreSubrecords.Fields('templateLifecycle')[2]=='templates');local n=M.Copy(T.record(ca));n.templates.foundation='OTHER';n.templates.uid='STD:OTHER';local check=SPCStoreSubrecords.CheckOne('templateLifecycle',n,function()return false end);assert(check.status=='CHECK_FAILED'and not check.permanent)")


class IndependentHistory(unittest.TestCase):
 def test_real_history_adds_current_N_without_E_even_when_template_history_is_isolated(self):
  v=wonders();v.execute("c=H.newIndustry();local n=M.Copy(T.record(c));n.templates.revision=99;T.propsSet(T.key(c),n);frozen=T.encode(n);c.buildings[102]=true;local before=T.writes();H.reload();local s=shared.CityProgressionStore;local x=H.read(c);assert(pcall(s.Base,0,c)and s.Status(c).subrecordIsolation.templateLifecycle and x.N==1 and x.E==0 and T.encode(T.record(c))==frozen and T.writes()==before);assert(not pcall(H.ledger,c)and shared.Standardization.scans==0);local h=shared.IndustryHistory;local r=h.Reconcile;calls=0;h.Reconcile=function(...)calls=calls+1;return r(...)end;for i=1,8 do shared.Standardization.Refresh(0,c:GetID())end;assert(calls==0 and H.read(c).N==1)")
  measure('S8b8_independent_wonder_N',{'actual_Store_Standardization_IndustryHistory':True,'current_N':1,'invented_E':0,'template_record_changes':0,'settled_refresh_reconcile_calls':0})
 def test_same_load_return_uses_confirmed_owner_change_not_stale_ready_marker(self):
  v=wonders();v.execute("c=H.newIndustry();local n=M.Copy(T.record(c));n.templates.revision=99;T.propsSet(T.key(c),n);frozen=T.encode(n.templates);H.reload();local s=shared.CityProgressionStore;assert(not shared.IndustryHistory.NeedsReconcile(c));s.RegisterExit('Fixture',function()end);local id=c:GetID();T.loss(c,3,450);H.wonder(c,3);c.s.ref.owner=0;c.s.ref.cityID=id;Events.CityTransfered.Fire(0,id,3);Events.GameCoreEventPublishComplete.Fire();assert(T.record(c).stage=='ACTIVE'and H.read(c).N==1 and H.read(c).E==0 and T.encode(T.record(c).templates)==frozen and not shared.IndustryHistory.NeedsReconcile(c));local count=0;local r=shared.IndustryHistory.Reconcile;shared.IndustryHistory.Reconcile=function(...)count=count+1;return r(...)end;for i=1,8 do shared.Standardization.Refresh(0,id)end;assert(count==0)")
 def test_industry_reentry_stamp_changes_without_normal_investment_rescans(self):
  v=wonders();v.execute("c=H.newIndustry();local s=shared.CityProgressionStore;local n=M.Copy(T.record(c));n.templates.revision=99;T.propsSet(T.key(c),n);H.reload();s=shared.CityProgressionStore;local raw=T.encode(T.record(c).templates);a=shared.InvestmentAction;T.invest(c,88907);T.invest(c,88908);assert(not shared.IndustryHistory.NeedsReconcile(c));local team={owner=0,id=777,uid='TEAM:777'};Players[0].GetUnits=function()return {FindID=function()return nil end}end;for i,kind in ipairs({'CULTURE','INDUSTRY'})do s.BeginRestructuring(0,c,team,'REENTRY:'..i);T.turn(5);s.ConfigureRestructuring(0,c,team,kind,{districtID=700+i,type=kind=='CULTURE'and'DISTRICT_THEATER'or'DISTRICT_INDUSTRIAL_ZONE',turn=T.now()});s.ConfirmRestructuringConsumption(0,c,team);assert(s.FinishRestructuring(0,c,team))end;c.buildings[102]=true;assert(shared.IndustryHistory.NeedsReconcile(c));shared.Standardization.Refresh(0,c:GetID());assert(H.read(c).N==1 and H.read(c).E==0 and T.encode(T.record(c).templates)==raw and not shared.IndustryHistory.NeedsReconcile(c))")
 def test_unknown_identity_cannot_invoke_independent_reconcile(self):
  v=wonders();v.execute("c=H.newIndustry();local s=shared.CityProgressionStore;local read=s.ReadTemplates;s.ReadTemplates=function()error('TEMPLATES_HISTORY_ISOLATED')end;local f=shared.EffectiveFacts.Read;shared.EffectiveFacts.Read=function()error('IDENTITY_UNKNOWN')end;calls=0;shared.IndustryHistory.Reconcile=function()calls=calls+1 end;shared.Standardization.Refresh(0,c:GetID());assert(calls==0 and shared.Standardization.errors['0:'..c:GetID()]:find('TEMPLATES_HISTORY_ISOLATED',1,true));s.ReadTemplates=read;shared.EffectiveFacts.Read=f")
 def test_healthy_read_order_and_settled_refresh_work_match_exact_B347(self):
  results=[]
  for old in (True,False):
   with before()if old else nullcontext():
    v=wonders()
    v.execute("c=H.newIndustry();order={};local s=shared.CityProgressionStore;local r=s.ReadTemplates;s.ReadTemplates=function(...)order[#order+1]='templates';return r(...)end;local h=M.ValidateTemplates;M.ValidateTemplates=function(...)order[#order+1]='history';return h(...)end;local n=shared.IndustryHistory.NeedsReconcile;shared.IndustryHistory.NeedsReconcile=function(...)order[#order+1]='needs';return n(...)end;local f=shared.EffectiveFacts.Read;shared.EffectiveFacts.Read=function(...)order[#order+1]='facts';return f(...)end;local w=shared.IndustryHistory.Reconcile;shared.IndustryHistory.Reconcile=function(...)order[#order+1]='reconcile';return w(...)end;before=T.writes();shared.Standardization.Refresh(0,c:GetID());observed=table.concat(order,',');bytes=T.encode(T.props());extra=T.writes()-before")
    results.append((v.eval('observed'),v.eval('bytes'),v.eval('extra')))
  self.assertEqual(results[0],results[1]);self.assertEqual(results[1][0],'templates,history,needs');self.assertEqual(results[1][2],0)


class FrozenBefore(unittest.TestCase):
 def test_original_unreviewed_template_scope_and_field_metadata_assertions_preserved(self):
  with before():
   commerce_cases.Store().test_core_and_unreviewed_templates_still_hold_without_guessing()
   registry_cases.ValidationRegistry().test_exact_declared_fields_are_detached_and_not_automatic()


def load_tests(loader,standard,pattern):
 selection=json.loads((ROOT/'DevelopmentTests/refactor_selection.json').read_text())
 def flatten(suite):
  for test in suite:
   if isinstance(test,unittest.TestSuite):yield from flatten(test)
   else:yield test
 inherited=unittest.TestSuite()
 for name in selection['stages']['S8b7b']:
  for test in flatten(loader.loadTestsFromName(name)):
   if test.id()not in SUPERSEDED:inherited.addTest(test)
 return unittest.TestSuite([standard,inherited])

if __name__=='__main__':unittest.main()
