"""S7d4 actual full-turn work, UNKNOWN suspension and scoped fact recovery.
Original models own receipts/cancel/completion. No native event-order proof.
"""
from contextlib import contextmanager
from hashlib import sha256
from pathlib import Path
import subprocess
import unittest
from unittest.mock import patch
from refactor_harness import Context,ROOT,TrackedLua51,SOURCES,legacy_source_observation,measure
from test_refactor_s7d1 import actual

BASE='7fc3d2167a06cdb6f68a5430b3792fc566ac1695'
KINDS=('Claim','Dialogue','Engineering')

@contextmanager
def history():
 old={ROOT/'Mod'/(n+'.lua'):subprocess.check_output(['git','show',BASE+':Mod/'+n+'.lua'],cwd=ROOT,text=True)for n in ('ClaimProjects','DialogueProjects','EngineeringStudyProjects','TimedProjects','TimedProjectModel')}
 read,execute=Path.read_text,TrackedLua51.execute
 hashes={sha256(s.encode()).hexdigest():'historical/'+BASE+'/'+str(p.relative_to(ROOT))for p,s in old.items()}
 def source(p,*a,**kw):return old[p]if p in old else read(p,*a,**kw)
 def run(vm,s,*a,**kw):
  digest=sha256(s.encode()if isinstance(s,str)else s).hexdigest()
  if digest in hashes:SOURCES[digest]=hashes[digest]
  return execute(vm,s,*a,**kw)
 with patch.object(Path,'read_text',source),patch.object(TrackedLua51,'execute',run),legacy_source_observation():yield

def fixture(kind):
 vm=actual(kind)
 vm.execute("""
 -- Settle the existing one-time GameEra access refresh before measuring work.
 Events.PlayerTurnActivated.Fire(0);pulse()
 targets,qualifications,nativeFinishes=0,0,0
 local raw=q.CurrentlyBuilding
 q.CurrentlyBuilding=function(...)
  targets=targets+1;assert(not queueUnknown,'QUEUE_UNAVAILABLE');local value=raw(...);if duringTargetRead then duringTargetRead()end;return value
 end
 local facts=shared.EffectiveFacts and shared.EffectiveFacts.Read
 if facts then shared.EffectiveFacts.Read=function(pid,city,...)
  local value=facts(pid,city,...)
  if city==c then qualifications=qualifications+1;if qualificationUnknown then value.activeStatus='UNKNOWN'end end
  return value
 end end
 local finish=q.FinishProgress
 q.FinishProgress=function(...)
  nativeFinishes=nativeFinishes+1;if callingOnly then return end;return finish(...)
 end
 function idle(n)for i=1,n do pulse()end end
 function boundary()Events.PlayerTurnDeactivated.Fire(0);Events.PlayerTurnActivated.Fire(0);pulse()end
 """)
 return vm

def next_turn(vm,kind):vm.execute('nextTurn()'if kind=='Claim'else'T.turn(1)')

class Pure(unittest.TestCase):
 def test_clock_facts_match_original_truth_table(self):
  c=Context();c.load('TimedProjectModel');c.execute("""
  for _,ended in ipairs({false,true})do for _,ending in ipairs({false,true})do for now=8,13 do
   local before='WAIT'
   if ending and now==10 then before='END'
   elseif not ending and now>10 then before=now==11 and ended and 'DUE'or 'MISSED'end
   assert(SPCTimedProjectModel.Boundary(10,ended,now,ending)==before)
  end end end
  """)
 def test_work_set_separates_pending_timers_and_recovery_without_native_access(self):
  c=Context();c.load('TimedProjects');c.execute("""
  local function cp(v)if type(v)~='table'then return v end;local out={};for k,x in pairs(v)do out[k]=cp(x)end;return out end
  w=SPCTimedProjects.WorkSet(cp)
  w.Track(0,1,'ACTIVE');w.Track(0,2,'HELD');w.Track(0,3,'CALLING');w.Track(0,4,'STOPPED')
  assert(w.Has(0,1)and w.Has(0,2)and w.Has(0,3)and not w.Has(0,4))
  assert(w.Active()['0:1']and not w.Active()['0:2']and not w.Active()['0:3'])
  local old=w.All();old['0:1'][2]=99;assert(w.All()['0:1'][2]==1)
  w.Block(0,1);assert(not w.CanRead(0,1)and not next(w.Active()))
  for i=1,1000 do w.Track(0,1,'ACTIVE')end;assert(not next(w.Active())and not next(w.TakeRecovery()))
  w.Wake(0,1);assert(not next(w.Active()));w.Track(0,1,'ACTIVE')
  assert(w.TakeRecovery()['0:1']and not next(w.TakeRecovery()))
  w.Block(0,1);w.Wake(0,1);w.Block(0,1);assert(not next(w.TakeRecovery()))
  w.Wake(0,1);w.Forget(0,1);assert(not w.Has(0,1)and not next(w.TakeRecovery()))
  """)

