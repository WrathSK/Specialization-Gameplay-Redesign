"""Real Bridge/Commerce and Sender busy boundaries; explicit native wire/event doubles."""
import unittest
from refactor_harness import ROOT,legacy_source_observation,measure
from refactor_defect_fixtures import commerce,fact_publication_profile


def fixture():
    l=commerce();fact_publication_profile(l,False)
    l.execute("fixtureDrain=true;function packet(n,data)return {Epoch=net.epoch,Seq=n,Turn=turn,Signal=shared.RouteSignalRevision,Valid=1,Count=3,Data=data or '0,4,0,2,10;0,2,0,1,11;0,2,0,5,12'}end;beforeSeq=net.players[0].seq;beforeAccepted=net.players[0].acceptedSeq;captures=0;local original=SPCNetworkInput.Capture;SPCNetworkInput.Capture=function(...)captures=captures+1;return original(...)end")
    return l


class Busy(unittest.TestCase):
    def test_latest_detached_packet_no_early_ack_and_freshness_guard(self):
        l=fixture();l.execute("""
        assert(toggle(2,'DISTRICT_CAMPUS',true));local gold=ownedGold(cities[2]);local original=SPCNetworkInput.Capture;local once=true
        SPCNetworkInput.Capture=function(...)
         local value=original(...);if once then once=false
          local a=packet(beforeSeq+10,'0,4,0,2,10;0,2,0,1,11;0,2,0,3,12')
          local b=packet(beforeSeq+11,'0,4,0,2,10;0,2,0,3,11;0,2,0,5,12')
          net.Receive(0,a);net.Receive(0,b);b.Data='CORRUPTED_AFTER_ENQUEUE'
          assert(net.players[0].seq==beforeSeq and net.players[0].acceptedSeq==beforeAccepted and not net.TransactionCurrent(0))
         end;return value
        end
        net.Refresh(0);assert(net.players[0].queuedWork and ownedGold(cities[2])==gold and not pcall(net.CurrentCapitalSources,0,cities[2],'RESEARCH'))
        assert(net.CurrentOutgoingDomestic(0,cities[2]).validity=='UNKNOWN')
        net.FlushPending();assert(net.players[0].seq==beforeSeq+11 and net.players[0].acceptedSeq==beforeSeq+11 and not net.players[0].queuedWork)
        local partners=net.CurrentOutgoingDomestic(0,cities[2]).partners;assert(#partners==2 and partners[1]==3 and partners[2]==5)
        assert(not net.FlushPending() and captures==2)
        """)
    def test_many_busy_refreshes_merge_once_then_thousand_idle_do_nothing(self):
        l=fixture();l.execute("local original=SPCNetworkInput.Capture;local once=true;SPCNetworkInput.Capture=function(...)local v=original(...);if once then once=false;for i=1,10 do net.Refresh(0)end end;return v end;net.Refresh(0);assert(captures==1 and net.players[0].queuedWork);net.FlushPending();assert(captures==2 and not net.players[0].queuedWork);for i=1,1000 do Events.GameCoreEventPublishComplete.Fire()end;assert(captures==2)")
        measure('S5c2_busy_refresh_budget',{'initial_captures':1,'ten_reentrant_causes_additional_captures':1,'thousand_idle_additional_captures':0})
    def test_packet_during_receive_validation_is_queued_not_nested_overwrite(self):
        l=fixture();l.execute("""
        local get=cities[2].GetOwner;local once=true
        cities[2].GetOwner=function()if once then once=false;net.Receive(0,packet(beforeSeq+21,'0,4,0,2,10;0,2,0,3,11;0,2,0,5,12'));assert(net.players[0].seq==beforeSeq+20 and net.players[0].acceptedSeq==beforeAccepted)end;return get()end
        net.Receive(0,packet(beforeSeq+20));assert(net.players[0].seq==beforeSeq+20 and not net.players[0].receiving)
        net.FlushPending();assert(net.players[0].acceptedSeq==beforeSeq+21 and not net.players[0].receiving)
        local p=net.CurrentOutgoingDomestic(0,cities[2]).partners;assert(p[1]==3 and p[2]==5)
        """)
    def test_stale_queued_turn_or_signal_revalidates_without_success(self):
        for stale in ('turn=turn+1','shared.RouteSignalRevision=shared.RouteSignalRevision+1'):
            l=fixture();l.execute("net.players[0].refreshing=true;net.Receive(0,packet(beforeSeq+30));net.players[0].refreshing=false;"+stale+";net.FlushPending();assert(net.players[0].acceptedSeq==beforeAccepted and not net.TransactionCurrent(0) and not net.players[0].queuedWork and not net.players[0].receiving)")
    def test_failure_consumes_only_real_cause_and_next_event_can_recover(self):
        l=fixture();l.execute("local original=SPCNetworkInput.Capture;local once=true;SPCNetworkInput.Capture=function(...)captures=captures+1;if once then once=false;net.Refresh(0)end;error('CAPTURE_UNAVAILABLE')end;net.Refresh(0);net.FlushPending();assert(captures==2 and not net.TransactionCurrent(0));for i=1,1000 do Events.GameCoreEventPublishComplete.Fire()end;assert(captures==2);SPCNetworkInput.Capture=original;net.Refresh(0);assert(net.TransactionCurrent(0))")
    def test_actual_new_reentry_during_drain_survives_next_boundary(self):
        l=fixture();l.execute("""
        local original=SPCNetworkInput.Capture;local budget=2
        SPCNetworkInput.Capture=function(...)local v=original(...);if budget>0 then budget=budget-1;net.Refresh(0)end;return v end
        net.Refresh(0);net.FlushPending();assert(captures==2 and net.players[0].queuedWork)
        net.FlushPending();assert(captures==3 and not net.players[0].queuedWork)
        """)
    def test_busy_wire_limit_replay_and_unknown_object_do_not_enter_queue(self):
        l=fixture();l.execute("net.players[0].refreshing=true;local replay=packet(beforeSeq);net.Receive(0,replay);local large=packet(beforeSeq+40);large.Data=string.rep('x',16385);net.Receive(0,large);local object=packet(beforeSeq+41);object.Data={};net.Receive(0,object);net.players[0].refreshing=false;assert(not net.FlushPending() and net.players[0].seq==beforeSeq and net.players[0].acceptedSeq==beforeAccepted)")


