"""PU02: owned UI -> real REST dispatcher/Store, Lua51, explicit controls/transport.

Optional SPC_UNIT_PANEL_LUA/SPC_HD_UNIT_PANEL_LUA select read-only originals.
Only their named builder/renderer fragments run; no claim of native mouse/layout,
whole-panel execution or game PASS. Proprietary source never enters this file.
"""
from contextlib import ExitStack
from hashlib import sha256
import os
from pathlib import Path
import re
import subprocess
import unittest
from unittest.mock import patch

import test_b247_restructuring as old
import test_store_write_boundaries as store
from refactor_harness import ROOT, TrackedLua51, executed, legacy_source_observation, measure

BASE = 'a068c0b27abb7b215452973c3bb1e54fec07b5ab'
PIN = {
    'SPC_UNIT_PANEL_LUA': '59e0ee36a36aeeef927a1024751f2d3c7a259ffefc45159738eb6c684368f8b3',
    'SPC_HD_UNIT_PANEL_LUA': '20c03c1d4aa4796e446739f3d88005ad671abbf18238e7f61ce51d524e135b9d',
}

SETUP = r'''
localPlayer=0;selected=u;u.GetUnitType=u.GetType;u.GetMovesRemaining=function()return 2 end
Game.GetLocalPlayer=function()return localPlayer end
GameInfo.Units={[247]={UnitType='UNIT_SPC_RESTRUCTURING_TEAM'},[248]={UnitType='UNIT_WARRIOR'}}
GameInfo.UnitCommands=setmetatable({UNITCOMMAND_DELETE={Hash=42}},{__call=function()return function()end end})
GameInfo.UnitOperations=setmetatable({},{__call=function()return function()end end})
UnitCommandTypes={DELETE=42};PlayerOperations={EXECUTE_SCRIPT=1};Mouse={eLClick=1,eMouseEnter=2};InterfaceModeTypes={SELECTION=1}
Locale={Lookup=function(key,...)local r={key};for _,v in ipairs({...})do r[#r+1]=tostring(v)end;return table.concat(r,':')end}
packets={};queued={};autoDeliver=true;mode=1;g_isOkayToProcess=true;refreshes=0;nativeClicks=0
UI={GetHeadSelectedUnit=function()return selected end,GetInterfaceMode=function()return mode end,
 SetInterfaceMode=function(value)mode=value end,PlaySound=function()end,DataError=function(s)error(s)end}
UnitManager={GetUnit=function(pid,id)return Z.units[id]end}
function clone(v)return SPCRestructuringModel.Copy(v)end
function deliver(i)
 local p=table.remove(queued,i or 1);assert(p,'NO_QUEUED_REQUEST');dispatch(0,p);return p
end
UI.RequestPlayerOperation=function(pid,kind,p)
 assert(pid==0 and kind==1 and p.OnStart=='SPC_P0_Request')
 packets[#packets+1]=clone(p)
 if autoDeliver then dispatch(pid,p)else queued[#queued+1]=clone(p)end
 if duringSend then duringSend(p)end
 if throwAfterSend then error('TRANSPORT_OUTCOME_UNKNOWN')end
 return not returnFalse
end
function actionCount(action)local n=0;for _,p in ipairs(packets)do if p.Action==action then n=n+1 end end;return n end
function emptyActions()
 return {ATTACK={},BUILD={},GAMEMODIFY={},MOVE={},OFFENSIVESPY={},INPLACE={},SECONDARY={},SPECIFIC={},
 displayOrder={primaryArea={'ATTACK','OFFENSIVESPY','SPECIFIC','MOVE','INPLACE','GAMEMODIFY'},secondaryArea={'SECONDARY'}}}
end
function AddActionToTable(actions,a,disabled,tip,tag,callback)
 local wrapped=function(...)local prior=UI.GetInterfaceMode();if prior~=1 then UI.SetInterfaceMode(1)end;return callback(...,prior)end
 table.insert(actions[a.CategoryInUI],{IconId=a.Icon,Disabled=disabled,helpString=tip,userTag=tag,CallbackFunc=wrapped})
end
function GetUnitActionsTable(unit)
 local a=emptyActions()
 AddActionToTable(a,{CategoryInUI='MOVE',Icon='NATIVE_MOVE'},false,'MOVE',77,function()nativeClicks=nativeClicks+1 end)
 AddActionToTable(a,{CategoryInUI='SECONDARY',Icon='DELETE'},false,'DELETE',42,function()nativeClicks=nativeClicks+1 end)
 return a
end
OnUnitActionClicked=function()nativeClicks=nativeClicks+1 end
OnPromptToDeleteUnit=OnUnitActionClicked;OnDeleteUnit=OnUnitActionClicked;OnUnitActionClicked_CancelSpyMission=OnUnitActionClicked
Refresh=function()end
for _,e in pairs(Events)do
 if type(e)=='table'and e.Add and not e.Remove then
  local add=e.Add;local active={};e.Add=function(fn)active[fn]=true;add(function(...)if active[fn]then fn(...)end end)end
  e.Remove=function(fn)active[fn]=nil end
 end
end
LuaEvents={SPC_ExpeditionActivityChanged={Add=function()end,Remove=function()end}}
ContextPtr={RequestRefresh=function()refreshes=refreshes+1 end,SetShutdown=function(_,fn)shutdown=fn end,SetUpdate=function()error('NO_UI_FRAME_OR_TIMER')end}
buttons={};used=0;width=44;height=53;padding=2
function button()
 return {RegisterCallback=function(self,key,fn)self[key]=fn end,
 SetDisabled=function(self,x)self.disabled=x end,SetAlpha=function(self,x)self.alpha=x end,
 SetToolTipString=function(self,x)self.tip=x end,SetVoid1=function(self,x)self.void1=x end,
 SetVoid2=function(self,x)self.void2=x end,SetTag=function(self,x)self.tag=x end,SetHide=function(self,x)self.hidden=x end,
 click=function(self)if not self.disabled and not self.hidden then return self[1](self.void1,self.void2)end end}
end
m_standardActionsIM={ResetInstances=function()used=0;for _,v in ipairs(buttons)do v.UnitActionButton.hidden=true end end,
 GetInstance=function()
  used=used+1
  if not buttons[used]then buttons[used]={UnitActionButton=button(),UnitActionIcon={SetIcon=function(self,x)self.icon=x end}}end
  buttons[used].UnitActionButton.hidden=false;return buttons[used]
 end}
function AddActionButton(instance,action)
 local b=instance.UnitActionButton;b:SetDisabled(action.Disabled);b:SetToolTipString(action.helpString);b:SetTag(action.userTag)
 b:RegisterCallback(1,action.CallbackFunc);instance.UnitActionIcon:SetIcon(action.IconId)
end
function render(actions)
 m_standardActionsIM:ResetInstances()
 for _,category in ipairs(actions.displayOrder.primaryArea)do for _,action in ipairs(actions[category])do AddActionButton(m_standardActionsIM:GetInstance(),action)end end
end
function draw()
 local a=GetUnitActionsTable(selected);render(a)
 -- Geometry double: native XML Right-growth, native hit-box size and padding.
 local left=500-(used*width+(used-1)*padding)
 for i=1,used do buttons[i].UnitActionButton.x=left+(i-1)*(width+padding)end
 return a
end
function tagged(tag)for i=1,used do local b=buttons[i].UnitActionButton;if b.tag==tag then return b end end end
function press(tag)local b=assert(tagged(tag),'BUTTON_MISSING');return b:click()end
function hit(x)for i=1,used do local b=buttons[i].UnitActionButton;if x>=b.x and x<b.x+width then b:click();return b.tag end end end
function read()svc.Read(0,400);draw()end
function configureStage()
 press(-247);draw();press(-248);T.turn(5);u.x=c:GetX()+1;SPCRestructuringUI.SelectedChanged();read()
 assert(svc.views['0:400'].legal and svc.views['0:400'].action=='CONFIGURE')
end
'''


