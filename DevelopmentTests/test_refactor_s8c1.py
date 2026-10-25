"""S8c1 actual Store/RuntimeWork completion ownership; no ownership gameplay change."""
from contextlib import contextmanager,nullcontext
from hashlib import sha256
from pathlib import Path
import subprocess
import unittest
from unittest.mock import patch
from refactor_harness import ROOT,TrackedLua51,SOURCES,legacy_source_observation,measure,Context
from test_refactor_s7f import actual_store

BASE='0d339aaf6e5a1ebb9c22cef84c98eb3abae691c4'
@contextmanager
def history():
 original={ROOT/'Mod'/(n+'.lua'):subprocess.check_output(['git','show',BASE+':Mod/'+n+'.lua'],cwd=ROOT,text=True)for n in ('RuntimeWork','CityProgressionStore')}
 read,execute=Path.read_text,TrackedLua51.execute;hashes={sha256(s.encode()).hexdigest():'historical/'+BASE+'/'+str(p.relative_to(ROOT))for p,s in original.items()}
 def source(p,*a,**kw):return original[p]if p in original else read(p,*a,**kw)
 def run(vm,s,*a,**kw):
  h=sha256(s.encode()if isinstance(s,str)else s).hexdigest()
  if h in hashes:SOURCES[h]=hashes[h]
  return execute(vm,s,*a,**kw)
 with patch.object(Path,'read_text',source),patch.object(TrackedLua51,'execute',run),legacy_source_observation():yield

SETUP="""
ca,cb=a,b;originID=ca:GetID();tries=0;canClean=false;cleaned=false;errors={};tickets={};losses={}
for owner=9,10 do Players[owner]={GetCities=function()return {
 FindID=function(_,id)for _,c in ipairs({ca,cb})do if c:GetID()==id then return c end end end,
 Members=function()return ipairs({ca,cb})end}end}end
jobs=SPCRuntimeWork.NewTargets(P,shared,function()error('POSITIVE_VISIT_FORBIDDEN')end,function(pid,cid,why)errors[pid..':'..cid]=why end)
function cleanup(c,loss)
 tries=tries+1;if replacement then local fn=replacement;replacement=nil;fn(c,loss)end
 if not canClean then error('NATIVE_CLEANUP_UNAVAILABLE')end
 cleaned=true
end
wrapped=jobs.Exit(cleanup,'Async')
shared.CityProgressionStore.RegisterExit('Async',function(c,loss,ticket)
 tickets[c]=ticket;losses[c]=M.Copy(loss);return wrapped(c,loss,ticket)
end)
function lose(c,id)T.loss(c,9,id)end
function retry()jobs.Retry({player=9,city=900})end
function status(c)return shared.CityProgressionStore.Status(c or ca).exitStatus end
"""
def fixture():
 vm=actual_store();vm.execute(SETUP);return vm


