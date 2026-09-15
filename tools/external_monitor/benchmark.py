#!/usr/bin/env python3
"""Benchmark ONLY a newly spawned synthetic Python worker, never discovers Civ VI."""
import json, os, resource, selectors, statistics, subprocess, sys, tempfile, time
from pathlib import Path
from monitor import MacReader, LogRoot, Session, capture_tool, VERSION
WORKER=r"""
import sys,time,resource,json
blob=bytearray(64*1024*1024)
print("READY",flush=True)
for line in sys.stdin:
 duration=float(line);start=time.monotonic();r=resource.getrusage(resource.RUSAGE_SELF)
 while time.monotonic()-start<duration:
  t=time.monotonic()
  while time.monotonic()-t<.005:pass
  time.sleep(.045)
 a=resource.getrusage(resource.RUSAGE_SELF)
 print(json.dumps({'wall':time.monotonic()-start,'cpu_seconds':a.ru_utime+a.ru_stime-r.ru_utime-r.ru_stime}),flush=True)
"""
def main():
 if len(sys.argv)!=2:raise SystemExit('usage: benchmark.py OUTPUT.json (only synthetic worker)')
 output=Path(sys.argv[1]);reader=MacReader();result={'monitor_version':VERSION,'target':'new synthetic64MiB Python worker; NOT Civ VI','phases':[]}
 with tempfile.TemporaryDirectory(dir='/private/tmp') as tmp:
  worker=subprocess.Popen([sys.executable,'-u','-c',WORKER],stdin=subprocess.PIPE,stdout=subprocess.PIPE,text=True)
  try:
   assert worker.stdout.readline().strip()=="READY"
   identity=reader.identity(worker.pid)
   root=LogRoot(Path(tmp)/'logs');session=Session(root,identity,'SYNTHETIC-NOT-GAME',30,'off')
   for mode in ('OFF','ON','OFF','ON'):
    before=time.process_time();children=resource.getrusage(resource.RUSAGE_CHILDREN);worker.stdin.write('3\n');worker.stdin.flush();durations=[]
    sel=selectors.DefaultSelector();sel.register(worker.stdout,selectors.EVENT_READ)
    while not sel.select(.1):
     if mode=='ON':
      row=reader.sample(identity);durations.append(row['collection_ms']);session.collect(row)
    payload=json.loads(worker.stdout.readline());sel.close();afterchildren=resource.getrusage(resource.RUSAGE_CHILDREN)
    payload.update(mode=mode,monitor_cpu_seconds=time.process_time()-before,ps_children_cpu_seconds=afterchildren.ru_utime+afterchildren.ru_stime-children.ru_utime-children.ru_stime,samples=len(durations),collection_median_ms=statistics.median(durations) if durations else None,collection_max_ms=max(durations) if durations else None)
    result['phases'].append(payload)
   result['monitor_resources']=reader.sample(reader.identity(os.getpid()))
   result['worker_resources']=reader.sample(identity)
   result['snapshots']=[]
   for kind in ('vmmap','footprint','sample'):
    snap=capture_tool(kind,worker.pid,Path(tmp)/(kind+'.txt'));snap['preview']=(Path(tmp)/(kind+'.txt')).read_text(errors='replace')[:240];result['snapshots'].append(snap)
   # Native short session records/retention exercised, not a game session.
   for _ in range(3):session.collect(reader.sample(identity));time.sleep(.1)
   session.close('synthetic benchmark complete');result['short_session_rows']=session.meta['rows'];result['short_session_bytes']=sum(p.stat().st_size for p in session.path.iterdir());root.close()
   # Exit identity must never resume/re-discover a replacement process.
   worker.stdin.close();worker.wait(timeout=3)
   try:reader.sample(identity);result['exit_detected']=False
   except Exception:result['exit_detected']=True
  finally:
   if worker.poll() is None:worker.terminate();worker.wait(timeout=3)
 output.parent.mkdir(parents=True,exist_ok=True);output.write_text(json.dumps(result,indent=2))
 print(json.dumps(result,indent=2))
if __name__=='__main__':main()
