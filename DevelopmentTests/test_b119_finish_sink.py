"""Native FinishProgress experiment: no Cheat Panel dependency; no engine proof."""
import unittest, xml.etree.ElementTree as ET
from lupa.lua55 import LuaRuntime
import test_b118_exact_progress as prev
ROOT=prev.ROOT
GP=(ROOT/'Mod/OverflowStorageProbe.lua').read_text(); UI=(ROOT/'Mod/UI/OverflowStorageRead.lua').read_text()
EXTRA=r'''
GameInfo.Buildings[1].Hash=9
q.FinishProgress=function()writes=writes+1;if fail then error('native exception')end
 if mode=='late' then return end
 pp=0;target='NONE';size=0
 if mode=='leak' then pool=500 end
end
'''
class FinishTests(unittest.TestCase):
 def setUp(self):
  self.lua=LuaRuntime(unpack_returned_tuples=True);self.runlua(prev.old.FIXTURE);self.runlua(prev.EXTRA);self.runlua(EXTRA);self.runlua(GP);self.runlua('SPCOverflowStorageProbe.Start(P,shared)');self.runlua(UI);self.runlua('ui=SPCOverflowStorageRead.New(P,function(s)shown=s end,send)')
 def runlua(self,s):return self.lua.execute(s)
 def get(self,s):return self.lua.eval(s)
 def test_finish_once(self):
  self.runlua('ui.Click();ui.Click();ui.Click();ui.Read()');self.assertEqual(self.get('writes'),1);self.assertEqual(self.get('sum'),0);self.assertEqual(self.get('size'),0);self.assertIn('无生产目标',self.get('shown'));self.assertIn('保留进度=0',self.get('shown'))
 def test_zero_can_finish(self):
  self.runlua('pp=0;ui.Click();ui.Click()');self.assertEqual(self.get('writes'),1)
 def test_invalid_values(self):
  for v in ['-1','10001','0/0','math.huge']:
   self.setUp();self.runlua('pp='+v+';ui.Click()');self.assertEqual(self.get('writes'),0)
 def test_zero_next_target_explicit(self):
  self.runlua("ui.Click();ui.Click();target='BUILDING_OLD';size=1;progress=0;ui.Read()");self.assertIn('old building｜进度=0',self.get('shown'))
  self.runlua('progress=8;turn=21;ui.Read()');self.assertIn('old building｜进度=8',self.get('shown'));self.assertIn('回合21',self.get('shown'))
 def test_unchanged_not_omitted(self):
  self.runlua("mode='late';ui.Click();ui.Click();ui.Read()");self.assertIn('test project｜进度=8',self.get('shown'))
  self.runlua("pp=0;size=0;target='NONE';ui.Read()");self.assertIn('保留进度=0',self.get('shown'));self.assertNotIn('7→7',self.get('shown'))
 def test_no_native_pass_for_leak(self):
  self.runlua("mode='leak';ui.Click();ui.Click();ui.Read()");self.assertEqual(self.get('shared.OverflowStorage.status'),'CALLED_NOT_PROVEN');self.assertNotIn('USER_GAME_TEST_PASS',self.get('shown'))
 def test_negative_visible(self):
  self.runlua("ui.Click();ui.Click();target='BUILDING_OLD';size=1;progress=-8;ui.Read()");self.assertIn('进度=-8',self.get('shown'))
 def test_missing_finish_no_write(self):
  self.runlua('q.FinishProgress=nil;ui.Click();ui.Click()');self.assertEqual(self.get('writes'),0)
 def test_unknown_target_not_zero(self):
  self.runlua('q.GetCurrentProductionTypeHash=function()return 888 end;ui.Read()');self.assertIn('当前读数不可确认',self.get('shown'))
 def test_no_cheat_needed(self):
  self.runlua('CheatPanel=nil;CompleteProduction=nil;ui.Click();ui.Click()');self.assertEqual(self.get('writes'),1)
 def test_actual_panel(self):
  self.runlua('SPCP0=P;include=function()end;SPCCityIdentityEvidence={New=function()return {}end};Events.GameCoreEventPublishComplete=prevEvent or event();Controls={Status={SetText=function(_,s)shown=s end}};UI.RequestPlayerOperation=send')
  panel=self.lua.execute((ROOT/'Mod/UI/P0Panel.lua').read_text().split('local function trace(s)')[0]+'\nreturn overflowRead');panel.Click();self.assertIn('不是扣生产力',self.get('shown'));panel.Click();panel.Read();self.assertIn('无生产目标',self.get('shown'))
# Preserve directly relevant guards, using this fixture and actual current code.
for name in ['test_prepare_no_write','test_wrong_target_queue','test_changed_progress','test_changed_other_progress','test_guard_changes','test_event_invalidates_even_back','test_unrelated_event','test_no_prepare_or_bad_token','test_missing_reader','test_delayed_request_rechecks_progress','test_native_error_no_retry','test_ui_wait_no_retry','test_reader_survives_gameplay_shared_replacement','test_missing_project','test_dispatch']:
 setattr(FinishTests,name,getattr(prev.ExactTests,name))
class Regression(prev.old.prior.EmptyTargetTests):
 def test_static(self):
  for f in ['Mod/OverflowStorageProbe.lua','Mod/UI/OverflowStorageRead.lua','Mod/UI/P0Panel.lua','Mod/Gameplay.lua','Mod/Probe.lua']:
   self.lua.execute('assert(load(...))',(ROOT/f).read_text())
  doc=ET.parse(ROOT/'Mod/SpecializationP0.modinfo');self.assertEqual(doc.getroot().get('version'),'146');files=[n.text for n in doc.findall('./Files/File')];self.assertEqual(len(files),len(set(files)));self.assertTrue(all((ROOT/'Mod'/f).is_file() for f in files))
  self.assertNotIn('AddProgress',GP);self.assertIn('q:FinishProgress()',GP);self.assertNotIn('SetUpdate',UI)
  panel=(ROOT/'Mod/UI/P0Panel.lua').read_text();self.assertIn('完成承接试验',panel);self.assertNotIn('再次左键调用−1000',panel);self.assertNotIn('再次左键只扣',UI)
if __name__=='__main__':unittest.main()
