include('Probe')
local P=SPCP0
local selection,pending,requestedAt,pendingMeta,targetPort
local layer=UILens.CreateLensLayerHash('Hex_Coloring_Great_People')
local ownsLayer=false
local renderedKey,lastLog,revision,backend,backendVersion
local builderPreview=false;local hooks={};local clock=0
local dirty=true;local renderDirty=false;local pumping=false;local stopped=false;local causeVersion=0
local function signal()causeVersion=causeVersion+1;dirty=true end
local function discardPending()
 local m=pendingMeta;pending=nil;pendingMeta=nil
 if m then pcall(m.discard,m.owner,m.token)end
end
local function sameChannel(m)
 local shared=ExposedMembers.SPC_P0
 return shared==m.backend and shared.Version==P.VERSION and shared.PlayerActionReplies==m.parent
  and m.parent.Targets==m.channel and m.channel.scope=='UNIT_TARGETS'
  and m.channel.epoch==m.epoch and m.channel.version==P.VERSION
  and m.channel.Has==m.has and m.channel.Take==m.take and m.channel.Discard==m.discard
end
local function ready()
 local m=pendingMeta;if not pending or not m then return false end
 if not sameChannel(m)then return true end
 local ok,value=pcall(m.has,m.owner,m.token);return not ok or value==true
end
local function clear()
 discardPending()
 local owned=ownsLayer;ownsLayer=false
 if owned then
  local cause,selectedKey=causeVersion,selection
  local u=UI.GetHeadSelectedUnit();local row=u and GameInfo.Units[u:GetType()]
  if causeVersion==cause and selection==selectedKey and(not row or (not row.GreatPersonClass and row.UnitType~='UNIT_NATURALIST'))then
   UILens.ClearLayerHexes(layer)
   if causeVersion==cause and selection==selectedKey then UILens.ToggleLayerOff(layer)end
  end
 end
 renderedKey=nil
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
 if stopped then return end
 local shared=ExposedMembers.SPC_P0;local parent=shared and shared.PlayerActionReplies
 local port=parent and parent.Targets
 if not shared or shared.Version~=P.VERSION or not port or port.version~=P.VERSION
  or port.scope~='UNIT_TARGETS'or type(port.epoch)~='number'or type(port.Has)~='function'
  or type(port.Take)~='function'or type(port.Discard)~='function'then return end
 local owner,id=u:GetOwner(),u:GetID()
 if stopped then return end
 ExposedMembers.SPC_P0_UISequence=(ExposedMembers.SPC_P0_UISequence or 0)+1
 pending=P.VERSION..':TARGETS:'..ExposedMembers.SPC_P0_UISequence;requestedAt=clock;targetPort=port
 local m={owner=owner,unitID=id,token=pending,backend=shared,parent=parent,channel=port,
  epoch=port.epoch,has=port.Has,take=port.Take,discard=port.Discard,builder=builderPreview}
 pendingMeta=m
 if not sameChannel(m)then discardPending();return end
 local ok,err=pcall(UI.RequestPlayerOperation,owner,PlayerOperations.EXECUTE_SCRIPT,
  {OnStart='SPC_P0_Request',Action='UNIT_TARGETS_READ',Token=pending,UnitID=id,BuilderPreview=builderPreview,
   ReplyChannel='UNIT_TARGETS',ReplyEpoch=port.epoch})
 if stopped or not rawequal(pendingMeta,m)then return end
 if not ok then clear();ExposedMembers.SPC_TargetMarkerStatus='Dispatch error: '..tostring(err)end
