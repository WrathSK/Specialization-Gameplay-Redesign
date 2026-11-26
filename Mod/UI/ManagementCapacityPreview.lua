-- Layout study. All numbers, cities and edits belong to this UI context.
include("Probe")
local total = 10
local perCity = 4
local examples = {
  {city="WASHINGTON", profession="RESEARCH", potential=1, arrived=2, assigned=3},
  {city="BOSTON", profession="CULTURE", potential=3, arrived=1, assigned=1},
  {city="NEW_YORK", profession="COMMERCE", potential=3, arrived=2, assigned=2},
  {city="DETROIT", profession="INDUSTRY", potential=4, arrived=0, assigned=0},
}
local rows = {}
local topStack, launchStack
local launchPath = "/InGame/LaunchBar/"
local topPath = "/InGame/TopPanel/"

local function sum(field)
  local used = 0
  for _, sample in ipairs(examples) do used = used + sample[field] end
  return used
end

local emblems = {
  RESEARCH="ICON_DISTRICT_CAMPUS", CULTURE="ICON_DISTRICT_THEATER",
  COMMERCE="ICON_DISTRICT_COMMERCIAL_HUB", INDUSTRY="ICON_DISTRICT_INDUSTRIAL_ZONE",
}
-- Governor promotion button visual states: 0 open, 3 unavailable, 4 earned, 5 selected.
local VIS_OPEN, VIS_LOCKED, VIS_EARNED, VIS_SELECTED = 0, 3, 4, 5

-- Level state for one slot. Arrived capacity counts only up to the confirmed allocation.
local function levelState(sample, level)
  local reached = level <= sample.potential
  if level <= sample.arrived then
    if level > sample.draft then return VIS_OPEN, Locale.Lookup("LOC_SPC_CAP_STATE_WITHDRAW") end
    if reached then return VIS_EARNED, Locale.Lookup("LOC_SPC_CAP_STATE_ACTIVE") end
    return VIS_OPEN, Locale.Lookup("LOC_SPC_CAP_STATE_ARRIVED_LOCKED")
  end
  if level <= sample.draft then
    local key = reached and "LOC_SPC_CAP_STATE_PENDING" or "LOC_SPC_CAP_STATE_PENDING_LOCKED"
    return VIS_SELECTED, Locale.Lookup(key, level - sample.arrived)
  end
  if reached then return VIS_OPEN, Locale.Lookup("LOC_SPC_CAP_STATE_OPEN") end
  return VIS_LOCKED, Locale.Lookup("LOC_SPC_CAP_STATE_LOCKED")
end

local function status(sample)
  local active = math.min(sample.arrived, sample.potential)
  local key
  if sample.draft ~= sample.assigned then key = "LOC_SPC_CAP_STATUS_UNCONFIRMED"
  elseif sample.assigned == 0 then key = "LOC_SPC_CAP_STATUS_IDLE"
  elseif sample.arrived < sample.assigned then key = "LOC_SPC_CAP_STATUS_GROWING"
  else key = "LOC_SPC_CAP_STATUS_SETTLED" end
  return Locale.Lookup(key, active)
end

local function render()
  local free = total - sum("draft")
  local dirty = false
  for i, sample in ipairs(examples) do
    local row = rows[i]
    for level, slot in ipairs(row.slots) do
      local visual, text = levelState(sample, level)
      slot.Slot:SetDisabled(true)
      slot.Slot:SetVisState(visual)
      slot.LevelState:SetText(text)
    end
    row.Status:SetText(status(sample))
    row.Points:SetText(tostring(sample.draft) .. " / " .. tostring(perCity))
    row.Minus:SetDisabled(sample.draft == 0)
    row.Plus:SetDisabled(sample.draft >= perCity or free == 0)
    if sample.draft ~= sample.assigned then dirty = true end
  end
  Controls.HUDCount:SetText(tostring(sum("assigned")) .. "/" .. tostring(total))
  Controls.Available:SetText(Locale.Lookup("LOC_SPC_CAP_FREE", free))
  Controls.Total:SetText(Locale.Lookup("LOC_SPC_CAP_TOTAL", total))
  Controls.Confirm:SetDisabled(not dirty)
  Controls.Undo:SetDisabled(not dirty)
end

local function discard()
  for _, sample in ipairs(examples) do sample.draft = sample.assigned end
  render()
end

local function closePanel()
  if UIManager:IsInPopupQueue(ContextPtr) then
    UIManager:DequeuePopup(ContextPtr)
  end
  Controls.Backdrop:SetHide(true)
  Controls.Window:SetHide(true)
  discard()
end

local function openPanel()
  local screens = ContextPtr:LookUpControl("/InGame/Screens")
  if not screens then return end
  ContextPtr:ChangeParent(screens)
  ContextPtr:SetHide(false)
  Controls.Backdrop:SetHide(false)
  Controls.Window:SetHide(false)
  UIManager:QueuePopup(ContextPtr, PopupPriority.Low, {
    RenderAtCurrentParent=true,
    InputAtCurrentParent=true,
    AlwaysVisibleInQueue=true,
  })
  Controls.ScreenAnimIn:SetToBeginning()
  Controls.ScreenAnimIn:Play()
