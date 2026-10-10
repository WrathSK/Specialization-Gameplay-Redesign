-- B185 UI native boundary. Read-only Gain Sources diagnostics; one-shot TRAVEL only.
SPCExpeditionSpyRead={KIND='UNIT_SPC_EXPEDITION_SPY'}
local M=SPCExpeditionSpyRead
local function integer(n)return type(n)=='number' and n==n and n>=0 and n<math.huge and n%1==0 end
local function call(obj,name,...)
 if not obj or type(obj[name])~='function' then return nil end
 local ok,v=pcall(obj[name],obj,...);if ok then return v end
end
function M.Capacity(pid)
 local d=Players[pid] and call(Players[pid],'GetDiplomacy')
 local n=call(d,'GetSpyCapacity');return integer(n) and n or nil
end
function M.Target(pid,owner,id)
 local p=Players[owner];local me=Players[pid]
 if not p or not me or pid==owner or call(p,'IsMajor')~=true or call(p,'IsAlive')~=true then return nil end
 if call(call(me,'GetDiplomacy'),'HasMet',owner)~=true then return nil end
 local cities=call(p,'GetCities');local c=cities and call(cities,'FindID',id)
 if not c or c:GetOwner()~=owner or call(c,'IsCapital')~=true then return nil end
 -- Gate-fixture restriction only, not the final Design's foreign-information policy.
 local vis=PlayersVisibility and PlayersVisibility[pid]
 if call(vis,'IsRevealed',c:GetX(),c:GetY())~=true then return nil end
 return c