def owned(lua, name, source=None):
    path = ROOT / 'Mod' / (name + '.lua')
    text = source if source is not None else path.read_text()
    return lua.execute(text)


def ui(native=False, unit_panel_entry='UI/ExpeditionSpyUnitPanel'):
    with patch.object(store, 'LuaRuntime', TrackedLua51), legacy_source_observation():
        l = old.runtime(True)
        source = (ROOT / 'Mod/Gameplay.lua').read_text()
        start = source.index("  if type(params.Action)=='string' and params.Action:match('^REST_')")
        end = source.index("  if params.Action=='NETWORK_ISOLATE'", start)
        executed('Mod/Gameplay.lua:REST_dispatch', sha256(source.encode()).hexdigest(), 'source_fragment', start=start, end=end)
        l.execute('function dispatch(playerID,params)' + source[start:end] + 'end')
        l.execute(SETUP)
        if native:
            native_fragments(l)
        baseline = os.environ.get('SPC_PU02_UI_BASELINE') == BASE
        def include(name):
            if name in ('DL_UnitPanel', 'UnitPanel_Expansion2'):
                return  # selected base fragments or a native double are already installed
            if name == 'ExpeditionSpyUnitPanel':
                name = 'UI/ExpeditionSpyUnitPanel'
            if name == 'RestructuringUI' and baseline:
                text = subprocess.check_output(['git', 'show', BASE + ':Mod/RestructuringUI.lua'], cwd=ROOT).decode()
                executed('baseline:RestructuringUI.lua', sha256(text.encode()).hexdigest(), 'complete_module', commit=BASE)
                return owned(l, name, text)
            return owned(l, name)
        l.globals().include = include
        if unit_panel_entry:
            owned(l, unit_panel_entry)
        l.execute('read()')
        return l


