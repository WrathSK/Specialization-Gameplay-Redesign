-- Fixed institution category at the top of city details. UI-only, no requests or polling.
include('InstanceManager')
include('InstitutionPresentation')
local M=SPCInstitutionPresentation
local parent,last
local rows=InstanceManager:new('InstitutionRowInstance','Top',Controls.InstitutionRows)
local roman={'Ⅰ','Ⅱ','Ⅲ','Ⅳ'}
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
 if not v then Controls.InstitutionContainer:SetHide(true);rows:ResetInstances();last=nil;size();return end
 local signature=tostring(v.owner)..':'..v.cityID..':'..v.potential..':'..tostring(v.active)..':'..tostring(v.activeStatus)
 if signature==last then return end;last=signature
 Controls.InstitutionContainer:SetHide(false)
 Controls.InstitutionHeader:SetText(Locale.Lookup('LOC_SPC_INSTITUTIONS_HEADER'))
 rows:ResetInstances()
 local known=type(v.active)=='number' and v.activeStatus~='UNKNOWN'
 local highest=0
 for _,entry in ipairs(M.Rows) do
  if entry.level<=v.potential and known and entry.level<=v.active then highest=math.max(highest,entry.level) end
 end
 for index,entry in ipairs(M.Rows) do if entry.level<=v.potential then
  local row=rows:GetInstance()
  local enabled=known and entry.level<=v.active
  local current=enabled and entry.level==highest
  local state=not known and 'UNKNOWN' or (not enabled and 'INACTIVE' or (current and 'CURRENT' or 'ENABLED'))
  row.Stage:SetText(roman[entry.level] or tostring(entry.level))
  row.Name:SetText(entry.name)
  row.State:SetText(Locale.Lookup('LOC_SPC_INSTITUTION_'..state))
  row.Name:SetAlpha(current and 1 or .9)
  row.Stage:SetAlpha(current and 1 or .8)
  row.State:SetAlpha(state=='ENABLED' and .65 or 1)
  row.Top:SetToolTipString(M.Tooltip(index,v))
 end end
 size()
end
ContextPtr:SetInitHandler(function() ContextPtr:SetHide(false);Controls.InstitutionContainer:SetHide(true);LuaEvents.SPC_InstitutionOverview.Add(render) end)
ContextPtr:SetShutdown(function() LuaEvents.SPC_InstitutionOverview.Remove(render);last=nil;rows:DestroyInstances();if parent then parent:DestroyChild(Controls.InstitutionContainer);parent=nil end end)
