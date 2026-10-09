include('CultureMeaningModel')
include('GreatWorkCatalog')
include('CurrentSpecializationFacts')
include('NetworkInput')
-- B166: current derived projection only. No saved ACTIVE/yield authority.
SPCCultureMeaning={}
function SPCCultureMeaning.Start(P,shared)
 assert(not shared.CultureMeaningProbe,'ME_PROBE_CONFLICT')
 local M=SPCCultureMeaningModel
 local d={ready=false,busy=false,records={},errors={},changes=0};shared.CultureMeaning=d
 local ids,coverage;local cleanupPending={};local owned={};for _,name in ipairs(M.Owned)do owned[name]=true end
 function d.IsOwnedCarrier(name)return owned[name]==true end
 local function key(pid,cid)return tostring(pid)..':'..tostring(cid) end
 local function validate()
  if ids then return end
  local nextIDs={}
  for _,name in ipairs(M.Owned)do
   local row=assert(P.Info('Buildings',name),'ME_DEFINITIONS_MISSING')
   assert((row.InternalOnly==1 or row.InternalOnly==true) and row.PrereqDistrict==(M.CarrierDistrict[name] or 'DISTRICT_CITY_CENTER') and row.CitizenSlots==0 and row.Housing==0,'ME_CARRIER_INVALID')
   nextIDs[name]=row.Index
  end
  ids=nextIDs
 end
 local function installed(c,name)
  local has=P.HasBuilding(c:GetBuildings(),ids[name]);assert(type(has)=='boolean','ME_CARRIER_UNKNOWN');return has
 end
 local function project(c,want,expected)
  validate();d.writing=key(c:GetOwner(),c:GetID())
  local ok,why=pcall(function()
   local failure
   -- Same exact removal-before-add algorithm as the native-tested probe.
   for _,name in ipairs(M.Owned)do
    local good,err=pcall(function()
     local has=installed(c,name);local damaged=false
     if has and want[name]then
      damaged=c:GetBuildings():IsPillaged(ids[name]);assert(type(damaged)=='boolean','ME_CARRIER_HEALTH_UNKNOWN')
     end
     if has and (not want[name] or damaged)then
      P.RemoveBuilding(c:GetBuildings(),ids[name]);assert(not installed(c,name),'ME_REMOVE_UNCONFIRMED');d.changes=d.changes+1
     end
    end)
    if not good then failure=failure or err end
   end
   assert(not failure,failure) -- Never add after any unconfirmed withdrawal.
   local function currentOwner()
    if expected then assert(c:GetOwner()==expected.owner and P.IsTestPlayer(expected.owner)
     and SPCNetworkInput.Reference(c)==expected.reference,'ME_REFERENCE_CHANGED')end
   end
   for _,name in ipairs(M.Owned)do if want[name]then
    currentOwner()
    if not installed(c,name)then
     P.CreateBuilding(c:GetBuildQueue(),ids[name]);currentOwner();assert(installed(c,name),'ME_CREATE_UNCONFIRMED');d.changes=d.changes+1
    end
   end end
   currentOwner()
  end)
  d.writing=nil;assert(ok,why)
 end
 local function retire(c)
  assert(shared.GreatWorkAdjacency.retired,'ME_LEGACY_NOT_RETIRED')
  shared.GreatWorkAdjacency.Withdraw(c) -- The legacy module owns its exact IDs.
 end
 local function ready()
  if d.ready then return true end
  if d.busy or d.startupFailed then return false end
  d.busy=true
  local ok,result=pcall(function()
   validate();local cities={};local supported=false
   for _,player in pairs(Players)do local collection=player:GetCities();if collection then
    for _,c in collection:Members()do
     P.Count('city_scan');cities[#cities+1]=c;assert(#cities<=2048,'ME_CLEANUP_SCOPE_LIMIT')
     if P.IsTestPlayer(c:GetOwner())then supported=true end
    end
   end end
   if not supported then return false end -- Missed/early load is not an empty PASS.
   for _,c in ipairs(cities)do
    local good,err=pcall(function()retire(c);project(c,{})end)
    if not good then local k=key(c:GetOwner(),c:GetID());d.errors[k]=tostring(err):sub(1,180);cleanupPending[k]=true end
   end
   -- This bounded immutable proof is reused for every city in this loaded game.
   coverage=M.RecipientCoverage(P);d.recipientStatus=coverage.status;d.recipientCount=coverage.verified
   d.ready=true;return true
  end)
  d.busy=false
  if not ok then d.startupFailed=true;d.startupError=tostring(result):sub(1,180)end
  return ok and result
 end
 local function reconcile(pid,c)
  assert(P.IsTestPlayer(pid) and c:GetOwner()==pid,'ME_OWNER_UNKNOWN')
  local k=key(pid,c:GetID());local reference=SPCNetworkInput.Reference(c);local old=d.records[k]
  -- A previously failed retirement is retried only for this affected city.
  if cleanupPending[k]then retire(c);project(c,{});cleanupPending[k]=nil end
  local ok,p=pcall(function()
   local f=SPCCurrentSpecializationFacts.Read(P,shared,pid,c)
   local w=shared.GreatWorkFacts.Summary(pid,c:GetID())
   if w then assert(w.reference==reference,'ME_REFERENCE_CHANGED')end
   local plan=M.Plan(f,w,nil)
   if plan.status=='NEEDS_DEPTH'then
    assert(coverage and coverage.status=='VERIFIED_LOADED_SET','ME_RECIPIENT_CATALOG_UNVERIFIED')
    if plan.count==0 then plan.status='READY'
    else plan=M.Plan(f,w,shared.DistrictCompleteness.ReadFacts(pid,c,f.token))end
   end
   return plan
  end)
  if not ok then
   local code=tostring(p)
   -- Temporary UNKNOWN on the same reference retains only a confirmed session
   -- projection. Cold load/new reference never replays saved carrier authority.
   if not old or old.reference~=reference or code:find('ME_FIXTURE_UNSUPPORTED_WORK',1,true)
    or code:find('ME_RECIPIENT_',1,true) or code:find('ME_REFERENCE_CHANGED',1,true)then
    project(c,{});d.records[k]=nil
   end
   error(p)
  end
  assert(c:GetOwner()==pid and SPCNetworkInput.Reference(c)==reference,'ME_REFERENCE_CHANGED')
  local want={}
  if p.status=='READY' and p.count>0 then
   for _,y in ipairs(M.ActiveWriteYields)do for _,name in ipairs(M.Parts(y,p.each[y]))do want[name]=true end end
  end
  local written,why=pcall(project,c,want,{owner=pid,reference=reference})
  if not written then
   -- A partially failed new projection is never mixed with the old writer.
   local cleared,err=pcall(project,c,{})
   d.records[k]=nil;error(cleared and why or err)
  end
  p.reference=reference;p.owner=pid;p.cityID=c:GetID();p.x=c:GetX();p.y=c:GetY()
  d.records[k]=p;d.errors[k]=nil
 end
 function d.Audit(scope)
  if scope and scope.player~=nil and not P.IsTestPlayer(scope.player)then return end
  if d.busy then
   -- Merge only reentrant recalculation, never ordered ownership transitions.
   local nextScope={player=scope and scope.player,city=scope and scope.city}
   if d.pending then
    if d.pending.player~=nextScope.player then nextScope.player=nil;nextScope.city=nil
    elseif d.pending.city~=nextScope.city then nextScope.city=nil end
   end
   d.pending=nextScope;return false,'BUSY'
  end
  if not ready()then return false,'NOT_READY'end
  if d.pending and not d.draining then
   if not scope or d.pending.player~=scope.player then scope=nil
   elseif d.pending.city~=scope.city then scope={player=scope.player}end
   d.pending=nil
  end
  d.busy=true
  local ok,why=pcall(function()
   for pid,player in pairs(Players)do if P.IsTestPlayer(pid) and (not scope or scope.player==nil or scope.player==pid)then
    local collection=player:GetCities();local present={}
    local function visit(c)
     present[key(pid,c:GetID())]=true;P.Count('city_scan')
     local good,err=pcall(reconcile,pid,c)
     if not good then d.errors[key(pid,c:GetID())]=tostring(err):sub(1,180)end
    end
    if scope and scope.city~=nil then
     local c=collection:FindID(scope.city);if c and c:GetOwner()==pid then visit(c)end
    else
     for _,c in collection:Members()do if c:GetOwner()==pid then visit(c)end end
     -- Completed/removed city session entries have no independent authority.
     for k,p in pairs(d.records)do if p.owner==pid and not present[k]then d.records[k]=nil end end
     local prefix=pid..':'
     for k in pairs(d.errors)do if k:sub(1,#prefix)==prefix and not present[k]then d.errors[k]=nil;cleanupPending[k]=nil end end
    end
   end end
  end)
  d.busy=false;d.error=not ok and tostring(why):sub(1,180) or nil
  if d.pending and not d.draining then
   local pending=d.pending;d.pending=nil;d.draining=true
   local drained,err=pcall(d.Audit,pending);d.draining=false
   if not drained then d.error=tostring(err):sub(1,180);return false end
  end -- One immediate catch-up; further invalidation waits for the next real boundary.
  return ok
 end
 function d.CollectionConfirmed(pid)
  if not P.IsTestPlayer(pid)then return false end
  if not d.ready then return d.Audit({player=pid})end
  return true -- Changed current facts already notify the exact cities below.
 end
 function d.Describe(pid,c)
  local k=key(pid,c:GetID());local p=d.records[k];local err=d.errors[k] or d.startupError or d.error
  if p and p.reference~=SPCNetworkInput.Reference(c)then p=nil end
  local labels={SCIENCE='科技',PRODUCTION='生产力',GOLD='金币',FOOD='食物',FAITH='信仰'}
  local lines={'意义延展｜自动生效（无需手动启用）'}
  if err then lines[#lines+1]='待复核：'..(err:match('ME_[A-Z_]+') or '当前事实未就绪')end
  if not p then lines[#lines+1]='等待当前资格与馆藏确认；不按旧收益快照恢复。'
  elseif p.status=='INACTIVE'then lines[#lines+1]='当前未生效：需要文化身份、Potential IV及ACTIVE IV。'
  else
   lines[#lines+1]=string.format('合格巨作%d件｜ACTIVE %s',p.count,tostring(p.active))
   for _,y in ipairs(M.ActiveWriteYields)do lines[#lines+1]=string.format('%s：每件%d｜全城基值%d',labels[y],p.each[y],p.total[y])end
  end
  lines[#lines+1]='以上为主题化前追加基值；原生主题化及城市加成可改变最终显示。'
  lines[#lines+1]='市政／外交文化追加暂延期；旧巨作相邻收益已退役。'
  return table.concat(lines,'\n')
 end
 local function bind(source,name,fn)local e=P.Field(source,name);if e and e.Add then e.Add(fn)end end
 bind(Events,'LoadScreenClose',function()
  d.pending=nil;d.ready=false;d.startupFailed=nil;d.startupError=nil;d.records={};d.errors={};cleanupPending={};ids=nil;coverage=nil;d.Audit()
 end)
 bind(Events,'CityBuildingsChanged',function(pid,cid)
  if d.writing==key(pid,cid)then return end
  d.Audit({player=pid,city=cid})
 end)
 for _,name in ipairs({'BuildingAddedToMap','BuildingRemovedFromMap'})do bind(Events,name,function(x,y,id,owner)
  local row=P.Info('Buildings',id);local typ=row and row.BuildingType
  if typ and (owned[typ] or shared.GreatWorkAdjacency.IsOwnedCarrier(typ) or shared.Dialogue.IsOwnedCarrier(typ)
   or shared.CultureInspiration and shared.CultureInspiration.IsOwnedCarrier(typ)
   or SPCCultureAesthetic and typ==SPCCultureAesthetic.Carrier)then return end
  if type(owner)=='number' and not P.IsTestPlayer(owner)then return end
  local ok,c=pcall(function()local district=CityManager.GetDistrictAt and CityManager.GetDistrictAt(x,y);return district and district:GetCity() or CityManager.GetCityAt(x,y)end)
  if ok and c and (owner==nil or c:GetOwner()==owner)then d.Audit({player=c:GetOwner(),city=c:GetID()})
  else d.Audit({player=owner})end
 end)end
 -- Only signatures already verified by the current UI/Gameplay paths are scoped.
 for _,name in ipairs({'GovernorAssigned','GovernorEstablished'})do bind(Events,name,function(owner,cid,governorOwner)
  if type(owner)=='number' and type(cid)=='number'then
   -- Assignment can also deactivate the former city; that ID is absent here.
   d.Audit({player=owner,city=name=='GovernorEstablished' and cid or nil})
   if type(governorOwner)=='number' and governorOwner~=owner then d.Audit({player=governorOwner})end
  else d.Audit()end
 end)end
 for _,name in ipairs({'GovernorPromoted','GovernorChanged'})do bind(Events,name,function(pid)d.Audit({player=type(pid)=='number' and pid or nil})end)end
 for _,name in ipairs({'DistrictRemovedFromMap','DistrictBuildProgressChanged'})do bind(Events,name,function(pid,districtID,cid)
  d.Audit({player=type(pid)=='number' and pid or nil,city=type(cid)=='number' and cid or nil})
 end)end
 for _,name in ipairs({'BuildingPillaged','BuildingRepaired','DistrictPillaged','DistrictRepaired','CityTransfered','CityRemovedFromMap'})do
  bind(Events,name,function()d.Audit()end) -- native signatures unresolved: supported player only
 end
 for _,name in ipairs({'BuildingConstructed','OnDistrictConstructed','OnPillage','CityBuilt'})do bind(GameEvents,name,function()d.Audit()end)end
 local lastTurn
 bind(Events,'PlayerTurnActivated',function(pid)
  if not P.IsTestPlayer(pid)then return end
  local turn=Game.GetCurrentGameTurn();if lastTurn~=turn then lastTurn=turn;d.Audit({player=pid})end
 end)
 local previous=shared.GreatWorkFacts.OnConfirmed
 shared.GreatWorkFacts.OnConfirmed=function(pid,changed)
  if previous then previous(pid,changed)end
  if not P.IsTestPlayer(pid)then return end
  if not d.ready then d.Audit({player=pid});return end
  for _,cid in ipairs(changed)do d.Audit({player=pid,city=cid})end
 end
 local store=shared.CityProgressionStore
 if store then
  store.RegisterExit('CultureMeaning',function(c,loss)
   assert(store.IsExitTarget(c,loss),'ME_EXIT_UNCONFIRMED');store.RemoveOwned(c,loss,M.Owned)
   for k,p in pairs(d.records)do if p.owner==loss.origin.owner and p.x==c:GetX() and p.y==c:GetY()then d.records[k]=nil;d.errors[k]=nil end end
  end)
  store.RegisterReturn('CultureMeaning',function(pid,c)d.Audit({player=pid,city=c:GetID()})end)
 end
 return d
end
