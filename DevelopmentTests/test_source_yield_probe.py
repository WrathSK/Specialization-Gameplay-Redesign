from pathlib import Path
from lupa.lua55 import LuaRuntime
import xml.etree.ElementTree as ET
r=Path(__file__).resolve().parent.parent/"Sid Meier's Civilization VI/Mods/SpecializationP0"
l=LuaRuntime(unpack_returned_tuples=True)
l.execute((r/'SourceYieldProbe.lua').read_text())
l.execute('''
YieldTypes={SCIENCE=0,CULTURE=1,PRODUCTION=2}
values={[0]=7.512345,[1]=1.25,[2]=11}
c={GetOwner=function() return 0 end,GetID=function() return 42 end,GetName=function() return 'Test City' end,GetYield=function(_,i) return values[i] end}
shared={CityFlowProbe={SupportFacts=function() return {specialization='RESEARCH',potential=1} end}}
local first=SPCSourceYieldProbe.Read(0,c,shared)
assert(first:find('SCIENCE total=7.512345') and first:find('CULTURE total=1.250000') and first:find('PRODUCTION total=11.000000'))
assert(first==SPCSourceYieldProbe.Read(0,c,shared))
values[0]=8.5;assert(SPCSourceYieldProbe.Read(0,c,shared):find('SCIENCE total=8.500000'))
values[1]=0/0;local out=SPCSourceYieldProbe.Read(0,c,shared);assert(out:find('CULTURE UNKNOWN') and out:find('SCIENCE total=8.500000'))
assert(SPCSourceYieldProbe.Read(1,c,shared):find('OWNER_CHANGED'))
YieldTypes=nil;GameInfo={Yields={YIELD_SCIENCE={Index=0},YIELD_CULTURE={Index=1},YIELD_PRODUCTION={Index=2}}}
assert(SPCSourceYieldProbe.Read(0,c,shared):find('SCIENCE total=8.500000'))
c.GetYield=function() error('GETTER_ABSENT') end
assert(SPCSourceYieldProbe.Read(0,c,shared):find('GETTER_ABSENT'))
-- Test actual scoped Gameplay request routing, before unrelated module initializers.
print=function() end
include=function() end
SPCP0={VERSION='P0-B-028',IsTestPlayer=function(id) return id==0 end,Scalar=tostring}
ExposedMembers={}
Players={[0]={GetCities=function() return {FindID=function(_,id) if id==42 then return c end end} end}}
GameEvents={SPC_P0_Request={Add=function(f) dispatch=f end}}
''')
s=(r/'Gameplay.lua').read_text().split('shared.TradeEvents={}')[0]
l.execute(s)
l.execute('''
ExposedMembers.SPC_P0.CityFlowProbe=shared.CityFlowProbe
c.GetYield=function(_,i) return i+2 end
YieldTypes={SCIENCE=0,CULTURE=1,PRODUCTION=2}
dispatch(0,{Action='SOURCE_YIELDS',Token='probe',CityID=42})
assert(ExposedMembers.SPC_P0.LastToken=='probe' and ExposedMembers.SPC_P0.Snapshot:find('SCIENCE total=2.000000'))
local last=ExposedMembers.SPC_P0.Snapshot
dispatch(1,{Action='SOURCE_YIELDS',Token='foreign',CityID=42});assert(ExposedMembers.SPC_P0.Snapshot==last)
''')
for p in r.rglob('*.lua'):l.execute('assert(load(...))',p.read_text())
m=ET.parse(r/'SpecializationP0.modinfo').getroot();assert m.attrib['version']=='35'
assert m.attrib['id']=='df9efdad-dd48-40a7-b868-87f0617bc16d'
for e in m.findall('.//File'):assert (r/e.text).is_file()
assert m.find(".//ImportFiles/File[.='SourceYieldProbe.lua']") is not None
xml=ET.parse(r/'UI/P0Panel.xml');assert xml.find(".//*[@ID='SourceYieldButton']") is not None
assert 'request("SOURCE_YIELDS")' in (r/'UI/P0Panel.lua').read_text()
print('LOCAL_SIMULATION_PASS: raw S/C/P, repeat/read refresh, partial getter errors, owner scope, enum fallback, actual Gameplay dispatch, Lua/XML/import and no native setters in fixture.')
