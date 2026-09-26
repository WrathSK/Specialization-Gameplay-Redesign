"""E2 targeted L3: actual save route + legacy hooks + existing investment executor.
Local mocks prove lifecycle invariants, not Civ VI property persistence or transfer cleanup.
"""
from pathlib import Path
import xml.etree.ElementTree as ET
from lupa.lua55 import LuaRuntime
R=Path(__file__).resolve().parents[1];M=R/'Mod';l=LuaRuntime()
for n in ['CityIdentityRead','CityProgressionStore','BindingProbe','CityJournalProbe','FreshBindingHook','CityFlowProbe','EffectiveFacts','InvestmentAction','NetworkInput']:
 l.execute((M/(n+'.lua')).read_text())
s=(R/'DevelopmentTests/test_p0_e1.py').read_text()
l.execute('M=SPCCityIdentityRead\n'+s[s.index('function fixture()'):s.index('function expect(')])
l.execute(r'''
local function event()local e={list={}};function e.Add(f)e.list[#e.list+1]=f end;function e.Fire(...)for _,f in ipairs(e.list)do f(...)end end;return e end
local function events()return setmetatable({},{__index=function(t,k)local e=event();rawset(t,k,e);return e end})end
local K=SPCCityProgressionStore.KEY
local props,cities,units,writes,cityWrites,kills,governor,fail,writeN
local function mkcity(s)
 local c={s=s}
 function c:GetOwner()return self.s.ref.owner end;function c:GetID()return self.s.ref.cityID end
 function c:GetX()return self.s.ref.x end;function c:GetY()return self.s.ref.y end
 function c:GetProperty(k)for n,key in pairs(M.Keys)do if key==k then return M.Copy(self.s.values[n])end end end
 function c:SetProperty(k,v)cityWrites=cityWrites+1;for n,key in pairs(M.Keys)do if key==k then self.s.values[n]=M.Copy(v);return end end;error('unexpected city key')end
 return c
end
P={VERSION='B098.125',Count=function()end,Field=function(t,k)return t and t[k]end,IsTestPlayer=function(pid)return pid==0 end,
 Families={DISTRICT_CAMPUS='RESEARCH',DISTRICT_THEATER='CULTURE',DISTRICT_INDUSTRIAL_ZONE='INDUSTRY',DISTRICT_COMMERCIAL_HUB='COMMERCE'},
 Rows=function(t)assert(t=='DistrictReplaces');return {}end,
 Info=function(t,k)if t=='Districts' then return {DistrictType=k}end end,
 CityRoleFacts=function(c)return {owner=c:GetOwner(),cityID=c:GetID(),governorGateStatus='KNOWN',governorLevelCeiling=governor}end,
 SetProperty=function(o,k,v)return o:SetProperty(k,v)end}
function boot()
 Events=events();GameEvents=events();shared={}
 SPCity=nil;SPCCityProgressionStore.Start(P,shared);SPCBindingProbe.Start(P,shared);SPCCityJournalProbe.Start(P,shared)
 SPCCityFlowProbe.Start(P,shared);SPCEffectiveFacts.Start(P,shared);SPCInvestmentAction.Start(P,shared)
 Events.LoadScreenClose.Fire()
 d=shared.CityProgressionStore;a=shared.InvestmentAction
end
function reset(potential,kind)
 props={};cities={};units={};writes=0;cityWrites=0;kills=0;governor=4;writeN=0;fail=nil
 s=fixture();s.values.JOURNAL.specialization=kind or 'RESEARCH';s.values.JOURNAL.first.type=({RESEARCH='DISTRICT_CAMPUS',CULTURE='DISTRICT_THEATER',INDUSTRY='DISTRICT_INDUSTRIAL_ZONE',COMMERCE='DISTRICT_COMMERCIAL_HUB'})[kind or 'RESEARCH']
 s.values.FLOW.facts=M.Copy(s.values.JOURNAL);s.values.FLOW.target=M.Copy(s.values.JOURNAL)
 s.values.INVEST.anchor.specialization=s.values.JOURNAL.specialization;s.values.INVEST.anchor.first=M.Copy(s.values.JOURNAL.first)
 s.values.INVEST.investments={};for i=1,potential-1 do s.values.INVEST.investments['r'..i]='crew'..i end;s.values.INVEST.revision=potential
 if potential==1 then s.values.INVEST=nil end
 c=mkcity(s);cities={c};props['SPC_DEV_BINDING_B013_P0']=M.Copy(s.ledger)
 Game={GetCurrentGameTurn=function()return 8 end,GetProperty=function(_,k)return M.Copy(props[k])end,
 SetProperty=function(_,k,v)assert(k==K,'unexpected Game write');writes=writes+1;writeN=writeN+1;if fail~=writeN then props[k]=M.Copy(v)end end}
 CityManager={GetCityAt=function(x,y)for _,v in ipairs(cities)do if v:GetX()==x and v:GetY()==y then return v end end end,
 GetCity=function(pid,id)for _,v in ipairs(cities)do if v:GetOwner()==pid and v:GetID()==id then return v end end end,
 GetDistrictAt=function()return {GetCity=function()return c end,GetOwner=function()return 0 end,GetType=function()return s.values.JOURNAL.first.type end}end}
 Players={[0]={GetCities=function()return {Members=function()return ipairs(cities)end,FindID=function(_,id)return CityManager.GetCity(0,id)end,GetCapitalCity=function()return c end}end,
 GetUnits=function()return {FindID=function(_,id)return units[id]end,Destroy=function(_,u)kills=kills+1;units[u.id]=nil;Events.UnitRemovedFromMap.Fire(0,u.id)end}end}}
 GameInfo={Units={[1]={UnitType='UNIT_SETTLER'}}}
 boot()
end
function addFixtureCity(id,x,serial,kind)
 local t=fixture();t.ref.cityID=id;t.ref.x=x;t.values.TOKEN='DEV-B013-P0-'..serial
 local j=t.values.JOURNAL;j.cityID=id;j.x=x;j.token=t.values.TOKEN;j.specialization=kind or 'RESEARCH'
 j.first.type=({RESEARCH='DISTRICT_CAMPUS',CULTURE='DISTRICT_THEATER',INDUSTRY='DISTRICT_INDUSTRIAL_ZONE',COMMERCE='DISTRICT_COMMERCIAL_HUB'})[j.specialization]
 local f=t.values.FLOW;f.cityID=id;f.x=x;f.token=t.values.TOKEN;f.facts=M.Copy(j);f.target=M.Copy(j);t.values.INVEST=nil
 local other=mkcity(t);cities[#cities+1]=other
 local ledger=props.SPC_DEV_BINDING_B013_P0;ledger.counter=math.max(ledger.counter,serial)
 ledger.records[tostring(id)]={owner=0,cityID=id,x=x,y=5,serial=serial,uid=t.values.TOKEN,state='CONFIRMED'}
 return other,t
end
function failFixtureWrite(offset)fail=offset and (writeN+offset) or nil end
function fixtureStats()return {writes=writes,cityWrites=cityWrites,kills=kills}end
function addunit(id,city)
 local site=city or c;local up={};units[id]={id=id,GetOwner=function()return 0 end,GetType=function()return 1 end,GetX=function()return site:GetX() end,GetY=function()return site:GetY() end,
 GetProperty=function(_,k)return up[k]end,SetProperty=function(_,k,v)up[k]=v end}
end
-- Tests address record state explicitly; raw collection/schema tests use Game directly.
function e2Record()
 local v=Game:GetProperty(K);if not v or v.schema==1 then return v end
 assert(v.schema==2);local first
 for _,r in pairs(v.records)do assert(not first,'single-record helper only');first=r end
 return first
end
function setE2Record(r)
 local v=Game:GetProperty(K)
 if v and v.schema==2 then local token=next(v.records);v.records[token]=r else v=r end
 Game:SetProperty(K,v)
end
function import()local out=d.Import(0,c);assert(out:find('旧City账本冻结'),out);assert(e2Record().stage=='ACTIVE')end
function prepare(id)
 addunit(id);local out=a.Prepare(0,c,id,'REQ'..id,false);assert(out:find('PREPARED'),out);return shared.InvestmentPreview.token
end
for _,kind in ipairs({'RESEARCH','CULTURE','INDUSTRY','COMMERCE'})do for level=1,4 do
 reset(level,kind);local before=shared.EffectiveFacts.Read(0,c);import();local after=shared.EffectiveFacts.Read(0,c)
 assert(before.potential==after.potential and before.active==after.active and before.specialization==after.specialization)
 assert(writes==2 and cityWrites==0);import();assert(writes==2)
 boot();assert(writes==2 and shared.EffectiveFacts.Read(0,c).potential==level)
 governor=1;assert(shared.EffectiveFacts.Read(0,c).active==1)
end end
reset(2);import();local frozen=M.Copy(s.values.INVEST);local token=prepare(12);local out=a.Confirm(0,c,token);assert(out:find('INVESTED'),out)
assert(kills==1 and writes==5 and cityWrites==0 and s.values.INVEST.revision==frozen.revision)
assert(shared.EffectiveFacts.Read(0,c).potential==3)
assert(a.Confirm(0,c,token):find('ALREADY_COMMITTED') and writes==5 and kills==1)
boot();assert(shared.EffectiveFacts.Read(0,c).potential==3 and writes==5)
-- Actual legacy completion/foundation/load callbacks cannot write the target.
GameEvents.CityBuilt.Fire(0,7,4,5);GameEvents.OnDistrictConstructed.Fire(0,s.values.JOURNAL.first.type,4,5)
shared.OnFreshCityBinding(0,c);assert(cityWrites==0 and writes==5)
for i=1,100 do Events.PublishComplete.Fire();Events.PlaybackComplete.Fire();assert(shared.EffectiveFacts.Read(0,c).potential==3)end
assert(writes==5 and cityWrites==0)
-- A second original city stays on its legacy backend, including after load.
local t=fixture();t.ref.cityID=8;t.ref.x=6;t.values.TOKEN='DEV-B013-P0-2'
local j=t.values.JOURNAL;j.cityID=8;j.x=6;j.token=t.values.TOKEN
local f=t.values.FLOW;f.cityID=8;f.x=6;f.token=t.values.TOKEN;f.facts=M.Copy(j);f.target=M.Copy(j);t.values.INVEST=nil
local other=mkcity(t);cities[2]=other
props.SPC_DEV_BINDING_B013_P0.counter=2;props.SPC_DEV_BINDING_B013_P0.records['8']={owner=0,cityID=8,x=6,y=5,serial=2,uid=t.values.TOKEN,state='CONFIRMED'}
boot();assert(not d.Owns(other) and shared.EffectiveFacts.Read(0,other).potential==1)
assert(shared.EffectiveFacts.Read(0,c).potential==3 and cityWrites==0)
-- Frozen legacy data is never a fallback, even when old journal/flow disappear.
s.values.FLOW=nil;s.values.JOURNAL=nil;s.values.INVEST=nil
assert(shared.EffectiveFacts.Read(0,c).potential==3);boot();assert(shared.EffectiveFacts.Read(0,c).potential==3)
assert(shared.EffectiveFacts.Read(0,other).potential==1)
reset(2);local netBefore=SPCNetworkInput.Capture(P,shared,0,{},'route0',nil)
import();local netAfter=SPCNetworkInput.Capture(P,shared,0,{},'route0',nil)
assert(netBefore.signature==netAfter.signature and writes==2)
s.values.FLOW=nil;assert(SPCNetworkInput.Capture(P,shared,0,{},'route0',nil).signature==netAfter.signature)
reset(2);fail=1;assert(d.Import(0,c):find('暂停') and d.Owns(c));assert(props[K]==nil and cityWrites==0)
reset(2);fail=2;assert(d.Import(0,c):find('暂停'));s.values.INVEST.revision=99;fail=nil;boot()
assert(e2Record().stage=='PREPARED' and not pcall(shared.EffectiveFacts.Read,0,c) and cityWrites==0)
-- Import and debit failure windows: no duplicate consumption or guessed receipt.
reset(2);fail=2;assert(d.Import(0,c):find('暂停'));assert(e2Record().stage=='PREPARED' and d.Owns(c));fail=nil;boot();assert(e2Record().stage=='ACTIVE')
for _,n in ipairs({3,4,5})do
 reset(1);import();token=prepare(12);fail=n;assert(a.Confirm(0,c,token):find('HELD'))
 local k=kills;fail=nil;boot();assert(kills==k)
 assert(shared.EffectiveFacts.Read(0,c).potential==(n==5 and 2 or 1))
end
reset(1);import();token=prepare(12);units[12]=nil;Events.UnitRemovedFromMap.Fire(0,12);addunit(12)
assert(a.Confirm(0,c,token):find('PREPARE_FIRST') and kills==0 and writes==2)
reset(1);s.values.JOURNAL.specialization='MILITARY';assert(d.Import(0,c):find('暂停') and writes==0)
reset(1);s.values.JOURNAL.specialization='REALLOCATING';assert(d.Import(0,c):find('暂停') and writes==0)
reset(1);s.values.JOURNAL.health='GAP';assert(d.Import(0,c):find('暂停') and writes==0)
reset(1);import();props[K].schema=99;boot();assert(d.Owns(c) and not pcall(shared.EffectiveFacts.Read,0,c));assert(writes==2)
-- Preserve record and block legacy adoption on confirmed reference departure.
reset(2);import();s.ref.owner=62;s.ref.cityID=40;Events.CityTransfered.Fire(62,40,0,7)
assert(e2Record().stage=='HELD_TRANSFER' and e2Record().investment.revision==2 and d.Owns(c))
assert(not pcall(shared.EffectiveFacts.Read,0,c) and cityWrites==0)
print('E2 LOCAL_SIMULATION_PASS: 16 imports; actual investment/legacy-load hooks; duplicate, failure recovery, old-key independence, four-kind gate. Transfer carrier cleanup NOT certified.')
''')
# Syntax and exact package inclusion, without executing UI in mocks.
for p in M.rglob('*.lua'):
 l.execute('assert(load(...))',p.read_text())
