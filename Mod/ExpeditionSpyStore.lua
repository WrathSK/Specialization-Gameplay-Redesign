-- B201: one bounded player-owned Expedition record. Game Property is save authority;
-- callers own phase/native-action semantics. No retries, migration or cleanup here.
SPCExpeditionSpyStore={PREFIX='SPC_EXPEDITION_TEAM_P'}
local M=SPCExpeditionSpyStore
local phases={TRAINING=true,CREATING=true,NAMING=true,CREATED=true,TRAVELLING=true,ARRIVED=true,
 TASK_PREPARING=true,TASK_RUNNING=true,TASK_COMPLETE=true,HELD=true,ENDING=true,ENDED=true}
local numbers={owner=true,unitID=true,createdID=true,sourceCity=true,x=true,y=true,
 trainingBorn=true,trainingTurn=true,trainingReceiptTurn=true,startTurn=true,dueTurn=true,taskStart=true,taskDue=true,taskCompleted=true,taskCompletions=true,taskCount=true,missionX=true,missionY=true,entryX=true,entryY=true}
local booleans={trainingQueued=true,trainingCompleted=true,nameVerified=true,activityOwned=true,activityPending=true,sleepConfirmed=true}
local strings={trainingToken=100,sourceName=220,sourceRef=2048,expectedName=220,teamKey=100,
 activityKey=100,activityMode=32,stop=100,errorStep=100,errorDetail=220,missionCategory=16,missionEvidence=160,taskOutcome=16}
local modes={NONE=true,SLEEP=true,ARMED=true,ASLEEP=true,RELEASE=true,BLOCKED=true}
local function integer(v)
 return type(v)=='number' and v==v and v>=0 and v<=9007199254740991 and v%1==0
end
local function plain(v)return type(v)=='table' and getmetatable(v)==nil end
local function bounded(v,n)return type(v)=='string' and #v>0 and #v<=n end
local function target(value)
 if not plain(value)then return nil end
 local out={}
 for key,v in pairs(value)do
  if key=='name' then if not bounded(v,220)then return nil end
  elseif key=='owner' or key=='id' or key=='x' or key=='y' then if not integer(v)then return nil end
  else return nil end
  out[key]=v
 end
 for _,key in ipairs({'owner','id','x','y'})do if out[key]==nil then return nil end end
 return out
end
local function state(value,pid)
 if not plain(value)or value.owner~=pid or not phases[value.phase]then return nil end
 local out={}
 for key,v in pairs(value)do
  if key=='phase' then if not phases[v]then return nil end
  elseif key=='target' then v=target(v);if not v then return nil end
  elseif numbers[key]then if not integer(v)then return nil end
  elseif booleans[key]then if type(v)~='boolean'then return nil end
  elseif strings[key]then
   if not bounded(v,strings[key])then return nil end
   if key=='activityMode' and not modes[v]then return nil end
  else return nil end
  out[key]=v
 end
 local phase=out.phase
 if phase=='TRAINING' then
  for _,k in ipairs({'sourceCity','sourceName','sourceRef','x','y','trainingToken','trainingTurn'})do if out[k]==nil then return nil end end
  if out.unitID~=nil or out.teamKey~=nil or out.expectedName~=nil then return nil end
 end
 if phase~='TRAINING' and phase~='CREATING' and phase~='HELD' and phase~='ENDING' and phase~='ENDED' then
  for _,k in ipairs({'unitID','createdID','sourceCity','sourceRef','x','y','teamKey'})do
   if out[k]==nil then return nil end
  end
 end
 if phase=='CREATED' or phase=='TRAVELLING' or phase=='ARRIVED' or
  phase=='TASK_PREPARING' or phase=='TASK_RUNNING' or phase=='TASK_COMPLETE' then
  if out.nameVerified~=true or out.expectedName==nil then return nil end
 end
 if phase=='TRAVELLING' then
  if not out.target or out.startTurn==nil or out.dueTurn==nil or out.dueTurn<out.startTurn then return nil end
 end
 if phase=='TASK_PREPARING' or phase=='TASK_RUNNING' or phase=='TASK_COMPLETE' then
  if not out.target or out.activityKey==nil then return nil end
 end
 if phase=='TASK_PREPARING' then
  if out.activityPending~=true or out.sleepConfirmed==true then return nil end
  if out.activityMode=='SLEEP' then
   if out.activityOwned~=false then return nil end
  elseif out.activityMode=='ARMED' then
   if out.activityOwned~=true then return nil end
  else return nil end
 end
 if phase=='TASK_RUNNING' then
  if out.activityMode~='ASLEEP' or out.sleepConfirmed~=true or out.activityPending~=false or
   type(out.activityOwned)~='boolean' or out.taskStart==nil or out.taskDue==nil or out.taskDue<out.taskStart then return nil end
 end
 if phase=='TASK_COMPLETE' then
  if out.taskStart==nil or out.taskDue==nil or out.taskCompleted==nil or not (out.taskCompletions==1 or (out.taskCompletions==0 and out.taskOutcome=='CANCELLED')) or
   out.taskDue<out.taskStart or (out.taskOutcome=='CANCELLED' and out.taskCompleted<out.taskStart or out.taskOutcome~='CANCELLED' and out.taskCompleted<out.taskDue) or
   type(out.activityOwned)~='boolean' or type(out.activityPending)~='boolean' then return nil end
  if out.activityMode=='RELEASE' then
   if not out.activityOwned and not out.activityPending then return nil end
  elseif out.activityMode=='NONE' or out.activityMode=='BLOCKED' then
   if out.activityPending then return nil end
   if out.activityMode=='NONE' and out.activityOwned then return nil end
  else return nil end
 end
 return out
