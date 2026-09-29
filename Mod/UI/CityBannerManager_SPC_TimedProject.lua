-- Expansion2 wildcard extension; keep the native/other-mod banner, override exact project only.
include("TimedProjectDisplay")
local baseProduction=CityBanner.UpdateProduction
function CityBanner:UpdateProduction(c)
 baseProduction(self,c)
 if not SPCTimedProjectDisplay.IsCurrent(c) then return end
 local inst=self.m_StatProductionIM and self.m_StatProductionIM:GetAllocatedInstance(1)
 if not inst then return end
 local turns,note=SPCTimedProjectDisplay.Text(c:GetOwner(),c:GetID())
 inst.TurnsLeft:SetText(turns)
 inst.Button:SetToolTipString(note)
 inst.FillMeter:SetHide(true);inst.IconMeter:SetHide(true)
end
LuaEvents.SPC_TimedProjectDisplayChanged.Add(function(pid,id)
 local c=Players[pid] and Players[pid]:GetCities():FindID(id)
 local banner=GetCityBanner(pid,id)
 if c and banner then banner:UpdateProduction(c)end
end)
