include('RuntimeWork')
include('ResearchCrossSample')
-- Sole RES_L3_CROSS writer. No population/specialist/Network/D input.
SPCResearchCross={}
local M=SPCResearchCross
M.Bits=16 -- signed encoding limit, not a gameplay cap: overflow HOLDs visibly
M.Retired={}
for i=0,7 do M.Retired[#M.Retired+1]='BUILDING_SPC_DEV_LV3_POP_RESEARCH_'..i end
for _,s in ipairs({'03','05','1'}) do M.Retired[#M.Retired+1]='BUILDING_SPC_B082_DISTRICT_'..s end
local function name(sign,i) return 'BUILDING_SPC_RESEARCH_CROSS_'..sign..'_'..i end
function M.Start(P,shared)
 local data={ready=false,busy=false,errors={},plans={},changes=0};shared.ResearchCross=data
 SPCSampleLifecycle.Reset(data,'cross')
 local function installed(c)
  local out={old={},bits={},amount=0,oldCount=0};local b=c:GetBuildings()
  for _,n in ipairs(M.Retired) do
   local id=assert(P.Info('Buildings',n),'CROSS_OLD_DEFINITION_MISSING').Index
   local yes=P.HasBuilding(b,id);assert(type(yes)=='boolean','CROSS_CARRIER_UNKNOWN')
   out.old[#out.old+1]={id=id,yes=yes};if yes then out.oldCount=out.oldCount+1 end
  end
  for _,sign in ipairs({'POS','NEG'}) do for i=0,M.Bits-1 do
   local id=assert(P.Info('Buildings',name(sign,i)),'CROSS_DEFINITION_MISSING').Index
   local yes=P.HasBuilding(b,id);assert(type(yes)=='boolean','CROSS_CARRIER_UNKNOWN')
   local pillaged=yes and b:IsPillaged(id) or false;assert(type(pillaged)=='boolean','CROSS_CARRIER_PILLAGE_UNKNOWN')
   out.bits[#out.bits+1]={id=id,yes=yes,pillaged=pillaged,sign=sign,bit=i}
   if yes and not pillaged then out.amount=out.amount+(sign=='POS' and 1 or -1)*2^i end
  end end
  return out
 end
 local function remove(c,r)
  P.RemoveBuilding(c:GetBuildings(),r.id);assert(P.HasBuilding(c:GetBuildings(),r.id)==false,'CROSS_REMOVE_UNCONFIRMED');r.yes=false;data.changes=data.changes+1
 end
 local function inspect(pid,c)
  local f=SPCCurrentSpecializationFacts.Read(P,shared,pid,c)
  local plan=SPCResearchCrossModel.Plan(f,{}) -- validate activation independently of sample availability
  if plan.status~='READY' then return plan end
  local districts=c:GetDistricts();local n=districts:GetNumDistricts()
  assert(type(n)=='number' and n%1==0 and n>=0 and n<=512,'CROSS_DISTRICT_COUNT_UNKNOWN')
  local rows={};local campus;local nc=0;local replaces=SPCResearchCrossSample.Replacements(P)
  for i=0,n-1 do
   local d=assert(districts:GetDistrictByIndex(i),'CROSS_DISTRICT_UNKNOWN');P.Count('district_scan')
   local info=assert(P.Info('Districts',d:GetType()),'CROSS_TYPE_UNKNOWN')
   local kind=info.DistrictType;local seen={}
   while replaces[kind] do assert(not seen[kind],'CROSS_REPLACEMENT_CYCLE');seen[kind]=true;kind=replaces[kind] end
   local complete,pillaged=d:IsComplete(),d:IsPillaged()
   assert(type(complete)=='boolean' and type(pillaged)=='boolean','CROSS_DISTRICT_STATE_UNKNOWN')
   if kind=='DISTRICT_CAMPUS' then nc=nc+1;campus={id=d:GetID(),complete=complete,pillaged=pillaged} end
   local r={id=d:GetID(),type=info.DistrictType,domain=SPCResearchCrossModel.Domain(info.DistrictType,replaces),complete=complete,pillaged=pillaged,
    reference=SPCSampleLifecycle.Reference(c,d,info)}
   rows[#rows+1]=r
  end
  assert(nc<=1,'CROSS_MULTIPLE_CAMPUSES')
  if not campus or not campus.complete or campus.pillaged then plan.status='INACTIVE';return plan end
  assert(f.first and f.first.districtID==campus.id,'CROSS_ANCHOR_UNKNOWN')
  for _,r in ipairs(rows) do if r.domain and r.complete and not r.pillaged then
   local batch=data.samples[pid];local sample=batch and batch.rows[c:GetID()..':'..r.id]
   assert(sample and sample.reference==r.reference and not sample.pillaged,'CROSS_SAMPLE_PENDING')
   r.yields=sample.yields
  end end
  plan=SPCResearchCrossModel.Plan(f,rows);plan.active=f.active;plan.potential=f.potential
  assert(math.abs(plan.science)<2^M.Bits,'CROSS_ENCODING_RANGE_UNSUPPORTED')
  return plan
 end
 local function reconcile(pid,c)
  local state=installed(c)
  -- SQL already makes these inert; cleanup is explicit, limited, and before new writes.
  for _,r in ipairs(state.old) do if r.yes then remove(c,r) end end
  local plan=inspect(pid,c);local amount=plan.science
  for _,r in ipairs(state.bits) do
   r.want=(amount>=0 and r.sign=='POS' or amount<0 and r.sign=='NEG') and math.floor(math.abs(amount)/2^r.bit)%2==1
   if r.yes and (not r.want or r.pillaged) then remove(c,r) end
  end
  for _,r in ipairs(state.bits) do if r.want and not r.yes then
   P.CreateBuilding(c:GetBuildQueue(),r.id)
   assert(P.HasBuilding(c:GetBuildings(),r.id)==true and c:GetBuildings():IsPillaged(r.id)==false,'CROSS_CREATE_UNCONFIRMED');data.changes=data.changes+1
  end end
  if state.amount~=0 and amount==0 then P.Count('cross_withdraw') end
  return plan
 end
 function data.Audit(scope)
  if not data.ready or data.busy then P.Count('busy_skip');return end
  data.busy=true
  for pid,player in pairs(Players) do if SPCRuntimeWork.Player(scope,pid) and P.IsTestPlayer(pid) then
   data.errors[pid]={};local nextPlans={}
   local ok,err=pcall(function()
    local cities=player:GetCities();if not cities then return end
    for _,c in cities:Members() do P.Count('city_scan')
     local good,p=pcall(reconcile,pid,c)
     if good then nextPlans[c:GetID()]=p else data.errors[pid][c:GetID()]=tostring(p) end
    end
   end)
   data.plans[pid]=nextPlans
   if not ok then data.errors[pid].player=tostring(err) end
  end end
  data.busy=false
 end
 function data.Receive(pid,p)
  if SPCResearchCrossSample.Receive(P,data,pid,p) then data.Audit({player=pid}) end
 end
 function data.Describe(pid,c,detail)
  local ok,text=pcall(function()
   local p=inspect(pid,c);local s=installed(c)
   local lines={'跨学科研究 | ACTIVE='..tostring(p.active or '未生效'),
    '合格区域 '..p.count..'；BASE合计 '..p.base,
    '50%原值 '..(p.rawScience or 0)..' → 临时floor：学院科技 '..p.science,
    '区域载体配置 '..s.amount..'；旧效果/实验残留 '..s.oldCount}
   local err=data.errors[pid] and (data.errors[pid][c:GetID()] or data.errors[pid].player)
   if err then lines[#lines+1]='待确认：'..(err:match('CROSS_[A-Z_]+') or '接口错误') end
   if c:GetProperty('SPC_B050_HALF_ENABLED') then lines[#lines+1]='旧半点实验仍开启，混合收益不可作为验收。' end
   lines[#lines+1]='配置不是原生实测；未来改用D仅为待审建议。'
   local labels={FOOD='食物',PRODUCTION='生产力',GOLD='金币',SCIENCE='科技',CULTURE='文化',FAITH='信仰'}
   local reasons={INCLUDED='计入',DOMAIN_EXCLUDED='非合格领域',UNFINISHED='未完成',PILLAGED='已掠夺'}
   if detail then for _,r in ipairs(p.rows) do
    local info=P.Info('Districts',r.type);local label=Locale and Locale.Lookup and Locale.Lookup(info and info.Name or r.type) or r.type
    local a={};for _,y in ipairs(SPCResearchCrossModel.Yields) do if r.yields[y] and r.yields[y]~=0 then a[#a+1]=labels[y]..' '..r.yields[y] end end
    lines[#lines+1]=label..'：'..(reasons[r.reason] or r.reason)..'；BASE '..r.base..' '..table.concat(a,' / ')
   end end
   return table.concat(lines,'\n')
  end)
  return ok and text or ('跨学科研究：暂不可确认，未将未知当0。\n'..(tostring(text):match('CROSS_[A-Z_]+') or '接口未就绪'))
 end
 local function bind(src,n,fn) local e=P.Field(src,n);if e and e.Add then e.Add(fn) end end
 bind(Events,'LoadScreenClose',function() data.ready=true;SPCSampleLifecycle.Reset(data,'cross');data.plans={};data.errors={};data.Audit() end)
 for _,n in ipairs({'PlayerTurnActivated','GovernorAssigned','GovernorEstablished','GovernorChanged','GovernorPromoted',
  'DistrictAddedToMap','DistrictRemovedFromMap','DistrictBuildProgressChanged','DistrictPillaged','DistrictRepaired','CityTransfered','CityRemovedFromMap'}) do
  SPCRuntimeWork.Hook(P,Events,n,data.Audit)
 end
 for _,n in ipairs({'OnDistrictConstructed','CityBuilt'}) do bind(GameEvents,n,data.Audit) end
end
