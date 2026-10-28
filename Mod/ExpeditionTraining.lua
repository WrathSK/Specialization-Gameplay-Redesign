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
 local function syncInputs(pid,id,c)
  local store=shared.CityProgressionStore;local gate=shared.ExpeditionGate;local facts=shared.EffectiveFacts
  local read=store and store.TrainingInputStamp;local capacity=T.CapacityInputStamp
  if shared.ExpeditionTraining~=d or not gate or gate.Training~=T or type(read)~='function'or type(capacity)~='function'or not c then return nil end
  local a={store=store,gate=gate,facts=facts,read=read,capacity=capacity,owner=pid,cityID=c:GetID(),x=c:GetX(),y=c:GetY(),turn=Game.GetCurrentGameTurn()}
  if a.cityID~=id or not(integer(a.cityID)and integer(a.x)and integer(a.y)and integer(a.turn))then return nil end
  a.before,a.core=read(pid,id,a.x,a.y);a.capacityInput=capacity(pid);a.factsRead=facts and facts.Read;a.available=T.Available;a.gateRead=T.Read
  if type(a.before)~='string'or type(a.core)~='string'or type(a.capacityInput)~='string'then return nil end
  return a
 end
 local function sameInputs(a)
  return a and shared.ExpeditionTraining==d and shared.CityProgressionStore==a.store and a.store.TrainingInputStamp==a.read
   and shared.EffectiveFacts==a.facts and a.facts and a.facts.Read==a.factsRead and shared.ExpeditionGate==a.gate
   and a.gate.Training==T and T.CapacityInputStamp==a.capacity and T.Available==a.available and T.Read==a.gateRead
 end
 local function coveredInputs(a)
  if not a or not a.after then return nil end
  local turn=Game.GetCurrentGameTurn() -- last native boundary, followed only by pure source/input checks
  if not sameInputs(a)then return nil end
  local capacity=a.capacity(a.owner);local post,core=a.read(a.owner,a.cityID,a.x,a.y)
  if not sameInputs(a)or type(post)~='string'or type(core)~='string'or core~=a.core or post~=a.after
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
  if not ok then if protect==nil or protect()then v=failure(pid,v)else v=tostring(v):gsub('^.-:%d+: ',''):sub(1,160)end;print('[SPC][B202][TRAINING] '..v)end
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
    if sameInputs(inputObservation)then
     local good,stamp,core=pcall(inputObservation.read,pid,p.CityID,inputObservation.x,inputObservation.y)
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
    mutation=true;local n=queue(exact(s));assert(n<=1,'TRAINING_MULTIPLE_QUEUE_ENTRIES')
    if p.Action=='CANCEL' then
     assert(n==0,'TRAINING_QUEUE_STILL_PRESENT');marker(exact(s),false);T.Cancel(pid,s.trainingToken)
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
 function d.Birth(pid,id)
  if not P.IsTestPlayer(pid)then return end
  if T.MarkUnitCapacity then
   local ok=pcall(T.MarkUnitCapacity,pid)
   if T.CapacityObservationFailed then pcall(T.CapacityObservationFailed,not ok)end
  end
  local u=Players[pid]:GetUnits():FindID(id);local r=u and P.Info('Units',u:GetType())
  if not r or r.UnitType~=M.KIND then return end
  run(pid,function()
   local s=T.Read(pid)
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
  if not P.IsTestPlayer(pid) or kind~=0 then return end
  local r=P.Info('Units',index);if not r or r.UnitType~=M.KIND then return end
  run(pid,function()
   popFlush('POP_SUMMARY',pid);observeAt('COMPLETE_CALLBACK',pid,id,nil,{eventOwner=pid,eventCity=id,eventKind=kind,eventIndex=index,cancelled=cancelled})
   local s=T.Read(pid)
   observeAt('COMPLETE_STATE',pid,id,s)
   if s.phase~='TRAINING' then return end
   assert(s.sourceCity==id and not cancelled and (s.trainingQueued or s.trainingTurn==Game.GetCurrentGameTurn()),'TRAINING_COMPLETION_MISMATCH')
   -- B209: the marker exists only in the reserved city after the saved
   -- reservation, so a same-turn native completion there is the queue evidence.
   if not s.trainingQueued then T.Evidence(pid,s.trainingToken,'trainingQueued',true)end
   T.Evidence(pid,s.trainingToken,'trainingCompleted',true);dirty=true
   observeAt('COMPLETE_EXIT',pid,id,s,{completed=true})
  end)
 end
 function d.Pulse(pid,recovery)
  if not P.IsTestPlayer(pid)then return end
  local s=T.Read(pid)
  if s.phase=='HELD' and s.trainingToken then pcall(function()marker(exact(s),false)end);return end
  if s.phase~='TRAINING' then return end
  if type(ExposedMembers.SPC_ExpeditionQueueRead)~='function' then waitingReader=pid;return end
  if waitingReader then waitingReader=nil;readerAttempts=0;recovery=true end
  run(pid,function()
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
    if T.NoUnits(pid) then marker(c,false);T.Cancel(pid,s.trainingToken)
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
 local function current(recovery)
  for pid in pairs(Players)do if P.IsTestPlayer(pid)then d.Pulse(pid,recovery);break end end
 end
 hook('GameCoreEventPublishComplete',function()
  if waitingReader then
   if type(ExposedMembers.SPC_ExpeditionQueueRead)=='function' then d.Pulse(waitingReader,true)
   else
    readerAttempts=readerAttempts+1
    if readerAttempts>=12 then local pid=waitingReader;waitingReader=nil;run(pid,function()error('TRAINING_QUEUE_READER_UNAVAILABLE')end)end
   end
  elseif dirty then dirty=false;current(false)end
 end)
 hook('PlayerTurnActivated',function(pid)turnMark('TURN_BEGIN',pid);d.Pulse(pid,false)end)
 hook('LoadScreenClose',function()
  if diag then pcall(diag.Load)end
  current(true)
  if diag then pcall(diag.Record,'LOAD_RECOVERY_RETURNED')end
 end)
 hook('CityTransfered',function()current(false)end)
 if shared.CityProgressionStore then shared.CityProgressionStore.RegisterExit('ExpeditionTraining',function(c,loss)
  local pid=loss.origin.owner;local s=T.Read(pid)
  if s.phase=='TRAINING' and s.sourceCity==loss.origin.cityID then
   run(pid,function()shared.CityProgressionStore.RemoveOwned(c,loss,{M.MARKER});error('TRAINING_SOURCE_LOST')end)
  end
 end)end
end
