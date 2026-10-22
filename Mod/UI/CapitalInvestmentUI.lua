-- B241 ordinary production-list action; never enqueues a project.
SPCCapitalInvestmentUI={PROJECT='PROJECT_SPC_CAPITAL_INVESTMENT'}
local M=SPCCapitalInvestmentUI
function M.Backend()return (ExposedMembers.SPC_P0 or {}).CapitalInvestment end
function M.Reference(pid,c)return table.concat({pid,c:GetID(),c:GetX(),c:GetY()},':')end
function M.New(P,notify)
 local api={};local revision=-1
 local function localCity(c)return c and c:GetOwner()==Game.GetLocalPlayer() and P.IsTestPlayer(c:GetOwner())end
 local function view(c)local b=M.Backend();return b and b.views[c:GetOwner()..':'..c:GetID()]end
 function api.Items(data)
  local c=data.City;if not localCity(c)then return end
  local out={};local v=view(c)
  for _,item in ipairs(data.ProjectItems or {})do
   if item.Type~=M.PROJECT then out[#out+1]=item
   elseif v and v.available then
    item.Disabled=false;item.Cost=0;item.TurnsLeft=0;item.Progress=0;item.SPC_CapitalAction=true
    item.ToolTip=Locale.Lookup('LOC_SPC_CAPITAL_OPEN_HELP');out[#out+1]=item
   end
  end;data.ProjectItems=out
 end
 function api.Before(c,item,queued)
  if not item or item.Type~=M.PROJECT then return true end
  local v=localCity(c) and view(c)
  if v and v.available then LuaEvents.SPC_CapitalOpen(c:GetOwner(),c:GetID())end
  return false
 end
 function api.Publish()
  local b=M.Backend();if not b or revision==b.revision then return end;revision=b.revision
  local c=UI.GetHeadSelectedCity();if localCity(c)then notify(c:GetOwner(),c:GetID())end
 end
 return api
end
