"""Exercise manifest-selected city panels over pinned stock callback fragments."""

from hashlib import sha256
import os
from pathlib import Path, PurePosixPath
import unittest
from unittest.mock import patch
import xml.etree.ElementTree as ET

from refactor_harness import ROOT, PackageVFS, TrackedLua51, executed, legacy_source_observation
from test_b265_city_presentation import presentation
import test_culture_institutions as culture
from test_environment_assembly import manifest, matches_profile
from test_pu02_restructuring_ui import function, strip_types


PINS = {
    'Base/Assets/UI/Panels/CityPanel.lua': '8598a08ad83ef9fc69dfbfca9541ebeda1e7636b4608dd9d5fa767f6e8e876fa',
    'Base/Assets/UI/Panels/CityPanelOverview.lua': '1409b950170e7fe9cc54b5889df2ddcf57a4961e7e0f56494ad369dcf06596b9',
    'Base/Assets/UI/Panels/CityPanel.xml': '3c97c071e1f4d0e04e2ddc9395081b5a353257dd8de1de178f87f07a8437c996',
    'Base/Assets/UI/Panels/CityPanelOverview.xml': 'ffd7ffbff92ec0c466829bfca4b289b4497b51cf89ec2da479aa10ea3a8f46bd',
    'DLC/Expansion2/UI/Replacements/CityPanel_Expansion2.lua': '6004871c523b4cb3a389ebde452a7b26792bd9889a6e50f5c8729450f884fb3b',
    'DLC/Expansion2/UI/Replacements/CityPanelOverview_Expansion2.lua': '16f9aa76df9c2e5523dcc9fef0afd7850380bbb7beff26901dfc64ccca91350d',
}


def official(rel, mode):
    raw = (Path(os.environ['SPC_OFFICIAL_ASSETS']) / rel).read_bytes()
    pin = PINS[rel]
    assert sha256(raw).hexdigest() == pin, 'EXTERNAL_CITY_PANEL_SOURCE_CHANGED'
    executed('external:' + rel, pin, mode)
    return raw.decode()


def attach(lua, name, hd, base):
    doc = manifest()
    criteria = {entry.get('id'): entry for entry in doc.findall('./ActionCriteria/Criteria')}
    entries = [entry.findtext('Properties/LuaReplace') for entry in doc.findall('./InGameActions/ReplaceUIScript')
               if entry.findtext('Properties/LuaContext') == name and matches_profile(entry, criteria, hd)]
    assert len(entries) <= 1, 'MULTIPLE_CITY_PANEL_ENTRIES'
    vfs = PackageVFS()
    expected = 'DL_' + name if hd else name + '_Expansion2'
    entered = []

    def load(relative):
        lua.execute((ROOT / 'Mod' / relative).read_text())

    def include(module):
        if module == expected:
            assert not entered, 'CITY_PANEL_BASE_LOADED_TWICE'
            entered.append(module)
            expansion = f'DLC/Expansion2/UI/Replacements/{name}_Expansion2.lua'
            if not hd:
                assert f'include("{name}_Expansion1")' in official(expansion, 'native_chain_source_review')
            base()
            return
        matches = [path for path in vfs.imports if PurePosixPath(path).name == module + '.lua']
        assert len(matches) == 1, 'CITY_PANEL_INCLUDE_UNRESOLVED ' + module
        load(matches[0])

    lua.globals().include = include
    with legacy_source_observation():
        if entries:
            assert entries[0] in vfs.files
            load(entries[0])
        else:
            include(expected)
    assert entered == [expected], 'CITY_PANEL_BASE_MISSING'


