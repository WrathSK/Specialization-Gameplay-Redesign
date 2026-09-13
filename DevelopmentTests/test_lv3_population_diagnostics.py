from pathlib import Path
w=Path(__file__).resolve().parents[1];r=w/"Sid Meier's Civilization VI/Mods/SpecializationP0"
p=w/'DevelopmentTests/test_lv3_effects.py';scope={'__file__':str(p),'__name__':'fixture'}
source=p.read_text().split('# Actual NetworkBridge')[0]
exec(compile(source,str(p),'exec'),scope);l=scope['l']
l.execute('''
kind='RESEARCH';potential=3;active=3;pop=4;workers=1;stored={};a.Audit()
city.GetYield=function() return 13.1 end
workers=0;local before=writes
local report=a.Describe(0,city)
assert(report:find('live workers=0',1,true))
assert(report:find('expected=0.0 carrier=2.0',1,true) or report:find('expected=0 carrier=2',1,true))
assert(report:find('Last audit workers=1',1,true) and report:find('13.1',1,true))
assert(writes==before)
a.Audit();report=a.Describe(0,city);assert(report:find('carrier=0',1,true))
''')
for p in r.rglob('*.lua'):l.execute('assert(load(...))',p.read_text())
print('PASS: actual read-only diagnostic distinguishes live workers0/old carrier2/last audit1/native total13.1; no mutation; earlier effects fixture regression passes. No new game proof.')
