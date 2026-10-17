-- Keep HD/native rendering and ordinary-unit callbacks intact.
include('DL_UnitPanel')
include('ExpeditionSpyUI')
local R=SPCExpeditionSpyUI
local baseActions=GetUnitActionsTable
local baseClick=OnUnitActionClicked
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
  local function eligible(selected,visible)
   local ok,yes=pcall(function()
    if command then
     if visible then return UnitManager.CanStartCommand(selected,row.Hash,true)end
     return UnitManager.CanStartCommand(selected,row.Hash,false,true)
    end
    if visible then return UnitManager.CanStartOperation(selected,row.Hash,nil,true)end
    return UnitManager.CanStartOperation(selected,row.Hash,nil,false,
     OperationResultsTypes and OperationResultsTypes.NO_TARGETS)
   end)
   return ok and yes==true
  end
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

-- Refresh clears native action/hotkey bindings before rebuilding our exact-type
-- list. Previously captured callbacks still recheck the current task lock.
local function activityChanged()
 local u=UI.GetHeadSelectedUnit()
 if R.IsTeam(u)then Refresh(u:GetOwner(),u:GetID())end
end
LuaEvents.SPC_ExpeditionActivityChanged.Add(activityChanged)
-- The inspected native/HD UnitPanel chain has no shutdown handler. Own only
-- this subscription; ordinary UnitPanel behavior and handlers remain intact.
ContextPtr:SetShutdown(function()
 LuaEvents.SPC_ExpeditionActivityChanged.Remove(activityChanged)
end)
