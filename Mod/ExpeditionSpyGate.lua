-- B190: session task owns native sleep only after explicit UI readback.
-- Source/capacity remain our own record; no city/player ledger, mission or reward.
-- Native name assignment and travel survival remain explicit user-game gates.
SPCExpeditionSpyGate={KIND='UNIT_SPC_EXPEDITION_SPY',LEGACY='UNIT_SPC_EXPEDITION_GATE',ZERO='UNIT_SPC_EXPEDITION_ZERO'}
function SPCExpeditionSpyGate.Start(P,shared)
 local M=SPCExpeditionSpyGate
 local serial=0;local state={};local busy=false;local mutating=false;local lastToken;local lastReply;local lastActivityToken;local lastActivityReply;local step='REQUEST'
 -- Scalar transition mirror, independent of explicit diagnostic snapshots.
 local revision=0;local published={}
 local function publishActivity()
  local v={owner=state.owner,unitID=state.unitID,expectedName=state.expectedName,x=state.x,y=state.y,
   teamKey=state.teamKey,activityKey=state.activityKey,phase=state.phase or 'IDLE',mode=state.activityMode or 'NONE',
   owned=state.activityOwned==true,releasePending=state.activityPending==true,taskStart=state.taskStart,taskDue=state.taskDue,
   taskCompleted=state.taskCompleted,taskCompletions=state.taskCompletions,error=state.stop}
  v.locked=v.mode~='NONE'
  local changed=false
  for k,value in pairs(v)do if published[k]~=value then changed=true;break end end
  if not changed then for k in pairs(published)do if k~='revision' and v[k]==nil then changed=true;break end end end
  if changed then revision=revision+1;v.revision=revision;published=v;ExposedMembers.SPC_ExpeditionActivity=v end
 end
 local function releaseActivity()
  if state.activityMode~='BLOCKED' then state.activityMode=(state.activityOwned or state.activityPending) and 'RELEASE' or 'NONE' end
 end
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
  print('[SPC][B190][N1_SPY_ERROR] step='..at..' code='..code..' detail='..raw)
 end
 local function hold(err)
  releaseActivity()
  state.phase='HELD';state.stop=reason(err);state.errorStep=step;state.errorDetail=detail(err)
  logFailure(state.stop,state.errorStep,state.errorDetail)
 end
 -- Compare raw engine names only; displayed/localized city text is never city authority.
 local function nameStatus(u)
  if not u then return 'NO_UNIT' end
  if not state.expectedName then return 'NO_SESSION' end
  local ok,value=pcall(function()
   local r=row(u)
   if u:GetOwner()~=state.owner or not r or r.UnitType~=M.KIND then return 'WRONG_UNIT' end
   if type(u.GetName)~='function' then return 'UNREADABLE' end
   local value=u:GetName()
   if value==nil or value=='' then return 'ABSENT' end
   return value==state.expectedName and 'MATCH' or 'MISMATCH'
  end)
  return ok and value or 'UNREADABLE'
 end
 local function named(u)return nameStatus(u)=='MATCH' end
 local function namePool(pid)
  local config=PlayerConfigurations and PlayerConfigurations[pid]
  assert(config and type(config.GetCivilizationTypeName)=='function','NAME_CIVILIZATION_UNAVAILABLE')
  local civ=config:GetCivilizationTypeName()
  assert(civ=='CIVILIZATION_SPC_TEST','NAME_TEST_CIVILIZATION_REQUIRED')
  assert(GameInfo and GameInfo.CivilizationCitizenNames,'NAME_POOL_UNAVAILABLE')
  local names={};local count=0
  for r in GameInfo.CivilizationCitizenNames()do
   if r.CivilizationType==civ then
    assert(type(r.CitizenName)=='string' and #r.CitizenName>0,'NAME_POOL_INVALID')
    if not names[r.CitizenName]then names[r.CitizenName]=true;count=count+1 end
   end
  end
  assert(count>0,'NAME_POOL_EMPTY')
  return names,count,civ
 end
 local function acceptName(pid,p)
  assert(state.owner==pid and state.unitID==p.UnitID and
   (state.phase=='NAMING' or state.phase=='CREATED'),'BOUND_TEAM_REQUIRED')
  assert(p.NameOffmapChecked==true and p.NameSampleTurn==Game.GetCurrentGameTurn(),'NAME_UI_SAMPLE_REQUIRED')
  source();local u=owned(pid,state.unitID)
  assert(u:GetX()==state.x and u:GetY()==state.y,'TEAM_DISPLACED_STOP')
  local names,count,civ=namePool(pid);local r=row(u)
  assert(type(p.Name)=='string' and #p.Name>0 and #p.Name<=220,'TEAM_NAME_INVALID')
  assert(type(r.Name)=='string' and p.Name~=r.Name and p.Name~=Locale.Lookup(r.Name),'TEAM_NAME_DEFAULT')
  if not names[p.Name]then
   local matches=0
   for key in pairs(names)do if Locale.Lookup(key)==p.Name then matches=matches+1 end end
   assert(matches>0,'TEAM_NAME_NOT_IN_POOL');assert(matches==1,'TEAM_NAME_AMBIGUOUS')
  end
  assert(type(u.GetName)=='function' and u:GetName()==p.Name,'TEAM_NAME_UNAVAILABLE')
  -- Explicit confirmation only. Include every visible same-owner unit, while
  -- the UI separately checks native off-map Spy records before sending NAME.
  -- Our single session reservation blocks another custom creation while absent.
  assert(#list(pid)==1,'TEAM_NAME_AMBIGUOUS')
  for _,other in Players[pid]:GetUnits():Members()do
   if other:GetID()~=state.unitID then
    assert(type(other.GetName)=='function','TEAM_NAME_UNREADABLE')
    assert(other:GetName()~=p.Name,'TEAM_NAME_AMBIGUOUS')
   end
  end
  assert(not state.nameVerified or state.expectedName==p.Name,'TEAM_NAME_CHANGED')
  state.expectedName=p.Name;state.namePoolCount=count;state.namePoolCivilization=civ
  state.nameVerified=true;state.phase='CREATED'
 end
 local function lookupStatus(id)
  if not id then return nil,'NO_UNIT' end
  local ok,u=pcall(function()return Players[state.owner]:GetUnits():FindID(id)end)
  if not ok then return nil,'UNREADABLE' end
  if not u then return nil,'NO_UNIT' end
  local read,actual=pcall(function()return u:GetID()end)
  if not read then return nil,'UNREADABLE' end
  return actual,nameStatus(u)
 end
 local function tracked()
  local u=owned(state.owner,state.unitID)
  assert(named(u),'TEAM_NAME_UNAVAILABLE');return u
 end
 local function observe(allowTaskCompletion,knownUnits)
  if not state.unitID or state.phase=='ENDED' or state.phase=='HELD' then return end
  source()
  if state.phase=='NAMING' then
   local u=owned(state.owner,state.unitID)
   assert(u:GetX()==state.x and u:GetY()==state.y,'TEAM_DISPLACED_STOP')
   return -- Only an explicit UI observation + independent NAME check can accept.
  end
  if state.phase=='TRAVELLING' then
   target(state.owner,state.target)
   -- Spies need not appear in physical plot occupancy. Inspect the exact
   -- prototype collection; the observed native name is the bounded continuity candidate.
   -- Snapshot passes its one collection read; pending-turn checks read once.
   local all=knownUnits or list(state.owner);local candidate
   for _,u in ipairs(all)do
    if named(u) then assert(not candidate,'TEAM_NAME_AMBIGUOUS');candidate=u end
   end
   if candidate then
    assert(#all==1,'TEAM_NAME_AMBIGUOUS')
    if candidate:GetX()==state.target.x and candidate:GetY()==state.target.y then
     local id=candidate:GetID()
     -- Validate the actual exact-lookup object as well as the collection item.
     local current=owned(state.owner,id)
     assert(named(current),'TEAM_NAME_UNAVAILABLE')
     assert(current:GetX()==state.target.x and current:GetY()==state.target.y,'TARGET_CHANGED')
     state.unitID=id;state.x=current:GetX();state.y=current:GetY();state.phase='ARRIVED'
     return
    end
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
    releaseActivity()
    state.taskCompletions=1 -- One fixture task per team; completion has no effects.
    print('[SPC][B190][N1_TASK] complete=1 reward=NONE nativeMission=NONE')
   end
  end
 end
 local function snapshot(pid)
  local units=list(pid)
  if state.owner==pid then local ok,err=pcall(observe,false,units);if not ok then hold(err)end end
  local v={owner=pid,count=#units,turn=Game.GetCurrentGameTurn(),phase=state.phase or 'IDLE'}
  if #units==1 then
   local u=units[1];v.unitID=u:GetID();v.x=u:GetX();v.y=u:GetY();v.legacy=row(u).UnitType~=M.KIND
   v.unbound=not v.legacy and (state.owner~=pid or state.unitID~=u:GetID())
  end
  if state.owner==pid then
   for _,k in ipairs({'sourceCity','sourceName','startTurn','dueTurn','stop','nativeAllowed','nativeStatus','removedEvents','arrivalOthers','errorStep','errorDetail','taskStart','taskDue','taskCompleted','taskCompletions','activityMode','activityOwned','activityKey','expectedName','teamKey','nameVerified','namePoolCount','namePoolCivilization'})do
    -- A missing original unit must not be substituted by another discovered unit.
    v[k]=state[k]
   end
   v.createdID=state.createdID;v.trackedID=state.unitID;v.bound=false
   v.targetName=state.target and state.target.name
   if state.target then v.targetOwner=state.target.owner;v.targetID=state.target.id;v.targetX=state.target.x;v.targetY=state.target.y end
   if state.unitID then
    local ok,id,x,y=pcall(function()
     local u=owned(pid,state.unitID)
     if named(u) then return u:GetID(),u:GetX(),u:GetY()end
    end)
    v.sameUnit=ok and id==state.unitID or false
    v.bound=v.sameUnit and state.nameVerified==true and state.phase~='HELD';v.unbound=not v.bound
    if v.sameUnit then v.unitID=id;v.x=x;v.y=y end
   end
   v.expectedX=state.x;v.expectedY=state.y
  end
  v.observedCount=v.count
  if state.owner==pid and state.unitID and state.phase~='ENDED' and not v.sameUnit then
   v.count=math.max(1,v.count);v.reservedCapacity=true
  end
  -- Explicit snapshots only: bounded diagnostic scalars, no history or native writes.
  if state.owner==pid and state.unitID then
   local d={turn=v.turn,memberCount=#units,plotStatus='NO_UNIT'};v.identity=d
   d.createdLookupID,d.createdName=lookupStatus(state.createdID)
   d.trackedLookupID,d.trackedName=lookupStatus(state.unitID)
   d.sourceStatus=pcall(source) and 'MATCH' or 'UNREADABLE'
   if #units==1 then
    local u=units[1];d.candidateID=u:GetID();d.candidateName=nameStatus(u)
    d.candidateLookupID,d.lookupName=lookupStatus(d.candidateID)
    local ok,n=pcall(function()return u:GetName()end);if ok and type(n)=='string' then v.observedName=n:sub(1,220)end
   else
    d.candidateName=#units==0 and 'NO_UNIT' or 'AMBIGUOUS';d.lookupName=d.candidateName
   end
  end
  if v.unitID and not v.legacy and v.x>=0 and v.y>=0 then
   local ok,o=pcall(occupants,v.x,v.y)
   if ok then
    v.coLocated=0;local found=false
    for _,a in ipairs(o)do
     if a.owner==pid and a.id==v.unitID then found=true else v.coLocated=v.coLocated+1 end
    end
    if v.identity then v.identity.plotStatus=found and 'PRESENT' or 'ABSENT' end
   else
    v.occupancyUnknown=true;if v.identity then v.identity.plotStatus='UNREADABLE' end
   end
  elseif v.identity and v.unitID and v.x and v.y and (v.x<0 or v.y<0)then
   v.identity.plotStatus='OFF_MAP'
  end
  return v
 end
 local function handle(pid,p)
  assert(type(p)=='table' and type(p.Token)=='string' and #p.Token>0 and #p.Token<=100,'BAD_REQUEST')
  assert(P.IsTestPlayer(pid),'SUPPORTED_PLAYER_REQUIRED')
  assert(p.Action=='READ' or p.Action=='CREATE' or p.Action=='NAME' or p.Action=='DISPATCH' or p.Action=='STOP' or p.Action=='TASK' or p.Action=='ACTIVITY' or p.Action=='END','BAD_ACTION')
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
   local _,poolCount,civ=namePool(pid)
   local before=occupants(c:GetX(),c:GetY())
   mutating=true;state={owner=pid,phase='CREATING',sourceCity=c:GetID(),sourceName=c:GetName(),sourceRef=SPCNetworkInput.Reference(c),x=c:GetX(),y=c:GetY(),namePoolCount=poolCount,namePoolCivilization=civ}
   local u=UnitManager.InitUnit(pid,M.KIND,c:GetX(),c:GetY())
   assert(u and u:GetOwner()==pid,'SPAWN_UNCONFIRMED')
   state.unitID=u:GetID();state.createdID=state.unitID;owned(pid,state.unitID)
   assert(type(u.GetName)=='function','TEAM_NAME_API_UNAVAILABLE')
   serial=serial+1
   state.teamKey=string.format('E%X-%X-%X',pid,state.createdID,serial)
   -- Logical session key is internal; it is never written into a name/Property.
   state.nameVerified=false
   assert(#list(pid)==1,'SPAWN_COUNT_UNCONFIRMED')
   assert(u:GetX()==state.x and u:GetY()==state.y,'EXACT_PLACEMENT_REJECTED')
   unchangedOthers(before);source();state.phase='NAMING'
  elseif p.Action=='NAME' then
   mutating=true;acceptName(pid,p)
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
   -- Do not advance the independent timer before native sleep is observed.
   mutating=true;state.activityKey=p.Token;state.activityMode='SLEEP';state.activityOwned=false;state.activityPending=true
   state.taskCompletions=0;state.phase='TASK_PREPARING'
  elseif p.Action=='ACTIVITY' then
   assert(state.owner==pid and state.unitID==p.UnitID and state.activityKey==p.ActivityKey,'ACTIVITY_REFERENCE_CHANGED')
   assert(type(p.Owned)=='boolean','ACTIVITY_OWNERSHIP_UNKNOWN')
   assert(p.Result=='ASLEEP' or p.Result=='RELEASED' or p.Result=='FAILED','ACTIVITY_RESULT_UNKNOWN')
   if p.Result=='ASLEEP' then
    assert(state.phase=='TASK_PREPARING' and state.activityMode=='SLEEP','ACTIVITY_NOT_PENDING')
    -- Retain attempted sleep ownership before source/target recheck can fail.
    -- The bridge independently guards exact unit/name/position before any release.
    mutating=true;state.activityOwned=p.Owned
    assert(p.SampleTurn==Game.GetCurrentGameTurn(),'STALE_ACTIVITY_SAMPLE')
    observe();tracked();target(pid,state.target)
    assert(p.NativeOperation==-1,'NATIVE_MISSION_ACTIVE_STOP')
    state.activityPending=false;state.activityMode='ASLEEP';state.phase='TASK_RUNNING'
    state.taskStart=Game.GetCurrentGameTurn();state.taskDue=state.taskStart+2
   elseif p.Result=='RELEASED' then
    assert(state.activityMode=='RELEASE','ACTIVITY_NOT_PENDING')
    -- The one-shot release reply is consumed. Any failed readback must be terminal, not a stuck RELEASE.
    mutating=true;state.activityMode='BLOCKED'
    assert(p.SampleTurn==Game.GetCurrentGameTurn(),'STALE_ACTIVITY_SAMPLE')
    local u=tracked();assert(u:GetX()==state.x and u:GetY()==state.y,'TEAM_DISPLACED_STOP')
    assert(p.NativeOperation==-1,'NATIVE_MISSION_ACTIVE_STOP')
    mutating=true;state.activityMode='NONE';state.activityOwned=false;state.activityPending=false
   else
    assert(state.activityMode=='SLEEP' or state.activityMode=='ASLEEP' or state.activityMode=='RELEASE','ACTIVITY_NOT_PENDING')
    mutating=true
    if state.activityMode=='RELEASE' then state.activityMode='BLOCKED'
    else state.activityOwned=state.activityOwned or p.Owned;state.activityPending=false end
    error('ACTIVITY_READBACK_STOP: '..tostring(p.Detail or 'UNKNOWN'):sub(1,180))
   end
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
 publishActivity() -- Fresh Gameplay context cannot adopt a surviving session activity lease.
 local data={};shared.ExpeditionGate=data
 function data.Request(pid,p)
  if not P.IsTestPlayer(pid) or type(p)~='table' or type(p.Token)~='string' or #p.Token==0 or #p.Token>100 then return end
  if busy then return end
  local activity=p.Action=='ACTIVITY'
  if activity and p.Token==lastActivityToken then ExposedMembers.SPC_ExpeditionActivityReply=lastActivityReply;return end
  if not activity and p.Token==lastToken then ExposedMembers.SPC_ExpeditionGateReply=lastReply;return end
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
  v.token=p.Token
  if activity then
   lastActivityToken=p.Token;lastActivityReply=v;ExposedMembers.SPC_ExpeditionActivityReply=v
  else
   lastToken=p.Token;lastReply=v;ExposedMembers.SPC_ExpeditionGateReply=v
  end
  publishActivity()
  print('[SPC][B190][N1_SPY] action='..tostring(p.Action)..' owner='..pid..' unit='..tostring(v.unitID)..' phase='..v.phase..' error='..tostring(v.error))
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
  publishActivity()
 end
 Events.PlayerTurnActivated.Add(data.Turn) -- Owned endpoints/unit; pending travel adds one player-unit collection read; no task-turn scan.
 if Events.CityTransfered then Events.CityTransfered.Add(function()
  if not busy and state.unitID and state.phase~='ENDED' and state.phase~='HELD' then
   step='REFERENCE';local ok,err=pcall(function()observe();if state.phase=='TRAVELLING' then target(state.owner,state.target)end end);if not ok then hold(err)end
   publishActivity()
  end
 end)end
 if Events.UnitRemovedFromMap then Events.UnitRemovedFromMap.Add(function(pid,id)
  if pid==state.owner and id==state.unitID then state.removedEvents=math.min(99,(state.removedEvents or 0)+1)end
 end)end
end
