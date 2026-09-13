"""Automatic Gameplay probe with no UI or game process. No authoritative promotion."""
from pathlib import Path
from lupa import LuaRuntime
root=Path(__file__).resolve().parents[1]/"Sid Meier's Civilization VI/Mods/SpecializationP0"
lua=LuaRuntime(unpack_returned_tuples=True)
lua.execute((root/'Probe.lua').read_text())
lua.execute((root/'TradeRouteProbe.lua').read_text())
lua.execute(r'''
local function event()
 local callbacks={};return {Add=function(f) callbacks[#callbacks+1]=f end,
 Fire=function(...) for _,f in ipairs(callbacks) do f(...) end end}
end
Events={};for _,n in ipairs({"LoadScreenClose","PlayerTurnActivated","PlayerTurnDeactivated","TradeRouteActivityChanged","TradeRouteRemovedFromMap","UnitRemovedFromMap","UnitOperationDeactivated","CityRemovedFromMap","CityAddedToMap","DiplomacyDeclareWar"}) do Events[n]=event() end
GameEvents={CityConquered=event(),TradeRoutePlundered=event()}
local p=SPCP0;p.IsTestPlayer=function(id) return id==0 end
local count=2;local scans=0;local paramReads=0
GameInfo={Units={[0]={MakeTradeRoute=true},[1]={MakeTradeRoute=false}}}
UnitOperationTypes={MAKE_TRADE_ROUTE=77,PARAM_X0=1,PARAM_Y0=2,PARAM_X1=3,PARAM_Y1=4}
local function trader(id,op)
 return {GetID=function() return id end,GetType=function() return 0 end,GetUnitType=function() error("UI_TYPE_GETTER_FORBIDDEN") end,
 GetOperationType=function() return op end,
 GetOperationParameter=function(self,index) paramReads=paramReads+1;assert(index>=1 and index<=4);return index+id end}
end
local a=trader(10,77);local b=trader(11,77);local idle=trader(12,-1)
local unitRows={a,b,idle,{GetType=function() return 1 end,GetUnitType=function() error("UI_TYPE_GETTER_FORBIDDEN") end}}
local player={GetID=function() return 0 end,
 GetTrade=function() return {CountOutgoingRoutes=function() return count end} end,
 GetUnits=function() scans=scans+1;return {Members=function() return ipairs(unitRows) end} end}
local other={GetID=function() return 1 end,GetTrade=function() error("NONTEST_FORBIDDEN") end}
local turn=1;Game={GetPlayers=function() return {player,other} end,GetCurrentGameTurn=function() return turn end}
local logs={};print=function(v) logs[#logs+1]=v end
local shared={};p.VERSION="P0-B-005"
SPCTradeRouteProbe.Start(p,shared)
assert(scans==1 and paramReads==8 and shared.AutoRouteProbe[0].reason=="INITIALIZE")
assert(table.concat(logs,"\n"):find("engineCount=2") and table.concat(logs,"\n"):find("authoritative=BLOCKED"))
Events.LoadScreenClose.Fire();assert(scans==2 and shared.AutoRouteProbe[0].reason=="LoadScreenClose")
for i=1,10 do Events.TradeRouteActivityChanged.Fire(0,0,1,0,2) end
assert(scans==2) -- coalesced; payload does not create route records
unitRows={b,idle};count=1;Events.UnitRemovedFromMap.Fire(0,10)
turn=2;Events.PlayerTurnActivated.Fire(0);assert(scans==3)
assert(shared.AutoRouteProbe[0].text:find("引擎路线计数：1"))
Events.PlayerTurnActivated.Fire(1);assert(scans==3)
a.GetOperationType=nil;unitRows={a};count=1;Events.PlayerTurnDeactivated.Fire(0)
assert(table.concat(logs,"\n"):find("unknownOperations=1"))
local oldType=a.GetType;a.GetType=nil;Events.LoadScreenClose.Fire()
assert(not shared.AutoRouteProbe[0].success and shared.AutoRouteProbe[0].text:find("GetType:ABSENT"))
assert(not shared.AutoRouteProbe[0].text:find("stack traceback"))
a.GetType=oldType
player.GetTrade=nil;Events.LoadScreenClose.Fire();assert(not shared.AutoRouteProbe[0].success)
assert(shared.AutoRouteProbe[0].text:find("GetTrade:ABSENT"))
-- Safe fresh initialization with no previous diagnostic cache / no route facts.
local fresh={};SPCTradeRouteProbe.Start(p,fresh);assert(fresh.AutoRouteProbe[0] and not fresh.AutoRouteProbe[0].success)
assert(shared.routes==nil and shared.network==nil)
Game.GetPlayers=nil;Events.LoadScreenClose.Fire()
assert(shared.AutoRouteProbe[0]==nil and shared.AutoRouteProbeError:find("Game.GetPlayers:ABSENT"))
''')
print('LOCAL_SIMULATION_PASS: automatic initialization/load/turn scans, coalesced dirty signals, changed trader list, idle filtering, absent getters, non-test exclusion, no UI dependency or authoritative state.')
