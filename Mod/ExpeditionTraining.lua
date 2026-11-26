-- B394 optional observer: deleting/disabling its module leaves this tap inert.
pcall(include,'CultureDiagnostics')
local function cultureObserve(point,build)
 pcall(function()
  local d=SPCCultureDiagnostics
  if d and d.ENABLED then d.Emit('CULTURE_GP',point,build)end
 end)
end
if not SPCIdentityEqual then include('IdentityEqual')end
local sameIdentity=SPCIdentityEqual.Same
-- B202: one saved queue reservation; native queue/completion/birth are evidence,
-- never an instruction to create a unit. No periodic all-city collection.
if include then include('ExpeditionTrainingDiagnostics')end
SPCExpeditionTraining={KIND='UNIT_SPC_EXPEDITION_SPY',MARKER='BUILDING_SPC_EXPEDITION_TRAINING_ACCESS'}
function SPCExpeditionTraining.Start(P,shared)
 local M=SPCExpeditionTraining;local T=assert(shared.ExpeditionGate.Training)
 local d={};shared.ExpeditionTraining=d
 local diag=SPCExpeditionTrainingDiagnostics and SPCExpeditionTrainingDiagnostics.New(P,'GAMEPLAY')
 local function observe(stage,c,s,extra)if diag then pcall(diag.Event,stage,c,s,extra)end end
 local busy=false;local dirty=false;local waitingReader;local readerAttempts=0;local lastToken,lastReply,latestRequest
 local lastLossSample
 -- Only the active transaction watches its own source across native calls.
 local watchedOwner,watchedCity,watchedToken,positiveReceipt
 local conflict='TRAINING_SOURCE_RECEIPT_CONFLICT'
 local function missingTrainingSource(s)
  return s.phase=='HELD' and s.stop=='TRAINING_SOURCE_CHANGED' and s.trainingToken~=nil and not s.unitID and not s.teamKey
 end
 local function watchOrder(s)watchedOwner,watchedCity,watchedToken,positiveReceipt=s.owner,s.sourceCity,s.trainingToken,false end
 local function noNewReceipt()return watchedOwner~=nil and not positiveReceipt end
 local function city(pid,id)return Players[pid] and Players[pid]:GetCities():FindID(id)end
 local function observeAt(stage,pid,id,s,extra)
  if diag then pcall(function()observe(stage,id~=nil and city(pid,id) or nil,s,extra)end)end
 end
 -- B206 diagnostic only: aggregate source-city population notifications while
 -- TRAINING. Emits the 1st, 2nd, 4th, 8th... notification per source and turn,
 -- plus unreported totals at lifecycle/turn boundaries. Never mutates state.
 local pops={}
 local function popReport(stage,pid,a)
  a.reported=a.events
  observeAt(stage,pid,a.city,T.Read(pid),{popSource=a.source,popEvents=a.events,popDelta=a.delta,popTo=a.to,popSum=a.sum,popMin=a.min,popMax=a.max,popTurn=a.turn})
 end
 local function popFlush(stage,pid)
  if not diag then return end
  pcall(function()for _,a in pairs(pops)do if a.pid==pid and a.events>a.reported then popReport(stage,pid,a)end end end)
 end
 local function exact(s)
  local c=city(s.owner,s.sourceCity)
  assert(c and c:GetOwner()==s.owner and SPCNetworkInput.Reference(c)==s.sourceRef,'TRAINING_SOURCE_CHANGED')
  return c
 end
 local function marker(c,wanted)
  local row=assert(P.Info('Buildings',M.MARKER),'TRAINING_MARKER_MISSING');local b=c:GetBuildings()
  local has=P.HasBuilding(b,row.Index);assert(type(has)=='boolean','TRAINING_MARKER_UNKNOWN')
  if has~=wanted then
   observe('MARKER_BEFORE',c,nil,{wanted=wanted})
   if wanted then P.CreateBuilding(c:GetBuildQueue(),row.Index)else P.RemoveBuilding(b,row.Index)end
   observe('MARKER_AFTER',c,nil,{wanted=wanted})
   assert(P.HasBuilding(b,row.Index)==wanted,'TRAINING_MARKER_UNCONFIRMED')
  end
 end
 local function queue(c)
  local read=assert(ExposedMembers.SPC_ExpeditionQueueRead,'TRAINING_QUEUE_READER_UNAVAILABLE')
  -- GetAt is a UI surface. Read a fresh exact-city sample, not a cached count.
  local v=read(c:GetOwner(),c:GetID())
  if type(v)=='table'then observe('QUEUE_SAMPLE',c,nil,{reader=v._b205_context,readerLoad=v._b205_load,count=v.count})end
  assert(type(v)=='table' and v.owner==c:GetOwner() and v.city==c:GetID() and v.turn==Game.GetCurrentGameTurn() and
   type(v.count)=='number' and v.count>=0 and v.count%1==0,'TRAINING_QUEUE_UNKNOWN')
  return v.count
 end
 -- Passive observation only; never substitutes for the original final getter.
 local function finalBinding(c,f)
  local store=shared.CityProgressionStore;local ticket
  local begin=store and store.BeginTrainingBindingObservation;local finish=store and store.FinishTrainingBindingObservation
  local live=shared.ExpeditionTraining==d
  if live and type(begin)=='function'and type(finish)=='function'then
   local ok,value=pcall(begin,f.owner,f.cityID,f.x,f.y,f.token);if ok then ticket=value end
  end
  local ok,value=pcall(c.GetProperty,c,'SPC_DEV_BINDING_B013_TOKEN') -- original single native read
  if ticket and shared.ExpeditionTraining==d and shared.CityProgressionStore==store
   and store.BeginTrainingBindingObservation==begin and store.FinishTrainingBindingObservation==finish then
   local good=pcall(finish,f.owner,f.cityID,f.x,f.y,ticket,ok,value)
   d.bindingObservationError=not good and 'TRAINING_BINDING_OBSERVATION_FAILED'or nil
  end
  if not ok then error(value,0)end
  return value
 end
 local function integer(v)return type(v)=='number'and v==v and v>=0 and v<1000000000 and v%1==0 end
 -- Same-turn input stamps only. Module tables and methods are not swapped at
 -- runtime, so there is no identity re-check between reads (CA-D14, B549).
 local function syncInputs(pid,id,c)
  if not c then return nil end
  local a={owner=pid,cityID=c:GetID(),x=c:GetX(),y=c:GetY(),turn=Game.GetCurrentGameTurn()}
  if a.cityID~=id or not(integer(a.cityID)and integer(a.x)and integer(a.y)and integer(a.turn))then return nil end
  a.before,a.core=shared.CityProgressionStore.TrainingInputStamp(pid,id,a.x,a.y);a.capacityInput=T.CapacityInputStamp(pid)
  if type(a.before)~='string'or type(a.core)~='string'or type(a.capacityInput)~='string'then return nil end
  return a
 end
 local function coveredInputs(a)
  if not a or not a.after then return nil end
  local turn=Game.GetCurrentGameTurn() -- last native boundary, followed only by pure source/input checks
  local capacity=T.CapacityInputStamp(a.owner);local post,core=shared.CityProgressionStore.TrainingInputStamp(a.owner,a.cityID,a.x,a.y)
  if type(post)~='string'or type(core)~='string'or core~=a.core or post~=a.after
   or capacity~=a.capacityInput or turn~=a.turn then return nil end
  return {version=1,owner=a.owner,cityID=a.cityID,x=a.x,y=a.y,turn=a.turn,storeInput=post,capacityInput=a.capacityInput}
 end
 local function eligible(pid,c,observation)
  assert(c and c:GetOwner()==pid,'OWN_CITY_REQUIRED')
  local f=shared.EffectiveFacts.Read(pid,c)
  if observation then
   observation.specialization=f.specialization;observation.potential=f.potential
   observation.active=f.active;observation.activeStatus=f.activeStatus
  end
  assert(f.specialization=='CULTURE' and f.active==4 and not f.investmentPending,'CULTURE_ACTIVE_IV_REQUIRED')
  assert(f.token and finalBinding(c,f)==f.token,'SOURCE_REFERENCE_UNKNOWN')
 end
 local function failure(pid,err)
  local s=T.Read(pid)
  if s.trainingToken and (s.phase=='TRAINING' or s.phase=='NAMING') then
   -- Withdraw only our marker, even after transfer, if the physical reference
   -- is still provable. A missing endpoint never frees the saved capacity.
   pcall(function()marker(exact(s),false)end)
   T.Hold(err)
  end
  return tostring(err):gsub('^.-:%d+: ',''):sub(1,160)
 end
 local function run(pid,fn,protect)
  if busy or not P.IsTestPlayer(pid)then return end
  busy=true;shared.RequestDepth=(shared.RequestDepth or 0)+1
  local ok,v=pcall(fn)
  if positiveReceipt then
   local s=T.Read(pid)
   if not s.blocked and s.trainingToken==watchedToken and (s.phase=='TRAINING' or missingTrainingSource(s))
    and not s.trainingBorn and not s.trainingCompleted then
    T.Hold(conflict);ok=false;v=conflict
   end
  end
  if not ok then if protect==nil or protect()then v=failure(pid,v)else v=tostring(v):gsub('^.-:%d+: ',''):sub(1,160)end;print('[SPC][B202][TRAINING] '..v)end
  watchedOwner,watchedCity,watchedToken,positiveReceipt=nil,nil,nil,nil
  shared.RequestDepth=shared.RequestDepth-1;busy=false
  return ok,v
 end
 function d.Request(pid,p)
  if not P.IsTestPlayer(pid) or type(p)~='table' or type(p.Token)~='string' or #p.Token==0 or #p.Token>100 then return end
  if p.Token==lastToken then ExposedMembers.SPC_ExpeditionTrainingReply=lastReply;return end
  if busy then return end
  local attempt={};latestRequest=attempt
  local mutation=false;local inputObservation
  local ok,value=run(pid,function()
   local s=T.Read(pid);local c=city(pid,p.CityID)
   if p.Action=='SYNC' then
    local sample={owner=pid,city=p.CityID,requestKey=p.Token}
    local sampled,a=pcall(syncInputs,pid,p.CityID,c);if sampled then inputObservation=a end
    local valid=pcall(eligible,pid,c,sample)
    if inputObservation then
     local good,stamp,core=pcall(shared.CityProgressionStore.TrainingInputStamp,pid,p.CityID,inputObservation.x,inputObservation.y)
     if good and core==inputObservation.core then inputObservation.after=stamp end
    end
    local allowed=valid and T.Available(pid)
    sample.eligibility=allowed;sample.reason=not valid and 'FACTS_INELIGIBLE' or not allowed and 'CAPACITY_UNAVAILABLE' or 'AVAILABLE'
    if diag then pcall(diag.Record,'TRAINING_SYNC_FACTS',sample)end
    return {eligible=allowed,phase=s.phase or 'IDLE'}
   elseif p.Action=='RESERVE' then
    observe('RESERVE_ENTRY',c,s)
    eligible(pid,c);assert(T.Available(pid),'TRAINING_CAPACITY_RESERVED')
    assert(queue(c)==0,'TRAINING_ALREADY_QUEUED')
    mutation=true;T.Reserve(pid,p.CityID,p.Token);marker(exact(T.Read(pid)),true);exact(T.Read(pid))
    observe('RESERVE_EXIT',c,nil,{reservation=p.Token})
    return {reserved=true,reservation=p.Token}
   elseif p.Action=='CONFIRM' or p.Action=='CANCEL' then
    assert(s.phase=='TRAINING' and s.trainingToken==p.Reservation and s.sourceCity==p.CityID,'TRAINING_RESERVATION_CHANGED')
    if p.Action=='CANCEL' then watchOrder(s)end
    mutation=true;local n=queue(exact(s));assert(n<=1,'TRAINING_MULTIPLE_QUEUE_ENTRIES')
    if p.Action=='CANCEL' then
     assert(n==0,'TRAINING_QUEUE_STILL_PRESENT');marker(exact(s),false);T.Cancel(pid,s.trainingToken,noNewReceipt)
    elseif n==1 then T.Evidence(pid,s.trainingToken,'trainingQueued',true)
    else return {waiting=true}end
    return {confirmed=true}
   end
   error('TRAINING_ACTION_INVALID')
  end,function()return mutation end)
  -- A rejected competing RESERVE must not hold someone else's valid queue.
  local v=ok and value or {error=value};v.token=p.Token;v.owner=pid;v.city=p.CityID
  if p.Action=='SYNC'then local good,input=pcall(coveredInputs,inputObservation);if good then v.input=input end end
  if not sameIdentity(latestRequest,attempt)then return end -- a newer accepted request owns publication
  lastToken=p.Token;lastReply=v;ExposedMembers.SPC_ExpeditionTrainingReply=v
 end
 -- A late positive receipt vetoes release. A team appearing after handover
 -- cannot be attributed to this order by position or unit type alone.
 local function lossReceipt(pid,sourceID)
  if watchedOwner==pid and (sourceID==nil or sourceID==watchedCity)then
   positiveReceipt=true
  end
  local s=T.Read(pid)
  if (missingTrainingSource(s) or s.phase=='HELD' and s.stop==T.TransferredOrder)
   and (sourceID==nil or s.sourceCity==sourceID)then
   T.Hold(conflict)
   return true
  end
 end
 function d.Birth(pid,id)
  if not P.IsTestPlayer(pid)then return end
  if T.MarkUnitCapacity then
   local ok=pcall(T.MarkUnitCapacity,pid)
   if T.CapacityObservationFailed then pcall(T.CapacityObservationFailed,not ok)end
  end
  local u=Players[pid]:GetUnits():FindID(id);local r=u and P.Info('Units',u:GetType())
  if r and (r.UnitType==M.KIND or r.UnitType=='UNIT_SPY')then cultureObserve('UNIT_ADDED_OBSERVED',function()return {eventOwner=pid,eventUnit=id,unitType=r.UnitType,unitIndex=r.Index}end)end
  if r and r.UnitType=='UNIT_SPY' and lastLossSample then dirty=true end
  if not r or r.UnitType~=M.KIND then return end
  if lossReceipt(pid,nil)then return end
  run(pid,function()
   local s=T.Read(pid)
   cultureObserve('EXPEDITION_BIRTH_STATE',function()return {owner=pid,eventUnit=id,phase=s.phase,reservation=s.trainingToken,ready=s.phase=='TRAINING'}end)
   if s.phase~='TRAINING' then return end
   popFlush('POP_SUMMARY',pid);observeAt('BIRTH_ENTRY',pid,s.sourceCity,s,{eventOwner=pid,eventUnit=id})
   -- B209: an order completed immediately (carried overflow) in the reservation
   -- turn is born before the UI can confirm the queue; matching completion
   -- evidence must still follow. Any later unconfirmed birth stays held.
   assert(s.trainingQueued or s.trainingTurn==Game.GetCurrentGameTurn(),'TRAINING_BIRTH_BEFORE_QUEUE_CONFIRMATION')
   T.Evidence(pid,s.trainingToken,'trainingBorn',id);dirty=true
   observeAt('BIRTH_EXIT',pid,s.sourceCity,s,{eventOwner=pid,eventUnit=id,born=id})
  end)
 end
 function d.Complete(pid,id,kind,index,cancelled)
  if not P.IsTestPlayer(pid)then return end
  cultureObserve('DIPLOMATIC_BUILDING_COMPLETED',function()
   if kind~=1 then return end
   local r=GameInfo.Buildings[index]
   if r and (r.BuildingType=='BUILDING_CONSULATE'or r.BuildingType=='BUILDING_CHANCERY')then return {owner=pid,city=id,eventKind=kind,eventIndex=index,recordType=r.BuildingType,requestAccepted=not cancelled}end
  end)
  if kind~=0 then return end
  local r=P.Info('Units',index);if not r or r.UnitType~=M.KIND then return end
  if cancelled~=true and lossReceipt(pid,id)then return end
  run(pid,function()
   popFlush('POP_SUMMARY',pid);observeAt('COMPLETE_CALLBACK',pid,id,nil,{eventOwner=pid,eventCity=id,eventKind=kind,eventIndex=index,cancelled=cancelled})
   local s=T.Read(pid)
   observeAt('COMPLETE_STATE',pid,id,s)
   if s.phase~='TRAINING' then return end
   -- A cancellation can precede the native queue update. Until removal is
   -- visible, the existing queue reconciliation or verified transfer owns it.
   if cancelled==true and s.sourceCity~=id then return end
   if cancelled==true and s.sourceCity==id and s.trainingQueued and not s.trainingBorn and not s.trainingCompleted then
    watchOrder(s)
    local c=exact(s)
    if queue(c)==0 then
     marker(c,false)
     assert(queue(exact(s))==0,'TRAINING_QUEUE_STILL_PRESENT')
     T.Cancel(pid,s.trainingToken,noNewReceipt)
    else dirty=true end
    return
   end
   assert(s.sourceCity==id and not cancelled and (s.trainingQueued or s.trainingTurn==Game.GetCurrentGameTurn()),'TRAINING_COMPLETION_MISMATCH')
   -- B209: the marker exists only in the reserved city after the saved
   -- reservation, so a same-turn native completion there is the queue evidence.
   if not s.trainingQueued then T.Evidence(pid,s.trainingToken,'trainingQueued',true)end
   T.Evidence(pid,s.trainingToken,'trainingCompleted',true);dirty=true
   observeAt('COMPLETE_EXIT',pid,id,s,{completed=true})
  end)
 end
 function d.Pulse(pid,recovery,published)
  if not P.IsTestPlayer(pid)then return end
  local s=T.Read(pid)
  if s.phase=='HELD' and s.stop==T.TransferredOrder then
   local read=ExposedMembers.SPC_ExpeditionOffMapCount
   local stamp=T.CapacityInputStamp(pid)
   if lastLossSample and lastLossSample.token==s.trainingToken and lastLossSample.reader==read
    and lastLossSample.stamp==stamp and not recovery then return end
   if not published and not recovery then dirty=true;return end
   lastLossSample={token=s.trainingToken,reader=read,stamp=stamp}
   local ok,ended=pcall(T.ReleaseTransferredOrder,pid,s.trainingToken,read)
   if not ok then print('[SPC][EXPEDITION_TRAINING] '..tostring(ended))end
   if ok and ended then lastLossSample=nil end
   return
  end
  lastLossSample=nil
  if s.phase=='HELD' and s.trainingToken then pcall(function()marker(exact(s),false)end);return end
  if s.phase~='TRAINING' then return end
  if type(ExposedMembers.SPC_ExpeditionQueueRead)~='function' then waitingReader=pid;return end
  if waitingReader then waitingReader=nil;readerAttempts=0;recovery=true end
  run(pid,function()
   if s.trainingQueued and not s.trainingBorn and not s.trainingCompleted then watchOrder(s)end
   local c=exact(s);local n=queue(c);assert(n<=1,'TRAINING_MULTIPLE_QUEUE_ENTRIES')
   if s.trainingBorn and s.trainingCompleted then
    if n==0 then
     observe('FINISH_ENTRY',c,s);marker(c,false);T.Finish(pid,s.trainingToken)
     observe('FINISH_EXIT',c,nil)
    elseif recovery or Game.GetCurrentGameTurn()>(s.trainingReceiptTurn or s.trainingTurn)then error('TRAINING_QUEUE_REMAINS_AFTER_COMPLETION')else dirty=true end
   elseif s.trainingBorn or s.trainingCompleted then
    -- Do not guess the missing half or release capacity at a publish boundary.
    if recovery or Game.GetCurrentGameTurn()>(s.trainingReceiptTurn or s.trainingTurn) then error('TRAINING_RECEIPT_INCOMPLETE')end
   elseif n==1 then
    if not s.trainingQueued then T.Evidence(pid,s.trainingToken,'trainingQueued',true)end
    marker(c,true)
   elseif s.trainingQueued then
    -- B210 (user-approved): an empty queue alone is not cancellation, but an
    -- empty queue with no birth/completion receipt and no Expedition unit on
    -- the map means the order was removed or replaced natively (including map
    -- placement paths that bypass the panel hook). A completed order would
    -- already have its unit, so late events cannot be mistaken for removal.
    if T.NoUnits(pid) then marker(c,false);T.Cancel(pid,s.trainingToken,noNewReceipt)
    elseif recovery then error('TRAINING_LOADED_QUEUE_MISSING')
    else marker(c,false)end
   elseif Game.GetCurrentGameTurn()>s.trainingTurn then
    error('TRAINING_ORDER_OUTCOME_UNKNOWN')
   end
  end)
 end
 local function hook(name,fn)if Events[name]then Events[name].Add(fn)end end
 local function popWatch(source,pid,id,delta,to)
  if not diag or not P.IsTestPlayer(pid)then return end
  pcall(function()
   local s=T.Read(pid);if s.phase~='TRAINING' or s.sourceCity~=id then return end
   local turn=Game.GetCurrentGameTurn();local a=pops[source]
   if not a or a.turn~=turn or a.city~=id or a.pid~=pid then a={source=source,pid=pid,city=id,turn=turn,events=0,reported=0,sum=0};pops[source]=a end
   a.events=a.events+1;a.delta=delta;a.to=to
   if type(delta)=='number'then a.sum=a.sum+delta;a.min=math.min(a.min or delta,delta);a.max=math.max(a.max or delta,delta)end
   local n=a.events;while n>1 and n%2==0 do n=n/2 end
   if n==1 then popReport('POP_CHANGE',pid,a)end
  end)
 end
 if GameEvents.OnCityPopulationChanged then GameEvents.OnCityPopulationChanged.Add(function(pid,id,delta)popWatch('GAME',pid,id,delta,nil)end)end
 if Events.CityPopulationChanged then Events.CityPopulationChanged.Add(function(pid,id,to)popWatch('EVENT',pid,id,nil,to)end)end
 local function turnMark(stage,pid)
  if not diag or not P.IsTestPlayer(pid)then return end
  popFlush('POP_SUMMARY',pid)
  pcall(function()local s=T.Read(pid);if s.phase=='TRAINING' then observeAt(stage,pid,s.sourceCity,s)end end)
 end
 if Events.PlayerTurnDeactivated then Events.PlayerTurnDeactivated.Add(function(pid)turnMark('TURN_END',pid)end)end
 GameEvents.SPC_ExpeditionTrainingRequest.Add(d.Request)
 hook('UnitAddedToMap',d.Birth);hook('CityProductionCompleted',d.Complete)
 local function affected(pid,id)
  if P.IsTestPlayer(pid)then local s=T.Read(pid);if s.phase=='TRAINING' and s.sourceCity==id then dirty=true end end
 end
 hook('CityProductionChanged',affected);hook('CityProductionQueueChanged',affected)
 local function current(recovery,published)
  for pid in pairs(Players)do if P.IsTestPlayer(pid)then d.Pulse(pid,recovery,published);break end end
 end
 hook('GameCoreEventPublishComplete',function()
  if waitingReader then
   if type(ExposedMembers.SPC_ExpeditionQueueRead)=='function' then d.Pulse(waitingReader,true)
   else
    readerAttempts=readerAttempts+1
    if readerAttempts>=12 then local pid=waitingReader;waitingReader=nil;run(pid,function()error('TRAINING_QUEUE_READER_UNAVAILABLE')end)end
   end
  elseif dirty then dirty=false;current(false,true)end
 end)
 hook('PlayerTurnActivated',function(pid)turnMark('TURN_BEGIN',pid);d.Pulse(pid,false)end)
 hook('LoadScreenClose',function()
  if diag then pcall(diag.Load)end
  current(true)
  if diag then pcall(diag.Record,'LOAD_RECOVERY_RETURNED')end
 end)
 hook('CityTransfered',function()current(false)end)
 shared.CityProgressionStore.RegisterExit('ExpeditionTraining',function(c,loss,ticket)
  local pid=loss.origin.owner
  local ok,value=run(pid,function()
   local s=T.Read(pid);assert(not s.blocked,'TRAINING_STATE_UNAVAILABLE')
   local wasTraining=s.phase=='TRAINING' or missingTrainingSource(s)
   local matched=wasTraining and s.sourceCity==loss.origin.cityID
   if matched then watchOrder(s)end
   -- Physical ownership is independent of the current reservation/profession.
   local store=shared.CityProgressionStore
   store.RemoveOwned(c,loss,{M.MARKER})
   if matched then
    assert(s.owner==pid and s.x==loss.origin.x and s.y==loss.origin.y,'TRAINING_SOURCE_CHANGED')
    local reason='TRAINING_SOURCE_LOST'
    if ticket and s.trainingQueued and not s.trainingBorn and not s.trainingCompleted and not s.trainingReceiptTurn
     and not s.unitID and not s.createdID and not s.teamKey then
     local token=assert(store.ReferenceToken(c),'TRAINING_SOURCE_BINDING_UNKNOWN')
     assert(SPCNetworkInput.ReferenceParts(pid,s.sourceCity,s.x,s.y,token)==s.sourceRef,'TRAINING_SOURCE_BINDING_CHANGED')
     assert(store.IsExitCurrent('ExpeditionTraining',c,loss,ticket),'TRAINING_EXIT_CHANGED')
     reason=positiveReceipt and conflict or T.TransferredOrder
    end
    local current=T.Read(pid) -- Native reads/removal may have run another callback.
    assert(not current.blocked and current.phase==s.phase and current.stop==s.stop and current.owner==s.owner
     and current.trainingBorn==s.trainingBorn and current.trainingCompleted==s.trainingCompleted
     and current.sourceCity==s.sourceCity and current.x==s.x and current.y==s.y
     and current.trainingToken==s.trainingToken and current.sourceRef==s.sourceRef,'TRAINING_EXIT_CHANGED')
    if reason==T.TransferredOrder then T.MarkTransferredOrder(pid,s.trainingToken)else T.Hold(reason)end
    local after=T.Read(pid)
    assert(not after.blocked and after.phase=='HELD'and after.stop==reason and after.owner==pid
     and after.sourceCity==s.sourceCity and after.x==s.x and after.y==s.y
     and after.trainingToken==s.trainingToken and after.sourceRef==s.sourceRef,'TRAINING_EXIT_UNCONFIRMED')
    if reason==T.TransferredOrder then dirty=true end
   elseif ticket and s.unitID and s.teamKey and s.owner==pid and s.sourceCity then
    -- The original owner's city ID may differ after a verified return. The saved
    -- endpoint, plot and Store token together identify the archive, even from abroad.
    local token=assert(store.ReferenceToken(c),'ARCHIVE_BINDING_UNKNOWN')
    local ref=SPCNetworkInput.ReferenceParts(pid,s.sourceCity,loss.origin.x,loss.origin.y,token)
    if ref==s.sourceRef then
     assert(store.IsExitCurrent('ExpeditionTraining',c,loss,ticket),'ARCHIVE_EXIT_CHANGED')
     T.LoseArchive(pid,ref,s.teamKey)
    end
   end
   return true
  end,function()return false end) -- an unrelated saved team is never held by this cleanup's failure
  return ok==true and value==true
 end)
end
