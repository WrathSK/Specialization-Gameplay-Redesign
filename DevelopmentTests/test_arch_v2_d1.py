"""D1 real Lua scheduling + real Network bridge scaling; no engine/deployment.
Historical tests remain byte-frozen. C1 direct-mutated fixtures explicitly signal
D1 dirtiness; A/B regressions use their historical Discount consumer to retain
old count assertions. New Discount counts/output are checked separately below.
"""
from pathlib import Path
import ast, subprocess
from lupa.lua55 import LuaRuntime
R=Path(__file__).resolve().parents[1];M=R/'Mod'
def historical(rev,file):
 return subprocess.check_output(['git','-C',str(R),'show',rev+':Mod/'+file],text=True)
def literal(file,name):
 for n in ast.parse((R/'DevelopmentTests'/file).read_text()).body:
  if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id==name for t in n.targets):return ast.literal_eval(n.value)
 raise AssertionError(name)
FIX=literal('test_arch_v2_c1.py','FIX')
BATCH=r"""
shared.NetworkBridge.DiscountBatch=function(pid)
 if unknown then error('NETWORK_REFRESH_PENDING') end
 local out={};for cid,ids in pairs(receivers) do out[cid]={};for _,id in ipairs(ids) do out[cid][id]=true end end
 return {input={epoch=1,inputVersion=1,validity='VERIFIED'},recipients=out}
end
"""
def runtime(source=None,ui=True):
 l=LuaRuntime(unpack_returned_tuples=True);l.execute(FIX+BATCH)
 l.execute((M/'PerformanceCounters.lua').read_text());l.execute('ExposedMembers.SPC_Performance=SPCPerformance.New();P.Count=SPCPerformance.Count')
 l.execute(source or (M/'StandardizationDiscount.lua').read_text());l.execute('SPCStandardizationDiscount.Start(P,shared);d=shared.StandardizationDiscount')
 if ui:l.execute((M/'UI/DiscountEligibility.lua').read_text())
 return l
