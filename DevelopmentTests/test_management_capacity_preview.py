"""Native UI layout contract with the real preview Lua and no gameplay services."""
import sqlite3
import unittest
from contextlib import closing
from pathlib import Path
from xml.etree import ElementTree as ET

from lupa.lua51 import LuaRuntime

MOD = Path(__file__).resolve().parents[1] / "Mod"
PANEL = MOD / "UI" / "ManagementCapacityPreview"
MODEL = """
local function event()
  local e = {}
  e.Add = function(f) assert(not e.fire); e.fire = f end
  e.Remove = function(f) assert(e.fire == f); e.fire = nil end
  return e
end
Events = {LoadGameViewStateDone=event(), LoadScreenClose=event()}
Mouse = {eLClick=1}
KeyEvents={KeyUp=2}; Keys={VK_ESCAPE=27}; PopupPriority={Low=1}
texts = texts or {}
Locale = {Lookup=function(tag, ...) return texts[tag] or (tag .. table.concat({...}, "/")) end}
eligible = true
PlayerConfigurations = {[0]={
  GetCivilizationTypeName=function() return eligible and "CIVILIZATION_SPC_AMERICA" or "OTHER" end,
  GetLeaderTypeName=function() return "LEADER_SPC_T_ROOSEVELT" end}}
Players = {[0]={IsHuman=function() return true end}}
GameConfiguration = {IsAnyMultiplayer=function() return false end}
Game = {GetLocalPlayer=function() return 0 end}
include = function(name) assert(name == "Probe") end
local control = {}
function widget() return setmetatable({children={}}, {__index=control}) end
function control:GetChildren() return self.children end
function control:AddChildAtIndex(child, index)
  child:ChangeParent(self)
  table.remove(self.children)
  table.insert(self.children, index+1, child)
end
function control:ChangeParent(parent)
  if self.parent then
    for i,v in ipairs(self.parent.children) do
      if v == self then table.remove(self.parent.children,i); break end
    end
  end
  self.parent=parent
  table.insert(parent.children,self)
end
function control:SetTexture(value) self.texture=value end
function control:SetText(value) self.text=value end
function control:SetIcon(value,size) self.icon=value; self.iconSize=size end
function control:SetHide(value) self.hidden=value end
function control:IsHidden() return self.hidden end
function control:SetDisabled(value) self.disabled=value end
function control:SetVisState(value) self.vis=value end
function control:SetAlpha(value) self.alpha=value end
function control:SetOffsetX(value) self.x=value end
function control:SetTruncateWidth(value) self.truncate=value end
function control:SetToolTipString(value) self.tooltip=value end
function control:RegisterCallback(button, callback) assert(button==1); self.click=callback end
function control:CalculateSize() end
function control:GetSizeX() return self.fixedWidth or (self.text and 6*#self.text) or 200+#self.children*56 end
function control:SetSizeX(value) self.width=value end
Controls = {}
for _,id in ipairs({"Window","Backdrop","ScreenAnimIn","Readout","HUDCount","Parking","OpenButton","LaunchItem","Cities",
                    "CityScroll","ModalBG","ModalScreenTitle","ModalScreenClose","YieldsContainer","Confirm","Undo","Available","Total"}) do Controls[id]=widget() end
Controls.Window:SetHide(true)
screenWidth=1512
Controls.Backdrop:SetHide(true)
function Controls.ScreenAnimIn:SetToBeginning() self.reset=true end
function Controls.ScreenAnimIn:Play() assert(self.reset); self.played=true end
top, trade, envoy, launch, otherButton, backing, tile = widget(),widget(),widget(),widget(),widget(),widget(),widget()
trade:ChangeParent(top); envoy:ChangeParent(top); otherButton:ChangeParent(launch)
Controls.Readout:ChangeParent(Controls.Parking); Controls.LaunchItem:ChangeParent(Controls.Parking)
hosts = {["/InGame/TopPanel/StaticInfoStack"]=top, ["/InGame/TopPanel/TradeRoutes"]=trade,
         ["/InGame/LaunchBar/ButtonStack"]=launch, ["/InGame/LaunchBar/LaunchBacking"]=backing,
         ["/InGame/LaunchBar/LaunchBackingTile"]=tile}
LuaEvents = {LaunchBar_Resize=function(width) assert(backing.width==width+116 and tile.width==width-20) end}
local screens=widget()
hosts["/InGame/Screens"]=screens
UIManager={queue=nil}
function UIManager:GetScreenSizeVal() return screenWidth, 900 end
function UIManager:IsInPopupQueue(context) return self.queue==context end
function UIManager:QueuePopup(context,priority,parameters)
  assert(self.queue==nil and context.parent==screens and priority==PopupPriority.Low)
  assert(parameters.RenderAtCurrentParent and parameters.InputAtCurrentParent and parameters.AlwaysVisibleInQueue)
  self.queue=context
end
function UIManager:DequeuePopup(context)
  assert(self.queue==context)
  self.queue=nil
end
ContextPtr = {hidden=true, SetHide=function(self, hidden) self.hidden=hidden end,
  ChangeParent=function(self,parent) self.parent=parent end,
  SetInputHandler=function(self,f,modal) assert(modal);self.input=f end,
  LookUpControl=function(self,path) return hosts[path] end,
  SetInitHandler=function(self,fn) self.init=fn end, SetShutdown=function(self,fn) self.stop=fn end}
rows = {}
function ContextPtr:BuildInstanceForControl(name, row, parent)
  if name=="CapacityAbility" then
    assert(parent==rows.slot.Abilities)
    for _,id in ipairs({"Line","AbilityName","AbilityState"}) do row[id]=widget() end
    return
  end
  if name=="CapacityLevelSlot" then
    assert(parent==rows.building.Slots)
    for _,id in ipairs({"Slot","InstitutionIcon","InstitutionName","Arrival","Abilities","Fade"}) do row[id]=widget() end
    rows.slot=row
    return
  end
  assert(name=="CapacityCityRow" and parent==Controls.Cities)
  for _,id in ipairs({"Root","Card","Emblem","Name","Title","Levels","Status","Slots","Minus","Plus","Points",
                      "Path1","Path2","Path3","Path4"}) do row[id]=widget() end
  rows.building=row
  table.insert(rows,row)
end
-- Compact "vis:state:arrival" view of one city's four slots.
function slots(row)
  local out={}
  for i,slot in ipairs(row.slots) do
    assert(slot.Slot.disabled, "slots are display-only")
    local state=slot.abilities[1].AbilityState.text
    for _,ability in ipairs(slot.abilities) do assert(ability.AbilityState.text==state) end
    state=state:gsub("%[COLOR:ResGoldLabelCS%]",""):gsub("%[ENDCOLOR%]",""):gsub("LOC_SPC_CAP_ABILITY_","")
    out[i]=slot.Slot.vis..":"..state..":"..slot.Arrival.text..(slot.Fade:IsHidden() and "" or ":fade")
  end
  return table.concat(out,",")
end
"""


