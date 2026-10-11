"""Actual B190 Gameplay lease transitions; native activity itself is tested separately."""
import unittest
from test_expedition_spy_task import gate, ui


def ready():
    l=gate()
    l.execute("""
      req('CREATE','a');nativeDispatch('b');arrival(41,true,false)
      function begin()
       handler(2,{Action='TASK',Token='task',UnitID=41,SampleTurn=currentTurn,NativeOperation=-1})
       return ExposedMembers.SPC_ExpeditionGateReply
      end
      seq=0
      function ack(result,owned,overrides)
       seq=seq+1
       local p={Action='ACTIVITY',Token='ack'..seq,ActivityKey=ExposedMembers.SPC_ExpeditionActivity.activityKey,UnitID=41,
        Result=result,Owned=owned,SampleTurn=currentTurn,NativeOperation=-1,Detail='test'}
       for k,v in pairs(overrides or {})do p[k]=v end
       if result=='ASLEEP' and owned==true and p.UnitID==41 and p.ActivityKey==ExposedMembers.SPC_ExpeditionActivity.activityKey and p.Owned==true and ExposedMembers.SPC_ExpeditionActivity.mode=='SLEEP' then
        handler(2,{Action='ACTIVITY',Token='arm'..seq,ActivityKey=p.ActivityKey,UnitID=41,Result='ARMED',Owned=true,Awake=true,Sleeping=false,NativeOperation=-1,SampleTurn=currentTurn})
       end
       handler(2,p);return ExposedMembers.SPC_ExpeditionActivityReply
      end
    """)
    return l


