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
function freeSource()
 Players[3].IsMajor=function()return false end
 PlayerConfigurations={[3]={GetCivilizationTypeName=function()return 'CIVILIZATION_FREE_CITIES' end}}
 local info=P.Info
 P.Info=function(t,k)
  if t=='Civilizations' and k=='CIVILIZATION_FREE_CITIES' then
   return {StartingCivilizationLevelType='CIVILIZATION_LEVEL_FREE_CITIES'}
  end
  return info(t,k)
 end
end
function conquest()
 local old=incoming:GetID()
 incoming.s.ref.owner,incoming.s.ref.cityID=0,902
 local x,y=incoming:GetX(),incoming:GetY()
 GameEvents.CityBuilt.Fire(0,902,x,y)
 GameEvents.CityConquered.Fire(0,3,902,x,y)
 Events.CityRemovedFromMap.Fire(3,old);Events.CityAddedToMap.Fire(0,902,x,y)
 Events.CityInitialized.Fire(0,902,x,y);final(incoming,CityTransferTypes.BY_COMBAT)
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


class Registration(unittest.TestCase):
    def setUp(self):
        with patch.object(store_fixture, 'LuaRuntime', LuaRuntime):
            self.lua = store_fixture.fixture()
        self.lua.execute(SETUP)
        self.lua.execute(NETWORK)

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
        self.lua.execute("conquest();assert(T.record(incoming));checkRegistered()")

    def test_peaceful_free_city_confirms_no_identity(self):
        self.lua.execute("""
        freeSource();mapTransfer(incoming,0,902);final(incoming,CityTransferTypes.BY_CULTURAL_IDENTITY)
        assert(T.record(incoming));checkRegistered()
        """)

    def test_free_city_combat_obeys_actual_store_admission_across_reload(self):
        # Test the network rule across either Store outcome, so a future admission fix
        # can legitimately change this case. S1128 records the observed B530 branch.
        self.lua.execute("""
        freeSource();conquest();local admitted=shared.CityProgressionStore.Owns(incoming)
        if admitted then checkRegistered() else
         assert(shared.CityProgressionStore.Describe(0,incoming):find('ACQUISITION_SOURCE_INELIGIBLE',1,true))
         checkUnresolved()
        end
        local saved=T.encode(T.props());T.reload();startNetwork()
        assert(shared.CityProgressionStore.Owns(incoming)==admitted and T.encode(T.props())==saved)
        if admitted then checkRegistered() else checkUnresolved() end
        """)


if __name__ == '__main__':
    unittest.main()
