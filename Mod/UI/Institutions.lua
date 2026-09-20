-- One fixed four-row prototype in city details. No request, polling or yield writes.
include('InstitutionPresentation')
local M=SPCInstitutionPresentation
local parent,last
local function size()
 Controls.InstitutionRows:CalculateSize();Controls.InstitutionContainer:CalculateSize()
 if parent then parent:CalculateSize();parent:ReprocessAnchoring() end
end
local function render(data,v)
 if not parent then
  parent=ContextPtr:LookUpControl('/InGame/CityPanelOverview/BreakdownStack')
  if not parent then return end
  Controls.InstitutionContainer:ChangeParent(parent)
 end
 if not v then Controls.InstitutionContainer:SetHide(true);last=nil;size();return end
 local signature=tostring(v.owner)..':'..v.cityID..':'..v.potential..':'..tostring(v.active)..':'..tostring(v.activeStatus)
 if signature==last then return end;last=signature
 Controls.InstitutionContainer:SetHide(false)
 Controls.InstitutionHeader:SetText('学院 · 专业机构（展示原型）')
 for i=1,4 do
  local row=Controls['Institution'..i];row:SetHide(i>v.potential)
  Controls['InstitutionName'..i]:SetText(M.Rows[i].name)
  Controls['InstitutionState'..i]:SetText(type(v.active)~='number' and '状态待确认' or (v.active>=i and '阶段已启用' or '能力未激活'))
  row:SetToolTipString(M.Tooltip(i,v))
 end
 size()
end
ContextPtr:SetInitHandler(function() ContextPtr:SetHide(false);Controls.InstitutionContainer:SetHide(true);LuaEvents.SPC_InstitutionOverview.Add(render) end)
ContextPtr:SetShutdown(function() LuaEvents.SPC_InstitutionOverview.Remove(render);last=nil;if parent then parent:DestroyChild(Controls.InstitutionContainer);parent=nil end end)
