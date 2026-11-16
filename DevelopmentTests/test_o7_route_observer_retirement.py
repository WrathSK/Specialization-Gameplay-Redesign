"""Exact retired package path and real nonempty UI-to-Gameplay route proof."""

from collections import deque
import unittest
import xml.etree.ElementTree as ET

from refactor_harness import Context, PackageVFS, ROOT, measure
from retired_crew_sources import B449, B450, gameplay as historical_context, package as historical_package
from test_o7_crew_retirement import verify_package_round_trip
from test_p0_panel_current_layout import panel_runtime
from test_pu11_package_absence import NATIVE, mirror_bridge, scalars


RETIRED = 'TradeRouteProbe.lua'
FORBIDDEN = ('SPCTradeRouteProbe',)
OBSERVER_READS = """
playerEnumerations=0;unitEnumerations=0
local player=Players[0]
local units=player.GetUnits
function Game.GetPlayers()playerEnumerations=playerEnumerations+1;return {player}end
function player:GetID()return 0 end
function player:GetUnits()unitEnumerations=unitEnumerations+1;return units(self)end
"""
TWO_CITIES = """
routes={{OriginCityPlayer=0,OriginCityID=1,DestinationCityPlayer=0,DestinationCityID=2,TraderUnitID=10}}
local cities={}
for id=1,2 do
 local c={id=id}
 function c:GetID()return self.id end
 function c:GetOwner()return 0 end
 function c:GetX()return self.id end
 function c:GetY()return 12 end
 function c:GetName()return 'City '..self.id end
 function c:GetProperty()return nil end
 function c:GetTrade()
  return {GetOutgoingRoutes=function()
   local rows={};for _,r in ipairs(routes)do if r.OriginCityID==self.id then rows[#rows+1]=r end end
   return rows
  end}
 end
 cities[id]=c
end
local trader={GetType=function()return 10 end}
local player=Players[0]
function player:GetCities()return {
 Members=function()return ipairs(cities)end,FindID=function(_,id)return cities[id]end,
 GetCapitalCity=function()return cities[2]end,
}end
function player:GetUnits()return {FindID=function(_,id)if id==10 then return trader end end}end
function player:GetTrade()return {GetNumOutgoingRoutes=function()return #routes end,
 CountOutgoingRoutes=function()return #routes end}end
GameInfo.Units={[10]={MakeTradeRoute=true}}
if ExposedMembers.SPC_P0 then
 -- Explicit role input at the fact boundary. Collection, proof, validation,
 -- signaling and transaction views run through the real two package roots.
 local shared=ExposedMembers.SPC_P0
 shared.EffectiveFacts.Read=function(_,c)
  if c==cities[1] then return {specialization='CULTURE',potential=4,active=4} end
  return {specialization='NONE',potential=0,active=0}
 end
 city1=cities[1]
 net=shared.NetworkBridge
 Game.SetProperty=function()error('ROUTE_PROOF_WROTE_PERMANENT_STATE')end
end
"""


def exercise_proof(g, u):
    for c in (g, u):
        c.execute('os=nil;io=nil;debug=nil;package=nil;require=nil;rawget=nil;loadfile=nil;dofile=nil')
        c.execute(NATIVE)
    g.load('Gameplay')
    g.execute('Events.LoadScreenClose.Fire();publish()')
    for c in (g, u):
        c.execute(TWO_CITIES)
    u.load('UI/BackgroundRoutes')
    mirror_bridge(g, u)
    packets = []

    def request(pid, op, payload):
        assert pid == 0 and op == 1
        packets.append(scalars(payload))

    u.globals().UI.RequestPlayerOperation = request
    u.execute('init()')
    g.execute("""
        function deliver(packet)GameEvents.SPC_P0_Request.Fire(0,packet);publish()end
        function verify(open,partner)
         assert(net.TransactionCurrent(0)==open)
         local result=net.CurrentOutgoingDomestic(0,city1)
         assert(result.validity==(open and 'VERIFIED' or 'UNKNOWN'),result.reason)
         if open then
          assert(#net.players[0].routes==1)
          if partner then assert(#result.partners==1 and result.partners[1]==2)
          else assert(#result.partners==0)end
         end
        end
    """)
    for i, data in enumerate(('0,1,0,2,10', '0,1,0,2,10', '0,2,0,1,10'), 1):
        if i == 2:
            g.execute('Events.UnitOperationStarted.Fire(0,10)')
        elif i == 3:
            for c in (g, u):
                c.execute('routes[1].OriginCityID=2;routes[1].DestinationCityID=1')
            g.execute('Events.TradeRouteActivityChanged.Fire(0,1,0,2)')
        if i > 1:
            mirror_bridge(g, u)
            u.execute('publish()')
            # An ACK from the old signal cannot reopen the transaction.
            g.execute('deliver(...)', g.table(packets[i-2]))
        assert len(packets) == i and packets[-1]['Data'] == data
        assert packets[-1]['Count'] == 1 and packets[-1]['Valid'] == 1
        g.execute('verify(false)')
        assert u.eval('ExposedMembers.SPC_NetworkRequestInFlight') is True
        g.execute('deliver(...);verify(true,select(2,...))', g.table(packets[-1]), i != 3)
        mirror_bridge(g, u)
        u.execute('for j=1,100 do publish()end')
        assert len(packets) == i
        assert u.eval('ExposedMembers.SPC_NetworkRequestInFlight') is False
    # Token has the package version prefix. The rest of the wire contract is equal.
    return [{**p, 'Token': p['Token'].split(':', 1)[1]} for p in packets]


