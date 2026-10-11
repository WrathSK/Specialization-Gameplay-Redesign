-- B190: invisible UI bridge for one Gameplay-owned Expedition activity lease.
-- No persistent state, native espionage mission, or dependency on the management window.
include('Probe')
local P=SPCP0
local KIND='UNIT_SPC_EXPEDITION_SPY'
local initialized=false;local stopped=false;local busy=false;local queued=false;local queuedMonitor=false
local job;local seen={};local lastRevision
local pump
local function detail(err)return tostring(err):gsub('[%c]',' '):sub(1,180)end
local function view()return ExposedMembers and ExposedMembers.SPC_ExpeditionActivity end
local function integer(v)return type(v)=='number' and v>=0 and v%1==0 end
local function same(v,n)
 return v and v.owner==n.owner and v.unitID==n.unitID and v.activityKey==n.activityKey
  and v.teamKey==n.teamKey and v.mode==n.mode and v.expectedName==n.expectedName
  and v.x==n.x and v.y==n.y
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
local function read(n)
 assert(Game.GetLocalPlayer()==n.owner and P.IsTestPlayer(n.owner),'ACTIVITY_LOCAL_OWNER_CHANGED')
 local p=Players[n.owner];assert(p and p.GetUnits,'ACTIVITY_PLAYER_UNREADABLE')
 local u=p:GetUnits():FindID(n.unitID)
 assert(u and u:GetID()==n.unitID and u:GetOwner()==n.owner,'ACTIVITY_EXACT_UNIT_CHANGED')
 local row=GameInfo.Units[u:GetUnitType()]
 assert(row and row.UnitType==KIND,'ACTIVITY_UNIT_TYPE_CHANGED')
 assert(type(u.GetName)=='function' and u:GetName()==n.expectedName,'ACTIVITY_NAME_CHANGED')
 assert(u:GetX()==n.x and u:GetY()==n.y,'ACTIVITY_POSITION_CHANGED')
 assert(type(u.GetSpyOperation)=='function' and u:GetSpyOperation()==-1,'ACTIVITY_NATIVE_MISSION_OR_UNREADABLE')
 assert(UnitManager and type(UnitManager.GetActivityType)=='function' and ActivityTypes,'ACTIVITY_READER_UNAVAILABLE')
 local activity=UnitManager.GetActivityType(u)
 assert(activity~=nil,'ACTIVITY_UNREADABLE')
 if activity==ActivityTypes.ACTIVITY_SLEEP and seen.key==n.activityKey then seen.sleepObserved=true end
 return u,activity
end
local function acknowledge(n,result,reason)
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
 local ok,err=pcall(function()
  assert(UI and type(UI.RequestPlayerOperation)=='function' and PlayerOperations,'ACTIVITY_REQUEST_UNAVAILABLE')
  UI.RequestPlayerOperation(n.owner,PlayerOperations.EXECUTE_SCRIPT,args)
 end)
 if not ok then
  -- The request may already have executed: never retry or submit another native operation.
  print('[SPC][B190][ACTIVITY_ACK_UNKNOWN] '..detail(err))
 end
