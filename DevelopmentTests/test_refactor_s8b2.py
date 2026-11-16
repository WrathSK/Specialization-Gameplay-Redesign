"""Insights-first D7 isolation: preserve invalid leaf; full base and CAS remain strict."""
from pathlib import Path
from unittest.mock import patch
import json,unittest
from refactor_harness import ROOT,measure
from test_refactor_s7f import actual_store
from test_refactor_s8b1 import SETUP

BAD="{version=1,records={WRONG={arbitrary='preserve',nested={extra=7}}},unknownExtension={a='keep'}}"

def fixture():
 p=ROOT/'Mod/CityProgressionStore.lua';read=Path.read_text
 source=read(p);marker=' restore() -- before Binding/Journal/Flow/Investment register load callbacks'
 assert source.count(marker)==1
 source=source.replace(marker,' __s8_save=__s8_save or {};__s8_save[storage]=save;'+marker)
 with patch.object(Path,'read_text',lambda f,*a,**kw:source if f==p else read(f,*a,**kw)):
  v=actual_store();v.execute(SETUP)
  v.execute("function saveCandidate(c,n)return pcall(__s8_save[T.storage(c)],n)end")
  # Reload stays inside this fixed test-only private-save seam.
  reload=v.eval('T.reload')
  def reboot():
   with patch.object(Path,'read_text',lambda f,*a,**kw:source if f==p else read(f,*a,**kw)):return reload()
  v.globals().testReload=reboot
 return v


def isolated(change=''):
 v=fixture();v.execute("local n=seed();n.expeditionInsights="+BAD+';'+(change+';'if change else '')+"frozen=install(n);testReload();s=shared.CityProgressionStore");return v


