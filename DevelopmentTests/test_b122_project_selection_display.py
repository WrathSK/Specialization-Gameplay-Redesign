"""B122 production entry and independent UI surfaces; engine order remains native-gated."""
import unittest,xml.etree.ElementTree as ET
import test_b121_timed_project as prior
ROOT=prior.ROOT
class Selection(unittest.TestCase):
 runlua=prior.Timer.runlua
 get=prior.Timer.get
 state=prior.Timer.state
 cycle=prior.Timer.cycle
 def setUp(self):
  prior.Timer.setUp(self)
  self.runlua((ROOT/'Mod/UI/TimedProjectSelection.lua').read_text())
  self.runlua("notifications=0;selection=SPCTimedProjectSelection.New(P,send,function()notifications=notifications+1 end);item={Type=project};target='BUILDING_OLD';size=1")
 def choose(self):self.runlua('selection.Before(c,item);target=project;selection.Pulse()')
 def test_click_waits_for_native_selection(self):
  self.runlua('selection.Before(c,item);selection.Pulse()');self.assertEqual(self.get('#packets'),0)
  self.runlua('target=project;selection.Pulse();selection.Pulse()');self.assertEqual(self.get('#packets'),1);self.assertEqual(self.state(),'ACTIVE')
 def test_no_click_no_activation(self):
  self.runlua('target=project;selection.Pulse();Events.PlayerTurnActivated(0)');self.assertEqual(self.get('#packets'),0);self.assertIsNone(self.get('shared.TimedProjectState'))
 def test_single_auto_cycle_without_p0(self):
  self.choose();self.cycle();self.runlua('selection.Pulse()');self.assertEqual(self.state(),'COMPLETED');self.assertEqual(self.get('writes'),1)
 def test_queue_not_current_no_start(self):
  self.runlua('selection.Before(c,item);size=2;selection.Pulse()');self.assertEqual(self.get('#packets'),0)
  self.runlua('target=project;selection.Pulse()');self.assertEqual(self.get('ExposedMembers.SPC_TimedProjectSelection.status'),'ERROR');self.assertEqual(self.get('writes'),0)
 def test_pending_duplicate_click_and_publish(self):
  self.runlua('defer=true;selection.Before(c,item);target=project;selection.Pulse();selection.Pulse()');self.assertEqual(self.get('#packets'),1)
 def test_second_click_before_ack_cannot_replace_request(self):
  self.runlua('defer=true;selection.Before(c,item);target=project;selection.Pulse();accepted=selection.Before(c,item);selection.Pulse()');self.assertFalse(self.get('accepted'));self.assertEqual(self.get('#packets'),1)
 def test_rejected_or_expired_selection(self):
  self.runlua('selection.Before(c,item);turn=21;selection.Pulse()');self.assertEqual(self.get('#packets'),0);self.assertEqual(self.get('ExposedMembers.SPC_TimedProjectSelection.status'),'ERROR')
 def test_error_request_not_retry(self):
  self.runlua("selection=SPCTimedProjectSelection.New(P,function()error('test send')end,function()end);selection.Before(c,item);target=project;selection.Pulse();selection.Pulse()")
  self.assertEqual(self.get('ExposedMembers.SPC_TimedProjectSelection.status'),'ERROR');self.assertEqual(self.get('writes'),0)
 def test_ordinary_choice_unchanged(self):
  self.runlua("accepted=selection.Before(c,{Type='PROJECT_OTHER'});selection.Pulse()");self.assertTrue(self.get('accepted'));self.assertEqual(self.get('#packets'),0)
 def test_old_timer_can_repeat_only_after_known_completion(self):
  self.choose();self.cycle();self.runlua('selection.Pulse();selection.Before(c,item);target=project;size=1;selection.Pulse();Events.PlayerTurnDeactivated(0);turn=22;Events.PlayerTurnActivated(0)');self.assertEqual(self.get('writes'),2);self.assertEqual(self.state(),'COMPLETED')
 def test_uncertain_completion_not_retried_by_selection(self):
  self.runlua('fail=true');self.choose();self.cycle();self.runlua('selection.Pulse();fail=false;selection.Before(c,item);selection.Pulse()');self.assertEqual(self.get('writes'),1);self.assertEqual(self.state(),'STOPPED')
 def test_stop_target_then_reselect(self):
  self.choose();self.runlua("target='BUILDING_OLD';Events.CityProductionChanged(0,10);selection.Pulse();selection.Before(c,item);target=project;selection.Pulse()");self.cycle();self.assertEqual(self.get('writes'),1)
 def test_busy_preserves_timer(self):
  self.choose();self.runlua('selection.Pulse();accepted=selection.Before(c,item)');self.assertFalse(self.get('accepted'));self.assertEqual(self.state(),'ACTIVE');self.assertEqual(self.get('#packets'),1)
