from pathlib import Path
import xml.etree.ElementTree as E
from lupa.lua55 import LuaRuntime
w=Path(__file__).resolve().parents[1];r=w/"Sid Meier's Civilization VI/Mods/SpecializationP0"
l=LuaRuntime(unpack_returned_tuples=True)
# Reuse read-only mock setup, not old version assertions.
old=Path(__file__).with_name('test_unit_site_probe.py').read_text()
setup=old.split("l.execute('''",1)[1].split("''')",1)[0]
l.execute(setup)
l.execute('''
Players[0].GetCities=function() return {Members=function() local once=false;return function() if not once then once=true;return 1,city end end end} end
Map.GetCityPlots=function() return {GetPurchasedPlots=function() return {10} end} end
Map.GetPlotByIndex=function() return plot end
local basePlot=Map.GetPlot;Map.GetPlot=function(x,y) local p=basePlot(x,y);p.GetOwner=function() return 0 end;return p end
''')
l.execute((r/'UnitTargets.lua').read_text())
l.execute('''
SPCUnitTargets.Start(P,shared)
local function read(preview)
 shared.UnitTargets.Refresh(0,{UnitID=1,Token='t',BuilderPreview=preview})
 return shared.UnitTargetSnapshot
end
assert(#read().plots==1)
potential=4;assert(#read().plots==0);potential=2
-- Can enumerate from elsewhere: unit's current position is not a target requirement.
x=11;assert(#read().plots==1 and read().plots[1].plot==10);x=10
kind='UNIT_BUILDER';assert(read().error)
assert(#read(true).plots==1)
current='WONDER';mark=7;assert(#read(true).plots==1)
mark=6;assert(#read(true).plots==0 and #read(true).unknown==1)
current='UNIT_WARRIOR';assert(#read(true).plots==0)
current='DISTRICT_CAMPUS';done=false;assert(#read(true).plots==1)
done=true;assert(#read(true).plots==0)
''')
u=LuaRuntime(unpack_returned_tuples=True)
u.execute('''
include=function() end
SPCP0={VERSION='P0-B-041',IsTestPlayer=function() return true end}
function event() return {Add=function(fn) end,Remove=function(fn) end} end
Events={UnitSelectionChanged=event(),InterfaceModeChanged=event(),LoadScreenClose=event()}
LuaEvents={SPC_ToggleBuilderTargets={Add=function(fn) toggle=fn end,Remove=function() end}}
ExposedMembers={}
Game={GetLocalPlayer=function() return 0 end}
PlayerOperations={EXECUTE_SCRIPT=1};InterfaceModeTypes={SELECTION=1}
ut=1;px=10;mode=1
unit={GetOwner=function() return 0 end,GetID=function() return 1 end,GetX=function() return px end,GetY=function() return 0 end,GetType=function() return ut end}
UI={GetHeadSelectedUnit=function() return unit end,GetInterfaceMode=function() return mode end,IsGameCoreBusy=function() return false end,
RequestPlayerOperation=function(_,_,p) sent=p end,GridToWorld=function(i) return i,0 end}
GameInfo={Units={[1]={UnitType='UNIT_SETTLER'},[2]={UnitType='UNIT_BUILDER'},[3]={UnitType='UNIT_GREAT_SCIENTIST'}}}
PlayersVisibility={[0]={IsVisible=function() return true end}}
draws=0;resets=0
InstanceManager={new=function() return {ResetInstances=function() resets=resets+1;draws=0 end,GetInstance=function()
draws=draws+1;return {Anchor={SetWorldPositionVal=function() end},Caption={SetText=function() end}} end} end}
ContextPtr={SetInitHandler=function(_,fn) init=fn end,SetUpdate=function(_,fn) tick=fn end,SetHide=function() end,SetShutdown=function(_,fn) shutdown=fn end,ClearUpdate=function() end}
''')
u.execute((r/'UI/UnitTargetMarkers.lua').read_text())
u.execute('''
init();tick(0.3);assert(sent.Action=='UNIT_TARGETS_READ')
ExposedMembers.SPC_P0={UnitTargetSnapshot={version='P0-B-041',token=sent.Token,owner=0,unitID=1,plots={{plot=10}},unknown={},mode='INVEST'}}
tick(0.3);assert(draws==1)
ut=3;tick(0.3);assert(draws==0) -- own instances clear; no UILens mock exists or needed
ut=2;sent=nil;tick(0.3);assert(sent==nil)
toggle();tick(0.3);assert(sent.BuilderPreview==true)
mode=2;tick(0.3);assert(draws==0)
shutdown()
''')
for f in r.rglob('*.lua'):l.execute('assert(load(...))',f.read_text())
m=E.parse(r/'SpecializationP0.modinfo').getroot();assert m.get('version')=='53'
for f in m.findall('.//File'):assert (r/f.text).exists()
E.parse(r/'UI/UnitSites.xml');E.parse(r/'UI/UnitTargetMarkers.xml')
print('LOCAL_SIMULATION_PASS: target enumeration and isolated marker selection/render/clear; Lua/XML/manifest53. Engine UI and city-plot enumeration await user test.')