TIMED_SETUP = """
function event()
 local rows={}
 return setmetatable({Add=function(f)rows[#rows+1]=f end,
  Remove=function(f)for i=#rows,1,-1 do if rows[i]==f then table.remove(rows,i)end end end,
  Count=function()return #rows end},
  {__call=function(_,...)for _,f in ipairs(rows)do f(...)end end})
end
LuaEvents=setmetatable({},{__index=function(t,k)local e=event();rawset(t,k,e);return e end})
local function control()
 local c={}
 function c:SetHide(v)self.hidden=v end
 function c:SetText(v)self.text=v end
 function c:GetText()return self.text end
 function c:GetSizeX()return 1 end
 function c:SetToolTipString(v)self.tip=v end
 function c:TrySetIcon(v)self.icon=v;return true end
 function c:CalculateSize()end
 function c:SetPercent(v)self.percent=v end
 function c:SetShadowPercent(v)self.shadow=v end
 return c
end
Controls=setmetatable({},{__index=function(t,k)local c=control();rawset(t,k,c);return c end})
ContextPtr={SetShutdown=function(_,fn)shutdown=fn end,SetUpdate=function()error('NO_NEW_FRAME_HANDLER')end}
function Clamp(v,lo,hi)return math.max(lo,math.min(hi,v))end
function TruncateStringWithTooltip(c,...)c:SetToolTipString('native tooltip')end
Locale={Lookup=function(k)return k end,ToUpper=string.upper}
target=89
local queue={GetCurrentProductionTypeHash=function()return target end}
g_pCity={GetOwner=function()return 0 end,GetID=function()return 7 end,GetBuildQueue=function()return queue end}
Players={[0]={GetCities=function()return {FindID=function(_,id)if id==7 then return g_pCity end end}end}}
Game={GetLocalPlayer=function()return 0 end}
GameInfo={Projects={PROJECT_SPC_ENGINEERING_STUDY={Hash=89}}}
ExposedMembers={SPC_P0={EngineeringStudy={views={['0:7']={stage='ACTIVE',L=1}}}}}
data={CurrentTurnsLeft=12,CurrentProdPercent=.5,ProdPercentNextTurn=.6,CurrentProductionStats='',
 CurrentProductionDescription='Native',CurrentProductionName='Native',CurrentProductionIcons={'ICON_NATIVE'}}
local refreshes=0
function Refresh()refreshes=refreshes+1;ViewMain(data)end
function refreshCount()return refreshes end
nativeShutdown=0
function OnShutdown()nativeShutdown=nativeShutdown+1 end
ContextPtr:SetShutdown(OnShutdown)
"""


OVERVIEW_SETUP = """
local lookup=ContextPtr.LookUpControl
ContextPtr.LookUpControl=function(self,path)
 if path:find('CityPanelOverview',1,true)then return parent end
 return lookup(self,path)
end
Controls.HealthButton={}
Controls.BuildingsButton={SetSelected=function()end}
Controls.BuildingsIcon={SetColorByName=function()end}
local offset=-330
opens,closes,cityShutdown=0,0,0
Controls.OverviewSlide={GetOffsetX=function()return offset end,
 SetToBeginning=function()offset=-330 end,Play=function()offset=0;opens=opens+1 end,
 SetToEnd=function()offset=0 end,Reverse=function()offset=-330;closes=closes+1 end}
LuaEvents.CityPanel_SetOverViewState=event()
LuaEvents.CityPanelOverview_Opened=event()
LuaEvents.CityPanelOverview_CloseButton=event()
UI.PlaySound=function()end
UI.SetInterfaceMode=function()end
UILens={SetActive=function()end}
InterfaceModeTypes={CITY_SELECTION=1,SELECTION=2}
function HideAll()Controls.PanelBreakdown:SetHide(true)end
function OnShutdown()cityShutdown=cityShutdown+1 end
ContextPtr:SetShutdown(OnShutdown)
local m_isShowingPanel=false
local m_tabs={selectedControl=Controls.HealthButton}
local m_pCity,m_kData
m_tabs.SelectTab=function(tab)
 m_tabs.selectedControl=tab
 if tab==Controls.BuildingsButton then OnSelectBuildingsTab()else HideAll()end
end
function Refresh()
 m_pCity=UI.GetHeadSelectedCity()
 m_kData=data
 m_tabs.SelectTab(m_tabs.selectedControl)
end
function isOpen()return m_isShowingPanel end
"""