# All previous C1 lifecycle Lua assertions, same delayed transport and engine mocks.
c1=(R/'DevelopmentTests/test_arch_v2_c1.py').read_text()
c1=c1[c1.index('l=runtime();'):c1.index('# Normal verified results')]
c1=c1.replace('d.Audit()',"d.MarkDirty(0,'test_direct');d.Audit()")
exec(compile(c1,'C1_lifecycle_with_direct_fact_signals','exec'))
# Generic notifications, ordinary units and other-module clean audits cannot scan.
l=runtime();l.execute(r"""
ready();cities[3]=nil;cities[4]=nil;receivers[3]=nil;receivers[4]=nil
d.MarkDirty(0,'city');d.Audit();pulse(3)
local audit=total('audit_standard');local cap=total('discount_fact_capture');local scan=total('discount_ui_scan');local w=writes
for i=1,10000 do pulse();fire('GameCoreEventPlaybackComplete');fire('SystemUpdateUI');fire('UnitOperationStarted');d.Audit() end
assert(total('audit_standard')==audit and total('discount_fact_capture')==cap)
assert(total('discount_ui_scan')==scan and writes==w)
print('PASS D1: 10000 Publish + Playback + UI + unit pulses: 0 audits / 0 captures / 0 native UI scans / 0 writes')
-- Once per player turn, not once per activation callback.
local n=total('discount_reconcile');turn=2
for i=1,10000 do fire('PlayerTurnActivated') end
assert(total('discount_reconcile')==n+1)
-- Missing direct event: turn reconciliation recovers changed ACTIVE.
cities[1].active=2;turn=3;fire('PlayerTurnActivated');pulse(3);assert(rate(2)==20)
local n=total('discount_fact_capture');local w=writes
for i=1,10000 do pulse() end
assert(total('discount_fact_capture')==n and writes==w)
-- Native permission is an independent input, not Network version.
permission=false;fire('ResearchCompleted');pulse(3);assert(rate(2)==0)
permission=true;fire('GovernmentPolicyChanged');pulse(3);assert(rate(2)==20)
local n=total('discount_fact_capture');local a=total('appliedSamples')
permission=false;fire('CityProductionChanged');pulse(3);assert(rate(2)==0)
assert(total('discount_fact_capture')==n) -- apply-only is not network capture
""".replace("local a=total('appliedSamples')",''))
print('PASS D1: missed event fallback, bounded turn, independent native permission apply-only')
# Real building callbacks, carrier self-events, template publication, duplicates.
l=runtime();l.execute(r"""
ready();local a=total('audit_standard');local u=total('discount_ui_scan')
rows[101]={BuildingType='BUILDING_SPC_B054_TEST_1'}
for _,f in ipairs(hooks.BuildingAddedToMap) do f(0,0,101,0) end
assert(total('audit_standard')==a and total('discount_ui_scan')==u)
permission=false
for _,f in ipairs(hooks.BuildingAddedToMap) do f(0,0,1,0) end
pulse(3);assert(rate(2)==0 and total('audit_standard')>a)
shared.Standardization.ReadLedger=function() return {learned={}} end
d.MarkDirty(0,'template');pulse(3);assert(next(d.plans[0].targets[2])==nil)
shared.Standardization.ReadLedger=function() return {learned={TEST=true}} end
permission=true;d.MarkDirty(0,'template');pulse(3);assert(rate(2)==40)
local a=total('audit_standard')
for i=1,10000 do d.Audit({player=0,epoch=1,inputVersion=1,validity='VERIFIED'}) end
assert(total('audit_standard')==a)
""")
print('PASS D1: building prerequisite, carrier feedback excluded, template change, duplicate publication')
# C1 -> D1 final full carrier map, union/max (two classified buildings/groups).
def comparison(source):
 l=runtime(source,False);l.execute(r"""
rows.EXTRA={Index=2,Hash=2,BuildingType='EXTRA'};rows[2]=rows.EXTRA
for n=1,4 do rows['BUILDING_SPC_B054_EXTRA_'..n]={Index=200+n} end
SPCStandardizationCatalog.Build=function() return {buildings={TEST={enabled=true,group='T1'},EXTRA={enabled=true,group='T2'}}} end
learned={[1]={TEST=true},[4]={EXTRA=true}}
shared.Standardization.ReadLedger=function(pid,c) return {learned=learned[c.id] or {}} end
receivers={[2]={1,4},[3]={1,4}}
function encode(t) if type(t)~='table' then return tostring(t) end;local a={};for k,v in pairs(t) do a[#a+1]=tostring(k)..'='..encode(v) end;table.sort(a);return '{'..table.concat(a,',')..'}' end
function update()
 if d.MarkDirty then d.MarkDirty(0,'fixture_change') end;d.Audit()
 local lines={};for cid,bs in pairs(d.plans[0].targets) do for id in pairs(bs) do lines[#lines+1]=cid..','..rows[id].Index..','..(permission and '1' or '0') end end
 seq2=(seq2 or 0)+1;local p=packet(seq2,table.concat(lines,';'));p.Count=#lines;d.Receive(0,p)
end
function result() local o={};for id,c in pairs(cities) do o[id]=c.built end;return encode(o) end
d.EnsureReady(0);ExposedMembers.SPC_DiscountClientEpoch=1
""");return l
a,b=comparison(historical('affe4c8','StandardizationDiscount.lua')),comparison(None)
cases=0
for level in range(1,5):
 for other in range(1,5):
  for allowed in (True,False):
   for l in (a,b):l.execute(f'cities[1].active={level};cities[4].active={other};permission={str(allowed).lower()};update()')
   assert a.eval('result()')==b.eval('result()');cases+=1
for step in ["learned[4]={}","cities[1].kind='RESEARCH'", "cities[1].kind='INDUSTRY'", "receivers[2]={}","cities[4].owner=1", "receivers[2]={1};cities[4].owner=0;learned[4]={EXTRA=true}","cities[2].x=10"]:
 for l in (a,b):l.execute(step+';update()')
 assert a.eval('result()')==b.eval('result()');cases+=1
