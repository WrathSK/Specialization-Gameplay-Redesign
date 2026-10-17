"""B194 retains B193 failure observation for unsupported states; owned OPERATION now waits.
B211: counts follow the B201 two-step arming (diagnostic read + pre-arm guard + pre-sleep
guard, one extra activity read); diagnostic semantics unchanged.
The numeric activities below are deterministic fixtures, not native measurements.
"""
import unittest
from test_expedition_spy_activity_diagnostic import diagnostic_bridge


def failure_bridge():
    lua = diagnostic_bridge()
    lua.execute("""
      function failure()return ExposedMembers.SPC_ExpeditionActivityFailureDiagnostic end
      activityReads=0
      local original=UnitManager.GetActivityType
      UnitManager.GetActivityType=function(u)activityReads=activityReads+1;return original(u)end
      function request_into_operation(activity)
       UnitManager.RequestOperation=function(u,op)
        assert(op==expectedSleepHash and u.id==41);sleepCalls=sleepCalls+1
        u.activity=activity or ActivityTypes.ACTIVITY_OPERATION
        Events.UnitActivityChanged(2,41);Events.GameCoreEventPublishComplete()
       end
      end
    """)
    return lua


class FailureDiagnostic(unittest.TestCase):
    def test_pre_request_guard_has_exact_failure_values_and_no_writer(self):
        l=failure_bridge()
        l.execute("""
         units[41].activity=7;publish('SLEEP');fail_without_writes()
         local d=failure()
         assert(d.owner==2 and d.unitID==41 and d.teamKey=='team1' and d.activityKey=='task1')
         assert(d.expectedName=='Native Named Spy' and d.x==15 and d.y==8 and d.turn==81)
         assert(d.phase=='PRE_REQUEST_GUARD' and d.reason=='ACTIVITY_UNEXPECTED_STATE')
         assert(d.activity=='7 (number)' and d.awake=='0 (number)' and d.hold=='2 (number)')
         assert(d.sleep=='1 (number)' and d.operationEnum=='3 (number)')
         assert(d.requested=='false (boolean)' and d.sleepAttempted=='false (boolean)')
         assert(d.equalsAwake=='false (boolean)' and d.equalsHold=='false (boolean)')
         assert(d.equalsSleep=='false (boolean)' and d.equalsOperation=='false (boolean)')
         assert(activityReads==1 and sleepChecks==1 and readinessReads==1 and endTurnReads==1)
        """)

    def test_post_request_unsupported_state_preserves_awake_startup_and_attempt_not_acceptance(self):
        l=failure_bridge()
        l.execute("""
         noAck=true;request_into_operation(9);publish('SLEEP')
         local s=diag();local d=failure()
         assert(s.activity=='0 (number)' and s.eligibilityStatus=='ALLOWED')
         assert(d.activity=='9 (number)' and d.equalsOperation=='false (boolean)')
         assert(d.equalsAwake=='false (boolean)' and d.equalsHold=='false (boolean)' and d.equalsSleep=='false (boolean)')
         assert(d.phase=='POST_REQUEST_READBACK' and d.requested=='true (boolean)' and d.sleepAttempted=='true (boolean)')
         assert(s~=d and sleepCalls==1 and wakeCalls==0 and sleepChecks==3 and wakeChecks==0)
         assert(activityReads==4 and readinessReads==1 and endTurnReads==1)
         assert(#packets==1 and packets[1].Result=='FAILED' and packets[1].Owned)
         assert(packets[1].Detail:find('ACTIVITY_UNEXPECTED_STATE',1,true) and update==nil)
         for k,v in pairs(d)do assert(type(v)~='table' and type(v)~='function' and type(v)~='userdata')end
        """)

    def test_failure_sample_survives_owned_release_failure_without_sending_wake(self):
        l=failure_bridge()
        l.execute("""
         request_into_operation(9);publish('SLEEP')
         assert(failure().phase=='POST_REQUEST_READBACK' and failure().activity=='9 (number)')
         assert(sleepCalls==1 and wakeCalls==0 and sleepChecks==3 and wakeChecks==0)
         assert(#packets==2 and packets[1].Detail:find('ACTIVITY_UNEXPECTED_STATE',1,true))
         assert(packets[2].Detail:find('ACTIVITY_RELEASE_STATE_UNKNOWN',1,true))
         assert(ExposedMembers.SPC_ExpeditionActivity.mode=='BLOCKED' and update==nil)
         assert(diag().activity=='0 (number)')
        """)

    def test_pending_poll_records_later_third_activity_without_repeat_queries(self):
        l=failure_bridge()
        l.execute("""
         noAck=true
         UnitManager.RequestOperation=function(u,op)assert(op==expectedSleepHash and u.id==41);sleepCalls=sleepCalls+1 end
         publish('SLEEP')
         assert(failure()==nil and activityReads==3 and sleepCalls==1 and sleepChecks==3 and update)
         units[41].activity=9;turn=82;update(.25)
         assert(failure().activity=='9 (number)' and failure().turn==82)
         assert(failure().phase=='POST_REQUEST_READBACK' and failure().requested=='true (boolean)')
         assert(diag().turn==81 and diag().activity=='0 (number)')
         assert(activityReads==4 and sleepChecks==3 and readinessReads==1 and endTurnReads==1)
         assert(sleepCalls==1 and wakeCalls==0 and #packets==1 and update==nil)
        """)

    def test_repeated_events_preserve_first_failure_and_do_not_reread_or_write(self):
        l=failure_bridge()
        l.execute("""
         noAck=true;request_into_operation(9);publish('SLEEP');local d=failure();local s=diag()
         units[41].activity=8;turn=82;local reads=activityReads
         for i=1,30 do Events.GameCoreEventPublishComplete();Events.LocalPlayerTurnBegin();Events.UnitActivityChanged(2,41)end
         assert(failure()==d and d.activity=='9 (number)' and d.turn==81 and diag()==s)
         assert(activityReads==reads and sleepChecks==3 and readinessReads==1 and endTurnReads==1)
         assert(sleepCalls==1 and wakeCalls==0 and #packets==1 and update==nil)
        """)

    def test_string_activity_is_not_numeric_awake(self):
        l=failure_bridge()
        l.execute("""
         units[41].activity='0';publish('SLEEP');fail_without_writes()
         assert(failure().activity=='0 (string)' and failure().awake=='0 (number)')
         assert(failure().equalsAwake=='false (boolean)' and failure().phase=='PRE_REQUEST_GUARD')
         assert(activityReads==1 and sleepChecks==1)
        """)

    def test_missing_or_string_enums_keep_typed_values_and_actual_equalities(self):
        l=failure_bridge()
        l.execute("""
         units[41].activity='operation';ActivityTypes.ACTIVITY_AWAKE=nil
         ActivityTypes.ACTIVITY_HOLD='hold';ActivityTypes.ACTIVITY_OPERATION='operation'
         publish('SLEEP');fail_without_writes()
         local d=failure()
         assert(d.awake=='nil (nil)' and d.hold=='hold (string)' and d.operationEnum=='operation (string)')
         assert(d.equalsAwake=='false (boolean)' and d.equalsHold=='false (boolean)' and d.equalsOperation=='true (boolean)')
         assert(activityReads==1 and sleepChecks==1)
        """)

    def test_unrelated_failures_do_not_create_failure_sample(self):
        for change in ["units[41].name='other'", "units[41].owner=3", "units[41].spy=9", "readThrow=true", "sleepDenied=true", "throwBeforeSleep=true"]:
            with self.subTest(change=change):
                l=failure_bridge()
                expected='REJECTED' if change=='sleepDenied=true' else 'FAILED'
                l.execute(change+";publish('SLEEP');assert(failure()==nil and packets[1].Result=='"+expected+"')")

    def test_normal_sleep_release_keeps_two_eligibility_reads_and_no_failure_sample(self):
        l=failure_bridge()
        l.execute("""
         publish('SLEEP');assert(failure()==nil and sleepChecks==3 and sleepCalls==1 and packets[1].Result=='ASLEEP')
         publish('RELEASE',true)
         assert(failure()==nil and sleepChecks==3 and wakeChecks==1 and sleepCalls==1 and wakeCalls==1)
         assert(#packets==2 and packets[2].Result=='RELEASED' and units[42].activity==0)
         assert(readinessReads==1 and endTurnReads==1 and update==nil)
        """)

    def test_preexisting_sleep_never_becomes_owned_or_gets_failure_sample(self):
        l=failure_bridge()
        l.execute("""
         units[41].activity=1;publish('SLEEP');publish('NONE')
         assert(failure()==nil and sleepCalls==0 and wakeCalls==0 and not packets[1].Owned)
        """)

    def test_unexpected_wake_is_not_reclassified_as_startup_failure(self):
        l=failure_bridge()
        l.execute("""
         publish('SLEEP');units[41].activity=0;Events.UnitActivityChanged(2,41)
         assert(failure()==nil and packets[2].Detail:find('ACTIVITY_UNEXPECTED_WAKE',1,true))
         assert(sleepCalls==1 and wakeCalls==0 and packets[3].Result=='RELEASED')
        """)

    def test_changed_identity_and_end_clear_both_snapshots_without_new_task_action(self):
        changes=["v.teamKey='team2'", "v.activityKey='task2'", "v.owner=3", "v.unitID=42", "v.expectedName='other'", "v.x=16", "v.y=9", "v.phase='ENDED'", "localOwner=3"]
        for change in changes:
            with self.subTest(change=change):
                l=failure_bridge()
                l.execute("units[41].activity=7;publish('SLEEP');assert(failure() and diag());local v=ExposedMembers.SPC_ExpeditionActivity;v.mode='NONE';"+change+";Events.GameCoreEventPublishComplete();assert(failure()==nil and diag()==nil and sleepCalls==0 and wakeCalls==0 and sleepChecks==1 and #packets==1)")

    def test_no_view_and_shutdown_clear_both_snapshots(self):
        for ending in ["ExposedMembers.SPC_ExpeditionActivity=nil;Events.GameCoreEventPublishComplete()", "shutdown()"]:
            with self.subTest(ending=ending):
                l=failure_bridge()
                l.execute("units[41].activity=7;publish('SLEEP');assert(failure() and diag());"+ending+";assert(failure()==nil and diag()==nil and sleepCalls==0 and wakeCalls==0 and update==nil)")

    def test_initialization_does_not_inherit_stale_failure_snapshot(self):
        l=failure_bridge()
        l.execute("""
         shutdown();ExposedMembers.SPC_ExpeditionActivityDiagnostic={activity='stale'}
         ExposedMembers.SPC_ExpeditionActivityFailureDiagnostic={activity='stale'}
         ExposedMembers.SPC_ExpeditionActivity=nil;init()
         assert(failure()==nil and diag()==nil and sleepCalls==0 and wakeCalls==0 and #packets==0)
        """)

    def test_new_task_key_replaces_bounded_snapshot_and_resets_attempt(self):
        l=failure_bridge()
        l.execute("""
         noAck=true;request_into_operation(9);publish('SLEEP');local old=failure()
         units[41].activity=7;turn=82;publish('SLEEP',false,'task2')
         local d=failure();assert(d~=old and d.activityKey=='task2' and d.activity=='7 (number)' and d.turn==82)
         assert(d.phase=='PRE_REQUEST_GUARD' and d.requested=='false (boolean)' and d.sleepAttempted=='false (boolean)')
         assert(sleepCalls==1 and wakeCalls==0 and sleepChecks==4 and #packets==2)
        """)

    def test_diagnostic_format_error_does_not_prevent_original_failure_ack(self):
        l=failure_bridge()
        l.execute("""
         noAck=true
         UnitManager.RequestOperation=function(u,op)
          sleepCalls=sleepCalls+1;u.activity=9
          local original=tostring
          tostring=function(v)if v==false then error('DIAGNOSTIC_FORMAT_FAILURE')end;return original(v)end
          Events.UnitActivityChanged(2,41)
         end
         publish('SLEEP')
         assert(sleepCalls==1 and wakeCalls==0 and sleepChecks==3 and #packets==1 and update==nil)
         assert(packets[1].Result=='FAILED' and packets[1].Owned and packets[1].Detail:find('ACTIVITY_UNEXPECTED_STATE',1,true))
         assert(diag().activity=='0 (number)')
        """)


if __name__=='__main__':
    unittest.main()
