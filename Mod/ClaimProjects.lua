-- Four concrete Claim projects. The city progression record owns all saved state.
SPCClaimProjects={}
function SPCClaimProjects.Start(P,shared)
 local store=assert(shared.CityProgressionStore);local cp=SPCCityIdentityRead.Copy
 local d={views={},syncAck={},revision=0,status="等待加载或城市生产面板确认"};shared.ClaimProjects=d
 local turn
 local ready=false;local busy=false;local dirty={};local active={};local derived={};local errors={}
 local kinds={'RESEARCH','CULTURE','INDUSTRY','COMMERCE'};local projects={};local markers={}
 for _,k in ipairs(kinds)do projects['PROJECT_SPC_CLAIM_'..k]=k;markers[#markers+1]='BUILDING_SPC_CLAIM_'..k end
 local function key(pid,id)return tostring(pid)..':'..tostring(id)end
 local function city(pid,id)return Players[pid] and Players[pid]:GetCities():FindID(id)end
 local function mark(pid,id)if P.IsTestPlayer(pid) and type(id)=='number' then dirty[key(pid,id)]={pid,id}end end
 local function publish(pid,id,value)
  local k=key(pid,id);local old=d.views[k]
  local function encode(v)if not v then return ''end;return tostring(v.stage)..'|'..tostring(v.project)..'|'..tostring(v.reason)..'|'..tostring(v.start)end
  if encode(old)~=encode(value)then d.views[k]=value;d.revision=d.revision+1 end
 end
 local function state(c)return store.ClaimState(c:GetOwner(),c)end
 local function queue(c,project)
  local q=c:GetBuildQueue();local ok,target=P.Call(q,'CurrentlyBuilding');assert(ok,'当前生产不可读')
  if target~=project then return q,false end
  local good,n=P.Call(q,'GetSize')
  if not good then
   local read=assert(ExposedMembers.SPC_ClaimQueueRead,'队列读数未就绪')
   local v=read(c:GetOwner(),c:GetID());assert(v.owner==c:GetOwner() and v.id==c:GetID() and v.turn==Game.GetCurrentGameTurn() and v.project==project,'队列读数不匹配');n=v.size
  end
  assert(n==1,'认领必须为唯一当前目标；队列数量='..tostring(n));return q,true
 end
 local function stop(c,s,why)
  if s and s.timer and s.timer.stage=='ACTIVE' then
   local t=cp(s.timer);t.stage='STOPPED';t.reason=why;store.WriteClaimTimer(c:GetOwner(),c,s.timer,t)
  end
 end
 local function audit(pid,id)
  local k=key(pid,id);local c=city(pid,id);active[k]=nil
  if not c or c:GetOwner()~=pid then publish(pid,id,nil);return end
  local ok,s=pcall(state,c)
  -- Access is transient; unknown authority disables access without deleting records.
  for i,kind in ipairs(kinds)do
   local row=assert(P.Info('Buildings',markers[i]),'认领入口定义缺失');local b=c:GetBuildings()
   local has=P.HasBuilding(b,row.Index);assert(type(has)=='boolean','认领入口读取失败')
   local wanted=ok and s and s.eligible and s.set[kind]==true or false
   if has~=wanted then
    if wanted then P.CreateBuilding(c:GetBuildQueue(),row.Index)else P.RemoveBuilding(b,row.Index)end
    assert(P.HasBuilding(b,row.Index)==wanted,'认领入口更新未确认')
   end
  end
  if not ok then publish(pid,id,{stage='STOPPED',reason=tostring(s):gsub('^.-:%d+: ',''):sub(1,160)});return end
  if not s then publish(pid,id,nil);return end
  if s.receipt then publish(pid,id,{stage='COMPLETED',project=s.receipt.project,reason='专业已认领，Potential 1'});return end
  local t=s.timer
  if t and t.stage=='ACTIVE' then
   local good,_,matches=pcall(queue,c,t.project)
   if good and not matches then stop(c,s,'已改选目标；重新选择须完整占用一回合');t=state(c).timer
   elseif not good then publish(pid,id,{stage='STOPPED',project=t.project,reason='当前队列未确认；不完成项目'});active[k]={pid,id};return
   elseif Game.GetCurrentGameTurn()>t.start+1 then stop(c,s,'错过完整回合窗口；请重新选择');t=state(c).timer
   else active[k]={pid,id}end
  end
  if not t and s.eligible then
   local ok,target=P.Call(c:GetBuildQueue(),'CurrentlyBuilding')
   if ok and projects[target] then
    publish(pid,id,{stage='STOPPED',project=target,reason='当前项目没有计时；请先改选普通目标，再重选认领项目，重新占用完整一回合'})
    return
   end
  end
  publish(pid,id,t and {stage=t.stage,project=t.project,start=t.start,reason=t.reason} or {stage='AVAILABLE',reason='选择一个候选项目，完成后认领专业'})
 end
 local function safe(pid,id,fn)
  local ok,err=pcall(fn)
  if not ok then errors[key(pid,id)]=tostring(err);publish(pid,id,{stage='STOPPED',reason=tostring(err):gsub('^.-:%d+: ',''):sub(1,160)})end
  return ok
 end
 function d.Flush()
  if d.startupError or not ready or busy then return end;busy=true
  local work=dirty;dirty={}
  for _,v in pairs(work)do safe(v[1],v[2],function()audit(v[1],v[2])end)end
  local players=derived;derived={}
  for pid in pairs(players)do
   -- Exact existing consumers: fresh facts, never a saved yield or route snapshot.
   for _,name in ipairs({'ResearchSupport','Lv2Housing','Lv2GPP','IndustrySupport','Lv3Support','Lv3Effects','CrewProjects','ResearchInfrastructure','ResearchCross'})do
    local consumer=shared[name];if consumer and consumer.Audit then
     local ok,err=pcall(consumer.Audit,{player=pid});if not ok then print('[SPC][Claim derive] '..name..': '..tostring(err))end
    end
   end
   if shared.NetworkBridge then
    local ok,err=pcall(shared.NetworkBridge.Refresh,pid);if not ok then print('[SPC][Claim network] '..tostring(err))end
   end
  end
  busy=false
 end
 -- One city sync: rehydrate access/timer; settle only a previously saved due timer. Never begin a timer.
 function d.Sync(pid,id,token)
  if d.startupError or busy or not P.IsTestPlayer(pid) or type(id)~='number' then return end
  local c=city(pid,id);if not c or c:GetOwner()~=pid then return end
  ready=true;d.status='已就绪';mark(pid,id);d.Flush()
  turn(pid,false,id)
  if type(token)=='string' then d.syncAck[key(pid,id)]=token end
 end
 function d.Request(pid,p)
  if d.startupError or not ready or busy or not P.IsTestPlayer(pid) or type(p.CityID)~='number' or not projects[p.Project] then return end
  safe(pid,p.CityID,function()
   local c=assert(city(pid,p.CityID),'城市不可读');local s=assert(state(c),'不是候选城市')
   assert(s.eligible and s.set[projects[p.Project]],'不在冻结候选内')
   assert(p.StartTurn==Game.GetCurrentGameTurn(),'选择请求已过期')
   if s.timer and s.timer.stage=='CALLING' then error('上次完成结果尚未确认；不重复调用')end
   if s.timer and s.timer.stage=='ACTIVE' then
    if s.timer.project==p.Project then return end
    stop(c,s,'改选另一认领项目');s=state(c)
   end
   local q,match=queue(c,p.Project);assert(match,'当前目标未确认')
   assert(type(P.Field(q,'FinishProgress'))=='function','完成接口缺失')
   local t={version=1,token=s.token,reference=cp(s.reference),kind=projects[p.Project],project=p.Project,
    start=p.StartTurn,deactivated=false,stage='ACTIVE',reason='1回合；保存读档继续计时'}
   store.WriteClaimTimer(pid,c,s.timer,t);errors[key(pid,p.CityID)]=nil;mark(pid,p.CityID)
  end)
  d.Flush()
 end
 local function district(c,kind)
  local ds=c:GetDistricts();local n=ds:GetNumDistricts();assert(type(n)=='number' and n>=0 and n%1==0 and n<=1024,'区域数量未知')
  local found
  for i=0,n-1 do
   local v=assert(ds:GetDistrictByIndex(i),'区域读取失败');local row=assert(P.Info('Districts',v:GetType()))
   local family=row.DistrictType;local seen={}
   for _=1,32 do
    assert(not seen[family],'区域替换循环');seen[family]=true
    if P.Families[family]then break end
    local parent
    for _,x in ipairs(P.Rows('DistrictReplaces'))do if x.CivUniqueDistrictType==family then assert(not parent or parent==x.ReplacesDistrictType,'区域替换冲突');parent=x.ReplacesDistrictType end end
    if not parent then break end;family=parent
   end
   if P.Families[family]==kind and v:IsComplete() then
    assert(v:GetOwner()==c:GetOwner() and v:GetCity():GetID()==c:GetID() and not found,'区域锚点不唯一')
    found={districtID=v:GetID(),type=row.DistrictType}
   end
  end
  return assert(found,'找不到对应已完成区域；暂停认领')
 end
 local function completed(pid,id,index)
  if d.startupError or not ready or not P.IsTestPlayer(pid)then return end
  local row=P.Info('Projects',index);local kind=row and projects[row.ProjectType];if not kind then return end
  safe(pid,id,function()
   local c=assert(city(pid,id));local s=assert(state(c),'无认领记录')
   if s.receipt then return end
   assert(s.eligible and s.set[kind],'完成事件不在候选内')
   local e=district(c,kind);e.reference=s.reference;e.token=s.token;e.kind=kind;e.project=row.ProjectType;e.turn=Game.GetCurrentGameTurn()
   if store.ClaimComplete(pid,c,e)then derived[pid]=true end
   active[key(pid,id)]=nil;mark(pid,id)
  end)
  -- This can reenter from FinishProgress; Flush is deliberately deferred.
 end
 turn=function(pid,ending,onlyID)
  if d.startupError or not ready or not P.IsTestPlayer(pid)then return end
  local work=cp(active)
  for _,v in pairs(work)do if v[1]==pid and (not onlyID or v[2]==onlyID) then safe(pid,v[2],function()
   local c=assert(city(pid,v[2]));local s=state(c);local t=s and s.timer
   if not t or t.stage~='ACTIVE' then return end
   local q,match=queue(c,t.project)
   if not match then stop(c,s,'当前目标已改变');mark(pid,v[2]);return end
   local now=Game.GetCurrentGameTurn()
   if ending and now==t.start then
    local next=cp(t);next.deactivated=true;store.WriteClaimTimer(pid,c,t,next)
   elseif not ending and now>t.start then
    if now~=t.start+1 or not t.deactivated then stop(c,s,'未确认完整生产回合；请重新选择')
    else
     local next=cp(t);next.stage='CALLING';next.reason='等待原生完成事件；结果未知时不重复调用'
     store.WriteClaimTimer(pid,c,t,next) -- persist before potentially reentrant native call
     q:FinishProgress()
    end
    mark(pid,v[2])
   end
  end)end end
  d.Flush()
 end
 local function hook(name,fn)
  local e=P.Field(Events,name)
  if name=='CityProductionQueueChanged' and not e then return end -- optional native notification; current-target checks remain mandatory
  assert(e and type(e.Add)=='function','Claim必要事件缺失 '..name);e.Add(fn)
 end
 hook('LoadScreenClose',function()
  if d.startupError then return end
  ready=true;d.status="已就绪"
  for pid,player in pairs(Players)do if P.IsTestPlayer(pid)then for _,c in player:GetCities():Members()do mark(pid,c:GetID())end end end
  d.Flush()
  -- A load after the saved end-turn boundary may not emit another activation.
  for pid in pairs(Players)do if P.IsTestPlayer(pid)then turn(pid,false)end end
 end)
 hook('CityProjectCompleted',completed)
 hook('GameCoreEventPublishComplete',d.Flush)
 hook('PlayerTurnDeactivated',function(pid)turn(pid,true)end)
 hook('PlayerTurnActivated',function(pid)turn(pid,false)end)
 for _,name in ipairs({'CityProductionChanged','CityProductionQueueChanged'})do hook(name,function(pid,id)
  if ready and P.IsTestPlayer(pid) and active[key(pid,id)]then safe(pid,id,function()
   local c=assert(city(pid,id));local s=state(c)
   if s and s.timer and s.timer.stage=='ACTIVE' then
    local _,match=queue(c,s.timer.project);if not match then stop(c,s,'已改选目标；需重新占用完整回合')end
   end
  end)end
  mark(pid,id)
 end)end
 for _,name in ipairs({'CityProductionUpdated','CityTransfered','CityInitialized'})do hook(name,mark)end
 local previous=shared.OnPermanentCityWrite
 shared.OnPermanentCityWrite=function(c,reason)if previous then previous(c,reason)end;mark(c:GetOwner(),c:GetID())end
 store.RegisterExit('ClaimProjects',function(c,loss)
  store.RemoveOwned(c,loss,markers)
  local k=key(loss.origin.owner,loss.origin.cityID);active[k]=nil;dirty[k]=nil;publish(loss.origin.owner,loss.origin.cityID,nil)
 end)
end
