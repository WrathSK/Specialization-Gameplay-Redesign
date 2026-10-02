-- Fixed institution category at the top of city details. UI-only, no requests or polling.
include('InstitutionPresentation')
local M=SPCInstitutionPresentation
local parent,last
local function top()
 local children=parent:GetChildren()
 local own=tostring(Controls.InstitutionContainer)
 if children[1] and tostring(children[1])==own then return end
 local ranks={}
 for i,c in ipairs(children) do ranks[tostring(c)]=i end
 ranks[own]=0
 -- Native SortChildren passes controls; preserve every other direct sibling's order.
 parent:SortChildren(function(a,b)return ranks[tostring(a)]<ranks[tostring(b)] end)
end
local function size()
 Controls.InstitutionRows:CalculateSize();Controls.InstitutionContainer:CalculateSize()
 if parent then
  parent:CalculateSize();parent:ReprocessAnchoring()
  local stack=ContextPtr:LookUpControl('/InGame/CityPanelOverview/PanelStack')
  if stack then stack:CalculateSize();stack:ReprocessAnchoring() end
 end
end
local function render(data,v)
 if not parent then
  parent=ContextPtr:LookUpControl('/InGame/CityPanelOverview/BreakdownStack')
  if not parent then return end
  Controls.InstitutionContainer:ChangeParent(parent)
 end
 top()
 if not v then Controls.InstitutionContainer:SetHide(true);last=nil;size();return end
 local signature=tostring(v.owner)..':'..v.cityID..':'..v.potential..':'..tostring(v.active)..':'..tostring(v.activeStatus)
 if signature==last then return end;last=signature
 Controls.InstitutionContainer:SetHide(false)
 Controls.InstitutionHeader:SetText('专业机构')
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
