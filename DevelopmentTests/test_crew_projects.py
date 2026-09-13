from pathlib import Path
import sqlite3,xml.etree.ElementTree as E,zlib
from lupa.lua55 import LuaRuntime
w=Path(__file__).resolve().parents[1];r=w/"Sid Meier's Civilization VI/Mods/SpecializationP0"
# Prior action and investment regression, adapted only for new catalog/manifest/art fixtures.
p=w/'DevelopmentTests/test_crew_unit_actions.py';t=p.read_text().replace("=='55'","=='57'")
helpers="P.CrewBase=function(k) if k=='UNIT_SPC_CREW_250' then return 250 end end;P.CrewAmount=function() return 250 end"
t=t.replace("l.execute((r/'UnitActions.lua').read_text())",f"l.execute({helpers!r})\nl.execute((r/'UnitActions.lua').read_text())")
t=t.replace("m.executescript((r/'Data/Crew.sql').read_text())", "m.execute(\"delete from Units where UnitType like 'UNIT_SPC_CREW_%'\")\nm.execute(\"delete from Types where Type like 'UNIT_SPC_CREW_%'\")\nm.executescript((r/'Data/Crew.sql').read_text())")
t=t.replace('len(entries)==1','len(entries)==5')
t=t.replace("ui.execute((r/'UI/UnitSites.lua').read_text())", "ui.execute(\"SPCP0.CrewBase=function(k) if k=='UNIT_SPC_CREW_250' then return 250 end end\")\nui.execute((r/'UI/UnitSites.lua').read_text())")
exec(compile(t,str(p),'exec'),{'__file__':str(p)})
# UI regression retains raw diagnostics separately from player-facing tooltip.
p=w/'DevelopmentTests/test_unit_panel_actions.py';t=p.read_text().split('l=LuaRuntime',1)[1]
t='l=LuaRuntime'+t
t=t.replace("l.execute((r/'UI/UnitPanelActions.lua').read_text())", "l.execute(\"SPCP0.CrewBase=function(k) if k=='UNIT_SPC_CREW_250' then return 250 end end;SPCP0.CrewAmount=function() return 250 end\")\nl.execute((r/'UI/UnitPanelActions.lua').read_text())")
exec(compile(t,str(p),'exec'),globals())
l.execute('''
kind=1;tick(0.3);Controls.PrepareButton.click()
ExposedMembers.SPC_P0.LastToken=sent.Token
ExposedMembers.SPC_P0.Snapshot='B033 PREPARED city=458758 COMMERCE\\nPotential 1 -> 2 | consume 1 Settler #99'
tick(0.3);assert(Controls.PrepareButton.tip:find('1 → 2',1,true));assert(not Controls.PrepareButton.tip:find('458758',1,true))
kind=2;Controls.PrepareButton.click();ExposedMembers.SPC_P0.LastToken=sent.Token
ExposedMembers.SPC_P0.Snapshot='CREW PREPARED | consume this Crew (250)\\nProgress=272 / 275 | apply=3 | waste=247'
tick(0.3);assert(Controls.PrepareButton.tip:find('本次投入：3',1,true));assert(Controls.PrepareButton.tip:find('超出浪费：247',1,true))
Controls.PrepareButton.click();ExposedMembers.SPC_P0.LastToken=sent.Token
ExposedMembers.SPC_P0.Snapshot='REJECTED: shared hint [MOVE_TO_LEGAL_TARGET]'
tick(0.3);assert(Controls.PrepareButton.tip:find('施工队移到',1,true));assert(not Controls.PrepareButton.tip:find('REJECTED',1,true))
''')
# Actual catalog, five denominations and every native speed. No rounding.
v=LuaRuntime(unpack_returned_tuples=True);v.execute((r/'Probe.lua').read_text())
v.execute('''GameConfiguration={GetGameSpeedType=function() return 0 end};GameInfo={GameSpeeds={[0]={CostMultiplier=100}}}''')
for mult in [50,67,100,150,300]:
 v.execute(f'GameInfo.GameSpeeds[0].CostMultiplier={mult}')
 for amount in [250,420,750,1000,1360]:
  assert abs(v.eval(f"SPCP0.CrewAmount('UNIT_SPC_CREW_{amount}')")-amount*mult/100)<1e-9
