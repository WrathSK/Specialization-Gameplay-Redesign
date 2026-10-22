-- B005: Gameplay-only automatic diagnostics. NEVER a GAMEPLAY_CURRENT provider.
-- Unit operation parameters are hypotheses, not certified active-route records.
SPCTradeRouteProbe={}
function SPCTradeRouteProbe.Start(P,shared)
  shared.AutoRouteProbe={}
  shared.RouteSignalRevision=0
  local busy=false
  local seq=0
  local pending={}
  local previous={}
  local function scalar(v) return P.Scalar(v) end
  local function need(obj,method,...)
    local ok,v=P.Call(obj,method,...)
    if not ok then error(method..":"..scalar(v)) end
    return v
  end
  local function optional(obj,method,...)
    local ok,v=P.Call(obj,method,...)
    if not ok then return "UNKNOWN("..scalar(v)..")" end
    return scalar(v)
  end
  local function shortError(err)
    local first=tostring(err):match("^[^\r\n]+") or "UNKNOWN_ERROR"
    return scalar(first:match(":%d+: (.+)$") or first)
  end
  local function scan(player)
    local pid=need(player,"GetID")
    local pt=need(player,"GetTrade")
    local count=need(pt,"CountOutgoingRoutes")
    if type(count)~="number" or count<0 or count%1~=0 then error("COUNT_INVALID") end
    local units=need(player,"GetUnits")
    local member=P.Field(units,"Members");if type(member)~="function" then error("UNIT_MEMBERS_ABSENT") end
    local iter,state,key=member(units);if type(iter)~="function" then error("UNIT_ITERATOR_INVALID") end
    local rows={};local scanned=0;local matched=0;local unknown=0
    local make=P.Field(UnitOperationTypes,"MAKE_TRADE_ROUTE")
    for _,unit in iter,state,key do
      scanned=scanned+1;if scanned>2048 then error("UNIT_SCAN_LIMIT") end
      local ut=need(unit,"GetType");local info=GameInfo.Units[ut]
      if not info then error("UNIT_DEFINITION_MISSING") end
      if info.MakeTradeRoute==true or info.MakeTradeRoute==1 then
        if #rows>=256 then error("TRADER_SCAN_LIMIT") end
        local id=need(unit,"GetID")
        local opok,op=P.Call(unit,"GetOperationType")
        local match=opok and type(op)=="number" and type(make)=="number" and op==make
        local line="trader="..scalar(id).." operation="..(opok and scalar(op) or "UNKNOWN("..scalar(op)..")")
          .." MAKE_TRADE_ROUTE="..scalar(make)
        if not opok or type(op)~="number" or type(make)~="number" then unknown=unknown+1 end
        local compact="商人 "..scalar(id).." | task="..(opok and scalar(op) or "UNKNOWN")
        if match then
          matched=matched+1
          for _,field in ipairs({"PARAM_X0","PARAM_Y0","PARAM_X1","PARAM_Y1"}) do
            local constant=P.Field(UnitOperationTypes,field)
            local value=type(constant)=="number" and optional(unit,"GetOperationParameter",constant) or "UNKNOWN_CONSTANT"
            line=line.." "..field.."="..value
            compact=compact.." "..field:gsub("PARAM_","").."="..value
          end
        end
        rows[#rows+1]={id=id,text=line,display=compact,match=match}
      end
    end
    table.sort(rows,function(a,b) if a.match~=b.match then return a.match end;return a.id<b.id end)
    return {engineCount=count,traders=#rows,matched=matched,unknown=unknown,rows=rows}
  end
  local function refresh(reason)
    if busy then pending.REENTRANT=true;return end
    busy=true;seq=seq+1;shared.AutoRouteProbeError=nil
    print("[SPC]["..P.VERSION.."][TRADE_STATE_PROBE] BEGIN seq="..seq.." reason="..reason)
    local ok,err=pcall(function()
      if type(Game.GetPlayers)~="function" then error("Game.GetPlayers:ABSENT") end
      local players=Game.GetPlayers();if type(players)~="table" then error("PLAYERS_NOT_TABLE") end
      local dirtyList={};for k in pairs(pending) do dirtyList[#dirtyList+1]=k end;table.sort(dirtyList);pending={}
      for i=1,257 do
        local player=players[i];if player==nil then break end
        if i>256 then error("PLAYER_SCAN_LIMIT") end
        local pid=need(player,"GetID")
        if P.IsTestPlayer(pid) then
          local good,r=pcall(scan,player)
          local prefix="[SPC]["..P.VERSION.."][TRADE_STATE_PROBE]"
          local header="seq="..seq.." turn="..scalar(Game.GetCurrentGameTurn()).." player="..pid.." reason="..reason
            .." dirty="..table.concat(dirtyList,",").." authoritative=BLOCKED"
          local lines={header}
          local display={"采样："..reason.." / turn="..scalar(Game.GetCurrentGameTurn()).." / seq="..seq}
          if good then
            lines[#lines+1]="CANDIDATE_ONLY engineCount="..r.engineCount.." traders="..r.traders.." matchingOperations="..r.matched.." unknownOperations="..r.unknown
            display[#display+1]="引擎路线计数："..r.engineCount.."；商人数量："..r.traders
            display[#display+1]="匹配建商路任务："..r.matched.."；未知任务类型："..r.unknown
            for _,row in ipairs(r.rows) do lines[#lines+1]=row.text end
            display[#display+1]="端点仍属候选：nil表示缺失，不是有效坐标。"
            for j=1,math.min(#r.rows,6) do display[#display+1]=r.rows[j].display end
            if #r.rows>6 then display[#display+1]="其余任务未显示；共"..#r.rows.."名商人，不据截断显示认定全集。" end
            display[#display+1]="候选读取成功 ≠ 当前路线集合验证通过。"
          else
            lines[#lines+1]="UNAVAILABLE "..scalar(r)
            display[#display+1]="候选接口不可用："..shortError(r)
          end
          display[#display+1]="正式路线来源：BLOCKED；未启用网络或收益。"
          local ids={}
          if good then for _,row in ipairs(r.rows) do if row.match then ids[row.id]=true end end end
          shared.AutoRouteProbe[pid]={text=table.concat(display,"\n"),sequence=seq,reason=reason,success=good,
            turn=Game.GetCurrentGameTurn(),signalRevision=shared.RouteSignalRevision,
            engineCount=good and r.engineCount or nil,matchingTraderIDs=ids,unknownOperations=good and r.unknown or nil}
          -- Always log scan boundary, detailed rows only on change or load/initialization.
          local details=table.concat(lines,"\n",2)
          print(prefix.." "..header)
          if previous[pid]~=details or reason=="INITIALIZE" or reason=="LoadScreenClose" then
            for j=2,#lines do print(prefix.." "..lines[j]) end;previous[pid]=details
          end
        end
      end
    end)
    busy=false
    if not ok then
      shared.AutoRouteProbeError=reason..": "..shortError(err)
      shared.AutoRouteProbe={} -- prevent a global refresh failure from displaying an old success as current
      print("[SPC]["..P.VERSION.."][TRADE_STATE_PROBE] GLOBAL_UNAVAILABLE "..scalar(err))
    end
  end
  local function listen(namespace,name,fn)
    local event=P.Field(namespace,name)
    if event and type(P.Field(event,"Add"))=="function" then event.Add(fn)
    else print("[SPC]["..P.VERSION.."][TRADE_STATE_PROBE] EVENT_ABSENT "..name) end
  end
  -- Event payloads are never route facts. No assumption about start/end semantics.
  for _,name in ipairs({"TradeRouteActivityChanged","TradeRouteRemovedFromMap","UnitRemovedFromMap",
      "UnitOperationDeactivated","UnitOperationStarted","UnitOperationsCleared","CityRemovedFromMap","CityAddedToMap","CityTransfered","DiplomacyDeclareWar"}) do
    local eventName=name;listen(Events,eventName,function(pid,id)
      if eventName:find('^Unit') then
        P.Count('unit_cb');if not P.RouteUnitRelevant(pid,id) then P.Count('unit_ignored');return end
      end
      pending[eventName]=true;shared.RouteSignalRevision=shared.RouteSignalRevision+1
    end)
  end
  for _,name in ipairs({"CityConquered","TradeRoutePlundered"}) do
    local eventName=name;listen(GameEvents,eventName,function() pending[eventName]=true;shared.RouteSignalRevision=shared.RouteSignalRevision+1 end)
  end
  listen(Events,"LoadScreenClose",function() refresh("LoadScreenClose") end)
  listen(Events,"PlayerTurnActivated",function(pid)
    if P.IsTestPlayer(pid) then refresh("PlayerTurnActivated") end
  end)
  listen(Events,"PlayerTurnDeactivated",function(pid)
    if P.IsTestPlayer(pid) then refresh("PlayerTurnDeactivated") end
  end)
  refresh("INITIALIZE")
end
