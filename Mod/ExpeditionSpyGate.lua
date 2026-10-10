-- B185: native Spy travel, marker-proved continuity, independent no-reward timer.
-- Only this unit gets a probe marker. No city/player ledger, native mission or reward.
-- Marker survival across engine travel is a native gate; missing/ambiguous proof stops.
SPCExpeditionSpyGate={KIND='UNIT_SPC_EXPEDITION_SPY',LEGACY='UNIT_SPC_EXPEDITION_GATE',ZERO='UNIT_SPC_EXPEDITION_ZERO',MARKER='SPC_N1_SPY_PROBE_ID'}
function SPCExpeditionSpyGate.Start(P,shared)
 local M=SPCExpeditionSpyGate
 local state={};local busy=false;local mutating=false;local lastToken;local lastReply;local step='REQUEST'
 local function int(n)return type(n)=='number' and n==n and n>=0 and n<math.huge and n%1==0 end
 local function flag(v)return v==true or v==1 end
 local function row(u)return u and P.Info('Units',u:GetType())end
 local function list(pid)
  local out={}
  for _,u in Players[pid]:GetUnits():Members()do
   local r=row(u)
   if r and (r.UnitType==M.KIND or r.UnitType==M.LEGACY or r.UnitType==M.ZERO)then out[#out+1]=u end
  end
  return out
 end
 local function owned(pid,id,allowLegacy)
  local u=Players[pid]:GetUnits():FindID(id);local r=row(u)
  assert(u and u:GetID()==id and u:GetOwner()==pid and r and (r.UnitType==M.KIND or allowLegacy and (r.UnitType==M.LEGACY or r.UnitType==M.ZERO)),'TEST_TEAM_CHANGED')
  return u
 end
 local function occupants(x,y)
  assert(Units and type(Units.GetUnitsInPlot)=='function','OCCUPANTS_UNAVAILABLE')
  local native=Units.GetUnitsInPlot(x,y);assert(type(native)=='table','OCCUPANTS_UNAVAILABLE')
  local out={}
  for _,u in pairs(native)do
   assert(#out<64,'OCCUPANTS_UNAVAILABLE')
   out[#out+1]={owner=u:GetOwner(),id=u:GetID(),kind=u:GetType(),x=u:GetX(),y=u:GetY()}
  end
  return out
 end
 local function unchangedOthers(before)
  for _,a in ipairs(before)do
   local p=Players[a.owner];local u=p and p:GetUnits():FindID(a.id)
   assert(u and u:GetOwner()==a.owner and u:GetType()==a.kind and u:GetX()==a.x and u:GetY()==a.y,'OTHER_UNIT_CHANGED_STOP')
  end
 end
 local function source()
  local c=Players[state.owner]:GetCities():FindID(state.sourceCity)
  assert(c and c:GetOwner()==state.owner and type(state.sourceRef)=='string' and SPCNetworkInput.Reference(c)==state.sourceRef,'SOURCE_REFERENCE_CHANGED')
  return c
 end
 local function target(pid,t)
  step='TARGET'
  assert(type(t)=='table' and int(t.owner) and int(t.id) and int(t.x) and int(t.y),'TARGET_CHANGED')
  local p=Players[t.owner]
  assert(p and t.owner~=pid and p:IsMajor() and p:IsAlive(),'TARGET_CHANGED')
  assert(Players[pid]:GetDiplomacy():HasMet(t.owner),'TARGET_CHANGED')
  local cities=p:GetCities();local c=cities:FindID(t.id)
  assert(c and c:GetOwner()==t.owner and c:GetX()==t.x and c:GetY()==t.y,'TARGET_CHANGED')
  -- City:IsCapital is UI-only. Gameplay reads the player's current capital.
  step='CAPITAL'
  assert(type(cities.GetCapitalCity)=='function','CAPITAL_API_UNAVAILABLE')
  local capital=cities:GetCapitalCity()
  assert(capital and capital:GetOwner()==t.owner and capital:GetID()==c:GetID()
   and capital:GetX()==t.x and capital:GetY()==t.y,'TARGET_CHANGED')
  step='TARGET'
  local vis=PlayersVisibility and PlayersVisibility[pid]
  assert(vis and vis:IsRevealed(t.x,t.y),'TARGET_UNKNOWN')
  return c -- Capital/revealed restriction belongs only to this bounded fixture.
 end
 local function reason(err)
  return tostring(err):match(':%d+:%s*([A-Z][A-Z0-9_]+)') or tostring(err):match('^([A-Z][A-Z0-9_]+)') or 'API_UNAVAILABLE'
 end
 local function detail(err)
  return tostring(err):gsub('[%c]',' '):gsub('%[','('):gsub('%]',')'):sub(1,220)
 end
 local function logFailure(code,at,raw)
  print('[SPC][B185][N1_SPY_ERROR] step='..at..' code='..code..' detail='..raw)
 end
 local function hold(err)
  state.phase='HELD';state.stop=reason(err);state.errorStep=step;state.errorDetail=detail(err)
  logFailure(state.stop,state.errorStep,state.errorDetail)
 end
 local function marked(u)
  local r=row(u)
  return u and u:GetOwner()==state.owner and r and r.UnitType==M.KIND
   and type(u.GetProperty)=='function' and u:GetProperty(M.MARKER)==state.marker and state.marker~=nil
 end
 local function tracked()
  local u=owned(state.owner,state.unitID)
  assert(marked(u),'TEAM_MARKER_UNAVAILABLE');return u
 end
 local function observe(allowTaskCompletion)
  if not state.unitID or state.phase=='ENDED' or state.phase=='HELD' then return end
  source()
  if state.phase=='TRAVELLING' then
   target(state.owner,state.target)
   -- Native FindID may return an object with a changed public ID. A matching ID,
   -- name or location is not continuity proof. Never copy a marker onto arrivals.
   local u=Players[state.owner]:GetUnits():FindID(state.unitID)
   if not (marked(u) and u:GetX()==state.target.x and u:GetY()==state.target.y) then
    u=nil
    for _,a in ipairs(occupants(state.target.x,state.target.y))do
     if a.owner==state.owner then
      local candidate=Players[state.owner]:GetUnits():FindID(a.id)
      if marked(candidate) then assert(not u,'TEAM_MARKER_AMBIGUOUS');u=candidate end
     end
    end
   end
   if u then
    -- One scan on the actual arrival transition, not a new per-turn player scan.
    local all=list(state.owner)
    assert(#all==1 and all[1]:GetID()==u:GetID() and marked(all[1]),'TEAM_MARKER_AMBIGUOUS')
    assert(u:GetX()==state.target.x and u:GetY()==state.target.y,'TARGET_CHANGED')
    local id=u:GetID();owned(state.owner,id)
    state.unitID=id;state.x=u:GetX();state.y=u:GetY();state.phase='ARRIVED'
    return
   end
   assert(Game.GetCurrentGameTurn()<=state.dueTurn+1,'NATIVE_IDENTITY_UNCONFIRMED')
   return
  end
  local u=tracked()
  assert(u:GetX()==state.x and u:GetY()==state.y,'TEAM_DISPLACED_STOP')
  if state.target then target(state.owner,state.target)end
  if state.phase=='TASK_RUNNING' then
   -- GetSpyOperation is established in UI, not assumed present in Gameplay.
   -- If exposed here, also reject a native mission; otherwise the no-reward
   -- fixture relies on the checked start sample + exact-type UI isolation.
   if type(u.GetSpyOperation)=='function' then assert(u:GetSpyOperation()==-1,'NATIVE_MISSION_ACTIVE_STOP')end
   if allowTaskCompletion and Game.GetCurrentGameTurn()>=state.taskDue then
    state.phase='TASK_COMPLETE';state.taskCompleted=Game.GetCurrentGameTurn()
    state.taskCompletions=1 -- One fixture task per team; completion has no effects.
    print('[SPC][B185][N1_TASK] complete=1 reward=NONE nativeMission=NONE')
   end
  end
 end
 local function snapshot(pid)
  if state.owner==pid then local ok,err=pcall(observe);if not ok then hold(err)end end
  local units=list(pid);local v={owner=pid,count=#units,turn=Game.GetCurrentGameTurn(),phase=state.phase or 'IDLE'}
  if #units==1 then
   local u=units[1];v.unitID=u:GetID();v.x=u:GetX();v.y=u:GetY();v.legacy=row(u).UnitType~=M.KIND
   v.unbound=not v.legacy and (state.owner~=pid or state.unitID~=u:GetID())
  end
  if state.owner==pid then
   for _,k in ipairs({'sourceCity','sourceName','startTurn','dueTurn','stop','nativeAllowed','nativeStatus','removedEvents','arrivalOthers','errorStep','errorDetail','taskStart','taskDue','taskCompleted','taskCompletions'})do
    -- A missing original unit must not be substituted by another discovered unit.
    v[k]=state[k]
   end
   v.createdID=state.createdID;v.trackedID=state.unitID;v.bound=false
   v.targetName=state.target and state.target.name
   if state.target then v.targetOwner=state.target.owner;v.targetID=state.target.id;v.targetX=state.target.x;v.targetY=state.target.y end
   if state.unitID then
    local u=Players[pid]:GetUnits():FindID(state.unitID);local r=row(u)
    v.sameUnit=u~=nil and u:GetID()==state.unitID and marked(u) or false
    v.bound=v.sameUnit and state.phase~='HELD';v.unbound=not v.bound
    if v.sameUnit then v.unitID=u:GetID();v.x=u:GetX();v.y=u:GetY()end
   end
   v.expectedX=state.x;v.expectedY=state.y
  end
  v.observedCount=v.count
  if state.owner==pid and state.unitID and state.phase~='ENDED' and not v.sameUnit then
   v.count=math.max(1,v.count);v.reservedCapacity=true
  end
  if v.unitID and not v.legacy and v.x>=0 and v.y>=0 then
   local ok,o=pcall(occupants,v.x,v.y)
   if ok then
    v.coLocated=0;for _,a in ipairs(o)do if a.owner~=pid or a.id~=v.unitID then v.coLocated=v.coLocated+1 end end
   else v.occupancyUnknown=true end
  end
  return v
 end
 local function handle(pid,p)
  assert(type(p)=='table' and type(p.Token)=='string' and #p.Token>0 and #p.Token<=100,'BAD_REQUEST')
  assert(P.IsTestPlayer(pid),'SUPPORTED_PLAYER_REQUIRED')
  assert(p.Action=='READ' or p.Action=='CREATE' or p.Action=='DISPATCH' or p.Action=='STOP' or p.Action=='TASK' or p.Action=='END','BAD_ACTION')
  step=p.Action
  if p.Action=='READ' then return snapshot(pid)end
  if p.Action=='CREATE' then
   assert(state.phase~='CREATING' and state.phase~='HELD' and (not state.unitID or state.phase=='ENDED'),'SPAWN_UNCERTAIN_NO_RETRY')
   assert(#list(pid)==0,'EXISTING_TEST_TEAM_COUNTS')
   local c=Players[pid]:GetCities():FindID(p.CityID)
   assert(c and c:GetOwner()==pid,'OWN_CITY_REQUIRED')
   local f=shared.EffectiveFacts.Read(pid,c)
   assert(f.specialization=='CULTURE' and f.active==4 and not f.investmentPending,'CULTURE_ACTIVE_IV_REQUIRED')
   assert(type(f.token)=='string' and #f.token>0 and c:GetProperty('SPC_DEV_BINDING_B013_TOKEN')==f.token,'SOURCE_REFERENCE_UNKNOWN')
   local r=P.Info('Units',M.KIND)
   assert(r and flag(r.Spy) and flag(r.IgnoreMoves) and flag(r.Stackable)
    and (r.CanRetreatWhenCaptured==false or r.CanRetreatWhenCaptured==0)
    and r.PromotionClass=='PROMOTION_CLASS_SPY','TEST_DATABASE_NOT_READY')
   local before=occupants(c:GetX(),c:GetY())
   mutating=true;state={owner=pid,phase='CREATING',sourceCity=c:GetID(),sourceName=c:GetName(),sourceRef=SPCNetworkInput.Reference(c),x=c:GetX(),y=c:GetY()}
   local u=UnitManager.InitUnit(pid,M.KIND,c:GetX(),c:GetY())
   assert(u and u:GetOwner()==pid,'SPAWN_UNCONFIRMED')
   state.unitID=u:GetID();state.createdID=state.unitID;owned(pid,state.unitID)
   assert(type(u.GetProperty)=='function' and type(u.SetProperty)=='function','TEAM_MARKER_API_UNAVAILABLE')
   assert(u:GetProperty(M.MARKER)==nil,'TEAM_MARKER_ALREADY_PRESENT')
   state.marker=p.Token..':'..state.sourceRef..':'..state.createdID
   u:SetProperty(M.MARKER,state.marker)
   assert(marked(u),'TEAM_MARKER_WRITE_UNCONFIRMED')
   assert(#list(pid)==1,'SPAWN_COUNT_UNCONFIRMED')
   assert(u:GetX()==state.x and u:GetY()==state.y,'EXACT_PLACEMENT_REJECTED')
   unchangedOthers(before);source();state.phase='CREATED'
  elseif p.Action=='DISPATCH' then
   assert(state.owner==pid and state.unitID==p.UnitID and (state.phase=='CREATED' or state.phase=='ARRIVED'),'BOUND_TEAM_REQUIRED')
   observe();local u=tracked()
   assert(state.phase~='HELD' and u:GetID()==p.UnitID,'BOUND_TEAM_REQUIRED')
   assert(p.SampleTurn==Game.GetCurrentGameTurn() and p.FromX==u:GetX() and p.FromY==u:GetY(),'STALE_TRAVEL_SAMPLE')
   assert(p.NativeStatus=='KNOWN' and p.NativeAllowed==true,'NATIVE_TRAVEL_NOT_ALLOWED')
   assert(int(p.Travel) and int(p.Establish) and p.Travel+p.Establish<=1000,'TRAVEL_TIME_UNKNOWN')
   local t={owner=p.TargetOwner,id=p.TargetID,x=p.TargetX,y=p.TargetY}
   local c=target(pid,t);t.name=c:GetName();step='DISPATCH'
   state.target=t;state.startTurn=Game.GetCurrentGameTurn();state.dueTurn=state.startTurn+p.Travel+p.Establish
   state.nativeAllowed=type(p.NativeAllowed)=='boolean' and p.NativeAllowed or false
   state.nativeStatus=p.NativeStatus=='KNOWN' and 'KNOWN' or 'UNKNOWN'
   mutating=true;state.phase='TRAVELLING';state.permit=p.Token
  elseif p.Action=='TASK' then
   assert(state.owner==pid and state.unitID==p.UnitID,'BOUND_TEAM_REQUIRED')
   observe();assert(state.phase=='ARRIVED' and not state.taskStart,'TASK_NOT_AVAILABLE')
   local u=tracked();target(pid,state.target)
   assert(p.SampleTurn==Game.GetCurrentGameTurn() and p.NativeOperation==-1,'NATIVE_OPERATION_UNKNOWN')
   if type(u.GetSpyOperation)=='function' then assert(u:GetSpyOperation()==-1,'NATIVE_MISSION_ACTIVE_STOP')end
   -- Fixed two player-turn boundaries are a test fixture, not a new Design duration.
   mutating=true;state.taskStart=Game.GetCurrentGameTurn();state.taskDue=state.taskStart+2
   state.taskCompletions=0;state.phase='TASK_RUNNING'
  elseif p.Action=='STOP' then
   assert(state.owner==pid and state.unitID==p.UnitID and state.phase~='ENDED','BOUND_TEAM_REQUIRED')
   mutating=true;error('ISOLATION_OR_REQUEST_STOP: '..tostring(p.Detail or 'UNKNOWN'):sub(1,180))
  elseif p.Action=='END' then
   -- Explicit cleanup of the exact currently owned prototype, including an unbound loaded one.
   local u=owned(pid,p.UnitID,true)
   assert(#list(pid)==1,'SPAWN_COUNT_UNCONFIRMED')
   mutating=true;state.phase='ENDING'
   Players[pid]:GetUnits():Destroy(u)
   assert(not Players[pid]:GetUnits():FindID(p.UnitID) and #list(pid)==0,'END_UNCONFIRMED')
   state={phase='ENDED'}
  end
  local v=snapshot(pid)
  if p.Action=='DISPATCH' and state.phase=='TRAVELLING' then v.nativePermit=state.permit end
  return v
 end
 local data={};shared.ExpeditionGate=data
 function data.Request(pid,p)
  if not P.IsTestPlayer(pid) or type(p)~='table' or type(p.Token)~='string' or #p.Token==0 or #p.Token>100 then return end
  if busy then return end
  if p.Token==lastToken then ExposedMembers.SPC_ExpeditionGateReply=lastReply;return end
  busy=true;shared.RequestDepth=(shared.RequestDepth or 0)+1
  step='REQUEST';local ok,v=pcall(handle,pid,p)
  shared.RequestDepth=shared.RequestDepth-1;busy=false
  if not ok then
   local err=v;local failedStep=step;local raw=detail(err)
   if mutating then hold(err)end
   local readOK,result=pcall(snapshot,pid)
   v=readOK and result or {owner=pid,phase=state.phase or 'HELD',snapshotUnknown=true}
   v.error=state.stop or reason(err)
   v.errorStep=state.errorStep or failedStep;v.errorDetail=state.errorDetail or raw
   if not mutating then logFailure(v.error,v.errorStep,v.errorDetail)end
  end
  mutating=false
  v.token=p.Token;lastToken=p.Token;lastReply=v
  ExposedMembers.SPC_ExpeditionGateReply=v
  print('[SPC][B185][N1_SPY] action='..tostring(p.Action)..' owner='..pid..' unit='..tostring(v.unitID)..' phase='..v.phase..' error='..tostring(v.error))
 end
 GameEvents.SPC_ExpeditionGateRequest.Add(data.Request)
 function data.Turn(pid)
  if busy or not P.IsTestPlayer(pid) or state.owner~=pid or not state.unitID or state.phase=='HELD' or state.phase=='ENDED' then return end
  busy=true;shared.RequestDepth=(shared.RequestDepth or 0)+1
  step='TURN';local ok,err=pcall(function()
   observe(true)
  end)
  shared.RequestDepth=shared.RequestDepth-1;busy=false
  mutating=false;if not ok then hold(err)end
 end
 Events.PlayerTurnActivated.Add(data.Turn) -- Owned endpoints/unit; travelling adds one bounded destination-occupant read.
 if Events.CityTransfered then Events.CityTransfered.Add(function()
  if not busy and state.unitID and state.phase~='ENDED' and state.phase~='HELD' then
   step='REFERENCE';local ok,err=pcall(function()observe();if state.phase=='TRAVELLING' then target(state.owner,state.target)end end);if not ok then hold(err)end
  end
 end)end
 if Events.UnitRemovedFromMap then Events.UnitRemovedFromMap.Add(function(pid,id)
  if pid==state.owner and id==state.unitID then state.removedEvents=math.min(99,(state.removedEvents or 0)+1)end
 end)end
end
