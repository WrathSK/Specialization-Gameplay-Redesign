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
for i=1,5 do cities[i]={GetID=function() return i end,GetOwner=function() return 0 end} end
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
 local text=b.Read(0,cities[city]);assert(text:find(kind..' N='..n..' selectedReceives='..(yes and 'YES' or 'NO'),1,true),text)
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
-- Malformed/partial complete packet withdraws; no historical fallback.
seq=seq+1;b.Receive(0,{Epoch=b.epoch,Seq=seq,Turn=1,Signal=0,Valid=1,Count=2,Data='0,1,0,2,10'})
assert(b.Read(0,cities[2]):find('UNKNOWN'))
''')
for p in r.rglob('*.lua'):l.execute('assert(load(...))',p.read_text())
m=ET.parse(r/'SpecializationP0.modinfo').getroot()
assert m.attrib['version']=='34' and m.attrib['id']=='df9efdad-dd48-40a7-b868-87f0617bc16d'
for e in m.findall('.//File'):assert (r/e.text).is_file()
ET.parse(r/'UI/P0Panel.xml')
print('LOCAL_SIMULATION_PASS: D0009 direct/capital reception, dedup, receive-only nonrelay, overlapping qualification withdrawal, empty/load rebuild, replay and malformed rejection; Lua/XML/manifest checked. Not game verification.')
