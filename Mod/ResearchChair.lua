include('RuntimeWork')
include('CarrierSet')
include('ResearchChairModel')
SPCResearchChair={Bits=8}
local M=SPCResearchChair
local function name(target,i) return 'BUILDING_SPC_RESEARCH_CHAIR_'..target..'_'..i end
local reasons={BUILDING_PILLAGED='已掠夺',UNDER_CONSTRUCTION='未完成',UNREVIEWED_BUILDING='未审建筑，暂不计入',
 WONDER='奇观',PALACE='宫殿',INTERNAL_OR_TECHNICAL='内部载体',ORDINARY_TIER_ZERO='不属于一至四级普通建筑',
 DISTRICT_PILLAGED='学院已掠夺',DISTRICT_UNFINISHED='学院未完成'}
local errors={CHAIR_WORKERS_UNKNOWN='工作专家数暂不可读',CHAIR_BUILDINGS_UNKNOWN='学院建筑事实暂不可读',
 CHAIR_ACTIVE_UNKNOWN='专业启用等级暂不可读',CHAIR_FACT_UNKNOWN='当前专业事实暂不可读',
 CHAIR_ENCODING_RANGE='专家数超出当前承载范围；未截断或改写收益',CHAIR_TARGET_UNSUPPORTED='目标建筑尚无已审承载定义',
 CHAIR_TIER_OR_LOCATION_UNKNOWN='建筑等级或位置尚未确认',CHAIR_REFERENCE_UNKNOWN='学院引用尚未确认'}
