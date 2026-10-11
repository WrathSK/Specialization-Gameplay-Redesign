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
-- Presentation only; this mirror cannot authorize an action or alter saved binding.
function M.UnavailableText(u)
 local v=M.ActivityView(u)
 if v and v.phase=='NAMING' and v.trainingToken then
  local n=ExposedMembers.SPC_ExpeditionTrainingNameStatus
  if n and n.owner==v.owner and n.unitID==v.unitID and n.teamKey==v.teamKey then
   if n.status=='STOPPED' then return Locale.Lookup('LOC_SPC_EXPEDITION_SPY_NAME_STOPPED',n.reason or 'UNKNOWN')end
   if n.status=='WAITING' then return Locale.Lookup('LOC_SPC_EXPEDITION_SPY_NAME_WAITING')end
  end
  return Locale.Lookup('LOC_SPC_EXPEDITION_SPY_NAME_PENDING')
 end
 return Locale.Lookup('LOC_SPC_EXPEDITION_SPY_ACTION_UNAVAILABLE')
end
-- Native-like selection routing is presentation only. Read the selected team's
-- current city through the native city lookup; unreadable facts never guess a
-- mission menu from a foreign-owned plot or a saved target. Keep ordinary Spy
-- selection and all explicit action controls on their existing paths.
local function selectionMode(u)
 if ExposedMembers and ExposedMembers.SPC_ExpeditionGateUIOpenVersion~=nil then return nil end
 local selected=UI.GetHeadSelectedUnit()
 if not M.IsTeam(u) or not M.IsTeam(selected) or selected:GetOwner()~=u:GetOwner()
  or selected:GetID()~=u:GetID()then return nil end
 local v=M.ActivityView(u)
 if not v or M.ActivityLocked(u)then return nil end
 local ok,mode=pcall(function()
  if u:GetX()~=v.x or u:GetY()~=v.y or not u:IsReadyToMove()
   or UnitManager.GetActivityType(u)~=ActivityTypes.ACTIVITY_AWAKE then return nil end
  local plot=Map.GetPlot(u:GetX(),u:GetY())
  local city=plot and Cities.GetPlotPurchaseCity(plot)
  if not city then return nil end
  local owner,id=city:GetOwner(),city:GetID()
  if type(owner)~='number' or owner<0 or owner%1~=0 or type(id)~='number' or id<0 or id%1~=0 then return nil end
  local player=Players[owner]
  local current=player and player:GetCities():FindID(id)
  if not current or current:GetOwner()~=owner or current:GetID()~=id
   or current:GetX()~=city:GetX() or current:GetY()~=city:GetY()then return nil end
  local desired=owner==Game.GetLocalPlayer() and 'TRAVEL' or 'TASK'
  return M.CanOpen(desired,u) and desired or nil
 end)
 return ok and mode or nil
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
function M.Open(mode,id,fromSelection)
 if routing then return false end
 local function allowed()
  local u=UI.GetHeadSelectedUnit()
  return M.IsTeam(u) and u:GetID()==id and M.CanOpen(mode,u)
   and (not fromSelection or selectionMode(u)==mode)
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
function M.OpenOnSelection(u)
 local mode=selectionMode(u)
 return mode~=nil and M.Open(mode,u:GetID(),true) or false
end
return M
