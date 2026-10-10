-- The native mission popup must never cache our team as its active mission unit.
include('EspionagePopup')
include('ExpeditionSpyUI')
local R=SPCExpeditionSpyUI
local blocked=false
local function redirect()
 blocked=true;Close();R.Open()
end
local baseBriefing=OnShowMissionBriefing
LuaEvents.EspionageChooser_ShowMissionBriefing.Remove(baseBriefing)
function OnShowMissionBriefing(operation,id,plot)
 if R.IsTeam(R.ByID(id))then redirect();return end
 blocked=false;return baseBriefing(operation,id,plot)
end
LuaEvents.EspionageChooser_ShowMissionBriefing.Add(OnShowMissionBriefing)
local baseAbort=OnShowMissionAbort
LuaEvents.UnitPanel_CancelMission.Remove(baseAbort)
function OnShowMissionAbort(id)
 if R.IsTeam(R.ByID(id))then redirect();return end
 blocked=false;return baseAbort(id)
end
LuaEvents.UnitPanel_CancelMission.Add(OnShowMissionAbort)
local baseCompleted=ShowMissionCompletedPopup
function ShowMissionCompletedPopup(...)
 blocked=false;return baseCompleted(...)
end
local baseRenew=RenewMission
function RenewMission(u,...)
 if R.IsTeam(u)then redirect();return end
 return baseRenew(u,...)
end
for _,name in ipairs({'OnAccept','OnAbort'})do
 local base=_G[name]
 _G[name]=function(...)
  if blocked then redirect();return end
  return base(...)
 end
end
Controls.AcceptButton:RegisterCallback(Mouse.eLClick,OnAccept)
Controls.AbortButton:RegisterCallback(Mouse.eLClick,OnAbort)
local baseDebug=OnGameDebugReturn
LuaEvents.GameDebug_Return.Remove(baseDebug)
function OnGameDebugReturn(context,data)
 if context=='EspionagePopup' and data and R.IsTeam(data.spy)then redirect();return end
 return baseDebug(context,data)
end
LuaEvents.GameDebug_Return.Add(OnGameDebugReturn)
-- The native/HD SpyMissionCompleted observers are deliberately not removed,
-- forged or rewritten. Our independent timer never publishes that event.
