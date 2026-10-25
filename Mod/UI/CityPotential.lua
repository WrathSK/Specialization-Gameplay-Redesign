-- B266: event-driven selected-city reads isolated from native layout failures. The legacy context name
-- is retained for package continuity; no WorldTracker badge or update timer.
include('Probe')
include('InstitutionPresentation')
include('LevelBannerModel')
include('ExpeditionTrainingDiagnostics')
local P=SPCP0;local M=SPCInstitutionPresentation;local B=SPCLevelBannerModel
local parent,key,pending,pendingMeta,view,observed,backend,backendVersion,shown,targetPort
local stopped=false;local causeVersion=0;local latest;local sourceSequence=0;local deliverySequence=0
local dirty=true;local pumping=false;local bindings={};local phase='IDLE'
local failureOwner,failureCity
local diag=SPCExpeditionTrainingDiagnostics.New(P,'CITY_PRESENTATION_UI')
local function signal()causeVersion=causeVersion+1;dirty=true end
local function clearPending()
 local m=pendingMeta;pending=nil;pendingMeta=nil
 if m then pcall(m.discard,m.owner,m.token)end
end
local function sameChannel(m)
 local shared=ExposedMembers.SPC_P0
 return shared==m.backend and shared.Version==P.VERSION and shared.PlayerActionReplies==m.parent
  and m.parent.Presentations==m.channel and m.channel.version==P.VERSION and m.channel.scope=='CITY_PRESENTATION'
  and m.channel.epoch==m.epoch and m.channel.Has==m.has and m.channel.Take==m.take and m.channel.Discard==m.discard
end
local function notify(packet)
 deliverySequence=deliverySequence+1;packet.deliverySequence=deliverySequence
 latest=packet;phase='OVERVIEW_NOTIFY';LuaEvents.SPC_PresentationChanged(packet)
end
local function resetAccepted()
 view=nil
 if latest and latest.status=='RESET'then return end
 notify({status='RESET',sourceSequence=sourceSequence,version=P.VERSION})
end
local function replay()
 if stopped then return end
 local packet=latest
 if packet and(packet.status=='RESET'or sameChannel(packet.meta))then
  LuaEvents.SPC_PresentationChanged(packet) -- fixed UI subscriber handshake; no Gameplay/native read
 else resetAccepted()end
end
local function record(stage,c,extra)
 if not diag then return end
 pcall(function()
  local v=extra or {};if c then v.owner=c:GetOwner();v.city=c:GetID()end
  diag.Record(stage,v)
 end)
end
local function layout()
 if not parent then return end
 -- The native hierarchy is Stack -> auto-sized Grid -> outer Stack.
 -- Grid has DoAutoSize; treating every ancestor as a Stack aborts refresh.
 phase='LAYOUT_ACTIONS';parent:CalculateSize();parent:ReprocessAnchoring()
 local backing=parent:GetParent();if not backing then return end
 phase='LAYOUT_BACKING';backing:DoAutoSize();backing:ReprocessAnchoring()
 local outer=backing:GetParent();if not outer then return end
 phase='LAYOUT_OUTER';outer:CalculateSize();outer:ReprocessAnchoring()
end
local hidden=true
local function hide(value)
 if hidden~=value then hidden=value;Controls.ActiveShortcut:SetHide(value);layout()end
end
local function selected()
 local pid=Game.GetLocalPlayer();local c=UI.GetHeadSelectedCity()
 if c and c:GetOwner()==pid and P.IsTestPlayer(pid)then return c end
end
local function render(c)
 if stopped then return end
 local cycle=causeVersion
 local m=view and B.View(view,c:GetOwner(),c:GetID(),c:GetX(),c:GetY())
 if stopped or causeVersion~=cycle then return end
 if not parent then
  local target=ContextPtr:LookUpControl('/InGame/CityPanel/ActionStack')
  if stopped or causeVersion~=cycle then return end
  if target then
   phase='SHORTCUT_ATTACH';Controls.ActiveShortcut:ChangeParent(target);parent=target;layout()
  end
 end
 if stopped or causeVersion~=cycle then return end
 hide(not (m and parent));if stopped or causeVersion~=cycle or not m or not parent then return end
 local text=Locale.Lookup('LOC_SPC_CITY_INSTITUTION_SHORTCUT',Locale.Lookup('LOC_SPC_LEVEL_'..m.kind),m.active)
 if stopped or causeVersion~=cycle then return end
 local signature=m.icon..':'..text
 if signature~=shown then
  phase='SHORTCUT_ICON';Controls.ActiveIcon:SetIcon(m.icon,32)
  if stopped or causeVersion~=cycle then return end
  Controls.ActiveIcon:SetSizeVal(32,32)
  if stopped or causeVersion~=cycle then return end
  Controls.ActiveShortcut:SetToolTipString(text);shown=signature
 end
