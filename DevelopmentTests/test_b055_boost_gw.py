"""Real new Lua and SQL, native effects remain user-game-test-required."""
from pathlib import Path
import sys, os, sqlite3, json, math, zlib, importlib.util, xml.etree.ElementTree as ET
from lupa.lua55 import LuaRuntime
R=Path(__file__).resolve().parents[1];M=Path(os.environ.get('SPC_B055_MOD',R/'Mod'))
# Pure generated table verification (generator can be tested before installation).
spec=importlib.util.spec_from_file_location('gen',R/'tools/generate_boost.py');gen=importlib.util.module_from_spec(spec);spec.loader.exec_module(gen)
for path,s in gen.render().items():assert (M/Path(path).relative_to('Mod')).read_text()==s
# SQLite read-only external snapshot copied into memory; never touch source database.
config=Path(os.environ.get('SPC_B055_CONFIG',R/'local/config.json'))
db=sqlite3.connect('file:'+json.loads(config.read_text())['debug_gameplay_db']+'?mode=ro',uri=True)
c=sqlite3.connect(':memory:');db.backup(c);db.close();c.create_function('Make_Hash',1,lambda s:zlib.crc32(s.encode()))
# Clean only own namespace in the disposable copy if running after game DB has loaded B055.
for table,col in [('BuildingModifiers','ModifierId'),('ModifierArguments','ModifierId'),('Modifiers','ModifierId'),('Buildings','BuildingType'),('Types','Type')]:
 c.execute(f"delete from {table} where {col} like 'SPC_B055_%' or {col} like 'BUILDING_SPC_B055_%'")
for name in ['NetworkBoost.sql','GreatWorkProbe.sql']:c.executescript((M/'Data'/name).read_text())
assert c.execute("select count(*) from Buildings where BuildingType like 'BUILDING_SPC_B055_%'").fetchone()[0]==1034
assert not c.execute("select 1 from Modifiers m left join DynamicModifiers d on m.ModifierType=d.ModifierType where m.ModifierId like 'SPC_B055_%' and d.ModifierType is null").fetchall()
assert c.execute("select Value from ModifierArguments where ModifierId='SPC_B055_CULTURE_4_1' and Name='Amount'").fetchone()[0]=='4.5'
assert math.isclose(float(c.execute("select Value from ModifierArguments where ModifierId='SPC_B055_RESEARCH_2_8' and Name='Amount'").fetchone()[0]),2.2*math.sqrt(8))
assert not c.execute("select * from ModifierArguments where ModifierId like 'SPC_B055_GW_%' and Value in ('GREATWORKOBJECT_PRODUCT','GREATWORKOBJECT_RELIC')").fetchall()
assert c.execute("select count(*) from BuildingModifiers where BuildingType='BUILDING_SPC_B055_GW_OBJECT'").fetchone()[0]==7
# No foreign records changed by new SQL.
root=ET.parse(M/'SpecializationP0.modinfo').getroot();assert root.get('version')=='72'
assert root.get('id')=='df9efdad-dd48-40a7-b868-87f0617bc16d'
for el in root.findall('./Files/File'):assert (M/el.text).is_file(),el.text
lua=LuaRuntime(unpack_returned_tuples=True)
load=lua.eval('function(s,n) local f,e=load(s,n);assert(f,e);return true end')
for name in ['BoostConfig.lua','NetworkBoost.lua','GreatWorkProbe.lua','NetworkBridge.lua','Gameplay.lua','UI/BoostRefresh.lua','UI/BoostGreatWorkRead.lua','UI/P0Panel.lua']:
 load((M/name).read_text(),name)
