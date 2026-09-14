include('Probe')
local P=SPCP0
local parent,pending,elapsed,timer,unitKey,feedback
local view,viewToken,viewRequestedAt,viewReceivedAt
local clock=0;local nextView=0
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
 if view and clock-(viewReceivedAt or 0)<1.5 and view.owner==u:GetOwner() and view.unitID==u:GetID()
  and view.turn==Game.GetCurrentGameTurn() and view.x==u:GetX() and view.y==u:GetY() then return view end
end
local function readView(u)
 if viewToken and clock-viewRequestedAt>2 then viewToken=nil;view=nil end
 if viewToken then
  local v=(ExposedMembers.SPC_P0 or {}).UnitActionView
  if v and v.token==viewToken then view=v;viewReceivedAt=clock;viewToken=nil end
 end
 if not viewToken and clock>=nextView and not pending then
  ExposedMembers.SPC_P0_UISequence=(ExposedMembers.SPC_P0_UISequence or 0)+1
  viewToken=P.VERSION..':VIEW:'..ExposedMembers.SPC_P0_UISequence;viewRequestedAt=clock;nextView=clock+0.5
  local ok=pcall(UI.RequestPlayerOperation,u:GetOwner(),PlayerOperations.EXECUTE_SCRIPT,
   {OnStart='SPC_P0_Request',Action='UNIT_ACTION_VIEW',UnitID=u:GetID(),Token=viewToken})
  if not ok then viewToken=nil;view=nil end
 end
end
local function number(n) return tostring(n):gsub('%.0+$','') end
local function crewTips(v)
 if v and v.prepared then
  local name=Locale.Lookup(v.targetName)
  return '施工预览[NEWLINE]当前目标：'..name..'[NEWLINE]当前进度：'..number(v.progress)..' / '..number(v.cost)
   ..'[NEWLINE]本次投入：'..number(v.amount)..'点生产力[NEWLINE]施工后：'..number(v.after)..' / '..number(v.cost)
   ..'[NEWLINE]浪费：'..number(v.waste)..'点生产力',
   '确认施工[NEWLINE]消耗此施工队，在当前建造项目上投入'..number(v.amount)..'点生产力。[NEWLINE]此操作无法撤销。'
 end
 if v and v.legal then return '施工[NEWLINE]准备在当前建造项目上投入'..number(v.amount)..'点生产力。[NEWLINE]点击后可预览施工结果并进行确认。' end
 return '施工[NEWLINE]将施工队移动至正在建造区域、建筑或奇观的单元格，即可进行施工。'
end
local function investmentTips(v)
 local names={RESEARCH='科研',CULTURE='文化',COMMERCE='商业',INDUSTRY='工业',GOVERNMENT='政府',MILITARY='军事'}
 if v and v.prepared then
  return '投资预览[NEWLINE]当前专业：'..(names[v.specialization] or v.specialization)
   ..'[NEWLINE]当前潜力：'..v.potential..'级[NEWLINE]投资后潜力：'..v.nextPotential..'级'
   ..'[NEWLINE]消耗：1名移民[NEWLINE][NEWLINE]高级专业能力仍需满足对应的总督条件。',
   '确认投资[NEWLINE]消耗此移民，使本城专业潜力永久提高至'..v.nextPotential..'级。[NEWLINE]此操作无法撤销。'
 end
 if v and v.legal then return '投资专业化[NEWLINE]消耗1名移民，使本城专业潜力永久提高1级。'
  ..'[NEWLINE]当前潜力：'..v.potential..'级 → '..v.nextPotential..'级[NEWLINE]点击后可预览投资结果并进行确认。' end
 if v and v.reason and v.reason:find('POTENTIAL_CAP_4',1,true) then return '投资专业化[NEWLINE]专业潜力已达到4级，无法继续投资。' end
 if v and v.reason and (v.reason:find('HELD',1,true) or v.reason:find('PENDING',1,true) or v.reason:find('RESERVED',1,true)) then
  return '投资专业化[NEWLINE]此前投资尚未确认，暂时无法投资。'
 end
 return '投资专业化[NEWLINE]将移民移动至本城的专业区域，即可投资城市专业化。'
