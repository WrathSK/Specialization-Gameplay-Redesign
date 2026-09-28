"""Actual B112 Lua with native API fixtures; not Civ VI engine confirmation."""
from pathlib import Path
import unittest
import xml.etree.ElementTree as ET
from lupa.lua55 import LuaRuntime
ROOT = Path(__file__).resolve().parents[1]
SOURCE = (ROOT / "Mod/UI/TimedTurnProbe.lua").read_text()
FIXTURE = r"""
function event()
 local list={}
 return setmetatable({Add=function(f) list[#list+1]=f end},
 {__call=function(_,...) for _,f in ipairs(list) do f(...) end end})
end
LuaEvents={SPC_TimedTurnProbe=event()};Events={PlayerTurnActivated=event()}
ExposedMembers={}; baseCalls=0; reads=0; turn=20; pid=0; queue=0; otherQueue=1
unit=false; ranged=false; policy=false; busy=false; sent=false; unready=false; first=1
blockers={1}; human=true; civicChanged=false
function include(name) end
function DoEndTurn(x) baseCalls=baseCalls+1; lastOptional=x; return 'BASE' end
SPCP0={IsTestPlayer=function() return human end}
Game={GetLocalPlayer=function() return pid end, GetCurrentGameTurn=function() return turn end}
function city(id,q)
 return {GetID=function() return id end,GetOwner=function() return 0 end,
 GetX=function() return id end,GetY=function() return 2 end,GetName=function() return 'City'..id end,
 GetBuildQueue=function() return {GetSize=q} end}
end
a=city(10,function() return queue end); b=city(11,function() return otherQueue end)
cities={a,b}
Players={[0]={GetCities=function() return {
 FindID=function(_,id) for _,c in ipairs(cities) do if c:GetID()==id then return c end end end,
 Members=function() return ipairs(cities) end} end,
 CanUnreadyTurn=function() return unready end,
 GetCulture=function() return {CivicCompletedThisTurn=function() return true end,
 PolicyChangeMade=function() return civicChanged end,GetCivicCompletedThisTurn=function() return 1 end} end}}
UI={GetHeadSelectedCity=function() return a end,IsProcessingMessages=function() return busy end,
 HasSentTurnComplete=function() return sent end,
 RequestAction=function() error('FORBIDDEN request') end}
NotificationManager={GetAllEndTurnBlocking=function() reads=reads+1;return blockers end,
 GetFirstEndTurnBlocking=function() return first end}
EndTurnBlockingTypes={ENDTURN_BLOCKING_PRODUCTION=1,ENDTURN_BLOCKING_RESEARCH=2}
Locale={Lookup=function(s) return s end};Modding={IsModActive=function() return policy end}
GameInfo={Civics={[1]={CivicType='CIVIC_TEST'}}}
function CheckUnitsHaveMovesState() return unit end
function CheckCityRangeAttackState() return ranged end
function print() end
"""

