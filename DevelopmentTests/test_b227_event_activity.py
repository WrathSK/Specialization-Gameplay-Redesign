"""B227 actual Lua: no hidden-context frames, bounded event transitions and unarmed expiry."""
import unittest
from pathlib import Path
from test_expedition_spy_activity_ui import bridge
from test_expedition_spy_activity_integration import integrated
from test_expedition_spy_persistence import fixture


def events(l, count=4):
    l.execute(f"for i=1,{count} do Events.GameCoreEventPublishComplete()end")

class EventActivity(unittest.TestCase):
    def ready(self):
        l=bridge(with_trace=True)
        l.execute("refreshAuto=false;nativeAuto=false;ContextPtr.RequestRefresh=function()error('FRAME_DEPENDENCY')end;ContextPtr.SetUpdate=function()error('TIMER_DEPENDENCY')end")
        return l
    def test_no_frame_or_timer_dependency_one_pass_per_event(self):
        l=self.ready();l.execute("publish('SLEEP');assert(arms==1 and sleepCalls==0 and #packets==0)")
        events(l,1);l.execute("assert(sleepCalls==1 and #packets==0)")
        events(l,1);l.execute("assert(packets[1].Result=='ASLEEP' and not update)")
        l.execute("publish('RELEASE',true);assert(wakeCalls==1 and #packets==1)")
        events(l,1);l.execute("assert(packets[2].Result=='RELEASED')")
        events(l,20);l.execute("assert(sleepCalls==1 and wakeCalls==1)")
    def test_no_arm_readback_no_native_write(self):
        l=self.ready();l.execute("noArmAck=true;publish('SLEEP')");events(l,20)
        l.execute("assert(arms==1 and sleepCalls==0 and #packets==0)")
    def test_busy_waits_for_real_event(self):
        l=self.ready();l.execute("coreBusy=true;publish('SLEEP');assert(arms==0 and sleepChecks==0);coreBusy=false;assert(arms==0)")
        events(l);l.execute("assert(sleepCalls==1 and packets[1].Result=='ASLEEP')")
    def test_denial_never_forces_sleep(self):
        l=self.ready();l.execute("sleepDenied=true;publish('SLEEP');assert(packets[1].Result=='REJECTED' and sleepCalls==0)")
    def test_operation_pending_until_real_activity_event(self):
        l=self.ready();l.execute("delaySleep=true;publish('SLEEP')");events(l)
        l.execute("units[41].activity=3");events(l,20)
        l.execute("assert(sleepCalls==1 and #packets==0 and not update);units[41].activity=1;Events.UnitActivityChanged(2,41);assert(packets[1].Result=='ASLEEP')")
    def test_ambiguous_native_write_remains_protected_on_later_turn(self):
        l=self.ready();l.execute("delaySleep=true;publish('SLEEP')");events(l)
        l.execute("turn=82;Events.LocalPlayerTurnBegin()");events(l)
        l.execute("assert(sleepCalls==1 and wakeCalls==0 and packets[1].Result=='FAILED' and ExposedMembers.SPC_ExpeditionActivity.mode=='BLOCKED')")
    def test_manual_sleep_never_acquired_or_woken(self):
        l=self.ready();l.execute("units[41].activity=1;publish('SLEEP');assert(not packets[1].Owned);publish('RELEASE',false,nil,true)");events(l)
        l.execute("assert(sleepCalls==0 and wakeCalls==0 and units[41].activity==1)")
    def test_owner_change_shutdown_no_late_writer(self):
        l=self.ready();l.execute("publish('SLEEP');localOwner=3");events(l)
        l.execute("assert(sleepCalls==0);shutdown();localOwner=2");events(l)
        l.execute("assert(sleepCalls==0)")
    def test_diagnostic_records_event_and_exact_guard(self):
        l=self.ready();l.execute("sleepDenied=true;publish('SLEEP')")
        l.execute("local event,guard=false,false;for _,v in ipairs(ExposedMembers.SPC_B205TrainingTrace.entries)do if v.stage=='ACTIVITY_EVENT'then event=v.evaluationOrigin=='NATIVE_EVENT'end;if v.stage=='ACTIVITY_FAILURE'then guard=v.guardStatus=='DENIED'end end;assert(event and guard)")

