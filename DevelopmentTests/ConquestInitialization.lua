-- D0010 offline contract reducer. No native events, Property writes or projects.
-- Inputs contain MOCK_ONLY proofs, never substitute them for real acquisition evidence.
local M={}
local kinds={CAMPUS="RESEARCH",THEATER_SQUARE="CULTURE",INDUSTRIAL_ZONE="INDUSTRY",COMMERCIAL_HUB="COMMERCE"}
local function clone(v)
 if type(v)~="table" then return v end
 local r={};for k,x in pairs(v) do r[k]=clone(x) end;return r
end
local function text(v) return type(v)=="string" and #v>0 end
local function int(v) return type(v)=="number" and v>=0 and v%1==0 and v<math.huge end
local function guard(fn)
 local ok,r=pcall(fn)
 if ok then return r end
 return {status="UNKNOWN",reason=tostring(r)}
end
local function context(c)
 assert(type(c)=="table" and c.contextSource=="MOCK_ONLY","OFFLINE_ONLY")
 assert(text(c.cityUID) and int(c.owner) and text(c.transitionID),"CONQUEST_REFERENCE_REQUIRED")
 assert(c.eligibility=="ENABLED","CURRENT_OWNER_NOT_ENABLED")
end
local function record(s,c)
 context(c)
 assert(type(s)=="table" and s.schema=="D0010_CONQUEST_CONTRACT_V1" and s.contextSource=="MOCK_ONLY","MODE_RECORD_REQUIRED")
 assert(s.cityUID==c.cityUID and s.owner==c.owner and s.transitionID==c.transitionID,"TRANSFER_OR_IDENTITY_ADAPTER_REQUIRED")
 assert(s.mode=="LEGACY_CLAIM" or s.mode=="NORMAL_FIRST_COMPLETION","INVALID_MODE")
 assert(type(s.legacySet)=="table" and int(s.boundary) and int(s.revision),"INVALID_SNAPSHOT")
 local n=0
 for kind,yes in pairs(s.legacySet) do
  assert(yes==true and (kind=="RESEARCH" or kind=="CULTURE" or kind=="INDUSTRY" or kind=="COMMERCE"),"INVALID_LEGACY_SET");n=n+1
 end
 assert((n>0)==(s.mode=="LEGACY_CLAIM"),"MODE_SNAPSHOT_CONFLICT")
 if s.identity then
  assert((s.identity=="RESEARCH" or s.identity=="CULTURE" or s.identity=="INDUSTRY" or s.identity=="COMMERCE")
   and s.potential==1 and type(s.origin)=="table","INVALID_INITIAL_IDENTITY")
  if s.mode=="LEGACY_CLAIM" then
   assert(s.legacySet[s.identity] and s.origin.kind=="LEGACY_CLAIM" and s.origin.transitionID==s.transitionID,"INVALID_CLAIM_ORIGIN")
  else
   assert(s.origin.kind=="FIRST_COMPLETION" and int(s.origin.sequence) and s.origin.sequence>s.boundary
    and text(s.origin.districtUID),"INVALID_COMPLETION_ORIGIN")
  end
 else assert(s.potential==nil and s.origin==nil,"UNASSIGNED_FACT_CONFLICT") end
 return clone(s)
