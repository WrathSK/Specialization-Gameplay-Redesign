-- B046 observation only. No retries, setters, grant, rounding or consumption.
SPCCrewPrecision={}
function SPCCrewPrecision.Start(P,shared)
 local function before(pid,params)
  local u=Players[pid]:GetUnits():FindID(params.UnitID)
  if not u then return nil end
  local kind=P.Info('Units',u:GetType()).UnitType;if not P.CrewBase(kind) then return nil end
  local previous=shared.UnitTargetSnapshot
  local ok,record=pcall(function()
   shared.UnitTargets.Refresh(pid,{UnitID=u:GetID(),Token='PRECISION_READ',BuilderPreview=false})
   local list=shared.UnitTargetSnapshot;assert(not list.error,list.error)
   local plot=Map.GetPlot(u:GetX(),u:GetY()):GetIndex();local city
   for _,v in ipairs(list.plots) do if v.plot==plot then city=Players[pid]:GetCities():FindID(v.cityID);break end end
   assert(city,'NO_CURRENT_TARGET')
   local s=shared.ConstructionProbe.ReadSnapshot(pid,city)
   return {owner=pid,cityID=city:GetID(),unitID=u:GetID(),kind=kind,target=s.target,targetKind=s.kind,
    before=s.progress,cost=s.cost,amount=P.CrewAmount(kind),turn=Game.GetCurrentGameTurn(),requestToken=params.Token}
  end)
  shared.UnitTargetSnapshot=previous
  return ok and record or {owner=pid,error=tostring(record),requestToken=params.Token}
 end
 local original=shared.UnitActions.Run
 shared.UnitActions.Run=function(pid,params)
  local measured=params.Action=='UNIT_ACTION_CONFIRM'
  local record
  if measured then local ok,v=pcall(before,pid,params);record=ok and v or {owner=pid,error=tostring(v)} end
  local result=original(pid,params) -- Original complete settlement sequence remains untouched.
  if record then
   record.result=result
   local ok,err=pcall(function()
    assert(not record.error,record.error)
    record.expected=math.min(record.amount,record.cost-record.before)
    local city=Players[pid]:GetCities():FindID(record.cityID);assert(city and city:GetOwner()==pid,'CITY_CHANGED')
    local s=shared.ConstructionProbe.ReadSnapshot(pid,city)
    record.afterTarget=s.target;record.after=s.progress
    record.unitPresent=Players[pid]:GetUnits():FindID(record.unitID)~=nil
    if not result:find('CREW CONSUMED',1,true) then record.note='ACTION_NOT_COMPLETED: not a precision measurement'
    elseif s.target==record.target then record.observed=record.after-record.before;record.difference=record.observed-record.expected
    else record.note='TARGET_COMPLETED_OR_CHANGED: do not subtract different targets' end
   end)
   if not ok then record.afterReadError=tostring(err) end
   shared.CrewPrecision=record
   print('[SPC][B046][PRECISION] before='..tostring(record.before)..' after='..tostring(record.after)..' expected='..tostring(record.expected)..' observed='..tostring(record.observed)..' difference='..tostring(record.difference))
  end
  return result
 end
end
