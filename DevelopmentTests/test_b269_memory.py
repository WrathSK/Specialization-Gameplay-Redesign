"""Actual Lua and offline native/transport doubles; never attaches to Civ VI."""
import importlib.util
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from lupa.lua55 import LuaRuntime
R=Path(__file__).resolve().parents[1]
def load(name,path):
 s=importlib.util.spec_from_file_location(name,R/path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
collector=load('b269collector','tools/collect_expedition_trace.py')
reader=collector.reader
Memory=collector.MemoryEvidence

class LuaTests(unittest.TestCase):
 def setUp(self):
  self.l=LuaRuntime(unpack_returned_tuples=True)
  self.l.execute('''
   turn=1;heap=300*1024;collections=0;prints=0
   print=function() prints=prints+1 end
   collectgarbage=function(mode) if mode=='count' then return heap elseif mode=='isrunning' then return true else collections=collections+1;heap=300*1024 end end
   Game={GetCurrentGameTurn=function()return turn end,GetLocalPlayer=function()return 0 end}
   ExposedMembers={};Events=setmetatable({},{__index=function(t,k)local e={callbacks={}};e.Add=function(f)table.insert(e.callbacks,f)end;e.Fire=function(...)for _,f in ipairs(e.callbacks)do f(...)end end;t[k]=e;return e end})
   P={Field=function(o,k)return o[k]end,IsTestPlayer=function(p)return p==0 end}
   shared={NetworkBridge={ready=true}};ExposedMembers.SPC_P0=shared
  ''')
  self.l.execute(getattr(self,'source',(R/'Mod/PerformanceCounters.lua').read_text()))
  self.l.execute('ExposedMembers.SPC_Performance=SPCPerformance.New();SPCPerformance.StartMemory(P,shared)')
 def test_duplicates_foreign_and_reload(self):
  self.l.execute('Events.PlayerTurnActivated.Fire(1);Events.PlayerTurnActivated.Fire(0);Events.PlayerTurnActivated.Fire(0)')
  self.assertEqual(self.l.eval('#shared.MemoryEvidence.rows'),2) # boundary + GC baseline
  self.l.execute('old=shared.MemoryEvidence;SPCPerformance.StartMemory(P,shared);Events.PlayerTurnActivated.Fire(0)')
  self.assertEqual(self.l.eval('#old.rows'),2)
  self.assertEqual(self.l.eval('#shared.MemoryEvidence.rows'),2)
 def test_gc_after_print_budget_and_ring_bound(self):
  self.l.execute('''Events.LoadScreenClose.Fire();for t=2,90 do turn=t;heap=600*1024;Events.PlayerTurnActivated.Fire(0);Events.GameCoreEventPublishComplete.Fire();Events.PlayerTurnDeactivated.Fire(0)end''')
  self.assertEqual(self.l.eval('#shared.MemoryEvidence.rows'),128)
  self.assertGreater(self.l.eval('collections'),24)
  self.assertLessEqual(self.l.eval('prints'),24)
  self.assertTrue(self.l.eval("shared.MemoryEvidence.rows[127].kind=='GC'"))
 def test_counters_not_reset_and_no_gc_on_boundaries(self):
  self.l.execute("SPCPerformance.Count('city_scan',5);Events.PlayerTurnDeactivated.Fire(0)")
  self.assertEqual(self.l.eval('ExposedMembers.SPC_Performance.entries.city_scan.total'),5)
  self.assertEqual(self.l.eval('shared.MemoryEvidence.rows[1].work_city_scan'),5)
  self.assertEqual(self.l.eval('collections'),0)
 def test_snapshot_round_trip(self):
  self.l.execute('Events.PlayerTurnActivated.Fire(0)')
  rows=[];self.l.globals().print=rows.append
  self.l.execute(reader.command('trace','TEST ','END'))
  self.assertTrue(any('MEM epoch=' in x and 'heapMiB=300' in x for x in rows))
  self.assertTrue(any('MEM_META' in x for x in rows))

 def test_gc_policy_matches_deployed_source(self):
  import subprocess
  baseline=subprocess.check_output(['git','show','852b04c:Mod/PerformanceCounters.lua'],cwd=R,text=True)
  results=[]
  for source in (baseline,(R/'Mod/PerformanceCounters.lua').read_text()):
   self.source=source;self.setUp()
   self.l.execute("Events.LoadScreenClose.Fire();for t=2,30 do turn=t;heap=(t%3==0 and 600 or 310)*1024;shared.NetworkBridge.ready=t%5~=0;Events.PlayerTurnActivated.Fire(0);Events.GameCoreEventPublishComplete.Fire();Events.PlayerTurnDeactivated.Fire(0)end")
   results.append((self.l.eval('collections'),self.l.eval('shared.MemoryObservation.AutoGC.reason'),self.l.eval('shared.MemoryObservation.AutoGC.enabled')))
  self.assertEqual(results[0],results[1])

 def test_full_snapshot_and_gc_failure(self):
  self.l.execute("Events.LoadScreenClose.Fire();for t=2,90 do turn=t;Events.PlayerTurnActivated.Fire(0);Events.PlayerTurnDeactivated.Fire(0)end;ExposedMembers.SPC_B205TrainingTrace={schema=205,entries={}};for i=1,256 do ExposedMembers.SPC_B205TrainingTrace.entries[i]={sequence=i,line='entry'}end")
  rows=[];self.l.globals().print=rows.append
  self.l.execute(reader.command('trace','TEST ','END'))
  self.assertLessEqual(len(rows),reader.MAX_RECORDS)
  self.assertEqual(sum('MEM epoch=' in x for x in rows),128)
  self.l.execute("collectgarbage=function(mode)if mode=='count'then return 900*1024 elseif mode=='isrunning'then return false end end;turn=100;Events.PlayerTurnActivated.Fire(0);Events.GameCoreEventPublishComplete.Fire()")
  self.assertEqual(self.l.eval('shared.MemoryObservation.AutoGC.failure'),'ENGINE_GC_STOPPED')
  self.assertEqual(self.l.eval('shared.MemoryEvidence.rows[128].gcFailure'),'ENGINE_GC_STOPPED')

class EvidenceTests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory(dir=R/'local');self.addCleanup(self.tmp.cleanup)
  self.events=[];self.m=Memory(Path(self.tmp.name),lambda *a,**k:self.events.append((a,k)))
  self.addCleanup(self.m.close)
 def row(self,seq,epoch='a',**kw):
  return dict(epoch=epoch,seq=str(seq),kind='TURN_END',heapMiB='300',work_city_scan=str(seq*5),**kw)
 def test_dedup_gap_reload(self):
  self.m.add(self.row(1));self.m.add(self.row(1));self.m.add(self.row(3));self.m.add(self.row(1,'b'))
  self.assertEqual(self.m.rows,3);self.assertEqual(self.m.segments,2)
  text=(Path(self.tmp.name)/'memory.jsonl').read_text()
  self.assertIn('"kind": "gap"',text)
  self.assertIn('"work_city_scan": 10',text)
 def test_cap(self):
  with patch.object(collector._memory,'CAP',100):
   self.m.write('test',text='a'*150);self.m.write('test')
  self.assertTrue(self.m.stopped);self.assertEqual(self.m.bytes,0)
 def test_os_failure_isolated(self):
  self.m.os_disabled=True;self.m.sample_process();self.m.add(self.row(1));self.assertEqual(self.m.rows,1)
 def test_process_identity_change_disables(self):
  class Fake:
   def sample(self,i):raise RuntimeError('changed')
  self.m.native=True;self.m.reader=Fake();self.m.identity={'pid':1}
  self.m.sample_process();self.assertTrue(self.m.os_disabled);self.assertIsNone(self.m.latest)
 def test_process_cadence_and_values(self):
  now=[0];self.m.clock=lambda:now[0]
  class Fake:
   calls=0
   def sample(self,i):
    self.calls+=1
    return dict(physical_footprint_bytes=1000+self.calls,rss_bytes=500)
  fake=Fake();self.m.native=True;self.m.reader=fake;self.m.identity={'pid':7}
  self.m.sample_process();now[0]=29;self.m.sample_process();now[0]=30;self.m.sample_process()
  self.assertEqual(fake.calls,2);self.assertEqual(self.m.last_process-self.m.first_process,1)
 def test_gc_summary_and_no_cross_load_delta(self):
  self.m.add(dict(epoch='a',seq='1',kind='GC',before='600',after='300',cpu='0.2',reason='AUTO_GROWTH'))
  self.m.add(self.row(2));self.m.add(self.row(1,'b'))
  self.assertEqual(self.m.gc_completed,1);self.assertEqual(self.m.gc_freed,300)
  import json
  rows=[json.loads(x) for x in (Path(self.tmp.name)/'memory.jsonl').read_text().splitlines()]
  self.assertEqual(rows[-1]['work_since_previous_end'],{})
 def test_gc_allowlist(self):
  self.assertIsNotNone(reader.gc_line('[SPC][GC_TRIAL] T10 AUTO_GROWTH beforeMiB=600 afterMiB=300 cpuSec=0.10 wallSec=0.00'))
  self.assertIsNone(reader.gc_line('arbitrary private output'))

if __name__=='__main__':unittest.main()
