-- B201: fresh recovery observations and durable arming before one native Sleep request.
-- No persistent state, native espionage mission, or dependency on the management window.
include('Probe')
local P=SPCP0
local KIND='UNIT_SPC_EXPEDITION_SPY'
local initialized=false;local stopped=false;local busy=false;local queued=false;local queuedMonitor=false
local job;local seen={};local lastRevision
local pump
local watch
local function detail(err)return tostring(err):gsub('[%c]',' '):sub(1,180)end
local function view()return ExposedMembers and ExposedMembers.SPC_ExpeditionActivity end
local function integer(v)return type(v)=='number' and v>=0 and v%1==0 end
local function same(v,n)
 return v and v.owner==n.owner and v.unitID==n.unitID and v.activityKey==n.activityKey
  and v.teamKey==n.teamKey and v.mode==n.mode and v.phase==n.phase and v.expectedName==n.expectedName
  and v.x==n.x and v.y==n.y and (v.owned==true)==n.publishedOwned
  and (v.releasePending==true)==n.releasePending
end
local function cancel()
 job=nil;ContextPtr:ClearUpdate()
end
local function supported(v)
 return type(v)=='table' and integer(v.revision) and integer(v.owner) and integer(v.unitID)
  and Game.GetLocalPlayer()==v.owner and P.IsTestPlayer(v.owner)
  and type(v.activityKey)=='string' and #v.activityKey>0 and #v.activityKey<=100
  and type(v.teamKey)=='string' and #v.teamKey>0 and #v.teamKey<=100
  and type(v.expectedName)=='string' and #v.expectedName>0
  and integer(v.x) and integer(v.y)
end
-- B217: initial placement visibility is event-driven; no timer/polling until position agrees.
local function positionDetail(n)
 return 'expected='..tostring(n.x)..','..tostring(n.y)..' actual='..tostring(n.actualX)..','..tostring(n.actualY)
end
local function positionLog(n,status)
 print('[SPC][B191][N1_TASK] position='..status..' owner='..n.owner..' unit='..n.unitID..' key='..n.activityKey..' phase='..tostring(n.phase)..' '..positionDetail(n))
end
local function read(n)
 assert(Game.GetLocalPlayer()==n.owner and P.IsTestPlayer(n.owner),'ACTIVITY_LOCAL_OWNER_CHANGED')
 local p=Players[n.owner];assert(p and p.GetUnits,'ACTIVITY_PLAYER_UNREADABLE')
 local u=p:GetUnits():FindID(n.unitID)
 assert(u and u:GetID()==n.unitID and u:GetOwner()==n.owner,'ACTIVITY_EXACT_UNIT_CHANGED')
 local row=GameInfo.Units[u:GetUnitType()]
 assert(row and row.UnitType==KIND,'ACTIVITY_UNIT_TYPE_CHANGED')
 assert(type(u.GetName)=='function' and u:GetName()==n.expectedName,'ACTIVITY_NAME_CHANGED')
 assert(type(u.GetSpyOperation)=='function' and u:GetSpyOperation()==-1,'ACTIVITY_NATIVE_MISSION_OR_UNREADABLE')
 n.actualX=u:GetX();n.actualY=u:GetY()
 assert(integer(n.actualX) and integer(n.actualY),'ACTIVITY_POSITION_UNREADABLE')
 if n.actualX~=n.x or n.actualY~=n.y then
  local initial=n.mode=='SLEEP' and n.phase=='TASK_PREPARING' and not n.owned and not n.requested
   and seen.key==n.activityKey and not seen.attempted and not seen.positionReady and same(view(),n)
  if initial then
   if not n.positionPending then n.positionPending=true;positionLog(n,'WAITING')end
   return nil -- Only native publications/movement events can resume; no SLEEP/ACK/timer.
  end
  positionLog(n,'REJECTED');error('ACTIVITY_POSITION_CHANGED '..positionDetail(n),0)
 end
 if n.positionPending then n.positionPending=false;positionLog(n,'CONVERGED')end
 if seen.key==n.activityKey then seen.positionReady=true end
 assert(UnitManager and type(UnitManager.GetActivityType)=='function' and ActivityTypes,'ACTIVITY_READER_UNAVAILABLE')
 local activity=UnitManager.GetActivityType(u)
 assert(activity~=nil,'ACTIVITY_UNREADABLE')
 if n.mode=='SLEEP' or n.mode=='ARMED' or n.mode=='RECOVER' then
  -- One replaceable last-read sample, not a fresh read at the timeout deadline.
  n.lastActivity=activity;n.sampledElapsed=n.elapsed
  n.sampleAwake=ActivityTypes.ACTIVITY_AWAKE;n.sampleHold=ActivityTypes.ACTIVITY_HOLD
  n.sampleSleep=ActivityTypes.ACTIVITY_SLEEP;n.sampleOperation=ActivityTypes.ACTIVITY_OPERATION
  local timed,turn=pcall(Game.GetCurrentGameTurn);n.sampleTurn=timed and turn or nil
 end
 if activity==ActivityTypes.ACTIVITY_SLEEP and seen.key==n.activityKey then seen.sleepObserved=true end
 return u,activity
