"""Actual two-record store + investment/old-writer routing; no native-engine claim."""
from pathlib import Path
import runpy
R=Path(__file__).resolve().parents[1]
l=runpy.run_path(str(R/'DevelopmentTests/test_b103_e2_hydration.py'))['l']
l.execute(r"""
P.IsTestPlayer=function(pid)return pid==0 end
local KEY=SPCCityProgressionStore.KEY
local function record(token)return Game:GetProperty(KEY).records[token]end
local function allDistricts(list)
 Players[0].GetDistricts=function()local rows={};for i,city in ipairs(list)do
  rows[i]={GetCity=function()return city end,GetType=function()return city.s.values.JOURNAL.first.type end,
   GetID=function()return 98+i end,IsComplete=function()return true end}
 end;return {Members=function()return ipairs(rows)end}end
end
-- A real accepted tokenless B103 singleton remains byte-for-byte intact on load,
-- then becomes the first schema2 entry during the second explicit import.
held();chain();local saved=e2Record();local token1=saved.base.token
Game:SetProperty(KEY,saved);local beforeWrites=fixtureStats().writes;boot();districts()
assert(Game:GetProperty(KEY).schema==1 and fixtureStats().writes==beforeWrites)
assert(shared.EffectiveFacts.Read(0,c).potential==3)
local b,bs=addFixtureCity(9,9,2,'COMMERCE');local token2=bs.values.TOKEN
boot();districts() -- legacy Flow resumes the newly supplied fixture before explicit import
local out=d.Import(0,b);assert(out:find('旧City账本冻结'),out)
local envelope=Game:GetProperty(KEY);assert(envelope.schema==2 and record(token2).stage=='ACTIVE')
assert(encode(record(token1))==encode(saved),'SINGLETON_CHANGED_DURING_CONVERSION')
assert(shared.EffectiveFacts.Read(0,b).potential==1 and shared.EffectiveFacts.Read(0,c).potential==3)
local raw=encode(envelope);d.Import(0,b);assert(encode(Game:GetProperty(KEY))==raw)
-- Genuine investment action in second city only; first receipt, potential and old
-- properties are untouched. Add a third unregistered city as legacy control.
local control=addFixtureCity(10,12,3);boot();allDistricts({c,b});d.RegisterExit('NoCarriers',function()end)
assert(not d.Owns(control) and shared.EffectiveFacts.Read(0,control).potential==1)
local oldA,oldB=encode(s.values),encode(bs.values);local first=encode(record(token1))
addunit(71,b);local result=a.Prepare(0,b,71,'TWO_CITY',false);assert(result:find('PREPARED'),result)
local action=shared.InvestmentPreview.token;assert(a.Confirm(0,b,action):find('INVESTED'))
assert(a.Confirm(0,b,action):find('ALREADY_COMMITTED'))
assert(shared.EffectiveFacts.Read(0,b).potential==2 and shared.EffectiveFacts.Read(0,c).potential==3)
assert(encode(record(token1))==first and encode(s.values)==oldA and encode(bs.values)==oldB)
local stable=encode(Game:GetProperty(KEY));boot();allDistricts({c,b});d.RegisterExit('NoCarriers',function()end)
assert(encode(Game:GetProperty(KEY))==stable and shared.EffectiveFacts.Read(0,b).potential==2)
-- Selected city, never implicit singleton/other-city diagnostic fallback.
assert(d.NativeDescribe(0,b):find('永久 COMMERCE | Potential 2',1,true))
assert(d.NativeDescribe(0,c):find('永久 RESEARCH | Potential 3',1,true))
assert(d.NativeDescribe(0,control):find('未登记',1,true))
assert(d.NativeDescribe(0):find('请选择',1,true))
assert(d.Import(0,control):find('TWO_CITY_TEST_LIMIT',1,true))
assert(encode(Game:GetProperty(KEY))==stable)
-- First-city loss/return leaves second record and its session evidence unchanged.
local second=encode(record(token2));local bStatus=encode(d.Status(b))
s.ref.owner=62;s.ref.cityID=40;Events.CityTransfered.Fire(62,40,0,0)
assert(record(token1).stage=='HELD_TRANSFER' and d.Status(c).exitStatus=='WITHDRAWN')
assert(encode(record(token2))==second and encode(d.Status(b))==bStatus)
assert(shared.EffectiveFacts.Read(0,b).potential==2 and not pcall(shared.EffectiveFacts.Read,0,c))
Events.CityAddedToMap.Fire(62,40,4,5);chain()
assert(record(token1).stage=='ACTIVE' and encode(record(token2))==second)
assert(encode(d.Status(b))==bStatus)
-- Two foreign holdings, independent bounded exit failure and transition state.
local hits={};d.RegisterExit('IndependentExit',function(city)
 local x=city:GetX();hits[x]=(hits[x] or 0)+1;if x==9 then error('SECOND_ONLY_FAIL')end
end)
s.ref.owner=62;s.ref.cityID=40;Events.CityTransfered.Fire(62,40,0,0)
bs.ref.owner=62;bs.ref.cityID=50;Events.CityTransfered.Fire(62,50,0,0)
for i=1,5 do d.ExitConfirmed()end
assert(hits[4]==1 and hits[9]==3)
assert(d.Status(c).exitStatus=='WITHDRAWN' and d.Status(b).exitStatus=='PARTIAL_HELD')
local frozenB=encode(record(token2));local failedB=encode(d.Status(b));chain()
assert(record(token1).stage=='ACTIVE' and encode(record(token2))==frozenB)
assert(encode(d.Status(b))==failedB and shared.EffectiveFacts.Read(0,c).potential==3)
bs.ref.owner=0;bs.ref.cityID=90;Events.CityTransfered.Fire(0,90,62,0)
assert(record(token2).stage=='HELD_TRANSFER' and d.Status(b).returnRejection=='RETURN_WITHDRAWAL_UNCONFIRMED')
assert(shared.EffectiveFacts.Read(0,c).potential==3)
-- On a fresh foreign-held load, successful exits allow second city's existing
-- matching-token path; no shared failure latch from the previous session.
bs.ref.owner=62;bs.ref.cityID=50;boot();allDistricts({c,b});d.RegisterExit('NoCarriers',function()end);d.ExitConfirmed()
bs.ref.owner=0;bs.ref.cityID=90;Events.CityTransfered.Fire(0,90,62,0)
assert(record(token2).stage=='ACTIVE' and shared.EffectiveFacts.Read(0,b).potential==2)
boot();assert(shared.EffectiveFacts.Read(0,c).potential==3 and shared.EffectiveFacts.Read(0,b).potential==2)
assert(not d.Owns(control) and shared.EffectiveFacts.Read(0,control).potential==1)
-- Idle/generic notifications and read-only diagnostics do not mutate the envelope.
local stats=fixtureStats();local last=encode(Game:GetProperty(KEY))
for i=1,20 do Events.PublishComplete.Fire();Events.PlaybackComplete.Fire();d.Describe(0,b)end
assert(encode(Game:GetProperty(KEY))==last and fixtureStats().writes==stats.writes)
-- Envelope collision/corruption is never another record or legacy permission.
local good=Game:GetProperty(KEY)
for _,mode in ipairs({'token','location','schema','record'})do
 local bad=M.Copy(good)
 if mode=='token' then bad.records[token2].base.token=token1
 elseif mode=='location' then bad.records[token2].origin=M.Copy(bad.records[token1].origin)
 elseif mode=='schema' then bad.schema=99
 else bad.records[token2].revision=-1 end
 Game:SetProperty(KEY,bad);boot()
 assert(d.Owns(c) and d.Owns(b) and not pcall(shared.EffectiveFacts.Read,0,c) and not pcall(shared.EffectiveFacts.Read,0,b))
end
Game:SetProperty(KEY,good);boot();assert(shared.EffectiveFacts.Read(0,b).potential==2)
-- Import collision and failed validation consume no record/worker slot.
reset(1);import();local aRecord=e2Record();local b2,t=addFixtureCity(9,9,2)
boot();local proper=t.values.TOKEN;t.values.TOKEN=s.values.TOKEN
assert(d.Import(0,b2):find('COLLISION',1,true));t.values.TOKEN=proper
local j=t.values.JOURNAL;t.values.JOURNAL=nil;assert(d.Import(0,b2):find('暂停'));t.values.JOURNAL=j
assert(d.Import(0,b2):find('旧City账本冻结'))
assert(encode(record(s.values.TOKEN))==encode(aRecord))
-- Failure at collection PREPARED versus activation write: existing city is not
-- rewritten/lost; reload either retains the old collection or resumes validated B.
for _,offset in ipairs({1,2})do
 reset(2);import();local aSaved=e2Record();local newCity=addFixtureCity(9,9,2);boot()
 failFixtureWrite(offset);assert(d.Import(0,newCity):find('暂停'));failFixtureWrite(nil)
 boot();assert(shared.EffectiveFacts.Read(0,c).potential==2)
 assert(encode(record(s.values.TOKEN))==encode(aSaved))
 assert(shared.EffectiveFacts.Read(0,newCity).potential==1)
 if offset==1 then assert(not d.Owns(newCity))else assert(d.Owns(newCity))end
end
-- Same CityID under a foreign Owner cannot read a registered original-owner record.
local second=CityManager.GetCity(0,9);local oldOwner=second.s.ref.owner
second.s.ref.owner=3
assert(d.Owns(second) and not pcall(d.Base,0,second))
second.s.ref.owner=oldOwner;assert(shared.EffectiveFacts.Read(0,second).potential==1)
print('B104 LOCAL_SIMULATION_PASS: B103 singleton adapter, two-city import/investment/receipt isolation, selected diagnostics, independent loss/return/retries, coldload, legacy third city, collision/corruption gates, bounded idle')
""")
# UI must actually transmit the selected city; no gameplay request on hover/timer added.
s=(R/'Mod/UI/P0Panel.lua').read_text()
line=next(x for x in s.splitlines() if 'local storageAction=' in x)
assert 'PROGRESSION_STORE_READ' not in line
assert 'CityID=city and city:GetID()' in s
print('B104 selected-city request STATIC_CONFIRMED')

