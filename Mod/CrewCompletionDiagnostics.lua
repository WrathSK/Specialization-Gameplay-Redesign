-- B413 disposable read-only evidence, never completion/admission authority.
-- Remove the protected Gameplay/UI attachment blocks and this file to retire.
if type(SPCCrewCompletionDiagnostics)=='table'and SPCCrewCompletionDiagnostics.VERSION==413 then return end
SPCCrewCompletionDiagnostics={VERSION=413,ENABLED=true,TURN_LIMIT=6,EVENT_LIMIT=64,PRELUDE_LIMIT=8,
 VISIT_LIMIT=256,SAMPLE_LIMIT=32,ROW_LIMIT=192,CITY_LIMIT=8,ORDER_LIMIT=8,ARG_LIMIT=12}
local M=SPCCrewCompletionDiagnostics
local instance;local used=false
local function integer(v)return type(v)=='number'and v>=0 and v<9007199254740991 and v%1==0 end
local function field(o,k)local ok,v=pcall(function()return o and o[k]end);if ok then return v end end
local function atom(v,limit)
 local t=type(v)
 if t=='nil'then return 'NIL' end
 if t=='boolean'then return v and 'true'or 'false'end
 if t=='number'then return v==v and v>-math.huge and v<math.huge and string.format('%.17g',v)or 'NONFINITE'end
 if t=='string'then
  if #v<=(limit or 72)and not v:find('[^%w_:%-%.|]')then return v end
  return 'REDACTED_STRING_'..#v
 end
 return 'OMITTED_'..t -- never stringify native tables/userdata/functions
