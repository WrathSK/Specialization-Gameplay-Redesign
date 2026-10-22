"""B195 native-art aliases: execute the actual icon SQL against a small icon DB.
Native names/coordinates were checked in Base/Assets/UI/Icons/Icons_Projects.xml,
Icons_Units.xml and Icons_UnitPortraits.xml. This is package evidence, not a render test.
"""
from pathlib import Path
import sqlite3
import unittest
import xml.etree.ElementTree as ET

R = Path(__file__).resolve().parents[1]
# Distinct Builder coordinates ensure an accidental old alias cannot pass as Spy.
SOURCES = [
    ('ICON_UNIT_BUILDER', 'FIXTURE_BUILDER', 1),
    ('ICON_UNIT_BUILDER_PORTRAIT', 'FIXTURE_BUILDER_PORTRAIT', 2),
    ('ICON_UNIT_SPY', 'ICON_ATLAS_UNITS', 17),
    ('ICON_UNIT_SPY_PORTRAIT', 'ICON_ATLAS_UNIT_PORTRAITS', 15),
    ('ICON_PROJECT_ENHANCE_DISTRICT_INDUSTRIAL_ZONE', 'ICON_ATLAS_PROJECTS', 13),
    ('ICON_PROJECT_ENHANCE_DISTRICT_COMMERCIAL_HUB', 'ICON_ATLAS_PROJECTS', 14),
    ('ICON_PROJECT_ENHANCE_DISTRICT_CAMPUS', 'ICON_ATLAS_PROJECTS', 16),
    ('ICON_PROJECT_ENHANCE_DISTRICT_THEATER', 'ICON_ATLAS_PROJECTS', 17),
]


class NativeIconAliases(unittest.TestCase):
    def setUp(self):
        self.db = sqlite3.connect(':memory:')
        self.addCleanup(self.db.close)
        self.db.execute('CREATE TABLE IconDefinitions(Name TEXT PRIMARY KEY, Atlas TEXT, "Index" INTEGER)')
        self.db.executemany('INSERT INTO IconDefinitions VALUES(?,?,?)', SOURCES)
        self.db.executescript((R/'Mod/Data/Icons.sql').read_text())

    def icon(self, name):
        return self.db.execute('SELECT Atlas,"Index" FROM IconDefinitions WHERE Name=?', (name,)).fetchall()

    def test_each_formal_one_turn_project_resolves_to_its_own_district_project_art(self):
        for project, native in (
            ('CLAIM_RESEARCH', 'CAMPUS'), ('CLAIM_CULTURE', 'THEATER'),
            ('CLAIM_INDUSTRY', 'INDUSTRIAL_ZONE'), ('CLAIM_COMMERCE', 'COMMERCIAL_HUB'),
            ('ERA_DIALOGUE', 'THEATER'),
        ):
            with self.subTest(project=project):
                rows = self.icon('ICON_PROJECT_SPC_'+project)
                self.assertEqual(len(rows), 1)
                self.assertEqual(rows, self.icon('ICON_PROJECT_ENHANCE_DISTRICT_'+native))

    def test_current_expedition_spy_uses_spy_art_and_legacy_units_keep_builder(self):
        for suffix in ('', '_PORTRAIT'):
            self.assertEqual(self.icon('ICON_UNIT_SPC_EXPEDITION_SPY'+suffix), self.icon('ICON_UNIT_SPY'+suffix))
            self.assertNotEqual(self.icon('ICON_UNIT_SPC_EXPEDITION_SPY'+suffix), self.icon('ICON_UNIT_BUILDER'+suffix))
            for unit in ('EXPEDITION_GATE', 'EXPEDITION_ZERO', 'CREW_250', 'CREW_420', 'CREW_750', 'CREW_1000', 'CREW_1360'):
                with self.subTest(unit=unit, suffix=suffix):
                    self.assertEqual(self.icon('ICON_UNIT_SPC_'+unit+suffix), self.icon('ICON_UNIT_BUILDER'+suffix))
        for tier in (250, 420, 750, 1000, 1360):
            self.assertEqual(self.icon(f'ICON_PROJECT_SPC_CREW_{tier}'), self.icon('ICON_UNIT_BUILDER'))
        self.assertEqual(self.icon('ICON_PROJECT_SPC_OVERFLOW_SINK_TEST'), [])

    def test_native_icon_definitions_are_unchanged(self):
        for name, atlas, index in SOURCES:
            with self.subTest(name=name):
                self.assertEqual(self.icon(name), [(atlas, index)])

    def test_icon_sql_has_one_existing_registration_per_frontend_and_ingame_context(self):
        modinfo = ET.parse(R/'Mod/SpecializationP0.modinfo').getroot()
        for context in ('FrontEndActions', 'InGameActions'):
            with self.subTest(context=context):
                entries = [node.text for node in modinfo.findall(f'./{context}/UpdateIcons/File')]
                self.assertEqual(entries.count('Data/Icons.sql'), 1)
        self.assertEqual([node.text for node in modinfo.findall('./Files/File')].count('Data/Icons.sql'), 1)


if __name__ == '__main__':
    unittest.main()
