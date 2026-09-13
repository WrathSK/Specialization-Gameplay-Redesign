-- Offline preparation: caller evidence is MOCK_ONLY, never an engine certificate.
-- One proposed envelope holds foundation qualification, delivery cursor and permanent facts.
local M={}
local function clone(x)
 if type(x)~="table" then return x end
 local y={};for k,v in pairs(x) do y[k]=clone(v) end;return y
end
local function integer(x) return type(x)=="number" and x>=0 and x%1==0 and x<math.huge end
local function text(x) return type(x)=="string" and #x>0 end
local function guard(fn)
 local ok,r=pcall(fn)
 if ok then return r end
 return {status="UNKNOWN",reason=tostring(r)}
end
function M.New(State)
 local J={}
 local function restore(saved,id)
  assert(type(id)=="table" and id.contextSource=="MOCK_ONLY","OFFLINE_ONLY")
  assert(type(saved)=="table" and saved.schema==1 and saved.origin=="FOUNDATION_QUALIFIED","NO_HISTORY_CERTIFICATE")
  assert(saved.cityUID==id.cityUID and saved.owner==id.owner,"IDENTITY_MISMATCH")
  assert(integer(saved.revision) and integer(saved.sequence),"BAD_CURSOR")
  assert(saved.health=="TRACKING" or saved.health=="GAP","BAD_HEALTH")
  assert(saved.health~="GAP" or text(saved.gapReason),"GAP_REASON_REQUIRED")
  if saved.sequence>0 then
   local r=saved.lastReceipt
   assert(type(r)=="table" and r.sequence==saved.sequence and text(r.eventID)
    and text(r.districtUID) and text(r.family) and type(r.complete)=="boolean","BAD_RECEIPT")
  else assert(saved.lastReceipt==nil,"UNEXPECTED_RECEIPT") end
  local checked=State.Restore(saved.facts,id)
  assert(checked.status=="READY",checked.reason or checked.status)
  local out=clone(saved);out.facts=checked.facts;return out
 end
 local function plan(saved,nextValue)
  return {status="PLAN_ONLY",expectedAbsent=saved==nil,expectedRevision=saved and saved.revision,
   proposed=nextValue,requires="COMPARE_BEFORE_WRITE_AND_VERIFIED_READBACK"}
 end
 function J.Restore(saved,id)
  return guard(function() return {status="READY",envelope=restore(saved,id)} end)
 end
 function J.Foundation(saved,id,evidence)
  return guard(function()
   local gate=State.Participation(id);if gate.status~="READY" then return gate end
   -- A replay never resets an established specialty, cursor or persistent GAP.
   if saved~=nil then return J.Restore(saved,id) end
   assert(type(evidence)=="table" and evidence.contextSource=="MOCK_ONLY"
    and evidence.phase=="AFTER_LOAD_CLOSE" and evidence.foundationObserved==true
    and evidence.bindingValidated==true and evidence.listenerReady==true
    and evidence.scanStatus=="COMPLETE" and evidence.completedV01Count==0,"FOUNDATION_NOT_QUALIFIED")
   local first=State.NewCity(id);assert(first.status=="READY",first.reason)
   return plan(nil,{schema=1,origin="FOUNDATION_QUALIFIED",cityUID=id.cityUID,owner=id.owner,
    revision=0,sequence=0,health="TRACKING",facts=first.facts})
  end)
 end
 function J.Gap(saved,id,reason)
  return guard(function()
   local gate=State.Participation(id);if gate.status~="READY" then return gate end
   local nextValue=restore(saved,id);assert(text(reason),"GAP_REASON_REQUIRED")
   if nextValue.health=="GAP" then return {status="READY",changed=false,envelope=nextValue} end
   nextValue.health="GAP";nextValue.gapReason=reason;nextValue.revision=nextValue.revision+1
   return plan(saved,nextValue)
  end)
 end
 function J.Complete(saved,id,event)
  return guard(function()
   local gate=State.Participation(id);if gate.status~="READY" then return gate end
   local nextValue=restore(saved,id)
   if nextValue.health=="GAP" then return {status="UNKNOWN",reason="PERSISTENT_HISTORY_GAP"} end
   assert(type(event)=="table" and event.contextSource=="MOCK_ONLY"
    and event.phase=="AFTER_LOAD_CLOSE" and event.owner==id.owner and event.cityUID==id.cityUID
    and event.mappingStatus=="VALIDATED_FAMILY" and integer(event.sequence) and event.sequence>0
    and text(event.eventID) and text(event.districtUID) and text(event.family)
    and type(event.complete)=="boolean","INVALID_NOTIFICATION")
   local receipt={sequence=event.sequence,eventID=event.eventID,districtUID=event.districtUID,
    family=event.family,complete=event.complete}
   if event.sequence==nextValue.sequence then
    for k,v in pairs(receipt) do assert(nextValue.lastReceipt[k]==v,"REPLAY_CONFLICT") end
    return {status="READY",changed=false,envelope=nextValue}
   end
   assert(event.sequence==nextValue.sequence+1,"DELIVERY_GAP_OR_STALE_EVENT")
   local result=State.Complete(nextValue.facts,id,{status="COMPLETE_ORDERED_BATCH",orderBasis="ENGINE_DELIVERY",
    owner=id.owner,cityUID=id.cityUID,eventID=event.eventID, districts={event}})
   assert(result.status=="READY",result.reason)
   nextValue.facts=result.facts;nextValue.lastReceipt=receipt;nextValue.sequence=event.sequence
   nextValue.revision=nextValue.revision+1
   return plan(saved,nextValue)
  end)
 end
 return J
end
return M
