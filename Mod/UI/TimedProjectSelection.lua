-- Explicit production-list selection -> one confirmed begin request. No load/hover activation.
SPCTimedProjectSelection={}
function SPCTimedProjectSelection.New(P,send,notify)
 local api={};local pending=nil;local seen=nil
 local function expose(status,reason)
  if not pending then return end
  ExposedMembers.SPC_TimedProjectSelection={owner=pending.owner,id=pending.id,token=pending.token,status=status,reason=reason}
 end
 function api.Before(c,item)
  if not item or item.Type~="PROJECT_SPC_OVERFLOW_SINK_TEST" then return true end
  if not c or not P.IsTestPlayer(c:GetOwner()) then return false end
  local g=(ExposedMembers.SPC_P0 or {}).TimedProjectState
  if pending then return false end
  if g and (g.status=="ACTIVE" or g.status=="CONFIRMING") then
   -- This batch retains the single-city boundary. Never silently replace its timer.
   ExposedMembers.SPC_TimedProjectSelection={owner=c:GetOwner(),id=c:GetID(),status="ERROR",reason="当前已有一个项目计时；本批仅支持单城实验"}
   notify(c:GetOwner(),c:GetID());return false
  end
  ExposedMembers.SPC_TimedProjectSerial=(ExposedMembers.SPC_TimedProjectSerial or 0)+1
  pending={owner=c:GetOwner(),id=c:GetID(),turn=Game.GetCurrentGameTurn(),token="B122:"..Game.GetCurrentGameTurn()..":"..ExposedMembers.SPC_TimedProjectSerial,sent=false}
  expose("PENDING","等待原生选择生产确认");return true
 end
 function api.Pulse()
  local g=(ExposedMembers.SPC_P0 or {}).TimedProjectState
  if pending then
   if g and g.token==pending.token then
    expose("ACK",g.reason);pending=nil
   elseif Game.GetCurrentGameTurn()~=pending.turn then
    expose("ERROR","选择/启动未在本回合确认；请重新选择项目");notify(pending.owner,pending.id);pending=nil
   elseif not pending.sent then
    local ok,v=pcall(function()return ExposedMembers.SPC_ProjectTurnRead(pending.owner,pending.id)end)
    if ok and v.owner==pending.owner and v.id==pending.id and v.turn==pending.turn and v.isProject then
     if v.size~=1 then
      expose("ERROR","本批项目必须为唯一当前目标，不能排队计时");notify(pending.owner,pending.id);pending=nil
     else
      -- Latch first: repeated publish notifications cannot submit twice.
      pending.sent=true;expose("PENDING","已选择项目，等待计时确认")
      local good,err=pcall(send,pending.owner,PlayerOperations.EXECUTE_SCRIPT,{OnStart="SPC_P0_Request",Action="TIMED_PROJECT_BEGIN",Token=pending.token,CityID=pending.id,StartTurn=pending.turn})
      if not good then expose("ERROR","计时请求异常；不重发："..tostring(err));notify(pending.owner,pending.id);pending=nil end
     end
    end
   end
  end
  g=(ExposedMembers.SPC_P0 or {}).TimedProjectState
  if g then
   local signature=g.token..":"..g.status..":"..tostring(g.deactivated)
   if signature~=seen then seen=signature;notify(g.owner,g.id)end
  end
 end
 return api
end