end
local function acknowledge(n,result,reason,sleeping,awake)
 local current=view()
 if not same(current,n)then cancel();return end
 if seen.key~=n.activityKey then return end
 local slot=n.mode=='ASLEEP' and 'monitor' or n.mode
 if seen[slot]then return end
 seen[slot]=true;cancel()
 ExposedMembers.SPC_ExpeditionGateSequence=(ExposedMembers.SPC_ExpeditionGateSequence or 0)+1
 local args={OnStart='SPC_ExpeditionGateRequest',Action='ACTIVITY',
  Token='Activity:'..tostring(ExposedMembers.SPC_ExpeditionGateSequence),
  UnitID=n.unitID,ActivityKey=n.activityKey,Result=result,Owned=n.owned==true,
  SampleTurn=Game.GetCurrentGameTurn(),Detail=reason and detail(reason) or nil}
 if result~='FAILED' then args.NativeOperation=-1 end
 if result=='RECOVERED' or result=='ARMED'then args.Sleeping=sleeping;args.Awake=awake end
 local ok,err=pcall(function()
  assert(UI and type(UI.RequestPlayerOperation)=='function' and PlayerOperations,'ACTIVITY_REQUEST_UNAVAILABLE')
  UI.RequestPlayerOperation(n.owner,PlayerOperations.EXECUTE_SCRIPT,args)
 end)
 if not ok then
  -- The request may already have executed: never retry or submit another native operation.
  print('[SPC][B191][ACTIVITY_ACK_UNKNOWN] '..detail(err))
 end
end
local function fail(n,err)acknowledge(n,'FAILED',err)end
-- Native UnitPanel resolves action identifiers through exact GameInfo rows.
-- Keep the checked hash for the one request; enum aliases and optional result hints
-- are not portable across the UI contexts used by supported game builds.
local function actionHash(tableName,key,label)
 local rows=GameInfo and GameInfo[tableName];local kind=type(rows)
 assert(kind=='table' or kind=='userdata','ACTIVITY_'..label..'_TABLE_UNAVAILABLE')
 local row=rows[key];kind=type(row)
 assert(kind=='table' or kind=='userdata','ACTIVITY_'..label..'_ROW_UNAVAILABLE')
 local hash=row.Hash
 assert(type(hash)=='number' and hash==hash and hash>-math.huge and hash<math.huge and hash%1==0,
  'ACTIVITY_'..label..'_HASH_UNAVAILABLE')
 return hash
end
-- A single historical observation, not a permission or state authority. All extra
-- reads are protected independently; no unit objects or history are retained.
local function diagnosticText(v)
 local kind=type(v)
 if kind~='nil' and kind~='boolean' and kind~='number' and kind~='string' then return '('..kind..')' end
 return (tostring(v):gsub('[%c%[%]]',' ')..' ('..kind..')'):sub(1,100)
