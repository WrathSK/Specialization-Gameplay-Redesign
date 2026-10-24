"""Typed committed history, actual Store/producers, Lua51. No native completion claim."""
import unittest
from refactor_harness import Context,ROOT,legacy_source_observation
from test_refactor_s5a2 import actual_store


def industry():
    import test_industry_history as m
    original=m.fixture;m.fixture=actual_store
    try:
        with legacy_source_observation():return m.runtime()
    finally:m.fixture=original


def study():
    import test_b235_engineering as m
    original=m.runtime;m.runtime=industry
    try:
        with legacy_source_observation():return m.study_runtime()
    finally:m.runtime=original


def dialogue():
    import test_dialogue_projects as m
    original=m.fixture;m.fixture=actual_store
    try:
        with legacy_source_observation():return m.game()
    finally:m.fixture=original


def watch(l,topic):
    l.execute("shared.FactChanges.Flush();history={};shared.FactChanges.RegisterConsumer('watch',function(e)history[#history+1]=e end,{kinds={'HISTORY'},topics={...}})",topic)


class Histories(unittest.TestCase):
    def test_templates_actual_initial_and_new_building_then_noop(self):
        l=industry();watch(l,'TEMPLATES');l.execute("""
        c=H.newIndustry();assert(#history==0);shared.FactChanges.Flush()
        assert(#history==1 and T.snapshot(c).templates.learned.BUILDING_A)
        c.buildings[11]=true;GameEvents.BuildingConstructed.Fire(0,c:GetID(),11);shared.FactChanges.Flush()
        assert(#history==2 and T.snapshot(c).templates.learned.BUILDING_B)
        local writes=T.writes();GameEvents.BuildingConstructed.Fire(0,c:GetID(),11);shared.FactChanges.Flush();assert(#history==2 and T.writes()==writes)
        """)
    def test_equal_template_reconcile_is_availability_notification(self):
        l=industry();l.execute("c=H.newIndustry();T.record(c).templateLifecycle.reconcilePending=true;T.reload()")
        watch(l,'TEMPLATES');l.execute("local old=shared.CityProgressionStore.ReadTemplates(c);shared.CityProgressionStore.WriteTemplates(c,old,M.Copy(old));shared.FactChanges.Flush();assert(#history==1 and not T.snapshot(c).templateLifecycle.reconcilePending);shared.CityProgressionStore.WriteTemplates(c,old,M.Copy(old));shared.FactChanges.Flush();assert(#history==1)")
    def test_failed_template_readback_never_notifies_success(self):
        l=industry();l.execute('c=H.newIndustry()');watch(l,'TEMPLATES');l.execute("local old=shared.CityProgressionStore.ReadTemplates(c);local value=M.Copy(old);value.learned.BUILDING_B=true;T.failKey(T.key(c));assert(not pcall(shared.CityProgressionStore.WriteTemplates,c,old,value));shared.FactChanges.Flush();assert(#history==0)")
    def test_engineering_completion_only_with_unique_native_finish(self):
        l=study();l.execute('c=S.make()');watch(l,'ENGINEERING');l.execute("S.begin(c);shared.FactChanges.Flush();assert(#history==0);S.endturn();shared.FactChanges.Flush();assert(#history==1 and S.L(c)==1 and S.finishes(c)==1);Events.CityProjectCompleted.Fire(0,c:GetID(),9001);shared.FactChanges.Flush();assert(#history==1 and S.finishes(c)==1)")
    def test_engineering_result_write_failure_cannot_publish_or_replay(self):
        l=study();l.execute('c=S.make()');watch(l,'ENGINEERING');l.execute("""
        S.begin(c);Events.PlayerTurnDeactivated.Fire(0);local setter=Game.SetProperty
        Game.SetProperty=function(o,k,v)if k==T.key(c) and v.engineering and v.engineering.L==1 then error('FAILED_RESULT')end;return setter(o,k,v)end
        T.turn(1);shared.FactChanges.Flush();assert(#history==0 and S.finishes(c)==1)
        for i=1,20 do Events.GameCoreEventPublishComplete.Fire();shared.FactChanges.Flush()end;assert(#history==0 and S.finishes(c)==1)
        """)
    def test_dialogue_zero_x_is_completed_history_pending_is_not(self):
        l=dialogue();watch(l,'DIALOGUE');l.execute("sampleX=0;duplicate=true;begin(c);shared.FactChanges.Flush();assert(#history==0);endturn();shared.FactChanges.Flush();assert(#history==1 and ledger(c).total==0 and ledger(c).used.ERA_CLASSICAL and samples==1 and finishes==1);Events.CityProjectCompleted.Fire(0,c:GetID(),999);shared.FactChanges.Flush();assert(#history==1 and samples==1 and finishes==1)")
    def test_dialogue_unknown_completion_not_notified_or_resampled(self):
        l=dialogue();watch(l,'DIALOGUE');l.execute("brokenSample=true;begin(c);endturn();shared.FactChanges.Flush();assert(#history==0 and not ledger(c).used.ERA_CLASSICAL and samples==1);for i=1,20 do Events.GameCoreEventPublishComplete.Fire();shared.FactChanges.Flush()end;assert(#history==0 and samples==1)")
    def test_insight_first_success_duplicate_and_second_category(self):
        l=dialogue();watch(l,'INSIGHTS');l.execute("local st=shared.CityProgressionStore;assert(st.AddExpeditionInsight(0,c,'CIVILIZATION_X','PEOPLE',5));shared.FactChanges.Flush();assert(#history==1);assert(not st.AddExpeditionInsight(0,c,'CIVILIZATION_X','PEOPLE',6));shared.FactChanges.Flush();assert(#history==1);assert(st.AddExpeditionInsight(0,c,'CIVILIZATION_X','WORKS',6));shared.FactChanges.Flush();assert(#history==2 and T.snapshot(c).expeditionInsights.records['CIVILIZATION_X:WORKS'])")
    def test_insight_failed_save_no_success_topic(self):
        l=dialogue();watch(l,'INSIGHTS');l.execute("T.failKey(T.key(c));assert(not pcall(shared.CityProgressionStore.AddExpeditionInsight,0,c,'CIVILIZATION_X','PEOPLE',5));shared.FactChanges.Flush();assert(#history==0)")
    def test_wonder_credit_is_player_scope_first_receipt_only(self):
        l=industry();watch(l,'WONDER_CREDIT');l.execute("c=H.city(1);H.wonder(c,1);shared.FactChanges.Flush();assert(#history==1 and history[1].player==0 and H.read(c).E==1);H.wonder(c,1);shared.FactChanges.Flush();assert(#history==1);H.wonder(c,3);shared.FactChanges.Flush();assert(#history==2 and H.read(c).E==2)")
    def test_wonder_failed_commit_does_not_notify(self):
        l=industry();watch(l,'WONDER_CREDIT');l.execute("c=H.city(1);H.failure='throw';H.wonder(c,1);shared.FactChanges.Flush();assert(#history==0)")


