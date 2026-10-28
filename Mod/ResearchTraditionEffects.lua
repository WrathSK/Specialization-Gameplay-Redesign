if not SPCIdentityEqual then include('IdentityEqual')end
local sameIdentity=SPCIdentityEqual.Same
include('RuntimeWork')
-- F2: transient, module-owned Science percentage. Store remains the age authority.
SPCResearchTraditionEffects={}
local M=SPCResearchTraditionEffects
local amounts={5,10,15,20,25}
local function name(n)return 'BUILDING_SPC_RESEARCH_TRADITION_'..n end
function M.Start(P,shared)
 local store=assert(shared.CityProgressionStore)
 local data={ready=false,changes=0};shared.ResearchTraditionEffects=data
 local pending={};local busy=false;local definitions
 local ownedIndex={};local markHealth;local writeGuard
 local strictCarrierReference=store.UsesNewAuthority==true
 local health=SPCRuntimeWork.NativeHealth(P,shared,data,function(id)return ownedIndex[id]==true end,function(scope)markHealth(scope)end,function()
  if strictCarrierReference then assert(writeGuard,'TRADITION_WRITE_WITNESS_UNAVAILABLE');writeGuard()end
 end)
 -- Fixed presentation-only slots; never effect/save authority or native-object storage.
 local records,byID,ownerGeneration={},{},{};local count=0;local generation=0;local sequence=0;local publicationDepth=0
 local function integer(v)return type(v)=='number'and v==v and v>=0 and v<1000000000 and v%1==0 end
 local function valid(f)
  return type(f)=='table'and getmetatable(f)==nil and integer(f.owner)and integer(f.cityID)and integer(f.x)and integer(f.y)
   and type(f.token)=='string'and #f.token>0 and #f.token<=256
   and type(f.specialization)=='string'and #f.specialization<=32 and integer(f.potential)and f.potential<=4
   and(f.active==nil or integer(f.active)and f.active<=4)and type(f.activeStatus)=='string'and #f.activeStatus<=64
   and(f.investmentPending==nil or type(f.investmentPending)=='boolean')
 end
 local function input(f)return table.concat({tostring(f.specialization),tostring(f.potential),tostring(f.active),tostring(f.activeStatus),tostring(f.investmentPending)},':')end
 local function location(f)return f.x..':'..f.y end
 local function invalidateRow(r,reason)
  if not r then return end
  r.serial=r.serial+1;r.attempt=nil;r.appliedStatus='UNKNOWN';r.applied=nil;r.gate='UNKNOWN';r.reason=reason
 end
 local function invalidate(scope,reason)
  local pid=type(scope)=='table'and scope.player or nil;local cid=type(scope)=='table'and scope.city or nil
  if pid==nil then generation=generation+1
  elseif cid==nil then ownerGeneration[pid]=(ownerGeneration[pid]or 0)+1
  else local k=byID[pid..':'..cid];local r=k and records[k]
   if r and r.owner==pid and r.cityID==cid then invalidateRow(r,reason)end
  end
 end
 local function safe(fn,...)
  local ok=pcall(fn,...);data.publicationError=not ok and 'TRADITION_PUBLICATION_UNAVAILABLE'or nil
 end
 local function bind(frame,f)
  if not valid(f)or f.owner~=frame.owner then return end
  frame.cityID=f.cityID
  local k=location(f);local r=records[k]
  if not r then if count>=2048 then return end;count=count+1;r={serial=0};records[k]=r end
  if r.owner~=f.owner or r.cityID~=f.cityID or r.token~=f.token then
   if r.owner~=nil and byID[r.owner..':'..r.cityID]==k then byID[r.owner..':'..r.cityID]=nil end
   r.owner,r.cityID,r.x,r.y,r.token=f.owner,f.cityID,f.x,f.y,f.token
   r.lastConfirmed=nil
  end
  local id=f.owner..':'..f.cityID;local previous=byID[id]
  if previous and previous~=k then invalidateRow(records[previous],'REFERENCE_REPLACED')end
  byID[id]=k;invalidateRow(r,'INPUT_UNAVAILABLE');r.attempt={}
  r.sequence=frame.sequence;frame.key,frame.row,frame.attempt,frame.serial=k,r,r.attempt,r.serial
  frame.input=input(f);frame.gate='UNKNOWN';frame.reason='ACTIVE_UNAVAILABLE';frame.errorReason='ACTIVE_UNAVAILABLE'
 end
 local function current(frame)
  return frame.row and records[frame.key]==frame.row and sameIdentity(frame.row.attempt,frame.attempt)
   and frame.row.serial==frame.serial and generation==frame.generation and(ownerGeneration[frame.owner]or 0)==frame.ownerGeneration
   and sameIdentity(shared.ResearchTraditionEffects,data)and sameIdentity(shared.CityProgressionStore,store)
 end
 local function publish(frame,known,value)
  if not current(frame)then return end
  local r=frame.row;r.generation=frame.generation;r.ownerGeneration=frame.ownerGeneration;r.input=frame.input
  r.gate=frame.gate;r.reason=known and frame.reason or frame.errorReason or 'APPLICATION_UNCONFIRMED'
  r.appliedStatus=known and 'KNOWN'or 'UNKNOWN';r.applied=known and value or nil
  if known then r.lastConfirmed=value end
 end
 function data.Applied(f)
  if not sameIdentity(shared.ResearchTraditionEffects,data)or not sameIdentity(shared.CityProgressionStore,store)then
   return {appliedStatus='UNAVAILABLE',gate='UNKNOWN',reason='SOURCE_REPLACED',requiredActive=4}
  end
  if not valid(f)then return {appliedStatus='UNOBSERVED',gate='UNKNOWN',reason='REFERENCE_UNAVAILABLE',requiredActive=4}end
  local r=records[location(f)]
  if not r or r.owner~=f.owner or r.cityID~=f.cityID or r.token~=f.token then
   return {appliedStatus=count>=2048 and 'UNAVAILABLE'or 'UNOBSERVED',gate='UNKNOWN',reason=count>=2048 and 'PUBLICATION_CAPACITY'or 'REFERENCE_UNOBSERVED',requiredActive=4}
  end
  local fresh=publicationDepth==0 and r.generation==generation and r.ownerGeneration==(ownerGeneration[f.owner]or 0)and r.input==input(f)
  return {appliedStatus=fresh and r.appliedStatus or 'UNKNOWN',applied=fresh and r.applied or nil,lastConfirmed=r.lastConfirmed,
   gate=fresh and r.gate or 'UNKNOWN',reason=fresh and r.reason or publicationDepth>0 and 'APPLICATION_BUSY'or 'INPUT_PENDING',requiredActive=4}
 end
 local function key(c,frame)
  local pid,id=c:GetOwner(),c:GetID() -- unchanged original diagnostic getters, after the business attempt
  if frame and not frame.row then safe(function()
   local k=byID[pid..':'..id];local r=k and records[k]
   if r and(r.sequence or 0)<=frame.sequence then invalidateRow(r,'FACTS_UNAVAILABLE')end
  end)end
  return pid..':'..id
 end
 local function defs()
  if definitions then return definitions end
  local out,nextOwned={},{}
  for _,n in ipairs(amounts)do
   local row=assert(P.Info('Buildings',name(n)),'TRADITION_CARRIER_MISSING')
   assert((row.InternalOnly==true or row.InternalOnly==1) and row.PrereqDistrict=='DISTRICT_CITY_CENTER'
    and row.CitizenSlots==0 and row.Housing==0,'TRADITION_CARRIER_INVALID')
   out[#out+1]={amount=n,id=row.Index};nextOwned[row.Index]=true
  end
  definitions=out;ownedIndex=nextOwned;return out
 end
 local function desired(pid,c,frame)
  assert(P.IsTestPlayer(pid) and c:GetOwner()==pid,'TRADITION_OWNER_UNKNOWN')
  local f
  if frame and strictCarrierReference then
   local facts=shared.EffectiveFacts;local reader=assert(facts.ReadWithCarrierReference,'TRADITION_WRITE_READER_UNAVAILABLE')
   local witness;f,witness=reader(pid,c)
   local stamp=assert(store.CarrierReferenceStamp,'TRADITION_WRITE_STAMP_UNAVAILABLE')
   local owner,id,x,y,token=f.owner,f.cityID,f.x,f.y,f.token
   local create,remove=P.CreateBuilding,P.RemoveBuilding
   writeGuard=function()
    assert(sameIdentity(shared.CityProgressionStore,store)and store.CarrierReferenceStamp==stamp
     and sameIdentity(shared.EffectiveFacts,facts)and facts.ReadWithCarrierReference==reader
     and sameIdentity(shared.ResearchTraditionEffects,data)and P.CreateBuilding==create and P.RemoveBuilding==remove,'TRADITION_WRITE_SOURCE_CHANGED')
    assert(type(witness)=='string'and stamp(owner,id,x,y,token)==witness,'TRADITION_WRITE_REFERENCE_CHANGED')
   end
   writeGuard()
  else f=shared.EffectiveFacts.Read(pid,c)end
  if frame then safe(bind,frame,f)end
  if f.specialization~='RESEARCH'then if frame then frame.gate='INELIGIBLE';frame.reason='NOT_RESEARCH'end;return 0 end
  assert(f.activeStatus=='KNOWN' and type(f.active)=='number','TRADITION_ACTIVE_UNKNOWN')
  if f.active<4 then if frame then frame.gate='INELIGIBLE';frame.reason='ACTIVE_BELOW_IV'end;return 0 end
  if frame then frame.gate='ELIGIBLE';frame.reason='HISTORY_UNAVAILABLE';frame.errorReason='HISTORY_UNAVAILABLE'end
  local t=store.ReadTradition(pid,c)
  if not t or t.state~='COUNTING'then if frame then frame.reason='TRADITION_NOT_COUNTING'end;return 0 end
  if frame then frame.reason='INTERVAL_NOT_CURRENT';frame.errorReason='INTERVAL_NOT_CURRENT'end
  assert(t.cursor==Game.GetCurrentGameTurn(),'TRADITION_INTERVAL_NOT_CURRENT')
  if frame then frame.reason='SPEED_UNAVAILABLE';frame.errorReason='SPEED_UNAVAILABLE'end
  local speed=GameInfo.GameSpeeds[GameConfiguration.GetGameSpeedType()]
  if frame and speed and speed.CostMultiplier then frame.reason='APPLIED'end
  return SPCResearchTradition.Shadow(t.age,assert(speed and speed.CostMultiplier,'TRADITION_SPEED_UNKNOWN')/100)
 end
 local function installed(c)
  local b=c:GetBuildings();local out={};local sum=0
  for _,d in ipairs(defs())do
   local has=P.HasBuilding(b,d.id);assert(type(has)=='boolean','TRADITION_CARRIER_UNKNOWN')
   local pillaged=false
   if has then pillaged=b:IsPillaged(d.id);assert(type(pillaged)=='boolean','TRADITION_CARRIER_STATE_UNKNOWN')end
   out[#out+1]={id=d.id,amount=d.amount,has=has,pillaged=pillaged}
   if has and not pillaged then sum=sum+d.amount end
  end
  return out,sum
 end
 function data.Read(pid,c)
  local want=desired(pid,c);local _,have=installed(c)
  return want,have
 end
 function data.Update(pid,c)
  if not data.ready or busy then return end
  busy=true;local previousGuard=writeGuard;writeGuard=nil
  sequence=sequence+1;publicationDepth=publicationDepth+1
  local frame={sequence=sequence,generation=generation,ownerGeneration=ownerGeneration[pid]or 0,owner=pid}
  local ok,err=pcall(function()
   defs();local want=desired(pid,c,frame);frame.errorReason='CARRIER_PREFLIGHT_UNAVAILABLE';local rows=installed(c) -- validate all inputs before writing
   frame.errorReason='APPLICATION_UNCONFIRMED'
   for _,v in ipairs(rows)do
    if v.has and (v.amount~=want or v.pillaged)then
     health.Remove(c,v.id)
     assert(P.HasBuilding(c:GetBuildings(),v.id)==false,'TRADITION_REMOVE_FAILED')
     v.has=false;data.changes=data.changes+1
    end
   end
   for _,v in ipairs(rows)do if v.amount==want and not v.has then
    health.Create(c,v.id)
    assert(P.HasBuilding(c:GetBuildings(),v.id)==true and c:GetBuildings():IsPillaged(v.id)==false,'TRADITION_CREATE_FAILED')
    v.has=true;v.pillaged=false;data.changes=data.changes+1
   end end
   local total=0;for _,v in ipairs(rows)do if v.has and not v.pillaged then total=total+v.amount end end
   safe(publish,frame,true,total)
  end)
  if not ok then safe(publish,frame,false)end
  writeGuard=previousGuard;busy=false
  local reported,why=pcall(function()
   if not ok then data.lastError={city=key(c,frame),reason=tostring(err)}
   elseif data.lastError and data.lastError.city==key(c)then data.lastError=nil end
  end)
  publicationDepth=publicationDepth-1
  if not reported then if not frame.row then generation=generation+1 end;error(why,0)end
 end
 function data.Mark(pid)
  if P.IsTestPlayer(pid)then invalidate({player=pid},'INPUT_PENDING');pending[pid]=true end
 end
 function data.Flush()
  if not data.ready or busy or not next(pending)then return end
  local work=pending;pending={}
  for pid in pairs(work)do
   local ok,err=pcall(store.VisitTradition,pid,function(c)data.Update(pid,c)end)
   if not ok then data.lastError={city='STORE',reason=tostring(err)}
   elseif data.lastError and data.lastError.city=='STORE' then data.lastError=nil end
  end
 end
 local function healthRun(scope)
  -- Update/Flush retain their established private guard. A synchronous native
  -- publish cannot consume another city's real cause while that guard is held.
  if busy then markHealth(scope);return end
  for pid,player in pairs(Players)do if P.IsTestPlayer(pid) and SPCRuntimeWork.Player(scope,pid)then
   if scope and scope.city~=nil then
    local c=player:GetCities():FindID(scope.city)
    if c and c:GetOwner()==pid then P.Count('city_scan');data.Update(pid,c)end
   else store.VisitTradition(pid,function(c)P.Count('city_scan');data.Update(pid,c)end)end
  end end
 end
 local auditHealth,mark,flushHealth=SPCRuntimeWork.NewAudit(P,shared,data,'ResearchTraditionEffects',healthRun)
 markHealth=function(scope)invalidate(scope,'HEALTH_PENDING');return mark(scope)end
 local function hook(n,fn)local e=P.Field(Events,n);if e and e.Add then e.Add(fn)end end
 SPCRuntimeWork.StartReady(P,shared,'ResearchTraditionEffects',function()
  definitions=nil;pending={};data.lastError=nil;data.ready=true
  for pid in pairs(Players)do data.Mark(pid)end
  data.Flush()
 end)
 -- Age is settled by Store's earlier listener. No new world/district scan.
 hook('PlayerTurnActivated',data.Mark)
 hook('GameCoreEventPublishComplete',data.Flush)
 store.RegisterExit('ResearchTradition',function(c,loss,ticket)
  local frame
  safe(function()
   local k=loss.origin.x..':'..loss.origin.y;local r=records[k]
   if r and r.owner==loss.origin.owner then
    invalidateRow(r,'EXIT_PENDING');r.gate='INELIGIBLE';sequence=sequence+1;r.sequence=sequence;r.attempt={}
    frame={key=k,row=r,attempt=r.attempt,serial=r.serial,owner=r.owner,ownerGeneration=ownerGeneration[r.owner]or 0,generation=generation,input=r.input,gate='INELIGIBLE',reason='EXIT_CONFIRMED'}
   end
  end)
  local ids={};for _,n in ipairs(amounts)do ids[#ids+1]=name(n)end
  local removed=store.RemoveOwned(c,loss,ids)
  safe(function()
   if frame and not busy and removed~=false and current(frame)and type(store.ReferenceToken)=='function'and type(store.IsExitCurrent)=='function'
    and store.ReferenceToken(c)==frame.row.token and store.IsExitCurrent('ResearchTradition',c,loss,ticket,function()return current(frame)end)==true and current(frame)then
    publish(frame,true,0)
   end
  end)
  data.lastError=nil -- one bounded diagnostic slot, never permanent state
 end)
end
