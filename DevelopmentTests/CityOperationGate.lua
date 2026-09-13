-- MOCK_ONLY preparation/commit experiment. Injected mock writer only; no engine API.
local M={}
local function copy(x,depth)
 depth=depth or 0;assert(depth<12,"FACT_DEPTH")
 if type(x)~="table" then assert(type(x)~="function" and type(x)~="userdata","SCALAR_FACTS");return x end
 local out={};for k,v in pairs(x) do assert(type(k)=="string" or type(k)=="number","FACT_KEY");out[k]=copy(v,depth+1) end;return out
end
local function same(a,b)
 if type(a)~=type(b) then return false end
 if type(a)~="table" then return a==b end
 for k,v in pairs(a) do if not same(v,b[k]) then return false end end
 for k in pairs(b) do if a[k]==nil then return false end end;return true
end
local function guarded(fn)
 local ok,r=pcall(fn);if ok then return r end;return {status="UNKNOWN",reason=tostring(r)}
end
function M.New(life,planner,resolve,context,recovery)
 assert(context=="MOCK_ONLY","OFFLINE_ONLY")
 local pending={};local G={}
 local busy,halted=false,false
 local acceptedDone=nil
 local reentry=0
 local function available()
  if busy then reentry=reentry+1;halted=true;error("REENTRANT_SESSION_STOP") end
  assert(not halted,"SESSION_HALTED")
  if recovery then
   local ok,s=pcall(recovery.read)
   if not ok or type(s)~="table" or s.status~="READ_OK" or (s.record~=nil and not (acceptedDone and same(s.record,acceptedDone))) then
    halted=true;error("RECOVERY_STORE_NOT_CLEAR")
   end
  end
 end
 local function current(pid,ref,permit)
  assert(life.Check(permit,pid),"NO_CURRENT_PERMISSION") -- before any city read
  local observed=resolve(ref)
  assert(life.Check(permit,pid),"PERMISSION_CHANGED_DURING_READ")
  assert(type(observed)=="table" and type(observed.id)=="table","CITY_READ_FAILED")
  local id=copy(observed.id)
  assert(id.contextSource=="MOCK_ONLY" and id.owner==pid and id.present==true
   and type(id.cityUID)=="string" and #id.cityUID>0,"CITY_IDENTITY_UNCONFIRMED")
  id.eligibility={contextSource="MOCK_ONLY",player=pid,status="ENABLED"}
  return id,copy(observed.facts)
 end
 function G.Prepare(action,pid,ref,ctx,batch)
  return guarded(function()
   available()
   assert(type(ctx)=="table" and ctx.contextSource=="MOCK_ONLY" and ctx.phase=="AFTER_LOAD_CLOSE","LIVE_PHASE_REQUIRED")
   assert(action=="FOUNDATION" or action=="COMPLETION_BATCH","MUTATION_PLAN_ONLY")
   local permit=life.Acquire(pid);assert(permit,"NO_CURRENT_PERMISSION")
   local id,facts=current(pid,ref,permit)
   if acceptedDone then
    assert(id.cityUID==acceptedDone.cityUID and id.owner==acceptedDone.owner and same(facts,acceptedDone.target),"DONE_FACTS_CHANGED")
   end
   local plan=planner.Plan(action,copy(facts),copy(id),ctx,batch)
   assert(life.Check(permit,pid),"PERMISSION_CHANGED_DURING_PLAN")
   if plan.status~="PLAN_ONLY" then return copy(plan) end
   local handle={}
   pending[handle]={permit=permit,pid=pid,ref=ref,id=id,facts=facts,plan=copy(plan)}
   return {status="PLAN_ONLY",handle=handle} -- contents private; caller cannot alter proposed facts
  end)
 end
 local function consume(handle)
  available()
  local p=pending[handle];assert(p,"UNKNOWN_OR_USED_PLAN")
  pending[handle]=nil
  local id,facts=current(p.pid,p.ref,p.permit)
  assert(id.cityUID==p.id.cityUID,"CITY_GENERATION_CHANGED")
  assert(same(id,p.id),"CITY_EVIDENCE_CHANGED")
  assert(same(facts,p.facts),"PERMANENT_FACTS_CHANGED")
  assert(life.Check(p.permit,p.pid),"PERMISSION_EXPIRED")
  return p
 end
 function G.CheckForCommit(handle)
  return guarded(function()
   local p=consume(handle)
   return {status="CHECKED_PLAN_ONLY",plan=copy(p.plan),requires="ENGINE_COMMIT_BOUNDARY_AND_READBACK"}
  end)
 end
 local function commit(handle,write,operationID)
  local entered=false
  local ok,result=pcall(function()
   assert(type(write)=="function","MOCK_WRITER_REQUIRED")
   local p=consume(handle)
   busy=true;entered=true
   local target=copy(p.plan.proposedFacts)
   if recovery then
    assert(not acceptedDone or operationID~=acceptedDone.operationID,"LAST_OPERATION_ID_REUSED")
    local made=recovery.model.Create(operationID,p.facts,target,"MOCK_ONLY")
    assert(made.status=="RECORD_PLAN_ONLY","RECOVERY_RECORD_INVALID")
    -- A failed save call can have written: exact readback decides, never retry.
    pcall(recovery.write,copy(made.record))
    local saved=recovery.read()
    assert(type(saved)=="table" and saved.status=="READ_OK" and same(saved.record,made.record),"INTENT_SAVE_UNCONFIRMED")
    -- Storage callbacks may have changed permission, city or facts. Recheck them.
    local id,facts=current(p.pid,p.ref,p.permit)
    assert(not halted and same(id,p.id) and same(facts,p.facts),"CHANGED_AFTER_INTENT")
    local final=recovery.read()
    assert(type(final)=="table" and final.status=="READ_OK" and same(final.record,made.record),"INTENT_CHANGED")
    assert(not halted and life.Check(p.permit,p.pid),"PERMISSION_CHANGED_AFTER_INTENT")
   end
   local called,err=pcall(write,p.pid,p.ref,copy(target)) -- exactly one attempt, never retry
   -- Readback is reconciliation, permitted even if running permission was revoked.
   -- It must not activate effects and must still prove the same owner/city identity.
   local observed=resolve(p.ref)
   assert(type(observed)=="table" and type(observed.id)=="table","READBACK_FAILED")
   local id=copy(observed.id);id.eligibility=copy(p.id.eligibility)
   assert(same(id,p.id),"READBACK_IDENTITY_CHANGED")
   local actual=copy(observed.facts)
   if same(actual,target) then
    if halted or not life.Check(p.permit,p.pid) then
     halted=true
     return {status="TARGET_OBSERVED_HALTED",writerReturned=called,reason="PERMISSION_LOST_OR_REENTRANT"}
    end
    if recovery then
     halted=true -- pending stays until a separate, explicit resolution protocol exists
     return {status="TARGET_OBSERVED_PENDING",writerReturned=called,mayResume=false}
    end
    return {status="COMMITTED_MOCK",writerReturned=called,writerError=not called and tostring(err) or nil}
   end
   halted=true
   return {status=same(actual,p.facts) and "OLD_VALUE_OBSERVED_HALTED" or "CONFLICT_OBSERVED_HALTED",
    writerReturned=called,reason="NO_RETRY_OR_ROLLBACK"}
  end)
  if entered then busy=false end
  if ok then return result end
  if entered then halted=true end
  return {status=entered and "WRITE_OUTCOME_UNKNOWN_HALTED" or "REJECTED_BEFORE_WRITE",reason=tostring(result)}
 end

 -- Explicit reconciliation. No city writer and no automatic PENDING deletion.
 function G.ResolveRecordedMock(ref,ctx)
  local entered=false
  local ok,result=pcall(function()
   assert(recovery and type(ctx)=="table" and ctx.contextSource=="MOCK_ONLY" and ctx.phase=="AFTER_LOAD_CLOSE","RECOVERY_PHASE_REQUIRED")
   if busy then reentry=reentry+1;halted=true;error("REENTRANT_SESSION_STOP") end
   busy=true;entered=true;halted=true
   local initialReentry=reentry
   local saved=recovery.read();assert(saved.status=="READ_OK" and type(saved.record)=="table","RECORD_REQUIRED")
   local record=copy(saved.record)
   local permit=life.Acquire(record.owner);assert(permit,"NO_CURRENT_PERMISSION")
   local function observe()
    local id,facts=current(record.owner,ref,permit)
    return {contextSource="MOCK_ONLY",status="READ_OK",present=id.present,cityUID=id.cityUID,owner=id.owner,facts=facts}
   end
   local done
   if record.state=="DONE" then
    assert(recovery.model.InspectDone(record,observe(),"MOCK_ONLY").status=="DONE_MATCHED","DONE_MISMATCH")
    done=record
   else
    local plan=recovery.model.ClosePlan(record,observe(),"MOCK_ONLY")
    assert(plan.status=="DONE_PLAN_ONLY","PENDING_NOT_RESOLVED")
    local check=recovery.read();assert(check.status=="READ_OK" and same(check.record,record),"RECOVERY_RECORD_CHANGED")
    assert(life.Check(permit,record.owner),"RECOVERY_PERMISSION_CHANGED")
    done=plan.record;pcall(recovery.write,copy(done))
   end
   local final=recovery.read();assert(final.status=="READ_OK" and same(final.record,done),"DONE_SAVE_UNCONFIRMED")
   assert(recovery.model.InspectDone(done,observe(),"MOCK_ONLY").status=="DONE_MATCHED","DONE_FINAL_MISMATCH")
   assert(life.Check(permit,record.owner),"RECOVERY_PERMISSION_CHANGED")
   assert(reentry==initialReentry,"RECOVERY_REENTRANT_STOP")
   acceptedDone=copy(done);pending={};halted=false
   return {status="DONE_CONFIRMED_MOCK",mayPrepare=true}
  end)
  if entered then busy=false end
  if ok then return result end
  return {status="RECOVERY_HELD",reason=tostring(result)}
 end
 function G.CommitMock(handle,write)
  if recovery then return {status="REJECTED_BEFORE_WRITE",reason="RECORDED_ENTRY_REQUIRED"} end
  return commit(handle,write)
 end
 function G.CommitRecordedMock(handle,operationID,write)
  if not recovery then return {status="REJECTED_BEFORE_WRITE",reason="RECOVERY_STORE_REQUIRED"} end
  return commit(handle,write,operationID)
 end
 return G
end
return M
