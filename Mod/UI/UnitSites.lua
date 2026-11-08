include('Probe')
local P=SPCP0
local token,elapsed,selection
local function selected()
 local pid=Game.GetLocalPlayer()
 if not P.IsTestPlayer(pid) then return nil end
 local u=UI.GetHeadSelectedUnit()
 if not u or u:GetOwner()~=pid then return nil end
 local r=GameInfo.Units[u:GetType()]
 if r and (r.UnitType=='UNIT_SETTLER' or r.UnitType=='UNIT_BUILDER' or P.CrewBase(r.UnitType)~=nil) then return u end
end
local function refresh()
 local u=selected()
 local now=u and (u:GetID()..':'..u:GetX()..':'..u:GetY()) or nil
 if now~=selection then
  selection=now;if not token then Controls.Window:SetHide(true) end
 end
end
local function read(action)
 refresh()
 local u=selected();local city=UI.GetHeadSelectedCity()
 if (action=='UNIT_ACTION_SPAWN' and not city) or (action~='UNIT_ACTION_SPAWN' and not u) then
  Controls.Window:SetHide(false);Controls.Report:SetText('Spawn: select own city with empty center. Action: select Settler or Crew.');return
 end
 ExposedMembers.SPC_P0_UISequence=(ExposedMembers.SPC_P0_UISequence or 0)+1
 token=P.VERSION..':SITE:'..Game.GetCurrentGameTurn()..':'..ExposedMembers.SPC_P0_UISequence
 elapsed=0;Controls.Window:SetHide(false);Controls.Report:SetText('Processing '..action..'...')
 local ok,err=pcall(UI.RequestPlayerOperation,Game.GetLocalPlayer(),PlayerOperations.EXECUTE_SCRIPT,
  {OnStart='SPC_P0_Request',Action=action,UnitID=u and u:GetID(),CityID=city and city:GetID(),Token=token,PlanToken=ExposedMembers.SPC_P0 and ExposedMembers.SPC_P0.UnitActionPreview and ExposedMembers.SPC_P0.UnitActionPreview.token})
 if not ok then token=nil;Controls.Report:SetText('Dispatch error: '..tostring(err)) end
end
local function showRoot()
 ContextPtr:SetHide(not P.IsTestPlayer(Game.GetLocalPlayer()))
end
local function initialize()
 showRoot();refresh()
 Controls.SpawnCrewButton:RegisterCallback(Mouse.eLClick,function() read('UNIT_ACTION_SPAWN') end)
 Controls.PrepareUnitButton:RegisterCallback(Mouse.eLClick,function() read('UNIT_ACTION_PREPARE') end)
 Controls.ConfirmUnitButton:RegisterCallback(Mouse.eLClick,function() read('UNIT_ACTION_CONFIRM') end)
 Controls.BuilderTargetsButton:RegisterCallback(Mouse.eLClick,function() LuaEvents.SPC_ToggleBuilderTargets() end)
 Controls.CloseButton:RegisterCallback(Mouse.eLClick,function() token=nil;Controls.Window:SetHide(true) end)
 local timer=0
 ContextPtr:SetUpdate(function(dt)
  if Controls.Window:IsHidden() and not token then return end
  timer=timer+dt;if timer<0.2 then return end
  local step=timer;timer=0;refresh()
  if not token and ExposedMembers.SPC_UnitPanelStatus then Controls.Report:SetText(tostring(ExposedMembers.SPC_UnitPanelStatus):gsub("\n","[NEWLINE]")) end
  Controls.TargetStatus:SetText(ExposedMembers.SPC_TargetMarkerStatus or "操作已移到单位面板；这里保留诊断与DEV生成。")
  if token then
   elapsed=elapsed+step
   local s=ExposedMembers.SPC_P0 or {}
   if s.Version==P.VERSION and s.LastToken==token then
    local text=tostring(s.Snapshot);Controls.Report:SetText(text:gsub('\n','[NEWLINE]'))
    print('[SPC][B040][UNIT_SITE] '..text);token=nil
   elseif elapsed>=10 then token=nil;Controls.Report:SetText('No response. Send Lua.log; no action was executed.') end
  end
 end)
 print('[SPC][B040][UNIT_SITE_UI_READY] visibility fix 52')
end
ContextPtr:SetInitHandler(initialize)
Events.LoadScreenClose.Add(showRoot)
ContextPtr:SetShutdown(function() ContextPtr:ClearUpdate();Events.LoadScreenClose.Remove(showRoot) end)
