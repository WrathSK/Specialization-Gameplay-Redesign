"""Scoped NET-1/NET-2: real Lua51 sender, background collector, bridge and consumers.
Native clocks, UI transport, city/route data and operations are explicit doubles.
No engine or external DB access. LOCAL_SIMULATION_PASS only.
"""
import unittest
from refactor_harness import ROOT, TrackedLua51, legacy_source_observation
from refactor_defect_fixtures import fact_publication_profile
import test_culture_network as culture_module

MOD = ROOT / 'Mod'


def pipeline(*, cold=False, hold=False, active=True, restricted=False):
    old = culture_module.LuaRuntime
    culture_module.LuaRuntime = TrackedLua51
    try:
        with legacy_source_observation():
            lua = culture_module.fixture(not cold)
    finally:
        culture_module.LuaRuntime = old
    fact_publication_profile(lua, False)
    lua.globals().activeState = active
    lua.globals().holdPackets = hold
    lua.execute('''
      complete(4,1);cn.SourceChanged(0,4)
      GP=Events;UP=events();shared.Version=P.VERSION;ExposedMembers.SPC_P0=shared
      P.Scalar=tostring;P.Call=function(o,m,...)return pcall(o[m],o,...)end
      P.RouteUnitRelevant=function(pid,id)return units[id]~=nil end
      SPCPerformance={Flight=function(n)inFlight=n end};SPCP0=P
      PlayerOperations={EXECUTE_SCRIPT=1};packets={};requests=0;proofFailures=0
      routeRows={
       {OriginCityPlayer=0,OriginCityID=4,DestinationCityPlayer=0,DestinationCityID=2,TraderUnitID=10},
       {OriginCityPlayer=0,OriginCityID=2,DestinationCityPlayer=0,DestinationCityID=1,TraderUnitID=11},
       {OriginCityPlayer=0,OriginCityID=2,DestinationCityPlayer=0,DestinationCityID=5,TraderUnitID=12}}
      routeCount=#routeRows
      for _,c in pairs(cities)do c.GetTrade=function()return {GetOutgoingRoutes=function()
        if uiReadFail then error('NATIVE_ROUTE_READ_UNAVAILABLE')end
        local rows={};for _,r in ipairs(routeRows)do if r.OriginCityID==c.id then rows[#rows+1]=r end end;return rows
      end}end end
      Players[0].GetTrade=function()return {
       CountOutgoingRoutes=function()return #routeRows end,
       GetNumOutgoingRoutes=function()return #routeRows end}end
      Players[0].IsTurnActive=function()
       if activeError then error('TURN_ACTIVITY_UNAVAILABLE')end;return activeState
      end
      ContextPtr={SetInitHandler=function(_,f)init=f end,SetShutdown=function(_,f)shutdown=f end,
       SetUpdate=function()error('TIMER_FORBIDDEN')end,ClearUpdate=function()end}
      UI={RequestPlayerOperation=function(pid,op,p)
       if p.Action=='NETWORK_REVALIDATE_FAILURE'then proofFailures=proofFailures+1;net.CheckEvidence(true);return true end
       requests=requests+1;packets[#packets+1]=p
       if sendThrows then error('SEND_THROW')end
       if not holdPackets then net.Receive(pid,p)end
       return true
      end}
      function gpDrain()
       shared.FactChanges.Flush();shared.FactBindings.Flush()
       GP.GameCoreEventPublishComplete.Fire()
      end
      function deliver(i)net.Receive(0,packets[i])end
      function idle(n)
       for i=1,n do UP.GameCoreEventPublishComplete.Fire();UP.GameCoreEventPlaybackComplete.Fire();UP.SystemUpdateUI.Fire()end
      end
      Events=UP
    ''')
    def include(name):
        if name != 'Probe':
            lua.execute((MOD / (name + '.lua')).read_text())
    lua.globals().include = include
    if restricted:
        lua.execute('os=nil;io=nil;debug=nil;package=nil;require=nil;rawget=nil;loadfile=nil;dofile=nil;collectgarbage=nil;table.unpack=nil;table.pack=nil')
    with legacy_source_observation():
        lua.execute((MOD / 'UI/BackgroundRoutes.lua').read_text())
    lua.execute('init();pub=ExposedMembers.SPC_P0_BackgroundRoutes')
    return lua


