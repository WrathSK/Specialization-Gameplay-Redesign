"""B166 automatic Meaning / exact legacy retirement. LOCAL simulation only.

Reuse the maintained read-only DB and two-city native-interface fixtures.
Actual writer, legacy module, Shared D, facts packet and request handler execute.
No game launch, deployment, process-memory conclusion or broad stress.
"""
from pathlib import Path
import subprocess, unittest, xml.etree.ElementTree as ET
from lupa.lua55 import LuaRuntime
import test_culture_aesthetic as ae
import test_culture_meaning_probe as legacy
R=Path(__file__).resolve().parents[1]

class AutomaticMeaningTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls): cls.sql=legacy.database()
    @classmethod
    def tearDownClass(cls): cls.sql.close()
    def runtime(self, ready=True, real=False):
        helper=ae.AestheticTests(); helper.sql=self.sql; l=helper.runtime(ready=False)
        for table,key in [('GreatWorks','GreatWorkType'),('Yields','YieldType'),('GreatPersonIndividuals','GreatPersonIndividualType'),('Eras','EraType'),('GreatWork_YieldChanges','GreatWorkType')]:
            cur=self.sql.execute('SELECT * FROM '+table); columns=[x[0]for x in cur.description];rows=[dict(zip(columns,x))for x in cur]
            for i,row in enumerate(rows):row['Index']=i+1
            l.globals().GameInfo[table]=l.globals().db(ae.lua_table(l,rows),key)
        for name in ['Dialogue','GreatWorkAdjacency','CultureMeaning']:l.globals().include(name)
        l.execute(r"""
          P.Scalar=function(v)return tostring(v)end
          for _,c in ipairs(cities)do
            c.identity='CULTURE';c.potential=4;c.active=4;c.workCount=1;c.badCount=0;c.categoryUnknown=0
            function c:GetName()return 'Fixture '..self.id end
            local campus=district(c,6,'DISTRICT_CAMPUS')
            building(c,'BUILDING_LIBRARY',campus);building(c,'BUILDING_UNIVERSITY',campus);building(c,'BUILDING_RESEARCH_LAB',campus)
          end
          shared.GreatWorkFacts.Summary=function(pid,cid)
            local c=Players[pid]:GetCities():FindID(cid)
            return c and {count=c.workCount,eraCount=c.eras,availability=c.worksUnknown and 'UNKNOWN' or 'KNOWN',
              hasConfirmed=not c.neverConfirmed,reference=SPCNetworkInput.Reference(c),modifierExcludedCount=c.badCount,unknownCategoryCount=c.categoryUnknown}
          end
          SPCDialogue.Start(P,shared);dialogue=shared.Dialogue
          SPCGWAdjacency.Start(P,shared,{retired=true});gwa=shared.GreatWorkAdjacency
          SPCCultureMeaning.Start(P,shared);meaning=shared.CultureMeaning
          assert(not shared.CultureMeaningProbe)
          function finalAmount(c,y)
            local out=0;for _,part in ipairs(SPCCultureMeaningModel.FinalValues[y])do if c.present[GameInfo.Buildings[part.name].Index]then out=out+part.amount end end;return out
          end
          function seed(c,name)building(c,name,c.ds[1])end
          function meaningCount(c)local n=0;for _,name in ipairs(SPCCultureMeaningModel.Owned)do if c.present[GameInfo.Buildings[name].Index]then n=n+1 end end;return n end
          function oldCount(c)local n=0;for _,y in ipairs(SPCGWAdjacencyModel.Yields)do for _,sign in ipairs({'P','N'})do for bit=0,12 do
            if c.present[GameInfo.Buildings['BUILDING_SPC_B060_'..y..'_'..sign..bit].Index]then n=n+1 end
          end end end;return n end
          function update(cid)meaning.Audit({player=0,city=cid or 1})end
        """)
        if real:
            l.globals().include('GreatWorkFacts')
            l.execute('local callback=shared.GreatWorkFacts.OnConfirmed;SPCGreatWorkFacts.Start(P,shared);shared.GreatWorkFacts.OnConfirmed=callback')
            legacy.bind_actual_request(l)
            l.execute(r"""
              function packet(seq,amountA,amountB)
                local bid=GameInfo.Buildings.BUILDING_AMPHITHEATER.Index
                local p={Action='DIALOGUE_SAMPLE',Token='facts:'..seq,Seq=seq,Turn=turn,Generation=dialogue.generation,Valid=1,
                  FactsEpoch=shared.GreatWorkFacts.epoch,FactsInput=shared.GreatWorkFacts.inputRevision,FactsRefs='',FactsData='',FactsCount=0,FactsCities=2,Data='',Count=0,AdjData='',AdjCount=0}
                for _,c in ipairs({a,b})do
                  p.FactsRefs=p.FactsRefs..c.id..','..SPCGreatWorkFacts.Hex(SPCNetworkInput.Reference(c))..',1;'
                  p.Data=p.Data..c.id..',-1,EMPTY;';p.Count=p.Count+1
                  for i=1,(c==a and amountA or amountB)do
                    local work=c.id*100+i
                    p.FactsData=p.FactsData..c.id..','..bid..','..(i-1)..','..work..',GREATWORK_BHASA_1;';p.FactsCount=p.FactsCount+1
                    p.Data=p.Data..c.id..','..work..',GREATWORK_BHASA_1;';p.Count=p.Count+1
                  end
                end
                p.Data=p.Data:sub(1,-2);return p
              end
              function sample(seq,n,m)meaningRequest(0,packet(seq,n,m))end
            """)
        if ready:l.execute("fire('LoadScreenClose')")
        return l
    def test_automatic_without_panel_two_cities_and_exact_final_values(self):
        l=self.runtime();l.execute("assert(meaning.ready and meaning.recipientStatus=='VERIFIED_LOADED_SET');assert(finalAmount(a,'SCIENCE')==3 and finalAmount(b,'SCIENCE')==3);assert(finalAmount(a,'CULTURE')==0);assert(gwa.retired and oldCount(a)==0)")
    def test_per_domain_floor_share_and_w_inherited(self):
        l=self.runtime();l.execute(r"""
          local w={count=2,hasConfirmed=true,availability='KNOWN',modifierExcludedCount=0,unknownCategoryCount=0}
          local f={validity='VERIFIED',identity='CULTURE',potential=4,activeStatus='KNOWN',active=4}
          local v={validity='VERIFIED',availability='READY',value={districts={},domains={}}}
          for _,entry in ipairs(SPCCultureMeaningModel.Domains)do v.value.domains[entry[1]]={value=1}end
          local p=SPCCultureMeaningModel.Plan(f,w,v);assert(p.each.PRODUCTION==0 and p.each.GOLD==2 and p.total.GOLD==4)
        """)
    def test_same_turn_d_replaces_old_single_value_and_duplicate_zero_writes(self):
        l=self.runtime();l.execute(r"""
          building(a,'BUILDING_RESEARCH_LAB',a.ds[6],false);fire('CityBuildingsChanged',0,1)
          assert(finalAmount(a,'SCIENCE')==1 and finalAmount(b,'SCIENCE')==3)
          local before=writes;update();update();assert(writes==before)
          building(a,'BUILDING_RESEARCH_LAB',a.ds[6]);fire('BuildingAddedToMap',a.ds[6].x,0,GameInfo.Buildings.BUILDING_RESEARCH_LAB.Index,0)
          assert(finalAmount(a,'SCIENCE')==3 and not a.present[GameInfo.Buildings.BUILDING_SPC_MEANING_PROBE_SCIENCE_VALUE_1.Index])
        """)
    def test_w_change_only_updates_plan_without_duplicate_carrier(self):
        l=self.runtime();l.execute("local before=writes;a.workCount=2;shared.GreatWorkFacts.OnConfirmed(0,{1});assert(meaning.records['0:1'].total.SCIENCE==6 and writes==before and meaning.records['0:2'].count==1)")
    def test_real_facts_callback_move_both_endpoints_and_duplicate_ack(self):
        l=self.runtime(real=True);l.execute("sample(1,1,1);assert(finalAmount(a,'SCIENCE')==3);sample(2,2,0);assert(meaning.records['0:1'].count==2 and meaningCount(b)==0);local before=writes;sample(2,2,0);assert(writes==before);sample(3,1,1);assert(finalAmount(b,'SCIENCE')==3)")
    def test_active_downgrade_and_same_turn_governor_restoration(self):
        l=self.runtime();l.execute("a.active=1;fire('GovernorAssigned',0,1,0);assert(meaningCount(a)==0 and finalAmount(b,'SCIENCE')==3);a.active=4;fire('GovernorEstablished',0,1,0);assert(finalAmount(a,'SCIENCE')==3)")
    def test_governor_assignment_recomputes_old_and_new_city(self):
        l=self.runtime();l.execute("a.active=1;b.active=4;fire('GovernorAssigned',0,2,0);assert(meaningCount(a)==0 and finalAmount(b,'SCIENCE')==3)")
    def test_known_district_notification_is_scoped_to_owner_city(self):
        l=self.runtime();l.execute("local handler=Events.DistrictBuildProgressChanged.list[#Events.DistrictBuildProgressChanged.list];local before=counts.city_scan;handler(0,6,1);assert(counts.city_scan==before+1);before=counts.city_scan;handler(3,6,1);assert(counts.city_scan==before)")
    def test_inactive_does_not_wait_for_works_and_identity_exit(self):
        l=self.runtime();l.execute("a.worksUnknown=true;a.active=1;update();assert(meaningCount(a)==0);a.identity='RESEARCH';a.active=4;update();assert(meaningCount(a)==0)")
    def test_unknown_current_inputs_retain_only_confirmed_session(self):
        for kind in ('factsUnknown','worksUnknown','active'):
            with self.subTest(kind=kind):
                l=self.runtime();l.globals().kind=kind;l.execute("if kind=='active'then a.active=nil else a[kind]=true end;local before=writes;update();assert(finalAmount(a,'SCIENCE')==3 and writes==before and meaning.errors['0:1'])")
    def test_new_reference_unknown_does_not_replay_loaded_projection(self):
        l=self.runtime();l.execute("a.token='replacement';a.factsUnknown=true;update();assert(meaningCount(a)==0 and meaning.records['0:1']==nil)")
    def test_cold_load_clears_saved_legacy_and_rebuilds_from_changed_facts(self):
        l=self.runtime();l.execute(r"""
          seed(a,'BUILDING_SPC_B060_SCIENCE_P1');seed(a,'BUILDING_SPC_MEANING_PROBE_PRODUCTION_0')
          a.active=1;fire('LoadScreenClose');assert(oldCount(a)==0 and meaningCount(a)==0 and finalAmount(b,'SCIENCE')==3)
          a.active=4;fire('GovernorEstablished',0,1,0);assert(finalAmount(a,'SCIENCE')==3)
        """)
    def test_cold_unknown_and_missed_load_ready_on_real_sample(self):
        l=self.runtime(real=True,ready=False);l.execute("assert(not meaning.ready);sample(1,1,1);assert(meaning.ready and finalAmount(a,'SCIENCE')==3)")
        l=self.runtime();l.execute("a.worksUnknown=true;fire('LoadScreenClose');assert(meaningCount(a)==0);a.worksUnknown=false;shared.GreatWorkFacts.OnConfirmed(0,{1});assert(finalAmount(a,'SCIENCE')==3)")
    def test_foreign_saved_carriers_withdraw_without_ai_gameplay(self):
        l=self.runtime(ready=False);l.execute("b.owner=3;seed(b,'BUILDING_SPC_MEANING_PROBE_GOLD_VALUE_4');seed(b,'BUILDING_SPC_B060_GOLD_P1');b.factsUnknown=true;fire('LoadScreenClose');assert(oldCount(b)==0 and meaningCount(b)==0 and finalAmount(a,'SCIENCE')==3 and not meaning.records['3:2'])")
    def test_confirmed_loss_exit_unknown_no_clear_and_recapture_current_gate(self):
        l=self.runtime();l.execute(r"""
          local loss={confirmed=false,targetID=1,origin={owner=0}}
          assert(not pcall(exits.CultureMeaning,a,loss));assert(finalAmount(a,'SCIENCE')==3)
          a.owner=3;loss.confirmed=true;exits.CultureMeaning(a,loss);exits.CultureMeaning(a,loss)
          assert(meaningCount(a)==0 and meaning.records['0:1']==nil and finalAmount(b,'SCIENCE')==3)
          a.owner=0;a.active=1;returns.CultureMeaning(0,a);assert(meaningCount(a)==0)
          a.active=4;returns.CultureMeaning(0,a);assert(finalAmount(a,'SCIENCE')==3)
        """)
    def test_owner_change_during_native_write_cannot_apply_foreign_effects(self):
        l=self.runtime();l.execute(r"""
          a.active=1;update();a.active=4
          local create=P.CreateBuilding;local once=false
          P.CreateBuilding=function(q,id)
            create(q,id)
            if q.city==a and not once then once=true;a.owner=3;exits.CultureMeaning(a,{confirmed=true,targetID=1,origin={owner=0}})end
          end
          update();assert(meaningCount(a)==0 and meaning.records['0:1']==nil and finalAmount(b,'SCIENCE')==3)
        """)
    def test_old_writer_receive_init_audit_controls_cannot_resurrect(self):
        l=self.runtime();legacy.bind_actual_request(l);l.execute(r"""
          local before=writes;gwa.Init();gwa.Audit(0);assert(gwa.Receive(0,{})==false)
          for _,action in ipairs({'GWA_AUTO','GWA_OFF','CULTURE_MEANING_ADVANCE','CULTURE_MEANING_GATE_ADVANCE','CULTURE_MEANING_END','CULTURE_MEANING_CONFIG','CULTURE_MEANING_DIAGNOSTIC_ADVANCE'})do
            meaningRequest(0,{Action=action,CityID=1,Token=action})
          end
          assert(oldCount(a)==0 and finalAmount(a,'SCIENCE')==3 and writes==before and not dialogue.meaningOverride)
        """)
    def test_readonly_status_no_native_write_or_fact_scan(self):
        l=self.runtime();legacy.bind_actual_request(l);l.execute("local before=writes;local captures=counts.dc_capture;meaningRequest(0,{Action='CULTURE_MEANING_STATUS',CityID=1,Token='read'});assert(writes==before and counts.dc_capture==captures and shared.CultureMeaningView==nil and shared.Snapshot:find('自动生效',1,true))")
    def test_unknown_loaded_recipient_gate_never_falls_back_to_old_yields(self):
        l=self.runtime(ready=False);l.execute(r"""
          local rows=GameInfo.GreatWorks
          GameInfo.GreatWorks=setmetatable({}, {__index=rows,__call=function()local it=rows();local extra=false;return function()local v=it();if v then return v end;if not extra then extra=true;return {GreatWorkType='GREATWORK_UNKNOWN_MOD',GreatWorkObjectType='GREATWORKOBJECT_WRITING'}end end end})
          fire('LoadScreenClose');assert(meaning.recipientStatus=='BLOCKED_LOADED_SET' and meaningCount(a)==0 and oldCount(a)==0)
        """)
    def test_exact_legacy_cleanup_failure_blocks_only_affected_city(self):
        l=self.runtime(ready=False);l.execute("seed(a,'BUILDING_SPC_B060_SCIENCE_P1');failRemove=GameInfo.Buildings.BUILDING_SPC_B060_SCIENCE_P1.Index;fire('LoadScreenClose');assert(meaningCount(a)==0 and meaning.errors['0:1'] and finalAmount(b,'SCIENCE')==3);failRemove=nil;update();assert(oldCount(a)==0 and finalAmount(a,'SCIENCE')==3)")
    def test_unknown_old_carrier_presence_cannot_be_treated_as_absence(self):
        l=self.runtime(ready=False);l.execute(r"""
          local has=P.HasBuilding;local id=GameInfo.Buildings.BUILDING_SPC_B060_SCIENCE_P1.Index
          P.HasBuilding=function(buildings,index)if buildings.city==a and index==id then return nil end;return has(buildings,index)end
          fire('LoadScreenClose');assert(meaningCount(a)==0 and meaning.errors['0:1'] and finalAmount(b,'SCIENCE')==3)
          P.HasBuilding=has;update();assert(finalAmount(a,'SCIENCE')==3)
        """)
    def test_failed_reconfiguration_never_adds_new_over_residual(self):
        l=self.runtime();l.execute("failRemove=GameInfo.Buildings.BUILDING_SPC_MEANING_PROBE_SCIENCE_VALUE_3.Index;building(a,'BUILDING_RESEARCH_LAB',a.ds[6],false);fire('CityBuildingsChanged',0,1);assert(not a.present[GameInfo.Buildings.BUILDING_SPC_MEANING_PROBE_SCIENCE_VALUE_1.Index] and meaning.errors['0:1']);failRemove=nil;update();assert(finalAmount(a,'SCIENCE')==1)")
    def test_reentrant_real_qualification_change_gets_one_current_catchup(self):
        l=self.runtime();l.execute(r"""
          local read=shared.EffectiveFacts.Read;local once=false
          shared.EffectiveFacts.Read=function(pid,c)
            local f=read(pid,c)
            if c==a and not once then once=true;a.active=1;meaning.Audit({player=0,city=1})end
            return f
          end
          update();assert(meaningCount(a)==0 and meaning.records['0:1'].active==1 and not meaning.busy and not meaning.draining)
        """)
    def test_reentrant_recalculation_queue_is_bounded_not_a_retry_loop(self):
        l=self.runtime();l.execute(r"""
          local read=shared.EffectiveFacts.Read;local visits=0
          shared.EffectiveFacts.Read=function(pid,c)visits=visits+1;meaning.Audit({player=pid,city=c:GetID()});return read(pid,c)end
          update();assert(visits==2 and meaning.pending and not meaning.busy and not meaning.draining)
        """)
    def test_owned_carrier_events_do_not_cause_recursive_census(self):
        l=self.runtime();l.execute("local before=counts.dc_capture;local scans=counts.city_scan;fire('BuildingAddedToMap',a.ds[1].x,0,GameInfo.Buildings.BUILDING_SPC_MEANING_PROBE_SCIENCE_VALUE_3.Index,0);assert(counts.dc_capture==before and counts.city_scan==scans)")
    def test_ordinary_buildings_and_no_permanent_city_writes(self):
        l=self.runtime();l.execute("a.active=1;update();assert(a.present[GameInfo.Buildings.BUILDING_LIBRARY.Index] and a.present[GameInfo.Buildings.BUILDING_PALACE.Index]);assert(meaningCount(a)==0)")
    def test_actual_positive_dialogue_has_no_meaning_override(self):
        l=self.runtime();l.execute("dialogue.Init();dialogue.samples[0]={turn=turn,seq=1,cities={[1]={{id=1,type='GREATWORK_BHASA_1'},{id=2,type='GREATWORK_SHAKESPEARE_1'}},[2]={{id=3,type='GREATWORK_BHASA_1'}}}};dialogue.Audit(0);assert(dialogue.last[0][1].applied>0 and finalAmount(a,'SCIENCE')==3 and not dialogue.meaningOverride)")
    def test_retired_ui_producer_keeps_facts_without_base_adjacency_reads(self):
        from test_p0_k import Fixture, PRODUCER
        fx=Fixture();fx.check(PRODUCER)
        fx.check("shared.GreatWorkAdjacency.retired=true")
        fx.lua.execute((R/'Mod/UI/DialogueRefresh.lua').read_text())
        fx.check(r"""
          SPCGWAdjacencyModel.Collect=function()error('RETIRED_BASE_ADJACENCY_READ')end
          init();assert(lastPacket.Valid==1 and lastPacket.AdjData=='' and lastPacket.AdjCount==0)
          local ui=ExposedMembers.SPC_DialogueBackground;local scans=ui.scans
          fire('FeatureRemovedFromMap');fire('SystemUpdateUI');assert(ui.scans==scans)
          a.slots[10]={100};fire('GreatWorkCreated',0,999,a.x,a.y,10,100);fire('SystemUpdateUI')
          assert(shared.GreatWorkFacts.Read(0,7).count==1 and ui.scans==scans+1)
        """)
    def test_no_probe_can_start_while_normal_owner_is_registered(self):
        l=self.runtime();l.globals().include('CultureMeaningProbe');l.execute("assert(not pcall(SPCCultureMeaningProbe.Start,P,shared))")
    def test_package_and_sql_are_unchanged_native_family(self):
        root=ET.parse(R/'Mod/SpecializationP0.modinfo').getroot();self.assertEqual(root.get('version'),'193')
        imports=[e.text for e in root.findall("./InGameActions/ImportFiles[@id='SPCP0_Common']/File")];files=[e.text for e in root.find('Files')]
        self.assertEqual(imports.count('CultureMeaning.lua'),1);self.assertEqual(files.count('CultureMeaning.lua'),1)
        self.assertEqual((R/'Mod/Data/CultureMeaningProbe.sql').read_bytes(),subprocess.check_output(['git','show','fffecc7:Mod/Data/CultureMeaningProbe.sql'],cwd=R))
        src=(R/'Mod/Gameplay.lua').read_text();self.assertNotIn('SPCCultureMeaningProbe.Start(P,shared)',src);self.assertIn('SPCCultureMeaning.Start(P,shared)',src)
        panel=(R/'Mod/UI/P0Panel.lua').read_text();self.assertIn("request('CULTURE_MEANING_STATUS')",panel);self.assertNotIn("request('CULTURE_MEANING_GATE_ADVANCE')",panel)
        l=LuaRuntime();
        for path in ['CultureMeaning.lua','CultureMeaningProbe.lua','GreatWorkAdjacency.lua','Gameplay.lua','CultureAesthetic.lua','UI/DialogueRefresh.lua','UI/P0Panel.lua','Probe.lua']:
            l.execute('assert(load(...))',(R/'Mod'/path).read_text())

