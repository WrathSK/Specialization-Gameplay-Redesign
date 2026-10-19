-- B241: bounded business state and pure quotes; no native calls or effect writer.
SPCCapitalInvestmentModel={}
local M=SPCCapitalInvestmentModel
M.Domains={
 {id='DISTRICT_CAMPUS',kind='RESEARCH',nameKey='LOC_SPC_CAPITAL_RESEARCH'},
 {id='DISTRICT_THEATER',kind='CULTURE',nameKey='LOC_SPC_CAPITAL_CULTURE'},
 {id='DISTRICT_INDUSTRIAL_ZONE',kind='INDUSTRY',nameKey='LOC_SPC_CAPITAL_INDUSTRY'}}
local domains={};for _,r in ipairs(M.Domains)do domains[r.id]=true end
local function copy(v)if type(v)~='table'then return v end;local n={};for k,x in pairs(v)do n[k]=copy(x)end;return n end
M.Copy=copy
function M.Same(a,b)
 if type(a)~=type(b)then return false end;if type(a)~='table'then return a==b end
 for k,v in pairs(a)do if not M.Same(v,b[k])then return false end end
 for k in pairs(b)do if a[k]==nil then return false end end;return true
end
function M.Finite(n)return type(n)=='number' and n==n and n>=0 and n<math.huge end
local function int(n)return M.Finite(n) and n%1==0 and n<2147483648 end
local function reference(r)
 return type(r)=='table' and int(r.owner) and int(r.cityID) and int(r.x) and int(r.y)
  and type(r.token)=='string' and #r.token>0 and int(r.changes)
end
local stages={DEBIT_INTENT=true,DEBIT_CALLING=true,ACTIVE=true,CREDIT_INTENT=true,CREDIT_CALLING=true,SETTLED=true,TERMINATED=true,HELD=true}
function M.New()return {version=1,sequence=0,contracts={},protection={}}end
function M.Validate(v)
 assert(type(v)=='table' and v.version==1 and int(v.sequence) and type(v.contracts)=='table' and type(v.protection)=='table','CAPITAL_HISTORY_INVALID')
 local owners=0;for k,n in pairs(v.protection)do
  assert(type(k)=='string' and k:match('^%d+$') and tonumber(k)<64 and int(n),'CAPITAL_PROTECTION_INVALID');owners=owners+1
 end;assert(owners<=64,'CAPITAL_PROTECTION_INVALID')
 local count=0;for domain,c in pairs(v.contracts)do
  count=count+1;assert(domains[domain] and type(c)=='table' and c.domain==domain and stages[c.stage]
   and int(c.sequence) and c.sequence>=1 and c.sequence<=v.sequence and type(c.request)=='string' and #c.request<=100
   and reference(c.source) and (c.sSource==nil or reference(c.sSource))
   and (c.mode=='STABLE' or c.mode=='VENTURE') and int(c.start) and c.due==c.start+10
   and M.Finite(c.principal) and c.principal>0 and M.Finite(c.safe) and M.Finite(c.success) and M.Finite(c.failure)
   and c.failure<c.principal and c.safe>=c.principal and c.success>=c.safe
   and M.Finite(c.probability) and c.probability<=.8 and type(c.won)=='boolean'
   and int(c.D) and c.D>=1 and c.D<=10 and int(c.S) and c.S>=1 and c.S<=4
   and (c.C==1 or c.C==1.25) and int(c.R) and c.R<=40 and int(c.failureCount)
   and M.Finite(c.balanceBefore) and M.Finite(c.balanceAfter),'CAPITAL_CONTRACT_INVALID')
  if c.stage=='SETTLED'then assert(M.Finite(c.paid) and int(c.settledTurn),'CAPITAL_RECEIPT_INVALID')end
 end;assert(count<=3,'CAPITAL_CONTRACT_BOUND')
 return v
