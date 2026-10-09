include('CultureInspirationModel')
include('CurrentSpecializationFacts')
include('NetworkInput')
-- Current derived city effect. No Property, investment or historical GPP ledger.
SPCCultureInspiration={}
function SPCCultureInspiration.Start(P,shared)
 assert(shared.CultureInspirationProbe and shared.CultureInspirationProbe.retired,'INSP_PROBE_NOT_RETIRED')
 local M=SPCCultureInspirationModel
 local d={ready=false,busy=false,records={},errors={},changes=0};shared.CultureInspiration=d
 local ids;local pendingCleanup={};local owned={}
 for _,name in ipairs(M.Owned)do owned[name]=true end
 function d.IsOwnedCarrier(name)return owned[name]==true end
 local function key(pid,cid)return tostring(pid)..':'..tostring(cid)end
 local function validate()
  if ids then return end
  local nextIDs={};local args,attachments={},{}
  for _,a in ipairs(assert(P.Rows('ModifierArguments'),'INSP_DB_UNKNOWN'))do
   if a.ModifierId:find('^SPC_INSPIRATION_ERA_')then args[a.ModifierId]=args[a.ModifierId] or {};args[a.ModifierId][a.Name]=a.Value end
  end
  for _,a in ipairs(assert(P.Rows('BuildingModifiers'),'INSP_DB_UNKNOWN'))do
   if owned[a.BuildingType]then attachments[a.BuildingType]=attachments[a.BuildingType] or {};table.insert(attachments[a.BuildingType],a.ModifierId)end
  end
  local dm=assert(P.Info('DynamicModifiers','MODIFIER_CITY_INCREASE_GREAT_PERSON_POINT_BONUS'),'INSP_EFFECT_MISSING')
  assert(dm.CollectionType=='COLLECTION_OWNER' and dm.EffectType=='EFFECT_ADJUST_CITY_GREAT_PERSON_POINTS_MODIFIER','INSP_EFFECT_SCOPE_INVALID')
  for e,name in ipairs(M.Owned)do
   local b=assert(P.Info('Buildings',name),'INSP_DEFINITION_MISSING');local mid='SPC_INSPIRATION_ERA_'..e
   local m=assert(P.Info('Modifiers',mid),'INSP_MODIFIER_MISSING');local a=args[mid];local links=attachments[name]
   assert((b.InternalOnly==1 or b.InternalOnly==true) and b.PrereqDistrict=='DISTRICT_CITY_CENTER' and b.CitizenSlots==0 and b.Housing==0,'INSP_CARRIER_INVALID')
   assert(m.ModifierType=='MODIFIER_CITY_INCREASE_GREAT_PERSON_POINT_BONUS' and not m.OwnerRequirementSetId and not m.SubjectRequirementSetId,'INSP_MODIFIER_INVALID')
   assert(a and tonumber(a.Amount)==e*M.PercentPerEra and a.GreatPersonClassType==nil,'INSP_AMOUNT_INVALID')
   assert(links and #links==1 and links[1]==mid,'INSP_ATTACHMENT_INVALID');nextIDs[name]=b.Index
  end
  ids=nextIDs
 end
 local function present(c,name)
  local v=P.HasBuilding(c:GetBuildings(),ids[name]);assert(type(v)=='boolean','INSP_PRESENCE_UNKNOWN');return v
 end
 local function project(c,want,expected)
  validate();d.writing=key(c:GetOwner(),c:GetID())
  local function current()
   if expected then assert(c:GetOwner()==expected.owner and P.IsTestPlayer(expected.owner)
    and SPCNetworkInput.Reference(c)==expected.reference,'INSP_REFERENCE_CHANGED')end
  end
  local ok,why=pcall(function()
   local failure
   for _,name in ipairs(M.Owned)do
    local good,err=pcall(function()
     local has=present(c,name);local damaged=false
     if has and name==want then damaged=c:GetBuildings():IsPillaged(ids[name]);assert(type(damaged)=='boolean','INSP_HEALTH_UNKNOWN')end
     if has and (name~=want or damaged)then
      P.RemoveBuilding(c:GetBuildings(),ids[name]);assert(not present(c,name),'INSP_REMOVE_UNCONFIRMED');d.changes=d.changes+1
     end
    end)
    if not good then failure=failure or err end
   end
   assert(not failure,failure);current()
   if want and not present(c,want)then
    P.CreateBuilding(c:GetBuildQueue(),ids[want]);current()
    assert(present(c,want),'INSP_CREATE_UNCONFIRMED');d.changes=d.changes+1
   end
   current()
  end)
  d.writing=nil;assert(ok,why)
 end
 local function withdraw(c)
  -- Both modules withdraw only exact owned IDs. A failure cannot authorize a new value.
  local ok,why=pcall(shared.CultureInspirationProbe.Withdraw,c)
  local cleared,err=pcall(project,c,nil)
  assert(ok and cleared,not ok and why or err)
 end
 local function ready()
  if d.ready then return true end
  if d.startupFailed then return false end
  d.busy=true
  local ok,result=pcall(function()
   validate();local all={};local supported=false
   for _,player in pairs(Players)do local cities=player:GetCities();if cities then for _,c in cities:Members()do
    all[#all+1]=c;assert(#all<=2048,'INSP_CLEANUP_SCOPE_LIMIT');if P.IsTestPlayer(c:GetOwner())then supported=true end
   end end end
   if not supported then return false end
   -- One startup pass replaces the retired probe's pass, including foreign saved carriers.
   for _,c in ipairs(all)do
    local good,err=pcall(withdraw,c)
    if not good then local k=key(c:GetOwner(),c:GetID());pendingCleanup[k]=true;d.errors[k]=tostring(err):sub(1,180)end
   end
   d.ready=true;return true
  end)
  d.busy=false
  if not ok then d.startupFailed=true;d.startupError=tostring(result):sub(1,180)end
  return ok and result
 end
 local function reconcile(pid,c)
  assert(P.IsTestPlayer(pid) and c:GetOwner()==pid,'INSP_OWNER_UNKNOWN')
  local k=key(pid,c:GetID());local reference=SPCNetworkInput.Reference(c);local old=d.records[k]
  if pendingCleanup[k]then withdraw(c);pendingCleanup[k]=nil end
  local ok,p=pcall(function()
   local f=SPCCurrentSpecializationFacts.Read(P,shared,pid,c)
   -- No Shared D, buildings, workers, full work list or diagnostic construction.
   local w
   if f.validity=='VERIFIED' and f.identity=='CULTURE' and type(f.potential)=='number' and f.potential>=4
    and f.activeStatus=='KNOWN' and type(f.active)=='number' and f.active>=4 then
    w=shared.GreatWorkFacts.Summary(pid,c:GetID())
    if w then assert(w.reference==reference,'INSP_REFERENCE_CHANGED')end
   end
   return M.Plan(f,w)
  end)
  if not ok then
   -- Same reference UNKNOWN holds only a confirmed session projection.
   if not old or old.reference~=reference or tostring(p):find('INSP_REFERENCE_CHANGED',1,true)then
    project(c,nil);d.records[k]=nil
   end
   error(p)
  end
  assert(c:GetOwner()==pid and SPCNetworkInput.Reference(c)==reference,'INSP_REFERENCE_CHANGED')
  local written,why=pcall(project,c,p.carrier,{owner=pid,reference=reference})
  if not written then local cleared,err=pcall(project,c,nil);d.records[k]=nil;error(cleared and why or err)end
  p.owner=pid;p.cityID=c:GetID();p.reference=reference;p.x=c:GetX();p.y=c:GetY()
  d.records[k]=p;d.errors[k]=nil
 end
 function d.Audit(scope)
  if scope and scope.player~=nil and not P.IsTestPlayer(scope.player)then return false end
  if d.busy then
   local nextScope={player=scope and scope.player,city=scope and scope.city}
   if d.pending then
    if d.pending.player~=nextScope.player then nextScope.player=nil;nextScope.city=nil
    elseif d.pending.city~=nextScope.city then nextScope.city=nil end
   end
   d.pending=nextScope;return false
  end
  if not ready()then return false end
  if d.pending and not d.draining then
   if not scope or d.pending.player~=scope.player then scope=nil
   elseif d.pending.city~=scope.city then scope={player=scope.player}end
   d.pending=nil
  end
  d.busy=true
  local ok,why=pcall(function()
   for pid,player in pairs(Players)do if P.IsTestPlayer(pid) and (not scope or scope.player==nil or scope.player==pid)then
    local cities=player:GetCities();local seen={}
    local function visit(c)
     local k=key(pid,c:GetID());seen[k]=true;P.Count('city_scan')
     local good,err=pcall(reconcile,pid,c);if not good then d.errors[k]=tostring(err):sub(1,180)end
    end
    if scope and scope.city~=nil then
     local c=cities:FindID(scope.city);if c and c:GetOwner()==pid then visit(c)end
    else
     for _,c in cities:Members()do if c:GetOwner()==pid then visit(c)end end
     for k,p in pairs(d.records)do if p.owner==pid and not seen[k]then d.records[k]=nil end end
     local prefix=pid..':'
     for k in pairs(d.errors)do if k:sub(1,#prefix)==prefix and not seen[k]then d.errors[k]=nil;pendingCleanup[k]=nil end end
    end
   end end
  end)
  d.busy=false;d.error=not ok and tostring(why):sub(1,180) or nil
  if d.pending and not d.draining then
   local pending=d.pending;d.pending=nil;d.draining=true;d.Audit(pending);d.draining=false
  end
  return ok
 end
 function d.CollectionConfirmed(pid)
  if P.IsTestPlayer(pid) and not d.ready then return d.Audit({player=pid})end
 end
 function d.Describe(pid,c)
  local k=key(pid,c:GetID());local reference=SPCNetworkInput.Reference(c);local p=d.records[k]
  if p and p.reference~=reference then p=nil end
  local err=d.errors[k] or d.startupError or d.error;local lines={Locale.Lookup('LOC_SPC_INSPIRATION_AUTO')}
  if err or not p then lines[#lines+1]=Locale.Lookup('LOC_SPC_INSPIRATION_PENDING')
  elseif p.status=='INACTIVE'then lines[#lines+1]=Locale.Lookup('LOC_SPC_INSPIRATION_INACTIVE')
  else lines[#lines+1]=Locale.Lookup('LOC_SPC_INSPIRATION_CURRENT',p.eras,p.percent)end
  local unresolved=0;for _ in pairs(pendingCleanup)do unresolved=unresolved+1 end
  if unresolved>0 then lines[#lines+1]=Locale.Lookup('LOC_SPC_INSPIRATION_CLEANUP_PENDING',unresolved)end
  lines[#lines+1]=Locale.Lookup('LOC_SPC_INSPIRATION_NOTE')
  return table.concat(lines,'\n'),{owner=pid,city=c:GetID(),reference=reference,eras=p and p.eras,percent=p and p.percent,
   status=err and 'UNKNOWN' or p and p.status or 'UNKNOWN',error=err}
 end
 local function bind(name,fn)local e=P.Field(Events,name);if e and e.Add then e.Add(fn)end end
 bind('LoadScreenClose',function()
  d.ready=false;d.startupFailed=nil;d.startupError=nil;d.records={};d.errors={};d.pending=nil;pendingCleanup={};ids=nil;d.Audit()
 end)
 for _,name in ipairs({'GovernorAssigned','GovernorEstablished'})do bind(name,function(pid,cid,governorOwner)
  if type(pid)=='number' and type(cid)=='number'then d.Audit({player=pid,city=name=='GovernorEstablished' and cid or nil})
   if type(governorOwner)=='number' and governorOwner~=pid then d.Audit({player=governorOwner})end
  else d.Audit()end
 end)end
 for _,name in ipairs({'GovernorChanged','GovernorPromoted'})do bind(name,function(pid)d.Audit({player=type(pid)=='number' and pid or nil})end)end
 bind('CityBuildingsChanged',function(pid,cid)
  if d.writing~=key(pid,cid)then d.Audit({player=pid,city=cid})end
 end) -- id-only native event: also repairs a removed/pillaged owned carrier.
 for _,name in ipairs({'DistrictPillaged','DistrictRepaired','DistrictRemovedFromMap','CityTransfered','CityRemovedFromMap'})do
  bind(name,function()d.Audit()end) -- unknown signatures retain supported-player reconciliation.
 end
 bind('DistrictBuildProgressChanged',function(pid,_,cid)
  if type(pid)=='number' and type(cid)=='number'then d.Audit({player=pid,city=cid})end
 end)
 local lastTurn
 bind('PlayerTurnActivated',function(pid)
  if P.IsTestPlayer(pid)then local turn=Game.GetCurrentGameTurn();if lastTurn~=turn then lastTurn=turn;d.Audit({player=pid})end end
 end)
 shared.GreatWorkFacts.RegisterConsumer('CultureInspiration',function(pid,changed)
  if P.IsTestPlayer(pid)then
   if not d.ready then d.Audit({player=pid})else for _,cid in ipairs(changed)do d.Audit({player=pid,city=cid})end end
  end
 end)
 local store=shared.CityProgressionStore
 if store then
  store.RegisterExit('CultureInspiration',function(c,loss)
   assert(store.IsExitTarget(c,loss),'INSP_EXIT_UNCONFIRMED');store.RemoveOwned(c,loss,M.Owned)
   shared.CultureInspirationProbe.Withdraw(c)
   for k,p in pairs(d.records)do if p.owner==loss.origin.owner and p.x==c:GetX() and p.y==c:GetY()then d.records[k]=nil;d.errors[k]=nil;pendingCleanup[k]=nil end end
  end)
  store.RegisterReturn('CultureInspiration',function(pid,c)d.Audit({player=pid,city=c:GetID()})end)
 end
 return d
end
