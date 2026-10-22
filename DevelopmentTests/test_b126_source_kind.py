"""B126 actual conquest handler without Gameplay IsMinor; retained B124 regression."""
from pathlib import Path
R=Path(__file__).resolve().parents[1]
s=(R/'DevelopmentTests/test_b124_claim.py').read_text()
extra=r"""
local previousInfo=P.Info
local levels={GENEVA='CIVILIZATION_LEVEL_CITY_STATE',MOD_MINOR='CIVILIZATION_LEVEL_CITY_STATE',FREE='CIVILIZATION_LEVEL_FREE_CITIES',BARB='CIVILIZATION_LEVEL_TRIBE',FULL='CIVILIZATION_LEVEL_FULL_CIV'}
P.Info=function(t,k)if t=='Civilizations'then return levels[k] and {StartingCivilizationLevelType=levels[k]}end;return previousInfo(t,k)end
for _,name in ipairs({'GENEVA','MOD_MINOR','FREE','BARB','FULL','MISSING','NO_CONFIG','THROW','BAD_TYPE','HUMAN'})do
 start();local c=ai(fresh(1));Players[3].IsMajor=function()return false end
 -- Deliberately absent: no mock API that does not exist in Gameplay.
 assert(Players[3].IsMinor==nil)
 PlayerConfigurations={[3]={GetCivilizationTypeName=function()
  if name=='THROW'then error('config unavailable')end
  if name=='BAD_TYPE'then return 7 end
  return name=='HUMAN' and 'GENEVA' or name
 end}}
 if name=='NO_CONFIG'then PlayerConfigurations[3]=nil end
 if name=='HUMAN'then Players[3].IsHuman=function()return true end end
 district(c,'DISTRICT_CAMPUS',201,true);take(c);flush()
 if name=='GENEVA' or name=='MOD_MINOR'then
  assert(record(c) and record(c).acquisition.legacySet.RESEARCH and c.q.buildings[201],d.Describe(0,c))
  local frozen=encode(record(c));complete(c,'DISTRICT_THEATER');assert(encode(record(c))==frozen)
  request(c,'RESEARCH');Events.PlayerTurnDeactivated.Fire(0);turn=turn+1;Events.PlayerTurnActivated.Fire(0);flush()
  assert(record(c).claim and shared.EffectiveFacts.Read(0,c).potential==1)
  saved=true;boot();assert(shared.EffectiveFacts.Read(0,c).potential==1)
 else
  assert(not record(c),name..' unexpectedly admitted')
  assert(shared.EffectiveFacts.Describe(0,c):find('城市取得待确认'))
 end
end
-- Major path unchanged; do not require a new config/DB read there.
start();PlayerConfigurations=nil;local c=conquered(1,'DISTRICT_COMMERCIAL_HUB');assert(record(c).acquisition.legacySet.COMMERCE)
print('B126 LOCAL_SIMULATION_PASS: no IsMinor; native-style config/database classification; city-state + mod city-state claim/load, free/tribe/full/unknown/bad-config/human refusal; major path unchanged')
"""
s=s.replace('exec(compile(header+helpers+cases+', 'cases+=extra\nexec(compile(header+helpers+cases+')
exec(compile(s,str(R/'DevelopmentTests/test_b124_claim.py'),'exec'))
assert "P.Call(old,'IsMinor')" not in (R/'Mod/CityProgressionStore.lua').read_text()
