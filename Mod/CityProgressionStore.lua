if not SPCResearchTradition then include('ResearchTradition') end
-- E2: bounded explicit city collection with isolated B103 lifecycle per record.
SPCCityProgressionStore={KEY='SPC_CITY_PROGRESSION_E2_V1',INDEX='SPC_PROGRESSION_INDEX_V3',RECORD='SPC_PROGRESSION_CITY_V3_'}
local function CreateProgressionRecord(P,shared,storage)
 local M=SPCCityIdentityRead;local cp=M.Copy
 local d={exitStatus="NOT_CONFIRMED",exitErrors={}}
 local exits,finished,attempts={},{},{};local exitBusy=false;local runningExit;local exitReads={}
 local returns={};function d.RegisterReturn(name,fn)assert(not returns[name]);returns[name]=fn end
 -- Fixed latest slot per native event; session-only evidence, never identity authority.
 local eventNames={'CityTransfered','CityConquered','CityAddedToMap','CityRemovedFromMap','CityInitialized','CityBuilt'}
 local nativeEvents={};local eventSequence=0
 local root,fault,busy;local ready=false
 local foreignSeen=false;local transition;local transitionFault;local conquest;local foundation;local firstTransitionFault
 local function observe(name,...)
  if not root then return end
  eventSequence=eventSequence+1
  local row={sequence=eventSequence,turn=Game.GetCurrentGameTurn(),argc=select('#',...)}
  for i=1,math.min(6,row.argc)do
   local v=select(i,...);local t=type(v)
   if t=='number' or t=='boolean' then row[i]=v else row[i]=t=='nil' and 'nil' or '<'..t..'>' end
  end
  nativeEvents[name]=row
 end
 local kinds={RESEARCH=true,CULTURE=true,INDUSTRY=true,COMMERCE=true}
 local function same(a,b)
  if type(a)~=type(b) then return false end;if type(a)~='table' then return a==b end
  for k,v in pairs(a) do if not same(v,b[k]) then return false end end
  for k in pairs(b) do if a[k]==nil then return false end end;return true
 end
 local function ref(c)return {owner=c:GetOwner(),cityID=c:GetID(),x=c:GetX(),y=c:GetY()}end
 local function validTransition(proof,loss,current)
  if type(proof)~='table' or (proof.version~=1 and proof.version~=2) or not loss or not same(proof.from,loss.target)
   or not same(proof.to,current) or type(proof.turn)~='number' or proof.turn<0 or proof.turn%1~=0 then return false end
  local r,a,i,t=proof.removed,proof.added,proof.initialized,proof.transferred
  if not (type(r)=='number' and type(a)=='number' and type(i)=='number' and type(t)=='number'
   and r>=1 and r%1==0 and a%1==0 and i%1==0 and t%1==0 and r<a and a<i and i<t) then return false end
  if proof.version==2 then
   local c,b=proof.conquest,proof.foundation
   if type(c)~='table' or type(b)~='table' or c.fromOwner~=loss.target.owner or not same(c.to,current)
    or not same(b.to,current) or c.turn~=proof.turn or b.turn~=proof.turn then return false end
   local cs,bs=c.sequence,b.sequence
   return type(cs)=='number' and type(bs)=='number' and cs>=1 and bs>=1 and cs%1==0 and bs%1==0 and cs<r and bs<t
  end
  return true
 end
 local function source(c)
  local s={ref=ref(c),values={}}
  for _,n in ipairs({'TOKEN','JOURNAL','FLOW','INVEST','TEMPLATES'}) do s.values[n]=c:GetProperty(M.Keys[n])end
  s.ledger=Game:GetProperty('SPC_DEV_BINDING_B013_P'..s.ref.owner)
  return cp(s)
 end
 local function validate(r)
  assert(type(r)=='table' and (r.schema==1 or r.schema==2 or r.schema==3) and (r.stage=='PREPARED' or r.stage=='ACTIVE' or r.stage=='HELD_TRANSFER')
   and type(r.revision)=='number' and r.revision>=1 and r.revision%1==0,'STORE_SCHEMA')
  assert(type(r.origin)=='table' and type(r.base)=='table','STORE_SCOPE')
  if r.schema==1 then
   assert(kinds[r.base.specialization] and r.base.potential==1,'STORE_SCOPE')
  else
   if r.schema==2 then
   local f=r.founding
   assert(type(f)=='table' and f.evidence=='FOUND_CITY+Initialized' and same(f.reference,r.origin)
    and type(f.unitID)=='number' and f.unitID>=0 and f.unitID%1==0 and type(f.reason)=='number'
    and f.reason==f.reason and math.abs(f.reason)<math.huge and f.turn==r.base.foundationTurn,'STORE_FOUNDATION')
   else
    local f=r.acquisition
    assert(type(f)=='table' and f.evidence=='CONQUEST+Initialized+Transfer' and same(f.reference,r.origin)
     and type(f.oldOwner)=='number' and f.oldOwner>=0 and f.oldOwner%1==0 and f.oldOwner~=r.origin.owner
     and f.turn==r.base.foundationTurn and type(f.legacySet)=='table','STORE_ACQUISITION')
    local c,a,i,t=f.conquered,f.added,f.initialized,f.transferred
    assert(type(c)=='number' and type(a)=='number' and type(i)=='number' and type(t)=='number'
     and c>=1 and c%1==0 and a%1==0 and i%1==0 and t%1==0 and c<a and a<i and i<t,'STORE_ACQUISITION_ORDER')
    local n=0;for k,v in pairs(f.legacySet)do assert(kinds[k] and v==true,'STORE_LEGACY_SET');n=n+1 end
    assert(f.mode==(n>0 and 'LEGACY_CLAIM' or 'FIRST_COMPLETION'),'STORE_ACQUISITION_MODE')
    if f.mode=='LEGACY_CLAIM' and r.progression=='SPECIALIZED' then
     local a=r.claim
     assert(type(a)=='table' and a.version==1 and a.kind==r.base.specialization and f.legacySet[a.kind]
      and a.project=='PROJECT_SPC_CLAIM_'..a.kind and a.token==r.base.token and same(a.reference,r.origin)
      and a.turn==r.base.first.turn and a.turn>=f.turn,'CLAIM_RECEIPT_INVALID')
    else assert(r.claim==nil,'CLAIM_UNEXPECTED_RECEIPT')end
   end
   assert(r.stage~='PREPARED' and (r.completionError==nil or type(r.completionError)=='string'),'STORE_FRESH_STAGE')
   if r.progression=='UNASSIGNED' then
    assert(r.base.specialization=='NONE' and r.base.potential==0 and r.base.first==nil
     and r.investment==nil and r.templates==nil and r.currentFirst==nil,'STORE_UNASSIGNED')
   else assert(r.progression=='SPECIALIZED' and kinds[r.base.specialization] and r.base.potential==1,'STORE_SCOPE')end
  end
  -- B140: missing history is not proof of first initialization. The optional
  -- extension adopts only validated existing ledgers; old ambiguous nil stays held.
  if r.templateLifecycle then
   local t=r.templateLifecycle
   assert(r.base.specialization=='INDUSTRY' and type(t)=='table' and t.version==1
    and (t.state=='UNINITIALIZED' or t.state=='INITIALIZED') and type(t.reconcilePending)=='boolean','TEMPLATES_LIFECYCLE_INVALID')
   assert(t.state~='UNINITIALIZED' or (r.templates==nil and t.reconcilePending),'TEMPLATES_LIFECYCLE_CONFLICT')
  end
  if r.researchTradition then SPCResearchTradition.Validate(r.researchTradition,r) end
  if r.claimTimer then
   local t=r.claimTimer
   assert(r.schema==3 and r.acquisition.mode=='LEGACY_CLAIM' and r.progression=='UNASSIGNED'
    and t.version==1 and t.token==r.base.token and same(t.reference,r.current or r.origin)
    and r.acquisition.legacySet[t.kind] and t.project=='PROJECT_SPC_CLAIM_'..t.kind
    and type(t.start)=='number' and t.start%1==0 and t.start>=r.acquisition.turn
    and type(t.deactivated)=='boolean' and (t.stage=='ACTIVE' or t.stage=='CALLING' or t.stage=='STOPPED')
    and type(t.reason)=='string','CLAIM_TIMER_INVALID')
  end
  -- Reuse the established bounded structural validator; live pending debit is checked
  -- by EffectiveFacts and InvestmentAction, not interpreted as a fresh import.
  local inv=cp(r.investment);if inv then inv.pending=nil end
  local v={TOKEN=r.base.token,JOURNAL=r.base,FLOW={schema=1,owner=r.base.owner,cityID=r.base.cityID,
   x=r.base.x,y=r.base.y,token=r.base.token,revision=1,stage='DONE',facts=r.base,target=r.base},INVEST=inv,TEMPLATES=r.templates}
  assert(M.Preview({ref=r.origin,values=v,ledger=r.binding}).state=='LOCAL_CANDIDATE','STORE_RECORD_INVALID')
  if r.current then
   assert((r.returnEvidence=='CityTransfered+original_binding' or (r.returnEvidence=='NATIVE_TRANSITION_V1' and validTransition(r.returnProof,r.lastLoss,r.current))) and r.lastLoss and same(r.lastLoss.origin,r.origin)
    and r.lastLoss.target.owner~=r.origin.owner
    and r.current.owner==r.origin.owner and type(r.current.cityID)=='number' and r.current.cityID>=0 and r.current.cityID%1==0
    and r.current.x==r.origin.x and r.current.y==r.origin.y,'STORE_CURRENT_REFERENCE')
   if r.progression=='UNASSIGNED' then assert(r.currentFirst==nil,'STORE_UNASSIGNED_ANCHOR')
   else assert(type(r.currentFirst)=='table' and r.currentFirst.turn==r.base.first.turn
    and r.currentFirst.type==r.base.first.type and type(r.currentFirst.districtID)=='number','STORE_CURRENT_FIRST')end
  end
  if r.loss then
   assert(r.stage=='HELD_TRANSFER' and same(r.loss.origin,r.origin) and r.loss.evidence=='CityTransfered+live_reference'
    and type(r.loss.target)=='table' and type(r.loss.target.owner)=='number' and r.loss.target.owner>=0
    and r.loss.target.owner~=r.origin.owner and type(r.loss.target.cityID)=='number'
    and r.loss.target.x==r.origin.x and r.loss.target.y==r.origin.y,'STORE_LOSS_EVIDENCE')
  end
  assert(r.referenceInvalidated==nil or r.referenceInvalidated==true,'STORE_REFERENCE_INVALIDATION')
  assert(r.stage~='PREPARED' or type(r.source)=='table','STORE_PREPARED_SOURCE')
 end
 -- Called by every old writer before entering player-wide error/repair handling.
 function d.Owns(c)
  if not ready then return true end -- unreadable root: never assume legacy authority
  if not root then return false end
  if type(root)~='table' or type(root.origin)~='table' then return true end
  local r=root.origin
  return c and c:GetX()==r.x and c:GetY()==r.y or false -- old cityID may be reused elsewhere
 end
 function d.IsRecaptured(c)return root and root.current~=nil and d.Owns(c) or false end
 local function active(pid,c)
  storage.Check()
  assert(ready and not fault and root and root.stage=='ACTIVE','PROGRESSION_HELD')
  assert(P.IsTestPlayer(pid) and pid==root.origin.owner and same(ref(c),root.current or root.origin),'PROGRESSION_REFERENCE_CHANGED')
  assert(not root.referenceInvalidated,'PROGRESSION_REFERENCE_REMOVED')
  assert(not root.completionError,root.completionError)
  if root.schema>=2 and not root.current then assert(c:GetProperty(M.Keys.TOKEN)==root.base.token,'PROGRESSION_BINDING_UNAVAILABLE')end
  if root.current then
   local token=c:GetProperty(M.Keys.TOKEN)
   if root.returnEvidence=='NATIVE_TRANSITION_V1' then
    assert(validTransition(root.returnProof,root.lastLoss,root.current) and (token==nil or token==root.base.token),'PROGRESSION_BINDING_CONFLICT')
   else assert(token==root.base.token,'PROGRESSION_BINDING_UNAVAILABLE')end
  end
  return root
 end
 local function projected(r,v,investment)
  v=cp(v);if not v or not r.current then return v end
  local a=investment and v.anchor or v;a.cityID=r.current.cityID;a.first=cp(r.currentFirst)
  return v
 end
 function d.Base(pid,c)local r=active(pid,c);return projected(r,r.base,false)end
 function d.Investment(pid,c)local r=active(pid,c);return projected(r,r.investment,true)end
 local function save(nextValue)
  assert(not fault,'STORE_WRITE_HELD');validate(nextValue)
  local previous=root;root=cp(nextValue) -- protect target before engine callbacks
  local ok,err=pcall(storage.Write,previous,nextValue)
  if not ok then fault=tostring(err);error(fault)end
 end
 function d.ReadTradition(pid,c)return cp(active(pid,c).researchTradition)end
 function d.VisitTradition(pid,fn)
  if not ready or fault or not root or root.stage~='ACTIVE' or root.origin.owner~=pid or not root.researchTradition then return end
  local a=root.current or root.origin
  local c=CityManager.GetCityAt(a.x,a.y)
  if c and c:GetOwner()==pid then fn(c)end -- consumer revalidates exact persistent reference
 end
 -- Only this record owns age writes. No diagnostics/effect writers participate.
 function d.TickTradition(pid,turn)
  if not ready or fault or not root or root.origin.owner~=pid or not root.researchTradition
   or root.stage~='ACTIVE' then return end
  local ok,err=pcall(function()
   local a=root.current or root.origin
   local c=assert(CityManager.GetCityAt(a.x,a.y),'TRADITION_CITY_UNKNOWN')
   local r=active(pid,c)
   local value=SPCResearchTradition.Advance(r.researchTradition,turn,r.base.specialization)
   if not same(value,r.researchTradition) then
    local n=cp(r);n.researchTradition=value;n.revision=n.revision+1;save(n)
   end
  end)
  d.traditionError=not ok and tostring(err) or nil
 end
 -- Session-only transition assembly. Never reconstruct an incomplete chain at load.
 local function track(name,owner,id,x,y)
  if not ready or fault or not root then return end
  local current=root.current or root.origin
  if name=='CityRemovedFromMap' and root.stage=='ACTIVE' and owner==current.owner and id==current.cityID then
   if not root.referenceInvalidated then local n=cp(root);n.referenceInvalidated=true;n.revision=n.revision+1;save(n)end
  end
  if not root.loss or root.stage~='HELD_TRANSFER' then return end
  local old=root.loss.target;local turn=Game.GetCurrentGameTurn()
  if name=='CityRemovedFromMap' and owner==old.owner and id==old.cityID then
   if not foreignSeen then transitionFault='RETURN_FOREIGN_REFERENCE_UNOBSERVED';return end
   if transition then
    if transition.turn~=turn then transitionFault='RETURN_CHAIN_CONFLICT'end
    return -- identical repeated removal is not another generation
   end
   transition={version=1,from=cp(old),turn=turn,removed=eventSequence}
  elseif (name=='CityAddedToMap' or name=='CityInitialized') and x==old.x and y==old.y then
   -- Saved foreign objects are also added/initialized during load. They are not
   -- a return candidate. Exempt only the exact saved reference before any transfer
   -- evidence; never clear a prior fault or reconstruct a partially loaded chain.
   if not transition and not conquest and not foundation and owner==old.owner and id==old.cityID then return end
   if not transition then transitionFault='RETURN_CHAIN_ORDER';return end
   if transition.turn~=turn or owner~=root.origin.owner or type(id)~='number' or id<0 or id%1~=0 then
    transitionFault='RETURN_CHAIN_CONFLICT';return
   end
   local endpoint={owner=owner,cityID=id,x=x,y=y}
   if transition.to and not same(transition.to,endpoint) then transitionFault='RETURN_CHAIN_CONFLICT';return end
   transition.to=endpoint
   if name=='CityAddedToMap' then
    if not transition.added then transition.added=eventSequence end
   elseif not transition.added then transitionFault='RETURN_CHAIN_ORDER'
   elseif not transition.initialized then transition.initialized=eventSequence end
  elseif name=='CityRemovedFromMap' and transition and transition.to
   and owner==transition.to.owner and id==transition.to.cityID then transitionFault='RETURN_CHAIN_TARGET_REMOVED'
  elseif name=='CityBuilt' and x==old.x and y==old.y then
   local row={to={owner=owner,cityID=id,x=x,y=y},turn=turn,sequence=eventSequence}
   if foundation and (not same(foundation.to,row.to) or foundation.turn~=turn) then transitionFault='RETURN_FOUNDATION_CONFLICT'
   elseif not foundation then foundation=row end
  end
 end
 local function trackConquest(newOwner,oldOwner,newID,x,y)
  if not ready or fault or not root or not root.loss or root.stage~='HELD_TRANSFER' then return end
  local old=root.loss.target
  if x~=old.x or y~=old.y then return end
  if newOwner~=root.origin.owner or oldOwner~=old.owner or type(newID)~='number' or newID<0 or newID%1~=0 then
   transitionFault='RETURN_CONQUEST_CONFLICT';return
  end
  local row={fromOwner=oldOwner,to={owner=newOwner,cityID=newID,x=x,y=y},turn=Game.GetCurrentGameTurn(),sequence=eventSequence}
  if conquest and (not same(conquest.to,row.to) or conquest.turn~=row.turn) then transitionFault='RETURN_CONQUEST_CONFLICT'
  elseif not conquest then conquest=row end
 end
 local function rememberFault(name)
  if transitionFault and not firstTransitionFault then
   firstTransitionFault={reason=transitionFault,name=name,event=cp(nativeEvents[name])}
  end
 end
 local function trackSafely(name,...)
  local ok=pcall(track,name,...)
  if not ok then transitionFault='RETURN_CHAIN_READ_FAILED' end
  rememberFault(name)
 end
 function d.WriteInvestment(pid,c,old,nextValue)
  local r=active(pid,c);assert(same(projected(r,r.investment,true),old),'STALE_LEDGER')
  local n=cp(r);n.investment=cp(nextValue)
  if n.investment then n.investment.anchor.cityID=r.origin.cityID;n.investment.anchor.first=cp(r.base.first)end
  local function receipts(v)local count=0;for _ in pairs(v and v.investments or {})do count=count+1 end;return count end
  if r.base.specialization=='RESEARCH' and not r.researchTradition and receipts(old)==2 and receipts(nextValue)==3 then
   local op=old and old.pending
   assert(op and op.stage=='CONSUMED_CONFIRMED' and nextValue.pending==nil
    and nextValue.investments[op.receipt]==op.unitUID,'TRADITION_FIRST_P4_UNCONFIRMED')
   n.researchTradition=SPCResearchTradition.Begin(Game.GetCurrentGameTurn(),op.receipt)
  end
  n.revision=n.revision+1;save(n)
  if n.researchTradition and shared.ResearchTraditionEffects then shared.ResearchTraditionEffects.Mark(pid)end
 end
 -- Only the existing Standardization module owns interpretation of this ledger.
 function d.ReadTemplates(c)
  local r=active(c:GetOwner(),c)
  if not r.templatesCaptured then
   assert(not r.current,'TEMPLATES_HISTORY_UNAVAILABLE')
   local n=cp(r);n.templates=c:GetProperty(M.Keys.TEMPLATES);n.templatesCaptured=true;n.revision=n.revision+1;save(n)
  end
  local t=root.templateLifecycle
  if root.base.specialization=='INDUSTRY' then
   assert(root.templates~=nil or (t and t.state=='UNINITIALIZED'),'TEMPLATES_HISTORY_UNAVAILABLE')
   return cp(root.templates),t==nil or t.reconcilePending
  end
  return cp(root.templates),false
 end
 function d.WriteTemplates(c,old,value)
  local r=active(c:GetOwner(),c)
  local current=d.ReadTemplates(c) -- same missing-history guard for every writer
  r=active(c:GetOwner(),c) -- a legacy capture may have replaced the record
  assert(r.base.specialization=='INDUSTRY' and r.templatesCaptured and same(current,old),'TEMPLATES_STALE')
  assert(type(value)=='table' and value.initialized==true,'TEMPLATES_VALUE_INVALID')
  if same(old,value) and r.templateLifecycle and not r.templateLifecycle.reconcilePending then return end
  local n=cp(root);n.templates=cp(value)
  n.templateLifecycle={version=1,state='INITIALIZED',reconcilePending=false}
  n.revision=n.revision+1;save(n) -- ledger and initialization acknowledgement share one city-record write
 end
 -- Fresh records use the same fact shape but never create legacy City journals.
 function d.Found(c,proof,binding)
  assert(ready and not fault and root==nil and same(ref(c),proof.reference),'FOUND_REFERENCE_CHANGED')
  local a=ref(c);local token=c:GetProperty(M.Keys.TOKEN)
  save({schema=2,stage='ACTIVE',progression='UNASSIGNED',revision=1,origin=a,founding=cp(proof),binding=cp(binding),
   base={schema=1,kind='DEV_FOUNDATION_JOURNAL',owner=a.owner,cityID=a.cityID,x=a.x,y=a.y,token=token,
    foundationTurn=proof.turn,revision=0,health='TRACKING',specialization='NONE',potential=0},templatesCaptured=true})
 end
 function d.Acquire(c,proof,binding)
  assert(ready and not fault and root==nil and same(ref(c),proof.reference),'ACQUISITION_REFERENCE_CHANGED')
  local a=ref(c)
  save({schema=3,stage='ACTIVE',progression='UNASSIGNED',revision=1,origin=a,acquisition=cp(proof),binding=cp(binding),
   base={schema=1,kind='DEV_FOUNDATION_JOURNAL',owner=a.owner,cityID=a.cityID,x=a.x,y=a.y,token=c:GetProperty(M.Keys.TOKEN),
    foundationTurn=proof.turn,revision=0,health='TRACKING',specialization='NONE',potential=0},templatesCaptured=true})
 end
 function d.HoldCompletion(reason)
  if not ready or fault or not root or root.schema<2 or root.progression~='UNASSIGNED' or root.completionError or root.stage~='ACTIVE' or root.referenceInvalidated then return end
  local n=cp(root);n.completionError=reason;n.revision=n.revision+1;save(n)
 end
 function d.Complete(pid,c,e)
  if not root or root.schema<2 or root.progression~='UNASSIGNED' then return end
  if root.acquisition and root.acquisition.mode=='LEGACY_CLAIM' then return end
  -- Transfer reconstruction is not a new local completion. Await confirmed return.
  if root.stage~='ACTIVE' or root.referenceInvalidated then return end
  local r=active(pid,c);assert(same(e.reference,r.current or r.origin),'COMPLETION_REFERENCE_CHANGED')
  local n=cp(r);n.progression='SPECIALIZED';n.base.specialization=e.specialization;n.base.potential=1
  if e.specialization=='INDUSTRY' then n.templateLifecycle={version=1,state='UNINITIALIZED',reconcilePending=true}end
  n.base.first={districtID=e.districtID,type=e.type,turn=e.turn};n.base.revision=n.base.revision+1
  if n.current then n.currentFirst=cp(n.base.first)end
  n.revision=n.revision+1;save(n)
  if shared.OnPermanentCityWrite then shared.OnPermanentCityWrite(c,'CityProgressionStore.lua')end
 end
 -- Claim state belongs to the existing city record, not UI or a second property.
 function d.ClaimState(pid,c)
  local r=active(pid,c)
  if r.schema~=3 or r.acquisition.mode~='LEGACY_CLAIM' then return nil end
  return cp({token=r.base.token,reference=r.current or r.origin,set=r.acquisition.legacySet,
   eligible=r.progression=='UNASSIGNED',timer=r.claimTimer,receipt=r.claim,revision=r.revision})
 end
 function d.WriteClaimTimer(pid,c,old,value)
  local r=active(pid,c)
  assert(r.schema==3 and r.acquisition.mode=='LEGACY_CLAIM' and r.progression=='UNASSIGNED','CLAIM_INELIGIBLE')
  assert(same(r.claimTimer,old),'CLAIM_TIMER_STALE')
  if same(old,value) then return end
  local n=cp(r);n.claimTimer=cp(value);n.revision=n.revision+1;save(n)
 end
 function d.ClaimComplete(pid,c,e)
  local r=active(pid,c)
  if r.claim then return false end -- duplicate native completion/readback
  assert(r.schema==3 and r.acquisition.mode=='LEGACY_CLAIM' and r.progression=='UNASSIGNED','CLAIM_INELIGIBLE')
  assert(same(e.reference,r.current or r.origin) and e.token==r.base.token and r.acquisition.legacySet[e.kind]
   and e.project=='PROJECT_SPC_CLAIM_'..e.kind and e.turn==Game.GetCurrentGameTurn(),'CLAIM_PROOF_INVALID')
  assert(type(e.districtID)=='number' and type(e.type)=='string','CLAIM_DISTRICT_INVALID')
  local n=cp(r);n.progression='SPECIALIZED';n.base.specialization=e.kind;n.base.potential=1
  if e.kind=='INDUSTRY' then n.templateLifecycle={version=1,state='UNINITIALIZED',reconcilePending=true}end
  n.base.first={districtID=e.districtID,type=e.type,turn=e.turn};n.base.revision=n.base.revision+1
  if n.current then n.currentFirst=cp(n.base.first)end
  -- Receipt retains the historical record anchor; active requests use current reference.
  n.claim={version=1,token=e.token,reference=cp(r.origin),kind=e.kind,project=e.project,turn=e.turn}
  n.claimTimer=nil;n.revision=n.revision+1;save(n)
  if shared.OnPermanentCityWrite then shared.OnPermanentCityWrite(c,'ClaimProjects.lua')end
  return true
 end
 local function activate(c)
  assert(root.stage=='PREPARED' and same(source(c),root.source),'IMPORT_SOURCE_CHANGED')
  assert(P.IsTestPlayer(root.origin.owner),'IMPORT_PLAYER_CHANGED')
  local n=cp(root);n.stage='ACTIVE';n.source=nil;n.revision=n.revision+1;save(n)
 end
 function d.Import(pid,c)
  assert(not busy,'IMPORT_BUSY');busy=true
  local ok,err=pcall(function()
   assert(ready and not fault and c and P.IsTestPlayer(pid) and c:GetOwner()==pid,'SELECT_OWN_CITY')
   if root then assert(same(ref(c),root.current or root.origin) and root.stage=='ACTIVE','ONE_CITY_ONLY_OR_HELD');return end
   local s=source(c);assert(M.Preview(s).state=='LOCAL_CANDIDATE','IMPORT_LEGACY_INCOMPLETE')
   assert(kinds[s.values.JOURNAL.specialization],'FOUR_PROFESSIONS_ONLY')
   local f=shared.EffectiveFacts.Read(pid,c);assert(not f.investmentPending,'IMPORT_PENDING')
   save({schema=1,stage='PREPARED',revision=1,origin=cp(s.ref),base=cp(s.values.JOURNAL),
    investment=cp(s.values.INVEST),binding=cp(s.ledger),templates=cp(s.values.TEMPLATES),templatesCaptured=true,source=s})
   activate(c)
  end)
  busy=false
  if not ok then return '进度迁移暂停：'..tostring(err)..'\n未回退旧账本；请保留测试档。'end
  return d.Describe(pid,c)
 end
 function d.Describe(pid,c)
  if not ready or fault then return '进度保存暂停：'..tostring(fault or '尚未就绪')..'\n不会使用旧记录补写。'end
  if not root then return '尚未迁移。请选择完整的己方四专业城市，右键“迁移进度”。\n先保留独立的迁移前存档；本批只支持一城同Owner测试。'end
  if root.origin.owner~=pid then return '本记录不属于当前玩家。'end
  if root.stage~='ACTIVE' then return '永久进度保留，能力休眠；退出：'..d.exitStatus..(next(d.exitErrors) and '（暂停模块：'..(function()local t={};for n in pairs(d.exitErrors)do t[#t+1]=n end;table.sort(t);return table.concat(t,'、')end)()..'）' or '')..'\n恢复：'..((d.observation or ''):match('RETURN_[A-Z_]+') or '等待匹配夺回事件')..'；未确认时勿投资。'end
  c=c or CityManager.GetCityAt(root.origin.x,root.origin.y)
  local ok,f=pcall(shared.EffectiveFacts.Read,pid,c)
  if not ok then return '进度记录已保存；当前事实未确认：'..tostring(f)end
  if root.schema==3 then
   local names={RESEARCH='科研',CULTURE='文化',INDUSTRY='工业',COMMERCE='商业'};local list={}
   for _,k in ipairs({'RESEARCH','CULTURE','INDUSTRY','COMMERCE'})do if root.acquisition.legacySet[k]then list[#list+1]=names[k]end end
   local mode=root.acquisition.mode=='LEGACY_CLAIM' and '待完成对应认定项目' or '等待征服后的首个合格区域完成'
   if root.progression=='SPECIALIZED' then mode='专业已锁定：'..names[f.specialization]end
   return P.VERSION..' | 征服城市进度\n取得已确认 | '..mode..'\n冻结候选：'..(#list>0 and table.concat(list,'、') or '无')
    ..'\nPotential '..f.potential..' | ACTIVE '..tostring(f.active)..' | 投资 '..f.investmentCount..('\n认领：'..(shared.ClaimProjects and (shared.ClaimProjects.startupError or (shared.ClaimProjects.views[tostring(pid)..':'..c:GetID()] or {}).reason or shared.ClaimProjects.status) or '模块未初始化；请保留报告'))
    ..'\n独立记录已保存；候选不会随之后建设增加。'
  end
  if root.schema==2 then
   return P.VERSION..' | 新城进度\n来源：正常建城 | '..(root.progression=='UNASSIGNED' and '等待首个合格区域完成' or ('专业已锁定：'..f.specialization))
    ..'\nPotential '..f.potential..' | ACTIVE '..tostring(f.active)..' | 已完成投资 '..f.investmentCount
    ..'\n独立Game记录已保存；不从现有区域补造历史。'
  end
  return P.VERSION..' | 城市进度保存\n'..f.specialization..' | Potential '..f.potential..' | ACTIVE '..tostring(f.active)
   ..'\n已完成投资：'..f.investmentCount..' | 待完成事务：'..tostring(f.investmentPending)
   ..'\n来源：独立Game记录；旧City账本冻结。\nACTIVE依当前事实；Network等待当前路线；回滚使用迁移前存档。'
 end
 -- On-demand evidence only. No state writes, refresh, requests or effect application.
 function d.NativeDescribe(pid)
  local ok,out=pcall(function()
   if not root or not ready or fault or root.schema>=2 then return d.Describe(pid)end
   assert(pid==root.origin.owner and P.IsTestPlayer(pid),'E2_WRONG_PLAYER')
   local function label(r)return r and (tostring(r.owner)..'/'..tostring(r.cityID)..' @'..tostring(r.x)..','..tostring(r.y)) or 'NONE'end
   local city=CityManager.GetCityAt(root.origin.x,root.origin.y)
   local readable,live=pcall(ref,city)
   local tokenOK,token=pcall(function()return city:GetProperty(M.Keys.TOKEN)end)
   local receipts=0;for _ in pairs(root.investment and root.investment.investments or {})do receipts=receipts+1 end
   local done,total,checked,removed=0,0,0,0
   for name in pairs(exits)do total=total+1;if finished[name]then done=done+1 end end
   for _,v in pairs(exitReads)do checked=checked+v.checked;removed=removed+v.removed end
   local fOK,f=pcall(shared.EffectiveFacts.Read,pid,city)
   local net=shared.NetworkBridge;local b=net and net.players[pid];local ids={root.origin.cityID}
   if root.current then ids[#ids+1]=root.current.cityID end
   local source,receiver=false,false
   if b then for _,id in ipairs(ids)do
    source=source or (b.sources and b.sources[id]~=nil) or false
    for _,set in pairs(b.recipients or {})do receiver=receiver or set[id]~=nil end
   end end
   local input;local inputState='NO_CURRENT_INPUT'
   if readable and live.owner~=pid then inputState='FOREIGN_OWNER_NOT_QUERIED'
   elseif readable then
    local candidate=b and b.input and b.input.cities and b.input.cities[live.cityID]
    local good,reference=pcall(function()return SPCNetworkInput.Reference(city)end)
    if candidate and good and candidate.reference==reference then input=candidate;inputState='MATCHED'
    elseif candidate then inputState='REFERENCE_MISMATCH' end
   end
   local detail={}
   local errors={};for name in pairs(d.exitErrors)do errors[#errors+1]=name end;table.sort(errors)
   for _,name in ipairs(errors)do
    local reason=tostring(d.exitErrors[name]):gsub('[\r\n]+',' '):sub(1,160)
    detail[#detail+1]='退出失败 '..name..' ['..tostring(attempts[name])..'/3] '..reason
   end
   detail[#detail+1]='事件为本次加载后各类最后一次；原始参数，不自动认领：'
   for _,name in ipairs(eventNames)do
    local row=nativeEvents[name]
    if row then
     local args={};for i=1,math.min(6,row.argc)do args[i]=tostring(row[i])end
     detail[#detail+1]='#'..row.sequence..' T'..row.turn..' '..name..'('..table.concat(args,',')..') argc='..row.argc
    end
   end
   if eventSequence==0 then detail[#detail+1]='本次加载未收到上述事件'end
   if firstTransitionFault then
    local f=firstTransitionFault;local e=f.event or {};local args={}
    for i=1,(e.argc and math.min(6,e.argc) or 0)do args[#args+1]=tostring(e[i])end
    detail[#detail+1]='首次拒绝 '..f.reason..' | #'..tostring(e.sequence)..' T'..tostring(e.turn)..' '..f.name..'('..table.concat(args,',')..')'
   end
   local binding=not tokenOK and 'UNREADABLE' or token==nil and 'MISSING' or token==root.base.token and 'MATCH' or 'MISMATCH'
   local gate=root.referenceInvalidated and root.stage=='ACTIVE' and 'REFERENCE_REMOVED' or root.stage~='HELD_TRANSFER' and 'NOT_HELD' or not readable and 'CURRENT_REFERENCE_UNREADABLE'
    or live.owner~=root.origin.owner and 'STILL_FOREIGN' or d.returnRejection or 'WAIT_MATCHING_TRANSFER_EVENT'
   local function carrierCount(names)
    if not city then return 'UNKNOWN'end
    local good,n=pcall(function()local count=0;for _,name in ipairs(names)do
     local row=assert(P.Info('Buildings',name));local has=P.HasBuilding(city:GetBuildings(),row.Index)
     assert(type(has)=='boolean');if has then count=count+1 end
    end;return count end);return good and tostring(n) or 'UNKNOWN'
   end
   local housing,gpp={},{};for i=0,8 do housing[#housing+1]='BUILDING_SPC_DEV_LV2_HOUSING_'..i end
   for i=0,7 do gpp[#gpp+1]='BUILDING_SPC_DEV_GPP_RESEARCH_'..i end
   local result=table.concat({P.VERSION..' | E2往返 | T'..Game.GetCurrentGameTurn()..' | '..root.stage,
    '原引用 '..label(root.origin)..' | record rev '..root.revision,
    '原凭据 '..root.base.token..' | 当前匹配 '..binding..' | 恢复依据 '..tostring(root.returnEvidence or '尚未确认'),
    '当前 '..(readable and label(live) or 'UNKNOWN')..' | token '..(tokenOK and tostring(token) or 'UNKNOWN'),
    '永久 '..root.base.specialization..' | Potential '..(1+receipts)..' | 投资 '..receipts,
    '当前ACTIVE '..(fOK and tostring(f.active)..' / '..tostring(f.activeStatus) or '未激活/UNKNOWN'),
    '失城确认 '..(root.loss and label(root.loss.target) or root.lastLoss and ('历史 '..label(root.lastLoss.target)) or 'NONE'),
    '退出 '..d.exitStatus..' | 完成 '..done..'/'..total..' | 核验ID '..checked..' / 移除 '..removed,
    '最近转移 '..(d.lastTransfer or '本次加载未收到'),
    '夺回 '..(root.current and root.stage=='ACTIVE' and not root.referenceInvalidated and 'ACCEPTED' or gate)..' | 最近候选 '..(d.returnCandidate or 'NONE'),
    '转移链 '..(transitionFault or (transition and (transition.initialized and 'READY' or 'INCOMPLETE') or 'NONE'))..' | CityBuilt '..(foundation and (conquest and '待核对征服' or '缺少征服佐证') or 'NONE'),
    '科研实存carrier：支持 '..carrierCount({'BUILDING_SPC_DEV_RESEARCH_SUPPORT'})..' / 住房 '..carrierCount(housing)..' / GPP '..carrierCount(gpp),
    'Network '..(b and b.validity or 'UNKNOWN')..' | epoch '..tostring(net and net.epoch)..' / input '..tostring(b and b.inputRevision)..' / derive '..tostring(b and b.derivedRevision),
    '旧/现本城 source '..tostring(source)..' / receiver '..tostring(receiver)..' | routes '..tostring(b and b.routes and #b.routes or 'UNKNOWN'),
    'Network当前引用 '..inputState..' | '..tostring(input and input.reference or 'NONE')..' | ACTIVE '..tostring(input and input.active or 'NONE'),
    table.concat(detail,'\n'),
    '载体读数≠引擎收益验证；请配合城市收益截图。'},'\n')
   return result
  end)
  local report=ok and out or ('E2诊断 UNKNOWN：'..tostring(out))
  print('[SPC][E2_NATIVE] '..report);return report
 end
 local function restore()
  local ok,err=pcall(function()
   root=storage.Read();if root then validate(root)end;ready=true
  end)
  if not ok then fault=tostring(err);ready=false end
 end
 function d.Ready()return ready and not fault end
 function d.Status()return cp(d and {exitStatus=d.exitStatus,exitErrors=d.exitErrors,observation=d.observation,
  returnRejection=d.returnRejection,returnCandidate=d.returnCandidate,lastTransfer=d.lastTransfer})end
 restore() -- before Binding/Journal/Flow/Investment register load callbacks
 -- No absence/failed getter is confirmation. A matched native ownership event is required.
 function d.IsExitTarget(c,loss)
  if not ready or fault or not root or not root.loss or not loss or not same(loss,root.loss) then return false end
  local ok,r=pcall(ref,c)
  return ok and same(r,loss.target) and r.owner~=root.origin.owner
 end
 function d.RegisterExit(name,fn)
  assert(type(fn)=='function' and not exits[name],'EXIT_REGISTRATION_CONFLICT');exits[name]=fn
 end
 -- Only module-supplied exact IDs: no DB/catalog enumeration or prefix matching.
 function d.RemoveOwned(c,loss,names)
  assert(d.IsExitTarget(c,loss),'EXIT_NOT_CONFIRMED')
  local rows,seen={},{};local buildings=c:GetBuildings()
  for _,name in ipairs(names) do
   assert(not seen[name],'EXIT_DUPLICATE_ID');seen[name]=true
   local row=assert(P.Info('Buildings',name),'EXIT_DEFINITION_MISSING '..name)
   assert(row.InternalOnly==true or row.InternalOnly==1,'EXIT_NON_INTERNAL_BUILDING')
   local has=P.HasBuilding(buildings,row.Index);assert(type(has)=='boolean','EXIT_CARRIER_UNKNOWN')
   rows[#rows+1]={id=row.Index,has=has}
  end
  local found=0;for _,r in ipairs(rows)do if r.has then found=found+1 end end
  for _,r in ipairs(rows) do if r.has then
   assert(d.IsExitTarget(c,loss),'EXIT_REFERENCE_CHANGED')
   P.RemoveBuilding(buildings,r.id)
   assert(P.HasBuilding(buildings,r.id)==false,'EXIT_REMOVE_UNCONFIRMED')
  end end
  if runningExit then exitReads[runningExit]={checked=#rows,removed=found}end
 end
 function d.ExitConfirmed()
  if exitBusy or not ready or fault or not root or not root.loss then return end
  local ok,c=pcall(CityManager.GetCityAt,root.origin.x,root.origin.y)
  if not ok or not c or not d.IsExitTarget(c,root.loss) then d.exitStatus='TARGET_UNAVAILABLE';return end
  foreignSeen=true
  exitBusy=true;local names={};for name in pairs(exits)do names[#names+1]=name end
  table.sort(names,function(a,b)if a=='NetworkBridge' then return b~='NetworkBridge' end;if b=='NetworkBridge' then return false end;return a<b end)
  for _,name in ipairs(names)do if not finished[name] and (attempts[name] or 0)<3 then
   attempts[name]=(attempts[name] or 0)+1
   runningExit=name;local good,err=pcall(exits[name],c,cp(root.loss));runningExit=nil
   if good then finished[name]=true;d.exitErrors[name]=nil else d.exitErrors[name]=tostring(err)end
  end end
  d.exitStatus=#names>0 and 'WITHDRAWN' or 'NO_EXIT_MODULES'
  for _,name in ipairs(names)do if not finished[name] then d.exitStatus='PARTIAL_HELD' end end
  exitBusy=false
 end
 local function recapture(c,current,newOwner,newID,oldOwner)
  if not root.loss or root.stage~='HELD_TRANSFER' or newOwner~=root.origin.owner
   or oldOwner~=root.loss.target.owner or newID~=current.cityID or current.owner~=newOwner then return false end
  d.returnCandidate=current.owner..'/'..current.cityID..' from '..tostring(oldOwner)
  d.returnRejection=nil -- latest matched attempt; diagnostics only
  assert(P.IsTestPlayer(newOwner),'RETURN_PLAYER_UNCONFIRMED')
  local token=c:GetProperty(M.Keys.TOKEN);local proof
  if token~=root.base.token then
   assert(token==nil,'RETURN_BINDING_CONFLICT')
   assert(not transitionFault,transitionFault)
   assert(foreignSeen and transition,'RETURN_CHAIN_MISSING')
   proof=cp(transition);proof.transferred=eventSequence
   if foundation then
    assert(conquest,'RETURN_NEW_FOUNDATION')
    proof.version=2;proof.conquest=cp(conquest);proof.foundation=cp(foundation)
    assert(validTransition(proof,root.loss,current),'RETURN_FOUNDATION_CONFLICT')
   elseif conquest then
    assert(conquest.turn==proof.turn and conquest.fromOwner==root.loss.target.owner and same(conquest.to,current)
     and conquest.sequence<proof.removed,'RETURN_CONQUEST_CONFLICT')
   end
   assert(proof.turn==Game.GetCurrentGameTurn() and validTransition(proof,root.loss,current),'RETURN_CHAIN_INCOMPLETE')
  end
  local count=0;for name in pairs(exits)do count=count+1;assert(finished[name],'RETURN_WITHDRAWAL_UNCONFIRMED')end
  assert(count>0,'RETURN_WITHDRAWAL_UNCONFIRMED')
  assert(not root.investment or root.investment.pending==nil,'RETURN_PENDING_INVESTMENT')
  -- Rebind the current district reference, never invent new historical completion.
  local first
  if root.progression~='UNASSIGNED' then
  for _,district in Players[newOwner]:GetDistricts():Members()do
   local city=district:GetCity();local row=P.Info('Districts',district:GetType())
   if city and same(ref(city),current) and row and row.DistrictType==root.base.first.type and district:IsComplete() then
    assert(not first,'RETURN_DISTRICT_AMBIGUOUS');first=cp(root.base.first);first.districtID=district:GetID()
   end
  end
  assert(first,'RETURN_DISTRICT_UNAVAILABLE')
  end -- P0 has no historical professional district to rebind.
  local n=cp(root)
  if n.base.specialization=='INDUSTRY' then
   -- Preserve reliable city experience; current eligible buildings are unioned
   -- by Standardization only after the authoritative return is committed.
   if n.templatesCaptured and n.templates then
    assert(shared.Standardization and shared.Standardization.ValidateRetained,'RETURN_TEMPLATE_VALIDATOR_UNAVAILABLE')
    shared.Standardization.ValidateRetained(c,n.templates)
   end -- missing pre-loss history holds Standardization reads, not Identity/Potential
   if n.templateLifecycle then n.templateLifecycle.reconcilePending=true end
  end
  -- Reset samples/quotes before making facts available. No callback applies yields.
  for _,fn in pairs(returns)do fn(root.origin.owner,c)end
  n.lastLoss=n.loss;n.loss=nil;n.stage='ACTIVE';n.current=current;n.currentFirst=first;n.returnEvidence=proof and 'NATIVE_TRANSITION_V1' or 'CityTransfered+original_binding';n.returnProof=proof;n.referenceInvalidated=nil
  n.revision=n.revision+1;save(n)
  finished={};attempts={};transition=nil;transitionFault=nil;firstTransitionFault=nil;conquest=nil;foundation=nil;foreignSeen=false;d.exitErrors={};d.exitStatus='NOT_CONFIRMED';d.returnStatus='CONFIRMED_CURRENT_FACTS_REQUIRED'
  return true
 end
 local function reconcile(newOwner,newID,oldOwner)
  if not ready or fault or not root then return end
  if newOwner~=nil then d.lastTransfer=tostring(oldOwner)..' → '..tostring(newOwner)..'/'..tostring(newID)end
  local ok,err=pcall(function()
   local c=CityManager.GetCityAt(root.origin.x,root.origin.y)
   if not c then d.observation='UNKNOWN_CITY';return end
   local current=ref(c)
   if type(current.owner)~='number' or current.owner<0 or type(current.cityID)~='number' then d.observation='UNKNOWN_OWNER';return end
   if recapture(c,current,newOwner,newID,oldOwner) then return
   elseif same(current,root.origin) and root.stage=='PREPARED' then activate(c)
   elseif not root.loss and current.owner~=root.origin.owner and oldOwner==root.origin.owner
    and newOwner==current.owner and newID==current.cityID then
    local n=cp(root);n.stage='HELD_TRANSFER';n.source=nil;n.claimTimer=nil;n.revision=n.revision+1
    if n.researchTradition then n.researchTradition.state='OWNER_POLICY_UNRESOLVED' end
    n.loss={origin=cp(root.origin),target=current,evidence='CityTransfered+live_reference'};save(n)
    finished={};attempts={};d.exitErrors={};transition=nil;transitionFault=nil;firstTransitionFault=nil;conquest=nil;foundation=nil;foreignSeen=false
   end
   d.observation='READABLE'
  end)
  if not ok then d.observation='UNKNOWN: '..tostring(err);d.returnRejection=tostring(err):match('RETURN_[A-Z_]+') or d.returnRejection end
  d.ExitConfirmed()
 end
 -- Manager forwards bounded native events; each record retains its own state.
 function d.Handle(name,...)
  if name=='LoadScreenClose' then reconcile();return end
  if not ready or fault or not root then return end
  local owner,id,x,y=...
  local relevant=false
  if name=='CityConquered' then local _,_,_,cx,cy=...;relevant=cx==root.origin.x and cy==root.origin.y
  elseif name=='CityTransfered' then
   local ok,c=pcall(CityManager.GetCityAt,root.origin.x,root.origin.y)
   if ok and c then local good,r=pcall(ref,c);relevant=good and r.owner==owner and r.cityID==id end
  elseif name=='CityRemovedFromMap' then
   for _,r in ipairs({root.current or root.origin,root.loss and root.loss.target or {},transition and transition.to or {}})do
    if r.owner==owner and r.cityID==id then relevant=true end
   end
  else relevant=x==root.origin.x and y==root.origin.y end
  if not relevant then return end
  pcall(observe,name,...)
  if name=='CityTransfered' then reconcile(...)
  elseif name=='CityConquered' then
   if not pcall(trackConquest,...) then transitionFault='RETURN_CHAIN_READ_FAILED'end
   rememberFault(name)
  else trackSafely(name,...);reconcile()end
 end
 return d
end

-- Production new-game authority. Historical adapter is explicit and test-only; no Claim.
function SPCCityProgressionStore.Start(P,shared,legacyTest)
 local M=SPCCityIdentityRead;local cp=M.Copy;local KEY=SPCCityProgressionStore.KEY
 local store={UsesNewAuthority=not legacyTest};shared.CityProgressionStore=store
 local envelope,raw,fault,writing;local workers={};local exits,returns={},{}
 local modern=not legacyTest;local index,positions,capacity;local initialized=false
 local INDEX=SPCCityProgressionStore.INDEX;local PREFIX=SPCCityProgressionStore.RECORD
 local initializeNew
 local function same(a,b)
  if type(a)~=type(b)then return false end;if type(a)~='table'then return a==b end
  for k,v in pairs(a)do if not same(v,b[k])then return false end end
  for k in pairs(b)do if a[k]==nil then return false end end;return true
 end
 local function check()assert(not fault,fault or 'STORE_COLLECTION_HELD')end
 local function count()if modern and index then return index.counter end;local n=0;for _ in pairs(envelope.records)do n=n+1 end;return n end
 function store.RecordCount()return count()end
 local function validateCollection(v)
  assert(type(v)=='table' and v.schema==2 and type(v.records)=='table' and type(v.revision)=='number'
   and v.revision>=0 and v.revision%1==0,'STORE_COLLECTION_SCHEMA')
  local positions,references={},{};local n=0
  for token,r in pairs(v.records)do
   n=n+1;assert(n<=2,'TWO_CITY_TEST_LIMIT')
   assert(type(token)=='string' and type(r)=='table' and type(r.base)=='table' and token==r.base.token
    and type(r.origin)=='table' and type(r.origin.x)=='number' and type(r.origin.y)=='number','STORE_RECORD_KEY')
   local position=r.origin.x..':'..r.origin.y
   assert(not positions[position],'STORE_LOCATION_COLLISION');positions[position]=true
   local current=r.loss and r.loss.target or r.current or r.origin
   assert(type(current)=='table' and type(current.owner)=='number' and type(current.cityID)=='number','STORE_CURRENT_REFERENCE')
   local reference=current.owner..':'..current.cityID
   assert(not references[reference],'STORE_REFERENCE_COLLISION');references[reference]=true
  end
 end
 local function make(token,admitting)
  local storage={}
  storage.Check=check
  function storage.Read()
   check()
   if modern and not admitting then assert(envelope.records[token],'REGISTRATION_INCOMPLETE')end
   return cp(envelope.records[token])
  end
  function storage.Write(old,value)
   check();assert(not writing,'STORE_COLLECTION_BUSY');assert(same(envelope.records[token],old),'STORE_STALE')
   assert(value.base.token==token,'STORE_TOKEN_CHANGED')
   if modern then
    local key=PREFIX..token;local before=envelope.records[token]
    assert(same(Game:GetProperty(key),before),'STORE_RECORD_STALE')
    -- Exact current-reference uniqueness; no collection clone/property rewrite.
    local current=value.loss and value.loss.target or value.current or value.origin
    for other,r in pairs(envelope.records)do if other~=token then
     local v=r.loss and r.loss.target or r.current or r.origin
     assert(current.owner~=v.owner or current.cityID~=v.cityID,'STORE_REFERENCE_COLLISION')
    end end
    writing=true
    local ok,err=pcall(function()
     P.SetProperty(Game,key,cp(value));assert(same(Game:GetProperty(key),value),'STORE_WRITE_UNCONFIRMED')
    end)
    writing=false
    -- Worker holds its own failed write; unrelated records remain usable.
    assert(ok,err);envelope.records[token]=cp(value);return
   end
   local nextValue=cp(envelope);nextValue.records[token]=cp(value);nextValue.revision=nextValue.revision+1
   validateCollection(nextValue)
   assert(same(Game:GetProperty(KEY),raw),'STORE_COLLECTION_STALE')
   writing=true;envelope=nextValue -- old-writer guards see the new record before engine callbacks
   local ok,err=pcall(function()
    P.SetProperty(Game,KEY,cp(nextValue))
    assert(same(Game:GetProperty(KEY),nextValue),'STORE_WRITE_UNCONFIRMED')
   end)
   writing=false
   if not ok then fault=tostring(err);error(fault)end
   raw=cp(nextValue)
  end
  local w=CreateProgressionRecord(P,shared,storage)
  workers[token]=w
  for name,fn in pairs(exits)do w.RegisterExit(name,fn)end
  for name,fn in pairs(returns)do w.RegisterReturn(name,fn)end
  return w
 end
 local function int(v)return type(v)=='number' and v>=0 and v<1000000000 and v%1==0 end
 local function copyIndex(v)
  assert(type(v)=='table' and v.schema==3 and int(v.counter) and v.counter<=capacity and type(v.entries)=='table','UNSUPPORTED_SAVE_SCHEMA')
  local out={schema=3,counter=v.counter,entries={}};local seen={};local n=0
  for token,a in pairs(v.entries)do
   n=n+1;assert(n<=capacity,'INDEX_LIMIT')
   assert(type(token)=='string' and type(a)=='table' and int(a.owner) and int(a.cityID) and int(a.x) and int(a.y)
    and int(a.serial) and a.serial>0 and a.serial<=v.counter and token=='DEV-B013-P'..a.owner..'-'..a.serial
    and not seen[a.serial],'INDEX_ENTRY')
   seen[a.serial]=true;out.entries[token]=cp(a)
  end
  assert(n==v.counter,'INDEX_INCOMPLETE');return out
 end
 local function loadIndex(v)
  index=copyIndex(v);positions={};envelope={records={}}
  for token,a in pairs(index.entries)do
   local pos=a.x..':'..a.y;assert(not positions[pos],'STORE_LOCATION_COLLISION');positions[pos]=token
   local good,row=pcall(function()
    local value=cp(Game:GetProperty(PREFIX..token))
    if value then assert((value.schema==2 or value.schema==3) and type(value.binding)=='table' and value.binding.schema==2 and same(value.origin,{owner=a.owner,cityID=a.cityID,x=a.x,y=a.y}) and type(value.base)=='table' and value.base.token==token,'INDEX_RECORD_CONFLICT')end
    return value
   end)
   if good then envelope.records[token]=row end
   -- Bad/missing city record gets a held worker, never legacy or a reset.
   local w=make(token)
   if not good then envelope.records[token]=nil end
  end
  local refs={}
  for _,row in pairs(envelope.records)do
   local a=row.loss and row.loss.target or row.current or row.origin
   local key=a.owner..':'..a.cityID;assert(not refs[key],'STORE_REFERENCE_COLLISION');refs[key]=true
  end
  initialized=true
 end
 if modern then
  local ok,err=pcall(function()
   local width,height=Map.GetGridSize();assert(int(width) and width>0 and int(height) and height>0,'MAP_SIZE_UNAVAILABLE')
   capacity=width*height;assert(capacity<1000000000,'MAP_SIZE_INVALID')
   envelope={records={}};positions={}
   local v=Game:GetProperty(INDEX)
   if v~=nil then loadIndex(v)
   elseif Game:GetProperty(KEY)~=nil then error('OLD_SAVE_UNSUPPORTED_START_NEW_GAME')end
  end)
  if not ok then fault=tostring(err)end
  initializeNew=function()
   if fault or initialized then return end
   local ok,err=pcall(function()
    -- Supported games enable the Mod from creation. No mid-game/old-save adoption.
    -- Existing index loads above; absent index requires the pristine start state below.
    assert(Game.GetCurrentGameTurn()==GameConfiguration.GetStartTurn(),'NOT_NEW_GAME_START')
    local humans=0
    for pid,player in pairs(Players)do
     assert(Game:GetProperty('SPC_DEV_BINDING_B013_P'..pid)==nil,'OLD_BINDING_SAVE_UNSUPPORTED')
     if P.IsTestPlayer(pid)then
      humans=humans+1
      for _ in player:GetCities():Members()do error('EXISTING_CITY_SAVE_UNSUPPORTED')end
     end
    end
    assert(humans==1,'LOCAL_HUMAN_UNCONFIRMED')
    assert(Game:GetProperty(INDEX)==nil and Game:GetProperty(KEY)==nil,'SAVE_AUTHORITY_CHANGED')
    local value={schema=3,counter=0,entries={}}
    P.SetProperty(Game,INDEX,value);assert(same(Game:GetProperty(INDEX),value),'INDEX_WRITE_UNCONFIRMED')
    loadIndex(value)
   end)
   if not ok then fault=tostring(err)end
  end
 else
 local ok,err=pcall(function()
  raw=cp(Game:GetProperty(KEY))
  if raw==nil then envelope={schema=2,revision=0,records={}}
  elseif type(raw)=='table' and raw.schema==1 then
   assert(raw.base and type(raw.base.token)=='string','STORE_LEGACY_KEY')
   -- Lossless read adapter; promote the whole value at the next actual write.
   envelope={schema=2,revision=0,records={[raw.base.token]=cp(raw)}}
  else envelope=cp(raw)end
  validateCollection(envelope)
  for token in pairs(envelope.records)do local w=make(token);assert(w.Ready(),'STORE_RECORD_INVALID')end
 end)
 if not ok then fault=tostring(err)end
 end
 local function find(c)
  check();if not c then return nil end
  if modern then local token=positions[c:GetX()..':'..c:GetY()];return token and workers[token]end
  local found
  for _,w in pairs(workers)do if w.Owns(c)then assert(not found,'STORE_ROUTE_AMBIGUOUS');found=w end end
  return found
 end
 local function requireCity(c)return assert(find(c),'CITY_NOT_REGISTERED')end
 function store.Owns(c)
  if fault then return true end -- unreadable collection cannot safely authorize any legacy fallback
  return find(c)~=nil
 end
 function store.IsRecaptured(c)local w=find(c);return w and w.IsRecaptured(c) or false end
 function store.ClaimState(pid,c)return requireCity(c).ClaimState(pid,c)end
 function store.WriteClaimTimer(pid,c,old,value)return requireCity(c).WriteClaimTimer(pid,c,old,value)end
 function store.ClaimComplete(pid,c,e)return requireCity(c).ClaimComplete(pid,c,e)end
 function store.Base(pid,c)return requireCity(c).Base(pid,c)end
 function store.Investment(pid,c)return requireCity(c).Investment(pid,c)end
 function store.WriteInvestment(pid,c,old,value)return requireCity(c).WriteInvestment(pid,c,old,value)end
 function store.ReadTradition(pid,c)return requireCity(c).ReadTradition(pid,c)end
 function store.VisitTradition(pid,fn)
  check();if not P.IsTestPlayer(pid)then return end
  local firstError
  for _,w in pairs(workers)do local ok,err=pcall(w.VisitTradition,pid,fn);if not ok then firstError=firstError or err end end
  assert(not firstError,firstError) -- an unreadable city must not prevent other records from updating
 end
 local function traditionTick(pid)
  if fault or not P.IsTestPlayer(pid)then return end
  local turn=Game.GetCurrentGameTurn()
  -- Existing registered records only: no world/city/building scan or fact packet.
  for _,w in pairs(workers)do w.TickTradition(pid,turn)end
 end
 local turnEvent=P.Field(Events,'PlayerTurnActivated')
 if turnEvent and turnEvent.Add then turnEvent.Add(traditionTick)end
 local loadEvent=P.Field(Events,'LoadScreenClose')
 if loadEvent and loadEvent.Add then loadEvent.Add(function()
  for pid in pairs(Players)do if P.IsTestPlayer(pid)then traditionTick(pid)end end
 end)end
 function store.ReadTemplates(c)return requireCity(c).ReadTemplates(c)end
 function store.WriteTemplates(c,old,value)return requireCity(c).WriteTemplates(c,old,value)end
 function store.IsExitTarget(c,loss)
  if fault then return false end;local w=find(c);return w and w.IsExitTarget(c,loss) or false
 end
 function store.RemoveOwned(c,loss,names)return requireCity(c).RemoveOwned(c,loss,names)end
 function store.RegisterExit(name,fn)
  assert(type(fn)=='function' and not exits[name],'EXIT_REGISTRATION_CONFLICT');exits[name]=fn
  for _,w in pairs(workers)do w.RegisterExit(name,fn)end
 end
 function store.RegisterReturn(name,fn)
  assert(type(fn)=='function' and not returns[name],'RETURN_REGISTRATION_CONFLICT');returns[name]=fn
  for _,w in pairs(workers)do w.RegisterReturn(name,fn)end
 end
 function store.ExitConfirmed()
  if fault then return end;for _,w in pairs(workers)do w.ExitConfirmed()end
 end
 -- Read-only, copied per-city diagnostic status; never expose mutable worker authority.
 function store.Status(c)
  local ok,w=pcall(find,c);if not ok then return {fault=tostring(w)}end
  return w and w.Status() or {unregistered=true}
 end
 function store.FailureReport()
  if not fault then return nil end
  local first=tostring(fault):match('^[^\r\n]+') or ''
  local message=first:match('.*:%d+: (.*)') or first
  local code=message:match('^([A-Z][A-Z_]+)') or 'INITIALIZATION_FAILED'
  local reason='初始化或保存校验未通过；只支持从开局启用本Mod的测试局。'
  return P.VERSION..' | 专业进度暂停\n'..reason..'\n原因：'..code
   ..'\n请停止投资并保留此报告；不会回退旧账本。'
 end
 function store.Describe(pid,c)
  if fault then return store.FailureReport() end
  if not c then return '请选择一座城市；不会默认读取另一城。'end
  local w=find(c)
  if not w and modern then return '所选城市尚无已确认的新局记录；不会读取旧账本或自动认领。\n正常建城须收到确认事件；征服须确认完整事件与无专业历史，不能自动认领。'end
  if not w then return '所选城市未登记；仍使用旧保存路径。右键迁移进度可登记完整的己方专业城。\n本批最多显式登记两城；先保留转换前存档。'end
  return w.Describe(pid,c)..'\n已登记：'..count()..(modern and ' | 所选城 ' or '/2 | 所选城 ')..c:GetOwner()..'/'..c:GetID()
 end
 function store.NativeDescribe(pid,c)
  if fault or not c then return store.Describe(pid,c)end
  local w=find(c);if not w then return store.Describe(pid,c)end
  return w.NativeDescribe(pid)..'\n所选城 '..c:GetOwner()..'/'..c:GetID()..' | 已登记 '..count()..(modern and '' or '/2')
 end
 function store.Import(pid,c)
  if modern then return '本版本只支持新测试局；旧进度迁移入口已关闭。请左键查看当前进度。'end
  local ok,out=pcall(function()
   check();assert(not writing and c and P.IsTestPlayer(pid) and c:GetOwner()==pid,'SELECT_OWN_CITY')
   local w=find(c)
   if not w then
    assert(count()<2,'TWO_CITY_TEST_LIMIT')
    local token=c:GetProperty(M.Keys.TOKEN)
    assert(type(token)=='string' and not workers[token] and not envelope.records[token],'IMPORT_TOKEN_COLLISION')
    w=make(token)
   end
   local result=w.Import(pid,c)
   -- A rejected pre-write import must not consume a slot or retain a phantom worker.
   for token,v in pairs(workers)do if v==w and not envelope.records[token] and not fault then workers[token]=nil end end
   return result
  end)
  if not ok then return '进度迁移暂停：'..tostring(out)..'；保留测试档。'end
  return out
 end
 -- At most four scalar candidates and eight ordered completion notifications each.
 -- No Publish/Playback/timer gate, no unit lookup, no load-time district inference.
 local pending={};local eventSerial=0;local freshReady=false;local freshOverflow=false;local hooks={}
 local LIMIT,COMPLETIONS=modern and (capacity or 0) or 4,8
 local function integer(v)return type(v)=='number' and v>=0 and v<1000000000 and v%1==0 end
 local foundReason=P.Field(EventSubTypes,'FOUND_CITY')
 if type(foundReason)~='number' or foundReason~=foundReason or math.abs(foundReason)==math.huge then foundReason=nil end
 local function reference(c)return {owner=c:GetOwner(),cityID=c:GetID(),x=c:GetX(),y=c:GetY()}end
 local function at(x,y)for _,q in ipairs(pending)do if q.reference.x==x and q.reference.y==y then return q end end end
 local function legacyPresent(c)
  for _,key in pairs(M.Keys)do if c:GetProperty(key)~=nil then return true end end
  return false
 end
 function store.BlocksLegacy(c)
  if modern then return true end -- no legacy writer, even for unsupported/unregistered cities
  if store.Owns(c)then return true end
  if not c then return false end
  return at(c:GetX(),c:GetY())~=nil or (freshOverflow and P.IsTestPlayer(c:GetOwner()) and not legacyPresent(c))
 end
 function store.CanAllocateFoundation(c)
  local q=at(c:GetX(),c:GetY())
  return q and q.committing and not q.error and same(q.reference,reference(c)) and not store.Owns(c)
 end
 local function candidate(owner,id,x,y)
  if not freshReady or not P.IsTestPlayer(owner) or not integer(x) or not integer(y) then return end
  local q=at(x,y)
  if q then
   if q.turn~=Game.GetCurrentGameTurn() then q.error='FOUNDATION_CROSS_TURN'
   elseif q.reference.owner~=owner or (id~=nil and q.reference.cityID~=nil and q.reference.cityID~=id) then q.error='FOUNDATION_REFERENCE_CONFLICT'
   elseif id~=nil then q.reference.cityID=id end
   return q
  end
  local c=CityManager.GetCityAt(x,y)
  -- Retained historical locations, including HELD records, never enroll again.
  if c and (store.Owns(c) or legacyPresent(c)) then return end
  for _,r in pairs(envelope.records)do if r.origin.x==x and r.origin.y==y then return end end
  if not modern and count()>=2 then return end -- historical test adapter only
  if #pending>=LIMIT then freshOverflow=true;return end
  q={reference={owner=owner,cityID=id,x=x,y=y},turn=Game.GetCurrentGameTurn(),completions={}}
  pending[#pending+1]=q
  if not integer(q.turn) then q.error='FOUNDATION_TURN_UNAVAILABLE' end
  return q
 end
 local function family(name)
  local rows=assert(P.Rows('DistrictReplaces'),'COMPLETION_REPLACEMENTS_UNAVAILABLE');local seen={}
  for i=1,32 do
   assert(P.Info('Districts',name) and not seen[name],'COMPLETION_MAPPING_INVALID');seen[name]=true
   local kind=P.Families[name]
   if kind then return ({RESEARCH=true,CULTURE=true,INDUSTRY=true,COMMERCE=true})[kind] and kind or nil end
   local parent
   for _,r in ipairs(rows)do if r.CivUniqueDistrictType==name then
    assert(not parent or parent==r.ReplacesDistrictType,'COMPLETION_MAPPING_CONFLICT');parent=r.ReplacesDistrictType
   end end
   if not parent then return end;name=parent
  end
  error('COMPLETION_MAPPING_LIMIT')
 end
 local function completion(pid,index,x,y)
  local district=assert(CityManager.GetDistrictAt(x,y),'COMPLETION_DISTRICT_UNAVAILABLE')
  local c=assert(district:GetCity(),'COMPLETION_CITY_UNAVAILABLE')
  assert(c:GetOwner()==pid and district:GetOwner()==pid and district:GetType()==index,'COMPLETION_REFERENCE_CHANGED')
  local info=assert(P.Info('Districts',index),'COMPLETION_TYPE_UNAVAILABLE')
  local kind=family(info.DistrictType)
  if not kind or district:IsComplete()~=true then return c end
  local id=district:GetID();assert(integer(id),'COMPLETION_ID_UNAVAILABLE')
  return c,{reference=reference(c),specialization=kind,type=info.DistrictType,districtID=id,turn=Game.GetCurrentGameTurn()}
 end
 local function admit(q)
  if not q or q.error or q.committing then return end
  if q.conquest then if not q.transferred then return end
  elseif not q.initialized or not q.found then return end
  q.committing=true
  local ok,err=pcall(function()
   check();assert(modern or count()<2,'TWO_CITY_TEST_LIMIT')
   assert(hooks.CityInitialized and hooks.OnDistrictConstructed and hooks.LoadScreenClose,'FOUNDATION_HOOK_UNAVAILABLE')
   if not q.conquest then assert(foundReason~=nil and hooks.UnitActivate,'FOUNDATION_HOOK_UNAVAILABLE')end
   assert(q.turn==Game.GetCurrentGameTurn(),'FOUNDATION_CROSS_TURN')
   local c=assert(CityManager.GetCityAt(q.reference.x,q.reference.y),'FOUNDATION_CITY_UNAVAILABLE')
   assert(P.IsTestPlayer(q.reference.owner) and same(reference(c),q.reference),'FOUNDATION_REFERENCE_CHANGED')
   assert(not store.Owns(c) and not legacyPresent(c),'FOUNDATION_EXISTING_HISTORY')
   local acquisition
   if q.conquest then
    assert(modern and hooks.CityConquered and hooks.CityAddedToMap and hooks.CityTransfered,'ACQUISITION_HOOK_UNAVAILABLE')
    assert(not q.found and q.added and q.initSequence and q.conquest.sequence<q.added and q.added<q.initSequence and q.initSequence<q.transferred,'ACQUISITION_ORDER')
    local old=assert(Players[q.conquest.oldOwner],'ACQUISITION_OLD_OWNER_UNAVAILABLE')
    local major=old:IsMajor();local minor=false
    assert(type(major)=='boolean','ACQUISITION_SOURCE_KIND_UNKNOWN')
    if not major then
     -- IsMinor is not a proven Gameplay interface. Resolve the original owner's
     -- configured civilization against the authoritative gameplay database instead.
     local config=PlayerConfigurations and PlayerConfigurations[q.conquest.oldOwner]
     local ok,civ=P.Call(config,'GetCivilizationTypeName')
     assert(ok and type(civ)=='string' and civ~='','ACQUISITION_SOURCE_CIV_UNAVAILABLE')
     local row=P.Info('Civilizations',civ)
     assert(row and type(row.StartingCivilizationLevelType)=='string','ACQUISITION_SOURCE_LEVEL_UNAVAILABLE')
     minor=row.StartingCivilizationLevelType=='CIVILIZATION_LEVEL_CITY_STATE'
    end
    assert((major==true or minor==true) and old:IsHuman()==false and not P.IsTestPlayer(q.conquest.oldOwner),'ACQUISITION_AI_MAJOR_OR_CITY_STATE_REQUIRED')
    local set={};local seen={}
    q.stage='区域快照读取'
    local districts=assert(c:GetDistricts(),'ACQUISITION_DISTRICTS_UNAVAILABLE')
    local n=districts:GetNumDistricts()
    assert(integer(n) and n>=0,'ACQUISITION_DISTRICT_COUNT_UNAVAILABLE')
    for i=0,n-1 do
     local district=assert(districts:GetDistrictByIndex(i),'ACQUISITION_DISTRICT_ENTRY_UNAVAILABLE')
     assert(same(reference(district:GetCity()),q.reference) and district:GetOwner()==q.reference.owner,'ACQUISITION_DISTRICT_REFERENCE')
     local id=district:GetID();assert(integer(id) and not seen[id],'ACQUISITION_DISTRICT_ID');seen[id]=true
     local complete=district:IsComplete();assert(type(complete)=='boolean','ACQUISITION_COMPLETENESS_UNKNOWN')
     local row=assert(P.Info('Districts',district:GetType()),'ACQUISITION_DISTRICT_TYPE')
     local kind=family(row.DistrictType);if complete and kind then set[kind]=true end
    end
    acquisition={evidence='CONQUEST+Initialized+Transfer',reference=cp(q.reference),oldOwner=q.conquest.oldOwner,
     turn=q.turn,conquered=q.conquest.sequence,added=q.added,initialized=q.initSequence,transferred=q.transferred,
     legacySet=set,mode=next(set) and 'LEGACY_CLAIM' or 'FIRST_COMPLETION'}
   end
   q.stage='城市登记写入'
   local token,ledger
   if modern then
    assert(initialized and not writing,'NEW_SAVE_NOT_READY')
    local a=q.reference;local nextIndex=copyIndex(index);local serial=nextIndex.counter+1
    assert(serial<=capacity,'MAP_REGISTRATION_LIMIT')
    token='DEV-B013-P'..a.owner..'-'..serial
    assert(Game:GetProperty(PREFIX..token)==nil,'FOUNDATION_ORPHAN_RECORD')
    nextIndex.counter=serial;nextIndex.entries[token]={owner=a.owner,cityID=a.cityID,x=a.x,y=a.y,serial=serial}
    assert(same(Game:GetProperty(INDEX),index),'INDEX_STALE')
    writing=true
    local good,err=pcall(function()
     P.SetProperty(Game,INDEX,nextIndex);assert(same(Game:GetProperty(INDEX),nextIndex),'INDEX_WRITE_UNCONFIRMED')
    end)
    writing=false
    if not good then fault=tostring(err);error(fault)end
    index=nextIndex;positions[a.x..':'..a.y]=token
    assert(same(reference(c),a) and c:GetProperty(M.Keys.TOKEN)==nil,'FOUNDATION_REFERENCE_CHANGED')
    P.SetProperty(c,M.Keys.TOKEN,token);assert(c:GetProperty(M.Keys.TOKEN)==token,'CITY_WRITE_UNCONFIRMED')
    ledger={schema=2,owner=a.owner,counter=serial,records={[tostring(a.cityID)]={owner=a.owner,cityID=a.cityID,x=a.x,y=a.y,serial=serial,uid=token,state='CONFIRMED'}}}
   else
    local binding=assert(shared.BindingProbe,'FOUNDATION_BINDING_NOT_READY')
    token,ledger=binding.AllocateFoundation(c)
   end
   assert(not workers[token] and not envelope.records[token],'FOUNDATION_TOKEN_COLLISION')
   assert(not q.error,q.error)
   local w=make(token,true)
   local proof={evidence='FOUND_CITY+Initialized',reference=cp(q.reference),turn=q.turn,unitID=q.found,reason=foundReason}
   if acquisition then w.Acquire(c,acquisition,ledger) else w.Found(c,proof,ledger)end
   -- Replay only delivered completion events, in delivery order, with live revalidation.
   for _,e in ipairs(q.completions)do
    local city,now=completion(e.owner,e.index,e.x,e.y)
    assert(now and same(now,e.fact) and same(reference(city),q.reference),'EARLY_COMPLETION_CHANGED')
    w.Complete(e.owner,city,now)
    break -- all buffered rows were qualified at delivery; only the first can lock
   end
   assert(not q.error,q.error)
   if shared.OnPermanentCityWrite then shared.OnPermanentCityWrite(c,'CityProgressionStore.lua')end
  end)
  q.committing=false
  if not ok then
   q.error=tostring(err)
   local c=CityManager.GetCityAt(q.reference.x,q.reference.y)
   local readable,w=pcall(find,c)
   if readable and w then pcall(w.HoldCompletion,'FOUNDATION_ADMISSION_INCOMPLETE')end
   return
  end
  for i,v in ipairs(pending)do if v==q then table.remove(pending,i);break end end
 end
 local function spatial(name,owner,id,x,y)
  if not integer(id) then return end
  local q=candidate(owner,id,x,y);if not q then return end
  if name=='CityInitialized' then q.initialized=true;q.initSequence=q.initSequence or eventSerial end
  if name=='CityAddedToMap' then q.added=q.added or eventSerial end
  admit(q)
 end
 local function founded(owner,unitID,x,y,reason)
  if foundReason==nil or reason~=foundReason or not integer(unitID) then return end
  local q=candidate(owner,nil,x,y);if not q then return end
  if q.found and q.found~=unitID then q.error='FOUNDATION_UNIT_CONFLICT' else q.found=unitID end
  admit(q)
 end
 local function constructed(pid,index,x,y)
  if not freshReady or not P.IsTestPlayer(pid)then return end
  local object=CityManager.GetDistrictAt(x,y);local target=object and object:GetCity()
  if not target then
   -- Cannot assign this missing native reference to one city. Retain history and
   -- hold only fresh UNASSIGNED records, never pick a later completion on load.
   for _,w in pairs(workers)do w.HoldCompletion('COMPLETION_CITY_UNAVAILABLE')end
   for _,q in ipairs(pending)do q.error='COMPLETION_CITY_UNAVAILABLE'end
   return
  end
  local q=target and at(target:GetX(),target:GetY());local w=target and find(target)
  if not q and not w then return end
  local ok,err=pcall(function()
   local c,e=completion(pid,index,x,y);if not e then return end
   if q then
    if q.error then return end
    if q.reference.cityID==nil and q.reference.owner==e.reference.owner and q.reference.x==e.reference.x and q.reference.y==e.reference.y then q.reference.cityID=e.reference.cityID end
    if q.turn~=e.turn or not same(q.reference,e.reference) then q.error='EARLY_COMPLETION_REFERENCE_CHANGED';return end
    for _,v in ipairs(q.completions)do if same(v.fact,e)then return end end
    if #q.completions>=COMPLETIONS then q.error='EARLY_COMPLETION_LIMIT';return end
    q.completions[#q.completions+1]={owner=pid,index=index,x=x,y=y,fact=e}
    return -- reentrant callbacks during admission are consumed by its ordered replay
   end
   w.Complete(pid,c,e)
  end)
  if not ok then
   if q then q.error=tostring(err) elseif w then w.HoldCompletion('COMPLETION_EVIDENCE_UNAVAILABLE')end
  end
 end
 local function freshHook(ns,name,fn)
  local ev=P.Field(ns,name);if not ev or type(ev.Add)~='function' then hooks[name]=false;return end
  hooks[name]=pcall(ev.Add,function(...)
   if fault then return end
   eventSerial=eventSerial+1
   local ok,err=pcall(fn,...)
   if not ok then
    -- Hold pending candidates only; never poison an unrelated existing-city writer.
    for _,q in ipairs(pending)do if not q.error then q.error=tostring(err)end end
   end
  end)
 end
 freshHook(Events,'LoadScreenClose',function()if modern then initializeNew()end;freshReady=not fault and (not modern or initialized)end)
 freshHook(GameEvents,'CityBuilt',function(...)spatial('CityBuilt',...)end)
 freshHook(Events,'CityAddedToMap',function(...)spatial('CityAddedToMap',...)end)
 freshHook(GameEvents,'CityConquered',function(owner,oldOwner,id,x,y)
  if not modern then return end
  local q=candidate(owner,id,x,y);if not q then return end
  if not integer(oldOwner) or oldOwner==owner then q.error='ACQUISITION_OWNER_INVALID';return end
  if q.conquest then
   if q.conquest.oldOwner~=oldOwner then q.error='ACQUISITION_CONFLICT'end
  else q.conquest={oldOwner=oldOwner,sequence=eventSerial}end
 end)
 freshHook(Events,'CityInitialized',function(...)spatial('CityInitialized',...)end)
 freshHook(Events,'UnitActivate',founded)
 freshHook(GameEvents,'OnDistrictConstructed',constructed)
 freshHook(Events,'CityTransfered',function(owner,id,oldOwner)
  if modern and freshReady and P.IsTestPlayer(owner) then
   local c=CityManager.GetCity(owner,id)
   local q=c and at(c:GetX(),c:GetY())
   if q and q.conquest then
    if oldOwner~=q.conquest.oldOwner then q.error='ACQUISITION_OWNER_CONFLICT';return end
    q.transferred=q.transferred or eventSerial
    -- Pre-transfer delivery is not a subsequent completion. Snapshot current facts once.
    q.completions={};admit(q);return
   end
  end
  for _,q in ipairs(pending)do
   local c=CityManager.GetCityAt(q.reference.x,q.reference.y)
   if c and c:GetOwner()==owner and c:GetID()==id and (oldOwner==q.reference.owner or owner~=q.reference.owner)then q.error='FOUNDATION_TRANSFER_BEFORE_ADMISSION'end
  end
 end)
 freshHook(Events,'CityRemovedFromMap',function(owner,id)
  for _,q in ipairs(pending)do if q.reference.owner==owner and q.reference.cityID==id then q.error='FOUNDATION_REFERENCE_REMOVED'end end
 end)
 local nativeDescribe=store.NativeDescribe
 function store.NativeDescribe(pid,c)
  if c and at(c:GetX(),c:GetY()) then return store.Describe(pid,c)end
  return nativeDescribe(pid,c)
 end
 local describe=store.Describe
 function store.Describe(pid,c)
  if c then
   local q=at(c:GetX(),c:GetY())
   if q then
    -- Keep raw error internally; the player report needs one actionable reason, not a traceback.
    local reason=tostring(q.error or (q.conquest and '等待征服完成/城市转移确认') or (foundReason==nil or not hooks.UnitActivate) and 'FOUND_CITY监听/枚举不可用' or 'FOUND_CITY / 城市初始化')
    reason=reason:match('[^\r\n]+') or 'UNKNOWN'
    reason=reason:gsub('^.-:%d+: ','')
    return P.VERSION..' | 城市取得待确认'..'\n阶段：'..(q.stage or '事件确认')..'\n原因：'..reason
     ..'\n登记尚未确认；不会自动认领或推断历史。\n请保留当前存档和报告；不要再次迁移或投资。'
   end
   if freshOverflow and not store.Owns(c) and not legacyPresent(c) then return '新城登记暂停：候选数量超过安全界限；未猜测城市历史。'end
  end
  if c and not store.Owns(c) and c:GetProperty(M.Keys.TOKEN)~=nil and c:GetProperty(M.Keys.JOURNAL)==nil and c:GetProperty(M.Keys.FLOW)==nil then
   return '新城记录未完成：绑定已存在，但缺少已确认的进度记录。\n请保留报告，回到建城前存档；不会自动认领或补造历史。'
  end
  return describe(pid,c)
 end
 local function listen(ns,name)
  local e=P.Field(ns,name);if not e or not e.Add then return end
  e.Add(function(...)
   if fault then return end
   for _,w in pairs(workers)do w.Handle(name,...)end
  end)
 end
 for _,name in ipairs({'LoadScreenClose','CityTransfered','CityAddedToMap','CityRemovedFromMap','CityInitialized'})do listen(Events,name)end
 listen(GameEvents,'CityConquered');listen(GameEvents,'CityBuilt')
end

-- Explicit historical test adapter, never selected by Gameplay or a UI action.
function SPCCityProgressionStore.StartLegacyTest(P,shared)return SPCCityProgressionStore.Start(P,shared,true)end
