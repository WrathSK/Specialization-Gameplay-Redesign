"""Pure model/temp-file tests. No game process discovery or diagnostics."""
import importlib.util, tempfile, unittest, json, argparse, subprocess, sys, time
from unittest.mock import patch
from pathlib import Path
R=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('external_monitor',R/'tools/external_monitor/monitor.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
ID={'pid':123,'start_sec':10,'start_usec':20,'name':'Civ6_Exe_Child'}
ROW={'rss_bytes':100,'physical_footprint_bytes':120,'virtual_size_bytes':1000,'cpu_pct_ps':0.0,'thread_count':3,'collection_ms':.1}
class Tests(unittest.TestCase):
 def test_10000_samples_and_retention(self):
  with tempfile.TemporaryDirectory(dir='/private/tmp') as tmp:
   root=m.LogRoot(Path(tmp)/'logs');root.prune();s=m.Session(root,ID,'test',30,'off')
   for _ in range(10000):s.collect(ROW)
   self.assertEqual(len(s.policy.history),4);self.assertEqual(s.meta['rows'],10000);self.assertLess(m.dir_size(s.path),m.SESSION_CAP)
   self.assertEqual(len(list(s.path.iterdir())),4);s.close('test')
   for _ in range(25):root.prune();a=m.Session(root,ID,'test',30,'off');a.close('test')
   self.assertEqual(len(list(root.path.glob('session-*'))),20);self.assertLess(m.dir_size(root.path),m.ROOT_CAP);root.close()
 def test_total_bytes_retention(self):
  with tempfile.TemporaryDirectory(dir='/private/tmp') as tmp:
   root=m.LogRoot(Path(tmp)/'logs')
   for _ in range(20):
    root.prune();s=m.Session(root,ID,'test',30,'off');s.close('test')
    with (s.path/'capture-01-vmmap.txt').open('wb') as f:f.truncate(20*m.MiB)
   self.assertLess(m.dir_size(root.path),m.ROOT_CAP);self.assertLess(len(list(root.path.glob('session-*'))),20);root.close()
 def test_run_ends_no_rediscovery(self):
  class Reader:
   calls=0
   def identity(self,pid):return ID
   def sample(self,identity):
    self.calls+=1
    if self.calls>1:raise m.ProcessEnded('Target exited')
    return ROW
  with tempfile.TemporaryDirectory(dir='/private/tmp') as tmp:
   with patch.object(m,'MacReader',return_value=Reader()),patch.object(m,'find_game',side_effect=AssertionError('must not rediscover')):
    m.run(argparse.Namespace(pid=123,log_dir=Path(tmp)/'logs',build='test',interval=0,auto_snapshots='off'))
   files=list((Path(tmp)/'logs').glob('session-*/session.json'));self.assertEqual(len(files),1)
   info=json.loads(files[0].read_text());self.assertEqual(info['state'],'ENDED');self.assertEqual(info['rows'],1)
 def test_game_log_root_rejected(self):
  with tempfile.TemporaryDirectory(dir='/private/tmp') as tmp:
   with self.assertRaises(ValueError):m.LogRoot(Path(tmp)/'Mods'/'logs')
 def test_snapshot_failure_does_not_stop_trend(self):
  class Reader:
   def identity(self,pid):return ID
  with tempfile.TemporaryDirectory(dir='/private/tmp') as tmp:
   root=m.LogRoot(Path(tmp)/'logs');s=m.Session(root,ID,'test',30,'off')
   with patch.object(m,'capture_tool',side_effect=PermissionError('test denial')) as call:
    s.snapshot(Reader(),'vmmap','manual',1000);s.snapshot(Reader(),'vmmap','manual',2000);self.assertEqual(call.call_count,1)
   s.collect(ROW);self.assertEqual(s.meta['rows'],1);self.assertIn('vmmap',s.disabled_tools);s.close('test');root.close()
 def test_capture_limits(self):
  class Reader:
   def identity(self,pid):return ID
  result={'exit_code':0,'completion':'complete','duration_seconds':.1}
  with tempfile.TemporaryDirectory(dir='/private/tmp') as tmp:
   root=m.LogRoot(Path(tmp)/'logs');s=m.Session(root,ID,'test',30,'off')
   with patch.object(m,'capture_tool',side_effect=lambda *a:dict(result)) as call:
    for n in range(1,4):s.snapshot(Reader(),'sample','manual',n*1000)
    self.assertEqual(call.call_count,2)
    for n in range(4,14):s.snapshot(Reader(),'vmmap','manual',n*1000)
    self.assertEqual(call.call_count,8)
   s.close('test');root.close()
 def test_policy(self):
  p=m.Policy()
  for t in range(0,60,30):p.observe(t,11e9);self.assertIsNone(p.due(t))
  p.observe(60,11e9);self.assertEqual(p.due(60),'baseline');p.captured(60)
  p.observe(90,16e9);self.assertIsNone(p.due(90));p.observe(660,16e9);self.assertEqual(p.due(660),'absolute_15GB');p.captured(660)
  for t,n in [(1170,16e9),(1200,16.2e9),(1230,16.4e9),(1260,16.6e9)]:p.observe(t,n)
  self.assertEqual(p.due(1260),'sustained_growth_256MiB_per_min')
  p.count=6;self.assertIsNone(p.due(10000))
 def test_caps_marker_and_control(self):
  with tempfile.TemporaryDirectory(dir='/private/tmp') as tmp:
   root=m.LogRoot(Path(tmp)/'logs');s=m.Session(root,ID,'test',30,'off')
   m.control(argparse.Namespace(session=s.path,action='mark',text='noticed slowdown'))
   self.assertIn('noticed slowdown',(s.path/'markers.tsv').read_text())
   m.control(argparse.Namespace(session=s.path,action='stop'))
   self.assertEqual(m.read_json(s.path/'request.json')['kind'],'stop')
   with self.assertRaises(FileExistsError):m.control(argparse.Namespace(session=s.path,action='stop'))
   f=s.path/'cap.tsv';m.append_tsv(f,['123'],4)
   with self.assertRaises(ValueError):m.append_tsv(f,['456'],4)
   s.close('test');root.close()
 def test_unowned_and_symlink(self):
  with tempfile.TemporaryDirectory(dir='/private/tmp') as tmp:
   p=Path(tmp);(p/'unrelated').write_text('preserve')
   with self.assertRaises(ValueError):m.LogRoot(p)
   (p/'link').symlink_to(p/'unrelated')
   with self.assertRaises(ValueError):m.no_links(p/'link')
   self.assertEqual((p/'unrelated').read_text(),'preserve')
 def test_single_monitor_lock(self):
  with tempfile.TemporaryDirectory(dir='/private/tmp') as tmp:
   r=m.LogRoot(Path(tmp)/'logs')
   with self.assertRaises(BlockingIOError):m.LogRoot(r.path)
   r.close()
 def test_pid_reuse_rejected_before_read(self):
  r=object.__new__(m.MacReader);r.identity=lambda pid:{**ID,'start_usec':21}
  with self.assertRaises(m.ProcessEnded):r.sample(ID)
 def test_capture_output_cap_and_timeout(self):
  with tempfile.TemporaryDirectory(dir='/private/tmp') as tmp:
   noisy=Path(tmp)/'noisy';noisy.write_text('#!'+sys.executable+'\nimport sys\nsys.stdout.write("x"*3000000)\n');noisy.chmod(0o700)
   old=m.TOOLS['vmmap'];m.TOOLS['vmmap']=str(noisy)
   try:
    out=Path(tmp)/'out';r=m.capture_tool('vmmap',123,out)
    self.assertEqual(r['completion'],'output_cap');self.assertEqual(out.stat().st_size,m.CAPTURE_CAP)
    noisy.write_text('#!'+sys.executable+'\nimport time\ntime.sleep(5)\n')
    r=m.capture_tool('vmmap',123,Path(tmp)/'timeout',timeout=.1)
    self.assertEqual(r['completion'],'timeout');self.assertLess(r['duration_seconds'],2)
   finally:m.TOOLS['vmmap']=old
 def test_no_mod_or_debugger_calls(self):
  s=(R/'tools/external_monitor/monitor.py').read_text()
  for token in ('task_for_pid','ptrace','mach_vm_read','RequestPlayerOperation','MallocStackLogging','shell=True','xctrace record'):
   self.assertNotIn(token,s)
if __name__=='__main__':unittest.main()
