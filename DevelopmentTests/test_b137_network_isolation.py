"""B137 bounded actual-module Network isolation tests.
No game, database, deployment, broad historical wrapper or stress loop.
Historical fixture literals alone are read with AST. Native API mocks prove local
control/ownership behavior, never native memory improvement or gameplay PASS.

PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/tmp/spc-b069-python /opt/homebrew/bin/python3.14 DevelopmentTests/test_b137_network_isolation.py
"""
from pathlib import Path
import argparse
import ast
import json
import subprocess
from lupa.lua55 import LuaRuntime

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--repo', type=Path, default=(Path(__file__).resolve().parents[1]
    if Path(__file__).resolve().parent.name == 'DevelopmentTests' else Path.cwd()))
args = parser.parse_args()
ROOT = args.repo.resolve()
MOD = ROOT / 'Mod'
BASELINE = 'bb1bab3'
COUNTS = {}


def source(name, old=False):
    path = name + '.lua'
    if old:
        return subprocess.check_output(['git', 'show', f'{BASELINE}:Mod/{path}'], cwd=ROOT, text=True)
    return (MOD / path).read_text()


def fixture(filename, name):
    tree = ast.parse((ROOT / 'DevelopmentTests' / filename).read_text())
    node = next(n for n in tree.body if isinstance(n, ast.Assign)
                and any(isinstance(t, ast.Name) and t.id == name for t in n.targets))
    return ast.literal_eval(node.value)


def runtime(fix, old=False):
    lua = LuaRuntime(unpack_returned_tuples=True)
    lua.execute(fix)
    lua.globals().include = lambda name: lua.execute(source(name, old))
    lua.execute(source('PerformanceCounters', old))
    lua.execute('ExposedMembers.SPC_Performance=SPCPerformance.New();P.Count=SPCPerformance.Count;print=function() end')
    return lua


