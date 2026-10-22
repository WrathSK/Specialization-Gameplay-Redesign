-- B120: one selected real project, session-only evidence; never writes production.
SPCProjectTurnObservation={}
function SPCProjectTurnObservation.Start(P,shared)
 local api={};shared.ProjectTurnObservation=api
 local s=nil;local missing={};local project="PROJECT_SPC_OVERFLOW_SINK_TEST"
 local function publish()
  if not s then shared.ProjectTurnEvidence=nil;return end
  local rows={};for i,v in ipairs(s.rows) do rows[i]=v end
  shared.ProjectTurnEvidence={token=s.token,owner=s.owner,id=s.id,start=s.start,status=s.status,reason=s.reason,rows=rows,missing=table.concat(missing,", ")}
 end
 local function stop(reason) s.status="STOPPED";s.reason=reason;publish() end
 local function sample(name)
  if not s or s.status~="ACTIVE" then return end
  if #s.rows>=32 then stop("超过32条，停止；证据不完整");return end
  local turn=Game.GetCurrentGameTurn()
  if turn>s.start+1 or turn<s.start then stop("超过一次回合观察窗口");return end
  local ok,err=pcall(function()
   assert(P.IsTestPlayer(s.owner),"玩家资格失效")
   local c=Players[s.owner] and Players[s.owner]:GetCities():FindID(s.id)
   assert(c and c:GetOwner()==s.owner and c:GetX()==s.x and c:GetY()==s.y,"城市移除/易主/引用变化")
   local q=c:GetBuildQueue();local readable,target=P.Call(q,"CurrentlyBuilding")
   assert(readable,"Gameplay目标未知")
   local text="T"..turn.." "..name.." | GP="..(target==project and "承接项目" or tostring(target))
   local reader=ExposedMembers.SPC_ProjectTurnRead
   local rok,v=pcall(function()assert(type(reader)=="function");return reader(s.owner,s.id)end)
   if rok and type(v)=="table" and v.owner==s.owner and v.id==s.id and v.turn==turn then
    text=text.." | UI缓存="..tostring(v.value).." 队列="..tostring(v.size).." 目标="..tostring(v.isProject)
   else text=text.." | UI=UNKNOWN" end
   s.rows[#s.rows+1]=text
   if target~=project then s.status="ENDED";s.reason="项目已离开当前目标；这是观察结果，不自动判断完成/取消" end
  end)
  if not ok then stop(tostring(err):match("[^\r\n]+") or "读取失败") end
  publish()
 end
 local function hook(source,name,label,cityEvent)
  local e=P.Field(source,name)
  if not e or not e.Add then missing[#missing+1]=name;return end
  e.Add(function(pid,cid,...)
   if not s or s.status~="ACTIVE" or pid~=s.owner or (cityEvent and cid~=s.id) then return end
   local tail={}
   for i=1,math.min(select("#",...),3) do tail[#tail+1]=tostring(select(i,...)) end
   sample(label..(#tail>0 and ("("..table.concat(tail,",")..")") or ""))
  end)
 end
 hook(Events,"CityProductionChanged","目标变化",true)
 hook(Events,"CityProductionQueueChanged","队列变化",true)
 hook(Events,"CityProductionUpdated","生产更新",true)
 hook(Events,"CityProductionCompleted","生产完成通知",true)
 hook(Events,"PlayerTurnDeactivated","玩家回合结束",false)
 hook(GameEvents,"PlayerTurnStarted","回合Started",false)
 hook(Events,"PlayerTurnActivated","回合Activated",false)
 hook(GameEvents,"PlayerTurnStartComplete","回合StartComplete",false)
 local removed=P.Field(Events,"CityRemovedFromMap")
 if removed and removed.Add then removed.Add(function(pid,cid)
  if s and s.status=="ACTIVE" and pid==s.owner and cid==s.id then stop("城市移除/易主，停止观察") end
 end) else missing[#missing+1]="CityRemovedFromMap" end
 function api.Request(pid,p)
  if p.Action=="PROJECT_TURN_END" then
   if not s or pid~=s.owner or p.Token~=s.token or p.CityID~=s.id then return end
   sample("手动报告终点")
   if s.status=="ACTIVE" then s.status="ENDED";s.reason="只读观察结束；没有自动完成/发奖" end
   publish();return
  end
  if p.Action~="PROJECT_TURN_BEGIN" then return end
  if s and (s.status=="ACTIVE" or s.token==p.Token) then return end
  s={token=p.Token,owner=pid,id=p.CityID,start=p.StartTurn,status="STOPPED",rows={}}
  local ok,err=pcall(function()
   assert(P.IsTestPlayer(pid) and p.StartTurn==Game.GetCurrentGameTurn(),"请求过期/玩家无效")
   local c=assert(Players[pid]:GetCities():FindID(p.CityID),"城市不存在")
   s.x=c:GetX();s.y=c:GetY()
   assert(c:GetOwner()==pid,"城市非己方")
   local readable,target=P.Call(c:GetBuildQueue(),"CurrentlyBuilding")
   assert(readable and target==project,"请先选择承接实验为当前目标")
   local reader=assert(ExposedMembers.SPC_ProjectTurnRead,"UI接口未载入")
   local v=reader(pid,p.CityID)
   assert(v.owner==pid and v.id==p.CityID and v.turn==s.start and v.isProject and v.size==1,"UI目标/唯一队列未确认")
   assert(#missing==0,"必要事件缺失："..table.concat(missing,", "))
   s.status="ACTIVE";s.reason="正常结束回合；恢复操作后左键结束观察/报告"
   sample("开启")
  end)
  if not ok then stop(tostring(err):match("[^\r\n]+") or "开始失败") end
  publish()
 end
 publish()
end
