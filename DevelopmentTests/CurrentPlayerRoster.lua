-- Native API candidate; not registered with the running Mod. No persisted state.
-- Membership, qualification and historical participation are different facts.
local M={}
local function integer(n) return type(n)=="number" and n>=0 and n<math.huge and n%1==0 end
function M.Collect(env,readEligibility)
 local ok,result=pcall(function()
  assert(type(readEligibility)=="function","QUALIFICATION_READER_REQUIRED")
  local ids=env.PlayerManager.GetAliveIDs()
  assert(type(ids)=="table","ROSTER_NOT_A_TABLE")
  local length=0
  for k in pairs(ids) do assert(integer(k) and k>=1,"ROSTER_NOT_AN_ARRAY");length=length+1 end
  assert(length<=128,"ROSTER_TOO_LARGE") -- bounded candidate, not an engine slot definition
  local ordered,seen={},{}
  for i=1,length do
   local pid=ids[i];assert(integer(pid),"INVALID_OR_SPARSE_ROSTER")
   if not seen[pid] then seen[pid]=true;ordered[#ordered+1]=pid end
  end
  table.sort(ordered)
  local out={contextSource="GAMEPLAY_CANDIDATE",status="COMPLETE_ROSTER",current=seen,
   ordered=ordered,enabled={},disabled={},unknown={}}
  for _,pid in ipairs(ordered) do
   local success,e=pcall(readEligibility,pid)
   if not success or type(e)~="table" or e.player~=pid or e.contextSource~="GAMEPLAY_CANDIDATE" then
    out.unknown[pid]="QUALIFICATION_READER_FAILED_OR_MISMATCH"
   elseif e.status=="ENABLED" then out.enabled[#out.enabled+1]=pid
   elseif e.status=="DISABLED" then out.disabled[pid]=true
   else out.unknown[pid]=e.reason or "QUALIFICATION_UNKNOWN" end
  end
  return out
 end)
 if ok then return result end
 -- Never return a partially authorized list or retain earlier results on roster failure.
 return {contextSource="GAMEPLAY_CANDIDATE",status="UNKNOWN",reason=tostring(result),enabled={}}
end
function M.Classify(snapshot,pid)
 if not integer(pid) or type(snapshot)~="table" or snapshot.contextSource~="GAMEPLAY_CANDIDATE"
  or snapshot.status~="COMPLETE_ROSTER" then return "UNKNOWN" end
 if not snapshot.current[pid] then return "NOT_CURRENT" end
 if snapshot.disabled[pid] then return "DISABLED" end
 if snapshot.unknown[pid] then return "UNKNOWN" end
 for _,p in ipairs(snapshot.enabled) do if p==pid then return "ENABLED" end end
 return "UNKNOWN"
end
return M
