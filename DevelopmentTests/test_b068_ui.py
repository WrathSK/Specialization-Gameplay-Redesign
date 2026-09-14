"""B068 actual UI logic under mocked Civ controls; no game files written."""
from pathlib import Path
import xml.etree.ElementTree as E
import hashlib
from lupa.lua55 import LuaRuntime
R=Path(__file__).resolve().parents[1];M=R/'Mod'
# Current panel contract: 15 read-only entries + close, no overlapping positions.
x=E.parse(M/'UI/P0Panel.xml').getroot();w=x.find('./Container')
buttons=[e for e in w.findall('./GridButton') if e.get('Hidden')!='1']
assert len(buttons)==16
assert len({(e.get('Anchor'),e.get('Offset')) for e in buttons})==16
assert not any(any(t in e.get('ID') for t in ['AUTO','OFF','Test','Prepare','Confirm','Record','Clear']) for e in buttons)
assert x.find(".//*[@ID='ReportScroll']") is not None
for p in M.rglob('*.xml'):E.parse(p)
for p in M.rglob('*.lua'):LuaRuntime().execute('assert(load(...))',p.read_text())
assert hashlib.sha256((R/'Specialization/Design/Specialization_v0.1_Design_Spec.md').read_bytes()).hexdigest()=='81dc772c1038718e567496cfdb165167e6090fae2b7b472b7301435d766d994b'
source=(M/'Gameplay.lua').read_text()
a=source.index('  -- B068 presentation');b=source.index("  if params.Action=='DIALOGUE_SAMPLE'",a)
branch=source[a:b]
assert 'SetProperty' not in branch and '.Audit' not in branch
l=LuaRuntime(unpack_returned_tuples=True)
l.execute('''
include=function() end
SPCP0={VERSION='test',IsTestPlayer=function(p) return p==0 end,CrewBase=function(t) return t=='CREW' and 250 or nil end}
ExposedMembers={SPC_P0={}};Game={GetLocalPlayer=function() return 0 end,GetCurrentGameTurn=function() return 1 end}
city={GetOwner=function() return 0 end,GetID=function() return 11 end}
selectedCity=city;selectedUnit=nil;mode=1
InterfaceModeTypes={SELECTION=1};PlayerOperations={EXECUTE_SCRIPT=1}
requests={};UI={GetHeadSelectedCity=function() return selectedCity end,GetHeadSelectedUnit=function() return selectedUnit end,
 GetInterfaceMode=function() return mode end,IsGameCoreBusy=function() return false end,
 RequestPlayerOperation=function(_,_,p) requests[#requests+1]=p end,GetColorValue=function(n) assert(n=='COLOR_SPC_LEGAL_TARGET');return 123 end}
local function control()
 return setmetatable({hidden=true},{__index=function(t,k)
 if k=='SetHide' then return function(_,v) t.hidden=v end end
 if k=='SetText' then return function(_,v) t.text=v end end
 if k=='SetToolTipString' then return function(_,v) t.tip=v end end
 if k=='RegisterCallback' then return function(_,_,v) t.click=v end end
 return function() end end})
end
Controls=setmetatable({},{__index=function(t,k) local v=control();rawset(t,k,v);return v end})
ContextPtr={SetInitHandler=function(_,f) init=f end,SetShutdown=function(_,f) shutdown=f end,
 SetUpdate=function(_,f) update=f end,ClearUpdate=function() end,SetHide=function() end,LookUpControl=function() return {} end}
''')
l.execute((M/'UI/CityPotential.lua').read_text());l.execute('init();update(.5)')
for n in range(1,5):
 l.execute('''local p=requests[#requests];ExposedMembers.SPC_P0.CityPresentationView={token=p.Token,owner=0,cityID=11,specialization='RESEARCH',potential=...,investments=(...)-1};update(.5);assert(not Controls.Badge.hidden);assert(Controls.Badge.text:find(tostring(...)..'级'));update(2)''',n,n,n)