C2 = fixture('test_arch_v2_c2.py', 'FIX')
C1 = fixture('test_arch_v2_c1.py', 'FIX')
NET = fixture('test_arch_v2_batch_a.py', 'FIXTURE')
MODULES = ['Lv3Effects', 'NetworkBoost', 'CopyYields', 'CommerceConvergence', 'StandardizationDiscount']
ADAPT = r'''
propertyWrites=0;ledgerReads=0;queryCalls=0;stopped=false
shared.NetworkIsolation={Active=function(pid) return stopped and (pid==nil or pid==0) end}
Game.SetProperty=function() propertyWrites=propertyWrites+1;error('PERMANENT_WRITE_FORBIDDEN') end
for _,c in pairs(cities) do c.SetProperty=Game.SetProperty end
-- Ordinary buildings and unrelated local carriers are deliberate sentinels.
function sentinels(c)
 c.built.BUILDING_LIBRARY=true;c.built.BUILDING_SPC_UNRELATED_SENTINEL=true
 c.built.BUILDING_SPC_DEV_LV3_POP_CULTURE_7=true
end
function assertSentinels()
 for _,c in pairs(cities) do
  assert(c.built.BUILDING_LIBRARY and c.built.BUILDING_SPC_UNRELATED_SENTINEL,'UNRELATED_REMOVED')
  assert(c.built.BUILDING_SPC_DEV_LV3_POP_CULTURE_7,'LOCAL_CULTURE_REMOVED')
 end
 assert(propertyWrites==0,'PERMANENT_WRITE_OCCURRED')
end
function carriers()
 local out={}
 if moduleName=='Lv3Effects' then
  for _,k in ipairs({'RESEARCH','CULTURE','INDUSTRY'}) do out[#out+1]='BUILDING_SPC_DEV_LV3_COM_'..k end
 elseif moduleName=='NetworkBoost' then
  for _,r in pairs(SPCBoostConfig.rows) do out[#out+1]=r.building end
  for _,id in pairs(SPCBoostIntegerConfig.rows) do out[#out+1]=id end
  for _,k in ipairs({'RESEARCH','CULTURE'}) do for _,n in ipairs({2,4}) do out[#out+1]='BUILDING_SPC_B057_'..k..'_'..n end end
 elseif moduleName=='CopyYields' then
  for _,m in ipairs({'POS','NEG','POP'}) do for bit=0,(m=='POP' and 7 or 15) do out[#out+1]='BUILDING_SPC_B051_PRODUCTION_'..m..'_'..bit end end
 elseif moduleName=='CommerceConvergence' then
  for _,y in ipairs({'SCIENCE','CULTURE','PRODUCTION'}) do for bit=0,15 do out[#out+1]='BUILDING_SPC_B061_'..y..'_'..bit end end
 else
  for i=1,4 do out[#out+1]=100+i end
 end
 table.sort(out);return out
end
function seedOwned()
 owned=carriers();for _,c in pairs(cities) do for _,id in ipairs(owned) do c.built[id]=true end;sentinels(c) end
end
function assertCleared()
 for _,c in pairs(cities) do for _,id in ipairs(owned) do assert(c.built[id]==nil,'RESIDUAL '..id) end end
 assertSentinels()
end
'''
C2_ADAPT = r'''
local originalInfo=P.Info;indexByName={};nameByIndex={};nextIndex=1000
P.Info=function(t,k)
 if t=='Buildings' then
  if type(k)=='number' then return {Index=k,BuildingType=nameByIndex[k]} end
  if not indexByName[k] then nextIndex=nextIndex+1;indexByName[k]=nextIndex;nameByIndex[nextIndex]=k end
  return {Index=indexByName[k],BuildingType=k}
 end
 return originalInfo(t,k)
end
local has,create,remove=P.HasBuilding,P.CreateBuilding,P.RemoveBuilding
P.HasBuilding=function(b,i) return has(b,nameByIndex[i] or i) end
P.CreateBuilding=function(b,i) return create(b,nameByIndex[i] or i) end
P.RemoveBuilding=function(b,i) return remove(b,nameByIndex[i] or i) end
Players[0].GetCities=function() return {Members=function() return pairs(cities) end,FindID=function(_,id) return cities[id] end,GetCapitalCity=function() return cities[1] end} end
for _,c in pairs(cities) do c.GetYield=function() return 25 end end
Map.GetPlot=function(x,y) return {GetAdjacencyYield=function() return districts[x].base end,GetWorkerCount=function() return districts[x].workers or 2 end} end
shared.NetworkBridge.ready=true
shared.NetworkBridge.Verified=function() return true end
shared.NetworkBridge.players[0].routes={{op=0,oc=1,dp=0,dc=2}}
shared.NetworkBridge.National=function() queryCalls=queryCalls+1;return {RESEARCH={n=2,level=4,sources={[1]=4}},CULTURE={n=1,level=3,sources={[2]=3}}} end
shared.NetworkBridge.ConnectedKinds=function() queryCalls=queryCalls+1;return {RESEARCH=true,CULTURE=true,INDUSTRY=true} end
local src=shared.NetworkBridge.RecipientSources
shared.NetworkBridge.RecipientSources=function(...) queryCalls=queryCalls+1;return src(...) end
function samples()
 local rows={};for key,r in pairs(SPCSampleLifecycle.Live(P,0,false)) do rows[key]={cityID=r.cityID,id=r.id,type=r.type,reference=r.reference,total=6,production=6,value=6} end
 d.samples[0]={turn=turn,rows=rows,signature='fixture'}
end
function choose(kind,active)
 local types={RESEARCH='DISTRICT_CAMPUS',CULTURE='DISTRICT_THEATER',INDUSTRY='DISTRICT_INDUSTRIAL_ZONE',COMMERCE='DISTRICT_COMMERCIAL_HUB'}
 facts[1]={specialization=kind,potential=4,active=active,first={districtID=11,type=types[kind]}}
 districts[11].kind=types[kind]
end
'''


def consumer(name, old=False):
    lua = runtime(C1 if name == 'StandardizationDiscount' else C2, old)
    lua.globals().moduleName = name
    # C1 intentionally uses a bounded fixed catalog rather than reading native DB.
    if name == 'StandardizationDiscount':
        lua.globals().include = lambda n: None if n == 'StandardizationCatalog' else lua.execute(source(n, old))
    lua.execute(ADAPT)
    if name == 'StandardizationDiscount':
        lua.execute("for i=1,4 do local k='BUILDING_SPC_B054_TEST_'..i;rows[k].BuildingType=k;rows[100+i]=rows[k] end")
    if name != 'StandardizationDiscount':
        lua.execute(C2_ADAPT)
    lua.execute(source(name, old))
    lua.execute(f'SPC{name}.Start(P,shared);d=shared.{name};d.ready=true')
    if name == 'CopyYields':
        lua.execute('samples()')
    return lua


