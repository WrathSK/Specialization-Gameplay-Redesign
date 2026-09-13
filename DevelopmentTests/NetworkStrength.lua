-- Pure calculation prototype only. Not imported by the runtime mod (including B004).
local M={Coefficients={RESEARCH=1,CULTURE=1}}
local function finite(v) return type(v)=="number" and v==v and v~=math.huge and v~=-math.huge end
-- Caller supplies validated, actually receiving OWNED city UIDs for one network.
-- Repeated routes/centers/providers may contribute the same UID; count it once.
-- This helper deliberately does not infer recipients from raw routes or pick a source.
function M.Calculate(kind,activeLevel,recipientUIDs,coefficient)
  assert(M.Coefficients[kind]~=nil,"unsupported boost network")
  assert(finite(activeLevel) and activeLevel%1==0 and activeLevel>=1 and activeLevel<=4,"invalid ACTIVE level")
  assert(type(recipientUIDs)=="table","recipient list required")
  local k=coefficient
  if k==nil then k=M.Coefficients[kind] end
  assert(finite(k) and k>=0,"invalid coefficient")
  local seen,n={},0
  for _,uid in ipairs(recipientUIDs) do
    assert(type(uid)=="string" and #uid>0,"validated stable city UID required")
    if not seen[uid] then seen[uid]=true;n=n+1 end
  end
  local strength=k*activeLevel*math.sqrt(n)
  assert(finite(strength),"strength overflow")
  return {N=n,L=activeLevel,k=k,networkStrength=strength,recipients=seen}
end
-- Consume a freshly derived ONE-player provenance snapshot, never historical routes.
-- Explicit MOCK_ONLY gate: this entry point is offline and cannot authorize gameplay.
function M.FromState(state,player,coefficients,contextSource)
  local ok,result=pcall(function()
    assert(contextSource=="MOCK_ONLY","OFFLINE_CONTEXT_REQUIRED")
    assert(type(player)=="number" and player%1==0 and player>=0,"PLAYER_REQUIRED")
    assert(state.status=="READY_PROVENANCE_ONLY" or state.status=="READY_SHADOW_PROVENANCE_ONLY","STATE_NOT_READY")
    local shadow=state.status=="READY_SHADOW_PROVENANCE_ONLY"
    if shadow then
      assert(state.authority=="UI_SHADOW_ONLY" and state.sourceContext=="UI" and state.contextSource=="MOCK_ONLY","SHADOW_SCOPE")
    end
    coefficients=coefficients or {}
    local out={status="READY_OFFLINE_STRENGTH",contextSource="MOCK_ONLY",
      authority=shadow and "UI_SHADOW_ONLY" or "MOCK_ONLY",player=player,
      routeRevision=state.routeRevision,contextRevision=state.contextRevision,networks={}}
    -- Reject mixed empire fixtures instead of letting their sources increase this player's L.
    for _,source in pairs(state.sources) do assert(source.owner==player,"SOURCE_OWNER") end
    for _,center in pairs(state.centers) do assert(center.owner==player,"CENTER_OWNER") end
    for _,kind in ipairs({"RESEARCH","CULTURE"}) do
      local activeSources,L={},0
      for _,center in pairs(state.centers) do
        for uid,reasons in pairs(center.connectedSources) do
          assert(type(reasons)=="table" and next(reasons)~=nil,"EMPTY_SOURCE_QUALIFICATION")
          local source=assert(state.sources[uid],"MISSING_SOURCE")
          if source.kind==kind then
            local level=source.activeLevel
            assert(finite(level) and level%1==0 and level>=1 and level<=4,"invalid ACTIVE level")
            activeSources[uid]=level;L=math.max(L,level)
          end
        end
      end
      local recipients={}
      for uid,recipient in pairs(state.recipients[kind] or {}) do
        -- A recipient requires a current center/source qualification, not a cached count.
        local supported=false
        for centerUID,sourceSet in pairs(recipient.qualifications or {}) do
          local center=assert(state.centers[centerUID],"MISSING_CENTER")
          for sourceUID,reasons in pairs(sourceSet) do
            assert(activeSources[sourceUID] and center.connectedSources[sourceUID]
              and type(reasons)=="table" and next(reasons)~=nil,"INVALID_RECIPIENT_QUALIFICATION")
            supported=true
          end
        end
        assert(supported,"RECIPIENT_WITHOUT_SOURCE")
        recipients[#recipients+1]=uid
      end
      table.sort(recipients)
      -- Calculate validates k even for the explicit empty-source boundary.
      local n=M.Calculate(kind,L==0 and 1 or L,recipients,coefficients[kind])
      n.L=L;if L==0 then n.networkStrength=0 end
      n.sources=activeSources;n.maxSources={}
      for uid,level in pairs(activeSources) do if level==L then n.maxSources[uid]=true end end
      out.networks[kind]=n
    end
    return out
  end)
  if not ok then return {status="UNKNOWN",contextSource="MOCK_ONLY",reason=tostring(result)} end
  return result
end
-- No Modifier amount, rounding, Industry merger, or Spaceport activation here.
return M
