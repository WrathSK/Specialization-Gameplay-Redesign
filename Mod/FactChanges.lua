-- Declared per-Gameplay fact propagation. No native reads, persistent state or timer.
SPCFactChanges={}
local M=SPCFactChanges
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
function M.New(shared)
 local previous=shared.FactChanges
 if previous and type(previous.Close)=='function'then previous.Close()end
 local d={sequence=0,emitted=0,delivered=0,pending=0,errors={},closed=false}
 local consumers,order,queue,keys={},{},{},{};local busy=false
 local activePhase,activeConsumer,activeWork,activeKeys
 d.flushRevision=0
 -- Session-local authority stamps, not fact values. Owner scope covers pool membership:
 -- a newly qualifying source may be absent from every old per-city dependency list.
 local generations={};local owners=0
 function d.Generation(owner,domain,cityID)
  local row=generations[owner]
  if domain=='COMMERCE' and cityID~=nil then return row and row.cities and row.cities[cityID] or 0 end
  return row and row[domain] or 0
 end
 local function invalidate(owner,cityID,kinds,topic)
  if owner==nil then return end
  local network=kinds.IDENTITY or kinds.POTENTIAL or kinds.ACTIVE
  local commerce=network or kinds.D or kinds.WORKERS or kinds.HISTORY and topic=='COMMERCE'
  if not network and not commerce then return end
  local row=generations[owner]
  if not row then assert(owners<2048,'FACT_OWNER_LIMIT');owners=owners+1;row={};generations[owner]=row end
  if network then row.NETWORK=(row.NETWORK or 0)+1 end
  if commerce then
   if network or cityID==nil then row.COMMERCE=(row.COMMERCE or 0)+1
   else
    row.cities=row.cities or {};row.cityCount=row.cityCount or 0
    if row.cities[cityID]==nil then assert(row.cityCount<2048,'FACT_CITY_LIMIT');row.cityCount=row.cityCount+1 end
    row.cities[cityID]=(row.cities[cityID] or 0)+1
   end
  end
 end
 shared.FactChanges=d
 -- Committed producers invalidate authority before fallible evidence construction.
 -- Emit also invalidates independently; repeated stamps are harmless opaque versions.
 function d.InvalidateCommitted(owner,cityID,kinds,topic)
  assert(not d.closed and integer(owner) and (cityID==nil or integer(cityID)),'FACT_COMMIT_SCOPE')
  local set={};entries(kinds,7,function(kind)assert(K[kind],'FACT_KIND_UNKNOWN');set[kind]=true end)
  assert(next(set) and (topic==nil or token(topic)),'FACT_COMMIT_KINDS')
  invalidate(owner,cityID,set,topic)
 end
 function d.RegisterConsumer(name,callback,options)
  assert(not d.closed and token(name) and not consumers[name] and type(callback)=='function','FACT_CONSUMER_INVALID')
  assert(#order<128,'FACT_CONSUMER_LIMIT');options=options or {}
  assert(type(options)=='table' and getmetatable(options)==nil,'FACT_OPTIONS_STRUCTURE');local kinds={}
  entries(options.kinds or {},7,function(kind)assert(K[kind],'FACT_KIND_UNKNOWN');kinds[kind]=true end)
  assert(next(kinds),'FACT_CONSUMER_KINDS_REQUIRED')
  local topics={};entries(options.topics or {},32,function(topic)assert(token(topic),'FACT_TOPIC_INVALID');topics[topic]=true end)
  local phase=options.phase or 1;assert(phase==0 or phase==1,'FACT_PHASE_INVALID')
  consumers[name]={name=name,callback=callback,kinds=kinds,topics=topics,phase=phase,order=#order+1}
  order[#order+1]=name
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
  local key=atom(event.owner)..atom(event.cityID)..atom(event.reference)
  local previous=queue[key]
  assert(previous or #keys<2048,'FACT_QUEUE_LIMIT')
  local row={player=event.owner,city=event.cityID,reference=event.reference,kinds={},causes={},topics={},revisions={}}
  if previous then
   for _,field in ipairs({'kinds','causes','topics','revisions'})do for k,v in pairs(previous[field])do row[field][k]=v end end
   row.evidence=previous.evidence;row.investment=previous.investment
  end
  row.cause=event.cause;row.revision=event.revision;row.sequence=d.sequence+1
  row.causes[event.cause]=true;if event.topic then row.topics[event.topic]=true end
  for kind in pairs(kinds)do row.kinds[kind]=true;row.revisions[kind]=event.revision end
  if evidence~=nil then row.evidence=evidence end
  if investment~=nil then row.investment=investment end
  -- Cause/topic names are detached bounded tokens, never raw filenames/errors.
  local n=0;for _ in pairs(row.causes)do n=n+1 end;assert(n<=32,'FACT_CAUSE_LIMIT')
  n=0;for _ in pairs(row.topics)do n=n+1 end;assert(n<=32,'FACT_TOPIC_LIMIT')
  invalidate(event.owner,event.cityID,kinds,event.topic) -- zero native calls; visible before deferred delivery
  d.sequence=row.sequence;d.emitted=d.emitted+1
  if not previous then keys[#keys+1]=key;d.pending=#keys end
  queue[key]=row;return row.sequence
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
  local ok,value=pcall(d.Emit,event)
  activeWork=queue;activeKeys=keys;queue=savedQueue;keys=savedKeys;d.pending=savedPending
  assert(ok,value);return value
 end
 local function interested(consumer,row)
  for kind in pairs(row.kinds)do if consumer.kinds[kind]then
   if kind~='HISTORY' or not next(consumer.topics)then return true end
   for topic in pairs(row.topics)do if consumer.topics[topic]then return true end end
  end end
  return false
 end
 function d.Flush()
  if d.closed or busy or #keys==0 then return false end
  busy=true
  local work,sequence=queue,keys;queue={};keys={};d.pending=0
  d.flushRevision=d.flushRevision+1;local initialCount=#sequence;activeWork=work;activeKeys=sequence
  -- Known phases, stable registration order. New causes never recurse into this snapshot.
  for phase=0,1 do activePhase=phase;for _,name in ipairs(order)do local consumer=consumers[name]
   if consumer and consumer.phase==phase then
    local failure;local attempted=false
    for index=1,(phase==0 and initialCount or #sequence)do
     local key=sequence[index]
     if d.closed then busy=false;activeWork=nil;activeKeys=nil;activeConsumer=nil;activePhase=nil;return true end
     local row=work[key]
     if interested(consumer,row)then
      attempted=true;activeConsumer=name;local ok,err=pcall(function()return consumer.callback(clone(row))end);activeConsumer=nil;d.delivered=d.delivered+1
      if not ok then local read,message=pcall(tostring,err);failure=read and message:sub(1,180) or 'FACT_CALLBACK_FAILED'end
     end
    end
    if attempted then d.errors[name]=failure end
   end
  end end
  busy=false;activePhase=nil;activeConsumer=nil;activeWork=nil;activeKeys=nil;return true
 end
 function d.Close()
  queue={};keys={};consumers={};order={};d.pending=0;d.closed=true
  if shared.FactChanges==d then shared.FactChanges=nil end
 end
 return d
end
