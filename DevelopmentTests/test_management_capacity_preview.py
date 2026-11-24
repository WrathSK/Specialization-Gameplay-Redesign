"""Native UI layout contract with the real preview Lua and no gameplay services."""
import sqlite3
import unittest
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
Locale = {Lookup=function(tag, ...) return tag .. table.concat({...}, "/") end}
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
function control:SetText(value) self.text=value end
function control:SetIcon(value,size) self.icon=value; self.iconSize=size end
function control:SetHide(value) self.hidden=value end
function control:IsHidden() return self.hidden end
function control:SetDisabled(value) self.disabled=value end
function control:RegisterCallback(button, callback) assert(button==1); self.click=callback end
function control:CalculateSize() end
function control:GetSizeX() return 200+#self.children*56 end
function control:SetSizeX(value) self.width=value end
Controls = {}
for _,id in ipairs({"Window","Readout","HUDCount","Parking","OpenButton","LaunchItem","Cities",
                    "Close","Confirm","Undo","Available","Total"}) do Controls[id]=widget() end
Controls.Window:SetHide(true)
top, trade, envoy, launch, otherButton, backing, tile = widget(),widget(),widget(),widget(),widget(),widget(),widget()
trade:ChangeParent(top); envoy:ChangeParent(top); otherButton:ChangeParent(launch)
Controls.Readout:ChangeParent(Controls.Parking); Controls.LaunchItem:ChangeParent(Controls.Parking)
hosts = {["/InGame/TopPanel/StaticInfoStack"]=top, ["/InGame/TopPanel/TradeRoutes"]=trade,
         ["/InGame/LaunchBar/ButtonStack"]=launch, ["/InGame/LaunchBar/LaunchBacking"]=backing,
         ["/InGame/LaunchBar/LaunchBackingTile"]=tile}
LuaEvents = {LaunchBar_Resize=function(width) assert(backing.width==width+116 and tile.width==width-20) end}
ContextPtr = {LookUpControl=function(self,path) return hosts[path] end,
  SetInitHandler=function(self,fn) self.init=fn end, SetShutdown=function(self,fn) self.stop=fn end}
rows = {}
function ContextPtr:BuildInstanceForControl(name, row, parent)
  assert(name=="CapacityCityRow" and parent==Controls.Cities)
  for _,id in ipairs({"ProfessionIcon","Name","Detail","Minus","Plus","Points"}) do row[id]=widget() end
  table.insert(rows,row)
end
"""


class CapacityPreview(unittest.TestCase):
    def setUp(self):
        self.lua = LuaRuntime()
        self.lua.execute(MODEL)
        self.lua.execute((MOD / "Probe.lua").read_text())
        self.lua.execute(PANEL.with_suffix(".lua").read_text())

    def test_placement_and_repeat_load_then_shutdown(self):
        self.lua.execute("""
          Events.LoadGameViewStateDone.fire(); Events.LoadScreenClose.fire(); ContextPtr.init(true)
          assert(#top.children==3 and top.children[1]==trade and top.children[2]==Controls.Readout and top.children[3]==envoy)
          assert(#launch.children==2 and launch.children[1]==otherButton and launch.children[2]==Controls.LaunchItem)
          assert(Controls.Window:IsHidden() and not Controls.Readout.click and Controls.HUDCount.text=="6/10")
          Controls.OpenButton.click(); assert(not Controls.Window:IsHidden())
          Controls.OpenButton.click(); assert(Controls.Window:IsHidden())
          ContextPtr.stop()
          assert(#top.children==2 and top.children[2]==envoy and #launch.children==1)
          assert(not Events.LoadGameViewStateDone.fire and not Events.LoadScreenClose.fire)
        """)

    def test_edits_only_change_examples_and_cancel_on_close(self):
        self.lua.execute("""
          Events.LoadGameViewStateDone.fire(); Controls.OpenButton.click()
          assert(#rows==4 and rows[1].Detail.text=="LOC_SPC_CAP_DETAIL1/1/2" and Controls.Undo.disabled)
          rows[1].Plus.click(); assert(rows[1].Points.text=="4" and rows[1].Plus.disabled)
          assert(Controls.HUDCount.text=="6/10" and Controls.Available.text=="LOC_SPC_CAP_FREE3")
          Controls.Undo.click(); assert(rows[1].Points.text=="3")
          for i=1,4 do rows[4].Plus.click() end
          assert(Controls.Available.text=="LOC_SPC_CAP_FREE0" and rows[2].Plus.disabled)
          Controls.Confirm.click(); assert(Controls.HUDCount.text=="10/10" and Controls.Confirm.disabled)
          assert(rows[4].Detail.text=="LOC_SPC_CAP_DETAIL0/4/0")
          rows[1].Minus.click(); Controls.Close.click(); Controls.OpenButton.click()
          assert(rows[1].Points.text=="3" and Controls.HUDCount.text=="10/10")
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
        with sqlite3.connect(":memory:") as db:
            db.execute("create table LocalizedText(Language, Tag, Text, primary key(Language,Tag))")
            db.executescript((MOD / text_file).read_text())
            tags = set(re.findall(r"LOC_SPC_CAP_[A-Z_]+", xml.read_text()+PANEL.with_suffix(".lua").read_text()))
            for language in ("zh_Hans_CN", "en_US"):
                self.assertEqual(tags, {row[0] for row in db.execute(
                    "select Tag from LocalizedText where Language=? and length(Text)>0", (language,))})


if __name__ == "__main__":
    unittest.main()
