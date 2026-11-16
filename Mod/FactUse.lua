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
function M.Qualification(f,identity,minimum)
 if type(f)~='table'or type(f.specialization)~='string'then return unknown('IDENTITY_UNAVAILABLE')end
 if f.specialization~=identity then return absent('IDENTITY_REQUIRED')end
 if f.activeStatus~='KNOWN'or f.investmentPending or not finite(f.active)or f.active%1~=0 or f.active>4 then return unknown('ACTIVE_UNAVAILABLE')end
 if f.active<minimum then return absent('ACTIVE_REQUIRED')end
 return confirmed(f.active)
end
function M.Depth(snapshot,domain)
 if not ready(snapshot)or type(snapshot.value.domains)~='table'then return unknown('DISTRICT_FACTS_UNAVAILABLE')end
 local row=snapshot.value.domains[domain]
 if row==nil then return absent('LOCAL_DISTRICT_REQUIRED')end
 if type(row)~='table'or not finite(row.value)or row.value%1~=0 then return unknown('DISTRICT_DEPTH_UNAVAILABLE')end
 return confirmed(row.value)
end
function M.Anchor(snapshot,first)
 if not ready(snapshot)or type(snapshot.value.districts)~='table'or type(first)~='table'then return unknown('ANCHOR_UNAVAILABLE')end
 for _,row in ipairs(snapshot.value.districts)do
  if row.id==first.districtID and row.type==first.type then
   if type(row.complete)~='boolean'or type(row.pillaged)~='boolean'or not finite(row.id)or row.id%1~=0
    or not finite(row.plot)or row.plot%1~=0 then return unknown('ANCHOR_UNAVAILABLE')end
   return confirmed({id=row.id,type=row.type,plot=row.plot,complete=row.complete,pillaged=row.pillaged})
  end
 end
 -- Missing anchor alone does not decide a historical identity's lifecycle.
 return unknown('ANCHOR_UNAVAILABLE')
end
