include('Probe')
include('ExpeditionSpyRead')
include('ExpeditionSpyUI')
include('InstanceManager')
include('SupportFunctions')
local P=SPCP0;local R=SPCExpeditionSpyRead;local U=SPCExpeditionSpyUI
local viewMode='DIAGNOSTIC';local requestedUnitID;local close
local current,pending,pendingAction,travel,gain,before,audit,comparison
local diagnosticPhase,diagnosticRevision,diagnosticTurn
local targets={};local selected=1;local taskSelected=false;local request;local lastNativePermit
local refreshHeader;local taskDisplay;local previewRow;local districtStrips={}
local naming,nameStage,nameReason,nameObservation
local auditSourceID
local cityRows=InstanceManager:new('SPCExpeditionDestination','DestinationButton',Controls.DestinationStack)
local taskRows=InstanceManager:new('SPCExpeditionMission','MissionButton',Controls.MissionStack)
local normalRows={};local rowGeneration=0
local function noAction()end
local function clearRows()
 rowGeneration=rowGeneration+1
 for _,row in ipairs(normalRows)do row.button:RegisterCallback(Mouse.eLClick,noAction)end
 for _,strip in ipairs(districtStrips)do
  strip.DistrictsScrollLeftButton:RegisterCallback(Mouse.eLClick,noAction)
  strip.DistrictsScrollRightButton:RegisterCallback(Mouse.eLClick,noAction)
  strip.iconPool:ResetInstances()
 end
 districtStrips={};normalRows={};previewRow=nil;cityRows:ResetInstances();taskRows:ResetInstances()
end
-- The selected outline is an overlay, never an input to row sizing. An auto
-- height button with a parent-height brace feeds its previous height back into
-- DoAutoSize. Measure only the text stack (which reserves 24px for the stats).
local function sizeMissionCard(row)
 row.MissionStatsStack:CalculateSize();row.DetailsStack:CalculateSize()
 local height=math.max(76,row.DetailsStack:GetSizeY()+14)
 row.MissionContent:SetSizeY(height);row.MissionButton:SetSizeY(height)
 row.MissionContent:ReprocessAnchoring();row.MissionButton:ReprocessAnchoring()
end
local function resizeSidebar()
 if viewMode=='DIAGNOSTIC' or ContextPtr:IsHidden()then return end
 local _,height=UIManager:GetScreenSizeVal()
 Controls.SlideAnim:SetSizeY(height-30)
 if previewRow then sizeMissionCard(previewRow)end
 Controls.NormalStack:CalculateSize();Controls.NormalScroll:CalculateInternalSize()
 Controls.NormalPreviewStack:CalculateSize();Controls.NormalMissionScroll:CalculateInternalSize()
end
local function screenChanged(kind)
 if kind==SystemUpdateUI.ScreenResize then resizeSidebar()end
end
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
-- Presentation mirror only. A request reply can predate task completion; the
-- Gate's current transition view supplies phase/activity without polling it.
local function activityView()
 local v=ExposedMembers.SPC_ExpeditionActivity
 if not current or type(v)~='table' or v.owner~=Game.GetLocalPlayer() or v.owner~=current.owner
  or v.unitID~=(current.trackedID or current.unitID) or type(current.teamKey)~='string'
  or v.teamKey~=current.teamKey then return nil end
 return v
end
-- Historical samples are never current-state or activity permission authority.
-- Keep both reports exact-key scoped even if an old diagnostic mirror survives.
local function activityDiagnostic(d)
 local a=activityView()
 if not a or type(d)~='table' or type(a.activityKey)~='string' or a.activityKey==''
  or d.owner~=a.owner or d.unitID~=a.unitID or d.teamKey~=a.teamKey or d.activityKey~=a.activityKey then return nil end
 for _,key in ipairs({'expectedName','x','y'})do
  if d[key]~=a[key]then return nil end
 end
 return d