local function explain(err) local code=tostring(err):match('CHAIR_[A-Z_]+');return errors[code] or code or '接口未就绪' end
function M.Start(P,shared)
 local data={ready=false,busy=false,errors={},changes=0};shared.ResearchChair=data
 local ownedIndex={}
 local health=SPCRuntimeWork.NativeHealth(P,shared,data,function(index)return ownedIndex[index]==true end,function(scope)data.MarkAudit(scope)end)
 local definitions,targets
 local function validate()
  if definitions then return end
  local rows=assert(P.Rows('SPC_ResearchChairTargets'),'CHAIR_TARGET_TABLE_UNKNOWN')
  local defs,ts,nextOwned={},{},{}
  for _,v in ipairs(rows) do
   assert(not ts[v.BuildingType],'CHAIR_TARGET_DUPLICATE');ts[v.BuildingType]=true
   for i=0,M.Bits-1 do
    local r=assert(P.Info('Buildings',name(v.BuildingType,i)),'CHAIR_CARRIER_MISSING')
    assert(r.PrereqDistrict=='DISTRICT_CAMPUS' and r.CitizenSlots==0 and r.Housing==0,'CHAIR_CARRIER_INVALID')
    defs[#defs+1]={target=v.BuildingType,bit=i,id=r.Index};nextOwned[r.Index]=true
   end
  end
  assert(#defs>0,'CHAIR_TARGET_TABLE_EMPTY');definitions=defs;targets=ts;ownedIndex=nextOwned
 end
 local function inspect(pid,c,detail)
  assert(c:GetOwner()==pid,'CHAIR_OWNER_CHANGED')
  return SPCCurrentSpecializationFacts.Inspect(P,shared,pid,c,function(f,readWorkers)
  local p=SPCResearchChairModel.Plan(f,nil,nil,targets)
  if p.status~='NEEDS_BUILDINGS' then return p end
  local reader=detail and shared.DistrictCompleteness.Read or shared.DistrictCompleteness.ReadFacts
  local v=reader(pid,c,f.token)
  p=SPCResearchChairModel.Plan(f,v,nil,targets)
  if p.status~='NEEDS_WORKERS' then return p end
  local workers=readWorkers({id=f.first.districtID,type=f.first.type,plot=p.plot},function()
   local n=assert(Map.GetPlotByIndex(p.plot),'CHAIR_PLOT_UNKNOWN'):GetWorkerCount()
   assert(type(n)=='number'and n>=0 and n<math.huge and n%1==0,'CHAIR_WORKERS_UNKNOWN');return n
  end)
  p=SPCResearchChairModel.Plan(f,v,workers,targets)
  -- Technical encoding bound, not gameplay cap; fail visibly, never truncate.
  assert(p.workers<2^M.Bits,'CHAIR_ENCODING_RANGE')
  return p
  end)
 end
 local function installed(c)
  local b=c:GetBuildings();local rows,amounts={},{}
  for _,d in ipairs(definitions) do
   local yes=P.HasBuilding(b,d.id);assert(type(yes)=='boolean','CHAIR_CARRIER_UNKNOWN')
   local r={id=d.id,target=d.target,bit=d.bit,yes=yes}
   if yes then
    r.plot=b:GetBuildingLocation(d.id);r.pillaged=b:IsPillaged(d.id)
    assert(type(r.plot)=='number' and r.plot>=0 and type(r.pillaged)=='boolean','CHAIR_CARRIER_LOCATION_UNKNOWN')
    if not r.pillaged then amounts[d.target]=(amounts[d.target] or 0)+2^d.bit end
   end
   rows[#rows+1]=r
  end
  return rows,amounts
 end
 local function reconcile(pid,c)
  local p=inspect(pid,c);local rows=installed(c)
  for _,r in ipairs(rows)do r.want=math.floor((p.amounts[r.target] or 0)/2^r.bit)%2==1 end
  SPCCarrierSet.ApplyLocated(P,c,rows,p.plot,health,
   {observedRemoval=true,removeError='CHAIR_REMOVE_FAILED',createError='CHAIR_CREATE_FAILED'},function()data.changes=data.changes+1 end)
 end
 local function audit(scope)
  local ok,err=pcall(function()
   validate();data.definitionError=nil
   for pid,player in pairs(Players) do if SPCRuntimeWork.Player(scope,pid) and P.IsTestPlayer(pid) then
    if not (scope and scope.city~=nil)then data.errors[pid]={}end
    data.errors[pid]=data.errors[pid] or {};local cities=player:GetCities()
    if cities then for _,c in SPCRuntimeWork.Cities(cities,scope) do
     local good,why=pcall(function()if c:GetOwner()==pid then P.Count('city_scan');reconcile(pid,c)end end)
     data.errors[pid][c:GetID()]=not good and tostring(why) or nil
    end end
   end end
  end)
  if not ok then data.definitionError=tostring(err) end
 end
 data.Audit,data.MarkAudit,data.FlushAudit=SPCRuntimeWork.NewAudit(P,shared,data,'ResearchChair',audit)
 function data.Describe(pid,c,detail)
  local ok,text=pcall(function()
   assert(data.ready,'CHAIR_NOT_READY');validate();local p=inspect(pid,c,true);local rows,amounts=installed(c)
   local total=0;local mismatch=false
   for k,n in pairs(amounts) do total=total+n;if n~=(p.amounts[k] or 0) then mismatch=true end end
   for k,n in pairs(p.amounts) do if n~=(amounts[k] or 0) then mismatch=true end end
   local lines={'学术主持 | '..(p.status=='READY' and '科研IV生效' or '未生效'),
    '工作科研专家 '..p.workers..'｜合格学院建筑 '..p.count,
    '每栋 +'..p.workers..' 科技｜合计基础科技预期 +'..p.total,
    '已配置合计 +'..total..(mismatch and '（与当前预期不一致）' or '（与当前预期一致）'),
    '逐栋计算，不按Tier加权，不受D上限限制。配置/预期不是原生实测。'}
   local err=data.definitionError or data.errors[pid] and data.errors[pid][c:GetID()]
   if err then lines[#lines+1]='待确认：'..explain(err) end
   for _,b in ipairs(p.rows) do
    if detail or b.reason=='UNREVIEWED_BUILDING' then
     lines[#lines+1]=Locale.Lookup(b.name or b.type)..'：Tier '..tostring(b.tier)..'；'..(b.eligible and ('预期+'..b.amount..'，配置+'..(amounts[b.type] or 0)) or ('不计入：'..(reasons[b.reason] or tostring(b.reason))))
    end
   end
   return table.concat(lines,'\n')
  end)
  return ok and text or ('学术主持：暂不可确认，保留上次配置。\n'..explain(text))
 end
 local function bind(src,n,f) local e=P.Field(src,n);if e and e.Add then e.Add(f) end end
 SPCRuntimeWork.StartReady(P,shared,'ResearchChair',function()definitions=nil;targets=nil;data.ready=true;data.errors={};data.Audit()end)
 -- Shared D/P0-C owns invalidation and registers first; reuse its confirmed view.
 -- Ordinary structural input is owned by scoped DC D; health is exact above.
 for _,n in ipairs({'PlayerTurnActivated','CityTransfered','CityRemovedFromMap'})do SPCRuntimeWork.Hook(P,Events,n,data.Audit)end
 -- E2 confirmed exit: exact transient IDs owned by this writer; no prefix scan.
 if shared.CityProgressionStore then shared.CityProgressionStore.RegisterExit('ResearchChair',function(c,loss)
   local ids={};for _,v in ipairs(assert(P.Rows('SPC_ResearchChairTargets'),'EXIT_CHAIR_TARGETS_UNKNOWN'))do for bit=0,M.Bits-1 do ids[#ids+1]=name(v.BuildingType,bit)end end
   shared.CityProgressionStore.RemoveOwned(c,loss,ids)
 end)end

end
