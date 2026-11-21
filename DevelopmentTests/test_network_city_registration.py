"""A fresh domestic route and the Store's city registration are independent inputs."""
import unittest
from unittest.mock import patch

from lupa.lua51 import LuaRuntime
import test_store_write_boundaries as store_fixture
from test_city_peaceful_acquisition import SETUP


NETWORK = """
home=T.fresh(1);T.register(home);T.complete(home,'DISTRICT_COMMERCIAL_HUB')
partner=T.fresh(2);T.register(partner);T.complete(partner,'DISTRICT_CAMPUS')
incoming=sourceCity(3)
Players[0].GetCities=function()
 local own={home,partner}
 if incoming:GetOwner()==0 then own[#own+1]=incoming end
 return {Members=function()return ipairs(own)end,
         FindID=function(_,id)return CityManager.GetCity(0,id)end,
         GetCapitalCity=function()return home end}
end
local nativeUnits=Players[0]:GetUnits()
Players[0].GetUnits=function()
 return {FindID=function(_,id)if id==41 then return {id=id} end;return nativeUnits:FindID(id)end}
end
Players[0].GetTrade=function()return {CountOutgoingRoutes=function()return 1 end}end
function startNetwork()
 shared.CityFlowProbe=nil -- retired from the production package
 ExposedMembers=ExposedMembers or {}
 include('FactChanges');SPCFactChanges.New(shared)
 include('NetworkBridge');SPCNetworkBridge.Start(P,shared)
 net=shared.NetworkBridge;Events.GameCoreEventPublishComplete.Fire()
 seq=0
end
function prove()
 seq=seq+1
 net.Receive(0,{Epoch=net.epoch,Seq=seq,Turn=Game.GetCurrentGameTurn(),Signal=shared.RouteSignalRevision,
  Valid=1,WireCount=2,Data=table.concat({0,home:GetID(),0,partner:GetID(),41},',')})
 local b=assert(net.players[0])
 assert(b.revalidation=='VERIFIED' and b.acceptedSeq==seq and #b.routes==1,b.error)
 assert(b.input.cities[home:GetID()].specialization=='COMMERCE')
 assert(b.input.cities[partner:GetID()].specialization=='RESEARCH')
 return b.input.cities[incoming:GetID()]
end
function checkGate(ready)
 assert(net.TransactionCurrent(0)==ready)
 local ok,capital=pcall(net.CurrentCapitalSources,0,home,'RESEARCH')
 assert(ok==ready and (ready or tostring(capital):find('CAPITAL_NETWORK_PENDING',1,true)))
 local outgoing=net.CurrentOutgoingDomestic(0,home)
 if ready then
  assert(outgoing.validity=='VERIFIED' and #outgoing.partners==1 and outgoing.partners[1]==partner:GetID())
 else
  assert(outgoing.validity=='UNKNOWN' and outgoing.reason=='NETWORK_REVALIDATION_PENDING')
 end
end
function minorSource(civ,level)
 Players[3].IsMajor=function()return false end
 PlayerConfigurations={[3]={GetCivilizationTypeName=function()return civ end}}
 local info=P.Info
 P.Info=function(t,k)
  if t=='Civilizations' and k==civ then
   return {StartingCivilizationLevelType=level}
  end
  return info(t,k)
 end
end
function freeSource() minorSource('CIVILIZATION_FREE_CITIES','CIVILIZATION_LEVEL_FREE_CITIES') end
function beginConquest()
 local old=incoming:GetID()
 incoming.s.ref.owner,incoming.s.ref.cityID=0,902
 local x,y=incoming:GetX(),incoming:GetY()
 GameEvents.CityBuilt.Fire(0,902,x,y)
 GameEvents.CityConquered.Fire(0,3,902,x,y)
 Events.CityRemovedFromMap.Fire(3,old);Events.CityAddedToMap.Fire(0,902,x,y)
 Events.CityInitialized.Fire(0,902,x,y)
end
function checkRegistered()
 local row=prove()
 assert(row.specialization=='NONE' and row.provenance=='CONFIRMED' and row.active==0)
 checkGate(true)
end
function checkUnresolved()
 local row=prove()
 assert(row.provenance=='UNKNOWN' and row.specialization=='UNKNOWN')
 checkGate(false)
end
startNetwork()
"""


def registration():
    with patch.object(store_fixture, 'LuaRuntime', LuaRuntime):
        lua = store_fixture.fixture()
    lua.execute(SETUP)
    lua.execute(NETWORK)
    return lua


