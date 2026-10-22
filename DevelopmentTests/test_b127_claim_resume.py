"""B127 actual saved timer sync, including a missed native load hook; inherited Claim rules."""
from pathlib import Path
R=Path(__file__).resolve().parents[1]
s=(R/'DevelopmentTests/test_b124_claim.py').read_text()
extra=r"""
-- Saved due timer, fresh Claim module misses LoadScreenClose: UI sync alone resumes.
start();local c=conquered(1,'DISTRICT_CAMPUS');request(c,'RESEARCH');Events.PlayerTurnDeactivated.Fire(0)
turn=turn+1
local priorAdd=Events.LoadScreenClose.Add;Events.LoadScreenClose.Add=function()end
local reg=shared.CityProgressionStore.RegisterExit;shared.CityProgressionStore.RegisterExit=function()end
SPCClaimProjects.Start(P,shared);shared.CityProgressionStore.RegisterExit=reg;Events.LoadScreenClose.Add=priorAdd
local f=finishCalls;shared.ClaimProjects.Sync(0,c:GetID());assert(record(c).claim and finishCalls==f+1)
local snapshot=encode(record(c));shared.ClaimProjects.Sync(0,c:GetID());Events.PlayerTurnActivated.Fire(0);flush()
assert(encode(record(c))==snapshot and finishCalls==f+1)
-- Same turn sync must retain saved start and perform no permanent write.
start();c=conquered(1,'DISTRICT_CAMPUS');request(c,'RESEARCH');snapshot=encode(record(c));local w=writes;f=finishCalls
shared.ClaimProjects.Sync(0,c:GetID());assert(encode(record(c))==snapshot and writes==w and finishCalls==f)
-- An incomplete end-turn boundary must never be completed by sync.
turn=turn+1;shared.ClaimProjects.Sync(0,c:GetID());assert(not record(c).claim and record(c).claimTimer.stage=='STOPPED' and finishCalls==f)
print('B127 LOCAL_SIMULATION_PASS: saved due timer resumed without production panel, duplicate safe; same-turn no-write; missing full-turn proof stops')
"""
s=s.replace('exec(compile(header+helpers+cases+', 'cases+=extra\nexec(compile(header+helpers+cases+')
exec(compile(s,str(R/'DevelopmentTests/test_b124_claim.py'),'exec'))
