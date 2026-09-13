from pathlib import Path
from lupa import LuaRuntime
import xml.etree.ElementTree as ET
P=Path(__file__).resolve().parent;R=P.parent/"Sid Meier's Civilization VI/Mods/SpecializationP0"
n={'__file__':str(P/'test_auto_constant_support.py')}
exec((P/'test_auto_constant_support.py').read_text().split('\nl=LuaRuntime(')[0],n)
f=n['f'].replace('B023_DATABASE_MISSING','B024_DATABASE_MISSING')+'''
defs.CULTURE=445
newcity()
Players[99]={}
setmetatable(Players,{__pairs=function(t)
 local i=0;return function() i=i+1;if i==1 then return 99,t[99] elseif i==2 then return 0,t[0] end end
end})
finish(1);assert(present[444],"DIRECT_COMPLETION_MISSING")
present[444]=nil;s.ResearchSupport.Audit()
assert(present[444],"UNREADY_PLAYER_ABORTED_VALID_CITY")
local prior=calls;s.ResearchSupport.Audit();assert(calls==prior)
assert(s.ResearchSupport.Run(0,city,"RESEARCH_READ"):find("skippedPlayers=1"))
boot();start();Events.LoadScreenClose.Fire();assert(present[444])
'''
l=LuaRuntime(unpack_returned_tuples=True)
for name in ['BindingProbe.lua','CityJournalProbe.lua','FreshBindingHook.lua','CityFlowProbe.lua','ResearchSupport.lua']:l.execute((R/name).read_text())
l.execute(f)
# Reproduce the isolated regression against the frozen B023 module.
old=R.parents[2]/'DevelopmentBackups/Specialization-before-B024'/R.relative_to(R.parents[2])/'ResearchSupport.lua'
# Explicit workspace path avoids assumptions about nested runtime parents.
old=P.parent/'DevelopmentBackups/Specialization-before-B024'/R.relative_to(P.parent)/'ResearchSupport.lua'
prior=LuaRuntime(unpack_returned_tuples=True)
for name in ['BindingProbe.lua','CityJournalProbe.lua','FreshBindingHook.lua','CityFlowProbe.lua']:prior.execute((R/name).read_text())
prior.execute(old.read_text())
try:prior.execute(f.replace('B024_DATABASE_MISSING','B023_DATABASE_MISSING'))
except Exception as e:
 assert 'DIRECT_COMPLETION_MISSING' in str(e) or 'UNREADY_PLAYER_ABORTED_VALID_CITY' in str(e),str(e)
else:raise AssertionError('Old version unexpectedly passed regression')
for p in R.rglob('*.lua'):l.execute('assert(load(...))',p.read_text())
m=ET.parse(R/'SpecializationP0.modinfo').getroot();assert m.attrib['version']=='31'
for e in m.findall('.//File'):assert (R/e.text).is_file()
ET.parse(R/'UI/P0Panel.xml')
print('LOCAL_SIMULATION_PASS: original three-type scenarios + unready player first + direct completion + repair/load/idempotence; old B023 reproduces failure. Actual incident root cause remains unconfirmed without runtime scan evidence.')
