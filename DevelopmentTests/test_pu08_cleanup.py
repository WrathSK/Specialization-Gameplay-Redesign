"""PU08 fixed required duties and actual Store/Support/Training composition.
Explicit native doubles; no native failure incidence or all-owner effect coverage.
"""
from contextlib import contextmanager
from pathlib import Path
from unittest.mock import patch
import re,subprocess,unittest
from refactor_harness import Context,ROOT,TrackedLua51,legacy_source_observation,measure
from test_refactor_s7f import actual_store
from test_refactor_s8c5c import entry
import test_expedition_training as training_cases

BASE='f6767845336ff6c7e2d5f794bccb5de3d8676bfd'
# The two exact before/after checks describe the mandatory-cleanup cutover.
# The other tests still exercise the current startup and cleanup paths.
PU08_CUTOVER='7729420ce9be628fc6915357f3e6ed5e2a650eb2'
@contextmanager
def baseline():
 paths=[ROOT/'Mod'/(n+'.lua')for n in ('RuntimeComposition','Gameplay','ExpeditionTraining')]
 sources={p:subprocess.check_output(['git','show',BASE+':'+str(p.relative_to(ROOT))],cwd=ROOT,text=True)for p in paths};read=Path.read_text
 with patch.object(Path,'read_text',lambda p,*a,**kw:sources[p]if p in sources else read(p,*a,**kw)),legacy_source_observation():yield

def declarations():
 text=entry('CityProgressionStore')
 if 'composition.RequireCleanup'not in text:return []
 text=text.split('for _,row in ipairs({',1)[1].split('})do composition.RequireCleanup',1)[0]
 rows=[]
 for owner,a,b in re.findall(r"\{'([^']+)',(nil|'[^']+')(?:,(nil|'[^']+'))?\}",text):
  rows.append((owner,None if a=='nil'else a.strip("'"),None if not b or b=='nil'else b.strip("'")))
 return rows

def component():
 c=Context();c.load('RuntimeComposition');c.execute("""
 print=function()end;d=SPCRuntimeComposition.New(shared);calls=0;exits={};returns={}
 shared.CityProgressionStore={RegisterExit=function(n,f)assert(not exits[n]);exits[n]=f end,
 RegisterReturn=function(n,f)assert(not returns[n]);returns[n]=f end}
 """);return c

def store_fixture(target='ResearchSupport',mode='failed'):
 v=actual_store();v.execute("""
 ca,cb=a,b;s=shared.CityProgressionStore;originID=ca:GetID();registered={};returned={};ordinary=999999
 for _,c in ipairs({ca,cb})do c.present={[ordinary]=true};c.GetBuildings=function(c)return {city=c}end end
 local names={'RESEARCH','CULTURE','COMMERCE'};supportDefinitions={};for i,kind in ipairs(names)do
  local name='BUILDING_SPC_DEV_'..kind..'_SUPPORT';supportDefinitions[name]={Index=7000+i,BuildingType=name,InternalOnly=1}
  ca.present[7000+i]=true;cb.present[7000+i]=true
 end
 local info=P.Info;P.Info=function(t,k)if t=='Buildings'then return supportDefinitions[k]end;return info(t,k)end
 reads,removals=0,0;P.HasBuilding=function(b,id)reads=reads+1;if unknownPresence then return nil end;return b.city.present[id]==true end
 P.RemoveBuilding=function(b,id)assert(id~=ordinary);removals=removals+1;if not removeNoop then b.city.present[id]=nil end end
 P.CreateBuilding=function()error('POSITIVE_EFFECT_FORBIDDEN')end
 P.Field=function(t,k)return t and t[k]end;P.Count=function()end
 shared.EffectiveFacts={Read=function()error('POSITIVE_FACTS_FORBIDDEN')end}
 s.HistoryStartStatus=function()return 'WAITING'end -- latch must not fabricate positive facts at startup
 local register,ret=s.RegisterExit,s.RegisterReturn
 s.RegisterExit=function(n,f)registered[n]=f;return register(n,f)end
 s.RegisterReturn=function(n,f)returned[n]=f;return ret(n,f)end
 include('RuntimeComposition');composition=SPCRuntimeComposition.New(shared)
 for _,name in ipairs({'CityIdentityDefinition','FactChanges','RuntimeRetirement','EffectiveFacts','NativeFacts'})do assert(composition.Run(name,{}, {},function()end))end
 """)
 # Read the real Gameplay declaration; this fixture executes its selected duty
 # with actual Store+owner. Full startup/table wiring is tested separately.
 rows=declarations();chosen=[row for row in rows if row[0]==target]
 if rows:
  assert len(chosen)==1
  owner,ex,ret=chosen[0]
  v.execute("composition.RequireCleanup(...)",owner,ex,ret)
 v.execute("s.RegisterExit('IndependentFixture',function()return true end)")
 if mode=='skipped':
  v.execute("assert(not composition.Run('UnavailableDependency',{}, {},function()error('INJECTED')end));assert(not composition.Run(...,{'UnavailableDependency'},{},function()error('MUST_NOT_RUN')end))",target)
 elif mode=='failed':v.execute("assert(not composition.Run(...,{}, {},function()error('INJECTED_BEFORE_REGISTRATION')end))",target)
 elif target=='ResearchSupport':
  v.execute(entry('ResearchSupport'))
  assert v.eval("shared.StartStatus.ResearchSupport.state=='OK'")
 else:raise ValueError((target,mode))
 v.execute("composition.Complete();function lose()T.loss(ca,9,900)end;function status()return s.Status(ca).exitStatus end")
 return v

