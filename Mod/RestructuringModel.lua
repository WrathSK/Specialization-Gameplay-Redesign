-- B247: city-owned current-identity transaction; original admission receipts stay intact.
SPCRestructuringModel={UNIT='UNIT_SPC_RESTRUCTURING_TEAM',UNIT_KEY='SPC_RESTRUCTURING_TEAM_V1'}
local M=SPCRestructuringModel
M.Kinds={RESEARCH=true,CULTURE=true,INDUSTRY=true,COMMERCE=true}
function M.Copy(v)if type(v)~='table'then return v end;local n={};for k,x in pairs(v)do n[k]=M.Copy(x)end;return n end
local cp=M.Copy
function M.Same(a,b)
 if type(a)~=type(b)then return false end;if type(a)~='table'then return a==b end
 for k,v in pairs(a)do if not M.Same(v,b[k])then return false end end
 for k in pairs(b)do if a[k]==nil then return false end end;return true
end
local function int(v)return type(v)=='number' and v>=0 and v%1==0 and v<9007199254740991 end
function M.Count(v)local n=0;for _ in pairs(v and v.investments or {})do n=n+1 end;return n end
function M.Current(r)
 local s=r.restructuring;local b=cp(r.base)
 if s then
  b.specialization=s.identity;b.potential=s.potential;b.first=cp(s.first)
  b.restructuring=true;b.progression=s.phase;b.restructuringSerial=s.serial
 end
 if s then return b,cp(s.investment)end
 return b,cp(r.investment)
