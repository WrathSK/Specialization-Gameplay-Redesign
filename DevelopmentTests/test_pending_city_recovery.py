from pathlib import Path
import json
from lupa import LuaRuntime
p=Path(__file__).resolve().parent
def runtime():
    l=LuaRuntime(unpack_returned_tuples=True)
    l.globals().Recovery=l.execute((p/'PendingCityRecovery.lua').read_text())
    return l
l=runtime()
l.execute('''
local target={schemaVersion=1,cityUID="c1",owner=0,revision=0,investments={},ownedTemplates={}}
local made=Recovery.Create("op1",nil,target,"MOCK_ONLY");assert(made.status=="RECORD_PLAN_ONLY")
saved=made.record;assert(saved.beforePresent==false and saved.before==nil)
target.owner=9;assert(saved.target.owner==0)
''')
def plain(t):return {k:plain(v) if hasattr(v,'items') else v for k,v in t.items()}
serialized=json.dumps(plain(l.globals().saved),sort_keys=True)
n=runtime()
def table(d):return n.table_from({k:table(v) if isinstance(v,dict) else v for k,v in d.items()})
n.globals().saved=table(json.loads(serialized))
n.execute('''
local function observed(facts)
 return {contextSource="MOCK_ONLY",status="READ_OK",present=true,cityUID="c1",owner=0,facts=facts}
end
local function inspect(o,expect)
 local r=Recovery.Inspect(saved,o,"MOCK_ONLY")
 assert(r.status=="RECOVERY_HELD" and r.comparison==expect)
 assert(not r.mayWrite and not r.mayActivate and not r.mayClearRecord)
end
inspect(observed(nil),"BEFORE_OBSERVED") -- saved after intent, before fact write
inspect(observed(saved.target),"TARGET_OBSERVED") -- saved after data write, before resolution
inspect(observed({other=true}),"CONFLICT_OBSERVED")
local o=observed(saved.target);o.owner=1;inspect(o,"UNKNOWN")
o=observed(saved.target);o.cityUID="new-city";inspect(o,"UNKNOWN")
o=observed(saved.target);o.present=false;inspect(o,"UNKNOWN")
o=observed(saved.target);o.status="READ_FAILED";inspect(o,"UNKNOWN")
assert(saved.state=="PENDING" and saved.operationID=="op1")
assert(Recovery.Inspect(nil,observed(nil),"MOCK_ONLY").comparison=="UNKNOWN")
local schema=saved.schema;saved.schema=99;inspect(observed(nil),"UNKNOWN");saved.schema=schema
saved.beforePresent=true;inspect(observed(nil),"UNKNOWN");saved.beforePresent=false
for i=1,3 do inspect(observed(saved.target),"TARGET_OBSERVED") end -- repeated read never resolves
local before={cityUID="c1",owner=0,revision=0,investments={}}
local after={cityUID="c1",owner=0,revision=1,investments={},specialization="RESEARCH"}
local next=Recovery.Create("op2",before,after,"MOCK_ONLY");assert(next.status=="RECORD_PLAN_ONLY")
local r=Recovery.Inspect(next.record,observed(before),"MOCK_ONLY");assert(r.comparison=="BEFORE_OBSERVED")
after.revision=3;assert(Recovery.Create("bad",before,after,"MOCK_ONLY").status=="UNKNOWN")
assert(Recovery.Create("bad",nil,saved.target,"GAMEPLAY").status=="UNKNOWN")
''')
print('LOCAL_SIMULATION_PASS: serialized pending record/new Lua VM; before/target/conflict/unknown recovery; owner/generation/read failures; corrupt schema/presence; repeated inspections preserve hold; no auto-write/clear/activation. No engine persistence claim.')