def training():
 original=training_cases.gate
 def gate():
  v=original();v.execute("""
 exits={};removedOwned=0;cleanupReads=0
 shared.CityProgressionStore.RegisterExit=function(n,f)exits[n]=f end
 shared.CityProgressionStore.RemoveOwned=function(c,loss,names)
  cleanupReads=cleanupReads+1;assert(c==exitCity and not badEndpoint and loss==lossProof,'EXIT_NOT_CONFIRMED')
  assert(#names==1 and names[1]=='BUILDING_SPC_EXPEDITION_TRAINING_ACCESS','WRONG_IDS')
  if onRemove then onRemove()end
  if cleanupThrow then error('CLEANUP_UNAVAILABLE')end
  local id=999;local b=c:GetBuildings();local has=P.HasBuilding(b,id)
  assert(type(has)=='boolean','PRESENCE_UNKNOWN')
  if has then P.RemoveBuilding(b,id)end
  assert(P.HasBuilding(b,id)==false,'REMOVE_UNCONFIRMED')
 end
 """);return v
 with patch.object(training_cases,'gate',gate),patch.object(__import__('test_expedition_gate'),'LuaRuntime',TrackedLua51),legacy_source_observation():v=training_cases.fixture()
 v.execute("""
 lossProof={origin={owner=2,cityID=1,x=1,y=1},target={owner=3,cityID=42,x=1,y=1}}
 exitCity={GetBuildings=function()return buildings end};local remove=P.RemoveBuilding
 P.RemoveBuilding=function(b,id)removedOwned=removedOwned+1;if removeNoop then return end;return remove(b,id)end
 function cleanup()return exits.ExpeditionTraining(exitCity,lossProof)end
 """);return v