l.execute("selectedCity=nil;update(.5);assert(Controls.Badge.hidden);shutdown()")
# Actual Gameplay read branch: never SetProperty, missing city handled separately.
l.execute("P=SPCP0;Players={[0]={GetCities=function() return {FindID=function() return city end} end}};shared={EffectiveFacts={Read=function() return {specialization='CULTURE',potential=3,investmentCount=2} end}};params={Action='CITY_PRESENTATION_READ',CityID=11,Token='x'};playerID=0")
l.execute('function readPresentation()\n'+branch+'\nend;readPresentation();assert(shared.CityPresentationView.potential==3 and shared.CityPresentationView.token=="x")')
# Actual target rendering: same set does not repaint; no world text, no activation/movement/appeal lens change.
l.execute('''
GameInfo={Units={[1]={UnitType='CREW'}}};selectedUnit={GetOwner=function() return 0 end,GetID=function() return 4 end,GetType=function() return 1 end,GetX=function() return 3 end,GetY=function() return 3 end}
PlayersVisibility={[0]={IsVisible=function() return true end}}
local function event() return {Add=function() end,Remove=function() end} end
Events={UnitSelectionChanged=event(),InterfaceModeChanged=event(),LoadScreenClose=event()};LuaEvents={SPC_ToggleBuilderTargets=event()}
paints=0;clears=0;on=false
UILens={CreateLensLayerHash=function(n) assert(n=='Hex_Coloring_Great_People');return 99 end,
 ClearLayerHexes=function() clears=clears+1 end,ToggleLayerOn=function() on=true end,ToggleLayerOff=function() on=false end,
 SetLayerHexesColoredArea=function(layer,pid,plots,color) assert(layer==99 and color==123 and #plots==2);paints=paints+1 end}
''')
l.execute((M/'UI/UnitTargetMarkers.lua').read_text())
l.execute('''init();update(.25)
local p=requests[#requests];ExposedMembers.SPC_P0.UnitTargetSnapshot={version='test',token=p.Token,owner=0,unitID=4,mode='CREW',plots={{plot=3},{plot=7}}};update(.25);assert(paints==1 and on)
update(6);p=requests[#requests];ExposedMembers.SPC_P0.UnitTargetSnapshot.token=p.Token;update(.25);assert(paints==1 and on)
selectedUnit=nil;update(.25);assert(not on);shutdown()
''')
# Bounded repetition log keeps evidence and occurrence count.
l.execute('emitted=0;print=function() emitted=emitted+1 end')
l.execute((M/'DiagnosticLog.lua').read_text());l.execute("local log=SPCDiagnosticLog.For('test');for i=1,100 do log('same error') end;assert(emitted==1 and ExposedMembers.SPC_UILog.test.rows['same error'].count==100)")
print('B068 LOCAL_SIMULATION_PASS: mutually exclusive Potential labels 1-4/selection cleanup, validated read-only bridge, purple target reuse/cleanup, 15 read-only entries, report scrolling, bounded error evidence, Lua/XML syntax; native layout/layer behavior still USER_GAME_TEST_REQUIRED.')
# Initialize the actual panel with all controls, then exercise read/export buttons.
l.execute('''
print=function() emitted=emitted+1 end
Mouse={eLClick=1};selectedCity=city;selectedUnit=nil
SPCP0.Scalar=tostring;SPCP0.Call=function() return false end
Events=setmetatable({}, {__index=function(t,k) local e={Add=function() end,Remove=function() end};rawset(t,k,e);return e end})
ContextPtr.LookUpControl=function() return {GetSizeX=function() return 296 end} end
ContextPtr.SetInitHandler=function(_,f) init=f end
ContextPtr.SetUpdate=function(_,f) update=f end
GameInfo.Yields={};UIManager={};Game.GetCurrentGameTurn=function() return 1 end
''')
l.execute((M/'UI/P0Panel.lua').read_text());l.execute('''init();Controls.SourceYieldButton.click();assert(requests[#requests].Action=='PROGRESSION_READ')
Controls.CopyButton.click();assert(Controls.Status.text:find('Lua.log'));shutdown()
''')
print('B068 panel init/anchor/read/log export callbacks PASS (mock UI APIs).')
