-- City-owned Dialogue history. No native calls, yields, owner partition or cap.
SPCDialogueProjectModel={}
local M=SPCDialogueProjectModel
local function copy(v)
 if type(v)~='table' then return v end
 local o={};for k,x in pairs(v)do o[k]=copy(x)end;return o
end
M.Copy=copy
local function integer(v) return type(v)=='number' and v>=0 and v%1==0 and v<=9007199254740991 end
local function era(v)return type(v)=='string' and v:match('^ERA_[A-Z0-9_]+$')~=nil end
local function reference(v)
 return type(v)=='table' and integer(v.owner) and integer(v.cityID) and integer(v.x) and integer(v.y)
end
function M.New()return {version=1,serial=0,total=0,used={}}end
function M.Validate(v,record)
 assert(type(v)=='table' and v.version==1 and integer(v.serial) and integer(v.total) and type(v.used)=='table','DIALOGUE_HISTORY_INVALID')
 local sum=0;local ids={}
 for e,r in pairs(v.used)do
  assert(era(e) and type(r)=='table' and integer(r.id) and r.id>0 and r.id<=v.serial and not ids[r.id]
   and integer(r.start) and integer(r.completed) and r.completed>=r.start and integer(r.x) and r.x<=7
   and r.gain==5*r.x and type(r.forced)=='boolean','DIALOGUE_RECEIPT_INVALID')
  ids[r.id]=true;sum=sum+r.gain
 end
 assert(sum==v.total,'DIALOGUE_HISTORY_TOTAL_MISMATCH')
 if v.last then
  assert(type(v.last)=='table' and integer(v.last.id) and v.last.id<=v.serial
   and type(v.last.reason)=='string' and #v.last.reason<=180,'DIALOGUE_LAST_INVALID')
 end
 local p=v.pending
 if p then
  assert(type(p)=='table' and p.id==v.serial and p.id>0 and era(p.era) and not v.used[p.era]
   and integer(p.start) and type(p.ended)=='boolean' and reference(p.reference)
   and type(p.token)=='string' and #p.token>0 and (p.stage=='ACTIVE' or p.stage=='CALLING' or p.stage=='HELD')
   and type(p.reason)=='string' and #p.reason<=180,'DIALOGUE_PENDING_INVALID')
  if record then
   local r=record.current or record.origin
   assert(record.stage=='ACTIVE' and p.token==record.base.token and p.reference.owner==r.owner
    and p.reference.cityID==r.cityID and p.reference.x==r.x and p.reference.y==r.y,'DIALOGUE_PENDING_REFERENCE')
  end
 end
 return v
end
function M.Begin(v,token,ref,e,turn)
 v=copy(v or M.New());M.Validate(v)
 assert(not v.pending and not v.used[e] and era(e) and integer(turn) and reference(ref),'DIALOGUE_START_REJECTED')
 v.serial=v.serial+1
 v.pending={id=v.serial,token=token,reference=copy(ref),era=e,start=turn,ended=false,stage='ACTIVE',reason='完整一回合计时中'}
 M.Validate(v);return v
end
function M.Cancel(v,reason)
 if not v or not v.pending then return v end
 v=copy(v);v.last={id=v.pending.id,reason=reason};v.pending=nil;M.Validate(v);return v
end
function M.Hold(v,reason)
 v=copy(v);assert(v and v.pending,'DIALOGUE_NO_PENDING')
 v.pending.stage='HELD';v.pending.reason=reason;M.Validate(v);return v
end
function M.EndTurn(v,turn)
 v=copy(v);local p=assert(v and v.pending,'DIALOGUE_NO_PENDING')
 assert(p.stage=='ACTIVE' and p.start==turn,'DIALOGUE_END_WINDOW')
 p.ended=true;return v
end
function M.Calling(v,turn)
 v=copy(v);local p=assert(v and v.pending,'DIALOGUE_NO_PENDING')
 assert(p.stage=='ACTIVE' and p.ended and turn==p.start+1,'DIALOGUE_FULL_TURN_UNCONFIRMED')
 p.stage='CALLING';p.reason='原生完成已请求；结果不明时不重复调用';return v
end
function M.Complete(v,id,x,turn)
 v=copy(v);M.Validate(v);local p=assert(v.pending,'DIALOGUE_NO_PENDING')
 assert(p.id==id and (p.stage=='ACTIVE' or p.stage=='CALLING') and integer(x) and x<=7
  and integer(turn) and turn>=p.start and not v.used[p.era],'DIALOGUE_COMPLETION_REJECTED')
 -- A native forced completion is the existing accepted exception, not proof of 1T.
 local forced=not (p.ended and turn==p.start+1)
 v.used[p.era]={id=id,start=p.start,completed=turn,x=x,gain=5*x,forced=forced}
 v.total=v.total+5*x;v.last={id=id,reason=forced and '原生提前完成；未证明完整生产回合' or '完整回合完成并已保存'}
 v.pending=nil;M.Validate(v);return v
end
