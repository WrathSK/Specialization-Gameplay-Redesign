include('CommerceModel')
include('CommerceCalculation')
include('NetworkInput')
include('ExpeditionTrainingDiagnostics')
-- B240: one current-effect owner. No timer, persisted derived output, generic
-- output-revision subscription, or second route authority.
SPCCommerce={Owned={'BUILDING_SPC_COMMERCIALIZATION_ACCESS'}}
local M=SPCCommerce
for bit=0,30 do M.Owned[#M.Owned+1]='BUILDING_SPC_COMMERCE_GOLD_'..bit end
function M.Start(P,shared)
 local store=assert(shared.CityProgressionStore,'COMMERCE_STORE_REQUIRED')
 local C=SPCCommerceCalculation;local model=SPCCommerceModel;local cp=model.Copy
 local d={views={},revision=0,ready=false,writes=0};shared.Commerce=d
 local views,dependencies,byTarget,dirty,known={},{},{},{},{}
 local definitions,legacy,sourceKinds={},{},{};local initialized=false;local busy=false;local writing=false;local permanentBound=false
 local ownNames={};for _,id in ipairs(M.Owned)do ownNames[id]=true end
 local trace=SPCExpeditionTrainingDiagnostics.New(P,'COMMERCE')
 local function key(pid,id)return pid..':'..id end
 local function city(pid,id)local p=Players[pid];return p and p:GetCities() and p:GetCities():FindID(id)end
 local function ref(c)return c:GetOwner()..':'..c:GetID()..':'..c:GetX()..':'..c:GetY()end
 local function same(a,b)
  if type(a)~=type(b)then return false end;if type(a)~='table'then return a==b end
  for k,v in pairs(a)do if not same(v,b[k])then return false end end
  for k in pairs(b)do if a[k]==nil then return false end end;return true
 end
 local function code(e)return tostring(e):match('(COMMERCE_[A-Z0-9_]+)') or tostring(e):match('(NETWORK_[A-Z0-9_]+)') or 'COMMERCE_STATE_UNKNOWN'end
 local function integer(n)return type(n)=='number' and n>=0 and n<math.huge and n%1==0 end
 local function isolated(pid)return shared.NetworkIsolation and shared.NetworkIsolation.Active(pid)==true end
 local function emit(stage,data)if trace then pcall(trace.Record,stage,data)end end
 local function publish(pid,id,v)
  local k=key(pid,id);local old=views[k]
  if v then v.revision=old and old.revision or 0 end
  if same(old,v)then return end
  d.revision=d.revision+1;if v then v.revision=d.revision end
  views[k]=cp(v);d.views[k]=cp(v)
  if shared.CapitalInvestment then shared.CapitalInvestment.Mark(pid,id)end
  if shared.DevelopmentInvestment then shared.DevelopmentInvestment.SourceChanged(pid,id)end
  if v then emit('COMMERCE',{owner=pid,city=id,phase=v.stage,reason=v.reason,workers=v.workers,
   count=v.reputation and v.reputation.age,expected=v.totalGold,baseInput=v.totalRaw,readStatus=v.stage=='HELD' and 'UNKNOWN' or 'VERIFIED'})end
  if v then for _,r in ipairs(v.domains or {})do if r.effective then
   emit('COMMERCE_DOMAIN',{owner=pid,city=id,networkKind=r.id,sourceCity=r.source,count=r.localD,
    previous=r.X,baseInput=r.raw,expected=r.gold,workers=v.workers,reason='COMMERCE_EFFECTIVE'})
  end end end
 end
 local function setDependencies(pid,id,sources)
  local k=key(pid,id)
  for source in pairs(byTarget[k] or {})do local t=dependencies[source];if t then t[k]=nil;if not next(t)then dependencies[source]=nil end end end
  byTarget[k]={}
  for sid in pairs(sources)do local s=key(pid,sid);dependencies[s]=dependencies[s] or {};dependencies[s][k]={pid,id};byTarget[k][s]=true end
 end
 local function validate()
  if definitions[1]then return end
  local nextDefinitions,nextLegacy={},{}
  for _,id in ipairs(M.Owned)do local r=assert(P.Info('Buildings',id),'COMMERCE_DEFINITION_MISSING');nextDefinitions[#nextDefinitions+1]={name=id,id=r.Index}end
  for _,kind in ipairs({'RESEARCH','CULTURE','INDUSTRY'})do
   nextLegacy[#nextLegacy+1]=assert(P.Info('Buildings','BUILDING_SPC_DEV_LV3_COM_'..kind),'COMMERCE_LEGACY_DEFINITION_MISSING').Index
  end
  for _,y in ipairs({'SCIENCE','CULTURE','PRODUCTION'})do for bit=0,15 do
   nextLegacy[#nextLegacy+1]=assert(P.Info('Buildings','BUILDING_SPC_B061_'..y..'_'..bit),'COMMERCE_LEGACY_DEFINITION_MISSING').Index
  end end
  definitions=nextDefinitions;legacy=nextLegacy
  -- Reuse implemented identity mapping; future professions are not enabled here.
  for _,domain in ipairs(C.Domains)do sourceKinds[domain.id]=P.Family(domain.id) or false end
 end
 local function present(c,id)local yes=P.HasBuilding(c:GetBuildings(),id);assert(type(yes)=='boolean','COMMERCE_CARRIER_UNKNOWN');return yes end
 local function set(c,id,want)
  if present(c,id)==want then return end
  writing=true
  local ok,err=pcall(function()
   if want then P.CreateBuilding(c:GetBuildQueue(),id)else P.RemoveBuilding(c:GetBuildings(),id)end
   assert(present(c,id)==want,'COMMERCE_WRITE_UNCONFIRMED');d.writes=d.writes+1
  end)
  writing=false;assert(ok,err)
 end
 local function observed(c,observer)
  local total=0
  for bit=0,30 do
   if observer then P.Count('observer_native_attempt');P.Count('observer_commerce_attempt')end
   if present(c,definitions[bit+2].id)then total=total+2^bit end
  end
  return total
 end
 local function applyGold(c,n)
  assert(integer(n) and n<=2147483647,'COMMERCE_ENCODING_RANGE')
  for _,adding in ipairs({false,true})do for bit=0,30 do
   local want=math.floor(n/2^bit)%2==1
   if want==adding then set(c,definitions[bit+2].id,want)end
  end end
  assert(observed(c)==n,'COMMERCE_WRITE_UNCONFIRMED')
 end
 local function clear(c)applyGold(c,0);set(c,definitions[1].id,false)end
 local function initialize()
  if initialized then return true end
  if store.HistoryStartStatus then local status=store.HistoryStartStatus();if status=='WAITING' or status=='HELD'then return false end end
  validate()
  -- Once per Gameplay context, only supported, proven current Store bindings.
  -- Confirmed owner-loss cleanup is Store's separate exact-owned exit callback.
  for pid,p in pairs(Players)do if P.IsTestPlayer(pid)then local cs=p:GetCities();if cs then for _,c in cs:Members()do
   local ok,h=pcall(store.HistoricalReference,c)
   if ok and h.owner==pid and h.cityID==c:GetID()then clear(c);known[key(pid,c:GetID())]={pid,c:GetID()}end
  end end end end
  initialized=true;d.ready=true;return true
 end
 local function facts(batch,pid,c)
  local k=key(pid,c:GetID());if not batch.facts[k]then batch.facts[k]=shared.EffectiveFacts.Read(pid,c)end
  return batch.facts[k]
 end
 local function depth(batch,pid,c,token)
  local k=key(pid,c:GetID())
  if not batch.depth[k]then
   local s=shared.DistrictCompleteness.ReadFacts(pid,c,token)
   assert(s.validity=='VERIFIED' and s.availability=='READY' and s.value,'COMMERCE_DISTRICT_FACTS_UNKNOWN')
   batch.depth[k]=s.value
  end
  return batch.depth[k]
 end
 local function title(c)
  local n=c:GetName();if Locale and Locale.Lookup then n=Locale.Lookup(n)end
  return tostring(n):gsub('[\r\n]',' ')
 end
 local function prepare(batch,pid,id)
  local c=assert(city(pid,id),'COMMERCE_CITY_UNKNOWN');assert(c:GetOwner()==pid,'COMMERCE_OWNER_CHANGED')
  local f=facts(batch,pid,c);local v={reference=ref(c),token=f.token,identity=f.specialization,potential=f.potential,
   active=f.active,activeStatus=f.activeStatus,workers=0,selected={},effective={},domains={},totalRaw=0,totalGold=0,
   stage='INELIGIBLE',reason='COMMERCE_IDENTITY_REQUIRED',canConfigure=false,reputation={age=0,effective=0}}
  local out={pid=pid,id=id,c=c,v=v,sources={[id]=true}}
  if f.specialization~='COMMERCE'then return out end
  local standard,speedReason=model.IsStandardSpeed()
  assert(standard,speedReason or 'COMMERCE_STANDARD_SPEED_ONLY')
  assert(f.owner==pid and f.cityID==id and type(f.token)=='string','COMMERCE_REFERENCE_CHANGED')
  local state=store.CommerceState(pid,c)
  assert(state.token==f.token,'COMMERCE_REFERENCE_CHANGED')
  local value=state.value or model.New(pid);model.Validate(value);assert(value.owner==pid,'COMMERCE_OWNER_CHANGED')
  v.selected=cp(value.selected);v.reputation=cp(value.reputation or {age=0,state='NOT_ESTABLISHED'});v.reputation.effective=0
  assert(f.activeStatus=='KNOWN' and integer(f.active) and not f.investmentPending,'COMMERCE_QUALIFICATION_UNKNOWN')
  if f.potential==4 then assert(value.reputation,'COMMERCE_REPUTATION_UNKNOWN')end
  if f.active==4 then
   assert(v.reputation.state=='COUNTING','COMMERCE_REPUTATION_UNKNOWN')
   v.reputation.effective=v.reputation.age
  end
  local dc=depth(batch,pid,c,f.token);local localDomains={}
  for domain,r in pairs(dc.domains)do localDomains[domain]=r.value end
  local anchor
  for _,r in ipairs(dc.districts)do if f.first and r.id==f.first.districtID and r.type==f.first.type then anchor=r;break end end
  assert(anchor and anchor.complete==true,'COMMERCE_ANCHOR_UNKNOWN')
  if anchor.pillaged~=true then
   local plot=assert(Map.GetPlotByIndex(anchor.plot),'COMMERCE_WORKERS_UNKNOWN')
   local n=plot:GetWorkerCount();assert(integer(n),'COMMERCE_WORKERS_UNKNOWN');v.workers=n
  end
  v.canConfigure=f.active>=3;v.domains=C.Layout(v.selected,v.workers,f.active,localDomains)
  if f.active<3 then v.reason='COMMERCE_ACTIVE_III_REQUIRED';return out end
  if shared.CommerceConvergence and shared.CommerceConvergence.Withdraw then shared.CommerceConvergence.Withdraw(c)end
  for _,index in ipairs(legacy)do assert(not present(c,index),'COMMERCE_LEGACY_REMAINS')end
  local network=shared.NetworkBridge.CurrentDomesticPartners(pid,c)
  assert(network.validity=='VERIFIED',network.reason or 'COMMERCE_NETWORK_UNKNOWN')
  out.network=network
  for _,sid in ipairs(network.partners)do out.sources[sid]=true end
  v.stage='READY';v.reason='COMMERCE_READY'
  for _,r in ipairs(v.domains)do if r.effective then v.effective[#v.effective+1]=r.id end end
  out.rows=v.domains;return out
 end
 local function sourceYield(batch,pid,c,y)
  local k=key(pid,c:GetID())..':'..y
  if batch.yields[k]~=nil then return batch.yields[k]end
  local index=assert(P.Info('Yields','YIELD_'..y),'COMMERCE_YIELD_DEFINITION_MISSING').Index
  local n=c:GetYield(index);assert(type(n)=='number' and n==n and n>=0 and n<math.huge,'COMMERCE_SOURCE_UNKNOWN')
  batch.yields[k]=n;return n
 end
 -- Only the Store's base identity is needed: no Governor, investment ledger,
 -- remote building scan or persistent/cache copy of derived source eligibility.
 local function sourceIdentity(batch,pid,c)
  local k=key(pid,c:GetID())
  if batch.identities[k]~=nil then return batch.identities[k]end
  local ok,kind=pcall(function()
   local owns=store.Owns(c);assert(type(owns)=='boolean','COMMERCE_SOURCE_IDENTITY_UNKNOWN')
   if not owns then return 'NONE' end
   local f=store.Base(pid,c)
   assert(f.owner==pid and f.cityID==c:GetID() and type(f.token)=='string'
    and type(f.specialization)=='string','COMMERCE_SOURCE_IDENTITY_UNKNOWN')
   return f.specialization
  end)
  assert(ok,'COMMERCE_SOURCE_IDENTITY_UNKNOWN')
  batch.identities[k]=kind;return kind
 end
 local function resolve(batch,x)
  if not x.rows then return end
  local values={}
  for _,r in ipairs(x.rows)do if r.effective then
   local best
   for sid in pairs(x.sources)do
    local c=assert(city(x.pid,sid),'COMMERCE_SOURCE_UNKNOWN');assert(c:GetOwner()==x.pid,'COMMERCE_SOURCE_OWNER_CHANGED')
    if sid~=x.id then assert(SPCNetworkInput.Reference(c)==x.network.references[sid],'COMMERCE_SOURCE_REFERENCE_CHANGED')end
    if sid==x.id or sourceKinds[r.id] and sourceIdentity(batch,x.pid,c)==sourceKinds[r.id]then
     local n=sourceYield(batch,x.pid,c,r.yield)
     if not best or n>best.X or n==best.X and sid<best.city then best={city=sid,owner=x.pid,name=title(c),X=n}end
    end
   end
   values[r.id]=assert(best,'COMMERCE_SOURCE_UNKNOWN')
  end end
  local result=C.Finish(x.rows,values,x.v.reputation.effective)
  x.v.domains=result.domains;x.v.totalRaw=result.totalRaw;x.v.totalGold=result.totalGold
 end
 local function addTargets(ids,pid,cid)
  if cid~=nil then ids[key(pid,cid)]={pid,cid};for k,v in pairs(dependencies[key(pid,cid)] or {})do ids[k]=v end
  else for k,v in pairs(known)do if v[1]==pid then ids[k]=v end end end
 end
 function d.Mark(pid,id)
  if pid==nil then for owner in pairs(Players)do if P.IsTestPlayer(owner)then d.Mark(owner,id)end end;return end
  if not P.IsTestPlayer(pid) or isolated(pid)then return end
  dirty[pid]=dirty[pid] or {cities={}}
  if id==nil then dirty[pid].all=true else dirty[pid].cities[id]=true end
 end
 function d.Audit(scope)
  if scope and scope.player~=nil and (not P.IsTestPlayer(scope.player) or isolated(scope.player))then return end
  if busy then d.Mark(scope and scope.player,scope and scope.city);return end
  busy=true;d.busy=true;d.error=nil
  local ok,why=pcall(function()
   if not initialize()then return end
   local ids={}
   for pid in pairs(Players)do if P.IsTestPlayer(pid) and not isolated(pid) and (not scope or scope.player==nil or scope.player==pid)then
    local changed=scope and (scope.changed or scope.city~=nil and {[scope.city]=true})
    if changed then for cid in pairs(changed)do addTargets(ids,pid,cid)end else addTargets(ids,pid)end
   end end
   local batch={facts={},depth={},yields={},identities={}};local plans={}
   for k,pair in pairs(ids)do
    local pid,id=pair[1],pair[2];local c=city(pid,id)
    if c and c:GetOwner()==pid then
     local good,x=pcall(prepare,batch,pid,id)
     if not good then
      local f=batch.facts[k];local old=views[k]
      x={pid=pid,id=id,c=c,v={reference=ref(c),token=f and f.token or old and old.token,
       identity=f and f.specialization or old and old.identity,potential=f and f.potential,active=f and f.active,
       activeStatus=f and f.activeStatus,selected=old and cp(old.selected) or {},effective={},domains=old and cp(old.domains) or {},
       workers=0,reputation=old and cp(old.reputation) or {age=0,effective=0},totalRaw=0,totalGold=0,
       stage='HELD',reason=code(x),canConfigure=false}}
      for _,r in ipairs(x.v.domains)do r.effective=false;r.suspended=r.selected;r.reason=x.v.reason;r.raw=0;r.gold=0;r.floor=0 end
     else setDependencies(pid,id,x.v.identity=='COMMERCE' and x.sources or {})end
     plans[k]=x;known[k]=(x.v.identity=='COMMERCE' or x.v.stage=='HELD') and {pid,id} or nil
    else publish(pid,id,nil);setDependencies(pid,id,{});known[k]=nil end
   end
   for _,x in pairs(plans)do
    local good,err=pcall(resolve,batch,x)
    if not good then x.v.stage='HELD';x.v.reason=code(err);x.v.totalGold=0;x.v.totalRaw=0;x.v.canConfigure=false
     x.v.effective={};for _,r in ipairs(x.v.domains)do r.effective=false;r.suspended=r.selected;r.reason=x.v.reason;r.raw=0;r.gold=0;r.floor=0 end
    end
   end
   -- D0055 inputs exclude Gold. Apply only differences; unchanged reads never
   -- dismantle effects or write to a remote source merely to sample its yield.
   for k,x in pairs(plans)do
    local binding=false
    local good,err=pcall(function()
     local h=store.HistoricalReference(x.c)
     assert(h.owner==x.pid and h.cityID==x.id and h.token==x.v.token,'COMMERCE_BINDING_UNAVAILABLE')
     binding=true
     assert(ref(x.c)==x.v.reference,'COMMERCE_REFERENCE_CHANGED')
     applyGold(x.c,x.v.totalGold);set(x.c,definitions[1].id,x.v.stage=='READY' and x.v.canConfigure)
    end)
    if not good then
     if binding then pcall(clear,x.c)end
     local read,remaining=pcall(observed,x.c)
     x.v.cleanupConfirmed=read and remaining==0;x.v.remainingCarrierGold=read and remaining or nil
     x.v.stage='HELD';x.v.reason=code(err);x.v.totalGold=0;x.v.totalRaw=0;x.v.canConfigure=false;x.v.effective={}
     for _,r in ipairs(x.v.domains)do r.effective=false;r.suspended=r.selected;r.reason=x.v.reason;r.raw=0;r.gold=0;r.floor=0 end
    end
    publish(x.pid,x.id,x.v)
   end

  end)
  if not ok then d.error=code(why)end
  busy=false;d.busy=false
 end
 function d.Refresh(pid,id)d.Audit({player=pid,city=id});return cp(views[key(pid,id)])end
 function d.SourceChanged(pid,id)d.Audit({player=pid,changed={[id]=true}})end
 function d.BindPermanentWrites()
  if permanentBound then return end
  local prior=shared.OnPermanentCityWrite
  shared.OnPermanentCityWrite=function(c,reason)
   if prior then prior(c,reason)end
   if c then d.Mark(c:GetOwner(),c:GetID())end
  end
  permanentBound=true
 end
 function d.ExperimentalNetworkWithdraw(pid)
  assert(isolated(pid) and P.IsTestPlayer(pid) and not busy,'COMMERCE_ISOLATION_REQUIRED')
  validate()
  local cs=assert(Players[pid]:GetCities(),'COMMERCE_CITY_COLLECTION_UNKNOWN')
  for _,c in cs:Members()do
   local ok,h=pcall(store.HistoricalReference,c)
   if ok and h.owner==pid and h.cityID==c:GetID()then
    clear(c)
    local v=cp(views[key(pid,c:GetID())])
    if v then
     v.stage='HELD';v.reason='COMMERCE_EXPERIMENT_ISOLATED';v.totalGold=0;v.totalRaw=0;v.canConfigure=false;v.effective={}
     for _,r in ipairs(v.domains or {})do r.effective=false;r.suspended=r.selected;r.gold=0;r.floor=0;r.raw=0 end
     publish(pid,c:GetID(),v)
    end
   end
  end
  dirty[pid]=nil;return true
 end
 function d.Request(pid,p)
  local accepted=false;local why
  local ok,err=pcall(function()
   assert(P.IsTestPlayer(pid) and type(p)=='table' and integer(p.CityID),'COMMERCE_REQUEST_INVALID')
   local c=assert(city(pid,p.CityID),'COMMERCE_CITY_UNKNOWN');assert(c:GetOwner()==pid,'COMMERCE_OWNER_CHANGED')
   if p.Action=='COMMERCE_READ'then accepted=true;return end -- report consumes published state only
   assert(p.Action=='COMMERCE_SELECT','COMMERCE_REQUEST_INVALID')
   local old=views[key(pid,p.CityID)]
   assert(old and old.revision==p.Revision and old.reference==p.Reference and old.token==p.CityToken,'COMMERCE_VIEW_STALE')
   d.Refresh(pid,p.CityID);local current=views[key(pid,p.CityID)]
   assert(current and current.revision==old.revision and current.reference==ref(c) and current.canConfigure,'COMMERCE_VIEW_STALE')
   assert(type(p.Enabled)=='boolean' or p.Enabled==0 or p.Enabled==1,'COMMERCE_REQUEST_INVALID')
   local enabled=p.Enabled==true or p.Enabled==1;local found
   for _,r in ipairs(current.domains)do if r.id==p.Domain then found=r;break end end
   assert(found and (not enabled or found.eligible),'COMMERCE_LOCAL_DISTRICT_REQUIRED')
   local s=store.CommerceState(pid,c);assert(s.token==current.token,'COMMERCE_REFERENCE_CHANGED')
   local nextValue=model.Select(s.value or model.New(pid),p.Domain,enabled)
   store.WriteCommerce(pid,c,s.value,nextValue)
   local actual=store.CommerceState(pid,c);assert(same(actual.value,nextValue) and actual.token==s.token,'COMMERCE_WRITE_UNCONFIRMED')
   d.SourceChanged(pid,p.CityID);accepted=true
  end)
  if not ok then why=code(err);if p and p.Action~='COMMERCE_READ' and integer(p.CityID)then pcall(d.Refresh,pid,p.CityID)end end
  d.lastRequest={token=p and p.Token,owner=pid,city=p and p.CityID,accepted=accepted,reason=why or 'COMMERCE_READY'}
  emit('COMMERCE_REQUEST',{owner=pid,city=p and p.CityID,requestAction=p and p.Action,requestAccepted=accepted,reason=d.lastRequest.reason})
  return accepted,why
 end
 function d.Describe(pid,c)
  local v=views[key(pid,c:GetID())]
  if not v then return '商业化：等待城市记录。'end
  local rows={'商业化｜'..title(c)..'｜'..(v.stage=='READY' and '已就绪' or v.reason),
   '工作专家 '..v.workers..'｜生效领域 '..#(v.effective or {})..'｜合计 +'..v.totalGold..' 基础金币/回合',
   '商业信誉 '..tostring(v.reputation and v.reputation.age or 0)..'；当前使用 '..tostring(v.reputation and v.reputation.effective or 0)}
  for _,r in ipairs(v.domains or {})do
   local n=Locale and Locale.Lookup and Locale.Lookup(r.nameKey) or r.id
   local reasons={COMMERCE_LOCAL_DISTRICT_REQUIRED='本城缺少对应区域',COMMERCE_NOT_SELECTED='未开启',
    COMMERCE_ACTIVE_III_REQUIRED='当前ACTIVE不足三级',COMMERCE_CAPACITY='专家名额不足，选择保留',
    COMMERCE_SOURCE_IDENTITY_UNKNOWN='来源专业身份暂不可确认'}
   rows[#rows+1]=n..(r.yield=='FOOD' and '（总粮食，非余粮）' or '')..'：'..(r.effective and string.format('D%d × X%.3f × 5%% × %.3f = %.3f → +%d',r.localD,r.X,1+.005*v.reputation.effective,r.raw,r.gold) or (reasons[r.reason] or '暂不可用：'..tostring(r.reason)))
   if r.effective then rows[#rows+1]='来源：'..r.sourceName end
  end
  if v.cleanupConfirmed==false then rows[#rows+1]='收益清理尚未确认；残留载体配置：'..tostring(v.remainingCarrierGold or '未知')end
  rows[#rows+1]='来源：本城，或直接国内商路连接的对应专业城市。'
  rows[#rows+1]='配置入口：城市生产列表 → 商业化 / 商业信誉；P0这里只读。'
  rows[#rows+1]='各领域分别向下取整后相加；城市既有金币倍率可能进一步调整实际收益。'
  return table.concat(rows,'\n')
 end
 -- B267 observes existing publications/carriers only; never reconciles effects.
 local turnTrace=SPCExpeditionTrainingDiagnostics.New(P,'COMMERCE_TURN')
 local turnStates={}
 local function diagnosticRead(object,method)
  local ok,v=pcall(function()local fn=object and object[method];if type(fn)~='function'then return 'UNAVAILABLE'end;P.Count('observer_native_attempt');P.Count('observer_commerce_attempt');return fn(object)end)
  if not ok then return 'READ_ERROR'end
  if type(v)=='number' or type(v)=='boolean' or v=='UNAVAILABLE'then return v end;return 'UNKNOWN'
 end
 local function turnSample(stage,pid)
  if not SPCExpeditionTrainingDiagnostics.ENABLED then return end
  if not P.IsTestPlayer(pid)then return end
  local player=Players[pid];local treasuryOK,treasury=pcall(function()P.Count('observer_native_attempt');P.Count('observer_commerce_attempt');return player:GetTreasury()end)
  if not treasuryOK then treasury=nil end
  local expected,actual,held,unknown=0,0,0,0;local firstReason
  for _,c in player:GetCities():Members()do
   P.Count('observer_city_scan')
   local id=c:GetID();local v=views[key(pid,id)];local good,n=pcall(observed,c,true)
   local want=v and v.totalGold or 0
   expected=expected+want;if good then actual=actual+n else unknown=unknown+1 end
   if v and v.stage=='HELD'then held=held+1;firstReason=firstReason or v.reason end
   local signature=table.concat({v and v.stage or 'NONE',v and v.reason or 'NONE',tostring(want),good and tostring(n) or 'UNKNOWN'},':')
   local k=ref(c)
   if turnStates[k]~=signature or not good or n~=want then
    turnTrace.Record('COMMERCE_TURN_CITY',{owner=pid,city=id,expected=want,carrierGold=good and n or 'UNKNOWN',
     phase=v and v.stage or 'NONE',reason=v and v.reason or 'NONE',readStatus=good and 'VERIFIED' or 'UNKNOWN'})
   end
   turnStates[k]=signature
  end
  local bridge=shared.NetworkBridge;local b=bridge and bridge.players and bridge.players[pid]
  local sender=ExposedMembers.SPC_P0_BackgroundRoutes or {}
  turnTrace.Record(stage,{owner=pid,goldBalance=diagnosticRead(treasury,'GetGoldBalance'),
   goldYield=diagnosticRead(treasury,'GetGoldYield'),maintenance=diagnosticRead(treasury,'GetTotalMaintenance'),
   ownerTurnActive=diagnosticRead(player,'IsTurnActive'),ready=d.ready,coreBusy=busy,commerceWrites=d.writes,
   expected=expected,carrierGold=unknown==0 and actual or 'UNKNOWN',heldCount=held,reason=firstReason or 'NONE',
   unreadableCount=unknown,networkRevalidation=b and b.revalidation,networkAvailability=b and b.availability,
   networkSignal=b and b.signal,routeSignal=shared.RouteSignalRevision or 0,
   senderResult=sender.senderResult or 'UNAVAILABLE',senderFailedTurn=sender.senderFailedTurn,
   senderTurn=sender.senderTurn,senderTurnActive=sender.senderTurnActive})
 end
 local function diagnosticTurn(stage,pid)
  local ok=pcall(turnSample,stage,pid)
  if not ok then pcall(turnTrace.Record,'COMMERCE_TURN_FAILURE',{owner=pid,reason='TURN_READ_ERROR'})end
 end
 local function flush()
  if busy then return end;local todo=dirty;dirty={}
  for pid,v in pairs(todo)do d.Audit({player=pid,changed=not v.all and v.cities or nil})end
 end
 local function hook(source,event,fn)local e=P.Field(source,event);if e and e.Add then e.Add(fn)end end
 hook(Events,'LoadScreenClose',function()d.Audit()end)
 hook(Events,'PlayerTurnDeactivated',function(pid)diagnosticTurn('COMMERCE_TURN_END',pid)end)
 hook(GameEvents,'PlayerTurnStarted',function(pid)diagnosticTurn('COMMERCE_TURN_STARTED',pid)end)
 hook(Events,'GameCoreEventPublishComplete',flush)
 hook(Events,'PlayerTurnActivated',function(pid)d.Mark(pid)end)
 for _,event in ipairs({'CityWorkerChanged','CityPopulationChanged','CityFocusChanged','CityBuildingsChanged','CityYieldChanged','CityYieldsChanged'})do
  hook(Events,event,function(pid,id)if not writing then d.Mark(pid,type(id)=='number' and id or nil)end end)
 end
 for _,event in ipairs({'GovernorAssigned','GovernorEstablished','GovernorChanged','GovernorPromoted','GovernmentPolicyChanged','GovernmentChanged','ResearchCompleted','CivicCompleted'})do
  hook(Events,event,function(pid)if not writing then d.Mark(type(pid)=='number' and pid or nil)end end)
 end
 for _,event in ipairs({'CityTransfered','CityRemovedFromMap','DistrictAddedToMap','DistrictRemovedFromMap','DistrictPillaged','DistrictRepaired','BuildingPillaged','BuildingRepaired','CityTileOwnershipChanged'})do
  hook(Events,event,function()if not writing then d.Mark()end end)
 end
 for _,event in ipairs({'BuildingAddedToMap','BuildingRemovedFromMap'})do
  hook(Events,event,function(x,y,index,owner)
   local row=P.Info('Buildings',index)
   if writing or row and ownNames[row.BuildingType]then return end
   local ok,c=pcall(function()return CityManager and CityManager.GetCityAt(x,y)end)
   if ok and c then d.Mark(c:GetOwner(),c:GetID());return end
   d.Mark(type(owner)=='number' and owner or nil)
  end)
 end
 for _,event in ipairs({'CityBuilt','OnBuildingConstructed','OnDistrictConstructed'})do
  -- Construction events are not uniformly (owner,cityID). In particular
  -- OnDistrictConstructed is (owner,districtType,x,y); do not route its type as a city.
  hook(GameEvents,event,function(pid)if not writing then d.Mark(type(pid)=='number' and pid or nil)end end)
 end
 store.RegisterExit('Commerce',function(c,loss)
  assert(store.IsExitTarget(c,loss),'COMMERCE_EXIT_UNCONFIRMED');store.RemoveOwned(c,loss,M.Owned)
  for k,pair in pairs(known)do if pair[1]==loss.origin.owner then
   local v=views[k]
   if v and v.reference==loss.origin.owner..':'..pair[2]..':'..c:GetX()..':'..c:GetY()then publish(pair[1],pair[2],nil);setDependencies(pair[1],pair[2],{});known[k]=nil end
  end end
  d.Mark(loss.origin.owner)
 end)
 store.RegisterReturn('Commerce',function(pid,c)d.Mark(pid,c:GetID())end)
 return d
end