def strip_types(text):
    # Civ script annotations only; never rewrite geometry/callback logic.
    return re.sub(r':\s*(?:table|object|number|boolean|string|ifunction)\b', '', text)


def function(text, name):
    start = text.index(name)
    end = text.index('\nend', start) + len('\nend')
    return strip_types(text[start:end])


def native_fragments(l):
    from xml.etree import ElementTree as ET
    texts = {}
    for key, expected in PIN.items():
        path = Path(os.environ[key]); data = path.read_bytes()
        assert sha256(data).hexdigest() == expected, 'EXTERNAL_PANEL_SOURCE_CHANGED'
        texts[key] = data.decode()
        executed('external:' + key, expected, 'source_fragments_only', redistribution='LOCAL_ONLY')
    base, hd = texts.values()
    xml = Path(os.environ['SPC_UNIT_PANEL_LUA']).with_suffix('.xml').read_bytes()
    assert sha256(xml).hexdigest() == '4187d5fe9cfb9f70bcf6b728670b2ce80317a51d4718dae06c0a335101536f59'
    root = ET.fromstring(xml)
    stack = next(e for e in root.iter() if e.get('ID') == 'StandardActionsStack')
    instance = next(e for e in root.iter() if e.get('Name') == 'UnitActionInstance')
    b, icon = list(instance)[0], list(list(instance)[0])[0]
    assert stack.get('StackGrowth') == 'Right'
    l.execute('width,height,padding=...', *map(int, b.get('Size').split(',')), int(stack.get('Padding')))
    assert icon.get('Size') == '38,38'
    l.execute(function(base, 'function AddActionToTable('))
    l.execute(function(base, 'function AddActionButton('))
    # HD additions/replacement do not replace the native action view geometry.
    l.execute('BASE_AddActionButton=AddActionButton;m_HDUnitCommands={}')
    l.execute(function(hd, 'function AddActionButton('))
    l.execute(function(hd, 'local BASE_GetUnitActionsTable = function').replace('local BASE_GetUnitActionsTable', 'BASE_GetUnitActionsTable', 1))
    l.execute(function(hd, 'function GetUnitActionsTable('))
    l.execute('''local build=GetUnitActionsTable
      GetUnitActionsTable=function(unit)local a=build(unit)
       AddActionToTable(a,{CategoryInUI='MOVE',Icon='NATIVE_MOVE'},false,'MOVE',77,function()nativeClicks=nativeClicks+1 end)
       return a end
      m_buildActionsIM={DestroyInstances=function()end,ResetInstances=function()end}
      m_secondaryActionsIM={ResetInstances=function()end};m_groupArtIM={ResetInstances=function()end}
      Controls={UnitPanelBaseContainer={SetSizeX=function()end}}
      HidePromotionPanel=function()end;StartIconGroup=function()m_numIconsInCurrentIconGroup=0 end;EndIconGroup=function()end
      table.count=function(t)local n=0;for _ in pairs(t)do n=n+1 end;return n end
    ''')
    start = base.index('function View(data)')
    end = base.index('\n\t\t-- Next fill in secondardy actions area', start)
    l.execute(strip_types(base[start:end]) + '\nend\nend')
    l.execute('render=function(a)View({Actions=a})end')