end
local function consume(c)
 local m=pendingMeta;if not pending or not m then return end
 local ok,ready=false,false
 if sameChannel(m)then ok,ready=pcall(m.has,m.owner,m.token)end
 if not ok then clearPending();return end
 if not ready then return end
 local good,row=pcall(m.take,m.owner,m.token)
 if not rawequal(pendingMeta,m)then return end
 clearPending()
 if stopped or not sameChannel(m)then return end
 local pid,id,x,y=c:GetOwner(),c:GetID(),c:GetX(),c:GetY()
 if stopped or not sameChannel(m)or pendingMeta~=nil or causeVersion~=m.cause
  or key~=m.key or pid~=m.owner or id~=m.cityID or x~=m.x or y~=m.y then return end
 local reply=good and type(row)=='table'and getmetatable(row)==nil and row.presentation
 local valid=type(row)=='table'and row.owner==m.owner and row.cityID==m.cityID and row.token==m.token
  and row.action=='CITY_PRESENTATION_READ'and row.version==P.VERSION and row.epoch==m.epoch
 if not valid or type(reply)~='table'or getmetatable(reply)~=nil or reply.token~=m.token
  or reply.owner~=m.owner or reply.cityID~=m.cityID then reply=nil end
 view=M.Matches(reply,pid,id,x,y)and reply or nil
 record('INSTITUTION_UI_APPLIED',c,{requestKey=m.token,specialization=reply and reply.specialization,
  potential=reply and reply.potential,active=reply and reply.active,activeStatus=reply and reply.activeStatus,readStatus=view and 'READY'or 'UNAVAILABLE'})
 if stopped or not sameChannel(m)or causeVersion~=m.cause then return end
 notify({status=reply and not reply.error and 'READY'or 'UNAVAILABLE',view=reply,meta=m,
  sourceSequence=sourceSequence,version=P.VERSION})
end
local function refresh()
 if stopped then return end
 local cycle=causeVersion
 phase='SELECT';local c=selected()
 if stopped or causeVersion~=cycle then return end
 if not c then
  key=nil;clearPending();observed=nil;shown=nil;resetAccepted();if not stopped then hide(true)end;return
 end
 local pid,id=c:GetOwner(),c:GetID();failureOwner=pid;failureCity=id
 local x,y=c:GetX(),c:GetY()
 if stopped or causeVersion~=cycle then return end
 local k=pid..':'..id..':'..x..':'..y
 local shared=ExposedMembers.SPC_P0
 if type(shared)~='table' then clearPending();backend=nil;resetAccepted();if not stopped then hide(true)end;return end
 phase='FACT_SIGNATURE'
 local d=shared.LevelBanners
 if k~=key or backend~=shared or backendVersion~=shared.Version then
  key=k;backend=shared;backendVersion=shared.Version;clearPending();observed=nil;shown=nil;dirty=true;resetAccepted()
  if stopped or causeVersion~=cycle then return end
 end
 local f=d and d.views[pid..':'..id] or {}
 local signature=table.concat({Game.GetCurrentGameTurn(),ExposedMembers.SPC_RuntimeUIRevision or 0,
  f.specialization or '',f.potential or -1,f.active or -1,f.activeStatus or ''},':')
 if signature~=observed then observed=signature;dirty=true end
 local service=shared.PlayerActionReplies;local port=service and service.Presentations
 if targetPort~=port or(latest and latest.meta and not sameChannel(latest.meta))
  or(pendingMeta and not sameChannel(pendingMeta))then
  targetPort=port;dirty=true;clearPending();resetAccepted()
 end
 if stopped or causeVersion~=cycle then return end
 if dirty then clearPending()else consume(c)end
 if stopped or causeVersion~=cycle then return end
 -- Superseding a read is safe: only a new semantic signal can do it. Idle
 -- publication never retries, polls native facts or enumerates other cities.
 local busy=dirty and UI.IsGameCoreBusy()
 if stopped or causeVersion~=cycle then return end
 if dirty and not busy then
  dirty=false
  if shared.Version~=P.VERSION or not port or port.version~=P.VERSION or port.scope~='CITY_PRESENTATION'
   or type(port.epoch)~='number'or type(port.Has)~='function'or type(port.Take)~='function'or type(port.Discard)~='function'then
   view=nil;phase='SHORTCUT';render(c);return
  end
  ExposedMembers.SPC_P0_UISequence=(ExposedMembers.SPC_P0_UISequence or 0)+1
  pending=P.VERSION..':PRESENTATION:'..ExposedMembers.SPC_P0_UISequence
  local m={owner=pid,cityID=id,x=x,y=y,key=k,token=pending,cause=causeVersion,backend=shared,parent=service,channel=port,
   epoch=port.epoch,has=port.Has,take=port.Take,discard=port.Discard}
  pendingMeta=m
  record('INSTITUTION_UI_REQUEST',c,{requestKey=pending,projectionRevision=d and d.revision,
   specialization=f.specialization,potential=f.potential,active=f.active,activeStatus=f.activeStatus})
  if stopped or not sameChannel(m)or causeVersion~=cycle then clearPending();return end
  phase='READ_REQUEST'
  local ok=pcall(UI.RequestPlayerOperation,pid,PlayerOperations.EXECUTE_SCRIPT,
   {OnStart='SPC_P0_Request',Action='CITY_PRESENTATION_READ',CityID=id,Token=pending,
    ReplyChannel='CITY_PRESENTATION',ReplyEpoch=port.epoch})
  if stopped or not rawequal(pendingMeta,m)then return end
  if not ok then clearPending();view=nil;record('INSTITUTION_UI_SEND_FAILED',c,{readStatus='SEND_ERROR'})
  else consume(c)end
 end
 if stopped or causeVersion~=cycle then return end
 phase='SHORTCUT';render(c)
