"""S7d5 actual Crew owner transaction, typed result and receipt preservation.
Native multipliers/event order remain doubles, not user-game acceptance.
"""
from contextlib import contextmanager,nullcontext
from hashlib import sha256
from pathlib import Path
import subprocess
import unittest
from unittest.mock import patch
from refactor_harness import ROOT,TrackedLua51,SOURCES,legacy_source_observation,measure
import test_store_write_boundaries as cities
import test_b236_crews as crews
import test_b238_crew_modifiers as modifiers
from test_refactor_s6i import investment
from test_refactor_s6h import ActualProfile

BASE='75f435a2530fa4d0236fbb8394f69cfd5c4fd28e'

@contextmanager
def profile():
 with patch.object(cities,'LuaRuntime',TrackedLua51),legacy_source_observation():yield

@contextmanager
def history():
 paths=('CrewProjects','CrewModel','UnitSiteFacts','UnitActions','CrewPrecision')
 original={ROOT/'Mod'/(n+'.lua'):subprocess.check_output(['git','show',BASE+':Mod/'+n+'.lua'],cwd=ROOT,text=True)for n in paths}
 read,execute=Path.read_text,TrackedLua51.execute
 hashes={sha256(s.encode()).hexdigest():'historical/'+BASE+'/'+str(p.relative_to(ROOT))for p,s in original.items()}
 def source(p,*a,**kw):return original[p]if p in original else read(p,*a,**kw)
 def run(vm,s,*a,**kw):
  h=sha256(s.encode()if isinstance(s,str)else s).hexdigest()
  if h in hashes:SOURCES[h]=hashes[h]
  return execute(vm,s,*a,**kw)
 with patch.object(Path,'read_text',source),patch.object(TrackedLua51,'execute',run),legacy_source_observation():yield

def fixture(observer=False):
 with profile():vm=modifiers.fixture(observer)
 vm.execute("""
 print=function()end
 c=C.make();local p=C.begin(c);C.complete(c,p);C.actions(c);u=C.units[20001]
 function prepare()return shared.UnitActions.Run(0,{Action='UNIT_ACTION_PREPARE',UnitID=20001,Token='USE'})end
 function confirm()return shared.UnitActions.Run(0,{Action='UNIT_ACTION_CONFIRM',UnitID=20001,PlanToken='USE',Token='CONFIRM'})end
 """)
 return vm

FAULTS={
 'normal':'do end',
 'receipt_drop':"local set=Players[0].SetProperty;Players[0].SetProperty=function(o,k,v)if k~='SPC_CREW_ACTION_RECEIPTS_V1'then return set(o,k,v)end end",
 'reservation_drop':"local set=u.SetProperty;u.SetProperty=function(o,k,v)if k~='SPC_CREW_RESERVED'then return set(o,k,v)end end",
 'debit_drop':"local get=Players[0].GetUnits;Players[0].GetUnits=function()local x=get();x.Destroy=function()end;return x end",
 'target_after_debit':"local get=Players[0].GetUnits;Players[0].GetUnits=function()local x=get();local destroy=x.Destroy;x.Destroy=function(...)destroy(...);c:GetBuildQueue().progress=11 end;return x end",
 'native_before':"local q=c:GetBuildQueue();q.AddProgress=function(_,n)q.adds[#q.adds+1]=n;error('native before')end",
 'native_after':"local q=c:GetBuildQueue();q.AddProgress=function(_,n)q.adds[#q.adds+1]=n;q.progress=q.progress+2*n;error('native after')end",
 'returned_receipt_drop':"local set=Players[0].SetProperty;Players[0].SetProperty=function(o,k,v)if k=='SPC_CREW_ACTION_RECEIPTS_V1'and next(v)then local _,row=next(v);if row.state=='GRANT_RETURNED'then return end end;return set(o,k,v)end",
}

class Transaction(unittest.TestCase):
 def test_success_and_all_destructive_faults_match_previous_effects_and_receipts(self):
  results=[]
  for old in (True,False):
   for mode,inject in FAULTS.items():
    with history()if old else nullcontext():
     vm=fixture();vm.execute("assert(prepare():find('PREPARED'));mutationLog={};local set=P.SetProperty;P.SetProperty=function(o,k,v)mutationLog[#mutationLog+1]=k..':'..(k=='SPC_CREW_ACTION_RECEIPTS_V1'and (select(2,next(v)).state)or tostring(v));return set(o,k,v)end;"+inject+";text,investmentReceipt,outcome=confirm();unitRemains=C.units[20001]~=nil;result=T.encode({receipts=C.props.SPC_CREW_ACTION_RECEIPTS_V1,adds=c:GetBuildQueue().adds,progress=c:GetBuildQueue().progress,present=unitRemains});for i=1,3 do confirm()end;assert(#c:GetBuildQueue().adds<=1)")
     results.append((old,mode,vm.eval('result'),list(vm.globals().mutationLog.values())))
  self.assertEqual([x[1:]for x in results[:len(FAULTS)]],[x[1:]for x in results[len(FAULTS):]])
  measure('S7d5_crew_use_differential',{'baseline':BASE,'modes':len(FAULTS),'same_unit_debit_receipts_progress_and_mutation_order':True,'native_grant_calls_max':1,'native_CPU_or_memory_claim':False})
 def test_typed_states_preserve_attempt_phase_and_no_second_call(self):
  for mode,inject in FAULTS.items():
   with self.subTest(fault=mode):
    vm=fixture();vm.execute("assert(prepare():find('PREPARED'));"+inject+";local text,r,outcome=confirm();assert(r==nil);result=outcome")
    self.assertEqual(vm.eval('result.status'),'COMMITTED'if mode=='normal'else'HELD')
    self.assertEqual(vm.eval('result.kind'),'CREW_USE')
    vm.execute('for i=1,5 do confirm()end;assert(#c:GetBuildQueue().adds<=1)')
 def test_owner_rejects_stale_preflight_without_intent_or_debit(self):
  vm=fixture();vm.execute("prepare();c:GetBuildQueue().progress=99;local text,r,o=confirm();assert(o.status=='REJECTED'and o.phase=='PRECHECK'and C.units[20001]and C.props.SPC_CREW_ACTION_RECEIPTS_V1==nil and #c:GetBuildQueue().adds==0)")
 def test_direct_owner_and_dispatcher_reentry_do_not_repeat_irreversible_work(self):
  vm=fixture();vm.execute("""
  local original=crew.Consume;local args
  crew.Consume=function(...)args={...};return original(...)end
  prepare();local q=c:GetBuildQueue();local add=q.AddProgress
  q.AddProgress=function(...)
   local nested=original(unpack(args));assert(nested.status=='BUSY')
   local text,receipt,o=confirm();assert(o.status=='BUSY'and receipt==nil)
   return add(...)
  end
  local text,r,o=confirm();assert(o.status=='COMMITTED'and r==nil and #q.adds==1)
  """)
 def test_owner_error_object_cannot_keep_busy_or_replay_after_ambiguity(self):
  vm=fixture();vm.execute("""
  prepare();local q=c:GetBuildQueue();q.AddProgress=function(_,n)q.adds[#q.adds+1]=n;error(setmetatable({},{__tostring=function()error('BAD_ERROR_TEXT')end}))end
  local text,r,o=confirm();assert(o.status=='HELD'and o.error=='CREW_USE_ERROR'and #q.adds==1)
  local _,_,nextOutcome=confirm();assert(nextOutcome.status=='REJECTED'and #q.adds==1)
  """)

