include('Probe')
local P=SPCP0
local parent,pending,pendingMeta,elapsed,unitKey,feedback
local view,viewToken,viewMeta,viewRequestedAt,viewPort
local clock=0;local dirty=true;local hooks={};local renderKey;local revision;local backend;local backendVersion
local renderDirty=true;local pumping=false;local stopped=false;local pump;local causeVersion=0
local function signal()causeVersion=causeVersion+1;dirty=true end
local function clearView()
 local m=viewMeta;viewToken=nil;viewMeta=nil
 if m then pcall(m.discard,m.owner,m.token)end
end
local function clearAction()
 local m=pendingMeta;pending=nil;pendingMeta=nil
 if m then pcall(m.discard,m.owner,m.token)end
end
local function sameChannel(m)
 local shared=ExposedMembers.SPC_P0
 return shared==m.backend and shared.Version==P.VERSION and shared.PlayerActionReplies==m.channel
  and m.channel.epoch==m.epoch and m.channel.version==P.VERSION
  and m.channel.Has==m.has and m.channel.Take==m.take and m.channel.Discard==m.discard
end
local function sameViewChannel(m)
 local shared=ExposedMembers.SPC_P0
 return shared==m.backend and shared.Version==P.VERSION and shared.PlayerActionReplies==m.parent
  and m.parent.Views==m.channel and m.channel.epoch==m.epoch and m.channel.version==P.VERSION
  and m.channel.scope=='UNIT_VIEW'and m.channel.Has==m.has
  and m.channel.Take==m.take and m.channel.Discard==m.discard
end
local function viewReady()
 local m=viewMeta;if not viewToken or not m then return false end
 if not sameViewChannel(m)then return true end
 local ok,value=pcall(m.has,m.owner,m.token);return not ok or value==true
end
local function consumeView(u)
 local m=viewMeta;if not m or not viewReady()then return end
 local ok,row=false,nil
 if sameViewChannel(m)then ok,row=pcall(m.take,m.owner,m.token)end
 if not rawequal(viewMeta,m)then return end
 clearView() -- a native selection read must not keep an old expected reply alive
 local v=ok and type(row)=='table'and getmetatable(row)==nil and row.view
 if type(v)~='table'or getmetatable(v)~=nil then view=nil;return end
 if row.owner~=m.owner or row.unitID~=m.unitID or row.token~=m.token
  or row.action~='UNIT_ACTION_VIEW'or row.epoch~=m.epoch or row.version~=P.VERSION
  or v.owner~=m.owner or v.unitID~=m.unitID or v.token~=m.token then view=nil;return end
 local valid=v.owner==u:GetOwner()and v.unitID==u:GetID()
  and v.turn==Game.GetCurrentGameTurn()and v.x==u:GetX()and v.y==u:GetY()
  and not stopped and sameViewChannel(m)and not pending and viewMeta==nil
 view=valid and v or nil
end
local function actionReady()
 local m=pendingMeta;if not pending or not m then return false end
 if not sameChannel(m)then return true end -- one explicit invalidation, never replay
 local ok,value=pcall(m.has,m.owner,m.token);return not ok or value==true
end
local function consumeAction()
 local m=pendingMeta;if not m or not actionReady()then return false end
 local localOwner=Game.GetLocalPlayer()
 local ok,row=false,nil
 if sameChannel(m)and localOwner==m.owner then ok,row=pcall(m.take,m.owner,m.token)end
 local valid=ok and type(row)=='table'and row.owner==m.owner and row.token==m.token
  and row.action==m.action and row.unitID==m.unitID and row.epoch==m.epoch
  and row.version==P.VERSION and type(row.text)=='string'and not stopped and sameChannel(m)
 clearAction() -- release before controls/notify can reenter
 feedback=valid and row.text or '操作结果暂不可确认；请查看诊断，不要重复确认。'
 ExposedMembers.SPC_UnitPanelStatus=feedback
 if valid then print('[SPC][B045][PANEL_RESULT] '..feedback)end
 view=nil;clearView();dirty=true
 return true
