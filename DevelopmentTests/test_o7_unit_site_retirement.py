"""Exact package absence, surviving unit controls and the real City Sequence route."""

from collections import deque
from pathlib import Path
import unittest
import xml.etree.ElementTree as ET

from refactor_harness import Context, PackageVFS, ROOT
from retired_crew_sources import B446, B447, gameplay as historical_gameplay, package as historical_package
from test_o7_crew_retirement import verify_package_round_trip
from test_p0_panel_current_layout import panel_runtime
from test_pu11_package_absence import NATIVE


RETIRED = ('UnitActionSitePolicy.lua', 'UnitSiteProbe.lua')
GLOBALS = tuple('SPC' + Path(path).stem for path in RETIRED)


SEQUENCE_FIXTURE = """
Events.LoadScreenClose.Fire()
local city={
 GetOwner=function()return 0 end,GetID=function()return 11 end,
 GetX=function()return 11 end,GetY=function()return 20 end}
local unit={
 GetOwner=function()return 0 end,GetID=function()return 17 end,GetType=function()return 1 end,
 GetX=function()return 21 end,GetY=function()return 20 end}
Players[0].GetUnits=function()return {FindID=function(_,id)assert(id==17);return unit end}end
Players[0].GetCities=function()return {FindID=function(_,id)assert(id==11);return city end}end
GameInfo.Units={[1]={UnitType='UNIT_SETTLER'}}
CityManager={GetCityAt=function(x,y)assert(y==20);if x==11 then return city end end}
Game.SetProperty=function()error('SEQUENCE_WROTE_PERMANENT_STATE')end
"""


