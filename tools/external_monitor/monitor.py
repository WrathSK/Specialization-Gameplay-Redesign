#!/usr/bin/env python3
"""Specialization external monitor. No imports from Mod, game commands, injection or debugger."""
from __future__ import annotations
import argparse, collections, csv, ctypes, datetime as dt, errno, fcntl, io, json, math
import os, platform, selectors, shutil, signal, statistics, subprocess, sys, time, uuid
from pathlib import Path

VERSION='1.0'; SCHEMA=1
OWNER='SpecializationExternalRuntimeMonitor-v1'
ROOT=Path.home()/'Library/Logs/SpecializationExternalMonitor'
MiB=1024*1024
TREND_CAP=4*MiB; EVENT_CAP=128*1024; CAPTURE_CAP=2*MiB
SESSION_CAP=24*MiB; ROOT_CAP=256*MiB; KEEP=20
TOOLS={'vmmap':'/usr/bin/vmmap','footprint':'/usr/bin/footprint','sample':'/usr/bin/sample'}

def utc(): return dt.datetime.now(dt.timezone.utc).isoformat(timespec='milliseconds')
def no_links(p):
    p=Path(os.path.abspath(p))
    if any(q.is_symlink() for q in (p,*p.parents)): raise ValueError('Symlink path rejected')
    return p

def save_json(p,value):
    p=no_links(p);tmp=p.with_name(p.name+'.tmp')
    with tmp.open('x') as f:json.dump(value,f,indent=2);f.flush()
    tmp.replace(p)

def read_json(p):
    p=no_links(p)
    if p.stat().st_size>16384:raise ValueError('Oversize metadata')
    return json.loads(p.read_text())

def append_tsv(p,fields,cap):
    p=no_links(p);s=io.StringIO();csv.writer(s,delimiter='\t',lineterminator='\n').writerow(fields);line=s.getvalue().encode()
    with p.open('ab') as f:
        fcntl.flock(f,fcntl.LOCK_EX)
        if f.tell()+len(line)>cap:raise ValueError('Log size limit reached')
        f.write(line);f.flush()

def owned_session(p):
    p=no_links(p)
    if not p.name.startswith('session-') or read_json(p/'session.json').get('owner')!=OWNER:raise ValueError('Not an owned monitor session')
    return p

def dir_size(p):
    size=0
    for item in p.rglob('*'):
        if item.is_symlink():raise ValueError('Symlink inside log tree rejected')
        if item.is_file():size+=item.stat().st_size
    return size

