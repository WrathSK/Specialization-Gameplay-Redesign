"""Fixed Dialogue/Engineering group isolation, no project replay or history reset."""
from pathlib import Path
from unittest.mock import patch
import json,unittest
from refactor_harness import ROOT,measure
from test_refactor_s8b2 import fixture
import test_refactor_s8b3 as prior
import test_refactor_s8b1 as flags
from test_refactor_s7d1 import profile
import test_dialogue_projects as dialogue_projects
import test_b235_engineering as study_projects

BASE='043dce7'
SUPERSEDED={
 'test_refactor_s8b1.Rebuild.test_missing_payload_bad_payload_other_bad_field_and_bad_base_do_not_repair',
 'test_refactor_s8b3.Tradition.test_other_core_and_unreviewed_ability_errors_still_hold_the_whole_worker'}
OWNERS={'dialogue':('DialogueState','WriteDialogue','dialogueKnown'),'engineering':('EngineeringState','WriteEngineering','engineeringKnown')}


def isolated(owner,extra=''):
 v=fixture();v.execute("local n=seed();n[...]= 'BROKEN';"+extra+"frozen=install(n);testReload();s=shared.CityProgressionStore",owner);return v


class Groups(unittest.TestCase):
 def test_each_bad_group_preserves_original_payload_and_marker_without_disabling_core(self):
  for owner,(getter,writer,flag)in OWNERS.items():
   v=isolated(owner);v.execute("assert(pcall(s.Base,0,ca)and pcall(s.Base,0,cb));assert(not pcall(s[...],0,ca));assert(T.writes()==beforeWrites and T.encode(T.record(ca))==frozen)",getter)
   v.execute("local owner,flag=...;assert(T.record(ca)[flag]==true and T.record(ca)[owner]=='BROKEN');assert(s.Status(ca).subrecordIsolation[owner]);assert(not pcall(s[select(3,...)],0,ca,'BROKEN',{}));assert(T.writes()==beforeWrites and T.encode(T.record(ca))==frozen)",owner,flag,writer)
 def test_group_save_preserves_both_fields_including_missing_or_false_known_marker(self):
  for owner,(_,_,flag)in OWNERS.items():
   for marker in ('false','nil'):
    v=isolated(owner,'n.'+flag+'='+marker+';');v.execute("owner,flag=...;assert(pcall(s.Base,0,ca)and T.writes()==beforeWrites);local n=M.Copy(T.record(ca));n.revision=n.revision+1;n[flag]=true;assert(not saveCandidate(ca,n));assert(T.writes()==beforeWrites and T.encode(T.record(ca))==frozen);n=M.Copy(T.record(ca));n.revision=n.revision+1;assert(saveCandidate(ca,n));assert(T.record(ca)[owner]=='BROKEN'and T.record(ca)[flag]==("+marker+"))",owner,flag)
 def test_valid_payload_only_known_flag_damage_still_rebuilds_once_without_isolation(self):
  for owner,(_,_,flag)in OWNERS.items():
   v=fixture();v.execute("local n=seed();n[...]=false;local before=T.encode(n[select(2,...)]);install(n);testReload();s=shared.CityProgressionStore;assert(pcall(s.Base,0,ca)and T.writes()==beforeWrites+1 and T.record(ca).revision==beforeRevision+1);assert(T.encode(T.record(ca)[select(2,...)])==before and not s.Status(ca).subrecordIsolation[select(2,...)]);assert(#s.Status(ca).subrecordRecovery.fields==1)",flag,owner)
 def test_mixed_valid_marker_repair_and_invalid_group_does_not_publish_bad_group_marker(self):
  for bad,good in (('dialogue','engineering'),('engineering','dialogue'),('dialogue','capital')):
   v=isolated(bad,'n.'+bad+'Known=false;n.'+good+'Known=false;');v.execute("bad,good=...;assert(pcall(s.Base,0,ca)and T.writes()==beforeWrites+1 and T.record(ca).revision==beforeRevision+1);assert(T.record(ca)[bad]=='BROKEN'and T.record(ca)[bad..'Known']==false and T.record(ca)[good..'Known']==true);local recovered=s.Status(ca).subrecordRecovery.fields;assert(#recovered==1 and recovered[1].key==good)",bad,good)
 def test_known_flag_repair_can_coexist_with_prior_Insights_and_Tradition_isolation(self):
  v=fixture();v.execute("local n=seed();n.dialogueKnown=false;n.engineeringKnown=false;n.expeditionInsights='BROKEN';n.researchTradition='BROKEN';install(n);testReload();s=shared.CityProgressionStore;assert(pcall(s.Base,0,ca)and T.writes()==beforeWrites+1);local st=s.Status(ca);assert(st.subrecordIsolation.expeditionInsights and st.subrecordIsolation.researchTradition and not st.subrecordIsolation.dialogue and not st.subrecordIsolation.engineering and #st.subrecordRecovery.fields==2);assert(T.record(ca).expeditionInsights=='BROKEN'and T.record(ca).researchTradition=='BROKEN')")
 def test_four_isolated_groups_preserve_all_original_fields_during_normal_investment_and_ticks(self):
  v=isolated('dialogue',"n.dialogueKnown=false;n.engineering='BROKEN';n.engineeringKnown=nil;n.expeditionInsights='BROKEN';n.researchTradition='BROKEN';")
  v.execute("local original=T.encode({T.record(ca).dialogue,T.record(ca).engineering,T.record(ca).expeditionInsights,T.record(ca).researchTradition});T.invest(ca,99501);T.turn(3);assert(shared.EffectiveFacts.Read(0,ca).potential==2);assert(T.encode({T.record(ca).dialogue,T.record(ca).engineering,T.record(ca).expeditionInsights,T.record(ca).researchTradition})==original and T.record(ca).dialogueKnown==false and T.record(ca).engineeringKnown==nil)")
 def test_other_base_or_unreviewed_history_error_still_blocks_repair_and_isolation(self):
  for bad in ("n.schema=99","n.base.token='FORGED'","n.origin.x=12345","n.binding={}","n.claimTimer={}","n.commerce='BROKEN'","n.capital='BROKEN'","n.development='BROKEN'","n.templates={}"):
   v=isolated('dialogue',bad+';');v.execute("assert(not pcall(s.Base,0,ca)and pcall(s.Base,0,cb)and T.writes()==beforeWrites and T.encode(T.record(ca))==frozen and next(s.Status(ca).subrecordIsolation)==nil)")
 def test_loss_and_return_do_not_try_Cancel_or_replay_invalid_project_payloads(self):
  for owner in OWNERS:
   v=isolated(owner);v.execute("owner=...;local id=ca:GetID();s.RegisterExit('Fixture',function()end);T.loss(ca,9,900);assert(T.record(ca).stage=='HELD_TRANSFER'and T.record(ca)[owner]=='BROKEN');ca.s.ref.owner=0;ca.s.ref.cityID=id;Events.CityTransfered.Fire(0,id,9);assert(T.record(ca).stage=='ACTIVE'and pcall(s.Base,0,ca)and T.record(ca)[owner]=='BROKEN'and s.Status(ca).subrecordIsolation[owner])",owner)
 def test_restructuring_can_complete_while_invalid_project_groups_stay_exact(self):
  v=isolated('dialogue',"n.engineering='BROKEN';");v.execute("for i=1,3 do T.invest(ca,99600+i)end;local team={owner=0,id=777,uid='TEAM:777'};s.BeginRestructuring(0,ca,team,'REST_BAD_PROJECTS');T.turn(5);s.ConfigureRestructuring(0,ca,team,'CULTURE',{districtID=601,type='DISTRICT_THEATER',turn=T.now()});Players[0].GetUnits=function()return {FindID=function()return nil end}end;s.ConfirmRestructuringConsumption(0,ca,team);assert(s.FinishRestructuring(0,ca,team));assert(shared.EffectiveFacts.Read(0,ca).specialization=='CULTURE'and T.record(ca).dialogue=='BROKEN'and T.record(ca).engineering=='BROKEN')")


