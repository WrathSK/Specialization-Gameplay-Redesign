-- Keep HD/native rendering and ordinary-unit callbacks intact.
include('DL_UnitPanel')
include('ExpeditionSpyUI')
local R=SPCExpeditionSpyUI
local baseActions=GetUnitActionsTable
function GetUnitActionsTable(u)
 if not R.IsTeam(u)then return baseActions(u)end
 -- Do not call the base builder first: it also registers native mission hotkeys.
 local actions={ATTACK={},BUILD={},GAMEMODIFY={},MOVE={},OFFENSIVESPY={},INPLACE={},SECONDARY={},SPECIFIC={},
  displayOrder={primaryArea={'ATTACK','OFFENSIVESPY','SPECIFIC','MOVE','INPLACE','GAMEMODIFY'},secondaryArea={'SECONDARY'}}}
 AddActionToTable(actions,{CategoryInUI='SPECIFIC',Icon='ICON_UNITOPERATION_SPY_TRAVEL_NEW_CITY'},false,
  Locale.Lookup('LOC_SPC_EXPEDITION_SPY_MANAGE'),-185,function()
   if R.IsTeam(UI.GetHeadSelectedUnit())then R.Open()end
  end)
 -- Skip is an ordinary unit operation, not a Spy mission; no reward/completion hook.
 local skip=GameInfo.UnitOperations.UNITOPERATION_SKIP_TURN
 if skip and UnitManager.CanStartOperation(u,skip.Hash,nil,nil,false)then
  AddActionToTable(actions,skip,false,Locale.Lookup(skip.Description),skip.Hash,function()
   local selected=UI.GetHeadSelectedUnit()
   if R.IsTeam(selected) and UnitManager.CanStartOperation(selected,skip.Hash,nil,nil,false)then
    UnitManager.RequestOperation(selected,skip.Hash)
   end
  end)
 end
 return actions
end
local baseClick=OnUnitActionClicked
function OnUnitActionClicked(...)
 if R.IsTeam(UI.GetHeadSelectedUnit())then R.Open();return end
 return baseClick(...)
end
local baseCancel=OnUnitActionClicked_CancelSpyMission
function OnUnitActionClicked_CancelSpyMission(...)
 if R.IsTeam(UI.GetHeadSelectedUnit())then R.Open();return end
 return baseCancel(...)
end
