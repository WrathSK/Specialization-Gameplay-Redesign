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
 local cache,catalog,buildingOrder={},nil,nil
 local clock,revision,epoch=0,0,1
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
 function data.MarkDirty(pid,cid,cause)
  if not valid(pid)then pid=nil;cid=nil elseif not valid(cid)then cid=nil end
  if pid~=nil and not P.IsTestPlayer(pid)then return end
  local function mark(e)if e then e.invalidation=(e.invalidation or 0)+1;if not e.dirty then e.dirty=true;count('dirty')end end end
  if pid~=nil and cid~=nil then mark(cache[key(pid,cid)])
  else for _,e in pairs(cache)do if pid==nil or e.ref.owner==pid then mark(e)end end end
  if shared.FactChanges then
   shared.FactChanges.Emit({owner=pid,cityID=cid,kinds={'D'},cause=cause or 'DISTRICT_FACTS_DIRTY'})
  end
 end
 local function read(pid,c,token,detail)
  count('read');assert(P.IsTestPlayer(pid),'DC_OWNER_NOT_ENABLED')
  local current=ref(pid,c,token);local k=key(pid,current.id);local turn=Game.GetCurrentGameTurn()
  local e=cache[k]
  if not e or not same(e.ref,current) then
   e={ref=current,dirty=true};cache[k]=e
  end
  clock=clock+1;e.used=clock
  local n=0;local oldest,oldKey
  for ck,ce in pairs(cache) do n=n+1;if ck~=k and (not oldest or ce.used<oldest) then oldest=ce.used;oldKey=ck end end
  if n>8 then cache[oldKey]=nil end
  if e.dirty or e.turn~=turn then
   e.dirty=false;e.turn=turn;local ticket=e.invalidation or 0
   local ok,value,raw=pcall(capture,pid,c)
   local refOK,finalRef=pcall(ref,pid,c,token)
   if ok and refOK and same(current,finalRef) and ticket==(e.invalidation or 0) then
    if not e.value or not same(e.value,value) then revision=revision+1;e.revision=revision;count('publish') end
    e.value=value;e.raw=raw;e.detail=nil;e.error=nil
   else e.error=ok and (ticket~=(e.invalidation or 0) and 'DC_CHANGED_DURING_CAPTURE' or 'DC_REFERENCE_CHANGED') or tostring(value);count('failure') end
  else count('hit') end
  local value=e.value
  if detail and e.raw then
   if not e.detail then e.detail=M.Calculate(catalog,e.raw) end
   value=e.detail
  end
  return {schema=1,epoch=epoch,reference=clone(current),validity=e.value and 'VERIFIED' or 'UNKNOWN',
   availability=e.error and 'TEMPORARILY_UNAVAILABLE' or 'READY',error=e.error,
   revision=e.revision,value=value and clone(value) or nil}
 end
 -- Both projections share one confirmed sample/error/ref/revision owner. The
 -- compact copy keeps all eligibility guards; neither returns mutable cache.
 function data.ReadFacts(pid,c,token)return read(pid,c,token,false) end
 function data.Read(pid,c,token)return read(pid,c,token,true) end
 function data.CacheSize() local n=0;for _ in pairs(cache) do n=n+1 end;return n end
 local function hook(source,name,fn)
  local event=P.Field(source,name);if event and event.Add then event.Add(fn) end
 end
 -- Verified player/district/city forms; one normalized scope drives cache and consumers.
 local function dirty(scope)
  scope=scope or {}
  if scope.transfer then
   local t=scope.transfer;data.MarkDirty(t.owner,t.city);data.MarkDirty(t.oldOwner)
  else data.MarkDirty(scope.player,scope.city)end
 end
 for _,name in ipairs({'DistrictAddedToMap','DistrictBuildProgressChanged','DistrictPillaged','DistrictRemovedFromMap'})do
  hook(Events,name,function(pid,did,cid)dirty({player=pid,city=cid})end)
 end
 hook(Events,'CityRemovedFromMap',function(pid,cid)data.MarkDirty(pid,cid)end)
 hook(Events,'CityTransfered',function(owner,cid,oldOwner)
  if type(owner)=='number' and type(cid)=='number' and type(oldOwner)=='number'then dirty({transfer={owner=owner,city=cid,oldOwner=oldOwner}})else dirty({})end
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
 hook(Events,'LoadScreenClose',function() cache={};catalog=nil;buildingOrder=nil;epoch=epoch+1 end)
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
 if shared.CityProgressionStore then shared.CityProgressionStore.RegisterReturn('DistrictCompleteness',function(pid,c)data.MarkDirty(pid,c and c:GetID() or nil) end)end

end
M.Clone=clone
