"""B229 actual-source retained evidence and unchanged release semantics."""
import unittest
from test_expedition_spy_activity_ui import bridge
from test_culture_network import fixture
from test_expedition_trace_reader import reader

class ReleaseEvidence(unittest.TestCase):
 def ready(self):
  l=bridge(with_trace=True);l.execute("print=function()end;function releaseRecord()for _,e in ipairs(ExposedMembers.SPC_B205TrainingTrace.entries)do if e.stage=='ACTIVITY_RELEASE'then return e end end end")
  return l
 def test_entry_release_records_and_never_wakes_awake_unit(self):
  l=self.ready();l.execute("publish('SLEEP');units[41].activity=0;publish('RELEASE',true);assert(releaseRecord().releaseBranch=='ENTRY_READ' and wakeCalls==0 and packets[#packets].Result=='RELEASED')")
 def test_second_read_release_records_one_wake_only(self):
  l=self.ready();l.execute('''
   nativeAuto=false;refreshAuto=false;publish('SLEEP')
   for i=1,4 do Events.GameCoreEventPublishComplete()end
   delayWake=true;publish('RELEASE',true);assert(wakeCalls==1)
   local reads=0
   UnitManager.GetActivityType=function(u)reads=reads+1;if reads==1 then return 1 end;u.activity=0;return 0 end
   Events.GameCoreEventPublishComplete()
   assert(releaseRecord().releaseBranch=='SECOND_READ' and packets[#packets].Result=='RELEASED')
   for i=1,20 do Events.GameCoreEventPublishComplete()end
   assert(wakeCalls==1)
  ''')
 def test_unowned_sleep_is_retained_and_never_woken(self):
  l=self.ready();l.execute("units[41].activity=1;publish('SLEEP');publish('RELEASE',false,nil,true);assert(releaseRecord().releaseBranch=='UNOWNED' and wakeCalls==0 and units[41].activity==1)")
 def test_false_readiness_does_not_invent_ownership_or_block_release(self):
  l=self.ready();l.execute("publish('SLEEP');units[41].activity=2;units[41].IsReadyToSelect=function()return false end;publish('RELEASE',true);assert(packets[#packets].Result=='RELEASED' and wakeCalls==0 and releaseRecord().readyToSelect=='false')")
 def test_broken_diagnostic_ring_does_not_prevent_release(self):
  l=self.ready();l.execute("publish('SLEEP');ExposedMembers.SPC_B205TrainingTrace.entries=nil;publish('RELEASE',true);assert(packets[#packets].Result=='RELEASED' and wakeCalls==1)")

class RetainedNetwork(unittest.TestCase):
 def ready(self):
  l=fixture();l.execute("print=function()end;function waits()local t={};for _,e in ipairs(ExposedMembers.SPC_B205TrainingTrace.entries)do if e.stage=='NETWORK_WAIT'then t[#t+1]=e end end;return t end")
  return l
 def test_snapshot_after_report_preserves_error_and_input(self):
  l=self.ready();l.execute("cn.errors['0:1']='CN_CREATE_UNCONFIRMED';cn.Describe(0,cities[1]);assert(#waits()==1 and waits()[1].networkLayer=='CITY' and waits()[1].networkValidity=='VERIFIED');lines={};print=function(s)lines[#lines+1]=s end")
  l.execute(reader.command('trace','MARK:','DONE'))
  entries=[reader.training_line(s) for s in l.globals().lines.values()]
  self.assertTrue(any(s and 'stage=NETWORK_WAIT' in s and 'CN_CREATE_UNCONFIRMED' in s for s in entries))
 def test_identical_reports_dedup_changes_record_without_writes(self):
  l=self.ready();l.execute('''
   cn.errors['0:1']='CN_CREATE_UNCONFIRMED';local before=created;local revision=net.players[0].inputRevision
   for i=1,100 do cn.Describe(0,cities[1])end;assert(#waits()==1)
   cn.errors['0:1']='CN_REMOVE_UNCONFIRMED';cn.Describe(0,cities[1]);assert(#waits()==2)
   assert(created==before and revision==net.players[0].inputRevision)
  ''')
 def test_budget_ring_and_error_sanitization(self):
  l=self.ready();l.execute('''
   for i=1,150 do cn.errors['0:1']='CN_ERROR_'..i;cn.Describe(0,cities[1])end
   local r=ExposedMembers.SPC_B205TrainingTrace;assert(#r.entries<=64 and r.suppressed>0)
  ''')
 def test_diagnostic_failure_cannot_break_waiting_report(self):
  l=self.ready();l.execute("cn.errors['0:1']='CN_CREATE_UNCONFIRMED';ExposedMembers.SPC_B205TrainingTrace.entries=nil;assert(cn.Describe(0,cities[1]):find('CN_CREATE_UNCONFIRMED',1,true))")

if __name__=='__main__':unittest.main()
