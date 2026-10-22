"""B135 targeted real-entrypoint simulation. No game/DB/deployment or stress run.
Requires Lupa lua55 and Git baseline d26f3f9. Reuses only existing Cross fixtures.
"""
from pathlib import Path
import ast
import subprocess
import xml.etree.ElementTree as ET
from lupa.lua55 import LuaRuntime

R = Path(__file__).resolve().parents[1]
M = R / 'Mod'
BASELINE = 'd26f3f9'

def ui_runtime():
    l = LuaRuntime(unpack_returned_tuples=True)
    l.execute('''
    include=function()end;print=function()end;localPlayer=4;turn=1;hooks={};packets={}
    Game={GetLocalPlayer=function()return localPlayer end,GetCurrentGameTurn=function()return turn end}
    Events=setmetatable({},{__index=function(t,k)
      local e={Add=function(f)hooks[k]=f end,Remove=function(f)assert(hooks[k]==f);hooks[k]=nil end};t[k]=e;return e
    end})
    function fire(n,pid)if hooks[n]then hooks[n](pid)end end
    function pulse()fire('GameCoreEventPublishComplete')end
    SPCP0={VERSION='B135',Field=function(o,k)return o[k]end,IsTestPlayer=function(p)return p==4 end}
    ExposedMembers={SPC_P0={Version='B135',Lv2GPP={ready=true}}}
    ContextPtr={SetInitHandler=function(_,f)init=f end,SetShutdown=function(_,f)close=f end}
    PlayerOperations={EXECUTE_SCRIPT=1}
    UI={RequestPlayerOperation=function(pid,op,p)
      assert(pid==4 and op==1);packets[#packets+1]=p
      if during then local f=during;during=nil;f()end
      if fail then error('transport failure')end
    end}
    function last(facts,workers)
      local p=packets[#packets];assert(p.FactsChanged==facts and p.WorkerOnly==workers)
    end
    ''')
    l.execute((M / 'UI/GPPRefresh.lua').read_text())
    l.execute('init();last(true,false)')
    return l

l=ui_runtime()
l.execute('''
local n=#packets;for i=1,8 do pulse();fire('SystemUpdateUI')end;assert(#packets==n)
fire('CityWorkerChanged',4);fire('CityFocusChanged',4);pulse();last(false,true);assert(#packets==n+1)
fire('CityWorkerChanged',0);fire('CityFocusChanged',3);pulse();assert(#packets==n+1)
close();assert(next(hooks)==nil)
''')
for owner in ['nil', "'4'", '-1', '4.5', '0/0', 'math.huge', '-math.huge', 'false']:
    for event in ['CityWorkerChanged', 'CityFocusChanged']:
        l=ui_runtime();l.execute(f"fire('{event}',{owner});pulse();last(false,false);assert(#packets==2)")
for mixed in ["fire('GovernorAssigned',4)", "fire('CityWorkerChanged')",
              "fire('PlayerTurnActivated',4)", "fire('LoadScreenClose')"]:
    for order in [0,1]:
        l=ui_runtime()
        # Not-ready bridge allows both orders to coalesce before dispatch.
        l.execute('ExposedMembers.SPC_P0.Lv2GPP.ready=false')
        worker="fire('CityWorkerChanged',4)"
        l.execute(';'.join([worker,mixed] if order==0 else [mixed,worker]))
        l.execute('ExposedMembers.SPC_P0.Lv2GPP.ready=true;pulse();assert(#packets==2)')
        l.execute('last('+('true' if 'Governor' in mixed else 'false')+',false)')
