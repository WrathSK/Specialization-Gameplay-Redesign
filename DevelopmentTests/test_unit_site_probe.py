from pathlib import Path
import xml.etree.ElementTree as E
from lupa.lua55 import LuaRuntime
w=Path(__file__).resolve().parents[1];r=w/"Sid Meier's Civilization VI/Mods/SpecializationP0"
l=LuaRuntime(unpack_returned_tuples=True)
l.execute('''
x=10;kind='UNIT_SETTLER';current='BUILDING_LIBRARY';mark=nil;potential=2;done=true
plot={GetIndex=function() return x end,GetX=function() return x end,GetY=function() return 0 end,
 GetOwner=function() return 0 end,GetDistrictType=function() return mark and 9 or 1 end,GetProperty=function() return mark end}
city={GetOwner=function() return 0 end,GetID=function() return 8 end,GetName=function() return 'Test' end,
 GetBuildQueue=function() return {CurrentlyBuilding=function() return current end} end,
 GetBuildings=function() return {HasBuilding=function() return false end} end}
d={GetID=function() return 3 end,GetType=function() return 'DISTRICT_CAMPUS' end,GetCity=function() return city end,
 GetX=function() return 10 end,GetY=function() return 0 end,IsComplete=function() return done end}
unit={GetOwner=function() return 0 end,GetType=function() return kind end,GetX=function() return x end,GetY=function() return 0 end}
Players={[0]={GetUnits=function() return {FindID=function(_,id) if id==1 then return unit end end} end,
 GetDistricts=function() return {Members=function() local once=false;return function() if not once then once=true;return 1,d end end end} end}}
Map={GetPlot=function(px,py) if px==x then return plot end;return {GetIndex=function() return px end,GetX=function() return px end,GetY=function() return py end} end}
Cities={GetPlotPurchaseCity=function() return city end}
P={IsTestPlayer=function(pid) return pid==0 end,Info=function(t,k)
 if t=='Units' then return {UnitType=k} end
 if t=='Districts' and k=='DISTRICT_CAMPUS' then return {Index=1,DistrictType=k} end
 if t=='Districts' and k=='DISTRICT_WONDER' then return {Index=9,DistrictType=k} end
 if t=='Buildings' and k=='BUILDING_LIBRARY' then return {Index=2,PrereqDistrict='DISTRICT_CAMPUS',IsWonder=false} end
 if t=='Buildings' and k=='WONDER' then return {Index=7,IsWonder=true} end
end}
shared={EffectiveFacts={Read=function() return {specialization='RESEARCH',potential=potential,first={districtID=3,type='DISTRICT_CAMPUS'}} end}}
''')
for n in ['UnitActionSitePolicy.lua','UnitSiteProbe.lua']:l.execute((r/n).read_text())
l.execute('''
SPCUnitSiteProbe.Start(P,shared);read=shared.UnitSiteProbe.Read
assert(read(0,1):find('Investment candidate: SITE OK'))
assert(read(0,1):find('Construction candidate: SITE OK'))
x=11;assert(read(0,1):find('MOVE_TO_TARGET_PLOT'));x=10
potential=4;assert(read(0,1):find('POTENTIAL_NOT_INVESTABLE'));potential=2
kind='UNIT_BUILDER';assert(read(0,1):find('SETTLER_REQUIRED'))
current='DISTRICT_CAMPUS';done=false;assert(read(0,1):find('Construction candidate: SITE OK'))
current='WONDER';mark=7;assert(read(0,1):find('Construction candidate: SITE OK'))
mark=6;assert(read(0,1):find('NOT VERIFIED'));mark=nil
current='UNIT_WARRIOR';assert(read(0,1):find('NO BUILDING / DISTRICT / WONDER TARGET'))
assert(read(1,1):find('UNKNOWN'));assert(read(0,2):find('UNKNOWN'))
''')
# Independent UI context: registration, selection visibility, dispatch, response and move stale clearing.
u=LuaRuntime(unpack_returned_tuples=True)
u.execute('''
include=function() end;SPCP0={VERSION='P0-B-040',IsTestPlayer=function() return true end}
ExposedMembers={};Mouse={eLClick=1};PlayerOperations={EXECUTE_SCRIPT=1};Game={GetLocalPlayer=function() return 0 end}
px=10;sel={GetOwner=function() return 0 end,GetType=function() return 1 end,GetID=function() return 1 end,GetX=function() return px end,GetY=function() return 0 end}
GameInfo={Units={[1]={UnitType='UNIT_SETTLER'}}}
UI={GetHeadSelectedUnit=function() return sel end,RequestPlayerOperation=function(_,_,p) params=p end}
Controls={}
for _,n in ipairs({'ReadButton','Window','Report','CloseButton'}) do Controls[n]={SetHide=function(self,v) self.hidden=v end,
 SetText=function(self,v) self.text=v end,RegisterCallback=function(self,_,fn) self.click=fn end} end
ContextPtr={SetUpdate=function(_,fn) update=fn end}
''')
u.execute((r/'UI/UnitSites.lua').read_text())
u.execute('''
assert(not Controls.ReadButton.hidden);Controls.ReadButton.click();assert(params.Action=='UNIT_SITE_READ' and params.UnitID==1)
ExposedMembers.SPC_P0={Version='P0-B-040',LastToken=params.Token,Snapshot='READ OK'};update(0.3)
assert(Controls.Report.text=='READ OK');px=11;update(0.3);assert(Controls.Window.hidden)
sel=nil;update(0.3);assert(Controls.ReadButton.hidden)
''')
for p in r.rglob('*.lua'):l.execute('assert(load(...))',p.read_text())
m=E.parse(r/'SpecializationP0.modinfo').getroot();assert m.get('version')=='51'
for f in m.findall('.//File'):assert (r/f.text).is_file(),f.text
E.parse(r/'UI/UnitSites.xml')
g=(r/'Gameplay.lua').read_text();assert g.index('shared.UnitSiteProbe.Read')<g.index('local city=type(params.CityID)')
print('LOCAL_SIMULATION_PASS: actual Gameplay site module and UI selection/dispatch/response; Lua/XML/manifest51. No game test claimed.')
