"""B105/B106 actual passive observer and UI/Gameplay ingress; no native ordering claim."""
from pathlib import Path
from lupa.lua55 import LuaRuntime
import xml.etree.ElementTree as ET
R=Path(__file__).resolve().parents[1];M=R/'Mod';l=LuaRuntime()
l.execute((M/'CitySequenceProbe.lua').read_text())
l.execute(r"""
local function event()local e={list={}};function e.Add(fn)e.list[#e.list+1]=fn end
 function e.Fire(...)for _,fn in ipairs(e.list)do fn(...)end end;return e end
function setup(missing)
 Events={};GameEvents={};EventSubTypes={FOUND_CITY=-77};shared={};reads=0;writes=0;lookups=0;native=nil;unknown=false
 for _,n in ipairs({'LoadScreenClose','CityAddedToMap','CityInitialized','CityRemovedFromMap','CityTransfered','UnitActivate','GameCoreEventPublishComplete','GameCoreEventPlaybackComplete'})do
  if n~=missing then Events[n]=event()end
 end
 GameEvents.CityBuilt=event();GameEvents.CityConquered=event()
 Game={GetCurrentGameTurn=function()return 13 end,SetProperty=function()writes=writes+1;error('observer wrote')end}
 P={IsTestPlayer=function(pid)return pid==0 end,Field=function(t,k)return t and t[k]end,
  Info=function(t,k)return k==1 and {UnitType='UNIT_SETTLER'}or {UnitType='UNIT_WARRIOR'}end}
 function city(o,id,x)return {GetOwner=function()return o end,GetID=function()return id end,GetX=function()return x or 4 end,GetY=function()return 5 end}end
 function unit(kind)return {GetOwner=function()return 0 end,GetID=function()return 7 end,GetType=function()return kind or 1 end,GetX=function()return 4 end,GetY=function()return 5 end}end
 CityManager={GetCityAt=function()reads=reads+1;if unknown then error('no getter')end;return native end,
 GetCity=function(o,id)lookups=lookups+1;if native and native:GetOwner()==o and native:GetID()==id then return native end end}
 SPCCitySequenceProbe.Start(P,shared);d=shared.CitySequenceProbe
end
function load()Events.LoadScreenClose.Fire()end
function report()local t={};for i=1,5 do t[#t+1]=d.Describe(0,i)end;return table.concat(t,'\n')end
setup()
assert(d.Begin(0,nil,unit(),'early'):find('未开始'))
for i=1,100 do Events.GameCoreEventPublishComplete.Fire();GameEvents.CityBuilt.Fire(0,1,4,5);Events.UnitActivate.Fire(0,7,4,5,-77,true)end
assert(reads==0 and writes==0 and lookups==0)
load();local msg=d.Begin(0,nil,unit(),'found');assert(msg:find('Start EMPTY',1,true),msg)
local idle=reads
for i=1,100 do Events.GameCoreEventPublishComplete.Fire();Events.GameCoreEventPlaybackComplete.Fire()end
assert(reads==idle)
native=city(0,9);GameEvents.CityBuilt.Fire(0,9,4,5,{secret='payload'})
Events.CityAddedToMap.Fire(0,9,4,5);Events.CityInitialized.Fire(0,9,4,5)
Events.GameCoreEventPublishComplete.Fire();Events.GameCoreEventPlaybackComplete.Fire()
msg=report();assert(msg:find('Built 0 / 9',1,true) and msg:find('Publish CITY / 0 / 9',1,true),msg)
assert(not msg:find('payload'));idle=reads;local old=msg
for i=1,100 do Events.GameCoreEventPublishComplete.Fire();Events.GameCoreEventPlaybackComplete.Fire();d.Describe(0,1)end
assert(reads==idle and report()==old and writes==0)
-- B106 founding signal: before/after city notifications, no unit/city lookup,
-- no visibility gate, signed enum, actual ordering retained, wrong plot ignored.
assert(msg:find('FOUND_CITY=-77',1,true) and msg:find('起始移民=7',1,true))
local beforeReads=reads;local beforeLookups=lookups
Events.UnitActivate.Fire(0,7,4,5,-77,false)
msg=report();assert(msg:find('FoundCity 0 / 7 / -77 / false',1,true),msg)
assert(reads==beforeReads and lookups==beforeLookups and writes==0)
old=report();Events.UnitActivate.Fire(0,7,8,5,-77,true);assert(report()==old)
Events.UnitActivate.Fire(0,7,4,5,123,true)
assert(report():find('UnitActivate 0 / 7 / 123 / true',1,true))
Events.UnitActivate.Fire(0,7,4,5,nil)
assert(report():find('UnitActivate 0 / 7 / UNAVAILABLE / UNKNOWN',1,true))
old=report()
-- Duplicate request token must not reset the trace; invalid arm preserves it.
d.Begin(0,nil,unit(),'found');assert(report()==old)
d.Begin(0,nil,unit(2),'bad');assert(report()==old)
d.Begin(3,native,nil,'foreign');assert(report()==old)
GameEvents.CityBuilt.Fire(0,77,8,5);Events.CityRemovedFromMap.Fire(3,500);assert(report()==old)
-- Capture current reference before transfer; snapshot at an intermediate flush
-- must remain an observation and must not classify new-city/destruction.
native=city(3,40);d.Begin(0,nil,unit(),'transfer')
GameEvents.CityBuilt.Fire(0,88,4,5)
Events.GameCoreEventPublishComplete.Fire()
GameEvents.CityConquered.Fire(0,3,88,4,5);Events.CityRemovedFromMap.Fire(3,40)
native=nil;Events.GameCoreEventPublishComplete.Fire()
native=city(0,88);Events.CityAddedToMap.Fire(0,88,4,5);Events.CityInitialized.Fire(0,88,4,5)
Events.CityTransfered.Fire(0,88,3,-100);Events.GameCoreEventPublishComplete.Fire()
msg=report();assert(msg:find('Publish EMPTY',1,true) and msg:find('Transfer 0 / 88 / 3 / -100',1,true),msg)
assert(msg:find('新城接管未开启',1,true) and writes==0)
-- Manual read markers distinguish a publish caused by the read operation itself.
GameEvents.CityBuilt.Fire(0,88,4,5);d.Read(0,1);Events.GameCoreEventPublishComplete.Fire()
msg=report();assert(msg:find('ReadRequest',1,true) and writes==0)
-- Removal without successor and later same-location build both remain visible;
-- observer cannot retire/migrate history. Unknown getter never becomes EMPTY.
d.Begin(0,native,nil,'raze');Events.CityRemovedFromMap.Fire(0,88);native=nil
unknown=true;Events.GameCoreEventPublishComplete.Fire();unknown=false
msg=report();assert(msg:find('Publish UNKNOWN',1,true),msg)
Events.GameCoreEventPlaybackComplete.Fire();assert(report():find('Playback EMPTY',1,true))
native=city(0,99);GameEvents.CityBuilt.Fire(0,99,4,5);Events.CityAddedToMap.Fire(0,99,4,5)
assert(report():find('Built 0 / 99',1,true));assert(writes==0)
-- Strict finite trace: preserve earlier evidence, mark overflow and stop reads.
d.Begin(0,native,nil,'bound')
for i=1,60 do GameEvents.CityBuilt.Fire(0,99,4,5);Events.GameCoreEventPublishComplete.Fire()end
assert(report():find('TRACE_LIMIT',1,true));old=report();idle=reads
for i=1,100 do GameEvents.CityBuilt.Fire(0,99,4,5);Events.GameCoreEventPublishComplete.Fire()end
assert(report()==old and reads==idle)
setup('GameCoreEventPublishComplete');load();d.Begin(0,nil,unit(),'missing')
assert(d.Describe(0,1):find('Publish=false',1,true))
assert(not d.Describe(8,1):find('位置',1,true))
setup();assert(d.Describe(0,1):find('尚未开始')) -- reload clears only diagnostic state
load();d.Begin(0,nil,unit(),'error');Game.GetCurrentGameTurn=function()error('failure')end
GameEvents.CityBuilt.Fire(0,9,4,5);assert(d.Describe(0,1):find('OBSERVER_READ_ERROR',1,true))

setup();load();native=city(0,40);d.Begin(0,native,nil,'transfer-negative')
GameEvents.CityBuilt.Fire(4,40,4,5);Events.CityRemovedFromMap.Fire(0,40)
native=city(4,40);Events.CityAddedToMap.Fire(4,40,4,5);Events.CityTransfered.Fire(4,40,0,-100)
assert(not report():find('FoundCity 4',1,true) and writes==0)
-- Unit events share the existing48-row budget; no new history or lookup.
for i=1,60 do Events.UnitActivate.Fire(4,7,4,5,-77,true)end
assert(report():find('TRACE_LIMIT',1,true));local count=reads;local frozen=report()
for i=1,100 do Events.UnitActivate.Fire(4,7,4,5,-77,true)end
assert(reads==count and report()==frozen)
setup('UnitActivate');load();d.Begin(0,nil,unit(),'nohook')
assert(report():find('UnitActivate=false',1,true))
setup();EventSubTypes=nil;shared={};SPCCitySequenceProbe.Start(P,shared);d=shared.CitySequenceProbe;load()
d.Begin(0,nil,unit(),'noenum');Events.UnitActivate.Fire(0,7,4,5,-77,true)
assert(report():find('FOUND_CITY=不可用',1,true) and not report():find('FoundCity 0',1,true))
assert(report():find('UnitActivate 0 / 7 / -77 / true',1,true))
setup();load();d.Begin(0,nil,unit(),'earlyfound')
Events.UnitActivate.Fire(0,7,4,5,-77,true)
native=city(0,9);GameEvents.CityBuilt.Fire(0,9,4,5);Events.CityInitialized.Fire(0,9,4,5)
msg=report();assert(msg:find('FoundCity 0',1,true)<msg:find('Built 0',1,true))
assert(writes==0)
""")
# Actual Gameplay branch: eligibility, unit existence, no consumer/action fallthrough.
g=(M/'Gameplay.lua').read_text();prefix=g[g.index('local function request('):g.index('  -- B068 presentation')]
l.execute('setup();load();Players={[0]={GetCities=function()return {FindID=function()return native end}end,GetUnits=function()return {FindID=function(_,id)if id==7 then return unit()end end}end}};P.Scalar=tostring;reached=0\n'+prefix+'reached=reached+1\nend\nDispatch=request')
l.execute(r"""
Dispatch(0,{Action='CITY_SEQUENCE_BEGIN',Token='ingress',UnitID=7});assert(shared.Snapshot:find('Start EMPTY',1,true))
Dispatch(0,{Action='CITY_SEQUENCE_READ',Token='read',Page=1});assert(shared.LastToken=='read' and reached==0)
Dispatch(0,{Action='CITY_SEQUENCE_BEGIN',Token='missing',UnitID=8});assert(shared.Snapshot:find('失败'))
Dispatch(0,{Action='GOVERNOR',Token='other'});assert(reached==1 and writes==0)
""")
# Execute actual UI packet construction. Read works after razing with no selected city.
u=LuaRuntime();s=(M/'UI/P0Panel.lua').read_text()
u.execute(r"""
ContextPtr={ClearUpdate=function()end};Game={GetLocalPlayer=function()return 0 end,GetCurrentGameTurn=function()return 13 end}
P={IsTestPlayer=function()return true end,VERSION='test',Scalar=tostring};ExposedMembers={};PlayerOperations={EXECUTE_SCRIPT=1}
function trace()end;function status()end;function waitForResponse()end
UI={GetHeadSelectedCity=function()return selectedCity end,GetHeadSelectedUnit=function()return selectedUnit end,
 RequestPlayerOperation=function(pid,op,p)packet=p;sends=(sends or 0)+1 end}
""")
u.execute(s[s.index('request=function(action,advance)'):s.index('local function legacyCopy')])
u.execute(r"""
selectedUnit={GetOwner=function()return 0 end,GetID=function()return 7 end}
request('CITY_SEQUENCE_BEGIN');assert(packet.UnitID==7 and not packet.CityID)
selectedUnit=nil;selectedCity={GetOwner=function()return 0 end,GetID=function()return 88 end}
request('CITY_SEQUENCE_BEGIN');assert(packet.CityID==88 and not packet.UnitID)
selectedCity=nil;request('CITY_SEQUENCE_READ',true);assert(packet.Page==1 and not packet.CityID)
request('CITY_SEQUENCE_READ',true);assert(packet.Page==2)
local before=sends;request('CITY_SEQUENCE_BEGIN');assert(sends==before)
""")
# This checkpoint intentionally cannot persist or classify identity.
probe=(M/'CitySequenceProbe.lua').read_text()
for forbidden in ['SetProperty','RequestPlayerOperation','RemoveBuilding','CreateBuilding','SetUpdate','print(']:
 assert forbidden not in probe, forbidden
root=ET.parse(M/'SpecializationP0.modinfo').getroot()
assert root.attrib['version']=='133'
assert len(root.findall(".//File[.='CitySequenceProbe.lua']"))==2
compile_lua=LuaRuntime().eval('function(s,n) local f,e=load(s,n);assert(f,e)end')
for p in M.rglob('*.lua'): compile_lua(p.read_text(),str(p))
print('B105/B106 LOCAL_SIMULATION_PASS: FOUND_CITY raw/missing/signed/visibility/ordering/negative-control,  bounded passive trace, split-batch visibility, idle/read zero work, failure/missing hooks, actual UI/Gameplay dispatch, Lua/manifest; native boundary UNVERIFIED')