end
local function observe(fn)
 local ok,v=pcall(fn)
 if not ok then return ('UNKNOWN: '..detail(v):gsub('[%[%]]',' ')):sub(1,100),nil end
 return diagnosticText(v),v
end
local function captureDiagnostic(n,u,activity)
 local d={owner=n.owner,unitID=n.unitID,teamKey=n.teamKey,activityKey=n.activityKey,
  expectedName=n.expectedName,x=n.x,y=n.y,turn=Game.GetCurrentGameTurn(),
  activity=diagnosticText(activity),awake=diagnosticText(ActivityTypes.ACTIVITY_AWAKE),
  hold=diagnosticText(ActivityTypes.ACTIVITY_HOLD),sleep=diagnosticText(ActivityTypes.ACTIVITY_SLEEP),
  operationEnum=diagnosticText(ActivityTypes.ACTIVITY_OPERATION)}
 d.ready=observe(function()
  assert(type(u.IsReadyToMove)=='function','READINESS_READER_UNAVAILABLE');return u:IsReadyToMove()
 end)
 d.operation=observe(function()return u:GetSpyOperation()end)
 d.endTurn=observe(function()
  assert(type(u.GetSpyOperationEndTurn)=='function','SPY_END_TURN_READER_UNAVAILABLE');return u:GetSpyOperationEndTurn()
 end)
 local hash;d.hash,hash=observe(function()return actionHash('UnitOperations','UNITOPERATION_SLEEP','SLEEP')end)
 local allowed
 d.eligibility,allowed=observe(function()
  assert(hash~=nil,'SLEEP_HASH_UNAVAILABLE')
  assert(type(UnitManager.CanStartOperation)=='function','SLEEP_ELIGIBILITY_READER_UNAVAILABLE')
  return UnitManager.CanStartOperation(u,hash,nil,false,false)
 end)
 d.eligibilityStatus=allowed==true and 'ALLOWED' or (allowed==false and 'DENIED' or 'UNKNOWN')
 -- A reentrant publication may have changed the target during a reader call.
 if same(view(),n) then ExposedMembers.SPC_ExpeditionActivityDiagnostic=d end
end
-- Preserve the exact failing evaluation separately from the first startup sample.
-- This observes existing control flags; an attempted request is not native acceptance.
local function captureFailureDiagnostic(n,activity,awake,hold,sleep,timeout)
 if seen.failureDiagnosed or not same(view(),n)then return end
 seen.failureDiagnosed=true
 local operation=ActivityTypes.ACTIVITY_OPERATION
 if timeout then operation=n.sampleOperation end
 local d={owner=n.owner,unitID=n.unitID,teamKey=n.teamKey,activityKey=n.activityKey,
  expectedName=n.expectedName,x=n.x,y=n.y,turn=Game.GetCurrentGameTurn(),
  reason=timeout and 'ACTIVITY_SLEEP_TIMEOUT' or 'ACTIVITY_UNEXPECTED_STATE',
  phase=timeout and 'PENDING_TIMEOUT' or ((n.requested==true or seen.attempted==true) and 'POST_REQUEST_READBACK' or 'PRE_REQUEST_GUARD'),
  activity=diagnosticText(activity),awake=diagnosticText(awake),hold=diagnosticText(hold),
  sleep=diagnosticText(sleep),operationEnum=diagnosticText(operation),
  equalsAwake=diagnosticText(activity==awake),equalsHold=diagnosticText(activity==hold),
  equalsSleep=diagnosticText(activity==sleep),equalsOperation=diagnosticText(activity==operation),
  requested=diagnosticText(n.requested==true),sleepAttempted=diagnosticText(seen.attempted==true)}
 if timeout then
  d.elapsed=diagnosticText(n.elapsed);d.sampledElapsed=diagnosticText(n.sampledElapsed)
  d.sampleTurn=n.sampleTurn
 end
 if same(view(),n)then ExposedMembers.SPC_ExpeditionActivityFailureDiagnostic=d end
