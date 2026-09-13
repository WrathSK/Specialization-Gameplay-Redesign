"""B035 real module + signal dispatch; SQLite in memory, native GPP multiplier is a mock."""
from pathlib import Path
import sqlite3,zlib,xml.etree.ElementTree as ET
from lupa.lua55 import LuaRuntime
W=Path(__file__).resolve().parents[1];R=W/"Sid Meier's Civilization VI/Mods/SpecializationP0"
source=sqlite3.connect((W/"Firaxis Games/Sid Meier's Civilization VI/Cache/DebugGameplay.sqlite").as_uri()+'?mode=ro',uri=True)
c=sqlite3.connect(':memory:');source.backup(c);source.close();c.row_factory=sqlite3.Row
c.create_function('Make_Hash',1,lambda s:zlib.crc32(s.encode())) # fixture only
c.executescript((R/'Data/Lv2GPP.sql').read_text())
bs=[dict(x) for x in c.execute("select * from Buildings where BuildingType like 'BUILDING_SPC_DEV_GPP_%'")]
points=[dict(x) for x in c.execute("select * from Building_GreatPersonPoints where BuildingType like 'BUILDING_SPC_DEV_GPP_%'")]
assert len(bs)==32 and len(points)==48
assert all(b['Housing']==0 and b['CitizenSlots']==0 and b['InternalOnly']==1 for b in bs)
assert not c.execute("select * from Building_CitizenYieldChanges where BuildingType like 'BUILDING_SPC_DEV_GPP_%'").fetchall()
for b in bs:
 bit=int(b['BuildingType'].rsplit('_',1)[1]);ps=[p for p in points if p['BuildingType']==b['BuildingType']]
 assert len(ps)==(3 if '_CULTURE_' in b['BuildingType'] else 1)
 assert all(p['PointsPerTurn']==2*2**bit for p in ps)
