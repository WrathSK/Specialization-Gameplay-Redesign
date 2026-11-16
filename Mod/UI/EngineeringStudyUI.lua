include('TimedProjectSelectionClient')
include('TimedProjectQueueIntent')
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
 if v and v.stage=='ACTIVE'then return '1',Locale.Lookup('LOC_SPC_TIMED_PROJECT_STUDY_ACTIVE')end
 if v and v.stage=='CALLING'then return Locale.Lookup('LOC_SPC_TIMED_QUEUE_LABEL_UNCONFIRMED'),Locale.Lookup('LOC_SPC_TIMED_PROJECT_STUDY_COMPLETION_PENDING')end
 if v and v.stage=='HELD'then
  if v.reason=='EST_SINGLE_PROJECT_REQUIRED'then return Locale.Lookup('LOC_SPC_TIMED_QUEUE_LABEL_PAUSED'),Locale.Lookup('LOC_SPC_TIMED_PROJECT_STUDY_REQUIRES_SOLE_ENTRY')end
  return Locale.Lookup('LOC_SPC_TIMED_QUEUE_LABEL_PAUSED'),Locale.Lookup('LOC_SPC_TIMED_PROJECT_STUDY_PAUSED')
 end
 local queueStatus=ExposedMembers.SPC_EngineeringStudyQueueStatus
 if type(queueStatus)=='function'then local ok,label,note=pcall(queueStatus,pid,id);if ok and label then return label,note end end
 local c=Players[pid] and Players[pid]:GetCities():FindID(id)
 if M.Current(c)then return Locale.Lookup('LOC_SPC_TIMED_QUEUE_LABEL_CONFIRMING'),Locale.Lookup('LOC_SPC_TIMED_PROJECT_STUDY_START_PENDING')end
 return '1',Locale.Lookup('LOC_SPC_TIMED_PROJECT_STUDY_PREVIEW')
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
 client.Configure('EngineeringStudy','SPC_EngineeringStudyRead','ENGINEERING_STUDY_SYNC',send)
 local queueIntent=SPCTimedProjectQueueIntent.New(P,client,'EngineeringStudy',send,notify);client.AttachQueueIntent(queueIntent)
 a.Connect=client.Connect;a.Sync=client.Sync;a.WarmStart=client.WarmStart
 function a.Before(c,item,queued)
  if not client.OwnsReader()then return not item or item.Type~=M.PROJECT end
  local k=c and (c:GetOwner()..':'..c:GetID())
  if not item or item.Type~=M.PROJECT then if k then pending[k]=nil end;return true end
  if c and queueIntent.Supported(c)then
   pending[k]=nil;return queueIntent.Before(c,item,queued)
  end
  if not c or queued or not P.IsTestPlayer(c:GetOwner())then return false end
  pending[k]={pid=c:GetOwner(),id=c:GetID(),turn=Game.GetCurrentGameTurn(),read=true};return true
 end
 function a.CancelSelection(c)
  if c then pending[c:GetOwner()..':'..c:GetID()]=nil;queueIntent.CancelUnconfirmed(c)end
 end
 local function drain()
  local d=(ExposedMembers.SPC_P0 or {}).EngineeringStudy;if not d then return end
  for k,p in pairs(pending)do
   if not client.OwnsReader()then return end
   if p.turn~=Game.GetCurrentGameTurn()then pending[k]=nil
   elseif p.read and client.Ready()then
    local ok,q,current=client.Read(k,p,function()return ExposedMembers.SPC_EngineeringStudyRead(p.pid,p.id)end)
    if current and ok and q.project==M.PROJECT and q.size==1 then
     pending[k]=nil -- latch before native re-entry; no ambiguous resend
     pcall(send,p.pid,PlayerOperations.EXECUTE_SCRIPT,{OnStart='SPC_P0_Request',Action='ENGINEERING_STUDY_BEGIN',CityID=p.id,StartTurn=p.turn,Token='EST:'..k..':'..p.turn})
    elseif current and ok and q.project==M.PROJECT and type(q.size)=='number' and q.size>1 then pending[k]=nil;notify(p.pid,p.id)end
   end
  end
  if not client.OwnsReader()then return end
  if revision==d.revision then return end;revision=d.revision
  for k in pairs(seen)do if not d.views[k]then seen[k]=nil;pending[k]=nil end end
  for k,v in pairs(d.views)do
   if not client.OwnsReader()then return end
   local sig=v.stage..':'..tostring(v.start)..':'..v.reason..':'..tostring(v.L)
   if seen[k]~=sig then seen[k]=sig;local pid,id=k:match('^(%d+):(%d+)$');if pid then notify(tonumber(pid),tonumber(id))end end
  end
 end
 a.Publish=client.Bind(drain)
 return a
end
