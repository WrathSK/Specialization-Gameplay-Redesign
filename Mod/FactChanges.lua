-- Declared per-Gameplay fact propagation. No native reads, persistent state or timer.
SPCFactChanges={}
local M=SPCFactChanges
local SCOPE_LIMIT=2048
-- Reservation replaces all older entries for this receiver and scope. Only
-- phase-zero derived work can also leave a separately queued next batch.
local RECEIPT_BATCHES=2
local RECEIPTS_PER_RECEIVER=SCOPE_LIMIT*RECEIPT_BATCHES
local K={IDENTITY=true,POTENTIAL=true,ACTIVE=true,D=true,WORKERS=true,HISTORY=true,NETWORK=true}
local function token(v)return type(v)=='string' and #v>0 and #v<=64 and v:match('^[A-Za-z][A-Za-z0-9_]*$')end
local function integer(v)return type(v)=='number' and v>=0 and v<9007199254740992 and v%1==0 end
local function atom(v)local s=type(v)..':'..tostring(v);return #s..':'..s end
local function entries(values,limit,visit)
 assert(type(values)=='table' and getmetatable(values)==nil,'FACT_DECLARATION_STRUCTURE')
 local count=0
 for index,value in pairs(values)do
  count=count+1;assert(integer(index) and index>=1 and index<=limit and count<=limit,'FACT_DECLARATION_LIMIT')
  visit(value)
 end
