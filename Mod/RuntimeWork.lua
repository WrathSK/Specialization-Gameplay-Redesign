-- D2: ephemeral batch indexes, never persisted or shared across writes/batches.
SPCRuntimeWork={}
function SPCRuntimeWork.New(P,shared)
 local b={};local byPlayer,live={}, {}
 local effective=shared.EffectiveFacts;local read=effective.NewReader and effective.NewReader() or effective.Read
 function b.Facts(pid,c)
  -- Every lookup revalidates the shared phase's authority/governor/write witness.
  return read(pid,c)
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
-- Known-city traversal performs no all-city enumeration. Native owner/reference
-- checks remain the individual writer's responsibility.
function SPCRuntimeWork.Cities(collection,scope)
 if type(scope)=='table' and scope.city~=nil then
  local done=false
  return function()
   if done then return end;done=true
   local c
   if collection.FindID then c=collection:FindID(scope.city)
   else for _,candidate in collection:Members()do if candidate:GetID()==scope.city then c=candidate;break end end end
   if c then return 1,c end
  end
 end
 return collection:Members()
end
-- Scope-only busy work: no native objects, automatic retry, timers or UNKNOWN
-- recovery. A real reentrant cause arms one later existing publish snapshot.
function SPCRuntimeWork.NewAudit(P,shared,data,label,run)
 local pending={};local total=0;local draining=false
 local function mark(scope)
  local pid=type(scope)=='table' and scope.player or nil
  if pid~=nil and not P.IsTestPlayer(pid)then return false end
  local key=pid==nil and '*' or pid;local q=pending[key]
  if not q then assert(total<2048,'RUNTIME_AUDIT_SCOPE_LIMIT');q={player=pid,cities={}};pending[key]=q;total=total+1 end
  local cid=type(scope)=='table' and scope.city or nil
  if pid==nil or cid==nil then q.all=true;q.cities={}
  elseif not q.all and not q.cities[cid]then
   assert(type(cid)=='number' and cid>=0 and cid%1==0 and total<2048,'RUNTIME_AUDIT_SCOPE_LIMIT')
   q.cities[cid]=true;total=total+1
  end
  return true
 end
 local function audit(scope)
  if type(scope)~='table'then scope=nil end
  if not data.ready then return false end
  if type(scope)=='table' and scope.player~=nil and not P.IsTestPlayer(scope.player)then return false end
  if data.busy then if P.Count then P.Count('busy_skip')end;mark(scope);return false end
  data.busy=true;if P.Observe then pcall(P.Observe,'audit',label)end
  local ok,why=pcall(run,scope);data.busy=false
  local safe,text=pcall(tostring,why)
  data.auditError=not ok and (safe and text:sub(1,180) or 'RUNTIME_AUDIT_FAILED') or nil
  return ok
 end
 local function flush()
  if draining or data.busy or not data.ready or not next(pending)then return false end
  draining=true;local work=pending;pending={};total=0
  if work['*']then audit()else
   for _,q in pairs(work)do
    if q.all then audit({player=q.player})
    else for cid in pairs(q.cities)do audit({player=q.player,city=cid})end end
   end
  end
  draining=false;return true
 end
 local e=P.Field(Events,'GameCoreEventPublishComplete');if e and e.Add then e.Add(flush)end
 local load=P.Field(Events,'LoadScreenClose');if load and load.Add then load.Add(function()pending={};total=0 end)end
 return audit,mark,flush
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
-- Fixed scalar attribution only. No native lookup, retained scope or event history.
function SPCRuntimeWork.NoteScope(P,source,scope)
 if not P.Count then return end
 local native=SPCRuntimeComposition and SPCRuntimeComposition.Native(source) or source
 P.Count('scope_dispatch');P.Count(native==(SPCRuntimeComposition and SPCRuntimeComposition.Native(GameEvents) or GameEvents) and 'scope_gameevents' or 'scope_events')
 local kind=type(scope)=='table' and (scope.transfer and 'transfer' or scope.plot and 'plot' or scope.city~=nil and 'city' or scope.player~=nil and 'player')
 P.Count(kind and ('scope_'..kind) or 'scope_fallback')
 if not kind then P.Count('scope_unknown_signature')elseif kind=='player'then P.Count('scope_player_signature')end
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
   local scope={player=type(owner)=='number' and owner or nil};SPCRuntimeWork.NoteScope(P,source,scope);fn(scope);return
  end
  if name=='PlayerTurnActivated' then
   if type(pid)~='number' then return end
   local turn=Game.GetCurrentGameTurn();if lastTurn[pid]==turn then return end
   lastTurn[pid]=turn;if P.Observe then P.Observe('dispatch',name) end;local scope={player=pid};SPCRuntimeWork.NoteScope(P,source,scope);fn(scope);return
  end
  -- Civ VI native city/worker/governor events start with player ID. Events with
  -- plot-first or transfer signatures intentionally retain a full safety scope.
  if P.Observe then P.Observe('dispatch',name) end
  if name:match('^Governor') or name=='CityWorkerChanged' or name=='CityFocusChanged'
   or name=='CityPopulationChanged' then local scope={player=pid};SPCRuntimeWork.NoteScope(P,source,scope);fn(scope);return end
  SPCRuntimeWork.NoteScope(P,source,nil);fn()
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
 return t
