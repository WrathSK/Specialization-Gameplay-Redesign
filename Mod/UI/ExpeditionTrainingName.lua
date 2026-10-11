-- B203: one bounded observer for normally trained teams; no diagnostic-window writer.
include('Probe')
include('ExpeditionSpyRead')
local P=SPCP0
local job,record
local seq=0
local initialized=false
local stopped=false
local function view()return ExposedMembers.SPC_ExpeditionActivity end
local function same(v,r)
 return v and r and v.owner==r.owner and v.unitID==r.id and v.teamKey==r.key and v.trainingToken==r.trainingToken
end
local function cancel()job=nil;ContextPtr:ClearUpdate()end
local function publish(status,reason)
 if not record then return end
 record.status=status;record.reason=reason
 ExposedMembers.SPC_ExpeditionTrainingNameError=reason
 ExposedMembers.SPC_ExpeditionTrainingNameStatus={owner=record.owner,unitID=record.id,teamKey=record.key,
  status=status,reason=reason,attempts=record.attempts}
 if LuaEvents and LuaEvents.SPC_ExpeditionActivityChanged then LuaEvents.SPC_ExpeditionActivityChanged()end
end
local function stop(status,reason)cancel();publish(status,reason)end
local function confirmed(v,r)
 return same(v,r) and v.phase=='CREATED' and type(v.expectedName)=='string'
  and r.sentName~=nil and v.expectedName==r.sentName
end
local function valid(v)
 return v and v.phase=='NAMING' and type(v.trainingToken)=='string' and type(v.teamKey)=='string'
  and type(v.unitID)=='number' and v.owner==Game.GetLocalPlayer() and P.IsTestPlayer(v.owner)
end
local function tick(dt)
 local j=job;if not j or stopped then return end
 local v=view()
 if confirmed(v,j)then stop('READY');return end
 if not same(v,j) or not valid(v)then stop('STOPPED','TRAINING_NAME_STATE_CHANGED');return end
 if j.sent then
  local reply=ExposedMembers.SPC_ExpeditionGateReply
  if reply and reply.owner==j.owner and reply.token==j.token then
   -- Success is the authoritative published transition, never just absence of an error.
   if reply.error then stop('STOPPED',reply.error);return end
  end
 end
 j.elapsed=j.elapsed+(dt or 0);j.poll=j.poll+(dt or 0)
 if j.elapsed>=10 then
  if j.sent then stop('STOPPED','TRAINING_NAME_ACK_UNCONFIRMED')
  elseif record.attempts>=3 then stop('STOPPED','TRAINING_NAME_RETRY_EXHAUSTED')
  else stop('WAITING','TRAINING_NAME_NOT_READY')end
  return
 end
 if j.poll<0.25 or j.sent then return end;j.poll=0
 local ok,r=pcall(SPCExpeditionSpyRead.NativeName,j.owner,j.id)
 -- Native readers/events may reenter; never send for an invalidated job.
 if job~=j or not same(view(),j) or not valid(view())then cancel();return end
 if not ok then stop('STOPPED','TRAINING_NAME_READ_ERROR');return end
 if r.status=='PENDING' then return end
 if r.status~='READY' then stop('STOPPED',r.reason or 'TRAINING_NAME_INVALID');return end
 seq=seq+1;j.token='TRAIN_NAME:'..j.key..':'..seq;j.sent=true;j.sentName=r.name;record.sentName=r.name
 j.elapsed=0 -- Give the asynchronous acknowledgement its own bounded window.
 publish('CONFIRMING')
 if job~=j or not same(view(),j) or not valid(view())then cancel();return end
 local sent=pcall(UI.RequestPlayerOperation,j.owner,PlayerOperations.EXECUTE_SCRIPT,
  {OnStart='SPC_ExpeditionGateRequest',Action='NAME',Token=j.token,UnitID=j.id,Name=r.name,
   NameOffmapChecked=true,NameSampleTurn=Game.GetCurrentGameTurn()})
 if job~=j then return end
 if confirmed(view(),j)then stop('READY')
 elseif not sent then stop('STOPPED','TRAINING_NAME_SEND_UNCONFIRMED')end
end
local function pulse(retry)
 if stopped then return end
 local v=view()
 if record and confirmed(v,record)then
  if record.status~='READY' then stop('READY')end
  return
 end
 if not valid(v)then
  cancel()
  if record and (not same(v,record) or v.phase~='NAMING')then
   record=nil;ExposedMembers.SPC_ExpeditionTrainingNameStatus=nil;ExposedMembers.SPC_ExpeditionTrainingNameError=nil
  end
  return
 end
 if not same(v,record)then
  cancel();record={owner=v.owner,id=v.unitID,key=v.teamKey,trainingToken=v.trainingToken,attempts=0}
 end
 if job or record.status=='STOPPED' or record.status=='READY' then return end
 if record.status=='WAITING' and not retry then return end
 if record.attempts>=3 then stop('STOPPED','TRAINING_NAME_RETRY_EXHAUSTED');return end
 record.attempts=record.attempts+1
 job={owner=record.owner,id=record.id,key=record.key,trainingToken=record.trainingToken,elapsed=0,poll=0}
 local j=job
 publish('PENDING')
 if job==j then ContextPtr:SetUpdate(tick)end
end
local function published()pulse(false)end
local function retry()pulse(true)end
local function selection(owner,id,...) -- Read selected unit, not a guessed event boolean layout.
 local v=view();if not valid(v) or owner~=v.owner or id~=v.unitID then return end
 local u=UI.GetHeadSelectedUnit()
 if u and u:GetOwner()==owner and u:GetID()==id then pulse(true)end
end
local function initialize()
 if initialized then return end;initialized=true
 Events.GameCoreEventPublishComplete.Add(published);Events.LoadScreenClose.Add(retry)
 Events.LocalPlayerTurnBegin.Add(retry);Events.UnitSelectionChanged.Add(selection)
 pulse(false)
end
ContextPtr:SetInitHandler(initialize)
ContextPtr:SetShutdown(function()
 stopped=true;cancel();record=nil
 ExposedMembers.SPC_ExpeditionTrainingNameStatus=nil;ExposedMembers.SPC_ExpeditionTrainingNameError=nil
 if initialized then
  Events.GameCoreEventPublishComplete.Remove(published);Events.LoadScreenClose.Remove(retry)
  Events.LocalPlayerTurnBegin.Remove(retry);Events.UnitSelectionChanged.Remove(selection)
 end
end)
