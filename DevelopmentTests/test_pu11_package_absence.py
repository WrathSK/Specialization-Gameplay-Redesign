"""PU11 opt-in actual package absence; source controls, never native PASS.

Empty-world roots characterize loading and transport only. They do not certify
valid four-profession saves/effects, O7 independence or native include semantics.
"""
from dataclasses import FrozenInstanceError
from hashlib import sha256
from pathlib import Path
import unittest
from unittest.mock import patch
from lupa.lua51 import lua_type
from refactor_harness import Context,PackageVFS,ROOT,RUN,measure
from retired_crew_sources import B447, gameplay as historical_gameplay, package as historical_package

NATIVE=r"""
print=function()end
local empty=setmetatable({}, {__call=function()return function()end end})
local cities={Members=function()return function()end end,FindID=function()return nil end,GetCapitalCity=function()return nil end}
local trade={GetNumOutgoingRoutes=function()return 0 end,CountOutgoingRoutes=function()return 0 end}
Players={[0]={IsHuman=function()return true end,IsTurnActive=function()return true end,
 GetCities=function()return cities end,GetUnits=function()return cities end,GetTrade=function()return trade end}}
PlayerConfigurations={[0]={GetCivilizationTypeName=function()return 'CIVILIZATION_SPC_AMERICA'end,
 GetLeaderTypeName=function()return 'LEADER_SPC_T_ROOSEVELT'end}}
GameConfiguration={IsAnyMultiplayer=function()return false end,GetGameSpeedType=function()return 'GAMESPEED_STANDARD'end}
GameInfo=setmetatable({}, {__index=function()return empty end});Locale={Lookup=function(s)return s end}
properties={};Game.GetProperty=function(k)return properties[k]end;Game.SetProperty=function(k,v)properties[k]=v end
UI={};Controls={};PlayerOperations={EXECUTE_SCRIPT=1};ContextPtr.ClearUpdate=function()end
"""

def root(name='Gameplay',profile=None):
    c=Context(name=name,vfs=profile or PackageVFS());c.execute(NATIVE);c.load(name);return c

def scalars(value):
    if lua_type(value)=='table':return {k:scalars(v) for k,v in value.items()}
    if value is None or isinstance(value,(str,int,float,bool)):return value
    raise AssertionError('NONSCALAR_TRANSPORT')

def mirror_bridge(g,u):
    # Explicit simulation of ExposedMembers visibility, not a native timing proof.
    packet=g.eval("""(function()local s=ExposedMembers.SPC_P0;local n=s.NetworkBridge;local b=n.players[0]
     return {Version=s.Version,RouteSignalRevision=s.RouteSignalRevision,NetworkBridge={ready=n.ready,epoch=n.epoch,
      players=b and {[0]={seq=b.seq,acceptedSeq=b.acceptedSeq,fingerprint=b.fingerprint,revalidation=b.revalidation,
        signal=b.signal,routes=b.routes and {}}}or{}}}end)()""")
    u.globals().ExposedMembers.SPC_P0=u.table(scalars(packet))

def pair(enabled=True, *, flight_observer=None, gameplay_setup=None, profile=None):
    g=root(profile=profile);g.execute('Events.LoadScreenClose.Fire();publish()')
    assert g.eval('ExposedMembers.SPC_P0.NetworkBridge.ready')
    if gameplay_setup:
        gameplay_setup(g)
    u=root('UI/BackgroundRoutes',profile=profile);mirror_bridge(g,u)
    u.execute('turn=...',g.eval('turn'))
    # Factory really ran in Gameplay; copy only its scalar exposed state into the
    # separate UI VM. No SPCPerformance/Probe/Sender replacement is installed.
    counters=scalars(g.eval('ExposedMembers.SPC_Performance'))
    if counters is not None:
        u.globals().ExposedMembers.SPC_Performance=u.table(counters)
    u.execute('if ExposedMembers.SPC_Performance then ExposedMembers.SPC_Performance.enabled=... end',enabled)
    if flight_observer == 'absent':
        u.execute('SPCPerformance=nil;ExposedMembers.SPC_Performance=nil')
    elif flight_observer == 'throws':
        u.execute("SPCPerformance.Flight=function()error('DIAGNOSTIC_OBSERVER_FAILED')end")
    packets=[]
    def request(pid,operation,payload):
        assert pid==0 and operation==1
        packets.append(scalars(payload))
    u.globals().UI.RequestPlayerOperation=request
    u.execute('init()');assert len(packets)==1 and packets[0]['Action']=='NETWORK_PUSH'
    return g,u,packets

