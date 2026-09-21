-- P0 probes only. A successful getter is evidence of a call, not its semantics.
SPCP0 = {}
local P = SPCP0
P.VERSION = "P0-B-089.116"
P.Families = {DISTRICT_CAMPUS="RESEARCH", DISTRICT_THEATER="CULTURE",
  DISTRICT_INDUSTRIAL_ZONE="INDUSTRY", DISTRICT_COMMERCIAL_HUB="COMMERCE"}
P.WorkTypes = {GREATWORKOBJECT_WRITING=true, GREATWORKOBJECT_MUSIC=true,
  GREATWORKOBJECT_LANDSCAPE=true, GREATWORKOBJECT_PORTRAIT=true,
  GREATWORKOBJECT_RELIGIOUS=true, GREATWORKOBJECT_SCULPTURE=true,
  GREATWORKOBJECT_ARTIFACT=true}
P.Specs = {{cost=280,charge=250},{cost=460,charge=420},{cost=820,charge=750},
  {cost=1100,charge=1000},{cost=1500,charge=1360}}
-- D0012: shared denomination catalog; floor speed-scaled Crew Production for display and execution.
function P.CrewBase(kind)
 for _,s in ipairs(P.Specs) do if kind=='UNIT_SPC_CREW_'..s.charge then return s.charge end end
end
function P.CrewAmount(kind)
 local base=P.CrewBase(kind);assert(base,'CREW_TYPE_UNKNOWN')
 local speed=GameInfo.GameSpeeds[GameConfiguration.GetGameSpeedType()]
 local n=speed and speed.CostMultiplier
 assert(type(n)=='number' and n>0 and n<math.huge,'GAME_SPEED_UNKNOWN')
 return math.floor(base*n/100)
end
P.Discounts = {10,20,30,40}

-- Do not traverse engine tables, invoke __tostring, or print unbounded values.
function P.Scalar(value)
  local kind=type(value)
  if kind=="string" then return value:sub(1,512) end
  if kind=="nil" or kind=="boolean" or kind=="number" then return tostring(value) end
  return "<"..kind..":not-inspected>"
end

function P.IsTestPlayer(playerID)
  local config=PlayerConfigurations and PlayerConfigurations[playerID]
  local ok,civ=P.Call(config,"GetCivilizationTypeName")
  local leaderOK,leader=P.Call(config,"GetLeaderTypeName")
  return ok and leaderOK and civ=="CIVILIZATION_SPC_TEST" and leader=="LEADER_SPC_TEST"
end

