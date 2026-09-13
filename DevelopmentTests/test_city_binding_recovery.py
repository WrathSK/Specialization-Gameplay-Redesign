from pathlib import Path
from lupa import LuaRuntime
p=Path(__file__).resolve().parent
lua=LuaRuntime(unpack_returned_tuples=True)
lua.globals().Recovery=lua.execute((p/'CityBindingRecovery.lua').read_text())
lua.execute('''
local i={contextSource="MOCK_ONLY",readStatus="COMPLETE",registryValidated=true,isTestCivilization=true,
 cityPresent=true,phase="AFTER_LOAD_CLOSE",freshFoundationObserved=true,owner=0,cityID=3,x=4,y=5}
assert(Recovery.Decide(i).status=="PLAN_RESERVATION")
i.phase="BEFORE_LOAD_CLOSE";assert(Recovery.Decide(i).status=="DESIGN_DECISION_REQUIRED")
i.phase="AFTER_LOAD_CLOSE";i.freshFoundationObserved=false
assert(Recovery.Decide(i).status=="DESIGN_DECISION_REQUIRED")
i.record={uid="allocated-1",owner=0,cityID=3,x=4,y=5,state="RESERVED"}
assert(Recovery.Decide(i).reason=="PARTIAL_BINDING_NO_AUTOFILL")
i.cityToken="allocated-1";assert(Recovery.Decide(i).status=="PLAN_CONFIRMATION")
i.phase="BEFORE_LOAD_CLOSE";assert(Recovery.Decide(i).status=="PLAN_CONFIRMATION")
i.record.state="CONFIRMED";assert(Recovery.Decide(i).status=="BOUND_CANDIDATE")
i.owner=1;assert(Recovery.Decide(i).status=="DESIGN_DECISION_REQUIRED");i.owner=0
i.cityID=9;assert(Recovery.Decide(i).reason=="REFERENCE_CONFLICT");i.cityID=3
i.x=9;assert(Recovery.Decide(i).reason=="REFERENCE_CONFLICT");i.x=4
i.cityToken="other";assert(Recovery.Decide(i).reason=="TOKEN_CONFLICT")
i.cityToken="allocated-1";i.record=nil;assert(Recovery.Decide(i).reason=="PARTIAL_BINDING_NO_AUTOFILL")
i.readStatus="ERROR";assert(Recovery.Decide(i).status=="UNKNOWN")
i.readStatus="COMPLETE";i.registryValidated=false;assert(Recovery.Decide(i).status=="UNKNOWN")
i.registryValidated=true;i.cityPresent=false;assert(Recovery.Decide(i).status=="UNKNOWN")
assert(Recovery.Decide({contextSource="GAMEPLAY"}).status=="UNKNOWN")
''')
print('LOCAL_SIMULATION_PASS: binding recovery decisions; two-sided confirmation; partial state refuses autofill; load/ownership/reference/read failures. No allocation, engine binding or writes.')
