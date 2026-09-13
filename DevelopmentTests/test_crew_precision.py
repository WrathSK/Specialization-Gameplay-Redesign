from pathlib import Path
from lupa.lua55 import LuaRuntime
import xml.etree.ElementTree as E
w=Path(__file__).resolve().parents[1];r=w/"Sid Meier's Civilization VI/Mods/SpecializationP0"
b=w/'DevelopmentBackups/Specialization-before-B046-project-precision/RuntimeSnapshot'
for n in ['UnitActions.lua','UI/UnitPanelActions.lua','UI/UnitPanelActions.xml','Data/Crew.sql','Data/CrewProjects.sql','CrewProjects.lua','ConstructionProbe.lua']:
 assert (r/n).read_bytes()==(b/n).read_bytes(),n
# Full prior UX/settlement regression with current-version fixture adaptation only.
p=w/'DevelopmentTests/test_crew_ux.py';t=p.read_text().replace('P0-B-045','P0-B-046').replace("=='58'","=='59'")
exec(compile(t,str(p),'exec'),{'__file__':str(p)})
l=LuaRuntime(unpack_returned_tuples=True)
l.execute('''include=function(n) assert(n=='DL_ProductionPanel') end
GetDataHelper=function() return data end
function item(n) return {Type=n,Cost=99,Disabled=true} end
data={ProjectItems={item('OTHER_A'),item('PROJECT_SPC_CREW_250'),item('OTHER_B'),item('PROJECT_SPC_CREW_750'),item('OTHER_C'),item('PROJECT_SPC_CREW_420'),item('PROJECT_SPC_CREW_1360'),item('PROJECT_SPC_CREW_1000'),item('OTHER_D')},OtherField=17}
old=data.ProjectItems
''')
l.execute((r/'UI/CrewProjectOrder.lua').read_text())
l.execute('''
local got=GetDataHelper();assert(got.OtherField==17 and #got.ProjectItems==9)
local expect={'OTHER_A','PROJECT_SPC_CREW_250','PROJECT_SPC_CREW_420','PROJECT_SPC_CREW_750','PROJECT_SPC_CREW_1000','PROJECT_SPC_CREW_1360','OTHER_B','OTHER_C','OTHER_D'}
for i,t in ipairs(expect) do assert(got.ProjectItems[i].Type==t) end
assert(got.ProjectItems[1]==old[1] and got.ProjectItems[7]==old[3]);GetDataHelper()
for i,t in ipairs(expect) do assert(data.ProjectItems[i].Type==t) end
data={ProjectItems={item('A'),item('PROJECT_SPC_CREW_1360'),item('B'),item('PROJECT_SPC_CREW_420')}}
GetDataHelper();assert(data.ProjectItems[2].Type=='PROJECT_SPC_CREW_420' and data.ProjectItems[3].Type=='PROJECT_SPC_CREW_1360' and #data.ProjectItems==4)
data=nil;assert(GetDataHelper()==nil)
''')
# Actual observer wraps actual executor: fractional preservation and a deliberately integer engine mock.
legacy=(w/'DevelopmentTests/test_crew_unit_actions.py').read_text();setup=legacy.split("l.execute('''",1)[1].split("''')",1)[0]
for quantized in [False,True]:
 v=LuaRuntime(unpack_returned_tuples=True);v.execute((r/'Probe.lua').read_text());v.execute(setup)
 v.execute("P.CrewBase=SPCP0.CrewBase;P.CrewAmount=SPCP0.CrewAmount;GameConfiguration={GetGameSpeedType=function() return 0 end};GameInfo={GameSpeeds={[0]={CostMultiplier=67}}}")
 if quantized:v.execute('city.GetBuildQueue=function() return {AddProgress=function(_,n) grants=grants+1;last=n;progress=progress+math.floor(n) end} end')
 v.execute((r/'UnitActions.lua').read_text());v.execute('SPCUnitActions.Start(P,shared)')
 v.execute((r/'CrewPrecision.lua').read_text());v.execute('SPCCrewPrecision.Start(P,shared)')
 v.execute('''
progress=0;cost=5000;add(1)
local a=shared.UnitActions;local prepared=a.Run(0,{Action='UNIT_ACTION_PREPARE',UnitID=1,Token='prepare'})
assert(prepared:find('CREW PREPARED'));assert(kills==0 and grants==0)
local result=a.Run(0,{Action='UNIT_ACTION_CONFIRM',UnitID=1,Token='confirm'})
assert(result:find('CREW CONSUMED') and kills==1 and grants==1 and last==167.5)
assert(shared.CrewPrecision.expected==167.5 and not shared.CrewPrecision.unitPresent)
''')
 assert v.eval('shared.CrewPrecision.difference')==(-.5 if quantized else 0)
 v.execute('''
local n=grants;shared.UnitActions.Run(0,{Action='UNIT_ACTION_CONFIRM',UnitID=1,Token='repeat'});assert(grants==n)
-- Failed observation cannot stop original preparation/confirmation.
add(2);progress=0;shared.UnitActions.Run(0,{Action='UNIT_ACTION_PREPARE',UnitID=2,Token='p2'})
local originalRefresh=shared.UnitTargets.Refresh;local calls=0
shared.UnitTargets.Refresh=function(...) calls=calls+1;if calls==1 then error('observer failed') end;return originalRefresh(...) end
local result=shared.UnitActions.Run(0,{Action='UNIT_ACTION_CONFIRM',UnitID=2,Token='c2'})
assert(result:find('CREW CONSUMED') and grants==n+1 and shared.CrewPrecision.error)
''')
root=E.parse(r/'SpecializationP0.modinfo').getroot();act=root.find("InGameActions/ReplaceUIScript[@id='SPC_B046_ProjectOrder']/Properties")
assert act.findtext('LuaContext')=='ProductionPanel' and int(act.findtext('LoadOrder'))>150000
print('LOCAL_SIMULATION_PASS B046: contiguous stable project grouping, partial lists, untouched row values; actual observer + executor at 67%, injected integer quantization detected, instrumentation failure does not alter action. Native engine precision remains user-test-required.')
# Actual precision report consumes UI getters, count and last confirmation without sending an action.
u=LuaRuntime(unpack_returned_tuples=True);u.execute((r/'Probe.lua').read_text())
u.execute('''
SPCP0.IsTestPlayer=function() return true end;include=function() end
Game={GetLocalPlayer=function() return 0 end};GameConfiguration={GetGameSpeedType=function() return 0 end}
GameInfo={GameSpeeds={[0]={CostMultiplier=67}},Projects={},Units={[1]={UnitType='UNIT_SPC_CREW_250'}}}
for i,s in ipairs(SPCP0.Specs) do GameInfo.Projects['PROJECT_SPC_CREW_'..s.charge]={Index=i} end
city={GetOwner=function() return 0 end,GetName=function() return '测试城' end,
GetBuildQueue=function() return {GetProjectCost=function(_,i) return SPCP0.Specs[i].cost*.67 end,GetProjectProgress=function() return 0 end} end}
Players={[0]={GetUnits=function() return {Members=function() return ipairs({{GetType=function() return 1 end}}) end} end}}
UI={GetHeadSelectedUnit=function() end,GetHeadSelectedCity=function() return city end,RequestPlayerOperation=function() error('must not send actions') end}
ExposedMembers={SPC_P0={CrewPrecision={owner=0,cityID=8,turn=1,before=0,after=167,cost=5000,expected=167.5,observed=167,difference=-.5,unitPresent=false}}}
Locale={Lookup=function(n) return n end};Mouse={eLClick=1};Events={LoadScreenClose={Add=function() end}};LuaEvents={}
Controls=setmetatable({},{__index=function(t,k) local c={SetHide=function() end,SetText=function(self,v) self.text=v end,RegisterCallback=function(self,_,f) self.click=f end};t[k]=c;return c end})
ContextPtr={SetHide=function() end,SetInitHandler=function(_,f) init=f end,SetUpdate=function() end,SetShutdown=function() end}
''')
u.execute((r/'UI/UnitSites.lua').read_text());u.execute('''init();Controls.PrecisionButton.click();assert(Controls.Report.text:find('差值=-0.5',1,true));assert(Controls.Report.text:find('1级=1',1,true));assert(Controls.Report.text:find('67%',1,true))''')
print('LOCAL_SIMULATION_PASS B046 report: project getters, speed, unit counts and measured difference; read button sends no game action.')
