-- Native UnitPanel adapter. Event/request replies only; no frame callback or timer.
SPCRestructuringUI={KIND='UNIT_SPC_RESTRUCTURING_TEAM'}
local M=SPCRestructuringUI
local serial=0
local pending -- One packet of scalars for this UI context; never a native object.
local function view(u)
 local v=(ExposedMembers.SPC_RestructuringViews or {})[u:GetOwner()..':'..u:GetID()]
 if type(v)=='table' and v.owner==u:GetOwner() and v.unit==u:GetID()
  and v.x==u:GetX() and v.y==u:GetY() and v.turn==Game.GetCurrentGameTurn()then return v end
end
local function awaiting()
 if pending then
  local reply=ExposedMembers.SPC_RestructuringReply
  local v=(ExposedMembers.SPC_RestructuringViews or {})[pending.owner..':'..pending.unit]
  -- A published matching plan is also a prepare ACK. A missing confirm ACK
  -- never becomes permission to resend, including after a transport exception.
  if reply and reply.owner==pending.owner and reply.unit==pending.unit and reply.token==pending.token
   or pending.action=='REST_PREPARE' and type(v)=='table' and v.owner==pending.owner and v.unit==pending.unit and v.prepared==pending.token then pending=nil end
 end
 return pending~=nil
end
function M.IsTeam(u)
 local row=u and GameInfo.Units[u:GetUnitType()]
 return row and row.UnitType==M.KIND and u:GetOwner()==Game.GetLocalPlayer() or false
end
function M.Request(action,u,plan)
 if not M.IsTeam(u)then return end
 if action~='REST_READ' and awaiting()then return end
 serial=serial+1
 local token='REST_UI:'..u:GetID()..':'..serial..':'..Game.GetCurrentGameTurn()
 local packet={OnStart='SPC_P0_Request',Action=action,UnitID=u:GetID(),Token=token,PlanToken=plan}
 if action~='REST_READ'then pending={owner=u:GetOwner(),unit=u:GetID(),token=token,action=action}end
 -- A false return or exception is not proof that Gameplay did not receive it.
 local ok=pcall(UI.RequestPlayerOperation,u:GetOwner(),PlayerOperations.EXECUTE_SCRIPT,packet)
 return ok and token or nil
end
function M.SelectedChanged()
 local u=UI.GetHeadSelectedUnit();if M.IsTeam(u)then M.Request('REST_READ',u)end
end
function M.Actions(u,actions)
 -- Native rendering, margins and idle/movement controls stay owned by UnitPanel.
 -- Remove DELETE and block the matching command callback/hotkey below.
 local row=GameInfo.UnitCommands.UNITCOMMAND_DELETE
 for category,entries in pairs(actions)do if category~='displayOrder' and type(entries)=='table'then
  for i=#entries,1,-1 do if row and entries[i].userTag==row.Hash then table.remove(entries,i)end end
 end end
 local v=view(u);local waiting=awaiting()
 local uid=u:GetID();local label=Locale.Lookup(v and v.action=='CONFIGURE' and 'LOC_SPC_REST_CONFIGURE' or 'LOC_SPC_REST_LIQUIDATE')
 local tip=label..'[NEWLINE]'
 if v and v.cityName then
  tip=tip..Locale.Lookup(v.action=='CONFIGURE' and 'LOC_SPC_REST_WAIT' or 'LOC_SPC_REST_PREVIEW',v.cityName,v.potential,v.remaining or 0)
 else tip=tip..Locale.Lookup('LOC_SPC_REST_MOVE')end
 if v and v.reason then
  local normal={REST_FIVE_FULL_TURNS_REQUIRED='WAIT_GATE',REST_MOVE_TO_SPECIALTY_DISTRICT='MOVE',REST_CURRENT_SPECIALTY_DISTRICT_REQUIRED='CURRENT_SITE',REST_DIFFERENT_IDENTITY_REQUIRED='OTHER_SITE',REST_SAME_CITY_REQUIRED='SAME_CITY',REST_POTENTIAL_TWO_REQUIRED='POTENTIAL_GATE'}
  local message=normal[v.reason];tip=tip..'[NEWLINE]'..Locale.Lookup('LOC_SPC_REST_'..(message or 'PENDING'))..(not message and (' ('..v.reason..')') or '')
 end
 local reply=ExposedMembers.SPC_RestructuringReply
 if reply and reply.unit==uid and reply.owner==u:GetOwner() and not reply.ok then tip=tip..'[NEWLINE]'..Locale.Lookup('LOC_SPC_REST_PENDING')..' ('..tostring(reply.reason)..')'end
 if waiting then tip=tip..'[NEWLINE]'..Locale.Lookup('LOC_SPC_REST_PENDING')end
 local owner=u:GetOwner()
 local x,y,turn=u:GetX(),u:GetY(),Game.GetCurrentGameTurn()
 local action,identity,city,prepared=v and v.action,v and v.uid,v and v.city,v and v.prepared
 local function click(confirm)
  local selected=UI.GetHeadSelectedUnit()
  if not M.IsTeam(selected) or selected:GetOwner()~=owner or selected:GetID()~=uid
   or selected:GetX()~=x or selected:GetY()~=y or Game.GetCurrentGameTurn()~=turn or g_isOkayToProcess~=true then return end
  local fresh=view(selected)
  if not fresh or not fresh.legal or fresh.action~=action or fresh.uid~=identity or fresh.city~=city
   or fresh.prepared~=prepared or awaiting()then return end
  if confirm then
   if not prepared then return end
  elseif prepared then return end -- A stays hoverable/informational after preparation.
  M.Request(confirm and 'REST_CONFIRM' or 'REST_PREPARE',selected,confirm and prepared or nil)
 end
 local icon=v and v.action=='CONFIGURE' and 'ICON_SPC_RAW_CONFIGURE' or 'ICON_SPC_RAW_LIQUIDATE'
 -- Native StandardActionsStack grows Right. Insert B before A so A keeps its
 -- original right-hand slot and B grows to the left; do not swap callback roles.
 if prepared then
  AddActionToTable(actions,{CategoryInUI='SPECIFIC',Icon=icon},not v.legal or waiting,
   Locale.Lookup('LOC_SPC_REST_CONFIRM',label)..'[NEWLINE]'..tip,-248,function()click(true)end)
 end
 AddActionToTable(actions,{CategoryInUI='SPECIFIC',Icon=icon},not(v and v.legal) or waiting,tip,-247,function()click(false)end)
 return actions