class Isolation(unittest.TestCase):
 def test_one_bad_leaf_keeps_core_and_other_abilities_usable_without_any_repair_write(self):
  v=isolated();v.execute("""
  assert(pcall(s.Base,0,ca)and pcall(s.Base,0,cb)and T.writes()==beforeWrites and T.encode(T.record(ca))==frozen)
  assert(s.DialogueState(0,ca).value.total==15 and s.EngineeringState(0,ca).value.L==1)
  assert(s.CapitalState(0,ca).value and s.DevelopmentState(0,ca).value and s.CommerceState(0,ca).value)
  local status=s.Status(ca).subrecordIsolation.expeditionInsights
  assert(status.state=='ISOLATED'and status.status=='CHECK_FAILED'and type(status.reason)=='string'and #status.reason<=180)
  assert(not status.records and not status.permanent)
  status.reason='MUTATE';assert(s.Status(ca).subrecordIsolation.expeditionInsights.reason~='MUTATE')
  """)
  measure('S8b2_Insights_isolation',{'invalid_leaf_preserved':True,'base_and_other_abilities_usable':True,'load_property_writes':0,'permanent_corruption_or_reset_claim':False})
 def test_getter_and_first_success_writer_reject_isolation_never_empty_or_success(self):
  v=isolated();v.execute("""
  assert(not pcall(s.ExpeditionInsights,0,ca));local before=T.encode(T.record(ca));local writes=T.writes()
  assert(not pcall(s.AddExpeditionInsight,0,ca,'CIVILIZATION_EGYPT','PEOPLE',5))
  assert(T.encode(T.record(ca))==before and T.writes()==writes and pcall(s.Base,0,ca))
  """)
 def test_save_rejects_change_deletion_or_unknown_extension_change_before_root_publication(self):
  for mutation in ("n.expeditionInsights=nil","n.expeditionInsights={version=1,records={}}","n.expeditionInsights.records.WRONG.nested.extra=8","n.expeditionInsights.unknownExtension.a='changed'","n.expeditionInsights.unknownExtension.newField=false"):
   v=isolated();v.execute("local n=M.Copy(T.record(ca));n.revision=n.revision+1;"+mutation+";assert(not saveCandidate(ca,n));assert(T.writes()==beforeWrites and T.encode(T.record(ca))==frozen and pcall(s.Base,0,ca))")
 def test_metatable_fallback_cannot_forge_preservation_of_an_empty_replacement(self):
  v=isolated();v.execute("local n=M.Copy(T.record(ca));local original=n.expeditionInsights;n.expeditionInsights=setmetatable({},{__index=original});n.revision=n.revision+1;assert(not saveCandidate(ca,n));assert(T.writes()==beforeWrites and T.encode(T.record(ca))==frozen and pcall(s.Base,0,ca))")
 def test_ordinary_investment_ticks_and_explicit_revision_preserve_complete_invalid_leaf(self):
  v=isolated();v.execute("""
  local original=T.encode(T.record(ca).expeditionInsights)
  T.invest(ca,9991);assert(shared.EffectiveFacts.Read(0,ca).potential==2)
  T.turn(2);local n=M.Copy(T.record(ca));n.revision=n.revision+1;assert(saveCandidate(ca,n))
  assert(T.encode(T.record(ca).expeditionInsights)==original and s.Status(ca).subrecordIsolation.expeditionInsights)
  local writes=T.writes();for i=1,1000 do Events.GameCoreEventPublishComplete.Fire()end;assert(T.writes()==writes)
  """)
 def test_loss_and_return_keep_same_city_history_isolated_without_reset(self):
  v=isolated();v.execute("""
  local original=T.encode(T.record(ca).expeditionInsights);local id=ca:GetID();s.RegisterExit('Fixture',function()end)
  T.loss(ca,9,900);assert(T.encode(T.record(ca).expeditionInsights)==original and not pcall(s.Base,9,ca))
  ca.s.ref.owner=0;ca.s.ref.cityID=id;Events.CityTransfered.Fire(0,id,9)
  assert(T.record(ca).stage=='ACTIVE'and pcall(s.Base,0,ca)and T.encode(T.record(ca).expeditionInsights)==original)
  assert(not pcall(s.ExpeditionInsights,0,ca)and s.Status(ca).subrecordIsolation.expeditionInsights)
  """)
 def test_core_or_second_bad_ability_stays_wholly_held_and_original_unchanged(self):
  for change in ("n.schema=99","n.revision=0","n.origin.x=12345","n.base.token='FORGED'","n.binding={}","n.base.first={}","n.current={}","n.loss={}","n.restructuring={}","n.researchTradition='BROKEN'","n.dialogueKnown=false","n.claimTimer={}"):
   v=isolated(change);v.execute("assert(not pcall(s.Base,0,ca)and pcall(s.Base,0,cb)and T.writes()==beforeWrites and T.encode(T.record(ca))==frozen and not s.Status(ca).subrecordIsolation.expeditionInsights)")
 def test_read_copy_cycle_unsupported_type_and_limit_failures_never_isolate_or_reset(self):
  for bad in ('READ','CYCLE','TYPE','LIMIT'):
   v=fixture();v.execute("""
   local n=seed();n.expeditionInsights={version=1,records={}};frozen=install(n);mode=...
   local key=T.key(ca);local get=Game.GetProperty
   Game.GetProperty=function(o,k)
    if k==key then
     if mode=='READ'then error('NATIVE_TEMPORARILY_UNAVAILABLE')end
     local r=get(o,k)
     if mode=='CYCLE'then r.expeditionInsights.self=r.expeditionInsights
     elseif mode=='TYPE'then r.expeditionInsights.fn=function()end
     else r.expeditionInsights.huge=string.rep('x',70000)end
     return r
    end
    return get(o,k)
   end
   testReload();local st=shared.CityProgressionStore
   assert(not pcall(st.Base,0,ca)and pcall(st.Base,0,cb)and T.writes()==beforeWrites and T.encode(T.record(ca))==frozen)
   assert(not st.Status(ca).subrecordIsolation.expeditionInsights)
   Game.GetProperty=get;testReload();assert(pcall(shared.CityProgressionStore.Base,0,ca)and T.writes()==beforeWrites)
   """,bad)
 def test_other_transient_model_error_is_not_blamed_on_Insights_even_if_leaf_is_bad(self):
  v=fixture();v.execute("""
  local n=seed();n.expeditionInsights="""+BAD+""";frozen=install(n)
  local validate=SPCCapitalInvestmentModel.Decode
  SPCCapitalInvestmentModel.Decode=function()error('TEMPORARILY_UNAVAILABLE')end
  testReload();local st=shared.CityProgressionStore
  assert(not pcall(st.Base,0,ca)and not st.Status(ca).subrecordIsolation.expeditionInsights and T.writes()==beforeWrites)
  SPCCapitalInvestmentModel.Decode=validate;testReload();st=shared.CityProgressionStore
  assert(pcall(st.Base,0,ca)and st.Status(ca).subrecordIsolation.expeditionInsights and T.writes()==beforeWrites and T.encode(T.record(ca))==frozen)
  """)
 def test_transient_Insights_check_exception_is_not_a_permanent_fault_or_reset(self):
  v=fixture();v.execute("local n=seed();n.expeditionInsights="+BAD+";frozen=install(n);local check=SPCStoreSubrecords.CheckOne;SPCStoreSubrecords.CheckOne=function()error('CHECK_UNAVAILABLE')end;testReload();local st=shared.CityProgressionStore;assert(not pcall(st.Base,0,ca)and T.writes()==beforeWrites and not st.Status(ca).subrecordIsolation.expeditionInsights);SPCStoreSubrecords.CheckOne=check;testReload();assert(pcall(shared.CityProgressionStore.Base,0,ca)and T.writes()==beforeWrites)")
 def test_failed_CAS_or_uncertain_setter_does_not_publish_or_overwrite_other_observed_bytes(self):
  for mode in ('PREWRITE','DROP','THROW_BEFORE','THROW_AFTER'):
   v=isolated();v.execute("""
   local n=M.Copy(T.record(ca));n.revision=n.revision+1;local key=T.key(ca);mode=...
   local get,set=Game.GetProperty,Game.SetProperty;attempts=0
   if mode=='PREWRITE'then local other=M.Copy(n);other.expeditionInsights.unknownExtension.a='external';T.propsSet(key,other)
   else Game.SetProperty=function(o,k,value)
    if k~=key then return set(o,k,value)end;attempts=attempts+1
    if mode=='DROP'then return end
    if mode=='THROW_BEFORE'then error('WRITE_UNKNOWN')end
    set(o,k,value);error('WRITE_UNKNOWN_AFTER')
   end end
   assert(not saveCandidate(ca,n)and not pcall(s.Base,0,ca))
   if mode=='PREWRITE'then assert(attempts==0 and T.record(ca).expeditionInsights.unknownExtension.a=='external')
   else assert(attempts==1 and T.encode(T.record(ca).expeditionInsights)==T.encode(n.expeditionInsights))end
   local count=attempts;for i=1,1000 do Events.GameCoreEventPublishComplete.Fire()end;assert(attempts==count)
   """,mode)
 def test_reload_reassesses_actual_record_without_preserving_stale_sidecar_or_writing(self):
  v=isolated();v.execute("""
  local n=M.Copy(T.record(ca));n.expeditionInsights={version=1,records={['CIVILIZATION_EGYPT:PEOPLE']={civ='CIVILIZATION_EGYPT',category='PEOPLE',turn=5}}};T.propsSet(T.key(ca),n)
  -- Test-only replacement stands for externally supplied authority, not a production repair API.
  testReload();s=shared.CityProgressionStore
  assert(s.ExpeditionInsights(0,ca)['CIVILIZATION_EGYPT:PEOPLE']and not s.Status(ca).subrecordIsolation.expeditionInsights and T.writes()==beforeWrites)
  """)
 def test_healthy_nil_valid_archive_and_rejected_new_invalid_input_do_not_enter_isolation(self):
  for mode in ('NIL','VALID'):
   v=fixture();v.execute("""
   local n=seed();if ...=='VALID'then n.expeditionInsights={version=1,records={['CIVILIZATION_EGYPT:PEOPLE']={civ='CIVILIZATION_EGYPT',category='PEOPLE',turn=5}}}end
   install(n);testReload();s=shared.CityProgressionStore;assert(pcall(s.Base,0,ca)and not s.Status(ca).subrecordIsolation.expeditionInsights and T.writes()==beforeWrites)
   local before=T.encode(T.record(ca));assert(not pcall(s.AddExpeditionInsight,0,ca,'BAD','PEOPLE',5));assert(T.encode(T.record(ca))==before and T.writes()==beforeWrites and not s.Status(ca).subrecordIsolation.expeditionInsights)
   assert(s.AddExpeditionInsight(0,ca,'CIVILIZATION_ROME','WORKS',5)==true)
   assert(s.AddExpeditionInsight(0,ca,'CIVILIZATION_ROME','WORKS',5)==false and T.writes()==beforeWrites+1)
   """,mode)


