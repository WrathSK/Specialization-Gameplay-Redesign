"""S3 actual composition/callback/readiness/adapters; explicit Lua51 native doubles."""
import re,subprocess,unittest
from refactor_harness import Context,ROOT
from refactor_defect_fixtures import startup,panel,request_context

class Composition(unittest.TestCase):
    def make(self):
        c=Context();c.load('RuntimeComposition');c.execute("d=SPCRuntimeComposition.New(shared);writes=0;originalEvents=Events;originalGameEvents=GameEvents;originalLuaEvents=LuaEvents;print=function()end")
        return c
    def test_late_failed_listeners_exit_return_and_consumer_quarantined(self):
        c=self.make();c.execute("""
        callbacks={};shared.CityProgressionStore={RegisterExit=function(n,f)callbacks.exit=f end,RegisterReturn=function(n,f)callbacks.ret=f end}
        shared.GreatWorkFacts={RegisterConsumer=function(n,f)callbacks.work=f end}
        previous=function()end;shared.OnPermanentCityWrite=previous
        originalRegister=shared.CityProgressionStore.RegisterExit
        assert(not d.Run('Broken',{}, {'Broken'},function()
          shared.Broken={Update=function()writes=writes+1 end}
          Events.LoadScreenClose.Add(shared.Broken.Update)
          shared.CityProgressionStore.RegisterExit('Broken',shared.Broken.Update)
          shared.CityProgressionStore.RegisterReturn('Broken',shared.Broken.Update)
          shared.GreatWorkFacts.RegisterConsumer('Broken',shared.Broken.Update)
          shared.OnPermanentCityWrite=shared.Broken.Update
          error('INJECTED_LATE_FAILURE')
        end))
        assert(Events==originalEvents and GameEvents==originalGameEvents and LuaEvents==originalLuaEvents)
        assert(shared.Broken==nil and shared.OnPermanentCityWrite==previous)
        assert(shared.CityProgressionStore.RegisterExit==originalRegister)
        Events.LoadScreenClose.Fire()
        assert(not pcall(callbacks.exit) and not pcall(callbacks.ret) and not pcall(callbacks.work))
        assert(writes==0 and shared.StartStatus.Broken.state=='FAILED')
        assert(not d.Run('Dependent',{'Broken'},{},function()error('MUST_NOT_RUN')end))
        assert(shared.StartStatus.Dependent.state=='SKIPPED_DEPENDENCY')
        assert(d.Run('Independent',{}, {},function()end));assert(d.Complete()==2 and d.sealed)
        """)
    def test_add_then_throw_missing_or_throwing_remove_still_quarantines(self):
        for remover in ('nil',"function()error('REMOVE_UNAVAILABLE')end"):
            c=self.make();c.execute("event=Events.Test;local add=event.Add;event.Remove="+remover+";event.Add=function(f)add(f);error('ADD_POST_REGISTRATION')end;assert(not d.Run('Broken',{}, {},function()Events.Test.Add(function()writes=writes+1 end)end));event.Fire();assert(writes==0 and Events==originalEvents)")
    def test_callable_events_identity_remove_and_starting_reentry_preserved(self):
        c=self.make();c.execute("""
        original=Events.Test;added={};local add=original.Add
        original.Add=function(f)added[#added+1]=f;add(f)end
        assert(d.Run('Good',{}, {},function()
          saved=Events.Test;fn=function()writes=writes+1 end
          saved.Add(fn);saved.Add(fn);assert(added[1]==added[2]);saved('REENTRANT')
        end))
        assert(writes==2 and original.Add~=nil)
        saved.Remove(fn);original.Fire();assert(writes==2)
        """)
    def test_missing_event_stays_missing(self):
        c=self.make();c.execute("Events.Absent=false;assert(d.Run('Good',{}, {},function()assert(not Events.Absent)end));assert(Events.Absent==false)")
    def test_start_order_matches_original_production_sequence(self):
        before=subprocess.check_output(['git','show','28aae8b:Mod/Gameplay.lua'],cwd=ROOT,text=True)
        after=(ROOT/'Mod/Gameplay.lua').read_text()
        # Diagnostic Startup helper calls are separate; all historical real Starts retain order.
        pattern=r'(SPC\w+)\.Start\(P,shared'
        self.assertEqual(re.findall(pattern,before),re.findall(pattern,after))
    def test_failed_store_skips_legacy_mode_selectors(self):
        c=startup();c.execute("SPCCityProgressionStore.Start=function()error('STORE_FAILED')end")
        c.load('Gameplay')
        for name in ('BindingProbe','CompletionRecordProbe','CityJournalProbe','CityFlowProbe','EffectiveFacts','ClaimProjects'):
            self.assertEqual(c.eval("ExposedMembers.SPC_P0.StartStatus['%s'].state"%name),'SKIPPED_DEPENDENCY')
        self.assertTrue(c.eval('sealed'));self.assertIn('INITIALIZED_PARTIAL',c.eval('ExposedMembers.SPC_P0.Stage'))
    def test_retired_dialogue_never_restored_by_failed_new_effect(self):
        c=startup();c.execute("SPCDialogueEffects.Start=function(P,s)s.DialogueEffects={};error('EFFECT_FAILED')end");c.load('Gameplay')
        self.assertTrue(c.eval('ExposedMembers.SPC_P0.Dialogue.retired'));self.assertIsNone(c.eval('ExposedMembers.SPC_P0.DialogueEffects'))
        self.assertEqual(c.eval('ExposedMembers.SPC_P0.StartStatus.DialogueEffects.state'),'FAILED')

