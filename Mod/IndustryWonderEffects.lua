include('NetworkInput')
include('RuntimeWork')
include('CarrierSet')
include('ExpeditionTrainingDiagnostics')
-- Derived ordinary-production effects only. No progress injection, N/E/L ledger
-- reads, topology or Crew writes. Native effect filters each Wonder's own era.
SPCIndustryWonderEffects={}
function SPCIndustryWonderEffects.Start(P,shared)
 local d={records={},errors={}};shared.IndustryWonderEffects=d
 local definitions,eras;local dirty,held={},{};local queued=0
 local initialized=false;local busy=false;local playerEra={}
 local facts=shared.FactChanges
 local queueLimit=facts and facts.ReceiptSlotsPerReceiver()or 2048
 local trace=SPCExpeditionTrainingDiagnostics.New(P,'INDUSTRY_WONDER_EFFECT')
 local function key(pid,id)return pid..':'..id end
 local function enqueue(pid,id)
  local q=dirty[pid]or held[pid]or {cities={},count=0}
  local added=0
  if id==nil then added=1-q.count
  elseif not q.all and not q.cities[id]then added=1 end
  if queued+added>queueLimit then d.errors.queue='IW_FACT_QUEUE_LIMIT';return false end
  if id==nil then q.all=true;q.cities={}
  elseif not q.all then q.cities[id]=true end
  q.count=q.count+added;queued=queued+added
  dirty[pid]=q;held[pid]=nil;d.errors.queue=nil
  return true
 end
 local function mark(pid,id)
  if P.IsTestPlayer(pid)then return enqueue(pid,id)end
 end
 local function retain(pid,q)
  local newer=dirty[pid]
  if not newer then held[pid]=q;return end
  -- A cause from the active audit owns the next snapshot, even on failure.
  if q.all or newer.all then
   queued=queued-q.count-newer.count+1
   newer.all=true;newer.cities={};newer.count=1
  else for id in pairs(q.cities)do
   if newer.cities[id]then queued=queued-1
   else newer.cities[id]=true;newer.count=newer.count+1 end
  end end
 end
 local ownedRegistry
 local health=SPCRuntimeWork.NativeHealth(P,shared,d,function(id)return ownedRegistry~=nil and ownedRegistry.Owns(id) end,function(scope)
  for pid in pairs(Players)do if SPCRuntimeWork.Player(scope,pid)then mark(pid,scope and scope.city)end end
 end)
 local function validate()
  if definitions then return end
  local list,byEra,nextOwned={},{},{}
  for _,r in ipairs(P.Rows('SPC_IndustryWonderEffects'))do
   local e=assert(P.Info('Eras',r.EraType),'IW_ERA_MISSING');local b=assert(P.Info('Buildings',r.CarrierType),'IW_CARRIER_MISSING')
   assert(type(e.ChronologyIndex)=='number' and (b.InternalOnly==true or b.InternalOnly==1) and b.CitizenSlots==0 and b.Housing==0,'IW_DEFINITION_INVALID')
   local row={id=r.CarrierType,index=b.Index,era=r.EraType,chronology=e.ChronologyIndex,amount=r.Amount}
   assert(row.amount==10 or row.amount==20 or row.amount==30,'IW_AMOUNT_INVALID')
   list[#list+1]=row;nextOwned[#nextOwned+1]={id=row.index,name=row.id};byEra[r.EraType]=byEra[r.EraType] or {};byEra[r.EraType][r.Amount]=row
  end
  assert(#list>0,'IW_DEFINITION_EMPTY');local registry=SPCCarrierSet.Registry(nextOwned);definitions,eras,ownedRegistry=list,byEra,registry
 end
 local function current(pid)
  local ok,e=P.Call(Players[pid],'GetEra');assert(ok,'IW_CIVILIZATION_ERA_UNKNOWN')
  local row=assert(P.Info('Eras',e),'IW_CIVILIZATION_ERA_UNKNOWN');return row.ChronologyIndex
 end
 local function present(c)
  local a={};local b=c:GetBuildings()
  for _,r in ipairs(definitions)do local has=P.HasBuilding(b,r.index);assert(type(has)=='boolean','IW_PRESENCE_UNKNOWN');if has then a[r.id]=true end end;return a
 end
 local function write(c,old,want)
  local b=c:GetBuildings()
  for _,r in ipairs(definitions)do if old[r.id] and not want[r.id]then
   if P.HasBuilding(b,r.index)then health.Remove(c,r.index)end
   assert(P.HasBuilding(b,r.index)==false,'IW_REMOVE_UNCONFIRMED');old[r.id]=nil
  end end
  for _,r in ipairs(definitions)do if want[r.id] and not old[r.id]then
   local has=P.HasBuilding(b,r.index);assert(type(has)=='boolean','IW_PRESENCE_UNKNOWN')
   if not has then health.Create(c,r.index)end
   assert(P.HasBuilding(b,r.index)==true,'IW_ADD_UNCONFIRMED');old[r.id]=true
  end end
 end
 local function reconcile(pid,c)
  local k=key(pid,c:GetID());local reference=SPCNetworkInput.Reference(c);local r=d.records[k]
  if not r or r.reference~=reference then r={owner=pid,x=c:GetX(),y=c:GetY(),reference=reference,applied=present(c)};d.records[k]=r end
  local f=shared.EffectiveFacts.Read(pid,c);local want={};local era
  assert(type(f.specialization)=='string','IW_FACTS_UNKNOWN')
  if f.specialization=='INDUSTRY'then
   assert(f.activeStatus=='KNOWN' and not f.investmentPending,'IW_ACTIVE_UNKNOWN')
   if f.active==4 then
    era=current(pid);assert(type(era)=='number','IW_CIVILIZATION_ERA_UNKNOWN')
    for _,levels in pairs(eras)do
     local gap=era-levels[10].chronology
     if gap>=1 then local amount=math.min(gap,3)*10;assert(levels[amount],'IW_ERA_GAP_INVALID');want[levels[amount].id]=true end
    end
   end
  end
  assert(reference==SPCNetworkInput.Reference(c) and c:GetOwner()==pid,'IW_REFERENCE_CHANGED')
  -- The session plan is not proof that the native projection still exists.
  -- Refresh only after all current qualification/era inputs are reliable.
  local physical=present(c)
  assert(reference==SPCNetworkInput.Reference(c) and c:GetOwner()==pid,'IW_REFERENCE_CHANGED')
  for id in pairs(r.applied)do r.applied[id]=nil end
  for id in pairs(physical)do r.applied[id]=true end
  write(c,r.applied,want);r.era=era;r.active=f.active;d.errors[k]=nil
  local sig=tostring(era)..':'..tostring(f.active)
  if sig~=r.observed then r.observed=sig;trace.Record('INDUSTRY_WONDER_EFFECT',{owner=pid,city=c:GetID(),count=f.active,eraCount=era,readStatus='VERIFIED',reason='IW_ERA_SCOPED'})end
 end
 local function reportFailure(pid,id,why)
  local safe,text=pcall(tostring,why)
  local reason=safe and text:match('IW_[A-Z_]+')or 'IW_READ_PENDING'
  d.errors[key(pid,id)]=reason
  if type(id)=='number'then trace.Record('INDUSTRY_WONDER_EFFECT',{owner=pid,city=id,readStatus='PENDING',reason=reason})end
 end
 local function auditOwner(pid,q)
  local player=Players[pid];local collection=assert(player and player:GetCities(),'IW_CITY_COLLECTION_UNAVAILABLE')
  local function visit(c)
   P.Count('city_scan')
   local good,why=pcall(reconcile,pid,c)
   if not good then reportFailure(pid,c:GetID(),why)end
  end
  if not q.all then
   for id in pairs(q.cities)do
    local good,why=pcall(function()
     local c=collection:FindID(id)
     if c and SPCRuntimeWork.AuditCityOwned(c,pid,true)then visit(c)end
    end)
    if not good then reportFailure(pid,id,why)end
   end
  else
   local live={}
   for _,c in collection:Members()do live[key(pid,c:GetID())]=true;visit(c)end
   for k,r in pairs(d.records)do if r.owner==pid and not live[k]then d.records[k]=nil;d.errors[k]=nil end end
  end
 end
 function d.Flush()
  if shared.IndustryWonderEffects~=d or facts and (facts.closed or shared.FactChanges~=facts)then
   dirty={};held={};queued=0;return
  end
  if busy or initialized and not next(dirty) or shared.CityProgressionStore.HistoryStartStatus()=='WAITING'then return end
  busy=true
  local ok,err=pcall(function()
   validate()
   if not initialized then
    -- Store's existing confirmed-exit/load callbacks own foreign-city cleanup.
    -- Initialization reads supported owners only; no extra world-city scan.
    for pid in pairs(Players)do mark(pid)end;initialized=true
   end
   local work=dirty;dirty={}
   for pid,q in pairs(work)do
    local covered,why=pcall(auditOwner,pid,q)
    if covered then queued=queued-q.count;d.errors[key(pid,'owner')]=nil
    else retain(pid,q);reportFailure(pid,'owner',why)end
   end
  end)
  busy=false;d.error=not ok and (tostring(err):match('IW_[A-Z_]+') or 'IW_READ_PENDING') or nil
 end
 function d.Refresh(pid,id)mark(pid,id);d.Flush()end
 if facts then facts.RegisterConsumer('IndustryWonderEffects',function(e)
  if shared.IndustryWonderEffects~=d then return false end
  if e.player==nil then return facts.Receipt(e,'IRRELEVANT','OWNER_SCOPE_REQUIRED')end
  local eligible,_,status=P.IsTestPlayer(e.player)
  if not eligible then
   if status=='INELIGIBLE'then return facts.Receipt(e,'IRRELEVANT','UNSUPPORTED_PLAYER')end
   return false
  end
  local receipt=facts.Receipt(e,'REGISTERED')
  return enqueue(e.player,e.city)and receipt or false
 end,{kinds={'IDENTITY','POTENTIAL','ACTIVE'},delivery='RESPONSIBILITY'})end
 function d.Describe(pid,c)
  local k=key(pid,c:GetID());local r=d.records[k];local reason=d.errors[k] or d.errors[key(pid,'owner')] or d.errors.queue or d.error
  return '巨构工程学：'..(reason and '等待 '..reason or r and r.active==4 and '本城自行生产旧时代奇观：时代差 1 / 2 / 3+ → +10% / +20% / +30%' or '未生效（需要工业 ACTIVE IV）')
   ..'\n按本文明时代与奇观自身时代比较；适用时也可加成施工队投入的基础施工力。'
 end
 local function hook(n,f)local e=P.Field(Events,n);if e and e.Add then e.Add(f)end end
 hook('CityRemovedFromMap',function(pid)mark(pid)end)
 hook('GameCoreEventPublishComplete',d.Flush)
 hook('LoadScreenClose',function()for pid in pairs(Players)do mark(pid)end;d.Flush()end)
 hook('PlayerEraChanged',function(pid)mark(pid);d.Flush()end)
 hook('PlayerTurnActivated',function(pid)
  if not P.IsTestPlayer(pid)then return end
  local ok,era=pcall(current,pid)
  if ok and era~=playerEra[pid]then playerEra[pid]=era;mark(pid)end
  for k in pairs(d.errors)do local p,id=k:match('^(%d+):(%d+)$');if tonumber(p)==pid then mark(pid,tonumber(id))end end
  d.Flush()
 end)
 local store=shared.CityProgressionStore
 store.RegisterExit('IndustryWonderEffects',function(c,loss)
  validate();store.RemoveOwned(c,loss,ownedRegistry.Names())
  for k,r in pairs(d.records)do if r.owner==loss.origin.owner and r.x==loss.origin.x and r.y==loss.origin.y then d.records[k]=nil;d.errors[k]=nil end end
  mark(loss.origin.owner)
 end)
 store.RegisterReturn('IndustryWonderEffects',function(pid,c)mark(pid,c:GetID())end)
end
