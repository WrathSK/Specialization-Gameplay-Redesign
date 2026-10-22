include('RuntimeWork')
-- B037: Lv3 specialist support only. Incremental +2 upgrades Lv1 3 to 5, never 3+5.
SPCLv3Support={}
local function historicalStart(P,shared)
 local batch
 local function readFacts(pid,c) return batch and batch.Facts(pid,c) or shared.EffectiveFacts.Read(pid,c) end
 local function districtsFor(pid,c)
  return (batch or SPCRuntimeWork.New(P,shared)).Districts(pid,c)
 end
 local data={ready=false,busy=false,errors={},changes=0};shared.Lv3Support=data
 local districts={RESEARCH='DISTRICT_CAMPUS',CULTURE='DISTRICT_THEATER',COMMERCE='DISTRICT_COMMERCIAL_HUB',INDUSTRY='DISTRICT_INDUSTRIAL_ZONE'}
 local names={};for k in pairs(districts) do names[#names+1]='BUILDING_SPC_DEV_LV3_'..k end
 for i=0,7 do names[#names+1]='BUILDING_SPC_DEV_LV3_INDUSTRY_GOLD_'..i end
 local function desired(pid,c)
  local wanted={}
  if c:GetOwner()~=pid or not P.IsTestPlayer(pid) then return wanted end
  local f=readFacts(pid,c)
  if not districts[f.specialization] or type(f.active)~='number' or f.active<3 then return wanted end
  assert(f.first and f.potential>=3,'LV3_FACT_INVALID')
  local found=false
  for _,d in districtsFor(pid,c) do
   local city=d:GetCity();local row=P.Info('Districts',d:GetType())
   if f.specialization=='INDUSTRY' then assert(city,'INDUSTRY_SAMPLE_UNAVAILABLE') end
   if city and city:GetOwner()==pid and city:GetID()==c:GetID() and d:GetID()==f.first.districtID then
    if f.specialization=='INDUSTRY' then assert(row and type(d:IsComplete())=='boolean','INDUSTRY_SAMPLE_UNAVAILABLE') end
    assert(row and row.DistrictType==districts[f.specialization] and f.first.type==row.DistrictType and d:IsComplete()==true,'LV3_ANCHOR_INVALID');found=true;break
   end
  end
  assert(found,'LV3_DISTRICT_MISSING')
  wanted['BUILDING_SPC_DEV_LV3_'..f.specialization]=true
  if f.specialization=='INDUSTRY' then
   local readable,base=pcall(shared.IndustrySupport.ReadBase,pid,c,batch)
   assert(readable,'INDUSTRY_SAMPLE_UNAVAILABLE')
   if base==nil then return {} end
   assert(type(base)=='number' and base>=0 and base<=255 and base%1==0,'LV3_BASE_UNKNOWN')
   for i=0,7 do if math.floor(base/2^i)%2==1 then wanted['BUILDING_SPC_DEV_LV3_INDUSTRY_GOLD_'..i]=true end end
  end
  return wanted
 end
 local function read(c)
  local f,p,g=0,0,0
  for _,name in ipairs(names) do
   local row=P.Info('Buildings',name);assert(row and row.Index,'B037_DATABASE_MISSING')
   if P.HasBuilding(c:GetBuildings(),row.Index) then
    local bit=name:match('_GOLD_(%d+)$')
    if bit then g=g+2*2^tonumber(bit) else f=f+2;if name~='BUILDING_SPC_DEV_LV3_INDUSTRY' then p=p+2 end end
   end
  end
  return f,p,g
 end
 function data.Audit(scope) P.Count('audit_lv3');
  if not data.ready or data.busy then P.Count('busy_skip');return end;data.busy=true;batch=SPCRuntimeWork.New(P,shared)
  for pid,player in pairs(Players) do if SPCRuntimeWork.Player(scope,pid) then
   local ok,err=pcall(function()
    local cities=player:GetCities();if not cities then return end
    for _,c in cities:Members() do P.Count('city_scan');
     local good,wanted=pcall(desired,pid,c);local reason=not good and tostring(wanted) or nil
     local hold=reason and (reason:find('BASE_BACKGROUND_SAMPLE_PENDING',1,true) or reason:find('INDUSTRY_FACT_INVALID',1,true) or reason:find('INDUSTRY_SAMPLE_UNAVAILABLE',1,true) or reason:find('SAMPLE_CITY_UNAVAILABLE',1,true))
     if not good then wanted={} end
     local applied,why=pcall(function()
      if hold then return end
      -- Remove obsolete carriers before adding current carriers.
      for _,adding in ipairs({false,true}) do for _,name in ipairs(names) do
       local row=P.Info('Buildings',name);assert(row and row.Index,'B037_DATABASE_MISSING')
       local want=wanted[name]==true
       if want==adding then
        local b=c:GetBuildings();local present=P.HasBuilding(b,row.Index);assert(type(present)=='boolean','LV3_CARRIER_UNKNOWN')
        if present~=want then
         if want then P.CreateBuilding(c:GetBuildQueue(),row.Index) else P.RemoveBuilding(b,row.Index) end
         assert(P.HasBuilding(b,row.Index)==want,'LV3_WRITE_UNCONFIRMED');data.changes=data.changes+1
        end
       end
      end end
     end)
     data.errors[pid..':'..c:GetID()]=reason or (not applied and tostring(why) or nil)
    end
   end)
   if not ok then print('[SPC][B037][SCAN_ERROR] '..tostring(err)) end
  end end
  data.busy=false;batch=nil
 end
 function data.Describe(pid,c)
  local ok,f,p,g=pcall(read,c)
  return '\nLv3 top-up carrier (added to Lv1): '..(ok and (f..'F / '..p..'P / '..g..'G') or ('ERROR '..tostring(f)))
   ..'\nLv3 status: '..tostring(data.errors[pid..':'..c:GetID()] or (data.ready and 'READY' or 'PENDING'))
 end
 local function hook(source,n,fn) local e=P.Field(source,n);if e and e.Add then e.Add(fn) end end
 hook(Events,'LoadScreenClose',function() data.ready=true;data.Audit() end)
 for _,n in ipairs({'PlayerTurnActivated','GovernorAssigned','GovernorChanged','GovernorEstablished','GovernorPromoted','CityTransfered','DistrictRemovedFromMap','DistrictBuildProgressChanged'}) do SPCRuntimeWork.Hook(P,Events,n,data.Audit) end
 for _,n in ipairs({'OnDistrictConstructed','OnBuildingConstructed','CityBuilt'}) do hook(GameEvents,n,data.Audit) end
end

-- P0-B1 permanent code gate: historicalStart is intentionally unreachable.
-- Exact tombstone IDs remain in DB, with no CitizenYieldChanges.
include('SpecialistSupport')
function SPCLv3Support.Start(P,shared)
 local data={ready=false,busy=false,errors={},changes=0,ruleset='RETIRED_D0032_P0B1'};shared.Lv3Support=data
 function data.Audit(scope)
  if not data.ready or data.busy then return end
  data.busy=true
  for pid,p in pairs(Players) do if SPCRuntimeWork.Player(scope,pid) then
   local ok,err=pcall(function()
    for _,c in p:GetCities():Members() do
     P.Count('city_scan');local good,n=pcall(SPCSpecialistSupport.Retire,P,c)
     data.errors[pid..':'..c:GetID()]=not good and tostring(n) or nil
     if good then data.changes=data.changes+n end
    end
   end)
   data.errors['player:'..pid]=not ok and tostring(err) or nil
  end end
  data.busy=false
 end
 function data.Describe(pid,c)
  return '\n旧三级专家升级：RETIRED（额外2F/2P、工业Gold不再生效）'
   ..'\nretiredRemoved='..data.changes..' error='..tostring(data.errors[pid..':'..c:GetID()] or 'NONE')
 end
 local e=P.Field(Events,'LoadScreenClose');if e and e.Add then e.Add(function() data.ready=true;data.Audit() end) end
 SPCRuntimeWork.Hook(P,Events,'CityTransfered',data.Audit)
 -- E2 confirmed exit: exact transient IDs owned by this writer; no prefix scan.
 if shared.CityProgressionStore then shared.CityProgressionStore.RegisterExit('Lv3Support',function(c,loss)
   local ids={};for _,id in ipairs(SPCSpecialistSupport.Retired)do ids[#ids+1]=id end
   shared.CityProgressionStore.RemoveOwned(c,loss,ids)
 end)end

end