end

-- Composition-owned; never installed lazily under a possibly failed consumer.
function SPCRuntimeWork.StartRetirement(P,shared)
 local d={index={},slots={},count=0};shared.RuntimeRetirement=d
 local function ownerKey(pid,cid)return tostring(pid)..':'..tostring(cid)end
 local function drop(slot)
  local rows=d.index[slot.owner];if rows then rows[slot.key]=nil;if not next(rows)then d.index[slot.owner]=nil end end
 end
 function d.Remember(tag,location,stamp,pid,cid)
  local byTag=d.slots[tag];if not byTag then byTag={};d.slots[tag]=byTag end
  local old=byTag[location]
  if old then drop(old)else assert(d.count<8192,'RETIREMENT_INDEX_LIMIT');d.count=d.count+1 end
  local owner=ownerKey(pid,cid);local slot={tag=tag,location=location,stamp=stamp,owner=owner,key=tag..'|'..location}
  d.index[owner]=d.index[owner] or {};d.index[owner][slot.key]=slot;byTag[location]=slot
 end
 local function clear()
  shared.RuntimeRetirementCache={};d.index={};d.slots={};d.count=0
 end
 local e=P.Field(Events,'LoadScreenClose');if e and e.Add then e.Add(clear)end
 local removed=P.Field(Events,'CityRemovedFromMap')
 if removed and removed.Add then removed.Add(function(pid,cid)
  local k=ownerKey(pid,cid);local rows=d.index[k];if not rows then return end
  d.index[k]=nil
  for _,slot in pairs(rows)do
   local cache=shared.RuntimeRetirementCache and shared.RuntimeRetirementCache[slot.tag]
   if cache and cache[slot.location]==slot.stamp then cache[slot.location]=nil end
   local byTag=d.slots[slot.tag]
   if byTag and byTag[slot.location]==slot then byTag[slot.location]=nil;d.count=d.count-1 end
  end
 end)end
 return d
end

-- Exact inert tombstones are verified once per current city reference/load.
-- Failure never publishes a clean marker; positive effects remain blocked.
function SPCRuntimeWork.RetireOnce(P,shared,c,tag,fn)
 shared.RuntimeRetirementCache=shared.RuntimeRetirementCache or {}
 local all=shared.RuntimeRetirementCache;all[tag]=all[tag] or {};local cache=all[tag]
 local x,y=c.GetX and c:GetX(),c.GetY and c:GetY()
 local k=x~=nil and (x..':'..y) or (c:GetOwner()..':'..c:GetID())
 local token=c.GetProperty and c:GetProperty('SPC_DEV_BINDING_B013_TOKEN') or ''
 local owner,cid=c:GetOwner(),c:GetID()
 local stamp=table.concat({owner,cid,tostring(x),tostring(y),tostring(token)},':')
 if cache[k]==stamp then return 0 end
 local n=fn()
 if cache[k]==nil then local count=0;for _ in pairs(cache)do count=count+1 end;assert(count<2048,'RETIREMENT_CACHE_LIMIT')end
 if shared.RuntimeRetirement then shared.RuntimeRetirement.Remember(tag,k,stamp,owner,cid)end
 cache[k]=stamp;return n
