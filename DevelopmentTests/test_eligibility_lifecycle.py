from pathlib import Path
from lupa import LuaRuntime
p=Path(__file__).resolve().parent
l=LuaRuntime(unpack_returned_tuples=True)
l.globals().Life=l.execute((p/'EligibilityLifecycle.lua').read_text())
l.globals().Roster=l.execute((p/'CurrentPlayerRoster.lua').read_text())
l.execute('''
local ids={0,1};local states={[0]="ENABLED",[1]="DISABLED"};local mode="ok";local gate
local function collect()
 if mode=="throw" then error("FAIL") end
 if mode=="invalidate" then gate.Invalidate() end
 if mode=="nested" then mode="ok";assert(gate.Refresh("AFTER_LOAD_CLOSE").status=="READY_OFFLINE") end
 return Roster.Collect({PlayerManager={GetAliveIDs=function() return ids end}},function(p)
  return {contextSource="GAMEPLAY_CANDIDATE",player=p,status=states[p] or "UNKNOWN"}
 end)
end
gate=Life.New(collect,"MOCK_ONLY")
assert(not gate.Acquire(0))
assert(gate.Refresh("INITIALIZE").status=="UNKNOWN")
assert(gate.Refresh("AFTER_LOAD_CLOSE").status=="READY_OFFLINE")
local a=gate.Acquire(0);assert(a and gate.Check(a,0) and not gate.Check(a,1))
assert(not gate.Acquire(1) and not gate.Check({},0))
a.epoch=999;a.player=1;assert(gate.Check(a,0)) -- issued identity not taken from token fields
mode="throw";assert(gate.Refresh("AFTER_LOAD_CLOSE").status=="UNKNOWN")
assert(not gate.Check(a,0) and not gate.Acquire(0))
mode="ok";gate.Refresh("AFTER_LOAD_CLOSE");assert(gate.Acquire(0) and not gate.Check(a,0))
local b=gate.Acquire(0);states[0]="UNKNOWN";gate.Refresh("AFTER_LOAD_CLOSE")
assert(not gate.Check(b,0) and not gate.Acquire(0))
states[0]="ENABLED";states[1]="ENABLED";gate.Refresh("AFTER_LOAD_CLOSE")
assert(gate.Acquire(0) and gate.Acquire(1))
local c=gate.Acquire(0);ids={1};gate.Refresh("AFTER_LOAD_CLOSE");assert(not gate.Check(c,0))
ids={0,1};gate.Refresh("AFTER_LOAD_CLOSE");assert(gate.Acquire(0))
mode="invalidate";assert(gate.Refresh("AFTER_LOAD_CLOSE").reason=="SUPERSEDED_REFRESH")
assert(not gate.Acquire(0))
mode="nested";assert(gate.Refresh("AFTER_LOAD_CLOSE").reason=="SUPERSEDED_REFRESH")
assert(gate.Acquire(0)) -- newer refresh kept, outer cannot overwrite
local old=gate.Acquire(0);gate=Life.New(collect,"MOCK_ONLY")
assert(not gate.Check(old,0));mode="ok";gate.Refresh("AFTER_LOAD_CLOSE")
assert(not gate.Check(old,0) and gate.Acquire(0))
local bad=Life.New(function() return {contextSource="GAMEPLAY_CANDIDATE",status="COMPLETE_ROSTER",
 current={[0]=true},enabled={0},disabled={[0]=true},unknown={}} end,"MOCK_ONLY")
assert(bad.Refresh("AFTER_LOAD_CLOSE").status=="UNKNOWN" and not bad.Acquire(0))
''')
print('LOCAL_SIMULATION_PASS: stale/foreign/forged permits rejected; invalidate before failed refresh; unknown/disabled/no-current excluded; reacquisition; reentrant invalidation/newer refresh; fresh instance; conflicting roster. No game effect revocation implemented.')
