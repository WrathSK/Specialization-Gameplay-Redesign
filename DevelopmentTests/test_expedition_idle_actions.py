"""B215 actual UnitPanel wrapper: idle native controls, not task-owned activity.
Native permission/rendering remains a user-game gate; fixtures model call shape.
"""
import unittest
from test_expedition_spy_task import ui, R


def fixture():
    l = ui('UnitPanel')
    l.execute("""
      panelShutdown()
      Events.GameCoreEventPublishComplete=event();Events.UnitOperationDeactivated=event()
      Refresh=function()calls.Refresh=(calls.Refresh or 0)+1;rendered=GetUnitActionsTable(selected)end
      UnitOperationTypes={TYPE=1};UnitCommandTypes={TYPE=2};OperationResultsTypes={NO_TARGETS=9}
      local function row(hash,key)return {Hash=hash,Description=key,Icon=key,CategoryInUI='INPLACE'}end
      GameInfo.UnitOperations.UNITOPERATION_SKIP_TURN=row(8,'skip')
      GameInfo.UnitOperations.UNITOPERATION_SLEEP=row(9,'sleep')
      GameInfo.UnitCommands={UNITCOMMAND_WAKE=row(10,'wake')}
      ActivityTypes={ACTIVITY_AWAKE=1,ACTIVITY_HOLD=2,ACTIVITY_SLEEP=3}
      UnitManager.GetActivityType=function()return sleeping and 3 or 1 end
      available=true;g_isOkayToProcess=true;requests={};sleeping=false
      UnitManager.CanStartOperation=function(u,h,params,visible,hint)
        assert(params==nil and type(visible)=='boolean' and (visible and hint==nil or not visible and hint==9))
        if throws then error('unavailable')end
        if unknown then return nil end
        return not sleeping and available
      end
      UnitManager.CanStartCommand=function(u,h,visible,results)
        assert(h==10 and type(visible)=='boolean' and (visible and results==nil or not visible and results==true))
        return sleeping and available
      end
      GetUnitActionsTable=function()calls.GetUnitActionsTable=(calls.GetUnitActionsTable or 0)+1;return 'ordinary'end
      UnitManager.RequestOperation=function(u,hash)
       assert(not u.stale,'REQUEST_USED_STALE_UNIT')
       requests[#requests+1]={kind=1,hash=hash,id=u:GetID()}
       if hash==9 then sleeping=true end
      end
      UnitManager.RequestCommand=function(u,hash)
       assert(not u.stale,'REQUEST_USED_STALE_UNIT')
       requests[#requests+1]={kind=2,hash=hash,id=u:GetID()};sleeping=false
      end
    """)
    l.execute((R/'Mod/UI/ExpeditionSpyUnitPanel.lua').read_text())
    return l


class IdleActions(unittest.TestCase):
    def test_idle_skip_sleep_wake_keep_native_rows_and_no_task_lease(self):
        l=fixture();l.execute("""
          phase('ARRIVED');local a=GetUnitActionsTable(team)
          assert(#a.INPLACE==2 and a.INPLACE[1].icon=='skip' and a.INPLACE[2].icon=='sleep')
          a.INPLACE[1].CallbackFunc();assert(requests[1].kind==1 and requests[1].hash==8)
          a.INPLACE[2].CallbackFunc();assert(sleeping and requests[2].hash==9)
          a=GetUnitActionsTable(team);assert(#a.INPLACE==1 and a.INPLACE[1].icon=='wake')
          a.INPLACE[1].CallbackFunc();assert(not sleeping and requests[3].kind==2 and requests[3].hash==10)
          assert(ExposedMembers.SPC_ExpeditionActivity.mode=='NONE' and not calls.GetUnitActionsTable)
          a=GetUnitActionsTable(team);a.SPECIFIC[1].CallbackFunc();assert(routed==1)
        """)

    def test_lock_blocks_new_and_stale_idle_callbacks(self):
        for phase,mode in [('TASK_PREPARING','SLEEP'),('TASK_RUNNING','ASLEEP'),('TASK_COMPLETE','RELEASE'),('HELD','BLOCKED')]:
            with self.subTest(phase=phase):
                l=fixture();l.execute("phase('ARRIVED');old=GetUnitActionsTable(team)")
                l.execute(f"phase('{phase}','{mode}',true)")
                l.execute("local a=GetUnitActionsTable(team);assert(#a.INPLACE==0);for _,v in ipairs(old.INPLACE)do v.CallbackFunc()end;assert(#requests==0)")

    def test_sleep_wake_callback_cannot_release_task_owned_sleep(self):
        l=fixture();l.execute("""
          sleeping=true;phase('ARRIVED');local old=GetUnitActionsTable(team)
          phase('TASK_RUNNING','ASLEEP',true);old.INPLACE[1].CallbackFunc()
          assert(#requests==0 and sleeping)
        """)

    def test_selection_owner_and_mirror_changes_reject_stale_callback(self):
        for change in ["selected=ordinary","selected=otherTeam","selected=nil","team.owner=3","ExposedMembers.SPC_ExpeditionActivity=nil"]:
            with self.subTest(change=change):
                l=fixture();l.execute("phase('ARRIVED');old=GetUnitActionsTable(team);"+change+";old.INPLACE[1].CallbackFunc();assert(#requests==0)")

    def test_native_permission_and_turn_gate_rechecked(self):
        for change in ['available=false','unknown=true','throws=true','g_isOkayToProcess=false','g_isOkayToProcess=nil']:
            with self.subTest(change=change):
                l=fixture();l.execute("phase('ARRIVED');old=GetUnitActionsTable(team);"+change+";old.INPLACE[1].CallbackFunc();assert(#requests==0)")

    def test_nonidle_phases_offer_no_idle_actions(self):
        for phase in ['NAMING','TRAVELLING','FUTURE_UNDEFINED','HELD']:
            with self.subTest(phase=phase):
                fixture().execute(f"phase('{phase}');assert(#GetUnitActionsTable(team).INPLACE==0)")

    def test_unknown_native_permission_keeps_disabled_controls(self):
        for change in ['unknown=true','throws=true']:
            with self.subTest(change=change):
                l=fixture();l.execute("phase('ARRIVED');"+change+";a=GetUnitActionsTable(team);assert(#a.INPLACE>=1 and #requests==0);for _,v in ipairs(a.INPLACE)do assert(v.disabled)end")

    def test_missing_operation_definition_never_fabricates_a_row(self):
        l=fixture();l.execute("phase('ARRIVED');GameInfo.UnitOperations.UNITOPERATION_SLEEP=nil;local a=GetUnitActionsTable(team);assert(#a.INPLACE==1 and a.INPLACE[1].icon=='skip' and #requests==0)")

    def test_ordinary_units_still_use_base_builder(self):
        l=fixture();l.execute("selected=ordinary;assert(GetUnitActionsTable(ordinary)=='ordinary' and calls.GetUnitActionsTable==1)")

