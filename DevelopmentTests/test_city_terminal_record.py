from pathlib import Path
from lupa import LuaRuntime
import json
p=Path(__file__).resolve().parent
def vm():
 l=LuaRuntime(unpack_returned_tuples=True)
 for n,f in [('Life','EligibilityLifecycle.lua'),('State','CitySpecializationState.lua'),('Planner','CityFactWritePlan.lua'),('Gate','CityOperationGate.lua'),('Recovery','PendingCityRecovery.lua')]:l.globals()[n]=l.execute((p/f).read_text())
 return l
l=vm();setup='''
ctx={contextSource="MOCK_ONLY",phase="AFTER_LOAD_CLOSE"}
function create()
 local life=Life.New(function() return {contextSource="GAMEPLAY_CANDIDATE",status="COMPLETE_ROSTER",current={[0]=true},enabled={0},disabled={},unknown={}} end,"MOCK_ONLY")
 life.Refresh("AFTER_LOAD_CLOSE")
 return Gate.New(life,Planner.New(State),function() return {id={contextSource="MOCK_ONLY",present=true,owner=0,cityUID="c1",freshFoundationObserved=true},facts=facts} end,"MOCK_ONLY",{
 model=Recovery,read=function() return {status="READ_OK",record=record} end,
 write=function(r) if mode=="reenter" and r.state=="DONE" then activeGate.Prepare("FOUNDATION",0,7,ctx) end;if mode=="drop_done" and r.state=="DONE" then return end;record=r;if mode=="after_done" and r.state=="DONE" then error("AFTER") end end})
end
''';l.execute(setup)
l.execute('''
mode="ok";local g=create()
local a=g.Prepare("FOUNDATION",0,7,ctx)
assert(g.CommitRecordedMock(a.handle,"op1",function(_,_,f) facts=f end).status=="TARGET_OBSERVED_PENDING")
mode="drop_done";assert(g.ResolveRecordedMock(7,ctx).status=="RECOVERY_HELD" and record.state=="PENDING")
assert(g.Prepare("FOUNDATION",0,7,ctx).status=="UNKNOWN")
mode="reenter";activeGate=g;assert(g.ResolveRecordedMock(7,ctx).status=="RECOVERY_HELD");assert(g.Prepare("FOUNDATION",0,7,ctx).status=="UNKNOWN")
mode="after_done";record.state="PENDING";assert(g.ResolveRecordedMock(7,ctx).status=="DONE_CONFIRMED_MOCK" and record.state=="DONE")
mode="ok"
local batch={status="COMPLETE_ORDERED_BATCH",orderBasis="ENGINE_DELIVERY",owner=0,cityUID="c1",eventID="first",
 districts={{family="CAMPUS",complete=true,districtUID="d1",mappingStatus="VALIDATED_FAMILY"}}}
a=g.Prepare("COMPLETION_BATCH",0,7,ctx,batch);assert(a.status=="PLAN_ONLY")
assert(g.CommitRecordedMock(a.handle,"op2",function(_,_,f) facts=f end).status=="TARGET_OBSERVED_PENDING")
assert(g.ResolveRecordedMock(7,ctx).status=="DONE_CONFIRMED_MOCK" and facts.specialization=="RESEARCH")
assert(record.operationID=="op2" and record.state=="DONE")
local previous=facts;facts={conflict=true};assert(g.ResolveRecordedMock(7,ctx).status=="RECOVERY_HELD")
assert(g.Prepare("FOUNDATION",0,7,ctx).status=="UNKNOWN");facts=previous
assert(g.ResolveRecordedMock(7,ctx).status=="DONE_CONFIRMED_MOCK")
''')
def plain(t):return {k:plain(v) if hasattr(v,'items') else v for k,v in t.items()}
data=json.dumps({k:plain(l.globals()[k]) for k in ['record','facts']})
n=vm();n.execute(setup)
def tab(d):return n.table_from({k:tab(v) if isinstance(v,dict) else v for k,v in d.items()})
for k,v in json.loads(data).items():n.globals()[k]=tab(v)
n.execute('''local g=create();assert(g.Prepare("FOUNDATION",0,7,ctx).status=="UNKNOWN");assert(g.ResolveRecordedMock(7,ctx).status=="DONE_CONFIRMED_MOCK");assert(g.Prepare("FOUNDATION",0,7,ctx).status=="READY")''')
print('LOCAL_SIMULATION_PASS: explicit DONE save/readback; drop and write-then-throw; two sequential city commits; conflict holds; retained receipt; JSON/new-VM requires reconciliation before next plan. No city writes during resolution.')
