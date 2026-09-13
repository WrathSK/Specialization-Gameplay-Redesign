from pathlib import Path
from lupa import LuaRuntime
p=Path(__file__).resolve().parent;l=LuaRuntime(unpack_returned_tuples=True)
for n,f in [('Life','EligibilityLifecycle.lua'),('State','CitySpecializationState.lua'),('Planner','CityFactWritePlan.lua'),('Gate','CityOperationGate.lua')]:l.globals()[n]=l.execute((p/f).read_text())
l.execute('''
local function scenario(mode)
 local id={contextSource="MOCK_ONLY",owner=0,present=true,cityUID="city1",freshFoundationObserved=true}
 local facts=nil;local writes=0;local reads=0;local g;local readError=false
 local life=Life.New(function() return {contextSource="GAMEPLAY_CANDIDATE",status="COMPLETE_ROSTER",
 current={[0]=true},enabled={0},disabled={},unknown={}} end,"MOCK_ONLY")
 life.Refresh("AFTER_LOAD_CLOSE")
 local function resolve() reads=reads+1;if readError then error("READ_ERROR") end;return {id=id,facts=facts} end
 g=Gate.New(life,Planner.New(State),resolve,"MOCK_ONLY")
 local ctx={contextSource="MOCK_ONLY",phase="AFTER_LOAD_CLOSE"}
 local a=g.Prepare("FOUNDATION",0,7,ctx);assert(a.status=="PLAN_ONLY")
 if mode=="stale" then facts={newer=true} end
 if mode=="pre_revoke" then life.Invalidate() end
 local outcome=g.CommitMock(a.handle,function(pid,ref,value)
  writes=writes+1;assert(pid==0 and ref==7)
  if mode=="before" then error("BEFORE_MUTATION") end
  if mode=="drop" then return end
  facts=value
  if mode=="after" then error("AFTER_MUTATION") end
  if mode=="readfail" then readError=true end
  if mode=="owner" then id.owner=1 end
  if mode=="revoke" then life.Invalidate() end
  if mode=="conflict" then facts={another_writer=true} end
  if mode=="reenter" then
   local r=g.Prepare("FOUNDATION",0,7,ctx);assert(r.status=="UNKNOWN")
  end
 end)
 local counts=writes
 assert(g.CommitMock(a.handle,function() writes=writes+1 end).status=="REJECTED_BEFORE_WRITE")
 assert(writes==counts)
 if mode=="ok" or mode=="after" then
  assert(outcome.status=="COMMITTED_MOCK" and facts.cityUID=="city1" and writes==1)
  assert(outcome.writerReturned==(mode=="ok"))
 elseif mode=="stale" or mode=="pre_revoke" then
  assert(outcome.status=="REJECTED_BEFORE_WRITE" and writes==0)
 elseif mode=="before" or mode=="drop" then
  assert(outcome.status=="OLD_VALUE_OBSERVED_HALTED" and facts==nil and writes==1)
 elseif mode=="revoke" or mode=="reenter" then
  assert(outcome.status=="TARGET_OBSERVED_HALTED" and facts.cityUID=="city1")
 elseif mode=="conflict" then
  assert(outcome.status=="CONFLICT_OBSERVED_HALTED" and facts.another_writer)
 else assert(outcome.status=="WRITE_OUTCOME_UNKNOWN_HALTED") end
 if mode~="ok" and mode~="after" and mode~="stale" and mode~="pre_revoke" then
  readError=false;id.owner=0;life.Refresh("AFTER_LOAD_CLOSE")
  assert(g.Prepare("FOUNDATION",0,7,ctx).status=="UNKNOWN") -- no silent resume or retry
 end
end
for _,mode in ipairs({"ok","after","before","drop","readfail","owner","revoke","reenter","conflict","stale","pre_revoke"}) do scenario(mode) end
''')
print('LOCAL_SIMULATION_PASS: 11 commit/readback scenarios; exactly one mock write; write-then-throw recognized; unchanged/conflicting/unreadable values halt; owner/permission/reentrancy; stale precheck; no retries/rollback/resume. No Civ VI setter.')
