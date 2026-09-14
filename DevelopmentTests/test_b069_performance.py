"""B069 real Lua event pipeline; no Civ VI launch. Counters and native writes compared."""
from pathlib import Path
from lupa.lua55 import LuaRuntime
import xml.etree.ElementTree as ET
R=Path(__file__).resolve().parents[1];M=R/'Mod'
l=LuaRuntime(unpack_returned_tuples=True)
l.globals().include=lambda name:l.execute((M/(name+'.lua')).read_text())
l.execute("""
turn=1;prints=0;print=function() prints=prints+1 end
Game={GetCurrentGameTurn=function() return turn end,GetLocalPlayer=function() return 0 end};ExposedMembers={}
function eventTable()
 return setmetatable({},{__index=function(t,k) local rows={};local e={Add=function(f) rows[#rows+1]=f end,Remove=function(f) for i=#rows,1,-1 do if rows[i]==f then table.remove(rows,i) end end end,Fire=function(...) for _,f in ipairs(rows) do f(...) end end};rawset(t,k,e);return e end})
end
GE=eventTable();UE=eventTable();Events=GE;GameEvents=eventTable()
PlayerConfigurations={[0]={GetCivilizationTypeName=function() return 'CIVILIZATION_SPC_TEST' end,GetLeaderTypeName=function() return 'LEADER_SPC_TEST' end}}
GameInfo={Units={[1]={MakeTradeRoute=false},[2]={MakeTradeRoute=true}}}
Locale={Lookup=function(v) return v end};PlayerOperations={EXECUTE_SCRIPT=1}
cities={};routes={};units={[1]={GetType=function() return 1 end},[10]={GetType=function() return 2 end},[11]={GetType=function() return 2 end}}
engineAdds=0;engineRemoves=0;engineProps=0;scanFail=false
for id=1,3 do
 local c={id=id,kind=id==1 and 'RESEARCH' or 'COMMERCE',active=4,values={SCIENCE=id==1 and 40 or 6},b={}}
 c.GetID=function() return c.id end;c.GetOwner=function() return 0 end;c.GetName=function() return 'C'..c.id end
 c.GetYield=function(_,y) return c.values[y] or 0 end
 c.GetBuildings=function() return {HasBuilding=function(_,k) return c.b[k]==true end,RemoveBuilding=function(_,k) c.b[k]=nil;engineRemoves=engineRemoves+1 end} end
 c.GetBuildQueue=function() return {CreateBuilding=function(_,k) c.b[k]=true;engineAdds=engineAdds+1 end} end
 c.SetProperty=function() engineProps=engineProps+1 end
 c.GetTrade=function() return {GetOutgoingRoutes=function() if scanFail then error('temporary read unavailable') end;local r={};for _,v in ipairs(routes) do if v.OriginCityID==c.id then r[#r+1]=v end end;return r end} end
 cities[id]=c
end
Players={[0]={GetID=function() return 0 end,GetCities=function() return {FindID=function(_,id) return cities[id] end,Members=function() return pairs(cities) end,GetCapitalCity=function() return cities[1] end} end,
 GetUnits=function() return {FindID=function(_,id) return units[id] end,Members=function() return pairs(units) end} end,
 GetTrade=function() return {CountOutgoingRoutes=function() return #routes end,GetNumOutgoingRoutes=function() return #routes end} end}}
Game.GetPlayers=function() return {Players[0]} end
UnitOperationTypes={MAKE_TRADE_ROUTE=1}
ContextPtr={SetInitHandler=function(_,f) init=f end,SetShutdown=function(_,f) shutdown=f end,SetUpdate=function(_,f) update=f end,ClearUpdate=function() update=nil end}
""")
l.execute((M/'Probe.lua').read_text())
l.execute("""
P=SPCP0;P.Info=function(t,k) if t=='Units' then return GameInfo.Units[k] end;if t=='Buildings' then return {Index=k} end;if t=='Yields' then return {Index=k:gsub('YIELD_','')} end end
ExposedMembers.SPC_Performance=SPCPerformance.New()
shared={Version=P.VERSION,RouteSignalRevision=0,EffectiveFacts={Read=function(pid,c) return {specialization=c.kind,active=c.active,potential=4} end}};ExposedMembers.SPC_P0=shared
""")
for f in ['NetworkBridge.lua','CommerceConvergence.lua','TradeRouteProbe.lua']:l.execute((M/f).read_text())
l.execute("""
SPCNetworkBridge.Start(P,shared);n=shared.NetworkBridge;n.ready=true
SPCCommerceConvergence.Start(P,shared);commerce=shared.CommerceConvergence
SPCTradeRouteProbe.Start(P,shared)
packets=0;emptyPackets=0;loopSender=nil
UI={RequestPlayerOperation=function(pid,op,p)
 if p.Action=='NETWORK_REVALIDATE_FAILURE' then n.CheckEvidence(true);return end
 packets=packets+1;if p.Valid~=1 then emptyPackets=emptyPackets+1 end
 n.Receive(pid,p)
end}
function route(id,origin,dest) return {OriginCityPlayer=0,OriginCityID=origin,DestinationCityPlayer=0,DestinationCityID=dest,TraderUnitID=id} end
routes={route(10,1,2)}
Events=UE
""")
# Probe inclusion resets P; retain fixture-only database reader after each include.
original_include=l.globals().include
def include(name):
    original_include(name)
    if name=='Probe':l.execute("SPCP0.Info=P.Info")
