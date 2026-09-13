-- Offline decision table for a future ledger -> city token -> confirmation protocol.
-- This classifies recovery only; it never allocates tokens or writes Properties.
local M={}
local function out(status,reason) return {status=status,reason=reason} end
local function integer(n) return type(n)=="number" and n>=0 and n<math.huge and n%1==0 end
function M.Decide(input)
 if type(input)~="table" or input.contextSource~="MOCK_ONLY" then return out("UNKNOWN","OFFLINE_ONLY") end
 if input.readStatus~="COMPLETE" or input.registryValidated~=true or input.isTestCivilization~=true
  or input.cityPresent~=true then return out("UNKNOWN","CURRENT_VALIDATED_READ_REQUIRED") end
 if not integer(input.owner) or not integer(input.cityID) or not integer(input.x) or not integer(input.y) then
  return out("UNKNOWN","CURRENT_REFERENCE_REQUIRED")
 end
 local r,t=input.record,input.cityToken
 if r==nil and t==nil then
  if input.phase=="AFTER_LOAD_CLOSE" and input.freshFoundationObserved==true then
   return out("PLAN_RESERVATION","FRESH_FOUNDATION_ONLY")
  end
  return out("DESIGN_DECISION_REQUIRED","OLD_CITY_OPEN_04")
 end
 if r==nil or t==nil then return out("UNKNOWN","PARTIAL_BINDING_NO_AUTOFILL") end
 if type(r)~="table" or type(t)~="string" or #t==0 or type(r.uid)~="string"
  or r.uid~=t then return out("UNKNOWN","TOKEN_CONFLICT") end
 if r.owner~=input.owner then return out("DESIGN_DECISION_REQUIRED","OWNERSHIP_OPEN_04") end
 if r.cityID~=input.cityID or r.x~=input.x or r.y~=input.y then return out("UNKNOWN","REFERENCE_CONFLICT") end
 if r.state=="RESERVED" then return out("PLAN_CONFIRMATION","BOTH_SIDES_MATCH") end
 if r.state=="CONFIRMED" then return out("BOUND_CANDIDATE","BOTH_SIDES_MATCH") end
 return out("UNKNOWN","INVALID_BINDING_STATE")
end
return M