class TimerRegression(prior.Timer):
 def ui_env(self):
  self.runlua("include=function()end;SPCP0=P;LuaEvents=setmetatable({},{__index=function(t,k)local e=event();rawset(t,k,e);return e end});ContextPtr={IsHidden=function()return true end};CheckQueueItemSelected=function()return false end;AdvanceProject=function()end;UI.RequestPlayerOperation=send")
  self.runlua((ROOT/'Mod/UI/TimedProjectSelection.lua').read_text())
 def test_actual_buttons(self):
  panel=(ROOT/'Mod/UI/P0Panel.lua').read_text();self.assertIn('PerformanceSnapshotButton:SetHide(true)',panel);self.assertNotIn('projectAction(timer.Begin)',panel);self.assertIn('projectAction(timer.Read)',panel)
 def test_display_exact_only_and_crew_sort(self):
  self.ui_env();self.runlua("RefreshCurrentProduction=function()return 'native' end;data={Owner=0,City=c,ProjectItems={{Type='PROJECT_OTHER',TurnsLeft=77},{Type='PROJECT_SPC_CREW_750'},{Type=project,TurnsLeft=90000,Cost=1000000},{Type='PROJECT_SPC_CREW_250'}}};GetDataHelper=function()return data end")
  self.runlua((ROOT/'Mod/UI/CrewProjectOrder.lua').read_text());self.runlua('out=GetDataHelper()');self.assertEqual(self.get('out.ProjectItems[1].TurnsLeft'),77);self.assertEqual(self.get('out.ProjectItems[2].Type'),'PROJECT_SPC_CREW_250');self.assertEqual(self.get('out.ProjectItems[4].TurnsLeft'),'未启动');self.assertEqual(self.get('out.ProjectItems[4].Cost'),1000000)
  self.runlua('ui.Begin();out=GetDataHelper()');self.assertEqual(self.get('out.ProjectItems[4].TurnsLeft'),'1')
 def test_display_without_crew_and_current_row(self):
  self.ui_env();self.runlua("RefreshCurrentProduction=function()return true end;data={Owner=0,City=c,ProjectItems={{Type=project,TurnsLeft=999}}};GetDataHelper=function()return data end;parent=setmetatable({},{__index=function(t,k)local v={SetText=function(_,s)text=s end,SetPercent=function()end,SetShadowPercent=function()end,SetToolTipString=function()end};rawset(t,k,v);return v end})")
  self.runlua((ROOT/'Mod/UI/CrewProjectOrder.lua').read_text());self.runlua('out=GetDataHelper();ui.Begin();RefreshCurrentProduction(parent,0,10)');self.assertEqual(self.get('out.ProjectItems[1].TurnsLeft'),'未启动');self.assertIn('计时已开启：1回合',self.get('text'))
  self.runlua("target='BUILDING_OLD';text='ordinary';RefreshCurrentProduction(parent,0,10)");self.assertEqual(self.get('text'),'ordinary')
 def test_display_wait_stop_other_city(self):
  self.runlua("mode='late';ui.Begin()");self.cycle();self.assertEqual(self.get('(SPCTimedProjectDisplay.Text(0,10))'),'待确认');self.assertEqual(self.get('(SPCTimedProjectDisplay.Text(0,11))'),'1*')
  self.runlua('turn=22;Events.PlayerTurnActivated(0)');self.assertEqual(self.get('(SPCTimedProjectDisplay.Text(0,10))'),'已暂停')
 def test_static_and_manifest(self):
  names=['TimedProject.lua','UI/TimedProjectSelection.lua','UI/TimedProjectDisplay.lua','UI/TimedProjectRead.lua','UI/CityBannerManager_SPC_TimedProject.lua','UI/TimedProjectCityPanel.lua','UI/CrewProjectOrder.lua','UI/P0Panel.lua']
  for p in names:self.lua.execute('assert(load(...))',(ROOT/'Mod'/p).read_text())
  tree=ET.parse(ROOT/'Mod/SpecializationP0.modinfo');self.assertEqual(tree.getroot().get('version'),'149')
  for parent in [tree.find('./Files'),tree.find("./InGameActions/ImportFiles[@id='SPCP0_Common']")]:
   files=[x.text for x in parent.findall('File')];self.assertEqual(len(files),len(set(files)));self.assertTrue(all((ROOT/'Mod'/p).exists() for p in files))
  for name in names[1:]:self.assertNotIn('FinishProgress()',(ROOT/'Mod'/name).read_text())
 def test_actual_advance_project_no_diagnostic(self):
  self.ui_env();self.runlua("GetDataHelper=function()return nil end;RefreshCurrentProduction=function()end;nativeCalls=0;AdvanceProject=function()nativeCalls=nativeCalls+1;target=project end;target='BUILDING_OLD'")
  self.runlua((ROOT/'Mod/UI/CrewProjectOrder.lua').read_text());self.runlua('AdvanceProject(c,{Type=project});Events.GameCoreEventPublishComplete()');self.assertEqual(self.get('nativeCalls'),1);self.assertEqual(self.state(),'ACTIVE');self.assertEqual(self.get('#packets'),1)
  self.cycle();self.assertEqual(self.get('writes'),1)
 def test_queue_selection_mode_does_not_arm(self):
  self.ui_env();self.runlua('CheckQueueItemSelected=function()return true end;GetDataHelper=function()return nil end;RefreshCurrentProduction=function()end')
  self.runlua((ROOT/'Mod/UI/CrewProjectOrder.lua').read_text());self.runlua('AdvanceProject(c,{Type=project});Events.GameCoreEventPublishComplete()');self.assertEqual(self.get('#packets'),0)
 def controls(self):
  self.ui_env();self.runlua("function control()return {text='',tip='',SetText=function(self,s)self.text=s end,SetToolTipString=function(self,s)self.tip=s end,SetHide=function(self,v)self.hidden=v end,SetPercent=function()end,SetShadowPercent=function()end}end;Controls=setmetatable({},{__index=function(t,k)local c=control();rawset(t,k,c);return c end})")
 def test_banner_number_tooltip_and_restore(self):
  self.controls();self.runlua("inst={TurnsLeft=control(),Button=control(),FillMeter=control(),IconMeter=control()};CityBanner={UpdateProduction=function(self,c)inst.TurnsLeft:SetText('native');inst.Button:SetToolTipString('native tip')end};banner=setmetatable({m_StatProductionIM={GetAllocatedInstance=function()return inst end}},{__index=CityBanner});GetCityBanner=function()return banner end")
  self.runlua((ROOT/'Mod/UI/CityBannerManager_SPC_TimedProject.lua').read_text());self.runlua('ui.Begin();banner:UpdateProduction(c)');self.assertEqual(self.get('inst.TurnsLeft.text'),'1');self.assertIn('自动完成',self.get('inst.Button.tip'))
  self.runlua("target='BUILDING_OLD';LuaEvents.SPC_TimedProjectDisplayChanged(0,10)");self.assertEqual(self.get('inst.TurnsLeft.text'),'native');self.assertEqual(self.get('inst.Button.tip'),'native tip')
 def test_bottom_panel_exact_project_and_ordinary(self):
  self.controls();self.runlua("g_pCity=c;ViewMain=function(data)Controls.ProductionNum:SetText('native');Controls.ProductionLabel:SetText('native label')end;Refresh=function()ViewMain({})end")
  self.runlua((ROOT/'Mod/UI/TimedProjectCityPanel.lua').read_text());self.runlua('ui.Begin();ViewMain({})');self.assertEqual(self.get('Controls.ProductionNum.text'),'1');self.assertEqual(self.get('Controls.ProductionLabel.text'),'回合后完成')
  self.runlua("target='BUILDING_OLD';LuaEvents.SPC_TimedProjectDisplayChanged(0,10)");self.assertEqual(self.get('Controls.ProductionNum.text'),'native')
 def test_foreign_city_not_overridden(self):
  self.runlua('owner=3');self.assertFalse(bool(self.get('SPCTimedProjectDisplay.IsCurrent(c)')))
class FinishRegression(prior.FinishRegression):pass
class ObserverRegression(prior.ObservationRegression):pass
if __name__=='__main__':unittest.main()
