-- B246: district-bound contracts. Capital contributes pure value/receipt helpers
-- only; its contract slots, source selection, random outcomes and timers are unused.
include('CapitalInvestmentModel')
SPCDevelopmentInvestmentModel={}
local M=SPCDevelopmentInvestmentModel;local V=SPCCapitalInvestmentModel
M.Copy=V.Copy;M.Same=V.Same;M.Finite=V.Finite;M.MoneyMatches=V.MoneyMatches;M.MONEY_TOLERANCE=V.MONEY_TOLERANCE
local function int(n)return M.Finite(n) and n%1==0 and n<2147483648 end
local function ref(r)return type(r)=='table' and int(r.owner) and int(r.cityID) and int(r.x) and int(r.y)
 and type(r.token)=='string' and #r.token>0 and #r.token<=100 and int(r.changes)end
local stages={DEBIT_INTENT=true,DEBIT_CALLING=true,ACTIVE=true,COMPLETED=true,TERMINATED=true,HELD=true}
function M.Open(c)return c and c.stage~='COMPLETED' and c.stage~='TERMINATED'end
function M.New()return {version=1,sequence=0,contracts={}}end
function M.Validate(v)
 assert(type(v)=='table' and v.version==1 and int(v.sequence) and type(v.contracts)=='table','DEVELOPMENT_HISTORY_INVALID')
 for key,c in pairs(v.contracts)do
  assert(type(c)=='table' and ref(c.source) and ref(c.target) and key==c.target.token and c.source.owner==c.target.owner
   and c.source.token~=c.target.token and int(c.sequence) and c.sequence>0 and c.sequence<=v.sequence
   and type(c.request)=='string' and #c.request>0 and #c.request<=100 and stages[c.stage] and int(c.start)
   and type(c.domain)=='string' and c.domain:match('^DISTRICT_[A-Z0-9_]+$')
   and type(c.quoteBuilding)=='string' and c.quoteBuilding:match('^BUILDING_[A-Z0-9_]+$')
   and M.Finite(c.quoteGold) and c.quoteGold>0 and M.Finite(c.cost) and c.cost==c.quoteGold*.15
   and M.Finite(c.balanceBefore) and M.Finite(c.balanceExpected) and c.balanceExpected==c.balanceBefore-c.cost
   and type(c.existing)=='table','DEVELOPMENT_CONTRACT_INVALID')
  for name,yes in pairs(c.existing)do
   assert(type(name)=='string' and name:match('^BUILDING_[A-Z0-9_]+$') and yes==true,'DEVELOPMENT_BUILDING_HISTORY_INVALID')
  end
  if c.debitAfter~=nil or c.debited~=nil then
   assert(M.MoneyMatches(c.balanceBefore,-c.cost,c.debitAfter) and c.debited==c.balanceBefore-c.debitAfter,'DEVELOPMENT_RECEIPT_INVALID')
  end
  if c.stage=='ACTIVE' or c.stage=='COMPLETED'then assert(c.debited~=nil,'DEVELOPMENT_RECEIPT_MISSING')end
  if c.stage=='DEBIT_INTENT' or c.stage=='DEBIT_CALLING'then assert(c.debited==nil,'DEVELOPMENT_RECEIPT_STAGE')end
  if c.stage=='COMPLETED'then assert(int(c.completedTurn) and type(c.completedBuilding)=='string'
   and not c.existing[c.completedBuilding],'DEVELOPMENT_COMPLETION_INVALID')end
 end
 return v
end
local amounts={quoteGold=true,cost=true,balanceBefore=true,balanceExpected=true,debitAfter=false,debited=false}
function M.Encode(v)
 M.Validate(v);assert(v.numberEncoding==nil,'DEVELOPMENT_ENCODING_INVALID')
 local out=M.Copy(v);out.numberEncoding='DECIMAL17_V1'
 for _,c in pairs(out.contracts)do for k,required in pairs(amounts)do if c[k]~=nil or required then
  local n=c[k];assert(M.Finite(n),'DEVELOPMENT_NUMBER_INVALID');c[k]=string.format('%.17g',n)
  assert(tonumber(c[k])==n,'DEVELOPMENT_NUMBER_ROUNDTRIP')
 end end end;return out
end
function M.Decode(v)
 if v==nil then return nil end
 assert(type(v)=='table' and v.numberEncoding=='DECIMAL17_V1' and type(v.contracts)=='table','DEVELOPMENT_ENCODING_INVALID')
 local out=M.Copy(v);out.numberEncoding=nil
 for _,c in pairs(out.contracts)do
  assert(type(c)=='table','DEVELOPMENT_CONTRACT_INVALID')
  for k,required in pairs(amounts)do if c[k]~=nil or required then
   local s=c[k];assert(type(s)=='string' and #s<=32,'DEVELOPMENT_NUMBER_INVALID')
   local n=tonumber(s);assert(M.Finite(n) and string.format('%.17g',n)==s,'DEVELOPMENT_NUMBER_INVALID');c[k]=n
  end end
 end;return M.Validate(out)
end
function M.Begin(old,q,request)
 local n=M.Copy(old or M.New());M.Validate(n)
 assert(not M.Open(n.contracts[q.target.token]),'DEVELOPMENT_TARGET_OCCUPIED')
 n.sequence=n.sequence+1
 n.contracts[q.target.token]={sequence=n.sequence,source=M.Copy(q.source),target=M.Copy(q.target),domain=q.domain,
  quoteBuilding=q.building,quoteGold=q.price,cost=q.cost,balanceBefore=q.balance,balanceExpected=q.balance-q.cost,
  existing=M.Copy(q.existing),start=q.turn,request=request,stage='DEBIT_INTENT'}
 return M.Validate(n)
end
function M.Activate(v,key,after)
 local n=M.Copy(v);local c=assert(n.contracts[key]);assert(c.stage=='DEBIT_CALLING','DEVELOPMENT_DEBIT_STAGE')
 assert(M.MoneyMatches(c.balanceBefore,-c.cost,after),'DEVELOPMENT_MONEY_UNCONFIRMED')
 c.debitAfter=after;c.debited=c.balanceBefore-after;c.stage='ACTIVE';return M.Validate(n)
end
function M.Terminate(v,reason)
 local n=M.Copy(v);for _,c in pairs(n.contracts)do if M.Open(c)then c.stage='TERMINATED';c.reason=reason end end
 return M.Validate(n)
end
