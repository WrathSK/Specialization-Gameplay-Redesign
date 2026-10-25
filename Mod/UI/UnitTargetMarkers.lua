include('Probe')
local P=SPCP0
local selection,pending,requestedAt,pendingBackend
local layer=UILens.CreateLensLayerHash('Hex_Coloring_Great_People')
local ownsLayer=false
local renderedKey,lastLog,revision,backend,backendVersion
local builderPreview=false;local hooks={};local clock=0
local dirty=true;local renderDirty=false;local pumping=false;local stopped=false;local causeVersion=0
local function signal()causeVersion=causeVersion+1;dirty=true end
local function clear()
 if ownsLayer then
  local u=UI.GetHeadSelectedUnit();local row=u and GameInfo.Units[u:GetType()]
  if not row or (not row.GreatPersonClass and row.UnitType~='UNIT_NATURALIST')then
   UILens.ClearLayerHexes(layer);UILens.ToggleLayerOff(layer)
  end
  ownsLayer=false
 end
 renderedKey=nil;pending=nil
end
local function eligible()
 local pid=Game.GetLocalPlayer()
 if not P.IsTestPlayer(pid)or UI.GetInterfaceMode()~=InterfaceModeTypes.SELECTION then return nil end
 local u=UI.GetHeadSelectedUnit()
 if not u or u:GetOwner()~=pid then return nil end
 local row=GameInfo.Units[u:GetType()]
 if row and (row.UnitType=='UNIT_SETTLER'or P.CrewBase(row.UnitType)~=nil or (builderPreview and row.UnitType=='UNIT_BUILDER'))then return u end
end
local function request(u)
 ExposedMembers.SPC_P0_UISequence=(ExposedMembers.SPC_P0_UISequence or 0)+1
 pending=P.VERSION..':TARGETS:'..ExposedMembers.SPC_P0_UISequence;requestedAt=clock;pendingBackend=ExposedMembers.SPC_P0
 local ok,err=pcall(UI.RequestPlayerOperation,u:GetOwner(),PlayerOperations.EXECUTE_SCRIPT,
  {OnStart='SPC_P0_Request',Action='UNIT_TARGETS_READ',Token=pending,UnitID=u:GetID(),BuilderPreview=builderPreview})
 if not ok then clear();ExposedMembers.SPC_TargetMarkerStatus='Dispatch error: '..tostring(err)end