class CityPanelProfiles(unittest.TestCase):
    def test_timed_city_panel_reuses_native_numeric_data_and_scopes_refresh(self):
        stock = official('Base/Assets/UI/Panels/CityPanel.lua', 'source_fragments_only')
        production = strip_types(stock[stock.index('\t--Production\n'):stock.index('\t-- Tutorial lockdown')])
        for hd in (False, True):
            with self.subTest(hd=hd):
                lua = TrackedLua51(unpack_returned_tuples=True)
                lua.execute(TIMED_SETUP)
                def base():
                    lua.execute('local MAX_BEFORE_TRUNC_TURN_LABELS=100\nfunction ViewMain(data)\n local widthNumLabel\n' +
                                production + '\nend')
                attach(lua, 'CityPanel', hd, base)
                lua.execute("""
                    ViewMain(data)
                    assert(Controls.ProductionNum.text=='1' and Controls.ProductionLabel.text=='回合后完成',
                        'NATIVE_TIMED_PROJECT_PRESENTATION_MISSING')
                    assert(data.CurrentTurnsLeft==12 and Controls.ProductionTurnsBar.percent==0)
                    LuaEvents.SPC_TimedProjectDisplayChanged(1,7)
                    LuaEvents.SPC_TimedProjectDisplayChanged(0,8)
                    assert(refreshCount()==0)
                    ExposedMembers.SPC_P0.EngineeringStudy.views['0:7'].stage='HELD'
                    LuaEvents.SPC_TimedProjectDisplayChanged(0,7)
                    assert(refreshCount()==1 and Controls.ProductionNum.text=='已暂停')
                    target=-1
                    LuaEvents.SPC_TimedProjectDisplayChanged(0,7)
                    assert(refreshCount()==2 and Controls.ProductionNum.text==12 and Controls.ProductionTurnsBar.percent==.5)
                """)
                lua.execute('shutdown();assert(nativeShutdown==1)')
                lua.execute('LuaEvents.SPC_TimedProjectDisplayChanged(0,7);assert(refreshCount()==2)')

    def test_overview_shortcut_and_native_toggle_share_the_applied_building_tab(self):
        path = ROOT / 'Mod/UI/InstitutionOverview.lua'
        read = Path.read_text
        stock = official('Base/Assets/UI/Panels/CityPanelOverview.lua', 'source_fragments_only')
        names = ['OnSelectBuildingsTab', 'GetSelectedTabButton', 'Close', 'OnCloseButtonClicked',
                 'OnShowOverviewPanel', 'ToggleOverviewTab', 'OnToggleBuildingsTab']
        for hd in (False, True):
            with self.subTest(hd=hd):
                # Prepare the real typed city reply and controls. Attach the selected
                # root afterwards so the shortcut must replay through its real listener.
                with patch.object(culture, 'LuaRuntime', TrackedLua51), patch.object(Path, 'read_text',
                        lambda p, *a, **kw: '' if p == path else read(p, *a, **kw)):
                    lua = presentation()
                def base():
                    lua.execute(OVERVIEW_SETUP + '\n' + '\n'.join(function(stock, f'function {name}(') for name in names))
                attach(lua, 'CityPanelOverview', hd, base)
                lua.execute("""
                    assert(#requests==1 and not Controls.ActiveShortcut.hidden)
                    Controls.ActiveShortcut.click()
                    assert(isOpen() and opens==1 and GetSelectedTabButton()==Controls.BuildingsButton,
                        'OFFICIAL_INSTITUTION_SHORTCUT_UNROUTED')
                    assert(#rows.items==4 and rows.items[3].State.text=='当前')
                    assert(#rendered.BuildingsAndDistricts[1].Buildings==2 and #data.BuildingsAndDistricts[1].Buildings==3)
                    Controls.ActiveShortcut.click()
                    assert(opens==1 and closes==0 and isOpen())
                    OnToggleBuildingsTab()
                    assert(not isOpen() and closes==1)
                    Controls.ActiveShortcut.click()
                    assert(isOpen() and opens==2)
                    LuaEvents.SPC_OpenInstitutions(1,4)
                    LuaEvents.SPC_OpenInstitutions(0,99)
                    assert(opens==2)
                    stopBridge()
                    assert(cityShutdown==1 and #LuaEvents.SPC_OpenInstitutions.handlers==0)
                """)

    def test_shipped_layout_has_existing_mounting_controls(self):
        panel = ET.fromstring(official('Base/Assets/UI/Panels/CityPanel.xml', 'native_control_source_review'))
        # The shipped overview contains a duplicate attribute outside these controls.
        overview = official('Base/Assets/UI/Panels/CityPanelOverview.xml', 'native_control_source_review')
        self.assertIsNotNone(panel.find(".//Grid/Stack[@ID='ActionStack']"))
        self.assertRegex(overview, r'<Grid\s+ID="PanelBreakdown"[^>]*>\s*<Stack\s+ID="BreakdownStack"')
        self.assertRegex(overview, r'<Stack\s+ID="PanelStack"')
