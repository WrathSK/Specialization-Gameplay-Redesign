"""Read cached SQLite in mode=ro; execute actual Lua family/candidate code; no game."""
from pathlib import Path
import sqlite3
from lupa import LuaRuntime
p=Path(__file__).resolve().parent
c=sqlite3.connect((p.parent/"Firaxis Games/Sid Meier's Civilization VI/Cache/DebugGameplay.sqlite").as_uri()+'?mode=ro',uri=True)
c.row_factory=sqlite3.Row
districts=[dict(r) for r in c.execute('SELECT DistrictType FROM Districts ORDER BY DistrictType')]
replaces=[dict(r) for r in c.execute('SELECT * FROM DistrictReplaces ORDER BY CivUniqueDistrictType')];c.close()
lua=LuaRuntime(unpack_returned_tuples=True)
def rows(items): return lua.table_from([lua.table_from(item) for item in items])
family=lua.execute((p/'DistrictFamily.lua').read_text())
registry=family.Build(rows(districts),rows(replaces));assert registry.status=='READY'
expected={'DISTRICT_CAMPUS':'CAMPUS','DISTRICT_SEOWON':'CAMPUS','DISTRICT_OBSERVATORY':'CAMPUS',
'DISTRICT_THEATER':'THEATER_SQUARE','DISTRICT_ACROPOLIS':'THEATER_SQUARE',
'DISTRICT_INDUSTRIAL_ZONE':'INDUSTRIAL_ZONE','DISTRICT_HANSA':'INDUSTRIAL_ZONE','DISTRICT_OPPIDUM':'INDUSTRIAL_ZONE',
'DISTRICT_COMMERCIAL_HUB':'COMMERCIAL_HUB','DISTRICT_SUGUBA':'COMMERCIAL_HUB'}
actual={d:family.Resolve(registry,d).family for d in registry.mapping if family.Resolve(registry,d).family!='NON_V01'}
assert actual==expected,actual
assert family.Resolve(registry,'DISTRICT_GOVERNMENT').family=='NON_V01'
assert family.Resolve(registry,'UNLISTED_MOD_DISTRICT').status=='UNKNOWN'
# Synthetic mods: replacement chains independent of TraitType, no fake generic classification.
extra=districts+[{'DistrictType':'MOD_CHAIN'},{'DistrictType':'MOD_OTHER'}]
chain=replaces+[{'CivUniqueDistrictType':'MOD_CHAIN','ReplacesDistrictType':'DISTRICT_HANSA'}]
r=family.Build(rows(extra),rows(chain));assert family.Resolve(r,'MOD_CHAIN').family=='INDUSTRIAL_ZONE'
assert family.Resolve(r,'MOD_OTHER').family=='NON_V01'
for edges in [
 chain+[{'CivUniqueDistrictType':'MOD_CHAIN','ReplacesDistrictType':'DISTRICT_CAMPUS'}],
 replaces+[{'CivUniqueDistrictType':'MOD_CHAIN','ReplacesDistrictType':'MOD_OTHER'},{'CivUniqueDistrictType':'MOD_OTHER','ReplacesDistrictType':'MOD_CHAIN'}],
 replaces+[{'CivUniqueDistrictType':'MOD_CHAIN','ReplacesDistrictType':'MISSING'}]]:
 assert family.Build(rows(extra),rows(edges)).status=='UNKNOWN'
lua.globals().Registry=registry;lua.globals().Family=family
lua.globals().Candidate=lua.execute((p/'DistrictCompletionCandidate.lua').read_text())
lua.execute('''
local event={contextSource="MOCK_ONLY",name="OnDistrictConstructed",player=0,districtType="DISTRICT_SEOWON",x=4,y=7}
local obj={isTestCivilization=true,owner=0,cityOwner=0,districtType="DISTRICT_SEOWON",x=4,y=7,
 cityID=65536,districtID=3,complete=true,lifecycle="KNOWN_CURRENT_CITY"}
local f=Family.Resolve(Registry,event.districtType)
local function inspect() return Candidate.Inspect(event,obj,f) end
assert(inspect().status=="CANDIDATE_COMPLETION" and inspect().family=="CAMPUS")
assert(inspect().cityID==65536 and inspect().districtID==3)
event.name="DistrictAddedToMap";assert(inspect().status=="IGNORED")
event.name="DistrictBuildProgressChanged";assert(inspect().status=="IGNORED")
event.name="OnDistrictConstructed";obj.complete=false;assert(inspect().reason=="NOT_COMPLETE")
obj.complete=nil;assert(inspect().status=="UNKNOWN")
obj.complete=true;obj.pillaged=true;assert(inspect().status=="CANDIDATE_COMPLETION")
obj.lifecycle="LOAD_REPLAY_UNKNOWN";assert(inspect().status=="UNKNOWN")
obj.lifecycle="CAPTURE_UNKNOWN";assert(inspect().status=="UNKNOWN")
obj.lifecycle="KNOWN_CURRENT_CITY";obj.cityOwner=1;assert(inspect().status=="UNKNOWN")
obj.cityOwner=0;obj.isTestCivilization=false;assert(inspect().status=="IGNORED")
obj.isTestCivilization=true;obj.cityID=nil;assert(inspect().status=="UNKNOWN");obj.cityID=65536
event.contextSource="GAMEPLAY";assert(inspect().status=="UNKNOWN")
''')
print(f'LOCAL_SIMULATION_PASS: {len(districts)} cached districts / {len(replaces)} replacements; {len(actual)} v0.1 types; chains, invalid graphs, completion candidate isolation. Cached DB is not a guarantee of the next mod load order.')
