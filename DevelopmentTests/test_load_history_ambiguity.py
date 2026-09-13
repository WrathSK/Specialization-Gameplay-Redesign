"""Counterexample: identical durable records do not certify uninterrupted history."""
from pathlib import Path
import ast
from lupa import LuaRuntime
P=Path(__file__).resolve().parent;R=P.parent/"Sid Meier's Civilization VI/Mods/SpecializationP0"
a=ast.parse((P/'test_city_journal_probe.py').read_text())
f=max((n.args[0].value for n in ast.walk(a) if isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute) and n.func.attr=='execute' and n.args and isinstance(n.args[0],ast.Constant) and isinstance(n.args[0].value,str)),key=len)
# Keep just the actual-source mock fixture; run an independent fault scenario.
f=f[:f.index('fresh();assert(s.CityJournalProbe.Read')]
f=f.replace('local props,gprops={},{}','local loseAll=false;local props,gprops={},{}')
f=f.replace(' if k==KEY then\n  physicalWrites',' if loseAll then return end\n if k==KEY then\n  physicalWrites',1)
f=f.replace('SPCCityJournalProbe.Start(P,s)','SPCCityJournalProbe.Start(P,s);SPCCityFlowProbe.Start(P,s)')
f+='''
local function equal(a,b)
 if type(a)~=type(b) then return false end
 if type(a)~="table" then return a==b end
 for k,v in pairs(a) do if not equal(v,b[k]) then return false end end
 for k in pairs(b) do if a[k]==nil then return false end end;return true
end
fresh();found()
local persisted=clone(props);local gamePersisted=clone(gprops)
local FLOW="SPC_DEV_CITY_FLOW_B020"
assert(props[FLOW].stage=="DONE" and props[FLOW].facts.specialization=="NONE")
-- An actual callback is delivered, but all City Property setter attempts are lost.
loseAll=true;complete(1);dlist[2]=current
assert(s.CityJournalProbe.players[0].halted and s.CityFlowProbe.players[0].halted)
assert(equal(props,persisted) and equal(gprops,gamePersisted))
-- Model subsequent removal of this district; current-city scan no longer exposes it.
dlist={district(0,10)};current=dlist[1];loseAll=false
boot();Events.LoadScreenClose.Fire()
assert(equal(props,persisted) and equal(gprops,gamePersisted))
assert(props[KEY].health=="TRACKING" and props[KEY].specialization=="NONE")
assert(not s.CityJournalProbe.players[0].halted)
assert(props[FLOW].stage=="DONE" and s.CityFlowProbe.Read(0,city):find("LOAD_READ_ONLY"))
assert(s.CityFlowProbe.players[0].writes==0)
-- The legacy path can select a later completion, despite the first one being lost.
complete(2)
assert(props[KEY].specialization=="CULTURE")
-- B020 does not make that guess: its read-only boundary preserves the saved state.
assert(props[FLOW].facts.specialization=="NONE" and s.CityFlowProbe.players[0].writes==0)
'''
l=LuaRuntime(unpack_returned_tuples=True)
for n in ['BindingProbe.lua','CityJournalProbe.lua','FreshBindingHook.lua','CityFlowProbe.lua']:l.execute((R/n).read_text())
l.execute(f)
print('LOCAL_SIMULATION_PASS: actual B015/B020 failure counterexample reproduced. Lost writes + lost GAP leave identical durable state; fresh instance loses session halt; current scan need not reveal history. B020 LOAD_READ_ONLY prevents later guessed first lock; legacy B015 can diverge. This is a limitation test, not recovery success or actual game failure.')