root=ET.parse(M/'SpecializationP0.modinfo').getroot()
assert root.attrib['version']=='133'
assert 'CityProgressionStore.lua' in [e.text for e in root.find('Files')]
# Real eligibility function with native-shaped API mocks, no silent fallback to AI.
probe=(M/'Probe.lua').read_text();fn=probe[probe.index('function P.IsTestPlayer'):probe.index('function P.Summary')]
l.execute(fn)
l.execute("""
P.Call=function(o,k,...)if not o or not o[k]then return false end;return pcall(o[k],o,...)end
local human,multi=true,false
PlayerConfigurations={[0]={GetCivilizationTypeName=function()return 'CIVILIZATION_SPC_TEST'end,GetLeaderTypeName=function()return 'LEADER_SPC_TEST'end,IsHuman=function()error('UI-only config method must not be called')end}}
Players={[0]={IsHuman=function()return human end}}
GameConfiguration={IsAnyMultiplayer=function()return multi end}
assert(P.IsTestPlayer(0));human=false;assert(not P.IsTestPlayer(0));human=true;multi=true;assert(not P.IsTestPlayer(0));multi=false
PlayerConfigurations[0].IsHuman=nil;assert(P.IsTestPlayer(0))
Players[0].IsHuman=nil;assert(not P.IsTestPlayer(0))
""")
print('Lua compile + modinfo + human/singleplayer gate PASS')

# Execute the actual operation dispatch fragment so the visible button reaches the store.
g=(M/'Gameplay.lua').read_text();frag=g[g.index("  if params.Action=='PROGRESSION_IMPORT'"):g.index("  if params.Action=='IDENTITY_RECORD'")]
u=LuaRuntime();u.execute("P={IsTestPlayer=function()return true end};Players={[0]={GetCities=function()return {FindID=function()return 'selected' end}end}};shared={CityProgressionStore={Import=function(pid,c)assert(pid==0 and c=='selected');return 'IMPORTED'end,Describe=function()return 'SUMMARY'end},CityIdentityExperiment={Begin=function()return 'E1_BEGIN'end,Describe=function()return 'E1_READ'end}}")
u.execute('function dispatch(playerID,params) '+frag+' end')
u.execute("dispatch(0,{Action='PROGRESSION_IMPORT',CityID=7,Token='1'});assert(shared.Snapshot=='IMPORTED');dispatch(0,{Action='PROGRESSION_STORE_READ',Token='2'});assert(shared.Snapshot=='SUMMARY');dispatch(0,{Action='IDENTITY_EXPERIMENT_READ',Token='3'});assert(shared.Snapshot=='E1_READ')")
print('Actual request dispatch PASS')