class Actions(unittest.TestCase):
    native = False

    def fixture(self):
        return ui(self.native)

    def test_A_position_stays_fixed_and_B_is_left_after_instance_reuse(self):
        l = self.fixture(); l.execute("local x=tagged(-247).x;press(-247);draw();assert(tagged(-247).x==x,'A_MOVED');assert(tagged(-248).x+width+padding==x,'B_NOT_LEFT');assert(not tagged(-247).disabled and tagged(-247).tip:find('REST_PREVIEW'));draw();assert(tagged(-248).x<tagged(-247).x)")

    def test_prepared_A_is_inert_even_for_retained_old_callback(self):
        l = self.fixture(); l.execute("local old=tagged(-247)[1];press(-247);draw();local plan=svc.views['0:400'].prepared;press(-247);old();assert(actionCount('REST_PREPARE')==1,'A_REPREPARED');assert(svc.views['0:400'].prepared==plan and not Z.state())")

    def test_delayed_prepare_blocks_duplicate_A_across_refresh_and_unrelated_reply(self):
        l = self.fixture(); l.execute("autoDeliver=false;press(-247);draw();assert(tagged(-247).disabled and tagged(-247).tip:find('REST_PENDING'));ExposedMembers.SPC_RestructuringReply={owner=0,unit=400,token='UNRELATED',ok=true};press(-247);assert(actionCount('REST_PREPARE')==1,'DUPLICATE_PENDING_A');assert(not tagged(-248));deliver();ExposedMembers.SPC_RestructuringReply={owner=0,unit=400,token='OTHER_AFTER_ACK',ok=true};draw();assert(tagged(-248) and not Z.state());press(-247);assert(actionCount('REST_PREPARE')==1)")

    def test_same_icon_instances_dispatch_at_distinct_nonoverlapping_coordinates(self):
        l = self.fixture(); l.execute("press(-247);draw();local a,b=tagged(-247),tagged(-248);assert(a.x>=b.x+width);assert(hit(a.x+width/2)==-247);assert(not Z.state() and actionCount('REST_PREPARE')==1);assert(hit(b.x+width/2)==-248);assert(Z.state().phase=='REALLOCATING' and T.control(c).potential==3);draw();assert(not tagged(-248))")

    def test_old_B_cannot_confirm_a_replaced_plan(self):
        l = self.fixture(); l.execute("press(-247);draw();local old=tagged(-248)[1];Z.command('REST_PREPARE','OTHER_PLAN');old();assert(actionCount('REST_CONFIRM')==0,'STALE_B_SENT');assert(not Z.state());draw();press(-248);assert(Z.state().phase=='REALLOCATING')")

    def test_delayed_confirmation_double_click_sends_one_packet_and_debits_once(self):
        l = self.fixture(); l.execute("press(-247);draw();autoDeliver=false;local f=tagged(-248)[1];f();f();draw();press(-248);assert(actionCount('REST_CONFIRM')==1,'DUPLICATE_PENDING_B');deliver();draw();assert(T.control(c).potential==3 and Z.state().phase=='REALLOCATING');f();assert(actionCount('REST_CONFIRM')==1)")

    def test_moved_unit_old_callback_rejected_then_new_current_preview_can_prepare(self):
        l = self.fixture(); l.execute("local f=tagged(-247)[1];u.x=u.x+1;SPCRestructuringUI.SelectedChanged();f();assert(actionCount('REST_PREPARE')==0,'STALE_POSITION_SENT');u.x=c:GetX();SPCRestructuringUI.SelectedChanged();draw();press(-247);assert(svc.views['0:400'].prepared)")

    def test_stale_turn_owner_selection_and_not_local_turn_never_send(self):
        for code in ('localPlayer=1', 'selected=Z.team(401);selected.GetUnitType=selected.GetType', 'g_isOkayToProcess=false', 'T.turn(1)'):
            with self.subTest(code=code):
                l = self.fixture(); l.execute("local f=tagged(-247)[1];" + code + ";f();assert(actionCount('REST_PREPARE')==0)")

    def test_unpublished_or_illegal_view_old_callback_never_sends(self):
        for code in ("svc.views['0:400']=nil", "svc.views['0:400'].legal=false"):
            with self.subTest(code=code):
                l = self.fixture(); l.execute("local f=tagged(-247)[1];" + code + ";f();assert(actionCount('REST_PREPARE')==0,'STALE_VIEW_SENT')")

    def test_backend_rejects_new_qualification_loss_after_confirm_was_sent(self):
        l = self.fixture(); l.execute("press(-247);draw();autoDeliver=false;press(-248);u.x=u.x+1;deliver();draw();assert(not svc.lastRequest.ok and not Z.state() and Z.kills==0)")

    def test_configuration_B_consumes_once_and_prepared_A_remains_inert(self):
        l = self.fixture(); l.execute("configureStage();local x=tagged(-247).x;press(-247);draw();assert(tagged(-247).x==x and tagged(-248).tip:find('REST_CONFIGURE'));local f=tagged(-248)[1];press(-247);assert(actionCount('REST_PREPARE')==2);f();f();draw();assert(Z.kills==1 and Z.state().phase=='SETTLED' and T.control(c).specialization=='CULTURE');assert(actionCount('REST_CONFIRM')==2)")

    def test_configuration_unknown_native_outcome_never_replays(self):
        l = self.fixture(); l.execute("configureStage();press(-247);draw();local f=tagged(-248)[1];destroyFail=true;f();draw();f();press(-247);assert(Z.kills==1 and Z.state().phase=='CONSUMING' and not svc.lastRequest.ok);assert(not tagged(-248));Events.GameCoreEventPublishComplete.Fire();assert(Z.kills==1)")

    def test_transport_exception_after_delivery_does_not_enable_replay(self):
        for flag in ('throwAfterSend=true', 'returnFalse=true'):
            with self.subTest(flag=flag):
                l = self.fixture(); l.execute("press(-247);draw();" + flag + ";local f=tagged(-248)[1];pcall(f);pcall(f);draw();assert(actionCount('REST_CONFIRM')==1 and Z.state().phase=='REALLOCATING')")

    def test_lost_confirmation_has_no_automatic_resend_or_timed_release(self):
        l = self.fixture(); l.execute("press(-247);draw();autoDeliver=false;press(-248);queued={};for i=1,10 do Events.GameCoreEventPublishComplete.Fire();draw()end;press(-248);assert(actionCount('REST_CONFIRM')==1,'LOST_CONFIRM_REPLAYED');assert(not Z.state());SPCRestructuringUI.SelectedChanged();assert(actionCount('REST_CONFIRM')==1)")

    def test_same_unit_id_new_binding_rejects_old_callback(self):
        l = self.fixture(); l.execute("local f=tagged(-247)[1];u=Z.team(400);selected=u;u.GetUnitType=u.GetType;u.GetMovesRemaining=function()return 2 end;u.properties.SPC_RESTRUCTURING_TEAM_V1.uid='TEAM:REPLACEMENT';SPCRestructuringUI.SelectedChanged();f();assert(actionCount('REST_PREPARE')==0);draw();press(-247);assert(svc.views['0:400'].prepared)")

    def test_known_failed_prepare_can_retry_after_new_reliable_read(self):
        l = self.fixture(); l.execute("autoDeliver=false;press(-247);local read=shared.EffectiveFacts.Read;shared.EffectiveFacts.Read=function()error('REST_TEMPORARILY_UNAVAILABLE')end;deliver();assert(not svc.lastRequest.ok);shared.EffectiveFacts.Read=read;SPCRestructuringUI.SelectedChanged();deliver();draw();press(-247);assert(actionCount('REST_PREPARE')==2);deliver();draw();assert(tagged(-248) and not Z.state())")

    def test_ordinary_units_and_delete_protection_preserved(self):
        l = self.fixture(); l.execute("local a=draw();assert(#a.SECONDARY==0);OnPromptToDeleteUnit();OnDeleteUnit({player=0,id=400});assert(nativeClicks==0);u.GetUnitType=function()return 248 end;draw();assert(not tagged(-247));OnUnitActionClicked();assert(nativeClicks==1)")

    def test_backend_plan_reference_is_rechecked_and_stale_credential_rejected(self):
        l = self.fixture(); l.execute("press(-247);local plan=svc.views['0:400'].prepared;Z.command('REST_CONFIRM','WRONG','NOT_'..plan);assert(not svc.lastRequest.ok and not Z.state());Z.command('REST_CONFIRM','RIGHT',plan);assert(Z.state().phase=='REALLOCATING');Z.command('REST_CONFIRM','REPLAY',plan);assert(T.control(c).potential==3 and Z.kills==0)")


