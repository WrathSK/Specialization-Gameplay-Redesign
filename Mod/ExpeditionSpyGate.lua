-- B201: bounded player-owned identity/intent, exact Property readback.
-- Native unit/travel/activity are fresh facts; no native mission or reward.
-- Native name assignment and travel survival remain explicit user-game gates.
if include and not SPCGreatWorkCatalog then include('GreatWorkCatalog')end
if include and not SPCExpeditionTrainingDiagnostics then include('ExpeditionTrainingDiagnostics')end
SPCExpeditionSpyGate={KIND='UNIT_SPC_EXPEDITION_SPY',LEGACY='UNIT_SPC_EXPEDITION_GATE',ZERO='UNIT_SPC_EXPEDITION_ZERO'}
function SPCExpeditionSpyGate.Start(P,shared)
 local M=SPCExpeditionSpyGate
 -- v0.1 supports standard speed only; Design floor(2 x speed multiplier) is deferred.
 local TASK_TURNS=2
 local returnToCentre
 local state={};local envelope;local loaded=false;local storeBlocked=false;local restored=false;local recovering=false;local busy=false;local mutating=false;local lastToken;local lastReply;local lastActivityToken;local lastActivityReply;local step='REQUEST'
 local movementProbeLocked=false
 local missionStatus,missionReason,missionRetryKey,missionUnknownReads
 local Store=SPCExpeditionSpyStore
 local fields={'trainingToken','trainingBorn','trainingReceiptTurn','trainingTurn','trainingQueued','trainingCompleted','owner','phase','unitID','createdID','sourceCity','sourceName','sourceRef','x','y','expectedName','nameVerified','teamKey','startTurn','dueTurn','taskStart','taskDue','taskCompleted','taskCompletions','taskCount','missionCategory','missionX','missionY','missionEvidence','missionWorkID','missionCompletionUnknownTurn','taskOutcome','entryX','entryY','activityKey','activityMode','activityOwned','activityPending','sleepConfirmed','stop','errorStep','errorDetail'}
 local function savedState()
  local out={};for _,k in ipairs(fields)do out[k]=state[k]end
  if state.target then out.target={};for _,k in ipairs({'name','owner','id','x','y'})do out.target[k]=state.target[k]end end
  return out
 end
 -- B223: one bounded diagnostic producer; never owns team/save decisions.
 local trace
 if SPCExpeditionTrainingDiagnostics then
  local ok,value=pcall(SPCExpeditionTrainingDiagnostics.New,P,'GATE')
  if ok then trace=value end
 end
 local function equal(a,b)
  if type(a)~=type(b)then return false end
  if type(a)~='table'then return a==b end
  for k,v in pairs(a)do if not equal(v,b[k])then return false end end
  for k in pairs(b)do if a[k]==nil then return false end end;return true
 end
 local function load(pid)
  if loaded then return end
  loaded=true
  local err;envelope,err=Store.Read(pid)
  if err then
   storeBlocked=true;state={owner=pid,phase='HELD',stop=err,activityMode='BLOCKED'};return
  end
  if envelope and envelope.state then
   state={};for k,v in pairs(envelope.state)do
    if type(v)=='table'then state[k]={};for a,b in pairs(v)do state[k][a]=b end else state[k]=v end
   end;restored=true
   recovering=state.activityMode=='SLEEP' or state.activityMode=='ARMED' or state.activityMode=='ASLEEP' or state.activityMode=='RELEASE'
   if state.phase=='CREATING' or state.phase=='ENDING' or (state.phase=='TRAINING' and (state.trainingBorn or state.trainingCompleted)) then
    state.phase='HELD';state.stop='EXPEDITION_NATIVE_TRANSACTION_UNCONFIRMED'
   end
  end
 end
 local function save(newGeneration)
  assert(not storeBlocked,'EXPEDITION_STORE_UNAVAILABLE')
  local nextState=savedState()
  if not newGeneration and envelope and equal(nextState,envelope.state)then return end
  local candidate={schema=1,owner=state.owner,generation=(envelope and envelope.generation or 0)+(newGeneration and 1 or 0),revision=(envelope and envelope.revision or 0)+1,state=nextState}
  if candidate.generation==0 then candidate.generation=1 end
  local confirmed,err=Store.Write(P,state.owner,envelope,candidate)
  if not confirmed then storeBlocked=true;recovering=false;state.activityMode='BLOCKED';error(err or 'EXPEDITION_STORE_WRITE_UNCONFIRMED',0)end
  envelope=confirmed
 end
 local function traceState(stage,u,extra)
  pcall(function()
   if not trace then return end
   if not u then
    local ok,value=pcall(function()
     local player=Players[state.owner];return player and player:GetUnits():FindID(state.unitID)
    end)
    if ok then u=value end
   end
   local v={owner=state.owner,eventUnit=state.unitID,sourceCity=state.sourceCity,
    teamKey=state.teamKey,activityKey=state.activityKey,phase=state.phase,mode=state.activityMode or 'NONE',
    x=state.x,y=state.y,missionCategory=state.missionCategory,taskStart=state.taskStart or 'NIL',taskDue=state.taskDue or 'NIL',
    owned=state.activityOwned==true,releasePending=state.activityPending==true,
    storeStatus=storeBlocked and 'BLOCKED' or (envelope and 'CONFIRMED' or 'ABSENT'),
    storeRevision=envelope and envelope.revision,savedPhase=envelope and envelope.state and envelope.state.phase,
    savedMatches=envelope~=nil and equal(savedState(),envelope.state)}
   if state.target then v.targetOwner=state.target.owner;v.targetCity=state.target.id;v.targetX=state.target.x;v.targetY=state.target.y end
   for k,value in pairs(extra or {})do v[k]=value end
   trace.Unit(stage,u,v)
  end)
 end
 -- Scalar transition mirror, independent of explicit diagnostic snapshots.
 local revision=0;local published={}
 local function publishActivity()
  local v={trainingToken=state.trainingToken,owner=state.owner,unitID=state.unitID,expectedName=state.expectedName,x=state.x,y=state.y,
   teamKey=state.teamKey,activityKey=state.activityKey,phase=state.phase or 'IDLE',mode=recovering and 'RECOVER' or state.activityMode or 'NONE',recovering=recovering,sleepConfirmed=state.sleepConfirmed==true,
   owned=state.activityOwned==true,releasePending=state.activityPending==true,taskStart=state.taskStart,taskDue=state.taskDue,
   taskCompleted=state.taskCompleted,taskCompletions=state.taskCompletions,missionStatus=missionStatus,missionReason=missionReason,error=state.stop,activityFailure=state.activityFailure,
   trainingReceipt=state.phase=='TRAINING' and (state.trainingBorn~=nil or state.trainingCompleted==true) or nil,
   trainingQueued=state.phase=='TRAINING' and state.trainingQueued==true or nil}
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
 -- B212: any city of a met, living major civilization. The target need not be
 -- revealed (user decision); the Expedition enters the civilization through one
 -- revealed city of that owner and travels on its internal routes.
 local function target(pid,t)
  step='TARGET'
  assert(type(t)=='table' and int(t.owner) and int(t.id) and int(t.x) and int(t.y),'TARGET_CHANGED')
  local p=Players[t.owner]
  assert(p and t.owner~=pid and p:IsMajor() and p:IsAlive(),'TARGET_CHANGED')
  assert(Players[pid]:GetDiplomacy():HasMet(t.owner),'TARGET_CHANGED')
  local cities=p:GetCities();local c=cities:FindID(t.id)
  assert(c and c:GetOwner()==t.owner and c:GetX()==t.x and c:GetY()==t.y,'TARGET_CHANGED')
  return c
 end
 local function entry(pid,t,x,y)
  step='ENTRY'
  assert(int(x) and int(y),'ENTRY_UNKNOWN')
  local c
  if x==t.x and y==t.y then c=target(pid,t);step='ENTRY'
  else
   local cities=Players[t.owner]:GetCities()
   assert(type(cities.Members)=='function','ENTRY_READER_UNAVAILABLE')
   for _,other in cities:Members()do if other:GetX()==x and other:GetY()==y then c=other end end
  end
  assert(c and c:GetOwner()==t.owner and c:GetX()==x and c:GetY()==y,'ENTRY_CHANGED')
  local vis=PlayersVisibility and PlayersVisibility[pid]
  assert(vis and vis:IsRevealed(x,y),'ENTRY_UNKNOWN')
  return c
 end
 local function civilization(owner)
  local config=PlayerConfigurations and PlayerConfigurations[owner]
  assert(config and type(config.GetCivilizationTypeName)=='function','TARGET_CIVILIZATION_UNAVAILABLE')
  local civ=config:GetCivilizationTypeName()
  assert(type(civ)=='string' and civ:match('^CIVILIZATION_[A-Z0-9_]+$'),'TARGET_CIVILIZATION_UNAVAILABLE')
  return civ
 end
 local function insightStore()
  return assert(shared.CityProgressionStore,'INSIGHT_STORE_UNAVAILABLE')
 end
 local function insights(pid)
  return insightStore().ExpeditionInsights(pid,source())
 end
 -- Native facts distinguish a confirmed invalid target from an unavailable reader.
 -- UI evidence selects the object; only a fresh native sample can authorize it.
 local function missionAssert(ok,status,code)
  if not ok then error({missionStatus=status,code=code},0)end
 end
 local function missionFact(value,code)
  missionAssert(value~=nil,'UNKNOWN',code);return value
 end
 local function missionBoolean(value,code)
  missionAssert(type(value)=='boolean','UNKNOWN',code);return value
 end
 local function readMission(pid,t,m)
  step='MISSION'
  missionAssert(type(m)=='table' and (m.category=='PEOPLE' or m.category=='WORKS' or m.category=='PLACES'),'UNKNOWN','MISSION_UNKNOWN')
  missionAssert(type(t)=='table' and int(t.owner) and int(t.id) and int(t.x) and int(t.y),'UNKNOWN','MISSION_TARGET_UNKNOWN')
  local p=missionFact(Players[t.owner],'MISSION_TARGET_UNKNOWN')
  missionAssert(t.owner~=pid and missionBoolean(p:IsMajor(),'MISSION_TARGET_UNKNOWN') and missionBoolean(p:IsAlive(),'MISSION_TARGET_UNKNOWN'),'INVALID','MISSION_TARGET_INVALID')
  missionAssert(missionBoolean(Players[pid]:GetDiplomacy():HasMet(t.owner),'MISSION_TARGET_UNKNOWN'),'INVALID','MISSION_TARGET_INVALID')
  local cities=missionFact(p:GetCities(),'MISSION_TARGET_UNKNOWN')
  local c=cities:FindID(t.id)
  missionAssert(c~=nil,'INVALID','MISSION_TARGET_INVALID')
  local owner,id,x,y=c:GetOwner(),c:GetID(),c:GetX(),c:GetY()
  missionAssert(int(owner) and int(id) and int(x) and int(y),'UNKNOWN','MISSION_TARGET_UNKNOWN')
  missionAssert(owner==t.owner and id==t.id and x==t.x and y==t.y,'INVALID','MISSION_TARGET_INVALID')
  missionAssert(int(m.x) and int(m.y),'UNKNOWN','MISSION_PLOT_UNKNOWN')
  if m.category=='PEOPLE' then
   -- Capital getters are native current facts, not saved destination labels.
   missionAssert(type(cities.GetCapitalCity)=='function','UNKNOWN','CAPITAL_API_UNAVAILABLE')
   local capital=cities:GetCapitalCity()
   missionAssert(capital~=nil,'UNKNOWN','MISSION_CAPITAL_UNKNOWN')
   local co,ci,cx,cy=capital:GetOwner(),capital:GetID(),capital:GetX(),capital:GetY()
   missionAssert(int(co) and int(ci) and int(cx) and int(cy),'UNKNOWN','MISSION_CAPITAL_UNKNOWN')
   missionAssert(co==t.owner and ci==t.id and cx==t.x and cy==t.y,'INVALID','MISSION_TARGET_INVALID')
   missionAssert(m.x==t.x and m.y==t.y,'INVALID','MISSION_PLOT_CHANGED')
   return c
  end
  local def=type(m.building)=='string' and P.Info('Buildings',m.building)
  missionAssert(def~=nil,'UNKNOWN','MISSION_BUILDING_UNKNOWN')
  local wonder=def.IsWonder==true or def.IsWonder==1
  -- Works can be held in a completed wonder as well as an ordinary building.
  missionAssert(m.category~='PLACES' or wonder,'INVALID','MISSION_BUILDING_UNKNOWN')
  local b=missionFact(c:GetBuildings(),'MISSION_BUILDING_UNKNOWN')
  local exists=P.HasBuilding(b,def.Index)
  missionAssert(missionBoolean(exists,'MISSION_BUILDING_UNKNOWN'),'INVALID','MISSION_TARGET_INVALID')
  local plot=missionFact(Map and Map.GetPlot and Map.GetPlot(m.x,m.y),'MISSION_PLOT_UNKNOWN')
  local index=missionFact(plot:GetIndex(),'MISSION_PLOT_UNKNOWN')
  missionAssert(type(b.GetBuildingLocation)=='function','UNKNOWN','MISSION_LOCATION_UNAVAILABLE')
  local at=missionFact(b:GetBuildingLocation(def.Index),'MISSION_LOCATION_UNAVAILABLE')
  missionAssert(int(at),'UNKNOWN','MISSION_LOCATION_UNAVAILABLE')
  missionAssert(at==index,'INVALID','MISSION_PLOT_CHANGED')
  local plotOwner=plot:GetOwner()
  missionAssert(type(plotOwner)=='number' and plotOwner==plotOwner and plotOwner%1==0,'UNKNOWN','MISSION_PLOT_UNKNOWN')
  missionAssert(plotOwner==t.owner,'INVALID','MISSION_PLOT_CHANGED')
  if m.category=='WORKS' then
   missionAssert(int(m.slot) and type(m.work)=='string','UNKNOWN','MISSION_WORK_UNKNOWN')
   missionAssert(SPCGreatWorkCatalog and type(SPCGreatWorkCatalog.Resolve)=='function','UNKNOWN','MISSION_WORK_CATALOG_UNAVAILABLE')
   local eligible,why=SPCGreatWorkCatalog.Resolve(P,m.work)
   missionAssert(eligible,(why=='UNSUPPORTED_TYPE' or why=='UNREVIEWED_ERA') and 'INVALID' or 'UNKNOWN','MISSION_WORK_INELIGIBLE')
   missionAssert(type(b.GetGreatWorkInSlot)=='function','UNKNOWN','MISSION_WORK_READER_UNAVAILABLE')
   local workID=b:GetGreatWorkInSlot(def.Index,m.slot)
   missionAssert(workID~=nil,'UNKNOWN','MISSION_WORK_READER_UNAVAILABLE')
   missionAssert(workID~=-1,'INVALID','MISSION_TARGET_INVALID')
   missionAssert(int(workID),'UNKNOWN','MISSION_WORK_READER_UNAVAILABLE')
   if m.requireWorkID then
    missionAssert(int(m.workID),'UNKNOWN','MISSION_WORK_ID_UNAVAILABLE')
    missionAssert(workID==m.workID,'INVALID','MISSION_TARGET_INVALID')
   end
   local reader=type(b.GetGreatWorkTypeFromIndex)=='function' and function(id)return b:GetGreatWorkTypeFromIndex(id)end
    or (Game and type(Game.GetGreatWorkTypeFromIndex)=='function' and Game.GetGreatWorkTypeFromIndex)
   missionAssert(reader~=nil,'UNKNOWN','MISSION_WORK_TYPE_UNAVAILABLE')
   local kind=missionFact(reader(workID),'MISSION_WORK_TYPE_UNAVAILABLE')
   missionAssert(type(kind)=='string' or (type(kind)=='number' and kind==kind and kind%1==0),'UNKNOWN','MISSION_WORK_TYPE_UNAVAILABLE')
   local row=missionFact(P.Info('GreatWorks',m.work),'MISSION_WORK_TYPE_UNAVAILABLE')
   missionAssert(kind==row.Index or kind==row.Hash or kind==m.work,'INVALID','MISSION_TARGET_INVALID')
   return c,workID
  end
  return c
 end
 local function mission(pid,t,m)
  local ok,value,workID=pcall(readMission,pid,t,m)
  if ok then return 'VALID',value,workID end
  if type(value)=='table' and value.missionStatus then return value.missionStatus,value.code end
  return 'UNKNOWN','MISSION_FACT_UNAVAILABLE'
 end
 local function missionOf()
  if not state.missionCategory then return nil end
  local e=state.missionEvidence or '';local building,slot,work=e:match('^([^|]*)|([^|]*)|([^|]*)$')
  return {category=state.missionCategory,x=state.missionX,y=state.missionY,building=building~='' and building or nil,
   slot=tonumber(slot),work=work~='' and work or nil,workID=state.missionWorkID,requireWorkID=true}
 end
 -- B218: bounded read-only placement evidence; never resumes or repairs a task.
 -- One scalar watch, no persisted fields, timer, polling or global unit scan.
 local placementWatch;local placementSequence=0
 local function diagnosticValue(u,key)
  local ok,value=pcall(function()return u[key](u)end)
  if ok and (type(value)=='number' or type(value)=='boolean')then return tostring(value)end
  return 'UNKNOWN'
 end
 local function placementSample(stage,ex,ey,record)
  local w=record or placementWatch;if not w then return end
  -- Diagnostics must never replace the original placement result/error.
  pcall(function()
   local player=Players[w.owner];local u=player and player:GetUnits():FindID(w.id)
   local prefix='[SPC][B191][N1_TASK] placement='..stage..' seq='..w.sequence..' owner='..w.owner..' unit='..w.id
   print(prefix..' requested='..w.x..','..w.y..' actual='..diagnosticValue(u,'GetX')..','..diagnosticValue(u,'GetY')
    ..' readOwner='..diagnosticValue(u,'GetOwner')..' readID='..diagnosticValue(u,'GetID')..' type='..diagnosticValue(u,'GetType')
    ..' operation='..diagnosticValue(u,'GetSpyOperation')..' event='..tostring(ex or 'NA')..','..tostring(ey or 'NA'))
   local ok,native=pcall(function()return Units.GetUnitsInPlot(w.x,w.y)end)
   if not ok or type(native)~='table' then print(prefix..' occupants=UNKNOWN');return end
   local n=0
   for _,other in pairs(native)do
    if n==8 then print(prefix..' occupants=TRUNCATED limit=8');return end
    n=n+1
    local kind=diagnosticValue(other,'GetType');local info=P.Info('Units',tonumber(kind)) or {}
    print(prefix..' occupant='..n..' otherOwner='..diagnosticValue(other,'GetOwner')..' otherID='..diagnosticValue(other,'GetID')
     ..' type='..kind..' xy='..diagnosticValue(other,'GetX')..','..diagnosticValue(other,'GetY')
     ..' spy='..tostring(info.Spy)..' stackable='..tostring(info.Stackable))
   end
   print(prefix..' occupants='..n)
  end)
 end
 local function closePlacement(stage)
  placementSample(stage);placementWatch=nil
 end
 if Events.UnitMoveComplete then Events.UnitMoveComplete.Add(function(pid,id,x,y)
  local w=placementWatch;if not w or pid~=w.owner or id~=w.id then return end
  w.events=w.events+1;placementSample('MOVE_EVENT',x,y)
  if w.events>=6 then closePlacement('EVENT_LIMIT')end
 end)end
 local function relocate(u,x,y)
  assert(UnitManager and type(UnitManager.PlaceUnit)=='function','PLACEMENT_UNAVAILABLE')
  placementSequence=placementSequence+1
  placementWatch={owner=state.owner,id=u:GetID(),x=x,y=y,sequence=placementSequence,events=0}
  local placementRecord=placementWatch
  placementSample('PRE')
  pcall(print,'[SPC][B191][N1_TASK] placement=CHANNEL moveEvent='..tostring(Events.UnitMoveComplete~=nil))
  if u:GetX()==x and u:GetY()==y then closePlacement('ALREADY_THERE');return u end
  if type(UnitManager.RestoreMovement)=='function' then UnitManager.RestoreMovement(u)end
  local placementOK,placementError=pcall(UnitManager.PlaceUnit,u,x,y)
  placementSample(placementOK and 'POST' or 'API_ERROR',nil,nil,placementRecord)
  if not placementOK then error(placementError,0)end
  local placed=owned(state.owner,u:GetID())
  assert(placed:GetX()==x and placed:GetY()==y,'EXACT_PLACEMENT_REJECTED')
  if type(UnitManager.FinishMoves)=='function' then UnitManager.FinishMoves(placed)end
  return placed
 end
 local function reason(err)
  return tostring(err):match(':%d+:%s*([A-Z][A-Z0-9_]+)') or tostring(err):match('^([A-Z][A-Z0-9_]+)') or 'API_UNAVAILABLE'
 end
 local function detail(err)
  return tostring(err):gsub('[%c]',' '):gsub('%[','('):gsub('%]',')'):sub(1,220)
 end
 local function logFailure(code,at,raw)
  print('[SPC][B191][N1_SPY_ERROR] step='..at..' code='..code..' detail='..raw)
 end
 local function hold(err)
  -- Recovery is consumed by a terminal hold; release still re-reads the exact
  -- native identity and owned activity independently before any Wake request.
  recovering=false
  if storeBlocked then state.activityMode='BLOCKED' else releaseActivity()end
  state.phase='HELD';state.stop=reason(err);state.errorStep=step;state.errorDetail=detail(err)
  logFailure(state.stop,state.errorStep,state.errorDetail)
  if state.owner and not storeBlocked then
   local ok,err=pcall(save);if not ok then state.stop=reason(err);state.activityMode='BLOCKED' end
  end
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
    local ex,ey=state.entryX or state.target.x,state.entryY or state.target.y
    if candidate:GetX()==ex and candidate:GetY()==ey then
     local id=candidate:GetID()
     -- Validate the actual exact-lookup object as well as the collection item.
     local current=owned(state.owner,id)
     assert(named(current),'TEAM_NAME_UNAVAILABLE')
     assert(current:GetX()==ex and current:GetY()==ey,'TARGET_CHANGED')
     state.unitID=id
     local route=ex==state.target.x and ey==state.target.y and 'DIRECT' or 'ENTRY_RELOCATE'
     traceState('ARRIVAL_BEFORE',current,{entryX=ex,entryY=ey,arrivalRoute=route})
     -- B212: entered through another city of the same civilization; continue on its
     -- internal routes to the target city centre (no added time, implementation reading).
     if ex~=state.target.x or ey~=state.target.y then step='ENTRY_RELOCATE';current=relocate(current,state.target.x,state.target.y)end
     state.x=current:GetX();state.y=current:GetY();state.phase='ARRIVED';state.entryX=nil;state.entryY=nil
     save()
     traceState('ARRIVAL_CONFIRMED',current,{entryX=ex,entryY=ey,arrivalRoute=route})
     return
    end
   end
   assert(Game.GetCurrentGameTurn()<=state.dueTurn+1,'NATIVE_IDENTITY_UNCONFIRMED')
   return
  end
  local u=tracked()
  assert(u:GetX()==state.x and u:GetY()==state.y,'TEAM_DISPLACED_STOP')
  if state.phase=='TASK_RUNNING' and not recovering then
   -- GetSpyOperation is established in UI, not assumed present in Gameplay.
   -- If exposed here, also reject a native mission; otherwise the no-reward
   -- fixture relies on the checked start sample + exact-type UI isolation.
   if type(u.GetSpyOperation)=='function' then assert(u:GetSpyOperation()==-1,'NATIVE_MISSION_ACTIVE_STOP')end
   local m=missionOf();local turn=Game.GetCurrentGameTurn()
   -- A later valid snapshot cannot prove the missed completion-time facts.
   if state.missionCompletionUnknownTurn and turn>state.missionCompletionUnknownTurn then
    missionStatus='UNKNOWN';missionReason='MISSION_COMPLETION_UNCONFIRMED'
    error('MISSION_COMPLETION_UNCONFIRMED',0)
   end
   local retryKey=tostring(state.activityKey)..':'..turn
   if retryKey~=missionRetryKey then missionRetryKey=retryKey;missionUnknownReads=0 end
   -- No frame poll or unbounded reentrant retry: at most three unavailable
   -- samples per attempt/turn. Explicit target-change events reopen that budget.
   local completionCiv
   if (missionUnknownReads or 0)<3 then
    missionStatus,missionReason=mission(state.owner,state.target,m)
    if missionStatus=='VALID' then
     missionReason=nil
     -- A due-time READ must confirm the same full evidence as completion before
     -- clearing UNKNOWN. Valid target geometry alone cannot prove the award key.
     if turn>=state.taskDue then
      local known,civ=pcall(civilization,state.target.owner)
      if known then completionCiv=civ
      else missionStatus='UNKNOWN';missionReason='TARGET_CIVILIZATION_UNAVAILABLE' end
     end
    end
    if missionStatus=='UNKNOWN' then missionUnknownReads=(missionUnknownReads or 0)+1
    else missionUnknownReads=0 end
   end
   if missionStatus=='UNKNOWN' then
    if turn>=state.taskDue and not state.missionCompletionUnknownTurn then state.missionCompletionUnknownTurn=turn;save()end
    return
   end
   if missionStatus=='VALID' and state.missionCompletionUnknownTurn then state.missionCompletionUnknownTurn=nil;save()end
   if missionStatus=='INVALID' then
    -- B212 target invalidation: cancel, no Insight, no quota; the unit returns to the centre.
    state.phase='TASK_COMPLETE';state.taskCompleted=Game.GetCurrentGameTurn();state.taskOutcome='CANCELLED'
    releaseActivity();state.taskCompletions=0;save()
    print('[SPC][B191][N1_TASK] mission='..tostring(state.missionCategory)..' outcome=CANCELLED reason=TARGET_INVALID')
   elseif allowTaskCompletion and turn>=state.taskDue then
    local civ=assert(completionCiv,'MISSION_COMPLETION_UNCONFIRMED')
    state.missionCompletionUnknownTurn=nil
    -- City history first; a repeated completion after a failed save is idempotent.
    local archive=source()
    local added=insightStore().AddExpeditionInsight(state.owner,archive,civ,m.category,Game.GetCurrentGameTurn())
    state.phase='TASK_COMPLETE';state.taskCompleted=Game.GetCurrentGameTurn();state.taskOutcome='SUCCESS'
    releaseActivity()
    state.taskCompletions=1
    state.taskCount=(state.taskCount or 0)+1 -- Successful tasks only; never used as an attempt identifier.
    save()
    print('[SPC][B191][N1_TASK] mission='..m.category..' outcome=SUCCESS civ='..civ..' insight='..(added and 'NEW' or 'EXISTING'))
    if shared.CultureInsightsTourism then shared.CultureInsightsTourism.Audit({player=state.owner,city=archive:GetID()})end
   end
  end
 end
 local function snapshot(pid)
  local units=list(pid)
  if state.owner==pid and not storeBlocked then local ok,err=pcall(observe,false,units);if not ok then hold(err)end end
  local v={owner=pid,count=#units,turn=Game.GetCurrentGameTurn(),phase=state.phase or 'IDLE'}
  if #units==1 then
   local u=units[1];v.unitID=u:GetID();v.x=u:GetX();v.y=u:GetY();v.legacy=row(u).UnitType~=M.KIND
   v.unbound=not v.legacy and (state.owner~=pid or state.unitID~=u:GetID())
  end
  if state.owner==pid then
   for _,k in ipairs({'trainingToken','sourceCity','sourceName','startTurn','dueTurn','stop','nativeAllowed','nativeStatus','removedEvents','arrivalOthers','errorStep','errorDetail','taskStart','taskDue','taskCompleted','taskCompletions','activityMode','activityOwned','activityKey','activityFailure','missionCategory','missionX','missionY','missionWorkID','missionCompletionUnknownTurn','taskOutcome','entryX','entryY','expectedName','teamKey','nameVerified','namePoolCount','namePoolCivilization'})do
    -- A missing original unit must not be substituted by another discovered unit.
    v[k]=state[k]
   end
   v.createdID=state.createdID;v.trackedID=state.unitID;v.bound=false
   -- B212 presentation of the archive city's Insight history; display only.
   if state.sourceCity and state.phase~='TRAINING' then
    local ok,records=pcall(insights,pid)
    if ok then
     local own=pcall(civilization,pid) and civilization(pid) or nil
     local keys,history,effective={},0,0
     for k,r in pairs(records)do keys[#keys+1]=k;history=history+1;if r.civ~=own then effective=effective+1 end end
     table.sort(keys);v.insightKeys=keys;v.insightHistory=history;v.insightEffective=effective
    else v.insightStatus='UNKNOWN' end
   end
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
  v.missionStatus=missionStatus;v.missionReason=missionStatus~='VALID' and missionReason or nil
  v.persistence=storeBlocked and 'UNAVAILABLE' or restored and 'RESTORED' or envelope and 'CONFIRMED' or 'ABSENT'
  v.recovering=recovering;v.generation=envelope and envelope.generation;v.storeRevision=envelope and envelope.revision
  v.observedCount=v.count
  if state.owner==pid and state.phase~='ENDED' and (storeBlocked or not v.sameUnit) then
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
 -- B212: after the mission activity is released, return to the target city centre
 -- (Spy-like) and be ready for another unfinished mission or a new dispatch.
 returnToCentre=function()
  if state.phase~='TASK_COMPLETE' or not state.target or state.activityMode~='NONE' then return end
  step='RETURN_CENTRE'
  local u=tracked()
  assert(u:GetX()==state.x and u:GetY()==state.y,'TEAM_DISPLACED_STOP')
  assert(u:GetX()==state.target.x and u:GetY()==state.target.y,'TEAM_NOT_AT_CENTRE')
  -- No return teleport: all tasks now execute at this exact centre.
  state.taskStart=nil;state.taskDue=nil;state.taskCompleted=nil;state.taskCompletions=nil;state.activityKey=nil
  state.activityMode=nil;state.activityOwned=nil;state.activityPending=nil;state.sleepConfirmed=nil
  print('[SPC][B191][N1_TASK] mission='..tostring(state.missionCategory)..' outcome='..tostring(state.taskOutcome)..' returned=CENTRE')
  state.missionCategory=nil;state.missionX=nil;state.missionY=nil;state.missionEvidence=nil;state.missionWorkID=nil;state.missionCompletionUnknownTurn=nil;state.taskOutcome=nil;missionStatus=nil;missionReason=nil;missionRetryKey=nil;missionUnknownReads=0
  state.phase='ARRIVED'
 end
 local function handle(pid,p)
  assert(type(p)=='table' and type(p.Token)=='string' and #p.Token>0 and #p.Token<=100,'BAD_REQUEST')
  assert(P.IsTestPlayer(pid),'SUPPORTED_PLAYER_REQUIRED')
  assert(p.Action=='READ' or p.Action=='CREATE' or p.Action=='NAME' or p.Action=='DISPATCH' or p.Action=='STOP' or p.Action=='TASK' or p.Action=='ACTIVITY' or p.Action=='END','BAD_ACTION')
  if p.Action=='END' or p.Action=='STOP' or p.Action=='DISPATCH' or p.Action=='CREATE' then closePlacement('ACTION_CLOSE')end
  load(pid);step=p.Action
  if p.Action=='READ' then return snapshot(pid)end
  assert(not storeBlocked,'EXPEDITION_STORE_UNAVAILABLE')
  if p.Action=='CREATE' then
   assert(state.phase~='TRAINING' and state.phase~='CREATING' and state.phase~='HELD' and (not state.unitID or state.phase=='ENDED'),'SPAWN_UNCERTAIN_NO_RETRY')
   assert(#list(pid)==0,'EXISTING_TEST_TEAM_COUNTS')
   local c=Players[pid]:GetCities():FindID(p.CityID)
   assert(c and c:GetOwner()==pid and c:GetID()==p.CityID,'OWN_CITY_REQUIRED')
   local f=shared.EffectiveFacts.Read(pid,c)
   assert(f.specialization=='CULTURE' and f.active==4 and not f.investmentPending,'CULTURE_ACTIVE_IV_REQUIRED')
   assert(type(f.token)=='string' and #f.token>0 and c:GetProperty('SPC_DEV_BINDING_B013_TOKEN')==f.token,'SOURCE_REFERENCE_UNKNOWN')
   local r=P.Info('Units',M.KIND)
   assert(r and flag(r.Spy) and flag(r.IgnoreMoves) and flag(r.Stackable)
    and (r.CanRetreatWhenCaptured==false or r.CanRetreatWhenCaptured==0)
    and r.PromotionClass=='PROMOTION_CLASS_SPY','TEST_DATABASE_NOT_READY')
   local _,poolCount,civ=namePool(pid)
   local x,y=c:GetX(),c:GetY();assert(int(x) and int(y),'SOURCE_REFERENCE_UNKNOWN')
   local function currentSource(expectedRef)
    local current=Players[pid]:GetCities():FindID(p.CityID)
    assert(current and current:GetOwner()==pid and current:GetID()==p.CityID
     and current:GetX()==x and current:GetY()==y
     and current:GetProperty('SPC_DEV_BINDING_B013_TOKEN')==f.token,'SOURCE_REFERENCE_CHANGED')
    local ref=SPCNetworkInput.Reference(current)
    assert(type(ref)=='string' and #ref>0 and #ref<=2048,'SOURCE_REFERENCE_UNKNOWN')
    assert(not expectedRef or ref==expectedRef,'SOURCE_REFERENCE_CHANGED')
    return current,ref
   end
   local before=occupants(x,y)
   local ref;c,ref=currentSource() -- Occupancy/native readers may change the source.
   mutating=true;state={owner=pid,phase='CREATING',sourceCity=c:GetID(),sourceName=c:GetName(),sourceRef=ref,x=x,y=y,namePoolCount=poolCount,namePoolCivilization=civ}
   save(true) -- Reserve before InitUnit; ambiguous outcome never retries or frees cap.
   currentSource(ref) -- Readback callbacks cannot invalidate the source then spawn.
   local u=UnitManager.InitUnit(pid,M.KIND,x,y)
   assert(u and u:GetOwner()==pid,'SPAWN_UNCONFIRMED')
   state.unitID=u:GetID();state.createdID=state.unitID;owned(pid,state.unitID)
   assert(type(u.GetName)=='function','TEAM_NAME_API_UNAVAILABLE')
   state.teamKey=string.format('E%X-%X-%X',pid,state.createdID,envelope.generation)
   -- Monotonic saved generation survives END and native UnitID reuse.
   state.nameVerified=false
   assert(#list(pid)==1,'SPAWN_COUNT_UNCONFIRMED')
   assert(u:GetX()==state.x and u:GetY()==state.y,'EXACT_PLACEMENT_REJECTED')
   unchangedOthers(before);source();state.phase='NAMING'
   save();restored=false -- Only a confirmed fresh native creation resets this diagnostic.
  elseif p.Action=='NAME' then
   mutating=true;acceptName(pid,p)
  elseif p.Action=='DISPATCH' then
   -- B211: a completed task may be redispatched once its native activity is released.
   local again=state.phase=='TASK_COMPLETE' and state.activityMode=='NONE' and not state.activityPending and not state.activityOwned
   assert(state.owner==pid and state.unitID==p.UnitID and (state.phase=='CREATED' or state.phase=='ARRIVED' or again),'BOUND_TEAM_REQUIRED')
   observe();local u=tracked()
   assert(state.phase~='HELD' and u:GetID()==p.UnitID,'BOUND_TEAM_REQUIRED')
   assert(p.SampleTurn==Game.GetCurrentGameTurn() and p.FromX==u:GetX() and p.FromY==u:GetY(),'STALE_TRAVEL_SAMPLE')
   assert(p.NativeStatus=='KNOWN' and p.NativeAllowed==true,'NATIVE_TRAVEL_NOT_ALLOWED')
   assert(int(p.Travel) and int(p.Establish) and p.Travel+p.Establish<=1000,'TRAVEL_TIME_UNKNOWN')
   local t={owner=p.TargetOwner,id=p.TargetID,x=p.TargetX,y=p.TargetY}
   local c=target(pid,t);t.name=c:GetName()
   -- Native Spy travel needs a revealed city; enter the civilization through one.
   local ex,ey=p.EntryX or t.x,p.EntryY or t.y
   entry(pid,t,ex,ey);step='DISPATCH'
   state.target=t;state.startTurn=Game.GetCurrentGameTurn();state.dueTurn=state.startTurn+p.Travel+p.Establish
   state.nativeAllowed=type(p.NativeAllowed)=='boolean' and p.NativeAllowed or false
   state.nativeStatus=p.NativeStatus=='KNOWN' and 'KNOWN' or 'UNKNOWN'
   if again then
    state.taskStart=nil;state.taskDue=nil;state.taskCompleted=nil;state.taskCompletions=nil;state.activityKey=nil;state.activityFailure=nil
    state.activityMode=nil;state.activityOwned=nil;state.activityPending=nil;state.sleepConfirmed=nil
   end
   state.missionCategory=nil;state.missionX=nil;state.missionY=nil;state.missionEvidence=nil;state.missionWorkID=nil;state.missionCompletionUnknownTurn=nil;state.taskOutcome=nil;missionStatus=nil;missionReason=nil;missionRetryKey=nil;missionUnknownReads=0
   if ex~=t.x or ey~=t.y then state.entryX=ex;state.entryY=ey else state.entryX=nil;state.entryY=nil end
   mutating=true;state.phase='TRAVELLING';state.permit=p.Token
   save() -- Durable intent precedes the one-shot UI native permit; never replay on load.
  elseif p.Action=='TASK' then
   assert(state.owner==pid and state.unitID==p.UnitID,'BOUND_TEAM_REQUIRED')
   observe();assert(state.phase=='ARRIVED' and not state.taskStart,'TASK_NOT_AVAILABLE')
   local u=tracked()
   assert(p.SampleTurn==Game.GetCurrentGameTurn() and p.NativeOperation==-1,'NATIVE_OPERATION_UNKNOWN')
   if type(u.GetSpyOperation)=='function' then assert(u:GetSpyOperation()==-1,'NATIVE_MISSION_ACTIVE_STOP')end
   -- B212: one of the three Design missions, revalidated from native facts; a
   -- completed (archive city x civilization x category) key cannot start again.
   local m={category=p.Mission,x=p.MissionX,y=p.MissionY,building=p.Building,slot=p.Slot,work=p.Work,
    workID=p.WorkID,requireWorkID=p.WorkID~=nil}
   local valid,result,workID=mission(pid,state.target,m)
   missionStatus=valid;missionReason=valid~='VALID' and result or nil
   -- Successful validation returns a city object, not an assertion message.
   if valid~='VALID' then error(result,0) end
   step='TASK'
   local done=insights(pid)
   assert(not done[civilization(state.target.owner)..':'..m.category],'MISSION_ALREADY_COMPLETED')
   local evidence=(m.building or '')..'|'..(m.slot and tostring(m.slot) or '')..'|'..(m.work or '')
   assert(#evidence<=160,'MISSION_EVIDENCE_TOO_LONG')
   -- B220 user-approved interim execution: evidence stays at the selected
   -- work/wonder, while the exact bound team stays at the destination centre.
   -- Never turn evidence coordinates into a placement request or accept drift.
   step='MISSION_CENTRE'
   assert(u:GetX()==state.target.x and u:GetY()==state.target.y,'TEAM_NOT_AT_CENTRE')
   state.missionCategory=m.category;state.missionX=m.x;state.missionY=m.y;state.missionEvidence=evidence;state.missionWorkID=workID;state.missionCompletionUnknownTurn=nil;state.taskOutcome=nil
   state.x=u:GetX();state.y=u:GetY()
   print('[SPC][B191][N1_TASK] mission='..m.category..' execution=CENTRE actual='..state.x..','..state.y..' evidence='..m.x..','..m.y)
   -- Do not advance the independent timer before native sleep is observed.
   -- Next durable revision identifies this attempt, even when the previous one cancelled.
   mutating=true;state.activityKey=state.teamKey..':attempt'..tostring(envelope.revision+1);state.activityMode='SLEEP';state.activityOwned=false;state.activityPending=true
   state.activityFailure=nil;state.taskCompletions=0;state.phase='TASK_PREPARING'
  elseif p.Action=='ACTIVITY' then
   assert(state.owner==pid and state.unitID==p.UnitID and state.activityKey==p.ActivityKey,'ACTIVITY_REFERENCE_CHANGED')
   assert(type(p.Owned)=='boolean','ACTIVITY_OWNERSHIP_UNKNOWN')
   assert(p.Result=='ARMED' or p.Result=='RECOVERED' or p.Result=='ASLEEP' or p.Result=='RELEASED' or p.Result=='REJECTED' or p.Result=='FAILED','ACTIVITY_RESULT_UNKNOWN')
   if p.Result=='RECOVERED' then
    assert(recovering,'ACTIVITY_NOT_PENDING')
    mutating=true;recovering=false -- Matching one-shot reply is consumed even if stale/invalid.
    assert(p.SampleTurn==Game.GetCurrentGameTurn(),'STALE_ACTIVITY_SAMPLE')
    local u=tracked();assert(u:GetX()==state.x and u:GetY()==state.y,'TEAM_DISPLACED_STOP')
    assert(p.NativeOperation==-1 and type(p.Sleeping)=='boolean' and type(p.Awake)=='boolean','ACTIVITY_RECOVERY_UNKNOWN')
    assert(p.Sleeping~=p.Awake,'ACTIVITY_RECOVERY_UNKNOWN')
    if state.activityMode=='SLEEP' and not state.activityOwned then
     -- No request could run before durable ARMED. Pre-existing Sleep remains unowned.
     if p.Sleeping then
      source();target(pid,state.target);state.sleepConfirmed=true;state.activityPending=false;state.activityMode='ASLEEP';state.phase='TASK_RUNNING'
      state.taskStart=Game.GetCurrentGameTurn();state.taskDue=state.taskStart+TASK_TURNS
     end
    elseif state.activityMode=='ARMED' then
     assert(p.Sleeping,'ACTIVITY_SLEEP_OUTCOME_UNKNOWN')
     source();target(pid,state.target);state.sleepConfirmed=true;state.activityPending=false;state.activityMode='ASLEEP';state.phase='TASK_RUNNING'
     state.taskStart=Game.GetCurrentGameTurn();state.taskDue=state.taskStart+TASK_TURNS
    elseif state.activityMode=='ASLEEP' then
     assert(p.Sleeping and state.sleepConfirmed,'ACTIVITY_UNEXPECTED_WAKE')
     source();target(pid,state.target)
    elseif state.activityMode=='RELEASE' then
     if p.Sleeping then assert(state.activityOwned,'ACTIVITY_UNOWNED_SLEEP');state.sleepConfirmed=true
     else state.activityMode='NONE';state.activityOwned=false;state.activityPending=false;returnToCentre()end
    else error('ACTIVITY_RECOVERY_UNKNOWN')end
   elseif p.Result=='REJECTED' then
    -- B222: only a proven unarmed, unexecuted attempt may return to idle.
    -- A stale/duplicate response cannot cancel a newer lease or an owned action.
    assert(not recovering and state.phase=='TASK_PREPARING' and state.activityMode=='SLEEP'
     and state.activityOwned==false and state.activityPending==true and not state.sleepConfirmed
     and not state.taskStart and not state.taskDue,'ACTIVITY_NOT_PENDING')
    assert(p.SampleTurn==Game.GetCurrentGameTurn() and p.NativeOperation==-1
     and p.Owned==false and p.Requested==false and p.Attempted==false
     and p.Awake==true and p.Sleeping==false and p.Detail=='ACTIVITY_SLEEP_NOT_ALLOWED','ACTIVITY_REJECTION_UNCONFIRMED')
    mutating=true -- A lost reference/readback below still takes the protected stop path.
    source();target(pid,state.target);local u=tracked()
    assert(u:GetX()==state.x and u:GetY()==state.y and state.x==state.target.x and state.y==state.target.y,'TEAM_DISPLACED_STOP')
    if type(u.GetSpyOperation)=='function'then assert(u:GetSpyOperation()==-1,'NATIVE_MISSION_ACTIVE_STOP')end
    state.phase='ARRIVED';state.activityMode=nil;state.activityOwned=nil;state.activityPending=nil;state.sleepConfirmed=nil;state.activityKey=nil
    state.taskCompletions=nil;state.missionCategory=nil;state.missionX=nil;state.missionY=nil;state.missionEvidence=nil;state.missionWorkID=nil;state.missionCompletionUnknownTurn=nil;state.taskOutcome=nil
    missionStatus=nil;missionReason=nil;missionRetryKey=nil;missionUnknownReads=0
    state.activityFailure='ACTIVITY_SLEEP_NOT_ALLOWED' -- Replaceable session feedback, not persistent history.
    print('[SPC][B191][N1_TASK] admission=REJECTED reason=ACTIVITY_SLEEP_NOT_ALLOWED nativeRequested=false')
   elseif p.Result=='ARMED' then
    assert(not recovering and state.phase=='TASK_PREPARING' and state.activityMode=='SLEEP','ACTIVITY_NOT_PENDING')
    assert(p.SampleTurn==Game.GetCurrentGameTurn() and p.NativeOperation==-1 and p.Owned and p.Awake==true and p.Sleeping==false,'STALE_ACTIVITY_SAMPLE')
    observe();tracked();target(pid,state.target)
    mutating=true;state.activityOwned=true;state.activityMode='ARMED'
    save() -- Readback grants one native Sleep attempt; saved intent is not completion.
   elseif p.Result=='ASLEEP' then
    assert(not recovering and state.phase=='TASK_PREPARING' and (state.activityMode=='SLEEP' or state.activityMode=='ARMED'),'ACTIVITY_NOT_PENDING')
    assert(not p.Owned or state.activityMode=='ARMED','ACTIVITY_OWNERSHIP_UNCONFIRMED')
    -- Retain attempted sleep ownership before source/target recheck can fail.
    -- The bridge independently guards exact unit/name/position before any release.
    mutating=true;state.activityOwned=p.Owned
    assert(p.SampleTurn==Game.GetCurrentGameTurn(),'STALE_ACTIVITY_SAMPLE')
    observe();tracked();target(pid,state.target)
    assert(p.NativeOperation==-1,'NATIVE_MISSION_ACTIVE_STOP')
    state.sleepConfirmed=true;state.activityPending=false;state.activityMode='ASLEEP';state.phase='TASK_RUNNING'
    state.taskStart=Game.GetCurrentGameTurn();state.taskDue=state.taskStart+TASK_TURNS
   elseif p.Result=='RELEASED' then
    assert(state.activityMode=='RELEASE','ACTIVITY_NOT_PENDING')
    -- The one-shot release reply is consumed. Any failed readback must be terminal, not a stuck RELEASE.
    mutating=true;state.activityMode='BLOCKED'
    assert(p.SampleTurn==Game.GetCurrentGameTurn(),'STALE_ACTIVITY_SAMPLE')
    local u=tracked();assert(u:GetX()==state.x and u:GetY()==state.y,'TEAM_DISPLACED_STOP')
    assert(p.NativeOperation==-1,'NATIVE_MISSION_ACTIVE_STOP')
    mutating=true;state.activityMode='NONE';state.activityOwned=false;state.activityPending=false
    returnToCentre()
   else
    assert(state.activityMode=='SLEEP' or state.activityMode=='ARMED' or state.activityMode=='ASLEEP' or state.activityMode=='RELEASE','ACTIVITY_NOT_PENDING')
    mutating=true;recovering=false
    if state.activityMode=='RELEASE' then state.activityMode='BLOCKED'
    else state.activityOwned=state.activityOwned or p.Owned;state.activityPending=false end
    state.activityFailure=tostring(p.Detail or ''):match('(ACTIVITY_[A-Z0-9_]+)') or 'ACTIVITY_FAILURE_UNKNOWN'
    error('ACTIVITY_READBACK_STOP: '..tostring(p.Detail or 'UNKNOWN'):sub(1,180))
   end
  elseif p.Action=='STOP' then
   assert(state.owner==pid and state.unitID==p.UnitID and state.phase~='ENDED','BOUND_TEAM_REQUIRED')
   mutating=true;error('ISOLATION_OR_REQUEST_STOP: '..tostring(p.Detail or 'UNKNOWN'):sub(1,180))
  elseif p.Action=='END' then
   -- Explicit cleanup of the exact currently owned prototype, including an unbound loaded one.
   local u=owned(pid,p.UnitID,true)
   assert(#list(pid)==1,'SPAWN_COUNT_UNCONFIRMED')
   mutating=true;state.owner=pid;state.unitID=p.UnitID;state.phase='ENDING';recovering=false
   save() -- Native destruction follows durable reservation.
   Players[pid]:GetUnits():Destroy(u)
   assert(not Players[pid]:GetUnits():FindID(p.UnitID) and #list(pid)==0,'END_UNCONFIRMED')
   state={owner=pid,phase='ENDED'};missionStatus=nil;missionReason=nil;missionRetryKey=nil;missionUnknownReads=0
  end
  if mutating then save()end
  local v=snapshot(pid)
  if p.Action=='DISPATCH' and state.phase=='TRAVELLING' then v.nativePermit=state.permit end
  return v
 end
 for pid in pairs(Players)do if P.IsTestPlayer(pid)then load(pid);break end end
 publishActivity() -- Restored activity is observation-only until a fresh UI sample.
 local data={};shared.ExpeditionGate=data
 -- B219 disposable-save experiment: read exact idle binding, then suspend this
 -- Gate in memory before movement. Never amend saved coordinates or history.
 function data.MovementProbeRead(pid)
  load(pid)
  assert(not movementProbeLocked and not busy and not storeBlocked and not recovering,'PROBE_GATE_NOT_IDLE')
  assert(state.owner==pid and (state.phase=='CREATED' or state.phase=='ARRIVED')
   and (not state.activityMode or state.activityMode=='NONE') and not state.activityOwned and not state.activityPending,'PROBE_TEAM_NOT_IDLE')
  source();local u=owned(pid,state.unitID)
  assert(state.nameVerified and u:GetName()==state.expectedName and u:GetX()==state.x and u:GetY()==state.y,'PROBE_BINDING_CHANGED')
  return {unitID=state.unitID,sourceCity=state.sourceCity,teamKey=state.teamKey}
 end
 function data.MovementProbeLock(pid,id)
  assert(data.MovementProbeRead(pid).unitID==id,'PROBE_BINDING_CHANGED')
  movementProbeLocked=true
 end
 -- Training shares this exact saved reservation with creation/travel. The
 -- adapter owns native event correlation; it cannot write this record directly.
 data.Training={}
 local T=data.Training
 function T.Read(pid)
  load(pid);local v=savedState();v.blocked=storeBlocked;return v
 end
 function T.Available(pid)
  load(pid)
  return not storeBlocked and not busy and (not state.phase or state.phase=='ENDED') and #list(pid)==0
 end
 function T.Reserve(pid,cid,token)
  assert(P.IsTestPlayer(pid) and T.Available(pid),'TRAINING_CAPACITY_RESERVED')
  local c=Players[pid]:GetCities():FindID(cid)
  assert(c and c:GetOwner()==pid,'OWN_CITY_REQUIRED')
  local f=shared.EffectiveFacts.Read(pid,c)
  assert(f.specialization=='CULTURE' and f.active==4 and not f.investmentPending,'CULTURE_ACTIVE_IV_REQUIRED')
  assert(f.token and c:GetProperty('SPC_DEV_BINDING_B013_TOKEN')==f.token,'SOURCE_REFERENCE_UNKNOWN')
  namePool(pid)
  local ref=SPCNetworkInput.Reference(c);assert(type(ref)=='string' and #ref>0,'SOURCE_REFERENCE_UNKNOWN')
  state={owner=pid,phase='TRAINING',sourceCity=cid,sourceName=c:GetName(),sourceRef=ref,x=c:GetX(),y=c:GetY(),trainingToken=token,trainingTurn=Game.GetCurrentGameTurn()}
  save(true);source();publishActivity()
 end
 function T.Evidence(pid,token,field,value)
  assert(not storeBlocked and state.owner==pid and state.phase=='TRAINING' and state.trainingToken==token,'TRAINING_RESERVATION_CHANGED')
  source()
  assert(field=='trainingQueued' or field=='trainingBorn' or field=='trainingCompleted','TRAINING_BAD_EVIDENCE')
  if field=='trainingBorn' then
   assert(int(value) and (not state.trainingBorn or state.trainingBorn==value),'TRAINING_MULTIPLE_BIRTHS')
   local u=owned(pid,value);assert(u:GetX()==state.x and u:GetY()==state.y,'TRAINING_BIRTH_ENDPOINT_CHANGED')
  else assert(value==true,'TRAINING_BAD_EVIDENCE')end
  state[field]=value
  if field~='trainingQueued' and not state.trainingReceiptTurn then state.trainingReceiptTurn=Game.GetCurrentGameTurn()end
  save();source();publishActivity()
 end
 function T.Finish(pid,token)
  assert(not storeBlocked and state.owner==pid and state.phase=='TRAINING' and state.trainingToken==token,'TRAINING_RESERVATION_CHANGED')
  assert(state.trainingQueued and state.trainingCompleted and state.trainingBorn,'TRAINING_RECEIPT_INCOMPLETE')
  source();local all=list(pid);assert(#all==1 and all[1]:GetID()==state.trainingBorn,'TRAINING_UNIT_AMBIGUOUS')
  local u=owned(pid,state.trainingBorn)
  assert(u:GetX()==state.x and u:GetY()==state.y,'TRAINING_BIRTH_ENDPOINT_CHANGED')
  state.unitID=u:GetID();state.createdID=state.unitID
  state.teamKey=string.format('E%X-%X-%X',pid,state.createdID,envelope.generation)
  state.phase='NAMING';state.nameVerified=false
  state.trainingReceiptTurn=nil;state.trainingBorn=nil;state.trainingCompleted=nil;state.trainingQueued=nil;state.trainingTurn=nil
  save();source();local confirmed=owned(pid,state.unitID)
  assert(confirmed:GetX()==state.x and confirmed:GetY()==state.y,'TRAINING_BIRTH_ENDPOINT_CHANGED')
  publishActivity()
 end
 -- B210: no Expedition-family unit exists for the player (live native read).
 function T.NoUnits(pid)load(pid);return #list(pid)==0 end
 function T.Cancel(pid,token)
  assert(not storeBlocked and state.owner==pid and state.phase=='TRAINING' and state.trainingToken==token,'TRAINING_RESERVATION_CHANGED')
  assert(not state.trainingBorn and not state.trainingCompleted and #list(pid)==0,'TRAINING_OUTCOME_UNKNOWN')
  source();state={owner=pid,phase='ENDED'};save();publishActivity()
 end
 function T.Hold(err)hold(err);publishActivity()end

 function data.Request(pid,p)
  if not P.IsTestPlayer(pid) or type(p)~='table' or type(p.Token)~='string' or #p.Token==0 or #p.Token>100 then return end
  if movementProbeLocked then
   ExposedMembers.SPC_ExpeditionGateReply={owner=pid,token=p.Token,phase=state.phase,error='MOVEMENT_PROBE_RELOAD_REQUIRED'}
   return
  end
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
  v.activityRevision=revision -- Correlate this diagnostic read with the scalar transition mirror.
  -- Reconnect-readable final result, after handle/save, any hold, and publication.
  -- A blocked write retains the last confirmed envelope; never label it idle success.
  if p.Action=='DISPATCH' or p.Action=='TASK' or p.Action=='ACTIVITY' then
   local known={ARMED=true,RECOVERED=true,ASLEEP=true,RELEASED=true,REJECTED=true,FAILED=true}
   traceState('GATE_RESULT',nil,{requestAction=p.Action,requestResult=known[p.Result] and p.Result or 'NONE',
    requestKey=p.ActivityKey,requestMission=({PEOPLE=true,WORKS=true,PLACES=true})[p.Mission] and p.Mission or nil,
    requestAccepted=ok and v.error==nil,reason=v.error})
  end
  print('[SPC][B191][N1_SPY] action='..tostring(p.Action)..' owner='..pid..' unit='..tostring(v.unitID)..' phase='..v.phase..' error='..tostring(v.error))
 end
 GameEvents.SPC_ExpeditionGateRequest.Add(data.Request)
 function data.Turn(pid)
  if movementProbeLocked then return end
  if placementWatch and pid==placementWatch.owner then closePlacement('TURN_CLOSE')end
  if P.IsTestPlayer(pid)then load(pid)end
  if busy or not P.IsTestPlayer(pid) or state.owner~=pid or not state.unitID or state.phase=='HELD' or state.phase=='ENDED' then return end
  busy=true;shared.RequestDepth=(shared.RequestDepth or 0)+1
  step='TURN';local ok,err=pcall(function()
   observe(true)
  end)
  shared.RequestDepth=shared.RequestDepth-1;busy=false
  mutating=false;if not ok then hold(err)end
  publishActivity()
 end
 if Events.LoadScreenClose then Events.LoadScreenClose.Add(function()
  closePlacement('LOAD_CLOSE')
  if state.owner then data.Turn(state.owner)end
 end)end
 Events.PlayerTurnActivated.Add(data.Turn) -- Owned endpoints/unit; pending travel adds one player-unit collection read; no task-turn scan.
 if Events.CityTransfered then Events.CityTransfered.Add(function()
  if not movementProbeLocked and not busy and state.unitID and state.phase~='ENDED' and state.phase~='HELD' then
   missionRetryKey=nil;missionUnknownReads=0
   step='REFERENCE';local ok,err=pcall(function()observe();if state.phase=='TRAVELLING' then target(state.owner,state.target)end end);if not ok then hold(err)end
   publishActivity()
  end
 end)end
 if Events.UnitRemovedFromMap then Events.UnitRemovedFromMap.Add(function(pid,id)
  if placementWatch and pid==placementWatch.owner and id==placementWatch.id then closePlacement('REMOVED_CLOSE')end
  if pid==state.owner and id==state.unitID then state.removedEvents=math.min(99,(state.removedEvents or 0)+1)end
 end)end
end
