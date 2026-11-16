"""Real route sender and city presentation with an absent or faulty observer."""

from collections import deque
import unittest
from unittest.mock import patch

from refactor_harness import Context, ROOT, measure
from retired_crew_sources import gameplay as historical_context, package as historical_package
from test_b265_city_presentation import presentation
import test_culture_institutions
from test_o7_network_trace import ABSENT, LOGGER, MODES, profile
from test_pu11_package_absence import NATIVE, mirror_bridge, scalars


B451 = '414edd5521415cde89be47a0b20f146ff31c4bc5'


def observer_include(context, mode, skip=()):
    def include(name):
        if name in skip:
            return None
        path = 'UI/LevelBannerModel' if name=='LevelBannerModel' else name
        result = context.load(path,included=True)
        if name == LOGGER and MODES[mode]:
            context.execute(MODES[mode])
        return result
    context.globals().include = include


def route(mode, before=None):
    if before:
        g = historical_context(before,revision=B451)
        u = historical_context(before,revision=B451,name='UI/BackgroundRoutes',
            absent=[LOGGER] if mode in ABSENT else [],missing_include=mode if mode in ABSENT else 'throw')
    else:
        g = Context()
        u = Context(name='UI/BackgroundRoutes',vfs=profile(mode))
    for context in (g,u):
        context.execute(NATIVE)
    g.load('Gameplay')
    g.execute('Events.LoadScreenClose.Fire();publish()')
    u.loads = deque(maxlen=256)
    observer_include(u, mode)
    u.execute("""
        activityReads=0
        Players[0].IsTurnActive=function()activityReads=activityReads+1;return true end
    """)
    u.load('UI/BackgroundRoutes')
    mirror_bridge(g,u)
    packets = []

    def request(pid,op,p):
        assert pid==0 and op==1
        packets.append(scalars(p))

    u.globals().UI.RequestPlayerOperation = request
    u.execute('init();pub=ExposedMembers.SPC_P0_BackgroundRoutes')
    assert len(packets)==1 and u.eval('pub.awaitingNetwork')
    assert not g.eval('ExposedMembers.SPC_P0.NetworkBridge.TransactionCurrent(0)')
    first = u.eval('pub.senderResult')
    g.execute('GameEvents.SPC_P0_Request.Fire(0,...);publish()', g.table(packets[0]))
    assert g.eval('ExposedMembers.SPC_P0.NetworkBridge.TransactionCurrent(0)')
    mirror_bridge(g,u)
    u.execute('for i=1,100 do publish()end')
    assert not u.eval('pub.awaitingNetwork') and not u.eval('ExposedMembers.SPC_NetworkRequestInFlight')
    u.execute('shutdown()')
    assert len(packets)==1 and not u.eval('ExposedMembers.SPC_NetworkRequestInFlight')
    if mode in ABSENT:
        assert any(r['module']==LOGGER+'.lua' and r['status']=='ABSENT' for r in u.loads)
    wire = packets[0].copy()
    wire['Token'] = wire['Token'].split(':',1)[1]
    return wire, u.eval('activityReads'), first, u.eval('pub.senderResult')


def city_view(mode):
    ctx = Context(name='UI/CityPotential',vfs=profile(mode))

    def load(lua):
        assert lua is ctx.lua
        # Keep the existing city/eligibility and native control doubles. The
        # actual UI code, reply ports, view logic and observer includes run.
        ctx.execute('SPCExpeditionTrainingDiagnostics=nil;recordAttempts=0')
        observer_include(ctx,mode,skip=('Probe',))
        ctx.load('UI/CityPotential')

    with patch.object(test_culture_institutions,'LuaRuntime',lambda:ctx.lua):
        view = presentation(load=load)
    return ctx,view


class UITrace(unittest.TestCase):
    def test_missing_or_disabled_trace_does_not_repeat_native_turn_reads(self):
        with historical_package(B451) as before:
            old_enabled = route('enabled',before)
            old_missing = route('throw',before)
            old_disabled = route('disabled',before)
        self.assertGreater(old_missing[1],1)
        self.assertGreater(old_disabled[1],1)
        self.assertEqual(route('enabled'),old_enabled)
        for mode in ('disabled',*ABSENT):
            with self.subTest(mode=mode):
                self.assertEqual(route(mode),(old_enabled[0],1,None,None))
        measure('route_sender_observation_turn_reads', {
            'old_missing': old_missing[1], 'old_disabled': old_disabled[1], 'current_each': 1,
            'enabled': old_enabled[1], 'wire_equal': True, 'idle_publications_per_mode': 100,
        })

    def test_city_presentation_uses_actual_reply_port_in_every_observer_profile(self):
        for mode in MODES:
            with self.subTest(mode=mode):
                ctx,view = city_view(mode)
                view.execute("""
                    assert(#requests==1 and Controls.ActiveIcon.icon=='ICON_SPC_LEVEL_CULTURE_3')
                    nativeActive=4;Events.GovernorPromoted(0);Events.GameCoreEventPublishComplete()
                    assert(#requests==2 and Controls.ActiveIcon.icon=='ICON_SPC_LEVEL_CULTURE_4')
                    assert(rows.items[4].State.text=='当前')
                    throwing=true;Events.GovernorChanged(0);Events.GameCoreEventPublishComplete()
                    local n=#requests
                    for i=1,100 do Events.GameCoreEventPublishComplete()end
                    assert(n==3 and #requests==n)
                    throwing=false;Events.GovernorChanged(0);Events.GameCoreEventPublishComplete()
                    assert(#requests==4 and rows.items[4].State.text=='当前')
                    stopBridge();assert(actionParent.destroyed==Controls.ActiveShortcut)
                """)
                if mode in ABSENT:
                    self.assertTrue(any(r['parent']=='Mod/UI/CityPotential.lua' and
                        r['module']==LOGGER+'.lua' and r['status']=='ABSENT' for r in ctx.loads))
                if mode=='record_error':
                    self.assertGreater(ctx.eval('recordAttempts'),0)
