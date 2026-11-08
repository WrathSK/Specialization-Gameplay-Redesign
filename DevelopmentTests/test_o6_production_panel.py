"""Exercise actual SPC panel entries with read-only stock callback fragments.

The fixture supplies native list rows and operation sinks, rather than running
the whole engine panel or issuing native requests.
"""
from hashlib import sha256
import os
from pathlib import Path, PurePosixPath
import unittest

from refactor_harness import Context, PackageVFS, executed
from test_b239_commerce_ui import SETUP as COMMERCE_VIEW
from test_environment_assembly import manifest, matches_profile
from test_pu02_restructuring_ui import function

BASE_FILES = {
    'Base/Assets/UI/Panels/ProductionPanel.lua': '99f1ff8235e9f533ade8eb672cd0668b9ca8f47dd96ab36e393520ba5a923083',
    'Base/Assets/UI/ProductionHelper.lua': '7653d066bc548e7a5fd51120eb5338aebd94331d5a26acde434e3bb2906ca1c9',
}
FIXTURE = r"""
Game.GetCurrentGameTurn=function()return 6 end
GameInfo={Projects={}}
GameConfiguration={GetValue=function(id)assert(id=='GAMEMODE_HEROES');return heroes end}
UI.PlaySound=function()end
nativeOps={};CityOperationTypes={BUILD='BUILD',PARAM_PROJECT_TYPE='project',PARAM_UNIT_TYPE='unit',
 PARAM_INSERT_MODE='mode',PARAM_QUEUE_LOCATION='location',PARAM_QUEUE_DESTINATION_LOCATION='location',
 VALUE_REPLACE_AT='replace',VALUE_REMOVE_AT='remove'}
CityManager={RequestOperation=function(city,op,params)
 assert(city==c and op=='BUILD');nativeOps[#nativeOps+1]=params
end}
function CheckQueueItemSelected()local found=queueSelected;queueSelected=false;return found end
function GetBuildInsertMode(p)p.mode='replace';p.location=0 end
function PopulateGenericItemData()end
function CreateQueueInstance()end
function RefreshCurrentProduction()end
nativeReads=0;nativeShutdown=0
function OnShutdown()nativeShutdown=nativeShutdown+1 end
function RightClickProductionItem(kind)lookupKind=kind end
local kinds={'PROJECT_NATIVE','PROJECT_SPC_COMMERCIALIZATION','PROJECT_SPC_CAPITAL_INVESTMENT',
 'PROJECT_SPC_DEVELOPMENT_INVESTMENT','PROJECT_SPC_CREW_420','PROJECT_SPC_CREW_250'}
function nativeData()
 nativeReads=nativeReads+1
 local projects={}
 for i,kind in ipairs(kinds)do
  projects[i]={Type=kind,Name=kind,Hash=100+i,Cost=600,Progress=0,TurnsLeft=25,IsCurrentProduction=false,
   Disabled=i>1 and i<5,ToolTip='NATIVE'}
 end
 return {City=c,Owner=0,ProjectItems=projects,UnitItems={{Type='UNIT_NATIVE',Hash=201}}}
end
local shared=ExposedMembers.SPC_P0
shared.Version=SPCP0.VERSION
shared.CapitalInvestment={views={['0:9']={available=true}}}
shared.DevelopmentInvestment={views={['0:9']={available=true}}}
shared.CrewProjects={views={['0:9']={allowed={PROJECT_SPC_CREW_250=true,PROJECT_SPC_CREW_420=true}}},errors={}}
capitalOpens=0;developmentOpens=0
LuaEvents.SPC_CapitalOpen.Add(function()capitalOpens=capitalOpens+1 end)
LuaEvents.SPC_DevelopmentOpen.Add(function()developmentOpens=developmentOpens+1 end)
"""


def panel(hd=False, heroes=False):
    doc = manifest()
    criteria = {e.get('id'): e for e in doc.findall('./ActionCriteria/Criteria')}
    entries = [
        e.findtext('Properties/LuaReplace') for e in doc.findall('./InGameActions/ReplaceUIScript')
        if e.findtext('Properties/LuaContext') == 'ProductionPanel' and matches_profile(e, criteria, hd)
    ]
    if len(entries) > 1:
        raise AssertionError('MULTIPLE_PRODUCTION_PANEL_ENTRIES')
    vfs = PackageVFS()
    context = Context(name='ProductionPanel', vfs=vfs)
    context.execute(COMMERCE_VIEW)
    context.execute('heroes=...', heroes)
    context.execute(FIXTURE)
    assets = Path(os.environ['SPC_OFFICIAL_ASSETS'])
    texts = {}
    for rel, pin in BASE_FILES.items():
        raw = (assets / rel).read_bytes()
        assert sha256(raw).hexdigest() == pin, 'EXTERNAL_PRODUCTION_SOURCE_CHANGED'
        executed('external:' + rel, pin, 'source_fragments_only')
        texts[rel] = raw.decode()
    base, helper = texts.values()
    for name in ('AdvanceProject', 'BuildUnit'):
        context.execute(function(base, f'function {name}('))
    context.execute(function(helper, 'function RemoveQueueItem('))
    context.execute('GetData=nativeData')
    loaded = []
    expected = 'DL_ProductionPanel' if hd else ('ProductionPanel_Babylon_Heroes' if heroes else 'ProductionPanel')

    def include(name):
        if name in ('ProductionPanel', 'ProductionPanel_Babylon_Heroes', 'DL_ProductionPanel'):
            assert name == expected and not loaded, 'WRONG_NATIVE_PRODUCTION_BASE'
            loaded.append(name)
            if hd:
                context.execute('GetDataHelper=nativeData;GetData=function()return GetDataHelper()end')
            elif name == 'ProductionPanel_Babylon_Heroes':
                rel = 'DLC/Babylon/UI/Replacements/ProductionPanel_Babylon_Heroes.lua'
                raw = (assets / rel).read_bytes()
                pin = '28e097095c5b9876d581accdd10f4a5e6636064506d841177593211ce376848c'
                assert sha256(raw).hexdigest() == pin, 'EXTERNAL_HEROES_SOURCE_CHANGED'
                executed('external:' + rel, pin, 'source_fragments_only')
                context.execute('local RightClickProductionItem_BASE=RightClickProductionItem\n' +
                                function(raw.decode(), 'function RightClickProductionItem('))
            return
        if name == 'Probe':
            return  # The Commerce fixture provides this context's identity double.
        hits = [p for p in vfs.imports if PurePosixPath(p).name == name + '.lua']
        if len(hits) != 1:
            raise AssertionError(f'PRODUCTION_INCLUDE_UNRESOLVED {name}')
        context.load(hits[0], included=True)

    context.globals().include = include
    if entries:
        context.load(entries[0])
    else:
        include(expected)
    return context, loaded


