"""Current P0 diagnostics visibility and callbacks under mock Civ controls.

L1 local UI evidence only: this does not prove native font, UI-scale, or
rendering behavior. Historical panel fixtures remain unchanged.
"""
from pathlib import Path
import unittest
import xml.etree.ElementTree as ET

from lupa.lua55 import LuaRuntime

ROOT = Path(__file__).resolve().parents[1]
PANEL = ROOT / 'Mod' / 'UI'
ROWS = (
    ('SourceYieldButton', 'GovernorButton', 'SpecialistsButton'),
    ('GWReadButton', 'AestheticButton', 'MeaningProbeButton'),
    ('DPReadButton', 'DP03Button', 'DP05Button'),
    ('CompletenessButton', 'TemplatesButton', 'UnitReadButton'),
    ('MeaningConfigButton', 'InspirationEndButton', 'CopyButton'),
)
VISIBLE = frozenset(button for row in ROWS for button in row)


def panel_runtime():
    """Execute the whole current panel, including its late initializer wrapper.

    Uses the same control/event stand-in pattern as test_b068_ui.py, but keeps
    left/right callbacks separate and seeds hidden flags from the actual XML.
    It requires no external database and never runs gameplay or probe writers.
    """
    tree = ET.parse(PANEL / 'P0Panel.xml')
    lua = LuaRuntime(unpack_returned_tuples=True)
    lua.execute(r'''
        requests={}; printed={}; included={}; eventAdds={}
        function event(name)
            return {Add=function(fn) eventAdds[name]=(eventAdds[name] or 0)+1 end,
                    Remove=function(fn) end}
        end
        Events=setmetatable({}, {__index=function(t,k)
            local e=event(k);rawset(t,k,e);return e
        end})
        Mouse={eLClick=1,eRClick=2}
        PlayerOperations={EXECUTE_SCRIPT=1}
        SPCP0={VERSION='current-panel-fixture', IsTestPlayer=function(pid)return pid==0 end,
               Scalar=tostring, Call=function()return false end, Count=function()end}
        Game={GetLocalPlayer=function()return 0 end,GetCurrentGameTurn=function()return 68 end}
        city={GetOwner=function()return 0 end,GetID=function()return 11 end}
        unit={GetOwner=function()return 0 end,GetID=function()return 17 end}
        selectedCity=city;selectedUnit=unit
        UI={GetHeadSelectedCity=function()return selectedCity end,
            GetHeadSelectedUnit=function()return selectedUnit end,
            RequestPlayerOperation=function(pid,operation,packet)
                assert(pid==0 and operation==PlayerOperations.EXECUTE_SCRIPT)
                requests[#requests+1]=packet
            end}
        Players={[0]={GetCities=function()return {FindID=function(id)return id==11 and city or nil end}end}}
        ExposedMembers={SPC_P0={Version=SPCP0.VERSION,
            MemoryObservation={AutoGC={enabled=true,calls=9}},
            NetworkBridge={ready=true,epoch=42}, permanentSentinel='preserve'},
            SPC_P0_BackgroundRoutes={sentinel='routes'}}
        local function noOp()end
        SPCOverflowStorageRead={New=function()return {Pulse=noOp}end}
        SPCBoostGreatWorkRead={ClearModifierRead=noOp,ClearMeaningRead=noOp}
        SPCCityIdentityEvidence={New=function()return {}end}
        SPCProjectTurnRead={New=function()return {}end}
        SPCTimedProjectRead={New=function()return {Pulse=noOp,Read=noOp,Cancel=noOp}end}
        Locale={Lookup=function(key)return key end}
        include=function(name)included[#included+1]=name end
        print=function(message)printed[#printed+1]=message end
        UIManager={};GameInfo={Yields={}}
        Controls={}
        function makeControl(id,hidden)
            local control={hidden=hidden,callbacks={}}
            function control:SetHide(value)self.hidden=value end
            function control:SetText(value)self.text=value end
            function control:SetToolTipString(value)self.tooltip=value end
            function control:RegisterCallback(event,callback)self.callbacks[event]=callback end
            function control:CalculateSize()end
            function control:ReprocessAnchoring()end
            function control:ChangeParent(parent)self.parent=parent end
            function control:SetOffsetVal(x,y)self.offsetX=x;self.offsetY=y end
            function control:GetSizeX()return 296 end
            Controls[id]=control
        end
        ContextPtr={hidden=false,
            SetInitHandler=function(_,fn)init=fn end,
            SetShutdown=function(_,fn)shutdown=fn end,
            SetUpdate=function(_,fn)update=fn end,
            ClearUpdate=function()update=nil end,
            SetHide=function(self,value)self.hidden=value end,
            LookUpControl=function()return {GetSizeX=function()return 296 end}end}
    ''')
    for element in tree.getroot().iter():
        control_id = element.get('ID')
        if control_id:
            lua.globals().makeControl(control_id, element.get('Hidden') == '1')
    lua.execute((PANEL / 'P0Panel.lua').read_text())
    lua.execute('init()')
    return tree, lua


