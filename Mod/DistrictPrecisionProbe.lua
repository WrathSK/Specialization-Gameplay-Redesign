-- B082 on-demand native district precision experiment; not a P0-D1 writer.
SPCDistrictPrecisionProbe={}
local M=SPCDistrictPrecisionProbe
M.Stages={'03','05','1'}
M.Amounts={['03']=0.3,['05']=0.5,['1']=1}
function M.Start(P,shared)
 local data={cleanupError=nil};shared.DistrictPrecisionProbe=data
 local function rows(c)
  local out={};local b=c:GetBuildings()
  for _,s in ipairs(M.Stages) do
   local id=assert(P.Info('Buildings','BUILDING_SPC_B082_DISTRICT_'..s),'DP_DATABASE_MISSING').Index
   local yes=P.HasBuilding(b,id);assert(type(yes)=='boolean','DP_BUILDING_UNKNOWN')
   out[#out+1]={stage=s,id=id,yes=yes}
  end
  return out
 end
 local function clear(c,rs)
  for _,r in ipairs(rs) do if r.yes then
   P.RemoveBuilding(c:GetBuildings(),r.id)
   assert(P.HasBuilding(c:GetBuildings(),r.id)==false,'DP_REMOVE_UNCONFIRMED');r.yes=false
  end end
 end
 local function campus(c)
  local n,found=0,nil
  for _,d in c:GetDistricts():Members() do
   local r=assert(P.Info('Districts',d:GetType()),'DP_DISTRICT_UNKNOWN')
   local match=r.DistrictType=='DISTRICT_CAMPUS'
   if not match then for _,v in ipairs(P.Rows('DistrictReplaces') or {}) do
    if v.CivUniqueDistrictType==r.DistrictType and v.ReplacesDistrictType=='DISTRICT_CAMPUS' then match=true end
   end end
   if match then
    assert(d:IsComplete()==true and d:IsPillaged()==false,'DP_CAMPUS_NOT_READY')
    n=n+1;found=d
   end
  end
  assert(n==1,'DP_ONE_COMPLETED_CAMPUS_REQUIRED');return found
 end
 function data.Run(pid,c,action)
  assert(P.IsTestPlayer(pid) and c:GetOwner()==pid,'DP_OWN_TEST_CITY_REQUIRED')
  local rs=rows(c)
  if action=='DP_OFF' then clear(c,rs)
  elseif action~='DP_READ' then
   local wanted=action:match('^DP_SET_(.+)$');assert(M.Amounts[wanted],'DP_BAD_STAGE')
   campus(c);assert(c:GetProperty('SPC_B050_HALF_ENABLED')~=true,'DP_DISABLE_OLD_HALF_EXPERIMENT')
   -- Remove before add; same explicit stage is idempotent, never a toggle/retry.
   for _,r in ipairs(rs) do if r.stage~=wanted and r.yes then clear(c,{r}) end end
   for _,r in ipairs(rs) do if r.stage==wanted and not r.yes then
    P.CreateBuilding(c:GetBuildQueue(),r.id)
    assert(P.HasBuilding(c:GetBuildings(),r.id)==true,'DP_CREATE_UNCONFIRMED');r.yes=true
   end end
  end
  local amount,count=0,0
  for _,r in ipairs(rs) do if r.yes then amount=amount+M.Amounts[r.stage];count=count+1 end end
  assert(count<=1,'DP_MIXED_EXPERIMENT')
  data.view={owner=pid,city=c:GetID(),amount=amount}
  return '学院科技精度实验：'..(count==0 and 'OFF' or ('配置 +'..amount..'（尚非实测）'))
   ..'\n仅实验；旧科研能力保持。读数比较区域原生值，城市总量含其它倍率。'
   ..(action~='DP_READ' and '\n请点击「区域读数」确认本阶段结算；结束后右键关闭。' or '')
   ..(data.cleanupError and '\n载入清理存在异常：'..data.cleanupError or '')
 end
 -- An experimental save never silently resumes a probe. One load pass, no retry loop.
 local function clean()
  data.view=nil;data.cleanupError=nil
  for _,p in pairs(Players) do
   local ok,err=pcall(function() for _,c in p:GetCities():Members() do clear(c,rows(c)) end end)
   if not ok then data.cleanupError=tostring(err) end
  end
 end
 local e=P.Field(Events,'LoadScreenClose');if e and e.Add then e.Add(clean) end
end