end
function M.Stop()if instance then instance.Stop('EXPLICIT_STOP')end end
function M.Start(P,side)
 if used then return instance end
 if not M.ENABLED or (side~='GAMEPLAY'and side~='UI')then return end
 local logger=SPCExpeditionTrainingDiagnostics
 if type(logger)~='table'or logger.ENABLED==false or type(logger.New)~='function'then return end
 local ok,trace=pcall(logger.New,P,'CREW_PROOF_'..side)
 if not ok or type(trace)~='table'or trace.id=='DISABLED'or type(trace.Record)~='function'then return end
 used=true
 local live,busy=true,false;local hooks={};local cities,pending={},{};local cityCount=0
 local rows,events,visits,samples=0,0,0,0;local localID;local qualified=false;local checks=0
 local firstTurn;local prelude=0;local observation=0;local afterAttached=false
 local api={}
 local function count()if type(P.Count)=='function'then pcall(P.Count,'observer_native_attempt')end end
 local function read(o,name,...)
  count();local args={...}
  return pcall(function()local fn=o and o[name];assert(type(fn)=='function');return fn(o,unpack(args))end)
 end
 local function record(stage,data)
  observation=observation+1;data.observerSide=side;data.observationSeq=observation
  pcall(trace.Record,stage,data)
 end
 function api.Stop(reason)
  if not live then return end;live=false
  -- Never mutate a native listener list while it may be dispatching. The
  -- fixed callbacks stay inert until this Lua context is destroyed.
  pending={};cities={}
  record('CREW_PROOF_STATUS',{point='STOP',reason=reason,eventCount=events,eventTotal=rows,
   eventTruncated=reason:find('LIMIT',1,true)~=nil})
 end
 function api.Stats()return {live=live,rows=rows,events=events,visits=visits,samples=samples,cities=cityCount,hooks=#hooks,prelude=prelude,pending=next(pending)~=nil}end
 local function emit(stage,data)
  if not live then return end
  if rows>=M.ROW_LIMIT then api.Stop('ROW_LIMIT');return end
  rows=rows+1;record(stage,data)
 end
 local function now()
  local ok,t=pcall(Game.GetCurrentGameTurn)
  if not ok or not integer(t)then return end
  if firstTurn and (t<firstTurn or t>=firstTurn+M.TURN_LIMIT)then api.Stop('WINDOW_END');return end
  return t
 end
 local function owner(pid)
  if not integer(pid)then return end
  if localID==nil then local ok,id=pcall(Game.GetLocalPlayer);if ok and integer(id)then localID=id end end
  if pid~=localID then return end
  if not qualified then
   if checks>=8 then api.Stop('OWNER_CHECK_LIMIT');return end
   checks=checks+1;local ok,v=pcall(P.IsTestPlayer,pid);qualified=ok and v==true
  end
  return qualified
 end
 local function project(index)
  local ok,row=pcall(P.Info,'Projects',index)
  local name=ok and field(row,'ProjectType')
  if type(name)=='string'and name:match('^PROJECT_SPC_CREW_%d')then return name end
 end
 local function city(pid,id)
  if visits>=M.VISIT_LIMIT then api.Stop('VISIT_LIMIT');return end
  visits=visits+1
  local ok,c=pcall(function()count();local collection=Players[pid]:GetCities();count();return collection:FindID(id)end)
  if not ok or not c then return end
  local ok,value=read(c,'GetOwner');if not ok or value~=pid then return end
  return c
 end
 local function rawOrders(c)
  local key=field(SPCCrewModel,'ORDER_PROPERTY')
  if type(key)~='string'then return false,'MODEL_UNAVAILABLE'end
  return read(c,'GetProperty',key)
 end
 -- Published owner state is only an observational relevance hint. Never read
 -- cities/properties just to discover whether an ordinary event is related.
 local function related(key,pid,id)
  if cities[key]then return true end
  local shared=ExposedMembers and ExposedMembers.SPC_P0
  local view=field(field(field(shared,'CrewProjects'),'views'),key)
  if field(view,'owner')~=pid or field(view,'city')~=id then return false end
  for _,name in ipairs({'reserved','queued','paused'})do
   local n=field(view,name);if integer(n)and n>0 then return true end
  end
  local retained=field(view,'retained')
  return type(retained)=='table'and next(retained)~=nil
 end
 local function relevant(name,a)
  local pid,id=a[1],a[2]
  if not integer(pid)or not integer(id)then return end
  local key=pid..':'..id
  local kind=name=='CityProjectCompleted'and project(a[3])or nil
  if not kind and not related(key,pid,id)then return end
  -- Queueing/ordinary construction gets only a small bounded prelude. Once
  -- full,it performs no native sampling;completion retains the remaining cap.
  if not firstTurn and not kind and prelude>=M.PRELUDE_LIMIT then return end
  if not owner(pid)then return end
  local t=now();if not t then return end
  if events>=M.EVENT_LIMIT then api.Stop('EVENT_LIMIT');return end
  -- A verified project type on this event arms observation,not grant authority.
  -- Unknown later arguments/ordinary production events imply no completion or
  -- cancellation semantics and cannot start the six-turn completion window.
  if kind then firstTurn=firstTurn or t
  elseif not firstTurn then prelude=prelude+1 end
  local c=city(pid,id)
  if not c then if kind then return 'CITY_UNAVAILABLE',kind,false,'CITY_UNAVAILABLE'end;return end
  local ok,raw=rawOrders(c)
  if not cities[key]then
   if cityCount>=M.CITY_LIMIT then api.Stop('CITY_LIMIT');return end
   cityCount=cityCount+1;cities[key]=true
  end
  return c,kind,ok,raw
 end
 local function snapshot(point,phase,pid,id,kind,c,ordersOK,raw,sample)
  if not live then return end
  local t=now();if not t then return end
  local list=ordersOK and type(raw)=='table'and field(raw,'orders')or nil
  local source=type(raw)=='table'and field(raw,'source')or nil
  local receiptKey=field(SPCCrewModel,'RECEIPT_PROPERTY')
  local receiptOK,receipt=false,nil
  if type(receiptKey)=='string'then receiptOK,receipt=read(Players[pid],'GetProperty',receiptKey)end
  local water=receiptOK and type(receipt)=='table'and field(receipt,'water')or nil
  local outstanding=receiptOK and type(receipt)=='table'and field(receipt,'pending')or nil
  local batch={};local cut=false
  if type(list)=='table'then
   for i=1,M.ORDER_LIMIT do
    local row=field(list,i);if row==nil then break end
    local itemProject=field(row,'project');kind=kind or (type(itemProject)=='string'and itemProject:match('^PROJECT_SPC_CREW_%d')and itemProject)
    local serial=field(row,'serial');local pendingRow
    if type(source)=='string'and integer(serial)and serial>0 and type(outstanding)=='table'then
     local keyOK,key=pcall(function()return SPCCrewModel.ReceiptKey(source,serial)end)
     if keyOK then pendingRow=field(outstanding,key)end
    end
    batch[#batch+1]=table.concat({'order',atom(serial),atom(field(row,'stage')),atom(itemProject),atom(field(row,'base')),
     atom(field(row,'capacity')),atom(field(row,'price')),atom(field(pendingRow,'stage')),atom(field(pendingRow,'count'))},':')
   end
   cut=field(list,M.ORDER_LIMIT+1)~=nil
  end
  local packed=table.concat(batch,'|')
  if #packed>1700 then packed='ORDER_BATCH_REDACTED';cut=true end
  local data={owner=pid,city=id,point=point,phase=phase,projectType=kind,
   readStatus=ordersOK and (raw==nil and 'NO_ORDER_RECORD'or type(raw)=='table'and 'RAW_ORDER_RECORD'or 'INVALID_ORDER_TYPE')or 'ORDER_READ_ERROR',
   recordType=type(raw),eventBatch=packed~=''and packed or 'NO_ORDER_ROWS',eventTruncated=cut,
   writerState=table.concat({'source',atom(source,100),'serial',atom(field(raw,'serial')),'version',atom(field(raw,'version')),
    'owner',atom(field(raw,'owner')),'x',atom(field(raw,'x')),'y',atom(field(raw,'y'))},':'),
   controlState=table.concat({'receipt',receiptOK and atom(field(receipt,'version'))or 'READ_ERROR',
    'water',atom(kind and field(water,kind))},':')}
  local shared=ExposedMembers and ExposedMembers.SPC_P0
  local errors=field(field(shared,'CrewProjects'),'errors');local reason=field(errors,pid..':'..id)
  if type(reason)=='string'then data.errorCode=reason:match('CREW_[A-Z0-9_]+')or 'UNCLASSIFIED'end
  for _,key in ipairs({'writerState','controlState'})do if #data[key]>256 then data[key]='EXCERPT_REDACTED';data.eventTruncated=true end end
  if sample and c=='CITY_UNAVAILABLE'then data.reader='CITY_UNAVAILABLE'
  elseif sample then
   if samples>=M.SAMPLE_LIMIT then api.Stop('SAMPLE_LIMIT');return end
   samples=samples+1
   local reader=ExposedMembers and ExposedMembers.SPC_CrewNativeRead
   if type(reader)~='function'then data.reader='UNAVAILABLE'
   else
    count();local ok,q=pcall(reader,pid,id)
    data.reader=not ok and 'READ_ERROR'or type(q)~='table'and 'INVALID_TYPE'or
     field(q,'owner')==pid and field(q,'city')==id and field(q,'turn')==t and 'RETURNED_CURRENT'or 'STALE_OR_WRONG_SCOPE'
    if data.reader=='RETURNED_CURRENT'then
     data.queueSize='NOT_EXPORTED';data.queued=kind and field(field(q,'projects'),kind)
     data.completed=kind and field(field(q,'completed'),kind);data.nativeProgress=kind and field(field(q,'progress'),kind)
     data.currentHash=field(q,'currentHash');data.activitySampleTurn=field(q,'turn')
    end
   end
  else data.reader='NOT_SAMPLED'end
  emit('CREW_PROOF_STATE',data)
 end
 local function rawEvent(name,phase,n,a)
  if not live then return end
  local c,kind,ok,raw=relevant(name,a);if not c or not live then return end
  local t=now();if not t then return end;events=events+1
  local parts={}
  for i=1,math.min(n,M.ARG_LIMIT)do
   local v=a[i];local text=type(v)=='string'and ('REDACTED_STRING_'..#v)or atom(v)
   parts[#parts+1]=i..':'..type(v)..':'..text
  end
  emit('CREW_PROOF_EVENT',{owner=a[1],city=a[2],point=name,phase=phase,projectType=kind,
   eventCount=n,eventBatch=table.concat(parts,'|'),eventTruncated=n>M.ARG_LIMIT})
  snapshot(name,phase,a[1],a[2],kind,c,ok,raw,name=='CityProjectCompleted')
  if not live then return end
  if not firstTurn and prelude==M.PRELUDE_LIMIT then
   emit('CREW_PROOF_STATUS',{point='PRELUDE_LIMIT',reason='WAITING_FOR_CREW_COMPLETION',eventTruncated=true})
  end
  if live and phase~='BEFORE_CREW'and c~='CITY_UNAVAILABLE'then pending[a[1]..':'..a[2]]={owner=a[1],city=a[2],project=kind}end
 end
 local function hook(name,phase)
  local event=Events and Events[name];local add=field(event,'Add')
  if type(add)~='function'then emit('CREW_PROOF_STATUS',{point='HOOK_UNAVAILABLE',reason=name});return false end
  local fn=function(...)
   if not live or busy then return end
   if not M.ENABLED then api.Stop('DISABLED');return end
   local n=select('#',...);local a={};for i=1,math.min(n,M.ARG_LIMIT)do a[i]=select(i,...)end
   busy=true;local ok=pcall(rawEvent,name,phase,n,a);busy=false
   if not ok then api.Stop('OBSERVER_ERROR')end
  end
  local ok=pcall(add,fn);if ok then hooks[#hooks+1]=fn
  else emit('CREW_PROOF_STATUS',{point='HOOK_UNAVAILABLE',reason=name})end
  return ok
 end
 local function followup()
  if not live or busy or not next(pending)then return end
  if not M.ENABLED then api.Stop('DISABLED');return end
  if not now()then return end
  local work=pending;pending={};busy=true
  local ok=pcall(function()
   for _,v in pairs(work)do
    if not live then break end
    local c=city(v.owner,v.city)
    if c then local good,raw=rawOrders(c);snapshot('FIRST_RELATED_PUBLISH','FOLLOWUP',v.owner,v.city,v.project,c,good,raw,true)end
   end
  end)
  busy=false;if not ok then api.Stop('OBSERVER_ERROR')end
 end
 if side=='GAMEPLAY'then hook('CityProjectCompleted','BEFORE_CREW')
 else hook('CityProjectCompleted','UI_ARRIVAL')end
 for _,name in ipairs({'CityProductionChanged','CityProductionCompleted'})do hook(name,side=='GAMEPLAY'and 'GP_ARRIVAL'or 'UI_ARRIVAL')end
 function api.After()
  if live and side=='GAMEPLAY'and not afterAttached then
   afterAttached=true;if hook('CityProjectCompleted','AFTER_CREW')then emit('CREW_PROOF_STATUS',{point='AFTER_ATTACHED',reason='READ_ONLY_AFTER_CREW',eventPublishCount=#hooks})end
  end
 end
 local event=Events and Events.GameCoreEventPublishComplete
 local add=field(event,'Add')
 if type(add)=='function'then
  local ok=pcall(add,followup);if ok then hooks[#hooks+1]=followup
  else emit('CREW_PROOF_STATUS',{point='HOOK_UNAVAILABLE',reason='GameCoreEventPublishComplete'})end
 else emit('CREW_PROOF_STATUS',{point='HOOK_UNAVAILABLE',reason='GameCoreEventPublishComplete'})end
 instance=api
 emit('CREW_PROOF_STATUS',{point='ARMED',reason='READ_ONLY_NO_GRANT_AUTHORITY',eventPublishCount=#hooks,eventCount=M.EVENT_LIMIT,eventTotal=M.ROW_LIMIT,
  eventBatch='args:'..M.ARG_LIMIT..'|samples:'..M.SAMPLE_LIMIT..'|visits:'..M.VISIT_LIMIT..'|cities:'..M.CITY_LIMIT..'|turns:'..M.TURN_LIMIT..'|prelude:'..M.PRELUDE_LIMIT})
 return api
end
