from pathlib import Path
from lupa.lua55 import LuaRuntime
R=Path(__file__).resolve().parents[1];M=R/'Mod'
s=(R/'DevelopmentTests/test_b063_inheritance_read.py').read_text().replace('89','90')
exec(compile(s,__file__,'exec'))
l=LuaRuntime(unpack_returned_tuples=True)
l.execute('''
table.unpack=nil;unpack=nil
function cp(x) if type(x)~='table' then return x end local r={} for k,v in pairs(x) do r[k]=cp(v) end return r end
store={};writes=0;owner=0;cid=11;alive=true;fail=false
props={SPC_DEV_BINDING_B013_TOKEN='u1',SPC_DEV_CITY_JOURNAL_B015={specialization='INDUSTRY'},SPC_DEV_INVESTMENT_LEDGER_V1={investments={a='x',b='y',c='z'}},SPC_STANDARDIZATION_LEDGER_V1={learned={b1=true,b2=true,b3=true,b4=true,b5=true,b6=true}}}
city={GetOwner=function() return owner end,GetID=function() return cid end,GetX=function() return 4 end,GetY=function() return 5 end,GetProperty=function(_,k) return props[k] end,SetProperty=function() error('FORBIDDEN_CITY_WRITE') end}
P={IsTestPlayer=function(p) return p==0 end}
function resetHooks() Events={};GameEvents={};for _,ns in ipairs({Events,GameEvents}) do setmetatable(ns,{__index=function(t,k) local h={};local e={Add=function(f) h[#h+1]=f end,Fire=function(...) for _,f in ipairs(h) do f(...) end end};rawset(t,k,e);return e end}) end end
resetHooks();Game={GetCurrentGameTurn=function() return 1 end,GetProperty=function(_,k) return cp(store[k]) end,SetProperty=function(_,k,v) assert(not fail,'DB_FAIL');store[k]=cp(v);writes=writes+1 end}
CityManager={GetCityAt=function() return alive and city or nil end}
Players={[0]={GetCities=function() return {Members=function() return ipairs(owner==0 and {city} or {}) end} end}}
shared={BindingProbe={Resolve=function(pid,c) return props.SPC_DEV_BINDING_B013_TOKEN,props.SPC_DEV_BINDING_B013_TOKEN and 'BOUND_MATCH' or 'PARTIAL' end}}
''')
l.execute((M/'InheritanceShadow.lua').read_text())
l.execute('''
SPCInheritanceShadow.Start(P,shared);Events.LoadScreenClose.Fire();local d=shared.InheritanceShadow
assert(writes==1);assert(d.Select(0,city):find('投资=3 | 模板=6'));local n=writes
for i=1,100 do d.Describe(0);d.Capture(city,'SAME') end assert(writes==n)
props.SPC_DEV_INVESTMENT_LEDGER_V1.pending={stage='INTENT'};shared.OnPermanentCityWrite(city,'intent');assert(d.Describe(0):find('pending=INTENT'))
props.SPC_DEV_INVESTMENT_LEDGER_V1.pending.stage='CONSUMED_CONFIRMED';shared.OnPermanentCityWrite(city,'debit');assert(d.Describe(0):find('pending=CONSUMED_CONFIRMED'))
props.SPC_DEV_INVESTMENT_LEDGER_V1.pending=nil;shared.OnPermanentCityWrite(city,'commit')
owner=1;cid=99;props={};Events.CityRemovedFromMap.Fire(0,11);Events.CityAddedToMap.Fire(1,99,4,5);GameEvents.CityConquered.Fire(1,0,99,4,5)
assert(d.Describe(0):find('投资=3 | 模板=6'));assert(d.Describe(0):find('当前=1/99'));assert(d.Describe(0):find('TOKEN 备份=有 当前=无'))
Events.CityTransfered.Fire(1,99,nil,false,0);local e=store[SPCInheritanceShadow.KEY].events[#store[SPCInheritanceShadow.KEY].events];assert(e.args=='1,99,nil,false,0')
local original=cp(store);resetHooks();SPCInheritanceShadow.Start(P,shared);Events.LoadScreenClose.Fire();d=shared.InheritanceShadow;assert(d.Describe(0):find('投资=3 | 模板=6'))
assert(store[SPCInheritanceShadow.KEY].revision==original[SPCInheritanceShadow.KEY].revision)
for i=1,40 do Events.CityAddedToMap.Fire(1,99,4,5) end assert(#store[SPCInheritanceShadow.KEY].events==24)
local n=writes;for i=1,100 do Events.CityAddedToMap.Fire(8,88,8,8);Events.PlayerTurnActivated.Fire();Events.SystemUpdateUI.Fire() end assert(writes==n)
alive=false;Events.CityRemovedFromMap.Fire(1,99);assert(d.Describe(0):find('原位置当前=无城市'));assert(d.Describe(0):find('投资=3'))
alive=true;owner=0;cid=55;props={SPC_DEV_BINDING_B013_TOKEN='u2'};shared.OnPermanentCityWrite(city,'NEW_FOUNDATION');assert(store[SPCInheritanceShadow.KEY].records.u1.values.INVEST.investments.a=='x');assert(store[SPCInheritanceShadow.KEY].records.u2.values.INVEST==nil)
fail=true;props.SPC_DEV_CITY_JOURNAL_B015={specialization='RESEARCH'};shared.OnPermanentCityWrite(city,'FAIL');assert(d.errors.last:find('SHADOW_CALLBACK_ERROR'));assert(store[SPCInheritanceShadow.KEY].records.u2.values.JOURNAL==nil)
assert(not pcall(d.Describe,1))
''')
print('B064 LOCAL_SIMULATION_PASS: Game shadow retains full receipts/templates after city loss and reload, pending stages, idempotence, bounded logs, no idle scans/writes, no adoption at rebuilt plot, safe failed backup; prior gameplay and D0025 model/SQL regression pass.')