print('PASS D1:',cases,'complete carrier-map comparisons versus B073: max/union/permission/template/qualification/reference/removal')
# Real bridge capture scaling; sources absent gives exact isolated C² -> C budget.
NFIX=literal('test_arch_v2_batch_a.py','FIXTURE')
def network_runtime(n,old=False):
 l=LuaRuntime(unpack_returned_tuples=True);l.globals().include=lambda name:l.execute((M/(name+'.lua')).read_text())
 l.execute(NFIX);l.execute((M/'PerformanceCounters.lua').read_text())
 l.execute('ExposedMembers.SPC_Performance=SPCPerformance.New();P.Count=SPCPerformance.Count')
 l.execute((M/'NetworkBridge.lua').read_text());l.execute('SPCNetworkBridge.Start(P,shared);net=shared.NetworkBridge;net.ready=true')
 l.globals().N=n
 l.execute(r"""
local prototype=cities[1];cities={}
for id=1,N do local c={id=id,owner=0,token='CITY'..id,kind='NONE',active=0,potential=0,built={}};cities[id]=c
 c.GetID=function() return c.id end;c.GetOwner=function() return 0 end;c.GetX=function() return c.id end;c.GetY=function() return 10 end
 c.GetProperty=function() return c.token end;c.GetName=function() return 'C'..c.id end;c.GetBuildings=function() return c.built end;c.GetBuildQueue=function() return c.built end
end
SPCStandardizationCatalog={Build=function() return {buildings={TEST={enabled=true,group='T1'}}} end}
P.Info=function(_,id) return {Index=100+tonumber(id:match('(%d+)$'))} end
P.HasBuilding=function(b,i) return b[i]==true end
P.CreateBuilding=function(b,i) b[i]=true;P.Count('building_create') end
P.RemoveBuilding=function(b,i) b[i]=nil;P.Count('building_remove') end
shared.Standardization={ReadLedger=function() return {learned={TEST=true}} end}
function total(k) return ExposedMembers.SPC_Performance.entries[k].total end
local read=shared.EffectiveFacts.Read;shared.EffectiveFacts.Read=function(...) P.Count('facts');return read(...) end
send('',0)
""")
 l.execute(historical('affe4c8','StandardizationDiscount.lua') if old else (M/'StandardizationDiscount.lua').read_text())
 l.execute('SPCStandardizationDiscount.Start(P,shared);d=shared.StandardizationDiscount;d.EnsureReady(0)')
 return l
print('cities | old fact reads / queries / city scans | D1 fact reads / queries / city scans / processed')
for n in [1,2,4,8]:
 results=[]
 for old in [True,False]:
  l=network_runtime(n,old);keys=['facts','derive_requested','city_scan','discount_city_processed']
  before=[l.eval(f'total("{k}")') for k in keys]
  l.execute("if d.MarkDirty then d.MarkDirty(0,'reconcile') end;d.Audit()")
  delta=[l.eval(f'total("{k}")')-v for k,v in zip(keys,before)];results.append(delta)
  assert delta[:3]==([n*n,n,n*n+2*n] if old else [n,1,3*n]),(n,old,delta)
  if not old:assert delta[3]==n
 print(n,results)
