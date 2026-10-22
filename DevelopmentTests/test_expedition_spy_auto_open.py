"""B200 exact-team, selection-only native-style automatic menu routing.

Actual helper/chooser Lua with isolated event/native-fact fixtures. Does not
prove native event ordering, city data visibility or UI rendering.
"""
import unittest
from test_expedition_spy_task import ui


class AutomaticSelection(unittest.TestCase):
    def test_own_city_selects_travel_without_native_operation(self):
        l=ui('Chooser')
        l.execute("""
          Events.UnitSelectionChanged(2,40,15,8,0,true,true)
          assert(routed==1 and routes[1].mode=='TRAVEL' and routes[1].id==40)
          assert(not calls.OnUnitSelectionChanged and not calls.skip and not calls.Open)
        """)

    def test_foreign_city_selects_task_without_selecting_or_starting_mission(self):
        l=ui('Chooser')
        l.execute("""
          phase('ARRIVED');selectionCityObject=foreignCity
          Events.UnitSelectionChanged(2,40,15,8,0,true,true)
          assert(routed==1 and routes[1].mode=='TASK' and routes[1].id==40)
          assert(not ExposedMembers.SPC_ExpeditionActivity.taskStart and not calls.skip)
          assert(not calls.OnMissionSelected and not calls.OnConfirmPlacement and not calls.Open)
        """)

    def test_ownership_comes_from_current_city_not_native_plot_owner(self):
        l=ui('Chooser')
        l.execute("""
          phase('ARRIVED');selectionCityObject=foreignCity
          Map.GetPlot=function()return {GetOwner=function()return 2 end}end
          Events.UnitSelectionChanged(2,40,15,8,0,true,true)
          assert(routes[1].mode=='TASK')
        """)

    def test_nonmatching_selected_event_never_routes(self):
        for args in ['2,40,15,8,0,false,true','3,40,15,8,0,true,true',
                     '2,42,15,8,0,true,true','2,40,15,8,0,true,false']:
            with self.subTest(args=args):
                l=ui('Chooser');l.execute("Events.UnitSelectionChanged("+args+");assert(routed==0 and not calls.skip)")

    def test_unknown_current_city_or_native_state_does_not_guess_menu(self):
        for change in ["Cities=nil", "Cities.GetPlotPurchaseCity=function()error('unavailable')end",
                       "selectionCityObject=nil", "Map.GetPlot=function()return nil end",
                       "Players[2].GetCities=function()return {FindID=function()return nil end}end",
                       "homeCity.GetOwner=function()return 3 end", "team.x=16",
                       "team.IsReadyToMove=nil", "team.ready=false", "activityType=nil",
                       "activityType=ActivityTypes.ACTIVITY_SLEEP", "UnitManager.GetActivityType=nil"]:
            with self.subTest(change=change):
                l=ui('Chooser');l.execute(change+";Events.UnitSelectionChanged(2,40,15,8,0,true,true);assert(routed==0 and not calls.skip)")

    def test_pending_travel_task_held_complete_and_unbound_do_not_auto_open(self):
        for phase in ['NAMING','TRAVELLING','TASK_PREPARING','TASK_RUNNING','TASK_COMPLETE','HELD','ENDED','UNKNOWN']:
            with self.subTest(phase=phase):
                l=ui('Chooser');l.execute("phase('"+phase+"');Events.UnitSelectionChanged(2,40,15,8,0,true,true);assert(routed==0 and not calls.skip)")
        for change in ['ExposedMembers.SPC_ExpeditionActivity=nil',
                       'ExposedMembers.SPC_ExpeditionActivity.unitID=42',
                       "phase('ARRIVED','RELEASE',false)"]:
            with self.subTest(change=change):
                l=ui('Chooser');l.execute(change+";Events.UnitSelectionChanged(2,40,15,8,0,true,true);assert(routed==0 and not calls.skip)")

    def test_open_window_marker_prevents_repeat_reads_and_selection_reset(self):
        l=ui('Chooser')
        l.execute("""
          phase('ARRIVED');selectionCityObject=foreignCity
          LuaEvents.SPC_ExpeditionGateOpen.Add(function()ExposedMembers.SPC_ExpeditionGateUIOpenVersion='test' end)
          Events.UnitSelectionChanged(2,40,15,8,0,true,true)
          local reads=cityLookups
          for i=1,12 do Events.UnitSelectionChanged(2,40,15,8,0,true,true)end
          assert(routed==1 and cityLookups==reads)
          -- Window close permits a later genuine selection to reopen.
          ExposedMembers.SPC_ExpeditionGateUIOpenVersion=nil
          Events.UnitSelectionChanged(2,40,15,8,0,true,true)
          assert(routed==2 and routes[2].mode=='TASK')
        """)

    def test_existing_diagnostic_or_manual_window_is_not_replaced(self):
        l=ui('Chooser')
        l.execute("""
          phase('ARRIVED');selectionCityObject=foreignCity
          ExposedMembers.SPC_ExpeditionGateUIOpenVersion='already-open'
          Cities.GetPlotPurchaseCity=function()error('must not read while any panel is open')end
          Events.UnitSelectionChanged(2,40,15,8,0,true,true)
          assert(routed==0)
          -- Explicit actions keep their existing independent path.
          assert(SPCExpeditionSpyUI.Open('TRAVEL',40) and routed==1 and routes[1].mode=='TRAVEL')
        """)

    def test_activity_mode_and_debug_callbacks_stay_suppression_only(self):
        l=ui('Chooser')
        l.execute("""
          phase('ARRIVED');selectionCityObject=foreignCity
          Events.UnitActivityChanged(2,40,ActivityTypes.ACTIVITY_AWAKE)
          GoToProperInterfaceMode(team);Open()
          LuaEvents.GameDebug_Return('EspionageChooser',{selectedSpy=team,isVisible=true})
          assert(routed==0 and not calls.Open and not calls.GoToProperInterfaceMode and not calls.skip)
        """)

    def test_mode_transition_rechecks_city_selection_and_task_lock(self):
        for change in ["selectionCityObject=foreignCity", "selected=ordinary", "phase('TASK_RUNNING','ASLEEP',true)",
                       "ExposedMembers.SPC_ExpeditionGateUIOpenVersion='opened-concurrently'"]:
            with self.subTest(change=change):
                l=ui('Chooser')
                l.execute("phase('ARRIVED');mode=9;onMode=function()"+change+" end;assert(not SPCExpeditionSpyUI.OpenOnSelection(team));assert(routed==0 and not calls.skip)")

    def test_ordinary_and_foreign_units_keep_native_selection_handler(self):
        for selected in ['ordinary','civilian','unit(1,3,50)','nil']:
            with self.subTest(selected=selected):
                l=ui('Chooser');l.execute("selected="+selected+";Events.UnitSelectionChanged(2,41,15,8,0,true,true);assert(calls.OnUnitSelectionChanged==1 and routed==0)")

    def test_shutdown_removes_owned_listener_and_calls_native_shutdown(self):
        l=ui('Chooser')
        l.execute("""
          local n=0;for _ in pairs(Events.UnitSelectionChanged.listeners)do n=n+1 end;assert(n==1)
          panelShutdown();assert(calls.OnShutdown==1)
          Events.UnitSelectionChanged(2,40,15,8,0,true,true);assert(routed==0)
          assert(next(Events.UnitSelectionChanged.listeners)==nil)
        """)