end
local function consume(u)
 local m=pendingMeta;if not m or not ready()then return end
 local ok,row=false,nil
 if sameChannel(m)then ok,row=pcall(m.take,m.owner,m.token)end
 if not rawequal(pendingMeta,m)then return end
 discardPending() -- release the expected reply before any native selection read
 if stopped then return end
 local s=ok and type(row)=='table'and getmetatable(row)==nil and row.targets
 if not sameChannel(m)then clear();selection=nil;dirty=true;return end
 if not ok or type(row)~='table'or getmetatable(row)~=nil or row.owner~=m.owner or row.unitID~=m.unitID or row.token~=m.token
  or row.action~='UNIT_TARGETS_READ'or row.version~=P.VERSION or row.epoch~=m.epoch
  or type(s)~='table'or getmetatable(s)~=nil then
  clear();ExposedMembers.SPC_TargetMarkerStatus='TARGETS_UNAVAILABLE';return
 end
 local expectedSelection=selection;local expectedCause=causeVersion
 local function current()
  return not stopped and sameChannel(m)and pendingMeta==nil and selection==expectedSelection
   and causeVersion==expectedCause and builderPreview==m.builder
 end
 local selected=eligible()
 if stopped then return end
 if not selected or selected:GetOwner()~=u:GetOwner()or selected:GetID()~=u:GetID()or selected:GetX()~=u:GetX()or selected:GetY()~=u:GetY()then
  clear();selection=nil;dirty=true;return
 end
 if s.token~=m.token or s.version~=P.VERSION or s.owner~=u:GetOwner()or s.unitID~=u:GetID()
  or s.turn~=Game.GetCurrentGameTurn()or s.x~=u:GetX()or s.y~=u:GetY()or not current()then
  clear();ExposedMembers.SPC_TargetMarkerStatus='Stale target reply discarded';return
 end
 local plots={}
 if not s.error then for _,r in ipairs(s.plots or {})do
  local visibility=PlayersVisibility[s.owner]
  if visibility and visibility:IsVisible(r.plot)then plots[#plots+1]=r.plot end
 end end
 if not current()then return end
 table.sort(plots)
 local nextKey=s.owner..':'..table.concat(plots,',')
 if nextKey~=renderedKey then
  clear()
  if not current()then return end
  if #plots>0 then
   UILens.ClearLayerHexes(layer)
   if not current()then return end
   local color=UI.GetColorValue('COLOR_SPC_LEGAL_TARGET')
   if not current()then return end
   ownsLayer=true;UILens.SetLayerHexesColoredArea(layer,s.owner,plots,color)
   if not current()then return end
   UILens.ToggleLayerOn(layer)
   if not current()then return end
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
 if stopped then return end
 local observedCause=causeVersion
 local u=eligible();local key=u and (u:GetOwner()..':'..u:GetID()..':'..u:GetX()..':'..u:GetY()..':'..Game.GetCurrentGameTurn())
 if stopped or causeVersion~=observedCause then return end
 if not key then
  if selection or pending or ownsLayer then clear()end
  if stopped or causeVersion~=observedCause then return end
  selection=nil;dirty=false;return
 end
 if key~=selection then clear();if stopped or causeVersion~=observedCause then return end;selection=key;dirty=true end
 if dirty then dirty=false;clear();if stopped or causeVersion~=observedCause then return end;request(u)end
 if not stopped then consume(u)end
end
local function pump()
 if stopped or pumping then return end
 local shared=ExposedMembers.SPC_P0;local r=ExposedMembers.SPC_RuntimeUIRevision or 0
 if backend~=shared or backendVersion~=(shared and shared.Version)then
  backend=shared;backendVersion=shared and shared.Version;selection=nil;dirty=true
 end
 local port=shared and shared.PlayerActionReplies and shared.PlayerActionReplies.Targets
 if targetPort~=port then targetPort=port;dirty=true end
 if revision~=r then revision=r;dirty=true end
 if not(dirty or renderDirty or ready())then return end
 pumping=true;renderDirty=false;local observedCause=causeVersion
 local ok=pcall(refresh);pumping=false
 if not ok then
  pcall(clear);dirty=causeVersion~=observedCause;ExposedMembers.SPC_TargetMarkerStatus='TARGET_MARKER_CALLBACK_FAILED'
 end
end
local function changed(pid)
 if type(pid)~='number'or pid==Game.GetLocalPlayer()then signal()end
end
local function selectedChanged(pid)
 selection=nil;discardPending();signal();pump()
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
  if pending and clock-requestedAt>10 then discardPending();renderDirty=true;ExposedMembers.SPC_TargetMarkerStatus='Target read timed out'end
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
