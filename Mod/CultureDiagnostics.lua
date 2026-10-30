-- B394 disposable scalar observer. No listeners, native objects, save or business API.
-- Disable here, or remove this optional file/import: protected taps become no-ops.
if type(SPCCultureDiagnostics)=='table' and SPCCultureDiagnostics.VERSION==396 then return end
SPCCultureDiagnostics={VERSION=396,ENABLED=true,LIMIT=192,KEYS=128}
local M=SPCCultureDiagnostics
local roles={};local allowedRoles={CULTURE_GP=true,CULTURE_PROJECT_UI=true,CULTURE_ACTIVITY_UI=true,CULTURE_GPP_READ_UI=true,CULTURE_GPP_READ_GP=true,CULTURE_GPP_DIRTY=true}
local fields={'owner','city','eventOwner','eventCity','eventX','eventY','eventCount','eventUnit','eventKind','eventIndex','unitType','unitIndex','phase',
 'readPoint','observerSide','requestKey','recordType','packetEpoch','packetSeq','queueSize','projectType','ready','readStatus','reason','requestAction',
 'requestAccepted','requestResult','taskStart','taskDue','workers','expected','expectedNumber','actualNumber',
 'active','specialization','activityKey','teamKey','mode','activity','activitySampleTurn','x','y','actualX','actualY',
 'operationEvent','operationHash','sourceCity','targetOwner','targetCity','reservation','queued','born','completed',
 'count','errorCode','errorClass','errorFile','errorLine','observerErrors','loadSequence'}
local arrivals={WORKER_CAUSE=true,UI_QUEUE_EVENT=true,UNIT_ADDED_OBSERVED=true,EXPEDITION_ACTIVITY_EVENT=true,EXPEDITION_OPERATION_EVENT=true,EXPEDITION_MOVE_EVENT=true,EXPEDITION_TURN_STATE=true}
local function scalar(v)
 local t=type(v)
 if t=='boolean' then return v end
 if t=='number' and v==v and v>-math.huge and v<math.huge then return v end
 if t=='string' and #v<=100 and not v:find('[^%w_:%-%.|]')then return v end
end
function M.Error(err)
 local s=type(err)=='string' and err or ''
 local file,line=s:match('([%w_]+%.lua):(%d+):')
 local known={TimedProjectSelectionClient=true,TimedProjectReaders=true,DialogueProjectUI=true,DialogueProjects=true,
  Gameplay=true,ExpeditionSpyActivity=true,ExpeditionTraining=true,Lv2GPP=true}
 if not file or not known[file:gsub('%.lua$','')]then file='UNKNOWN'end
 return {errorClass=s:find('nil value',1,true)and 'LUA_NIL' or s:find('attempt to',1,true)and 'LUA_TYPE' or 'OBSERVED_ERROR',
  errorCode=s:match('([A-Z][A-Z0-9]+_[A-Z0-9_]+)')or 'UNCLASSIFIED',errorFile=file,errorLine=tonumber(line)}
end
-- The optional observer owns its transport. Never re-include an existing logger:
-- its file assigns globals,including ENABLED. Missing dependency is tried once.
local transportAttempted=false
local function transport()
 local logger=SPCExpeditionTrainingDiagnostics
 if type(logger)=='table' and logger.ENABLED==false then return end
 if type(logger)~='table' or type(logger.New)~='function'then
  if transportAttempted then return end
  transportAttempted=true;pcall(include,'ExpeditionTrainingDiagnostics')
  logger=SPCExpeditionTrainingDiagnostics
 end
 if type(logger)=='table' and type(logger.New)=='function' and logger.ENABLED~=false then return logger end
end
local function trace(r,logger,role)
 if not r.trace then r.trace=logger.New(nil,role)end
 return type(r.trace)=='table' and r.trace.id~='DISABLED' and type(r.trace.Record)=='function'