# Setup API mocks with real NetworkBridge derive logic and current source/recipient facts.
lua.execute('''
function event() return {Add=function(f) end} end
Events=setmetatable({}, {__index=function(t,k) local e=event();rawset(t,k,e);return e end});GameEvents=Events
Game={GetCurrentGameTurn=function() return 1 end};ExposedMembers={};Locale={Lookup=function(x) return x end}
P={Field=function(t,k) return t[k] end,IsTestPlayer=function(p) return p==0 end}
local rows={}; local nextIndex=0
P.Info=function(t,k) if t~='Buildings' then return nil end if not rows[k] then nextIndex=nextIndex+1;rows[k]={Index=nextIndex,BuildingType=k} end return rows[k] end
function makeCity(id,pid,kind,active)
 local c={id=id,owner=pid,kind=kind,active=active,buildings={},writes=0}
 function c:GetID() return self.id end;function c:GetOwner() return self.owner end
 function c:GetName() return 'city'..self.id end
 function c:GetBuildings() return {HasBuilding=function(_,i) return self.buildings[i]==true end,RemoveBuilding=function(_,i) self.buildings[i]=nil;self.writes=self.writes+1 end} end
 function c:GetBuildQueue() return {CreateBuilding=function(_,i) self.buildings[i]=true;self.writes=self.writes+1 end} end
 return c
end
cities={makeCity(1,0,'COMMERCE',1),makeCity(2,0,'RESEARCH',2),makeCity(3,0,'RESEARCH',4),makeCity(4,0,'CULTURE',3),makeCity(5,0,'COMMERCE',1),makeCity(6,0,'RESEARCH',1)}
capital=cities[1];routes={}
local col={FindID=function(_,id) for _,c in ipairs(cities) do if c.id==id and c.owner==0 then return c end end end,GetCapitalCity=function() return capital end,Members=function() local i=0;return function() i=i+1;if cities[i] then return i,cities[i] end end end}
Players={[0]={GetCities=function() return col end,GetTrade=function() return {CountOutgoingRoutes=function() return #routes end} end}}
shared={EffectiveFacts={Read=function(pid,c) return {specialization=c.kind,active=c.active,potential=4} end}}
include=function() end
''')
for name in ['BoostConfig.lua','NetworkBridge.lua','NetworkBoost.lua','GreatWorkProbe.lua']:lua.execute((M/name).read_text())
lua.execute('''
SPCNetworkBridge.Start(P,shared);shared.NetworkBridge.ready=true
SPCNetworkBoost.Start(P,shared);SPCGreatWorkProbe.Start(P,shared)
function receive()
 local text={};for _,r in ipairs(routes) do text[#text+1]='0,'..r[1]..',0,'..r[2]..','..r[3] end
 seq=(seq or 0)+1
 shared.NetworkBridge.Receive(0,{Epoch=shared.NetworkBridge.epoch,Seq=seq,Turn=1,Signal=shared.RouteSignalRevision or 0,Valid=1,Count=#routes,Data=table.concat(text,';')})
end
local d=shared.NetworkBoost
receive();d.EnsureReady(0);assert(d.ready and d.plans[0].RESEARCH.amount==0)
routes={{2,1,10},{3,1,11},{4,1,12},{1,5,13},{1,5,14}};receive()
assert(d.plans[0].RESEARCH.n==2 and d.plans[0].RESEARCH.level==4)
assert(math.abs(d.plans[0].RESEARCH.amount-4.5*math.sqrt(2))<1e-10)
assert(d.plans[0].CULTURE.n==2 and d.plans[0].CULTURE.level==3)
local old=d.applied[0].RESEARCH.building;local writes=capital.writes
d.Audit();receive();assert(capital.writes==writes) -- repeated refresh does not reattach
cities[3].active=1;d.Audit();assert(d.plans[0].RESEARCH.level==2)
assert(not capital:GetBuildings():HasBuilding(P.Info('Buildings',old).Index))
routes={{4,1,12}};receive();assert(d.plans[0].RESEARCH.amount==0 and d.applied[0].RESEARCH==nil)
-- Invalid batch cannot preserve stale current networks.
shared.RouteSignalRevision=1;d.Audit();assert(d.applied[0].CULTURE==nil)
receive();assert(d.plans[0].CULTURE.n==1)
-- Capital transfer: previous host loses both carriers, current host receives one.
local oldCapital=capital;capital=cities[5];receive()
for _,r in pairs(SPCBoostConfig.rows) do assert(not oldCapital:GetBuildings():HasBuilding(P.Info('Buildings',r.building).Index)) end
-- Deliberately wrong persisted carrier is removed during reconstruction.
local wrong=SPCBoostConfig.rows['RESEARCH:4:129'].building
cities[6]:GetBuildQueue():CreateBuilding(P.Info('Buildings',wrong).Index)
SPCNetworkBoost.Start(P,shared);d=shared.NetworkBoost;d.EnsureReady(0)
assert(not cities[6]:GetBuildings():HasBuilding(P.Info('Buildings',wrong).Index))
assert(d.applied[0].CULTURE and not d.applied[0].RESEARCH)
-- Capital self source, with empty routes, is one real recipient.
capital=cities[2];routes={};receive();assert(d.plans[0].RESEARCH.n==1)
assert(d.plans[0].RESEARCH.amount==2.2)
-- Endpoint becomes unavailable: reject packet and remove effect.
routes={{2,1,1}};cities[1].owner=1;receive();assert(d.applied[0].RESEARCH==nil)
-- GW mutually exclusive, no repeated stacking, OFF and load cleanup.
local gw=shared.GreatWorkProbe;local c=cities[2]
gw.Run(0,c,'GW_OBJECT');local w=c.writes;gw.Run(0,c,'GW_OBJECT');assert(c.writes==w)
gw.Run(0,c,'GW_CITY');assert(not c:GetBuildings():HasBuilding(P.Info('Buildings','BUILDING_SPC_B055_GW_OBJECT').Index))
gw.Run(0,c,'GW_OFF');assert(not c:GetBuildings():HasBuilding(P.Info('Buildings','BUILDING_SPC_B055_GW_CITY').Index))
gw.Run(0,c,'GW_OBJECT');gw.Clean();assert(not c:GetBuildings():HasBuilding(P.Info('Buildings','BUILDING_SPC_B055_GW_OBJECT').Index))
assert(not pcall(gw.Run,1,c,'GW_CITY'))
''')
# Real readout methods: isolate one boost, retain decimal Δ and flag next-turn contamination.
lua.execute((M/'UI/BoostGreatWorkRead.lua').read_text())
lua.execute('''
Game.GetLocalPlayer=function() return 0 end
local function iterator(r) return function() local done=false;return function() if not done then done=true;return r end end end end
GameInfo={Technologies=iterator({Index=1,Name='Technology'}),Civics=iterator({Index=1,Name='Civic'})}
boosted=false;progress=0
local tech={GetResearchCost=function() return 1000 end,GetResearchProgress=function() return progress end,HasBoostBeenTriggered=function() return boosted end}
local civic={GetCultureCost=function() return 1000 end,GetCulturalProgress=function() return 0 end,HasBoostBeenTriggered=function() return false end}
Players[0].GetTechs=function() return tech end;Players[0].GetCulture=function() return civic end
assert(SPCBoostGreatWorkRead.Boost(P,true):find('已记录'))
boosted=true;progress=411
assert(SPCBoostGreatWorkRead.Boost(P,false):find('41.100000'))
Game.GetCurrentGameTurn=function() return 2 end
assert(SPCBoostGreatWorkRead.Boost(P,false):find('跨回合'))
''')
print('B055 LOCAL_SIMULATION_PASS: generated floats; SQL 1034 carriers; real bridge Lmax/N union; no duplicate writes; downgrade/removal/stale/reload/capital/endpoint; GW exclusion/mutual exclusion/cleanup; native-readout arithmetic. Native application NOT tested.')
# UI startup when LoadScreenClose was never delivered: one successful handshake, no open panel.
u=LuaRuntime(unpack_returned_tuples=True)
u.execute('''
include=function() end
SPCP0={VERSION='test',Field=function(t,k) return t[k] end,IsTestPlayer=function(p) return p==0 end}
Game={GetLocalPlayer=function() return 0 end};PlayerOperations={EXECUTE_SCRIPT=1}
local d={ready=false};local gw={ready=false};ExposedMembers={SPC_P0={Version='test',NetworkBoost=d,GreatWorkProbe=gw}}
Events=setmetatable({}, {__index=function(t,k) local e={Add=function(f) t[k..'Handler']=f end};rawset(t,k,e);return e end})
ContextPtr={SetInitHandler=function(_,f) init=f end,SetShutdown=function() end}
sends=0;UI={RequestPlayerOperation=function(pid,op,p) assert(p.Action=='BOOST_INIT');sends=sends+1;d.ready=true;gw.ready=true end}
''')
u.execute((M/'UI/BoostRefresh.lua').read_text());u.execute("init();assert(sends==1);Events.SystemUpdateUIHandler();assert(sends==1)")
# Native work readout contract: count once, exclude product/relic, retain work types/eras.
u.execute((M/'UI/BoostGreatWorkRead.lua').read_text())
u.execute('''
Locale={Lookup=function(n) return n end}
GameInfo={Buildings=function() local i=0;return function() i=i+1;if i==1 then return {Index=1} end end end}
local works={{Name='Book',GreatWorkObjectType='GREATWORKOBJECT_WRITING',EraType='ERA_CLASSICAL'},{Name='Product',GreatWorkObjectType='GREATWORKOBJECT_PRODUCT'},{Name='Relic',GreatWorkObjectType='GREATWORKOBJECT_RELIC'}}
P={Info=function(t,k) if t=='GreatWorks' then return works[k] end return {Index=1} end}
local b={HasBuilding=function() return true end,GetNumGreatWorkSlots=function() return 3 end,GetBuildingYieldFromGreatWorks=function() return 8 end,GetBuildingTourismFromGreatWorks=function(_,religion) return religion and 1 or 3 end,GetGreatWorkInSlot=function(_,i,s) return s+1 end,GetGreatWorkTypeFromIndex=function(_,id) return id end}
local c={GetBuildings=function() return b end,GetYield=function() return 14.5 end}
local text=SPCBoostGreatWorkRead.Works(P,c);assert(text:find('作品=3 / 本实验合格=1') and text:find('作品旅游业=4.0000') and text:find('整城文化=14.5000'))
''')
print('B055 LOCAL_SIMULATION_PASS: missed-load startup handshake and native work readout/exclusion mocks.')
