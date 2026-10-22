"""B189 citizen-name data only; native automatic assignment/travel remain user-game gates.
The configured external DB is opened read-only and copied in memory. No runtime writes.
"""
from pathlib import Path
from contextlib import closing
import re
import sqlite3
import unittest
import zlib
from project_paths import external_database

R = Path(__file__).resolve().parents[1]
DESTINATION = 'CIVILIZATION_SPC_TEST'
SOURCE = 'CIVILIZATION_SCOTLAND'
IDENTITY_SQL = (R / 'Mod/Data/Identity.sql').read_text()
POOL_SQL = re.search(
    r'INSERT OR IGNORE INTO CivilizationCitizenNames\b[^;]+;',
    IDENTITY_SQL,
).group(0)


class NamePool(unittest.TestCase):
    def setUp(self):
        path = external_database(R)
        with closing(sqlite3.connect(path.as_uri() + '?mode=ro', uri=True)) as source:
            self.db = sqlite3.connect(':memory:')
            source.backup(self.db)
        self.addCleanup(self.db.close)
        self.db.create_function('Make_Hash', 1, lambda s: zlib.crc32(s.encode()))
        self.db.execute('DELETE FROM CivilizationCitizenNames WHERE CivilizationType=?',
                        (DESTINATION,))
        self.assertGreater(len(self.pool(SOURCE)), 0, 'Configured DB must contain the source name pool')

    def pool(self, civilization):
        return self.db.execute(
            'SELECT CitizenName,Female,Modern FROM CivilizationCitizenNames '
            'WHERE CivilizationType=? ORDER BY CitizenName', (civilization,)
        ).fetchall()

    def unrelated(self):
        return self.db.execute(
            'SELECT * FROM CivilizationCitizenNames WHERE CivilizationType<>? '
            'ORDER BY CivilizationType,CitizenName', (DESTINATION,)
        ).fetchall()

    def test_full_identity_initialization_copies_complete_source_metadata(self):
        # Reset only the independently defined identity in this disposable DB copy.
        # This exercises composition with the real file, not a second hand-written insert.
        before = self.unrelated()
        expected = self.pool(SOURCE)
        for table, column, value in [
            ('Types', 'Type', DESTINATION),
            ('Types', 'Type', 'LEADER_SPC_TEST'),
            ('Types', 'Type', 'TRAIT_CIVILIZATION_SPC_TEST'),
            ('Civilizations', 'CivilizationType', DESTINATION),
            ('Leaders', 'LeaderType', 'LEADER_SPC_TEST'),
            ('CivilizationLeaders', 'CivilizationType', DESTINATION),
            ('CityNames', 'CivilizationType', DESTINATION),
            ('Traits', 'TraitType', 'TRAIT_CIVILIZATION_SPC_TEST'),
            ('CivilizationTraits', 'CivilizationType', DESTINATION),
            ('LoadingInfo', 'LeaderType', 'LEADER_SPC_TEST'),
            ('DiplomacyInfo', 'Type', 'LEADER_SPC_TEST'),
        ]:
            self.db.execute(f'DELETE FROM {table} WHERE {column}=?', (value,))
        self.db.executescript(IDENTITY_SQL)
        self.assertEqual(self.pool(DESTINATION), expected)
        self.assertEqual(self.unrelated(), before)
        self.assertTrue(any(row[1] == 1 for row in expected))
        self.assertTrue(any(row[2] == 1 for row in expected))

    def test_pool_addition_is_idempotent_and_does_not_touch_spy_or_global_rules(self):
        tables = ['Units', 'GlobalParameters', 'Modifiers', 'ModifierArguments']
        before = {t: self.db.execute(f'SELECT * FROM {t} ORDER BY 1').fetchall() for t in tables}
        unrelated = self.unrelated()
        self.db.executescript(POOL_SQL)
        once = self.pool(DESTINATION)
        self.db.executescript(POOL_SQL)
        self.assertEqual(self.pool(DESTINATION), once)
        self.assertEqual(once, self.pool(SOURCE))
        self.assertEqual(self.unrelated(), unrelated)
        for table in tables:
            self.assertEqual(self.db.execute(f'SELECT * FROM {table} ORDER BY 1').fetchall(),
                             before[table], table)

    def test_absent_source_stays_empty_without_another_civilization_fallback(self):
        self.db.execute('DELETE FROM CivilizationCitizenNames WHERE CivilizationType=?', (SOURCE,))
        before = self.unrelated()
        self.assertGreater(len(self.pool('CIVILIZATION_ENGLAND')), 0)
        self.db.executescript(POOL_SQL)
        self.assertEqual(self.pool(DESTINATION), [])
        self.assertEqual(self.unrelated(), before)
        # Data cannot synthesize a usable name. The runtime gate must reject this state.

    def test_existing_destination_name_is_retained_without_overwrite(self):
        name, female, modern = self.pool(SOURCE)[0]
        retained = (name, 1 - female, 1 - modern)
        self.db.execute('INSERT INTO CivilizationCitizenNames (CivilizationType,CitizenName,Female,Modern) VALUES (?,?,?,?)',
                        (DESTINATION, *retained))
        self.db.executescript(POOL_SQL)
        actual = dict((n, (f, m)) for n, f, m in self.pool(DESTINATION))
        self.assertEqual(actual[name], retained[1:])
        self.assertEqual(set(actual), {row[0] for row in self.pool(SOURCE)})


if __name__ == '__main__':
    unittest.main()
