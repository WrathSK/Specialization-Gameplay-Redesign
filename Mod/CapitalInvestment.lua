include('CapitalInvestmentModel')
include('CapitalInvestmentDiagnostics')
include('CommerceModel')
include('ExpeditionTrainingDiagnostics')
SPCCapitalInvestment={ACCESS='BUILDING_SPC_CAPITAL_ACCESS'}
function SPCCapitalInvestment.Start(P,shared)
 local M=SPCCapitalInvestmentModel;local cp=M.Copy;local same=M.Same
 local store=assert(shared.CityProgressionStore,'CAPITAL_STORE_REQUIRED')
 local d={views={},revision=0};shared.CapitalInvestment=d
 local busy=false;local dirty={};local known={};local quotes={};local sequence=0
 ExposedMembers.SPC_CapitalEpoch=(ExposedMembers.SPC_CapitalEpoch or 0)+1
 local epoch=ExposedMembers.SPC_CapitalEpoch
 local trace=SPCExpeditionTrainingDiagnostics.New(P,'CAPITAL')
 local function emit(stage,v)if trace then pcall(trace.Record,stage,v)end end
 local D=SPCCapitalInvestmentDiagnostics
 local function code(err)return D.Error(err).errorCode end
 local function failure(err,pid,id,domain,attempt)
  local info=D.Error(err,type(attempt)=='table' and attempt.phase or attempt)
  for k,v in pairs(type(attempt)=='table' and attempt.readback or {})do info[k]=v end
  local event=cp(info);event.owner=pid;event.city=id;event.contractDomain=domain;event.reason=info.errorCode
  emit('CAPITAL_FAILURE',event);return info
 end
 local function key(pid,id)return pid..':'..id end
 local function city(pid,id)local p=Players[pid];return p and p:GetCities():FindID(id)end
 local function title(c)return Locale and Locale.Lookup and Locale.Lookup(c:GetName()) or c:GetName()end
 local function money(pid)
  local p=assert(Players[pid],'CAPITAL_OWNER_CHANGED')
  local t=assert(p:GetTreasury(),'CAPITAL_TREASURY_UNAVAILABLE')
  local n=t:GetGoldBalance();assert(M.Finite(n),'CAPITAL_TREASURY_UNAVAILABLE');return n,t
 end
 local function reference(c)
  local h=store.HistoricalReference(c);local r=store.CapitalReference(h.token)
  assert(r.owner==c:GetOwner() and r.cityID==c:GetID() and r.x==c:GetX() and r.y==c:GetY()
   and r.stage=='ACTIVE','CAPITAL_REFERENCE_CHANGED');return r
 end
 local function write(pid,c,old,value,domain,attempt,phase)
  if attempt then attempt.phase=phase;attempt.readback={diagnosticStatus='NOT_OBSERVED'}end
  store.WriteCapital(pid,c,old,value,attempt and function(point,readOK,observed,expected,status,matches)
   -- Retain the Store's existing observation even if detailed projection fails.
   local out={readPoint=point,readStatus=readOK and 'READABLE' or 'READ_ERROR',writeStatus=status,
    savedMatches=readOK and matches or false,recordType=readOK and type(observed) or 'UNKNOWN',diagnosticStatus='STARTED'}
   attempt.readback=out
   local ok,err=pcall(function()
    local detail=D.Readback(point,readOK,observed,expected,domain,status,matches)
    assert(type(detail)=='table','CAPITAL_DIAGNOSTIC_RESULT_INVALID')
    for k,v in pairs(detail)do out[k]=v end
   end)
   if ok then out.diagnosticStatus='COMPLETE'
   else
    -- Keep this separate from the original Store error; it cannot authorize replay.
    out.diagnosticStatus='ERROR'
    local detail=D.Error(err)
    out.diagnosticErrorCode=detail.errorCode;out.diagnosticErrorClass=detail.errorClass
    out.diagnosticErrorFile=detail.errorFile;out.diagnosticErrorLine=detail.errorLine
   end
  end or nil)
  local after=store.CapitalState(pid,c)
  assert(same(after.value,value),'CAPITAL_WRITE_UNCONFIRMED')
 end
 local function setStage(pid,c,old,domain,stage,reason,attempt)
  local n=cp(old);n.contracts[domain].stage=stage;n.contracts[domain].reason=reason
  write(pid,c,old,n,domain,attempt,stage..'_WRITE');return n
 end
 local function validReferences(c)
  for _,r in ipairs({c.source,c.sSource})do
   local actual=store.CapitalReference(r.token)
   if actual.changes~=r.changes or actual.owner~=r.owner then return false,'CAPITAL_OWNER_CHANGED'end
   assert(actual.cityID==r.cityID and actual.x==r.x and actual.y==r.y and actual.stage=='ACTIVE','CAPITAL_REFERENCE_UNAVAILABLE')
  end
  return true
 end
 local function mutate(pid,delta,expectedBefore,c,phase)
  local before,t=money(pid);assert(before==expectedBefore,'CAPITAL_TREASURY_CHANGED')
  local expected=before+delta
  assert(M.Finite(expected),'CAPITAL_MONEY_UNCONFIRMED')
  local called=pcall(function()t:ChangeGoldBalance(delta)end)
  local readable,after=pcall(function()return money(pid)end)
  local accepted=called and readable and M.MoneyMatches(before,delta,after)
  local actual=readable and after-before or nil
  emit('CAPITAL_MONEY',{owner=pid,city=c.source.cityID,contractID=c.sequence,contractDomain=c.domain,
   phase=phase,balanceBefore=before,balanceAfter=readable and after or nil,
   expected=expected,requestedDelta=delta,actualDelta=actual,principal=c.principal,
   moneyError=actual and actual-delta or nil,moneyTolerance=M.MONEY_TOLERANCE,moneyAccepted=accepted,
   contractDue=c.due,readStatus=readable and 'READABLE' or 'UNKNOWN',submitStatus=called and 'RETURNED' or 'THREW',
   reason=called and 'CAPITAL_MONEY_READBACK' or 'CAPITAL_NATIVE_ERROR'})
  -- Only native money has the approved allowance. Never round terms, compensate
  -- with another call, or relax exact Property/receipt persistence checks.
  assert(accepted,'CAPITAL_MONEY_UNCONFIRMED')
  assert(validReferences(c),'CAPITAL_OWNER_CHANGED')
  return after
 end
 local function publish(pid,id,v)
  local k=key(pid,id);local old=d.views[k]
  if v then v.revision=old and old.revision or 0 end
  if same(old,v)then return end
  d.revision=d.revision+1;if v then v.revision=d.revision end;d.views[k]=cp(v)
 end
 local function marker(c,wanted)
  local row=assert(P.Info('Buildings',SPCCapitalInvestment.ACCESS),'CAPITAL_ACCESS_MISSING')
  local has=P.HasBuilding(c:GetBuildings(),row.Index);assert(type(has)=='boolean','CAPITAL_ACCESS_UNKNOWN')
  if has==wanted then return end
  if wanted then P.CreateBuilding(c:GetBuildQueue(),row.Index)else P.RemoveBuilding(c:GetBuildings(),row.Index)end
  assert(P.HasBuilding(c:GetBuildings(),row.Index)==wanted,'CAPITAL_ACCESS_UNCONFIRMED')
 end
 function d.Mark(pid,id)
  if pid==nil then for owner in pairs(Players)do if P.IsTestPlayer(owner)then d.Mark(owner)end end;return end
  if not P.IsTestPlayer(pid)then return end
  dirty[pid]=dirty[pid] or {};if id==nil then dirty[pid].all=true else dirty[pid][id]=true end
 end
 local function prepare(pid,c)
  local r=reference(c);local saved=store.CapitalState(pid,c);local value=saved.value or M.New();M.Validate(value)
  local f=shared.EffectiveFacts.Read(pid,c)
  local v={reference=r,token=r.token,identity=f.specialization,potential=f.potential,canSign=false,stage='READY',contracts={},domains={}}
  for domain,contract in pairs(value.contracts)do v.contracts[domain]=M.PublicContract(contract)end
  local hasContract=next(value.contracts)~=nil
  local enabled=f.specialization=='COMMERCE' and f.potential>=3
  v.available=enabled or hasContract
  if not v.available then return v,{} end
  local qualified=f.specialization=='COMMERCE' and f.activeStatus=='KNOWN' and type(f.active)=='number' and f.active>=3 and not f.investmentPending
  v.canSign=qualified
  if not qualified then v.reason='CAPITAL_ACTIVE_III_REQUIRED';return v,{} end
  for _,contract in pairs(value.contracts)do
   if contract.stage=='DEBIT_INTENT' or contract.stage=='DEBIT_CALLING' or contract.stage=='HELD'then
    v.canSign=false;v.stage='HELD';v.reason='CAPITAL_NATIVE_OUTCOME_UNKNOWN';return v,{}
   end
  end
  local standard,why=SPCCommerceModel.IsStandardSpeed();assert(standard,why or 'CAPITAL_STANDARD_SPEED_ONLY')
  local cv=shared.Commerce and shared.Commerce.views[key(pid,c:GetID())]
  assert(cv and cv.token==r.token and cv.stage=='READY' and (not shared.Commerce.TransactionCurrent or shared.Commerce.TransactionCurrent(pid,c:GetID())),'CAPITAL_COMMERCE_PENDING')
  local dc=shared.DistrictCompleteness.ReadFacts(pid,c,f.token)
  assert(dc.validity=='VERIFIED' and dc.availability=='READY' and dc.value,'CAPITAL_DISTRICT_UNKNOWN')
  local balance=money(pid);v.balance=balance;local currentTurn=Game.GetCurrentGameTurn();local internal={}
  local factCache={}
  for _,domain in ipairs(M.Domains)do
   local row={id=domain.id,nameKey=domain.nameKey,contract=v.contracts[domain.id]}
   local phase='NETWORK_SOURCES'
   local ok,q=pcall(function()
    local ids=shared.NetworkBridge.CurrentCapitalSources(pid,c,domain.kind);local candidates={}
    for _,sid in ipairs(ids)do
     phase='SOURCE_FACTS'
     local target=assert(city(pid,sid),'CAPITAL_SOURCE_UNKNOWN')
     local sf=factCache[sid]
     if not sf then sf=shared.EffectiveFacts.Read(pid,target);factCache[sid]=sf end
     assert(sf.specialization==domain.kind and sf.activeStatus=='KNOWN' and not sf.investmentPending,'CAPITAL_SOURCE_UNKNOWN')
     if sf.specialization==domain.kind and sf.active>=1 then
      phase='INSTITUTION_HISTORY'
      local times=store.InstitutionHistory(pid,target)
      candidates[#candidates+1]={reference=reference(target),level=sf.active,attained=times[sf.active],name=title(target)}
     end
    end
    local commercialized=false;for _,entry in ipairs(cv.domains or {})do if entry.id==domain.id and entry.effective then commercialized=true end end
    local depth=dc.value.domains[domain.id]
    phase='QUOTE'
    local q=M.Quote({domain=domain.id,source=r,sourceName=title(c),turn=currentTurn,balance=balance,
     D=depth and depth.value or 0,R=cv.reputation.effective or 0,commercialized=commercialized,
     candidates=candidates,failureCount=value.protection[tostring(pid)] or 0})
    return q
   end)
   if ok then
    row.quote=M.PublicQuote(q);row.canSign=not M.Open(row.contract) and q.principal>0
    row.reason=M.Open(row.contract) and 'CAPITAL_DOMAIN_OCCUPIED' or q.principal<=0 and 'CAPITAL_TREASURY_EMPTY' or 'CAPITAL_READY'
    internal[domain.id]={quote=q,old=cp(saved.value)}
   else
    row.canSign=false;row.reason=code(q)
    local prior=d.views[key(pid,c:GetID())];local oldReason
    for _,oldRow in ipairs(prior and prior.domains or {})do if oldRow.id==row.id then oldReason=oldRow.reason end end
    if oldReason~=row.reason then failure(q,pid,c:GetID(),domain.id,phase)end
   end
   v.domains[#v.domains+1]=row
  end
  return v,internal
 end
 function d.Refresh(pid,id)
  local c=city(pid,id);local k=key(pid,id)
  if not c then publish(pid,id,nil);quotes[k]=nil;known[k]=nil;return end
  local ok,v,internal=pcall(prepare,pid,c)
  if not ok then
   local readError=v
   local old=d.views[k];v={reference=old and old.reference,token=old and old.token,available=old and old.available or false,
    canSign=false,stage='HELD',reason=code(readError),contracts=old and cp(old.contracts) or {},domains={}};internal={}
   local detail=failure(readError,pid,id,nil,'REFRESH_READ')
   v.failure=old and old.failure or detail
  end
  if v.stage=='HELD' and not v.failure then local old=d.views[k];v.failure=old and cp(old.failure)end
  publish(pid,id,v);known[k]=v.available and {pid,id} or nil
  quotes[k]=internal
  local good,why=pcall(function()if ok then marker(c,v.available==true)end end)
  if not good then v.stage='HELD';v.reason=code(why);v.canSign=false;v.failure=failure(why,pid,id,nil,'ACCESS_UPDATE');publish(pid,id,v)end
  return cp(d.views[k])
 end
 local function changedContract(pid,c,value,domain,attempt)
  local contract=value.contracts[domain]
  local okay,reason=validReferences(contract)
  if not okay then
   value=setStage(pid,c,value,domain,'TERMINATED',reason,attempt)
   emit('CAPITAL_TERMINATED',{owner=pid,city=c:GetID(),contractID=contract.sequence,contractDomain=domain,reason=reason})
   return value
  end
  if contract.stage=='DEBIT_INTENT'then
   return setStage(pid,c,value,domain,'TERMINATED','CAPITAL_UNUSED_INTENT',attempt)
  end
  if contract.stage=='DEBIT_CALLING' or contract.stage=='CREDIT_CALLING'then
   return setStage(pid,c,value,domain,'HELD','CAPITAL_NATIVE_OUTCOME_UNKNOWN',attempt)
  end
  if contract.stage=='ACTIVE' and Game.GetCurrentGameTurn()>=contract.due then
   value=setStage(pid,c,value,domain,'CREDIT_INTENT',nil,attempt);contract=value.contracts[domain]
  end
  if contract.stage=='CREDIT_INTENT'then
   local amount=M.Payout(contract);local before=money(pid)
   local calling=cp(value);calling.contracts[domain].stage='CREDIT_CALLING'
   calling.contracts[domain].creditBefore=before;calling.contracts[domain].creditAfter=before+amount
   write(pid,c,value,calling,domain,attempt,'CREDIT_CALLING_WRITE')
   attempt.phase='NATIVE_CREDIT';attempt.readback=nil
   local after=mutate(pid,amount,before,contract,'CREDIT')
   local done=cp(calling);local final=done.contracts[domain]
   final.stage='SETTLED';final.creditActualAfter=after;final.paid=after-before
   final.settledTurn=Game.GetCurrentGameTurn()
   write(pid,c,calling,done,domain,attempt,'SETTLED_RECEIPT_WRITE')
   emit('CAPITAL_SETTLED',{owner=pid,city=c:GetID(),contractID=contract.sequence,contractDomain=domain,
    phase='SETTLED',mode=contract.mode,principal=contract.principal,requestedDelta=amount,returnAmount=final.paid,
    balanceBefore=before,balanceAfter=after,actualDelta=final.paid,requestResult=contract.won and 'SUCCESS' or 'FAILURE'})
   return done
  end
  return value
 end
 function d.Reconcile(pid)
  if busy or not P.IsTestPlayer(pid)then d.Mark(pid);return end
  busy=true
  local ok,why=pcall(store.VisitCapital,pid,function(saved,r)
   local c=city(pid,r.cityID)
   if r.owner~=pid or r.stage~='ACTIVE' or not c then return end
   known[key(pid,r.cityID)]={pid,r.cityID}
   local value=saved
   if r.identity~='COMMERCE' and next(value.protection)then
    local n=M.ResetProtection(value);local attempt={phase='PROTECTION_RESET'}
    local good,err=pcall(write,pid,c,value,n,nil,attempt,'PROTECTION_RESET_WRITE')
    if not good then failure(err,pid,c:GetID(),nil,attempt);error(err)end;value=n
   end
   -- Only existing three-slot contracts, never a city/building/world facts scan.
   for _,def in ipairs(M.Domains)do
    local domain=def.id;local contract=value.contracts[domain]
    if M.Open(contract)then
     local attempt={phase='RECONCILE_REFERENCE'}
     local good,nextValue=pcall(changedContract,pid,c,value,domain,attempt)
     if good then value=nextValue else
      local detail=failure(nextValue,pid,r.cityID,domain,attempt)
      local v=d.views[key(pid,r.cityID)];if v then v=cp(v);v.failure=detail;v.stage='HELD';v.canSign=false;publish(pid,r.cityID,v)end
      -- A callback failure may have persisted CALLING; never overwrite it with
      -- the older snapshot or credit again. Other cities continue independently.
      d.error=code(nextValue);break
     end
    end
   end
  end)
  if not ok then d.error=code(why)end
  busy=false;d.Mark(pid)
 end
 function d.Audit(scope)
  local pid=scope and scope.player
  d.Mark(pid)
 end
 local function flush()
  if busy then return end
  local todo=dirty;dirty={}
  for pid,changes in pairs(todo)do
   local ids={}
   for _,v in pairs(known)do if v[1]==pid and (changes.all or changes[v[2]])then ids[v[2]]=true end end
   for k,v in pairs(shared.Commerce and shared.Commerce.views or {})do
    if v.identity=='COMMERCE' and (changes.all or changes[tonumber(k:match(':(%d+)$'))])then ids[tonumber(k:match(':(%d+)$'))]=true end
   end
   for id in pairs(ids)do d.Refresh(pid,id)end
  end
 end
 function d.Request(pid,p)
  local attempt={phase='REQUEST_VALIDATE'};local responseView
  local packet=type(p)=='table' and p or {}
  local good,why=pcall(function()
   assert(P.IsTestPlayer(pid) and type(p)=='table' and type(p.CityID)=='number' and type(p.Token)=='string' and #p.Token<=100,'CAPITAL_REQUEST_INVALID')
   assert(not busy,'CAPITAL_BUSY')
   local c=assert(city(pid,p.CityID),'CAPITAL_CITY_UNKNOWN')
   if p.Action=='CAPITAL_OPEN' or p.Action=='CAPITAL_REFRESH'then
    local v=d.Refresh(pid,p.CityID);responseView=v
    for _,row in ipairs(v and v.domains or {})do if row.quote and (p.Domain==nil or p.Domain==row.id)then
     local q=row.quote
     emit('CAPITAL_QUOTE',{owner=pid,city=p.CityID,contractDomain=row.id,sourceCity=q.sSource and q.sSource.cityID,
      capitalD=q.D,capitalS=q.S,capitalC=q.C,capitalR=q.R,principal=q.principal,profitRate=q.r,probability=q.probability,
      balanceBefore=q.balance,expected=q.safe,returnAmount=q.expected,contractDue=q.due})
    end end;return
   end
   assert(p.Action=='CAPITAL_CONFIRM' and (p.Mode=='STABLE' or p.Mode=='VENTURE'),'CAPITAL_REQUEST_INVALID')
   attempt.phase='QUOTE_VALIDATE'
   local k=key(pid,p.CityID);local v=d.views[k]
   assert(v and v.revision==p.Revision and v.token==p.CityToken,'CAPITAL_QUOTE_STALE')
   local entry=quotes[k] and quotes[k][p.Domain]
   assert(entry and entry.quote and v.canSign,'CAPITAL_QUOTE_UNAVAILABLE')
   local locked=cp(entry);local current,internal=prepare(pid,c)
   local actual=internal[p.Domain]
   assert(actual and same(actual,locked) and current.canSign,'CAPITAL_QUOTE_STALE')
   assert(not M.Open(locked.old and locked.old.contracts[p.Domain]),'CAPITAL_DOMAIN_OCCUPIED')
   local q=locked.quote
   assert(q.principal>0,'CAPITAL_TREASURY_EMPTY')
   local roll=0
   if p.Mode=='VENTURE'then
    assert(type(Game.GetRandNum)=='function','CAPITAL_ROLL_UNAVAILABLE')
    roll=Game.GetRandNum(1000000,'SPC Capital Investment')/1000000
   end
   attempt.phase='CONTRACT_BUILD'
   local value=M.Begin(locked.old,q,p.Mode,roll,p.Token)
   local calling=cp(value);calling.contracts[p.Domain].stage='DEBIT_CALLING'
   busy=true
   local applied,err=pcall(function()
    write(pid,c,locked.old,value,p.Domain,attempt,'DEBIT_INTENT_WRITE')
    write(pid,c,value,calling,p.Domain,attempt,'DEBIT_CALLING_WRITE')
    attempt.phase='NATIVE_DEBIT';attempt.readback=nil
    local after=mutate(pid,-q.principal,q.balance,calling.contracts[p.Domain],'DEBIT')
    attempt.phase='CONTRACT_ACTIVATE'
    local active=M.Activate(calling,p.Domain,after);write(pid,c,calling,active,p.Domain,attempt,'ACTIVE_RECEIPT_WRITE')
    emit('CAPITAL_SIGNED',{owner=pid,city=p.CityID,contractID=active.sequence,contractDomain=p.Domain,
     phase='ACTIVE',mode=p.Mode,principal=q.principal,contractDue=q.due,profitRate=q.r,probability=q.probability,
     balanceBefore=q.balance,balanceAfter=after,actualDelta=after-q.balance})
   end)
   busy=false
   assert(applied,err)
   d.Mark(pid)
  end)
  local detail
  if not good then detail=failure(why,pid,packet.CityID,packet.Domain,attempt);why=detail.errorCode end
  if packet.Action=='CAPITAL_CONFIRM' and type(packet.CityID)=='number' and P.IsTestPlayer(pid)then
   local ok,v=pcall(d.Refresh,pid,packet.CityID)
   if ok then
    responseView=v
    if v and v.stage=='HELD' and detail then
     -- Keep the first useful failure through later held reads. Never clear Store protection.
     v.failure=v.failure and v.failure.readPoint and v.failure or detail
     publish(pid,packet.CityID,v)
    end
   end
  end
  local responseReason=good and 'CAPITAL_READY' or why
  if good and responseView then
   if responseView.stage=='HELD' or not responseView.canSign then
    responseReason=responseView.reason or 'CAPITAL_UNAVAILABLE'
   else
    for _,row in ipairs(responseView.domains or {})do
     if row.id==packet.Domain and not row.canSign then responseReason=row.reason end
    end
   end
  end
  d.lastRequest={token=packet.Token,owner=pid,city=packet.CityID,accepted=good,reason=responseReason,
   viewStage=responseView and responseView.stage,canSign=responseView and responseView.canSign,failure=detail}
  emit('CAPITAL_REQUEST',{owner=pid,city=packet.CityID,requestAction=packet.Action,requestAccepted=good,
   phase=attempt.phase,viewStage=responseView and responseView.stage,canSign=responseView and responseView.canSign,reason=responseReason})
  return good,good and nil or why
 end
 function d.Describe(pid,c)
  local v=d.views[key(pid,c:GetID())]
  if not v then return '资本投资：等待城市记录。'end
  local out={'资本投资｜'..title(c),'入口：城市生产列表 → 资本投资。'}
  if v.stage=='HELD'then out[#out+1]='资本投资已暂停，请在投资窗口查看原因并回传日志；刷新不会重新扣款。'end
  for _,def in ipairs(M.Domains)do
   local contract=v.contracts[def.id]
   if contract then
    local status={ACTIVE='执行中',SETTLED='已结算',TERMINATED='已终止',HELD='需核对金币回执',DEBIT_INTENT='确认中',DEBIT_CALLING='需核对扣款回执',CREDIT_INTENT='到期待结算',CREDIT_CALLING='需核对返还回执'}
    out[#out+1]=(Locale and Locale.Lookup and Locale.Lookup(def.nameKey) or def.kind)..'：'..(status[contract.stage] or contract.stage)..'；到期 T'..contract.due
   end
  end
  return table.concat(out,'\n')
 end
 local function hook(name,fn)local e=P.Field(Events,name);if e and e.Add then e.Add(fn)end end
 hook('LoadScreenClose',function()
  for pid in pairs(Players)do if P.IsTestPlayer(pid)then d.Reconcile(pid)end end
  flush()
 end)
 hook('PlayerTurnActivated',function(pid)if P.IsTestPlayer(pid)then d.Reconcile(pid);flush()end end)
 hook('GameCoreEventPublishComplete',flush)
 hook('CityTransfered',function(newOwner,newID,oldOwner)
  if type(oldOwner)=='number' and P.IsTestPlayer(oldOwner)then d.Reconcile(oldOwner)end
  if type(newOwner)=='number' and newOwner~=oldOwner and P.IsTestPlayer(newOwner)then d.Reconcile(newOwner)end
 end)
 for _,event in ipairs({'TreasuryChanged','PlayerTreasuryChanged','PlayerGoldChanged'})do hook(event,function(pid)d.Mark(pid)end)end
 store.RegisterExit('CapitalInvestment',function(c,loss)
  assert(store.IsExitTarget(c,loss),'CAPITAL_EXIT_UNCONFIRMED')
  store.RemoveOwned(c,loss,{SPCCapitalInvestment.ACCESS});d.Mark(loss.origin.owner)
 end)
 store.RegisterReturn('CapitalInvestment',function(pid,c)d.Mark(pid,c:GetID())end)
 return d
end
