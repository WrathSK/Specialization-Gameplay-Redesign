include('RuntimeWork')
-- B048: only RES-004/CUL-004 per-specialist percentage component.
SPCLv4Percent={}
function SPCLv4Percent.Start(P,shared)
 local batch
 local function readFacts(pid,c) return batch and batch.Facts(pid,c) or shared.EffectiveFacts.Read(pid,c) end
 local function districtsFor(pid,c)
  return (batch or SPCRuntimeWork.New(P,shared)).Districts(pid,c)
 end
 local data={ready=false,busy=false,errors={},changes=0};shared.Lv4Percent=data
 local districts={CULTURE='DISTRICT_THEATER'}
 local function name(k,i) return 'BUILDING_SPC_LV4_PERCENT_'..k..'_'..i end
 local function facts(pid,c)
  if not P.IsTestPlayer(pid) or c:GetOwner()~=pid then return nil,0,nil end
  local f=readFacts(pid,c);local kind=f.specialization
  if not districts[kind] then return nil,0,f.active end
  assert(f.first and f.potential>=1 and (f.active~=4 or f.potential==4),'LV4_FACT_INVALID')
  for _,d in districtsFor(pid,c) do
   local dc=d:GetCity()
   if dc and dc:GetOwner()==pid and dc:GetID()==c:GetID() and d:GetID()==f.first.districtID then
    local row=P.Info('Districts',d:GetType())
    assert(row and row.DistrictType==districts[kind] and f.first.type==row.DistrictType and d:IsComplete()==true,'LV4_ANCHOR_INVALID')
    local n=Map.GetPlot(d:GetX(),d:GetY()):GetWorkerCount()
    assert(type(n)=='number' and n>=0 and n<=255 and n%1==0,'LV4_WORKERS_UNKNOWN')
    return kind,f.active==4 and n or 0,f.active,n
   end
  end
  error('LV4_DISTRICT_MISSING')
 end
 function data.Audit(scope)
  if not data.ready or data.busy then P.Count('busy_skip');return end;data.busy=true;batch=SPCRuntimeWork.New(P,shared)
  for pid,player in pairs(Players) do if SPCRuntimeWork.Player(scope,pid) then
   local scanned,err=pcall(function()
    local cities=player:GetCities();if not cities then return end
    for _,c in cities:Members() do P.Count('city_scan');
     local ok,kind,n=pcall(facts,pid,c);local reason=not ok and tostring(kind) or nil
     if not ok then kind=nil;n=0 end
     local changed,why=pcall(function()
      for _,adding in ipairs({false,true}) do
       for _,k in ipairs({'CULTURE'}) do for i=0,7 do
        local row=P.Info('Buildings',name(k,i));assert(row and row.Index,'B048_DATABASE_MISSING')
        local want=kind==k and math.floor(n/2^i)%2==1
        if want==adding then
         local b=c:GetBuildings();local present=P.HasBuilding(b,row.Index);assert(type(present)=='boolean','LV4_CARRIER_UNKNOWN')
         if present~=want then
          if want then P.CreateBuilding(c:GetBuildQueue(),row.Index) else P.RemoveBuilding(b,row.Index) end
          assert(P.HasBuilding(b,row.Index)==want,'LV4_WRITE_UNCONFIRMED');data.changes=data.changes+1
         end
        end
       end end
      end
     end)
     data.errors[pid..':'..c:GetID()]=reason or (not changed and tostring(why) or nil)
    end
   end)
   if not scanned then print('[SPC][B048][ERROR] '..tostring(err)) end
  end end
  data.busy=false;batch=nil
 end
 function data.Describe(pid,c)
  local ok,out=pcall(function()
   local kind,n,active,workers=facts(pid,c);shared.Lv4PercentRead={owner=pid,cityID=c:GetID(),kind=kind};local science,culture=0,0
   for _,k in ipairs({'CULTURE'}) do for i=0,7 do
    local row=P.Info('Buildings',name(k,i));assert(row and row.Index,'B048_DATABASE_MISSING')
    if P.HasBuilding(c:GetBuildings(),row.Index) then
     if k=='RESEARCH' then science=science+5*2^i else culture=culture+5*2^i end
    end
   end end
   return 'Lv4专家百分比 | city='..c:GetID()..' | '..tostring(kind or '非科研/文化')
    ..'\nACTIVE='..tostring(active)..' | 实际专家='..tostring(workers or 0)..' | 生效计数='..n..' | 预期本项加成='..(n*5)..'个百分点'
    ..'\n当前载体：科技 +'..science..'% / 文化 +'..culture..'%（配置，不是实测增量）'
    ..'\n状态='..tostring(data.errors[pid..':'..c:GetID()] or (data.ready and 'READY' or 'PENDING'))
    ..'\n请核对原生城市产出明细；不包含Lv4相邻复制/巨作效果。'
  end)
  return ok and out or ('Lv4百分比读取失败：'..tostring(out))
 end
 local function hook(src,n,fn) local e=P.Field(src,n);if e and e.Add then e.Add(fn) end end
 hook(Events,'LoadScreenClose',function() data.ready=true;data.Audit() end)
 for _,n in ipairs({'PlayerTurnActivated','GovernorAssigned','GovernorChanged','GovernorEstablished','GovernorPromoted','CityTransfered','CityWorkerChanged','CityFocusChanged','CityPopulationChanged','DistrictRemovedFromMap'}) do SPCRuntimeWork.Hook(P,Events,n,data.Audit) end
 for _,n in ipairs({'OnDistrictConstructed','OnBuildingConstructed','CityBuilt'}) do hook(GameEvents,n,data.Audit) end
end