end
local function dispatch(confirm)
 if pending then return end
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
 pending=P.VERSION..':PANEL:'..Game.GetCurrentGameTurn()..':'..ExposedMembers.SPC_P0_UISequence;elapsed=0
 local ok,err=pcall(UI.RequestPlayerOperation,u:GetOwner(),PlayerOperations.EXECUTE_SCRIPT,
  {OnStart='SPC_P0_Request',Action=confirm and 'UNIT_ACTION_CONFIRM' or 'UNIT_ACTION_PREPARE',UnitID=u:GetID(),Token=pending,PlanToken=p and p.token})
 feedback=ok and '正在处理，请稍候。' or '请求未送达，请查看日志。'
 if not ok then print('[SPC][B043][PANEL_ERROR] '..tostring(err));pending=nil end
end
local function update(dt)
 clock=clock+dt
 timer=timer+dt;if timer<0.2 then return end
 local step=timer;timer=0
 if not parent then
  parent=ContextPtr:LookUpControl('/InGame/UnitPanel/StandardActionsStack')
  if parent then Controls.ActionGroup:ChangeParent(parent)
  else ExposedMembers.SPC_UnitPanelStatus='UNIT_PANEL_STACK_NOT_FOUND';return end
 end
 if pending then
  elapsed=elapsed+step;local s=ExposedMembers.SPC_P0 or {}
  if s.Version==P.VERSION and s.LastToken==pending then
   feedback=tostring(s.Snapshot);ExposedMembers.SPC_UnitPanelStatus=feedback
   print('[SPC][B045][PANEL_RESULT] '..feedback);pending=nil;view=nil;viewToken=nil;nextView=0
  elseif elapsed>10 then pending=nil;feedback='等待结果超时；请查看专业化诊断中的移民 / 施工队，不要重复确认。';ExposedMembers.SPC_UnitPanelStatus=feedback end
 end
 local u,kind=current();local key=u and (u:GetOwner()..':'..u:GetID())
 if unitKey~=key then unitKey=key;feedback=nil;view=nil;viewToken=nil;nextView=0 end
 local visible=u~=nil and UI.GetInterfaceMode()==InterfaceModeTypes.SELECTION
 Controls.ActionGroup:SetHide(not visible)
 if visible then
  local invest=kind=='UNIT_SETTLER';local icon=invest and 'ICON_UNITOPERATION_FOUND_CITY' or 'ICON_UNITOPERATION_BUILD_IMPROVEMENT'
  Controls.PrepareIcon:SetIcon(icon);Controls.ConfirmIcon:SetIcon(icon)
  readView(u);local v=crewView(u);local a,b
  if invest then a,b=investmentTips(v) else a,b=crewTips(v) end
  -- Reserve both positions in both states. Confirm never replaces the first click.
  Controls.ActionGroup:SetSizeX(90)
  Controls.PrepareButton:SetOffsetX(46);Controls.ConfirmButton:SetOffsetX(0)
  Controls.PrepareButton:SetToolTipString(a);Controls.ConfirmButton:SetToolTipString(b or (invest and '确认投资' or '确认施工'))
  Controls.ConfirmButton:SetHide(not (v and v.prepared and preview(u) and preview(u).token==v.planToken))
  Controls.PrepareButton:SetDisabled(pending~=nil)
  Controls.ConfirmButton:SetDisabled(pending~=nil)
 end
 parent:CalculateSize();parent:ReprocessAnchoring()
end
ContextPtr:SetInitHandler(function()
 timer=0;ContextPtr:SetHide(false)
 Controls.PrepareButton:RegisterCallback(Mouse.eLClick,function() dispatch(false) end)
 Controls.ConfirmButton:RegisterCallback(Mouse.eLClick,function() dispatch(true) end)
 ContextPtr:SetUpdate(update)
end)
ContextPtr:SetShutdown(function() ContextPtr:ClearUpdate();Controls.ActionGroup:SetHide(true) end)
