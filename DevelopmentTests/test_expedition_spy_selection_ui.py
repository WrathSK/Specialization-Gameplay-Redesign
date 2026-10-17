"""B199 explicit selection and task-acknowledgement presentation regressions.

Runs actual Window/Gate Lua. Native rendering and icon availability remain the
user-game UI gate; no gameplay/persistence behavior is simulated as native PASS.
"""
from pathlib import Path
import unittest
import xml.etree.ElementTree as ET
from test_expedition_spy_sidebar_ui import sidebar
from test_expedition_spy_locations import add_locations

R=Path(__file__).resolve().parents[1]


class Selection(unittest.TestCase):
    def test_relocation_open_and_reopen_require_explicit_city_choice(self):
        lua=sidebar(second_target=True)
        lua.execute("""
          for attempt=1,2 do
           gateOpen('TRAVEL',40)
           local rows=instanceManagers.SPCExpeditionDestination.instances
           assert(#rows==2 and Controls.NormalConfirmButton.disabled and Controls.NormalMissionGrid.hidden)
           local before=sent;Controls.NormalConfirmButton.click()
           assert(sent==before and nativeCalls==0)
           rows[2].DestinationButton.click()
           assert(not Controls.NormalConfirmButton.disabled and not Controls.NormalMissionGrid.hidden)
           assert(Controls.NormalCityName.text:find('第二目标',1,true))
           for _,row in ipairs(rows)do assert(row.SelectorBrace.hidden)end
           Controls.NormalCancelButton.click();assert(ContextPtr.hidden and sent==before)
          end
          assert(properties==0 and placeCalls==0)
        """)

    def test_task_open_and_reopen_require_explicit_task_choice(self):
        lua=sidebar(arrived=True)
        lua.execute("""
          for attempt=1,2 do
           gateOpen('TASK',41)
           local row=instanceManagers.SPCExpeditionMission.instances[1]
           assert(Controls.NormalConfirmButton.disabled and row.SelectorBrace.hidden)
           assert(not row.MissionContent.hidden and not Controls.NormalMissionGrid.hidden)
           local before=sent;Controls.NormalConfirmButton.click()
           assert(sent==before and ExposedMembers.SPC_ExpeditionActivity.phase=='ARRIVED')
           row.MissionButton.click()
           assert(not Controls.NormalConfirmButton.disabled and not row.SelectorBrace.hidden)
           Controls.NormalCancelButton.click();assert(ContextPtr.hidden and sent==before)
          end
          assert(nativeCalls==0 and properties==0)
        """)

    def test_relocation_drawer_is_readonly_mission_preview_not_travel_duration(self):
        lua=sidebar()
        lua.execute("""
          gateOpen('TRAVEL',40);chooseCity()
          local row=instanceManagers.SPCExpeditionMission.instances[1]
          assert(Controls.NormalTravelTime.text=='4' and row.MissionTurns.text=='2')
          assert(row.MissionName.text:find('MISSION_PEOPLE_NAME',1,true))
          assert(Controls.NormalDrawerTitle.text:find('NORMAL_MISSION_PREVIEW',1,true))
          assert(row.MissionIcon.hidden and row.MissionCivilizationIcon.icon=='ICON_CIVILIZATION_TARGET')
          assert(row.MissionButton.disabled and row.SelectorBrace.hidden and not row.MissionContent.hidden)
          local before=sent;local reads=helperCalls;row.MissionButton.click()
          assert(sent==before and helperCalls==reads and nativeCalls==0)
          assert(ExposedMembers.SPC_ExpeditionActivity.phase=='CREATED')
          Controls.NormalConfirmButton.click()
          assert(lastPacket.Action=='DISPATCH' and nativeCalls==1 and ContextPtr.hidden)
        """)

    def test_stale_selected_task_callback_cannot_reselect_after_reopen(self):
        lua=sidebar(arrived=True)
        lua.execute("""
          gateOpen('TASK',41)
          local old=instanceManagers.SPCExpeditionMission.instances[1].MissionButton.click
          old();assert(not Controls.NormalConfirmButton.disabled)
          Controls.NormalCancelButton.click();gateOpen('TASK',41)
          local before=sent;old();Controls.NormalConfirmButton.click()
          assert(Controls.NormalConfirmButton.disabled and sent==before)
          assert(ExposedMembers.SPC_ExpeditionActivity.phase=='ARRIVED' and properties==0)
        """)

    def test_selection_refresh_and_resize_do_not_choose_for_user(self):
        for mode,unit in [('TRAVEL',40),('TASK',41)]:
            with self.subTest(mode=mode):
                lua=sidebar(arrived=mode=='TASK')
                lua.execute(f"gateOpen('{mode}',{unit})")
                lua.execute("""
                  local before=sent;local reads=helperCalls
                  activityChanged();publish();turnBegin();systemUpdate(SystemUpdateUI.ScreenResize)
                  assert(Controls.NormalConfirmButton.disabled and sent==before and helperCalls==reads)
                  Controls.NormalConfirmButton.click();assert(sent==before and nativeCalls==0)
                """)

    def test_unselected_mission_content_is_not_inside_selection_overlay(self):
        root=ET.parse(R/'Mod/UI/ExpeditionSpyWindow.xml').getroot()
        instance=root.find("./Instance[@Name='SPCExpeditionMission']")
        content=instance.find(".//*[@ID='MissionContent']")
        brace=instance.find(".//*[@ID='SelectorBrace']")
        self.assertIsNotNone(content);self.assertIsNotNone(brace)
        self.assertNotIn(content,list(brace.iter()))
        self.assertIsNotNone(content.find(".//*[@ID='MissionName']"))


