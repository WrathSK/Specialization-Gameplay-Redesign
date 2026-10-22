-- B083 fixes Gameplay indexed enumeration and absent city containers; B082 on-demand native district precision experiment; not a P0-D1 writer.
SPCDistrictPrecisionProbe={}
local M=SPCDistrictPrecisionProbe
M.Stages={'03','05','1'}
M.Amounts={['03']=0.3,['05']=0.5,['1']=1}
function M.Error(err)
 local code=tostring(err):match('DP_[A-Z_]+') or 'DP_API_UNAVAILABLE'
 local text={DP_API_UNAVAILABLE='游戏接口不可用',DP_ONE_COMPLETED_CAMPUS_REQUIRED='需要一座已完成的学院',
  DP_CAMPUS_NOT_READY='学院未完成或被掠夺',DP_DISABLE_OLD_HALF_EXPERIMENT='请先关闭旧半点实验',
  DP_REMOVE_UNCONFIRMED='旧实验撤销未确认，未继续添加',DP_CREATE_UNCONFIRMED='实验载体创建未确认',
  DP_DISTRICT_COUNT_UNKNOWN='区域数量暂不可读',DP_DISTRICT_ENTRY_UNKNOWN='区域对象暂不可读',
  DP_OWN_TEST_CITY_REQUIRED='请选中己方测试城市'}
 return (text[code] or '实验状态未确认')..'（'..code..'）'
end
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
  local districts=assert(c:GetDistricts(),'DP_DISTRICT_COLLECTION_UNKNOWN')
  local count=districts:GetNumDistricts()
  assert(type(count)=='number' and count>=0 and count%1==0 and count<=512,'DP_DISTRICT_COUNT_UNKNOWN')
  for i=0,count-1 do
   local d=assert(districts:GetDistrictByIndex(i),'DP_DISTRICT_ENTRY_UNKNOWN')
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
   local ok,err=pcall(function()
    local cities=p:GetCities()
    -- Unused/non-city player slots legitimately expose no city collection.
    if cities then for _,c in cities:Members() do clear(c,rows(c)) end end
   end)
   if not ok then data.cleanupError=M.Error(err) end
  end
 end
 local e=P.Field(Events,'LoadScreenClose');if e and e.Add then e.Add(clean) end
end
