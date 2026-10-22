"""Bounded update-path contracts against actual current Lua; no runtime edits.

Requires Python 3, Lupa's lua55 module, and the repository's P0-A/P0-B2/B135
fixture sources and SQL. Extracts fixture declarations with AST; never executes
historical test wrappers, Git baselines, stress cases, deployment, or game APIs.
Mock-native validation is LOCAL_SIMULATION_PASS, not a Civ VI acceptance result.
"""
from pathlib import Path
import argparse
import ast
import json
from lupa.lua55 import LuaRuntime

DEFAULT_REPO = Path(__file__).resolve().parents[1]


def fixture_through_function(path, function_name, extra=None):
    """Execute declaration prefix through a named fixture, excluding test bodies."""
    tree = ast.parse(path.read_text())
    prefix = []
    for node in tree.body:
        prefix.append(node)
        if isinstance(node, ast.FunctionDef) and node.name == function_name:
            break
    else:
        raise AssertionError(f'Fixture function missing: {path}:{function_name}')
    ns = {'__file__': str(path)}
    if extra:
        ns.update(extra)
    exec(compile(ast.Module(body=prefix, type_ignores=[]), str(path), 'exec'), ns)
    return ns


def extract_function(path, name, namespace):
    functions = [n for n in ast.parse(path.read_text()).body
                 if isinstance(n, ast.FunctionDef) and n.name == name]
    assert len(functions) == 1, (path, name)
    exec(compile(ast.Module(body=functions, type_ignores=[]), str(path), 'exec'), namespace)
    return namespace[name]


def runtime_work(mod):
    lua = LuaRuntime(unpack_returned_tuples=True)
    lua.execute('''
      turn=1;hooks={};calls={};observed=0
      Game={GetCurrentGameTurn=function()return turn end}
      Events=setmetatable({},{__index=function(t,k)
        local e={Add=function(f)hooks[k]=hooks[k]or{};table.insert(hooks[k],f)end};t[k]=e;return e
      end})
      function fire(n,...)for _,f in ipairs(hooks[n]or{})do f(...)end end
      P={Field=function(t,k)return t[k]end,Count=function()end,
        Observe=function()observed=observed+1 end,
        Info=function(t,id)
          assert(t=='Buildings')
          if id==1 then return {BuildingType='BUILDING_LIBRARY'}end
          if id==2 then return {BuildingType='BUILDING_SPC_TEST_CARRIER'}end
        end}
      function record(scope)calls[#calls+1]={scope=scope}end
      function bind(n)SPCRuntimeWork.Hook(P,Events,n,record)end
      function reset()calls={}end
      function playerAt(i,pid)return SPCRuntimeWork.Player(calls[i].scope,pid)end
    ''')
    lua.execute((mod / 'RuntimeWork.lua').read_text())
    return lua


def check_dispatch(mod):
    lua = runtime_work(mod)
    lua.execute('''
      bind('PlayerTurnActivated')
      -- Existing per-player fallback marker is independent of any other owner.
      fire('PlayerTurnActivated',7);fire('PlayerTurnActivated',7)
      fire('PlayerTurnActivated',4);fire('PlayerTurnActivated',4)
      assert(#calls==2 and playerAt(1,7) and not playerAt(1,4) and playerAt(2,4))
      turn=2;fire('PlayerTurnActivated',7);fire('PlayerTurnActivated',4)
      assert(#calls==4)
      -- No once/city/turn suppression may be imposed on actual input changes.
      reset();bind('CityWorkerChanged');bind('GovernorChanged')
      fire('CityWorkerChanged',4);fire('CityWorkerChanged',4)
      fire('GovernorChanged',4);fire('GovernorChanged',4)
      assert(#calls==4)
      for i=1,4 do assert(playerAt(i,4) and not playerAt(i,7))end
      fire('CityWorkerChanged');fire('GovernorChanged')
      assert(#calls==6 and playerAt(5,4) and playerAt(5,7) and playerAt(6,7))
      -- Public full scope remains possible for nationally dependent consumers.
      assert(SPCRuntimeWork.Player(nil,4) and SPCRuntimeWork.Player(nil,7))
      assert(SPCRuntimeWork.Player({},4) and SPCRuntimeWork.Player({},7))
      assert(SPCRuntimeWork.Player({player=4},4) and not SPCRuntimeWork.Player({player=4},7))
    ''')
    print('PASS RuntimeWork: per-player fallback, same-turn worker/governor changes, UNKNOWN and national scope')
    lua.execute('''
      reset();bind('BuildingAddedToMap');bind('BuildingRemovedFromMap')
      fire('BuildingAddedToMap',10,20,1,7)
      fire('BuildingRemovedFromMap',10,20,1,4)
      assert(#calls==2 and playerAt(1,7) and not playerAt(1,4) and playerAt(2,4))
      fire('BuildingAddedToMap',10,20,1,nil)
      fire('BuildingRemovedFromMap',10,20,1,'unreadable')
      assert(#calls==4 and playerAt(3,4) and playerAt(3,7) and playerAt(4,7))
      local n=observed;fire('BuildingAddedToMap',10,20,2,4);fire('BuildingRemovedFromMap',10,20,2,4)
      assert(#calls==4 and observed==n)
      -- Transfer arguments are not guessed as a single-player update scope.
      reset();bind('CityTransfered');bind('LoadScreenClose')
      fire('CityTransfered',7,42,4);fire('CityTransfered',4,84,7);fire('LoadScreenClose')
      assert(#calls==3)
      for i=1,3 do assert(playerAt(i,4) and playerAt(i,7))end
    ''')
    print('PASS RuntimeWork: building-owner contract, technical-carrier feedback filter, full transfer/load scope')


