-- B024 automatic constant Lv1 carriers; bounded existing DEV facts, not general eligibility.
SPCResearchSupport={}
function SPCResearchSupport.Start(P,shared)
 local data={changes=0,ready=false,errors={},scan="NOT_RUN",events=0};shared.ResearchSupport=data
 local kinds={"RESEARCH","CULTURE","COMMERCE"}
 local districts={RESEARCH="DISTRICT_CAMPUS",CULTURE="DISTRICT_THEATER",COMMERCE="DISTRICT_COMMERCIAL_HUB"}
 local function definition(kind)
  local row=P.Info("Buildings","BUILDING_SPC_DEV_"..kind.."_SUPPORT")
  assert(row and type(row.Index)=="number","B024_DATABASE_MISSING "..kind..": new test game required")
  return row.Index
 end
 local function eligible(pid,city)
  assert(city:GetOwner()==pid and P.IsTestPlayer(pid),"OUTSIDE_TEST_OWNER")
  local f=shared.EffectiveFacts.Read(pid,city)
  if not districts[f.specialization] then return nil end
  assert(f.potential>=1 and f.first,"SPECIALTY_FACT_INVALID")
  local count=0
  for _,d in Players[pid]:GetDistricts():Members() do
   count=count+1;assert(count<=512,"DISTRICT_SCAN_LIMIT")
   local c=d:GetCity()
   if c and c:GetID()==city:GetID() and c:GetOwner()==pid and d:GetID()==f.first.districtID then
    local info=P.Info("Districts",d:GetType())
    assert(info and info.DistrictType==f.first.type and d:IsComplete()==true,"SPECIALTY_DISTRICT_CHANGED")
    assert(info.DistrictType==districts[f.specialization],"UNIQUE_DISTRICT_NOT_IN_B024")
    return f.specialization,d
   end
  end
  error("SPECIALTY_DISTRICT_MISSING")
 end
 local function set(city,id,wanted)
  local b=city:GetBuildings();local present=b:HasBuilding(id)
  assert(type(present)=="boolean","BUILDING_READ_UNKNOWN")
  if present==wanted then return end
  data.changes=data.changes+1
  if wanted then city:GetBuildQueue():CreateBuilding(id) else b:RemoveBuilding(id) end
  assert(b:HasBuilding(id)==wanted,"CARRIER_CHANGE_UNCONFIRMED")
 end
 local function key(pid,city) return pid..":"..city:GetID() end
 local function reconcile(pid,city)
  local wanted
  local ok,result=pcall(eligible,pid,city)
  if ok then wanted=result end
  -- Never infer facts from buildings. Remove every wrong carrier before adding one.
  for _,kind in ipairs(kinds) do
   local row=P.Info("Buildings","BUILDING_SPC_DEV_"..kind.."_SUPPORT")
   if row and kind~=wanted then set(city,row.Index,false) end
  end
  if wanted then set(city,definition(wanted),true) end
  return wanted
 end
 local function process(pid,city)
  local k=key(pid,city)
  if data.errors[k] then return end
  local ok,err=pcall(reconcile,pid,city)
  if not ok then data.errors[k]=tostring(err);print("[SPC][B024][AUTO_ERROR] "..k.." "..tostring(err)) end
 end
 function data.Audit()
  if not data.ready or data.busy then return end
  data.busy=true
  local checked,skipped=0,0
  local scanOK,scanError=pcall(function()
   for pid,player in pairs(Players) do
    -- One unused/unready player must not abort every other player's cities.
    local ok,err=pcall(function()
     local cities=player:GetCities()
     if not cities then return end
     for _,city in cities:Members() do process(pid,city);checked=checked+1 end
    end)
    if not ok then skipped=skipped+1;print("[SPC][B024][PLAYER_SCAN_ERROR] "..tostring(pid).." "..tostring(err)) end
   end
  end)
  data.busy=false
  data.scan=scanOK and ("cities="..checked.." skippedPlayers="..skipped) or ("ERROR "..tostring(scanError))
  print("[SPC][B024][SCAN] "..data.scan)
 end
 local function completed(pid,index,x,y)
  if not data.ready or data.busy then return end
  data.events=data.events+1
  data.busy=true
  local ok,err=pcall(function()
   local d=CityManager.GetDistrictAt(x,y)
   local city=d and d:GetCity()
   assert(city and city:GetOwner()==pid,"EVENT_CITY_NOT_READY")
   process(pid,city)
  end)
  data.busy=false
  if not ok then data.scan="EVENT_ERROR "..tostring(err) end
 end
 function data.Run(pid,city,action)
  -- Read-only diagnostic. Old ON/OFF request names cannot override automatic mode.
  local ok,result=pcall(function()
   assert(data.ready,"AUTO_NOT_READY")
   assert(not data.errors[key(pid,city)],data.errors[key(pid,city)])
   local permitted,kind,d=pcall(eligible,pid,city)
   local expected=permitted and kind or nil
   local enabled={}
   for _,k in ipairs(kinds) do
    local row=P.Info("Buildings","BUILDING_SPC_DEV_"..k.."_SUPPORT")
    if row and city:GetBuildings():HasBuilding(row.Index) then enabled[#enabled+1]=k end
   end
   if expected then definition(expected) end
   local workers="N/A"
   if d and permitted then
    local good,n=pcall(function() return Map.GetPlot(d:GetX(),d:GetY()):GetWorkerCount() end)
    if good and type(n)=="number" and n>=0 and n%1==0 then workers=n else workers="UNKNOWN" end
   end
   return "city="..city:GetID().." AUTO expected="..(expected or "NONE")
    .."\ncarrier="..(#enabled==0 and "NONE" or table.concat(enabled,",")).." workers="..workers
    .."\nchanges this load="..data.changes.." events="..data.events.." scan="..data.scan
    .."\n"..(permitted and "Native per worker +3 Food / +3 Production when carrier active." or tostring(kind))
    .."\nRead only; inspect actual citizen yields. No ON/OFF needed."
  end)
  local out="B024 Auto Lv1 | "..(ok and result or "ERROR "..tostring(result))
  print("[SPC][B024] "..out);return out
 end
 local load=P.Field(Events,"LoadScreenClose")
 if load and load.Add then load.Add(function() data.ready=true;data.Audit() end) end
 for _,name in ipairs({"PlayerTurnActivated","CityTransfered"}) do
  local event=P.Field(Events,name);if event and event.Add then event.Add(data.Audit) end
 end
 -- Installed after B015/B021, so facts are committed before effects are reconciled.
 local event=P.Field(GameEvents,"OnDistrictConstructed")
 if event and event.Add then event.Add(completed) end
 local built=P.Field(GameEvents,"CityBuilt")
 if built and built.Add then built.Add(data.Audit) end
end
