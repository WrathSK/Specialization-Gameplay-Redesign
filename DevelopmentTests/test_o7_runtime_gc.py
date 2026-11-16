"""Actual B447-to-candidate GC decisions and genuine counter-file absence."""

from collections import deque
import unittest

from refactor_harness import Context, PackageVFS, measure
from retired_crew_sources import B447, gameplay as historical_gameplay, package as historical_package
from test_pu11_package_absence import NATIVE, mirror_bridge, pair, scalars


GC_NATIVE = """
heap=200*1024;gcCalls=0;countCalls=0;runStateCalls=0;cpu=0;wall=0;running=true
function installHeap()
 collectgarbage=function(mode)
  if mode=='count'then countCalls=countCalls+1;return heap end
  if mode=='isrunning'then runStateCalls=runStateCalls+1;return running end
  assert(mode=='collect','NEW_GC_MODE');gcCalls=gcCalls+1;heap=100*1024
  if duringCollect then duringCollect()end
 end
 os={clock=function()cpu=cpu+(cpuStep or 0.01);return cpu end,time=function()wall=wall+0.01;return wall end}
end
installHeap()
outcomes={}
function state(label)
 local d=ExposedMembers.SPC_P0.MemoryObservation.AutoGC
 outcomes[#outcomes+1]={label=label,reason=d.reason,failure=d.failure,enabled=d.enabled,
  calls=gcCalls,countCalls=countCalls,runStateCalls=runStateCalls,baseline=d.baselineSource,
  rows=#d.rows,collections=d.collections}
end
function activate()Events.PlayerTurnActivated.Fire(0);publish()end
"""

NORMAL = """
Events.LoadScreenClose.Fire();publish();state('LOAD')
turn=2;heap=399*1024;activate();state('INTERVAL')
turn=3;ExposedMembers.SPC_NetworkRequestInFlight=true
ExposedMembers.SPC_CopyBackground={pending=1};activate();state('WAITING_FOR_ACK')
for i=1,1000 do publish()end
state('IDLE')
ExposedMembers.SPC_NetworkRequestInFlight=false;publish();state('OTHER_UI_PENDING')
ExposedMembers.SPC_CopyBackground.pending=0;duringCollect=publish;publish();state('ACK')
assert(gcCalls==1)
activate();publish();state('DUPLICATE');assert(gcCalls==1)
"""

NEGATIVE_ON_TURN_END = """
Events.LoadScreenClose.Fire();publish();state('LOAD')
turn=2;heap=-1024;Events.PlayerTurnDeactivated.Fire(0);state('NEGATIVE_BOUNDARY')
turn=3;heap=500*1024;activate();state('UNTRUSTED')
local a=ExposedMembers.SPC_P0.MemoryObservation.AutoGC
assert(gcCalls==0 and not a.enabled and a.failure=='COUNT_UNAVAILABLE')
"""

FIRST_LOCAL_TURN = """
Events.PlayerTurnActivated.Fire(7);state('FOREIGN')
activate();state('LOCAL_BASELINE')
local a=ExposedMembers.SPC_P0.MemoryObservation.AutoGC
assert(a.baselineSource=='LOCAL_TURN' and gcCalls==0)
Events.LoadScreenClose.Fire();publish();state('LATE_LOAD')
assert(a.baselineSource=='LOCAL_TURN' and a.baselineTurn==1)
turn=3;heap=400*1024;running=false;activate();state('STOPPED_NATIVE')
assert(gcCalls==0 and not a.enabled and a.failure=='ENGINE_GC_STOPPED')
"""

SLOW_COLLECTION = """
Events.LoadScreenClose.Fire();publish()
turn=3;heap=500*1024;cpuStep=2.5;activate();state('STOP_SLOW')
assert(gcCalls==1 and ExposedMembers.SPC_P0.MemoryObservation.AutoGC.failure=='OVER_2_SECONDS')
turn=5;heap=600*1024;activate();state('LATCHED');assert(gcCalls==1)
"""


def absent(mode):
    return PackageVFS(absent=['PerformanceCounters'],missing_include=mode,forbidden_globals=['SPCPerformance'])


def observe(ctx, script, profile):
    ctx.loads=deque(maxlen=512)
    ctx.execute(NATIVE)
    ctx.execute(GC_NATIVE)
    ctx.load('Gameplay')
    ctx.execute("""
        local s=ExposedMembers.SPC_P0
        assert(s.StartStatus.MemoryObservation.state=='OK' and type(s.MemoryObservation.ReadGC)=='function')
    """)
    if profile=='disabled':
        ctx.execute('ExposedMembers.SPC_Performance.enabled=false')
    if profile in ('throw','silent_nil'):
        ctx.execute("""
            assert(SPCPerformance==nil and ExposedMembers.SPC_Performance==nil)
            assert(ExposedMembers.SPC_P0.MemoryEvidence==nil)
        """)
        assert any(row['module']=='PerformanceCounters.lua' and row['status']=='ABSENT'
                   and row['parent']=='Mod/Probe.lua' for row in ctx.loads)
        assert ctx.load_counts['failed']==0
    ctx.execute(script)
    return (scalars(ctx.eval('outcomes')),
            scalars(ctx.eval('ExposedMembers.SPC_P0.MemoryObservation.AutoGC')),
            scalars(ctx.eval('ExposedMembers.SPC_P0.MemoryEvidence and ExposedMembers.SPC_P0.MemoryEvidence.rows')))