def check_batches(mod):
    lua = runtime_work(mod)
    lua.execute('''
      function city(pid,id)return {GetID=function()return id end,GetOwner=function()return pid end}end
      a=city(4,1);b=city(4,2);foreign=city(7,1);version=1;factReads=0;failFacts=false
      shared={EffectiveFacts={Read=function(pid,c)
        factReads=factReads+1;if failFacts then error('FACTS_UNKNOWN')end
        assert(c:GetOwner()==pid);return {owner=pid,city=c:GetID(),version=version}
      end}}
      work=SPCRuntimeWork.New(P,shared)
      local a1=work.Facts(4,a);assert(work.Facts(4,a)==a1 and factReads==1)
      local b1=work.Facts(4,b);local f1=work.Facts(7,foreign)
      assert(factReads==3 and a1~=b1 and a1~=f1 and f1.owner==7)
      -- New synchronous work must read again; no cross-batch/current-fact cache.
      version=2;nextWork=SPCRuntimeWork.New(P,shared)
      assert(nextWork.Facts(4,a).version==2 and factReads==4)
      retry=SPCRuntimeWork.New(P,shared);failFacts=true
      local ok,why=pcall(retry.Facts,4,a)
      assert(not ok and tostring(why):find('FACTS_UNKNOWN',1,true) and factReads==5)
      failFacts=false;local recovered=retry.Facts(4,a)
      assert(recovered.version==2 and factReads==6 and retry.Facts(4,a)==recovered and factReads==6)
    ''')
    print('PASS RuntimeWork: city/player fact isolation, fresh new batch and failed fact retry')
    lua.execute('''
      -- Fixture represents a read-only batch. No cross-write reuse is promised.
      districts={{GetCity=function()return a end},{GetCity=function()return b end},{GetCity=function()return foreign end}}
      enumerations=0;failEnumeration=true
      Players={[4]={GetDistricts=function()return {Members=function()
        enumerations=enumerations+1;local i=0
        return function()
          i=i+1;if i==2 and failEnumeration then error('DISTRICT_UNKNOWN')end
          if districts[i]then return i,districts[i]end
        end
      end}end}}
      function districtCount(w,c)local n=0;for _,d in w.Districts(4,c)do assert(d:GetCity()==c);n=n+1 end;return n end
      local ok,why=pcall(districtCount,work,a)
      assert(not ok and tostring(why):find('DISTRICT_UNKNOWN',1,true) and enumerations==1)
      failEnumeration=false
      assert(districtCount(work,a)==1 and enumerations==2)
      assert(districtCount(work,b)==1 and enumerations==2)
      assert(districtCount(SPCRuntimeWork.New(P,shared),a)==1 and enumerations==3)
    ''')
    print('PASS RuntimeWork: incomplete district capture is never published; complete index reused only in its batch')


def check_gpp_ownership(repo):
    fixture = fixture_through_function(repo / 'DevelopmentTests/test_p0_b2.py', 'runtime')
    lua = fixture['runtime']()
    lua.execute('''
      -- The fixture declares actual P0-B2 SQL and starts actual current writers.
      setBuildings(d,{'BUILDING_LIBRARY'});audit();noErrors();assert(gpp(c,'RESEARCH')==6)
      local p=Players[0];Players={[7]=p};c.owner=7;P.IsTestPlayer=function(pid)return pid==0 end
      unknownCarrier=GameInfo.Buildings.BUILDING_SPC_DEV_GPP_COMMERCE_7.Index
      fire('CityTransfered',7,1,0)
      assert(gpp(c,'RESEARCH')==6 and shared.Lv2GPP.errors['7:1'])
      unknownCarrier=nil;fire('PlayerTurnActivated',7)
      assert(gpp(c,'RESEARCH')==0 and not shared.Lv2GPP.errors['7:1'])
      -- Separate real load listener still removes dormant-owner native carriers.
      c.carriers[GameInfo.Buildings.BUILDING_SPC_DEV_GPP_RESEARCH_0.Index]=true
      assert(gpp(c,'RESEARCH')==2)
      fire('LoadScreenClose')
      assert(gpp(c,'RESEARCH')==0 and not shared.Lv2GPP.errors['7:1'])
      -- Same-owner current changes in one turn remain observable without dedupe.
      Players={[0]=p};c.owner=0;P.IsTestPlayer=function(pid)return pid==0 end
      d.workers=1;fire('CityWorkerChanged',0);assert(gpp(c,'RESEARCH')==2)
      d.workers=4;fire('CityWorkerChanged',0);assert(gpp(c,'RESEARCH')==8)
    ''')
    print('PASS actual GPP: transfer UNKNOWN holds 6, foreign turn withdraws to 0; load cleanup and same-turn workers 2→8')


