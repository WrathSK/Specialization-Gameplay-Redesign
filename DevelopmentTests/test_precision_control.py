from pathlib import Path
import sqlite3,xml.etree.ElementTree as ET
from lupa.lua55 import LuaRuntime
w=Path(__file__).resolve().parent.parent;r=w/"Sid Meier's Civilization VI/Mods/SpecializationP0"
source=sqlite3.connect((w/"Firaxis Games/Sid Meier's Civilization VI/Cache/DebugGameplay.sqlite").as_uri()+'?mode=ro',uri=True)
c=sqlite3.connect(':memory:');source.backup(c);source.close()
for table, key in [('TraitModifiers','ModifierId'),('ModifierArguments','ModifierId'),('Modifiers','ModifierId'),('RequirementSetRequirements','RequirementSetId'),('RequirementSets','RequirementSetId'),('RequirementArguments','RequirementId'),('Requirements','RequirementId')]:
    c.execute(f"DELETE FROM {table} WHERE {key} LIKE 'SPC_B029_%'")
before=set(c.execute('PRAGMA foreign_key_check'))
c.executescript((r/'Data/YieldCarrierProbe.sql').read_text())
assert set(c.execute('PRAGMA foreign_key_check'))==before
assert c.execute("select count(*) from Modifiers where ModifierId like 'SPC_B029_%'").fetchone()[0]==6
assert c.execute("select count(*) from ModifierArguments where ModifierId like 'SPC_B029_HALF_%' and Name='Amount' and Value='1.5'").fetchone()[0]==3
assert c.execute("select distinct TraitType from TraitModifiers where ModifierId like 'SPC_B029_%'").fetchall()==[('TRAIT_CIVILIZATION_SPC_TEST',)]
l=LuaRuntime(unpack_returned_tuples=True);l.execute((r/'YieldCarrierProbe.lua').read_text())
l.execute('''
YieldTypes={SCIENCE=0,CULTURE=1,PRODUCTION=2};local props={};local writes=0
plot={GetOwner=function() return 0 end,GetProperty=function(_,k) return props[k] end,SetProperty=function(_,k,v) writes=writes+1;props[k]=v end}
Map={GetPlot=function() return plot end};multiplier=1
city={GetOwner=function() return 0 end,GetID=function() return 1 end,GetX=function() return 2 end,GetY=function() return 3 end,
 GetYield=function(_,y) return 10+y+multiplier*((props.SPC_B029_ONE==1 and 1 or 0)+(props.SPC_B029_HALF==1 and 1.5 or 0)) end}
GameInfo={Modifiers={}}
for _,bit in ipairs({'ONE','HALF'}) do for _,y in ipairs({'SCIENCE','CULTURE','PRODUCTION'}) do GameInfo.Modifiers['SPC_B029_'..bit..'_'..y]={} end end
local p=SPCYieldCarrierProbe
assert(p.Run(0,city,'STEP'):find('delta=1.000000'))
assert(p.Run(0,city,'STEP'):find('delta=2.500000'))
for i=1,20 do assert(p.Run(0,city,'STEP'):find('delta=2.500000')) end
assert(p.Run(0,city,'OFF'):find('delta=0.000000'))
multiplier=1.5;assert(p.Run(0,city,'STEP'):find('delta=1.500000'))
assert(p.Run(0,city,'STEP'):find('delta=3.750000'))
local old=writes;p.Describe(0,city);assert(writes==old)
assert(p.Run(1,city,'STEP'):find('OWNER_CHANGED'));assert(writes==old)
GameInfo.Modifiers={};assert(p.Run(0,city,'STEP'):find('DEFINITIONS_ABSENT'));assert(writes==old)
assert(p.Run(0,city,'OFF'):find('delta=0.000000')) -- missing SQL does not prevent OFF
for _,bit in ipairs({'ONE','HALF'}) do for _,y in ipairs({'SCIENCE','CULTURE','PRODUCTION'}) do GameInfo.Modifiers['SPC_B029_'..bit..'_'..y]={} end end
for _,second in ipairs({0,1,1.5}) do
 p.Run(0,city,'OFF');multiplier=1
 city.GetYield=function(_,y) return 10+y+(props.SPC_B029_ONE==1 and 1 or 0)+(props.SPC_B029_HALF==1 and second or 0) end
 assert(p.Run(0,city,'STEP'):find('delta=1.000000'))
 local result=p.Run(0,city,'STEP')
 assert(result:find('delta='..string.format('%.6f',1+second)))
 for i=1,3 do assert(p.Run(0,city,'STEP')==result) end
 assert(p.Run(0,city,'OFF'):find('delta=0.000000'))
end
-- Actual Gameplay dispatch scope with this module already loaded.
print=function() end;include=function() end
SPCP0={VERSION='P0-B-030',IsTestPlayer=function(id) return id==0 end,Scalar=tostring}
ExposedMembers={};Players={[0]={GetCities=function() return {FindID=function(_,id) if id==1 then return city end end} end}}
GameEvents={SPC_P0_Request={Add=function(f) dispatch=f end}}
''')
l.execute((r/'Gameplay.lua').read_text().split('shared.TradeEvents={}')[0])
l.execute('''
dispatch(0,{Action='CARRIER_OFF',Token='off',CityID=1});assert(ExposedMembers.SPC_P0.LastToken=='off')
dispatch(0,{Action='SOURCE_YIELDS',Token='read',CityID=1});assert(ExposedMembers.SPC_P0.Snapshot:find('configured=0'))
''')
for p in r.rglob('*.lua'):l.execute('assert(load(...))',p.read_text())
m=ET.parse(r/'SpecializationP0.modinfo').getroot();assert m.attrib['version']=='37' and m.attrib['id']=='df9efdad-dd48-40a7-b868-87f0617bc16d'
for e in m.findall('.//File'):assert (r/e.text).is_file()
x=ET.parse(r/'UI/P0Panel.xml');ids=[e.attrib['ID'] for e in x.iter() if 'ID' in e.attrib];assert len(ids)==len(set(ids))
for name in ['CarrierStepButton','CarrierOffButton']:assert name in ids
print('STATIC_CONFIRMED: SQL against in-memory copy of current database; six trait-scoped effects, no added FK errors, fractional TEXT stored; Lua/XML/manifest valid.')
print('LOCAL_SIMULATION_PASS: fixed flag replacement, repeated STEP no accumulation, OFF, missing definitions/ownership, readonly report, actual request dispatch; fractional/multiplier behavior is fixture-only, not engine proof.')
