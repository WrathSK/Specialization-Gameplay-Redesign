-- Preserve Expansion/HD's native chooser for all ordinary spies.
include('EspionageChooser_Expansion1')
include('ExpeditionSpyUI')
local R=SPCExpeditionSpyUI
local blocked=false
local function redirect()
 blocked=true;Close();R.SuppressNative()
end
local baseOpen=Open
function Open(...)
 if R.IsTeam(UI.GetHeadSelectedUnit())then redirect();return end
 blocked=false;return baseOpen(...)
end
local baseMode=GoToProperInterfaceMode
function GoToProperInterfaceMode(u,...)
 if R.IsTeam(u)then redirect();return end
 blocked=false;return baseMode(u,...)
end
-- The native initializer already captured its selection listener. Replace
-- only that entry: generic mode/activity/debug callbacks keep suppressing our
-- team, so native SLEEP/release notifications cannot reopen a management panel.
local baseSelection=OnUnitSelectionChanged
Events.UnitSelectionChanged.Remove(baseSelection)
function OnUnitSelectionChanged(playerID,unitID,x,y,z,selected,editable)
 local u=UI.GetHeadSelectedUnit()
 if not R.IsTeam(u)then return baseSelection(playerID,unitID,x,y,z,selected,editable)end
 redirect()
 if selected==true and editable~=false and playerID==Game.GetLocalPlayer() and unitID==u:GetID()then
  R.OpenOnSelection(u)
 end
end
Events.UnitSelectionChanged.Add(OnUnitSelectionChanged)
local baseShutdown=OnShutdown
function OnShutdown(...)
 Events.UnitSelectionChanged.Remove(OnUnitSelectionChanged)
 return baseShutdown(...)
end
ContextPtr:SetShutdown(OnShutdown)
-- Guard both mouse callbacks and global calls. The native initializer captured
-- the original confirmation function, so explicitly replace that control binding.
for _,name in ipairs({'TeleportToSelectedCity','OnConfirmPlacement','OnCounterspySelected','OnMissionSelected'})do
 local base=_G[name]
 _G[name]=function(...)
  if blocked or R.IsTeam(UI.GetHeadSelectedUnit())then redirect();return end
  return base(...)
 end
end
Controls.ConfirmButton:RegisterCallback(Mouse.eLClick,OnConfirmPlacement)
local baseDebug=OnGameDebugReturn
LuaEvents.GameDebug_Return.Remove(baseDebug)
function OnGameDebugReturn(context,data)
 if context=='EspionageChooser' and data and R.IsTeam(data.selectedSpy)then redirect();return end
 return baseDebug(context,data)
end
LuaEvents.GameDebug_Return.Add(OnGameDebugReturn)
