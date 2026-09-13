-- Offline PROG-001..004 reducer. No engine calls, Property writer, or unit consumption.
-- Stable identities and validated engine-notification order are caller contracts (PROG-005).
local M={}
local kinds={CAMPUS="RESEARCH",THEATER_SQUARE="CULTURE",INDUSTRIAL_ZONE="INDUSTRY",COMMERCIAL_HUB="COMMERCE"}
local function fail(status,reason) error({status=status,reason=reason},0) end
local function check(v,reason) if not v then fail("UNKNOWN",reason) end end
local function text(v) return type(v)=="string" and #v>0 end
local function integer(v) return type(v)=="number" and v==v and v%1==0 and v>=0 and v<math.huge end
local function guarded(fn)
 local ok,result=pcall(fn)
 if ok then return result end
 if type(result)=="table" and result.status then return result end
 return {status="UNKNOWN",reason="MALFORMED_INPUT"}
end
local function identity(id)
 check(type(id)=="table" and id.contextSource=="MOCK_ONLY","OFFLINE_CONTEXT_REQUIRED")
 check(text(id.cityUID) and integer(id.owner),"VALIDATED_CITY_IDENTITY_REQUIRED")
 check(id.present==true,"CITY_NOT_PRESENT")
end
-- Explicit current-player qualification; never infer it from civ, leader, human or saved facts.
function M.Participation(id)
 return guarded(function()
  identity(id)
  local e=id.eligibility
  check(type(e)=="table" and e.contextSource=="MOCK_ONLY" and e.player==id.owner,
   "CURRENT_OWNER_ELIGIBILITY_REQUIRED")
  check(e.status=="ENABLED" or e.status=="DISABLED","ELIGIBILITY_UNKNOWN")
  return {status=e.status=="ENABLED" and "READY" or "DORMANT",active=0,effectsEnabled=false}
 end)
end
local function enabled(id)
 local e=M.Participation(id)
 if e.status~="READY" then fail(e.status,e.reason or "PLAYER_DISABLED") end
end
local function facts(saved,id)
 identity(id)
 if saved==nil then fail("UNKNOWN","OLD_SAVE_COMPATIBILITY_REQUIRED") end
 check(type(saved)=="table" and saved.schemaVersion==1,"UNSUPPORTED_FACT_SCHEMA")
 check(saved.cityUID==id.cityUID,"CITY_GENERATION_MISMATCH")
 if saved.owner~=id.owner then fail("UNKNOWN","VERIFIED_OWNERSHIP_TRANSFER_REQUIRED") end
 check(integer(saved.revision),"FACT_REVISION")
 local f={schemaVersion=1,cityUID=id.cityUID,owner=id.owner,revision=saved.revision,investments={},ownedTemplates={}}
 check(saved.ownedTemplates==nil or type(saved.ownedTemplates)=="table","OWNED_TEMPLATE_SET_REQUIRED")
 for template,known in pairs(saved.ownedTemplates or {}) do
  check(text(template) and known==true,"INVALID_OWNED_TEMPLATE");f.ownedTemplates[template]=true
 end
 check(type(saved.investments)=="table","INVESTMENT_LEDGER_REQUIRED")
 local count,units=0,{}
 for receipt,unit in pairs(saved.investments) do
  check(text(receipt) and text(unit) and not units[unit],"INVALID_INVESTMENT_LEDGER")
  units[unit]=true;f.investments[receipt]=unit;count=count+1
 end
 if saved.specialization==nil then
  check(saved.potential==nil and saved.firstCompletion==nil and count==0,"UNASSIGNED_FACT_CONFLICT")
 else
  local first=saved.firstCompletion
  check(type(first)=="table" and kinds[first.family]==saved.specialization and text(first.eventID)
   and text(first.districtUID),"FIRST_COMPLETION_REQUIRED")
  check(integer(saved.potential) and saved.potential>=1 and saved.potential<=4
   and saved.potential==1+count,"POTENTIAL_LEDGER_MISMATCH")
  f.specialization=saved.specialization;f.potential=saved.potential
  f.firstCompletion={family=first.family,eventID=first.eventID,districtUID=first.districtUID}
 end
 return f