end
local function envelope(value,pid)
 if not plain(value)or value.schema~=1 or value.owner~=pid or
  not integer(value.generation)or not integer(value.revision)or value.revision<1 or value.generation<1 then return nil end
 local out={schema=1,owner=pid,generation=value.generation,revision=value.revision}
 for key in pairs(value)do
  if key~='schema' and key~='owner' and key~='generation' and key~='revision' and key~='state' then return nil end
 end
 if value.state~=nil then out.state=state(value.state,pid);if not out.state then return nil end end
 return out
end
local function equal(a,b)
 if type(a)~=type(b)then return false end
 if type(a)~='table'then return a==b end
 for k,v in pairs(a)do if not equal(v,b[k])then return false end end
 for k in pairs(b)do if a[k]==nil then return false end end
 return true
end
local function key(pid)return M.PREFIX..tostring(pid)end
local function read(pid)
 local ok,raw=pcall(function()
  assert(Game and type(Game.GetProperty)=='function','PROPERTY_READER_UNAVAILABLE')
  return Game:GetProperty(key(pid))
 end)
 if not ok then return nil,'STORE_UNREADABLE' end
 if raw==nil then return nil end
 local value=envelope(raw,pid)
 if not value then return nil,'STORE_CORRUPT' end
 return value
end
function M.Read(pid)
 if not integer(pid)then return nil,'STORE_OWNER_INVALID' end
 return read(pid)
end
function M.Write(P,pid,expected,candidate)
 if not integer(pid)then return nil,'STORE_OWNER_INVALID' end
 local old
 if expected~=nil then old=envelope(expected,pid);if not old then return nil,'STORE_EXPECTED_INVALID' end end
 local nextValue=envelope(candidate,pid)
 if not nextValue then return nil,'STORE_CANDIDATE_INVALID' end
 if nextValue.revision~=(old and old.revision+1 or 1)or
  (old and nextValue.generation~=old.generation and nextValue.generation~=old.generation+1)or
  (not old and nextValue.generation~=1)then return nil,'STORE_SEQUENCE_INVALID' end
 local current,err=read(pid)
 if err then return nil,err end
 if not equal(current,old)then return nil,'STORE_STALE_EXPECTED' end
 -- Treat a writer return/exception as inconclusive. The validated readback is
 -- the outcome authority, including a write that succeeded before throwing.
 pcall(function()
  assert(P and type(P.SetProperty)=='function','PROPERTY_WRITER_UNAVAILABLE')
  P.SetProperty(Game,key(pid),envelope(nextValue,pid))
 end)
 local observed,readError=read(pid)
 if readError then
  return nil,readError=='STORE_CORRUPT' and 'STORE_WRITE_READBACK_CORRUPT' or 'STORE_WRITE_READBACK_UNREADABLE'
 end
 if equal(observed,nextValue)then return envelope(observed,pid) end
 if observed==nil then return nil,'STORE_WRITE_UNCONFIRMED_ABSENT' end
 if equal(observed,old)then return nil,'STORE_WRITE_UNCONFIRMED_OLD' end
 return nil,'STORE_WRITE_UNCONFIRMED_OTHER'
end
return M