end
local function appendActivityDiagnostic(out)
 local d=activityDiagnostic(ExposedMembers.SPC_ExpeditionActivityDiagnostic);if not d then return end
 local function raw(key)return type(d[key])=='string' and d[key] or 'UNKNOWN' end
 local status=d.eligibilityStatus
 if status~='ALLOWED' and status~='DENIED' then status='UNKNOWN' end
 out[#out+1]=L('DIAGNOSTIC_HEADER',value(d.turn))
 out[#out+1]=L('DIAGNOSTIC_ACTIVITY',raw('activity'),raw('ready'))
 out[#out+1]=L('DIAGNOSTIC_ENUM_A',raw('awake'),raw('hold'))
 out[#out+1]=L('DIAGNOSTIC_ENUM_B',raw('sleep'),raw('operationEnum'))
 out[#out+1]=L('DIAGNOSTIC_SPY',raw('operation'),raw('endTurn'))
 out[#out+1]=L('DIAGNOSTIC_SLEEP_HASH',raw('hash'))
 out[#out+1]=L('DIAGNOSTIC_ELIGIBILITY',L('DIAGNOSTIC_'..status),raw('eligibility'))
end
-- B193: the failed guard has its own sample; do not infer it from startup.
local function appendFailureDiagnostic(out)
 local d=activityDiagnostic(ExposedMembers.SPC_ExpeditionActivityFailureDiagnostic);if not d then return end
 local function raw(key)return type(d[key])=='string' and d[key] or 'UNKNOWN' end
 local phase=d.phase
 if phase~='PRE_REQUEST_GUARD' and phase~='POST_REQUEST_READBACK' and phase~='PENDING_TIMEOUT' then phase='UNKNOWN' end
 local timeout=phase=='PENDING_TIMEOUT'
 out[#out+1]=L(timeout and 'FAILURE_DIAGNOSTIC_TIMEOUT_HEADER' or 'FAILURE_DIAGNOSTIC_HEADER',value(d.turn))
 out[#out+1]=L('FAILURE_DIAGNOSTIC_PHASE',L('FAILURE_DIAGNOSTIC_PHASE_'..phase),raw('reason'))
 if timeout then out[#out+1]=L('FAILURE_DIAGNOSTIC_TIMING',raw('elapsed'),raw('sampledElapsed'),value(d.sampleTurn))end
 out[#out+1]=L(timeout and 'FAILURE_DIAGNOSTIC_TIMEOUT_ACTIVITY' or 'FAILURE_DIAGNOSTIC_ACTIVITY',raw('activity'))
 out[#out+1]=L('FAILURE_DIAGNOSTIC_REQUEST',raw('requested'),raw('sleepAttempted'))
 out[#out+1]=L('DIAGNOSTIC_ENUM_A',raw('awake'),raw('hold'))
 out[#out+1]=L('DIAGNOSTIC_ENUM_B',raw('sleep'),raw('operationEnum'))
 out[#out+1]=L('FAILURE_DIAGNOSTIC_EQUAL_A',raw('equalsAwake'),raw('equalsHold'))
 out[#out+1]=L('FAILURE_DIAGNOSTIC_EQUAL_B',raw('equalsSleep'),raw('equalsOperation'))
end
local function syncActivity()
 local v=activityView();if not v then return end
 current.phase=v.phase or current.phase
 current.activityMode=v.mode;current.activityOwned=v.owned;current.recovering=v.recovering
 current.activityError=v.error;current.activityFailure=v.activityFailure
 current.taskStart=v.taskStart;current.taskDue=v.taskDue;current.taskCompleted=v.taskCompleted;current.taskCompletions=v.taskCompletions
 if v.phase=='HELD' then current.bound=false;current.unbound=true end
end
-- Transition publication is not a fresh identity read. Only a diagnostic reply
-- sampled in this held phase/revision/turn can support a matching-source label.
local function heldDiagnosticCurrent()
 local a=activityView()
 return diagnosticPhase=='HELD' and diagnosticTurn==Game.GetCurrentGameTurn()
  and a~=nil and diagnosticRevision~=nil and diagnosticRevision==a.revision
end
local function activityFailureText(code)
 local category
 if type(code)=='string' then
  if code:find('_TABLE_UNAVAILABLE',1,true) or code:find('_ROW_UNAVAILABLE',1,true) or code:find('_HASH_UNAVAILABLE',1,true)then category='DATA'
  elseif code:find('_API_UNAVAILABLE',1,true) or code=='ACTIVITY_READER_UNAVAILABLE' or code=='ACTIVITY_REQUEST_UNAVAILABLE'then category='API'
  elseif code:find('_NOT_ALLOWED',1,true) or code:find('_REJECTED',1,true)then category='DENIED' end
 end
 return category and L('ACTIVITY_FAILURE',L('ACTIVITY_CAUSE_'..category),code) or L('ACTIVITY_ERROR',code)
end
local function activityLocked()
 local v=activityView()
 return v~=nil and (v.locked==true or v.mode=='SLEEP' or v.mode=='RELEASE' or v.mode=='BLOCKED'
  or v.phase=='TASK_PREPARING' or v.phase=='TASK_RUNNING')
end
-- Normal views are read-only presentation of the same Gate. No native fact
-- collection occurs here; only explicit requests run preflight readers.
local function normalExact()
 local u=UI.GetHeadSelectedUnit()
 return U.IsTeam(u) and u:GetID()==requestedUnitID and current~=nil
  and current.unitID==requestedUnitID and activityView()~=nil
end
local function normalCanAct()
 return normalExact() and current.bound==true and not pending and not naming
  and U.CanOpen(viewMode,UI.GetHeadSelectedUnit())
end
local function setReport(s)
 if viewMode~='DIAGNOSTIC'then
  Controls.NormalFeedback:SetText(s);Controls.NormalFeedback:SetToolTipString(s)
  Controls.NormalPreviewStack:CalculateSize();Controls.NormalMissionScroll:CalculateInternalSize();return
 end
 Controls.Report:SetText(s);Controls.ReportScroll:CalculateSize();Controls.ReportScroll:ReprocessAnchoring()
end
local function failureText(v)
 local code=v.errorDetail or v.activityFailure or v.activityError or v.error or v.stop
 if not code then return nil end
 local key='NORMAL_FAILURE_UNKNOWN'
 if code:find('ORDINARY_SPY_PREFLIGHT',1,true)then key='NORMAL_FAILURE_CREATION'
 elseif code:find('TARGET',1,true)then key='NORMAL_FAILURE_TARGET'
 elseif code:find('TRAVEL_REQUEST',1,true) or code:find('TRAVEL_NOT_ALLOWED',1,true) or code:find('NATIVE_REQUEST',1,true)then key='NORMAL_FAILURE_NATIVE' end
 return L(key)
end
local function renderNormal()
 local exact=normalExact();local v=current
 -- Native SLEEP can clear selection before an immediate task failure arrives.
 -- Keep that exact team's correlated error visible; selection still gates actions.
 local failure=(exact or (v and v.unitID==requestedUnitID and activityView())) and failureText(v) or nil
 local o={}
 if not exact then o[1]=failure or L('NORMAL_SELECTION_CHANGED')
 else
  o[#o+1]=L('NORMAL_TEAM',v.expectedName or L('NORMAL_NAME_UNKNOWN'))
  o[#o+1]=L('NORMAL_SOURCE',v.sourceName and Locale.Lookup(v.sourceName) or L('NORMAL_NAME_UNKNOWN'))
  o[#o+1]=L('NORMAL_PHASE_'..v.phase)
  if v.recovering then o[#o+1]=L('ACTIVITY_RECOVER')end
  if v.targetName then o[#o+1]=L('NORMAL_DESTINATION',Locale.Lookup(v.targetName))end
  if v.phase=='TASK_RUNNING' and v.taskDue then
   o[#o+1]=L('NORMAL_REMAINING',math.max(0,v.taskDue-Game.GetCurrentGameTurn()))
  end
  if v.phase=='TASK_COMPLETE'then o[#o+1]=L('NORMAL_ONE_SHOT')end
  if v.activityFailure or v.activityError or v.error or v.stop then
   o[#o+1]=failureText(v)
  end
 end
 local summary=table.concat(o,'[NEWLINE]')
 Controls.NormalSummary:SetText(summary);Controls.NormalCurrentSlot:SetToolTipString(summary)
 if failure then setReport(failure)
 elseif not exact then setReport(L('NORMAL_SELECTION_CHANGED'))end
 local can=normalCanAct()
 Controls.NormalConfirmButton:SetDisabled(not can or (viewMode=='TRAVEL' and not targets[selected])
  or (viewMode=='TASK' and not taskSelected))
 for _,row in ipairs(normalRows)do
  -- City selection lives in the header. A relocation mission is preview-only.
  row.button:SetDisabled(not can or (row.index==nil and viewMode=='TRAVEL'))
  row.brace:SetHide(row.index~=nil or viewMode~='TASK' or not taskSelected)
 end
 resizeSidebar()
end
local function render()
 syncActivity()
 if viewMode~='DIAGNOSTIC'then renderNormal();return end
 local v=current;if not v then setReport(L('INITIAL'));return end
 local o={L('PHASE_'..v.phase)};local failure=v.error or v.stop
 if v.persistence then o[#o+1]=L('PERSISTENCE',L('PERSISTENCE_'..v.persistence),v.generation or '—')end
 local activityFailure=v.activityFailure or v.activityError
 if activityFailure then o[#o+1]=activityFailureText(activityFailure)end
 appendFailureDiagnostic(o)
 appendActivityDiagnostic(o)
 local held=v.phase=='HELD' and type(v.teamKey)=='string' and v.sourceCity~=nil
 local heldFresh=held and heldDiagnosticCurrent()
 local heldMatch=heldFresh and v.sameUnit==true and v.nameVerified==true and v.identity~=nil and v.identity.sourceStatus=='MATCH'
 if held then o[#o+1]=L(heldMatch and 'HELD_MATCH' or 'HELD_RECHECK')end
 if v.activityMode and (v.taskStart or v.phase=='TASK_PREPARING' or v.activityMode~='NONE')then
  o[#o+1]=L('ACTIVITY_'..v.activityMode)
 end
 if nameStage and not held then o[#o+1]=L('NAME_STAGE',L('NAME_STAGE_'..nameStage),nameReason or '—')end
 if failure and not activityFailure then o[#o+1]=failureText(v);o[#o+1]=common('ERROR',failure)end
 local trainingError=ExposedMembers.SPC_ExpeditionTrainingUIError or ExposedMembers.SPC_ExpeditionTrainingNameError
 if trainingError then o[#o+1]=L('TRAINING_ERROR',trainingError)end
 o[#o+1]=common('COUNT',v.count or 'UNKNOWN')
 if v.reservedCapacity then o[#o+1]=L('RESERVED',v.observedCount or 'UNKNOWN')end
 if v.unitID then o[#o+1]=common('UNIT',v.unitID,v.x,v.y)end
 if not held and (v.legacy or v.unbound)then o[#o+1]=L('UNBOUND')end
 if v.sourceName then
  if held then o[#o+1]=L('HELD_SOURCE',Locale.Lookup(v.sourceName),v.sourceCity)
  else o[#o+1]=v.bound and common('SOURCE',Locale.Lookup(v.sourceName),v.sourceCity)
   or L('RETAINED_SOURCE',Locale.Lookup(v.sourceName),v.sourceCity)end
 end
 if v.namePoolCivilization or v.namePoolCount then o[#o+1]=L('NAME_POOL',value(v.namePoolCivilization),value(v.namePoolCount))end
 if nameObservation then o[#o+1]=L('NAME_OBSERVATION',value(nameObservation.name),value(nameObservation.defaultName),value(nameObservation.poolCount),value(nameObservation.offmapCount))end
 if v.expectedName and (not held or heldFresh)then o[#o+1]=L('NAME_READBACK',v.expectedName,v.observedName or 'UNKNOWN',L(v.nameVerified and 'NAME_VERIFIED' or 'NAME_WAITING'))end
 if v.bound then o[#o+1]=L('BOUND',v.createdID,v.unitID)end
 if v.identity and (not held or heldFresh)then
  local d=v.identity
  local function status(s)return L('IDENTITY_'..(s or 'UNREADABLE'))end
  o[#o+1]=L('IDENTITY_SUMMARY',status(d.candidateName),status(d.lookupName),status(d.plotStatus),status(d.sourceStatus))
  if not v.bound then
   o[#o+1]=L('IDENTITY_IDS',value(v.createdID),value(v.trackedID),value(d.candidateID),d.memberCount)
   o[#o+1]=L('IDENTITY_LOOKUPS',value(d.createdLookupID),status(d.createdName),value(d.trackedLookupID),status(d.trackedName),value(d.candidateLookupID),status(d.lookupName))
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
local function stopName(reason)
 naming=nil;ContextPtr:ClearUpdate();nameReason=reason
 request('STOP',reason)
 return true
end
local function checkName()
 if not naming then return end
 local n=naming
 if ContextPtr:IsHidden() or Game.GetLocalPlayer()~=n.owner or not P.IsTestPlayer(n.owner)then
  naming=nil;ContextPtr:ClearUpdate();return true
 end
 if n.stage=='READINESS' then
  local status,reason=R.NameReadiness(n.owner,n.id)
  local changed=nameReason~=reason;nameReason=reason
  if status=='PENDING' then if changed then render()end;return end
  if status~='READY' then return stopName(reason)end
  -- Only now is the new unit visible in UI. Do not compare a stale post-create
  -- snapshot or submit a command while exact unit identity is still unknown.
  updateAudit();afterPublish=false
  if comparison=='CHANGED' or comparison=='UNKNOWN' then
   return stopName('ORDINARY_SPY_PREFLIGHT_'..comparison)
  end
  n.stage='READING';n.elapsed=0;n.poll=0;nameStage='READING';nameReason=nil
 end
 if n.stage~='READING' then return end
 local observation=R.NativeName(n.owner,n.id)
 if naming~=n then return true end -- A close/shutdown must cancel any later confirmation.
 local changed=not nameObservation or nameObservation.reason~=observation.reason or nameObservation.name~=observation.name
 nameObservation=observation;nameReason=observation.reason
 if observation.status=='PENDING' then if changed then render()end;return end
 if observation.status~='READY' then return stopName(observation.reason)end
 naming=nil;ContextPtr:ClearUpdate();nameStage='GAMEPLAY';nameReason=nil
 -- Gameplay verifies this evidence independently. It remains the only binding
 -- writer; UI never sets a unit name, source binding or persistent Property.
 request('NAME',observation.name)
 return true
end
local function prepareName(v)
 naming={owner=v.owner,id=v.unitID,stage='READINESS',elapsed=0,poll=0}
 nameStage='READINESS';nameReason=nil;nameObservation=nil;render()
 if checkName()then return end
 local n=naming
 ContextPtr:SetUpdate(function(dt)
  if naming~=n then return end
  n.elapsed=n.elapsed+dt;n.poll=n.poll+dt
  if n.elapsed>=10 then
   stopName(n.stage=='READINESS' and ('TEAM_UI_READY_TIMEOUT:'..(nameReason or 'UNKNOWN')) or ('TEAM_NATIVE_NAME_TIMEOUT:'..(nameReason or 'UNKNOWN')));return
  end
  if n.poll>=0.25 then n.poll=0;checkName()end
 end)
end
local function reply()
 if not pending then return end
 local v=ExposedMembers.SPC_ExpeditionGateReply
 if not v or v.owner~=Game.GetLocalPlayer() or v.token~=pending then return end
 local action,token=pendingAction,pending;pending=nil;pendingAction=nil;ContextPtr:ClearUpdate()
 -- Do not mutate the shared request reply when applying current activity facts.
 current={};for key,item in pairs(v)do current[key]=item end
 diagnosticPhase=v.phase;diagnosticRevision=v.activityRevision;diagnosticTurn=v.turn
 if viewMode~='DIAGNOSTIC'then Controls.NormalFeedback:SetText('')end
 if action=='CREATE' and not v.error then
  observing=true;missionEvents=0;lastMission=nil;taskBefore=nil;taskAfter=nil;taskEventsBefore=nil;afterPublish=false
  prepareName(v);return true
 elseif action=='READ' and v.phase=='NAMING' and not v.error then
  prepareName(v);return true
 elseif action=='DISPATCH' and not v.error and v.nativePermit and v.nativePermit~=lastNativePermit then
  lastNativePermit=v.nativePermit -- Consume before a native request, including exceptions.
  local target={owner=v.targetOwner,id=v.targetID,x=v.targetX,y=v.targetY}
  local ok,err=R.SubmitTravel(v.owner,v.unitID,target,v.nativePermit)
  if not ok then request('STOP',err);return true end
  print('[SPC][B191][N1_SPY_REQUEST] submitted unit='..tostring(v.unitID))
  -- Native travel may replace the UnitID. Close this exact-unit view; arrival
  -- requires a new explicit action against the freshly selected team.
  if viewMode=='TRAVEL'then close(true);return true end
  request('READ');return true
 elseif action=='TASK' and not v.error then
  taskAfter=taskRead();syncActivity()
  local a=activityView()
  -- Accepted TASK owns the independent activity lease, not this window. A
  -- synchronous bridge failure can already supersede the preparing reply.
  if viewMode=='TASK' and v.unitID==requestedUnitID and type(v.activityKey)=='string' and v.bound==true
   and (v.phase=='TASK_PREPARING' or v.phase=='TASK_RUNNING') and a and a.activityKey==v.activityKey and a.teamKey==v.teamKey
   and (a.phase=='TASK_PREPARING' or a.phase=='TASK_RUNNING')
   and not v.stop and not v.activityFailure and not a.error and not a.activityFailure then
   close(true);return true
  end
 elseif action=='END' and not v.error then
  observing=false;travel=nil;gain=nil;taskBefore=nil;taskAfter=nil;nameStage=nil;nameReason=nil;nameObservation=nil;updateAudit();afterPublish=true
 end
 if v.nameVerified and v.bound and nameStage then nameStage='CONFIRMED';nameReason=nil end
 if v.taskStart and v.unitID then taskAfter=taskRead()end
 if action=='READ' and viewMode=='TASK' and refreshHeader then
  taskDisplay=nil;refreshHeader()
  if not v.error and not taskSelected then setReport('')end
 end
 render();return true
end
local function readChecks()
 syncActivity()
 if activityLocked()then setReport(L('ACTIVITY_WAIT'));return false end
 if not current or not current.unitID or current.legacy or current.unbound or current.phase=='HELD' then setReport(L('BOUND_REQUIRED'));return false end
 local t=targets[selected];if not t then setReport(common('NO_TARGET'));return false end
 travel=R.Read(Game.GetLocalPlayer(),current.unitID,t)
 if viewMode=='DIAGNOSTIC'then gain=R.GainSources(Game.GetLocalPlayer(),current.unitID,t)end
 updateAudit();render()
 if gain then
  print('[SPC][B191][N1_SPY_READ] travel='..travel.status..' native='..tostring(travel.nativeAllowed)..' sources='..value(gain.sourceTurns)..' gainAllowed='..yes(gain.canStart)..' undetected='..value(gain.ESPIONAGE_SUCCESS_UNDETECTED)..' detected='..value(gain.ESPIONAGE_SUCCESS_MUST_ESCAPE)..' execution=BLOCKED')
 end
 local allowed=travel.status=='READ_OK' and travel.nativeStatus=='KNOWN' and travel.nativeAllowed==true
 if not allowed and viewMode~='DIAGNOSTIC'then setReport(L(travel.nativeStatus=='KNOWN' and travel.nativeAllowed==false and 'NORMAL_FAILURE_NATIVE' or 'NORMAL_PREFLIGHT_UNKNOWN'))end
 return allowed
end
request=function(action,detail)
 syncActivity()
 if viewMode~='DIAGNOSTIC'then
  local expected=viewMode=='TRAVEL' and 'DISPATCH' or 'TASK'
  if action~='READ' and action~='STOP' then
   if action~=expected or not normalCanAct()then setReport(L('ACTION_UNAVAILABLE'));return end
   if action=='DISPATCH' and not targets[selected]then setReport(L('NORMAL_SELECT_CITY'));return end
   if action=='TASK' and not taskSelected then setReport(L('NORMAL_SELECT_TASK'));return end
  end
 end
 if (action=='TASK' or action=='DISPATCH') and activityLocked()then setReport(L('ACTIVITY_WAIT'));return end
 if pending or naming then setReport(common('WAIT'));return end
 local pid=Game.GetLocalPlayer();if not P.IsTestPlayer(pid)then return end
 local c=UI.GetHeadSelectedCity();local id=current and (action=='STOP' and current.trackedID or current.unitID)
 if (action=='DISPATCH' or action=='END' or action=='STOP' or action=='TASK' or action=='NAME') and not id then setReport(common('TEAM_CHANGED'));return end
 if action=='CREATE' then
  if not c or c:GetOwner()~=pid then setReport(common('OWN_CITY'));return end
  auditSourceID=c:GetID();before=R.Audit(pid,auditSourceID);audit=nil;comparison=nil;travel=nil;gain=nil;nameStage=nil;nameReason=nil;nameObservation=nil
  if before.status~='KNOWN' then setReport(L('READ_ERROR',before.error or 'CAPACITY_UNKNOWN'));return end
 end
 if action=='TASK' then
  if not current or not current.bound or current.phase~='ARRIVED' then setReport(L('TASK_REQUIRES_ARRIVAL'));return end
  taskBefore=taskRead();taskEventsBefore=missionEvents
  if not taskBefore or taskBefore.status~='KNOWN' or taskBefore.operation~=-1 then setReport(L('TASK_NATIVE_NOT_IDLE'));return end
 end
 if action=='DISPATCH' then
  if not readChecks()then return end
  -- Creation owns the before/after ordinary-Spy isolation check. Later player
  -- actions may legitimately change that fingerprint/capacity. Keep it as
  -- diagnostics; dispatch authority is the exact current team/target preflight.
 end
 ExposedMembers.SPC_ExpeditionGateSequence=(ExposedMembers.SPC_ExpeditionGateSequence or 0)+1
 pending='N1:'..P.VERSION..':'..ExposedMembers.SPC_ExpeditionGateSequence;pendingAction=action
 local packet={OnStart='SPC_ExpeditionGateRequest',Token=pending,Action=action,CityID=c and c:GetID(),UnitID=id,Detail=detail}
 if action=='NAME' then
  -- Only the READY NativeName path calls NAME; Gameplay validates the current
  -- turn and raw name, while off-map enumeration remains this UI read boundary.
  packet.Name=detail;packet.Detail=nil;packet.NameOffmapChecked=true;packet.NameSampleTurn=Game.GetCurrentGameTurn()
 end
 if action=='TASK' then packet.SampleTurn=Game.GetCurrentGameTurn();packet.NativeOperation=taskBefore.operation end
 if action=='DISPATCH' then
  packet.SampleTurn=travel.turn;packet.FromX=travel.fromX;packet.FromY=travel.fromY
  packet.TargetOwner=travel.targetOwner;packet.TargetID=travel.targetID;packet.TargetX=travel.targetX;packet.TargetY=travel.targetY
  packet.Travel=travel.travel;packet.Establish=travel.establish;packet.NativeAllowed=travel.nativeAllowed;packet.NativeStatus=travel.nativeStatus
 end
 local token=pending
 local ok,err=pcall(UI.RequestPlayerOperation,pid,PlayerOperations.EXECUTE_SCRIPT,packet)
 -- A synchronous publish can consume this reply/start naming, or close can
 -- cancel it. This request must not replace that newer timer or reopen a wait.
 if pending~=token then return end
 if not ok then pending=nil;pendingAction=nil;setReport(common('SEND_ERROR',tostring(err)));return end
 setReport(common('WAIT'));if reply()then return end
 local elapsed=0
 ContextPtr:SetUpdate(function(dt)
  if pending~=token then return end
  elapsed=elapsed+dt;if reply()then return end
  if elapsed>=10 then pending=nil;pendingAction=nil;ContextPtr:ClearUpdate();setReport(common('TIMEOUT'))end
 end)
end
-- Native city-banner/district-strip presentation. Display snapshots are owned
-- by this explicit open and discarded at close. Paging/resize/render do not
-- query the world, and retired callbacks cannot operate on reused rows.
local header={BannerBase=Controls.NormalBannerBase,CityName=Controls.NormalCityName,
 TravelTime=Controls.NormalTravelTime,TravelTimeIcon=Controls.NormalTravelTimeIcon,
 TravelTimeStack=Controls.NormalTravelTimeStack,DistrictInfo=Controls.NormalDistrictInfo,
 LocationNotice=Controls.NormalLocationNotice,
 DistrictIconStack=Controls.NormalDistrictIconStack,
 DistrictsScrollLeftButton=Controls.NormalDistrictsScrollLeftButton,
 DistrictsScrollRightButton=Controls.NormalDistrictsScrollRightButton}
local function paintDistricts(row,items)
 if not row.iconPool then row.iconPool=InstanceManager:new('SPCExpeditionDistrict','DistrictIcon',row.DistrictIconStack)end
 row.iconPool:ResetInstances()
 local icons={};local start=1;local generation=rowGeneration
 for _,item in ipairs(items or {})do
  local icon=row.iconPool:GetInstance().DistrictIcon
  local iconName=item.icon
  if item.kind=='WONDER' then
   -- Native IconManager reports missing atlas sizes with a nil/empty sheet.
   -- This is display-only; a missing individual asset must not hide the site.
   local ok,x,y,sheet=pcall(function()return IconManager:FindIconAtlas(iconName,32)end)
   if not ok or type(sheet)~='string' or sheet=='' then iconName='ICON_DISTRICT_WONDER'end
  end
  icon:SetIcon(iconName);icon:SetToolTipString(Locale.Lookup(item.name));icons[#icons+1]=icon
 end
 local function page(delta)
  if generation~=rowGeneration or ContextPtr:IsHidden()then return end
  start=math.max(1,math.min(math.max(1,#icons-6),start+delta))
  for i,icon in ipairs(icons)do icon:SetHide(i<start or i>start+6)end
  row.DistrictsScrollLeftButton:SetDisabled(start==1)
  row.DistrictsScrollRightButton:SetDisabled(start>=#icons-6)
  row.DistrictIconStack:CalculateSize()
 end
 row.DistrictsScrollLeftButton:SetHide(#icons<=7);row.DistrictsScrollRightButton:SetHide(#icons<=7)
 row.DistrictsScrollLeftButton:RegisterCallback(Mouse.eLClick,function()page(-1)end)
 row.DistrictsScrollRightButton:RegisterCallback(Mouse.eLClick,function()page(1)end)
 -- Header can be refreshed more than once; own each pool only once per open.
 local seen=false;for _,strip in ipairs(districtStrips)do if strip==row then seen=true;break end end
 if not seen then districtStrips[#districtStrips+1]=row end
 page(0)
end
local function paintCity(row,display,showTime)
 local valid=display and display.owner~=nil
 local incomplete=valid and display.locationStatus~='READABLE'
 row.LocationNotice:SetHide(not incomplete)
 row.LocationNotice:SetText(incomplete and L('NORMAL_LOCATIONS_INCOMPLETE') or '')
 row.LocationNotice:SetToolTipString(incomplete and L('NORMAL_LOCATIONS_INCOMPLETE_TT') or '')
 row.DistrictInfo:SetToolTipString(incomplete and L('NORMAL_LOCATIONS_INCOMPLETE_TT') or '')
 if row.DestinationButton then
  -- Only incomplete rows need a short second line beneath the icon strip.
  row.DestinationButton:SetSizeY(incomplete and 90 or 72)
  row.DistrictInfo:SetOffsetY(incomplete and 24 or 6)
  row.DistrictsScrollLeftButton:SetOffsetY(incomplete and 28 or 10)
  row.DistrictsScrollRightButton:SetOffsetY(incomplete and 28 or 10)
 end
 row.BannerBase:SetHide(not valid);row.DistrictInfo:SetHide(not valid)
 row.TravelTimeStack:SetHide(not valid or not showTime)
 if not valid then paintDistricts(row,{});return end
 local back,front=UI.GetPlayerColors(display.owner)
 row.BannerBase:SetColor(back);row.CityName:SetColor(front)
 TruncateStringWithTooltip(row.CityName,185,'[ICON_Capital] '..Locale.Lookup(display.name))
 row.TravelTime:SetColor(front);row.TravelTimeIcon:SetColor(front)
 row.TravelTime:SetText(display.total and tostring(display.total) or '?')
 row.BannerBase:SetToolTipString(display.total and Locale.Lookup('LOC_ESPIONAGECHOOSER_TRAVEL_TIME_TOOLTIP',display.travel,display.establish) or L('NORMAL_TIMING_UNKNOWN'))
 paintDistricts(row,display.districts)
end
refreshHeader=function()
 if viewMode=='DIAGNOSTIC'then return end
 local display
 if viewMode=='TRAVEL'then display=targets[selected] and targets[selected].display
 elseif current and current.targetID and current.unitID==requestedUnitID then
  if not taskDisplay then
   taskDisplay=R.Presentation(Game.GetLocalPlayer(),requestedUnitID,
    {owner=current.targetOwner,id=current.targetID,x=current.targetX,y=current.targetY})
  end
  display=taskDisplay
 end
 paintCity(header,display,viewMode=='TRAVEL')
 Controls.NormalEmptyLabel:SetHide(display~=nil and display.owner~=nil)
 Controls.NormalEmptyLabel:SetText(viewMode=='TRAVEL' and #targets>0 and L('NORMAL_SELECT_CITY') or common('NO_TARGET'))
 Controls.NormalMissionGrid:SetHide(viewMode=='TRAVEL' and not targets[selected])
 if previewRow then
  TruncateStringWithTooltip(previewRow.MissionLocation,135,display and display.name and Locale.Lookup(display.name) or L('NORMAL_NAME_UNKNOWN'))
  previewRow.MissionTurns:SetText('2')
  sizeMissionCard(previewRow)
 end
end
local function updateTarget()
 local t=targets[selected];local label=t and Locale.Lookup(t.name) or common('NO_TARGET')
 Controls.TargetLabel:SetText(label)
 if viewMode=='TRAVEL'then TruncateStringWithTooltip(Controls.NormalTargetLabel,250,label);refreshHeader()end
end
local function populateSidebar()
 clearRows()
 Controls.NormalScroll:SetHide(viewMode~='TRAVEL')
 Controls.DestinationStack:SetHide(viewMode~='TRAVEL');Controls.MissionStack:SetHide(false)
 Controls.NormalMissionGrid:SetOffsetX(viewMode=='TRAVEL' and 296 or 0)
 Controls.NormalDrawerTitle:SetText(L(viewMode=='TRAVEL' and 'NORMAL_MISSION_PREVIEW' or 'ACTION_TASK'))
 local generation,id=rowGeneration,requestedUnitID
 if viewMode=='TRAVEL'then
  for index,target in ipairs(targets)do
   local row=cityRows:GetInstance();local owner,cityID=target.owner,target.id
   target.display=R.Presentation(Game.GetLocalPlayer(),id,target)
   paintCity(row,target.display,true)
   local config=PlayerConfigurations and PlayerConfigurations[owner]
   local civType=config and config:GetCivilizationTypeName()
   local civ=civType and GameInfo.Civilizations and GameInfo.Civilizations[civType]
   row.DestinationButton:SetToolTipString(civ and Locale.Lookup(civ.Name) or L('SIDEBAR_CIV_UNKNOWN'))
   normalRows[#normalRows+1]={button=row.DestinationButton,brace=row.SelectorBrace,index=index}
   row.DestinationButton:RegisterCallback(Mouse.eLClick,function()
    if generation~=rowGeneration or requestedUnitID~=id or viewMode~='TRAVEL' or not normalCanAct()
     or targets[index]~=target or target.owner~=owner or target.id~=cityID then return end
    selected=index;travel=nil;gain=nil;updateTarget();setReport('');render()
   end)
  end
 end
 local row=taskRows:GetInstance();previewRow=row
 row.MissionIcon:SetIcon('ICON_UNITOPERATION_SPY_GAIN_SOURCES')
 row.MissionName:SetText(L('SIDEBAR_TASK_NAME'))
 row.MissionDetails:SetText(L(viewMode=='TRAVEL' and 'NORMAL_MISSION_PREVIEW_DETAILS' or 'SIDEBAR_TASK_DETAILS'))
 normalRows[#normalRows+1]={button=row.MissionButton,brace=row.SelectorBrace}
 row.MissionButton:RegisterCallback(Mouse.eLClick,function()
  if generation~=rowGeneration or requestedUnitID~=id or viewMode~='TASK' or not normalCanAct()then return end
  taskSelected=true;setReport('');render()
 end)
 refreshHeader()
end
local function refreshTargets()
 local old=viewMode=='DIAGNOSTIC' and targets[selected] or nil
 targets=R.Targets(Game.GetLocalPlayer());selected=viewMode=='DIAGNOSTIC' and 1 or nil
 if old then for i,t in ipairs(targets)do if t.owner==old.owner and t.id==old.id then selected=i;break end end end
 updateTarget()
end
close=function(force)
 -- Do not cancel the UI half of an accepted dispatch while its permit reply
 -- is in flight. This window does not own or cancel the independent task.
 if not force and viewMode~='DIAGNOSTIC' and (pendingAction=='DISPATCH' or pendingAction=='TASK')then
  setReport(common('WAIT'));return false
 end
 if naming or pendingAction=='CREATE' then nameStage='CANCELLED';nameReason='UI_NAME_WAIT_CANCELLED' end
 -- Hide immediately only after the pending-action guard. The native generic
 -- close animation callback must not bypass our request acknowledgement.
 clearRows();Controls.SlideAnim:Stop()
 Controls.Window:SetHide(true);ContextPtr:SetHide(true);ExposedMembers.SPC_ExpeditionGateUIOpenVersion=nil
 ContextPtr:ClearUpdate();pending=nil;pendingAction=nil;naming=nil;afterPublish=false;targets={};travel=nil;gain=nil
 requestedUnitID=nil;taskDisplay=nil;selected=nil;taskSelected=false;return true
end
local function open(mode,id)
 if not P.IsTestPlayer(Game.GetLocalPlayer()) or pending or naming then return end
 if mode~=nil and mode~='TRAVEL' and mode~='TASK'then return end
 if mode then
  local u=UI.GetHeadSelectedUnit()
  if not U.IsTeam(u) or u:GetID()~=id or not U.CanOpen(mode,u)then return end
 end
 viewMode=mode or 'DIAGNOSTIC';requestedUnitID=mode and id or nil;taskDisplay=nil
 if mode then selected=nil end;taskSelected=false
 Controls.DiagnosticPanel:SetHide(mode~=nil);Controls.NormalPanel:SetHide(mode==nil)
 Controls.TitleLabel:SetText(mode and L('ACTION_'..mode) or L('TITLE'))
 if mode then
  Controls.Title:SetText(L('ACTION_'..mode))
  Controls.NormalIntro:SetText(L(mode=='TRAVEL' and 'SIDEBAR_TRAVEL_HINT' or 'SIDEBAR_TASK_HINT'))
  Controls.NormalConfirmLabel:SetText(L(mode=='TASK' and 'NORMAL_START_TASK' or 'NORMAL_TRAVEL_CONFIRM'))
  Controls.NormalConfirmIcon:SetIcon(mode=='TRAVEL' and 'ICON_UNITOPERATION_SPY_TRAVEL_NEW_CITY' or 'ICON_UNITOPERATION_SPY_GAIN_SOURCES')
  Controls.NormalTargetLabel:SetHide(true);setReport('')
  -- Do not enable a control from a previous diagnostic reply.
  current=nil;Controls.NormalConfirmButton:SetDisabled(true)
 end
 ContextPtr:SetHide(false);Controls.Window:SetHide(false)
 if ContextPtr:IsHidden() or Controls.Window:IsHidden()then return end
 if mode~='TASK'then refreshTargets()end
 if mode then
  populateSidebar();resizeSidebar();Controls.SlideAnim:SetToBeginning();Controls.SlideAnim:Play()
 end
 request('READ');ExposedMembers.SPC_ExpeditionGateUIOpenVersion=P.VERSION
end
local function visibility()
 if not P.IsTestPlayer(Game.GetLocalPlayer())then close(true)
 elseif not ContextPtr:IsHidden() and viewMode~='DIAGNOSTIC'then render()end
end
local function missionEvent(pid,id)
 if not observing or not P.IsTestPlayer(pid)then return end
 missionEvents=math.min(99,missionEvents+1)
 local ok,m=pcall(function()return Players[pid]:GetDiplomacy():GetMission(pid,id)end)
 lastMission=ok and type(m)=='table' and tostring(m.Operation):sub(1,40) or 'UNKNOWN'
 -- Player-level event only: never infer ownership from a matching unit name.
 print('[SPC][B191][N1_SPY_EVENT] player='..pid..' mission='..tostring(id)..' operation='..lastMission..' attribution=UNKNOWN')
end
local function published()
 if naming and checkName()then return end
 local waiting=afterPublish
 reply()
 if waiting then
  afterPublish=false;updateAudit()
  if current and current.taskStart then taskAfter=taskRead()end
  if not ContextPtr:IsHidden()then render()end
 end
end
local function activityChanged()
 if ContextPtr:IsHidden() or not activityView()then return end
 syncActivity()
 if current.taskStart then taskAfter=taskRead()end
 render()
end
local initialized=false
local function initialize()
 if initialized then return end
 Controls.CloseButton:RegisterCallback(Mouse.eLClick,function()close()end)
 Controls.NormalCloseButton:RegisterCallback(Mouse.eLClick,function()close()end)
 Controls.NormalCancelButton:RegisterCallback(Mouse.eLClick,function()close()end)
 Controls.CreateButton:RegisterCallback(Mouse.eLClick,function()if viewMode=='DIAGNOSTIC'then request('CREATE')end end)
 Controls.RefreshButton:RegisterCallback(Mouse.eLClick,function()if viewMode=='DIAGNOSTIC'then refreshTargets();updateAudit();request('READ')end end)
 Controls.ArmButton:RegisterCallback(Mouse.eLClick,function()if viewMode=='DIAGNOSTIC'then request('DISPATCH')end end)
 Controls.TaskButton:RegisterCallback(Mouse.eLClick,function()if viewMode=='DIAGNOSTIC'then request('TASK')end end)
 Controls.EndButton:RegisterCallback(Mouse.eLClick,function()if viewMode=='DIAGNOSTIC'then request('END')end end)
 Controls.TravelButton:RegisterCallback(Mouse.eLClick,function()if viewMode=='DIAGNOSTIC' and not pending and not naming then readChecks()end end)
 local function move(delta)
  if pending or naming or (viewMode~='DIAGNOSTIC' and (viewMode~='TRAVEL' or not normalCanAct()))then return end
  if #targets>0 then selected=((selected-1+delta)%#targets)+1;travel=nil;gain=nil;updateTarget();render()end
 end
 Controls.PreviousButton:RegisterCallback(Mouse.eLClick,function()if viewMode=='DIAGNOSTIC'then move(-1)end end)
 Controls.NextButton:RegisterCallback(Mouse.eLClick,function()if viewMode=='DIAGNOSTIC'then move(1)end end)
 Controls.NormalConfirmButton:RegisterCallback(Mouse.eLClick,function()
  if viewMode=='DIAGNOSTIC' or not normalCanAct()then return end
  request(viewMode=='TRAVEL' and 'DISPATCH' or 'TASK')
 end)
 for c,k in pairs({CreateButtonCaption='CREATE',TravelButtonCaption='CHECK',ArmButtonCaption='DISPATCH',TaskButtonCaption='TASK'})do Controls[c]:SetText(L(k))end
 for c,k in pairs({CloseButtonCaption='CLOSE',RefreshButtonCaption='REFRESH',EndButtonCaption='END',PreviousButtonCaption='PREVIOUS',NextButtonCaption='NEXT'})do Controls[c]:SetText(common(k))end
 LuaEvents.SPC_ExpeditionGateOpen.Add(open);Events.LoadScreenClose.Add(visibility);Events.LocalPlayerTurnBegin.Add(visibility)
 Events.GameCoreEventPublishComplete.Add(published)
 LuaEvents.SPC_ExpeditionActivityChanged.Add(activityChanged)
 if Events.SpyMissionCompleted then Events.SpyMissionCompleted.Add(missionEvent)end
 Events.SystemUpdateUI.Add(screenChanged)
 ContextPtr:SetInputHandler(function(message,key)
  -- Native input uses an InputStruct; retain the existing legacy signature too.
  if type(message)=='table' or type(message)=='userdata'then
   key=message:GetKey();message=message:GetMessageType()
  end
  if message==KeyEvents.KeyUp and key==Keys.VK_ESCAPE and not Controls.Window:IsHidden()then close();return true end
  return false
 end,true)
 close();visibility();initialized=true;ExposedMembers.SPC_ExpeditionGateUIVersion=P.VERSION
end
ContextPtr:SetInitHandler(initialize)
ContextPtr:SetShutdown(function()
 close(true);observing=false
 if initialized then
  Events.SystemUpdateUI.Remove(screenChanged)
  LuaEvents.SPC_ExpeditionGateOpen.Remove(open);Events.LoadScreenClose.Remove(visibility);Events.LocalPlayerTurnBegin.Remove(visibility)
  Events.GameCoreEventPublishComplete.Remove(published)
  LuaEvents.SPC_ExpeditionActivityChanged.Remove(activityChanged)
  if Events.SpyMissionCompleted then Events.SpyMissionCompleted.Remove(missionEvent)end
  ExposedMembers.SPC_ExpeditionGateUIVersion=nil;initialized=false
 end
end)
