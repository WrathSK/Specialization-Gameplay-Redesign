include('TimedProjectSelectionClient')
-- Read-only queue bridge and explicit normal-production intent. Existing native
-- publication events drain pending clicks; no timers, frame callbacks or probes.
SPCEngineeringStudyUI={PROJECT='PROJECT_SPC_ENGINEERING_STUDY'}
local M=SPCEngineeringStudyUI
function M.Current(c)
 local row=GameInfo.Projects[M.PROJECT]
 return c and c:GetOwner()==Game.GetLocalPlayer() and row and c:GetBuildQueue():GetCurrentProductionTypeHash()==row.Hash and M.PROJECT or nil
end
function M.Text(pid,id)
 local d=(ExposedMembers.SPC_P0 or {}).EngineeringStudy;local v=d and d.views[pid..':'..id]
 if v and v.stage=='ACTIVE'then return '1','工程传统研习：完整一回合后，本城历史层数 +1。'end
 if v and v.stage=='CALLING'then return '待确认','原生完成回执待确认；不会重复发放。'end
 if v and v.stage=='HELD'then return '已暂停','研习未确认，请查看工业历史报告。'end
 local c=Players[pid] and Players[pid]:GetCities():FindID(id)
 if M.Current(c)then return '确认中','请选择为唯一当前项目；中断后需要重新选择。'end
 return '1','需要工业 ACTIVE IV 且本城 L 小于全国 E；中断取消本轮。'
end
function M.New(P,send,notify)
 local a={};local pending,seen={},{};local revision=-1
 local client=SPCTimedProjectSelectionClient.New(P,pending);a.QueueEvent=client.QueueEvent;a.Close=client.Close
 ExposedMembers.SPC_EngineeringStudyRead=function(pid,id)
  assert(pid==Game.GetLocalPlayer() and P.IsTestPlayer(pid),'EST_UI_OWNER')
  local c=assert(Players[pid]:GetCities():FindID(id),'EST_UI_CITY')
  assert(c:GetOwner()==pid,'EST_UI_OWNER')
  return {reference={owner=pid,cityID=id,x=c:GetX(),y=c:GetY()},turn=Game.GetCurrentGameTurn(),project=M.Current(c),size=c:GetBuildQueue():GetSize()}
 end
 function a.Before(c,item,queued)
  local k=c and (c:GetOwner()..':'..c:GetID())
  if not item or item.Type~=M.PROJECT then if k then pending[k]=nil end;return true end
  if not c or queued or not P.IsTestPlayer(c:GetOwner())then return false end
  pending[k]={pid=c:GetOwner(),id=c:GetID(),turn=Game.GetCurrentGameTurn(),read=true};return true
 end
 local function drain()
  local d=(ExposedMembers.SPC_P0 or {}).EngineeringStudy;if not d then return end
  for k,p in pairs(pending)do
   if p.turn~=Game.GetCurrentGameTurn()then pending[k]=nil
   elseif p.read then
    local ok,q,current=client.Read(k,p,function()return ExposedMembers.SPC_EngineeringStudyRead(p.pid,p.id)end)
    if current and ok and q.project==M.PROJECT and q.size==1 then
     pending[k]=nil -- latch before native re-entry; no ambiguous resend
     pcall(send,p.pid,PlayerOperations.EXECUTE_SCRIPT,{OnStart='SPC_P0_Request',Action='ENGINEERING_STUDY_BEGIN',CityID=p.id,StartTurn=p.turn,Token='EST:'..k..':'..p.turn})
    elseif current and ok and q.project==M.PROJECT and type(q.size)=='number' and q.size>1 then pending[k]=nil;notify(p.pid,p.id)end
   end
  end
  if revision==d.revision then return end;revision=d.revision
  for k in pairs(seen)do if not d.views[k]then seen[k]=nil;pending[k]=nil end end
  for k,v in pairs(d.views)do
   local sig=v.stage..':'..tostring(v.start)..':'..v.reason..':'..tostring(v.L)
   if seen[k]~=sig then seen[k]=sig;local pid,id=k:match('^(%d+):(%d+)$');if pid then notify(tonumber(pid),tonumber(id))end end
  end
 end
 a.Publish=client.Bind(drain)
 return a
end