end
function M.Emit(role,point,build,nativeSample)
 -- Keep an explicit GP read available after the automatic cause budget ends.
 if role=='CULTURE_GP' and point=='GPP_EXPLICIT_GP'then role='CULTURE_GPP_READ_GP'end
 if not M.ENABLED or not allowedRoles[role]then return end
 local r=roles[role]
 if r and (r.busy or r.stopped)then return end
 if not r then r={count=0,last={},order={}};roles[role]=r end
 r.busy=true
 local ok=pcall(function()
  if r.count>=M.LIMIT then
   r.stopped=true;if r.trace then r.trace.Record('CULTURE_DIAGNOSTIC',{point='LIMIT_REACHED',recordType=role,eventTruncated=true,eventCount=r.count})end;return
  end
  local logger=transport()
  if not logger then r.stopped=true;return end
  -- Scalar-only taps keep lazy construction after dedup. UI native sampling
  -- requires a working,non-noop transport before reading any native fact.
  if nativeSample and not trace(r,logger,role)then r.stopped=true;return end
  local v=build();if type(v)~='table'then return end
  local data={point=scalar(point)};local signature={}
  for _,key in ipairs(fields)do
   local value=scalar(v[key]);if value~=nil then data[key]=value;signature[#signature+1]=key..':'..tostring(value)end
  end
  local key=table.concat({point,tostring(data.owner),tostring(data.city),tostring(data.eventUnit),tostring(data.recordType)},'|')
  local text=table.concat(signature,'|');if not arrivals[point]and r.last[key]==text then return end
  if arrivals[point]then r.arrivals=(r.arrivals or 0)+1;data.eventCount=r.arrivals end
  if not trace(r,logger,role)then r.stopped=true;return end
  if r.last[key]==nil then
   if #r.order>=M.KEYS then r.last[table.remove(r.order,1)]=nil end
   r.order[#r.order+1]=key
  end
  r.last[key]=text;r.count=r.count+1
  r.trace.Record('CULTURE_DIAGNOSTIC',data)
 end)
 r.busy=false
 if not ok then r.stopped=true end -- diagnostics may stop; business never waits for it
end

-- B395 explicit P0 reply only. Never a fact provider or a citizen-management command.
local gppTokens,gppOrder={},{}
local gppKinds={RESEARCH=true,CULTURE=true,INDUSTRY=true,COMMERCE=true}
function M.ObserveGPPUI(P,token,cityID,kind)
 if not M.ENABLED or not gppKinds[kind] or type(token)~='string' or #token>100 or gppTokens[token]then return end
 local role=roles.CULTURE_GPP_READ_UI;if role and role.stopped then return end
 if #gppOrder>=128 then gppTokens[table.remove(gppOrder,1)]=nil end
 gppTokens[token]=true;gppOrder[#gppOrder+1]=token -- bounded recent-request dedup, never a business fact
 M.Emit('CULTURE_GPP_READ_UI','GPP_EXPLICIT_UI',function()
  local out={city=cityID,requestKey=token,specialization=kind,readStatus='UNKNOWN'}
  local readPoint='PLAYER'
  local ok=pcall(function()
   local pid=Game.GetLocalPlayer();out.owner=pid
   assert(P.IsTestPlayer(pid),'PLAYER')
   readPoint='SELECTED_CITY'
   local c=UI.GetHeadSelectedCity();assert(c and c:GetOwner()==pid and c:GetID()==cityID,'CITY')
   local x,y=c:GetX(),c:GetY()
   readPoint='DISTRICTS'
   local anchor,n=nil,0
   for _,district in c:GetDistricts():Members()do
    n=n+1;assert(n<=64,'DISTRICT_BOUND')
    local row=P.Info('Districts',district:GetType())
    if row and P.Family(row.DistrictType)==kind then
     local owner=assert(district:GetCity());assert(owner:GetOwner()==pid and owner:GetID()==cityID,'DISTRICT_OWNER')
     assert(anchor==nil,'AMBIGUOUS_ANCHOR');anchor=Map.GetPlot(district:GetX(),district:GetY()):GetIndex()
    end
   end
   assert(type(anchor)=='number','ANCHOR')
   readPoint='COMMAND_TARGETS'
   local params={};params[CityCommandTypes.PARAM_MANAGE_CITIZEN]=UI.GetInterfaceModeParameter(CityCommandTypes.PARAM_MANAGE_CITIZEN)
   local rows=assert(CityManager.GetCommandTargets(c,CityCommandTypes.MANAGE,params),'TARGETS')
   readPoint='CITIZEN_ARRAYS'
   local plots=assert(rows[CityCommandResults.PLOTS]);local actual=assert(rows[CityCommandResults.CITIZENS])
   local capacity=assert(rows[CityCommandResults.MAX_CITIZENS]);local locked=assert(rows[CityCommandResults.LOCKED_CITIZENS])
   readPoint='ANCHOR_MATCH'
   local count,found=0,nil
   for i,index in pairs(plots)do
    count=count+1;assert(count<=128,'BOUND')
    if index==anchor then
     assert(not found,'AMBIGUOUS');found={plot=assert(Map.GetPlotByIndex(index)),index=index,actual=actual[i],capacity=capacity[i],locked=locked[i]}
    end
   end
   assert(found,'ANCHOR')
   local function integer(v)return type(v)=='number' and v>=0 and v<=255 and v%1==0 end
   readPoint='UI_WORKER_COUNT'
   local workers=found.plot:GetWorkerCount()
   readPoint='COUNT_VALUES'
   assert(integer(found.actual)and integer(found.capacity)and integer(found.locked)and integer(workers),'NUMBERS')
   assert(found.actual<=found.capacity and found.locked<=found.actual,'RANGE')
   readPoint='FINAL_SELECTION'
   local selected=UI.GetHeadSelectedCity()
   assert(selected and selected:GetOwner()==pid and selected:GetID()==cityID and selected:GetX()==x and selected:GetY()==y
    and c:GetOwner()==pid and c:GetID()==cityID,'CITY_CHANGED')
   out.workers=found.actual;out.count=found.locked;out.expectedNumber=found.capacity;out.actualNumber=workers
   out.eventIndex=found.index;out.readStatus='UI_COMMAND_TARGETS'
  end)
  if not ok then out.reason='READ_UNCONFIRMED';out.readPoint=readPoint end
  return out
 end,true)
end