class Package(unittest.TestCase):
    def test_actual_manifest_separates_entry_from_include_visibility(self):
        v=PackageVFS();self.assertEqual(v.manifest_sha256,sha256((ROOT/'Mod/SpecializationP0.modinfo').read_bytes()).hexdigest())
        self.assertIn('Gameplay.lua',v.files);self.assertNotIn('Gameplay.lua',v.imports)
        c=Context(vfs=v)
        with self.assertRaisesRegex(FileNotFoundError,'NOT_IMPORTED'):c.execute("include('Gameplay')")
        c.load('IdentityEqual');self.assertIsNotNone(c.globals().SPCIdentityEqual)
        self.assertIsNone(c.globals().SPCP0)
    def test_absent_typo_unsafe_paths_and_invalid_mode_are_rejected(self):
        for n in ('/Probe','../Probe','UI//Probe','Probe;error','Probe.lua.lua'):
            with self.subTest(n=n),self.assertRaises(ValueError):PackageVFS(absent=[n])
        with self.assertRaisesRegex(ValueError,'ABSENT_MODULE_NOT_IN_PACKAGE'):PackageVFS(absent=['TypoModule'])
        with self.assertRaisesRegex(ValueError,'INVALID_MISSING_INCLUDE_MODE'):PackageVFS(missing_include='optimistic')
    def test_profiles_are_immutable_and_imports_must_be_packaged(self):
        v=PackageVFS()
        with self.assertRaises(FrozenInstanceError):v.missing_include='silent_nil'
        raw=b'<Mod><Files><File>A.lua</File></Files><InGameActions><ImportFiles><File>B.lua</File></ImportFiles></InGameActions></Mod>'
        with patch.object(Path,'read_bytes',return_value=raw),self.assertRaisesRegex(ValueError,'INVALID_PACKAGE_MANIFEST'):PackageVFS()
    def test_throw_and_silent_nil_have_no_execution_or_export(self):
        for mode in ('throw','silent_nil'):
            c=Context(vfs=PackageVFS(absent=['IdentityEqual'],missing_include=mode,forbidden_globals=['SPCIdentityEqual']))
            before=dict(RUN['executed'])
            if mode=='throw':
                with self.assertRaisesRegex(FileNotFoundError,'PACKAGE_ABSENT'):c.execute("include('IdentityEqual')")
            else:self.assertIsNone(c.execute("return include('IdentityEqual')"))
            self.assertEqual(RUN['executed'],before);self.assertIsNone(c.globals().SPCIdentityEqual)
            self.assertEqual(c.load_counts,dict(attempts=1,missing=1,completed=0,failed=0))
            with self.assertRaisesRegex(FileNotFoundError,'PACKAGE_ABSENT'):c.load('IdentityEqual')
    def test_forbidden_global_cannot_mask_a_missing_file_even_when_false(self):
        for value in (False,7,{}):
            c=Context(vfs=PackageVFS(absent=['PerformanceCounters'],forbidden_globals=['SPCPerformance']))
            c.globals().SPCPerformance=c.table(value)
            with self.assertRaisesRegex(AssertionError,'FORBIDDEN_PREINJECTED_GLOBAL'):c.load('Probe')
            self.assertEqual(c.load_counts['attempts'],0)
    def test_bounded_load_observations_do_not_claim_missing_source_executed(self):
        c=Context(vfs=PackageVFS(absent=['IdentityEqual'],missing_include='silent_nil'))
        before=dict(RUN['executed']);c.execute("for i=1,1000 do include('IdentityEqual')end")
        self.assertEqual(len(c.loads),64);self.assertEqual(c.load_counts['missing'],1000)
        self.assertEqual(c.load_counts['completed'],0);self.assertEqual(RUN['executed'],before)
    def test_packaged_file_missing_on_disk_is_not_a_successful_include(self):
        c=Context(vfs=PackageVFS(missing_include='silent_nil'));before=dict(RUN['executed'])
        with patch.object(Path,'read_text',side_effect=FileNotFoundError('MISSING_ON_DISK')):
            with self.assertRaisesRegex(FileNotFoundError,'MISSING_ON_DISK'):c.execute("include('IdentityEqual')")
        self.assertEqual(c.loads[-1]['status'],'FILE_READ_FAILED')
        self.assertEqual(c.load_counts['failed'],1);self.assertEqual(c.load_counts['completed'],0)
        self.assertEqual(RUN['executed'],before)
    def test_fresh_reload_retains_profile_and_only_explicit_scalar_snapshot(self):
        v=PackageVFS(absent=['PerformanceCounters'],forbidden_globals=['SPCPerformance'])
        c=Context(vfs=v);c.globals().oldSession='MUST_NOT_COPY';c.load('IdentityEqual')
        r=c.reload({'token':'r1','level':3});self.assertIs(r.vfs,v)
        self.assertIsNone(r.globals().oldSession);self.assertIsNone(r.globals().SPCIdentityEqual)
        self.assertIsNone(r.globals().SPCPerformance);self.assertEqual(r.eval('retained.level'),3)
        self.assertEqual(r.load_counts['attempts'],0)
    def test_default_context_keeps_existing_identity_dependency_and_reload(self):
        c=Context();self.assertIsNone(c.vfs);self.assertIsNotNone(c.globals().SPCIdentityEqual)
        c.load('FactChanges');self.assertIsNotNone(c.globals().SPCFactChanges)
        r=c.reload({'x':1});self.assertIsNotNone(r.globals().SPCIdentityEqual);self.assertIsNone(r.globals().SPCFactChanges)

