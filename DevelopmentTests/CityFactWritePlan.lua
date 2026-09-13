-- Offline planning only. No Property writes, event registration, or UID allocation.
-- State is CitySpecializationState; callers supply validated MOCK identities/batches.
local M={}
function M.New(State)
 local planner={}
 function planner.Plan(action,saved,id,context,batch)
  if type(context)~="table" or context.contextSource~="MOCK_ONLY" then
   return {status="UNKNOWN",reason="OFFLINE_ONLY"}
  end
  -- Restoring is allowed during load, but never manufactures missing facts.
  if action=="RESTORE" then return State.Restore(saved,id) end
  if context.phase~="AFTER_LOAD_CLOSE" then
   return {status="UNKNOWN",reason="LIVE_PHASE_REQUIRED"}
  end
  local gate=State.Participation(id);if gate.status~="READY" then return gate end
  local result
  if action=="FOUNDATION" then
   -- Even a duplicate foundation notification must preserve investment/history.
   if saved~=nil then return State.Restore(saved,id) end
   result=State.NewCity(id)
  elseif action=="COMPLETION_BATCH" then
   -- This module does NOT convert individual native events into an ordered batch.
   result=State.Complete(saved,id,batch)
  else
   return {status="IGNORED",reason="NOT_A_FACT_WRITE_ACTION"}
  end
  if result.status~="READY" then return result end
  if result.changed==false then return result end
  return {status="PLAN_ONLY",cityUID=result.facts.cityUID,owner=result.facts.owner,
   expectedAbsent=saved==nil,expectedRevision=saved and saved.revision or nil,
   proposedFacts=result.facts,requires="VALIDATED_IDENTITY_AND_COMPARE_BEFORE_WRITE"}
 end
 return planner
end
return M
