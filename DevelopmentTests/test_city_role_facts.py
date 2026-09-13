"""Read-only selected-city facts; legacy properties never establish specialization."""
from pathlib import Path
from lupa import LuaRuntime
p=Path(__file__).resolve().parents[1]/"Sid Meier's Civilization VI/Mods/SpecializationP0/Probe.lua"
lua=LuaRuntime(unpack_returned_tuples=True);lua.execute(p.read_text())
lua.execute('''
PlayerConfigurations={[0]={GetCivilizationTypeName=function() return "CIVILIZATION_SPC_TEST" end,GetLeaderTypeName=function() return "LEADER_SPC_TEST" end}}
local props={SPC_P0_GOV_CONTROL_A007=1}
local capital={GetID=function() return 1 end,GetOwner=function() return 0 end}
local collection={GetCapitalCity=function() return capital end}
Players={[0]={GetCities=function() return collection end}}
local city={GetID=function() return 1 end,GetOwner=function() return 0 end,GetProperty=function(self,k) return props[k] end,
 SetProperty=function() error('WRITE_FORBIDDEN') end,GetDistricts=function() error('HISTORY_INFERENCE_FORBIDDEN') end,
 GetAssignedGovernor=function() error('GOVERNOR_OBJECT_FORBIDDEN') end}
local function read() return SPCP0.CityRoleFacts(city) end
local f=read();assert(f.capitalStatus=='YES' and f.centerStatus=='YES_CAPITAL' and f.governorLevelCeiling==1)
assert(f.specializationStatus=='UNKNOWN_NO_PERSISTENT_WRITER' and f.activeStatus=='UNKNOWN_SPECIALIZATION_AND_POTENTIAL')
props.SPC_P0_FIRST_SPEC='RESEARCH';f=read();assert(f.specialization==nil and f.legacySpecDiagnostic=='RESEARCH')
city.GetID=function() return 2 end;f=read();assert(f.capitalStatus=='NO' and f.centerStatus=='UNKNOWN')
props.SPC_P0_GOV_PRESENT=1;assert(read().governorLevelCeiling==1)
props.SPC_P0_GOV_ESTABLISHED=1
for level=2,4 do props['SPC_P0_GOV_REQ_'..level]=1;assert(read().governorLevelCeiling==level) end
props.SPC_P0_GOV_REQ_3=0;assert(read().governorGateStatus=='UNKNOWN_INCONSISTENT_PROPERTIES')
props.SPC_P0_GOV_CONTROL_A007=nil;assert(read().governorLevelCeiling==nil)
props={SPC_P0_GOV_CONTROL_A007=1,SPC_P0_GOV_REQ_2=0,SPC_P0_GOV_REQ_3=0,SPC_P0_GOV_REQ_4=0}
assert(read().governorLevelCeiling==1) -- zero is not truthy activation
props.SPC_P0_GOV_REQ_2='1';assert(read().governorLevelCeiling==nil)
collection.GetCapitalCity=nil;assert(read().capitalStatus=='UNKNOWN' and read().centerStatus=='UNKNOWN')
city.GetProperty=nil;assert(read().governorGateStatus=='UNKNOWN')
city.GetOwner=function() return 1 end;assert(read().status=='REJECTED_PLAYER')
''')
print('LOCAL_SIMULATION_PASS: read-only capital/noncapital/unknown role facts; untrusted legacy spec ignored; no inferred potential/ACTIVE; native ceiling 1-4, zero/missing/inconsistent gates; unavailable APIs and non-test rejection.')