class RouteObserverRetirement(unittest.TestCase):
    def test_real_roots_do_not_load_or_sample_the_retired_observer(self):
        with historical_package(B449) as checkout:
            previous = historical_context(checkout, revision=B449)
            profile = PackageVFS(forbidden_globals=FORBIDDEN)
            self.assertNotIn(RETIRED, profile.files | profile.imports)
            current = Context(vfs=profile)
            for old, ctx in ((True, previous), (False, current)):
                ctx.loads = deque(maxlen=512)
                ctx.execute(NATIVE)
                ctx.execute(OBSERVER_READS)
                ctx.load('Gameplay')
                ctx.execute("""
                    Events.LoadScreenClose.Fire();publish()
                    Events.PlayerTurnActivated.Fire(0);publish()
                    Events.PlayerTurnDeactivated.Fire(0);publish()
                    assert(ExposedMembers.SPC_P0.StartStatus.NetworkBridge.state=='OK')
                """)
                self.assertEqual(any(r['module']==RETIRED for r in ctx.loads), old)
                self.assertEqual(ctx.load_counts['missing'], 0)
                self.assertEqual(ctx.eval('playerEnumerations'), 4 if old else 0)
                self.assertEqual(ctx.eval('unitEnumerations'), 4 if old else 0)
            self.assertIsNone(current.eval('ExposedMembers.SPC_P0.AutoRouteProbe'))
            measure('retired_route_player_unit_enumerations', {'old_each': 4, 'current_each': 0})

    def test_actual_nonempty_transport_before_and_after_retirement(self):
        with historical_package(B449) as checkout:
            previous = exercise_proof(
                historical_context(checkout, revision=B449),
                historical_context(checkout, revision=B449, name='UI/BackgroundRoutes'),
            )
        vfs = PackageVFS(forbidden_globals=FORBIDDEN)
        candidate = exercise_proof(Context(vfs=vfs), Context(name='UI/BackgroundRoutes',vfs=vfs))
        self.assertEqual(candidate, previous)
        measure('nonempty_route_retirement_transport', {
            'packets': len(candidate), 'unchanged_route_signal': True, 'changed_route': True,
            'stale_receipt_kept_blocked': True, 'idle_publications': 300,
        })

    def test_only_hidden_route_state_is_removed_and_other_controls_work(self):
        with historical_package(B449) as checkout:
            old_tree, old = panel_runtime(checkout/'Mod/UI')
            old.execute("""
                ExposedMembers.SPC_P0.AutoRouteProbe={[0]={text='OLD_ROUTE_CACHE',sequence=17}}
                Controls.RouteStateButton.callbacks[Mouse.eLClick]()
                assert(Controls.Status.text:find('OLD_ROUTE_CACHE') and #requests==0)
                assert(ExposedMembers.SPC_P0.AutoRouteProbe[0].sequence==17)
            """)
        with historical_package(B450) as retired:
            tree, current = panel_runtime(retired/'Mod/UI')
        def controls(doc):
            return {el.get('ID') for el in doc.iter() if el.get('ID')}
        self.assertEqual(controls(old_tree)-controls(tree), {'RouteStateButton'})
        self.assertFalse(controls(tree)-controls(old_tree))
        current.execute("""
            assert(Controls.RouteStateButton==nil)
            ExposedMembers.SPC_P0_BackgroundRoutes={version=SPCP0.VERSION,text='BACKGROUND_CACHE'}
            Controls.BackgroundRoutesButton.callbacks[Mouse.eLClick]()
            assert(Controls.Status.text:find('BACKGROUND_CACHE') and #requests==0)
            Controls.RouteEventsButton.callbacks[Mouse.eLClick]()
            SPCP0.NetworkProbe=function(city,action)
                assert(city==selectedCity and action=='TRADE');return 'LOCAL_TRADE_REPORT'
            end
            Controls.TradeButton.callbacks[Mouse.eLClick]()
            assert(#requests==1 and requests[1].Action=='TRADE_EVENTS')
            assert(Controls.Status.text:find('LOCAL_TRADE_REPORT'))
        """)

    def test_exact_route_removal_and_complete_old_package_recovery(self):
        with historical_package(B449) as before, historical_package(B450) as after:
            verify_package_round_trip(self, before/'Mod', after/'Mod', (RETIRED,), 'NetworkBridge.lua')