end
function M.NewCity(id)
 return guarded(function()
  enabled(id)
  check(id.freshFoundationObserved==true,"FRESH_FOUNDATION_REQUIRED")
  return {status="READY",facts={schemaVersion=1,cityUID=id.cityUID,owner=id.owner,revision=0,investments={}}}
 end)
end
-- This proof must come from a future audited acquisition adapter, not missing Property alone.
function M.AcquireUnassigned(saved,id,proof)
 return guarded(function()
  enabled(id)
  check(saved==nil,"EXISTING_FACTS_MUST_BE_PRESERVED")
  check(type(proof)=="table" and proof.contextSource=="MOCK_ONLY"
   and proof.status=="VERIFIED_NEVER_ENABLED_NO_FACTS" and proof.cityUID==id.cityUID
   and integer(proof.fromOwner) and proof.fromOwner~=id.owner and proof.toOwner==id.owner,
   "VERIFIED_ACQUISITION_HISTORY_REQUIRED")
  -- D0010: never initialize every acquisition as ordinary first-completion.
  -- A mode-aware snapshot/Claim adapter must replace this schema-v1 shortcut.
  return {status="UNKNOWN",reason="D0010_CONQUEST_INITIALIZER_REQUIRED"}
 end)
end
function M.Restore(saved,id)
 return guarded(function() return {status="READY",facts=facts(saved,id)} end)
end
-- D0005: only explicit verified SAME-city transfer may change the owner of facts.
-- MOCK proof is caller evidence, not a discovered Civ VI permanent UID API.
function M.TransferOwnership(saved,oldID,newID,proof)
 return guarded(function()
  check(type(oldID)=="table","OLD_IDENTITY_REQUIRED")
  local f=facts(saved,oldID)
  check(type(newID)=="table" and newID.contextSource=="MOCK_ONLY" and newID.present==true
   and integer(newID.owner) and newID.cityUID==f.cityUID,"SAME_CITY_IDENTITY_REQUIRED")
  check(type(proof)=="table" and proof.contextSource=="MOCK_ONLY" and proof.status=="VERIFIED_SAME_CITY"
   and proof.cityUID==f.cityUID and proof.fromOwner==f.owner and proof.toOwner==newID.owner
   and proof.expectedRevision==f.revision,"OWNERSHIP_PROOF_REQUIRED")
  check(newID.owner~=f.owner,"NOT_AN_OWNERSHIP_CHANGE")
  f.owner=newID.owner;f.revision=f.revision+1
  -- facts() copied only permanent fields: no prior ACTIVE or received network cache.
  return {status="READY",changed=true,facts=f,requires="REEVALUATE_ELIGIBILITY_BEFORE_DERIVED_STATE"}
 end)
