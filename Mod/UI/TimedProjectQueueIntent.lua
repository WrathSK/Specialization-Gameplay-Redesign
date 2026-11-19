-- B398: two opt-in UI queue policies. No timer, save authority or queue mutation.
SPCTimedProjectQueueIntent={LIMIT=2048,QUEUE_LIMIT=100}
local M=SPCTimedProjectQueueIntent
local kinds={DialogueProjects={project='PROJECT_SPC_ERA_DIALOGUE',status='SPC_DialogueQueueStatus',action='DIALOGUE_PROJECT_BEGIN'},
 EngineeringStudy={project='PROJECT_SPC_ENGINEERING_STUDY',status='SPC_EngineeringStudyQueueStatus',action='ENGINEERING_STUDY_BEGIN'}}
local function int(n)return type(n)=='number'and n>=0 and n%1==0 and n<9007199254740991 end
local function key(pid,id)return tostring(pid)..':'..tostring(id)end
local function reference(c)return key(c:GetOwner(),c:GetID())..':'..c:GetX()..':'..c:GetY()end
function M.New(P,client,kind,send,notify)
 local spec=assert(kinds[kind],'TIMED_QUEUE_KIND');local d={};local rows,hints,hintKeys={},{},{};local hintNext=1;local count,serial,generation=0,0,-1;local busy,closed=false,false;local work=false;local localPlayer,seenBackend,seenRevision,seenClosed,seenOpen
 local function backend()return (ExposedMembers.SPC_P0 or {})[kind]end
 local function owned()return not closed and client.OwnsReader()end
 local function reset()
  if generation~=client.Generation()then rows,hints,hintKeys={},{},{};hintNext=1;count=0;generation=client.Generation();work=false;localPlayer=nil;seenBackend=nil;seenRevision=nil;seenClosed=nil;seenOpen=nil end
 end
 local function view(k)local b=backend();return b and b.views and b.views[k]end
 local function reasonCode(v)
  if kind=='DialogueProjects'then return v.reasonCode end
  return v.reason -- Engineering Study already publishes stable reason codes.
 end
 local function viewKey(v)
  if not v then return 'UNKNOWN'end
  return tostring(v.stage)..':'..tostring(reasonCode(v))..':'..tostring(v.start)..':'..tostring(v.L)..':'..tostring(v.E)..':'..tostring(v.era)..':'..tostring(v.token)..':'..tostring(v.completedID)..':'..tostring(v.cancelledID)
 end
 local function window(pid)
  local b=backend();return b and tostring(b.beginClosedTurns and b.beginClosedTurns[pid])..':'..tostring(b.beginOpenTurns and b.beginOpenTurns[pid])or 'UNKNOWN'
 end
 local function hint(p,label,helpKey)
  local k=key(p.pid,p.id);local old=hints[k];local signature=viewKey(view(k))
  if old and old.label==label and old.helpKey==helpKey and old.view==signature then return end
  local slot=old and old.slot
  if not slot then
   slot=hintNext;hintNext=hintNext%M.LIMIT+1
   local victim=hintKeys[slot]
   if victim and hints[victim]and hints[victim].slot==slot then hints[victim]=nil end
   hintKeys[slot]=k
  end
  hints[k]={label=label,helpKey=helpKey,view=signature,slot=slot}
  if notify then pcall(notify,p.pid,p.id)end
 end
 local function forget(k,label,helpKey)
  local p=rows[k];if p then rows[k]=nil;count=count-1;if label then hint(p,label,helpKey)else hints[k]=nil end end
 end
 local function admit(c,origin)
  reset();local pid,id=c:GetOwner(),c:GetID();localPlayer=pid;local k=key(pid,id);local p=rows[k]
  local ref=reference(c)
  if p and p.reference~=ref then forget(k);p=nil end
  if not p then
   if count>=M.LIMIT then d.error='TIMED_QUEUE_CAPACITY';hint({pid=pid,id=id},'UNAVAILABLE','CANDIDATE_LIMIT');return end
   serial=serial+1;p={pid=pid,id=id,reference=ref,origin=origin,serial=serial,revision=0};rows[k]=p;count=count+1
  end
  return p
 end
 local function current(p,rev,gen)
  return owned()and generation==gen and client.Generation()==gen and rows[key(p.pid,p.id)]==p and p.revision==rev
 end
 function d.Supported(c)
  if not c or not P.IsTestPlayer(c:GetOwner())then return false end
  local ok,q=pcall(c.GetBuildQueue,c)
  return ok and type(P.Field(q,'GetAt'))=='function'
 end
 local function sample(c,p)
  local rev,gen=p.revision,generation
  local ref=reference(c);assert(ref==p.reference and c:GetOwner()==Game.GetLocalPlayer(),'TIMED_QUEUE_REFERENCE')
  local turn=Game.GetCurrentGameTurn();local q=c:GetBuildQueue();local n=q:GetSize()
  assert(int(n)and n<=M.QUEUE_LIMIT,'TIMED_QUEUE_SIZE_UNKNOWN')
  local projectDirective=assert(CityProductionDirectives and CityProductionDirectives.PROJECT,'TIMED_QUEUE_DIRECTIVE_UNKNOWN')
  local target=assert(GameInfo.Projects[spec.project],'TIMED_QUEUE_PROJECT_UNKNOWN');local matches,index=0,nil
  for i=0,n-1 do
   local entry=assert(q:GetAt(i),'TIMED_QUEUE_ENTRY_UNKNOWN');local directive=P.Field(entry,'Directive')
   assert(type(directive)=='number'or type(directive)=='string','TIMED_QUEUE_DIRECTIVE_UNKNOWN')
   if directive==projectDirective then
    local row=assert(GameInfo.Projects[P.Field(entry,'ProjectType')],'TIMED_QUEUE_TYPE_UNKNOWN')
    assert(type(row.ProjectType)=='string','TIMED_QUEUE_TYPE_UNKNOWN')
    if row.ProjectType==spec.project then matches=matches+1;index=i end
   end
  end
  local hash=q:GetCurrentProductionTypeHash()
  assert(hash~=nil and (hash~=target.Hash or n>0 and matches>0),'TIMED_QUEUE_CURRENT_UNKNOWN')
  assert(n==q:GetSize()and hash==q:GetCurrentProductionTypeHash()and ref==reference(c)
   and turn==Game.GetCurrentGameTurn()and current(p,rev,gen),'TIMED_QUEUE_CHANGED_DURING_READ')
  if matches==1 and index==0 then assert(hash==target.Hash,'TIMED_QUEUE_CURRENT_UNKNOWN')end
  return {size=n,count=matches,index=index,turn=turn,signature=n..':'..tostring(hash)..':'..matches..':'..tostring(index)}
 end
 local function exhausted(v)
  return v and (v.stage=='USED'or v.stage=='INELIGIBLE')
 end
 local function exhaustedHelp(v)
  if v and (v.stage=='USED'or reasonCode(v)=='EST_KNOWLEDGE_REACHED')then
   return kind=='EngineeringStudy'and 'STUDY_KNOWLEDGE_REACHED'or 'DIALOGUE_ERA_USED'
  end
  return 'INELIGIBLE'
 end
 function d.Before(c,item,selected)
  if not item or item.Type~=spec.project then return nil end
  if not owned()or not c or selected or not P.IsTestPlayer(c:GetOwner())then return false end
  local p=admit(c,'EXPLICIT_SELECTION');if not p then return false end
  if p.inserting then hint(p,'WAITING_TO_QUEUE','QUEUE_REQUEST_PENDING');return false end
  p.revision=p.revision+1;p.force=true;p.attempt=nil;p.read=nil
  local v=view(key(p.pid,p.id));p.completedID=v and v.completedID;p.origin='EXPLICIT_SELECTION';p.initialAccepted=true
  if exhausted(v)then forget(key(p.pid,p.id),'INELIGIBLE',exhaustedHelp(v));return false end
  local rev=p.revision;local ok,s=pcall(sample,c,p)
  if not current(p,rev,generation)then return false end
  if not ok then hint(p,'VERIFYING','CANNOT_CONFIRM_SELECTION');return false end
  p.read=true;work=true
  if s.count>0 then
   p.confirmed=s.count==1;hint(p,s.count>1 and 'PAUSED'or 'ALREADY_QUEUED',s.count>1 and 'DUPLICATE_PROJECT'or 'ALREADY_QUEUED')
   return false -- existing entry is the explicit selection; never append a copy
  end
  local insertion={} -- private attempt identity survives optional notification reentry
  p.inserting=insertion -- native BUILD is asynchronous; lock before returning to the base panel
  hint(p,'WAITING_TO_QUEUE','QUEUE_INSERT_PENDING')
  if not current(p,rev,generation)then if p.inserting==insertion then p.inserting=nil end;return false end
  return true
 end
 function d.CancelUnconfirmed(c)
  if not owned()or not c then return end;reset()
  local k=key(c:GetOwner(),c:GetID());local p=rows[k]
  -- Explicit replacement/removal intent abandons only an unconfirmed insertion,
  -- not a proven queued entry or any saved Gameplay round.
  if p and not p.confirmed then forget(k)end
 end
 function d.Event(pid,id)
  if not owned()or type(pid)~='number'or type(id)~='number'then return end
  reset();local p=rows[key(pid,id)]
  if p and P.IsTestPlayer(pid)then p.revision=p.revision+1;p.read=true;work=true end
 end
 function d.Initial(c)
  if not owned()or not d.Supported(c)then return end
  local k=key(c:GetOwner(),c:GetID());local p=admit(c,'RECOVERED_NATIVE_QUEUE');if not p then return end
  local rev=p.revision;local ok,s=pcall(sample,c,p)
  if not current(p,rev,generation)then return end
  if not ok or s.count==0 then forget(k);return end
  p.confirmed=s.count==1;p.read=true;work=true;p.initialTurn=s.turn;local v=view(k);p.completedID=v and v.completedID
 end
 function d.Boundary()
  if not owned()then return end;reset()
  local turn=Game.GetCurrentGameTurn()
  for _,p in pairs(rows)do if p.waitWindow and p.boundaryTurn~=turn then
   p.boundaryTurn=turn;p.revision=p.revision+1;p.read=true;p.waitWindow=nil;work=true
  end end
 end
 local function allowedView(v)
  if not v or exhausted(v)or v.stage=='CALLING'then return false end
  if v.stage=='HELD'then
   local why=reasonCode(v)
   if kind=='DialogueProjects'then return why=='DIALOGUE_RELATED_FACT_REQUIRED'end
   return why=='EST_SINGLE_PROJECT_REQUIRED'or why=='EST_RELATED_FACT_REQUIRED'or why=='EST_QUEUE_UNKNOWN'
  end
  return v.stage=='AVAILABLE'or v.stage=='ACTIVE'
 end
 local function process(k,p)
  local v=view(k);local vk=viewKey(v);local w=window(p.pid)
  if p.origin=='RECOVERED_NATIVE_QUEUE'and not p.initialAccepted then
   if not v or not int(v.completedID)then p.read=nil;p.view=vk;return end
   if v.completedID>0 and (not int(v.completedTurn)or v.completedTurn>=p.initialTurn)then
    forget(k,'UNCONFIRMED','ALREADY_COMPLETED_THIS_TURN');return
   end
   p.initialAccepted=true
  end
  if v and v.completedID~=nil then
   if p.completedID~=nil and v.completedID>p.completedID then forget(k);return end
   p.completedID=v.completedID
  end
  if p.view~=vk then
   if p.view~=nil then p.read=true;p.revision=p.revision+1 end
   p.view=vk
  end
  if p.waitWindow and p.window~=w then p.read=true;p.revision=p.revision+1;p.waitWindow=nil end;p.window=w
  if exhausted(v)then forget(k,'INELIGIBLE',exhaustedHelp(v));return end
  if not p.read then return end
  p.read=nil;local revision,gen=p.revision,generation
  local c=Players[p.pid]and Players[p.pid]:GetCities():FindID(p.id)
  if not c then forget(k);return end
  if reference(c)~=p.reference then forget(k);return end
  local ok,s=pcall(sample,c,p)
  if not current(p,revision,gen)then return end
  if not ok then hint(p,'VERIFYING','QUEUE_UNCONFIRMED');return end
  if s.count==0 then
   if p.confirmed then forget(k)else hint(p,'WAITING_TO_QUEUE','QUEUE_INSERT_PENDING')end
   return
  end
  p.inserting=nil -- a real entry proves the insertion outcome
  if s.count>1 then hint(p,'PAUSED','DUPLICATE_PROJECT');return end
  p.confirmed=true
  if s.size~=1 or s.index~=0 then
   if s.index~=0 then p.force=true end
   hint(p,s.index==0 and 'PAUSED'or 'QUEUED',s.index==0 and 'REQUIRES_SOLE_ENTRY'or 'WAITS_TURN_IN_QUEUE')
   p.queue=s.signature;return
  end
  if not allowedView(v)then hint(p,'UNCONFIRMED');return end
  if v.stage=='ACTIVE'and v.start==s.turn and not p.force then hints[k]=nil;p.waitWindow=nil;p.queue=s.signature;return end
  local b=backend()
  if b.beginClosedTurns and b.beginClosedTurns[p.pid]==s.turn then
   p.waitWindow=true;hint(p,'WAITING_TO_START','WAITING_FOR_NEXT_TURN');return
  end
  local player=Players[p.pid];local method=P.Field(player,'IsTurnActive')
  local activeOK,active=false,nil;if type(method)=='function'then activeOK,active=pcall(method,player)end
  if not current(p,revision,gen)then return end
  if not activeOK or active~=true then p.waitWindow=true;hint(p,'WAITING_TO_START','WAITING_FOR_ACTIVE_TURN');return end
  -- A confirmed owner cancellation changes cancelledID; unknown sends do not.
  local attempt=s.turn..':'..p.serial..':'..s.signature..':'..vk
  if p.attempt==attempt then return end
  p.attempt=attempt;p.force=nil;p.queue=s.signature -- latch before script-operation reentry
  hint(p,'CONFIRMING','CONFIRMING_FULL_TURN')
  if not current(p,revision,gen)or b~=backend()then return end
  local sent=pcall(send,p.pid,PlayerOperations.EXECUTE_SCRIPT,{OnStart='SPC_P0_Request',Action=spec.action,CityID=p.id,StartTurn=s.turn,Token='TQI:'..generation..':'..p.serial..':'..s.turn..':'..tostring(v.cancelledID or 0)})
  if not sent and current(p,revision,gen)then hint(p,'UNCONFIRMED','START_REQUEST_UNCONFIRMED')end
 end
 function d.Pulse()
  if busy or not owned()or not client.Ready()then return end;reset()
  local b=backend();local revision=b and b.revision
  local ending=b and b.beginClosedTurns and b.beginClosedTurns[localPlayer]
  local opening=b and b.beginOpenTurns and b.beginOpenTurns[localPlayer]
  if not work and b==seenBackend and revision==seenRevision and ending==seenClosed and opening==seenOpen then return end
  work=false;seenBackend=b;seenRevision=revision;seenClosed=ending;seenOpen=opening;busy=true
  local ok,err=pcall(function()for k,p in pairs(rows)do if not owned()then break end;process(k,p)end end);busy=false
  if not ok then d.error='TIMED_QUEUE_READ_FAILED'end
 end
 local status=function(pid,id)
  if not owned()then return end;reset();local k=key(pid,id);local h=hints[k]
  local v=view(k)
  if h and h.view==viewKey(v)then
   local label=Locale.Lookup('LOC_SPC_TIMED_QUEUE_LABEL_'..h.label)
   local help=h.helpKey and Locale.Lookup('LOC_SPC_TIMED_QUEUE_HELP_'..h.helpKey)
   return label,help or (v and v.reason) or Locale.Lookup('LOC_SPC_TIMED_QUEUE_HELP_AWAITING_PROJECT_FACTS')
  end
 end
 ExposedMembers[spec.status]=status
 function d.Close()
  if closed then return end;closed=true
  if ExposedMembers[spec.status]==status then ExposedMembers[spec.status]=nil end
  rows,hints,hintKeys={},{},{};count=0
 end
 return d
end
