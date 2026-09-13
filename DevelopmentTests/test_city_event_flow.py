from pathlib import Path
import ast
from lupa import LuaRuntime
P=Path(__file__).resolve().parent
# Reuse the existing city API fixture without executing its test script.
setup=next(ast.literal_eval(n.value) for n in ast.parse((P/'test_city_property_bridge.py').read_text()).body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='SETUP' for t in n.targets))
def vm():
 l=LuaRuntime(unpack_returned_tuples=True)
 for n,f in [('Life','EligibilityLifecycle.lua'),('State','CitySpecializationState.lua'),('Planner','CityFactWritePlan.lua'),('Gate','CityOperationGate.lua'),('Recovery','PendingCityRecovery.lua'),('Envelope','UnifiedCityEnvelope.lua'),('Bridge','CityPropertyBridge.lua'),('Flow','CityEventFlow.lua')]:l.globals()[n]=l.execute((P/f).read_text())
 l.execute(setup)
 l.execute('''legacyCalls=0;health="TRACKING";scan="COMPLETE";v01=0;order={}
 function newFlow()
 return Flow.New({life=life,
 legacy=function(pid,cid) legacyCalls=legacyCalls+1;order[#order+1]="legacy";if reenter then flow.Fresh(pid,cid) end;if revoke then life.Invalidate() end end,
 inspectFresh=function(pid,cid) order[#order+1]="inspect";return {contextSource="MOCK_ONLY",owner=pid,cityID=cid,token="dev-"..cid,legacyHealth=health,bindingValidated=true,foundationObserved=true,scanStatus=scan,centerComplete=true,completedV01Count=v01} end,
 open=function(pid,cid,token,proof) order[#order+1]="open";return Bridge.New(deps,pid,cid,token,proof,"MOCK_ONLY") end,
 inspectComplete=function(pid,raw) return raw end},"MOCK_ONLY") end
 flow=newFlow()
 function event(family,cid) return {status="VALIDATED",owner=0,cityID=cid or 1,token="dev-"..(cid or 1),complete=true,mappingStatus="VALIDATED_FAMILY",family=family,districtUID="district-"..family} end
 function ready() flow.Ready({fresh=true,complete=true}) end
 ''');return l
l=vm();l.execute('''
assert(flow.Fresh(0,1).status=="IGNORED_PHASE" and legacyCalls==0 and writes==0)
assert(flow.Complete(0,event("CAMPUS")).status=="IGNORED_PHASE")
ready();assert(flow.Fresh(0,1).status=="COMMITTED_MOCK" and writes==3)
assert(table.concat(order,",")=="legacy,inspect,open")
assert(flow.Fresh(0,1).status=="DUPLICATE_NO_WRITE" and legacyCalls==2 and writes==3)
assert(flow.Complete(0,event("THEATER_SQUARE")).status=="COMMITTED_MOCK" and writes==6)
assert(cells["1"].facts.specialization=="CULTURE")
assert(flow.Complete(0,event("CAMPUS")).status=="NO_WRITE" and writes==6)
assert(flow.Complete(0,event("THEATER_SQUARE")).status=="NO_WRITE" and writes==6)
assert(flow.Complete(0,event("CAMPUS",2)).status=="UNTRACKED_NO_WRITE" and writes==6)
assert(flow.Fresh(0,2).status=="COMMITTED_MOCK" and writes==9)
assert(flow.Complete(0,event("CAMPUS",2)).status=="COMMITTED_MOCK" and cells["2"].facts.specialization=="RESEARCH" and writes==12)
-- A new stream cannot use existing DONE as a certificate of continuous history.
flow.Close();assert(flow.Complete(0,event("CAMPUS")).status=="IGNORED_PHASE")
flow=newFlow();ready();assert(flow.Complete(0,event("CAMPUS")).status=="UNTRACKED_NO_WRITE" and writes==12)
''')
for mutation in ('health="GAP"','scan="PARTIAL"','v01=1','reenter=true','revoke=true'):
 n=vm();n.execute('ready()');n.execute(mutation)
 n.execute('assert(flow.Fresh(0,1).status=="HELD" and writes==0);assert(flow.Complete(0,event("CAMPUS")).status=="HELD" and writes==0)')
n=vm();n.execute('''ready();assert(flow.Fresh(0,1).status=="COMMITTED_MOCK")
local bad=event("CAMPUS");bad.status="UNKNOWN"
assert(flow.Complete(0,bad).status=="HELD")
assert(flow.Complete(0,event("THEATER_SQUARE")).status=="HELD" and writes==3 and cells["1"].facts.specialization==nil)
''')
n=vm();n.execute('ready();mode="drop";assert(flow.Fresh(0,1).status=="HELD" and writes==1);mode="ok";assert(flow.Fresh(0,1).status=="HELD" and writes==1)')
n=vm();n.execute('ready();life.Invalidate();assert(flow.Fresh(0,1).status=="HELD" and legacyCalls==0 and lookups==0)')
print('LOCAL_SIMULATION_PASS: ordered legacy/verify/bridge flow; no load adoption; two-city first delivered lock; duplicate preservation; swallowed legacy failure, incomplete scan, reentry, permission loss, invalid completion and write failure hold later events. Session only, not native event or persistent continuity proof.')