class Registration(unittest.TestCase):
    def setUp(self):
        self.lua = registration()

    def test_gift_waits_for_terminal_identity_and_fresh_route_proof(self):
        self.lua.execute("""
        assert(prove()==nil);checkGate(true)
        local before=T.encode(T.record(home))
        mapTransfer(incoming,0,902)
        assert(not T.record(incoming));checkUnresolved()
        final(incoming,CityTransferTypes.BY_GIFT)
        assert(T.record(incoming) and not net.TransactionCurrent(0))
        checkRegistered();assert(T.encode(T.record(home))==before)
        local saved=T.encode(T.props());T.reload();startNetwork();checkRegistered()
        assert(T.encode(T.props())==saved)
        """)

    def test_an_unfinished_transfer_is_still_unknown_after_another_route_packet(self):
        self.lua.execute("""
        mapTransfer(incoming,0,902)
        final(incoming,CityTransferTypes.BY_GIFT,0) -- wrong previous owner
        local saved=T.encode(T.props());checkUnresolved();checkUnresolved()
        T.reload();startNetwork();checkUnresolved();assert(T.encode(T.props())==saved)
        """)

    def test_registered_city_with_unreadable_binding_is_not_a_reliable_negative(self):
        self.lua.execute("""
        mapTransfer(incoming,0,902);final(incoming,CityTransferTypes.BY_GIFT);checkRegistered()
        local token=incoming.s.values.TOKEN;incoming.s.values.TOKEN='WRONG'
        assert(not pcall(shared.EffectiveFacts.Read,0,incoming))
        local row=prove();assert(row.provenance~='CONFIRMED');checkGate(false)
        incoming.s.values.TOKEN=token;checkRegistered()
        """)

    def test_combat_from_major_player_confirms_no_identity(self):
        self.lua.execute("beginConquest();final(incoming,CityTransferTypes.BY_COMBAT);assert(T.record(incoming));checkRegistered()")

    def test_combat_from_city_state_uses_its_configured_level(self):
        self.lua.execute("""
        minorSource('CITY_STATE_FIXTURE','CIVILIZATION_LEVEL_CITY_STATE')
        beginConquest();final(incoming,CityTransferTypes.BY_COMBAT)
        assert(T.record(incoming));checkRegistered()
        """)

    def test_peaceful_free_city_confirms_no_identity(self):
        self.lua.execute("""
        freeSource();mapTransfer(incoming,0,902);final(incoming,CityTransferTypes.BY_CULTURAL_IDENTITY)
        assert(T.record(incoming));checkRegistered()
        """)

    def test_free_city_conquest_waits_for_handover_and_freezes_completed_candidates(self):
        self.lua.execute("""
        freeSource();assert(prove()==nil);checkGate(true)
        local homeBefore,partnerBefore=T.encode(T.record(home)),T.encode(T.record(partner))
        T.district(incoming,'DISTRICT_CAMPUS',301,true)
        T.district(incoming,'DISTRICT_THEATER',302,false)
        local scans=0;local districts=incoming.GetDistricts
        incoming.GetDistricts=function(city)scans=scans+1;return districts(city)end
        beginConquest();assert(not T.record(incoming) and scans==0);checkUnresolved()
        final(incoming,CityTransferTypes.BY_COMBAT)
        local record=assert(T.record(incoming),shared.CityProgressionStore.Describe(0,incoming))
        local proof=record.acquisition
        assert(scans==1 and record.schema==3 and proof.mode=='LEGACY_CLAIM')
        assert(proof.evidence=='CONQUEST+Initialized+Transfer' and proof.oldOwner==3 and proof.reference.cityID==902)
        assert(proof.conquered<proof.added and proof.added<proof.initialized and proof.initialized<proof.transferred)
        assert(proof.legacySet.RESEARCH and not proof.legacySet.CULTURE and not record.claim)
        assert(not net.TransactionCurrent(0));checkRegistered()
        assert(T.encode(T.record(home))==homeBefore and T.encode(T.record(partner))==partnerBefore)
        local saved,writes=T.encode(T.props()),T.writes()
        T.complete(incoming,'DISTRICT_THEATER');final(incoming,CityTransferTypes.BY_COMBAT)
        T.reload();startNetwork();checkRegistered()
        assert(scans==1 and T.writes()==writes and T.encode(T.props())==saved)
        assert(shared.CityProgressionStore.ClaimState(0,incoming).eligible)
        """)

    def test_free_city_without_candidates_waits_for_the_first_later_completion(self):
        self.lua.execute("""
        freeSource();T.district(incoming,'DISTRICT_CAMPUS',301,false)
        beginConquest();final(incoming,CityTransferTypes.BY_COMBAT)
        local proof=assert(T.record(incoming),shared.CityProgressionStore.Describe(0,incoming)).acquisition
        assert(proof.mode=='FIRST_COMPLETION' and next(proof.legacySet)==nil)
        assert(shared.CityProgressionStore.ClaimState(0,incoming)==nil)
        T.reload();startNetwork();checkRegistered()
        T.complete(incoming,'DISTRICT_INDUSTRIAL_ZONE');T.complete(incoming,'DISTRICT_CAMPUS')
        local facts=T.control(incoming)
        assert(facts.specialization=='INDUSTRY' and facts.potential==1)
        """)

    def test_free_city_combat_reason_without_conquest_witness_cannot_register(self):
        self.lua.execute("""
        freeSource();local saved=T.encode(T.props())
        mapTransfer(incoming,0,902);final(incoming,CityTransferTypes.BY_COMBAT)
        assert(not T.record(incoming) and T.encode(T.props())==saved);checkUnresolved()
        """)

    def test_conquest_keeps_source_and_previous_owner_guards(self):
        cases = (
            ("minorSource('CIVILIZATION_BARBARIAN','CIVILIZATION_LEVEL_TRIBE')", 3, 'ACQUISITION_SOURCE_INELIGIBLE'),
            ("minorSource('UNKNOWN',nil)", 3, 'ACQUISITION_SOURCE_LEVEL_UNAVAILABLE'),
            ("freeSource();PlayerConfigurations=nil", 3, 'ACQUISITION_SOURCE_CIV_UNAVAILABLE'),
            ("freeSource();Players[3].IsHuman=function()return true end", 3, 'ACQUISITION_SOURCE_INELIGIBLE'),
            ("freeSource()", 4, 'ACQUISITION_CONFLICT'),
        )
        for setup, previous_owner, reason in cases:
            with self.subTest(reason=reason, source=setup):
                lua = registration()
                lua.execute(setup)
                lua.globals().previousOwner = previous_owner
                lua.globals().reason = reason
                lua.execute("""
                local saved=T.encode(T.props())
                beginConquest();final(incoming,CityTransferTypes.BY_COMBAT,previousOwner)
                assert(not T.record(incoming) and T.encode(T.props())==saved)
                assert(shared.CityProgressionStore.Describe(0,incoming):find(reason,1,true));checkUnresolved()
                """)


if __name__ == '__main__':
    unittest.main()
