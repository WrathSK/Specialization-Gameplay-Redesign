"""B107 L3: actual foundation/binding/legacy writers/first completion/investment.
LOCAL_SIMULATION_PASS is not native founding or engine persistence evidence.
"""
from pathlib import Path
from lupa.lua55 import LuaRuntime
R=Path(__file__).resolve().parents[1];l=LuaRuntime()
for n in ['CityIdentityRead','CityProgressionStore','BindingProbe','CompletionRecordProbe','CityJournalProbe','FreshBindingHook','CityFlowProbe','EffectiveFacts','InvestmentAction','NetworkInput']:
 l.execute((R/'Mod'/f'{n}.lua').read_text())
s=(R/'DevelopmentTests/test_p0_e1.py').read_text()
l.execute('M=SPCCityIdentityRead\n'+s[s.index('function fixture()'):s.index('function expect(')])
s=(R/'DevelopmentTests/test_p0_e2.py').read_text()
harness=s[s.index('local function event()'):s.index("for _,kind in ipairs({'RESEARCH'")]
harness=harness.replace('SPCBindingProbe.Start(P,shared);SPCCityJournalProbe', 'SPCBindingProbe.Start(P,shared);SPCCompletionRecordProbe.Start(P,shared);SPCCityJournalProbe')
harness=harness.replace('shared={}\n SPCity', "shared={}\n if missingHook then Events.UnitActivate.Add=nil end\n SPCity")
l.execute(harness+r'''
local KEY=SPCCityProgressionStore.KEY
local ds;local turn;local propertyHook
local function record(city)return Game:GetProperty(KEY).records[city:GetProperty(M.Keys.TOKEN)]end
local function serialized(v)
 if type(v)~='table'then return tostring(v)end
 local t={};for k,x in pairs(v)do t[#t+1]=tostring(k)..'='..serialized(x)end;table.sort(t);return '{'..table.concat(t,',')..'}'
end
local function fresh(id,x)
 local city=mkcity({ref={owner=0,cityID=id or 9,x=x or 8,y=5},values={}});cities[#cities+1]=city;return city
end
local function start()
 EventSubTypes={FOUND_CITY=-1828126782};turn=8;propertyHook=nil
 reset(2);import();ds={}
 Game.GetCurrentGameTurn=function()return turn end
 Game.SetProperty=function(_,k,v)
  assert(k==KEY or k=='SPC_DEV_BINDING_B013_P0','unexpected Game write')
  writes=writes+1;writeN=writeN+1;if fail~=writeN then props[k]=M.Copy(v)end
  if propertyHook then propertyHook(k,v)end
 end
 CityManager.GetDistrictAt=function(x,y)return ds[x..':'..y]end
 P.Rows=function(t)assert(t=='DistrictReplaces');return {{CivUniqueDistrictType='DISTRICT_SEOWON',ReplacesDistrictType='DISTRICT_CAMPUS'}}end
 local n=fresh();return n
end
local function built(n)GameEvents.CityBuilt.Fire(0,n:GetID(),n:GetX(),n:GetY())end
local function init(n)Events.CityInitialized.Fire(0,n:GetID(),n:GetX(),n:GetY())end
local function found(n,unit,reason)Events.UnitActivate.Fire(0,unit or 101,n:GetX(),n:GetY(),reason or EventSubTypes.FOUND_CITY,false)end
local function district(n,kind,x,complete)
 local d={complete=complete~=false}
 function d:GetCity()return n end;function d:GetOwner()return n:GetOwner()end
 function d:GetID()return x+50 end;function d:GetType()return kind end;function d:IsComplete()return self.complete end
 ds[x..':5']=d;return d
end
local function done(n,kind,x,complete)
 local d=district(n,kind,x,complete);GameEvents.OnDistrictConstructed.Fire(0,kind,x,5);return d
end
local function cleanLegacy(n)
 assert((shared.CompletionRecordProbe.players[0] or {}).writes==nil or shared.CompletionRecordProbe.players[0].writes==0)
 assert(n.s.values.JOURNAL==nil and n.s.values.FLOW==nil and n.s.values.INVEST==nil and n.s.values.TEMPLATES==nil)
 assert(not (shared.CityJournalProbe.players[0] or {}).halted and not (shared.CityFlowProbe.players[0] or {}).halted)
end
-- Both orders, duplicate/invisible event, no arm/unit API, known NONE facts, coldload.
for _,early in ipairs({true,false})do
 local n=start();local control=serialized(record(c));local before=fixtureStats()
 built(n);assert(not d.Owns(n) and d.BlocksLegacy(n));assert(n.s.values.TOKEN==nil)
 for i=1,20 do Events.GameCoreEventPublishComplete.Fire();Events.GameCoreEventPlaybackComplete.Fire()end
 assert(fixtureStats().writes==before.writes)
 if early then found(n);init(n)else init(n);found(n)end
 assert(d.Owns(n) and record(n).schema==2 and record(n).progression=='UNASSIGNED')
 local f=shared.EffectiveFacts.Read(0,n);assert(f.specialization=='NONE' and f.potential==0 and f.active==0 and f.investmentCount==0)
 local net=SPCNetworkInput.Capture(P,shared,0,{},'empty');assert(net.cities[n:GetID()].active==0 and net.cities[n:GetID()].specialization=='NONE')
 cleanLegacy(n);assert(record(c).schema==1 and serialized(record(c))==control)
 local frozen=serialized(Game:GetProperty(KEY));local stats=fixtureStats()
 found(n);init(n);built(n);assert(serialized(Game:GetProperty(KEY))==frozen and fixtureStats().writes==stats.writes)
 addunit(201,n);assert(not a.Prepare(0,n,201,'NONE',false):find('PREPARED'))
 boot();assert(shared.EffectiveFacts.Read(0,n).potential==0 and fixtureStats().writes==stats.writes)
 -- Not a recognized complete district: no identity. Then a unique replacement wins.
 done(n,'DISTRICT_HOLY_SITE',9);local placed=done(n,'DISTRICT_CAMPUS',10,false)
 assert(record(n).progression=='UNASSIGNED')
 done(n,'DISTRICT_SEOWON',11);done(n,'DISTRICT_THEATER',12)
 assert(record(n).progression=='SPECIALIZED' and record(n).base.first.type=='DISTRICT_SEOWON')
 assert(shared.EffectiveFacts.Read(0,n).potential==1);cleanLegacy(n)
 local rev=record(n).revision;GameEvents.OnDistrictConstructed.Fire(0,'DISTRICT_SEOWON',11,5);assert(record(n).revision==rev)
 addunit(202,n);local out=a.Prepare(0,n,202,'INVEST',false);assert(out:find('PREPARED'),out)
 local request=shared.InvestmentPreview.token;out=a.Confirm(0,n,request);assert(out:find('INVESTED'),out)
 assert(shared.EffectiveFacts.Read(0,n).potential==2 and fixtureStats().kills==1)
 assert(a.Confirm(0,n,request):find('ALREADY_COMMITTED'))
 boot();assert(shared.EffectiveFacts.Read(0,n).potential==2 and serialized(record(c))==control);cleanLegacy(n)
 assert(d.Describe(0,n):find('正常建城') and d.NativeDescribe(0,n):find('专业已锁定'))
end
-- Completion during pending/admission: delivery order, not district ID or a scan.
for _,reentrant in ipairs({false,true})do
 local n=start();built(n);init(n)
 local function early()
  done(n,'DISTRICT_THEATER',12);done(n,'DISTRICT_CAMPUS',9);cleanLegacy(n)
 end
 if reentrant then propertyHook=function(k)if k=='SPC_DEV_BINDING_B013_P0' then propertyHook=nil;early()end end else early()end
 found(n);assert(record(n).base.specialization=='CULTURE' and record(n).base.first.districtID==62);cleanLegacy(n)
end
-- Transfer control is never registration. Pending evidence cannot leak old writes.
local n=start();built(n);init(n);Events.GameCoreEventPublishComplete.Fire()
n.s.ref.owner=2;Events.CityTransfered.Fire(2,n:GetID(),0,0)
assert(not d.Owns(n) and n.s.values.TOKEN==nil and d.Describe(0,n):find('TRANSFER_BEFORE_ADMISSION'))
n.s.ref.owner=0;found(n);assert(not d.Owns(n));cleanLegacy(n)
-- Missing/wrong/foreign/cross-turn signal: no adoption; session evidence isn't rebuilt on load.
n=start();built(n);init(n);Events.UnitActivate.Fire(2,101,8,5,EventSubTypes.FOUND_CITY,true)
found(n,101,0);assert(n.s.values.TOKEN==nil)
turn=9;found(n);assert(d.Describe(0,n):find('CROSS_TURN') and not d.Owns(n))
boot();init(n);assert(not d.Owns(n) and n.s.values.TOKEN==nil)
n=start();EventSubTypes=nil;boot();built(n);init(n);Events.UnitActivate.Fire(0,101,8,5,-1828126782,true)
assert(not d.Owns(n) and n.s.values.TOKEN==nil)
-- A missing hook holds even if other callbacks deliver valid evidence.
n=start();missingHook=true;boot();missingHook=nil;built(n);init(n);found(n)
assert(not d.Owns(n) and n.s.values.TOKEN==nil and d.Describe(0,n):find('不可用'))
-- No historical allocation/location reuse; duplicate existing-city event preserves all history.
n=start();local frozen=serialized(record(c));built(c);init(c);found(c);assert(serialized(record(c))==frozen)
local old=props.SPC_DEV_BINDING_B013_P0;old.records['7'].x=8;old.records['7'].y=5
built(n);init(n);found(n);assert(n.s.values.TOKEN==nil and d.Describe(0,n):find('LOCATION_HISTORY'))
-- Two slots remain a test limit; it never evicts the accepted control.
n=start();built(n);init(n);found(n);local b=fresh(10,14);found(b);init(b)
assert(not d.Owns(b) and b.s.values.TOKEN==nil and serialized(record(c)):find('RESEARCH'))
-- Candidate and early-completion bounds; no unbounded event history.
n=start();built(n);init(n)
for i=1,9 do done(n,'DISTRICT_CAMPUS',20+i)end
found(n);assert(not d.Owns(n) and d.Describe(0,n):find('EARLY_COMPLETION_LIMIT') and n.s.values.TOKEN==nil)
n=start();for i=1,5 do local b=i==1 and n or fresh(10+i,20+i);built(b)end
local b=cities[#cities];assert(d.BlocksLegacy(b) and b.s.values.TOKEN==nil)
-- Write failure gates (reserve, token, confirm, record); no retry or fallback.
for _,offset in ipairs({1,2,3})do
 n=start();built(n);init(n);failFixtureWrite(offset);found(n)
 local stats=fixtureStats();found(n);init(n);built(n);assert(fixtureStats().writes==stats.writes)
 if offset<3 then assert(shared.EffectiveFacts.Read(0,c).potential==2)else assert(not pcall(shared.EffectiveFacts.Read,0,c))end;cleanLegacy(n)
 assert(not pcall(shared.EffectiveFacts.Read,0,n))
end
n=start();built(n);init(n);local set=n.SetProperty;n.SetProperty=function()end;found(n);n.SetProperty=set
assert(n.s.values.TOKEN==nil and d.Describe(0,n):find('CITY_WRITE_UNCONFIRMED'));cleanLegacy(n)
-- A failed completion read cannot silently choose the next district, including after load.
n=start();built(n);init(n);found(n)
local bad=district(n,'DISTRICT_CAMPUS',15);bad.GetID=function()error('native read failure')end
GameEvents.OnDistrictConstructed.Fire(0,'DISTRICT_CAMPUS',15,5)
assert(record(n).completionError=='COMPLETION_EVIDENCE_UNAVAILABLE')
done(n,'DISTRICT_THEATER',16);boot();assert(record(n).progression=='UNASSIGNED' and not pcall(shared.EffectiveFacts.Read,0,n))
-- Foreign/wrong-owner completion never locks the local record.
n=start();built(n);init(n);found(n);district(n,'DISTRICT_CAMPUS',15)
GameEvents.OnDistrictConstructed.Fire(2,'DISTRICT_CAMPUS',15,5);assert(record(n).progression=='UNASSIGNED')
-- Event before city object and initialization: unit isn't looked up; explicit reference comes later.
n=start();table.remove(cities);found(n);cities[#cities+1]=n;built(n);init(n);assert(record(n).progression=='UNASSIGNED')
-- Token-only partial save is a diagnosed hold, not load-time adoption.
n=start();built(n);init(n);failFixtureWrite(2);found(n);boot()
assert(not d.Owns(n) and d.Describe(0,n):find('绑定已存在') and not pcall(shared.EffectiveFacts.Read,0,n))
-- Corrupt/unsupported inner schema and NONE+receipt combination are never reinterpreted as legacy.
for _,mutate in ipairs({function(r)r.schema=99 end,function(r)r.progression=nil end,function(r)r.investment={}end})do
 n=start();built(n);init(n);found(n);local saved=Game:GetProperty(KEY);mutate(saved.records[n.s.values.TOKEN]);Game:SetProperty(KEY,saved)
 boot();assert(not pcall(shared.EffectiveFacts.Read,0,n) and d.Owns(n))
end
-- A formerly complete early event becoming unreadable stops the record after admission/reload.
n=start();built(n);init(n);local early=done(n,'DISTRICT_CAMPUS',15);early.complete=false;found(n)
assert(record(n).completionError=='FOUNDATION_ADMISSION_INCOMPLETE');boot()
assert(not pcall(shared.EffectiveFacts.Read,0,n));done(n,'DISTRICT_THEATER',16);assert(record(n).progression=='UNASSIGNED')
-- Completion between FOUND_CITY and Initialized has no pre-assumed city ID/order.
n=start();found(n);done(n,'DISTRICT_CAMPUS',15);init(n);assert(record(n).base.specialization=='RESEARCH')
-- Missing object cannot silently choose a later completion for an unassigned record.
n=start();built(n);init(n);found(n);GameEvents.OnDistrictConstructed.Fire(0,'DISTRICT_CAMPUS',99,5)
assert(record(n).completionError=='COMPLETION_CITY_UNAVAILABLE')
-- UNASSIGNED loss is retained/dormant, not generalized recapture.
n=start();built(n);init(n);found(n);local token=n.s.values.TOKEN
d.RegisterExit('NoEffects',function()end);n.s.ref.owner=2;Events.CityTransfered.Fire(2,n:GetID(),0,0)
assert(Game:GetProperty(KEY).records[token].stage=='HELD_TRANSFER')
n.s.ref.owner=0;Events.CityTransfered.Fire(0,n:GetID(),2,0)
assert(Game:GetProperty(KEY).records[token].stage=='HELD_TRANSFER' and d.Status(n).returnRejection=='RETURN_UNASSIGNED_DEFERRED')
print('B107 LOCAL_SIMULATION_PASS: automatic founding, mixed schema, NONE/coldload, ordered completion, investment, legacy guards, negative evidence, bounded pending, write failures, unassigned transfer hold')
''')
