-- Explicit production-list selection -> one confirmed begin request. No load/hover activation.
SPCTimedProjectSelection={}
function SPCTimedProjectSelection.New(P,send,notify)
 local api={};local pending=nil;local seen=nil;local shownPending=nil
 -- This field is UI presentation, not a timer authority. A new UI context must
 -- not inherit an earlier session's rejection or pending click.
 ExposedMembers.SPC_TimedProjectSelection=nil
 local function expose(status,reason)
  if not pending then return end
  ExposedMembers.SPC_TimedProjectSelection={owner=pending.owner,id=pending.id,token=pending.token,status=status,reason=reason,queueSize=pending.queueSize}
 end
 function api.Before(c,item)
  if not item or item.Type~="PROJECT_SPC_OVERFLOW_SINK_TEST" then
   if pending and c and c:GetOwner()==pending.owner and c:GetID()==pending.id and not pending.sent then
    expose("ERROR","已改选其它生产目标；未启动计时");pending=nil
   end
   return true
  end
  if not c or not P.IsTestPlayer(c:GetOwner()) then return false end
  local g=(ExposedMembers.SPC_P0 or {}).TimedProjectState
  if pending then return false end
  if g and (g.status=="ACTIVE" or g.status=="CONFIRMING") then
   -- This batch retains the single-city boundary. Never silently replace its timer.
   ExposedMembers.SPC_TimedProjectSelection={owner=c:GetOwner(),id=c:GetID(),status="ERROR",reason="当前已有一个项目计时；本批仅支持单城实验"}
   notify(c:GetOwner(),c:GetID());return false
  end
  ExposedMembers.SPC_TimedProjectSerial=(ExposedMembers.SPC_TimedProjectSerial or 0)+1
  pending={owner=c:GetOwner(),id=c:GetID(),turn=Game.GetCurrentGameTurn(),token="B123:"..Game.GetCurrentGameTurn()..":"..ExposedMembers.SPC_TimedProjectSerial,sent=false}
  expose("PENDING","等待原生选择生产确认");return true
 end
 function api.Pulse()
  local g=(ExposedMembers.SPC_P0 or {}).TimedProjectState
  if pending then
   if g and g.token==pending.token then
    expose("ACK",g.reason);pending=nil
   elseif Game.GetCurrentGameTurn()~=pending.turn then
    expose("ERROR","启动确认超时；队列数量="..tostring(pending.queueSize or "未知").."；请重新选择项目");notify(pending.owner,pending.id);pending=nil
   elseif not pending.sent then
    local ok,v=pcall(function()return ExposedMembers.SPC_ProjectTurnRead(pending.owner,pending.id)end)
    if ok and type(v)=="table" and v.owner==pending.owner and v.id==pending.id and v.turn==pending.turn then
     pending.queueSize=v.size
     if not v.isProject then
      expose("PENDING","等待当前生产目标确认；队列数量="..tostring(v.size))
     elseif type(v.size)=="number" and v.size>1 then
      expose("ERROR","启动被拒绝：队列数量="..tostring(v.size).."；项目必须是唯一当前目标")
      notify(pending.owner,pending.id);pending=nil
     elseif v.size~=1 then
      -- A hash and queue count need not become visible in the same publish.
      -- Wait only for this explicit click, within its starting turn; no polling,
      -- no request until size=1, and never reinterpret zero as a valid queue.
      expose("PENDING","等待队列确认；数量="..tostring(v.size).."（需要1）")
     else
      -- Latch first: repeated publish notifications cannot submit twice.
      pending.sent=true;expose("PENDING","已选择项目，等待计时确认")
      local good,err=pcall(send,pending.owner,PlayerOperations.EXECUTE_SCRIPT,{OnStart="SPC_P0_Request",Action="TIMED_PROJECT_BEGIN",Token=pending.token,CityID=pending.id,StartTurn=pending.turn})
      if not good then expose("ERROR","计时请求异常；不重发："..tostring(err));notify(pending.owner,pending.id);pending=nil end
     end
    else
     expose("PENDING","等待城市/队列读取确认；未提交计时请求")
    end
   end
  end
  local view=ExposedMembers.SPC_TimedProjectSelection
  if view and view.status=="PENDING" then
   local signature=view.token..":"..view.reason
   if signature~=shownPending then shownPending=signature;notify(view.owner,view.id)end
  end
  g=(ExposedMembers.SPC_P0 or {}).TimedProjectState
  if g then
   local signature=g.token..":"..g.status..":"..tostring(g.deactivated)
   if signature~=seen then seen=signature;notify(g.owner,g.id)end
  end
 end
 return api
end
