"""B263 identity composition and access regression; rendering remains a native test.

Fixtures describe database interfaces and hostile original traits. No installation
paths, external assets or game writes are required by these repeatable checks.
"""
from pathlib import Path
import sqlite3
import unittest
import xml.etree.ElementTree as ET
from lupa.lua55 import LuaRuntime
from test_expedition_training import fixture as training_fixture

ROOT = Path(__file__).resolve().parents[1]
MOD = ROOT / 'Mod'
CIV = 'CIVILIZATION_SPC_AMERICA'
LEADER = 'LEADER_SPC_T_ROOSEVELT'
OLD = 'CIVILIZATION_SPC_TEST'
KINDS = ('River', 'Volcano', 'Mountain', 'Desert', 'Lake', 'Sea')


def schema_db():
    db = sqlite3.connect(':memory:')
    tables = {
        'Types': 'Type TEXT PRIMARY KEY,Kind TEXT',
        'Civilizations': 'CivilizationType TEXT PRIMARY KEY,Name TEXT,Description TEXT,Adjective TEXT,StartingCivilizationLevelType TEXT,RandomCityNameDepth INTEGER,Ethnicity TEXT',
        'Leaders': "LeaderType TEXT PRIMARY KEY,Name TEXT,InheritFrom TEXT,SceneLayers INTEGER,Sex TEXT DEFAULT 'Male',SameSexPercentage INTEGER DEFAULT 0",
        'CivilizationLeaders': 'CivilizationType TEXT,LeaderType TEXT,CapitalName TEXT',
        'CityNames': 'CivilizationType TEXT,CityName TEXT,SortIndex INTEGER DEFAULT 0',
        'CivilizationCitizenNames': 'CivilizationType TEXT,CitizenName TEXT,Female INTEGER,Modern INTEGER,PRIMARY KEY(CivilizationType,CitizenName)',
        'Traits': 'TraitType TEXT PRIMARY KEY,Name TEXT,Description TEXT',
        'CivilizationTraits': 'CivilizationType TEXT,TraitType TEXT',
        'LeaderTraits': 'LeaderType TEXT,TraitType TEXT',
        'LoadingInfo': 'LeaderType TEXT,ForegroundImage TEXT,BackgroundImage TEXT,LeaderText TEXT,PlayDawnOfManAudio INTEGER,DawnOfManLeaderId TEXT',
        'DiplomacyInfo': 'Type TEXT,BackgroundImage TEXT',
        'CivilizationInfo': 'CivilizationType TEXT,Header TEXT,Caption TEXT,SortIndex INTEGER',
        'LeaderInfo': 'LeaderType TEXT,Header TEXT,Caption TEXT,SortIndex INTEGER',
        'LeaderQuotes': 'LeaderType TEXT,Quote TEXT,QuoteAudio TEXT',
    }
    for kind in KINDS:
        tables['Named' + kind + 'Civilizations'] = f'Named{kind}Type TEXT,CivilizationType TEXT'
    for table, columns in tables.items():
        db.execute(f'CREATE TABLE {table}({columns})')
    db.executescript("""
    INSERT INTO Civilizations VALUES ('CIVILIZATION_AMERICA','original','original','original','CIVILIZATION_LEVEL_FULL_CIV',10,'ETHNICITY_EURO');
    INSERT INTO Leaders VALUES ('LEADER_T_ROOSEVELT','original','LEADER_DEFAULT',4,'Male',100);
    INSERT INTO Leaders VALUES ('LEADER_DEFAULT','neutral',NULL,0,'Male',0);
    INSERT INTO CivilizationLeaders VALUES ('CIVILIZATION_AMERICA','LEADER_T_ROOSEVELT','LOC_CITY_NAME_WASHINGTON');
    INSERT INTO CivilizationTraits VALUES ('CIVILIZATION_AMERICA','TRAIT_CIVILIZATION_FOUNDING_FATHERS'),('CIVILIZATION_AMERICA','TRAIT_CIVILIZATION_BUILDING_FILM_STUDIO'),('CIVILIZATION_AMERICA','TRAIT_CIVILIZATION_UNIT_AMERICAN_P51');
    INSERT INTO LeaderTraits VALUES ('LEADER_T_ROOSEVELT','TRAIT_LEADER_ANTIQUES_AND_PARKS');
    INSERT INTO CityNames VALUES ('CIVILIZATION_AMERICA','LOC_CITY_NAME_WASHINGTON',0),('CIVILIZATION_AMERICA','LOC_CITY_NAME_NEW_YORK',1);
    INSERT INTO CivilizationCitizenNames VALUES ('CIVILIZATION_AMERICA','LOC_CITIZEN_TEST_A',0,0),('CIVILIZATION_AMERICA','LOC_CITIZEN_TEST_B',1,1),('CIVILIZATION_SCOTLAND','LOC_CITIZEN_SCOT',0,0);
    INSERT INTO CivilizationInfo VALUES ('CIVILIZATION_AMERICA','H','C',1);
    INSERT INTO LeaderInfo VALUES ('LEADER_T_ROOSEVELT','H','C',2);
    INSERT INTO LeaderQuotes VALUES ('LEADER_T_ROOSEVELT','QUOTE','AUDIO');
    """)
    for kind in KINDS:
        db.execute(f'INSERT INTO Named{kind}Civilizations VALUES (?,?)', ('PLACE_' + kind, 'CIVILIZATION_AMERICA'))
    db.executescript((MOD / 'Data/Identity.sql').read_text())
    return db, tables


