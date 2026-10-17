"""B197 sidebar presentation delta over the existing Expedition request adapters.

Actual Lua with mocked native controls/events. This proves routing, guard and
lifecycle preservation locally, not native visual appearance or render scaling.
"""
from pathlib import Path
import sqlite3
import unittest
import xml.etree.ElementTree as ET

from test_expedition_spy_actions_ui import normal_window

R = Path(__file__).resolve().parents[1]


def sidebar(arrived=False, second_target=False):
    lua = normal_window(arrived=arrived)
    if second_target:
        lua.execute("""
          anotherCity={id=10,owner=4,x=20,y=9}
          for key,value in pairs(targetCity)do
           if type(value)=='function'then anotherCity[key]=value end
          end
          anotherCity.GetName=function()return '第二目标' end
          Players[4]={IsMajor=function()return true end,IsAlive=function()return true end,
           GetCities=function()return {FindID=function(self,id)if id==10 then return anotherCity end end,
            GetCapitalCity=function()return anotherCity end,
            Members=function()local done=false;return function()if not done then done=true;return 1,anotherCity end end end}end}
        """)
    return lua


class SidebarRouting(unittest.TestCase):
    def test_city_rows_only_select_and_confirm_routes_exact_destination_once(self):
        lua=sidebar(second_target=True)
        lua.execute("""
          gateOpen('TRAVEL',40)
          local rows=instanceManagers.SPCExpeditionDestination.instances
          assert(#rows==2 and not Controls.DestinationStack.hidden and Controls.NormalMissionGrid.hidden)
          local before=sent;local reads=helperCalls;rows[2].DestinationButton.click()
          assert(sent==before and nativeCalls==0 and helperCalls==reads and lastPacket.Action=='READ')
          assert(Controls.NormalCityName.text:find('第二目标',1,true) and not Controls.NormalMissionGrid.hidden)
          Controls.NormalConfirmButton.click()
          assert(lastPacket.Action=='DISPATCH' and lastPacket.TargetOwner==4 and lastPacket.TargetID==10)
          assert(nativeCalls==1 and ContextPtr.hidden and properties==0 and placeCalls==0)
          Controls.NormalConfirmButton.click();assert(nativeCalls==1)
        """)

    def test_stale_city_row_cannot_select_after_close_and_reopen(self):
        lua=sidebar(second_target=True)
        lua.execute("""
          gateOpen('TRAVEL',40)
          local old=instanceManagers.SPCExpeditionDestination.instances[2].DestinationButton.click
          Controls.NormalCloseButton.click();assert(ContextPtr.hidden)
          gateOpen('TRAVEL',40)
          local before=Controls.NormalCityName.text;local count=sent
          old()
          assert(Controls.NormalCityName.text==before and sent==count and nativeCalls==0)
        """)

    def test_stale_city_row_rejects_changed_unit_and_wrong_view(self):
        for change in ["selectedID=99", "gateOpen('TASK',41)"]:
            with self.subTest(change=change):
                lua=sidebar(arrived=True,second_target=True)
                lua.execute("""
                  gateOpen('TRAVEL',41)
                  stale=instanceManagers.SPCExpeditionDestination.instances[2].DestinationButton.click
                """)
                lua.execute(change)
                lua.execute("""
                  local before=Controls.NormalCityName.text;local count=sent
                  stale()
                  assert(Controls.NormalCityName.text==before and sent==count and nativeCalls==0 and properties==0)
                """)

    def test_mission_card_is_preview_and_confirm_uses_independent_task_request(self):
        lua=sidebar(arrived=True)
        lua.execute("""
          gateOpen('TASK',41)
          local rows=instanceManagers.SPCExpeditionMission.instances
          -- B212: three Design missions; the target capital offers 风土考察 (PEOPLE).
          assert(#rows==3 and Controls.DestinationStack.hidden and not Controls.MissionStack.hidden)
          assert(rows[1].MissionLocation.truncateWidth==135)
          local before=sent;local operations=nativeCalls
          rows[1].MissionButton.click()
          assert(sent==before and nativeCalls==operations and ExposedMembers.SPC_ExpeditionActivity.phase=='ARRIVED')
          Controls.NormalConfirmButton.click()
          assert(lastPacket.Action=='TASK' and lastPacket.Mission=='PEOPLE' and lastPacket.MissionX==15 and lastPacket.MissionY==8)
          assert(ExposedMembers.SPC_ExpeditionActivity.phase=='TASK_PREPARING')
          assert(not ExposedMembers.SPC_ExpeditionActivity.taskStart and nativeCalls==operations and properties==0)
        """)

    def test_locked_activity_rejects_captured_mission_and_confirm(self):
        lua=sidebar(arrived=True)
        lua.execute("""
          gateOpen('TASK',41);chooseTask()
          local old=instanceManagers.SPCExpeditionMission.instances[1].MissionButton.click
          local v=ExposedMembers.SPC_ExpeditionActivity;v.mode='ASLEEP';v.locked=true;v.phase='TASK_RUNNING'
          activityChanged();local before=sent
          old();Controls.NormalConfirmButton.click()
          assert(Controls.NormalConfirmButton.disabled and sent==before and nativeCalls==0 and properties==0)
        """)

    def test_pending_dispatch_cannot_be_cancelled_by_sidebar_close_or_escape(self):
        lua=sidebar()
        lua.execute("""
          gateOpen('TRAVEL',40);chooseCity();deferred=true;Controls.NormalConfirmButton.click()
          local packet=lastPacket;local before=sent
          assert(packet.Action=='DISPATCH' and nativeCalls==0)
          Controls.NormalCloseButton.click();Controls.NormalCancelButton.click();assert(input(KeyEvents.KeyUp,Keys.VK_ESCAPE))
          Controls.NormalConfirmButton.click()
          assert(not ContextPtr.hidden and sent==before)
          handler(2,packet);deferred=false;publish()
          assert(ContextPtr.hidden and nativeCalls==1 and ExposedMembers.SPC_ExpeditionActivity.phase=='TRAVELLING')
          publish();assert(nativeCalls==1 and properties==0)
        """)

    def test_object_escape_closes_idle_sidebar_without_request(self):
        lua=sidebar()
        lua.execute("""
          gateOpen('TRAVEL',40);local before=sent
          local event={GetMessageType=function()return KeyEvents.KeyUp end,GetKey=function()return Keys.VK_ESCAPE end}
          assert(input(event));assert(ContextPtr.hidden and sent==before and nativeCalls==0 and properties==0)
        """)

    def test_pending_task_uses_same_guard_without_native_operation(self):
        lua=sidebar(arrived=True)
        lua.execute("""
          gateOpen('TASK',41);chooseTask();deferred=true;Controls.NormalConfirmButton.click()
          local packet=lastPacket;local before=sent;local operations=nativeCalls
          Controls.NormalCloseButton.click();Controls.NormalCancelButton.click();assert(input(KeyEvents.KeyUp,Keys.VK_ESCAPE))
          assert(not ContextPtr.hidden and sent==before)
          handler(2,packet);deferred=false;publish()
          assert(ExposedMembers.SPC_ExpeditionActivity.phase=='TASK_PREPARING' and nativeCalls==operations and properties==0)
        """)

    def test_no_targets_shows_empty_state_and_does_not_send_dispatch(self):
        lua=sidebar()
        lua.execute("""
          met=false;gateOpen('TRAVEL',40)
          assert(#instanceManagers.SPCExpeditionDestination.instances==0)
          assert(not Controls.NormalEmptyLabel.hidden and Controls.NormalConfirmButton.disabled)
          local before=sent;Controls.NormalConfirmButton.click()
          assert(sent==before and nativeCalls==0 and properties==0)
        """)

    def test_resize_changes_only_layout_and_close_releases_instance_rows(self):
        lua=sidebar(second_target=True)
        lua.execute("""
          gateOpen('TRAVEL',40)
          local before=sent;local rows=instanceManagers.SPCExpeditionDestination.instances
          screenHeight=768;systemUpdate(SystemUpdateUI.ScreenResize)
          assert(Controls.SlideAnim.sizey==738 and #rows==2 and sent==before and nativeCalls==0)
          Controls.NormalCloseButton.click()
          assert(ContextPtr.hidden and #instanceManagers.SPCExpeditionDestination.instances==0)
          assert(#instanceManagers.SPCExpeditionMission.instances==0 and properties==0 and destroys==0)
        """)

    def test_shutdown_removes_resize_listener_and_does_not_destroy_team(self):
        lua=sidebar()
        lua.execute("""
          gateOpen('TRAVEL',40);local before=sent;shutdown()
          assert(systemUpdate==nil and gateOpen==nil and publish==nil and turnBegin==nil)
          assert(ContextPtr.hidden and sent==before and units[40] and destroys==0 and properties==0)
        """)


