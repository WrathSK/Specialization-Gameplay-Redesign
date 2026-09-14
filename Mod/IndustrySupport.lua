-- B036 IND-001: native per-specialist Food + base Production adjacency.
-- No actual-adjacency fallback, rounding or city-wide multiplication. Crew access is independently audited.
SPCIndustrySupport={}
function SPCIndustrySupport.Start(P,shared)
 local data={ready=false,busy=false,changes=0,errors={}};shared.IndustrySupport=data
 local samples={}
 local function name(bit) return 'BUILDING_SPC_DEV_INDUSTRY_LV1_'..bit end
 local function inspect(pid,city)
  if city:GetOwner()~=pid or not P.IsTestPlayer(pid) then return nil end
  local f=shared.EffectiveFacts.Read(pid,city)
  if f.specialization~='INDUSTRY' then return nil end
  assert(f.potential>=1 and f.first,'INDUSTRY_FACT_INVALID')
  for _,d in Players[pid]:GetDistricts():Members() do P.Count('district_scan');
   local c=d:GetCity()
   if c and c:GetOwner()==pid and c:GetID()==city:GetID() and d:GetID()==f.first.districtID then
    local row=P.Info('Districts',d:GetType())
    assert(row and row.DistrictType=='DISTRICT_INDUSTRIAL_ZONE' and f.first.type==row.DistrictType and d:IsComplete()==true,'INDUSTRY_ANCHOR_CHANGED')
    local sample=samples[pid..':'..city:GetID()]
    assert(sample and sample.districtID==d:GetID(),'BASE_BACKGROUND_SAMPLE_PENDING')
    local n=sample.value
    assert(type(n)=='number' and n>=0 and n<=255 and n%1==0,'BASE_ADJACENCY_UNKNOWN_FRACTIONAL_OR_OUT_OF_RANGE')
    return n
   end
  end
  error('INDUSTRY_DISTRICT_MISSING')
 end
 local function carriers(city,n,write)
  local total,food=0,0
  for bit=-1,7 do
   local row=P.Info('Buildings',name(bit));assert(row and row.Index,'B036_DATABASE_MISSING: restart/new test game required')
   local wanted=n~=nil and (bit==-1 or math.floor(n/2^bit)%2==1)
   local b=city:GetBuildings();local present=P.HasBuilding(b,row.Index)
   assert(type(present)=='boolean','CARRIER_READ_UNKNOWN')
   if write and present~=wanted then
    if wanted then P.CreateBuilding(city:GetBuildQueue(),row.Index) else P.RemoveBuilding(b,row.Index) end
    assert(P.HasBuilding(b,row.Index)==wanted,'CARRIER_WRITE_UNCONFIRMED')
    data.changes=data.changes+1;present=wanted
   end
   if present then if bit==-1 then food=3 else total=total+2^bit end end
  end
  return total,food
 end
 function data.Audit()
  if not data.ready or data.busy then P.Count('busy_skip');return end;data.busy=true
  for pid,player in pairs(Players) do
   local scanOK,scanError=pcall(function()
    local cities=player:GetCities();if not cities then return end
    for _,city in cities:Members() do P.Count('city_scan');
     local k=pid..':'..city:GetID();local ok,n=pcall(inspect,pid,city)
     local changed,err=pcall(carriers,city,ok and n or nil,true)
     data.errors[k]=not ok and tostring(n) or (not changed and tostring(err) or nil)
     if data.errors[k] then print('[SPC][B036][ERROR] '..k..' '..data.errors[k]) end
    end
   end)
   if not scanOK then print('[SPC][B036][SCAN_ERROR] '..tostring(scanError)) end
  end
  data.busy=false
  if shared.Lv3Support then shared.Lv3Support.Audit() end
  if shared.CrewProjects then shared.CrewProjects.Audit() end
 end
 data.ReadBase=inspect
 function data.Receive(pid,params)
  if not data.ready or not P.IsTestPlayer(pid) then return end
  if type(params.CityID)~='number' or type(params.DistrictID)~='number' or type(params.BaseProduction)~='number' then return end
  local n=params.BaseProduction
  if n~=-1 and not (n>=0 and n<=255 and n%1==0) then return end
  -- Only a current owned matching district is admitted; inspect still checks permanent specialty anchor.
  for _,d in Players[pid]:GetDistricts():Members() do P.Count('district_scan');
   local c=d:GetCity();local row=P.Info('Districts',d:GetType())
   if c and c:GetOwner()==pid and c:GetID()==params.CityID and d:GetID()==params.DistrictID
    and row and row.DistrictType=='DISTRICT_INDUSTRIAL_ZONE' and d:IsComplete()==true then
    samples[pid..':'..c:GetID()]={districtID=d:GetID(),value=n};data.Audit();return
   end
  end
 end
 function data.Describe(pid,city)
  local ok,n=pcall(inspect,pid,city)
  local valid,p,f=pcall(carriers,city,nil,false)
  return 'B036 Industry Lv1 city='..city:GetID()
   ..'\nBASE Production adjacency='..(ok and tostring(n or 'N/A') or 'ERROR '..tostring(n))
   ..'\nPer worker expected='..(ok and n~=nil and ('3F / '..n..'P') or 'NONE')
   ..' carrier='..(valid and (f..'F / '..p..'P') or ('ERROR '..tostring(p)))
   ..'\nchanges='..data.changes..' error='..tostring(data.errors[pid..':'..city:GetID()] or 'NONE')
   ..'\nRead only; verify native specialist yields. Crew projects available from Industry Lv1; project engine behavior requires B044 testing.'
 end
 local function hook(source,name,fn) local e=P.Field(source,name);if e and e.Add then e.Add(fn) end end
 hook(Events,'LoadScreenClose',function() data.ready=true;data.Audit() end)
 for _,n in ipairs({'PlayerTurnActivated','PlayerTurnDeactivated','CityTransfered','DistrictAddedToMap','DistrictRemovedFromMap','DistrictBuildProgressChanged','ImprovementAddedToMap','ImprovementRemovedFromMap','FeatureRemovedFromMap','CityWorkerChanged'}) do hook(Events,n,data.Audit) end
 for _,n in ipairs({'OnDistrictConstructed','OnBuildingConstructed','CityBuilt'}) do hook(GameEvents,n,data.Audit) end
end
