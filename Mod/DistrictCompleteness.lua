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
function M.Calculate(catalog,raw)
 local out={districts={},domains={},excluded={},catalogRevision=catalog.revision}
 local seen={}
 table.sort(raw.districts,function(a,b) return a.id<b.id end)
 for _,d in ipairs(raw.districts) do
  assert(not seen[d.id],'DC_DUPLICATE_DISTRICT');seen[d.id]=true
  local domain=catalog.Domain(d.type)
  local r={id=d.id,type=d.type,plot=d.plot,domain=domain,complete=d.complete,pillaged=d.pillaged,buildings={},uncapped=0,value=0}
  bool(d.complete,'DC_COMPLETION_UNKNOWN');bool(d.pillaged,'DC_DISTRICT_PILLAGE_UNKNOWN')
  for _,b in ipairs(d.buildings) do
   local c=catalog.buildings[b.index] or {type=tostring(b.index),reason='UNREVIEWED_BUILDING'}
   local v={type=c.type,name=c.name,tier=c.tier,tierSource=c.tierSource,ordinary=c.ordinary==true,
    complete=b.complete,pillaged=b.pillaged,contribution=0,reason=c.reason}
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
 for _,b in ipairs(raw.unplaced or {}) do out.excluded[#out.excluded+1]=clone(b) end
 return out
end
function M.Start(P,shared)
 local cache,catalog={},nil
 local clock,revision,epoch=0,0,1
 local data={};shared.DistrictCompleteness=data
 local function count(n) P.Count('dc_'..n) end
 local function key(pid,cid) return tostring(pid)..':'..tostring(cid) end
 local function ref(pid,c,token)
  assert(c:GetOwner()==pid,'DC_OWNER_CHANGED')
  return {owner=pid,id=c:GetID(),x=c:GetX(),y=c:GetY(),token=token}
 end
 local function capture(pid,c)
  count('capture')
  catalog=catalog or SPCOrdinaryBuildingCatalog.Build(P)
  local buildings=c:GetBuildings();local districts=c:GetDistricts()
  local raw={districts={},unplaced={}};local seen={};local byPlot={}
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
  -- One DB catalog pass for this selected city, not one pass per district/player.
  -- Includes non-ordinary entries so exclusions remain visible in diagnostics.
  for row in GameInfo.Buildings() do
   local index=row.Index;P.Count('building_check')
   if bool(buildings:HasBuilding(index),'DC_BUILDING_COMPLETION_UNKNOWN') then
    seen[index]=true
    local location=buildings:GetBuildingLocation(index)
    local located=type(location)=='number' and location>=0
    local entry=catalog.buildings[index]
    assert(located or not (entry and entry.ordinary),'DC_BUILDING_LOCATION_UNAVAILABLE')
    local pillaged=bool(buildings:IsPillaged(index),'DC_BUILDING_PILLAGE_UNKNOWN')
    local rec=located and byPlot[location]
    if rec then
     rec.buildings[#rec.buildings+1]={index=index,complete=true,pillaged=pillaged}
    else
     -- Wonders/internal objects can live off district plots. Never drop a known
     -- ordinary building silently: that would publish an incomplete D as zero.
     assert(not (entry and entry.ordinary),'DC_ORDINARY_LOCATION_UNRESOLVED')
     raw.unplaced[#raw.unplaced+1]={type=row.BuildingType,reason=entry and entry.reason or 'UNREVIEWED_BUILDING',
      contribution=0,pillaged=pillaged,plot=location}
    end
   end
  end
  -- Only the current unfinished Building is diagnostic evidence, not a contribution.
  local current=c:GetBuildQueue():CurrentlyBuilding();local row=P.Info('Buildings',current)
  if row and not seen[row.Index] and not buildings:HasBuilding(row.Index) then
   raw.unplaced[#raw.unplaced+1]={type=row.BuildingType,reason='UNDER_CONSTRUCTION',contribution=0,pillaged=false}
  end
  assert(c:GetOwner()==pid,'DC_OWNER_CHANGED_DURING_READ')
  return M.Calculate(catalog,raw)
 end
 function data.MarkDirty(pid,cid)
  -- At most eight cached city entries, no native reads, strings or event history.
  for _,e in pairs(cache) do
   if (pid==nil or e.ref.owner==pid) and (cid==nil or e.ref.id==cid) and not e.dirty then
    e.dirty=true;count('dirty')
   end
  end
 end
 function data.Read(pid,c,token)
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
   e.dirty=false;e.turn=turn
   local ok,value=pcall(capture,pid,c)
   if ok and same(current,ref(pid,c,token)) then
    if not e.value or not same(e.value,value) then revision=revision+1;e.revision=revision;count('publish') end
    e.value=value;e.error=nil
   else e.error=ok and 'DC_REFERENCE_CHANGED' or tostring(value);count('failure') end
  else count('hit') end
  return {schema=1,epoch=epoch,reference=clone(current),validity=e.value and 'VERIFIED' or 'UNKNOWN',
   availability=e.error and 'TEMPORARILY_UNAVAILABLE' or 'READY',error=e.error,
   revision=e.revision,value=e.value and clone(e.value) or nil}
 end
 function data.CacheSize() local n=0;for _ in pairs(cache) do n=n+1 end;return n end
 local function hook(source,name,fn)
  local event=P.Field(source,name);if event and event.Add then event.Add(fn) end
 end
 -- Generic Publish/Playback/UI ticks and unit movement are deliberately absent.
 for _,name in ipairs({'CityBuildingsChanged'}) do hook(Events,name,function(pid,cid) data.MarkDirty(pid,cid) end) end
 for _,name in ipairs({'DistrictAddedToMap','DistrictRemovedFromMap','DistrictBuildProgressChanged','DistrictPillaged','BuildingPillaged','CityTransfered','CityRemovedFromMap'}) do
  hook(Events,name,function() data.MarkDirty() end) -- signatures vary; bounded dirty marks only
 end
 for _,name in ipairs({'BuildingConstructed','OnDistrictConstructed','OnPillage','CityBuilt'}) do
  hook(GameEvents,name,function() data.MarkDirty() end)
 end
 hook(Events,'LoadScreenClose',function() cache={};catalog=nil;epoch=epoch+1 end)
 for _,name in ipairs({'BuildingAddedToMap','BuildingRemovedFromMap'}) do
  hook(Events,name,function(x,y,id)
   local row=P.Info('Buildings',id)
   if row and type(row.BuildingType)=='string' and row.BuildingType:match('^BUILDING_SPC_') then return end
   data.MarkDirty()
  end)
 end
 -- Missed native events: next explicit read in a new turn reconciles once.
 if shared.CityProgressionStore then shared.CityProgressionStore.RegisterReturn('DistrictCompleteness',function(pid)data.MarkDirty() end)end

end
M.Clone=clone
