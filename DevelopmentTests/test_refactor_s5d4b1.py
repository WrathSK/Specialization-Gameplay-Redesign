"""S5d4b1 actual native role producer and existing effect consumers. Lua51/local only."""
import unittest
from refactor_harness import Context,ROOT,legacy_source_observation,measure
from refactor_defect_fixtures import startup,fact_publication_profile
from test_refactor_s5d1 import research
from test_refactor_s4a import industry,load_industry_ui


def native():
    c=Context();c.load('FactChanges');c.load('NativeFacts')
    c.execute("P={Field=function(t,k)return t and t[k]end,Count=function(k)counts[k]=(counts[k]or 0)+1 end,IsTestPlayer=function(pid)return pid==0 end};Players={[0]={GetCities=function()error('MARK_CITY_READ_FORBIDDEN')end},[1]={GetCities=function()error('FOREIGN_CITY_READ_FORBIDDEN')end}};d=SPCFactChanges.New(shared);n=SPCNativeFacts.New(P,shared);seen={};d.RegisterConsumer('test',function(e)seen[#seen+1]=e end,{kinds={'ACTIVE'}})")
    return c


class NativeRole(unittest.TestCase):
    def test_one_hook_marks_only_coalesces_real_notifications_and_no_idle(self):
        c=native();c.execute("assert(Events.GovernorChanged.Count()==1);for i=1,44 do Events.GovernorChanged.Fire(0)end;assert(#seen==0 and d.pending==1 and d.Generation(0,'NETWORK')==88);d.Flush();assert(#seen==1 and seen[1].player==0);for i=1,1000 do publish();d.Flush()end;assert(#seen==1 and not counts.city_scan)")
        measure('S5d4b1_role_mark',{'native_notifications':44,'native_owner_listeners':1,'scoped_deliveries':1,'city_visits_at_mark':0,'thousand_idle_extra_deliveries':0})
    def test_known_foreign_has_no_local_dirty_generation(self):
        c=native();c.execute("Events.GovernorChanged.Fire(1);Events.GovernorAssigned.Fire(1,777,1);d.Flush();assert(#seen==0 and d.sequence==0)")
    def test_cross_owner_and_established_scope(self):
        c=native();c.execute("Events.GovernorAssigned.Fire(1,777,0);d.Flush();assert(#seen==1 and seen[1].player==0 and seen[1].city==nil);Events.GovernorEstablished.Fire(0,2,0);d.Flush();assert(#seen==2 and seen[2].city==2 and seen[2].causes.NATIVE_GOVERNOR_ESTABLISHED)")
    def test_unknown_scope_expands_enabled_participants_without_guess_or_nil_owner(self):
        c=native();c.execute("P.IsTestPlayer=function(pid)return pid==1 end;Events.GovernorChanged.Fire(-1);d.Flush();assert(#seen==1 and seen[1].player==1 and seen[1].city==nil);Events.GovernorAssigned.Fire();d.Flush();assert(#seen==2 and seen[2].player==1)")
    def test_same_turn_second_change_is_a_new_delivery(self):
        c=native();c.execute("Events.GovernorChanged.Fire(0);d.Flush();local gen=d.Generation(0,'NETWORK');Events.GovernorPromoted.Fire(0);d.Flush();assert(#seen==2 and d.Generation(0,'NETWORK')>gen and turn==1)")
    def test_first_owner_mark_failure_does_not_block_second(self):
        c=native();c.execute("P.IsTestPlayer=function(pid)return pid==0 or pid==1 end;local emit=d.Emit;d.Emit=function(e)if e.owner==1 then error('FIRST_OWNER_FAILURE')end;return emit(e)end;Events.GovernorAssigned.Fire(1,9,0);d.Flush();assert(#seen==1 and seen[1].player==0 and n.errors.GovernorAssigned)")
    def test_unknown_participant_failure_isolated_and_proof_invalid_before_fallible_emit(self):
        c=native();c.execute("P.IsTestPlayer=function(pid)return true end;local emit=d.Emit;d.Emit=function(e)if e.owner==1 then error('ONE_PARTICIPANT_FAILED')end;return emit(e)end;Events.GovernorChanged.Fire();d.Flush();assert(#seen==1 and seen[1].player==0 and d.Generation(1,'NETWORK')>0 and n.errors.GovernorChanged)")
    def test_real_composition_failure_quarantines_dependents_not_store(self):
        c=startup();include=c.globals().include
        def injected(name):
            out=include(name)
            if name=='NativeFacts':c.execute("local new=SPCNativeFacts.New;SPCNativeFacts.New=function(...)new(...);error('NATIVE_OWNER_START_FAILED')end")
            return out
        c.globals().include=injected;c.load('Gameplay')
        c.execute("local s=ExposedMembers.SPC_P0;assert(s.StartStatus.NativeFacts.state=='FAILED' and s.NativeFacts==nil and s.StartStatus.CityProgressionStore.state=='OK');for _,name in ipairs({'ResearchTraditionEffects','ResearchSupport','IndustrySupport','NetworkBridge','ResearchChair','DialogueEffects','Commerce','CultureNetwork'})do assert(s.StartStatus[name].state=='SKIPPED_DEPENDENCY',name)end;assert(Events.GovernorChanged.Count()==0)")