class ActualRoots(unittest.TestCase):
    def test_actual_gameplay_and_ui_load_without_injected_production_globals(self):
        for name in ('Gameplay','UI/BackgroundRoutes'):
            c=Context(vfs=PackageVFS());c.execute(NATIVE)
            for key in ('SPCP0','SPCPerformance','SPCNetworkSender','SPCRuntimeComposition'):
                self.assertIsNone(c.globals()[key])
            c.load(name);self.assertEqual(c.load_counts['missing'],0);self.assertEqual(c.load_counts['failed'],0)
            self.assertEqual(c.load_counts['completed'],c.load_counts['attempts'])
            self.assertIsNotNone(c.globals().SPCP0);self.assertIsNotNone(c.globals().SPCPerformance)
            if name=='Gameplay':
                self.assertEqual(c.eval('ExposedMembers.SPC_P0.StartStatus.NetworkBridge.state'),'OK')
                states={}
                for _,row in c.globals().ExposedMembers.SPC_P0.StartStatus.items():
                    state=row['state'];states[state]=states.get(state,0)+1
                measure('pu11_empty_world_start_states',{'states':states,'load_counts':c.load_counts,'scope':'Empty native DB;load characterization only,not healthy four-profession startup or valid-save acceptance.'})
    def test_optional_culture_observer_absence_reaches_actual_gameplay_consumer(self):
        for mode in ('throw','silent_nil'):
            c=root('Gameplay',PackageVFS(absent=['CultureDiagnostics'],missing_include=mode,forbidden_globals=['SPCCultureDiagnostics']))
            self.assertIsNone(c.globals().SPCCultureDiagnostics);self.assertIsNotNone(c.globals().SPCPerformance)
            affected=[row for row in c.loads if row['status']=='ABSENT'and row['module']=='CultureDiagnostics.lua']
            self.assertGreater(len(affected),0,'MISSING_FILE_DID_NOT_AFFECT_TESTED_PATH')
            self.assertEqual(c.load_counts['failed'],0)
    def test_background_routes_does_not_load_culture_observer_not_an_absence_claim(self):
        c=root('UI/BackgroundRoutes',PackageVFS(absent=['CultureDiagnostics'],missing_include='throw',forbidden_globals=['SPCCultureDiagnostics']))
        self.assertEqual(c.load_counts['missing'],0)
        self.assertFalse(any(row['module']=='CultureDiagnostics.lua'for row in c.loads))
        self.assertIsNone(c.globals().SPCCultureDiagnostics)
    def test_absent_performance_is_current_required_coupling_not_independence_pass(self):
        with historical_package(B447) as checkout:
            for name in ('Gameplay','UI/BackgroundRoutes'):
                for mode in ('throw','silent_nil'):
                    c=historical_gameplay(checkout,revision=B447,name=name,absent=['PerformanceCounters'],
                        missing_include=mode,forbidden_globals=['SPCPerformance'])
                    c.execute(NATIVE)
                    with self.assertRaises(Exception) as got:c.load(name)
                    self.assertTrue('PerformanceCounters' in str(got.exception) or 'SPCPerformance' in str(got.exception))
                    self.assertIsNone(c.globals().SPCPerformance)
                    missing=[row for row in c.loads if row['status']=='ABSENT'];self.assertEqual(len(missing),1)
                    self.assertEqual(missing[0]['parent'],'historical/'+B447+'/Mod/Probe.lua')
                    self.assertEqual(c.load_counts['failed'],2)
                    key='historical/'+B447+'/Mod/'+name+'.lua'
                    self.assertEqual(RUN['executed'][key]['execution_by_test'][RUN.get('active_test')or'fixture'],'FAILED_PARTWAY')