class Observers(unittest.TestCase):
    def test_each_chain_link_and_predecessor_protected_in_order(self):
        c=Context();c.load('SafeCallbacks');c.execute("""
        seen={};shared.OnPermanentCityWrite=function()seen[#seen+1]='old';error('OLD_ERROR')end
        SPCSafeCallbacks.Chain(shared,'first',function()seen[#seen+1]='first';error('SELF_ERROR')end)
        SPCSafeCallbacks.Chain(shared,'second',function()seen[#seen+1]='second'end)
        assert(pcall(shared.OnPermanentCityWrite,{},'COMMITTED'))
        assert(table.concat(seen,',')=='old,first,second')
        assert(shared.ObserverErrors['first:prior'] and shared.ObserverErrors['first:self'])
        """)
    def test_unit_and_ui_fact_fanouts_preserve_siblings_scope_and_ack(self):
        c=request_context();c.execute("P.Observe=function()end;shared.UnitActions={Run=function()return 'COMMITTED',{}end};shared.ResearchInfrastructure={Audit=function()error('OBSERVER')end};shared.ResearchChair={Audit=function(s)assert(s.player==0);sibling=(sibling or 0)+1 end};runRequest(0,{Action='UNIT_ACTION_CONFIRM',Token='UNIT',CityID=1});assert(shared.LastToken=='UNIT' and sibling==1);runRequest(0,{Action='LV2_GPP_DIRTY',Token='GPP',FactsChanged=true});assert(sibling==2)")

class Readiness(unittest.TestCase):
    def test_latch_waits_for_store_then_initializes_exactly_once_without_frames(self):
        for boundary in ('publish()','Events.PlayerTurnActivated.Fire(0)','Events.LoadScreenClose.Fire()'):
            c=Context();c.load('RuntimeWork');c.execute("P={Field=function(t,k)return t[k]end};state='WAITING';shared.CityProgressionStore={HistoryStartStatus=function()return state end};starts=0;SPCRuntimeWork.StartReady(P,shared,'Fixture',function()starts=starts+1 end);for i=1,10 do publish();Events.PlayerTurnActivated.Fire(0);Events.LoadScreenClose.Fire()end;assert(starts==0 and frames==0);state='READY';"+boundary+";for i=1,10 do publish();Events.PlayerTurnActivated.Fire(0);Events.LoadScreenClose.Fire()end;assert(starts==1 and frames==0)")
    def test_actual_nine_load_only_modules_use_latch_and_self_register(self):
        modules=['ResearchSupport','Lv2Housing','Lv2GPP','ResearchInfrastructure','ResearchCross','ResearchApply','ResearchChair','ResearchTraditionEffects','NetworkBridge']
        c=Context();c.execute("""
        print=function()end;Players={};P={Field=function(t,k)return t and t[k]end,Count=function()end,Observe=function()end,IsTestPlayer=function()return false end,Rows=function()return {}end,Info=function()return {}end};SPCP0=P
        state='WAITING';registered={};shared.ReadinessSummary={Register=function(n)registered[n]=true end}
        shared.CityProgressionStore={HistoryStartStatus=function()return state end,RegisterExit=function()end,RegisterReturn=function()end,VisitTradition=function()end}
        shared.EffectiveFacts={};SPCResearchTradition={}
        """)
        for name in modules:c.load(name);c.execute('SPC'+name+'.Start(P,shared)')
        c.execute('publish()')
        for name in modules:self.assertFalse(c.eval('shared.'+name+'.ready'));self.assertTrue(c.eval('registered.'+name))
        c.execute("state='READY';publish()")
        for name in modules:self.assertTrue(c.eval('shared.'+name+'.ready'))
        c.execute('for i=1,5 do publish()end');self.assertEqual(c.eval('frames'),0)

