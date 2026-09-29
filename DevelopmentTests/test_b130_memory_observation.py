"""Small deterministic observer/94-counter logger tests; no native GC claim."""
from pathlib import Path
from lupa.lua55 import LuaRuntime
import xml.etree.ElementTree as ET
R=Path(__file__).resolve().parents[1];l=LuaRuntime(unpack_returned_tuples=True)
l.execute("""
turn=20;calls=0;Game={GetCurrentGameTurn=function()return turn end};ExposedMembers={}
function event()local e={fs={}};e.Add=function(f)e.fs[#e.fs+1]=f end;e.Fire=function(...)for _,f in ipairs(e.fs)do f(...)end end;return e end
Events={PlayerTurnActivated=event(),PlayerTurnDeactivated=event(),CityTransfered=event(),GameCoreEventPublishComplete=event()}
P={IsTestPlayer=function(p)return p==0 end,Field=function(o,k)return o[k]end}
shared={DistrictCompleteness={CacheSize=function()return 2 end},CityProgressionStore={RecordCount=function()return 12 end}}
collectgarbage=function(mode)assert(mode=='count','GC manipulation prohibited');calls=calls+1;return 10240 end
""")
l.execute((R/'Mod/PerformanceCounters.lua').read_text())
assert l.eval('type(SPCPerformance.Heap)')=='function' # UI can read without starting Gameplay observer
l.execute("""
ExposedMembers.SPC_Performance=SPCPerformance.New();SPCPerformance.StartMemory(P,shared)
Events.PlayerTurnActivated.Fire(0);Events.CityTransfered.Fire(0,10,3);Events.GameCoreEventPublishComplete.Fire();assert(calls==0)
local d=shared.MemoryObservation;assert(d.Read(1,true):find('仅本地'));assert(calls==0)
assert(d.Read(0,true):find('10.00 MiB'));assert(calls==1)
SPCPerformance.Count('building_create',3);Events.PlayerTurnDeactivated.Fire(0);Events.PlayerTurnDeactivated.Fire(0);assert(calls==2)
Events.GameCoreEventPublishComplete.Fire();local n=calls;for i=1,20 do Events.GameCoreEventPublishComplete.Fire()end;assert(calls==n)
Events.CityTransfered.Fire(2,10,3);assert(calls==n)
Events.CityTransfered.Fire(0,10,3);assert(calls==n+1)
for t=21,25 do turn=t;Events.PlayerTurnActivated.Fire(0);Events.PlayerTurnDeactivated.Fire(0);Events.GameCoreEventPublishComplete.Fire()end
local text=d.Read(0,false);local _,rows=text:gsub('10.00 MiB','');assert(rows==6);assert(text:find('建载体 3'));assert(text:find('城市记录 12'))
turn=26;Events.PlayerTurnActivated.Fire(0);n=calls;Events.GameCoreEventPublishComplete.Fire();Events.CityTransfered.Fire(0,99,3);assert(calls==n)
assert(d.Read(0,false):find('已停止'))
collectgarbage=nil;assert(d.Read(0,true):find('不可用'))
collectgarbage=function()error('unavailable')end;assert(d.Read(0,false):find('不可用'))
""")
l.execute((R/'Mod/RuntimeAuditCore.lua').read_text())
l.execute("""
c=ExposedMembers.SPC_Performance;sink={Rotate=function(h)header=h(1)end,Append=function(t)text=t end}
a=SPCRuntimeAudit.New(c,sink,{turn=26,build='B130.157',modinfo=157});assert(a.state=='ACTIVE');assert(#a.names==94)
assert(a.EndTurn(26,c,{}));assert(not a.EndTurn(26,c,{}));assert(#text<16384)
sink.Append=function()error('disk full')end;assert(not a.EndTurn(27,c,{}));assert(a.state=='DISABLED')
local invalid={entries={}};for i=1,129 do invalid.entries['x'..i]={total=0}end;assert(not pcall(SPCRuntimeAudit.New,invalid,sink,{turn=26}))
""")
for f in ['PerformanceCounters.lua','Gameplay.lua','CityProgressionStore.lua','RuntimeAuditCore.lua','UI/RuntimeAudit.lua','UI/P0Panel.lua','Probe.lua']:
 l.execute('assert(load(...))',(R/'Mod'/f).read_text())
assert ET.parse(R/'Mod/SpecializationP0.modinfo').getroot().get('version')=='157'
print('PASS: opt-in only, event/turn dedup, six-row/six-turn bounds, read-only heap capability fallback; 94-counter logging, 129 rejection and I/O failure; syntax/version')
