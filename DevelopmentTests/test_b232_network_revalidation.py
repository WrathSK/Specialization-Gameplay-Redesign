"""B232 actual sender/collector/bridge/Culture path. Local mocks, never native PASS."""
from pathlib import Path
import unittest
from test_culture_network import fixture

R = Path(__file__).resolve().parents[1]
M = R / 'Mod'
ROUTES = '0,4,0,2,10;0,2,0,1,11;0,2,0,5,12'


def pipeline(async_send=False):
    l = fixture()
    l.execute('''
      complete(4,1);cn.SourceChanged(0,4)
      GP=Events;UP=events();shared.Version=P.VERSION;ExposedMembers.SPC_P0=shared
      P.Scalar=tostring;P.Call=function(o,m,...)return pcall(o[m],o,...)end
      P.RouteUnitRelevant=function(pid,id)return units[id]~=nil end
      SPCPerformance={Flight=function()end};SPCP0=P
      PlayerOperations={EXECUTE_SCRIPT=1};requests=0;proofFailures=0;deliveries={};routeRows={}
      for _,r in ipairs(net.players[0].routes)do routeRows[#routeRows+1]={
        OriginCityPlayer=r.op,OriginCityID=r.oc,DestinationCityPlayer=r.dp,DestinationCityID=r.dc,TraderUnitID=r.trader}end
      for _,c in pairs(cities)do c.GetTrade=function()return {GetOutgoingRoutes=function()
        if uiReadFail then error('NATIVE_ROUTE_READ_UNAVAILABLE')end
        local rows={};for _,r in ipairs(routeRows)do if r.OriginCityID==c.id then rows[#rows+1]=r end end;return rows
      end}end end
      Players[0].GetTrade=function()return {CountOutgoingRoutes=function()return #routeRows end,
        GetNumOutgoingRoutes=function()return #routeRows end}end
      ContextPtr={SetInitHandler=function(_,f)init=f end,SetShutdown=function(_,f)shutdown=f end,
        SetUpdate=function()error('TIMER_FORBIDDEN')end,ClearUpdate=function()end}
      UI={RequestPlayerOperation=function(pid,op,p)
        if p.Action=='NETWORK_REVALIDATE_FAILURE'then proofFailures=proofFailures+1;net.CheckEvidence(true);return end
        requests=requests+1
        if asyncSend then deliveries[#deliveries+1]=p
        else if rejectPacket then p.WireCount=999 end;net.Receive(pid,p)end
      end}
      Events=UP
    ''')
    l.globals().asyncSend = async_send
    def include(name):
        if name != 'Probe':
            l.execute((M / (name + '.lua')).read_text())
    l.globals().include = include
    l.execute((M / 'UI/BackgroundRoutes.lua').read_text())
    l.execute('init();pub=ExposedMembers.SPC_P0_BackgroundRoutes;assert(requests==0)')
    return l


