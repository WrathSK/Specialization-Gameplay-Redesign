"""B109: Mod enabled from new-game creation; no old-save migration compatibility.
Reuse B108 actual-module coverage. Two initialization assertions are adapted to the
user-confirmed support contract; all historical source tests remain unchanged.
"""
from pathlib import Path
R=Path(__file__).resolve().parents[1]
s=(R/'DevelopmentTests/test_b108_e2_multicity.py').read_text()
s=s.replace("=='135'", "=='136'")
s=s.replace("modinfo135", "modinfo136")
old="start();props={};saved=true;boot();assert(next(props)==nil and d.Describe(0):find('OLD_OR_UNKNOWN'))"
assert old in s
s=s.replace(old,"start();props={};saved=true;fresh(1);boot();assert(next(props)==nil and d.Describe(0):find('EXISTING_CITY'))")
old="start();props={};GameConfiguration.IsSavedGame=nil;boot();assert(next(props)==nil)"
assert old in s
s=s.replace(old,"start();props={};GameConfiguration.IsSavedGame=nil;boot();assert(props[INDEX] and props[INDEX].counter==0)")
cases=r'''-- Missing/throwing UI-only API is never invoked in Gameplay.
for _,api in ipairs({false,function()error('function expected instead of nil')end})do
 start();props={};GameConfiguration.IsSavedGame=api;local n=writes;boot()
 assert(props[INDEX] and props[INDEX].counter==0 and writes==n+1)
 Events.LoadScreenClose.Fire();assert(writes==n+1)
 local b=fresh(1);register(b);complete(b,'DISTRICT_CAMPUS')
 local c=fresh(2);register(c);complete(c,'DISTRICT_THEATER')
 assert(shared.EffectiveFacts.Read(0,b).specialization=='RESEARCH')
 assert(shared.EffectiveFacts.Read(0,c).specialization=='CULTURE')
 invest(b,777);local before=encode(props);n=writes;saved=true;boot()
 assert(encode(props)==before and writes==n and shared.EffectiveFacts.Read(0,b).potential==2)
 assert(shared.EffectiveFacts.Read(0,c).potential==1)
end
-- Missing index at an advanced turn or with an existing city never adopts history.
start();props={};turn=1;boot();assert(next(props)==nil and d.Describe(0):find('NOT_NEW_GAME'))
local text=d.Describe(0);assert(#text<600 and not text:find('stack traceback'))
assert(shared.EffectiveFacts.Describe(0,fresh(1))==text)
start();props={};fresh(1);boot();assert(next(props)==nil and d.Describe(0):find('EXISTING_CITY'))
-- Supported empty and populated saves restore existing index without new allocation.
start();local before=encode(props);local n=writes;turn=12;saved=true;boot()
assert(encode(props)==before and writes==n)
-- Unknown start-turn API cannot silently supply a default; no old-binding adoption.
start();props={};GameConfiguration.GetStartTurn=nil;boot();assert(next(props)==nil)
start();props={};GameConfiguration.GetStartTurn=function()error('/Civilization VI/CityProgressionStore.lua:625: START_API_UNAVAILABLE')end;boot()
assert(next(props)==nil and d.Describe(0):find('原因：START_API_UNAVAILABLE') and not d.Describe(0):find('原因：VI'))
start();props={SPC_DEV_BINDING_B013_P0={}};before=encode(props);boot()
assert(encode(props)==before and d.Describe(0):find('OLD_BINDING'))
start()
print('B109 LOCAL_SIMULATION_PASS: absent/throwing IsSavedGame ignored, first Research/Culture completion, investment/coldload, duplicate initialization, start-turn/zero-city/old-ledger guards, short diagnostics')
'''
s=s.replace("clean();print('B108 LOCAL_SIMULATION_PASS",cases+"\nclean();print('B108 LOCAL_SIMULATION_PASS",1)
exec(compile(s,str(R/'DevelopmentTests/test_b108_e2_multicity.py'),'exec'))
assert 'GameConfiguration.IsSavedGame()' not in (R/'Mod/CityProgressionStore.lua').read_text()
print('B109 STATIC_CONFIRMED: no UI bridge or new-save inference from missing index alone; native test pending')