class UnitSiteRetirement(unittest.TestCase):
    def test_actual_package_excludes_the_two_site_diagnostics(self):
        vfs = PackageVFS(forbidden_globals=GLOBALS)
        self.assertFalse(set(RETIRED) & (vfs.files | vfs.imports))
        g = Context(vfs=vfs)
        g.loads = deque(maxlen=512)
        g.execute(NATIVE)
        g.load('Gameplay')
        self.assertFalse(set(RETIRED) & {row['module'] for row in g.loads})
        self.assertEqual(g.load_counts['missing'], 0)
        g.execute("""
            local s=ExposedMembers.SPC_P0
            assert(s.StartStatus.UnitSiteProbe==nil and s.UnitSiteProbe==nil)
            for _,name in ipairs({'UnitTargets','UnitActions','InvestmentAction','CrewProjects','PlayerActionReplies'})do
                assert(s.StartStatus[name].state=='OK',name)
            end
            assert(type(s.UnitTargets.ReadAtSite)=='function' and type(s.UnitActions.Run)=='function')
            s.LastToken='prior';s.Snapshot='prior report'
            Players[0].GetUnits=function()error('RETIRED_NATIVE_READ')end
            GameEvents.SPC_P0_Request.Fire(0,{Action='UNIT_SITE_READ',UnitID=17,Token='retired'})
            assert(s.LastToken=='prior' and s.Snapshot=='prior report')
        """)

    def test_p0_right_click_still_reaches_actual_city_sequence_for_unit_and_city(self):
        with historical_package(B446) as checkout:
            old = historical_gameplay(checkout, revision=B446)
            current = Context(vfs=PackageVFS(forbidden_globals=GLOBALS))
            reports = []
            for previous,gameplay,panel in (
                (True,old,checkout/'Mod/UI'), (False,current,ROOT/'Mod/UI'),
            ):
                gameplay.execute(NATIVE)
                gameplay.load('Gameplay')
                gameplay.execute(SEQUENCE_FIXTURE)
                _, ui = panel_runtime(panel)
                if previous:
                    ui.execute("""
                        Controls.UnitReadButton.callbacks[Mouse.eLClick]()
                        assert(requests[1].Action=='UNIT_SITE_READ' and requests[1].UnitID==17)
                    """)
                else:
                    ui.execute("""
                        assert(Controls.UnitReadButton.callbacks[Mouse.eLClick]==nil)
                        assert(Controls.UnitReadButton.hidden and Controls.UnitReadButtonCaption.text=='城市事件观察')
                    """)
                    self.assertIn('右键“城市事件观察”', gameplay.eval('ExposedMembers.SPC_P0.CitySequenceProbe.Describe(0,1)'))
                current_reports = []
                for city,unit,location,start in ((None,17,'21,20','Start EMPTY'), (11,None,'11,20','Start CITY')):
                    ui.execute("""
                        if ... then selectedUnit=nil end
                        Controls.UnitReadButton.callbacks[Mouse.eRClick]()
                    """, city is not None)
                    packet = dict(ui.eval('requests[#requests]').items())
                    self.assertEqual((packet['Action'],packet.get('CityID'),packet.get('UnitID')),
                                     ('CITY_SEQUENCE_BEGIN',city,unit))
                    gameplay.execute("""
                        local p=...;GameEvents.SPC_P0_Request.Fire(0,p)
                        assert(ExposedMembers.SPC_P0.LastToken==p.Token)
                    """, gameplay.table(packet))
                    report = gameplay.eval('ExposedMembers.SPC_P0.Snapshot')
                    self.assertIn(location,report)
                    self.assertIn(start,report)
                    current_reports.append(report)
                reports.append(current_reports)
            self.assertEqual(*reports)

    def test_unit_sites_retains_spawn_prepare_confirm_and_target_toggle(self):
        path = ROOT/'Mod/UI/UnitSites.xml'
        ids = {el.get('ID') for el in ET.parse(path).iter() if el.get('ID')}
        with historical_package(B446) as checkout:
            before = {el.get('ID') for el in ET.parse(checkout/'Mod/UI/UnitSites.xml').iter() if el.get('ID')}
        self.assertEqual(before-ids,{'ReadButton'})
        self.assertFalse(ids-before)
        ui = Context(name='UI/UnitSites',vfs=PackageVFS(forbidden_globals=GLOBALS))
        ui.execute(NATIVE)
        ui.execute("""
            Mouse={eLClick=1}
            ContextPtr.SetHide=function()end
            ContextPtr.SetUpdate=function(_,fn)update=fn end
            local city={GetID=function()return 11 end}
            local unit={
                GetOwner=function()return 0 end,GetID=function()return 17 end,
                GetType=function()return 1 end,GetX=function()return 21 end,GetY=function()return 20 end}
            UI.GetHeadSelectedUnit=function()return unit end
            UI.GetHeadSelectedCity=function()return city end
            GameInfo.Units={[1]={UnitType='UNIT_SETTLER'}}
            requests={}
            UI.RequestPlayerOperation=function(pid,op,packet)
                assert(pid==0 and op==PlayerOperations.EXECUTE_SCRIPT)
                requests[#requests+1]=packet
            end
            toggled=0;LuaEvents.SPC_ToggleBuilderTargets.Add(function()toggled=toggled+1 end)
            for _,id in ipairs({...})do
                Controls[id]={
                    SetHide=function()end,SetText=function()end,
                    RegisterCallback=function(self,button,fn)assert(button==Mouse.eLClick);self.click=fn end}
            end
        """, *sorted(ids))
        ui.load('UI/UnitSites')
        ui.execute("""
            init()
            for i,id in ipairs({'SpawnCrewButton','PrepareUnitButton','ConfirmUnitButton'})do
                Controls[id].click()
                local p=requests[i]
                assert(p.Action=='UNIT_ACTION_'..({'SPAWN','PREPARE','CONFIRM'})[i])
                assert(p.CityID==11 and p.UnitID==17)
            end
            Controls.BuilderTargetsButton.click()
            assert(toggled==1 and #requests==3)
            Controls.CloseButton.click()
        """)

    def test_exact_site_diagnostic_round_trip_on_the_real_packages(self):
        with historical_package(B446) as before, historical_package(B447) as after:
            verify_package_round_trip(self, before/'Mod', after/'Mod', RETIRED, 'UnitSiteFacts.lua')
