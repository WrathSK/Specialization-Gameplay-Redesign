-- P0-D2: user-authorized floor per specialist AFTER grouping domains by yield.
SPCResearchApplyModel={}
local M=SPCResearchApplyModel
M.Yields={'FOOD','PRODUCTION','GOLD','CULTURE','FAITH'}
M.Mapping={
 {'DISTRICT_INDUSTRIAL_ZONE','PRODUCTION',1,'工业区'}, {'DISTRICT_ENCAMPMENT','PRODUCTION',1,'军营'},
 {'DISTRICT_THEATER','CULTURE',1,'剧院'}, {'DISTRICT_GOVERNMENT','CULTURE',1,'市政广场'},
 {'DISTRICT_DIPLOMATIC_QUARTER','CULTURE',1,'外交区'}, {'DISTRICT_COMMERCIAL_HUB','GOLD',3,'商业中心'},
 {'DISTRICT_HARBOR','GOLD',3,'港口'}, {'DISTRICT_HOLY_SITE','FAITH',1,'圣地'}, {'DISTRICT_NEIGHBORHOOD','FOOD',1,'社区'}}
M.Labels={FOOD='食物',PRODUCTION='生产力',GOLD='金币',CULTURE='文化',FAITH='信仰'}
function M.Plan(f,depth,workers)
 local p={status='INACTIVE',rows={},raw={},per={},total={}}
 for _,y in ipairs(M.Yields) do p.per[y]=0;p.total[y]=0 end
 assert(f.validity=='VERIFIED' and type(f.identity)=='string','AP_FACT_UNKNOWN')
 if f.identity~='RESEARCH' then return p end
 assert(type(f.active)=='number' and f.active%1==0 and f.active>=0 and f.active<=4
  and type(f.potential)=='number' and f.potential%1==0 and f.potential>=f.active and f.potential<=4,'AP_ACTIVE_UNKNOWN')
 if f.active<3 then return p end
 if depth==nil then p.status='NEEDS_DEPTH';return p end
 assert(depth.validity=='VERIFIED' and depth.availability=='READY' and depth.value,'AP_DEPTH_UNKNOWN')
 assert(type(workers)=='number' and workers>=0 and workers%1==0 and workers<math.huge,'AP_WORKERS_UNKNOWN')
 if not depth.value.domains.DISTRICT_CAMPUS then return p end
 for _,m in ipairs(M.Mapping) do
  local d=depth.value.domains[m[1]];local n=d and d.value or 0
  assert(type(n)=='number' and n>=0 and n<=10 and n%1==0,'AP_DEPTH_INVALID')
  local v=.5*n*m[3];p.per[m[2]]=p.per[m[2]]+v
  p.rows[#p.rows+1]={domain=m[1],label=m[4],district=d and d.districtID,d=n,shares=.5*n,yield=m[2],amount=v}
 end
 for _,y in ipairs(M.Yields) do p.raw[y]=p.per[y];p.per[y]=math.floor(p.raw[y]);p.total[y]=p.per[y]*workers end
 p.workers=workers;p.status='READY';return p
end
