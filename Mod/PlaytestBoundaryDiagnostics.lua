-- B399 disposable observers only. No business owner consumes this module.
-- Disable ENABLED, call Stop(), or remove the optional Gameplay startup/file.
if type(SPCPlaytestBoundaryDiagnostics)=='table'and SPCPlaytestBoundaryDiagnostics.VERSION==399 then return end
SPCPlaytestBoundaryDiagnostics={VERSION=399,ENABLED=true,TURN_LIMIT=6,TREASURY_LIMIT=96,POSITION_LIMIT=64,CHANGE_LIMIT=8,PHASE_LIMIT=512}
local M=SPCPlaytestBoundaryDiagnostics
local instance
local function integer(n)return type(n)=='number'and n>=0 and n%1==0 and n<9007199254740991 end
local function scalar(v)
 if type(v)=='boolean'then return v end
 if type(v)=='number'and v==v and v>-math.huge and v<math.huge then return v end
 if type(v)=='string'and #v<=100 and not v:find('[^%w_:%-%.|]')then return v end
end
local function nativeRead(object,method,arg,count)
 local ok,value=pcall(function()
  local fn=object and object[method];if type(fn)~='function'then return 'UNAVAILABLE'end
  if count then count()end
  if arg~=nil then return fn(object,arg)end
  return fn(object)
 end)
 if not ok then return 'READ_ERROR'end
 if type(value)=='boolean'or type(value)=='number'and scalar(value)~=nil then return value end
 if value=='UNAVAILABLE'then return value end
 return value==nil and 'NIL'or 'INVALID_TYPE'
end
function M.Stop()if instance then instance.Stop('EXPLICIT_STOP')end end
function M.Observe(point,build)
 if M.ENABLED and instance then pcall(instance.Observe,point,build)end
