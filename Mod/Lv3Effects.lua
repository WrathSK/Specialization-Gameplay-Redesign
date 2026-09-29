include('RuntimeWork')
-- B038: native population yield per specialist; Commerce direct connected types.
SPCLv3Effects={}
function SPCLv3Effects.Start(P,shared)
 local batch
 local function readFacts(pid,c) return batch and batch.Facts(pid,c) or shared.EffectiveFacts.Read(pid,c) end
 local function districtsFor(pid,c)
  return (batch or SPCRuntimeWork.New(P,shared)).Districts(pid,c)
 end
 local data={ready=false,busy=false,errors={},changes=0,observed={}};shared.Lv3Effects=data
 local districts={RESEARCH='DISTRICT_CAMPUS',CULTURE='DISTRICT_THEATER',COMMERCE='DISTRICT_COMMERCIAL_HUB',INDUSTRY='DISTRICT_INDUSTRIAL_ZONE'}
 local names={}
 for _,k in ipairs({'CULTURE'}) do for i=0,7 do names[#names+1]='BUILDING_SPC_DEV_LV3_POP_'..k..'_'..i end end
 for _,k in ipairs({'RESEARCH','CULTURE','INDUSTRY'}) do names[#names+1]='BUILDING_SPC_DEV_LV3_COM_'..k end
 local function desired(pid,c)
  local wanted={}
  if c:GetOwner()~=pid or not P.IsTestPlayer(pid) then return wanted end
  local f=readFacts(pid,c)
  if f.specialization=='RESEARCH' then return wanted end -- P0-D1 owns Research III
  if not districts[f.specialization] or type(f.active)~='number' or f.active<3 then return wanted end
  assert(f.first and f.potential>=3,'LV3_FACT_INVALID')
  local found=false
  for _,d in districtsFor(pid,c) do
   local city=d:GetCity();local row=P.Info('Districts',d:GetType())
   if city and city:GetOwner()==pid and city:GetID()==c:GetID() and d:GetID()==f.first.districtID then
    assert(row and row.DistrictType==districts[f.specialization] and f.first.type==row.DistrictType and d:IsComplete()==true,'LV3_ANCHOR_INVALID');found=true;break
   end
  end
  assert(found,'LV3_DISTRICT_MISSING')
  if f.specialization=='CULTURE' then
   local target
   for _,d in districtsFor(pid,c) do
    local city=d:GetCity()
    if city and city:GetOwner()==pid and city:GetID()==c:GetID() and d:GetID()==f.first.districtID then target=d;break end
   end
   local n=Map.GetPlot(target:GetX(),target:GetY()):GetWorkerCount()
   data.observed[pid..':'..c:GetID()]={workers=n,pop=c:GetPopulation(),active=f.active}
   assert(type(n)=='number' and n>=0 and n<=255 and n%1==0,'WORKERS_UNKNOWN_OR_OUT_OF_RANGE')
   for i=0,7 do if math.floor(n/2^i)%2==1 then wanted['BUILDING_SPC_DEV_LV3_POP_'..f.specialization..'_'..i]=true end end
  elseif f.specialization=='COMMERCE' then
   local kinds=(shared.NetworkBridge.CurrentConnectedKinds or shared.NetworkBridge.ConnectedKinds)(pid,c)
   for _,k in ipairs({'RESEARCH','CULTURE','INDUSTRY'}) do if kinds[k] then wanted['BUILDING_SPC_DEV_LV3_COM_'..k]=true end end
  end
  return wanted
 end
 local function read(c)
  local coefficients={RESEARCH=0,CULTURE=0};local flags={}
  for _,name in ipairs(names) do
   local row=P.Info('Buildings',name);assert(row and row.Index,'B038_DATABASE_MISSING')
   if P.HasBuilding(c:GetBuildings(),row.Index) then
    local k,bit=name:match('_POP_(%u+)_(%d+)$')
    if k then coefficients[k]=coefficients[k]+0.5*2^tonumber(bit)
    else flags[#flags+1]=name:match('_COM_(%u+)$') end
   end
  end
  return coefficients,flags
 end
 function data.Audit(scope) P.Count('audit_lv3');
  if P.Observe then P.Observe('audit','Lv3Effects') end
  if not data.ready or data.busy then P.Count('busy_skip');return end;data.busy=true;batch=SPCRuntimeWork.New(P,shared)
  for pid,player in pairs(Players) do if SPCRuntimeWork.Player(scope,pid) then
   local ok,err=pcall(function()
    local cities=player:GetCities();if not cities then return end
    for _,c in cities:Members() do P.Count('city_scan');
     local good,wanted=pcall(desired,pid,c);local reason=not good and tostring(wanted) or nil
     if not good then wanted={} end
     local applied,why=pcall(function()
      -- Remove obsolete carriers before adding current carriers.
      for _,adding in ipairs({false,true}) do for _,name in ipairs(names) do
       local row=P.Info('Buildings',name);assert(row and row.Index,'B038_DATABASE_MISSING')
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
   if not ok then print('[SPC][B038][SCAN_ERROR] '..tostring(err)) end
  end end
  data.busy=false;batch=nil
 end
 function data.Describe(pid,c)
  local ok,out=pcall(function()
   local coef,flags=read(c);local pop=c:GetPopulation()
   local f=readFacts(pid,c)
   if f.specialization=='RESEARCH' then return shared.ResearchCross and shared.ResearchCross.Describe(pid,c) or '跨学科研究尚未初始化' end
   local lines={}
   if f.specialization=='CULTURE' then
    local workers
    for _,d in districtsFor(pid,c) do
     local city=d:GetCity()
     if f.first and city and city:GetOwner()==pid and city:GetID()==c:GetID() and d:GetID()==f.first.districtID then
      workers=Map.GetPlot(d:GetX(),d:GetY()):GetWorkerCount();break
     end
    end
    local valid=type(workers)=='number' and workers>=0 and workers%1==0
    local enabled=type(f.active)=='number' and f.active>=3
    local expected=valid and (enabled and 0.5*pop*workers or 0) or 'UNKNOWN'
    local last=data.observed[pid..':'..c:GetID()]
    local row=P.Info('Yields',f.specialization=='RESEARCH' and 'YIELD_SCIENCE' or 'YIELD_CULTURE')
    local got,total=pcall(function() return c:GetYield(row.Index) end)
    if not got or type(total)~='number' then total='UNKNOWN' end
    lines[#lines+1]='Population support: ACTIVE='..tostring(f.active)..' pop='..pop..' live workers='..tostring(workers or 'UNKNOWN')
    lines[#lines+1]='Base bonus expected='..expected..' carrier='..coef[f.specialization]*pop..' (not measured effect)'
    lines[#lines+1]='Last audit workers='..tostring(last and last.workers or 'NONE')..' native city total='..tostring(total)
   else
    lines[#lines+1]='Commerce specialist +2 per type: '..(#flags>0 and table.concat(flags,',') or 'NONE')
   end
   return '\n'..table.concat(lines,'\n')

  end)
  return (ok and out or ('\nLv3 effects ERROR '..tostring(out)))..'\nLv3 effects status: '..tostring(data.errors[pid..':'..c:GetID()] or (data.ready and 'READY' or 'PENDING'))
 end
 local function hook(source,n,fn) local e=P.Field(source,n);if e and e.Add then e.Add(fn) end end
 hook(Events,'LoadScreenClose',function() data.ready=true;data.Audit() end)
 for _,n in ipairs({'PlayerTurnActivated','GovernorAssigned','GovernorChanged','GovernorEstablished','GovernorPromoted','CityTransfered','CityWorkerChanged','CityFocusChanged','CityPopulationChanged'}) do SPCRuntimeWork.Hook(P,Events,n,data.Audit) end
 for _,n in ipairs({'OnDistrictConstructed','OnBuildingConstructed','CityBuilt'}) do hook(GameEvents,n,data.Audit) end
 -- E2 confirmed exit: exact transient IDs owned by this writer; no prefix scan.
 if shared.CityProgressionStore then shared.CityProgressionStore.RegisterExit('Lv3Effects',function(c,loss)
   local ids={};for _,id in ipairs(names)do ids[#ids+1]=id end
   shared.CityProgressionStore.RemoveOwned(c,loss,ids)
 end)end

end
