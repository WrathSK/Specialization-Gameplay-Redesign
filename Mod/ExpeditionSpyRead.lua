-- B189 UI native boundary. Read-only native citizen-name observation; Read-only Gain Sources diagnostics; one-shot TRAVEL only.
include('GreatWorkCatalog')
if include and not SPCExpeditionTrainingDiagnostics then include('ExpeditionTrainingDiagnostics')end
SPCExpeditionSpyRead={KIND='UNIT_SPC_EXPEDITION_SPY'}
local M=SPCExpeditionSpyRead
local function integer(n)return type(n)=='number' and n==n and n>=0 and n<math.huge and n%1==0 end
local function call(obj,name,...)
 if not obj or type(obj[name])~='function' then return nil end
 local ok,v=pcall(obj[name],obj,...);if ok then return v end
end
-- B225: fresh selected-city eligible-work existence. No exact work/site lock.
function M.WorksCity(observer,owner,id,x,y)
 assert(observer==Game.GetLocalPlayer() and integer(owner) and integer(id)
  and integer(x) and integer(y),'MISSION_WORK_REFERENCE_UNKNOWN')
 local turn=Game.GetCurrentGameTurn()
 local c=assert(Players[owner] and Players[owner]:GetCities():FindID(id),'MISSION_WORK_REFERENCE_UNKNOWN')
 local function sameCity()
  return c:GetOwner()==owner and c:GetID()==id and c:GetX()==x and c:GetY()==y
   and Game.GetCurrentGameTurn()==turn and Game.GetLocalPlayer()==observer
 end
 assert(sameCity(),'MISSION_WORK_REFERENCE_CHANGED')
 local sample={owner=owner,city=id,x=x,y=y,turn=turn,status='INVALID'}
 local b=c:GetBuildings();local ds=c:GetDistricts();local uncertain=false;local checked,slots=0,0
 local adapter={Info=function(name,key)local t=GameInfo[name];return t and t[key]end}
 local function building(kind)
  local def=assert(GameInfo.Buildings[kind],'MISSION_BUILDING_UNKNOWN')
  local present=b:HasBuilding(def.Index);assert(type(present)=='boolean','MISSION_BUILDING_UNKNOWN')
  if not present then return end
  local n=b:GetNumGreatWorkSlots(def.Index);assert(integer(n) and n<=256,'MISSION_WORK_READER_UNAVAILABLE')
  for slot=0,n-1 do
   slots=slots+1;assert(slots<=4096,'MISSION_WORK_READER_UNAVAILABLE')
   local ok,found=pcall(function()
    local wid=b:GetGreatWorkInSlot(def.Index,slot)
    assert(wid==-1 or integer(wid),'MISSION_WORK_READER_UNAVAILABLE')
    if wid==-1 then return false end
    local row=assert(GameInfo.GreatWorks[b:GetGreatWorkTypeFromIndex(wid)],'MISSION_WORK_TYPE_UNAVAILABLE')
    local eligible,why=SPCGreatWorkCatalog.Resolve(adapter,row.GreatWorkType)
    if eligible then sample.status='VALID';sample.work=row.GreatWorkType;return true end
    assert(why=='UNSUPPORTED_TYPE','MISSION_WORK_TYPE_UNAVAILABLE')
    return false
   end)
   if not ok then uncertain=true elseif found then return true end
  end
 end
 for _,district in ds:Members()do
  checked=checked+1;assert(checked<=256,'MISSION_WORK_READER_UNAVAILABLE')
  local ok,list=pcall(function()
   local complete=district:IsComplete();assert(type(complete)=='boolean','MISSION_BUILDING_UNKNOWN')
   if not complete then return {}end
   local plot=assert(Map.GetPlot(district:GetX(),district:GetY()),'MISSION_WORK_REFERENCE_UNKNOWN')
   local at=b:GetBuildingsAtLocation(plot:GetIndex());assert(type(at)=='table' and #at<=512,'MISSION_BUILDING_UNKNOWN');return at
  end)
  if not ok then uncertain=true
  else for _,kind in ipairs(list)do
   local read,found=pcall(building,kind)
   if not read then uncertain=true
   elseif found then break end
  end end
  if sample.status=='VALID' then break end
 end
 if sample.status~='VALID' and uncertain then sample.status='UNKNOWN'end
 assert(sameCity(),'MISSION_WORK_REFERENCE_CHANGED')
 return sample
end
function M.Capacity(pid)
 local d=Players[pid] and call(Players[pid],'GetDiplomacy')
 local n=call(d,'GetSpyCapacity');return integer(n) and n or nil
end
-- B212: native Spy travel needs a revealed city. The Expedition enters a target
-- civilization through its revealed city nearest the target (the target itself
-- when revealed) and continues on internal routes; the target need not be revealed.
local function revealed(pid,c)
 local vis=PlayersVisibility and PlayersVisibility[pid]
 return call(vis,'IsRevealed',c:GetX(),c:GetY())==true
end
function M.Entry(pid,owner,target)
 local p=Players[owner];if not p or not target then return nil end
 if revealed(pid,target)then return target end
 local best,bestD
 local cities=call(p,'GetCities')
 if not cities or type(cities.Members)~='function' then return nil end
 for _,c in cities:Members()do
  if c:GetOwner()==owner and revealed(pid,c)then
   local d=(Map and type(Map.GetPlotDistance)=='function' and Map.GetPlotDistance(c:GetX(),c:GetY(),target:GetX(),target:GetY()))
    or math.abs(c:GetX()-target:GetX())+math.abs(c:GetY()-target:GetY())
   if not best or d<bestD or (d==bestD and c:GetID()<best:GetID())then best,bestD=c,d end
  end
 end
 return best
end
function M.Target(pid,owner,id)
 local p=Players[owner];local me=Players[pid]
 if not p or not me or pid==owner or call(p,'IsMajor')~=true or call(p,'IsAlive')~=true then return nil end
 if call(call(me,'GetDiplomacy'),'HasMet',owner)~=true then return nil end
 local cities=call(p,'GetCities');local c=cities and call(cities,'FindID',id)
 if not c or c:GetOwner()~=owner then return nil end
 if not M.Entry(pid,owner,c)then return nil end
 return c
end
function M.Targets(pid)
 local out={}
 for owner,p in pairs(Players)do
  if owner~=pid and call(p,'IsMajor')==true and call(p,'IsAlive')==true
   and call(call(Players[pid],'GetDiplomacy'),'HasMet',owner)==true then
   local cities=call(p,'GetCities')
   if cities and type(cities.Members)=='function' then
    for _,c in cities:Members()do
     if M.Target(pid,owner,c:GetID())then
      out[#out+1]={owner=owner,id=c:GetID(),name=c:GetName(),x=c:GetX(),y=c:GetY(),capital=call(c,'IsCapital')==true}
     end
    end
   end
  end
 end
 table.sort(out,function(a,b)if a.owner~=b.owner then return a.owner<b.owner end;if a.capital~=b.capital then return a.capital end;return a.id<b.id end)
 return out
end
-- B199: present actual mission locations, not every city district. This is a
-- bounded display read of the selected eligible city; it never grants a mission.
local function locationRead(obj,name,...)
 if not obj or type(obj[name])~='function' then error('LOCATION_READER_UNAVAILABLE:'..name,0) end
 local ok,value=pcall(obj[name],obj,...)
 if not ok then error('LOCATION_READ_FAILED:'..name,0) end
 return value
end
local function locationRequire(value,reason)
 if not value then error(reason,0) end
 return value
end
local function site(out,category,plotID,value)
 local old=out.sites[category]
 if not old or plotID<old.plot then value.plot=plotID;out.sites[category]=value end
 out.siteStatus[category]='VALID'
end
local function locationSnapshot(city,out)
 out.sites=out.sites or {}
 local items={};out.districts=items
 -- Only positive mission opportunities are shown; no universal city-center icon.
 -- Capital availability is independent from work and Wonder availability.
 local capitalRead,capital=pcall(locationRead,city,'IsCapital')
 if capitalRead and type(capital)=='boolean' then out.siteStatus.PEOPLE=capital and 'VALID' or 'INVALID' end
 if capitalRead and capital==true then
  out.sites.PEOPLE={x=city:GetX(),y=city:GetY(),plot=-1}
  local config=PlayerConfigurations and PlayerConfigurations[city:GetOwner()]
  local civ=config and call(config,'GetCivilizationTypeName')
  if type(civ)=='string' then
   items[#items+1]={icon='ICON_'..civ,name='LOC_SPC_EXPEDITION_SPY_MISSION_PEOPLE_NAME',category='PEOPLE'}
  end
 end
 local districtDefs=locationRequire(GameInfo.Districts,'LOCATION_DISTRICT_DEFINITION_UNAVAILABLE')
 local buildings=locationRequire(locationRead(city,'GetBuildings'),'LOCATION_BUILDINGS_UNAVAILABLE')
 local districts=locationRequire(locationRead(city,'GetDistricts'),'LOCATION_DISTRICTS_UNAVAILABLE')
 locationRequire(type(districts.Members)=='function','LOCATION_READER_UNAVAILABLE:Members')
 local seen={};local definitions=locationRequire(GameInfo.Buildings,'LOCATION_BUILDING_DEFINITION_UNAVAILABLE')
 local adapter={Info=function(tableName,key)local t=GameInfo[tableName];return t and t[key]end}
 for _,district in districts:Members()do
  local complete=locationRead(district,'IsComplete')
  locationRequire(type(complete)=='boolean','LOCATION_DISTRICT_COMPLETION_UNKNOWN')
  if complete then
   locationRequire(districtDefs[locationRead(district,'GetType')],'LOCATION_DISTRICT_DEFINITION_UNAVAILABLE')
   local x,y=locationRead(district,'GetX'),locationRead(district,'GetY')
   locationRequire(integer(x) and integer(y),'LOCATION_COORDINATES_UNKNOWN')
   locationRequire(Map and type(Map.GetPlot)=='function','LOCATION_MAP_READER_UNAVAILABLE')
   local plot=locationRequire(Map.GetPlot(x,y),'LOCATION_PLOT_UNAVAILABLE')
   local plotID=locationRead(plot,'GetIndex');locationRequire(integer(plotID),'LOCATION_PLOT_INDEX_UNKNOWN')
   local at=locationRead(buildings,'GetBuildingsAtLocation',plotID)
   locationRequire(type(at)=='table','LOCATION_BUILDINGS_AT_PLOT_UNKNOWN')
   for _,kind in ipairs(at)do
    local building=locationRequire(definitions[kind],'LOCATION_BUILDING_DEFINITION_UNAVAILABLE')
    local present=locationRead(buildings,'HasBuilding',building.Index)
    locationRequire(type(present)=='boolean','LOCATION_BUILDING_PRESENCE_UNKNOWN')
    if present then
     if building.IsWonder==true or building.IsWonder==1 then
      local key=tostring(plotID)..':'..building.BuildingType
      if not seen[key] then
       seen[key]=true;items[#items+1]={icon='ICON_'..building.BuildingType,name=building.Name,kind='WONDER',category='PLACES'}
      end
      site(out,'PLACES',plotID,{x=x,y=y,building=building.BuildingType})
     end
     -- A Wonder can independently host eligible works; icon deduplication must
     -- not change mission qualification or skip its slots.
     local slots=locationRead(buildings,'GetNumGreatWorkSlots',building.Index)
     locationRequire(integer(slots) and slots<=256,'LOCATION_SLOT_COUNT_UNKNOWN')
     for slot=0,slots-1 do
      local workID=locationRead(buildings,'GetGreatWorkInSlot',building.Index,slot)
      locationRequire(workID==-1 or integer(workID),'LOCATION_WORK_SLOT_UNKNOWN')
      if workID~=-1 then
       local workType=locationRead(buildings,'GetGreatWorkTypeFromIndex',workID)
       local work=GameInfo.GreatWorks and GameInfo.GreatWorks[workType]
       locationRequire(work and type(work.GreatWorkType)=='string','LOCATION_WORK_DEFINITION_UNAVAILABLE')
       locationRequire(SPCGreatWorkCatalog and type(SPCGreatWorkCatalog.Resolve)=='function','LOCATION_WORK_CATALOG_UNAVAILABLE')
       local eligible,why=SPCGreatWorkCatalog.Resolve(adapter,work.GreatWorkType)
       locationRequire(eligible or why=='UNSUPPORTED_TYPE','LOCATION_WORK_METADATA_UNKNOWN')
       if eligible then
        site(out,'WORKS',plotID,{x=x,y=y,building=building.BuildingType,slot=slot,work=work.GreatWorkType,workID=workID})
        if not seen.WORKS then
         seen.WORKS=true;items[#items+1]={icon='ICON_GREATWORKOBJECT_WRITING',name='LOC_SPC_EXPEDITION_SPY_MISSION_WORKS_NAME',category='WORKS'}
        end
       end
      end
     end
    end
   end
  end
 end
 out.siteStatus.WORKS=out.sites.WORKS and 'VALID' or 'INVALID'
 out.siteStatus.PLACES=out.sites.PLACES and 'VALID' or 'INVALID'
end
-- Optional presentation failures never grant/deny travel. No capacity/operation
-- reader, permission token, persistent cache or mutation. READABLE means the API
-- snapshot was readable; it does not certify foreign inventory completeness.
function M.Presentation(pid,id,target)
 local out={districts={},siteStatus={PEOPLE='UNKNOWN',WORKS='UNKNOWN',PLACES='UNKNOWN'},locationStatus='UNKNOWN',locationReason='LOCATION_TARGET_UNAVAILABLE'}
 local ok=pcall(function()
  local city=target and M.Target(pid,target.owner,target.id)
  if not city or city:GetX()~=target.x or city:GetY()~=target.y then return end
  out.name=city:GetName();out.owner=target.owner;out.id=target.id
  local unit=call(call(Players[pid],'GetUnits'),'FindID',id)
  local row=unit and GameInfo.Units[unit:GetUnitType()]
  if unit and unit:GetID()==id and unit:GetOwner()==pid and row and row.UnitType==M.KIND then
   local timing,t,e=pcall(function()
    local via=assert(M.Entry(pid,target.owner,city))
    return UnitManager.GetTravelTime(unit,via),UnitManager.GetEstablishInCityTime(unit,via)
   end)
   if timing and integer(t) and integer(e) then out.travel=t;out.establish=e;out.total=t+e end
  end
  local read,reason=pcall(locationSnapshot,city,out)
  if read and out.siteStatus.PEOPLE~='UNKNOWN' then out.locationStatus='READABLE';out.locationReason=nil
  elseif read then out.locationReason='LOCATION_CAPITAL_UNKNOWN'
  else out.locationReason=tostring(reason):match('LOCATION_[%w_:]+') or 'LOCATION_READ_FAILED' end
  if city:GetOwner()~=target.owner or city:GetID()~=target.id or city:GetX()~=target.x or city:GetY()~=target.y then
   out.districts={};out.sites={};out.siteStatus={PEOPLE='UNKNOWN',WORKS='UNKNOWN',PLACES='UNKNOWN'};out.locationStatus='UNKNOWN';out.locationReason='LOCATION_TARGET_CHANGED'
  end
 end)
 if not ok then out.districts={};out.sites={};out.siteStatus={PEOPLE='UNKNOWN',WORKS='UNKNOWN',PLACES='UNKNOWN'};out.locationStatus='UNKNOWN';out.locationReason='LOCATION_READ_FAILED' end
 return out
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
  local e=assert(M.Entry(pid,target.owner,c),'ENTRY_UNKNOWN')
  v.entryX=e:GetX();v.entryY=e:GetY();v.entryID=e:GetID()
  v.travel=UnitManager.GetTravelTime(u,e)
  v.establish=UnitManager.GetEstablishInCityTime(u,e)
  v.spyAfter=M.Capacity(pid)
  assert(integer(v.travel) and integer(v.establish),'HELPER_RESULT_INVALID')
  assert(u:GetOwner()==pid and u:GetID()==unitID and u:GetX()==v.fromX and u:GetY()==v.fromY,'UNIT_CHANGED_DURING_READ')
  v.nativeStatus='UNKNOWN'
  -- Diagnostic only. A false result is not proof that Spy is the only reason.
  local checked,allowed=pcall(function()
   assert(UnitOperationTypes and UnitOperationTypes.SPY_TRAVEL_NEW_CITY and Map and Map.GetPlot)
   local params={};params[UnitOperationTypes.PARAM_X]=e:GetX();params[UnitOperationTypes.PARAM_Y]=e:GetY()
   return UnitManager.CanStartOperation(u,UnitOperationTypes.SPY_TRAVEL_NEW_CITY,Map.GetPlot(e:GetX(),e:GetY()),params)
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
-- Names are observed only. No rename command or fallback label is submitted.
-- Gameplay creation can precede publication into UI. This exact lookup is
-- read-only and never searches for a substitute unit or uses selection/name.
function M.NameReadiness(pid,id)
 local at='UI_UNITS_UNREADABLE'
 local ok,status,reason,u=pcall(function()
  local player=Players and Players[pid]
  if not player then return 'INVALID','UI_PLAYER_UNAVAILABLE' end
  local units=player:GetUnits()
  if not units then return 'PENDING','UI_UNITS_UNREADABLE' end
  at='UI_UNIT_LOOKUP_UNREADABLE'
  local unit=units:FindID(id)
  if not unit then return 'PENDING','UI_UNIT_NOT_PUBLISHED' end
  at='UI_UNIT_ID_UNREADABLE';local actual=unit:GetID()
  if actual==nil then return 'PENDING',at end
  if actual~=id then return 'INVALID','UI_UNIT_ID_MISMATCH' end
  at='UI_UNIT_OWNER_UNREADABLE';local owner=unit:GetOwner()
  if owner==nil then return 'PENDING',at end
  if owner~=pid then return 'INVALID','UI_UNIT_OWNER_MISMATCH' end
  at='UI_UNIT_TYPE_UNREADABLE';local kind=unit:GetUnitType()
  if kind==nil then return 'PENDING',at end
  local row=GameInfo and GameInfo.Units and GameInfo.Units[kind]
  if not row then return 'INVALID','UI_UNIT_DEFINITION_UNAVAILABLE' end
  if row.UnitType~=M.KIND then return 'INVALID','UI_UNIT_TYPE_MISMATCH' end
  return 'READY','UI_UNIT_READY',unit
 end)
 if not ok then return 'PENDING',at end
 return status,reason,u
end
function M.NameStatus(pid,id,expected)
 local ready,reason,u=M.NameReadiness(pid,id)
 if ready~='READY' then return 'UNREADABLE',reason end
 local ok,name=pcall(function()return u:GetName()end)
 if not ok or type(name)~='string' then return 'UNREADABLE','TEAM_NAME_UNREADABLE' end
 return name==expected and 'MATCH' or 'MISMATCH'
end
-- The loaded current-civilization pool is evidence, not a name generator. Accept
-- a raw pool key or its unique localized value. Preserve the observed string
-- verbatim for continuity; ambiguous localized names never establish identity.
function M.NativeName(pid,id)
 local ready,reason,u=M.NameReadiness(pid,id)
 local v={status=ready,reason=reason}
 if ready~='READY' then return v end
 local at='CITIZEN_NAME_POOL_UNREADABLE';local failure='INVALID'
 local ok=pcall(function()
  local config=PlayerConfigurations and PlayerConfigurations[pid]
  if not config or type(config.GetCivilizationTypeName)~='function' then
   v.status='INVALID';v.reason='CIVILIZATION_CONFIGURATION_UNAVAILABLE';return
  end
  at='CIVILIZATION_CONFIGURATION_UNREADABLE'
  local civ=config:GetCivilizationTypeName();v.civilization=civ
  if type(civ)~='string' or civ=='' then v.status='INVALID';v.reason='CIVILIZATION_TYPE_UNAVAILABLE';return end
  if not GameInfo or not GameInfo.CivilizationCitizenNames then
   v.status='INVALID';v.reason='CITIZEN_NAME_POOL_UNAVAILABLE';return
  end
  at='CITIZEN_NAME_POOL_UNREADABLE'
  local names={};v.poolCount=0
  for row in GameInfo.CivilizationCitizenNames()do
   if row.CivilizationType==civ then
    if type(row.CitizenName)~='string' or row.CitizenName=='' then
     v.status='INVALID';v.reason='CITIZEN_NAME_POOL_INVALID';return
    end
    if not names[row.CitizenName]then names[row.CitizenName]=true;v.poolCount=v.poolCount+1 end
   end
  end
  if v.poolCount==0 then v.status='INVALID';v.reason='CITIZEN_NAME_POOL_EMPTY';return end
  local row=GameInfo.Units[u:GetUnitType()];v.defaultName=row and row.Name
  if type(v.defaultName)~='string' or v.defaultName=='' then
   v.status='INVALID';v.reason='UI_UNIT_DEFAULT_NAME_UNAVAILABLE';return
  end
  at='UNIT_DEFAULT_LOCALIZATION_UNREADABLE'
  local defaultLocalized=Locale.Lookup(v.defaultName)
  failure='PENDING';at='TEAM_NATIVE_NAME_UNREADABLE'
  local name=u:GetName();v.name=type(name)=='string' and name or nil
  if type(name)~='string' or name:match('^%s*$')then v.status='PENDING';v.reason='TEAM_NATIVE_NAME_UNASSIGNED';return end
  if name==v.defaultName or name==defaultLocalized then v.status='PENDING';v.reason='TEAM_NATIVE_NAME_DEFAULT';return end
  if #name>220 then v.status='INVALID';v.reason='TEAM_NATIVE_NAME_OUTSIDE_POOL';return end
  if names[name]then v.representation='RAW_KEY'
  else
   failure='INVALID';at='CITIZEN_NAME_LOCALIZATION_UNREADABLE'
   local matches=0
   for key in pairs(names)do if Locale.Lookup(key)==name then matches=matches+1 end end
   if matches>1 then v.status='INVALID';v.reason='TEAM_NATIVE_NAME_AMBIGUOUS_LOCALIZED';return end
   if matches==0 then v.status='INVALID';v.reason='TEAM_NATIVE_NAME_OUTSIDE_POOL';return end
   v.representation='LOCALIZED_VALUE'
  end
  failure='PENDING'
  at='VISIBLE_NAME_COLLISION_READ_UNAVAILABLE'
  for _,other in Players[pid]:GetUnits():Members()do
   if other:GetOwner()==pid and other:GetID()~=id then
    local otherName=other:GetName()
    if type(otherName)~='string' then error(at)end
    if otherName==name then v.status='INVALID';v.reason='TEAM_NATIVE_NAME_DUPLICATE_VISIBLE';return end
   end
  end
  -- Native Overview enumerates off-map spy records with (player, zero-based
  -- index). Include every record, even ReturnTurn=-1; display filtering is not
  -- identity evidence. This is an initial collision check, not a global registry.
  at='OFFMAP_NAME_COUNT_UNAVAILABLE'
  local diplomacy=Players[pid]:GetDiplomacy()
  local count=diplomacy:GetNumSpiesOffMap();v.offmapCount=count
  if not integer(count)then error(at)end
  at='OFFMAP_NAME_COLLISION_READ_UNAVAILABLE'
  for i=0,count-1 do
   local other=diplomacy:GetNthOffMapSpy(pid,i)
   if type(other)~='table' or type(other.Name)~='string' or other.Name=='' then error(at)end
   if other.Name==name then v.status='INVALID';v.reason='TEAM_NATIVE_NAME_DUPLICATE_OFFMAP';return end
  end
  local final,why,exact=M.NameReadiness(pid,id)
  if final~='READY' then v.status=final;v.reason=why;return end
  at='TEAM_NATIVE_NAME_UNREADABLE'
  if exact:GetName()~=name then v.status='PENDING';v.reason='TEAM_NATIVE_NAME_CHANGED_DURING_READ';return end
  v.status='READY';v.reason='TEAM_NATIVE_NAME_CONFIRMED'
 end)
 if not ok then v.status=failure;v.reason=at end
 return v
end
local lastPermit
local travelTrace
local function traceTravel(stage,u,pid,id,t,ex,ey,status)
 pcall(function()
  if not SPCExpeditionTrainingDiagnostics then return end
  if not travelTrace then travelTrace=SPCExpeditionTrainingDiagnostics.New(nil,'TRAVEL_UI')end
  local v=ExposedMembers and ExposedMembers.SPC_ExpeditionActivity
  local same=type(v)=='table' and v.owner==pid and v.unitID==id
  travelTrace.Unit(stage,u,{owner=pid,eventUnit=id,teamKey=same and v.teamKey or nil,
   phase=same and v.phase or 'UNKNOWN',targetOwner=t.owner,targetCity=t.id,targetX=t.x,targetY=t.y,
   entryX=ex,entryY=ey,arrivalRoute=ex==t.x and ey==t.y and 'DIRECT' or 'ENTRY_RELOCATE',submitStatus=status})
 end)
end
function M.SubmitTravel(pid,id,t,permit)
 if type(permit)~='string' or #permit==0 or #permit>100 or permit==lastPermit then return false,'INVALID_OR_USED_PERMIT' end
 local ok,err=pcall(function()
  local u=Players[pid]:GetUnits():FindID(id);local r=u and GameInfo.Units[u:GetUnitType()]
  assert(u and u:GetID()==id and u:GetOwner()==pid and r and r.UnitType==M.KIND and (r.Spy==true or r.Spy==1),'SPY_TEST_TEAM_REQUIRED')
  local c=M.Target(pid,t.owner,t.id);assert(c and c:GetX()==t.x and c:GetY()==t.y,'TARGET_CHANGED')
  -- B212: travel natively to the entry city recorded by Gameplay (the target when revealed).
  local ex,ey=t.entryX or c:GetX(),t.entryY or c:GetY()
  local e
  for _,other in Players[t.owner]:GetCities():Members()do
   if other:GetX()==ex and other:GetY()==ey then e=other end
  end
  assert(e and e:GetOwner()==t.owner and revealed(pid,e),'ENTRY_CHANGED')
  local params={};params[UnitOperationTypes.PARAM_X]=ex;params[UnitOperationTypes.PARAM_Y]=ey
  traceTravel('DISPATCH_BEFORE',u,pid,id,t,ex,ey,'NOT_REQUESTED')
  assert(UnitManager.CanStartOperation(u,UnitOperationTypes.SPY_TRAVEL_NEW_CITY,Map.GetPlot(ex,ey),params)==true,'NATIVE_TRAVEL_NOT_ALLOWED')
  lastPermit=permit -- Reserve BEFORE the request; an ambiguous result is not retried.
  local result=UnitManager.RequestOperation(u,UnitOperationTypes.SPY_TRAVEL_NEW_CITY,params)
  traceTravel('DISPATCH_RETURNED',u,pid,id,t,ex,ey,result==false and 'RETURNED_FALSE' or 'CALL_RETURNED')
  assert(result~=false,'NATIVE_REQUEST_REJECTED') -- nil is common for command submission, not arrival PASS.
 end)
 return ok,not ok and tostring(err):sub(1,200) or 'REQUEST_SUBMITTED'
end
return M