end
local function clone(value,seen,depth,budget)
 local kind=type(value)
 if kind~='table'then
  assert(kind=='nil' or kind=='string' and #value<=1024 or kind=='number' and value==value and math.abs(value)<math.huge or kind=='boolean','FACT_EVIDENCE_NOT_SCALAR')
  return value
 end
 seen=seen or {};depth=depth or 0;budget=budget or {n=0,limit=1024}
 assert(depth<8 and not seen[value] and getmetatable(value)==nil,'FACT_EVIDENCE_STRUCTURE')
 seen[value]=true;local out={}
 for key,v in pairs(value)do
  assert(type(key)=='string' and #key<=128 or integer(key),'FACT_EVIDENCE_KEY')
  budget.n=budget.n+1;assert(budget.n<=(budget.limit or 1024),'FACT_EVIDENCE_LIMIT')
  out[key]=clone(v,seen,depth+1,budget)
 end
 seen[value]=nil;return out
end
-- Typed native transfer scope is independent of generic last-writer evidence.
-- It is a routing hint only, never Store ownership/loss or transaction proof.
local function transfer(value,owner,city)
 if value==nil then return end
 assert(type(value)=='table' and getmetatable(value)==nil,'FACT_TRANSFER_STRUCTURE')
 local allowed={owner=true,city=true,oldOwner=true};local n=0
 for k,v in pairs(value)do
  n=n+1;assert(allowed[k] and integer(v) and v<2147483648,'FACT_TRANSFER_FIELD')
 end
 assert(n==3 and value.owner~=nil and value.city~=nil and value.oldOwner~=nil,'FACT_TRANSFER_FIELDS')
 assert(owner==nil or owner==value.owner or owner==value.oldOwner,'FACT_TRANSFER_OWNER')
 assert(city==nil or owner==value.owner and city==value.city,'FACT_TRANSFER_CITY')
 return {owner=value.owner,city=value.city,oldOwner=value.oldOwner}
end
function M.New(shared)
 local previous=shared.FactChanges
 if previous and type(previous.Close)=='function'then previous.Close()end
 M.epoch=(M.epoch or 0)+1
 local d={epoch=M.epoch,sequence=0,emitted=0,delivered=0,pending=0,retained=0,retainedScopes=0,retryReady=0,errors={},closed=false}
 local consumers,order,queue,keys={},{},{},{};local responsibilityOrder={};local busy=false
 local scopeReceipts={}
 local activePhase,activeConsumer,activeWork,activeKeys,deriving
 d.flushRevision=0
 -- Session-local authority stamps, not fact values. Owner scope covers pool membership:
 -- a newly qualifying source may be absent from every old per-city dependency list.
 local generations={};local owners=0;local global={NETWORK=0,COMMERCE=0}
 function d.Generation(owner,domain,cityID)
  local row=generations[owner]
  if domain=='COMMERCE' and cityID~=nil then return global.COMMERCE+(row and row.cities and row.cities[cityID] or 0) end
  return (global[domain] or 0)+(row and row[domain] or 0)
 end
 -- Scalar role-fact versions. Never evict a city and accidentally certify old facts.
 function d.NetworkCityGeneration(owner,cityID)
  local row=generations[owner]
  return global.NETWORK+(row and row.NETWORK_WIDE or 0)+(row and row.networkCities and row.networkCities[cityID] or 0)
 end
 local function invalidate(owner,cityID,kinds,topic)
  local network=kinds.IDENTITY or kinds.POTENTIAL or kinds.ACTIVE
  local commerce=network or kinds.D or kinds.WORKERS or kinds.HISTORY and topic=='COMMERCE'
  if not network and not commerce then return end
  if owner==nil then
   if network then global.NETWORK=global.NETWORK+1 end
   if commerce then global.COMMERCE=global.COMMERCE+1 end
   return
  end
  local row=generations[owner]
  if not row then assert(owners<2048,'FACT_OWNER_LIMIT');owners=owners+1;row={};generations[owner]=row end
  if network then
   row.NETWORK=(row.NETWORK or 0)+1
   row.networkCities=row.networkCities or {};row.networkCityCount=row.networkCityCount or 0
   if cityID==nil or row.networkCities[cityID]==nil and row.networkCityCount>=2048 then
    row.NETWORK_WIDE=(row.NETWORK_WIDE or 0)+1
   else
    if row.networkCities[cityID]==nil then row.networkCityCount=row.networkCityCount+1 end
    row.networkCities[cityID]=(row.networkCities[cityID] or 0)+1
   end
  end
  if commerce then
   if network or cityID==nil or (row.cityCount or 0)>=2048 and row.cities[cityID]==nil then
    -- Existing city stamps stay valid as identities. The owner stamp makes an
    -- unindexable change unsafe for strict use without allocating or evicting.
    row.COMMERCE=(row.COMMERCE or 0)+1
   else
    row.cities=row.cities or {};row.cityCount=row.cityCount or 0
    if row.cities[cityID]==nil then row.cityCount=row.cityCount+1 end
    row.cities[cityID]=(row.cities[cityID] or 0)+1
   end
  end
 end
 shared.FactChanges=d
 -- Committed producers invalidate authority before fallible evidence construction.
 -- Emit also invalidates independently; repeated stamps are harmless opaque versions.
 function d.InvalidateCommitted(owner,cityID,kinds,topic)
  assert(not d.closed and (owner==nil or integer(owner))
   and (cityID==nil or owner~=nil and integer(cityID)),'FACT_COMMIT_SCOPE')
  local set={};entries(kinds,7,function(kind)assert(K[kind],'FACT_KIND_UNKNOWN');set[kind]=true end)
  assert(next(set) and (topic==nil or token(topic)),'FACT_COMMIT_KINDS')
  invalidate(owner,cityID,set,topic)
 end
 -- A scope is counted once, independent of the number of subscribers. Check
 -- both budgets before committing any reservation or changing the queue.
 local function checkCapacity(scopes,receipts,receiverCount)
  assert(d.retained+receipts<=RECEIPTS_PER_RECEIVER*receiverCount,'FACT_DELIVERY_RECEIVER_LIMIT')
  assert(d.retainedScopes+scopes<=SCOPE_LIMIT,'FACT_DELIVERY_SCOPE_LIMIT')
 end
 function d.ReceiptSlotsPerReceiver()return RECEIPTS_PER_RECEIVER end
 local interested
 local function merged(previous,row)
  if not previous then return row end
  local out=clone(row)
  for _,field in ipairs({'kinds','causes','topics','revisions'})do
   for k,v in pairs(previous[field])do if out[field][k]==nil then out[field][k]=v end end
  end
  if out.evidence==nil then out.evidence=previous.evidence end
  if out.investment==nil then out.investment=previous.investment end
  if previous.transfers then
   out.transfers=out.transfers or {};for k,v in pairs(previous.transfers)do if not out.transfers[k]then out.transfers[k]=clone(v)end end
  end
  for _,field in ipairs({'causes','topics','transfers'})do
   local n=0;for _ in pairs(out[field] or {})do n=n+1 end;assert(n<=32,'FACT_DELIVERY_MERGE_LIMIT')
  end
  clone(out);return out
 end
 local function slot(key,batch)return key..atom(batch)end
 local function prepare(consumer,key,row)
  local replaced={};local source=consumer.byScope[key] or {}
  -- A phase0-derived fact belongs to the active snapshot. A separately queued
  -- next-snapshot cause must neither leak into it nor be erased by its ACK.
  for batch,old in pairs(source)do if batch<=row.deliveryBatch then replaced[#replaced+1]=old end end
  table.sort(replaced,function(a,b)return a.row.sequence<b.row.sequence end)
  local prior
  for _,old in ipairs(replaced)do prior=merged(prior,old.row)end
  -- Share the detached row until a receiver needs its own retained history.
  -- Only a fresh copy leaves this registry during an attempt.
  return {key=slot(key,row.deliveryBatch),scope=key,batch=row.deliveryBatch,row=merged(prior,row),state='QUEUED',wakes={},replaces=replaced}
 end
 local function remove(consumer,entry)
  if consumer.deliveries[entry.key]~=entry then return false end
  if entry.armed then d.retryReady=d.retryReady-1 end
  if entry.error then consumer.failures=consumer.failures-1 end
  consumer.deliveries[entry.key]=nil
  local scope=consumer.byScope[entry.scope]
  if scope then scope[entry.batch]=nil;if not next(scope)then consumer.byScope[entry.scope]=nil end end
  local receipts=scopeReceipts[entry.scope]-1
  if receipts==0 then
   scopeReceipts[entry.scope]=nil
   d.retainedScopes=d.retainedScopes-1
  else scopeReceipts[entry.scope]=receipts end
  d.retained=d.retained-1;return true
 end
 local function install(consumer,entry)
  for _,old in ipairs(entry.replaces)do remove(consumer,old)end
  entry.replaces=nil
  consumer.deliveries[entry.key]=entry;consumer.byScope[entry.scope]=consumer.byScope[entry.scope] or {}
  consumer.byScope[entry.scope][entry.batch]=entry;d.retained=d.retained+1
  local receipts=scopeReceipts[entry.scope]
  if not receipts then d.retainedScopes=d.retainedScopes+1 end
  scopeReceipts[entry.scope]=(receipts or 0)+1
 end
 function d.Receipt(event,status,reason)
  local v=type(event)=='table' and getmetatable(event)==nil and event.delivery
  assert(not d.closed and type(v)=='table' and getmetatable(v)==nil and v.epoch==d.epoch
   and token(v.consumer) and integer(v.ticket),'FACT_RECEIPT_CONTEXT')
  assert(status=='REGISTERED' or status=='IRRELEVANT' and token(reason),'FACT_RECEIPT_STATUS')
  return {status=status,epoch=v.epoch,consumer=v.consumer,ticket=v.ticket,reason=reason}
 end
 function d.AcceptsReceipt(event,receipt)
  if d.closed or type(receipt)~='table' or getmetatable(receipt)~=nil then return false end
  local v=event.delivery
  return v and v.epoch==d.epoch and receipt.epoch==v.epoch and receipt.consumer==v.consumer and receipt.ticket==v.ticket
   and (receipt.status=='REGISTERED' or receipt.status=='IRRELEVANT' and token(receipt.reason)) or false
 end
 function d.RegisterConsumer(name,callback,options)
  assert(not d.closed and token(name) and not consumers[name] and type(callback)=='function','FACT_CONSUMER_INVALID')
  assert(#order<128,'FACT_CONSUMER_LIMIT');options=options or {}
  assert(type(options)=='table' and getmetatable(options)==nil,'FACT_OPTIONS_STRUCTURE');local kinds={}
  entries(options.kinds or {},7,function(kind)assert(K[kind],'FACT_KIND_UNKNOWN');kinds[kind]=true end)
  assert(next(kinds),'FACT_CONSUMER_KINDS_REQUIRED')
  local topics={};entries(options.topics or {},32,function(topic)assert(token(topic),'FACT_TOPIC_INVALID');topics[topic]=true end)
  local phase=options.phase or 1;assert(phase==0 or phase==1,'FACT_PHASE_INVALID')
  assert(options.delivery==nil or options.delivery=='RESPONSIBILITY' and phase==1,'FACT_DELIVERY_MODE')
  assert(options.ordered==nil or options.ordered==true and options.delivery=='RESPONSIBILITY','FACT_ORDERED_DELIVERY_MODE')
  assert(options.delivery==nil or not busy,'FACT_DELIVERY_REGISTER_DURING_FLUSH')
  local consumer={name=name,callback=callback,kinds=kinds,topics=topics,phase=phase,order=#order+1,
   responsibility=options.delivery~=nil,ordered=options.ordered,deliveries={},byScope={},failures=0}
  local reserved={}
  if consumer.responsibility then
   local scopes=0
   for _,key in ipairs(keys)do
    local row=queue[key]
    if interested(consumer,row)then
     reserved[#reserved+1]=prepare(consumer,key,row)
     if not scopeReceipts[key]then scopes=scopes+1 end
    end
   end
   checkCapacity(scopes,#reserved,#responsibilityOrder+1)
  end
  consumers[name]=consumer;order[#order+1]=name
  if consumer.responsibility then responsibilityOrder[#responsibilityOrder+1]=name end
  for _,entry in ipairs(reserved)do install(consumer,entry)end
  return name
 end
 function d.Emit(event)
  assert(not d.closed and type(event)=='table' and getmetatable(event)==nil,'FACT_CHANGE_STRUCTURE')
  assert(token(event.cause),'FACT_CHANGE_INVALID')
  assert(event.owner==nil or integer(event.owner),'FACT_OWNER_INVALID')
  assert(event.cityID==nil or integer(event.cityID) and event.owner~=nil,'FACT_CITY_INVALID')
  assert(event.reference==nil or type(event.reference)=='string' and #event.reference<=512,'FACT_REFERENCE_INVALID')
  assert(event.revision==nil or integer(event.revision),'FACT_REVISION_INVALID')
  assert(event.topic==nil or token(event.topic),'FACT_TOPIC_INVALID')
  local kinds={};entries(event.kinds or {},7,function(kind)assert(K[kind],'FACT_KIND_UNKNOWN');kinds[kind]=true end)
  assert(next(kinds),'FACT_KINDS_REQUIRED')
  -- Validate the whole payload before changing queue state; native objects fail closed.
  local evidence=clone(event.evidence,nil,1,{n=0,limit=256});local investment=clone(event.investment,nil,1,{n=0,limit=256})
  local moved=transfer(event.transfer,event.owner,event.cityID)
  local key=atom(event.owner)..atom(event.cityID)..atom(event.reference)
  local previous=queue[key]
  assert(previous or #keys<SCOPE_LIMIT,'FACT_QUEUE_LIMIT')
  local row={player=event.owner,city=event.cityID,reference=event.reference,kinds={},causes={},topics={},revisions={},
   deliveryBatch=deriving and d.flushRevision or d.flushRevision+1}
  if previous then
   for _,field in ipairs({'kinds','causes','topics','revisions'})do for k,v in pairs(previous[field])do row[field][k]=v end end
   row.evidence=previous.evidence;row.investment=previous.investment
  end
  if moved or previous and previous.transfers then
   local transfers={};local n=0
   for k,v in pairs(previous and previous.transfers or {})do
    n=n+1;transfers[k]={owner=v.owner,city=v.city,oldOwner=v.oldOwner}
   end
   if moved then
    local k=atom(moved.owner)..atom(moved.city)..atom(moved.oldOwner)
    if not transfers[k]then n=n+1 end
    assert(n<=32,'FACT_TRANSFER_LIMIT');transfers[k]=moved
   end
   row.transfers=transfers
  end
  row.cause=event.cause;row.revision=event.revision;row.sequence=d.sequence+1
  row.causes[event.cause]=true;if event.topic then row.topics[event.topic]=true end
  for kind in pairs(kinds)do row.kinds[kind]=true;row.revisions[kind]=event.revision end
  if evidence~=nil then row.evidence=evidence end
  if investment~=nil then row.investment=investment end
  -- Cause/topic names are detached bounded tokens, never raw filenames/errors.
  local n=0;for _ in pairs(row.causes)do n=n+1 end;assert(n<=32,'FACT_CAUSE_LIMIT')
  n=0;for _ in pairs(row.topics)do n=n+1 end;assert(n<=32,'FACT_TOPIC_LIMIT')
  local reserved={};local added=0
  for _,name in ipairs(responsibilityOrder)do local consumer=consumers[name]
   if interested(consumer,row)then
    local entry=prepare(consumer,key,row);reserved[#reserved+1]={consumer,entry};added=added+1-#entry.replaces
   end
  end
  local newScope=#reserved>0 and not scopeReceipts[key] and 1 or 0
  checkCapacity(newScope,added,#responsibilityOrder)
  invalidate(event.owner,event.cityID,kinds,event.topic) -- zero native calls; visible before deferred delivery
  d.sequence=row.sequence;d.emitted=d.emitted+1
  if not previous then keys[#keys+1]=key;d.pending=#keys end
  queue[key]=row
  for _,item in ipairs(reserved)do install(item[1],item[2])end
  return row.sequence
 end
 -- A Bridge proof published inside its own sampling callback can feed phase1.
 -- Every unrelated/reentrant cause remains in the next ordinary snapshot.
 function d.EmitDerived(event)
  assert(type(event)=='table' and getmetatable(event)==nil,'FACT_DERIVED_STRUCTURE')
  local count=0;entries(event.kinds or {},7,function(k)assert(k=='NETWORK','FACT_DERIVED_KIND');count=count+1 end)
  assert(count==1,'FACT_DERIVED_KIND')
  if not (busy and activePhase==0 and activeConsumer=='NetworkBridge')then return d.Emit(event)end
  local savedQueue,savedKeys,savedPending=queue,keys,d.pending
  queue=activeWork;keys=activeKeys;d.pending=#keys
  local wasDeriving=deriving;deriving=true
  local ok,value=pcall(d.Emit,event);deriving=wasDeriving
  activeWork=queue;activeKeys=keys;queue=savedQueue;keys=savedKeys;d.pending=savedPending
  assert(ok,value);return value
 end
 interested=function(consumer,row)
  for kind in pairs(row.kinds)do if consumer.kinds[kind]then
   if kind~='HISTORY' or not next(consumer.topics)then return true end
   for topic in pairs(row.topics)do if consumer.topics[topic]then return true end end
  end end
  return false
 end
 -- Explicit completion/availability wake only. Repeated cause/revision cannot
 -- rearm a failed ticket; idle publication never manufactures retry evidence.
 function d.WakeConsumer(name,cause,revision,scope)
  if d.closed then return false end
  local consumer=consumers[name]
  assert(consumer and consumer.responsibility and token(cause) and integer(revision),'FACT_WAKE_INVALID')
  assert(scope==nil or type(scope)=='table' and getmetatable(scope)==nil,'FACT_WAKE_SCOPE')
  if scope then
   assert(scope.player==nil or integer(scope.player),'FACT_WAKE_PLAYER')
   assert(scope.city==nil or integer(scope.city) and scope.player~=nil,'FACT_WAKE_CITY')
   assert(scope.reference==nil or type(scope.reference)=='string' and #scope.reference<=512,'FACT_WAKE_REFERENCE')
  end
  local woke=false
  for _,entry in pairs(consumer.deliveries)do local row=entry.row
   if entry.state=='HELD' and (not scope or (scope.player==nil or row.player==scope.player)
    and (scope.city==nil or row.city==nil or row.city==scope.city)
    and (scope.reference==nil or row.reference==scope.reference)) and revision>(entry.wakes[cause] or -1)then
    if entry.wakes[cause]==nil then local n=0;for _ in pairs(entry.wakes)do n=n+1 end;assert(n<32,'FACT_WAKE_CAUSE_LIMIT')end
    entry.wakes[cause]=revision
    if not entry.armed then entry.armed=true;d.retryReady=d.retryReady+1 end
    woke=true
   end
  end
  return woke
 end
 local function finish(consumer,entry,ok,result)
  -- Reentrant Emit/Close owns the newer entry.
  if d.closed or consumer.deliveries[entry.key]~=entry then return end
  local event={delivery={epoch=d.epoch,consumer=consumer.name,ticket=entry.row.sequence}}
  if ok and d.AcceptsReceipt(event,result)then
   remove(consumer,entry)
  else
   if not entry.error then consumer.failures=consumer.failures+1 end
   local safe,text=pcall(tostring,result)
   entry.error=not ok and (safe and text:sub(1,180) or 'FACT_CALLBACK_FAILED') or 'FACT_DELIVERY_UNACKNOWLEDGED'
   entry.state='HELD'
  end
  if consumer.ordered then d.errors[consumer.name]=consumer.failures>0 and 'FACT_DELIVERY_UNACKNOWLEDGED' or nil end
 end
 local function attempt(consumer,entry)
  if consumer.deliveries[entry.key]~=entry then return end
  if entry.armed then entry.armed=false;d.retryReady=d.retryReady-1 end
  local resolve,resolved
  if consumer.ordered then
   local name,key,ticket=consumer.name,entry.key,entry.row.sequence
   resolve=function(receipt)
    if resolved then return end;resolved=true
    local current=consumers[name];local received=current and current.deliveries[key]
    if received and received.row.sequence==ticket then finish(current,received,true,receipt)end
   end
  end
  local ok,result=pcall(function()
   local event=clone(entry.row);event.delivery={epoch=d.epoch,consumer=consumer.name,ticket=entry.row.sequence}
   if resolve then return consumer.callback(event,resolve)end
   return consumer.callback(event)
  end)
  d.delivered=d.delivered+1
  -- The existing Binding drain will finish this exact ticket. A successful
  -- collection alone does not acknowledge the owner's audit.
  if resolved then return end
  if resolve and ok and result==true then
   if not d.closed and consumer.deliveries[entry.key]==entry then entry.state='COLLECTED'end
  else resolved=true;finish(consumer,entry,ok,result)end
 end
 function d.Flush()
  if d.closed or busy or #keys==0 and d.retryReady==0 then return false end
  busy=true
  local work,sequence=queue,keys;queue={};keys={};d.pending=0
  local retry={}
  for _,name in ipairs(order)do local consumer=consumers[name]
   if consumer.responsibility then
    local rows={};for _,entry in pairs(consumer.deliveries)do if entry.armed then rows[#rows+1]=entry end end;retry[name]=rows
   end
  end
  d.flushRevision=d.flushRevision+1;local initialCount=#sequence;activeWork=work;activeKeys=sequence
  -- Known phases, stable registration order. New causes never recurse into this snapshot.
  for phase=0,1 do activePhase=phase;for _,name in ipairs(order)do local consumer=consumers[name]
   if consumer and consumer.phase==phase then
    local failure;local attempted=false;local seen={}
    for index=1,(phase==0 and initialCount or #sequence)do
     local key=sequence[index]
     if d.closed then busy=false;activeWork=nil;activeKeys=nil;activeConsumer=nil;activePhase=nil;return true end
     local row=work[key]
     if interested(consumer,row)then
      activeConsumer=name
      if consumer.responsibility then
       local entry=consumer.deliveries[slot(key,row.deliveryBatch)]
       if entry and entry.row.sequence==row.sequence then attempted=true;seen[entry]=true;attempt(consumer,entry)end
      else
       attempted=true;local ok,err=pcall(function()return consumer.callback(clone(row))end);d.delivered=d.delivered+1
       if not ok then local read,message=pcall(tostring,err);failure=read and message:sub(1,180) or 'FACT_CALLBACK_FAILED'end
      end
      activeConsumer=nil
     end
    end
    for _,entry in ipairs(retry[name] or {})do
     if d.closed then break end
     if not seen[entry] and consumer.deliveries[entry.key]==entry and entry.armed then
      attempted=true;activeConsumer=name;attempt(consumer,entry);activeConsumer=nil
     end
    end
    if consumer.responsibility then
     d.errors[name]=consumer.failures>0 and 'FACT_DELIVERY_UNACKNOWLEDGED' or nil
    elseif attempted then d.errors[name]=failure end
   end
  end end
  busy=false;activePhase=nil;activeConsumer=nil;activeWork=nil;activeKeys=nil;return true
 end
 function d.Close()
  queue={};keys={};consumers={};order={};responsibilityOrder={};scopeReceipts={}
  d.pending=0;d.retained=0;d.retainedScopes=0;d.retryReady=0;d.closed=true
  if shared.FactChanges==d then shared.FactChanges=nil end
 end
 return d
end
