-- City-owned engineering study history. E is current civilization knowledge,
-- never the authority for saved L. Only successful full-turn receipts increase L.
SPCEngineeringStudyModel={}
local M=SPCEngineeringStudyModel
local function copy(v)if type(v)~='table'then return v end;local n={};for k,x in pairs(v)do n[k]=copy(x)end;return n end
M.Copy=copy
local function int(v)return type(v)=='number' and v>=0 and v%1==0 and v<=9007199254740991 end
local function ref(v)return type(v)=='table' and int(v.owner) and int(v.cityID) and int(v.x) and int(v.y)end
function M.New()return {version=1,serial=0,L=0,receipts={}}end
function M.Validate(v,r)
 assert(type(v)=='table' and v.version==1 and int(v.serial) and int(v.L) and type(v.receipts)=='table','EST_HISTORY_INVALID')
 local n,ids=0,{}
 for level,a in pairs(v.receipts)do
  assert(int(level) and level>=1 and level<=v.L and type(a)=='table' and int(a.id) and a.id>0 and a.id<=v.serial
   and not ids[a.id] and int(a.start) and a.completed==a.start+1,'EST_RECEIPT_INVALID')
  n=n+1;ids[a.id]=true
 end
 assert(n==v.L,'EST_HISTORY_INCOMPLETE')
 if v.last then assert(type(v.last)=='table' and int(v.last.id) and v.last.id<=v.serial
  and type(v.last.reason)=='string' and #v.last.reason<=100,'EST_LAST_INVALID')end
 local p=v.pending
 if p then
  assert(type(p)=='table' and p.id==v.serial and p.id>0 and not ids[p.id] and int(p.start) and type(p.ended)=='boolean'
   and ref(p.reference) and type(p.token)=='string' and #p.token>0
   and (p.stage=='ACTIVE' or p.stage=='CALLING' or p.stage=='HELD') and type(p.reason)=='string','EST_PENDING_INVALID')
  if r then
   local a=r.current or r.origin
   assert(r.stage=='ACTIVE' and p.token==r.base.token and a.owner==p.reference.owner and a.cityID==p.reference.cityID
    and a.x==p.reference.x and a.y==p.reference.y,'EST_PENDING_REFERENCE')
  end
 end
 return v
end
function M.Begin(v,token,reference,turn,E)
 v=copy(v or M.New());M.Validate(v)
 assert(not v.pending and int(E) and v.L<E and int(turn) and ref(reference),'EST_BEGIN_REJECTED')
 v.serial=v.serial+1;v.pending={id=v.serial,token=token,reference=copy(reference),start=turn,ended=false,stage='ACTIVE',reason='EST_FULL_TURN'}
 M.Validate(v);return v
end
function M.Cancel(v,reason)
 if not v or not v.pending then return v end
 v=copy(v);v.last={id=v.pending.id,reason=reason};v.pending=nil;M.Validate(v);return v
end
function M.Hold(v,reason)v=copy(v);assert(v and v.pending,'EST_NO_PENDING');v.pending.stage='HELD';v.pending.reason=reason;return v end
function M.EndTurn(v,turn)
 v=copy(v);local p=assert(v and v.pending,'EST_NO_PENDING');assert(p.stage=='ACTIVE' and p.start==turn,'EST_END_WINDOW');p.ended=true;return v
end
function M.Calling(v,turn)
 v=copy(v);local p=assert(v and v.pending,'EST_NO_PENDING')
 assert(p.stage=='ACTIVE' and p.ended and turn==p.start+1,'EST_FULL_TURN_UNCONFIRMED');p.stage='CALLING';p.reason='EST_NATIVE_PENDING';return v
end
function M.Complete(v,id,turn)
 v=copy(v);M.Validate(v);local p=assert(v.pending,'EST_NO_PENDING')
 assert(p.id==id and (p.stage=='ACTIVE' or p.stage=='CALLING') and p.ended and turn==p.start+1,'EST_FULL_TURN_UNCONFIRMED')
 v.L=v.L+1;v.receipts[v.L]={id=id,start=p.start,completed=turn};v.last={id=id,reason='EST_COMPLETED'};v.pending=nil;M.Validate(v);return v
end
