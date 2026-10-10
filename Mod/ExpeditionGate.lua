-- B178: explicit N1 engine gate. No mission engine, city archive, Property or reward writes.
SPCExpeditionGate={KIND='UNIT_SPC_EXPEDITION_GATE'}
function SPCExpeditionGate.Start(P,shared)
 local M=SPCExpeditionGate
 local state={};local busy=false;local lastToken;local lastReply;local watch
 local function list(pid)
  local result={}
  for _,u in Players[pid]:GetUnits():Members()do
   local r=P.Info('Units',u:GetType())
   if r and r.UnitType==M.KIND then result[#result+1]=u end
  end
  return result
 end
 local function owned(pid,id)
  local u=Players[pid]:GetUnits():FindID(id)
  assert(u and u:GetOwner()==pid and P.Info('Units',u:GetType()).UnitType==M.KIND,'TEST_TEAM_CHANGED')
  return u
 end
 local function snapshot(pid)
  local units=list(pid);local v={owner=pid,count=#units,turn=Game.GetCurrentGameTurn(),phase=state.phase or 'IDLE'}
  if #units==1 then
   local u=units[1];v.unitID=u:GetID();v.x=u:GetX();v.y=u:GetY()
  end
  if state.owner==pid and state.unitID then
   v.createdID=state.unitID
   local u=Players[pid]:GetUnits():FindID(state.unitID)
   v.sameUnit=u~=nil and u:GetOwner()==pid and P.Info('Units',u:GetType()).UnitType==M.KIND
   v.sourceCity=state.sourceCity
  end
  if watch and watch.owner==pid then
   v.watchID=watch.id;v.watchX=watch.x;v.watchY=watch.y;v.removedEvents=watch.removed
   local u=Players[pid]:GetUnits():FindID(watch.id)
   v.watchedAlive=u~=nil and u:GetOwner()==pid and P.Info('Units',u:GetType()).UnitType==M.KIND
   if v.watchedAlive then v.watchedX=u:GetX();v.watchedY=u:GetY()end
  end
  return v
 end
 local function handle(pid,p)
  assert(type(p)=='table' and type(p.Token)=='string' and #p.Token>0 and #p.Token<=100,'BAD_REQUEST')
  assert(P.IsTestPlayer(pid),'SUPPORTED_PLAYER_REQUIRED')
  assert(p.Action=='READ' or p.Action=='CREATE' or p.Action=='ARM' or p.Action=='END','BAD_ACTION')
  if p.Action=='READ' then return snapshot(pid)end
  if p.Action=='CREATE' then
   assert(state.phase~='CREATING' and state.phase~='HELD','SPAWN_UNCERTAIN_NO_RETRY')
   assert(#list(pid)==0,'EXISTING_TEST_TEAM_COUNTS')
   local c=Players[pid]:GetCities():FindID(p.CityID)
   assert(c and c:GetOwner()==pid,'OWN_CITY_REQUIRED')
   local f=shared.EffectiveFacts.Read(pid,c)
   assert(f.specialization=='CULTURE' and f.active==4 and not f.investmentPending,'CULTURE_ACTIVE_IV_REQUIRED')
   for _,u in Players[pid]:GetUnits():Members()do
    local r=P.Info('Units',u:GetType())
    assert(u:GetX()~=c:GetX() or u:GetY()~=c:GetY() or r.FormationClass~='FORMATION_CLASS_CIVILIAN','CITY_CENTER_OCCUPIED')
   end
   local r=P.Info('Units',M.KIND)
   assert(r and (r.CanRetreatWhenCaptured==true or r.CanRetreatWhenCaptured==1)
    and (r.Spy==false or r.Spy==0),'TEST_DATABASE_NOT_READY')
   -- Reserve before the native call; unknown outcome must not spawn a second unit.
   state={owner=pid,phase='CREATING',sourceCity=c:GetID()}
   local u=UnitManager.InitUnit(pid,M.KIND,c:GetX(),c:GetY())
   assert(u and u:GetOwner()==pid,'SPAWN_UNCONFIRMED')
   state.unitID=u:GetID();owned(pid,state.unitID)
   assert(#list(pid)==1,'SPAWN_COUNT_UNCONFIRMED')
   state.phase='CREATED';watch=nil
  elseif p.Action=='ARM' then
   local u=owned(pid,p.UnitID)
   watch={owner=pid,id=u:GetID(),x=u:GetX(),y=u:GetY(),removed=0}
  elseif p.Action=='END' then
   assert(state.phase~='HELD' and state.phase~='CREATING','SPAWN_UNCERTAIN_NO_RETRY')
   local u=owned(pid,p.UnitID)
   Players[pid]:GetUnits():Destroy(u)
   assert(not Players[pid]:GetUnits():FindID(p.UnitID),'END_UNCONFIRMED')
   state={phase='ENDED'};watch=nil
  end
  return snapshot(pid)
 end
 local data={};shared.ExpeditionGate=data
 function data.Request(pid,p)
  if not P.IsTestPlayer(pid) or type(p)~='table' or type(p.Token)~='string' or #p.Token==0 or #p.Token>100 then return end
  if busy then return end
  if p.Token==lastToken then ExposedMembers.SPC_ExpeditionGateReply=lastReply;return end
  busy=true;shared.RequestDepth=(shared.RequestDepth or 0)+1
  local ok,v=pcall(handle,pid,p)
  shared.RequestDepth=shared.RequestDepth-1;busy=false
  if not ok then
   if state.phase=='CREATING' then state.phase='HELD' end
   local reason=tostring(v):match(':%d+:%s*([A-Z][A-Z0-9_]+)') or tostring(v):match('^([A-Z][A-Z0-9_]+)') or 'API_UNAVAILABLE'
   v={owner=pid,error=reason,phase=state.phase or 'IDLE'}
  end
  v.token=p.Token;lastToken=p.Token;lastReply=v
  ExposedMembers.SPC_ExpeditionGateReply=v
  print('[SPC][B178][N1_GATE] action='..tostring(p.Action)..' owner='..pid..' unit='..tostring(v.unitID)..' phase='..v.phase..' error='..tostring(v.error))
 end
 GameEvents.SPC_ExpeditionGateRequest.Add(data.Request)
 -- One owned watched unit only; no scans, registrations, timers or resurrection here.
 if Events.UnitRemovedFromMap then Events.UnitRemovedFromMap.Add(function(pid,id)
  if watch and pid==watch.owner and id==watch.id then watch.removed=math.min(999,watch.removed+1)end
 end)end
end