class Required(unittest.TestCase):
 def test_before_start_missing_binding_and_skipped_owner_fail_closed(self):
  for mode in ('not_started','missing','failed','skipped','late_failed'):
   c=component();c.execute("d.RequireCleanup('Owner','EXIT','RETURN')")
   if mode=='missing':c.execute("assert(d.Run('Owner',{}, {},function()end))")
   if mode=='failed':c.execute("assert(not d.Run('Owner',{}, {},function()error('BEFORE')end))")
   if mode=='skipped':c.execute("assert(not d.Run('Owner',{'Absent'}, {},function()error('UNREACHABLE')end))")
   if mode=='late_failed':c.execute("assert(not d.Run('Owner',{}, {},function()shared.CityProgressionStore.RegisterExit('EXIT',function()calls=calls+1 end);shared.CityProgressionStore.RegisterReturn('RETURN',function()calls=calls+1 end);error('AFTER')end))")
   c.execute("for i=1,4 do assert(not pcall(exits.EXIT)and not pcall(returns.RETURN))end;assert(calls==0)")
 def test_successful_matching_registration_keeps_args_values_and_one_registry_entry(self):
  c=component();c.execute("""
  d.RequireCleanup('Owner','EXIT','RETURN');local ex,ret=exits.EXIT,returns.RETURN
  assert(d.Run('Owner',{}, {},function()
   shared.CityProgressionStore.RegisterExit('EXIT',function(a,b,c)calls=calls+1;assert(a==1 and b==2 and c==3);return false,'DETAIL'end)
   shared.CityProgressionStore.RegisterReturn('RETURN',function(a,b)assert(a==4 and b==5);calls=calls+1 end)
  end));local ok,detail=exits.EXIT(1,2,3);assert(ok==false and detail=='DETAIL');assert(returns.RETURN(4,5)==nil)
  assert(ex==exits.EXIT and ret==returns.RETURN and calls==2)
  """)
 def test_wrong_owner_or_duplicate_binding_is_not_accepted(self):
  c=component();c.execute("d.RequireCleanup('Owner','EXIT');assert(not d.Run('Impostor',{}, {},function()shared.CityProgressionStore.RegisterExit('EXIT',function()calls=calls+1 end)end));assert(not pcall(exits.EXIT));assert(not d.Run('Owner',{}, {},function()shared.CityProgressionStore.RegisterExit('EXIT',function()calls=calls+1 end);shared.CityProgressionStore.RegisterExit('EXIT',function()calls=calls+1 end)end));assert(not pcall(exits.EXIT)and calls==0)")
 def test_late_requirement_store_replacement_and_optional_failure_do_not_bypass(self):
  c=component();c.execute("d.RequireCleanup('Owner','EXIT');assert(d.Run('Owner',{}, {},function()shared.CityProgressionStore.RegisterExit('EXIT',function()calls=calls+1 end)end));assert(not d.Run('Observer',{}, {},function()error('OPTIONAL')end));assert(pcall(exits.EXIT)and calls==1);assert(not pcall(d.RequireCleanup,'Owner','ANOTHER'));shared.CityProgressionStore={};assert(not pcall(exits.EXIT)and calls==1)")
 def test_all_actual_declared_names_have_reviewed_production_registration(self):
  rows=declarations();self.assertEqual(len(rows),34)
  self.assertEqual(sum(ex is not None for _,ex,_ in rows),29);self.assertEqual(sum(ret is not None for _,_,ret in rows),23)
  for owner,ex,ret in rows:
   source=(ROOT/'Mod'/(owner+'.lua')).read_text()if owner!='LegacyCleanup'else entry('LegacyCleanup')
   if ex:self.assertIn("RegisterExit('"+ex+"'",source)
   if ret:self.assertIn("RegisterReturn('"+ret+"'",source)
  self.assertEqual(len({ex for _,ex,_ in rows if ex}),29);self.assertEqual(len({ret for _,_,ret in rows if ret}),23)
  self.assertFalse(any(o in {'CopyYields','StandardizationDiscount','CarrierHealthTrace','ReadinessSummary','HalfYieldProbe'}for o,_,_ in rows))
  measure('PU08_fixed_duties',{'owners':34,'exit_slots':29,'return_slots':23,'new_native_reads_or_events':0,'scope':'static reviewed actual current Gameplay declaration,not native registry observation'})
 def test_actual_full_Gameplay_reserves_duties_before_any_later_Start(self):
  from refactor_defect_fixtures import startup
  c=startup();c.execute("""
  requiredExits={};requiredReturns={}
  SPCCityProgressionStore.Start=function(P,s)
   s.CityProgressionStore={RegisterExit=function(n,f)assert(not requiredExits[n]);requiredExits[n]=f end,
    RegisterReturn=function(n,f)assert(not requiredReturns[n]);requiredReturns[n]=f end}
  end
  SPCResearchTraditionEffects=module('HealthyResearchTraditionEffects','ResearchTraditionEffects')
  """);c.load('Gameplay');c.execute("local e,r=0,0;for _ in pairs(requiredExits)do e=e+1 end;for _ in pairs(requiredReturns)do r=r+1 end;assert(e==29 and r==23);assert(not pcall(requiredExits.ResearchSupport)and not pcall(requiredExits.ExpeditionTraining)and not pcall(requiredReturns.Standardization))")
 def test_entire_ordinary_start_order_matches_fixed_before_source(self):
  before=subprocess.check_output(['git','show',BASE+':Mod/Gameplay.lua'],cwd=ROOT,text=True)
  after=subprocess.check_output(['git','show',PU08_CUTOVER+':Mod/Gameplay.lua'],cwd=ROOT,text=True)
  names=re.findall(r'(SPC\w+)\.Start\(P,shared',after);self.assertGreater(len(names),70)
  self.assertEqual(re.findall(r'(SPC\w+)\.Start\(P,shared',before),names)
 def test_successful_sibling_and_phase_ranked_return_order_not_changed(self):
  before=subprocess.check_output(['git','show',BASE+':Mod/CityProgressionStore.lua'],cwd=ROOT)
  after=subprocess.check_output(['git','show',PU08_CUTOVER+':Mod/CityProgressionStore.lua'],cwd=ROOT)
  self.assertEqual(after,before)
  c=component();c.execute("d.RequireCleanup('One','A');d.RequireCleanup('Two','B');assert(d.Run('One',{}, {},function()shared.CityProgressionStore.RegisterExit('A',function()calls=calls+1 end)end));assert(not d.Run('Two',{}, {},function()error('FAIL')end));assert(pcall(exits.A)and not pcall(exits.B)and calls==1)")
 def test_no_idle_discovery_or_retry_and_restricted_lua(self):
  c=component();c.execute("local pulse=Events.GameCoreEventPublishComplete;debug=nil;rawget=nil;rawset=nil;rawequal=nil;os=nil;io=nil;package=nil;d.RequireCleanup('Owner','E','R');assert(d.Run('Owner',{}, {},function()shared.CityProgressionStore.RegisterExit('E',function()calls=calls+1 end);shared.CityProgressionStore.RegisterReturn('R',function()calls=calls+1 end)end));d.Complete();for i=1,1000 do publish()end;assert(calls==0 and not pcall(d.RequireCleanup,'Later','E2'))")

