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
a=SPCRuntimeAudit.New(c,sink,{turn=26,build='B131.158',modinfo=158});assert(a.state=='ACTIVE');assert(#a.names==94)
assert(a.EndTurn(26,c,{}));assert(not a.EndTurn(26,c,{}));assert(#text<16384)
sink.Append=function()error('disk full')end;assert(not a.EndTurn(27,c,{}));assert(a.state=='DISABLED')
local invalid={entries={}};for i=1,129 do invalid.entries['x'..i]={total=0}end;assert(not pcall(SPCRuntimeAudit.New,invalid,sink,{turn=26}))
""")
for f in ['PerformanceCounters.lua','Gameplay.lua','CityProgressionStore.lua','RuntimeAuditCore.lua','UI/RuntimeAudit.lua','UI/P0Panel.lua','Probe.lua']:
 l.execute('assert(load(...))',(R/'Mod'/f).read_text())
assert ET.parse(R/'Mod/SpecializationP0.modinfo').getroot().get('version')=='158'

# Actual observer, actual event wrapper and actual UI producer; no engine effects.
l.execute('collectgarbage=function(mode)assert(mode=="count");return 10240 end; shared.MemoryObservation.Read(0,true)')
l.execute('''
local a=ExposedMembers.SPC_MemoryAttribution
assert(a.audit.ResearchChair==0)
SPCPerformance.Observe('audit','ResearchChair');SPCPerformance.Observe('audit','ResearchChair')
SPCPerformance.Observe('audit','unknown');SPCPerformance.Observe('unknown','ResearchChair')
assert(a.audit.ResearchChair==2 and a.audit.unknown==nil and a.unknown==nil)
SPCPerformance.Count('dc_capture',3);SPCPerformance.Count('dc_hit',2)
local text=shared.MemoryObservation.Read(0,false)
assert(text:find('学术主持 2') and text:find('重建 3') and text:find('命中 2'))
assert(not text:find('独立context'))
P.Observe=SPCPerformance.Observe;P.Info=function()return {BuildingType='BUILDING_LIBRARY'}end
Events.CityWorkerChanged=event();Events.DistrictBuildProgressChanged=event();Events.BuildingAddedToMap=event()
scopeCalls=0
''')
l.execute((R/'Mod/RuntimeWork.lua').read_text())
l.execute('''
SPCRuntimeWork.Hook(P,Events,'CityWorkerChanged',function(s)scopeCalls=scopeCalls+1;assert(s.player==3 and s.cityID==nil)end)
for i=1,3 do Events.CityWorkerChanged.Fire(3,17)end
assert(scopeCalls==3 and ExposedMembers.SPC_MemoryAttribution.dispatch.CityWorkerChanged==3)
SPCRuntimeWork.Hook(P,Events,'DistrictBuildProgressChanged',function(s)assert(s==nil)end)
Events.DistrictBuildProgressChanged.Fire(3,17)
SPCRuntimeWork.Hook(P,Events,'PlayerTurnActivated',function(s)assert(s.player==0)end)
Events.PlayerTurnActivated.Fire(0);Events.PlayerTurnActivated.Fire(0)
assert(ExposedMembers.SPC_MemoryAttribution.dispatch.PlayerTurnActivated==1)
local a=ExposedMembers.SPC_MemoryAttribution
SPCRuntimeWork.Hook(P,Events,'BuildingAddedToMap',function()error('carrier feedback')end)
P.Info=function()return {BuildingType='BUILDING_SPC_X'}end
Events.BuildingAddedToMap.Fire(1,2,3,0)
assert(a.dispatch.BuildingAddedToMap==0)
include=function()end;SPCP0=P;P.VERSION='TEST'
Game.GetLocalPlayer=function()return 0 end
ExposedMembers.SPC_P0={Version='TEST',Lv2GPP={ready=true}}
PlayerOperations={EXECUTE_SCRIPT=1};sent=0
UI={RequestPlayerOperation=function(pid,op,params)assert(pid==0 and params.Action=='LV2_GPP_DIRTY');sent=sent+1;lastParams=params;SPCPerformance.Observe('ui','received')end}
Events=setmetatable({},{__index=function(t,k)local e=event();rawset(t,k,e);return e end})
ContextPtr={SetInitHandler=function(self,f)initialize=f end,SetShutdown=function()end}
''')
l.execute((R/'Mod/UI/GPPRefresh.lua').read_text())
l.execute('''
initialize()
shared.MemoryObservation.Read(0,true)
local a=ExposedMembers.SPC_MemoryAttribution;sent=0
Events.CityWorkerChanged.Fire(3,17);Events.CityWorkerChanged.Fire(0,18);Events.CityWorkerChanged.Fire(nil,18)
assert(a.ui.worker_foreign==1 and a.ui.worker_local==1 and a.ui.worker_unknown==1)
Events.GameCoreEventPublishComplete.Fire()
assert(sent==1 and a.ui.send==1 and a.ui.sent==1 and a.ui.received==1 and lastParams.FactsChanged==false)
Events.GameCoreEventPlaybackComplete.Fire();Events.SystemUpdateUI.Fire();assert(sent==1)
Events.GovernorChanged.Fire(3);Events.GameCoreEventPublishComplete.Fire()
assert(a.ui.governor_foreign==1 and sent==2 and lastParams.FactsChanged==true)
UI.RequestPlayerOperation=function()error('request unavailable')end
Events.CityFocusChanged.Fire(0);Events.GameCoreEventPublishComplete.Fire()
assert(a.ui.focus_local==1 and a.ui.failed==1)
local before=a.audit.ResearchChair
turn=turn+6;SPCPerformance.Observe('audit','ResearchChair')
assert(not a.active and a.audit.ResearchChair==before)
assert(shared.MemoryObservation.Read(0,false):find('已停止'))
shared.MemoryObservation.Read(0,true)
assert(ExposedMembers.SPC_MemoryAttribution~=a and ExposedMembers.SPC_MemoryAttribution.ui.sent==0)
SPCPerformance.StartMemory(P,shared)
assert(ExposedMembers.SPC_MemoryAttribution==nil)
SPCPerformance.Observe('audit','ResearchChair');assert(ExposedMembers.SPC_MemoryAttribution==nil)
''')
# Prove each consumer edit is only an optional diagnostic call; no writer logic edits.
import subprocess
modules=['Lv2Housing','Lv2GPP','ResearchInfrastructure','ResearchCross','ResearchApply','ResearchChair',
         'ResearchSupport','IndustrySupport','Lv3Effects','Lv4Percent','CommerceConvergence',
         'CopyYields','StandardizationDiscount','NetworkBoost','Dialogue']
for name in modules:
    rel=f'Mod/{name}.lua'
    text=(R/rel).read_text()
    # Literal newline, exact one-line-only change relative to deployed B130 source.
    line=f"  if P.Observe then P.Observe('audit','{name}') end"+chr(10)
    assert text.count(line)==1
    old=subprocess.check_output(['git','show',f'0d547ee:{rel}'],cwd=R,text=True)
    assert text.replace(line,'')==old, rel
    l.execute('assert(load(...))',text)
for rel in ['Mod/RuntimeWork.lua','Mod/UI/GPPRefresh.lua']:
    l.execute('assert(load(...))',(R/rel).read_text())
print('PASS: B130 bounded observation checks; fixed attribution schema/reset/expiry; real event scopes/dedup/carrier suppression; UI owner buckets/coalescing/failure and unchanged refresh requests; 15 consumers diagnostic-only; Lua syntax/modinfo158')