class Adapters(unittest.TestCase):
    def test_actual_panel_constructor_and_before_failures_preserve_native_selection(self):
        c=panel("SPCCapitalInvestmentUI.New=function()error('NEW_FAILED')end")
        c.execute("AdvanceProject({}, {Type='PROJECT_NATIVE'});assert(nativeAdvances==1);AdvanceProject({}, {Type='PROJECT_SPC_CAPITAL_INVESTMENT'});assert(nativeAdvances==1);assert(GetDataHelper().ProjectItems[1].Name=='native')")
        c=panel("SPCCapitalInvestmentUI.New=function()return {Before=function()error('BEFORE_FAILED')end}end")
        c.execute("AdvanceProject({}, {Type='PROJECT_NATIVE'});assert(nativeAdvances==1);AdvanceProject({}, {Type='PROJECT_SPC_CAPITAL_INVESTMENT'});assert(nativeAdvances==1)")
    def test_mutating_failure_restores_both_native_lists_and_blocks_exact_item(self):
        c=Context('UI');c.load('UI/SafeAdapters');c.execute("""
        d=SPCSafeAdapters.New();entry=d.Add('test',function(item)return item.Type=='PROJECT_SPC_TEST'end,{},function()return {Items=function(data)
         data.ProjectItems[1].Name='bad';data.UnitItems[1].Name='bad';data.ProjectItems[2]={Type='PROJECT_PARTIAL'};error('MUTATION')
        end,Before=function()error('BEFORE')end}end)
        data={ProjectItems={{Type='PROJECT_NATIVE',Name='good'},{Type='PROJECT_SPC_TEST'}},UnitItems={{Type='UNIT_NATIVE',Name='unit'}}}
        d.Items(entry,data);assert(data.ProjectItems[1].Name=='good' and data.ProjectItems[2].Type=='PROJECT_SPC_TEST' and data.ProjectItems[2].Disabled)
        assert(data.UnitItems[1].Name=='unit' and d.Before(entry,{}, {Type='PROJECT_NATIVE'}) and not d.Before(entry,{}, {Type='PROJECT_SPC_TEST'}))
        """)
    def test_events_isolate_each_adapter_and_shutdown_is_identity_safe(self):
        c=panel("""
        baseShutdown=0;OnShutdown=function()baseShutdown=baseShutdown+1 end
        SPCClaimProjectUI.New=function()ExposedMembers.SPC_ClaimQueueRead=function()end;ExposedMembers.SPC_ClaimSelection={};return {Before=function()return true end,Pulse=function()error('PULSE')end}end
        SPCDialogueProjectUI.New=function()return {Before=function()return true end,Pulse=function()pulseSibling=(pulseSibling or 0)+1 end}end
        """)
        c.execute("""
        Events.GameCoreEventPublishComplete.Fire();assert(pulseSibling==1)
        newer=function()end;ExposedMembers.SPC_ClaimQueueRead=newer
        shutdown();assert(ExposedMembers.SPC_ClaimQueueRead==newer and ExposedMembers.SPC_ClaimSelection==nil and baseShutdown==1)
        assert(Events.GameCoreEventPublishComplete.Count()==0);Events.GameCoreEventPublishComplete.Fire();assert(pulseSibling==1)
        """)