end

function SPCRuntimeWork.TargetHook(P,source,name,fn)
 local e=P.Field(source,name);if not e or not e.Add then return end
 local function native(v)return SPCRuntimeComposition and SPCRuntimeComposition.Native(v) or v end
 local gameplay=native(source)==native(GameEvents)
 local function valid(v)return type(v)=='number' and v>=0 and v<2147483648 and v%1==0 end
 local function scope(pid,cid)
  return {player=valid(pid) and pid or nil,city=valid(pid) and valid(cid) and cid or nil}
 end
 local function scoped(value)if P.Observe then pcall(P.Observe,'dispatch',name)end;pcall(SPCRuntimeWork.NoteScope,P,source,value);return fn(value)end
 if gameplay then
  if name=='BuildingConstructed' or name=='BuildingPillageStateChanged' or name=='CityBuilt'then
   e.Add(function(pid,cid)scoped(scope(pid,cid))end)
  elseif name=='OnDistrictConstructed'then
   e.Add(function(pid)scoped(scope(pid))end) -- district type is NOT cityID
  elseif name=='OnPillage'then
   e.Add(function(actor,unit,improvement,building,district,plotId)
    local ok,owner=pcall(function()return Map.GetPlotByIndex(plotId):GetOwner()end)
    scoped(scope(ok and owner or nil)) -- acting player is not the damaged city owner
   end)
  else e.Add(function()scoped(nil)end)end -- no Events-name inference across namespaces
 elseif name=='DistrictBuildProgressChanged' or name=='DistrictAddedToMap'
  or name=='DistrictPillaged' or name=='DistrictRemovedFromMap' or name=='DistrictRepaired' then
  e.Add(function(pid,did,cid)scoped(scope(pid,cid))end)
 elseif name=='CityTransfered' then
  e.Add(function(owner,cid,oldOwner)
   if valid(owner) and valid(cid) and valid(oldOwner)then scoped({transfer={owner=owner,city=cid,oldOwner=oldOwner}})
   else scoped({})end
  end)
 elseif name=='GovernorAssigned' or name=='GovernorEstablished'then
  e.Add(function(owner,cid,governorOwner)
   local ok,err=pcall(scoped,scope(owner,name=='GovernorEstablished' and cid or nil))
   if valid(governorOwner) and governorOwner~=owner then
    local good,why=pcall(scoped,scope(governorOwner));if not good and ok then ok=false;err=why end
   end
   if not ok then error(err,0)end
  end)
 elseif name=='GovernorChanged' or name=='GovernorPromoted'then
  e.Add(function(pid)scoped(scope(pid))end)
 elseif name=='PlayerTurnActivated'then SPCRuntimeWork.Hook(P,source,name,fn)
 elseif name=='ImprovementAddedToMap' or name=='ImprovementRemovedFromMap' or name=='FeatureRemovedFromMap' then
  e.Add(function(x,y)scoped(type(x)=='number' and type(y)=='number' and {plot={x,y}} or {})end)
 elseif name=='CityWorkerChanged' or name=='CityFocusChanged' or name=='CityPopulationChanged'
  or name=='CityRemovedFromMap' or name=='CityTileOwnershipChanged'then
  e.Add(function(pid,cid)scoped(scope(pid,cid))end)
 elseif name=='BuildingAddedToMap' or name=='BuildingRemovedFromMap'then
  e.Add(function(x,y,index,owner)
   local ok,row=pcall(P.Info,'Buildings',index)
   if ok and row and type(row.BuildingType)=='string' and row.BuildingType:match('^BUILDING_SPC_')then return end
   local found,c=pcall(function()
    local d=CityManager and CityManager.GetDistrictAt and CityManager.GetDistrictAt(x,y)
    return d and d:GetCity() or CityManager and CityManager.GetCityAt and CityManager.GetCityAt(x,y)
   end)
   if found and c then
    local good,pid,cid=pcall(function()return c:GetOwner(),c:GetID()end)
    if good then scoped(scope(pid,cid));return end
   end
   scoped(scope(owner))
  end)
 else SPCRuntimeWork.Hook(P,source,name,fn)end
end