class Completion(unittest.TestCase):
 def test_async_cleanup_after_budget_exhaustion_acknowledges_actual_store_before_counterexample(self):
  values=[]
  for old in (True,False):
   with history()if old else nullcontext():vm=fixture()
   vm.execute("lose(ca,900);shared.CityProgressionStore.ExitConfirmed();shared.CityProgressionStore.ExitConfirmed();assert(tries==3 and status()=='PARTIAL_HELD');canClean=true;retry();assert(tries==4 and cleaned and next(jobs.exits)==nil);result=status()")
   values.append(vm.eval('result'))
  self.assertEqual(values,['PARTIAL_HELD','WITHDRAWN'])
  measure('S8c1_async_cleanup_completion',{'before':'cleaned but Store PARTIAL_HELD after3 attempts','after':'same cleanup readback acknowledges current exact loss','additional_native_cleanup_calls':1,'gameplay_or_saved_schema_change':False})
 def test_stable_ticket_three_attempt_budget_and_successful_siblings_never_rerun(self):
  vm=fixture();vm.execute("""
  bridgeCalls,siblingCalls=0,0
  shared.CityProgressionStore.RegisterExit('NetworkBridge',function()bridgeCalls=bridgeCalls+1 end)
  shared.CityProgressionStore.RegisterExit('Sibling',function()siblingCalls=siblingCalls+1 end)
  lose(ca,900);local ticket=tickets[ca]
  for i=1,100 do shared.CityProgressionStore.ExitConfirmed();assert(tickets[ca]==ticket)end
  assert(tries==3 and bridgeCalls==1 and siblingCalls==1 and status()=='PARTIAL_HELD')
  local writes=T.writes();for i=1,1000 do Events.GameCoreEventPublishComplete.Fire()end
  assert(tries==3 and T.writes()==writes)
  canClean=true;retry();assert(status()=='WITHDRAWN')
  assert(shared.CityProgressionStore.ExitCompleted('Async',ca,losses[ca],ticket))
  shared.CityProgressionStore.ExitConfirmed();assert(tries==4 and bridgeCalls==1 and siblingCalls==1)
  """)
 def test_wrong_label_worker_ticket_native_reference_or_unknown_getter_rejected(self):
  vm=fixture();vm.execute("""
  lose(ca,900);lose(cb,901);local s=shared.CityProgressionStore
  assert(not s.ExitCompleted('Missing',ca,losses[ca],tickets[ca]))
  assert(not s.ExitCompleted('Async',ca,losses[ca],tickets[cb]))
  assert(not s.ExitCompleted('Async',cb,losses[ca],tickets[ca]))
  ca.s.ref.cityID=999;assert(not s.ExitCompleted('Async',ca,losses[ca],tickets[ca]));ca.s.ref.cityID=900
  local get=ca.GetX;ca.GetX=function()error('NATIVE_UNKNOWN')end
  assert(not s.ExitCompleted('Async',ca,losses[ca],tickets[ca]));ca.GetX=get
  assert(status()=='PARTIAL_HELD')
  """)
 def test_old_ticket_cannot_complete_identical_looking_later_loss(self):
  vm=fixture();vm.execute("""
  lose(ca,900);local first=tickets[ca];local loss=M.Copy(losses[ca]);canClean=true;retry();assert(status()=='WITHDRAWN')
  ca.s.ref.owner=0;ca.s.ref.cityID=originID;Events.CityTransfered.Fire(0,originID,9)
  assert(T.record(ca).stage=='ACTIVE')
  canClean=false;lose(ca,900);assert(tickets[ca]~=first and T.encode(losses[ca])==T.encode(loss))
  assert(not shared.CityProgressionStore.ExitCompleted('Async',ca,loss,tickets[cb]or first)and status()=='PARTIAL_HELD')
  """)
 def test_ticket_survives_same_loss_private_storage_revision(self):
  vm=fixture();vm.execute("lose(ca,900);local ticket=tickets[ca];local n=T.normal(T.record(ca));assert(T.write(ca,n));canClean=true;retry();assert(tickets[ca]==ticket and status()=='WITHDRAWN')")
 def test_commit_boundary_does_not_accept_completion(self):
  vm=fixture();vm.execute("""
  lose(ca,900);local key=T.key(ca);local set=Game.SetProperty;acks=0
  Game.SetProperty=function(o,k,v)if k==key then acks=acks+1;assert(not shared.CityProgressionStore.ExitCompleted('Async',ca,losses[ca],tickets[ca]))end;return set(o,k,v)end
  assert(T.write(ca,T.normal(T.record(ca)))and acks==1 and status()=='PARTIAL_HELD')
  """)
 def test_false_and_unprintable_cleanup_do_not_finish_or_latch_busy(self):
  for mode in ('false','unprintable'):
   vm=fixture();vm.execute("mode=...;shared.CityProgressionStore.RegisterExit('Fault',function()if recovered then return true end;if mode=='false'then return false end;error(setmetatable({},{__tostring=function()error('FORMAT_FAILED')end}))end);lose(ca,900);assert(status()=='PARTIAL_HELD');recovered=true;canClean=true;shared.CityProgressionStore.ExitConfirmed();assert(status()=='WITHDRAWN')",mode)
 def test_ack_during_running_callback_waits_for_successful_return_and_blocks_recapture(self):
  for mode in ('false','throw'):
   vm=actual_store();vm.execute("""
   ca,cb=a,b;local original=ca:GetID();attempts=0;mode=...
   shared.CityProgressionStore.RegisterExit('Provisional',function(c,loss,ticket)
    attempts=attempts+1;assert(shared.CityProgressionStore.ExitCompleted('Provisional',c,loss,ticket))
    ca.s.ref.owner=0;ca.s.ref.cityID=original;Events.CityTransfered.Fire(0,original,9)
    assert(T.record(ca).stage=='HELD_TRANSFER')
    ca.s.ref.owner=9;ca.s.ref.cityID=900
    if mode=='false'then return false end;error('AFTER_ACK_FAILED')
   end)
   T.loss(ca,9,900);assert(attempts==1 and shared.CityProgressionStore.Status(ca).exitStatus=='PARTIAL_HELD')
   """,mode)
 def test_network_first_and_new_registration_cannot_be_hidden_by_old_snapshot(self):
  vm=actual_store();vm.execute("""
  ca=a;order={}
  shared.CityProgressionStore.RegisterExit('ZLast',function()order[#order+1]='ZLast';shared.CityProgressionStore.RegisterExit('New',function()order[#order+1]='New'end)end)
  shared.CityProgressionStore.RegisterExit('NetworkBridge',function()order[#order+1]='NetworkBridge'end)
  shared.CityProgressionStore.RegisterExit('AFirst',function()order[#order+1]='AFirst'end)
  T.loss(ca,9,900);assert(table.concat(order,',')=='NetworkBridge,AFirst,ZLast'and shared.CityProgressionStore.Status(ca).exitStatus=='PARTIAL_HELD')
  shared.CityProgressionStore.ExitConfirmed();assert(order[4]=='New'and #order==4 and shared.CityProgressionStore.Status(ca).exitStatus=='WITHDRAWN')
  """)

 def test_native_post_callback_read_cannot_finish_a_later_identical_loss(self):
  vm=actual_store();vm.execute("""
  local c=a;local original=c:GetID();local store=shared.CityProgressionStore
  calls=0;once=true;callbackDone=false
  store.RegisterExit('Cycle',function(city,loss,ticket)
   calls=calls+1;receipt=M.Copy(loss);cap=ticket;callbackDone=true
  end)
  local get=c.GetOwner
  c.GetOwner=function(city)
   if callbackDone and once then
    once=false;assert(store.ExitCompleted('Cycle',city,receipt,cap))
    city.s.ref.owner=0;city.s.ref.cityID=original;Events.CityTransfered.Fire(0,original,9)
    assert(T.record(city).stage=='ACTIVE')
    city.s.ref.owner=9;city.s.ref.cityID=900;Events.CityTransfered.Fire(9,900,0)
    assert(T.record(city).stage=='HELD_TRANSFER')
   end
   return get(city)
  end
  T.loss(c,9,900)
  assert(calls==1 and T.record(c).ownerChanges==2 and store.Status(c).exitStatus~='WITHDRAWN')
  store.ExitConfirmed()
  assert(calls==2 and T.record(c).ownerChanges==2 and store.Status(c).exitStatus=='WITHDRAWN')
  """)
 def test_opaque_ticket_equality_metamethod_cannot_forge_completion(self):
  vm=fixture();vm.execute("""
  lose(ca,900);local mt={__eq=function()return true end}
  setmetatable(tickets[ca],mt);local forged=setmetatable({},mt)
  assert(not shared.CityProgressionStore.ExitCompleted('Async',ca,losses[ca],forged))
  assert(status()=='PARTIAL_HELD');canClean=true;retry();assert(status()=='WITHDRAWN')
  """)
 def test_initial_native_lookup_reentry_cannot_recurse_exit_or_duplicate_cleanup(self):
  vm=actual_store();vm.execute("""
  calls,lookups=0,0;local s=shared.CityProgressionStore
  s.RegisterExit('Once',function()calls=calls+1 end)
  local get=CityManager.GetCityAt
  CityManager.GetCityAt=function(...)
   lookups=lookups+1;assert(lookups<20);s.ExitConfirmed();return get(...)
  end
  T.loss(a,9,900);assert(calls==1 and lookups<20 and s.Status(a).exitStatus=='WITHDRAWN')
  """)

 def test_collection_fault_inside_native_ack_reference_read_cannot_finish(self):
  vm=fixture();vm.execute("""
  lose(ca,900);local fresh=T.fresh(3);local get=ca.GetOwner;local once=true
  ca.GetOwner=function(c)
   if once then once=false;T.failKey(SPCCityProgressionStore.INDEX);T.register(fresh)end
   return get(c)
  end
  assert(not shared.CityProgressionStore.ExitCompleted('Async',ca,losses[ca],tickets[ca]))
  assert(shared.CityProgressionStore.FailureReport()and shared.CityProgressionStore.Status(ca).fault)
  """)
 def test_collection_fault_after_successful_exit_callback_cannot_publish_completion(self):
  vm=actual_store();vm.execute("""
  local fresh=T.fresh(3);local get=a.GetOwner;local once=true;local done=false;local s=shared.CityProgressionStore
  s.RegisterExit('FaultDuringRead',function()done=true end)
  a.GetOwner=function(c)
   if once and done then once=false;T.failKey(SPCCityProgressionStore.INDEX);T.register(fresh)end
   return get(c)
  end
  T.loss(a,9,900);assert(done and s.FailureReport()and s.Status(a).exitStatus~='WITHDRAWN')
  """)


