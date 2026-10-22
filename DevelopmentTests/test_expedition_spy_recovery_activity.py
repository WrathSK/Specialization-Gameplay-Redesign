"""B201 actual activity UI: recovery only reads, durable ARM gates native Sleep.

Uses the existing native-fact bridge fixture, replacing only the mocked Gate ACK
contract. Actual persistent Gate/store integration is covered separately.
"""
import unittest
from test_expedition_spy_activity_ui import bridge


def recovery_bridge():
    lua=bridge()
    lua.execute(r"""
      arms=0;acks={};recoverMode='NONE';recoverOwned=false
      UI.RequestPlayerOperation=function(owner,op,args)
       assert(owner==2 and op==7 and args.Action=='ACTIVITY')
       assert(args.SampleTurn==turn and args.UnitID==41)
       acks[#acks+1]=args
       if args.Result~='FAILED'then assert(args.NativeOperation==-1)end
       if args.Result=='ARMED'then
        arms=arms+1;assert(args.Owned and sleepCalls==0 and args.Awake==true and args.Sleeping==false)
        if onArm then onArm()end
        if not delayArm then publish('ARMED',true,nil,true)end
       elseif args.Result=='RECOVERED'then
        assert(type(args.Sleeping)=='boolean' and type(args.Awake)=='boolean' and args.Sleeping~=args.Awake)
        if not noRecoveryAck then publish(recoverMode,recoverOwned,nil,recoverMode=='RELEASE')end
       elseif args.Result=='ASLEEP'then publish('ASLEEP',args.Owned)
       elseif args.Result=='RELEASED'then publish('NONE',false)
       else publish('BLOCKED',args.Owned)end
      end
      function count(result)local n=0;for _,p in ipairs(acks)do if p.Result==result then n=n+1 end end;return n end
    """)
    return lua