end
function M.ValidateLedger(inv,base)
 if not inv then return end
 local a=inv.anchor
 assert(type(inv)=='table' and inv.schema==1 and type(a)=='table' and a.owner==base.owner and a.cityID==base.cityID
  and a.token==base.token and a.specialization==base.specialization and M.Same(a.first,base.first)
  and type(inv.investments)=='table','REST_INVESTMENT_ANCHOR')
 local n,units=0,{}
 for receipt,uid in pairs(inv.investments)do
  assert(type(receipt)=='string' and #receipt>0 and type(uid)=='string' and #uid>0 and not units[uid],'REST_INVESTMENT_RECEIPT')
  units[uid]=true;n=n+1
 end
 assert(n+base.potential<=4 and inv.revision==1+n,'REST_INVESTMENT_CAP')
 if inv.pending then
  local p=inv.pending
  assert(type(p)=='table' and (p.stage=='INTENT' or p.stage=='CONSUMED_CONFIRMED') and int(p.unitID)
   and p.owner==base.owner and p.cityUID==base.token and p.expectedRevision==inv.revision and type(p.receipt)=='string'
   and type(p.unitUID)=='string' and not inv.investments[p.receipt] and not units[p.unitUID] and n+base.potential<4,'REST_INVESTMENT_PENDING')
 end
end
function M.Validate(s,r)
 assert(type(s)=='table' and s.version==1 and int(s.serial) and s.serial>0 and int(s.started)
  and int(s.before) and s.before>=2 and s.before<=4 and M.Kinds[s.previous]
  and type(s.receipt)=='string' and #s.receipt>0 and type(s.team)=='table' and int(s.team.owner) and int(s.team.id)
  and type(s.team.uid)=='string' and #s.team.uid>0 and type(s.institutions)=='table' and type(s.established)=='table','REST_RECORD_INVALID')
 assert(({REALLOCATING=true,CONSUMING=true,SETTLED=true,DISCARDED=true,UNASSIGNED=true})[s.phase],'REST_PHASE_INVALID')
 assert(s.team.owner==r.origin.owner,'REST_TEAM_OWNER')
 for kind,level in pairs(s.established)do assert(M.Kinds[kind] and int(level) and level>=1 and level<=4,'REST_ESTABLISHED_INVALID')end
 for kind,times in pairs(s.institutions)do
  assert(M.Kinds[kind] and type(times)=='table','REST_INSTITUTIONS_INVALID')
  for lv,turn in pairs(times)do assert(int(lv) and lv>=1 and lv<=4 and int(turn),'REST_INSTITUTIONS_INVALID')end
 end
 if s.phase=='SETTLED' then
  assert(M.Kinds[s.identity] and int(s.potential) and s.potential>=1 and s.potential<=3 and type(s.first)=='table'
   and int(s.first.districtID) and type(s.first.type)=='string' and int(s.first.turn),'REST_IDENTITY_INVALID')
  assert((s.consumed==true and s.potential==s.before-1 and s.first.turn>=s.started+5) or (s.consumed==nil and int(s.recaptureTurn) and s.potential==1 and s.first.turn>=s.recaptureTurn),'REST_IDENTITY_PROOF')
 elseif s.phase=='UNASSIGNED' or s.phase=='DISCARDED' then
  assert(s.identity=='NONE' and s.potential==0 and s.first==nil and s.investment==nil,'REST_DISCARDED_IDENTITY')
 else
  assert(s.identity=='NONE' and s.potential==s.before-1 and s.first==nil and s.investment==nil,'REST_REALLOCATING_IDENTITY')
 end
 if s.consumed~=nil then assert(s.consumed==true and (s.phase=='CONSUMING' or s.phase=='SETTLED'),'REST_CONSUMED_INVALID')end
 if s.phase=='CONSUMING' then
  local c=s.configuration
  assert(type(c)=='table' and M.Kinds[c.kind] and c.kind~=s.previous and type(c.first)=='table'
   and int(c.first.districtID) and type(c.first.type)=='string' and c.first.turn>=s.started+5,'REST_CONFIGURATION_INVALID')
 end
 if s.phase=='UNASSIGNED' then
  assert(type(s.candidates)=='table' and int(s.recaptureTurn),'REST_RECAPTURE_INVALID')
  for kind,value in pairs(s.candidates)do assert(M.Kinds[kind] and value==true,'REST_CANDIDATE_INVALID')end
 end
 for serial,e in pairs(s.epochs or {})do
  assert(int(serial) and serial<s.serial and type(e)=='table' and e.base.token==r.base.token,'REST_EPOCH_INVALID');M.ValidateLedger(e.investment,e.base)
 end
 local b=M.Current(r);M.ValidateLedger(s.investment,b)
 return s
end
function M.Begin(r,f,team,receipt,turn)
 assert(M.Kinds[f.specialization] and f.potential>=2 and not f.investmentPending,'REST_TARGET_INELIGIBLE')
 local old=r.restructuring;assert(not old or old.phase=='SETTLED','REST_ALREADY_ACTIVE')
 local history=cp(old and old.institutions or {})
 local established=cp(old and old.established or {});established[f.specialization]=math.max(established[f.specialization] or 0,f.potential)
 history[f.specialization]=history[f.specialization] or {}
 local times=history[f.specialization]
 if not old then
  times[1]=r.base.first.turn
  for level,t in pairs(r.institutionTurns or {})do times[level]=t end
 end
 -- All established levels exist; an unavailable historic date is not invented.
 local epochs=cp(old and old.epochs or {})
 if old and old.investment then local b=M.Current(r);epochs[old.serial]={base=b,investment=cp(old.investment)}end
 local s={version=1,serial=(old and old.serial or 0)+1,phase='REALLOCATING',identity='NONE',potential=f.potential-1,
  before=f.potential,previous=f.specialization,started=turn,team=cp(team),receipt=receipt,institutions=history,established=established,epochs=epochs}
 return s
end
function M.Configure(s,kind,first,turn)
 assert(s.phase=='REALLOCATING' and turn>=s.started+5 and M.Kinds[kind] and kind~=s.previous,'REST_CONFIGURATION_INELIGIBLE')
 local n=cp(s);n.phase='CONSUMING';n.configuration={kind=kind,first=cp(first)};n.configuration.first.turn=turn;return n
end
function M.Finish(s)
 assert(s.phase=='CONSUMING' and s.consumed==true,'REST_NO_CONSUMPTION_RECEIPT')
 local n=cp(s);n.phase='SETTLED';n.identity=n.configuration.kind;n.first=cp(n.configuration.first);n.configuration=nil
 n.established[n.identity]=math.max(n.established[n.identity] or 0,n.potential)
 n.institutions[n.identity]=n.institutions[n.identity] or {}
 for level=1,n.potential do n.institutions[n.identity][level]=n.institutions[n.identity][level] or n.first.turn end
 return n
end
function M.Discard(s)
 local n=cp(s);n.phase='DISCARDED';n.identity='NONE';n.potential=0;n.first=nil;n.investment=nil;n.configuration=nil;n.candidates=nil;n.consumed=nil;return n
end
function M.Recapture(s,candidates,turn)
 assert(s.phase=='DISCARDED','REST_RECAPTURE_PHASE');local n=cp(s);n.phase='UNASSIGNED';n.candidates=cp(candidates);n.recaptureTurn=turn;return n
end
function M.Claim(s,kind,first)
 assert(s.phase=='UNASSIGNED' and (next(s.candidates)==nil or s.candidates[kind]),'REST_CLAIM_INELIGIBLE')
 local n=cp(s);n.phase='SETTLED';n.identity=kind;n.potential=1;n.first=cp(first);n.candidates=nil
 n.established[kind]=math.max(n.established[kind] or 0,1);n.institutions[kind]=n.institutions[kind] or {};n.institutions[kind][1]=n.institutions[kind][1] or first.turn;return n
end
-- Bounded first-P4 evidence for a post-restructuring investment epoch.
function M.Qualification(r,base,inv,receipt)
 assert(base.potential+M.Count(inv)==4 and inv and inv.investments[receipt],'REST_P4_UNCONFIRMED')
 return {token=r.base.token,base=cp(base),investment=cp(inv)}
end
function M.ValidateQualification(q,r,receipt,start,kind)
 assert(type(q)=='table' and q.token==r.base.token and q.base.token==q.token and q.base.specialization==kind
  and q.base.owner==r.origin.owner and q.base.x==r.origin.x and q.base.y==r.origin.y and start>=q.base.first.turn,'REST_P4_ORIGIN')
 M.ValidateLedger(q.investment,q.base)
 assert(q.investment.pending==nil and q.investment.investments[receipt] and q.base.potential+M.Count(q.investment)==4,'REST_P4_RECEIPTS')
end
