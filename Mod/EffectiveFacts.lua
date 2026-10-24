-- B032: native read-only investment overlay. No Property writes or unit actions.
SPCEffectiveFacts={}
function SPCEffectiveFacts.Start(P,shared)
 local KEY='SPC_DEV_INVESTMENT_LEDGER_V1'
 local kinds={RESEARCH=true,CULTURE=true,INDUSTRY=true,COMMERCE=true}
 local function clone(v) if type(v)~='table' then return v end;local r={};for k,x in pairs(v) do r[k]=clone(x) end;return r end
 local function same(a,b)
  if type(a)~=type(b) then return false end;if type(a)~='table' then return a==b end
  for k,v in pairs(a) do if not same(v,b[k]) then return false end end
  for k in pairs(b) do if a[k]==nil then return false end end;return true
 end
 local data={};shared.EffectiveFacts=data
 -- One synchronous declared read window, never a turn/global native-object cache.
 local phase;local generation=0;local writes=0;local tickets={}
 local function pack(...)return {n=select('#',...),...}end
 local function finish(result)
  if not result[1]then error(result[2],0)end
  return unpack(result,2,result.n)
 end
 function data.Version()return generation end
 function data.Invalidate()
  generation=generation+1;if phase then phase.values={};phase.count=0 end
 end
 function data.BeginWrite()
  data.Invalidate();writes=writes+1;local ticket={};tickets[ticket]=true;return ticket
 end
 function data.EndWrite(ticket)
  assert(tickets[ticket],'FACT_WRITE_TICKET_INVALID');tickets[ticket]=nil;writes=writes-1;data.Invalidate()
 end
 function data.WithPhase(label,fn,...)
  assert(type(fn)=='function','FACT_PHASE_CALLBACK_INVALID')
  if phase then return fn(...)end
  phase={values={},count=0,label=label};local result=pack(pcall(fn,...));phase=nil
  return finish(result)
 end
 local function stamp(pid,city)
  local store=shared.CityProgressionStore
  -- The isolated legacy Flow authority has different recovery guards; do not cache it.
  if not (store and store.FactStamp)then return nil end
  local value=store.FactStamp(pid,city);if value==nil then return nil end
  return table.concat({city:GetOwner(),city:GetID(),city:GetX(),city:GetY(),Game.GetCurrentGameTurn(),value},':')
 end
 local function gate(city)return {P.GovernorGate(city)}end
 local function capture(pid,city) P.Count('facts');
  assert(P.IsTestPlayer(pid) and city:GetOwner()==pid,'EFFECTIVE_OWNER_CHANGED')
  local f=shared.CityFlowProbe.SupportFacts(pid,city)
  assert(f.owner==pid and f.cityID==city:GetID() and type(f.token)=='string','EFFECTIVE_FOUNDATION_IDENTITY')
  local store=shared.CityProgressionStore
  local ledger
  if store and store.Owns(city) then ledger=store.Investment(pid,city) else ledger=city:GetProperty(KEY) end
  local n=0
  if f.specialization=='NONE' then
   assert(ledger==nil and (f.potential==0 or f.restructuring and (f.progression=='REALLOCATING' or f.progression=='CONSUMING') and f.potential>=1 and f.potential<=3),'UNASSIGNED_INVESTMENT_CONFLICT')
  else
   assert(kinds[f.specialization] and (f.potential==1 or f.restructuring and f.potential>=1 and f.potential<=3) and type(f.first)=='table','EFFECTIVE_FOUNDATION_INVALID')
   if ledger~=nil then
    -- Comparison only: borrow first here; the returned facts below still deep-copy it.
    local anchor={owner=pid,cityID=f.cityID,token=f.token,first=f.first,specialization=f.specialization}
    assert(type(ledger)=='table' and ledger.schema==1 and same(ledger.anchor,anchor),'INVESTMENT_ANCHOR_CHANGED')
    assert(type(ledger.investments)=='table','INVESTMENT_LEDGER_INVALID')
    local units={}
    for receipt,unit in pairs(ledger.investments) do
     assert(type(receipt)=='string' and #receipt>0 and type(unit)=='string' and #unit>0 and not units[unit],'INVESTMENT_RECEIPT_INVALID')
     units[unit]=true;n=n+1;assert(n+f.potential<=4,'INVESTMENT_CAP_EXCEEDED')
    end
    assert(ledger.revision==1+n,'INVESTMENT_REVISION_INVALID')
    if ledger.pending~=nil then
     local op=ledger.pending
     assert(type(op)=='table' and (op.stage=='INTENT' or op.stage=='CONSUMED_CONFIRMED')
      and type(op.unitID)=='number' and op.unitID>=0 and op.unitID%1==0
      and op.owner==pid and op.cityUID==f.token and op.expectedRevision==ledger.revision
      and type(op.receipt)=='string' and #op.receipt>0 and type(op.unitUID)=='string' and #op.unitUID>0
      and not ledger.investments[op.receipt] and not units[op.unitUID] and n+f.potential<4,'INVESTMENT_PENDING_INVALID')
    end
   end
  end
  local out=clone(f);out.basePotential=f.potential;out.potential=f.potential+n
  out.investmentCount=n;out.investmentPending=ledger and ledger.pending~=nil or false
  out.ledgerStatus=ledger and 'PRESENT' or 'ABSENT_NO_WRITES'
  out.active=out.potential;out.activeStatus='KNOWN'
  if f.specialization=='NONE' then out.active=0
  elseif out.potential>1 then
   local gateOwner,gateCityID,gateStatus,ceiling=P.GovernorGate(city)
   if gateOwner==pid and gateCityID==f.cityID and gateStatus=='KNOWN'
    and type(ceiling)=='number' and ceiling%1==0 and ceiling>=1 and ceiling<=4 then
    out.active=math.min(out.potential,ceiling)
   else out.active=nil;out.activeStatus='UNKNOWN_GOVERNOR' end
  end
  return out
 end
 local function phasedRead(pid,city)
  if not phase or writes>0 then return capture(pid,city)end
  assert(P.IsTestPlayer(pid) and city:GetOwner()==pid,'EFFECTIVE_OWNER_CHANGED')
  local before=generation;local identity=stamp(pid,city)
  if not identity then return capture(pid,city)end
  local key=tostring(pid)..':'..tostring(city:GetID());local cached=phase.values[key]
  if cached and cached.identity==identity then
   local current=cached.gate and gate(city) or nil
   if (not cached.gate or same(current,cached.gate)) and stamp(pid,city)==identity and generation==before and writes==0 then
    P.Count('facts_reuse');return clone(cached.value)
   end
  end
  if cached then phase.values[key]=nil;phase.count=phase.count-1 end
  local value=capture(pid,city)
  -- A getter may reenter native code. Never publish old confirmed facts across a write/reference boundary.
  assert(stamp(pid,city)==identity and generation==before and writes==0,'EFFECTIVE_FACTS_CHANGED_DURING_READ')
  if value.activeStatus=='KNOWN' and not value.investmentPending then
   local witness
   if value.specialization~='NONE' and value.potential>1 then
    witness=gate(city)
    assert(witness[1]==pid and witness[2]==value.cityID and witness[3]=='KNOWN'
     and value.active==math.min(value.potential,witness[4]),'EFFECTIVE_GOVERNOR_CHANGED_DURING_READ')
   end
   assert(stamp(pid,city)==identity and generation==before and writes==0,'EFFECTIVE_FACTS_CHANGED_DURING_READ')
   if phase.count<2048 then
    phase.count=phase.count+1
    phase.values[key]={identity=identity,value=clone(value),gate=witness}
   end
  end
  return clone(value)
 end
 function data.Read(pid,city)
  local result=pack(pcall(phasedRead,pid,city))
  if not result[1]then data.Invalidate()end
  return finish(result)
 end
 -- A RuntimeWork audit keeps its existing local reuse, but every lookup now revalidates.
 -- Detached scope is owned only by that short-lived batch; no registry retains it.
 function data.NewReader()
  local scope={values={},count=0,version=generation}
  return function(pid,city)
   if phase then return data.Read(pid,city)end
   if scope.version~=generation then scope.values={};scope.count=0 end
   phase=scope;local result=pack(pcall(data.Read,pid,city));phase=nil;scope.version=generation
   return finish(result)
  end
 end
 P.FactReadService=data
 function data.Describe(pid,city)
  local store=shared.CityProgressionStore
  local failure=store and store.FailureReport and store.FailureReport()
  if failure then return failure end
  if store and city and store.Owns and not store.Owns(city) then return store.Describe(pid,city) end
  local ok,result=pcall(function()
   local f=data.Read(pid,city)
   return 'B033 city='..f.cityID..' | '..f.specialization
    ..'\nPotential='..f.potential..' | ACTIVE='..tostring(f.active)..' | '..f.activeStatus
    ..'\nCompleted investments='..f.investmentCount..' | pending='..tostring(f.investmentPending)
    ..'\nLedger='..f.ledgerStatus
    ..'\nRead only. Lv2 housing/GPP automatic; inspect native city and Great People UI.'
  end)
  if ok then return result end
  local reason=tostring(result):match('[^\r\n]+') or 'UNKNOWN';reason=reason:gsub('^.-:%d+: ','')
  return '城市专业暂不可读\n原因：'..reason..'\n未推断或重建专业历史；请保留报告。'
 end
end
