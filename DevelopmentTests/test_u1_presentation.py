"""Actual U1 display Lua in mocks; no claim about native layout/rendering."""
from pathlib import Path
import subprocess,xml.etree.ElementTree as ET
from lupa.lua55 import LuaRuntime
R=Path(__file__).resolve().parents[1];M=R/'Mod';l=LuaRuntime()
def run(name):l.execute((M/name).read_text())
l.execute("""
function include() end
local function event() local t={};function t.Add(f)t.f=f end;function t.Remove()t.f=nil end;return setmetatable(t,{__call=function(_,...)if t.f then t.f(...) end end})end
LuaEvents={SPC_InstitutionOverview=event(),SPC_PresentationChanged=event()}
ExposedMembers={SPC_P0={}}
Game={GetLocalPlayer=function()return 0 end}
city={GetID=function()return 1 end,GetOwner=function()return 0 end,GetX=function()return 4 end,GetY=function()return 5 end}
UI={GetHeadSelectedCity=function()return city end}
ContextPtr={SetShutdown=function(self,f)shutdown=f end}
Controls={PanelBreakdown={IsHidden=function()return false end}}
local definitions={{BuildingType='BUILDING_SPC_A',InternalOnly=true},{BuildingType='BUILDING_OTHER_INTERNAL',InternalOnly=true},{BuildingType='BUILDING_LIBRARY',InternalOnly=false},{BuildingType='BUILDING_SPC_ORDINARY',InternalOnly=false}}
GameInfo={Buildings=function()local i=0;return function()i=i+1;return definitions[i]end end}
calls=0;function ViewPanelBreakdown(d)calls=calls+1;rendered=d end
function OnShutdown()end
v={owner=0,cityID=1,x=4,y=5,specialization='RESEARCH',potential=4,active=4}
ExposedMembers.SPC_P0.CityPresentationView=v
data={Owner=0,City=city,BuildingsAndDistricts={{Buildings={{Type='BUILDING_SPC_A'},{Type='BUILDING_LIBRARY'},{Type='BUILDING_OTHER_INTERNAL'},{Type='BUILDING_SPC_ORDINARY'}}}}}
""")
run('InstitutionPresentation.lua');run('UI/InstitutionOverview.lua')
l.execute("""
ViewPanelBreakdown(data);assert(#rendered.BuildingsAndDistricts[1].Buildings==3);assert(#data.BuildingsAndDistricts[1].Buildings==4)
assert(rendered.BuildingsAndDistricts[1].Buildings[1].Type=='BUILDING_LIBRARY')
for p=1,4 do for a=0,4 do v.potential=p;v.active=a;assert(SPCInstitutionPresentation.Matches(v,0,1,4,5));for i=1,p do assert(#SPCInstitutionPresentation.Tooltip(i,v)>0)end end end
v.potential=4;v.active=4;ViewPanelBreakdown(data)
ExposedMembers.SPC_P0.CityPresentationView={owner=0,cityID=1,error='temporary'};ViewPanelBreakdown(data);assert(#rendered.BuildingsAndDistricts[1].Buildings==3)
ExposedMembers.SPC_P0.CityPresentationView={owner=0,cityID=1,x=4,y=5,specialization='COMMERCE',potential=4};ViewPanelBreakdown(data);assert(rendered==data)
assert(not SPCInstitutionPresentation.Matches(v,0,2,4,5));assert(not SPCInstitutionPresentation.Matches(v,0,1,8,9))
local n=calls;for i=1,10000 do SPCInstitutionPresentation.Tooltip(4,v);LuaEvents.SPC_PresentationChanged() end;assert(calls==n)
shutdown()
""")
# UI renderer: fixed controls; duplicate notifications must not reparent/create/rebuild.
l.execute("""
local function ctl()return {SetHide=function(self,x)self.hidden=x end,SetText=function(self,x)self.text=x end,SetToolTipString=function(self,x)self.tip=x end,ChangeParent=function()parents=parents+1 end,CalculateSize=function()sizes=sizes+1 end,DestroyChild=function()end,ReprocessAnchoring=function()end}end
parents=0;sizes=0;Controls={InstitutionContainer=ctl(),InstitutionRows=ctl(),InstitutionHeader=ctl()}
for i=1,4 do Controls['Institution'..i]=ctl();Controls['InstitutionName'..i]=ctl();Controls['InstitutionState'..i]=ctl()end
ContextPtr={SetHide=function()end,LookUpControl=function()return ctl()end,SetInitHandler=function(self,f)init=f end,SetShutdown=function(self,f)shutdown=f end}
""")
run('UI/Institutions.lua')
l.execute("""
init();LuaEvents.SPC_InstitutionOverview(data,v);local n=sizes
for i=1,10000 do LuaEvents.SPC_InstitutionOverview(data,v)end
assert(sizes==n and parents==1)
assert(Controls.Institution4.hidden==false)
v.active=1;LuaEvents.SPC_InstitutionOverview(data,v);assert(Controls.Institution4.hidden==false);assert(Controls.InstitutionState4.text=='能力未激活')
assert(Controls.Institution4.tip:find('本测试版尚未实现'))
LuaEvents.SPC_InstitutionOverview(data,nil);assert(Controls.InstitutionContainer.hidden)
shutdown()
""")
for p in M.rglob('*.lua'):l.execute('assert(load(...))',p.read_text())
x=ET.parse(M/'SpecializationP0.modinfo').getroot();assert x.get('version')=='114'
assert sorted(f.text for f in x.findall('./Files/File'))==sorted(str(p.relative_to(M)) for p in M.rglob('*') if p.is_file() and p.suffix!='.modinfo')
ET.parse(M/'UI/Institutions.xml')
allowed={'UI/RuntimeAudit.lua','Gameplay.lua','Probe.lua','SpecializationP0.modinfo','UI/CityPotential.lua','InstitutionPresentation.lua','UI/InstitutionOverview.lua','UI/Institutions.lua','UI/Institutions.xml'}
for p in M.rglob('*'):
 if p.is_file() and str(p.relative_to(M)) not in allowed:assert p.read_bytes()==subprocess.check_output(['git','show','b1b997f:Mod/'+str(p.relative_to(M))],cwd=R),p
for p in ['InstitutionPresentation.lua','UI/InstitutionOverview.lua','UI/Institutions.lua']:
 s=(M/p).read_text()
 for forbidden in ['RequestPlayerOperation','SetUpdate','CreateBuilding','RemoveBuilding','SetProperty']:assert forbidden not in s,(p,forbidden)
for p in subprocess.check_output(['git','ls-files','Specialization/Design'],cwd=R,text=True).splitlines():assert (R/p).read_bytes()==subprocess.check_output(['git','show','b1b997f:'+p],cwd=R),p
print('U1 LOCAL PASS: cumulative/ACTIVE/UNKNOWN/identity/city-ref; owned-only filter, original data retained; 10k duplicate display/hover, fixed4 controls, zero new requests/writes; all Lua/XML/manifest114, all protected runtime and Design byte-identical')
