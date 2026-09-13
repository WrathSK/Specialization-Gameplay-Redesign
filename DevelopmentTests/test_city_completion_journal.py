"""D0004 offline qualification / ordered facts envelope. No Civ VI writes."""
from pathlib import Path
import json
from lupa import LuaRuntime
p=Path(__file__).resolve().parent

def vm():
    l=LuaRuntime(unpack_returned_tuples=True)
    l.globals().State=l.execute((p/'CitySpecializationState.lua').read_text())
    l.globals().Module=l.execute((p/'CityCompletionJournal.lua').read_text())
    l.execute('J=Module.New(State)')
    return l
l=vm()
l.execute('''
id={contextSource="MOCK_ONLY",eligibility={contextSource="MOCK_ONLY",player=0,status="ENABLED"},isTestCivilization=true,present=true,owner=0,cityUID="fixture-city-1",freshFoundationObserved=true}
evidence={contextSource="MOCK_ONLY",phase="AFTER_LOAD_CLOSE",foundationObserved=true,bindingValidated=true,
 listenerReady=true,scanStatus="COMPLETE",completedV01Count=0}
local function event(seq,family)
 return {contextSource="MOCK_ONLY",phase="AFTER_LOAD_CLOSE",owner=0,cityUID=id.cityUID,sequence=seq,
 eventID="delivery-"..seq,districtUID="district-"..seq,family=family,complete=true,mappingStatus="VALIDATED_FAMILY"}
end
for key,bad in pairs({listenerReady=false,bindingValidated=false,foundationObserved=false,
 scanStatus="PARTIAL",completedV01Count=1,phase="BEFORE_LOAD_CLOSE",contextSource="GAMEPLAY"}) do
 local old=evidence[key];evidence[key]=bad;assert(J.Foundation(nil,id,evidence).status=="UNKNOWN");evidence[key]=old
end
local init=J.Foundation(nil,id,evidence);assert(init.status=="PLAN_ONLY" and init.expectedAbsent)
local saved=nil;local writes=0
-- This commit is a fixture, not engine atomicity. Stale plans must be rejected.
local function commit(plan)
 if plan.status~="PLAN_ONLY" then return false end
 if plan.expectedAbsent then if saved then return false end
 elseif not saved or saved.revision~=plan.expectedRevision then return false end
 saved=plan.proposed;writes=writes+1;return true
end
assert(commit(init) and not commit(init))
local e1=event(1,"CAMPUS");local pending=J.Complete(saved,id,e1)
assert(saved.facts.specialization==nil and pending.proposed.facts.specialization=="RESEARCH")
assert(commit(pending) and not commit(pending))
assert(J.Complete(saved,id,e1).changed==false)
local e2=event(2,"THEATER_SQUARE");assert(commit(J.Complete(saved,id,e2)))
assert(saved.facts.specialization=="RESEARCH" and saved.facts.potential==1)
local opposite=init.proposed
opposite=J.Complete(opposite,id,event(1,"THEATER_SQUARE")).proposed
opposite=J.Complete(opposite,id,event(2,"CAMPUS")).proposed
assert(opposite.facts.specialization=="CULTURE")
assert(J.Complete(saved,id,e1).status=="UNKNOWN")
local conflict=event(2,"CAMPUS");assert(J.Complete(saved,id,conflict).status=="UNKNOWN")
assert(J.Complete(saved,id,event(4,"CAMPUS")).status=="UNKNOWN")
local loading=event(3,"CAMPUS");loading.phase="BEFORE_LOAD_CLOSE"
assert(J.Complete(saved,id,loading).status=="UNKNOWN")
assert(J.Foundation(saved,id,evidence).envelope.facts.specialization=="RESEARCH")
local dev={schema=1,kind="FIRST_OBSERVED_COMPLETION",observedFamily="RESEARCH"}
assert(J.Restore(dev,id).status=="UNKNOWN" and J.Foundation(dev,id,evidence).status=="UNKNOWN")
-- A failed earlier completion must quarantine history, not choose the next successful type.
local fresh=init.proposed
local failed=J.Complete(fresh,id,event(1,"THEATER_SQUARE"));assert(failed.status=="PLAN_ONLY")
-- Simulated failed write: do not commit failed; persist GAP separately if possible.
local gap=J.Gap(fresh,id,"WRITE_UNCONFIRMED");assert(gap.status=="PLAN_ONLY")
quarantined=gap.proposed
assert(quarantined.facts.specialization==nil)
assert(J.Complete(quarantined,id,event(1,"CAMPUS")).reason=="PERSISTENT_HISTORY_GAP")
assert(J.Foundation(quarantined,id,evidence).envelope.health=="GAP")
assert(J.Gap(quarantined,id,"another").changed==false)
assert(J.Restore(quarantined,id).envelope.health=="GAP")
local restored=J.Restore(saved,id).envelope;restored.facts.specialization="CULTURE"
assert(saved.facts.specialization=="RESEARCH")
id.owner=1;assert(J.Restore(saved,id).status=="UNKNOWN");id.owner=0
id.cityUID="reused-generation";assert(J.Restore(saved,id).status=="UNKNOWN");id.cityUID="fixture-city-1"
assert(writes==3);persisted=saved
''')
def plain(v):
    return {k:plain(x) for k,x in v.items()} if hasattr(v,'items') else v
wire=json.loads(json.dumps({k:plain(l.globals()[k]) for k in ['id','persisted','quarantined']}))
fresh=vm()
def tab(v):
    return fresh.table_from({k:tab(x) for k,x in v.items()}) if isinstance(v,dict) else v
for k,v in wire.items(): fresh.globals()[k]=tab(v)
fresh.execute('''
assert(J.Restore(persisted,id).envelope.facts.specialization=="RESEARCH")
assert(J.Restore(persisted,id).envelope.facts.potential==1)
assert(J.Restore(quarantined,id).envelope.health=="GAP")
''')
print('LOCAL_SIMULATION_PASS: qualified foundation; delivery order both directions; stale/duplicate/conflict; no DEV migration; persistent GAP; single-envelope plans; new VM restore. Engine writer/continuous coverage NOT proven.')
