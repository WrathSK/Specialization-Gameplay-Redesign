"""B190 actual invisible activity bridge; native sleep/ready-unit behavior remains a user gate."""
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
      GameInfo={Units={[1]={UnitType='UNIT_SPC_EXPEDITION_SPY'},[2]={UnitType='UNIT_SPY'}}}
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
      UnitOperationTypes={SLEEP=70};UnitCommandTypes={WAKE=80};OperationResultsTypes={NO_TARGETS=99}
      UnitManager={GetActivityType=function(u)if readThrow then error('READ_THROW')end;return u.activity end}
      UnitManager.CanStartOperation=function(u,op,target,visible,results)
       assert(op==70 and target==nil and visible==false and results==99);return not sleepDenied end
      UnitManager.RequestOperation=function(u,op)
       assert(op==70 and u.id==41);sleepCalls=sleepCalls+1
       if throwBeforeSleep then error('AMBIGUOUS_BEFORE_SLEEP')end
       if not delaySleep then u.activity=1 end
       Events.UnitActivityChanged(2,41);Events.GameCoreEventPublishComplete()
       if throwAfterSleep then error('AMBIGUOUS_AFTER_SLEEP')end
       if rejectSleep then return false end
      end
      UnitManager.CanStartCommand=function(u,cmd,visible)assert(cmd==80 and visible==false);return not wakeDenied end
      UnitManager.RequestCommand=function(u,cmd)
       assert(cmd==80 and u.id==41);wakeCalls=wakeCalls+1
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

    def test_denied_sleep_or_wake_never_bypasses_guard(self):
        l=bridge();l.execute("sleepDenied=true;publish('SLEEP');assert(sleepCalls==0 and packets[1].Result=='FAILED' and not packets[1].Owned)")
        l=bridge();l.execute("publish('SLEEP');wakeDenied=true;publish('RELEASE',true);assert(wakeCalls==0 and packets[2].Result=='FAILED' and packets[2].Owned)")

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