class Negative(unittest.TestCase):
    def test_confirmed_exit_during_capture_wins_over_positive_candidate(self):
        l=fixture();l.execute("""
        local original=SPCNetworkInput.Capture;local once=true
        SPCNetworkInput.Capture=function(...)local value=original(...);if once then once=false
         net.Receive(0,packet(beforeSeq+50));cities[4].owner=1
         local ok,err=pcall(exits.NetworkBridge,cities[4],{confirmed=true,origin={owner=0,cityID=4}})
         assert(not ok and tostring(err):find('EXIT_NETWORK_QUEUED'))
        end;return value end
        net.Refresh(0);assert(not net.players[0].input.cities[4] and net.Input(0).continuityOnly and not net.TransactionCurrent(0))
        net.FlushPending();assert(not net.players[0].input.cities[4] and net.players[0].acceptedSeq==beforeAccepted)
        """)
    def test_native_unit_loss_during_capture_has_bounded_urgent_negative_check(self):
        l=fixture();l.execute("local original=SPCNetworkInput.Capture;local once=true;SPCNetworkInput.Capture=function(...)local value=original(...);if once then once=false;units[10]=nil;net.CheckEvidence(false,'UNIT_REMOVED')end;return value end;net.Refresh(0);for _,row in ipairs(net.players[0].routes)do assert(row.trader~=10)end;assert(net.Input(0).continuityOnly and not net.TransactionCurrent(0));local n=captures;for i=1,1000 do Events.GameCoreEventPublishComplete.Fire()end;assert(captures==n)")
    def test_failed_negative_is_dormant_not_lost_or_idle_retried(self):
        l=fixture();l.execute("""
        local capture=SPCNetworkInput.Capture;local signature=SPCNetworkInput.Signature;local once=true;local failures=0
        SPCNetworkInput.Signature=function(input)if input.negativeProof then failures=failures+1;error('NEGATIVE_FAILED')end;return signature(input)end
        SPCNetworkInput.Capture=function(...)local value=capture(...);if once then once=false;cities[4].owner=1;pcall(exits.NetworkBridge,cities[4],{confirmed=true,origin={owner=0,cityID=4}})end;return value end
        net.Refresh(0);assert(net.players[0].negativeHeld and net.players[0].input.cities[4] and not net.TransactionCurrent(0));local count=failures
        for i=1,1000 do Events.GameCoreEventPublishComplete.Fire()end;assert(failures==count)
        SPCNetworkInput.Signature=signature;net.Refresh(0);assert(not net.players[0].negativeHeld and not net.players[0].input.cities[4])
        """)

    def test_queued_positive_input_holds_gold_even_during_actual_commerce_audit(self):
        l=fixture();l.execute("""
        assert(toggle(2,'DISTRICT_CAMPUS',true));local gold=ownedGold(cities[2])
        net.players[0].refreshing=true;net.Receive(0,packet(beforeSeq+60));net.players[0].refreshing=false
        cities[1].yields.SCIENCE=1000;com.Audit({player=0,city=2});assert(ownedGold(cities[2])==gold)
        net.FlushPending();assert(net.players[0].acceptedSeq==beforeSeq+60)
        com.Audit({player=0,city=2});assert(ownedGold(cities[2])>gold)
        """)
    def test_failed_negative_keeps_coqueued_wire_until_new_evidence(self):
        l=fixture();l.execute("""
        local capture=SPCNetworkInput.Capture;local signature=SPCNetworkInput.Signature;local once=true;local failures=0
        SPCNetworkInput.Signature=function(input)if input.negativeProof then failures=failures+1;error('NEGATIVE_FAILED')end;return signature(input)end
        SPCNetworkInput.Capture=function(...)local value=capture(...);if once then once=false
         units[13]=units[11];net.Receive(0,packet(beforeSeq+61,'0,4,0,2,13;0,2,0,1,11;0,2,0,5,12'));units[10]=nil;net.CheckEvidence(false,'UNIT_REMOVED')
        end;return value end
        net.Refresh(0);assert(net.players[0].negativeHeld and not net.players[0].refreshing and not net.players[0].receiving)
        assert(net.players[0].acceptedSeq==beforeAccepted and not net.TransactionCurrent(0));local count=failures
        for i=1,1000 do Events.GameCoreEventPublishComplete.Fire()end;assert(failures==count and net.players[0].acceptedSeq==beforeAccepted)
        SPCNetworkInput.Signature=signature;net.CheckEvidence(false,'NEW_RELIABLE_FACT');net.FlushPending()
        assert(not net.players[0].negativeHeld and net.players[0].acceptedSeq==beforeSeq+61)
        for _,row in ipairs(net.players[0].routes)do assert(row.trader~=10)end
        """)
    def test_failed_negative_keeps_coqueued_refresh_no_idle_retry(self):
        l=fixture();l.execute("""
        local capture=SPCNetworkInput.Capture;local signature=SPCNetworkInput.Signature;local once=true;local failures=0
        SPCNetworkInput.Signature=function(input)if input.negativeProof then failures=failures+1;error('NEGATIVE_FAILED')end;return signature(input)end
        SPCNetworkInput.Capture=function(...)local value=capture(...);if once then once=false;net.Refresh(0);units[10]=nil;net.CheckEvidence(false,'UNIT_REMOVED')end;return value end
        net.Refresh(0);assert(net.players[0].negativeHeld and not net.players[0].refreshing);local count=failures;local reads=captures
        for i=1,1000 do Events.GameCoreEventPublishComplete.Fire()end;assert(failures==count and captures==reads)
        SPCNetworkInput.Signature=signature;net.CheckEvidence(false,'NEW_RELIABLE_FACT');net.FlushPending()
        assert(not net.players[0].negativeHeld and captures>reads)
        """)
    def test_failed_full_read_does_not_rearm_ui_request_while_busy(self):
        l=fixture();l.execute("""
        requests=0;ExposedMembers.SPC_P0_BackgroundRoutes={RequestRevalidation=function()requests=requests+1 end}
        local capture=SPCNetworkInput.Capture;local once=true
        SPCNetworkInput.Capture=function(...)local value=capture(...);if once then once=false;net.CheckEvidence(true,'EXHAUSTED_UI_READ')end;return value end
        net.Refresh(0);net.FlushPending();assert(requests==0)
        net.CheckEvidence(false,'NEW_NATIVE_CAUSE');assert(requests==1)
        """)

    def test_confirmed_route_loss_and_other_unknown_preserve_negative_continuity(self):
        l=fixture();l.execute("""
        units[10]=nil;local get=cities[1].GetOwner;cities[1].GetOwner=function()error('TEMPORARY_NATIVE_UNKNOWN')end
        net.CheckEvidence(false,'MIXED_EVIDENCE');assert(net.Input(0).continuityOnly)
        local traders={};for _,row in ipairs(net.players[0].routes)do traders[row.trader]=true end
        assert(not traders[10] and traders[11] and traders[12] and not net.TransactionCurrent(0));cities[1].GetOwner=get
        """)
    def test_native_evidence_dominates_failed_read_in_both_orders(self):
        for order in ('net.CheckEvidence(true);net.CheckEvidence(false)','net.CheckEvidence(false);net.CheckEvidence(true)'):
            l=fixture();l.execute("requests=0;ExposedMembers.SPC_P0_BackgroundRoutes={RequestRevalidation=function()requests=requests+1 end};net.players[0].refreshing=true;"+order+";net.players[0].refreshing=false;net.FlushPending();assert(requests==1);for i=1,1000 do Events.GameCoreEventPublishComplete.Fire()end;assert(requests==1)")
    def test_experimental_stop_discards_pending_without_new_dispatch(self):
        l=fixture();l.execute("""
        net.players[0].refreshing=true;net.Refresh(0);net.Receive(0,packet(beforeSeq+70));net.players[0].refreshing=false
        shared.NetworkIsolation={Active=function(pid)return pid==0 end};net.ExperimentalStop(0)
        local proof=net.ProofRevision(0);local reads=captures;local seq=shared.FactChanges.sequence
        for i=1,1000 do net.FlushPending()end
        assert(net.ProofRevision(0)==proof and captures==reads and shared.FactChanges.sequence==seq)
        assert(not net.players[0].queuedWork and not net.players[0].negativeHeld)
        """)