end
local function clearStaleDiagnostic(v,key)
 local d=ExposedMembers and ExposedMembers[key]
 if not d then return end
 if type(v)~='table' or v.owner~=Game.GetLocalPlayer() or v.owner~=d.owner or v.unitID~=d.unitID
  or v.teamKey~=d.teamKey or v.activityKey~=d.activityKey or v.expectedName~=d.expectedName
  or v.x~=d.x or v.y~=d.y or v.phase=='ENDED' then
  ExposedMembers[key]=nil
 end
end
local function evaluate(n)
 local ok,u,activity=pcall(read,n)
 if not ok then fail(n,u);return end
 if not u then return end -- Initial placement still invisible in this UI context.
 if job==n and not n.watching then watch(n)end -- Existing native-activity handling starts only after agreement.
 if n.mode=='ASLEEP' then
  if activity~=ActivityTypes.ACTIVITY_SLEEP then fail(n,'ACTIVITY_UNEXPECTED_WAKE')end
  return
 end
 if n.mode=='RECOVER' then
  -- Saved intent never substitutes for actual activity. No eligibility/writer
  -- calls here; Gameplay decides how the preserved phase continues.
  if activity==ActivityTypes.ACTIVITY_SLEEP then acknowledge(n,'RECOVERED',nil,true,false)
  elseif activity==ActivityTypes.ACTIVITY_AWAKE or activity==ActivityTypes.ACTIVITY_HOLD then acknowledge(n,'RECOVERED',nil,false,true)
  elseif activity~=ActivityTypes.ACTIVITY_OPERATION then fail(n,'ACTIVITY_RECOVERY_STATE_UNKNOWN')end
  return
 end
 if n.mode=='SLEEP' or n.mode=='ARMED' then
  if not seen.diagnosed then
   seen.diagnosed=true
   local captured,err=pcall(captureDiagnostic,n,u,activity)
   if not captured then print('[SPC][B192][ACTIVITY_DIAGNOSTIC_UNAVAILABLE] '..detail(err))end
   if job~=n or not same(view(),n)then return end
  end
  local sleep=ActivityTypes.ACTIVITY_SLEEP
  if activity==sleep then
   if n.mode=='SLEEP'then n.owned=false end -- Pre-existing Sleep is never acquired.
   acknowledge(n,'ASLEEP');return
  end
  -- Native OPERATION after our own request is pending, never proof of Sleep.
  -- Reuse the existing deadline; do not request again or start the Gameplay timer.
  if n.requested==true and n.owned==true and seen.attempted==true
   and activity==ActivityTypes.ACTIVITY_OPERATION then return end
  local awake,hold=ActivityTypes.ACTIVITY_AWAKE,ActivityTypes.ACTIVITY_HOLD
  if activity~=awake and activity~=hold then
   local captured,err=pcall(captureFailureDiagnostic,n,activity,awake,hold,sleep)
   if not captured then print('[SPC][B193][ACTIVITY_FAILURE_DIAGNOSTIC_UNAVAILABLE] '..detail(err))end
   fail(n,'ACTIVITY_UNEXPECTED_STATE');return
  end
  if not n.requested then
   local allowed,hash=pcall(function()
    local hash=actionHash('UnitOperations','UNITOPERATION_SLEEP','SLEEP')
    assert(type(UnitManager.CanStartOperation)=='function' and type(UnitManager.RequestOperation)=='function','ACTIVITY_SLEEP_API_UNAVAILABLE')
    assert(UnitManager.CanStartOperation(u,hash,nil,false,false)==true,'ACTIVITY_SLEEP_NOT_ALLOWED')
    return hash
   end)
   if not allowed then fail(n,hash);return end
   if job~=n or not same(view(),n)then return end
   if n.mode=='SLEEP' then
    -- The durable Gate must confirm this intent before the native writer runs.
    -- A lost/failed acknowledgement cannot authorize a best-effort Sleep.
    seen.armRequested=true;n.owned=true;acknowledge(n,'ARMED',nil,false,true);return
   end
   if not seen.armRequested then fail(n,'ACTIVITY_ARM_ACK_NOT_OBSERVED');return end
   n.requested=true;n.owned=true;seen.attempted=true -- Preserve the attempt until this activity key ends.
   local sent,err=pcall(function()
    assert(UnitManager.RequestOperation(u,hash)~=false,'ACTIVITY_SLEEP_REJECTED')
   end)
   if not sent then fail(n,err);return end
  end
 elseif n.mode=='RELEASE' then
  -- Cancellation can precede the Gameplay acknowledgement. Only this UI lease knows
  -- whether a sleep was attempted; never wake a pre-existing, unowned sleep.
  if not n.owned then acknowledge(n,'RELEASED');return end
  if activity==ActivityTypes.ACTIVITY_AWAKE or activity==ActivityTypes.ACTIVITY_HOLD then
   -- Awake is not proof that an attempted, unobserved operation cannot still arrive.
   if seen.attempted and not seen.sleepObserved then fail(n,'ACTIVITY_SLEEP_OUTCOME_UNKNOWN');return end
   acknowledge(n,'RELEASED');return
  end
  if activity~=ActivityTypes.ACTIVITY_SLEEP then fail(n,'ACTIVITY_RELEASE_STATE_UNKNOWN');return end
  if not n.requested then
   local allowed,hash=pcall(function()
    local hash=actionHash('UnitCommands','UNITCOMMAND_WAKE','WAKE')
    assert(type(UnitManager.CanStartCommand)=='function' and type(UnitManager.RequestCommand)=='function','ACTIVITY_WAKE_API_UNAVAILABLE')
    assert(UnitManager.CanStartCommand(u,hash,false)==true,'ACTIVITY_WAKE_NOT_ALLOWED')
    return hash
   end)
   if not allowed then fail(n,hash);return end
   n.requested=true
   local sent,err=pcall(function()
    assert(UnitManager.RequestCommand(u,hash)~=false,'ACTIVITY_WAKE_REJECTED')
   end)
   if not sent then fail(n,err);return end
  end
 end
 -- A synchronous writer may have published/reentered; recheck the current lease before readback.
 if job~=n or not same(view(),n)then return end
 local readOK,_,after=pcall(read,n)
 if not readOK then fail(n,_);return end
 if (n.mode=='SLEEP' or n.mode=='ARMED') and after==ActivityTypes.ACTIVITY_SLEEP then acknowledge(n,'ASLEEP')
 elseif n.mode=='RELEASE' and (after==ActivityTypes.ACTIVITY_AWAKE or after==ActivityTypes.ACTIVITY_HOLD)then acknowledge(n,'RELEASED')end