# Every exact consumer-owned ID: seed without any in-memory applied map as on load.
for name in MODULES:
    l = consumer(name)
    l.execute("seedOwned();local n=writes;assert(not pcall(d.ExperimentalNetworkWithdraw,0) and writes==n,'UNARMED_WITHDRAWAL')")
    l.execute('seedOwned();stopped=true;assert(d.ExperimentalNetworkWithdraw(0)==true);assertCleared();local n=writes;assert(d.ExperimentalNetworkWithdraw(0)==true);assert(writes==n);assertCleared()')
    COUNTS[name + '_owned_ids'] = len(list(l.globals().owned.values()))
    for failure in ['unknown_presence', 'remove_unconfirmed', 'missing_city_list']:
        l = consumer(name)
        l.execute("seedOwned();stopped=true;bad=type(owned[1])=='number' and owned[1] or P.Info('Buildings',owned[1]).Index")
        if failure == 'unknown_presence':
            l.execute("local h=P.HasBuilding;P.HasBuilding=function(b,id) if id==bad then return nil end;return h(b,id) end")
        elif failure == 'remove_unconfirmed':
            l.execute("local r=P.RemoveBuilding;P.RemoveBuilding=function(b,id) if id~=bad then r(b,id) end end")
        else:
            l.execute('Players[0].GetCities=function() return nil end')
        l.execute("local ok=pcall(d.ExperimentalNetworkWithdraw,0);assert(not ok,'FAILURE_REPORTED_SUCCESS');assert(not d.busy,'BUSY_LEFT_SET');assertSentinels()")
    # Source/fact UNKNOWN must not be consulted for exact experimental exit.
    l = consumer(name)
    l.execute("seedOwned();stopped=true;shared.EffectiveFacts.Read=function() error('FACT_READ_FORBIDDEN') end;shared.NetworkBridge=setmetatable({},{__index=function() error('NETWORK_READ_FORBIDDEN') end});assert(d.ExperimentalNetworkWithdraw(0)==true);assertCleared()")

# Normal behavior remains byte-for-byte output equivalent to accepted B136 source.
for name in MODULES:
    a,b=consumer(name,True),consumer(name)
    cases = [('RESEARCH',4),('CULTURE',3),('COMMERCE',4),('INDUSTRY',1)]
    for seq,(kind,level) in enumerate(cases,1):
        if name == 'StandardizationDiscount':
            code=f"cities[1].active={level};d.EnsureReady(0);d.MarkDirty(0,'test');d.Audit();ExposedMembers.SPC_DiscountClientEpoch=1;d.Receive(0,packet({seq},'2,1,1;3,1,1;4,1,1'))"
            for lua in [a,b]: lua.execute(code)
            assert [a.eval(f'rate({i})') for i in range(1,5)] == [b.eval(f'rate({i})') for i in range(1,5)], name
        else:
            for lua in [a,b]: lua.execute(f"choose('{kind}',{level});d.Audit()")
            assert a.eval('output()') == b.eval('output()'), (name,kind,level)
    COUNTS[name+'_normal_comparisons']=len(cases)

# Mixed consumer retains/recomputes local Culture while Commerce network stays off.
l=consumer('Lv3Effects')
l.execute("choose('CULTURE',4);d.Audit();assert(cities[1].built.BUILDING_SPC_DEV_LV3_POP_CULTURE_1);stopped=true;d.ExperimentalNetworkWithdraw(0);districts[11].workers=3;d.Audit();assert(cities[1].built.BUILDING_SPC_DEV_LV3_POP_CULTURE_0 and cities[1].built.BUILDING_SPC_DEV_LV3_POP_CULTURE_1);choose('COMMERCE',4);local q=queryCalls;d.Audit();assert(queryCalls==q);for _,id in ipairs(carriers()) do assert(not cities[1].built[id]) end;assert(propertyWrites==0)")
COUNTS['culture_local_recomputed']=1




def network(old=False):
    l=runtime(NET,old)
    l.execute("shared.Version=P.VERSION;ExposedMembers.SPC_P0=shared;Game.GetLocalPlayer=function() return 0 end;Game.SetProperty=function() propertyWrites=propertyWrites+1;error('PERMANENT_WRITE_FORBIDDEN') end;exits={};returns={};shared.CityProgressionStore={RegisterExit=function(n,f) exits[n]=f end,RegisterReturn=function(n,f) returns[n]=f end,IsExitTarget=function() return true end}")
    l.execute(source('NetworkBridge',old))
    l.execute('SPCNetworkBridge.Start(P,shared);net=shared.NetworkBridge;net.ready=true')
    return l