@unittest.skipUnless(all(os.environ.get(k) for k in PIN), 'read-only pinned external panel files not configured')
class NativePanelFragments(Actions):
    """Same contracts through actual native/HD builders,renderer and XML dimensions."""
    native = True


class _PanelLua51(TrackedLua51):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # refresh_fixture (not production) was authored for Lua55. Preserve
        # vararg arity in that deferred-refresh double; primary PU02 cases run
        # bare Lua51 without these two fixture-only compatibility helpers.
        self.execute("table.pack=function(...)return {n=select('#',...),...}end;table.unpack=unpack")

    def execute(self, source, *args, **kwargs):
        # The frozen Expedition fixture intentionally stubs include(). Supply
        # its real production dependency; keep every frozen assertion unchanged.
        panel = (ROOT/'Mod/UI/ExpeditionSpyUnitPanel.lua').read_text()
        if source == panel and self.globals().SPCRestructuringUI is None:
            owned(self, 'RestructuringUI')
        return super().execute(source, *args, **kwargs)


class _PanelProfile:
    def setUp(self):
        import test_expedition_spy_task as fixture
        self.stack = ExitStack()
        self.stack.enter_context(patch.object(fixture, 'LuaRuntime', _PanelLua51))
        self.stack.enter_context(legacy_source_observation())

    def tearDown(self):
        self.stack.close()


import test_expedition_idle_actions as idle_cases


class ExistingIdleActions(_PanelProfile, idle_cases.IdleActions):
    """Unchanged frozen idle/selection/permission assertions, actual dependency."""


class ExistingArrivalRefresh(_PanelProfile, idle_cases.ArrivalRefresh):
    """Unchanged frozen refresh/reentry/shutdown assertions, Lua51."""


class Restricted(unittest.TestCase):
    def test_adapter_has_no_timer_native_mutation_or_unbounded_retained_collection(self):
        from lupa.lua51 import LuaRuntime
        l = LuaRuntime(unpack_returned_tuples=True)
        l.execute('io=nil;os=nil;debug=nil;package=nil;require=nil;dofile=nil;loadfile=nil')
        owned(l, 'RestructuringUI')
        s = (ROOT/'Mod/RestructuringUI.lua').read_text()
        self.assertNotRegex(s, r'SetUpdate\s*\(')
        for op in ('Destroy(', 'SetProperty(', 'ChangeGoldBalance(', 'Audit(', '.Add('):
            self.assertNotIn(op, s)
        measure('PU02_UI_scope', {'new_timers':0,'new_event_subscriptions':0,'native_writes':0,'saved_fields':0})


if __name__ == '__main__':
    unittest.main()