end
function M.Open(c)return c and c.stage~='SETTLED' and c.stage~='TERMINATED'end
function M.Choose(candidates)
 local best,tied=0,{}
 for _,v in ipairs(candidates)do
  assert(reference(v.reference) and int(v.level) and v.level>=1 and v.level<=4,'CAPITAL_SOURCE_UNKNOWN')
  if v.level>best then best=v.level;tied={v}elseif v.level==best then tied[#tied+1]=v end
 end
 if #tied==0 then return nil,1 end
 if #tied>1 then
  for _,v in ipairs(tied)do assert(int(v.attained),'CAPITAL_ATTAINMENT_HISTORY_UNKNOWN')end
  table.sort(tied,function(a,b)
   if a.attained~=b.attained then return a.attained<b.attained end
   if a.reference.cityID~=b.reference.cityID then return a.reference.cityID<b.reference.cityID end
   return a.reference.token<b.reference.token
  end)
 end
 return copy(tied[1]),best
end
function M.Quote(input)
 assert(domains[input.domain] and reference(input.source) and int(input.turn)
  and int(input.D) and input.D<=10 and int(input.R) and input.R<=40
  and int(input.failureCount) and M.Finite(input.balance),'CAPITAL_QUOTE_UNKNOWN')
 local chosen,S=M.Choose(input.candidates or {})
 local D=math.max(1,input.D);local C=input.commercialized and 1.25 or 1
 local principal=input.balance/4;local r=.01*D*S*C
 local base=math.min(.8,.4+.01*D*S)
 local probability=.8-(.8-base)*(.75^input.failureCount)
 local safe=principal*(1+r);local success=principal*(1+3*r);local failure=principal*(.5+.005*input.R)
 local q={domain=input.domain,source=copy(input.source),sSource=chosen and copy(chosen.reference),attained=chosen and chosen.attained,
  sourceName=input.sourceName,sSourceName=chosen and chosen.name,turn=input.turn,due=input.turn+10,
  D=D,S=S,C=C,R=input.R,principal=principal,balance=input.balance,r=r,probability=probability,
  safe=safe,success=success,failure=failure,expected=probability*success+(1-probability)*failure,failureCount=input.failureCount}
 q.net=q.expected-principal;return q
end
function M.Begin(old,q,mode,roll,request)
 local n=copy(old or M.New());M.Validate(n)
 assert(not M.Open(n.contracts[q.domain]),'CAPITAL_DOMAIN_OCCUPIED')
 assert(mode=='STABLE' or mode=='VENTURE','CAPITAL_MODE_INVALID')
 assert(q.principal>0,'CAPITAL_TREASURY_EMPTY')
 assert(type(request)=='string' and #request>0 and #request<=100,'CAPITAL_REQUEST_INVALID')
 assert(M.Finite(roll) and roll<1,'CAPITAL_ROLL_UNAVAILABLE')
 n.sequence=n.sequence+1
 n.contracts[q.domain]={sequence=n.sequence,request=request,domain=q.domain,source=copy(q.source),sSource=copy(q.sSource),
  sourceName=q.sourceName,sSourceName=q.sSourceName,attained=q.attained,mode=mode,start=q.turn,due=q.due,
  principal=q.principal,D=q.D,S=q.S,C=q.C,R=q.R,safe=q.safe,success=q.success,failure=q.failure,
  probability=q.probability,won=mode=='STABLE' or roll<q.probability,failureCount=q.failureCount,
  balanceBefore=q.balance,balanceAfter=q.balance-q.principal,stage='DEBIT_INTENT'}
 return M.Validate(n)
end
function M.Activate(value,domain)
 local n=copy(value);local c=assert(n.contracts[domain]);assert(c.stage=='DEBIT_CALLING','CAPITAL_DEBIT_STAGE')
 local owner=tostring(c.source.owner)
 assert((n.protection[owner] or 0)==c.failureCount,'CAPITAL_PROTECTION_STALE')
 if c.mode=='VENTURE'then n.protection[owner]=c.won and 0 or c.failureCount+1 end
 c.stage='ACTIVE';return M.Validate(n)
end
function M.Payout(c)return c.mode=='STABLE' and c.safe or c.won and c.success or c.failure end
function M.Terminate(value,reason)
 local n=copy(value);for _,c in pairs(n.contracts)do if M.Open(c)then c.stage='TERMINATED';c.reason=reason end end
 return M.Validate(n)
end
function M.ResetProtection(value)local n=copy(value);n.protection={};return M.Validate(n)end
function M.PublicQuote(q)
 local n=copy(q);n.failureCount=nil;return n
end
function M.PublicContract(c)
 if not c then return nil end
 local n=copy(c);n.failureCount=nil
 if c.stage~='SETTLED'then n.won=nil end
 return n
end
