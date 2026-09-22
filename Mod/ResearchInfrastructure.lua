include('RuntimeWork')
-- P0-C RES_L4_INFRA. One Campus per city (user-confirmed environment).
-- Shared D remains highest-single-district; unexpected multiple Campuses HOLD.
SPCResearchInfrastructure={}
local M=SPCResearchInfrastructure
M.Retired={}
for i=0,7 do M.Retired[#M.Retired+1]='BUILDING_SPC_LV4_PERCENT_RESEARCH_'..i end
for _,mode in ipairs({'POS','NEG','POP'}) do for i=0,(mode=='POP' and 7 or 15) do
 M.Retired[#M.Retired+1]='BUILDING_SPC_B051_SCIENCE_'..mode..'_'..i
end end
local function name(i) return 'BUILDING_SPC_RESEARCH_INFRA_'..i end
local function integer(n) return type(n)=='number' and n>=0 and n<math.huge and n%1==0 end
function M.Start(P,shared)
 local data={ready=false,busy=false,errors={},changes=0};shared.ResearchInfrastructure=data
 local definitions
 local function validate()
  if definitions then return end
  local rows=assert(P.Rows('Building_CitizenYieldChanges'),'RI_DATABASE_UNAVAILABLE')
  for i=0,3 do
   local r=assert(P.Info('Buildings',name(i)),'RI_BUILDING_MISSING')
   assert(r.PrereqDistrict=='DISTRICT_CAMPUS' and r.CitizenSlots==0 and r.Housing==0,'RI_BUILDING_MISMATCH')
   local found=0
   for _,v in ipairs(rows) do if v.BuildingType==name(i) then
    assert(v.YieldType=='YIELD_SCIENCE' and v.YieldChange==2^i,'RI_YIELD_MISMATCH');found=found+1
   end end
   assert(found==1,'RI_YIELD_MISSING')
  end
  for _,n in ipairs(M.Retired) do assert(P.Info('Buildings',n),'RI_TOMBSTONE_MISSING') end
  definitions=true
 end
 local function inspect(pid,c)
  if c:GetOwner()~=pid or not P.IsTestPlayer(pid) then return {d=0,workers=0,science=0,status='INACTIVE'} end
  local f=SPCCurrentSpecializationFacts.Read(P,shared,pid,c)
  assert(f.validity=='VERIFIED' and type(f.identity)=='string','RI_FACTS_UNKNOWN')
  local p={identity=f.identity,potential=f.potential,active=f.active,d=0,workers=0,science=0,status='INACTIVE'}
  if f.identity~='RESEARCH' then return p end
  assert(integer(f.active) and f.active<=4 and integer(f.potential) and f.potential<=4 and f.active<=f.potential,'RI_ACTIVE_UNKNOWN')
  if f.active<4 then return p end
  local v=shared.DistrictCompleteness.Read(pid,c,f.token)
  assert(v.validity=='VERIFIED' and v.availability=='READY' and v.value,'RI_DEPTH_UNAVAILABLE')
  p.depth=v
  local count=0;local campus
  for _,r in ipairs(v.value.districts) do if r.domain=='DISTRICT_CAMPUS' then
   count=count+1;campus=r
  end end
  assert(count<=1,'RI_MULTIPLE_CAMPUSES_UNSUPPORTED_ENVIRONMENT')
  if not campus or not campus.complete or campus.pillaged then return p end
  assert(f.first and f.first.districtID==campus.id and f.first.type==campus.type,'RI_CURRENT_REFERENCE_UNKNOWN')
  for _,b in ipairs(campus.buildings) do
   assert(not (b.ordinary and b.complete and not b.pillaged and (b.tier==nil or b.reason=='BUILDING_LOCATION_DOMAIN_CONFLICT')),'RI_ORDINARY_TIER_UNKNOWN')
  end
  local input=SPCResearchInfrastructureShadow.WithWorkers(f,v)
  local plan=SPCResearchInfrastructureShadow.Plan(input,v)
  assert(plan.status=='READY' and integer(plan.d) and plan.d<=10 and integer(plan.workers),'RI_WORKERS_OR_DEPTH_UNKNOWN')
  p.status='READY';p.d=plan.d;p.workers=plan.workers;p.science=plan.science;p.plot=campus.plot;p.district=campus.id
  return p
 end
 local function installed(c)
  local b=c:GetBuildings();local out={old={},bits={},oldCount=0,coefficient=0}
  for _,n in ipairs(M.Retired) do
   local id=P.Info('Buildings',n).Index;local yes=P.HasBuilding(b,id)
   assert(type(yes)=='boolean','RI_CARRIER_READ_UNKNOWN');out.old[#out.old+1]={id=id,yes=yes}
   if yes then out.oldCount=out.oldCount+1 end
  end
  for i=0,3 do
   local id=P.Info('Buildings',name(i)).Index;local yes=P.HasBuilding(b,id)
   assert(type(yes)=='boolean','RI_CARRIER_READ_UNKNOWN')
   local r={id=id,yes=yes}
   if yes then
    r.plot=b:GetBuildingLocation(id);r.pillaged=b:IsPillaged(id)
    assert(type(r.plot)=='number' and r.plot>=0 and type(r.pillaged)=='boolean','RI_CARRIER_LOCATION_UNKNOWN')
    if not r.pillaged then out.coefficient=out.coefficient+2^i end
   end
   out.bits[i]=r
  end
  return out
 end
 local function remove(c,id)
  P.RemoveBuilding(c:GetBuildings(),id)
  assert(P.HasBuilding(c:GetBuildings(),id)==false,'RI_REMOVE_UNCONFIRMED');data.changes=data.changes+1
 end
 local function reconcile(pid,c)
  validate()
  local p=inspect(pid,c);local state=installed(c) -- complete read before any writes
  -- Old definitions are inert SQL tombstones; this is their sole cleanup owner.
  for _,r in ipairs(state.old) do if r.yes then remove(c,r.id) end end
  local amount=p.workers>0 and p.d or 0
  for i=0,3 do
   local r=state.bits[i];local wanted=math.floor(amount/2^i)%2==1
   if r.yes and (not wanted or r.plot~=p.plot or r.pillaged) then remove(c,r.id);r.yes=false end
  end
  for i=0,3 do
   local r=state.bits[i]
   if math.floor(amount/2^i)%2==1 and not r.yes then
    P.CreateBuilding(c:GetBuildQueue(),r.id)
    local b=c:GetBuildings()
    assert(P.HasBuilding(b,r.id)==true and b:GetBuildingLocation(r.id)==p.plot and b:IsPillaged(r.id)==false,'RI_CREATE_UNCONFIRMED')
    data.changes=data.changes+1
   end
  end
 end
 function data.Audit(scope)
  if not data.ready or data.busy then return end
  data.busy=true
  for pid,player in pairs(Players) do if SPCRuntimeWork.Player(scope,pid) then
   data.errors[pid]={}
   local ok,err=pcall(function()
    local cities=player:GetCities();if not cities then return end
    for _,c in cities:Members() do
     P.Count('city_scan');local good,why=pcall(reconcile,pid,c)
     if not good then data.errors[pid][c:GetID()]=tostring(why) end
    end
   end)
   if not ok then data.errors[pid].player=tostring(err) end
  end end
  data.busy=false
 end
 function data.Describe(pid,c,detail)
  local ok,text=pcall(function()
   assert(data.ready,'RI_NOT_READY');validate()
   local p=inspect(pid,c);local s=installed(c)
   local lines={P.VERSION..' | 科研基础设施',
    '科研资格：'..(p.status=='READY' and '满足' or '未生效')..' | Potential='..tostring(p.potential)..' / ACTIVE='..tostring(p.active),
    p.status=='READY' and ('基础设施深度 D='..p.d..'；工作科研专家='..p.workers) or '本项未生效；学院实际D组成可右键查看。',
    '预期新增基础科技：'..p.science..'（每名 +'..p.d..'）',
    '载体配置：每名 +'..s.coefficient..'；旧科研四残留：'..s.oldCount}
   local err=data.errors[pid] and (data.errors[pid][c:GetID()] or data.errors[pid].player)
   lines[#lines+1]=err and ('待处理：'..err) or '配置不是原生实测；请对照城市科技明细。'
   if c:GetProperty('SPC_B050_HALF_ENABLED') then lines[#lines+1]='注意：半点实验仍开启，不能将混合产出作为本项验收。' end
   if detail then
    -- Independent on-demand composition, including when ACTIVE is below IV.
    local f=SPCCurrentSpecializationFacts.Read(P,shared,pid,c)
    local v=shared.DistrictCompleteness.Read(pid,c,f.token)
    assert(v.availability=='READY' and v.value,'RI_DEPTH_UNAVAILABLE')
    for _,r in ipairs(v.value.districts) do if r.domain=='DISTRICT_CAMPUS' then
     local chosen=v.value.domains.DISTRICT_CAMPUS
     lines[#lines+1]='学院 #'..r.id..'：cap前 '..r.uncapped..' → D'..r.value..'；选中='..tostring(chosen and chosen.districtID==r.id or false)
     for _,b in ipairs(r.buildings) do
      if b.ordinary or not b.type:match('^BUILDING_SPC_') then
       local label=Locale and Locale.Lookup and Locale.Lookup(b.name or b.type) or b.type
       lines[#lines+1]=label..'：Tier '..tostring(b.tier)..'，贡献 '..b.contribution..'，掠夺 '..tostring(b.pillaged)..'，'..tostring(b.reason)
      end
     end
    end end
    for _,b in ipairs(v.value.excluded) do
     local row=P.Info('Buildings',b.type)
     if row and row.PrereqDistrict=='DISTRICT_CAMPUS' and not b.type:match('^BUILDING_SPC_') then lines[#lines+1]=b.type..'：不计入，'..b.reason end
    end
   end
   return table.concat(lines,'\n')
  end)
  return ok and text or (P.VERSION..' | 科研基础设施：暂不可确认\n未把未知当作0；保留上次配置。\n原因：'..tostring(text))
 end
 local function bind(src,n,fn) local e=P.Field(src,n);if e and e.Add then e.Add(fn) end end
 bind(Events,'LoadScreenClose',function() data.ready=true;data.errors={};definitions=nil;data.Audit() end)
 -- Depth-changing events invalidate the bounded shared cache before reading it.
 for _,n in ipairs({'BuildingAddedToMap','BuildingRemovedFromMap','BuildingPillaged','BuildingRepaired','DistrictRemovedFromMap','DistrictBuildProgressChanged','DistrictPillaged','DistrictRepaired','CityTransfered','CityRemovedFromMap'}) do
  SPCRuntimeWork.Hook(P,Events,n,function(scope) shared.DistrictCompleteness.MarkDirty(scope and scope.player);data.Audit(scope) end)
 end
 for _,n in ipairs({'CityWorkerChanged','CityFocusChanged','GovernorAssigned','GovernorEstablished','GovernorChanged','GovernorPromoted','PlayerTurnActivated'}) do SPCRuntimeWork.Hook(P,Events,n,data.Audit) end
 for _,n in ipairs({'OnDistrictConstructed','BuildingConstructed','CityBuilt','OnPillage'}) do bind(GameEvents,n,function() shared.DistrictCompleteness.MarkDirty();data.Audit() end) end
 -- E2 confirmed exit: exact transient IDs owned by this writer; no prefix scan.
 if shared.CityProgressionStore then shared.CityProgressionStore.RegisterExit('ResearchInfrastructure',function(c,loss)
   local ids={};for bit=0,3 do ids[#ids+1]=name(bit)end;for _,id in ipairs(M.Retired)do ids[#ids+1]=id end
   shared.CityProgressionStore.RemoveOwned(c,loss,ids)
 end)end

end
