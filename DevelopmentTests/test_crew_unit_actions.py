from pathlib import Path
import sqlite3,xml.etree.ElementTree as E,zlib
from lupa.lua55 import LuaRuntime
w=Path(__file__).resolve().parents[1];r=w/"Sid Meier's Civilization VI/Mods/SpecializationP0"
l=LuaRuntime(unpack_returned_tuples=True)
l.execute('''
props={};units={};progress=200;cost=300;current='WONDER';kills=0;grants=0;turn=1
city={GetOwner=function() return 0 end,GetID=function() return 8 end,
 GetBuildQueue=function() return {AddProgress=function(_,n) grants=grants+1;last=n;progress=progress+n end} end}
player={GetUnits=function() return {FindID=function(_,id) return units[id] end,Destroy=function(_,u) kills=kills+1;units[u:GetID()]=nil end} end,
 GetCities=function() return {FindID=function() return city end} end,
 GetProperty=function(_,k) return props[k] end,SetProperty=function(_,k,v) props[k]=v end}
Players={[0]=player};Game={GetCurrentGameTurn=function() return turn end}
Map={GetPlot=function(x,y) return {GetIndex=function() return x end} end}
P={IsTestPlayer=function(p) return p==0 end,Info=function() return {UnitType='UNIT_SPC_CREW_250'} end}
shared={UnitTargets={Refresh=function(_,p) shared.UnitTargetSnapshot={plots={{plot=10,cityID=8}}} end},
 ConstructionProbe={ReadSnapshot=function() return {target=current,kind='Buildings',cost=cost,progress=progress} end}}
function add(id)
 local up={};local u={x=10,charges=1}
 u.GetOwner=function() return 0 end;u.GetID=function() return id end;u.GetType=function() return 1 end
 u.GetX=function() return u.x end;u.GetY=function() return 0 end;u.GetBuildCharges=function() return u.charges end
 u.GetProperty=function(_,k) return up[k] end;u.SetProperty=function(_,k,v) up[k]=v end;units[id]=u;return u
end
''')
l.execute((r/'UnitActions.lua').read_text())
l.execute('''
SPCUnitActions.Start(P,shared);local a=shared.UnitActions
local function run(act,id,token) return a.Run(0,{Action='UNIT_ACTION_'..act,UnitID=id,Token=token}) end
local u=add(1)
assert(run('PREPARE',1,'p1'):find('CREW PREPARED'));assert(kills==0 and grants==0)
assert(run('CONFIRM',1,'c1'):find('CREW CONSUMED'));assert(kills==1 and grants==1 and last==100 and progress==300)
run('CONFIRM',1,'c2');assert(grants==1)
progress=0;cost=500;u=add(2);u.x=11
assert(run('PREPARE',2,'p2'):find('REJECTED'));assert(kills==1)
u.x=10;u.charges=2;assert(run('PREPARE',2,'p3'):find('EXACTLY_ONE'));u.charges=1
run('PREPARE',2,'p4');progress=1;assert(run('CONFIRM',2,'c4'):find('TARGET_CHANGED'));assert(units[2])
run('PREPARE',2,'p5');turn=2;assert(run('CONFIRM',2,'c5'):find('TARGET_CHANGED'))
run('PREPARE',2,'p6');assert(run('CONFIRM',2,'c6'):find('CREW CONSUMED'));assert(last==250 and kills==2 and grants==2)
SPCUnitActions.Start(P,shared);assert(shared.UnitActions.Run(0,{Action='UNIT_ACTION_CONFIRM',UnitID=2,Token='replay'}):find('REJECTED'));assert(grants==2)
''')
# Actual older center-investment suite remains valid; adjust only historical manifest assertion.
p=w/'DevelopmentTests/test_native_investment.py'
t=p.read_text().replace("['version']=='41'","['version']=='55'")
exec(compile(t,str(p),'exec'),{'__file__':str(p)})
# New district investment path, retaining actual ledger/executor mocks.
t=p.read_text().split('# Actual UI request',1)[0]
# Extract initial main Lua block and inject district adapter before reset tests.
setup=t.split("l.execute('''",1)[1].split("''')",1)[0]
needle='reset()\nfor level=2,4 do'
addition='''Players[0].GetDistricts=function() return {Members=function() return ipairs({{
GetCity=function() return c end,GetID=function() return 2 end,GetType=function() return 3 end,
IsComplete=function() return true end,GetX=function() return 9 end,GetY=function() return 5 end}}) end} end
P.Info=function() return {DistrictType='DISTRICT_CAMPUS'} end
reset();local siteUnit=add(70)
assert(shared.InvestmentAction.Prepare(0,c,70,'SITE',true):find('MOVE_SETTLER_TO_IDENTITY'))
siteUnit.x=9
assert(shared.InvestmentAction.Prepare(0,c,70,'SITE',true):find('PREPARED'))
assert(shared.InvestmentAction.Confirm(0,c,shared.InvestmentPreview.token):find('INVESTED'))
assert(kills==1 and shared.EffectiveFacts.Read(0,c).potential==2)
'''
v=LuaRuntime(unpack_returned_tuples=True)
for n in ['EffectiveFacts.lua','InvestmentAction.lua']:v.execute((r/n).read_text())
v.execute(setup.replace(needle,addition+needle))
d=sqlite3.connect((w/"Firaxis Games/Sid Meier's Civilization VI/Cache/DebugGameplay.sqlite").as_uri()+'?mode=ro',uri=True)
m=sqlite3.connect(':memory:');d.backup(m);m.create_function('Make_Hash',1,lambda x:zlib.crc32(x.encode()))
m.executescript((r/'Data/Crew.sql').read_text())
row=m.execute("select BuildCharges,CanTrain,PurchaseYield,FormationClass from Units where UnitType='UNIT_SPC_CREW_250'").fetchone()
assert row==(1,0,None,'FORMATION_CLASS_CIVILIAN'),row
assert m.execute("select count(*) from TypeTags where Type='UNIT_SPC_CREW_250'").fetchone()[0]==0
art=E.parse(r/'ArtDefs/Units.artdef').getroot()
entries=art.findall('m_RootCollections/Element/Element')
assert len(entries)==1 and entries[0].find('m_Name').get('text')=='UNIT_SPC_CREW_250'
E.parse(r/'Specialization.dep')
print('LOCAL_SIMULATION_PASS B042: Crew cap/consume/repeat/stale/charge guards; actual investment center regression + district path; read-only DB fixture and art XML. Engine visuals/actions not tested.')
ui=LuaRuntime(unpack_returned_tuples=True)
ui.execute("""
include=function() end;SPCP0={VERSION='P0-B-042',IsTestPlayer=function() return true end}
ExposedMembers={};Mouse={eLClick=1};PlayerOperations={EXECUTE_SCRIPT=1}
Game={GetLocalPlayer=function() return 0 end,GetCurrentGameTurn=function() return 3 end}
local callbacks={}
Events={LoadScreenClose={Add=function() end,Remove=function() end}}
LuaEvents={SPC_ToggleBuilderTargets=function() end}
sel=nil;citySel={GetID=function() return 8 end}
UI={GetHeadSelectedCity=function() return citySel end,GetHeadSelectedUnit=function() return sel end,
RequestPlayerOperation=function(_,_,p) sent=p end}
GameInfo={Units={[1]={UnitType='UNIT_SPC_CREW_250'}}}
Controls=setmetatable({},{__index=function(t,k)
local c={SetHide=function(self,v) self.hidden=v end,SetText=function(self,v) self.text=v end,RegisterCallback=function(self,_,f) self.click=f end};rawset(t,k,c);return c end})
ContextPtr={SetHide=function() end,SetInitHandler=function(_,f) init=f end,SetShutdown=function() end,SetUpdate=function(_,f) tick=f end}
""")
ui.execute((r/'UI/UnitSites.lua').read_text())
ui.execute("""
init();Controls.SpawnCrewButton.click();assert(sent.Action=='UNIT_ACTION_SPAWN' and sent.CityID==8)
sel={GetID=function() return 9 end,GetOwner=function() return 0 end,GetType=function() return 1 end,GetX=function() return 1 end,GetY=function() return 1 end}
Controls.PrepareUnitButton.click();assert(sent.Action=='UNIT_ACTION_PREPARE' and sent.UnitID==9)
Controls.ConfirmUnitButton.click();assert(sent.Action=='UNIT_ACTION_CONFIRM')
sel=nil;ExposedMembers.SPC_P0={Version='P0-B-042',LastToken=sent.Token,Snapshot='CREW CONSUMED'}
tick(0.3);assert(Controls.Report.text=='CREW CONSUMED' and not Controls.Window.hidden)
""")
print('LOCAL_SIMULATION_PASS B042 UI: spawn/prepare/confirm dispatch and receipt survives unit disappearance.')
