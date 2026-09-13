"""B009 shadow UI context tests, without opening/creating any game UI or launching Civ6."""
from pathlib import Path
import xml.etree.ElementTree as ET
from lupa import LuaRuntime
root=Path(__file__).resolve().parents[1]/"Sid Meier's Civilization VI/Mods/SpecializationP0"
lua=LuaRuntime(unpack_returned_tuples=True)
lua.execute((root/'Probe.lua').read_text())
lua.execute((root/'ShadowRouteState.lua').read_text())
lua.execute(r'''
include=function() end
local function event()
 local t={callbacks={}};t.Add=function(f) t.callbacks[#t.callbacks+1]=f end
 t.Remove=function(f) for i=#t.callbacks,1,-1 do if t.callbacks[i]==f then table.remove(t.callbacks,i) end end end
 t.Fire=function(...) for _,f in ipairs(t.callbacks) do f(...) end end;return t
end
Events=setmetatable({},{__index=function(t,k) local e=event();rawset(t,k,e);return e end})
ContextPtr={SetInitHandler=function(self,f) self.init=f end,SetUpdate=function(self,f) self.update=f end,
 SetShutdown=function(self,f) self.shutdown=f end,ClearUpdate=function(self) self.update=nil end}
UI=setmetatable({},{__index=function() error("UI_CONTROL_OR_REQUEST_FORBIDDEN") end})
Controls=setmetatable({},{__index=function() error("WINDOW_FORBIDDEN") end})
Locale={Lookup=function(n) return n end}
PlayerConfigurations={[0]={GetCivilizationTypeName=function() return "CIVILIZATION_SPC_TEST" end,GetLeaderTypeName=function() return "LEADER_SPC_TEST" end}}
localPlayer=0;turn=2;Game={GetLocalPlayer=function() return localPlayer end,GetCurrentGameTurn=function() return turn end}
reads=0;count=0;cities={};outgoing={};rows={}
function city(id,owner)
 local c={GetID=function() return id end,GetOwner=function() return owner end,GetName=function() return "City"..id end,
 GetTrade=function() return {GetOutgoingRoutes=function() reads=reads+1;return outgoing[id] or {} end} end}
 return c
end
cities[1]=city(1,0);cities[2]=city(2,0);cities[3]=city(3,0);cities[8]=city(8,1)
for i=1,3 do rows[i]=cities[i] end
local collection={Members=function() return ipairs(rows) end,FindID=function(self,id) return cities[id] end}
Players={[0]={GetCities=function() return collection end,GetTrade=function() return {GetNumOutgoingRoutes=function() return count end} end},
[1]={GetCities=function() return collection end}}
function route(t,o,d,dp)
 return setmetatable({TraderUnitID=t,OriginCityPlayer=0,OriginCityID=o,DestinationCityPlayer=dp or 0,DestinationCityID=d},
 {__pairs=function() error("NO_ENGINE_ROW_RECURSION") end,__tostring=function() error("NO_ENGINE_ROW_TOSTRING") end})
end
function gameSample(ids,n)
 local set={};for _,id in ipairs(ids) do set[id]=true end
 return {text="MOCK",success=true,engineCount=n,turn=turn,signalRevision=0,unknownOperations=0,matchingTraderIDs=set}
end
ExposedMembers={SPC_P0={Version=SPCP0.VERSION,RouteSignalRevision=0,AutoRouteProbe={[0]=gameSample({},0)}}}
logs={};print=function(s) logs[#logs+1]=s end
function tick(n) for i=1,n or 2 do ContextPtr.update(0.25) end end
function s() return ExposedMembers.SPC_P0_BackgroundRoutes end
''')
lua.execute((root/'UI/BackgroundRoutes.lua').read_text())
lua.execute(r'''
ContextPtr:init();assert(s().status=="COMPLETE_UI_SHADOW" and s().snapshot.count==0)
assert(s().text:find("MATCH") and s().authority=="UI_SHADOW_ONLY")
local started=reads;ContextPtr:init();assert(reads==started) -- idempotent init
outgoing[1]={route(10,1,2),route(11,1,3)};outgoing[2]={route(12,2,1)};count=3
ExposedMembers.SPC_P0.AutoRouteProbe[0]=gameSample({10,11,12},3)
Events.LoadScreenClose.Fire()
assert(s().snapshot.count==3 and s().text:find("MATCH")) -- no Context update needed
-- B008: no SystemUpdateUI or Context update required for mutation batches.
local generationBefore=s().generation
for i=1,10 do Events.CityRemovedFromMap.Fire() end
assert(s().status=="UNKNOWN" and not s().snapshot and s().generation==generationBefore)
-- Simulate endpoint disappearing before engine route cleanup has completed.
local savedCity=cities[3];cities[3]=nil
Events.GameCoreEventPublishComplete.Fire()
assert(s().status=="UNKNOWN" and s().error:find("ENDPOINT_CITY_MISSING"))
-- Engine settles before playback completion. Only routes touching city 3 disappear.
outgoing[1]={route(10,1,2)};count=2
Events.GameCoreEventPlaybackComplete.Fire()
assert(s().snapshot.count==2 and s().text:find("/ %-1"))
assert(s().text:find("采样入口：GameCoreEventPlaybackComplete"))
local settledGeneration=s().generation
for i=1,10 do Events.GameCoreEventPublishComplete.Fire();Events.GameCoreEventPlaybackComplete.Fire() end
assert(s().generation==settledGeneration) -- clean boundaries do not rescan
-- Persistent inconsistency stops retries after three attempts, never restores stale data.
count=3;Events.CityRemovedFromMap.Fire()
for i=1,10 do Events.GameCoreEventPublishComplete.Fire() end
assert(s().generation==settledGeneration+3 and s().status=="UNKNOWN" and not s().snapshot)
assert(s().text:find("本批尝试=3/3"))
-- A new signal permits recovery after retry exhaustion, with no timer/UI opening.
count=2;Events.TradeRouteRemovedFromMap.Fire();Events.GameCoreEventPublishComplete.Fire()
assert(s().snapshot.count==2)
-- Restore the original fixture for existing regression cases.
cities[3]=savedCity;outgoing[1]={route(10,1,2),route(11,1,3)};count=3
Events.TradeRouteActivityChanged.Fire();Events.GameCoreEventPublishComplete.Fire()
assert(s().snapshot.count==3)
local normalized=s().ReadNormalizedRoutes()
assert(normalized.status=="READY_UI_SHADOW" and normalized.count==3 and normalized.authority=="UI_SHADOW_ONLY")
local rev=normalized.revision
normalized.count=999;normalized.routes={}
assert(s().ReadNormalizedRoutes().count==3)
Events.CityRemovedFromMap.Fire()
assert(s().ReadNormalizedRoutes().status=="UNKNOWN")
Events.GameCoreEventPublishComplete.Fire()
assert(s().ReadNormalizedRoutes().revision==rev) -- same set does not increment revision
local initialGeneration=s().generation
for i=1,10 do Events.TradeRouteActivityChanged.Fire() end
assert(s().status=="UNKNOWN" and s().snapshot==nil)
Events.SystemUpdateUI.Fire() -- no dt and no Context update
assert(s().snapshot.count==3 and s().generation==initialGeneration+1)
assert(s().text:find("系统通知=1") and s().text:find("Context更新=0"))
local generation=s().generation
for i=1,20 do Events.TradeRouteActivityChanged.Fire() end
tick();assert(s().generation==generation+1 and s().snapshot.count==3) -- coalesce duplicate events
-- No event: timed fallback still replaces source; never appends to cached route history.
outgoing[1]={route(11,1,3)};count=2;tick(42)
assert(s().snapshot.count==2 and s().text:find("/ %-1"))
assert(s().text:find("MISMATCH")) -- stale-in-content gameplay sample cannot silently match
ExposedMembers.SPC_P0.RouteSignalRevision=1
tick();assert(s().snapshot.count==2 and s().text:find("PENDING"))
ExposedMembers.SPC_P0.AutoRouteProbe[0]=gameSample({11,12},2)
ExposedMembers.SPC_P0.AutoRouteProbe[0].signalRevision=1
tick();assert(s().text:find("MATCH"))
-- Identical count but different unit IDs must be rejected as a match.
ExposedMembers.SPC_P0.AutoRouteProbe[0].matchingTraderIDs={[10]=true,[12]=true}
tick();assert(s().text:find("MISMATCH"))
-- Partial read/count disagreement is UNKNOWN; previous snapshot is not current.
count=3;Events.TradeRouteRemovedFromMap.Fire();tick();assert(s().status=="UNKNOWN" and not s().snapshot)
count=2;local old=cities[3];cities[3]=nil;Events.CityRemovedFromMap.Fire();tick()
assert(s().status=="UNKNOWN" and s().error:find("ENDPOINT_CITY_MISSING"))
cities[3]=city(3,1);Events.CityAddedToMap.Fire();tick();assert(s().error:find("ENDPOINT_CHANGED"))
cities[3]=old
-- Changed endpoints with unchanged counts: replace route, preserve remaining route.
outgoing[1]={route(11,1,8,1)};Events.TradeRouteActivityChanged.Fire();tick()
assert(s().snapshot.count==2 and s().text:find("City1 → City8"))
local intl=false;for _,r in pairs(s().snapshot.routes) do if not r.domestic then intl=true end end;assert(intl)
-- Same pair different traders retained; exact duplicates deduplicated; conflicting trader invalid.
outgoing[1]={route(11,1,8,1),route(13,1,8,1)};count=3;Events.UnitOperationStarted.Fire();tick();assert(s().snapshot.count==3)
outgoing[1][3]=route(13,1,8,1);Events.UnitOperationStarted.Fire();tick();assert(s().snapshot.count==3)
outgoing[1][3]=route(13,1,3);Events.UnitOperationStarted.Fire();tick();assert(s().status=="UNKNOWN" and s().error:find("TRADER_ROUTE_CONFLICT"))
-- Getter unavailable: explicit failure; retries occur on another dirty event/fallback.
local oldTrade=cities[1].GetTrade;cities[1].GetTrade=nil;Events.LoadScreenClose.Fire();tick()
assert(s().status=="UNKNOWN" and s().error:find("GetTrade:ABSENT"))
cities[1].GetTrade=oldTrade;outgoing={};count=0;Events.LoadScreenClose.Fire();tick();assert(s().snapshot.count==0)
-- Late Gameplay context is optional for UI shadow read, but match stays pending.
ExposedMembers.SPC_P0=nil;Events.LoadScreenClose.Fire();tick();assert(s().snapshot.count==0 and s().text:find("PENDING"))
localPlayer=1;tick(42);assert(s().status=="OUTSIDE_TEST_CIV" and not s().snapshot)
localPlayer=0;Events.LoadScreenClose.Fire();tick();assert(s().snapshot.count==0)
local reader=s().ReadNormalizedRoutes
ContextPtr:shutdown();assert(reader().status=="UNKNOWN");assert(ExposedMembers.SPC_P0_BackgroundRoutes==nil and ContextPtr.update==nil)
for _,e in pairs(Events) do assert(#e.callbacks==0) end
''')
# Simulated fresh context load overwrites stale/corrupt exported snapshot with real source.
lua.execute('ExposedMembers.SPC_P0_BackgroundRoutes={status="COMPLETE_UI_SHADOW",snapshot={count=999}}')
lua.execute((root/'UI/BackgroundRoutes.lua').read_text())
lua.execute('ContextPtr:init();assert(s().snapshot.count==0 and s().generation==1);ContextPtr:shutdown()')
manifest=ET.parse(root/'SpecializationP0.modinfo')
assert manifest.find("./InGameActions/AddUserInterfaces[@id='SPCP0_BackgroundRoutes']/File").text=='UI/BackgroundRoutes.xml'
assert len(list(ET.parse(root/'UI/BackgroundRoutes.xml').getroot()))==0
print('LOCAL_SIMULATION_PASS: independent no-controls UI context; init/load/timer/dirty scans; exact scalar copy, counts & IDs comparison with stale guard; replace/remove/ownership/partial/conflicting duplicates/errors; no panel requests; shutdown/reload. UI_SHADOW_ONLY, no engine verification.')
