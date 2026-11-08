"""O5a data assembly from pinned native definitions, in memory only.

Set SPC_OFFICIAL_DB, SPC_HD_DB and SPC_OFFICIAL_ASSETS explicitly. Manifest
criteria and ordering are modeled locally. Native selection and effects are
separate gates. Set SPC_LEGACY_SQLITE to the SQLite 3.38.5 CLI to check the
assembly statement against a parser that requires GROUP BY with HAVING.
"""
from contextlib import closing
from hashlib import sha256
import os
from pathlib import Path
import sqlite3
import subprocess
import unittest
from xml.etree import ElementTree as ET
import zlib

MOD = Path(__file__).resolve().parents[1] / 'Mod'
HD_ID = '521b8777-0977-4859-a5ee-3e411a732e5c'
LEUGI_ID = 'b248a322-3e2a-4a6a-830a-6b0d1f3435fc'
DB_SHA256 = {
    'SPC_OFFICIAL_DB': 'a37e505731f433bbaf2507ec4cf1f0867019813d645c8c7943c3ceae1691bb32',
    'SPC_HD_DB': 'd483b5f2848907329b8439dc257c061ea285c4b90a88c22bdb792f0e4ab42439',
}
GENERATORS = (
    'SPC_B054_Discounts', 'SPC_B234_Standardization', 'SPC_B235_EngineeringStudy',
    'SPC_DevelopmentInvestmentEffects', 'SPC_B053_Purchase', 'SPC_ResearchCross',
)
INPUT_ACTIONS = {
    'SPC_EnvironmentSchema', 'SPC_EnvironmentOfficial', 'SPC_EnvironmentHD', 'SPC_EnvironmentBuildings',
}
ASSEMBLY_ACTIONS = {*INPUT_ACTIONS, 'SPC_B246_Development', 'SPC_InternalCarrierPillage', *GENERATORS}
CARRIER_TABLES = (
    'SPC_B054_Targets', 'SPC_StandardizationTargets', 'SPC_StandardizationLevels',
    'SPC_IndustryWonderEffects', 'SPC_DevelopmentEffects',
)
WRAPPER_PAIRS = {
    'MODIFIER_SPC_CITY_ADJUST_BUILDING_PURCHASE_COST': 'MODIFIER_CITY_ADJUST_BUILDING_PURCHASE_COST',
    'MODIFIER_SPC_CITY_DISTRICTS_ADJUST_YIELD_CHANGE': 'MODIFIER_CITY_DISTRICTS_ADJUST_YIELD_CHANGE',
    'MODIFIER_SPC_SINGLE_CITY_ADJUST_DISTRICT_PRODUCTION': 'MODIFIER_SINGLE_CITY_ADJUST_DISTRICT_PRODUCTION',
}
ACCESS_PROJECTS = ('PROJECT_SPC_DEVELOPMENT_INVESTMENT', 'PROJECT_SPC_ENGINEERING_STUDY')


def manifest():
    return ET.parse(MOD / 'SpecializationP0.modinfo').getroot()


def snapshot(variable):
    path = Path(os.environ[variable]).resolve(strict=True)
    if sha256(path.read_bytes()).hexdigest() != DB_SHA256[variable]:
        raise ValueError(f'{variable} does not match the fixed native snapshot')
    db = sqlite3.connect(':memory:')
    db.create_function('Make_Hash', 1, lambda value: zlib.crc32(value.encode()))
    with closing(sqlite3.connect(path.as_uri() + '?mode=ro&immutable=1', uri=True)) as source:
        source.backup(db)
    return db


def execute_data(db, name):
    db.executescript((MOD / 'Data' / name).read_text(encoding='utf-8'))


