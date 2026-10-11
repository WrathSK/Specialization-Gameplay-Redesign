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
-- Current task controls consume the Gate's transition-published scalar view,
-- never a diagnostic request reply. Restrict the lock to this exact owned unit.
function M.ActivityView(u)
 if not M.IsTeam(u)then return nil end
 local ok,v=pcall(function()
  local view=ExposedMembers and ExposedMembers.SPC_ExpeditionActivity
  if type(view)~='table' or view.owner~=Game.GetLocalPlayer() or view.owner~=u:GetOwner()
   or view.unitID~=u:GetID()then return nil end
  return view
 end)
 return ok and v or nil
end
function M.ActivityLocked(u)
 local v=M.ActivityView(u)
 return v~=nil and (v.locked==true or v.mode=='SLEEP' or v.mode=='RELEASE' or v.mode=='BLOCKED'
  or v.phase=='TASK_PREPARING' or v.phase=='TASK_RUNNING')
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
