-- Narrow HD adapter: retain its production panel and all original item data.
include('DL_ProductionPanel')
include('TimedProjectDisplay')
local claimSelection
local baseCurrent=RefreshCurrentProduction
function RefreshCurrentProduction(parent,pid,id)
 local result=baseCurrent(parent,pid,id)
 SPCTimedProjectDisplay.Current(parent,pid,id)
 return result
end
local ranks={PROJECT_SPC_CREW_250=1,PROJECT_SPC_CREW_420=2,PROJECT_SPC_CREW_750=3,PROJECT_SPC_CREW_1000=4,PROJECT_SPC_CREW_1360=5}
local baseGetData=GetDataHelper
function GetDataHelper(...)
 local data=baseGetData(...)
 if not data or not data.ProjectItems then return data end
 if claimSelection then claimSelection.Sync(data.City)end
 SPCTimedProjectDisplay.Items(data)
 local items=data.ProjectItems;local crew,others={},{};local insertion
 for _,item in ipairs(items) do
  if ranks[item.Type] then
   insertion=insertion or (#others+1);crew[#crew+1]=item
  else others[#others+1]=item end
 end
 if not insertion then return data end
 table.sort(crew,function(a,b) return ranks[a.Type]<ranks[b.Type] end)
 local result={}
 for i=1,#others+1 do
  if i==insertion then for _,item in ipairs(crew) do result[#result+1]=item end end
  if others[i] then result[#result+1]=others[i] end
 end
 data.ProjectItems=result;return data
end

-- Normal native project operation is retained; start only after the selected target is readable.
include('Probe')
include('ProjectTurnRead')
include('TimedProjectSelection')
include('ClaimProjectUI')
SPCProjectTurnRead.New(SPCP0,function()end,function()end)
local projectSelection=SPCTimedProjectSelection.New(SPCP0,function(...)return UI.RequestPlayerOperation(...)end,
 function(pid,id)LuaEvents.SPC_TimedProjectDisplayChanged(pid,id)end)
claimSelection=SPCClaimProjectUI.New(SPCP0,function(...)return UI.RequestPlayerOperation(...)end,
 function(pid,id)LuaEvents.SPC_TimedProjectDisplayChanged(pid,id)end)
local baseAdvance=AdvanceProject
function AdvanceProject(c,item)
 if not claimSelection.Before(c,item,CheckQueueItemSelected()) then return end
 if item.Type=="PROJECT_SPC_OVERFLOW_SINK_TEST" and CheckQueueItemSelected() then return end
 if not projectSelection.Before(c,item) then return end
 return baseAdvance(c,item)
end
Events.GameCoreEventPublishComplete.Add(projectSelection.Pulse)
Events.GameCoreEventPublishComplete.Add(claimSelection.Pulse)
LuaEvents.SPC_TimedProjectDisplayChanged.Add(function(pid,id)
 local c=UI.GetHeadSelectedCity()
 if c and c:GetOwner()==pid and c:GetID()==id and not ContextPtr:IsHidden() then Refresh()end
end)
