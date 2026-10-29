-- B394 disposable scalar observer. No listeners, native objects, save or business API.
-- Disable here, or remove this optional file/import: protected taps become no-ops.
if type(SPCCultureDiagnostics)=='table' and SPCCultureDiagnostics.VERSION==394 then return end
SPCCultureDiagnostics={VERSION=394,ENABLED=true,LIMIT=192,KEYS=128}
local M=SPCCultureDiagnostics
local roles={};local allowedRoles={CULTURE_GP=true,CULTURE_PROJECT_UI=true,CULTURE_ACTIVITY_UI=true}
local fields={'owner','city','eventOwner','eventCity','eventX','eventY','eventCount','eventUnit','eventKind','eventIndex','unitType','unitIndex','phase',
 'recordType','packetEpoch','packetSeq','queueSize','projectType','ready','readStatus','reason','requestAction',
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
function M.Emit(role,point,build)
 if not M.ENABLED or not allowedRoles[role]then return end
 local r=roles[role]
 if r and (r.busy or r.stopped)then return end
 if not r then r={count=0,last={},order={}};roles[role]=r end
 r.busy=true
 local ok=pcall(function()
  local v=build();if type(v)~='table'then return end
  local data={point=scalar(point)};local signature={}
  for _,key in ipairs(fields)do
   local value=scalar(v[key]);if value~=nil then data[key]=value;signature[#signature+1]=key..':'..tostring(value)end
  end
  local key=table.concat({point,tostring(data.owner),tostring(data.city),tostring(data.eventUnit),tostring(data.recordType)},'|')
  local text=table.concat(signature,'|');if not arrivals[point]and r.last[key]==text then return end
  if arrivals[point]then r.arrivals=(r.arrivals or 0)+1;data.eventCount=r.arrivals end
  local logger=SPCExpeditionTrainingDiagnostics
  if type(logger)~='table' or type(logger.New)~='function'then return end
  if not r.trace then r.trace=logger.New(nil,role)end
  if type(r.trace)~='table' or type(r.trace.Record)~='function'then return end
  if r.count>=M.LIMIT then
   r.stopped=true;r.trace.Record('CULTURE_DIAGNOSTIC',{point='LIMIT_REACHED',recordType=role,eventTruncated=true,eventCount=r.count});return
  end
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
