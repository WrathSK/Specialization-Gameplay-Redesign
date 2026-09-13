-- Pure provenance prototype; no source-level merger, boost strength or yield application.
local M={}
local function add(t,k,v) t[k]=t[k] or {};t[k][v]=true end
local function keys(t) local r={};for k in pairs(t) do r[#r+1]=k end;table.sort(r);return r end
local function derive(routeState,context,shadow)
  local sources=context.sources or {};local centers=context.centers or {}
  local n={status=shadow and "READY_SHADOW_PROVENANCE_ONLY" or "READY_PROVENANCE_ONLY",routeRevision=routeState.revision,contextRevision=context.revision,
    sources={},centers={},recipients={},strengthStatus="NOT_CALCULATED",industryStrengthStatus="NOT_CALCULATED"}
  if shadow then
    n.sourceContext="UI";n.authority="UI_SHADOW_ONLY";n.contextSource="MOCK_ONLY"
    n.identityKind="OWNER_CITY_ID_SNAPSHOT_ONLY"
  end
  local originField=shadow and "originCityKey" or "originUID"
  local destinationField=shadow and "destinationCityKey" or "destinationUID"
  for uid,s in pairs(sources) do
    assert(s.kind=="RESEARCH" or s.kind=="CULTURE" or s.kind=="INDUSTRY","SOURCE_KIND")
    assert(type(s.activeLevel)=="number" and s.activeLevel%1==0 and s.activeLevel>=1 and s.activeLevel<=4,"ACTIVE_LEVEL")
    -- Only preserve provenance, including the template revision. No merge decision.
    n.sources[uid]={kind=s.kind,activeLevel=s.activeLevel,owner=s.owner,templateRevision=s.templateRevision}
    if shadow then n.sources[uid].cityKey=uid else n.sources[uid].uid=uid end
  end
  for uid,c in pairs(centers) do n.centers[uid]={owner=c.owner,connectedSources={},distributionRoutes={}} end
  local function connect(h,s,reason)
    if n.centers[h] and sources[s] and sources[s].owner==centers[h].owner then
      add(n.centers[h].connectedSources,s,reason)
    end
  end
  for _,k in ipairs(routeState.orderedKeys) do
    local r=routeState.routes[k]
    if r.domestic and centers[r[destinationField]] and centers[r[destinationField]].owner==r.originPlayer then
      connect(r[destinationField],r[originField],"route:"..k)
    end
  end
  -- D0005: only a validated current CAPITAL role grants source self-connection.
  -- This adds no recipient and creates no synthetic route.
  for uid,c in pairs(centers) do
    if c.isCapital==true then connect(uid,uid,"CAPITAL_SELF_CONNECTION") end
  end
  -- Other legal local qualifications remain explicit caller input.
  for h,sourceSet in pairs(context.localConnections or {}) do
    for s,enabled in pairs(sourceSet) do if enabled then connect(h,s,"local-eligibility") end end
  end
  local function receive(h,recipient,reason)
    for s in pairs(n.centers[h].connectedSources) do
      local kind=sources[s].kind;n.recipients[kind]=n.recipients[kind] or {}
      local set=n.recipients[kind];set[recipient]=set[recipient] or {sources={},centers={},qualifications={}}
      set[recipient].sources[s]=true;set[recipient].centers[h]=true
      -- retain center + source + qualification without concatenation collisions
      local q=set[recipient].qualifications;q[h]=q[h] or {};add(q[h],s,reason)
    end
  end
  for _,k in ipairs(routeState.orderedKeys) do
    local r=routeState.routes[k];local h=r[originField]
    if r.domestic and n.centers[h] and centers[h].owner==r.originPlayer then
      n.centers[h].distributionRoutes[k]=r[destinationField]
      receive(h,r[destinationField],"route:"..k)
    end
  end
  -- Hypothetical Commerce IV eligibility supplied by the caller; no runtime effect.
  for h,c in pairs(centers) do if c.freeSelfReceiver==true then receive(h,h,"COMMERCE_IV_SELF") end end
  n.recipientCounts={}
  for kind,set in pairs(n.recipients) do n.recipientCounts[kind]=#keys(set) end
  -- No recursive propagation: receiving at another center does not create direct sources.
  return n
end
function M.Derive(routeState,context)
  if routeState.status~="READY" then return {status="UNKNOWN",reason="ROUTES_NOT_READY"} end
  return derive(routeState,context,false)
end
-- Offline experiment only. Never relabel UI records as READY/GAMEPLAY_CURRENT.
-- Real specialization/center discovery is not implemented; roles must be explicit fixtures.
function M.DeriveShadow(routeState,context)
  local ok,result=pcall(function()
    assert(routeState.status=="READY_UI_SHADOW" and routeState.authority=="UI_SHADOW_ONLY"
      and routeState.sourceContext=="UI" and routeState.schemaVersion==1,"SHADOW_ROUTES_NOT_READY")
    assert(context.contextSource=="MOCK_ONLY","EXPLICIT_MOCK_ROLES_REQUIRED")
    local player=routeState.player
    local function validRole(key,role)
      assert(role.owner==player and type(key)=="string" and key:match("^"..player..":%d+$"),"SHADOW_ROLE_SCOPE")
    end
    for k,s in pairs(context.sources or {}) do validRole(k,s) end
    for k,c in pairs(context.centers or {}) do validRole(k,c) end
    for _,k in ipairs(routeState.orderedKeys) do
      local r=routeState.routes[k]
      assert(r.current==true and r.originPlayer==player and r.identityKind=="OWNER_CITY_ID_SNAPSHOT_ONLY","SHADOW_ROW_INVALID")
      assert(r.originCityKey==r.originPlayer..":"..r.originCityID
        and r.destinationCityKey==r.destinationPlayer..":"..r.destinationCityID,"SHADOW_CITY_MAPPING")
      assert(r.domestic==(r.originPlayer==r.destinationPlayer),"SHADOW_DOMESTIC_MISMATCH")
    end
    return derive(routeState,context,true)
  end)
  if not ok then return {status="UNKNOWN",authority="UI_SHADOW_ONLY",reason=tostring(result)} end
  return result
end
return M
