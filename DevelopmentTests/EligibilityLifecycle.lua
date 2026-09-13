-- Offline authorization lifecycle only. No engine events, writes, or effect removal.
local M={}
function M.New(collect,context)
 assert(context=="MOCK_ONLY" and type(collect)=="function","OFFLINE_ONLY")
 local epoch,ready,allowed,tickets=0,false,{},{}
 local S={}
 function S.Invalidate()
  epoch=epoch+1;ready=false;allowed={};tickets={}
  return epoch
 end
 function S.Refresh(phase)
  local attempt=S.Invalidate() -- old authorizations die BEFORE any external reads
  if phase~="AFTER_LOAD_CLOSE" then return {status="UNKNOWN",reason="NOT_READY_PHASE"} end
  local ok,s=pcall(collect)
  if attempt~=epoch then return {status="UNKNOWN",reason="SUPERSEDED_REFRESH"} end
  local valid,nextAllowed=pcall(function()
   assert(ok and type(s)=="table" and s.contextSource=="GAMEPLAY_CANDIDATE"
    and s.status=="COMPLETE_ROSTER","ROSTER_UNAVAILABLE")
   assert(type(s.enabled)=="table" and type(s.current)=="table"
    and type(s.disabled)=="table" and type(s.unknown)=="table","BAD_ROSTER")
   local out={};local n=0
   for k in pairs(s.enabled) do
    assert(type(k)=="number" and k>=1 and k%1==0,"BAD_ENABLED_ARRAY");n=n+1
   end
   for i=1,n do
    local p=s.enabled[i]
    assert(type(p)=="number" and p>=0 and p<math.huge and p%1==0 and s.current[p]==true
     and not s.disabled[p] and not s.unknown[p] and not out[p],"CONFLICTING_ELIGIBILITY")
    out[p]=true
   end
   return out
  end)
  if not valid then return {status="UNKNOWN",reason=tostring(nextAllowed)} end
  if attempt~=epoch then return {status="UNKNOWN",reason="SUPERSEDED_REFRESH"} end
  allowed=nextAllowed;ready=true
  return {status="READY_OFFLINE",epoch=epoch}
 end
 function S.Acquire(player)
  if not ready or not allowed[player] then return nil end
  local token={} -- private issuance registry, not mutable public epoch fields
  tickets[token]={player=player,epoch=epoch}
  return token
 end
 function S.Check(token,player)
  local receipt=tickets[token]
  return ready and receipt~=nil and receipt.player==player and receipt.epoch==epoch and allowed[player]==true
 end
 return S
end
return M