def coordinator():
    l=network()
    l.execute(r'''
 calls={};dispatches=0
 for _,name in ipairs({'Lv3Effects','NetworkBoost','CopyYields','CommerceConvergence','StandardizationDiscount'}) do
  shared[name]={busy=false,Audit=function() dispatches=dispatches+1 end,
   ExperimentalNetworkWithdraw=function(pid) calls[name]=(calls[name] or 0)+1;if failModule==name then error('MOCK_REMOVE_UNKNOWN') end;return true end}
 end
 function acknowledgments()
  for _,key in ipairs({'SPC_P0_BackgroundRoutes','SPC_CopyBackground','SPC_DiscountEligibility'}) do
   ExposedMembers[key]={networkStopped=true,networkStopEpoch=net.epoch,version=P.VERSION}
  end
 end
 function sumCalls() local n=0;for _,v in pairs(calls) do n=n+v end;return n end
 ''')
    l.execute(source('NetworkIsolation'))
    l.execute('SPCNetworkIsolation.Start(P,shared);iso=shared.NetworkIsolation')
    return l

# Existing nonzero accepted route output and UNKNOWN holds match B136.
a,b=network(True),network()
for code in ["send('0,1,0,2,10;0,2,0,3,11;0,4,0,2,12',3)",
             "cities[1].active=4;Events.GovernorPromoted.Fire(0)",
             "readFail=true;net.Rebuild()",
             "readFail=false;send('EMPTY',0)"]:
    for l in [a,b]:l.execute(code)
    assert a.eval('output()')==b.eval('output()'),code
COUNTS['network_normal_comparisons']=4

# All preflight failures are explicit, leave normal Gameplay state untouched.
for setup,epoch in [('', 'net.epoch'),('acknowledgments()', 'net.epoch+1'),
    ('acknowledgments();shared.CopyYields.busy=true','net.epoch'),
    ('acknowledgments();shared.CopyYields=nil','net.epoch'),
    ('acknowledgments();net.ready=false','net.epoch'),
    ("acknowledgments();ExposedMembers.SPC_CopyBackground.version='OLD'",'net.epoch'),
    ('acknowledgments();ExposedMembers.SPC_CopyBackground.networkStopEpoch=999','net.epoch')]:
    l=coordinator();l.execute(setup)
    l.execute(f"assert(not pcall(iso.Begin,0,{epoch}));assert(not iso.Active() and iso.phase=='NORMAL' and sumCalls()==0 and propertyWrites==0)")
COUNTS['coordinator_preflight_refusals']=7

# Stop after a valid nonzero network, then invoke every direct and event route.
l=coordinator()
l.execute(r'''
send('0,1,0,2,10;0,2,0,3,11;0,4,0,2,12',3)
local nativeCapture=SPCNetworkInput.Capture;captures=0
SPCNetworkInput.Capture=function(...) captures=captures+1;return nativeCapture(...) end
acknowledgments();local published=ExposedMembers.SPC_Performance.entries.input_publication.total
local derived=ExposedMembers.SPC_Performance.entries.derive_executed.total;local notified=dispatches
local text=iso.Begin(0,net.epoch)
assert(iso.phase=='READY' and iso.completed==5 and iso.Active(0) and iso.Active() and not iso.Active(1))
assert(sumCalls()==5 and captures==0 and propertyWrites==0 and text:find('READY'))
assert(net.players[0].routes==nil and net.players[0].input==nil and net.players[0].sources==nil and net.players[0].validity=='EXPERIMENT_ISOLATED')
for _,read in ipairs({function() return net.CurrentNational(0) end,function() return net.National(0) end,
 function() return net.CurrentConnectedKinds(0,cities[2]) end,function() return net.ConnectedKinds(0,cities[2]) end,
 function() return net.CurrentRecipientSources(0,cities[3],'RESEARCH') end,function() return net.RecipientSources(0,cities[3],'RESEARCH') end,
 function() return net.DiscountBatch(0) end}) do assert(not pcall(read),'STOPPED_VIEW_ESCAPED') end
for _,event in ipairs({'PlayerTurnActivated','GovernorChanged','GovernorPromoted','GovernorAssigned','GovernorEstablished','CapitalCityChanged','CityAddedToMap','TradeRouteActivityChanged','TradeRouteRemovedFromMap','UnitRemovedFromMap','CityRemovedFromMap','CityTransfered','DiplomacyDeclareWar','LoadScreenClose'}) do Events[event].Fire(0) end
GameEvents.CityBuilt.Fire(0);GameEvents.OnDistrictConstructed.Fire(0)
turn=turn+1;send('0,1,0,2,10',1);net.Refresh(0);net.Rebuild();net.CheckEvidence(true)
assert(net.Verified(0)==false);net.Read(0,cities[2]);net.Read(0,cities[2],true)
exits.NetworkBridge(cities[1],{origin={owner=0,cityID=1}});returns.NetworkBridge(0)
assert(captures==0 and dispatches==notified and propertyWrites==0)
assert(ExposedMembers.SPC_Performance.entries.input_publication.total==published)
assert(ExposedMembers.SPC_Performance.entries.derive_executed.total==derived)
iso.Begin(0,net.epoch);assert(sumCalls()==5 and iso.phase=='READY','SAME_SESSION_RETRY_OR_REOPEN')
local read=iso.Read(0);assert(read:find('可观察') and read:find('原存档'))
P.Count('route_scan');assert(iso.Read(0):find('停止对照'),'COUNTER_DRIFT_NOT_REPORTED')
''')
COUNTS['bridge_stopped_ingress_queries_events']=1

