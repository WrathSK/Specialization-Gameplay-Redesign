"""Production legacy-owner wiring with actual Store, participants and target recovery."""
from contextlib import contextmanager
from pathlib import Path
from unittest.mock import patch
import json,re,subprocess,unittest
from refactor_harness import ROOT,measure
from test_refactor_s7f import actual_store
from test_refactor_s8c5b import SETUP

BASE='49eee15'
MODULES=('Lv3Support','Lv3Effects','Lv4Percent','HalfYieldProbe','PurchaseProbe','NetworkBoost','GreatWorkProbe','Dialogue','GreatWorkAdjacency','CommerceConvergence')
SUPPORT=('CopyYields','StandardizationDiscount','CultureInspirationProbe')
SYMBOL={'GreatWorkAdjacency':'SPCGWAdjacency'}
OLD_ASSERTIONS={
 'test_refactor_s3.Composition.test_start_order_matches_original_production_sequence',
 'test_refactor_s8c4.ActualCurrentOwners.test_actual_production_Withdraw_and_fixture_hold_duties_are_preserved'}

def entry(name,source=None):
 s=source or(ROOT/'Mod/Gameplay.lua').read_text();a=s.index("composition.Run('"+name+"'");b=s.find('\n\n',a)
 return s[a:]if b<0 else s[a:b]

@contextmanager
def old_gameplay_assertion():
 p=ROOT/'Mod/Gameplay.lua';old=subprocess.check_output(['git','show',BASE+':Mod/Gameplay.lua'],cwd=ROOT,text=True);read=Path.read_text
 with patch.object(Path,'read_text',lambda path,*a,**kw:old if path==p else read(path,*a,**kw)):yield


def production(extra='',failure=None,late=None):
 v=actual_store();v.execute('priorInfo=P.Info;priorGameInfo=GameInfo');v.execute(SETUP.split('coreBeforeTurns=')[0])
 v.execute("""
 P.Field=function(t,k)return t and t[k]end;P.Count=function()end
 P.Info=function(t,k)if t=='Buildings'then return definitions[k]end;return priorInfo(t,k)end
 setmetatable(GameInfo,{__index=priorGameInfo})
 P.Rows=function()return {}end
 shared.EffectiveFacts={Read=function()error('POSITIVE_FACTS_FORBIDDEN')end}
 local source=GameInfo.Eras
 P.Rows=function(t)if t~='Eras'then return {}end;local out={};for r in source()do out[#out+1]=r end;return out end
 registered={};local register=shared.CityProgressionStore.RegisterExit
 shared.CityProgressionStore.RegisterExit=function(name,fn)assert(not registered[name]);registered[name]=true;return register(name,fn)end
 include('RuntimeComposition');composition=SPCRuntimeComposition.New(shared)
 for _,name in ipairs({'CityProgressionStore','RuntimeRetirement','EffectiveFacts','NativeFacts','GreatWorkFacts'})do
  assert(composition.Run(name,{}, {},function()end))
 end
 """+extra)
 include=v.globals().include
 def wrapped(name):
  if failure==name:raise RuntimeError('INCLUDE_FAILURE_'+name)
  out=include(name)
  if late==name:
   sym=SYMBOL.get(name,'SPC'+name)
   v.execute('local module=_G[...];local start=module.Start;module.Start=function(...)local out=start(...);error("LATE_START_FAILURE")end',sym)
  return out
 v.globals().include=wrapped
 v.execute(entry('LegacyCleanup'))
 for name in MODULES:v.execute(entry(name))
 v.execute("if shared.Dialogue then shared.Dialogue.retired=true end;composition.Complete();s=shared.CityProgressionStore;function status()return s.Status(ca).exitStatus end;function lose()T.loss(ca,9,900)end")
 return v


