"""Explicit Expedition actions and generic native callback isolation.
B200 actual selection routing is covered in test_expedition_spy_auto_open.
Actual Lua UI helpers/wrappers, mocked Civ VI controls and events. No native mission evidence.
"""
import unittest
from test_expedition_spy_task import ui


class ExplicitActions(unittest.TestCase):
    def test_created_city_dispatch_only_and_arrived_has_two_explicit_modes(self):
        l=ui('UnitPanel')
        l.execute("""
         phase('CREATED');local a=GetUnitActionsTable(team)
         assert(#a.SPECIFIC==2 and not a.SPECIFIC[1].disabled and a.SPECIFIC[2].disabled)
         assert(a.SPECIFIC[1].icon=='ICON_UNITOPERATION_SPY_TRAVEL_NEW_CITY')
         assert(a.SPECIFIC[2].icon=='ICON_UNITOPERATION_SPY_GAIN_SOURCES')
         a.SPECIFIC[2].CallbackFunc();assert(routed==0)
         a.SPECIFIC[1].CallbackFunc();assert(routed==1 and routes[1].mode=='TRAVEL' and routes[1].id==40)
         phase('ARRIVED');a=GetUnitActionsTable(team)
         assert(not a.SPECIFIC[1].disabled and not a.SPECIFIC[2].disabled)
         a.SPECIFIC[2].CallbackFunc();assert(routed==2 and routes[2].mode=='TASK' and routes[2].id==40)
         assert(not calls.GetUnitActionsTable and not calls.skip)
        """)

    def test_complete_is_visible_but_disabled_without_repeat_gameplay_authority(self):
        l=ui('UnitPanel')
        l.execute("""
         phase('ARRIVED');local stale=GetUnitActionsTable(team)
         phase('TASK_COMPLETE');local a=GetUnitActionsTable(team)
         assert(#a.SPECIFIC==2 and a.SPECIFIC[1].disabled and a.SPECIFIC[2].disabled)
         for _,v in ipairs(a.SPECIFIC)do v.CallbackFunc()end
         for _,v in ipairs(stale.SPECIFIC)do v.CallbackFunc()end
         assert(routed==0 and not calls.skip and not calls.GetUnitActionsTable)
        """)

    def test_activity_transition_locks_have_no_actions_and_reject_stale_callbacks(self):
        for state in [('TASK_PREPARING','SLEEP',True),('TASK_RUNNING','ASLEEP',True),('TASK_COMPLETE','RELEASE',False),('HELD','BLOCKED',False)]:
            with self.subTest(state=state):
                l=ui('UnitPanel')
                l.execute("phase('ARRIVED');stale=GetUnitActionsTable(team)")
                phase,mode,locked=state
                l.execute(f"phase('{phase}','{mode}',{str(locked).lower()})")
                l.execute("""
                 local a=GetUnitActionsTable(team);local n=0
                 for _,area in ipairs({'primaryArea','secondaryArea'})do
                  for _,category in ipairs(a.displayOrder[area])do n=n+#a[category]end
                 end
                 assert(n==0)
                 stale.SPECIFIC[1].CallbackFunc();stale.SPECIFIC[2].CallbackFunc()
                 OnUnitActionClicked(99,9);OnUnitActionClicked_CancelSpyMission()
                 assert(routed==0 and not calls.skip and not calls.OnUnitActionClicked and not calls.OnUnitActionClicked_CancelSpyMission)
                """)

    def test_missing_or_unmatched_activity_view_never_exposes_actions(self):
        for change in ["ExposedMembers.SPC_ExpeditionActivity=nil", "ExposedMembers.SPC_ExpeditionActivity.owner=3", "ExposedMembers.SPC_ExpeditionActivity.unitID=42"]:
            with self.subTest(change=change):
                l=ui('UnitPanel')
                l.execute("phase('ARRIVED');local stale=GetUnitActionsTable(team);"+change+";local a=GetUnitActionsTable(team);assert(#a.SPECIFIC==0 and #a.INPLACE==0);stale.SPECIFIC[1].CallbackFunc();stale.SPECIFIC[2].CallbackFunc();assert(routed==0 and not calls.skip)")

    def test_unknown_phase_is_unavailable_and_never_guessed_as_created_or_arrived(self):
        l=ui('UnitPanel')
        l.execute("""
         phase('FUTURE_UNDEFINED');local a=GetUnitActionsTable(team)
         for _,v in ipairs(a.SPECIFIC)do assert(v.disabled);v.CallbackFunc()end
         assert(not SPCExpeditionSpyUI.CanOpen('TRAVEL',team) and not SPCExpeditionSpyUI.CanOpen('TASK',team))
         assert(routed==0 and not calls.skip)
        """)

    def test_captured_buttons_cannot_open_another_team_or_ordinary_unit(self):
        for selected in ['otherTeam','ordinary','nil']:
            with self.subTest(selected=selected):
                l=ui('UnitPanel')
                l.execute("phase('ARRIVED');local old=GetUnitActionsTable(team);selected="+selected+";old.SPECIFIC[1].CallbackFunc();old.SPECIFIC[2].CallbackFunc();assert(routed==0 and not calls.skip)")

    def test_explicit_open_rechecks_selection_after_mode_transition(self):
        l=ui('UnitPanel')
        l.execute("""
         phase('ARRIVED');mode=9;onMode=function()selected=otherTeam end
         assert(SPCExpeditionSpyUI.Open('TASK',40)==false)
         assert(mode==InterfaceModeTypes.SELECTION and routed==0 and not calls.skip)
        """)

    def test_explicit_open_rechecks_lock_after_mode_transition(self):
        l=ui('UnitPanel')
        l.execute("""
         phase('ARRIVED');mode=9;onMode=function()phase('TASK_RUNNING','ASLEEP',true)end
         assert(SPCExpeditionSpyUI.Open('TRAVEL',40)==false and routed==0)
        """)

    def test_invalid_mode_and_wrong_id_reject_without_native_operation(self):
        l=ui('UnitPanel')
        l.execute("""
         phase('ARRIVED')
         assert(SPCExpeditionSpyUI.Open('MISSION',40)==false)
         assert(SPCExpeditionSpyUI.Open('TASK',42)==false)
         assert(SPCExpeditionSpyUI.Open(nil,40)==false)
         assert(routed==0 and not calls.skip)
        """)

    def test_generic_native_unit_buttons_suppress_without_report_even_when_unlocked(self):
        l=ui('UnitPanel')
        l.execute("""
         phase('ARRIVED');OnUnitActionClicked(99,9);OnUnitActionClicked_CancelSpyMission()
         assert(routed==0 and not calls.OnUnitActionClicked and not calls.OnUnitActionClicked_CancelSpyMission)
         selected=ordinary;OnUnitActionClicked(99,9);OnUnitActionClicked_CancelSpyMission()
         assert(calls.OnUnitActionClicked==1 and calls.OnUnitActionClicked_CancelSpyMission==1 and routed==0)
        """)

    def test_generic_native_chooser_callbacks_never_open_custom_window(self):
        l=ui('Chooser')
        l.execute("""
         phase('ARRIVED');Open();GoToProperInterfaceMode(team)
         LuaEvents.GameDebug_Return('EspionageChooser',{selectedSpy=team,isVisible=true})
         Controls.ConfirmButton.click();OnMissionSelected();OnCounterspySelected();TeleportToSelectedCity()
         assert(routed==0 and not calls.Open and not calls.GoToProperInterfaceMode and not calls.TeleportToSelectedCity)
         assert(not calls.OnConfirmPlacement and not calls.OnMissionSelected and not calls.OnCounterspySelected and not calls.skip)
         selected=ordinary;Open();Controls.ConfirmButton.click()
         assert(calls.Open==1 and calls.OnConfirmPlacement==1)
        """)

    def test_native_popup_callbacks_never_open_custom_window_or_run_mission(self):
        l=ui('Popup')
        l.execute("""
         phase('ARRIVED');LuaEvents.EspionageChooser_ShowMissionBriefing(9,40,{})
         Controls.AcceptButton.click();LuaEvents.UnitPanel_CancelMission(40);Controls.AbortButton.click();RenewMission(team,9,1,1)
         assert(routed==0 and not calls.OnAccept and not calls.OnAbort and not calls.RenewMission and not calls.skip)
         selected=ordinary;LuaEvents.EspionageChooser_ShowMissionBriefing(9,41,{})
         Controls.AcceptButton.click();RenewMission(ordinary,9,1,1)
         assert(calls.OnShowMissionBriefing==1 and calls.OnAccept==1 and calls.RenewMission==1)
        """)