class Identity(unittest.TestCase):
    def setUp(self):
        self.db, self.tables = schema_db()
        self.addCleanup(self.db.close)
        self.before = {t: self.db.execute(f'SELECT * FROM {t}').fetchall() for t in self.tables}
        self.db.executescript((MOD / 'Data/TestAmerica.sql').read_text())

    def test_neutral_traits_and_inheritance_without_touching_original_or_legacy(self):
        self.assertEqual(self.db.execute('SELECT TraitType FROM CivilizationTraits WHERE CivilizationType=?', (CIV,)).fetchall(), [('TRAIT_CIVILIZATION_SPC_TEST',)])
        self.assertEqual(self.db.execute('SELECT * FROM LeaderTraits WHERE LeaderType=?', (LEADER,)).fetchall(), [])
        self.assertEqual(self.db.execute('SELECT InheritFrom FROM Leaders WHERE LeaderType=?', (LEADER,)).fetchone(), ('LEADER_DEFAULT',))
        for table, old_rows in self.before.items():
            after = [r for r in self.db.execute(f'SELECT * FROM {table}') if CIV not in r and LEADER not in r]
            self.assertEqual(after, old_rows, table)

    def test_full_city_citizen_and_geographic_pools(self):
        for table, columns in [('CityNames', 'CityName,SortIndex'), ('CivilizationCitizenNames', 'CitizenName,Female,Modern'), ('CivilizationInfo', 'Header,Caption,SortIndex')]:
            original = self.db.execute(f'SELECT {columns} FROM {table} WHERE CivilizationType=? ORDER BY 1', ('CIVILIZATION_AMERICA',)).fetchall()
            self.assertTrue(original)
            self.assertEqual(self.db.execute(f'SELECT {columns} FROM {table} WHERE CivilizationType=? ORDER BY 1', (CIV,)).fetchall(), original)
        for kind in KINDS:
            self.assertEqual(self.db.execute(f'SELECT Named{kind}Type FROM Named{kind}Civilizations WHERE CivilizationType=?', (CIV,)).fetchall(), [('PLACE_' + kind,)])
        self.assertEqual(self.db.execute('SELECT CapitalName FROM CivilizationLeaders WHERE CivilizationType=?', (CIV,)).fetchone(), ('LOC_CITY_NAME_WASHINGTON',))

    def test_loading_presentation_and_neutral_biography(self):
        self.assertEqual(self.db.execute('SELECT ForegroundImage,BackgroundImage,LeaderText,PlayDawnOfManAudio,DawnOfManLeaderId FROM LoadingInfo WHERE LeaderType=?', (LEADER,)).fetchone(), ('LEADER_T_ROOSEVELT_NEUTRAL', 'LEADER_T_ROOSEVELT_BACKGROUND', 'LOC_LOADING_INFO_LEADER_T_ROOSEVELT', 1, 'LEADER_T_ROOSEVELT'))
        self.assertEqual(self.db.execute('SELECT Quote,QuoteAudio FROM LeaderQuotes WHERE LeaderType=?', (LEADER,)).fetchall(), [('QUOTE','AUDIO')])

    def test_frontend_only_new_shell_and_no_original_unique_items(self):
        db = sqlite3.connect(':memory:'); self.addCleanup(db.close)
        fields = 'Domain CivilizationType LeaderType CivilizationName CivilizationIcon LeaderName LeaderIcon CivilizationAbilityName CivilizationAbilityDescription CivilizationAbilityIcon LeaderAbilityName LeaderAbilityDescription LeaderAbilityIcon Portrait PortraitBackground'.split()
        db.execute('CREATE TABLE Players(' + ','.join(f + ' TEXT' for f in fields) + ')')
        db.executescript((MOD / 'Config/Players.sql').read_text())
        self.assertEqual(db.execute('SELECT count(*) FROM Players').fetchone()[0], 0)
        db.executescript((MOD / 'Config/TestAmerica.sql').read_text())
        self.assertEqual(db.execute('SELECT Domain,CivilizationType,LeaderType,Portrait,PortraitBackground FROM Players').fetchall(), [('Players:Expansion2_Players', CIV, LEADER, 'LEADER_T_ROOSEVELT_NEUTRAL', 'LEADER_T_ROOSEVELT_BACKGROUND')])
        # No PlayerItems table is even supplied: any accidental unique-item copy fails.

    def test_chinese_copy_and_history_alias_do_not_copy_native_strategy(self):
        db = sqlite3.connect(':memory:'); self.addCleanup(db.close)
        db.execute('CREATE TABLE LocalizedText(Language TEXT,Tag TEXT,Text TEXT,PRIMARY KEY(Language,Tag))')
        for family, identity in [('LEADERS','LEADER_T_ROOSEVELT'), ('CIVILIZATIONS','CIVILIZATION_AMERICA')]:
            for chapter in ('HISTORY_PARA_1','DETAILED_BODY'):
                db.execute('INSERT INTO LocalizedText VALUES (?,?,?)', ('zh_Hans_CN',f'LOC_PEDIA_{family}_PAGE_{identity}_CHAPTER_{chapter}', '原历史' if chapter.startswith('HISTORY') else '原特色能力说明'))
        db.executescript((MOD / 'Text/TestAmerica.sql').read_text())
        for lang in ('zh_Hans_CN','en_US'):
            self.assertEqual(db.execute('SELECT Text FROM LocalizedText WHERE Language=? AND Tag=?', (lang,'LOC_SPC_AMERICA_NAME')).fetchone(), ('美国（专业测试）',))
            self.assertEqual(db.execute('SELECT Text FROM LocalizedText WHERE Language=? AND Tag=?', (lang,'LOC_PEDIA_LEADERS_PAGE_LEADER_SPC_T_ROOSEVELT_CHAPTER_HISTORY_PARA_1')).fetchone(), ('原历史',))
        inherited_bad = db.execute("SELECT Tag FROM LocalizedText WHERE Tag LIKE '%SPC%' AND Text='原特色能力说明'").fetchall()
        self.assertEqual(inherited_bad, [])

    def test_icon_aliases_leave_originals_and_rough_rider_separate(self):
        db = sqlite3.connect(':memory:'); self.addCleanup(db.close)
        db.execute('CREATE TABLE IconDefinitions(Name TEXT PRIMARY KEY,Atlas TEXT,"Index" INTEGER)')
        original = [('ICON_CIVILIZATION_AMERICA','CIV',3),('ICON_LEADER_T_ROOSEVELT','LEADER',18),('ICON_LEADER_T_ROOSEVELT_PORTRAIT','PORTRAIT',0),('ICON_LEADER_T_ROOSEVELT_ROUGHRIDER','RR',5)]
        db.executemany('INSERT INTO IconDefinitions VALUES (?,?,?)', original)
        db.executescript((MOD / 'Data/TestAmericaIcons.sql').read_text())
        self.assertEqual(db.execute('SELECT Atlas,"Index" FROM IconDefinitions WHERE Name=?', ('ICON_' + LEADER,)).fetchone(), ('LEADER',18))
        self.assertEqual(db.execute("SELECT count(*) FROM IconDefinitions WHERE Name LIKE '%SPC%ROUGHRIDER%'").fetchone()[0],0)
        for row in original:
            self.assertEqual(db.execute('SELECT * FROM IconDefinitions WHERE Name=?', (row[0],)).fetchone(), row)


