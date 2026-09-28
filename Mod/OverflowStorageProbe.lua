-- B117: explicit disposable-save primitive experiment, not an overflow clearing service.
SPCOverflowStorageProbe={}
function SPCOverflowStorageProbe.Start(P,shared)
 local api={};shared.OverflowStorageProbe=api
 local pending=nil;local epochs={};local used={};local count=0;local missingHook=false
 local function key(pid,id) return tostring(pid)..":"..tostring(id) end
 local function empty(v) return v==nil or v=="" or v=="NONE" end
 local function city(pid,id)
  assert(P.IsTestPlayer(pid),"玩家资格失效")
  local c=Players[pid] and Players[pid]:GetCities():FindID(id)
  assert(c and c:GetOwner()==pid,"测试城不可确认")
  local q=c:GetBuildQueue();local ok,v=P.Call(q,"CurrentlyBuilding")
  assert(ok and empty(v),"Gameplay目标不是已确认空队列；不调用负数")
  -- GetSize is UI-only on known builds. If also exposed here it must agree.
  if type(P.Field(q,"GetSize"))=="function" then
   local good,n=P.Call(q,"GetSize");assert(good and n==0,"Gameplay队列非空或不可读")
  end
  assert(type(P.Field(q,"AddProgress"))=="function","AddProgress不可用")
  return c,q
 end
 local function publish(params,pid,state,reason)
  shared.OverflowStorage={token=params.Token,owner=pid,id=params.CityID,turn=Game.GetCurrentGameTurn(),status=state,reason=reason,amount=-1000}
 end
 local function changed(pid,id)
  -- Track only the current prepared city; never scan the world.
  if pending and pid==pending.owner and id==pending.id then
   local k=key(pid,id);epochs[k]=(epochs[k] or 0)+1
  end
 end
 for _,n in ipairs({"CityProductionChanged","CityProductionQueueChanged","CityProductionUpdated","CityProductionCompleted","CityRemovedFromMap"}) do
  local e=P.Field(Events,n);if e and e.Add then e.Add(changed) else missingHook=true end
 end
 function api.Request(pid,params)
  if type(params)~="table" or type(params.Token)~="string" or #params.Token>100 then return end
  if params.Action~="OVERFLOW_PREPARE" and params.Action~="OVERFLOW_APPLY" then return end
  local attempted=false
  local ok,err=pcall(function()
   assert(type(params.CityID)=="number" and params.StartTurn==Game.GetCurrentGameTurn(),"请求过期/城市无效")
   assert(not missingHook,"生产/城市事件接口缺失；不能保护准备后的状态变化")
   local k=key(pid,params.CityID)
   assert(not used[k],"本城本次加载已调用或结果不明；禁止重复扣除，重载测试前存档")
   local c,q=city(pid,params.CityID)
   if params.Action=="OVERFLOW_PREPARE" then
    assert(count<16,"本次加载实验上限已到")
    if pending and pending.token==params.Token then return end
    epochs={};epochs[k]=0
    pending={owner=pid,id=params.CityID,x=c:GetX(),y=c:GetY(),turn=params.StartTurn,token=params.Token,epoch=0}
    publish(params,pid,"PREPARED","尚未写入。仅独立测试存档：再次点击才调用−1000；取消可选其它按钮。")
    return
   end
   assert(pending and pending.token==params.Token and pending.owner==pid and pending.id==params.CityID
    and pending.turn==params.StartTurn and pending.x==c:GetX() and pending.y==c:GetY()
    and pending.epoch==(epochs[k] or 0),"准备后城市/生产状态变化；必须重新准备，不写入")
   -- Latch BEFORE the native call; even an exception cannot justify retry.
   used[k]=true;count=count+1;pending=nil;attempted=true
   q:AddProgress(-1000)
   publish(params,pid,"CALLED_NOT_PROVEN","已调用一次−1000；不代表已清空。请检查目标进度及下一正常生产回合；不要连续重试。")
  end)
  if not ok then
   local raw=tostring(err);print("[SPC][OverflowStorage] "..raw)
   publish(params,pid,attempted and "UNCERTAIN_NO_RETRY" or "REJECTED",raw:gsub("^.-:%d+: ?",""):match("^[^\r\n]+") or "接口失败")
  end
 end
end