class CapacityPreview(unittest.TestCase):
    def setUp(self):
        self.lua = LuaRuntime()
        texts = self.lua.eval("{}")
        with closing(sqlite3.connect(":memory:")) as db:
            db.execute("create table LocalizedText(Language, Tag, Text)")
            for path in sorted((MOD / "Text").glob("*.sql")):
                db.executescript(path.read_text().replace("INSERT OR REPLACE INTO", "INSERT INTO"))
            for tag, text in db.execute("select Tag, Text from LocalizedText where Language='zh_Hans_CN' "
                                        "and Tag like 'LOC_SPC_%_INSTITUTION_%' order by rowid"):
                texts[tag] = text
        self.lua.globals().texts = texts
        self.lua.execute(MODEL)
        self.lua.execute((MOD / "Probe.lua").read_text())
        self.lua.execute(PANEL.with_suffix(".lua").read_text())

    def test_placement_and_repeat_load_then_shutdown(self):
        self.lua.execute("""
          Events.LoadGameViewStateDone.fire(); Events.LoadScreenClose.fire(); ContextPtr.init(true)
          assert(#top.children==3 and top.children[1]==trade and top.children[2]==Controls.Readout and top.children[3]==envoy)
          assert(#launch.children==2 and launch.children[1]==otherButton and launch.children[2]==Controls.LaunchItem)
          assert(Controls.Window:IsHidden() and not Controls.Readout.click and Controls.HUDCount.text=="6/10")
          assert(not ContextPtr.hidden, "visible HUD siblings do not imply a visible panel context")
          ContextPtr.hidden=true
          Controls.OpenButton.click(); assert(not ContextPtr.hidden and not Controls.Window:IsHidden())
          assert(UIManager.queue==ContextPtr and not Controls.Backdrop:IsHidden() and Controls.ScreenAnimIn.played)
          local esc={GetMessageType=function() return KeyEvents.KeyUp end,GetKey=function() return Keys.VK_ESCAPE end}
          assert(ContextPtr.input(esc) and UIManager.queue==nil and Controls.Window:IsHidden() and Controls.Backdrop:IsHidden())
          assert(not ContextPtr.input(esc))
          Controls.OpenButton.click(); assert(UIManager.queue==ContextPtr)
          Controls.OpenButton.click(); assert(UIManager.queue==nil and Controls.Window:IsHidden())
          ContextPtr.stop()
          assert(#top.children==2 and top.children[2]==envoy and #launch.children==1)
          assert(not Events.LoadGameViewStateDone.fire and not Events.LoadScreenClose.fire)
        """)

    def test_edits_only_change_examples_and_cancel_on_close(self):
        self.lua.execute("""
          Events.LoadGameViewStateDone.fire(); Controls.OpenButton.click()
          assert(#rows==4 and #rows[1].slots==4 and Controls.Undo.disabled)
          assert(rows[1].Emblem.icon=="ICON_DISTRICT_CAMPUS" and rows[4].Emblem.icon=="ICON_DISTRICT_INDUSTRIAL_ZONE")
          assert(rows[1].Title.text=="LOC_SPC_CAP_CITY_TITLELOC_SPC_LEVEL_RESEARCH")
          local s3=rows[1].slots[3]
          assert(s3.InstitutionIcon.icon=="ICON_SPC_INSTITUTION_RESEARCH_3" and s3.InstitutionName.text=="学术联合会")
          assert(s3.InstitutionIcon.iconSize==24)
          assert(s3.InstitutionName.truncate==204-52-6*#s3.Arrival.text-8 and rows[1].slots[1].InstitutionName.truncate==204-52)
          assert(#s3.abilities==2 and s3.abilities[1].AbilityName.text=="跨学科研究" and s3.abilities[2].AbilityName.text=="学以致用")
          assert(not s3.Slot.tooltip:find("@SPC_METRIC@",1,true) and s3.Slot.tooltip:find("学术联合会",1,true)==1)
          local counts={}
          for _,row in ipairs(rows) do for _,slot in ipairs(row.slots) do counts[#counts+1]=#slot.abilities end end
          assert(table.concat(counts,"")=="1123112311231123", table.concat(counts,""))
          -- Washington: institution I established, 2 points arrived, 3 allocated.
          assert(slots(rows[1])=="4:ACTIVE:,3:UNBUILT:LOC_SPC_CAP_ARRIVED,3:UNBUILT:LOC_SPC_CAP_ARRIVES1,3:UNBUILT::fade", slots(rows[1]))
          assert(rows[1].slots[2].InstitutionIcon.alpha<1 and rows[1].slots[1].InstitutionIcon.alpha==1)
          assert(rows[1].Levels.text=="LOC_SPC_CAP_CITY_LEVELS1/1" and rows[1].Status.text=="LOC_SPC_CAP_STATUS_GROWING")
          assert(rows[1].Points.text=="3 / 4")
          -- Boston: three institutions, one point arrived.
          assert(slots(rows[2])=="4:ACTIVE:,3:INACTIVE:,3:INACTIVE:,3:UNBUILT::fade", slots(rows[2]))
          assert(rows[4].Status.text=="LOC_SPC_CAP_STATUS_IDLE" and rows[4].Minus.disabled)
          assert(rows[2].Status.text=="LOC_SPC_CAP_STATUS_SETTLED")
          rows[1].Plus.click(); assert(rows[1].Points.text=="4 / 4" and rows[1].Plus.disabled)
          assert(rows[1].slots[4].Arrival.text=="LOC_SPC_CAP_ARRIVES2")
          assert(rows[1].Status.text=="LOC_SPC_CAP_STATUS_UNCONFIRMED")
          assert(Controls.HUDCount.text=="6/10" and Controls.Available.text=="LOC_SPC_CAP_FREE3")
          Controls.Undo.click(); assert(rows[1].Points.text=="3 / 4")
          for i=1,4 do rows[4].Plus.click() end
          assert(slots(rows[4])=="3:INACTIVE:LOC_SPC_CAP_ARRIVES1,3:INACTIVE:LOC_SPC_CAP_ARRIVES2,"..
            "3:INACTIVE:LOC_SPC_CAP_ARRIVES3,3:INACTIVE:LOC_SPC_CAP_ARRIVES4", slots(rows[4]))
          assert(Controls.Available.text=="LOC_SPC_CAP_FREE0" and rows[2].Plus.disabled)
          Controls.Confirm.click(); assert(Controls.HUDCount.text=="10/10" and Controls.Confirm.disabled)
          assert(rows[4].Status.text=="LOC_SPC_CAP_STATUS_GROWING")
          -- New York: three institutions, two points arrived; withdraw one.
          rows[3].Minus.click()
          assert(slots(rows[3])=="4:ACTIVE:,4:ACTIVE:LOC_SPC_CAP_WITHDRAW,3:INACTIVE:,3:UNBUILT::fade", slots(rows[3]))
          Controls.ModalScreenClose.click(); Controls.OpenButton.click()
          assert(rows[3].Points.text=="2 / 4" and Controls.HUDCount.text=="10/10")
        """)

    def test_layout_follows_screen_width_without_crossing_paths(self):
        self.lua.execute("""
          Events.LoadGameViewStateDone.fire(); Controls.OpenButton.click()
          local function check(card,gap,slot)
            for _,row in ipairs(rows) do
              assert(row.Card.width==card and row.Root.width==card+4*(gap+slot), row.Root.width)
              local left=card
              for level,s in ipairs(row.slots) do
                local path=row["Path"..level]
                assert(path.x==left and path.width==gap, "path fills only the gap")
                assert(s.Slot.x==left+gap and s.Slot.width==slot)
                left=s.Slot.x+slot
              end
            end
          end
          check(300,28,204)
          assert(Controls.Window.width==1228+64, "window hugs the rows")
          Controls.ModalScreenClose.click(); screenWidth=1024; Controls.OpenButton.click()
          check(240,20,174)
          assert(rows[1].Root.width<=1024-8 and Controls.Window.width==1024)
        """)

    def test_scope_and_late_hud_container(self):
        self.lua.execute("""
          eligible=false; Events.LoadGameViewStateDone.fire()
          assert(#launch.children==1 and #top.children==2)
          eligible=true; hosts["/InGame/TopPanel/StaticInfoStack"]=nil
          Events.LoadGameViewStateDone.fire(); assert(#launch.children==2 and #top.children==2)
          hosts["/InGame/TopPanel/StaticInfoStack"]=top; Events.LoadScreenClose.fire()
          assert(#top.children==3 and #launch.children==2)
        """)

    def test_packaging_strings_and_display_only_top(self):
        import re
        xml = PANEL.with_suffix(".xml")
        tree = ET.parse(xml)
        window = tree.find(".//Container[@ID='Window']")
        self.assertEqual(window.get("Anchor"), "C,C")
        self.assertEqual(window.get("Size"), "parent,768")
        self.assertEqual(window.get("MinSize"), "1024,768")
        self.assertIsNotNone(window.find("./Container[@Style='ModalScreenWide']"))
        self.lua.execute("""
          assert(Controls.ModalBG.texture=="Governors_BackgroundTile_ScreenFill")
          assert(Controls.ModalScreenTitle.text=="LOC_SPC_CAP_TITLE" and Controls.YieldsContainer:IsHidden())
        """)
        self.assertEqual(tree.find(".//Container[@ID='Backdrop']").get("Style"), "FullScreenVignetteConsumer")
        hud = tree.find(".//Grid[@ID='Readout']")
        self.assertIsNotNone(hud)
        self.assertFalse(any("Button" in node.tag for node in hud.iter()))
        self.assertTrue(tree.find(".//Container[@ID='LaunchItem']/Button").get("Size") == "49,49")
        manifest = ET.parse(MOD / "SpecializationP0.modinfo")
        prefix = "UI/ManagementCapacityPreview"
        self.assertEqual([prefix + ".xml"], [n.text for n in manifest.findall(
            ".//AddUserInterfaces[@id='SPC_ManagementCapacityPreview']/File")])
        self.assertFalse(any(prefix in (n.text or "") for n in manifest.findall(".//AddGameplayScripts/File")))
        text_file = "Text/ManagementCapacityPreview.sql"
        self.assertIn(text_file, [n.text for n in manifest.findall(".//UpdateText/File")])
        required = {prefix + ".xml", prefix + ".lua", text_file}
        self.assertLessEqual(required, {n.text for n in manifest.findall("./Files/File")})
        with closing(sqlite3.connect(":memory:")) as db:
            db.execute("create table LocalizedText(Language, Tag, Text, primary key(Language,Tag))")
            db.executescript((MOD / text_file).read_text())
            tags = set(re.findall(r"LOC_SPC_CAP_[A-Z_]*[A-Z]", xml.read_text()+PANEL.with_suffix(".lua").read_text()))
            tags.discard("LOC_SPC_CAP_ABILITY")
            tags |= {f"LOC_SPC_CAP_ABILITY_{state}" for state in ("ACTIVE", "INACTIVE", "UNBUILT")}
            for language in ("zh_Hans_CN", "en_US"):
                self.assertEqual(tags, {row[0] for row in db.execute(
                    "select Tag from LocalizedText where Language=? and length(Text)>0", (language,))})


if __name__ == "__main__":
    unittest.main()
