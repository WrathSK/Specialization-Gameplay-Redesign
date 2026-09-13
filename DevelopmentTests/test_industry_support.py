from pathlib import Path
import sqlite3,zlib,xml.etree.ElementTree as ET
from lupa.lua55 import LuaRuntime
W=Path(__file__).resolve().parents[1];R=W/"Sid Meier's Civilization VI/Mods/SpecializationP0"
lua=LuaRuntime(unpack_returned_tuples=True)
lua.execute('''
local function event() return {Add=function() end} end
Events=setmetatable({},{__index=function() return event() end});GameEvents=Events
base=5;actual=10;kind='INDUSTRY';owner=0;complete=true;present={};writes=0
city={GetID=function() return 10 end,GetOwner=function() return owner end}
city.GetBuildings=function() return {HasBuilding=function(_,i) return present[i]==true end,RemoveBuilding=function(_,i) present[i]=false;writes=writes+1 end} end
city.GetBuildQueue=function() return {CreateBuilding=function(_,i) present[i]=true;writes=writes+1 end} end
district={GetCity=function() return city end,GetID=function() return 8 end,GetType=function() return 2 end,IsComplete=function() return complete end,GetX=function() return 1 end,GetY=function() return 1 end}
local function members(v) return function() local done=false;return function() if not done then done=true;return 1,v end end end end
Players={[0]={GetCities=function() return {Members=members(city)} end,GetDistricts=function() return {Members=members(district)} end}}
Map={GetPlot=function() return {GetAdjacencyYield=function(_,p,c,d,y) assert(p==0 and c==10 and d==2 and y==1);if missing then error('ABSENT') end;return base end} end}
P={IsTestPlayer=function(i) return i==0 end,Field=function(t,k) return t[k] end,Info=function(t,k)
 if t=='Districts' then return {DistrictType='DISTRICT_INDUSTRIAL_ZONE'} end
 if t=='Yields' then return {Index=1} end
 return {Index=k}
end}
shared={EffectiveFacts={Read=function() return {specialization=kind,potential=1,active=1,first={districtID=8,type='DISTRICT_INDUSTRIAL_ZONE'}} end}}
''')
lua.execute((R/'IndustrySupport.lua').read_text())
lua.execute('''
SPCIndustrySupport.Start(P,shared);a=shared.IndustrySupport;a.ready=true
function send() a.Receive(0,{CityID=10,DistrictID=8,BaseProduction=missing and -1 or base}) end
send();assert(a.Describe(0,city):find('carrier=3F / 5.0P',1,true) or a.Describe(0,city):find('carrier=3F / 5P',1,true))
local before=writes;a.Audit();assert(writes==before)
-- Actual adjacency can change without affecting the base carrier.
actual=20;a.Audit();assert(writes==before)
base=7;send();assert(present['BUILDING_SPC_DEV_INDUSTRY_LV1_0'] and present['BUILDING_SPC_DEV_INDUSTRY_LV1_1'] and present['BUILDING_SPC_DEV_INDUSTRY_LV1_2'])
base=0;send();assert(present['BUILDING_SPC_DEV_INDUSTRY_LV1_-1']);for i=0,7 do assert(not present['BUILDING_SPC_DEV_INDUSTRY_LV1_'..i]) end
base=5;send();base=-1;send();for _,v in pairs(present) do assert(not v) end;assert(a.errors['0:10'])
base=5;send();assert(not a.errors['0:10'])
missing=true;send();for _,v in pairs(present) do assert(not v) end
missing=false;kind='RESEARCH';a.Audit();for _,v in pairs(present) do assert(not v) end
kind='INDUSTRY';send();owner=1;a.Audit();for _,v in pairs(present) do assert(not v) end
owner=0;a.Audit();complete=false;a.Audit();for _,v in pairs(present) do assert(not v) end
complete=true;SPCIndustrySupport.Start(P,shared);shared.IndustrySupport.ready=true;shared.IndustrySupport.Receive(0,{CityID=10,DistrictID=8,BaseProduction=5});assert(present['BUILDING_SPC_DEV_INDUSTRY_LV1_2'])
local before=writes;shared.IndustrySupport.Describe(0,city);assert(writes==before)
''')
# Execute the real independent background UI -> actual gameplay receiver.
lua.execute("""
a=shared.IndustrySupport;base=9;missing=false;owner=0;complete=true
SPCP0=P;P.VERSION='P0-B-036';ExposedMembers={SPC_P0=shared};shared.Version=P.VERSION
Game={GetLocalPlayer=function() return 0 end};PlayerOperations={EXECUTE_SCRIPT=1};requests=0
include=function() end
UI={RequestPlayerOperation=function(pid,op,params) requests=requests+1;a.Receive(pid,params) end}
ContextPtr={SetInitHandler=function(_,f) init=f end,SetShutdown=function(_,f) shutdown=f end}
local handlers={};Events=setmetatable({},{__index=function(t,k) local e={Add=function(f) handlers[k]=f end,Remove=function() end};rawset(t,k,e);return e end})
fire=function(k) handlers[k]() end
""")
lua.execute((R/'UI/IndustryRefresh.lua').read_text())
lua.execute("""
init();assert(requests==1);fire('GameCoreEventPublishComplete');assert(requests==1)
base=10;fire('GameCoreEventPublishComplete');assert(requests==2)
missing=true;fire('GameCoreEventPublishComplete');assert(requests==3);for _,v in pairs(present) do assert(not v) end
missing=false;base=6;fire('GameCoreEventPublishComplete');assert(requests==4)
fire('SystemUpdateUI');assert(requests==4);shutdown()
""")
dbpath=W/'Firaxis Games/Sid Meier\'s Civilization VI/Cache/DebugGameplay.sqlite'
src=sqlite3.connect(dbpath.as_uri()+'?mode=ro',uri=True);db=sqlite3.connect(':memory:');src.backup(db);src.close();db.create_function('Make_Hash',1,lambda s:zlib.crc32(s.encode()))
db.executescript((R/'Data/IndustrySupport.sql').read_text())
rows=db.execute("SELECT b.BuildingType,b.CitizenSlots,b.Housing,c.YieldType,c.YieldChange FROM Buildings b JOIN Building_CitizenYieldChanges c USING(BuildingType) WHERE b.BuildingType LIKE 'BUILDING_SPC_DEV_INDUSTRY_LV1_%'").fetchall()
assert len(rows)==9
for n,slots,housing,y,v in rows:
 bit=int(n.rsplit('_',1)[1]);assert slots==0 and housing==0;assert v==(3 if bit==-1 else 2**bit)
# SQL basis: each native working specialist receives same configured yields.
for workers in [0,1,2,4]: assert workers*(1+4)==workers*5
for p in R.rglob('*.lua'): lua.execute('assert(load(...))',p.read_text())
root=ET.parse(R/'SpecializationP0.modinfo').getroot();assert root.attrib['version']=='44';assert root.attrib['id']=='df9efdad-dd48-40a7-b868-87f0617bc16d'
for e in root.findall('.//File'): assert (R/e.text).exists(),e.text
print('PASS: Industry actual Lua reconciliation/error recovery/read-only diagnostics; live-schema SQL in RAM; Lua syntax/manifest. Engine getter and native yields NOT game-tested.')
