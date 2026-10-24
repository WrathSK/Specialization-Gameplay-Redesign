include('NetworkInput')
include('RuntimeWork')
include('ExpeditionTrainingDiagnostics')
-- B235: template-holder-specific III/IV projection. Store owns knowledge/L;
-- Bridge owns topology. One final-value carrier per target, no purchase unlock.
SPCStandardizationEffects={}
function SPCStandardizationEffects.Start(P,shared)
 local d={ready=false,busy=false,records={},errors={},changes=0};shared.StandardizationEffects=d
 local catalog,definitions,byTarget;local dirty={};local initialized=false;local cleaned={}
 local ownedIndex={};local healthSequence=0
 local trace=SPCExpeditionTrainingDiagnostics and SPCExpeditionTrainingDiagnostics.New(P,'INDUSTRY_STANDARDIZATION')
 local function key(pid,cid)return tostring(pid)..':'..tostring(cid)end
 local function ref(c)return SPCNetworkInput.Reference(c)end
 local function code(s)return type(s)=='string' and (s:match('(STD_[A-Z_]+)') or s:match('(NETWORK_[A-Z_]+)') or s:match('(STORE_[A-Z_]+)') or s:match('(EST_[A-Z_]+)')) or 'STD_READ_PENDING'end
 local function mark(pid,cid)
  if pid==nil then for owner in pairs(Players)do if P.IsTestPlayer(owner)then mark(owner,cid)end end;return end
  if not P.IsTestPlayer(pid)then return end
  local q=dirty[pid] or {cities={}};dirty[pid]=q
  if cid==nil then q.all=true else q.cities[cid]=true end
 end
 local carrierHealth=SPCRuntimeWork.NativeHealth(P,shared,d,function(id)return ownedIndex[id]==true end,function(scope)
  healthSequence=healthSequence+1
  local function owner(pid)
   if not P.IsTestPlayer(pid)then return end
   if scope.city~=nil then
    local r=d.records[key(pid,scope.city)];if r then r.healthTicket=healthSequence end
   else for _,r in pairs(d.records)do if r.owner==pid then r.healthTicket=healthSequence end end end
   mark(pid,scope.city)
  end
  if scope.player~=nil then owner(scope.player)else for pid in pairs(Players)do owner(pid)end end
 end)
 local function validate()
  if definitions then return end
  local cat=SPCStandardizationCatalog.Build(P);local rows,map,nextOwned={},{},{}
  for _,r in ipairs(P.Rows('SPC_StandardizationTargets'))do
   assert(r.Kind=='BUILDING' or r.Kind=='DISTRICT','STD_TARGET_KIND')
   local t=r.Kind..':'..r.TargetType;assert(not map[t],'STD_TARGET_DUPLICATE')
   local entry=r.Kind=='BUILDING' and cat.buildings[r.TargetType] or cat.districts[r.TargetType]
   assert(entry and (r.Kind~='BUILDING' or entry.enabled),'STD_TARGET_CATALOG_MISMATCH')
   local b=assert(P.Info('Buildings',r.CarrierType),'STD_CARRIER_MISSING')
   assert((b.InternalOnly==true or b.InternalOnly==1) and b.PrereqDistrict=='DISTRICT_CITY_CENTER'
    and b.CitizenSlots==0 and b.Housing==0,'STD_CARRIER_INVALID')
   local row={index=b.Index,id=r.CarrierType,kind=r.Kind,target=r.TargetType,key=t,name=entry.name}
   nextOwned[row.index]=true;row.amount=10;row.levels={[10]=row};rows[#rows+1]=row;map[t]=row
  end
  for id,b in pairs(cat.buildings)do if b.enabled then assert(map['BUILDING:'..id],'STD_BUILDING_TARGET_MISSING')end end
  for id in pairs(cat.districts)do assert(map['DISTRICT:'..id],'STD_DISTRICT_TARGET_MISSING')end
  for _,r in ipairs(P.Rows('SPC_StandardizationLevels'))do
   local t=r.Kind..':'..r.TargetType;local base=assert(map[t],'STD_LEVEL_TARGET_MISSING')
   assert(type(r.Level)=='number' and r.Level>0 and r.Level%1==0,'STD_LEVEL_INVALID')
   local b=assert(P.Info('Buildings',r.CarrierType),'STD_CARRIER_MISSING');local amount=10+2*r.Level
   assert((b.InternalOnly==true or b.InternalOnly==1) and b.PrereqDistrict=='DISTRICT_CITY_CENTER'
    and b.CitizenSlots==0 and b.Housing==0 and not base.levels[amount],'STD_LEVEL_INVALID')
   local row={index=b.Index,id=r.CarrierType,kind=r.Kind,target=r.TargetType,key=t,name=base.name,amount=amount}
   base.levels[amount]=row;rows[#rows+1]=row;nextOwned[row.index]=true
  end
  assert(#rows>0,'STD_TARGETS_EMPTY');catalog,definitions,byTarget,ownedIndex=cat,rows,map,nextOwned
 end
 local function present(c)
  local out={};local b=c:GetBuildings()
  for _,r in ipairs(definitions)do
   local has=P.HasBuilding(b,r.index);assert(type(has)=='boolean','STD_CARRIER_UNKNOWN')
   if has then assert(not out[r.key],'STD_MULTIPLE_FINAL_VALUES');out[r.key]=r.amount end
  end
  return out
 end
 local function missingWanted(c,old,want)
  local missing={};local b=c:GetBuildings()
  -- Sample every requested equal-value slot before any native mutation. This is
  -- proportional to wanted targets, never all level definitions.
  for t,amount in pairs(want)do if old[t]==amount then
   local row=assert(byTarget[t] and byTarget[t].levels[amount],'STD_LEVEL_DEFINITION_MISSING')
   local has=P.HasBuilding(b,row.index);assert(type(has)=='boolean','STD_HEALTH_PRESENCE_UNKNOWN')
   if not has then missing[t]=true end
  end end
  return missing
 end
 local function write(c,old,want,missing)
  -- Remove before adding; changed entries only after initial ownership read.
  local b=c:GetBuildings()
  for t,amount in pairs(old)do if want[t]~=amount then
   local r=assert(byTarget[t] and byTarget[t].levels[amount],'STD_OWNED_TARGET_UNKNOWN')
   local has=P.HasBuilding(b,r.index);assert(type(has)=='boolean','STD_REMOVE_PRESENCE_UNKNOWN')
   if has then carrierHealth.Remove(c,r.index);assert(P.HasBuilding(b,r.index)==false,'STD_REMOVE_UNCONFIRMED')end
   old[t]=nil;d.changes=d.changes+1
  end end
  for t,amount in pairs(want)do if old[t]~=amount or missing and missing[t]then
   local r=assert(byTarget[t] and byTarget[t].levels[amount],'STD_LEVEL_DEFINITION_MISSING')
   local has=P.HasBuilding(b,r.index);assert(type(has)=='boolean','STD_ADD_PRESENCE_UNKNOWN')
   if not has then carrierHealth.Create(c,r.index);assert(P.HasBuilding(b,r.index)==true,'STD_ADD_UNCONFIRMED')end
   old[t]=amount;d.changes=d.changes+1
  end end
 end
 local function retire(c)
  local k=key(c:GetOwner(),c:GetID());local reference=ref(c)
  if cleaned[k]==reference then return end
  local before=shared.StandardizationDiscount.changes+shared.CopyYields.changes
  assert(shared.StandardizationDiscount.retired and shared.CopyYields.retired,'STD_LEGACY_WRITER_ACTIVE')
  assert(shared.StandardizationDiscount.Withdraw(c),'STD_LEGACY_DISCOUNT_PENDING')
  assert(shared.CopyYields.Withdraw(c),'STD_LEGACY_COPY_PENDING')
  cleaned[k]=reference
  local removed=shared.StandardizationDiscount.changes+shared.CopyYields.changes-before
  if trace and removed>0 then trace.Record('INDUSTRY_LEGACY_EXIT',{owner=c:GetOwner(),city=c:GetID(),count=removed,readStatus='VERIFIED',reason='EXACT_OWNED_IDS'})end
 end
 local function source(batch,pid,id)
  if batch.sources[id]then return batch.sources[id]end
  local result={targets={},eligible=false,provenance='CONFIRMED'};batch.sources[id]=result
  local ok,why=pcall(function()
   local c=Players[pid]:GetCities():FindID(id)
   if c then assert(type(c:GetOwner())=='number','STD_SOURCE_OWNER_UNKNOWN')end
   if not c or c:GetOwner()~=pid then result.confirmedLoss=true;return end
   result.reference=ref(c)
   local f=shared.EffectiveFacts.Read(pid,c)
   assert(type(f.specialization)=='string','STD_SOURCE_UNKNOWN')
   if f.specialization~='INDUSTRY'then return end
   assert(type(f.active)=='number' and f.active%1==0 and f.active>=0 and f.active<=4,'STD_ACTIVE_UNKNOWN')
   if f.active<3 then return end
   result.eligible=true
   local amount=10
   if f.active==4 then
    local state=shared.CityProgressionStore.EngineeringState(pid,c)
    assert(state.token==f.token,'STD_SOURCE_REFERENCE_CHANGED')
    amount=10+2*(state.value and state.value.L or 0)
   end
   result.ceiling=amount
   local ledger=shared.Standardization.ReadKnowledge(pid,c)
   local groups,bases={},{}
   for id,row in pairs(ledger.learned)do
    local b=catalog.buildings[id]
    if b and b.district==row.district and b.tier==row.tier then
     if b.enabled then groups[b.group]=true end
    else result.warning='STD_RETAINED_CLASSIFICATION_UNAVAILABLE'end
   end
   if ledger.districts then
    for base,row in pairs(ledger.districts.learned)do
     local current=catalog.districts[row.observedType]
     if current and current.base==base then bases[base]=true
     else result.warning='STD_RETAINED_CLASSIFICATION_UNAVAILABLE'end
    end
   else result.warning='STD_DISTRICT_HISTORY_PENDING'end
   for t,r in pairs(byTarget)do
    local matches=r.kind=='BUILDING' and groups[catalog.buildings[r.target].group]
     or r.kind=='DISTRICT' and bases[catalog.districts[r.target].base]
    if matches then assert(r.levels[amount],'STD_LEVEL_DEFINITION_MISSING');result.targets[t]=amount end
   end
   assert(c:GetOwner()==pid and ref(c)==result.reference,'STD_SOURCE_CHANGED')
  end)
  if not ok then result.error=code(why);result.targets={}end
  return result
 end
 local function network(batch,pid)
  local bridge=assert(shared.NetworkBridge,'STD_NETWORK_UNAVAILABLE')
  local input=bridge.Input(pid)
  if input.validity=='CONFIRMED_INVALID'then return {input=input,recipients={}}end
  local view=bridge.CurrentIndustryBatch(pid)
  assert(view.input.validity=='VERIFIED' and (view.input.effectAvailability=='AVAILABLE' or view.input.effectAvailability==nil and view.input.availability=='AVAILABLE' or view.input.continuityOnly),'STD_NETWORK_PENDING')
  return view
 end
 local function plan(batch,pid,c,old)
  local wanted,sources,ids={}, {},{[c:GetID()]=true};local reason=batch.networkError
  local continuity=batch.networkError~=nil or batch.view and batch.view.input.continuityOnly
  if batch.view then for id in pairs(batch.view.recipients[c:GetID()] or {})do ids[id]=true end
  else for id in pairs(old.sources or {})do ids[id]=true end end
  local removed=false
  for id in pairs(ids)do
   local s=source(batch,pid,id);local prior=old.sources[id];local targets=s.targets;local status='CONFIRMED'
   if s.error then
    reason=s.error;local retain=prior and not s.confirmedLoss and (s.reference==nil or prior.reference==s.reference)
    targets=retain and prior.targets or {}
    status=retain and 'RETAINED' or 'UNKNOWN'
    if retain and s.reference==nil then s.reference=prior.reference end
   elseif continuity and s.eligible then
    targets=prior and prior.reference==s.reference and prior.targets or {}
    status=prior and prior.reference==s.reference and 'RETAINED' or 'UNKNOWN'
   elseif s.warning then reason=s.warning end
   if prior and s.ceiling then
    local limited={}
    for t,amount in pairs(targets)do limited[t]=math.min(amount,s.ceiling);if limited[t]<amount then removed=true end end
    targets=limited
   end
   if prior and next(prior.targets) and (s.confirmedLoss or not s.error and not s.eligible or s.reference and prior.reference~=s.reference)then removed=true end
   sources[id]={reference=s.reference,targets=targets,provenance=status,reason=s.error}
   for t,amount in pairs(targets)do wanted[t]=math.max(wanted[t] or 0,amount)end
  end
  if continuity then
   reason=reason or 'STD_RETAINED_TOPOLOGY'
   for id in pairs(old.sources)do if not ids[id]then removed=true end end
   -- The local/network physical result is inseparable. Pending topology never
   -- adds newly calculated self values; only a confirmed negative may withdraw
   -- decomposed contributions. A cold installed aggregate uses exception A.
   if old.loaded or not removed then
    local retained={}
    for id,prior in pairs(old.sources)do
     local targets={};for t,amount in pairs(prior.targets)do targets[t]=amount end
     retained[id]={reference=prior.reference,targets=targets,provenance=prior.provenance=='UNKNOWN' and 'UNKNOWN' or 'RETAINED',reason=reason}
    end
    return old.applied,retained,reason,old.loaded,true
   end
  end
  if old.loaded and reason then return old.applied,sources,'STD_COLD_AGGREGATE_RETAINED',true,true end
  return wanted,sources,reason,false,false
 end
 local function observe(pid,c,r,reason,force)
  local b,n,src,maxAmount=0,0,0,0
  local changed=false
  for t,amount in pairs(r.applied)do
   if byTarget[t].kind=='BUILDING'then b=b+1 else n=n+1 end;maxAmount=math.max(maxAmount,amount)
   if not r.observedValues or r.observedValues[t]~=amount then changed=true end
  end
  for _ in pairs(r.sources or {})do src=src+1 end
  local sig=tostring(b)..':'..n..':'..src..':'..tostring(reason)
  if force or changed or sig~=r.observed then
   if trace then trace.Record('INDUSTRY_STANDARDIZATION',{owner=pid,city=c:GetID(),templateCount=b,districtTemplateCount=n,
    sourceCount=src,expected=maxAmount,readStatus=reason and 'PENDING' or 'VERIFIED',reason=reason or 'STD_READY'})end
   -- Preserve exact diagnostics without rebuilding sorted display strings on
   -- unchanged notifications. This bounded snapshot is replaced, not appended.
   r.observedValues={};for t,amount in pairs(r.applied)do r.observedValues[t]=amount end
  end
  r.observed=sig
 end
 local function reconcile(batch,pid,c)
  local k=key(pid,c:GetID());local reference=ref(c);local old=d.records[k]
  if not old or old.reference~=reference then
   retire(c) -- A failed exact withdrawal prevents the replacement writer.
   local installed=present(c)
   old={owner=pid,city=c:GetID(),reference=reference,applied=installed,sources={},loaded=next(installed)~=nil};d.records[k]=old
  end
  local wanted,sources,reason,loaded,held=plan(batch,pid,c,old)
  assert(c:GetOwner()==pid and ref(c)==reference,'STD_RECEIVER_CHANGED')
  local ticket=old.healthTicket
  local repair=ticket and not held and not reason and not batch.networkError
   and batch.view and not batch.view.input.continuityOnly
  local missing=repair and missingWanted(c,old.applied,wanted) or nil
  assert(c:GetOwner()==pid and ref(c)==reference,'STD_RECEIVER_CHANGED')
  if not held then write(c,old.applied,wanted,missing)end
  -- A native callback during the write owns a later ticket and cannot be ACKed.
  if repair and old.healthTicket==ticket then old.healthTicket=nil end
  old.sources=sources;old.loaded=loaded;old.retained=held;d.errors[k]=reason
  observe(pid,c,old,reason)
 end
 function d.Audit(scope)
  local store=shared.CityProgressionStore
  if store and store.HistoryStartStatus and store.HistoryStartStatus()=='WAITING'then return end
  if d.busy then
   if scope and scope.changed then for cid in pairs(scope.changed)do mark(scope.player,cid)end
   else mark(scope and scope.player,scope and scope.city)end
   return
  end
  d.busy=true
  local good,why=pcall(function()
   validate()
   if not initialized then
    -- Exact historical owners, once per context; no all-world turn cleanup.
    for pid,p in pairs(Players)do
     local cities=p:GetCities()
     if cities then for _,c in cities:Members()do
      retire(c)
      if not P.IsTestPlayer(pid)then write(c,present(c),{})end
     end end
    end
    initialized=true;d.ready=true
   end
   for pid,p in pairs(Players)do if P.IsTestPlayer(pid) and (not scope or scope.player==nil or scope.player==pid)then
    local batch={sources={}};local ok,view=pcall(network,batch,pid)
    if ok then batch.view=view else batch.networkError=code(view)end
    local changed=scope and (scope.changed or scope.city~=nil and {[scope.city]=true});local live={}
    for _,c in p:GetCities():Members()do
     local cid=c:GetID();local k=key(pid,cid);live[k]=true;local old=d.records[k]
     local visit=not changed or changed[cid] or not old
     if changed then
      for id in pairs(ok and view.recipients[cid] or {})do if changed[id]then visit=true end end
      for id in pairs(old and old.sources or {})do if changed[id]then visit=true end end
     end
     if visit then
      local success,err=pcall(reconcile,batch,pid,c)
      if not success then d.errors[k]=code(err)
       if trace then trace.Record('INDUSTRY_STANDARDIZATION',{owner=pid,city=cid,readStatus='PENDING',reason=d.errors[k]})end
      end
     end
    end
    for k,r in pairs(d.records)do if r.owner==pid and not live[k]then d.records[k]=nil;d.errors[k]=nil;cleaned[k]=nil end end
   end end
  end)
  d.error=not good and code(why) or nil;d.busy=false
  if d.error and trace then trace.Record('INDUSTRY_STANDARDIZATION',{readStatus='PENDING',reason=d.error})end
 end
 function d.SourceChanged(pid,cid)
  if not P.IsTestPlayer(pid)then return end
  d.Audit({player=pid,changed={[cid]=true}})
  if shared.NetworkBridge.RequestPendingProof then
   local ok,err=pcall(shared.NetworkBridge.RequestPendingProof,pid)
   d.errors['network-request:'..pid]=not ok and code(err) or nil
  end
 end
 local function flush()
  if d.busy then return end
  local todo=dirty;dirty={}
  for pid,q in pairs(todo)do d.Audit({player=pid,changed=not q.all and q.cities or nil})end
 end
 function d.Describe(pid,c,page)
  local r=d.records[key(pid,c:GetID())];local reason=d.errors[key(pid,c:GetID())] or d.error
  if not r then return '工业标准化 | '..c:GetName()..'\n等待：'..tostring(reason or 'STD_NOT_READY')end
  local ids={};for t in pairs(r.applied)do ids[#ids+1]=t end;table.sort(ids)
  local pages=math.max(1,math.ceil(#ids/5));page=(math.max(1,tonumber(page) or 1)-1)%pages+1
  local names={};for id in pairs(r.sources)do
   local sourceCity=Players[pid]:GetCities():FindID(id)
   names[#names+1]=sourceCity and sourceCity:GetName() or tostring(id)
  end;table.sort(names)
  local out={'工业标准化 | '..c:GetName(),'三级建造 +10% / 购买折扣 0%；四级持有者每层研习各 +2 个百分点',
   '来源：'..(#names>0 and table.concat(names,'、') or '无合格模板来源'),
   '匹配目标 '..#ids..' | 页 '..page..'/'..pages}
  for i=(page-1)*5+1,math.min(page*5,#ids)do
   local row=byTarget[ids[i]];out[#out+1]=(row.kind=='DISTRICT' and '区域：' or '建筑：')..Locale.Lookup(row.name)..' 建造 +'..r.applied[ids[i]]..'% / '..(row.kind=='BUILDING' and ('购买折扣 '..(r.applied[ids[i]]-10)..'%') or '区域购买折扣待接口')
  end
  out[#out+1]='状态：'..tostring(reason or '正常')
  out[#out+1]='仅加速本来合法的普通建筑／区域；不含奇观，不授予建造或购买权限。'
  out[#out+1]='各模板只取实际持有者最大值；区域逐模板购买折扣未接入。配置须与原生进度／价格核对。'
  observe(pid,c,r,reason,true)
  if shared.ConstructionProbe and shared.ConstructionProbe.ReadSnapshot then
   local ok,q=pcall(shared.ConstructionProbe.ReadSnapshot,pid,c)
   if ok then
    out[#out+1]='当前生产进度：'..q.progress..' / '..q.cost
    if trace then trace.Record('INDUSTRY_CONSTRUCTION_REPORT',{owner=pid,city=c:GetID(),eventKind=q.kind,
     requested=q.target,nativeProgress=q.progress,nativeCost=q.cost,expected=r.applied[(q.kind=='Buildings' and 'BUILDING:' or 'DISTRICT:')..q.target] or 0})end
   else out[#out+1]='当前生产进度未读取；请以原生生产列表为准。'end
  end
  return table.concat(out,'\n')
 end
 local function hook(src,n,f)local e=P.Field(src,n);if e and e.Add then e.Add(f)end end
 local function all()for pid in pairs(Players)do mark(pid)end end
 hook(Events,'LoadScreenClose',function()all();flush()end)
 hook(Events,'GameCoreEventPublishComplete',function()
  if not initialized then all()end;flush()
 end)
 hook(Events,'PlayerTurnActivated',function(pid)mark(pid);flush()end)
 -- NativeFacts owns governor qualification causes; declared ACTIVE delivery is deferred.
 hook(Events,'CityTransfered',function()initialized=false;cleaned={};all();flush()end)
 -- Store confirmed loss owns destination reference proof; no guessed coordinates.
 local store=shared.CityProgressionStore
 if store then
  store.RegisterExit('StandardizationEffects',function(c,loss)
   validate();cleaned[key(c:GetOwner(),c:GetID())]=nil;retire(c);local ids={};for _,r in ipairs(definitions)do ids[#ids+1]=r.id end
   store.RemoveOwned(c,loss,ids)
   d.records[key(loss.origin.owner,loss.origin.cityID)]=nil;d.errors[key(loss.origin.owner,loss.origin.cityID)]=nil
   cleaned[key(loss.origin.owner,loss.origin.cityID)]=nil
   mark(loss.origin.owner);mark(c:GetOwner())
  end)
  store.RegisterReturn('StandardizationEffects',function(pid,c)mark(pid,c:GetID())end)
 end
end
