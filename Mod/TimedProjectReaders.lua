-- B394 optional observer: deleting/disabling its module leaves this tap inert.
pcall(include,'CultureDiagnostics')
local function cultureObserve(point,build)
 pcall(function()
  local d=SPCCultureDiagnostics
  if d and d.ENABLED then d.Emit('CULTURE_GP',point,build)end
 end)
end
include('RuntimeWork')
-- Fixed three-slot initialization handshake, not a discovery/event bus.
-- Wake callbacks mark UI work only; this service never reads cities or retries actions.
SPCTimedProjectReaders={}
function SPCTimedProjectReaders.New(P,shared)
 local keys={ClaimProjects='SPC_ClaimQueueRead',DialogueProjects='SPC_DialogueProjectRead',EngineeringStudy='SPC_EngineeringStudyRead'}
 local d={epoch=0,errors={},readers={}};shared.TimedProjectReaders=d
 local sealed=false;local backends,registrations,delivered,serials={},{},{},{}
 local status
 local function current(kind,row)
  local slots=ExposedMembers.SPC_TimedProjectReaderSlots
  return type(row)=='table'and type(row.serial)=='number'and row.serial>=1 and row.serial<9007199254740992 and row.serial%1==0
   and type(slots)=='table'and slots[kind]==row and type(row.reader)=='function'
   and type(row.wake)=='function'and ExposedMembers[keys[kind]]==row.reader
 end
 local function notify(kind)
  local backend,binding=backends[kind],registrations[kind];local row=binding and binding.row
  if shared.TimedProjectReaders~=d or not sealed or d.epoch==0 or not backend or shared[kind]~=backend or not current(kind,row)or binding.reader~=row.reader or binding.wake~=row.wake or binding.serial~=row.serial then return end
  local start=shared.StartStatus and shared.StartStatus[kind=='EngineeringStudy'and 'EngineeringStudyProjects'or kind]
  if shared.StartStatus and (not start or start.state~='OK')then return end
  local last=delivered[kind]
  if last and last.backend==backend and last.row==row and last.reader==row.reader and last.epoch==d.epoch then return end
  local state=status()
  if state~='FRESH'and state~='EXISTING'then d.error=state=='HELD'and 'TIMED_STORE_HELD'or state==nil and 'TIMED_STORE_UNKNOWN'or 'TIMED_STORE_NOT_READY';return end
  d.error=nil
  delivered[kind]={backend=backend,row=row,reader=row.reader,epoch=d.epoch} -- latch before cross-context reentry
  local ok,err=pcall(row.wake,backend,d.epoch,row.reader)
  if kind=='DialogueProjects'then cultureObserve('READER_WAKE_RESULT',function()local e=not ok and SPCCultureDiagnostics.Error(err)or {};e.recordType=kind;e.packetEpoch=d.epoch;e.packetSeq=row.serial;e.requestAccepted=ok;return e end)end
  local printable,text=pcall(tostring,err)
  d.errors[kind]=not ok and (printable and text:sub(1,180)or 'TIMED_READER_WAKE_FAILED')or nil
 end
 function d.Register(kind,row)
  assert(keys[kind],'TIMED_READER_KIND')
  if not current(kind,row)then if kind=='DialogueProjects'then cultureObserve('READER_REGISTER_REJECT',function()return {recordType=kind,packetEpoch=d.epoch,reason='CURRENT_ROW_MISMATCH'}end)end;return false end
  local prior=registrations[kind];local greatest=serials[kind]or 0
  if prior and prior.row==row and (prior.serial~=row.serial or prior.reader~=row.reader or prior.wake~=row.wake)then return false end
  if row.serial<greatest or row.serial==greatest and (not prior or prior.row~=row or prior.reader~=row.reader or prior.wake~=row.wake)then return false end
  d.readers[kind]=row;serials[kind]=row.serial;registrations[kind]={row=row,reader=row.reader,wake=row.wake,serial=row.serial}
  if kind=='DialogueProjects'then cultureObserve('READER_REGISTER',function()return {recordType=kind,packetEpoch=d.epoch,packetSeq=row.serial,ready=sealed}end)end
  notify(kind);return true
 end
 function d.Unregister(kind,row)
  if registrations[kind]and registrations[kind].row==row then registrations[kind]=nil;delivered[kind]=nil;d.readers[kind]=nil end
 end
 function d.Attach(kind,backend)
  assert(keys[kind]and type(backend)=='table','TIMED_BACKEND_KIND')
  backends[kind]=backend;notify(kind)
 end
 status=function()
  local ok,state=pcall(shared.CityProgressionStore.HistoryStartStatus)
  if not ok then d.error='TIMED_STORE_UNKNOWN';return nil end;return state
 end
 local function ready()
  if not sealed then return end
  local state=status()
  if state~='FRESH'and state~='EXISTING'then d.error=state=='HELD'and 'TIMED_STORE_HELD'or state==nil and 'TIMED_STORE_UNKNOWN'or 'TIMED_STORE_NOT_READY';return end
  d.epoch=1;d.error=nil
  cultureObserve('READER_SERVICE_READY',function()return {packetEpoch=d.epoch,readStatus=state}end)
  for kind in pairs(keys)do notify(kind)end
 end
 SPCRuntimeWork.StartReady(P,shared,'TimedProjectReaders',ready)
 function d.Seal()
  sealed=true
  local slots=ExposedMembers.SPC_TimedProjectReaderSlots
  for kind in pairs(keys)do if type(slots)=='table'and slots[kind]then d.Register(kind,slots[kind])end end
  -- Loaded Store may already be initialized even if LoadScreenClose was missed.
  ready()
 end
 return d
end