l=ui_runtime();l.execute('''
fire('PlayerTurnActivated',4);last(false,false)
fire('CityWorkerChanged',4);fire('LoadScreenClose');pulse();last(false,false)
fire('CityWorkerChanged',4);fire('PlayerTurnActivated',4);pulse();last(false,false)
local n=#packets;fire('PlayerTurnActivated',4);fire('LoadScreenClose');pulse();assert(#packets==n)
fire('CityWorkerChanged',4);pulse();last(false,true)
turn=2;fire('PlayerTurnActivated',4);last(false,false)
''')
# Failure bounded to three attempts; new real event retains original retry behavior.
l=ui_runtime();l.execute('''
fail=true;fire('CityWorkerChanged',4);for i=1,6 do pulse()end
assert(#packets==4);last(false,true)
fail=false;pulse();assert(#packets==4)
fire('GovernorChanged',4);pulse();assert(#packets==5);last(true,false)
''')
for failure in [False,True]:
    for first,second in [('CityWorkerChanged','GovernorChanged'),('GovernorChanged','CityWorkerChanged'),
                         ('CityWorkerChanged','LoadScreenClose')]:
        l=ui_runtime();l.execute("fire('PlayerTurnActivated',4)")
        l.execute(f"fail={str(failure).lower()};during=function()fire('{second}',4);pulse()end;fire('{first}',4);pulse()")
        # Nested pulse cannot dispatch while busy. Latest cause survives success or merges on failure.
        assert l.eval('#packets')==3
        l.execute('fail=false;pulse();assert(#packets==4)')
        expected_facts = second=='GovernorChanged' or (failure and first=='GovernorChanged')
        expected_workers = second=='CityWorkerChanged' and not failure
        l.execute(f'last({str(expected_facts).lower()},{str(expected_workers).lower()})')
        l.execute('local n=#packets;pulse();assert(#packets==n)')
print('PASS UI provenance: nonzero local owner, malformed/foreign, bidirectional coalescing, turn/load fallback, bounded retry, synchronous reentry, idle/shutdown')

def branch(source):
    return source[source.index('  if params.Action=="LV2_GPP_DIRTY" then'):source.index('  if params.Action=="NETWORK_PUSH" then')]
old_source=subprocess.check_output(['git','show',BASELINE+':Mod/Gameplay.lua'],cwd=R,text=True)
new_source=(M/'Gameplay.lua').read_text()
old,new=branch(old_source),branch(new_source)
# Only the intended branch changed: investment/Claim/ownership/direct request dispatch remains identical.
assert old_source.replace(old,'GPP_BRANCH')==new_source.replace(new,'GPP_BRANCH')
for params,skip in [("{FactsChanged=false,WorkerOnly=true}",True),
                    ("{FactsChanged=false}",False),("{}",False),
                    ("{FactsChanged=true,WorkerOnly=true}",False),
                    ("{WorkerOnly=true}",False),
                    ("{FactsChanged=false,WorkerOnly=false}",False),
                    ("{FactsChanged=false,WorkerOnly=1}",False),
                    ("{FactsChanged=false,WorkerOnly='true'}",False),
                    ("{FactsChanged=0,WorkerOnly=true}",False),
                    ("{FactsChanged='false',WorkerOnly=true}",False)]:
    results=[]
    for code in [old,new]:
        l=LuaRuntime();l.execute('''
        P={IsTestPlayer=function(p)return p==4 end,Observe=function()end};counts={};shared={}
        for _,n in ipairs({'Lv2Housing','Lv2GPP','Lv3Effects','Lv4Percent','ResearchInfrastructure','ResearchCross','ResearchApply','ResearchChair'})do
          shared[n]={Audit=function(s)assert(s.player==4);counts[n]=(counts[n]or 0)+1 end}
        end
        shared.NetworkBridge={Refresh=function(p)counts.network=(counts.network or 0)+1 end}
        ''')
        l.execute('function dispatch(playerID,params)\n'+code+'\nend')
        l.execute('local p='+params+";p.Action='LV2_GPP_DIRTY';dispatch(4,p)")
        results.append(dict(l.globals().counts.items()))
    expected=results[0].copy()
    if skip: expected.pop('ResearchCross')
    assert results[1]==expected,(params,results)
print('PASS real Gameplay dispatch: only exact true/false pair skips Cross; all other consumer counts identical to B134; other action branches byte-identical')

# Reuse declarations only, without running historical stress/DB/stamp assertions.
p=R/'DevelopmentTests/test_research_cross.py';tree=ast.parse(p.read_text());prefix=[]
for node in tree.body:
    prefix.append(node)
    if isinstance(node,ast.FunctionDef) and node.name=='runtime':break
