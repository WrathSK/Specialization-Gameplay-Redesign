"""B239 verified direct-pair reads and transport bounds. Local Lua fixtures only."""
from pathlib import Path
import unittest

from test_culture_network import fixture

ROOT = Path(__file__).resolve().parents[1]


class DirectDomesticPartners(unittest.TestCase):
    def test_direct_incoming_outgoing_dedup_without_transitive_distribution(self):
        lua = fixture(False)
        lua.execute("""
          send('0,4,0,2,10;0,2,0,4,11;0,2,0,1,12',3)
          local a=net.CurrentDomesticPartners(0,cities[4])
          assert(a.validity=='VERIFIED' and #a.partners==1 and a.partners[1]==2)
          assert(a.references[2]==SPCNetworkInput.Reference(cities[2]))
          assert(a.reference==SPCNetworkInput.Reference(cities[4]) and a.cityID==4)
          local b=net.CurrentDomesticPartners(0,cities[2])
          assert(#b.partners==2 and b.partners[1]==1 and b.partners[2]==4)
          assert(net.CurrentDomesticPartners(0,cities[1]).partners[1]==2)
        """)

    def test_foreign_route_is_not_a_domestic_partner(self):
        lua = fixture(False)
        lua.execute("""
          local foreign={GetOwner=function()return 1 end,GetID=function()return 2 end,
            GetX=function()return 99 end,GetY=function()return 100 end,GetProperty=function()return 'FOREIGN'end}
          Players[1]={GetCities=function()return {FindID=function()return foreign end}end}
          send('0,4,1,2,10',1)
          local a=net.CurrentDomesticPartners(0,cities[4])
          assert(a.validity=='VERIFIED' and #a.partners==0 and next(a.references)==nil)
        """)

    def test_missing_pending_and_confirmed_empty_are_distinct(self):
        lua = fixture(False)
        lua.execute("""
          local a=net.CurrentDomesticPartners(0,cities[4])
          assert(a.validity=='UNKNOWN' and a.partners==nil)
          send('',0);a=net.CurrentDomesticPartners(0,cities[4])
          assert(a.validity=='VERIFIED' and #a.partners==0)
          net.CheckEvidence(false);a=net.CurrentDomesticPartners(0,cities[4])
          assert(a.validity=='UNKNOWN' and a.partners==nil)
          send('',0);assert(net.CurrentDomesticPartners(0,cities[4]).validity=='VERIFIED')
        """)

    def test_no_refresh_fact_scan_publish_or_shared_mutable_projection(self):
        lua = fixture()
        lua.execute("""
          local scans=counts.city_scan;local derives=counts.derive;local rev=net.Input(0).inputVersion
          net.Refresh=function()error('READ_MUST_NOT_REFRESH')end
          net.Verified=function()error('READ_MUST_NOT_VERIFY_ALL_ROUTES')end
          shared.EffectiveFacts.Read=function()error('READ_MUST_NOT_READ_FACTS')end
          local a=net.CurrentDomesticPartners(0,cities[4]);assert(a.partners[1]==2)
          a.partners[1]=999;a.references[2]='MUTATED';a.input.epoch=999
          net.players[0].centers={};net.players[0].sources={};net.players[0].recipients={}
          for i=1,12 do
            local b=net.CurrentDomesticPartners(0,cities[4])
            assert(b.partners[1]==2 and b.references[2]~='MUTATED' and b.input.epoch==net.epoch)
          end
          assert(counts.city_scan==scans and counts.derive==derives and propertyWrites==0)
          assert(net.Input(0).inputVersion==rev)
        """)

    def test_reference_owner_and_epoch_changes_cannot_reuse_partner_set(self):
        for expression in [
            "cities[2].token='REPLACED'",
            "cities[4].token='REPLACED'",
            "cities[2].owner=1",
            "cities[4].owner=1",
            "net.epoch=net.epoch+1",
            "shared.RouteSignalRevision=shared.RouteSignalRevision+1",
        ]:
            with self.subTest(change=expression):
                lua = fixture()
                lua.execute(expression + ";local a=net.CurrentDomesticPartners(0,cities[4]);assert(a.validity=='UNKNOWN' and a.partners==nil)")

    def test_unreadable_reference_is_unknown_and_does_not_overwrite_accepted_view(self):
        lua = fixture()
        lua.execute("""
          local before=net.Input(0);local getter=cities[2].GetProperty
          cities[2].GetProperty=function()error('NATIVE_UNREADABLE')end
          local a=net.CurrentDomesticPartners(0,cities[4]);assert(a.validity=='UNKNOWN' and a.partners==nil)
          cities[2].GetProperty=getter;a=net.CurrentDomesticPartners(0,cities[4])
          assert(a.validity=='VERIFIED' and a.partners[1]==2 and a.input.inputVersion==before.inputVersion)
        """)

    def test_confirmed_loss_clears_direct_view_and_complete_recovery_replaces_it(self):
        lua = fixture()
        lua.execute("""
          cities[2].token='REPLACED';fire('CityTransfered',0)
          local a=net.CurrentDomesticPartners(0,cities[4]);assert(a.validity=='CONFIRMED_INVALID' and a.partners==nil)
          send('0,4,0,1,10',1);a=net.CurrentDomesticPartners(0,cities[4])
          assert(a.validity=='VERIFIED' and #a.partners==1 and a.partners[1]==1)
          assert(net.CurrentDomesticPartners(0,cities[2]).validity=='VERIFIED')
        """)


