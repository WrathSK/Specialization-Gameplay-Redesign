-- Presentation-only production action. No native project is ever queued.
SPCCommerceUI={PROJECT='PROJECT_SPC_COMMERCIALIZATION'}
local M=SPCCommerceUI
M.DOMAINS={
 {id='DISTRICT_CAMPUS',key='CAMPUS',icon='ICON_PROJECT_ENHANCE_DISTRICT_CAMPUS'},
 {id='DISTRICT_THEATER',key='THEATER',icon='ICON_PROJECT_ENHANCE_DISTRICT_THEATER'},
 {id='DISTRICT_INDUSTRIAL_ZONE',key='INDUSTRIAL_ZONE',icon='ICON_PROJECT_ENHANCE_DISTRICT_INDUSTRIAL_ZONE'},
 {id='DISTRICT_HOLY_SITE',key='HOLY_SITE',icon='ICON_PROJECT_ENHANCE_DISTRICT_HOLY_SITE'},
 {id='DISTRICT_HARBOR',key='HARBOR',icon='ICON_PROJECT_ENHANCE_DISTRICT_HARBOR'}}
function M.Backend()return (ExposedMembers.SPC_P0 or {}).Commerce end
function M.Available(v)return type(v)=='table' and v.identity=='COMMERCE' and type(v.potential)=='number' and v.potential>=3 end
function M.Reference(pid,c)return table.concat({pid,c:GetID(),c:GetX(),c:GetY()},':')end
function M.New(P,notify,observer)
 local api={};local revision=-1
 local function localCity(c)return c and c:GetOwner()==Game.GetLocalPlayer() and P.IsTestPlayer(c:GetOwner())end
 local function view(c)local b=M.Backend();local pid,id=c:GetOwner(),c:GetID();local k=pid..':'..id;return b and b.views[k],k,b,pid,id end
 function api.Items(data)
  local c=data.City;if not localCity(c)then return end
  local result={};local v,k,b=view(c)
  for _,item in ipairs(data.ProjectItems or {})do
   if item.Type~=M.PROJECT then result[#result+1]=item
   elseif M.Available(v)then
    item.Disabled=false;item.SPC_CommerceAction=true;item.TurnsLeft=0;item.Progress=0;item.Cost=0
    item.ToolTip=Locale.Lookup('LOC_SPC_COMMERCE_OPEN_HELP');result[#result+1]=item
   end
  end
  data.ProjectItems=result
  if observer then observer.Observe(b,k,v)end
 end
 function api.Before(c,item,queued)
  if not item or item.Type~=M.PROJECT then return true end
  -- This remains false even for stale/disabled/current-production list items.
  -- The visible dashboard owns the subsequent explicit domain selection.
  if localCity(c) and M.Available(view(c))then LuaEvents.SPC_CommerceOpen(c:GetOwner(),c:GetID())end
  return false
 end
 function api.Publish()
  local b=M.Backend()
  if observer then if not observer.SourceChanged(b)then return end
  else if not b or revision==b.revision then return end;revision=b.revision end
  local c=UI.GetHeadSelectedCity();if localCity(c)then
   if not observer then notify(c:GetOwner(),c:GetID())
   else local v,k,current,pid,id=view(c);if observer.Observe(current,k,v)then notify(pid,id)end end
  end
 end
 if observer then function api.Close()observer.Close()end end
 return api
end
