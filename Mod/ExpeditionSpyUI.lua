-- Exact-type UI routing only; no native/global request API is patched.
SPCExpeditionSpyUI={KIND='UNIT_SPC_EXPEDITION_SPY'}
local M=SPCExpeditionSpyUI
function M.IsTeam(u)
 local ok,v=pcall(function()
  local r=u and GameInfo.Units[u:GetUnitType()]
  return r and r.UnitType==M.KIND and u:GetOwner()==Game.GetLocalPlayer() or false
 end)
 return ok and v==true
end
function M.ByID(id)
 local p=Players[Game.GetLocalPlayer()]
 return p and p:GetUnits():FindID(id)
end
local routing=false
function M.Open()
 if routing then return end
 routing=true
 local ok,err=pcall(function()
  if UI.GetInterfaceMode()~=InterfaceModeTypes.SELECTION then UI.SetInterfaceMode(InterfaceModeTypes.SELECTION)end
  LuaEvents.SPC_ExpeditionGateOpen()
 end)
 routing=false
 if not ok then print('[SPC][B185][N1_UI_ROUTE] '..tostring(err):sub(1,180))end
end
return M
