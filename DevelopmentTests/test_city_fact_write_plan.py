"""Offline B011 lifecycle replay. No engine storage or native batch authority."""
from pathlib import Path
from lupa import LuaRuntime
p = Path(__file__).resolve().parent
lua = LuaRuntime(unpack_returned_tuples=True)
lua.globals().State = lua.execute((p / 'CitySpecializationState.lua').read_text())
lua.globals().Planner = lua.execute((p / 'CityFactWritePlan.lua').read_text())
lua.execute('''
local plan=Planner.New(State)
local id={contextSource="MOCK_ONLY",eligibility={contextSource="MOCK_ONLY",player=0,status="ENABLED"},isTestCivilization=true,present=true,
 owner=0,cityUID="fixture-generation-1",freshFoundationObserved=true}
local live={contextSource="MOCK_ONLY",phase="AFTER_LOAD_CLOSE"}
local load={contextSource="MOCK_ONLY",phase="BEFORE_LOAD_CLOSE"}
local stored=nil
local writes=0
-- Deliberately a fixture store, not an assertion of engine atomicity.
local function commit(p)
 if p.status~="PLAN_ONLY" then return false end
 if p.expectedAbsent then if stored~=nil then return false end
 elseif not stored or stored.cityUID~=p.cityUID or stored.owner~=p.owner
  or stored.revision~=p.expectedRevision then return false end
 stored=p.proposedFacts;writes=writes+1;return true
end
local function batch(family)
 return {status="COMPLETE_ORDERED_BATCH",orderBasis="ENGINE_DELIVERY",owner=0,cityUID=id.cityUID,eventID="fixture-event",
 districts={{family=family,districtUID="fixture-district-1",complete=true,mappingStatus="VALIDATED_FAMILY"}}}
end
-- Raw events never become fact-writing commands, including the pre-CityBuilt center.
for _,action in ipairs({"DistrictAddedToMap","OnDistrictConstructed"}) do
 assert(plan.Plan(action,nil,id,live,batch("NON_V01")).status=="IGNORED")
end
assert(writes==0)
assert(plan.Plan("FOUNDATION",nil,id,load).status=="UNKNOWN")
local init=plan.Plan("FOUNDATION",nil,id,live)
assert(init.status=="PLAN_ONLY" and stored==nil and init.expectedAbsent)
assert(commit(init) and not commit(init) and writes==1)
assert(plan.Plan("FOUNDATION",stored,id,live).status=="READY")
assert(not commit(plan.Plan("COMPLETION_BATCH",stored,id,live,batch("NON_V01"))))
assert(not commit(plan.Plan("DistrictAddedToMap",stored,id,live,batch("CAMPUS"))))
assert(not commit(plan.Plan("COMPLETION_BATCH",stored,id,load,batch("CAMPUS"))))
local campus=plan.Plan("COMPLETION_BATCH",stored,id,live,batch("CAMPUS"))
assert(stored.specialization==nil and campus.proposedFacts.specialization=="RESEARCH")
assert(commit(campus) and not commit(campus) and writes==2)
assert(not commit(plan.Plan("COMPLETION_BATCH",stored,id,live,batch("CAMPUS"))))
-- A later foundation replay cannot reset a real (fixture) investment.
local investment=State.CommitInvestment(stored,id,{contextSource="MOCK_ONLY",status="COMMITTED",
 id="receipt",unitUID="unit-generation",unitType="SETTLER",unitConsumed=true,
 cityUID=id.cityUID,owner=0,expectedRevision=stored.revision})
assert(investment.status=="READY");stored=investment.facts
local again=plan.Plan("FOUNDATION",stored,id,live)
assert(again.status=="READY" and again.facts.potential==2 and again.facts.investments.receipt)
local restored=plan.Plan("RESTORE",stored,id,load)
assert(restored.status=="READY" and restored.facts.potential==2)
restored.facts.investments.receipt="mutated-copy"
assert(stored.investments.receipt=="unit-generation")
assert(plan.Plan("RESTORE",nil,id,load).status=="UNKNOWN")
assert(plan.Plan("COMPLETION_BATCH",nil,id,live,batch("CAMPUS")).status=="UNKNOWN")
assert(plan.Plan("FOUNDATION",stored,id,{contextSource="GAMEPLAY",phase="AFTER_LOAD_CLOSE"}).status=="UNKNOWN")
id.owner=1;assert(plan.Plan("FOUNDATION",stored,id,live).status=="UNKNOWN");id.owner=0
id.cityUID="reused-city-new-generation";assert(plan.Plan("FOUNDATION",stored,id,live).status=="UNKNOWN");id.cityUID="fixture-generation-1"
id.freshFoundationObserved=false;assert(plan.Plan("FOUNDATION",nil,id,live).status=="UNKNOWN");id.freshFoundationObserved=true
id.eligibility.status="DISABLED";assert(plan.Plan("FOUNDATION",nil,id,live).status=="DORMANT");id.eligibility.status="ENABLED"
local corrupt={schemaVersion=99};assert(plan.Plan("FOUNDATION",corrupt,id,live).status=="UNKNOWN")
local multiple=batch("CAMPUS")
multiple.districts[2]={family="THEATER_SQUARE",districtUID="other",complete=true,mappingStatus="VALIDATED_FAMILY"}
assert(plan.Plan("COMPLETION_BATCH",State.NewCity(id).facts,id,live,multiple).proposedFacts.specialization=="RESEARCH")
assert(writes==2)
''')
print('LOCAL_SIMULATION_PASS: B011 sequence; no raw-event authority; duplicate foundation preserves investment; load isolation; fixture stale-write rejection; unresolved lifecycle refuses writes. No engine writes.')