class TargetOwnership(unittest.TestCase):
 def test_same_key_exit_replacement_during_direct_cleanup_is_not_erased(self):
  vm=fixture();vm.execute("""
  replacement=function(c,loss)
   newer=jobs.Exit(function()if newReady then return true end;return false end,'Async')
   assert(not pcall(newer,c,loss,tickets[c]))
  end
  canClean=true;lose(ca,900);assert(status()=='PARTIAL_HELD'and jobs.exits['9:900'])
  newReady=true;retry();assert(status()=='WITHDRAWN'and not jobs.exits['9:900'])
  """)
 def test_same_key_replacement_during_retry_is_deferred_and_not_reported_as_old_success(self):
  vm=fixture();vm.execute("""
  lose(ca,900);canClean=true
  replacement=function(c,loss)
   newer=jobs.Exit(function()if newReady then return true end;return false end,'Async')
   assert(not pcall(newer,c,loss,tickets[c]))
  end
  retry();assert(status()=='PARTIAL_HELD'and jobs.exits['9:900'])
  newReady=true;retry();assert(status()=='WITHDRAWN'and not jobs.exits['9:900'])
  """)
 def test_replacement_during_native_ack_reference_read_cannot_finish_old_work(self):
  vm=fixture();vm.execute("""
  lose(ca,900);canClean=true;local owner=ca.GetOwner;local once=true
  ca.GetOwner=function(c)
   if once and cleaned then once=false
    local newer=jobs.Exit(function()return newReady==true end,'Async')
    assert(not pcall(newer,ca,losses[ca],tickets[ca]))
   end
   return owner(c)
  end
  retry();assert(status()=='PARTIAL_HELD'and jobs.exits['9:900'])
  newReady=true;retry();assert(status()=='WITHDRAWN'and not jobs.exits['9:900'])
  """)
 def test_replaced_entry_during_resolve_cannot_run_stale_cleanup(self):
  vm=fixture();vm.execute("""
  lose(ca,900);canClean=true;local owner=ca.GetOwner;local once=true;local before=tries
  ca.GetOwner=function(c)
   if once then once=false
    local newer=jobs.Exit(function()return false end,'Async')
    assert(not pcall(newer,ca,losses[ca],tickets[ca]))
   end
   return owner(c)
  end
  retry();assert(tries==before and not cleaned and jobs.exits['9:900']and status()=='PARTIAL_HELD')
  """)
 def test_missing_modern_ack_or_ticket_or_failed_ack_keeps_pending_work(self):
  for mode in ('missing','throw','false','ticket'):
   vm=fixture();vm.execute("""
   lose(ca,900);canClean=true;local ack=shared.CityProgressionStore.ExitCompleted;mode=...
   if mode=='missing'then shared.CityProgressionStore.ExitCompleted=nil
   elseif mode=='throw'then shared.CityProgressionStore.ExitCompleted=function()error('ACK_UNAVAILABLE')end
   elseif mode=='false'then shared.CityProgressionStore.ExitCompleted=function()return false end
   else jobs.exits['9:900'].ticket=nil end
   retry();assert(jobs.exits['9:900']and status()=='PARTIAL_HELD')
   shared.CityProgressionStore.ExitCompleted=ack
   if mode=='ticket'then shared.CityProgressionStore.ExitConfirmed()else retry()end
   assert(status()=='WITHDRAWN'and not jobs.exits['9:900'])
   """,mode)
 def test_unprintable_async_failure_and_new_pending_during_report_remain_isolated(self):
  vm=fixture();vm.execute("lose(ca,900);local e=jobs.exits['9:900'];e.fn=function()error(setmetatable({},{__tostring=function()error('FORMAT_FAILED')end}))end;retry();assert(jobs.exits['9:900']==e and status()=='PARTIAL_HELD')")
  c=Context();c.load('RuntimeWork');c.execute("""
  P={IsTestPlayer=function()return true end,Count=function()end};local city={GetOwner=function()return 0 end,GetID=function()return 1 end}
  Players={[0]={GetCities=function()return {FindID=function()return city end}end}}
  local t;local replaced=false;t=SPCRuntimeWork.NewTargets(P,shared,function()end,function(_,_,why)
   if why==nil and not replaced then replaced=true
    local newer=t.Exit(function()error('NEW_PENDING')end);assert(not pcall(newer,city,{}));t.pending['0:1']={owner=0,city=1}
   end
  end)
  local first=t.Exit(function()error('FIRST_PENDING')end);pcall(first,city,{})
  t.exits['0:1'].fn=function()return true end;t.Retry({player=0,city=1})
  assert(replaced and t.exits['0:1']and t.pending['0:1'])
  """)

if __name__=='__main__':unittest.main()