class ArrivalRefresh(unittest.TestCase):
    def test_native_availability_changes_without_gate_revision(self):
        l=fixture();l.execute("""
          phase('ARRIVED');available=false;Events.GameCoreEventPublishComplete()
          assert(#rendered.INPLACE==2 and rendered.INPLACE[1].disabled and calls.Refresh==1)
          local rev=ExposedMembers.SPC_ExpeditionActivity.revision
          available=true;Events.GameCoreEventPublishComplete()
          assert(#rendered.INPLACE==2 and calls.Refresh==2)
          for i=1,20 do Events.GameCoreEventPublishComplete()end
          assert(calls.Refresh==2 and ExposedMembers.SPC_ExpeditionActivity.revision==rev and #requests==0)
        """)

    def test_sleep_and_wake_update_without_task_or_diagnostic(self):
        l=fixture();l.execute("""
          phase('ARRIVED');Events.GameCoreEventPublishComplete()
          sleeping=true;Events.UnitActivityChanged(2,40)
          assert(#rendered.INPLACE==1 and rendered.INPLACE[1].icon=='wake')
          sleeping=false;Events.UnitOperationDeactivated(2,40)
          assert(#rendered.INPLACE==2 and #requests==0)
        """)

    def test_replaced_arrival_id_and_selection_rebuild(self):
        l=fixture();l.execute("""
          phase('TRAVELLING');Events.GameCoreEventPublishComplete()
          units[40]=nil;units[52]=team;team.id=52;ExposedMembers.SPC_ExpeditionActivity.unitID=52;phase('ARRIVED')
          Events.UnitSelectionChanged(2,52,true);assert(#rendered.INPLACE==2)
          local n=calls.Refresh;selected=ordinary;Events.GameCoreEventPublishComplete()
          assert(calls.Refresh==n);selected=team;Events.UnitSelectionChanged(2,52,true)
          assert(calls.Refresh==n+1)
        """)

    def test_locked_unknown_other_unit_and_shutdown(self):
        l=fixture();l.execute("""
          phase('ARRIVED');Events.GameCoreEventPublishComplete();local n=calls.Refresh
          available=false;Events.UnitOperationDeactivated(3,40);assert(calls.Refresh==n)
          phase('TASK_RUNNING','ASLEEP',true);ExposedMembers.SPC_ExpeditionActivity.revision=2
          LuaEvents.SPC_ExpeditionActivityChanged();assert(#rendered.INPLACE==0)
          phase('ARRIVED');ExposedMembers.SPC_ExpeditionActivity.revision=3;unknown=true
          Events.GameCoreEventPublishComplete();assert(#rendered.INPLACE==2 and rendered.INPLACE[1].disabled)
          n=calls.Refresh;panelShutdown();unknown=false;available=true
          Events.GameCoreEventPublishComplete();Events.UnitOperationDeactivated(2,40)
          LuaEvents.SPC_ExpeditionActivityChanged();assert(calls.Refresh==n and #requests==0)
        """)

    def test_refresh_reentrancy_is_bounded(self):
        l=fixture();l.execute("""
          local original=Refresh;Refresh=function(...)Events.GameCoreEventPublishComplete();return original(...)end
          phase('ARRIVED');Events.GameCoreEventPublishComplete();assert(calls.Refresh==1)
        """)

if __name__=='__main__':unittest.main()