class ActualTransport(unittest.TestCase):
    def test_ui_sender_real_bridge_ack_and_flight_survive_counting_disabled(self):
        for enabled in (True,False):
            g,u,packets=pair(enabled)
            self.assertEqual(u.eval('ExposedMembers.SPC_Performance.inflight'),1)
            self.assertIs(u.eval('ExposedMembers.SPC_NetworkRequestInFlight'),True)
            self.assertFalse(g.eval('ExposedMembers.SPC_P0.NetworkBridge.TransactionCurrent(0)'))
            p=packets[0];g.execute('ExposedMembers.SPC_P0.NetworkBridge.Receive(0,...)',g.table(p))
            self.assertTrue(g.eval('ExposedMembers.SPC_P0.NetworkBridge.TransactionCurrent(0)'))
            mirror_bridge(g,u);u.execute('publish()')
            self.assertEqual(u.eval('ExposedMembers.SPC_Performance.inflight'),0)
            self.assertIs(u.eval('ExposedMembers.SPC_NetworkRequestInFlight'),False)
            self.assertEqual(len(packets),1)
            self.assertEqual(u.eval('ExposedMembers.SPC_Performance.entries.net_send.total'),1 if enabled else 0)
            u.execute('for i=1,1000 do publish()end');self.assertEqual(len(packets),1)
            u.execute('shutdown()');self.assertEqual(u.eval('ExposedMembers.SPC_Performance.inflight'),0)
            self.assertIs(u.eval('ExposedMembers.SPC_NetworkRequestInFlight'),False)
    def test_unacked_proof_does_not_retry_on_idle_and_stop_clears_real_flight(self):
        g,u,packets=pair(False);u.execute('for i=1,1000 do publish()end')
        self.assertEqual(len(packets),1);self.assertEqual(u.eval('ExposedMembers.SPC_Performance.inflight'),1)
        self.assertFalse(g.eval('ExposedMembers.SPC_P0.NetworkBridge.TransactionCurrent(0)'))
        u.execute('shutdown()');self.assertEqual(u.eval('ExposedMembers.SPC_Performance.inflight'),0)
    def prepare_gc(self,g):
        g.execute("""
         heap=200*1024;gcCalls=0;cpu=0;wall=0
         collectgarbage=function(mode)if mode=='count'then return heap elseif mode=='isrunning'then return true end
          assert(mode=='collect');gcCalls=gcCalls+1;heap=100*1024 end
         os={clock=function()cpu=cpu+0.01;return cpu end,time=function()wall=wall+0.01;return wall end}
         shared=ExposedMembers.SPC_P0;SPCRuntimeGC.Start(SPCP0,shared,SPCPerformance.PrepareMemoryObserver)
         ExposedMembers.SPC_Performance.enabled=false;Events.LoadScreenClose.Fire()
         turn=3;heap=400*1024
        """)

    def mirror_flight(self,g,u):
        # Copy the actual production scalar, not the optional counter or table.
        g.execute('ExposedMembers.SPC_NetworkRequestInFlight=...',u.eval('ExposedMembers.SPC_NetworkRequestInFlight'))

    def test_actual_gc_waits_for_ui_flight_with_counters_disabled(self):
        g,u,packets=pair(False,gameplay_setup=self.prepare_gc)
        self.mirror_flight(g,u)
        g.execute('Events.PlayerTurnActivated.Fire(0);publish()')
        self.assertEqual(g.eval('gcCalls'),0)
        self.assertEqual(g.eval('shared.MemoryObservation.AutoGC.reason'),'SKIP:NETWORK_INFLIGHT')
        g.execute('ExposedMembers.SPC_P0.NetworkBridge.Receive(0,...)',g.table(packets[0]))
        self.assertTrue(g.eval('ExposedMembers.SPC_P0.NetworkBridge.TransactionCurrent(0)'))
        mirror_bridge(g,u);u.execute('publish()')
        self.mirror_flight(g,u)
        g.execute('publish();publish()');self.assertEqual(g.eval('gcCalls'),1)
        self.assertEqual(g.eval('shared.MemoryObservation.AutoGC.reason'),'AUTO_GROWTH')

    def test_actual_request_ack_and_gc_survive_unavailable_flight_observer(self):
        for observer in ('absent','throws'):
            with self.subTest(observer=observer):
                g,u,packets=pair(False,flight_observer=observer,gameplay_setup=self.prepare_gc)
                self.assertIs(u.eval('ExposedMembers.SPC_NetworkRequestInFlight'),True)
                self.assertFalse(g.eval('ExposedMembers.SPC_P0.NetworkBridge.TransactionCurrent(0)'))
                g.execute('ExposedMembers.SPC_Performance=nil')
                self.mirror_flight(g,u)
                g.execute('Events.PlayerTurnActivated.Fire(0);publish()')
                self.assertEqual(g.eval('shared.MemoryObservation.AutoGC.reason'),'SKIP:NETWORK_INFLIGHT')
                g.execute('for i=1,1000 do publish()end;assert(gcCalls==0)')
                u.execute('for i=1,1000 do publish()end')
                self.assertEqual(len(packets),1)
                g.execute('ExposedMembers.SPC_P0.NetworkBridge.Receive(0,...)',g.table(packets[0]))
                self.assertTrue(g.eval('ExposedMembers.SPC_P0.NetworkBridge.TransactionCurrent(0)'))
                mirror_bridge(g,u);u.execute('publish()')
                self.assertIs(u.eval('ExposedMembers.SPC_NetworkRequestInFlight'),False)
                self.mirror_flight(g,u)
                g.execute('publish();publish();assert(gcCalls==1)')
                self.assertEqual(g.eval('shared.MemoryObservation.AutoGC.reason'),'AUTO_GROWTH')

    def test_actual_waiting_for_bridge_is_not_an_inflight_gc_retry(self):
        g,u,packets=pair()
        g.execute('ExposedMembers.SPC_P0.NetworkBridge.Receive(0,...)',g.table(packets[0]))
        mirror_bridge(g,u);u.execute('publish()')
        u.execute("""
          ExposedMembers.SPC_P0.NetworkBridge.ready=false
          Events.TradeRouteActivityChanged.Fire();publish()
          assert(ExposedMembers.SPC_P0_BackgroundRoutes.awaitingNetwork)
          assert(ExposedMembers.SPC_NetworkRequestInFlight==false)
        """)
        self.assertEqual(len(packets),1)
        self.prepare_gc(g)
        self.mirror_flight(g,u)
        g.execute("""
          -- A stale measurement is ignored, but the existing UI pending guard remains.
          ExposedMembers.SPC_Performance.inflight=1
          ExposedMembers.SPC_P0_BackgroundRoutes={awaitingNetwork=true}
          Events.PlayerTurnActivated.Fire(0);publish()
          assert(gcCalls==0 and shared.MemoryObservation.AutoGC.reason=='SKIP:ROUTES_PENDING')
          ExposedMembers.SPC_P0_BackgroundRoutes.awaitingNetwork=false
          publish();assert(gcCalls==0)
        """)

class RetainedGC(unittest.TestCase):
    # Frozen standalone safety tests are retained regression, NOT absence proof.
    def run_case(self,name):
        from refactor_harness import TrackedLua51,legacy_source_observation
        import test_b138_gc as old
        with patch.object(old,'LuaRuntime',TrackedLua51),legacy_source_observation():getattr(old,name)(ROOT)
    def test_existing_gc_bounded_state(self):self.run_case('bounded_state')

if __name__=='__main__':unittest.main()
