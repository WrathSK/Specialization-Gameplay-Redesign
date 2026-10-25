"""Research-history isolation, actual effect routing and unchanged lifecycle authority."""
from contextlib import contextmanager,ExitStack
from hashlib import sha256
from pathlib import Path
from unittest.mock import patch
import json,subprocess,unittest
from refactor_harness import ROOT,TrackedLua51,SOURCES,legacy_source_observation,measure
from test_refactor_s8b2 import fixture,BAD
import test_b247_restructuring as restructuring
import test_store_write_boundaries as store_fixture

BASE='6823150'
SUPERSEDED='test_refactor_s8b2.Isolation.test_core_or_second_bad_ability_stays_wholly_held_and_original_unchanged'

@contextmanager
def before():
 original={ROOT/'Mod'/(n+'.lua'):subprocess.check_output(['git','show',BASE+':Mod/'+n+'.lua'],cwd=ROOT,text=True)for n in ('CityProgressionStore','StoreSubrecords')}
 read,execute=Path.read_text,TrackedLua51.execute;hashes={sha256(s.encode()).hexdigest():'historical/'+BASE+'/'+str(p.relative_to(ROOT))for p,s in original.items()}
 def source(p,*a,**kw):return original[p]if p in original else read(p,*a,**kw)
 def run(vm,s,*a,**kw):
  h=sha256(s.encode()if isinstance(s,str)else s).hexdigest()
  if h in hashes:SOURCES[h]=hashes[h]
  return execute(vm,s,*a,**kw)
 with patch.object(Path,'read_text',source),patch.object(TrackedLua51,'execute',run),legacy_source_observation():yield


def tradition(extra=''):
 v=fixture();v.execute("local n=seed();n.researchTradition='BROKEN';"+extra+"frozen=install(n);testReload();s=shared.CityProgressionStore");return v


def effect():
 v=tradition();v.execute("""
 for i=1,3 do T.invest(ca,99100+i)end;T.governor(4)
 GameConfiguration.GetGameSpeedType=function()return 'STANDARD'end;GameInfo.GameSpeeds={STANDARD={CostMultiplier=100}}
 local info=P.Info;local rows={};for _,n in ipairs({5,10,15,20,25})do rows['BUILDING_SPC_RESEARCH_TRADITION_'..n]={Index=900+n,InternalOnly=1,PrereqDistrict='DISTRICT_CITY_CENTER',CitizenSlots=0,Housing=0}end
 P.Info=function(t,k)if t=='Buildings'and rows[k]then return rows[k]end;return info(t,k)end
 fxWrites,fxReads=0,0;for _,city in ipairs({ca,cb})do
  city.fx={};city.GetBuildings=function(c)return {city=c,IsPillaged=function()return false end,GetBuildingLocation=function()return c:GetY()*200+c:GetX()end}end
  city.GetBuildQueue=function(c)return {city=c}end
 end
 ca.fx[905]=true;Map.GetPlotIndex=function(x,y)return y*200+x end
 P.HasBuilding=function(b,id)fxReads=fxReads+1;return b.city.fx[id]==true end
 P.RemoveBuilding=function(b,id)b.city.fx[id]=nil;fxWrites=fxWrites+1 end
 P.CreateBuilding=function(q,id)q.city.fx[id]=true;fxWrites=fxWrites+1 end
 include('ResearchTraditionEffects');effects=SPCResearchTraditionEffects.Start(P,shared)
 effects=shared.ResearchTraditionEffects;Events.GameCoreEventPublishComplete.Fire();assert(effects.ready)
 """);return v


