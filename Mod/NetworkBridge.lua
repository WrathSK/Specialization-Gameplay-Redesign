include('RuntimeWork')
include('ReverseDependencies')
-- AV2-B: one private derived view per accepted complete input; no consumer-yield cache.
include("NetworkInput")
include("ExpeditionTrainingDiagnostics")
SPCNetworkBridge={}
function SPCNetworkBridge.Start(P,shared)
 local d={ready=false,players={},proofRevisions={}};shared.NetworkBridge=d
 shared.RouteSignalRevision=0 -- compatibility projection; Bridge is the sole production writer
 function d.RegisterConsumer(name,fn)
  assert(shared.FactChanges,'NETWORK_FACT_REGISTRY_UNAVAILABLE')
  return shared.FactChanges.RegisterConsumer('NET_'..name,fn,{kinds={'NETWORK'}})
 end
 local function generation(pid)return shared.FactChanges and shared.FactChanges.Generation(pid,'NETWORK') or 0 end
 local function currentGeneration(pid,b)return (b.factGeneration or 0)==generation(pid)end
 local function isolatedForProof(pid)return shared.NetworkIsolation and shared.NetworkIsolation.Active(pid)==true end
 local notify
 local pending,dormant={},{};local draining=false
 function d.ProofRevision(pid)return d.proofRevisions[pid] or 0 end
 function d.TransactionCurrent(pid)
  local b=d.players[pid]
  return b~=nil and b.availability=='AVAILABLE' and b.revalidation=='VERIFIED'
   and b.signal==(shared.RouteSignalRevision or 0) and currentGeneration(pid,b) and not b.queuedWork and not b.negativeHeld and not isolatedForProof(pid)
 end
 ExposedMembers.SPCNetworkEpoch=(ExposedMembers.SPCNetworkEpoch or 0)+1
 d.epoch=ExposedMembers.SPCNetworkEpoch
 local function integer(n) return type(n)=="number" and n>=0 and n%1==0 and n<2147483648 end
 local function city(pid,id)
  local p=Players[pid];local c=p and p:GetCities():FindID(id)
  assert(c and c:GetOwner()==pid,"ENDPOINT_MISSING_OR_CHANGED");return c
 end
 local function short(err)
  local first=tostring(err):match("[^\r\n]+") or "UNKNOWN"
  return (first:match(":%d+: (.+)$") or first):sub(1,180)
 end
 local function isolated(pid) return shared.NetworkIsolation and shared.NetworkIsolation.Active(pid) end
 local derive
 local inputProviders={} -- one call-local service identity/turn witness per accepted owner input
 local views={} -- private, at most one view per player; never keyed by historical versions
 local reportTrace
 local traceOK,value=pcall(SPCExpeditionTrainingDiagnostics.New,P,'NETWORK_REPORT')
 if traceOK then reportTrace=value end
 local stateTrace=SPCExpeditionTrainingDiagnostics.New(P,'NETWORK_STATE')
 local function state(stage,pid,b,reason,packet)
  if stage=='NETWORK_VERIFIED' and shared.EventTiming then pcall(shared.EventTiming.Verified,pid,b)end
  pcall(function()
   -- Fixed token only; never retain raw engine errors or route payloads.
   local token=type(reason)=='string' and (reason:match('NETWORK_[A-Z0-9_]+') or reason:match(':%d+: ([A-Z][A-Z0-9_]+)') or reason:match('^([A-Z][A-Z0-9_]+)$') or reason:match('^[A-Za-z][A-Za-z0-9_]+$') and reason:upper()) or nil
   stateTrace.Record(stage,{owner=pid,reason=token or 'READ_ERROR',ready=d.ready,
    networkAvailability=b and b.availability,networkRevalidation=b and b.revalidation,
    networkInputRevision=b and b.inputRevision,networkSignal=b and b.signal,routeSignal=shared.RouteSignalRevision or 0,
    routeCount=b and b.routes and #b.routes,packetSeq=packet and packet.Seq,packetTurn=packet and packet.Turn,
    packetSignal=packet and packet.Signal,packetEpoch=packet and packet.Epoch})
  end)
 end
 local function copy(v)
  if type(v)~='table' then return v end
  local out={};for k,x in pairs(v) do out[k]=copy(x) end;return out
 end
 local function buildView(pid,rows,input)
  P.Count('derive_requested');P.Count('derived_cache_miss')
  local sources,centers,recipients=derive(pid,rows,input)
  local connected,national={},{}
  for id,set in pairs(centers) do
   connected[id]={};for src in pairs(set) do connected[id][sources[src]]=true end
  end
  for _,kind in ipairs({'RESEARCH','CULTURE'}) do
   local n={n=0,level=0,sources={},recipients={}};national[kind]=n
   for cid,set in pairs(recipients[kind] or {}) do
    for src in pairs(set) do
     local f=input.cities[src]
     if f and f.specialization==kind and type(f.active)=='number' and f.active>=1 and f.active<=4 and f.active%1==0 then
      n.sources[src]=f.active;n.recipients[cid]=true;n.level=math.max(n.level,f.active)
     end
    end
   end
   for _ in pairs(n.recipients) do n.n=n.n+1 end
  end
  -- B239 Commerce uses direct pairs, not center distribution or reachability.
  -- Keep this projection private and rebuild it only with a new verified input.
  local directDomestic,directOutgoing,references={},{},{}
  for id,f in pairs(input.cities) do references[id]=f.reference end
  for _,r in ipairs(rows) do
   if r.op==pid and r.dp==pid and r.oc~=r.dc then
    directOutgoing[r.oc]=directOutgoing[r.oc] or {};directOutgoing[r.oc][r.dc]=true
    directDomestic[r.oc]=directDomestic[r.oc] or {};directDomestic[r.oc][r.dc]=true
    directDomestic[r.dc]=directDomestic[r.dc] or {};directDomestic[r.dc][r.oc]=true
   end
  end
  -- B311: private scalar topology index, replaced with this one accepted view.
  -- Capacity failure disables only scoped copying; the complete view stays valid.
  local cultureIndex=SPCReverseDependencies.New()
  for cid,set in pairs(recipients.CULTURE or {})do if not cultureIndex.Replace(pid,cid,set)then break end end
  return {sources=sources,centers=centers,recipients=recipients,connected=connected,national=national,
   directDomestic=directDomestic,directOutgoing=directOutgoing,references=references,cultureIndex=cultureIndex}
 end
 local function bucket(pid)
  if not d.players[pid] then d.players[pid]={seq=-1,revision=0,inputRevision=0,derivedRevision=0,validity='UNKNOWN',availability='UNAVAILABLE'} end
  return d.players[pid]
 end
 -- A dirty event requests one UI resample through its existing event flush.
 -- This callback only marks work; it never scans or sends a command inline.
 local function pendingProof(pid,b,request,cause)
  local first=b.revalidation~='NEEDS_REVALIDATION'
  b.proofPending=true;b.revalidation='NEEDS_REVALIDATION';b.availability=b.input and 'NEEDS_REVALIDATION' or 'UNAVAILABLE';b.effectAvailability='PENDING'
  if first then state('NETWORK_PENDING',pid,b,cause or 'READ_OR_SIGNAL');if notify then notify(pid)end end
  if request==true or request==nil and first then
   local ui=ExposedMembers.SPC_P0_BackgroundRoutes
   if ui and type(ui.RequestRevalidation)=='function' then pcall(ui.RequestRevalidation,d.epoch,pid) end
  end
 end
 function d.RequestPendingProof(pid)
  if isolated(pid) or not d.ready or not P.IsTestPlayer(pid) then return end
  local b=d.players[pid]
  if b and b.revalidation=='NEEDS_REVALIDATION' then pendingProof(pid,b,true) end
 end
 -- Metadata is a value copy. Input revision belongs to this Gameplay epoch, not the save.
 function d.Input(pid)
  local b=bucket(pid)
  return {contract=1,epoch=d.epoch,player=pid,inputVersion=b.inputRevision,signature=b.inputSignature,
   validity=b.validity,availability=(b.queuedWork or b.negativeHeld) and 'NEEDS_REVALIDATION' or b.availability,routeRevision=b.revision,routeValidity=b.routes and 'VERIFIED' or b.validity,revalidation=b.revalidation,
   derivedRevision=b.derivedRevision,derivedFor=b.derivedFor,withdrawal=b.withdrawal==true,transportFailure=b.transportFailure,
   factAvailability=b.input and b.input.factAvailability or 'UNKNOWN',provenance=b.input and copy(b.input.provenance),
   effectAvailability=(b.queuedWork or b.negativeHeld) and 'PENDING' or b.effectAvailability,continuityOnly=b.continuityOnly==true}
 end
 local function proofSignature(b)
  local parts={tostring(b.inputRevision),tostring(b.validity),tostring(b.withdrawal),tostring(b.availability),tostring(b.effectAvailability),tostring(b.revalidation),
   tostring(b.signal),tostring(shared.RouteSignalRevision or 0),tostring(b.transportFailure),tostring(b.continuityOnly),tostring(b.factGeneration or 0),tostring(b.queuedWork==true),tostring(b.negativeHeld==true)}
  local ids={};for id in pairs(b.input and b.input.provenance or {})do ids[#ids+1]=id end;table.sort(ids)
  for _,id in ipairs(ids)do local f=b.input.provenance[id];parts[#parts+1]=id..':'..f.reference..':'..f.status end
  return table.concat(parts,'|')
 end
 notify=function(pid)
  local b=bucket(pid);local signature=proofSignature(b)
  if b.lastNotifiedProof==signature then return false end
  b.lastNotifiedProof=signature;if b.effectAvailability=='AVAILABLE'then b.proofPending=false end
  d.proofRevisions[pid]=(d.proofRevisions[pid] or 0)+1
  if shared.FactChanges then
   local ok,err=pcall(shared.FactChanges.EmitDerived,{owner=pid,kinds={'NETWORK'},cause='NETWORK_PROOF_PUBLISHED',revision=d.proofRevisions[pid],
    evidence={epoch=d.epoch,inputVersion=b.inputRevision,proofRevision=d.proofRevisions[pid],validity=b.validity,
     availability=(b.queuedWork or b.negativeHeld) and 'NEEDS_REVALIDATION' or b.availability,effectAvailability=(b.queuedWork or b.negativeHeld) and 'PENDING' or b.effectAvailability,revalidation=b.revalidation,continuityOnly=b.continuityOnly==true}})
   b.consumerError=not ok and short(err) or nil
  end
  return true
 end
 local function mergeWork(dst,src)
  dst.losses=dst.losses or {};dst.drops=dst.drops or {}
  for id,refs in pairs(src.losses or {})do dst.losses[id]=dst.losses[id] or {};for ref in pairs(refs)do dst.losses[id][ref]=true end end
  for ref in pairs(src.drops or {})do dst.drops[ref]=true end
  local n=0;for _,refs in pairs(dst.losses)do for _ in pairs(refs)do n=n+1 end end;for _ in pairs(dst.drops)do n=n+1 end
  assert(n<=2048,'NETWORK_PENDING_NEGATIVE_LIMIT')
  if src.packet and (not dst.packet or src.packet.Seq>dst.packet.Seq)then dst.packet=src.packet end
  dst.refresh=dst.refresh or src.refresh
  if src.evidence=='NATIVE' or dst.evidence~='NATIVE'then dst.evidence=src.evidence or dst.evidence end
  return dst
 end
 -- Only real reentrant causes arm this scalar work. UNKNOWN/idle publication never does.
 local function enqueue(pid,kind,value)
  local q=pending[pid]
  if not q then
   local n=0;for _ in pairs(pending)do n=n+1 end;assert(n<2048,'NETWORK_PENDING_OWNER_LIMIT')
   q={losses={},drops={},version=0};pending[pid]=q
  end
  if dormant[pid]then mergeWork(q,dormant[pid]);dormant[pid]=nil end
  if kind=='packet'then
   if not q.packet or value.Seq>q.packet.Seq then q.packet=value end
  elseif kind=='loss'then
   assert(integer(value.city) and type(value.reference)=='string' and #value.reference<=512,'NETWORK_PENDING_LOSS_SHAPE')
   mergeWork(q,{losses={[value.city]={[value.reference]=true}}})
  elseif kind=='negative'then mergeWork(q,value)
  elseif kind=='evidence'then if value=='NATIVE' or q.evidence~='NATIVE'then q.evidence=value end
  else q[kind]=true end
  q.version=q.version+1
  local b=bucket(pid);b.queuedWork=true;notify(pid);return q
 end
 local function wire(p)
  local out={}
  for _,key in ipairs({'Epoch','Seq','Turn','Signal','Valid','Count','WireCount'})do
   local v=p[key];assert(v==nil or type(v)=='number','NETWORK_BUSY_PACKET_SHAPE');out[key]=v
  end
  for key,limit in pairs({Failure=64,Data=16384})do
   local v=p[key];assert(v==nil or type(v)=='string' and #v<=limit,'NETWORK_BUSY_PACKET_LIMIT');out[key]=v
  end
  return out
 end
 local function publish(pid,b,input,view,withdrawal)
  if b.inputSignature==input.signature then P.Count('input_duplicate');return false end
  b.inputRevision=b.inputRevision+1;b.inputSignature=input.signature;b.input=input
  b.validity=input.validity;b.withdrawal=withdrawal==true
  if views[pid] then P.Count('derived_invalidation') end
  views[pid]=view
  if view then
   view.contract=1;view.epoch=d.epoch;view.player=pid;view.inputVersion=b.inputRevision
   view.derivedFor=b.inputRevision;view.validity='VERIFIED';view.signature=input.signature
  end
  -- Compatibility/debug projections must not expose the private cache to mutation.
  b.sources=view and copy(view.sources);b.centers=view and copy(view.centers);b.recipients=view and copy(view.recipients)
  if input.validity=='VERIFIED' then b.derivedRevision=b.derivedRevision+1;b.derivedFor=b.inputRevision
  else b.derivedFor=nil end
  P.Count('fact_change');P.Count('input_version_change');P.Count('input_publication')
  if withdrawal then P.Count('withdrawal') end
  notify(pid);return true
 end
 local function withdraw(pid,b,reason)
  if isolated(pid) then return false end
  if b.validity=='CONFIRMED_INVALID' and not b.routes then return false end
  b.routes=nil;b.fingerprint=nil;b.routeReferences=nil;b.candidate=nil;b.transportFailure=nil;b.reason='CONFIRMED_INVALID';b.error=reason
  b.revalidation='CONFIRMED_INVALID';b.availability='UNAVAILABLE';b.revision=b.revision+1
  P.Count('confirmed_invalid')
  local input={validity='CONFIRMED_INVALID',routeSignature='',cities={}}
  input.signature=SPCNetworkInput.Signature(input)
  local perf=ExposedMembers.SPC_Performance;if perf then perf.revision=b.revision;perf.routes=0 end
  return publish(pid,b,input,nil,true)
 end
 local function prune(pid,b,lost,rows,reason)
  if not b.input or b.input.validity~='VERIFIED' then return false end
  local input=copy(b.input);local changed=false
  for id in pairs(lost or {})do if input.cities[id]then input.cities[id]=nil;input.provenance[id]=nil;changed=true end end
  if input.capital and not input.cities[input.capital]then input.capital=nil end
  local kept={};for _,r in ipairs(rows or b.routes or {})do
   if not (r.op==pid and lost and lost[r.oc] or r.dp==pid and lost and lost[r.dc])then kept[#kept+1]=r end
  end
  if #kept~=#(b.routes or {})then changed=true end
  if not changed then return false end
  input.routeSignature=input.routeSignature..':NEGATIVE:'..tostring(b.inputRevision+1)
  input.pending=true;input.factAvailability='MIXED';input.negativeProof=true
  for id,f in pairs(input.cities)do
   f.provenance=f.provenance=='UNKNOWN' and 'UNKNOWN' or 'RETAINED'
   input.provenance[id]={reference=f.reference,status=f.provenance,reason='NETWORK_LAST_PROVEN_TOPOLOGY'}
  end
  input.signature=SPCNetworkInput.Signature(input)
  local ok,view=pcall(buildView,pid,kept,input);if not ok then b.error=short(view);return false end
  b.routes=kept;b.candidate=nil;b.continuityOnly=true;b.effectAvailability='RETAINED_NEGATIVE'
  b.revalidation='NEEDS_REVALIDATION';b.availability='NEEDS_REVALIDATION';b.error=reason
  return publish(pid,b,input,view,true)
 end
 local function routeKey(b,r)
  local refs=b.routeReferences and b.routeReferences[r.trader] or {}
  local origin,destination=tostring(refs.origin),tostring(refs.destination)
  return table.concat({r.op,r.oc,r.dp,r.dc,r.trader,#origin,origin,#destination,destination},':')
 end
 local function losses(pid,q)
  local b=bucket(pid);local lost={};local work={losses=q.losses,drops=q.drops};local ticket=q.version
  q.losses={};q.drops={}
  for id,refs in pairs(work.losses)do local f=b.input and b.input.cities[id];if f and refs[f.reference]then lost[id]=true end end
  local kept={};local dropped=false
  for _,r in ipairs(b.routes or {})do if work.drops[routeKey(b,r)]then dropped=true else kept[#kept+1]=r end end
  if next(lost) or dropped then
   b.refreshing=true;local ok,err=pcall(prune,pid,b,lost,dropped and kept or nil,'CONFIRMED_LOSS_DEFERRED');b.refreshing=false
   local remaining=false
   for id in pairs(lost)do if b.input and b.input.cities[id] and work.losses[id][b.input.cities[id].reference]then remaining=true end end
   for _,r in ipairs(b.routes or {})do if work.drops[routeKey(b,r)]then remaining=true end end
   if not ok or remaining then
    mergeWork(q,work);dormant[pid]=q;b.negativeHeld=true
    b.operationError=not ok and short(err) or b.error or 'NETWORK_NEGATIVE_PROJECTION_UNCONFIRMED'
    if pending[pid]==q and q.version==ticket then pending[pid]=nil
    elseif pending[pid]then mergeWork(pending[pid],q);dormant[pid]=nil end
    return false
   end
  end
  b.negativeHeld=nil;dormant[pid]=nil;return true
 end
 -- Concrete native evidence only. Unknown getters preserve the accepted snapshot.
 function d.Verified(pid,failedFullRead)
  if isolated(pid) then return false end
  local b=d.players[pid];if not b or not b.routes then return false end
  if b.refreshing then return true end
  local lost,kept={},{};local uncertain=false
  for _,r in ipairs(b.routes)do
   local ok,invalid=pcall(function()
    local op,dp=Players[r.op],Players[r.dp]
    if not op or not dp then return true end
    local o,z=op:GetCities():FindID(r.oc),dp:GetCities():FindID(r.dc)
    if o then assert(type(o:GetOwner())=='number','NETWORK_OWNER_UNKNOWN')end
    if z then assert(type(z:GetOwner())=='number','NETWORK_OWNER_UNKNOWN')end
    if not o or o:GetOwner()~=r.op then if r.op==pid then lost[r.oc]=true end;return true end
    if not z or z:GetOwner()~=r.dp then if r.dp==pid then lost[r.dc]=true end;return true end
    local refs=b.routeReferences and b.routeReferences[r.trader]
    if refs and SPCNetworkInput.Reference(o)~=refs.origin then if r.op==pid then lost[r.oc]=true end;return true end
    if refs and SPCNetworkInput.Reference(z)~=refs.destination then if r.dp==pid then lost[r.dc]=true end;return true end
    local known,u=pcall(function()return op:GetUnits():FindID(r.trader)end)
    if known and not u then return true end
    if r.op~=r.dp then local read,war=pcall(function()return op:GetDiplomacy():IsAtWarWith(r.dp)end);if read and war==true then return true end end
    return false
   end)
   if ok and invalid then else kept[#kept+1]=r;if not ok then uncertain=true end end
  end
  -- A count drop alone does not identify which route disappeared. Hold and request
  -- a complete sample; never erase unrelated routes by guessing from the delta.
  if #kept<#b.routes then
   local negative={losses={},drops={}};local present={}
   for _,r in ipairs(kept)do present[routeKey(b,r)]=true end
   for _,r in ipairs(b.routes)do local key=routeKey(b,r);if not present[key]then negative.drops[key]=true end end
   for id in pairs(lost)do local f=b.input and b.input.cities[id];if f then negative.losses[id]={[f.reference]=true}end end
   local q=enqueue(pid,'negative',negative);losses(pid,q)
   if uncertain then pendingProof(pid,b,not failedFullRead)end
   return true,true -- native negative attempt made; no second urgent attempt in this call

  end
  if uncertain then pendingProof(pid,b,not failedFullRead)end
  return true
 end
 -- Capture a coherent complete input before changing any officially published input.
 local function refresh(pid,incremental)
  if isolated(pid) then return false end
  if not P.IsTestPlayer(pid) or not d.ready then return false end
  local b=bucket(pid)
  if b.refreshing then P.Count('busy_skip');return false end
  if not b.candidate and not d.Verified(pid) then return false end
  b.refreshing=true
  local sampledGeneration=generation(pid)
  local candidate=b.candidate
  if candidate and (candidate.turn~=Game.GetCurrentGameTurn() or candidate.signal~=(shared.RouteSignalRevision or 0)) then
   b.candidate=nil;candidate=nil;P.Count('stale_input')
  end
  if not candidate and not b.routes then b.refreshing=false;return false end
  local rows=candidate and candidate.routes or b.routes
  local fingerprint=candidate and candidate.fingerprint or b.fingerprint
  local registry=shared.FactChanges;local provider=registry
  if not (provider and type(provider.NetworkCityGeneration)=='function')then provider=nil end
  local effective,store=shared.EffectiveFacts,shared.CityProgressionStore
  local reader=effective and effective.Read
  local prior=inputProviders[pid];local now
  local baseReader=store and store.Base;local stampReader=store and store.FactStamp
  local ok,input=pcall(function()
   now=Game.GetCurrentGameTurn()
   local sampling=provider and {provider=provider,reuse=incremental==true and not candidate and prior~=nil
    and prior.registry==provider and prior.effective==effective and prior.reader==reader
    and prior.store==store and prior.base==baseReader and prior.stamp==stampReader and prior.turn==now}
   if candidate then assert(Players[pid]:GetTrade():CountOutgoingRoutes()==#rows,'NETWORK_CANDIDATE_COUNT_CHANGED') end
   local result=SPCNetworkInput.Capture(P,shared,pid,rows,fingerprint,b.input,sampling)
   assert(shared.FactChanges==registry and shared.EffectiveFacts==effective and effective.Read==reader
    and shared.CityProgressionStore==store and (store and store.Base)==baseReader
    and (store and store.FactStamp)==stampReader
    and Game.GetCurrentGameTurn()==now,'NETWORK_INPUT_SERVICE_CHANGED')
   return result
  end)
  local changed=false
  if ok then
   local duplicate=b.inputSignature==input.signature
   local good,view=true,nil
   if not duplicate then good,view=pcall(buildView,pid,rows,input) end
   if good then
    local withdrawal=false
    if not duplicate then
     withdrawal=b.input and b.input.capital~=nil and b.input.capital~=input.capital or false
     if candidate and b.routes then
      local present={};for _,route in ipairs(rows) do present[route.trader..':'..route.oc..':'..route.dp..':'..route.dc]=true end
      for _,route in ipairs(b.routes) do
       if not present[route.trader..':'..route.oc..':'..route.dp..':'..route.dc] then withdrawal=true end
      end
     end
     for id,old in pairs(b.input and b.input.cities or {}) do
      local new=input.cities[id]
      if old.potential>=1 and (not new or new.reference~=old.reference or new.specialization~=old.specialization
       or new.active<old.active or new.potential<1) then withdrawal=true end
     end
    end
    if candidate then
     if b.fingerprint~=fingerprint or not b.routes then b.revision=b.revision+1;P.Count('publication') end
     b.routes=rows;b.routeReferences=candidate.references;b.fingerprint=fingerprint
     b.turn=candidate.turn;b.signal=candidate.signal;b.reason='READY_BACKGROUND_UI';b.revalidation='VERIFIED'
     b.acceptedSeq=candidate.seq;b.candidate=nil;b.transportFailure=nil -- receipt, distinct from merely seen/rejected seq
     local perf=ExposedMembers.SPC_Performance;if perf then perf.revision=b.revision;perf.routes=#rows end
    end
    -- Commit current proof BEFORE exposing availability or notifying a consumer.
    -- A proved route set does not resolve unreadable city facts.
    inputProviders[pid]={registry=provider,effective=effective,reader=reader,store=store,base=store and store.Base,stamp=store and store.FactStamp,turn=now}
    b.factGeneration=sampledGeneration
    b.continuityOnly=not candidate and b.continuityOnly==true or withdrawal and (input.roleUnknown or b.revalidation=='NEEDS_REVALIDATION') or false
    local fresh=b.revalidation=='VERIFIED' and b.signal==(shared.RouteSignalRevision or 0) and currentGeneration(pid,b)
    b.effectAvailability=b.continuityOnly and 'RETAINED_NEGATIVE' or fresh and not input.roleUnknown and 'AVAILABLE' or 'PENDING'
    b.availability=(input.pending or not fresh) and 'NEEDS_REVALIDATION' or 'AVAILABLE';b.error=b.transportFailure
    if duplicate then
     b.input=input;P.Count('input_duplicate')
     notify(pid)
    else changed=publish(pid,b,input,view,withdrawal) end
   if b.availability=='AVAILABLE' and b.revalidation=='VERIFIED'then state('NETWORK_VERIFIED',pid,b,'SAMPLE_ACCEPTED')end
   else b.availability='NEEDS_REVALIDATION';b.effectAvailability=b.continuityOnly and 'RETAINED_NEGATIVE' or 'PENDING';b.error=short(view);state('NETWORK_SAMPLE_FAILED',pid,b,b.error)end
  else
   b.availability=b.input and 'NEEDS_REVALIDATION' or 'UNAVAILABLE';b.effectAvailability=b.continuityOnly and 'RETAINED_NEGATIVE' or 'PENDING';b.error=short(input)
   state('NETWORK_SAMPLE_FAILED',pid,b,b.error)
   -- A failed new sample cannot hide independently confirmed loss of an old input.
   local lost,rows={},b.routes
   for id,old in pairs(b.input and b.input.cities or {})do
    pcall(function()
     local c=Players[pid]:GetCities():FindID(id)
     if c then assert(type(c:GetOwner())=='number','NETWORK_OWNER_UNKNOWN')end
     if not c or c:GetOwner()~=pid then lost[id]=true
     else local good,reference=pcall(SPCNetworkInput.Reference,c);if good and reference~=old.reference then lost[id]=true end end
    end)
   end
   if candidate and b.routes then
    local current={};for _,r in ipairs(candidate.routes)do current[r.trader..':'..r.oc..':'..r.dp..':'..r.dc]=true end
    rows={};for _,r in ipairs(b.routes)do if current[r.trader..':'..r.oc..':'..r.dp..':'..r.dc]then rows[#rows+1]=r end end
   end
   changed=prune(pid,b,lost,rows,'CONFIRMED_INPUT_LOSS_WHILE_SAMPLE_PENDING')
  end
  notify(pid);b.refreshing=false;return changed
 end
 function d.Refresh(pid,fromReceive,incremental)
  local b=d.players[pid]
  if b and (b.refreshing or b.receiving and not fromReceive)then P.Count('busy_skip');enqueue(pid,'refresh');return false end
  if dormant[pid]then enqueue(pid,'refresh')end
  local ok,value=pcall(refresh,pid,incremental)
  b=d.players[pid];if b then b.refreshing=false end
  -- One bounded urgent negative catch-up; no positive resample or recursive retry loop.
  local q=pending[pid]
  if b and q then
   local attempted=false
   if q.evidence then
    local evidence=q.evidence;q.evidence=nil
    pendingProof(pid,b,evidence=='NATIVE','DEFERRED_NATIVE_EVIDENCE')
    local good,_,projected=pcall(d.Verified,pid,evidence=='FAILED');b.refreshing=false
    attempted=good and projected==true
    if not good then b.operationError='NETWORK_DEFERRED_VERIFICATION_FAILED' end
   end
   q=pending[pid]
   if q and not attempted and (next(q.losses) or next(q.drops))then losses(pid,q)end
   q=pending[pid]
   if q and not q.packet and not q.refresh and not q.evidence and not next(q.losses) and not next(q.drops)then pending[pid]=nil end
   b.queuedWork=pending[pid]~=nil;notify(pid)
  end
  if not ok then if b then b.operationError=short(value)end;error(value,0)end
  return value
 end
 -- Only the declared role-fact binding opts in. Every other entry stays full.
 function d.RefreshFacts(pid)return d.Refresh(pid,false,true)end
 local function receiveImpl(pid,p,deferred)

  if isolated(pid) then state('NETWORK_RECEIVE_DROP',pid,nil,'ISOLATED',p);return end -- includes delayed pre-experiment packets
  if not deferred then P.Count('net_receive')end
  if not P.IsTestPlayer(pid) or p.Epoch~=d.epoch or not integer(p.Seq) then P.Count('stale_input');state('NETWORK_RECEIVE_DROP',pid,nil,'OWNER_EPOCH_OR_SEQUENCE',p);return end
  local b=bucket(pid)
  if b.refreshing or b.receiving then
   if p.Seq<=b.seq then P.Count('send_duplicate');P.Count('stale_input');return end
   local ok,value=pcall(wire,p)
   if ok then enqueue(pid,'packet',value)else P.Count('stale_input');state('NETWORK_RECEIVE_DROP',pid,b,'BUSY_PACKET_REJECT',p)end
   P.Count('busy_skip');return -- seq/acceptedSeq are untouched until the normal processing path
  end
  if p.Seq<=b.seq then P.Count('send_duplicate');P.Count('stale_input');state('NETWORK_RECEIVE_DROP',pid,b,'REPLAY',p);return end
  b.receiving=true
  b.seq=p.Seq;b.candidate=nil -- a newer packet supersedes any unpublished older candidate
  local ok,err=pcall(function()
   assert(d.ready,'LOAD_NOT_READY')
   assert(p.Turn==Game.GetCurrentGameTurn() and p.Signal==(shared.RouteSignalRevision or 0),'STALE_SIGNAL_OR_TURN')
   if p.Valid~=1 then
    local prior=b.availability
    pendingProof(pid,b,false)
    -- A complete collector sample that exceeds transport bounds is UNKNOWN,
    -- never an empty/partial route publication. Preserve the last accepted view.
    if p.Failure=='NETWORK_ROUTE_LIMIT' or p.Failure=='NETWORK_PAYLOAD_LIMIT' then
     local changed=b.transportFailure~=p.Failure
     b.transportFailure=p.Failure;b.error=p.Failure
     if changed or prior~=b.availability then notify(pid) end
    end
    return
   end
   local count=p.Count
   if p.WireCount~=nil then
    assert(integer(p.WireCount) and p.WireCount>=1 and p.WireCount<=129,'WIRE_COUNT_INVALID')
    count=p.WireCount-1;assert(p.Count==nil or p.Count==count,'WIRE_COUNT_CONFLICT')
   end
   assert(integer(count) and count<=128,'ROUTE_COUNT_INVALID')
   local data=p.Data;if count==0 and data=='EMPTY' then data='' end
   assert(type(data)=='string' and #data<=16384,'ROUTE_DATA_INVALID')
   local rows,seen,keys={},{},{}
   for line in data:gmatch('[^;]+') do
    local a,o,c,z,u=line:match('^(%d+),(%d+),(%d+),(%d+),(%d+)$')
    assert(a,'ROW_FORMAT');a,o,c,z,u=tonumber(a),tonumber(o),tonumber(c),tonumber(z),tonumber(u)
    for _,v in ipairs({a,o,c,z,u}) do assert(integer(v),'ROW_RANGE') end
    assert(a==pid and not seen[u],'ORIGIN_OR_DUPLICATE_TRADER');seen[u]=true
    city(a,o);city(c,z)
    local known,unit=pcall(function() return Players[a]:GetUnits():FindID(u) end)
    assert(not known or unit,'CURRENT_TRADER_MISSING')
    rows[#rows+1]={op=a,oc=o,dp=c,dc=z,trader=u}
    keys[#keys+1]=a..':'..u..'|'..a..':'..o..'>'..c..':'..z
   end
   assert(#rows==count,'PARTIAL_BATCH')
   assert(Players[pid]:GetTrade():CountOutgoingRoutes()==count,'CURRENT_COUNT_CHANGED')
   table.sort(keys);local fingerprint=table.concat(keys,'\n')
   if b.routes and b.fingerprint==fingerprint then
    P.Count('same_snapshot');P.Count('revalidate_same')
   end
   local references={}
   for _,r in ipairs(rows) do references[r.trader]={origin=SPCNetworkInput.Reference(city(r.op,r.oc)),destination=SPCNetworkInput.Reference(city(r.dp,r.dc))} end
   b.candidate={routes=rows,references=references,fingerprint=fingerprint,turn=p.Turn,signal=p.Signal,seq=p.Seq}
  end)
  if not ok then pendingProof(pid,b,false,'RECEIVE_REJECT');b.error=short(err);state('NETWORK_RECEIVE_REJECT',pid,b,b.error,p);P.Count('route_failure');P.Count('stale_input')end
  if ok and p.Valid==1 then d.Refresh(pid,true) else d.Verified(pid) end
 end
 local function receive(pid,p,deferred)
  local b=d.players[pid];local nested=b and b.receiving
  local ok,err=pcall(receiveImpl,pid,p,deferred)
  b=d.players[pid];if b and not nested then b.receiving=false end
  if not ok then if b then b.operationError=short(err)end;error(err,0)end
 end
 function d.Receive(pid,p)return receive(pid,p,false)end
 function d.FlushPending()
  if draining or not next(pending)then return false end;draining=true
  local work=pending;pending={}
  for pid,q in pairs(work)do
   local b=bucket(pid)
   if b.refreshing or b.receiving then
    local fresh=pending[pid]
    if not fresh then pending[pid]=q
    else
     mergeWork(fresh,q)
    end
   else
    local ok,err=pcall(function()
     if not losses(pid,q)then return end
     if q.evidence then pendingProof(pid,b,q.evidence=='NATIVE','DEFERRED_NATIVE_EVIDENCE');d.Verified(pid,q.evidence=='FAILED');if b.negativeHeld then mergeWork(dormant[pid],q);return end end
     if q.packet then receive(pid,q.packet,true)
     elseif q.refresh or q.evidence then d.Refresh(pid)end
    end)
    if not ok then b.operationError=short(err)end
    b.refreshing=false;b.queuedWork=pending[pid]~=nil;notify(pid)
   end
  end
  draining=false;return true
 end
 local publishEvent=P.Field(Events,'GameCoreEventPublishComplete')
 if publishEvent and publishEvent.Add then publishEvent.Add(d.FlushPending)end
 derive=function(pid,rows,input)
  P.Count("derive");P.Count("derive_executed")
  local sources,centers,recipients={},{},{}
  input=input or assert(d.players[pid].input,'NETWORK_INPUT_UNAVAILABLE')
  local capital=input.capital
  for id,f in pairs(input.cities) do
   if f.potential>=1 then
    if f.specialization=="RESEARCH" or f.specialization=="CULTURE" or f.specialization=="INDUSTRY" then sources[id]=f.specialization end
    if f.specialization=="COMMERCE" then centers[id]={} end
   end
  end
  if capital then centers[capital]=centers[capital] or {} end
  for _,r in ipairs(rows) do
   if r.dp==pid and centers[r.dc] and sources[r.oc] then centers[r.dc][r.oc]=true end
  end
  if capital and sources[capital] then centers[capital][capital]=true end
  -- D0009: direct connection grants reception, independently of distribution.
  -- Recipient keys merge direct, capital-self and outgoing-route qualifications.
  for centerID,sourceSet in pairs(centers) do
   for src in pairs(sourceSet) do
    local kind=sources[src];recipients[kind]=recipients[kind] or {}
    local set=recipients[kind];set[centerID]=set[centerID] or {};set[centerID][src]=true
   end
  end
  for _,r in ipairs(rows) do
   if r.dp==pid and centers[r.oc] then
    for src in pairs(centers[r.oc]) do
     local kind=sources[src];recipients[kind]=recipients[kind] or {}
     local set=recipients[kind];set[r.dc]=set[r.dc] or {};set[r.dc][src]=true
    end
   end
  end
  return sources,centers,recipients
 end
 -- Refresh remains the Batch A fact boundary (its scans are not cached in Batch B).
 local function currentView(pid,confirmedOnly)
  assert(not isolated(pid),'NETWORK_EXPERIMENT_ISOLATED')
  P.Count('derive_requested')
  if not confirmedOnly then d.Refresh(pid) end
  local b=d.players[pid]
  assert(b and b.input and b.validity=='VERIFIED' and (confirmedOnly or d.Verified(pid)),'NETWORK_REFRESH_PENDING')
  assert(currentGeneration(pid,b),'NETWORK_FACTS_PENDING')
  local v=views[pid]
  local matches=v and v.contract==1 and v.epoch==d.epoch and v.player==pid
   and v.validity=='VERIFIED' and v.inputVersion==b.inputRevision and v.derivedFor==b.inputRevision
   and b.derivedFor==b.inputRevision and v.signature==b.inputSignature
  if not matches then P.Count('derived_cache_miss');error('NETWORK_DERIVED_VIEW_UNAVAILABLE') end
  P.Count('derived_cache_hit');return v
 end
 -- D1: one synchronous consumer batch, copied projection; never retain across batches.
 -- Performs the complete A/B confirmation once, not once per recipient query.
 function d.DiscountBatch(pid)
  assert(d.ready and P.IsTestPlayer(pid),'NETWORK_NOT_READY_OR_OWNER')
  local v=currentView(pid)
  return {input=d.Input(pid),recipients=copy(v.recipients.INDUSTRY or {})}
 end
 -- B226: one private-view read/copy per Culture consumer batch. No Refresh,
 -- all-city fact collection, public mutable bucket or received-payload recursion.
 function d.CurrentIndustryBatch(pid)
  assert(d.ready and P.IsTestPlayer(pid),'NETWORK_NOT_READY_OR_OWNER')
  local v=currentView(pid,true)
  return {input=d.Input(pid),recipients=copy(v.recipients.INDUSTRY or {})}
 end
 function d.CurrentCultureBatch(pid,selection)
  assert(d.ready and P.IsTestPlayer(pid),'NETWORK_NOT_READY_OR_OWNER')
  local v=currentView(pid,true);local rows=v.recipients.CULTURE or {}
  if type(selection)=='table'and type(selection.sources)=='table'and type(selection.targets)=='table'then
   local candidates={};local scoped=true
   for cid,selected in pairs(selection.targets)do if selected then candidates[cid]=true end end
   for source,changed in pairs(selection.sources)do if changed then
    local targets=v.cultureIndex.Dependents(pid,source)
    if not targets then scoped=false;break end
    for cid in pairs(targets)do candidates[cid]=true end
   end end
   if scoped then
    local recipients={}
    -- Every selected receiver retains ALL its sources, including unchanged ones.
    for cid in pairs(candidates)do if rows[cid]then recipients[cid]=copy(rows[cid])end end
    return {input=d.Input(pid),recipients=recipients,candidates=candidates,scoped=true}
   end
  end
  return {input=d.Input(pid),recipients=copy(rows)}
 end
 -- B239 read-only per-city direct route projection. No Refresh, proof request,
 -- all-city scan or reference retention by the caller. UNKNOWN has no partners.
 local function domesticPartners(pid,selected,outgoing,effects)
  local b=d.players[pid];local v=views[pid]
  local out={validity='UNKNOWN',reason='NETWORK_NO_INPUT'}
  if b then out.input=d.Input(pid) end
  if isolated(pid) then out.reason='NETWORK_EXPERIMENT_ISOLATED';return out end
  if not d.ready or not P.IsTestPlayer(pid) then out.reason='NETWORK_NOT_READY_OR_OWNER';return out end
  if not b then return out end
  if not currentGeneration(pid,b)then out.reason='NETWORK_FACTS_PENDING';return out end
  if (b.queuedWork or b.negativeHeld) and (not effects or not b.continuityOnly)then out.reason='NETWORK_EVIDENCE_QUEUED';return out end
  if b.validity=='CONFIRMED_INVALID' then out.validity='CONFIRMED_INVALID';out.reason=b.error or 'NETWORK_CONFIRMED_INVALID';return out end
  local matches=b.validity=='VERIFIED' and v and v.contract==1 and v.epoch==d.epoch and v.player==pid
   and v.validity=='VERIFIED' and v.inputVersion==b.inputRevision and v.derivedFor==b.inputRevision
   and b.derivedFor==b.inputRevision and v.signature==b.inputSignature
  if not matches then out.reason='NETWORK_VIEW_UNAVAILABLE';return out end
  if not (effects and (b.effectAvailability=='AVAILABLE' or b.continuityOnly)) and
   (b.availability~='AVAILABLE' or b.revalidation~='VERIFIED' or b.signal~=(shared.RouteSignalRevision or 0)) then
   if b.signal~=(shared.RouteSignalRevision or 0)then state('NETWORK_SIGNAL_STALE',pid,b,'NETWORK_SIGNAL_UNPROVEN')end
   out.reason=b.transportFailure or 'NETWORK_REVALIDATION_PENDING';return out
  end
  local ok,ids,references,reference=pcall(function()
   assert(selected and selected:GetOwner()==pid,'NETWORK_SELECTED_OWNER_CHANGED')
   local id=selected:GetID();local ref=assert(v.references[id],'NETWORK_SELECTED_NOT_SAMPLED')
   assert(SPCNetworkInput.Reference(city(pid,id))==ref and SPCNetworkInput.Reference(selected)==ref,'NETWORK_SELECTED_REFERENCE_CHANGED')
   local keys,refs={},{}
   local projection=outgoing and v.directOutgoing or v.directDomestic
   for cid in pairs(projection[id] or {}) do
    local partner=assert(v.references[cid],'NETWORK_PARTNER_NOT_SAMPLED')
    if not effects then assert(SPCNetworkInput.Reference(city(pid,cid))==partner,'NETWORK_PARTNER_REFERENCE_CHANGED')end
    keys[#keys+1]=cid;refs[cid]=partner
   end
   table.sort(keys);return keys,refs,ref
  end)
  if not ok then out.reason=short(ids);return out end
  out.validity='VERIFIED';out.reason='NETWORK_AVAILABLE';out.cityID=selected:GetID();out.reference=reference
  out.partners=ids;out.references=references;out.provenance=copy(b.input.provenance);out.continuityOnly=b.continuityOnly==true;return out
 end
 function d.CurrentEffectPartners(pid,selected)return domesticPartners(pid,selected,false,true)end
 function d.CurrentDomesticPartners(pid,selected)return domesticPartners(pid,selected,false)end
 function d.CurrentOutgoingDomestic(pid,selected)return domesticPartners(pid,selected,true)end
 -- B241 Capital consumes the existing center/recipient topology, not the
 -- direct-pair Commercialization pool. Require current proof before selecting S.
 function d.CurrentCapitalSources(pid,selected,kind)
  local b=d.players[pid]
  assert(d.TransactionCurrent(pid),'CAPITAL_NETWORK_PENDING')
  local v=currentView(pid,true);local id=selected:GetID()
  assert(selected:GetOwner()==pid and v.references[id]==SPCNetworkInput.Reference(city(pid,id)),'CAPITAL_REFERENCE_CHANGED')
  local out={};for sid in pairs((v.recipients[kind] or {})[id] or {})do
   assert(v.references[sid]==SPCNetworkInput.Reference(city(pid,sid)),'CAPITAL_REFERENCE_CHANGED')
   out[#out+1]=sid
  end;table.sort(out);return out
 end
 function d.CurrentConnectedKinds(pid,selected)
  assert(d.ready and selected:GetOwner()==pid,'NETWORK_NOT_READY_OR_OWNER')
  return copy(currentView(pid,true).connected[selected:GetID()] or {})
 end
 function d.CurrentNational(pid)
  assert(d.ready and P.IsTestPlayer(pid),'NETWORK_NOT_READY_OR_OWNER')
  return copy(currentView(pid,true).national)
 end
 function d.CurrentRecipientSources(pid,selected,kind)
  assert(d.ready and selected:GetOwner()==pid,'NETWORK_NOT_READY_OR_OWNER')
  local v=currentView(pid,true);local ids={}
  for id in pairs((v.recipients[kind] or {})[selected:GetID()] or {}) do ids[#ids+1]=id end
  table.sort(ids);return ids
 end
 function d.ConnectedKinds(pid,selected)
  assert(d.ready and selected:GetOwner()==pid,'NETWORK_NOT_READY_OR_OWNER')
  return copy(currentView(pid).connected[selected:GetID()] or {})
 end
 function d.National(pid)
  assert(P.IsTestPlayer(pid) and d.ready,'NETWORK_NOT_READY_OR_OWNER')
  return copy(currentView(pid).national)
 end
 function d.RecipientSources(pid,selected,kind)
  assert(d.ready and selected:GetOwner()==pid,'NETWORK_NOT_READY_OR_OWNER')
  local v=currentView(pid);local result={}
  for src in pairs((v.recipients[kind] or {})[selected:GetID()] or {}) do result[#result+1]=src end
  table.sort(result);return result
 end
 local kinds={"RESEARCH","CULTURE","INDUSTRY"}
 local labels={RESEARCH="科研",CULTURE="文化",INDUSTRY="工业"}
 local function size(set) local n=0;for _ in pairs(set or {}) do n=n+1 end;return n end
 local function name(pid,id)
  local c=city(pid,id);local ok,n=pcall(function() return c:GetName() end)
  if not ok or type(n)~="string" then return "城市#"..id end
  if Locale and Locale.Lookup then local yes,v=pcall(Locale.Lookup,n);if yes then n=v end end
  return n:gsub("[\r\n]"," ").." (#"..id..")"
 end
 -- B231 explicit read only. No Refresh/Verified/Input, publication, recompute,
 -- carrier write or business cache mutation. Missing and retained inputs differ.
 function d.ReadSnapshot(pid,selected,details,page)
  assert(selected and selected:GetOwner()==pid,'NETWORK_SELECTED_OWNER_CHANGED')
  local id=selected:GetID();local b=d.players[pid];local v=views[pid]
  local coherent=b and b.validity=='VERIFIED' and v and v.contract==1 and v.epoch==d.epoch and v.player==pid and v.validity=='VERIFIED'
   and v.inputVersion==b.inputRevision and v.derivedFor==b.inputRevision
   and b.derivedFor==b.inputRevision and v.signature==b.inputSignature
  local reason=isolated(pid) and 'NETWORK_ISOLATED' or not d.ready and 'NETWORK_NOT_READY'
   or not b and 'NETWORK_NO_INPUT' or not coherent and 'NETWORK_VIEW_UNAVAILABLE'
   or b.availability~='AVAILABLE' and 'NETWORK_REVALIDATION_PENDING' or 'NETWORK_AVAILABLE'
  local function safeName(owner,cid)
   local ok,title=pcall(name,owner,cid);return ok and title or ('城市#'..tostring(cid)..'（玩家'..tostring(owner)..'）')
  end
  local function emit(stage,fields)if reportTrace then pcall(reportTrace.Record,stage,fields)end end
  local sources=coherent and v.sources or {};local centers=coherent and v.centers or {};local recipients=coherent and v.recipients or {}
  local receivers={};for _,set in pairs(recipients)do for cid in pairs(set)do receivers[cid]=true end end
  local err=b and b.error and SPCExpeditionTrainingDiagnostics.Failure(b.error,'SHARED_INPUT')
  local header=reason=='NETWORK_AVAILABLE' and '已就绪' or reason=='NETWORK_REVALIDATION_PENDING' and '上次已发布拓扑；当前待核验' or '尚无可用当前拓扑'
  local lines={'公共网络｜'..safeName(pid,id)..'｜'..header,
   '输入 '..tostring(b and b.validity or 'UNKNOWN')..' / '..tostring(b and b.availability or 'UNAVAILABLE')
    ..'；版本 '..tostring(b and b.inputRevision or '无')..' → '..tostring(b and b.derivedFor or '无')}
  emit('NETWORK_PUBLIC',{owner=pid,city=id,ready=d.ready,reason=reason,
   networkValidity=b and b.validity,networkAvailability=b and b.availability,
   networkInputRevision=b and b.inputRevision,networkDerivedFor=b and b.derivedFor,
   routeCount=b and b.routes and #b.routes,sourceCount=coherent and size(sources),
   centerCount=coherent and size(centers),recipientCount=coherent and size(receivers),
   phase=err and err.phase,errorCode=err and err.errorCode,errorClass=err and err.errorClass,
   errorFile=err and err.errorFile,errorLine=err and err.errorLine})
  if reason~='NETWORK_AVAILABLE'then lines[#lines+1]='状态：'..reason..(err and ('；错误 '..err.errorCode) or '')end
  if not details then
   lines[#lines+1]='已发布商路 '..tostring(b and b.routes and #b.routes or '未知')
    ..'｜来源城 '..(coherent and size(sources) or '未知')..'｜中心 '..(coherent and size(centers) or '未知')
   local f=b and b.input and b.input.cities[id]
   lines[#lines+1]=not coherent and '本城来源 / 中心角色尚未确认。' or '本城：'..(labels[sources[id]] and labels[sources[id]]..'来源' or '非来源')
    ..' / '..(centers[id] and '贸易中心' or '非中心')..(f and ('；已采样 ACTIVE '..tostring(f.active)) or '；城市事实未采样')
   for _,kind in ipairs(kinds)do
    local n=coherent and size((recipients[kind] or {})[id])
    lines[#lines+1]=labels[kind]..'：本城接入 '..tostring(n or '未知')..' 个来源；全国接收 '..tostring(coherent and size(recipients[kind]) or '未知')..' 城'
   end
  else
   local entries={}
   local function add(text,relation,kind,sourceCity,targetOwner,targetCity)
    entries[#entries+1]={text=text,fields={owner=pid,city=id,relation=relation,networkKind=kind,
     sourceCity=sourceCity,targetOwner=targetOwner,targetCity=targetCity,reason=reason}}
   end
   for cid,kind in pairs(sources)do add('来源 '..(labels[kind] or kind)..'：'..safeName(pid,cid),'SOURCE',kind,cid)end
   for cid in pairs(centers)do add('贸易中心：'..safeName(pid,cid),'CENTER',nil,cid)end
   for src in pairs(centers[id] or {})do
    add('本中心接入 '..(labels[sources[src]] or '?')..'：'..safeName(pid,src),'CENTER_INPUT',sources[src],src,pid,id)
   end
   for _,kind in ipairs(kinds)do for src in pairs((recipients[kind] or {})[id] or {})do
    add('本城接收 '..labels[kind]..'：'..safeName(pid,src),'RECEIVES',kind,src,pid,id)
   end end
   for _,route in ipairs(b and b.routes or {})do
    if route.oc==id or route.dp==pid and route.dc==id then
     add('商路 '..safeName(route.op,route.oc)..' → '..safeName(route.dp,route.dc),'ROUTE',nil,route.oc,route.dp,route.dc)
    end
   end
   table.sort(entries,function(a,z)return a.text<z.text end)
   local pages=math.max(1,math.ceil(#entries/5));page=integer(page) and page>=1 and ((page-1)%pages+1) or 1
   lines[#lines+1]='来源 / 接收 / 相关商路 '..page..'/'..pages
   if #entries==0 then lines[#lines+1]=coherent and '当前记录中无来源、中心或相关商路。' or '尚无可列出的记录；不是已确认零连接。'end
   for i=(page-1)*5+1,math.min(page*5,#entries)do
    lines[#lines+1]=entries[i].text;emit('NETWORK_LINK',entries[i].fields)
   end
   lines[#lines+1]='再次点击「网络来源 / 接收」翻页。'
  end
  lines[#lines+1]='只读已发布记录；查看不触发刷新，接收来源不代表可以转发。'
  return table.concat(lines,'\n')
 end
 -- Consumer reporting is independently protected: it cannot suppress topology.
 function d.Report(pid,selected,details,page)
  local ok,public=pcall(d.ReadSnapshot,pid,selected,details,page)
  if not ok then
   local f=SPCExpeditionTrainingDiagnostics.Failure(public,'PUBLIC_REPORT')
   public='公共网络读取失败：'..f.errorCode..'；'..f.errorFile..':'..tostring(f.errorLine or '?')
   if reportTrace then pcall(reportTrace.Record,'NETWORK_REPORT_ERROR',f)end
  end
  local consumer=shared.CultureNetwork
  if not consumer then return public..'\n文化收益模块：未建立。'end
  local good,culture=pcall(consumer.Describe,pid,selected)
  if good then return public..'\n\n'..culture end
  local f=SPCExpeditionTrainingDiagnostics.Failure(culture,'CULTURE_REPORT')
  if reportTrace then pcall(reportTrace.Record,'NETWORK_REPORT_ERROR',f)end
  return public..'\n文化收益报告失败：'..f.errorCode..'；'..f.errorFile..':'..tostring(f.errorLine or '?')
 end
 local detailPage={}
 function d.Read(pid,selected,details)
  if isolated(pid) then return shared.NetworkIsolation.Read(pid) end
  d.Refresh(pid)
  local b=d.players[pid]
  if not b or not b.routes then return "B031 网络待刷新: "..(b and b.reason or "NO_BACKGROUND_BATCH") end
  if not d.Verified(pid) then return "B031 网络待刷新: REFRESH_PENDING" end
  local ok,out=pcall(function()
   assert(selected:GetOwner()==pid,"SELECTED_OWNER_CHANGED")
   assert(d.Verified(pid),"CURRENT_ROUTE_INVALID")
   local v=currentView(pid)
   local sources,centers,recipients=v.sources,v.centers,v.recipients
   local id=selected:GetID();local title="B031 "..name(pid,id)
   if details then
    local entries={}
    for src in pairs(centers[id] or {}) do
     entries[#entries+1]="接入 "..labels[sources[src]]..": "..name(pid,src)..(src==id and " [首都自身]" or " [直连]")
    end
    for _,k in ipairs(kinds) do
     for src in pairs((recipients[k] or {})[id] or {}) do
      entries[#entries+1]="接收 "..labels[k]..": 来源 "..name(pid,src)
     end
    end
    for _,route in ipairs(b.routes) do
     if route.oc==id or (route.dp==pid and route.dc==id) then
      entries[#entries+1]="商路 "..name(route.op,route.oc).." → "..name(route.dp,route.dc)
     end
    end
    table.sort(entries)
    if #entries==0 then entries[1]="无接入来源、接收来源或相关商路" end
    local signature=table.concat(entries,"\n");local key=pid..":"..id;local cursor=detailPage[key]
    local pages=math.ceil(#entries/3)
    local page=(cursor and cursor.signature==signature) and (cursor.page%pages+1) or 1
    detailPage[key]={signature=signature,page=page}
    local lines={title.." | 明细 "..page.."/"..pages}
    for i=(page-1)*3+1,math.min(page*3,#entries) do lines[#lines+1]=entries[i] end
    lines[#lines+1]="再次点网络明细翻页；接收来源不等于可转发来源。"
    lines[#lines+1]="DEV网络状态；商业III专家奖励另按ACTIVE门控。"
    return table.concat(lines,"\n")
   end
   detailPage[pid..":"..id]=nil
   local dist=0
   for _,route in ipairs(b.routes) do if route.oc==id and route.dp==pid and centers[id] and next(centers[id]) then dist=dist+1 end end
   local lines={title.." | 当前商路总数="..#b.routes,
    "本城来源类型="..(labels[sources[id]] or (centers[id] and "贸易中心/非来源" or "非网络来源")).." | 贸易中心="..(centers[id] and "是" or "否").." | 分发路线="..dist}
   for _,k in ipairs(kinds) do
    local connected=0;for src in pairs(centers[id] or {}) do if sources[src]==k then connected=connected+1 end end
    local set=recipients[k] or {}
    lines[#lines+1]=labels[k]..": 本中心接入来源="..connected.." | 全国接收城市="..size(set).." | 本城接收="..(set[id] and "是" or "否")
   end
   lines[#lines+1]="来源数≠接收城市数；网络明细可看城市/方向。DEV网络；商业III专家奖励另按ACTIVE门控。"
   return table.concat(lines,"\n")
  end)
  return ok and out or ("B031 网络待刷新: "..short(out))
 end
 -- Clear only this session's derived topology. Explicit experiment != UNKNOWN/loss.
 function d.ExperimentalStop(pid)
  assert(isolated(pid),'NETWORK_EXPERIMENT_NOT_ARMED')
  local b=bucket(pid);assert(not b.refreshing,'NETWORK_EXPERIMENT_BUSY')
  views[pid]=nil;inputProviders[pid]=nil;pending[pid]=nil;dormant[pid]=nil;b.queuedWork=nil;b.negativeHeld=nil
  b.routes=nil;b.fingerprint=nil;b.routeReferences=nil;b.candidate=nil;b.input=nil;b.inputSignature=nil
  b.sources=nil;b.centers=nil;b.recipients=nil;b.derivedFor=nil
  b.validity='EXPERIMENT_ISOLATED';b.availability='EXPERIMENT_ISOLATED';b.reason='EXPERIMENT_ISOLATED'
  b.revalidation='EXPERIMENT_ISOLATED';b.error=nil;b.transportFailure=nil
  detailPage={}
  local perf=ExposedMembers.SPC_Performance;if perf then perf.routes=0 end
  return true -- no Capture/derive/publication/consumer dispatch
 end
 -- Event payloads only invalidate proof; they never become route facts.
 local function routeUnitRelevant(pid,id,removed)
  local b=d.players[pid]
  return not P.RouteUnitRelevant or P.RouteUnitRelevant(pid,id,removed and b and b.routeReferences or nil)
 end
 local function signal(namespace,name,unit)
  local event=P.Field(namespace,name);if not event or not event.Add then return end
  event.Add(function(pid,id)
   if unit then
    if type(pid)=='number' and not P.IsTestPlayer(pid)then return end
    if not routeUnitRelevant(pid,id,name=='UnitRemovedFromMap')then return end
   end
   shared.RouteSignalRevision=shared.RouteSignalRevision+1
  end)
 end
 for _,name in ipairs({'TradeRouteActivityChanged','TradeRouteRemovedFromMap','UnitRemovedFromMap','UnitOperationDeactivated','UnitOperationStarted','UnitOperationsCleared','CityRemovedFromMap','CityAddedToMap','CityTransfered','DiplomacyDeclareWar'})do signal(Events,name,name:find('^Unit')~=nil)end
 -- Preserve optional GameEvents namespace: B271's absent Events names do not establish these absent.
 for _,name in ipairs({'CityConquered','TradeRoutePlundered'})do signal(GameEvents,name,false)end
 function d.Rebuild()
  if isolated() then return end
  for pid in pairs(d.players) do d.Refresh(pid) end
 end
 for _,name in ipairs({"OnDistrictConstructed","CityBuilt"}) do
  local ev=P.Field(GameEvents,name);if ev and ev.Add then ev.Add(function(pid)
   if integer(pid)then if P.IsTestPlayer(pid)then d.Refresh(pid)end else d.Rebuild()end
  end) end
 end
 function d.CheckEvidence(failedFullRead,cause)
  if isolated() then return end
  for pid,b in pairs(d.players) do
   if b.refreshing then enqueue(pid,'evidence',failedFullRead and 'FAILED' or 'NATIVE')
   else
    if b.routes then pendingProof(pid,b,not failedFullRead,cause);d.Verified(pid,failedFullRead) end
    d.Refresh(pid)
   end
  end
 end
 for _,name in ipairs({'TradeRouteActivityChanged','TradeRouteRemovedFromMap','UnitRemovedFromMap','CityRemovedFromMap','CityTransfered','DiplomacyDeclareWar'}) do
  local ev=P.Field(Events,name);if ev and ev.Add then ev.Add(function(pid,id)
   if name=='UnitRemovedFromMap' then
    if type(pid)=='number' and not P.IsTestPlayer(pid)then return end
    if not routeUnitRelevant(pid,id,true)then return end
   end
   d.CheckEvidence(false,name)
  end) end
 end
 -- Current facts, not the event name/turn, determine whether a version is published.
 -- These events identify the affected player in their first native argument.
 -- Keep every local notification, including repeated ones within the same turn.
 local function rebuildPlayer(pid)
  if integer(pid) then d.Refresh(pid) else d.Rebuild() end
 end
 for _,name in ipairs({'PlayerTurnActivated'}) do
  local ev=P.Field(Events,name);if ev and ev.Add then ev.Add(rebuildPlayer) end
 end
 -- Governor changes arrive through NativeFacts/ACTIVE. Independent capital
 -- and city-membership causes retain their existing full safety scope.
 for _,name in ipairs({'CapitalCityChanged','CityAddedToMap'}) do
  local ev=P.Field(Events,name);if ev and ev.Add then ev.Add(d.Rebuild) end
 end
 SPCRuntimeWork.StartReady(P,shared,'NetworkBridge',function()d.ready=true;d.Rebuild()end)
 -- The shared view is an indivisible verified snapshot. Known ownership loss
 -- invalidates the former participant's snapshot via its existing publication contract.
 if shared.CityProgressionStore then shared.CityProgressionStore.RegisterExit('NetworkBridge',function(c,loss)
  assert(shared.CityProgressionStore.IsExitTarget(c,loss),'EXIT_NOT_CONFIRMED')
  local pid=loss.origin.owner;local b=d.players[pid]
  if b then
   if b.refreshing then
    local source=b.input and b.input.cities[loss.origin.cityID]
    if source then enqueue(pid,'loss',{city=loss.origin.cityID,reference=source.reference})end
    error('EXIT_NETWORK_QUEUED',0) -- preserve Store's unconfirmed-exit guard until its ordinary retry
   end
   b.refreshing=true
   local ok,err=pcall(prune,pid,b,{[loss.origin.cityID]=true},nil,'E2_CONFIRMED_OWNER_LOSS')
   b.refreshing=false;assert(ok,err)
  end
 end)end

 if shared.CityProgressionStore then shared.CityProgressionStore.RegisterReturn('NetworkBridge',function(pid)
  local b=d.players[pid];if b then pendingProof(pid,b,true,'E2_RECAPTURE_REQUIRES_CURRENT_ROUTES')end
 end)end

end
