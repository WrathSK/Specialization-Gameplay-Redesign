"""B176 native-carrier comparison. Actual Lua/request/SQL, simulated engine only.
Read-only configured DB is copied to memory; no saved Dialogue/history writes.
"""
from pathlib import Path
import unittest, xml.etree.ElementTree as ET
from lupa.lua55 import LuaRuntime
import test_culture_meaning_automatic as auto
import test_culture_meaning_probe as legacy
R=Path(__file__).resolve().parents[1]

class CarrierTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sql=legacy.database()
        # Rebuild this family's exact definition IDs only in the disposable DB.
        for table,col in [('BuildingModifiers','ModifierId'),('ModifierArguments','ModifierId'),('Modifiers','ModifierId'),('Buildings','BuildingType'),('Types','Type')]:
            cls.sql.execute(f"DELETE FROM {table} WHERE {col} LIKE 'SPC_B059_%' OR {col} LIKE 'BUILDING_SPC_B059_%'")
        cls.sql.execute('DROP TABLE IF EXISTS SPC_DialogueLevels')
        cls.sql.executescript((R/'Mod/Data/Dialogue.sql').read_text())
    @classmethod
    def tearDownClass(cls):cls.sql.close()
    def runtime(self):
        h=auto.AutomaticMeaningTests();h.sql=self.sql;l=h.runtime(real=True)
        l.execute(r"""
          function sampleTwo(seq)
            local p=packet(seq,2,1)
            p.Data=p.Data:gsub('102,GREATWORK_BHASA_1','102,GREATWORK_SHAKESPEARE_1')
            p.FactsData=p.FactsData:gsub('102,GREATWORK_BHASA_1','102,GREATWORK_SHAKESPEARE_1')
            meaningRequest(0,p)
          end
          sampleTwo(1)
          function nextTest(token,c)
            c=c or a
            meaningRequest(0,{Action='DIALOGUE_CARRIER_NEXT',Token=token,CityID=c.id,Reference=SPCNetworkInput.Reference(c)})
            assert(not shared.Snapshot:find('暂停',1,true),shared.Snapshot)
          end
          function has(c,n)return c.present[GameInfo.Buildings['BUILDING_SPC_B059_TEST'..n].Index]==true end
          function assertOwned(c,expected)
            for row in GameInfo.Buildings()do if dialogue.IsOwnedCarrier(row.BuildingType)then
              assert((c.present[row.Index]==true)==(row.BuildingType==expected),row.BuildingType)
            end end
          end
        """)
        return l
    def test_sql_exact_native_types_arguments_and_unchanged_hd(self):
        for value in (100,200):
            rows=self.sql.execute("SELECT m.ModifierType,a.Name,a.Value FROM BuildingModifiers b JOIN Modifiers m USING(ModifierId) JOIN ModifierArguments a USING(ModifierId) WHERE b.BuildingType=?",(f'BUILDING_SPC_B059_TEST{value}',)).fetchall()
            factors=[v for _,name,v in rows if name=='ScalingFactor']
            self.assertEqual(factors,[str(100+value)]*14)
            self.assertEqual({t for t,_,_ in rows},{'MODIFIER_SINGLE_CITY_ADJUST_GREATWORK_YIELD','MODIFIER_SINGLE_CITY_ADJUST_TOURISM'})
            self.assertFalse(any(name in ('Amount','YieldChange') for _,name,_ in rows))
            self.assertEqual({v for _,name,v in rows if name=='GreatWorkObjectType'}, {'GREATWORKOBJECT_'+x for x in ('WRITING','MUSIC','SCULPTURE','PORTRAIT','LANDSCAPE','RELIGIOUS','ARTIFACT')})
        for name,args in {
          'HD_AMPHITHEATER_WRITING_CULTURE_BOOST':{'YieldChange':'2','YieldType':'YIELD_CULTURE','GreatWorkObjectType':'GREATWORKOBJECT_WRITING'},
          'HD_AMPHITHEATER_WRITING_TOURISM_BOOST':{'ScalingFactor':'150','GreatWorkObjectType':'GREATWORKOBJECT_WRITING'},
          'HD_BROADCAST_MUISIC_TOURISM_BOOST':{'ScalingFactor':'200','GreatWorkObjectType':'GREATWORKOBJECT_MUSIC'},
        }.items():
            self.assertEqual(dict(self.sql.execute('SELECT Name,Value FROM ModifierArguments WHERE ModifierId=?',(name,))),args)
    def test_full_cycle_scoped_replacement_and_current_auto_restoration(self):
        l=self.runtime();l.execute(r"""
          assert(dialogue.last[0][1].applied==25);local science=finalAmount(a,'SCIENCE');local other=dialogue.last[0][2].applied
          nextTest('base');assertOwned(a,nil);assert(dialogue.carrierTest.percent==0)
          nextTest('100');assertOwned(a,'BUILDING_SPC_B059_TEST100')
          nextTest('200');assertOwned(a,'BUILDING_SPC_B059_TEST200')
          assert(finalAmount(a,'SCIENCE')==science and dialogue.last[0][2].applied==other)
          nextTest('end');assert(not dialogue.carrierTest and not dialogue.meaningOverride)
          assertOwned(a,'BUILDING_SPC_B059_D2');assert(finalAmount(a,'SCIENCE')==science)
        """)
    def test_active_three_can_probe_without_changing_old_auto_gate(self):
        l=self.runtime();l.execute("a.active=3;dialogue.Audit(0,1);assert(dialogue.last[0][1].applied==0);nextTest('base');nextTest('100');assert(has(a,100));nextTest('200');nextTest('end');assertOwned(a,nil)")
    def test_duplicate_click_is_idempotent_including_end(self):
        l=self.runtime();l.execute("nextTest('base');local before=writes;nextTest('base');assert(writes==before and dialogue.carrierTest.percent==0);nextTest('100');before=writes;nextTest('100');assert(writes==before and has(a,100));nextTest('200');nextTest('end');before=writes;nextTest('end');assert(writes==before and not dialogue.carrierTest)")
    def test_packet_reference_other_city_and_unsupported_owner_rejected(self):
        l=self.runtime();l.execute(r"""
          nextTest('base');nextTest('100');local before=writes
          meaningRequest(0,{Action='DIALOGUE_CARRIER_NEXT',Token='wrong',CityID=1,Reference='wrong'})
          assert(shared.Snapshot:find('REFERENCE_CHANGED',1,true) and writes==before)
          meaningRequest(0,{Action='DIALOGUE_CARRIER_NEXT',Token='other',CityID=2,Reference=SPCNetworkInput.Reference(b)})
          assert(shared.Snapshot:find('OTHER_CITY',1,true) and writes==before and has(a,100))
          assert(not pcall(dialogue.CarrierTestNext,3,a,'foreign',SPCNetworkInput.Reference(a)))
        """)
    def test_unknown_before_start_does_not_acquire_or_clear_fixture(self):
        l=self.runtime();l.execute("a.active=nil;local before=writes;meaningRequest(0,{Action='DIALOGUE_CARRIER_NEXT',Token='unknown',CityID=1,Reference=SPCNetworkInput.Reference(a)});assert(shared.Snapshot:find('ACTIVE_UNKNOWN',1,true));assert(writes==before and not dialogue.carrierTest and not dialogue.meaningOverride)")
    def test_reconfiguration_failure_never_adds_over_residual_and_next_exits(self):
        l=self.runtime();l.execute(r"""
          nextTest('base');nextTest('100');failRemove=GameInfo.Buildings.BUILDING_SPC_B059_TEST100.Index
          meaningRequest(0,{Action='DIALOGUE_CARRIER_NEXT',Token='200',CityID=1,Reference=SPCNetworkInput.Reference(a)})
          assert(dialogue.carrierTest.error and has(a,100) and not has(a,200))
          failRemove=nil;nextTest('recover-end');assert(not dialogue.carrierTest);assertOwned(a,'BUILDING_SPC_B059_D2')
        """)
    def test_create_failure_keeps_action_recoverable_without_history_write(self):
        l=self.runtime();l.execute("nextTest('base');failCreate=true;meaningRequest(0,{Action='DIALOGUE_CARRIER_NEXT',Token='100',CityID=1,Reference=SPCNetworkInput.Reference(a)});assert(dialogue.carrierTest.error and not has(a,100));failCreate=false;nextTest('recover');assert(not dialogue.carrierTest)")
    def test_governor_drop_withdraws_and_end_does_not_restore_snapshot(self):
        l=self.runtime();l.execute("nextTest('base');nextTest('100');a.active=1;fire('GovernorAssigned',0,1,0);assertOwned(a,nil);meaningRequest(0,{Action='DIALOGUE_CARRIER_NEXT',Token='inactive',CityID=1,Reference=SPCNetworkInput.Reference(a)});assert(dialogue.carrierTest.error);nextTest('end');assert(not dialogue.carrierTest);assertOwned(a,nil)")
    def test_known_loss_exact_exit_clears_test_and_unrelated_city_survives(self):
        l=self.runtime();l.execute(r"""
          nextTest('base');nextTest('100');local beforeB=finalAmount(b,'SCIENCE')
          assert(not pcall(exits.Dialogue,a,{confirmed=false,targetID=1,origin={owner=0,cityID=1}}));assert(has(a,100))
          a.owner=3;exits.Dialogue(a,{confirmed=true,targetID=1,origin={owner=0,cityID=1}})
          assert(not dialogue.carrierTest and not dialogue.meaningOverride and not has(a,100));assert(finalAmount(b,'SCIENCE')==beforeB)
        """)
    def test_saved_test_carrier_is_not_control_authority_on_reconstruction(self):
        l=self.runtime();l.execute(r"""
          nextTest('base');nextTest('100');nextTest('200');assert(has(a,200))
          exits.Dialogue=nil;returns.Dialogue=nil;SPCDialogue.Start(P,shared);dialogue=shared.Dialogue
          assert(not dialogue.carrierTest and not dialogue.meaningOverride);dialogue.Init();assertOwned(a,nil)
          sampleTwo(2);assertOwned(a,'BUILDING_SPC_B059_D2')
        """)
    def test_reference_change_does_not_write_or_accept_new_fixture(self):
        l=self.runtime();l.execute("nextTest('base');nextTest('100');a.token='new-reference';local before=writes;meaningRequest(0,{Action='DIALOGUE_CARRIER_NEXT',Token='bad',CityID=1,Reference=SPCNetworkInput.Reference(a)});assert(shared.Snapshot:find('OTHER_CITY',1,true) and writes==before)")
    def test_end_recomputes_changed_collection_and_never_replays_25_percent(self):
        l=self.runtime();l.execute("nextTest('base');nextTest('100');sample(2,1,1);nextTest('200');nextTest('end');assert(dialogue.last[0][1].applied==0);assertOwned(a,nil)")
    def test_unknown_current_sample_is_not_confirmed_or_a_successful_restore(self):
        l=self.runtime();l.execute("nextTest('base');nextTest('100');nextTest('200');turn=turn+1;meaningRequest(0,{Action='DIALOGUE_CARRIER_NEXT',Token='end',CityID=1,Reference=SPCNetworkInput.Reference(a)});assert(dialogue.carrierTest.error and not has(a,200));sampleTwo(2);nextTest('retry-end');assert(not dialogue.carrierTest);assertOwned(a,'BUILDING_SPC_B059_D2')")
    def test_noninterference_with_ordinary_buildings_and_project_state(self):
        l=self.runtime();l.execute(r"""
          local calls=0;shared.DialogueProjects={Describe=function()calls=calls+1;return '+5% / used Medieval' end}
          nextTest('base');nextTest('100');nextTest('200');nextTest('end')
          assert(calls==0 and a.present[GameInfo.Buildings.BUILDING_AMPHITHEATER.Index])
          meaningRequest(0,{Action='DIALOGUE_PROJECT_READ',Token='report',CityID=1})
          assert(calls==1 and shared.Snapshot:find('+5% / used Medieval',1,true))
        """)
    def test_package_syntax_localization_and_visible_button_remain_bounded(self):
        tree=ET.parse(R/'Mod/SpecializationP0.modinfo');self.assertEqual(tree.getroot().get('version'),'203')
        l=LuaRuntime();check=l.eval('function(s)local f,e=load(s);assert(f,e)end')
        for name in ['Dialogue.lua','Gameplay.lua','Probe.lua','UI/P0Panel.lua']:check((R/'Mod'/name).read_text())
        from test_p0_panel_current_layout import panel_runtime
        tree,l=panel_runtime()
        l.execute("SPCNetworkInput={Reference=function()return 'fixture-ref'end};Controls.GWCityButton.callbacks[Mouse.eLClick]();assert(requests[#requests].Action=='DIALOGUE_PROJECT_READ');Controls.GWCityButton.callbacks[Mouse.eRClick]();assert(requests[#requests].Action=='DIALOGUE_CARRIER_NEXT' and requests[#requests].Reference=='fixture-ref')")
        self.assertFalse(l.globals().Controls.GWCityButton.hidden)
        import sqlite3
        d=sqlite3.connect(':memory:');d.execute('CREATE TABLE LocalizedText(Language TEXT,Tag TEXT,Text TEXT,PRIMARY KEY(Language,Tag))')
        d.executescript((R/'Mod/Text/DialogueProjects.sql').read_text())
        self.assertEqual(d.execute('SELECT COUNT(*) FROM LocalizedText').fetchone()[0],8)
        self.assertEqual(d.execute("SELECT COUNT(*) FROM LocalizedText WHERE Tag='LOC_SPC_DIALOGUE_CARRIER_HINT'").fetchone()[0],2)
        d.close()
        files=[e.text for e in ET.parse(R/'Mod/SpecializationP0.modinfo').findall('./Files/File')]
        self.assertEqual(len(files),len(set(files)))
        self.assertEqual(set(files),{p.relative_to(R/'Mod').as_posix() for p in (R/'Mod').rglob('*') if p.is_file() and p.name not in ('SpecializationP0.modinfo','.DS_Store')})
        self.assertTrue(l.globals().Controls.DialogueTest100Button.hidden)

if __name__=='__main__':unittest.main(verbosity=2)
