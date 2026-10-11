-- B204: event-first exact-team confirmation; timers only follow a pending read/ack.
include('Probe')
include('ExpeditionSpyRead')
local P=SPCP0
local job,record
local seq=0
local initialized=false
local stopped=false
local busy=false
local notificationWarned=false
local pump
local function detail(v)return tostring(v):gsub('[%c%[%]]',' '):sub(1,160)end
local function view()return ExposedMembers.SPC_ExpeditionActivity end
local function same(v,r)
 return v and r and v.owner==r.owner and v.unitID==r.id and v.teamKey==r.key and v.trainingToken==r.trainingToken
end
local function cancel()job=nil;ContextPtr:ClearUpdate()end
local function notify()
 -- Presentation failure must not strand an assigned job before its first read.
 if LuaEvents and LuaEvents.SPC_ExpeditionActivityChanged then
  local ok,err=pcall(LuaEvents.SPC_ExpeditionActivityChanged)
  if not ok and not notificationWarned then
   notificationWarned=true;print('[SPC][B204][TRAIN_NAME_FEEDBACK] '..detail(err))
  end
 end
end
local function idle()
 local old=ExposedMembers.SPC_ExpeditionTrainingNameStatus
 if old and old.status=='IDLE' and old.initialized==initialized then return end
 ExposedMembers.SPC_ExpeditionTrainingNameError=nil
 ExposedMembers.SPC_ExpeditionTrainingNameStatus={version=P.VERSION,initialized=initialized,status='IDLE'}
 notify()
end
local function publish(status,reason)
 if not record then return end
 reason=reason and detail(reason) or nil
 if record.status==status and record.reason==reason and record.publishedAttempt==record.attempts then return end
 record.status=status;record.reason=reason;record.publishedAttempt=record.attempts
 ExposedMembers.SPC_ExpeditionTrainingNameError=(status=='STOPPED' or status=='WAITING') and reason or nil
 ExposedMembers.SPC_ExpeditionTrainingNameStatus={version=P.VERSION,initialized=initialized,
  owner=record.owner,unitID=record.id,teamKey=record.key,trainingToken=record.trainingToken,
  status=status,reason=reason,attempts=record.attempts,trigger=record.trigger,
  readAttempted=record.readAttempted==true,requestAttempted=record.requestAttempted==true,
  lastReadReason=record.lastReadReason}
 print('[SPC][B204][TRAIN_NAME] stage='..status..' trigger='..detail(record.trigger)..
  ' unit='..tostring(record.id)..' attempt='..tostring(record.attempts)..' reason='..(reason or '-'))
 notify()
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
local function evaluate(j)
 local v=view()
 if confirmed(v,j)then stop('READY');return end
 if job~=j or not same(v,j) or not valid(v)then stop('STOPPED','TRAINING_NAME_STATE_CHANGED');return end
 if j.sent then
  local reply=ExposedMembers.SPC_ExpeditionGateReply
  if reply and reply.owner==j.owner and reply.token==j.token and reply.error then stop('STOPPED',reply.error)end
  return -- Never repeat an attempted request, including from a second event.
 end
 if not j.readAttempted then
  j.readAttempted=true;record.readAttempted=true;publish('READING')
  if job~=j or not same(view(),j) or not valid(view())then cancel();return end
 end
 local ok,r=pcall(SPCExpeditionSpyRead.NativeName,j.owner,j.id)
 -- Readers/notifications may reenter. Authority and exact identity are checked again.
 if job~=j or not same(view(),j) or not valid(view())then cancel();return end
 if not ok or type(r)~='table' then stop('STOPPED','TRAINING_NAME_READ_ERROR');return end
 record.lastReadReason=r.reason and detail(r.reason) or nil
 if r.status=='PENDING' then publish('PENDING',r.reason or 'TRAINING_NAME_NOT_READY');return end
 if r.status~='READY' then stop('STOPPED',r.reason or 'TRAINING_NAME_INVALID');return end
 seq=seq+1;j.token='TRAIN_NAME:'..j.key..':'..seq;j.sent=true;j.sentName=r.name;record.sentName=r.name
 j.elapsed=0;j.poll=0 -- The asynchronous acknowledgement has its own bounded window.
 record.requestAttempted=true;publish('CONFIRMING')
 if job~=j or not same(view(),j) or not valid(view())then cancel();return end
 local sent=pcall(UI.RequestPlayerOperation,j.owner,PlayerOperations.EXECUTE_SCRIPT,
  {OnStart='SPC_ExpeditionGateRequest',Action='NAME',Token=j.token,UnitID=j.id,Name=r.name,
   NameOffmapChecked=true,NameSampleTurn=Game.GetCurrentGameTurn()})
 if job~=j then return end
 if confirmed(view(),j)then stop('READY')
 elseif not sent then stop('STOPPED','TRAINING_NAME_SEND_UNCONFIRMED')end
