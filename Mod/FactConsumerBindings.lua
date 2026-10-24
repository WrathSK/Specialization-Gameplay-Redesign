-- Explicit propagation edges. Collected scopes are disposable scalars; gameplay policy stays in each owner.
SPCFactConsumerBindings={}
function SPCFactConsumerBindings.New(shared)
 local d={errors={}};shared.FactBindings=d
 local pending={};local networkDrains={}
 local function target(name)
  local value=shared[name];local state=shared.StartStatus and shared.StartStatus[name]
  if value and not value.startupError and not (state and (state.state=='FAILED' or state.state=='SKIPPED_DEPENDENCY'))then return value end
 end
 local role={'IDENTITY','POTENTIAL','ACTIVE'}
 -- All own-state synchronizations precede the one owner-wide network sample.
 shared.FactChanges.RegisterConsumer('RestructuringSync',function(e)
  local value=target('Restructuring');if value and value.FactChanged then value.FactChanged(e)end
 end,{kinds=role,phase=0})
 shared.FactChanges.RegisterConsumer('NetworkBridge',function(e)
  local value=target('NetworkBridge');local revision=shared.FactChanges.flushRevision
  if value and networkDrains[e.player]~=revision then networkDrains[e.player]=revision;value.Refresh(e.player)end
 end,{kinds=role,phase=0})
 local declarations={
  {target='Standardization',method='Refresh',cityOnly=true,kinds={'IDENTITY'}},
  {target='ResearchSupport',method='Audit',kinds={'IDENTITY','POTENTIAL','ACTIVE','D'}},
  {target='Lv2Housing',method='Audit',kinds={'IDENTITY','POTENTIAL','ACTIVE','D'}},
  {target='Lv2GPP',method='Audit',kinds={'IDENTITY','POTENTIAL','ACTIVE','D','WORKERS'}},
  {target='IndustrySupport',method='Audit',cityOnly=true,allowOwnerCause='REQUEST_FACTS_DIRTY',kinds={'D'}},
  {target='Lv3Support',method='Audit',kinds=role},
  {target='Lv3Effects',method='Audit',kinds={'IDENTITY','POTENTIAL','ACTIVE','D','WORKERS','NETWORK'}},
  {target='Lv4Percent',method='Audit',kinds={'IDENTITY','POTENTIAL','ACTIVE','D','WORKERS'}},
  {target='ResearchInfrastructure',method='Audit',kinds={'IDENTITY','POTENTIAL','ACTIVE','D','WORKERS'}},
  {target='ResearchCross',method='Audit',kinds={'IDENTITY','POTENTIAL','ACTIVE','D'}},
  {target='ResearchApply',method='Audit',kinds={'IDENTITY','POTENTIAL','ACTIVE','D','WORKERS'}},
  {target='ResearchChair',method='Audit',kinds={'IDENTITY','POTENTIAL','ACTIVE','D','WORKERS'}},
  {target='CultureAesthetic',method='Audit',kinds={'IDENTITY','POTENTIAL','ACTIVE','D'}},
  {target='CultureMeaning',method='Audit',kinds={'IDENTITY','POTENTIAL','ACTIVE','D'}},
  {target='CultureMeaningProbe',method='Audit',kinds={'ACTIVE','D'}},
  {target='CultureInspiration',method='Audit',kinds={'IDENTITY','POTENTIAL','ACTIVE','D'}},
  {target='CultureInsightsTourism',method='Audit',kinds={'IDENTITY','POTENTIAL','ACTIVE','HISTORY'},topics={'INSIGHTS'}},
  {target='DialogueEffects',method='Audit',kinds={'IDENTITY','POTENTIAL','ACTIVE','HISTORY'},topics={'DIALOGUE'}},
  {target='ResearchTraditionEffects',method='Mark',kinds={'IDENTITY','POTENTIAL','ACTIVE','HISTORY'},topics={'TRADITION'}},
  {target='StandardizationEffects',method='Audit',source=true,request=true,kinds={'IDENTITY','POTENTIAL','ACTIVE','NETWORK','HISTORY'},topics={'TEMPLATES','ENGINEERING'}},
  {target='CultureNetwork',method='Audit',source=true,request=true,kinds={'IDENTITY','POTENTIAL','ACTIVE','NETWORK','HISTORY'},topics={'INSIGHTS'}},
  {target='EngineeringStudy',method='CreditChanged',kinds={'HISTORY'},topics={'WONDER_CREDIT'}},
  {target='DialogueProjects',method='RefreshAccess',cityOnly=true,kinds=role},
  {target='Commerce',method='Mark',kinds={'ACTIVE','NETWORK'}},
  {target='CapitalInvestment',method='Mark',kinds={'IDENTITY','POTENTIAL','ACTIVE','NETWORK'}},
  {target='DevelopmentInvestment',method='Audit',kinds={'NETWORK'}},
 }
 local function collect(row,e)
  local owners=pending[row.target] or {};pending[row.target]=owners
  local key=tostring(e.player);local q=owners[key]
  if not q then q={player=e.player,cities={},order={},proofs={},references={},topics={},causes={}};owners[key]=q end
  if e.city==nil then q.all=true;q.proofs={}
  elseif not q.cities[e.city]then
   assert(#q.order<2048,'FACT_BINDING_SCOPE_LIMIT');q.cities[e.city]=true;q.order[#q.order+1]=e.city;q.references[e.city]=e.reference
  elseif q.references[e.city]~=e.reference then q.proofs[e.city]=nil;q.conflicting=true end
  if not q.all and not q.conflicting and e.investment then q.proofs[e.city]=e.investment end
  for name in pairs(e.topics)do q.topics[name]=true end
  for name in pairs(e.causes)do q.causes[name]=true end
 end
 for _,declaration in ipairs(declarations)do
  local row=declaration
  local remaining={};local callback=function(e)collect(row,e)end
  for _,kind in ipairs(row.kinds)do
   local provider=kind=='D' and shared.DistrictCompleteness or kind=='NETWORK' and shared.NetworkBridge
   if provider and type(provider.RegisterConsumer)=='function'then provider.RegisterConsumer('Binding_'..row.target,callback)
   else remaining[#remaining+1]=kind end
  end
  if #remaining>0 then shared.FactChanges.RegisterConsumer('Binding_'..row.target,callback,{kinds=remaining,topics=row.topics})end
 end
 local function invoke(row,q)
  local value=target(row.target);if not value or type(value[row.method])~='function'then return end
  local fn=value[row.method];local failure
  local function call(...)
   local ok,err=pcall(fn,...)
   if not ok then local safe,text=pcall(tostring,err);failure=safe and text:sub(1,180) or 'FACT_BINDING_FAILED'end
  end
  if row.cityOnly and q.all and not (row.allowOwnerCause and q.causes[row.allowOwnerCause])then
   for _,id in ipairs(q.order)do
    if row.method=='Audit'then call({player=q.player,city=id})else call(q.player,id)end
   end
   if failure then error(failure,0)end;return
  end
  if row.source then
   call({player=q.player,changed=not q.all and q.cities or nil})
   if row.request and next(q.topics)then
    local bridge=target('NetworkBridge');if bridge and bridge.RequestPendingProof then bridge.RequestPendingProof(q.player)end
   end
  elseif row.method=='Audit'then
   if q.all then call({player=q.player})
   else for _,id in ipairs(q.order)do
    local proof=not q.conflicting and not q.causes.RESTRUCTURING_COMMITTED and q.proofs[id] or nil
    call({player=q.player,city=id,investment=proof})
   end end
  elseif row.method=='CreditChanged' or row.target=='ResearchTraditionEffects' then call(q.player)
  elseif q.all then call(q.player)
  else for _,id in ipairs(q.order)do call(q.player,id)end end
  if failure then error(failure,0)end
 end
 function d.Flush()
  if d.busy then return false end;d.busy=true
  local work=pending;pending={}
  for _,row in ipairs(declarations)do
   local owners=work[row.target] or {};local global=owners['nil']
   -- A real all-player Audit already contains the known owner/city scopes.
   -- City-only methods deliberately ignore global fallback and keep their narrow work.
   if global and not row.cityOnly and (row.method=='Audit' or row.source)then owners={global=global}end
   for _,q in pairs(owners)do
    local ok,err=pcall(invoke,row,q)
    if ok then d.errors[row.target]=nil else local safe,value=pcall(tostring,err);d.errors[row.target]=safe and value:sub(1,180) or 'FACT_BINDING_FAILED'end
   end
  end
  d.busy=false;return true
 end
 return d
end
