"""B191 actual Gameplay Gate + database-hash activity bridge + optional management Window.
Engine writes/events are mocked; native sleep/ready-unit behavior remains USER_GAME_TEST.
"""
from pathlib import Path
import unittest
from test_expedition_spy_task import gate

R = Path(__file__).resolve().parents[1]


def integrated(window=False):
    l = gate(ui=True, window=window)
    l.execute(r"""
      print=function()end;include=function()end;SPCP0=P
      UI=UI or {};PlayerOperations=PlayerOperations or {EXECUTE_SCRIPT=1}
      Game.GetLocalPlayer=function()return 2 end
      function event()
       local e={listeners={}}
       function e.Add(f)e.listeners[f]=true end
       function e.Remove(f)e.listeners[f]=nil end
       return setmetatable(e,{__call=function(self,...)
        local copy={};for f in pairs(self.listeners)do copy[#copy+1]=f end
        for _,f in ipairs(copy)do f(...)end
       end})
      end
      local previousPublish=publish;local previousTurn=turnBegin;local previousChanged=activityChanged
      Events.GameCoreEventPublishComplete=event();Events.LocalPlayerTurnBegin=event();Events.UnitActivityChanged=event()
      LuaEvents=LuaEvents or {};LuaEvents.SPC_ExpeditionActivityChanged=event()
      if previousPublish then Events.GameCoreEventPublishComplete.Add(previousPublish)end
      if previousTurn then Events.LocalPlayerTurnBegin.Add(previousTurn)end
      if previousChanged then LuaEvents.SPC_ExpeditionActivityChanged.Add(previousChanged)end
      ActivityTypes={ACTIVITY_AWAKE=0,ACTIVITY_SLEEP=1,ACTIVITY_HOLD=2,ACTIVITY_OPERATION=3}
      GameInfo.UnitOperations={UNITOPERATION_SLEEP={Hash=70}}
      GameInfo.UnitCommands={UNITCOMMAND_WAKE={Hash=80}}
      UnitOperationTypes.SLEEP=nil;UnitCommandTypes.WAKE=nil;OperationResultsTypes=nil
      sleepCalls=0;wakeCalls=0;activityPackets={};armPackets={};allActivityPackets={};delayedPackets={}
      UnitManager.GetActivityType=function(u)return u.activity or 0 end
      local canOperation=UnitManager.CanStartOperation;local requestOperation=UnitManager.RequestOperation
      UnitManager.CanStartOperation=function(u,op,target,visible,results)
       if op~=70 then return canOperation(u,op,target,visible,results)end
       assert(target==nil and visible==false and results==false);return true
      end
      UnitManager.RequestOperation=function(u,op,...)
       if op~=70 then return requestOperation(u,op,...)end
       assert(u:GetID()==41);sleepCalls=sleepCalls+1
       if not delaySleep then u.activity=1 end
       if onSleep then onSleep()end
       Events.UnitActivityChanged(2,41);Events.GameCoreEventPublishComplete()
       if throwAfterSleep then error('AMBIGUOUS_SLEEP_RESULT')end
      end
      UnitManager.CanStartCommand=function(u,cmd,visible)
       assert(cmd==80 and visible==false);return true
      end
      UnitManager.RequestCommand=function(u,cmd)
       assert(cmd==80 and u:GetID()==41);wakeCalls=wakeCalls+1;u.activity=0
       Events.UnitActivityChanged(2,41);Events.GameCoreEventPublishComplete()
      end
      function deliver(packet)
       handler(2,packet);Events.GameCoreEventPublishComplete()
      end
      UI.RequestPlayerOperation=function(pid,op,packet)
       assert(pid==2 and op==PlayerOperations.EXECUTE_SCRIPT)
       sent=(sent or 0)+1;lastPacket=packet
       if packet.Action=='ACTIVITY' then
        allActivityPackets[#allActivityPackets+1]=packet
        if packet.Result=='ARMED' then armPackets[#armPackets+1]=packet; if deferArm then delayedPackets[#delayedPackets+1]=packet;return end
        else activityPackets[#activityPackets+1]=packet end
        if deferActivity and packet.Result~='ARMED' then delayedPackets[#delayedPackets+1]=packet;return end
       end
       handler(pid,packet)
       -- Publish before the caller returns, exercising synchronous/reentrant ordering.
       Events.GameCoreEventPublishComplete()
      end
      req('CREATE','setup-create');nativeDispatch('setup-travel');arrival(41,true,false)
      units[41].activity=0
      activityContext={SetInitHandler=function(self,f)activityInit=f end,
       SetShutdown=function(self,f)activityShutdown=f end,
       SetUpdate=function(self,f)activityUpdate=f end,ClearUpdate=function()activityUpdate=nil end}
      activityEnvironment=setmetatable({ContextPtr=activityContext},{__index=_G})
      function beginTask(token)
       handler(2,{Action='TASK',Token=token or 'task1',UnitID=41,SampleTurn=currentTurn,NativeOperation=-1,Mission='PEOPLE',MissionX=15,MissionY=8})
       Events.GameCoreEventPublishComplete()
      end
      function view()return ExposedMembers.SPC_ExpeditionActivity end
    """)
    l.eval("function(source)assert(load(source,'ExpeditionSpyActivity','t',activityEnvironment))()end")(
        (R / 'Mod/UI/ExpeditionSpyActivity.lua').read_text())
    l.execute('activityInit()')
    return l


