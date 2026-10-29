-- B394 optional observer: deleting/disabling its module leaves this tap inert.
pcall(include,'CultureDiagnostics')
local function cultureObserve(point,build)
 pcall(function()
  local d=SPCCultureDiagnostics
  if d and d.ENABLED then d.Emit('CULTURE_PROJECT_UI',point,build)end
 end)
end
-- One explicit intent-read gate, shared by the three independent project UIs.
-- No native listeners, clock retries, save authority or project eligibility here.
SPCTimedProjectSelectionClient={}
local specs={ClaimProjects={'SPC_ClaimQueueRead','CLAIM_SYNC'},DialogueProjects={'SPC_DialogueProjectRead','DIALOGUE_PROJECT_SYNC'},EngineeringStudy={'SPC_EngineeringStudyRead','ENGINEERING_STUDY_SYNC'}}
function SPCTimedProjectSelectionClient.New(P,pending)
 local d={};local closed,draining=false,false
 local config,registration,registeredService,available;local generation,warmed=0,0;local wakePending=false
 local sent,waiting={},{};local sentGeneration,count=0,0
 local function message(v)local ok,t=pcall(tostring,v);return ok and t:sub(1,180)or 'TIMED_UI_ERROR'end
 local function shared()return ExposedMembers.SPC_P0 or {}end
 local function report(k,state,why)
  if config and config.onStatus and d.Ready()then local ok,err=pcall(config.onStatus,k,state,why);if not ok then d.error=message(err)end end
 end
 function d.Configure(kind,readerKey,action,send,onStatus)
  assert(not config and specs[kind]and specs[kind][1]==readerKey and specs[kind][2]==action and type(send)=='function','TIMED_UI_CONFIGURATION')
  assert(type(ExposedMembers[readerKey])=='function','TIMED_UI_READER')
  config={kind=kind,readerKey=readerKey,action=action,send=send,onStatus=onStatus,reader=assert(ExposedMembers[readerKey],'TIMED_UI_READER')}
 end
 function d.OwnsReader()
  local slots=ExposedMembers.SPC_TimedProjectReaderSlots
  return not closed and config and ExposedMembers[config.readerKey]==config.reader
   and (not registration or type(slots)=='table'and slots[config.kind]==registration)or false
 end
 function d.Ready()
  local service=shared().TimedProjectReaders
  return d.OwnsReader()and available and registration and service==available.service and service.readers[config.kind]==registration
   and shared()[config.kind]==available.backend and not available.backend.startupError or false
 end
 function d.Connect()
  if closed or registration then return end
  assert(config,'TIMED_UI_CONFIGURATION')
  if ExposedMembers[config.readerKey]~=config.reader then d.error='TIMED_UI_READER_REPLACED';return false end
  local serial=ExposedMembers.SPC_TimedProjectReaderSerial or 0
  assert(type(serial)=='number'and serial>=0 and serial%1==0 and serial<9007199254740991,'TIMED_UI_SERIAL')
  serial=serial+1;ExposedMembers.SPC_TimedProjectReaderSerial=serial
  local slots=ExposedMembers.SPC_TimedProjectReaderSlots
  assert(slots==nil or type(slots)=='table','TIMED_UI_SLOTS')
  slots=slots or {};ExposedMembers.SPC_TimedProjectReaderSlots=slots
  local row={serial=serial,reader=config.reader}
  row.wake=function(backend,epoch,reader)
   if closed or registration~=row or slots[config.kind]~=row or ExposedMembers[config.readerKey]~=row.reader
    or reader~=row.reader or shared()[config.kind]~=backend then return end
   local service=shared().TimedProjectReaders
   if not service or service.readers[config.kind]~=row then return end
   assert(type(epoch)=='number'and epoch>=1 and epoch%1==0,'TIMED_UI_EPOCH')
   if available and available.backend==backend and available.epoch==epoch and available.reader==reader and available.service==service then return end
   available={backend=backend,epoch=epoch,reader=reader,service=service};generation=generation+1;wakePending=true
   if config.kind=='DialogueProjects'then cultureObserve('UI_READER_WAKE',function()return {recordType=config.kind,packetEpoch=epoch,packetSeq=row.serial,ready=true}end)end
  end
  registration=row;slots[config.kind]=row
  registeredService=shared().TimedProjectReaders
  if registeredService then registeredService.Register(config.kind,row)end
  if config.kind=='DialogueProjects'then cultureObserve('UI_READER_CONNECT',function()return {recordType=config.kind,packetSeq=row.serial,ready=available~=nil,reason=registeredService and 'SERVICE_PRESENT'or 'SERVICE_MISSING'}end)end
 end
 local function resetGeneration()
  if sentGeneration~=generation then
   sent,waiting={},{};count=0;sentGeneration=generation
  end
 end
 function d.Sync(c)
  if not d.Ready()or not c then return 'WAITING_READY'end
  local captured,context=generation,available
  local pid,id=c:GetOwner(),c:GetID();if not P.IsTestPlayer(pid)then return 'INELIGIBLE'end
  if not d.Ready()or captured~=generation or context~=available then return 'WAITING_READY'end
  resetGeneration();local k=pid..':'..id;local old=sent[k]
  if old then return old.state,old.token end
  if count>=2048 then d.error='TIMED_UI_SYNC_CAPACITY';report(k,'FAILED',d.error);return 'FAILED'end
  count=count+1
  local state={backend=available.backend,token='TPS:'..registration.serial..':'..generation..':'..k,state='SENT'}
  sent[k]=state;waiting[k]=state -- one attempt, before potentially reentrant native send
  report(k,'SENT')
  if not d.Ready()or generation~=captured or sent[k]~=state then state.state='HELD_CONTEXT';return state.state,state.token end
  local ok,err=pcall(config.send,pid,PlayerOperations.EXECUTE_SCRIPT,{OnStart='SPC_P0_Request',Action=config.action,CityID=id,Token=state.token})
  if not ok then state.state='FAILED';state.error=message(err);if sent[k]==state then waiting[k]=nil;if generation==captured then report(k,'FAILED',state.error)end end end
  return state.state,state.token
 end
 function d.WarmStart()
  if not d.Ready()or warmed==generation then return end
  local pid=Game.GetLocalPlayer();local player=Players[pid]
  if not player or not P.IsTestPlayer(pid)then return end
  local captured=generation;warmed=captured -- one known-city reconciliation for this actual availability generation
  for _,c in player:GetCities():Members()do
   if generation~=captured or not d.Ready()then break end
   d.Sync(c)
  end
 end
 local function replies()
  local captured=generation
  for k,state in pairs(waiting)do
   if captured~=generation or not d.Ready()then return end
   if state.backend.syncAck and state.backend.syncAck[k]==state.token then
    waiting[k]=nil;state.state='ACK';report(k,'ACK')
   end
  end
 end
 function d.QueueEvent(pid,id)
  if config and config.kind=='DialogueProjects'then cultureObserve('UI_QUEUE_EVENT',function()
   local _,p=next(pending);if not p then return end
   return {owner=p.pid,city=p.id,eventOwner=pid,eventCity=id,taskStart=p.turn,ready=p.pid==pid and p.id==id,requestAccepted=not closed}
  end)end
  if closed or config and not d.OwnsReader()or type(pid)~='number' or type(id)~='number'then return end
  local p=pending[pid..':'..id]
  if p and not p.sent and p.turn==Game.GetCurrentGameTurn()and P.IsTestPlayer(pid)then p.read=true end
 end
 function d.Read(k,p,read)
  if closed or not p.read or config and not d.Ready()then return false,nil,false end
  local captured=generation
  p.read=nil -- consume before the getter; a new event can permit the next drain
  local ok,value=pcall(read)
  local current=not closed and captured==generation and (not config or d.Ready())and not p.read and pending[k]==p and p.turn==Game.GetCurrentGameTurn()
  if config and config.kind=='DialogueProjects'then cultureObserve('UI_QUEUE_READ',function()
   local e=not ok and SPCCultureDiagnostics.Error(value)or {};e.owner=p.pid;e.city=p.id;e.taskStart=p.turn;e.packetEpoch=generation;e.requestAccepted=ok;e.ready=current
   if ok and type(value)=='table'then e.projectType=value.project or 'OTHER';e.queueSize=value.size else e.readStatus='READ_ERROR'end;return e
  end)end
  return ok,value,current
 end
 function d.Bind(fn)
  return function()
   if closed or draining then return end;draining=true
   local ok,value=pcall(function()
    if config then
     if not d.Ready()then
      if config.kind=='DialogueProjects'then cultureObserve('UI_WAIT_READER',function()
       local _,p=next(pending);if not p then return end
       return {recordType=config.kind,owner=p.pid,city=p.id,taskStart=p.turn,packetEpoch=generation,ready=false}
      end)end
      return
     end
     local captured=generation
     if wakePending then
      wakePending=false;resetGeneration()
      for _,p in pairs(pending)do if not p.sent then p.read=true end end
      d.WarmStart()
     end
     replies()
     if generation~=captured or not d.Ready()then return end
    end
    return fn()
   end);draining=false
   if not ok then error(value,0)end;return value
  end
 end
 function d.Close()
  if closed then return end;closed=true
  local row=registration
  if row and config then
   local slots=ExposedMembers.SPC_TimedProjectReaderSlots
   if slots and slots[config.kind]==row then slots[config.kind]=nil end
   local service=shared().TimedProjectReaders
   if registeredService then pcall(registeredService.Unregister,config.kind,row)end
   if service and service~=registeredService then pcall(service.Unregister,config.kind,row)end
  end
  available,registration,registeredService=nil,nil,nil;sent,waiting={},{}
  for k in pairs(pending)do pending[k]=nil end
 end
 return d
end
