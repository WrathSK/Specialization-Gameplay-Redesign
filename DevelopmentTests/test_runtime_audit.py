"""Actual Lua logger/counters/UI observer; filesystem only inside TemporaryDirectory."""
from pathlib import Path
import tempfile, csv, io as pyio, xml.etree.ElementTree as ET
from lupa.lua55 import LuaRuntime
R=Path(__file__).resolve().parents[1];M=R/'Mod'
def runtime():
 l=LuaRuntime(unpack_returned_tuples=True)
 l.execute("turn=1;Game={GetCurrentGameTurn=function() return turn end};ExposedMembers={}")
 for name in ('PerformanceCounters','RuntimeAuditCore'):l.execute((M/(name+'.lua')).read_text())
 l.execute("c=SPCPerformance.New();ExposedMembers.SPC_Performance=c;opts={turn=1,build='B072.99',modinfo=99,start=123,sourceBase='407717c'};info={elapsed=0,player=0,cities=4,routes=3,inputRevision=2,derivedRevision=2,validity='VERIFIED',networkPlayers=1,networkInputs=1,diagnosticEntries=2}")
 l.execute("function nodes(t) local n=1;for _,v in pairs(t) do n=n+1;if type(v)=='table' then n=n+nodes(v) end end;return n end")
 return l
with tempfile.TemporaryDirectory() as tmp:
 l=runtime();l.globals().directory=tmp
 l.execute("sink=SPCRuntimeAudit.FileSink(io,directory);audit=SPCRuntimeAudit.New(c,sink,opts);assert(audit.state=='ACTIVE');initialNodes=nodes(audit)+nodes(c);initialWrites=sink.writes")
 l.execute("for i=1,1000000 do SPCPerformance.Count('unit_cb') end;assert(sink.writes==initialWrites);assert(nodes(audit)+nodes(c)==initialNodes)")
 l.execute("assert(audit.EndTurn(1,c,info));assert(not audit.EndTurn(1,c,info));steadyNodes=nodes(audit)+nodes(c)")
 l.execute("for t=2,10000 do turn=t;for k in pairs(c.entries) do SPCPerformance.Count(k,1000000) end;assert(audit.EndTurn(t,c,info));assert(nodes(audit)+nodes(c)==steadyNodes) end")
 assert l.eval('audit.rows')==10000
 assert l.eval('sink.serial')>1
 files=list(Path(tmp).glob('*.tsv'));assert len(files)<=8
 assert max(p.stat().st_size for p in files)<=4*1024*1024
 print('10k stress bytes=',sum(p.stat().st_size for p in files),'segments=',l.eval('sink.serial'),'retained_nodes=',l.eval('nodes(audit)+nodes(c)'))
 # Only nine owned files can exist; rotate across more than eight sessions.
 l.execute("for i=1,12 do local s=SPCRuntimeAudit.FileSink(io,directory);local a=SPCRuntimeAudit.New(c,s,opts);assert(a.state=='ACTIVE');assert(a.EndTurn(10001,c,info)) end")
 assert len(list(Path(tmp).iterdir()))==9
 assert sum(p.stat().st_size for p in Path(tmp).glob('*.tsv'))<=8*4*1024*1024
 print('PASS: 1,000,000 callbacks zero I/O; 10,000 summaries fixed nodes, rotation; 12 additional sessions retention <=8 files')