class SignalCatchUp(unittest.TestCase):
    def test_same_content_signal_only_event_reconfirms_and_wakes_real_bindings(self):
        l=pipeline();l.execute('''
         assert(requests==0 and net.TransactionCurrent(0))
         local fp=net.players[0].fingerprint;local rev=net.Input(0).inputVersion
         local proof=net.ProofRevision(0);local writes=created+removed
         wakes=0;shared.Commerce={Mark=function(pid)assert(pid==0);wakes=wakes+1 end}
         GP.UnitOperationStarted.Fire(0,10)
         assert(net.players[0].revalidation=='VERIFIED' and not net.TransactionCurrent(0))
         UP.GameCoreEventPublishComplete.Fire();gpDrain();UP.GameCoreEventPublishComplete.Fire()
         assert(requests==1 and wakes>0 and net.TransactionCurrent(0))
         assert(net.players[0].signal==shared.RouteSignalRevision and net.players[0].fingerprint==fp)
         assert(net.Input(0).inputVersion==rev and net.ProofRevision(0)>proof)
         assert(created+removed==writes and propertyWrites==0)
        ''')

    def test_verified_unchanged_content_signal_and_lifecycle_are_duplicates(self):
        l=pipeline();l.execute('''
         local scans=counts.route_scan;local writes=created+removed
         idle(1000);assert(requests==0 and counts.route_scan==scans)
         for i=1,10 do UP.LoadScreenClose.Fire();UP.LocalPlayerTurnBegin.Fire()end
         idle(20);assert(requests==0 and created+removed==writes and net.TransactionCurrent(0))
        ''')

    def test_no_passive_recompute_or_transaction_use_before_new_proof(self):
        l=pipeline(hold=True);l.execute('''
         local old=amount(cities[1]);GP.UnitOperationStarted.Fire(0,10);net.CheckEvidence(false)
         complete(4,2);cn.SourceChanged(0,4)
         assert(amount(cities[1])==old and not net.TransactionCurrent(0))
         assert(not pcall(net.CurrentCapitalSources,0,cities[1],'CULTURE'))
         assert(net.CurrentOutgoingDomestic(0,cities[2]).validity=='UNKNOWN')
         UP.GameCoreEventPublishComplete.Fire();idle(20)
         assert(requests==1 and amount(cities[1])==old and not net.TransactionCurrent(0))
         deliver(1);gpDrain();UP.GameCoreEventPublishComplete.Fire()
         assert(net.TransactionCurrent(0) and amount(cities[1])==2)
        ''')


