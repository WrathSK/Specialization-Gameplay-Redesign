-- Pure UI shadow cache. No engine calls, permanent city UID, or gameplay authority.
local M={}
local function integer(n) return type(n)=="number" and n>=0 and n<math.huge and n%1==0 end
local function copy(t)
  if type(t)~="table" then return t end
  local r={};for k,v in pairs(t) do r[k]=copy(v) end;return r
end
local function cityKey(p,c) return p..":"..c end
local function normalize(s)
  assert(type(s)=="table" and s.status=="COMPLETE_UI_SHADOW" and s.sourceContext=="UI"
    and s.authority=="UI_SHADOW_ONLY","SHADOW_SOURCE_REQUIRED")
  assert(integer(s.player) and integer(s.turn) and integer(s.count) and s.count<=4096,"SHADOW_HEADER_INVALID")
  assert(type(s.keys)=="table" and type(s.routes)=="table","SHADOW_ROWS_INVALID")
  local n=0;for i in pairs(s.keys) do assert(integer(i) and i>=1 and i<=s.count,"SHADOW_KEYS_INVALID");n=n+1 end
  assert(n==s.count,"SHADOW_PARTIAL")
  local rows,keys,traders={},{},{}
  for i=1,s.count do
    local key=s.keys[i];assert(type(key)=="string" and #key<=256,"SHADOW_KEY_INVALID")
    local r=s.routes[key];assert(type(r)=="table","SHADOW_ROW_MISSING")
    for _,f in ipairs({"originPlayer","originCityID","destinationPlayer","destinationCityID","traderUnitID"}) do
      assert(integer(r[f]),"SHADOW_ENDPOINT_INVALID:"..f)
    end
    assert(r.originPlayer==s.player,"SHADOW_PLAYER_MISMATCH")
    local o,d=cityKey(r.originPlayer,r.originCityID),cityKey(r.destinationPlayer,r.destinationCityID)
    local expected=r.originPlayer..":"..r.traderUnitID.."|"..o..">"..d
    assert(key==expected and not rows[key],"SHADOW_KEY_CONFLICT")
    assert(not traders[r.traderUnitID],"SHADOW_TRADER_CONFLICT")
    traders[r.traderUnitID]=true;keys[#keys+1]=key
    rows[key]={key=key,traderUnitID=r.traderUnitID,originPlayer=r.originPlayer,originCityID=r.originCityID,
      destinationPlayer=r.destinationPlayer,destinationCityID=r.destinationCityID,
      originCityKey=o,destinationCityKey=d,identityKind="OWNER_CITY_ID_SNAPSHOT_ONLY",
      domestic=r.originPlayer==r.destinationPlayer,current=true,validity="UI_COLLECTOR_VALIDATED"}
  end
  n=0;for key in pairs(s.routes) do assert(rows[key],"SHADOW_EXTRA_ROW");n=n+1 end
  assert(n==s.count,"SHADOW_PARTIAL")
  table.sort(keys)
  return {status="READY_UI_SHADOW",schemaVersion=1,sourceContext="UI",authority="UI_SHADOW_ONLY",
    player=s.player,turn=s.turn,count=#keys,orderedKeys=keys,routes=rows,fingerprint=table.concat(keys,"\n")}
end
function M.New()
  local current,lastGood,revision=nil,nil,0
  local reason="INITIALIZATION_REQUIRED"
  local state={}
  function state:Invalidate(why) current=nil;reason=why or "DIRTY" end
  function state:Reset() current=nil;lastGood=nil;revision=0;reason="CONTEXT_RESET" end
  function state:Replace(snapshot)
    local ok,nextState=pcall(normalize,snapshot)
    if not ok then self:Invalidate("NORMALIZATION_FAILED");return false,tostring(nextState) end
    if lastGood and lastGood.player~=nextState.player then self:Reset() end
    local added,removed=0,0
    for _,k in ipairs(nextState.orderedKeys) do if not lastGood or not lastGood.routes[k] then added=added+1 end end
    if lastGood then for _,k in ipairs(lastGood.orderedKeys) do if not nextState.routes[k] then removed=removed+1 end end end
    if not lastGood or nextState.fingerprint~=lastGood.fingerprint then revision=revision+1 end
    nextState.revision=revision;nextState.addedCount=added;nextState.removedCount=removed
    current=nextState;lastGood=nextState;reason=nil
    return true
  end
  function state:Read()
    if not current then return {status="UNKNOWN",sourceContext="UI",authority="UI_SHADOW_ONLY",reason=reason} end
    return copy(current) -- owned scalar records only; consumer cannot mutate cache.
  end
  function state:Summary()
    return current and ("READY_UI_SHADOW；rev="..revision.."；count="..current.count) or "UNKNOWN"
  end
  return state
end
SPCShadowRouteState=M
return M
