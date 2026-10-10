include('Probe')
include('ExpeditionSpyRead')
local P=SPCP0;local R=SPCExpeditionSpyRead
local current,pending,pendingAction,travel,gain,before,audit,comparison
local targets={};local selected=1;local request;local lastNativePermit
local auditSourceID
local taskBefore,taskAfter,taskEventsBefore,afterPublish
local function taskRead()
 if current and current.unitID and current.targetID then
  return R.TaskRead(Game.GetLocalPlayer(),current.unitID,{owner=current.targetOwner,id=current.targetID,x=current.targetX,y=current.targetY})
 end
end
local missionEvents=0;local lastMission;local observing=false
local function L(k,...)return Locale.Lookup('LOC_SPC_EXPEDITION_SPY_'..k,...)end
local function common(k,...)return Locale.Lookup('LOC_SPC_EXPEDITION_GATE_'..k,...)end
local function value(v)return v==nil and 'UNKNOWN' or tostring(v)end
local function yes(v)return v==nil and 'UNKNOWN' or L(v and 'YES' or 'NO')end
local function setReport(s)
 Controls.Report:SetText(s);Controls.ReportScroll:CalculateSize();Controls.ReportScroll:ReprocessAnchoring()
end
local function render()
 local v=current;if not v then setReport(L('INITIAL'));return end
 local o={L('PHASE_'..v.phase)};local failure=v.error or v.stop
 if failure then o[#o+1]=common('ERROR',failure)end
 o[#o+1]=common('COUNT',v.count or 'UNKNOWN')
 if v.reservedCapacity then o[#o+1]=L('RESERVED',v.observedCount or 'UNKNOWN')end
 if v.unitID then o[#o+1]=common('UNIT',v.unitID,v.x,v.y)end
 if v.legacy or v.unbound then o[#o+1]=L('UNBOUND')end
 if v.sourceName then
  o[#o+1]=v.bound and common('SOURCE',Locale.Lookup(v.sourceName),v.sourceCity)
   or L('RETAINED_SOURCE',Locale.Lookup(v.sourceName),v.sourceCity)
 end
 if v.bound then o[#o+1]=L('BOUND',v.createdID,v.unitID)end
 if v.identity then
  local d=v.identity
  local function status(s)return L('IDENTITY_'..(s or 'UNREADABLE'))end
  o[#o+1]=L('IDENTITY_SUMMARY',status(d.candidateMarker),status(d.lookupMarker),status(d.plotStatus),status(d.sourceStatus))
  if not v.bound then
   o[#o+1]=L('IDENTITY_IDS',value(v.createdID),value(v.trackedID),value(d.candidateID),d.memberCount)
   o[#o+1]=L('IDENTITY_LOOKUPS',value(d.createdLookupID),status(d.createdMarker),value(d.trackedLookupID),status(d.trackedMarker),value(d.candidateLookupID),status(d.lookupMarker))
   o[#o+1]=L('IDENTITY_TURN',d.turn,value(v.dueTurn))
  end
 end
 if v.taskStart then
  o[#o+1]=L('TASK_PROGRESS',v.taskStart,v.taskDue,v.taskCompletions or 0)
  o[#o+1]=L('TASK_ISOLATION',value(taskBefore and taskBefore.sourceTurns),value(taskAfter and taskAfter.sourceTurns),value(taskAfter and taskAfter.operation),missionEvents-(taskEventsBefore or missionEvents))
 end
 if v.phase=='TRAVELLING' then o[#o+1]=L('JOURNEY',Locale.Lookup(v.targetName),v.dueTurn)
 elseif v.coLocated~=nil then o[#o+1]=common('COLOCATED',v.coLocated)end
 if before and audit then
  o[#o+1]=L('AUDIT',value(before.capacity),value(audit.capacity),value(before.normal),value(audit.normal),yes(before.trainable),yes(audit.trainable))
  o[#o+1]=L('CLASSIFIED',value(audit.nativeTotal),L('COMPARE_'..(comparison or 'PARTIAL')))
 end
 if travel then
  o[#o+1]=travel.status=='READ_OK' and L('TIMING',travel.travel,travel.establish,yes(travel.nativeAllowed)) or L('READ_ERROR',travel.error or 'UNKNOWN')
 end
 if gain then
  o[#o+1]=L('GAIN',value(gain.sourceTurns),yes(gain.canStart),value(gain.ESPIONAGE_SUCCESS_UNDETECTED),value(gain.ESPIONAGE_SUCCESS_MUST_ESCAPE))
  o[#o+1]=L('GAIN_BLOCKED')
  if gain.error then o[#o+1]=L('READ_ERROR',gain.error)end
 end
 if observing or missionEvents>0 then o[#o+1]=L('EVENTS',missionEvents,lastMission or 'NONE')end
 if v.errorStep then o[#o+1]=common('FAILURE_STEP',v.errorStep)end
 if v.errorDetail then o[#o+1]=common('FAILURE_DETAIL',v.errorDetail)end
 o[#o+1]=L('STOP_HINT');setReport(table.concat(o,'[NEWLINE]'))
end
local function updateAudit()
 if before then
  audit=R.Audit(Game.GetLocalPlayer(),auditSourceID)
  comparison=R.Compare(before,audit)
 end
end
local function reply()
 if not pending then return end
 local v=ExposedMembers.SPC_ExpeditionGateReply
 if not v or v.owner~=Game.GetLocalPlayer() or v.token~=pending then return end
 local action=pendingAction;pending=nil;pendingAction=nil;ContextPtr:ClearUpdate();current=v
 if action=='CREATE' and not v.error then
  observing=true;missionEvents=0;lastMission=nil;taskBefore=nil;taskAfter=nil;taskEventsBefore=nil;updateAudit();afterPublish=true
  if comparison=='CHANGED' or comparison=='UNKNOWN' then
   request('STOP','ORDINARY_SPY_PREFLIGHT_'..comparison);return true
  end
 elseif action=='DISPATCH' and not v.error and v.nativePermit and v.nativePermit~=lastNativePermit then
  lastNativePermit=v.nativePermit -- Consume before a native request, including exceptions.
  local target={owner=v.targetOwner,id=v.targetID,x=v.targetX,y=v.targetY}
  local ok,err=R.SubmitTravel(v.owner,v.unitID,target,v.nativePermit)
  if not ok then request('STOP',err);return true end
  print('[SPC][B186][N1_SPY_REQUEST] submitted unit='..tostring(v.unitID))
  request('READ');return true
 elseif action=='TASK' and not v.error then taskAfter=taskRead()
 elseif action=='END' and not v.error then
  observing=false;travel=nil;gain=nil;taskBefore=nil;taskAfter=nil;updateAudit();afterPublish=true
 end
 if v.taskStart and v.unitID then taskAfter=taskRead()end
 render();return true
end
local function readChecks()
 if not current or not current.unitID or current.legacy or current.unbound or current.phase=='HELD' then setReport(L('BOUND_REQUIRED'));return false end
 local t=targets[selected];if not t then setReport(common('NO_TARGET'));return false end
 travel=R.Read(Game.GetLocalPlayer(),current.unitID,t)
 gain=R.GainSources(Game.GetLocalPlayer(),current.unitID,t)
 updateAudit();render()
 print('[SPC][B186][N1_SPY_READ] travel='..travel.status..' native='..tostring(travel.nativeAllowed)..' sources='..value(gain.sourceTurns)..' gainAllowed='..yes(gain.canStart)..' undetected='..value(gain.ESPIONAGE_SUCCESS_UNDETECTED)..' detected='..value(gain.ESPIONAGE_SUCCESS_MUST_ESCAPE)..' execution=BLOCKED')
 return travel.status=='READ_OK' and travel.nativeStatus=='KNOWN' and travel.nativeAllowed==true
end
request=function(action,detail)
 if pending then setReport(common('WAIT'));return end
 local pid=Game.GetLocalPlayer();if not P.IsTestPlayer(pid)then return end
 local c=UI.GetHeadSelectedCity();local id=current and (action=='STOP' and current.trackedID or current.unitID)
 if (action=='DISPATCH' or action=='END' or action=='STOP' or action=='TASK') and not id then setReport(common('TEAM_CHANGED'));return end
 if action=='CREATE' then
  if not c or c:GetOwner()~=pid then setReport(common('OWN_CITY'));return end
  auditSourceID=c:GetID();before=R.Audit(pid,auditSourceID);audit=nil;comparison=nil;travel=nil;gain=nil
  if before.status~='KNOWN' then setReport(L('READ_ERROR',before.error or 'CAPACITY_UNKNOWN'));return end
 end
 if action=='TASK' then
  if not current or not current.bound or current.phase~='ARRIVED' then setReport(L('TASK_REQUIRES_ARRIVAL'));return end
  taskBefore=taskRead();taskEventsBefore=missionEvents
  if not taskBefore or taskBefore.status~='KNOWN' or taskBefore.operation~=-1 then setReport(L('TASK_NATIVE_NOT_IDLE'));return end
 end
 if action=='DISPATCH' then
  if not readChecks()then return end
  if comparison=='CHANGED' or comparison=='UNKNOWN' then request('STOP','ORDINARY_SPY_PREFLIGHT_'..comparison);return end
 end
 ExposedMembers.SPC_ExpeditionGateSequence=(ExposedMembers.SPC_ExpeditionGateSequence or 0)+1
 pending='N1:'..P.VERSION..':'..ExposedMembers.SPC_ExpeditionGateSequence;pendingAction=action
 local packet={OnStart='SPC_ExpeditionGateRequest',Token=pending,Action=action,CityID=c and c:GetID(),UnitID=id,Detail=detail}
 if action=='TASK' then packet.SampleTurn=Game.GetCurrentGameTurn();packet.NativeOperation=taskBefore.operation end
 if action=='DISPATCH' then
  packet.SampleTurn=travel.turn;packet.FromX=travel.fromX;packet.FromY=travel.fromY
  packet.TargetOwner=travel.targetOwner;packet.TargetID=travel.targetID;packet.TargetX=travel.targetX;packet.TargetY=travel.targetY
  packet.Travel=travel.travel;packet.Establish=travel.establish;packet.NativeAllowed=travel.nativeAllowed;packet.NativeStatus=travel.nativeStatus
 end
 local ok,err=pcall(UI.RequestPlayerOperation,pid,PlayerOperations.EXECUTE_SCRIPT,packet)
 if not ok then pending=nil;pendingAction=nil;setReport(common('SEND_ERROR',tostring(err)));return end
 setReport(common('WAIT'));if reply()then return end
 local elapsed=0
 ContextPtr:SetUpdate(function(dt)
  elapsed=elapsed+dt;if reply()then return end
  if elapsed>=10 then pending=nil;pendingAction=nil;ContextPtr:ClearUpdate();setReport(common('TIMEOUT'))end
 end)
end
local function updateTarget()
 local t=targets[selected];Controls.TargetLabel:SetText(t and Locale.Lookup(t.name) or common('NO_TARGET'))
end
local function refreshTargets()
 local old=targets[selected];targets=R.Targets(Game.GetLocalPlayer());selected=1
 if old then for i,t in ipairs(targets)do if t.owner==old.owner and t.id==old.id then selected=i;break end end end
 updateTarget()
end
local function close()
 Controls.Window:SetHide(true);ContextPtr:SetHide(true);ExposedMembers.SPC_ExpeditionGateUIOpenVersion=nil
 ContextPtr:ClearUpdate();pending=nil;pendingAction=nil;targets={};travel=nil;gain=nil
end
local function open()
 if not P.IsTestPlayer(Game.GetLocalPlayer())then return end
 ContextPtr:SetHide(false);Controls.Window:SetHide(false)
 if ContextPtr:IsHidden() or Controls.Window:IsHidden()then return end
 refreshTargets();request('READ');ExposedMembers.SPC_ExpeditionGateUIOpenVersion=P.VERSION
end
local function visibility()if not P.IsTestPlayer(Game.GetLocalPlayer())then close()end end
local function missionEvent(pid,id)
 if not observing or not P.IsTestPlayer(pid)then return end
 missionEvents=math.min(99,missionEvents+1)
 local ok,m=pcall(function()return Players[pid]:GetDiplomacy():GetMission(pid,id)end)
 lastMission=ok and type(m)=='table' and tostring(m.Operation):sub(1,40) or 'UNKNOWN'
 -- Player-level event only: never infer ownership from a matching unit name.
 print('[SPC][B186][N1_SPY_EVENT] player='..pid..' mission='..tostring(id)..' operation='..lastMission..' attribution=UNKNOWN')
end
local function published()
 local waiting=afterPublish
 reply()
 if waiting then
  afterPublish=false;updateAudit()
  if current and current.taskStart then taskAfter=taskRead()end
  if not ContextPtr:IsHidden()then render()end
 end
end
local initialized=false
local function initialize()
 if initialized then return end
 Controls.CloseButton:RegisterCallback(Mouse.eLClick,close)
 Controls.CreateButton:RegisterCallback(Mouse.eLClick,function()request('CREATE')end)
 Controls.RefreshButton:RegisterCallback(Mouse.eLClick,function()refreshTargets();updateAudit();request('READ')end)
 Controls.ArmButton:RegisterCallback(Mouse.eLClick,function()request('DISPATCH')end)
 Controls.TaskButton:RegisterCallback(Mouse.eLClick,function()request('TASK')end)
 Controls.EndButton:RegisterCallback(Mouse.eLClick,function()request('END')end)
 Controls.TravelButton:RegisterCallback(Mouse.eLClick,function()if not pending then readChecks()end end)
 local function move(delta)
  if pending then return end
  if #targets>0 then selected=((selected-1+delta)%#targets)+1;travel=nil;gain=nil;updateTarget();render()end
 end
 Controls.PreviousButton:RegisterCallback(Mouse.eLClick,function()move(-1)end)
 Controls.NextButton:RegisterCallback(Mouse.eLClick,function()move(1)end)
 for c,k in pairs({CreateButtonCaption='CREATE',TravelButtonCaption='CHECK',ArmButtonCaption='DISPATCH',TaskButtonCaption='TASK'})do Controls[c]:SetText(L(k))end
 for c,k in pairs({CloseButtonCaption='CLOSE',RefreshButtonCaption='REFRESH',EndButtonCaption='END',PreviousButtonCaption='PREVIOUS',NextButtonCaption='NEXT'})do Controls[c]:SetText(common(k))end
 LuaEvents.SPC_ExpeditionGateOpen.Add(open);Events.LoadScreenClose.Add(visibility);Events.LocalPlayerTurnBegin.Add(visibility)
 Events.GameCoreEventPublishComplete.Add(published)
 if Events.SpyMissionCompleted then Events.SpyMissionCompleted.Add(missionEvent)end
 ContextPtr:SetInputHandler(function(message,key)
  if message==KeyEvents.KeyUp and key==Keys.VK_ESCAPE and not Controls.Window:IsHidden()then close();return true end
  return false
 end,true)
 close();visibility();initialized=true;ExposedMembers.SPC_ExpeditionGateUIVersion=P.VERSION
end
ContextPtr:SetInitHandler(initialize)
ContextPtr:SetShutdown(function()
 close();observing=false
 if initialized then
  LuaEvents.SPC_ExpeditionGateOpen.Remove(open);Events.LoadScreenClose.Remove(visibility);Events.LocalPlayerTurnBegin.Remove(visibility)
  Events.GameCoreEventPublishComplete.Remove(published)
  if Events.SpyMissionCompleted then Events.SpyMissionCompleted.Remove(missionEvent)end
  ExposedMembers.SPC_ExpeditionGateUIVersion=nil;initialized=false
 end
end)
