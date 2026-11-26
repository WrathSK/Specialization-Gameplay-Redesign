-- Detached, read-only status/use projections. No cache, scheduler or save authority.
-- Providers own observations; consumers own qualification and effect policy.
SPCFactUse={}
local M=SPCFactUse
local function confirmed(value)return {status='CONFIRMED',value=value}end
local function unknown(reason)return {status='UNKNOWN',reason=reason}end
local function absent(reason)return {status='NOT_APPLICABLE',reason=reason}end
local function finite(n)return type(n)=='number'and n==n and n>=0 and n<math.huge end
local function ready(snapshot)
 return type(snapshot)=='table'and snapshot.validity=='VERIFIED'and snapshot.availability=='READY'and type(snapshot.value)=='table'
end
function M.Number(read,integer,maximum,reason)
 local ok,value=pcall(read)
 if not ok or not finite(value)or integer and value%1~=0 or maximum and value>maximum then return unknown(reason)end
 return confirmed(value) -- confirmed zero is a value, never missing input
end
-- Inputs come from our own producers (EffectiveFacts, DistrictCompleteness). Their
-- real UNKNOWN states stay UNKNOWN; a shape violation is a bug and throws.
local function integer(n)return finite(n)and n%1==0 end
function M.Qualification(f,identity,minimum)
 assert(type(f)=='table'and type(f.specialization)=='string','FACT_USE_IDENTITY_CONTRACT')
 if f.specialization~=identity then return absent('IDENTITY_REQUIRED')end
 if f.activeStatus~='KNOWN'or f.investmentPending then return unknown('ACTIVE_UNAVAILABLE')end
 assert(integer(f.active)and f.active<=4,'FACT_USE_ACTIVE_CONTRACT')
 if f.active<minimum then return absent('ACTIVE_REQUIRED')end
 return confirmed(f.active)
end
function M.Depth(snapshot,domain)
 if not ready(snapshot)then return unknown('DISTRICT_FACTS_UNAVAILABLE')end
 local row=assert(snapshot.value.domains,'FACT_USE_DEPTH_CONTRACT')[domain]
 if row==nil then return absent('LOCAL_DISTRICT_REQUIRED')end
 if row.depthError then return unknown('DISTRICT_DEPTH_UNAVAILABLE')end -- Tier rule: an unreviewed tier is unknown
 assert(integer(row.value),'FACT_USE_DEPTH_CONTRACT')
 return confirmed(row.value)
end
function M.Anchor(snapshot,first)
 assert(type(first)=='table','FACT_USE_ANCHOR_CONTRACT')
 if not ready(snapshot)then return unknown('ANCHOR_UNAVAILABLE')end
 for _,row in ipairs(assert(snapshot.value.districts,'FACT_USE_ANCHOR_CONTRACT'))do
  if row.id==first.districtID and row.type==first.type then
   assert(type(row.complete)=='boolean'and type(row.pillaged)=='boolean'and integer(row.id)and integer(row.plot),'FACT_USE_ANCHOR_CONTRACT')
   return confirmed({id=row.id,type=row.type,plot=row.plot,complete=row.complete,pillaged=row.pillaged})
  end
 end
 -- Missing anchor alone does not decide a historical identity's lifecycle.
 return unknown('ANCHOR_UNAVAILABLE')
end
