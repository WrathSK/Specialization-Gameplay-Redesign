"""Failure injection against a MOCK store, not Civ VI Property atomicity."""
from pathlib import Path
from lupa import LuaRuntime
p=Path(__file__).resolve().parent
lua=LuaRuntime(unpack_returned_tuples=True)
lua.globals().Registry=lua.execute((p/'CityIdentityRegistry.lua').read_text())
lua.execute('''
local ref={owner=0,cityID=7}
local proof={isTestCivilization=true,present=true,validatedInstance=true,instanceProof="fixture-instance-A",
 registryBootstrapConfirmed=true,freshFoundationObserved=true,phase="AFTER_LOAD_CLOSE"}
local function fixture(mode)
 local f={writes=0,reads=0}
 f.io={Read=function()
  f.reads=f.reads+1
  if (mode=="read_fail" and f.reads==1) or (mode=="readback_fail" and f.reads==3) then error("read failure") end
  if mode=="concurrent" and f.reads==2 then f.value={schema=1,counter=0,revision=0,records={}} end
  return f.value -- intentional reference sharing
 end,Write=function(v)
  f.writes=f.writes+1
  if mode=="before" then error("before write") end
  if mode=="drop" then return end
  if mode=="reentrant" then assert(f.registry.Ensure(ref,proof).reason=="REENTRANT_CALL") end
  f.value=v
  if mode=="corrupt" then f.value.counter=99 end
  if mode=="after" then error("lost acknowledgment") end
 end}
 f.registry=Registry.New(f.io,"MOCK_ONLY")
 return f
end
local f=fixture()
local one=f.registry.Ensure(ref,proof);assert(one.status=="READY" and one.uid=="SPC-CITY-1")
assert(not f.registry.Ensure(ref,proof).changed and f.writes==1)
-- Recreate the allocator: no in-memory counter is needed for recovery.
f.registry=Registry.New(f.io,"MOCK_ONLY")
proof.phase="BEFORE_LOAD_CLOSE";proof.freshFoundationObserved=false
assert(f.registry.Ensure(ref,proof).uid==one.uid and f.writes==1)
assert(f.registry.Ensure({owner=0,cityID=8},proof).status=="DESIGN_DECISION_REQUIRED")
proof.phase="AFTER_LOAD_CLOSE";proof.freshFoundationObserved=true
assert(f.registry.Ensure({owner=1,cityID=7},proof).status=="DESIGN_DECISION_REQUIRED")
proof.instanceProof="fixture-instance-B"
assert(f.registry.Ensure({owner=0,cityID=8},proof).uid=="SPC-CITY-2")
-- A failed update must not mutate the table returned by a shared-reference getter.
local original=f.value
local failUpdate=Registry.New({Read=function() return original end,Write=function() error("failed") end},"MOCK_ONLY")
proof.instanceProof="fixture-instance-C"
assert(failUpdate.Ensure({owner=0,cityID=9},proof).status=="NOT_COMMITTED")
assert(original.counter==2 and original.records["0:9"]==nil)
-- References are not UIDs: a different object reusing the same reference is rejected.
proof.instanceProof="fixture-reused-instance"
assert(f.registry.Ensure(ref,proof).reason=="INSTANCE_REUSE_UNRESOLVED")
proof.instanceProof="fixture-instance-A"
for _,mode in ipairs({"before","drop"}) do
 local x=fixture(mode);assert(x.registry.Ensure(ref,proof).status=="NOT_COMMITTED")
 assert(x.writes==1 and x.value==nil)
 -- A retry with a healthy storage backend does not skip an allocation.
 local healthy=fixture();assert(healthy.registry.Ensure(ref,proof).uid=="SPC-CITY-1")
end
local after=fixture("after")
local ack=after.registry.Ensure(ref,proof)
assert(ack.status=="READY" and not ack.writeAcknowledged)
assert(not after.registry.Ensure(ref,proof).changed and after.writes==1)
local uncertain=fixture("readback_fail")
assert(uncertain.registry.Ensure(ref,proof).status=="UNKNOWN" and uncertain.writes==1)
uncertain.registry=Registry.New(uncertain.io,"MOCK_ONLY")
assert(uncertain.registry.Ensure(ref,proof).uid=="SPC-CITY-1" and uncertain.writes==1)
local bad=fixture("corrupt");assert(bad.registry.Ensure(ref,proof).status=="UNKNOWN")
assert(bad.registry.Ensure(ref,proof).status=="UNKNOWN" and bad.writes==1)
local unread=fixture("read_fail");assert(unread.registry.Ensure(ref,proof).status=="UNKNOWN" and unread.writes==0)
local conflict=fixture("concurrent");assert(conflict.registry.Ensure(ref,proof).reason=="STALE_PLAN" and conflict.writes==0)
local reentrant=fixture("reentrant");assert(reentrant.registry.Ensure(ref,proof).status=="READY" and reentrant.writes==1)
local invalid=fixture();invalid.value={schema=2,counter=0,revision=0,records={}}
assert(invalid.registry.Ensure(ref,proof).status=="UNKNOWN" and invalid.writes==0)
local off=fixture();off.registry=Registry.New(off.io,"GAMEPLAY")
assert(off.registry.Ensure(ref,proof).reason=="OFFLINE_ONLY" and off.writes==0)
proof.isTestCivilization=false;assert(f.registry.Ensure(ref,proof).status=="UNKNOWN");proof.isTestCivilization=true
proof.validatedInstance=false;assert(f.registry.Ensure(ref,proof).status=="UNKNOWN");proof.validatedInstance=true
proof.registryBootstrapConfirmed=false
local missing=fixture();assert(missing.registry.Ensure(ref,proof).reason=="EMPTY_REGISTRY_NOT_PROVEN_NEW" and missing.writes==0)
proof.registryBootstrapConfirmed=true
savedRegistry=f.value
''')
# Serialize/reload in a new Lua VM, modelling a fresh process without registry memory.
import json
def plain(v):
    return {k:plain(x) for k,x in v.items()} if hasattr(v,'items') else v
serialized=json.dumps(plain(lua.globals().savedRegistry))
new=LuaRuntime(unpack_returned_tuples=True)
new.globals().Registry=new.execute((p/'CityIdentityRegistry.lua').read_text())
def table(v):
    return new.table_from({k:table(x) for k,x in v.items()}) if isinstance(v,dict) else v
new.globals().persisted=table(json.loads(serialized))
new.execute('''
local r=Registry.New({Read=function() return persisted end,Write=function() error("RESTORE_MUST_NOT_WRITE") end},"MOCK_ONLY")
assert(r.Ensure({owner=0,cityID=7},{isTestCivilization=true,present=true,validatedInstance=true,
 instanceProof="fixture-instance-A",phase="BEFORE_LOAD_CLOSE"}).uid=="SPC-CITY-1")
''')
print('LOCAL_SIMULATION_PASS: identity envelope; duplicate/reload; write-before/after/drop; failed readback recovery; corruption; stale/reentrant rejection; JSON/new-VM restoration. Engine identity proof and Property durability NOT verified.')
