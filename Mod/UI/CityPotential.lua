-- B266: event-driven selected-city reads isolated from native layout failures. The legacy context name
-- is retained for package continuity; no WorldTracker badge or update timer.
include('Probe')
include('InstitutionPresentation')
include('LevelBannerModel')
include('ExpeditionTrainingDiagnostics')
local P=SPCP0;local M=SPCInstitutionPresentation;local B=SPCLevelBannerModel
local parent,key,pending,view,observed,backend,shown
local dirty=true;local pumping=false;local bindings={};local phase='IDLE'
local failureOwner,failureCity
local diag=SPCExpeditionTrainingDiagnostics.New(P,'CITY_PRESENTATION_UI')
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
 local m=view and B.View(view,c:GetOwner(),c:GetID(),c:GetX(),c:GetY())
 if not parent then
  local target=ContextPtr:LookUpControl('/InGame/CityPanel/ActionStack')
  if target then
   phase='SHORTCUT_ATTACH';Controls.ActiveShortcut:ChangeParent(target);parent=target;layout()
  end
 end
 hide(not (m and parent));if not m or not parent then return end
 local text=Locale.Lookup('LOC_SPC_CITY_INSTITUTION_SHORTCUT',Locale.Lookup('LOC_SPC_LEVEL_'..m.kind),m.active)
 local signature=m.icon..':'..text
 if signature~=shown then
  phase='SHORTCUT_ICON';Controls.ActiveIcon:SetIcon(m.icon,32);Controls.ActiveIcon:SetSizeVal(32,32)
  Controls.ActiveShortcut:SetToolTipString(text);shown=signature
 end
end
local function consume(c)
 local reply=(ExposedMembers.SPC_P0 or {}).CityPresentationView
 if not pending or not reply or reply.token~=pending then return end
 pending=nil
 view=M.Matches(reply,c:GetOwner(),c:GetID(),c:GetX(),c:GetY()) and reply or nil
 record('INSTITUTION_UI_APPLIED',c,{requestKey=reply.token,specialization=reply.specialization,
  potential=reply.potential,active=reply.active,activeStatus=reply.activeStatus,readStatus=view and 'READY' or 'UNAVAILABLE'})
 phase='OVERVIEW_NOTIFY';LuaEvents.SPC_PresentationChanged()
end
local function refresh()
 phase='SELECT';local c=selected()
 if not c then
  hide(true);key=nil;pending=nil;view=nil;observed=nil;shown=nil;return
 end
 local pid,id=c:GetOwner(),c:GetID();failureOwner=pid;failureCity=id
 local k=pid..':'..id..':'..c:GetX()..':'..c:GetY()
 local shared=ExposedMembers.SPC_P0
 if type(shared)~='table' then hide(true);pending=nil;view=nil;backend=nil;return end
 phase='FACT_SIGNATURE'
 local d=shared.LevelBanners
 if k~=key or backend~=shared then
  key=k;backend=shared;pending=nil;view=nil;observed=nil;shown=nil;dirty=true
 end
 local f=d and d.views[pid..':'..id] or {}
 local signature=table.concat({Game.GetCurrentGameTurn(),ExposedMembers.SPC_RuntimeUIRevision or 0,
  f.specialization or '',f.potential or -1,f.active or -1,f.activeStatus or ''},':')
 if signature~=observed then observed=signature;dirty=true end
 consume(c)
 -- Superseding a read is safe: only a new semantic signal can do it. Idle
 -- publication never retries, polls native facts or enumerates other cities.
 if dirty and not UI.IsGameCoreBusy()then
  dirty=false
  ExposedMembers.SPC_P0_UISequence=(ExposedMembers.SPC_P0_UISequence or 0)+1
  pending=P.VERSION..':PRESENTATION:'..ExposedMembers.SPC_P0_UISequence
  record('INSTITUTION_UI_REQUEST',c,{requestKey=pending,projectionRevision=d and d.revision,
   specialization=f.specialization,potential=f.potential,active=f.active,activeStatus=f.activeStatus})
  phase='READ_REQUEST'
  local ok=pcall(UI.RequestPlayerOperation,pid,PlayerOperations.EXECUTE_SCRIPT,
   {OnStart='SPC_P0_Request',Action='CITY_PRESENTATION_READ',CityID=id,Token=pending})
  if not ok then pending=nil;view=nil;record('INSTITUTION_UI_SEND_FAILED',c,{readStatus='SEND_ERROR'})
  else consume(c)end
 end
 phase='SHORTCUT';render(c)
end
local function pump()
 if pumping then return end
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
 if pid==nil or pid==Game.GetLocalPlayer()then dirty=true end
end
local function bind(source,name,fn)
 local e=source[name];if e then e.Add(fn);bindings[#bindings+1]={e,fn}end
end
ContextPtr:SetInitHandler(function()
 ContextPtr:SetHide(false)
 Controls.ActiveShortcut:RegisterCallback(Mouse.eLClick,function()
  local c=selected();if not c then return end
  dirty=true;pump()
  if view and B.View(view,c:GetOwner(),c:GetID(),c:GetX(),c:GetY())then
   LuaEvents.SPC_OpenInstitutions(c:GetOwner(),c:GetID())
  end
 end)
 for _,name in ipairs({'GovernorAssigned','GovernorEstablished','GovernorChanged','GovernorPromoted','PlayerTurnActivated'})do bind(Events,name,invalidate)end
 bind(Events,'CitySelectionChanged',function()dirty=true;pump()end)
 bind(Events,'LocalPlayerChanged',function()key=nil;dirty=true;pump()end)
 bind(Events,'LoadScreenClose',function()backend=nil;dirty=true;pump()end)
 bind(Events,'GameCoreEventPublishComplete',pump)
 bind(Events,'GameCoreEventPlaybackComplete',pump)
 bind(LuaEvents,'CityPanel_LiveCityDataChanged',pump)
 pump()
end)
ContextPtr:SetShutdown(function()
 for _,b in ipairs(bindings)do b[1].Remove(b[2])end
 hide(true);if parent then parent:DestroyChild(Controls.ActiveShortcut);layout();parent=nil end
end)