def matches_profile(action, criteria, hd):
    name = action.get('criteria')
    if name is None:
        return True
    condition = criteria[name]
    mod = condition.find('ModInUse')
    if ([child.tag for child in condition] != ['RuleSetInUse', 'ModInUse']
            or condition.findtext('RuleSetInUse') != 'RULESET_EXPANSION_2'
            or mod.text.lower() != HD_ID or mod.get('inverse') not in (None, '1')):
        raise AssertionError(f'Unmodeled assembly criterion {name}')
    return hd != (mod.get('inverse') == '1')


def replay(db, hd, selected=None):
    root = manifest()
    criteria = {entry.get('id'): entry for entry in root.findall('./ActionCriteria/Criteria')}
    actions = root.findall('./InGameActions/UpdateDatabase')
    actions.sort(key=lambda entry: int(entry.findtext('Properties/LoadOrder', '0')))
    files = []
    for action in actions:
        if selected is not None and action.get('id') not in selected:
            continue
        if not matches_profile(action, criteria, hd):
            continue
        for file in action.findall('File'):
            if file.attrib:
                raise AssertionError('Replay requires explicit handling of file priority')
            try:
                db.executescript((MOD / file.text).read_text(encoding='utf-8'))
            except sqlite3.Error as error:
                raise AssertionError(f'{action.get("id")}: {file.text}: {error}') from error
            files.append(file.text)
    return files


def prepare_hd_inputs(db):
    # Retained consumer tests accept a native fixture from before O5a.
    if not db.execute("SELECT 1 FROM sqlite_master WHERE name='SPC_EnvironmentAssembly'").fetchone():
        replay(db, hd=True, selected=INPUT_ACTIONS)


def rows(db, sql, parameters=()):
    return set(db.execute(sql, parameters))


def scoped_outputs(db):
    tables = {name: rows(db, f'SELECT * FROM {name}') for name in CARRIER_TABLES}
    carriers = set().union(*(rows(db, f'SELECT CarrierType FROM {name}') for name in CARRIER_TABLES))
    carriers |= rows(db, """
        SELECT BuildingType FROM BuildingModifiers JOIN Modifiers USING (ModifierId)
        WHERE SubjectRequirementSetId='SPC_CROSS_CAMPUS'
    """)
    carriers |= {(name,) for name in (
        'BUILDING_SPC_B053_FIXTURE', 'BUILDING_SPC_B053_DISCOUNT',
        'BUILDING_SPC_DEVELOPMENT_ACCESS', 'BUILDING_SPC_ENGINEERING_STUDY_ACCESS',
    )}
    building_ids = tuple(sorted(name for (name,) in carriers))
    placeholders = ','.join('?' for _ in building_ids)
    attachments = rows(db, f'SELECT * FROM BuildingModifiers WHERE BuildingType IN ({placeholders})', building_ids)
    modifier_ids = tuple(sorted({modifier for _, modifier in attachments}))
    mod_params = ','.join('?' for _ in modifier_ids)
    return {
        'tables': tables, 'building_ids': building_ids, 'modifier_ids': modifier_ids,
        'buildings': rows(db, f'SELECT * FROM Buildings WHERE BuildingType IN ({placeholders})', building_ids),
        'attachments': attachments,
        'modifiers': rows(db, f'SELECT ModifierId,ModifierType,SubjectRequirementSetId FROM Modifiers WHERE ModifierId IN ({mod_params})', modifier_ids),
        'arguments': rows(db, f'SELECT * FROM ModifierArguments WHERE ModifierId IN ({mod_params})', modifier_ids),
        'projects': rows(db, 'SELECT * FROM Projects WHERE ProjectType IN (?,?)', ACCESS_PROJECTS),
    }