class ActualWindowRouting(unittest.TestCase):
    def fixture(self, arrived=False):
        from test_expedition_spy_actions_ui import normal_window
        l=normal_window(arrived=arrived)
        l.execute("""
          local u=units[selectedID];u.IsReadyToMove=function()return true end
          ActivityTypes={ACTIVITY_AWAKE=0};UnitManager.GetActivityType=function()return 0 end
          InterfaceModeTypes={SELECTION=0};UI.GetInterfaceMode=function()return 0 end
          UI.SetInterfaceMode=function()error('already in selection mode')end
          Cities={GetPlotPurchaseCity=function(plot)
            if plot.x==city.x and plot.y==city.y then return city end
            if plot.x==targetCity.x and plot.y==targetCity.y then return targetCity end
          end}
          setmetatable(LuaEvents.SPC_ExpeditionGateOpen,{__call=function(self,...)gateOpen(...)end})
        """)
        return l

    def test_automatic_travel_preserves_explicit_choice_and_bounded_open(self):
        l=self.fixture()
        l.execute("""
          assert(SPCExpeditionSpyUI.OpenOnSelection(units[40]))
          assert(not ContextPtr.hidden and Controls.NormalConfirmButton.disabled)
          assert(lastPacket.Action=='READ' and nativeCalls==0)
          chooseCity();assert(not Controls.NormalConfirmButton.disabled)
          local requests=sent;local reads=helperCalls
          assert(not SPCExpeditionSpyUI.OpenOnSelection(units[40]))
          assert(sent==requests and helperCalls==reads and not Controls.NormalConfirmButton.disabled)
          Controls.NormalCloseButton.click();assert(ContextPtr.hidden)
          assert(SPCExpeditionSpyUI.OpenOnSelection(units[40]) and Controls.NormalConfirmButton.disabled)
        """)

    def test_automatic_task_keeps_explicit_selection_confirmation_and_close(self):
        l=self.fixture(arrived=True)
        l.execute("""
          local nativeBefore=nativeCalls
          assert(SPCExpeditionSpyUI.OpenOnSelection(units[41]))
          assert(not ContextPtr.hidden and Controls.NormalConfirmButton.disabled)
          assert(lastPacket.Action=='READ' and ExposedMembers.SPC_ExpeditionActivity.phase=='ARRIVED')
          chooseTask();assert(not Controls.NormalConfirmButton.disabled)
          Controls.NormalConfirmButton.click()
          assert(lastPacket.Action=='TASK' and ContextPtr.hidden and nativeCalls==nativeBefore)
          assert(ExposedMembers.SPC_ExpeditionActivity.phase=='TASK_PREPARING')
          assert(not SPCExpeditionSpyUI.OpenOnSelection(units[41]))
        """)


if __name__=='__main__':unittest.main()
