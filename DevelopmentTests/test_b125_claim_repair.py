"""B125 Claim access recovery and explicit city-state admission; local simulation only."""
from pathlib import Path
R=Path(__file__).resolve().parents[1]
s=(R/'DevelopmentTests/test_b124_claim.py').read_text()
# Keep original B124 assertions; append scoped cases inside the same actual-handler fixture.
extra=r"""
start();local c=ai(fresh(1));Players[3].IsMajor=function()return false end;Players[3].IsMinor=function()return true end
district(c,'DISTRICT_CAMPUS',201,true);take(c);flush()
assert(record(c) and record(c).acquisition.legacySet.RESEARCH and c.q.buildings[201])
assert(not record(c).claimTimer and record(c).base.potential==0)
local before=encode(record(c));c.q.buildings={};local writesBefore=writes
shared.ClaimProjects.Sync(0,c:GetID());assert(c.q.buildings[201] and encode(record(c))==before and writes==writesBefore)
shared.ClaimProjects.Sync(3,c:GetID());assert(encode(record(c))==before)
request(c,'RESEARCH');Events.PlayerTurnDeactivated.Fire(0);turn=turn+1;Events.PlayerTurnActivated.Fire(0);flush();assert(record(c).claim)
saved=true;boot();assert(shared.EffectiveFacts.Read(0,c).potential==1)
-- Neither minor nor major, unknown minor and human sources remain denied.
for _,mode in ipairs({'free','unknown','human'})do
 start();c=ai(fresh(1));Players[3].IsMajor=function()return false end
 Players[3].IsMinor=function()if mode=='unknown'then return nil end;return mode=='human'end
 if mode=='human'then Players[3].IsHuman=function()return true end end
 district(c,'DISTRICT_CAMPUS',201,true);take(c);flush();assert(not record(c))
 local report=shared.EffectiveFacts.Describe(0,c);assert(report:find('城市取得待确认') and not report:find('stack traceback'))
end
-- Missing loading notification for Claim only: exact sync recovers access; no identity/timer write.
start();c=conquered(1,'DISTRICT_COMMERCIAL_HUB');before=encode(record(c));c.q.buildings={}
local priorAdd=Events.LoadScreenClose.Add;Events.LoadScreenClose.Add=function()end
-- New independent Claim instance over same Store, suppress exact duplicate exit registration only in fixture.
local reg=shared.CityProgressionStore.RegisterExit;shared.CityProgressionStore.RegisterExit=function()end
SPCClaimProjects.Start(P,shared);shared.CityProgressionStore.RegisterExit=reg;Events.LoadScreenClose.Add=priorAdd
shared.ClaimProjects.Sync(0,c:GetID());assert(c.q.buildings[204] and not c.q.buildings[201] and encode(record(c))==before)
assert(shared.ClaimProjects.status=='已就绪' and shared.ClaimProjects.views['0:'..c:GetID()].stage=='AVAILABLE')
print('B125 LOCAL_SIMULATION_PASS: explicit city-state, reject free/unknown/human, panel sync without load notification, no persistent writes, concise pending report')
"""
s=s.replace('exec(compile(header+helpers+cases+', 'cases+=extra\nexec(compile(header+helpers+cases+')
exec(compile(s,str(R/'DevelopmentTests/test_b124_claim.py'),'exec'))

game=(R/'Mod/Gameplay.lua').read_text()
assert game.index('SPCClaimProjects.Start') < game.index('SPCCityIdentityMapping.Start')
assert "params.Action=='CLAIM_SYNC'" in game and 'claim.Sync(playerID,params.CityID)' in game
print('B125 STATIC_CONFIRMED: formal startup before optional experiments; sync dispatch wired')
