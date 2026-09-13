"""API-shaped current roster + qualification candidate. No actual game execution."""
from pathlib import Path
from lupa import LuaRuntime
p=Path(__file__).resolve().parent
l=LuaRuntime(unpack_returned_tuples=True)
for n,f in [('Roster','CurrentPlayerRoster.lua'),('Carrier','EligibilityCarrierCandidate.lua')]:
    l.globals()[n]=l.execute((p/f).read_text())
l.execute('''
local ids={0,1};local calls={}
local env={PlayerManager={GetAliveIDs=function() return ids end}}
local function reader(pid)
 calls[pid]=(calls[pid] or 0)+1
 return {contextSource="GAMEPLAY_CANDIDATE",player=pid,status=pid==0 and "ENABLED" or "DISABLED"}
end
local s=Roster.Collect(env,reader)
assert(s.status=="COMPLETE_ROSTER" and #s.enabled==1 and Roster.Classify(s,0)=="ENABLED")
assert(Roster.Classify(s,1)=="DISABLED" and Roster.Classify(s,54)=="NOT_CURRENT")
assert(not calls[54]) -- absent from fixture roster, not hardcoded excluded
ids={61,0,61};s=Roster.Collect(env,function(pid)
 return {contextSource="GAMEPLAY_CANDIDATE",player=pid,status="ENABLED"}
end)
assert(#s.enabled==2 and s.enabled[2]==61) -- high-numbered eligible player is allowed
ids={0,54};s=Roster.Collect(env,function(pid)
 if pid==54 then return {contextSource="GAMEPLAY_CANDIDATE",player=pid,status="UNKNOWN",reason="CIV_NOT_READY"} end
 return reader(pid)
end)
assert(#s.enabled==1 and s.unknown[54]=="CIV_NOT_READY" and Roster.Classify(s,54)=="UNKNOWN")
ids={};s=Roster.Collect(env,reader);assert(s.status=="COMPLETE_ROSTER" and #s.enabled==0)
ids=nil;assert(Roster.Collect(env,reader).status=="UNKNOWN")
ids={[1]=0,[3]=2};assert(Roster.Collect(env,reader).status=="UNKNOWN")
ids={0,-1};assert(Roster.Collect(env,reader).status=="UNKNOWN")
ids={0};s=Roster.Collect(env,function() error("READ_FAIL") end);assert(s.unknown[0] and #s.enabled==0)
s=Roster.Collect(env,function() return {player=1,contextSource="GAMEPLAY_CANDIDATE",status="ENABLED"} end)
assert(s.unknown[0] and #s.enabled==0)
-- Fresh collection discards dead players; later revival may be eligible again.
ids={0};local old=Roster.Collect(env,reader);ids={1};s=Roster.Collect(env,reader)
assert(Roster.Classify(s,0)=="NOT_CURRENT" and #s.enabled==0 and #old.enabled==1)
ids={0};assert(#Roster.Collect(env,reader).enabled==1)
env.PlayerManager.GetAliveIDs=function() error("ROSTER_FAIL") end
s=Roster.Collect(env,reader);assert(s.status=="UNKNOWN" and #s.enabled==0)
-- Compose with actual API-shaped carrier, poison all city/property paths.
local function poison() error("NO_CITY_OR_PROPERTY_WORK") end
local trait="TRAIT_CIVILIZATION_SPC_TEST"
env={PlayerManager={GetAliveIDs=function() return {0,1,54} end},
 Players={[0]={GetCities=poison},[1]={GetCities=poison},[54]={GetCities=poison}},
 PlayerConfigurations={
 [0]={GetCivilizationTypeName=function() return "TEST" end},
 [1]={GetCivilizationTypeName=function() return "OTHER" end},
 [54]={GetCivilizationTypeName=function() return "" end}},
 GameInfo={Traits={[trait]={}},CivilizationTraits=function()
  local done=false;return function() if not done then done=true;return {CivilizationType="TEST",TraitType=trait} end end
 end}}
local c=Carrier.New(env,trait);s=Roster.Collect(env,c.Read)
assert(#s.enabled==1 and s.disabled[1] and s.unknown[54])
assert(Roster.Classify(s,61)=="NOT_CURRENT")
-- No historical fact storage argument exists; absence cannot erase dormant city facts.
''')
print('LOCAL_SIMULATION_PASS: complete/current vs eligibility separation; absent and unknown distinct; duplicate/high IDs; partial/failing roster; owner mismatch; death/revival; composed carrier without city/property access. No live roster or slot identity proven.')
