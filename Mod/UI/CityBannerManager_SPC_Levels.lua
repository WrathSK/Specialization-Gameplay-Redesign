-- Native banner extension: keep visibility, zoom, sizing and other-mod callbacks.
local baseName=CityBanner.UpdateName
local baseUninitialize=CityBanner.Uninitialize
local function attach(b)
 local inst=b.m_Instance
 if not inst or not inst.CityBannerButton or not inst.Container then return end
 local c=b:GetCity();if not c then return end
 LuaEvents.SPC_LevelBannerAttach(c:GetOwner(),c:GetID(),c:GetX(),c:GetY(),inst.Container)
end
function CityBanner:UpdateName()
 baseName(self);attach(self)
end
function CityBanner:Uninitialize()
 local inst=self.m_Instance
 if inst and inst.CityBannerButton and inst.Container then LuaEvents.SPC_LevelBannerDetach(inst.Container)end
 baseUninitialize(self)
end
local function ready()
 local pid=Game.GetLocalPlayer();local p=Players[pid];if not p then return end
 for _,c in p:GetCities():Members()do local b=GetCityBanner(pid,c:GetID());if b then attach(b)end end
end
LuaEvents.SPC_LevelBannerReady.Add(ready)
local baseShutdown=OnShutdown
function OnShutdown()
 LuaEvents.SPC_LevelBannerReady.Remove(ready)
 if baseShutdown then baseShutdown()end
end