for failed in MODULES:
    l=coordinator();l.globals().failModule=failed
    l.execute("acknowledgments();iso.Begin(0,net.epoch);assert(iso.phase=='FAILED' and iso.completed==4 and iso.Active(0));assert(sumCalls()==5);failModule=nil;iso.Begin(0,net.epoch);assert(iso.phase=='FAILED' and sumCalls()==5 and propertyWrites==0);assert(iso.Read(0):find('停止对照'))")
COUNTS['coordinator_partial_failure_no_retry']=5

# A separate clean context recreates normal mode; no same-session restore API.
l=coordinator();l.execute("assert(iso.phase=='NORMAL' and not iso.Active());send('0,1,0,2,10',1);assert(net.CurrentNational(0).RESEARCH.n>0 and sumCalls()==0 and propertyWrites==0)")
assert 'function d.Restore' not in source('NetworkIsolation')
COUNTS['fresh_session_default_normal']=1



def ui_consumer(name, old=False):
    l=consumer(name,old)
    l.globals().include=lambda n: None if n in ['Probe','StandardizationCatalog','DiagnosticLog'] else l.execute(source(n,old))
    l.execute('shared.NetworkBridge.epoch=77;shared.NetworkBridge.ready=true')
    if name=='StandardizationDiscount':l.execute('d.EnsureReady(0)')
    ui='UI/CopyYieldRefresh' if name=='CopyYields' else 'UI/DiscountEligibility'
    l.execute(source(ui,old))
    return l,ui,'SPC_CopyBackground' if name=='CopyYields' else 'SPC_DiscountEligibility'

