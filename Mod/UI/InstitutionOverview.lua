-- Preserve installed HD implementation (including its city-policy/Suk chain).
-- This prototype targets the tested HD environment; it is not a universal UI adapter.
include('DL_CityPanelOverview')
if not ViewPanelBreakdown then
 include('CityPanelOverview_Expansion2')
end
include('InstitutionPresentation')
local M=SPCInstitutionPresentation
local original=ViewPanelBreakdown
local owned={}
for b in GameInfo.Buildings() do
 if b.BuildingType:match('^BUILDING_SPC_') and (b.InternalOnly==true or b.InternalOnly==1) then owned[b.BuildingType]=true end
end
local claimOwned={BUILDING_SPC_CLAIM_RESEARCH=true,BUILDING_SPC_CLAIM_CULTURE=true,BUILDING_SPC_CLAIM_INDUSTRY=true,BUILDING_SPC_CLAIM_COMMERCE=true}
local lastData,verified,verifiedKey,lastSignature,accepted
local sourceSequence=-1;local deliverySequence=-1;local closedSource=-1;local generation=0;local stopped=false
local function currentPacket(p)
 local m=p and p.meta;local shared=ExposedMembers.SPC_P0
 return m and shared==m.backend and shared.Version==p.version and shared.PlayerActionReplies==m.parent
  and m.parent.Presentations==m.channel and m.channel.epoch==m.epoch and m.channel.version==p.version
  and m.channel.scope=='CITY_PRESENTATION'and m.channel.Has==m.has and m.channel.Take==m.take and m.channel.Discard==m.discard
end
local function eligible(data)
 local c=data and data.City
 if not c or data.Owner~=Game.GetLocalPlayer() then verified=nil;verifiedKey=nil;return false end
 local k=data.Owner..':'..c:GetID()..':'..c:GetX()..':'..c:GetY()
 if k~=verifiedKey then verified=nil;verifiedKey=k end
 local p=accepted
 if not currentPacket(p)then verified=nil;return false end
 local m=p.meta
 if m.owner~=data.Owner or m.cityID~=c:GetID()or m.x~=c:GetX()or m.y~=c:GetY()then verified=nil;return false end
 local v=p.view
 if M.Matches(v,data.Owner,c:GetID(),c:GetX(),c:GetY()) then verified=v;return true,v end
 -- A confirmed different Identity withdraws; temporary unavailable preserves institutions.
 if v and not v.error and v.owner==data.Owner and v.cityID==c:GetID() and v.x==c:GetX() and v.y==c:GetY() then verified=nil end
 if verified then local pending={};for key,value in pairs(verified) do pending[key]=value end;pending.active=nil;pending.activeStatus='UNKNOWN';pending.institutionSummary={known=false};return true,pending end
 return false
end
local function signature(ok,v)
 if not ok then return 'UNAVAILABLE' end
 return v.owner..':'..v.cityID..':'..v.x..':'..v.y..':'..M.Signature(v)
end
function ViewPanelBreakdown(data)
 if stopped then return end
 local cycle=generation
 lastData=data
 local ok,v=eligible(data)
 if stopped or generation~=cycle then return end
 lastSignature=signature(ok,v)
 original(M.Filter(data,ok and owned or claimOwned))
 if stopped or generation~=cycle or lastData~=data then return end
 LuaEvents.SPC_InstitutionOverview(data,ok and v or nil)
end
local function changed(packet)
 if stopped then return end
 if type(packet)=='table'and type(packet.sourceSequence)=='number'and type(packet.deliverySequence)=='number'and packet.sourceSequence>=sourceSequence then
  if packet.sourceSequence==sourceSequence and(packet.deliverySequence<=deliverySequence or closedSource==sourceSequence)then return end
  if packet.sourceSequence~=sourceSequence then verified=nil;verifiedKey=nil;deliverySequence=-1;closedSource=-1 end
  sourceSequence=packet.sourceSequence;deliverySequence=packet.deliverySequence;generation=generation+1
  if packet.status=='CLOSED'then closedSource=sourceSequence;accepted=nil;verified=nil;verifiedKey=nil
  elseif packet.status=='RESET'then accepted=nil;verified=nil;verifiedKey=nil
  elseif packet.status=='READY'or packet.status=='UNAVAILABLE'then accepted=packet end
 elseif packet~=nil then return end
 local cycle=generation
 if lastData and not Controls.PanelBreakdown:IsHidden() then
  local c=UI.GetHeadSelectedCity()
  if c and lastData.City and c:GetOwner()==lastData.Owner and c:GetID()==lastData.City:GetID() then
   local ok,v=eligible(lastData)
   if stopped or generation~=cycle then return end
   if signature(ok,v)~=lastSignature then ViewPanelBreakdown(lastData) end
  end
 end
end
-- Native overview open/close functions remain responsible for lens, input,
-- animation and checkbox state. Unlike the stock toggle, this shortcut opens.
local showing=false
local baseShow,baseClose=OnShowOverviewPanel,Close
if baseShow then
 function OnShowOverviewPanel(value)
  if value then showing=true end
  return baseShow(value)
 end
end
if baseClose then
 function Close()showing=false;return baseClose()end
end
local function openInstitutions(pid,id)
 if stopped then return end
 local c=UI.GetHeadSelectedCity()
 if pid~=Game.GetLocalPlayer() or not c or c:GetOwner()~=pid or c:GetID()~=id then return end
 if not showing then OnShowOverviewPanel(true)end
 if GetSelectedTabButton()~=Controls.BuildingsButton then OnToggleBuildingsTab()end
end
local openEvent=LuaEvents.SPC_OpenInstitutions
if openEvent then openEvent.Add(openInstitutions)end
LuaEvents.SPC_PresentationChanged.Add(changed)
local readyEvent=LuaEvents.SPC_PresentationConsumerReady
if readyEvent then pcall(readyEvent)end -- replay accepted UI data only; no Gameplay request
local shutdown=OnShutdown
ContextPtr:SetShutdown(function() stopped=true;generation=generation+1;LuaEvents.SPC_PresentationChanged.Remove(changed);if openEvent then openEvent.Remove(openInstitutions)end;lastData=nil;accepted=nil;verified=nil;if shutdown then shutdown() end end)