end
local function current()
 local pid=Game.GetLocalPlayer();if not P.IsTestPlayer(pid) then return nil end
 local u=UI.GetHeadSelectedUnit();if not u or u:GetOwner()~=pid then return nil end
 local row=GameInfo.Units[u:GetType()]
 if row and (row.UnitType=='UNIT_SETTLER' or P.CrewBase(row.UnitType)~=nil) then return u,row.UnitType end
end
local function preview(u)
 local s=ExposedMembers.SPC_P0 or {};local p=s.UnitActionPreview
 if p and p.owner==u:GetOwner() and p.unitID==u:GetID() and p.turn==Game.GetCurrentGameTurn()
  and p.x==u:GetX() and p.y==u:GetY() then return p end
end
-- Raw responses remain in SPC_UnitPanelStatus/log; tooltips use structured views.
local function crewView(u)
 if view and view.owner==u:GetOwner() and view.unitID==u:GetID()
  and view.turn==Game.GetCurrentGameTurn() and view.x==u:GetX() and view.y==u:GetY() then return view end
end
local function readView(u)
 if stopped then return end
 if pending then dirty=false;return end
 local shared=ExposedMembers.SPC_P0
 if not shared or shared.Version~=P.VERSION then dirty=false;view=nil;clearView();return end
 if dirty then view=nil;clearView()end
 consumeView(u)
 if stopped then return end
 if not viewToken and dirty then
  dirty=false
  local owner,id=u:GetOwner(),u:GetID()
  if stopped then return end
  shared=ExposedMembers.SPC_P0
  local parent=shared and shared.PlayerActionReplies;local channel=parent and parent.Views
  if not shared or shared.Version~=P.VERSION or not channel or channel.version~=P.VERSION
   or channel.scope~='UNIT_VIEW'or type(channel.epoch)~='number'or type(channel.Has)~='function'
   or type(channel.Take)~='function'or type(channel.Discard)~='function'then return end
  ExposedMembers.SPC_P0_UISequence=(ExposedMembers.SPC_P0_UISequence or 0)+1
  viewToken=P.VERSION..':VIEW:'..ExposedMembers.SPC_P0_UISequence;viewRequestedAt=clock
  viewPort=channel -- this request already observes the new endpoint; do not resample it next publish
  viewMeta={owner=owner,unitID=id,token=viewToken,backend=shared,parent=parent,
   channel=channel,epoch=channel.epoch,has=channel.Has,take=channel.Take,discard=channel.Discard}
  local attempt=viewMeta
  local ok=pcall(UI.RequestPlayerOperation,owner,PlayerOperations.EXECUTE_SCRIPT,
   {OnStart='SPC_P0_Request',Action='UNIT_ACTION_VIEW',UnitID=id,Token=viewToken,
    ReplyChannel='UNIT_VIEW',ReplyEpoch=channel.epoch})
  if stopped or not rawequal(viewMeta,attempt)then return end
  if not ok then clearView();view=nil else consumeView(u)end
 end
end

local function number(n) return tostring(n):gsub('%.0+$','') end
local function crewTips(v)
 if v and v.prepared then
  local name=Locale.Lookup(v.targetName)
  return '施工预览[NEWLINE]当前目标：'..name..'[NEWLINE]当前进度：'..number(v.progress)..' / '..number(v.cost)
   ..'[NEWLINE]'..Locale.Lookup('LOC_SPC_CREW_BASE_PREVIEW',v.amount,v.baseInput,v.baseUnused),
   '确认施工[NEWLINE]'..Locale.Lookup('LOC_SPC_CREW_BASE_CONFIRM',v.baseInput)
 end
 if v and v.legal then return '施工[NEWLINE]'..Locale.Lookup('LOC_SPC_CREW_BASE_READY',v.amount) end
 return '施工[NEWLINE]将施工队移动至正在建造奇观的单元格，即可进行施工。'
