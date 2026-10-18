include('CrewModel')
include('ExpeditionTrainingDiagnostics')
-- B236: paid native projects; saved admission/grant proof; native living inventory.
-- This writer never guesses a source from a new unit's position or name.
SPCCrewProjects={}
function SPCCrewProjects.Start(P,shared)
 local M=SPCCrewModel;local cp,same=M.Copy,M.Same;local store=assert(shared.CityProgressionStore)
 local d={ready=false,busy=false,errors={},views={},revision=0};shared.CrewProjects=d
 local dirty,settling,failed,issued={}, {}, {}, {};local knownUnits={};local lastRequest,lastReply;local trace=SPCExpeditionTrainingDiagnostics.New(P,'CREW')
 local function key(pid,id)return pid..':'..id end
 local function city(pid,id)return Players[pid] and Players[pid]:GetCities():FindID(id)end
 local function mark(pid,id)if P.IsTestPlayer(pid) and M.Int(id)then dirty[key(pid,id)]={pid,id}end end
 local function markPlayer(pid)if P.IsTestPlayer(pid)then for _,c in Players[pid]:GetCities():Members()do mark(pid,c:GetID())end end end
 local function code(e)return tostring(e):match('CREW_[A-Z_]+') or 'CREW_READ_UNAVAILABLE'end
 local function observe(stage,pid,c,v)
  v=v or {};v.owner=pid;v.city=c and c:GetID();trace.Record(stage,v)
 end
 local function source(pid,c)
  assert(c and c:GetOwner()==pid and P.IsTestPlayer(pid),'CREW_OWNER_CHANGED')
  local a=store.HistoricalReference(c)
  assert(type(a.token)=='string' and a.owner==pid and a.x==c:GetX() and a.y==c:GetY(),'CREW_SOURCE_UNAVAILABLE');return a
 end
 local function speed()local r=GameInfo.GameSpeeds[GameConfiguration.GetGameSpeedType()];return assert(r and r.CostMultiplier,'CREW_SPEED_UNKNOWN')end
 local function orders(pid,c)
  local a=source(pid,c);local v=c:GetProperty(M.ORDER_PROPERTY)
  if v==nil then return {version=1,source=a.token,x=a.x,y=a.y,owner=pid,serial=0,orders={}},nil,a end
  assert(type(v)=='table' and v.version==1 and v.source==a.token and v.x==a.x and v.y==a.y and M.Int(v.serial)
   and M.Int(v.owner) and type(v.orders)=='table' and #v.orders<=2,'CREW_ORDER_HISTORY_INVALID')
  if v.owner~=pid then assert(#v.orders==0,'CREW_PREVIOUS_OWNER_ORDER_HELD');local n=cp(v);n.owner=pid;return n,v,a end
  local seen={}
  for _,o in ipairs(v.orders)do
   local tier,ratio=M.Parse(o.project)
   assert(type(o)=='table' and tier and tier==o.tier and ratio==o.ratio and M.Int(o.serial) and o.serial<=v.serial
    and not seen[o.serial] and M.Int(o.base) and M.Int(o.capacity) and o.capacity>0
    and (o.stage=='RESERVED' or o.stage=='QUEUED' or o.stage=='CALLING' or o.stage=='HELD'),'CREW_ORDER_HISTORY_INVALID')
   seen[o.serial]=true
  end
  return cp(v),v,a
 end
 local function save(c,old,v)
  assert(same(c:GetProperty(M.ORDER_PROPERTY),old),'CREW_STALE_ORDER')
  local ok=pcall(P.SetProperty,c,M.ORDER_PROPERTY,cp(v))
  assert(same(c:GetProperty(M.ORDER_PROPERTY),v),'CREW_ORDER_WRITE_UNCONFIRMED')
  return ok -- readback, not a setter's return, establishes the saved value
 end
 local function queue(pid,c)
  local r=assert(ExposedMembers.SPC_CrewNativeRead,'CREW_UI_READER_UNAVAILABLE')(pid,c:GetID())
  assert(type(r)=='table' and r.owner==pid and r.city==c:GetID() and r.x==c:GetX() and r.y==c:GetY()
   and r.turn==Game.GetCurrentGameTurn() and type(r.projects)=='table' and type(r.completed)=='table','CREW_QUEUE_UNKNOWN')
  local count=0;for id,n in pairs(r.projects)do assert(M.Parse(id) and M.Int(n),'CREW_QUEUE_UNKNOWN');count=count+n end
  assert(count<=2,'CREW_QUEUE_OVER_CAPACITY');return r,count
 end
 function d.Unit(pid,u)
  assert(u and u:GetOwner()==pid,'CREW_OWNER_CHANGED')
  local row=P.Info('Units',u:GetType());return cp(M.ValidateUnit(u:GetProperty(M.UNIT_PROPERTY),pid,row and row.UnitType))
 end
 function d.Inventory(pid)
  local counts={};local seen={};local units={}
  for _,u in Players[pid]:GetUnits():Members()do
   local row=P.Info('Units',u:GetType())
   if row and P.CrewBase(row.UnitType)then
    local v=d.Unit(pid,u);assert(not seen[v.grant],'CREW_DUPLICATE_GRANT_UNIT');seen[v.grant]=true;units[u:GetID()]=v.source
    counts[v.source]=(counts[v.source] or 0)+1
   end
  end
  knownUnits[pid]=units;return counts
 end
 local function receipts(pid)
  local v=Players[pid]:GetProperty(M.RECEIPT_PROPERTY) or {};assert(type(v)=='table','CREW_RECEIPT_INVALID')
  for id,r in pairs(v)do assert(M.Parse(id) and type(r)=='table' and M.Int(r.count) and r.count>0
   and type(r.source)=='string' and (r.stage=='CALLING' or r.stage=='BOUND')
   and (r.stage=='CALLING' or M.Int(r.unitID)),'CREW_RECEIPT_INVALID')end
  return cp(v)
 end
 local function receiptSave(pid,old,v)
  assert(same(Players[pid]:GetProperty(M.RECEIPT_PROPERTY) or {},old),'CREW_STALE_RECEIPT')
  pcall(P.SetProperty,Players[pid],M.RECEIPT_PROPERTY,cp(v))
  assert(same(Players[pid]:GetProperty(M.RECEIPT_PROPERTY),v),'CREW_RECEIPT_WRITE_UNCONFIRMED')
 end
 local function safe(pid,id,fn)
  local ok,err=pcall(fn);local k=key(pid,id)
  if not ok then d.errors[k]=code(err);observe('CREW_HELD',pid,city(pid,id),{reason=code(err)})else d.errors[k]=failed[k] end
  return ok,err
 end
 local function qualified(pid,c,a)
  local f=shared.EffectiveFacts.Read(pid,c)
  assert(f.token==a.token and f.activeStatus=='KNOWN' and not f.investmentPending,'CREW_QUALIFICATION_UNKNOWN')
  if f.specialization~='INDUSTRY' or f.active<3 then return nil,f.active end
  local N=0
  if f.active==4 then local h=shared.IndustryHistory.Read(pid,c);assert(h.cityState~='UNKNOWN','CREW_N_UNKNOWN');N=h.N end
  return M.Multiplier(f.active,N),f.active,N
 end
 local function marker(c,id,wanted)
  local row=assert(P.Info('Buildings',id),'CREW_MARKER_MISSING');local b=c:GetBuildings();local has=P.HasBuilding(b,row.Index)
  assert(type(has)=='boolean','CREW_MARKER_UNKNOWN')
  if has~=wanted then
   if wanted then P.CreateBuilding(c:GetBuildQueue(),row.Index)else P.RemoveBuilding(b,row.Index)end
   assert(P.HasBuilding(b,row.Index)==wanted,'CREW_MARKER_WRITE_UNCONFIRMED')
  end
 end
 local function reconcile(pid,c,v,old,q)
  -- Queue removal is cancellation, never a refund. A proved completion or
  -- in-flight admission must not be mistaken for removal during nested events.
  local changed=false;local keep={};local available=cp(q.projects)
  for _,o in ipairs(v.orders)do
   if o.stage=='CALLING' or o.stage=='HELD'then keep[#keep+1]=o
   elseif (available[o.project] or 0)>0 then
    available[o.project]=available[o.project]-1
    if o.stage~='QUEUED'then o.stage='QUEUED';changed=true end;keep[#keep+1]=o
   elseif o.stage=='RESERVED' and issued[key(pid,c:GetID())..':'..o.serial]then keep[#keep+1]=o
   elseif (q.completed[o.project] or -1)>o.base then
    o.stage='HELD';changed=true;keep[#keep+1]=o -- missed native completion cannot be reconstructed as a grant
   else changed=true end
  end
  if changed then v.orders=keep;save(c,old,v);old=cp(v)end
  return v,old
 end
 local function audit(pid,id,inventory)
  local c=city(pid,id);local k=key(pid,id)
  if not c or c:GetOwner()~=pid then d.views[k]=nil;return end
  local a=source(pid,c);local v,old=orders(pid,c);local q,n=queue(pid,c)
  v,old=reconcile(pid,c,v,old,q)
  local count=assert(inventory)[a.token] or 0;local held=failed[k]
  for _,o in ipairs(v.orders)do if o.stage=='HELD' or o.stage=='CALLING'then held=true end end
  for _,r in pairs(receipts(pid))do if r.stage=='CALLING' and r.source==a.token then held=true end end
  local ratio,active,N=qualified(pid,c,a)
  local available=not held and count+#v.orders<2 and ratio~=nil
  local wanted={}
  for tier in ipairs(M.CAPACITY)do for _,price in ipairs(M.RATIOS)do
   local idp=M.Project(tier,price,speed())
   local admitted=false;for _,o in ipairs(v.orders)do if o.project==idp and o.stage~='HELD' and o.stage~='CALLING'then admitted=true end end
   local value=admitted or available and price==ratio and tier<=(active==4 and 5 or 3)
   marker(c,M.Marker(tier,price),value);wanted[idp]=not not (available and price==ratio and tier<=(active==4 and 5 or 3))
  end end
  marker(c,'BUILDING_SPC_CREW_PROJECT_ACCESS',false) -- exact retired B044 access only
  local view={owner=pid,city=id,source=a.token,active=active,N=N,ratio=ratio,count=count,reserved=#v.orders,held=not not held,allowed=wanted}
  if not same(d.views[k],view)then d.views[k]=view;d.revision=d.revision+1;observe('CREW_STATE',pid,c,{count=count,queued=#v.orders,wanted=available,expected=ratio,phase=held and 'HELD' or 'READY'})end
 end
 local function initialize()
  if d.ready then return true end
  local s=store.HistoryStartStatus();if s=='WAITING' or s=='HELD'then return false end
  d.ready=true;for pid in pairs(Players)do markPlayer(pid)end;return true
 end
 function d.Flush()
  if d.busy or not initialize()then return end;d.busy=true
  local work=dirty;dirty={};local inventory={}
  for _,v in pairs(work)do local pid,id=v[1],v[2]
   safe(pid,id,function()
    if not inventory[pid]then inventory[pid]=d.Inventory(pid)end
    audit(pid,id,inventory[pid])
   end)
  end;d.busy=false
 end
 function d.Refresh(pid,id)mark(pid,id);d.Flush()end
 function d.Audit(scope)if scope and scope.player then markPlayer(scope.player)else for pid in pairs(Players)do markPlayer(pid)end end;d.Flush()end
 function d.Request(pid,p)
  if not initialize() or d.busy or not P.IsTestPlayer(pid) or type(p.Token)~='string' or #p.Token>100 then return end
  if p.Token==lastRequest then ExposedMembers.SPC_CrewReply=lastReply;return end
  d.busy=true
  local ok,out=safe(pid,p.CityID,function()
   local c=assert(city(pid,p.CityID),'CREW_CITY_UNKNOWN');local v,old,a=orders(pid,c);local q,n=queue(pid,c)
   v,old=reconcile(pid,c,v,old,q)
   if p.Action=='RESERVE'then
    assert(not failed[key(pid,p.CityID)],'CREW_SOURCE_HELD')
    local tier,ratio=M.Parse(p.Project);assert(tier,'CREW_PROJECT_UNKNOWN')
    local wanted,active=qualified(pid,c,a);assert(ratio==wanted and tier<=(active==4 and 5 or 3),'CREW_PROJECT_NOT_CURRENT_PRICE')
    local count=d.Inventory(pid)[a.token] or 0
    for _,r in pairs(receipts(pid))do assert(r.source~=a.token or r.stage~='CALLING','CREW_GRANT_UNRESOLVED')end
    for _,o in ipairs(v.orders)do assert(o.stage=='QUEUED','CREW_ORDER_PENDING')end
    assert(count+#v.orders<2 and n==#v.orders,'CREW_CAPACITY_FULL_OR_QUEUE_UNKNOWN')
    local row=P.Info('Projects',p.Project);local capacity=M.Amount(tier,speed());local price=M.Cost(tier,ratio,speed())
    assert(q.costs[p.Project]==price,'CREW_NATIVE_COST_MISMATCH')
    local base=q.completed[p.Project];assert(M.Int(base),'CREW_NATIVE_COMPLETION_COUNTER_UNKNOWN')
    v.serial=v.serial+1;local o={serial=v.serial,project=p.Project,tier=tier,ratio=ratio,capacity=capacity,price=price,
     base=base,stage='RESERVED',turn=Game.GetCurrentGameTurn(),before=q.projects[p.Project] or 0}
    v.orders[#v.orders+1]=o;save(c,old,v);issued[key(pid,p.CityID)..':'..o.serial]=true
    observe('CREW_ORDER',pid,c,{reservation=o.serial,nativeCost=price,expected=capacity,phase='RESERVED'})
    return {reservation=o.serial,project=p.Project,before=o.before,base=o.base}
   end
   local index;for i,o in ipairs(v.orders)do if o.serial==p.Reservation then index=i;break end end
   if not index then return {finished=true}end
   local o=v.orders[index]
   if p.Action=='CANCEL'then
    assert(o.stage=='RESERVED' and (q.projects[o.project] or 0)==o.before and q.completed[o.project]==o.base,'CREW_CANCEL_UNCONFIRMED')
    table.remove(v.orders,index);save(c,old,v);issued[key(pid,p.CityID)..':'..o.serial]=nil;return {cancelled=true}
   end
   assert(p.Action=='CONFIRM','CREW_REQUEST_UNKNOWN')
   assert(o.stage=='QUEUED' or o.stage=='RESERVED','CREW_CONFIRM_HELD')
   assert(o.stage=='QUEUED','CREW_QUEUE_NOT_CONFIRMED') -- reconciliation assigned this actual queue entry, even if an earlier same-type order just completed
   issued[key(pid,p.CityID)..':'..o.serial]=nil;return {confirmed=true}
  end)
  d.busy=false
  local reply=ok and out or {error=code(out)};reply.token=p.Token;reply.owner=pid;reply.city=p.CityID
  lastRequest=p.Token;lastReply=reply;ExposedMembers.SPC_CrewReply=reply;mark(pid,p.CityID);d.Flush()
 end
 local function completion(pid,id,index)
  if not initialize() or not P.IsTestPlayer(pid)then return end
  local row=P.Info('Projects',index);local tier=row and M.Parse(row.ProjectType);if not tier then return end
  local k=key(pid,id);if settling[k]then return end;settling[k]=true
  local ok=safe(pid,id,function()
   local c=assert(city(pid,id),'CREW_CITY_UNKNOWN');local v,old,a=orders(pid,c);local q=queue(pid,c)
   local native=q.completed[row.ProjectType];assert(M.Int(native),'CREW_NATIVE_COMPLETION_COUNTER_UNKNOWN')
   local all=receipts(pid);local prior=all[row.ProjectType]
   if prior and native<=prior.count then return end -- duplicate/reordered notification, no second grant
   local which;for i,o in ipairs(v.orders)do if o.project==row.ProjectType then which=i;break end end
   assert(which,'CREW_COMPLETION_WITHOUT_ADMISSION');local o=v.orders[which]
   assert((o.stage=='QUEUED' or o.stage=='RESERVED') and native>o.base,'CREW_COMPLETION_NOT_PROVED')
   assert(not prior or prior.stage=='BOUND','CREW_PREVIOUS_GRANT_UNRESOLVED')
   assert(native==(prior and prior.count or o.base)+1,'CREW_COMPLETION_SEQUENCE_AMBIGUOUS')
   local live=d.Inventory(pid)[a.token] or 0;assert(live<2,'CREW_COMPLETION_CAPACITY_FULL')
   -- Persist BEFORE native creation. A missing return or binding write never replays InitUnit.
   o.stage='CALLING';save(c,old,v);old=cp(v)
   local next=cp(all);next[row.ProjectType]={count=native,source=a.token,stage='CALLING'};receiptSave(pid,all,next)
   local grant=pid..':'..row.ProjectType..':'..native
   assert(source(pid,c).token==a.token,'CREW_SOURCE_CHANGED_DURING_GRANT')
   local u=UnitManager.InitUnit(pid,'UNIT_SPC_CREW_'..M.CAPACITY[tier],c:GetX(),c:GetY())
   assert(u and u:GetOwner()==pid and M.Int(u:GetID()) and Players[pid]:GetUnits():FindID(u:GetID()),'CREW_GRANT_RETURN_UNKNOWN')
   assert(source(pid,c).token==a.token,'CREW_SOURCE_CHANGED_DURING_GRANT')
   assert(P.Info('Units',u:GetType()).UnitType=='UNIT_SPC_CREW_'..M.CAPACITY[tier],'CREW_GRANT_TYPE_MISMATCH')
   assert(u:GetProperty(M.UNIT_PROPERTY)==nil,'CREW_GRANT_ALREADY_BOUND')
   local binding={version=1,owner=pid,source=a.token,x=a.x,y=a.y,tier=tier,capacity=o.capacity,grant=grant}
   pcall(P.SetProperty,u,M.UNIT_PROPERTY,cp(binding));assert(same(u:GetProperty(M.UNIT_PROPERTY),binding),'CREW_BINDING_UNCONFIRMED')
   local bound=cp(next);bound[row.ProjectType].stage='BOUND';bound[row.ProjectType].unitID=u:GetID();receiptSave(pid,next,bound)
   table.remove(v.orders,which);save(c,old,v);issued[k..':'..o.serial]=nil
   observe('CREW_BOUND',pid,c,{born=u:GetID(),count=live+1,expected=binding.capacity,reservation=o.serial,readStatus='VERIFIED'})
  end)
  if not ok then failed[k]=d.errors[k] or 'CREW_GRANT_UNCONFIRMED' end
  settling[k]=nil;mark(pid,id) -- normal publish handles removal after completion callbacks
 end
 function d.RecordUse(pid,c,uid,stage,capacity,progress,cost,amount)
  observe(stage,pid,c,{eventUnit=uid,expected=capacity,nativeProgress=progress,nativeCost=cost,count=amount})
 end
 function d.Describe(pid,c)
  d.Refresh(pid,c:GetID());local v=d.views[key(pid,c:GetID())];local err=d.errors[key(pid,c:GetID())]
  if err or not v then return '施工队：暂不可确认；'..tostring(err or 'CREW_NOT_READY')end
  return '施工队｜本城来源：'..v.count..'/2；在建或预留：'..v.reserved
   ..'\n当前新开工成本：'..(v.ratio and v.ratio..'%' or '未达到工业三级')..'；开工锁价，已完成队伍固定施工力。'
   ..'\n仅用于奇观；注入不受普通生产力倍率加成，超额不溢出。'..(v.held and '\n存在未确认发放，停止本城新组建并回传日志。' or '')
 end
 function d.BindPermanentWrites()
  local prior=shared.OnPermanentCityWrite
  shared.OnPermanentCityWrite=function(c,reason)if prior then prior(c,reason)end;if c then d.Refresh(c:GetOwner(),c:GetID())end end
 end
 local function hook(n,fn)local e=P.Field(Events,n);if e and e.Add then e.Add(fn)end end
 hook('CityProjectCompleted',completion)
 for _,n in ipairs({'CityProductionChanged','CityProductionQueueChanged','CityInitialized','CityRemovedFromMap'})do hook(n,mark)end
 hook('UnitAddedToMap',function(pid,id)
  local u=Players[pid] and Players[pid]:GetUnits():FindID(id);local r=u and P.Info('Units',u:GetType())
  if r and P.CrewBase(r.UnitType)then knownUnits[pid]=knownUnits[pid] or {};knownUnits[pid][id]=true;markPlayer(pid)end
 end)
 hook('UnitRemovedFromMap',function(pid,id)
  local source=knownUnits[pid] and knownUnits[pid][id];if not source then return end
  knownUnits[pid][id]=nil
  if type(source)=='string'then
   for _,v in pairs(d.views)do if v.owner==pid and v.source==source then mark(pid,v.city)end end
  else markPlayer(pid)end -- observed Crew whose binding was still unconfirmed
 end)
 for _,n in ipairs({'GovernorAssigned','GovernorEstablished','GovernorPromoted','GovernorChanged'})do hook(n,markPlayer)end
 hook('WonderCompleted',function(x,y,building,pid,id)mark(pid,id)end)
 hook('GameCoreEventPublishComplete',d.Flush)
 hook('LoadScreenClose',function()for pid in pairs(Players)do markPlayer(pid)end;d.Flush()end)
 store.RegisterExit('CrewProjects',function(c,loss)
  local ids={'BUILDING_SPC_CREW_PROJECT_ACCESS'}
  for tier in ipairs(M.CAPACITY)do for _,ratio in ipairs(M.RATIOS)do ids[#ids+1]=M.Marker(tier,ratio)end end
  store.RemoveOwned(c,loss,ids)
  local old=c:GetProperty(M.ORDER_PROPERTY)
  if old and old.owner==loss.origin.owner and old.x==loss.origin.x and old.y==loss.origin.y then
   local v=cp(old);v.orders={};save(c,old,v)
   for k,w in pairs(d.views)do if w.source==old.source then d.views[k]=nil;dirty[k]=nil;failed[k]=nil end end
  end
 end)
 store.RegisterReturn('CrewProjects',function(pid,c)mark(pid,c:GetID())end)
 local e=GameEvents.SPC_CrewRequest;if e and e.Add then e.Add(d.Request)end
end
