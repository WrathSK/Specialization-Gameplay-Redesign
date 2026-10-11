-- B202: bounded admission adapter. Native production owns cost/progress/copy
-- history; this UI never spawns, destroys or teleports the trained unit.
SPCExpeditionTrainingUI={KIND='UNIT_SPC_EXPEDITION_SPY'}
function SPCExpeditionTrainingUI.New(P,send,notify,build)
 local M=SPCExpeditionTrainingUI;local api={};local pending;local selected;local sync;local view;local lastRevision
 local function request(action,c,reservation)
  ExposedMembers.SPC_ExpeditionTrainingSequence=(ExposedMembers.SPC_ExpeditionTrainingSequence or 0)+1
  local token='TRAIN:'..P.VERSION..':'..ExposedMembers.SPC_ExpeditionTrainingSequence
  local packet={OnStart='SPC_ExpeditionTrainingRequest',Action=action,Token=token,CityID=c:GetID(),Reservation=reservation}
  return token,packet
 end
 local function transmit(pid,p)send(pid,PlayerOperations.EXECUTE_SCRIPT,p)end
 local function city(pid,id)return Players[pid] and Players[pid]:GetCities():FindID(id)end
 local function localCity(c)return c and c:GetOwner()==Game.GetLocalPlayer() and P.IsTestPlayer(c:GetOwner())end
 ExposedMembers.SPC_ExpeditionQueueRead=function(pid,id)
  local c=assert(city(pid,id),'TRAINING_CITY_UNREADABLE');assert(c:GetOwner()==pid)
  local q=c:GetBuildQueue();local n=q:GetSize();assert(type(n)=='number' and n>=0 and n<=100,'TRAINING_QUEUE_SIZE_UNKNOWN')
  local count=0
  for i=0,n-1 do
   local e=assert(q:GetAt(i),'TRAINING_QUEUE_ENTRY_UNKNOWN')
   if e.Directive==CityProductionDirectives.TRAIN then
    local r=assert(GameInfo.Units[e.UnitType],'TRAINING_QUEUE_TYPE_UNKNOWN')
    if r.UnitType==M.KIND then count=count+1 end
   end
  end
  return {owner=pid,city=id,turn=Game.GetCurrentGameTurn(),count=count}
 end
 function api.Sync(c)
  if not localCity(c)then return end
  local revision=tostring(ExposedMembers.SPC_RuntimeUIRevision)..':'..Game.GetCurrentGameTurn()..':'..tostring((ExposedMembers.SPC_ExpeditionActivity or {}).revision)
  if selected~=c:GetID() or lastRevision~=revision then
   selected=c:GetID();view=nil;sync=nil;lastRevision=revision
  end
  if sync or pending then return end
  local token,packet=request('SYNC',c);sync={token=token,owner=c:GetOwner(),city=c:GetID()}
  transmit(c:GetOwner(),packet)
 end
 function api.Items(data)
  local c=data.City;if not localCity(c)then return end
  api.Sync(c)
  local items={};for _,v in ipairs(data.UnitItems or {})do if v.Type~=M.KIND then items[#items+1]=v end end
  data.UnitItems=items
  if not view or view.city~=c:GetID() or not view.eligible then return end
  local r=GameInfo.Units[M.KIND];if not r then return end
  local q=c:GetBuildQueue()
  items[#items+1]={Index=r.Index,Type=r.UnitType,Name=r.Name,Hash=r.Hash,Kind='KIND_UNIT',
   ToolTip=Locale.Lookup('LOC_SPC_EXPEDITION_TRAINING_HELP')..(ExposedMembers.SPC_ExpeditionTrainingUIError and ('[NEWLINE]'..Locale.Lookup('LOC_SPC_EXPEDITION_SPY_TRAINING_ERROR',ExposedMembers.SPC_ExpeditionTrainingUIError)) or ''),TurnsLeft=q:GetTurnsLeft(r.Hash),
   Disabled=pending~=nil,Civilian=true,Cost=q:GetUnitCost(r.Index),Progress=q:GetUnitProgress(r.Index),
   Corps=false,Army=false,CorpsCost=0,ArmyCost=0,CorpsTurnsLeft=1,ArmyTurnsLeft=1,
   CorpsTooltip="",ArmyTooltip="",CorpsName="",ArmyName="",ReligiousStrength=r.ReligiousStrength or 0,
   IsCurrentProduction=q:GetCurrentProductionTypeHash()==r.Hash,SortIndex=999}
 end
 function api.Before(c,item,queueSelected)
  if not item or item.Type~=M.KIND then return true end
  if not localCity(c) or pending or queueSelected then return false end
  local token,packet=request('RESERVE',c)
  pending={owner=c:GetOwner(),city=c:GetID(),token=token,item=item,stage='RESERVE',turn=Game.GetCurrentGameTurn(),attempts=0}
  transmit(c:GetOwner(),packet);return false
 end
 function api.CancelQueue(c,index)
  if not localCity(c)then return end
  local e=c:GetBuildQueue():GetAt(index);local r=e and e.Directive==CityProductionDirectives.TRAIN and GameInfo.Units[e.UnitType]
  local v=ExposedMembers.SPC_ExpeditionActivity
  if r and r.UnitType==M.KIND and v and v.phase=='TRAINING' and v.trainingToken then
   pending={owner=c:GetOwner(),city=c:GetID(),reservation=v.trainingToken,stage='CANCEL',attempts=0}
  end
 end
 local function clear(p,err)
  pending=nil;sync=nil;view=nil
  ExposedMembers.SPC_ExpeditionTrainingUIError=err
  notify(p.owner,p.city)
 end
 function api.Pulse()
  local reply=ExposedMembers.SPC_ExpeditionTrainingReply
  if sync and reply and reply.token==sync.token then
   local s=sync;view=reply
   -- Set before notify: Refresh can re-enter Sync.
   sync={token='CONSUMED',owner=s.owner,city=s.city};notify(s.owner,s.city)
  end
  local p=pending;if not p then return end
  p.age=(p.age or 0)+1
  if p.age>12 then clear(p,'TRAINING_HANDSHAKE_UNCONFIRMED');return end
  local c=city(p.owner,p.city)
  if not localCity(c)then clear(p,'TRAINING_CITY_CHANGED');return end
  if p.stage=='RESERVE' and reply and reply.token==p.token then
   if reply.error then clear(p,reply.error);return end
   if not reply.reserved then clear(p,'TRAINING_RESERVATION_UNCONFIRMED');return end
   p.reservation=reply.reservation
   local chosen=UI.GetHeadSelectedCity()
   if not chosen or chosen:GetID()~=p.city or chosen:GetOwner()~=p.owner or CheckQueueItemSelected() then p.stage='CANCEL'
   else
    local row=GameInfo.Units[M.KIND]
    if not c:GetBuildQueue():CanProduce({UnitType=row.Hash},false,true)then p.stage='CANCEL';p.cancelReason=Locale.Lookup('LOC_SPC_EXPEDITION_TRAINING_NATIVE_DENIED')
    else
     p.stage='QUEUE';p.issued=true -- before native callback; never resend BUILD
     local ok,err=pcall(build,c,p.item)
     if not ok then clear(p,tostring(err));return end
    end
   end
  end
  if p.stage=='QUEUE' or p.stage=='CANCEL' then
   local ok,q=pcall(ExposedMembers.SPC_ExpeditionQueueRead,p.owner,p.city)
   if not ok then clear(p,tostring(q));return end
   if p.stage=='QUEUE' and q.count==1 or p.stage=='CANCEL' and q.count==0 then
    local token,packet=request(p.stage=='QUEUE' and 'CONFIRM' or 'CANCEL',c,p.reservation)
    p.token=token;p.stage='ACK';transmit(p.owner,packet)
   else
    p.attempts=p.attempts+1
    if p.attempts>=12 then clear(p,'TRAINING_NATIVE_QUEUE_UNCONFIRMED');return end
   end
  elseif p.stage=='ACK' and reply and reply.token==p.token then
   clear(p,reply.error or p.cancelReason)
  end
 end
 return api
end
