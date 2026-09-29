"""L3 bounded native-timing prototype. Mocks do not establish engine settlement/overflow."""
import unittest, xml.etree.ElementTree as ET
from lupa.lua55 import LuaRuntime
import test_b120_project_turn_observer as previous
ROOT=previous.ROOT
class Timer(unittest.TestCase):
 def setUp(self):
  self.lua=LuaRuntime(unpack_returned_tuples=True)
  self.runlua(previous.old.prev.old.FIXTURE);self.runlua(previous.old.prev.EXTRA);self.runlua(previous.old.EXTRA)
  self.runlua("Events.PlayerTurnActivated=event();Events.PlayerTurnDeactivated=event();Events.GameCoreEventPublishComplete=event();GameEvents={PlayerTurnStarted=event(),PlayerTurnStartComplete=event()}")
  for f in ['Mod/TimedProject.lua','Mod/UI/ProjectTurnRead.lua','Mod/UI/TimedProjectRead.lua','Mod/UI/TimedProjectDisplay.lua']:
   self.runlua((ROOT/f).read_text())
  self.runlua("SPCTimedProject.Start(P,shared);SPCProjectTurnRead.New(P,function()end,function()end);function send(pid,op,p)packets[#packets+1]=p;if not defer then shared.TimedProject.Request(pid,p)end end;ui=SPCTimedProjectRead.New(P,function(s)shown=s end,send)")
 def runlua(self,s):return self.lua.execute(s)
 def get(self,s):return self.lua.eval(s)
 def state(self):return self.get('shared.TimedProjectState.status')
 def cycle(self):self.runlua('Events.PlayerTurnDeactivated(0);turn=21;Events.PlayerTurnActivated(0)')
 def test_normal_b120_sequence(self):
  self.runlua('ui.Begin();Events.PlayerTurnDeactivated(0);turn=21;GameEvents.PlayerTurnStarted(0);GameEvents.PlayerTurnStartComplete(0);pp=15;Events.CityProductionUpdated(0,10)')
  self.assertEqual(self.get('writes'),0);self.runlua('Events.PlayerTurnActivated(0);ui.Read()');self.assertEqual(self.state(),'COMPLETED');self.assertEqual(self.get('writes'),1);self.assertEqual(self.get('pp'),0);self.assertEqual(self.get('progress'),17)
 def test_zero_no_production_notification(self):
  self.runlua('pp=0;ui.Begin()');self.cycle();self.assertEqual(self.state(),'COMPLETED')
 def test_large_no_manual_cap(self):
  self.runlua('pp=300000;ui.Begin()');self.cycle();self.assertEqual(self.get('writes'),1)
 def test_ui_unavailable_after_admission(self):
  self.runlua('ui.Begin();ExposedMembers.SPC_ProjectTurnRead=nil');self.cycle();self.assertEqual(self.get('writes'),1)
 def test_same_turn_duplicate(self):
  self.runlua('ui.Begin();Events.PlayerTurnActivated(0)');self.assertEqual(self.state(),'ACTIVE');self.assertEqual(self.get('writes'),0)
 def test_duplicate_activation(self):
  self.runlua('ui.Begin()');self.cycle();self.runlua('Events.PlayerTurnActivated(0);Events.GameCoreEventPublishComplete();ui.Begin()');self.assertEqual(self.get('writes'),1)
 def test_reentrant_native_notifications(self):
  self.runlua("q.FinishProgress=function()writes=writes+1;Events.CityProductionQueueChanged(0,10);Events.PlayerTurnActivated(0);target='NONE';size=0;Events.CityProductionCompleted(0,10)end;ui.Begin()")
  self.cycle();self.assertEqual(self.state(),'COMPLETED');self.assertEqual(self.get('writes'),1)
 def test_missing_deactivated(self):
  self.runlua('ui.Begin();turn=21;Events.PlayerTurnActivated(0)');self.assertEqual(self.state(),'STOPPED');self.assertEqual(self.get('writes'),0)
 def test_late_activation(self):
  self.runlua('ui.Begin();Events.PlayerTurnDeactivated(0);turn=22;Events.PlayerTurnActivated(0)');self.assertEqual(self.state(),'STOPPED');self.assertEqual(self.get('writes'),0)
 def test_owner_position_wrong_target(self):
  for code in ['owner=3','x=99',"target='BUILDING_OLD'",'q.CurrentlyBuilding=nil','size=2']:
   self.setUp();self.runlua('ui.Begin();Events.PlayerTurnDeactivated(0);turn=21;'+code+';Events.PlayerTurnActivated(0)');self.assertEqual(self.state(),'STOPPED');self.assertEqual(self.get('writes'),0)
 def test_target_out_and_back(self):
  self.runlua("ui.Begin();target='BUILDING_OLD';Events.CityProductionChanged(0,10);target=project");self.cycle();self.assertEqual(self.get('writes'),0)
 def test_same_target_queue_mutation(self):
  self.runlua('ui.Begin();Events.CityProductionQueueChanged(0,10)');self.cycle();self.assertEqual(self.state(),'STOPPED');self.assertEqual(self.get('writes'),0)
 def test_progress_only_not_cancel(self):
  self.runlua('ui.Begin();pp=400;Events.CityProductionUpdated(0,10)');self.cycle();self.assertEqual(self.get('writes'),1)
 def test_other_city_and_player(self):
  self.runlua('ui.Begin();Events.CityProductionChanged(0,11);Events.CityProductionQueueChanged(3,10);Events.CityRemovedFromMap(3,10);Events.PlayerTurnActivated(3)');self.cycle();self.assertEqual(self.get('writes'),1)
 def test_removed_city(self):
  self.runlua('ui.Begin();Events.CityRemovedFromMap(0,10)');self.cycle();self.assertEqual(self.get('writes'),0)
 def test_early_cheat(self):
  self.runlua("ui.Begin();target='NONE';size=0;Events.CityProductionCompleted(0,10)");self.assertEqual(self.state(),'EARLY_END');self.cycle();self.assertEqual(self.get('writes'),0)
 def test_native_exception_never_retry(self):
  self.runlua('fail=true;ui.Begin()');self.cycle();self.runlua('fail=false;Events.PlayerTurnActivated(0);ui.Begin()');self.assertEqual(self.get('writes'),1);self.assertEqual(self.state(),'STOPPED')
 def test_late_target_exit_confirms_without_second_write(self):
  self.runlua("mode='late';ui.Begin()");self.cycle();self.assertEqual(self.state(),'CONFIRMING')
  self.runlua("Events.PlayerTurnActivated(0);target='NONE';Events.GameCoreEventPublishComplete()");self.assertEqual(self.state(),'COMPLETED');self.assertEqual(self.get('writes'),1)
 def test_unconfirmed_expires_without_retry(self):
  self.runlua("mode='late';ui.Begin()");self.cycle();self.runlua('turn=22;Events.PlayerTurnActivated(0)');self.assertEqual(self.state(),'STOPPED');self.assertEqual(self.get('writes'),1)
 def test_nil_empty_target_native(self):
  self.runlua('q.FinishProgress=function()writes=writes+1;target=nil;size=0 end;ui.Begin()');self.cycle();self.assertEqual(self.state(),'COMPLETED')
 def test_reload_no_resume(self):
  # A fresh Gameplay context has fresh listeners and no persisted timer.
  self.runlua('ui.Begin()');self.setUp();self.runlua('turn=21;Events.PlayerTurnActivated(0);ui.Read()');self.assertIsNone(self.get('shared.TimedProjectState'));self.assertEqual(self.get('writes'),0);self.assertIn('未开启',self.get('shown'))
 def test_admission_and_missing_event(self):
  for code in ['size=2','owner=3',"target='BUILDING_OLD'",'q.FinishProgress=nil']:
   self.setUp();self.runlua(code+';ui.Begin()');self.assertEqual(self.get('writes'),0);self.assertNotEqual(self.get('shared.TimedProjectState and shared.TimedProjectState.status'),'ACTIVE')
  self.setUp();self.runlua('Events.PlayerTurnDeactivated=nil;SPCTimedProject.Start(P,shared);ui.Begin()');self.assertEqual(self.state(),'STOPPED')
 def test_manual_exclusion(self):
  self.runlua(previous.old.GP);self.runlua('SPCOverflowStorageProbe.Start(P,shared);ui.Begin();prep()');self.assertEqual(self.get('shared.OverflowStorage.status'),'REJECTED');self.assertEqual(self.get('writes'),0)
 def test_manual_pending_before_timer_excluded(self):
  self.runlua(previous.old.GP);self.runlua(previous.old.UI);self.runlua('SPCOverflowStorageProbe.Start(P,shared);SPCOverflowStorageRead.New(P,function()end,function()end);prep();ui.Begin();apply()');self.assertEqual(self.get('writes'),0);self.assertEqual(self.state(),'ACTIVE')
 def test_pending_ui_no_repeat(self):
  self.runlua('defer=true;ui.Begin();ui.Begin();ui.Read()');self.assertEqual(self.get('#packets'),1)
 def test_cancel_scoped(self):
  self.runlua("ui.Begin();shared.TimedProject.Request(0,{Action='TIMED_PROJECT_CANCEL',CityID=11,Token=packets[1].Token})");self.assertEqual(self.state(),'ACTIVE');self.runlua('ui.Cancel()');self.cycle();self.assertEqual(self.get('writes'),0)
 def test_actual_dispatch(self):
  code=(ROOT/'Mod/Gameplay.lua').read_text().split("  if params.Action=='CITY_SEQUENCE_BEGIN'")[0]
  self.runlua('include=function()end;SPCP0=P;SPCPerformance={New=function()return {}end};P.Scalar=tostring')
  fn=self.lua.execute(code+'\nend\nreturn request');self.runlua('shared=ExposedMembers.SPC_P0;SPCTimedProject.Start(P,shared)')
  fn(0,self.lua.table_from(dict(Action='TIMED_PROJECT_BEGIN',Token='actual',CityID=10,StartTurn=20)));self.assertEqual(self.state(),'ACTIVE')
 def test_actual_buttons(self):
  self.runlua("include=function()end;ContextPtr={ClearUpdate=function()end};Mouse={eLClick=1,eRClick=2};UI.RequestPlayerOperation=send;Controls=setmetatable({},{__index=function(t,k)local c={callbacks={},SetText=function()end,SetToolTipString=function()end,RegisterCallback=function(self,k,f)self.callbacks[k]=f end};rawset(t,k,c);return c end})")
  panel=(ROOT/'Mod/UI/P0Panel.lua').read_text();block=panel.split(' include("ProjectTurnRead")')[1].split('\nend\nContextPtr:SetInitHandler')[0]
  self.runlua('local function status(s)shown=s end;'+block);self.runlua('Controls.PerformanceSnapshotButton.callbacks[1]()');self.assertEqual(self.state(),'ACTIVE');self.cycle();self.runlua('Controls.PerformanceReadButton.callbacks[1]()');self.assertIn('项目已退出',self.get('shown'))
 def test_display_exact_only_and_crew_sort(self):
  self.runlua("include=function()end;RefreshCurrentProduction=function()return 'native' end;data={Owner=0,City=c,ProjectItems={{Type='PROJECT_OTHER',TurnsLeft=77},{Type='PROJECT_SPC_CREW_750'},{Type=project,TurnsLeft=90000,Cost=1000000},{Type='PROJECT_SPC_CREW_250'}}};GetDataHelper=function()return data end")
  self.runlua((ROOT/'Mod/UI/CrewProjectOrder.lua').read_text());self.runlua('out=GetDataHelper()');self.assertEqual(self.get('out.ProjectItems[1].TurnsLeft'),77);self.assertEqual(self.get('out.ProjectItems[2].Type'),'PROJECT_SPC_CREW_250');self.assertEqual(self.get('out.ProjectItems[4].TurnsLeft'),'开启后1');self.assertEqual(self.get('out.ProjectItems[4].Cost'),1000000)
  self.runlua('ui.Begin();out=GetDataHelper()');self.assertEqual(self.get('out.ProjectItems[4].TurnsLeft'),'1')
 def test_display_without_crew_and_current_row(self):
  self.runlua("include=function()end;RefreshCurrentProduction=function()return true end;data={Owner=0,City=c,ProjectItems={{Type=project,TurnsLeft=999}}};GetDataHelper=function()return data end;parent=setmetatable({},{__index=function(t,k)local v={SetText=function(_,s)text=s end,SetPercent=function()end,SetShadowPercent=function()end,SetToolTipString=function()end};rawset(t,k,v);return v end})")
  self.runlua((ROOT/'Mod/UI/CrewProjectOrder.lua').read_text());self.runlua('out=GetDataHelper();ui.Begin();RefreshCurrentProduction(parent,0,10)');self.assertEqual(self.get('out.ProjectItems[1].TurnsLeft'),'开启后1');self.assertIn('计时已开启：1回合',self.get('text'))
  self.runlua("target='BUILDING_OLD';text='ordinary';RefreshCurrentProduction(parent,0,10)");self.assertEqual(self.get('text'),'ordinary')
 def test_manual_guard_is_city_scoped(self):
  self.runlua('ui.Begin()');self.assertTrue(self.get('shared.TimedProject.BlocksManual(0,10)'));self.assertFalse(bool(self.get('shared.TimedProject.BlocksManual(0,11)')));self.assertFalse(bool(self.get('shared.TimedProject.BlocksManual(3,10)')))
 def test_cached_read_display_no_requests(self):
  self.runlua('ui.Begin();for i=1,5 do ui.Read();ui.Pulse();SPCTimedProjectDisplay.Text(0,10)end');self.assertEqual(self.get('#packets'),1)
 def test_display_wait_stop_other_city(self):
  self.runlua("mode='late';ui.Begin()");self.cycle();self.assertEqual(self.get('(SPCTimedProjectDisplay.Text(0,10))'),'待确认');self.assertEqual(self.get('(SPCTimedProjectDisplay.Text(0,11))'),'开启后1')
  self.runlua('turn=22;Events.PlayerTurnActivated(0)');self.assertEqual(self.get('(SPCTimedProjectDisplay.Text(0,10))'),'已暂停')
 def test_static_and_manifest(self):
  paths=['Mod/TimedProject.lua','Mod/UI/TimedProjectRead.lua','Mod/UI/TimedProjectDisplay.lua','Mod/UI/CrewProjectOrder.lua','Mod/Gameplay.lua','Mod/UI/P0Panel.lua','Mod/OverflowStorageProbe.lua']
  for p in paths:self.lua.execute('assert(load(...))',(ROOT/p).read_text())
  tree=ET.parse(ROOT/'Mod/SpecializationP0.modinfo');self.assertEqual(tree.getroot().get('version'),'148')
  for parent in [tree.find('./Files'),tree.find("./InGameActions/ImportFiles[@id='SPCP0_Common']")]:
   files=[x.text for x in parent.findall('File')];self.assertEqual(len(files),len(set(files)));self.assertTrue(all((ROOT/'Mod'/p).exists() for p in files))
  source=(ROOT/'Mod/TimedProject.lua').read_text();self.assertNotIn('AddProgress',source);self.assertNotIn('SetProperty',source);self.assertEqual(source.count('q:FinishProgress()'),1)
  for p in ['Mod/UI/TimedProjectDisplay.lua','Mod/UI/TimedProjectRead.lua']:self.assertNotIn('SetUpdate',(ROOT/p).read_text())
# Direct old writers and event observers, not a full gameplay regression.
class FinishRegression(previous.old.FinishTests):pass
class ObservationRegression(previous.Observer):
 def test_actual_panel_buttons(self):
  # B120 UI binding intentionally superseded; actual B121 buttons tested above.
  self.run('ui.Begin();ui.Read();ui.End()');self.assertEqual(self.state(),'ENDED');self.assertEqual(self.get('writes'),0)
if __name__=='__main__':unittest.main()