-- One initialization latch. Fallback checks only the Store's scalar lifecycle state.
function SPCRuntimeWork.StartReady(P,shared,name,start)
 local latched=false
 local function attempt(fromLoad)
  if latched then return end
  local store=shared.CityProgressionStore
  if store and type(store.HistoryStartStatus)=='function'then
   local ok,state=pcall(store.HistoryStartStatus)
   if not ok or state=='WAITING'then return end
  elseif not fromLoad then return end
  latched=true -- never repeat initialization/Audit after a callback exception
  start()
 end
 local function bind(event,fn)local e=P.Field(Events,event);if e and e.Add then e.Add(fn)end end
 bind('LoadScreenClose',function()attempt(true)end)
 bind('GameCoreEventPublishComplete',function()attempt(false)end)
 bind('PlayerTurnActivated',function()attempt(false)end)
 if shared.ReadinessSummary and shared.ReadinessSummary.Register then pcall(shared.ReadinessSummary.Register,name)end
 return function()return latched end
end

-- Exact live carrier health only. No policy, prefix ownership or periodic audit.
function SPCRuntimeWork.NativeHealth(P,shared,data,owns,mark)
 local h={};local removing,creating
 local function valid(v)return type(v)=='number' and v>=0 and v<2147483648 and v%1==0 end
 local function guarded(fn,...)
  local ok,err=pcall(fn,...)
  if not ok then local safe,text=pcall(tostring,err);data.healthError=safe and text:sub(1,180) or 'CARRIER_HEALTH_MARK_FAILED'end
 end
 local function scoped(pid,cid)
  if not valid(pid)then pid=nil;cid=nil elseif not valid(cid)then cid=nil end
  if pid~=nil and not P.IsTestPlayer(pid)then return end
  mark({player=pid,city=cid})
 end
 local function coordinate(x,y)
  if Map.GetPlotIndex then return Map.GetPlotIndex(x,y)end
  return Map.GetPlot(x,y):GetIndex()
 end
 local function removed(x,y,index,owner)
  if not owns(index) or valid(owner) and not P.IsTestPlayer(owner)then return end
  local w=removing
  if w and w.owner==owner and w.index==index and valid(w.plot)then
   local ok,plot=pcall(coordinate,x,y);if ok and plot==w.plot then return end
  end
  local ok,c=pcall(function()
   local d=CityManager and CityManager.GetDistrictAt and CityManager.GetDistrictAt(x,y)
   return d and d:GetCity() or CityManager and CityManager.GetCityAt and CityManager.GetCityAt(x,y)
  end)
  if ok and c then
   local good,pid,cid=pcall(function()return c:GetOwner(),c:GetID()end)
   if good and valid(pid) and valid(cid) and (not valid(owner) or owner==pid)then scoped(pid,cid);return end
  end
  scoped(owner) -- identity/location UNKNOWN never means harmless or city zero
 end
 local e=P.Field(Events,'BuildingRemovedFromMap')
 if e and e.Add then e.Add(function(...)guarded(removed,...)end)end
 e=P.Field(GameEvents,'BuildingPillageStateChanged')
 if e and e.Add then e.Add(function(pid,cid,index,state)
  guarded(function()
   if not owns(index)then return end
   local w=creating
   if state==false and w and w.owner==pid and w.city==cid and w.index==index then return end
   scoped(pid,cid) -- confirmed true/UNKNOWN state is never hidden by a busy flag
  end)
 end)end
 local function witness(c,index,plot)
  return {owner=c:GetOwner(),city=c:GetID(),index=index,plot=plot}
 end
 function h.Remove(c,index,plot)
  if plot==nil then
   local ok,value=pcall(function()return c:GetBuildings():GetBuildingLocation(index)end)
   if ok then plot=value end -- optional proof; do not add a new qualification failure
  end
  local prior=removing;removing=witness(c,index,plot)
  local ok,value=pcall(function()return P.RemoveBuilding(c:GetBuildings(),index)end);removing=prior
  if not ok then error(value,0)end;return value
 end
 function h.Create(c,index,plot)
  local prior=creating;creating=witness(c,index,plot)
  local ok,value=pcall(function()return P.CreateBuilding(c:GetBuildQueue(),index)end);creating=prior
  if not ok then error(value,0)end;return value
 end
 return h
end
