-- B112 stage A: native observation only. No queue/state writes or turn requests.
-- Preserve the installed HD -> native ActionPanel chain; this prototype targets HD.
include("HD_ActionPanel")
include("Probe")
local originalDoEndTurn = DoEndTurn
local armed, scans = nil, 0
local report = "回合原型已载入（只观察）。选中一座己方空队列城市，点击开始单城观察。"
local function publish(s)
  report = s
  ExposedMembers.SPC_TimedTurnProbeReport = s
end
local function bool(v)
  if type(v) ~= "boolean" then error("布尔接口返回未知值") end
  return v and "是" or "否"
end
local function size(city)
  local n = city:GetBuildQueue():GetSize()
  if type(n) ~= "number" or n < 0 or n ~= math.floor(n) then error("队列长度未知") end
  return n
end
local function tag(city)
  return Locale.Lookup(city:GetName()).."("..tostring(city:GetID())..")"
end
local function disarm(reason)
  armed = nil
  publish(report.."[NEWLINE]观察已关闭："..reason)
end
local function sample(optional)
  local pid = Game.GetLocalPlayer()
  if not SPCP0.IsTestPlayer(pid) or pid ~= armed.owner then error("当前玩家不匹配") end
  local player = Players[pid]
  local city = player:GetCities():FindID(armed.id)
  if not city or city:GetOwner() ~= pid or city:GetX() ~= armed.x or city:GetY() ~= armed.y then
    error("观察城已失效；不按位置恢复城市")
  end
  if Game.GetCurrentGameTurn() ~= armed.turn then error("回合已改变，请重新开始观察") end
  if size(city) ~= 0 then error("观察城已开始生产，停止本次观察") end
  local all = NotificationManager.GetAllEndTurnBlocking(pid)
  if type(all) ~= "table" then error("全部阻塞接口不可读") end
  local labels, entries, productionOnly = {}, 0, true
  local production = EndTurnBlockingTypes.ENDTURN_BLOCKING_PRODUCTION
  if production == nil then error("生产阻塞枚举缺失") end
  for k,v in pairs(all) do
    if type(k) ~= "number" or k < 1 or k ~= math.floor(k) or type(v) ~= "number" then
      error("阻塞列表不是原生数组格式")
    end
    entries = entries + 1
  end
  if entries ~= #all then error("阻塞数组不连续") end
  for _,v in ipairs(all) do
    local name = "UNKNOWN("..tostring(v)..")"
    for key,value in pairs(EndTurnBlockingTypes) do
      if value == v then name = key; break end
    end
    labels[#labels+1] = name
    if v ~= production then productionOnly = false end
  end
  local first = NotificationManager.GetFirstEndTurnBlocking(pid)
  local empty, total, unrelated = {}, 0, 0
  for _,c in player:GetCities():Members() do
    total = total + 1
    if total > 128 then error("城市数超过原型扫描上限128；覆盖未确认") end
    if c:GetOwner() ~= pid then error("城列表所有者不一致") end
    if size(c) == 0 then
      if #empty < 8 then empty[#empty+1] = tag(c) end
      if c:GetID() ~= armed.id then unrelated = unrelated + 1 end
    end
  end
  local units = CheckUnitsHaveMovesState()
  local ranged = CheckCityRangeAttackState()
  local busy, sent = UI.IsProcessingMessages(), UI.HasSentTurnComplete()
  local unready = player:CanUnreadyTurn()
  local policyEnabled = Modding.IsModActive("2778f75d-9c72-4919-a081-620f6482f5d6")
  bool(policyEnabled)
  local policy = false
  if policyEnabled then
    local culture = player:GetCulture()
    local completed, changed = culture:CivicCompletedThisTurn(), culture:PolicyChangeMade()
    bool(completed); bool(changed)
    local civic = GameInfo.Civics[culture:GetCivicCompletedThisTurn()]
    policy = completed and not changed and Game.GetCurrentGameTurn() ~= 1
      and (not civic or civic.CivicType ~= "CIVIC_FUTURE_CIVIC")
  end
  local details = "单位待行动="..bool(units).."；城市可攻击="..bool(ranged)
    .."[NEWLINE]HD政策提醒启用="..bool(policyEnabled).."；提醒条件="..bool(policy)
    .."[NEWLINE]处理中="..bool(busy).."；已提交="..bool(sent).."；可撤回="..bool(unready)
  local candidate = entries > 0 and productionOnly and first == production and unrelated == 0
    and not units and not ranged and not policy and not busy and not sent and not unready and optional == nil
  return "B112 回合阻塞原型｜只观察，不强制结束[NEWLINE]观察城："..tag(city)
    .."；回合="..tostring(armed.turn).."；采样="..scans
    .."[NEWLINE]阻塞："..(#labels > 0 and table.concat(labels,", ") or "空列表")
    .."[NEWLINE]首阻塞="..tostring(first).."；指定阻塞="..tostring(optional)
    .."[NEWLINE]空队列城："..table.concat(empty,", ").."；扫描="..total.."城；其它空城="..unrelated
    .."[NEWLINE]"..details
    .."[NEWLINE]"..(candidate and "候选条件满足；逐城阻塞覆盖仍待实机核对。" or "候选条件未满足；保留原提示。")
    .."[NEWLINE]空队列只是候选代理，不是已证实的完整生产阻塞清单。未建立定时项目。"
end
local function onCommand(action)
  if action == "READ" then publish(report); return end -- cached; no engine scan
  if action == "CLEAR" then disarm("手动取消"); return end
  if action ~= "ARM" then return end
  local ok, result = pcall(function()
    local pid = Game.GetLocalPlayer()
    if not SPCP0.IsTestPlayer(pid) then error("只允许单人本地测试文明") end
    local city = UI.GetHeadSelectedCity()
    if not city or city:GetOwner() ~= pid then error("请选中己方城市") end
    if size(city) ~= 0 then error("请先让此城没有生产目标；原型不会清除队列") end
    return {owner=pid,id=city:GetID(),x=city:GetX(),y=city:GetY(),turn=Game.GetCurrentGameTurn()}
  end)
  if not ok then armed=nil;publish("未开始观察："..tostring(result)); return end
  armed, scans = result, 0
  publish("单城观察已开始。关闭诊断面板，点击正常结束回合，再左键读取回合原型报告。"
    .."[NEWLINE]只观察，不改变生产、不强制结束。右键报告取消；读档/跨回合需重新开始。")
end
function DoEndTurn(optional)
  if armed then
    scans = scans + 1
    local ok, result = pcall(sample, optional)
    if ok then publish(result) else armed=nil;publish("原型暂停（原按钮继续）："..tostring(result)) end
    print("[SPC_TURN_PROBE] "..report)
  end
  return originalDoEndTurn(optional) -- exactly once, including unknown/failed observations
end
local function onTurn(pid)
  if armed and (pid ~= armed.owner or Game.GetCurrentGameTurn() ~= armed.turn) then disarm("回合/玩家改变") end
end
LuaEvents.SPC_TimedTurnProbe.Add(onCommand)
Events.PlayerTurnActivated.Add(onTurn)
publish(report)
-- No update loop, auto-end hook, saved property, yield writer or RequestAction.