class TransportLimits(unittest.TestCase):
    def test_explicit_limit_holds_snapshot_notifies_commerce_once_and_recovers(self):
        for reason in ['NETWORK_ROUTE_LIMIT', 'NETWORK_PAYLOAD_LIMIT']:
            with self.subTest(reason=reason):
                lua = fixture()
                lua.globals().failure_reason = reason
                lua.execute("""
                  local rev=net.Input(0).inputVersion;local fingerprint=net.players[0].fingerprint
                  notices={};shared.Commerce={Audit=function(p)
                    notices[#notices+1]=p
                    local current=net.CurrentDomesticPartners(0,cities[4])
                    assert(current.validity==(p.availability=='AVAILABLE' and 'VERIFIED' or 'UNKNOWN'))
                  end}
                  function failPacket()
                    seq=seq+1;net.Receive(0,{Epoch=net.epoch,Seq=seq,Turn=turn,Signal=0,Valid=0,Failure=failure_reason,Count=129})
                  end
                  failPacket();local a=net.CurrentDomesticPartners(0,cities[4])
                  assert(a.validity=='UNKNOWN' and a.reason==failure_reason and a.partners==nil)
                  assert(net.Input(0).transportFailure==failure_reason and #notices==1)
                  assert(net.players[0].fingerprint==fingerprint and net.Input(0).inputVersion==rev)
                  net.Refresh(0);assert(net.players[0].error==failure_reason)
                  failPacket();assert(#notices==1)
                  send('0,4,0,2,10;0,2,0,1,11;0,2,0,5,12',3)
                  assert(#notices==2 and net.CurrentDomesticPartners(0,cities[4]).validity=='VERIFIED')
                  assert(net.Input(0).inputVersion==rev and net.Input(0).transportFailure==nil)
                """)

    def test_old_epoch_or_unrecognized_failure_never_installs_diagnostic_text(self):
        lua = fixture()
        lua.execute("""
          seq=seq+1;net.Receive(0,{Epoch=net.epoch-1,Seq=seq,Turn=turn,Signal=0,Valid=0,Failure='NETWORK_ROUTE_LIMIT'})
          assert(net.CurrentDomesticPartners(0,cities[4]).validity=='VERIFIED')
          seq=seq+1;net.Receive(0,{Epoch=net.epoch,Seq=seq,Turn=turn,Signal=0,Valid=0,Failure='UNTRUSTED_TEXT'})
          assert(net.Input(0).transportFailure==nil and net.players[0].error~='UNTRUSTED_TEXT')
        """)

    def sender(self):
        lua = fixture()
        lua.execute((ROOT/'Mod/NetworkSender.lua').read_text())
        lua.execute("""
          shared.Version=P.VERSION;ExposedMembers.SPC_P0=shared
          Game.GetLocalPlayer=function()return 0 end
          SPCPerformance={Flight=function()end};PlayerOperations={EXECUTE_SCRIPT=1};packets={}
          UI={RequestPlayerOperation=function(pid,op,p)packets[#packets+1]=p;net.Receive(pid,p)end}
          pump=SPCNetworkSender.New(P)
          pub={status='COMPLETE_UI_SHADOW',snapshot={turn=turn,signal=0,count=129,keys={},routes={},fingerprint='LIMIT'}}
        """)
        return lua

    def test_sender_route_limit_is_explicit_bounded_and_can_recover_same_turn(self):
        lua = self.sender()
        lua.execute("""
          pump(pub);assert(#packets==1 and packets[1].Valid==0 and packets[1].Failure=='NETWORK_ROUTE_LIMIT' and packets[1].Data=='EMPTY')
          assert(net.CurrentDomesticPartners(0,cities[4]).reason=='NETWORK_ROUTE_LIMIT')
          for i=1,10 do pump(pub)end;assert(#packets==1)
          pub.snapshot={turn=turn,signal=0,count=0,keys={},routes={},fingerprint=''};routeCount=0
          pump(pub);assert(#packets==2 and packets[2].Valid==1)
          assert(net.CurrentDomesticPartners(0,cities[4]).validity=='VERIFIED')
          pump(pub);assert(#packets==2)
        """)

    def test_sender_payload_limit_never_sends_partial_rows(self):
        lua = self.sender()
        lua.execute("""
          local keys,rows={},{}
          for i=1,128 do keys[i]=i;rows[i]={originPlayer=0,originCityID=string.rep('1',130),destinationPlayer=0,destinationCityID=2,traderUnitID=i}end
          pub.snapshot.count=128;pub.snapshot.keys=keys;pub.snapshot.routes=rows
          pump(pub);assert(#packets==1 and packets[1].Valid==0 and packets[1].Failure=='NETWORK_PAYLOAD_LIMIT' and packets[1].Data=='EMPTY')
          assert(net.CurrentDomesticPartners(0,cities[4]).reason=='NETWORK_PAYLOAD_LIMIT')
          pump(pub);assert(#packets==1)
        """)

    def test_128_real_integer_routes_are_accepted_without_relaxing_the_cap(self):
        lua = self.sender()
        lua.execute("""
          local keys,rows={},{}
          for i=1,128 do
            keys[i]=i;units[1000+i]={}
            rows[i]={originPlayer=0,originCityID=4,destinationPlayer=0,destinationCityID=2,traderUnitID=1000+i}
          end
          pub.snapshot.count=128;pub.snapshot.keys=keys;pub.snapshot.routes=rows;routeCount=128
          pump(pub);assert(#packets==1 and packets[1].Valid==1 and packets[1].Count==128 and #net.players[0].routes==128)
          local a=net.CurrentDomesticPartners(0,cities[4]);assert(a.validity=='VERIFIED' and #a.partners==1 and a.partners[1]==2)
        """)


if __name__ == '__main__':
    unittest.main()