end
local function investmentTips(v)
 local names={RESEARCH='科研',CULTURE='文化',COMMERCE='商业',INDUSTRY='工业',GOVERNMENT='政府',MILITARY='军事'}
 if v and v.prepared then
  return '专业投资预览[NEWLINE]当前专业：'..(names[v.specialization] or v.specialization)
   ..'[NEWLINE]当前潜力：'..v.potential..'级[NEWLINE]投资后潜力：'..v.nextPotential..'级'
   ..'[NEWLINE]本次消耗：1 名移民[NEWLINE][NEWLINE]提示：更高阶的专业能力仍需满足对应的总督就职与晋升条件方可启用。',
   '确认专业投资[NEWLINE]消耗此移民，使本城的专业潜力永久提升至 '..v.nextPotential..' 级。[NEWLINE]此操作一旦确认无法撤销。'
 end
 if v and v.legal then return '投资专业化[NEWLINE]消耗 1 名移民，使本城的专业潜力永久提升 1 级。'
  ..'[NEWLINE]潜力变化：'..v.potential..' 级 → '..v.nextPotential..' 级[NEWLINE]点击以预览投资结果并进行最终确认。' end
 if v and v.reason and v.reason:find('POTENTIAL_CAP_4',1,true) then return '投资专业化[NEWLINE]专业潜力已达到4级，无法继续投资。' end
 if v and v.reason and (v.reason:find('HELD',1,true) or v.reason:find('PENDING',1,true) or v.reason:find('RESERVED',1,true)) then
  return '投资专业化[NEWLINE]此前专业投资的结果尚待确认，暂时无法再次投资。'
 end
 return '投资专业化[NEWLINE]将移民移动至本城的专业区域，即可投资城市专业化。'
end
local function dispatch(confirm)
 if stopped then return end
 if stopped or pending then return end
 local u,kind=current();if not u then return end
 local p=preview(u)
 do
  local v=crewView(u)
  if not v or not v.legal then return end
  if not confirm and v.prepared then return end -- Preview click is intentionally inert.
  if confirm and (not v.prepared or not p or p.token~=v.planToken) then return end
 end
 if confirm and not p then return end
 ExposedMembers.SPC_P0_UISequence=(ExposedMembers.SPC_P0_UISequence or 0)+1
 local owner,id,turn=u:GetOwner(),u:GetID(),Game.GetCurrentGameTurn()
 if stopped then return end
 local shared=ExposedMembers.SPC_P0;local channel=shared and shared.PlayerActionReplies
 if not shared or shared.Version~=P.VERSION or not channel or channel.version~=P.VERSION
  or channel.scope~='UNIT_ACTION'or type(channel.epoch)~='number'or type(channel.Has)~='function'
  or type(channel.Take)~='function'or type(channel.Discard)~='function'then
  ExposedMembers.SPC_UnitPanelStatus='操作结果通道尚未就绪；未发送操作。';return
 end
 clearView()
 pending=P.VERSION..':PANEL:'..turn..':'..ExposedMembers.SPC_P0_UISequence;elapsed=0;renderDirty=true
 local action=confirm and 'UNIT_ACTION_CONFIRM'or 'UNIT_ACTION_PREPARE'
 pendingMeta={owner=owner,unitID=id,token=pending,action=action,backend=shared,channel=channel,
  epoch=channel.epoch,has=channel.Has,take=channel.Take,discard=channel.Discard}
 local attempt=pendingMeta
 local ok,err=pcall(UI.RequestPlayerOperation,owner,PlayerOperations.EXECUTE_SCRIPT,
  {OnStart='SPC_P0_Request',Action=action,UnitID=id,Token=pending,PlanToken=p and p.token,
   ReplyChannel='UNIT_ACTION',ReplyEpoch=channel.epoch})
 if stopped or not rawequal(pendingMeta,attempt)then return end -- an older send cannot clear a later action
 feedback=ok and '正在处理，请稍候。' or '请求未送达，请查看日志。'
 if not ok then print('[SPC][B043][PANEL_ERROR] '..tostring(err));clearAction()end
