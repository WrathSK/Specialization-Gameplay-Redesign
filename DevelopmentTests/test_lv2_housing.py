"""B034 actual Lua reconciliation + current HD schema; no game launch / DB writes."""
from pathlib import Path
import sqlite3, zlib, xml.etree.ElementTree as ET
from lupa.lua55 import LuaRuntime
W=Path(__file__).resolve().parents[1]; R=W/"Sid Meier's Civilization VI/Mods/SpecializationP0"
l=LuaRuntime(unpack_returned_tuples=True)
l.execute((R/'Lv2Housing.lua').read_text())
l.execute(r'''
local function event()
 local e={handlers={}};e.Add=function(f) table.insert(e.handlers,f) end
 e.fire=function(...) for _,f in ipairs(e.handlers) do f(...) end end;return e
end
Events={};GameEvents={}
for _,n in ipairs({'LoadScreenClose','GovernorAssigned','GovernorEstablished','GovernorChanged','PlayerTurnActivated','CityTransfered','CityBuildingsChanged'}) do Events[n]=event() end
for _,n in ipairs({'BuildingConstructed','OnDistrictConstructed','CityBuilt'}) do GameEvents[n]=event() end
local info={Buildings={},Districts={}}
for i=0,8 do info.Buildings['BUILDING_SPC_DEV_LV2_HOUSING_'..i]={Index=100+i} end
local maps={};GameInfo={SPC_Lv2HousingTiers=function() local i=0;return function() i=i+1;return maps[i] end end}
local districts={'DISTRICT_CAMPUS','DISTRICT_THEATER','DISTRICT_COMMERCIAL_HUB','DISTRICT_INDUSTRIAL_ZONE'}
for i,d in ipairs(districts) do
 info.Districts[i]={DistrictType=d}
 for tier=1,5 do
  local b='TEST_'..i..'_'..tier;local index=i*10+tier
  info.Buildings[b]={Index=index};maps[#maps+1]={BuildingType=b,DistrictType=d,Tier=tier}
 end
end
info.Buildings.ALTERNATIVE={Index=99};maps[#maps+1]={BuildingType='ALTERNATIVE',DistrictType=districts[1],Tier=1}
local cities,ds={},{}
local function members(t) local i=0;return function() i=i+1;if t[i] then return i,t[i] end end end
Players={[0]={GetCities=function() return {Members=function() return members(cities) end} end,GetDistricts=function() return {Members=function() return members(ds) end} end}}
P={Info=function(t,k) return info[t][k] end,Field=function(t,k) return t[k] end,IsTestPlayer=function(pid) return pid==0 end}
s={EffectiveFacts={Read=function(pid,c) if c.bad then error('BAD_FACTS') end;return c.f end}}
local types={'RESEARCH','CULTURE','COMMERCE','INDUSTRY'}
for i=1,4 do
 local c={id=i,owner=0,buildings={},writes=0};cities[i]=c
 c.f={specialization=types[i],active=1,first={districtID=i,type=districts[i]}}
 c.GetID=function() return c.id end;c.GetOwner=function() return c.owner end
 c.GetBuildings=function() return {HasBuilding=function(_,id) return c.buildings[id]==true end,RemoveBuilding=function(_,id) c.buildings[id]=nil;c.writes=c.writes+1;GameEvents.BuildingConstructed.fire() end} end
 c.GetBuildQueue=function() return {CreateBuilding=function(_,id) c.buildings[id]=true;c.writes=c.writes+1;GameEvents.BuildingConstructed.fire() end} end
 ds[i]={GetCity=function() return c end,GetID=function() return i end,GetType=function() return i end,IsComplete=function() return not c.incomplete end}
end
SPCLv2Housing.Start(P,s)
Events.LoadScreenClose.fire()
for _,c in ipairs(cities) do assert(c.writes==0) end
-- Four families; base district + only own real tier. Read cannot enable anything.
for i,c in ipairs(cities) do
 c.f.active=2;c.buildings[i*10+1]=true
 local before=c.writes;assert(s.Lv2Housing.Describe(0,c):find('expected=+2 carrier=+0',1,true));assert(c.writes==before)
end
Events.GovernorEstablished.fire()
for _,c in ipairs(cities) do assert(c.buildings[100] and c.buildings[101]);assert(c.writes==2) end
local c=cities[1]
-- Alternative at same tier + unrelated district building never inflate housing.
c.buildings[99]=true;c.buildings[22]=true
GameEvents.BuildingConstructed.fire();assert(c.writes==2)
-- Higher tier adds one; repeated events idempotent; reentrant creation skipped.
c.buildings[12]=true;GameEvents.BuildingConstructed.fire();assert(c.writes==3 and c.buildings[102])
for i=1,5 do Events.GovernorChanged.fire() end;assert(c.writes==3)
-- Total remains when ACTIVE changes 2 -> 4; no worker dependency / bonus scaling.
c.f.active=4;Events.GovernorChanged.fire();assert(c.writes==3)
-- Governor moves; only Lv2 carriers removed. Real building and Lv1 stand-in survive.
c.buildings[500]=true;c.f.active=1;Events.GovernorAssigned.fire()
assert(not c.buildings[100] and not c.buildings[101] and not c.buildings[102]);assert(c.buildings[11] and c.buildings[500]);assert(c.writes==6)
c.f.active=2;Events.GovernorEstablished.fire();assert(c.writes==9)
-- Load destroys in-memory state; correct existing carrier set needs no writes.
local before=c.writes;SPCLv2Housing.Start(P,s);Events.LoadScreenClose.fire();assert(c.writes==before)
-- Corrupt disposable cache is reconstructed from facts, not retained as truth.
c.buildings[108]=true;c.buildings[101]=nil;Events.PlayerTurnActivated.fire();assert(not c.buildings[108] and c.buildings[101])
-- Lost building tier removes only corresponding carrier; alternative keeps tier1.
c.buildings[12]=nil;Events.CityBuildingsChanged.fire();assert(not c.buildings[102] and c.buildings[101])
c.buildings[11]=nil;Events.CityBuildingsChanged.fire();assert(c.buildings[101])
c.buildings[99]=nil;Events.CityBuildingsChanged.fire();assert(not c.buildings[101] and c.buildings[100])
-- Unknown governor clears advanced effects; invalid facts recover on next event.
c.f.active=nil;Events.GovernorChanged.fire();assert(not c.buildings[100])
c.f.active=2;c.bad=true;Events.GovernorChanged.fire();assert(not c.buildings[100])
c.bad=false;Events.GovernorChanged.fire();assert(c.buildings[100])
c.incomplete=true;Events.PlayerTurnActivated.fire();assert(not c.buildings[100])
c.incomplete=false;Events.PlayerTurnActivated.fire();assert(c.buildings[100])
-- Wrong-owner state cannot retain effect; other cities unaffected.
c.owner=1;Events.CityTransfered.fire();assert(not c.buildings[100]);assert(cities[2].buildings[100])
''')
print('LOCAL_SIMULATION_PASS: real housing Lua: four families, gates, tiers, alternative dedup, recovery, revoke, reentrant/idempotent, read-only')
# Copy live schema/data into RAM; never write the live database.
src=sqlite3.connect((W/"Firaxis Games/Sid Meier's Civilization VI/Cache/DebugGameplay.sqlite").as_uri()+'?mode=ro',uri=True)
c=sqlite3.connect(':memory:');src.backup(c);src.close()
assert not c.execute("select name from sqlite_master where name='SPC_Lv2HousingTiers'").fetchall()
# Engine hash function is a fixture, not a verified Civ VI hash implementation.
c.create_function('Make_Hash',1,lambda text:zlib.crc32(text.encode()))
c.executescript((R/'Data/Lv2Housing.sql').read_text())
rows=dict(c.execute('select BuildingType,Tier from SPC_Lv2HousingTiers'))
assert len(rows)==50
for b,t in {'BUILDING_LIBRARY':1,'BUILDING_JNR_ACADEMY':1,'BUILDING_UNIVERSITY':2,'BUILDING_JNR_ARCHITECTURE':3,'BUILDING_RESEARCH_LAB':4,'BUILDING_HD_DATA_CENTER':5,'BUILDING_JNR_GRAND_HOTEL':3,'BUILDING_MUSEUM_ART':3,'BUILDING_FAIR':1,'BUILDING_MARKET':2,'BUILDING_BANK':3,'BUILDING_STOCK_EXCHANGE':4,'BUILDING_IZ_WATER_MILL':1,'BUILDING_WORKSHOP':2,'BUILDING_FACTORY':3,'BUILDING_COAL_POWER_PLANT':4}.items():assert rows[b]==t,(b,rows[b],t)
assert all('_DUMMY_' not in b and '_SPC_' not in b for b in rows)
assert c.execute("select count(*),sum(Housing) from Buildings where BuildingType like 'BUILDING_SPC_DEV_LV2_HOUSING_%'").fetchone()==(9,9)
assert not c.execute("select * from Building_GreatPersonPoints where BuildingType like 'BUILDING_SPC_DEV_LV2_HOUSING_%'").fetchall()
assert not c.execute("select * from pragma_foreign_key_check where \"table\"='SPC_Lv2HousingTiers'").fetchall()
manifest=ET.parse(R/'SpecializationP0.modinfo').getroot()
assert manifest.attrib=={'id':'df9efdad-dd48-40a7-b868-87f0617bc16d','version':'42'}
for f in manifest.findall('.//File'):assert (R/f.text).is_file(),f.text
assert [f.text for f in manifest.findall('./InGameActions/ImportFiles/File')].count('Lv2Housing.lua')==1
assert [f.text for f in manifest.findall('./InGameActions/UpdateDatabase/File')].count('Data/Lv2Housing.sql')==1
for p in R.rglob('*.lua'):l.execute('assert(load(...))',p.read_text())
xml=ET.parse(R/'UI/P0Panel.xml');ids=[x.get('ID') for x in xml.iter() if x.get('ID')];assert len(ids)==len(set(ids));assert 'Lv2HousingButton' in ids
print('STATIC_CONFIRMED: isolated live HD schema SQL, 50 reviewed tiers, native integer housing only, manifest/UUID/assets/Lua/XML')
