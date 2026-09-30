-- B009 UI SHADOW ONLY. No gameplay requests, modifiers, properties or BTS dependencies.
include("Probe")
include("ShadowRouteState")
local normalized=SPCShadowRouteState.New()
local P=SPCP0
include("NetworkSender")
local sendNetwork,stopSender=SPCNetworkSender.New(P)
local networkStopped=false
local active=false
local public
local lastGood,firstComplete,lastChange
local generation=0
local dirty=true
local pendingReason="INITIALIZE"
local sinceDirty,clock,scanAge=0,0,0
local lastGame,lastSignal
local hooks={}
local systemPulses,contextPulses=0,0
local dispatching=false
local publishPulses,playbackPulses=0,0
local attempts,retryPending=0,false
local lastFlush="INITIALIZE"
local function integer(n) return type(n)=="number" and n>=0 and n<math.huge and n%1==0 end
local function need(o,m,...)
  local ok,v=P.Call(o,m,...);if not ok then error(m..":"..P.Scalar(v)) end;return v
end
local function short(err)
  local first=tostring(err):match("^[^\r\n]+") or "UNKNOWN"
  return P.Scalar(first:match(":%d+: (.+)$") or first)
end
local function ordered(map) local a={};for k in pairs(map) do a[#a+1]=k end;table.sort(a);return a end
local function endpoint(playerID,cityID)
  local player=Players[playerID];if not player then error("ENDPOINT_PLAYER_MISSING") end
  local cities=need(player,"GetCities");local c=need(cities,"FindID",cityID)
  if not c then error("ENDPOINT_CITY_MISSING") end
  if need(c,"GetOwner")~=playerID or need(c,"GetID")~=cityID then error("ENDPOINT_CHANGED") end
  local ok,name=P.Call(c,"GetName")
  if ok and type(name)=="string" then
    if Locale and Locale.Lookup then local lok,n=pcall(Locale.Lookup,name);if lok and type(n)=="string" then name=n end end
  else name="city "..playerID..":"..cityID end
  return P.Scalar(name)
end
local function collect(pid)
  local bridgeSignal=ExposedMembers.SPC_P0 and ExposedMembers.SPC_P0.RouteSignalRevision or 0
  local player=Players[pid];local pt=need(player,"GetTrade")
  local before=need(pt,"GetNumOutgoingRoutes");assert(integer(before),"COUNT_UNKNOWN")
  local cities=need(player,"GetCities");local members=P.Field(cities,"Members")
  assert(type(members)=="function","CITY_MEMBERS_ABSENT")
  local iter,state,key=members(cities);assert(type(iter)=="function","CITY_ITERATOR_INVALID")
  local routes,traders={},{};local scanned,raw=0,0
  for _,city in iter,state,key do
    P.Count('city_scan');scanned=scanned+1;assert(scanned<=512,"CITY_SCAN_LIMIT")
    local owner,id=need(city,"GetOwner"),need(city,"GetID")
    assert(owner==pid and integer(id),"CITY_SCOPE_CHANGED")
    local list=need(need(city,"GetTrade"),"GetOutgoingRoutes")
    assert(type(list)=="table","ROUTES_NOT_TABLE")
    for i=1,4097 do
      local row=list[i];if row==nil then break end
      raw=raw+1;assert(raw<=4096,"ROUTE_SCAN_LIMIT")
      -- Copy only known scalars; never traverse/stringify an engine route object.
      local op,oc=P.Field(row,"OriginCityPlayer"),P.Field(row,"OriginCityID")
      local dp,dc=P.Field(row,"DestinationCityPlayer"),P.Field(row,"DestinationCityID")
      local tid=P.Field(row,"TraderUnitID")
      assert(integer(op) and integer(oc) and integer(dp) and integer(dc) and integer(tid),"ROUTE_FIELDS_UNKNOWN")
      assert(op==pid and oc==id,"ORIGIN_SCOPE_CHANGED")
      local k=op..":"..tid.."|"..op..":"..oc..">"..dp..":"..dc
      assert(not traders[tid] or traders[tid]==k,"TRADER_ROUTE_CONFLICT")
      traders[tid]=k
      if not routes[k] then
        routes[k]={key=k,traderUnitID=tid,originPlayer=op,originCityID=oc,destinationPlayer=dp,destinationCityID=dc,
          domestic=op==dp,identityKind="SNAPSHOT_KEY_NOT_PERMANENT_UID",
          display=endpoint(op,oc).." → "..endpoint(dp,dc).." ["..tid.."]"}
      end
    end
  end
  assert(bridgeSignal==(ExposedMembers.SPC_P0 and ExposedMembers.SPC_P0.RouteSignalRevision or 0),"BRIDGE_SIGNAL_CHANGED")
  local keys=ordered(routes);local after=need(pt,"GetNumOutgoingRoutes")
  assert(integer(after) and before==after and #keys==after,"COUNT_OR_SNAPSHOT_CHANGED")
  return {signal=bridgeSignal,routes=routes,keys=keys,count=#keys,traders=traders,fingerprint=table.concat(keys,"\n"),player=pid,
    status="COMPLETE_UI_SHADOW",sourceContext="UI",authority="UI_SHADOW_ONLY",turn=Game.GetCurrentGameTurn()}
end
local function comparison(s)
  local game=ExposedMembers.SPC_P0
  local g=game and game.AutoRouteProbe and game.AutoRouteProbe[s.player]
  if not game or game.Version~=P.VERSION or not g or not g.success or g.turn~=s.turn
    or g.signalRevision~=game.RouteSignalRevision then return "PENDING（Gameplay对照未就绪/已变旧）" end
  if g.unknownOperations~=0 then return "UNKNOWN（Gameplay任务类型缺失）" end
  local n=0
  for id in pairs(g.matchingTraderIDs or {}) do n=n+1;if not s.traders[id] then return "MISMATCH（商人集合不同）" end end
  if n~=s.count or g.engineCount~=s.count then return "MISMATCH（数量不同）" end
  return "MATCH（仅数量与商人ID，不证明端点权威性）"
end

local function render()
 local snapshot=public.snapshot
 public.text='B069 route state='..public.status..' | '..(public.revalidation or 'IDLE')
  ..'\nverified routes='..tostring(snapshot and snapshot.count or 'NONE')..' scans='..generation
  ..' reason='..pendingReason..' attempts='..attempts..'/3'
  ..'\n'..normalized:Summary()..(public.error and ('\n'..public.error) or '')
end
-- B137 one-way UI session closure. No Gameplay function is invoked here.
local function stopNetwork(epoch)
 if networkStopped then return public.networkStopEpoch==epoch end
 networkStopped=true;stopSender(public)
 dirty=false;retryPending=false;attempts=0;lastGood=nil;public.snapshot=nil;normalized:Reset()
 public.networkStopped=true;public.networkStopEpoch=epoch;public.status='ISOLATED_SESSION'
 public.revalidation='STOPPED';public.error=nil;render();return true
end
local function networkBlocked()
 if networkStopped then return true end
 local shared=ExposedMembers.SPC_P0;local isolation=shared and shared.NetworkIsolation
 if isolation and isolation.active==true and isolation.player==Game.GetLocalPlayer() then
  stopNetwork(isolation.epoch);return true
 end
 return false
end
local function requestStop(epoch)
 local shared=ExposedMembers.SPC_P0;local bridge=shared and shared.NetworkBridge
 if type(epoch)~='number' or not active or not shared or shared.Version~=P.VERSION or not bridge or epoch~=bridge.epoch then return false end
 return stopNetwork(epoch)
end
local function mark(reason)
 if not active or networkBlocked() then return end
 P.Count('revalidate')
 if not dirty then attempts=0 end
 dirty=true;pendingReason=reason;public.revalidation='NEEDS_REVALIDATION'
 -- The verified snapshot and formal consumer state remain intact.
end
local function refresh()
 if networkBlocked() then return end
 P.Count('route_scan');generation=generation+1
 local pid=Game.GetLocalPlayer()
 if not P.IsTestPlayer(pid) then dirty=false;return end
 local ok,s=pcall(collect,pid)
 if networkBlocked() then return end
 if ok then
  local accepted,err=normalized:Replace(s);if not accepted then ok=false;s=err end
 end
 if ok then
  if lastGood and lastGood.player==s.player and lastGood.fingerprint==s.fingerprint then P.Count('same_snapshot') end
  lastGood=s;public.snapshot=s;public.status='COMPLETE_UI_SHADOW';public.error=nil
  public.revalidation='VERIFIED';dirty=false;retryPending=false
  sendNetwork(public) -- sender also compares content + epoch + receiver ACK
 else
  P.Count('route_failure');public.error=short(s);public.revalidation='NEEDS_REVALIDATION'
  -- No invalid packet solely because a read failed. Gameplay independently checks
  -- count decrease / missing endpoints before permitting use of the old routes.
  retryPending=attempts<3;dirty=false
  if not retryPending then
   local g=ExposedMembers.SPC_P0;local b=g and g.NetworkBridge
   if b then pcall(UI.RequestPlayerOperation,pid,PlayerOperations.EXECUTE_SCRIPT,
    {OnStart='SPC_P0_Request',Action='NETWORK_REVALIDATE_FAILURE',Token=P.VERSION..':proof:'..generation,Epoch=b.epoch}) end
  end
 end
 public.generation=generation;render()
end
local function observeGame()
 local game=ExposedMembers.SPC_P0
 if game~=lastGame then
  lastGame=game;lastSignal=game and game.RouteSignalRevision
  lastGood=nil;public.snapshot=nil;public.status='UNKNOWN';normalized:Reset()
  mark('GAMEPLAY_CONTEXT_READY_OR_RESET')
 elseif game and game.RouteSignalRevision~=lastSignal then
  lastSignal=game.RouteSignalRevision;mark('GAMEPLAY_DIRTY_SIGNAL')
 end
end
local function flush()
 if not active or networkBlocked() then return end
 if dispatching then P.Count('busy_skip');return end
 observeGame()
 if not dirty and not retryPending then
  -- ACK checking is bounded, and sender returns before encoding unchanged data.
  if public.snapshot and public.awaitingNetwork then sendNetwork(public) end
  return
 end
 dispatching=true;attempts=attempts+1
 local ok=pcall(refresh)
 dispatching=false
 if networkStopped then return end
 if not ok then P.Count('route_failure');dirty=false;retryPending=false;public.revalidation='RETRY_STOPPED' end
end
local function bind(name,fn)
 local e=P.Field(Events,name)
 if e and e.Add then e.Add(fn);hooks[#hooks+1]={event=e,callback=fn} end
end
local function initialize()
 if active then return end;active=true
 public={version=P.VERSION,status='UNKNOWN',sourceContext='UI',authority='UI_SHADOW_ONLY'}
 public.ReadNormalizedRoutes=function() return normalized:Read() end
 public.StopNetwork=requestStop
 ExposedMembers.SPC_P0_BackgroundRoutes=public
 lastGame=ExposedMembers.SPC_P0;lastSignal=lastGame and lastGame.RouteSignalRevision
 for _,name in ipairs({'LoadScreenClose','TradeRouteActivityChanged','TradeRouteAddedToMap','TradeRouteRemovedFromMap',
  'UnitOperationStarted','UnitOperationsCleared','UnitOperationDeactivated','UnitRemovedFromMap',
  'CityAddedToMap','CityRemovedFromMap','CityTransfered','DiplomacyDeclareWar','PlayerTurnActivated','PlayerTurnDeactivated'}) do
  local eventName=name
  bind(name,function(pid,id)
   if networkBlocked() then return end
   if eventName:find('^Unit') then
    P.Count('unit_cb');if not P.RouteUnitRelevant(pid,id) then P.Count('unit_ignored');return end
   end
   if eventName:find('^PlayerTurn') and pid~=Game.GetLocalPlayer() then return end
   mark(eventName)
   if eventName=='LoadScreenClose' or eventName:find('^PlayerTurn') then flush() end
  end)
 end
 for _,name in ipairs({'GameCoreEventPublishComplete','GameCoreEventPlaybackComplete','SystemUpdateUI'}) do bind(name,flush) end
 flush()
 -- No recurring full-scan timer. Events and local turn boundaries remain primary.
end
ContextPtr:SetInitHandler(initialize)
ContextPtr:SetShutdown(function()
 active=false;if public then stopSender(public) end;normalized:Reset();ContextPtr:ClearUpdate()
 for _,h in ipairs(hooks) do if h.event.Remove then h.event.Remove(h.callback) end end
 if ExposedMembers.SPC_P0_BackgroundRoutes==public then ExposedMembers.SPC_P0_BackgroundRoutes=nil end
end)
