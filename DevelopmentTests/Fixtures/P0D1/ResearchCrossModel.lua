-- P0-D1 pure BASE model. No rounding, sampling, writes or hidden formula inputs.
SPCResearchCrossModel={}
local M=SPCResearchCrossModel
M.Yields={'FOOD','PRODUCTION','GOLD','SCIENCE','CULTURE','FAITH'}
M.Domains={DISTRICT_INDUSTRIAL_ZONE=true,DISTRICT_ENCAMPMENT=true,DISTRICT_THEATER=true,DISTRICT_GOVERNMENT=true,DISTRICT_DIPLOMATIC_QUARTER=true,DISTRICT_COMMERCIAL_HUB=true,DISTRICT_HARBOR=true,DISTRICT_HOLY_SITE=true,DISTRICT_NEIGHBORHOOD=true}
function M.Domain(kind,replaces)
 local seen={}
 while replaces[kind] do assert(not seen[kind],'CROSS_REPLACEMENT_CYCLE');seen[kind]=true;kind=replaces[kind] end
 return M.Domains[kind] and kind or nil
end
function M.Plan(f,rows)
 assert(f.validity=='VERIFIED' and type(f.identity)=='string','CROSS_FACTS_UNKNOWN')
 local result={science=0,base=0,count=0,rows={},status='INACTIVE'}
 if f.identity~='RESEARCH' then return result end
 assert(type(f.active)=='number' and f.active%1==0 and f.active>=0 and f.active<=4
  and type(f.potential)=='number' and f.potential%1==0 and f.potential>=f.active and f.potential<=4,'CROSS_ACTIVE_UNKNOWN')
 if f.active<3 then return result end
 assert(type(rows)=='table','CROSS_SAMPLE_UNAVAILABLE')
 local seen={}
 for _,r in ipairs(rows) do
  assert(type(r.reference)=='string' and not seen[r.reference],'CROSS_DUPLICATE_REFERENCE');seen[r.reference]=true
  assert(type(r.complete)=='boolean' and type(r.pillaged)=='boolean','CROSS_DISTRICT_UNAVAILABLE')
  local rec={reference=r.reference,type=r.type,domain=r.domain,base=0,yields={},reason='INCLUDED'}
  if not M.Domains[r.domain] then rec.reason='DOMAIN_EXCLUDED'
  elseif not r.complete then rec.reason='UNFINISHED'
  elseif r.pillaged then rec.reason='PILLAGED'
  else
   assert(type(r.yields)=='table','CROSS_BASE_UNAVAILABLE')
   for _,y in ipairs(M.Yields) do
    local v=r.yields[y];assert(type(v)=='number' and v==v and math.abs(v)<math.huge,'CROSS_BASE_UNAVAILABLE')
    rec.yields[y]=v;rec.base=rec.base+v
   end
   result.count=result.count+1;result.base=result.base+rec.base
  end
  result.rows[#result.rows+1]=rec
 end
 result.science=result.base*0.5;result.status='READY';return result
end
-- Existing B050/B051 primitive has proven integer/half support only.
-- This check diagnoses its domain; it never rounds a Design result into that domain.
function M.ExistingPrimitive(amount,pop)
 if type(amount)~='number' or amount~=amount or amount<0 or amount>65535.5 or amount*2%1~=0 then
  return nil,'CROSS_NATIVE_PRECISION_UNVERIFIED'
 end
 local whole=math.floor(amount)
 if whole==amount then return {integer=whole,amount=amount} end
 if type(pop)~='number' or pop%1~=0 or pop<1 or pop>255 then return nil,'CROSS_NATIVE_POPULATION_UNVERIFIED' end
 local odd,bit=pop,0
 while odd%2==0 do odd=odd/2;bit=bit+1 end
 return {integer=whole-(odd-1)/2,coefficient=1/2^(bit+1),bit=bit,amount=amount}
end