ns={'__file__':str(p)};exec(compile(ast.Module(body=prefix,type_ignores=[]),str(p),'exec'),ns)
l=ns['runtime']();l.execute('sync=true;initUI();pulse();crossCalls=0;carrierReads=0;factsReads=0;P.Observe=function(k,n)if k=="audit" and n=="ResearchCross"then crossCalls=crossCalls+1 end end')
l.execute('''
local read=P.HasBuilding;P.HasBuilding=function(...)carrierReads=carrierReads+1;return read(...)end
local factsRead=shared.EffectiveFacts.Read;shared.EffectiveFacts.Read=function(...)factsReads=factsReads+1;return factsRead(...)end
for _,n in ipairs({'Lv2Housing','Lv2GPP','Lv3Effects','Lv4Percent','ResearchInfrastructure','ResearchApply','ResearchChair'})do shared[n]={Audit=function()end}end
shared.NetworkBridge={Refresh=function()end}
''')
l.execute('function dispatch(playerID,params)\n'+new+'\nend')
l.execute('''
local w=writes
worker={Action='LV2_GPP_DIRTY',FactsChanged=false,WorkerOnly=true}
fallback={Action='LV2_GPP_DIRTY',FactsChanged=false,WorkerOnly=false}
dispatch(0,worker);assert(crossCalls==0 and carrierReads==0 and factsReads==0 and writes==w)
dispatch(0,fallback);assert(crossCalls==1 and carrierReads==86 and factsReads==2 and writes==w)
-- Same-turn independent BASE changes still apply after skipped worker notifications.
local n=crossCalls;districts[13].base=10;fire('FeatureAddedToMap');pulse()
assert(crossCalls==n+1 and d.plans[0][1].science==5)
dispatch(0,worker);districts[13].base=14;fire('ResourceAddedToMap');pulse()
assert(crossCalls==n+2 and d.plans[0][1].science==7)
-- UNKNOWN preserves current carriers; current qualification withdraws and returns normally.
w=writes;factUnknown=true;dispatch(0,fallback);assert(writes==w and d.errors[0][1])
factUnknown=false;facts[1].active=2;fire('GovernorChanged');assert(d.plans[0][1].science==0)
facts[1].active=3;fire('GovernorChanged');assert(d.plans[0][1].science==7)
-- Model late native facts: direct callback sees old facts; unchanged sample does not Audit.
fire('GovernorChanged');pulse();local n=crossCalls;facts[1].active=2
fire('GovernmentPolicyChanged');pulse();assert(crossCalls==n and d.plans[0][1].science==7)
dispatch(0,fallback);assert(d.plans[0][1].science==0)
facts[1].active=3;dispatch(0,fallback);assert(d.plans[0][1].science==7)
-- Load epoch still rejects the old packet; current-reference ambiguity cannot apply new samples.
local pkt=queue[#queue];sync=false;fire('LoadScreenClose');local a=total('cross_apply');local w=writes
d.Receive(0,pkt);assert(total('cross_apply')==a and writes==w)
pulse();d.Receive(0,queue[#queue]);pulse()
turn=turn+1;fire('PlayerTurnActivated');pulse();pkt=queue[#queue];cities[1].token='NEW'
a=total('cross_apply');d.Receive(0,pkt);assert(total('cross_apply')==a)
''')
print('PASS real Cross: pure worker 0 city/facts/carrier visits vs fallback 2 cities/86 prechecks; same-turn Science5→7, UNKNOWN hold, governor withdraw/return, late facts/UNCHANGED fallback, load/reference rejection')
# Confirm exact loss/return/Claim/Network/GC/persistence implementation remains baseline.
changed=subprocess.check_output(['git','diff','--name-only',BASELINE,'--','Mod'],cwd=R,text=True).splitlines()
assert set(changed)=={'Mod/UI/GPPRefresh.lua','Mod/Gameplay.lua','Mod/Probe.lua','Mod/SpecializationP0.modinfo'},changed
for name in ['UI/GPPRefresh.lua','Gameplay.lua','Probe.lua']:
    l.execute('assert(load(...))',(M/name).read_text())
x=ET.parse(M/'SpecializationP0.modinfo').getroot();assert x.get('version')=='162'
files=[e.text for e in x.findall('./Files/File')]
assert len(files)==len(set(files)) and set(files)=={p.relative_to(M).as_posix() for p in M.rglob('*') if p.is_file() and p.name!='SpecializationP0.modinfo'}
assert 'P.VERSION = "P0-B-135.162"' in (M/'Probe.lua').read_text()
print('PASS changed Lua syntax/modinfo162 exact file set; unchanged E2 loss/return/Claim, Network, GC and persistent writers inherit prior evidence; no native performance claim')
