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
 function data.Read(pid,city)
  assert(P.IsTestPlayer(pid) and city:GetOwner()==pid,'EFFECTIVE_OWNER_CHANGED')
  local f=shared.CityFlowProbe.SupportFacts(pid,city)
  assert(f.owner==pid and f.cityID==city:GetID() and type(f.token)=='string','EFFECTIVE_FOUNDATION_IDENTITY')
  local ledger=city:GetProperty(KEY)
  local n=0
  if f.specialization=='NONE' then
   assert(f.potential==0 and ledger==nil,'UNASSIGNED_INVESTMENT_CONFLICT')
  else
   assert(kinds[f.specialization] and f.potential==1 and type(f.first)=='table','EFFECTIVE_FOUNDATION_INVALID')
   if ledger~=nil then
    local anchor={owner=pid,cityID=f.cityID,token=f.token,first=clone(f.first),specialization=f.specialization}
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
   local gate=P.CityRoleFacts(city)
   if gate.owner==pid and gate.cityID==f.cityID and gate.governorGateStatus=='KNOWN'
    and type(gate.governorLevelCeiling)=='number' and gate.governorLevelCeiling%1==0
    and gate.governorLevelCeiling>=1 and gate.governorLevelCeiling<=4 then
    out.active=math.min(out.potential,gate.governorLevelCeiling)
   else out.active=nil;out.activeStatus='UNKNOWN_GOVERNOR' end
  end
  return out
 end
 function data.Describe(pid,city)
  local ok,result=pcall(function()
   local f=data.Read(pid,city)
   return 'B033 city='..f.cityID..' | '..f.specialization
    ..'\nPotential='..f.potential..' | ACTIVE='..tostring(f.active)..' | '..f.activeStatus
    ..'\nCompleted investments='..f.investmentCount..' | pending='..tostring(f.investmentPending)
    ..'\nLedger='..f.ledgerStatus
    ..'\nRead only. Lv2 housing/GPP automatic; inspect native city and Great People UI.'
  end)
  return ok and result or ('B033 progression UNKNOWN: '..tostring(result))
 end
end