def strip_replayed_outputs(db, outputs):
    # Remove only the owned definitions in the replay closure, in memory.
    # Foreign-key cascades remove their attachment, argument and XP2 rows.
    db.execute('PRAGMA foreign_keys=ON')
    for table in CARRIER_TABLES:
        db.execute(f'DROP TABLE {table}')
    db.executemany('DELETE FROM Modifiers WHERE ModifierId=?', ((key,) for key in outputs['modifier_ids']))
    types = (*outputs['building_ids'], *ACCESS_PROJECTS, 'MODIFIER_SPC_CITY_WONDER_ERA_PRODUCTION')
    db.executemany('DELETE FROM Types WHERE Type=?', ((key,) for key in types))
    db.execute("""DELETE FROM Requirements WHERE RequirementId IN (
        SELECT RequirementId FROM RequirementSetRequirements WHERE RequirementSetId='SPC_CROSS_CAMPUS'
    )""")
    db.execute("DELETE FROM RequirementSets WHERE RequirementSetId='SPC_CROSS_CAMPUS'")
    db.commit()


class Assembly(unittest.TestCase):
    @unittest.skipUnless(os.environ.get('SPC_LEGACY_SQLITE'), 'Set SPC_LEGACY_SQLITE for the legacy parser check')
    def test_legacy_parser_preserves_assembly_guard(self):
        fixture = """
            PRAGMA foreign_keys=ON;
            SELECT sqlite_version();
            CREATE TABLE Districts(DistrictType TEXT PRIMARY KEY,InternalOnly INTEGER);
            CREATE TABLE Buildings(BuildingType TEXT PRIMARY KEY,PrereqDistrict TEXT,InternalOnly INTEGER,IsWonder INTEGER);
            CREATE TABLE HD_DUMMY_BUILDINGS(BuildingType TEXT PRIMARY KEY);
            INSERT INTO Districts VALUES ('DISTRICT_CAMPUS',0);
        """
        cases = (
            (('Official',), False, 'OFFICIAL'), (('HD',), False, 'HD'),
            ((), False, None), (('Official', 'HD'), False, None), (('Official',), True, None),
        )
        for profiles, empty_inventory, expected in cases:
            with self.subTest(profiles=profiles, empty_inventory=empty_inventory):
                scripts = ['EnvironmentSchema', *(f'Environment{profile}' for profile in profiles), 'EnvironmentBuildings']
                building = "" if empty_inventory else "INSERT INTO Buildings VALUES ('BUILDING_LIBRARY','DISTRICT_CAMPUS',0,0);"
                sql = '\n'.join((fixture, building, *((MOD / f'Data/{name}.sql').read_text(encoding='utf-8') for name in scripts),
                                 'SELECT Id,Profile,SchemaVersion FROM SPC_EnvironmentAssembly;'))
                run = subprocess.run([os.environ['SPC_LEGACY_SQLITE'], '-init', os.devnull, '-batch', ':memory:'],
                                     input=sql, capture_output=True, text=True, timeout=10)
                lines = run.stdout.splitlines()
                self.assertEqual(lines[:1], ['3.38.5'], run.stderr)
                if expected:
                    self.assertEqual(run.returncode, 0, run.stderr)
                    self.assertEqual(lines[1:], [f'1|{expected}|1'])
                else:
                    self.assertNotEqual(run.returncode, 0)
                    self.assertIn('NOT NULL constraint failed: SPC_EnvironmentAssembly.Profile', run.stderr)
                    self.assertEqual(lines[1:], [])

    def check_integrity(self, db, profile):
        self.assertEqual(rows(db, 'SELECT * FROM SPC_EnvironmentAssembly'), {(1, profile, 1)})
        self.assertEqual(rows(db, 'PRAGMA foreign_key_check'), set())
        self.assertEqual(rows(db, """
            SELECT ModifierId FROM Modifiers m LEFT JOIN DynamicModifiers d USING (ModifierType)
            WHERE d.ModifierType IS NULL
        """), set())
        self.assertEqual(rows(db, """
            SELECT BuildingType FROM Buildings b LEFT JOIN Buildings_XP2 x USING (BuildingType)
            WHERE b.InternalOnly=1 AND b.BuildingType GLOB 'BUILDING_SPC_*'
            AND (x.Pillage IS NULL OR x.Pillage<>0)
        """), set())

    def test_official_selected_full_gameplay_sql_without_hd(self):
        with closing(snapshot('SPC_OFFICIAL_DB')) as db:
            files = replay(db, hd=False)
            self.assertIn('Data/EnvironmentOfficial.sql', files)
            self.assertNotIn('Data/EnvironmentHD.sql', files)
            self.assertEqual(rows(db, "SELECT name FROM sqlite_master WHERE name IN ('HD_BuildingTiers','HD_DUMMY_BUILDINGS')"), set())
            self.check_integrity(db, 'OFFICIAL')
            self.assertEqual(rows(db, 'SELECT BuildingType FROM SPC_EnvironmentBuildings WHERE TierOverride IS NOT NULL'), set())
            self.assertEqual(rows(db, """
                SELECT DistrictType FROM SPC_EnvironmentBuildings WHERE BuildingType='BUILDING_SEWER'
            """), {('DISTRICT_CITY_CENTER',)})
            for table, count in zip(CARRIER_TABLES, (256, 95, 855, 27, 16)):
                self.assertEqual(db.execute(f'SELECT COUNT(*) FROM {table}').fetchone()[0], count, table)
            self.assertEqual(files[-1], 'Data/InternalCarrierPillage.sql')
            self.assertEqual(db.execute('SELECT COUNT(*) FROM SPC_EnvironmentBuildings').fetchone()[0], 82)

    def test_hd_reconstructed_slice_preserves_exact_loaded_outputs(self):
        with closing(snapshot('SPC_HD_DB')) as db:
            expected = scoped_outputs(db)
            existing_tiers = rows(db, 'SELECT BuildingType,PrereqDistrict FROM HD_BuildingTiers')
            wrappers = rows(db, """
                SELECT ModifierType,CollectionType,EffectType FROM DynamicModifiers
                WHERE ModifierType IN (?,?,?)
            """, tuple(WRAPPER_PAIRS.values()))
            strip_replayed_outputs(db, expected)
            # The old Tier table is comparison evidence only for the SQL slice.
            db.execute('DROP TABLE HD_BuildingTiers')
            files = replay(db, hd=True, selected=ASSEMBLY_ACTIONS)
            self.assertIn('Data/EnvironmentHD.sql', files)
            self.assertNotIn('Data/EnvironmentOfficial.sql', files)
            self.check_integrity(db, 'HD')
            self.assertEqual(rows(db, 'SELECT BuildingType,DistrictType FROM SPC_EnvironmentBuildings'), existing_tiers)
            self.assertEqual(rows(db, 'SELECT BuildingType,TierOverride FROM SPC_EnvironmentBuildings WHERE TierOverride IS NOT NULL'), {
                ('BUILDING_JNR_HOSPITIUM', 4), ('BUILDING_JNR_GARDEN', 4),
            })
            self.assertEqual(rows(db, """
                SELECT BuildingType FROM SPC_EnvironmentExcludedBuildings WHERE BuildingType='BUILDING_JNR_MILL_RACE'
            """), {('BUILDING_JNR_MILL_RACE',)})
            actual = scoped_outputs(db)
            for new, old in WRAPPER_PAIRS.items():
                _, collection, effect = next(row for row in wrappers if row[0] == old)
                self.assertEqual(rows(db, 'SELECT CollectionType,EffectType FROM DynamicModifiers WHERE ModifierType=?', (new,)), {(collection, effect)})
            actual['modifiers'] = {(key, WRAPPER_PAIRS.get(kind, kind), subject) for key, kind, subject in actual['modifiers']}
            for part in expected:
                self.assertEqual(actual[part], expected[part], part)

    def test_invalid_selection_or_empty_inventory_blocks_target_generation(self):
        for profile_count, empty_inventory in ((0, False), (2, False), (1, True)):
            with self.subTest(profiles=profile_count, empty_inventory=empty_inventory), closing(snapshot('SPC_OFFICIAL_DB')) as db:
                execute_data(db, 'EnvironmentSchema.sql')
                execute_data(db, 'EnvironmentModifiers.sql')
                if profile_count:
                    execute_data(db, 'EnvironmentOfficial.sql')
                if profile_count == 2:
                    db.execute('CREATE TABLE HD_DUMMY_BUILDINGS(BuildingType TEXT PRIMARY KEY)')
                    execute_data(db, 'EnvironmentHD.sql')
                if empty_inventory:
                    db.execute('INSERT INTO SPC_EnvironmentExcludedBuildings SELECT BuildingType FROM Buildings')
                with self.assertRaisesRegex(sqlite3.IntegrityError, r'SPC_EnvironmentAssembly\.Profile'):
                    execute_data(db, 'EnvironmentBuildings.sql')
                self.assertEqual(rows(db, 'SELECT * FROM SPC_EnvironmentAssembly'), set())
                self.assertEqual(rows(db, 'SELECT * FROM SPC_EnvironmentBuildings'), set())
                # Simulate the later actions still running after the selector error.
                replay(db, hd=False, selected={'SPC_B246_Development', *GENERATORS})
                for table in CARRIER_TABLES:
                    if table != 'SPC_IndustryWonderEffects':
                        self.assertEqual(rows(db, f'SELECT * FROM {table}'), set(), table)
                self.assertEqual(rows(db, "SELECT RequiredBuilding FROM Projects WHERE ProjectType='PROJECT_SPC_DEVELOPMENT_INVESTMENT'"), {
                    ('BUILDING_SPC_DEVELOPMENT_ACCESS',),
                })


