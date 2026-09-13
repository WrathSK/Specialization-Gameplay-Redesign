"""D0014 all non-Campus district scope regression; legacy test files stay frozen."""
from pathlib import Path
w=Path(__file__).resolve().parents[1]
wrapper=(w/'DevelopmentTests/test_b051_background_fix.py').read_text()
wrapper=wrapper.replace("root.get('version')=='66'", "root.get('version')=='67'").replace("report:find('B051.66')","report:find('B051.67')")
inject='''s=s.replace("unknown=district(9,1,'DISTRICT_UNKNOWN',1);fire('GameCoreEventPublishComplete');assert(amount(cities[1],'SCIENCE')==0)", "unknown=district(9,1,'DISTRICT_UNKNOWN',1);fire('GameCoreEventPublishComplete');assert(amount(cities[1],'SCIENCE')==9)")
s=s.replace("assert(shared.CopyYields.errors['0:1:SCIENCE']:find('SCOPE_UNRESOLVED'))", "assert(not shared.CopyYields.errors['0:1:SCIENCE'])")
'''
wrapper=wrapper.replace('exec(compile(s,',inject+'exec(compile(s,')
exec(compile(wrapper,str(w/'DevelopmentTests/test_b051_background_fix.py'),'exec'))
l.execute('''
local info=P.Info
P.Info=function(t,k)
 local row=info(t,k)
 if t=='Districts' then row.Name=k;row.RequiresPopulation=false end
 return row
end
for _,c in ipairs(cities) do c.GetName=function() return 'Test city' end end
Locale={Lookup=function(n) return n end}
-- All non-Campus types, including zero-yield and non-population districts.
for i,k in ipairs({'DISTRICT_ENCAMPMENT','DISTRICT_HOLY_SITE','DISTRICT_GOVERNMENT','DISTRICT_NEIGHBORHOOD','DISTRICT_ENTERTAINMENT_COMPLEX','DISTRICT_CITY_CENTER'}) do
 district(20+i,1,k,1,2)
end
fire('GameCoreEventPublishComplete');assert(amount(cities[1],'SCIENCE')==17.5)
local n=changes;fire('GameCoreEventPublishComplete');assert(changes==n)
local zero=district(30,1,'DISTRICT_AQUEDUCT',0);fire('GameCoreEventPublishComplete');assert(amount(cities[1],'SCIENCE')==17.5)
zero.prod=2;fire('GameCoreEventPublishComplete');assert(amount(cities[1],'SCIENCE')==18.5)
zero.complete=false;fire('GameCoreEventPublishComplete');assert(amount(cities[1],'SCIENCE')==17.5)
campus.prod=9999;fire('GameCoreEventPublishComplete');assert(amount(cities[1],'SCIENCE')==17.5)
facts[1].active=3;fire('GovernorAssigned');assert(amount(cities[1],'SCIENCE')==0)
facts[1].active=4;fire('GovernorEstablished');assert(amount(cities[1],'SCIENCE')==17.5)
''')
l.execute((r/'Lv4CopyRead.lua').read_text())
l.execute('''
local m=SPCLv4CopyRead.Metadata(P,shared,0,cities[1],'scope-test')
local text=SPCLv4CopyRead.Render(P,m)
assert(text:find('全部非学院区域合计=35') and text:find('DISTRICT_NEIGHBORHOOD') and text:find('DISTRICT_GOVERNMENT'))
assert(not text:find('范围另行确认'))
''')
print('LOCAL_SIMULATION_PASS D0014 all types / no population-slot filter / city center / zero-yield / cross-yield / incomplete excluded / Campus excluded / ACTIVE gating / readout same scope. Native new scope USER_GAME_TEST_REQUIRED.')
