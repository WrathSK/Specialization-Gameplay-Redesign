"""B051.66 regression: real background script driven solely by engine events, no frame callbacks."""
from pathlib import Path
w=Path(__file__).resolve().parents[1]
s=(w/'DevelopmentTests/test_b051_copy_yields.py').read_text()
s=s.replace("root.get('version')=='65'", "root.get('version')=='66'")
s=s.replace('update(1)', "fire('GameCoreEventPublishComplete')")
s=s.replace("fire('LoadScreenClose');assert(amount(cities[1],'SCIENCE')==0);", "fire('LoadScreenClose');")
s=s.replace('shared.CopyYields.Receive(pid,p) end}', "shared.CopyYields.Receive(pid,p);fire('GameCoreEventPublishComplete') end}")
s=s.replace("print('LOCAL_SIMULATION_PASS B051:", "print('LOCAL_SIMULATION_PASS B051.66 EVENT ONLY (including synchronous publish reentry):")
s=s.replace("m.executescript((r/'Data/CopyYields.sql').read_text())", "\n".join([
 "for table,col,pattern in [('BuildingModifiers','BuildingType','BUILDING_SPC_B051_%'),('ModifierArguments','ModifierId','SPC_B051_%'),('Modifiers','ModifierId','SPC_B051_%'),('Buildings','BuildingType','BUILDING_SPC_B051_%'),('Types','Type','BUILDING_SPC_B051_%')]:",
 " m.execute(f'DELETE FROM {table} WHERE {col} LIKE ?', (pattern,))",
 "m.executescript((r/'Data/CopyYields.sql').read_text())"]))
exec(compile(s,str(w/'DevelopmentTests/test_b051_copy_yields.py'),'exec'))
# Reset with no timer pulses; SystemUpdateUI is also a load-order fallback.
l.execute('''
enabled=true;network=true;unknown.complete=false
SPCCopyYields.Start(P,shared);shared.CopyYields.ready=true;shared.CopyYields.generation=99
fire('LoadScreenClose');fire('SystemUpdateUI')
assert(shared.CopyYields.samples[0] and amount(cities[1],'SCIENCE')==8.5)
local report=shared.CopyYields.Describe(0,cities[1]);assert(report:find('B051.66') and report:find('后台='))
shared.CopyYields.samples={};shared.CopyYields.Audit()
report=shared.CopyYields.Describe(0,cities[1]);assert(report:find('COPY_BACKGROUND_PENDING'))
''')
print('PASS diagnostic distinguishes unstarted/pending/current sample; no formula/SQL changes')