class LifecycleRecovery(unittest.TestCase):
    def test_cold_first_lost_packet_recovers_on_load_close_same_turn(self):
        l=pipeline(cold=True,hold=True);l.execute('''
         assert(requests==1 and not net.TransactionCurrent(0));local first=packets[1]
         idle(1000);assert(requests==1)
         holdPackets=false;UP.LoadScreenClose.Fire();gpDrain();idle(2)
         assert(requests==2 and packets[2].Seq>first.Seq and packets[2].Epoch==first.Epoch)
         assert(net.TransactionCurrent(0) and net.players[0].acceptedSeq==packets[2].Seq)
         assert(not pub.awaitingNetwork and inFlight==0 and propertyWrites==0)
        ''')

    def test_local_begin_is_second_bounded_recovery_opportunity(self):
        l=pipeline(cold=True,hold=True);l.execute('''
         assert(requests==1);UP.LoadScreenClose.Fire();assert(requests==2)
         idle(1000);assert(requests==2)
         holdPackets=false;UP.LocalPlayerTurnBegin.Fire();gpDrain();idle(2)
         assert(requests==3 and net.TransactionCurrent(0) and not pub.awaitingNetwork)
        ''')

    def test_repeated_lifecycle_and_idle_do_not_rearm_each_kind(self):
        l=pipeline(cold=True,hold=True);l.execute('''
         for i=1,100 do UP.LoadScreenClose.Fire();UP.LocalPlayerTurnBegin.Fire();idle(1)end
         assert(requests==3 and not net.TransactionCurrent(0))
         idle(1000);assert(requests==3)
         deliver(3);gpDrain();idle(2);assert(net.TransactionCurrent(0))
         for i=1,10 do UP.LoadScreenClose.Fire();UP.LocalPlayerTurnBegin.Fire()end
         assert(requests==3)
        ''')

    def test_load_witness_survives_temporary_collection_failure(self):
        l=pipeline(cold=True,hold=True);l.execute("""
         uiReadFail=true;UP.LoadScreenClose.Fire();assert(requests==1)
         uiReadFail=false;holdPackets=false;idle(2);gpDrain();idle(2)
         assert(requests==2 and net.TransactionCurrent(0) and not pub.awaitingNetwork)
        """)

    def test_failed_collection_witness_does_not_rearm_idle_read_budget(self):
        l=pipeline(cold=True,hold=True);l.execute("""
         uiReadFail=true;local scans=counts.route_scan;UP.LoadScreenClose.Fire();idle(1000)
         assert(counts.route_scan==scans+3 and requests==1 and not net.TransactionCurrent(0))
         uiReadFail=false;holdPackets=false;UP.LocalPlayerTurnBegin.Fire();gpDrain();idle(2)
         assert(requests==2 and net.TransactionCurrent(0))
        """)

    def test_busy_lifecycle_witness_is_drained_after_native_reentry(self):
        l=pipeline(cold=True,hold=True);l.execute("""
         local send=UI.RequestPlayerOperation;local once=false
         UI.RequestPlayerOperation=function(...)
          local r=send(...)
          if not once then once=true;UP.LoadScreenClose.Fire();holdPackets=false end
          return r
         end
         UP.LocalPlayerTurnBegin.Fire();assert(requests==2)
         idle(2);gpDrain();idle(2)
         assert(requests==3 and net.TransactionCurrent(0) and not pub.awaitingNetwork)
        """)

    def test_normal_local_begin_and_foreign_turn_do_no_extra_collection(self):
        l=pipeline();l.execute("""
         local scans=counts.route_scan;UP.PlayerTurnActivated.Fire(9)
         for i=1,20 do UP.LocalPlayerTurnBegin.Fire();idle(1)end
         assert(requests==0 and counts.route_scan==scans and net.TransactionCurrent(0))
        """)

    def test_current_empty_routes_recover_without_restoring_the_dropped_routes(self):
        l=pipeline(cold=True,hold=True);l.execute("""
         routeRows={};holdPackets=false;UP.LoadScreenClose.Fire();gpDrain();idle(2)
         assert(requests==2 and packets[2].Count==0 and packets[2].Data=='EMPTY')
         assert(net.TransactionCurrent(0) and #net.players[0].routes==0)
         local seq=net.players[0].acceptedSeq;deliver(1)
         assert(net.players[0].acceptedSeq==seq and #net.players[0].routes==0)
        """)

    def test_turn_wait_does_not_poll_turn_activity_on_idle_frames(self):
        l=pipeline(cold=True,hold=True,active=False);l.execute("""
         local reads=0;Players[0].IsTurnActive=function()reads=reads+1;return false end
         UP.LoadScreenClose.Fire();local n=reads;idle(1000)
         assert(requests==0 and reads==n and pub.awaitingTurn)
         Players[0].IsTurnActive=function()return true end;holdPackets=false
         UP.LocalPlayerTurnBegin.Fire();gpDrain();idle(2)
         assert(requests==1 and not pub.awaitingTurn and net.TransactionCurrent(0))
        """)

    def test_known_inactive_does_not_send_or_spend_recovery(self):
        l=pipeline(cold=True,hold=True,active=False);l.execute("""
         assert(requests==0);UP.LoadScreenClose.Fire();UP.LocalPlayerTurnBegin.Fire();idle(100)
         assert(requests==0 and not net.TransactionCurrent(0))
         activeState=true;holdPackets=false;UP.LocalPlayerTurnBegin.Fire();gpDrain();idle(2)
         assert(requests==1 and net.TransactionCurrent(0))
        """)

    def test_unknown_activity_retains_transport_but_never_invents_proof(self):
        l=pipeline(cold=True,hold=True,active=None);l.execute("""
         assert(requests==1 and not net.TransactionCurrent(0));idle(100);assert(requests==1)
         assert(not pcall(net.CurrentCapitalSources,0,cities[1],'CULTURE'))
         holdPackets=false;UP.LoadScreenClose.Fire();gpDrain();idle(2)
         assert(requests==2 and net.TransactionCurrent(0))
        """)

    def test_unavailable_activity_getter_never_claims_proof_without_receipt(self):
        l=pipeline(cold=True,hold=True,active=False);l.execute("""
         Players[0].IsTurnActive=nil;UP.LoadScreenClose.Fire();idle(100)
         assert(requests==1 and not net.TransactionCurrent(0))
         Players[0].IsTurnActive=function()return true end
         holdPackets=false;UP.LocalPlayerTurnBegin.Fire();gpDrain();idle(2)
         assert(requests==2 and net.TransactionCurrent(0))
        """)

    def test_late_old_ack_cannot_clear_newer_flight(self):
        l=pipeline(cold=True,hold=True);l.execute('''
         UP.LoadScreenClose.Fire();assert(requests==2)
         deliver(1);gpDrain();UP.GameCoreEventPublishComplete.Fire()
         assert(requests==2 and pub.awaitingNetwork and inFlight==1)
         deliver(2);gpDrain();UP.GameCoreEventPublishComplete.Fire()
         assert(not pub.awaitingNetwork and inFlight==0)
         local seq=net.players[0].acceptedSeq;deliver(1);assert(net.players[0].acceptedSeq==seq)
        ''')

    def test_new_signal_before_retry_rejects_old_packet_and_confirms_current(self):
        l=pipeline(cold=True,hold=True);l.execute('''
         GP.UnitOperationStarted.Fire(0,10);UP.LoadScreenClose.Fire();assert(requests==2)
         assert(packets[2].Signal==shared.RouteSignalRevision and packets[2].Signal~=packets[1].Signal)
         deliver(1);assert(not net.TransactionCurrent(0))
         deliver(2);gpDrain();idle(2);assert(net.TransactionCurrent(0))
         assert(net.players[0].signal==packets[2].Signal)
        ''')

    def test_seen_but_rejected_packet_does_not_unlock_failed_turn(self):
        l=pipeline(cold=True,hold=True);l.execute('''
         packets[1].WireCount=999;deliver(1);UP.GameCoreEventPublishComplete.Fire()
         assert(not net.TransactionCurrent(0));local n=requests
         for i=1,10 do UP.LoadScreenClose.Fire();UP.LocalPlayerTurnBegin.Fire();idle(1)end
         assert(requests==n and not net.TransactionCurrent(0))
        ''')

    def test_throwing_send_remains_failed_turn_despite_lifecycle(self):
        l=pipeline();l.execute('''
         sendThrows=true;GP.UnitOperationStarted.Fire(0,10);UP.GameCoreEventPublishComplete.Fire()
         assert(requests==1);sendThrows=false
         for i=1,10 do UP.LoadScreenClose.Fire();UP.LocalPlayerTurnBegin.Fire();idle(1)end
         assert(requests==1 and not net.TransactionCurrent(0))
        ''')

    def test_receiver_epoch_change_discards_old_flight_and_uses_new_epoch(self):
        l=pipeline(cold=True,hold=True);l.execute('''
         local oldEpoch=net.epoch;net.epoch=oldEpoch+1;net.players={}
         UP.GameCoreEventPublishComplete.Fire();assert(requests==2 and packets[2].Epoch==net.epoch)
         deliver(1);assert(not net.TransactionCurrent(0))
         deliver(2);gpDrain();idle(2);assert(net.TransactionCurrent(0))
        ''')

    def test_isolation_and_shutdown_stop_recovery(self):
        for mode in ('isolate','shutdown'):
            with self.subTest(mode=mode):
                l=pipeline(cold=True,hold=True)
                if mode=='isolate':
                    l.execute("shared.NetworkIsolation={active=true,player=0,epoch=net.epoch,Active=function()return true end}")
                else:l.execute('shutdown()')
                l.execute('''
                 for i=1,10 do UP.LoadScreenClose.Fire();UP.LocalPlayerTurnBegin.Fire();idle(1)end
                 assert(requests==1 and not pub.awaitingNetwork and inFlight==0)
                ''')

    def test_actual_recovery_executes_without_unavailable_lua_libraries(self):
        l=pipeline(cold=True,hold=True,restricted=True);l.execute('''
         assert(_VERSION=='Lua 5.1' and requests==1)
         holdPackets=false;UP.LocalPlayerTurnBegin.Fire();gpDrain();idle(2)
         assert(requests==2 and net.TransactionCurrent(0))
        ''')


