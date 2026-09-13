-- Offline-only executor over an injected store/unit adapter. Not registered in Civ VI.
-- CitySpecializationState remains the authoritative offline rule reducer.
local M={}
local function copy(v) if type(v)~='table' then return v end;local r={};for k,x in pairs(v) do r[k]=copy(x) end;return r end
local function same(a,b)
 if type(a)~=type(b) then return false end
 if type(a)~='table' then return a==b end
 for k,v in pairs(a) do if not same(v,b[k]) then return false end end
 for k in pairs(b) do if a[k]==nil then return false end end;return true
end
function M.New(rules,io)
 local busy,halted=false,false
 local function ready(result) assert(result.status=='READY',result.reason or result.status);return result end
 local function write(old,nextValue)
  assert(not halted,'REENTRANT_HELD')
  assert(same(io.read(),old),'STALE_STORE')
  io.write(copy(nextValue))
  assert(not halted and same(io.read(),nextValue),'WRITE_UNCONFIRMED')
 end
 local function finish(state,id)
  local op=state.pending;assert(op and op.stage=='CONSUMED_CONFIRMED','CONSUMPTION_PROOF_REQUIRED')
  assert(op.owner==id.owner and op.cityUID==id.cityUID,'PENDING_IDENTITY_CHANGED')
  -- Do not issue another unit deletion on recovery.
  assert(io.presence(op.unitUID)=='ABSENT','CONSUMED_UNIT_REAPPEARED_OR_UNKNOWN')
  local nextFacts=ready(rules.CommitInvestment(state.facts,id,{
   contextSource='MOCK_ONLY',status='COMMITTED',cityUID=op.cityUID,owner=op.owner,
   unitType='SETTLER',unitConsumed=true,unitUID=op.unitUID,id=op.receipt,
   expectedRevision=op.expectedRevision})).facts
  local target={schema=1,facts=nextFacts};write(state,target)
  return {status='READY',changed=true,potential=nextFacts.potential}
 end
 local function guard(fn)
  if busy then halted=true;return {status='HELD',reason='REENTRANT_HELD'} end
  if halted then return {status='HELD',reason='EXECUTOR_HALTED'} end
  busy=true;local ok,out=pcall(fn);busy=false
  if not ok then halted=true;return {status='HELD',reason=tostring(out)} end
  return out
 end
 local function stateFor(id)
  assert(id.contextSource=='MOCK_ONLY','OFFLINE_ONLY')
  local s=io.read();assert(type(s)=='table' and s.schema==1,'STORE_REQUIRED')
  ready(rules.Restore(s.facts,id));return s
 end
 local obj={}
 function obj.Run(id,unit,receipt)
  return guard(function()
   assert(type(receipt)=='string' and #receipt>0,'RECEIPT_REQUIRED')
   local state=stateFor(id)
   assert(not state.pending,'PENDING_HELD')
   local previous=state.facts.investments[receipt]
   if previous then
    assert(previous==unit.unitUID,'RECEIPT_CONFLICT')
    return {status='READY',changed=false,potential=state.facts.potential}
   end
   -- Invalid input/cap/disabled are clean rejection before any write or debit.
   local plan=rules.PlanInvestment(state.facts,id,unit)
   if plan.status~='READY' then return {status='REJECTED',reason=plan.reason or plan.status} end
   assert(io.presence(unit.unitUID)=='PRESENT','UNIT_NOT_CONFIRMED_PRESENT')
   local pending=copy(state);pending.pending={stage='INTENT',receipt=receipt,unitUID=unit.unitUID,
    owner=id.owner,cityUID=id.cityUID,expectedRevision=plan.expectedRevision}
   write(state,pending)
   -- Adapter must recheck the same owner, unit generation and location at debit.
   assert(io.validate(unit,id)==true and not halted,'UNIT_CHANGED_BEFORE_DEBIT')
   io.consume(unit,id)
   assert(not halted and io.presence(unit.unitUID)=='ABSENT','CONSUMPTION_UNCONFIRMED')
   local confirmed=copy(pending);confirmed.pending.stage='CONSUMED_CONFIRMED'
   write(pending,confirmed)
   return finish(confirmed,id)
  end)
 end
 function obj.Resume(id)
  return guard(function()
   local state=stateFor(id)
   if not state.pending then return {status='READY',changed=false,potential=state.facts.potential} end
   -- Missing unit alone is not proof that THIS operation consumed it.
   assert(state.pending.stage=='CONSUMED_CONFIRMED','INTENT_REQUIRES_REVIEW_NO_AUTORETRY')
   return finish(state,id)
  end)
 end
 return obj
end
return M