class StoreComposition(unittest.TestCase):
 def test_failed_start_with_installed_carriers_is_not_vacuous_exit(self):
  v=store_fixture();v.execute("lose();assert(status()=='PARTIAL_HELD','FAILED_START_EXIT_WAS_VACUOUSLY_COMPLETE');assert(s.Status(ca).exitErrors.ResearchSupport and removals==0 and ca.present[7001]and cb.present[7001])")
 def test_skipped_start_with_installed_carriers_keeps_required_duty(self):
  v=store_fixture(mode='skipped');v.execute("lose();assert(status()=='PARTIAL_HELD','SKIPPED_START_DUTY_DISAPPEARED');assert(s.Status(ca).exitErrors.ResearchSupport and removals==0)")
 def test_actual_support_withdraws_exact_old_effects_on_noncurrent_profession(self):
  v=store_fixture(mode='healthy');v.execute("lose();assert(status()=='WITHDRAWN');assert(removals==3 and ca.present[ordinary]and cb.present[ordinary]);for i=7001,7003 do assert(not ca.present[i]and cb.present[i])end;local n=removals;s.ExitConfirmed();assert(removals==n)")
 def test_unknown_presence_and_remove_readback_do_not_complete_affected_owner(self):
  for fault in ('unknownPresence=true','removeNoop=true'):
   v=store_fixture(mode='healthy');v.execute(fault+";lose();assert(status()=='PARTIAL_HELD'and s.Status(ca).exitErrors.ResearchSupport);unknownPresence=false;removeNoop=false;s.ExitConfirmed();assert(status()=='WITHDRAWN'and not ca.present[7001]and cb.present[7001])")
 def test_wrong_endpoint_reference_and_third_owner_never_clean_arbitrary_city(self):
  v=store_fixture(mode='healthy');v.execute("local get=CityManager.GetCityAt;CityManager.GetCityAt=function()return nil end;lose();assert(removals==0);ca.s.ref.owner=10;ca.s.ref.cityID=1000;CityManager.GetCityAt=get;s.ExitConfirmed();assert(removals==0);ca.s.ref.owner=9;ca.s.ref.cityID=900;Events.CityTransfered.Fire(9,900,0);s.ExitConfirmed();assert(status()=='WITHDRAWN'and removals==3 and cb.present[7001])")
 def test_failed_return_owner_cannot_commit_restored_identity(self):
  v=store_fixture(target='DistrictCompleteness');v.execute("lose();assert(status()=='WITHDRAWN');ca.s.ref.owner=0;ca.s.ref.cityID=originID;Events.CityTransfered.Fire(0,originID,9);assert(T.record(ca).stage=='HELD_TRANSFER','MISSING_RETURN_DUTY_ALLOWED_RECAPTURE');assert(s.Status(ca).returnErrors.DistrictCompleteness)")
 def test_failed_duties_retain_existing_attempt_budget_and_idle_has_zero_effect_work(self):
  v=store_fixture();v.execute("lose();s.ExitConfirmed();s.ExitConfirmed();local readsBefore=reads;for i=1,100 do s.ExitConfirmed()end;for i=1,1000 do Events.GameCoreEventPublishComplete.Fire()end;assert(reads==readsBefore and removals==0 and status()=='PARTIAL_HELD')")