end
watch=function(n)
 n.watching=true
 ContextPtr:SetUpdate(function(dt)
  if stopped or job~=n then return end
  n.elapsed=n.elapsed+dt;n.poll=n.poll+dt
  if not same(view(),n)then cancel();pump(false);return end
  if n.poll>=0.25 then n.poll=0;pump(false)end
  if job==n and n.elapsed>=10 then
   if n.mode=='SLEEP' or n.mode=='ARMED' then
    local captured,err=pcall(captureFailureDiagnostic,n,n.lastActivity,n.sampleAwake,n.sampleHold,n.sampleSleep,true)
    if not captured then print('[SPC][B194][ACTIVITY_TIMEOUT_DIAGNOSTIC_UNAVAILABLE] '..detail(err))end
   end
   fail(n,'ACTIVITY_'..(n.mode=='ARMED' and 'SLEEP' or n.mode)..'_TIMEOUT')
  end
 end)
end
local function start(v)
 local n={revision=v.revision,owner=v.owner,unitID=v.unitID,expectedName=v.expectedName,
  x=v.x,y=v.y,teamKey=v.teamKey,activityKey=v.activityKey,mode=v.mode,phase=v.phase,
  owned=v.owned==true or (v.mode~='RECOVER' and v.releasePending==true and seen.attempted==true),
  publishedOwned=v.owned==true,releasePending=v.releasePending==true,elapsed=0,poll=0}
 job=n
 if n.mode~='SLEEP' or n.phase~='TASK_PREPARING' or n.owned or seen.attempted or seen.positionReady then watch(n)end

 return n