def load_tests(loader,tests,pattern):
    # Current native DB already contains L1 SQL. Rebuild only exact owned
    # definitions in memory; inherited source and semantic assertions stay intact.
    class CurrentAestheticFixture(ae.AestheticTests):
        @classmethod
        def setUpClass(cls):cls.sql=legacy.database()
        @classmethod
        def tearDownClass(cls):cls.sql.close()
    for name in ['test_formula_and_two_cities','test_unknown_reference_load_and_gate',
                 'test_confirmed_loss_recapture_only_current','test_same_turn_change_idle_and_cleanup',
                 'test_inactive_city_still_clears_exact_legacy','test_failed_legacy_withdrawal_and_bounded_errors',
                 'test_missed_load_confirmed_sample_starts_without_panel']:
        tests.addTest(CurrentAestheticFixture(name))
    import test_p0_k as k
    wanted=['test_same_turn_move_then_return_updates_both_city_counts',
            'test_wrong_epoch_and_duplicate_sequence_cannot_poison',
            'test_binding_change_rejects_old_reference_and_removes_current_fact',
            'test_exit_return_and_cold_load_are_session_only',
            'test_native_create_move_same_turn_scope_and_redundant_input',
            'test_native_district_and_governor_parameter_scope',
            'test_generation_and_epoch_changes_recollect_same_turn']
    added=0
    for cls in vars(k).values():
        if isinstance(cls,type) and issubclass(cls,unittest.TestCase):
            for name in wanted:
                if hasattr(cls,name):tests.addTest(cls(name));added+=1
    assert added==len(wanted),'Direct K regression entry changed; review required'
    return tests

if __name__=='__main__':unittest.main()