# Run the real UI request body with minimal native-shaped stubs.
from lupa.lua55 import LuaRuntime
u=LuaRuntime()
u.execute("""
P={VERSION='B104.131',IsTestPlayer=function()return true end,Scalar=tostring}
ContextPtr={ClearUpdate=function()end};Game={GetLocalPlayer=function()return 0 end,GetCurrentGameTurn=function()return 8 end}
ExposedMembers={};PlayerOperations={EXECUTE_SCRIPT=1};trace=function()end;status=function()end;waitForResponse=function()end
local selected
function choose(id,owner)selected=id and {GetID=function()return id end,GetOwner=function()return owner or 0 end}or nil end
UI={GetHeadSelectedCity=function()return selected end,RequestPlayerOperation=function(pid,op,p)packet=p;sends=(sends or 0)+1 end}
""")
u.execute(s[s.index('request=function(action,advance)'):s.index('local function legacyCopy')])
u.execute("""
choose(9);request('PROGRESSION_STORE_READ');assert(packet.CityID==9 and sends==1)
choose(88);request('PROGRESSION_STORE_READ');assert(packet.CityID==88 and sends==2)
choose(nil);request('PROGRESSION_STORE_READ');assert(sends==2)
choose(9,3);request('PROGRESSION_STORE_READ');assert(sends==2)
""")
print('B104 actual UI selected-city dispatch LOCAL_SIMULATION_PASS')
