-- MOCK_ONLY single-city storage adapter. No Civ VI API or crash-atomicity claim.
local M={}
local function copy(v,d)
 d=d or 0;assert(d<16,"DEPTH_LIMIT")
 if type(v)=="table" then
  assert(getmetatable(v)==nil,"PLAIN_TABLE_REQUIRED")
  local out={};for k,x in pairs(v) do assert(type(k)=="string","STRING_KEYS_REQUIRED");out[k]=copy(x,d+1) end;return out
 end
 assert(v==nil or type(v)=="boolean" or type(v)=="string" or (type(v)=="number" and v==v and math.abs(v)<math.huge),"SERIALIZABLE_REQUIRED")
 return v
end
local function same(a,b)
 if type(a)~=type(b) then return false end
 if type(a)~="table" then return a==b end
 for k,v in pairs(a) do if not same(v,b[k]) then return false end end
 for k in pairs(b) do if a[k]==nil then return false end end;return true
end
function M.New(store,model,identity,context)
 assert(context=="MOCK_ONLY","OFFLINE_ONLY")
 local A={};local busy=false
 local function id()
  local i=copy(identity())
  assert(i.contextSource=="MOCK_ONLY" and i.present==true and type(i.cityUID)=="string" and #i.cityUID>0,"IDENTITY_REQUIRED")
  assert(type(i.owner)=="number" and i.owner>=0 and i.owner%1==0,"OWNER_REQUIRED")
  return i
 end
 local function observation(i,f)
  return {contextSource="MOCK_ONLY",status="READ_OK",present=true,cityUID=i.cityUID,owner=i.owner,facts=f}
 end
 local function read()
  local i=id();local r=store.read();assert(r.status=="READ_OK","STORE_READ_FAILED")
  local e=copy(r.value)
  if e==nil then
   assert(i.freshFoundationObserved==true,"EMPTY_NOT_NEW_CITY_PROOF")
   return nil,i
  end
  assert(type(e)=="table" and e.schema==1 and e.kind=="MOCK_CITY_ENVELOPE","ENVELOPE_SCHEMA")
  for k in pairs(e) do assert(k=="schema" or k=="kind" or k=="owner" or k=="cityUID" or k=="storageRevision" or k=="facts" or k=="record","UNKNOWN_FIELD") end
  assert(e.owner==i.owner and e.cityUID==i.cityUID,"ENVELOPE_IDENTITY")
  assert(type(e.storageRevision)=="number" and e.storageRevision>=1 and e.storageRevision<2^53 and e.storageRevision%1==0,"STORAGE_REVISION")
  assert(type(e.record)=="table","RECORD_REQUIRED")
  local o=observation(i,e.facts)
  if e.record.state=="DONE" then
   assert(model.InspectDone(e.record,o,context).status=="DONE_MATCHED","DONE_FACTS_MISMATCH")
  else
   local v=model.Inspect(e.record,o,context)
   assert(v.comparison=="BEFORE_OBSERVED" or v.comparison=="TARGET_OBSERVED","PENDING_FACTS_MISMATCH")
  end
  return e,i
 end
 local function replace(before,target)
  assert(not busy,"STORAGE_REENTRY");busy=true
  local ok,err=pcall(function()
   local current=read();assert(same(current,before),"ENVELOPE_CHANGED")
   -- One whole-table attempt. A throwing setter may have written; never retry.
   local called,why=pcall(store.write,copy(target))
   local actual=read();assert(same(actual,target),"ENVELOPE_READBACK_MISMATCH:"..tostring(called)..":"..tostring(why))
  end)
  busy=false;assert(ok,err)
 end
 function A.ReadRecord()
  local ok,e=pcall(read)
  if not ok then return {status="UNKNOWN",reason=tostring(e)} end
  return {status="READ_OK",record=e and copy(e.record) or nil}
 end
 function A.Resolve()
  local e,i=read();return {id=i,facts=e and copy(e.facts) or nil}
 end
 function A.WriteRecord(record)
  assert(not busy,"STORAGE_REENTRY")
  local before,i=read();local f=before and before.facts or nil
  local next=before and copy(before) or {schema=1,kind="MOCK_CITY_ENVELOPE",cityUID=i.cityUID,owner=i.owner,storageRevision=0}
  if record.state=="PENDING" then
   assert(not before or before.record.state=="DONE","PENDING_ALREADY_EXISTS")
   assert(not before or record.operationID~=before.record.operationID,"LAST_OPERATION_ID_REUSED")
   assert(model.Inspect(record,observation(i,f),context).comparison=="BEFORE_OBSERVED","BEGIN_BEFORE_MISMATCH")
  else
   assert(before and before.record.state=="PENDING","PENDING_REQUIRED")
   local close=model.ClosePlan(before.record,observation(i,f),context)
   assert(close.status=="DONE_PLAN_ONLY" and same(close.record,record),"CLOSE_TARGET_MISMATCH")
  end
  next.record=copy(record);next.storageRevision=next.storageRevision+1
  replace(before,next)
 end
 function A.WriteFacts(pid,ref,facts)
  assert(not busy,"STORAGE_REENTRY")
  local before,i=read()
  assert(pid==i.owner and ref==i.cityUID,"WRITE_REFERENCE_MISMATCH")
  assert(before and before.record.state=="PENDING","PENDING_REQUIRED")
  assert(model.Inspect(before.record,observation(i,before.facts),context).comparison=="BEFORE_OBSERVED","ALREADY_APPLIED_OR_CONFLICT")
  assert(same(facts,before.record.target),"ONLY_RECORDED_TARGET")
  local next=copy(before);next.facts=copy(facts);next.storageRevision=next.storageRevision+1
  replace(before,next)
 end
 return A
end
return M
