include('RuntimeWork')
-- B177: saved city history -> current Tourism-only technical fallback.
-- No new persistence. One final-value carrier; no stacked bit multipliers.
include('DialogueProjectModel')
include('CultureMeaningModel')
include('GreatWorkCatalog')
include('NetworkInput')
SPCDialogueEffects={}
function SPCDialogueEffects.Start(P,shared)
 local store=assert(shared.CityProgressionStore);local legacy=assert(shared.Dialogue)
 local d={ready=false,busy=false,records={},errors={},changes=0};shared.DialogueEffects=d
 legacy.retired=true -- Disable old/manual writers even if new initialization fails.
 legacy.off={};legacy.test={};legacy.carrierTest=nil;legacy.meaningOverride=nil;legacy.meaningQualification=nil
 local owned,ids,eras,ownedIndex={},{},{},{};local coverage;local max=0
 for row in GameInfo.Eras()do eras[row.EraType]=true;max=max+40 end
 -- At most one receipt per loaded Game Era, each adds 5*X with X<=8.
 -- This enumerates every reachable total, not an added gameplay cap.
 for value=5,max,5 do owned[#owned+1]='BUILDING_SPC_DIALOGUE_TOTAL_'..value end
 local ownedSet={};for _,name in ipairs(owned)do ownedSet[name]=true end
 function d.IsOwnedCarrier(name)return ownedSet[name]==true end
 local function key(pid,cid)return tostring(pid)..':'..tostring(cid)end
 local function sameRef(a,c)return a and a.owner==c:GetOwner() and a.cityID==c:GetID() and a.x==c:GetX() and a.y==c:GetY()end
 local function project(c,value,reference,prior)
  local want=value>0 and 'BUILDING_SPC_DIALOGUE_TOTAL_'..value or nil
  assert(not want or ids[want],'DIALOGUE_TOTAL_UNREPRESENTABLE')
  local function check()
   if reference then assert(P.IsTestPlayer(c:GetOwner()) and SPCNetworkInput.Reference(c)==reference,'DIALOGUE_EFFECT_REFERENCE_CHANGED')end
  end
  d.writing=key(c:GetOwner(),c:GetID())
  local ok,why=pcall(function()
   local failure
   local checkNames=owned
   if prior~=nil then
    checkNames={}
    if prior>0 then checkNames[#checkNames+1]='BUILDING_SPC_DIALOGUE_TOTAL_'..prior end
    if want and value~=prior then checkNames[#checkNames+1]=want end
   end
   for _,name in ipairs(checkNames)do
    local good,err=pcall(function()
     local b=c:GetBuildings();local has=P.HasBuilding(b,ids[name]);assert(type(has)=='boolean','DIALOGUE_CARRIER_UNKNOWN')
     local damaged=false
     if has and name==want then damaged=b:IsPillaged(ids[name]);assert(type(damaged)=='boolean','DIALOGUE_CARRIER_HEALTH_UNKNOWN')end
     if has and (name~=want or damaged)then
      check()
      local ok,plot=pcall(function()return b:GetBuildingLocation(ids[name])end)
      d.removing={owner=c:GetOwner(),index=ids[name],plot=ok and plot or nil}
      local removed,err=pcall(P.RemoveBuilding,b,ids[name]);d.removing=nil;assert(removed,err)
      assert(P.HasBuilding(b,ids[name])==false,'DIALOGUE_REMOVE_UNCONFIRMED');d.changes=d.changes+1
     end
    end)
    if not good then failure=failure or err end
   end
   assert(not failure,failure) -- Never add over unconfirmed removal.
   check()
   if want and not P.HasBuilding(c:GetBuildings(),ids[want])then
    P.CreateBuilding(c:GetBuildQueue(),ids[want]);check()
    assert(P.HasBuilding(c:GetBuildings(),ids[want])==true,'DIALOGUE_CREATE_UNCONFIRMED');d.changes=d.changes+1
   end
  end)
  d.writing=nil;d.removing=nil;assert(ok,why)
 end
 local function ready()
  if d.ready then return true end
  if d.startupError or d.initializing then return false end
  local supported=false;for pid in pairs(Players)do if P.IsTestPlayer(pid)then supported=true end end
  if not supported then return false end
  d.initializing=true
  local ok,why=pcall(function()
   for _,name in ipairs(owned)do
    local row=assert(P.Info('Buildings',name),'DIALOGUE_DEFINITION_MISSING')
    assert((row.InternalOnly==1 or row.InternalOnly==true) and row.PrereqDistrict=='DISTRICT_CITY_CENTER' and row.CitizenSlots==0 and row.Housing==0,'DIALOGUE_DEFINITION_INVALID')
    ids[name]=row.Index;ownedIndex[row.Index]=true
   end
   legacy.ready=false;legacy.Init() -- Exact legacy IDs; never infer history from those buildings.
   local n=0
   for _,player in pairs(Players)do local cities=player:GetCities();if cities then for _,c in cities:Members()do
    n=n+1;assert(n<=2048,'DIALOGUE_CLEANUP_SCOPE_LIMIT');project(c,0)
    if P.IsTestPlayer(c:GetOwner())then d.records[key(c:GetOwner(),c:GetID())]={owner=c:GetOwner(),cityID=c:GetID(),x=c:GetX(),y=c:GetY(),reference=SPCNetworkInput.Reference(c),applied=0,state='WAITING'}end
   end end end
   -- Reuse the reviewed category-coverage proof, once per loaded game.
   coverage=SPCCultureMeaningModel.RecipientCoverage(P)
   d.ready=true
  end)
  d.initializing=false
  if not ok then d.startupError=tostring(why):sub(1,180)end
  return ok
 end
 local function reconcile(pid,c)
  assert(P.IsTestPlayer(pid) and c:GetOwner()==pid,'DIALOGUE_EFFECT_OWNER')
  local k=key(pid,c:GetID());local reference=SPCNetworkInput.Reference(c);local old=d.records[k]
  local function remember(total,value,state)
   d.records[k]={owner=pid,cityID=c:GetID(),x=c:GetX(),y=c:GetY(),reference=reference,total=total,applied=value,state=state}
  end
  local prior=old and old.reference==reference and old.applied or nil
  local function clear(state)project(c,0,reference,prior);remember(nil,0,state)end
  local function unknown(reason)
   if not old or old.reference~=reference then clear('WAITING')end
   error(reason)
  end
  local function history()
   local good,s=pcall(store.DialogueState,pid,c)
   assert(good,'DIALOGUE_HISTORY_UNAVAILABLE')
   assert(sameRef(s.reference,c),'DIALOGUE_EFFECT_REFERENCE_CHANGED')
   if s.value then
    SPCDialogueProjectModel.Validate(s.value)
    for era in pairs(s.value.used)do assert(eras[era],'DIALOGUE_HISTORY_ERA_UNAVAILABLE')end
    assert(s.value.total<=max,'DIALOGUE_TOTAL_UNREPRESENTABLE')
   end
   return s
  end
  local factsOK,f=pcall(shared.EffectiveFacts.Read,pid,c)
  if not factsOK then
   -- EffectiveFacts also reads the Store: its error may be damaged history,
   -- not temporary governor uncertainty. Never retain a bonus on that guess.
   if prior and prior>0 then
    local good,why=pcall(history);if not good then clear('HELD');error(why)end
   end
   unknown('DIALOGUE_CURRENT_FACTS_UNKNOWN')
  end
  if f.owner~=pid or f.cityID~=c:GetID()then clear('HELD');error('DIALOGUE_EFFECT_REFERENCE_CHANGED')end
  -- Other professions/unassigned cities need no Dialogue history read at all.
  -- Known ineligibility withdraws even when an unrelated governor fact is unknown.
  if f.specialization~='CULTURE' or f.activeStatus=='KNOWN' and f.active<3 then
   clear('INACTIVE');d.errors[k]=nil;return
  end
  if f.activeStatus~='KNOWN' or f.investmentPending then
   if prior and prior>0 then local good,why=pcall(history);if not good then clear('HELD');error(why)end end
   unknown('DIALOGUE_CURRENT_FACTS_UNKNOWN')
  end
  local valid,s=pcall(history)
  if not valid then clear('HELD');error(s)end
  if f.token~=s.token then clear('HELD');error('DIALOGUE_EFFECT_REFERENCE_CHANGED')end
  local total=s.value and s.value.total or 0
  local value=0;local state='INACTIVE'
  if f.specialization=='CULTURE' and f.active>=3 then
   state='READY'
   if total>0 then
    assert(coverage and coverage.status=='VERIFIED_LOADED_SET','DIALOGUE_RECIPIENT_CATALOG_UNVERIFIED')
    local w=shared.GreatWorkFacts.Summary(pid,c:GetID())
    if not w or not w.hasConfirmed or w.availability~='KNOWN'then unknown('DIALOGUE_COLLECTION_UNKNOWN')end
    if w.reference~=reference or w.modifierExcludedCount~=0 or w.unknownCategoryCount~=0 then
     project(c,0,reference);d.records[k]=nil;error('DIALOGUE_RECIPIENT_UNCONFIRMED')
    end
    if w.count>0 then value=total else state='NO_WORKS'end
   end
  end
  local written,err=pcall(project,c,value,reference,old and old.reference==reference and old.applied or nil)
  if not written then
   d.records[k]=nil;local cleared,clearError=pcall(project,c,0,reference);error(cleared and err or clearError)
  end
  d.records[k]={owner=pid,cityID=c:GetID(),x=c:GetX(),y=c:GetY(),reference=reference,total=total,applied=value,state=state}
  d.errors[k]=nil
 end
 local function audit(scope)
  local ok,why=pcall(function()
   assert(ready(),d.startupError or 'DIALOGUE_NOT_READY')
   for pid,player in pairs(Players)do if P.IsTestPlayer(pid) and (not scope or scope.player==nil or scope.player==pid)then
    local cities=player:GetCities();local present={}
    local function visit(c)
     local k=key(pid,c:GetID());present[k]=true;P.Count('city_scan')
     local good,err=pcall(reconcile,pid,c);if not good then d.errors[k]=tostring(err):sub(1,180)end
    end
    if scope and scope.city~=nil then local c=cities:FindID(scope.city);if c and c:GetOwner()==pid then visit(c)end
    else
     for _,c in cities:Members()do visit(c)end
     local prefix=pid..':'
     for k in pairs(d.records)do if k:sub(1,#prefix)==prefix and not present[k]then d.records[k]=nil end end
     for k in pairs(d.errors)do if k:sub(1,#prefix)==prefix and not present[k]then d.errors[k]=nil end end
    end
   end end
  end)
  d.error=not ok and tostring(why):sub(1,180) or nil
  return ok
 end
 local direct,mark,flush=SPCRuntimeWork.NewAudit(P,shared,d,'DialogueEffects',audit)
 d.MarkAudit=mark;d.FlushAudit=flush
 function d.Audit(scope)
  if d.initializing then mark(scope);return false end
  if scope and scope.player~=nil and not P.IsTestPlayer(scope.player)then return false end
  if not d.ready then
   local ok,why=pcall(ready)
   if not ok or not why then d.error=not ok and tostring(why):sub(1,180) or d.startupError or 'DIALOGUE_NOT_READY';return false end
  end
  return direct(scope)
 end
 function d.Describe(pid,c)
  local k=key(pid,c:GetID());local p=d.records[k];local err=d.errors[k] or d.startupError or d.error
  if p and p.reference~=SPCNetworkInput.Reference(c)then p=nil end
  local lines={'实际收益：旅游业绩限定路径（已接受的技术备用方案）'}
  if err then lines[#lines+1]='待确认：'..(tostring(err):match('DIALOGUE_[A-Z_]+') or '历史或当前资格未就绪')end
  if p then
   lines[#lines+1]=(p.total~=nil and string.format('已得累计 +%d%%｜当前载体 +%d%%',p.total,p.applied) or string.format('当前载体 +%d%%｜已得历史见上方累计记录',p.applied))
   if p.state=='INACTIVE'then lines[#lines+1]='当前资格不足；已成功历史保留。'
   elseif p.state=='NO_WORKS'then lines[#lines+1]='当前没有合格巨作；累计记录保留。'end
  else lines[#lines+1]='当前载体尚未确认；不从旧效果推算历史。'end
  lines[#lines+1]='自动应用于本城合格巨作旅游业绩；不放大意义延展。小幅增益可能被原生取整。'
  return table.concat(lines,'\n')
 end
 local function hook(name,fn)local e=P.Field(Events,name);if e and e.Add then e.Add(fn)end end
 hook('LoadScreenClose',function()d.Audit()end)
 -- NativeFacts owns governor qualification causes; declared ACTIVE delivery is deferred.
 hook('CityTransfered',function(owner,cid,oldOwner)
  if type(owner)=='number' and owner>=0 then mark({player=owner,city=type(cid)=='number' and cid or nil})else mark()end
  if type(oldOwner)=='number' and oldOwner>=0 and oldOwner~=owner then mark({player=oldOwner})end
 end)
 shared.GreatWorkFacts.RegisterConsumer('DialogueEffects',function(pid,changed)
  if not P.IsTestPlayer(pid)then return end
  local failure
  for _,cid in ipairs(changed)do
   local ok=d.Audit({player=pid,city=cid})
   if not ok or d.errors[key(pid,cid)] or d.error or d.auditError then failure='DIALOGUE_COLLECTION_DELIVERY_PENDING'end
  end
  -- The real provider retries only on a new accepted sample, including equal facts.
  -- A queued/broken projection must not acknowledge successful consumer delivery.
  assert(not failure,failure)
 end)
 local function owns(index)return ownedIndex[index]==true end -- loaded definitions already validated once
 -- DC deliberately excludes internal carriers. This writer owns health recovery.
 local e=P.Field(GameEvents,'BuildingPillageStateChanged')
 if e and e.Add then e.Add(function(pid,cid,index,state)
  if P.IsTestPlayer(pid) and owns(index) and (state~=false or d.writing~=key(pid,cid))then mark({player=pid,city=cid})end
 end)end
 hook('BuildingRemovedFromMap',function(x,y,index,owner)
  if not owns(index)then return end
  local w=d.removing
  if w and w.owner==owner and w.index==index and type(w.plot)=='number' and w.plot>=0 then
   local ok,plot=pcall(function()
    if Map.GetPlotIndex then return Map.GetPlotIndex(x,y)end
    return Map.GetPlot(x,y):GetIndex()
   end)
   if ok and plot==w.plot then return end -- exact synchronous own removal only
  end
  local ok,c=pcall(function()
   local district=CityManager and CityManager.GetDistrictAt and CityManager.GetDistrictAt(x,y)
   return district and district:GetCity() or CityManager and CityManager.GetCityAt and CityManager.GetCityAt(x,y)
  end)
  if ok and c then
   local good,pid,cid=pcall(function()return c:GetOwner(),c:GetID()end)
   if good then if P.IsTestPlayer(pid)then mark({player=pid,city=cid})end;return end
  end
  mark({player=type(owner)=='number' and owner or nil}) -- unresolved external target is never suppressed by another city's write
 end)
 store.RegisterExit('DialogueEffects',function(c,loss)
  assert(store.IsExitTarget(c,loss),'DIALOGUE_EXIT_UNCONFIRMED');store.RemoveOwned(c,loss,owned)
  for k,p in pairs(d.records)do if p.owner==loss.origin.owner and p.x==c:GetX() and p.y==c:GetY()then d.records[k]=nil;d.errors[k]=nil end end
 end)
 store.RegisterReturn('DialogueEffects',function(pid,c)d.Audit({player=pid,city=c:GetID()})end)
 return d
end