def normal_window(arrived=False):
    from test_expedition_spy_task import gate
    l=gate(ui=True,window=True)
    l.globals().print=lambda *args:None
    l.execute("""
     -- Exercise the real CREATE entry, including its ordinary-Spy audit and
     -- asynchronous-name confirmation. A direct req('CREATE') omits that state.
     function chooseCity(index)
      local row=instanceManagers.SPCExpeditionDestination.instances[index or 1]
      assert(row,'explicit city choice requires an available row');row.DestinationButton.click()
     end
     function chooseTask()
      local row=instanceManagers.SPCExpeditionMission.instances[1]
      assert(row,'explicit task choice requires an available row');row.MissionButton.click()
     end
     gateOpen();Controls.CreateButton.click()
     assert(ExposedMembers.SPC_ExpeditionGateReply.phase=='CREATED' and nameConfirmCalls==1)
     selectedID=40;UI.GetHeadSelectedUnit=function()return units[selectedID]end
     Controls.CloseButton.click();assert(ContextPtr.hidden)
    """)
    if arrived:
        l.execute("nativeDispatch('normal-window-travel');arrival(41,true,false);selectedID=41")
    return l


class ExplicitWindow(unittest.TestCase):
    def test_travel_entry_is_not_diagnostic_and_dispatch_requires_explicit_confirm(self):
        l=normal_window()
        l.execute("""
         gateOpen('TRAVEL',40);chooseCity()
         assert(not ContextPtr.hidden and not Controls.NormalPanel.hidden and Controls.DiagnosticPanel.hidden)
         assert(not Controls.NormalCurrentSlot.hidden and not Controls.NormalConfirmButton.disabled)
         assert(nativeCalls==0 and lastPacket.Action=='READ')
         Controls.NormalConfirmButton.click()
         assert(lastPacket.Action=='DISPATCH' and nativeCalls==1 and placeCalls==0 and properties==0)
        """)

    def test_task_entry_hides_destination_controls_and_starts_only_on_confirm(self):
        l=normal_window(arrived=True)
        l.execute("""
         local nativeBefore=nativeCalls;gateOpen('TASK',41);chooseTask()
         assert(not ContextPtr.hidden and not Controls.NormalPanel.hidden and Controls.DiagnosticPanel.hidden)
         assert(Controls.NormalTargetLabel.hidden and Controls.DestinationStack.hidden and not Controls.MissionStack.hidden)
         assert(not Controls.NormalConfirmButton.disabled and lastPacket.Action=='READ')
         assert(ExposedMembers.SPC_ExpeditionActivity.phase=='ARRIVED')
         Controls.NormalConfirmButton.click()
         assert(lastPacket.Action=='TASK' and ExposedMembers.SPC_ExpeditionActivity.phase=='TASK_PREPARING')
         assert(not ExposedMembers.SPC_ExpeditionActivity.taskStart and nativeCalls==nativeBefore and properties==0)
        """)

    def test_opened_normal_window_cannot_submit_after_selection_changes(self):
        l=normal_window(arrived=True)
        l.execute("""
         gateOpen('TASK',41);chooseTask();local before=sent;selectedID=99
         Controls.NormalConfirmButton.click()
         assert(sent==before and ExposedMembers.SPC_ExpeditionActivity.phase=='ARRIVED' and properties==0)
        """)

    def test_opened_normal_window_cannot_submit_after_activity_locks(self):
        l=normal_window(arrived=True)
        l.execute("""
         gateOpen('TASK',41);chooseTask();local before=sent
         local v=ExposedMembers.SPC_ExpeditionActivity;v.mode='ASLEEP';v.locked=true;v.phase='TASK_RUNNING'
         activityChanged();Controls.NormalConfirmButton.click()
         assert(Controls.NormalConfirmButton.disabled and sent==before and properties==0)
        """)

    def test_wrong_entry_unit_and_unknown_mode_do_not_open_or_submit(self):
        l=normal_window(arrived=True)
        l.execute("""
         local before=sent;gateOpen('TASK',40);assert(ContextPtr.hidden and sent==before)
         gateOpen('UNRECOGNIZED',41);assert(ContextPtr.hidden and sent==before)
        """)

    def test_no_argument_entry_preserves_explicit_p0_diagnostic_controls(self):
        l=normal_window()
        l.execute("""
         gateOpen();assert(not ContextPtr.hidden and not Controls.DiagnosticPanel.hidden and Controls.NormalPanel.hidden)
         assert(lastPacket.Action=='READ' and nativeCalls==0 and properties==0)
        """)

    def test_pending_native_dispatch_reply_is_not_cancelled_by_close_or_duplicate_click(self):
        l=normal_window()
        l.execute("""
         gateOpen('TRAVEL',40);chooseCity();deferred=true;Controls.NormalConfirmButton.click()
         local packet=lastPacket;local before=sent
         assert(packet.Action=='DISPATCH' and nativeCalls==0)
         Controls.CloseButton.click();Controls.NormalConfirmButton.click()
         assert(not ContextPtr.hidden and sent==before and nativeCalls==0)
         handler(2,packet);deferred=false;publish()
         assert(nativeCalls==1 and ContextPtr.hidden and ExposedMembers.SPC_ExpeditionActivity.phase=='TRAVELLING')
         publish();assert(nativeCalls==1 and properties==0 and destroys==0)
        """)

    def test_hidden_diagnostic_callbacks_cannot_submit_from_normal_view(self):
        for mode in ['TRAVEL','TASK']:
            with self.subTest(mode=mode):
                l=normal_window(arrived=True)
                l.execute("gateOpen('"+mode+"',41);before=sent")
                l.execute("""
                 for _,name in ipairs({'CreateButton','EndButton','ArmButton','TaskButton','TravelButton','RefreshButton','PreviousButton','NextButton'})do
                  Controls[name].click()
                 end
                 assert(sent==before and ExposedMembers.SPC_ExpeditionActivity.phase=='ARRIVED' and destroys==0)
                """)


if __name__=='__main__':unittest.main()
