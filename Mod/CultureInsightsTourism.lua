include('CurrentSpecializationFacts')
include('NetworkInput')
-- City history is owned by CityProgressionStore; this module owns only derived carriers.
SPCCultureInsightsTourism={Max=192,Owned={}}
local M=SPCCultureInsightsTourism
for n=1,M.Max do M.Owned[n]='BUILDING_SPC_INSIGHT_TOURISM_'..n end
function M.Plan(f,records,ownCiv)
 assert(f and f.validity=='VERIFIED','INSIGHT_FACT_UNKNOWN')
 if f.identity~='CULTURE' then return 0 end
 assert(type(f.potential)=='number','INSIGHT_POTENTIAL_UNKNOWN')
 if f.potential<4 then return 0 end
 assert(f.activeStatus=='KNOWN' and type(f.active)=='number','INSIGHT_ACTIVE_UNKNOWN')
 if f.active<4 then return 0 end
 assert(type(records)=='table' and type(ownCiv)=='string','INSIGHT_HISTORY_UNKNOWN')
 local n,total=0,0
 for _,r in pairs(records)do
  assert(type(r)=='table' and type(r.civ)=='string' and (r.category=='PEOPLE' or r.category=='WORKS' or r.category=='PLACES'),'INSIGHT_RECORD_UNKNOWN')
  total=total+1;if r.civ~=ownCiv then n=n+1 end
 end
 assert(total<=M.Max,'INSIGHT_RANGE_UNKNOWN');return n
