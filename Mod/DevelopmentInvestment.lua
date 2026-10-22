include('DevelopmentInvestmentModel')
include('DevelopmentInvestmentCatalog')
include('CommerceModel')
include('ExpeditionTrainingDiagnostics')
SPCDevelopmentInvestment={ACCESS='BUILDING_SPC_DEVELOPMENT_ACCESS'}
function SPCDevelopmentInvestment.Start(P,shared)
 local M=SPCDevelopmentInvestmentModel;local cp,same=M.Copy,M.Same
 local store=assert(shared.CityProgressionStore,'DEVELOPMENT_STORE_REQUIRED')
 local d={views={},revision=0};shared.DevelopmentInvestment=d
 local trace=SPCExpeditionTrainingDiagnostics.New(P,'DEVELOPMENT')
 local function emit(stage,v)if trace then pcall(trace.Record,stage,v)end end
 local function code(e)return tostring(e):match('(DEVELOPMENT_[A-Z0-9_]+)') or tostring(e):match('(STORE_[A-Z0-9_]+)') or 'DEVELOPMENT_STATE_UNKNOWN'end
 local function failure(e,pid,id,phase)
  local reason=code(e);emit('DEVELOPMENT_FAILURE',{owner=pid,city=id,phase=phase,reason=reason});return reason
 end
 local function key(pid,id)return pid..':'..id end
 local function city(pid,id)return Players[pid] and Players[pid]:GetCities():FindID(id)end
 local function title(c)return Locale and Locale.Lookup and Locale.Lookup(c:GetName()) or c:GetName()end
 local function ref(c)
  local h=store.HistoricalReference(c);local r=store.CapitalReference(h.token)
  assert(r.owner==c:GetOwner() and r.cityID==c:GetID() and r.x==c:GetX() and r.y==c:GetY() and r.stage=='ACTIVE','DEVELOPMENT_REFERENCE_CHANGED')
  return {owner=r.owner,cityID=r.cityID,x=r.x,y=r.y,token=r.token,changes=r.changes}
 end
 local catalog=SPCDevelopmentInvestmentCatalog.Build(P)
 local names={SPCDevelopmentInvestment.ACCESS};local effects={}
 for r in assert(P.Field(GameInfo,'SPC_DevelopmentEffects'),'DEVELOPMENT_EFFECTS_UNAVAILABLE')()do
  effects[r.DistrictType]=r.CarrierType;names[#names+1]=r.CarrierType
 end
 table.sort(names)
 local records,occupancy,reservations,dirty,quotes={},{},{},{},{}
 local loaded=false;local indexError;local busy=false;local openViews={}
 local function rebuild()
  occupancy={}
  for token,r in pairs(records)do for target,c in pairs(r.value.contracts)do if M.Open(c)then
   assert(not occupancy[target] or occupancy[target]==token,'DEVELOPMENT_OCCUPANCY_CONFLICT');occupancy[target]=token
  end end end
 end
 local function remember(value,r)
  records[r.token]={value=cp(value),reference=cp(r)};rebuild()
 end
 local function set(c,name,want)
  local b=assert(P.Info('Buildings',name),'DEVELOPMENT_EFFECT_DEFINITION_MISSING')
  local has=P.HasBuilding(c:GetBuildings(),b.Index);assert(type(has)=='boolean','DEVELOPMENT_EFFECT_UNKNOWN')
  if has==want then return false end
  if want then P.CreateBuilding(c:GetBuildQueue(),b.Index)else P.RemoveBuilding(c:GetBuildings(),b.Index)end
  assert(P.HasBuilding(c:GetBuildings(),b.Index)==want,'DEVELOPMENT_EFFECT_UNCONFIRMED');return true
 end
 local function effect(c,domain)
  if domain then assert(effects[domain],'DEVELOPMENT_EFFECT_DEFINITION_MISSING')end
  local changed=0
  for id,name in pairs(effects)do if id~=domain and set(c,name,false)then changed=changed+1 end end
  if domain and set(c,effects[domain],true)then changed=changed+1 end
  if changed>0 then emit('DEVELOPMENT_EFFECTS',{owner=c:GetOwner(),city=c:GetID(),contractDomain=domain,expected=domain and 50 or 0,count=changed})end
 end
 local function publish(pid,id,v)
  local k=key(pid,id);local old=d.views[k];v.revision=old and old.revision or 0
  if same(old,v)then return end
  d.revision=d.revision+1;v.revision=d.revision;d.views[k]=cp(v)
 end
 function d.Mark(pid,id)
  if not P.IsTestPlayer(pid)then return end
  dirty[pid]=dirty[pid] or {};if id then dirty[pid][id]=true else dirty[pid].all=true end
 end
 local function invalidate(pid,id)
  if id then quotes[key(pid,id)]=nil end
  d.Mark(pid,id)
 end
 function d.Audit(scope)
  local pid=scope and scope.player
  if pid and P.IsTestPlayer(pid)then
   for k,x in pairs(quotes)do if x.owner==pid then quotes[k]=nil end end;d.Mark(pid)
  end
 end
 function d.SourceChanged(pid,id)invalidate(pid,id)end
 local function money(pid)
  local t=assert(Players[pid] and Players[pid]:GetTreasury(),'DEVELOPMENT_TREASURY_UNKNOWN')
  local n=t:GetGoldBalance();assert(M.Finite(n),'DEVELOPMENT_TREASURY_UNKNOWN');return n,t
 end
 local function state(pid,c)
  local s=store.DevelopmentState(pid,c);return s.value
 end
 local function count(v)local n=0;for _,c in pairs(v and v.contracts or {})do if M.Open(c)then n=n+1 end end;return n end
 local function write(pid,c,old,value,phase)
  store.WriteDevelopment(pid,c,old,value,function(point,ok,observed,expected,status,matches)
   emit('DEVELOPMENT_READBACK',{owner=pid,city=c:GetID(),phase=phase,readPoint=point,
    readStatus=ok and 'READABLE' or 'READ_ERROR',writeStatus=status,savedMatches=ok and matches or false,recordType=ok and type(observed) or 'UNKNOWN'})
  end)
  assert(same(state(pid,c),value),'DEVELOPMENT_WRITE_UNCONFIRMED')
  remember(value,ref(c))
 end
 local function validateReference(r)
  local a=store.CapitalReference(r.token)
  if a.owner~=r.owner or a.changes~=r.changes then return false end
  assert(a.cityID==r.cityID and a.x==r.x and a.y==r.y and a.stage=='ACTIVE','DEVELOPMENT_REFERENCE_UNAVAILABLE')
  local c=assert(city(r.owner,r.cityID),'DEVELOPMENT_CITY_UNKNOWN');assert(same(ref(c),r),'DEVELOPMENT_REFERENCE_CHANGED');return true,c
 end
 local function completed(c,contract)
  local bs=c:GetBuildings()
  for _,b in ipairs(assert(catalog.domains[contract.domain],'DEVELOPMENT_DISTRICT_UNKNOWN'))do
   local has=P.HasBuilding(bs,b.index);assert(type(has)=='boolean','DEVELOPMENT_BUILDING_UNKNOWN')
   if has and not contract.existing[b.id]then return b.id end
  end
 end
 local function reconcileRecord(token)
  local tracked=records[token];if not tracked then return end
  local r=store.CapitalReference(token)
  -- Source-owner loss already terminates its saved contracts in the Store.
  -- We still own withdrawal in targets that remain under the original owner.
  if r.owner~=tracked.reference.owner or r.changes~=tracked.reference.changes then
   for _,contract in pairs(tracked.value.contracts)do if M.Open(contract)then
    local ok,target=validateReference(contract.target);if ok then effect(target,nil)end
   end end
   records[token]=nil;rebuild();return
  end
  local source=assert(city(r.owner,r.cityID),'DEVELOPMENT_CITY_UNKNOWN')
  local old=state(r.owner,source);assert(old,'DEVELOPMENT_HISTORY_UNAVAILABLE');local value=cp(old)
  for targetKey,c in pairs(value.contracts)do if M.Open(c)then
   local valid,target=validateReference(c.target)
   if not valid then c.stage='TERMINATED';c.reason='DEVELOPMENT_OWNER_CHANGED'
   elseif c.stage=='DEBIT_INTENT'then c.stage='TERMINATED';c.reason='DEVELOPMENT_UNUSED_INTENT'
   elseif c.stage=='DEBIT_CALLING'then c.stage='HELD';c.reason='DEVELOPMENT_NATIVE_OUTCOME_UNKNOWN'
   elseif c.stage=='ACTIVE'then
    local b=completed(target,c)
    if b then c.stage='COMPLETED';c.completedBuilding=b;c.completedTurn=Game.GetCurrentGameTurn();c.reason='DEVELOPMENT_BUILDING_COMPLETED'end
   end
   -- Withdrawal is valid even if the following receipt fails; no payment retry.
   if valid and c.stage~='ACTIVE'then effect(target,nil)end
  end end
  if not same(old,value)then write(r.owner,source,old,value,'RECONCILE_WRITE')
   for _,c in pairs(value.contracts)do if not M.Open(c) and old.contracts[c.target.token].stage~=c.stage then
    emit('DEVELOPMENT_CLOSED',{owner=r.owner,city=r.cityID,targetCity=c.target.cityID,contractID=c.sequence,contractDomain=c.domain,phase=c.stage,reason=c.reason,eventKind=c.completedBuilding})
   end end
  else remember(value,ref(source))end
  for targetKey,c in pairs(value.contracts)do
   if not M.Open(c) and reservations[targetKey]==token then reservations[targetKey]=nil end
  end
  for _,c in pairs(value.contracts)do if c.stage=='ACTIVE'then
   local valid,target=validateReference(c.target);assert(valid,'DEVELOPMENT_OWNER_CHANGED');effect(target,c.domain)
  end end
  invalidate(r.owner,r.cityID)
 end
 function d.Reconcile(pid,id)
  if busy or not loaded or not P.IsTestPlayer(pid)then return end
  busy=true
  for token,r in pairs(records)do if r.reference.owner==pid then
   local relevant=id==nil or r.reference.cityID==id
   if not relevant then for _,c in pairs(r.value.contracts)do if M.Open(c) and c.target.cityID==id then relevant=true;break end end end
   if relevant and count(r.value)>0 then
    local ok,err=pcall(reconcileRecord,token)
    if not ok then d.error=failure(err,pid,r.reference.cityID,'RECONCILE');invalidate(pid,r.reference.cityID)end
   end
  end end
  busy=false
 end
 local function initialize()
  if loaded then return true end
  if store.HistoryStartStatus and store.HistoryStartStatus()=='WAITING'then return false end
  local ok,err=pcall(function()
   for pid,p in pairs(Players)do if P.IsTestPlayer(pid)then
    store.VisitDevelopment(pid,function(value,r)remember(value,r)end)
    -- Once per context: retire only this module's derived effects, then rebuild.
    for _,c in p:GetCities():Members()do if store.Owns(c)then
     ref(c);effect(c,nil);d.Mark(pid,c:GetID())
    end end
   end end
  end)
  loaded=true;indexError=not ok and code(err) or nil
  if indexError then d.error=failure(err,nil,nil,'LOAD_INDEX')end
  for pid in pairs(Players)do if P.IsTestPlayer(pid)then d.Reconcile(pid)end end
  return true
 end
 local function sourceFacts(pid,c)
  local f=shared.EffectiveFacts.Read(pid,c);local r=ref(c);local old=state(pid,c)
  local v={reference=r,token=r.token,identity=f.specialization,potential=f.potential,stage='READY',workers=0,
   available=(f.specialization=='COMMERCE' and f.potential>=4) or old~=nil,contracts=cp(old and old.contracts or {}),used=count(old),canSign=false}
  if not v.available then return v,old end
  assert(SPCCommerceModel.IsStandardSpeed(),'DEVELOPMENT_STANDARD_SPEED_ONLY')
  v.balance=money(pid)
  if indexError then v.stage='HELD';v.reason=indexError;return v,old end
  for _,contract in pairs(v.contracts)do if M.Open(contract) and contract.stage~='ACTIVE'then v.stage='HELD';v.reason='DEVELOPMENT_NATIVE_OUTCOME_UNKNOWN';return v,old end end
  if f.specialization~='COMMERCE' or f.activeStatus~='KNOWN' or f.active~=4 or f.investmentPending then v.reason='DEVELOPMENT_ACTIVE_IV_REQUIRED';return v,old end
  -- Current worker count, independent of Commercialization's yield/network readiness.
  local dc=shared.DistrictCompleteness.ReadFacts(pid,c,r.token)
  assert(dc.validity=='VERIFIED' and dc.availability=='READY' and dc.value,'DEVELOPMENT_WORKERS_UNKNOWN')
  local anchor
  for _,row in ipairs(dc.value.districts)do if f.first and row.id==f.first.districtID and row.type==f.first.type then anchor=row;break end end
  assert(anchor and anchor.complete,'DEVELOPMENT_WORKERS_UNKNOWN')
  if not anchor.pillaged then
   local plot=assert(Map.GetPlotByIndex(anchor.plot),'DEVELOPMENT_WORKERS_UNKNOWN');local n=plot:GetWorkerCount()
   assert(type(n)=='number' and n>=0 and n%1==0,'DEVELOPMENT_WORKERS_UNKNOWN');v.workers=n
  end
  v.canSign=v.used<v.workers;v.reason=v.canSign and 'DEVELOPMENT_READY' or 'DEVELOPMENT_CAPACITY_FULL'
  return v,old
 end
 local function nativeTarget(pid,c)
  local reader=assert(ExposedMembers.SPC_DevelopmentRead,'DEVELOPMENT_PRICE_READER_UNAVAILABLE')
  local out=reader(pid,c:GetID())
  assert(type(out)=='table' and out.owner==pid and out.cityID==c:GetID() and out.x==c:GetX() and out.y==c:GetY()
   and out.turn==Game.GetCurrentGameTurn() and type(out.options)=='table' and type(out.existing)=='table','DEVELOPMENT_NATIVE_FACTS_STALE')
  return out
 end
 local function snapshot(pid,c,onlyTarget)
  local v,old=sourceFacts(pid,c);local rows={};local internal={owner=pid,options={}}
  v.options=rows
  if not v.canSign then return v,internal end
  local routes=shared.NetworkBridge.CurrentOutgoingDomestic(pid,c)
  assert(routes.validity=='VERIFIED','DEVELOPMENT_OUTGOING_PENDING')
  for _,id in ipairs(routes.partners)do if onlyTarget==nil or id==onlyTarget then
   local target=assert(city(pid,id),'DEVELOPMENT_CITY_UNKNOWN')
   local okay,result=pcall(function()
    local tr=ref(target)
    if occupancy[tr.token] or reservations[tr.token]then return {{targetCity=id,targetName=title(target),reason='DEVELOPMENT_TARGET_OCCUPIED',canSign=false}}end
    local facts=nativeTarget(pid,target);local options={}
    for _,option in ipairs(facts.options)do
     local row={targetCity=id,targetName=title(target),domain=option.domain,building=option.building,price=option.price,tier=option.tier,
      reason=option.reason,candidates=option.count,canSign=false}
     if option.price then
      assert(M.Finite(option.price) and option.price>0 and catalog.buildings[option.building]
       and catalog.buildings[option.building].domain==option.domain and effects[option.domain],'DEVELOPMENT_PRICE_UNAVAILABLE')
      row.cost=option.price*.15;row.canSign=v.balance>=row.cost;row.reason=row.canSign and 'DEVELOPMENT_READY' or 'DEVELOPMENT_GOLD_INSUFFICIENT'
      local q={source=cp(v.reference),target=tr,domain=option.domain,building=option.building,price=option.price,cost=row.cost,
       balance=v.balance,turn=Game.GetCurrentGameTurn(),existing=cp(assert(facts.existing[option.domain],'DEVELOPMENT_BUILDING_UNKNOWN'))}
      internal.options[id..':'..option.domain]={quote=q,old=cp(old)}
     end
     emit('DEVELOPMENT_QUOTE',{owner=pid,city=c:GetID(),targetCity=id,contractDomain=option.domain,eventKind=option.building,nativeCost=option.price,principal=row.cost,reason=row.reason,count=option.count})
     options[#options+1]=row
    end
    if #options==0 then options[1]={targetCity=id,targetName=title(target),reason='DEVELOPMENT_NO_BUILDING',canSign=false}end
    return options
   end)
   if okay then for _,row in ipairs(result)do rows[#rows+1]=row end
   else rows[#rows+1]={targetCity=id,targetName=title(target),reason=code(result),canSign=false};failure(result,pid,c:GetID(),'TARGET_QUOTE')end
  end end
  if #rows==0 then v.reason='DEVELOPMENT_NO_OUTGOING'end
  return v,internal
 end
 function d.Refresh(pid,id,withQuotes)
  local c=city(pid,id);if not c then d.views[key(pid,id)]=nil;quotes[key(pid,id)]=nil;openViews[key(pid,id)]=nil;return end
  local ok,v,q=pcall(function()if withQuotes then return snapshot(pid,c)else return sourceFacts(pid,c)end end)
  if not ok then v={stage='HELD',available=d.views[key(pid,id)] and d.views[key(pid,id)].available or false,canSign=false,reason=failure(v,pid,id,'REFRESH'),options={}}end
  if withQuotes then quotes[key(pid,id)]=ok and q or nil;openViews[key(pid,id)]=true
  elseif openViews[key(pid,id)]then
   local previous=d.views[key(pid,id)]
   v.options=previous and cp(previous.options) or {};v.quoteStale=quotes[key(pid,id)]==nil
  end
  publish(pid,id,v)
  if ok then local good,err=pcall(set,c,SPCDevelopmentInvestment.ACCESS,v.available==true);if not good then d.error=failure(err,pid,id,'ACCESS')end end
  return cp(d.views[key(pid,id)])
 end
 function d.Request(pid,p)
  local phase='REQUEST';local packet=type(p)=='table' and p or {};local response
  local ok,err=pcall(function()
   assert(P.IsTestPlayer(pid) and type(p)=='table' and type(p.CityID)=='number' and type(p.Token)=='string' and #p.Token<=100,'DEVELOPMENT_REQUEST_INVALID')
   assert(not busy,'DEVELOPMENT_BUSY');assert(initialize(),'DEVELOPMENT_LOADING')
   local c=assert(city(pid,p.CityID),'DEVELOPMENT_CITY_UNKNOWN')
   if p.Action=='DEVELOPMENT_OPEN' or p.Action=='DEVELOPMENT_REFRESH'then response=d.Refresh(pid,p.CityID,true);return end
   assert(p.Action=='DEVELOPMENT_CONFIRM' and type(p.TargetCity)=='number' and type(p.Domain)=='string','DEVELOPMENT_REQUEST_INVALID')
   local k=key(pid,p.CityID);local view=d.views[k];local cached=quotes[k]
   assert(view and cached and view.revision==p.Revision and view.token==p.CityToken and view.canSign,'DEVELOPMENT_QUOTE_STALE')
   local chosen=p.TargetCity..':'..p.Domain;local old=cached.options[chosen];assert(old,'DEVELOPMENT_QUOTE_STALE')
   -- One fresh confirmation snapshot; no UI-supplied amounts or production conversion.
   phase='REVALIDATE';local current,new=snapshot(pid,c,p.TargetCity);local confirmed=new.options[chosen]
   assert(current.canSign and confirmed and same(old,confirmed),'DEVELOPMENT_QUOTE_STALE')
   local q=confirmed.quote;assert(q.balance>=q.cost and q.cost>0,'DEVELOPMENT_GOLD_INSUFFICIENT')
   assert(not occupancy[q.target.token] and not reservations[q.target.token],'DEVELOPMENT_TARGET_OCCUPIED')
   reservations[q.target.token]=q.source.token -- session-only unknown-outcome reservation
   local value=M.Begin(confirmed.old,q,p.Token);local calling=cp(value);calling.contracts[q.target.token].stage='DEBIT_CALLING'
   busy=true
   local applied,why=pcall(function()
    phase='DEBIT_INTENT_WRITE';write(pid,c,confirmed.old,value,phase)
    phase='DEBIT_CALLING_WRITE';write(pid,c,value,calling,phase)
    phase='NATIVE_DEBIT'
    local before,t=money(pid);assert(before==q.balance,'DEVELOPMENT_TREASURY_CHANGED')
    assert(validateReference(q.source) and validateReference(q.target),'DEVELOPMENT_OWNER_CHANGED')
    local called=pcall(function()t:ChangeGoldBalance(-q.cost)end)
    local readable,after=pcall(money,pid);local actual=readable and after-before or nil
    local accepted=called and readable and M.MoneyMatches(before,-q.cost,after)
    emit('DEVELOPMENT_MONEY',{owner=pid,city=p.CityID,targetCity=p.TargetCity,contractDomain=p.Domain,
     principal=q.cost,nativeCost=q.price,balanceBefore=before,balanceAfter=readable and after or nil,requestedDelta=-q.cost,actualDelta=actual,
     moneyError=actual and actual+q.cost or nil,moneyTolerance=M.MONEY_TOLERANCE,moneyAccepted=accepted,phase=phase,
     submitStatus=called and 'RETURNED' or 'THREW',readStatus=readable and 'READABLE' or 'UNKNOWN'})
    assert(accepted,'DEVELOPMENT_MONEY_UNCONFIRMED')
    assert(validateReference(q.source) and validateReference(q.target),'DEVELOPMENT_OWNER_CHANGED')
    local active=M.Activate(calling,q.target.token,after)
    phase='ACTIVE_RECEIPT_WRITE';write(pid,c,calling,active,phase);reservations[q.target.token]=nil
    phase='EFFECT_APPLY';local target=assert(city(pid,p.TargetCity),'DEVELOPMENT_CITY_UNKNOWN');effect(target,q.domain)
    emit('DEVELOPMENT_SIGNED',{owner=pid,city=p.CityID,targetCity=p.TargetCity,contractID=active.sequence,contractDomain=p.Domain,
     eventKind=q.building,nativeCost=q.price,principal=q.cost,actualDelta=actual,phase='ACTIVE'})
   end)
   busy=false;assert(applied,why)
   d.Reconcile(pid,p.TargetCity);invalidate(pid,p.CityID);response=d.Refresh(pid,p.CityID,true)
  end)
  if not ok then err=failure(err,pid,packet.CityID,phase)
   if type(packet.CityID)=='number' and P.IsTestPlayer(pid)then pcall(function()response=d.Refresh(pid,packet.CityID,true)end)end
  end
  d.lastRequest={owner=pid,city=packet.CityID,token=packet.Token,accepted=ok,reason=ok and response and response.reason or err,phase=phase}
  emit('DEVELOPMENT_REQUEST',{owner=pid,city=packet.CityID,targetCity=packet.TargetCity,requestAction=packet.Action,requestAccepted=ok,reason=d.lastRequest.reason,phase=phase})
  return ok,ok and nil or err
 end
 function d.Describe(pid,c)
  local v=d.views[key(pid,c:GetID())]
  return '发展投资｜'..title(c)..'\n入口：城市生产列表 → 发展投资。\n'..(v and v.used and ('已占用 '..v.used..' / 当前名额 '..v.workers) or '等待城市状态。')
 end
 local function flush()
  if busy or not initialize()then return end
  local todo=dirty;dirty={}
  for pid,changes in pairs(todo)do
   local ids={};for k,v in pairs(shared.Commerce and shared.Commerce.views or {})do local id=tonumber(k:match(':(%d+)$'))
    if k:match('^(%d+):')==tostring(pid) and (changes.all or changes[id])then ids[id]=true end
   end
   for _,r in pairs(records)do if r.reference.owner==pid and (changes.all or changes[r.reference.cityID])then ids[r.reference.cityID]=true end end
   for id in pairs(changes)do if type(id)=='number'then ids[id]=true end end
   for id in pairs(ids)do d.Refresh(pid,id,false)end
  end
 end
 local function building(pid,id,bid)
  local b=P.Info('Buildings',bid);if not b or not catalog.buildings[b.BuildingType] or not P.IsTestPlayer(pid)then return end
  if busy then d.Mark(pid,id);return end
  d.Reconcile(pid,id)
  for k,x in pairs(quotes)do if x.owner==pid then for _,r in pairs(x.options)do if r.quote.target.cityID==id then quotes[k]=nil;d.Mark(pid,r.quote.source.cityID);break end end end end
 end
 local function hook(source,event,fn)local e=P.Field(source,event);if e and e.Add then e.Add(fn)end end
 hook(Events,'LoadScreenClose',flush)
 hook(Events,'GameCoreEventPublishComplete',flush)
 hook(Events,'PlayerTurnActivated',function(pid)if P.IsTestPlayer(pid)then initialize();d.Reconcile(pid);d.Mark(pid);flush()end end)
 for _,n in ipairs({'BuildingConstructed','OnBuildingConstructed'})do hook(GameEvents,n,building)end
 hook(Events,'BuildingAddedToMap',function(x,y,bid,pid)
  local b=P.Info('Buildings',bid);if not b or not catalog.buildings[b.BuildingType] or not P.IsTestPlayer(pid)then return end
  local district=CityManager.GetDistrictAt and CityManager.GetDistrictAt(x,y)
  local c=district and district:GetCity() or CityManager.GetCityAt(x,y)
  if c and c:GetOwner()==pid then building(pid,c:GetID(),bid)end
 end)
 hook(Events,'CityTransfered',function(newOwner,newID,oldOwner)
  if type(oldOwner)=='number' and P.IsTestPlayer(oldOwner)then d.Reconcile(oldOwner);d.Audit({player=oldOwner})end
 end)
 for _,n in ipairs({'TreasuryChanged','PlayerTreasuryChanged','PlayerGoldChanged'})do hook(Events,n,function(pid)d.Audit({player=pid})end)end
 store.RegisterExit('DevelopmentInvestment',function(c,loss)
  store.RemoveOwned(c,loss,names);d.Mark(loss.origin.owner)
 end)
 store.RegisterReturn('DevelopmentInvestment',function(pid,c)invalidate(pid,c:GetID())end)
 local previous=shared.OnPermanentCityWrite
 shared.OnPermanentCityWrite=function(c,reason)if previous then previous(c,reason)end;if c then invalidate(c:GetOwner(),c:GetID())end end
 return d
end
