-- Preserve Expansion/HD's native chooser for all ordinary spies.
include('EspionageChooser_Expansion1')
include('ExpeditionSpyUI')
local R=SPCExpeditionSpyUI
local blocked=false
local function redirect()
 blocked=true;Close();R.Open()
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
