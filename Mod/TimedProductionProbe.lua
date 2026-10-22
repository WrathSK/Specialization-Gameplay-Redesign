-- B116 session-only evidence. No production, persistent state or rewards are written.
SPCTimedProductionProbe={}
function SPCTimedProductionProbe.Start(P,shared)
 local state=nil;local hooks={};local api={};shared.TimedProductionProbe=api
 local function empty(value) return value==nil or value=="" or value=="NONE" end
 local function failure(err)
  state.errorDetail=tostring(err)
  print("[SPC][TimedProduction] "..state.errorDetail)
  local short=state.errorDetail:match("^(.-)stack traceback:") or state.errorDetail
  short=short:match("^[^\r\n]+") or "未知错误"
  short=short:gsub("^.-:%d+: ?","")
  state.status="STOPPED";state.reason=short
 end
 local function publish()
  if not state then shared.TimedProduction=nil;return end
  local rows={};for i,v in ipairs(state.rows) do rows[i]=v end
  shared.TimedProduction={token=state.token,owner=state.owner,id=state.id,turn=state.turn,status=state.status,reason=state.reason,errorDetail=state.errorDetail,rows=rows,hooks=table.concat(hooks,", ")}
 end
 local function current()
  assert(P.IsTestPlayer(state.owner),"玩家资格失效")
  local c=Players[state.owner]:GetCities():FindID(state.id)
  assert(c and c:GetOwner()==state.owner and c:GetX()==state.x and c:GetY()==state.y,"观察城失效")
  local q=c:GetBuildQueue();local ok,value=P.Call(q,"CurrentlyBuilding")
  assert(ok,"Gameplay生产目标接口不可读")
  return value
 end
 local function add(name,value)
  if #state.rows>=24 then state.status="STOPPED";state.reason="事件超过24条，证据不完整";publish();return false end
  state.rows[#state.rows+1]=tostring(Game.GetCurrentGameTurn()).." "..name.." 目标="..tostring(value)
  return true
 end
 local function sample(name,changed)
  if not state or state.status~="ACTIVE" then return end
  local ok,value=pcall(current)
  if not ok then failure(value);publish();return end
  if not add(name,value) then return end
  -- A target-change notification invalidates continuity even if cancellation already emptied it.
  if changed or not empty(value) then
   state.status="INTERRUPTED";state.reason="生产目标/队列发生变化；清空后也不能续算"
  end
  publish()
 end
 local function hook(source,name,fn,required)
  local event=P.Field(source,name)
  if event and event.Add then event.Add(fn);hooks[#hooks+1]=name
  elseif required then hooks[#hooks+1]="MISSING:"..name end
 end
 for _,name in ipairs({"CityProductionChanged","CityProductionQueueChanged","CityProductionUpdated","CityProductionCompleted"}) do
  hook(Events,name,function(pid,cid,...)
   if state and state.status=="ACTIVE" and pid==state.owner and cid==state.id then local args={...};local tail={}
    for i=1,math.min(select("#",...),4) do tail[#tail+1]=tostring(args[i]) end
    sample(name.."("..table.concat(tail,",")..")",name~="CityProductionUpdated") end
  end,true)
 end
 hook(Events,"PlayerTurnDeactivated",function(pid)
  if state and pid==state.owner then sample("PlayerTurnDeactivated",false) end
 end,true)
 local function nextTurn(name,pid)
  if not state or state.status~="ACTIVE" or pid~=state.owner then return end
  sample(name,false)
  if state.status=="ACTIVE" and Game.GetCurrentGameTurn()~=state.turn then
   state.status="ENDED";state.reason="回合边界已到；事件顺序仅为观察，完整生产结算未证实";publish()
  end
 end
 hook(GameEvents,"PlayerTurnStarted",function(pid) nextTurn("PlayerTurnStarted",pid) end,true)
 hook(Events,"PlayerTurnActivated",function(pid) nextTurn("PlayerTurnActivated",pid) end,true)
 hook(Events,"CityRemovedFromMap",function(pid,cid)
  if state and state.status=="ACTIVE" and pid==state.owner and cid==state.id then
   state.status="STOPPED";state.reason="城市移除/易主，停止观察";publish()
  end
 end,true)
 function api.Request(pid,params)
  if params.Action=="TIMED_PRODUCTION_CANCEL" then
   if state and state.owner==pid and state.token==params.Token and state.status=="ACTIVE" then
    state.status="STOPPED";state.reason="UI取消/中断";publish()
   end
   return
  end
  if params.Action~="TIMED_PRODUCTION_BEGIN" then return end
  if state and state.token==params.Token then return end
  if state and state.status=="ACTIVE" then shared.TimedProductionBeginError={token=params.Token,reason="另一次观察仍活动，拒绝替换"};return end
  state={token=params.Token,owner=pid,id=params.CityID,turn=params.StartTurn,status="STOPPED",rows={}}
  local ok,err=pcall(function()
   assert(P.IsTestPlayer(pid) and params.StartTurn==Game.GetCurrentGameTurn(),"开始请求过期/玩家无效")
   assert(not table.concat(hooks,","):find("MISSING:",1,true),"必要事件接口缺失："..table.concat(hooks,", "))
   local c=assert(Players[pid]:GetCities():FindID(params.CityID),"城市不存在")
   state.x=c:GetX();state.y=c:GetY()
   local v=current();assert(empty(v),"Gameplay目标非空："..tostring(v))
   state.status="ACTIVE";state.reason="等待原生事件；不自动证明生产结算";add("BEGIN",v)
  end)
  if not ok then failure(err) end
  publish()
 end
 publish()
end
