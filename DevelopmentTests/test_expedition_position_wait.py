"""B217: actual UI bridge, independently delayed position view; no native PASS."""
import unittest
from test_expedition_spy_activity_ui import bridge

class PositionWait(unittest.TestCase):
    def test_initial_ui_lag_converges_without_early_sleep_or_ack(self):
        l=bridge();l.execute("""
         units[41].x=14;publish('SLEEP')
         assert(sleepCalls==0 and arms==0 and #packets==0 and not update)
         Events.UnitMoveComplete(2,42);assert(sleepCalls==0 and #packets==0 and not update)
         units[41].x=15;Events.UnitMoveComplete(2,41)
         assert(sleepCalls==1 and arms==1 and #packets==1 and packets[1].Result=='ASLEEP' and not update)
        """)

    def test_unresolved_position_stops_at_turn_event_and_logs_are_collector_compatible(self):
        import sys
        from pathlib import Path
        sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tools'))
        from read_expedition_trace import GATE_PATTERN
        l=bridge();lines=[];l.globals().print=lines.append
        l.execute("units[41].x=14;publish('SLEEP');for i=1,30 do Events.GameCoreEventPublishComplete()end;assert(#packets==0 and not update);Events.LocalPlayerTurnBegin();assert(sleepCalls==0 and arms==0 and #packets==1 and packets[1].Detail:find('ACTIVITY_POSITION_UNCONFIRMED_AT_TURN') and packets[1].Detail:find('actual=14,8') and not update)")
        self.assertEqual(len(lines),2)
        self.assertTrue(all(GATE_PATTERN.fullmatch(x) for x in lines))
    def test_failed_boundary_cannot_later_resume_old_attempt(self):
        l=bridge();l.execute("units[41].x=14;publish('SLEEP');Events.LocalPlayerTurnBegin();units[41].x=15;Events.UnitMoveComplete(2,41);assert(sleepCalls==0 and #packets==1 and packets[1].Detail:find('UNCONFIRMED_AT_TURN') and not update)")
    def test_wrong_identity_or_native_mission_during_wait_fails_immediately(self):
        for change in ["units[41].name='other'","units[41].owner=3","units[41].spy=9","units[41]=nil"]:
            with self.subTest(change=change):
                l=bridge();l.execute("units[41].x=14;publish('SLEEP');"+change+";Events.GameCoreEventPublishComplete();assert(#packets==1 and packets[1].Result=='FAILED' and sleepCalls==0 and not update)")
    def test_stale_attempt_cancels_wait_without_old_ack(self):
        l=bridge();l.execute("units[41].x=14;publish('SLEEP');assert(not update);publish('NONE',false,'task2');units[41].x=15;Events.UnitMoveComplete(2,41);assert(#packets==0 and sleepCalls==0 and not update)")
    def test_running_release_and_recovery_displacement_never_waits(self):
        for mode in ['ASLEEP','RELEASE','RECOVER']:
            with self.subTest(mode=mode):
                l=bridge();l.execute("units[41].x=14;publish('"+mode+"',true);Events.LocalPlayerTurnBegin();assert(#packets=="+("1" if mode=="RELEASE" else "2")+" and packets[1].Detail:find('POSITION_CHANGED') and sleepCalls==0 and wakeCalls==0 and not update)")
    def test_position_was_confirmed_then_changed_before_arm_ack_is_not_initial(self):
        l=bridge();l.execute("noArmAck=true;publish('SLEEP');assert(arms==1 and sleepCalls==0);units[41].x=14;publish('ARMED',true);assert(packets[1].Result=='FAILED' and packets[1].Detail:find('POSITION_CHANGED') and not update)")
    def test_unknown_coordinates_are_not_transient_position_evidence(self):
        l=bridge();l.execute("units[41].GetX=function()return nil end;publish('SLEEP');assert(packets[1].Detail:find('POSITION_UNREADABLE') and not update and sleepCalls==0)")
    def test_actual_gate_timer_waits_for_independent_ui_position_then_completes(self):
        from test_expedition_spy_activity_integration import integrated
        l=integrated();l.execute("""
         uiX=14
         local proxy=setmetatable({GetX=function()return uiX end},{__index=units[41],__newindex=units[41]})
         activityEnvironment.Players={[2]={GetUnits=function()return {FindID=function(self,id)if id==41 then return proxy end;return units[id]end}end}}
         beginTask();assert(view().phase=='TASK_PREPARING' and not view().taskStart and sleepCalls==0 and not activityUpdate)
         Events.GameCoreEventPublishComplete();assert(not view().taskStart and not activityUpdate)
         uiX=15;Events.GameCoreEventPublishComplete()
         assert(view().phase=='TASK_RUNNING' and view().taskStart==83 and sleepCalls==1)
         currentTurn=85;ownTurn(2);Events.GameCoreEventPublishComplete()
         assert(insightWrites==1 and wakeCalls==1 and view().mode=='NONE')
        """)

if __name__=='__main__':unittest.main()
