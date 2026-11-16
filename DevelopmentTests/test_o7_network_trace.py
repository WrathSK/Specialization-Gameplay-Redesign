"""Network proof, Culture effects and error reports with optional TRAIN observers."""

from collections import deque
import unittest

from refactor_harness import Context, PackageVFS, ROOT, measure
from retired_crew_sources import B450, package as historical_package
from test_culture_network import BASE as CULTURE_BASE, ADAPT
from test_pu11_package_absence import mirror_bridge, pair


LOGGER = 'ExpeditionTrainingDiagnostics'
MODES = {
    'enabled': '',
    'disabled': 'SPCExpeditionTrainingDiagnostics.ENABLED=false',
    'construction_error': "SPCExpeditionTrainingDiagnostics.New=function()error('TRACE_FACTORY')end",
    'bad_record': 'SPCExpeditionTrainingDiagnostics.New=function()return {Record=false}end',
    'record_error': """SPCExpeditionTrainingDiagnostics.New=function()
        return {Record=function()recordAttempts=recordAttempts+1;error('TRACE_WRITE')end}
    end""",
    'formatter_error': "SPCExpeditionTrainingDiagnostics.Failure=function()error('TRACE_FORMAT')end",
    'throw': '',
    'silent_nil': '',
}
ABSENT = ('throw', 'silent_nil')


def profile(mode, root=ROOT):
    return PackageVFS(
        manifest=root/'Mod/SpecializationP0.modinfo',
        absent=[LOGGER] if mode in ABSENT else [],
        missing_include=mode if mode in ABSENT else 'throw',
        forbidden_globals=['SPCExpeditionTrainingDiagnostics'] if mode in ABSENT else [],
    )


def network(mode, checkout=None):
    context = Context(name='NetworkTrace', vfs=profile(mode, checkout or ROOT),
                      history=(checkout,B450) if checkout else None)
    context.loads = deque(maxlen=256)
    context.execute(CULTURE_BASE)
    context.execute(ADAPT)
    context.execute("""
        os=nil;io=nil;debug=nil;package=nil;require=nil;rawget=nil;loadfile=nil;dofile=nil
        recordAttempts=0;verifications=0;shared.EventTiming={Verified=function()verifications=verifications+1 end}
        P.RouteUnitRelevant=function(_,id)return id==10 end
    """)

    def include(name):
        result = context.load(name, included=True)
        if name == LOGGER and MODES[mode]:
            context.execute(MODES[mode])
        return result

    context.globals().include = include
    return context


def outcomes(ctx):
    ctx.load('NetworkBridge')
    ctx.execute('SPCNetworkBridge.Start(P,shared);net=shared.NetworkBridge;net.ready=true;cities[4].active=4')
    for name in ('FactChanges','NativeFacts','FactConsumerBindings','CultureNetwork'):
        ctx.load(name)
    ctx.execute("""
        SPCFactChanges.New(shared);SPCNativeFacts.New(P,shared);SPCFactConsumerBindings.New(shared)
        SPCCultureNetwork.Start(P,shared);cn=shared.CultureNetwork
        function settle()
         shared.FactChanges.Flush();shared.FactBindings.Flush();fire('GameCoreEventPublishComplete')
        end
        function proof()send('0,4,0,2,10;0,2,0,1,11;0,2,0,5,12',3);settle()end
        complete(4,1)
        Players[63]={GetCities=function()error('path-private/CultureNetwork.lua:237: attempt to index a nil value secret',0)end}
        proof();fire('LoadScreenClose');settle()
        assert(not cn.ready and not cn.busy and amount(cities[1])==0)
        local failure=cn.failure
        assert(failure and failure.phase=='INITIAL_CITY_COLLECTION' and failure.owner==63)
        assert(failure.errorCode=='LUA_NIL' and failure.errorClass=='LUA_NIL'
            and failure.errorFile=='CultureNetwork.lua' and failure.errorLine==237)
        pending=net.Report(0,cities[1],false)
        assert(pending:find('已发布商路 3') and pending:find('LUA_NIL') and not pending:find('secret'))
        Players[63].GetCities=function()return nil end
        fire('PlayerTurnActivated',0);settle();proof()
        assert(cn.ready and not cn.failure and amount(cities[1])==1 and net.TransactionCurrent(0))
        local begin=created+removed
        local accepted=net.players[0].acceptedSeq
        Events.UnitOperationStarted.Fire(0,10);net.CheckEvidence(false);settle()
        assert(not net.TransactionCurrent(0))
        assert(net.CurrentOutgoingDomestic(0,cities[1]).validity=='UNKNOWN')
        assert(not pcall(net.CurrentCapitalSources,0,cities[1],'CULTURE'))
        complete(4,2);cn.SourceChanged(0,4)
        assert(amount(cities[1])==1 and created+removed==begin)
        proof()
        assert(net.TransactionCurrent(0) and net.players[0].acceptedSeq>accepted and amount(cities[1])==2)
        healthy=net.Report(0,cities[1],false)
        assert(healthy:find('完整文明 2') and healthy:find('已发布商路 3'))
        local describe=cn.Describe
        cn.Describe=function()error('path-private/CultureNetwork.lua:350: CN_REPORT_PENDING secret',0)end
        reportFailure=net.Report(0,cities[1],false)
        assert(reportFailure:find('已发布商路 3') and reportFailure:find('CultureNetwork.lua:350')
            and reportFailure:find('CN_REPORT_PENDING') and not reportFailure:find('secret'))
        cn.Describe=describe
        rejected=net.Report(0,nil,false)
        assert(rejected:find('NETWORK_SELECTED_OWNER_CHANGED'))
        finalCreates,finalRemoves,finalSeq=created,removed,net.players[0].acceptedSeq
        assert(propertyWrites==0 and verifications>0)
        rows={}
        local trace=ExposedMembers.SPC_B205TrainingTrace
        for _,row in ipairs(trace and trace.entries or {})do rows[row.stage]=true end
    """)
    keys = ('pending','healthy','reportFailure','rejected','finalCreates','finalRemoves','finalSeq','verifications')
    return tuple(ctx.eval(key) for key in keys)