# Both producers leave pending sends behind before the one-way stop handshake.
for name in ['CopyYields','StandardizationDiscount']:
    l,ui,key=ui_consumer(name)
    l.globals().publicKey=key
    l.execute(r'''
 local pub=ExposedMembers[publicKey]
 assert(pub.StopNetwork(77)==false,'UNINITIALIZED_STOP_ACCEPTED')
 initUI();assert(sends==1,'PENDING_SEND_FIXTURE_MISSING');late=queue[1]
 assert(pub.StopNetwork(78)==false and not pub.networkStopped,'STALE_EPOCH_ACCEPTED')
 assert(pub.StopNetwork(77)==true and pub.StopNetwork(77)==true)
 assert(pub.networkStopped and pub.networkStopEpoch==77 and pub.version==P.VERSION)
 stopped=true;shared.NetworkIsolation.active=true;shared.NetworkIsolation.player=0;shared.NetworkIsolation.epoch=77
 d.ExperimentalNetworkWithdraw(0)
 savedWrites=writes;savedSends=sends;savedCounters={}
 for _,key in ipairs({'copy_send','copy_retry','discount_send','discount_retry','discount_ui_scan','district_scan'}) do savedCounters[key]=ExposedMembers.SPC_Performance.entries[key].total end
 for i=1,8 do turn=turn+1;tick(6);fire('GameCoreEventPublishComplete');fire('GameCoreEventPlaybackComplete');fire('SystemUpdateUI');fire('PlayerTurnActivated');fire('LoadScreenClose');fire('GovernorChanged');fire('ResourceAddedToMap');fire('ResearchCompleted') end
 d.Receive(0,late)
 assert(sends==savedSends and writes==savedWrites and propertyWrites==0,'STOPPED_PRODUCER_RESUMED')
 for key,n in pairs(savedCounters) do assert(ExposedMembers.SPC_Performance.entries[key].total==n,'STOPPED_COUNTER '..key) end
 assert(not ExposedMembers.SPC_CopyIssued and not ExposedMembers.SPC_DiscountIssued,'PENDING_ISSUED_RETAINED')
 ''')
    # Recreating only the UI context in this isolated session must auto-latch.
    l.execute(source(ui))
    l.execute("initUI();assert(ExposedMembers[publicKey].networkStopped and ExposedMembers[publicKey].networkStopEpoch==77);tick(10);fire('GameCoreEventPublishComplete');assert(sends==savedSends and writes==savedWrites)")
    # A new independent normal session reconstructs the original sample flow.
    a,_,_=ui_consumer(name,True);b,_,_=ui_consumer(name)
    for q in [a,b]:q.execute('sync=true;initUI();pulse();turn=turn+1;pulse()')
    assert a.eval('sends')==b.eval('sends'),name
    if name=='CopyYields':assert a.eval('output()')==b.eval('output()')
    else:assert [a.eval(f'rate({i})') for i in range(1,5)]==[b.eval(f'rate({i})') for i in range(1,5)]
    COUNTS[name+'_ui_stop_recreate_normal']=1


def first_literal_execute(filename,var):
    tree=ast.parse((ROOT/'DevelopmentTests'/filename).read_text())
    for n in tree.body:
        if isinstance(n,ast.Expr) and isinstance(n.value,ast.Call):
            c=n.value
            if (isinstance(c.func,ast.Attribute) and c.func.attr=='execute'
                and isinstance(c.func.value,ast.Name) and c.func.value.id==var
                and c.args and isinstance(c.args[0],ast.Constant)):
                return ast.literal_eval(c.args[0])
    raise AssertionError('Fixture not found')


def background(old=False):
    l=LuaRuntime(unpack_returned_tuples=True)
    l.globals().include=lambda n: l.execute(source(n,old))
    l.execute(source('Probe',old));l.execute(source('ShadowRouteState',old))
    l.execute(first_literal_execute('test_background_routes.py','lua'))
    l.execute(source('PerformanceCounters',old))
    l.execute(source('NetworkSender',old))
    l.execute(r'''
 P=SPCP0;P.IsTestPlayer=function(pid) return pid==0 end
 ExposedMembers.SPC_Performance=SPCPerformance.New();P.Count=SPCPerformance.Count
 packets={};PlayerOperations={EXECUTE_SCRIPT=1}
 UI={RequestPlayerOperation=function(pid,op,p) packets[#packets+1]=p end}
 ExposedMembers.SPC_P0.NetworkBridge={epoch=77,ready=true,players={}}
 ''')
    l.execute(source('UI/BackgroundRoutes',old))
    return l

l=background()
l.execute(r'''
ContextPtr:init();assert(s().status=='COMPLETE_UI_SHADOW' and s().snapshot.count==0 and #packets==1)
local pub=s();assert(pub.StopNetwork(78)==false and pub.StopNetwork(77)==true)
assert(pub.networkStopped and pub.networkStopEpoch==77 and pub.version==P.VERSION)
assert(pub.snapshot==nil and pub.ReadNormalizedRoutes().status=='UNKNOWN' and not pub.awaitingNetwork)
ExposedMembers.SPC_P0.NetworkIsolation={active=true,player=0,epoch=77}
savedReads=reads;savedPackets=#packets;local generation=pub.generation;beforeCounters={}
for _,k in ipairs({'route_scan','net_send','city_scan','unit_cb'}) do beforeCounters[k]=ExposedMembers.SPC_Performance.entries[k].total end
for i=1,8 do
 turn=turn+1
 for name,event in pairs(Events) do event.Fire(0,1) end
end
assert(reads==savedReads and #packets==savedPackets and pub.generation==generation,'STOPPED_BACKGROUND_RESUMED')
assert(ExposedMembers.SPC_Performance.inflight==0)
for k,n in pairs(beforeCounters) do assert(ExposedMembers.SPC_Performance.entries[k].total==n,'BACKGROUND_COUNTER '..k) end
ContextPtr:shutdown()
''')
l.execute(source('UI/BackgroundRoutes'))
l.execute("ContextPtr:init();assert(s().networkStopped and s().networkStopEpoch==77 and s().snapshot==nil);Events.LoadScreenClose.Fire();assert(reads==savedReads and #packets==savedPackets)")
a,b=background(True),background()
for q in [a,b]:q.execute("ContextPtr:init();outgoing[1]={route(10,1,2)};count=1;Events.TradeRouteActivityChanged.Fire();Events.GameCoreEventPublishComplete.Fire()")
assert a.eval('reads')==b.eval('reads') and a.eval('#packets')==b.eval('#packets')
assert a.eval('s().snapshot.fingerprint')==b.eval('s().snapshot.fingerprint')
COUNTS['background_ui_stop_recreate_normal']=1