class Work(unittest.TestCase):
 def test_unknown_stops_all_turn_retries_and_silent_recovery_does_not_restart(self):
  for kind in KINDS:
   with self.subTest(owner=kind):
    vm=fixture(kind);vm.execute("""
    local before=snapshot();queueUnknown=true;changed();assert(snapshot()==before and pending().stage=='ACTIVE')
    local n=targets;local f=nativeFinishes;idle(1000);for i=1,10 do boundary()end
    assert(targets==n and nativeFinishes==f and snapshot()==before,'UNKNOWN_TURN_RETRY')
    queueUnknown=false;for i=1,10 do boundary()end
    assert(targets==n and nativeFinishes==f and snapshot()==before,'SILENT_RECOVERY_RETRIED')
    changed();assert(targets>n and pending().stage=='ACTIVE')
    Events.PlayerTurnDeactivated.Fire(0)
    """);next_turn(vm,kind);vm.execute('pulse();assert(finished()and nativeFinishes==1)')
 def test_real_turns_do_not_retry_or_erase_unknown_round_and_late_recovery_does_not_backfill(self):
  for kind in KINDS:
   with self.subTest(owner=kind):
    vm=fixture(kind);vm.execute('queueUnknown=true;changed();local n=targets;blockedTargets=n')
    for _ in range(3):vm.execute('Events.PlayerTurnDeactivated.Fire(0)');next_turn(vm,kind)
    vm.execute("assert(targets==blockedTargets and pending().stage=='ACTIVE'and not finished());queueUnknown=false;changed();assert(not finished()and nativeFinishes==0 and (not pending()or pending().stage=='STOPPED'))")
 def test_reliable_event_after_due_boundary_recovers_in_same_window_once(self):
  for kind in KINDS:
   with self.subTest(owner=kind):
    vm=fixture(kind);vm.execute('Events.PlayerTurnDeactivated.Fire(0);queueUnknown=true')
    next_turn(vm,kind)
    vm.execute("""
    pulse();assert(pending().stage=='ACTIVE'and nativeFinishes==0)
    local n=targets;queueUnknown=false;idle(1000);assert(targets==n and nativeFinishes==0)
    changed();assert(finished()and nativeFinishes==1)
    changed();idle(1000);assert(nativeFinishes==1)
    """)
 def test_calling_is_not_timer_work_or_a_native_replay(self):
  for kind in KINDS:
   with self.subTest(owner=kind):
    vm=fixture(kind);vm.execute('callingOnly=true;Events.PlayerTurnDeactivated.Fire(0)');next_turn(vm,kind)
    vm.execute("""
    pulse();assert(pending().stage=='CALLING'and nativeFinishes==1)
    local t,q0,f=targets,qualifications,nativeFinishes
    for i=1,10 do boundary()end;idle(1000)
    assert(targets==t and qualifications==q0 and nativeFinishes==f,'CALLING_WAS_TIMED_OR_REPLAYED')
    q.target='NORMAL';changed();assert(not pending()or pending().stage=='STOPPED'or pending().stage=='CALLING')
    assert(nativeFinishes==1)
    """)
 def test_held_completion_is_not_timer_work_or_resampled(self):
  for kind in ('Dialogue','Engineering'):
   with self.subTest(owner=kind):
    vm=fixture(kind);vm.execute("""
    brokenSample=true;q.target=nil;q.GetSize=function()return 0 end
    local index=P.Info('Projects',project).Index;Events.CityProjectCompleted.Fire(0,c:GetID(),index);pulse()
    assert(pending().stage=='HELD');local before=snapshot();local t,q0=targets,qualifications
    for i=1,10 do boundary()end;idle(1000)
    assert(targets==t and qualifications==q0 and snapshot()==before and nativeFinishes==0,'HELD_WAS_TIMED')
    """)
 def test_unrelated_city_or_player_never_wakes_blocked_round(self):
  for kind in KINDS:
   vm=fixture(kind);vm.execute("""
   queueUnknown=true;changed();local n=targets;queueUnknown=false
   Events.CityProductionChanged.Fire(3,c:GetID());changed(999)
   idle(1000);for i=1,10 do boundary()end
   assert(targets==n and nativeFinishes==0 and pending().stage=='ACTIVE')
   """)
 def test_global_governor_or_era_display_refresh_does_not_rearm_queue_unknown(self):
  for kind in ('Dialogue','Engineering'):
   vm=fixture(kind);vm.execute("""
   queueUnknown=true;changed();local n=targets;queueUnknown=false
   Events.GovernorPromoted.Fire(0);pulse();blockedTargets=n;assert(targets==n and pending().stage=='ACTIVE')
   """)
   if kind=='Dialogue':vm.execute("GameEra='ERA_MEDIEVAL';Events.PlayerTurnActivated.Fire(0);pulse();assert(targets==blockedTargets)")
 def test_qualification_unknown_needs_related_fact_recovery(self):
  for kind in ('Dialogue','Engineering'):
   vm=fixture(kind);vm.execute("""
   qualificationUnknown=true;changed();local before=snapshot();local n=qualifications
   for i=1,10 do boundary()end;idle(1000)
   assert(qualifications==n and snapshot()==before and nativeFinishes==0)
   qualificationUnknown=false
   for i=1,10 do boundary()end;assert(qualifications==n and nativeFinishes==0)
   """)
   vm.execute("dp.RefreshAccess(0,c:GetID())"if kind=='Dialogue'else"study.Refresh(0,c:GetID())")
   vm.execute('Events.PlayerTurnDeactivated.Fire(0)');next_turn(vm,kind);vm.execute('pulse();assert(finished()and nativeFinishes==1)')

