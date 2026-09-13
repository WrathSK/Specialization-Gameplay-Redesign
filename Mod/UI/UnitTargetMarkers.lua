include('Probe')
include('InstanceManager')
local P=SPCP0
local manager,selection,pending,timer,age,active
local builderPreview=false
local hooks={}
local function clear()
 if manager then manager:ResetInstances() end
 pending=nil
end
local function eligible()
 local pid=Game.GetLocalPlayer()
 if not P.IsTestPlayer(pid) or UI.GetInterfaceMode()~=InterfaceModeTypes.SELECTION then return nil end
 local u=UI.GetHeadSelectedUnit()
 if not u or u:GetOwner()~=pid then return nil end
 local row=GameInfo.Units[u:GetType()]
 if row and (row.UnitType=='UNIT_SETTLER' or P.CrewBase(row.UnitType)~=nil or (builderPreview and row.UnitType=='UNIT_BUILDER')) then return u end
end
local function request(u)
 clear()
 ExposedMembers.SPC_P0_UISequence=(ExposedMembers.SPC_P0_UISequence or 0)+1
 pending=P.VERSION..':TARGETS:'..ExposedMembers.SPC_P0_UISequence;age=0
 local ok,err=pcall(UI.RequestPlayerOperation,Game.GetLocalPlayer(),PlayerOperations.EXECUTE_SCRIPT,
  {OnStart='SPC_P0_Request',Action='UNIT_TARGETS_READ',Token=pending,UnitID=u:GetID(),BuilderPreview=builderPreview})
 if not ok then clear();ExposedMembers.SPC_TargetMarkerStatus='Dispatch error: '..tostring(err) end
end
local function changed() selection=nil;clear() end
local function toggle()
 builderPreview=not builderPreview;changed()
 ExposedMembers.SPC_TargetMarkerStatus='Builder target preview '..(builderPreview and 'ON' or 'OFF')
end
local function update(dt)
 timer=timer+dt;if timer<0.25 then return end
 local step=timer;timer=0
 local u=eligible();local key=u and (u:GetOwner()..':'..u:GetID()..':'..u:GetX()..':'..u:GetY()) or nil
 if not key then if selection or pending then clear() end;selection=nil;return end
 if key~=selection then selection=key;request(u) end
 age=(age or 0)+step
 if pending then
  local shared=ExposedMembers.SPC_P0 or {};local s=shared.UnitTargetSnapshot
  if s and s.version==P.VERSION and s.token==pending and s.owner==u:GetOwner() and s.unitID==u:GetID() then
   pending=nil
   local count=0
   if not s.error then
    for _,r in ipairs(s.plots or {}) do
     local visibility=PlayersVisibility[s.owner]
     if visibility and visibility:IsVisible(r.plot) then
      local instance=manager:GetInstance();local x,y=UI.GridToWorld(r.plot)
      instance.Anchor:SetWorldPositionVal(x,y,35)
      instance.Caption:SetText(s.mode);count=count+1
     end
    end
   end
   ExposedMembers.SPC_TargetMarkerStatus=s.error or (s.mode..' markers='..count..' | unknown cities='..#(s.unknown or {})..' | locations, not movement range')
   if s.unknown and s.unknown[1] then
    ExposedMembers.SPC_TargetMarkerStatus=ExposedMembers.SPC_TargetMarkerStatus..' | city '..s.unknown[1].cityID..': '..s.unknown[1].reason
   end
   print('[SPC][B041][TARGETS] '..ExposedMembers.SPC_TargetMarkerStatus)
   for _,v in ipairs(s.unknown or {}) do print('[SPC][B041][TARGET_UNKNOWN] '..v.cityID..' '..v.reason) end
  elseif age>10 then clear();ExposedMembers.SPC_TargetMarkerStatus='Target read timed out' end
 end
 -- Bounded read-only reconciliation for queue/investment changes with no selection event.
 if not pending and age>5 and not UI.IsGameCoreBusy() then request(u) end
end
local function init()
 manager=InstanceManager:new('TargetInstance','Anchor',ContextPtr)
 ContextPtr:SetHide(false);timer=0;age=0;active=true
 ContextPtr:SetUpdate(function(dt) if active then update(dt) end end)
 LuaEvents.SPC_ToggleBuilderTargets.Add(toggle)
 for _,name in ipairs({'UnitSelectionChanged','InterfaceModeChanged','LoadScreenClose'}) do
  local e=Events[name];if e then e.Add(changed);hooks[#hooks+1]={e,changed} end
 end
end
ContextPtr:SetInitHandler(init)
ContextPtr:SetShutdown(function()
 active=false;clear();ContextPtr:ClearUpdate();LuaEvents.SPC_ToggleBuilderTargets.Remove(toggle)
 for _,h in ipairs(hooks) do h[1].Remove(h[2]) end
end)