class CurrentPanelTests(unittest.TestCase):
    def test_exact_visible_set_survives_entire_initializer(self):
        tree, lua = panel_runtime()
        window = tree.getroot().find("Container[@ID='Window']")
        buttons = window.findall('GridButton')
        tasks = [button for button in buttons if button.get('ID') != 'CloseButton']
        for button in tasks:
            with self.subTest(button=button.get('ID')):
                self.assertIn(button.get('Hidden'), ('0', '1'))
        xml_visible = {button.get('ID') for button in tasks if button.get('Hidden') == '0'}
        final_visible = {button.get('ID') for button in tasks
                         if not lua.globals().Controls[button.get('ID')].hidden}
        self.assertEqual(xml_visible, VISIBLE)
        self.assertEqual(final_visible, VISIBLE)
        self.assertTrue(lua.globals().Controls.LegacyProbeButtons.hidden)
        for control_id in ('GWAReadButton', 'PerformanceSnapshotButton', 'PerformanceReadButton',
                           'InheritRecordButton', 'InheritReadButton', 'BackgroundRoutesButton',
                           'NetworkButton', 'CarrierStepButton', 'DiscountsButton'):
            with self.subTest(retired=control_id):
                self.assertTrue(lua.globals().Controls[control_id].hidden)

    def test_three_columns_five_rows_and_report_do_not_overlap(self):
        tree = ET.parse(PANEL / 'P0Panel.xml')
        window = tree.getroot().find("Container[@ID='Window']")
        self.assertEqual(window.get('Size'), '840,664')
        buttons = {button.get('ID'): button for button in window.findall('GridButton')}
        rectangles = []
        for row_number, row in enumerate(ROWS):
            for column, control_id in enumerate(row):
                button = buttons[control_id]
                self.assertEqual(button.get('Anchor'), 'L,B')
                self.assertEqual(button.get('Offset'), f'{18 + column * 262},{178 - row_number * 40}')
                self.assertEqual(button.get('Size'), '240,32')
                x, bottom = map(int, button.get('Offset').split(','))
                width, height = map(int, button.get('Size').split(','))
                y = 664 - bottom - height
                rectangles.append((control_id, x, y, x + width, y + height))
        report = window.find("ScrollPanel[@ID='ReportScroll']")
        self.assertEqual(report.get('Offset'), '18,58')
        self.assertEqual(report.get('Size'), '804,380')
        report_bottom = 58 + 380
        for control_id, x1, y1, x2, y2 in rectangles:
            with self.subTest(control=control_id):
                self.assertGreaterEqual(x1, 0)
                self.assertLessEqual(x2, 840)
                self.assertGreater(y1, report_bottom)
                self.assertLessEqual(y2, 664)
        for i, first in enumerate(rectangles):
            for second in rectangles[i + 1:]:
                with self.subTest(pair=(first[0], second[0])):
                    separated = (first[3] <= second[1] or second[3] <= first[1]
                                 or first[4] <= second[2] or second[4] <= first[2])
                    self.assertTrue(separated)

    def test_inspiration_next_read_and_end_remain_available(self):
        _, lua = panel_runtime()
        lua.execute(r'''
            Controls.MeaningConfigButton.callbacks[Mouse.eLClick]()
            assert(requests[#requests].Action=='INSPIRE_NEXT')
            Controls.MeaningConfigButton.callbacks[Mouse.eRClick]()
            assert(requests[#requests].Action=='INSPIRE_READ')
            for _,event in ipairs({Mouse.eLClick,Mouse.eRClick})do
                Controls.InspirationEndButton.callbacks[event]()
                assert(requests[#requests].Action=='INSPIRE_END')
            end
            assert(#requests==4)
        ''')

    def test_meaning_both_clicks_are_read_only_status(self):
        _, lua = panel_runtime()
        lua.execute(r'''
            for _,event in ipairs({Mouse.eLClick,Mouse.eRClick})do
                Controls.MeaningProbeButton.callbacks[event]()
                assert(requests[#requests].Action=='CULTURE_MEANING_STATUS')
            end
            assert(#requests==2)
        ''')

    def test_core_read_and_detail_callbacks_keep_current_actions(self):
        _, lua = panel_runtime()
        pairs = (
            ('SourceYieldButton', 1, 'PROGRESSION_READ'),
            ('GovernorButton', 1, 'GOVERNOR'),
            ('SpecialistsButton', 1, 'SPECIALISTS'),
            ('GWReadButton', 1, 'GREAT_WORK_FACTS_READ'),
            ('GWReadButton', 2, 'GREAT_WORK_FACTS_DETAIL'),
            ('AestheticButton', 1, 'CULTURE_AESTHETIC_READ'),
            ('AestheticButton', 2, 'CULTURE_AESTHETIC_DETAIL'),
            ('DPReadButton', 1, 'RESEARCH_CROSS_READ'),
            ('DPReadButton', 2, 'RESEARCH_CROSS_DETAIL'),
            ('DP03Button', 1, 'RESEARCH_APPLY_READ'),
            ('DP03Button', 2, 'RESEARCH_APPLY_DETAIL'),
            ('DP05Button', 1, 'RESEARCH_CHAIR_DETAIL'),
            ('DP05Button', 2, 'RESEARCH_TRADITION_READ'),
            ('CompletenessButton', 1, 'COMPLETENESS_READ'),
            ('CompletenessButton', 2, 'RESEARCH_INFRA_DETAIL'),
            ('TemplatesButton', 1, 'STANDARDIZATION_READ'),
            ('UnitReadButton', 1, 'UNIT_SITE_READ'),
            ('UnitReadButton', 2, 'CITY_SEQUENCE_BEGIN'),
        )
        for control_id, event, expected in pairs:
            with self.subTest(control=control_id, event=event):
                lua.globals().Controls[control_id].callbacks[event]()
                request = lua.globals().requests[len(lua.globals().requests)]
                self.assertEqual(request.Action, expected)
                self.assertEqual(request.UnitID if control_id == 'UnitReadButton' else request.CityID,
                                 17 if control_id == 'UnitReadButton' else 11)
        lua.execute('local n=#requests;Controls.CopyButton.callbacks[Mouse.eLClick]();assert(#requests==n);assert(Controls.Status.text:find("Lua.log"))')

    def test_visibility_cleanup_does_not_execute_probe_or_change_runtime_state(self):
        _, lua = panel_runtime()
        lua.execute(r'''
            assert(#requests==0)
            assert(ExposedMembers.SPC_P0.MemoryObservation.AutoGC.enabled==true)
            assert(ExposedMembers.SPC_P0.MemoryObservation.AutoGC.calls==9)
            assert(ExposedMembers.SPC_P0.NetworkBridge.ready==true)
            assert(ExposedMembers.SPC_P0.NetworkBridge.epoch==42)
            assert(ExposedMembers.SPC_P0.permanentSentinel=='preserve')
            assert(ExposedMembers.SPC_P0_BackgroundRoutes.sentinel=='routes')
            Controls.OpenButton.callbacks[Mouse.eLClick]()
            assert(not Controls.Window.hidden and #requests==0)
            Controls.CloseButton.callbacks[Mouse.eLClick]()
            assert(Controls.Window.hidden and #requests==0)
            shutdown()
            assert(#requests==0 and ExposedMembers.SPC_P0.MemoryObservation.AutoGC.enabled==true)
        ''')

    def test_unique_xml_control_ids_and_current_lua_parse(self):
        tree = ET.parse(PANEL / 'P0Panel.xml')
        ids = [element.get('ID') for element in tree.getroot().iter() if element.get('ID')]
        self.assertEqual(len(ids), len(set(ids)))
        lua = LuaRuntime()
        parsed, error = lua.eval('function(source)local fn,err=load(source);return fn~=nil,err end')(
            (PANEL / 'P0Panel.lua').read_text())
        self.assertTrue(parsed, error)


if __name__ == '__main__':
    unittest.main(verbosity=2)