# Real Network publisher handles source ACTIVE/qualification without route change.
l=network_runtime(4);l.execute(r"""
cities[1].kind='INDUSTRY';cities[1].active=3;cities[1].potential=4
send('0,1,0,2,10',1)
assert(d.plans[0].targets[2].TEST==3)
local rev=net.Input(0).inputVersion
cities[1].active=4;net.Rebuild();assert(net.Input(0).inputVersion==rev+1 and d.plans[0].targets[2].TEST==4)
cities[1].active=0;net.Rebuild();assert(next(d.plans[0].targets[2])==nil)
cities[1].active=4;net.Rebuild();assert(d.plans[0].targets[2].TEST==4)
local w=total('building_create')+total('building_remove');readFail=true;net.Rebuild()
d.MarkDirty(0,'reconcile');d.Audit();assert(d.plans[0].targets[2].TEST==4)
assert(total('building_create')+total('building_remove')==w)
readFail=false;units[10]=nil;net.CheckEvidence(false);assert(next(d.plans[0].targets[2])==nil)
""")
print('PASS D1: real A/B publisher ACTIVE 3->4->0->4 / UNKNOWN holds / confirmed route removal')
# Shared source ledger is read once even when every city receives Industry.
l=network_runtime(8);l.execute(r"""
cities[1].kind='INDUSTRY';cities[1].active=4;cities[1].potential=4
ledgerReads=0;shared.Standardization.ReadLedger=function(pid,c)
 ledgerReads=ledgerReads+1;shared.EffectiveFacts.Read(pid,c);return {learned={TEST=true}}
end
send('0,1,0,2,10;0,1,0,3,11;0,1,0,4,12;0,1,0,5,13;0,1,0,6,14;0,1,0,7,15;0,1,0,8,16',7)
local f=total('facts');local q=total('derive_requested');local led=ledgerReads
d.MarkDirty(0,'template');d.Audit()
assert(total('facts')-f==10 and total('derive_requested')-q==1 and ledgerReads-led==1)
local copy=net.DiscountBatch(0);copy.recipients[2]={};d.MarkDirty(0,'template');d.Audit()
assert(d.plans[0].targets[2].TEST==4) -- caller cannot mutate shared view
""")
print('PASS D1: 8 Industry recipients: 8 capture facts + 2 source/ledger facts; one ledger read / one Network query')
# Real ledger writes signal downstream; rediscovery of unchanged ledger does not.
l=runtime();l.execute(r"""
ready();GameEvents=Events
for _,c in pairs(cities) do c.props={};c.GetProperty=function(_,k) return c.props[k] end end
P.SetProperty=function(c,k,v) c.props[k]=v end
shared.EffectiveFacts.Read=function(pid,c) return {specialization=c.kind,active=c.active,token='CITY'..c.id} end
SPCStandardizationCatalog.Build=function() return {buildings={TEST={enabled=true,group='T1',district='DISTRICT_TEST',tier=1,index=1}}} end
""")
l.execute((M/'Standardization.lua').read_text());l.execute(r"""
SPCStandardization.Start(P,shared);local std=shared.Standardization;std.ready=true
std.Discover(0);pulse(3);local dirty=total('discount_dirty_mark');local a=total('audit_standard')
std.Discover(0);pulse(3);assert(total('discount_dirty_mark')==dirty and total('audit_standard')==a)
cities[1].built[1]=true;std.Queue(0,1,1,'TEST_COMPLETION');std.Flush();pulse(3)
assert(std.writes==5 and d.plans[0].targets[2].TEST==4)
""")
print('PASS D1: actual Standardization initial/learned write notification, unchanged ledger no dirty')
# Failed initialization does not become a generic-event retry storm.
l=runtime(ui=False);l.execute(r"""
local calls=0;SPCStandardizationCatalog.Build=function() calls=calls+1;error('MOCK_DATABASE_UNAVAILABLE') end
d.EnsureReady(0);local a=total('audit_standard');local before=calls;pulse(10000)
assert(calls==before and total('audit_standard')==a and d.globalError)
""")
print('PASS D1: failed batch retries only on new direct input or turn reconciliation')
# All A/B/B069 network correctness matrices, historical consumer count contract.
# Only substitute old Discount inside the historical B runner, not production files.
s=(R/'DevelopmentTests/test_arch_v2_batch_b.py').read_text().replace("get('version')=='98'","get('version')=='101'")
s=s.replace("(M/'StandardizationDiscount.lua').read_text()", "historical_discount")
ns={'__file__':str(R/'DevelopmentTests/test_arch_v2_batch_b.py'),'historical_discount':historical('affe4c8','StandardizationDiscount.lua')}
exec(compile(s,'A_B_regression_historical_consumer','exec'),ns)
for p in M.rglob('*.lua'):
 v=l.eval('load')(p.read_text(),str(p));assert not isinstance(v,tuple),(p,v)
print('LOCAL_SIMULATION_PASS D1; all Lua syntax; historical tests unmodified; no deployment')