class LocationPresentation(unittest.TestCase):
    def test_unknown_snapshot_is_visible_and_does_not_trigger_extra_reads(self):
        lua=sidebar();add_locations(lua)
        lua.execute("""
          locationBuildings.GetGreatWorkInSlot=nil
          gateOpen('TRAVEL',40)
          local row=instanceManagers.SPCExpeditionDestination.instances[1]
          assert(not row.LocationNotice.hidden and row.DestinationButton.sizey==90)
          assert(row.LocationNotice.text:find('NORMAL_LOCATIONS_INCOMPLETE',1,true))
          assert(not row.LocationNotice.tooltip:find('LOCATION_READER_UNAVAILABLE',1,true))
          assert(Controls.NormalLocationNotice.hidden)
          chooseCity();assert(not Controls.NormalLocationNotice.hidden)
          local reads=buildingLocationReads;local districts=districtReads;local helpers=helperCalls;local requests=sent
          activityChanged();publish();turnBegin();systemUpdate(SystemUpdateUI.ScreenResize)
          assert(buildingLocationReads==reads and districtReads==districts and helperCalls==helpers and sent==requests)
          assert(not Controls.NormalConfirmButton.disabled)
          Controls.NormalConfirmButton.click();assert(nativeCalls==1 and ContextPtr.hidden and properties==0)
        """)

    def test_readable_snapshot_keeps_compact_rows_and_no_incomplete_notice(self):
        lua=sidebar();add_locations(lua)
        lua.execute("""
          gateOpen('TRAVEL',40);chooseCity()
          local row=instanceManagers.SPCExpeditionDestination.instances[1]
          assert(row.LocationNotice.hidden and row.DestinationButton.sizey==72)
          assert(Controls.NormalLocationNotice.hidden and not Controls.NormalConfirmButton.disabled)
          assert(properties==0 and nativeCalls==0)
        """)

    def test_wonder_uses_actual_atlas_when_available_and_generic_icon_when_unknown(self):
        cases={
            "return 0,0,'TestWonder.dds'":'ICON_BUILDING_PYRAMIDS',
            'return nil,nil,nil':'ICON_DISTRICT_WONDER',
            "return 0,0,''":'ICON_DISTRICT_WONDER',
            "error('atlas unknown')":'ICON_DISTRICT_WONDER',
        }
        for expression,expected in cases.items():
            with self.subTest(expression=expression):
                lua=sidebar();add_locations(lua);lua.globals().expectedWonderIcon=expected
                lua.execute("IconManager={FindIconAtlas=function(self,icon,size)assert(size==32 or size==40);"+expression+" end}")
                lua.execute("""
                  gateOpen('TRAVEL',40);chooseCity()
                  local icons=instanceManagers.SPCExpeditionDestination.instances[1].iconPool.instances
                  assert(icons[1].CivilizationIcon.icon=='ICON_CIVILIZATION_TARGET')
                  assert(icons[2].WorksIcon.icon=='ICON_GREATWORKOBJECT_WRITING')
                  assert(icons[3].WonderIcon.icon==expectedWonderIcon)
                  assert(icons[3].DistrictIcon.tooltip==Locale.Lookup('LOC_BUILDING_PYRAMIDS'))
                  assert(not Controls.NormalConfirmButton.disabled and properties==0 and nativeCalls==0)
                """)

    def test_missing_atlas_api_does_not_invent_an_asset_or_block_dispatch(self):
        lua=sidebar();add_locations(lua)
        lua.execute("""
          IconManager=nil;gateOpen('TRAVEL',40);chooseCity()
          local icons=instanceManagers.SPCExpeditionDestination.instances[1].iconPool.instances
          assert(icons[3].WonderIcon.icon=='ICON_DISTRICT_WONDER')
          Controls.NormalConfirmButton.click();assert(nativeCalls==1 and ContextPtr.hidden and properties==0)
        """)