end
function M.Start(P,shared)
 local store=assert(shared.CityProgressionStore,'INSIGHT_STORE_REQUIRED')
 local d={records={},errors={},ready=false,busy=false};shared.CultureInsightsTourism=d
 local ids,owned={},{};for _,name in ipairs(M.Owned)do owned[name]=true end
 local function key(c)return tostring(c:GetOwner())..':'..tostring(c:GetID())end
 local function ref(c)return SPCNetworkInput.Reference(c)end
 local function validate()
  if ids[1]then return end
  local dm=assert(P.Info('DynamicModifiers','MODIFIER_SINGLE_CITY_ADJUST_TOURISM_LATE_ERAS'),'INSIGHT_EFFECT_MISSING')
  assert(dm.CollectionType=='COLLECTION_OWNER' and dm.EffectType=='EFFECT_ADJUST_CITY_TOURISM_LATE_ERAS','INSIGHT_EFFECT_INVALID')
  local args,links={},{}
  for _,a in ipairs(P.Rows('ModifierArguments'))do if a.ModifierId:match('^SPC_INSIGHT_TOURISM_')then
   args[a.ModifierId]=args[a.ModifierId] or {};args[a.ModifierId][a.Name]=a.Value
  end end
  for _,a in ipairs(P.Rows('BuildingModifiers'))do if owned[a.BuildingType]then
   links[a.BuildingType]=links[a.BuildingType] or {};table.insert(links[a.BuildingType],a.ModifierId)
  end end
  local nextIDs={}
  for n,name in ipairs(M.Owned)do
   local b=assert(P.Info('Buildings',name),'INSIGHT_CARRIER_MISSING');local mid='SPC_INSIGHT_TOURISM_'..n
   local m=assert(P.Info('Modifiers',mid),'INSIGHT_MODIFIER_MISSING');local a=args[mid];local l=links[name]
   assert((b.InternalOnly==true or b.InternalOnly==1) and b.PrereqDistrict=='DISTRICT_CITY_CENTER' and b.CitizenSlots==0 and b.Housing==0,'INSIGHT_CARRIER_INVALID')
   assert(m.ModifierType=='MODIFIER_SINGLE_CITY_ADJUST_TOURISM_LATE_ERAS' and not m.OwnerRequirementSetId and not m.SubjectRequirementSetId,'INSIGHT_MODIFIER_INVALID')
   assert(a and tonumber(a.Modifier)==2*n and a.MinimumEra=='ERA_ANCIENT' and not a.GreatWorkObjectType,'INSIGHT_ARGUMENT_INVALID')
   assert(l and #l==1 and l[1]==mid,'INSIGHT_ATTACHMENT_INVALID');nextIDs[n]=b.Index
  end
  ids=nextIDs
 end
 local function has(c,n)
  local yes=P.HasBuilding(c:GetBuildings(),ids[n]);assert(type(yes)=='boolean','INSIGHT_PRESENCE_UNKNOWN');return yes
 end
 local function remove(c,n)
  if n and n>0 and has(c,n)then P.RemoveBuilding(c:GetBuildings(),ids[n]);assert(not has(c,n),'INSIGHT_REMOVE_UNCONFIRMED')end
 end
 local function clear(c)
  -- Full owned-ID cleanup only on first observation/load, fault recovery or confirmed exit.
  d.writing=key(c);local ok,err=pcall(function()for n=1,M.Max do remove(c,n)end end);d.writing=nil
  assert(ok,err)
 end
 local function reconcile(pid,c)
  validate();local k=key(c);local reference=ref(c);local old=d.records[k]
  if not old or old.reference~=reference then clear(c);old={reference=reference,n=0,x=c:GetX(),y=c:GetY(),owner=pid};d.records[k]=old end
  local f=SPCCurrentSpecializationFacts.Read(P,shared,pid,c)
  local records,civ
  if f.validity=='VERIFIED' and f.identity=='CULTURE' and f.potential and f.potential>=4 and f.activeStatus=='KNOWN' and f.active and f.active>=4 then
   records=store.ExpeditionInsights(pid,c)
   local config=PlayerConfigurations and PlayerConfigurations[pid]
   civ=config and config:GetCivilizationTypeName()
  end
  local n=M.Plan(f,records,civ) -- UNKNOWN holds only a confirmed same-reference session projection.
  assert(c:GetOwner()==pid and ref(c)==reference,'INSIGHT_REFERENCE_CHANGED')
  d.writing=k
  local ok,err=pcall(function()
   if old.n~=n then remove(c,old.n)end
   if n>0 then
    local present=has(c,n)
    if present then
     local damaged=c:GetBuildings():IsPillaged(ids[n]);assert(type(damaged)=='boolean','INSIGHT_HEALTH_UNKNOWN')
     if damaged then remove(c,n);present=false end
    end
    if not present then P.CreateBuilding(c:GetBuildQueue(),ids[n]);assert(has(c,n),'INSIGHT_CREATE_UNCONFIRMED')end
   end
   assert(c:GetOwner()==pid and ref(c)==reference,'INSIGHT_REFERENCE_CHANGED')
  end)
  d.writing=nil
  if not ok then d.records[k]=nil;local cleared,why=pcall(clear,c);error(cleared and err or why)end
  old.n=n;d.errors[k]=nil
 end
 function d.Audit(scope)
  if scope and scope.player~=nil and not P.IsTestPlayer(scope.player)then return end
  if d.busy then
   local nextScope={player=scope and scope.player,city=scope and scope.city}
   if d.pending then
    if d.pending.player~=nextScope.player then nextScope={}elseif d.pending.city~=nextScope.city then nextScope.city=nil end
   end
   d.pending=nextScope;return
  end
  d.busy=true
  local ok,err=pcall(function()
   validate()
   if not d.ready then
    -- Remove saved derived effects, including cities now owned by unsupported players.
    d.records={};d.errors={}
    for _,p in pairs(Players)do local cities=p:GetCities();if cities then for _,c in cities:Members()do
     clear(c)
     if P.IsTestPlayer(c:GetOwner())then d.records[key(c)]={reference=ref(c),n=0,x=c:GetX(),y=c:GetY(),owner=c:GetOwner()}end
    end end end
    d.ready=true
   end
   local seen={}
   for pid,p in pairs(Players)do if P.IsTestPlayer(pid) and (not scope or scope.player==nil or scope.player==pid)then
    local function visit(c)
     local k=key(c);seen[k]=true
     local good,why=pcall(reconcile,pid,c);if not good then d.errors[k]=tostring(why):sub(1,180)end
    end
    if scope and scope.city~=nil then local c=p:GetCities():FindID(scope.city);if c and c:GetOwner()==pid then visit(c)end
    else for _,c in p:GetCities():Members()do if store.Owns(c)then visit(c)end end end
   end end
   if not scope or scope.city==nil then
    for k,p in pairs(d.records)do if (not scope or scope.player==nil or p.owner==scope.player) and not seen[k]then d.records[k]=nil;d.errors[k]=nil end end
    for k in pairs(d.errors)do
     local pid=tonumber(k:match('^(%d+):'))
     if (not scope or scope.player==nil or pid==scope.player) and not seen[k]then d.errors[k]=nil end
    end
   end
  end)
  d.busy=false;d.error=not ok and tostring(err):sub(1,180) or nil
  if d.pending and not d.draining then local pending=d.pending;d.pending=nil;d.draining=true;d.Audit(pending);d.draining=false end
 end
 function d.Describe(pid,c)
  local k=key(c);local p=d.records[k];local err=d.errors[k] or d.error
  local known=p and p.reference==ref(c) and not err
  local percent=known and 2*p.n or nil
  print('[SPC][B191][N1_INSIGHT] kind=TOURISM owner='..pid..' city='..c:GetID()..' status='..(known and 'KNOWN' or 'UNKNOWN')..' percent='..tostring(percent))
  return known and Locale.Lookup('LOC_SPC_INSIGHT_TOURISM_CURRENT',percent) or Locale.Lookup('LOC_SPC_INSIGHT_TOURISM_UNKNOWN')
 end
 local function bind(name,fn)local e=P.Field(Events,name);if e and e.Add then e.Add(fn)end end
 bind('LoadScreenClose',function()d.ready=false;d.records={};d.errors={};ids={};d.Audit()end)
 for _,name in ipairs({'GovernorAssigned','GovernorChanged','GovernorPromoted','GovernorEstablished'})do
  bind(name,function(pid) d.Audit({player=type(pid)=='number' and pid or nil})end)
 end
 bind('PlayerTurnActivated',function(pid)if P.IsTestPlayer(pid)then d.Audit({player=pid})end end)
 bind('CityBuildingsChanged',function(pid,cid)if d.writing~=tostring(pid)..':'..tostring(cid)then d.Audit({player=pid,city=cid})end end)
 store.RegisterExit('CultureInsightsTourism',function(c,loss)
  assert(store.IsExitTarget(c,loss),'INSIGHT_EXIT_UNCONFIRMED');store.RemoveOwned(c,loss,M.Owned)
  for k,p in pairs(d.records)do if p.owner==loss.origin.owner and p.x==c:GetX() and p.y==c:GetY()then d.records[k]=nil;d.errors[k]=nil end end
 end)
 store.RegisterReturn('CultureInsightsTourism',function(pid,c)d.Audit({player=pid,city=c:GetID()})end)
 return d
end