class ProductionPanelProfiles(unittest.TestCase):
    def test_native_lists_preserve_visible_items_and_attach_applied_actions(self):
        for hd, heroes in ((False, False), (False, True), (False, 1), (True, False)):
            with self.subTest(hd=hd, heroes=heroes):
                context, bases = panel(hd, heroes)
                context.execute("""
                    local data=GetData()
                    assert(nativeReads==1 and data.ProjectItems[1].Type=='PROJECT_NATIVE')
                    assert(data.ProjectItems[1].Cost==600 and data.UnitItems[1].Type=='UNIT_NATIVE')
                    for i=2,4 do local item=data.ProjectItems[i]
                        assert(not item.Disabled and item.Cost==0 and item.TurnsLeft==0,'APPLIED_ACTION_ROW_MISSING')
                    end
                    assert(data.ProjectItems[5].Type=='PROJECT_SPC_CREW_250' and data.ProjectItems[6].Type=='PROJECT_SPC_CREW_420')
                    assert(not SPCOfficialProductionBase and #nativeOps==0)
                    assert(#sent==1 and sent[1].OnStart=='SPC_ExpeditionTrainingRequest' and sent[1].Action=='SYNC')
                    GetData()
                    assert(#sent==1,'UNCHANGED_RENDER_RESENT_TRAINING_SYNC')
                """)
                self.assertEqual(bases, ['DL_ProductionPanel' if hd else
                    ('ProductionPanel_Babylon_Heroes' if heroes else 'ProductionPanel')])

    def test_official_action_rows_open_once_and_never_enqueue(self):
        panel()[0].execute("""
            local data=GetData()
            local reads=#sent
            for i=2,4 do AdvanceProject(c,data.ProjectItems[i])end
            assert(opens==1 and capitalOpens==1 and developmentOpens==1,'OFFICIAL_ACTIONS_NOT_INTERCEPTED')
            assert(#nativeOps==0 and #sent==reads,'PANEL_OPEN_MUTATED_QUEUE_OR_BALANCE')
            queueSelected=true
            AdvanceProject(c,data.ProjectItems[1])
            assert(#nativeOps==0 and not queueSelected)
            AdvanceProject(c,data.ProjectItems[1])
            BuildUnit(c,data.UnitItems[1])
            RemoveQueueItem(3)
            assert(#nativeOps==3 and nativeOps[1].project==101 and nativeOps[1].mode=='replace')
            assert(nativeOps[2].unit==201 and nativeOps[3].mode=='remove' and nativeOps[3].location==3)
        """)

    def test_crew_click_retains_reservation_and_reader_lifecycle(self):
        panel()[0].execute("""
            local item=GetData().ProjectItems[5]
            local reads=#sent
            AdvanceProject(c,item)
            AdvanceProject(c,item)
            assert(#sent==reads+1 and sent[#sent].Action=='RESERVE' and sent[#sent].Project=='PROJECT_SPC_CREW_250',
                'CREW_RESERVATION_BYPASSED')
            assert(#nativeOps==0 and type(ExposedMembers.SPC_CrewNativeRead)=='function')
            assert(type(ExposedMembers.SPC_CrewTargetRead)=='function','CREW_TARGET_SLOT_MISSING')
            ContextPtr.shutdown()
            assert(nativeShutdown==1 and ExposedMembers.SPC_CrewNativeRead==nil and ExposedMembers.SPC_CrewTargetRead==nil)
        """)

    def test_heroes_mode_keeps_shipped_right_click_lookup(self):
        panel(heroes=True)[0].execute("""
            GameInfo={Projects={PROJECT_HERO_EXAMPLE={}}}
            GameInfo.HeroClasses=function()
                local sent=false
                return function()
                    if not sent then
                        sent=true
                        return {CreationProjectType='PROJECT_HERO_EXAMPLE',UnitType='UNIT_HERO_EXAMPLE'}
                    end
                end
            end
            RightClickProductionItem('PROJECT_HERO_EXAMPLE')
            assert(lookupKind=='UNIT_HERO_EXAMPLE')
            RightClickProductionItem('PROJECT_NATIVE')
            assert(lookupKind=='PROJECT_NATIVE')
        """)