class ReviewBoundaries(unittest.TestCase):
    def test_readiness_observer_failure_cannot_fail_business_registration(self):
        c=Context();c.load('RuntimeWork');c.execute("P={Field=function(t,k)return t[k]end};shared.ReadinessSummary={Register=function()error('DIAGNOSTIC_ONLY')end};shared.CityProgressionStore={HistoryStartStatus=function()return 'READY'end};n=0;assert(pcall(SPCRuntimeWork.StartReady,P,shared,'Fixture',function()n=n+1 end));publish();assert(n==1)")
    def test_required_missing_nil_before_never_admits_spc(self):
        for api in ('nil','{}','5',"{Before=function()return nil end}"):
            c=panel('SPCCapitalInvestmentUI.New=function()return '+api+' end')
            c.execute("AdvanceProject({}, {Type='PROJECT_SPC_CAPITAL_INVESTMENT'});assert(nativeAdvances==0)")
            if api!="{Before=function()return nil end}":c.execute("AdvanceProject({}, {Type='PROJECT_NATIVE'});assert(nativeAdvances==1)")
    def test_crew_model_failure_is_not_native_admission(self):
        c=panel("SPCCrewModel=nil;SPCCrewProjectUI.New=function()error('MODEL_MISSING')end")
        c.execute("AdvanceProject({}, {Type='PROJECT_NATIVE'});assert(nativeAdvances==1);AdvanceProject({}, {Type='PROJECT_SPC_CREW_250'});assert(nativeAdvances==1)")
    def test_dynamic_selection_publication_close_preserves_newer_context(self):
        for newer in (False,True):
            c=Context('UI');c.load('UI/TimedProjectSelection');c.execute("P={IsTestPlayer=function()return true end};api=SPCTimedProjectSelection.New(P,function()end,function()end);city={GetOwner=function()return 0 end,GetID=function()return 1 end};assert(api.Before(city,{Type='PROJECT_SPC_OVERFLOW_SINK_TEST'}));assert(ExposedMembers.SPC_TimedProjectSelection.status=='PENDING')")
            if newer:c.execute('newer={};ExposedMembers.SPC_TimedProjectSelection=newer')
            c.execute('api.Close()');self.assertTrue(c.eval('ExposedMembers.SPC_TimedProjectSelection==newer'if newer else'ExposedMembers.SPC_TimedProjectSelection==nil'))
    def test_failed_constructor_restores_partial_export_and_newer_close_safe(self):
        c=Context('UI');c.load('UI/SafeAdapters');c.execute("d=SPCSafeAdapters.New();old={};ExposedMembers.Reader=old;e=d.Add('Broken',function()return false end,{'Reader'},function()ExposedMembers.Reader={};error('CONSTRUCTOR')end);assert(ExposedMembers.Reader==old);d.Close();assert(ExposedMembers.Reader==old)")
    def test_add_then_throw_only_disables_affected_adapter(self):
        c=Context('UI');c.load('UI/SafeAdapters');c.execute("""
        d=SPCSafeAdapters.New();n=0;e=d.Add('Broken',function(i)return i.Type=='SPC'end,{},function()return {Publish=function()n=n+1 end,Before=function()return true end}end)
        local ev=Events.Fault;local add=ev.Add;ev.Add=function(f)add(f);error('LATE_ADD')end
        d.Hook(Events,'Fault',e,'Publish');ev.Fire();assert(n==0 and e.unavailable and not d.Before(e,{}, {Type='SPC'}) and d.Before(e,{}, {Type='NATIVE'}));d.Close()
        """)
    def test_explicit_external_partial_export_rollback(self):
        c=Context();c.load('RuntimeComposition');c.execute("print=function()end;d=SPCRuntimeComposition.New(shared);old={};ExposedMembers.SPC_RestructuringViews=old;assert(not d.Run('REST',{}, {'Restructuring'},function()ExposedMembers.SPC_RestructuringViews={};error('AFTER_PUBLISH')end,{{ExposedMembers,'SPC_RestructuringViews'}}));assert(ExposedMembers.SPC_RestructuringViews==old)")
    def test_normal_epilogue_and_independent_module_failure_scopes(self):
        c=startup();c.execute("SPCResearchTraditionEffects=module('HealthyResearchTraditionEffects','ResearchTraditionEffects')");c.load('Gameplay')
        self.assertEqual(c.eval('ExposedMembers.SPC_P0.Stage'),'INITIALIZED ISOLATED_PROBES USER_GAME_TEST_REQUIRED')
        self.assertTrue(c.eval('sealed'))
        c=startup();c.execute("SPCDistrictCompleteness.Start=function()error('DISTRICT_OWNER_FAILED')end");c.load('Gameplay')
        for name in ('ResearchSupport','Lv2GPP','ResearchCross','Lv4Percent'):
            self.assertEqual(c.eval("ExposedMembers.SPC_P0.StartStatus['%s'].state"%name),'OK')
        self.assertEqual(c.eval('ExposedMembers.SPC_P0.StartStatus.Lv2Housing.state'),'SKIPPED_DEPENDENCY')
    def test_readiness_cannot_hide_skipped_writers_or_exceed_fixed_fields(self):
        c=Context();c.execute("P={Field=function(t,k)return t[k]end};rows={};SPCExpeditionTrainingDiagnostics={ENABLED=true,New=function()return {Record=function(stage,v)rows[#rows+1]={stage=stage,value=v}end}end};shared.CityProgressionStore={FreshReady=function()return true end};shared.StartStatus={Missing={state='SKIPPED_DEPENDENCY',code='D'},Failed={state='FAILED',code='START_ERROR'}}")
        c.load('ReadinessSummary');c.execute("summary=SPCReadinessSummary.Start(P,shared)")
        for name in ['ResearchSupport','Lv2Housing','Lv2GPP','ResearchInfrastructure','ResearchCross','ResearchApply','ResearchChair','ResearchTraditionEffects','NetworkBridge']:
            c.execute("shared[...]= {ready=true};summary.Register(...)",name)
        c.execute("summary.Seal();publish();local seen=false;for _,r in ipairs(rows)do if r.stage=='READINESS_SUMMARY'then assert(r.value.notReady=='STARTUP_2' and #r.value.writerState<=256);seen=true end end;assert(seen)")