class Projects(unittest.TestCase):
 def test_actual_Dialogue_isolated_CALLING_keeps_raw_receipt_removes_access_and_never_finishes(self):
  with profile():v=dialogue_projects.game()
  v.execute("""
  begin(c);local n=T.record(c);n.dialogue.pending.stage='CALLING';n.dialogue.pending.reference.cityID=99999
  local raw=T.encode(n.dialogue);T.propsSet(T.key(c),n);local writes=T.writes();reload()
  assert(pcall(shared.CityProgressionStore.Base,0,c)and not pcall(shared.CityProgressionStore.DialogueState,0,c))
  assert(not c.b.present[998]and view(c).stage=='HELD'and T.encode(T.record(c).dialogue)==raw and T.writes()==writes)
  local first=finishes;local sampled=samples;for i=1,3 do endturn();Events.GameCoreEventPublishComplete.Fire()end
  assert(finishes==first and samples==sampled and T.encode(T.record(c).dialogue)==raw and T.writes()==writes)
  """)
 def test_actual_Study_isolated_CALLING_preserves_existing_access_and_never_finishes(self):
  with profile():v=study_projects.study_runtime()
  v.execute("""
  c=S.make();S.begin(c);local n=T.record(c);n.engineering.pending.stage='CALLING';n.engineering.pending.reference.cityID=99999
  local raw=T.encode(n.engineering);T.propsSet(T.key(c),n);local writes=T.writes();assert(c.buildings[9002]);S.reload(c)
  assert(pcall(shared.CityProgressionStore.Base,0,c)and not pcall(shared.CityProgressionStore.EngineeringState,0,c))
  assert(c.buildings[9002]and study.views['0:'..c:GetID()].stage=='HELD'and T.encode(T.record(c).engineering)==raw and T.writes()==writes)
  for i=1,3 do S.endturn()end;assert(S.finishes(c)==0 and T.encode(T.record(c).engineering)==raw and T.writes()==writes)
  """)
  measure('S8b4_actual_isolated_projects',{'owners':2,'new_finish_calls':0,'corrupt_CALLING_replay':False,'Dialogue_access':'existing_withdraw_policy','Study_access':'existing_UNKNOWN_retention_policy'})


