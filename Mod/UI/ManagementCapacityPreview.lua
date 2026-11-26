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

local function render()
  local free = total - sum("draft")
  local dirty = false
  for i, sample in ipairs(examples) do
    local row = rows[i]
    local active = math.min(sample.arrived, sample.potential)
    row.Detail:SetText(Locale.Lookup("LOC_SPC_CAP_DETAIL", active, sample.potential, sample.arrived))
    row.Points:SetText(tostring(sample.draft))
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
  Controls.Window:SetHide(true)
  discard()
end

local function adjust(sample, delta)
  local amount = sample.draft + delta
  if amount < 0 or amount > perCity or (delta > 0 and sum("draft") >= total) then return end
  sample.draft = amount
  render()
end

local function buildRows()
  for i, sample in ipairs(examples) do
    local row = {}
    ContextPtr:BuildInstanceForControl("CapacityCityRow", row, Controls.Cities)
    row.ProfessionIcon:SetIcon("ICON_SPC_INSTITUTION_" .. sample.profession .. "_BASE", 32)
    row.Name:SetText(Locale.Lookup("LOC_SPC_CAP_CITY_NAME",
      Locale.Lookup("LOC_CITY_NAME_" .. sample.city), Locale.Lookup("LOC_SPC_LEVEL_" .. sample.profession)))
    row.Minus:RegisterCallback(Mouse.eLClick, function() adjust(sample, -1) end)
    row.Plus:RegisterCallback(Mouse.eLClick, function() adjust(sample, 1) end)
    rows[i] = row
  end
  Controls.Cities:CalculateSize()
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
  Controls.Window:SetHide(true)
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

buildRows()
Controls.OpenButton:RegisterCallback(Mouse.eLClick, function()
  if Controls.Window:IsHidden() then
    ContextPtr:SetHide(false)
    Controls.Window:SetHide(false)
  else
    closePanel()
  end
end)
Controls.Close:RegisterCallback(Mouse.eLClick, closePanel)
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