class ProbeTests(unittest.TestCase):
 def setUp(self):
  self.lua=LuaRuntime(unpack_returned_tuples=True)
  self.lua.execute(FIXTURE);self.lua.execute(SOURCE)
 def runlua(self, code): self.lua.execute(code)
 def report(self): return self.lua.globals().ExposedMembers.SPC_TimedTurnProbeReport
 def arm(self): self.runlua("LuaEvents.SPC_TimedTurnProbe('ARM')")
 def click(self): self.assertEqual(self.lua.eval("DoEndTurn(nil)"),'BASE')
 def test_idle_delegates_without_scan(self):
  self.click();self.assertEqual(self.lua.globals().reads,0);self.assertEqual(self.lua.globals().baseCalls,1)
 def test_candidate_is_only_observation(self):
  self.arm();self.click();self.assertIn('候选条件满足',self.report());self.assertEqual(self.lua.globals().baseCalls,1)
 def test_nonproduction_and_retry(self):
  self.arm();self.runlua('blockers={1,2}');self.click();self.assertIn('候选条件未满足',self.report())
  self.runlua('blockers={1}');self.click();self.assertIn('候选条件满足',self.report())
 def test_other_empty_city(self):
  self.arm();self.runlua('otherQueue=0');self.click();self.assertIn('其它空城=1',self.report());self.assertIn('未满足',self.report())
 def test_independent_checks(self):
  for flag in ['unit','ranged','policy','busy','sent','unready']:
   self.runlua(flag+'=true');self.arm();self.click();self.assertIn('未满足',self.report(),flag);self.runlua(flag+'=false')
 def test_unknown_read_pauses_but_delegates(self):
  self.arm();self.runlua('blockers=false');self.click();self.assertIn('原型暂停',self.report())
  before=self.lua.globals().reads;self.click();self.assertEqual(self.lua.globals().reads,before)
 def test_production_change_disarms(self):
  self.arm();self.runlua('queue=1');self.click();self.assertIn('已开始生产',self.report());self.assertEqual(self.lua.globals().reads,0)
 def test_turn_clear_and_cached_read(self):
  self.arm();self.click();before=self.lua.globals().reads
  self.runlua("LuaEvents.SPC_TimedTurnProbe('READ');turn=21;Events.PlayerTurnActivated(0)")
  self.click();self.assertEqual(self.lua.globals().reads,before);self.assertIn('已关闭',self.report())
 def test_missing_city_and_scope(self):
  self.arm();self.runlua('cities={b}');self.click();self.assertIn('观察城已失效',self.report())
  self.runlua('human=false');self.arm();self.assertIn('未开始观察',self.report())
 def test_cancel_and_reload_unarmed(self):
  self.arm();self.runlua("LuaEvents.SPC_TimedTurnProbe('CLEAR')");self.click();self.assertEqual(self.lua.globals().reads,0)
  fresh=LuaRuntime();fresh.execute(FIXTURE);fresh.execute(SOURCE);fresh.execute('DoEndTurn(nil)')
  self.assertEqual(fresh.globals().reads,0)
 def test_explicit_navigation_preserved(self):
  self.arm();self.runlua('DoEndTurn(1)');self.assertEqual(self.lua.globals().lastOptional,1);self.assertIn('未满足',self.report())
 def test_sparse_unknown_and_bounded_city_list(self):
  self.arm();self.runlua('blockers={[1]=1,[3]=1}');self.click();self.assertIn('原型暂停',self.report())
  self.runlua('blockers={777}');self.arm();self.click();self.assertIn('UNKNOWN(777)',self.report());self.assertIn('未满足',self.report())
  self.runlua('cities={};for i=1,129 do cities[i]=a end');self.arm();self.click();self.assertIn('上限128',self.report())
 def test_manifest_ui_and_no_write_surface(self):
  doc=ET.parse(ROOT/'Mod/SpecializationP0.modinfo');top=doc.getroot()
  self.assertEqual(top.attrib['version'],'139')
  files=[n.text for n in top.findall('./Files/File')]
  self.assertEqual(files.count('UI/TimedTurnProbe.lua'),1)
  self.assertTrue(all((ROOT/'Mod'/p).is_file() for p in files))
  hook=top.find("./InGameActions/ReplaceUIScript[@id='SPC_TimedTurnProbe']")
  self.assertEqual(hook.findtext('./Properties/LuaContext'),'ActionPanel')
  ET.parse(ROOT/'Mod/UI/P0Panel.xml')
  for forbidden in ['UI.RequestAction(',':SetProperty(',':AddProgress(',':SetUpdate(',':RequestOperation(']:
   self.assertNotIn(forbidden,SOURCE)
  # Syntax only for touched UI/common Lua; mocked execution above covers the actual observer.
  for p in ['Mod/UI/P0Panel.lua','Mod/Probe.lua']:
   self.lua.execute('assert(load(...))',(ROOT/p).read_text())

if __name__=='__main__': unittest.main()
