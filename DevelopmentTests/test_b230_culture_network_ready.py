"""B230 actual Lua initialization and read-only diagnostics; LOCAL evidence only."""
import unittest
from pathlib import Path
from test_culture_network import fixture
from test_p0_panel_current_layout import panel_runtime
ROUTES="send('0,4,0,2,10;0,2,0,1,11;0,2,0,5,12',3)"
class Readiness(unittest.TestCase):
 def fresh(self):
  l=fixture(False);l.execute('print=function()end');return l
 def test_publication_initializes_without_load_or_p0(self):
  l=self.fresh();l.execute("complete(4,1);"+ROUTES+";assert(cn.ready and amount(cities[1])==1 and propertyWrites==0)")
 def test_turn_event_recovers_preexisting_input_without_new_publication(self):
  l=self.fresh();l.execute("shared.CultureNetwork=nil;"+ROUTES+";shared.CultureNetwork=cn;complete(4,1);assert(not cn.ready);fire('PlayerTurnActivated',0);fire('GameCoreEventPublishComplete');assert(cn.ready and amount(cities[1])==1)")
 def test_repeated_load_events_do_not_remove_recreated_carriers(self):
  l=self.fresh();l.execute("complete(4,1);"+ROUTES+";local a,b=created,removed;for i=1,5 do fire('LoadScreenClose');fire('PlayerTurnActivated',0);fire('GameCoreEventPublishComplete')end;assert(created==a and removed==b)")
 def test_cleanup_occurs_once_and_preserves_unowned_and_history(self):
  l=self.fresh();l.execute("cities[1].present.BUILDING_SPC_CULTURE_NETWORK_RESEARCH_7=true;cities[1].locations.BUILDING_SPC_CULTURE_NETWORK_RESEARCH_7=100;cities[1].present.KEEP=true;complete(4,1);"+ROUTES+";assert(amount(cities[1])==1 and cities[1].present.KEEP and next(history[4]) and propertyWrites==0)")
 def test_invalid_database_can_recover_on_later_real_event(self):
  l=self.fresh();l.execute("local rows=P.Rows;P.Rows=function()return nil end;cn.Audit();assert(not cn.ready and cn.error);P.Rows=rows;complete(4,1);"+ROUTES+";assert(cn.ready and not cn.error and amount(cities[1])==1)")
 def test_wrong_owner_does_not_initialize(self):
  l=self.fresh();l.execute("cn.Audit({player=99});assert(not cn.ready and created==0 and removed==0)")
 def test_unknown_history_not_fabricated(self):
  l=self.fresh();l.execute("cities[4].historyUnknown=true;"+ROUTES+";assert(cn.ready and cn.errors['0:1'] and amount(cities[1])==0);cities[4].historyUnknown=false;complete(4,1);cn.SourceChanged(0,4);assert(amount(cities[1])==1 and not cn.errors['0:1'])")
class Reports(unittest.TestCase):
 def test_buttons_both_read_only_and_in_current_empty_slots(self):
  _,l=panel_runtime();l.execute("Controls.NetworkButton.callbacks[Mouse.eLClick]();assert(requests[#requests].Action=='NETWORK_READ');Controls.NetworkButton.callbacks[Mouse.eRClick]();assert(requests[#requests].Action=='NETWORK_DETAIL');Controls.CarrierStepButton.callbacks[Mouse.eLClick]();assert(requests[#requests].Action=='NETWORK_DETAIL')")
 def test_report_does_not_initialize_or_refresh(self):
  l=fixture(False);l.execute("print=function()end;net.Refresh=function()error('REPORT_REFRESH')end;local out=cn.Report(0,cities[1],true);assert(out:find('CN_NOT_READY') and not cn.ready and created==0 and removed==0)")
 def test_details_and_log_preserve_business_state(self):
  l=fixture();l.execute("print=function()end;complete(4,1);cn.SourceChanged(0,4);local a,b=created,removed;local rev=net.players[0].inputRevision;net.Refresh=function()error('REPORT_REFRESH')end;local report=cn.Report(0,cities[1],true);assert(report:find('完整文明 1') and report:find('来源'));assert(created==a and removed==b and propertyWrites==0 and net.players[0].inputRevision==rev);local found=false;for _,e in ipairs(ExposedMembers.SPC_B205TrainingTrace.entries)do if e.stage=='NETWORK_STATE' and e.city=='1' and e.expected=='2'then found=true end end;assert(found)")
 def test_automatic_success_without_opening_report(self):
  l=fixture(False);l.execute("print=function()end;complete(4,1);"+ROUTES+";local found=false;for _,e in ipairs(ExposedMembers.SPC_B205TrainingTrace.entries)do if e.stage=='NETWORK_STATE' and e.count=='1'then found=true end end;assert(found)")
 def test_diagnostic_failure_does_not_block_yields(self):
  l=fixture(False);l.execute("print=function()end;ExposedMembers.SPC_B205TrainingTrace.entries=nil;complete(4,1);"+ROUTES+";assert(cn.ready and amount(cities[1])==1)")
 def test_unchanged_updates_do_not_fill_trace_across_turns(self):
  l=fixture(False);l.execute("print=function()end;complete(4,1);"+ROUTES+";local n=ExposedMembers.SPC_B205TrainingTrace.sequence;for i=1,20 do turn=turn+1;cn.Audit({player=0})end;assert(ExposedMembers.SPC_B205TrainingTrace.sequence==n)")
 def test_real_network_state_survives_late_collector_snapshot(self):
  from test_expedition_trace_reader import reader
  l=fixture();l.execute("print=function()end;complete(4,1);cn.SourceChanged(0,4);cn.Report(0,cities[1],true);lines={};print=function(s)lines[#lines+1]=s end")
  l.execute(reader.command('trace','MARK:','DONE'))
  lines=[reader.training_line(s) for s in l.globals().lines.values()]
  self.assertTrue(any(s and 'stage=NETWORK_STATE' in s and 'expected=2' in s for s in lines))
 def test_gameplay_routes_reports_without_legacy_refresh(self):
  text=(Path(__file__).resolve().parents[1]/'Mod/Gameplay.lua').read_text()
  branch=text.split('if params.Action=="NETWORK_READ" or params.Action=="NETWORK_DETAIL" then',1)[1].split('return',1)[0]
  # B231 keeps the read-only intent and restores independent shared topology.
  self.assertIn('shared.NetworkBridge.Report',branch)
  self.assertNotIn('NetworkBridge.Read(',branch)
  self.assertNotIn('.Refresh(',branch)
 def test_no_activity_changes_or_timer_added(self):
  text=(Path(__file__).resolve().parents[1]/'Mod/CultureNetwork.lua').read_text()
  for forbidden in ('SetUpdate','SystemUpdateUI','RequestOperation','RequestCommand'):
   self.assertNotIn(forbidden,text)
if __name__=='__main__':unittest.main()
