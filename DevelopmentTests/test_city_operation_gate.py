from pathlib import Path
from lupa import LuaRuntime
p=Path(__file__).resolve().parent;l=LuaRuntime(unpack_returned_tuples=True)
for n,f in [('Life','EligibilityLifecycle.lua'),('State','CitySpecializationState.lua'),('Planner','CityFactWritePlan.lua'),('Gate','CityOperationGate.lua')]:l.globals()[n]=l.execute((p/f).read_text())
l.execute('''
local enabled=true;local reads=0;local invalidateOnRead=false
local life=Life.New(function() return {contextSource="GAMEPLAY_CANDIDATE",status="COMPLETE_ROSTER",
 current={[0]=true},enabled=enabled and {0} or {},disabled=enabled and {} or {[0]=true},unknown={}} end,"MOCK_ONLY")
life.Refresh("AFTER_LOAD_CLOSE")
local id={contextSource="MOCK_ONLY",owner=0,present=true,cityUID="city1",freshFoundationObserved=true}
local facts=nil
local g=Gate.New(life,Planner.New(State),function(ref)
 reads=reads+1;assert(ref==7)
 if invalidateOnRead then life.Invalidate() end
 return {id=id,facts=facts}
end,"MOCK_ONLY")
local ctx={contextSource="MOCK_ONLY",phase="AFTER_LOAD_CLOSE"}
local function prep() return g.Prepare("FOUNDATION",0,7,ctx) end
assert(g.Prepare("FOUNDATION",0,7,{contextSource="MOCK_ONLY",phase="INITIALIZE"}).status=="UNKNOWN" and reads==0)
enabled=false;life.Refresh("AFTER_LOAD_CLOSE");assert(prep().status=="UNKNOWN" and reads==0)
enabled=true;life.Refresh("AFTER_LOAD_CLOSE")
local a=prep();assert(a.status=="PLAN_ONLY")
local done=g.CheckForCommit(a.handle);assert(done.status=="CHECKED_PLAN_ONLY" and facts==nil)
assert(g.CheckForCommit(a.handle).status=="UNKNOWN" and g.CheckForCommit({}).status=="UNKNOWN")
a=prep();life.Invalidate();local n=reads;assert(g.CheckForCommit(a.handle).status=="UNKNOWN" and reads==n)
life.Refresh("AFTER_LOAD_CLOSE");a=prep();id.owner=1
assert(g.CheckForCommit(a.handle).status=="UNKNOWN");id.owner=0
a=prep();id.cityUID="reused-city-reference";assert(g.CheckForCommit(a.handle).status=="UNKNOWN");id.cityUID="city1"
a=prep();id.present=false;assert(g.CheckForCommit(a.handle).status=="UNKNOWN");id.present=true
a=prep();facts=done.plan.proposedFacts;assert(g.CheckForCommit(a.handle).status=="UNKNOWN")
-- Compose a real completion plan; concurrent change with unchanged revision must still reject.
local batch={status="COMPLETE_ORDERED_BATCH",orderBasis="ENGINE_DELIVERY",owner=0,cityUID="city1",eventID="e1",
 districts={{family="CAMPUS",complete=true,districtUID="d1",mappingStatus="VALIDATED_FAMILY"}}}
a=g.Prepare("COMPLETION_BATCH",0,7,ctx,batch);assert(a.status=="PLAN_ONLY")
facts.ownedTemplates={CHANGED=true};assert(g.CheckForCommit(a.handle).status=="UNKNOWN")
facts.ownedTemplates=nil
a=g.Prepare("COMPLETION_BATCH",0,7,ctx,batch)
local result=g.CheckForCommit(a.handle)
assert(result.status=="CHECKED_PLAN_ONLY" and result.plan.proposedFacts.specialization=="RESEARCH")
assert(facts.specialization==nil) -- no commit, no caller data mutation
facts=nil;invalidateOnRead=true;assert(prep().status=="UNKNOWN")
''')
print('LOCAL_SIMULATION_PASS: actual city planner + lifecycle; no read before permission; load gate; stale/used/foreign handle; owner/generation/removal; same-revision changed facts; read-time invalidation; first completion proposal; zero commit writes.')
