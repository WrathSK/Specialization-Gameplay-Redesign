from pathlib import Path
import math,xml.etree.ElementTree as E
from lupa.lua55 import LuaRuntime
w=Path(__file__).resolve().parents[1];r=w/"Sid Meier's Civilization VI/Mods/SpecializationP0";b=w/'DevelopmentBackups/Specialization-before-D0012-integer-crews/RuntimeSnapshot'
for n in ['UnitActions.lua','ConstructionProbe.lua','CrewPrecision.lua','CrewProjects.lua','Data/Crew.sql','Data/CrewProjects.sql','UnitTargets.lua','UI/UnitPanelActions.lua','UI/UnitPanelActions.xml','InvestmentAction.lua']:
 assert (r/n).read_bytes()==(b/n).read_bytes(),n
legacy=(w/'DevelopmentTests/test_crew_unit_actions.py').read_text();setup=legacy.split("l.execute('''",1)[1].split("''')",1)[0]
l=LuaRuntime(unpack_returned_tuples=True);l.execute((r/'Probe.lua').read_text());l.execute(setup)
l.execute("P.CrewBase=SPCP0.CrewBase;P.CrewAmount=SPCP0.CrewAmount;GameConfiguration={GetGameSpeedType=function() return 0 end};GameInfo={GameSpeeds={[0]={CostMultiplier=100}}}")
l.execute((r/'UnitActions.lua').read_text());l.execute('SPCUnitActions.Start(P,shared)')
for speed in [50,67,100,150,300]:
 for base in [250,420,750,1000,1360]:
  amount=math.floor(base*speed/100)
  for cap in [False,True]:
   remaining=10 if cap else 10000
   token=f'{speed}-{base}-{cap}'
   l.execute(f"""
   GameInfo.GameSpeeds[0].CostMultiplier={speed};P.Info=function() return {{UnitType='UNIT_SPC_CREW_{base}'}} end
   progress=0;cost={remaining};add(90)
   assert(P.CrewAmount('UNIT_SPC_CREW_{base}')=={amount})
   local g=grants;local k=kills;local a=shared.UnitActions
   assert(a.Run(0,{{Action='UNIT_ACTION_PREPARE',UnitID=90,Token='{token}'}}):find('CREW PREPARED'));assert(kills==k and grants==g)
   assert(a.Run(0,{{Action='UNIT_ACTION_CONFIRM',UnitID=90,Token='{token}-c'}}):find('CREW CONSUMED'))
   assert(last==math.min({amount},{remaining}) and kills==k+1 and grants==g+1)
   a.Run(0,{{Action='UNIT_ACTION_CONFIRM',UnitID=90,Token='{token}-duplicate'}});assert(grants==g+1)
   """)
# Actual UI/ReadView regression at Quick speed: reuse the previous complete fixture, update only expected integers.
p=w/'DevelopmentTests/test_crew_ux.py';t=p.read_text().split('l=LuaRuntime(unpack_returned_tuples=True)',1)[1]
t='l=LuaRuntime(unpack_returned_tuples=True)'+t
t=t.replace('CostMultiplier=100','CostMultiplier=67').replace('投入250','投入167').replace('本次投入：250','本次投入：167').replace('浪费：150','浪费：67')
exec(compile(t,str(p),'exec'),globals())
syntax=LuaRuntime(unpack_returned_tuples=True)
for p in r.rglob('*.lua'):syntax.execute('assert(load(...))',p.read_text())
for p in r.rglob('*.xml'):E.parse(p)
root=E.parse(r/'SpecializationP0.modinfo').getroot();assert root.get('version')=='60'
for f in root.findall('.//File'):assert (r/f.text).is_file()
print('LOCAL_SIMULATION_PASS D0012/B047: 25 exact floor amounts, 50 actual capped/full consume cases with duplicate guards; Quick UI preview/confirmation integer167 and overflow67; protected mechanics byte-identical; Lua/XML/manifest valid.')