class MissionIconAndUnknownDisplay(unittest.TestCase):
    def test_header_and_cards_use_mission_assets_without_a_universal_center_icon(self):
        lua=sidebar();add_locations(lua)
        lua.execute("""
          IconManager={FindIconAtlas=function(self,name,size)return 0,0,'fixture.dds' end}
          gateOpen('TRAVEL',40);chooseCity()
          local icons=instanceManagers.SPCExpeditionDestination.instances[1].iconPool.instances
          assert(icons[1].CivilizationIcon.icon=='ICON_CIVILIZATION_TARGET' and not icons[1].CivilizationIcon.hidden)
          assert(icons[1].WorksIcon.hidden and icons[1].WonderIcon.hidden)
          assert(icons[2].WorksIcon.icon=='ICON_GREATWORKOBJECT_WRITING' and not icons[2].WorksIcon.hidden)
          assert(icons[3].WonderIcon.icon=='ICON_BUILDING_PYRAMIDS' and not icons[3].WonderIcon.hidden)
          local cards=instanceManagers.SPCExpeditionMission.instances
          assert(cards[1].MissionCivilizationIcon.icon=='ICON_CIVILIZATION_TARGET' and cards[1].MissionIcon.hidden)
          assert(cards[2].MissionIcon.icon=='ICON_GREATWORKOBJECT_WRITING')
          assert(cards[3].MissionIcon.icon=='ICON_BUILDING_PYRAMIDS')
          assert(properties==0 and nativeCalls==0)
        """)
        root=ET.parse(R/'Mod/UI/ExpeditionSpyWindow.xml').getroot()
        district=root.find("./Instance[@Name='SPCExpeditionDistrict']")
        sizes={e.get('ID'):e.get('IconSize') for e in district.iter() if e.tag=='Image'}
        self.assertEqual(sizes,{'WonderIcon':'32','WorksIcon':'20','CivilizationIcon':'30'})

    def test_mission_cards_preserve_per_category_known_and_unknown_states(self):
        lua=sidebar();add_locations(lua)
        lua.execute("""
          targetCity.IsCapital=function()return nil end
          gateOpen('TRAVEL',40);chooseCity()
          local cards=instanceManagers.SPCExpeditionMission.instances
          assert(cards[1].MissionDetails.text:find('MISSION_TARGET_UNKNOWN',1,true))
          assert(cards[2].MissionDetails.text:find('MISSION_AVAILABLE',1,true))
          assert(cards[3].MissionDetails.text:find('MISSION_AVAILABLE',1,true))
          Controls.NormalCancelButton.click()
          targetCity.IsCapital=function()return false end;targetCity.GetBuildings=nil
          gateOpen('TRAVEL',40);chooseCity();cards=instanceManagers.SPCExpeditionMission.instances
          assert(cards[1].MissionDetails.text:find('MISSION_NO_TARGET',1,true))
          assert(cards[2].MissionDetails.text:find('MISSION_TARGET_UNKNOWN',1,true))
          assert(cards[3].MissionDetails.text:find('MISSION_TARGET_UNKNOWN',1,true))
          assert(properties==0 and nativeCalls==0)
        """)

    def test_unknown_activity_fact_is_visible_without_error_or_reward_claim(self):
        lua=sidebar(arrived=True)
        lua.execute("""
          gateOpen('TASK',41)
          local a=ExposedMembers.SPC_ExpeditionActivity
          a.missionStatus='UNKNOWN';a.missionReason='MISSION_WORK_TYPE_UNAVAILABLE'
          activityChanged()
          assert(Controls.NormalSummary.text:find('MISSION_FACTS_UNKNOWN',1,true))
          assert(ExposedMembers.SPC_ExpeditionActivity.phase=='ARRIVED' and properties==0 and nativeCalls==0)
        """)


