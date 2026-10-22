-- B122: single-city/session-only native timing prototype, no reward or persisted state.
SPCTimedProject={}
function SPCTimedProject.Start(P,shared)
 local api={};shared.TimedProject=api
 local s=nil;local used={};local completed={};local missing={};local project="PROJECT_SPC_OVERFLOW_SINK_TEST"
 local function key(pid,id)return tostring(pid)..":"..tostring(id)end
 local function live()return s and (s.status=="ACTIVE" or s.status=="CONFIRMING")end
 local function publish()
  if not s then shared.TimedProjectState=nil;return end
  local out={};for k,v in pairs(s)do if k~="inCall" then out[k]=v end end
  shared.TimedProjectState=out
 end
 local function stop(reason) s.status="STOPPED";s.reason=reason;publish() end
 local function facts()
  assert(P.IsTestPlayer(s.owner),"玩家资格失效")
  local c=Players[s.owner] and Players[s.owner]:GetCities():FindID(s.id)
  assert(c and c:GetOwner()==s.owner and c:GetX()==s.x and c:GetY()==s.y,"城市移除/易主/引用变化")
  local q=c:GetBuildQueue();local ok,target=P.Call(q,"CurrentlyBuilding")
  assert(ok,"当前生产目标未知")
  return q,target
 end
 local function confirm()
  if not s or s.status~="CONFIRMING" or s.inCall then return end
  local ok,q,target=pcall(facts)
  if not ok then stop("完成结果未知；不重试："..tostring(q));return end
  if target~=project then
   completed[key(s.owner,s.id)]=true
   s.status="COMPLETED";s.reason="一次原生调用后目标已退出；请检查后续普通目标是否仍为0进度"
  elseif Game.GetCurrentGameTurn()>s.start+1 then
   s.status="STOPPED";s.reason="调用后仍未确认退出；不重试"
  end
  publish()
 end
 function api.BlocksManual(pid,id)
  return used[key(pid,id)] or (live() and s.owner==pid and s.id==id)
 end
 local function cityEvent(kind,pid,id)
  if not live() or s.owner~=pid or s.id~=id or s.inCall then return end
  if s.status=="CONFIRMING" then confirm();return end
  if kind=="removed" then stop("城市移除/易主；计时中断");return end
  local ok,q,target=pcall(facts)
  if not ok then stop(tostring(q));return end
  if target~=project then
   s.status=kind=="completed" and "EARLY_END" or "STOPPED"
   s.reason=kind=="completed" and "项目提前退出；不阻止自然/强制完成，不再调用" or "当前目标已改变；如需重试请重新开启"
   publish();return
  end
  if kind=="changed" then stop("目标/队列改变通知；连续占用无法确认，需重新开启");return end
  if Game.GetCurrentGameTurn()>s.start+1 then stop("错过下一回合窗口；不延后完成") end
 end
 local function hook(source,name,fn)
  local e=P.Field(source,name);if e and e.Add then e.Add(fn) else missing[#missing+1]=name end
 end
 hook(Events,"CityProductionChanged",function(p,id)cityEvent("changed",p,id)end)
 hook(Events,"CityProductionQueueChanged",function(p,id)cityEvent("changed",p,id)end)
 hook(Events,"CityProductionUpdated",function(p,id)cityEvent("updated",p,id)end)
 hook(Events,"CityProductionCompleted",function(p,id)cityEvent("completed",p,id)end)
 hook(Events,"CityRemovedFromMap",function(p,id)cityEvent("removed",p,id)end)
 hook(Events,"PlayerTurnDeactivated",function(pid)
  if not live() or pid~=s.owner then return end
  if s.status=="CONFIRMING" then confirm();return end
  if Game.GetCurrentGameTurn()~=s.start then stop("结束回合通知超出启动回合");return end
  local ok,q,target=pcall(facts)
  if not ok or target~=project then stop("结束回合时城市/项目不可确认");return end
  s.deactivated=true;publish()
 end)
 hook(Events,"PlayerTurnActivated",function(pid)
  if not live() or pid~=s.owner then return end
  if s.status=="CONFIRMING" then confirm();return end
  local turn=Game.GetCurrentGameTurn()
  if turn==s.start then return end -- duplicate same-turn activation is not a production cycle.
  if turn~=s.start+1 or not s.deactivated then stop("未确认连续的一次正常回合；没有调用完成");return end
  local ok,err=pcall(function()
   local q,target=facts()
   assert(target==project,"当前目标已改变；不完成其它对象")
   if type(P.Field(q,"GetSize"))=="function" then
    local good,n=P.Call(q,"GetSize");assert(good and n==1,"队列不再唯一")
   end
   assert(type(P.Field(q,"FinishProgress"))=="function","原生完成接口不可用")
   -- No UI progress or positive yield prerequisite. Latch before native/reentrant events.
   used[key(s.owner,s.id)]=true;s.attempts=1;s.status="CONFIRMING";s.reason="已调用，正在确认目标退出"
   s.inCall=true;publish();q:FinishProgress();s.inCall=false
  end)
  if not ok then s.inCall=false;stop((s.attempts==1 and "原生调用异常；不重试：" or "未调用：")..tostring(err));return end
  confirm()
 end)
 hook(Events,"GameCoreEventPublishComplete",confirm)
 function api.Request(pid,p)
  if type(p)~="table" or type(p.Token)~="string" or #p.Token>100 then return end
  if p.Action=="TIMED_PROJECT_CANCEL" then
   if s and s.owner==pid and s.id==p.CityID and s.token==p.Token and s.status=="ACTIVE" then stop("用户取消计时；没有完成或清空项目")end
   return
  end
  if p.Action~="TIMED_PROJECT_BEGIN" or live() or (s and s.token==p.Token) then return end
  s={token=p.Token,owner=pid,id=p.CityID,start=p.StartTurn,status="STOPPED",reason="尚未开启",attempts=0,deactivated=false}
  local ok,err=pcall(function()
   assert(type(p.CityID)=="number" and p.StartTurn==Game.GetCurrentGameTurn(),"请求过期/城市无效")
   assert(P.IsTestPlayer(pid),"不是当前本地人类玩家")
   assert(not used[key(pid,p.CityID)] or completed[key(pid,p.CityID)],"上次完成结果不明；不自动重试")
   assert(#missing==0,"必要事件缺失："..table.concat(missing,", "))
   local c=assert(Players[pid] and Players[pid]:GetCities():FindID(p.CityID),"城市不存在")
   s.x=c:GetX();s.y=c:GetY()
   local q,target=facts();assert(target==project,"请先选择专用项目为当前目标")
   assert(type(P.Field(q,"FinishProgress"))=="function","原生完成接口不可用")
   local reader=assert(ExposedMembers.SPC_ProjectTurnRead,"UI队列接口未就绪")
   local v=reader(pid,p.CityID)
   assert(v.owner==pid and v.id==p.CityID and v.turn==s.start and v.isProject and v.size==1,"启动复核失败：队列数量="..tostring(v.size).."；必须为唯一当前项目")
   used[key(pid,p.CityID)]=nil;completed[key(pid,p.CityID)]=nil
   s.status="ACTIVE";s.reason="1回合：正常过回合，下一次恢复操作时尝试自动完成"
  end)
  if not ok then stop(tostring(err)) else publish() end
 end
 publish()
end
