"""D7 redundant template metadata proof; no history reconstruction or zero reset."""
from contextlib import contextmanager
from pathlib import Path
from unittest.mock import patch
import json,unittest
from refactor_harness import ROOT,measure
from test_refactor_s8b8 import templates,wonders
import test_refactor_s8b8 as prior
from test_refactor_s8b2 import BAD

BASE='6471b6d'
SUPERSEDED={
 'test_refactor_s8b8.TemplateIsolation.test_bad_ledger_lifecycle_or_anchor_isolate_only_fixed_family_without_any_write',
 'test_refactor_s8b8.TemplateIsolation.test_saved_valid_ledger_with_missing_capture_marker_cannot_be_overwritten_from_legacy'}

@contextmanager
def before():
 with patch.object(prior,'BASE',BASE),prior.before():yield


class Metadata(unittest.TestCase):
 def test_complete_typed_ledger_proves_only_broken_metadata_with_one_restore_CAS(self):
  for change in ("n.templateLifecycle=nil;","n.templateLifecycle='BROKEN';","n.templateLifecycle.state='UNKNOWN';","n.templateLifecycle.reconcilePending=nil;","n.templateLifecycle.districtsKnown='BAD';"):
   v=templates(change);v.execute("local r=T.record(ca);assert(pcall(s.Base,0,ca)and r.templatesCaptured==true and r.templateLifecycle.version==1 and r.templateLifecycle.state=='INITIALIZED'and r.templateLifecycle.reconcilePending and r.templateLifecycle.districtsKnown==true);assert(T.writes()==beforeWrites+1 and r.revision==beforeRevision+1 and not s.Status(ca).subrecordIsolation.templateLifecycle);assert(s.Status(ca).subrecordRecovery.kind=='PROVEN_METADATA_REBUILT');local old=T.encode(r.templates);local w=T.writes();testReload();s=shared.CityProgressionStore;assert(T.writes()==w and T.encode(T.record(ca).templates)==old and not s.Status(ca).subrecordRecovery)")
  measure('S8b9_template_metadata_proof',{'authoritative_saved_ledger':'typed building+district receipts','history_rebuilt':False,'restore_CAS':1,'second_restore_CAS':0,'permanent_irrecoverability_claim':False})
 def test_capture_only_missing_false_or_wrong_type_preserves_valid_lifecycle_and_ledger(self):
  for flag in ('nil','false',"'WRONG'",'{}'):
   v=templates('n.templatesCaptured='+flag+';');v.execute("local r=T.record(ca);assert(r.templatesCaptured==true and r.templateLifecycle.reconcilePending==false and T.writes()==beforeWrites+1);assert(s.ReadTemplates(ca).learned.BUILDING_OLD and not s.Status(ca).subrecordIsolation.templateLifecycle and #s.Status(ca).subrecordRecovery.fields==1);local w=T.writes();testReload();assert(T.writes()==w)")
 def test_ledger_bytes_extensions_and_current_catalog_independence_are_preserved(self):
  v=templates("n.templateLifecycle.state='UNKNOWN';n.templateLifecycle.extension={keep=42};savedLedger=T.encode(n.templates);P.Info=function()error('CURRENT_CATALOG_FORBIDDEN')end;")
  v.execute("assert(T.encode(T.record(ca).templates)==savedLedger and T.record(ca).templateLifecycle.extension.keep==42 and T.writes()==beforeWrites+1 and s.ReadTemplates(ca).learned.BUILDING_OLD)")
 def test_known_and_template_repair_merge_without_overwriting_isolated_sibling(self):
  v=templates("n.templatesCaptured=nil;n.capitalKnown=false;n.expeditionInsights="+BAD+";savedLedger=T.encode(n.templates);rawInsights=T.encode(n.expeditionInsights);")
  v.execute("local r=T.record(ca);assert(r.templatesCaptured and r.capitalKnown and r.templateLifecycle.reconcilePending==false and T.encode(r.templates)==savedLedger and T.encode(r.expeditionInsights)==rawInsights);assert(T.writes()==beforeWrites+1 and #s.Status(ca).subrecordRecovery.fields==2 and s.Status(ca).subrecordIsolation.expeditionInsights)")
 def test_invalid_ledger_or_explicit_unknown_subversion_never_supplies_proof(self):
  for change in ("n.templates=nil;","n.templates.revision=99;","n.templates.foundation='FORGED';","n.templates.x=12345;","n.templates.knowledgeVersion=2;","n.templates.districts=nil;","n.templateLifecycle.version=2;"):
   v=templates("n.templateLifecycle.state='UNKNOWN';n.templatesCaptured=nil;"+change)
   v.execute("assert(pcall(s.Base,0,ca)and not pcall(s.ReadTemplates,ca)and T.encode(T.record(ca))==frozen and T.writes()==beforeWrites and not s.Status(ca).subrecordRecovery)")
 def test_old_building_only_ledger_is_not_a_complete_typed_history_proof(self):
  v=templates("n.templateLifecycle=nil;n.templatesCaptured=nil;n.templates.knowledgeVersion=nil;n.templates.districts=nil;")
  v.execute("assert(pcall(s.Base,0,ca)and not pcall(s.ReadTemplates,ca)and T.encode(T.record(ca))==frozen and T.writes()==beforeWrites)")
 def test_no_industry_or_invalid_core_prevents_metadata_publication(self):
  for change in ("n.base.specialization='RESEARCH';n.base.first.type='DISTRICT_CAMPUS';","n.schema=99;","n.base.token='FORGED';","n.origin.x=12345;"):
   v=templates("n.templateLifecycle.state='UNKNOWN';n.templatesCaptured=nil;"+change)
   v.execute("assert(T.encode(T.record(ca))==frozen and T.writes()==beforeWrites and not s.Status(ca).subrecordRecovery)")
 def test_legal_metadata_with_temporary_validator_failure_is_not_rewritten(self):
  v=templates('');v.execute("local validate=M.ValidateTemplates;M.ValidateTemplates=function()error('TEMPORARY_TEMPLATE_VALIDATOR')end;testReload();s=shared.CityProgressionStore;assert(pcall(s.Base,0,ca)and s.Status(ca).subrecordIsolation.templateLifecycle and T.encode(T.record(ca))==frozen and T.writes()==beforeWrites and not s.Status(ca).subrecordRecovery);M.ValidateTemplates=validate;testReload();assert(T.writes()==beforeWrites and shared.CityProgressionStore.ReadTemplates(ca).learned.BUILDING_OLD)")
 def test_bad_metadata_validator_exception_preserves_all_original_until_proof_recovers(self):
  v=templates("n.templateLifecycle.state='UNKNOWN';local validate=M.ValidateTemplates;M.ValidateTemplates=function()error('TEMPORARY_TEMPLATE_VALIDATOR')end;restoreValidator=validate;")
  v.execute("assert(T.encode(T.record(ca))==frozen and T.writes()==beforeWrites and not s.Status(ca).subrecordRecovery);M.ValidateTemplates=restoreValidator;testReload();s=shared.CityProgressionStore;assert(s.ReadTemplates(ca).learned.BUILDING_OLD and T.writes()==beforeWrites+1 and s.Status(ca).subrecordRecovery)")
 def test_transient_second_check_does_not_report_rejected_template_candidate_as_applied(self):
  v=templates("n.templatesCaptured=nil;n.capitalKnown=false;local validate=M.ValidateTemplates;validationCalls=0;M.ValidateTemplates=function(...)validationCalls=validationCalls+1;if validationCalls==2 then error('TRANSIENT_AFTER_CANDIDATE')end;return validate(...)end;")
  v.execute("local r=T.record(ca);local st=s.Status(ca);assert(validationCalls==2 and T.writes()==beforeWrites+1 and r.capitalKnown==true and r.templatesCaptured==nil and st.subrecordIsolation.templateLifecycle and st.subrecordRecovery.kind=='KNOWN_FLAGS_REBUILT'and #st.subrecordRecovery.fields==1 and st.subrecordRecovery.fields[1].field=='capitalKnown')")
 def test_setter_and_readback_failures_never_publish_success_or_retry(self):
  for mode in ('DROP','THROW_BEFORE','THROW_AFTER'):
   v=templates('')
   v.execute("local n=M.Copy(T.record(ca));n.templatesCaptured=nil;T.propsSet(T.key(ca),n);frozen=T.encode(n);local set=Game.SetProperty;mode=...;attempts=0;local key=T.key(ca);Game.SetProperty=function(o,k,value)if k==key then attempts=attempts+1;if mode=='DROP'then return elseif mode=='THROW_BEFORE'then error('SET_UNKNOWN')end;set(o,k,value);error('SET_UNKNOWN_AFTER')end;return set(o,k,value)end;local w=T.writes();testReload();s=shared.CityProgressionStore;assert(not pcall(s.Base,0,ca)and not s.Status(ca).subrecordRecovery and attempts==1);for i=1,1000 do Events.GameCoreEventPublishComplete.Fire()end;assert(attempts==1)",mode)
 def test_unrepresentable_revision_prevents_recovery_write(self):
  v=templates("n.templatesCaptured=nil;n.revision=9007199254740992;")
  v.execute("assert(not pcall(s.Base,0,ca)and T.writes()==beforeWrites and T.encode(T.record(ca))==frozen and not s.Status(ca).subrecordRecovery)")
 def test_full_industry_start_reconciles_pending_separately_without_rebuilding_history(self):
  v=wonders();v.execute("c=H.newIndustry();local n=M.Copy(T.record(c));n.templateLifecycle.state='UNKNOWN';T.propsSet(T.key(c),n);local before=T.writes();local ledger=T.encode(n.templates);H.reload();assert(T.writes()==before+2 and T.encode(T.record(c).templates)==ledger and not T.record(c).templateLifecycle.reconcilePending and H.ledger(c).learned.BUILDING_A and H.read(c).E==0)")


class FrozenBefore(unittest.TestCase):
 def test_previous_raw_preservation_and_no_capture_assertions_remain_exact_on_B349(self):
  with before():
   prior.TemplateIsolation().test_bad_ledger_lifecycle_or_anchor_isolate_only_fixed_family_without_any_write()
   prior.TemplateIsolation().test_saved_valid_ledger_with_missing_capture_marker_cannot_be_overwritten_from_legacy()


def load_tests(loader,standard,pattern):
 selection=json.loads((ROOT/'DevelopmentTests/refactor_selection.json').read_text())
 def flatten(suite):
  for test in suite:
   if isinstance(test,unittest.TestSuite):yield from flatten(test)
   else:yield test
 inherited=unittest.TestSuite()
 for name in selection['stages']['S9a1']:
  for test in flatten(loader.loadTestsFromName(name)):
   if test.id()not in SUPERSEDED:inherited.addTest(test)
 return unittest.TestSuite([standard,inherited])

if __name__=='__main__':unittest.main()