class Tradition(unittest.TestCase):
 def test_single_bad_history_keeps_other_abilities_and_independent_city_usable_without_writes(self):
  v=tradition();v.execute("assert(pcall(s.Base,0,ca)and pcall(s.Base,0,cb)and s.DialogueState(0,ca).value.total==15 and s.EngineeringState(0,ca).value.L==1);assert(T.writes()==beforeWrites and T.encode(T.record(ca))==frozen and s.Status(ca).subrecordIsolation.researchTradition and not pcall(s.ReadTradition,0,ca));assert(next(s.ExpeditionInsights(0,ca))==nil)")
 def test_current_two_reviewed_leaves_isolate_independently_and_preserve_both(self):
  v=tradition('n.expeditionInsights='+BAD+';');v.execute("""
  assert(pcall(s.Base,0,ca)and not pcall(s.ReadTradition,0,ca)and not pcall(s.ExpeditionInsights,0,ca))
  local st=s.Status(ca).subrecordIsolation;assert(st.expeditionInsights and st.researchTradition)
  local x=s.InstitutionSummary(0,ca);assert(x.known and x.traditionKnown==false and x.insightsKnown==false and x.tradition==nil and x.insights==nil and x.dialogue==15)
  local n=M.Copy(T.record(ca));n.revision=n.revision+1;assert(saveCandidate(ca,n));assert(T.encode(T.record(ca).expeditionInsights)==T.encode(n.expeditionInsights)and T.record(ca).researchTradition=='BROKEN')
  local writes=T.writes();n.revision=n.revision+1;n.researchTradition=nil;assert(not saveCandidate(ca,n)and T.writes()==writes and pcall(s.Base,0,ca))
  """)
 def test_initial_P4_investment_and_confirmed_history_do_not_replace_bad_history(self):
  v=tradition();v.execute("""
  for i=1,3 do T.invest(ca,99200+i)end
  assert(shared.EffectiveFacts.Read(0,ca).potential==4 and T.record(ca).researchTradition=='BROKEN')
  local h=s.InstitutionHistory(0,ca);assert(h[4]==T.now())
  assert(not pcall(s.ReadTradition,0,ca)and s.Status(ca).subrecordIsolation.researchTradition)
  """)
 def test_history_date_does_not_fall_back_to_invalid_age_object_or_load_time(self):
  v=tradition();v.execute("local h=s.InstitutionHistory(0,ca);assert(h[1]==T.record(ca).base.first.turn and h[4]==nil and T.writes()==beforeWrites)")
 def test_twenty_turns_do_not_read_advance_or_rewrite_isolated_age(self):
  v=tradition('n.commerce=nil;n.commerceKnown=nil;');v.execute("""
  local advance=SPCResearchTradition.Advance;SPCResearchTradition.Advance=function()error('ISOLATED_AGE_MUST_NOT_ADVANCE')end
  local get=CityManager.GetCityAt;local reads=0;CityManager.GetCityAt=function(...)reads=reads+1;return get(...)end
  for i=1,20 do T.turn(1)end
  assert(reads==0 and T.writes()==beforeWrites and T.encode(T.record(ca))==frozen and pcall(s.Base,0,ca))
  SPCResearchTradition.Advance=advance;CityManager.GetCityAt=get
  """)
 def test_loss_and_return_keep_bad_leaf_exact_instead_of_editing_owner_policy_state(self):
  for payload in ("'BROKEN'","{version=1,start=0,age=999,cursor=0,state='COUNTING',receipt='UNKNOWN',extra='keep'}"):
   v=tradition('n.researchTradition='+payload+';');v.execute("""
   local original=T.encode(T.record(ca).researchTradition);local id=ca:GetID();s.RegisterExit('Fixture',function()end)
   T.loss(ca,9,900);assert(T.record(ca).stage=='HELD_TRANSFER'and T.encode(T.record(ca).researchTradition)==original)
   ca.s.ref.owner=0;ca.s.ref.cityID=id;Events.CityTransfered.Fire(0,id,9)
   assert(T.record(ca).stage=='ACTIVE'and pcall(s.Base,0,ca)and T.encode(T.record(ca).researchTradition)==original and not pcall(s.ReadTradition,0,ca))
   """)
 def test_restructuring_begin_finish_preserve_bad_leaf_without_blocking_identity_transaction(self):
  v=tradition();v.execute("""
  for i=1,3 do T.invest(ca,99300+i)end;team={owner=0,id=777,uid='TEAM:777'}
  s.BeginRestructuring(0,ca,team,'REST_BAD_AGE');assert(T.record(ca).restructuring.phase=='REALLOCATING'and T.record(ca).researchTradition=='BROKEN')
  T.turn(5);s.ConfigureRestructuring(0,ca,team,'CULTURE',{districtID=601,type='DISTRICT_THEATER',turn=T.now()})
  Players[0].GetUnits=function()return {FindID=function()return nil end}end
  s.ConfirmRestructuringConsumption(0,ca,team);assert(s.FinishRestructuring(0,ca,team)==true)
  assert(shared.EffectiveFacts.Read(0,ca).specialization=='CULTURE'and T.record(ca).researchTradition=='BROKEN'and s.Status(ca).subrecordIsolation.researchTradition)
  """)
 def test_save_cannot_delete_change_or_forge_preserved_Tradition(self):
  for candidate in ("nil","{}","{state='COUNTING'}","setmetatable({},{__index={state='COUNTING'}})"):
   v=tradition();v.execute("local n=M.Copy(T.record(ca));n.revision=n.revision+1;n.researchTradition="+candidate+";assert(not saveCandidate(ca,n));assert(T.writes()==beforeWrites and T.encode(T.record(ca))==frozen and pcall(s.Base,0,ca))")
 def test_other_core_and_unreviewed_ability_errors_still_hold_the_whole_worker(self):
  for change in ("n.schema=99","n.revision=0","n.origin.x=12345","n.base.token='FORGED'","n.binding={}","n.base.first={}","n.current={}","n.loss={}","n.restructuring={}","n.dialogueKnown=false","n.claimTimer={}"):
   v=tradition(change+';');v.execute("assert(not pcall(s.Base,0,ca)and pcall(s.Base,0,cb)and T.writes()==beforeWrites and T.encode(T.record(ca))==frozen and next(s.Status(ca).subrecordIsolation)==nil)")
 def test_visit_keeps_actual_effect_owner_routing_after_history_isolation(self):
  v=tradition();v.execute("local calls=0;s.VisitTradition(0,function(c)assert(c==ca);calls=calls+1;assert(not pcall(s.ReadTradition,0,c))end);assert(calls==1 and T.writes()==beforeWrites)")


