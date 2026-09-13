-- B009 UI SHADOW ONLY. No gameplay requests, modifiers, properties or BTS dependencies.
include("Probe")
include("ShadowRouteState")
local normalized=SPCShadowRouteState.New()
local P=SPCP0
include("NetworkSender")
local sendNetwork=SPCNetworkSender.New(P)
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
    scanned=scanned+1;assert(scanned<=512,"CITY_SCAN_LIMIT")
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
  if public.status~="COMPLETE_UI_SHADOW" then normalized:Invalidate(public.error or pendingReason) end
  local lines={"来源：独立后台 UI / SHADOW ONLY；未接入收益"}
  if public.status=="COMPLETE_UI_SHADOW" then
    local s=public.snapshot
    lines[#lines+1]="状态：COMPLETE_UI_SHADOW | turn="..s.turn.." | seq="..generation
    lines[#lines+1]="触发："..public.reason.."；本玩家当前商路："..s.count
    lines[#lines+1]="Gameplay对照："..comparison(s)
    if firstComplete then lines[#lines+1]="首次自动完成："..firstComplete.reason.." / "..firstComplete.count.."条" end
    if lastChange then lines[#lines+1]="最近变化：+"..lastChange.added.." / -"..lastChange.removed end
    if lastChange and lastChange.firstRemoved then lines[#lines+1]="已移除："..lastChange.firstRemoved end
    for i=1,math.min(#s.keys,6) do lines[#lines+1]=i..". "..s.routes[s.keys[i]].display end
    if #s.keys>6 then lines[#lines+1]="仅显示前6条；缓存完整数量="..s.count end
  else
    lines[#lines+1]="状态："..public.status.."；原因："..(public.error or pendingReason)
    lines[#lines+1]="没有可用的当前快照；不把未知当零条，也不使用旧结果。"
  end
  lines[#lines+1]="刷新次数="..generation.."；系统通知="..systemPulses.."；Context更新="..contextPulses
  lines[#lines+1]="发布完成="..publishPulses.."；播放完成="..playbackPulses.."；本批尝试="..attempts.."/3"
  lines[#lines+1]="采样入口："..lastFlush
  lines[#lines+1]="标准缓存："..normalized:Summary()
  lines[#lines+1]="此按钮只看缓存，不触发采样。"
  public.text=table.concat(lines,"\n")
  sendNetwork(public)
end
local function mark(reason)
  if not active then return end
  if not dirty then sinceDirty=0 end
  dirty=true;pendingReason=reason
  attempts=0;retryPending=false
  public.status="UNKNOWN";public.snapshot=nil;public.error=nil
  render()
end
local function refresh()
  generation=generation+1;scanAge=0
  local pid=Game.GetLocalPlayer()
  if not P.IsTestPlayer(pid) then
    lastGood=nil;firstComplete=nil;lastChange=nil;normalized:Reset()
    public.status="OUTSIDE_TEST_CIV";public.snapshot=nil;public.error=nil;dirty=false;render();return
  end
  local ok,s=pcall(function()
    local snapshot=collect(pid)
    local accepted,err=normalized:Replace(snapshot)
    if not accepted then error(err) end
    return snapshot
  end)
  if ok then
    local added,removed=0,0;local firstRemoved
    if lastGood and lastGood.player~=pid then lastGood=nil;firstComplete=nil;lastChange=nil end
    for _,k in ipairs(s.keys) do if not lastGood or not lastGood.routes[k] then added=added+1 end end
    if lastGood then for _,k in ipairs(lastGood.keys) do if not s.routes[k] then removed=removed+1;firstRemoved=firstRemoved or lastGood.routes[k].display end end end
    if added>0 or removed>0 or not lastGood then lastChange={added=added,removed=removed,firstRemoved=firstRemoved} end
    firstComplete=firstComplete or {reason=pendingReason,count=s.count}
    lastGood=s;public.snapshot=s;public.status=s.status;public.reason=pendingReason;public.error=nil
  else public.status="UNKNOWN";public.snapshot=nil;public.error=short(s) end
  public.generation=generation;dirty=false
  render()
  print("[SPC]["..P.VERSION.."][BACKGROUND_ROUTES] seq="..generation.." reason="..pendingReason.." "..public.status.." "..(public.error or ("count="..public.snapshot.count)))
end
local function observeGame()
  local game=ExposedMembers.SPC_P0
  if game~=lastGame then
    if lastGame~=nil then lastGood=nil;firstComplete=nil;lastChange=nil;normalized:Reset() end
    lastGame=game;lastSignal=game and game.RouteSignalRevision
    mark("GAMEPLAY_CONTEXT_READY_OR_RESET")
  elseif game and game.RouteSignalRevision~=lastSignal then
    lastSignal=game.RouteSignalRevision;mark("GAMEPLAY_DIRTY_SIGNAL")
  end
end
local function dispatch(source)
  if not active or dispatching then return end
  dispatching=true
  attempts=attempts+1;lastFlush=source or pendingReason
  local ok,err=pcall(refresh)
  dispatching=false
  if not ok then public.status="UNKNOWN";public.snapshot=nil;public.error=short(err);dirty=false end
  retryPending=public.status=="UNKNOWN" and attempts<3
  render()
end
local function listen(name)
  local event=P.Field(Events,name)
  if event and type(P.Field(event,"Add"))=="function" then
    local callback=function()
      mark(name)
      -- These lifecycle boundaries must not depend on an empty context receiving SetUpdate.
      if name=="LoadScreenClose" or name=="PlayerTurnActivated" or name=="PlayerTurnDeactivated" then dispatch() end
    end
    event.Add(callback);hooks[#hooks+1]={event=event,callback=callback}
  end
end
local function initialize()
  if active then return end
  active=true
  public={version=P.VERSION,status="UNKNOWN",sourceContext="UI",authority="UI_SHADOW_ONLY"}
  public.ReadNormalizedRoutes=function() return normalized:Read() end
  ExposedMembers.SPC_P0_BackgroundRoutes=public
  lastGame=ExposedMembers.SPC_P0;lastSignal=lastGame and lastGame.RouteSignalRevision
  for _,name in ipairs({"LoadScreenClose","TradeRouteActivityChanged","TradeRouteAddedToMap","TradeRouteRemovedFromMap",
    "UnitOperationStarted","UnitOperationsCleared","UnitOperationDeactivated","UnitRemovedFromMap",
    "CityAddedToMap","CityRemovedFromMap","DiplomacyDeclareWar","PlayerTurnActivated","PlayerTurnDeactivated"}) do listen(name) end
  -- Native UI uses publish-complete to flush a batch of GameCore changes.
  -- No visibility check, UI opening, or event payload as route truth.
  for _,name in ipairs({"GameCoreEventPublishComplete","GameCoreEventPlaybackComplete"}) do
    local event=P.Field(Events,name)
    if event and type(P.Field(event,"Add"))=="function" then
      local callback=function()
        if not active then return end
        if name=="GameCoreEventPublishComplete" then publishPulses=publishPulses+1 else playbackPulses=playbackPulses+1 end
        local ok,err=pcall(function()
          observeGame()
          if dirty or retryPending then dispatch(name) else render() end
        end)
        if not ok then public.status="UNKNOWN";public.snapshot=nil;public.error=short(err);dirty=false;retryPending=false;render() end
      end
      event.Add(callback);hooks[#hooks+1]={event=event,callback=callback}
    end
  end
  local systemEvent=P.Field(Events,"SystemUpdateUI")
  if systemEvent and type(P.Field(systemEvent,"Add"))=="function" then
    local callback=function()
      if not active then return end
      systemPulses=systemPulses+1
      local ok,err=pcall(function()
        observeGame()
        if dirty then dispatch() else render() end
      end)
      if not ok then public.status="UNKNOWN";public.snapshot=nil;public.error=short(err);dirty=false;render() end
    end
    systemEvent.Add(callback);hooks[#hooks+1]={event=systemEvent,callback=callback}
  end
  dispatch() -- no panel/UI open action involved
  ContextPtr:SetUpdate(function(dt)
    contextPulses=contextPulses+1
    if not active or type(dt)~="number" or dt<0 then return end
    clock=clock+dt;scanAge=scanAge+dt;sinceDirty=sinceDirty+dt
    if clock<0.25 then return end;clock=0
    local ok,err=pcall(function()
      observeGame()
      if scanAge>=10 and not dirty then mark("TIMER_FALLBACK") end
      if dirty and sinceDirty>=0.20 then dispatch() else render() end
    end)
    if not ok then public.status="UNKNOWN";public.snapshot=nil;public.error=short(err);dirty=false;render() end
  end)
end
ContextPtr:SetInitHandler(initialize)
ContextPtr:SetShutdown(function()
  active=false;normalized:Reset();ContextPtr:ClearUpdate()
  for _,h in ipairs(hooks) do if type(P.Field(h.event,"Remove"))=="function" then h.event.Remove(h.callback) end end
  if ExposedMembers.SPC_P0_BackgroundRoutes==public then ExposedMembers.SPC_P0_BackgroundRoutes=nil end
end)
