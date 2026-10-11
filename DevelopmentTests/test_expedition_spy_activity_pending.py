"""B194: owned requested OPERATION waits for exact SLEEP; no early Gameplay timer.
Uses actual bridge and Gate with deterministic native mocks, not native proof.
"""
import unittest
from test_expedition_spy_activity_failure import failure_bridge
from test_expedition_spy_activity_integration import integrated


def pending_bridge(no_ack=False):
    l=failure_bridge()
    l.execute("request_into_operation();noAck="+str(no_ack).lower())
    return l


def number(text):
    return float(text.split(' (',1)[0])


class ActivityPending(unittest.TestCase):
    def test_b193_native_enum_numbers_remain_pending_then_ack_exact_sleep(self):
        l=pending_bridge()
        l.execute("""
         ActivityTypes={ACTIVITY_AWAKE=1797587246,ACTIVITY_HOLD=75236491,
          ACTIVITY_SLEEP=38434027,ACTIVITY_OPERATION=1225574625}
         units[41].activity=ActivityTypes.ACTIVITY_AWAKE
         expectedSleepHash=-41338758;GameInfo.UnitOperations.UNITOPERATION_SLEEP.Hash=expectedSleepHash
         publish('SLEEP')
         assert(sleepCalls==1 and sleepChecks==2 and #packets==0 and update and failure()==nil)
         assert(diag().activity=='1797587246 (number)' and units[41].activity==1225574625)
         update(.25);assert(#packets==0 and sleepCalls==1 and sleepChecks==2)
         units[41].activity=ActivityTypes.ACTIVITY_SLEEP;Events.UnitActivityChanged(2,41)
         assert(#packets==1 and packets[1].Result=='ASLEEP' and packets[1].Owned and update==nil)
         assert(sleepCalls==1 and wakeCalls==0 and failure()==nil)
        """)

    def test_duplicate_events_do_not_retry_or_ack_operation_and_keep_deadline(self):
        l=pending_bridge(no_ack=True)
        l.execute("""
         publish('SLEEP');local s=diag()
         for i=1,30 do Events.GameCoreEventPublishComplete();Events.LocalPlayerTurnBegin();Events.UnitActivityChanged(2,41)end
         update(9.75)
         assert(#packets==0 and sleepCalls==1 and sleepChecks==2 and wakeCalls==0 and failure()==nil)
         assert(diag()==s and readinessReads==1 and endTurnReads==1)
         update(.25)
         assert(#packets==1 and packets[1].Detail:find('ACTIVITY_SLEEP_TIMEOUT',1,true))
         assert(failure().phase=='PENDING_TIMEOUT' and update==nil and sleepCalls==1 and sleepChecks==2)
        """)

    def test_persistent_operation_timeout_is_bounded_and_retains_original_observation(self):
        l=pending_bridge(no_ack=True)
        l.execute("""
         publish('SLEEP');local before=activityReads;update(10)
         local d=failure()
         assert(d.reason=='ACTIVITY_SLEEP_TIMEOUT' and d.phase=='PENDING_TIMEOUT')
         assert(d.activity=='3 (number)' and d.equalsOperation=='true (boolean)')
         assert(d.requested=='true (boolean)' and d.sleepAttempted=='true (boolean)')
         assert(d.turn==81 and d.sampleTurn==81 and activityReads==before+1)
         assert(sleepChecks==2 and sleepCalls==1 and wakeChecks==0 and wakeCalls==0)
         assert(#packets==1 and packets[1].Result=='FAILED' and packets[1].Owned and update==nil)
         assert(diag().activity=='0 (number)' and diag().turn==81)
         for k,v in pairs(d)do assert(type(v)~='table' and type(v)~='function' and type(v)~='userdata')end
         local reads=activityReads
         for i=1,10 do Events.GameCoreEventPublishComplete();Events.LocalPlayerTurnBegin()end
         assert(failure()==d and activityReads==reads and #packets==1 and sleepCalls==1)
        """)
        self.assertEqual(number(l.eval('failure().elapsed')),10)
        self.assertEqual(number(l.eval('failure().sampledElapsed')),10)

    def test_timeout_between_polls_uses_last_validated_activity_without_new_query(self):
        l=pending_bridge(no_ack=True)
        l.execute("""
         publish('SLEEP');update(9.9);local reads=activityReads
         turn=82;units[41].activity=8;update(.11)
         assert(activityReads==reads and failure().activity=='3 (number)')
         assert(failure().turn==82 and failure().sampleTurn==81)
         assert(failure().reason=='ACTIVITY_SLEEP_TIMEOUT' and sleepChecks==2 and sleepCalls==1 and wakeCalls==0)
        """)
        self.assertAlmostEqual(number(l.eval('failure().elapsed')),10.01)
        self.assertAlmostEqual(number(l.eval('failure().sampledElapsed')),9.9)

    def test_timeout_snapshot_survives_conservative_release_failure(self):
        l=pending_bridge()
        l.execute("""
         publish('SLEEP');update(10)
         assert(failure().phase=='PENDING_TIMEOUT' and failure().reason=='ACTIVITY_SLEEP_TIMEOUT')
         assert(#packets==2 and packets[1].Detail:find('ACTIVITY_SLEEP_TIMEOUT',1,true))
         assert(packets[2].Detail:find('ACTIVITY_RELEASE_STATE_UNKNOWN',1,true))
         assert(ExposedMembers.SPC_ExpeditionActivity.mode=='BLOCKED' and update==nil)
         assert(sleepCalls==1 and wakeCalls==0 and sleepChecks==2)
        """)

    def test_timeout_formatter_failure_does_not_prevent_original_failed_ack(self):
        l=pending_bridge(no_ack=True)
        l.execute("""
         publish('SLEEP');local original=tostring
         tostring=function(v)if v==false then error('TIMEOUT_DIAGNOSTIC_FORMAT_FAILURE')end;return original(v)end
         update(10)
         assert(sleepCalls==1 and wakeCalls==0 and sleepChecks==2 and #packets==1 and update==nil)
         assert(packets[1].Result=='FAILED' and packets[1].Owned and packets[1].Detail:find('ACTIVITY_SLEEP_TIMEOUT',1,true))
         assert(diag().activity=='0 (number)')
        """)

    def test_sleep_at_last_allowed_poll_succeeds_instead_of_timeout(self):
        l=pending_bridge()
        l.execute("""
         publish('SLEEP');update(9.75);units[41].activity=1;update(.25)
         assert(#packets==1 and packets[1].Result=='ASLEEP' and failure()==nil and update==nil)
         assert(sleepCalls==1 and wakeCalls==0 and sleepChecks==2)
        """)

    def test_preexisting_operation_never_adopts_or_requests_sleep(self):
        l=pending_bridge()
        l.execute("""
         units[41].activity=3;publish('SLEEP');fail_without_writes()
         assert(failure().phase=='PRE_REQUEST_GUARD' and failure().equalsOperation=='true (boolean)')
         assert(failure().requested=='false (boolean)' and failure().sleepAttempted=='false (boolean)')
         assert(sleepChecks==1 and update==nil)
        """)

    def test_string_operation_value_does_not_match_numeric_enum(self):
        l=pending_bridge(no_ack=True)
        l.execute("""
         UnitManager.RequestOperation=function(u,op)sleepCalls=sleepCalls+1;u.activity='3';Events.UnitActivityChanged(2,41)end
         publish('SLEEP')
         assert(packets[1].Detail:find('ACTIVITY_UNEXPECTED_STATE',1,true) and update==nil)
         assert(failure().activity=='3 (string)' and failure().equalsOperation=='false (boolean)' and sleepCalls==1)
        """)

    def test_wrong_identity_or_native_mission_during_pending_never_waits_or_wakes(self):
        changes=["units[41].owner=3", "units[41].name='other'", "units[41].x=99", "units[41].kind=2", "units[41].spy=9", "readThrow=true"]
        for change in changes:
            with self.subTest(change=change):
                l=pending_bridge(no_ack=True)
                l.execute("publish('SLEEP');assert(update and #packets==0);"+change+";update(.25);assert(update==nil and #packets==1 and packets[1].Result=='FAILED' and packets[1].Owned and failure()==nil and sleepCalls==1 and wakeCalls==0 and sleepChecks==2)")

    def test_pending_cancel_cannot_wake_unknown_operation_or_restart_after_late_sleep(self):
        l=pending_bridge()
        l.execute("""
         publish('SLEEP');publish('RELEASE',false,nil,true)
         assert(#packets==1 and packets[1].Detail:find('ACTIVITY_RELEASE_STATE_UNKNOWN',1,true))
         assert(update==nil and ExposedMembers.SPC_ExpeditionActivity.mode=='BLOCKED' and sleepCalls==1 and wakeCalls==0)
         units[41].activity=1;Events.UnitActivityChanged(2,41);Events.LocalPlayerTurnBegin()
         assert(#packets==1 and sleepCalls==1 and wakeCalls==0 and update==nil and failure()==nil)
        """)

    def test_pending_cancel_after_actual_sleep_uses_existing_owned_release(self):
        l=pending_bridge()
        l.execute("""
         publish('SLEEP');units[41].activity=1;publish('RELEASE',false,nil,true)
         assert(#packets==1 and packets[1].Result=='RELEASED' and packets[1].Owned)
         assert(sleepCalls==1 and wakeCalls==1 and update==nil and failure()==nil)
        """)

    def test_operation_after_asleep_is_still_unexpected_wake(self):
        l=failure_bridge()
        l.execute("""
         publish('SLEEP');units[41].activity=3;Events.UnitActivityChanged(2,41)
         assert(packets[2].Detail:find('ACTIVITY_UNEXPECTED_WAKE',1,true) and failure()==nil)
         assert(sleepCalls==1 and wakeCalls==0 and update==nil)
        """)

    def test_pending_is_not_inherited_by_an_unrequested_new_key(self):
        l=pending_bridge(no_ack=True)
        l.execute("""
         publish('SLEEP');assert(#packets==0 and update);publish('SLEEP',false,'task2')
         assert(#packets==1 and packets[1].Detail:find('ACTIVITY_UNEXPECTED_STATE',1,true) and not packets[1].Owned)
         assert(failure().phase=='PRE_REQUEST_GUARD' and failure().activityKey=='task2')
         assert(failure().requested=='false (boolean)' and failure().sleepAttempted=='false (boolean)')
         assert(sleepCalls==1 and wakeCalls==0 and update==nil)
        """)

    def test_timeout_sample_and_poll_are_cleared_by_end_shutdown_or_removed_view(self):
        for ending in ["ExposedMembers.SPC_ExpeditionActivity.phase='ENDED';ExposedMembers.SPC_ExpeditionActivity.mode='NONE';Events.GameCoreEventPublishComplete()", "ExposedMembers.SPC_ExpeditionActivity=nil;Events.GameCoreEventPublishComplete()", "shutdown()"]:
            with self.subTest(ending=ending):
                l=pending_bridge(no_ack=True)
                l.execute("publish('SLEEP');update(10);assert(failure());"+ending+";assert(failure()==nil and diag()==nil and update==nil and sleepCalls==1 and wakeCalls==0)")


