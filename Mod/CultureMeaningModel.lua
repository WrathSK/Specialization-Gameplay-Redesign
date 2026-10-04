-- D0046 retains nine-domain Design; B164 quarantines failed Culture projection.
-- Seven live domains / five yields; all six owned definition families stay for cleanup.
-- Floor EACH domain before same-yield sum and W; controlled one-city probe only.
SPCCultureMeaningModel={K=0.5,Domains={
 {'DISTRICT_CAMPUS','SCIENCE'},{'DISTRICT_INDUSTRIAL_ZONE','PRODUCTION'},
 {'DISTRICT_COMMERCIAL_HUB','GOLD'},{'DISTRICT_HARBOR','GOLD'},{'DISTRICT_ENCAMPMENT','PRODUCTION'},
 {'DISTRICT_HOLY_SITE','FAITH'},{'DISTRICT_NEIGHBORHOOD','FOOD'}
}}
local M=SPCCultureMeaningModel
M.WriteYields={'SCIENCE','PRODUCTION','GOLD','FOOD','FAITH','CULTURE'}
M.CultureDeferred=true -- Native coexistence failed; never take over another mod's effect.
M.ActiveWriteYields={'SCIENCE','PRODUCTION','GOLD','FOOD','FAITH'} -- Not formal all-city cutover.
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
M.ProbeBits={SCIENCE=4,GOLD=6,CULTURE=4,PRODUCTION=4,FOOD=3,FAITH=3};M.ProbeScale={SCIENCE=2,GOLD=2,CULTURE=1,PRODUCTION=1,FOOD=1,FAITH=1};M.Owned={}
for _,y in ipairs({'SCIENCE','GOLD','CULTURE'})do for bit=0,M.ProbeBits[y]-1 do
 M.Owned[#M.Owned+1]='BUILDING_SPC_MEANING_PROBE_'..y..'_'..bit
end end
-- Legacy Culture candidates remain exact withdrawal metadata, not normal final values.
M.Variants={'SPLIT','SINGLE3','SINGLE3_SCALE100'}
M.VariantParts={
 SINGLE3={name='BUILDING_SPC_MEANING_PROBE_CULTURE_SINGLE3',amount=3},
 SINGLE3_SCALE100={name='BUILDING_SPC_MEANING_PROBE_CULTURE_SINGLE3_SCALE100',amount=3,scalingFactor=100}
}
for _,variant in ipairs(M.Variants)do
 local part=M.VariantParts[variant];if part then M.Owned[#M.Owned+1]=part.name end
end
-- Ten additional integer pieces. Existing S/G definitions and all sixteen old
-- IDs stay stable, including inert Culture candidates for saved-effect cleanup.
for _,y in ipairs({'PRODUCTION','FOOD','FAITH'})do for bit=0,M.ProbeBits[y]-1 do
 M.Owned[#M.Owned+1]='BUILDING_SPC_MEANING_PROBE_'..y..'_'..bit
end end
local function bitParts(y,amount)
 assert(y~='CULTURE','ME_CULTURE_DEFERRED')
 local bits=assert(M.ProbeBits[y],'ME_PROBE_YIELD');local n=amount*M.ProbeScale[y]
 assert(integer(n) and n<2^bits,'ME_ENCODING_RANGE')
 local out={};for bit=0,bits-1 do if n%2==1 then out[#out+1]='BUILDING_SPC_MEANING_PROBE_'..y..'_'..bit end;n=math.floor(n/2)end
 return out
end
-- Fixed B160 controls retain the exact old pieces as negative evidence.
-- Production's model projection uses one FINAL per-work value, never these bits.
M.DiagnosticSingle3={name='BUILDING_SPC_MEANING_PROBE_PRODUCTION_SINGLE3',amount=3}
M.Owned[#M.Owned+1]=M.DiagnosticSingle3.name
M.ProductionValues={}
for amount=1,10 do
 local part={name='BUILDING_SPC_MEANING_PROBE_PRODUCTION_VALUE_'..amount,amount=amount}
 M.ProductionValues[amount]=part;M.Owned[#M.Owned+1]=part.name
end
-- Reuse the verified Production directory; append only the other exact values.
M.FinalLimits={SCIENCE=5,PRODUCTION=10,GOLD=30,FOOD=5,FAITH=5,CULTURE=10}
M.FinalValues={PRODUCTION=M.ProductionValues};M.CarrierDistrict={}
for _,y in ipairs(M.WriteYields)do if y~='PRODUCTION' then
 local values={};M.FinalValues[y]=values
 for amount=1,M.FinalLimits[y]do
  local part={name='BUILDING_SPC_MEANING_PROBE_'..y..'_VALUE_'..amount,amount=amount}
  values[amount]=part;M.Owned[#M.Owned+1]=part.name
  -- A real host delta from the failed B155 CityCenter Culture candidate.
  -- This is a technical gate, not permission to remove or compensate HD yields.
  if y=='CULTURE' then M.CarrierDistrict[part.name]='DISTRICT_THEATER' end
 end
end end
function M.Parts(y,amount,variant)
 assert(not M.CultureDeferred or y~='CULTURE' or amount==0,'ME_CULTURE_DEFERRED')
 assert(variant==nil or variant=='SPLIT','ME_VARIANT_DEFERRED')
 local limit=assert(M.FinalLimits[y],'ME_PROBE_YIELD')
 assert(integer(amount) and amount<=limit,'ME_ENCODING_RANGE')
 return amount==0 and {} or {M.FinalValues[y][amount].name}
end
M.DiagnosticExpected={BASELINE=0,SINGLE1=1,CLEAR1=0,SINGLE2=2,PAIR12=3,REMAIN2=2,SINGLE3=3,OFF=0}
function M.DiagnosticParts(stage)
 local amount=assert(M.DiagnosticExpected[stage],'ME_DIAGNOSTIC_STAGE')
 if stage=='SINGLE3' then return {M.DiagnosticSingle3.name}end
 return bitParts('PRODUCTION',amount)
end
