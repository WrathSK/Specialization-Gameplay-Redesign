-- MOCK_ONLY identity allocation experiment. Not loaded by modinfo.
-- A single envelope couples the allocator and its identity records.
-- Instance proof is a fixture prerequisite, NOT a discovered engine UID API.
local M={}
local function copy(v)
 if type(v)~="table" then return v end
 local out={};for k,x in pairs(v) do out[k]=copy(x) end;return out
end
local function equal(a,b)
 if type(a)~=type(b) then return false end
 if type(a)~="table" then return a==b end
 for k,v in pairs(a) do if not equal(v,b[k]) then return false end end
 for k in pairs(b) do if a[k]==nil then return false end end
 return true
end
local function int(n) return type(n)=="number" and n>=0 and n%1==0 and n<9007199254740991 end
local function text(s) return type(s)=="string" and #s>0 end
local function valid(v)
 if type(v)~="table" or v.schema~=1 or not int(v.counter) or not int(v.revision)
  or type(v.records)~="table" then return false end
 local seen,instances={},{};local count=0
 for key,r in pairs(v.records) do
  if type(r)~="table" or not int(r.owner) or not int(r.cityID) or not text(r.instanceProof)
   or not int(r.serial) or r.serial<1 or r.serial>v.counter or seen[r.serial] or instances[r.instanceProof]
   or key~=r.owner..":"..r.cityID or r.uid~="SPC-CITY-"..r.serial then return false end
  seen[r.serial]=true;instances[r.instanceProof]=true;count=count+1
 end
 return count==v.counter and v.revision==v.counter
end
function M.New(storage,context)
 local busy=false
 local function result(status,reason) return {status=status,reason=reason} end
 local function read()
  local ok,v=pcall(storage.Read)
  if not ok then return false,nil end
  -- Copy before any edits: Property implementations may return shared tables.
  if v~=nil and not valid(v) then return false,nil end
  return true,copy(v)
 end
 local function ensure(ref,proof)
  if context~="MOCK_ONLY" then return result("UNKNOWN","OFFLINE_ONLY") end
  if type(ref)~="table" or not int(ref.owner) or not int(ref.cityID)
   or type(proof)~="table" or proof.isTestCivilization~=true or proof.present~=true
   or proof.validatedInstance~=true or not text(proof.instanceProof) then
   return result("UNKNOWN","VALIDATED_INSTANCE_REQUIRED")
  end
  local ok,old=read();if not ok then return result("UNKNOWN","READ_OR_SCHEMA_FAILURE") end
  if old==nil and proof.registryBootstrapConfirmed~=true then
   return result("UNKNOWN","EMPTY_REGISTRY_NOT_PROVEN_NEW")
  end
  local key=ref.owner..":"..ref.cityID
  local existing=old and old.records[key]
  if existing then
   if existing.instanceProof~=proof.instanceProof then return result("UNKNOWN","INSTANCE_REUSE_UNRESOLVED") end
   return {status="READY",uid=existing.uid,changed=false}
  end
  for _,record in pairs(old and old.records or {}) do
   if record.instanceProof==proof.instanceProof then
    return result("DESIGN_DECISION_REQUIRED","CHANGED_REFERENCE_OR_OWNERSHIP_OPEN_04")
   end
  end
  if proof.freshFoundationObserved~=true or proof.phase~="AFTER_LOAD_CLOSE" then
   return result("DESIGN_DECISION_REQUIRED","MISSING_IDENTITY_OPEN_04")
  end
  local next=copy(old or {schema=1,counter=0,revision=0,records={}})
  next.counter=next.counter+1;next.revision=next.revision+1
  local uid="SPC-CITY-"..next.counter
  next.records[key]={owner=ref.owner,cityID=ref.cityID,instanceProof=proof.instanceProof,serial=next.counter,uid=uid}
  if not valid(next) then return result("UNKNOWN","ALLOCATION_LIMIT") end
  local before,current=read()
  if not before then return result("UNKNOWN","PREWRITE_READ_FAILURE") end
  if not equal(old,current) then return result("UNKNOWN","STALE_PLAN") end
  -- No blind retry: the setter can throw after it has already written.
  local writeOK=pcall(storage.Write,copy(next))
  local after,stored=read()
  if not after then return result("UNKNOWN","WRITE_OUTCOME_UNCONFIRMED") end
  if equal(stored,next) then
   return {status="READY",uid=uid,changed=true,writeAcknowledged=writeOK}
  end
  if equal(stored,old) then return result("NOT_COMMITTED","UNCHANGED_READBACK") end
  return result("UNKNOWN","WRITE_OUTCOME_CONFLICT")
 end
 return {Ensure=function(ref,proof)
  if busy then return result("UNKNOWN","REENTRANT_CALL") end
  busy=true;local ok,r=pcall(ensure,ref,proof);busy=false
  if not ok then return result("UNKNOWN","MALFORMED_INPUT") end
  return r
 end}
end
return M