end
local function pump()
 if stopped or pumping then return end
 pumping=true;failureOwner=nil;failureCity=nil
 local ok,err=pcall(refresh)
 -- Always release, including native-control and subscriber exceptions. This
 -- does not mark facts dirty or retry a request on unchanged publish events.
 pumping=false
 if not ok then
  local failure={errorCode='PRESENTATION_CALLBACK_FAILED',readStatus='UNAVAILABLE',viewStage=phase,
   owner=failureOwner,city=failureCity}
  -- Reuse bounded/redacted diagnostic metadata; never print a raw exception.
  if SPCExpeditionTrainingDiagnostics.Failure then
   local good,details=pcall(SPCExpeditionTrainingDiagnostics.Failure,err,'CITY_PRESENTATION')
   if good then failure.errorClass=details.errorClass;failure.errorFile=details.errorFile;failure.errorLine=details.errorLine end
  end
  record('INSTITUTION_UI_FAILURE',nil,failure)
 end
 phase='IDLE'
end
local function invalidate(pid)
 if pid==nil or pid==Game.GetLocalPlayer()then signal()end
end
local function bind(source,name,fn)
 local e=source[name];if e then e.Add(fn);bindings[#bindings+1]={e,fn}end
end
ContextPtr:SetInitHandler(function()
 stopped=false;ExposedMembers.SPC_P0_UISequence=(ExposedMembers.SPC_P0_UISequence or 0)+1;sourceSequence=ExposedMembers.SPC_P0_UISequence
 ContextPtr:SetHide(false)
 Controls.ActiveShortcut:RegisterCallback(Mouse.eLClick,function()
  if stopped then return end
  local c=selected();if not c then return end
  signal();pump()
  if stopped then return end
  if view and B.View(view,c:GetOwner(),c:GetID(),c:GetX(),c:GetY())then
   LuaEvents.SPC_OpenInstitutions(c:GetOwner(),c:GetID())
  end
 end)
 for _,name in ipairs({'GovernorAssigned','GovernorEstablished','GovernorChanged','GovernorPromoted','PlayerTurnActivated'})do bind(Events,name,invalidate)end
 bind(Events,'CitySelectionChanged',function()signal();pump()end)
 bind(Events,'LocalPlayerChanged',function()key=nil;signal();pump()end)
 bind(Events,'LoadScreenClose',function()backend=nil;signal();pump()end)
 bind(Events,'GameCoreEventPublishComplete',pump)
 bind(Events,'GameCoreEventPlaybackComplete',pump)
 bind(LuaEvents,'CityPanel_LiveCityDataChanged',pump)
 bind(LuaEvents,'SPC_PresentationConsumerReady',replay)
 pump()
end)
ContextPtr:SetShutdown(function()
 stopped=true;clearPending();latest=nil;view=nil
 deliverySequence=deliverySequence+1
 pcall(LuaEvents.SPC_PresentationChanged,{status='CLOSED',sourceSequence=sourceSequence,deliverySequence=deliverySequence,version=P.VERSION})
 for _,b in ipairs(bindings)do b[1].Remove(b[2])end
 hide(true);if parent then parent:DestroyChild(Controls.ActiveShortcut);layout();parent=nil end
end)
