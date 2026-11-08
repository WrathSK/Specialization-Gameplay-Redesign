"""The old event log disappears while actual route proofs still authorize transactions."""
import unittest

from refactor_harness import Context, PackageVFS, ROOT, measure
from retired_crew_sources import B465, package
from test_deployment_removals import deploy
from test_o7_route_observer_retirement import exercise_proof
from test_p0_panel_current_layout import panel_runtime
from test_pu11_package_absence import scalars

CONTROL='RouteEventsButton'


def roots(root):
    retired=root==ROOT
    vfs=PackageVFS(manifest=root/'Mod/SpecializationP0.modinfo')
    history=None if retired else (root,B465)
    gp,ui=(Context(name=name,vfs=vfs,history=history) for name in ('Gameplay','UI/BackgroundRoutes'))
    packets=exercise_proof(gp,ui)
    assert len(packets)==3
    gp.execute("""
      local projected=...
      local s=ExposedMembers.SPC_P0
      local activity=Events.TradeRouteActivityChanged
      assert(net.TransactionCurrent(0))
      for i=1,40 do activity.Fire(0,0,1,0,2,i)end
      assert(not net.TransactionCurrent(0))
      activity.Fire(1,3,1,4,2,999)
      local raw=s.TradeEvents
      rawCount=raw and #raw or 0
      if projected then assert(raw==nil)
      else
        assert(rawCount==32 and raw[1].text:find('extra=9',1,true) and raw[32].text:find('extra=40',1,true))
      end
      local function request(action,token)
        GameEvents.SPC_P0_Request.Fire(0,{Action=action,Token=token,CityID=city1:GetID()})
        assert(s.RequestIngress.action==action and s.RequestDepth==0)
      end
      request('NETWORK_READ','retained')
      assert(s.LastToken=='retained' and type(s.Snapshot)=='string' and s.FailureAt==nil)
      currentReport=s.Snapshot
      request('TRADE_EVENTS','old-raw')
      if projected then assert(s.LastToken=='retained' and s.Snapshot==currentReport)
      else
        assert(s.LastToken=='old-raw' and s.Snapshot:find('GAMEPLAY EVENT OBSERVATION',1,true))
        assert(s.Snapshot:find('extra=40',1,true) and s.Snapshot:find('extra=39',1,true)
          and s.Snapshot:find('extra=38',1,true) and not s.Snapshot:find('extra=37',1,true))
      end
      assert(s.FailureAt==nil and not net.TransactionCurrent(0))
      after={revision=s.RouteSignalRevision,acceptedSeq=net.players[0].acceptedSeq,
             revalidation=net.players[0].revalidation,transaction=net.TransactionCurrent(0)}
    """,retired)
    assert all(c.load_counts['missing']+c.load_counts['failed']==0 for c in (gp,ui))
    report=gp.eval('currentReport').removeprefix(gp.eval('SPCP0.VERSION')+' | ')
    return (packets,scalars(gp.eval('after')),report,gp.eval('rawCount'),
            gp.eval('Events.TradeRouteActivityChanged.Count()'),
            ui.eval('Events.TradeRouteActivityChanged.Count()'),gp.load_counts,ui.load_counts)


def panel(root):
    doc,ui=panel_runtime(root/'Mod/UI')
    controls=ui.globals().Controls
    buttons={n.get('ID'):controls[n.get('ID')].hidden for n in doc.iter('GridButton') if n.get('ID')}
    ui.execute("""
      Controls.NetworkButton.callbacks[Mouse.eLClick]()
      Controls.NetworkButton.callbacks[Mouse.eRClick]()
      Controls.CityJournalButton.callbacks[Mouse.eLClick]()
      Controls.OpenButton.callbacks[Mouse.eRClick]()
      if ... then Controls.RouteEventsButton.callbacks[Mouse.eLClick]()end
    """,root!=ROOT)
    return buttons,[dict(p.items()) for p in ui.globals().requests.values()]


class RawTradeActivityRetirement(unittest.TestCase):
    def test_real_route_proofs_and_gate_match_without_raw_listener(self):
        with package(B465) as previous:
            old,new=(roots(root) for root in (previous,ROOT))
        self.assertEqual(old[:3],new[:3])
        self.assertEqual(old[5:],new[5:])
        self.assertEqual((old[3],new[3]),(32,0))
        self.assertEqual(old[4]-new[4],1)
        measure('raw_trade_activity_retirement',dict(modeled_activity_events=40,
            modeled_raw_rows_after_burst=[32,0],modeled_gameplay_activity_listeners_removed=1,
            matching_production_packets=3,production_signal_and_strict_gate_match=True))

    def test_only_the_hidden_raw_activity_report_retires(self):
        with package(B465) as previous:
            old_buttons,old_requests=panel(previous)
            before=deploy.snapshot(previous.resolve()/'Mod')
        new_buttons,new_requests=panel(ROOT)
        self.assertTrue(old_buttons.pop(CONTROL))
        self.assertEqual(old_buttons,new_buttons)
        self.assertEqual(old_requests[:-1],new_requests)
        self.assertEqual(old_requests[-1]['Action'],'TRADE_EVENTS')
        self.assertEqual([p['Action'] for p in new_requests],
            ['NETWORK_READ','NETWORK_DETAIL','CITY_JOURNAL_READ','EVENT_ORDER_TOGGLE'])
        after=deploy.snapshot(ROOT/'Mod')
        self.assertEqual(before['files'].keys(),after['files'].keys())
        for name in ('NetworkBridge.lua','UI/BackgroundRoutes.lua','NetworkSender.lua','EventTimingDiagnostics.lua'):
            self.assertEqual(before['files'][name],after['files'][name])
