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
-- Availability follows the existing one-shot Gate, not a second lifecycle.
function M.CanOpen(mode,u)
 local v=M.ActivityView(u)
 if not v or M.ActivityLocked(u)then return false end
 if mode=='TRAVEL'then return v.phase=='CREATED' or v.phase=='ARRIVED' end
 return mode=='TASK' and v.phase=='ARRIVED' and v.taskStart==nil
end
local routing=false
function M.SuppressNative()
 if routing then return end
 routing=true
 local ok,err=pcall(function()
  if UI.GetInterfaceMode()~=InterfaceModeTypes.SELECTION then UI.SetInterfaceMode(InterfaceModeTypes.SELECTION)end
 end)
 routing=false
 if not ok then print('[SPC][B196][N1_UI_SUPPRESS] '..tostring(err):sub(1,180))end
end
function M.Open(mode,id)
 if routing then return false end
 local function allowed()
  local u=UI.GetHeadSelectedUnit()
  return M.IsTeam(u) and u:GetID()==id and M.CanOpen(mode,u)
 end
 if not allowed()then return false end
 routing=true
 local opened=false
 local ok,err=pcall(function()
  if UI.GetInterfaceMode()~=InterfaceModeTypes.SELECTION then UI.SetInterfaceMode(InterfaceModeTypes.SELECTION)end
  -- Changing interface mode can change selection synchronously.
  if allowed()then LuaEvents.SPC_ExpeditionGateOpen(mode,id);opened=true end
 end)
 routing=false
 if not ok then print('[SPC][B196][N1_UI_OPEN] '..tostring(err):sub(1,180))end
 return ok and opened
end
return M
