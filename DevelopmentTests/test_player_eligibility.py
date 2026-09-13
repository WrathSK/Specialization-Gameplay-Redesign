"""D0007 offline eligibility, dormancy and acquisition; no Civ VI writes."""
from pathlib import Path
import json
from lupa import LuaRuntime
p=Path(__file__).resolve().parent
def vm():
    l=LuaRuntime(unpack_returned_tuples=True)
    for name,file in [('State','CitySpecializationState.lua'),('Eligibility','PlayerEligibility.lua'),('Journal','CityCompletionJournal.lua'),('Planner','CityFactWritePlan.lua')]:
        l.globals()[name]=l.execute((p/file).read_text())
    return l
l=vm()
l.execute('''
snapshot={contextSource="MOCK_ONLY",status="COMPLETE",players={
 [0]={enabled=true,isHuman=true},[1]={enabled=false},[2]={enabled=true,isHuman=false},[3]={}}}
function identity(owner)
 return {contextSource="MOCK_ONLY",owner=owner,cityUID="same-city",present=true,
  freshFoundationObserved=true,isTestCivilization=false,eligibility=Eligibility.Resolve(snapshot,owner)}
end
local function batch(owner)
 return {status="COMPLETE_ORDERED_BATCH",orderBasis="ENGINE_DELIVERY",cityUID="same-city",owner=owner,
 eventID="first",districts={{family="CAMPUS",complete=true,districtUID="campus",mappingStatus="VALIDATED_FAMILY"}}}
end
local function specialized(owner)
 local id=identity(owner)
 local r=State.NewCity(id);assert(r.status=="READY",r.reason)
 return State.Complete(r.facts,id,batch(owner)).facts
end
local human,ai=specialized(0),specialized(2)
assert(human.specialization==ai.specialization and human.potential==ai.potential)
local id=identity(0)
local f=human
for i=1,3 do
 f=State.CommitInvestment(f,id,{contextSource="MOCK_ONLY",status="COMMITTED",owner=0,cityUID=id.cityUID,
 unitType="SETTLER",unitConsumed=true,id="receipt"..i,unitUID="settler"..i,expectedRevision=f.revision}).facts
end
f.ownedTemplates={LIBRARY=true}
local function transfer(f,from,to)
 return State.TransferOwnership(f,identity(from),identity(to),{contextSource="MOCK_ONLY",
 status="VERIFIED_SAME_CITY",cityUID="same-city",fromOwner=from,toOwner=to,expectedRevision=f.revision})
end
-- Enabled -> disabled: permanent facts survive, absolutely no active Lv1.
local dormant=transfer(f,0,1);assert(dormant.status=="READY")
local d=dormant.facts;local off=identity(1)
assert(d.potential==4 and d.investments.receipt3=="settler3" and d.ownedTemplates.LIBRARY)
assert(State.Restore(d,off).status=="READY")
local poison=setmetatable({},{__index=function() error("SHOULD_NOT_READ_INACTIVE_DATA") end})
local inactive=State.Derive(poison,off,poison)
assert(inactive.status=="DORMANT" and inactive.active==0 and not inactive.effectsEnabled)
assert(State.NewCity(off).status=="DORMANT")
assert(State.Complete(d,off,batch(1)).status=="DORMANT")
assert(State.PlanInvestment(d,off,poison).status=="DORMANT")
assert(State.CommitInvestment(d,off,poison).status=="DORMANT")
-- Unknown qualification must not read state, infer enablement, or erase facts.
local unknown=identity(3)
assert(State.Derive(poison,unknown,poison).status=="UNKNOWN")
assert(State.NewCity(unknown).status=="UNKNOWN")
off.eligibility.player=0;assert(State.Participation(off).status=="UNKNOWN");off=identity(1)
-- Dormant -> enabled AI and enabled -> enabled, with new owner's governor facts.
local resumed=transfer(d,1,2);assert(resumed.status=="READY")
local gov={owner=2,cityUID="same-city",governorGateStatus="KNOWN",governorLevelCeiling=1}
assert(State.Derive(resumed.facts,identity(2),gov).active==1)
assert(resumed.facts.potential==4 and resumed.facts.ownedTemplates.LIBRARY)
assert(transfer(f,0,2).facts.potential==4)
assert(f.owner==0 and d.owner==1) -- neither source table was edited
-- Never-enabled/no-facts acquisition needs explicit provenance, not a missing property.
local proof={contextSource="MOCK_ONLY",status="VERIFIED_NEVER_ENABLED_NO_FACTS",
 cityUID="same-city",fromOwner=1,toOwner=2}
local acquired=identity(2);acquired.freshFoundationObserved=false
assert(State.AcquireUnassigned(nil,acquired,{}).status=="UNKNOWN")
assert(State.Restore(nil,acquired).reason=="OLD_SAVE_COMPATIBILITY_REQUIRED")
local a=State.AcquireUnassigned(nil,acquired,proof)
assert(a.status=="UNKNOWN" and a.reason=="D0010_CONQUEST_INITIALIZER_REQUIRED")
assert(State.AcquireUnassigned(resumed.facts,acquired,proof).status=="UNKNOWN")
-- D0010 snapshot-mode cases live in test_conquest_initialization.py.
-- No acquired schema-v1 facts may bypass Legacy Claim by invoking Complete.
proof.toOwner=1;assert(State.AcquireUnassigned(nil,identity(1),proof).status=="DORMANT")
-- High-level plans cannot bypass eligibility with a replay or gap.
local j=Journal.New(State);local planner=Planner.New(State)
local evidence={contextSource="MOCK_ONLY",phase="AFTER_LOAD_CLOSE",foundationObserved=true,
 bindingValidated=true,listenerReady=true,scanStatus="COMPLETE",completedV01Count=0}
local envelope=j.Foundation(nil,id,evidence).proposed
snapshot.players[0].enabled=false;local off0=identity(0)
assert(j.Foundation(envelope,off0,evidence).status=="DORMANT")
assert(j.Complete(envelope,off0,poison).status=="DORMANT")
assert(j.Gap(envelope,off0,"test").status=="DORMANT")
assert(j.Restore(envelope,off0).status=="READY")
assert(planner.Plan("FOUNDATION",f,off0,{contextSource="MOCK_ONLY",phase="AFTER_LOAD_CLOSE"}).status=="DORMANT")
snapshot.players[0].enabled=true
-- No city/governor/network callback for disabled or unknown players.
local seen={};local r=Eligibility.Dispatch(snapshot,function(p,e)
 assert(p==0 or p==2);assert(e.status=="ENABLED");seen[#seen+1]=p
end)
assert(r.visited==2 and seen[1]==0 and seen[2]==2)
snapshot.status="PARTIAL"
assert(Eligibility.Dispatch(snapshot,function() error("NO_PARTIAL_DISPATCH") end).visited==0)
assert(Eligibility.Resolve(snapshot,0).status=="UNKNOWN")
snapshot.status="COMPLETE";snapshot.players[2].enabled=false
assert(Eligibility.Dispatch(snapshot,function(p) assert(p==0) end).visited==1)
assert(Eligibility.Resolve(snapshot,99).status=="UNKNOWN")
saved=d
''')
def plain(t):
    return {k:plain(v) if hasattr(v,'items') else v for k,v in t.items()}
serialized=json.dumps(plain(l.globals().saved),sort_keys=True)
n=vm()
def table(d):
    return n.table_from({k:table(v) if isinstance(v,dict) else v for k,v in d.items()})
n.globals().saved=table(json.loads(serialized))
n.execute('''
local id={contextSource="MOCK_ONLY",owner=1,cityUID="same-city",present=true,
 eligibility={contextSource="MOCK_ONLY",player=1,status="DISABLED"}}
assert(State.Restore(saved,id).facts.potential==4)
assert(State.Derive(saved,id,nil).status=="DORMANT")
id.eligibility.status="ENABLED"
local gov={owner=1,cityUID="same-city",governorGateStatus="KNOWN",governorLevelCeiling=2}
assert(State.Derive(saved,id,gov).active==2 and saved.potential==4)
assert(saved.ownedTemplates.LIBRARY and saved.investments.receipt3=="settler3")
''')
print('LOCAL_SIMULATION_PASS: enabled human/AI equivalence; disabled/unknown short-circuit; existing-identity transfers and D0010 rejection of legacy unassigned acquisition; no inferred history; replay gates; participant dispatch; JSON/new-VM dormancy and resumption. MOCK_ONLY, no engine carrier/UID proof.')