class ActivityIntegration(unittest.TestCase):
    def test_actual_gate_bridge_complete_once_with_window_closed(self):
        l=integrated();l.execute("""
          beginTask();assert(view().phase=='TASK_RUNNING' and view().mode=='ASLEEP' and view().owned)
          assert(view().taskStart==83 and view().taskDue==85 and sleepCalls==1 and not activityUpdate)
          currentTurn=84;ownTurn(2);Events.LocalPlayerTurnBegin();assert(view().taskCompletions==0)
          currentTurn=85;ownTurn(2);Events.GameCoreEventPublishComplete();Events.LocalPlayerTurnBegin()
          ownTurn(2);Events.GameCoreEventPublishComplete()
          assert(view().phase=='ARRIVED' and view().mode=='NONE' and insightWrites==1)
          assert(sleepCalls==1 and wakeCalls==1 and units[41].activity==0 and not activityUpdate)
          assert(properties==0 and nativeCalls==0 and destroys==0 and placeCalls==0 and finishCalls==0)
        """)

    def test_cancel_release_and_restart_uses_fresh_actual_bridge_attempt(self):
        l=integrated();l.execute("""
          beginTask();local oldKey=view().activityKey
          assert(sleepCalls==1 and view().taskDue==85)
          local cities=Players[3]:GetCities();local readCapital=cities.GetCapitalCity
          cities.GetCapitalCity=function()return city end;Players[3].GetCities=function()return cities end
          currentTurn=84;ownTurn(2);Events.GameCoreEventPublishComplete()
          assert(view().phase=='ARRIVED' and wakeCalls==1 and insightWrites==0 and not activityUpdate)
          cities.GetCapitalCity=readCapital;beginTask('retry')
          assert(view().activityKey~=oldKey and view().phase=='TASK_RUNNING' and view().taskDue==86)
          assert(sleepCalls==2 and units[41].activity==1 and not activityUpdate)
          currentTurn=86;ownTurn(2);Events.GameCoreEventPublishComplete()
          assert(view().phase=='ARRIVED' and wakeCalls==2 and insightWrites==1 and not activityUpdate)
        """)

    def test_actual_bridge_keeps_unknown_running_then_releases_unconfirmed_completion(self):
        from test_expedition_missions import MISSION_FIXTURE
        l=integrated();l.execute(MISSION_FIXTURE);l.execute("""
          local p={Action='TASK',Token='work1',UnitID=41,SampleTurn=currentTurn,NativeOperation=-1}
          for k,v in pairs(WORKS)do p[k]=v end
          handler(2,p);Events.GameCoreEventPublishComplete()
          assert(view().phase=='TASK_RUNNING' and sleepCalls==1)
          typeError=true;currentTurn=85;ownTurn(2);Events.GameCoreEventPublishComplete()
          assert(view().phase=='TASK_RUNNING' and view().missionStatus=='UNKNOWN')
          assert(sleepCalls==1 and wakeCalls==0 and insightWrites==0 and not activityUpdate)
          typeError=false;currentTurn=86;ownTurn(2);Events.GameCoreEventPublishComplete()
          assert(view().phase=='HELD' and view().error=='MISSION_COMPLETION_UNCONFIRMED')
          assert(view().mode=='NONE' and wakeCalls==1 and units[41].activity==0 and insightWrites==0 and not activityUpdate)
        """)

    def test_missing_sleep_row_preserves_specific_failure_without_starting_task(self):
        l=integrated();l.execute("""
          GameInfo.UnitOperations.UNITOPERATION_SLEEP=nil;beginTask()
          assert(view().phase=='HELD' and view().mode=='NONE' and not view().taskStart)
          assert(view().taskCompletions==0 and not view().owned and not activityUpdate)
          assert(sleepCalls==0 and wakeCalls==0 and #activityPackets==1)
          assert(activityPackets[1].Detail:find('ACTIVITY_SLEEP_ROW_UNAVAILABLE',1,true))
          assert(view().activityFailure and view().activityFailure:find('ACTIVITY_SLEEP_ROW_UNAVAILABLE',1,true))
          handler(2,{Action='READ',Token='failure-read'})
          assert(ExposedMembers.SPC_ExpeditionGateReply.activityFailure:find('ACTIVITY_SLEEP_ROW_UNAVAILABLE',1,true))
          for i=1,10 do Events.GameCoreEventPublishComplete();Events.LocalPlayerTurnBegin()end
          assert(sleepCalls==0 and wakeCalls==0 and #activityPackets==1 and not view().taskStart)
        """)

    def test_invalid_wake_hash_keeps_release_blocked_and_specific_reason(self):
        l=integrated();l.execute("""
          beginTask();GameInfo.UnitCommands.UNITCOMMAND_WAKE.Hash='80'
          currentTurn=85;ownTurn(2);Events.GameCoreEventPublishComplete()
          assert(view().phase=='HELD' and view().mode=='BLOCKED' and view().owned)
          assert(view().taskCompletions==1 and sleepCalls==1 and wakeCalls==0 and units[41].activity==1)
          assert(view().activityFailure and view().activityFailure:find('ACTIVITY_WAKE_HASH_UNAVAILABLE',1,true))
          for i=1,10 do Events.GameCoreEventPublishComplete();Events.LocalPlayerTurnBegin()end
          assert(sleepCalls==1 and wakeCalls==0 and not activityUpdate)
        """)

    def test_source_loss_after_sleep_before_readback_releases_attempt(self):
        l=integrated();l.execute("""
          delaySleep=true;beginTask();assert(sleepCalls==1 and #activityPackets==0 and activityUpdate)
          units[41].activity=1;city.owner=3;transfer();Events.GameCoreEventPublishComplete()
          assert(view().phase=='HELD' and view().mode=='NONE' and not view().owned and not view().releasePending)
          assert(not view().taskStart and view().taskCompletions==0 and wakeCalls==1 and units[41].activity==0)
          assert(#activityPackets==1 and activityPackets[1].Result=='RELEASED' and not activityUpdate)
        """)

    def test_source_loss_reentrant_inside_native_sleep_releases_once(self):
        l=integrated();l.execute("""
          onSleep=function()city.owner=3;transfer();Events.GameCoreEventPublishComplete()end
          beginTask();assert(view().phase=='HELD' and view().mode=='NONE' and not view().taskStart)
          assert(sleepCalls==1 and wakeCalls==1 and units[41].activity==0 and not activityUpdate)
        """)

    def test_sleep_throw_after_effect_holds_releases_and_never_retries(self):
        l=integrated();l.execute("""
          throwAfterSleep=true;beginTask()
          for i=1,20 do Events.GameCoreEventPublishComplete()end
          assert(view().phase=='HELD' and view().mode=='NONE' and not view().taskStart)
          assert(sleepCalls==1 and wakeCalls==1 and units[41].activity==0 and not activityUpdate)
        """)

    def test_stale_sleep_ack_preserves_ownership_and_releases_without_timer(self):
        l=integrated();l.execute("""
          deferActivity=true;beginTask();assert(#delayedPackets==1 and delayedPackets[1].Result=='ASLEEP')
          currentTurn=84;deferActivity=false;deliver(delayedPackets[1])
          assert(view().phase=='HELD' and view().mode=='NONE' and not view().taskStart)
          assert(view().error=='STALE_ACTIVITY_SAMPLE' and sleepCalls==1 and wakeCalls==1 and units[41].activity==0)
          deliver(delayedPackets[1]);assert(wakeCalls==1 and not activityUpdate and not view().taskStart)
        """)

    def test_late_ack_after_source_loss_cannot_restart_task(self):
        l=integrated();l.execute("""
          deferActivity=true;beginTask();local old=delayedPackets[1]
          deferActivity=false;city.owner=3;transfer();Events.GameCoreEventPublishComplete()
          assert(view().phase=='HELD' and view().mode=='NONE' and wakeCalls==1)
          deliver(old);assert(view().phase=='HELD' and view().mode=='NONE' and not view().taskStart)
          assert(wakeCalls==1 and units[41].activity==0 and not activityUpdate)
        """)

    def test_preexisting_sleep_is_never_claimed_or_woken_on_pending_cancel(self):
        l=integrated();l.execute("""
          units[41].activity=1;deferActivity=true;beginTask();assert(not delayedPackets[1].Owned)
          deferActivity=false;city.owner=3;transfer();Events.GameCoreEventPublishComplete()
          assert(view().phase=='HELD' and view().mode=='NONE' and not view().taskStart)
          assert(sleepCalls==0 and wakeCalls==0 and units[41].activity==1 and not activityUpdate)
        """)

    def test_changed_identity_blocks_release_instead_of_waking_wrong_unit(self):
        l=integrated();l.execute("""
          delaySleep=true;beginTask();units[41].activity=1;units[41].name='wrong'
          city.owner=3;transfer();Events.GameCoreEventPublishComplete()
          assert(view().phase=='HELD' and view().mode=='BLOCKED' and wakeCalls==0 and units[41].activity==1)
          assert(not activityUpdate and not view().taskStart)
        """)

    def test_stale_release_ack_blocks_without_resending_native_wake(self):
        l=integrated();l.execute("""
          beginTask();deferActivity=true;currentTurn=85;ownTurn(2);Events.GameCoreEventPublishComplete()
          assert(wakeCalls==1 and #delayedPackets==1 and delayedPackets[1].Result=='RELEASED')
          currentTurn=86;deferActivity=false;deliver(delayedPackets[1])
          assert(view().phase=='HELD' and view().mode=='BLOCKED' and view().error=='STALE_ACTIVITY_SAMPLE')
          for i=1,20 do Events.GameCoreEventPublishComplete()end
          assert(wakeCalls==1 and sleepCalls==1 and not activityUpdate)
        """)

    def test_identity_change_between_release_readback_and_ack_is_terminal(self):
        l=integrated();l.execute("""
          beginTask();deferActivity=true;currentTurn=85;ownTurn(2);Events.GameCoreEventPublishComplete()
          assert(wakeCalls==1 and delayedPackets[1].Result=='RELEASED')
          units[41].name='changed-between-readback-and-ack';deferActivity=false;deliver(delayedPackets[1])
          assert(view().phase=='HELD' and view().mode=='BLOCKED' and view().error=='TEAM_NAME_UNAVAILABLE')
          for i=1,20 do Events.GameCoreEventPublishComplete()end
          assert(wakeCalls==1 and sleepCalls==1 and not activityUpdate)
        """)

    def test_activity_reply_cannot_overwrite_window_request_even_when_reentrant(self):
        l=integrated(window=True);l.execute("""
          gateOpen();Controls.TaskButton.click()
          local reply=ExposedMembers.SPC_ExpeditionGateReply
          assert(reply.phase=='TASK_PREPARING' and reply.token~='Activity:1')
          assert(view().phase=='TASK_RUNNING' and Controls.Report.text:find('PHASE_TASK_RUNNING'))
          assert(sleepCalls==1 and not update and not activityUpdate)
          local token=reply.token;deliver(activityPackets[1])
          assert(ExposedMembers.SPC_ExpeditionGateReply.token==token and not update)
          Controls.CloseButton.click();currentTurn=85;ownTurn(2);Events.GameCoreEventPublishComplete()
          assert(wakeCalls==1 and view().phase=='ARRIVED' and view().mode=='NONE' and insightWrites==1)
        """)