class EffectsAndPresentation(unittest.TestCase):
 def test_actual_Mark_Flush_reliably_withdraws_when_ACTIVE_drops(self):
  v=effect();v.execute("""
  assert(ca.fx[905]and fxWrites==0 and effects.lastError)
  local writes=T.writes();T.governor(1);effects.Mark(0);effects.Flush()
  assert(not ca.fx[905]and fxWrites==1 and T.writes()==writes and T.record(ca).researchTradition=='BROKEN')
  """)
  measure('S8b3_actual_Tradition_effect_routing',{'modules':'Store/EffectiveFacts/ResearchTraditionEffects','isolated_qualified_history':'UNKNOWN_retains','confirmed_ACTIVE_drop':'withdraws','history_writes_from_effect':0})
 def test_rejected_early_Visit_guard_counterexample_then_original_route_recovers(self):
  v=effect();v.execute("""
  local visit=s.VisitTradition;s.VisitTradition=function()error('TRADITION_HISTORY_ISOLATED')end
  T.governor(1);effects.Mark(0);effects.Flush();assert(ca.fx[905]and fxWrites==0)
  s.VisitTradition=visit;effects.Mark(0);effects.Flush();assert(not ca.fx[905]and fxWrites==1)
  """)
 def test_qualified_UNKNOWN_does_not_create_zero_or_idle_retry(self):
  v=effect();v.execute("""
  assert(ca.fx[905]and fxWrites==0 and effects.lastError)
  local reads,writes=fxReads,T.writes();for i=1,1000 do Events.GameCoreEventPublishComplete.Fire()end
  assert(fxReads==reads and fxWrites==0 and T.writes()==writes)
  """)
 def test_institution_summary_and_tooltip_do_not_call_bad_age_not_started_or_zero(self):
  v=tradition();v.execute("""
  local summary=s.InstitutionSummary(0,ca);assert(summary.known and summary.traditionKnown==false and summary.tradition==nil and summary.dialogue==15 and summary.insightsKnown)
  include('InstitutionPresentation');Locale={Lookup=function(k,...)return k end}
  local value={specialization='RESEARCH',potential=4,active=4,activeStatus='KNOWN',institutionSummary=summary}
  local tooltip=SPCInstitutionPresentation.Tooltip(4,value)
  assert(tooltip:find('LOC_SPC_INST_PENDING',1,true)and not tooltip:find('LOC_SPC_INST_NOT_STARTED',1,true)and not tooltip:find('LOC_SPC_INST_TRADITION_VALUE',1,true))
  local sig=SPCInstitutionPresentation.Signature(value);summary.traditionKnown=true;summary.tradition=false
  assert(SPCInstitutionPresentation.Signature(value)~=sig and SPCInstitutionPresentation.Tooltip(4,value):find('LOC_SPC_INST_NOT_STARTED',1,true))
  """)


class RetainedRestructuring(restructuring.Store):
 def setUp(self):
  self.context=ExitStack();self.addCleanup(self.context.close)
  self.context.enter_context(patch.object(store_fixture,'LuaRuntime',TrackedLua51))
  self.context.enter_context(legacy_source_observation())


class FrozenBefore(unittest.TestCase):
 def test_original_B341_single_Insights_scope_remains_frozen_before_Tradition_extension(self):
  from test_refactor_s8b2 import Isolation
  with before():Isolation('test_core_or_second_bad_ability_stays_wholly_held_and_original_unchanged').test_core_or_second_bad_ability_stays_wholly_held_and_original_unchanged()


def load_tests(loader,standard,pattern):
 selection=json.loads((ROOT/'DevelopmentTests/refactor_selection.json').read_text())
 def flatten(suite):
  for test in suite:
   if isinstance(test,unittest.TestSuite):yield from flatten(test)
   else:yield test
 inherited=unittest.TestSuite()
 for name in selection['stages']['S8b2']:
  for test in flatten(loader.loadTestsFromName(name)):
   if test.id()!=SUPERSEDED:inherited.addTest(test)
 return unittest.TestSuite([standard,inherited])

if __name__=='__main__':unittest.main()
