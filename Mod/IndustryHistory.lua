-- B233: supported-player completions and city-local Industry-entry reconciliation.
-- Foreign completions are ignored. Current possession can supply N, never civilization E.
if not SPCExpeditionTrainingDiagnostics then include('ExpeditionTrainingDiagnostics')end
SPCIndustryHistory={KEY='SPC_INDUSTRY_WONDER_HISTORY_V1'}
function SPCIndustryHistory.Start(P,shared)
 local M=SPCIndustryHistory;local copy=SPCCityIdentityRead.Copy
 local d={ready=false,writes=0,published=0};shared.IndustryHistory=d
 local root,fault,busy;local queue,queued={},{}
 local trace=SPCExpeditionTrainingDiagnostics.New(P,'INDUSTRY_HISTORY')
 local function int(v)return type(v)=='number' and v>=0 and v<1000000000 and v%1==0 end
 local function same(a,b)
  if type(a)~=type(b)then return false end;if type(a)~='table'then return a==b end
  for k,v in pairs(a)do if not same(v,b[k])then return false end end
  for k in pairs(b)do if a[k]==nil then return false end end;return true
 end
 local function code(err)return tostring(err):match('IH_[A-Z_]+') or 'IH_READ_UNAVAILABLE'end
 local function ref(c)return {owner=c:GetOwner(),cityID=c:GetID(),x=c:GetX(),y=c:GetY()}end
 local function validate(v)
  assert(type(v)=='table' and v.version==1 and int(v.startTurn) and int(v.revision)
   and (v.coverage=='COMPLETE' or v.coverage=='UNAVAILABLE') and type(v.records)=='table'
   and type(v.reconciled)=='table','IH_HISTORY_INVALID')
  local n=0
  for id,r in pairs(v.records)do
   assert(type(id)=='string' and id:match('^BUILDING_') and type(r)=='table' and r.kind=='WONDER_COMPLETED'
    and int(r.turn) and r.turn>=v.startTurn and type(r.era)=='string'
    and (r.era=='UNKNOWN' or r.era:match('^ERA_')) and type(r.city)=='table'
    and int(r.city.owner) and int(r.city.cityID) and int(r.city.x) and int(r.city.y)
    and int(r.x) and int(r.y),'IH_RECEIPT_INVALID')
   assert(r.token==nil or (type(r.token)=='string' and r.token:match('^DEV%-B013%-P%d+%-%d+$')),'IH_TOKEN_INVALID')
   n=n+1
  end
  for token,city in pairs(v.reconciled)do
   assert(type(token)=='string' and token:match('^DEV%-B013%-P%d+%-%d+$') and type(city)=='table'
    and int(city.x) and int(city.y) and int(city.turn) and type(city.wonders)=='table','IH_RECONCILIATION_INVALID')
   n=n+1
   for id,observed in pairs(city.wonders)do
    assert(type(id)=='string' and id:match('^BUILDING_') and int(observed) and observed>=v.startTurn,'IH_RECONCILIATION_INVALID')
    n=n+1
   end
  end
  assert(v.revision==n+1,'IH_REVISION_INVALID');return v
 end
 local function log(stage,extra)
  extra=extra or {};extra.historyCoverage=root and root.coverage or 'UNAVAILABLE'
  extra.historyRevision=root and root.revision or 0;extra.reason=extra.reason or fault or 'OK'
  trace.Record(stage,extra)
 end
 local function hold(err)
  fault=code(err);d.ready=false;d.error=fault
  -- A missed completion must not become complete history again on cold load.
  -- Preserve the actual readable value, including a write that threw after saving.
  -- One bounded coverage downgrade; never replay the completion or replace corrupt data.
  local gapOK=pcall(function()
   local actual=Game:GetProperty(M.KEY)
   if actual==nil then return end -- absence already restores as unknown, not zero
   local gap=copy(validate(actual));gap.coverage='UNAVAILABLE'
   if not same(gap,actual)then
    P.SetProperty(Game,M.KEY,gap);assert(same(Game:GetProperty(M.KEY),gap),'IH_COVERAGE_WRITE_UNCONFIRMED')
   end
  end)
  d.coverageHeld=gapOK;log('INDUSTRY_HISTORY_HELD',{storeStatus=gapOK and 'COVERAGE_HELD' or 'RESTORE_PRE_EVENT_SAVE'})
 end
 local function commit(old,value)
  validate(value)
  assert(same(Game:GetProperty(M.KEY),old),'IH_STALE_WRITE')
  P.SetProperty(Game,M.KEY,value)
  assert(same(Game:GetProperty(M.KEY),value),'IH_WRITE_UNCONFIRMED')
  assert(not fault,'IH_REENTRANT_FAILURE')
  -- Publish only confirmed authority; no independently written N/E counters.
  root=copy(value);d.ready=true;d.writes=d.writes+1;d.published=d.published+1
 end
 local function ensure()
  if root or fault then return root~=nil and not fault end
  local ok,err=pcall(function()
   local saved=Game:GetProperty(M.KEY)
   if saved~=nil then root=copy(validate(saved));d.ready=true;log('INDUSTRY_HISTORY_RESTORED');return end
   local store=assert(shared.CityProgressionStore,'IH_STORE_UNAVAILABLE')
   local state=store.HistoryStartStatus()
   if state=='WAITING'then return end
   assert(state~='HELD','IH_STORE_UNAVAILABLE')
   local turn=Game.GetCurrentGameTurn();assert(int(turn),'IH_TURN_UNAVAILABLE')
   local value={version=1,startTurn=turn,coverage=state=='FRESH' and 'COMPLETE' or 'UNAVAILABLE',revision=1,records={},reconciled={}}
   commit(nil,value);log('INDUSTRY_HISTORY_INITIALIZED')
  end)
  if not ok then hold(err)end
  return d.ready
 end
 local function eraOf(row)
  local source=row.PrereqTech and P.Info('Technologies',row.PrereqTech)
  if not source and row.PrereqCivic then source=P.Info('Civics',row.PrereqCivic)end
  local era=source and source.EraType
  return type(era)=='string' and P.Info('Eras',era) and era or 'UNKNOWN'
 end
 local function receipt(q)
  local c=CityManager.GetCity(q.owner,q.cityID)
  assert(c and same(ref(c),q.city),'IH_CITY_CHANGED')
  -- WonderCompleted is the native completion evidence; no second current-building
  -- snapshot can reconstruct completion ownership or improve this event's timing.
  local token
  local ok,a=pcall(shared.CityProgressionStore.HistoricalReference,c)
  if ok and a then token=a.token end -- a later lawful local scan can supply N, never E
  return {kind='WONDER_COMPLETED',turn=q.turn,era=q.era,city=copy(q.city),x=q.x,y=q.y,token=token}
 end
 local function consume(id,q)
  local old=root.records[id]
  if old then
   -- Duplicate delivery never transfers completing credit or rewrites provenance.
   log('INDUSTRY_WONDER_DUPLICATE',{owner=q.owner,city=q.cityID,wonderType=id,readStatus='RETAINED_ORIGINAL'})
   return true
  end
  local r=receipt(q);local nextValue=copy(root)
  nextValue.records[id]=r;nextValue.revision=nextValue.revision+1
  commit(root,nextValue)
  if shared.EngineeringStudy then shared.EngineeringStudy.CreditChanged(r.city.owner)end
  log('INDUSTRY_WONDER_RECORDED',{owner=r.city.owner,city=r.city.cityID,wonderType=id,wonderEra=r.era,
   readStatus=r.token and 'BOUND' or 'CITY_CONTINUITY_UNKNOWN'})
  return true
 end
 local function completed(x,y,buildingIndex,owner,cityID)
  if not P.IsTestPlayer(owner) or fault then return end
  local ok,err=pcall(function()
   assert(ensure(),'IH_INITIALIZATION_UNAVAILABLE')
   local row=P.Info('Buildings',buildingIndex)
   assert(row,'IH_BUILDING_UNAVAILABLE')
   if not(row.IsWonder==true or row.IsWonder==1) or row.InternalOnly==true or row.InternalOnly==1 then return end
   assert(row.MaxWorldInstances==1,'IH_NON_UNIQUE_WONDER')
   assert(int(x) and int(y) and int(owner) and int(cityID),'IH_EVENT_INVALID')
   local c=assert(CityManager.GetCity(owner,cityID),'IH_CITY_UNAVAILABLE')
   local city=ref(c);assert(city.owner==owner and city.cityID==cityID,'IH_CITY_CHANGED')
   local q={x=x,y=y,owner=owner,cityID=cityID,city=city,index=row.Index,era=eraOf(row),turn=Game.GetCurrentGameTurn()}
   assert(int(q.turn),'IH_TURN_UNAVAILABLE')
   local id=row.BuildingType
   if queued[id]then return end
   queued[id]=true;queue[#queue+1]={id=id,event=q}
   if busy then return end
   busy=true
   local i=1
   while i<=#queue do
    assert(not fault,'IH_REENTRANT_FAILURE')
    local item=queue[i];consume(item.id,item.event);i=i+1
   end
   queue={};queued={};busy=false
  end)
  if not ok then busy=false;queue={};queued={};hold(err)end
 end
 -- Called only by the existing lawful Industry initialize/return path. A local
 -- scan adds presently verifiable city experience; it cannot manufacture E credit.
 local wonderCatalog;local reconciledThisSession={} -- readiness only, not duplicated N history
 function d.NeedsReconcile(c)
  if not d.ready or fault then return true end
  local a=shared.CityProgressionStore.HistoricalReference(c)
  return not reconciledThisSession[a.token]
 end
 function d.Reconcile(pid,c)
  assert(d.ready and root and not fault,'IH_HISTORY_UNAVAILABLE')
  assert(not busy,'IH_COMPLETION_IN_PROGRESS')
  assert(c and c:GetOwner()==pid and P.IsTestPlayer(pid),'IH_OWNER_CHANGED')
  local f=shared.EffectiveFacts.Read(pid,c);assert(f.specialization=='INDUSTRY','IH_INDUSTRY_REQUIRED')
  local a=shared.CityProgressionStore.HistoricalReference(c)
  assert(a.token==f.token,'IH_CITY_CHANGED')
  reconciledThisSession[a.token]=nil -- failed/re-entry scans remain retryable on existing events/load
  if not wonderCatalog then
   local list={}
   for _,row in ipairs(P.Rows('Buildings'))do
    if (row.IsWonder==true or row.IsWonder==1) and not(row.InternalOnly==true or row.InternalOnly==1)then
     assert(row.MaxWorldInstances==1,'IH_NON_UNIQUE_WONDER');list[#list+1]=row
    end
   end
   assert(#list>0,'IH_WONDER_CATALOG_UNAVAILABLE');wonderCatalog=list
  end
  local old=root.reconciled[a.token]
  if old then assert(old.x==c:GetX() and old.y==c:GetY(),'IH_CITY_CHANGED')end
  local now=Game.GetCurrentGameTurn();assert(int(now),'IH_TURN_UNAVAILABLE')
  local value=old and copy(old) or {x=c:GetX(),y=c:GetY(),turn=now,wonders={}}
  local additions=old and 0 or 1
  local native=assert(c:GetBuildings(),'IH_BUILDINGS_UNAVAILABLE')
  for _,row in ipairs(wonderCatalog)do
   local exists=P.HasBuilding(native,row.Index);assert(type(exists)=='boolean','IH_BUILDING_FACT_UNKNOWN')
   local completion=root.records[row.BuildingType]
   if exists and not value.wonders[row.BuildingType] and not(completion and completion.token==a.token)then
    value.wonders[row.BuildingType]=now;additions=additions+1
   end
  end
  if additions==0 then reconciledThisSession[a.token]=true;return false end
  local candidate=copy(root);candidate.reconciled[a.token]=value;candidate.revision=candidate.revision+additions
  local ok,err=pcall(commit,root,candidate)
  if not ok then hold(err);error(fault)end
  reconciledThisSession[a.token]=true
  log('INDUSTRY_WONDER_RECONCILED',{owner=pid,city=c:GetID(),readStatus='CURRENT_UNION_RETAINED'})
  return true
 end
 -- Ordinary study eligibility reads only civilization credit, not city display
 -- lists or copied Wonder details. One set over existing bounded receipts.
 function d.Credit(pid)
  assert(d.ready and root and not fault,'IH_HISTORY_UNAVAILABLE')
  assert(P.IsTestPlayer(pid),'IH_OWNER_CHANGED')
  local eras={};local E=0;local known=root.coverage=='COMPLETE'
  for _,r in pairs(root.records)do if r.city.owner==pid then
   if r.era=='UNKNOWN'then known=false elseif not eras[r.era]then eras[r.era]=true;E=E+1 end
  end end
  return {E=E,known=known,revision=root.revision}
 end
 function d.Read(pid,c)
  assert(d.ready and root and not fault,'IH_HISTORY_UNAVAILABLE')
  assert(c and c:GetOwner()==pid and P.IsTestPlayer(pid),'IH_OWNER_CHANGED')
  local result={N=0,E=0,eras={},wonders={},coverage=root.coverage,revision=root.revision,
   cityState='UNKNOWN',eraState=root.coverage=='COMPLETE' and 'KNOWN' or 'UNKNOWN'}
  local ok,a=pcall(shared.CityProgressionStore.HistoricalReference,c)
  if ok and a and a.founded and a.foundationTurn>=root.startTurn and root.coverage=='COMPLETE'then result.cityState='KNOWN'end
  for id,r in pairs(root.records)do
   if r.city.owner==pid then
    if r.era=='UNKNOWN'then result.eraState='UNKNOWN'else result.eras[r.era]=true end
   end
   if ok and a and r.token==a.token then result.wonders[id]=true end
  end
  local reconciled=ok and a and root.reconciled[a.token]
  if reconciled then
   assert(reconciled.x==c:GetX() and reconciled.y==c:GetY(),'IH_CITY_CHANGED')
   for id in pairs(reconciled.wonders)do result.wonders[id]=true end
   result.cityState='RECONCILED' -- accepted current-facts union; no unseen foreign history claim
  end
  for _ in pairs(result.wonders)do result.N=result.N+1 end
  for _ in pairs(result.eras)do result.E=result.E+1 end
  return result
 end
 local function label(tab,id)
  local row=P.Info(tab,id);local name=row and row.Name or id
  return Locale and Locale.Lookup and Locale.Lookup(name) or name
 end
 function d.Describe(pid,c)
  local ok,value=pcall(d.Read,pid,c)
  if not ok then
   log('INDUSTRY_HISTORY_REPORT',{owner=pid,city=c:GetID(),readStatus='HELD',reason=fault or code(value)})
   return '工业历史：暂不可用（'..tostring(fault or code(value))..'）。未推断旧历史。'
    ..(d.coverageHeld==false and '\n保存未确认；请保留日志并恢复本次完成前的存档。' or '')
  end
  log('INDUSTRY_HISTORY_REPORT',{owner=pid,city=c:GetID(),wonderCount=value.N,eraCount=value.E,
   readStatus=value.cityState,eligibilityStatus=value.eraState})
  local eras={};for id in pairs(value.eras)do eras[#eras+1]=label('Eras',id)end;table.sort(eras)
  local wonders={};for id in pairs(value.wonders)do wonders[#wonders+1]=label('Buildings',id)end;table.sort(wonders)
  return table.concat({'工业历史 / '..tostring(c:GetName()),
   '本城完成奇观 N：'..value.N..(value.cityState=='RECONCILED' and '（可靠记录＋本城现存奇观）' or value.cityState=='KNOWN' and '' or '（已确认下限；完整历史未知）'),
   '本文明完成时代 E：'..value.E..(value.eraState=='KNOWN' and '' or '（已确认下限；完整历史未知）'),
   '奇观自身时代：'..(#eras>0 and table.concat(eras,'、') or '无已记录时代'),
   '本城奇观：'..(#wonders>0 and table.concat(wonders,'、') or '无已记录奇观'),
   '覆盖：'..(value.coverage=='COMPLETE' and '从本局开局采集' or '此前历史未采集；没有按零补造'),
   shared.EngineeringStudy and shared.EngineeringStudy.Describe(pid,c) or '研习模块尚未就绪。',
   shared.IndustryWonderEffects and shared.IndustryWonderEffects.Describe(pid,c) or '巨构工程学模块尚未就绪。'},'\n')
 end
 local function hook(name,fn)
  local e=P.Field(Events,name);assert(e and e.Add,'IH_EVENT_UNAVAILABLE');e.Add(fn)
 end
 local ok,err=pcall(function()
  hook('WonderCompleted',completed)
  hook('LoadScreenClose',ensure)
  hook('GameCoreEventPublishComplete',function()if not root and not fault then ensure()end end)
 end)
 if not ok then hold(err)else ensure()end
end