class TrainingCleanup(unittest.TestCase):
 def test_matching_source_reaches_saved_held_and_confirmed_absence(self):
  v=training();v.execute("reserve();local before=storeWrites;assert(cleanup()==true,'MATCHED_TRAINING_CLEANUP_NOT_CONFIRMED');assert(state().phase=='HELD'and not state().blocked and not marker and storeWrites==before+1 and initCalls==0);local n=storeWrites;assert(cleanup()==true and storeWrites==n and removedOwned==1)")
 def test_cleanup_throw_is_not_success_or_unrelated_team_hold(self):
  v=training();v.execute("reserve();lossProof.origin.cityID=2;lossProof.origin.x=2;cleanupThrow=true;assert(cleanup()==false,'THROWN_CLEANUP_REPORTED_SUCCESS');assert(state().phase=='TRAINING'and marker and removedOwned==0)")
 def test_same_source_failed_removal_keeps_exit_pending(self):
  v=training();v.execute("reserve();removeNoop=true;local writes=storeWrites;assert(cleanup()==false,'UNCONFIRMED_REMOVE_REPORTED_SUCCESS');assert(state().phase=='TRAINING'and storeWrites==writes and marker)")
 def test_busy_nested_exit_is_false_with_no_replayed_action(self):
  v=training();v.execute("reserve();local once=true;onRemove=function()if once then once=false;nested=cleanup();assert(nested==false,'BUSY_CLEANUP_WAS_SUCCESS')end end;assert(cleanup()==true and nested==false and removedOwned==1 and initCalls==0 and state().phase=='HELD')")
 def test_saved_hold_readback_failure_cannot_confirm_exit(self):
  v=training();v.execute("reserve();storeNoop=true;assert(cleanup()==false,'UNSAVED_HOLD_REPORTED_SUCCESS');assert(state().blocked and not marker and initCalls==0);local w=storeWrites;assert(cleanup()==false and storeWrites==w)")
 def test_wrong_source_location_is_not_held_or_guessed(self):
  v=training();v.execute("reserve();lossProof.origin.x=99;local w=storeWrites;assert(cleanup()==false and state().phase=='TRAINING'and storeWrites==w and not marker)")
 def test_inactive_or_other_training_record_still_retires_exact_physical_marker(self):
  for active in (False,True):
   v=training();v.execute("if ...then reserve();lossProof.origin.cityID=2;lossProof.origin.x=2 else marker=true end;local writes=storeWrites;assert(cleanup()==true,'RESIDUAL_MARKER_NOT_CONFIRMED');assert(not marker and removedOwned==1 and storeWrites==writes and initCalls==0)",active)
 def test_unknown_state_and_bad_native_endpoint_stay_pending(self):
  for fault in ('badEndpoint=true','storeReadError=true'):
   v=training();v.execute("reserve();"+fault+";assert(cleanup()==false and initCalls==0)")
 def test_native_cleanup_reentry_does_not_overwrite_newer_gate_state(self):
  v=training();v.execute("reserve();onRemove=function()shared.ExpeditionGate.Training.Hold('NEWER_GATE_STOP')end;assert(cleanup()==false and state().phase=='HELD'and state().stop=='NEWER_GATE_STOP'and not marker);onRemove=nil;local w=storeWrites;assert(cleanup()==true and storeWrites==w and initCalls==0)")
 def test_no_idle_native_action_added_and_observer_absence_is_independent(self):
  v=training();v.execute("SPCExpeditionTrainingDiagnostics=nil;SPCCultureDiagnostics=nil;reserve();assert(cleanup()==true);local n,w=removedOwned,storeWrites;for i=1,1000 do hooks.GameCoreEventPublishComplete()end;assert(removedOwned==n and storeWrites==w and initCalls==0)")

if __name__=='__main__':unittest.main()
