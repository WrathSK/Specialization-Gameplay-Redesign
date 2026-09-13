-- Only classifies read-only observations. It NEVER emits COMPLETE_ORDERED_BATCH.
-- Caller must resolve native event district TYPE index via GameInfo before this boundary.
local M={}
local function integer(v) return type(v)=="number" and v==v and v>=0 and v%1==0 and v<math.huge end
function M.Inspect(event,observed,family)
 local function unknown(reason) return {status="UNKNOWN",reason=reason} end
 if type(event)~="table" or type(observed)~="table" then return unknown("OBSERVATION_REQUIRED") end
 if event.contextSource~="MOCK_ONLY" then return unknown("OFFLINE_ONLY") end
 if event.name~="OnDistrictConstructed" then return {status="IGNORED",reason="NOT_CONSTRUCTION_EVENT"} end
 if not integer(event.player) or not integer(event.x) or not integer(event.y) or type(event.districtType)~="string"
  or not integer(observed.cityID) or not integer(observed.districtID) then return unknown("IDENTIFIERS_REQUIRED") end
 if observed.isTestCivilization~=true then return {status="IGNORED",reason="NOT_TEST_CIVILIZATION"} end
 if observed.owner~=event.player or observed.cityOwner~=event.player or observed.districtType~=event.districtType
  or observed.x~=event.x or observed.y~=event.y then return unknown("EVENT_OBJECT_MISMATCH") end
 if type(observed.complete)~="boolean" then return unknown("COMPLETENESS_UNAVAILABLE") end
 if not observed.complete then return {status="IGNORED",reason="NOT_COMPLETE"} end
 if type(family)~="table" or family.status~="READY" or family.mappingStatus~="VALIDATED_FAMILY" or family.districtType~=event.districtType then return unknown("FAMILY_UNAVAILABLE") end
 if family.family=="NON_V01" then return {status="IGNORED",reason="OUT_OF_V01"} end
 if observed.lifecycle~="KNOWN_CURRENT_CITY" then return unknown("LIFECYCLE_UNRESOLVED") end
 -- A complete (even pillaged) district is not an authoritative first-completion history.
 return {status="CANDIDATE_COMPLETION",family=family.family,districtType=event.districtType,
  cityID=observed.cityID,districtID=observed.districtID,owner=event.player,
  requires={"STABLE_CITY_IDENTITY","EVENT_ORDER_AND_REPLAY_VALIDATION","PERSISTENT_FACT_TRANSACTION"}}
end
return M