assert v.eval("SPCP0.CrewBase('UNIT_BUILDER')")==None
# Each denomination also passes through the actual executor, not just the arithmetic helper.
legacy=(w/'DevelopmentTests/test_crew_unit_actions.py').read_text()
setup=legacy.split("l.execute('''",1)[1].split("''')",1)[0]
a=LuaRuntime(unpack_returned_tuples=True);a.execute((r/'Probe.lua').read_text());a.execute(setup)
a.execute("P.CrewBase=SPCP0.CrewBase;P.CrewAmount=SPCP0.CrewAmount;GameConfiguration={GetGameSpeedType=function() return 0 end};GameInfo={GameSpeeds={[0]={CostMultiplier=100}}}")
a.execute((r/'UnitActions.lua').read_text())
a.execute("SPCUnitActions.Start(P,shared)")
for mult in [50,67,100,150,300]:
 for amount in [250,420,750,1000,1360]:
  a.execute(f"""
  P.Info=function() return {{UnitType='UNIT_SPC_CREW_{amount}'}} end
  GameInfo.GameSpeeds[0].CostMultiplier={mult};progress=0;cost=10000
  add(90);local token='size{amount}speed{mult}'
  local result=shared.UnitActions.Run(0,{{Action='UNIT_ACTION_PREPARE',UnitID=90,Token=token}})
  assert(result:find('CREW PREPARED'),result)
  local done=shared.UnitActions.Run(0,{{Action='UNIT_ACTION_CONFIRM',UnitID=90,Token=token..'confirm'}})
  assert(done:find('CREW CONSUMED'),done);assert(math.abs(last-{amount}*{mult}/100)<0.000001)
  """)
# SQL runs only in copied in-memory database.
d=sqlite3.connect((w/"Firaxis Games/Sid Meier's Civilization VI/Cache/DebugGameplay.sqlite").as_uri()+'?mode=ro',uri=True)
m=sqlite3.connect(':memory:');d.backup(m);m.create_function('Make_Hash',1,lambda x:zlib.crc32(x.encode()))
m.execute("delete from Units where UnitType like 'UNIT_SPC_CREW_%'");m.execute("delete from Types where Type like 'UNIT_SPC_CREW_%'")
m.executescript((r/'Data/Crew.sql').read_text());m.executescript((r/'Data/CrewProjects.sql').read_text())
for cost,amount in [(280,250),(460,420),(820,750),(1100,1000),(1500,1360)]:
 n=f'PROJECT_SPC_CREW_{amount}'
 assert m.execute('select Cost,CostProgressionModel,RequiredBuilding,PrereqTech,PrereqCivic,MaxPlayerInstances from Projects where ProjectType=?',(n,)).fetchone()==(cost,'NO_PROGRESSION_MODEL','BUILDING_SPC_CREW_PROJECT_ACCESS',None,None,None)
 mod=m.execute('select ModifierId from ProjectCompletionModifiers where ProjectType=?',(n,)).fetchone()[0]
 assert dict(m.execute('select Name,Value from ModifierArguments where ModifierId=?',(mod,)))=={'UnitType':f'UNIT_SPC_CREW_{amount}','Amount':'1','AllowUniqueOverride':'0'}
 assert m.execute('select BuildCharges,CanTrain,PurchaseYield from Units where UnitType=?',(f'UNIT_SPC_CREW_{amount}',)).fetchone()==(1,0,None)
