if not SPCIdentityEqual then include('IdentityEqual')end
local sameIdentity=SPCIdentityEqual.Same
-- ProductionPanel-local containment; native data and selection remain the base panel's.
SPCSafeAdapters={}
function SPCSafeAdapters.New()
 local d={entries={},hooks={},closed=false}
 -- Fixed UI phases only; ranks preserve different render/selection/hook orders.
 -- Declarations are copied scalar metadata, never event discovery or native facts.
 local phases={Render={},Before={},Publish={},Pulse={},Warm={},Queue={},Connect={}}
 local methods={Render={Items=true,Sync=true},Before={Before=true},Publish={Publish=true},Pulse={Pulse=true},
  Warm={WarmStart=true},Queue={QueueEvent=true},Connect={Connect=true}}
 local function declaration(name,rank,e,method,queued,fn)
  local phase=assert(phases[name],'ADAPTER_PHASE_UNKNOWN')
  assert(type(rank)=='number'and rank>=1 and rank<=100 and rank%1==0,'ADAPTER_PHASE_RANK')
  assert(#phase<16,'ADAPTER_PHASE_LIMIT')
  assert(fn and (name=='Render'or name=='Before')or not fn and methods[name][method],'ADAPTER_PHASE_METHOD')
  assert(queued==nil or name=='Before'and type(queued)=='boolean','ADAPTER_PHASE_QUEUE')
  for _,step in ipairs(phase)do assert(step.rank~=rank,'ADAPTER_PHASE_DUPLICATE')end
  return {rank=rank,entry=e,method=method,queued=queued,fn=fn}
 end
 local function install(name,step)
  local phase=phases[name];phase[#phase+1]=step;table.sort(phase,function(a,b)return a.rank<b.rank end)
 end
 function d.Barrier(name,rank,fn)
  assert(type(fn)=='function','ADAPTER_PHASE_BARRIER');install(name,declaration(name,rank,nil,nil,nil,fn))
 end
 function d.Each(name,visit)
  for _,step in ipairs(assert(phases[name],'ADAPTER_PHASE_UNKNOWN'))do visit(step.entry,step.method)end
 end
 function d.Render(data)
  for _,step in ipairs(phases.Render)do
   if step.fn then pcall(step.fn,data)
   elseif step.method=='Items'then d.Items(step.entry,data)
   else d.Call(step.entry,step.method,data.City)end
  end
 end
 function d.BeforeAll(c,item,checkQueued)
  for _,step in ipairs(phases.Before)do
   if step.fn then if not step.fn(c,item)then return false end
   else
    local queued;if step.queued then queued=checkQueued()end
    if not d.Before(step.entry,c,item,queued)then return false end
   end
  end
  return true
 end
 local function clone(v,seen)
  if type(v)~='table'then return v end
  seen=seen or {};if seen[v]then return seen[v]end
  local o={};seen[v]=o;for k,x in pairs(v)do o[k]=clone(x,seen)end;return o
 end
 function d.Add(name,owns,keys,construct,plan)
  local e={name=name,owns=owns,errors={},exports={}};d.entries[#d.entries+1]=e
  local pending={}
  for phase,spec in pairs(plan or {})do
   assert(type(spec)=='table'and #spec>=2 and #spec<=3,'ADAPTER_PHASE_SPEC')
   pending[phase]=declaration(phase,spec[1],e,spec[2],spec[3])
  end
  local before={};for _,key in ipairs(keys or {})do before[key]={value=ExposedMembers[key]}end
  local ok,api=pcall(construct)
  e.api=ok and type(api)=='table' and api or nil
  if not e.api then e.errors.New=ok and 'ADAPTER_API_INVALID' or tostring(api)end
  for _,key in ipairs(keys or {})do
   local current=ExposedMembers[key]
   if ok then e.exports[key]=current
   elseif current~=before[key].value then ExposedMembers[key]=before[key].value end
  end
  for phase,step in pairs(pending)do install(phase,step)end
  return e
 end
 function d.Call(e,method,...)
  if d.closed or not e or not e.api or e.unavailable then return false end
  local fn=e.api[method];if type(fn)~='function'then return true end
  local ok,value=pcall(fn,...);e.errors[method]=not ok and tostring(value) or nil
  return ok,value
 end
 function d.Items(e,data)
  if not e then return end
  if not e.api or e.unavailable or type(e.api.Items)~='function'then
   for _,key in ipairs({'ProjectItems','UnitItems'})do for _,item in ipairs(data[key] or {})do
    if (not e.api or e.unavailable) and e.owns(item)then item.Disabled=true;item.ToolTip='专业化界面暂不可用，请保留日志。'end
   end end
   return
  end
  -- Current adapters mutate list membership and row fields only. Copies are local
  -- to this UI render and never clone City/native handles or persist between calls.
  local projects,units=clone(data.ProjectItems),clone(data.UnitItems)
  local ok=d.Call(e,'Items',data)
  if not ok then
   data.ProjectItems=projects;data.UnitItems=units
   for _,key in ipairs({'ProjectItems','UnitItems'})do for _,item in ipairs(data[key] or {})do
    if e.owns(item)then item.Disabled=true;item.ToolTip='专业化界面暂不可用，请保留日志。'end
   end end
  end
 end
 function d.Before(e,c,item,queued)
  if not e or not e.api or e.unavailable or type(e.api.Before)~='function'then return not (e and e.owns(item))end
  local ok,result=d.Call(e,'Before',c,item,queued)
  if not ok then return not e.owns(item)end
  return not not result
 end
 function d.Hook(source,name,e,method,fn)
  local event=source and source[name];if not event or type(event.Add)~='function'then return end
  local active=true
  local callback=function(...)if active and not d.closed then
   if fn then pcall(fn,...)else d.Call(e,method,...)end
  end end
  d.hooks[#d.hooks+1]={event,callback}
  local ok,err=pcall(event.Add,callback)
  if not ok then
   active=false
   if e then e.unavailable=true;e.errors['Hook:'..name]=tostring(err)end
  end
 end
 function d.Close()
  if d.closed then return end;d.closed=true
  for _,h in ipairs(d.hooks)do if h[1].Remove then pcall(h[1].Remove,h[2])end end;d.hooks={}
  for _,e in ipairs(d.entries)do
   if e.api and type(e.api.Close)=='function'then pcall(e.api.Close)end
   for key,value in pairs(e.exports)do
   if ExposedMembers[key]==value then ExposedMembers[key]=nil end
  end end
 end
 return d
end

-- Production-only selected-view observer. One owner and one scalar row version;
-- module revisions remain the cheap gate, so idle publish adds no native reads.
function SPCSafeAdapters.NewViewObserver()
 local d={};local owner,ownerRevision;local ownerSeen=false
 local key,rowRevision,present;local rowSeen=false
 local rowToken,reference,refOwner,refCity,refX,refY,refToken,refChanges;local closed=false
 local function scalar(n)return type(n)=='number'and n==n and math.abs(n)<9007199254740992 end
 local function source(value)
  if not sameIdentity(owner,value)then owner=value;ownerRevision=nil;ownerSeen=false;rowSeen=false end
 end
 function d.SourceChanged(value)
  if closed then return false end
  source(value);local revision=value and value.revision
  if ownerSeen and ownerRevision==revision then return false end
  ownerSeen=true;ownerRevision=revision;return value~=nil
 end
 function d.Observe(value,cityKey,row)
  if closed then return false end
  source(value)
  local exists=row~=nil;local revision=type(row)=='table'and row.revision or nil
  if exists and not(type(revision)=='number'and revision>=0 and revision<9007199254740992 and revision%1==0)then
   rowSeen=false;return true -- unavailable version is never cached as confirmed
  end
  local token=type(row)=='table'and row.token or nil
  local r=type(row)=='table'and row.reference or nil;local ownerID,id,x,y,rt,changes
  if exists then
   if type(token)~='string'or #token==0 or #token>512 then rowSeen=false;return true end
   if type(r)=='table'then
    ownerID,id,x,y,rt,changes=r.owner,r.cityID,r.x,r.y,r.token,r.changes
    if not scalar(ownerID)or not scalar(id)or not scalar(x)or not scalar(y)
     or rt~=nil and(type(rt)~='string'or #rt>512)or changes~=nil and not scalar(changes)then rowSeen=false;return true end
    r='TABLE'
   elseif type(r)~='string'or #r==0 or #r>512 then rowSeen=false;return true end
  end
  local changed=not rowSeen or key~=cityKey or present~=exists or rowRevision~=revision or rowToken~=token
   or reference~=r or refOwner~=ownerID or refCity~=id or refX~=x or refY~=y or refToken~=rt or refChanges~=changes
  key=cityKey;present=exists;rowRevision=revision;rowToken=token;reference=r
  refOwner,refCity,refX,refY,refToken,refChanges=ownerID,id,x,y,rt,changes;rowSeen=true;return changed
 end
 function d.Close()closed=true;owner=nil;ownerRevision=nil;key=nil;rowRevision=nil;rowToken=nil;reference=nil;refToken=nil;rowSeen=false end
 return d
end
