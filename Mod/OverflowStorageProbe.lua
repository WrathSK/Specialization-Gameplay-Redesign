-- B119: native FinishProgress on a dedicated no-reward project; not a storage clearing service.
SPCOverflowStorageProbe={}
function SPCOverflowStorageProbe.Start(P,shared)
 local api={};shared.OverflowStorageProbe=api
 local pending=nil;local epochs={};local used={};local count=0;local missingHook=false
 local function key(pid,id) return tostring(pid)..":"..tostring(id) end
 local project="PROJECT_SPC_OVERFLOW_SINK_TEST"
 local function finite(v) return type(v)=="number" and v==v and math.abs(v)<math.huge end
 local function city(pid,id)
  assert(P.IsTestPlayer(pid),"玩家资格失效")
  local c=Players[pid] and Players[pid]:GetCities():FindID(id)
  assert(c and c:GetOwner()==pid,"测试城不可确认")
  local q=c:GetBuildQueue();local ok,v=P.Call(q,"CurrentlyBuilding")
  assert(ok and v==project,"Gameplay目标不是专用溢出承接实验；不写入")
  -- GetSize is UI-only on known builds. If also exposed here it must agree.
  if type(P.Field(q,"GetSize"))=="function" then
   local good,n=P.Call(q,"GetSize");assert(good and n==1,"Gameplay队列必须只有专用实验项目")
  end
  assert(type(P.Field(q,"FinishProgress"))=="function","FinishProgress不可用")
  return c,q
 end
 local attemptAmount=nil
 local function publish(params,pid,state,reason)
  shared.OverflowStorage={token=params.Token,owner=pid,id=params.CityID,turn=Game.GetCurrentGameTurn(),status=state,reason=reason,amount=attemptAmount}
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
   assert(not (shared.TimedProject and shared.TimedProject.BlocksManual(pid,params.CityID)),"本城自动计时活动或已尝试完成；禁止混用手动工具")
   local k=key(pid,params.CityID)
   assert(not used[k],"本城本次加载已调用或结果不明；禁止重复完成，重载测试前存档")
   local c,q=city(pid,params.CityID)
   local reader=ExposedMembers.SPC_OverflowExactRead
   assert(type(reader)=="function","UI即时项目读数桥不可用；不写入")
   local facts=reader(pid,params.CityID)
   assert(type(facts)=="table" and facts.owner==pid and facts.id==params.CityID and facts.turn==params.StartTurn
    and facts.project==project and facts.size==1,"UI即时目标/队列无法确认")
   local value=facts.value
   assert(finite(value) and value>=0 and value<=10000,"实验要求0≤项目进度≤10000；负数或超界均不写入")
   assert(value==params.Progress,"即时项目进度与本次请求不同；重新准备")
   if params.Action=="OVERFLOW_PREPARE" then
    assert(count<16,"本次加载实验上限已到")
    if pending and pending.token==params.Token then return end
    epochs={};epochs[k]=0
    pending={owner=pid,id=params.CityID,x=c:GetX(),y=c:GetY(),turn=params.StartTurn,token=params.Token,epoch=0,progress=value}
    attemptAmount=value
    publish(params,pid,"PREPARED","尚未写入；再次左键仅原生完成专用无收益项目。")
    return
   end
   assert(pending and pending.token==params.Token and pending.owner==pid and pending.id==params.CityID
    and pending.turn==params.StartTurn and pending.x==c:GetX() and pending.y==c:GetY()
    and pending.progress==value and pending.epoch==(epochs[k] or 0),"准备后城市/生产状态变化；必须重新准备，不写入")
   -- Latch BEFORE the native call; even an exception cannot justify retry.
   used[k]=true;count=count+1;pending=nil;attempted=true
   attemptAmount=value
   q:FinishProgress()
   publish(params,pid,"CALLED_NOT_PROVEN","已调用一次原生FinishProgress；不代表无溢出。右键刷新当前状态，再检查后续目标，勿重试。")
  end)
  if not ok then
   local raw=tostring(err);print("[SPC][OverflowStorage] "..raw)
   publish(params,pid,attempted and "UNCERTAIN_NO_RETRY" or "REJECTED",raw:gsub("^.-:%d+: ?",""):match("^[^\r\n]+") or "接口失败")
  end
 end
end