end
local function process(retry,event,dt)
 local v=view()
 if record and confirmed(v,record)then
  if record.status~='READY' then record.trigger=event;stop('READY')end
  return
 end
 if not valid(v)then
  cancel()
  if record and (not same(v,record) or v.phase~='NAMING')then record=nil;idle()end
  return
 end
 if not same(v,record)then
  cancel();record={owner=v.owner,id=v.unitID,key=v.teamKey,trainingToken=v.trainingToken,attempts=0}
 end
 if record.status=='STOPPED' or record.status=='READY' then return end
 if not job then
  if record.status=='WAITING' and not retry then return end
  if record.attempts>=3 then stop('STOPPED','TRAINING_NAME_RETRY_EXHAUSTED');return end
  record.attempts=record.attempts+1
  job={owner=record.owner,id=record.id,key=record.key,trainingToken=record.trainingToken,elapsed=0,poll=0}
 end
 local j=job;record.trigger=event
 if dt then
  j.elapsed=j.elapsed+dt;j.poll=j.poll+dt
  if j.elapsed>=10 then
   if j.sent then stop('STOPPED','TRAINING_NAME_ACK_UNCONFIRMED')
   elseif record.attempts>=3 then stop('STOPPED','TRAINING_NAME_RETRY_EXHAUSTED')
   else stop('WAITING',record.lastReadReason or 'TRAINING_NAME_NOT_READY')end
   return
  end
  if j.poll<0.25 then return end;j.poll=0
 end
 -- Event wake-ups reach the reader here immediately, even without frame delivery.
 evaluate(j)
 if job==j and not j.timer then
  j.timer=true
  ContextPtr:SetUpdate(function(delta)
   if job==j and not stopped then pump(false,'UPDATE',delta or 0)end
  end)
 end
end
pump=function(retry,event,dt)
 if stopped or busy then return end
 busy=true
 local ok,err=pcall(process,retry,event,dt)
 busy=false
 if not ok then
  if record then stop('STOPPED','TRAINING_NAME_OBSERVER_ERROR')else
   ExposedMembers.SPC_ExpeditionTrainingNameStatus={version=P.VERSION,initialized=initialized,status='ERROR',reason='TRAINING_NAME_OBSERVER_ERROR'}
  end
  print('[SPC][B204][TRAIN_NAME_ERROR] '..detail(err))
 end
end
local function published()pump(false,'PUBLISH')end
local function loaded()pump(true,'LOAD')end
local function turn()pump(true,'TURN')end
local function selection(owner,id,...) -- Read the selected unit, not a guessed boolean layout.
 local v=view();if not valid(v) or owner~=v.owner or id~=v.unitID then return end
 local u=UI.GetHeadSelectedUnit()
 if u and u:GetOwner()==owner and u:GetID()==id then pump(true,'SELECTION')end
end
local function initialize()
 if initialized then return end;initialized=true
 Events.GameCoreEventPublishComplete.Add(published);Events.LoadScreenClose.Add(loaded)
 Events.LocalPlayerTurnBegin.Add(turn);Events.UnitSelectionChanged.Add(selection)
 idle();print('[SPC][B204][TRAIN_NAME] stage=INITIALIZED')
 pump(false,'INIT')
end
-- One transient health/status record; no diagnostic history or persistent fields.
ExposedMembers.SPC_ExpeditionTrainingNameStatus={version=P.VERSION,initialized=false,status='LOADED'}
print('[SPC][B204][TRAIN_NAME] stage=LOADED')
ContextPtr:SetInitHandler(initialize)
ContextPtr:SetShutdown(function()
 stopped=true;cancel();record=nil
 ExposedMembers.SPC_ExpeditionTrainingNameStatus=nil;ExposedMembers.SPC_ExpeditionTrainingNameError=nil
 if initialized then
  Events.GameCoreEventPublishComplete.Remove(published);Events.LoadScreenClose.Remove(loaded)
  Events.LocalPlayerTurnBegin.Remove(turn);Events.UnitSelectionChanged.Remove(selection)
 end
end)