function P.Summary(playerID,cityID)
  local out={}
  if not P.IsTestPlayer(playerID) then return "OUTSIDE_TEST_CIV" end
  local city=cityID and Players[playerID]:GetCities():FindID(cityID)
  if not city then return "Select an owned test-civilization city for compact comparison." end
  local function val(object,method,...)
    local ok,v=P.Call(object,method,...)
    return ok and (v==nil and "nil" or v) or "API_UNAVAILABLE"
  end
  out[#out+1]="City="..tostring(cityID).." "..city:GetName().." | CIVILIZATION_SPC_TEST / LEADER_SPC_TEST"
  out[#out+1]="Marker="..tostring(val(city,"GetProperty","SPC_P0_MARKER")).." | Spec(test)="..tostring(val(city,"GetProperty","SPC_P0_FIRST_SPEC"))
  out[#out+1]="Potential/Active=NOT_IMPLEMENTED (no invented levels)"
  local ok,gov=P.Call(city,"GetAssignedGovernor")
  local promotions,base,nonbase=0,0,0
  local complete=true
  if ok and gov then
    local typeOK,typeID=P.Call(gov,"GetType")
    local info=typeOK and P.Info("Governors",typeID)
    local rows=P.Rows("GovernorPromotionSets")
    if not info or not rows then complete=false end
    for _,row in ipairs(rows or {}) do
      if info and row.GovernorType==info.GovernorType then
        local pr=P.Info("GovernorPromotions",row.GovernorPromotion)
        local hasOK,has=P.Call(gov,"HasPromotion",pr and pr.Hash)
        if not hasOK or not pr then complete=false
        elseif has then
          promotions=promotions+1
          if pr.BaseAbility==true or pr.BaseAbility==1 then base=base+1 else nonbase=nonbase+1 end
        end
      end
    end
  elseif not ok then complete=false end
  out[#out+1]="Governor established="..tostring(gov and val(gov,"IsEstablished") or false)
    .." | promotions="..tostring(complete and promotions or "UNKNOWN")
    .." | titleCandidate="..tostring(complete and (gov and (1+nonbase) or 0) or "UNKNOWN").." (not historical spend)"
  out[#out+1]="Engine Req2/3/4 raw="..tostring(val(city,"GetProperty","SPC_P0_GOV_REQ_2")).."/"
    ..tostring(val(city,"GetProperty","SPC_P0_GOV_REQ_3")).."/"..tostring(val(city,"GetProperty","SPC_P0_GOV_REQ_4"))
  local enumOK,err=pcall(function()
    for _,d in city:GetDistricts():Members() do
      local info=P.Info("Districts",d:GetType())
      local plot=Map.GetPlot(d:GetX(),d:GetY())
      out[#out+1]=(info and info.DistrictType or tostring(d:GetType())).." workers="..tostring(val(plot,"GetWorkerCount"))
    end
  end)
  if not enumOK then out[#out+1]="DISTRICTS UNKNOWN: "..tostring(err) end
  return table.concat(out,"\n")
end

function P.Field(object, key)
  if object == nil then return nil end
  local ok, value = pcall(function() return object[key] end)
  if ok then return value end
end
function P.Call(object, method, ...)
  local f = P.Field(object, method)
  if type(f) ~= "function" then return false, "ABSENT" end
  return pcall(f, object, ...)
end
function P.Rows(name)
  local info = P.Field(GameInfo, name)
  if info == nil then return nil, "TABLE_ABSENT" end
  local rows = {}
  local ok, err = pcall(function() for row in info() do rows[#rows+1] = row end end)
  if not ok then return nil, tostring(err) end
  return rows
end
function P.Info(name, key) return P.Field(P.Field(GameInfo, name), key) end
function P.Encode(v, seen)
  if type(v) ~= "table" then return tostring(v) end
  seen = seen or {}
  if seen[v] then return "<cycle>" end
  seen[v] = true
  local keys, out = {}, {}
  for k in pairs(v) do keys[#keys+1] = k end
  table.sort(keys, function(a,b) return tostring(a)<tostring(b) end)
  for _,k in ipairs(keys) do out[#out+1] = tostring(k).."="..P.Encode(v[k],seen) end
  seen[v] = nil
  return "{"..table.concat(out,",").."}"
end
function P.Family(districtType)
  local seen = {}
  local replacements = P.Rows("DistrictReplaces") or {}
  while districtType and not seen[districtType] do
    if P.Families[districtType] then return P.Families[districtType] end
    seen[districtType] = true
    local nextType
    for _,r in ipairs(replacements) do
      if r.CivUniqueDistrictType == districtType then nextType=r.ReplacesDistrictType; break end
    end
    districtType = nextType
  end
end

-- Pure test oracle; does not inject anything into the game.
function P.CrewPreview(charge, cost, progress, kind)
  if kind~="DISTRICT" and kind~="BUILDING" and kind~="WONDER" then return nil,"INVALID_TARGET" end
  local values={charge,cost,progress}
  for i=1,3 do
    local v=values[i]
    if type(v)~="number" or v~=v or v==math.huge or v==-math.huge then return nil,"INVALID_VALUE" end
  end
  if charge<=0 or cost<=0 or progress<0 or progress>=cost then return nil,"NO_REMAINING" end
  local applied=math.min(charge,cost-progress)
  return {applied=applied,wasted=charge-applied,nextTarget=0}
end

function P.Snapshot(context, playerID, reason, cityID)
  if not P.IsTestPlayer(playerID) then return "OUTSIDE_TEST_CIV: capture refused",false end
  local lines = {}
  local unavailable, traversalErrors = 0, 0
  local turn = Game and Game.GetCurrentGameTurn and Game.GetCurrentGameTurn() or "?"
  local function log(key, value)
    lines[#lines+1] = "[SPC]["..P.VERSION.."]["..context.."][turn="..tostring(turn)
      .."][player="..tostring(playerID).."] "..key.." "..P.Encode(value)
  end
  local function read(key, object, method, ...)
    local ok,v = P.Call(object,method,...)
    if not ok then unavailable=unavailable+1 end
    log(key,{method=method,call=ok and "CALL_OK" or "UNAVAILABLE",value=v,semantics="USER_GAME_TEST_REQUIRED"})
    if ok then return v end
  end
  local function members(key, object, fn)
    local ok,err = pcall(function() for _,item in object:Members() do fn(item) end end)
    if not ok then traversalErrors=traversalErrors+1; log(key,{status="USER_GAME_TEST_REQUIRED",error=tostring(err)}) end
  end
  log("BEGIN",{reason=reason,status="USER_GAME_TEST_REQUIRED",context=context})
  local ok, err = pcall(function()
    local player = Players[playerID]
    assert(player,"PLAYER_ABSENT")
    local cities = read("CITIES",player,"GetCities")
    local capital=read("CAPITAL",cities,"GetCapitalCity")
    if capital then log("CAPITAL_ID",capital:GetID()) end
    local governors = read("GOVERNORS",player,"GetGovernors")
    read("NATIONAL_TITLES_NOT_LOCAL",governors,"GetGovernorPointsSpent")
    read("PLAYER_ERA",player,"GetEra")
    local yields = assert(P.Rows("Yields"))
    for _,tableName in ipairs({"District_CitizenGreatPersonPoints","Building_CitizenYieldChanges",
      "Building_YieldDistrictCopies","Boosts"}) do
      local rows,errorText=P.Rows(tableName)
      if not rows then log("DB_"..tableName,{error=errorText})
      else
        log("DB_COUNT_"..tableName,#rows)
        for _,r in ipairs(rows) do
          if tableName=="Building_YieldDistrictCopies" or P.Families[r.DistrictType] then
            log("DB_"..tableName,r)
          end
        end
      end
    end
    for _,r in ipairs(P.Rows("Districts") or {}) do
      log("DISTRICT_CLASSIFICATION",{type=r.DistrictType,RequiresPopulation=r.RequiresPopulation,
        InternalOnly=r.InternalOnly,CityCenter=r.CityCenter,family=P.Family(r.DistrictType),
        classification="USER_GAME_TEST_REQUIRED_DO_NOT_INFER_FROM_ONE_FLAG"})
    end
    members("CITY_ENUMERATION",cities,function(city)
      if cityID~=nil and city:GetID()~=cityID then return end
      local id=city:GetID()
      local key="CITY:"..tostring(id)
      log(key,{name=city:GetName(),x=city:GetX(),y=city:GetY()})
      read(key.." POPULATION",city,"GetPopulation")
      read(key.." MARKER",city,"GetProperty","SPC_P0_MARKER")
      read(key.." FIRST_COMPLETION",city,"GetProperty","SPC_P0_FIRST_SPEC")
      read(key.." HISTORY_ELIGIBLE",city,"GetProperty","SPC_P0_FIRST_ELIGIBLE")
      for n=2,4 do read(key.." ENGINE_GOV_REQ_"..n,city,"GetProperty","SPC_P0_GOV_REQ_"..n) end
      local gov=read(key.." GOVERNOR",city,"GetAssignedGovernor")
      if gov then
        read(key.." ESTABLISHED",gov,"IsEstablished")
        local govType=read(key.." GOVERNOR_TYPE",gov,"GetType")
        local govInfo=P.Info("Governors",govType)
        for _,r in ipairs(P.Rows("GovernorPromotionSets") or {}) do
          if govInfo and r.GovernorType==govInfo.GovernorType then
            local promotion=P.Info("GovernorPromotions",r.GovernorPromotion)
            if promotion then
              local has=read(key.." PROMOTION:"..r.GovernorPromotion,gov,"HasPromotion",promotion.Hash)
              log(key.." PROMOTION_METADATA",{type=r.GovernorPromotion,has=has,
                BaseAbility=promotion.BaseAbility,Level=promotion.Level,Column=promotion.Column})
            end
          end
        end
      end
      local districts=read(key.." DISTRICTS",city,"GetDistricts")
      members(key.." DISTRICT_ENUMERATION",districts,function(d)
        local info=P.Info("Districts",d:GetType())
        local dk=key.." DISTRICT:"..tostring(d:GetID())..":"..tostring(info and info.DistrictType)
        local plot=Map.GetPlot(d:GetX(),d:GetY())
        read(dk.." COMPLETE",d,"IsComplete")
        read(dk.." WORKERS",plot,"GetWorkerCount")
        read(dk.." PILLAGED",districts,"IsPillaged",d:GetType(),plot:GetIndex())
        for _,y in ipairs(yields) do
          read(dk.." BASE_CANDIDATE:"..y.YieldType,plot,"GetAdjacencyYield",playerID,id,d:GetType(),y.Index)
          read(dk.." ACTUAL_CANDIDATE:"..y.YieldType,d,"GetAdjacencyYield",y.Index)
        end
      end)
      local trade=read(key.." TRADE",city,"GetTrade")
      read(key.." OUTGOING_RAW",trade,"GetOutgoingRoutes")
      read(key.." INCOMING_CROSSCHECK_ONLY",trade,"GetIncomingRoutes")
      local queue=read(key.." BUILDQUEUE",city,"GetBuildQueue")
      local current=read(key.." CURRENT_TARGET",queue,"CurrentlyBuilding")
      if current then
        local building=P.Info("Buildings",current)
        local district=P.Info("Districts",current)
        local row=building or district
        if row then
          local kind=building and (building.IsWonder and "WONDER" or "BUILDING") or "DISTRICT"
          local stem=building and "Building" or "District"
          local cost=read(key.." TARGET_COST",queue,"Get"..stem.."Cost",row.Index)
          local progress=read(key.." TARGET_PROGRESS",queue,"Get"..stem.."Progress",row.Index)
          for _,spec in ipairs(P.Specs) do
            local preview,status=P.CrewPreview(spec.charge,cost,progress,kind)
            log(key.." CREW_DRY_RUN",{kind=kind,spec=spec,result=preview,error=status,status="USER_GAME_TEST_REQUIRED_NO_INJECTION"})
          end
        else log(key.." CREW_TARGET","INVALID_OR_UNRESOLVED_NO_INJECTION") end
      end
      local buildings=read(key.." BUILDINGS",city,"GetBuildings")
      local locations={}
      local plotsOK,cityPlots=pcall(function() return Map.GetCityPlots():GetPurchasedPlots(city) end)
      if plotsOK and type(cityPlots)=="table" then
        for _,plotID in pairs(cityPlots) do
          local at=read(key.." BUILDINGS_AT:"..tostring(plotID),buildings,"GetBuildingsAtLocation",plotID)
          if type(at)=="table" then for _,buildingID in pairs(at) do locations[buildingID]=plotID end end
        end
      else
        unavailable=unavailable+1
        log(key.." BUILDING_LOCATIONS",{status="USER_GAME_TEST_REQUIRED",error=tostring(cityPlots)})
      end
      for _,b in ipairs(P.Rows("Buildings") or {}) do
        local hasOK,has=P.Call(buildings,"HasBuilding",b.Index)
        if not hasOK then log(key.." BUILDING_ENUM",{status="USER_GAME_TEST_REQUIRED",reason=has}); break end
        if has then
          log(key.." BUILDING_PRESENT",{type=b.BuildingType,district=b.PrereqDistrict,IsWonder=b.IsWonder})
          local location=locations[b.Index]
          log(key.." BUILDING_LOCATION:"..b.BuildingType,{plot=location,status=location and "OBSERVED" or "USER_GAME_TEST_REQUIRED"})
          local slots=read(key.." WORK_SLOTS:"..b.BuildingType,buildings,"GetNumGreatWorkSlots",b.Index)
          if type(slots)=="number" then
            for slot=0,slots-1 do
              local instance=read(key.." WORK_SLOT",buildings,"GetGreatWorkInSlot",b.Index,slot)
              if type(instance)=="number" and instance>=0 then
                local typeID=read(key.." WORK_TYPE",buildings,"GetGreatWorkTypeFromIndex",instance)
                local work=P.Info("GreatWorks",typeID)
                log(key.." WORK",{instance=instance,typeID=typeID,type=work and work.GreatWorkType,
                  objectType=work and work.GreatWorkObjectType,era=work and work.EraType,slot=slot,
                  building=b.BuildingType,plot=location,standardCulture=work and P.WorkTypes[work.GreatWorkObjectType]==true})
                if work then
                  for _,yr in ipairs(P.Rows("GreatWork_YieldChanges") or {}) do
                    if yr.GreatWorkType==work.GreatWorkType then log(key.." WORK_INTRINSIC",yr) end
                  end
                end
              end
            end
          end
        end
      end
    end)
  end)
  if not ok then log("SNAPSHOT_ERROR",tostring(err)) end
  local complete=ok and traversalErrors==0 and unavailable==0
  log("END",{complete=complete,unavailableCalls=unavailable,traversalErrors=traversalErrors,semantics="USER_GAME_TEST_REQUIRED"})
  return table.concat(lines,"\n"),complete
end

-- Selected-city role facts only. No history reconstruction, defaults or writes.
function P.CityRoleFacts(city)
  local facts={status="PARTIAL_ROLE_FACTS",sourceContext="GAMEPLAY_PROBE",
    specializationStatus="UNKNOWN_NO_PERSISTENT_WRITER",potentialStatus="UNKNOWN_NO_PERSISTENT_WRITER",
    activeStatus="UNKNOWN_SPECIALIZATION_AND_POTENTIAL",capitalStatus="UNKNOWN",centerStatus="UNKNOWN",
    governorGateStatus="UNKNOWN"}
  local ok,owner=P.Call(city,"GetOwner")
  if not ok or not P.IsTestPlayer(owner) then facts.status="REJECTED_PLAYER";return facts end
  local idOK,id=P.Call(city,"GetID")
  if not idOK or type(id)~="number" then facts.status="UNKNOWN_CITY";return facts end
  facts.owner=owner;facts.cityID=id;facts.cityKey=owner..":"..id
  facts.identityKind="OWNER_CITY_ID_SNAPSHOT_ONLY"
  local function prop(key)
    local success,value=P.Call(city,"GetProperty",key)
    if not success then return false,nil end
    return true,value
  end
  -- Legacy diagnostic value is not a validated persistent specialization ledger.
  local legacyOK,legacy=prop("SPC_P0_FIRST_SPEC")
  facts.legacySpecDiagnostic=legacyOK and P.Scalar(legacy) or "GETTER_ERROR"
  local okCities,cities=P.Call(Players[owner],"GetCities")
  local okCapital,capital=false,nil
  if okCities then okCapital,capital=P.Call(cities,"GetCapitalCity") end
  if okCapital and capital then
    local a,capitalID=P.Call(capital,"GetID");local b,capitalOwner=P.Call(capital,"GetOwner")
    if a and b and type(capitalID)=="number" and capitalOwner==owner then
      facts.capitalStatus=capitalID==id and "YES" or "NO"
      if capitalID==id then facts.centerStatus="YES_CAPITAL" end
      -- A noncapital may be Commerce; unknown specialization must not become NO.
    end
  end
  local keys={"SPC_P0_GOV_CONTROL_A007","SPC_P0_GOV_PRESENT","SPC_P0_GOV_ESTABLISHED",
    "SPC_P0_GOV_REQ_2","SPC_P0_GOV_REQ_3","SPC_P0_GOV_REQ_4"}
  local values={};local valid=true
  for i,key in ipairs(keys) do
    local success,value=prop(key);values[i]=value
    if not success or (value~=nil and value~=0 and value~=1) then valid=false end
  end
  if valid and values[1]==1 then
    local present,established=values[2]==1,values[3]==1
    local two,three,four=values[4]==1,values[5]==1,values[6]==1
    if (established and not present) or ((two or three or four) and not established)
      or (four and not three) or (three and not two) then
      facts.governorGateStatus="UNKNOWN_INCONSISTENT_PROPERTIES"
    else
      facts.governorGateStatus="KNOWN"
      facts.governorLevelCeiling=four and 4 or three and 3 or two and 2 or 1
    end
  end
  return facts
end

-- Isolated, read-only A004 probes. Never serialize engine objects or call Snapshot.
function P.FocusProbe(city,action,stage)
  local function get(object,method,...)
    stage("BEFORE_"..method)
    local ok,value=P.Call(object,method,...)
    if not ok then error(method..":"..P.Scalar(value)) end
    return value
  end
  local out={"city="..P.Scalar(get(city,"GetID")).." mode="..action}
  if action=="GOVERNOR" then
    out[#out+1]="lookup=NATIVE_REQUIREMENTS (no governor Lua getter)"
    local control=get(city,"GetProperty","SPC_P0_GOV_CONTROL_A007")
    local present=get(city,"GetProperty","SPC_P0_GOV_PRESENT")
    local established=get(city,"GetProperty","SPC_P0_GOV_ESTABLISHED")
    out[#out+1]="control="..P.Scalar(control).." | present="..P.Scalar(present).." established="..P.Scalar(established)
    local raw={}
    for n=2,4 do raw[#raw+1]=P.Scalar(get(city,"GetProperty","SPC_P0_GOV_REQ_"..n)) end
    out[#out+1]="Established title thresholds 2/3/4="..table.concat(raw,"/")
    if control~=1 then
      out[#out+1]="NOT_READY: native probe control missing; do not infer no governor"
    else
      out[#out+1]="CONTROL_OK: raw conditions still require state-change validation"
    end
    out[#out+1]="1=condition active; nil/0=inactive candidate. No exact title count inferred."
    local role=P.CityRoleFacts(city)
    out[#out+1]="ROLE cityKey="..P.Scalar(role.cityKey).." | capital="..role.capitalStatus.." | center="..role.centerStatus
    out[#out+1]="Specialization=UNKNOWN | Potential=UNKNOWN | ACTIVE=UNKNOWN (no persistent writer)"
    out[#out+1]="Governor ceiling="..P.Scalar(role.governorLevelCeiling).." | "..role.governorGateStatus.." (not ACTIVE)"
    out[#out+1]="Legacy spec diagnostic="..P.Scalar(role.legacySpecDiagnostic).." (not adopted)"
  elseif action=="SPECIALISTS" then
    local owner=get(city,"GetOwner")
    local cityID=get(city,"GetID")
    local districts=get(Players[owner],"GetDistricts")
    stage("BEFORE_PLAYER_DISTRICT_MEMBERS")
    local method=P.Field(districts,"Members")
    if type(method)~="function" then error("PLAYER_DISTRICT_MEMBERS_ABSENT") end
    local iterator,state,key=method(districts)
    if type(iterator)~="function" then error("PLAYER_DISTRICT_ITERATOR_INVALID") end
    local scanned,count=0,0
    for _,d in iterator,state,key do
      scanned=scanned+1
      if scanned>512 then error("PLAYER_DISTRICT_SCAN_LIMIT") end
      local districtCity=get(d,"GetCity")
      if districtCity and get(districtCity,"GetOwner")==owner and get(districtCity,"GetID")==cityID then
      local info=P.Info("Districts",get(d,"GetType"))
      if not info then error("DISTRICT_DEFINITION_MISSING") end
      if info.RequiresPopulation==true or info.RequiresPopulation==1 or P.Families[info.DistrictType] then
        count=count+1
        if count>6 then error("DISPLAY_LIMIT: choose city with at most 6 specialty districts") end
        local x,y=get(d,"GetX"),get(d,"GetY")
        stage("BEFORE_GetPlot")
        local plot=Map.GetPlot(x,y)
        local workers=get(plot,"GetWorkerCount")
        if type(workers)~="number" or workers<0 or workers%1~=0 then error("WORKERS_INVALID") end
        local complete=get(d,"IsComplete")
        if type(complete)~="boolean" then error("IsComplete:NON_BOOLEAN") end
        out[#out+1]=P.Scalar(info.DistrictType).." workers="..workers.." complete="..tostring(complete)
      end
    end
    end -- selected city filter
    if count==0 then out[#out+1]="NO_SPECIALTY_DISTRICT (not a specialist test pass)" end
  else error("UNKNOWN_FOCUS_ACTION") end
  out[#out+1]="RAW_API_ONLY | USER_GAME_TEST_REQUIRED"
  return table.concat(out,"\n")
end

-- B003: bounded scalar-only observations. Adjacency and current routes run in UI.
-- Gameplay activity events are a separate diagnostic; neither grants effects.
function P.NetworkProbe(city,action,stage,page)
  local function get(o,m,...)
    stage("BEFORE_"..m)
    local ok,v=P.Call(o,m,...)
    if not ok then error(m..":"..P.Scalar(v)) end
    return v
  end
  local owner,id=get(city,"GetOwner"),get(city,"GetID")
  local out={"city="..id.." owner="..owner.." mode="..action}
  page=page or 1
  assert(type(page)=="number" and page>=1 and page%1==0 and page<=512,"PAGE_INVALID")
  if action=="ADJACENCY" then
    local collection=get(Players[owner],"GetDistricts")
    stage("BEFORE_PLAYER_DISTRICT_MEMBERS")
    local method=P.Field(collection,"Members")
    if type(method)~="function" then error("DISTRICT_MEMBERS_ABSENT") end
    local iter,state,key=method(collection)
    if type(iter)~="function" then error("DISTRICT_ITERATOR_INVALID") end
    local list,scanned={},0
    for _,d in iter,state,key do
      scanned=scanned+1;if scanned>512 then error("DISTRICT_SCAN_LIMIT") end
      local c=get(d,"GetCity")
      if c and get(c,"GetOwner")==owner and get(c,"GetID")==id then
        local dt=get(d,"GetType");local info=P.Info("Districts",dt)
        if not info then error("DISTRICT_DEFINITION_MISSING") end
        if info.RequiresPopulation==true or info.RequiresPopulation==1 or P.Families[info.DistrictType] then
          list[#list+1]={district=d,info=info,id=get(d,"GetID"),type=dt}
        end
      end
    end
    table.sort(list,function(a,b) return a.id<b.id end)
    if #list==0 then return table.concat(out,"\n").."\nNO_SPECIALTY_DISTRICT" end
    local index=(page-1)%#list+1;local item=list[index];local d=item.district
    out[#out+1]="district "..index.."/"..#list.." id="..item.id.." "..P.Scalar(item.info.DistrictType)
    out[#out+1]="complete="..P.Scalar(get(d,"IsComplete")).." | BASE_CANDIDATE / ACTUAL_CANDIDATE"
    local x,y=get(d,"GetX"),get(d,"GetY")
    stage("BEFORE_GetPlot");local plot=Map.GetPlot(x,y)
    local count=0
    for yield in GameInfo.Yields() do
      count=count+1;if count>12 then error("YIELD_DISPLAY_LIMIT") end
      stage("BEFORE_BASE_"..P.Scalar(yield.YieldType))
      local bok,b=P.Call(plot,"GetAdjacencyYield",owner,id,item.type,yield.Index)
      stage("BEFORE_ACTUAL_"..P.Scalar(yield.YieldType))
      local aok,a=P.Call(d,"GetAdjacencyYield",yield.Index)
      local function number(ok,v)
        if not ok or type(v)~="number" or v~=v or v==math.huge or v==-math.huge then return "UNKNOWN" end
        return tostring(v)
      end
      out[#out+1]=P.Scalar(yield.YieldType)..": "..number(bok,b).." / "..number(aok,a)
    end
    if count==0 then error("YIELDS_EMPTY") end
    out[#out+1]="UI_ONLY: UNKNOWN is not zero; policy/cross-yield semantics unverified"
  elseif action=="TRADE" then
    local trade=get(city,"GetTrade")
    local routes=get(trade,"GetOutgoingRoutes")
    if type(routes)~="table" then error("ROUTES_NOT_TABLE") end
    local list={}
    -- Only array entries + named scalar fields; never encode the route object.
    for i=1,257 do
      local row=routes[i];if row==nil then break end
      if i>256 then error("ROUTE_SCAN_LIMIT") end
      list[#list+1]=row
    end
    local diagnostics=out
    out={"商路读取 · 本城出发共 "..#list.." 条（不是全国总数）"}
    diagnostics[#diagnostics+1]="UI OUTGOING rawCount="..#list.." (not recipient N)"
    if #list==0 then out[#out+1]="本城当前没有出发商路。";diagnostics[#diagnostics+1]="NO_OUTGOING_ROUTES" else
      local index=(page-1)%#list+1;local row=list[index]
      out[#out+1]="当前第 "..index.." / "..#list.." 条 · Next district / route 查看下一条"
      diagnostics[#diagnostics+1]="route "..index.."/"..#list.." trader="..P.Scalar(P.Field(row,"TraderUnitID"))
      local op,oc=P.Field(row,"OriginCityPlayer"),P.Field(row,"OriginCityID")
      local dp,dc=P.Field(row,"DestinationCityPlayer"),P.Field(row,"DestinationCityID")
      local function endpoint(p,c)
        local text=P.Scalar(p)..":"..P.Scalar(c)
        if type(p)~="number" or type(c)~="number" then return text.." UNKNOWN", "未知端点 ("..text..")" end
        local player=Players[p]
        local cok,cities=P.Call(player,"GetCities");local fok,found=P.Call(cok and cities or nil,"FindID",c)
        if not fok or not found then return text.." UNRESOLVED", "城市未解析 ("..text..")" end
        local nok,name=P.Call(found,"GetName")
        if nok and type(name)=="string" and Locale and Locale.Lookup then name=Locale.Lookup(name) end
        local ook,actualOwner=P.Call(found,"GetOwner")
        return text.." "..(nok and P.Scalar(name) or "UNKNOWN_NAME").." currentOwner="..(ook and P.Scalar(actualOwner) or "UNKNOWN"), (nok and type(name)=="string" and P.Scalar(name) or "城市名未知 ("..text..")")
      end
      local originDetail,originName=endpoint(op,oc)
      local destinationDetail,destinationName=endpoint(dp,dc)
      out[#out+1]="出发："..originName
      out[#out+1]="到达："..destinationName
      diagnostics[#diagnostics+1]="FROM "..originDetail
      diagnostics[#diagnostics+1]="TO   "..destinationDetail
      diagnostics[#diagnostics+1]="originMatchesSelection="..tostring(op==owner and oc==id)
      diagnostics[#diagnostics+1]="sameOwnerRaw="..(type(op)=="number" and type(dp)=="number" and tostring(op==dp) or "UNKNOWN")
    end
    out[#out+1]="仅显示商路端点；尚未判定专业网络接收关系。"
    out[#out+1]=""
    out[#out+1]="排错信息（无需手抄 ID）"
    out[#out+1]=table.concat(diagnostics,"\n")
  else error("UNKNOWN_NETWORK_PROBE") end
  return table.concat(out,"\n")
end

-- Instrument only owned call sites; do not monkey-patch engine objects.
include('PerformanceCounters')
P.Count=SPCPerformance.Count
function P.HasBuilding(object,id) P.Count('building_check');return object:HasBuilding(id) end
function P.CreateBuilding(object,id) P.Count('building_create');local r=object:CreateBuilding(id);ExposedMembers.SPC_RuntimeUIRevision=(ExposedMembers.SPC_RuntimeUIRevision or 0)+1;return r end
function P.RemoveBuilding(object,id) P.Count('building_remove');local r=object:RemoveBuilding(id);ExposedMembers.SPC_RuntimeUIRevision=(ExposedMembers.SPC_RuntimeUIRevision or 0)+1;return r end
function P.SetProperty(object,key,value) P.Count('property_write');local r=object:SetProperty(key,value);ExposedMembers.SPC_RuntimeUIRevision=(ExposedMembers.SPC_RuntimeUIRevision or 0)+1;return r end
-- A live non-trader is a reliable negative. Missing/removed/unknown unit is not.
function P.RouteUnitRelevant(pid,id)
 if type(pid)~='number' or type(id)~='number' then return true end
 local player=Players and Players[pid]
 if not player then return true end
 local ok,u=pcall(function() return player:GetUnits():FindID(id) end)
 if not ok or not u then return true end
 local good,info=pcall(function() return P.Info('Units',u:GetType()) end)
 if not good or not info or info.MakeTradeRoute==nil then return true end
 return info.MakeTradeRoute==true or info.MakeTradeRoute==1
end