class Production(unittest.TestCase):
 def test_real_production_options_register_one_gate_and_preserve_all_old_start_order(self):
  s=(ROOT/'Mod/Gameplay.lua').read_text();old=subprocess.check_output(['git','show',BASE+':Mod/Gameplay.lua'],cwd=ROOT,text=True)
  pattern=r'(SPC\w+)\.Start\(P,shared'
  names=re.findall(pattern,s);self.assertEqual(names.count('SPCLegacyCleanup'),1)
  self.assertEqual([n for n in names if n!='SPCLegacyCleanup'],re.findall(pattern,old))
  self.assertLess(s.index("composition.Run('CityProgressionStore'"),s.index("composition.Run('LegacyCleanup'"));self.assertLess(s.index("composition.Run('LegacyCleanup'"),s.index("composition.Run('BindingProbe'"))
  self.assertNotIn("composition.Run('YieldCarrierExit'",s)
  for name in MODULES:self.assertIn('centralExit=true',entry(name))
  self.assertIn('retireCommerce=true',entry('Lv3Effects'))
  for name in ('NetworkBoost','GreatWorkAdjacency','CommerceConvergence'):self.assertIn('retired=true',entry(name))
  for name in SUPPORT:self.assertNotIn('centralExit',entry(name))
  v=production();v.execute("for _,name in ipairs({...})do assert(shared.StartStatus[name].state=='OK',name)end",*MODULES)
  v.execute("local n=0;for name in pairs(registered)do assert(name=='LegacyCleanup');n=n+1 end;assert(n==1);lose();assert(status()=='WITHDRAWN'and removeCalls==1409 and plotWrites==2);assert(ca.present[999999]and cb.present[999999]and ca.plotValues.OTHER=='keep');for id in pairs(byID)do assert(not ca.present[id]and cb.present[id])end")
  measure('S8c5c_actual_production_cleanup',{'prior_legacy_exits':11,'current_legacy_exit_gates':1,'building_removals':1409,'plot_writes':2,'native_effect_cleanup':'USER_GAME_TEST_REQUIRED','new_events_timers':0})
 def test_thunk_is_registered_before_include_or_Start_can_fail(self):
  for failure,late in (('LegacyCleanup',None),(None,'LegacyCleanup')):
   v=production(failure=failure,late=late);v.execute("assert(shared.StartStatus.LegacyCleanup.state=='FAILED'and shared.LegacyCleanup==nil);assert(shared.StartStatus.Lv3Support.state=='SKIPPED_DEPENDENCY'and shared.StartStatus.Lv3Effects.state=='SKIPPED_DEPENDENCY'and shared.StartStatus.Dialogue.state=='SKIPPED_DEPENDENCY');lose();assert(status()=='PARTIAL_HELD'and removeCalls==0 and plotWrites==0);s.ExitConfirmed();s.ExitConfirmed();assert(status()=='PARTIAL_HELD')")
 def test_required_participant_failure_never_fakes_group_success(self):
  for name in ('Lv3Support','Lv3Effects','Dialogue'):
   for is_late in (False,True):
    v=production(failure=None if is_late else name,late=name if is_late else None)
    v.execute("failed=...;assert(shared.StartStatus[failed].state=='FAILED');lose();assert(status()=='PARTIAL_HELD'and plotWrites==2 and not ca.present[definitions[byGroup.NetworkBoost.names[1]].Index]);s.ExitConfirmed();s.ExitConfirmed();assert(status()=='PARTIAL_HELD')",name)
 def test_nonparticipant_start_failure_does_not_lose_its_physical_cleanup(self):
  for name in ('HalfYieldProbe','PurchaseProbe','GreatWorkProbe','Lv4Percent','NetworkBoost','GreatWorkAdjacency','CommerceConvergence'):
   v=production(failure=name);v.execute("assert(shared.StartStatus[...].state=='FAILED');lose();assert(status()=='WITHDRAWN'and removeCalls==1409 and plotWrites==2)",name)
 def test_actual_two_target_owners_recover_independently_after_Store_budget(self):
  v=production("""
  local has=P.HasBuilding;P.HasBuilding=function(b,id)local group=byID[id].group
   if group=='Lv3Support'and not supportReady or group=='Lv3Effects'and not effectsReady then return nil end
   return has(b,id)
  end
  """)
  v.execute("""
  shared.Lv3Support.ready=true;shared.Lv3Effects.ready=true
  lose();s.ExitConfirmed();s.ExitConfirmed();assert(status()=='PARTIAL_HELD')
  local prior=removeCalls;supportReady=true;shared.Lv3Support.Audit({player=9,city=900})
  assert(status()=='PARTIAL_HELD'and removeCalls==prior+12)
  effectsReady=true;shared.Lv3Effects.Audit({player=9,city=900});assert(status()=='WITHDRAWN'and removeCalls==1409)
  local n=removeCalls;shared.Lv3Support.Audit({player=9,city=900});shared.Lv3Effects.Audit({player=9,city=900});assert(removeCalls==n)
  """)
 def test_exact_Dialogue_hold_clears_only_after_its_physical_readback(self):
  for field,value in (('MATCH',None),('owner',11),('city',12345),('reference','OTHER')):
   v=production();v.execute("""
   local d=shared.Dialogue;d.carrierTest={owner=0,reference='HOLD'};d.meaningOverride={reference='HOLD',city=originA};d.meaningQualification={value='keep'}
   local field,value=...;if field=='owner'then d.carrierTest.owner=value elseif field~='MATCH'then d.meaningOverride[field]=value end
   faultGroup='Dialogue';lose();assert(status()=='PARTIAL_HELD'and d.carrierTest and d.meaningOverride and d.meaningQualification)
   faultGroup=nil;s.ExitConfirmed();assert(status()=='WITHDRAWN')
   if field=='MATCH'then assert(d.carrierTest==nil and d.meaningOverride==nil and d.meaningQualification==nil)
   else assert(d.carrierTest and d.meaningOverride and d.meaningQualification)end
   """,field,value)
 def test_Dialogue_post_fault_retains_only_its_group_until_same_original_retry(self):
  v=production();v.execute("""
  local d=shared.Dialogue;d.carrierTest=setmetatable({},{__index=function()error('POST_UNAVAILABLE')end})
  lose();assert(status()=='PARTIAL_HELD'and removeCalls==1409);d.carrierTest=nil;s.ExitConfirmed();assert(status()=='WITHDRAWN'and removeCalls==1409)
  """)
 def test_Dialogue_return_reset_is_still_registered_and_history_unchanged(self):
  v=production();v.execute("""
  local d=shared.Dialogue;d.samples={stale=true};d.paired={stale=true};d.seq={stale=true};d.last={stale=true};d.test={stale=true};local generation=d.generation
  lose();ca.s.ref.owner=0;ca.s.ref.cityID=originA;Events.CityTransfered.Fire(0,originA,9)
  assert(T.record(ca).stage=='ACTIVE'and d.generation==generation+1 and next(d.samples)==nil and next(d.paired)==nil and next(d.seq)==nil and next(d.last)==nil and next(d.test)==nil)
  """)
 def test_live_Withdraw_and_manual_entry_points_remain_callable(self):
  v=production()
  for name in SUPPORT:v.execute(entry(name))
  v.execute("assert(type(shared.CopyYields.Withdraw)=='function'and type(shared.StandardizationDiscount.Withdraw)=='function'and type(shared.CultureInspirationProbe.Withdraw)=='function'and type(shared.Lv3Effects.WithdrawCulture)=='function'and type(shared.Lv4Percent.WithdrawCulture)=='function'and type(shared.GreatWorkAdjacency.Withdraw)=='function'and type(shared.CommerceConvergence.Withdraw)=='function'and type(shared.Dialogue.Init)=='function'and type(shared.HalfYieldProbe.Run)=='function'and type(shared.GreatWorkProbe.Run)=='function'and type(shared.PurchaseProbe.Run)=='function')")
 def test_real_composition_late_module_failure_keeps_registered_runner_guarded(self):
  v=production(late='Lv3Support');v.execute("lose();assert(status()=='PARTIAL_HELD');for i=1,5 do s.ExitConfirmed()end;assert(status()=='PARTIAL_HELD'and removeByGroup.Lv3Support==nil and removeCalls==1397)")