end
function M.BlockDelete(hash)
 local row=GameInfo.UnitCommands.UNITCOMMAND_DELETE
 return M.IsTeam(UI.GetHeadSelectedUnit()) and row and hash==row.Hash
end

-- B248: one replaceable observation key in this UI context, no gameplay write.
-- Native CanProduce remains the sole production-list gate; never inject an item.
local trainingTrace,trainingStamp
function M.ObserveTraining(P,data)
 local c=data and data.City
 if not c or c:GetOwner()~=Game.GetLocalPlayer() or not P.IsTestPlayer(c:GetOwner())then return end
 local row=GameInfo.Units[M.KIND];local marker=GameInfo.Buildings.BUILDING_SPC_RESTRUCTURING_ACCESS
 local found,disabled=false,false
 for _,item in ipairs(data.UnitItems or {})do if item.Type==M.KIND then found=true;disabled=item.Disabled==true;break end end
 local svc=ExposedMembers.SPC_P0 and ExposedMembers.SPC_P0.Restructuring
 local stamp=c:GetOwner()..':'..c:GetID()..':'..Game.GetCurrentGameTurn()..':'..tostring(ExposedMembers.SPC_RuntimeUIRevision)
  ..':'..tostring(found)..':'..tostring(disabled)..':'..tostring(svc and svc.ready)
 if stamp==trainingStamp then return end;trainingStamp=stamp
 if not SPCExpeditionTrainingDiagnostics then return end
 trainingTrace=trainingTrace or SPCExpeditionTrainingDiagnostics.New(P,'RESTRUCTURING_UI')
 local v={owner=c:GetOwner(),city=c:GetID(),count=found and 1 or 0,paused=disabled,
  ready=svc and svc.ready==true or false,guardStatus=svc and 'PRESENT' or 'ABSENT',readStatus='VERIFIED'}
 local ok=pcall(function()
  assert(row and marker,'REST_DEFINITION_MISSING')
  v.unitIndex=row.Index;v.unitHash=row.Hash;v.markerIndex=marker.Index
  v.markerPresent=c:GetBuildings():HasBuilding(marker.Index)
  local q=c:GetBuildQueue();local p={UnitType=row.Hash,MilitaryFormationType=MilitaryFormationTypes.STANDARD_MILITARY_FORMATION}
  v.readyToSelect=q:CanProduce(p,true) -- native production-list visibility, not a permission override
  local allowed,results=q:CanProduce(p,false,true);v.eligibility=allowed
  v.nativeCost=q:GetUnitCost(row.Index)
  local reasons=results and CityCommandResults and results[CityCommandResults.FAILURE_REASONS]
  v.nativeReasonStatus=type(reasons)=='table' and 'AVAILABLE' or 'UNAVAILABLE'
  if type(reasons)=='table'then
   v.nativeReasonCount=#reasons;v.nativeReasonTruncated=#reasons>4
   for i=1,math.min(4,#reasons)do
    local value=reasons[i]
    v['nativeReason'..i]=type(value)=='string' and #value<=100 and value:match('^LOC_[A-Z0-9_]+$')and value or 'REDACTED'
   end
  end
 end)
 if not ok then v.readStatus='FAILED';v.reason='REST_TRAINING_READ_FAILED'end
 trainingTrace.Record('REST_TRAINING_LIST',v)
end