class SidebarLayout(unittest.TestCase):
    def test_independent_sidebar_uses_native_presentation_styles_without_native_callbacks(self):
        root=ET.parse(R/'Mod/UI/ExpeditionSpyWindow.xml').getroot()
        controls=[e for child in root if child.tag!='Instance' for e in child.iter() if e.get('ID')]
        ids={e.get('ID'):e for e in controls}
        self.assertEqual(len(ids),len(controls))
        for instance in root.findall('./Instance'):
            names=[e.get('ID') for e in instance.iter() if e.get('ID')]
            self.assertEqual(len(names),len(set(names)))
        self.assertTrue(any(e.tag=='SlideAnim' and e.get('Style')=='ChooserAnim' for e in root.iter()))
        self.assertIn('NormalCloseButton',ids)
        self.assertIn('NormalScroll',ids)
        self.assertEqual(ids['NormalScroll'].get('Offset'),'18,133')
        self.assertEqual(ids['NormalCurrentSlot'].get('Texture'),'DestinationChooser_CurrentSlot')
        self.assertEqual(ids['NormalMissionGrid'].get('Offset'),'296,126')
        self.assertEqual(ids['NormalBannerBase'].get('Texture'),'CityPanel_BannerBase')
        self.assertEqual(ids['NormalBannerDarker'].get('Texture'),'CityPanel_BannerDarker')
        self.assertEqual(ids['NormalBannerLighter'].get('Texture'),'CityPanel_BannerLighter')
        self.assertIn('NormalCancelButton',ids)
        self.assertNotIn('NormalFeedbackScroll',ids)
        self.assertNotIn('NormalTargetPrevious',ids)
        self.assertNotIn('NormalTargetNext',ids)
        self.assertEqual({e.get('Name') for e in root.findall('./Instance')},{'SPCExpeditionDestination','SPCExpeditionMission','SPCExpeditionDistrict'})
        source=(R/'Mod/UI/ExpeditionSpyWindow.lua').read_text()
        self.assertNotIn("include('EspionageChooser')",source)
        self.assertNotIn("include('AnimSidePanelSupport')",source)
        self.assertNotIn('RequestOperation(',source)

    def test_static_xml_localization_keys_exist_in_both_languages(self):
        db=sqlite3.connect(':memory:')
        db.execute('create table LocalizedText(Language text,Tag text,Text text,primary key(Language,Tag))')
        db.executescript((R/'Mod/Text/ExpeditionGate.sql').read_text())
        root=ET.parse(R/'Mod/UI/ExpeditionSpyWindow.xml').getroot()
        for element in root.iter():
            key=element.get('String','')
            if key.startswith('LOC_SPC_'):
                with self.subTest(key=key):
                    self.assertEqual(db.execute('select count(*) from LocalizedText where Tag=?',(key,)).fetchone()[0],2)
        db.close()


if __name__=='__main__':
    unittest.main()
