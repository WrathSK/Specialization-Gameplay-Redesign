"""Approved B270 GC scheduling/count quality and collector regressions; no game attachment."""
from pathlib import Path
import importlib.util
import tempfile
import unittest
R=Path(__file__).resolve().parents[1]
def load(name,path):
    s=importlib.util.spec_from_file_location(name,R/path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
old=load('b270_existing_memory','DevelopmentTests/test_b269_memory.py')

class GCRepairTests(unittest.TestCase):
    def setUp(self):
        fixture=old.LuaTests();fixture.setUp();self.l=fixture.l
        self.l.execute("rawReads=0;base=collectgarbage;collectgarbage=function(m)if m=='count'then rawReads=rawReads+1 end;return base(m)end;Events.LoadScreenClose.Fire();turn=3;heap=700*1024")
    def test_one_ack_retry_and_scalar_wait(self):
        self.l.execute('''
          ExposedMembers.SPC_Performance.inflight=1;Events.PlayerTurnActivated.Fire(0);Events.GameCoreEventPublishComplete.Fire()
          local r,p=rawReads,prints
          for i=1,10000 do Events.GameCoreEventPublishComplete.Fire()end
          assert(rawReads==r and prints==p and collections==0)
          Events.PlayerTurnActivated.Fire(0);ExposedMembers.SPC_Performance.inflight=0
          Events.GameCoreEventPublishComplete.Fire();assert(collections==1)
          heap=900*1024;Events.PlayerTurnActivated.Fire(0);Events.GameCoreEventPublishComplete.Fire();assert(collections==1)
        ''')
    def test_foreign_activation_and_deactivation_cancel_retry(self):
        for event in ('Events.PlayerTurnActivated.Fire(7)','Events.PlayerTurnDeactivated.Fire(0)'):
            self.setUp();self.l.execute('ExposedMembers.SPC_Performance.inflight=1;Events.PlayerTurnActivated.Fire(0);Events.GameCoreEventPublishComplete.Fire();'+event+';ExposedMembers.SPC_Performance.inflight=0;Events.GameCoreEventPublishComplete.Fire();assert(collections==0)')
    def test_retry_keeps_all_guards_and_is_spent_once(self):
        self.l.execute('''ExposedMembers.SPC_Performance.inflight=1;Events.PlayerTurnActivated.Fire(0);Events.GameCoreEventPublishComplete.Fire()
          ExposedMembers.SPC_Performance.inflight=0;shared.RequestDepth=1;Events.GameCoreEventPublishComplete.Fire()
          shared.RequestDepth=0;Events.GameCoreEventPublishComplete.Fire();assert(collections==0)
          turn=4;Events.PlayerTurnActivated.Fire(0);Events.GameCoreEventPublishComplete.Fire();assert(collections==1)
        ''')
    def test_negative_and_wrapped_positive_remain_untrusted(self):
        self.l.execute('''heap=-1024;local n,s,r=SPCPerformance.ReadHeap();assert(n==nil and s=='NATIVE_NEGATIVE' and r==-1024)
          heap=56*1024;local v,q=SPCPerformance.ReadHeap();assert(v==nil and q=='RANGE_UNTRUSTED')
          Events.PlayerTurnActivated.Fire(0);Events.GameCoreEventPublishComplete.Fire();assert(collections==0 and shared.MemoryObservation.AutoGC.failure=='COUNT_UNAVAILABLE')
        ''')
    def test_raw_invalid_status_roundtrip(self):
        self.l.execute('heap=-1024;Events.PlayerTurnDeactivated.Fire(0)')
        lines=[];self.l.globals().print=lines.append;self.l.execute(old.reader.command('trace','TEST ','END'))
        self.assertTrue(any('heapStatus=NATIVE_NEGATIVE' in x and 'heapRawKB=-1024' in x for x in lines))
    def test_old_runtime_count_is_explicit_legacy(self):
        self.l.execute("shared.MemoryEvidence={schema=1,epoch='old',rows={{seq=1,kind='TURN_END',turn=1,heapMiB=300}}}")
        lines=[];self.l.globals().print=lines.append;self.l.execute(old.reader.command('trace','TEST ','END'))
        self.assertTrue(any('heapStatus=LEGACY' in x and 'heapMiB=300' in x for x in lines))

class SummaryRepairTests(unittest.TestCase):
    def test_invalid_interval_not_erased_and_latest_boundary_retained(self):
        with tempfile.TemporaryDirectory() as td:
            e=old.Memory(Path(td),lambda *a,**k:None)
            e.add(dict(epoch='a',seq='1',turn='40',kind='TURN_END',heapMiB='1865',heapStatus='OK',work_city_scan='10'))
            e.add(dict(epoch='a',seq='2',turn='41',kind='TURN_BEGIN',heapMiB='UNKNOWN',heapStatus='NATIVE_NEGATIVE',heapRawKB='-123'))
            e.add(dict(epoch='a',seq='3',turn='52',kind='TURN_BEGIN',heapMiB='56',heapStatus='RANGE_UNTRUSTED',work_city_scan='20'))
            text='\n'.join(e.summary());e.close()
            self.assertIn('1865.0 / UNTRUSTED',text)
            self.assertIn("'work_city_scan': 20",text);self.assertIn('T52 TURN_BEGIN',text)
    def test_lost_connection_does_not_sample_exit_tail(self):
        from types import SimpleNamespace
        now=[0];samples=[];calls=[0]
        session=SimpleNamespace(memory=SimpleNamespace(sample_process=lambda:samples.append(now[0])),
                                event=lambda *a,**k:None)
        def capture(mode,on_record,record_seconds):
            calls[0]+=1
            if calls[0]==1:
                on_record(old.reader.PREFIX+'LISTENING seconds=30')
                now[0]+=30
            else:
                raise old.reader.CaptureError('SOCKET_UNAVAILABLE')
        result=old.collector.run(session,capture=capture,clock=lambda:now[0],
                                 sleep=lambda n:now.__setitem__(0,now[0]+n),
                                 idle_exit=30,out=lambda s:None)
        self.assertEqual(result,'GAME_EXITED')
        self.assertEqual(samples,[0])

if __name__=='__main__': unittest.main()