class StrictTransactions(unittest.TestCase):
    def test_actual_development_service_rejects_unknown_network_without_money(self):
        from test_b246_development import runtime
        lua=runtime()
        lua.execute("networkFail=true;assert(not sign() and moneyCalls==0)")


# Retain selected historical assertions under the current real FC/Lua51 fixture.
# No synthetic consumer notifications or assertion rewrites are used.
class ExistingProofGuards(unittest.TestCase):
    pass


def existing_guard(module_name, class_name, method_name):
    def run(self):
        from importlib import import_module
        from unittest.mock import patch
        import test_b232_network_revalidation as b232
        import test_b239_commerce_network as b239
        original=culture_module.fixture
        def adapted(*args, **kwargs):
            return fact_publication_profile(original(*args, **kwargs))
        with patch.object(culture_module,'LuaRuntime',TrackedLua51), \
             patch.object(b232,'fixture',adapted),patch.object(b239,'fixture',adapted):
            case=getattr(import_module(module_name),class_name)(method_name)
            result=unittest.TestResult();case.run(result)
        self.assertEqual(result.testsRun,1)
        self.assertFalse(result.failures or result.errors,
                         str(result.failures+result.errors))
    return run


for module_name,class_name,methods in (
    ('test_b232_network_revalidation','Revalidation',(
      'test_inflight_packet_is_not_duplicated',
      'test_rejected_equal_content_ack_does_not_resend_each_flush',
      'test_new_event_after_successful_receipt_before_ack_can_revalidate',
      'test_stale_partial_and_wrong_epoch_cannot_clear_pending',
      'test_successful_route_proof_does_not_hide_failed_derive',
      'test_generation_change_discards_old_proof_candidate',
      'test_ui_callback_guards_owner_epoch_shutdown_and_isolation')),
    ('test_b239_commerce_network','DirectDomesticPartners',(
      'test_no_refresh_fact_scan_publish_or_shared_mutable_projection',)),
    ('test_b239_commerce_network','TransportLimits',(
      'test_sender_route_limit_is_explicit_bounded_and_can_recover_same_turn',
      'test_sender_payload_limit_never_sends_partial_rows',
      'test_128_real_integer_routes_are_accepted_without_relaxing_the_cap'))):
    for method_name in methods:
        setattr(ExistingProofGuards,'test_existing_'+method_name[5:],
                existing_guard(module_name,class_name,method_name))


if __name__=='__main__':unittest.main()