end
local function refresh()
 if not parent then
  parent=ContextPtr:LookUpControl('/InGame/UnitPanel/StandardActionsStack')
  if parent then Controls.ActionGroup:ChangeParent(parent)
  else ExposedMembers.SPC_UnitPanelStatus='UNIT_PANEL_STACK_NOT_FOUND';dirty=false;return end
 end
 local acknowledged=consumeAction() -- a completed source unit may already be gone
 if stopped then return end
 local u,kind=current();local key=u and (u:GetOwner()..':'..u:GetID()..':'..u:GetX()..':'..u:GetY()..':'..Game.GetCurrentGameTurn())
 if stopped then return end
 if unitKey~=key then
  unitKey=key;if not acknowledged then feedback=nil end;view=nil;clearView();dirty=true
 end
 local visible=u~=nil and UI.GetInterfaceMode()==InterfaceModeTypes.SELECTION
 if not visible then
  if renderKey~=false then Controls.ActionGroup:SetHide(true);renderKey=false;parent:CalculateSize();parent:ReprocessAnchoring() end
  dirty=false;return
 end
 if renderKey==false or renderKey==nil then Controls.ActionGroup:SetHide(false) end
 if visible then
  local invest=kind=='UNIT_SETTLER';local icon=invest and 'ICON_SPC_RAW_INVEST_PREPARE' or 'ICON_SPC_RAW_CREW_PREPARE'
  local confirmIcon=invest and 'ICON_SPC_RAW_INVEST_CONFIRM' or 'ICON_SPC_RAW_CREW_CONFIRM'

  readView(u)
  if stopped then return end
  local selected=UI.GetHeadSelectedUnit()
  if not selected or selected:GetOwner()~=u:GetOwner()or selected:GetID()~=u:GetID()or selected:GetX()~=u:GetX()or selected:GetY()~=u:GetY()or selected:GetType()~=u:GetType()then
   view=nil;clearView();dirty=true;Controls.ActionGroup:SetHide(true);renderKey=false;return
  end
  if stopped then return end
  local v=crewView(u);local a,b
  if invest then a,b=investmentTips(v) else a,b=crewTips(v) end
  local confirmed=v and v.prepared and preview(u) and preview(u).token==v.planToken
  local newKey=icon..'|'..a..'|'..tostring(b)..'|'..tostring(confirmed)..'|'..tostring(pending~=nil)
  if newKey==renderKey then return end;renderKey=newKey
  Controls.PrepareIcon:SetIcon(icon,38);Controls.ConfirmIcon:SetIcon(confirmIcon,38)
  -- The group grows to the left only when a matching confirmation exists.
  -- Keep Prepare at the right edge; Confirm never replaces the first-click hitbox.
  Controls.ActionGroup:SetSizeX(confirmed and 90 or 44)
  Controls.ActionSlot:SetSizeX(confirmed and 93 or 47)
  Controls.PrepareButton:SetOffsetX(confirmed and 46 or 0);Controls.ConfirmButton:SetOffsetX(0)
  Controls.PrepareButton:SetToolTipString(a);Controls.ConfirmButton:SetToolTipString(b or (invest and '确认投资' or '确认施工'))
  Controls.ConfirmButton:SetHide(not confirmed)
  Controls.PrepareButton:SetDisabled(pending~=nil)
  Controls.ConfirmButton:SetDisabled(pending~=nil)
 end
 parent:CalculateSize();parent:ReprocessAnchoring()
