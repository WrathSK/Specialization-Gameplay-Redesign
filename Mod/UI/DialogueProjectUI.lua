include('TimedProjectSelectionClient')
-- Normal production intent/read model. Gameplay owns timers, quota and history.
include('GreatWorkFacts')
SPCDialogueProjectUI={}
local M=SPCDialogueProjectUI
M.PROJECT='PROJECT_SPC_ERA_DIALOGUE'
function M.Current(c)
 local row=GameInfo.Projects[M.PROJECT]
 return c and c:GetOwner()==Game.GetLocalPlayer() and row and c:GetBuildQueue():GetCurrentProductionTypeHash()==row.Hash and M.PROJECT or nil
end
function M.Preview()
 return '1','时代对话：需连续占用完整的 1 个回合；完成后按本城合格馆藏覆盖的作品时代数，永久累计巨作原生旅游业绩倍率。'
end
function M.Text(pid,id)
 local d=(ExposedMembers.SPC_P0 or {}).DialogueProjects;local v=d and d.views[pid..':'..id]
 if v and v.stage=='ACTIVE' then return '1',v.reason end
 if v and v.stage=='CALLING' then return '待确认',v.reason end
 if v and v.stage=='HELD' then return '已暂停',v.reason end
 local c=Players[pid] and Players[pid]:GetCities():FindID(id)
 if M.Current(c)then return '待计时','此项目须独占生产队列并连续占用完整的 1 个回合；计时等待Gameplay确认，未确认时不会完成项目。'end
 return M.Preview()
end
function M.New(P,send,notify)
 local api={};local pending,seen={},{};local revision=-1
 local client=SPCTimedProjectSelectionClient.New(P,pending);api.QueueEvent=client.QueueEvent;api.Close=client.Close
 local collect=SPCGreatWorkFacts.Collector(P)
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
   local raw=collect(c)
   assert(c:GetOwner()==pid and c:GetID()==id and c:GetX()==ref.x and c:GetY()==ref.y
    and v.turn==Game.GetCurrentGameTurn(),'完成取样期间引用变化')
   v.protocol=2;v.raw=raw
  end
  return v
 end
 local function backend()return (ExposedMembers.SPC_P0 or {}).DialogueProjects end
 local function queue(pid,id)return ExposedMembers.SPC_DialogueProjectRead(pid,id,false)end
 client.Configure('DialogueProjects','SPC_DialogueProjectRead','DIALOGUE_PROJECT_SYNC',send)
 api.Connect=client.Connect;api.Sync=client.Sync;api.WarmStart=client.WarmStart
 function api.Before(c,item,queued)
  if not client.OwnsReader()then return not item or item.Type~=M.PROJECT end
  local k=c and (c:GetOwner()..':'..c:GetID())
  if not item or item.Type~=M.PROJECT then if k then pending[k]=nil end;return true end
  if not c or not P.IsTestPlayer(c:GetOwner()) or queued or pending[k]then return false end
  pending[k]={pid=c:GetOwner(),id=c:GetID(),turn=Game.GetCurrentGameTurn(),read=true};return true
 end
 local function drain()
  local b=backend();if not b then return end
  for k,p in pairs(pending)do
   if not client.OwnsReader()then return end
   local v=b.views[k]
   if v and v.stage=='ACTIVE' and v.start==p.turn then pending[k]=nil
   elseif p.turn~=Game.GetCurrentGameTurn() or (p.sent and v and v.stage=='HELD')then pending[k]=nil;notify(p.pid,p.id)
   elseif not p.sent and p.read and client.Ready()then
    local ok,q,current=client.Read(k,p,function()return queue(p.pid,p.id)end)
    if current and ok and q.project==M.PROJECT and q.size==1 then
     p.sent=true
     local sent=pcall(send,p.pid,PlayerOperations.EXECUTE_SCRIPT,{OnStart='SPC_P0_Request',Action='DIALOGUE_PROJECT_BEGIN',CityID=p.id,StartTurn=p.turn,Token='DIALOGUE:'..k..':'..p.turn})
     if not sent and pending[k]==p and client.OwnsReader()then pending[k]=nil end
    elseif current and ok and q.project==M.PROJECT and type(q.size)=='number' and q.size>1 then pending[k]=nil;notify(p.pid,p.id)end
   end
  end
  if not client.OwnsReader()then return end
  if revision~=b.revision then
  revision=b.revision
  for k in pairs(seen)do if not b.views[k]then seen[k]=nil;pending[k]=nil end end
  for k,v in pairs(b.views)do
   if not client.OwnsReader()then return end
   local s=v.stage..':'..tostring(v.start)..':'..v.reason..':'..tostring(v.total)
   if seen[k]~=s then seen[k]=s;local pid,id=k:match('^(%d+):(%d+)$');if pid then notify(tonumber(pid),tonumber(id))end end
  end
  end
 end
 api.Pulse=client.Bind(drain)
 return api
end
