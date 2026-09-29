"""Targeted B123 queue publication/reload regression; not native ordering proof."""
import unittest
import xml.etree.ElementTree as ET
import test_b122_project_selection_display as previous
ROOT=previous.ROOT
class Selection(previous.Selection):
 def test_transient_zero_then_one(self):
  self.runlua('selection.Before(c,item);target=project;size=0;selection.Pulse()')
  self.assertEqual(self.get('#packets'),0)
  self.assertEqual(self.get('ExposedMembers.SPC_TimedProjectSelection.status'),'PENDING')
  self.assertIn('数量=0',self.get('ExposedMembers.SPC_TimedProjectSelection.reason'))
  self.runlua('size=1;selection.Pulse();selection.Pulse()')
  self.assertEqual(self.state(),'ACTIVE');self.assertEqual(self.get('#packets'),1)
  self.cycle();self.assertEqual(self.get('writes'),1)
 def test_zero_never_admitted_and_expires(self):
  self.runlua('selection.Before(c,item);target=project;size=0;for i=1,10 do selection.Pulse() end;turn=21;selection.Pulse()')
  self.assertEqual(self.get('#packets'),0);self.assertIsNone(self.get('shared.TimedProjectState'))
  self.assertEqual(self.get('ExposedMembers.SPC_TimedProjectSelection.status'),'ERROR')
  self.assertIn('数量=0',self.get('ExposedMembers.SPC_TimedProjectSelection.reason'))
 def test_bad_reader_then_recovers(self):
  self.runlua('reader=ExposedMembers.SPC_ProjectTurnRead;selection.Before(c,item);target=project;ExposedMembers.SPC_ProjectTurnRead=function()return nil end;selection.Pulse()')
  self.assertEqual(self.get('#packets'),0)
  self.runlua('ExposedMembers.SPC_ProjectTurnRead=reader;selection.Pulse()');self.assertEqual(self.state(),'ACTIVE')
 def test_transient_to_multiple_is_rejected(self):
  self.runlua('selection.Before(c,item);target=project;size=0;selection.Pulse();size=2;selection.Pulse();size=1;selection.Pulse()')
  self.assertEqual(self.get('#packets'),0);self.assertIn('数量=2',self.get('ExposedMembers.SPC_TimedProjectSelection.reason'))
 def test_normal_selection_cancels_unsent_click(self):
  self.runlua("selection.Before(c,item);target=project;size=0;selection.Pulse();selection.Before(c,{Type='BUILDING_OTHER'});size=1;selection.Pulse()")
  self.assertEqual(self.get('#packets'),0)
 def test_fresh_ui_clears_error_without_start(self):
  self.runlua('selection.Before(c,item);target=project;size=2;selection.Pulse();selection=SPCTimedProjectSelection.New(P,send,function()end);size=1;selection.Pulse()')
  self.assertIsNone(self.get('ExposedMembers.SPC_TimedProjectSelection'));self.assertEqual(self.get('#packets'),0)
 def test_fresh_ui_preserves_gameplay_timer(self):
  self.choose();self.runlua('selection=SPCTimedProjectSelection.New(P,send,function()end);selection.Pulse()')
  self.assertEqual(self.state(),'ACTIVE');self.assertEqual(self.get('#packets'),1)
 def test_owner_mismatch_not_admitted(self):
  self.runlua('selection.Before(c,item);target=project;owner=3;selection.Pulse()');self.assertEqual(self.get('#packets'),0)
 def test_pending_read_and_changed_only_notification(self):
  self.runlua('selection.Before(c,item);target=project;size=0;selection.Pulse();ui.Read();n=notifications;selection.Pulse()')
  self.assertIn('数量=0',self.get('shown'));self.assertEqual(self.get('notifications'),self.get('n'))
class Regression(previous.TimerRegression):
 def test_static_and_manifest(self):
  names=['TimedProject.lua','UI/TimedProjectSelection.lua','UI/TimedProjectDisplay.lua','UI/TimedProjectRead.lua','UI/CityBannerManager_SPC_TimedProject.lua','UI/TimedProjectCityPanel.lua','UI/CrewProjectOrder.lua','UI/P0Panel.lua']
  for name in names:self.lua.execute('assert(load(...))',(ROOT/'Mod'/name).read_text())
  tree=ET.parse(ROOT/'Mod/SpecializationP0.modinfo');self.assertEqual(tree.getroot().get('version'),'150')
  for parent in [tree.find('./Files'),tree.find("./InGameActions/ImportFiles[@id='SPCP0_Common']")]:
   files=[x.text for x in parent.findall('File')];self.assertEqual(len(files),len(set(files)));self.assertTrue(all((ROOT/'Mod'/p).exists() for p in files))
  s=(ROOT/'Mod/UI/TimedProjectSelection.lua').read_text();self.assertNotIn('SetUpdate',s);self.assertNotIn('FinishProgress',s)
class FinishRegression(previous.FinishRegression):pass
class ObserverRegression(previous.ObserverRegression):pass
if __name__=='__main__':unittest.main()
