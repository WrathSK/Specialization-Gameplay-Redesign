-- B267 fixed-scope observation only; no properties, repair or carrier writes.
SPCCarrierHealthTrace={}
function SPCCarrierHealthTrace.Start(P,shared)
 if not SPCExpeditionTrainingDiagnostics.ENABLED then return {}end
 local trace=SPCExpeditionTrainingDiagnostics.New(P,'CARRIER_HEALTH')
 local names={};for _,kind in ipairs({'RESEARCH','CULTURE','COMMERCE'})do names[#names+1]='BUILDING_SPC_DEV_'..kind..'_SUPPORT'end
 for _,kind in ipairs({'RESEARCH','CULTURE','INDUSTRY','COMMERCE'})do for bit=0,7 do names[#names+1]='BUILDING_SPC_DEV_GPP_'..kind..'_'..bit end end
 local d={};shared.CarrierHealthTrace=d
 local previous={};local loaded=false;local firstTurn=true;local lastTurn;local transitions=0
 local function read(b,method,index)
  if P.Count then P.Count('observer_native_attempt');P.Count('observer_carrier_attempt')end
  local ok,v=pcall(function()return b[method](b,index)end)
  return ok and type(v)=='boolean' and (v and 'YES' or 'NO') or 'UNKNOWN'
 end
 local function sweep(reason)
  if not SPCExpeditionTrainingDiagnostics.ENABLED then return end
  local pid=Game.GetLocalPlayer();if not P.IsTestPlayer(pid)then return end
  local cs=Players[pid]:GetCities();local nextState={};local presentCount,unknown=0,0
  for _,c in cs:Members()do
   if P.Count then P.Count('observer_city_scan')end
   local id=c:GetID();local ref=table.concat({pid,id,c:GetX(),c:GetY()},':');local b=c:GetBuildings()
   for _,name in ipairs(names)do
    local row=P.Info('Buildings',name);local index=row and row.Index
    local present=type(index)=='number' and read(b,'HasBuilding',index) or 'UNKNOWN'
    local pillaged=present=='YES' and read(b,'IsPillaged',index) or present=='NO' and 'ABSENT' or 'UNKNOWN'
    local k=ref..':'..name;local before=previous[k]
    if present=='YES'then presentCount=presentCount+1 end
    if pillaged=='UNKNOWN'then unknown=unknown+1 end
    if pillaged=='YES' and before~='YES'then
     transitions=transitions+1
     trace.Record('CARRIER_PILLAGED_PRESENT',{owner=pid,city=id,x=c:GetX(),y=c:GetY(),buildingIndex=index,count=transitions,present=true,pillaged=true,reason=reason})
    elseif (pillaged=='NO' or pillaged=='ABSENT') and before=='YES'then
     transitions=transitions+1
     trace.Record('CARRIER_PILLAGE_CLEARED',{owner=pid,city=id,x=c:GetX(),y=c:GetY(),buildingIndex=index,count=transitions,present=present=='YES',pillaged=false,reason=pillaged=='ABSENT' and 'CARRIER_REMOVED' or reason})
    end
    -- UNKNOWN preserves the last proved health, never inventing repair evidence.
    nextState[k]=pillaged=='UNKNOWN' and before or pillaged
   end
  end
  previous=nextState
  if reason=='LOAD_BASELINE' or reason=='FIRST_TURN_NO_LOAD' or unknown>0 then trace.Record('CARRIER_HEALTH_SWEEP',{owner=pid,carrierCount=#names,count=presentCount,unreadableCount=unknown,reason=reason})end
 end
 local function safe(fn)return function(...)local ok=pcall(fn,...);if not ok then pcall(trace.Record,'CARRIER_OBSERVER_FAILURE',{reason='CARRIER_READ_ERROR'})end end end
 local function hook(source,name,fn)local e=P.Field(source,name);if e and e.Add then e.Add(safe(fn))end end
 hook(Events,'LoadScreenClose',function()loaded=true;sweep('LOAD_BASELINE')end)
 hook(Events,'PlayerTurnActivated',function(pid)
  if pid~=Game.GetLocalPlayer() or not P.IsTestPlayer(pid)then return end
  local turn=Game.GetCurrentGameTurn();if lastTurn==turn then return end;lastTurn=turn;sweep(firstTurn and not loaded and 'FIRST_TURN_NO_LOAD' or 'LOCAL_TURN');firstTurn=false
 end)
 hook(GameEvents,'BuildingPillageStateChanged',function(pid,id,index,state)
  if pid~=Game.GetLocalPlayer() or not P.IsTestPlayer(pid)then return end
  local owned=false;for _,name in ipairs(names)do local row=P.Info('Buildings',name);if row and row.Index==index then owned=true;break end end
  if not owned then return end
  trace.Record('CARRIER_PILLAGE_EVENT',{owner=pid,city=id,buildingIndex=index,pillaged=state,reason='NATIVE_PILLAGE_EVENT'})
 end)
 return d
end
