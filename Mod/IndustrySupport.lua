include('RuntimeWork')
include('SampleLifecycle')
-- B036 IND-001: native per-specialist Food + base Production adjacency.
-- No actual-adjacency fallback, rounding or city-wide multiplication. Crew access is independently audited.
SPCIndustrySupport={}
function SPCIndustrySupport.Start(P,shared)
 local batch
 local function readFacts(pid,c) return batch and batch.Facts(pid,c) or shared.EffectiveFacts.Read(pid,c) end
 local data={ready=false,busy=false,changes=0,errors={}};shared.IndustrySupport=data
 SPCSampleLifecycle.Reset(data,'industry')
 local function name(bit) return 'BUILDING_SPC_DEV_INDUSTRY_LV1_'..bit end
 local function inspect(pid,city,externalBatch)
  if city:GetOwner()~=pid or not P.IsTestPlayer(pid) then return nil end
  local f=externalBatch and externalBatch.Facts(pid,city) or readFacts(pid,city)
  assert(type(f.specialization)=='string','INDUSTRY_FACT_INVALID')
  if f.specialization~='INDUSTRY' then return nil end
  assert(f.potential>=1 and f.first,'INDUSTRY_FACT_INVALID')
  for _,d in (externalBatch or batch or SPCRuntimeWork.New(P,shared)).Districts(pid,city) do
   local c=d:GetCity()
   if c and c:GetOwner()==pid and c:GetID()==city:GetID() and d:GetID()==f.first.districtID then
    local row=P.Info('Districts',d:GetType())
    assert(row and type(d:IsComplete())=='boolean','INDUSTRY_FACT_INVALID')
    if row.DistrictType~='DISTRICT_INDUSTRIAL_ZONE' or f.first.type~=row.DistrictType or d:IsComplete()~=true then return nil end
    local batch=data.samples[pid];local sample=batch and batch.rows[city:GetID()..':'..d:GetID()]
    assert(sample,'BASE_BACKGROUND_SAMPLE_PENDING')
    if sample.reference~=SPCSampleLifecycle.Reference(city,d,row) then return nil end
    local n=sample.value
    assert(type(n)=='number' and n>=0 and n<=255 and n%1==0,'BASE_ADJACENCY_UNKNOWN_FRACTIONAL_OR_OUT_OF_RANGE')
    return n
   end
  end
  return nil -- complete enumeration proves anchor absent
 end
 local function carriers(city,n,write)
  local total,food=0,0;local removed=false
  for bit=-1,7 do
   local row=P.Info('Buildings',name(bit));assert(row and row.Index,'B036_DATABASE_MISSING: restart/new test game required')
   local wanted=n~=nil and (bit==-1 or math.floor(n/2^bit)%2==1)
   local b=city:GetBuildings();local present=P.HasBuilding(b,row.Index)
   assert(type(present)=='boolean','CARRIER_READ_UNKNOWN')
   if write and present~=wanted then
    if wanted then P.CreateBuilding(city:GetBuildQueue(),row.Index) else P.RemoveBuilding(b,row.Index);removed=true end
    assert(P.HasBuilding(b,row.Index)==wanted,'CARRIER_WRITE_UNCONFIRMED')
    data.changes=data.changes+1;present=wanted
   end
   if present then if bit==-1 then food=3 else total=total+2^bit end end
  end
  if removed and n==nil then P.Count('industry_withdraw') end
  return total,food
 end
 function data.Audit(scope)
  if not data.ready or data.busy then P.Count('busy_skip');return end;data.busy=true;batch=SPCRuntimeWork.New(P,shared)
  for pid,player in pairs(Players) do if SPCRuntimeWork.Player(scope,pid) then
   local scanOK,scanError=pcall(function()
    local cities=player:GetCities();if not cities then return end
    for _,city in cities:Members() do P.Count('city_scan');
     local k=pid..':'..city:GetID();local ok,n=pcall(inspect,pid,city)
     local changed,err=true,nil
     if ok then changed,err=pcall(carriers,city,n,true) end -- unreadable sample preserves projection
     data.errors[k]=not ok and tostring(n) or (not changed and tostring(err) or nil)

    end
   end)
   if not scanOK then print('[SPC][B036][SCAN_ERROR] '..tostring(scanError)) end
  end end
  data.busy=false;batch=nil
 end
 data.ReadBase=inspect
 function data.Receive(pid,params)
  if SPCSampleLifecycle.Receive(P,data,'industry',pid,params,true) then
   data.Audit({player=pid})
   if shared.Lv3Support then shared.Lv3Support.Audit({player=pid}) end
  end
 end
 function data.Describe(pid,city)
  local bg=ExposedMembers.SPC_IndustryBackground
  local ok,n=pcall(inspect,pid,city)
  local valid,p,f=pcall(carriers,city,nil,false)
  return 'B036 Industry Lv1 city='..city:GetID()
   ..'\nBASE Production adjacency='..(ok and tostring(n or 'N/A') or 'ERROR '..tostring(n))
   ..'\nPer worker expected='..(ok and n~=nil and ('3F / '..n..'P') or 'NONE')
   ..' carrier='..(valid and (f..'F / '..p..'P') or ('ERROR '..tostring(p)))
   ..'\nbackground='..tostring(bg and bg.state or 'NOT_STARTED')..' pending='..tostring(bg and bg.pending or 0)..' requests='..tostring(bg and bg.requests or 0)
   ..' receive='..tostring(data.receiveErrors and data.receiveErrors[pid] or 'NONE')
   ..'\nchanges='..data.changes..' error='..tostring(data.errors[pid..':'..city:GetID()] or 'NONE')
   ..'\nRead only; verify native specialist yields. Crew projects available from Industry Lv1; project engine behavior requires B044 testing.'
 end
 local function hook(source,name,fn) local e=P.Field(source,name);if e and e.Add then e.Add(fn) end end
 hook(Events,'LoadScreenClose',function() data.ready=true;SPCSampleLifecycle.Reset(data,'industry');data.Audit() end)
 for _,n in ipairs({'PlayerTurnActivated','CityTransfered','DistrictAddedToMap','DistrictRemovedFromMap','DistrictBuildProgressChanged','ImprovementAddedToMap','ImprovementRemovedFromMap','FeatureRemovedFromMap'}) do SPCRuntimeWork.Hook(P,Events,n,data.Audit) end
 for _,n in ipairs({'OnDistrictConstructed','OnBuildingConstructed','CityBuilt'}) do hook(GameEvents,n,data.Audit) end
end