l=LuaRuntime(unpack_returned_tuples=True)
l.globals().buildings=l.table_from([l.table_from(dict(b,Index=1000+i)) for i,b in enumerate(bs)])
l.globals().points=l.table_from([l.table_from(p) for p in points])
l.execute((R/'Lv2GPP.lua').read_text())
l.execute(r'''
local function event()
 local e={handlers={}};e.Add=function(f) table.insert(e.handlers,f) end
 e.Remove=function(f) for i=#e.handlers,1,-1 do if e.handlers[i]==f then table.remove(e.handlers,i) end end end
 e.fire=function(...) for _,f in ipairs(e.handlers) do f(...) end end;return e
end
function bus()
 Events={};GameEvents={}
 for _,n in ipairs({'CityWorkerChanged','CityFocusChanged','GovernorAssigned','GovernorEstablished','GovernorChanged','PlayerTurnActivated','PlayerTurnDeactivated','CityTransfered','LoadScreenClose','GameCoreEventPublishComplete','GameCoreEventPlaybackComplete','SystemUpdateUI'}) do Events[n]=event() end
 for _,n in ipairs({'OnDistrictConstructed','BuildingConstructed','CityBuilt'}) do GameEvents[n]=event() end
end
local info={Buildings={},Districts={},GreatPersonClasses={}}
for _,b in ipairs(buildings) do info.Buildings[b.BuildingType]=b end
local kinds={'RESEARCH','CULTURE','INDUSTRY','COMMERCE'}
local ds={'DISTRICT_CAMPUS','DISTRICT_THEATER','DISTRICT_INDUSTRIAL_ZONE','DISTRICT_COMMERCIAL_HUB'}
local classes={'SCIENTIST','WRITER','ARTIST','MUSICIAN','ENGINEER','MERCHANT'}
for i,cl in ipairs(classes) do info.GreatPersonClasses['GREAT_PERSON_CLASS_'..cl]={Index=i} end
local cities,districts={},{}
for i=1,4 do
 local city={owner=0,id=i,present={},workers=0,writes=0}
 city.GetID=function() return city.id end;city.GetOwner=function() return city.owner end
 city.f={specialization=kinds[i],active=2,first={districtID=i,type=ds[i]}}
 city.GetBuildings=function() return {HasBuilding=function(_,id) return city.present[id]==true end,
 RemoveBuilding=function(_,id) city.present[id]=nil;city.writes=city.writes+1;GameEvents.BuildingConstructed.fire() end} end
 city.GetBuildQueue=function() return {CreateBuilding=function(_,id) city.present[id]=true;city.writes=city.writes+1;GameEvents.BuildingConstructed.fire() end} end
 cities[i]=city;info.Districts[i]={DistrictType=ds[i]}
 districts[i]={GetCity=function() return city end,GetID=function() return i end,GetType=function() return i end,
 IsComplete=function() return true end,GetX=function() return i end,GetY=function() return 0 end}
end
Players={[0]={GetCities=function() return {Members=function() return ipairs(cities) end,FindID=function(_,id) return cities[id] end} end,
 GetDistricts=function() return {Members=function() return ipairs(districts) end} end,
 GetGreatPeoplePoints=function() return {GetPointsPerTurn=function(_,index) return 99+index end} end}}
Map={GetPlot=function(x,y) return {GetWorkerCount=function() return cities[x].workers end} end}
P={VERSION='P0-B-035',Info=function(t,k) return info[t][k] end,Rows=function() return points end,
 Field=function(t,k) return t and t[k] end,IsTestPlayer=function(pid) return pid==0 end,Scalar=tostring}
shared={Version=P.VERSION,EffectiveFacts={Read=function(pid,city) if city.bad then error('BAD_IDENTITY') end;return city.f end}}
function boot() bus();SPCLv2GPP.Start(P,shared);Events.LoadScreenClose.fire() end
local function count(city,kind)
 local n=0
 for bit=0,7 do local b=info.Buildings['BUILDING_SPC_DEV_GPP_'..kind..'_'..bit];if city.present[b.Index] then n=n+2^bit end end
 return n
end
boot();for _,city in ipairs(cities) do assert(city.writes==0) end
-- Read never reconciles: native count changes alone do not fake an applied carrier.
cities[1].workers=1
assert(shared.Lv2GPP.Describe(0,cities[1]):find('expected=2 carrier=0',1,true));assert(cities[1].writes==0)
Events.CityWorkerChanged.fire();assert(count(cities[1],'RESEARCH')==1)
-- Four families, count 0/1/2/3/4 transitions, idempotent repeats and own district only.
for _,n in ipairs({1,2,3,4,2,0}) do
 for _,city in ipairs(cities) do city.workers=n end
 Events.CityWorkerChanged.fire()
 for i,city in ipairs(cities) do
  assert(count(city,kinds[i])==n)
  local before=city.writes;Events.CityFocusChanged.fire();assert(city.writes==before)
  for _,k in ipairs(kinds) do if k~=kinds[i] then assert(count(city,k)==0) end end
 end
end
-- Culture's native rows carry all three classes simultaneously (from executed SQL).
local city=cities[2];city.workers=3;Events.CityWorkerChanged.fire()
local actual={}
for _,p in ipairs(points) do
 if city.present[info.Buildings[p.BuildingType].Index] then actual[p.GreatPersonClassType]=(actual[p.GreatPersonClassType] or 0)+p.PointsPerTurn end
end
for _,cl in ipairs({'WRITER','ARTIST','MUSICIAN'}) do assert(actual['GREAT_PERSON_CLASS_'..cl]==6) end
-- GPP multiplier arithmetic is a fixture assertion only, not proof of native behavior.
assert(actual.GREAT_PERSON_CLASS_WRITER*1.25==7.5)
-- No stale benefit after loss of governor; no unrelated carrier deletion.
city.present[9999]=true;city.f.active=1;Events.GovernorAssigned.fire();assert(count(city,'CULTURE')==0 and city.present[9999])
city.f.active=2;Events.GovernorEstablished.fire();assert(count(city,'CULTURE')==3)
local before=city.writes;boot();assert(city.writes==before and count(city,'CULTURE')==3)
-- Saved derived corruption rebuilt; no dependency on diagnostic reads.
city.present[info.Buildings.BUILDING_SPC_DEV_GPP_RESEARCH_7.Index]=true
Events.PlayerTurnActivated.fire();assert(count(city,'RESEARCH')==0 and count(city,'CULTURE')==3)
city.bad=true;Events.CityWorkerChanged.fire();assert(count(city,'CULTURE')==0)
city.bad=false;Events.CityWorkerChanged.fire();assert(count(city,'CULTURE')==3)
city.f.active=nil;Events.GovernorChanged.fire();assert(count(city,'CULTURE')==0)
city.f.active=2;city.workers=256;Events.CityWorkerChanged.fire();assert(count(city,'CULTURE')==0 and shared.Lv2GPP.errors['0:2'])
city.workers=1;Events.CityWorkerChanged.fire();assert(count(city,'CULTURE')==1)
city.owner=1;Events.CityTransfered.fire();assert(count(city,'CULTURE')==0);city.owner=0
-- Unexpected load-order doubling is rejected, never accepted as the desired +2.
points[1].PointsPerTurn=points[1].PointsPerTurn*2;boot();assert(shared.Lv2GPP.errors['0:1']);assert(count(cities[1],'RESEARCH')==0)
points[1].PointsPerTurn=points[1].PointsPerTurn/2;boot()
-- Native read route may be unavailable without preventing the base effect.
Players[0].GetGreatPeoplePoints=function() return {} end
assert(shared.Lv2GPP.Describe(0,cities[1]):find('UNKNOWN',1,true))
fixture={city=cities[1],cities=cities}
''')
# Actual gameplay dispatch: dirty request cannot overwrite a report or trust supplied count.
l.execute("include=function() end;SPCP0=P;ExposedMembers={};GameEvents.SPC_P0_Request={Add=function(fn) dispatch=fn end}")
l.execute((R/'Gameplay.lua').read_text().split('shared.TradeEvents={}')[0])
l.execute('''
local g=ExposedMembers.SPC_P0;local audits=0;g.Snapshot='KEEP';g.LastToken='KEEP_TOKEN'
g.Lv2GPP={ready=true,Audit=function() audits=audits+1 end,Describe=function(pid,city) assert(pid==0 and city==fixture.city);return 'READ_ONLY' end}
dispatch(0,{Action='LV2_GPP_DIRTY',Token='X',Count=255});assert(audits==1 and g.Snapshot=='KEEP' and g.LastToken=='KEEP_TOKEN')
dispatch(1,{Action='LV2_GPP_DIRTY',Token='Y'});assert(audits==1)
dispatch(0,{Action='LV2_GPP_READ',Token='READ',CityID=1});assert(g.Snapshot=='READ_ONLY' and audits==1)
-- Background context has no controls; sends no counts and coalesces dirty events.
local requestCount=0;local pid=0;UI={RequestPlayerOperation=function(player,operation,params)
 assert(player==0 and params.Action=='LV2_GPP_DIRTY' and params.Count==nil and params.CityID==nil);requestCount=requestCount+1
end};PlayerOperations={EXECUTE_SCRIPT=1};Game={GetLocalPlayer=function() return pid end}
ContextPtr={SetInitHandler=function(_,fn) init=fn end,SetShutdown=function(_,fn) shutdown=fn end}
fixture.requests=function() return requestCount end;fixture.player=function(v) pid=v end
''')
l.execute((R/'UI/GPPRefresh.lua').read_text())
l.execute('''
init();assert(fixture.requests()==1)
Events.SystemUpdateUI.fire();assert(fixture.requests()==1)
Events.CityWorkerChanged.fire();Events.CityWorkerChanged.fire();Events.CityFocusChanged.fire()
Events.GameCoreEventPublishComplete.fire();assert(fixture.requests()==2)
Events.GameCoreEventPlaybackComplete.fire();assert(fixture.requests()==2)
fixture.player(1);Events.CityWorkerChanged.fire();Events.SystemUpdateUI.fire();assert(fixture.requests()==2)
fixture.player(0);Events.SystemUpdateUI.fire();assert(fixture.requests()==3)
shutdown();Events.CityWorkerChanged.fire();Events.SystemUpdateUI.fire();assert(fixture.requests()==3)
''')
l.execute((R/'GPPReadout.lua').read_text())
l.execute("""
Players[0].GetGreatPeoplePoints=function() return {GetPointsPerTurn=function(_,i) return i*10 end} end
local report='city=1 CULTURE ACTIVE=2 workers=1\\nNative EMPIRE GPP/turn: UNKNOWN\\ncarrier=2'
local result=SPCGPPReadout.Render(P,report)
assert(result:find('UI EMPIRE GPP/turn: WRITER:20 | ARTIST:30 | MUSICIAN:40',1,true))
assert(result:find('carrier=2',1,true))
""")
# Actual button request -> Gameplay ACK -> UI-native rate decoration.
l.execute(r"""
Controls={Status={SetText=function(_,s) rendered=s end}}
ContextPtr.ClearUpdate=function() end;ContextPtr.SetUpdate=function() end
Game.GetCurrentGameTurn=function() return 1 end
UI.GetHeadSelectedCity=function() return fixture.city end
UI.RequestPlayerOperation=function(pid,operation,params) dispatch(pid,params) end
ExposedMembers.SPC_P0.Lv2GPP.Describe=function() return 'city=1 CULTURE ACTIVE=2 workers=1\nNative EMPIRE GPP/turn: UNKNOWN' end
""")
request=l.execute((R/'UI/P0Panel.lua').read_text().split('local function copy(asBaseline)')[0]+'\nreturn request')
request('LV2_GPP_READ')
l.execute("assert(rendered:find('UI EMPIRE GPP/turn: WRITER:20',1,true))")
manifest=ET.parse(R/'SpecializationP0.modinfo').getroot();assert manifest.get('version')=='43' and manifest.get('id')=='df9efdad-dd48-40a7-b868-87f0617bc16d'
for e in manifest.findall('.//File'):assert (R/e.text).is_file(),e.text
assert manifest.find("./InGameActions/UpdateDatabase[@id='SPC_B035_GPP']/Properties/LoadOrder").text=='10001000'
for p in R.rglob('*.lua'):l.execute('assert(load(...))',p.read_text())
xml=ET.parse(R/'UI/P0Panel.xml');ids=[e.get('ID') for e in xml.iter() if e.get('ID')];assert len(ids)==len(set(ids)) and 'Lv2GPPButton' in ids
print('LOCAL_SIMULATION_PASS: actual GPP Lua four families/counts, revoke/load/idempotence, Culture three classes, SQL mismatch refusal, read-only request, independent no-controls dirty sender. Native multiplier/timing still USER_GAME_TEST_REQUIRED.')
print('STATIC_CONFIRMED: native SQL in isolated live schema (Make_Hash stub), 32 buildings/48 class rows, manifest/load order, UUID, Lua/XML.')