end
function M.Start(P,shared)
 if instance then instance.Stop(M.ENABLED and 'REATTACH'or 'DISABLED')end
 if not M.ENABLED then return end
 local logger=SPCExpeditionTrainingDiagnostics
 if type(logger)~='table'or logger.ENABLED==false or type(logger.New)~='function'then return end
 local good,trace=pcall(logger.New,P,'PLAYTEST_BOUNDARY')
 if not good or type(trace)~='table'or trace.id=='DISABLED'or type(trace.Record)~='function'then return end
 local api={};local hooks={};local live=true;local busy=false;local firstTurn;local ordinal=0
 local phaseReads,playerReads=0,0;local cachedPlayer
 local function count()pcall(function()if type(P.Count)=='function'then P.Count('observer_native_attempt')end end)end
 local function read(object,method,arg)return nativeRead(object,method,arg,count)end
 local moneyUsed,positionUsed=0,0;local moneyNotice,positionNotice=false,false
 local changeTurn,changes=nil,0;local boundaries={};local lastBalance;local watch;local publishPending=false
 local function emit(stage,data)
  ordinal=ordinal+1;data.observationSeq=ordinal;pcall(trace.Record,stage,data)
 end
 function api.Stop(reason)
  if not live then return end;live=false
  for _,h in ipairs(hooks)do pcall(h.remove,h.fn)end
  hooks={};watch=nil;lastBalance=nil;publishPending=false
  if instance==api then instance=nil end
  if reason~='DISABLED'then emit('PLAYTEST_PROBE_STATUS',{reason=reason,eventCount=moneyUsed,eventTotal=positionUsed,point='STOP',eventTruncated=reason=='PHASE_LIMIT'})end
 end
 -- Observer-only identity admission is cached,not re-read for each event.
 -- The existing identity helper has at most four native/configuration calls.
 local function localPlayer()
  if cachedPlayer~=nil then return cachedPlayer end
  if playerReads>=4 then api.Stop('LOCAL_PLAYER_UNAVAILABLE');return end
  playerReads=playerReads+1;count()
  local ok,pid=pcall(Game.GetLocalPlayer)
  if ok and integer(pid)then
   local checked,allowed=pcall(P.IsTestPlayer,pid)
   if checked and allowed then cachedPlayer=pid;return pid end
  end
 end
 local function permit(pid)
  if not live then return end
  if not M.ENABLED then api.Stop('DISABLED');return end
  if not integer(pid)or pid~=localPlayer()then return end
  if phaseReads>=M.PHASE_LIMIT then api.Stop('PHASE_LIMIT');return end
  phaseReads=phaseReads+1;count();local t=Game.GetCurrentGameTurn();if not integer(t)then return end
  cachedPlayer=pid
  if firstTurn==nil then firstTurn=t end
  if t<firstTurn or t>=firstTurn+M.TURN_LIMIT then api.Stop('WINDOW_END');return end
  return t
 end
 local function money(point,pid,change)
  if change and changes>=M.CHANGE_LIMIT then
   if changes==M.CHANGE_LIMIT then changes=changes+1;emit('PLAYTEST_PROBE_STATUS',{owner=pid,point='CHANGE_LIMIT',reason='BUDGET_STOP',eventTruncated=true,eventCount=M.CHANGE_LIMIT})end
   return
  end
  if moneyUsed>=M.TREASURY_LIMIT then
   if not moneyNotice then moneyNotice=true;emit('PLAYTEST_PROBE_STATUS',{owner=pid,point='TREASURY_LIMIT',reason='BUDGET_STOP',eventTruncated=true,eventCount=moneyUsed})end
   return
  end
  local t=permit(pid);if not t then return end
  if change then
   if changeTurn~=t then changeTurn=t;changes=0 end
   changes=changes+1
  end
  moneyUsed=moneyUsed+1 -- consume before optional native access/reentry
  local player=Players[pid];local treasury
  local treasuryOK=pcall(function()count();treasury=player and player:GetTreasury()end)
  local balance=treasuryOK and read(treasury,'GetGoldBalance')or 'READ_ERROR';local delta
  if type(balance)=='number'and type(lastBalance)=='number'then delta=balance-lastBalance end
  lastBalance=type(balance)=='number'and balance or nil
  local b=shared and shared.NetworkBridge and shared.NetworkBridge.players and shared.NetworkBridge.players[pid]
  emit('PLAYTEST_TREASURY',{owner=pid,point=point,goldBalance=balance,actualDelta=delta,
   goldYield=read(treasury,'GetGoldYield'),maintenance=read(treasury,'GetTotalMaintenance'),
   buildingMaintenance=read(treasury,'GetBuildingMaintenance'),districtMaintenance=read(treasury,'GetDistrictMaintenance'),
   unitMaintenance=read(treasury,'GetUnitMaintenance'),wmdMaintenance=read(treasury,'GetWMDMaintenance'),
   ownerTurnActive=read(player,'IsTurnActive'),networkRevalidation=b and b.revalidation,networkAvailability=b and b.availability})
 end
 local function position(point)
  local w=watch;if not w then return end
  if positionUsed>=M.POSITION_LIMIT then
   if not positionNotice then positionNotice=true;emit('PLAYTEST_PROBE_STATUS',{owner=w.owner,point='POSITION_LIMIT',reason='BUDGET_STOP',eventTruncated=true,eventCount=positionUsed})end
   return
  end
  if not permit(w.owner)then return end
  positionUsed=positionUsed+1
  local u;pcall(function()count();local units=Players[w.owner]:GetUnits();count();u=units:FindID(w.unitID)end)
  local owner,id=read(u,'GetOwner'),read(u,'GetID')
  local valid=owner==w.owner and id==w.unitID
  local data={owner=w.owner,eventUnit=w.unitID,point=point,phase=w.phase,x=w.x,y=w.y,
   targetOwner=w.targetOwner,targetCity=w.targetCity,readStatus=valid and 'OWNER_ID_MATCH'or 'UNAVAILABLE'}
  if valid then
   data.actualX=read(u,'GetX');data.actualY=read(u,'GetY');data.unitIndex=read(u,'GetType')
   data.spyOperation=read(u,'GetSpyOperation');data.movesRemaining=read(u,'GetMovesRemaining')
   local ok,value=pcall(function()count();return UnitManager.GetActivityType(u)end);data.nativeActivity=ok and type(value)=='number'and scalar(value)or 'UNAVAILABLE'
   if integer(w.targetOwner)then
    local diplomacy;pcall(function()count();diplomacy=Players[w.owner]:GetDiplomacy()end)
    local border=read(diplomacy,'HasOpenBordersFrom',w.targetOwner)
    data.reason=border==true and 'BORDER_OPEN'or border==false and 'BORDER_CLOSED'or 'BORDER_UNAVAILABLE'
   end
  end
  emit('PLAYTEST_POSITION',data)
 end
 function api.Observe(point,build)
  if not live or busy or not M.ENABLED or point~='EXPEDITION_TURN'then return end
  -- Builder is scalar-only; native sampling still requires this module's window.
  if positionUsed>=M.POSITION_LIMIT then
   if not positionNotice then positionNotice=true;emit('PLAYTEST_PROBE_STATUS',{point='POSITION_LIMIT',reason='BUDGET_STOP',eventTruncated=true,eventCount=positionUsed})end
   return
  end
  busy=true
  local ok=pcall(function()
   local v=build();if type(v)~='table'or not permit(v.owner)then return end
   if not integer(v.eventUnit)or v.phase=='ENDED'then watch=nil;return end
   watch={owner=v.owner,unitID=v.eventUnit,phase=scalar(v.phase),x=scalar(v.x),y=scalar(v.y),
    targetOwner=scalar(v.targetOwner),targetCity=scalar(v.targetCity)}
   position(point)
  end)
  busy=false
 end
 local function guarded(fn)
  return function(...)
   if not live or busy then return end
   if not M.ENABLED then api.Stop('DISABLED');return end
   busy=true;pcall(fn,...);busy=false
  end
 end
 local function hook(source,name,fn)
  local ok,add,remove=pcall(function()
   local event=source and source[name];return event and event.Add,event and event.Remove
  end)
  -- An optional observer never installs an unremovable native subscription.
  if ok and type(add)=='function'and type(remove)=='function'then
   local callback=guarded(fn);hooks[#hooks+1]={remove=remove,fn=callback}
   local added=pcall(add,callback);if not added then pcall(remove,callback)end
  end
 end
 -- END opens a transition allowance; ACTIVATED opens the actionable interval.
 -- Repeated unchanged lifecycle callbacks cannot replenish either allowance.
 local function boundary(point,pid)
  local t=permit(pid);if not t then return end
  if boundaries[point]~=t then boundaries[point]=t;changes=0;changeTurn=t end
  money(point,pid)
 end
 local function localPoint(point)
  return function()local pid=localPlayer();if pid then money(point,pid);publishPending=live end end
 end
 hook(Events,'PlayerTurnDeactivated',function(pid)boundary('END',pid);if watch and watch.owner==pid then position('END')end end)
 hook(GameEvents,'PlayerTurnStarted',function(pid)money('STARTED',pid)end)
 hook(Events,'PlayerTurnActivated',function(pid)boundary('ACTIVATED',pid)end)
 hook(Events,'LocalPlayerTurnBegin',localPoint('LOCAL_BEGIN'))
 hook(Events,'LocalPlayerTurnEnd',localPoint('LOCAL_END'))
 hook(Events,'LoadScreenClose',localPoint('LOAD_CLOSE'))
 for _,name in ipairs({'TreasuryChanged','PlayerTreasuryChanged','PlayerGoldChanged'})do
  hook(Events,name,function(pid)money(name:upper(),pid,true)end)
 end
 hook(Events,'GameCoreEventPublishComplete',function()
  if not publishPending then return end;publishPending=false
  local pid=localPlayer();if pid then money('FIRST_PUBLISH',pid)end
 end)
 for _,name in ipairs({'UnitMoveComplete','UnitTeleported','UnitActivityChanged'})do
  hook(Events,name,function(pid,id)if watch and pid==watch.owner and id==watch.unitID then position(name:upper())end end)
 end
 hook(Events,'DiplomacyRelationshipChanged',function(a,b)
  if watch and ((a==watch.owner and b==watch.targetOwner)or(b==watch.owner and a==watch.targetOwner))then position('RELATIONSHIP')end
 end)
 hook(Events,'UnitRemovedFromMap',function(pid,id)if watch and pid==watch.owner and id==watch.unitID then watch=nil end end)
 instance=api
 local pid=localPlayer();if pid then guarded(function()money('ATTACHED',pid)end)()end
 return api
end
