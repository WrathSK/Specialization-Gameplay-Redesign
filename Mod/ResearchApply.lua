include('RuntimeWork')
include('ResearchApplyModel')
-- Sole RES_L3_APPLY writer. Native Campus specialist yield, never city flat compensation.
SPCResearchApply={}
local M=SPCResearchApply
M.Bits=5 -- max current Gold coefficient30; rejects overflow, never clamps
local function name(y,i) return 'BUILDING_SPC_RESEARCH_APPLY_'..y..'_'..i end
function M.Start(P,shared)
 local data={ready=false,busy=false,errors={},changes=0};shared.ResearchApply=data
 local definitions
 local function validate()
  if definitions then return end
  local rows=assert(P.Rows('Building_CitizenYieldChanges'),'AP_DATABASE_UNKNOWN')
  for _,y in ipairs(SPCResearchApplyModel.Yields) do for i=0,M.Bits-1 do
   local r=assert(P.Info('Buildings',name(y,i)),'AP_BUILDING_MISSING')
   assert(r.PrereqDistrict=='DISTRICT_CAMPUS' and r.CitizenSlots==0 and r.Housing==0,'AP_BUILDING_MISMATCH')
   local n=0;for _,v in ipairs(rows) do if v.BuildingType==name(y,i) then
    assert(v.YieldType=='YIELD_'..y and v.YieldChange==2^i,'AP_YIELD_MISMATCH');n=n+1
   end end;assert(n==1,'AP_YIELD_MISSING')
  end end;definitions=true
 end
 local function inspect(pid,c)
  local f=SPCCurrentSpecializationFacts.Read(P,shared,pid,c)
  local inactive=SPCResearchApplyModel.Plan(f,nil,nil)
  if inactive.status~='NEEDS_DEPTH' then return inactive end
  local v=shared.DistrictCompleteness.Read(pid,c,f.token)
  assert(v.validity=='VERIFIED' and v.availability=='READY' and v.value,'AP_DEPTH_UNKNOWN')
  local campus,n=nil,0;local warnings={}
  for _,d in ipairs(v.value.districts) do
   if d.domain=='DISTRICT_CAMPUS' then campus=d;n=n+1 end
   for _,b in ipairs(d.buildings) do
    assert(not (b.ordinary and b.depthEligible~=false and b.complete and not b.pillaged and (b.tier==nil or b.reason=='BUILDING_LOCATION_DOMAIN_CONFLICT')),'AP_BUILDING_FACT_UNKNOWN')
    if b.reason=='UNREVIEWED_BUILDING' then warnings[#warnings+1]=b.name or b.type end
   end
  end
  assert(n<=1,'AP_MULTIPLE_CAMPUSES')
  if not campus or not campus.complete or campus.pillaged then
   local p=SPCResearchApplyModel.Plan({validity='VERIFIED',identity='NONE'},nil,nil);p.reason='学院不可用';return p
  end
  assert(f.first and f.first.districtID==campus.id and f.first.type==campus.type,'AP_REFERENCE_UNKNOWN')
  local workers=assert(Map.GetPlotByIndex(campus.plot),'AP_PLOT_UNKNOWN'):GetWorkerCount()
  local p=SPCResearchApplyModel.Plan(f,v,workers)
  p.depth=v;p.plot=campus.plot;p.district=campus.id;p.active=f.active;p.warnings=warnings
  for _,y in ipairs(SPCResearchApplyModel.Yields) do assert(p.per[y]>=0 and p.per[y]<2^M.Bits,'AP_ENCODING_RANGE') end
  return p
 end
 local function installed(c)
  local b=c:GetBuildings();local rows={};local amounts={}
  for _,y in ipairs(SPCResearchApplyModel.Yields) do amounts[y]=0
   for i=0,M.Bits-1 do
    local id=assert(P.Info('Buildings',name(y,i)),'AP_BUILDING_MISSING').Index
    local yes=P.HasBuilding(b,id);assert(type(yes)=='boolean','AP_CARRIER_UNKNOWN')
    local row={id=id,yes=yes,y=y,bit=i}
    if yes then row.plot=b:GetBuildingLocation(id);row.pillaged=b:IsPillaged(id)
     assert(type(row.plot)=='number' and row.plot>=0 and type(row.pillaged)=='boolean','AP_CARRIER_LOCATION_UNKNOWN')
     if not row.pillaged then amounts[y]=amounts[y]+2^i end
    end
    rows[#rows+1]=row
   end
  end
  return rows,amounts
 end
 local function remove(c,row)
  P.RemoveBuilding(c:GetBuildings(),row.id);assert(P.HasBuilding(c:GetBuildings(),row.id)==false,'AP_REMOVE_FAILED');row.yes=false;data.changes=data.changes+1
 end
 local function reconcile(pid,c)
  local p=inspect(pid,c);local rows=installed(c)
  for _,v in ipairs(rows) do
   v.want=math.floor(p.per[v.y]/2^v.bit)%2==1
   if v.yes and (not v.want or v.plot~=p.plot or v.pillaged) then remove(c,v) end
  end
  for _,v in ipairs(rows) do if v.want and not v.yes then
   P.CreateBuilding(c:GetBuildQueue(),v.id)
   local b=c:GetBuildings();assert(P.HasBuilding(b,v.id)==true and b:GetBuildingLocation(v.id)==p.plot and b:IsPillaged(v.id)==false,'AP_CREATE_LOCATION_FAILED');data.changes=data.changes+1
  end end
 end
 function data.Audit(scope)
  if P.Observe then P.Observe('audit','ResearchApply') end
  if not data.ready or data.busy then return end
  data.busy=true
  local ok,err=pcall(function()
   validate();data.definitionError=nil
   for pid,player in pairs(Players) do if SPCRuntimeWork.Player(scope,pid) and P.IsTestPlayer(pid) then
    data.errors[pid]={};local cities=player:GetCities()
    if cities then for _,c in cities:Members() do
     P.Count('city_scan');local good,why=pcall(reconcile,pid,c)
     if not good then data.errors[pid][c:GetID()]=tostring(why) end
    end end
   end end
  end)
  if not ok then data.definitionError=tostring(err) end
  data.busy=false
 end
 function data.Describe(pid,c,detail)
  local ok,text=pcall(function()
   assert(data.ready,'AP_NOT_READY');validate()
   local p=inspect(pid,c);local rows,coeff=installed(c)
   local lines={'学以致用 | '..(p.status=='READY' and ('ACTIVE '..p.active..'；工作科研专家 '..p.workers) or '未生效'),
    '同产出领域先合并 → 每名floor → 按工作专家结算。'}
   for _,y in ipairs(SPCResearchApplyModel.Yields) do
    if p.per[y]~=0 or coeff[y]~=0 or (p.raw[y] or 0)~=0 then
     lines[#lines+1]=SPCResearchApplyModel.Labels[y]..'：每名 '..(p.raw[y] or 0)..' → '..p.per[y]..'；全城预期 +'..p.total[y]..'；每名配置 '..coeff[y]
    end
   end
   local err=data.definitionError or data.errors[pid] and data.errors[pid][c:GetID()]
   if err then lines[#lines+1]='待确认：'..(err:match('AP_[A-Z_]+') or '接口错误') end
   if p.warnings and #p.warnings>0 then
    local a={};for _,x in ipairs(p.warnings) do a[#a+1]=Locale.Lookup(x) end
    lines[#lines+1]='未审建筑已排除：'..table.concat(a,'、')..'；目录覆盖非全环境PASS。'
   end
   lines[#lines+1]='配置/预期不是原生实测；不包含基础3食物3生产力及其它能力。'
   if detail and p.depth then
    for _,v in ipairs(p.rows) do if v.district then
     lines[#lines+1]=v.label..' D'..v.d..' → '..v.shares..'份 → 原值每人+'..v.amount..SPCResearchApplyModel.Labels[v.yield]
     for _,d in ipairs(p.depth.value.districts) do if d.id==v.district then
      lines[#lines+1]='  选中区域#'..d.id..'；cap前 '..d.uncapped..' → '..d.value
      for _,b in ipairs(d.buildings) do if not b.type:match('^BUILDING_SPC_') then
       lines[#lines+1]='  '..Locale.Lookup(b.name or b.type)..'：Tier '..tostring(b.tier)..'，贡献 '..b.contribution..(b.pillaged and '（已掠夺）' or '')
      end end
     end end
    end end
   end
   return table.concat(lines,'\n')
  end)
  return ok and text or ('学以致用：暂不可确认，保留上次配置。\n'..(tostring(text):match('AP_[A-Z_]+') or '接口未就绪'))
 end
 local function bind(src,n,f) local e=P.Field(src,n);if e and e.Add then e.Add(f) end end
 bind(Events,'LoadScreenClose',function() definitions=nil;data.ready=true;data.errors={};data.Audit() end)
 -- Shared D/P0-C registers first and owns depth invalidation. Do not re-dirty a
 -- fresh snapshot here: both consumers reuse it during the same native event.
 for _,n in ipairs({'BuildingAddedToMap','BuildingRemovedFromMap','BuildingPillaged','BuildingRepaired',
  'DistrictRemovedFromMap','DistrictBuildProgressChanged','DistrictPillaged','DistrictRepaired','CityTransfered','CityRemovedFromMap',
  'CityWorkerChanged','CityFocusChanged','GovernorAssigned','GovernorEstablished','GovernorChanged','GovernorPromoted','PlayerTurnActivated'}) do
  SPCRuntimeWork.Hook(P,Events,n,data.Audit)
 end
 for _,n in ipairs({'OnDistrictConstructed','BuildingConstructed','CityBuilt','OnPillage'}) do bind(GameEvents,n,data.Audit) end
 -- E2 confirmed exit: exact transient IDs owned by this writer; no prefix scan.
 if shared.CityProgressionStore then shared.CityProgressionStore.RegisterExit('ResearchApply',function(c,loss)
   local ids={};for _,y in ipairs(SPCResearchApplyModel.Yields)do for bit=0,M.Bits-1 do ids[#ids+1]=name(y,bit)end end
   shared.CityProgressionStore.RemoveOwned(c,loss,ids)
 end)end

end
