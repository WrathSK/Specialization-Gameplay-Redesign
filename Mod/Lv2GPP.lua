include('RuntimeWork')
include('SpecialistSupport')
-- B035: working-specialist count -> native building base GPP. No ChangePointsTotal.
SPCLv2GPP={}
function SPCLv2GPP.Start(P,shared)
 local batch
 local data={ready=false,busy=false,changes=0,refreshes=0,errors={}};shared.Lv2GPP=data
 local kinds={"RESEARCH","CULTURE","INDUSTRY","COMMERCE"}
 local districts={RESEARCH="DISTRICT_CAMPUS",CULTURE="DISTRICT_THEATER",INDUSTRY="DISTRICT_INDUSTRIAL_ZONE",COMMERCE="DISTRICT_COMMERCIAL_HUB"}
 local classes={RESEARCH={"SCIENTIST"},CULTURE={"WRITER","ARTIST","MUSICIAN"},INDUSTRY={"ENGINEER"},COMMERCE={"MERCHANT"}}
 local definitions
 local function int(v) return type(v)=="number" and v>=0 and v%1==0 and v<math.huge end
 local function name(kind,bit) return "BUILDING_SPC_DEV_GPP_"..kind.."_"..bit end
 local function validateDefinitions()
  if definitions then return end
  local rows=P.Rows("Building_GreatPersonPoints");assert(rows,"GPP_DATABASE_UNAVAILABLE")
  for _,kind in ipairs(kinds) do for bit=0,7 do
   local building=name(kind,bit);local b=P.Info("Buildings",building)
   assert(b and type(b.Index)=="number" and b.PrereqDistrict==districts[kind] and b.Housing==0 and b.CitizenSlots==0,"B035_BUILDING_DATABASE_MISMATCH "..building)
   local expected={};for _,cl in ipairs(classes[kind]) do expected["GREAT_PERSON_CLASS_"..cl]=true end
   local seen={}
   for _,r in ipairs(rows) do if r.BuildingType==building then
    assert(expected[r.GreatPersonClassType] and not seen[r.GreatPersonClassType] and r.PointsPerTurn==2*2^bit,"B035_BASE_GPP_DATABASE_MISMATCH "..building)
    seen[r.GreatPersonClassType]=true
   end end
   for cl in pairs(expected) do assert(seen[cl],"B035_GPP_DEFINITION_MISSING "..building) end
  end end
  definitions=true
 end
 local function inspect(pid,city)
  local kind,d,f=SPCSpecialistSupport.Anchor(P,shared,pid,city,batch or SPCRuntimeWork.New(P,shared))
  if not classes[kind] then return {workers=0,enabled=false,reason='CONFIRMED_INELIGIBLE'} end
  if f.active<2 then return {kind=kind,active=f.active,workers=0,enabled=false,reason='ACTIVE_BELOW_II'} end
  local plot=assert(Map.GetPlot(d:GetX(),d:GetY()),'B2_GPP_PLOT_UNAVAILABLE')
  local n=plot:GetWorkerCount();assert(int(n) and n<=255,'WORKER_COUNT_UNKNOWN_OR_UNSUPPORTED')
  return {kind=kind,workers=n,active=f.active,enabled=true,reason='VERIFIED anchor='..d:GetID()}
 end

 local function set(city,id,wanted)
  local b=city:GetBuildings();local present=P.HasBuilding(b,id);assert(type(present)=="boolean","GPP_CARRIER_READ_UNKNOWN")
  if present==wanted then return end
  if wanted then P.CreateBuilding(city:GetBuildQueue(),id) else P.RemoveBuilding(b,id) end
  assert(P.HasBuilding(b,id)==wanted,"GPP_CARRIER_CHANGE_UNCONFIRMED");data.changes=data.changes+1
 end
 local function reconcile(pid,city)
  validateDefinitions();local f=inspect(pid,city)
  local n=f.enabled and f.workers or 0
  local kind=f.kind
  local wanted={}
  for _,k in ipairs(kinds) do for bit=0,7 do
   wanted[name(k,bit)]=k==kind and math.floor(n/2^bit)%2==1
  end end
  -- Verify every installed carrier before any write; UNKNOWN holds projection.
  for _,k in ipairs(kinds) do for bit=0,7 do
   local b=P.Info('Buildings',name(k,bit))
   assert(type(P.HasBuilding(city:GetBuildings(),b.Index))=='boolean','GPP_CARRIER_READ_UNKNOWN')
  end end
  -- Remove all stale classes/bits before adding the new count. No cumulative reward.
  for _,k in ipairs(kinds) do for bit=0,7 do
   local key=name(k,bit);local b=P.Info("Buildings",key)
   if b and not wanted[key] then set(city,b.Index,false) end
  end end
  for _,k in ipairs(kinds) do for bit=0,7 do
   local key=name(k,bit);if wanted[key] then set(city,P.Info("Buildings",key).Index,true) end
  end end
 end
 function data.Audit(scope)
  if not data.ready or data.busy then P.Count('busy_skip');return end
  data.busy=true;batch=SPCRuntimeWork.New(P,shared);data.refreshes=data.refreshes+1
  if type(scope)~='table' or scope.player==nil then data.errors={} end
  for pid,player in pairs(Players) do if SPCRuntimeWork.Player(scope,pid) then
   local good,err=pcall(function()
    local cities=player:GetCities()
    if cities then for _,city in cities:Members() do P.Count('city_scan');
     local key=pid..":"..city:GetID();local ok,e=pcall(reconcile,pid,city)
     data.errors[key]=not ok and tostring(e) or nil

    end end
   end)
   data.errors['player:'..pid]=not good and tostring(err) or nil
  end end
  data.busy=false;batch=nil
 end
 function data.Describe(pid,city)
  local ok,result=pcall(function()
   assert(data.ready,"GPP_NOT_READY");validateDefinitions()
   local f=inspect(pid,city);local n=f.enabled and f.workers or 0;local actual,other=0,0
   for _,kind in ipairs(kinds) do for bit=0,7 do
    if P.HasBuilding(city:GetBuildings(),P.Info("Buildings",name(kind,bit)).Index) then
     if kind==f.kind then actual=actual+2^bit else other=other+2^bit end
    end
   end end
   local native={}
   for _,cl in ipairs(classes[f.kind] or {}) do
    local good,value=pcall(function()
     local info=P.Info("GreatPersonClasses","GREAT_PERSON_CLASS_"..cl)
     return Players[pid]:GetGreatPeoplePoints():GetPointsPerTurn(info.Index)
    end)
    native[#native+1]=cl..":"..(good and type(value)=="number" and tostring(value) or "UNKNOWN")
   end
   local err=data.errors[pid..":"..city:GetID()]
   return "city="..city:GetID().." "..(f.kind or f.reason).." ACTIVE="..tostring(f.active).." workers="..f.workers
    .."\nAdded BASE per class: expected="..2*n.." carrier="..2*actual.." other="..other
    .."\nNative EMPIRE GPP/turn: "..(#native>0 and table.concat(native," | ") or "N/A")
    .."\nchanges="..data.changes.." refreshes="..data.refreshes.." "..f.reason..(err and " ERROR="..err or "")
    .."\nRead only. Carrier is base, not measured final GPP. UNKNOWN: use Great People UI."
  end)
  local out="P0-B2 Lv2 GPP | "..(ok and result or "ERROR "..tostring(result));print("[SPC][B035] "..out);return out
 end
 local function bind(events,event,fn) local e=P.Field(events,event);if e and e.Add then e.Add(fn) end end
 bind(Events,"LoadScreenClose",function() data.ready=true;data.errors={};data.Audit() end)
 for _,event in ipairs({"CityWorkerChanged","CityFocusChanged","GovernorAssigned","GovernorEstablished","GovernorChanged","GovernorPromoted","PlayerTurnActivated","CityTransfered","CityRemovedFromMap","DistrictRemovedFromMap","DistrictBuildProgressChanged","DistrictPillaged","DistrictRepaired","BuildingAddedToMap","BuildingRemovedFromMap","BuildingPillaged","BuildingRepaired"}) do SPCRuntimeWork.Hook(P,Events,event,data.Audit) end
 for _,event in ipairs({"OnDistrictConstructed","BuildingConstructed","CityBuilt","OnPillage"}) do bind(GameEvents,event,data.Audit) end
 -- E2 confirmed exit: exact transient IDs owned by this writer; no prefix scan.
 if shared.CityProgressionStore then shared.CityProgressionStore.RegisterExit('Lv2GPP',function(c,loss)
   local ids={};for _,k in ipairs(kinds)do for bit=0,7 do ids[#ids+1]=name(k,bit)end end
   shared.CityProgressionStore.RemoveOwned(c,loss,ids)
 end)end

end
