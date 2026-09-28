"""B120 bounded event observation. Simulations are not native event-order proof."""
import unittest
import xml.etree.ElementTree as ET
from lupa.lua55 import LuaRuntime
import test_b119_finish_sink as old
ROOT=old.ROOT
GP=(ROOT/'Mod/ProjectTurnObservation.lua').read_text()
UI=(ROOT/'Mod/UI/ProjectTurnRead.lua').read_text()
class Observer(unittest.TestCase):
 def setUp(self):
  self.lua=LuaRuntime(unpack_returned_tuples=True)
  self.run(old.prev.old.FIXTURE);self.run(old.prev.EXTRA)
  self.run("GameEvents={PlayerTurnStarted=event(),PlayerTurnStartComplete=event()};Events.PlayerTurnActivated=event();Events.PlayerTurnDeactivated=event()")
  self.run(GP);self.run('SPCProjectTurnObservation.Start(P,shared)');self.run(UI)
  self.run("function send(pid,op,p)packets[#packets+1]=p;if not defer then shared.ProjectTurnObservation.Request(pid,p)end end;ui=SPCProjectTurnRead.New(P,function(s)shown=s end,send)")
 def run(self,*args,**kwargs):
  if args and isinstance(args[0],str):return self.lua.execute(args[0])
  return super().run(*args,**kwargs)
 def get(self,s):return self.lua.eval(s)
 def state(self):return self.get('shared.ProjectTurnEvidence.status')
 def test_full_window(self):
  self.run('ui.Begin();Events.PlayerTurnDeactivated(0);turn=21;GameEvents.PlayerTurnStarted(0);pp=16.3;Events.CityProductionUpdated(0,10);Events.PlayerTurnActivated(0);GameEvents.PlayerTurnStartComplete(0)')
  self.assertEqual(self.state(),'ACTIVE');self.run('ui.End()');self.assertEqual(self.state(),'ENDED');self.assertIn('16.3',self.get('shown'));self.assertIn('StartComplete',self.get('shown'));self.assertEqual(self.get('writes'),0)
 def test_alternate_order(self):
  self.run('ui.Begin();turn=21;Events.PlayerTurnActivated(0);GameEvents.PlayerTurnStartComplete(0);pp=17;Events.CityProductionUpdated(0,10);ui.End()');self.assertIn('17',self.get('shown'));self.assertEqual(self.state(),'ENDED')
 def test_duplicates_bounded(self):
  self.run('ui.Begin();for i=1,35 do Events.CityProductionUpdated(0,10)end');self.assertEqual(self.state(),'STOPPED');self.assertEqual(self.get('#shared.ProjectTurnEvidence.rows'),32)
 def test_other_city_player(self):
  self.run('ui.Begin();Events.CityProductionUpdated(0,11);Events.CityProductionUpdated(3,10);GameEvents.PlayerTurnStarted(3)');self.assertEqual(self.get('#shared.ProjectTurnEvidence.rows'),1)
 def test_owner_change(self):
  self.run('ui.Begin();owner=3;Events.CityProductionUpdated(0,10)');self.assertEqual(self.state(),'STOPPED')
 def test_removed(self):
  self.run('ui.Begin();Events.CityRemovedFromMap(0,10)');self.assertEqual(self.state(),'STOPPED')
 def test_unknown_gp(self):
  self.run('ui.Begin();q.CurrentlyBuilding=nil;Events.CityProductionUpdated(0,10)');self.assertEqual(self.state(),'STOPPED')
 def test_missing_ui(self):
  self.run('ui.Begin();ExposedMembers.SPC_ProjectTurnRead=nil;Events.CityProductionUpdated(0,10);ui.Read()');self.assertIn('UI=UNKNOWN',self.get('shown'));self.assertNotIn('UI缓存=0',self.get('shown'))
 def test_early_finish_allowed_observation(self):
  self.run("ui.Begin();target='NONE';size=0;pp=0;Events.CityProductionCompleted(0,10,7);ui.Read()")
  self.assertEqual(self.state(),'ENDED');self.assertNotIn('拒绝',self.get('shown'));self.assertEqual(self.get('writes'),0)
 def test_changed_target_no_resume(self):
  self.run("ui.Begin();target='BUILDING_OLD';Events.CityProductionChanged(0,10);target=project;Events.CityProductionChanged(0,10)");self.assertEqual(self.state(),'ENDED');self.assertEqual(self.get('#shared.ProjectTurnEvidence.rows'),2)
 def test_same_target_events_evidence_not_guess(self):
  self.run('ui.Begin();Events.CityProductionQueueChanged(0,10);ui.Read()');self.assertEqual(self.state(),'ACTIVE');self.assertIn('队列变化',self.get('shown'))
 def test_expiry(self):
  self.run('ui.Begin();turn=22;GameEvents.PlayerTurnStarted(0)');self.assertEqual(self.state(),'STOPPED')
 def test_read_only_not_end(self):
  self.run('ui.Begin();ui.Read();ui.Read()');self.assertEqual(self.state(),'ACTIVE');self.assertEqual(self.get('#packets'),1)
 def test_zero_no_growth_required(self):
  self.run('pp=0;ui.Begin();turn=21;GameEvents.PlayerTurnStarted(0);ui.End()');self.assertEqual(self.state(),'ENDED');self.assertIn('UI缓存=0',self.get('shown'))
 def test_stale_ui_labeled(self):
  self.run('ui.Begin();ExposedMembers.SPC_ProjectTurnRead=function()return {owner=0,id=10,turn=20,value=999,size=1,isProject=true}end;turn=21;GameEvents.PlayerTurnStarted(0);ui.End()');self.assertIn('UI=UNKNOWN',self.get('shown'))
 def test_negative_visible(self):
  self.run('ui.Begin();pp=-8;ui.End()');self.assertIn('UI缓存=-8',self.get('shown'))
 def test_begin_wrong_queue(self):
  for code in ['size=0','size=2',"target='NONE'",'owner=3','selected=false']:
   self.setUp();self.run(code+';ui.Begin()');self.assertEqual(self.get('#packets'),0)
 def test_missing_hook(self):
  self.run('GameEvents.PlayerTurnStartComplete=nil;SPCProjectTurnObservation.Start(P,shared);ui.Begin()');self.assertEqual(self.state(),'STOPPED');self.assertIn('PlayerTurnStartComplete',self.get('shown'))
 def test_reload_resets(self):
  self.run('ui.Begin();SPCProjectTurnObservation.Start(P,shared);ui.Read()');self.assertIsNone(self.get('shared.ProjectTurnEvidence'));self.assertIn('重载',self.get('shown'))
 def test_pending_no_retry(self):
  self.run('defer=true;ui.Begin();ui.Begin();ui.Read()');self.assertEqual(self.get('#packets'),1)
 def test_begin_duplicate(self):
  self.run('ui.Begin();ui.Begin();shared.ProjectTurnObservation.Request(0,packets[1])');self.assertEqual(self.get('#shared.ProjectTurnEvidence.rows'),1)
 def test_bad_end(self):
  self.run("ui.Begin();shared.ProjectTurnObservation.Request(0,{Action='PROJECT_TURN_END',Token='wrong',CityID=10})");self.assertEqual(self.state(),'ACTIVE')
 def test_actual_dispatch(self):
  code=(ROOT/'Mod/Gameplay.lua').read_text().split("  if params.Action=='CITY_SEQUENCE_BEGIN'")[0]
  self.run("include=function()end;SPCP0=P;SPCPerformance={New=function()return {}end};P.Scalar=tostring")
  fn=self.lua.execute(code+'\nend\nreturn request')
  self.run('shared=ExposedMembers.SPC_P0;SPCProjectTurnObservation.Start(P,shared)')
  fn(0,self.lua.table_from(dict(Action='PROJECT_TURN_BEGIN',Token='actual',CityID=10,StartTurn=20)))
  self.assertEqual(self.state(),'ACTIVE')
 def test_actual_panel_buttons(self):
  self.run("include=function()end;Events.GameCoreEventPublishComplete=event();ContextPtr={ClearUpdate=function()end};Mouse={eLClick=1,eRClick=2};UI.RequestPlayerOperation=send;Controls=setmetatable({},{__index=function(t,k)local c={callbacks={},SetText=function()end,SetToolTipString=function()end,RegisterCallback=function(self,k,f)self.callbacks[k]=f end};rawset(t,k,c);return c end})")
  panel=(ROOT/'Mod/UI/P0Panel.lua').read_text();block=panel.split(' include("ProjectTurnRead")')[1].split('\nend\nContextPtr:SetInitHandler')[0]
  self.run('local function status(s)shown=s end;'+block)
  self.run('Controls.PerformanceSnapshotButton.callbacks[1]();turn=21;GameEvents.PlayerTurnStarted(0);Controls.PerformanceReadButton.callbacks[2]()');self.assertEqual(self.state(),'ACTIVE')
  self.run('Controls.PerformanceReadButton.callbacks[1]()');self.assertEqual(self.state(),'ENDED');self.assertEqual(self.get('writes'),0)
 def test_delayed_ack_end(self):
  self.run('defer=true;ui.Begin();shared.ProjectTurnObservation.Request(0,packets[1]);ui.Pulse();turn=21;ui.End();shared.ProjectTurnObservation.Request(0,packets[2]);ui.Pulse()');self.assertEqual(self.state(),'ENDED');self.assertIn('观察结束',self.get('shown'))
