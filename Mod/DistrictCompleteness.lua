-- P0-A shared read-only fact owner. Lazy scoped refresh; no effect/persistence writes.
SPCDistrictCompleteness={}
local M=SPCDistrictCompleteness
local function clone(v)
 if type(v)~='table' then return v end
 local t={};for k,x in pairs(v) do t[k]=clone(x) end;return t
end
local function same(a,b)
 if type(a)~=type(b) then return false end
 if type(a)~='table' then return a==b end
 for k,v in pairs(a) do if not same(v,b[k]) then return false end end
 for k in pairs(b) do if a[k]==nil then return false end end
 return true
end
local function bool(v,code) assert(type(v)=='boolean',code);return v end
-- Pure calculation consumes a complete native sample and reviewed catalog only.
function M.Calculate(catalog,raw,detail)
 detail=detail~=false
 local out={districts={},domains={},catalogRevision=catalog.revision}
 if detail then out.excluded={} end
 local seen={}
 table.sort(raw.districts,function(a,b) return a.id<b.id end)
 for _,d in ipairs(raw.districts) do
  assert(not seen[d.id],'DC_DUPLICATE_DISTRICT');seen[d.id]=true
  local domain=catalog.Domain(d.type)
  local r={id=d.id,type=d.type,plot=d.plot,domain=domain,baseDistrict=catalog.District and catalog.District(d.type) or domain,complete=d.complete,pillaged=d.pillaged,buildings={},uncapped=0,value=0}
  bool(d.complete,'DC_COMPLETION_UNKNOWN');bool(d.pillaged,'DC_DISTRICT_PILLAGE_UNKNOWN')
  for _,b in ipairs(d.buildings) do
   local c=catalog.buildings[b.index] or {type=tostring(b.index),reason='UNREVIEWED_BUILDING'}
   local v={type=c.type,name=detail and c.name or nil,tier=c.tier,tierSource=detail and c.tierSource or nil,ordinary=c.ordinary==true,
    complete=b.complete,pillaged=b.pillaged,contribution=0,reason=c.reason,
    ordinaryReason=c.ordinaryReason,ordinaryDistrict=c.ordinaryDistrict,depthEligible=c.depthEligible~=false}
   bool(b.complete,'DC_BUILDING_COMPLETION_UNKNOWN');bool(b.pillaged,'DC_BUILDING_PILLAGE_UNKNOWN')
   if not b.complete then v.reason='UNDER_CONSTRUCTION'
   elseif not c.ordinary or c.tier==nil then -- preserve ontology reason
   elseif not domain then v.reason='DOMAIN_UNMAPPED'
   elseif c.domain~=domain then v.reason='BUILDING_LOCATION_DOMAIN_CONFLICT'
   elseif not d.complete then v.reason='DISTRICT_UNFINISHED'
   elseif d.pillaged then v.reason='DISTRICT_PILLAGED'
   elseif b.pillaged then v.reason='BUILDING_PILLAGED'
   else v.contribution=c.tier;v.reason=c.tier==0 and 'ORDINARY_TIER_ZERO' or 'INCLUDED' end
   r.uncapped=r.uncapped+v.contribution;r.buildings[#r.buildings+1]=v
  end
  table.sort(r.buildings,function(a,b) return a.type<b.type end)
  r.value=math.min(10,r.uncapped);out.districts[#out.districts+1]=r
  if domain and d.complete and not d.pillaged then
   local previous=out.domains[domain]
   -- Stable tie: smallest district ID, never sum multiple instances.
   if not previous or r.value>previous.value then out.domains[domain]={value=r.value,districtID=r.id} end
  end
 end
 if detail then
  -- These small native observations belong to the same confirmed capture;
  -- names/reasons/excluded display rows are materialized only on explicit Read.
  for _,b in ipairs(raw.observations or {}) do
   local entry=catalog.buildings[b.index]
   out.excluded[#out.excluded+1]={type=entry.type,reason=entry.reason or 'UNREVIEWED_BUILDING',
    contribution=0,pillaged=b.pillaged,plot=b.plot}
  end
  if raw.queued then
   out.excluded[#out.excluded+1]={type=raw.queued,reason='UNDER_CONSTRUCTION',contribution=0,pillaged=false}
  end
  -- Existing pure callers/fixtures may supply already-described unplaced rows.
  for _,b in ipairs(raw.unplaced or {}) do out.excluded[#out.excluded+1]=clone(b) end
 end
 return out
end
function M.Start(P,shared)
 local cache,reports,catalog,buildingOrder={},{},nil,nil
 local businessCount,reportCount=0,0
 local clock,revision,epoch,sampleSerial=0,0,1,0
 local inFlight={}
 local BUSINESS_LIMIT,REPORT_LIMIT,CAPTURE_LIMIT=2048,8,8
 local data={};shared.DistrictCompleteness=data
 function data.RegisterConsumer(name,fn)
  assert(shared.FactChanges,'DC_FACT_REGISTRY_UNAVAILABLE')
  return shared.FactChanges.RegisterConsumer('DC_'..name,fn,{kinds={'D'}})
 end
 local function count(n) P.Count('dc_'..n) end
 local function key(pid,cid) return tostring(pid)..':'..tostring(cid) end
 local function ref(pid,c,token)
  assert(c:GetOwner()==pid,'DC_OWNER_CHANGED')
  return {owner=pid,id=c:GetID(),x=c:GetX(),y=c:GetY(),token=token}
 end
 local function capture(pid,c)
  count('capture')
  if not catalog then
   -- Reuse the already-reviewed static definitions; native city presence is
   -- still read each capture. Never omit non-ordinary diagnostic exclusions.
   local nextCatalog=SPCOrdinaryBuildingCatalog.Build(P);local order={}
   for index,entry in pairs(nextCatalog.buildings) do
    if type(index)=='number' then order[#order+1]=entry end
   end
   table.sort(order,function(a,b)return a.index<b.index end)
   catalog=nextCatalog;buildingOrder=order
  end
  local buildings=c:GetBuildings();local districts=c:GetDistricts()
  local raw={districts={}};local seen={};local byPlot={}
  -- Use indexed Gameplay CityDistricts and Gameplay building locations, not UI enumeration.
  local n=districts:GetNumDistricts()
  assert(type(n)=='number' and n>=0 and n%1==0,'DC_DISTRICT_COUNT_UNAVAILABLE')
  for i=0,n-1 do
   local d=assert(districts:GetDistrictByIndex(i),'DC_DISTRICT_ENTRY_UNAVAILABLE')
   P.Count('district_scan')
   local plot=assert(Map.GetPlot(d:GetX(),d:GetY()),'DC_PLOT_UNAVAILABLE')
   local row=assert(P.Info('Districts',d:GetType()),'DC_DISTRICT_TYPE_UNKNOWN')
   local rec={id=d:GetID(),type=row.DistrictType,plot=plot:GetIndex(),
    complete=bool(d:IsComplete(),'DC_COMPLETION_UNKNOWN'),pillaged=bool(d:IsPillaged(),'DC_DISTRICT_PILLAGE_UNKNOWN'),buildings={}}
   assert(not byPlot[rec.plot],'DC_DUPLICATE_DISTRICT_LOCATION')
   byPlot[rec.plot]=rec;raw.districts[#raw.districts+1]=rec
  end
  -- One cached definition pass for this selected city, not one pass per district/player.
  -- Retain even non-ordinary checks: failures are still availability evidence.
  for _,entry in ipairs(buildingOrder) do
   local index=entry.index;P.Count('building_check')
   if bool(buildings:HasBuilding(index),'DC_BUILDING_COMPLETION_UNKNOWN') then
    seen[index]=true
    local location=buildings:GetBuildingLocation(index)
    local located=type(location)=='number' and location>=0
    assert(located or not (entry and entry.ordinary),'DC_BUILDING_LOCATION_UNAVAILABLE')
    local pillaged=bool(buildings:IsPillaged(index),'DC_BUILDING_PILLAGE_UNKNOWN')
    local rec=located and byPlot[location]
    if rec then
     rec.buildings[#rec.buildings+1]={index=index,complete=true,pillaged=pillaged}
    else
     -- Wonders/internal objects can live off district plots. Never drop a known
     -- ordinary building silently: that would publish an incomplete D as zero.
     assert(not (entry and entry.ordinary),'DC_ORDINARY_LOCATION_UNRESOLVED')
     raw.observations=raw.observations or {}
     raw.observations[#raw.observations+1]={index=index,pillaged=pillaged,plot=location}
    end
   end
  end
  -- Only the current unfinished Building is diagnostic evidence, not a contribution.
  local current=c:GetBuildQueue():CurrentlyBuilding();local row=P.Info('Buildings',current)
  if row and not seen[row.Index] and not buildings:HasBuilding(row.Index) then
   raw.queued=row.BuildingType
  end
  assert(c:GetOwner()==pid,'DC_OWNER_CHANGED_DURING_READ')
  return M.Calculate(catalog,raw,false),raw
 end
 local function valid(v)return type(v)=='number' and v>=0 and v<2147483648 and v%1==0 end
 function data.MarkDirty(pid,cid,cause,transfer)
  if not valid(pid)then pid=nil;cid=nil elseif not valid(cid)then cid=nil end
  if pid~=nil and not P.IsTestPlayer(pid)then return end
  local marked={}
  local function mark(e)if e and not marked[e]then marked[e]=true;e.invalidation=(e.invalidation or 0)+1;if not e.dirty then e.dirty=true;count('dirty')end end end
  if pid~=nil and cid~=nil then mark(cache[key(pid,cid)])
  else for _,e in pairs(cache)do if pid==nil or e.ref.owner==pid then mark(e)end end end
  -- Uncached overflow reads still need the same synchronous invalidation proof.
  for _,e in ipairs(inFlight)do
   if (pid==nil or e.ref.owner==pid)and(cid==nil or e.ref.id==cid)then mark(e)end
  end
  if shared.FactChanges then
   shared.FactChanges.Emit({owner=pid,cityID=cid,kinds={'D'},cause=cause or 'DISTRICT_FACTS_DIRTY',transfer=transfer})
  end
 end
 local function forget(k)
  if cache[k]then cache[k]=nil;businessCount=businessCount-1 end
  if reports[k]then reports[k]=nil;reportCount=reportCount-1 end
 end
 local function reportFor(k,e)
  local row=reports[k]
  if row and row.sample==e.sample and same(row.ref,e.ref)then return row end
 end
 local function retainRaw(k,e,raw)
  clock=clock+1
  if not reports[k]then reportCount=reportCount+1 end
  reports[k]={ref=clone(e.ref),sample=e.sample,raw=raw,used=clock}
  if reportCount>REPORT_LIMIT then
   local oldest,oldKey
   for rk,row in pairs(reports)do
    if rk~=k and(not oldest or row.used<oldest)then oldest=row.used;oldKey=rk end
   end
   reports[oldKey]=nil;reportCount=reportCount-1
  end
 end
 local function writeVersion()
  local facts=shared.EffectiveFacts
  return facts and facts.Version and facts.Version()or nil
 end
 local function read(pid,c,token,detail)
  count('read');assert(P.IsTestPlayer(pid),'DC_OWNER_NOT_ENABLED')
  local current=ref(pid,c,token);local k=key(pid,current.id);local turn=Game.GetCurrentGameTurn()
  for _,active in ipairs(inFlight)do if same(active.ref,current)then
   -- A getter may reenter a consumer before the outer sample is certified.
   -- Return the last complete value as unavailable, never a false fresh hit.
   return {schema=1,epoch=epoch,reference=clone(current),validity=active.value and 'VERIFIED'or 'UNKNOWN',
    availability='TEMPORARILY_UNAVAILABLE',error='DC_CAPTURE_IN_PROGRESS',revision=active.revision,
    value=not detail and active.value and clone(active.value)or nil}
  end end
  local e=cache[k]
  if not e or not same(e.ref,current)then
   if e then forget(k)end
   e={ref=current,dirty=true}
   -- Overflow remains readable; do not evict the supported warm business set.
   if businessCount<BUSINESS_LIMIT then cache[k]=e;businessCount=businessCount+1 end
  end
  local retained=cache[k]==e
  local row=reportFor(k,e)
  -- A report miss may explicitly reacquire raw facts, but cannot turn a failed
  -- sample into an idle retry. Normal compact reads never materialize reports.
  local needsReport=detail and not row and not e.error
  if e.dirty or e.turn~=turn or needsReport then
   e.dirty=false;e.turn=turn;local ticket=e.invalidation or 0
   local readEpoch=epoch;local before=writeVersion()
   local ok,value,raw
   if #inFlight<CAPTURE_LIMIT then
    inFlight[#inFlight+1]=e
    ok,value,raw=pcall(capture,pid,c)
    local refOK,finalRef=pcall(ref,pid,c,token)
    local versionOK,after=pcall(writeVersion)
    inFlight[#inFlight]=nil
    local unchanged=ticket==(e.invalidation or 0)and readEpoch==epoch and(not retained or cache[k]==e)
    if ok and refOK and versionOK and same(current,finalRef)and unchanged and before==after then
     if not e.value or not same(e.value,value)then revision=revision+1;e.revision=revision;count('publish')end
     sampleSerial=sampleSerial+1;e.sample=sampleSerial;e.value=value;e.error=nil
     retainRaw(k,e,raw)
    else
     if not ok then
      local printable,message=pcall(tostring,value);e.error=printable and message:sub(1,180)or 'DC_CAPTURE_FAILED'
     elseif not unchanged then e.error='DC_CHANGED_DURING_CAPTURE'
     elseif not versionOK or before~=after then e.error='DC_WRITE_DURING_CAPTURE'
     else e.error='DC_REFERENCE_CHANGED'end
     count('failure')
    end
   else e.error='DC_CAPTURE_REENTRY_LIMIT';count('failure')end
  else count('hit')end
  local value=e.value
  if detail then
   row=reportFor(k,e);value=nil
   if row then
    clock=clock+1;row.used=clock
    if not row.detail then row.detail=M.Calculate(catalog,row.raw)end
    value=row.detail
   end
  end
  return {schema=1,epoch=epoch,reference=clone(current),validity=e.value and 'VERIFIED'or 'UNKNOWN',
   availability=e.error and 'TEMPORARILY_UNAVAILABLE'or 'READY',error=e.error,
   revision=e.revision,value=value and clone(value)or nil}
 end
 -- One fact/error/reference owner, independent bounded report retention.
 function data.ReadFacts(pid,c,token)return read(pid,c,token,false)end
 function data.Read(pid,c,token)return read(pid,c,token,true)end
 function data.CacheSize()return reportCount end -- compatibility: raw/detail LRU remains eight
 function data.BusinessCacheSize()return businessCount end
 local function hook(source,name,fn)
  local event=P.Field(source,name);if event and event.Add then event.Add(fn) end
 end
 -- Verified player/district/city forms; one normalized scope drives cache and consumers.
 local function dirty(scope)
  scope=scope or {}
  if scope.transfer then
   local t=scope.transfer
   -- Both sides carry the original detached routing hint. A foreign destination
   -- is still meaningful to the supported former owner's cleanup candidates.
   local ok,why=pcall(data.MarkDirty,t.owner,t.city,'NATIVE_CITY_TRANSFERRED',t)
   local good,err=pcall(data.MarkDirty,t.oldOwner,nil,'NATIVE_CITY_TRANSFERRED',t)
   if not ok or not good then
    local safe,text=pcall(tostring,not ok and why or err)
    data.transferError=safe and text:sub(1,180) or 'DISTRICT_TRANSFER_MARK_FAILED'
   end
  else data.MarkDirty(scope.player,scope.city)end
 end
 for _,name in ipairs({'DistrictAddedToMap','DistrictBuildProgressChanged','DistrictPillaged','DistrictRemovedFromMap'})do
  hook(Events,name,function(pid,did,cid)dirty({player=pid,city=cid})end)
 end
 hook(Events,'CityRemovedFromMap',function(pid,cid)
  if valid(pid)and valid(cid)and P.IsTestPlayer(pid)then forget(key(pid,cid))end
  data.MarkDirty(pid,cid)
 end)
 hook(Events,'CityTransfered',function(owner,cid,oldOwner)
  if valid(owner) and valid(cid) and valid(oldOwner)then dirty({transfer={owner=owner,city=cid,oldOwner=oldOwner}})else dirty({})end
 end)
 local function internal(index)
  local ok,row=pcall(P.Info,'Buildings',index)
  return ok and row and type(row.BuildingType)=='string' and row.BuildingType:match('^BUILDING_SPC_')~=nil
 end
 for _,name in ipairs({'BuildingConstructed','BuildingPillageStateChanged'})do
  hook(GameEvents,name,function(pid,cid,index)if not internal(index)then data.MarkDirty(pid,cid)end end)
 end
 hook(GameEvents,'CityBuilt',function(pid,cid)data.MarkDirty(pid,cid)end)
 hook(GameEvents,'OnDistrictConstructed',function(pid)data.MarkDirty(pid)end) -- type/x/y are not cityID
 hook(GameEvents,'OnPillage',function(actor,unit,improvement,building,district,plotId)
  -- This action can carry both building and district metadata; do not infer
  -- an unchanged district from an internal building field.
  local ok,owner=pcall(function()return Map.GetPlotByIndex(plotId):GetOwner()end)
  data.MarkDirty(ok and owner or nil) -- actor may be a foreign raider
 end)
 hook(Events,'LoadScreenClose',function()cache={};reports={};businessCount=0;reportCount=0;catalog=nil;buildingOrder=nil;epoch=epoch+1 end)
 for _,name in ipairs({'BuildingAddedToMap','BuildingRemovedFromMap'}) do
  hook(Events,name,function(x,y,id,owner)
   if internal(id)then return end
   local ok,c=pcall(function()
    local d=CityManager and CityManager.GetDistrictAt and CityManager.GetDistrictAt(x,y)
    return d and d:GetCity() or CityManager and CityManager.GetCityAt and CityManager.GetCityAt(x,y)
   end)
   if ok and c then
    local good,pid,cid=pcall(function()return c:GetOwner(),c:GetID()end)
    if good and valid(pid) and valid(cid) and (not valid(owner) or owner==pid)then
     data.MarkDirty(pid,cid);return
    end
    -- Transfer/rebinding can resolve a different current city. The reliable
    -- event owner wins; its former city ID cannot be inferred from that city.
   end
   data.MarkDirty(owner) -- reliable owner or conservative UNKNOWN; never guess zero
  end)
 end
 -- Missed native events: next explicit read in a new turn reconciles once.
 if shared.CityProgressionStore then shared.CityProgressionStore.RegisterReturn('DistrictCompleteness',function(pid,c)
  -- Store confirmed a return. The old ID may differ; only the same physical
  -- location under the original owner identifies stale compact cache entries.
  if c then
   local ok,x,y=pcall(function()return c:GetX(),c:GetY()end)
   if ok then
    local stale={};for k,e in pairs(cache)do if e.ref.owner==pid and e.ref.x==x and e.ref.y==y then stale[#stale+1]=k end end
    for _,k in ipairs(stale)do forget(k)end
   end
  end
  data.MarkDirty(pid,c and c:GetID()or nil)
 end)end

end
M.Clone=clone
