-- B114: opt-in single-city UI prototype, not a saved Gameplay project.
include("HD_ActionPanel")
include("Probe")
local baseRefresh, baseInput, baseAction = OnRefresh, OnInputHandler, OnInputActionTriggered
local baseClick, baseEnd = OnEndTurnClicked, DoEndTurn
local armed, cache, dirty, submitted, popup = nil, nil, true, false, false
local serial, scans = 0, 0
local report = "B114：未开启。选中己方空队列城市后，点击开启单城测试。"
local function publish(s) report=s;ExposedMembers.SPC_TimedTurnProbeReport=s end
local function boolean(v) if type(v)~="boolean" then error("布尔状态未知") end;return v end
local function queue(c)
 local n=c:GetBuildQueue():GetSize()
 if type(n)~="number" or n<0 or n~=math.floor(n) then error("队列未知") end
 return n
end
local function mark()
 if armed then dirty=true;ContextPtr:RequestRefresh() end
end
local function stop(reason)
 armed=nil;cache=nil;dirty=true;popup=false
 publish(report.."[NEWLINE]测试关闭："..reason);ContextPtr:RequestRefresh()
end
local function readFacts()
 scans=scans+1
 local pid=Game.GetLocalPlayer()
 if not armed or not SPCP0.IsTestPlayer(pid) or pid~=armed.owner then error("玩家不匹配") end
 local p=Players[pid];local c=p:GetCities():FindID(armed.id)
 if not c or c:GetOwner()~=pid or c:GetX()~=armed.x or c:GetY()~=armed.y then error("测试城已失效") end
 if Game.GetCurrentGameTurn()~=armed.turn then error("测试回合已结束") end
 if queue(c)~=0 then error("测试城已指定生产；占用中断") end
 local f={token=armed.token,city=Locale.Lookup(c:GetName()),turn=armed.turn,production=0,other={},empty=0,unrelated=0,total=0}
 f.ready=boolean(p:IsAlive()) and boolean(p:IsTurnActiveComplete())
 f.busy=boolean(UI.IsProcessingMessages());f.sent=boolean(UI.HasSentTurnComplete())
 f.unready=boolean(p:CanUnreadyTurn())
 f.tutorial=boolean(IsTutorialRunning());f.automation=boolean(Automation.IsActive())
 local all=NotificationManager.GetAllEndTurnBlocking(pid)
 if type(all)~="table" then error("阻塞列表未知") end
 local n=0
 for k,v in pairs(all) do
  if type(k)~="number" or k<1 or k~=math.floor(k) or type(v)~="number" then error("阻塞格式未知") end
  n=n+1
 end
 if n~=#all then error("阻塞列表不连续") end
 local prod=EndTurnBlockingTypes.ENDTURN_BLOCKING_PRODUCTION
 if prod==nil then error("生产枚举缺失") end
 for _,v in ipairs(all) do
  if v==prod then f.production=f.production+1 else f.other[#f.other+1]=v end
 end
 f.first=NotificationManager.GetFirstEndTurnBlocking(pid)
 local found=false;for _,v in ipairs(all) do if v==f.first then found=true end end
 if not found then error("首阻塞与列表不一致") end
 for _,city in p:GetCities():Members() do
  f.total=f.total+1;if f.total>128 then error("超过128城原型上限") end
  if city:GetOwner()~=pid then error("城市所有者不一致") end
  if queue(city)==0 then f.empty=f.empty+1;if city:GetID()~=armed.id then f.unrelated=f.unrelated+1 end end
 end
 -- Native target object identifies the city; camera location is not identity evidence.
 f.target=false;f.targetInfo="未读取（生产阻塞不是1）"
 if f.production==1 then
  local notification=NotificationManager.FindEndTurnBlocking(prod,pid)
  if not notification or notification:GetPlayerID()~=pid or boolean(notification:IsDismissed()) then error("生产通知归属不可确认") end
  local valid=boolean(notification:IsTargetValid())
  f.targetInfo="目标有效="..tostring(valid)
  if valid then
   local owner,id,kind=notification:GetTarget()
   if type(owner)~="number" or type(id)~="number" or kind==nil or not PlayerComponentTypes or PlayerComponentTypes.CITY==nil then error("生产通知目标字段未知") end
   f.targetInfo=f.targetInfo.."；玩家="..tostring(owner).."；对象="..tostring(id).."；类型="..tostring(kind).."（城市="..tostring(PlayerComponentTypes.CITY).."）"
   f.target=owner==pid and id==armed.id and kind==PlayerComponentTypes.CITY
  end
 end
 f.units=boolean(CheckUnitsHaveMovesState());f.ranged=boolean(CheckCityRangeAttackState())
 f.policy=false
 if boolean(Modding.IsModActive("2778f75d-9c72-4919-a081-620f6482f5d6")) then
  local culture=p:GetCulture();local completed=boolean(culture:CivicCompletedThisTurn())
  local changed=boolean(culture:PolicyChangeMade());local civic=GameInfo.Civics[culture:GetCivicCompletedThisTurn()]
  f.policy=completed and not changed and f.turn~=1 and (not civic or civic.CivicType~="CIVIC_FUTURE_CIVIC")
 end
 f.filter=f.production==1 and f.empty==1 and f.unrelated==0 and f.target
 f.operable=f.ready and not f.busy and not f.sent and not f.unready and not f.tutorial and not f.automation
 f.allow=f.filter and f.operable and #f.other==0 and not f.units and not f.ranged
 return f
end
local function summary(f)
 local reasons={}
 if not f.target then reasons[#reasons+1]="通知目标未匹配测试城" end
 if not f.ready then reasons[#reasons+1]="玩家未就绪" end
 for _,item in ipairs({{"busy","引擎处理消息中"},{"sent","已提交回合"},{"unready","回合已就绪可撤回"},{"tutorial","教程中"},{"automation","自动模式"}}) do
  if f[item[1]] then reasons[#reasons+1]=item[2] end
 end
 local names={};for _,id in ipairs(f.other) do
  local info=g_kMessageInfo[id];names[#names+1]=info and info.Message or ("未知阻塞:"..tostring(id))
 end
 return "B114 单城按钮原型｜"..f.city.."｜回合"..f.turn
  .."[NEWLINE]生产阻塞="..f.production.."；其它空城="..f.unrelated.."；通知对应测试城="..tostring(f.target)
  .."[NEWLINE]"..f.targetInfo
  .."[NEWLINE]其它阻塞："..(#names>0 and table.concat(names,"、") or "无")
  .."[NEWLINE]单位="..tostring(f.units).."；城攻击="..tostring(f.ranged).."；政策提醒="..tostring(f.policy)
  .."[NEWLINE]"..(f.allow and (f.policy and "需先确认HD政策提醒。" or "允许显示下一回合；点击时重新核对。") or "仍有真实待办或未知状态，不强制结束。")
  ..(#reasons>0 and ("[NEWLINE]未放行："..table.concat(reasons,"；")) or "")
  .."[NEWLINE]扫描次数="..scans.."；仅测试按钮/过回合，未建立固定时长项目。"
end
local function evaluate()
 local ok,f=pcall(readFacts)
 dirty=false
 if not ok then stop("原型暂停："..tostring(f));return nil end
 cache=f;publish(summary(f));return f
end
local function paint(f)
 if not f or not f.filter or not f.operable or submitted then return end
 local message,icon,tip
 if #f.other>0 then
  local info=g_kMessageInfo[f.other[1]]
  if not info then return end
  message,icon,tip=info.Message,info.Icon,info.ToolTip
 elseif f.units then message="单位需要命令";icon="ICON_NOTIFICATION_COMMAND_UNITS"
 elseif f.ranged then message="城市可发动远程攻击";icon="ICON_NOTIFICATION_CITY_RANGE_ATTACK"
 elseif f.policy then message="检查政策";icon="ICON_NOTIFICATION_CHOOSE_CIVIC"
 else message=Locale.Lookup("LOC_ACTION_PANEL_NEXT_TURN");icon="ICON_NOTIFICATION_NEXT_TURN" end
 Controls.EndTurnText:SetText(message)
 Controls.EndTurnButton:SetToolTipString(tip or (message.."[NEWLINE]单城测试：点击会重新检查其它待办。"))
 Controls.EndTurnButtonLabel:SetToolTipString(tip or message)
 Controls.CurrentTurnBlockerIcon:SetHide(false);Controls.CurrentTurnBlockerIcon:SetIcon(icon)
 Controls.CountImage:SetHide(true)
 -- Remove obsolete secondary icons only when no remaining real blockers exist.
 if #f.other==0 then
  for i=2,4 do local ctrl=Controls["TurnBlockerAlpha"..i];if ctrl then ctrl:SetHide(true) end end
  Controls.OverflowCheckboxGroup:SetHide(true)
 end
end
function OnRefresh()
 baseRefresh()
 if armed and not submitted then paint(dirty and evaluate() or cache) end
end
local function send(f)
 if submitted then return end
 submitted=true -- before native request; uncertain result stays latched, no blind retry
 publish(summary(f).."[NEWLINE]已发送一次测试结束请求；等待引擎回合变化。")
 local ok,err=pcall(function() UI.RequestAction(ActionTypes.ACTION_ENDTURN,{REASON="UserForced"}) end)
 if not ok then publish(report.."[NEWLINE]请求结果未知："..tostring(err).."；禁止重试，请截图。") end
 ContextPtr:RequestRefresh()
end
local function explicit()
 if submitted or popup then return end
 if not armed then return baseClick() end
 local f=evaluate()
 if not f or not f.filter or not f.operable then return baseClick() end
 if #f.other>0 then return baseEnd(f.other[1]) end
 if f.units then UI.SelectNextReadyUnit();return end
 if f.ranged then
  local city=Players[Game.GetLocalPlayer()]:GetCities():GetFirstRangedAttackCity()
  if city then UI.SelectCity(city);UI.SetInterfaceMode(InterfaceModeTypes.CITY_RANGE_ATTACK) end
  return
 end
 if f.policy then
  local token=f.token
  local ok,err=pcall(function()
   local dialog=PopupDialogInGame:new("SPCTimedPolicyConfirm")
   dialog:AddTitle(Locale.Lookup("LOC_FF16_NEWPOLICY_TITLE"))
   dialog:AddText(Locale.Lookup("LOC_FF16_NEWPOLICY_DESC"))
   dialog:AddCancelButton(Locale.Lookup("LOC_FF16_NEWPOLICY_CHANGE"),function()
    popup=false;LuaEvents.NotificationPanel_GovernmentOpenPolicies();mark()
   end)
   dialog:AddConfirmButton(Locale.Lookup("LOC_FF16_NEWPOLICY_CONTINUE"),function()
    popup=false
    if submitted or not armed or armed.token~=token then return end
    local fresh=evaluate()
    if fresh and fresh.token==token and fresh.allow then send(fresh) else ContextPtr:RequestRefresh() end
   end)
   popup=true;dialog:Open()
  end)
  if not ok then popup=false;stop("政策确认不可用："..tostring(err)) end
  return
 end
 if f.allow then send(f) end
end
-- Explicit player entry points only. DoEndTurn itself stays the unmodified HD path.
function OnEndTurnClicked() return explicit() end
function OnInputActionTriggered(id)
 if id==Input.GetActionId("EndTurn") then return explicit() end
 return baseAction(id)
end
local function input(event)
 if event:GetMessageType()==KeyEvents.KeyUp and event:GetKey()==Keys.VK_RETURN and not event:IsShiftDown() then
  explicit();return true
 end
 return baseInput(event) -- native Shift+Enter remains native, not prototype evidence
end
local function command(action)
 if action=="READ" then publish(report);return end
 if action=="CLEAR" then
  if submitted then publish(report.."[NEWLINE]请求已在途，不能解除防重。") else stop("手动取消") end
  return
 end
 if action~="ARM" or submitted or popup then return end
 local ok,f=pcall(function()
  local pid=Game.GetLocalPlayer();local c=UI.GetHeadSelectedCity()
  if not SPCP0.IsTestPlayer(pid) or not c or c:GetOwner()~=pid then error("请选择己方测试城市") end
  if queue(c)~=0 then error("请先使该城没有生产目标；原型不清队列") end
  return {owner=pid,id=c:GetID(),x=c:GetX(),y=c:GetY(),turn=Game.GetCurrentGameTurn()}
 end)
 if not ok then stop("无法开启："..tostring(f));return end
 serial=serial+1;f.token=serial;armed=f;scans=0;mark()
 publish("B114：已开启单城测试。仅此城缺生产时，右下角将显示下一回合。右键报告取消。")
end
local function turn(pid)
 if armed and (pid~=armed.owner or Game.GetCurrentGameTurn()~=armed.turn) then
  stop("回合/玩家改变；本次测试结束，未发放收益")
  submitted=false
 end
end
LuaEvents.SPC_TimedTurnProbe.Add(command)
Events.PlayerTurnActivated.Add(turn)
-- Coalesced native events; no frame/hover scan. A fresh check is mandatory on every explicit action.
for _,name in ipairs({"EndTurnDirty","EndTurnBlockingChanged","CityProductionChanged","NotificationAdded","NotificationDismissed", "ResearchChanged","UnitOperationSegmentComplete","UnitOperationsCleared","UserOptionChanged","CityRemovedFromMap"}) do
 Events[name].Add(mark)
end
ContextPtr:SetRefreshHandler(OnRefresh)
ContextPtr:SetInputHandler(input,true)
publish(report)