class Bindings(unittest.TestCase):
    def test_declared_consumers_isolate_failure_scope_and_idle_budget(self):
        c=Context();c.load('FactChanges');c.load('FactConsumerBindings');c.execute("""
        d=SPCFactChanges.New(shared);calls={};shared.CultureInsightsTourism={Audit=function(e)assert(e.player==0 and e.city==1);error('BROKEN_TOURISM')end}
        shared.CultureNetwork={SourceChanged=function(pid,id)assert(pid==0 and id==1);calls[#calls+1]='network'end}
        shared.DialogueEffects={Audit=function()error('UNRELATED')end};SPCFactConsumerBindings.New(shared)
        d.Emit({owner=0,cityID=1,kinds={'HISTORY'},topic='INSIGHTS',cause='INSIGHTS_COMMITTED'});d.Flush()
        assert(#calls==1 and d.errors.HistoryInsightsTourism and not d.errors.HistoryCultureNetwork)
        local n=d.delivered;for i=1,1000 do d.Flush()end;assert(d.delivered==n)
        """)
    def test_failed_optional_target_does_not_disable_other_bindings(self):
        c=Context();c.load('FactChanges');c.load('FactConsumerBindings');c.execute("""
        d=SPCFactChanges.New(shared);calls=0;shared.StartStatus={DialogueEffects={state='FAILED'}}
        shared.DialogueEffects={Audit=function()error('FAILED_TARGET_LIVE')end}
        shared.StandardizationEffects={SourceChanged=function(pid,id)assert(pid==0 and id==2);calls=calls+1 end}
        SPCFactConsumerBindings.New(shared);d.Emit({owner=0,cityID=2,kinds={'HISTORY'},topic='TEMPLATES',cause='TEMPLATES_COMMITTED'});d.Emit({owner=0,cityID=1,kinds={'HISTORY'},topic='DIALOGUE',cause='DIALOGUE_COMMITTED'});d.Flush();assert(calls==1 and not d.errors.HistoryDialogue)
        """)
    def test_late_binding_factory_failure_quarantines_registered_observers(self):
        c=Context();c.load('FactChanges');c.load('FactConsumerBindings');c.load('RuntimeComposition');c.execute("""
        d=SPCFactChanges.New(shared);composition=SPCRuntimeComposition.New(shared);calls=0
        shared.DialogueEffects={Audit=function()calls=calls+1 end}
        assert(not composition.Run('Bindings',{}, {'FactBindings'},function()SPCFactConsumerBindings.New(shared);error('LATE_BINDING_FAILURE')end))
        d.Emit({owner=0,cityID=1,kinds={'HISTORY'},topic='DIALOGUE',cause='DIALOGUE_COMMITTED'});d.Flush();assert(calls==0 and shared.FactBindings==nil)
        """)

if __name__=='__main__':unittest.main()
