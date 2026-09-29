"""Explicit full-GC diagnostic contract; Lua mock evidence, never native heap proof."""
from pathlib import Path
from lupa.lua55 import LuaRuntime
import xml.etree.ElementTree as ET
R=Path(__file__).resolve().parents[1]
l=LuaRuntime(unpack_returned_tuples=True)
l.execute('''
turn=40;Game={GetCurrentGameTurn=function()return turn end};ExposedMembers={}
function event()local e={fs={}};e.Add=function(f)e.fs[#e.fs+1]=f end;e.Fire=function(...)for _,f in ipairs(e.fs)do f(...)end end;return e end
Events={PlayerTurnActivated=event(),PlayerTurnDeactivated=event(),CityTransfered=event(),GameCoreEventPublishComplete=event()}
P={IsTestPlayer=function(p)return p==0 end,Field=function(o,k)return o[k]end,VERSION='P0-B-134.161',Scalar=tostring}
SPCP0=P;shared={};calls={};heap=204800;gcRunning=true;clock=0
os={clock=function()clock=clock+0.25;return clock end}
function gc(mode)
 calls[#calls+1]=mode
 if mode=='count' then return heap end
 if mode=='isrunning' then return gcRunning end
 assert(mode=='collect','strategy mutation forbidden')
 heap=102400;return 0
end
collectgarbage=gc
''')
l.execute((R/'Mod/PerformanceCounters.lua').read_text())
l.execute('''
SPCPerformance.StartMemory(P,shared);d=shared.MemoryObservation
for i=1,3 do
 Events.PlayerTurnActivated.Fire(0);Events.PlayerTurnDeactivated.Fire(0)
 Events.CityTransfered.Fire(0,4,3);Events.GameCoreEventPublishComplete.Fire()
end
assert(#calls==0)
assert(d.ReadGC(0):find('默认关闭'));assert(#calls==0)
assert(d.CollectGC(2,'foreign'):find('仅本地'));assert(#calls==0)
assert(d.CollectGC(0,''):find('无效'));assert(#calls==0)
local s=d.CollectGC(0,'one')
assert(s:find('200.00 → 100.00 MiB') and s:find('0.250秒') and s:find('运行 → 运行'))
assert(s:find('\\n') and not s:find('\\\\n'));assert(#calls==5)
assert(d.CollectGC(0,'one')==s and #calls==5) -- immediate duplicate cannot collect twice
assert(d.ReadGC(0)==s and #calls==5) -- read does not sample or collect
local n=#calls;for i=1,3 do Events.PlayerTurnActivated.Fire(0);Events.GameCoreEventPublishComplete.Fire()end;assert(#calls==n)
-- Observer remains count-only, GC is never piggybacked on its events.
d.Read(0,true);Events.PlayerTurnActivated.Fire(0);Events.GameCoreEventPublishComplete.Fire()
for i=n+1,#calls do assert(calls[i]=='count')end
-- Fixed three rows; no saved ledger. More samples explicitly requested by user.
for i=2,5 do turn=turn+1;heap=heap+1024;d.CollectGC(0,'manual'..i)end
s=d.ReadGC(0);local _,rows=s:gsub('完整GC调用成功','');assert(rows==3)
assert(not s:find('T40 ') and s:find('T44 '))
-- Stopped collector is observed; never restarted or tuned.
SPCPerformance.StartMemory(P,shared);gcRunning=false;heap=204800
assert(shared.MemoryObservation.CollectGC(0,'stopped'):find('停止 → 停止'));assert(not gcRunning)
-- Runtime capability/method failure: one attempt, bounded error, no automatic retry.
SPCPerformance.StartMemory(P,shared);d=shared.MemoryObservation
collectgarbage=function(mode)if mode=='count' then return 1024 end;if mode=='isrunning'then error('unsupported')end;error('collect unavailable')end
s=d.CollectGC(0,'fail');assert(s:find('调用失败') and s:find('collect unavailable'))
collectgarbage=function()error('must not retry')end
assert(d.CollectGC(0,'retry')==s)
-- Missing count: no destructive/control call at all.
SPCPerformance.StartMemory(P,shared);d=shared.MemoryObservation;collectgarbage=nil
assert(d.CollectGC(0,'missing'):find('count接口不可用'))
-- Optional timing/status absent; collect still has usable before/after counts.
SPCPerformance.StartMemory(P,shared);d=shared.MemoryObservation;os=nil;heap=204800
collectgarbage=function(mode)if mode=='isrunning'then error('no status')end;return gc(mode)end
s=d.CollectGC(0,'optional');assert(s:find('调用成功') and s:find('CPU耗时 不可用') and s:find('未知 → 未知'))
-- A successful call may increase heap (finalizers/other allocations); preserve the observation.
SPCPerformance.StartMemory(P,shared);d=shared.MemoryObservation
collectgarbage=function(mode)if mode=='count'then return heap elseif mode=='isrunning'then return true end;heap=heap+1024 end
s=d.CollectGC(0,'increase');assert(s:find('100.00 → 101.00 MiB'))
-- Unexpected state change stops diagnostic; do not silently repair engine state.
SPCPerformance.StartMemory(P,shared);d=shared.MemoryObservation;gcRunning=true
collectgarbage=function(mode)if mode=='count'then return 1024 elseif mode=='isrunning'then return gcRunning end;gcRunning=false end
assert(d.CollectGC(0,'changed'):find('运行状态改变'));assert(not gcRunning)
-- New load resets only diagnostic samples; prior saved authority is untouched.
shared.savedAuthority={identity='RESEARCH',potential=3,receipts=2}
SPCPerformance.StartMemory(P,shared)
assert(shared.MemoryObservation.ReadGC(0):find('默认关闭') and shared.savedAuthority.receipts==2)
''')
# Execute the actual early Gameplay request closure, before any gameplay action.
s=(R/'Mod/Gameplay.lua').read_text()
prefix=s[:s.index("  if params.Action=='CLAIM_BEGIN'")]
l.execute('include=function()end;print=function()end')
l.execute(prefix+'\nend\nrequestGC=request;requestShared=shared')
l.execute('''
collectgarbage=gc;os=nil;heap=204800;gcRunning=true;calls={}
SPCPerformance.StartMemory(P,requestShared)
requestGC(0,{Action='MEMORY_GC_READ',Token='read'})
assert(requestShared.LastToken=='read' and #calls==0)
requestGC(0,{Action='MEMORY_GC_COLLECT',Token='collect'})
assert(requestShared.LastToken=='collect' and requestShared.Snapshot:find('200.00 → 100.00'))
local n=#calls;requestGC(0,{Action='MEMORY_GC_COLLECT',Token='collect'});assert(#calls==n)
requestGC(2,{Action='MEMORY_GC_COLLECT',Token='foreign'});assert(#calls==n)
requestShared.MemoryObservation=nil
requestGC(0,{Action='MEMORY_GC_COLLECT',Token='notready'})
assert(requestShared.Snapshot:find('GC诊断不可用') and #calls==n)
''')
# Direct caller/automatic-control boundaries plus syntax, not a screenshot/layout claim.
perf=(R/'Mod/PerformanceCounters.lua').read_text()
assert perf.count("pcall(collectgarbage,'collect')")==1
assert all("collectgarbage,'"+x+"'" not in perf for x in ('stop','restart','setpause','setstepmul','step','incremental','generational'))
ui=(R/'Mod/UI/P0Panel.lua').read_text()
assert "Mouse.eRClick,function()request('MEMORY_GC_COLLECT')" in ui
assert "Mouse.eLClick,function()request('MEMORY_GC_READ')" in ui
assert "local storageAction=action=='MEMORY_GC_READ' or action=='MEMORY_GC_COLLECT'" in ui
assert "if action:find('^GWA_') then gwaFlight=" in ui # no diagnostic resend machinery
assert "'MEMORY_GC' or ((pendingAction" in ui # bounded, city-independent result cache
for name in ['PerformanceCounters.lua','Gameplay.lua','NetworkBridge.lua','UI/P0Panel.lua','Probe.lua']:
 l.execute('assert(load(...))',(R/'Mod'/name).read_text())
assert ET.parse(R/'Mod/SpecializationP0.modinfo').getroot().get('version')=='161'
print('PASS: manual-only GC; no event/read/foreign/duplicate collection; bounded results; unsupported/failure/no-retry; optional CPU/status; stopped/state-change handling; actual early request path; changed Lua syntax/modinfo161. Native GC semantics/timing remain unverified.')
