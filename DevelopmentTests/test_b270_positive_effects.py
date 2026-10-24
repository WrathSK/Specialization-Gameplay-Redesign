"""B270 read-only positive-effects validation. Frozen tests remain unchanged.
Requires Lupa Lua5.1; extracts unchanged historical matrix sections, not their full acceptance suites.
Uses extracted frozen fixtures/assertions plus explicit current producer invalidation.
No native process access. No repository writes.
"""
from pathlib import Path
from unittest.mock import patch
import ast
import lupa.lua55
from lupa.lua51 import LuaRuntime
lupa.lua55.LuaRuntime=LuaRuntime # Nested fixture imports also execute under Lua 5.1.
R=Path(__file__).resolve().parents[1]
T=R/'DevelopmentTests'

def execute_prefix(filename,cutoff,setup_profile=()):
    p=T/filename; src=p.read_text().split(cutoff)[0]
    ns={'__file__':str(p)}
    for before,after in setup_profile:
     assert src.count(before)==1,'FIXTURE_PROFILE_SOURCE_CHANGED'
     src=src.replace(before,after)
    exec(compile(src,str(p)+'[selected frozen prefix]','exec'),ns)
    return ns

with patch('ctypes.CDLL',side_effect=OSError('Native process access disabled')):
    print('Lua 5.1 actual current runtime + actual SQL; offline fixture scope only',flush=True)
    b1=execute_prefix('test_p0_b1.py','# Exact retirement')
    l=b1['module_runtime']('Lv3Support',1)
    l.execute("for _,id in ipairs(SPCSpecialistSupport.Retired) do cities[1].built[id]=true end;cities[1].built.BUILDING_SPC_DEV_LV3_POP_RESEARCH_0=true;fire('LoadScreenClose');assert(d.changes==12 and writes==12);local w=writes;d.Audit();fire('LoadScreenClose');fire('GovernorPromoted');assert(writes==w and cities[1].built.BUILDING_SPC_DEV_LV3_POP_RESEARCH_0);for _,id in ipairs(SPCSpecialistSupport.Retired) do assert(not cities[1].built[id]) end")
    l=b1['module_runtime']('ResearchSupport',1)
    l.execute("setup('RESEARCH',4,2);cities[1].built.BUILDING_SPC_DEV_LV3_RESEARCH=true;local remove=P.RemoveBuilding;P.RemoveBuilding=function() error('INTENTIONAL_RETIRE_FAILURE') end;d.Audit();assert(writes==0 and d.errors['0:1']);P.RemoveBuilding=remove;d.Audit();assert(cities[1].built.BUILDING_SPC_DEV_RESEARCH_SUPPORT and not cities[1].built.BUILDING_SPC_DEV_LV3_RESEARCH);local w=writes;d.Audit();assert(writes==w)")
    print('B1 cold-load exact12 cleanup, population carrier retained; failed retirement blocks creation and recovers PASS',flush=True)
    src=(T/'test_p0_b1.py').read_text(); sql=src[src.index('# SQL executes real definitions'):src.index('# Full changed-file allowlist')]
    exec(compile(sql,'B1 SQL definitions','exec'),b1)
    print('B1 actual SQL inert tombstones and exact base3F3P PASS',flush=True)

    b2=execute_prefix('test_p0_b2.py','l=runtime()\nfor buildings,expected')
    l=b2['runtime']()
    # Every direct fixture edit marks the real producer dirty before asking the
    # current consumer to read. Historical wrappers omitted this contract.
    for names,expected in [([],1),(['LIBRARY'],2),(['LIBRARY','UNIVERSITY'],3),(['LIBRARY','UNIVERSITY','JNR_LABORATORY'],4),(['LIBRARY','UNIVERSITY','JNR_LABORATORY','RESEARCH_LAB'],5),(['JNR_LABORATORY'],2)]:
        l.globals().names=l.table_from(['BUILDING_'+b for b in names])
        l.execute(f"setBuildings(d,names);svc.MarkDirty();audit();noErrors();assert(housing(c)=={expected});local w=writes;audit();assert(writes==w)")
    l.execute("setBuildings(d,{'BUILDING_LIBRARY'});svc.MarkDirty();audit();noErrors();assert(housing(c)==2 and gpp(c,'RESEARCH')==6)")
    for fault,repair in [('c.active=nil','c.active=4'),('c.factsError=true','c.factsError=false'),('d.pillaged=nil','d.pillaged=false')]:
        l.execute(f"local w=writes;{fault};svc.MarkDirty();audit();assert(writes==w and shared.Lv2Housing.errors['0:1'] and shared.Lv2GPP.errors['0:1']);{repair};svc.MarkDirty();audit();noErrors();assert(writes==w)")
    l.execute("local w=writes;failRead=true;svc.MarkDirty();shared.Lv2Housing.Audit();assert(writes==w and shared.Lv2Housing.errors['0:1']);failRead=false;svc.MarkDirty();shared.Lv2Housing.Audit();noErrors();assert(writes==w);d.workers=nil;shared.Lv2GPP.Audit();assert(writes==w and shared.Lv2GPP.errors['0:1']);d.workers=3;shared.Lv2GPP.Audit();noErrors();assert(writes==w)")
    for family in ['LV2_HOUSING_8','GPP_COMMERCE_7']:
        owner='Lv2Housing' if family.startswith('LV2') else 'Lv2GPP'
        l.execute(f"local w=writes;c.active=1;unknownCarrier=GameInfo.Buildings['BUILDING_SPC_DEV_{family}'].Index;shared.{owner}.Audit();assert(writes==w);unknownCarrier=nil;c.active=4;audit();noErrors();assert(writes==w)")
    for fault,repair in [('c.active=1','c.active=4'),('d.pillaged=true','d.pillaged=false'),('d.complete=false','d.complete=true'),("c.identity='NONE'","c.identity='RESEARCH'")]:
        l.execute(f"{fault};svc.MarkDirty();audit();noErrors();assert(housing(c)==0 and gpp(c,'RESEARCH')==0);local w=writes;audit();assert(writes==w);{repair};svc.MarkDirty();audit();noErrors();assert(housing(c)==2 and gpp(c,'RESEARCH')==6)")
    l.execute("d.workers=0;fire('CityWorkerChanged',0,1);noErrors();assert(housing(c)==2 and gpp(c,'RESEARCH')==0);d.workers=1;fire('CityWorkerChanged',0,1);noErrors();assert(gpp(c,'RESEARCH')==2)")
    print('B2 explicit current producer invalidation: building tiers1/2/3/4/5/2; UNKNOWN hold, confirmed withdrawal, recovery and idempotence PASS',flush=True)
    for n in [1,2,4,8]:
        l=b2['runtime'](n);l.execute('counters={};audit();noErrors()')
        assert l.eval('counters.facts')==2*n and l.eval('counters.district_scan')==3*n
        l.execute("local w=writes;for i=1,10000 do fire('GameCoreEventPublishComplete');fire('GameCoreEventPlaybackComplete');fire('SystemUpdateUI');fire('UnitOperationStarted');fire('CityBuildingsChanged',0,1) end;assert(writes==w);fire('PlayerTurnActivated',0);local r,w=reads,writes;for i=1,10000 do fire('PlayerTurnActivated',0) end;assert(reads==r and writes==w);c.active=1;turn=turn+1;fire('PlayerTurnActivated',0);noErrors();assert(housing(c)==0 and gpp(c,'RESEARCH')==0)")
        print('B2 scaling/idle/once-turn',n,'cities PASS',flush=True)

    pc=execute_prefix('test_p0_c.py','# Old public writers cannot recreate',[("c.token='NEW';fire('LoadScreenClose')","c.token='NEW';fire('PlayerTurnActivated',0)")])
    for n in [1,2,4,8]:
        l=pc['runtime'](n);l.execute("counters={};for _,c in pairs(cities) do setBuildings(c.ds[1],{'BUILDING_LIBRARY'}) end;audit();good()")
        assert l.eval('counters.facts')==n and l.eval('counters.dc_capture')==n and l.eval('counters.district_scan')==n
        l.execute("local r,w=reads,writes;for i=1,10000 do fire('GameCoreEventPublishComplete');fire('GameCoreEventPlaybackComplete');fire('SystemUpdateUI');fire('UnitOperationStarted') end;assert(reads==r and writes==w);fire('PlayerTurnActivated',0);r=reads;w=writes;for i=1,10000 do fire('PlayerTurnActivated',0) end;assert(reads==r and writes==w);c.active=3;turn=turn+1;fire('PlayerTurnActivated',0);good();assert(coeff(c)==0)")
        print('RI scaling/idle/once-turn',n,'cities PASS',flush=True)
    l=pc['runtime']();l.execute("setBuildings(d,{'BUILDING_LIBRARY'});audit();good();assert(coeff(c)==1);local p=Players[0];Players={[7]=p};c.owner=7;P.IsTestPlayer=function(pid)return pid==0 end;unknownCarrier=GameInfo.Buildings.BUILDING_SPC_RESEARCH_INFRA_3.Index;fire('CityTransfered',7,1,0);assert(coeff(c)==1 and shared.ResearchInfrastructure.errors[7][1]);unknownCarrier=nil;fire('PlayerTurnActivated',7);assert(coeff(c)==0 and not shared.ResearchInfrastructure.errors[7][1]);seedOld();c.carriers[GameInfo.Buildings.BUILDING_SPC_RESEARCH_INFRA_0.Index]=true;c.locations[GameInfo.Buildings.BUILDING_SPC_RESEARCH_INFRA_0.Index]=d.plot;fire('LoadScreenClose');good();retired();assert(coeff(c)==0)")
    print('RI foreign ownership UNKNOWN holds, known foreign-turn withdrawal, cold-load exact retired/current cleanup PASS',flush=True)
print('ALL SELECTED OFFLINE POSITIVE-EFFECT VALIDATIONS PASS; no engine acceptance claimed',flush=True)