class FrozenBefore(unittest.TestCase):
 def test_original_strict_pre_owner_start_sequence_on_B339(self):
  from test_refactor_s3 import Composition
  with old_gameplay_assertion():Composition('test_start_order_matches_original_production_sequence').test_start_order_matches_original_production_sequence()
 def test_original_no_production_owner_assertion_on_B339(self):
  from test_refactor_s8c4 import ActualCurrentOwners
  ActualCurrentOwners.setUpClass()
  try:
   with old_gameplay_assertion():ActualCurrentOwners('test_actual_production_Withdraw_and_fixture_hold_duties_are_preserved').test_actual_production_Withdraw_and_fixture_hold_duties_are_preserved()
  finally:ActualCurrentOwners.tearDownClass()


def load_tests(loader,standard,pattern):
 # Keep inherited assertions exact. Only the two expressly superseded source-wiring
 # assertions execute against the precise pre-cutover source, above.
 selection=json.loads((ROOT/'DevelopmentTests/refactor_selection.json').read_text())
 source=selection['stages']['S8c5b']
 def flatten(suite):
  for test in suite:
   if isinstance(test,unittest.TestSuite):yield from flatten(test)
   else:yield test
 inherited=unittest.TestSuite()
 for name in source:
  for test in flatten(loader.loadTestsFromName(name)):
   if test.id()not in OLD_ASSERTIONS:inherited.addTest(test)
 return unittest.TestSuite([standard,inherited])

if __name__=='__main__':unittest.main()
