-- Exact Claim entry/read model. No UI-owned timer or per-frame requests.
SPCClaimProjectUI={}
local M=SPCClaimProjectUI
local kinds={RESEARCH=true,CULTURE=true,INDUSTRY=true,COMMERCE=true}
function M.IsProject(name)return type(name)=='string' and kinds[name:match('^PROJECT_SPC_CLAIM_(.+)$')] or false end
function M.Current(c)
 if not c or c:GetOwner()~=Game.GetLocalPlayer()then return nil end
 local hash=c:GetBuildQueue():GetCurrentProductionTypeHash()
 for kind in pairs(kinds)do local name='PROJECT_SPC_CLAIM_'..kind;local row=GameInfo.Projects[name]
  if row and row.Hash==hash then return name end
 end
end
function M.Text(pid,id,project)
 local s=(ExposedMembers.SPC_P0 or {}).ClaimProjects
 local view=s and s.views[tostring(pid)..':'..tostring(id)]
 if view and view.stage=='ACTIVE' and view.project==project then return '1',view.reason end
 if view and (view.stage=='STOPPED' or view.stage=='CALLING')then return '已暂停',view.reason end
 local c=Players[pid] and Players[pid]:GetCities():FindID(id)
 if M.Current(c)==project then
  local v=ExposedMembers.SPC_ClaimSelection and ExposedMembers.SPC_ClaimSelection[tostring(pid)..':'..tostring(id)]
  local sync=ExposedMembers.SPC_ClaimSync and ExposedMembers.SPC_ClaimSync[tostring(pid)..':'..tostring(id)]
  return '确认中',v or sync or '等待Gameplay确认；若持续如此请查看当前项目提示'
 end
 return '1','认领需完整一回合；完成才建立专业。已有未分配生产与项目期间生产不留给后续目标。'
