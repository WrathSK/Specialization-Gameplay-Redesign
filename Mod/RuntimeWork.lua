-- D2: ephemeral batch indexes, never persisted or shared across writes/batches.
SPCRuntimeWork={}
function SPCRuntimeWork.New(P,shared)
 local b={};local facts,byPlayer,live={}, {}, {}
 function b.Facts(pid,c)
  facts[pid]=facts[pid] or {};local t=facts[pid];local id=c:GetID()
  if not t[id] then t[id]=shared.EffectiveFacts.Read(pid,c) end
  return t[id]
 end
 function b.Districts(pid,c)
  if not byPlayer[pid] then
   local t={}
   for _,d in Players[pid]:GetDistricts():Members() do P.Count('district_scan')
    local city=assert(d:GetCity(),'SAMPLE_CITY_UNAVAILABLE')
    if city:GetOwner()==pid then local id=city:GetID();t[id]=t[id] or {};t[id][#t[id]+1]=d end
   end
   byPlayer[pid]=t -- publish the index only after complete enumeration
  end
  return ipairs(byPlayer[pid][c:GetID()] or {})
 end
 function b.Live(pid,industry)
  local k=pid..':'..tostring(industry)
  if not live[k] then live[k]=SPCSampleLifecycle.Live(P,pid,industry) end
  return live[k]
 end
 return b
end
-- Only named publisher metadata is interpreted as a scope. Native event argument
-- layouts are not guessed here; their wrappers below explicitly identify player.
function SPCRuntimeWork.Player(scope,pid)
 return type(scope)~='table' or scope.player==nil or scope.player==pid
end
-- Only the named, synchronous investment result may narrow these two writers.
-- Native hooks/player scopes remain unchanged. Facts belong to this writer's
-- batch; the next writer must revalidate rather than reuse post-write inputs.
function SPCRuntimeWork.InvestmentCity(P,shared,scope,batch)
 local function same(a,b)
  if type(a)~=type(b) then return false end;if type(a)~='table' then return a==b end
  for k,v in pairs(a)do if not same(v,b[k])then return false end end
  for k in pairs(b)do if a[k]==nil then return false end end;return true
 end
 local e=scope.investment;local pid=scope.player
 assert(type(e)=='table' and e.status=='COMMITTED' and e.cause=='INVESTMENT_COMMITTED'
  and type(pid)=='number' and pid==e.player and P.IsTestPlayer(pid),'INVESTMENT_SCOPE_UNKNOWN')
 assert(type(e.city)=='number' and e.city>=0 and e.city%1==0 and type(e.anchor)=='table'
  and e.anchor.owner==pid and e.anchor.cityID==e.city and type(e.anchor.token)=='string' and #e.anchor.token>0
  and type(e.receipt)=='string' and #e.receipt>0 and type(e.unitUID)=='string'
  and type(e.revision)=='number' and e.revision>=2 and e.revision<=4 and e.revision%1==0,'INVESTMENT_EVIDENCE_UNKNOWN')
 local player=assert(Players[pid],'INVESTMENT_PLAYER_UNAVAILABLE')
 local city=assert(player:GetCities():FindID(e.city),'INVESTMENT_CITY_UNAVAILABLE')
 assert(same(e.reference,{owner=city:GetOwner(),cityID=city:GetID(),x=city:GetX(),y=city:GetY()})
  and city:GetOwner()==pid,'INVESTMENT_REFERENCE_CHANGED')
 local f=batch.Facts(pid,city)
 assert(same(e.anchor,{owner=f.owner,cityID=f.cityID,token=f.token,first=f.first,specialization=f.specialization})
  and not f.investmentPending and f.investmentCount>=e.revision-1,'INVESTMENT_BINDING_CHANGED')
 assert(same(e.reference,{owner=city:GetOwner(),cityID=city:GetID(),x=city:GetX(),y=city:GetY()}),'INVESTMENT_CHANGED_DURING_READ')
 return city
end
function SPCRuntimeWork.Hook(P,source,name,fn)
 local e=P.Field(source,name);if not e or not e.Add then return end
 local lastTurn={}
 e.Add(function(pid,...)
  if name=='BuildingAddedToMap' or name=='BuildingRemovedFromMap' then
   local y,building,owner=...
   local row=P.Info('Buildings',building)
   if row and type(row.BuildingType)=='string' and row.BuildingType:match('^BUILDING_SPC_') then return end
   if P.Observe then P.Observe('dispatch',name) end
   fn({player=type(owner)=='number' and owner or nil});return
  end
  if name=='PlayerTurnActivated' then
   if type(pid)~='number' then return end
   local turn=Game.GetCurrentGameTurn();if lastTurn[pid]==turn then return end
   lastTurn[pid]=turn;if P.Observe then P.Observe('dispatch',name) end;fn({player=pid});return
  end
  -- Civ VI native city/worker/governor events start with player ID. Events with
  -- plot-first or transfer signatures intentionally retain a full safety scope.
  if P.Observe then P.Observe('dispatch',name) end
  if name:match('^Governor') or name=='CityWorkerChanged' or name=='CityFocusChanged'
   or name=='CityPopulationChanged' then fn({player=pid});return end
  fn()
 end)
end

-- B270 opt-in target owner. Existing Player/Hook contracts stay unchanged for
-- other consumers. Only scalar references survive a synchronous audit.
function SPCRuntimeWork.NewTargets(P,shared,visit,onError)
 local t={pending={},exits={},known={},transfers={}}
 local function report(pid,cid,err)
  local ok,why=pcall(onError,pid,cid,err)
  if not ok then t.error=tostring(why)end
 end
 local function reference(c)
  local r={owner=c:GetOwner(),city=c:GetID()}
  if c.GetX and c.GetY then r.x=c:GetX();r.y=c:GetY() end
  return r
 end
 local function key(r)return tostring(r.owner)..':'..tostring(r.city)end
 local function matches(c,r)
  return c and c:GetOwner()==r.owner and c:GetID()==r.city
   and (r.x==nil or (c:GetX()==r.x and c:GetY()==r.y))
 end
 local function selected(scope,r)
  if type(scope)~='table' then return true end
  return (scope.player==nil or scope.player==r.owner) and (scope.city==nil or scope.city==r.city)
 end
 local function lookup(cs,id)
  if not cs then return end
  if cs.FindID then return cs:FindID(id)end
  for _,c in cs:Members()do if c:GetID()==id then return c end end
 end
 local function resolve(r)
  local p=Players[r.owner];local cs=p and p:GetCities()
  local c=lookup(cs,r.city)
  if matches(c,r)then return c end
 end
 local function put(dst,k,value)
  if dst[k]==nil then local n=0;for _ in pairs(dst)do n=n+1 end;assert(n<2048,'RUNTIME_TARGET_LIMIT')end
  dst[k]=value
 end
 local function run(pid,c)
  local r=reference(c);local k=key(r);P.Count('city_scan')
  if P.IsTestPlayer(pid)then put(t.known,k,r)end
  local ok,err=pcall(visit,pid,c)
  if ok then t.pending[k]=nil else put(t.pending,k,r)end
  report(pid,r.city,not ok and tostring(err) or nil)
  return k
 end
 local transfers
 function t.Retry(scope)
  if transfers then transfers(scope)end
  local seen={}
  for k,e in pairs(t.exits)do if selected(scope,e.ref)then
   local ok,c=pcall(resolve,e.ref)
   -- Keep UNKNOWN/reference changes; only the store's original loss proof can
   -- authorize withdrawal. Never follow a reused ID or coordinate to a new city.
   if ok and c then
    local good,err=pcall(e.fn,c,e.loss)
    report(e.ref.owner,e.ref.city,not good and tostring(err) or nil)
    if good then t.exits[k]=nil;t.pending[k]=nil end
    seen[k]=true
   end
  end end
  for k,r in pairs(t.pending)do if not seen[k] and selected(scope,r)then
   local ok,c=pcall(resolve,r);if ok and c then run(r.owner,c);seen[k]=true end
  end end
  return seen
 end
 transfers=function(scope)
  for k,v in pairs(t.transfers)do if selected(scope,{owner=v.owner,city=v.city})then
   local ok,done=pcall(function()
    local p=Players[v.owner];local cs=p and p:GetCities();local c=lookup(cs,v.city)
    if not c or c:GetOwner()~=v.owner then return false end
    local r=reference(c)
    local candidates={};for k,r in pairs(t.known)do candidates[k]=r end;for k,r in pairs(t.pending)do candidates[k]=r end
    for oldKey,old in pairs(candidates)do
     local samePlace=old.x~=nil and r.x~=nil and old.x==r.x and old.y==r.y
     if old.owner==v.oldOwner and (samePlace or (old.x==nil and old.city==r.city))then
      put(t.pending,key(r),r);t.known[oldKey]=nil;t.pending[oldKey]=nil;break
     end
    end
    return true
   end)
   if ok and done then t.transfers[k]=nil
   elseif not ok then report(v.owner,v.city,tostring(done))end
  end end
 end
 function t.Run(scope)
  local seen=t.Retry(scope)
  for pid,p in pairs(Players)do
   if SPCRuntimeWork.Player(scope,pid) and (type(scope)=='table' and scope.load or P.IsTestPlayer(pid))then
    local ok,err=pcall(function()
     local cs=p:GetCities();if not cs then return end
     if type(scope)=='table' and scope.city~=nil then
      local c=lookup(cs,scope.city);if c and not seen[key(reference(c))]then run(pid,c)end
     else
      for _,c in cs:Members()do
       if not seen[key(reference(c))]then
        run(pid,c) -- plot/unknown metadata falls back only to participants, never guessed radii
       end
      end
     end
    end)
    if not ok then report(pid,'player',tostring(err))end
   end
  end
 end
 local runImpl,retryImpl=t.Run,t.Retry
 function t.Run(scope)
  local ok,err=pcall(runImpl,scope)
  if not ok then t.error=tostring(err);report(type(scope)=='table' and scope.player or 'runtime','player',t.error)end
 end
 function t.Retry(scope)
  local ok,out=pcall(function()
   if type(scope)=='table' and scope.transfer then
    local v=scope.transfer;put(t.transfers,tostring(v.owner)..':'..tostring(v.city),v)
   end
   return retryImpl(scope)
  end)
  if not ok then t.error=tostring(out);report(type(scope)=='table' and scope.player or 'runtime','player',t.error);return {}end
  return out
 end
 function t.Exit(fn)
  return function(c,loss)
   local r=reference(c);local k=key(r)
   put(t.exits,k,{ref=r,loss=loss,fn=fn}) -- retain before the first possibly failing read
   local ok,err=pcall(fn,c,loss)
   if ok then t.exits[k]=nil;t.pending[k]=nil else error(err)end
  end
 end
 function t.Forget(pid,cid)
  local k=tostring(pid)..':'..tostring(cid);t.pending[k]=nil;t.exits[k]=nil;t.known[k]=nil
 end
 -- Shared reset is registered before the first consumer load callback.
 if not shared.RuntimeRetirementHook then
  shared.RuntimeRetirementHook=true
  local e=P.Field(Events,'LoadScreenClose')
  if e and e.Add then e.Add(function()shared.RuntimeRetirementCache={}end)end
 end
 local removed=P.Field(Events,'CityRemovedFromMap')
 if removed and removed.Add then removed.Add(function(pid,cid)
  -- Removal is also emitted during transfers. Invalidate clean stamps only;
  -- exact pending/exit proofs are retained until confirmed cleanup succeeds.
  local all=shared.RuntimeRetirementCache or {};local prefix=tostring(pid)..':'..tostring(cid)..':'
  for _,cache in pairs(all)do for k,stamp in pairs(cache)do
   if stamp:sub(1,#prefix)==prefix then cache[k]=nil end
  end end
 end)end
 return t
end

-- Exact inert tombstones are verified once per current city reference/load.
-- Failure never publishes a clean marker; positive effects remain blocked.
function SPCRuntimeWork.RetireOnce(P,shared,c,tag,fn)
 shared.RuntimeRetirementCache=shared.RuntimeRetirementCache or {}
 local all=shared.RuntimeRetirementCache;all[tag]=all[tag] or {};local cache=all[tag]
 local x,y=c.GetX and c:GetX(),c.GetY and c:GetY()
 local k=x~=nil and (x..':'..y) or (c:GetOwner()..':'..c:GetID())
 local token=c.GetProperty and c:GetProperty('SPC_DEV_BINDING_B013_TOKEN') or ''
 local stamp=table.concat({c:GetOwner(),c:GetID(),tostring(x),tostring(y),tostring(token)},':')
 if cache[k]==stamp then return 0 end
 local n=fn()
 if cache[k]==nil then local count=0;for _ in pairs(cache)do count=count+1 end;assert(count<2048,'RETIREMENT_CACHE_LIMIT')end
 cache[k]=stamp;return n
end

function SPCRuntimeWork.TargetHook(P,source,name,fn)
 local e=P.Field(source,name);if not e or not e.Add then return end
 -- These signatures are verified in native CityBannerManager/ObserverCamera
 -- and the existing progression completion owner; unknown forms stay bounded.
 if name=='DistrictBuildProgressChanged' or name=='DistrictAddedToMap'
  or name=='DistrictPillaged' or name=='DistrictRepaired' then
  e.Add(function(pid,did,cid)
   fn({player=type(pid)=='number' and pid or nil,city=type(cid)=='number' and cid or nil})
  end)
 elseif name=='CityTransfered' then
  e.Add(function(owner,cid,oldOwner)
   if type(owner)=='number' and type(cid)=='number' and type(oldOwner)=='number'then
    fn({transfer={owner=owner,city=cid,oldOwner=oldOwner}})
   else fn({})end
  end)
 elseif name=='ImprovementAddedToMap' or name=='ImprovementRemovedFromMap' or name=='FeatureRemovedFromMap' then
  e.Add(function(x,y)fn(type(x)=='number' and type(y)=='number' and {plot={x,y}} or {})end)
 elseif name=='CityWorkerChanged' or name=='CityFocusChanged' or name=='CityPopulationChanged' then
  e.Add(function(pid,cid)fn({player=type(pid)=='number' and pid or nil,city=type(cid)=='number' and cid or nil})end)
 elseif source==GameEvents and name=='OnDistrictConstructed' then
  e.Add(function(pid)fn({player=type(pid)=='number' and pid or nil})end)
 else SPCRuntimeWork.Hook(P,source,name,fn)end
end
