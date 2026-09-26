"""B108 production Start: actual per-city persistence/founding/consumer isolation.
L3 local simulation only; native IsSavedGame/property persistence still needs user test.
"""
from pathlib import Path
from lupa.lua55 import LuaRuntime
R=Path(__file__).resolve().parents[1];l=LuaRuntime()
for n in ['CityIdentityRead','CityProgressionStore','BindingProbe','CompletionRecordProbe','CityJournalProbe','FreshBindingHook','CityFlowProbe','EffectiveFacts','InvestmentAction','NetworkInput','Standardization']:
 l.execute((R/'Mod'/f'{n}.lua').read_text())
s=(R/'DevelopmentTests/test_p0_e1.py').read_text()
l.execute('M=SPCCityIdentityRead\n'+s[s.index('function fixture()'):s.index('function expect(')])
s=(R/'DevelopmentTests/test_p0_e2.py').read_text()
h=s[s.index('local function event()'):s.index("for _,kind in ipairs({'RESEARCH'")]
h=h.replace('SPCCityProgressionStore.StartLegacyTest(P,shared)','SPCCityProgressionStore.Start(P,shared)')
h=h.replace('SPCBindingProbe.Start(P,shared);SPCCityJournalProbe','SPCBindingProbe.Start(P,shared);SPCCompletionRecordProbe.Start(P,shared);SPCCityJournalProbe')
l.execute(h+r'''
local INDEX=SPCCityProgressionStore.INDEX;local PREFIX=SPCCityProgressionStore.RECORD
local ds,perKey,turn,saved,hook,failKey
local function encode(v)
 if type(v)~='table'then return tostring(v)end
 local rows={};for k,x in pairs(v)do rows[#rows+1]=tostring(k)..'='..encode(x)end
 table.sort(rows);return '{'..table.concat(rows,',')..'}'
end
local function start()
 Map={GetGridSize=function()return 200,100 end}
 saved=false;GameConfiguration={IsSavedGame=function()return saved end,GetStartTurn=function()return 0 end}
 EventSubTypes={FOUND_CITY=-1828126782}
 reset(1);props={};cities={};units={};writes=0;cityWrites=0;kills=0;writeN=0;fail=nil
 turn=0;ds={};perKey={};hook=nil;failKey=nil
 Game.GetCurrentGameTurn=function()return turn end
 Game.GetProperty=function(_,k)return M.Copy(props[k])end
 Game.SetProperty=function(_,k,v)
  assert(k==INDEX or k:sub(1,#PREFIX)==PREFIX,'unexpected Game write '..k)
  writes=writes+1;perKey[k]=(perKey[k]or 0)+1
  if failKey~=k then props[k]=M.Copy(v)end
  if hook then hook(k,v)end
 end
 CityManager.GetDistrictAt=function(x,y)return ds[x..':'..y]end
 Players[0].GetDistricts=function()local rows={};for _,v in pairs(ds)do rows[#rows+1]=v end;return {Members=function()return ipairs(rows)end}end
 boot();assert(props[INDEX] and props[INDEX].counter==0,d.Describe(0))
end
local function fresh(i,owner)
 local city=mkcity({ref={owner=owner or 0,cityID=100+i,x=i*2,y=5},values={}});cities[#cities+1]=city;return city
end
local function register(c,reverse)
 GameEvents.CityBuilt.Fire(c:GetOwner(),c:GetID(),c:GetX(),c:GetY())
 local function init()Events.CityInitialized.Fire(c:GetOwner(),c:GetID(),c:GetX(),c:GetY())end
 local function found()Events.UnitActivate.Fire(c:GetOwner(),c:GetID()+1000,c:GetX(),c:GetY(),EventSubTypes.FOUND_CITY,false)end
 if reverse then found();init()else init();found()end
end
local function record(c)return c.s.values.TOKEN and props[PREFIX..c.s.values.TOKEN]end
local function complete(c,kind)
 local x=c:GetX()+1;local id=c:GetID()+500
 local v={GetCity=function()return c end,GetOwner=function()return c:GetOwner()end,GetID=function()return id end,
  GetType=function()return kind end,IsComplete=function()return true end}
 ds[x..':5']=v
 GameEvents.OnDistrictConstructed.Fire(c:GetOwner(),kind,x,5)
end
local function invest(c,id)
 addunit(id,c);local out=a.Prepare(0,c,id,'INVEST',false);assert(out:find('PREPARED'),out)
 local request=shared.InvestmentPreview.token;out=a.Confirm(0,c,request);assert(out:find('INVESTED'),out)
 assert(a.Confirm(0,c,request):find('ALREADY_COMMITTED'));return request
end
local function clean()
 assert(props[SPCCityProgressionStore.KEY]==nil and props.SPC_DEV_BINDING_B013_P0==nil)
 for _,c in ipairs(cities)do
  for _,name in ipairs({'JOURNAL','FLOW','INVEST','TEMPLATES'})do assert(c.s.values[name]==nil,'legacy '..name)end
 end
end
-- Scale and write locality using actual normal-game Start. No historical import adapter.
for _,n in ipairs({1,2,4,8,33})do
 start();local group={};local tokens={}
 for i=1,n do
  local c=fresh(i);group[i]=c;register(c,i%2==0)
  assert(record(c) and record(c).progression=='UNASSIGNED',d.Describe(0,c))
  assert(not tokens[c.s.values.TOKEN]);tokens[c.s.values.TOKEN]=true
  assert(shared.EffectiveFacts.Read(0,c).potential==0)
  if i%3~=1 then complete(c,i%2==0 and 'DISTRICT_CAMPUS' or 'DISTRICT_THEATER')end
 end
 assert(props[INDEX].counter==n and perKey[INDEX]==n+1)
 local before=encode(props[INDEX]);local bytes=0;local frozen={}
 for i,c in ipairs(group)do
  local entries=0;for _ in pairs(record(c).binding.records)do entries=entries+1 end;assert(entries==1)
  bytes=bytes+#encode(record(c));frozen[i]=encode(record(c))
 end
 if n>=2 then
  local old=perKey[PREFIX..group[1].s.values.TOKEN];local indexWrites=perKey[INDEX]
  invest(group[2],901);assert(shared.EffectiveFacts.Read(0,group[2]).potential==2)
  assert(perKey[INDEX]==indexWrites and perKey[PREFIX..group[1].s.values.TOKEN]==old)
  for i,c in ipairs(group)do if i~=2 then assert(encode(record(c))==frozen[i])end end
 end
 assert(encode(props[INDEX])==before);local w=writes;saved=true;boot();assert(writes==w,'load rewrote state')
 for i,c in ipairs(group)do
  local f=shared.EffectiveFacts.Read(0,c);assert(f.potential==(i==2 and 2 or i%3==1 and 0 or 1))
  assert(shared.BindingProbe.Resolve(0,c)==c.s.values.TOKEN)
 end
 for i=1,20 do Events.GameCoreEventPublishComplete.Fire();Events.GameCoreEventPlaybackComplete.Fire();d.Describe(0,group[1])end
 assert(writes==w);clean()
 print('B108 SCALE cities='..n..' aggregate_record_chars='..bytes..' index_writes='..perKey[INDEX]..' coldload_writes=0 idle_writes=0')
end
-- Targeted pending/receipt identity: a stale preview cannot invest into another city.
start();local aCity=fresh(1);register(aCity);complete(aCity,'DISTRICT_CAMPUS')
local bCity=fresh(2);register(bCity);complete(bCity,'DISTRICT_THEATER')
addunit(901,aCity);assert(a.Prepare(0,aCity,901,'A',false):find('PREPARED'));local oldRequest=shared.InvestmentPreview.token
addunit(902,bCity);assert(a.Prepare(0,bCity,902,'B',false):find('PREPARED'))
local request=shared.InvestmentPreview.token;assert(not a.Confirm(0,aCity,oldRequest):find('INVESTED') and kills==0)
assert(a.Confirm(0,bCity,request):find('INVESTED') and kills==1)
assert(shared.EffectiveFacts.Read(0,aCity).potential==1 and shared.EffectiveFacts.Read(0,bCity).potential==2)
-- One-record write failure/corruption doesn't rewrite or halt an unrelated record.
local control=encode(record(bCity));failKey=PREFIX..aCity.s.values.TOKEN
addunit(903,aCity);assert(a.Prepare(0,aCity,903,'FAIL',false):find('PREPARED'))
assert(a.Confirm(0,aCity,shared.InvestmentPreview.token):find('HELD'))
assert(encode(record(bCity))==control and shared.EffectiveFacts.Read(0,bCity).potential==2)
failKey=nil;saved=true;boot();assert(shared.EffectiveFacts.Read(0,bCity).potential==2)
local key=PREFIX..aCity.s.values.TOKEN;props[key].revision=-1;boot()
assert(not pcall(shared.EffectiveFacts.Read,0,aCity) and shared.EffectiveFacts.Read(0,bCity).potential==2)
-- Unknown/old saves are not rewritten, migrated, or allowed to use old writers.
start();local c=fresh(1);register(c);local before=encode(props);props[INDEX].schema=99;saved=true;boot()
assert(not pcall(shared.EffectiveFacts.Read,0,c) and d.BlocksLegacy(c))
local w=writes;register(fresh(2));assert(writes==w)
start();props={};saved=true;boot();assert(next(props)==nil and d.Describe(0):find('OLD_OR_UNKNOWN'))
c=fresh(1);register(c);clean();assert(c.s.values.TOKEN==nil and not pcall(shared.EffectiveFacts.Read,0,c))
assert(d.Import(0,c):find('已关闭'))
start();props={};props[SPCCityProgressionStore.KEY]={schema=2,records={}};local old=encode(props);boot();assert(encode(props)==old and d.Describe(0):find('OLD_SAVE'))
start();props={};GameConfiguration.IsSavedGame=nil;boot();assert(next(props)==nil)
-- Allocation interrupted after index reservation: only that entry held across reload.
start();c=fresh(1);c.SetProperty=function()end;register(c)
assert(props[INDEX].counter==1 and not record(c));saved=true;boot()
assert(d.Owns(c) and not pcall(shared.EffectiveFacts.Read,0,c))
local other=fresh(2);register(other);assert(shared.EffectiveFacts.Read(0,other).potential==0)
-- Existing unrelated foreign city with the same numeric CityID never receives authority.
start();c=fresh(1);register(c);local foreign=fresh(2,3);foreign.s.ref.cityID=c:GetID()
register(foreign);assert(not d.Owns(foreign) and not pcall(d.Base,0,foreign))
assert(shared.EffectiveFacts.Read(0,c).potential==0)
-- Actual loss + retained-token return: B096/B097 workers, current governor and network inputs.
complete(c,'DISTRICT_CAMPUS');invest(c,901);governor=4
table.remove(cities);Players[0].GetCities=function()return {Members=function()return ipairs(cities)end,GetCapitalCity=function()return c end}end;local net=SPCNetworkInput.Capture(P,shared,0,{},'before')
assert(net.cities[c:GetID()].active==2)
local exits=0;d.RegisterExit('OwnedEffects',function()exits=exits+1 end)
c.s.ref.owner=3;c.s.ref.cityID=40;Events.CityTransfered.Fire(3,40,0)
assert(record(c).stage=='HELD_TRANSFER' and exits==1 and not pcall(shared.EffectiveFacts.Read,0,c))
Events.CityTransfered.Fire(3,40,0);assert(exits==1)
-- The map city exists under the foreign owner; load performs bounded module exits again.
saved=true;boot();d.RegisterExit('OwnedEffects',function()end);d.ExitConfirmed();governor=1
c.s.ref.owner=0;c.s.ref.cityID=400;Events.CityTransfered.Fire(0,400,3)
assert(record(c).stage=='ACTIVE',d.Describe(0,c))
assert(shared.EffectiveFacts.Read(0,c).potential==2 and shared.EffectiveFacts.Read(0,c).active==1)
local after=SPCNetworkInput.Capture(P,shared,0,{},'changed');assert(after.cities[400].active==1 and not after.cities[101])
local rev=record(c).revision;Events.CityTransfered.Fire(0,400,3);assert(record(c).revision==rev)

-- Completion reentered during index reservation: delivered first event wins.
start();local early=fresh(1)
hook=function(key)if key==INDEX then hook=nil;complete(early,'DISTRICT_CAMPUS')end end
register(early);assert(shared.EffectiveFacts.Read(0,early).specialization=='RESEARCH')
-- Actual Industry ledger consumer routes to its own Game record, not City properties.
start();local industry=fresh(1);register(industry);complete(industry,'DISTRICT_INDUSTRIAL_ZONE')
local control=fresh(2);register(control);local frozen=encode(record(control))
SPCStandardizationCatalog={Build=function()return {buildings={BUILDING_WORKSHOP={index=1,district='DISTRICT_INDUSTRIAL_ZONE',tier=1}}}end}
P.HasBuilding=function()return true end;industry.GetBuildings=function()return {}end
SPCStandardization.Start(P,shared);Events.LoadScreenClose.Fire()
local ledger=shared.Standardization.ReadLedger(0,industry);assert(ledger.learned.BUILDING_WORKSHOP)
assert(industry.s.values.TEMPLATES==nil and encode(record(control))==frozen)
local before=writes;shared.Standardization.Discover();assert(writes==before)
saved=true;boot();assert(d.ReadTemplates(industry).learned.BUILDING_WORKSHOP)
-- Restore a specialized fixture for the tokenless return test.
start();c=fresh(1);register(c);complete(c,'DISTRICT_CAMPUS');invest(c,901)
d.RegisterExit('OwnedEffects',function()end);governor=1
-- Tokenless native-chain recapture after a foreign-held coldload, using actual worker evidence.
c.s.ref.owner=3;c.s.ref.cityID=45;Events.CityTransfered.Fire(3,45,0)
c.s.values.TOKEN=nil;saved=true;boot();d.RegisterExit('OwnedEffects',function()end);d.ExitConfirmed()
Events.CityAddedToMap.Fire(3,45,c:GetX(),5);Events.CityInitialized.Fire(3,45,c:GetX(),5)
GameEvents.CityBuilt.Fire(0,500,c:GetX(),5)
GameEvents.CityConquered.Fire(0,3,500,c:GetX(),5)
Events.CityRemovedFromMap.Fire(3,45)
c.s.ref.owner=0;c.s.ref.cityID=500
Events.CityAddedToMap.Fire(0,500,c:GetX(),5);Events.CityInitialized.Fire(0,500,c:GetX(),5)
Events.CityTransfered.Fire(0,500,3)
local token=next(props[INDEX].entries);local retained=props[PREFIX..token]
assert(retained.stage=='ACTIVE' and retained.returnProof.version==2,d.Describe(0,c))
assert(shared.EffectiveFacts.Read(0,c).potential==2 and shared.EffectiveFacts.Read(0,c).active==1)
local rev=retained.revision;Events.CityTransfered.Fire(0,500,3);assert(props[PREFIX..token].revision==rev)
boot();assert(shared.EffectiveFacts.Read(0,c).potential==2 and c.s.values.TOKEN==nil)
-- Per-record debit failure windows: no repeat unit consumption; unrelated P0 stays usable.
for _,offset in ipairs({1,2,3})do
 start();local aCity=fresh(1);register(aCity);complete(aCity,'DISTRICT_CAMPUS')
 local bCity=fresh(2);register(bCity);local frozen=encode(record(bCity))
 local key=PREFIX..aCity.s.values.TOKEN;local target=(perKey[key]or 0)+offset
 local real=Game.SetProperty
 Game.SetProperty=function(o,k,v)if k==key and (perKey[k]or 0)+1==target then failKey=k end;return real(o,k,v)end
 addunit(999,aCity);assert(a.Prepare(0,aCity,999,'FAIL_WINDOW',false):find('PREPARED'))
 assert(a.Confirm(0,aCity,shared.InvestmentPreview.token):find('HELD'))
 local killed=kills;Game.SetProperty=real;failKey=nil;saved=true;boot()
 assert(kills==killed and encode(record(bCity))==frozen and shared.EffectiveFacts.Read(0,bCity).potential==0)
 if offset==1 then assert(shared.EffectiveFacts.Read(0,aCity).potential==1)
 elseif offset==2 then assert(shared.EffectiveFacts.Read(0,aCity).investmentPending)
 else assert(shared.EffectiveFacts.Read(0,aCity).potential==2)end
end
-- A partial record reservation/readback failure survives load without legacy adoption.
start();c=fresh(1);failKey=PREFIX..'DEV-B013-P0-1';register(c);assert(not record(c))
failKey=nil;saved=true;boot();assert(d.Owns(c) and not pcall(shared.EffectiveFacts.Read,0,c))
local other=fresh(2);register(other);assert(shared.EffectiveFacts.Read(0,other).potential==0)
-- New-save init/index failure never rolls onward or modifies old authority.
start();props={};failKey=INDEX;boot();assert(next(props)==nil)
start();local q={schema=3,counter=1,entries={['DEV-B013-P0-1']={owner=0,cityID=101,x=2,y=5,serial=2}}}
props[INDEX]=q;saved=true;boot();assert(d.Describe(0):find('INDEX_ENTRY'))

clean();print('B108 LOCAL_SIMULATION_PASS: production multi-city authority, compact bindings, record-local writes/faults, old writer cutoff, new-save gate, loss/return/current facts')
''')

for p in (R/'Mod').rglob('*.lua'):
 l.execute('assert(load(...))',p.read_text())
import xml.etree.ElementTree as ET
assert ET.parse(R/'Mod/SpecializationP0.modinfo').getroot().attrib['version']=='135'
g=(R/'Mod/Gameplay.lua').read_text()
assert 'SPCCityProgressionStore.Start(P,shared)' in g and 'StartLegacyTest' not in g
ui=(R/'Mod/UI/P0Panel.lua').read_text()
assert 'Controls.InheritRecordButton:SetHide(true)' in ui
for name in ['BindingProbe','CityFlowProbe','CityJournalProbe','CompletionRecordProbe']:
 assert 'UsesNewAuthority' in (R/'Mod'/f'{name}.lua').read_text()
print('B108 STATIC_CONFIRMED: all Lua compile, modinfo135, production dispatch, retired migration UI / old listeners')
