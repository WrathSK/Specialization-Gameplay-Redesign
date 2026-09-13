from pathlib import Path
import sqlite3,zlib,xml.etree.ElementTree as E
from lupa.lua55 import LuaRuntime
w=Path(__file__).resolve().parents[1];r=w/"Sid Meier's Civilization VI/Mods/SpecializationP0";l=LuaRuntime(unpack_returned_tuples=True)
l.execute('''
local function event() return {Add=function() end} end
Events=setmetatable({},{__index=function() return event() end});GameEvents=Events
kind='RESEARCH';active=3;potential=3;base=6;complete=true;owner=0;writes=0;stored={}
local districts={RESEARCH='DISTRICT_CAMPUS',CULTURE='DISTRICT_THEATER',COMMERCE='DISTRICT_COMMERCIAL_HUB',INDUSTRY='DISTRICT_INDUSTRIAL_ZONE'}
city={GetOwner=function() return owner end,GetID=function() return 10 end}
city.GetBuildings=function() return {HasBuilding=function(_,n) return stored[n]==true end,RemoveBuilding=function(_,n) stored[n]=false;writes=writes+1 end} end
city.GetBuildQueue=function() return {CreateBuilding=function(_,n) stored[n]=true;writes=writes+1 end} end
d={GetCity=function() return city end,GetID=function() return 3 end,GetType=function() return 2 end,IsComplete=function() return complete end}
local function members(x) return function() local done=false;return function() if not done then done=true;return 1,x end end end end
Players={[0]={GetCities=function() return {Members=members(city)} end,GetDistricts=function() return {Members=members(d)} end}}
P={Field=function(t,k) return t[k] end,IsTestPlayer=function(p) return p==0 end,Info=function(t,k) if t=='Districts' then return {DistrictType=districts[kind]} end;return {Index=k} end}
shared={EffectiveFacts={Read=function() return {specialization=kind,active=active,potential=potential,first={districtID=3,type=districts[kind]}} end},IndustrySupport={ReadBase=function() if base==nil then error('BASE_PENDING') end;return base end}}
''')
l.execute((r/'Lv3Support.lua').read_text())
l.execute('''
SPCLv3Support.Start(P,shared);a=shared.Lv3Support;a.ready=true
for _,k in ipairs({'RESEARCH','CULTURE','COMMERCE','INDUSTRY'}) do
 kind=k;active=3;potential=3;a.Audit()
 assert(stored['BUILDING_SPC_DEV_LV3_'..k]);local count=writes;a.Audit();assert(writes==count)
 local t=a.Describe(0,city);assert(t:find('2F / ',1,true))
 if k=='INDUSTRY' then assert(t:find('0P / 12',1,true)) else assert(t:find('2P / 0G',1,true)) end
 active=2;a.Audit();for _,v in pairs(stored) do assert(not v) end
 active=nil;a.Audit();for _,v in pairs(stored) do assert(not v) end
end
kind='INDUSTRY';active=4;potential=4;base=1;a.Audit();assert(stored.BUILDING_SPC_DEV_LV3_INDUSTRY_GOLD_0)
base=4;a.Audit();assert(not stored.BUILDING_SPC_DEV_LV3_INDUSTRY_GOLD_0 and stored.BUILDING_SPC_DEV_LV3_INDUSTRY_GOLD_2)
base=0;a.Audit();assert(stored.BUILDING_SPC_DEV_LV3_INDUSTRY)
base=nil;a.Audit();for _,v in pairs(stored) do assert(not v) end;assert(a.errors['0:10'])
base=6;a.Audit();assert(not a.errors['0:10']);owner=1;a.Audit();for _,v in pairs(stored) do assert(not v) end
owner=0;complete=false;a.Audit();for _,v in pairs(stored) do assert(not v) end
complete=true;a.Audit();SPCLv3Support.Start(P,shared);a=shared.Lv3Support;a.ready=true;local n=writes;a.Audit();assert(writes==n);a.Describe(0,city);assert(writes==n)
''')
p=w/"Firaxis Games/Sid Meier's Civilization VI/Cache/DebugGameplay.sqlite";src=sqlite3.connect(p.as_uri()+'?mode=ro',uri=True);db=sqlite3.connect(':memory:');src.backup(db);src.close();db.create_function('Make_Hash',1,lambda s:zlib.crc32(s.encode()));db.executescript((r/'Data/Lv3Support.sql').read_text())
rows=db.execute("select BuildingType,YieldType,YieldChange from Building_CitizenYieldChanges where BuildingType like 'BUILDING_SPC_DEV_LV3_%'").fetchall();assert len(rows)==15
for k in ['RESEARCH','CULTURE','COMMERCE']:
 assert sorted((y,n) for b,y,n in rows if b=='BUILDING_SPC_DEV_LV3_'+k)==[('YIELD_FOOD',2),('YIELD_PRODUCTION',2)]
assert [(y,n) for b,y,n in rows if b=='BUILDING_SPC_DEV_LV3_INDUSTRY']==[('YIELD_FOOD',2)]
assert db.execute("select count(*) from Buildings where BuildingType like 'BUILDING_SPC_DEV_LV3_%' and (CitizenSlots<>0 or Housing<>0)").fetchone()[0]==0
for p in r.rglob('*.lua'):l.execute('assert(load(...))',p.read_text())
m=E.parse(r/'SpecializationP0.modinfo').getroot();assert m.get('version')=='46'
for e in m.findall('.//File'):assert (r/e.text).exists()
print('PASS actual Lv3 module four families, ACTIVE gates, idempotence, revoke/reload/read-only, Industry base dynamics/errors; RAM SQL 12 buildings/15 yield rows; Lua syntax and manifest46. No game proof.')
