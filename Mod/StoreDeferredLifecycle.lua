-- Pure optional recovery evidence for the existing nine ability owners.
-- The Store supplies confirmed lifecycle facts; this model never reads the game,
-- changes ability payloads, retries, writes Properties or proves native outcomes.
SPCStoreDeferredLifecycle={}
local M=SPCStoreDeferredLifecycle
local keys={'expeditionInsights','researchTradition','dialogue','engineering','capital','development','claimTimer','commerce','templateLifecycle'}
local allowed={};for _,key in ipairs(keys)do allowed[key]=true end
local function int(n)return type(n)=='number'and n==n and n>=0 and n<9007199254740991 and n%1==0 end
local function plain(t)return type(t)=='table'and getmetatable(t)==nil end
local function fields(t,list)
 assert(plain(t),'DEFERRED_STRUCTURE_INVALID')
 for key in pairs(t)do assert(list[key],'DEFERRED_FIELD_UNKNOWN')end
end
local refFields={owner=true,cityID=true,x=true,y=true}
local function reference(r)
 fields(r,refFields)
 assert(int(r.owner)and int(r.cityID)and int(r.x)and int(r.y),'DEFERRED_REFERENCE_INVALID')
end
local function sameRef(a,b)
 return a and b and a.owner==b.owner and a.cityID==b.cityID and a.x==b.x and a.y==b.y
end
local function refCopy(r)return {owner=r.owner,cityID=r.cityID,x=r.x,y=r.y}end
local function parent(r)
 assert(plain(r)and(r.schema==1 or r.schema==2 or r.schema==3)and plain(r.base)
  and type(r.base.token)=='string'and #r.base.token>0 and #r.base.token<=256
  and int(r.ownerChanges)and r.ownerChanges>0,'DEFERRED_PARENT_INVALID')
 reference(r.origin)
end
local envelopeFields={version=true,token=true,owner=true,x=true,y=true,entries=true}
local entryFields={epoch=true,firstTurn=true,lossTurn=true,lossTarget=true,returnTurn=true,returned=true,scope=true}
local witnessFields={key=true,token=true,epoch=true,firstTurn=true,lossTurn=true,lossTarget=true,returnTurn=true,returned=true,scope=true}
local function entry(e,origin,witness)
 fields(e,witness and witnessFields or entryFields);reference(e.lossTarget)
 assert(int(e.epoch)and e.epoch>0 and int(e.firstTurn)
  and e.lossTarget.owner~=origin.owner and e.lossTarget.x==origin.x and e.lossTarget.y==origin.y,'DEFERRED_EPISODE_INVALID')
 assert(e.lossTurn==nil or int(e.lossTurn)and e.lossTurn>=e.firstTurn,'DEFERRED_LOSS_TURN_INVALID')
 assert((e.returnTurn==nil)==(e.returned==nil),'DEFERRED_RETURN_PAIR_INVALID')
 if e.returned then
  reference(e.returned)
  assert(int(e.returnTurn)and e.returnTurn>=(e.lossTurn or e.firstTurn)
   and e.returned.owner==origin.owner and e.returned.x==origin.x and e.returned.y==origin.y,'DEFERRED_RETURN_INVALID')
 else assert(e.lossTurn~=nil,'DEFERRED_LOSS_MISSING')end
