-- Pure, unconnected prototype. No engine/UI imports, properties, effects or event ledger.
-- Only a future audited GAMEPLAY_CURRENT provider may satisfy the full-refresh contract.
local M={}
local function integer(v) return type(v)=="number" and v>=0 and v%1==0 and v<math.huge end
local function text(v) return type(v)=="string" and #v>0 and #v<=256 end
local function copy(t)
  if type(t)~="table" then return t end
  local r={};for k,v in pairs(t) do r[k]=copy(v) end;return r
end
local function keys(t) local r={};for k in pairs(t) do r[#r+1]=k end;table.sort(r);return r end
local function part(v) v=tostring(v);return #v..":"..v end
local function signature(r)
  local a={};for _,k in ipairs({"key","originPlayer","originCityID","originUID","destinationPlayer","destinationCityID","destinationUID","traderUnitID","identityKind"}) do a[#a+1]=part(r[k]) end
  return table.concat(a,"|")
end
local function normalize(snapshot,resolve,atWar)
  assert(type(snapshot)=="table" and snapshot.status=="COMPLETE" and snapshot.context=="GAMEPLAY"
    and snapshot.authority=="GAMEPLAY_CURRENT" and text(snapshot.sourceID),"AUTHORITATIVE_FULL_SOURCE_REQUIRED")
  assert(type(snapshot.rows)=="table" and integer(snapshot.count) and snapshot.count<=4096,"BAD_SNAPSHOT_SHAPE")
  -- Provider must already copy engine rows into a dense, scalar-only array.
  local entries=0
  for k in pairs(snapshot.rows) do
    assert(integer(k) and k>=1 and k<=snapshot.count,"SPARSE_OR_EXTRA_ROW")
    entries=entries+1
  end
  assert(entries==snapshot.count,"PARTIAL_SNAPSHOT")
  local routes,traders={},{};local rejected=0
  for i=1,snapshot.count do
    local row=snapshot.rows[i];assert(type(row)=="table","BAD_ROW")
    assert(type(row.current)=="boolean","CURRENT_STATUS_UNKNOWN")
    for _,f in ipairs({"originPlayer","originCityID","destinationPlayer","destinationCityID"}) do assert(integer(row[f]),"BAD_ENDPOINT_FIELD:"..f) end
    if row.current then
      local o=resolve(row.originPlayer,row.originCityID)
      local d=resolve(row.destinationPlayer,row.destinationCityID)
      assert(type(o)=="table" and type(d)=="table","ENDPOINT_RESOLUTION_UNKNOWN")
      assert(o.status=="PRESENT" or o.status=="ABSENT","ORIGIN_UNKNOWN")
      assert(d.status=="PRESENT" or d.status=="ABSENT","DESTINATION_UNKNOWN")
      local valid=o.status=="PRESENT" and d.status=="PRESENT"
      if valid then
        assert(integer(o.owner) and integer(d.owner) and integer(o.cityID) and integer(d.cityID) and text(o.uid) and text(d.uid),"BAD_CITY_MAPPING")
        valid=o.owner==row.originPlayer and d.owner==row.destinationPlayer and o.cityID==row.originCityID and d.cityID==row.destinationCityID
      end
      if valid and o.owner~=d.owner then
        local war=atWar(o.owner,d.owner);assert(type(war)=="boolean","DIPLOMACY_UNKNOWN");valid=not war
      end
      if valid then
        local engine=row.engineRouteID;local trader=row.traderUnitID
        assert(engine==nil or integer(engine) or text(engine),"BAD_ENGINE_ID")
        assert(trader==nil or integer(trader),"BAD_TRADER_ID")
        assert(engine~=nil or trader~=nil,"ROUTE_IDENTITY_MISSING")
        local key,kind
        if engine~=nil then key="engine|"..part(o.owner).."|"..part(type(engine))..part(engine);kind="ENGINE_ID"
        else key="trader|"..part(o.owner)..part(trader)..part(o.uid)..part(d.uid);kind="TRADER_ENDPOINT_SNAPSHOT_KEY" end
        local r={key=key,engineRouteID=engine,traderUnitID=trader,identityKind=kind,
          originPlayer=o.owner,originCityID=o.cityID,originUID=o.uid,
          destinationPlayer=d.owner,destinationCityID=d.cityID,destinationUID=d.uid,
          domestic=o.owner==d.owner,current=true,validity="CURRENT_ENDPOINTS_VALID"}
        if trader~=nil then
          local unitKey=part(o.owner)..part(trader)
          assert(traders[unitKey]==nil or traders[unitKey]==key,"TRADER_CONFLICTING_ROUTES")
          traders[unitKey]=key
        end
        assert(routes[key]==nil or signature(routes[key])==signature(r),"CONFLICTING_DUPLICATE")
        routes[key]=r
      else rejected=rejected+1 end
    else rejected=rejected+1 end
  end
  local ordered=keys(routes);local parts={}
  for _,k in ipairs(ordered) do parts[#parts+1]=signature(routes[k]) end
  return {routes=routes,orderedKeys=ordered,count=#ordered,fingerprint=table.concat(parts,"\n"),sourceID=snapshot.sourceID,rejected=rejected}
end
function M.New()
  local s={ready=false,dirty=true,revision=0,attempts=0,lastGood=nil,current=nil,reason="INITIALIZATION_REQUIRED"}
  function s:MarkDirty(reason) self.dirty=true;self.ready=false;self.current=nil;self.reason=reason or "DIRTY" end
  function s:Refresh(fetch,resolve,atWar)
    self.attempts=self.attempts+1
    local ok,nextState=pcall(function() return normalize(fetch(),resolve,atWar) end)
    if not ok then
      self:MarkDirty("SOURCE_UNAVAILABLE_OR_INVALID")
      self.error=tostring(nextState)
      return false,self.error -- lastGood is diagnostics only; never returned by Read().
    end
    local old=self.lastGood;local added,removed={},{}
    for _,k in ipairs(nextState.orderedKeys) do if not old or not old.routes[k] then added[#added+1]=k end end
    if old then for _,k in ipairs(old.orderedKeys) do if not nextState.routes[k] then removed[#removed+1]=k end end end
    if not old or old.fingerprint~=nextState.fingerprint then self.revision=self.revision+1 end
    nextState.revision=self.revision;nextState.added=added;nextState.removed=removed
    self.current=nextState;self.lastGood=copy(nextState);self.ready=true;self.dirty=false;self.error=nil;self.reason="FULL_REFRESH"
    return true,copy(nextState)
  end
  function s:Read()
    if not self.ready or self.dirty then return {status="UNKNOWN",reason=self.reason,error=self.error} end
    local r=copy(self.current);r.status="READY";return r
  end
  return s
end
return M
