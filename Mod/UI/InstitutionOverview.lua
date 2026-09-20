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
local lastData,verified,verifiedKey,lastSignature
local function eligible(data)
 local c=data and data.City
 if not c or data.Owner~=Game.GetLocalPlayer() then verified=nil;verifiedKey=nil;return false end
 local k=data.Owner..':'..c:GetID()..':'..c:GetX()..':'..c:GetY()
 if k~=verifiedKey then verified=nil;verifiedKey=k end
 local v=(ExposedMembers.SPC_P0 or {}).CityPresentationView
 if M.Matches(v,data.Owner,c:GetID(),c:GetX(),c:GetY()) then verified=v;return true,v end
 -- A confirmed different Identity withdraws; temporary unavailable preserves institutions.
 if v and not v.error and v.owner==data.Owner and v.cityID==c:GetID() and v.x==c:GetX() and v.y==c:GetY() then verified=nil end
 if verified then local pending={};for key,value in pairs(verified) do pending[key]=value end;pending.active=nil;pending.activeStatus='UNKNOWN';return true,pending end
 return false
end
local function signature(ok,v)
 if not ok then return 'UNAVAILABLE' end
 return v.owner..':'..v.cityID..':'..v.x..':'..v.y..':'..v.potential..':'..tostring(v.active)..':'..tostring(v.activeStatus)
end
function ViewPanelBreakdown(data)
 lastData=data
 local ok,v=eligible(data)
 lastSignature=signature(ok,v)
 original(ok and M.Filter(data,owned) or data)
 LuaEvents.SPC_InstitutionOverview(data,ok and v or nil)
end
local function changed()
 if lastData and not Controls.PanelBreakdown:IsHidden() then
  local c=UI.GetHeadSelectedCity()
  if c and lastData.City and c:GetOwner()==lastData.Owner and c:GetID()==lastData.City:GetID() then
   local ok,v=eligible(lastData)
   if signature(ok,v)~=lastSignature then ViewPanelBreakdown(lastData) end
  end
 end
end
LuaEvents.SPC_PresentationChanged.Add(changed)
local shutdown=OnShutdown
ContextPtr:SetShutdown(function() LuaEvents.SPC_PresentationChanged.Remove(changed);lastData=nil;if shutdown then shutdown() end end)