end
local function consume(u)
 local shared=ExposedMembers.SPC_P0 or {};local s=shared.UnitTargetSnapshot
 if not pending or not s or s.token~=pending then return end
 if shared~=pendingBackend then clear();selection=nil;dirty=true;return end
 local selected=eligible()
 if not selected or selected:GetOwner()~=u:GetOwner()or selected:GetID()~=u:GetID()or selected:GetX()~=u:GetX()or selected:GetY()~=u:GetY()then clear();selection=nil;dirty=true;return end
 if s.version~=P.VERSION or s.owner~=u:GetOwner()or s.unitID~=u:GetID()
  or s.turn~=Game.GetCurrentGameTurn()or s.x~=u:GetX()or s.y~=u:GetY()then
  clear();ExposedMembers.SPC_TargetMarkerStatus='Stale target reply discarded';return
 end
 pending=nil
 local plots={}
 if not s.error then for _,r in ipairs(s.plots or {})do
  local visibility=PlayersVisibility[s.owner]
  if visibility and visibility:IsVisible(r.plot)then plots[#plots+1]=r.plot end
 end end
 table.sort(plots)
 local nextKey=s.owner..':'..table.concat(plots,',')
 if nextKey~=renderedKey then
  clear()
  if #plots>0 then
   UILens.ClearLayerHexes(layer);ownsLayer=true
   UILens.SetLayerHexesColoredArea(layer,s.owner,plots,UI.GetColorValue('COLOR_SPC_LEGAL_TARGET'))
   UILens.ToggleLayerOn(layer)
  end
  renderedKey=nextKey
 end
 local message=s.error or (s.mode..' purple targets='..#plots..' | unknown cities='..#(s.unknown or {}))
 ExposedMembers.SPC_TargetMarkerStatus=message
 if message~=lastLog then
  print('[SPC][TARGETS] '..message)
  for _,v in ipairs(s.unknown or {})do print('[SPC][TARGET_UNKNOWN] '..v.cityID..' '..v.reason)end
  lastLog=message
 end
end
local function refresh()
 local u=eligible();local key=u and (u:GetOwner()..':'..u:GetID()..':'..u:GetX()..':'..u:GetY()..':'..Game.GetCurrentGameTurn())
 if not key then
  if selection or pending or ownsLayer then clear()end;selection=nil;dirty=false;return
 end
 if key~=selection then clear();selection=key;dirty=true end
 if dirty then dirty=false;clear();request(u)end
 consume(u)
end
local function pump()
 if stopped or pumping then return end
 local shared=ExposedMembers.SPC_P0;local r=ExposedMembers.SPC_RuntimeUIRevision or 0
 if backend~=shared or backendVersion~=(shared and shared.Version)then
  backend=shared;backendVersion=shared and shared.Version;selection=nil;dirty=true
 end
 if revision~=r then revision=r;dirty=true end
 local reply=shared and shared.UnitTargetSnapshot
 if not(dirty or renderDirty or pending and reply and reply.token==pending)then return end
 pumping=true;renderDirty=false;local observedCause=causeVersion
 local ok=pcall(refresh);pumping=false
 if not ok then
  pending=nil;pcall(clear);dirty=causeVersion~=observedCause;ExposedMembers.SPC_TargetMarkerStatus='TARGET_MARKER_CALLBACK_FAILED'
 end
end
local function changed(pid)
 if type(pid)~='number'or pid==Game.GetLocalPlayer()then signal()end
end
local function selectedChanged(pid)
 selection=nil;pending=nil;signal();pump()
end
local function unitChanged(pid,id)
 if type(pid)=='number'and pid~=Game.GetLocalPlayer()then return end
 if selection and type(pid)=='number'and type(id)=='number'and selection:sub(1,#(pid..':'..id..':'))~=pid..':'..id..':'then return end
 selectedChanged(pid)
end
local function toggle()
 builderPreview=not builderPreview;selectedChanged()
 ExposedMembers.SPC_TargetMarkerStatus='Builder target preview '..(builderPreview and 'ON'or 'OFF')
end
local function bind(name,fn)
 local e=P.Field(Events,name);if e and e.Add then e.Add(fn);hooks[#hooks+1]={e,fn}end
end
local function init()
 stopped=false;ContextPtr:SetHide(false)
 -- Existing timeout clock only; no native reads, reply polling or retries here.
 ContextPtr:SetUpdate(function(dt)
  clock=clock+dt
  if pending and clock-requestedAt>10 then pending=nil;renderDirty=true;ExposedMembers.SPC_TargetMarkerStatus='Target read timed out'end
 end)
 LuaEvents.SPC_ToggleBuilderTargets.Add(toggle)
 for _,name in ipairs({'CityProductionChanged','CityProductionUpdated','CityProductionCompleted','CityBuildQueueChanged','DistrictBuildProgressChanged','DistrictRemovedFromMap','PlayerTurnActivated'})do bind(name,changed)end
 for _,name in ipairs({'CityTransfered','LocalPlayerTurnBegin'})do bind(name,function()signal()end)end
 for _,name in ipairs({'UnitMoveComplete','UnitRemovedFromMap'})do bind(name,unitChanged)end
 -- Optional teleport signature is not narrowed; use the conservative UI cause.
 bind('UnitTeleported',function()selectedChanged()end)
 bind('UnitSelectionChanged',selectedChanged)
 bind('InterfaceModeChanged',function()signal();pump()end)
 bind('LocalPlayerChanged',function()backend=nil;signal();pump()end)
 bind('LoadScreenClose',function()backend=nil;signal();pump()end)
 bind('GameCoreEventPublishComplete',pump);bind('GameCoreEventPlaybackComplete',pump)
 pump()
end
ContextPtr:SetInitHandler(init)
ContextPtr:SetShutdown(function()
 stopped=true;pcall(clear);ContextPtr:ClearUpdate();LuaEvents.SPC_ToggleBuilderTargets.Remove(toggle)
 for _,h in ipairs(hooks)do h[1].Remove(h[2])end
end)