class ActivityGate(unittest.TestCase):
    def test_pending_sleep_does_not_start_timer_or_complete(self):
        l=ready();l.execute("local r=begin();assert(r.phase=='TASK_PREPARING' and not r.taskStart);currentTurn=85;ownTurn(2);r=req('READ','pending');assert(r.phase=='TASK_PREPARING' and not r.taskStart and r.taskCompletions==0);local v=ExposedMembers.SPC_ExpeditionActivity;assert(v.locked and v.mode=='SLEEP' and not v.owned)")

    def test_ack_starts_two_turns_then_releases_and_unlocks(self):
        l=ready();l.execute("begin();currentTurn=84;local r=ack('ASLEEP',true);assert(r.phase=='TASK_RUNNING' and r.taskDue==86);currentTurn=85;ownTurn(2);assert(ExposedMembers.SPC_ExpeditionActivity.mode=='ASLEEP');currentTurn=86;ownTurn(2);local v=ExposedMembers.SPC_ExpeditionActivity;assert(v.mode=='RELEASE' and v.locked and v.taskCompletions==1);ack('RELEASED',true);v=ExposedMembers.SPC_ExpeditionActivity;assert(v.phase=='TASK_COMPLETE' and v.mode=='NONE' and not v.locked and not v.owned);ownTurn(2);assert(v.taskCompletions==1 and nativeCalls==0 and properties==0)")

    def test_preexisting_sleep_is_not_released(self):
        l=ready();l.execute("begin();ack('ASLEEP',false);currentTurn=85;ownTurn(2);local v=ExposedMembers.SPC_ExpeditionActivity;assert(v.mode=='NONE' and not v.owned and v.taskCompletions==1)")

    def test_stale_key_owner_unit_or_turn_cannot_accept(self):
        for p in ["ActivityKey='other'", "UnitID=40", "Owned=3"]:
            with self.subTest(p=p):
                l=ready();l.execute("begin();local r=ack('ASLEEP',true,{"+p+"});assert(r.error and r.phase=='TASK_PREPARING' and not r.taskStart and not r.activityOwned)")
        l=ready();l.execute("begin();handler(3,{Action='ACTIVITY',Token='foreign',ActivityKey=ExposedMembers.SPC_ExpeditionActivity.activityKey,UnitID=41,Result='ASLEEP',Owned=true,SampleTurn=currentTurn});assert(ExposedMembers.SPC_ExpeditionActivity.mode=='SLEEP')")

    def test_late_sleep_ack_holds_and_releases_without_starting_timer(self):
        l=ready();l.execute("begin();currentTurn=84;local r=ack('ASLEEP',true,{SampleTurn=83});assert(r.phase=='HELD' and r.activityMode=='RELEASE' and r.activityOwned and not r.taskStart)")

    def test_source_loss_before_sleep_ack_preserves_pending_release(self):
        l=ready();l.execute("begin();city.owner=3;transfer();local v=ExposedMembers.SPC_ExpeditionActivity;assert(v.phase=='HELD' and v.mode=='RELEASE' and v.releasePending and not v.owned);assert(ack('ASLEEP',true).error);assert(ExposedMembers.SPC_ExpeditionActivity.mode=='RELEASE');ack('RELEASED',true);assert(ExposedMembers.SPC_ExpeditionActivity.mode=='NONE')")

    def test_invalid_result_does_not_consume_pending_lease(self):
        l=ready();l.execute("begin();assert(ack('OTHER',true).error);assert(ack('RELEASED',true).error);assert(ack('ASLEEP',true).phase=='TASK_RUNNING')")

    def test_duplicate_ack_does_not_restart_timer_or_release(self):
        l=ready();l.execute("begin();ack('ASLEEP',true);currentTurn=84;assert(ack('ASLEEP',true).error);assert(req('READ','read').taskDue==85);currentTurn=85;ownTurn(2);ack('RELEASED',true);assert(ack('RELEASED',true).error);local v=ExposedMembers.SPC_ExpeditionActivity;assert(v.mode=='NONE' and v.taskCompletions==1)")

    def test_failed_sleep_before_attempt_has_no_release(self):
        l=ready();l.execute("begin();local r=ack('FAILED',false);assert(r.phase=='HELD' and r.activityMode=='NONE' and not r.taskStart)")

    def test_failed_sleep_after_ambiguous_attempt_retains_release_ownership(self):
        l=ready();l.execute("begin();local r=ack('FAILED',true);assert(r.phase=='HELD' and r.activityMode=='RELEASE' and r.activityOwned);r=ack('RELEASED',true);assert(r.phase=='HELD' and r.activityMode=='NONE' and not r.activityOwned)")

    def test_source_loss_after_native_sleep_before_ack_preserves_release(self):
        l=ready();l.execute("begin();ack('ARMED',true,{Awake=true,Sleeping=false});city.token=nil;local r=ack('ASLEEP',true);assert(r.phase=='HELD' and r.activityMode=='RELEASE' and r.activityOwned and not r.taskStart);ack('RELEASED',true);assert(ExposedMembers.SPC_ExpeditionActivity.mode=='NONE')")

    def test_source_loss_during_running_releases_exact_unit_without_reward(self):
        l=ready();l.execute("begin();ack('ASLEEP',true);city.owner=3;transfer();local v=ExposedMembers.SPC_ExpeditionActivity;assert(v.phase=='HELD' and v.mode=='RELEASE' and v.taskCompletions==0);ack('RELEASED',true);assert(ExposedMembers.SPC_ExpeditionActivity.mode=='NONE' and properties==0)")

    def test_release_unknown_stops_without_retry(self):
        l=ready();l.execute("begin();ack('ASLEEP',true);currentTurn=85;ownTurn(2);local r=ack('FAILED',true);assert(r.phase=='HELD' and r.activityMode=='BLOCKED');local v=ExposedMembers.SPC_ExpeditionActivity;for i=1,3 do ownTurn(2);req('READ','r'..i)end;assert(ExposedMembers.SPC_ExpeditionActivity.revision==v.revision and v.locked)")

    def test_changed_unit_cannot_be_released_by_gate(self):
        for change in ["units[41].name='wrong'", "units[41].owner=3", "units[41].type_=103", "units[41].x=16"]:
            with self.subTest(change=change):
                l=ready();l.execute("begin();ack('ASLEEP',true);currentTurn=85;ownTurn(2);"+change+";local r=ack('RELEASED',true);assert(r.error and r.activityOwned and r.activityMode=='BLOCKED' and destroys==0)")

    def test_end_clears_mirror_and_late_ack_never_mutates(self):
        l=ready();l.execute("begin();ack('ASLEEP',true);req('END','end',41);assert(ExposedMembers.SPC_ExpeditionActivity.mode=='NONE' and not ExposedMembers.SPC_ExpeditionActivity.unitID);ack('ASLEEP',true);assert(destroys==1 and ExposedMembers.SPC_ExpeditionActivity.phase=='ENDED')")

    def test_cold_context_never_rebuilds_activity_ownership(self):
        l=ready();l.execute("begin();ack('ASLEEP',true);gameProperties={};SPCExpeditionSpyGate.Start(P,shared);local v=ExposedMembers.SPC_ExpeditionActivity;assert(v.mode=='NONE' and not v.unitID);assert(req('READ','cold').unbound and properties==0)")

    def test_unchanged_task_turns_do_not_republish_or_scan_collection(self):
        l=ready();l.execute("begin();ack('ASLEEP',true);local v=ExposedMembers.SPC_ExpeditionActivity;Players[2]:GetUnits().Members=function()error('scan')end;currentTurn=84;ownTurn(2);ownTurn(2);assert(ExposedMembers.SPC_ExpeditionActivity==v and shared.RequestDepth==0)")

    def test_ui_controls_lock_and_release_selected_exact_team(self):
        l=ui('UnitPanel');l.execute("""
          selected=team;phase('ARRIVED');local old=GetUnitActionsTable(team)
          phase('TASK_RUNNING','ASLEEP',true)
          assert(#GetUnitActionsTable(team).SPECIFIC==0 and #GetUnitActionsTable(team).INPLACE==0)
          old.SPECIFIC[1].CallbackFunc();old.SPECIFIC[2].CallbackFunc();assert(routed==0 and not calls.skip)
          LuaEvents.SPC_ExpeditionActivityChanged(1);assert(calls.Refresh==1)
          selected=ordinary;LuaEvents.SPC_ExpeditionActivityChanged(2);assert(calls.Refresh==1 and GetUnitActionsTable(ordinary)=='ordinary')
          selected=team;phase('ARRIVED')
          assert(#GetUnitActionsTable(team).SPECIFIC==2 and #GetUnitActionsTable(team).INPLACE==0)
          panelShutdown();LuaEvents.SPC_ExpeditionActivityChanged(3);assert(calls.Refresh==1)
        """)

if __name__=='__main__':unittest.main()
