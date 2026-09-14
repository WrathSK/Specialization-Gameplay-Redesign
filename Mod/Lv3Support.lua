-- B037: Lv3 specialist support only. Incremental +2 upgrades Lv1 3 to 5, never 3+5.
SPCLv3Support={}
function SPCLv3Support.Start(P,shared)
 local data={ready=false,busy=false,errors={},changes=0};shared.Lv3Support=data
 local districts={RESEARCH='DISTRICT_CAMPUS',CULTURE='DISTRICT_THEATER',COMMERCE='DISTRICT_COMMERCIAL_HUB',INDUSTRY='DISTRICT_INDUSTRIAL_ZONE'}
 local names={};for k in pairs(districts) do names[#names+1]='BUILDING_SPC_DEV_LV3_'..k end
 for i=0,7 do names[#names+1]='BUILDING_SPC_DEV_LV3_INDUSTRY_GOLD_'..i end
 local function desired(pid,c)
  local wanted={}
  if c:GetOwner()~=pid or not P.IsTestPlayer(pid) then return wanted end
  local f=shared.EffectiveFacts.Read(pid,c)
  if not districts[f.specialization] or type(f.active)~='number' or f.active<3 then return wanted end
  assert(f.first and f.potential>=3,'LV3_FACT_INVALID')
  local found=false
  for _,d in Players[pid]:GetDistricts():Members() do P.Count('district_scan');
   local city=d:GetCity();local row=P.Info('Districts',d:GetType())
   if city and city:GetOwner()==pid and city:GetID()==c:GetID() and d:GetID()==f.first.districtID then
    assert(row and row.DistrictType==districts[f.specialization] and f.first.type==row.DistrictType and d:IsComplete()==true,'LV3_ANCHOR_INVALID');found=true;break
   end
  end
  assert(found,'LV3_DISTRICT_MISSING')
  wanted['BUILDING_SPC_DEV_LV3_'..f.specialization]=true
  if f.specialization=='INDUSTRY' then
   local base=shared.IndustrySupport.ReadBase(pid,c)
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
 function data.Audit() P.Count('audit_lv3');
  if not data.ready or data.busy then P.Count('busy_skip');return end;data.busy=true
  for pid,player in pairs(Players) do
   local ok,err=pcall(function()
    local cities=player:GetCities();if not cities then return end
    for _,c in cities:Members() do P.Count('city_scan');
     local good,wanted=pcall(desired,pid,c);local reason=not good and tostring(wanted) or nil
     if not good then wanted={} end
     local applied,why=pcall(function()
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
  end
  data.busy=false
 end
 function data.Describe(pid,c)
  local ok,f,p,g=pcall(read,c)
  return '\nLv3 top-up carrier (added to Lv1): '..(ok and (f..'F / '..p..'P / '..g..'G') or ('ERROR '..tostring(f)))
   ..'\nLv3 status: '..tostring(data.errors[pid..':'..c:GetID()] or (data.ready and 'READY' or 'PENDING'))
 end
 local function hook(source,n,fn) local e=P.Field(source,n);if e and e.Add then e.Add(fn) end end
 hook(Events,'LoadScreenClose',function() data.ready=true;data.Audit() end)
 for _,n in ipairs({'PlayerTurnActivated','PlayerTurnDeactivated','GovernorAssigned','GovernorChanged','GovernorEstablished','GovernorPromoted','CityTransfered'}) do hook(Events,n,data.Audit) end
 for _,n in ipairs({'OnDistrictConstructed','OnBuildingConstructed','CityBuilt'}) do hook(GameEvents,n,data.Audit) end
end