class UIBaseSelection(unittest.TestCase):
    def test_profile_replacements_keep_order_and_use_selected_bases(self):
        root = manifest()
        criteria = {entry.get('id'): entry for entry in root.findall('./ActionCriteria/Criteria')}
        hd_overrides = {
            'ProductionPanel': ('UI/CrewProjectOrder.lua', 150100),
            'UnitPanel': ('UI/SPCUnitPanelHD.lua', 2000006),
            'CityPanel': ('UI/SPCCityPanelHD.lua', 2000005),
            'CityPanelOverview': ('UI/SPCCityOverviewHD.lua', 2000003),
            'ActionPanel': ('UI/TimedTurnProbe.lua', 2000004),
        }
        shared = {
            'EspionageChooser': ('UI/ExpeditionSpyChooser.lua', 2000006),
            'EspionagePopup': ('UI/ExpeditionSpyPopup.lua', 2000006),
        }
        official_overrides = {
            'UnitPanel': ('UI/SPCUnitPanelOfficial.lua', 2000006),
            'ProductionPanel': ('UI/SPCProductionPanelOfficial.lua', 150100),
            'CityPanel': ('UI/SPCCityPanelOfficial.lua', 2000005),
            'CityPanelOverview': ('UI/SPCCityOverviewOfficial.lua', 2000003),
        }
        for hd, expected in ((False, official_overrides | shared), (True, hd_overrides | shared)):
            with self.subTest(hd=hd):
                active = {}
                for action in root.findall('./InGameActions/ReplaceUIScript'):
                    if not matches_profile(action, criteria, hd):
                        continue
                    context = action.findtext('Properties/LuaContext')
                    self.assertNotIn(context, active)
                    active[context] = (action.findtext('Properties/LuaReplace'), int(action.findtext('Properties/LoadOrder')))
                self.assertEqual(active, expected)

        assets = Path(os.environ['SPC_OFFICIAL_ASSETS'])
        base = assets / 'Base/Assets/UI'
        ingame = ET.parse(base / 'InGame.xml')
        production = ingame.find(".//LuaContext[@ID='ProductionPanel']")
        self.assertEqual(production.get('FileName'), 'ProductionPanel')
        self.assertTrue((base / 'Panels/ProductionPanel.lua').is_file())
        expansion = assets / 'DLC/Expansion2'
        xp2 = ET.parse(expansion / 'Expansion2.modinfo')
        replacements = {
            action.findtext('Properties/LuaContext'): action.findtext('Properties/LuaReplace')
            for action in xp2.findall('./InGameActions/ReplaceUIScript') if action.get('criteria') == 'Expansion2'
        }
        for context in hd_overrides.keys() - {'ProductionPanel'}:
            expected = f'UI/Replacements/{context}_Expansion2.lua'
            self.assertEqual(replacements.get(context), expected)
            self.assertTrue((expansion / expected).is_file())


