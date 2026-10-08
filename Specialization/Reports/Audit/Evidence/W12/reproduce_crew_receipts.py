"""Audit-only current Crew action, mocked native queue/Properties and explicit faults.
No historical test cases, repository mutation, game, database or deployment.
"""
from pathlib import Path
import argparse, hashlib, json
from lupa.lua55 import LuaRuntime
p=argparse.ArgumentParser(description=__doc__);p.add_argument('--repo',type=Path,required=True);p.add_argument('--output',type=Path,required=True)
a=p.parse_args();root=a.repo.resolve()
LUA=r'''
local function cp(v)if type(v)~='table'then return v end;local c={};for k,x in pairs(v)do c[k]=cp(x)end;return c end
local function ev()local v={list={}};v.Add=function(f)v.list[#v.list+1]=f end;v.Fire=function(...)for _,f in ipairs(v.list)do f(...)end end;return v end
Events={UnitRemovedFromMap=ev()};Game={GetCurrentGameTurn=function()return 10 end}
GameInfo={GameSpeeds={STANDARD={CostMultiplier=100}},Units={[7]={UnitType='UNIT_SPC_CREW_250'}},Buildings={BUILDING_A={Index=1}}}
GameConfiguration={GetGameSpeedType=function()return 'STANDARD'end}
local stores={};local units={};local destroys,grants,writes,passed=0,0,0,0
local q={progress=0,cost=500,target='BUILDING_A'}
q.CurrentlyBuilding=function()return q.target end
q.AddProgress=function(_,amount)grants=grants+1;q.progress=q.progress+amount end
local c={GetOwner=function()return 0 end,GetID=function()return 8 end,GetX=function()return 1 end,GetY=function()return 1 end,GetBuildQueue=function()return q end}
local collections={FindID=function(_,id)return units[id]end,Destroy=function(_,u)destroys=destroys+1;units[u:GetID()]=nil;Events.UnitRemovedFromMap.Fire(0,u:GetID())end}
Players={[0]={GetUnits=function()return collections end,GetCities=function()return {FindID=function(_,id)if id==8 then return c end end}end}}
Players[0].GetProperty=function(_,k)return cp(stores[k])end
Players[0].SetProperty=function(_,k,v)
 writes=writes+1;local n=0;for _ in pairs(v)do n=n+1 end;passed=passed+n
 if MODE=='SILENT_DROP_ALL' then return end
 if MODE=='THROW_INTENT' then error('AUDIT_INTENT_WRITE_THROW')end
 stores[k]=cp(v)
end
Map={GetPlot=function()return {GetIndex=function()return 10 end}end}
ExposedMembers={DLHD={Utils={GetCityCurrentBuildQueueCost=function()return q.cost end,GetCityCurrentBuildQueueProgress=function()return q.progress end}}}
local P=SPCP0;P.IsTestPlayer=function(pid)return pid==0 end;P.Count=function()end
P.Info=function(t,k)return GameInfo[t] and GameInfo[t][k] end
local shared={UnitTargets={}}
-- Lua closure captures the same table used by current handlers.
shared.UnitTargets.Refresh=function()shared.UnitTargetSnapshot={plots={{plot=10,cityID=8}}}end
SPCConstructionProbe.Start(P,shared);SPCUnitActions.Start(P,shared)
local last
for i=1,N do
 local up={};local id=i
 units[id]={GetID=function()return id end,GetOwner=function()return 0 end,GetType=function()return 7 end,
 GetBuildCharges=function()return 1 end,GetX=function()return 1 end,GetY=function()return 1 end,
 GetProperty=function(_,k)return up[k]end,SetProperty=function(_,k,v)up[k]=v end}
 q.progress=0
 local prepared=shared.UnitActions.Run(0,{Action='UNIT_ACTION_PREPARE',UnitID=id,Token='R'..i});assert(prepared:find('PREPARED'),prepared)
 last=shared.UnitActions.Run(0,{Action='UNIT_ACTION_CONFIRM',UnitID=id,Token='CONFIRM'..i,PlanToken='R'..i})
 if MODE=='THROW_INTENT' then assert(last:find('HELD') and destroys==0 and grants==0)
 else assert(last:find('CREW CONSUMED') and q.progress==250 and destroys==i and grants==i,last)end
 local d,g=destroys,grants;shared.UnitActions.Run(0,{Action='UNIT_ACTION_CONFIRM',UnitID=id,Token='REPEAT'..i});assert(destroys==d and grants==g)
end
local count=0;for _ in pairs(stores.SPC_CREW_ACTION_RECEIPTS_V1 or {})do count=count+1 end
if MODE=='SILENT_DROP_ALL' then assert(count==0 and writes==3*N and destroys==N and grants==N)
elseif MODE=='THROW_INTENT' then assert(count==0 and writes==N)
else assert(count==N and writes==3*N and passed==3*N*(N+1)/2)end
result={mode=MODE,actions=N,persisted_receipts=count,receipt_setter_calls=writes,
 cumulative_receipt_entries_passed=passed,unit_consumptions=destroys,grant_calls=grants,
 final_message=last:match('^[^\n]+'),repeat_grants=0}
'''
def run(mode,n):
 lua=LuaRuntime(unpack_returned_tuples=True);lua.execute('print=function()end')
 lua.globals().include=lambda name:lua.execute((root/'Mod'/f'{name}.lua').read_text())
 for name in ['Probe','ConstructionProbe','UnitActions']:lua.execute((root/'Mod'/f'{name}.lua').read_text())
 lua.globals().MODE=mode;lua.globals().N=n;lua.execute(LUA)
 return {k:v for k,v in lua.globals().result.items()}
r={'evidence':'LOCAL_STRUCTURAL_REPRODUCTION','source':{n:hashlib.sha256((root/n).read_bytes()).hexdigest() for n in ['Mod/Probe.lua','Mod/PerformanceCounters.lua','Mod/ConstructionProbe.lua','Mod/UnitActions.lua']},
 'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
 'limits':['Native queue, units, HD readers and deep-copy Player Property are explicit mocks.',
 'Silent-drop/throw are injected, not observed native faults; no zero-overflow or engine multiplier claim.',
 'Entries passed describe full-map setter payload shape, not measured Lua allocation, serialization or native time.'],
 'fault_cases':[run('NORMAL',1),run('SILENT_DROP_ALL',1),run('THROW_INTENT',1)],
 'history_cases':[run('NORMAL',n) for n in [1,8,64]]}
a.output.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n');print(json.dumps(r,ensure_ascii=False,indent=2))