end
function M.Initialize(saved,c,proof,snapshot)
 return guard(function()
  context(c)
  -- Repeated notification/reload uses the stored mode; no new scan or candidate expansion.
  if saved then return {status="READY",changed=false,record=record(saved,c)} end
  assert(type(proof)=="table" and proof.contextSource=="MOCK_ONLY" and proof.cityUID==c.cityUID
   and proof.toOwner==c.owner and proof.transitionID==c.transitionID and int(proof.fromOwner)
   and proof.fromOwner~=c.owner and proof.status=="OWNERSHIP_TRANSITION_COMPLETE","TRANSITION_PROOF_REQUIRED")
  if proof.permanentFacts=="VERIFIED_EXISTING_IDENTITY" then
   return {status="INHERIT_REQUIRED",reason="PROG_004_PRESERVE_FACTS_RECOMPUTE_DERIVED"}
  end
  assert(proof.permanentFacts=="VERIFIED_NO_IDENTITY_NO_PRIOR_SPECIALIZATION","NO_IDENTITY_PROOF_REQUIRED")
  assert(type(snapshot)=="table" and snapshot.status=="COMPLETE_AT_TRANSITION"
   and snapshot.transitionID==c.transitionID and int(snapshot.boundary) and type(snapshot.districts)=="table","EXACT_BOUNDARY_SNAPSHOT_REQUIRED")
  local set,seen,count={},{},0
  for k in pairs(snapshot.districts) do assert(int(k) and k>=1,"DENSE_SCAN_REQUIRED");count=count+1 end
  for i=1,count do
   local d=snapshot.districts[i]
   assert(type(d)=="table" and d.mappingStatus=="VALIDATED_FAMILY" and text(d.districtUID)
    and type(d.complete)=="boolean" and (kinds[d.family] or d.family=="NON_V01"),"VERIFIED_DISTRICT_REQUIRED")
   if seen[d.districtUID] then
    assert(seen[d.districtUID].family==d.family and seen[d.districtUID].complete==d.complete,"CONFLICTING_DISTRICT_SCAN")
   else seen[d.districtUID]=d end
   if d.complete and kinds[d.family] then set[kinds[d.family]]=true end
  end
  return {status="READY",changed=true,record={schema="D0010_CONQUEST_CONTRACT_V1",contextSource="MOCK_ONLY",
   owner=c.owner,cityUID=c.cityUID,transitionID=c.transitionID,boundary=snapshot.boundary,revision=1,
   mode=next(set) and "LEGACY_CLAIM" or "NORMAL_FIRST_COMPLETION",legacySet=set}}
 end)
end
function M.AvailableClaims(saved,c)
 return guard(function()
  local s=record(saved,c)
  return {status="READY",claims=(s.mode=="LEGACY_CLAIM" and not s.identity) and clone(s.legacySet) or {}}
 end)
end
function M.Complete(saved,c,event)
 return guard(function()
  local s=record(saved,c)
  if s.identity or s.mode=="LEGACY_CLAIM" then return {status="READY",changed=false,record=s} end
  assert(type(event)=="table" and event.contextSource=="MOCK_ONLY" and event.cityUID==c.cityUID
   and event.owner==c.owner and event.transitionID==c.transitionID and event.delivery=="LIVE_COMPLETION"
   and int(event.sequence) and event.sequence>s.boundary,"POST_TRANSITION_COMPLETION_REQUIRED")
  local d=event.district
  assert(type(d)=="table" and d.mappingStatus=="VALIDATED_FAMILY" and text(d.districtUID)
   and type(d.complete)=="boolean" and (kinds[d.family] or d.family=="NON_V01"),"VERIFIED_DISTRICT_REQUIRED")
  if d.complete and kinds[d.family] then
   s.identity=kinds[d.family];s.potential=1;s.origin={kind="FIRST_COMPLETION",sequence=event.sequence,districtUID=d.districtUID}
   s.revision=s.revision+1;return {status="READY",changed=true,record=s}
  end
  return {status="READY",changed=false,record=s}
 end)
end
function M.Claim(saved,c,kind)
 return guard(function()
  local s=record(saved,c)
  if s.identity then return {status="READY",changed=false,record=s} end
  assert(s.mode=="LEGACY_CLAIM" and s.legacySet[kind]==true,"CLAIM_OUTSIDE_FROZEN_SET")
  s.identity=kind;s.potential=1;s.origin={kind="LEGACY_CLAIM",transitionID=s.transitionID}
  s.revision=s.revision+1
  return {status="READY",changed=true,record=s}
 end)
end
return M