class LogRoot:
    def __init__(self,path):
        self.path=no_links(path)
        if any(x in self.path.parts for x in ('Mod','Mods','Saves','Cache','ModUserData',"Sid Meier's Civilization VI")):
            raise ValueError('Log root must be outside game/runtime/save directories')
        self.path.mkdir(parents=True,exist_ok=True,mode=0o700)
        marker=self.path/'.monitor-owner'
        if not marker.exists():
            if any(self.path.iterdir()):raise ValueError('Refuse nonempty unowned log root')
            marker.write_text(OWNER)
        with no_links(marker).open() as f:owner=f.read(len(OWNER)+1)
        if owner!=OWNER:raise ValueError('Wrong log root owner')
        self.lock=no_links(self.path/'.lock').open('a')
        try:fcntl.flock(self.lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
        except BaseException:self.lock.close();raise
    def prune(self):
        sessions=[]
        for p in self.path.iterdir():
            if p.name.startswith('session-'):
                owned_session(p);sessions.append((p.name,p,dir_size(p)))
        sessions.sort()
        # Reserve a complete new bounded session, rather than pruning during collection.
        while sessions and (len(sessions)>=KEEP or sum(x[2] for x in sessions)+SESSION_CAP>ROOT_CAP):
            _,p,_=sessions.pop(0);shutil.rmtree(p)
    def close(self):self.lock.close()

# ABI from installed Apple SDK sys/proc_info.h and sys/resource.h.
class BSDInfo(ctypes.Structure):
    _fields_=[(n,ctypes.c_uint32) for n in ('flags','status','xstatus','pid','ppid','uid','gid','ruid','rgid','svuid','svgid','reserved')]+[
        ('comm',ctypes.c_char*16),('name',ctypes.c_char*32)]+[(n,ctypes.c_uint32) for n in ('nfiles','pgid','jobc','tdev','tpgid')]+[
        ('nice',ctypes.c_int32),('start_sec',ctypes.c_uint64),('start_usec',ctypes.c_uint64)]
class TaskInfo(ctypes.Structure):
    _fields_=[(n,ctypes.c_uint64) for n in ('vsz','rss','user','system','threads_user','threads_system')]+[(n,ctypes.c_int32) for n in (
        'policy','faults','pageins','cow','msgsent','msgrecv','machcalls','unixcalls','switches','threads','running','priority')]
class RUsage(ctypes.Structure):
    _fields_=[('uuid',ctypes.c_uint8*16)]+[(n,ctypes.c_uint64) for n in ('user','system','idle','interrupt','pageins','wired','rss','footprint','start','exit')]

class ProcessEnded(Exception):pass
class MacReader:
    def __init__(self):
        if sys.platform!='darwin':raise ValueError('macOS only')
        self.lib=ctypes.CDLL('/usr/lib/libproc.dylib',use_errno=True)
        self.lib.proc_pidinfo.argtypes=[ctypes.c_int,ctypes.c_int,ctypes.c_uint64,ctypes.c_void_p,ctypes.c_int]
        self.lib.proc_pidinfo.restype=ctypes.c_int
        self.lib.proc_pid_rusage.argtypes=[ctypes.c_int,ctypes.c_int,ctypes.c_void_p]
        self.lib.proc_pid_rusage.restype=ctypes.c_int
        self.footprint_available=True
    def info(self,pid,flavor,kind):
        result=kind();n=self.lib.proc_pidinfo(pid,flavor,0,ctypes.byref(result),ctypes.sizeof(result))
        if n!=ctypes.sizeof(result):
            e=ctypes.get_errno()
            if e in (errno.ESRCH,errno.ENOENT):raise ProcessEnded('Target exited')
            raise OSError(e,'proc_pidinfo unavailable; no privilege escalation attempted')
        return result
    def identity(self,pid):
        b=self.info(pid,3,BSDInfo)
        if b.status==5:raise ProcessEnded('Target is zombie/exited')
        return {'pid':pid,'start_sec':b.start_sec,'start_usec':b.start_usec,'name':(b.name or b.comm).decode(errors='replace')}
    def sample(self,identity):
        begin=time.monotonic()
        if self.identity(identity['pid'])!=identity:raise ProcessEnded('PID identity changed')
        t=self.info(identity['pid'],4,TaskInfo);footprint=''
        if self.footprint_available:
            u=RUsage()
            if self.lib.proc_pid_rusage(identity['pid'],0,ctypes.byref(u))==0:footprint=u.footprint
            else:self.footprint_available=False  # optional field; no repeated failing probes
        # ps %cpu avoids ambiguous native CPU tick units across Apple Silicon/Rosetta.
        p=subprocess.run(['/bin/ps','-p',str(identity['pid']),'-o','pcpu='],capture_output=True,text=True,timeout=3,env={**os.environ,'LC_ALL':'C'})
        cpu=''
        if p.returncode==0 and len(p.stdout)<128:
            try:
                val=float(p.stdout.strip())
                if math.isfinite(val) and val>=0:cpu=val
            except ValueError:pass
        if self.identity(identity['pid'])!=identity:raise ProcessEnded('PID identity changed during read')
        return {'rss_bytes':t.rss,'physical_footprint_bytes':footprint,'virtual_size_bytes':t.vsz,
                'cpu_pct_ps':cpu,'thread_count':t.threads,'collection_ms':(time.monotonic()-begin)*1000}

def find_game():
    p=subprocess.run(['/usr/bin/pgrep','-x','Civ6_Exe_Child'],capture_output=True,text=True,timeout=3)
    ids=p.stdout.split()
    if len(ids)!=1 or not ids[0].isdigit():raise ValueError('Expected exactly one Civ6_Exe_Child; start game yourself or provide --pid')
    return int(ids[0])

class Policy:
    def __init__(self):
        self.history=collections.deque(maxlen=4);self.seen=set();self.count=0;self.last=-1e9
    def observe(self,elapsed,value):self.history.append((elapsed,value))
    def due(self,elapsed):
        if self.count>=6 or elapsed<60 or elapsed-self.last<600:return None
        value=self.history[-1][1]
        if not self.count:return 'baseline'
        crossed=[n for n in (10,15,20,30,40) if value>=n*10**9 and n not in self.seen]
        if crossed:return 'absolute_'+str(max(crossed))+'GB'
        h=list(self.history)
        if len(h)==4 and all(b[0]>a[0] and (b[1]-a[1])/(b[0]-a[0])*60>=256*MiB for a,b in zip(h,h[1:])):
            return 'sustained_growth_256MiB_per_min'
        return None
    def captured(self,elapsed):
        self.count+=1;self.last=elapsed
        if self.history:self.seen.update(n for n in (10,15,20,30,40) if self.history[-1][1]>=n*10**9)

def capture_tool(kind,pid,destination,timeout=None):
    """Bounded pipe output. Terminates only the child diagnostic tool on timeout/limit."""
    args={'vmmap':[TOOLS['vmmap'],'-summary',str(pid)],'footprint':[TOOLS['footprint'],'-p',str(pid)],
          'sample':[TOOLS['sample'],str(pid),'5','10','-file','/dev/stdout']}[kind]
    start=time.monotonic();limit=timeout or (15 if kind=='sample' else 5)
    p=subprocess.Popen(args,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    sel=selectors.DefaultSelector();sel.register(p.stdout,selectors.EVENT_READ);size=0;reason='complete'
    try:
        with no_links(destination).open('xb') as f:
            while True:
                if time.monotonic()-start>limit:reason='timeout';break
                events=sel.select(.1)
                if not events:
                    if p.poll() is not None:break
                    continue
                chunk=os.read(p.stdout.fileno(),8192)
                if not chunk:break
                remaining=CAPTURE_CAP-size;f.write(chunk[:remaining]);size+=min(len(chunk),remaining)
                if len(chunk)>remaining:reason='output_cap';break
    finally:
        sel.close();p.stdout.close()
        if p.poll() is None:
            p.terminate()
            try:p.wait(timeout=1)
            except subprocess.TimeoutExpired:p.kill();p.wait(timeout=1)
        else:p.wait()
    return {'tool':kind,'duration_seconds':round(time.monotonic()-start,4),'bytes':size,'exit_code':p.returncode,'completion':reason}

FIELDS=['timestamp_utc','elapsed_seconds','pid','process_start_sec','process_start_usec','rss_bytes','physical_footprint_bytes','virtual_size_bytes','cpu_pct_ps','thread_count','collection_ms']
class Session:
    def __init__(self,root,identity,build,interval,auto_tool):
        self.root=root;self.start=time.monotonic();self.path=root.path/('session-'+dt.datetime.now(dt.timezone.utc).strftime('%Y%m%dT%H%M%S%f')+'-'+uuid.uuid4().hex[:8]);self.path.mkdir(mode=0o700)
        self.meta={'owner':OWNER,'schema':SCHEMA,'monitor_version':VERSION,'session':self.path.name,'start_utc':utc(),'identity':identity,'specialization_build_label':build,'interval_seconds':interval,'auto_snapshot_tool':auto_tool,'state':'RUNNING','monitor_pid':os.getpid(),'rows':0}
        save_json(self.path/'session.json',self.meta)
        append_tsv(self.path/'trend.tsv',FIELDS,TREND_CAP)
        append_tsv(self.path/'events.tsv',['timestamp_utc','elapsed_seconds','type','detail'],EVENT_CAP)
        append_tsv(self.path/'markers.tsv',['timestamp_utc','text'],EVENT_CAP)
        self.policy=Policy();self.capture_count=0;self.sample_count=0;self.disabled_tools=set();self.metric=None
    def event(self,kind,detail):append_tsv(self.path/'events.tsv',[utc(),round(time.monotonic()-self.start,3),kind,str(detail)[:512]],EVENT_CAP)
    def collect(self,row):
        elapsed=time.monotonic()-self.start;id=self.meta['identity']
        append_tsv(self.path/'trend.tsv',[utc(),round(elapsed,3),id['pid'],id['start_sec'],id['start_usec'],*(row[k] for k in FIELDS[5:])],TREND_CAP)
        self.meta['rows']+=1
        metric='physical_footprint_bytes' if row['physical_footprint_bytes']!='' else 'rss_bytes'
        if metric!=self.metric:self.policy.history.clear();self.policy.seen.clear();self.metric=metric;self.event('threshold_metric',metric)
        self.policy.observe(elapsed,row[metric]);return elapsed
    def snapshot(self,reader,kind,reason,elapsed):
        if kind in self.disabled_tools:return
        if self.capture_count>=8 or (kind=='sample' and self.sample_count>=2) or elapsed-self.policy.last<600:
            self.event('capture_suppressed','limit_or_cooldown');return
        if reader.identity(self.meta['identity']['pid'])!=self.meta['identity']:raise ProcessEnded('PID changed before capture')
        self.capture_count+=1;self.sample_count+=int(kind=='sample');self.policy.captured(elapsed)
        name=f'capture-{self.capture_count:02d}-{kind}.txt'
        try:result=capture_tool(kind,self.meta['identity']['pid'],self.path/name)
        except (OSError,subprocess.SubprocessError) as e:
            self.disabled_tools.add(kind);self.event('tool_disabled',kind+': '+str(e));return
        # PID-bound command tools cannot eliminate the tiny exit/reuse race at launch; reject evidence on change.
        try:still_same=reader.identity(self.meta['identity']['pid'])==self.meta['identity']
        except ProcessEnded:still_same=False
        result.update(timestamp_utc=utc(),reason=reason,file=name,identity_still_matches=still_same)
        self.event('capture',json.dumps(result));self.meta['last_capture']=result
        if result['exit_code'] or result['completion']!='complete' or result['duration_seconds']>(10 if kind=='sample' else 3) or not still_same:
            self.disabled_tools.add(kind);self.event('tool_disabled',kind)
        if not still_same:raise ProcessEnded('Target exited/changed during capture')
    def close(self,reason):
        self.meta.update(state='ENDED',end_utc=utc(),end_reason=reason,captures=self.capture_count)
        save_json(self.path/'session.json',self.meta)

def run(args):
    reader=MacReader();pid=args.pid or find_game();identity=reader.identity(pid)
    if identity['name'] not in ('Civ6_Exe_Child','Civilization VI'):raise ValueError('PID is not recognized Civ VI process')
    initial=reader.sample(identity) # fail before creating a session if ordinary access is denied
    root=LogRoot(args.log_dir)
    try:
        root.prune();s=Session(root,identity,args.build,args.interval,args.auto_snapshots)
        print('Session:',s.path,flush=True);print('Ctrl+C stops ONLY the monitor.',flush=True)
        reason='stopped';stop=False
        def stop_monitor(*_):nonlocal stop;stop=True
        previous={n:signal.signal(n,stop_monitor) for n in (signal.SIGINT,signal.SIGTERM)}
        try:
            row=initial
            while not stop:
                elapsed=s.collect(row)
                command=s.path/'request.json'
                if command.exists():
                    req=read_json(command);command.unlink();kind=req.get('kind')
                    if kind=='stop':reason='user_stop';break
                    if kind in TOOLS:s.snapshot(reader,kind,'manual',elapsed)
                    else:s.event('invalid_request','unknown kind')
                elif args.auto_snapshots!='off':
                    why=s.policy.due(elapsed)
                    if why:s.snapshot(reader,args.auto_snapshots,why,elapsed)
                # No active timer/daemon after exit. Sleeps rather than busy polling.
                deadline=time.monotonic()+args.interval
                while not stop and time.monotonic()<deadline:time.sleep(max(0,min(1,deadline-time.monotonic())))
                if stop:break
                row=reader.sample(identity)
        except ProcessEnded as e:reason=str(e)
        except Exception as e:reason='monitor_error: '+str(e)
        finally:
            s.close(reason)
            for n,handler in previous.items():signal.signal(n,handler)
        print('Ended:',reason,flush=True)
    finally:root.close()

def control(args):
    s=owned_session(args.session);meta=read_json(s/'session.json')
    if meta['state']!='RUNNING':raise ValueError('Session already ended')
    if args.action=='mark':append_tsv(s/'markers.tsv',[utc(),args.text[:200]],EVENT_CAP);return
    req=no_links(s/'request.json')
    with req.open('x') as f:json.dump({'kind':'stop' if args.action=='stop' else args.kind,'timestamp_utc':utc()},f)
    print('Queued for next sample boundary (normally30s; diagnostic tools may delay it). Ctrl+C also stops the monitor.')

def main():
    p=argparse.ArgumentParser(description=__doc__);subs=p.add_subparsers(dest='action',required=True)
    q=subs.add_parser('start');q.add_argument('--pid',type=int);q.add_argument('--build',required=True);q.add_argument('--interval',type=float,default=30);q.add_argument('--log-dir',type=Path,default=ROOT);q.add_argument('--auto-snapshots',choices=['off','vmmap','footprint'],default='off')
    for action in ('mark','capture','stop'):
        q=subs.add_parser(action);q.add_argument('--session',type=Path,required=True)
        if action=='mark':q.add_argument('text')
        if action=='capture':q.add_argument('kind',choices=tuple(TOOLS))
    a=p.parse_args()
    try:
        if a.action=='start':
            if not 10<=a.interval<=3600 or not math.isfinite(a.interval):p.error('interval must be10–3600 seconds')
            if a.pid is not None and a.pid<=0:p.error('pid must be positive')
            if len(a.build)>80:p.error('build label too long')
            run(a)
        else:control(a)
    except (ValueError,OSError,ProcessEnded,subprocess.SubprocessError) as e:p.exit(1,str(e)+'\n')
if __name__=='__main__':main()
