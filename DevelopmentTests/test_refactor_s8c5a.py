"""S8c5a read-only current-loss proof and explicit target group adapter; actual Store."""
import unittest
from refactor_harness import measure
from test_refactor_s8c1 import fixture

SETUP="""
canClean=true;s=shared.CityProgressionStore;groupA=false;groupB=false;groupCallsA=0;groupCallsB=0;adapterCallsA=0;adapterCallsB=0;aggregateAcks=0
jobsA=SPCRuntimeWork.NewTargets(P,shared,function()error('POSITIVE_A_FORBIDDEN')end,function()end)
jobsB=SPCRuntimeWork.NewTargets(P,shared,function()error('POSITIVE_B_FORBIDDEN')end,function()end)
local complete=s.ExitCompleted;s.ExitCompleted=function(name,...)
 if name=='Composite'then aggregateAcks=aggregateAcks+1 end;return complete(name,...)
end
function groupAdapter(which,c,loss,ticket,current)
 if which=='a'then adapterCallsA=adapterCallsA+1 else adapterCallsB=adapterCallsB+1 end
 assert(current()and s.IsExitCurrent('Composite',c,loss,ticket,current))
 if adapterFailure=='false'then return false elseif adapterFailure=='nil'then return nil
 elseif adapterFailure=='throw'then error(setmetatable({},{__tostring=function()error('FORMAT_UNKNOWN')end}))end
 if replacement then local replace=replacement;replacement=nil;replace(c,loss,ticket)end
 if which=='a'then doneA=true else doneB=true end
 if doneA and doneB then return s.ExitCompleted('Composite',c,loss,ticket,current)end
 return true -- group success, intentionally no aggregate acknowledgement yet
end
adapterA=function(...)return groupAdapter('a',...)end;adapterB=function(...)return groupAdapter('b',...)end
wrappedA=jobsA.Exit(function()groupCallsA=groupCallsA+1;return groupA end,'Composite',adapterA)
wrappedB=jobsB.Exit(function()groupCallsB=groupCallsB+1;return groupB end,'Composite',adapterB)
s.RegisterExit('Composite',function(c,loss,ticket)
 if not rawequal(lastTicket,ticket)then lastTicket=ticket;doneA=false;doneB=false end
 lastLoss=M.Copy(loss)
 local a=pcall(wrappedA,c,loss,ticket);local b=pcall(wrappedB,c,loss,ticket)
 assert(a and b,'GROUPS_STILL_PENDING')
end)
function retryA()jobsA.Retry({player=9,city=900})end
function retryB()jobsB.Retry({player=9,city=900})end
"""
def grouped():
 v=fixture();v.execute(SETUP);return v


class ReadOnlyProof(unittest.TestCase):
 def test_current_proof_is_readonly_and_cannot_finish_or_allow_return(self):
  v=fixture();v.execute("""
  lose(ca,900);local writes=T.writes();local triesBefore=tries
  for i=1,1000 do assert(shared.CityProgressionStore.IsExitCurrent('Async',ca,losses[ca],tickets[ca]))end
  assert(tries==triesBefore and T.writes()==writes and status()=='PARTIAL_HELD')
  ca.s.ref.owner=0;ca.s.ref.cityID=originID;Events.CityTransfered.Fire(0,originID,9)
  assert(T.record(ca).stage=='HELD_TRANSFER')
  """)
 def test_wrong_name_forged_ticket_and_predicate_failure_cannot_prove_current(self):
  v=fixture();v.execute("""
  lose(ca,900);local s=shared.CityProgressionStore;local mt={__eq=function()return true end};setmetatable(tickets[ca],mt)
  assert(not s.IsExitCurrent('Async',ca,losses[ca],setmetatable({},mt)))
  assert(not s.IsExitCurrent('Wrong',ca,losses[ca],tickets[ca]))
  assert(not s.IsExitCurrent('Async',ca,losses[ca],tickets[ca],function()return false end))
  assert(not s.IsExitCurrent('Async',ca,losses[ca],tickets[ca],function()error('PREDICATE_FAILED')end))
  assert(status()=='PARTIAL_HELD')
  """)
 def test_readonly_proof_rejects_native_reference_and_commit_boundary(self):
  v=fixture();v.execute("""
  lose(ca,900);local s=shared.CityProgressionStore;local get=ca.GetX;ca.GetX=function()error('REFERENCE_UNKNOWN')end
  assert(not s.IsExitCurrent('Async',ca,losses[ca],tickets[ca]));ca.GetX=get
  local set=Game.SetProperty;local key=T.key(ca);checked=0
  Game.SetProperty=function(o,k,value)if k==key then checked=checked+1;assert(not s.IsExitCurrent('Async',ca,losses[ca],tickets[ca]))end;return set(o,k,value)end
  assert(T.write(ca,T.normal(T.record(ca)))and checked==1)
  """)