end
-- The existing scalar timeout also releases its bounded reply slot. It performs
-- no game reads, reply polling, request, render or time-based retry.
local function tick(dt)
 clock=clock+dt
 if pending then
  elapsed=elapsed+dt
  if elapsed>10 then
   clearAction();view=nil;clearView();renderDirty=true
   feedback='等待结果超时；请查看专业化诊断中的移民 / 施工队，不要重复确认。'
   ExposedMembers.SPC_UnitPanelStatus=feedback
  end
 end
 if viewToken and clock-viewRequestedAt>2 then clearView();view=nil;renderDirty=true end
end
pump=function()
 if stopped or pumping then return end
 local shared=ExposedMembers.SPC_P0;local r=ExposedMembers.SPC_RuntimeUIRevision or 0
 if backend~=shared or backendVersion~=(shared and shared.Version)then backend=shared;backendVersion=shared and shared.Version;clearAction();view=nil;clearView();unitKey=nil;dirty=true end
 if revision~=r then revision=r;dirty=true end
 local parent=shared and shared.PlayerActionReplies;local port=parent and parent.Views
 if viewPort~=port then viewPort=port;view=nil;clearView();dirty=true end
 local action=actionReady()
 local received=viewReady()
 if not(dirty or renderDirty or action or received)then return end
 pumping=true;renderDirty=false;local observedCause=causeVersion
 local ok=pcall(refresh)
 pumping=false
 if not ok then dirty=causeVersion~=observedCause;renderDirty=false;renderKey=nil;ExposedMembers.SPC_UnitPanelStatus='UNIT_PANEL_CALLBACK_FAILED'end
end
local function mark(pid)
 if type(pid)~='number'or pid==Game.GetLocalPlayer()then signal()end
end
local function selectedChanged(pid,id)
 view=nil;clearView();signal();pump()
end
local function unitChanged(pid,id)
 if type(pid)=='number'and pid~=Game.GetLocalPlayer()then return end
 if unitKey and type(pid)=='number'and type(id)=='number'and unitKey:sub(1,#(pid..':'..id..':'))~=pid..':'..id..':'then return end
 view=nil;clearView();signal();pump()
end
local function bind(name,fn)
 local e=P.Field(Events,name);if e and e.Add then e.Add(fn);hooks[#hooks+1]={e,fn}end
end
ContextPtr:SetInitHandler(function()
 stopped=false;ContextPtr:SetHide(false)
 for _,name in ipairs({'CityProductionChanged','CityProductionUpdated','CityProductionCompleted','CityBuildQueueChanged',
  'DistrictBuildProgressChanged','DistrictRemovedFromMap','PlayerTurnActivated','GovernorEstablished','GovernorPromoted','GovernorAssigned'})do bind(name,mark)end
 -- Building map events begin with coordinates, not an owner ID.
 for _,name in ipairs({'BuildingAddedToMap','BuildingRemovedFromMap','CityTransfered','LocalPlayerTurnBegin'})do bind(name,function()signal()end)end
 for _,name in ipairs({'UnitMoveComplete','UnitRemovedFromMap'})do bind(name,unitChanged)end
 -- Optional teleport signature is not narrowed; use the conservative UI cause.
 bind('UnitTeleported',function()selectedChanged()end)
 bind('UnitSelectionChanged',selectedChanged)
 bind('InterfaceModeChanged',function()signal();pump()end)
 bind('LocalPlayerChanged',function()clearAction();backend=nil;signal();pump()end)
 bind('LoadScreenClose',function()clearAction();backend=nil;signal();pump()end)
 bind('GameCoreEventPublishComplete',pump);bind('GameCoreEventPlaybackComplete',pump)
 Controls.PrepareButton:RegisterCallback(Mouse.eLClick,function()dispatch(false)end)
 Controls.ConfirmButton:RegisterCallback(Mouse.eLClick,function()dispatch(true)end)
 ContextPtr:SetUpdate(tick);pump()
end)
ContextPtr:SetShutdown(function()
 stopped=true;clearAction();view=nil;clearView();ContextPtr:ClearUpdate();Controls.ActionGroup:SetHide(true)
 for _,h in ipairs(hooks)do h[1].Remove(h[2])end
end)
