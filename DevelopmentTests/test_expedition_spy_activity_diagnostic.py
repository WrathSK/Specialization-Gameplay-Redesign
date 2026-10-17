"""B192 actual bridge: bounded, read-only preflight evidence cannot authorize activity.
B211: check counts follow the B201 two-step arming (3 eligibility reads on the normal path).
Fixtures prove isolation and representation, not native readiness or SLEEP support.
"""
import unittest
from test_expedition_spy_activity_ui import bridge


def diagnostic_bridge():
    lua = bridge()
    lua.execute("""
      readinessReads=0;endTurnReads=0
      units[41].IsReadyToMove=function(self)readinessReads=readinessReads+1;return true end
    """)
    lua.execute("""
      units[41].GetSpyOperationEndTurn=function(self)endTurnReads=endTurnReads+1;return 83 end
      function diag()return ExposedMembers.SPC_ExpeditionActivityDiagnostic end
      function fail_without_writes()
       assert(sleepCalls==0 and wakeCalls==0 and #packets==1)
       assert(packets[1].Result=='FAILED' and not packets[1].Owned)
       assert(packets[1].Detail:find('ACTIVITY_UNEXPECTED_STATE',1,true))
       assert(update==nil)
      end
    """)
    return lua


class ActivityDiagnostic(unittest.TestCase):
    def test_third_activity_captures_allowed_and_denied_without_bypassing_guard(self):
        for denied, status in [(False, 'ALLOWED'), (True, 'DENIED')]:
            with self.subTest(denied=denied):
                l=diagnostic_bridge()
                l.execute(f"units[41].activity=7;sleepDenied={str(denied).lower()};publish('SLEEP');fail_without_writes();assert(diag().eligibilityStatus=='{status}' and sleepChecks==1)")
                l.execute("""
                 local d=diag()
                 assert(d.owner==2 and d.unitID==41 and d.teamKey=='team1' and d.activityKey=='task1')
                 assert(d.expectedName=='Native Named Spy' and d.x==15 and d.y==8 and d.turn==81)
                 assert(d.activity=='7 (number)' and d.awake=='0 (number)' and d.hold=='2 (number)')
                 assert(d.sleep=='1 (number)' and d.operationEnum=='3 (number)')
                 assert(d.ready=='true (boolean)' and d.operation=='-1 (number)' and d.endTurn=='83 (number)')
                 assert(d.hash=='70 (number)' and readinessReads==1 and endTurnReads==1)
                """)

    def test_string_activity_and_undefined_or_string_enums_remain_distinct(self):
        l=diagnostic_bridge()
        l.execute("""
         units[41].activity='0';ActivityTypes.ACTIVITY_HOLD=nil
         ActivityTypes.ACTIVITY_OPERATION='operation';publish('SLEEP');fail_without_writes()
         assert(diag().activity=='0 (string)' and diag().awake=='0 (number)')
         assert(diag().hold=='nil (nil)' and diag().operationEnum=='operation (string)')
         assert(diag().eligibilityStatus=='ALLOWED')
        """)

    def test_undefined_awake_hold_still_captured_without_state_bypass(self):
        l=diagnostic_bridge()
        l.execute("""
         units[41].activity=7;ActivityTypes.ACTIVITY_AWAKE=nil;ActivityTypes.ACTIVITY_HOLD=nil
         publish('SLEEP');fail_without_writes()
         assert(diag().awake=='nil (nil)' and diag().hold=='nil (nil)' and sleepChecks==1)
        """)

    def test_missing_or_throwing_readiness_does_not_hide_other_fields(self):
        for value in ['nil', "function()error('READY_UNREADABLE')end"]:
            with self.subTest(value=value):
                l=diagnostic_bridge()
                l.execute("units[41].activity=7;units[41].IsReadyToMove="+value+";publish('SLEEP');fail_without_writes();assert(diag().ready:find('UNKNOWN',1,true)==1 and diag().endTurn=='83 (number)' and diag().eligibilityStatus=='ALLOWED' and sleepChecks==1)")

    def test_missing_or_throwing_end_turn_does_not_hide_other_fields(self):
        for value in ['nil', "function()error('END_UNREADABLE')end"]:
            with self.subTest(value=value):
                l=diagnostic_bridge()
                l.execute("units[41].activity=7;units[41].GetSpyOperationEndTurn="+value+";publish('SLEEP');fail_without_writes();assert(diag().endTurn:find('UNKNOWN',1,true)==1 and diag().ready=='true (boolean)' and diag().eligibilityStatus=='ALLOWED')")

    def test_missing_or_throwing_eligibility_is_unknown_without_replacing_failure(self):
        for value in ['nil', "function()error('ELIGIBILITY_UNREADABLE')end"]:
            with self.subTest(value=value):
                l=diagnostic_bridge()
                l.execute("units[41].activity=7;UnitManager.CanStartOperation="+value+";publish('SLEEP');fail_without_writes();assert(diag().eligibilityStatus=='UNKNOWN' and diag().eligibility:find('UNKNOWN',1,true)==1 and diag().activity=='7 (number)' and diag().ready=='true (boolean)')")

    def test_non_boolean_eligibility_is_not_native_permission(self):
        for value, text in [('nil', 'nil (nil)'), ('1', '1 (number)'), ("'true'", 'true (string)')]:
            with self.subTest(value=value):
                l=diagnostic_bridge()
                l.execute("units[41].activity=7;UnitManager.CanStartOperation=function()sleepChecks=sleepChecks+1;return "+value+" end;publish('SLEEP');fail_without_writes();assert(diag().eligibilityStatus=='UNKNOWN' and diag().eligibility=='"+text+"' and sleepChecks==1)")

    def test_unavailable_hash_skips_eligibility_but_preserves_state_observation(self):
        l=diagnostic_bridge()
        l.execute("""
         units[41].activity=7;GameInfo.UnitOperations.UNITOPERATION_SLEEP=nil
         publish('SLEEP');fail_without_writes()
         assert(diag().hash:find('UNKNOWN',1,true)==1 and diag().eligibilityStatus=='UNKNOWN')
         assert(diag().ready=='true (boolean)' and diag().activity=='7 (number)' and sleepChecks==0)
        """)

    def test_invalid_exact_identity_never_performs_diagnostic_queries(self):
        for change in ["units[41]=nil", "units[41].id=99", "units[41].owner=3", "units[41].kind=2", "units[41].name='other'", "units[41].x=16", "units[41].spy=9", "readThrow=true"]:
            with self.subTest(change=change):
                l=diagnostic_bridge()
                l.execute(change+";publish('SLEEP');assert(diag()==nil and sleepChecks==0 and readinessReads==0 and endTurnReads==0 and sleepCalls==0 and wakeCalls==0 and #packets==1 and packets[1].Result=='FAILED')")

    def test_normal_task_keeps_exact_writer_and_ack_behavior(self):
        l=diagnostic_bridge()
        l.execute("""
         publish('SLEEP')
         assert(sleepChecks==3 and sleepCalls==1 and wakeCalls==0 and #packets==1 and packets[1].Result=='ASLEEP')
         assert(diag().activity=='0 (number)' and diag().ready=='true (boolean)' and diag().eligibilityStatus=='ALLOWED')
         local saved=diag();publish('RELEASE',true)
         assert(wakeChecks==1 and wakeCalls==1 and #packets==2 and packets[2].Result=='RELEASED')
         assert(sleepChecks==3 and readinessReads==1 and endTurnReads==1)
         assert(saved.activity=='0 (number)' and units[42].activity==0)
        """)

    def test_diagnostic_eligibility_neither_authorizes_nor_vetoes_actual_guard(self):
        l=diagnostic_bridge()
        l.execute("""
         UnitManager.CanStartOperation=function()sleepChecks=sleepChecks+1;return sleepChecks==1 end
         publish('SLEEP');assert(diag().eligibilityStatus=='ALLOWED' and sleepChecks==2)
         assert(sleepCalls==0 and wakeCalls==0 and packets[1].Detail:find('ACTIVITY_SLEEP_NOT_ALLOWED',1,true))
        """)
        l=diagnostic_bridge()
        l.execute("""
         UnitManager.CanStartOperation=function()sleepChecks=sleepChecks+1;return sleepChecks>=2 end
         publish('SLEEP');assert(diag().eligibilityStatus=='DENIED' and sleepChecks==3)
         assert(sleepCalls==1 and packets[1].Result=='ASLEEP')
        """)

    def test_diagnostic_eligibility_exception_does_not_prevent_real_recheck(self):
        l=diagnostic_bridge()
        l.execute("""
         UnitManager.CanStartOperation=function()
          sleepChecks=sleepChecks+1;if sleepChecks==1 then error('TRANSIENT_READ')end;return true
         end
         publish('SLEEP');assert(diag().eligibilityStatus=='UNKNOWN' and sleepChecks==3)
         assert(sleepCalls==1 and packets[1].Result=='ASLEEP')
        """)

    def test_missing_diagnostic_only_readers_do_not_block_normal_task(self):
        l=diagnostic_bridge()
        l.execute("""
         units[41].IsReadyToMove=nil;units[41].GetSpyOperationEndTurn=nil;publish('SLEEP')
         assert(sleepCalls==1 and packets[1].Result=='ASLEEP' and diag().ready:find('UNKNOWN',1,true)==1)
         publish('RELEASE',true);assert(wakeCalls==1 and packets[2].Result=='RELEASED')
        """)

    def test_bounded_sample_is_not_replaced_by_held_refresh_or_turn_monitor(self):
        l=diagnostic_bridge()
        l.execute("""
         units[41].activity=7;publish('SLEEP');local saved=diag()
         units[41].activity=8;turn=82
         for i=1,20 do Events.GameCoreEventPublishComplete();Events.LocalPlayerTurnBegin();Events.UnitActivityChanged(2,41)end
         assert(diag()==saved and saved.activity=='7 (number)' and saved.turn==81)
         assert(sleepChecks==1 and readinessReads==1 and endTurnReads==1 and sleepCalls==0 and wakeCalls==0 and #packets==1 and update==nil)
        """)

    def test_new_key_replaces_sample_without_growing_history(self):
        l=diagnostic_bridge()
        l.execute("""
         noAck=true;units[41].activity=7;publish('SLEEP');local old=diag()
         units[41].activity=8;turn=82;publish('SLEEP',false,'task2')
         assert(diag()~=old and diag().activityKey=='task2' and diag().activity=='8 (number)' and diag().turn==82)
         assert(sleepChecks==2 and readinessReads==2 and endTurnReads==2 and sleepCalls==0 and wakeCalls==0)
         for k,v in pairs(diag())do assert(type(v)~='table' and type(v)~='function' and type(v)~='userdata')end
        """)

    def test_new_team_clears_stale_sample_even_before_task(self):
        l=diagnostic_bridge()
        l.execute("""
         units[41].activity=7;publish('SLEEP');assert(diag())
         local v=ExposedMembers.SPC_ExpeditionActivity;v.teamKey='team2';v.mode='NONE';v.revision=v.revision+1
         Events.GameCoreEventPublishComplete();assert(diag()==nil and sleepChecks==1 and sleepCalls==0 and wakeCalls==0)
        """)

    def test_missing_view_and_shutdown_clear_without_native_actions(self):
        for ending in ["ExposedMembers.SPC_ExpeditionActivity=nil;Events.GameCoreEventPublishComplete()", "shutdown()"]:
            with self.subTest(ending=ending):
                l=diagnostic_bridge()
                l.execute("units[41].activity=7;publish('SLEEP');assert(diag());"+ending+";assert(diag()==nil and sleepCalls==0 and wakeCalls==0 and update==nil)")

    def test_end_and_local_owner_change_discard_observation(self):
        for change in ["ExposedMembers.SPC_ExpeditionActivity.phase='ENDED'", "localOwner=3"]:
            with self.subTest(change=change):
                l=diagnostic_bridge()
                l.execute("units[41].activity=7;publish('SLEEP');assert(diag());"+change+";Events.GameCoreEventPublishComplete();assert(diag()==nil and sleepCalls==0 and wakeCalls==0 and sleepChecks==1)")

    def test_context_reinitialize_does_not_inherit_preexisting_observation(self):
        l=diagnostic_bridge()
        l.execute("""
         shutdown();ExposedMembers.SPC_ExpeditionActivityDiagnostic={activity='stale'}
         ExposedMembers.SPC_ExpeditionActivity=nil;init()
         assert(diag()==nil and sleepCalls==0 and wakeCalls==0 and sleepChecks==0 and #packets==0)
        """)

    def test_reentrant_diagnostic_read_never_writes_or_publishes_stale_lease(self):
        for replacement in ["ExposedMembers.SPC_ExpeditionActivity=nil", "local v=ExposedMembers.SPC_ExpeditionActivity;v.teamKey='team2';v.activityKey='task2';v.mode='NONE';v.revision=v.revision+1"]:
            with self.subTest(replacement=replacement):
                l=diagnostic_bridge()
                l.execute("UnitManager.CanStartOperation=function()sleepChecks=sleepChecks+1;"+replacement+";Events.GameCoreEventPublishComplete();return true end;publish('SLEEP');assert(diag()==nil and sleepChecks==1 and sleepCalls==0 and wakeCalls==0 and #packets==0 and update==nil)")

    def test_error_strings_are_bounded_and_single_line(self):
        l=diagnostic_bridge()
        l.execute("""
         units[41].activity=7;units[41].IsReadyToMove=function()error(string.rep('r',400)..'\\nnot another line')end
         publish('SLEEP');fail_without_writes()
         assert(#diag().ready<=220 and not diag().ready:find('[%c]') and diag().eligibilityStatus=='ALLOWED')
        """)


if __name__ == '__main__':
    unittest.main()
