-- Explicit propagation edges. Collected scopes are disposable scalars; gameplay policy stays in each owner.
SPCFactConsumerBindings={}
function SPCFactConsumerBindings.New(shared)
 local d={errors={}};shared.FactBindings=d
 local pending,receiptCounts={},{};local networkDrains={};local registry=shared.FactChanges;local deliveryNames={}
 local function target(name)
  local value=shared[name];local state=shared.StartStatus and shared.StartStatus[name]
  if value and not value.startupError and not (state and (state.state=='FAILED' or state.state=='SKIPPED_DEPENDENCY'))then return value end
 end
 local role={'IDENTITY','POTENTIAL','ACTIVE'}
 -- All own-state synchronizations precede the one owner-wide network sample.
 shared.FactChanges.RegisterConsumer('RestructuringSync',function(e)
  local value=target('Restructuring');if not value or not value.FactChanged then return end
  local result,reason=value.FactChanged(e)
  if result~=true and result~='IRRELEVANT' then error(reason or 'REST_SYNC_UNCONFIRMED',0)end
 end,{kinds=role,phase=0})
 shared.FactChanges.RegisterConsumer('NetworkBridge',function(e)
  local value=target('NetworkBridge');local revision=shared.FactChanges.flushRevision
  if value and networkDrains[e.player]~=revision then networkDrains[e.player]=revision;(value.RefreshFacts or value.Refresh)(e.player)end
 end,{kinds=role,phase=0})
 local declarations={
  {target='Standardization',method='Refresh',cityOnly=true,kinds={'IDENTITY'}},
  {target='ResearchSupport',method='Audit',ordered='AcceptFact',kinds={'IDENTITY','POTENTIAL','ACTIVE','D'}},
  {target='Lv2Housing',method='Audit',ordered='AcceptFact',kinds={'IDENTITY','POTENTIAL','ACTIVE','D'}},
  {target='Lv2GPP',method='Audit',ordered='AcceptFact',kinds={'IDENTITY','POTENTIAL','ACTIVE','D','WORKERS'}},
  {target='IndustrySupport',method='Audit',ordered='AcceptFact',cityOnly=true,ownerCauses={REQUEST_FACTS_DIRTY=true,DISTRICT_FACTS_DIRTY=true},kinds={'D'}},
  {target='Lv3Support',method='Audit',kinds=role},
  {target='Lv3Effects',method='Audit',kinds={'IDENTITY','POTENTIAL','ACTIVE','D','WORKERS','NETWORK'}},
  {target='Lv4Percent',method='Audit',kinds={'IDENTITY','POTENTIAL','ACTIVE','D','WORKERS'}},
  {target='ResearchInfrastructure',method='Audit',ordered='AcceptFact',kinds={'IDENTITY','POTENTIAL','ACTIVE','D','WORKERS'}},
  {target='ResearchCross',method='Audit',ordered='AcceptFact',sample=true,kinds={'IDENTITY','POTENTIAL','ACTIVE','D'}},
  {target='ResearchApply',method='Audit',ordered='AcceptFact',kinds={'IDENTITY','POTENTIAL','ACTIVE','D','WORKERS'}},
  {target='ResearchChair',method='Audit',ordered='AcceptFact',kinds={'IDENTITY','POTENTIAL','ACTIVE','D','WORKERS'}},
  {target='CultureAesthetic',method='Audit',ordered='AcceptFact',kinds={'IDENTITY','POTENTIAL','ACTIVE','D'}},
  {target='CultureMeaning',method='Audit',ordered='AcceptFact',kinds={'IDENTITY','POTENTIAL','ACTIVE','D'}},
  {target='CultureInspiration',method='Audit',ordered='AcceptFact',kinds={'IDENTITY','POTENTIAL','ACTIVE','D'}},
  {target='CultureInsightsTourism',method='Audit',ordered='AcceptFact',kinds={'IDENTITY','POTENTIAL','ACTIVE','HISTORY'},topics={'INSIGHTS'}},
  {target='DialogueEffects',method='Audit',ordered='AcceptFact',kinds={'IDENTITY','POTENTIAL','ACTIVE','HISTORY'},topics={'DIALOGUE'}},
  {target='ResearchTraditionEffects',takeover='AcceptFact',kinds={'IDENTITY','POTENTIAL','ACTIVE','HISTORY'},topics={'TRADITION'}},
  {target='StandardizationEffects',method='Audit',ordered='AcceptFact',source=true,request=true,kinds={'IDENTITY','POTENTIAL','ACTIVE','NETWORK','HISTORY'},topics={'TEMPLATES','ENGINEERING'}},
  {target='CultureNetwork',method='Audit',ordered='AcceptFact',source=true,request=true,kinds={'IDENTITY','POTENTIAL','ACTIVE','D','NETWORK','HISTORY'},topics={'INSIGHTS'}},
  {target='EngineeringStudy',method='CreditChanged',kinds={'HISTORY'},topics={'WONDER_CREDIT'}},
  {target='DialogueProjects',method='RefreshAccess',cityOnly=true,kinds=role},
  {target='Commerce',takeover='AcceptFact',kinds={'IDENTITY','POTENTIAL','ACTIVE','D','WORKERS','HISTORY','NETWORK'},topics={'COMMERCE'}},
  {target='CapitalInvestment',takeover='AcceptFact',kinds={'IDENTITY','POTENTIAL','ACTIVE','NETWORK','HISTORY'},topics={'CAPITAL_RECOVERY'}},
  {target='DevelopmentInvestment',takeover='AcceptFact',kinds={'NETWORK'}},
 }
 local function ownerAllowed(row,e)
  if not row.ownerCauses then return false end
  for cause in pairs(row.ownerCauses)do if e.causes[cause]then return true end end
  return false
 end
 local function collect(row,e,resolve,signal)
  if row.ownerCauses and e.city==nil and not ownerAllowed(row,e)then
   if resolve then return registry.Receipt(e,'IRRELEVANT','OUTSIDE_AUDIT_SCOPE')end
   return
  end
  if resolve then
   assert((receiptCounts[row.target] or 0)<registry.ReceiptSlotsPerReceiver(),'FACT_BINDING_RECEIPT_LIMIT')
  end
  local owners=pending[row.target] or {};pending[row.target]=owners
  local key=tostring(e.player);local q=owners[key]
  if not q then q={player=e.player,cities={},order={},proofs={},references={},topics={},causes={}};owners[key]=q end
  if signal then q[signal]=true;return end
  if e.city==nil then q.all=true;q.proofs={}
  elseif not q.cities[e.city]then
   assert(#q.order<2048,'FACT_BINDING_SCOPE_LIMIT');q.cities[e.city]=true;q.order[#q.order+1]=e.city;q.references[e.city]=e.reference
  elseif q.references[e.city]~=e.reference then q.proofs[e.city]=nil;q.conflicting=true end
  if not q.all and not q.conflicting and e.investment then q.proofs[e.city]=e.investment end
  for name in pairs(e.topics)do q.topics[name]=true end
  for name in pairs(e.causes)do q.causes[name]=true end
  if resolve then
   local receipt=registry.Receipt(e,'REGISTERED')
   local key=e.city or false;q.receipts=q.receipts or {}
   local group=q.receipts[key] or {};q.receipts[key]=group
   group[#group+1]=function(accepted)resolve(accepted and receipt or nil)end
   receiptCounts[row.target]=(receiptCounts[row.target] or 0)+1
   return true
  end
 end
 local function takeover(row,e)
  local value=target(row.target);local receipt
  local ok,err=pcall(function()
   assert(value and type(value[row.takeover])=='function','FACT_BINDING_TARGET_UNAVAILABLE')
   receipt=value[row.takeover](e)
   assert(registry.AcceptsReceipt(e,receipt),'FACT_BINDING_NOT_REGISTERED')
  end)
  if not ok then
   local safe,text=pcall(tostring,err);d.errors[row.target]=safe and text:sub(1,180) or 'FACT_BINDING_FAILED'
   error(d.errors[row.target],0)
  end
  d.errors[row.target]=nil;return receipt
 end
 function d.Wake(name,cause,revision,scope)
  local consumer=deliveryNames[name]
  return consumer and registry.WakeConsumer(consumer,cause,revision,scope)or false
 end
 local function subscribeLegacy(row,callback,suffix)
  local remaining={};local name='Binding_'..row.target..(suffix or '')
  for _,kind in ipairs(row.kinds)do
   local provider=kind=='D' and shared.DistrictCompleteness or kind=='NETWORK' and shared.NetworkBridge
   if provider and type(provider.RegisterConsumer)=='function'then provider.RegisterConsumer(name,callback)
   else remaining[#remaining+1]=kind end
  end
  if #remaining>0 then registry.RegisterConsumer(name,callback,{kinds=remaining,topics=row.topics})end
 end
 for _,row in ipairs(declarations)do
  if row.takeover then
   -- Reserve one obligation for the owner's combined scope, including when
   -- phase0 adds a Network proof to an already queued role fact.
   deliveryNames[row.target]=registry.RegisterConsumer('Binding_'..row.target,
    function(e)return takeover(row,e)end,{kinds=row.kinds,topics=row.topics,delivery='RESPONSIBILITY'})
  elseif row.ordered then
   deliveryNames[row.target]=registry.RegisterConsumer('Binding_'..row.target,function(e,resolve)
    return collect(row,e,resolve)
   end,{kinds=row.kinds,topics=row.topics,delivery='RESPONSIBILITY',ordered=true})
   -- Keep the existing sampler dirty signal tied to new producer causes.
   -- A held effect audit waking on availability must not ask UI to resample.
   if row.sample then subscribeLegacy(row,function(e)collect(row,e,nil,'sample')end,'_Source')end
   -- A fresh history cause may request the existing proof. Receipt recovery
   -- alone must not repeat that side effect from retained history.
   if row.request then subscribeLegacy(row,function(e)
    if next(e.topics)then collect(row,e,nil,'requestProof')end
   end,'_Proof')end
  else
   subscribeLegacy(row,function(e)collect(row,e)end)
  end
 end
 local function complete(groups,accepted,city)
  for _,q in pairs(groups)do
   local receipts=q.receipts
   if receipts and city~=nil then
    for _,resolve in ipairs(receipts[city] or {})do resolve(accepted)end
    receipts[city]=nil
   elseif receipts then
    for _,group in pairs(receipts)do for _,resolve in ipairs(group)do resolve(accepted)end end
    q.receipts=nil
   end
  end
 end
 local function invoke(row,q,covered)
  local value=target(row.target);local fn=value and value[row.ordered or row.method]
  if type(fn)~='function'then
   if row.ordered then complete(covered,false);error('FACT_BINDING_TARGET_UNAVAILABLE',0)end
   return
  end
  local failure
  -- C2 producer gets only real declared input causes, never a global write pulse
  -- or its own sample reply. This is a scalar wake, not an extra fact read.
  local sample=not row.ordered and row.sample;local hasScope=not row.ordered
  if covered then for _,group in pairs(covered)do
   if group.sample then sample=true end
   if group.receipts then hasScope=true end
  end end
  if sample and type(value.SampleChanged)=='function'then
   local ok=pcall(value.SampleChanged);if not ok then failure='SAMPLE_CAUSE_NOTIFY_FAILED'end
  end
  if not hasScope then if failure then error(failure,0)end;return end
  local function call(...)
   if registry.closed or shared.FactChanges~=registry then return false end
   local ok,result=pcall(fn,...)
   if not ok then local safe,text=pcall(tostring,result);failure=safe and text:sub(1,180) or 'FACT_BINDING_FAILED'
   elseif row.ordered and result~=true then failure='FACT_BINDING_NOT_REGISTERED'end
   return ok and result==true
  end
  if row.cityOnly and q.all and not ownerAllowed(row,q)then
   for _,id in ipairs(q.order)do
    if row.method=='Audit'then
     local accepted=call({player=q.player,city=id})
     if row.ordered then complete(covered,accepted,id)end
    else call(q.player,id)end
   end
   if failure then error(failure,0)end;return
  end
  if row.source then
   local accepted=call({player=q.player,changed=not q.all and q.cities or nil})
   complete(covered,accepted)
   if q.requestProof then
    local bridge=target('NetworkBridge');if bridge and bridge.RequestPendingProof then bridge.RequestPendingProof(q.player)end
   end
  elseif row.method=='Audit'then
   if q.all then
    local accepted=call({player=q.player})
    if row.ordered then complete(covered,accepted)end
   else for _,id in ipairs(q.order)do
    local proof=not q.conflicting and not q.causes.RESTRUCTURING_COMMITTED and q.proofs[id] or nil
    local accepted=call({player=q.player,city=id,investment=proof})
    if row.ordered then complete(covered,accepted,id)end
   end end
  elseif row.method=='CreditChanged' then call(q.player)
  elseif q.all then call(q.player)
  else for _,id in ipairs(q.order)do call(q.player,id)end end
  if failure then error(failure,0)end
 end
 function d.Flush()
  if registry.closed or shared.FactChanges~=registry then pending={};receiptCounts={};return false end
  if d.busy then return false end;d.busy=true
  local work=pending;pending={};receiptCounts={}
  for _,row in ipairs(declarations)do
   local owners=work[row.target] or {};local global=owners['nil']
   -- A real all-player Audit already contains the known owner/city scopes.
   -- City-only methods deliberately ignore global fallback and keep their narrow work.
   local collapse=global and global.all and (not row.cityOnly or ownerAllowed(row,global)) and (row.method=='Audit' or row.source)
   local selected=collapse and {global=global} or owners
   for _,q in pairs(selected)do
    local covered=row.ordered and (collapse and owners or {q}) or nil
    local ok,err=pcall(invoke,row,q,covered)
    if covered then complete(covered,false)end -- any unvisited receipt stays held
    if ok then d.errors[row.target]=nil else local safe,value=pcall(tostring,err);d.errors[row.target]=safe and value:sub(1,180) or 'FACT_BINDING_FAILED'end
   end
  end
  d.busy=false;return true
 end
 return d
end