class UnarmedExit(unittest.TestCase):
    def ready(self):
        l=fixture();l.execute("ready();prepare();oldKey=saved().state.activityKey");return l
    def test_same_turn_keeps_attempt_next_turn_cancels_without_award(self):
        l=self.ready();l.execute("ownTurn(2);assert(saved().state.phase=='TASK_PREPARING');currentTurn=84;ownTurn(2);local r=req('READ','r');assert(r.phase=='ARRIVED' and r.activityFailure=='ACTIVITY_START_NOT_ARMED' and not saved().state.activityKey and insightWrites==0);noNativeSideEffects()")
    def test_late_arm_cannot_cancel_or_advance_new_attempt(self):
        l=self.ready();l.execute("""
        currentTurn=84;ownTurn(2);handler(2,{Action='TASK',Token='new',UnitID=41,SampleTurn=currentTurn,NativeOperation=-1,Mission='PEOPLE',MissionX=15,MissionY=8})
        local key=saved().state.activityKey;assert(key~=oldKey)
        handler(2,{Action='ACTIVITY',Token='late',UnitID=41,ActivityKey=oldKey,Result='ARMED',Owned=true,Awake=true,Sleeping=false,SampleTurn=currentTurn,NativeOperation=-1})
        assert(saved().state.activityKey==key and saved().state.activityMode=='SLEEP' and not saved().state.taskStart)
        """)
    def test_armed_never_treated_as_unwritten(self):
        l=self.ready();l.execute("activity('ARMED','arm');currentTurn=84;ownTurn(2);assert(saved().state.phase=='TASK_PREPARING' and saved().state.activityMode=='ARMED' and saved().state.activityOwned)")
    def test_loaded_unarmed_gets_observation_grace_not_guessed_old_clock(self):
        l=self.ready();l.execute("restart();currentTurn=84;ownTurn(2);assert(saved().state.phase=='TASK_PREPARING');ownTurn(2);assert(saved().state.phase=='TASK_PREPARING');currentTurn=85;ownTurn(2);assert(saved().state.phase=='ARRIVED' and insightWrites==0);noNativeSideEffects()")
    def test_changed_or_unreadable_store_never_cleared(self):
        for change in ('storeReadError=true',"saved().revision=saved().revision+1", "saved().state.activityMode='ARMED';saved().state.activityOwned=true"):
            with self.subTest(change=change):
                l=self.ready();l.execute(change+";currentTurn=84;ownTurn(2);assert(req('READ','r').phase=='HELD' and insightWrites==0);noNativeSideEffects()")
    def test_failed_unwind_write_stays_blocked(self):
        l=self.ready();l.execute("storeNoop=true;currentTurn=84;ownTurn(2);local r=req('READ','r');assert(r.phase=='HELD' and saved().state.phase=='TASK_PREPARING' and insightWrites==0);noNativeSideEffects()")
    def test_lost_source_or_wrong_unit_never_returns_idle(self):
        for change in ("city.owner=3", "units[41].name='different'", "units[41].x=16"):
            with self.subTest(change=change):
                l=self.ready();l.execute(change+";currentTurn=84;ownTurn(2);assert(req('READ','r').phase=='HELD' and insightWrites==0);noNativeSideEffects()")

class IntegratedEvents(unittest.TestCase):
    def test_real_gate_arm_sleep_completion_release_without_frames(self):
        l=integrated();l.execute("refreshAuto=false;nativeAuto=false;beginTask();assert(view().mode=='ARMED' and sleepCalls==0)");events(l)
        l.execute("assert(view().phase=='TASK_RUNNING' and view().taskDue==85);currentTurn=85;ownTurn(2)");events(l)
        l.execute("assert(view().phase=='ARRIVED' and insightWrites==1 and wakeCalls==1 and not view().activityKey)")
    def test_lost_arm_delivery_expires_then_late_reply_cannot_write(self):
        l=integrated();l.execute("refreshAuto=false;nativeAuto=false;deferArm=true;beginTask();assert(view().mode=='SLEEP');currentTurn=84;ownTurn(2);assert(view().phase=='ARRIVED');deliver(delayedPackets[1])");events(l)
        l.execute("assert(view().phase=='ARRIVED' and sleepCalls==0 and insightWrites==0)")
    def test_file_has_no_hidden_frame_scheduler(self):
        source=(Path(__file__).resolve().parents[1]/'Mod/UI/ExpeditionSpyActivity.lua').read_text()
        for api in ('SetUpdate(', 'RequestRefresh(', 'SetRefreshHandler('):self.assertNotIn(api,source)

if __name__=='__main__':unittest.main()