end

local function adjust(sample, delta)
  local amount = sample.draft + delta
  if amount < 0 or amount > perCity or (delta > 0 and sum("draft") >= total) then return end
  sample.draft = amount
  render()
end

local function buildRows()
  for i, sample in ipairs(examples) do
    local row = {slots={}}
    ContextPtr:BuildInstanceForControl("CapacityCityRow", row, Controls.Cities)
    row.Emblem:SetIcon(emblems[sample.profession], 50)
    row.Name:SetText(Locale.Lookup("LOC_CITY_NAME_" .. sample.city))
    row.Title:SetText(Locale.Lookup("LOC_SPC_CAP_CITY_TITLE",
      Locale.Lookup("LOC_SPC_LEVEL_" .. sample.profession), sample.potential))
    for level = 1, perCity do
      local slot = {}
      ContextPtr:BuildInstanceForControl("CapacityLevelSlot", slot, row.Levels)
      slot.LevelName:SetText(Locale.Lookup("LOC_SPC_CAP_LEVEL_" .. level))
      row.slots[level] = slot
    end
    row.Levels:CalculateSize()
    row.Minus:RegisterCallback(Mouse.eLClick, function() adjust(sample, -1) end)
    row.Plus:RegisterCallback(Mouse.eLClick, function() adjust(sample, 1) end)
    rows[i] = row
  end
  Controls.Cities:CalculateSize()
  Controls.CityScroll:CalculateSize()
  discard()
end

local function resizeLaunch(stack)
  stack:CalculateSize()
  local width = stack:GetSizeX()
  local backing = ContextPtr:LookUpControl(launchPath .. "LaunchBacking")
  local tile = ContextPtr:LookUpControl(launchPath .. "LaunchBackingTile")
  if backing then backing:SetSizeX(width + 116) end
  if tile then tile:SetSizeX(width - 20) end
  LuaEvents.LaunchBar_Resize(width)
end

local function resizeTop()
  topStack:CalculateSize()
  local info = ContextPtr:LookUpControl(topPath .. "InfoStack")
  if info then info:CalculateSize() end
end

local function detach()
  if topStack then
    Controls.Readout:ChangeParent(Controls.Parking)
    resizeTop()
    topStack = nil
  end
  if launchStack then
    Controls.LaunchItem:ChangeParent(Controls.Parking)
    resizeLaunch(launchStack)
    launchStack = nil
  end
  closePanel()
end

local function attach()
  if not SPCP0.IsTestPlayer(Game.GetLocalPlayer()) then
    detach()
    return
  end
  -- The reparented HUD controls can be visible before the panel context is shown.
  ContextPtr:SetHide(false)
  if not topStack then
    topStack = ContextPtr:LookUpControl(topPath .. "StaticInfoStack")
    if topStack then
      Controls.Readout:ChangeParent(topStack)
      local trade = ContextPtr:LookUpControl(topPath .. "TradeRoutes")
      if trade then
        for index, child in ipairs(topStack:GetChildren()) do
          if child == trade or (trade.CData and child.CData == trade.CData) then
            -- Lua index of TradeRoutes is the zero-based slot immediately after it.
            topStack:AddChildAtIndex(Controls.Readout, index)
            break
          end
        end
      end
      resizeTop()
    end
  end
  if not launchStack then
    launchStack = ContextPtr:LookUpControl(launchPath .. "ButtonStack")
    if launchStack then
      Controls.LaunchItem:ChangeParent(launchStack)
      resizeLaunch(launchStack)
    end
  end
end

Controls.ModalBG:SetTexture("Governors_BackgroundTile_ScreenFill")
Controls.ModalScreenTitle:SetText(Locale.Lookup("LOC_SPC_CAP_TITLE"))
Controls.YieldsContainer:SetHide(true)
buildRows()
Controls.OpenButton:RegisterCallback(Mouse.eLClick, function()
  if UIManager:IsInPopupQueue(ContextPtr) then closePanel() else openPanel() end
end)
ContextPtr:SetInputHandler(function(input)
  if UIManager:IsInPopupQueue(ContextPtr) and input:GetMessageType()==KeyEvents.KeyUp
      and input:GetKey()==Keys.VK_ESCAPE then
    closePanel()
    return true
  end
  return false
end, true)
Controls.ModalScreenClose:RegisterCallback(Mouse.eLClick, closePanel)
Controls.Undo:RegisterCallback(Mouse.eLClick, discard)
Controls.Confirm:RegisterCallback(Mouse.eLClick, function()
  for _, sample in ipairs(examples) do
    sample.assigned = sample.draft
    sample.arrived = math.min(sample.arrived, sample.assigned)
  end
  render()
end)

Events.LoadGameViewStateDone.Add(attach)
Events.LoadScreenClose.Add(attach)
ContextPtr:SetInitHandler(function(isReload) if isReload then attach() end end)
ContextPtr:SetShutdown(function()
  Events.LoadGameViewStateDone.Remove(attach)
  Events.LoadScreenClose.Remove(attach)
  detach()
end)