end
function M.Complete(saved,id,batch)
 return guarded(function()
  enabled(id)
  local f=facts(saved,id)
  check(type(batch)=="table" and batch.status=="COMPLETE_ORDERED_BATCH" and batch.orderBasis=="ENGINE_DELIVERY" and batch.cityUID==id.cityUID
   and batch.owner==id.owner and text(batch.eventID),"COMPLETION_BATCH_REQUIRED")
  check(type(batch.districts)=="table","DISTRICTS_REQUIRED")
  local candidates,seen={},{}
  local length=0
  for k in pairs(batch.districts) do check(integer(k) and k>=1,"SPARSE_BATCH");length=length+1 end
  for i=1,length do
   local d=batch.districts[i];check(type(d)=="table","SPARSE_BATCH")
   check(d.mappingStatus=="VALIDATED_FAMILY" and text(d.districtUID) and type(d.complete)=="boolean","DISTRICT_FACT_REQUIRED")
   check(kinds[d.family]~=nil or d.family=="NON_V01","UNREVIEWED_DISTRICT_FAMILY")
   if d.complete and kinds[d.family] then
    if seen[d.districtUID] then check(seen[d.districtUID]==d.family,"DISTRICT_FAMILY_CONFLICT")
    else candidates[#candidates+1]=d;seen[d.districtUID]=d.family end
   end
  end
  -- Existing specialization cannot be replaced by later completed districts.
  if f.specialization or #candidates==0 then return {status="READY",changed=false,facts=f} end
  -- D0004 PROG-005: preserve delivery order; never sort by type/ID or aggregate a turn.
  local d=candidates[1]
  f.specialization=kinds[d.family];f.potential=1;f.revision=f.revision+1
  f.firstCompletion={eventID=batch.eventID,districtUID=d.districtUID,family=d.family}
  return {status="READY",changed=true,facts=f}
 end)
end
-- Read-only eligibility before a future transaction consumes anything.
function M.PlanInvestment(saved,id,unit)
 return guarded(function()
  enabled(id)
  local f=facts(saved,id)
  check(type(unit)=="table" and unit.contextSource=="MOCK_ONLY" and unit.owner==id.owner
   and unit.cityUID==id.cityUID and unit.unitType=="SETTLER" and unit.present==true
   and text(unit.unitUID),"ELIGIBLE_SETTLER_REQUIRED")
  check(f.specialization~=nil,"SPECIALIZATION_REQUIRED")
  check(f.potential<4,"POTENTIAL_CAP")
  for _,spent in pairs(f.investments) do check(spent~=unit.unitUID,"SETTLER_ALREADY_SPENT") end
  return {status="READY",expectedRevision=f.revision,cityUID=f.cityUID,unitUID=unit.unitUID,
   targetPotential=f.potential+1,consumed=false}
 end)
end
-- A committed MOCK receipt models an atomic Settler debit + investment transaction.
-- No claim that Civ VI can atomically consume a unit and persist this ledger yet.
function M.CommitInvestment(saved,id,receipt)
 return guarded(function()
  enabled(id)
  local f=facts(saved,id)
  check(type(receipt)=="table" and receipt.contextSource=="MOCK_ONLY" and receipt.status=="COMMITTED"
   and receipt.cityUID==id.cityUID and receipt.owner==id.owner and receipt.unitType=="SETTLER"
   and receipt.unitConsumed==true and text(receipt.unitUID) and text(receipt.id),"COMMITTED_SETTLER_RECEIPT_REQUIRED")
  check(f.specialization~=nil,"SPECIALIZATION_REQUIRED")
  if f.investments[receipt.id] then
   check(f.investments[receipt.id]==receipt.unitUID,"RECEIPT_CONFLICT")
   return {status="READY",changed=false,facts=f}
  end
  check(receipt.expectedRevision==f.revision,"STALE_INVESTMENT_PLAN")
  for _,unit in pairs(f.investments) do check(unit~=receipt.unitUID,"SETTLER_ALREADY_SPENT") end
  check(f.potential<4,"POTENTIAL_CAP")
  f.investments[receipt.id]=receipt.unitUID;f.potential=f.potential+1;f.revision=f.revision+1
  return {status="READY",changed=true,facts=f}
 end)
end
function M.Derive(saved,id,governor)
 return guarded(function()
  local e=M.Participation(id)
  if e.status~="READY" then return {status=e.status,reason=e.reason or "PLAYER_DISABLED",active=0,effectsEnabled=false} end
  local f=facts(saved,id)
  if not f.specialization then return {status="READY",cityUID=f.cityUID,active=0,reason="NO_SPECIALIZATION"} end
  -- Consume the existing read-only probe's KNOWN ceiling, never infer from spent titles.
  check(type(governor)=="table" and governor.governorGateStatus=="KNOWN"
   and governor.owner==id.owner and governor.cityUID==id.cityUID,"GOVERNOR_FACTS_REQUIRED")
  local ceiling=governor.governorLevelCeiling
  check(integer(ceiling) and ceiling>=1 and ceiling<=4,"GOVERNOR_CEILING_INVALID")
  return {status="READY",cityUID=f.cityUID,specialization=f.specialization,potential=f.potential,
   active=math.min(f.potential,ceiling),effectsEnabled=true,factRevision=f.revision}
 end)
end
return M