class PendingGameplayIntegration(unittest.TestCase):
    def test_actual_gate_starts_timer_only_after_sleep_then_completes_and_releases_once(self):
        l=integrated()
        l.execute("""
         delaySleep=true;onSleep=function()units[41].activity=3 end;beginTask()
         assert(view().phase=='TASK_PREPARING' and not view().taskStart and not view().taskDue)
         assert(view().taskCompletions==0 and #activityPackets==0 and activityUpdate and sleepCalls==1)
         for i=1,10 do Events.GameCoreEventPublishComplete();Events.LocalPlayerTurnBegin()end
         activityUpdate(.25)
         assert(not view().taskStart and not view().taskDue and #activityPackets==0 and sleepCalls==1)
         units[41].activity=1;Events.UnitActivityChanged(2,41)
         assert(view().phase=='TASK_RUNNING' and view().taskStart==83 and view().taskDue==85 and view().owned)
         assert(#activityPackets==1 and activityPackets[1].Result=='ASLEEP' and not activityUpdate)
         currentTurn=84;ownTurn(2);Events.LocalPlayerTurnBegin();assert(view().taskCompletions==0)
         currentTurn=85;ownTurn(2);Events.GameCoreEventPublishComplete();ownTurn(2)
         assert(view().phase=='TASK_COMPLETE' and view().taskCompletions==1 and view().mode=='NONE')
         assert(sleepCalls==1 and wakeCalls==1 and not activityUpdate and units[41].activity==0)
         assert(properties==0 and nativeCalls==0 and destroys==0 and placeCalls==0 and finishCalls==0)
         handler(2,{Action='READ',Token='after-pending-completion'})
         local r=ExposedMembers.SPC_ExpeditionGateReply
         assert(r.bound and r.sourceCity==1 and r.count==1)
        """)

    def test_actual_gate_timeout_has_no_task_timer_or_completion(self):
        l=integrated()
        l.execute("""
         delaySleep=true;onSleep=function()units[41].activity=3 end;beginTask();activityUpdate(10)
         assert(view().phase=='HELD' and view().mode=='BLOCKED' and not view().taskStart and not view().taskDue)
         assert(view().taskCompletions==0 and sleepCalls==1 and wakeCalls==0 and not activityUpdate)
         assert(ExposedMembers.SPC_ExpeditionActivityFailureDiagnostic.reason=='ACTIVITY_SLEEP_TIMEOUT')
         currentTurn=85;ownTurn(2);Events.GameCoreEventPublishComplete();Events.LocalPlayerTurnBegin()
         assert(not view().taskStart and view().taskCompletions==0 and sleepCalls==1 and wakeCalls==0)
         assert(properties==0 and nativeCalls==0 and destroys==0 and placeCalls==0 and finishCalls==0)
        """)

    def test_source_loss_while_pending_remains_held_without_forced_release(self):
        l=integrated()
        l.execute("""
         delaySleep=true;onSleep=function()units[41].activity=3 end;beginTask()
         city.owner=3;transfer();Events.GameCoreEventPublishComplete()
         assert(view().phase=='HELD' and view().mode=='BLOCKED' and not view().taskStart and not view().taskDue)
         assert(sleepCalls==1 and wakeCalls==0 and not activityUpdate and view().taskCompletions==0)
         assert(properties==0 and nativeCalls==0 and destroys==0 and placeCalls==0 and finishCalls==0)
        """)


if __name__=='__main__':
    unittest.main()
