"""Actual API-shaped candidate in mock environment; never starts the game."""
from pathlib import Path
import sqlite3
from lupa import LuaRuntime
p=Path(__file__).resolve().parent
l=LuaRuntime(unpack_returned_tuples=True)
l.globals().Carrier=l.execute((p/'EligibilityCarrierCandidate.lua').read_text())
l.execute('''
local trait="TRAIT_CIVILIZATION_SPC_TEST"
local rows={{CivilizationType="CIVILIZATION_SPC_TEST",TraitType=trait}}
local function iter()
 local i=0;return function() i=i+1;return rows[i] end
end
local function forbidden() error("NO_CITY_PROPERTY_HUMAN_OR_UI_ACCESS") end
local env={Players={[0]={GetCities=forbidden,GetProperty=forbidden},[1]={},[2]={}},
 PlayerConfigurations={
 [0]={GetCivilizationTypeName=function() return "CIVILIZATION_SPC_TEST" end,IsHuman=forbidden},
 [1]={GetCivilizationTypeName=function() return "CIVILIZATION_SCOTLAND" end},
 [2]={GetCivilizationTypeName=function() return "CIVILIZATION_OTHER" end}},
 GameInfo={Traits={[trait]={TraitType=trait}},CivilizationTraits=iter}}
local c=Carrier.New(env,trait)
assert(c.Read(0).status=="ENABLED" and c.Read(1).status=="DISABLED")
assert(c.Read(0).contextSource=="GAMEPLAY_CANDIDATE") -- not a fabricated MOCK or certified engine result
assert(c.Read(2).status=="DISABLED")
rows[2]={CivilizationType="CIVILIZATION_OTHER",TraitType=trait}
assert(c.Read(2).status=="ENABLED") -- configurable carrier, no core civ/leader restriction
rows[2]=nil;assert(c.Read(2).status=="DISABLED") -- no stale enabled cache
assert(c.Read(-1).status=="UNKNOWN" and c.Read(9).status=="UNKNOWN")
env.PlayerConfigurations[0]=nil;assert(c.Read(0).status=="UNKNOWN")
env.PlayerConfigurations[0]={GetCivilizationTypeName=function() return "" end}
assert(c.Read(0).status=="UNKNOWN")
env.PlayerConfigurations[0]={GetCivilizationTypeName=function() return "CIVILIZATION_SPC_TEST" end}
env.GameInfo.Traits[trait]=nil;assert(c.Read(0).status=="UNKNOWN")
env.GameInfo.Traits[trait]={}
env.GameInfo.CivilizationTraits=function()
 local n=0;return function() n=n+1;if n==1 then return rows[1] end;error("PARTIAL_DATABASE") end
end
assert(c.Read(0).status=="UNKNOWN") -- even after matching row, partial read not enabled
assert(c.Read(1).status=="UNKNOWN") -- failed lookup is not disabled
-- Reconstruct fresh instance/complete tables (simulated load) without prior events/cache.
env.GameInfo.CivilizationTraits=iter
assert(Carrier.New(env,trait).Read(0).status=="ENABLED")
''')
# Inspect the actual identity SQL in isolated in-memory tables.
r=p.parent/"Sid Meier's Civilization VI/Mods/SpecializationP0/Data/Identity.sql"
sql=r.read_text()
import re
con=sqlite3.connect(':memory:')
con.execute('create table Traits(TraitType text,Name text,Description text)')
con.execute('create table CivilizationTraits(CivilizationType text,TraitType text)')
for table in ['Traits','CivilizationTraits']:
    statement=re.search(r'INSERT INTO '+table+r'\b[^;]+;',sql).group()
    con.execute(statement)
assert con.execute('select CivilizationType from CivilizationTraits where TraitType=?',('TRAIT_CIVILIZATION_SPC_TEST',)).fetchall()==[('CIVILIZATION_SPC_TEST',)]
assert con.execute('select count(*) from Traits where TraitType=?',('TRAIT_CIVILIZATION_SPC_TEST',)).fetchone()[0]==1
print('LOCAL_SIMULATION_PASS: API-shaped read-only carrier; ready/missing/partial cases; configurable civ binding; fresh reconstruction; no city/Human/UI/property access. In-memory actual identity SQL binding confirmed. Gameplay execution remains untested.')