end
local function refresh(monitor)
 local v=view()
 clearStaleDiagnostic(v,'SPC_ExpeditionActivityDiagnostic')
 clearStaleDiagnostic(v,'SPC_ExpeditionActivityFailureDiagnostic')
 if type(v)=='table' and integer(v.revision) and v.revision~=lastRevision then
  lastRevision=v.revision
  if LuaEvents and LuaEvents.SPC_ExpeditionActivityChanged then LuaEvents.SPC_ExpeditionActivityChanged(v.revision)end
 end
 if not supported(v)then cancel();return end
 if seen.key~=v.activityKey then seen={key=v.activityKey};cancel()end
 if v.mode=='ASLEEP' then
  cancel()
  if monitor and not seen.monitor then
   evaluate({owner=v.owner,unitID=v.unitID,expectedName=v.expectedName,x=v.x,y=v.y,
    teamKey=v.teamKey,activityKey=v.activityKey,mode=v.mode,phase=v.phase,owned=v.owned==true,
    publishedOwned=v.owned==true,releasePending=v.releasePending==true})
  end
  return
 end
 if v.mode~='SLEEP' and v.mode~='ARMED' and v.mode~='RECOVER' and v.mode~='RELEASE' then cancel();return end
 if v.mode=='RELEASE' and v.owned~=true and v.releasePending~=true then cancel();return end
 if seen[v.mode]then cancel();return end
 if not job or not same(v,job)then cancel();start(v)end
 evaluate(job)
end
pump=function(monitor)
 if stopped then return end
 if busy then queued=true;queuedMonitor=queuedMonitor or monitor;return end
 busy=true
 local ok,err=pcall(function()
  local rounds=0
  repeat
   queued=false;local shouldMonitor=monitor or queuedMonitor;queuedMonitor=false
   refresh(shouldMonitor);monitor=false;rounds=rounds+1
  until not queued or rounds>=4
 end)
 busy=false
 if not ok then
  local n=job
  if n then fail(n,err)else print('[SPC][B191][ACTIVITY_READ_FAILED] '..detail(err))end
 end
end
local function published()pump(false)end
local function activityChanged(pid,id)
 local v=view()
 if supported(v) and pid==v.owner and id==v.unitID then pump(true)end
end
local function turn()
 -- Re-read at the player-turn event; unresolved placement cannot silently carry on.
 -- This is a lifecycle event boundary, not an elapsed-time or event-count timeout.
 pump(true)
 local n=job
 if n and n.positionPending and same(view(),n)then
  positionLog(n,'TURN_BOUNDARY_STOP');fail(n,'ACTIVITY_POSITION_UNCONFIRMED_AT_TURN '..positionDetail(n));return
 end
end
local function initialize()
 if initialized then return end
 initialized=true;stopped=false
 ExposedMembers.SPC_ExpeditionActivityDiagnostic=nil
 ExposedMembers.SPC_ExpeditionActivityFailureDiagnostic=nil
 Events.GameCoreEventPublishComplete.Add(published)
 Events.LocalPlayerTurnBegin.Add(turn)
 if Events.UnitActivityChanged then Events.UnitActivityChanged.Add(activityChanged)end
 if Events.UnitMoveComplete then Events.UnitMoveComplete.Add(activityChanged)end
 pump(true)
end
ContextPtr:SetInitHandler(initialize)
ContextPtr:SetShutdown(function()
 stopped=true;cancel()
 ExposedMembers.SPC_ExpeditionActivityDiagnostic=nil
 ExposedMembers.SPC_ExpeditionActivityFailureDiagnostic=nil
 if initialized then
  Events.GameCoreEventPublishComplete.Remove(published)
  Events.LocalPlayerTurnBegin.Remove(turn)
  if Events.UnitActivityChanged then Events.UnitActivityChanged.Remove(activityChanged)end
  if Events.UnitMoveComplete then Events.UnitMoveComplete.Remove(activityChanged)end
 end
 initialized=false
end)
