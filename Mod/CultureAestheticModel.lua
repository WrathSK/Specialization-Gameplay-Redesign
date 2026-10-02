-- Culture D0029 CUL_L3_AESTHETIC. Initial K is not final balance.
SPCCultureAestheticModel={K=1}
local M=SPCCultureAestheticModel
local function integer(v)return type(v)=='number' and v>=0 and v<math.huge and v%1==0 end
function M.Plan(f,works,view,detail)
 assert(f and f.validity=='VERIFIED','AE_FACT_UNKNOWN')
 local p={status='INACTIVE',active=f.active,eras=0,count=0,each=0,total=0,amounts={},rows={}}
 if f.identity~='CULTURE' then return p end
 assert(integer(f.potential),'AE_POTENTIAL_UNKNOWN')
 if f.potential<3 then return p end
 assert(f.activeStatus=='KNOWN' and integer(f.active),'AE_ACTIVE_UNKNOWN')
 if f.active<3 then return p end
 assert(works and works.hasConfirmed and works.availability=='KNOWN' and integer(works.eraCount),'AE_WORKS_UNKNOWN')
 p.eras=works.eraCount;p.each=p.eras*M.K;p.status='READY'
 if not view then p.status='NEEDS_BUILDINGS';return p end
 assert(view.validity=='VERIFIED' and view.availability=='READY' and view.value,'AE_BUILDINGS_UNKNOWN')
 local seen={}
 for _,d in ipairs(view.value.districts) do
  assert(integer(d.plot) and type(d.complete)=='boolean' and type(d.pillaged)=='boolean','AE_DISTRICT_UNKNOWN')
  for _,b in ipairs(d.buildings) do
   local yes=b.ordinary==true;local reason=b.ordinaryReason or b.reason
   if yes then
    assert(not seen[b.type],'AE_DUPLICATE_BUILDING');seen[b.type]=true
    assert(b.ordinaryDistrict and b.ordinaryDistrict==d.baseDistrict,'AE_BUILDING_LOCATION_UNKNOWN')
    assert(type(b.complete)=='boolean' and type(b.pillaged)=='boolean','AE_BUILDING_UNKNOWN')
    if not b.complete then yes=false;reason='UNDER_CONSTRUCTION'
    elseif not d.complete then yes=false;reason='DISTRICT_UNFINISHED'
    elseif d.pillaged then yes=false;reason='DISTRICT_PILLAGED'
    elseif b.pillaged then yes=false;reason='BUILDING_PILLAGED'
    else reason='ELIGIBLE' end
   end
   local amount=yes and p.each or 0
   if detail then p.rows[#p.rows+1]={type=b.type,name=b.name,plot=d.plot,eligible=yes,reason=reason,amount=amount}end
   if yes then p.count=p.count+1;p.total=p.total+amount;p.amounts[d.plot]=(p.amounts[d.plot] or 0)+amount end
  end
 end
 for _,b in ipairs(detail and view.value.excluded or {})do
  p.rows[#p.rows+1]={type=b.type,name=b.name,plot=b.plot,eligible=false,reason=b.reason,amount=0}
 end
 return p
end
