"""Compose actual local gate/envelope/bridge with API-shaped city objects, not engine APIs."""
from pathlib import Path
import json
from lupa import LuaRuntime
P=Path(__file__).resolve().parent
SETUP='''
ctx={contextSource="MOCK_ONLY",phase="AFTER_LOAD_CLOSE"}; writes=0; reads=0; lookups=0; mode="ok"; cells={}; cities={}
function copy(v) if type(v)~="table" then return v end;local c={};for k,x in pairs(v) do c[k]=copy(x) end;return c end
life=Life.New(function() return {contextSource="GAMEPLAY_CANDIDATE",status="COMPLETE_ROSTER",current={[0]=true},enabled={0},disabled={},unknown={}} end,"MOCK_ONLY")
life.Refresh("AFTER_LOAD_CLOSE")
for n=1,2 do
 local c={owner=0,cid=n,token="dev-"..n,x=n,y=0}
 function c:GetOwner() return self.owner end
 function c:GetID() return self.cid end
 function c:GetX() return self.x end
 function c:GetY() return self.y end
 function c:GetProperty(k)
  reads=reads+1;assert(k=="SPC_MOCK_CITY_ENVELOPE_CANDIDATE")
  if mode=="read_error" then error("READ") end
  if mode=="revoke_read" then life.Invalidate() end
  if mode=="owner_read" then self.owner=1 end
  return copy(cells[tostring(n)])
 end
 function c:SetProperty(k,v)
  writes=writes+1;assert(k=="SPC_MOCK_CITY_ENVELOPE_CANDIDATE")
  if mode=="drop" then return end
  cells[tostring(n)]=copy(v)
  if mode=="revoke_write" then life.Invalidate() end
  if mode=="after" then error("AFTER") end
 end
 cities[n]=c
end
local manager={GetCity=function(pid,cid) lookups=lookups+1;return cities[cid] end}
local binding={Resolve=function(pid,c) return c.token,"BOUND_MATCH" end}
deps={contextSource="MOCK_ONLY",life=life,CityManager=manager,binding=binding,Envelope=Envelope,Gate=Gate,Recovery=Recovery,Planner=Planner,State=State}
function channel(n,fresh)
 local proof=fresh and {contextSource="MOCK_ONLY",status="FRESH_BOUND_HISTORY_COMPLETE",owner=0,cityID=n,token="dev-"..n} or nil
 return Bridge.New(deps,0,n,"dev-"..n,proof,"MOCK_ONLY")
end
function submit(c,action,op,batch)
 local p=c.gate.Prepare(action,0,c.reference,ctx,batch)
 if p.status~="PLAN_ONLY" then return p end
 return c.gate.CommitRecordedMock(p.handle,op,c.writeFacts)
end
function finish(c) return c.gate.ResolveRecordedMock(c.reference,ctx) end
'''
def vm():
 l=LuaRuntime(unpack_returned_tuples=True)
 for n,f in [('Life','EligibilityLifecycle.lua'),('State','CitySpecializationState.lua'),('Planner','CityFactWritePlan.lua'),('Gate','CityOperationGate.lua'),('Recovery','PendingCityRecovery.lua'),('Envelope','UnifiedCityEnvelope.lua'),('Bridge','CityPropertyBridge.lua')]:l.globals()[n]=l.execute((P/f).read_text())
 l.execute(SETUP);return l
l=vm();l.execute('''
a=channel(1,true);b=channel(2,true)
assert(submit(a,"FOUNDATION","a1").status=="TARGET_OBSERVED_PENDING");assert(finish(a).status=="DONE_CONFIRMED_MOCK")
assert(submit(b,"FOUNDATION","b1").status=="TARGET_OBSERVED_PENDING");assert(finish(b).status=="DONE_CONFIRMED_MOCK")
local batch={status="COMPLETE_ORDERED_BATCH",orderBasis="ENGINE_DELIVERY",owner=0,cityUID="dev-1",eventID="first",
 districts={{family="CAMPUS",complete=true,districtUID="campus-1",mappingStatus="VALIDATED_FAMILY"}}}
assert(submit(a,"COMPLETION_BATCH","a2",batch).status=="TARGET_OBSERVED_PENDING");assert(finish(a).status=="DONE_CONFIRMED_MOCK")
assert(cells["1"].facts.specialization=="RESEARCH" and cells["2"].facts.specialization==nil)
local before=writes;assert(submit(a,"COMPLETION_BATCH","a3",batch).status=="READY" and writes==before)
assert(submit(b,"COMPLETION_BATCH","b2",batch).status=="UNKNOWN" and writes==before)
''')
def plain(t):return {k:plain(v) if hasattr(v,'items') else v for k,v in t.items()}
snapshot=json.loads(json.dumps(plain(l.globals().cells)))
n=vm()
def table(d):return n.table_from({k:table(v) if isinstance(v,dict) else v for k,v in d.items()})
n.globals().cells=table(snapshot)
n.execute('''a=channel(1,false);assert(writes==0);assert(submit(a,"FOUNDATION","new").status=="UNKNOWN");assert(finish(a).status=="DONE_CONFIRMED_MOCK" and writes==0);assert(submit(a,"FOUNDATION","new").status=="READY" and writes==0)''')
# Existing city without history must not be auto-created.
n=vm();n.execute('a=channel(1,false);assert(submit(a,"FOUNDATION","x").status=="UNKNOWN" and writes==0)')
# Expired eligibility must reject before any city lookup at channel creation.
n=vm();n.execute('life.Invalidate();assert(not pcall(channel,1,true) and lookups==0 and writes==0)')
# Owner/binding/position/deletion changes between plan and commit prohibit writes.
for change in ('cities[1].owner=1','cities[1].token="replacement"','cities[1].x=77','cities[1]=nil','life.Invalidate()','mode="owner_read"','mode="revoke_read"','mode="read_error"'):
 n=vm();n.execute('a=channel(1,true);p=a.gate.Prepare("FOUNDATION",0,a.reference,ctx);assert(p.status=="PLAN_ONLY")');n.execute(change)
 n.execute('local r=a.gate.CommitRecordedMock(p.handle,"op",a.writeFacts);assert(r.status=="REJECTED_BEFORE_WRITE" and writes==0)')
for mode in ('drop','after','revoke_write'):
 n=vm();n.execute('a=channel(1,true)');n.globals().mode=mode
 r=n.eval('submit(a,"FOUNDATION","x")')
 if mode=='after':
  assert r.status=='TARGET_OBSERVED_PENDING';n.execute('assert(finish(a).status=="DONE_CONFIRMED_MOCK" and writes==3)')
 else:
  assert r.status=='WRITE_OUTCOME_UNKNOWN_HALTED';assert n.globals().writes==1
  if mode=='revoke_write':n.execute('assert(cells["1"].record.state=="PENDING" and cells["1"].facts==nil)')
print('LOCAL_SIMULATION_PASS: API-shaped City Property bridge + existing gate; 2 independent cities, completion/no-op, JSON reload reconciliation, no-history refusal, entry permission before city access, owner/token/position/deletion/revocation/read/write failures. No engine or event hook.')
