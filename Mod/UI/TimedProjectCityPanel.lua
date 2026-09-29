-- Preserve HD's city panel and its native view; no numeric turns data is replaced by strings.
include("DL_CityPanel")
include("TimedProjectDisplay")
local baseView=ViewMain
function ViewMain(data)
 baseView(data)
 local c=g_pCity
 if not SPCTimedProjectDisplay.IsCurrent(c) then return end
 local turns,note=SPCTimedProjectDisplay.Text(c:GetOwner(),c:GetID())
 Controls.ProductionNum:SetHide(false);Controls.ProductionNum:SetText(turns)
 Controls.ProductionLabel:SetText(turns=="1" and "回合后完成" or "计时项目")
 Controls.ProductionLabel:SetToolTipString(note)
 Controls.ProductionNum:SetToolTipString(note)
 Controls.ProductionTurnsBar:SetPercent(0);Controls.ProductionTurnsBar:SetShadowPercent(0)
end
LuaEvents.SPC_TimedProjectDisplayChanged.Add(function(pid,id)
 if g_pCity and g_pCity:GetOwner()==pid and g_pCity:GetID()==id then Refresh()end
end)