class Namespaces(unittest.TestCase):
    def test_existing_gameevent_route_signals_are_not_events_namespace_absence(self):
        l=fixture();l.execute("local n=shared.RouteSignalRevision;GameEvents.CityConquered.Fire(0,1,2);GameEvents.TradeRoutePlundered.Fire(0);assert(shared.RouteSignalRevision==n+2)")
    def test_foreign_pillage_actor_does_not_hide_supported_victim(self):
        from test_refactor_s5c1 import depth
        c=depth();c.execute("sample(1);sample(2);resetCounts();GameEvents.OnPillage.Fire(1,10,0,0,0,99);sample(1);sample(2);assert(counts.dc_capture==2 and fc.pending==1)")


class Sender(unittest.TestCase):
    def test_real_sender_does_not_misclassify_queued_receive_as_failed_ack(self):
        l=fixture()
        with legacy_source_observation():l.globals().include('NetworkSender')
        l.execute("""
        ExposedMembers.SPC_P0={Version=P.VERSION,NetworkBridge=net,RouteSignalRevision=shared.RouteSignalRevision}
        SPCPerformance={Flight=function(n)flight=n end};PlayerOperations={EXECUTE_SCRIPT=1}
        UI={RequestPlayerOperation=function(pid,_,p)net.Receive(pid,p)end};Game.GetLocalPlayer=function()return 0 end
        public={status='COMPLETE_UI_SHADOW',snapshot={count=3,turn=turn,signal=shared.RouteSignalRevision,fingerprint=net.players[0].fingerprint,keys={'a','b','c'},routes={
         a={originPlayer=0,originCityID=4,destinationPlayer=0,destinationCityID=2,traderUnitID=10},
         b={originPlayer=0,originCityID=2,destinationPlayer=0,destinationCityID=1,traderUnitID=11},
         c={originPlayer=0,originCityID=2,destinationPlayer=0,destinationCityID=5,traderUnitID=12}}}}
        net.players[0].revalidation='NEEDS_REVALIDATION';net.players[0].refreshing=true;local pulse=SPCNetworkSender.New(P)
        pulse(public);assert(flight==1 and net.players[0].seq==beforeSeq);pulse(public)
        assert(flight==1 and not counts.send_timeout and public.senderFailedTurn=='NONE')
        net.players[0].refreshing=false;net.FlushPending();pulse(public)
        assert(flight==0 and net.players[0].acceptedSeq>beforeAccepted and not counts.send_timeout and public.senderFailedTurn=='NONE')
        """)

if __name__=='__main__':unittest.main()
