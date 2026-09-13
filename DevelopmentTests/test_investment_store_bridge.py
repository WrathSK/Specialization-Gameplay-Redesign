from pathlib import Path
from lupa.lua55 import LuaRuntime
w=Path(__file__).resolve().parent
l=LuaRuntime(unpack_returned_tuples=True)
for name,file in [('Rules','CitySpecializationState.lua'),('Executor','SettlerInvestmentExecutor.lua'),('Bridge','InvestmentStoreBridge.lua')]:
 l.globals()[name]=l.execute((w/file).read_text())
l.execute('''
local function cp(v) if type(v)~='table' then return v end;local c={};for k,x in pairs(v) do c[k]=cp(x) end;return c end
local id={contextSource='MOCK_ONLY',owner=0,cityUID='B013_TOKEN',present=true,
 eligibility={contextSource='MOCK_ONLY',player=0,status='ENABLED'}}
local base={owner=0,cityID=7,token='B013_TOKEN',specialization='RESEARCH',potential=1,
 health='TRACKING',kind='DEV_FOUNDATION_JOURNAL',first={districtID=3,type='DISTRICT_CAMPUS',turn=4}}
local saved;local writes=0;local live={};local kills=0
local storage={foundation=function() return cp(base) end,read=function() return cp(saved) end,
 write=function(v) writes=writes+1;saved=cp(v) end}
local bridge=Bridge.New(Rules,id,storage)
local io={read=bridge.read,write=bridge.write,validate=function() return true end,
 presence=function(n) return live[n] and 'PRESENT' or 'ABSENT' end,
 consume=function(u) live[u.unitUID]=nil;kills=kills+1 end}
assert(bridge.read().facts.potential==1 and saved==nil and writes==0)
for level=2,4 do
 local u={contextSource='MOCK_ONLY',owner=0,cityUID=id.cityUID,unitType='SETTLER',present=true,unitUID='U'..level}
 live[u.unitUID]=true;local ex=Executor.New(Rules,io)
 local result=ex.Run(id,u,'R'..level);assert(result.status=='READY' and result.potential==level,result.reason)
 assert(base.potential==1 and base.specialization=='RESEARCH')
 assert(saved.potential==nil and saved.specialization==nil and saved.active==nil)
 local n=writes;assert(not ex.Run(id,u,'R'..level).changed and writes==n)
 -- reconstruct bridge/executor as on reload from detached stored record.
 bridge=Bridge.New(Rules,id,storage);io.read=bridge.read;io.write=bridge.write
 assert(Executor.New(Rules,io).Resume(id).potential==level and kills==level-1)
end
local governor={governorGateStatus='KNOWN',owner=0,cityUID=id.cityUID,governorLevelCeiling=4}
assert(bridge.effective(governor).active==4)
governor.governorLevelCeiling=1;assert(bridge.effective(governor).active==1)
assert(bridge.read().facts.potential==4 and base.potential==1)
local n=writes;base.token='OTHER';assert(not pcall(bridge.read));base.token=id.cityUID
base.first.districtID=8;assert(not pcall(bridge.read));base.first.districtID=3
local prior=cp(saved);saved.investments.extra='U4';assert(not pcall(bridge.read));saved=prior
saved.pending={stage='INTENT'};assert(not pcall(bridge.effective,governor));saved.pending=nil
assert(writes==n)
base.specialization='NONE';base.potential=0;assert(not pcall(bridge.read));assert(writes==n)
''')
print('LOCAL_SIMULATION_PASS: real-shaped foundation adapter + executor 1→4, foundation untouched, ledger is sole investment authority, read no migration, reload/replay, ACTIVE demotion, anchor/corrupt/pending rejection. Offline only.')