end
function M.Targets(pid)
 local out={}
 for owner,p in pairs(Players)do
  if owner~=pid and call(p,'IsMajor')==true and call(p,'IsAlive')==true
   and call(call(Players[pid],'GetDiplomacy'),'HasMet',owner)==true then
   local c=call(call(p,'GetCities'),'GetCapitalCity')
   if c and M.Target(pid,owner,c:GetID())then
    out[#out+1]={owner=owner,id=c:GetID(),name=c:GetName(),x=c:GetX(),y=c:GetY()}
   end
  end
 end
 table.sort(out,function(a,b)return a.owner<b.owner end);return out
end
function M.Read(pid,unitID,target)
 local v={owner=pid,unitID=unitID,turn=Game.GetCurrentGameTurn(),status='UNKNOWN'}
 local ok,err=pcall(function()
  local u=Players[pid]:GetUnits():FindID(unitID)
  assert(u and u:GetOwner()==pid,'TEAM_UNAVAILABLE')
  local row=GameInfo.Units[u:GetUnitType()]
  assert(row and row.UnitType==M.KIND and (row.Spy==true or row.Spy==1),'SPY_TEST_TEAM_REQUIRED')
  local c=target and M.Target(pid,target.owner,target.id)
  assert(c and c:GetX()==target.x and c:GetY()==target.y,'TARGET_CHANGED')
  assert(UnitManager and type(UnitManager.GetTravelTime)=='function' and type(UnitManager.GetEstablishInCityTime)=='function','HELPER_UNAVAILABLE')
  v.fromX=u:GetX();v.fromY=u:GetY();v.targetOwner=target.owner;v.targetID=target.id;v.targetName=c:GetName()
  v.targetX=c:GetX();v.targetY=c:GetY();v.spyBefore=M.Capacity(pid)
  v.travel=UnitManager.GetTravelTime(u,c)
  v.establish=UnitManager.GetEstablishInCityTime(u,c)
  v.spyAfter=M.Capacity(pid)
  assert(integer(v.travel) and integer(v.establish),'HELPER_RESULT_INVALID')
  assert(u:GetOwner()==pid and u:GetID()==unitID and u:GetX()==v.fromX and u:GetY()==v.fromY,'UNIT_CHANGED_DURING_READ')
  v.nativeStatus='UNKNOWN'
  -- Diagnostic only. A false result is not proof that Spy is the only reason.
  local checked,allowed=pcall(function()
   assert(UnitOperationTypes and UnitOperationTypes.SPY_TRAVEL_NEW_CITY and Map and Map.GetPlot)
   local params={};params[UnitOperationTypes.PARAM_X]=c:GetX();params[UnitOperationTypes.PARAM_Y]=c:GetY()
   return UnitManager.CanStartOperation(u,UnitOperationTypes.SPY_TRAVEL_NEW_CITY,Map.GetPlot(c:GetX(),c:GetY()),params)
  end)
  if checked and type(allowed)=='boolean' then v.nativeStatus='KNOWN';v.nativeAllowed=allowed end
  assert(u:GetOwner()==pid and u:GetID()==unitID and u:GetX()==v.fromX and u:GetY()==v.fromY,'UNIT_CHANGED_DURING_READ')
  v.total=v.travel+v.establish;v.status='READ_OK'  -- Not deployed or native travel PASS.
 end)
 if not ok then v.error=tostring(err):sub(1,220)end
 return v
end

-- Explicit-action snapshots only. This reports native classification separately
-- from our cap1; an unchanged maximum never proves unused native slots unchanged.
function M.Audit(pid,sourceID)
 local v={status='UNKNOWN',capacity=M.Capacity(pid)}
 local ok,err=pcall(function()
  local player=assert(Players[pid]);local normal={};v.normal=0;v.nativeTotal=0
  for _,u in player:GetUnits():Members()do
   local r=GameInfo.Units[u:GetUnitType()]
   assert(r,'UNIT_DEFINITION_UNKNOWN')
   if r.Spy==true or r.Spy==1 then
    v.nativeTotal=v.nativeTotal+1
    if r.UnitType~=M.KIND then
     v.normal=v.normal+1
     normal[#normal+1]=tostring(u:GetID())..':'..r.UnitType..':'..tostring(call(u,'GetSpyOperation'))
    end
   end
  end
  table.sort(normal);v.fingerprint=table.concat(normal,'|')
  local d=player:GetDiplomacy();v.offmap=call(d,'GetNumSpiesOffMap')
  local c=sourceID and player:GetCities():FindID(sourceID)
  local q=c and call(c,'GetBuildQueue');local spy=GameInfo.Units.UNIT_SPY
  if q and spy and MilitaryFormationTypes then
   local value=call(q,'CanProduce',{UnitType=spy.Hash,MilitaryFormationType=MilitaryFormationTypes.STANDARD_MILITARY_FORMATION},false,true)
   if type(value)=='boolean' then v.trainable=value end
  end
  assert(integer(v.capacity),'CAPACITY_UNKNOWN');v.status='KNOWN'
 end)
 if not ok then v.error=tostring(err):sub(1,200)end
 return v
end
function M.Compare(before,after)
 if not before or not after or before.status~='KNOWN' or after.status~='KNOWN' then return 'UNKNOWN' end
 if before.capacity~=after.capacity or before.fingerprint~=after.fingerprint then return 'CHANGED' end
 -- Native used slots/off-map count/trainability may change: explicitly accepted
 -- temporary cost, still displayed. Not evidence of independent native capacity.
 if before.nativeTotal~=after.nativeTotal or before.offmap~=after.offmap or before.trainable~=after.trainable then return 'SLOT_COST_ACCEPTED' end
 return before.trainable==true and after.trainable==true and integer(before.offmap) and integer(after.offmap) and 'SCOPED_UNCHANGED' or 'PARTIAL'
end
function M.GainSources(pid,id,t)
 local v={status='NOT_ISOLATED',executionAllowed=false}
 local ok,err=pcall(function()
  local u=Players[pid]:GetUnits():FindID(id);local r=u and GameInfo.Units[u:GetUnitType()]
  assert(u and u:GetID()==id and u:GetOwner()==pid and r and r.UnitType==M.KIND,'SPY_TEST_TEAM_REQUIRED')
  local c=M.Target(pid,t.owner,t.id);assert(c and c:GetX()==t.x and c:GetY()==t.y,'TARGET_CHANGED')
  local d=Players[pid]:GetDiplomacy();local turns=call(d,'GetSourceTurnsRemaining',c)
  if integer(turns)then v.sourceTurns=turns end
  local op=GameInfo.UnitOperations.UNITOPERATION_SPY_GAIN_SOURCES
  assert(op and UnitOperationTypes.SPY_GAIN_SOURCES,'GAIN_SOURCES_UNAVAILABLE')
  local params={};params[UnitOperationTypes.PARAM_X]=c:GetX();params[UnitOperationTypes.PARAM_Y]=c:GetY()
  local read,allowed=pcall(UnitManager.CanStartOperation,u,UnitOperationTypes.SPY_GAIN_SOURCES,Map.GetPlot(c:GetX(),c:GetY()),params)
  if read and type(allowed)=='boolean' then v.canStart=allowed end
  -- Raw outcome categories, never the misleading aggregate success percentage.
  local readOdds,odds=pcall(UnitManager.GetResultProbability,op.Index,u,Map.GetPlot(c:GetX(),c:GetY()))
  if readOdds and type(odds)=='table' then
   for _,key in ipairs({'ESPIONAGE_SUCCESS_UNDETECTED','ESPIONAGE_SUCCESS_MUST_ESCAPE'})do
    local value=odds[key]
    if type(value)=='number' and value==value and value>=0 and value<=1 then v[key]=value end
   end
  end
  v.readOK=true
 end)
 if not ok then v.error=tostring(err):sub(1,200)end
 -- Even undetected=1 cannot isolate native source state or HD completion hooks.
 return v
end
function M.TaskRead(pid,id,t)
 local v={status='UNKNOWN'}
 local ok,err=pcall(function()
  local u=Players[pid]:GetUnits():FindID(id);local r=u and GameInfo.Units[u:GetUnitType()]
  assert(u and u:GetID()==id and u:GetOwner()==pid and r and r.UnitType==M.KIND,'SPY_TEST_TEAM_REQUIRED')
  local c=M.Target(pid,t.owner,t.id)
  assert(c and c:GetX()==t.x and c:GetY()==t.y,'TARGET_CHANGED')
  v.operation=call(u,'GetSpyOperation');assert(type(v.operation)=='number','NATIVE_OPERATION_UNKNOWN')
  v.sourceTurns=call(Players[pid]:GetDiplomacy(),'GetSourceTurnsRemaining',c)
  if not integer(v.sourceTurns)then v.sourceTurns=nil end
  v.status='KNOWN'
 end)
 if not ok then v.error=tostring(err):sub(1,200)end
 return v
end
local lastPermit
function M.SubmitTravel(pid,id,t,permit)
 if type(permit)~='string' or #permit==0 or #permit>100 or permit==lastPermit then return false,'INVALID_OR_USED_PERMIT' end
 local ok,err=pcall(function()
  local u=Players[pid]:GetUnits():FindID(id);local r=u and GameInfo.Units[u:GetUnitType()]
  assert(u and u:GetID()==id and u:GetOwner()==pid and r and r.UnitType==M.KIND and (r.Spy==true or r.Spy==1),'SPY_TEST_TEAM_REQUIRED')
  local c=M.Target(pid,t.owner,t.id);assert(c and c:GetX()==t.x and c:GetY()==t.y,'TARGET_CHANGED')
  local params={};params[UnitOperationTypes.PARAM_X]=c:GetX();params[UnitOperationTypes.PARAM_Y]=c:GetY()
  assert(UnitManager.CanStartOperation(u,UnitOperationTypes.SPY_TRAVEL_NEW_CITY,Map.GetPlot(c:GetX(),c:GetY()),params)==true,'NATIVE_TRAVEL_NOT_ALLOWED')
  lastPermit=permit -- Reserve BEFORE the request; an ambiguous result is not retried.
  local result=UnitManager.RequestOperation(u,UnitOperationTypes.SPY_TRAVEL_NEW_CITY,params)
  assert(result~=false,'NATIVE_REQUEST_REJECTED') -- nil is common for command submission, not arrival PASS.
 end)
 return ok,not ok and tostring(err):sub(1,200) or 'REQUEST_SUBMITTED'
end
return M
