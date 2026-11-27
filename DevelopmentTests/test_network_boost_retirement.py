"""Retire only the old research/culture boost experiment. Native inputs are read-only."""
from contextlib import closing
from unittest import TestCase, mock

import test_environment_assembly as assembly
from refactor_harness import Context, ROOT, measure
from retired_crew_sources import B533, boost_history, package
from test_o7_crew_retirement import verify_package_round_trip, verify_stable_round_trip
from test_o7_legacy_panel_cleanup import fixture
from test_refactor_s8c5b import core_fixture

REMOVED = ('BoostIntegerConfig.lua', 'Data/BoostIntegerTest.sql',
           'Data/NetworkBoost.sql', 'Data/NetworkBoostInteger.sql')
# Child tables first so removal also works with immediate foreign keys.
TABLES = (
    ('BuildingModifiers', 'BuildingType', 1126),
    ('ModifierArguments', 'ModifierId', 3378),
    ('Buildings_XP2', 'BuildingType', 1126),
    ('Modifiers', 'ModifierId', 2252),
    ('Buildings', 'BuildingType', 1126),
    ('Types', 'Type', 1126),
)


def exact_ids():
    ids = set()
    for kind in ('RESEARCH', 'CULTURE'):
        for level in range(1, 5):
            ids.update(f'BUILDING_SPC_B055_{kind}_{level}_{n}' for n in range(1, 130))
        ids.update(f'BUILDING_SPC_B057_{kind}_{n}' for n in (2, 4))
        ids.update(f'BUILDING_SPC_B058_{kind}_{n}' for n in range(1, 46))
    modifiers = {name.removeprefix('BUILDING_') for name in ids}
    modifiers |= {name + '_HD' for name in modifiers}
    return ids, modifiers


def key_table(db):
    buildings, modifiers = exact_ids()
    db.execute('CREATE TEMP TABLE retired(id TEXT PRIMARY KEY)')
    db.executemany('INSERT INTO retired VALUES (?)', ((i,) for i in buildings | modifiers))


class Retirement(TestCase):
    def test_work_cleanup_keeps_its_two_lifecycle_signals(self):
        for first_event in ('LoadScreenClose', 'PlayerTurnActivated'):
            with self.subTest(first_event=first_event):
                ctx = fixture(ROOT, None)
                ctx.execute("""
                  local cleanup=ExposedMembers.SPC_P0.GreatWorkLoadCleanup
                  local close,turn=Events.LoadScreenClose,Events.PlayerTurnActivated
                  close.Order({workClose});turn.Order({workTurn})
                  local nativeReads,boostReads=0,0
                  local has=SPCP0.HasBuilding
                  SPCP0.HasBuilding=function(b,id)
                    nativeReads=nativeReads+1
                    if id==boostID then boostReads=boostReads+1 end
                    if nativeReads==1 then close.Fire() end
                    return has(b,id)
                  end
                  turn.Fire(1)
                  Game.GetLocalPlayer=function()return -1 end
                  close.Fire();turn.Fire(0)
                  assert(nativeReads==0 and not cleanup.ready and #changes==0)
                  Game.GetLocalPlayer=function()return 0 end
                  Events[...].Fire(0)
                  assert(not cleanup.ready and #changes==1 and localPresent[objectWorkID])
                  local stalled=nativeReads
                  turn.Fire(1);assert(nativeReads==stalled)
                  rejectObject=false;turn.Fire(0)
                  assert(cleanup.ready and #changes==2 and changes[1][3]=='BUILDING_SPC_B055_GW_CITY'
                         and changes[2][3]=='BUILDING_SPC_B055_GW_OBJECT')
                  local done=nativeReads
                  close.Fire();turn.Fire(0);assert(nativeReads==done and boostReads==0)
                  assert(localPresent[boostID] and localPresent[monumentID] and foreignPresent[monumentID])
                  assert(propertyWrites==0 and #changes==2)
                """, first_event)
                self.assertEqual(ctx.load_counts['missing'] + ctx.load_counts['failed'], 0)
        measure('retired_boost_startup', {'boost_building_reads': 0, 'removed_work_buildings': 2,
                                         'retry': 'supported turn after failed readback'})

    def test_confirmed_exit_waits_for_the_remaining_work(self):
        ctx = core_fixture("faultGroup='GreatWorkProbe'")
        ctx.execute("""
          assert(#groups==10 and byGroup.NetworkBoost==nil and byGroup.GreatWorkProbe)
          local count=0;for _ in pairs(byID)do count=count+1 end;assert(count==283)
          lose(ca,900)
          assert(status()=='PARTIAL_HELD' and removeCalls==281 and countPresent(ca,'GreatWorkProbe')==2)
          faultGroup=nil;s.ExitConfirmed()
          assert(status()=='WITHDRAWN' and removeCalls==283 and plotWrites==2 and postCalls==1)
          assert(ca.present[999999] and cb.present[999999])
          for id in pairs(byID)do assert(not ca.present[id] and cb.present[id])end
          s.ExitConfirmed();assert(removeCalls==283)
        """)

    def test_absent_boost_reads_before_and_after(self):
        for previous in (True, False):
            ctx = Context()
            loader = boost_history(ctx) if previous else ctx.load
            loader('LegacyCleanup')
            ctx.execute("""
              local before=...
              lookups,reads,removes={}, {},0
              P={Field=function(t,k)return t[k]end,Count=function()end,IsTestPlayer=function(id)return id==0 end,
                Info=function(_,name)lookups[name]=true;return {Index=name}end,
                HasBuilding=function(_,id)reads[id]=(reads[id] or 0)+1;return false end,
                RemoveBuilding=function()removes=removes+1 end}
              local city={GetBuildings=function()return {}end}
              Players={[0]={GetCities=function()return {Members=function()return ipairs({city})end}end}}
              if before then SPCLegacyCleanup.StartBoostLoad(P,shared)end
              SPCLegacyCleanup.StartGreatWorkLoad(P,shared)
              publish()
              assert(not shared.GreatWorkLoadCleanup.ready and not reads.BUILDING_SPC_B055_GW_CITY)
              Events.LoadScreenClose.Fire()
              assert(shared.GreatWorkLoadCleanup.ready and removes==0)
            """, previous)
            counts = dict(ctx.globals().reads)
            for name in ('BUILDING_SPC_B055_GW_CITY', 'BUILDING_SPC_B055_GW_OBJECT'):
                self.assertEqual(counts.pop(name), 2)
            self.assertEqual(set(counts), exact_ids()[0] if previous else set())
            self.assertEqual(sum(counts.values()), 1126 if previous else 0)
        measure('boost_empty_city_before_after', {'b533_checks': 1126, 'current_checks': 0,
                                                  'great_work_presence_reads_per_city': 4})

    def test_network_input_keeps_both_independent_coefficients(self):
        ctx = Context()
        ctx.load('NetworkBridge')
        ctx.execute("""
          local cities={GetCapitalCity=function()return nil end, Members=function()return ipairs({})end}
          Players={[0]={GetCities=function()return cities end}}
          local function capture()return SPCNetworkInput.Capture({},shared,0,{},'empty')end
          local initial=capture()
          assert(initial.kResearch==1 and initial.kCulture==1 and SPCBoostConfig.rows==nil)
          SPCBoostConfig.k.RESEARCH=1.2
          local research=capture()
          assert(research.kResearch==1.2 and research.kCulture==1 and research.signature~=initial.signature)
          SPCBoostConfig.k.CULTURE=1.3
          local both=capture()
          assert(both.kResearch==1.2 and both.kCulture==1.3 and both.signature~=research.signature)
        """)

    def test_exact_package_switch_and_rollback(self):
        with package(B533) as prior:
            verify_package_round_trip(self, prior/'Mod', ROOT/'Mod', REMOVED, 'Data/GreatWorkProbe.sql')
            verify_stable_round_trip(self, prior/'Mod', ROOT/'Mod', REMOVED)


