"""D0009 actual Gameplay network bridge; no Civ VI process or yield application."""
from pathlib import Path
from lupa.lua55 import LuaRuntime
import xml.etree.ElementTree as ET
w=Path(__file__).resolve().parent.parent
r=w/"Sid Meier's Civilization VI/Mods/SpecializationP0"
l=LuaRuntime(unpack_returned_tuples=True)
l.execute((r/'NetworkBridge.lua').read_text())
l.execute('''
print=function() end
local onLoad;local count=0
Events={LoadScreenClose={Add=function(f) onLoad=f end}}
Game={GetCurrentGameTurn=function() return 1 end};ExposedMembers={}
local cities={}
for i=1,5 do cities[i]={GetID=function() return i end,GetName=function() return 'TestCity'..i end,GetOwner=function() return 0 end} end
local cc={FindID=function(_,i) return cities[i] end,GetCapitalCity=function() return cities[1] end,Members=function() return ipairs(cities) end}
Players={[0]={GetCities=function() return cc end,GetTrade=function() return {CountOutgoingRoutes=function() return count end} end}}
local roles={[1]='RESEARCH',[2]='COMMERCE',[3]='COMMERCE',[4]='CULTURE'}
local shared={RouteSignalRevision=0,CityFlowProbe={SupportFacts=function(_,c) return {specialization=roles[c:GetID()],potential=1} end}}
local P={IsTestPlayer=function(id) return id==0 end,Field=function(t,k) return t and t[k] end}
SPCNetworkBridge.Start(P,shared);onLoad()
local b=shared.NetworkBridge;local seq=0
local function send(data,n)
 count=n;seq=seq+1;b.Receive(0,{Epoch=b.epoch,Seq=seq,Turn=1,Signal=0,Valid=1,Count=n,Data=data})
 assert(b.players[0].reason=='READY_BACKGROUND_UI',b.players[0].reason)
end
local function check(city,kind,n,yes)
 local set=b.players[0].recipients[kind] or {};local count=0;for _ in pairs(set) do count=count+1 end;assert(count==n);assert((set[city]~=nil)==yes)
end
-- No route: natural research capital receives itself.
send('',0);check(1,'RESEARCH',1,true);check(2,'RESEARCH',1,false)
-- Source capital and culture connect to Commerce: direct center receives both.
send('0,1,0,2,10;0,4,0,2,11',2)
check(2,'RESEARCH',2,true);check(2,'CULTURE',1,true)
-- Add distribution to another center: no direct-source propagation.
send('0,1,0,2,10;0,4,0,2,11;0,2,0,3,12;0,3,0,5,13',4)
check(3,'RESEARCH',3,true);check(3,'CULTURE',2,true)
check(5,'RESEARCH',3,false);check(5,'CULTURE',2,false)
assert(not next(b.players[0].centers[3]))
-- Same destination, different traders: recipient dedup.
send('0,1,0,2,10;0,4,0,2,11;0,2,0,3,12;0,2,0,3,14',4)
check(3,'RESEARCH',3,true);check(3,'CULTURE',2,true)
-- Direct and distribution overlap. Remove direct; distribution remains, relay stops.
send('0,1,0,2,10;0,4,0,2,11;0,2,0,3,12;0,4,0,3,15;0,3,0,5,13',5)
check(3,'CULTURE',3,true);check(5,'CULTURE',3,true)
send('0,1,0,2,10;0,4,0,2,11;0,2,0,3,12;0,3,0,5,13',4)
check(3,'CULTURE',2,true);check(5,'CULTURE',2,false)
-- Remove last culture source, only natural capital research survives empty rebuild.
send('',0);check(2,'CULTURE',0,false);check(1,'RESEARCH',1,true)
-- New load epoch discards poisoned cache; full current source reconstructs.
b.players[0].recipients.RESEARCH[5]={};local oldEpoch=b.epoch
SPCNetworkBridge.Start(P,shared);b=shared.NetworkBridge;onLoad();assert(b.epoch~=oldEpoch)
send('0,1,0,2,10;0,4,0,2,11',2);check(5,'RESEARCH',2,false)
local accepted=b.players[0].seq
b.Receive(0,{Epoch=b.epoch,Seq=accepted,Valid=0});check(2,'CULTURE',1,true)
-- Report separates direct sources from reception; pages cycle and reset on summary.
local overview=b.Read(0,cities[2]);assert(overview:find('TestCity2 (#2)',1,true));assert(overview:find('文化: 本中心接入来源=1 | 全国接收城市=1 | 本城接收=是',1,true))
local detail1=b.Read(0,cities[2],true);local detail2=b.Read(0,cities[2],true)
assert(detail1:find('明细 1/2',1,true));assert(detail2:find('明细 2/2',1,true));assert((detail1..detail2):find('→',1,true))
assert(b.Read(0,cities[2],true)==detail1);b.Read(0,cities[2]);assert(b.Read(0,cities[2],true)==detail1)
-- Distribution removal preserves direct center and removes only recipient.
send('0,4,0,2,11;0,2,0,5,12',2);check(5,'CULTURE',2,true)
send('0,4,0,2,11',1);check(5,'CULTURE',1,false);check(2,'CULTURE',1,true)
-- Count mismatch refuses stale display even if an invalidation signal was missed.
count=0;assert(b.Read(0,cities[2]):find('CURRENT_COUNT_CHANGED'));count=1
-- Existing endpoint ownership change cannot display obsolete membership.
cities[4].GetOwner=function() return 9 end;assert(b.Read(0,cities[2]):find('ENDPOINT_MISSING_OR_CHANGED'))
cities[4].GetOwner=function() return 0 end
-- Malformed/partial complete packet withdraws; no historical fallback.
seq=seq+1;b.Receive(0,{Epoch=b.epoch,Seq=seq,Turn=1,Signal=0,Valid=1,Count=2,Data='0,1,0,2,10'})
assert(b.Read(0,cities[2]):find('网络待刷新'))
''')
for p in r.rglob('*.lua'):l.execute('assert(load(...))',p.read_text())
m=ET.parse(r/'SpecializationP0.modinfo').getroot()
assert m.attrib['version']=='38' and m.attrib['id']=='df9efdad-dd48-40a7-b868-87f0617bc16d'
for e in m.findall('.//File'):assert (r/e.text).is_file()
xml=ET.parse(r/'UI/P0Panel.xml');ids=[e.attrib['ID'] for e in xml.iter() if 'ID' in e.attrib];assert len(ids)==len(set(ids))
# Execute actual request dispatcher with new action, ownership/test-player gates retained.
l.execute('''
include=function() end
SPCP0={VERSION='P0-B-031',IsTestPlayer=function(id) return id==0 end,Scalar=tostring}
local c={GetID=function() return 2 end,GetOwner=function() return 0 end}
Players={[0]={GetCities=function() return {FindID=function(_,id) if id==2 then return c end end} end}}
GameEvents={SPC_P0_Request={Add=function(f) dispatch=f end}}
ExposedMembers={}
''')
l.execute((r/'Gameplay.lua').read_text().split('shared.TradeEvents={}')[0])
l.execute('''
ExposedMembers.SPC_P0.NetworkBridge={Read=function(pid,c,detail) return detail and 'DETAIL_CALLED' or 'SUMMARY_CALLED' end}
dispatch(0,{Action='NETWORK_DETAIL',Token='detail',CityID=2});assert(ExposedMembers.SPC_P0.Snapshot=='DETAIL_CALLED')
dispatch(0,{Action='NETWORK_READ',Token='summary',CityID=2});assert(ExposedMembers.SPC_P0.Snapshot=='SUMMARY_CALLED')
''')
print('LOCAL_SIMULATION_PASS: D0009 direct/capital reception, dedup, receive-only nonrelay, overlapping qualification withdrawal, empty/load rebuild, replay and malformed rejection; Lua/XML/manifest checked. Not game verification.')
