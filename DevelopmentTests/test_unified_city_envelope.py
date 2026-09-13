"""Exercise the actual Gate + recovery + single-cell adapter, including JSON/new VM."""
from pathlib import Path
import json
from lupa import LuaRuntime
P = Path(__file__).resolve().parent
SETUP = '''
ctx={contextSource="MOCK_ONLY",phase="AFTER_LOAD_CLOSE"}; writes=0; snapshots={}; mode="ok"; faultAt=0
fresh=true; owner=0; uid="c1"
function identity() return {contextSource="MOCK_ONLY",present=true,owner=owner,cityUID=uid,freshFoundationObserved=fresh} end
function clone(x) if type(x)~="table" then return x end;local t={};for k,v in pairs(x) do t[k]=clone(v) end;return t end
store={read=function() if readFailure then return {status="UNKNOWN"} end;return {status="READ_OK",value=clone(cell)} end,
 write=function(x)
  writes=writes+1
  if writes==faultAt and mode=="drop" then return end
  cell=clone(x);snapshots[writes]=clone(cell)
  if writes==faultAt and mode=="throw_after" then error("AFTER_WRITE") end
 end}
adapter=Envelope.New(store,Recovery,identity,"MOCK_ONLY")
life=Life.New(function() return {contextSource="GAMEPLAY_CANDIDATE",status="COMPLETE_ROSTER",current={[0]=true},enabled={0},disabled={},unknown={}} end,"MOCK_ONLY")
life.Refresh("AFTER_LOAD_CLOSE")
g=Gate.New(life,Planner.New(State),adapter.Resolve,"MOCK_ONLY",{model=Recovery,read=adapter.ReadRecord,write=adapter.WriteRecord})
function commitFoundation()
 local p=g.Prepare("FOUNDATION",0,"c1",ctx);assert(p.status=="PLAN_ONLY")
 return g.CommitRecordedMock(p.handle,"op1",adapter.WriteFacts)
end
'''

def vm():
    l = LuaRuntime(unpack_returned_tuples=True)
    for name, filename in [('Life','EligibilityLifecycle.lua'), ('State','CitySpecializationState.lua'), ('Planner','CityFactWritePlan.lua'), ('Gate','CityOperationGate.lua'), ('Recovery','PendingCityRecovery.lua'), ('Envelope','UnifiedCityEnvelope.lua')]:
        l.globals()[name] = l.execute((P/filename).read_text())
    l.execute(SETUP)
    return l

def plain(x):
    return {k:plain(v) for k,v in x.items()} if hasattr(x,'items') else x

def reload_cell(value):
    l=vm()
    def table(x):
        return l.table_from({k:table(v) for k,v in x.items()}) if isinstance(x,dict) else x
    l.globals().cell=table(json.loads(json.dumps(plain(value))))
    l.execute('fresh=false')
    return l

l=vm()
l.execute('''
assert(commitFoundation().status=="TARGET_OBSERVED_PENDING" and writes==2)
assert(g.ResolveRecordedMock("c1",ctx).status=="DONE_CONFIRMED_MOCK" and writes==3)
assert(g.Prepare("FOUNDATION",0,"c1",ctx).status=="READY" and writes==3)
local batch={status="COMPLETE_ORDERED_BATCH",orderBasis="ENGINE_DELIVERY",owner=0,cityUID="c1",eventID="first",
 districts={{family="CAMPUS",complete=true,districtUID="d1",mappingStatus="VALIDATED_FAMILY"}}}
local p=g.Prepare("COMPLETION_BATCH",0,"c1",ctx,batch);assert(p.status=="PLAN_ONLY")
assert(g.CommitRecordedMock(p.handle,"op2",adapter.WriteFacts).status=="TARGET_OBSERVED_PENDING")
assert(g.ResolveRecordedMock("c1",ctx).status=="DONE_CONFIRMED_MOCK")
assert(writes==6 and cell.storageRevision==6 and cell.facts.specialization=="RESEARCH" and cell.record.operationID=="op2")
assert(not pcall(adapter.WriteFacts,0,"c1",cell.facts) and writes==6)
''')
# Every durable checkpoint from two operations becomes a fresh VM with no session state.
for stage in range(1,7):
    n=reload_cell(l.globals().snapshots[stage])
    n.execute('assert(g.Prepare("FOUNDATION",0,"c1",ctx).status=="UNKNOWN" and writes==0)')
    if stage in (1,4):
        n.execute('assert(g.ResolveRecordedMock("c1",ctx).status=="RECOVERY_HELD" and writes==0)')
    else:
        n.execute('assert(g.ResolveRecordedMock("c1",ctx).status=="DONE_CONFIRMED_MOCK")')
        assert n.globals().writes == (1 if stage in (2,5) else 0)
        n.execute('assert(g.Prepare("FOUNDATION",0,"c1",ctx).status=="READY")')
# Dropped writes at each stage stop without reattempt; throwing after a write uses readback.
for mode in ('drop','throw_after'):
    for stage in (1,2,3):
        n=vm();n.globals().mode=mode;n.globals().faultAt=stage
        result=n.eval('commitFoundation()').status
        if mode=='drop' and stage==1:
            assert result=='WRITE_OUTCOME_UNKNOWN_HALTED'
        elif mode=='drop' and stage==2:
            assert result=='OLD_VALUE_OBSERVED_HALTED'
        else:
            assert result=='TARGET_OBSERVED_PENDING'
            result=n.eval('g.ResolveRecordedMock("c1",ctx)').status
            assert result==('RECOVERY_HELD' if mode=='drop' and stage==3 else 'DONE_CONFIRMED_MOCK')
        assert n.globals().writes==(stage if mode=='drop' else 3)
# Corrupt or inconsistent record/facts, owner changes, unknown data and failed read are rejected.
for mutation in ('cell.facts.revision=99','cell.record.target.owner=1',
                 'cell.storageRevision=0','cell.extra="foreign"','owner=1','uid="other"','readFailure=true'):
    n=reload_cell(l.globals().snapshots[6]);n.execute(mutation)
    n.execute('assert(adapter.ReadRecord().status=="UNKNOWN");assert(g.ResolveRecordedMock("c1",ctx).status=="RECOVERY_HELD" and writes==0)')
n=vm();n.execute('fresh=false;assert(adapter.ReadRecord().status=="UNKNOWN");assert(g.Prepare("FOUNDATION",0,"c1",ctx).status=="UNKNOWN" and writes==0)')
# External whole-cell change between transition planning and final check must not be overwritten.
n=reload_cell(l.globals().snapshots[2])
n.execute('''
local done=Recovery.ClosePlan(cell.record,{contextSource="MOCK_ONLY",status="READ_OK",present=true,owner=0,cityUID="c1",facts=cell.facts},"MOCK_ONLY").record
local original=store.read;local reads=0
store.read=function() reads=reads+1;if reads==2 then cell.storageRevision=99 end;return original() end
assert(not pcall(adapter.WriteRecord,done) and writes==0 and cell.storageRevision==99)
''')
print('LOCAL_SIMULATION_PASS: actual gate/recovery/one-cell adapter; 2 sequential operations; 6 JSON/new-VM checkpoints; 6 write faults; invalid state/identity/read rejection; no-op; stale snapshot rejection. Engine persistence not tested.')
