"""B177 cumulative Dialogue: actual Lua/SQL and existing two-city/Store fixtures.
No simulated test claims native percentage math, serialization or performance.
"""
from pathlib import Path
import unittest, xml.etree.ElementTree as ET
from lupa.lua55 import LuaRuntime
import test_culture_meaning_automatic as auto
import test_culture_meaning_probe as legacy
import test_dialogue_projects as projects
R=Path(__file__).resolve().parents[1]

class Effects(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sql=legacy.database()
        cls.sql.executescript((R/'Mod/Data/DialogueEffects.sql').read_text())
    @classmethod
    def tearDownClass(cls):cls.sql.close()
    def runtime(self,boot=True,real=False):
        helper=auto.AutomaticMeaningTests();helper.sql=self.sql;l=helper.runtime(real=real)
        l.globals().include('DialogueProjectModel');l.globals().include('DialogueEffects')
        l.execute(r"""
          local read=shared.EffectiveFacts.Read
          shared.EffectiveFacts.Read=function(pid,c)local f=read(pid,c);f.owner=pid;f.cityID=c.id;f.investmentPending=c.pending;return f end
          function history(c,values)
            local h=SPCDialogueProjectModel.New();local names={'ERA_ANCIENT','ERA_CLASSICAL','ERA_MEDIEVAL','ERA_RENAISSANCE','ERA_INDUSTRIAL','ERA_MODERN','ERA_ATOMIC','ERA_INFORMATION','ERA_FUTURE'}
            for i,x in ipairs(values)do h.serial=i;h.used[names[i]]={id=i,start=1,completed=2,x=x,gain=x*5,forced=false};h.total=h.total+x*5 end
            c.history=h
          end
          history(a,{1});history(b,{2})
          shared.CityProgressionStore.DialogueState=function(pid,c)
            assert(not c.historyError,'STORE_HISTORY_UNAVAILABLE')
            return {value=SPCDialogueProjectModel.Copy(c.history),token=c.token,
              reference={owner=pid,cityID=c.id,x=c.x,y=0}}
          end
          function total(c)
            local sum,n=0,0
            for row in GameInfo.SPC_DialogueTotals()do if c.present[GameInfo.Buildings['BUILDING_SPC_DIALOGUE_TOTAL_'..row.Bonus].Index]then sum=sum+row.Bonus;n=n+1 end end
            assert(n<=1,'duplicate final carriers');return sum
          end
          function boot()
            SPCDialogueEffects.Start(P,shared);effects=shared.DialogueEffects;effects.Audit()
          end
          function one()effects.Audit({player=0,city=1})end
        """)
        # Same GameInfo adapter as existing tests, with SQL-derived legal totals.
        import test_culture_aesthetic as ae
        l.globals().GameInfo['SPC_DialogueTotals']=l.globals().db(ae.lua_table(l,[{'Bonus':r[0]}for r in self.sql.execute('SELECT Bonus FROM SPC_DialogueTotals')]),'Bonus')
        if boot:l.execute('boot()')
        return l
    def test_earned_history_replaces_collection_formula_and_no_panel(self):
        l=self.runtime();l.execute("assert(total(a)==5 and total(b)==10);assert(dialogue.retired);a.eras=7;one();assert(total(a)==5);assert(effects.Describe(0,a):find('旅游业绩限定') and effects.Describe(0,a):find('累计 +5%',1,true))")
    def test_first_zero_history_has_no_effect_not_old_auto(self):
        l=self.runtime();l.execute("a.history=nil;one();assert(total(a)==0);for n=2,9 do assert(not a.present[GameInfo.Buildings['BUILDING_SPC_B059_D'..n].Index])end")
    def test_active_three_and_pause_return_keep_ledger(self):
        l=self.runtime();l.execute("a.active=3;fire('GovernorEstablished',0,1,0);assert(total(a)==5);a.active=1;fire('GovernorAssigned',0,1,0);assert(total(a)==0 and a.history.total==5 and total(b)==10);a.active=3;fire('GovernorAssigned',0,1,0);assert(total(a)==5)")
    def test_identity_exit_retains_history_and_return_recomputes(self):
        l=self.runtime();l.execute("a.identity='REALLOCATING';one();assert(total(a)==0 and a.history.total==5);a.identity='CULTURE';a.active=3;one();assert(total(a)==5)")
    def test_unknown_preserves_only_same_confirmed_projection(self):
        l=self.runtime();l.execute("a.active=nil;one();assert(total(a)==5 and effects.errors['0:1']);a.token='new';one();assert(total(a)==0);a.active=3;one();assert(total(a)==5)")
    def test_missing_or_corrupt_history_withdraws_without_reconstruction(self):
        for failure in ("a.historyError=true", "a.history.total=55", "a.history.used.ERA_ANCIENT=nil"):
            with self.subTest(failure=failure):
                l=self.runtime();l.execute(failure+";one();assert(total(a)==0 and total(b)==10 and effects.errors['0:1'])")
    def test_effective_facts_failure_does_not_hide_unreadable_store(self):
        l=self.runtime();l.execute("shared.EffectiveFacts.Read=function()error('Store dependency failed')end;one();assert(total(a)==5);a.historyError=true;one();assert(total(a)==0 and effects.errors['0:1']:find('HISTORY_UNAVAILABLE'))")
    def test_unknown_governor_cannot_mask_corrupt_history(self):
        l=self.runtime();l.execute("a.active=nil;a.history.total=55;one();assert(total(a)==0 and effects.errors['0:1'])")
    def test_legal_maximum_and_unknown_historical_era_not_clamped(self):
        l=self.runtime();l.execute("history(a,{7,7,7,7,7,7,7,7,7});one();assert(total(a)==315);local x=a.history.used.ERA_ANCIENT;a.history.used.ERA_ANCIENT=nil;a.history.used.ERA_UNKNOWN=x;one();assert(total(a)==0 and a.history.total==315 and effects.errors['0:1']:find('ERA_UNAVAILABLE'))")
    def test_replace_single_final_value_and_duplicates_are_read_bounded(self):
        l=self.runtime();l.execute(r"""
          history(a,{2});one();assert(total(a)==10 and not a.present[GameInfo.Buildings.BUILDING_SPC_DIALOGUE_TOTAL_5.Index])
          local before=writes;local calls=0;local has=P.HasBuilding
          P.HasBuilding=function(b,id)calls=calls+1;return has(b,id)end
          one();one();assert(writes==before and calls<=6)
        """)
    def test_removal_failure_never_adds_over_residual(self):
        l=self.runtime();l.execute("failRemove=GameInfo.Buildings.BUILDING_SPC_DIALOGUE_TOTAL_5.Index;history(a,{2});one();assert(total(a)==5 and effects.errors['0:1']);assert(not a.present[GameInfo.Buildings.BUILDING_SPC_DIALOGUE_TOTAL_10.Index]);failRemove=nil;one();assert(total(a)==10)")
    def test_create_failure_does_not_undo_committed_history(self):
        l=self.runtime();l.execute("history(a,{3});failCreate=true;one();assert(total(a)==0 and a.history.total==15 and effects.errors['0:1']);failCreate=false;one();assert(total(a)==15)")
    def test_confirmed_loss_duplicate_and_current_fact_recapture(self):
        l=self.runtime();l.execute(r"""
          assert(not pcall(exits.DialogueEffects,a,{confirmed=false,targetID=1,origin={owner=0}}));assert(total(a)==5)
          a.owner=3;local loss={confirmed=true,targetID=1,origin={owner=0}};exits.DialogueEffects(a,loss);exits.DialogueEffects(a,loss)
          assert(total(a)==0 and a.history.total==5 and total(b)==10)
          a.owner=0;a.active=1;returns.DialogueEffects(0,a);assert(total(a)==0)
          a.active=3;returns.DialogueEffects(0,a);assert(total(a)==5)
        """)
    def test_cold_reconstruction_ignores_saved_carrier_values(self):
        l=self.runtime(boot=False);l.execute("seed(a,'BUILDING_SPC_DIALOGUE_TOTAL_200');seed(a,'BUILDING_SPC_B059_D2');boot();assert(total(a)==5 and not a.present[GameInfo.Buildings.BUILDING_SPC_B059_D2.Index]);assert(a.history.total==5)")
    def test_legacy_failure_blocks_new_writer_and_never_falls_back(self):
        l=self.runtime(boot=False);l.execute("seed(a,'BUILDING_SPC_B059_D2');failRemove=GameInfo.Buildings.BUILDING_SPC_B059_D2.Index;boot();assert(effects.startupError and total(a)==0 and dialogue.retired)")
    def test_collection_unknown_empty_and_restored(self):
        l=self.runtime();l.execute("a.worksUnknown=true;one();assert(total(a)==5 and effects.errors['0:1']);a.worksUnknown=false;a.workCount=0;one();assert(total(a)==0);a.workCount=2;one();assert(total(a)==5)")
    def test_real_transport_ack_and_meaning_unchanged(self):
        l=self.runtime(real=True);l.execute("sample(1,1,1);assert(total(a)==5);local n=finalAmount(a,'SCIENCE');sample(2,2,1);assert(total(a)==5 and finalAmount(a,'SCIENCE')==n);assert(dialogue.seq[0]==2 and shared.GreatWorkFacts.ack==2);assert(not pcall(dialogue.HoldMeaningProbe,0,a,100))")
    def test_stale_manual_ingress_is_read_only(self):
        l=self.runtime(real=True);l.execute("sample(1,1,1);local before=writes;local reads=0;shared.DialogueProjects={Describe=function()reads=reads+1;return '累计+5%'end};meaningRequest(0,{Action='DIALOGUE_CARRIER_NEXT',CityID=1,Token='old'});assert(reads==1 and writes==before and total(a)==5 and not dialogue.carrierTest)")
    def test_inactive_other_profession_does_not_read_missing_history(self):
        l=self.runtime();l.execute("a.identity='NONE';a.active=0;a.history=nil;local reads=0;shared.CityProgressionStore.DialogueState=function()reads=reads+1;error('not registered')end;one();local before=writes;one();assert(reads==0 and writes==before and total(a)==0 and not effects.errors['0:1'])")
    def test_ordinary_building_event_does_not_rescan_history_and_damage_recovers(self):
        l=self.runtime();l.execute("local read=shared.CityProgressionStore.DialogueState;local n=0;shared.CityProgressionStore.DialogueState=function(...)n=n+1;return read(...)end;fire('CityBuildingsChanged',0,1);assert(n==0);local id=GameInfo.Buildings.BUILDING_SPC_DIALOGUE_TOTAL_5.Index;a.pillaged[id]=true;fire('CityBuildingsChanged',0,1);assert(n==1 and total(a)==5 and not a.pillaged[id])")
    def test_unknown_recipient_metadata_blocks_before_projection(self):
        l=self.runtime(boot=False);l.execute("SPCCultureMeaningModel.RecipientCoverage=function()return {status='BLOCKED_LOADED_SET'}end;boot();assert(total(a)==0 and effects.errors['0:1']:find('CATALOG_UNVERIFIED'))")
    def test_database_covers_each_legal_total_only_tourism_and_seven_categories(self):
        d=self.sql;eras=d.execute('SELECT COUNT(*) FROM Eras').fetchone()[0]
        values=[r[0]for r in d.execute('SELECT Bonus FROM SPC_DialogueTotals ORDER BY Bonus')]
        self.assertEqual(values,list(range(5,35*eras+1,5)))
        for value in values:
            rows=d.execute("SELECT m.ModifierType,a.Value FROM BuildingModifiers b JOIN Modifiers m USING(ModifierId) JOIN ModifierArguments a USING(ModifierId) WHERE b.BuildingType=? AND a.Name='ScalingFactor'",('BUILDING_SPC_DIALOGUE_TOTAL_'+str(value),)).fetchall()
            self.assertEqual(rows,[('MODIFIER_SINGLE_CITY_ADJUST_TOURISM',str(100+value))]*7)
        self.assertEqual(d.execute("SELECT COUNT(*) FROM ModifierArguments WHERE ModifierId LIKE 'SPC_DIALOGUE_TOTAL_%' AND (Name='YieldType' OR Value IN ('GREATWORKOBJECT_RELIC','GREATWORKOBJECT_PRODUCT'))").fetchone()[0],0)
    def test_package_lua_syntax_and_read_only_panel(self):
        tree=ET.parse(R/'Mod/SpecializationP0.modinfo');self.assertEqual(tree.getroot().get('version'),'204')
        l=LuaRuntime();check=l.eval('function(s)local f,e=load(s);assert(f,e)end')
        for name in ['DialogueEffects.lua','Dialogue.lua','DialogueProjects.lua','Gameplay.lua','UI/P0Panel.lua']:check((R/'Mod'/name).read_text())
        from test_p0_panel_current_layout import panel_runtime
        tree,l=panel_runtime();l.execute("Controls.GWCityButton.callbacks[Mouse.eLClick]();Controls.GWCityButton.callbacks[Mouse.eRClick]();assert(requests[#requests].Action=='DIALOGUE_PROJECT_READ' and requests[#requests-1].Action=='DIALOGUE_PROJECT_READ')")
        files=[e.text for e in ET.parse(R/'Mod/SpecializationP0.modinfo').findall('./Files/File')]
        self.assertEqual(len(files),len(set(files)))
        self.assertEqual(set(files),{p.relative_to(R/'Mod').as_posix()for p in (R/'Mod').rglob('*')if p.is_file()and p.name not in ('SpecializationP0.modinfo','.DS_Store')})

class ProjectCommitNotification(unittest.TestCase):
    def test_actual_store_commits_before_target_effect_and_duplicate_does_not_reaward(self):
        l=projects.game();l.execute(r"""
          notifications=0
          shared.DialogueEffects={Audit=function(scope)
            assert(scope.player==0 and scope.city==c:GetID());assert(ledger(c).total==5)
            notifications=notifications+1
          end}
          begin(c);endturn();assert(notifications==1)
          Events.CityProjectCompleted.Fire(0,c:GetID(),999);assert(notifications==1 and ledger(c).total==5)
        """)
    def test_failure_does_not_publish_uncommitted_reward(self):
        l=projects.game();l.execute(r"""
          shared.DialogueEffects={Audit=function()error('uncommitted effect notification')end}
          brokenSample=true;begin(c);endturn();assert(ledger(c).total==0 and ledger(c).pending.stage=='HELD')
        """)

if __name__=='__main__':unittest.main(verbosity=2)