class ActualConsumers(unittest.TestCase):
    def test_real_apply_chair_same_turn_with_no_ui_or_old_governor_hooks(self):
        l=research()
        with legacy_source_observation():fact_publication_profile(l,False)
        l.execute("""
        function rolepublish()shared.FactChanges.Flush();shared.FactBindings.Flush();fire('GameCoreEventPublishComplete')end
        auditCounts={};P.Observe=function(kind,name)if kind=='audit'then auditCounts[name]=(auditCounts[name]or 0)+1 end end;cities[2].GetBuildings=function()error('UNRELATED_CITY_READ_FORBIDDEN')end;
        counters={};cities[1].active=3;fire('GovernorEstablished',0,1,0);assert(cc('BUILDING_LIBRARY')==3);rolepublish();assert(cc('BUILDING_LIBRARY')==0 and cc('BUILDING_LIBRARY',cities[2])==3 and counters.city_scan==3 and auditCounts.ResearchApply==1 and auditCounts.ResearchChair==1 and auditCounts.ResearchInfrastructure==1)
        cities[1].active=4;fire('GovernorEstablished',0,1,0);rolepublish();assert(cc('BUILDING_LIBRARY')==3 and cc('BUILDING_LIBRARY',cities[2])==3 and counters.city_scan==6 and auditCounts.ResearchApply==2 and auditCounts.ResearchChair==2 and auditCounts.ResearchInfrastructure==2)
        local cap,readsBefore,writesBefore=counters.dc_capture,reads,writes;for i=1,1000 do rolepublish()end;assert(counters.dc_capture==cap and reads==readsBefore and writes==writesBefore)
        """)
    def test_real_industry_owner_governor_withdrawal_and_recovery_no_new_sample(self):
        l=industry();load_industry_ui(l)
        l.execute("""
        assert(d.ReadBase(0,cities[2])==6 and cities[2].built['BUILDING_SPC_DEV_INDUSTRY_LV1_-1']);local sendsBefore=sends
        facts[2].active=0;fire('GovernorChanged');pulse();assert(not cities[2].built['BUILDING_SPC_DEV_INDUSTRY_LV1_-1'])
        facts[2].active=1;fire('GovernorChanged');pulse();assert(cities[2].built['BUILDING_SPC_DEV_INDUSTRY_LV1_-1'] and not cities[1].built['BUILDING_SPC_DEV_INDUSTRY_LV1_-1'] and sends==sendsBefore)
        """)
    def test_real_industry_unknown_holds_waits_new_governor_cause(self):
        l=industry();load_industry_ui(l)
        l.execute("""
        factUnknown=true;fire('GovernorChanged');pulse();assert(cities[2].built['BUILDING_SPC_DEV_INDUSTRY_LV1_-1'] and d.errors['0:2']);local n=writes
        factUnknown=false;facts[2].active=0;for i=1,1000 do pulse()end;assert(writes==n and cities[2].built['BUILDING_SPC_DEV_INDUSTRY_LV1_-1'])
        fire('GovernorChanged');pulse();assert(not cities[2].built['BUILDING_SPC_DEV_INDUSTRY_LV1_-1'] and not d.errors['0:2'])
        """)
    def test_real_bridge_one_capture_and_immediate_transaction_invalidation(self):
        from test_refactor_s5c2 import fixture
        l=fixture();l.execute("""
        function rolepublish()shared.FactChanges.Flush();shared.FactBindings.Flush();Events.GameCoreEventPublishComplete.Fire()end
        local rev=net.ProofRevision(0);for i=1,44 do Events.GovernorChanged.Fire(0)end
        assert(captures==0 and not net.TransactionCurrent(0));rolepublish();assert(captures==1 and net.ProofRevision(0)>rev)
        Events.GovernorChanged.Fire(0);rolepublish();assert(captures==2 and turn==1)
        for i=1,1000 do rolepublish()end;assert(captures==2)
        """)
    def test_real_transaction_proof_revoked_even_when_native_notification_queue_fails(self):
        from test_refactor_s5c2 import fixture
        l=fixture();l.execute("assert(net.TransactionCurrent(0));local emit=shared.FactChanges.Emit;shared.FactChanges.Emit=function()error('NOTIFICATION_QUEUE_FAILURE')end;Events.GovernorChanged.Fire(0);assert(not net.TransactionCurrent(0) and shared.NativeFacts.errors.GovernorChanged and captures==0);shared.FactChanges.Emit=emit;Events.GovernorChanged.Fire(0);shared.FactChanges.Flush();shared.FactBindings.Flush();assert(captures==1)")
    def test_real_bridge_foreign_zero_cross_owner_local_recovers(self):
        from test_refactor_s5c2 import fixture
        l=fixture();l.execute("""
        Events.GovernorChanged.Fire(1);shared.FactChanges.Flush();shared.FactBindings.Flush();assert(captures==0)
        Events.GovernorAssigned.Fire(1,777,0);assert(not net.TransactionCurrent(0));shared.FactChanges.Flush();shared.FactBindings.Flush();assert(captures==1)
        """)
    def test_production_old_governor_edges_gone_with_explicit_dependencies(self):
        names=['ResearchSupport','Lv2Housing','Lv2GPP','IndustrySupport','Lv3Effects','ResearchInfrastructure','ResearchApply','ResearchChair','ResearchCross','CultureAesthetic','CultureMeaning','CultureInspiration','CultureInsightsTourism','ResearchTraditionEffects','StandardizationEffects','CultureNetwork','Commerce','NetworkBridge','DialogueEffects']
        source=(ROOT/'Mod/Gameplay.lua').read_text()
        import re
        for name in names:
            module=(ROOT/'Mod'/f'{name}.lua').read_text()
            self.assertNotRegex(module,r"['\"]Governor(?:Assigned|Established|Changed|Promoted)['\"]",name)
            line=next(row for row in source.splitlines()if row.startswith("composition.Run('"+name+"'"))
            self.assertIn("'NativeFacts'",line)
        self.assertLess(source.index("composition.Run('NativeFacts'"),source.index("composition.Run('ResearchTraditionEffects'"))


if __name__=='__main__':unittest.main()