end
function M.Keys()local out={};for i,key in ipairs(keys)do out[i]=key end;return out end
function M.Validate(v,r)
 if v==nil then return nil end
 fields(v,envelopeFields)
 assert(v.version==1 and type(v.token)=='string'and #v.token>0 and #v.token<=256
  and int(v.owner)and int(v.x)and int(v.y)and plain(v.entries),'DEFERRED_ENVELOPE_INVALID')
 local n=0
 for key,e in pairs(v.entries)do
  assert(allowed[key],'DEFERRED_OWNER_UNKNOWN');n=n+1;entry(e,v)
  assert(e.scope==nil or key=='commerce'and e.scope=='REPUTATION','DEFERRED_SCOPE_INVALID')
 end
 assert(n>0 and n<=#keys,'DEFERRED_BOUND_INVALID')
 if r then
  parent(r)
  assert(v.token==r.base.token and v.owner==r.origin.owner and v.x==r.origin.x and v.y==r.origin.y,'DEFERRED_PARENT_REFERENCE_CHANGED')
  local loss=r.stage=='HELD_TRANSFER'and r.loss or r.stage=='ACTIVE'and r.lastLoss
  assert(plain(loss)and sameRef(loss.origin,r.origin),'DEFERRED_PARENT_LOSS_UNAVAILABLE')
  for _,e in pairs(v.entries)do
   assert(e.epoch==r.ownerChanges and sameRef(e.lossTarget,loss.target),'DEFERRED_PARENT_EPISODE_CHANGED')
   if r.stage=='HELD_TRANSFER'then assert(e.returned==nil,'DEFERRED_PARENT_STAGE_CHANGED')
   else assert(e.returned and sameRef(e.returned,r.current),'DEFERRED_PARENT_RETURN_CHANGED')end
  end
 end
 return v
end
local function entryCopy(e)
 return {epoch=e.epoch,firstTurn=e.firstTurn,lossTurn=e.lossTurn,lossTarget=refCopy(e.lossTarget),
  returnTurn=e.returnTurn,returned=e.returned and refCopy(e.returned)or nil,scope=e.scope}
end
local function copy(v,r)
 M.Validate(v)
 local out={version=1,token=r.base.token,owner=r.origin.owner,x=r.origin.x,y=r.origin.y,entries={}}
 if v then
  assert(v.token==out.token and v.owner==out.owner and v.x==out.x and v.y==out.y,'DEFERRED_PARENT_REFERENCE_CHANGED')
  for key,e in pairs(v.entries)do out.entries[key]=entryCopy(e)end
 end
 return out
end
local function selected(wanted)
 assert(plain(wanted),'DEFERRED_SELECTION_INVALID')
 for key,value in pairs(wanted)do assert(allowed[key]and(type(value)=='boolean'or key=='commerce'and value=='REPUTATION'),'DEFERRED_SELECTION_INVALID')end
end
local function scope(old,wanted)
 if old and old.scope==nil or wanted==true then return nil end
 return old and old.scope or wanted=='REPUTATION'and 'REPUTATION'or nil
end
local function finish(v,r)
 if next(v.entries)==nil then return nil end
 return M.Validate(v,r)
end
function M.Loss(v,r,wanted,turn)
 parent(r);selected(wanted);assert(int(turn),'DEFERRED_TURN_INVALID')
 assert(r.stage=='HELD_TRANSFER'and plain(r.loss)and sameRef(r.loss.origin,r.origin),'DEFERRED_LOSS_UNCONFIRMED')
 reference(r.loss.target)
 assert(r.loss.target.owner~=r.origin.owner and r.loss.target.x==r.origin.x and r.loss.target.y==r.origin.y,'DEFERRED_LOSS_UNCONFIRMED')
 local out=copy(v,r)
 for _,key in ipairs(keys)do if wanted[key]or out.entries[key]then
  local old=out.entries[key]
  assert(not old or r.ownerChanges>=old.epoch and turn>=old.firstTurn,'DEFERRED_EPOCH_REVERSED')
  if old and old.epoch==r.ownerChanges then
   assert(not old.returned and sameRef(old.lossTarget,r.loss.target),'DEFERRED_EPOCH_REUSED')
   assert(turn>=old.lossTurn,'DEFERRED_TURN_REVERSED') -- duplicate keeps original boundary
   old.scope=scope(old,wanted[key])
  else
   out.entries[key]={epoch=r.ownerChanges,firstTurn=old and old.firstTurn or turn,
    lossTurn=turn,lossTarget=refCopy(r.loss.target),scope=scope(old,wanted[key])}
  end
 end end
 return finish(out,r)
end
function M.Return(v,r,wanted,turn)
 parent(r);selected(wanted);assert(int(turn),'DEFERRED_TURN_INVALID')
 assert(r.stage=='ACTIVE'and plain(r.lastLoss)and sameRef(r.lastLoss.origin,r.origin),'DEFERRED_RETURN_UNCONFIRMED')
 reference(r.current);reference(r.lastLoss.target)
 assert(r.current.owner==r.origin.owner and r.current.x==r.origin.x and r.current.y==r.origin.y
  and r.lastLoss.target.owner~=r.origin.owner and r.lastLoss.target.x==r.origin.x and r.lastLoss.target.y==r.origin.y,'DEFERRED_RETURN_UNCONFIRMED')
 local out=copy(v,r)
 for _,key in ipairs(keys)do if wanted[key]or out.entries[key]then
  local e=out.entries[key]
  if e then
   assert(e.epoch==r.ownerChanges and sameRef(e.lossTarget,r.lastLoss.target),'DEFERRED_PARENT_EPISODE_CHANGED')
   assert(turn>=(e.returnTurn or e.lossTurn or e.firstTurn),'DEFERRED_TURN_REVERSED')
   if e.returned then assert(sameRef(e.returned,r.current),'DEFERRED_PARENT_RETURN_CHANGED')end
  else e={epoch=r.ownerChanges,firstTurn=turn,lossTarget=refCopy(r.lastLoss.target),scope=scope(nil,wanted[key])};out.entries[key]=e end
  e.scope=scope(e,wanted[key])
  if not e.returned then e.returnTurn=turn;e.returned=refCopy(r.current)end
 end end
 return finish(out,r)
end
function M.Entry(v,key,r)
 assert(allowed[key],'DEFERRED_OWNER_UNKNOWN');M.Validate(v,r)
 if not v or not v.entries[key]then return nil end
 local out=entryCopy(v.entries[key]);out.key=key;out.token=v.token;return out
end
local function sameEntry(a,b)
 return plain(a)and plain(b)and a.epoch==b.epoch and a.firstTurn==b.firstTurn and a.lossTurn==b.lossTurn
  and a.returnTurn==b.returnTurn and a.scope==b.scope and sameRef(a.lossTarget,b.lossTarget)
  and(a.returned==nil and b.returned==nil or sameRef(a.returned,b.returned))
end
function M.Clear(v,key,witness,r)
 assert(allowed[key],'DEFERRED_OWNER_UNKNOWN');M.Validate(v,r)
 assert(v and v.entries[key]and plain(witness),'DEFERRED_CLEAR_UNCONFIRMED')
 entry(witness,v,true);assert(witness.key==key and witness.token==v.token and sameEntry(v.entries[key],witness),'DEFERRED_CLEAR_STALE')
 local out=copy(v,r);out.entries[key]=nil;return finish(out,r)
end
