include('Probe')
local P=SPCP0
local selection,pending,timer,age,active
local layer=UILens.CreateLensLayerHash('Hex_Coloring_Great_People')
local ownsLayer=false
local renderedKey,lastLog;local revision
local builderPreview=false
local hooks={}
local function clear()
 if ownsLayer then
  local u=UI.GetHeadSelectedUnit();local row=u and GameInfo.Units[u:GetType()]
  -- A newly selected native great person/naturalist owns this layer now.
  if not row or (not row.GreatPersonClass and row.UnitType~='UNIT_NATURALIST') then
   UILens.ClearLayerHexes(layer);UILens.ToggleLayerOff(layer)
  end
  ownsLayer=false
 end
 renderedKey=nil
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
 pending=nil
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
 local u=eligible();local key=u and (u:GetOwner()..':'..u:GetID()..':'..u:GetX()..':'..u:GetY()..':'..Game.GetCurrentGameTurn()) or nil
 if not key then if selection or pending then clear() end;selection=nil;return end
 local r=ExposedMembers.SPC_RuntimeUIRevision or 0;if r~=revision then revision=r;selection=nil end
 if key~=selection then selection=key;request(u) end
 age=(age or 0)+step
 if pending then
  local shared=ExposedMembers.SPC_P0 or {};local s=shared.UnitTargetSnapshot
  if s and s.version==P.VERSION and s.token==pending and s.owner==u:GetOwner() and s.unitID==u:GetID() then
   pending=nil
   local plots={}
   if not s.error then
    for _,r in ipairs(s.plots or {}) do
     local visibility=PlayersVisibility[s.owner]
     if visibility and visibility:IsVisible(r.plot) then plots[#plots+1]=r.plot end
    end
   end
   table.sort(plots)
   local nextKey=s.owner..':'..table.concat(plots,',')
   if nextKey~=renderedKey then
    clear()
    if #plots>0 then
     local ok,err=pcall(function()
      UILens.ClearLayerHexes(layer);ownsLayer=true
      UILens.SetLayerHexesColoredArea(layer,s.owner,plots,UI.GetColorValue('COLOR_SPC_LEGAL_TARGET'))
      UILens.ToggleLayerOn(layer)
     end)
     if not ok then clear();s.error=tostring(err) end
    end
    renderedKey=nextKey
   end
   local message=s.error or (s.mode..' purple targets='..#plots..' | unknown cities='..#(s.unknown or {}))
   ExposedMembers.SPC_TargetMarkerStatus=message
   if message~=lastLog then
    print('[SPC][TARGETS] '..message)
    for _,v in ipairs(s.unknown or {}) do print('[SPC][TARGET_UNKNOWN] '..v.cityID..' '..v.reason) end
    lastLog=message
   end
  elseif age>10 then clear();ExposedMembers.SPC_TargetMarkerStatus='Target read timed out' end
 end
 -- Bounded read-only reconciliation for queue/investment changes with no selection event.
 -- No time-only retry after success/timeout; next direct change or turn reconciles.
end
local function init()
 ContextPtr:SetHide(false);timer=0;age=0;active=true
 ContextPtr:SetUpdate(function(dt) if active then update(dt) end end)
 LuaEvents.SPC_ToggleBuilderTargets.Add(toggle)
 for _,name in ipairs({'UnitSelectionChanged','InterfaceModeChanged','LoadScreenClose','CityProductionChanged','CityProductionUpdated','CityProductionCompleted','CityBuildQueueChanged','DistrictBuildProgressChanged','DistrictRemovedFromMap','CityTransfered'}) do
  local e=Events[name];if e then e.Add(changed);hooks[#hooks+1]={e,changed} end
 end
end
ContextPtr:SetInitHandler(init)
ContextPtr:SetShutdown(function()
 active=false;clear();ContextPtr:ClearUpdate();LuaEvents.SPC_ToggleBuilderTargets.Remove(toggle)
 for _,h in ipairs(hooks) do h[1].Remove(h[2]) end
end)
