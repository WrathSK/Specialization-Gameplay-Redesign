-- Normal production intent/read model. Gameplay owns timers, quota and history.
include('GreatWorkFacts')
SPCDialogueProjectUI={}
local M=SPCDialogueProjectUI
M.PROJECT='PROJECT_SPC_ERA_DIALOGUE'
function M.Current(c)
 local row=GameInfo.Projects[M.PROJECT]
 return c and c:GetOwner()==Game.GetLocalPlayer() and row and c:GetBuildQueue():GetCurrentProductionTypeHash()==row.Hash and M.PROJECT or nil
end
function M.Text(pid,id)
 local d=(ExposedMembers.SPC_P0 or {}).DialogueProjects;local v=d and d.views[pid..':'..id]
 if v and v.stage=='ACTIVE' then return '1',v.reason end
 if v and v.stage=='CALLING' then return '待确认',v.reason end
 if v and v.stage=='HELD' then return '已暂停',v.reason end
 local c=Players[pid] and Players[pid]:GetCities():FindID(id)
 if M.Current(c)then return '确认中','等待Gameplay确认计时；未确认时不会完成项目'end
 return '1','时代对话：连续占用完整一回合；本批验证记录，不增加新倍率产出。'
end
function M.New(P,send,notify)
 local api={};local pending,synced,seen,retry={},{},{},{};local warmed=false;local pulse=0;local revision=-1
 local collect=SPCGreatWorkFacts.Collector(P);local catalog
 local function era()
  local row=assert(P.Info('Eras',Game.GetEras():GetCurrentEra()),'游戏时代不可读')
  return assert(row.EraType,'游戏时代类型不可读')
 end
 ExposedMembers.SPC_DialogueGameEra=era
 ExposedMembers.SPC_DialogueProjectRead=function(pid,id,works)
  assert(pid==Game.GetLocalPlayer() and P.IsTestPlayer(pid),'对话读取玩家不匹配')
  local c=assert(Players[pid] and Players[pid]:GetCities():FindID(id),'对话城市不可读')
  assert(c:GetOwner()==pid,'对话城市易主')
  local ref={owner=pid,cityID=id,x=c:GetX(),y=c:GetY()}
  local v={reference=ref,turn=Game.GetCurrentGameTurn(),project=M.Current(c),size=c:GetBuildQueue():GetSize()}
  if works then
   -- Fresh slots in this synchronous completion call; never the last background ACK.
   catalog=catalog or SPCGreatWorkCatalog.Build(P)
   local raw=collect(c);local p=SPCGreatWorkFacts.Plan(catalog,raw)
   assert(c:GetOwner()==pid and c:GetID()==id and c:GetX()==ref.x and c:GetY()==ref.y
    and v.turn==Game.GetCurrentGameTurn(),'完成取样期间引用变化')
   v.x=p.eraCount
  end
  return v
 end
 local function backend()return (ExposedMembers.SPC_P0 or {}).DialogueProjects end
 local function queue(pid,id)return ExposedMembers.SPC_DialogueProjectRead(pid,id,false)end
 function api.Sync(c)
  if not c or not P.IsTestPlayer(c:GetOwner())then return end
  local pid,id=c:GetOwner(),c:GetID();local k=pid..':'..id;local b=backend();if not b then return end
  local s=synced[k]
  if not s then s={pid=pid,id=id,tries=0,nextPulse=0};synced[k]=s end
  if s.done then return end
  if s.token and b.syncAck[k]==s.token then s.done=true;retry[k]=nil;return end
  if b.startupError then retry[k]=nil;return end
  if s.tries>=3 then retry[k]=nil;return end
  if pulse<s.nextPulse then return end
  retry[k]=s;s.tries=s.tries+1;s.nextPulse=pulse+6;s.token='DIALOGUE_SYNC:'..k..':'..s.tries
  pcall(send,pid,PlayerOperations.EXECUTE_SCRIPT,{OnStart='SPC_P0_Request',Action='DIALOGUE_PROJECT_SYNC',CityID=id,Token=s.token})
 end
 function api.WarmStart()
  if warmed then return end
  local pid=Game.GetLocalPlayer();if not Players[pid] or not P.IsTestPlayer(pid) or not backend()then return end
  warmed=true;for _,c in Players[pid]:GetCities():Members()do api.Sync(c)end
 end
 function api.Before(c,item,queued)
  local k=c and (c:GetOwner()..':'..c:GetID())
  if not item or item.Type~=M.PROJECT then if k then pending[k]=nil end;return true end
  if not c or not P.IsTestPlayer(c:GetOwner()) or queued or pending[k]then return false end
  pending[k]={pid=c:GetOwner(),id=c:GetID(),turn=Game.GetCurrentGameTurn()};return true
 end
 function api.Pulse()
  pulse=pulse+1;api.WarmStart()
  for k,s in pairs(retry)do
   local c=Players[s.pid] and Players[s.pid]:GetCities():FindID(s.id)
   if c and c:GetOwner()==s.pid then api.Sync(c)else retry[k]=nil;synced[k]=nil;pending[k]=nil;seen[k]=nil end
  end
  local b=backend();if not b then return end
  for k,p in pairs(pending)do
   local v=b.views[k]
   if v and v.stage=='ACTIVE' and v.start==p.turn then pending[k]=nil
   elseif p.turn~=Game.GetCurrentGameTurn() or (p.sent and v and v.stage=='HELD')then pending[k]=nil;notify(p.pid,p.id)
   elseif not p.sent then
    local ok,q=pcall(queue,p.pid,p.id)
    if ok and q.project==M.PROJECT and q.size==1 then
     p.sent=true
     local sent=pcall(send,p.pid,PlayerOperations.EXECUTE_SCRIPT,{OnStart='SPC_P0_Request',Action='DIALOGUE_PROJECT_BEGIN',CityID=p.id,StartTurn=p.turn,Token='DIALOGUE:'..k..':'..p.turn})
     if not sent then pending[k]=nil end
    elseif ok and q.project==M.PROJECT and type(q.size)=='number' and q.size>1 then pending[k]=nil;notify(p.pid,p.id)end
   end
  end
  if revision~=b.revision then
  revision=b.revision
  for k in pairs(seen)do if not b.views[k]then seen[k]=nil;synced[k]=nil;retry[k]=nil;pending[k]=nil end end
  for k,v in pairs(b.views)do
   local s=v.stage..':'..tostring(v.start)..':'..v.reason..':'..tostring(v.total)
   if seen[k]~=s then seen[k]=s;local pid,id=k:match('^(%d+):(%d+)$');if pid then notify(tonumber(pid),tonumber(id))end end
  end
  end
 end
 return api
end
