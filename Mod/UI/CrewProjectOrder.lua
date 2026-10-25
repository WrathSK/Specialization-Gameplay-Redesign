-- Narrow HD adapter: retain its production panel and all original item data.
include('DL_ProductionPanel')
include('SafeAdapters')
local adapters=SPCSafeAdapters.New()
pcall(include,'TimedProjectDisplay')
pcall(include,'RestructuringUI')
-- Decorate only this Mod's claim projects after native rendering; recycled
-- rows receive a hide request for every non-claim item.
local baseGenericItem=PopulateGenericItemData
function PopulateGenericItemData(instance,item)
 local result=baseGenericItem(instance,item)
 pcall(function()LuaEvents.SPC_ClaimIconDecorate(instance.Icon,'ICON_'..item.Type)end)
 return result
end
local baseQueueInstance=CreateQueueInstance
function CreateQueueInstance(...)
 local instance=baseQueueInstance(...)
 if instance then pcall(function()LuaEvents.SPC_ClaimIconDecorate(instance.ProductionIcon,instance.iconTexture)end)end
 return instance
end
local claimSelection,dialogueSelection,trainingSelection,engineeringSelection,crewSelection,commerceSelection,capitalSelection,developmentSelection
local displaySelection=adapters.Add('TimedDisplay',function()return false end,{},function()return SPCTimedProjectDisplay end,{Render={100,'Items'}})
local baseCurrent=RefreshCurrentProduction
function RefreshCurrentProduction(parent,pid,id)
 local result=baseCurrent(parent,pid,id)
 pcall(function()LuaEvents.SPC_ClaimIconDecorate(parent.ProductionIcon,result and parent.iconTexture or nil)end)
 pcall(function()SPCTimedProjectDisplay.Current(parent,pid,id)end)
 return result
