"""B190 actual Gameplay Gate + invisible activity bridge + optional management Window.
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
      UnitOperationTypes.SLEEP=70;UnitCommandTypes.WAKE=80;OperationResultsTypes={NO_TARGETS=99}
      sleepCalls=0;wakeCalls=0;activityPackets={};delayedPackets={}
      UnitManager.GetActivityType=function(u)return u.activity or 0 end
      local canOperation=UnitManager.CanStartOperation;local requestOperation=UnitManager.RequestOperation
      UnitManager.CanStartOperation=function(u,op,target,visible,results)
       if op~=70 then return canOperation(u,op,target,visible,results)end
       assert(target==nil and visible==false and results==99);return true
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
        activityPackets[#activityPackets+1]=packet
        if deferActivity then delayedPackets[#delayedPackets+1]=packet;return end
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
      function beginTask()
       handler(2,{Action='TASK',Token='task1',UnitID=41,SampleTurn=currentTurn,NativeOperation=-1})
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
          assert(view().phase=='TASK_COMPLETE' and view().mode=='NONE' and view().taskCompletions==1)
          assert(sleepCalls==1 and wakeCalls==1 and units[41].activity==0 and not activityUpdate)
          assert(properties==0 and nativeCalls==0 and destroys==0 and placeCalls==0 and finishCalls==0)
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
          assert(wakeCalls==1 and view().phase=='TASK_COMPLETE' and view().mode=='NONE')
        """)


if __name__=='__main__':unittest.main()
