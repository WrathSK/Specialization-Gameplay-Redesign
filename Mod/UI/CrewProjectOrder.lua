-- Narrow HD adapter: retain its production panel and all original item data.
include('DL_ProductionPanel')
include('TimedProjectDisplay')
local claimSelection,dialogueSelection,trainingSelection,engineeringSelection
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
 if trainingSelection then trainingSelection.Items(data)end
 if claimSelection then claimSelection.Sync(data.City)end
 if dialogueSelection then dialogueSelection.Sync(data.City)end
 SPCTimedProjectDisplay.Items(data)
 -- HD exposes Disabled from native CanProduce. Filter only our exact project IDs.
 local items={}
 for _,item in ipairs(data.ProjectItems)do
  local owned=ranks[item.Type] or SPCClaimProjectUI.IsProject(item.Type) or item.Type==SPCDialogueProjectUI.PROJECT or item.Type==SPCEngineeringStudyUI.PROJECT
  if not owned or item.Disabled~=true or item.IsCurrentProduction==true then items[#items+1]=item end
 end
 data.ProjectItems=items
 local crew,others={},{};local insertion
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
dialogueSelection=SPCDialogueProjectUI.New(SPCP0,function(...)return UI.RequestPlayerOperation(...)end,
 function(pid,id)LuaEvents.SPC_TimedProjectDisplayChanged(pid,id)end)
engineeringSelection=SPCEngineeringStudyUI.New(SPCP0,function(...)return UI.RequestPlayerOperation(...)end,
 function(pid,id)LuaEvents.SPC_TimedProjectDisplayChanged(pid,id)end)
local baseAdvance=AdvanceProject
function AdvanceProject(c,item)
 if not engineeringSelection.Before(c,item,CheckQueueItemSelected())then return end
 if not dialogueSelection.Before(c,item,CheckQueueItemSelected())then return end
 if not claimSelection.Before(c,item,CheckQueueItemSelected()) then return end
 if item.Type=="PROJECT_SPC_OVERFLOW_SINK_TEST" and CheckQueueItemSelected() then return end
 if not projectSelection.Before(c,item) then return end
 return baseAdvance(c,item)
end
Events.GameCoreEventPublishComplete.Add(engineeringSelection.Publish)
Events.GameCoreEventPublishComplete.Add(projectSelection.Pulse)
Events.GameCoreEventPublishComplete.Add(claimSelection.Pulse)
Events.GameCoreEventPublishComplete.Add(dialogueSelection.Pulse)
Events.LoadScreenClose.Add(dialogueSelection.WarmStart)
Events.LoadScreenClose.Add(claimSelection.WarmStart)
LuaEvents.SPC_TimedProjectDisplayChanged.Add(function(pid,id)
 local c=UI.GetHeadSelectedCity()
 if c and c:GetOwner()==pid and c:GetID()==id and not ContextPtr:IsHidden() then Refresh()end
end)

-- B202 exact normal-unit queue admission, preserving the native insert mode.
include('ExpeditionTrainingUI')
local baseBuildUnit=BuildUnit
trainingSelection=SPCExpeditionTrainingUI.New(SPCP0,function(...)return UI.RequestPlayerOperation(...)end,
 function(pid,id)LuaEvents.SPC_TimedProjectDisplayChanged(pid,id)end,baseBuildUnit)
function BuildUnit(c,item)
 if item.Type~=SPCExpeditionTrainingUI.KIND then return baseBuildUnit(c,item)end
 if trainingSelection.Before(c,item,CheckQueueItemSelected())then return baseBuildUnit(c,item)end
end
local baseRemoveQueueItem=RemoveQueueItem
function RemoveQueueItem(index)
 trainingSelection.CancelQueue(UI.GetHeadSelectedCity(),index)
 return baseRemoveQueueItem(index)
end
Events.GameCoreEventPublishComplete.Add(trainingSelection.Pulse)

-- Observe native replacement intent without changing its parameters. This also
-- covers ordinary building/project selection replacing the reserved queue slot.
local baseGetBuildInsertMode=GetBuildInsertMode
function GetBuildInsertMode(parameters)
 local result=baseGetBuildInsertMode(parameters)
 if parameters[CityOperationTypes.PARAM_INSERT_MODE]==CityOperationTypes.VALUE_REPLACE_AT then
  trainingSelection.CancelQueue(UI.GetHeadSelectedCity(),parameters[CityOperationTypes.PARAM_QUEUE_DESTINATION_LOCATION])
 end
 return result
end
