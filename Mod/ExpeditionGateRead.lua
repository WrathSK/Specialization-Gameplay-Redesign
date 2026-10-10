-- UI-only read gate. No RequestOperation, native Spy registration or gameplay setter.
SPCExpeditionGateRead={KIND='UNIT_SPC_EXPEDITION_ZERO'}
local M=SPCExpeditionGateRead
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
  assert(row and row.UnitType==M.KIND and (row.Spy==false or row.Spy==0),'NON_SPY_TEST_TEAM_REQUIRED')
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
return M
