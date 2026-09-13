-- Serializable intent/readonly recovery model, not registered with Civ VI.
local M={}
local function clone(v,depth)
 depth=depth or 0;assert(depth<12,"DEPTH_LIMIT")
 local t=type(v)
 if t=="table" then
  assert(getmetatable(v)==nil,"PLAIN_RECORD_REQUIRED")
  local r={};for k,x in pairs(v) do assert(type(k)=="string","STRING_KEYS_REQUIRED");r[k]=clone(x,depth+1) end;return r
 end
 assert(t=="nil" or t=="string" or t=="boolean" or (t=="number" and v==v and math.abs(v)<math.huge),"SERIALIZABLE_SCALAR_REQUIRED")
 return v
end
local function equal(a,b)
 if type(a)~=type(b) then return false end
 if type(a)~="table" then return a==b end
 for k,v in pairs(a) do if not equal(v,b[k]) then return false end end
 for k in pairs(b) do if a[k]==nil then return false end end;return true
end
local function uid(v) return type(v)=="string" and #v>0 end
local function integer(v) return type(v)=="number" and v>=0 and v<math.huge and v%1==0 end
local function validate(r)
 assert(r.schema==1 and r.kind=="MOCK_CITY_PENDING" and r.state=="PENDING","PENDING_SCHEMA_REQUIRED")
 assert(uid(r.operationID) and uid(r.cityUID) and integer(r.owner),"IDENTITY_REQUIRED")
 assert(type(r.beforePresent)=="boolean" and type(r.target)=="table","FACT_ENVELOPE_REQUIRED")
 assert((r.beforePresent and type(r.before)=="table") or (not r.beforePresent and r.before==nil),"BEFORE_PRESENCE_CONFLICT")
 assert(r.target.cityUID==r.cityUID and r.target.owner==r.owner and integer(r.target.revision),"TARGET_IDENTITY_REQUIRED")
 if r.beforePresent then
  assert(r.before.cityUID==r.cityUID and r.before.owner==r.owner and integer(r.before.revision),"BEFORE_IDENTITY_REQUIRED")
  assert(r.target.revision==r.before.revision+1,"REVISION_STEP_REQUIRED")
 else assert(r.target.revision==0,"INITIAL_REVISION_REQUIRED") end
end
function M.Create(operationID,before,target,context)
 local ok,r=pcall(function()
  assert(context=="MOCK_ONLY","OFFLINE_ONLY")
  local out={schema=1,kind="MOCK_CITY_PENDING",state="PENDING",operationID=operationID,
   cityUID=target.cityUID,owner=target.owner,beforePresent=before~=nil,before=clone(before),target=clone(target)}
  validate(out);return out
 end)
 return ok and {status="RECORD_PLAN_ONLY",record=r} or {status="UNKNOWN",reason=tostring(r)}
end
function M.Inspect(record,observation,context)
 local ok,r=pcall(function()
  assert(context=="MOCK_ONLY","OFFLINE_ONLY")
  local saved=clone(record);assert(type(saved)=="table","PENDING_RECORD_REQUIRED");validate(saved)
  assert(type(observation)=="table" and observation.contextSource=="MOCK_ONLY" and observation.status=="READ_OK","READ_UNCONFIRMED")
  assert(observation.present==true and observation.cityUID==saved.cityUID and observation.owner==saved.owner,"SAME_CITY_REQUIRED")
  local actual=clone(observation.facts)
  local comparison=equal(actual,saved.target) and "TARGET_OBSERVED"
   or (equal(actual,saved.before) and "BEFORE_OBSERVED" or "CONFLICT_OBSERVED")
  return {status="RECOVERY_HELD",comparison=comparison,operationID=saved.operationID,
   mayWrite=false,mayActivate=false,mayClearRecord=false}
 end)
 if ok then return r end
 return {status="RECOVERY_HELD",comparison="UNKNOWN",reason=tostring(r),mayWrite=false,mayActivate=false,mayClearRecord=false}
end
function M.ClosePlan(record,observation,context)
 local r=M.Inspect(record,observation,context)
 if r.comparison~="TARGET_OBSERVED" then return r end
 local done=clone(record);done.state="DONE"
 return {status="DONE_PLAN_ONLY",record=done}
end
function M.InspectDone(record,observation,context)
 if type(record)~="table" or record.state~="DONE" then return {status="RECOVERY_HELD"} end
 local ok,p=pcall(clone,record)
 if not ok then return {status="RECOVERY_HELD"} end
 p.state="PENDING"
 local r=M.Inspect(p,observation,context)
 return {status=r.comparison=="TARGET_OBSERVED" and "DONE_MATCHED" or "RECOVERY_HELD",comparison=r.comparison}
end
return M
