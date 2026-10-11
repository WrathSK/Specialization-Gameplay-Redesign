"""B191 actual activity bridge, database action hashes, and bounded activity ownership.
Native sleep/ready-unit behavior remains a user gate.
"""
from pathlib import Path
import unittest
from lupa.lua55 import LuaRuntime
R=Path(__file__).resolve().parents[1]


def bridge():
    l=LuaRuntime(unpack_returned_tuples=True)
    l.execute(r'''
      include=function()end
      SPCP0={IsTestPlayer=function(pid)return pid==2 end}
      ExposedMembers={};turn=81;localOwner=2;packets={};sleepCalls=0;wakeCalls=0;changed=0
      function event()local e={listeners={}};function e.Add(f)e.listeners[f]=true end;function e.Remove(f)e.listeners[f]=nil end
       return setmetatable(e,{__call=function(self,...)for f in pairs(self.listeners)do f(...)end end})end
      Events={GameCoreEventPublishComplete=event(),UnitActivityChanged=event(),LocalPlayerTurnBegin=event()}
      LuaEvents={SPC_ExpeditionActivityChanged=event()};LuaEvents.SPC_ExpeditionActivityChanged.Add(function()changed=changed+1 end)
      ContextPtr={SetInitHandler=function(self,f)init=f end,SetShutdown=function(self,f)shutdown=f end,
       SetUpdate=function(self,f)update=f end,ClearUpdate=function()update=nil end}
      Game={GetLocalPlayer=function()return localOwner end,GetCurrentGameTurn=function()return turn end}
      GameInfo={Units={[1]={UnitType='UNIT_SPC_EXPEDITION_SPY'},[2]={UnitType='UNIT_SPY'}},
       UnitOperations={UNITOPERATION_SLEEP={Hash=70}},UnitCommands={UNITCOMMAND_WAKE={Hash=80}}}
      expectedSleepHash=70;expectedWakeHash=80;sleepChecks=0;wakeChecks=0
      ActivityTypes={ACTIVITY_AWAKE=0,ACTIVITY_SLEEP=1,ACTIVITY_HOLD=2,ACTIVITY_OPERATION=3}
      function unit(id,owner,kind)
       local u={id=id,owner=owner or 2,kind=kind or 1,name='Native Named Spy',x=15,y=8,activity=0,spy=-1}
       function u:GetID()return self.id end;function u:GetOwner()return self.owner end
       function u:GetUnitType()return self.kind end;function u:GetName()return self.name end
       function u:GetX()return self.x end;function u:GetY()return self.y end
       function u:GetSpyOperation()return self.spy end
       return u
      end
      units={[41]=unit(41),[42]=unit(42,2,2)}
      Players={[2]={GetUnits=function()return {FindID=function(self,id)return units[id]end}end}}
      UnitOperationTypes={};UnitCommandTypes={};OperationResultsTypes=nil
      UnitManager={GetActivityType=function(u)if readThrow then error('READ_THROW')end;return u.activity end}
      UnitManager.CanStartOperation=function(u,op,target,visible,results)
       assert(op==expectedSleepHash and target==nil and visible==false and results==false)
       sleepChecks=sleepChecks+1;if mutateSleepRow then GameInfo.UnitOperations.UNITOPERATION_SLEEP.Hash=71 end
       return not sleepDenied end
      UnitManager.RequestOperation=function(u,op)
       assert(op==expectedSleepHash and u.id==41);sleepCalls=sleepCalls+1
       if throwBeforeSleep then error('AMBIGUOUS_BEFORE_SLEEP')end
       if not delaySleep then u.activity=1 end
       Events.UnitActivityChanged(2,41);Events.GameCoreEventPublishComplete()
       if throwAfterSleep then error('AMBIGUOUS_AFTER_SLEEP')end
       if rejectSleep then return false end
      end
      UnitManager.CanStartCommand=function(u,cmd,visible)
       assert(cmd==expectedWakeHash and visible==false);wakeChecks=wakeChecks+1
       if mutateWakeRow then GameInfo.UnitCommands.UNITCOMMAND_WAKE.Hash=81 end
       return not wakeDenied end
      UnitManager.RequestCommand=function(u,cmd)
       assert(cmd==expectedWakeHash and u.id==41);wakeCalls=wakeCalls+1
       if not delayWake then u.activity=0 end
       Events.UnitActivityChanged(2,41);Events.GameCoreEventPublishComplete()
       if throwWake then error('AMBIGUOUS_WAKE')end
      end
      PlayerOperations={EXECUTE_SCRIPT=7}
      function publish(mode,owned,key,releasePending)
       local previous=ExposedMembers.SPC_ExpeditionActivity
       ExposedMembers.SPC_ExpeditionActivity={revision=(previous and previous.revision or 0)+1,
        owner=2,unitID=41,expectedName='Native Named Spy',x=15,y=8,teamKey='team1',
        activityKey=key or 'task1',mode=mode,owned=owned==true,releasePending=releasePending==true,phase=mode=='SLEEP' and 'TASK_PREPARING' or 'TASK_RUNNING',locked=mode~='NONE'}
       Events.GameCoreEventPublishComplete()
      end
      UI={RequestPlayerOperation=function(owner,op,args)
       assert(owner==2 and op==7 and args.OnStart=='SPC_ExpeditionGateRequest' and args.Action=='ACTIVITY')
       assert(args.UnitID==41 and (args.ActivityKey=='task1' or args.ActivityKey=='task2') and type(args.Token)=='string' and #args.Token<=100)
       assert(args.SampleTurn==turn);packets[#packets+1]=args
       if args.Result~='FAILED'then assert(args.NativeOperation==-1)end
       if not noAck then
        if args.Result=='ASLEEP'then publish('ASLEEP',args.Owned)
        elseif args.Result=='RELEASED'then publish('NONE',false)
        else
         local v=ExposedMembers.SPC_ExpeditionActivity
         publish(args.Owned and v.mode~='RELEASE' and 'RELEASE' or 'BLOCKED',args.Owned)
        end
       end
      end}
    ''')
    l.execute((R/'Mod/UI/ExpeditionSpyActivity.lua').read_text())
    l.execute('init()')
    return l