l.globals().include=include
l.execute((M/'UI/BackgroundRoutes.lua').read_text())
l.execute("""
init();UE.SystemUpdateUI.Fire();assert(n.players[0].revision==1 and commerce.last['0:2'].amount.SCIENCE==8)
local pub=ExposedMembers.SPC_P0_BackgroundRoutes;local perf=ExposedMembers.SPC_Performance
local rev=n.players[0].revision;local adds,removes,props=engineAdds,engineRemoves,engineProps;local sent=packets;local scans=perf.entries.route_scan.total;local derives=perf.entries.derive.total
-- Cases 1/4: ten genuine non-traders; real Game + UI events + generic flushes.
for i=1,10 do
 GE.UnitOperationStarted.Fire(0,1);UE.UnitOperationStarted.Fire(0,1)
 GE.UnitOperationDeactivated.Fire(0,1);UE.UnitOperationDeactivated.Fire(0,1)
 UE.GameCoreEventPublishComplete.Fire();UE.GameCoreEventPlaybackComplete.Fire();UE.SystemUpdateUI.Fire()
 assert(n.players[0].routes and n.players[0].revision==rev)
end
assert(engineAdds==adds and engineRemoves==removes and engineProps==props)
assert(packets==sent and emptyPackets==0 and perf.entries.route_scan.total==scans and perf.entries.derive.total==derives)
-- Unknown unit must revalidate but never publish empty; identical content suppressed.
for i=1,10 do GE.UnitOperationStarted.Fire(0,999);UE.UnitOperationStarted.Fire(0,999);UE.GameCoreEventPublishComplete.Fire() end
assert(packets==sent and emptyPackets==0 and n.players[0].revision==rev)
assert(engineAdds==adds and engineRemoves==removes and engineProps==props and perf.entries.derive.total==derives)
-- Case 2: genuine addition, one content publication.
routes={route(10,1,2),route(11,1,3)}
UE.TradeRouteAddedToMap.Fire();UE.GameCoreEventPublishComplete.Fire()
assert(n.players[0].revision==rev+1 and packets==sent+1 and #n.players[0].routes==2)
assert(commerce.last['0:3'].amount.SCIENCE==8)
-- Case 3: complete removal snapshot (only removed recipient loses its effect).
local existing=engineAdds;routes={route(10,1,2)}
GE.TradeRouteRemovedFromMap.Fire();UE.TradeRouteRemovedFromMap.Fire();UE.GameCoreEventPublishComplete.Fire()
assert(n.players[0].revision==rev+2 and packets==sent+2 and #n.players[0].routes==1)
assert(commerce.last['0:2'].amount.SCIENCE==8 and commerce.last['0:3'].amount.SCIENCE==0 and engineAdds==existing)
-- Read failure retains last verified route; bounded attempts stop, no empty packets.
scanFail=true;local before=perf.entries.route_scan.total
UE.UnitOperationStarted.Fire(0,999)
for i=1,50 do UE.SystemUpdateUI.Fire();UE.GameCoreEventPublishComplete.Fire() end
assert(perf.entries.route_scan.total-before==3 and n.players[0].routes and emptyPackets==0)
-- Confirmed endpoint destruction cannot leave an invalid route in consumers.
cities[2]=nil;GE.CityRemovedFromMap.Fire()
assert(n.players[0].routes==nil and perf.entries.confirmed_invalid.total>0)
-- Complete zero recovers; no recursive retry storm.
scanFail=false;routes={};UE.TradeRouteRemovedFromMap.Fire();UE.SystemUpdateUI.Fire()
assert(n.players[0].routes and #n.players[0].routes==0)
-- Current turn number alone does not invalidate verified topology.
turn=2;assert(n.Verified(0));local r=n.players[0].revision
UE.PlayerTurnActivated.Fire(0);UE.SystemUpdateUI.Fire();assert(n.players[0].revision==r)
-- Fixed memory: same key set over 10000 simulated turns; no automatic IO/prints.
local function nodes(x) if type(x)~='table' then return 0 end;local v=1;for _,y in pairs(x) do v=v+nodes(y) end;return v end
local size=nodes(perf);local logs=prints
for t=3,10003 do turn=t;P.Count('unit_cb');P.Count('building_check',10) end
assert(nodes(perf)==size and prints==logs)
assert(perf.entries.unit_cb.previous==1 and perf.entries.unit_cb.current==1)
local text=SPCPerformance.Describe(true);assert(text:find('auto_log=DISABLED') and #text<6000)
local total=perf.entries.unit_cb.total;perf.enabled=false;P.Count('unit_cb');assert(perf.entries.unit_cb.total==total);perf.enabled=true
shutdown()
""")
l.execute("""
-- A reentrant send before ACK cannot recursively emit another packet.
turn=10004;local send=SPCNetworkSender.New(P);local b=n.players[0]
local snap={status='COMPLETE_UI_SHADOW',snapshot={count=1,turn=turn,signal=shared.RouteSignalRevision,keys={'x'},fingerprint='0:10|0:1>0:3',routes={x={originPlayer=0,originCityID=1,destinationPlayer=0,destinationCityID=3,traderUnitID=10}}}}
local requests=0
UI.RequestPlayerOperation=function(pid,op,a) requests=requests+1;send(snap);n.Receive(pid,a) end
routes={route(10,1,3)};send(snap);send(snap);assert(requests==1 and b.fingerprint==snap.snapshot.fingerprint)
-- Rejected packet gets no infinite automatic resend in this turn.
turn=10005;snap.snapshot.turn=turn;snap.snapshot.fingerprint='changed';snap.snapshot.routes.x.destinationCityID=999
send(snap);local rejected=requests
for i=1,100 do send(snap) end
assert(requests==rejected and b.routes and b.fingerprint=='0:10|0:1>0:3')
-- Old complete network survives malformed input / Valid=0 without native invalidity.
local revision=b.revision;n.Receive(0,{Epoch=n.epoch,Seq=100000,Turn=turn,Signal=shared.RouteSignalRevision,Valid=0})
assert(b.routes and b.revision==revision)
-- Native count reduction + failed complete reads revokes; success restores empty snapshot.
routes={};n.CheckEvidence(true);assert(not b.routes)
""")
for p in M.rglob('*.lua'):l.eval('function(s) assert(load(s)) end')(p.read_text())
x=ET.parse(M/'SpecializationP0.modinfo');assert x.getroot().get('version')=='96'
for f in x.findall('.//File'):assert (M/f.text).is_file()
assert 'PerformanceCounters.lua' in [f.text for f in x.findall('.//ImportFiles/File')]
assert 'PerformanceCounters.lua' in [f.text for f in x.findall('./Files/File')]
print('B069 LOCAL_SIMULATION_PASS: actual collector/sender/receiver + Commerce writes; 10 known/unknown operations; unchanged zero writes/publications/derive; addition/removal; bounded failure; endpoint invalidation; turn; fixed counters 10000 turns; all Lua compile/XML references.')