# Once-per-turn anomaly counts, disabled failures, unavailable fields.
l=runtime();l.execute("sink={serial=0,writes=0,text=''};sink.Rotate=function(h) sink.serial=sink.serial+1;sink.header=h(sink.serial) end;sink.Append=function(t) sink.writes=sink.writes+1;sink.text=t end;audit=SPCRuntimeAudit.New(c,sink,opts);SPCPerformance.Count('derive_executed',300);SPCPerformance.Count('building_create',300);info.elapsed=nil;assert(audit.EndTurn(1,c,info));assert(not audit.EndTurn(1,c,info));assert(sink.writes==1)")
fields=list(csv.DictReader(pyio.StringIO(l.eval('sink.header').split('\n',1)[1]+l.eval('sink.text')),delimiter='\t'))[0]
assert fields['elapsed_seconds']=='NA' and fields['derive_executed_interval']=='300'
assert fields['anomalies'].count('DERIVE_HIGH')==1
l.execute("sink.Append=function() sink.writes=sink.writes+1;error('disk full') end;turn=2;assert(not audit.EndTurn(2,c,info));assert(audit.state=='DISABLED');local w=sink.writes;for t=3,10000 do audit.EndTurn(t,c,info) end;assert(w==sink.writes)")
# UI observer uses native event pattern, no calls into Gameplay. Native io is NOT assumed available.
def ui(capable):
 l=runtime();l.globals().include=lambda n:l.execute((M/(n+'.lua')).read_text())
 l.execute("callbacks={};Events={};for _,n in ipairs({'LoadScreenClose','LocalPlayerTurnEnd'}) do Events[n]={Add=function(f) callbacks[n]=f end,Remove=function(f) callbacks[n]=nil end} end;ContextPtr={SetShutdown=function(_,f) shutdown=f end};Game.GetLocalPlayer=function() return 0 end;Players={[0]={GetCities=function() return {GetCount=function() return 4 end} end}};ExposedMembers.SPC_P0={Events={'one'},NetworkBridge={players={[0]={routes={},inputRevision=1,derivedRevision=1,validity='VERIFIED',input={}}}}}")
 if not capable:l.execute('io=nil;os=nil')
 else:
  # Capability-backed mock avoids writing the actual Mac log path.
  l.execute("openCount=0;mockData={};io={open=function(path,mode) openCount=openCount+1;if mode=='rb' then return nil end;return {write=function(_,s) mockData.last=s;return true end,close=function() return true end} end};os={getenv=function() return '/test-home' end,time=function() return 123 end}")
 l.execute((M/'UI/RuntimeAudit.lua').read_text());l.execute("callbacks.LoadScreenClose();callbacks.LocalPlayerTurnEnd()")
 return l
l=ui(False);assert l.eval('ExposedMembers.SPC_RuntimeAudit.state')=='DISABLED'
l.execute("for i=1,10000 do callbacks.LocalPlayerTurnEnd() end;assert(ExposedMembers.SPC_Performance.entries.derive.total==0)")
l=ui(True);assert l.eval('ExposedMembers.SPC_RuntimeAudit.rows')==1
l.execute("local n=openCount;for i=1,10000 do callbacks.LocalPlayerTurnEnd() end;assert(openCount==n);for _,e in pairs(c.entries) do assert(e.total==0) end;assert(ExposedMembers.SPC_P0.NetworkBridge.players[0].inputRevision==1);shutdown();assert(next(callbacks)==nil)")
# Logging ON and OFF observe identical simulation facts/counters; no reads cause audits.
a,b=ui(True),ui(False)
for l in (a,b):l.execute("for t=2,100 do turn=t;SPCPerformance.Count('unit_cb',10);callbacks.LocalPlayerTurnEnd() end")
for key in a.eval('c.entries').keys():assert a.eval('c.entries')[key]['total']==b.eval('c.entries')[key]['total']
print('PASS: missing metrics, anomaly dedup, write failure disables without retry; ON/OFF counters/facts equal; observer shutdown; absent native file capability explicit DISABLED')
# Syntax/manifest and static isolation.
for p in M.rglob('*.lua'):runtime_l=LuaRuntime();runtime_l.execute('assert(load(...))',p.read_text())
x=ET.parse(M/'SpecializationP0.modinfo').getroot();assert x.get('version')=='99'
for node in x.findall('.//File'):assert (M/node.text).is_file(),node.text
s=(M/'UI/RuntimeAudit.lua').read_text()
for bad in ('RequestPlayerOperation','SetProperty','CreateBuilding','SetUpdate','.Audit(','.National(','.Rebuild('):assert bad not in s
print('PASS: all Lua syntax, manifest references, no periodic UI update or Gameplay requests/writes')