end
local function fail(n,err)acknowledge(n,'FAILED',err)end
local function evaluate(n)
 local ok,u,activity=pcall(read,n)
 if not ok then fail(n,u);return end
 if n.mode=='ASLEEP' then
  if activity~=ActivityTypes.ACTIVITY_SLEEP then fail(n,'ACTIVITY_UNEXPECTED_WAKE')end
  return
 end
 if n.mode=='SLEEP' then
  if activity==ActivityTypes.ACTIVITY_SLEEP then acknowledge(n,'ASLEEP');return end
  if activity~=ActivityTypes.ACTIVITY_AWAKE and activity~=ActivityTypes.ACTIVITY_HOLD then
   fail(n,'ACTIVITY_UNEXPECTED_STATE');return
  end
  if not n.requested then
   local allowed,why=pcall(function()
    assert(UnitOperationTypes and UnitOperationTypes.SLEEP and OperationResultsTypes and OperationResultsTypes.NO_TARGETS,'ACTIVITY_SLEEP_CONSTANTS_UNAVAILABLE')
    assert(type(UnitManager.CanStartOperation)=='function' and type(UnitManager.RequestOperation)=='function','ACTIVITY_SLEEP_API_UNAVAILABLE')
    assert(UnitManager.CanStartOperation(u,UnitOperationTypes.SLEEP,nil,false,OperationResultsTypes.NO_TARGETS)==true,'ACTIVITY_SLEEP_NOT_ALLOWED')
   end)
   if not allowed then fail(n,why);return end
   n.requested=true;n.owned=true;seen.attempted=true -- Preserve the attempt until this activity key ends.
   local sent,err=pcall(function()
    assert(UnitManager.RequestOperation(u,UnitOperationTypes.SLEEP)~=false,'ACTIVITY_SLEEP_REJECTED')
   end)
   if not sent then fail(n,err);return end
  end
 elseif n.mode=='RELEASE' then
  -- Cancellation can precede the Gameplay acknowledgement. Only this UI lease knows
  -- whether a sleep was attempted; never wake a pre-existing, unowned sleep.
  if n.releasePending and not n.owned then acknowledge(n,'RELEASED');return end
  if activity==ActivityTypes.ACTIVITY_AWAKE or activity==ActivityTypes.ACTIVITY_HOLD then
   -- Awake is not proof that an attempted, unobserved operation cannot still arrive.
   if seen.attempted and not seen.sleepObserved then fail(n,'ACTIVITY_SLEEP_OUTCOME_UNKNOWN');return end
   acknowledge(n,'RELEASED');return
  end
  if activity~=ActivityTypes.ACTIVITY_SLEEP then fail(n,'ACTIVITY_RELEASE_STATE_UNKNOWN');return end
  if not n.requested then
   local allowed,why=pcall(function()
    assert(UnitCommandTypes and UnitCommandTypes.WAKE,'ACTIVITY_WAKE_CONSTANT_UNAVAILABLE')
    assert(type(UnitManager.CanStartCommand)=='function' and type(UnitManager.RequestCommand)=='function','ACTIVITY_WAKE_API_UNAVAILABLE')
    assert(UnitManager.CanStartCommand(u,UnitCommandTypes.WAKE,false)==true,'ACTIVITY_WAKE_NOT_ALLOWED')
   end)
   if not allowed then fail(n,why);return end
   n.requested=true
   local sent,err=pcall(function()
    assert(UnitManager.RequestCommand(u,UnitCommandTypes.WAKE)~=false,'ACTIVITY_WAKE_REJECTED')
   end)
   if not sent then fail(n,err);return end
  end
 end
 -- A synchronous writer may have published/reentered; recheck the current lease before readback.
 if job~=n or not same(view(),n)then return end
 local readOK,_,after=pcall(read,n)
 if not readOK then fail(n,_);return end
 if n.mode=='SLEEP' and after==ActivityTypes.ACTIVITY_SLEEP then acknowledge(n,'ASLEEP')
 elseif n.mode=='RELEASE' and (after==ActivityTypes.ACTIVITY_AWAKE or after==ActivityTypes.ACTIVITY_HOLD)then acknowledge(n,'RELEASED')end
end
local function start(v)
 local n={revision=v.revision,owner=v.owner,unitID=v.unitID,expectedName=v.expectedName,
  x=v.x,y=v.y,teamKey=v.teamKey,activityKey=v.activityKey,mode=v.mode,
  owned=v.owned==true or (v.releasePending==true and seen.attempted==true),
  releasePending=v.releasePending==true,elapsed=0,poll=0}
 job=n
 ContextPtr:SetUpdate(function(dt)
  if stopped or job~=n then return end
  n.elapsed=n.elapsed+dt;n.poll=n.poll+dt
  if not same(view(),n)then cancel();pump(false);return end
  if n.poll>=0.25 then n.poll=0;pump(false)end
  if job==n and n.elapsed>=10 then fail(n,'ACTIVITY_'..n.mode..'_TIMEOUT')end
 end)
 return n
end
local function refresh(monitor)
 local v=view()
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
    teamKey=v.teamKey,activityKey=v.activityKey,mode=v.mode,owned=v.owned==true})
  end
  return
 end
 if v.mode~='SLEEP' and v.mode~='RELEASE' then cancel();return end
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
  if n then fail(n,err)else print('[SPC][B190][ACTIVITY_READ_FAILED] '..detail(err))end
 end
end
local function published()pump(false)end
local function activityChanged(pid,id)
 local v=view()
 if supported(v) and pid==v.owner and id==v.unitID then pump(true)end
end
local function turn()pump(true)end
local function initialize()
 if initialized then return end
 initialized=true;stopped=false
 Events.GameCoreEventPublishComplete.Add(published)
 Events.LocalPlayerTurnBegin.Add(turn)
 if Events.UnitActivityChanged then Events.UnitActivityChanged.Add(activityChanged)end
 pump(true)
end
ContextPtr:SetInitHandler(initialize)
ContextPtr:SetShutdown(function()
 stopped=true;cancel()
 if initialized then
  Events.GameCoreEventPublishComplete.Remove(published)
  Events.LocalPlayerTurnBegin.Remove(turn)
  if Events.UnitActivityChanged then Events.UnitActivityChanged.Remove(activityChanged)end
 end
 initialized=false
end)
