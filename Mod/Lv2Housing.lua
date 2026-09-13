-- B034: disposable native housing carriers, rebuilt from effective city facts.
SPCLv2Housing={}
function SPCLv2Housing.Start(P,shared)
 local data={ready=false,busy=false,changes=0,errors={},events=0}
 shared.Lv2Housing=data
 local families={RESEARCH="DISTRICT_CAMPUS",CULTURE="DISTRICT_THEATER",COMMERCE="DISTRICT_COMMERCIAL_HUB",INDUSTRY="DISTRICT_INDUSTRIAL_ZONE"}
 local function carrier(i)
  local row=P.Info("Buildings","BUILDING_SPC_DEV_LV2_HOUSING_"..i)
  assert(row and type(row.Index)=="number","B034_DATABASE_MISSING: reload updated mod database")
  return row.Index
 end
 local function expected(pid,city)
  local wanted={}
  if not P.IsTestPlayer(pid) then return wanted,"OUTSIDE_TEST_OWNER" end
  assert(city:GetOwner()==pid,"OWNER_CHANGED")
  local f=shared.EffectiveFacts.Read(pid,city)
  local districtType=families[f.specialization]
  if not districtType then return wanted,"NO_SUPPORTED_SPECIALIZATION" end
  if type(f.active)~="number" then return wanted,"ACTIVE_UNKNOWN" end
  if f.active<2 then return wanted,"ACTIVE="..f.active end
  local found=false
  for _,d in Players[pid]:GetDistricts():Members() do
   local ownerCity=d:GetCity()
   if ownerCity and ownerCity:GetID()==city:GetID() and ownerCity:GetOwner()==pid and f.first and d:GetID()==f.first.districtID then
    local row=P.Info("Districts",d:GetType())
    assert(row and row.DistrictType==districtType and f.first.type==districtType and d:IsComplete()==true,"SPECIALTY_DISTRICT_CHANGED")
    found=true
   end
  end
  assert(found,"SPECIALTY_DISTRICT_MISSING")
  wanted[0]=true
  local map=P.Field(GameInfo,"SPC_Lv2HousingTiers")
  assert(map,"B034_TIER_DATABASE_MISSING")
  for row in map() do
   if row.DistrictType==districtType then
    assert(type(row.Tier)=="number" and row.Tier>=1 and row.Tier<=8 and row.Tier%1==0,"UNSUPPORTED_BUILDING_TIER")
    local b=P.Info("Buildings",row.BuildingType)
    if b and city:GetBuildings():HasBuilding(b.Index) then wanted[row.Tier]=true end
   end
  end
  return wanted,f.specialization.." ACTIVE="..f.active
 end
 local function set(city,id,wanted)
  local buildings=city:GetBuildings();local present=buildings:HasBuilding(id)
  assert(type(present)=="boolean","HOUSING_CARRIER_READ_UNKNOWN")
  if present==wanted then return end
  if wanted then city:GetBuildQueue():CreateBuilding(id) else buildings:RemoveBuilding(id) end
  assert(buildings:HasBuilding(id)==wanted,"HOUSING_CHANGE_UNCONFIRMED")
  data.changes=data.changes+1
 end
 local function process(pid,city)
  local k=pid..":"..city:GetID()
  local ok,wanted,reason=pcall(expected,pid,city)
  -- Invalid facts cannot retain advanced housing. Retry on the next real event.
  if not ok then reason=tostring(wanted);wanted={} end
  local applied,err=pcall(function()
   local ids={};for i=0,8 do ids[i]=carrier(i) end
   for i=0,8 do if not wanted[i] then set(city,ids[i],false) end end
   for i=0,8 do if wanted[i] then set(city,ids[i],true) end end
  end)
  data.errors[k]=(not applied and tostring(err)) or (not ok and reason) or nil
  if data.errors[k] then print("[SPC][B034][HOUSING_ERROR] "..k.." "..data.errors[k]) end
 end
 function data.Audit()
  if not data.ready or data.busy then return end
  data.busy=true;data.events=data.events+1
  for pid,player in pairs(Players) do
   local ok,err=pcall(function()
    local cities=player:GetCities()
    if cities then for _,city in cities:Members() do process(pid,city) end end
   end)
   if not ok then print("[SPC][B034][SCAN_ERROR] "..tostring(pid).." "..tostring(err)) end
  end
  data.busy=false
 end
 function data.Describe(pid,city)
  -- Read is intentionally not a reconciliation trigger.
  local ok,out=pcall(function()
   assert(data.ready,"HOUSING_NOT_READY")
   local wanted,reason=expected(pid,city);local n,actual,tiers=0,0,{}
   for i=0,8 do
    if wanted[i] then n=n+1;if i>0 then tiers[#tiers+1]=i end end
    if city:GetBuildings():HasBuilding(carrier(i)) then actual=actual+1 end
   end
   local err=data.errors[pid..":"..city:GetID()]
   return "city="..city:GetID().." "..reason
    .."\nHousing expected=+"..n.." carrier=+"..actual.." tiers="..(#tiers>0 and table.concat(tiers,",") or "NONE")
    .."\nchanges="..data.changes.." refreshes="..data.events..(err and " ERROR="..err or "")
    .."\nRead only; compare actual housing in city UI."
    .."\nLv2 GPP is separate; other advanced yields not enabled."
  end)
  local out="B034 Lv2 Housing | "..(ok and out or "ERROR "..tostring(out))
  print("[SPC][B034] "..out);return out
 end
 local function bind(events,name,fn)
  local e=P.Field(events,name);if e and e.Add then e.Add(fn) end
 end
 bind(Events,"LoadScreenClose",function() data.ready=true;data.Audit() end)
 for _,name in ipairs({"GovernorAssigned","GovernorEstablished","GovernorChanged","PlayerTurnActivated","CityTransfered","CityBuildingsChanged"}) do bind(Events,name,data.Audit) end
 for _,name in ipairs({"BuildingConstructed","OnDistrictConstructed","CityBuilt"}) do bind(GameEvents,name,data.Audit) end
end
