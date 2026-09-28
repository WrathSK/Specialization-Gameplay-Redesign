"""B116 native NONE regression and concise diagnostic checks; inherit B115 protections."""
import unittest
import xml.etree.ElementTree as ET
import test_b115_production_observer as previous
class EmptyTargetTests(previous.ObserverTests):
 def setUp(self):
  super().setUp();self.runlua("gpTarget='NONE'")
 def test_static(self):
  for f in ['Mod/Gameplay.lua','Mod/TimedProductionProbe.lua','Mod/UI/TimedTurnProbe.lua','Mod/Probe.lua']:
   self.lua.execute('assert(load(...))',(previous.prior.ROOT/f).read_text())
  doc=ET.parse(previous.prior.ROOT/'Mod/SpecializationP0.modinfo');self.assertEqual(doc.getroot().get('version'),'143')
  self.assertTrue(all((previous.prior.ROOT/'Mod'/n.text).is_file() for n in doc.findall('./Files/File')))
  for x in ['SetProperty','AddProgress','FinishProgress','RequestOperation','SetUpdate']:self.assertNotIn(x,previous.GP)
 def report(self):
  self.runlua("LuaEvents.SPC_TimedTurnProbe('READ')");return self.get('ExposedMembers.SPC_TimedTurnProbeReport')
 def test_none_start_sample_and_end(self):
  self.arm();self.assertEqual(self.status(),'ACTIVE')
  self.runlua('Events.CityProductionUpdated(0,10);Events.PlayerTurnDeactivated(0)');self.assertEqual(self.status(),'ACTIVE')
  self.runlua('turn=21;GameEvents.PlayerTurnStarted(0)');self.assertEqual(self.status(),'ENDED')
 def test_supported_empty_values(self):
  for value in ['nil',"''","'NONE'"]:
   self.setUp();self.runlua('gpTarget='+value);self.arm();self.assertEqual(self.status(),'ACTIVE')
 def test_not_fuzzy_none(self):
  for value in ["'none'","'NONE_X'",'false','0',"'BUILDING_MONUMENT'"]:
   self.setUp();self.runlua('gpTarget='+value);self.arm();self.click();self.assertEqual(self.status(),'STOPPED');self.assertEqual(self.get('requests'),0)
 def test_empty_queue_does_not_read_stale_hash(self):
  self.arm();self.runlua("a.GetBuildQueue=function() return {GetSize=function() return 0 end,GetCurrentProductionTypeHash=function() error('MUST NOT READ') end} end;GameInfo.Buildings[0]={Name='纪念碑',Index=0}")
  text=self.report();self.assertIn('无生产目标',text);self.assertNotIn('纪念碑',text);self.assertNotIn('MUST NOT READ',text)
 def test_nonempty_real_progress(self):
  self.arm();self.runlua("a.GetBuildQueue=function() return {GetSize=function() return 1 end,GetCurrentProductionTypeHash=function() return 123 end,GetBuildingProgress=function() return 17 end} end;GameInfo.Buildings[123]={Name='纪念碑',Index=0}")
  self.assertIn('纪念碑=17',self.report())
 def test_nonempty_zero_hash_not_monument(self):
  self.arm();self.runlua("queue=1;GameInfo.Buildings[0]={Name='纪念碑',Index=0}")
  text=self.report();self.assertIn('目标hash不可确认',text);self.assertNotIn('纪念碑=',text)
 def test_inline_stack_shortened_and_preserved(self):
  self.runlua("a.GetBuildQueue=function() error('接口失败 stack traceback: secret/path.lua:42') end")
  # Direct Gameplay begin avoids the UI queue precheck, exercises actual error preservation.
  self.runlua("ExposedMembers.SPC_P0.TimedProductionProbe.Request(0,{Action='TIMED_PRODUCTION_BEGIN',Token='err',CityID=10,StartTurn=20})")
  reason=self.get('ExposedMembers.SPC_P0.TimedProduction.reason');detail=self.get('ExposedMembers.SPC_P0.TimedProduction.errorDetail')
  self.assertNotIn('stack traceback',reason);self.assertNotIn('secret/path',reason);self.assertIn('stack traceback',detail)
 def test_error_in_later_sample_short(self):
  self.arm();self.runlua("a.GetBuildQueue=function() error('后续读取失败\\nstack traceback: full detail') end;Events.CityProductionUpdated(0,10)")
  self.assertEqual(self.status(),'STOPPED');self.assertNotIn('stack traceback',self.get('ExposedMembers.SPC_P0.TimedProduction.reason'))
if __name__=='__main__':unittest.main()
