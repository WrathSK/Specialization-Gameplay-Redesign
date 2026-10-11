"""B200 mission-card sizing regression; actual Lua, simulated text measurements.

The native renderer/wrapping remains a user-game UI gate. These cases prove the
row height uses only measured content, not its previous selected-overlay height.
"""
from pathlib import Path
import unittest
import xml.etree.ElementTree as ET
from test_expedition_spy_sidebar_ui import sidebar

R=Path(__file__).resolve().parents[1]


class MissionCardLayout(unittest.TestCase):
    def test_card_height_is_measured_content_not_a_recursive_overlay(self):
        lua=sidebar(arrived=True)
        lua.execute("""
          gateOpen('TASK',41)
          local row=instanceManagers.SPCExpeditionMission.instances[1]
          row.DetailsStack.CalculateSize=function(self)self.sizey=104 end
          -- Reproduce the prior oversized selected frame as old control state.
          row.MissionButton.sizey=440;row.MissionContent.sizey=440
          row.SelectorBrace.sizey=440
          row.MissionButton.DoAutoSize=function()error('overlay must not drive auto height')end
          local reads=helperCalls;local requests=sent
          for i=1,20 do
           systemUpdate(SystemUpdateUI.ScreenResize)
           assert(row.MissionButton.sizey==118 and row.MissionContent.sizey==118)
          end
          assert(row.SelectorBrace.hidden and Controls.NormalConfirmButton.disabled)
          row.MissionButton.click();assert(not row.SelectorBrace.hidden)
          for i=1,20 do
           publish();activityChanged();systemUpdate(SystemUpdateUI.ScreenResize)
           assert(row.MissionButton.sizey==118 and row.MissionContent.sizey==118)
          end
          assert(helperCalls==reads and sent==requests and nativeCalls==0 and properties==0)
        """)

    def test_long_wrapped_text_can_grow_and_shrink_without_old_height_retention(self):
        lua=sidebar(arrived=True)
        lua.execute("""
          gateOpen('TASK',41)
          local row=instanceManagers.SPCExpeditionMission.instances[1]
          measuredHeight=180
          row.DetailsStack.CalculateSize=function(self)self.sizey=measuredHeight end
          systemUpdate(SystemUpdateUI.ScreenResize)
          assert(row.MissionButton.sizey==194 and row.MissionContent.sizey==194)
          measuredHeight=88;systemUpdate(SystemUpdateUI.ScreenResize)
          assert(row.MissionButton.sizey==102 and row.MissionContent.sizey==102)
          measuredHeight=42;systemUpdate(SystemUpdateUI.ScreenResize)
          assert(row.MissionButton.sizey==76 and row.MissionContent.sizey==76)
          assert(Controls.NormalConfirmButton.disabled and nativeCalls==0 and properties==0)
        """)

    def test_relocation_preview_resizes_without_choosing_or_dispatching(self):
        lua=sidebar()
        lua.execute("""
          gateOpen('TRAVEL',40)
          local row=instanceManagers.SPCExpeditionMission.instances[1]
          row.DetailsStack.CalculateSize=function(self)self.sizey=116 end
          local before=sent;local reads=helperCalls
          systemUpdate(SystemUpdateUI.ScreenResize)
          assert(row.MissionButton.sizey==130 and row.MissionContent.sizey==130)
          assert(Controls.NormalMissionGrid.hidden and Controls.NormalConfirmButton.disabled)
          chooseCity()
          assert(row.MissionButton.sizey==130 and row.MissionContent.sizey==130)
          assert(not Controls.NormalMissionGrid.hidden and row.MissionButton.disabled and row.SelectorBrace.hidden)
          assert(sent==before and helperCalls==reads and nativeCalls==0 and properties==0)
        """)

    def test_idle_task_open_and_read_refresh_have_no_extra_instruction_line(self):
        lua=sidebar(arrived=True)
        lua.execute("""
          gateOpen('TASK',41)
          assert(Controls.NormalFeedback.text=='' and Controls.NormalConfirmButton.disabled)
          publish();activityChanged();systemUpdate(SystemUpdateUI.ScreenResize)
          assert(Controls.NormalFeedback.text=='' and Controls.NormalConfirmButton.disabled)
          local before=sent;Controls.NormalConfirmButton.click()
          assert(sent==before and nativeCalls==0 and properties==0)
          Controls.NormalCancelButton.click();gateOpen('TASK',41)
          assert(Controls.NormalFeedback.text=='' and Controls.NormalConfirmButton.disabled)
        """)

    def test_mission_scroll_clears_header_and_preserves_footer_boundary(self):
        root=ET.parse(R/'Mod/UI/ExpeditionSpyWindow.xml').getroot()
        header=root.find(".//*[@ID='NormalDrawerHeader']")
        scroll=root.find(".//*[@ID='NormalMissionScroll']")
        footer=root.find(".//*[@ID='NormalDestinationChooserButtons']")
        header_top=int(header.get('Offset').split(',')[1])
        header_height=int(header.get('Size').split(',')[1])
        scroll_top=int(scroll.get('Offset').split(',')[1])
        scroll_bottom_inset=int(scroll.get('Size').split(',')[1].removeprefix('parent-'))-scroll_top
        footer_height=int(footer.get('Size').split(',')[1])
        self.assertGreaterEqual(scroll_top-(header_top+header_height),6)
        self.assertEqual(scroll_bottom_inset-footer_height,2)

    def test_xml_has_no_parent_height_to_auto_height_feedback_and_reserves_stats_space(self):
        instance=ET.parse(R/'Mod/UI/ExpeditionSpyWindow.xml').getroot().find(
            "./Instance[@Name='SPCExpeditionMission']")
        button=instance.find("./GridButton[@ID='MissionButton']")
        content=button.find("./Container[@ID='MissionContent']")
        brace=button.find("./Grid[@ID='SelectorBrace']")
        self.assertEqual(button.get('Size'),'parent,76')
        self.assertEqual(content.get('Size'),'parent,76')
        self.assertEqual(content.get('Anchor'),'L,T')
        self.assertIsNone(content.get('AutoSizePadding'))
        self.assertEqual(brace.get('Size'),'parent,parent')
        self.assertEqual(brace.get('ConsumeMouse'),'0')
        details=content.find("./Stack[@ID='DetailsStack']")
        self.assertEqual(details.find('./Container').get('Size'),'192,24')
        self.assertEqual(details.find("./Label[@ID='MissionDetails']").get('WrapWidth'),'192')
        self.assertEqual(content.find("./Stack[@ID='MissionStatsStack']").get('Anchor'),'R,B')


if __name__=='__main__':
    unittest.main()