class AcceptedTaskClose(unittest.TestCase):
    def test_synchronous_exact_acceptance_closes_without_cancelling_task(self):
        lua=sidebar(arrived=True)
        lua.execute("""
          gateOpen('TASK',41);chooseTask();Controls.NormalConfirmButton.click()
          local packet=lastPacket;local a=ExposedMembers.SPC_ExpeditionActivity
          assert(packet.Action=='TASK' and ContextPtr.hidden and a.phase=='TASK_PREPARING')
          assert(a.activityKey:sub(1,#a.teamKey)==a.teamKey and a.activityKey:match(':attempt%d+$') and not a.taskStart and not a.taskDue)
          handler(2,{Action='ACTIVITY',Token=packet.Token..':arm',UnitID=41,ActivityKey=a.activityKey,Result='ARMED',Owned=true,Awake=true,Sleeping=false,SampleTurn=currentTurn,NativeOperation=-1})
          handler(2,{Action='ACTIVITY',Token=packet.Token..':sleep',UnitID=41,
           ActivityKey=a.activityKey,Result='ASLEEP',Owned=true,SampleTurn=currentTurn,NativeOperation=-1})
          assert(ExposedMembers.SPC_ExpeditionActivity.phase=='TASK_RUNNING')
          assert(ExposedMembers.SPC_ExpeditionActivity.taskDue==85)
          currentTurn=84;ownTurn(2);assert(ExposedMembers.SPC_ExpeditionActivity.taskCompletions==0)
          currentTurn=85;ownTurn(2);ownTurn(2)
          assert(ExposedMembers.SPC_ExpeditionActivity.taskCompletions==1)
          assert(ExposedMembers.SPC_ExpeditionActivity.phase=='TASK_COMPLETE')
          assert(ContextPtr.hidden and nativeCalls==0 and properties==0 and destroys==0)
        """)

    def test_delayed_exact_acceptance_stays_open_until_ack_then_closes(self):
        lua=sidebar(arrived=True)
        lua.execute("""
          gateOpen('TASK',41);chooseTask();deferred=true;Controls.NormalConfirmButton.click()
          local packet=lastPacket;local before=sent
          assert(packet.Action=='TASK' and not ContextPtr.hidden)
          Controls.NormalCancelButton.click();Controls.NormalConfirmButton.click();publish()
          assert(not ContextPtr.hidden and sent==before)
          handler(2,packet);deferred=false;publish()
          assert(ContextPtr.hidden and ExposedMembers.SPC_ExpeditionActivity.phase=='TASK_PREPARING')
          publish();assert(sent==before and nativeCalls==0 and properties==0)
        """)

    def test_rejected_request_stays_open_with_error(self):
        lua=sidebar(arrived=True)
        lua.execute("""
          gateOpen('TASK',41);chooseTask();deferred=true;Controls.NormalConfirmButton.click()
          local packet=lastPacket;currentTurn=currentTurn+1
          handler(2,packet);deferred=false;publish()
          assert(not ContextPtr.hidden and ExposedMembers.SPC_ExpeditionGateReply.error)
          assert(ExposedMembers.SPC_ExpeditionActivity.phase=='ARRIVED')
          assert(Controls.NormalFeedback.text~='' and nativeCalls==0 and properties==0)
        """)

    def test_mismatched_reply_cannot_close_as_accepted_task(self):
        for change in ["r.unitID=42", "r.activityKey='wrong-task'", "r.bound=false",
                       "r.token='wrong-token'", "r.owner=3", "r.phase='ARRIVED'",
                       "r.stop='REJECTED'", "r.activityFailure='FAILURE'"]:
            with self.subTest(change=change):
                lua=sidebar(arrived=True)
                lua.execute("""
                  gateOpen('TASK',41);chooseTask();deferred=true;Controls.NormalConfirmButton.click()
                  local packet=lastPacket;handler(2,packet)
                  local r=ExposedMembers.SPC_ExpeditionGateReply
                """+change+"""
                  deferred=false;publish()
                  assert(not ContextPtr.hidden and nativeCalls==0 and properties==0)
                """)

    def test_newer_held_activity_supersedes_accepted_reply_and_stays_visible(self):
        for change in ["a.phase='HELD';a.mode='BLOCKED';a.error='SLEEP_REJECTED'",
                       "a.activityFailure='SLEEP_FAILURE'", "a.activityKey='new-task'",
                       "a.unitID=42", "a.teamKey='different-team'"]:
            with self.subTest(change=change):
                lua=sidebar(arrived=True)
                lua.execute("""
                  gateOpen('TASK',41);chooseTask();deferred=true;Controls.NormalConfirmButton.click()
                  local packet=lastPacket;handler(2,packet)
                  local a=ExposedMembers.SPC_ExpeditionActivity
                """+change+"""
                  deferred=false;publish()
                  assert(not ContextPtr.hidden and nativeCalls==0 and properties==0)
                """)

    def test_immediate_matching_failure_remains_readable_after_native_selection_clears(self):
        lua=sidebar(arrived=True)
        lua.execute("""
          gateOpen('TASK',41);chooseTask()
          local dispatch=handler
          handler=function(pid,packet)
           dispatch(pid,packet)
           if packet.Action=='TASK' then
            selectedID=nil
            local a=ExposedMembers.SPC_ExpeditionActivity
            a.phase='HELD';a.mode='BLOCKED';a.error='ACTIVITY_UNEXPECTED_STATE'
            a.activityFailure='ACTIVITY_UNEXPECTED_STATE'
           end
          end
          Controls.NormalConfirmButton.click()
          assert(not ContextPtr.hidden and Controls.NormalConfirmButton.disabled)
          assert(Controls.NormalFeedback.text:find('NORMAL_FAILURE_UNKNOWN',1,true))
          assert(not Controls.NormalFeedback.text:find('NORMAL_SELECTION_CHANGED',1,true))
          assert(Controls.NormalSummary.text:find('NORMAL_FAILURE_UNKNOWN',1,true))
          local before=sent;Controls.NormalConfirmButton.click()
          assert(sent==before and nativeCalls==0 and properties==0)
        """)

    def test_wrong_unit_failure_is_not_attributed_when_selection_clears(self):
        lua=sidebar(arrived=True)
        lua.execute("""
          gateOpen('TASK',41);chooseTask()
          local dispatch=handler
          handler=function(pid,packet)
           dispatch(pid,packet)
           if packet.Action=='TASK' then
            selectedID=nil
            local r=ExposedMembers.SPC_ExpeditionGateReply
            r.unitID=42;r.trackedID=42;r.phase='HELD';r.error='ACTIVITY_UNEXPECTED_STATE'
            local a=ExposedMembers.SPC_ExpeditionActivity
            a.unitID=42;a.phase='HELD';a.mode='BLOCKED';a.error='ACTIVITY_UNEXPECTED_STATE'
           end
          end
          Controls.NormalConfirmButton.click()
          assert(not ContextPtr.hidden and Controls.NormalConfirmButton.disabled)
          assert(Controls.NormalFeedback.text:find('NORMAL_SELECTION_CHANGED',1,true))
          assert(not Controls.NormalFeedback.text:find('NORMAL_FAILURE_UNKNOWN',1,true))
          local before=sent;Controls.NormalConfirmButton.click()
          assert(sent==before and nativeCalls==0 and properties==0)
        """)

    def test_exact_accepted_task_still_closes_when_native_selection_clears(self):
        lua=sidebar(arrived=True)
        lua.execute("""
          gateOpen('TASK',41);chooseTask()
          local dispatch=handler
          handler=function(pid,packet)
           dispatch(pid,packet);if packet.Action=='TASK' then selectedID=nil end
          end
          Controls.NormalConfirmButton.click()
          assert(ContextPtr.hidden and ExposedMembers.SPC_ExpeditionActivity.phase=='TASK_PREPARING')
          assert(lastPacket.Action=='TASK' and nativeCalls==0 and properties==0)
        """)

    def test_diagnostic_task_ack_does_not_autoclose_p0_window(self):
        lua=sidebar(arrived=True)
        lua.execute("""
          gateOpen();Controls.TaskButton.click()
          assert(lastPacket.Action=='TASK' and not ContextPtr.hidden)
          assert(ExposedMembers.SPC_ExpeditionActivity.phase=='TASK_PREPARING')
          assert(not Controls.DiagnosticPanel.hidden and nativeCalls==0 and properties==0)
        """)


if __name__=='__main__':unittest.main()