end
function M.New(P,send,notify)
 local api={};local pending={};local seen={};local pendingText={};local synced={};local warmed=false;local pulse=0
 ExposedMembers.SPC_ClaimSelection={}
 ExposedMembers.SPC_ClaimSync={}
 ExposedMembers.SPC_ClaimQueueRead=function(pid,id)
  local c=assert(Players[pid] and Players[pid]:GetCities():FindID(id));assert(c:GetOwner()==pid)
  return {owner=pid,id=id,turn=Game.GetCurrentGameTurn(),project=M.Current(c),size=c:GetBuildQueue():GetSize()}
 end
 -- At most three sends per city/UI lifetime, on bounded publish opportunities.
 -- Sending is not acknowledgement. Sync never creates or restarts a saved timer.
 function api.Sync(c)
  if not c or not P.IsTestPlayer(c:GetOwner())then return end
  local k=tostring(c:GetOwner())..':'..c:GetID()
  local s=synced[k]
  if not s then s={owner=c:GetOwner(),id=c:GetID(),tries=0,nextPulse=pulse};synced[k]=s end
  local backend=(ExposedMembers.SPC_P0 or {}).ClaimProjects
  if backend and backend.syncAck and s.token and backend.syncAck[k]==s.token then
   s.done=true;ExposedMembers.SPC_ClaimSync[k]=nil;return
  end
  if s.done or pulse<s.nextPulse then return end
  if backend and backend.startupError then
   ExposedMembers.SPC_ClaimSync[k]='认领模块未就绪：'..backend.startupError;return
  end
  if s.tries>=3 then
   ExposedMembers.SPC_ClaimSync[k]='读档同步未获确认；请保留存档和E2报告，暂停测试';return
  end
  -- Wait for the actual module; early UI construction must not consume retries.
  if not backend then ExposedMembers.SPC_ClaimSync[k]='等待认领模块加载';return end
  s.tries=s.tries+1;s.token='CLAIM_SYNC:'..k..':'..s.tries
  s.nextPulse=pulse+(s.tries==1 and 4 or 12)
  ExposedMembers.SPC_ClaimSync[k]='读档同步等待确认（'..s.tries..'/3）'
  local ok,err=pcall(send,c:GetOwner(),PlayerOperations.EXECUTE_SCRIPT,{OnStart='SPC_P0_Request',Action='CLAIM_SYNC',Token=s.token,CityID=c:GetID()})
  if not ok then ExposedMembers.SPC_ClaimSync[k]='读档同步发送失败：'..tostring(err)end
 end
 -- One bounded local-city reconciliation per UI lifetime, independent of opening a panel.
 function api.WarmStart()
  if warmed then return end
  local pid=Game.GetLocalPlayer();local player=Players[pid]
  if not player or not P.IsTestPlayer(pid)then return end
  warmed=true
  for _,c in player:GetCities():Members()do api.Sync(c)end
 end
 function api.Before(c,item,queueMode)
  local name=item and item.Type;local k=c and tostring(c:GetOwner())..':'..c:GetID()
  if not M.IsProject(name)then if k then pending[k]=nil;ExposedMembers.SPC_ClaimSelection[k]=nil end;return true end
  if not c or not P.IsTestPlayer(c:GetOwner())then return false end
  if queueMode then ExposedMembers.SPC_ClaimSelection[k]='认领项目不能排在队列后面；请选为唯一当前目标';notify(c:GetOwner(),c:GetID());return false end
  if pending[k]then return false end
  pending[k]={owner=c:GetOwner(),id=c:GetID(),project=name,turn=Game.GetCurrentGameTurn()}
  ExposedMembers.SPC_ClaimSelection[k]='等待原生选择确认';return true
 end
 function api.Pulse()
  pulse=pulse+1
  api.WarmStart() -- fallback when this context missed LoadScreenClose; no repeated city scan
  local shared=(ExposedMembers.SPC_P0 or {}).ClaimProjects
  for _,s in pairs(synced)do if not s.done then
   local c=Players[s.owner] and Players[s.owner]:GetCities():FindID(s.id)
   if c then api.Sync(c)end
  end end
  for k,p in pairs(pending)do
   local view=shared and shared.views[k]
   if view and view.project==p.project and view.stage=='ACTIVE' then pending[k]=nil;ExposedMembers.SPC_ClaimSelection[k]=nil
   elseif p.sent and view and view.stage=='STOPPED' then pending[k]=nil;ExposedMembers.SPC_ClaimSelection[k]=view.reason;notify(p.owner,p.id)
   elseif p.turn~=Game.GetCurrentGameTurn()then pending[k]=nil;ExposedMembers.SPC_ClaimSelection[k]='启动确认超时；请重新选择项目';notify(p.owner,p.id)
   elseif not p.sent then
    local ok,v=pcall(ExposedMembers.SPC_ClaimQueueRead,p.owner,p.id)
    if ok and v.project==p.project then
     if v.size==1 then
      p.sent=true
      local good,err=pcall(send,p.owner,PlayerOperations.EXECUTE_SCRIPT,{OnStart='SPC_P0_Request',Action='CLAIM_BEGIN',Token='CLAIM:'..k..':'..p.turn,CityID=p.id,Project=p.project,StartTurn=p.turn})
      if not good then ExposedMembers.SPC_ClaimSelection[k]='启动请求失败：'..tostring(err);pending[k]=nil;notify(p.owner,p.id)end
     elseif type(v.size)=='number' and v.size>1 then
      ExposedMembers.SPC_ClaimSelection[k]='认领必须为唯一当前目标；队列数量='..v.size;pending[k]=nil;notify(p.owner,p.id)
     else ExposedMembers.SPC_ClaimSelection[k]='等待队列确认；数量='..tostring(v.size)end
    end
   end
  end
  for k,reason in pairs(ExposedMembers.SPC_ClaimSelection)do
   if pendingText[k]~=reason then pendingText[k]=reason;local pid,id=k:match('^(%d+):(%d+)$');if pid then notify(tonumber(pid),tonumber(id))end end
  end
  if shared then
   for k,v in pairs(shared.views)do
    local signature=tostring(v.stage)..':'..tostring(v.project)..':'..tostring(v.start)..':'..v.reason
    if signature~=seen[k]then seen[k]=signature;local pid,id=k:match('^(%d+):(%d+)$');if pid then notify(tonumber(pid),tonumber(id))end end
   end
  end
 end
 return api
end
