-- B219: explicit disposable-save comparison, never a mission transport fallback.
-- One tested native call per load. No Property, capacity, binding or reward writes.
SPCExpeditionMovementProbe={}
function SPCExpeditionMovementProbe.Start(P,shared)
 local used=false;local busy=false;local lastToken;local lastReply;local watch
 local function integer(v)return type(v)=='number' and v>=0 and v<math.huge and v%1==0 end
 local function flag(v)return v==true or v==1 end
 local function unit(pid,id)
  local player=Players[pid];local u=player and player:GetUnits():FindID(id)
  assert(u and u:GetOwner()==pid and u:GetID()==id,'UNIT_CHANGED');return u
 end
 local function scalar(u,k)
  local ok,v=pcall(function()return u[k](u)end)
  if ok and (type(v)=='number' or type(v)=='boolean')then return tostring(v)end
  return 'UNKNOWN'
 end
 local function log(s)pcall(print,'[SPC][B191][N1_TASK] movementProbe='..s)end
 local function occupants(x,y)
  assert(Units and type(Units.GetUnitsInPlot)=='function','OCCUPANTS_UNKNOWN')
  local list=Units.GetUnitsInPlot(x,y);assert(type(list)=='table','OCCUPANTS_UNKNOWN')
  local out={};for _,u in pairs(list)do
   assert(#out<8,'OCCUPANTS_LIMIT')
   local r=P.Info('Units',u:GetType());assert(r,'OCCUPANTS_UNKNOWN')
   out[#out+1]={owner=u:GetOwner(),id=u:GetID(),kind=u:GetType(),x=u:GetX(),y=u:GetY(),spy=flag(r.Spy),stackable=flag(r.Stackable)}
  end
  table.sort(out,function(a,b)return a.owner==b.owner and a.id<b.id or a.owner<b.owner end)
  return out
 end
 local function signature(list)
  local out={};for _,v in ipairs(list)do out[#out+1]=table.concat({v.owner,v.id,v.kind,v.x,v.y},':')end
  return table.concat(out,';')
 end
 local function sameOthers(list)
  for _,v in ipairs(list)do
   local ok,u=pcall(unit,v.owner,v.id)
   if not ok or u:GetType()~=v.kind or u:GetX()~=v.x or u:GetY()~=v.y then return false end
  end
  return true
 end
 local function sample(stage,ex,ey,record)
  local w=record or watch;if not w then return end
  pcall(function()
   local p=Players[w.owner];local u=p and p:GetUnits():FindID(w.id)
   log(stage..' method='..w.method..' owner='..w.owner..' unit='..w.id..' target='..w.x..','..w.y
    ..' actual='..scalar(u,'GetX')..','..scalar(u,'GetY')..' readOwner='..scalar(u,'GetOwner')..' readID='..scalar(u,'GetID')
    ..' type='..scalar(u,'GetType')..' operation='..scalar(u,'GetSpyOperation')..' activity='..scalar(u,'GetActivityType')
    ..' moves='..scalar(u,'GetMovesRemaining')..' event='..tostring(ex or 'NA')..','..tostring(ey or 'NA'))
   local ok,list=pcall(occupants,w.x,w.y)
   if not ok then log(stage..' occupants=UNKNOWN_OR_LIMIT');return end
   for i,v in ipairs(list)do
    log(stage..' occupant='..i..' owner='..v.owner..' unit='..v.id..' type='..v.kind..' xy='..v.x..','..v.y
     ..' spy='..tostring(v.spy)..' stackable='..tostring(v.stackable))
   end
   log(stage..' occupants='..#list..' originalOthersUnchanged='..tostring(sameOthers(w.others)))
  end)
 end
 local function close(reason)if watch then sample(reason);watch=nil end end
 local function event(kind,pid,id,x,y)
  local w=watch;if not w or w.owner~=pid or w.id~=id then return end
  w.events=w.events+1;sample(kind,x,y)
  if w.events>=8 then close('EVENT_LIMIT')end
 end
 if Events.UnitMoveComplete then Events.UnitMoveComplete.Add(function(...)event('MOVE_EVENT',...)end)end
 if Events.UnitTeleported then Events.UnitTeleported.Add(function(...)event('TELEPORT_EVENT',...)end)end
 if Events.PlayerTurnActivated then Events.PlayerTurnActivated.Add(function(pid)
  if watch and watch.owner==pid then close('TURN_CLOSE')end
 end)end
 if Events.UnitRemovedFromMap then Events.UnitRemovedFromMap.Add(function(pid,id)
  if watch and watch.owner==pid and watch.id==id then close('REMOVED_CLOSE')end
 end)end
 if Events.LoadScreenClose then Events.LoadScreenClose.Add(function()close('LOAD_CLOSE')end)end
 local function run(pid,p)
  assert(not used,'RELOAD_REQUIRED')
  assert(p.Method=='PlaceUnit' or p.Method=='MoveUnit','METHOD_INVALID')
  assert(integer(p.UnitID) and integer(p.X) and integer(p.Y),'INPUT_INVALID')
  assert(p.SampleTurn==Game.GetCurrentGameTurn() and p.NativeOperation==-1,'NATIVE_IDLE_UNKNOWN')
  local u=unit(pid,p.UnitID);local r=P.Info('Units',u:GetType())
  assert(r and (r.UnitType=='UNIT_SPY' or r.UnitType=='UNIT_SPC_EXPEDITION_SPY') and flag(r.Spy),'SPY_REQUIRED')
  assert(u:GetType()==p.Kind and u:GetName()==p.Name and u:GetX()==p.FromX and u:GetY()==p.FromY,'UNIT_SAMPLE_CHANGED')
  if type(u.GetSpyOperation)=='function'then assert(u:GetSpyOperation()==-1,'NATIVE_MISSION_ACTIVE')end
  local gate=shared.ExpeditionGate
  assert(gate and gate.MovementProbeRead and gate.MovementProbeLock,'GATE_UNAVAILABLE')
  local binding=gate.MovementProbeRead(pid)
  if r.UnitType=='UNIT_SPC_EXPEDITION_SPY'then assert(binding.unitID==u:GetID(),'UNBOUND_TEAM')end
  local target=Map.GetPlot(p.X,p.Y);assert(target,'TARGET_UNKNOWN')
  local visibility=PlayersVisibility and PlayersVisibility[pid]
  assert(visibility and visibility:IsRevealed(p.X,p.Y)==true,'TARGET_UNREVEALED')
  assert(target:IsWater()==false and target:IsImpassable()==false,'TARGET_NOT_LAND')
  assert(u:GetX()~=p.X or u:GetY()~=p.Y,'ALREADY_ON_TARGET')
  local others=occupants(p.X,p.Y);assert(#others>0,'OCCUPIED_TARGET_REQUIRED')
  local civilian=false
  for _,v in ipairs(others)do
   local info=P.Info('Units',v.kind)
   assert(not v.spy,'TARGET_CONTAINS_SPY')
   if info and info.FormationClass=='FORMATION_CLASS_CIVILIAN' and not v.spy then civilian=true end
  end
  assert(civilian,'CIVILIAN_TARGET_REQUIRED')
  -- Deterministic common adjacent pad. Both unit types and both methods can use
  -- the same saved world; an occupied/unknown pad is never cleared or displaced.
  local pad
  for d=0,5 do
   local plot=Map.GetAdjacentPlot(p.X,p.Y,d)
   if plot and plot:IsWater()==false and plot:IsImpassable()==false and visibility:IsRevealed(plot:GetX(),plot:GetY())==true then
    local ok,list=pcall(occupants,plot:GetX(),plot:GetY())
    if ok and #list==0 then pad=plot;break end
   end
  end
  assert(pad,'EMPTY_ADJACENT_PAD_REQUIRED')
  assert(UnitManager and type(UnitManager.PlaceUnit)=='function' and type(UnitManager[p.Method])=='function'
   and type(UnitManager.RestoreMovement)=='function','MOVEMENT_API_UNAVAILABLE')
  -- Native movement is the only mutation. Lock ordinary team processing before
  -- it can observe a deliberately displaced test subject. Reload ends this lease.
  gate.MovementProbeLock(pid,binding.unitID);used=true
  watch={owner=pid,id=u:GetID(),x=p.X,y=p.Y,method=p.Method,others=others,events=0}
  log('BEGIN method='..p.Method..' kind='..r.UnitType..' original='..p.FromX..','..p.FromY..' pad='..pad:GetX()..','..pad:GetY()
   ..' sourceCity='..binding.sourceCity..' team='..binding.teamKey..' moveEvent='..tostring(Events.UnitMoveComplete~=nil)..' teleportEvent='..tostring(Events.UnitTeleported~=nil))
  local record=watch
  log('SUBJECT spy='..tostring(r.Spy)..' stackable='..tostring(r.Stackable)..' formation='..tostring(r.FormationClass)..' domain='..tostring(r.Domain))
  sample('PRE_STAGE',nil,nil,record)
  -- This known primitive only prepares an EMPTY tile; its outcome is separately
  -- reported and cannot be mistaken for the occupied-destination test.
  UnitManager.RestoreMovement(u);UnitManager.PlaceUnit(u,pad:GetX(),pad:GetY())
  sample('STAGED',nil,nil,record)
  u=unit(pid,p.UnitID)
  assert(u:GetType()==p.Kind and u:GetName()==p.Name,'STAGING_IDENTITY_CHANGED')
  assert(u:GetX()==pad:GetX() and u:GetY()==pad:GetY(),'STAGING_NOT_EXACT')
  assert(sameOthers(others) and signature(occupants(p.X,p.Y))==signature(others),'OCCUPANCY_CHANGED')
  assert(signature(occupants(pad:GetX(),pad:GetY()))==signature({{owner=pid,id=u:GetID(),kind=u:GetType(),x=u:GetX(),y=u:GetY()}}),'PAD_CHANGED')
  UnitManager.RestoreMovement(u);sample('PRE_CALL',nil,nil,record)
  UnitManager[p.Method](u,p.X,p.Y)
  sample('POST_CALL',nil,nil,record)
  u=unit(pid,p.UnitID)
  assert(u:GetType()==p.Kind and u:GetName()==p.Name,'IDENTITY_CHANGED')
  assert(sameOthers(others),'OTHER_UNIT_CHANGED')
  local exact=u:GetX()==p.X and u:GetY()==p.Y
  return {status=exact and 'EXACT' or 'NOT_EXACT',x=u:GetX(),y=u:GetY(),unitID=u:GetID(),method=p.Method}
 end
 local function request(pid,p)
  if not P.IsTestPlayer(pid) or type(p)~='table' or type(p.Token)~='string' or #p.Token==0 or #p.Token>100 or busy then return end
  if p.Token==lastToken then ExposedMembers.SPC_ExpeditionMovementReply=lastReply;return end
  busy=true;local ok,v=pcall(run,pid,p);busy=false
  if not ok then
   local code=tostring(v):match('([A-Z][A-Z_]+)$') or 'UNCLASSIFIED_ERROR'
   v={status='STOP',reason=code};sample('ERROR');log('STOP reason='..code..' reload='..tostring(used))
  end
  v.owner=pid;v.token=p.Token;v.version=P.VERSION;v.reload=used
  lastToken=p.Token;lastReply=v;ExposedMembers.SPC_ExpeditionMovementReply=v
  log('RESULT status='..v.status..' method='..tostring(v.method or p.Method)..' reload='..tostring(used))
 end
 GameEvents.SPC_ExpeditionMovementRequest.Add(request)
end
