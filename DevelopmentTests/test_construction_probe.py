from pathlib import Path
import xml.etree.ElementTree as E
from lupa.lua55 import LuaRuntime
w=Path(__file__).resolve().parents[1];r=w/"Sid Meier's Civilization VI/Mods/SpecializationP0";l=LuaRuntime(unpack_returned_tuples=True)
l.execute('''
kind='Buildings';target='TARGET';cost=500;progress=10;owner=0;turn=1;calls=0;nextProgress=0;wonder=false
city={GetID=function() return 8 end,GetOwner=function() return owner end}
queue={CurrentlyBuilding=function() return target end,AddProgress=function(_,n)
 calls=calls+1;lastAmount=n;progress=progress+n
 if progress>=cost then nextProgress=progress-cost;target='NEXT';progress=nextProgress;cost=500 end
end}
city.GetBuildQueue=function() return queue end
P={IsTestPlayer=function(p) return p==0 end,Info=function(t,k) if t==kind then return {Index=1,IsWonder=wonder} end end}
Game={GetCurrentGameTurn=function() return turn end}
ExposedMembers={DLHD={Utils={GetCityCurrentBuildQueueCost=function() return cost end,GetCityCurrentBuildQueueProgress=function() return progress end}}}
shared={}
''')
l.execute((r/'ConstructionProbe.lua').read_text())
l.execute('''
SPCConstructionProbe.Start(P,shared);a=shared.ConstructionProbe
for _,k in ipairs({'Buildings','Districts'}) do
 kind=k;target='TARGET';cost=500;progress=10
 local before=calls;assert(a.Prepare(0,city):find('PREVIEW'));assert(calls==before)
 a.Apply(0,city);assert(progress==260 and calls==before+1 and lastAmount==250)
 a.Apply(0,city);assert(calls==before+1)
end
kind='Buildings';wonder=true;target='WONDER';cost=300;progress=200
assert(a.Prepare(0,city):find('Wonder'));a.Apply(0,city);assert(lastAmount==100 and nextProgress==0)
for _,k in ipairs({'Units','Projects'}) do kind=k;assert(a.Prepare(0,city):find('REJECTED')) end
kind='Buildings';target=nil;assert(a.Prepare(0,city):find('REJECTED'));target='TARGET';cost=500;progress=0
local n=calls;a.Prepare(0,city);progress=1;assert(a.Apply(0,city):find('REJECTED'));assert(calls==n)
a.Prepare(0,city);turn=2;assert(a.Apply(0,city):find('REJECTED'));assert(calls==n)
a.Prepare(0,city);owner=1;assert(a.Apply(0,city):find('REJECTED'));assert(calls==n);owner=0
-- Exception after an attempted grant cannot silently retry using the same preview.
a.Prepare(0,city);queue.AddProgress=function() calls=calls+1;error('engine uncertain') end
assert(a.Apply(0,city):find('RESULT_UNCERTAIN'));a.Apply(0,city);assert(calls==n+1)
''')
for p in r.rglob('*.lua'):l.execute('assert(load(...))',p.read_text())
m=E.parse(r/'SpecializationP0.modinfo').getroot();assert m.get('version')=='50'
for f in m.findall('.//File'):assert (r/f.text).exists()
x=E.parse(r/'UI/P0Panel.xml').getroot();ids=[n.get('ID') for n in x.iter() if n.get('ID')];assert len(ids)==len(set(ids));win=x.find("Container[@ID='Window']");assert len(win.findall('GridButton'))==10
assert win.find("Container[@ID='LegacyProbeButtons']/GridButton[@ID='GovernorButton']") is not None
print('PASS actual probe: preview no grant, Building/District/Wonder capped injection, simulated zero overflow, repeat/stale/invalid/exception protections, Lua/manifest50 and 9 task buttons. Engine AddProgress overflow remains user-game-test-required.')
