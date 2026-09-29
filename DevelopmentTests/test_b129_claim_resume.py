"""Current actual-handler return and saved timer checks, plus sync receipt."""
from pathlib import Path
R=Path(__file__).resolve().parents[1]
for name in ['test_b128_unassigned_return.py','test_b127_claim_resume.py']:
 s=(R/'DevelopmentTests'/name).read_text()
 exec(compile(s,str(R/'DevelopmentTests'/name),'exec'))
# Reuse actual Claim fixture with a received token, not UI-owned timer fabrication.
s=(R/'DevelopmentTests/test_b124_claim.py').read_text()
extra=r"""
start();local c=conquered(1,'DISTRICT_COMMERCIAL_HUB');request(c,'COMMERCE');saved=true;boot()
local before=encode(record(c));shared.ClaimProjects.Sync(0,c:GetID(),'coldload-1')
assert(shared.ClaimProjects.syncAck['0:'..c:GetID()]=='coldload-1' and encode(record(c))==before)
shared.ClaimProjects.Sync(0,c:GetID(),'coldload-2');assert(encode(record(c))==before)
Events.PlayerTurnDeactivated.Fire(0);turn=turn+1;Events.PlayerTurnActivated.Fire(0);flush()
assert(record(c).claim and record(c).base.specialization=='COMMERCE')
local f=finishCalls;shared.ClaimProjects.Sync(0,c:GetID(),'after');assert(finishCalls==f)
print('B129 LOCAL_SIMULATION_PASS saved Commerce timer/ack, duplicate no-write/no-repeat')
"""
s=s.replace('exec(compile(header+helpers+cases+', 'cases+=extra\nexec(compile(header+helpers+cases+')
exec(compile(s,str(R/'DevelopmentTests/test_b124_claim.py'),'exec'))
