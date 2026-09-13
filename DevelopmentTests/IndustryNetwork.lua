-- D0005 offline only. Per-recipient current provenance; no purchase or production APIs.
local M={}
local function finite(v) return type(v)=="number" and v==v and v>=0 and v<math.huge end
function M.FromState(state,player,details,contextSource)
 local ok,result=pcall(function()
  assert(contextSource=="MOCK_ONLY","OFFLINE_ONLY")
  assert(type(player)=="number" and player>=0 and player%1==0,"PLAYER_REQUIRED")
  -- UI shadow never becomes a production authority through this module.
  assert(state.status=="READY_PROVENANCE_ONLY" and state.authority~="UI_SHADOW_ONLY","PROVENANCE_REQUIRED")
  local out={status="READY_OFFLINE_INDUSTRY",contextSource="MOCK_ONLY",player=player,
   routeRevision=state.routeRevision,contextRevision=state.contextRevision,recipients={}}
  for _,s in pairs(state.sources) do assert(s.owner==player,"SOURCE_OWNER") end
  for _,c in pairs(state.centers) do assert(c.owner==player,"CENTER_OWNER") end
  for uid,recipient in pairs(state.recipients.INDUSTRY or {}) do
   local sources={}
   for centerID,sourceSet in pairs(recipient.qualifications or {}) do
    local center=assert(state.centers[centerID],"CENTER_MISSING")
    for sourceID,reasons in pairs(sourceSet) do
     assert(type(reasons)=="table" and next(reasons) and center.connectedSources[sourceID]
      and next(center.connectedSources[sourceID]),"QUALIFICATION_MISSING")
     local s=assert(state.sources[sourceID],"SOURCE_MISSING")
     assert(s.kind=="INDUSTRY" and s.owner==player,"SOURCE_SCOPE")
     assert(finite(s.activeLevel) and s.activeLevel%1==0 and s.activeLevel>=1 and s.activeLevel<=4,"ACTIVE_REQUIRED")
     sources[sourceID]=s
    end
   end
   assert(next(sources),"RECIPIENT_WITHOUT_SOURCE")
   local r={production=0,discount=0,templates={},templateSources={},productionSources={},discountSources={},sources={}}
   for sourceID,s in pairs(sources) do
    local d=assert(details[sourceID],"SOURCE_DETAILS_MISSING")
    assert(d.templateRevision==s.templateRevision and d.templateRevision~=nil,"TEMPLATE_REVISION_MISMATCH")
    assert(type(d.templates)=="table","TEMPLATES_REQUIRED")
    r.sources[sourceID]=true
    local discount=10*s.activeLevel
    if discount>r.discount then r.discount=discount;r.discountSources={} end
    if discount==r.discount then r.discountSources[sourceID]=true end
    for template,known in pairs(d.templates) do
     assert(type(template)=="string" and #template>0 and known==true,"INVALID_TEMPLATE")
     r.templates[template]=true;r.templateSources[template]=r.templateSources[template] or {}
     r.templateSources[template][sourceID]=true
    end
    if s.activeLevel==4 then
     assert(finite(d.productionOutput),"VALIDATED_IV_OUTPUT_REQUIRED")
     if d.productionOutput>r.production then r.production=d.productionOutput;r.productionSources={} end
     if d.productionOutput==r.production then r.productionSources[sourceID]=true end
    end
   end
   out.recipients[uid]=r
  end
  return out
 end)
 if not ok then return {status="UNKNOWN",contextSource="MOCK_ONLY",reason=tostring(result)} end
 return result
end
-- Only a proposed percentage; caller still validates normal purchase eligibility.
function M.DiscountFor(result,recipient,template,currency)
 assert(result.status=="READY_OFFLINE_INDUSTRY" and result.contextSource=="MOCK_ONLY","OFFLINE_RESULT_REQUIRED")
 local r=result.recipients[recipient]
 if currency~="GOLD" or not r or not r.templates[template] then return 0 end
 return r.discount
end
return M
