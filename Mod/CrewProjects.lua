include('SafeCallbacks')
include('UnitSiteFacts')
if not SPCPropertyCell then include('PropertyCell')end
include('CrewModel')
include('ExpeditionTrainingDiagnostics')
-- B239: paid native projects retain one capacity admission while paused; actual queue entries stay separate.
-- Saved admission/grant proof and native living inventory remain the only capacity sources.
-- This writer never guesses a source from a new unit's position or name.
SPCCrewProjects={}
function SPCCrewProjects.Start(P,shared)
 local M=SPCCrewModel;local cp,same=M.Copy,M.Same;local store=assert(shared.CityProgressionStore)
 local d={ready=false,busy=false,errors={},views={},revision=0};shared.CrewProjects=d
 local consuming={}
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
   and M.Int(v.owner) and type(v.orders)=='table' and #v.orders<=#M.CAPACITY*#M.RATIOS+2,'CREW_ORDER_HISTORY_INVALID')
  if v.owner~=pid then assert(#v.orders==0,'CREW_PREVIOUS_OWNER_ORDER_HELD');local n=cp(v);n.owner=pid;return n,v,a end
  local seen,paused={},{};local reserved=0
  for _,o in ipairs(v.orders)do
   local tier,ratio=M.Parse(o.project)
   assert(type(o)=='table' and tier and tier==o.tier and ratio==o.ratio and M.Int(o.serial) and o.serial<=v.serial
    and not seen[o.serial] and M.Int(o.base) and M.Int(o.capacity) and o.capacity>0 and M.Int(o.price) and o.price>0
    and (o.stage=='RESERVED' or o.stage=='QUEUED' or o.stage=='CALLING' or o.stage=='HELD' or o.stage=='PAUSED'),'CREW_ORDER_HISTORY_INVALID')
   seen[o.serial]=true
   if o.stage=='PAUSED'then assert(not paused[o.project],'CREW_ORDER_HISTORY_INVALID');paused[o.project]=true
   else reserved=reserved+1 end
  end
  assert(reserved<=2,'CREW_ORDER_HISTORY_INVALID')
  return cp(v),v,a
 end
 local function save(c,old,v)
  assert(same(c:GetProperty(M.ORDER_PROPERTY),old),'CREW_STALE_ORDER')
  local setter=P.SetProperty;local payload=cp(v) -- clone errors precede the attempted write
  local result=SPCPropertyCell.WriteReadback(function()return setter(c,M.ORDER_PROPERTY,payload)end,
   function()return c:GetProperty(M.ORDER_PROPERTY)end)
  if not result.readReturned then error(result.observed,0)end
  assert(same(result.observed,v),'CREW_ORDER_WRITE_UNCONFIRMED')
  return result.writeReturned -- readback, not a setter's return, establishes the saved value
 end
 local function queue(pid,c)
  local r=assert(ExposedMembers.SPC_CrewNativeRead,'CREW_UI_READER_UNAVAILABLE')(pid,c:GetID())
  assert(type(r)=='table' and r.owner==pid and r.city==c:GetID() and r.x==c:GetX() and r.y==c:GetY()
   and r.turn==Game.GetCurrentGameTurn() and type(r.projects)=='table' and type(r.completed)=='table' and type(r.progress)=='table','CREW_QUEUE_UNKNOWN')
  local count=0;for id,n in pairs(r.projects)do assert(M.Parse(id) and M.Int(n),'CREW_QUEUE_UNKNOWN');count=count+n end
  assert(count<=2,'CREW_QUEUE_OVER_CAPACITY')
  for tier in ipairs(M.CAPACITY)do for _,ratio in ipairs(M.RATIOS)do
   local id=M.Project(tier,ratio,speed());local value=r.progress[id]
   assert(type(value)=='number' and value>=0 and value<1000000000,'CREW_PROJECT_PROGRESS_UNKNOWN')
  end end
  return r,count
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
  local setter=P.SetProperty;local target=Players[pid];local payload=cp(v)
  local result=SPCPropertyCell.WriteReadback(function()return setter(target,M.RECEIPT_PROPERTY,payload)end,
   function()return Players[pid]:GetProperty(M.RECEIPT_PROPERTY)end)
  if not result.readReturned then error(result.observed,0)end
  assert(same(result.observed,v),'CREW_RECEIPT_WRITE_UNCONFIRMED')
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
 local function reserved(v)return #v.orders end
 local function queued(v)
  local n=0;for _,o in ipairs(v.orders)do if o.stage=='QUEUED'then n=n+1 end end;return n
 end
 local function reconcile(pid,c,v,old,q)
  -- A native project owns one progress bucket even when absent from the queue.
  -- Keep at most one paid paused admission per native bucket; it still owns one slot.
  local initial=cp(v);local keep,paused,available={}, {},cp(q.projects)
  for _,o in ipairs(v.orders)do
   local before=o.stage;local retain=true
   if before=='CALLING' or before=='HELD'then
   elseif before~='PAUSED' and (available[o.project] or 0)>0 then
    available[o.project]=available[o.project]-1;o.stage='QUEUED';o.resuming=nil
   elseif before=='RESERVED' and issued[key(pid,c:GetID())..':'..o.serial]then
   elseif q.progress[o.project]>0 then
    -- Positive local progress is not a missed completion in another city.
    -- Do not duplicate a shared bucket still represented in this city's queue.
    if not paused[o.project] and (q.projects[o.project] or 0)==0 then
     o.stage='PAUSED';o.resuming=nil;paused[o.project]=true
    else retain=false end
   elseif (q.completed[o.project] or -1)>o.base then
    o.stage='HELD' -- zero progress + new counter is not proof of cancellation
   else retain=false end
   if retain then keep[#keep+1]=o end
   if not retain or before~=o.stage then
    observe('CREW_ORDER_STATE',pid,c,{projectType=o.project,reservation=o.serial,lockedPrice=o.price,
     nativeProgress=q.progress[o.project],queued=q.projects[o.project] or 0,phase=retain and o.stage or 'CANCELLED'})
   end
  end
  v.orders=keep
  if not same(v,initial)then save(c,old,v);old=cp(v)end
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
  local slots=reserved(v);local occupied=count+slots;local queueKnown=n==queued(v)
  local room=not held and queueKnown and occupied<2
  -- Old B238 states may already over-admit paid work. Never delete it: an
  -- existing admission can resume only if living + actual queued completions
  -- still fit the two-unit ceiling. It does not request another reservation.
  local resumeRoom=not held and queueKnown and count+n<2
  local allowed,startable,retained,wanted={}, {}, {}, {};local paused=0
  for _,o in ipairs(v.orders)do
   if o.stage=='PAUSED'then paused=paused+1 end
   if o.stage=='PAUSED' or o.stage=='QUEUED' or o.stage=='RESERVED'then
    assert(q.costs[o.project]==o.price,'CREW_NATIVE_COST_MISMATCH')
    retained[o.project]={stage=o.stage,price=o.price}
   end
  end
  for tier in ipairs(M.CAPACITY)do for _,price in ipairs(M.RATIOS)do
   local idp=M.Project(tier,price,speed());local record=retained[idp]
   local fresh=room and ratio~=nil and price==ratio and tier<=(active==4 and 5 or 3)
   local resume=resumeRoom and record and record.stage=='PAUSED'
   allowed[idp]=not not(record or fresh);startable[idp]=not not(resume or fresh)
   wanted[M.Marker(tier,price)]=allowed[idp]
  end end
  -- Add new eligibility before withdrawing obsolete unstarted variants.
  for id,want in pairs(wanted)do if want then marker(c,id,true)end end
  for id,want in pairs(wanted)do if not want then marker(c,id,false)end end
  marker(c,'BUILDING_SPC_CREW_PROJECT_ACCESS',false) -- exact retired B044 access only
  local view={owner=pid,city=id,source=a.token,active=active,N=N,ratio=ratio,count=count,reserved=slots,queued=n,paused=paused,
   occupied=occupied,overCapacity=occupied>2,resumeBlocked=not resumeRoom,queueKnown=queueKnown,
   held=not not held,allowed=allowed,startable=startable,retained=retained}
  if not same(d.views[k],view)then d.views[k]=view;d.revision=d.revision+1
   observe('CREW_STATE',pid,c,{count=count,queued=n,paused=paused,wanted=room,expected=ratio,
    phase=(held or not queueKnown) and 'HELD' or occupied>2 and 'OVER_CAPACITY' or 'READY',reason=not queueKnown and 'CREW_QUEUE_ADMISSION_MISMATCH' or nil})
  end
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
    local resume
    for _,o in ipairs(v.orders)do
     assert(o.stage=='QUEUED' or o.stage=='PAUSED','CREW_ORDER_PENDING')
     if o.stage=='PAUSED' and o.project==p.Project then resume=o end
    end
    if not resume then
     local wanted,active=qualified(pid,c,a);assert(ratio==wanted and tier<=(active==4 and 5 or 3),'CREW_PROJECT_NOT_CURRENT_PRICE')
    end
    local count=d.Inventory(pid)[a.token] or 0
    for _,r in pairs(receipts(pid))do assert(r.source~=a.token or r.stage~='CALLING','CREW_GRANT_UNRESOLVED')end
    assert(n==queued(v),'CREW_CAPACITY_FULL_OR_QUEUE_UNKNOWN')
    assert(resume and count+n<2 or not resume and count+reserved(v)<2,'CREW_CAPACITY_FULL_OR_QUEUE_UNKNOWN')
    local capacity=resume and resume.capacity or M.Amount(tier,speed())
    local price=resume and resume.price or M.Cost(tier,ratio,speed())
    assert(q.costs[p.Project]==price,'CREW_NATIVE_COST_MISMATCH')
    local base=q.completed[p.Project];assert(M.Int(base),'CREW_NATIVE_COMPLETION_COUNTER_UNKNOWN')
    local o=resume
    if not o then
     v.serial=v.serial+1;o={serial=v.serial,project=p.Project,tier=tier,ratio=ratio,capacity=capacity,price=price}
     v.orders[#v.orders+1]=o
    else assert(q.progress[p.Project]>0,'CREW_RESUME_PROGRESS_UNKNOWN');o.resuming=true end
    o.base=base;o.stage='RESERVED';o.turn=Game.GetCurrentGameTurn();o.before=q.projects[p.Project] or 0
    save(c,old,v);issued[key(pid,p.CityID)..':'..o.serial]=true
    observe('CREW_ORDER',pid,c,{projectType=o.project,reservation=o.serial,nativeCost=price,lockedPrice=price,nativeProgress=q.progress[o.project],expected=capacity,phase=resume and 'RESUMING' or 'RESERVED'})
    return {reservation=o.serial,project=p.Project,before=o.before,base=o.base}
   end
   local index;for i,o in ipairs(v.orders)do if o.serial==p.Reservation then index=i;break end end
   if not index then return {finished=true}end
   local o=v.orders[index]
   if p.Action=='CANCEL'then
    assert(o.stage=='RESERVED' and (q.projects[o.project] or 0)==o.before and q.completed[o.project]==o.base,'CREW_CANCEL_UNCONFIRMED')
    if o.resuming then o.stage='PAUSED';o.resuming=nil else table.remove(v.orders,index)end
    save(c,old,v);issued[key(pid,p.CityID)..':'..o.serial]=nil;return {cancelled=true}
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
   local which;for i,o in ipairs(v.orders)do if o.project==row.ProjectType and o.stage~='PAUSED'then which=i;break end end
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
   local u=UnitManager.InitUnit(pid,'UNIT_SPC_CREW_'..M.IDS[tier],c:GetX(),c:GetY())
   assert(u and u:GetOwner()==pid and M.Int(u:GetID()) and Players[pid]:GetUnits():FindID(u:GetID()),'CREW_GRANT_RETURN_UNKNOWN')
   assert(source(pid,c).token==a.token,'CREW_SOURCE_CHANGED_DURING_GRANT')
   assert(P.Info('Units',u:GetType()).UnitType=='UNIT_SPC_CREW_'..M.IDS[tier],'CREW_GRANT_TYPE_MISMATCH')
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
 function d.UseTarget(pid,u)
  d.Unit(pid,u) -- strict permanent source and locked capacity
  assert(u:GetBuildCharges()==1,'CREW_REQUIRES_EXACTLY_ONE_CHARGE')
  assert(u:GetProperty('SPC_CREW_RESERVED')==nil,'CREW_RESERVED')
  local c=SPCUnitSiteFacts.TargetCity(shared,pid,u);local s=shared.ConstructionProbe.ReadSnapshot(pid,c)
  local row=s.kind=='Buildings' and P.Info('Buildings',s.target)
  assert(row and (row.IsWonder==true or row.IsWonder==1) and s.progress<s.cost,'CREW_WONDER_REQUIRED')
  -- D0053 accepts native Production modifiers. Keep base input bounded;
  -- receipt, target and debit checks remain authoritative.
  return c,s
 end

 function d.Consume(pid,u,c,plan)
  if consuming[pid]then return {status='BUSY',kind='CREW_USE',phase='PRECHECK'}end
  consuming[pid]=true;local destructive=false;local phase='PRECHECK'
  local ok,result=pcall(function()
   assert(P.IsTestPlayer(pid)and u and u:GetOwner()==pid,'OWN_UNIT_REQUIRED')
   local current=Players[pid]:GetUnits():FindID(u:GetID());assert(current and current:GetOwner()==pid,'OWN_UNIT_REQUIRED');u=current
   assert(type(plan)=='table'and plan.unitID==u:GetID(),'PREPARE_THIS_UNIT_FIRST');plan=cp(plan)
   assert(c and c:GetOwner()==pid and c:GetID()==plan.cityID,'OWNER_CHANGED')
   local binding=d.Unit(pid,u);local amount=binding.capacity;assert(amount==plan.amount and binding.grant==plan.grant,'TARGET_CHANGED_PREPARE_AGAIN')
   local now,s=d.UseTarget(pid,u)
   assert(now:GetID()==c:GetID() and plan.turn==Game.GetCurrentGameTurn() and s.target==plan.target and s.cost==plan.cost and s.progress==plan.progress,'TARGET_CHANGED_PREPARE_AGAIN')
   local receipts=cp(Players[pid]:GetProperty(M.USE_RECEIPT_PROPERTY) or {});assert(type(receipts)=='table','CREW_USE_HISTORY_INVALID');assert(not receipts[binding.grant],'RECEIPT_EXISTS')
   local function record(state)
    receipts[binding.grant]={state=state,unitID=plan.unitID,cityID=c:GetID(),target=s.target,amount=math.floor(math.min(amount,s.cost-s.progress)+0.5)}
    -- Evidence amount only: integer readback survives binary32 Property storage.
    -- Reservation/debit and the actual fractional AddProgress below stay exact.
    pcall(P.SetProperty,Players[pid],M.USE_RECEIPT_PROPERTY,receipts)
    assert(same(Players[pid]:GetProperty(M.USE_RECEIPT_PROPERTY),receipts),'CREW_USE_RECEIPT_UNCONFIRMED')
   end
   destructive=true;phase='INTENT';record('INTENT');P.SetProperty(u,'SPC_CREW_RESERVED',plan.token)
   assert(u:GetProperty('SPC_CREW_RESERVED')==plan.token,'RESERVATION_UNCONFIRMED')
   Players[pid]:GetUnits():Destroy(u)
   assert(not Players[pid]:GetUnits():FindID(plan.unitID),'UNIT_DEBIT_UNCONFIRMED')
   local after=shared.ConstructionProbe.ReadSnapshot(pid,c)
   assert(after.target==s.target and after.progress==s.progress and after.cost==s.cost,'TARGET_CHANGED_AFTER_DEBIT')
   phase='GRANT_ATTEMPTED';record('GRANT_ATTEMPTED') -- Never automatically replay an uncertain engine grant.
   d.RecordUse(pid,c,plan.unitID,'CREW_USE_ATTEMPT',amount,s.progress,s.cost,math.min(amount,s.cost-s.progress))
   c:GetBuildQueue():AddProgress(math.min(amount,s.cost-s.progress)) -- One native call; accepted modifiers apply. No correction/replay.
   phase='GRANT_RETURNED';record('GRANT_RETURNED')
   d.RecordUse(pid,c,plan.unitID,'CREW_USE_RETURNED',amount,s.progress,s.cost,math.min(amount,s.cost-s.progress))
   return {status='COMMITTED',kind='CREW_USE',phase=phase,baseInput=math.min(amount,s.cost-s.progress),unusedBase=math.max(0,amount-(s.cost-s.progress))}
  end)
  consuming[pid]=nil
  if ok then return result end
  local printable,text=pcall(tostring,result)
  text=printable and text or 'CREW_USE_ERROR'
  return {status=destructive and 'HELD'or 'REJECTED',kind='CREW_USE',phase=phase,error=text}
 end
 function d.RecordUse(pid,c,uid,stage,capacity,progress,cost,amount)
  observe(stage,pid,c,{eventUnit=uid,baseCapacity=capacity,nativeProgress=progress,nativeCost=cost,baseInput=amount})
 end
 function d.RecordPrecision(pid,r)
  observe('CREW_PRECISION',pid,r.cityID and city(pid,r.cityID) or nil,{eventUnit=r.unitID,nativeProgress=r.before,afterProgress=r.after,
   baseCapacity=r.amount,baseInput=r.baseInput,actualDelta=r.observed,targetChanged=not r.afterReadError and r.afterTarget~=r.target or nil,readStatus=(r.error or r.afterReadError) and 'UNKNOWN' or r.observed~=nil and 'OBSERVED' or 'NOT_MEASURED'})
 end
 function d.Describe(pid,c)
  d.Refresh(pid,c:GetID());local v=d.views[key(pid,c:GetID())];local err=d.errors[key(pid,c:GetID())]
  if err or not v then return '施工队：暂不可确认；'..tostring(err or 'CREW_NOT_READY')end
  return '施工队｜已占名额：'..v.occupied..'/2；存活：'..v.count..'；未完成组建：'..v.reserved
   ..'\n当前新开工成本：'..(v.ratio and v.ratio..'%' or '未达到工业三级')..'；开工锁价，已完成队伍基础施工力锁定。'
   ..'\n可续建半成品：'..v.paused..'；续建继续占用原名额，保留已有成本与进度。'
   ..(v.overCapacity and '\n已有未完成组建超过当前名额；不再接纳新开工，释放存活或已排队名额后可安全续建。' or '')
   ..(not v.queueKnown and '\n原生队列与开工记录不一致，暂停新开工与续建；已有成本及进度保留。' or '')
   ..'\n施工仅用于在建奇观；基础施工力可受适用生产力加成，余量不结转。'..(v.held and '\n存在未确认发放，停止本城新组建并回传日志。' or '')
 end
 function d.BindPermanentWrites()
  if shared.FactChanges then shared.FactChanges.RegisterConsumer('CrewProjects',function(e)mark(e.player,e.city)end,{kinds={'IDENTITY','POTENTIAL','ACTIVE'}})end
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
