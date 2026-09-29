"""B124 Claim UI plus direct B123 timer/selection regression; not native ordering proof."""
import unittest
import xml.etree.ElementTree as ET
import test_b122_project_selection_display as previous
from lupa.lua55 import LuaRuntime
ROOT=previous.ROOT
def setup_timer(self):
 self.lua=LuaRuntime(unpack_returned_tuples=True)
 old=previous.prior.previous
 self.runlua(old.old.prev.old.FIXTURE);self.runlua(old.old.prev.EXTRA);self.runlua(old.old.EXTRA)
 self.runlua("include=function()end;Events.PlayerTurnActivated=event();Events.PlayerTurnDeactivated=event();Events.GameCoreEventPublishComplete=event();GameEvents={PlayerTurnStarted=event(),PlayerTurnStartComplete=event()}")
 for f in ['Mod/UI/ClaimProjectUI.lua','Mod/TimedProject.lua','Mod/UI/ProjectTurnRead.lua','Mod/UI/TimedProjectRead.lua','Mod/UI/TimedProjectDisplay.lua']:
  self.runlua((ROOT/f).read_text())
 self.runlua("SPCTimedProject.Start(P,shared);SPCProjectTurnRead.New(P,function()end,function()end);function send(pid,op,p)packets[#packets+1]=p;if not defer then shared.TimedProject.Request(pid,p)end end;ui=SPCTimedProjectRead.New(P,function(s)shown=s end,send)")
class Selection(previous.Selection):
 def setUp(self):
  setup_timer(self)
  self.runlua((ROOT/'Mod/UI/TimedProjectSelection.lua').read_text())
  self.runlua("notifications=0;selection=SPCTimedProjectSelection.New(P,send,function()notifications=notifications+1 end);item={Type=project};target='BUILDING_OLD';size=1")
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
 setUp=setup_timer
 def test_static_and_manifest(self):
  names=['TimedProject.lua','UI/TimedProjectSelection.lua','UI/TimedProjectDisplay.lua','UI/TimedProjectRead.lua','UI/CityBannerManager_SPC_TimedProject.lua','UI/TimedProjectCityPanel.lua','UI/CrewProjectOrder.lua','UI/P0Panel.lua']
  for name in names:self.lua.execute('assert(load(...))',(ROOT/'Mod'/name).read_text())
  tree=ET.parse(ROOT/'Mod/SpecializationP0.modinfo');self.assertEqual(tree.getroot().get('version'),'151')
  for parent in [tree.find('./Files'),tree.find("./InGameActions/ImportFiles[@id='SPCP0_Common']")]:
   files=[x.text for x in parent.findall('File')];self.assertEqual(len(files),len(set(files)));self.assertTrue(all((ROOT/'Mod'/p).exists() for p in files))
  s=(ROOT/'Mod/UI/TimedProjectSelection.lua').read_text();self.assertNotIn('SetUpdate',s);self.assertNotIn('FinishProgress',s)
class ClaimUI(unittest.TestCase):
 setUp=setup_timer
 runlua=previous.prior.Timer.runlua
 get=previous.prior.Timer.get
 def prepare_claim(self):
  self.runlua("claim='PROJECT_SPC_CLAIM_RESEARCH';GameInfo.Projects[claim]={ProjectType=claim,Hash=888};local nativeHash=q.GetCurrentProductionTypeHash;q.GetCurrentProductionTypeHash=function()return target==claim and 888 or nativeHash()end;notified=0;claimUI=SPCClaimProjectUI.New(P,function(pid,op,p)packets[#packets+1]=p end,function()notified=notified+1 end);target='OTHER';size=0")
 def test_claim_wait_single_request_and_display(self):
  self.prepare_claim();self.runlua("claimUI.Before(c,{Type=claim},false);target=claim;claimUI.Pulse()")
  self.assertEqual(self.get('#packets'),0)
  self.runlua('size=1;claimUI.Pulse();claimUI.Pulse()');self.assertEqual(self.get('#packets'),1)
  self.assertEqual(self.get('packets[1].Action'),'CLAIM_BEGIN')
  self.runlua("shared.ClaimProjects={views={['0:10']={stage='ACTIVE',project=claim,start=turn,reason='one turn'}}};claimUI.Pulse()")
  self.assertEqual(self.get('(SPCTimedProjectDisplay.Text(0,10))'),'1')
 def test_claim_load_never_fabricates_request(self):
  self.prepare_claim();self.runlua('target=claim;size=1;claimUI.Pulse()');self.assertEqual(self.get('#packets'),0)
 def test_claim_multiple_queue_rejected(self):
  self.prepare_claim();self.runlua('claimUI.Before(c,{Type=claim},false);target=claim;size=2;claimUI.Pulse()');self.assertEqual(self.get('#packets'),0)
  self.assertIn('数量=2',self.get("ExposedMembers.SPC_ClaimSelection['0:10']"))
 def test_claim_list_and_foreign_display(self):
  self.prepare_claim();self.runlua("list={Owner=0,City=c,ProjectItems={{Type=claim,TurnsLeft=999},{Type='OTHER',TurnsLeft=9}}};SPCTimedProjectDisplay.Items(list)")
  self.assertEqual(self.get('list.ProjectItems[1].TurnsLeft'),'1');self.assertEqual(self.get('list.ProjectItems[2].TurnsLeft'),9)
  self.runlua('owner=3;target=claim');self.assertIsNone(self.get('SPCClaimProjectUI.Current(c)'))
class FinishRegression(previous.FinishRegression):pass
class ObserverRegression(previous.ObserverRegression):pass
if __name__=='__main__':unittest.main()