class ActivityBridge(unittest.TestCase):
    def test_no_view_cold_context_never_adopts_or_writes(self):
        l=bridge();l.execute("for i=1,10 do Events.GameCoreEventPublishComplete();Events.LocalPlayerTurnBegin()end;assert(sleepCalls==0 and wakeCalls==0 and #packets==0 and update==nil)")

    def test_exact_sleep_ack_then_release_once_under_reentrant_publications(self):
        l=bridge();l.execute("publish('SLEEP');assert(sleepCalls==1 and #packets==1 and packets[1].Result=='ASLEEP' and packets[1].Owned and update==nil);for i=1,100 do Events.GameCoreEventPublishComplete()end;publish('RELEASE',true);assert(wakeCalls==1 and #packets==2 and packets[2].Result=='RELEASED' and units[42].activity==0 and update==nil);for i=1,100 do Events.GameCoreEventPublishComplete()end;assert(sleepCalls==1 and wakeCalls==1)")

    def test_already_asleep_is_not_owned_and_is_never_woken(self):
        l=bridge();l.execute("units[41].activity=1;publish('SLEEP');assert(sleepCalls==0 and #packets==1 and not packets[1].Owned);publish('NONE');assert(wakeCalls==0 and units[41].activity==1)")

    def test_management_window_independence_and_turn_monitor(self):
        l=bridge();l.execute("publish('SLEEP');managementWindowHidden=true;Events.LocalPlayerTurnBegin();assert(#packets==1 and update==nil);publish('RELEASE',true);assert(wakeCalls==1 and packets[2].Result=='RELEASED')")

    def test_delayed_sleep_readback_no_repeated_request(self):
        l=bridge();l.execute("delaySleep=true;publish('SLEEP');assert(sleepCalls==1 and #packets==0 and update);for i=1,5 do update(.25);Events.GameCoreEventPublishComplete()end;units[41].activity=1;Events.UnitActivityChanged(2,41);assert(sleepCalls==1 and #packets==1 and packets[1].Owned and update==nil)")

    def test_sleep_timeout_unobserved_awake_outcome_blocks_without_writer(self):
        l=bridge();l.execute("delaySleep=true;publish('SLEEP');update(11);assert(sleepCalls==1 and wakeCalls==0 and #packets==2 and packets[1].Result=='FAILED' and packets[1].Owned and packets[1].Detail:find('TIMEOUT') and packets[2].Result=='FAILED' and packets[2].Owned and packets[2].Detail:find('ACTIVITY_SLEEP_OUTCOME_UNKNOWN') and ExposedMembers.SPC_ExpeditionActivity.mode=='BLOCKED' and update==nil)")

    def test_sleep_error_after_effect_releases_once_no_retry(self):
        l=bridge();l.execute("throwAfterSleep=true;publish('SLEEP');assert(sleepCalls==1 and wakeCalls==1 and #packets==2 and packets[1].Result=='FAILED' and packets[1].Owned and packets[2].Result=='RELEASED' and units[41].activity==0)")

    def test_wrong_identity_or_native_mission_never_writes(self):
        for change in ["units[41]=nil", "units[41].id=99", "units[41].owner=3", "units[41].kind=2", "units[41].name='other'", "units[41].x=16", "units[41].spy=9", "units[41].GetSpyOperation=nil", "readThrow=true"]:
            with self.subTest(change=change):
                l=bridge();l.execute(change+";publish('SLEEP');assert(sleepCalls==0 and wakeCalls==0 and #packets==1 and packets[1].Result=='FAILED' and not packets[1].Owned and update==nil)")

    def test_release_unknown_or_wrong_unit_does_not_wake(self):
        for change in ["units[41].owner=3", "units[41].spy=9", "units[41].name='other'", "units[41].activity=3"]:
            with self.subTest(change=change):
                l=bridge();l.execute("publish('SLEEP');"+change+";publish('RELEASE',true);assert(sleepCalls==1 and wakeCalls==0 and #packets==2 and packets[2].Result=='FAILED' and packets[2].Owned);Events.GameCoreEventPublishComplete();assert(#packets==2)")

    def test_already_awake_or_hold_release_has_no_writer(self):
        for activity in [0,2]:
            with self.subTest(activity=activity):
                l=bridge();l.execute(f"units[41].activity={activity};publish('RELEASE',true);assert(wakeCalls==0 and sleepCalls==0 and #packets==1 and packets[1].Result=='RELEASED')")

    def test_unexpected_wake_fails_without_resleep(self):
        l=bridge();l.execute("publish('SLEEP');units[41].activity=0;Events.UnitActivityChanged(2,41);assert(sleepCalls==1 and wakeCalls==0 and #packets==3 and packets[2].Result=='FAILED' and packets[2].Owned and packets[3].Result=='RELEASED')")

    def test_native_mission_during_asleep_is_not_cancelled_or_woken(self):
        l=bridge();l.execute("publish('SLEEP');units[41].spy=9;Events.LocalPlayerTurnBegin();assert(sleepCalls==1 and wakeCalls==0 and packets[2].Result=='FAILED' and packets[3].Result=='FAILED' and update==nil)")

    def test_default_fixture_requires_no_alias_or_optional_result_constants(self):
        l=bridge();l.execute("assert(UnitOperationTypes.SLEEP==nil and UnitCommandTypes.WAKE==nil and OperationResultsTypes==nil);publish('SLEEP');publish('RELEASE',true);assert(sleepChecks==1 and wakeChecks==1 and sleepCalls==1 and wakeCalls==1 and #packets==2)")

    def test_stale_aliases_are_ignored_in_favor_of_database_hash(self):
        l=bridge();l.execute("UnitOperationTypes.SLEEP=700;UnitCommandTypes.WAKE=800;OperationResultsTypes={NO_TARGETS=999};publish('SLEEP');publish('RELEASE',true);assert(sleepCalls==1 and wakeCalls==1 and #packets==2 and packets[2].Result=='RELEASED')")

    def test_valid_signed_and_zero_database_hashes_use_same_eligibility_and_writer_hash(self):
        for sleep_hash, wake_hash in [(-2147483648, -1), (0, 0)]:
            with self.subTest(sleep_hash=sleep_hash, wake_hash=wake_hash):
                l=bridge();l.execute(f"expectedSleepHash={sleep_hash};expectedWakeHash={wake_hash};GameInfo.UnitOperations.UNITOPERATION_SLEEP.Hash=expectedSleepHash;GameInfo.UnitCommands.UNITCOMMAND_WAKE.Hash=expectedWakeHash;publish('SLEEP');publish('RELEASE',true);assert(sleepChecks==1 and wakeChecks==1 and sleepCalls==1 and wakeCalls==1 and #packets==2)")

    def test_indexable_userdata_database_collection_and_row_are_supported(self):
        l=bridge()
        # Lupa exposes these mapping objects as userdata, like a native database adapter.
        l.globals().nativeOperations={"UNITOPERATION_SLEEP": {"Hash": 70}}
        l.globals().nativeCommands={"UNITCOMMAND_WAKE": {"Hash": 80}}
        l.execute("GameInfo.UnitOperations=nativeOperations;GameInfo.UnitCommands=nativeCommands;assert(type(GameInfo.UnitOperations)=='userdata' and type(GameInfo.UnitOperations.UNITOPERATION_SLEEP)=='userdata');publish('SLEEP');publish('RELEASE',true);assert(sleepCalls==1 and wakeCalls==1 and #packets==2 and packets[2].Result=='RELEASED')")

    def test_hash_change_inside_eligibility_cannot_change_the_subsequent_writer(self):
        l=bridge();l.execute("mutateSleepRow=true;mutateWakeRow=true;publish('SLEEP');publish('RELEASE',true);assert(sleepCalls==1 and wakeCalls==1 and #packets==2 and packets[2].Result=='RELEASED')")

    def test_missing_invalid_action_rows_stop_before_native_eligibility_and_writer(self):
        cases = [
            ("TABLE_UNAVAILABLE", "nil"),
            ("TABLE_UNAVAILABLE", "false"),
            ("TABLE_UNAVAILABLE", "'invalid table'"),
            ("TABLE_UNAVAILABLE", "7"),
            ("ROW_UNAVAILABLE", "{}"),
            ("ROW_UNAVAILABLE", "{ROW=false}"),
            ("ROW_UNAVAILABLE", "{ROW='invalid row'}"),
            ("ROW_UNAVAILABLE", "{ROW=7}"),
            ("HASH_UNAVAILABLE", "{ROW={}}"),
            ("HASH_UNAVAILABLE", "{ROW={Hash=false}}"),
            ("HASH_UNAVAILABLE", "{ROW={Hash='70'}}"),
            ("HASH_UNAVAILABLE", "{ROW={Hash=70.5}}"),
            ("HASH_UNAVAILABLE", "{ROW={Hash=0/0}}"),
            ("HASH_UNAVAILABLE", "{ROW={Hash=math.huge}}"),
            ("HASH_UNAVAILABLE", "{ROW={Hash=-math.huge}}"),
        ]
        for action, table, row in [("SLEEP", "UnitOperations", "UNITOPERATION_SLEEP"),
                                   ("WAKE", "UnitCommands", "UNITCOMMAND_WAKE")]:
            for suffix, value in cases:
                with self.subTest(action=action, suffix=suffix, value=value):
                    l=bridge()
                    # A correct alias is deliberately present: invalid DB data must not fall back to it.
                    l.execute("UnitOperationTypes.SLEEP=70;UnitCommandTypes.WAKE=80")
                    if action == "WAKE":
                        l.execute("publish('SLEEP')")
                    l.execute(f"GameInfo.{table}={value.replace('ROW', row)}")
                    l.execute("publish('SLEEP')" if action == "SLEEP" else "publish('RELEASE',true)")
                    packet=1 if action=="SLEEP" else 2
                    prior=0 if action=="SLEEP" else 1
                    l.execute(f"assert(sleepCalls=={prior} and wakeCalls==0 and #packets=={packet} and packets[{packet}].Result=='FAILED' and packets[{packet}].Detail:find('ACTIVITY_{action}_{suffix}',1,true) and packets[{packet}].Owned=={str(action=='WAKE').lower()} and update==nil);assert(sleepChecks=={prior} and wakeChecks==0);for i=1,10 do Events.GameCoreEventPublishComplete()end;assert(#packets=={packet})")

    def test_denied_sleep_or_wake_never_bypasses_guard(self):
        l=bridge();l.execute("sleepDenied=true;publish('SLEEP');assert(sleepChecks==1 and sleepCalls==0 and wakeCalls==0 and packets[1].Result=='FAILED' and not packets[1].Owned and packets[1].Detail:find('ACTIVITY_SLEEP_NOT_ALLOWED',1,true))")
        l=bridge();l.execute("publish('SLEEP');wakeDenied=true;publish('RELEASE',true);assert(wakeChecks==1 and sleepCalls==1 and wakeCalls==0 and packets[2].Result=='FAILED' and packets[2].Owned and packets[2].Detail:find('ACTIVITY_WAKE_NOT_ALLOWED',1,true))")

    def test_missing_native_eligibility_or_writer_api_is_reported_without_native_write(self):
        for action, method in [("SLEEP", "CanStartOperation"), ("SLEEP", "RequestOperation"),
                               ("WAKE", "CanStartCommand"), ("WAKE", "RequestCommand")]:
            with self.subTest(action=action, method=method):
                l=bridge()
                if action=="WAKE":l.execute("publish('SLEEP')")
                l.execute(f"UnitManager.{method}=nil")
                l.execute("publish('SLEEP')" if action=="SLEEP" else "publish('RELEASE',true)")
                packet=1 if action=="SLEEP" else 2
                prior=0 if action=="SLEEP" else 1
                l.execute(f"assert(sleepCalls=={prior} and wakeCalls==0 and #packets=={packet} and packets[{packet}].Result=='FAILED' and packets[{packet}].Detail:find('ACTIVITY_{action}_API_UNAVAILABLE',1,true) and update==nil)")

    def test_delayed_wake_timeout_is_bounded(self):
        l=bridge();l.execute("publish('SLEEP');delayWake=true;publish('RELEASE',true);assert(wakeCalls==1 and update);update(11);assert(wakeCalls==1 and packets[2].Result=='FAILED' and packets[2].Owned and update==nil)")

    def test_ack_unknown_never_repeats_native_action(self):
        l=bridge();l.execute("noAck=true;publish('SLEEP');for i=1,10 do Events.GameCoreEventPublishComplete()end;assert(sleepCalls==1 and #packets==1 and update==nil)")

    def test_unowned_release_malformed_view_and_foreign_owner_never_write(self):
        l=bridge();l.execute("units[41].activity=1;publish('RELEASE',false);assert(wakeCalls==0 and #packets==0 and update==nil)")
        for change in ["localOwner=3", "ExposedMembers.SPC_ExpeditionActivity.activityKey=''", "ExposedMembers.SPC_ExpeditionActivity.teamKey=nil", "ExposedMembers.SPC_ExpeditionActivity.expectedName=nil", "ExposedMembers.SPC_ExpeditionActivity.x=-1"]:
            with self.subTest(change=change):
                l=bridge();l.execute("publish('NONE');"+change+";ExposedMembers.SPC_ExpeditionActivity.mode='SLEEP';Events.GameCoreEventPublishComplete();assert(wakeCalls==0 and sleepCalls==0 and #packets==0 and update==nil)")

    def test_asleep_publish_never_reads_native_activity_but_turn_does(self):
        l=bridge();l.execute("publish('SLEEP');readThrow=true;for i=1,20 do Events.GameCoreEventPublishComplete()end;assert(#packets==1);Events.LocalPlayerTurnBegin();assert(#packets==3 and packets[2].Result=='FAILED' and packets[3].Result=='FAILED')")

    def test_token_uses_existing_cross_context_sequence(self):
        l=bridge();l.execute("ExposedMembers.SPC_ExpeditionGateSequence=37;publish('SLEEP');assert(packets[1].Token=='Activity:38');publish('RELEASE',true);assert(packets[2].Token=='Activity:39')")

    def test_cancel_unacknowledged_sleep_releases_retained_attempt_once(self):
        l=bridge();l.execute("delaySleep=true;publish('SLEEP');assert(sleepCalls==1 and #packets==0 and update);units[41].activity=1;publish('RELEASE',false,nil,true);assert(wakeCalls==1 and #packets==1 and packets[1].Result=='RELEASED' and packets[1].Owned and units[41].activity==0 and update==nil);for i=1,10 do Events.GameCoreEventPublishComplete()end;assert(wakeCalls==1)")

    def test_cancel_after_delayed_ack_preserves_attempt_ownership(self):
        l=bridge();l.execute("noAck=true;publish('SLEEP');assert(sleepCalls==1 and #packets==1 and packets[1].Result=='ASLEEP' and update==nil);publish('RELEASE',false,nil,true);assert(wakeCalls==1 and #packets==2 and packets[2].Result=='RELEASED' and packets[2].Owned and units[41].activity==0)")

    def test_cancel_preexisting_sleep_without_attempt_never_wakes(self):
        l=bridge();l.execute("units[41].activity=1;noAck=true;publish('SLEEP');assert(sleepCalls==0 and not packets[1].Owned);publish('RELEASE',false,nil,true);assert(wakeCalls==0 and #packets==2 and packets[2].Result=='RELEASED' and not packets[2].Owned and units[41].activity==1 and update==nil)")

    def test_pending_release_without_prior_sleep_still_checks_exact_identity(self):
        l=bridge();l.execute("units[41].activity=1;publish('RELEASE',false,nil,true);assert(sleepCalls==0 and wakeCalls==0 and packets[1].Result=='RELEASED' and not packets[1].Owned and units[41].activity==1)")
        for change in ["units[41].name='other'", "units[41].spy=9", "units[41].x=99"]:
            with self.subTest(change=change):
                l=bridge();l.execute(change+";publish('RELEASE',false,nil,true);assert(sleepCalls==0 and wakeCalls==0 and packets[1].Result=='FAILED' and not packets[1].Owned)")

    def test_pending_attempt_does_not_cross_activity_keys(self):
        l=bridge();l.execute("noAck=true;publish('SLEEP');publish('RELEASE',false,'task2',true);assert(sleepCalls==1 and wakeCalls==0 and #packets==2 and packets[2].Result=='RELEASED' and not packets[2].Owned and units[41].activity==1)")

    def test_late_sleep_after_unknown_outcome_stays_blocked_without_automatic_actions(self):
        l=bridge();l.execute("delaySleep=true;publish('SLEEP');publish('RELEASE',false,nil,true);assert(sleepCalls==1 and wakeCalls==0 and #packets==1 and packets[1].Result=='FAILED' and packets[1].Owned and packets[1].Detail:find('ACTIVITY_SLEEP_OUTCOME_UNKNOWN') and ExposedMembers.SPC_ExpeditionActivity.mode=='BLOCKED');units[41].activity=1;Events.UnitActivityChanged(2,41);Events.LocalPlayerTurnBegin();for i=1,10 do Events.GameCoreEventPublishComplete()end;assert(sleepCalls==1 and wakeCalls==0 and #packets==1 and units[41].activity==1 and update==nil)")

    def test_throw_before_observed_effect_keeps_unknown_outcome_blocked(self):
        l=bridge();l.execute("throwBeforeSleep=true;publish('SLEEP');assert(sleepCalls==1 and wakeCalls==0 and #packets==2 and packets[1].Result=='FAILED' and packets[2].Result=='FAILED' and packets[2].Detail:find('ACTIVITY_SLEEP_OUTCOME_UNKNOWN') and ExposedMembers.SPC_ExpeditionActivity.mode=='BLOCKED' and update==nil)")

    def test_removed_lease_and_shutdown_cancel_pending_poll(self):
        l=bridge();l.execute("delaySleep=true;publish('SLEEP');local tick=update;ExposedMembers.SPC_ExpeditionActivity=nil;Events.GameCoreEventPublishComplete();tick(20);assert(sleepCalls==1 and #packets==0 and update==nil);shutdown();Events.GameCoreEventPublishComplete();Events.LocalPlayerTurnBegin();assert(sleepCalls==1 and #packets==0)")


if __name__=='__main__': unittest.main()
