-- B205/B206 diagnostic-only scalar trace. Never an admission/ownership authority.
SPCExpeditionTrainingDiagnostics={ENABLED=true,KEEP=256,BUDGET=96,TURN_LIMIT=512,DEDUP_LIMIT=4096}
local M=SPCExpeditionTrainingDiagnostics
local KEY='SPC_B205TrainingTrace'
local keys={'specialization','potential','active','activeStatus','projectionRevision','diagnosticStatus','diagnosticErrorCode','diagnosticErrorClass','diagnosticErrorFile','diagnosticErrorLine','readErrorCode','readErrorClass','readPoint','writeStatus','recordType','capitalType','contractType','diffPath','diffCount','expectedType','actualType','expectedNumber','actualNumber','viewStage','canSign','capitalD','capitalS','capitalC','capitalR','requestedDelta','moneyError','moneyTolerance','moneyAccepted','balanceBefore','balanceAfter','principal','returnAmount','profitRate','probability','contractID','contractDomain','contractDue','contractStage','baseCapacity','baseInput','projectType','lockedPrice','paused','actualDelta','afterProgress','targetChanged','wonderType','wonderEra','wonderCount','eraCount','historyCoverage','historyRevision','templateCount','districtTemplateCount','errorCode','errorClass','errorFile','errorLine','errorSymbol','routeCount','sourceCount','centerCount','recipientCount','relation','networkKind','workers','expected','releaseBranch','networkLayer','networkValidity','networkAvailability','networkInputRevision','networkDerivedFor','networkRevalidation','networkError','bridgeReady','readyToSelect','sleepVisible','sleepAllowed','wakeVisible','wakeAllowed','wakeLegacyAllowed','evaluationOrigin','signalOrigin','coreBusy','operationEvent','lastOperationHash','stage','context','previous','gp','ui','bridge','reader','readerLoad','turn','owner','city','population','phase','reservation','queued','born','completed','eventOwner','eventCity','eventKind','eventIndex','eventUnit','cancelled','unitIndex','unitHash','unitReverse','definitionCost','costModel','costStep','populationCost','spyCost','nativeCost','nativeProgress','queueSize','currentHash','markerIndex','markerHash','markerReverse','markerPresent','wanted','count','priorReader','loads','loadSequence','spyNativeCost','popSource','popEvents','popDelta','popTo','popSum','popMin','popMax','popTurn','readStatus','activityKey','teamKey','mode','activity','activitySampleTurn','awake','hold','sleep','operationEnum','ready','eligibility','eligibilityStatus','guardStatus','guardError','requested','attempted','reason','x','y','actualX','actualY','operationHash','reasonQueryStatus','reasonResultHint','reasonPermission','unitType','nativeResultType','nativeReasonStatus','nativeReasonCount','nativeReasonTruncated','nativeReason1','nativeReason2','nativeReason3','nativeReason4','nativeOwner','nativeUnit','nativeActivity','movesRemaining','maxMoves','nativeReady','spyOperation','spyEndTurn','ownerTurnActive','localPlayer','interfaceMode','sourceCity','targetOwner','targetCity','targetX','targetY','entryX','entryY','arrivalRoute','requestAction','requestResult','requestKey','requestAccepted','storeStatus','storeRevision','savedPhase','savedMatches','taskStart','taskDue','owned','releasePending','submitStatus','missionCategory','requestMission'}
local extraKeys={'observationSeq','observationEpoch','observationCycle','point','lastVerifiedSeq','eventBatch','eventCount','eventTotal','eventTruncated','eventPublishCount','counterBatch','counterTotal','counterOther','counterRest','counterGroup','observerSide','observerErrors','packetSeq','packetTurn','packetSignal','packetEpoch','traceRole','throttleLimit','sampleSuppressed','sealed','loadBeforeSeal','loadSeen','notReady','writerState','controlState','goldBalance','goldYield','maintenance','commerceWrites','carrierGold','heldCount','senderResult','senderFailedTurn','senderTurn','senderTurnActive','networkSignal','routeSignal','buildingIndex','present','pillaged','carrierCount','unreadableCount'}
for _,k in ipairs(extraKeys)do keys[#keys+1]=k end
local changeOnly={REST_ACCESS=true,COMMERCE=true,COMMERCE_DOMAIN=true,NETWORK_PENDING=true,NETWORK_SIGNAL_STALE=true,NETWORK_RECEIVE_REJECT=true,NETWORK_RECEIVE_DROP=true,NETWORK_VERIFIED=true,NETWORK_SAMPLE_FAILED=true,CARRIER_PILLAGED_PRESENT=true,CARRIER_PILLAGE_CLEARED=true}
local identityKeys={'owner','city','targetOwner','targetCity','targetX','targetY','sourceCity','networkKind','contractDomain','projectType','buildingIndex'}
local precise={expectedNumber=true,actualNumber=true,balanceBefore=true,balanceAfter=true,principal=true,
 returnAmount=true,expected=true,actualDelta=true,requestedDelta=true,moneyError=true,moneyTolerance=true,goldBalance=true,goldYield=true,maintenance=true,carrierGold=true}
local function scalar(v,key)
 local t=type(v)
 if t=='nil'then return 'NIL' end
 -- Preserve exact evidence for receipts/comparisons; no extra samples or reads.
 if t=='number' and precise[key] and v==v and v>-math.huge and v<math.huge then
  return string.format('%.17g',v)
 end
 if t=='boolean' or t=='number'then return tostring(v)end
 if t~='string'then return 'OMITTED_'..t end
 -- No user names, arbitrary errors, paths or object stringification.
 if #v>((key=='eventBatch' or key=='counterBatch') and 1800 or (key=='writerState' or key=='controlState') and 256 or 100) or v:find('[^%w_:%-%.|]')then return 'REDACTED' end
 return v
end
-- B231: allowlisted failure metadata only; never retain a path or raw error here.
function M.Failure(value,phase)
 local s=type(value)=='string' and value or ''
 local code=s:match('(CN_[A-Z0-9_]+)') or s:match('(NETWORK_[A-Z0-9_]+)')
  or s:match('(PROGRESSION_[A-Z0-9_]+)') or s:match('(EFFECTIVE_[A-Z0-9_]+)')
  or s:match('(PRESENTATION_[A-Z0-9_]+)')
 local class=code and 'CONTRACT' or s:find('nil value',1,true) and 'LUA_NIL'
  or s:find('attempt to',1,true) and 'LUA_TYPE' or 'READ_ERROR'
 local file,line=s:match('([%w_]+%.lua):(%d+):')
 local allowed={CultureNetwork=true,NetworkBridge=true,NetworkInput=true,CurrentSpecializationFacts=true,
  CityProgressionStore=true,EffectiveFacts=true,CityFlowProbe=true,BindingProbe=true,PropertyCell=true,StoreSubrecords=true,Gameplay=true,CityPotential=true}
 if not file or not allowed[file:gsub('%.lua$','')]then file='UNKNOWN'end
 line=tonumber(line or s:match(':(%d+):'))
 local symbol=s:match("attempt to call %w+ '([%w_]+)' %(a nil value%)")
 local symbols={rawget=true,rawset=true,rawequal=true,getmetatable=true,setmetatable=true,unpack=true,select=true}
 if not symbols[symbol]then symbol=nil end
 return {phase=phase,errorCode=code or class,errorClass=class,errorFile=file,errorLine=line,errorSymbol=symbol}
end
local function root()
 local r=ExposedMembers[KEY]
 if type(r)~='table' or r.schema~=205 then
  r={schema=205,epoch=tostring({}):gsub('[^%w]',''),serial=0,sequence=0,entries={},roles={},suppressed=0,sampleSuppressed=0,errors=0,logged=0}
  ExposedMembers[KEY]=r
 end
 return r
end
local function field(o,k)local ok,v=pcall(function()return o and o[k]end);if ok then return v end end
local function read(o,k,...)
 local fn=field(o,k);if type(fn)~='function'then return 'UNAVAILABLE' end
 local ok,v=pcall(fn,o,...);if not ok then return 'READ_ERROR' end
 return v
end
local function info(P,name,k)
 local ok,v=pcall(function()return P.Info(name,k)end);return ok and v or nil
end
-- B223: optional native readers are observations only. No names, properties,
-- eligibility queries, operations, timers or retries; preserve false/zero/-1.
local function nativeCall(object,key,method,...)
 local fn=field(object,key);if type(fn)~='function'then return 'UNAVAILABLE'end
 local ok,value
 if method then ok,value=pcall(fn,object,...)else ok,value=pcall(fn,...)end
 if not ok then return 'READ_ERROR'end
 if value==nil then return 'NIL'end
 if type(value)=='boolean' or (type(value)=='number' and value==value and value>-math.huge and value<math.huge)then return value end
 return 'INVALID_TYPE'
end
local function unitSample(u)
 local owner=nativeCall(u,'GetOwner',true)
 local player=type(owner)=='number' and field(Players,owner) or nil
 local activity='UNAVAILABLE';if u then activity=nativeCall(UnitManager,'GetActivityType',false,u)end
 return {nativeOwner=owner,nativeUnit=nativeCall(u,'GetID',true),
  actualX=nativeCall(u,'GetX',true),actualY=nativeCall(u,'GetY',true),
  nativeActivity=activity,
  movesRemaining=nativeCall(u,'GetMovesRemaining',true),maxMoves=nativeCall(u,'GetMaxMoves',true),
  nativeReady=nativeCall(u,'IsReadyToMove',true),spyOperation=nativeCall(u,'GetSpyOperation',true),
  spyEndTurn=nativeCall(u,'GetSpyOperationEndTurn',true),ownerTurnActive=nativeCall(player,'IsTurnActive',true),
  localPlayer=nativeCall(Game,'GetLocalPlayer',false),interfaceMode=nativeCall(UI,'GetInterfaceMode',false)}
end
-- B228: optional observations at existing UI lifecycle samples only. Never a
-- permission authority, retry trigger, writer or all-unit scan.
local function activityEligibility(u,stage)
 local v={readyToSelect=nativeCall(u,'IsReadyToSelect',true)}
 local function query(tab,key,fn,...)
  local row=field(field(GameInfo,tab),key);local hash=field(row,'Hash')
  if type(hash)~='number'then return 'UNAVAILABLE'end
  return nativeCall(UnitManager,fn,false,u,hash,...)
 end
 if stage=='IDLE_UI'then
 v.sleepVisible=query('UnitOperations','UNITOPERATION_SLEEP','CanStartOperation',nil,true)
 v.sleepAllowed=query('UnitOperations','UNITOPERATION_SLEEP','CanStartOperation',nil,false,false)
 end
 v.wakeVisible=query('UnitCommands','UNITCOMMAND_WAKE','CanStartCommand',true)
 v.wakeAllowed=query('UnitCommands','UNITCOMMAND_WAKE','CanStartCommand',false,true)
 v.wakeLegacyAllowed=query('UnitCommands','UNITCOMMAND_WAKE','CanStartCommand',false)
 return v
end
local activityStages={IDLE_UI=true,ACTIVITY_START=true,ACTIVITY_FAILURE=true,ACTIVITY_RELEASE=true,ACTIVITY_WAKE_REQUEST=true}
local noop={id='DISABLED',loads=0,Event=function()end,Record=function()end,Unit=function()end,Load=function()end}
function M.New(P,role)
 if not M.ENABLED then return noop end
 local ok,api=pcall(function()
  local r=root();r.serial=r.serial+1
  local prior=r.roles[role]
  -- Plain Lua allocation only: observational identity, never a saved/native token.
  local id=role..':'..r.serial..':'..tostring({}):gsub('[^%w]','')
  local a={id=id,loads=0};local sampled=0;local busy=false;local sampling=false
  local last,order={},{};local turnKey,turnUsed,throttled=nil,0,false
  r.roles[role]=id
  local function append(v)
   local out,saved={},{}
   for _,k in ipairs(keys)do if v[k]~=nil then saved[k]=scalar(v[k],k);out[#out+1]=k..'='..saved[k]end end
   r.sequence=r.sequence+1;saved.sequence=r.sequence
   saved.line=('[SPC][B205][TRAIN] seq='..r.sequence..' '..table.concat(out,' ')):sub(1,4096)
   r.entries[#r.entries+1]=saved;if #r.entries>M.KEEP then table.remove(r.entries,1)end
   pcall(print,saved.line)
   pcall(function()if LuaEvents then LuaEvents.SPC_B205TrainingTrace()end end)
  end
  local function record(stage,data)
   if busy or r.sinkEmitting then return end
   busy=true
   local good=pcall(function()
    local v={stage=stage,context=id,traceRole=role,gp=r.roles.GAMEPLAY,ui=r.roles.PRODUCTION_UI,bridge=r.bridge,loads=a.loads,loadSequence=r.loadSequence or 0}
    local turnOK,turn=pcall(function()return Game.GetCurrentGameTurn()end);v.turn=turnOK and turn or 'UNAVAILABLE'
    for _,k in ipairs(keys)do if data and data[k]~=nil then v[k]=data[k]end end
    local stable=changeOnly[stage] or stage:match('_QUOTE$') or stage:match('_FAILURE$') or stage:match('_HELD$')
    local ident={stage};for _,k in ipairs(identityKeys)do ident[#ident+1]=scalar(v[k],k)end
    local k=table.concat(ident,'|');local parts={}
    for _,name in ipairs(keys)do
     if v[name]~=nil and (not stable or (name~='turn' and name~='context' and name~='gp' and name~='ui' and name~='loads' and name~='loadSequence'))then
      parts[#parts+1]=name..'='..scalar(v[name],name)
     end
    end
    local signature=table.concat(parts,' ')
    if stable and last[k]==signature then return end
    if turnKey~=v.turn then turnKey=v.turn;turnUsed=0;throttled=false end
    if turnUsed>=M.TURN_LIMIT then
     r.suppressed=math.min(2147483647,r.suppressed+1)
     if not throttled then
      throttled=true
      append({stage='TRACE_THROTTLED',context=id,traceRole=role,turn=v.turn,throttleLimit=M.TURN_LIMIT,reason='RUNAWAY_BREAKER'})
     end
     return
    end
    if stable and not last[k]then
     if #order>=M.DEDUP_LIMIT then last[table.remove(order,1)]=nil end
     order[#order+1]=k
    end
    if stable then last[k]=signature end;turnUsed=turnUsed+1;append(v)
   end)
   if not good then r.errors=math.min(2147483647,r.errors+1)end
   busy=false
  end
  local function sampleAllowed()
   if sampled>=M.BUDGET then r.sampleSuppressed=math.min(2147483647,(r.sampleSuppressed or 0)+1);return false end
   sampled=sampled+1;return true
  end
  function a.Record(stage,data)record(stage,data)end
  function a.Unit(stage,u,extra)
   if busy or sampling then return end
   if not sampleAllowed()then return end
   sampling=true
   local good=pcall(function()
    local v=unitSample(u)
    if activityStages[stage] and type(v.nativeActivity)=='number'then for k,value in pairs(activityEligibility(u,stage))do v[k]=value end end
    -- Callers supply only fixed state/attempt scalars. Native samples stay separate
    -- from the activity guard's last-read fields and from persisted authority.
    for _,k in ipairs(keys)do if extra and extra[k]~=nil then v[k]=extra[k]end end
    record(stage,v)
   end)
   if not good then r.errors=math.min(2147483647,r.errors+1)end
   sampling=false
  end
  function a.Event(stage,c,s,extra)
   if busy or sampling then return end
   if not sampleAllowed()then return end
   sampling=true
   local good=pcall(function()
    local v={owner=read(c,'GetOwner'),city=read(c,'GetID'),population=read(c,'GetPopulation')}
    if s then v.phase=field(s,'phase');v.reservation=field(s,'trainingToken');v.queued=field(s,'trainingQueued');v.born=field(s,'trainingBorn');v.completed=field(s,'trainingCompleted')end
    local u=info(P,'Units','UNIT_SPC_EXPEDITION_SPY');local b=info(P,'Buildings','BUILDING_SPC_EXPEDITION_TRAINING_ACCESS')
    local i=field(u,'Index');local bi=field(b,'Index')
    v.unitIndex=i;v.unitHash=field(u,'Hash');v.unitReverse=field(info(P,'Units',i),'UnitType')
    v.definitionCost=field(u,'Cost');v.costModel=field(u,'CostProgressionModel');v.costStep=field(u,'CostProgressionParam1');v.populationCost=scalar(field(u,'PopulationCost'))
    v.spyCost=field(info(P,'Units','UNIT_SPY'),'Cost')
    v.markerIndex=bi;v.markerHash=field(b,'Hash');v.markerReverse=field(info(P,'Buildings',bi),'BuildingType')
    local q=read(c,'GetBuildQueue');local buildings=read(c,'GetBuildings')
    v.nativeCost=type(i)=='number' and read(q,'GetUnitCost',i) or 'INDEX_UNKNOWN'
    v.nativeProgress=type(i)=='number' and read(q,'GetUnitProgress',i) or 'INDEX_UNKNOWN'
    -- B206: ordinary spy native cost in the same city, for comparison only.
    local si=field(info(P,'Units','UNIT_SPY'),'Index');v.spyNativeCost=type(si)=='number' and read(q,'GetUnitCost',si) or 'INDEX_UNKNOWN'
    v.queueSize=read(q,'GetSize');v.currentHash=read(q,'GetCurrentProductionTypeHash')
    if type(bi)=='number'then v.markerPresent=read(buildings,'HasBuilding',bi)else v.markerPresent='INDEX_UNKNOWN'end
    for _,k in ipairs(keys)do if extra and extra[k]~=nil then v[k]=extra[k]end end
    record(stage,v)
   end)
   if not good then r.errors=math.min(2147483647,r.errors+1)end
   sampling=false
  end
  function a.Load()a.loads=a.loads+1;r.loadSequence=(r.loadSequence or 0)+1;a.Record('LOAD_CLOSE')end
  a.Record('CONTEXT_START',{previous=prior,priorReader=type(ExposedMembers.SPC_ExpeditionQueueRead)})
  return a
 end)
 return ok and api or noop
end
-- Called in the existing independent UI observer, never from Gameplay.
function M.Sink(P)
 local a=M.New(P,'LOG_UI');local stopped=false;local busy=false;local emitted=0;local failed=false
 local event=LuaEvents and LuaEvents.SPC_B205TrainingTrace
 local function flush()
  if stopped or busy or failed or not M.ENABLED then return end
  busy=true
  local ok=pcall(function()
   local r=root();if r.sink~=a.id then return end
   if not UI or type(UI.DataError)~='function'then r.sinkStatus='UNAVAILABLE';return end
   for _,e in ipairs(r.entries)do
    if e.sequence>r.logged then
     if emitted>=128 then r.sinkStatus='BUDGET_STOP';return end
     r.logged=e.sequence;emitted=emitted+1 -- before native call/reentry
     r.sinkEmitting=true
     local good=pcall(UI.DataError,e.line)
     r.sinkEmitting=false
     if not good then failed=true;r.sinkStatus='ERROR_STOP';return end
    end
   end
   r.sinkStatus='CALLS_RETURNED' -- NOT proof of disk output on this platform.
  end)
  if not ok then failed=true;pcall(function()root().sinkStatus='ERROR_STOP'end)end
  busy=false
 end
 if M.ENABLED then
  pcall(function()root().sink=a.id;if event and event.Add then event.Add(flush)end end)
  flush()
 end
 function a.Stop()
  a.Record('UI_SHUTDOWN');flush();stopped=true
  pcall(function()if event and event.Remove then event.Remove(flush)end end)
 end
 return a
end
function M.Report()
 local ok,result=pcall(function()
  local r=ExposedMembers[KEY];if not M.ENABLED or type(r)~='table' or r.schema~=205 then return '' end
  local lines={Locale.Lookup('LOC_SPC_EXPEDITION_TRAIN_DIAG_HEADER'),Locale.Lookup('LOC_SPC_EXPEDITION_TRAIN_DIAG_STATE',#r.entries,r.suppressed,r.errors,r.sinkStatus or 'NOT_STARTED')}
  for i=math.max(1,#r.entries-7),#r.entries do
   local e=r.entries[i];lines[#lines+1]=string.format('#%s %s T%s city=%s pop=%s cost=%s/%s phase=%s',e.sequence,e.stage,e.turn or '?',e.city or '-',e.population or '-',e.definitionCost or '?',e.nativeCost or '?',e.phase or '-')
  end
  return table.concat(lines,'[NEWLINE]')
 end)
 return ok and result or ''
end
