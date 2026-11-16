"""Named S2 counterexamples in actual production callers; no game/native PASS."""
import unittest
from refactor_harness import measure
from refactor_defect_fixtures import commerce,gc,request_context,startup,greatworks,panel,store_completion

class Defects(unittest.TestCase):
    def test_investment_commit_ack_and_sibling_survive_observer_failure(self):
        c=request_context();c.execute("committed=0;sibling=0;shared.InvestmentAction={Confirm=function()committed=committed+1;return 'COMMITTED',{}end};shared.ResearchInfrastructure={Audit=function()error('FIXTURE_OBSERVER')end};shared.ResearchChair={Audit=function()sibling=sibling+1 end};pcall(runRequest,0,{Action='INVEST_CONFIRM',CityID=1,Token='T',PlanToken='P'})")
        self.assertEqual(c.eval('committed'),1);self.assertEqual(c.eval('shared.LastToken'),'T','S3_COMMIT_ACK_LOST');self.assertEqual(c.eval('sibling'),1)
    def test_late_start_failure_does_not_abort_siblings_or_seal(self):
        c=startup()
        error=None
        try:c.load('Gameplay')
        except Exception as exc:error=str(exc)
        self.assertIn('ResearchTraditionEffects',c.eval("table.concat(starts,',')"),'fixture must reach the injected late-start failure')
        if error:self.assertIn('FIXTURE_LATE_START_FAILURE',error,'unrelated fixture failure is not the counterexample')
        self.assertTrue(c.eval('sealed'),'S3_START_CHAIN_ABORTED')
        c.execute('Events.LoadScreenClose.Fire()');self.assertEqual(c.eval('lateWrites'),0,'S3_FAILED_START_LISTENER_LIVE')
    def test_adapter_failure_preserves_native_rows_and_siblings(self):
        c=panel();result=c.execute('local ok,data=pcall(GetDataHelper);return ok,ok and data.ProjectItems[1].Name or "ERROR",siblings')
        self.assertTrue(result[0],'S3_ADAPTER_ABORTED_NATIVE_LIST');self.assertEqual(result[1],'native');self.assertEqual(result[2],1)
    def test_greatwork_nil_active_does_not_invalidate_other_city_facts(self):
        c=greatworks();self.assertEqual(c.eval('packet.FactsCities'),2,'S4_GW_NIL_ACTIVE_ABORT');self.assertEqual(c.eval('packet.Valid'),1)
    def test_UI_pending_gc_recovers_in_eligible_window(self):
        l=gc();l.execute('ExposedMembers.SPC_IndustryBackground={pending=1};Events.PlayerTurnActivated.Fire(0);Events.GameCoreEventPublishComplete.Fire();ExposedMembers.SPC_IndustryBackground.pending=0;Events.GameCoreEventPublishComplete.Fire()')
        self.assertEqual(l.eval('collections'),1,'S4_UI_PENDING_GC_STUCK')
    def test_commerce_carrier_present_across_network_pending(self):
        l=commerce();l.execute("assert(toggle(2,'DISTRICT_CAMPUS',true));before=ownedGold(cities[2]);net.CheckEvidence(true)")
        measure('T08_commerce_pending_before',{'before':l.eval('before'),'after':l.eval('ownedGold(cities[2])')})
        self.assertGreater(l.eval('before'),0);self.assertEqual(l.eval('ownedGold(cities[2])'),l.eval('before'),'S4_COMMERCE_PENDING_WITHDRAWAL')

    def test_post_commit_observer_does_not_fail_completed_identity(self):
        c=store_completion();ok=c.execute("return pcall(d.Complete,0,{}, {reference=root.origin,specialization='RESEARCH',districtID=1,type='DISTRICT_CAMPUS',turn=1})")
        self.assertEqual(c.eval('writes'),1);self.assertEqual(c.eval('root.progression'),'SPECIALIZED')
        self.assertTrue(ok[0] if isinstance(ok,tuple)else ok,'S3_POST_COMMIT_OBSERVER_FAILURE')
    def test_equal_value_proof_recovery_notifies_consumers(self):
        import test_culture_network
        from refactor_harness import TrackedLua51,legacy_source_observation
        test_culture_network.LuaRuntime=TrackedLua51
        with legacy_source_observation():l=test_culture_network.fixture()
        from refactor_defect_fixtures import fact_publication_profile
        fact_publication_profile(l)
        l.execute("recovered=0;shared.Commerce={Mark=function()recovered=recovered+1;assert(net.CurrentDomesticPartners(0,cities[2]).validity=='VERIFIED')end};shared.RouteSignalRevision=shared.RouteSignalRevision+1;net.players[0].revalidation='NEEDS_REVALIDATION';send('0,4,0,2,10;0,2,0,1,11;0,2,0,5,12',3)")
        self.assertEqual(l.eval('recovered'),1,'S4_RECOVERY_NOT_NOTIFIED')