class Presentation(unittest.TestCase):
 def test_summary_projects_independent_knownness_without_inspecting_invalid_archive(self):
  v=isolated();v.execute("local x=s.InstitutionSummary(0,ca);assert(x.known and x.insightsKnown==false and x.insights==nil and x.dialogue==15 and x.engineering==1);assert(T.writes()==beforeWrites)")
 def test_only_CultureIV_shows_pending_and_availability_changes_signature(self):
  v=isolated();v.execute("""
  include('InstitutionPresentation')
  Locale={Lookup=function(key,...)local a={...};for i,x in ipairs(a)do a[i]=tostring(x)end;return key..'('..table.concat(a,',')..')'end}
  local value={specialization='CULTURE',potential=4,active=4,activeStatus='KNOWN',institutionSummary=s.InstitutionSummary(0,ca)}
  local fourth=SPCInstitutionPresentation.Tooltip(4,value);local third=SPCInstitutionPresentation.Tooltip(3,value)
  assert(fourth:find('LOC_SPC_INST_PENDING',1,true)and not fourth:find('LOC_SPC_INST_INSIGHTS_VALUE',1,true))
  assert(third:find('LOC_SPC_INST_DIALOGUE_VALUE(15)',1,true))
  local sig=SPCInstitutionPresentation.Signature(value);value.institutionSummary.insightsKnown=true
  assert(SPCInstitutionPresentation.Signature(value)~=sig)
  value.institutionSummary.insights=0;fourth=SPCInstitutionPresentation.Tooltip(4,value)
  assert(fourth:find('LOC_SPC_INST_INSIGHTS_VALUE(0)',1,true))
  """)


def load_tests(loader,standard,pattern):
 selection=json.loads((ROOT/'DevelopmentTests/refactor_selection.json').read_text())
 inherited=unittest.TestSuite(loader.loadTestsFromName(name)for name in selection['stages']['S8c5c'])
 return unittest.TestSuite([standard,inherited])

if __name__=='__main__':unittest.main()
