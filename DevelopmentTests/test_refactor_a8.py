"""Approved eight-era successor tests. Lua51 + explicit read-only DB memory copy."""
from pathlib import Path
import json
import sqlite3
import unittest
from refactor_harness import Context,ROOT,TrackedLua51,legacy_source_observation,measure
from project_paths import external_database


def reset_projection(db,prefix,modifier):
    buildings=[v[0] for v in db.execute("SELECT BuildingType FROM Buildings WHERE substr(BuildingType,1,?)=?",(len(prefix),prefix))]
    modifiers=[v[0] for v in db.execute("SELECT ModifierId FROM Modifiers WHERE substr(ModifierId,1,?)=?",(len(modifier),modifier))]
    for table,col,values in [('BuildingModifiers','BuildingType',buildings),('Buildings','BuildingType',buildings),('Types','Type',buildings),('ModifierArguments','ModifierId',modifiers),('Modifiers','ModifierId',modifiers)]:
        db.executemany('DELETE FROM '+table+' WHERE '+col+'=?',[(v,) for v in values])


class EightEras(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        import test_culture_meaning_probe as legacy
        import test_culture_aesthetic as ae
        ae.LuaRuntime=TrackedLua51
        cls.db=legacy.database() # explicit read-only external DB -> disposable in-memory copy
        reset_projection(cls.db,'BUILDING_SPC_INSPIRATION_ERA_','SPC_INSPIRATION_ERA_')
        reset_projection(cls.db,'BUILDING_SPC_DIALOGUE_TOTAL_','SPC_DIALOGUE_TOTAL_')
        cls.db.execute('DROP TABLE IF EXISTS SPC_DialogueTotals')
        for name in ['CultureInspiration','DialogueEffects']:
            cls.db.executescript((ROOT/'Mod/Data'/f'{name}.sql').read_text())
    @classmethod
    def tearDownClass(cls):cls.db.close()
    def inspiration(self,real=False):
        from test_culture_inspiration_automatic import InspirationAutomaticTests
        helper=InspirationAutomaticTests();helper.sql=self.db
        with legacy_source_observation():return helper.runtime(real=real)
    def effects(self):
        from test_dialogue_effects import Effects
        helper=Effects();helper.sql=self.db
        with legacy_source_observation():return helper.runtime()
    def test_model_zero_to_eight_and_invalid_nine_fraction_negative(self):
        c=Context();c.load('CultureInspirationModel');c.execute("f={validity='VERIFIED',identity='CULTURE',potential=4,activeStatus='KNOWN',active=4};for e=0,8 do local p=SPCCultureInspirationModel.Plan(f,{hasConfirmed=true,availability='KNOWN',eraCount=e});assert(p.percent==e*3 and p.eras==e)end;for _,e in ipairs({-1,9,.5})do assert(not pcall(SPCCultureInspirationModel.Plan,f,{hasConfirmed=true,availability='KNOWN',eraCount=e}))end")
    def test_actual_writer_eight_to_seven_to_eight_unknown_and_duplicate(self):
        l=self.inspiration();l.execute("a.eras=8;refresh();assert(inspiration(a)==24);local n=writes;refresh();assert(writes==n);a.eras=7;refresh();assert(inspiration(a)==21);a.eras=8;refresh();assert(inspiration(a)==24);n=writes;a.worksUnknown=true;refresh();assert(inspiration(a)==24 and writes==n);a.worksUnknown=false;a.identity='NONE';a.active=0;refresh();assert(inspiration(a)==0)")
    def test_actual_catalogue_and_facts_count_eight_without_pool_change(self):
        l=self.inspiration(True);l.execute("local cat=SPCGreatWorkCatalog.Build(P);local found,works={},{};for kind,w in pairs(cat.works)do if not found[w.era]then found[w.era]=true;works[#works+1]={id=#works+1,type=kind}end end;assert(#works==8);local f=SPCGreatWorkFacts.Plan(cat,works);assert(f.eraCount==8 and f.count==8 and f.eras.ERA_ANCIENT);works[#works+1]={id=99,type=works[1].type};works[#works+1]={id=100,type='UNSUPPORTED_NATIVE_WRITING'};local g=SPCGreatWorkFacts.Plan(cat,works,function()return 'GREATWORKOBJECT_WRITING'end);assert(g.eraCount==8 and g.count==9 and g.modifierExcludedCount==1)")
    def test_actual_controller_store_x8_one_receipt_reload_and_x9_safe_failure(self):
        import test_store_write_boundaries as storage
        import test_dialogue_projects as module
        storage.LuaRuntime=TrackedLua51
        # Scalar-x transport at B353; current raw eight-era completion is covered in S9b2.
        from test_refactor_s9b2 import before
        with before(),legacy_source_observation():l=module.game()
        l.execute("sampleX=8;duplicate=true;begin(c);GameEra='ERA_INFORMATION';endturn();assert(ledger(c).total==40 and ledger(c).used.ERA_CLASSICAL.x==8 and not ledger(c).used.ERA_INFORMATION and samples==1 and finishes==1);local old=T.encode(ledger(c));Events.CityProjectCompleted.Fire(0,c:GetID(),999);assert(T.encode(ledger(c))==old);reload();assert(T.encode(ledger(c))==old);sampleX=9;begin(c);endturn();assert(ledger(c).total==40 and ledger(c).pending.stage=='HELD' and samples==2)")
    def test_model_old_receipt_valid_new_x8_valid_x9_rejected_without_mutation(self):
        c=Context();c.load('DialogueProjectModel');c.execute("local M=SPCDialogueProjectModel;local r={owner=0,cityID=1,x=1,y=1};local v=M.Begin(nil,'T',r,'ERA_ANCIENT',1);local a=M.Complete(v,v.serial,7,2);assert(a.total==35 and M.Validate(a));local b=M.Begin(a,'T',r,'ERA_CLASSICAL',2);local d=M.Complete(b,b.serial,8,3);assert(d.total==75 and M.Validate(d));assert(not pcall(M.Complete,b,b.serial,9,3));assert(b.pending and b.total==35 and not b.used.ERA_CLASSICAL)")
    def test_effect_history_covers_all_loaded_game_eras_not_eight_game_era_cap(self):
        l=self.effects();l.execute("history(a,{8,8,8,8,8,8,8,8,8});one();assert(total(a)==360 and a.history.total==360);local n=writes;one();assert(writes==n);history(a,{7,7,7,7,7,7,7,7,7});one();assert(total(a)==315);assert(effects.IsOwnedCarrier('BUILDING_SPC_DIALOGUE_TOTAL_360'))")
    def test_sql_exact_new_values_seven_categories_and_pillage_zero(self):
        d=self.db;eras=d.execute('SELECT COUNT(*) FROM Eras').fetchone()[0]
        values=[r[0]for r in d.execute('SELECT Bonus FROM SPC_DialogueTotals ORDER BY Bonus')]
        self.assertEqual(values,list(range(5,40*eras+1,5)))
        self.assertEqual(dict(d.execute("SELECT Name,Value FROM ModifierArguments WHERE ModifierId='SPC_INSPIRATION_ERA_8'")),{'Amount':'24'})
        self.assertEqual(d.execute("SELECT ModifierId FROM BuildingModifiers WHERE BuildingType='BUILDING_SPC_INSPIRATION_ERA_8'").fetchall(),[('SPC_INSPIRATION_ERA_8',)])
        for n in values:
            args=d.execute("SELECT a.Value FROM BuildingModifiers b JOIN ModifierArguments a USING(ModifierId) WHERE b.BuildingType=? AND a.Name='ScalingFactor'",('BUILDING_SPC_DIALOGUE_TOTAL_'+str(n),)).fetchall()
            self.assertEqual(args,[(str(100+n),)]*7)
        before=d.execute("SELECT * FROM Buildings_XP2 WHERE substr(BuildingType,1,13)!='BUILDING_SPC_' ORDER BY BuildingType").fetchall()
        d.executescript((ROOT/'Mod/Data/InternalCarrierPillage.sql').read_text())
        for name in ['BUILDING_SPC_INSPIRATION_ERA_8','BUILDING_SPC_DIALOGUE_TOTAL_'+str(40*eras)]:
            self.assertEqual(d.execute('SELECT Pillage FROM Buildings_XP2 WHERE BuildingType=?',(name,)).fetchone(),(0,))
        self.assertEqual(before,d.execute("SELECT * FROM Buildings_XP2 WHERE substr(BuildingType,1,13)!='BUILDING_SPC_' ORDER BY BuildingType").fetchall())
        measure('A8_loaded_database',{'game_eras':eras,'max_dialogue_total':40*eras,'new_inspiration_percent':24,'dialogue_category_count':7,'source':'configured read-only DB, disposable copy only'})
    def test_tooltip_both_locales_matches_accepted_maximum(self):
        d=sqlite3.connect(':memory:');d.execute('CREATE TABLE LocalizedText(Language,Tag,Text,PRIMARY KEY(Language,Tag))');d.executescript((ROOT/'Mod/Text/TestText.sql').read_text())
        rows=d.execute("SELECT Language,Text FROM LocalizedText WHERE Tag='LOC_SPC_CULTURE_INSTITUTION_4_HELP'").fetchall();self.assertEqual(len(rows),2)
        for _,text in rows:self.assertIn('最多8个时代，最高+24%',text);self.assertNotIn('最多7个时代',text)
        d.close()

if __name__=='__main__':unittest.main()
