-- P0-M1: real production/timer/history; cumulative yield projection is not cut over.
include('DialogueProjectModel')
SPCDialogueProjects={}
function SPCDialogueProjects.Start(P,shared)
 local M=SPCDialogueProjectModel;local cp=M.Copy;local store=assert(shared.CityProgressionStore)
 local PROJECT='PROJECT_SPC_ERA_DIALOGUE';local MARKER='BUILDING_SPC_ERA_DIALOGUE_ACCESS'
 local d={views={},syncAck={},revision=0};shared.DialogueProjects=d
 local ready,busy=false,false;local dirty,active,settling,interrupted,finishing,armed={},{},{},{},{},{};local lastEra
 local function key(pid,id)return tostring(pid)..':'..tostring(id)end
 local function city(pid,id)return Players[pid] and Players[pid]:GetCities():FindID(id)end
 local function ref(c)return {owner=c:GetOwner(),cityID=c:GetID(),x=c:GetX(),y=c:GetY()}end
 local function same(a,b)
  if type(a)~=type(b)then return false end;if type(a)~='table'then return a==b end
  for k,v in pairs(a)do if not same(v,b[k])then return false end end
  for k in pairs(b)do if a[k]==nil then return false end end;return true
 end
 local function era()
  local ok,row=pcall(function()return P.Info('Eras',Game.GetEras():GetCurrentEra())end)
  if ok and row and row.EraType then return row.EraType end
  return assert(ExposedMembers.SPC_DialogueGameEra,'游戏时代接口未就绪')()
 end
 local function mark(pid,id)
  if P.IsTestPlayer(pid) and type(id)=='number' then dirty[key(pid,id)]={pid,id}end
 end
 local function markPlayer(pid)
  if not P.IsTestPlayer(pid)then return end
  for _,c in Players[pid]:GetCities():Members()do mark(pid,c:GetID())end
 end
 local function publish(pid,id,v)
  local k=key(pid,id)
  if not same(d.views[k],v)then d.views[k]=v;d.revision=d.revision+1 end
 end
 local function read(pid,c)
  local s=store.DialogueState(pid,c);local f=shared.EffectiveFacts.Read(pid,c)
  assert(f.token==s.token and f.owner==pid and f.cityID==c:GetID(),'城市专业引用不一致')
  local known=f.activeStatus=='KNOWN' and not f.investmentPending
  return s,f,known,known and f.specialization=='CULTURE' and f.active>=3
 end
 local function write(pid,c,s,v)
  store.WriteDialogue(pid,c,s.value,v)
  local actual=store.DialogueState(pid,c)
  assert(same(actual.value,v) and same(actual.reference,s.reference) and actual.token==s.token,'对话写入或引用未确认')
  return actual
 end
 local function queue(c)
  local q=c:GetBuildQueue();local ok,target=P.Call(q,'CurrentlyBuilding');assert(ok,'当前生产不可读')
  if target~=PROJECT then return q,false end
  local good,n=P.Call(q,'GetSize')
  if not good then
   local v=assert(ExposedMembers.SPC_DialogueProjectRead,'队列读取未就绪')(c:GetOwner(),c:GetID(),false)
   assert(same(v.reference,ref(c)) and v.turn==Game.GetCurrentGameTurn() and v.project==PROJECT,'队列引用不一致');n=v.size
  end
  assert(type(n)=='number' and n==1,'时代对话必须为唯一当前生产目标')
  return q,true
 end
 local function cancel(pid,c,s,reason)
  if s.value and s.value.pending then write(pid,c,s,M.Cancel(s.value,reason))end
  active[key(pid,c:GetID())]=nil;interrupted[key(pid,c:GetID())]=nil;armed[key(pid,c:GetID())]=nil;mark(pid,c:GetID())
 end
 local function safe(pid,id,fn)
  local ok,why=pcall(fn)
  if not ok then
   local old=d.views[key(pid,id)]
   publish(pid,id,{stage='HELD',reference=old and old.reference,token=old and old.token,reason=tostring(why):gsub('^.-:%d+: ',''):sub(1,180)})
  end
  return ok
 end
 local function audit(pid,id)
  local c=city(pid,id);local k=key(pid,id)
  if not c or c:GetOwner()~=pid then active[k]=nil;publish(pid,id,nil);return end
  local ok,s,f,known,eligible=pcall(read,pid,c)
  local eOK,e=pcall(era)
  local allowed=ok and known and eligible and eOK and not (s.value and s.value.used[e])
  local row=assert(P.Info('Buildings',MARKER),'时代对话入口定义缺失');local buildings=c:GetBuildings()
  local has=P.HasBuilding(buildings,row.Index);assert(type(has)=='boolean','项目入口状态不可读')
  if has~=allowed then
   if allowed then P.CreateBuilding(c:GetBuildQueue(),row.Index)else P.RemoveBuilding(buildings,row.Index)end
   assert(P.HasBuilding(buildings,row.Index)==allowed,'项目入口更新未确认')
  end
  if not ok then error(s)end
  if not eOK then error(e)end
  local v=s.value;local p=v and v.pending
  if p then
   active[k]={pid,id}
   if interrupted[k] then cancel(pid,c,s,'生产已中断；本轮取消，未消耗时代机会');v=store.DialogueState(pid,c).value;p=nil
   elseif known and not eligible then cancel(pid,c,s,'资格已失效；本轮取消，未消耗时代机会');v=store.DialogueState(pid,c).value;p=nil
   elseif known then
    local _,matches=queue(c)
    if not matches and p.stage=='ACTIVE' then cancel(pid,c,s,'已改选生产；本轮取消，重新开始需完整一回合');v=store.DialogueState(pid,c).value;p=nil end
   end
  else active[k]=nil end
  local stage=p and p.stage or (v and v.used[e] and 'USED' or eligible and 'AVAILABLE' or 'INELIGIBLE')
  local reason=p and p.reason or (stage=='USED' and '本游戏时代已成功；不可重复' or stage=='AVAILABLE' and '从城市生产列表选择时代对话' or '需要文化身份及ACTIVE III')
  if not known then stage='HELD';reason='当前资格尚不可确认；未清除历史，也不完成项目'
  elseif not p and v and v.last and stage=='AVAILABLE' then reason=v.last.reason..'；可重新选择'end
  local lastGain,lastX
  if v and v.last then for _,r in pairs(v.used)do if r.id==v.last.id then lastGain=r.gain;lastX=r.x end end end
  publish(pid,id,{stage=stage,reason=reason,start=p and p.start,era=p and p.era or e,total=v and v.total or 0,
   used=v and v.used[e]~=nil or false,x=lastX,gain=lastGain,reference=s.reference,token=s.token})
 end
 function d.Flush()
  if not ready or busy then return end;busy=true
  local work=dirty;dirty={}
  for _,v in pairs(work)do safe(v[1],v[2],function()audit(v[1],v[2])end)end
  busy=false
 end
 function d.Refresh(pid,id)mark(pid,id);d.Flush()end
 local advance
 function d.Sync(pid,id,token)
  if not P.IsTestPlayer(pid) or type(id)~='number' or not city(pid,id)then return end
  ready=true;d.Refresh(pid,id);advance(pid,false,id)
  if type(token)=='string' then d.syncAck[key(pid,id)]=token end
 end
 function d.Request(pid,p)
  if not ready or busy or not P.IsTestPlayer(pid) or type(p.CityID)~='number' then return end
  safe(pid,p.CityID,function()
   local c=assert(city(pid,p.CityID),'城市不可读');local s,_,known,eligible=read(pid,c)
   if interrupted[key(pid,p.CityID)] then cancel(pid,c,s,'改选后重新开始');s=store.DialogueState(pid,c)end
   assert(known and eligible,'需要已确认的文化ACTIVE III')
   assert(p.StartTurn==Game.GetCurrentGameTurn(),'启动请求已过期')
   local q,matches=queue(c);assert(matches,'当前目标未确认');assert(type(P.Field(q,'FinishProgress'))=='function','完成接口缺失')
   if s.value and s.value.pending then assert(s.value.pending.stage=='ACTIVE','上次完成尚未确认；请先改选普通目标');return end
   write(pid,c,s,M.Begin(s.value,s.token,s.reference,era(),p.StartTurn));mark(pid,p.CityID)
  end)
  d.Flush()
 end
 local function completion(pid,id,index)
  if not ready or not P.IsTestPlayer(pid)then return end
  local row=P.Info('Projects',index);if not row or row.ProjectType~=PROJECT then return end
  local k=key(pid,id);if settling[k]then return end;settling[k]=true
  safe(pid,id,function()
   local c=assert(city(pid,id));local s,_,known,eligible=read(pid,c);local v=s.value;local p=v and v.pending
   if not p then return end -- repeated native event never creates a start or reward
   if known and not eligible then cancel(pid,c,s,'完成前资格失效；未记奖励或额度');return end
   if p.stage=='HELD' then return end -- never resample a failed completion boundary later
   if p.stage=='CALLING' and (armed[k]~=p.id or Game.GetCurrentGameTurn()~=p.start+1)then
    write(pid,c,s,M.Hold(v,'完成来源已不确定；不重放或补取之后的馆藏'));armed[k]=nil;mark(pid,id);return
   end
   armed[k]=nil -- one completion sample, including a failed permanent commit
   if p.stage=='ACTIVE' then
    local _,stillCurrent=queue(c);assert(not stillCurrent,'提前完成事件尚未退出当前项目；不推断成功')
   end
   local good,sample=pcall(function()
    assert(known,'完成时资格未知')
    local value=assert(ExposedMembers.SPC_DialogueProjectRead,'完成时馆藏读取未就绪')(pid,id,true)
    assert(same(value.reference,s.reference) and value.turn==Game.GetCurrentGameTurn(),'完成时馆藏引用不一致')
    assert(type(value.x)=='number' and value.x%1==0 and value.x>=0 and value.x<=7,'完成时馆藏时代未知')
    local after,_,currentKnown,currentEligible=read(pid,c)
    assert(currentKnown and currentEligible and same(after,s),'完成取样期间状态已变化')
    return value
   end)
   if not good then
    write(pid,c,s,M.Hold(v,'完成时事实未确认；不以之后的馆藏补算'));mark(pid,id);return
   end
   write(pid,c,s,M.Complete(v,p.id,sample.x,sample.turn));active[k]=nil;interrupted[k]=nil;mark(pid,id)
  end)
  settling[k]=nil
 end
 advance=function(pid,ending,onlyID)
  if not ready or busy or not P.IsTestPlayer(pid)then return end
  local work=cp(active)
  for _,v in pairs(work)do if v[1]==pid and (onlyID==nil or onlyID==v[2])then safe(pid,v[2],function()
   local c=assert(city(pid,v[2]));local s,_,known,eligible=read(pid,c);local p=s.value and s.value.pending
   if not p then active[key(pid,v[2])]=nil;return end
   if known and not eligible then cancel(pid,c,s,'资格已失效；本轮取消');return end
   if not known then return end
   local q,matches=queue(c)
   if not matches and p.stage=='ACTIVE' then cancel(pid,c,s,'生产中断；本轮取消');return end
   if p.stage~='ACTIVE' then return end
   local now=Game.GetCurrentGameTurn()
   if ending and now==p.start then
    if not p.ended then write(pid,c,s,M.EndTurn(s.value,now))end
   elseif not ending and now>p.start then
    if now~=p.start+1 or not p.ended then cancel(pid,c,s,'未确认完整生产回合；请重新选择')
    else
     assert(type(P.Field(q,'FinishProgress'))=='function','完成接口缺失')
     write(pid,c,s,M.Calling(s.value,now)) -- persist before native reentry, never replay after load
     local k=key(pid,v[2]);armed[k]=p.id;finishing[k]=true
     local ok,err=pcall(q.FinishProgress,q);finishing[k]=nil;mark(pid,v[2])
     assert(ok,err)
    end
   end
  end)end end
  d.Flush()
 end
 local function production(pid,id)
  if not ready or not P.IsTestPlayer(pid)then return end
  local k=key(pid,id)
  if active[k] and not settling[k]then safe(pid,id,function()
   local c=assert(city(pid,id));local s,_,known,eligible=read(pid,c);local p=s.value and s.value.pending
   if p and known and not eligible then cancel(pid,c,s,'资格已失效；本轮取消')
   elseif p then
    local _,matches=queue(c)
    -- Native completion can publish target change before CityProjectCompleted.
    -- Retain only this publish's interruption latch; no completion => cancel at Flush,
    -- even if the user changed away and back before that flush.
    if not matches and p.stage=='ACTIVE' then interrupted[k]=true
    elseif not matches and (p.stage=='HELD' or p.stage=='CALLING' and not finishing[k])then
     cancel(pid,c,s,'已放弃未确认轮次；历史与额度未增加')end
   end
  end)end
  mark(pid,id)
 end
 function d.Describe(pid,c)
  local s=store.DialogueState(pid,c);local v=s.value;local p=v and v.pending;local e=era()
  local f=shared.EffectiveFacts.Read(pid,c)
  local row=d.views[key(pid,c:GetID())]
  local lines={'时代对话｜'..c:GetName()..'｜项目 / 保存验证',
   '文化资格：'..(f.specialization=='CULTURE' and '文化' or '非文化')..' ACTIVE '..tostring(f.active),
   '累计记录：+'..tostring(v and v.total or 0)..'%（本批尚未接入实际产出）',
   '当前游戏时代：'..Locale.Lookup((P.Info('Eras',e) or {}).Name or e)..'｜机会：'..(v and v.used[e] and '已使用' or '未使用')}
  local readOK,current=pcall(function()
   local x=assert(ExposedMembers.SPC_DialogueProjectRead)(pid,c:GetID(),true)
   assert(same(x.reference,s.reference) and x.turn==Game.GetCurrentGameTurn());return x.x
  end)
  lines[#lines+1]='当前合格馆藏时代：'..(readOK and tostring(current) or '未确认')..'（成功时才取样记账）'
  if p then lines[#lines+1]='本轮：'..p.reason..'｜启动T'..p.start..'｜启动时代：'..Locale.Lookup((P.Info('Eras',p.era) or {}).Name or p.era)
  elseif v and v.last then
   lines[#lines+1]='最近结果：'..v.last.reason
   for _,r in pairs(v.used)do if r.id==v.last.id then lines[#lines+1]='完成时 '..r.x..' 个时代 → 记录 +'..r.gain..' 个百分点'end end
  else lines[#lines+1]='在城市生产列表选择“时代对话”；报告按钮只读。'end
  if row and row.stage=='HELD' then lines[#lines+1]='需要处理：'..row.reason end
  lines[#lines+1]='旧对话收益未在本批替换；请验项目、记录和额度，不按这里的累计值验收益。'
  return table.concat(lines,'\n')
 end
 local function hook(name,fn,optional)
  local e=P.Field(Events,name)
  if optional and not e then return end
  assert(e and type(e.Add)=='function','Dialogue必要事件缺失 '..name);e.Add(fn)
 end
 hook('CityProjectCompleted',completion)
 hook('CityProductionChanged',production)
 hook('CityProductionQueueChanged',production,true)
 hook('GameCoreEventPublishComplete',d.Flush)
 hook('PlayerTurnDeactivated',function(pid)advance(pid,true)end)
 hook('PlayerTurnActivated',function(pid)
  if not ready or not P.IsTestPlayer(pid)then return end
  local ok,e=pcall(era);if ok and e~=lastEra then lastEra=e;markPlayer(pid);d.Flush()end
  advance(pid,false)
 end)
 for _,name in ipairs({'GovernorAssigned','GovernorEstablished','GovernorPromoted','GovernorChanged'})do hook(name,function(pid)
  if not ready then return end
  for p in pairs(Players)do if P.IsTestPlayer(p) and (type(pid)~='number' or pid==p or pid<0)then
   -- Ordered qualification changes cannot be coalesced away across a loss/return burst.
   for _,v in pairs(cp(active))do if v[1]==p then safe(p,v[2],function()audit(p,v[2])end)end end
   markPlayer(p)
  end end
 end,true)end
 hook('CityInitialized',mark,true);hook('CityTransfered',mark,true)
 hook('LoadScreenClose',function()
  ready=true
  for pid in pairs(Players)do if P.IsTestPlayer(pid)then markPlayer(pid)end end
  d.Flush();for pid in pairs(Players)do advance(pid,false)end
 end)
 store.RegisterExit('DialogueProjects',function(c,loss)
  store.RemoveOwned(c,loss,{MARKER})
  for k,row in pairs(d.views)do if row.reference and row.reference.owner==loss.origin.owner
   and row.reference.x==c:GetX() and row.reference.y==c:GetY()then
   active[k]=nil;dirty[k]=nil;interrupted[k]=nil;armed[k]=nil;d.views[k]=nil;d.syncAck[k]=nil
  end end
  d.revision=d.revision+1
 end)
 store.RegisterReturn('DialogueProjects',function(pid,c)mark(pid,c:GetID())end)
 function d.IsBusy()return busy or next(settling)~=nil end
end