class Revalidation(unittest.TestCase):
    def test_nontrader_gameplay_invalidation_reaches_ui_despite_ui_filter(self):
        l=pipeline();l.execute('''
          local scans=counts.route_scan;local rev=net.Input(0).inputVersion;local derives=counts.derive
          GP.UnitRemovedFromMap.Fire(0,999);UP.UnitRemovedFromMap.Fire(0,999)
          complete(4,2);cn.SourceChanged(0,4)
          assert(counts.route_scan==scans and requests==0 and amount(cities[1])==1)
          UP.GameCoreEventPublishComplete.Fire()
          assert(requests==1 and counts.route_scan==scans+1)
          assert(net.Input(0).availability=='AVAILABLE' and amount(cities[1])==2 and amount(cities[5])==2)
          assert(net.Input(0).inputVersion==rev and counts.derive==derives and propertyWrites==0)
        ''')

    def test_available_insight_event_updates_only_dependent_receivers_immediately(self):
        l=pipeline();l.execute('''
          local derives=counts.derive;local rev=net.Input(0).inputVersion;local scans=counts.route_scan
          factReads={};historyReads={};complete(4,2);cn.SourceChanged(0,4)
          assert(amount(cities[1])==2 and amount(cities[5])==2 and amount(cities[3])==0)
          assert(historyReads[4]==1 and not factReads[3] and factReads[4]==1)
          assert(requests==0 and counts.route_scan==scans and counts.derive==derives and net.Input(0).inputVersion==rev)
          local writes=created+removed;cn.SourceChanged(0,4);assert(created+removed==writes)
          cn.SourceChanged(9,4);assert(created+removed==writes and propertyWrites==0)
        ''')

    def test_changed_candidate_publishes_available_before_consumer_notification(self):
        l=pipeline();l.execute('''
          net.CheckEvidence(false);complete(4,2);routeRows[3].TraderUnitID=13
          local observed={};shared.StandardizationEffects={Audit=function(p)
            observed[#observed+1]=p;assert(p.availability=='AVAILABLE');assert(net.CurrentNational(0))
          end}
          UP.GameCoreEventPublishComplete.Fire()
          assert(#observed==1 and net.players[0].revalidation=='VERIFIED' and amount(cities[1])==2)
          assert(net.Input(0).inputVersion==2 and net.Input(0).derivedFor==2)
        ''')

    def test_recovery_notifies_all_named_consumers_once_without_new_input(self):
        l=pipeline();l.execute('''
          watched={};for _,n in ipairs({'Lv3Effects','StandardizationEffects','Commerce'})do
            local name=n;watched[name]=0;shared[name]={Audit=function(p)
              watched[name]=watched[name]+1;assert(p.player==0 and p.availability=='AVAILABLE')
              local again=net.Refresh(0);assert(again==false)
              assert(net.CurrentNational(0) and net.CurrentCultureBatch(0).input.availability=='AVAILABLE' and net.CurrentIndustryBatch(0).input.availability=='AVAILABLE')
            end}
          end
          local original=cn.Audit;local calls=0;cn.Audit=function(p)calls=calls+1;original(p)end
          net.CheckEvidence(false);UP.GameCoreEventPublishComplete.Fire()
          assert(calls==1);for _,n in pairs(watched)do assert(n==1)end
          local writes=created+removed;local derives=counts.derive;local sent=requests
          for i=1,8 do UP.GameCoreEventPublishComplete.Fire();UP.GameCoreEventPlaybackComplete.Fire();UP.SystemUpdateUI.Fire();net.Refresh(0)end
          assert(calls==1 and created+removed==writes and counts.derive==derives and requests==sent)
        ''')

    def test_unknown_city_facts_remain_pending_after_route_proof_then_recover(self):
        l=pipeline();l.execute('''
          readFail=true;net.CheckEvidence(false);UP.GameCoreEventPublishComplete.Fire()
          assert(net.players[0].revalidation=='VERIFIED' and net.Input(0).availability=='NEEDS_REVALIDATION')
          local sent=requests;local derives=counts.derive;local rev=net.Input(0).inputVersion
          complete(4,2);cn.SourceChanged(0,4);assert(amount(cities[1])==1)
          UP.GameCoreEventPublishComplete.Fire();assert(requests==sent)
          readFail=false;GP.GovernorChanged.Fire(0)
          assert(net.Input(0).availability=='AVAILABLE' and amount(cities[1])==2)
          assert(net.Input(0).inputVersion==rev and counts.derive==derives and propertyWrites==0)
        ''')

    def test_burst_dirty_events_coalesce_one_native_scan_and_packet(self):
        l=pipeline();l.execute('''
          local scans=counts.route_scan;local writes=created+removed;local derives=counts.derive
          for i=1,12 do GP.UnitRemovedFromMap.Fire(0,999)end
          assert(counts.route_scan==scans and requests==0)
          UP.GameCoreEventPublishComplete.Fire();UP.GameCoreEventPlaybackComplete.Fire()
          assert(requests==1 and counts.route_scan==scans+1 and counts.derive==derives and created+removed==writes)
        ''')

    def test_inflight_packet_is_not_duplicated(self):
        l=pipeline(True);l.execute('''
          net.CheckEvidence(false);UP.GameCoreEventPublishComplete.Fire()
          for i=1,6 do UP.GameCoreEventPlaybackComplete.Fire()end
          assert(requests==1 and #deliveries==1)
          net.Receive(0,deliveries[1]);UP.GameCoreEventPublishComplete.Fire()
          assert(requests==1 and not pub.awaitingNetwork and net.Input(0).availability=='AVAILABLE')
        ''')

    def test_rejected_equal_content_ack_does_not_resend_each_flush(self):
        l=pipeline();l.execute('''
          rejectPacket=true;net.CheckEvidence(false);UP.GameCoreEventPublishComplete.Fire()
          local accepted=net.players[0].acceptedSeq
          for i=1,6 do UP.GameCoreEventPublishComplete.Fire();UP.SystemUpdateUI.Fire()end
          assert(requests==1 and net.players[0].acceptedSeq==accepted and net.Input(0).availability=='NEEDS_REVALIDATION')
          rejectPacket=false;turn=turn+1;UP.PlayerTurnActivated.Fire(0)
          assert(requests==2 and net.Input(0).availability=='AVAILABLE')
        ''')

    def test_new_event_after_successful_receipt_before_ack_can_revalidate(self):
        l=pipeline(True);l.execute('''
          net.CheckEvidence(false);UP.GameCoreEventPublishComplete.Fire();net.Receive(0,deliveries[1])
          net.CheckEvidence(false);UP.GameCoreEventPublishComplete.Fire()
          assert(requests==2);net.Receive(0,deliveries[2]);UP.GameCoreEventPublishComplete.Fire()
          assert(requests==2 and net.Input(0).availability=='AVAILABLE')
        ''')

    def test_ui_failure_is_bounded_and_a_new_insight_is_a_fresh_event(self):
        l=pipeline();l.execute('''
          uiReadFail=true;local scans=counts.route_scan;net.CheckEvidence(false)
          for i=1,8 do UP.GameCoreEventPublishComplete.Fire()end
          assert(counts.route_scan==scans+3 and proofFailures==1 and requests==0)
          uiReadFail=false;complete(4,2);cn.SourceChanged(0,4)
          assert(amount(cities[1])==1);UP.GameCoreEventPublishComplete.Fire()
          assert(amount(cities[1])==2 and requests==1)
        ''')

    def test_ui_callback_guards_owner_epoch_shutdown_and_isolation(self):
        l=pipeline();l.execute('''
          local scans=counts.route_scan
          assert(not pub.RequestRevalidation(net.epoch-1,0) and not pub.RequestRevalidation(net.epoch,9))
          UP.GameCoreEventPublishComplete.Fire();assert(counts.route_scan==scans)
          shared.NetworkIsolation={active=true,player=0,epoch=net.epoch,Active=function()return true end}
          assert(not pub.RequestRevalidation(net.epoch,0));cn.SourceChanged(0,4)
          UP.GameCoreEventPublishComplete.Fire();assert(counts.route_scan==scans and requests==0)
          shutdown();assert(not pub.RequestRevalidation(net.epoch,0))
        ''')

    def test_callback_failure_does_not_invent_success_or_block_event_refresh(self):
        l=pipeline();l.execute('''
          local callback=pub.RequestRevalidation;pub.RequestRevalidation=function()error('UI_UNAVAILABLE')end
          net.CheckEvidence(false);assert(net.Input(0).availability=='NEEDS_REVALIDATION')
          pub.RequestRevalidation=callback;UP.PlayerTurnActivated.Fire(0)
          assert(net.Input(0).availability=='AVAILABLE')
        ''')

    def test_confirmed_loss_removes_old_effect_and_valid_empty_recovers(self):
        l=pipeline();l.execute('''
          units[10]=nil;GP.UnitRemovedFromMap.Fire(0,10)
          assert(net.Input(0).validity=='CONFIRMED_INVALID' and amount(cities[1])==0)
          routeRows={};UP.GameCoreEventPublishComplete.Fire()
          assert(net.Input(0).availability=='AVAILABLE' and #net.players[0].routes==0 and amount(cities[1])==0)
          assert(propertyWrites==0)
        ''')

    def test_unknown_new_city_and_known_route_loss_preserve_withdrawal(self):
        l=pipeline();l.execute('''
          local original=SPCNetworkInput.Capture;SPCNetworkInput.Capture=function()error('NETWORK_FACTS_UNAVAILABLE')end
          net.CheckEvidence(false);table.remove(routeRows,1);UP.GameCoreEventPublishComplete.Fire()
          assert(net.Input(0).validity=='CONFIRMED_INVALID' and amount(cities[1])==0)
          SPCNetworkInput.Capture=original
        ''')

    def test_stale_partial_and_wrong_epoch_cannot_clear_pending(self):
        for field,value in [('Turn','turn-1'),('Signal','99'),('WireCount','2'),('Data',"'0,4,0,2,10'"),('Epoch','net.epoch-1')]:
            with self.subTest(field=field):
                l=pipeline(True);l.execute('net.CheckEvidence(false);UP.GameCoreEventPublishComplete.Fire();p=deliveries[1]')
                l.execute('p.'+field+'='+value+';net.Receive(0,p)')
                l.execute("assert(net.Input(0).availability=='NEEDS_REVALIDATION' and amount(cities[1])==1)")

    def test_successful_route_proof_does_not_hide_failed_derive(self):
        l=pipeline();l.execute('''
          local original=SPCNetworkInput.Capture
          SPCNetworkInput.Capture=function(...)
            local x=original(...);x.signature='DIFFERENT';x.cities[1].potential=nil;return x
          end
          net.CheckEvidence(false);UP.GameCoreEventPublishComplete.Fire()
          assert(net.Input(0).availability=='NEEDS_REVALIDATION' and net.players[0].error)
          assert(amount(cities[1])==1)
        ''')

    def test_generation_change_discards_old_proof_candidate(self):
        l=pipeline(True);l.execute('''
          net.CheckEvidence(false);UP.GameCoreEventPublishComplete.Fire();local old=deliveries[1]
          capitalFail=true;net.Receive(0,old);assert(net.players[0].candidate)
          turn=turn+1;capitalFail=false;net.Refresh(0)
          assert(not net.players[0].candidate and net.Input(0).availability=='NEEDS_REVALIDATION')
          UP.PlayerTurnActivated.Fire(0);net.Receive(0,deliveries[2])
          assert(net.Input(0).availability=='AVAILABLE')
        ''')

    def test_report_read_does_not_request_proof_or_refresh(self):
        l=pipeline();l.execute('''
          net.CheckEvidence(false);local before=counts.route_scan;local calls=0
          pub.RequestRevalidation=function()calls=calls+1 end
          local text=net.Report(0,cities[1],false)
          assert(text:find('NETWORK_REVALIDATION_PENDING') and calls==0 and counts.route_scan==before and requests==0)
        ''')

if __name__=='__main__': unittest.main()
