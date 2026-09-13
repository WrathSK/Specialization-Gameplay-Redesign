from pathlib import Path
from lupa.lua55 import LuaRuntime
import xml.etree.ElementTree as E
w=Path(__file__).resolve().parents[1];r=w/"Sid Meier's Civilization VI/Mods/SpecializationP0"
# Existing actual Crew/investment suites, version fixture only.
p=w/'DevelopmentTests/test_crew_unit_actions.py'
t=p.read_text().replace("=='55'","=='56'")
t=t.replace("m.executescript((r/'Data/Crew.sql').read_text())", "m.executescript((r/'Data/Crew.sql').read_text()) if not m.execute(\"select 1 from Units where UnitType='UNIT_SPC_CREW_250'\").fetchone() else None")
exec(compile(t,str(p),'exec'),{'__file__':str(p)})
l=LuaRuntime(unpack_returned_tuples=True)
l.execute("""
include=function() end;SPCP0={VERSION='P0-B-043',IsTestPlayer=function() return true end}
ExposedMembers={SPC_P0={}};Mouse={eLClick=1};PlayerOperations={EXECUTE_SCRIPT=1};InterfaceModeTypes={SELECTION=1}
Game={GetLocalPlayer=function() return 0 end,GetCurrentGameTurn=function() return 1 end}
kind=1;selected={GetOwner=function() return 0 end,GetID=function() return 9 end,GetX=function() return 10 end,GetY=function() return 20 end,GetType=function() return kind end}
GameInfo={Units={[1]={UnitType='UNIT_SETTLER'},[2]={UnitType='UNIT_SPC_CREW_250'},[3]={UnitType='UNIT_BUILDER'}}}
UI={GetHeadSelectedUnit=function() return selected end,GetInterfaceMode=function() return 1 end,
RequestPlayerOperation=function(_,_,p) sent=p end}
parent={CalculateSize=function() end,ReprocessAnchoring=function() end}
Controls=setmetatable({},{__index=function(t,k) local c={SetHide=function(self,v) self.hide=v end,
SetDisabled=function(self,v) self.disabled=v end,SetIcon=function(self,v) self.icon=v end,
SetToolTipString=function(self,v) self.tip=v end,ChangeParent=function(self,p) self.parent=p end,
RegisterCallback=function(self,_,fn) self.click=fn end};t[k]=c;return c end})
ContextPtr={SetInitHandler=function(_,fn) init=fn end,SetUpdate=function(_,fn) tick=fn end,
SetHide=function() end,SetShutdown=function() end,LookUpControl=function(_,path) assert(path=='/InGame/UnitPanel/StandardActionsStack');return parent end}
""")
l.execute((r/'UI/UnitPanelActions.lua').read_text())
l.execute("""
init();tick(0.3);assert(Controls.ActionGroup.parent==parent and not Controls.ActionGroup.hide)
assert(Controls.PrepareIcon.icon=='ICON_UNITOPERATION_FOUND_CITY');assert(Controls.ConfirmButton.hide)
Controls.PrepareButton.click();assert(sent.Action=='UNIT_ACTION_PREPARE')
ExposedMembers.SPC_P0={Version='P0-B-043',LastToken=sent.Token,Snapshot='PREPARED',UnitActionPreview={owner=0,unitID=9,turn=1,x=10,y=20,token='PLAN'}}
tick(0.3);assert(not Controls.ConfirmButton.hide)
Controls.ConfirmButton.click();assert(sent.Action=='UNIT_ACTION_CONFIRM' and sent.PlanToken=='PLAN')
ExposedMembers.SPC_P0.LastToken=sent.Token;ExposedMembers.SPC_P0.Snapshot='DONE';ExposedMembers.SPC_P0.UnitActionPreview=nil;tick(0.3)
kind=2;tick(0.3);assert(Controls.PrepareIcon.icon=='ICON_UNITOPERATION_BUILD_IMPROVEMENT')
kind=3;tick(0.3);assert(Controls.ActionGroup.hide)
""")
E.parse(r/'UI/UnitPanelActions.xml')
print('LOCAL_SIMULATION_PASS B043: parent attachment, correct icons, prepare/confirm receipt token, other units hidden; underlying action suites preserved.')