# One real coordinator + real Bridge + all five real consumers in one context.
# This owns a small explicit catalog; the test does not infer native DB support.
l=runtime(C2)
l.execute(ADAPT);l.execute(C2_ADAPT)
l.execute("SPCStandardizationCatalog={Build=function() return {buildings={TEST={enabled=true,group='T1',name='Test'}}} end}")
l.globals().include=lambda n: None if n=='StandardizationCatalog' else l.execute(source(n))
for name in MODULES:
    l.execute(source(name));l.execute(f'SPC{name}.Start(P,shared);shared.{name}.ready=true')
l.execute(source('NetworkBridge'));l.execute('SPCNetworkBridge.Start(P,shared);net=shared.NetworkBridge;net.ready=true')
l.execute(source('NetworkIsolation'));l.execute('SPCNetworkIsolation.Start(P,shared);iso=shared.NetworkIsolation')
l.execute(r'''
allOwned={}
for _,name in ipairs({'Lv3Effects','NetworkBoost','CopyYields','CommerceConvergence','StandardizationDiscount'}) do
 moduleName=name;local ids=carriers()
 if name=='StandardizationDiscount' then ids={};for i=1,4 do ids[#ids+1]='BUILDING_SPC_B054_TEST_'..i end end
 for _,id in ipairs(ids) do allOwned[#allOwned+1]=id;for _,c in pairs(cities) do c.built[id]=true;sentinels(c) end end
end
for _,key in ipairs({'SPC_P0_BackgroundRoutes','SPC_CopyBackground','SPC_DiscountEligibility'}) do ExposedMembers[key]={version=P.VERSION,networkStopped=true,networkStopEpoch=net.epoch} end
local s=iso.Begin(0,net.epoch);assert(iso.phase=='READY' and iso.completed==5,s)
for _,c in pairs(cities) do for _,id in ipairs(allOwned) do assert(c.built[id]==nil,'INTEGRATED_RESIDUAL '..id) end end
assertSentinels();local w=writes
iso.Begin(0,net.epoch);assert(writes==w and iso.phase=='READY' and propertyWrites==0)
''')
COUNTS['real_bridge_coordinator_five_consumers']=1

# A bridge stop failure is also terminal for this session, even if exits finish.
l=coordinator();l.execute("acknowledgments();net.ExperimentalStop=function() error('BRIDGE_FAILED') end;iso.Begin(0,net.epoch);assert(iso.phase=='FAILED' and iso.completed==5 and iso.Active(0));iso.Begin(0,net.epoch);assert(sumCalls()==5)")
COUNTS['bridge_stop_failure_terminal']=1

# Mode fields are in memory only; running the experiment produces no save write.
for name in ['NetworkIsolation','UI/BackgroundRoutes','UI/CopyYieldRefresh','UI/DiscountEligibility']:
    assert 'SetProperty(' not in source(name),name
assert 'collectgarbage(' not in source('NetworkIsolation')
# Mixed Culture/Commerce writer must not retry failed network carrier removal.
l=consumer('Lv3Effects')
l.execute("choose('CULTURE',4);seedOwned();stopped=true;local remove=P.RemoveBuilding;local bad=P.Info('Buildings',owned[1]).Index;P.RemoveBuilding=function(b,id) if id~=bad then remove(b,id) end end;assert(not pcall(d.ExperimentalNetworkWithdraw,0));P.RemoveBuilding=remove;local retained=owned[1];assert(cities[1].built[retained]);districts[11].workers=3;d.Audit();assert(cities[1].built[retained],'FAILED_NETWORK_EXIT_RETRIED');assert(cities[1].built.BUILDING_SPC_DEV_LV3_POP_CULTURE_0 and cities[1].built.BUILDING_SPC_DEV_LV3_POP_CULTURE_1)")
COUNTS['mixed_consumer_failed_exit_no_retry']=1


