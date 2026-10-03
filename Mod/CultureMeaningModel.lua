-- Culture D0038: Floor EACH domain contribution before same-yield sum and W.
-- Pure model covers nine mappings; the opt-in writer probes S/G/Culture only.
SPCCultureMeaningModel={K=0.5,Domains={
 {'DISTRICT_CAMPUS','SCIENCE'},{'DISTRICT_INDUSTRIAL_ZONE','PRODUCTION'},
 {'DISTRICT_COMMERCIAL_HUB','GOLD'},{'DISTRICT_HARBOR','GOLD'},{'DISTRICT_ENCAMPMENT','PRODUCTION'},
 {'DISTRICT_HOLY_SITE','FAITH'},{'DISTRICT_GOVERNMENT','CULTURE'},{'DISTRICT_DIPLOMATIC_QUARTER','CULTURE'},{'DISTRICT_NEIGHBORHOOD','FOOD'}
}}
local M=SPCCultureMeaningModel
local function integer(n)return type(n)=='number' and n>=0 and n<math.huge and n%1==0 end
function M.Plan(f,w,depth)
 assert(f and f.validity=='VERIFIED','ME_FACT_UNKNOWN')
 local p={status='INACTIVE',active=f.active,count=0,each={},total={},domains={}}
 for _,y in ipairs({'FOOD','PRODUCTION','GOLD','SCIENCE','CULTURE','FAITH'})do p.each[y]=0;p.total[y]=0 end
 if f.identity~='CULTURE' then return p end
 assert(integer(f.potential),'ME_POTENTIAL_UNKNOWN');if f.potential<4 then return p end
 assert(f.activeStatus=='KNOWN' and integer(f.active),'ME_ACTIVE_UNKNOWN');if f.active<4 then return p end
 assert(w and w.hasConfirmed and w.availability=='KNOWN' and integer(w.count),'ME_WORKS_UNKNOWN')
 assert(w.modifierExcludedCount==0 and w.unknownCategoryCount==0,'ME_FIXTURE_UNSUPPORTED_WORK')
 p.count=w.count;p.status='NEEDS_DEPTH';if not depth then return p end
 assert(depth.validity=='VERIFIED' and depth.availability=='READY' and depth.value,'ME_DEPTH_UNKNOWN')
 local used={};for _,d in ipairs(M.Domains)do used[d[1]]=true end
 for _,d in ipairs(depth.value.districts)do if used[d.domain] and d.complete and not d.pillaged then
  for _,b in ipairs(d.buildings)do
   assert(not (b.ordinary and b.depthEligible and b.complete and not b.pillaged and b.tier==nil),'ME_TIER_UNKNOWN')
  end
 end end
 for _,d in ipairs(M.Domains)do
  local raw=depth.value.domains[d[1]];local n=raw and raw.value or 0
  assert(integer(n) and n<=10,'ME_DEPTH_INVALID')
  local rawEach=M.K*n*(d[2]=='GOLD' and 3 or 1);local each=math.floor(rawEach)
  p.domains[d[1]]={value=n,districtID=raw and raw.districtID,yield=d[2],rawEach=rawEach,each=each}
  p.each[d[2]]=p.each[d[2]]+each
 end
 for y,n in pairs(p.each)do p.total[y]=n*p.count end
 p.status='READY';return p
end
-- Half-unit encoding is an exact technical bound, never a quantization policy.
M.ProbeBits={SCIENCE=4,GOLD=6,CULTURE=4};M.ProbeScale={SCIENCE=2,GOLD=2,CULTURE=1};M.Owned={}
for _,y in ipairs({'SCIENCE','GOLD','CULTURE'})do for bit=0,M.ProbeBits[y]-1 do
 M.Owned[#M.Owned+1]='BUILDING_SPC_MEANING_PROBE_'..y..'_'..bit
end end
-- Two fixed Culture3 candidates only; no general runtime yield directory.
M.Variants={'SPLIT','SINGLE3','SINGLE3_SCALE100'}
M.VariantParts={
 SINGLE3={name='BUILDING_SPC_MEANING_PROBE_CULTURE_SINGLE3',amount=3},
 SINGLE3_SCALE100={name='BUILDING_SPC_MEANING_PROBE_CULTURE_SINGLE3_SCALE100',amount=3,scalingFactor=100}
}
for _,variant in ipairs(M.Variants)do
 local part=M.VariantParts[variant];if part then M.Owned[#M.Owned+1]=part.name end
end
function M.Parts(y,amount,variant)
 variant=variant or 'SPLIT'
 if variant~='SPLIT' then
  local part=assert(M.VariantParts[variant],'ME_ENCODING_VARIANT_UNKNOWN')
  assert(y=='CULTURE','ME_ENCODING_VARIANT_CULTURE_ONLY')
  assert(amount==part.amount,'ME_ENCODING_VARIANT_CULTURE3_REQUIRED')
  return {part.name}
 end
 local bits=assert(M.ProbeBits[y],'ME_PROBE_YIELD');local n=amount*M.ProbeScale[y]
 assert(integer(n) and n<2^bits,'ME_ENCODING_RANGE')
 local out={};for bit=0,bits-1 do if n%2==1 then out[#out+1]='BUILDING_SPC_MEANING_PROBE_'..y..'_'..bit end;n=math.floor(n/2)end
 return out
end
