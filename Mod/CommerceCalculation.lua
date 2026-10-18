-- B239 pure Commercialization calculation. Store owns choices/reputation;
-- native current facts and the verified route boundary own all inputs.
SPCCommerceCalculation={}
local M=SPCCommerceCalculation
M.Domains={
 {id='DISTRICT_CAMPUS',yield='SCIENCE',nameKey='LOC_DISTRICT_CAMPUS_NAME'},
 {id='DISTRICT_THEATER',yield='CULTURE',nameKey='LOC_DISTRICT_THEATER_NAME'},
 {id='DISTRICT_INDUSTRIAL_ZONE',yield='PRODUCTION',nameKey='LOC_DISTRICT_INDUSTRIAL_ZONE_NAME'},
 {id='DISTRICT_HOLY_SITE',yield='FAITH',nameKey='LOC_DISTRICT_HOLY_SITE_NAME'},
 {id='DISTRICT_HARBOR',yield='GOLD',nameKey='LOC_DISTRICT_HARBOR_NAME'}}
local function finite(n)return type(n)=='number' and n==n and n>=0 and n<math.huge end
function M.Layout(selected,workers,active,localDomains)
 assert(type(selected)=='table' and finite(workers) and workers%1==0,'COMMERCE_CAPACITY_UNKNOWN')
 local chosen,effective,used={},{},0
 for i,id in ipairs(selected)do
  assert(not chosen[id],'COMMERCE_SELECTION_INVALID');chosen[id]=i
  if active>=3 and localDomains[id]~=nil and used<workers then effective[id]=true;used=used+1 end
 end
 local rows={}
 for _,def in ipairs(M.Domains)do
  local depth=localDomains[def.id]
  assert(depth==nil or finite(depth) and depth<=10 and depth%1==0,'COMMERCE_DEPTH_UNKNOWN')
  local selectedHere=chosen[def.id]~=nil;local enabled=effective[def.id]==true
  local reason=not selectedHere and 'COMMERCE_NOT_SELECTED' or depth==nil and 'COMMERCE_LOCAL_DISTRICT_REQUIRED'
   or active<3 and 'COMMERCE_ACTIVE_III_REQUIRED' or not enabled and 'COMMERCE_CAPACITY' or 'COMMERCE_EFFECTIVE'
  rows[#rows+1]={id=def.id,nameKey=def.nameKey,yield=def.yield,localD=depth or 0,eligible=depth~=nil,
   selected=selectedHere,effective=enabled,suspended=selectedHere and not enabled,reason=reason,raw=0,gold=0,floor=0}
 end
 return rows
end
function M.Finish(rows,sources,reputation)
 assert(finite(reputation) and reputation%1==0 and reputation<=40,'COMMERCE_REPUTATION_UNKNOWN')
 local raw,total=0,0
 for _,r in ipairs(rows)do
  if r.effective then
   local s=assert(sources[r.id],'COMMERCE_SOURCE_UNKNOWN')
   assert(finite(s.X) and type(s.city)=='number','COMMERCE_SOURCE_UNKNOWN')
   r.X=s.X;r.source=s.city;r.sourceCity=s.city;r.sourceOwner=s.owner;r.sourceName=s.name
   -- Exact algebraic coefficients: .05*(1+.005R)=(200+R)/4000.
   -- Multiply before division, without epsilon or source-value quantization.
   r.raw=r.localD*s.X*(200+reputation)/4000
   assert(finite(r.raw),'COMMERCE_VALUE_UNKNOWN')
   -- Explicit user decision: Floor each domain, then sum, never merge first.
   r.gold=math.floor(r.raw);r.floor=r.gold;raw=raw+r.raw;total=total+r.gold
  end
 end
 assert(total<=2147483647,'COMMERCE_ENCODING_RANGE') -- exact representability; never clamp
 return {domains=rows,totalRaw=raw,totalGold=total}
end
