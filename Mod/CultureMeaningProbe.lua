include('CultureMeaningModel')
include('GreatWorkCatalog')
include('CurrentSpecializationFacts')
include('NetworkInput')
-- One explicitly chosen session fixture, no saved authority or benefit replay.
SPCCultureMeaningProbe={}
function SPCCultureMeaningProbe.Start(P,shared)
 local M=SPCCultureMeaningModel
 local d={ready=false,busy=false,mode='OFF',variant='SPLIT',changes=0,cleanupStatus='PENDING',cleanupPasses=0};shared.CultureMeaningProbe=d
 local target,indices,recoveryCity
 local owned={};for _,name in ipairs(M.Owned)do owned[name]=true end
 function d.IsOwnedCarrier(name)return owned[name]==true end
 local function validate()
  if indices then return end
  local nextIDs={}
  for _,name in ipairs(M.Owned)do
   local r=assert(P.Info('Buildings',name),'ME_DEFINITIONS_MISSING')
   assert((r.InternalOnly==1 or r.InternalOnly==true) and r.PrereqDistrict==(M.CarrierDistrict[name] or 'DISTRICT_CITY_CENTER') and r.CitizenSlots==0 and r.Housing==0,'ME_CARRIER_INVALID')
   nextIDs[name]=r.Index
  end
  indices=nextIDs
 end
 local function installed(c,name)
  local yes=P.HasBuilding(c:GetBuildings(),indices[name]);assert(type(yes)=='boolean','ME_CARRIER_UNKNOWN');return yes
 end
 local function project(c,want)
  validate()
  local failure
  for _,name in ipairs(M.Owned)do
   local ok,why=pcall(function()
    local present=installed(c,name);local damaged=false
    if present and want[name] then
     local value=c:GetBuildings():IsPillaged(indices[name]);assert(type(value)=='boolean','ME_CARRIER_HEALTH_UNKNOWN');damaged=value
    end
    if present and (not want[name] or damaged) then
     P.RemoveBuilding(c:GetBuildings(),indices[name]);assert(not installed(c,name),'ME_REMOVE_UNCONFIRMED');d.changes=d.changes+1
    end
   end)
   if not ok then failure=failure or why end
  end
  assert(not failure,failure) -- Attempt all exact withdrawals, never add after any failure.
  for _,name in ipairs(M.Owned)do if want[name] and not installed(c,name) then
   P.CreateBuilding(c:GetBuildQueue(),indices[name]);assert(installed(c,name),'ME_CREATE_UNCONFIRMED');d.changes=d.changes+1
  end end
 end
 local function current()
  assert(target,'ME_NO_FIXTURE')
  local c=assert(Players[target.owner]:GetCities():FindID(target.city),'ME_CITY_UNKNOWN')
  assert(c:GetOwner()==target.owner and P.IsTestPlayer(target.owner),'ME_OWNER_UNKNOWN')
  assert(SPCNetworkInput.Reference(c)==target.reference,'ME_REFERENCE_CHANGED');return c
 end
 local function plan(c)
  local f=SPCCurrentSpecializationFacts.Read(P,shared,target.owner,c)
  local w=shared.GreatWorkFacts.Summary(target.owner,target.city)
  if w then assert(w.reference==target.reference,'ME_WORK_REFERENCE_CHANGED')end
  local p=M.Plan(f,w,nil)
  if p.status=='NEEDS_DEPTH' and target.diagnostic then
   -- A deliberately fixed native-control fixture, never the D-based ability formula.
   if p.count~=1 then p.status='DIAGNOSTIC_WORK_CHANGED'
   else
    local r=shared.GreatWorkFacts.Read(target.owner,target.city)
    assert(r and r.hasConfirmed and r.availability=='KNOWN' and r.reference==target.reference,'ME_WORKS_UNKNOWN')
    if #r.works~=1 or #(r.excluded or {})~=0 or r.works[1].category~='GREATWORKOBJECT_WRITING' then p.status='DIAGNOSTIC_WORK_CHANGED'
    else
     local work=r.works[1];p.work={id=work.id,type=work.type,building=work.building,slot=work.slot}
     p.status='READY';p.each.PRODUCTION=assert(M.DiagnosticExpected[d.diagnosticStage],'ME_DIAGNOSTIC_STAGE')
     p.total.PRODUCTION=p.each.PRODUCTION
    end
   end
  elseif p.status=='NEEDS_DEPTH' then p=M.Plan(f,w,shared.DistrictCompleteness.Read(target.owner,c,f.token))end
  assert(SPCNetworkInput.Reference(c)==target.reference,'ME_REFERENCE_CHANGED');return p
 end
 local function dialogueHold(pid,c,percent)
  if target and target.normalEnvironment then
   assert(d.recipientCoverage and d.recipientCoverage.status=='VERIFIED_LOADED_SET','ME_RECIPIENT_CATALOG_UNVERIFIED')
   local actual,why=shared.Dialogue.ReadNormalForMeaning(pid,c)
   if actual==nil then
    local updated,reason=shared.Dialogue.Audit(pid,c:GetID());assert(updated,'ME_DIALOGUE_UPDATE_PENDING: '..tostring(reason))
    actual,why=shared.Dialogue.ReadNormalForMeaning(pid,c)
   end
   assert(actual~=nil,why) -- Reuse the accepted projection; no duplicate work plan.
   return
  end
  local ok,why=pcall(shared.Dialogue.HoldMeaningProbe,pid,c,percent)
  if not ok then d.error=tostring(why):sub(1,240);error(why)end
 end
 local function forget()
  if target then
   shared.Dialogue.ForgetMeaningProbe(target.owner,target.city,target.reference)
   shared.GreatWorkAdjacency.ForgetMeaningProbe(target.owner,target.city,target.reference)
  end
  target=nil;d.mode='OFF';d.diagnosticStage=nil;d.lastPlan=nil;d.error=nil;d.stopping=nil
 end
 local function finish()
  d.stopping=true
  local ok,why=pcall(function()
   local c=current();project(c,{}) -- Old writer cannot resume until this confirms.
   if shared.Dialogue.meaningOverride then shared.Dialogue.ReleaseMeaningProbe(target.owner,c)end
   shared.GreatWorkAdjacency.ReleaseMeaningProbe(target.owner,c);forget()
  end)
  if not ok then d.error=tostring(why);error(why)end
 end
 local function reset(isLoad,reason)
  -- One startup/load pass over 92 exact test-owned IDs, including saved foreign
  -- pieces. No AI ability audit; no persistent state or per-frame retry.
  if d.busy then return false,'ME_CLEANUP_BUSY' end
  d.busy=true;d.ready=false;d.cleanupStatus='CLEANING';d.cleanupReason=reason or (isLoad and 'LOAD' or 'STARTUP')
  local pending=false
  local ok,why=pcall(function()
   validate();local cities={};local supported=false
   for _,player in pairs(Players)do local collection=player:GetCities();if collection then
    for _,c in collection:Members()do
     P.Count('city_scan');cities[#cities+1]=c;assert(#cities<=2048,'ME_CLEANUP_SCOPE_LIMIT')
     if P.IsTestPlayer(c:GetOwner()) then supported=true end
    end
   end end
   -- An early/missing load notification cannot certify an empty enumeration.
   -- Existing background projection or local turn will retry when cities exist.
   if not supported then pending=true;return end
   d.cleanupPasses=d.cleanupPasses+1
   local failure
   for _,c in ipairs(cities)do
    local cleared,err=pcall(project,c,{})
    if not cleared then failure=failure or err end -- Other cities still withdraw.
   end
   assert(not failure,failure)
   if isLoad then shared.Dialogue.ready=false;shared.Dialogue.Init()
   elseif target then shared.Dialogue.WithdrawMeaningProbe(target.owner,current())
   else shared.Dialogue.Init()end -- Do not clear already-ready unrelated cities.
   forget();if isLoad then d.variant='SPLIT';d.lastAction=nil end;d.ready=true
  end)
  d.busy=false
  d.cleanupStatus=not ok and 'FAILED' or pending and 'PENDING' or 'CONFIRMED'
  d.cleanupError=not ok and tostring(why):sub(1,240) or pending and 'ME_CITIES_PENDING' or nil
  d.error=not ok and d.cleanupError or nil;d.resetFailed=not ok or nil
  return ok and not pending,d.cleanupError
 end
 function d.EnsureStartupCleanup(reason)
  if d.ready then return true end
  if d.busy then return false,'ME_CLEANUP_BUSY' end
  if d.resetFailed then return false,d.cleanupError end -- No automatic deletion storm.
  return reset(false,reason)
 end
 function d.CanProjectLegacy(pid,c,writer)
  if not c or c:GetOwner()~=pid or not P.IsTestPlayer(pid) then return false,'ME_OWNER_UNKNOWN' end
  -- Only normal Dialogue may coexist during this gate's synchronous update.
  -- GWA remains held; startup/recovery and unknown ownership never bypass exit.
  if writer=='Dialogue' and d.ready and not recoveryCity and target and target.normalEnvironment
   and target.owner==pid and target.city==c:GetID() and target.reference==SPCNetworkInput.Reference(c)
   and d.recipientCoverage and d.recipientCoverage.status=='VERIFIED_LOADED_SET' then return true end
  if not d.busy and not recoveryCity and d.EnsureStartupCleanup('LEGACY_PROJECTION') then return true end
  -- A failed city must not mix residual Meaning with the old writers. Already
  -- cleared cities may run normally, without releasing a failed fixture hold.
  local safe,why=pcall(function()
   validate();for _,name in ipairs(M.Owned)do assert(not installed(c,name),'ME_CLEANUP_RESIDUE')end
  end)
  return safe,not safe and tostring(why):sub(1,240) or nil
 end
 local function audit(scope)
  if not d.ready or d.busy or not target then return end
  if scope and ((scope.player~=nil and scope.player~=target.owner) or (scope.city~=nil and scope.city~=target.city))then return end
  d.busy=true;local c
  local ok,why=pcall(function()
   local candidate=Players[target.owner]:GetCities():FindID(target.city)
   if candidate and candidate:GetOwner()==target.owner and SPCNetworkInput.Reference(candidate)~=target.reference then
    project(candidate,{});forget();error('ME_REFERENCE_CHANGED')
   end
   c=current();P.Count('city_scan');local p=plan(c);local want={}
   assert(shared.GreatWorkAdjacency.IsMeaningHeld(target.owner,c),'ME_OLD_WRITER_NOT_HELD')
   if not d.stopping and p.status=='READY' and p.count>0 then
    dialogueHold(target.owner,c,0)
   end
   if not d.stopping and d.mode=='ACTIVE' and p.status=='READY' and p.count>0 then
    if target.diagnostic then
     for _,name in ipairs(M.DiagnosticParts(d.diagnosticStage))do want[name]=true end
    else
     for _,y in ipairs(M.ActiveWriteYields)do for _,name in ipairs(M.Parts(y,p.each[y]))do want[name]=true end end
    end
   end
   project(c,want);d.lastPlan=p
  end)
  if not ok then
   local code=tostring(why)
   -- Unknown same-reference inputs retain the last confirmed projection. A
   -- known unsafe collection/configuration removes only these ninety-two exact test IDs.
   if c and (code:find('ME_FIXTURE_UNSUPPORTED_WORK') or code:find('ME_CREATE_') or code:find('ME_ENCODING_') or code:find('ME_OLD_WRITER_'))then
    local cleared,err=pcall(project,c,{});if not cleared then why=err end
   end
  end
  d.error=not ok and tostring(why) or nil;d.busy=false
  return ok
 end
 function d.Audit(scope)
  if d.advancing then
   -- Coalesce only reentrant recalculation of this fixture. No event history.
   if target and (not scope or (scope.player==nil or scope.player==target.owner) and (scope.city==nil or scope.city==target.city))then d.deferred=true end
   return false,'TRANSITION_BUSY'
  end
  return audit(scope)
 end
 local function transition(mode,c,stage)
  local previous,previousStage=d.mode,d.diagnosticStage;d.mode=mode
  if target.diagnostic then d.diagnosticStage=stage end
  if not audit({player=c:GetOwner(),city=c:GetID()})then
   local why=d.error or 'ME_UPDATE_PENDING'
   if target then
    local percent=0
    local restored,err=true,nil
    if not target.normalEnvironment then restored,err=pcall(shared.Dialogue.RestoreMeaningProbeIntent,c:GetOwner(),c,percent)end
    if restored then d.mode=previous;d.diagnosticStage=previousStage else why=why..'; '..tostring(err)end
   end -- An exact reference exit may already have forgotten this fixture.
   error(why)
  end
 end
 local function action(fn,...)
  assert(not d.advancing and not d.busy,'ME_TRANSITION_BUSY')
  d.advancing=true;local ok,why=pcall(fn,...);d.advancing=false
  local deferred=d.deferred;d.deferred=nil
  if not ok then d.error=tostring(why):sub(1,240);error(why)end
  -- Re-read current inputs after a successful transition. This is one bounded
  -- reconciliation, not a retry loop or a once-per-turn suppression.
  if deferred and target and not d.stopping then audit({player=target.owner,city=target.city})end
 end
 local function advance(pid,c,diagnostic,normalEnvironment)
  if not d.ready then assert(reset(false,'ADVANCE'),'ME_LOAD_CLEANUP_FAILED')end
  if target and (target.owner~=pid or target.city~=c:GetID() or target.reference~=SPCNetworkInput.Reference(c))then finish()end
  assert(not target or target.diagnostic==diagnostic and target.normalEnvironment==normalEnvironment,'ME_DIAGNOSTIC_OTHER_FLOW')
  if target and diagnostic and d.error and not d.stopping then
   -- Unknown facts never turn an advance into an implicit END. Reconfirm this
   -- exact fixture once; on failure retain the stage and confirmed projection.
   assert(audit({player=pid,city=c:GetID()}),d.error or 'ME_UPDATE_PENDING')
  end
  if not target then
   target={owner=pid,city=c:GetID(),reference=SPCNetworkInput.Reference(c),x=c:GetX(),y=c:GetY(),diagnostic=diagnostic,normalEnvironment=normalEnvironment}
   d.diagnosticStage=diagnostic and 'BASELINE' or nil
   local ok,p=pcall(function()
    local value=plan(c)
    if value.status=='READY' and value.count>0 then for _,y in ipairs(M.ActiveWriteYields)do M.Parts(y,value.each[y])end end
    return value
   end) -- Validate only the authorized final-value projection before holding old effects.
   if not ok or p.status~='READY' or p.count==0 then forget();error(not ok and p or 'ME_NEEDS_CULTURE_IV_AND_WORK')end
   -- Hold first, clear by old writer's exact owned path, never use off[player].
   d.mode='BASELINE'
   local held,why=pcall(shared.GreatWorkAdjacency.HoldMeaningProbe,pid,c)
   if not held then d.error=tostring(why);error(why)end
   project(c,{});dialogueHold(pid,c,0);d.lastPlan=p;d.error=nil
  elseif d.stopping or d.error then finish()
  elseif d.mode=='BASELINE' then
   -- Repeat the old module's confirmation before any new native write.
   shared.GreatWorkAdjacency.HoldMeaningProbe(pid,c)
   local p=plan(c);assert(p.status=='READY' and p.count>0,'ME_NEEDS_CULTURE_IV_AND_WORK')
   transition('ACTIVE',c,diagnostic and 'SINGLE1' or nil)
  elseif diagnostic then
   local p=plan(c);assert(p.status=='READY' and p.count==1,'ME_DIAGNOSTIC_WORK_REQUIRED')
   local nextStage=({SINGLE1='CLEAR1',CLEAR1='SINGLE2',SINGLE2='PAIR12',PAIR12='REMAIN2',REMAIN2='SINGLE3'})[d.diagnosticStage]
   if nextStage then
    -- PAIR12 starts clean, in +1/+2 order; SINGLE3 is an independent flat3.
    -- REMAIN2 deliberately uses project({+2}) without clearing the healthy +2:
    -- its native instance must survive while only the +1 instance is removed.
    if nextStage=='PAIR12' or nextStage=='SINGLE3' then project(c,{})end
    transition('ACTIVE',c,nextStage)
   else finish()end
  else finish()end
 end
 function d.Advance(pid,c,token)
  assert(P.IsTestPlayer(pid) and c and c:GetOwner()==pid,'ME_OWNER_UNKNOWN')
  if token then
   assert(type(token)=='string' and #token>0 and #token<=100,'ME_ACTION_TOKEN')
   local old=d.lastAction
   if old and old.token==token then
    assert(old.owner==pid and old.city==c:GetID() and old.kind=='ADVANCE','ME_ACTION_TOKEN_CONFLICT');return
   end
  end
  return action(function()
   if token then d.lastAction={token=token,owner=pid,city=c:GetID(),kind='ADVANCE'}end -- One bounded receipt.
   advance(pid,c,false)
  end)
 end
 function d.GateAdvance(pid,c,token)
  assert(P.IsTestPlayer(pid) and c and c:GetOwner()==pid,'ME_OWNER_UNKNOWN')
  assert(type(token)=='string' and #token>0 and #token<=100,'ME_ACTION_TOKEN')
  local old=d.lastAction
  if old and old.token==token then
   assert(old.owner==pid and old.city==c:GetID() and old.kind=='GATE_ADVANCE','ME_ACTION_TOKEN_CONFLICT');return
  end
  return action(function()
   d.lastAction={token=token,owner=pid,city=c:GetID(),kind='GATE_ADVANCE'}
   if not d.recipientCoverage then d.recipientCoverage=M.RecipientCoverage(P)end
   assert(d.recipientCoverage.status=='VERIFIED_LOADED_SET','ME_RECIPIENT_CATALOG_UNVERIFIED: '..table.concat(d.recipientCoverage.reasons,';'))
   advance(pid,c,false,true)
  end)
 end
 function d.DiagnosticAdvance(pid,c,token)
  assert(P.IsTestPlayer(pid) and c and c:GetOwner()==pid,'ME_OWNER_UNKNOWN')
  if token then
   assert(type(token)=='string' and #token>0 and #token<=100,'ME_ACTION_TOKEN')
   local old=d.lastAction
   if old and old.token==token then
    assert(old.owner==pid and old.city==c:GetID() and old.kind=='DIAGNOSTIC_ADVANCE','ME_ACTION_TOKEN_CONFLICT');return
   end
  end
  return action(function()
   if token then d.lastAction={token=token,owner=pid,city=c:GetID(),kind='DIAGNOSTIC_ADVANCE'}end
   advance(pid,c,true)
  end)
 end
 -- Reject queued old UI configuration requests; no candidate can be enabled.
 function d.CycleVariant(pid,c,token)
  assert(P.IsTestPlayer(pid) and c and c:GetOwner()==pid,'ME_OWNER_UNKNOWN')
  error('ME_VARIANT_DEFERRED')
 end
 function d.View(pid,c,diagnostic)
  local ref=SPCNetworkInput.Reference(c)
  local match=target and target.owner==pid and target.city==c:GetID() and target.reference==ref
  local p=match and d.lastPlan or nil
  local diagnosticFlow=diagnostic or match and target.diagnostic
  local finalNames={};for y,values in pairs(M.FinalValues)do for _,part in ipairs(values)do finalNames[part.name]={yield=y,amount=part.amount}end end
  local configured={SCIENCE=0,GOLD=0,PRODUCTION=0,FOOD=0,FAITH=0,CULTURE=0}
  local stamp={};if p then for _,entry in ipairs(M.Domains)do local v=p.domains[entry[1]];stamp[#stamp+1]=entry[1]..':'..tostring(v and v.value)end end
  local dialoguePercent,dialogueError
  if match then
   if target.normalEnvironment then dialoguePercent,dialogueError=shared.Dialogue.ReadNormalForMeaning(pid,c)
   else dialoguePercent,dialogueError=shared.Dialogue.ReadMeaningProbe(pid,c)end
  end
  local q=match and shared.Dialogue.meaningQualification
  if q and (q.owner~=pid or q.city~=c:GetID() or q.reference~=ref)then q=nil end
  local read,why=pcall(function()
   validate();for _,y in ipairs(M.WriteYields)do for bit=0,M.ProbeBits[y]-1 do
    local name='BUILDING_SPC_MEANING_PROBE_'..y..'_'..bit
    if installed(c,name) then
     local damaged=c:GetBuildings():IsPillaged(indices[name]);assert(type(damaged)=='boolean','ME_CARRIER_HEALTH_UNKNOWN')
     if not damaged then configured[y]=configured[y]+2^bit/M.ProbeScale[y] end
    end
   end end
   if installed(c,M.DiagnosticSingle3.name) then
    local damaged=c:GetBuildings():IsPillaged(indices[M.DiagnosticSingle3.name]);assert(type(damaged)=='boolean','ME_CARRIER_HEALTH_UNKNOWN')
    if not damaged then configured.PRODUCTION=configured.PRODUCTION+M.DiagnosticSingle3.amount end
   end
   local finalCounts={}
   for y,values in pairs(M.FinalValues)do
    finalCounts[y]=0
    for _,part in ipairs(values)do if installed(c,part.name) then
     finalCounts[y]=finalCounts[y]+1
     local damaged=c:GetBuildings():IsPillaged(indices[part.name]);assert(type(damaged)=='boolean','ME_CARRIER_HEALTH_UNKNOWN')
     if not damaged then configured[y]=configured[y]+part.amount end
    end end
   end
   if not diagnosticFlow then
    assert(not M.CultureDeferred or finalCounts.CULTURE==0,'ME_DEFERRED_CULTURE_PRESENT')
    for _,n in pairs(finalCounts)do assert(n<=1,'ME_MULTIPLE_FINAL_VALUES')end
    for _,name in ipairs(M.Owned)do
     assert(finalNames[name] or not installed(c,name),'ME_LEGACY_PROJECTION_PRESENT')
    end
   end
   -- Failed old Culture pieces are not valid restored final values.
   -- End/load use the same exact directory, never a prefix sweep.
   for bit=0,M.ProbeBits.CULTURE-1 do
    assert(not installed(c,'BUILDING_SPC_MEANING_PROBE_CULTURE_'..bit),'ME_LEGACY_CULTURE_PRESENT')
   end
   for _,part in pairs(M.VariantParts)do assert(not installed(c,part.name),'ME_LEGACY_CULTURE_PRESENT')end
  end)
  local v={variant=d.variant,configuredScience=read and configured.SCIENCE or nil,configuredGold=read and configured.GOLD or nil,configuredCulture=read and configured.CULTURE or nil,configuredProduction=read and configured.PRODUCTION or nil,configuredFood=read and configured.FOOD or nil,configuredFaith=read and configured.FAITH or nil,configurationError=not read and tostring(why) or nil,
   owner=pid,cityID=c:GetID(),reference=ref,mode=match and d.mode or 'OFF',error=d.error,
   cleanupStatus=d.cleanupStatus,cleanupError=d.cleanupError,cleanupReason=d.cleanupReason,
   currentIdentity=q and q.specialization,currentPotential=q and q.potential,currentActive=q and q.active,currentActiveStatus=q and q.activeStatus,
   active=p and p.active,count=p and p.count,science=p and p.each.SCIENCE,gold=p and p.each.GOLD,culture=p and p.each.CULTURE,production=p and p.each.PRODUCTION,food=p and p.each.FOOD,faith=p and p.each.FAITH,
   totalScience=p and p.total.SCIENCE,totalGold=p and p.total.GOLD,totalCulture=p and p.total.CULTURE,totalProduction=p and p.total.PRODUCTION,totalFood=p and p.total.FOOD,totalFaith=p and p.total.FAITH,planStatus=p and p.status,
   campus=p and p.domains.DISTRICT_CAMPUS and p.domains.DISTRICT_CAMPUS.value,
   commerce=p and p.domains.DISTRICT_COMMERCIAL_HUB and p.domains.DISTRICT_COMMERCIAL_HUB.value,
   harbor=p and p.domains.DISTRICT_HARBOR and p.domains.DISTRICT_HARBOR.value,
   oldHeld=match and shared.GreatWorkAdjacency.IsMeaningHeld(pid,c) or false,
   dialoguePercent=dialoguePercent,dialogueError=dialogueError,stamp=table.concat(stamp,';')}
  v.finalValues=not diagnosticFlow;v.productionOnly=false;v.cultureDeferred=M.CultureDeferred
  v.normalEnvironment=match and target.normalEnvironment==true or false
  local coverage=d.recipientCoverage
  v.recipientStatus=coverage and coverage.status;v.recipientCount=coverage and coverage.verified
  v.recipientBlocked=coverage and coverage.blocked;v.recipientReason=coverage and table.concat(coverage.reasons,';')
  if diagnosticFlow then
   v.diagnostic=true;v.diagnosticStage=match and target.diagnostic and d.diagnosticStage or 'OFF'
   v.diagnosticExpected=assert(M.DiagnosticExpected[v.diagnosticStage],'ME_DIAGNOSTIC_STAGE')
   v.diagnosticWork=p and p.work
   local f=SPCCurrentSpecializationFacts.Read(P,shared,pid,c)
   v.currentIdentity=f.identity;v.currentPotential=f.potential;v.currentActive=f.active
   v.currentActiveStatus=f.validity=='VERIFIED' and f.activeStatus or 'UNKNOWN_FACTS'
  end
  local rows={};local known,reason=pcall(function()
    validate()
    for _,name in ipairs(M.Owned)do if installed(c,name) then
     local pillaged=c:GetBuildings():IsPillaged(indices[name]);assert(type(pillaged)=='boolean','ME_CARRIER_HEALTH_UNKNOWN')
     local y,bit=name:match('^BUILDING_SPC_MEANING_PROBE_([A-Z]+)_(%d+)$');local amount
     if y then amount=2^tonumber(bit)/M.ProbeScale[y]
     elseif finalNames[name] then y=finalNames[name].yield;amount=finalNames[name].amount
     elseif name==M.DiagnosticSingle3.name then y='PRODUCTION';amount=M.DiagnosticSingle3.amount
     else for _,part in pairs(M.VariantParts)do if part.name==name then y='CULTURE';amount=part.amount end end end
     assert(y and amount,'ME_DEFINITION_UNKNOWN');rows[#rows+1]={name=name,yield=y,amount=amount,pillaged=pillaged}
    end end
   end)
   v.diagnosticCarriers=known and rows or nil;v.remainingOwned=known and #rows or nil
   if not known then v.configurationError=v.configurationError or tostring(reason)end
   if diagnosticFlow and match and not target.diagnostic then v.error=v.error or 'ME_DIAGNOSTIC_OTHER_FLOW'end
  return v
 end
 function d.End(pid,c,token)
  assert(P.IsTestPlayer(pid) and c and c:GetOwner()==pid,'ME_OWNER_UNKNOWN')
  if token then
   assert(type(token)=='string' and #token>0 and #token<=100,'ME_ACTION_TOKEN')
   local old=d.lastAction
   if old and old.token==token then
    assert(old.owner==pid and old.city==c:GetID() and old.kind=='END','ME_ACTION_TOKEN_CONFLICT');return
   end
  end
  return action(function()
   if not target and d.mode=='OFF' and token then
    d.lastAction={token=token,owner=pid,city=c:GetID(),kind='END'}
    -- OFF describes the session only. Explicit END must withdraw saved pieces,
    -- not merely acknowledge a token. Keep this recovery scoped to this city.
    recoveryCity=c;d.busy=true;local cleared,why=pcall(project,c,{});d.busy=false
    if not cleared then
     d.ready=false;d.resetFailed=true;d.cleanupStatus='FAILED';d.cleanupError=tostring(why):sub(1,240)
    end
    -- During this explicit scoped recovery, do not start a global sweep. Both
    -- old writers independently check exact absence; on failure they withdraw
    -- their own pieces instead of restoring a saved/current positive effect.
    local resumed,err=pcall(function()
     shared.Dialogue.Audit(pid,c:GetID());shared.GreatWorkAdjacency.Audit(pid,c:GetID())
    end)
    recoveryCity=nil;assert(cleared,why);assert(resumed,err)
    d.error=nil;return
   end
   assert(target and target.owner==pid and target.city==c:GetID(),'ME_NO_FIXTURE')
   if token then d.lastAction={token=token,owner=pid,city=c:GetID(),kind='END'}end
   finish()
  end)
 end
 function d.Describe(pid,c,view)
  local v=view or d.View(pid,c)
  if v.diagnostic then
   local names={OFF='已关闭',BASELINE='①基线',SINGLE1='②单片＋1',CLEAR1='③撤销至0（仍在对照）',SINGLE2='④单片＋2',PAIR12='⑤两片＋1／＋2',REMAIN2='⑥仅撤＋1，保留＋2',SINGLE3='⑦独立单片＋3'}
   local nextText={BASELINE='左键：单片＋1。',SINGLE1='左键：只撤＋1至0。',CLEAR1='旧收益仍暂停；左键：重新配置单片＋2。',SINGLE2='左键：清空后建立两片＋1／＋2。',PAIR12='已知组合对照；左键：只撤＋1，保留＋2。',REMAIN2='左键：清空后建立独立单片＋3。',SINGLE3='左键：结束。'}
   local lines={'生产力组合诊断｜'..(names[v.diagnosticStage] or '未确认')}
   lines[#lines+1]='首次清理：'..(({CONFIRMED='已确认',PENDING='待城市就绪',CLEANING='进行中',FAILED='失败，需处理'})[v.cleanupStatus] or '未确认')
   if v.diagnosticStage=='OFF' then lines[#lines+1]='左键开始；右键只读退出状态。'
   else lines[#lines+1]=(nextText[v.diagnosticStage] or '状态未确认，先结束。')..' 右键读取实例；可随时结束。'end
   local err=v.error or v.configurationError or v.dialogueError
   if err then lines[#lines+1]='待处理：'..(tostring(err):match('ME_[A-Z_]+') or '接口未确认')..'；先结束。'
   elseif v.planStatus=='DIAGNOSTIC_WORK_CHANGED' then lines[#lines+1]='作品条件已变，新片已撤；需本城仅1件著作。'
   elseif v.diagnosticStage=='OFF' then lines[#lines+1]='OFF不等于原生撤销通过，请右键核对。'end
   return table.concat(lines,'\n')
  end
  local names={OFF='未开启',BASELINE='①基线',ACTIVE='②追加中'}
  local lines={'意义延展｜'..(names[v.mode] or '状态未确认')..'｜五产出单值'}
  lines[#lines+1]='文化追加暂隔离；HD原有效果保持。'
  if v.normalEnvironment then
   lines[#lines+1]='正常时代对话＋'..tostring(v.dialoguePercent or '未确认')..'%；主题状态保持。'
   lines[#lines+1]='已加载recipient核对：'..tostring(v.recipientCount)..'个已支持定义；此结论仅限当前规则环境。'
  elseif v.recipientBlocked and v.recipientBlocked>0 then
   lines[#lines+1]='接入门禁未通过：'..v.recipientBlocked..'个同类定义未获支持；未启用新追加。'
   lines[#lines+1]=v.recipientReason
  end
  if v.cleanupStatus~='CONFIRMED' then lines[#lines+1]='首次清理尚未确认：'..tostring(v.cleanupStatus)end
  if v.count then lines[#lines+1]=string.format('合格%d件｜当前ACTIVE %s',v.count,tostring(v.currentActiveStatus=='KNOWN' and v.currentActive or '未确认'))end
  if v.mode=='OFF' then lines[#lines+1]='左键准备基线；需文化ACTIVE4及确认馆藏。'
  elseif v.mode=='BASELINE' then lines[#lines+1]='先右键记录基线，再左键启用。'
  else lines[#lines+1]='右键查看五项预期／原生差值；结束验证可撤回。'end
  if v.currentActiveStatus and v.currentActiveStatus~='KNOWN' then lines[#lines+1]='当前资格未确认，UNKNOWN不当作0。'end
  local err=v.error or v.configurationError or v.dialogueError
  if err then lines[#lines+1]='待处理：'..(tostring(err):match('ME_[A-Z_]+') or '接口未确认')..'；先结束验证。'end
  return table.concat(lines,'\n')
 end

 local store=shared.CityProgressionStore
 if store then store.RegisterExit('CultureMeaningProbe',function(c,loss)
  assert(store.IsExitTarget(c,loss),'ME_EXIT_UNCONFIRMED')
  store.RemoveOwned(c,loss,M.Owned)
  if target and target.owner==loss.origin.owner and target.x==c:GetX() and target.y==c:GetY() then forget()end
 end)end
 local function bind(source,name,fn)local e=P.Field(source,name);if e and e.Add then e.Add(fn)end end
 bind(Events,'LoadScreenClose',function()reset(true)end)
 local lastTurn
 bind(Events,'PlayerTurnActivated',function(pid)
  if not P.IsTestPlayer(pid)then return end
  if not d.ready and not d.resetFailed then d.EnsureStartupCleanup('PLAYER_TURN')end
  local turn=Game.GetCurrentGameTurn();if lastTurn~=turn then lastTurn=turn;d.Audit({player=pid})end
 end)
 bind(Events,'CityBuildingsChanged',function(pid,cid)d.Audit({player=pid,city=cid})end)
 for _,name in ipairs({'BuildingAddedToMap','BuildingRemovedFromMap'})do bind(Events,name,function(x,y,id,owner)
  if not target or d.busy then return end
  local row=P.Info('Buildings',id);local typ=row and row.BuildingType
  if typ and (indices and indices[typ] or shared.GreatWorkAdjacency.IsOwnedCarrier(typ) or shared.Dialogue.IsOwnedCarrier(typ))then return end
  if type(owner)=='number' and owner>=0 and owner%1==0 and owner~=target.owner then return end
  local ok,c=pcall(function()local district=CityManager.GetDistrictAt and CityManager.GetDistrictAt(x,y);return district and district:GetCity() or CityManager.GetCityAt(x,y)end)
  d.Audit({player=owner,city=ok and c and c:GetID() or nil})
 end)end
 -- Native signatures vary; fallback is still only the current one-city fixture.
 for _,name in ipairs({'BuildingPillaged','BuildingRepaired','DistrictRemovedFromMap','DistrictBuildProgressChanged','DistrictPillaged','DistrictRepaired','GovernorAssigned','GovernorEstablished','GovernorChanged','GovernorPromoted'})do
  bind(Events,name,function()d.Audit()end)
 end
 for _,name in ipairs({'BuildingConstructed','OnDistrictConstructed','OnPillage'})do bind(GameEvents,name,function()d.Audit()end)end
 -- Called only after both Receive functions accepted this exact request.
 -- The Facts callback remains owned by the existing independent consumers.
 function d.CollectionConfirmed(pid,packet)
  if not target or pid~=target.owner then return false end
  local c=current();local paired,why=shared.Dialogue.IsMeaningSampleCurrent(pid,c,packet)
  if not paired then return false,why end
  d.Audit({player=pid,city=target.city}) -- Also refresh unchanged collections on a new turn.
  return not d.busy and not d.error
 end
end