class NativeDatabaseInputs(TestCase):
    def check_delta(self, before, after):
        buildings, modifiers = exact_ids()
        key_table(before)
        for table, key, count in TABLES:
            with self.subTest(table=table):
                columns = [c[1] for c in before.execute(f'PRAGMA table_info({table})')]
                index = columns.index(key)
                previous = set(before.execute(f'SELECT * FROM {table}'))
                current = set(after.execute(f'SELECT * FROM {table}'))
                removed = previous - current
                expected = set(before.execute(f'SELECT * FROM {table} WHERE {key} IN (SELECT id FROM retired)'))
                self.assertFalse(current - previous)
                self.assertEqual(removed, expected)
                self.assertEqual(len(removed), count)
                if table in ('Types', 'Buildings', 'Buildings_XP2', 'Modifiers'):
                    self.assertEqual({r[index] for r in removed}, modifiers if key=='ModifierId' else buildings)
        for key in ('BUILDING_SPC_B055_GW_CITY','BUILDING_SPC_B055_GW_OBJECT'):
            self.assertTrue(after.execute('SELECT 1 FROM BuildingModifiers WHERE BuildingType=?', (key,)).fetchone())
        self.assertEqual(set(before.execute('PRAGMA foreign_key_check')), set(after.execute('PRAGMA foreign_key_check')))

    def test_official_full_manifest_exact_delta(self):
        with (package(B533) as prior, closing(assembly.snapshot('SPC_OFFICIAL_DB')) as before,
              closing(assembly.snapshot('SPC_OFFICIAL_DB')) as after):
            with mock.patch.object(assembly, 'MOD', prior/'Mod'):
                old_files = assembly.replay(before, hd=False)
            files = assembly.replay(after, hd=False)
            self.assertEqual(set(old_files) - set(files), set(REMOVED[1:]))
            self.assertEqual(files, [f for f in old_files if f not in REMOVED])
            self.check_delta(before, after)

    def test_hd_replays_confirmed_rows_and_only_retires_this_family(self):
        with (package(B533) as prior, closing(assembly.snapshot('SPC_HD_DB')) as captured,
              closing(assembly.snapshot('SPC_HD_DB')) as model):
            key_table(model)
            hashes = dict(captured.execute('SELECT Type,Hash FROM Types'))
            model.create_function('Make_Hash', 1, hashes.__getitem__)
            for table, key, _ in TABLES:
                model.execute(f'DELETE FROM {table} WHERE {key} IN (SELECT id FROM retired)')
            actions = {'SPC_B055_Boost', 'SPC_InternalCarrierPillage'}
            with mock.patch.object(assembly, 'MOD', prior/'Mod'):
                assembly.replay(model, hd=True, selected=actions)
            for table, _, _ in TABLES:
                self.assertEqual(set(captured.execute(f'SELECT * FROM {table}')),
                                 set(model.execute(f'SELECT * FROM {table}')), table)
            for table, key, _ in TABLES:
                model.execute(f'DELETE FROM {table} WHERE {key} IN (SELECT id FROM retired)')
            self.assertEqual(assembly.replay(model, hd=True, selected=actions), ['Data/InternalCarrierPillage.sql'])
            self.check_delta(captured, model)
