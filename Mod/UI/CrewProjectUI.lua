include('CrewModel')
-- Read-only native queue/cost/counter surface plus one explicit admission handshake.
-- Existing engine publish events drive the handshake; no timers or frame update.
SPCCrewProjectUI={}
function SPCCrewProjectUI.New(P,send,notify,build)
 local M=SPCCrewModel;local a={};local pending;local revision=-1
 local function localCity(c)return c and c:GetOwner()==Game.GetLocalPlayer() and P.IsTestPlayer(c:GetOwner())end
 local function request(c,action,extra)
  ExposedMembers.SPC_CrewUISequence=(ExposedMembers.SPC_CrewUISequence or 0)+1
  local packet=extra or {};packet.Action=action;packet.CityID=c:GetID();packet.Token='CREW:'..P.VERSION..':'..ExposedMembers.SPC_CrewUISequence;packet.OnStart='SPC_CrewRequest'
  pending.token=packet.Token -- publish callbacks may run during transmission
  send(c:GetOwner(),PlayerOperations.EXECUTE_SCRIPT,packet)
 end
 ExposedMembers.SPC_CrewNativeRead=function(pid,id)
  assert(pid==Game.GetLocalPlayer() and P.IsTestPlayer(pid),'CREW_UI_OWNER')
  local c=assert(Players[pid]:GetCities():FindID(id),'CREW_UI_CITY');assert(c:GetOwner()==pid,'CREW_UI_OWNER')
  local q=c:GetBuildQueue();local n=q:GetSize();assert(M.Int(n) and n<=100,'CREW_QUEUE_SIZE_UNKNOWN')
  local v={owner=pid,city=id,x=c:GetX(),y=c:GetY(),turn=Game.GetCurrentGameTurn(),projects={},completed={},costs={}}
  for i=0,n-1 do
   local e=assert(q:GetAt(i),'CREW_QUEUE_ENTRY_UNKNOWN')
   if e.Directive==CityProductionDirectives.PROJECT then
    local row=assert(GameInfo.Projects[e.ProjectType],'CREW_QUEUE_TYPE_UNKNOWN')
    if M.Parse(row.ProjectType)then v.projects[row.ProjectType]=(v.projects[row.ProjectType] or 0)+1 end
   end
  end
  local stats=Players[pid]:GetStats();assert(stats and stats.GetNumProjectsAdvanced,'CREW_NATIVE_COMPLETION_COUNTER_UNKNOWN')
  for tier in ipairs(M.CAPACITY)do for _,ratio in ipairs(M.RATIOS)do
   local speed=assert(GameInfo.GameSpeeds[GameConfiguration.GetGameSpeedType()],'CREW_SPEED_UNKNOWN').CostMultiplier
   local idp=M.Project(tier,ratio,speed);local row=assert(GameInfo.Projects[idp],'CREW_PROJECT_DEFINITION_MISSING')
   local count=stats:GetNumProjectsAdvanced(row.Index);assert(M.Int(count),'CREW_NATIVE_COMPLETION_COUNTER_UNKNOWN')
   v.completed[idp]=count;v.costs[idp]=q:GetProjectCost(row.Index)
  end end
  return v
 end
 function a.Items(data)
  local c=data.City;if not localCity(c)then return end
  local d=(ExposedMembers.SPC_P0 or {}).CrewProjects;local v=d and d.views[c:GetOwner()..':'..c:GetID()]
  local result={}
  for _,item in ipairs(data.ProjectItems or {})do
   if not M.Parse(item.Type)then result[#result+1]=item
   elseif v and v.allowed[item.Type] and not d.errors[c:GetOwner()..':'..c:GetID()]then
    if pending then item.Disabled=true end
    item.ToolTip=(item.ToolTip or '')..'[NEWLINE]'..Locale.Lookup('LOC_SPC_CREW_FORMATION_HELP')
    if ExposedMembers.SPC_CrewUIError then item.ToolTip=item.ToolTip..'[NEWLINE]'..Locale.Lookup('LOC_SPC_CREW_FORMATION_ERROR',ExposedMembers.SPC_CrewUIError)end
    result[#result+1]=item
   end
  end;data.ProjectItems=result
 end
 function a.Before(c,item,selected)
  if not item or not M.Parse(item.Type)then return true end
  if not localCity(c) or pending or selected then return false end
  pending={pid=c:GetOwner(),city=c:GetID(),item=item,stage='RESERVE',turn=Game.GetCurrentGameTurn()}
  ExposedMembers.SPC_CrewUIError=nil;request(c,'RESERVE',{Project=item.Type});return false
 end
 local function clear(err)
  local p=pending;pending=nil;ExposedMembers.SPC_CrewUIError=err
  if p then notify(p.pid,p.city)end
 end
 function a.Publish()
  local p=pending
  if p then
   local c=Players[p.pid] and Players[p.pid]:GetCities():FindID(p.city)
   if not localCity(c)then clear('CREW_UI_CITY_CHANGED');return end
   local reply=ExposedMembers.SPC_CrewReply
   if reply and reply.token==p.token then
    if reply.error then clear(reply.error);return end
    if p.stage=='RESERVE'then
     p.reservation=reply.reservation;p.before=reply.before;p.base=reply.base
     local selected=UI.GetHeadSelectedCity()
     if not selected or selected:GetID()~=p.city or selected:GetOwner()~=p.pid or Game.GetCurrentGameTurn()~=p.turn then
      p.stage='ACK';request(c,'CANCEL',{Reservation=p.reservation})
     else
      p.stage='BUILD' -- before calling native, so a nested publication cannot issue twice
      local ok,result=pcall(build,c,p.item)
      if not ok or result==false then
       p.stage='ACK';request(c,'CANCEL',{Reservation=p.reservation})
      else p.stage='QUEUE'end
     end
    elseif p.stage=='ACK'then clear();return end
   end
   if p.stage=='QUEUE'then
    -- Observe the native queue on engine publication; never repeat BUILD or
    -- confirm an asynchronous operation merely because Request returned.
    local ok,q=pcall(ExposedMembers.SPC_CrewNativeRead,p.pid,p.city)
    if not ok then clear('CREW_UI_QUEUE_UNREADABLE');return end
    if (q.projects[p.item.Type] or 0)>p.before or (q.completed[p.item.Type] or 0)>p.base then
     p.stage='ACK';request(c,'CONFIRM',{Reservation=p.reservation})
    elseif Game.GetCurrentGameTurn()~=p.turn then
     p.stage='ACK';request(c,'CANCEL',{Reservation=p.reservation}) -- no surviving native order, no command retry
    end
   end
  end
  local d=(ExposedMembers.SPC_P0 or {}).CrewProjects
  if d and revision~=d.revision then
   revision=d.revision;local c=UI.GetHeadSelectedCity();if localCity(c)then notify(c:GetOwner(),c:GetID())end
  end
 end
 return a
end
