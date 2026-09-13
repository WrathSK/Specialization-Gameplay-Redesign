-- MOCK_ONLY ordered flow. No native hook, persistent-history claim or load adoption.
local M={}
function M.New(d,context)
 assert(context=="MOCK_ONLY","OFFLINE_ONLY")
 local F={};local phase="LOADING";local busy=false;local halted=false;local channels={};local serial=0
 function F.Ready(hooks)
  assert(phase=="LOADING" and hooks.fresh==true and hooks.complete==true,"LISTENERS_REQUIRED")
  phase="LIVE"
 end
 function F.Close() halted=true;phase="CLOSED" end
 local function execute(pid,fn)
  if phase~="LIVE" then return {status="IGNORED_PHASE"} end
  if busy then halted=true;return {status="HELD",reason="REENTRANT_DELIVERY"} end
  if halted then return {status="HELD",reason="HISTORY_UNCERTAIN"} end
  local permit=d.life.Acquire(pid)
  if not permit then
   -- Never mutate dormant facts. Conservatively stop this candidate stream.
   halted=true;return {status="HELD",reason="NO_PERMISSION"}
  end
  busy=true
  local function check() assert(not halted and d.life.Check(permit,pid),"DELIVERY_PERMISSION_OR_HISTORY_CHANGED") end
  local ok,r=pcall(function() check();return fn(check) end)
  busy=false
  if not ok or halted then halted=true;return {status="HELD",reason=tostring(ok and "REENTRANT_DELIVERY" or r)} end
  return r
 end
 local function submit(c,action,op,batch)
  local p=c.gate.Prepare(action,c.owner,c.reference,{contextSource=context,phase="AFTER_LOAD_CLOSE"},batch)
  if p.status=="READY" then return {status="NO_WRITE"} end
  assert(p.status=="PLAN_ONLY","PLAN_NOT_CONFIRMED")
  local r=c.gate.CommitRecordedMock(p.handle,op,c.writeFacts)
  assert(r.status=="TARGET_OBSERVED_PENDING","SUBMISSION_UNCERTAIN")
  assert(c.gate.ResolveRecordedMock(c.reference,{contextSource=context,phase="AFTER_LOAD_CLOSE"}).status=="DONE_CONFIRMED_MOCK","DONE_UNCONFIRMED")
  return {status="COMMITTED_MOCK"}
 end
 local function fresh(pid,cid,provided)
  return execute(pid,function(check)
   -- Keep existing legacy processing first. A nil return is NOT success evidence.
   local e=provided
   if e==nil then d.legacy(pid,cid);check();e=d.inspectFresh(pid,cid) end
   check()
   assert(type(e)=="table" and e.owner==pid and e.cityID==cid and type(e.token)=="string","FRESH_IDENTITY_REQUIRED")
   assert(e.legacyHealth=="TRACKING","LEGACY_RESULT_NOT_CONFIRMED")
   local c=channels[e.token]
   if c then assert(c.owner==pid and c.cityID==cid,"TOKEN_COLLISION");return {status="DUPLICATE_NO_WRITE"} end
   assert(e.contextSource==context and e.bindingValidated==true and e.foundationObserved==true
    and e.scanStatus=="COMPLETE" and e.centerComplete==true and e.completedV01Count==0,"FRESH_HISTORY_REQUIRED")
   local proof={contextSource=context,status="FRESH_BOUND_HISTORY_COMPLETE",owner=pid,cityID=cid,token=e.token}
   c=d.open(pid,cid,e.token,proof);check();c.owner=pid;c.cityID=cid
   serial=serial+1;local result=submit(c,"FOUNDATION","foundation:"..serial)
   check();channels[e.token]=c;return result
  end)
 end
 function F.Fresh(pid,cid) return fresh(pid,cid,nil) end
 -- Verified after-legacy adapter entry; never invoke legacy twice.
 function F.AfterLegacy(pid,cid,evidence)
  if type(evidence)~="table" then return {status="HELD",reason="EVIDENCE_REQUIRED"} end
  return fresh(pid,cid,evidence)
 end
 function F.Complete(pid,raw)
  return execute(pid,function(check)
   local e=d.inspectComplete(pid,raw);check()
   assert(type(e)=="table" and e.status=="VALIDATED" and e.owner==pid,"EVENT_UNVERIFIED")
   if e.family=="NON_V01" then return {status="IGNORED_NON_V01"} end
   assert(e.complete==true and e.mappingStatus=="VALIDATED_FAMILY","INVALID_COMPLETION")
   local c=channels[e.token]
   if not c then return {status="UNTRACKED_NO_WRITE"} end
   assert(c.owner==pid and c.cityID==e.cityID,"EVENT_CITY_MISMATCH")
   serial=serial+1
   local batch={status="COMPLETE_ORDERED_BATCH",orderBasis="ENGINE_DELIVERY",owner=pid,cityUID=e.token,
    eventID="delivery:"..serial,districts={{family=e.family,complete=true,districtUID=e.districtUID,mappingStatus=e.mappingStatus}}}
   local result=submit(c,"COMPLETION_BATCH","complete:"..serial,batch);check();return result
  end)
 end
 return F
end
return M
