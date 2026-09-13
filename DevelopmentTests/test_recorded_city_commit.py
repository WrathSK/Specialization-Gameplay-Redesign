from pathlib import Path
from lupa import LuaRuntime
import json
p=Path(__file__).resolve().parent
def vm():
 l=LuaRuntime(unpack_returned_tuples=True)
 for n,f in [('Life','EligibilityLifecycle.lua'),('State','CitySpecializationState.lua'),('Planner','CityFactWritePlan.lua'),('Gate','CityOperationGate.lua'),('Recovery','PendingCityRecovery.lua')]:l.globals()[n]=l.execute((p/f).read_text())
 return l
l=vm()
setup='''
function fixture(mode,seed)
 local record=seed;local facts=nil;local cityWrites=0;local intentWrites=0;local storeReads=0
 local id={contextSource="MOCK_ONLY",owner=0,present=true,cityUID="c1",freshFoundationObserved=true}
 local life=Life.New(function() return {contextSource="GAMEPLAY_CANDIDATE",status="COMPLETE_ROSTER",current={[0]=true},enabled={0},disabled={},unknown={}} end,"MOCK_ONLY")
 life.Refresh("AFTER_LOAD_CLOSE")
 local store={model=Recovery,read=function()
  storeReads=storeReads+1
  if mode=="unreadable" or (mode=="readback_fail" and intentWrites>0) then error("READ_FAIL") end
  return {status="READ_OK",record=record}
 end,write=function(r)
  intentWrites=intentWrites+1
  if mode=="intent_drop" then return end
  record=r
  if mode=="intent_after" then error("WRITTEN_THEN_ERROR") end
  if mode=="revoke" then life.Invalidate() end
  if mode=="city_changed" then facts={other=true} end
  if mode=="intent_conflict" then record={someoneElse=true} end
 end}
 local g=Gate.New(life,Planner.New(State),function() return {id=id,facts=facts} end,"MOCK_ONLY",store)
 local plan=g.Prepare("FOUNDATION",0,7,{contextSource="MOCK_ONLY",phase="AFTER_LOAD_CLOSE"})
 local result
 if plan.status=="PLAN_ONLY" then
  assert(g.CommitMock(plan.handle,function() error("BYPASS") end).status=="REJECTED_BEFORE_WRITE")
  result=g.CommitRecordedMock(plan.handle,"op1",function(_,_,target)
   cityWrites=cityWrites+1;assert(record and record.state=="PENDING")
   if mode=="city_before" then error("NO_CITY_WRITE") end
   facts=target
   if mode=="city_after" then error("CITY_WRITTEN_THEN_ERROR") end
  end)
  assert(g.CommitRecordedMock(plan.handle,"op1",function() cityWrites=cityWrites+1 end).status=="REJECTED_BEFORE_WRITE")
 else result=plan end
 return result,record,facts,cityWrites,intentWrites,storeReads
end
'''
l.execute(setup)
l.execute('''
for _,mode in ipairs({"ok","intent_after","city_after"}) do
 local r,j,f,c,i=fixture(mode)
 assert(r.status=="TARGET_OBSERVED_PENDING" and c==1 and i==1 and j.state=="PENDING" and f.cityUID=="c1")
 saved=j
end
for _,mode in ipairs({"intent_drop","readback_fail","revoke","city_changed","intent_conflict"}) do
 local r,j,f,c,i=fixture(mode);assert(c==0 and i==1 and r.status=="WRITE_OUTCOME_UNKNOWN_HALTED")
end
local r,j,f,c,i=fixture("city_before");assert(c==1 and i==1 and f==nil and j.state=="PENDING" and r.status=="OLD_VALUE_OBSERVED_HALTED")
r,j,f,c,i=fixture("unreadable");assert(c==0 and i==0 and r.status=="UNKNOWN")
r,j,f,c,i=fixture("ok",{corrupt=true});assert(c==0 and i==0 and r.status=="UNKNOWN")
''')
def plain(t):return {k:plain(v) if hasattr(v,'items') else v for k,v in t.items()}
data=json.dumps(plain(l.globals().saved))
n=vm();n.execute(setup)
def table(x):return n.table_from({k:table(v) if isinstance(v,dict) else v for k,v in x.items()})
n.globals().seed=table(json.loads(data))
n.execute('''local r,j,f,c,i=fixture("ok",seed);assert(r.status=="UNKNOWN" and c==0 and i==0 and j.operationID=="op1")''')
print('LOCAL_SIMULATION_PASS: intent saved/readback before city write; store error/drop/conflict; revalidation after intent; write-then-error; no unrecorded bypass; pending/corrupt/unreadable startup blocks; JSON/new-VM retained pending blocks; no real persistence guarantee.')