# Execute actual early Gameplay dispatch without booting unrelated modules.
l=coordinator()
l.execute('savedShared=shared;SPCP0=P;P.Scalar=tostring;include=function() end')
prefix=source('Gameplay').split("  if params.Action=='MEMORY_GC_READ'",1)[0]
l.execute(prefix+'\nend\nrequestB137=request;requestShared=shared')
l.execute(r'''
requestShared.NetworkIsolation=savedShared.NetworkIsolation
requestB137(0,{Action='NETWORK_ISOLATION_READ',Token='read'});assert(sumCalls()==0 and not iso.Active() and requestShared.LastToken=='read')
requestB137(0,{Action='NETWORK_ISOLATE',Token='early',Epoch=net.epoch});assert(sumCalls()==0 and requestShared.Snapshot:find('未就绪'))
acknowledgments();requestB137(0,{Action='NETWORK_ISOLATE',Token='stop',Epoch=net.epoch})
assert(sumCalls()==5 and iso.phase=='READY' and requestShared.LastToken=='stop')
requestB137(0,{Action='NETWORK_ISOLATE',Token='stop',Epoch=net.epoch});assert(sumCalls()==5)
requestB137(1,{Action='NETWORK_ISOLATE',Token='foreign',Epoch=net.epoch});assert(sumCalls()==5 and requestShared.FailureAt=='PLAYER_ELIGIBILITY')
requestShared.NetworkIsolation=nil;requestB137(0,{Action='NETWORK_ISOLATION_READ',Token='absent'});assert(requestShared.Snapshot:find('未就绪'))
assert(propertyWrites==0)
''')
COUNTS['actual_gameplay_request_ingress']=1

# Actual panel request closure: city-free reads, all-three UI stop before dispatch,
# failed handshake sends nothing, waiting for an ACK never retries this action.
UI_PREFIX=source('UI/P0Panel').split('local function legacyCopy',1)[0]
for failure in [False,True]:
    l=runtime(C2)
    l.execute(r'''
 include=function() end;P.Scalar=tostring;SPCP0=P
 SPCCityIdentityEvidence={New=function() return {} end}
 SPCOverflowStorageRead={New=function() return {Pulse=function() end} end}
 Controls={Status={SetText=function(_,s) statusText=s end}}
 shared.NetworkBridge.epoch=77;shared.NetworkBridge.ready=true
 stopCalls={};packets={}
 UI.GetHeadSelectedCity=function() error('CITY_SELECTION_NOT_REQUIRED') end
 UI.RequestPlayerOperation=function(pid,op,p)
  if p.Action=='NETWORK_ISOLATE' then assert(#stopCalls==3,'DISPATCH_BEFORE_ALL_STOPS') end
  packets[#packets+1]=p
 end
 for _,key in ipairs({'SPC_P0_BackgroundRoutes','SPC_CopyBackground','SPC_DiscountEligibility'}) do
  ExposedMembers[key]={StopNetwork=function(epoch) assert(epoch==77);stopCalls[#stopCalls+1]=key;return not (failHandshake and #stopCalls==2) end}
 end
 ''')
    l.globals().failHandshake=failure
    l.execute(UI_PREFIX+'\nrequestPanelB137=request')
    l.execute("requestPanelB137('NETWORK_ISOLATION_READ');assert(#packets==1 and #stopCalls==0 and packets[1].CityID==nil);requestPanelB137('NETWORK_ISOLATE')")
    if failure:
        l.execute("assert(#packets==1 and #stopCalls==2 and statusText:find('冷启动原存档'))")
    else:
        l.execute("assert(#packets==2 and #stopCalls==3 and packets[2].Epoch==77 and packets[2].CityID==nil);for i=1,3 do tick(11) end;assert(#packets==2,'ISOLATION_REQUEST_RETRIED')")
COUNTS['actual_panel_request_handshake']=2

print(json.dumps({'scope':'B137_LOCAL_SIMULATION_PASS','checks':COUNTS},sort_keys=True))