class Reentry(unittest.TestCase):
 def test_unknown_fact_during_target_getter_cannot_commit_an_end_boundary(self):
  for kind in KINDS:
   with self.subTest(owner=kind):
    vm=fixture(kind);vm.execute("""
    local before=snapshot()
    duringTargetRead=function()duringTargetRead=nil;queueUnknown=true;changed()end
    Events.PlayerTurnDeactivated.Fire(0);pulse()
    assert(snapshot()==before,'STALE_READ_COMMITTED_AFTER_NEW_UNKNOWN')
    local n=targets;for i=1,10 do boundary()end;assert(targets==n and nativeFinishes==0)
    queueUnknown=false;changed();Events.PlayerTurnDeactivated.Fire(0)
    """);next_turn(vm,kind);vm.execute('pulse();assert(finished()and nativeFinishes==1)')


class Scope(unittest.TestCase):
 def test_two_pending_study_cities_recover_independently_without_reading_sibling(self):
  vm=fixture('Engineering');vm.execute("""
  other=H.city(2);other.buildings[10]=true;H.district(other,'DISTRICT_INDUSTRIAL_ZONE',true)
  for i=1,3 do T.invest(other,9000+i)end;S.queue(other);S.begin(other)
  local oq=other:GetBuildQueue();local get=oq.CurrentlyBuilding;otherTargets=0;otherUnknown=true
  oq.CurrentlyBuilding=function(...)otherTargets=otherTargets+1;assert(not otherUnknown,'OTHER_QUEUE_UNKNOWN');return get(...)end
  Events.CityProductionChanged.Fire(0,other:GetID());pulse();queueUnknown=true;changed()
  local n,m=targets,otherTargets
  for i=1,10 do boundary()end;assert(targets==n and otherTargets==m)
  queueUnknown=false;changed();assert(targets>n and otherTargets==m)
  assert(S.state(other).value.pending.stage=='ACTIVE'and S.finishes(other)==0)
  otherUnknown=false;Events.CityProductionChanged.Fire(0,other:GetID());pulse();assert(otherTargets>m)
  Events.PlayerTurnDeactivated.Fire(0);T.turn(1);pulse()
  assert(S.L(c)==1 and S.L(other)==1 and S.finishes(c)==1 and S.finishes(other)==1)
  """)
 def test_confirmed_qualification_loss_withdraws_blocked_attempt_without_queue_recovery(self):
  for kind in ('Dialogue','Engineering'):
   vm=fixture(kind);vm.execute('queueUnknown=true;changed();local n=targets;blockedTargets=n')
   vm.execute("T.governor(1);Events.GovernorChanged.Fire(0);pulse();assert(not pending()and targets==blockedTargets and nativeFinishes==0)")


class Differential(unittest.TestCase):
 def test_turn_work_before_after_and_unchanged_records(self):
  rows=[]
  for kind in KINDS:
   values=[]
   for old in (True,False):
    with history()if old else __import__('contextlib').nullcontext():
     vm=fixture(kind);vm.execute("queueUnknown=true;changed();before=snapshot();local n=targets;for i=1,10 do boundary()end;result=targets-n;assert(snapshot()==before)")
     values.append(vm.eval('result'))
   self.assertGreater(values[0],0);self.assertEqual(values[1],0)
   rows.append({'owner':kind,'before_queue_targets':values[0],'after_queue_targets':values[1]})
  measure('S7d4_unknown_turn_work',{'baseline':BASE,'same_clock_turn_boundaries':20,'rows':rows,'unchanged_saved_round':True,'native_CPU_or_memory_claim':False})

if __name__=='__main__':unittest.main()