# Localized text against a read-only source copy, icons against native alias-shaped fixture.
loc=sqlite3.connect((w/"Firaxis Games/Sid Meier's Civilization VI/Cache/DebugLocalization.sqlite").as_uri()+'?mode=ro',uri=True)
lm=sqlite3.connect(':memory:');loc.backup(lm);lm.executescript((r/'Text/TestText.sql').read_text())
for amount in [250,420,750,1000,1360]:
 for lang in ['en_US','zh_Hans_CN']:
  assert lm.execute('select Text from LocalizedText where Language=? and Tag=?',(lang,f'LOC_PROJECT_SPC_CREW_{amount}_NAME')).fetchone()
ic=sqlite3.connect(':memory:');ic.execute('create table IconDefinitions(Name text primary key,Atlas text,"Index" integer)')
ic.executemany('insert into IconDefinitions values(?,?,?)',[(n,'FIXTURE',0) for n in ['ICON_UNIT_BUILDER','ICON_UNIT_BUILDER_PORTRAIT']])
ic.executescript((r/'Data/Icons.sql').read_text())
for amount in [250,420,750,1000,1360]:
 for n in [f'ICON_PROJECT_SPC_CREW_{amount}',f'ICON_UNIT_SPC_CREW_{amount}',f'ICON_UNIT_SPC_CREW_{amount}_PORTRAIT']:
  assert ic.execute('select 1 from IconDefinitions where Name=?',(n,)).fetchone(),n
# Actual project eligibility: independent from adjacency/workers/governor high levels, rebuilt on load.
v.execute('''
P=SPCP0;P.IsTestPlayer=function(pid) return pid==0 end;P.Field=function(t,k) return t and t[k] end
P.Info=function(table,key) if table=='Buildings' then return {Index=7} else return {DistrictType='DISTRICT_INDUSTRIAL_ZONE'} end end
present=false;changes=0;complete=true;spec='INDUSTRY';owner=0
c={GetOwner=function() return owner end,GetID=function() return 8 end,
 GetBuildings=function() return {HasBuilding=function() return present end,RemoveBuilding=function() present=false;changes=changes+1 end} end,
 GetBuildQueue=function() return {CreateBuilding=function() present=true;changes=changes+1 end} end}
d={GetCity=function() return c end,GetID=function() return 3 end,GetType=function() return 1 end,IsComplete=function() return complete end}
Players={[0]={GetCities=function() return {Members=function() return ipairs({c}) end} end,GetDistricts=function() return {Members=function() return ipairs({d}) end} end}}
shared={EffectiveFacts={Read=function() return {specialization=spec,potential=1,active=1,first={districtID=3,type='DISTRICT_INDUSTRIAL_ZONE'}} end}}
Events={LoadScreenClose={Add=function(f) load=f end}};GameEvents={}
''')
v.execute((r/'CrewProjects.lua').read_text());v.execute('''
SPCCrewProjects.Start(P,shared);assert(not present);load();assert(present and changes==1)
shared.CrewProjects.Audit();assert(changes==1)
spec='RESEARCH';shared.CrewProjects.Audit();assert(not present and changes==2)
spec='INDUSTRY';complete=false;shared.CrewProjects.Audit();assert(not present)
complete=true;shared.CrewProjects.Audit();assert(present)
owner=1;shared.CrewProjects.Audit();assert(not present)
owner=0;load();assert(present)
shared.EffectiveFacts.Read=function() error('unknown') end;shared.CrewProjects.Audit();assert(not present)
''')
# Syntax and manifest resolution for entire runtime, not execution of engine APIs.
syntax=LuaRuntime(unpack_returned_tuples=True)
for p in r.rglob('*.lua'):syntax.execute('assert(load(...))',p.read_text())
for p in r.rglob('*.xml'):E.parse(p)
root=E.parse(r/'SpecializationP0.modinfo').getroot();assert root.get('version')=='57'
for f in root.findall('.//File'):assert (r/f.text).is_file(),f.text
print('LOCAL_SIMULATION_PASS B044: five SQL projects/units, catalog 25 speed combinations, access grant/revoke/load/idempotence, Chinese tooltip separation, prior consumption/investment protections. Native project completion and fractional engine injection require user testing.')
