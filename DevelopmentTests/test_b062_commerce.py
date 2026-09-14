from pathlib import Path
from lupa.lua55 import LuaRuntime
import sqlite3,json,zlib,xml.etree.ElementTree as ET,subprocess
R=Path(__file__).resolve().parents[1];M=R/'Mod'
s=(R/'DevelopmentTests/test_b060_request_recovery.py').read_text().replace('"78","85"','"78","88"').replace("'\\\"78\\\",\\\"85\\\"'","'\\\"78\\\",\\\"88\\\"'")
exec(compile(s,__file__,'exec'))
l=LuaRuntime(unpack_returned_tuples=True)
l.execute('''
include=function() end;turn=1;count=0;writes=0
local noop={Add=function() end};Events=setmetatable({},{__index=function() return noop end});GameEvents=Events
Game={GetCurrentGameTurn=function() return turn end,GetLocalPlayer=function() return 0 end};ExposedMembers={}
cities={};function make(id,k,active,values)
 local c={id=id,kind=k,active=active,values=values,b={}}
 c.GetID=function() return id end;c.GetOwner=function() return 0 end;c.GetName=function() return 'City'..id end
 c.GetYield=function(_,y) return c.values[y] or 0 end
 c.GetBuildings=function() return {HasBuilding=function(_,id) return c.b[id]==true end,RemoveBuilding=function(_,id) c.b[id]=nil;writes=writes+1 end} end
 c.GetBuildQueue=function() return {CreateBuilding=function(_,id) c.b[id]=true;writes=writes+1 end} end
 cities[id]=c;return c
end
make(1,'RESEARCH',1,{SCIENCE=28.4219});make(2,'COMMERCE',4,{SCIENCE=6});make(3,'RESEARCH',4,{SCIENCE=20});make(4,'COMMERCE',4,{});make(5,'CULTURE',4,{CULTURE=61});make(6,'INDUSTRY',4,{PRODUCTION=89})
Players={[0]={GetCities=function() return {FindID=function(_,id) return cities[id] end,Members=function() return pairs(cities) end,GetCapitalCity=function() return cities[1] end} end,GetTrade=function() return {CountOutgoingRoutes=function() return count end} end}}
P={VERSION='test',IsTestPlayer=function(pid) return pid==0 end,Field=function(t,k) return t[k] end,Info=function(t,k) if t=='Yields' then return {Index=k:gsub('YIELD_','')} end;if t=='Buildings' then return {Index=k} end end}
shared={Version='test',RouteSignalRevision=0,EffectiveFacts={Read=function(pid,c) return {specialization=c.kind,active=c.active,potential=4} end}};ExposedMembers.SPC_P0=shared;Locale={Lookup=function(s) return s end}
''')
for f in ['NetworkBridge.lua','NetworkSender.lua','CommerceConvergence.lua']:l.execute((M/f).read_text())
l.execute('''
SPCNetworkBridge.Start(P,shared);n=shared.NetworkBridge;n.ready=true;SPCCommerceConvergence.Start(P,shared);d=shared.CommerceConvergence
PlayerOperations={EXECUTE_SCRIPT=1};calls=0
UI={RequestPlayerOperation=function(pid,op,a)
 calls=calls+1;packet=a
 -- Boundary fixture: an empty Count/Data may disappear; native behavior is not assumed proved.
 if a.Count==0 then a.Count=nil end;if a.Data=='' then a.Data=nil end
 n.Receive(pid,a);return true
end}
local send=SPCNetworkSender.New(P)
local public={status='COMPLETE_UI_SHADOW',generation=1,snapshot={count=0,turn=turn,signal=0,keys={},routes={}}}
send(public);assert(n.players[0].reason=='READY_BACKGROUND_UI' and #n.players[0].routes==0);assert(packet.WireCount==1 and packet.Data=='EMPTY')
local before=calls;for i=1,100 do send(public) end;assert(calls==before)
local routes={a={originPlayer=0,originCityID=1,destinationPlayer=0,destinationCityID=2,traderUnitID=10},b={originPlayer=0,originCityID=3,destinationPlayer=0,destinationCityID=2,traderUnitID=11},c={originPlayer=0,originCityID=2,destinationPlayer=0,destinationCityID=4,traderUnitID=12}}
public.generation=2;count=3;public.snapshot={count=3,turn=turn,signal=0,keys={'a','b','c'},routes=routes};send(public)
assert(d.last['0:2'].amount.SCIENCE==5 and d.last['0:4'].amount.SCIENCE==0)
local plan=d.Plan(0,cities[2]);assert(plan.source.SCIENCE==1 and plan.basis.SCIENCE==28.4219)
local before=writes;for i=1,100 do d.Audit() end;assert(writes==before)
d.Control(0,cities[2],'OFF');assert(next(cities[2].b)==nil)
d.Control(0,cities[2],'TEST5');for _,y in ipairs({'SCIENCE','CULTURE','PRODUCTION'}) do assert(cities[2].b['BUILDING_SPC_B061_'..y..'_0'] and cities[2].b['BUILDING_SPC_B061_'..y..'_2']) end
assert(d.Describe(0,cities[2]):find('载体=5') and d.Describe(0,cities[2]):find('OFF差值'))
d.Control(0,cities[2],'AUTO');assert(d.last['0:2'].amount.SCIENCE==5 and d.last['0:2'].amount.CULTURE==0)
cities[3].values.SCIENCE=40;d.Audit();assert(d.last['0:2'].amount.SCIENCE==8)
cities[2].active=3;d.Audit();assert(next(cities[2].b)==nil);cities[2].active=4
-- A full zero snapshot removes old routes and grants; old same-count history never survives.
count=0;turn=2;public.generation=3;public.snapshot={count=0,turn=turn,signal=0,keys={},routes={}};send(public)
assert(n.players[0].turn==2 and #n.players[0].routes==0 and next(cities[2].b)==nil)
-- Missing nonempty payload and count conflict remain invalid; sentinel is not a wildcard.
n.Receive(0,{Epoch=n.epoch,Seq=100,Turn=turn,Signal=0,Valid=1,WireCount=2,Data='EMPTY'});assert(n.players[0].routes==nil)
n.Receive(0,{Epoch=n.epoch,Seq=101,Turn=turn,Signal=0,Valid=1,WireCount=1,Count=1,Data='EMPTY'});assert(n.players[0].reason=='WIRE_COUNT_CONFLICT')
-- Load-time cleanup of a saved old carrier, even without a usable network.
cities[2].b.BUILDING_SPC_B061_SCIENCE_2=true;SPCCommerceConvergence.Start(P,shared);shared.CommerceConvergence.Audit();assert(next(cities[2].b)==nil)
''')
# Baseline itself rejects the lossy zero packet: defect predates B061.87 retry changes.
old=subprocess.check_output(['git','show','3382d7d:Mod/NetworkBridge.lua'],cwd=R,text=True);l.execute(old);l.execute("SPCNetworkBridge.Start(P,shared);local b=shared.NetworkBridge;b.ready=true;b.Receive(0,{Epoch=b.epoch,Seq=1,Turn=turn,Signal=0,Valid=1});assert(b.players[0].reason=='BATCH_LIMIT_OR_SHAPE')")
src=sqlite3.connect('file:'+json.loads((R/'local/config.json').read_text())['debug_gameplay_db']+'?mode=ro',uri=True);db=sqlite3.connect(':memory:');src.backup(db);src.close();db.create_function('Make_Hash',1,lambda s:zlib.crc32(s.encode()))
for t,c in [('BuildingModifiers','ModifierId'),('ModifierArguments','ModifierId'),('Modifiers','ModifierId'),('Buildings','BuildingType'),('Types','Type')]:db.execute(f"delete from {t} where {c} like 'SPC_B061_%' or {c} like 'BUILDING_SPC_B061_%'")
db.executescript((M/'Data/CommerceConvergence.sql').read_text());assert db.execute("select Value from ModifierArguments where ModifierId='SPC_B061_SCIENCE_2' and Name='Amount'").fetchone()[0]=='4'
for p in M.rglob('*.lua'):l.eval('function(s) assert(load(s)) end')(p.read_text())
x=ET.parse(M/'SpecializationP0.modinfo');assert x.getroot().get('version')=='88'
for f in x.findall('.//File'):assert (M/f.text).is_file()
assert (M/'UI/BackgroundRoutes.lua').read_bytes()==subprocess.check_output(['git','show','3382d7d:Mod/UI/BackgroundRoutes.lua'],cwd=R)
print('B062 LOCAL_SIMULATION_PASS: old-baseline loss reproduced; actual sender/receiver explicit empty, nonempty->empty withdrawal, malformed rejection; direct max/floor/not level/no distribution; idempotence/OFF/TEST5/AUTO/ACTIVE/load; SQL bits; unchanged background scanner; full prior regression.')
