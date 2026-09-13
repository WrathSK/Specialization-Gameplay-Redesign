from pathlib import Path
from lupa.lua55 import LuaRuntime
p=Path(__file__).resolve().parent
l=LuaRuntime(unpack_returned_tuples=True)
l.globals().C=l.execute((p/'ConvergencePlan.lua').read_text())
l.execute('''
local s={context='MOCK_ONLY',complete=true,player=0,revision=1,cities={
 R={owner=0,specialization='RESEARCH',active=1,totalYields={SCIENCE=2000},localYields={SCIENCE=1700},localBasisVerified=true},
 R4={owner=0,specialization='RESEARCH',active=4,totalYields={SCIENCE=900},localYields={SCIENCE=900},localBasisVerified=true},
 K={owner=0,specialization='CULTURE',active=2,totalYields={CULTURE=555.5},localYields={CULTURE=500},localBasisVerified=true},
 I={owner=0,specialization='INDUSTRY',active=4,totalYields={PRODUCTION=750},localYields={PRODUCTION=600},localBasisVerified=true},
 B={owner=0,specialization='COMMERCE',active=4,totalYields={SCIENCE=999999}},
 D={owner=0,specialization='COMMERCE',active=4,totalYields={SCIENCE=999999}}},
 directSources={B={R=true,R4=true,K=true,I=true},D={B=true}},
 receivedNetworks={D={RESEARCH=true}}}
local function plan(mode) local p=C.Plan(s,mode or 'TOTAL');assert(p.status=='OFFLINE_PROPOSAL',p.reason);return p end
local p=plan();assert(p.cities.B.SCIENCE.amount==400 and p.cities.B.SCIENCE.sources.R)
assert(math.abs(p.cities.B.CULTURE.amount-111.1)<1e-10 and p.cities.B.PRODUCTION.amount==150)
assert(p.cities.D.SCIENCE.amount==0) -- received network and Commerce source cannot relay convergence
assert(plan('LOCAL').cities.B.SCIENCE.amount==340) -- distinguish accepted basis vs conditional total
-- Apply absolute outputs in a mock repeatedly; Commerce totals grow only once.
for i=1,100 do
 local q=plan();s.cities.B.totalYields.SCIENCE=100+q.cities.B.SCIENCE.amount
 assert(q.cities.B.SCIENCE.amount==400 and q.cities.D.SCIENCE.amount==0)
end
s.directSources.B.R=nil;assert(plan().cities.B.SCIENCE.amount==180)
s.directSources.B.R4=nil;assert(plan().cities.B.SCIENCE.amount==0)
s.directSources.B.R=true;s.cities.B.active=3;assert(plan().cities.B==nil)
s.cities.B.active=4;s.cities.R.owner=1;assert(plan().cities.B.SCIENCE.amount==0)
s.cities.R.owner=0;s.cities.R.totalYields.SCIENCE=0/0;assert(C.Plan(s,'TOTAL').status=='UNKNOWN')
s.cities.R.totalYields.SCIENCE=2000;s.cities.R.localBasisVerified=false
assert(C.Plan(s,'LOCAL').status=='UNKNOWN')
-- Even synchronous read-then-write does not eliminate cross-round feedback.
local a,b=100,100
for i=1,10 do a,b=100+0.2*b,100+0.2*a end
assert(a>124 and b>124) -- not the intended single-copy 120
s.extraDependencies={{from='B',to='R'}}
assert(C.Plan(s,'TOTAL').reason:find('YIELD_DEPENDENCY_CYCLE'))
s.extraDependencies=nil;assert(plan().cities.B.SCIENCE.amount==400)
''')
print('LOCAL_SIMULATION_PASS: conditional TOTAL vs LOCAL planner, yield-max not ACTIVE, separate yields, fractional values retained, no Commerce/received-only relay, absolute repeated refresh, source loss/owner/ACTIVE changes, invalid inputs, cycle counterexample and conservative graph rejection. No native API proof.')
