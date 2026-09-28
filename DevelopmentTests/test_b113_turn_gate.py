"""B113 actual UI Lua, isolated native fixtures. No Civ VI engine claims."""
from pathlib import Path
import unittest
import xml.etree.ElementTree as ET
from lupa.lua55 import LuaRuntime
from test_b112_turn_probe import FIXTURE
ROOT=Path(__file__).resolve().parents[1]
SOURCE=(ROOT/'Mod/UI/TimedTurnProbe.lua').read_text()
EXTRA=r"""
for _,n in ipairs({'EndTurnDirty','EndTurnBlockingChanged','CityProductionChanged','NotificationAdded','NotificationDismissed','ResearchChanged','UnitOperationSegmentComplete','UnitOperationsCleared','UserOptionChanged','CityRemovedFromMap'}) do Events[n]=event() end
refreshes=0; requests=0; selectedUnit=0; selectedCity=0; openedPolicies=0
ready=true; alive=true; tutorial=false; auto=false; notifyX=10; notifyY=2;notifyOwner=0;dismissed=false
Automation={IsActive=function() return auto end};function IsTutorialRunning() return tutorial end
Players[0].IsAlive=function() return alive end;Players[0].IsTurnActiveComplete=function() return ready end
NotificationManager.FindEndTurnBlocking=function() return {
 GetPlayerID=function() return notifyOwner end,IsDismissed=function() return dismissed end,
 GetLocation=function() return notifyX,notifyY end} end
function control() return {SetText=function(self,v) self.text=v end,SetToolTipString=function(self,v) self.tip=v end,
 SetHide=function(self,v) self.hidden=v end,SetIcon=function(self,v) self.icon=v end} end
Controls={EndTurnText=control(),EndTurnButton=control(),EndTurnButtonLabel=control(),CurrentTurnBlockerIcon=control(),CountImage=control(),OverflowCheckboxGroup=control()}
for i=2,4 do Controls['TurnBlockerAlpha'..i]=control() end
ContextPtr={RequestRefresh=function() refreshes=refreshes+1 end,
 SetRefreshHandler=function(_,f) refreshHandler=f end,SetInputHandler=function(_,f) inputHandler=f end}
function OnRefresh() Controls.EndTurnText:SetText('NATIVE');Controls.CountImage:SetHide(false) end
function OnEndTurnClicked() return DoEndTurn() end
function OnInputHandler(e) originalInput=true;return true end
function OnInputActionTriggered(id) originalAction=id end
Input={GetActionId=function() return 42 end};KeyEvents={KeyUp=1};Keys={VK_RETURN=13}
ActionTypes={ACTION_ENDTURN=99};InterfaceModeTypes={CITY_RANGE_ATTACK=8}
g_kMessageInfo={[2]={Message='研究待办',Icon='SCIENCE',ToolTip='选择研究'}}
UI.RequestAction=function(id,p)
 requests=requests+1;reason=p.REASON
 if reenter then OnEndTurnClicked() end
 if requestError then error('uncertain request') end
end
UI.SelectNextReadyUnit=function() selectedUnit=selectedUnit+1 end
UI.SelectCity=function() selectedCity=selectedCity+1 end
UI.SetInterfaceMode=function() end
LuaEvents.NotificationPanel_GovernmentOpenPolicies=function() openedPolicies=openedPolicies+1 end
PopupDialogInGame={new=function() return {AddTitle=function() end,AddText=function() end,
 AddCancelButton=function(_,_,f) cancelPolicy=f end,AddConfirmButton=function(_,_,f) confirmPolicy=f end,
 Open=function() popupOpened=true end} end}
function key(shift) return {GetMessageType=function() return 1 end,GetKey=function() return 13 end,IsShiftDown=function() return shift end} end
"""
class GateTests(unittest.TestCase):
 def setUp(self):
  self.lua=LuaRuntime(unpack_returned_tuples=True);self.lua.execute(FIXTURE+EXTRA);self.lua.execute(SOURCE)
 def runlua(self,s):self.lua.execute(s)
 def get(self,s):return self.lua.eval(s)
 def arm(self):self.runlua("LuaEvents.SPC_TimedTurnProbe('ARM');refreshHandler()")
 def click(self):self.runlua('OnEndTurnClicked()')
 def test_idle_no_scan(self):
  self.runlua('refreshHandler();OnEndTurnClicked()');self.assertEqual(self.get('reads'),0);self.assertEqual(self.get('baseCalls'),1)
 def test_button_and_one_request(self):
  self.arm();self.assertEqual(self.get('Controls.EndTurnText.text'),'LOC_ACTION_PANEL_NEXT_TURN')
  self.click();self.click();self.runlua('OnInputActionTriggered(42)')
  self.assertEqual(self.get('requests'),1);self.assertEqual(self.get('reason'),'UserForced');self.assertEqual(self.get('baseCalls'),0)
 def test_normal_empty_city_not_exempt(self):
  self.runlua('otherQueue=0;blockers={1,1}');self.arm();self.click()
  self.assertEqual(self.get('Controls.EndTurnText.text'),'NATIVE');self.assertEqual(self.get('requests'),0)
 def test_other_blocker_display_and_navigation(self):
  self.runlua('blockers={1,2}');self.arm();self.assertEqual(self.get('Controls.EndTurnText.text'),'研究待办')
  self.click();self.assertEqual(self.get('lastOptional'),2);self.assertEqual(self.get('requests'),0)
 def test_click_fresh_not_cached(self):
  self.arm();self.runlua('otherQueue=0;blockers={1,1}');self.click();self.assertEqual(self.get('requests'),0)
 def test_unknown_location_stops(self):
  self.runlua('notifyX=nil');self.arm();self.click();self.assertEqual(self.get('requests'),0)
  self.assertIn('原型暂停',self.get('ExposedMembers.SPC_TimedTurnProbeReport'))
 def test_wrong_location_blocks(self):
  self.runlua('notifyX=99');self.arm();self.click();self.assertEqual(self.get('requests'),0)
 def test_independent_unit(self):
  self.runlua('unit=true');self.arm();self.click();self.assertEqual(self.get('selectedUnit'),1);self.assertEqual(self.get('requests'),0)
 def test_ranged_keeps_block(self):
  self.runlua('ranged=true;Players[0].GetCities=function() return {FindID=function() return a end,Members=function() return ipairs(cities) end,GetFirstRangedAttackCity=function() return a end} end')
  self.arm();self.click();self.assertEqual(self.get('selectedCity'),1);self.assertEqual(self.get('requests'),0)
 def test_policy_confirmation(self):
  self.runlua('policy=true');self.arm();self.click();self.assertTrue(self.get('popupOpened'));self.assertEqual(self.get('requests'),0)
  self.runlua('confirmPolicy();confirmPolicy()');self.assertEqual(self.get('requests'),1)
 def test_policy_revalidation(self):
  self.runlua('policy=true');self.arm();self.click();self.runlua('blockers={1,2};confirmPolicy()');self.assertEqual(self.get('requests'),0)
 def test_policy_cancel(self):
  self.runlua('policy=true');self.arm();self.click();self.runlua('cancelPolicy()');self.assertEqual(self.get('openedPolicies'),1);self.assertEqual(self.get('requests'),0)
 def test_stale_popup_token(self):
  self.runlua('policy=true');self.arm();self.click();self.runlua("LuaEvents.SPC_TimedTurnProbe('CLEAR');LuaEvents.SPC_TimedTurnProbe('ARM');confirmPolicy()")
  self.assertEqual(self.get('requests'),0)
 def test_enter_vs_automatic(self):
  self.arm();self.runlua('DoEndTurn()');self.assertEqual(self.get('requests'),0)
  self.runlua('inputHandler(key(false))');self.assertEqual(self.get('requests'),1)
 def test_shift_unchanged(self):
  self.arm();self.runlua('inputHandler(key(true))');self.assertTrue(self.get('originalInput'));self.assertEqual(self.get('requests'),0)
 def test_inflight_reentry_unknown(self):
  self.arm();self.runlua('reenter=true;requestError=true');self.click();self.click();self.runlua("LuaEvents.SPC_TimedTurnProbe('CLEAR');LuaEvents.SPC_TimedTurnProbe('ARM')");self.click()
  self.assertEqual(self.get('requests'),1)
 def test_dirty_coalesced_and_hover_free(self):
  self.arm();before=self.get('reads');self.runlua("refreshHandler();refreshHandler();LuaEvents.SPC_TimedTurnProbe('READ')")
  self.assertEqual(self.get('reads'),before)
  self.runlua('Events.EndTurnDirty();Events.CityProductionChanged();refreshHandler()');self.assertEqual(self.get('reads'),before+1)
 def test_lifecycle_and_save_session(self):
  self.arm();self.click();self.runlua('turn=21;Events.PlayerTurnActivated(0);refreshHandler()')
  self.assertEqual(self.get('Controls.EndTurnText.text'),'NATIVE');self.assertIn('测试结束',self.get('ExposedMembers.SPC_TimedTurnProbeReport'))
  self.click();self.assertEqual(self.get('requests'),1)
  fresh=LuaRuntime();fresh.execute(FIXTURE+EXTRA);fresh.execute(SOURCE);fresh.execute('OnEndTurnClicked()');self.assertEqual(fresh.globals().requests,0)
 def test_gates(self):
  for setting in ['ready=false','alive=false','busy=true','sent=true','unready=true','tutorial=true','auto=true','notifyOwner=5','dismissed=true','blockers={777}','blockers={[1]=1,[3]=1}']:
   self.setUp();self.runlua(setting);self.arm();self.click();self.assertEqual(self.get('requests'),0,setting)
 def test_prod_interrupt_and_player_loss(self):
  self.arm();self.runlua('queue=1');self.click();self.assertEqual(self.get('requests'),0)
  self.setUp();self.arm();self.runlua('human=false');self.click();self.assertEqual(self.get('requests'),0)
 def test_static(self):
  for p in ['Mod/UI/TimedTurnProbe.lua','Mod/UI/P0Panel.lua','Mod/Probe.lua']:self.lua.execute('assert(load(...))',(ROOT/p).read_text())
  doc=ET.parse(ROOT/'Mod/SpecializationP0.modinfo');self.assertEqual(doc.getroot().get('version'),'140')
  self.assertTrue(all((ROOT/'Mod'/n.text).is_file() for n in doc.findall('./Files/File')))
  ui=ET.parse(ROOT/'Mod/UI/P0Panel.xml')
  for name in ['TurnProbeReadCaption','TurnProbeArmCaption']:self.assertIsNotNone(ui.find(".//Label[@ID='"+name+"']"))
  for write in [':SetProperty(',':AddProgress(',':RequestOperation(',':SetUpdate(']:self.assertNotIn(write,SOURCE)
if __name__=='__main__':unittest.main()
