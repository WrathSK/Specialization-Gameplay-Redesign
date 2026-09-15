"""B072 entry: unchanged A/B/B069 behavior assertions, current stamp only."""
from pathlib import Path
R=Path(__file__).resolve().parents[1]
ns={'__file__':str(R/'DevelopmentTests/test_arch_v2_batch_b.py')}
s=(R/'DevelopmentTests/test_arch_v2_batch_b.py').read_text().replace("get('version')=='98'", "get('version')=='99'")
exec(compile(s,ns['__file__'],'exec'),ns)
a,b=ns['runtime'](),ns['runtime']()
for l in (a,b):
 l.execute((R/'Mod/RuntimeAuditCore.lua').read_text())
 l.execute("send('0,1,0,2,10;0,2,0,3,11',2)")
 l.execute("auditSink={Rotate=function(h) h(1) end,Append=function() end};audit=SPCRuntimeAudit.New(ExposedMembers.SPC_Performance,auditSink,{turn=1,build='B072.99',modinfo=99});info={}")
b.execute("audit.Fail('OFF')")
for turn in range(1,21):
 for l in (a,b):
  l.execute(f"turn={turn};cities[1].active={turn%4+1};net.Rebuild();audit.EndTurn(turn,ExposedMembers.SPC_Performance,info)")
 assert a.eval('fullOutput()')==b.eval('fullOutput()')
 assert a.eval('writes')==b.eval('writes') and a.eval('propertyWrites')==b.eval('propertyWrites')
 assert a.eval('encode(ExposedMembers.SPC_Performance.entries)')==b.eval('encode(ExposedMembers.SPC_Performance.entries)')
print('PASS: real Batch B bridge output, engine writes, property writes and all counters identical with logging ON/OFF over 20 input transitions')
