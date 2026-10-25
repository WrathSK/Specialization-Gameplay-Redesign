include('CurrentSpecializationFacts')
include('RuntimeWork')
include('NetworkInput')
include('ReverseDependencies')
include('ExpeditionTrainingDiagnostics')
-- B226: current network projection only. Store owns history; Bridge owns topology;
-- native district workers own the yield count. No received history or timer.
SPCCultureNetwork={Bits=8,Owned={},Districts={RESEARCH='DISTRICT_CAMPUS',CULTURE='DISTRICT_THEATER',INDUSTRY='DISTRICT_INDUSTRIAL_ZONE',COMMERCE='DISTRICT_COMMERCIAL_HUB'}}
local M=SPCCultureNetwork
local function name(kind,bit)return 'BUILDING_SPC_CULTURE_NETWORK_'..kind..'_'..bit end
for _,kind in ipairs({'RESEARCH','CULTURE','INDUSTRY','COMMERCE'})do
 for bit=0,M.Bits-1 do M.Owned[#M.Owned+1]=name(kind,bit)end
end
local function int(n)return type(n)=='number' and n>=0 and n<math.huge and n%1==0 end
function M.Source(records,own)
 assert(type(records)=='table' and type(own)=='string','CN_HISTORY_UNKNOWN')
 local groups,out={},{};local n=0
 for key,r in pairs(records)do
  assert(type(r)=='table' and type(r.civ)=='string' and key==r.civ..':'..tostring(r.category)
   and (r.category=='PEOPLE' or r.category=='WORKS' or r.category=='PLACES'),'CN_HISTORY_INVALID')
  n=n+1;assert(n<=192,'CN_HISTORY_RANGE')
  if r.civ~=own then groups[r.civ]=groups[r.civ] or {};groups[r.civ][r.category]=true end
 end
 for civ,t in pairs(groups)do if t.PEOPLE and t.WORKS and t.PLACES then out[civ]=true end end
 return out
end
 local function diagnosticCode(value)
  if value==nil then return 'NONE'end
  if type(value)=='boolean' or type(value)=='number'then return tostring(value)end
  if type(value)~='string'then return 'UNKNOWN'end
  return (value:match('(CN_[A-Z0-9_]+)') or value:match('([A-Z][A-Z0-9_]+)$') or 'READ_ERROR'):sub(1,48)
 end
function M.Start(P,shared)
 local store=assert(shared.CityProgressionStore,'CN_STORE_REQUIRED')
 local d={ready=false,busy=false,records={},errors={},changes=0};shared.CultureNetwork=d
 local dependents=SPCReverseDependencies.New()
 local function replaceDependencies(pid,cid,sources)
  local ok,why=dependents.Replace(pid,cid,sources)
  if not ok then d.dependencyIndexError=why end -- scalar cache degradation, not a business failure
 end
 local definitions,dirty,sourceSamples,sourceCounts={},{},{},{};local initialized=false
 local ownedIndex={}
 local carrierHealth=SPCRuntimeWork.NativeHealth(P,shared,d,function(id)return ownedIndex[id]==true end,function(scope)d.Mark(scope.player,scope.city)end)
 local trace;local lastWait;local lastHealth;local observe
 if SPCExpeditionTrainingDiagnostics then
  local ok,value=pcall(SPCExpeditionTrainingDiagnostics.New,P,'CULTURE_NETWORK')
  if ok then trace=value end
 end
 local function health(pid,reason,failure)
  local bridge=shared.NetworkBridge;local b=bridge and bridge.players and bridge.players[pid]
  local signature=table.concat({tostring(pid),tostring(d.ready),reason,diagnosticCode(b and b.availability),diagnosticCode(b and b.inputRevision),failure and failure.phase or '',failure and failure.errorFile or '',failure and tostring(failure.errorLine) or ''},':')
  if signature==lastHealth then return end
  if trace then pcall(trace.Record,'NETWORK_HEALTH',{owner=pid,ready=d.ready,reason=reason,
   bridgeReady=bridge and bridge.ready==true,networkError=reason=='CN_READY' and 'NONE' or reason,
   phase=failure and failure.phase,errorCode=failure and failure.errorCode,errorClass=failure and failure.errorClass,
   errorFile=failure and failure.errorFile,errorLine=failure and failure.errorLine,eventOwner=failure and failure.owner,
   eventCity=failure and failure.city,
   networkValidity=diagnosticCode(b and b.validity),networkAvailability=diagnosticCode(b and b.availability),
   networkInputRevision=diagnosticCode(b and b.inputRevision),networkDerivedFor=diagnosticCode(b and b.derivedFor)})end
  lastHealth=signature
 end
 local function key(pid,id)return tostring(pid)..':'..tostring(id)end
 local function ref(c)return SPCNetworkInput.Reference(c)end
 local function forgetSource(pid,id)
  local k=key(pid,id);if sourceSamples[k]then sourceSamples[k]=nil;sourceCounts[pid]=math.max(0,(sourceCounts[pid] or 1)-1)end
 end
 local function isolated(pid)return shared.NetworkIsolation and shared.NetworkIsolation.Active(pid)==true end
 local function validate()
  if definitions[1]then return end
  local allowed={};local count=0
  for _,r in ipairs(assert(P.Rows('Civilizations'),'CN_CIV_DATABASE_UNKNOWN'))do
   assert(type(r.CivilizationType)=='string','CN_CIV_DATABASE_UNKNOWN')
   if not allowed[r.CivilizationType]then allowed[r.CivilizationType]=true;count=count+1 end
  end
  assert(count>0 and count<2^M.Bits,'CN_LOADED_CIV_ENCODING_RANGE') -- encoding, never clamp a gameplay set
  local yields={}
  for _,row in ipairs(assert(P.Rows('Building_CitizenYieldChanges'),'CN_YIELD_DATABASE_UNKNOWN'))do
   yields[row.BuildingType]=yields[row.BuildingType] or {};table.insert(yields[row.BuildingType],row)
  end
  local rows,nextOwned={},{}
  for _,kind in ipairs({'RESEARCH','CULTURE','INDUSTRY','COMMERCE'})do for bit=0,M.Bits-1 do
   local id=name(kind,bit);local r=assert(P.Info('Buildings',id),'CN_CARRIER_MISSING');local ys=yields[id]
   assert(r.PrereqDistrict==M.Districts[kind] and (r.InternalOnly==1 or r.InternalOnly==true)
    and r.CitizenSlots==0 and r.Housing==0,'CN_CARRIER_INVALID')
   assert(ys and #ys==1 and ys[1].YieldType=='YIELD_CULTURE' and ys[1].YieldChange==2^bit,'CN_YIELD_INVALID')
   rows[#rows+1]={id=r.Index,kind=kind,bit=bit};nextOwned[r.Index]=true
  end end
  definitions=rows;ownedIndex=nextOwned;d.allowedCivilizations=allowed
 end
 local function remove(c,row)
  carrierHealth.Remove(c,row.id)
  assert(P.HasBuilding(c:GetBuildings(),row.id)==false,'CN_REMOVE_UNCONFIRMED');d.changes=d.changes+1
 end
 local function clear(c)
  d.writing=key(c:GetOwner(),c:GetID())
  local ok,why=pcall(function()
   local present={}
   for _,row in ipairs(definitions)do
    local yes=P.HasBuilding(c:GetBuildings(),row.id);assert(type(yes)=='boolean','CN_PRESENCE_UNKNOWN')
    if yes then present[#present+1]=row end
   end
   for _,row in ipairs(present)do remove(c,row)end
  end)
  d.writing=nil;assert(ok,why)
 end
 local function facts(batch,pid,c)
  local id=c:GetID();if not batch.facts[id]then batch.facts[id]=SPCCurrentSpecializationFacts.Read(P,shared,pid,c)end
  return batch.facts[id]
 end
 local function anchor(batch,pid,c)
  assert(c:GetOwner()==pid,'CN_RECEIVER_OWNER_CHANGED')
  local f=facts(batch,pid,c);assert(f.validity=='VERIFIED' and type(f.identity)=='string','CN_RECEIVER_UNKNOWN')
  if f.identity=='NONE' then return nil end
  local domain=assert(M.Districts[f.identity],'CN_IDENTITY_UNSUPPORTED')
  assert(int(f.potential) and f.potential>=1 and f.first and int(f.first.districtID),'CN_ANCHOR_UNKNOWN')
  -- Receiver qualification is Identity, not ACTIVE. Avoid the support helper's ACTIVE gate.
  local ds=c:GetDistricts();local n=ds:GetNumDistricts();assert(int(n) and n<=256,'CN_DISTRICT_UNKNOWN')
  local found,count=nil,0
  for i=0,n-1 do
   local district=assert(ds:GetDistrictByIndex(i),'CN_DISTRICT_UNKNOWN')
   local row=assert(P.Info('Districts',district:GetType()),'CN_DISTRICT_UNKNOWN')
   if P.Family(row.DistrictType)==f.identity then
    count=count+1
    if district:GetID()==f.first.districtID then
     local complete,pillaged=district:IsComplete(),district:IsPillaged()
     assert(type(complete)=='boolean' and type(pillaged)=='boolean','CN_DISTRICT_UNKNOWN')
     assert(row.DistrictType==f.first.type,'CN_ANCHOR_CHANGED')
     if complete and not pillaged then found=district end
    end
   end
  end
  assert(count<=1,'CN_MULTIPLE_IDENTITY_DISTRICTS')
  if not found then return nil end
  local plot=assert(Map.GetPlot(found:GetX(),found:GetY()),'CN_PLOT_UNKNOWN'):GetIndex()
  assert(int(plot),'CN_PLOT_UNKNOWN');return f.identity,plot
 end
 local function source(batch,pid,id)
  if batch.sources[id]then return batch.sources[id]end
  local out={set={},eligible=false,provenance='CONFIRMED'};batch.sources[id]=out
  local ok,err=pcall(function()
   local c=Players[pid]:GetCities():FindID(id)
   if c then assert(type(c:GetOwner())=='number','CN_SOURCE_OWNER_UNKNOWN')end
   if not c or c:GetOwner()~=pid then out.confirmedLoss=true;return end
   out.reference=ref(c);local f=facts(batch,pid,c)
   assert(f.validity=='VERIFIED' and type(f.identity)=='string','CN_SOURCE_UNKNOWN')
   if f.identity~='CULTURE' then return end
   assert(int(f.potential),'CN_SOURCE_UNKNOWN');if f.potential<4 then return end
   assert(f.activeStatus=='KNOWN' and int(f.active),'CN_SOURCE_ACTIVE_UNKNOWN')
   if f.active<4 then return end
   assert(f.active==4 and f.potential==4,'CN_SOURCE_LEVEL_INVALID');out.eligible=true
   local config=PlayerConfigurations and PlayerConfigurations[pid]
   local own=config and config:GetCivilizationTypeName();assert(d.allowedCivilizations[own],'CN_OWNER_CIV_UNKNOWN')
   out.set=M.Source(store.ExpeditionInsights(pid,c),own)
   for civ in pairs(out.set)do assert(d.allowedCivilizations[civ],'CN_HISTORY_CIV_UNKNOWN')end
   assert(c:GetOwner()==pid and ref(c)==out.reference,'CN_SOURCE_CHANGED')
  end)
  local k=key(pid,id);local old=sourceSamples[k]
  if old and out.reference and old.reference~=out.reference then forgetSource(pid,id);old=nil end
  if not ok then
   out.error=tostring(err)
   if old and not out.confirmedLoss and (out.reference==nil or old.reference==out.reference)then
    out.reference=out.reference or old.reference
    out.set={};for civ in pairs(old.set)do out.set[civ]=true end
    out.eligible=old.eligible;out.provenance='RETAINED'
   else out.set={};out.provenance='UNKNOWN' end
  else
   local saved={reference=out.reference,eligible=out.eligible,set={}}
   for civ in pairs(out.set)do saved.set[civ]=true end
   if old or (sourceCounts[pid] or 0)<512 then
    if not old then sourceCounts[pid]=(sourceCounts[pid] or 0)+1 end
    sourceSamples[k]=saved
   end
  end
  return out
 end
 local function network(batch,pid)
  assert(not batch.networkFailed,batch.networkFailed)
  if batch.network then return batch.network end
  local bridge=assert(shared.NetworkBridge,'CN_NETWORK_UNAVAILABLE');local input=bridge.Input(pid)
  if input.validity=='CONFIRMED_INVALID' then batch.network={input=input,recipients={}};return batch.network end
  local current=bridge.CurrentCultureBatch(pid,batch.selection)
  assert(current.input.validity=='VERIFIED' and (current.input.effectAvailability=='AVAILABLE' or current.input.effectAvailability==nil and current.input.availability=='AVAILABLE' or current.input.continuityOnly),'CN_NETWORK_PENDING')
  batch.network=current;return current
 end
 local function plan(batch,pid,c,old)
  local kind,plot=anchor(batch,pid,c);local p={kind=kind,plot=plot,n=0,set={},sources={},contributors={},contributions={},provenance={}}
  if not kind then return p end
  local view=network(batch,pid)
  for id in pairs(view.recipients[c:GetID()] or {})do
   local s=source(batch,pid,id)
   if view.input.continuityOnly and s.eligible then
    local prior=old and old.contributions and old.contributions[id]
    if prior and prior.reference==s.reference then s={reference=prior.reference,set=prior.set,eligible=prior.eligible,provenance='RETAINED'} else s={set={},reference=s.reference,provenance='UNKNOWN'}end
    p.reason='CN_RETAINED_TOPOLOGY'
   end
   if s.provenance~='CONFIRMED' then p.reason=s.error or 'CN_MIXED_FACTS' end
   p.provenance[id]={reference=s.reference,status=s.provenance}
   p.contributions[id]={reference=s.reference,set=s.set,eligible=s.eligible,provenance=s.provenance}
   p.sources[id]=s.reference or false
   if next(s.set)then p.contributors[id]=s.reference end
   for civ in pairs(s.set)do p.set[civ]=true end
  end
  for _ in pairs(p.set)do p.n=p.n+1 end
  assert(p.n<2^M.Bits,'CN_UNION_ENCODING_RANGE');return p
 end
 local function negativePlan(batch,pid,c,old)
  if not old or not next(old.contributions or {})then return nil end
  local p={kind=old.kind,plot=old.plot,n=0,set={},sources={},contributors={},contributions={},provenance={},reason='CN_RETAINED_TOPOLOGY'}
  local changed=false
  for id,prior in pairs(old.contributions)do
   local found,live=pcall(function()return Players[pid]:GetCities():FindID(id)end)
   local ownerOK,owner=pcall(function()return live and live:GetOwner()end)
   local lost=found and (not live or ownerOK and type(owner)=='number' and owner~=pid)
   local check,reference=pcall(function()return live and ref(live)end)
   if check and reference~=prior.reference then lost=true end
   if not lost and live then
    local ok,f=pcall(facts,batch,pid,live)
    if ok and f.validity=='VERIFIED' and (f.identity~='CULTURE' or int(f.potential) and f.potential<4
     or f.activeStatus=='KNOWN' and int(f.active) and f.active<4)then lost=true end
   end
   if lost then forgetSource(pid,id);changed=true else
    p.sources[id]=prior.reference;p.contributions[id]=prior;p.provenance[id]={reference=prior.reference,status='RETAINED'}
    if next(prior.set)then p.contributors[id]=prior.reference end
    for civ in pairs(prior.set)do p.set[civ]=true end
   end
  end
  if not changed then return nil end
  for _ in pairs(p.set)do p.n=p.n+1 end;return p
 end
 local function reconcile(batch,pid,c)
  local k=key(pid,c:GetID());local reference=ref(c);local old=d.records[k]
  if old and old.reference~=reference then clear(c);d.records[k]=nil;dependents.Remove(pid,c:GetID());old=nil end
  local ok,p=pcall(plan,batch,pid,c,old)
  if not ok then
   local reason=p;p=negativePlan(batch,pid,c,old)
   if not p then
    if old then
     old.retained=true;old.reason=tostring(reason);local provenance={}
     for id,f in pairs(old.provenance or {})do provenance[id]={reference=f.reference,status=f.status=='UNKNOWN' and 'UNKNOWN' or 'RETAINED'}end
     old.provenance=provenance
    end
    error(reason)
   end
  end
  assert(c:GetOwner()==pid and ref(c)==reference,'CN_RECEIVER_CHANGED')
  d.writing=k
  -- A health cause cannot turn retained topology into a new positive fact.
  -- Confirmed logical changes (including anchor/source loss) still reconcile.
  local pending=batch.networkFailed or batch.network and batch.network.input.continuityOnly
  local held=pending and old and p.kind~=nil and old.kind==p.kind and old.plot==p.plot and old.n==p.n
  local mutating=false
  local wrote,why=pcall(function()
   if held then return end
   local rows={};local b=c:GetBuildings()
   for _,def in ipairs(definitions)do
    local yes=P.HasBuilding(b,def.id);assert(type(yes)=='boolean','CN_PRESENCE_UNKNOWN')
    local want=def.kind==p.kind and math.floor(p.n/2^def.bit)%2==1
    local row={id=def.id,want=want,yes=yes};rows[#rows+1]=row
    if yes then
     local at,damage=b:GetBuildingLocation(def.id),b:IsPillaged(def.id)
     assert(int(at) and type(damage)=='boolean','CN_LOCATION_UNKNOWN')
     row.remove=not want or at~=p.plot or damage
    end
   end
   for _,row in ipairs(rows)do if row.remove then mutating=true;remove(c,row);row.yes=false end end
   for _,row in ipairs(rows)do if row.want and not row.yes then
    mutating=true;carrierHealth.Create(c,row.id)
    assert(P.HasBuilding(b,row.id)==true and b:GetBuildingLocation(row.id)==p.plot and b:IsPillaged(row.id)==false,'CN_CREATE_UNCONFIRMED')
    d.changes=d.changes+1
   end end
   assert(c:GetOwner()==pid and ref(c)==reference,'CN_RECEIVER_CHANGED')
  end)
  d.writing=nil
  if not wrote then
   if mutating then d.records[k]=nil;dependents.Remove(pid,c:GetID());pcall(clear,c)end
   error(why)
  end
  p.retained=held or nil;p.reference=reference;p.owner=pid;p.id=c:GetID();p.x=c:GetX();p.y=c:GetY();d.records[k]=p;replaceDependencies(pid,c:GetID(),p.sources);d.errors[k]=p.reason
 end
 function d.Mark(pid,cid)
  if pid==nil then for owner in pairs(Players)do if P.IsTestPlayer(owner)then d.Mark(owner,cid)end end;return end
  if not P.IsTestPlayer(pid) or isolated(pid)then return end
  dirty[pid]=dirty[pid] or {cities={}}
  if cid==nil then dirty[pid].all=true else dirty[pid].cities[cid]=true end
 end
 function d.Audit(scope)
  -- Real gameplay events/publications can initialize after a missed UI load event.
  if scope and scope.player~=nil and (not P.IsTestPlayer(scope.player) or isolated(scope.player))then return end
  if d.busy then
   if scope and scope.changed then for cid in pairs(scope.changed)do d.Mark(scope.player,cid)end
   else d.Mark(scope and scope.player,scope and scope.city)end
   return
  end
  d.busy=true;d.error=nil;d.failure=nil
  local phase='DEFINITION_VALIDATION';local failureOwner,failureCity
  local good,why=pcall(function()
   validate()
   if not initialized then
    -- Preserve current owned installed values until reliable topology/source facts.
    -- Foreign exact-owned cleanup remains separate from this cold-load continuity.
    for owner,player in pairs(Players)do
     phase='INITIAL_CITY_COLLECTION';failureOwner=owner;failureCity=nil
     local cities=player:GetCities()
     if cities then for _,c in cities:Members()do
      failureCity=c:GetID()
      if not P.IsTestPlayer(owner)then clear(c)
      else
       local success,err=pcall(function()
        local r={owner=owner,id=c:GetID(),x=c:GetX(),y=c:GetY(),reference=ref(c),n=0,sources={},contributors={},contributions={},provenance={},loaded=true}
        for _,row in ipairs(definitions)do
         local has=P.HasBuilding(c:GetBuildings(),row.id);assert(type(has)=='boolean','CN_PRESENCE_UNKNOWN')
         if has then assert(not r.kind or r.kind==row.kind,'CN_MULTIPLE_INSTALLED_KINDS');r.kind=row.kind;r.n=r.n+2^row.bit end
        end
        d.records[key(owner,c:GetID())]=r
       end)
       if not success then d.errors[key(owner,c:GetID())]=tostring(err)end
      end
     end end
    end
    initialized=true;d.ready=true
   end
   for pid,player in pairs(Players)do if P.IsTestPlayer(pid) and not isolated(pid) and (not scope or scope.player==nil or pid==scope.player)then
    phase='PLAYER_RECONCILIATION';failureOwner=pid;failureCity=nil
    local changed=scope and (scope.changed or scope.city~=nil and {[scope.city]=true})
    local affected={};local indexed=true
    if changed then for source,isChanged in pairs(changed)do if isChanged then
     affected[source]=true;local prior=dependents.Dependents(pid,source)
     if prior then for cid in pairs(prior)do affected[cid]=true end else indexed=false end
    end end end
    local batch={facts={},sources={},selection=changed and indexed and {sources=changed,targets=affected}or nil}
    local viewOk,view=pcall(network,batch,pid);if not viewOk then batch.networkFailed=tostring(view)end;local ids={}
    d.playerError=d.playerError or {};d.playerError[pid]=not viewOk and tostring(view):sub(1,180) or nil
    if changed and indexed and viewOk and view.scoped==true then
     for cid in pairs(view.candidates)do
      if d.records[key(pid,cid)]or view.recipients[cid]or scope.city==cid then ids[cid]=true end
     end
     -- Candidate discovery is already old dependencies + new topology + self.
     for cid in pairs(ids)do affected[cid]=true end
    else
     -- Cold, owner-wide, unavailable-index and old-adapter compatibility path.
     if viewOk then for cid in pairs(view.recipients)do ids[cid]=true end end
     for _,r in pairs(d.records)do if r.owner==pid then ids[r.id]=true end end
     if scope and scope.city~=nil then ids[scope.city]=true end
     if changed and viewOk and indexed then
      for cid,sources in pairs(view.recipients)do for source in pairs(sources)do if changed[source]then affected[cid]=true;break end end end
     end
    end
    for cid in pairs(ids)do
     local old=d.records[key(pid,cid)];local visit=not changed or affected[cid]
     if changed and not indexed then
      for src in pairs(viewOk and view.recipients[cid] or {})do if changed[src]then visit=true end end
      for src in pairs(old and old.sources or {})do if changed[src]then visit=true end end
     end
     if visit then
      local c=player:GetCities():FindID(cid);local k=key(pid,cid)
      if c and c:GetOwner()==pid then
       local previous=old and old.diagnosticSignature
       local ok,err=pcall(reconcile,batch,pid,c);if not ok then d.errors[k]=tostring(err):sub(1,180)end
       if observe then pcall(observe,pid,c,previous)end
      else d.records[k]=nil;dependents.Remove(pid,cid);d.errors[k]=nil;forgetSource(pid,cid)end
     end
    end
    health(pid,not viewOk and diagnosticCode(view) or 'CN_READY')
   end end
  end)
  d.error=not good and tostring(why):sub(1,180) or nil;d.busy=false
  if not good then
   d.failure=SPCExpeditionTrainingDiagnostics.Failure(why,phase)
   d.failure.owner=failureOwner;d.failure.city=failureCity
   health(scope and scope.player,d.failure.errorCode,d.failure)
  end
 end
 -- The successful Insight writer actively calls this in the same event.
 -- History is an effect input, not a topology signature: update dependent cities
 -- directly, or request the outstanding route proof and let recovery notify us.
 function d.SourceChanged(pid,cid)
  if not P.IsTestPlayer(pid) or isolated(pid)then return end
  d.Audit({player=pid,changed={[cid]=true}})
  local bridge=shared.NetworkBridge
  if bridge and bridge.RequestPendingProof then bridge.RequestPendingProof(pid)end
 end
 local function flush()
  if d.busy then return end
  local todo=dirty;dirty={}
  for pid,v in pairs(todo)do d.Audit({player=pid,changed=not v.all and v.cities or nil})end
 end
 -- Retained observation/report only; never Refresh or gameplay writes.
 local function pendingReport(pid,c,p,err,workerError,quiet)
  local bridge=shared.NetworkBridge;local b=bridge and bridge.players and bridge.players[pid]
  local layer=not d.ready and 'MODULE' or d.errors[key(pid,c:GetID())] and 'CITY' or d.error and 'MODULE'
   or d.playerError and d.playerError[pid] and 'NETWORK'
   or not p and 'NO_RECORD' or 'CURRENT_FACTS'
  local failure=d.failure or SPCExpeditionTrainingDiagnostics.Failure(err or workerError,
   layer=='CITY' and 'CITY_RECONCILIATION' or layer=='NETWORK' and 'NETWORK_INPUT' or 'REPORT_FACTS')
  local reason=err and failure.errorCode or not d.ready and 'CN_NOT_READY' or diagnosticCode(workerError or 'CN_REPORT_PENDING')
  local fields={'kind=NETWORK_WAIT','owner='..pid,'city='..c:GetID(),
   'layer='..layer,'reason='..reason,'phase='..failure.phase,'errorClass='..failure.errorClass,
   'errorFile='..failure.errorFile,'errorLine='..tostring(failure.errorLine or 'NONE'),'ready='..tostring(d.ready),
   'bridgeReady='..tostring(bridge and bridge.ready==true)}
  if not quiet then print('[SPC][B191][N1_INSIGHT] '..table.concat(fields,' '))end
  fields={'kind=NETWORK_INPUT','owner='..pid,'city='..c:GetID()}
  for _,k in ipairs({'validity','availability','inputRevision','derivedFor','revalidation','error'})do
   fields[#fields+1]=k..'='..diagnosticCode(b and b[k])
  end
  if not quiet then print('[SPC][B191][N1_INSIGHT] '..table.concat(fields,' '))end
  -- One replaceable signature, no per-city history. Existing ring/budget only.
  local signature=pid..':'..c:GetID()..':'..layer..':'..reason..':'..tostring(d.ready)..':'..tostring(bridge and bridge.ready==true)..':'..table.concat(fields,' ')
  if signature~=lastWait and trace then
   local ok=pcall(trace.Record,'NETWORK_WAIT',{owner=pid,city=c:GetID(),networkLayer=layer,
    reason=reason,ready=d.ready,bridgeReady=bridge and bridge.ready==true,
    phase=failure.phase,errorCode=failure.errorCode,errorClass=failure.errorClass,errorFile=failure.errorFile,errorLine=failure.errorLine,
    networkValidity=diagnosticCode(b and b.validity),networkAvailability=diagnosticCode(b and b.availability),
    networkInputRevision=diagnosticCode(b and b.inputRevision),networkDerivedFor=diagnosticCode(b and b.derivedFor),
    networkRevalidation=diagnosticCode(b and b.revalidation),networkError=diagnosticCode(b and b.error)})
   if ok then lastWait=signature end
  end
  local labels={CITY='城市事实或收益应用',MODULE='文化网络初始化',NETWORK='网络输入或拓扑',NO_RECORD='尚无城市计算结果',CURRENT_FACTS='当前城市或专家事实'}
  return '文化网络：等待确认｜'..labels[layer]..'（'..reason..'）\n输入：'
   ..diagnosticCode(b and b.validity)..' / '..diagnosticCode(b and b.availability)
   ..'；版本 '..diagnosticCode(b and b.inputRevision)..' → '..diagnosticCode(b and b.derivedFor)
   ..'。\n阶段：'..failure.phase..'；'..failure.errorFile..':'..tostring(failure.errorLine or '?')..'（'..failure.errorClass..'）。'
 end
 -- Observational only; no Refresh, initialization, fact rebuild or native write.
 observe=function(pid,c,previous,workers)
  local p=d.records[key(pid,c:GetID())];local b=shared.NetworkBridge and shared.NetworkBridge.players[pid]
  local err=d.errors[key(pid,c:GetID())] or d.error or d.playerError and d.playerError[pid]
  if not d.ready or not p or err then return pendingReport(pid,c,p,err,'CN_REPORT_PENDING',true)end
  local signature=table.concat({tostring(p.n),diagnosticCode(b and b.validity),diagnosticCode(b and b.availability),diagnosticCode(b and b.inputRevision),diagnosticCode(b and b.derivedFor)},':')
  if signature~=(previous or p.diagnosticSignature) or workers~=nil then
   if trace then pcall(trace.Record,'NETWORK_STATE',{owner=pid,city=c:GetID(),ready=d.ready,
    networkValidity=diagnosticCode(b and b.validity),networkAvailability=diagnosticCode(b and b.availability),
    networkInputRevision=diagnosticCode(b and b.inputRevision),networkDerivedFor=diagnosticCode(b and b.derivedFor),
    count=p.n,workers=workers,expected=workers and workers*p.n,reason='CN_PROJECTED'})end
  end
  p.diagnosticSignature=signature
 end
 function d.Describe(pid,c)
  local k=key(pid,c:GetID());local p=d.records[k];local error=d.errors[k] or d.error or d.playerError and d.playerError[pid]
  local ok,workers=pcall(function()
   assert(d.ready and p and p.reference==ref(c) and not error,'CN_REPORT_PENDING')
   if not p.plot then return 0 end
   local n=Map.GetPlotByIndex(p.plot):GetWorkerCount();assert(int(n),'CN_WORKERS_UNKNOWN');return n
  end)
  if not ok then return pendingReport(pid,c,p,error,workers)end
  pcall(observe,pid,c,nil,workers)
  lastWait=nil -- Permit a later report; the shared ring still applies its own dedup/budget.
  print('[SPC][B191][N1_INSIGHT] kind=NETWORK owner='..pid..' city='..c:GetID()..' civilizations='..p.n..' workers='..workers..' expected='..p.n*workers)
  return '文化网络｜完整文明 '..p.n..'｜本专业工作专家 '..workers..'\n每名额外 +'..p.n..' 文化；本城预期 +'..p.n*workers..' 文化。'
 end
 function d.Report(pid,c,details)
  local out={d.Describe(pid,c)}
  local bridge=shared.NetworkBridge;local b=bridge and bridge.players and bridge.players[pid]
  out[#out+1]='网络输入：'..diagnosticCode(b and b.validity)..' / '..diagnosticCode(b and b.availability)
  if details then
   local p=d.records[key(pid,c:GetID())];local lines={}
   for id,reference in pairs(p and p.sources or {})do
    local source=Players[pid]:GetCities():FindID(id)
    local title=source and source.GetName and source:GetName() or tostring(id)
    lines[#lines+1]='来源 '..title..(p.contributors[id] and '：提供完整文明' or '：当前未提供完整文明')
    if trace then pcall(trace.Record,'NETWORK_SOURCE',{owner=pid,city=c:GetID(),sourceCity=id,owned=reference~=false,
      reason=p.contributors[id] and 'CN_CONTRIBUTOR' or 'CN_NO_COMPLETE_SET'})end
   end
   table.sort(lines)
   if #lines==0 then lines[1]='本城暂无文化网络来源记录。'end
   for _,line in ipairs(lines)do out[#out+1]=line end
   out[#out+1]='完整文明需同一来源城完成三类考察；重复文明只计一次。'
   out[#out+1]='输入版本 '..diagnosticCode(b and b.inputRevision)..' / 计算版本 '..diagnosticCode(b and b.derivedFor)..'；拓扑错误 '..diagnosticCode(b and b.error)
  end
  out[#out+1]='以上为当前记录与预期配置；只读查看不会强制刷新网络。'
  return table.concat(out,'\n')
 end
 function d.ExperimentalNetworkWithdraw(pid)
  assert(isolated(pid) and not d.busy,'CN_ISOLATION_REQUIRED');validate()
  for _,c in Players[pid]:GetCities():Members()do clear(c);d.records[key(pid,c:GetID())]=nil;dependents.Remove(pid,c:GetID());d.errors[key(pid,c:GetID())]=nil end
  dirty[pid]=nil;return true
 end
 local function bind(name,fn)local e=P.Field(Events,name);if e and e.Add then e.Add(fn)end end
 bind('LoadScreenClose',function()d.Audit()end) -- duplicate notifications do not erase rebuilt effects
 bind('GameCoreEventPublishComplete',flush)
 -- D owns ordinary district/building inputs when available. The optional
 -- dependency fallback retains the original district signals, with verified scope.
 if not shared.DistrictCompleteness then
  for _,event in ipairs({'DistrictPillaged','DistrictRepaired','DistrictRemovedFromMap','DistrictBuildProgressChanged'})do
   SPCRuntimeWork.TargetHook(P,Events,event,function(scope)d.Mark(scope.player,scope.city)end)
  end
 end
 bind('CityTransfered',function()d.Mark()end)
 bind('PlayerTurnActivated',function(pid)if P.IsTestPlayer(pid)then d.Mark(pid)end end)
 -- Working specialists scale through the native carrier, not a stored/count ledger.
 store.RegisterExit('CultureNetwork',function(c,loss)
  assert(store.IsExitTarget(c,loss),'CN_EXIT_UNCONFIRMED');store.RemoveOwned(c,loss,M.Owned)
  forgetSource(loss.origin.owner,loss.origin.cityID)
  for k,p in pairs(d.records)do if p.owner==loss.origin.owner and p.x==c:GetX() and p.y==c:GetY()then d.records[k]=nil;dependents.Remove(p.owner,p.id);d.errors[k]=nil end end
  d.Mark(loss.origin.owner)
 end)
 store.RegisterReturn('CultureNetwork',function(pid,c)d.Mark(pid,c:GetID())end) -- facts commit later
 return d
end
