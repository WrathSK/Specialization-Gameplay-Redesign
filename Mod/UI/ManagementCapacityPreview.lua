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
-- Governor promotion button visual states. Natively 0, 4 and 5 all read as gold and only 3 is dark,
-- so gold is kept for active levels and everything else is dark with text explaining why.
local VIS_DARK, VIS_EARNED = 3, 4
local ABILITY_COLOR = {ACTIVE="[COLOR:ResGoldLabelCS]", INACTIVE="", UNBUILT=""}

-- Ability names are the headings inside each institution's help text ("Name:" then a line break),
-- so the window reuses the one localized source instead of keeping a second name list.
local function abilityNames(help)
  local names = {}
  for heading in help:gmatch("%[NEWLINE%]%[NEWLINE%]([^%[]-)%s*%[NEWLINE%]") do
    local name = heading:match("^(.-)：$") or heading:match("^(.-):$")
    if name and name ~= "" then names[#names+1] = name end
  end
  return names
end

-- Potential is shown to the player as "institution established"; arrived capacity as "active".
-- Returns the slot visual, ability state, title note and whether the slot is furthest from active.
local function levelState(sample, level)
  local built = level <= sample.potential
  local arrived = level <= sample.arrived
  local allocated = level <= sample.draft
  local active = built and arrived
  local note = ""
  if arrived and not allocated then
    note = Locale.Lookup("LOC_SPC_CAP_WITHDRAW")
  elseif allocated and not arrived then
    note = Locale.Lookup("LOC_SPC_CAP_ARRIVES", level - sample.arrived)
  elseif arrived and not built then
    note = Locale.Lookup("LOC_SPC_CAP_ARRIVED")
  end
  local state = (active and "ACTIVE") or (built and "INACTIVE") or "UNBUILT"
  return active and VIS_EARNED or VIS_DARK, state, note, not built and not allocated and not arrived
end

local function status(sample)
  if sample.draft ~= sample.assigned then return Locale.Lookup("LOC_SPC_CAP_STATUS_UNCONFIRMED") end
  if sample.assigned == 0 then return Locale.Lookup("LOC_SPC_CAP_STATUS_IDLE") end
  if sample.arrived < sample.assigned then return Locale.Lookup("LOC_SPC_CAP_STATUS_GROWING") end
  return Locale.Lookup("LOC_SPC_CAP_STATUS_SETTLED")
end

local function render()
  local free = total - sum("draft")
  local dirty = false
  for i, sample in ipairs(examples) do
    local row = rows[i]
    for level, slot in ipairs(row.slots) do
      local visual, state, arrival, remote = levelState(sample, level)
      slot.Slot:SetDisabled(true)
      slot.Slot:SetVisState(visual)
      slot.Fade:SetHide(not remote)
      slot.Header:SetOffsetY(visual == VIS_EARNED and 4 or 3)
      slot.InstitutionIcon:SetAlpha(state == "UNBUILT" and 0.45 or 1)
      slot.Arrival:SetText(arrival)
      -- Leave the right side of the title for the arrival note.
      local room = row.slotWidth - 52
      if arrival ~= "" then room = room - slot.Arrival:GetSizeX() - 8 end
      slot.InstitutionName:SetTruncateWidth(room)
      slot.InstitutionName:SetText(slot.name)
      local text = ABILITY_COLOR[state] .. Locale.Lookup("LOC_SPC_CAP_ABILITY_" .. state)
      if ABILITY_COLOR[state] ~= "" then text = text .. "[ENDCOLOR]" end
      for _, ability in ipairs(slot.abilities) do ability.AbilityState:SetText(text) end
    end
    row.Levels:SetText(Locale.Lookup("LOC_SPC_CAP_CITY_LEVELS", sample.potential,
      math.min(sample.potential, sample.arrived)))
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

-- Vanilla slot width is 204 and the card 300 on screens of 1280 or wider; narrower screens
-- shrink both down to the slot texture's 174 minimum so four levels still fit beside the card.
local function layout()
  local width = UIManager:GetScreenSizeVal()
  local wide = width >= 1280
  local gap, card = wide and 28 or 20, wide and 300 or 240
  local slotWidth = math.max(174, math.min(204, math.floor((width - 48 - card - 4 * gap) / 4)))
  -- The window hugs the rows instead of spanning the screen.
  local rowWidth = card + 4 * (gap + slotWidth)
  Controls.Window:SetSizeX(math.min(width, math.max(1024, rowWidth + 64)))
  for _, row in ipairs(rows) do
    row.slotWidth = slotWidth
    row.Root:SetSizeX(rowWidth)
    row.Card:SetSizeX(card)
    for level, slot in ipairs(row.slots) do
      local x = card + level * gap + (level - 1) * slotWidth
      row["Path" .. level]:SetOffsetX(x - gap)
      row["Path" .. level]:SetSizeX(gap)
      slot.Slot:SetOffsetX(x)
      slot.Slot:SetSizeX(slotWidth)
      for _, ability in ipairs(slot.abilities) do
        ability.Line:SetSizeX(slotWidth - 24)
        ability.AbilityName:SetTruncateWidth(slotWidth - 90)
      end
    end
  end
  Controls.Cities:CalculateSize()
  Controls.CityScroll:CalculateSize()
  render()
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
  layout()
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
    local profession = Locale.Lookup("LOC_SPC_LEVEL_" .. sample.profession)
    row.Emblem:SetIcon(emblems[sample.profession], 50)
    row.Name:SetText(Locale.Lookup("LOC_CITY_NAME_" .. sample.city))
    row.Title:SetText(Locale.Lookup("LOC_SPC_CAP_CITY_TITLE", profession))
    for level = 1, perCity do
      local slot = {abilities={}}
      ContextPtr:BuildInstanceForControl("CapacityLevelSlot", slot, row.Slots)
      local key = "LOC_SPC_" .. sample.profession .. "_INSTITUTION_" .. level
      local help = Locale.Lookup(key .. "_HELP")
      slot.InstitutionIcon:SetIcon("ICON_SPC_LEVEL_" .. sample.profession .. "_" .. level, 24)
      slot.name = Locale.Lookup(key)
      slot.Slot:SetToolTipString(Locale.Lookup(key) .. "[NEWLINE][NEWLINE]" .. help:gsub("@SPC_METRIC@", ""))
      for _, name in ipairs(abilityNames(help)) do
        local ability = {}
        ContextPtr:BuildInstanceForControl("CapacityAbility", ability, slot.Abilities)
        ability.AbilityName:SetText(name)
        slot.abilities[#slot.abilities+1] = ability
      end
      row.slots[level] = slot
    end
    row.Minus:RegisterCallback(Mouse.eLClick, function() adjust(sample, -1) end)
    row.Plus:RegisterCallback(Mouse.eLClick, function() adjust(sample, 1) end)
    rows[i] = row
  end
  for _, sample in ipairs(examples) do sample.draft = sample.assigned end
  layout()
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