class GroupAdapters(unittest.TestCase):
 def test_two_independent_retries_after_budget_require_both_groups_to_ack_aggregate(self):
  v=grouped();v.execute("""
  lose(ca,900);s.ExitConfirmed();s.ExitConfirmed()
  assert(groupCallsA==3 and groupCallsB==3 and status()=='PARTIAL_HELD')
  groupA=true;retryA()
  assert(doneA and not doneB and aggregateAcks==0 and status()=='PARTIAL_HELD'and not jobsA.exits['9:900']and jobsB.exits['9:900'])
  groupB=true;retryB()
  assert(doneA and doneB and aggregateAcks==1 and status()=='WITHDRAWN'and not jobsB.exits['9:900'])
  local a,b=groupCallsA,groupCallsB;s.ExitConfirmed();for i=1,1000 do Events.GameCoreEventPublishComplete.Fire()end
  assert(groupCallsA==a and groupCallsB==b and aggregateAcks==1)
  """)
  measure('S8c5a_explicit_group_ack',{'actual_modules':'Store/RuntimeWork','groups':2,'Store_attempts_before_independent_recovery':3,'aggregate_ACK_after_first_group':0,'aggregate_ACK_after_second_group':1,'production_legacy_wiring':'NOT_YET_CHANGED'})
 def test_relabel_without_adapter_is_a_confirmed_rejected_composition(self):
  v=grouped();v.execute("""
  wrappedA=jobsA.Exit(function()return groupA end,'Composite')
  lose(ca,900);groupA=true;retryA()
  assert(status()=='WITHDRAWN'and jobsB.exits['9:900']and not groupB)
  """)
  measure('S8c5a_rejected_direct_relabel',{'constructed_composition':'A target directly ACKs Composite without group adapter','premature_aggregate_completion':True,'approved_production_use':False})
 def test_adapter_false_nil_and_unprintable_error_keep_target_pending(self):
  for mode in ('false','nil','throw'):
   v=grouped();v.execute("lose(ca,900);groupA=true;adapterFailure=...;retryA();assert(jobsA.exits['9:900']and status()=='PARTIAL_HELD'and aggregateAcks==0);adapterFailure=nil;retryA();assert(not jobsA.exits['9:900']and doneA and not doneB and aggregateAcks==0)",mode)
 def test_missing_readonly_api_or_wrong_ticket_never_runs_adapter_or_drops_work(self):
  for mode in ('missing','ticket'):
   v=grouped();v.execute("""
   lose(ca,900);groupA=true;local proof=s.IsExitCurrent;local ticket=jobsA.exits['9:900'].ticket;mode=...
   if mode=='missing'then s.IsExitCurrent=nil else jobsA.exits['9:900'].ticket={}end
   retryA();assert(adapterCallsA==0 and jobsA.exits['9:900']and aggregateAcks==0 and status()=='PARTIAL_HELD')
   s.IsExitCurrent=proof;jobsA.exits['9:900'].ticket=ticket;retryA();assert(adapterCallsA==1 and not jobsA.exits['9:900'])
   """,mode)
 def test_newer_pending_inside_adapter_is_preserved(self):
  v=grouped();v.execute("""
  lose(ca,900);groupA=true;jobsA.pending['9:900']={owner=9,city=900};local old=jobsA.pending['9:900']
  replacement=function()jobsA.pending['9:900']={owner=9,city=900}end
  retryA();assert(not jobsA.exits['9:900']and jobsA.pending['9:900']and jobsA.pending['9:900']~=old and status()=='PARTIAL_HELD')
  """)
 def test_replaced_slot_during_proof_cannot_run_old_adapter(self):
  v=grouped();v.execute("""
  lose(ca,900);groupA=true;local get=ca.GetOwner;local once=true;wasCleaned=false
  jobsA.exits['9:900'].fn=function()wasCleaned=true;return true end
  ca.GetOwner=function(c)
   if once and wasCleaned then once=false;local newer=jobsA.Exit(function()return newReady==true end,'Composite',adapterA);assert(not pcall(newer,ca,lastLoss,lastTicket))end
   return get(c)
  end
  retryA();assert(adapterCallsA==0 and jobsA.exits['9:900']and status()=='PARTIAL_HELD')
  newReady=true;retryA();assert(adapterCallsA==1 and not jobsA.exits['9:900']and status()=='PARTIAL_HELD')
  """)
 def test_named_function_adapter_is_required_at_creation(self):
  v=grouped();v.execute("assert(not pcall(jobsA.Exit,function()end,nil,adapterA));assert(not pcall(jobsA.Exit,function()end,'Composite','INVALID'))")

if __name__=='__main__':unittest.main()