class Observers(unittest.TestCase):
 def test_localized_success_is_measured_from_type_not_english_substring(self):
  vm=fixture(True);vm.execute("""
  local run=shared.UnitActions.Run
  shared.UnitActions.Run=function(pid,p)local text,r,o=run(pid,p);return p.Action=='UNIT_ACTION_CONFIRM'and '施工完成'or text,r,o end
  local observed;crew.RecordPrecision=function(pid,r)observed=r end;SPCCrewPrecision.Start(P,shared)
  prepare();local text,r,o=confirm();assert(text=='施工完成'and r==nil and o.status=='COMMITTED')
  assert(observed.observed==260 and observed.note==nil and #c:GetBuildQueue().adds==1)
  """)
 def test_success_words_inside_held_diagnostic_never_become_success(self):
  vm=fixture(True);vm.execute("""
  crew.Consume=function()return {status='HELD',kind='CREW_USE',error='CREW CONSUMED is only diagnostic text'}end
  local observed;crew.RecordPrecision=function(pid,r)observed=r end;SPCCrewPrecision.Start(P,shared)
  prepare();local text,r,o=confirm();assert(text:find('HELD')and o.status=='HELD'and r==nil)
  assert(observed.observed==nil and observed.note:find('ACTION_NOT_COMPLETED')and C.units[20001])
  """)
 def test_actual_investment_receipt_and_outcome_survive_observer(self):
  vm=investment();vm.globals().include('CrewPrecision');vm.execute("""
  local u,t=makePreview(920);SPCCrewPrecision.Start(P,shared)
  local text,receipt,outcome=confirm(920,t)
  assert(text:find('INVESTED')and receipt.status=='COMMITTED'and outcome.kind=='INVESTMENT'and outcome.status=='COMMITTED')
  assert(receipt.cause=='INVESTMENT_COMMITTED'and shared.EffectiveFacts.Read(0,source).potential==2)
  """)
 def test_actual_inner_unknown_investment_is_held_without_rewriting_its_receipt(self):
  vm=investment();vm.execute("""
  local u,t=makePreview(921);local setter=Game.SetProperty;local once=true
  Game.SetProperty=function(o,k,v)setter(o,k,v);if once and k==T.key(source)and T.record(source).investment and T.record(source).investment.pending then once=false;u.x=u.x+1 end end
  local text,receipt,outcome=confirm(921,t)
  assert(text:find('HELD')and receipt.status=='UNKNOWN'and outcome.status=='HELD')
  local count=T.writes();for i=1,5 do confirm(921,t)end;assert(T.writes()==count)
  """)

class StaticOwnership(unittest.TestCase):
 def test_ownership_alarm_moves_to_crew_without_an_additional_writer(self):
  from refactor_static import scan,counts
  key='|PROPERTY_PRODUCER_OWNERSHIP'
  observed=counts(scan())
  self.assertEqual(observed.get('Mod/UnitActions.lua'+key,0),0)
  self.assertEqual(observed.get('Mod/CrewProjects.lua'+key,0),1)
  old={n:subprocess.check_output(['git','show',BASE+':Mod/'+n+'.lua'],cwd=ROOT,text=True)for n in ('UnitActions','CrewProjects')}
  self.assertEqual(sum(':SetProperty('in x or 'P.SetProperty('in x for x in old.values()),1)
  self.assertNotIn('SPC_CREW_ACTION_RECEIPTS_V1',(ROOT/'Mod/UnitActions.lua').read_text())
  self.assertIn("USE_RECEIPT_PROPERTY='SPC_CREW_ACTION_RECEIPTS_V1'",(ROOT/'Mod/CrewModel.lua').read_text())


class RetainedConsumption(ActualProfile,crews.Consumption):pass
class RetainedModifiers(ActualProfile,modifiers.AcceptedInjection):pass

if __name__=='__main__':unittest.main()