class RuntimeGC(unittest.TestCase):
    def test_same_decisions_native_read_counts_and_stop_latches(self):
        scenarios={'ack_and_busy':NORMAL,'negative_boundary':NEGATIVE_ON_TURN_END,
                   'late_load':FIRST_LOCAL_TURN,'slow_collection':SLOW_COLLECTION}
        with historical_package(B447) as checkout:
            for name,script in scenarios.items():
                baseline=observe(historical_gameplay(checkout,revision=B447),script,'present')
                disabled=observe(historical_gameplay(checkout,revision=B447),script,'disabled')
                for profile in ('present','disabled','throw','silent_nil'):
                    with self.subTest(scenario=name,observer=profile):
                        vfs=absent(profile) if profile in ('throw','silent_nil') else PackageVFS()
                        candidate=observe(Context(vfs=vfs),script,profile)
                        self.assertEqual(candidate[:2],baseline[:2])
                        if profile in ('throw','silent_nil'):
                            self.assertIsNone(candidate[2])
                        else:
                            self.assertEqual(candidate[2],(disabled if profile=='disabled' else baseline)[2])
        measure('O7f_gc_owner_differential', {'baseline':B447,'scenarios':len(scenarios),'candidate_profiles':4,
                'same_native_gc_calls_and_reads':True,'same_stop_latches':True,'idle_publications':1000})

    def test_actual_counter_file_absence_keeps_route_ack_and_gc_controls(self):
        for mode in ('throw','silent_nil'):
            with self.subTest(mode=mode):
                def setup(g):
                    g.execute(GC_NATIVE)
                    g.execute("""
                        SPCRuntimeGC.Start(SPCP0,ExposedMembers.SPC_P0)
                        Events.LoadScreenClose.Fire()
                        turn=3;heap=400*1024
                    """)
                g,u,packets=pair(gameplay_setup=setup,profile=absent(mode))
                self.assertIsNone(u.globals().SPCPerformance)
                self.assertIsNone(u.eval('ExposedMembers.SPC_Performance'))
                self.assertIs(u.eval('ExposedMembers.SPC_NetworkRequestInFlight'),True)
                self.assertFalse(g.eval('ExposedMembers.SPC_P0.NetworkBridge.TransactionCurrent(0)'))
                g.execute('ExposedMembers.SPC_NetworkRequestInFlight=...',u.eval('ExposedMembers.SPC_NetworkRequestInFlight'))
                g.execute("""
                    activate()
                    assert(gcCalls==0 and ExposedMembers.SPC_P0.MemoryObservation.AutoGC.reason=='SKIP:NETWORK_INFLIGHT')
                """)
                g.execute('ExposedMembers.SPC_P0.NetworkBridge.Receive(0,...)',g.table(packets[0]))
                self.assertTrue(g.eval('ExposedMembers.SPC_P0.NetworkBridge.TransactionCurrent(0)'))
                mirror_bridge(g,u);u.execute('publish()')
                self.assertIs(u.eval('ExposedMembers.SPC_NetworkRequestInFlight'),False)
                g.execute('ExposedMembers.SPC_NetworkRequestInFlight=...',u.eval('ExposedMembers.SPC_NetworkRequestInFlight'))
                g.execute("""
                    publish();assert(gcCalls==1)
                    local s=ExposedMembers.SPC_P0
                    GameEvents.SPC_P0_Request.Fire(0,{Action='MEMORY_GC_READ',Token='gc'})
                    assert(s.LastToken=='gc' and s.Snapshot:find('GC试运行',1,true))
                    GameEvents.SPC_P0_Request.Fire(0,{Action='MEMORY_READ',Token='obs'})
                    assert(s.LastToken=='obs' and s.Snapshot=='内存观测未启用。')
                """)
                self.assertEqual(len(packets),1)

    def test_real_native_write_fence_remains_active_with_counters_absent(self):
        for mode in ('throw','silent_nil'):
            with self.subTest(mode=mode):
                ctx=Context(vfs=absent(mode))
                ctx.execute(NATIVE)
                ctx.load('Gameplay')
                ctx.execute("""
                    local p=SPCP0;local f=ExposedMembers.SPC_P0.EffectiveFacts
                    assert(f and p.FactReadService==f and SPCPerformance==nil)
                    local owner={}
                    function owner:SetProperty(key,value)
                        assert(select(3,f.DistrictWriteVersion(0,1)))
                        self[key]=value;error('NATIVE_APPLIED_THEN_THROW')
                    end
                    local version=f.Version()
                    local ok,err=pcall(p.SetProperty,owner,'value',9)
                    assert(not ok and err:find('NATIVE_APPLIED_THEN_THROW',1,true) and owner.value==9)
                    assert(f.Version()==version+2 and not select(3,f.DistrictWriteVersion(0,1)))
                """)