class Presentation(unittest.TestCase):
 def test_metrics_are_independent_unknown_and_Industry_IV_does_not_compute_zero_L_boost(self):
  v=isolated('dialogue',"n.engineering='BROKEN';");v.execute("""
  include('InstitutionPresentation');Locale={Lookup=function(k,...)return k end}
  local x=s.InstitutionSummary(0,ca);assert(x.known and x.dialogueKnown==false and x.engineeringKnown==false and x.dialogue==nil and x.engineering==nil and x.insightsKnown)
  local view={specialization='CULTURE',potential=4,active=4,activeStatus='KNOWN',institutionSummary=x}
  local text=SPCInstitutionPresentation.Tooltip(3,view);assert(text:find('LOC_SPC_INST_PENDING',1,true)and not text:find('LOC_SPC_INST_DIALOGUE_VALUE',1,true))
  local sig=SPCInstitutionPresentation.Signature(view);x.dialogueKnown=true;assert(SPCInstitutionPresentation.Signature(view)~=sig);x.dialogueKnown=false
  view.specialization='INDUSTRY';x.templatesKnown=true;x.buildingTemplates=3;x.districtTemplates=2
  text=SPCInstitutionPresentation.Tooltip(4,view);assert(text:find('LOC_SPC_INST_PENDING',1,true)and not text:find('LOC_SPC_INST_ENGINEERING_VALUE',1,true))
  text=SPCInstitutionPresentation.Tooltip(3,view);assert(text:find('LOC_SPC_INST_TEMPLATES_VALUE',1,true)and text:find('LOC_SPC_INST_PENDING',1,true)and not text:find('LOC_SPC_INST_STANDARDIZATION_VALUE',1,true))
  view.active=3;text=SPCInstitutionPresentation.Tooltip(3,view);assert(text:find('LOC_SPC_INST_STANDARDIZATION_VALUE',1,true))
  """)


class FrozenBefore(unittest.TestCase):
 def test_B342_unreviewed_group_scope_matrix_kept_exact(self):
  with patch.object(prior,'BASE',BASE),prior.before():
   prior.Tradition('test_other_core_and_unreviewed_ability_errors_still_hold_the_whole_worker').test_other_core_and_unreviewed_ability_errors_still_hold_the_whole_worker()
 def test_B342_whole_worker_flag_failure_matrix_kept_exact(self):
  with patch.object(prior,'BASE',BASE),prior.before():
   flags.Rebuild('test_missing_payload_bad_payload_other_bad_field_and_bad_base_do_not_repair').test_missing_payload_bad_payload_other_bad_field_and_bad_base_do_not_repair()


def load_tests(loader,standard,pattern):
 selection=json.loads((ROOT/'DevelopmentTests/refactor_selection.json').read_text())
 def flatten(suite):
  for test in suite:
   if isinstance(test,unittest.TestSuite):yield from flatten(test)
   else:yield test
 inherited=unittest.TestSuite()
 for name in selection['stages']['S8b3']:
  for test in flatten(loader.loadTestsFromName(name)):
   if test.id()not in SUPERSEDED:inherited.addTest(test)
 return unittest.TestSuite([standard,inherited])

if __name__=='__main__':unittest.main()
