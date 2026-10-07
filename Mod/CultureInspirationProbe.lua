include('CurrentSpecializationFacts')
include('NetworkInput')
-- L3-A native precision gate only. No saved rewards, no normal ability writer.
SPCCultureInspirationProbe={}
function SPCCultureInspirationProbe.Start(P,shared)
 local d={ready=false,busy=false,stage=-1,changes=0,sequence=0};shared.CultureInspirationProbe=d
 local values={0,0.1,0.3,0.6,1}
 local names={};for _,v in ipairs({1,3,6,10})do names[#names+1]='BUILDING_SPC_INSPIRE_PROBE_'..v end
 local ids,target,cleanupFailed,lastRequest
 local function tr(key,...)return Locale.Lookup('LOC_SPC_INSPIRE_'..key,...)end
 local function reference(c)return SPCNetworkInput.Reference(c)end
 local function validate()
  if ids then return end
  local found={}
  for i,name in ipairs(names)do
   local b=assert(P.Info('Buildings',name),'INSPIRE_DEFINITION_MISSING')
   assert((b.InternalOnly==1 or b.InternalOnly==true) and b.PrereqDistrict=='DISTRICT_CITY_CENTER' and b.CitizenSlots==0 and b.Housing==0,'INSPIRE_CARRIER_INVALID')
   local mid='SPC_INSPIRE_PROBE_'..({1,3,6,10})[i];local m=P.Info('Modifiers',mid)
   assert(m and m.ModifierType=='MODIFIER_SINGLE_CITY_ADJUST_GREAT_PERSON_POINT','INSPIRE_MODIFIER_INVALID')
   local a={};for _,row in ipairs(assert(P.Rows('ModifierArguments'),'INSPIRE_DB_UNKNOWN'))do if row.ModifierId==mid then a[row.Name]=row.Value end end
   assert(tonumber(a.Amount)==values[i+1] and a.GreatPersonClassType=='GREAT_PERSON_CLASS_SCIENTIST','INSPIRE_AMOUNT_INVALID')
   local n=0;for _,row in ipairs(assert(P.Rows('BuildingModifiers'),'INSPIRE_DB_UNKNOWN'))do if row.BuildingType==name then assert(row.ModifierId==mid,'INSPIRE_ATTACHMENT_INVALID');n=n+1 end end
   assert(n==1,'INSPIRE_ATTACHMENT_MISSING');found[name]=b.Index
  end
  ids=found
 end
 local function present(c,name)
  local v=P.HasBuilding(c:GetBuildings(),ids[name]);assert(type(v)=='boolean','INSPIRE_PRESENCE_UNKNOWN');return v
 end
 local function same(c)
  return target and c:GetOwner()==target.owner and c:GetID()==target.city and P.IsTestPlayer(target.owner) and reference(c)==target.reference
 end
 local function eligible(c)
  local f=SPCCurrentSpecializationFacts.Read(P,shared,c:GetOwner(),c)
  assert(f.validity=='VERIFIED' and type(f.potential)=='number','INSPIRE_FACT_UNKNOWN')
  if f.identity~='CULTURE' or f.potential<4 then return false end
  assert(f.activeStatus=='KNOWN' and type(f.active)=='number','INSPIRE_ACTIVE_UNKNOWN')
  return f.identity=='CULTURE' and f.potential>=4 and f.active>=4
 end
 local function project(c,want)
  validate();local failure
  for _,name in ipairs(names)do
   local ok,why=pcall(function()
    local has=present(c,name)
    if has and name~=want then P.RemoveBuilding(c:GetBuildings(),ids[name]);assert(not present(c,name),'INSPIRE_REMOVE_UNCONFIRMED');d.changes=d.changes+1 end
   end)
   if not ok then failure=failure or why end
  end
  assert(not failure,failure)
  if want and not present(c,want)then
   assert(same(c) and eligible(c),'INSPIRE_TARGET_CHANGED')
   P.CreateBuilding(c:GetBuildQueue(),ids[want]);d.changes=d.changes+1
   if not same(c)then
    -- Remove only our four IDs if native creation caused confirmed owner change.
    for _,name in ipairs(names)do if present(c,name)then P.RemoveBuilding(c:GetBuildings(),ids[name]);assert(not present(c,name),'INSPIRE_REMOVE_UNCONFIRMED')end end
    error('INSPIRE_TARGET_CHANGED')
   end
   assert(present(c,want),'INSPIRE_CREATE_UNCONFIRMED')
  end
 end
 local function forget()target=nil;d.stage=-1;d.error=nil end
 local function cleanup()
  if d.ready then return true end
  if cleanupFailed then return false end
  local ok,why=pcall(function()
   validate();local count,supported=0,false;local all={}
   for _,p in pairs(Players)do local cities=p:GetCities();if cities then for _,c in cities:Members()do
    count=count+1;assert(count<=2048,'INSPIRE_CLEANUP_LIMIT');all[#all+1]=c
    if P.IsTestPlayer(c:GetOwner())then supported=true end
   end end end
   if not supported then return end
   local failure
   for _,c in ipairs(all)do local good,err=pcall(project,c,nil);if not good then failure=failure or err end end
   assert(not failure,failure);forget();d.ready=true
  end)
  if not ok then cleanupFailed=true;d.error=tostring(why):sub(1,180)end
  return d.ready
 end
 local function current()
  assert(target,'INSPIRE_NO_TARGET');local c=assert(Players[target.owner]:GetCities():FindID(target.city),'INSPIRE_CITY_UNKNOWN')
  assert(same(c),'INSPIRE_REFERENCE_CHANGED');return c
 end
 function d.Audit(pid)
  if d.busy or not target or pid~=nil and pid~=target.owner then return end
  d.busy=true
  local ok,why=pcall(function()
   local candidate=Players[target.owner]:GetCities():FindID(target.city)
   if candidate and candidate:GetOwner()==target.owner and reference(candidate)~=target.reference then project(candidate,nil);forget();return end
   local c=current()
   if not eligible(c)then project(c,nil);forget()end
  end)
  d.busy=false;if not ok then d.error=tostring(why):sub(1,180)end
 end
 function d.Request(pid,c,action,token)
  if type(token)~='string' then return tr('STOP','INSPIRE_TOKEN_REQUIRED')end
  if lastRequest and lastRequest.token==token then
   if lastRequest.pid==pid and lastRequest.city==(c and c:GetID()) and lastRequest.action==action then return lastRequest.out end
   return tr('STOP','INSPIRE_TOKEN_CONFLICT')
  end
  if d.busy then return tr('BUSY')end
  d.busy=true
  local ok,out=pcall(function()
   assert(P.IsTestPlayer(pid) and c and c:GetOwner()==pid,'INSPIRE_OWNER_UNKNOWN')
   assert(cleanup(),d.error or 'INSPIRE_LOADING')
   if action=='INSPIRE_END' then
    if target then project(current(),nil);forget()end
   elseif action=='INSPIRE_NEXT' then
    if not target then
     assert(eligible(c),'INSPIRE_REQUIRE_ACTIVE_IV');d.sequence=d.sequence+1
     target={owner=pid,city=c:GetID(),reference=reference(c),session=d.sequence};d.stage=0
     project(c,nil)
    else
     assert(same(c),'INSPIRE_FINISH_PREVIOUS_CITY');assert(eligible(c),'INSPIRE_REQUIRE_ACTIVE_IV')
     assert(d.stage<4,'INSPIRE_STAGES_COMPLETE');local nextStage=d.stage+1
     project(c,names[nextStage]);d.stage=nextStage
    end
   elseif action~='INSPIRE_READ' then error('INSPIRE_ACTION_UNKNOWN')end
   if target then
    assert(same(c),'INSPIRE_FINISH_PREVIOUS_CITY')
    if action~='INSPIRE_READ' and not eligible(c)then project(c,nil);forget()end
   end
   local count=0;for _,name in ipairs(names)do if present(c,name)then count=count+1 end end
   local amount=target and values[d.stage+1] or 0
   shared.CultureInspirationView={token=token,owner=pid,city=c:GetID(),reference=reference(c),
     session=target and target.session or nil,stage=d.stage,amount=amount,count=count}
   d.error=nil
   local title=target and tr('STAGE',d.stage,amount) or tr('OFF')
   return tr('TITLE')..'\n'..title..'\n'..tr('INSTANCES',count)..'\n'..tr('CONTROL')..'\n'..tr('NEXT_HELP')
  end)
  d.busy=false
  if not ok then d.error=tostring(out):sub(1,180);shared.CultureInspirationView=nil;out=tr('STOP',d.error)end
  lastRequest={token=token,pid=pid,city=c and c:GetID(),action=action,out=out}
  return out
 end
 local function bind(name,fn)local e=P.Field(Events,name);if e and e.Add then e.Add(fn)end end
 bind('LoadScreenClose',function() d.ready=false;cleanupFailed=nil;lastRequest=nil;shared.CultureInspirationView=nil;cleanup()end)
 bind('PlayerTurnActivated',function(pid)if P.IsTestPlayer(pid)then cleanup();d.Audit(pid)end end)
 for _,name in ipairs({'GovernorAssigned','GovernorEstablished','GovernorChanged','GovernorPromoted','CityTransfered','CityRemovedFromMap'})do bind(name,function(pid)d.Audit(pid)end)end
 if shared.CityProgressionStore then shared.CityProgressionStore.RegisterExit('CultureInspirationProbe',function(c,loss)
  if not shared.CityProgressionStore.IsExitTarget(c,loss)then return end
  shared.CityProgressionStore.RemoveOwned(c,loss,names)
  if target and loss.origin and target.owner==loss.origin.owner and target.city==loss.targetID then forget()end
 end)end
end