class FinishRegression(old.FinishTests):pass
class OldObserverRegression(old.Regression):
 def test_static(self):
  for path in ['Mod/ProjectTurnObservation.lua','Mod/UI/ProjectTurnRead.lua','Mod/UI/P0Panel.lua','Mod/Gameplay.lua','Mod/Probe.lua','Mod/OverflowStorageProbe.lua','Mod/UI/OverflowStorageRead.lua']:
   self.lua.execute('assert(load(...))',(ROOT/path).read_text())
  doc=ET.parse(ROOT/'Mod/SpecializationP0.modinfo');self.assertEqual(doc.getroot().get('version'),'147')
  files=[e.text for e in doc.findall('./Files/File')];self.assertEqual(len(files),len(set(files)));self.assertTrue(all((ROOT/'Mod'/f).is_file() for f in files))
  for text in ['SetProperty','AddProgress','FinishProgress','RequestOperation','SetUpdate']:
   self.assertNotIn(text,GP)
  self.assertNotIn('SetUpdate',UI);self.assertIn('q:FinishProgress()',old.GP);self.assertNotIn('AddProgress',old.GP)
  panel=(ROOT/'Mod/UI/P0Panel.lua').read_text();self.assertIn('开始项目观察',panel);self.assertIn('完成承接试验',panel)
if __name__=='__main__':unittest.main()