class Access(unittest.TestCase):
    def test_exact_pairs_human_and_multiplayer_guards(self):
        lua = LuaRuntime(unpack_returned_tuples=True)
        lua.globals().include = lambda name: lua.execute((MOD / (name + '.lua')).read_text())
        lua.execute((MOD/'Probe.lua').read_text())
        lua.execute('''
        cfg={GetCivilizationTypeName=function()return civ end,GetLeaderTypeName=function()return leader end}
        PlayerConfigurations={[0]=cfg};Players={[0]={IsHuman=function()return human end}}
        GameConfiguration={IsAnyMultiplayer=function()return multi end};human=true;multi=false
        function allowed()local ok=SPCP0.IsTestPlayer(0);return ok end
        ''')
        for civ, leader in [(CIV, LEADER), (OLD, 'LEADER_SPC_TEST')]:
            lua.globals().civ = civ; lua.globals().leader = leader
            self.assertTrue(lua.eval('allowed()'))
            for human in (False,None,1):
                lua.globals().human = human
                self.assertFalse(lua.eval('allowed()'))
            lua.globals().human = True
            for multi in (True,None):
                lua.globals().multi = multi
                self.assertFalse(lua.eval('allowed()'))
            lua.globals().multi = False
        for civ, leader in [(CIV,'LEADER_SPC_TEST'),(OLD,LEADER),('CIVILIZATION_AMERICA','LEADER_T_ROOSEVELT')]:
            lua.globals().civ = civ; lua.globals().leader = leader
            self.assertFalse(lua.eval('allowed()'))

    def test_training_binding_and_citizen_name_confirmation_for_both_identities(self):
        for civ in (CIV, OLD):
            with self.subTest(civ=civ):
                lua = training_fixture(); lua.globals().civilization = civ
                lua.execute('''
                for _,row in ipairs(poolRows)do if row.CivilizationType=='CIVILIZATION_SPC_TEST' then row.CivilizationType=civilization end end
                reserve();born();complete();pulse()
                assert(state().phase=='NAMING' and state().unitID==50 and state().sourceCity==1)
                confirmName('name',50)
                assert(state().phase=='CREATED' and state().expectedName=='LOC_CITIZEN_TEST_A')
                assert(not shared.ExpeditionGate.Training.Available(2))
                local n=storeWrites;confirmName('repeat',50);assert(storeWrites==n)
                ''')