class RestructuringArt(unittest.TestCase):
    def test_model_audio_dependencies_and_icons_resolve_to_shipped_content(self):
        base = Path(os.environ['SPC_OFFICIAL_ASSETS']) / 'Base'
        original = ET.parse(base / 'ArtDefs/Units.artdef')
        source = ET.parse(MOD / 'ArtDefs/Units.artdef')
        def unit(tree, name):
            return next(element for element in tree.iter('Element') if element.findtext('m_Name') == name
                        or element.find('m_Name[@text="' + name + '"]') is not None)
        official = unit(original, 'UNIT_GREAT_MERCHANT_MALE_MODERN')
        team = unit(source, 'UNIT_SPC_RESTRUCTURING_TEAM')
        for tag, value in (('m_ElementName', 'Great_Merchant_Male_Modern'), ('m_Value', 'GreatMerchantModern')):
            for node in (official, team):
                self.assertIsNotNone(node.find(f'.//{tag}[@text="{value}"]'))
        self.assertNotIn(LEUGI_ID, {node.get('id').lower() for node in manifest().findall('./Dependencies/Mod')})
        dep = ET.parse(MOD / 'Specialization.dep')
        self.assertNotIn(LEUGI_ID, {node.get('text').lower() for node in dep.findall('./RequiredGameArtIDs/Element/id')})
        with closing(sqlite3.connect(':memory:')) as db:
            db.executescript('''
                CREATE TABLE IconDefinitions(Name TEXT PRIMARY KEY,Atlas TEXT,"Index" INTEGER);
                CREATE TABLE IconTextureAtlases(Name TEXT,IconSize INTEGER,IconsPerRow INTEGER,
                 IconsPerColumn INTEGER,Filename TEXT,PRIMARY KEY(Name,IconSize));
            ''')
            icons = base / 'Assets/UI/Icons'
            for name in ('Icons_Units.xml', 'Icons_UnitFlags.xml', 'Icons_UnitPortraits.xml'):
                db.executemany('INSERT INTO IconDefinitions VALUES (?,?,?)', (
                    (node.get('Name'), node.get('Atlas'), int(node.get('Index')))
                    for node in ET.parse(icons / name).iter('Row')
                    if node.get('Name', '').startswith('ICON_UNIT_GREAT_MERCHANT') and node.get('Atlas')
                ))
            execute_data(db, 'Icons.sql')
            suffixes = ('', '_PORTRAIT', '_PORTRAIT_ERA_MODERN', '_WHITE', '_BLACK', '_FOW')
            for suffix in suffixes:
                native = rows(db, 'SELECT Atlas,"Index" FROM IconDefinitions WHERE Name=?', ('ICON_UNIT_GREAT_MERCHANT' + suffix,))
                self.assertEqual(len(native), 1)
                self.assertEqual(rows(db, 'SELECT Atlas,"Index" FROM IconDefinitions WHERE Name=?', ('ICON_UNIT_SPC_RESTRUCTURING_TEAM' + suffix,)), native)
            execute_data(db, 'RawIcons.sql')
            for suffix in suffixes:
                self.assertEqual(rows(db, 'SELECT Atlas,"Index" FROM IconDefinitions WHERE Name=?', ('ICON_UNIT_SPC_RESTRUCTURING_TEAM' + suffix,)),
                                 {('ICON_ATLAS_SPC_RAW', 1)})


if __name__ == '__main__':
    unittest.main()