class NetworkTrace(unittest.TestCase):
    def test_old_loader_is_a_required_observer_dependency(self):
        with historical_package(B450) as checkout:
            for name in ('NetworkBridge','CultureNetwork'):
                with self.subTest(name=name):
                    ctx = network('throw',checkout)
                    with self.assertRaisesRegex(FileNotFoundError,'PACKAGE_ABSENT:ExpeditionTrainingDiagnostics.lua'):
                        ctx.load(name)

    def test_observers_cannot_change_actual_proof_effects_or_failure_reports(self):
        with historical_package(B450) as checkout:
            expected = outcomes(network('enabled',checkout))
        for mode in MODES:
            with self.subTest(mode=mode):
                ctx = network(mode)
                # Lua's local stack location in the nil-city check moves with source.
                actual = outcomes(ctx)
                self.assertEqual(actual[:3]+actual[4:], expected[:3]+expected[4:])
                self.assertEqual(actual[3].split('；')[0],expected[3].split('；')[0])
                if mode in ('enabled','formatter_error'):
                    for stage in ('NETWORK_PUBLIC','NETWORK_VERIFIED','NETWORK_HEALTH','NETWORK_REPORT_ERROR','NETWORK_WAIT'):
                        self.assertTrue(ctx.eval('rows')[stage],stage)
                else:
                    self.assertIsNone(ctx.eval('next(rows)'))
                if mode in ABSENT:
                    touched = {r['parent'] for r in ctx.loads if r['module']==LOGGER+'.lua'
                               and r['status']=='ABSENT'}
                    self.assertEqual(touched, {'Mod/CultureNetwork.lua','Mod/NetworkBridge.lua'})
                if mode=='record_error':
                    self.assertGreater(ctx.eval('recordAttempts'), 0)
        measure('network_trace_owner_isolation',{
            'observer_profiles': len(MODES), 'retained_while_proof_pending': True,
            'changed_effect_after_ack': True,'private_message_redacted': True,'property_writes': 0,
        })

    def test_actual_gameplay_and_ui_proof_ack_without_observer_file(self):
        for mode in ABSENT:
            with self.subTest(mode=mode):
                g,u,packets = pair(profile=profile(mode))
                g.execute("""
                    local s=ExposedMembers.SPC_P0
                    assert(s.StartStatus.NetworkBridge.state=='OK' and s.StartStatus.CultureNetwork.state=='OK')
                    assert(not s.NetworkBridge.TransactionCurrent(0))
                """)
                self.assertTrue(u.eval('ExposedMembers.SPC_NetworkRequestInFlight'))
                g.execute('GameEvents.SPC_P0_Request.Fire(0,...);publish()',g.table(packets[0]))
                self.assertTrue(g.eval('ExposedMembers.SPC_P0.NetworkBridge.TransactionCurrent(0)'))
                mirror_bridge(g,u)
                u.execute('for i=1,100 do publish()end')
                self.assertFalse(u.eval('ExposedMembers.SPC_NetworkRequestInFlight'))
                self.assertEqual(len(packets),1)
                for context in (g,u):
                    self.assertIsNone(context.globals().SPCExpeditionTrainingDiagnostics)