class Package(unittest.TestCase):
    def test_leader_model_fallback_and_civilization_art_use_only_new_identity(self):
        for filename, identity, expected in [('Leaders.artdef',LEADER,'ART_LEADER_THEO'),('FallbackLeaders.artdef',LEADER,'FALLBACK_NEUTRAL_ROOSEVELT'),('Civilizations.artdef',CIV,'America')]:
            root=ET.parse(MOD/'ArtDefs'/filename).getroot()
            entries=root.findall('./m_RootCollections/Element/Element')
            self.assertEqual([e.find('m_Name').get('text') for e in entries],[identity])
            self.assertIn(expected,ET.tostring(root,encoding='unicode'))
            self.assertNotIn('CLEO',ET.tostring(root,encoding='unicode'))
        cultures=ET.parse(MOD/'ArtDefs/Cultures.artdef').getroot()
        entries=cultures.findall('./m_RootCollections/Element/Element')
        self.assertEqual([e.find('m_Name').get('text') for e in entries],['America','AncientWood','European'])
        for e in entries:
            self.assertEqual(e.findtext('m_AppendMergedParameterCollections'),'true')
            self.assertEqual([x.get('text') for x in e.iter('m_ElementName')],[CIV])

    def test_art_registration_and_package_closure(self):
        info=ET.parse(MOD/'SpecializationP0.modinfo').getroot()
        files=[n.text for n in info.findall('./Files/File')]
        self.assertEqual(len(files),len(set(files)))
        for f in files:self.assertTrue((MOD/f).is_file(),f)
        self.assertEqual(info.get('version'),'290')
        self.assertTrue(any(n.get('id').lower()=='113d9459-0a3b-4fcb-a49c-483f40303575' for n in info.findall('./Dependencies/Mod')))
        dep=ET.parse(MOD/'Specialization.dep').getroot()
        systems={e.find('ConsumerName').get('text'):e for e in dep.findall('./SystemDependencies/Element')}
        for system,asset in [('Leaders','Leaders.artdef'),('LeaderFallback','FallbackLeaders.artdef'),('Civilizations','Civilizations.artdef'),('Cultures','Cultures.artdef')]:
            self.assertIn(asset,[x.get('text') for x in systems[system].findall('./ArtDefDependencyPaths/Element')])
            self.assertIn('ArtDefs/'+asset,files)
        self.assertIn('Units',systems)
        for stage in ('FrontEndActions','InGameActions'):
            for kind in ('UpdateDatabase','UpdateIcons','UpdateText','UpdateColors'):
                matches=[n for n in info.findall(f'./{stage}/{kind}') if n.get('id','').startswith('SPC_B263_')]
                self.assertEqual(len(matches),1,(stage,kind))
                self.assertGreater(int(matches[0].findtext('./Properties/LoadOrder')),10001090)


if __name__ == '__main__':
    unittest.main()
