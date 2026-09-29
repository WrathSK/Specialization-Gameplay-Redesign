"""B127 load sync and exact native-disabled list filtering; local, not engine evidence."""
import unittest
import test_b124_project_ui as base
from pathlib import Path
R=Path(__file__).resolve().parents[1]
class UI(unittest.TestCase):
 runlua=base.ClaimUI.runlua
 get=base.ClaimUI.get
 def setUp(self):
  base.setup_timer(self)
  base.ClaimUI.prepare_claim(self)
  self.runlua("local old=Players[0].GetCities;Players[0].GetCities=function()local cs=old();cs.Members=function()return ipairs({c})end;return cs end")
 def test_load_once_without_panel_or_begin(self):
  self.runlua("target=claim;size=1;claimUI.WarmStart();claimUI.Pulse();claimUI.WarmStart();claimUI.Sync(c)")
  self.assertEqual(self.get('#packets'),1)
  self.assertEqual(self.get('packets[1].Action'),'CLAIM_SYNC')
  self.runlua("shared.ClaimProjects={views={['0:10']={stage='ACTIVE',project=claim,start=turn,reason='restored'}}};claimUI.Pulse();n=notified;claimUI.Pulse()")
  self.assertEqual(self.get('(SPCTimedProjectDisplay.Text(0,10))'),'1')
  self.assertEqual(self.get('notified'),self.get('n'))
 def test_missed_load_first_publish(self):
  self.runlua('claimUI.Pulse();claimUI.Pulse()')
  self.assertEqual(self.get('#packets'),1)
  self.assertEqual(self.get('packets[1].Action'),'CLAIM_SYNC')
 def test_no_player_waits_then_one_sync(self):
  self.runlua('local get=Game.GetLocalPlayer;Game.GetLocalPlayer=function()return -1 end;claimUI.Pulse();Game.GetLocalPlayer=get')
  self.assertEqual(self.get('#packets'),0)
  self.runlua('claimUI.Pulse();claimUI.Pulse()');self.assertEqual(self.get('#packets'),1)
 def test_selection_still_single_begin(self):
  self.runlua('claimUI.WarmStart();packets={};claimUI.Before(c,{Type=claim},false);target=claim;size=1;claimUI.Pulse();claimUI.Pulse()')
  self.assertEqual(self.get('#packets'),1);self.assertEqual(self.get('packets[1].Action'),'CLAIM_BEGIN')
 def test_exact_filter_and_order(self):
  # Execute the real adapter including registration, without the external HD UI.
  self.runlua("include=function()end;RefreshCurrentProduction=function()end;GetDataHelper=function()return data end;AdvanceProject=function()end;Events.LoadScreenClose=event();LuaEvents={SPC_TimedProjectDisplayChanged=event()};SPCP0=P;UI.RequestPlayerOperation=function()end;ContextPtr={IsHidden=function()return true end}")
  self.runlua((R/'Mod/UI/TimedProjectSelection.lua').read_text())
  self.runlua((R/'Mod/UI/CrewProjectOrder.lua').read_text())
  self.runlua("data={Owner=0,City=c,ProjectItems={{Type='PROJECT_SPC_CLAIM_RESEARCH',Disabled=true},{Type='PROJECT_SPC_CREW_1360',Disabled=false},{Type='OTHER',Disabled=true},{Type='PROJECT_SPC_CREW_250',Disabled=false},{Type='PROJECT_SPC_CREW_420',Disabled=true},{Type='PROJECT_SPC_CLAIM_COMMERCE',Disabled=false},{Type='PROJECT_SPC_CREW_UNKNOWN',Disabled=true},{Type='PROJECT_SPC_CLAIM_CULTURE',Disabled=true,IsCurrentProduction=true}}};GetDataHelper()")
  self.assertEqual(self.get('#data.ProjectItems'),6)
  self.assertEqual(self.get('data.ProjectItems[1].Type'),'PROJECT_SPC_CREW_250')
  self.assertEqual(self.get('data.ProjectItems[2].Type'),'PROJECT_SPC_CREW_1360')
  self.assertEqual(self.get('data.ProjectItems[3].Type'),'OTHER')
  self.assertEqual(self.get('data.ProjectItems[4].Type'),'PROJECT_SPC_CLAIM_COMMERCE')
  self.assertEqual(self.get('data.ProjectItems[5].Type'),'PROJECT_SPC_CREW_UNKNOWN')
  self.assertTrue(self.get('data.ProjectItems[6].IsCurrentProduction'))
 def test_static(self):
  for name in ['UI/CrewProjectOrder.lua','UI/ClaimProjectUI.lua','ClaimProjects.lua']:
   self.lua.execute('assert(load(...))',(R/'Mod'/name).read_text())
  self.assertIn('Events.LoadScreenClose.Add(claimSelection.WarmStart)',(R/'Mod/UI/CrewProjectOrder.lua').read_text())
if __name__=='__main__':unittest.main()
