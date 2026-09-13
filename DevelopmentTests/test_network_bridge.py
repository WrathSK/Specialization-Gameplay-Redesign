from pathlib import Path
from lupa.lua55 import LuaRuntime
import xml.etree.ElementTree as ET
R=Path(__file__).resolve().parent.parent/"Sid Meier's Civilization VI/Mods/SpecializationP0"
l=LuaRuntime(unpack_returned_tuples=True)
for name in ['NetworkBridge.lua','NetworkSender.lua']:l.execute((R/name).read_text())
l.execute('''
print=function() end
local turn=1;local count=0;local load
Events={LoadScreenClose={Add=function(fn) load=fn end}}
Game={GetCurrentGameTurn=function() return turn end,GetLocalPlayer=function() return 0 end}
ExposedMembers={}
local cities={};for i=1,5 do cities[i]={GetID=function() return i end,GetOwner=function() return 0 end} end
local collection={FindID=function(_,id) return cities[id] end,Members=function() return ipairs(cities) end,GetCapitalCity=function() return cities[1] end}
Players={[0]={GetCities=function() return collection end,GetTrade=function() return {GetNumOutgoingRoutes=function() return count end} end}}
local roles={[1]="RESEARCH",[2]="COMMERCE",[4]="CULTURE"}
local P={VERSION="P0-B-025",IsTestPlayer=function(pid) return pid==0 end,Field=function(t,k) return t and t[k] end}
local shared={Version=P.VERSION,RouteSignalRevision=0,CityFlowProbe={SupportFacts=function(pid,c)
 assert(roles[c:GetID()],"UNTRACKED");return {specialization=roles[c:GetID()],potential=1}
end}}
ExposedMembers.SPC_P0=shared;SPCNetworkBridge.Start(P,shared);load()
local bridge=shared.NetworkBridge
local function send(seq,body,n)
 count=n;bridge.Receive(0,{Epoch=bridge.epoch,Seq=seq,Turn=turn,Signal=shared.RouteSignalRevision,Valid=1,Count=n,Data=body})
end
send(1,"0,1,0,2,100;0,4,0,2,101;0,2,0,3,102",3)
local out=bridge.Read(0,cities[3]);assert(out:find("RESEARCH N=2 selectedReceives=YES") and out:find("CULTURE N=1 selectedReceives=YES"))
assert(bridge.Read(0,cities[2]):find("CULTURE@4"))
-- Remove source route: no lingering Culture; Research still connected.
send(2,"0,1,0,2,100;0,2,0,3,102",2)
assert(bridge.Read(0,cities[3]):find("CULTURE N=0 selectedReceives=NO"))
-- Stale replay cannot restore a removed connection.
send(1,"0,1,0,2,100;0,4,0,2,101;0,2,0,3,102",3)
assert(bridge.Read(0,cities[3]):find("CULTURE N=0"))
-- Same route count, changed destination: replace not accumulate.
send(3,"0,1,0,2,100;0,2,0,5,102",2)
assert(bridge.Read(0,cities[3]):find("RESEARCH N=2 selectedReceives=NO"))
assert(bridge.Read(0,cities[5]):find("selectedReceives=YES"))
-- Incomplete and malformed batches withdraw usable state.
send(4,"0,1,0,2,100",2);assert(bridge.Read(0,cities[3]):find("UNKNOWN"))
send(5,"0,1,0,2,100;0,2,0,3,100",2);assert(bridge.Read(0,cities[3]):find("UNKNOWN"))
send(6,"",0);assert(bridge.Read(0,cities[3]):find("routes=0"))
-- Signal changes invalidate synchronously, before another packet is sent.
send(7,"0,1,0,2,100",1);shared.RouteSignalRevision=1
assert(bridge.Read(0,cities[3]):find("REFRESH_PENDING"))
-- Actual UI sender feeds actual Gameplay receiver; never requires a panel open.
local requests=0
PlayerOperations={EXECUTE_SCRIPT=1}
UI={RequestPlayerOperation=function(pid,operation,params) requests=requests+1;bridge.Receive(pid,params) end}
local pump=SPCNetworkSender.New(P)
-- New Gameplay context resets receive sequence; old epoch packet rejected.
SPCNetworkBridge.Start(P,shared);bridge=shared.NetworkBridge;load()
count=1
local public={generation=1,status="COMPLETE_UI_SHADOW",snapshot={count=1,turn=1,signal=1,keys={"a"},routes={a={originPlayer=0,originCityID=1,destinationPlayer=0,destinationCityID=3,traderUnitID=100}}}}
pump(public);assert(requests==1 and bridge.Read(0,cities[3]):find("selectedReceives=YES"))
pump(public);assert(requests==1)
public.status="UNKNOWN";public.snapshot=nil;pump(public)
assert(requests==2 and bridge.Read(0,cities[3]):find("BACKGROUND_INVALIDATED"))
''')
for p in R.rglob('*.lua'):l.execute('assert(load(...))',p.read_text())
m=ET.parse(R/'SpecializationP0.modinfo').getroot();assert m.attrib['version']=='32'
for e in m.findall('.//File'):assert (R/e.text).is_file()
ET.parse(R/'UI/P0Panel.xml')
print('LOCAL_SIMULATION_PASS: real sender/receiver mocks, complete replace, all-network distribution, unique recipients, source withdrawal, equal-count reroute, replay/partial/duplicate/signal invalidation, no effects; native UI operation transport remains USER_GAME_TEST_REQUIRED.')
