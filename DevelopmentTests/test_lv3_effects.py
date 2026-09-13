from pathlib import Path
import sqlite3,zlib,xml.etree.ElementTree as E
from lupa.lua55 import LuaRuntime
w=Path(__file__).resolve().parents[1];r=w/"Sid Meier's Civilization VI/Mods/SpecializationP0"
p=w/'DevelopmentTests/test_lv3_support.py';scope={'__file__':str(p),'__name__':'fixture'};exec(compile(p.read_text().split('p=w/')[0],str(p),'exec'),scope);l=scope['l']
l.execute('''
workers=1;pop=3;city.GetPopulation=function() return pop end;d.GetX=function() return 1 end;d.GetY=function() return 1 end
Map={GetPlot=function() return {GetWorkerCount=function() return workers end} end}
connected={RESEARCH=true,CULTURE=true,INDUSTRY=true};netReady=true
shared.NetworkBridge={ConnectedKinds=function() assert(netReady,'NETWORK_REFRESH_PENDING');return connected end}
''')
l.execute((r/'Lv3Effects.lua').read_text())
l.execute('''
SPCLv3Effects.Start(P,shared);a=shared.Lv3Effects;a.ready=true
for _,k in ipairs({'RESEARCH','CULTURE'}) do
 stored={};kind=k;potential=3;active=3;workers=1;a.Audit();assert(stored['BUILDING_SPC_DEV_LV3_POP_'..k..'_0'])
 assert(a.Describe(0,city):find('1.5',1,true));local n=writes;a.Audit();assert(writes==n)
 workers=3;a.Audit();assert(stored['BUILDING_SPC_DEV_LV3_POP_'..k..'_0'] and stored['BUILDING_SPC_DEV_LV3_POP_'..k..'_1'])
 workers=0;a.Audit();for _,v in pairs(stored) do assert(not v) end
 workers=1;a.Audit();active=2;a.Audit();for _,v in pairs(stored) do assert(not v) end
end
kind='COMMERCE';active=3;workers=2;a.Audit()
for _,k in ipairs({'RESEARCH','CULTURE','INDUSTRY'}) do assert(stored['BUILDING_SPC_DEV_LV3_COM_'..k]) end
local n=writes;a.Audit();assert(writes==n)
connected.RESEARCH=nil;a.Audit();assert(not stored.BUILDING_SPC_DEV_LV3_COM_RESEARCH and stored.BUILDING_SPC_DEV_LV3_COM_CULTURE)
netReady=false;a.Audit();for _,v in pairs(stored) do assert(not v) end
netReady=true;a.Audit();assert(stored.BUILDING_SPC_DEV_LV3_COM_CULTURE)
SPCLv3Effects.Start(P,shared);a=shared.Lv3Effects;a.ready=true;n=writes;a.Audit();assert(writes==n)
''')
# Actual NetworkBridge, same-type duplicate sources and direct-vs-received distinction.
l.execute('''
P.VERSION='P0-B-038';ExposedMembers={};Game={GetCurrentGameTurn=function() return 1 end}
local function members(t) return function() return ipairs(t) end end
local cities={};for i=1,4 do cities[i]={GetID=function() return i end,GetOwner=function() return 0 end} end
Players={[0]={GetCities=function() return {FindID=function(_,i) return cities[i] end,GetCapitalCity=function() return cities[1] end,Members=members(cities)} end,GetTrade=function() return {CountOutgoingRoutes=function() return routeCount end} end}}
local kinds={[1]='RESEARCH',[2]='RESEARCH',[3]='COMMERCE',[4]='COMMERCE'}
local bridgeShared={EffectiveFacts={Read=function(_,c) return {potential=1,specialization=kinds[c:GetID()]} end},RouteSignalRevision=0}
bridgeFixture={cities=cities,shared=bridgeShared};routeCount=3
''')
l.execute((r/'NetworkBridge.lua').read_text())
l.execute('''
SPCNetworkBridge.Start(P,bridgeFixture.shared);b=bridgeFixture.shared.NetworkBridge;b.ready=true
b.Receive(0,{Epoch=b.epoch,Seq=1,Turn=1,Signal=0,Valid=1,Count=3,Data='0,1,0,3,11;0,2,0,3,12;0,3,0,4,13'})
local types=b.ConnectedKinds(0,bridgeFixture.cities[3]);assert(types.RESEARCH);local n=0;for _ in pairs(types) do n=n+1 end;assert(n==1)
assert(next(b.ConnectedKinds(0,bridgeFixture.cities[4]))==nil)
bridgeFixture.shared.RouteSignalRevision=1;assert(not pcall(b.ConnectedKinds,0,bridgeFixture.cities[3]))
''')
p=w/"Firaxis Games/Sid Meier's Civilization VI/Cache/DebugGameplay.sqlite";src=sqlite3.connect(p.as_uri()+'?mode=ro',uri=True);db=sqlite3.connect(':memory:');src.backup(db);src.close();db.create_function('Make_Hash',1,lambda s:zlib.crc32(s.encode()));db.executescript((r/'Data/Lv3Effects.sql').read_text())
assert db.execute("select count(*) from Modifiers where ModifierId like 'SPC_LV3_POP_%'").fetchone()[0]==16
assert float(db.execute("select Value from ModifierArguments where ModifierId='SPC_LV3_POP_RESEARCH_0' and Name='Amount'").fetchone()[0])==0.5
assert db.execute("select count(*) from Building_CitizenYieldChanges where BuildingType GLOB 'BUILDING_SPC_DEV_LV3_COM_*' and YieldChange=2").fetchone()[0]==3
for p in r.rglob('*.lua'):l.execute('assert(load(...))',p.read_text())
m=E.parse(r/'SpecializationP0.modinfo').getroot();assert m.get('version')=='48'
for x in m.findall('.//File'):assert (r/x.text).exists()
print('PASS actual effects module/bridge: worker bits, half-point configured basis, active revoke/load, type dedup/direct-only/stale rejection; new SQL in RAM and all Lua/manifest. Native fractional yields still need game test.')
