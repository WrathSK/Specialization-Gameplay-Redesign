-- Keep HD/native rendering and ordinary-unit callbacks intact.
include('DL_UnitPanel')
include('ExpeditionSpyUI')
local R=SPCExpeditionSpyUI
local baseActions=GetUnitActionsTable
local baseClick=OnUnitActionClicked
local function nativeEligible(u,row,command,visible)
 local ok,yes=pcall(function()
  if command then
   if visible then return UnitManager.CanStartCommand(u,row.Hash,true)end
   return UnitManager.CanStartCommand(u,row.Hash,false,true)
  end
  if visible then return UnitManager.CanStartOperation(u,row.Hash,nil,true)end
  return UnitManager.CanStartOperation(u,row.Hash,nil,false,
   OperationResultsTypes and OperationResultsTypes.NO_TARGETS)
 end)
 return ok and yes==true
end
function GetUnitActionsTable(u)
 if not R.IsTeam(u)then return baseActions(u)end
 -- Do not call the base builder first: it also registers native mission hotkeys.
 local actions={ATTACK={},BUILD={},GAMEMODIFY={},MOVE={},OFFENSIVESPY={},INPLACE={},SECONDARY={},SPECIFIC={},
  displayOrder={primaryArea={'ATTACK','OFFENSIVESPY','SPECIFIC','MOVE','INPLACE','GAMEMODIFY'},secondaryArea={'SECONDARY'}}}
 if not R.ActivityView(u) or R.ActivityLocked(u)then return actions end
 local id,owner=u:GetID(),u:GetOwner()
 local function add(mode,icon,key,hash)
  local enabled=R.CanOpen(mode,u)
  local label=Locale.Lookup('LOC_SPC_EXPEDITION_SPY_ACTION_'..key)
  if not enabled then label=label..'[NEWLINE]'..R.UnavailableText(u)end
  AddActionToTable(actions,{CategoryInUI='SPECIFIC',Icon=icon},not enabled,label,hash,function()
   local selected=UI.GetHeadSelectedUnit()
   if R.IsTeam(selected) and selected:GetOwner()==owner and selected:GetID()==id and R.CanOpen(mode,selected)then
    R.Open(mode,id)
   end
  end)
 end
 add('TRAVEL','ICON_UNITOPERATION_SPY_TRAVEL_NEW_CITY','TRAVEL',-196)
 add('TASK','ICON_UNITOPERATION_SPY_GAIN_SOURCES','TASK',-197)
 -- Allow only idle controls, not the base Spy builder or its mission hotkeys.
 -- Manual sleep is native-owned: it never writes the task activity lease.
 local function idle(selected)
  return R.IsTeam(selected) and selected:GetOwner()==owner and selected:GetID()==id
   and R.CanOpen('TRAVEL',selected)
 end
 local function nativeAction(tableName,key,command)
  local row=GameInfo[tableName] and GameInfo[tableName][key]
  local actionType=command and UnitCommandTypes and UnitCommandTypes.TYPE
   or (not command and UnitOperationTypes and UnitOperationTypes.TYPE)
  if not row or type(row.Hash)~='number' or type(actionType)~='number' or not idle(u)then return end
  local function eligible(selected,visible)return nativeEligible(selected,row,command,visible)end
  if not eligible(u,true)then return end
  AddActionToTable(actions,row,not eligible(u,false),Locale.Lookup(row.Description),row.Hash,function()
   local selected=UI.GetHeadSelectedUnit()
   if idle(selected) and eligible(selected,false)then
    -- Retain native turn-processing and interface-mode checks.
    baseClick(actionType,row.Hash,UI.GetInterfaceMode())
   end
  end)
 end
 nativeAction('UnitOperations','UNITOPERATION_SKIP_TURN',false)
 nativeAction('UnitOperations','UNITOPERATION_SLEEP',false)
 nativeAction('UnitCommands','UNITCOMMAND_WAKE',true)
 return actions
end
function OnUnitActionClicked(...)
 if R.IsTeam(UI.GetHeadSelectedUnit())then R.SuppressNative();return end
 return baseClick(...)
end
local baseCancel=OnUnitActionClicked_CancelSpyMission
function OnUnitActionClicked_CancelSpyMission(...)
 if R.IsTeam(UI.GetHeadSelectedUnit())then R.SuppressNative();return end
 return baseCancel(...)
end

-- B220: a Gate revision alone does not describe native action availability.
-- Read only the selected team's three idle controls at event publication; keep
-- one disposable signature and rebuild only on change. No frame/timer polling.
local lastSignature;local refreshing=false
local function signature(u)
 local v=R.ActivityView(u)
 local key=tostring(u:GetOwner())..':'..u:GetID()..':'..tostring(v and v.revision)
 if not R.CanOpen('TRAVEL',u)then return key..':LOCKED'end
 local function bits(tableName,name,command)
  local row=GameInfo[tableName] and GameInfo[tableName][name]
  if not row or type(row.Hash)~='number'then return ':NA'end
  return ':'..tostring(nativeEligible(u,row,command,true))..':'..tostring(nativeEligible(u,row,command,false))
 end
 return key..bits('UnitOperations','UNITOPERATION_SKIP_TURN',false)
  ..bits('UnitOperations','UNITOPERATION_SLEEP',false)..bits('UnitCommands','UNITCOMMAND_WAKE',true)
end
local function refreshSelected()
 if refreshing then return end
 local u=UI.GetHeadSelectedUnit()
 if not R.IsTeam(u)then lastSignature=nil;return end
 local nextSignature=signature(u)
 if nextSignature==lastSignature then return end
 refreshing=true
 local ok,err=pcall(Refresh,u:GetOwner(),u:GetID())
 refreshing=false
 if ok then
  lastSignature=nextSignature
  print('[SPC][B191][N1_TASK] idleActions=REFRESH state='..nextSignature)
 else
  print('[SPC][B191][N1_TASK] idleActions=ERROR reason='..tostring(err):sub(1,160))
 end
end
local function unitChanged(pid,id)
 local u=UI.GetHeadSelectedUnit()
 if R.IsTeam(u) and pid==u:GetOwner() and id==u:GetID()then refreshSelected()end
end
LuaEvents.SPC_ExpeditionActivityChanged.Add(refreshSelected)
local events={}
local function listen(event,handler)
 if event then event.Add(handler);events[#events+1]={event,handler}end
end
listen(Events.GameCoreEventPublishComplete,refreshSelected)
listen(Events.UnitSelectionChanged,refreshSelected)
listen(Events.UnitActivityChanged,unitChanged)
listen(Events.UnitOperationDeactivated,unitChanged)
ContextPtr:SetShutdown(function()
 LuaEvents.SPC_ExpeditionActivityChanged.Remove(refreshSelected)
 for _,v in ipairs(events)do v[1].Remove(v[2])end
 lastSignature=nil
end)
