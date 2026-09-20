-- Narrow per-building plan; D value/uncapped sum never participates in output.
SPCResearchChairModel={}
local M=SPCResearchChairModel
function M.Plan(f,v,workers,targets)
 local p={status='INACTIVE',workers=0,count=0,total=0,amounts={},rows={}}
 assert(f.validity=='VERIFIED' and type(f.identity)=='string','CHAIR_FACT_UNKNOWN')
 if f.identity~='RESEARCH' then return p end
 assert(type(f.active)=='number' and f.active%1==0 and f.active>=0 and f.active<=4
  and type(f.potential)=='number' and f.potential%1==0 and f.potential>=f.active and f.potential<=4,'CHAIR_ACTIVE_UNKNOWN')
 if f.active<4 then return p end
 if not v then p.status='NEEDS_BUILDINGS';return p end
 assert(v.validity=='VERIFIED' and v.availability=='READY' and v.value,'CHAIR_BUILDINGS_UNKNOWN')
 local campus,n=nil,0
 for _,d in ipairs(v.value.districts) do if d.domain=='DISTRICT_CAMPUS' then campus=d;n=n+1 end end
 assert(n<=1,'CHAIR_MULTIPLE_CAMPUSES')
 if not campus or not campus.complete or campus.pillaged then return p end
 assert(f.first and f.first.districtID==campus.id and f.first.type==campus.type,'CHAIR_REFERENCE_UNKNOWN')
 if workers==nil then p.status='NEEDS_WORKERS';p.plot=campus.plot;return p end
 assert(type(workers)=='number' and workers>=0 and workers<math.huge and workers%1==0,'CHAIR_WORKERS_UNKNOWN')
 p.plot=campus.plot;p.workers=workers;p.status='READY'
 for _,b in ipairs(campus.buildings) do
  local eligible=b.ordinary and b.complete and not b.pillaged
  if eligible then assert(type(b.tier)=='number' and b.reason~='BUILDING_LOCATION_DOMAIN_CONFLICT','CHAIR_TIER_OR_LOCATION_UNKNOWN') end
  eligible=eligible and b.tier>=1 and b.tier<=4
  if eligible then
   assert(targets[b.type],'CHAIR_TARGET_UNSUPPORTED')
   assert(p.amounts[b.type]==nil,'CHAIR_DUPLICATE_BUILDING')
   p.amounts[b.type]=workers;p.count=p.count+1;p.total=p.total+workers
  end
  if not b.type:match('^BUILDING_SPC_') then p.rows[#p.rows+1]={type=b.type,name=b.name,tier=b.tier,
   amount=eligible and workers or 0,eligible=eligible,reason=b.reason,pillaged=b.pillaged} end
 end
 return p
end
