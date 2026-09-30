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
 function data.Read(pid,city) P.Count('facts');
  assert(P.IsTestPlayer(pid) and city:GetOwner()==pid,'EFFECTIVE_OWNER_CHANGED')
  local f=shared.CityFlowProbe.SupportFacts(pid,city)
  assert(f.owner==pid and f.cityID==city:GetID() and type(f.token)=='string','EFFECTIVE_FOUNDATION_IDENTITY')
  local store=shared.CityProgressionStore
  local ledger
  if store and store.Owns(city) then ledger=store.Investment(pid,city) else ledger=city:GetProperty(KEY) end
  local n=0
  if f.specialization=='NONE' then
   assert(f.potential==0 and ledger==nil,'UNASSIGNED_INVESTMENT_CONFLICT')
  else
   assert(kinds[f.specialization] and f.potential==1 and type(f.first)=='table','EFFECTIVE_FOUNDATION_INVALID')
   if ledger~=nil then
    -- Comparison only: borrow first here; the returned facts below still deep-copy it.
    local anchor={owner=pid,cityID=f.cityID,token=f.token,first=f.first,specialization=f.specialization}
    assert(type(ledger)=='table' and ledger.schema==1 and same(ledger.anchor,anchor),'INVESTMENT_ANCHOR_CHANGED')
    assert(type(ledger.investments)=='table','INVESTMENT_LEDGER_INVALID')
    local units={}
    for receipt,unit in pairs(ledger.investments) do
     assert(type(receipt)=='string' and #receipt>0 and type(unit)=='string' and #unit>0 and not units[unit],'INVESTMENT_RECEIPT_INVALID')
     units[unit]=true;n=n+1;assert(n<=3,'INVESTMENT_CAP_EXCEEDED')
    end
    assert(ledger.revision==1+n,'INVESTMENT_REVISION_INVALID')
    if ledger.pending~=nil then
     local op=ledger.pending
     assert(type(op)=='table' and (op.stage=='INTENT' or op.stage=='CONSUMED_CONFIRMED')
      and type(op.unitID)=='number' and op.unitID>=0 and op.unitID%1==0
      and op.owner==pid and op.cityUID==f.token and op.expectedRevision==ledger.revision
      and type(op.receipt)=='string' and #op.receipt>0 and type(op.unitUID)=='string' and #op.unitUID>0
      and not ledger.investments[op.receipt] and not units[op.unitUID] and n<3,'INVESTMENT_PENDING_INVALID')
    end
   end
  end
  local out=clone(f);out.basePotential=f.potential;out.potential=f.potential+n
  out.investmentCount=n;out.investmentPending=ledger and ledger.pending~=nil or false
  out.ledgerStatus=ledger and 'PRESENT' or 'ABSENT_NO_WRITES'
  out.active=out.potential;out.activeStatus='KNOWN'
  if out.potential>1 then
   local gateOwner,gateCityID,gateStatus,ceiling=P.GovernorGate(city)
   if gateOwner==pid and gateCityID==f.cityID and gateStatus=='KNOWN'
    and type(ceiling)=='number' and ceiling%1==0 and ceiling>=1 and ceiling<=4 then
    out.active=math.min(out.potential,ceiling)
   else out.active=nil;out.activeStatus='UNKNOWN_GOVERNOR' end
  end
  return out
 end
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
