"""B114 target-object contract. Inherit B113 protections; supersede only location/version assertions."""
import unittest
import xml.etree.ElementTree as ET
import test_b113_turn_gate as prior
from lupa.lua55 import LuaRuntime
TARGET=r'''
targetValid=true;targetOwner=0;targetID=10;targetType=7;targetReads=0
PlayerComponentTypes={CITY=7,UNIT=8}
NotificationManager.FindEndTurnBlocking=function() return {
 GetPlayerID=function() return notifyOwner end,IsDismissed=function() return dismissed end,
 IsTargetValid=function() return targetValid end,
 GetTarget=function() targetReads=targetReads+1;return targetOwner,targetID,targetType end,
 GetLocation=function() error('Camera location must not determine target identity') end} end
'''
class TargetTests(prior.GateTests):
 def setUp(self):
  self.lua=LuaRuntime(unpack_returned_tuples=True)
  self.lua.execute(prior.FIXTURE+prior.EXTRA+TARGET);self.lua.execute(prior.SOURCE)
 def test_unknown_location_stops(self):
  # Supersedes B113: unavailable camera coordinates do not invalidate a valid CITY target.
  self.runlua('notifyX=nil');self.arm();self.click();self.assertEqual(self.get('requests'),1)
 def test_wrong_location_blocks(self):
  # Supersedes B113: camera location and target object serve separate native purposes.
  self.runlua('notifyX=99');self.arm();self.click();self.assertEqual(self.get('requests'),1)
 def test_static(self):
  for p in ['Mod/UI/TimedTurnProbe.lua','Mod/UI/P0Panel.lua','Mod/Probe.lua']:
   self.lua.execute('assert(load(...))',(prior.ROOT/p).read_text())
  doc=ET.parse(prior.ROOT/'Mod/SpecializationP0.modinfo');self.assertEqual(doc.getroot().get('version'),'141')
  self.assertTrue(all((prior.ROOT/'Mod'/n.text).is_file() for n in doc.findall('./Files/File')))
  ui=ET.parse(prior.ROOT/'Mod/UI/P0Panel.xml')
  for name in ['TurnProbeReadCaption','TurnProbeArmCaption']:self.assertIsNotNone(ui.find(".//Label[@ID='"+name+"']"))
  for write in [':SetProperty(',':AddProgress(',':RequestOperation(',':SetUpdate(']:self.assertNotIn(write,prior.SOURCE)
 def test_invalid_target_not_read(self):
  self.runlua('targetValid=false');self.arm();self.click()
  self.assertEqual(self.get('requests'),0);self.assertEqual(self.get('targetReads'),0)
  self.assertIn('目标有效=false',self.get('ExposedMembers.SPC_TimedTurnProbeReport'))
 def test_wrong_target(self):
  for setting in ['targetOwner=3','targetID=11','targetType=8']:
   self.setUp();self.runlua(setting);self.arm();self.click();self.assertEqual(self.get('requests'),0)
   self.assertIn('未放行：通知目标未匹配测试城',self.get('ExposedMembers.SPC_TimedTurnProbeReport'))
 def test_unknown_target_fails_closed(self):
  for setting in ['targetValid=nil','targetID=nil','targetOwner=nil','targetType=nil','PlayerComponentTypes=nil','PlayerComponentTypes.CITY=nil',
   'NotificationManager.FindEndTurnBlocking=function() return {GetPlayerID=function() return 0 end,IsDismissed=function() return false end} end']:
   self.setUp();self.runlua(setting);self.arm();self.click();self.assertEqual(self.get('requests'),0)
   self.assertIn('原型暂停',self.get('ExposedMembers.SPC_TimedTurnProbeReport'))
 def test_target_rechecked_on_click(self):
  self.arm();self.runlua('targetID=11');self.click();self.assertEqual(self.get('requests'),0)
 def test_target_rechecked_after_policy(self):
  self.runlua('policy=true');self.arm();self.click();self.runlua('targetID=11;confirmPolicy()');self.assertEqual(self.get('requests'),0)
 def test_city_disappears(self):
  self.arm();self.runlua('cities={b}');self.click();self.assertEqual(self.get('requests'),0)
 def test_operable_reason(self):
  self.runlua('busy=true');self.arm();self.assertIn('引擎处理消息中',self.get('ExposedMembers.SPC_TimedTurnProbeReport'))
if __name__=='__main__':unittest.main()