class RecoveryActivity(unittest.TestCase):
    def test_recovery_sleep_reads_once_without_request_or_eligibility(self):
        l=recovery_bridge();l.execute("units[41].activity=1;noRecoveryAck=true;publish('RECOVER',true);assert(#acks==1 and acks[1].Result=='RECOVERED' and acks[1].Sleeping and not acks[1].Awake and acks[1].Owned);for i=1,20 do Events.GameCoreEventPublishComplete()end;assert(#acks==1 and sleepCalls==0 and wakeCalls==0 and sleepChecks==0 and wakeChecks==0 and update==nil)")

    def test_recovery_awake_or_hold_is_fresh_observation_not_resleep(self):
        for a in [0,2]:
            with self.subTest(activity=a):
                l=recovery_bridge();l.execute(f"units[41].activity={a};publish('RECOVER',true);assert(#acks==1 and not acks[1].Sleeping and acks[1].Awake and sleepCalls==0 and wakeCalls==0 and sleepChecks==0)")

    def test_recovery_ignores_persisted_confirmed_sleep_when_actually_awake(self):
        l=recovery_bridge();l.execute("noRecoveryAck=true;publish('NONE',true);ExposedMembers.SPC_ExpeditionActivity.sleepConfirmed=true;ExposedMembers.SPC_ExpeditionActivity.recovering=true;ExposedMembers.SPC_ExpeditionActivity.mode='RECOVER';Events.GameCoreEventPublishComplete();assert(acks[1].Awake and not acks[1].Sleeping and sleepCalls==0)")

    def test_recovery_operation_waits_then_reports_actual_sleep(self):
        l=recovery_bridge();l.execute("units[41].activity=3;publish('RECOVER',true);assert(not update and #acks==0);for i=1,5 do Events.GameCoreEventPublishComplete()end;units[41].activity=1;Events.UnitActivityChanged(2,41);assert(#acks==1 and acks[1].Sleeping and sleepCalls==0 and wakeCalls==0 and sleepChecks==0 and update==nil)")

    def test_recovery_operation_timeout_is_bounded_and_never_retried(self):
        l=recovery_bridge();l.execute("units[41].activity=3;publish('RECOVER',true);turn=turn+1;Events.LocalPlayerTurnBegin();assert(#acks==1 and acks[1].Result=='FAILED' and acks[1].Detail:find('ACTIVITY_RECOVER_TIMEOUT',1,true) and update==nil);for i=1,10 do Events.LocalPlayerTurnBegin();Events.GameCoreEventPublishComplete()end;assert(#acks==1 and sleepCalls==0 and wakeCalls==0)")

    def test_recovery_unexpected_activity_fails_without_native_action(self):
        for a in [8,"'3'","nil"]:
            with self.subTest(activity=a):
                l=recovery_bridge();l.execute(f"units[41].activity={a};publish('RECOVER',true);assert(#acks==1 and acks[1].Result=='FAILED' and sleepCalls==0 and wakeCalls==0 and update==nil)")

    def test_recovery_exact_identity_and_native_mission_checks_precede_ack(self):
        for change in ["units[41]=nil","units[41].id=9","units[41].name='other'","units[41].owner=3","units[41].kind=2","units[41].x=99","units[41].spy=5","readThrow=true"]:
            with self.subTest(change=change):
                l=recovery_bridge();l.execute(change+";publish('RECOVER',true);assert(#acks==1 and acks[1].Result=='FAILED' and sleepCalls==0 and wakeCalls==0 and sleepChecks==0)")

    def test_durable_arm_ack_precedes_native_sleep_and_asleep_ack(self):
        l=recovery_bridge();l.execute("publish('SLEEP');assert(arms==1 and sleepCalls==1 and count('ARMED')==1 and count('ASLEEP')==1 and #acks==2 and acks[1].Result=='ARMED' and acks[2].Result=='ASLEEP' and acks[2].Owned and update==nil);for i=1,10 do Events.GameCoreEventPublishComplete()end;assert(sleepCalls==1 and #acks==2)")

    def test_lost_arm_ack_never_falls_back_to_sleep(self):
        l=recovery_bridge();l.execute("delayArm=true;publish('SLEEP');assert(arms==1 and sleepCalls==0 and update==nil);for i=1,20 do Events.GameCoreEventPublishComplete();Events.LocalPlayerTurnBegin()end;assert(#acks==1 and sleepCalls==0);publish('ARMED',true,nil,true);assert(sleepCalls==1 and count('ASLEEP')==1)")

    def test_failed_arm_write_blocks_before_native_sleep(self):
        l=recovery_bridge();l.execute("delayArm=true;onArm=function()publish('BLOCKED',true)end;publish('SLEEP');assert(arms==1 and sleepCalls==0 and wakeCalls==0 and count('ASLEEP')==0 and update==nil)")

    def test_preexisting_sleep_is_unowned_and_does_not_arm(self):
        l=recovery_bridge();l.execute("units[41].activity=1;publish('SLEEP');assert(#acks==1 and acks[1].Result=='ASLEEP' and not acks[1].Owned and arms==0 and sleepCalls==0);publish('RELEASE',false,nil,true);assert(wakeCalls==0 and units[41].activity==1 and not acks[2].Owned)")

    def test_stale_armed_publication_after_ui_restart_does_not_retry(self):
        l=recovery_bridge();l.execute("publish('ARMED',true,nil,true);assert(sleepCalls==0 and count('FAILED')==1 and acks[1].Detail:find('ACTIVITY_ARM_ACK_NOT_OBSERVED',1,true));Events.GameCoreEventPublishComplete();assert(sleepCalls==0 and #acks==1)")

    def test_arm_rechecks_exact_unit_and_state_before_native_request(self):
        for change in ["units[41].name='other'","units[41].x=99","units[41].spy=8","units[41].activity=3"]:
            with self.subTest(change=change):
                l=recovery_bridge();l.execute("onArm=function()"+change+" end;publish('SLEEP');assert(arms==1 and sleepCalls==0 and wakeCalls==0 and count('ASLEEP')==0 and count('FAILED')==1)")

    def test_armed_owned_operation_waits_without_second_request(self):
        l=recovery_bridge();l.execute("UnitManager.RequestOperation=function(u,op)sleepCalls=sleepCalls+1;u.activity=3;Events.UnitActivityChanged(2,41)end;publish('SLEEP');assert(arms==1 and sleepCalls==1 and count('ASLEEP')==0 and not update);for i=1,8 do Events.GameCoreEventPublishComplete()end;units[41].activity=1;Events.UnitActivityChanged(2,41);assert(sleepCalls==1 and count('ASLEEP')==1 and update==nil)")

    def test_armed_timeout_retains_sleep_failure_diagnostic(self):
        l=recovery_bridge();l.execute("UnitManager.RequestOperation=function(u,op)sleepCalls=sleepCalls+1;u.activity=3 end;publish('SLEEP');turn=turn+1;Events.LocalPlayerTurnBegin();assert(sleepCalls==1 and count('FAILED')==1 and acks[2].Detail:find('ACTIVITY_SLEEP_TIMEOUT',1,true));local d=ExposedMembers.SPC_ExpeditionActivityFailureDiagnostic;assert(d and d.reason=='ACTIVITY_SLEEP_TIMEOUT' and d.phase=='PENDING_TIMEOUT')")

    def test_fresh_recovered_owned_sleep_is_only_woken_after_gate_release(self):
        l=recovery_bridge();l.execute("units[41].activity=1;recoverMode='RELEASE';recoverOwned=true;publish('RECOVER',true);assert(acks[1].Result=='RECOVERED' and acks[1].Sleeping and wakeCalls==1 and sleepCalls==0 and count('RELEASED')==1 and units[41].activity==0)")

    def test_fresh_recovered_unowned_sleep_is_never_woken(self):
        l=recovery_bridge();l.execute("units[41].activity=1;recoverMode='RELEASE';recoverOwned=false;publish('RECOVER',false);assert(acks[1].Sleeping and not acks[1].Owned and wakeCalls==0 and sleepCalls==0 and units[41].activity==1)")

    def test_recovered_release_rereads_sleep_before_wake(self):
        l=recovery_bridge();l.execute("units[41].activity=1;noRecoveryAck=true;publish('RECOVER',true);units[41].name='replaced';publish('RELEASE',true,nil,true);assert(wakeCalls==0 and count('FAILED')==1)")

    def test_recovery_read_that_changes_lease_cannot_ack_old_observation(self):
        l=recovery_bridge();l.execute("local read=UnitManager.GetActivityType;UnitManager.GetActivityType=function(u)local a=read(u);local v=ExposedMembers.SPC_ExpeditionActivity;v.mode='BLOCKED';return a end;publish('RECOVER',true);assert(#acks==0 and sleepCalls==0 and wakeCalls==0)")

    def test_recovery_owned_flag_does_not_inherit_previous_ui_attempt(self):
        l=recovery_bridge();l.execute("publish('SLEEP');assert(sleepCalls==1);noRecoveryAck=true;publish('RECOVER',false,nil,true);assert(acks[#acks].Result=='RECOVERED' and not acks[#acks].Owned and acks[#acks].Sleeping and wakeCalls==0)")

    def test_shutdown_removes_bounded_recovery_poll(self):
        l=recovery_bridge();l.execute("units[41].activity=3;publish('RECOVER',true);assert(not update);shutdown();assert(update==nil);units[41].activity=1;Events.UnitActivityChanged(2,41);assert(#acks==0 and sleepCalls==0 and wakeCalls==0)")


if __name__=='__main__':unittest.main()