class PersistentActivityIntegration(unittest.TestCase):
    def restart_bridge(self,l):
        l.execute("activityShutdown();SPCExpeditionSpyGate.Start(P,shared)")
        l.eval("function(source)assert(load(source,'ExpeditionSpyActivity','t',activityEnvironment))()end")((R/'Mod/UI/ExpeditionSpyActivity.lua').read_text())
        l.execute('activityInit()')

    def test_durable_arm_precedes_native_sleep_and_cold_running_keeps_due(self):
        l=integrated();l.execute("""
          local nativeSleep=UnitManager.RequestOperation
          UnitManager.RequestOperation=function(u,op,...)
           if op==70 then local saved=gameProperties.SPC_EXPEDITION_TEAM_P2
            assert(saved.state.activityMode=='ARMED' and saved.state.activityOwned and not saved.state.sleepConfirmed)
           end
           return nativeSleep(u,op,...)
          end
          beginTask();assert(#armPackets==1 and allActivityPackets[1].Result=='ARMED')
          assert(view().taskDue==85 and view().mode=='ASLEEP' and sleepCalls==1)
        """)
        self.restart_bridge(l)
        l.execute("""
          assert(view().mode=='ASLEEP' and view().taskDue==85 and sleepCalls==1 and wakeCalls==0)
          assert(allActivityPackets[#allActivityPackets].Result=='RECOVERED')
          currentTurn=85;ownTurn(2);Events.GameCoreEventPublishComplete()
          assert(view().phase=='ARRIVED' and view().mode=='NONE' and insightWrites==1 and wakeCalls==1 and sleepCalls==1)
          assert(gameProperties.SPC_EXPEDITION_TEAM_P2.state.phase=='ARRIVED' and insightWrites==1)
        """)

    def test_work_instance_and_unconfirmed_due_time_survive_actual_cold_recovery(self):
        from test_expedition_missions import MISSION_FIXTURE
        l=integrated();l.execute(MISSION_FIXTURE);l.execute("""
          local p={Action='TASK',Token='work1',UnitID=41,SampleTurn=currentTurn,NativeOperation=-1}
          for k,v in pairs(WORKS)do p[k]=v end
          handler(2,p);Events.GameCoreEventPublishComplete()
          typeError=true;currentTurn=85;ownTurn(2);Events.GameCoreEventPublishComplete()
          local s=gameProperties.SPC_EXPEDITION_TEAM_P2.state
          assert(s.missionWorkID==12 and s.missionCompletionUnknownTurn==85)
          typeError=false;currentTurn=86
        """)
        self.restart_bridge(l)
        l.execute("""
          assert(view().phase=='HELD' and view().error=='MISSION_COMPLETION_UNCONFIRMED')
          assert(view().mode=='NONE' and wakeCalls==1 and sleepCalls==1 and insightWrites==0 and not activityUpdate)
          local s=gameProperties.SPC_EXPEDITION_TEAM_P2.state
          assert(s.missionWorkID==12 and s.missionCompletionUnknownTurn==85 and s.taskDue==85)
        """)

    def test_unreadable_cold_recovery_reaches_terminal_block_without_guessed_wake(self):
        l=integrated();l.execute("""
          beginTask();UnitManager.GetActivityType=function()error('ACTIVITY_UNREADABLE')end
        """)
        self.restart_bridge(l)
        l.execute("""
          assert(view().phase=='HELD' and view().mode=='BLOCKED' and not view().recovering)
          assert(view().taskCompletions==0 and not view().taskCompleted and sleepCalls==1 and wakeCalls==0)
          assert(units[41].activity==1 and not activityUpdate)
          local packets=#allActivityPackets
          UnitManager.GetActivityType=function(u)return u.activity or 0 end
          for i=1,20 do Events.GameCoreEventPublishComplete();Events.LocalPlayerTurnBegin()end
          assert(#allActivityPackets==packets and wakeCalls==0 and not activityUpdate)
        """)

    def test_stale_cold_recovery_consumes_reply_then_releases_exact_owned_sleep_once(self):
        l=integrated();l.execute("beginTask();deferActivity=true")
        self.restart_bridge(l)
        l.execute("""
          assert(view().mode=='RECOVER' and #delayedPackets==1 and delayedPackets[1].Result=='RECOVERED')
          currentTurn=84;deferActivity=false;deliver(delayedPackets[1])
          assert(view().phase=='HELD' and view().mode=='NONE' and not view().recovering)
          assert(view().taskCompletions==0 and not view().taskCompleted and view().taskDue==85)
          assert(sleepCalls==1 and wakeCalls==1 and units[41].activity==0 and not activityUpdate)
          deliver(delayedPackets[1]);Events.GameCoreEventPublishComplete()
          assert(wakeCalls==1 and view().mode=='NONE' and not view().recovering)
        """)

    def test_source_loss_before_cold_recovery_ack_releases_only_fresh_owned_sleep(self):
        l=integrated();l.execute("beginTask();activityShutdown();SPCExpeditionSpyGate.Start(P,shared);city.token=nil;ownTurn(2)")
        l.eval("function(source)assert(load(source,'ExpeditionSpyActivity','t',activityEnvironment))()end")((R/'Mod/UI/ExpeditionSpyActivity.lua').read_text())
        l.execute("""
          activityInit();assert(view().phase=='HELD' and view().mode=='NONE' and not view().recovering)
          assert(view().taskCompletions==0 and not view().taskCompleted and units[41].activity==0)
          assert(sleepCalls==1 and wakeCalls==1 and not activityUpdate)
        """)

    def test_changed_exact_unit_during_cold_recovery_never_wakes_a_substitute(self):
        for change in ("units[41].name='substitute'", "units[41].owner=3", "units[41].type_=103", "units[41].x=16"):
            with self.subTest(change=change):
                l=integrated();l.execute("beginTask();"+change)
                self.restart_bridge(l)
                l.execute("""
                  assert(view().phase=='HELD' and view().mode=='BLOCKED' and not view().recovering)
                  assert(sleepCalls==1 and wakeCalls==0 and not view().taskCompleted and view().taskCompletions==0)
                  for i=1,10 do Events.GameCoreEventPublishComplete()end
                  assert(wakeCalls==0 and not activityUpdate)
                """)

    def test_failed_arm_store_readback_never_requests_sleep(self):
        l=integrated();l.execute("""
          local write=P.SetProperty
          P.SetProperty=function(o,k,v)if v.state.activityMode=='ARMED' then return end;return write(o,k,v)end
          beginTask();assert(view().phase=='HELD' and view().mode=='BLOCKED' and sleepCalls==0 and wakeCalls==0)
          assert(gameProperties.SPC_EXPEDITION_TEAM_P2.state.activityMode=='SLEEP')
        """)

    def test_delayed_arm_ack_cannot_submit_native_action(self):
        l=integrated();l.execute("""
          deferArm=true;beginTask();assert(#delayedPackets==1 and delayedPackets[1].Result=='ARMED' and sleepCalls==0)
          assert(gameProperties.SPC_EXPEDITION_TEAM_P2.state.activityMode=='SLEEP')
          deferArm=false;deliver(delayedPackets[1]);assert(sleepCalls==1 and view().taskDue==85)
        """)

    def test_load_pending_operation_observes_sleep_without_resubmitting(self):
        l=integrated();l.execute("""
          delaySleep=true;beginTask();units[41].activity=3
          assert(sleepCalls==1 and view().mode=='ARMED' and not view().taskStart)
        """)
        self.restart_bridge(l)
        l.execute("""
          assert(view().mode=='RECOVER' and sleepCalls==1 and activityUpdate)
          units[41].activity=1;Events.UnitActivityChanged(2,41)
          assert(view().mode=='ASLEEP' and view().taskDue==85 and sleepCalls==1 and not activityUpdate)
        """)


if __name__=='__main__':unittest.main()