def check_late_ui_and_dispatch(repo):
    mod = repo / 'Mod'
    ns = {'LuaRuntime': LuaRuntime, 'R': repo, 'M': mod}
    ui_runtime = extract_function(repo / 'DevelopmentTests/test_b135_gpp_scope.py', 'ui_runtime', ns)
    lua = ui_runtime()
    lua.execute('''
      fire('CityWorkerChanged',4);pulse();last(false,true)
      fire('CityWorkerChanged');pulse();last(false,false)
      -- Late turn/load fallbacks cannot be mistaken for pure worker input.
      turn=2;fire('PlayerTurnActivated',4);last(false,false)
      fire('CityWorkerChanged',4);fire('LoadScreenClose');pulse();last(false,false)
      fire('CityWorkerChanged',4);fire('GovernorChanged',4);pulse();last(true,false)
      -- Synchronous reentry belongs to a subsequent batch and is not swallowed.
      during=function()fire('GovernorChanged',4);pulse()end
      local n=#packets;fire('CityWorkerChanged',4);pulse();assert(#packets==n+1);last(false,true)
      pulse();assert(#packets==n+2);last(true,false)
      -- Failed sends retain their entire cause set for the existing bounded retry.
      fail=true;fire('CityWorkerChanged',4);pulse();last(false,true)
      fail=false;pulse();last(false,true)
      local n=#packets;pulse();assert(#packets==n)
    ''')
    source = (mod / 'Gameplay.lua').read_text()
    start = source.index('  if params.Action=="LV2_GPP_DIRTY" then')
    end = source.index('  if params.Action=="NETWORK_PUSH" then', start)
    branch = source[start:end]
    for params, cross, facts in [
        ('{FactsChanged=false,WorkerOnly=true}', 0, False),
        ('{FactsChanged=false,WorkerOnly=false}', 1, False),
        ('{FactsChanged=false}', 1, False),
        ('{}', 1, False),
        ('{FactsChanged=true,WorkerOnly=true}', 1, True),
    ]:
        lua = LuaRuntime(unpack_returned_tuples=True)
        lua.execute('''
          P={IsTestPlayer=function(pid)return pid==4 end,Observe=function()end}
          counts={};shared={}
          for _,name in ipairs({'Lv2Housing','Lv2GPP','Lv3Effects','Lv4Percent','ResearchInfrastructure','ResearchCross','ResearchApply','ResearchChair'})do
            shared[name]={Audit=function(scope)assert(scope.player==4);counts[name]=(counts[name]or 0)+1 end}
          end
          shared.NetworkBridge={Refresh=function(pid)assert(pid==4);counts.NetworkBridge=(counts.NetworkBridge or 0)+1 end}
        ''')
        lua.execute('function dispatch(playerID,params)\n' + branch + '\nend')
        lua.execute('local p=' + params + ';p.Action="LV2_GPP_DIRTY";dispatch(4,p)')
        actual = dict(lua.globals().counts.items())
        expected = {name: 1 for name in ['Lv2GPP', 'Lv3Effects', 'Lv4Percent', 'ResearchInfrastructure', 'ResearchApply', 'ResearchChair']}
        if cross:
            expected['ResearchCross'] = 1
        if facts:
            expected.update(Lv2Housing=1, NetworkBridge=1)
        assert actual == expected, (params, actual, expected)
    print('PASS actual GPP UI/Gameplay: pure-worker Cross guard, mixed/UNKNOWN/late turn/load, reentry and failed-send retry')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', type=Path, default=DEFAULT_REPO)
    args = parser.parse_args()
    repo = args.repo.resolve()
    assert (repo / 'Mod/RuntimeWork.lua').is_file(), repo
    check_dispatch(repo / 'Mod')
    check_batches(repo / 'Mod')
    check_gpp_ownership(repo)
    check_late_ui_and_dispatch(repo)
    print(json.dumps({'result': 'LOCAL_SIMULATION_PASS', 'scope': 'bounded update contracts; no runtime behavior change',
                      'groups': 6, 'runtime': 'Lupa lua55', 'repo': str(repo)}, ensure_ascii=False))


if __name__ == '__main__':
    main()