end
pcall(include,'CrewModel')
local ranks=setmetatable({},{__index=function(_,id)if SPCCrewModel and SPCCrewModel.Parse then return SPCCrewModel.Parse(id)end end})
adapters.Barrier('Render',20,function(data)SPCRestructuringUI.ObserveTraining(SPCP0,data)end)
local baseGetData=GetDataHelper
function GetDataHelper(...)
 local data=baseGetData(...)
 if not data or not data.ProjectItems then return data end
 adapters.Render(data)
 -- HD exposes Disabled from native CanProduce. Filter only our exact project IDs.
 local items={}
 for _,item in ipairs(data.ProjectItems)do
  local owned=ranks[item.Type] or (item.Type=='PROJECT_SPC_CLAIM_RESEARCH' or item.Type=='PROJECT_SPC_CLAIM_CULTURE' or item.Type=='PROJECT_SPC_CLAIM_INDUSTRY' or item.Type=='PROJECT_SPC_CLAIM_COMMERCE') or item.Type=='PROJECT_SPC_ERA_DIALOGUE' or item.Type=='PROJECT_SPC_ENGINEERING_STUDY'
  if not owned or item.Disabled~=true or item.IsCurrentProduction==true or item.SPC_CrewRetained==true then items[#items+1]=item end
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
local function send(...)return UI.RequestPlayerOperation(...)end
local function notify(pid,id)LuaEvents.SPC_TimedProjectDisplayChanged(pid,id)end
local function one(name)return function(item)return item and item.Type==name end end
local function claim(item)
 local t=item and item.Type
 return t=='PROJECT_SPC_CLAIM_RESEARCH' or t=='PROJECT_SPC_CLAIM_CULTURE' or t=='PROJECT_SPC_CLAIM_COMMERCE' or t=='PROJECT_SPC_CLAIM_INDUSTRY'
end
local crewTypes={['PROJECT_SPC_CREW_1000']=true,['PROJECT_SPC_CREW_1000_P120']=true,['PROJECT_SPC_CREW_1000_P130']=true,['PROJECT_SPC_CREW_1000_P140']=true,['PROJECT_SPC_CREW_1360']=true,['PROJECT_SPC_CREW_1360_P120']=true,['PROJECT_SPC_CREW_1360_P130']=true,['PROJECT_SPC_CREW_1360_P140']=true,['PROJECT_SPC_CREW_250']=true,['PROJECT_SPC_CREW_250_P120']=true,['PROJECT_SPC_CREW_250_P130']=true,['PROJECT_SPC_CREW_250_P140']=true,['PROJECT_SPC_CREW_420']=true,['PROJECT_SPC_CREW_420_P120']=true,['PROJECT_SPC_CREW_420_P130']=true,['PROJECT_SPC_CREW_420_P140']=true,['PROJECT_SPC_CREW_750']=true,['PROJECT_SPC_CREW_750_P120']=true,['PROJECT_SPC_CREW_750_P130']=true,['PROJECT_SPC_CREW_750_P140']=true}
local function crew(item)
 if not item or type(item.Type)~='string'then return false end
 if crewTypes[item.Type]then return true end
 local base,speed=item.Type:match('^(PROJECT_SPC_CREW_[%d_P]+)_S(%d+)$')
 -- Generated speed variants exist only for the exact packaged base IDs.
 return base~=nil and crewTypes[base]==true and GameInfo and GameInfo.Projects and GameInfo.Projects[item.Type]~=nil or false
end
adapters.Add('ProjectTurnRead',function()return false end,{'SPC_ProjectTurnRead'},function()
 include('ProjectTurnRead');return SPCProjectTurnRead.New(SPCP0,function()end,function()end)
end)
local projectSelection=adapters.Add('TimedProjectSelection',one('PROJECT_SPC_OVERFLOW_SINK_TEST'),{'SPC_TimedProjectSelection'},function()
 include('TimedProjectSelection');return SPCTimedProjectSelection.New(SPCP0,send,notify)
end,{Before={90,'Before'},Pulse={10,'Pulse'}})
claimSelection=adapters.Add('ClaimProjectUI',claim,{'SPC_ClaimQueueRead','SPC_ClaimSelection','SPC_ClaimSync'},function()
 include('ClaimProjectUI');return SPCClaimProjectUI.New(SPCP0,send,notify)
end,{Render={70,'Sync'},Before={70,'Before',true},Pulse={20,'Pulse'},Warm={20,'WarmStart'},Queue={10,'QueueEvent'},Connect={10,'Connect'}})
dialogueSelection=adapters.Add('DialogueProjectUI',one('PROJECT_SPC_ERA_DIALOGUE'),{'SPC_DialogueGameEra','SPC_DialogueProjectRead'},function()
 include('DialogueProjectUI');return SPCDialogueProjectUI.New(SPCP0,send,notify)
end,{Render={80,'Sync'},Before={60,'Before',true},Pulse={30,'Pulse'},Warm={10,'WarmStart'},Queue={20,'QueueEvent'},Connect={20,'Connect'}})
engineeringSelection=adapters.Add('EngineeringStudyUI',one('PROJECT_SPC_ENGINEERING_STUDY'),{'SPC_EngineeringStudyRead'},function()
 include('EngineeringStudyUI');return SPCEngineeringStudyUI.New(SPCP0,send,notify)
end,{Render={90,'Sync'},Before={50,'Before',true},Publish={50,'Publish'},Warm={30,'WarmStart'},Queue={30,'QueueEvent'},Connect={30,'Connect'}})
local baseAdvance=AdvanceProject
capitalSelection=adapters.Add('CapitalInvestmentUI',one('PROJECT_SPC_CAPITAL_INVESTMENT'),{},function()
 include('CapitalInvestmentUI');return SPCCapitalInvestmentUI.New(SPCP0,notify,SPCSafeAdapters.NewViewObserver())
end,{Render={40,'Items'},Before={10,'Before',true},Publish={10,'Publish'}})
developmentSelection=adapters.Add('DevelopmentInvestmentUI',one('PROJECT_SPC_DEVELOPMENT_INVESTMENT'),{'SPC_DevelopmentRead','SPC_DevelopmentPriceRead'},function()
 include('DevelopmentInvestmentUI');return SPCDevelopmentInvestmentUI.New(SPCP0,notify,SPCSafeAdapters.NewViewObserver())
end,{Render={50,'Items'},Before={20,'Before',true},Publish={20,'Publish'}})
commerceSelection=adapters.Add('CommerceUI',one('PROJECT_SPC_COMMERCIALIZATION'),{},function()
 include('CommerceUI');return SPCCommerceUI.New(SPCP0,notify,SPCSafeAdapters.NewViewObserver())
end,{Render={60,'Items'},Before={30,'Before',true},Publish={30,'Publish'}})
crewSelection=adapters.Add('CrewProjectUI',crew,{'SPC_CrewNativeRead'},function()
 include('CrewProjectUI');return SPCCrewProjectUI.New(SPCP0,send,notify,baseAdvance)
end,{Render={30,'Items'},Before={40,'Before',true},Publish={40,'Publish'}})
adapters.Barrier('Before',80,function(c,item)
 return not(item.Type=='PROJECT_SPC_OVERFLOW_SINK_TEST'and CheckQueueItemSelected())
end)
local function queuedSelection()return CheckQueueItemSelected()end
function AdvanceProject(c,item)
 if adapters.BeforeAll(c,item,queuedSelection)then return baseAdvance(c,item)end
end
adapters.Each('Publish',function(e,method)adapters.Hook(Events,'GameCoreEventPublishComplete',e,method)end)
adapters.Each('Pulse',function(e,method)adapters.Hook(Events,'GameCoreEventPublishComplete',e,method)end)
adapters.Each('Warm',function(e,method)
 adapters.Hook(Events,'LoadScreenClose',e,method)
 adapters.Hook(Events,'LocalPlayerTurnBegin',e,method) -- only an uninitialized availability generation can enumerate
end)
-- Keep one listener per adapter and the original event-major registration order.
for _,name in ipairs({'CityProductionChanged','CityProductionQueueChanged','CityProductionUpdated'})do
 adapters.Each('Queue',function(e,method)adapters.Hook(Events,name,e,method)end)
end
adapters.Hook(LuaEvents,'SPC_TimedProjectDisplayChanged',nil,nil,function(pid,id)
 local c=UI.GetHeadSelectedCity()
 if c and c:GetOwner()==pid and c:GetID()==id and not ContextPtr:IsHidden()then Refresh()end
end)

-- B202 exact normal-unit queue admission, preserving the native insert mode.
local baseBuildUnit=BuildUnit
trainingSelection=adapters.Add('ExpeditionTrainingUI',one('UNIT_SPC_EXPEDITION_SPY'),{'SPC_ExpeditionQueueRead'},function()
 include('ExpeditionTrainingUI');return SPCExpeditionTrainingUI.New(SPCP0,send,notify,baseBuildUnit)
end,{Render={10,'Items'}})
function BuildUnit(c,item)
 if item.Type~='UNIT_SPC_EXPEDITION_SPY' then return baseBuildUnit(c,item)end
 if adapters.Before(trainingSelection,c,item,CheckQueueItemSelected())then return baseBuildUnit(c,item)end
end
local baseRemoveQueueItem=RemoveQueueItem
function RemoveQueueItem(index)
 adapters.Call(trainingSelection,'CancelQueue',UI.GetHeadSelectedCity(),index)
 return baseRemoveQueueItem(index)
end
adapters.Hook(Events,'GameCoreEventPublishComplete',trainingSelection,'Pulse')
adapters.Hook(Events,'GameCoreEventPlaybackComplete',trainingSelection,'RefreshFacts')
for _,name in ipairs({'GovernorAssigned','GovernorEstablished','GovernorChanged','GovernorPromoted','PlayerTurnActivated'})do
 adapters.Hook(Events,name,trainingSelection,'Invalidate')
end

-- Observe native replacement intent without changing its parameters. This also
-- covers ordinary building/project selection replacing the reserved queue slot.
local baseGetBuildInsertMode=GetBuildInsertMode
function GetBuildInsertMode(parameters)
 local result=baseGetBuildInsertMode(parameters)
 if parameters[CityOperationTypes.PARAM_INSERT_MODE]==CityOperationTypes.VALUE_REPLACE_AT then
  adapters.Call(trainingSelection,'CancelQueue',UI.GetHeadSelectedCity(),parameters[CityOperationTypes.PARAM_QUEUE_DESTINATION_LOCATION])
 end
 return result
end

-- The verified native/HD base installs global OnShutdown. Preserve that callback.
local nativeShutdown=OnShutdown
ContextPtr:SetShutdown(function()
 adapters.Close()
 if nativeShutdown then nativeShutdown()end
end)

-- Publish readers only after all successful adapters and native hooks are wired.
adapters.Each('Connect',function(e,method)adapters.Call(e,method)end)
