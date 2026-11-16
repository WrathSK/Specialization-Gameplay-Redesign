"""Remove the inactive Meaning experiment while exercising the current owner."""
import unittest

from refactor_harness import Context, PackageVFS, ROOT, measure
from retired_crew_sources import B458, B459, gameplay, package, source
from test_o7_crew_retirement import verify_package_round_trip
from test_pu11_package_absence import NATIVE

REMOVED = 'CultureMeaningProbe.lua'
REMOVED_BINDINGS = ('fact/Binding_CultureMeaningProbe', 'district/Binding_CultureMeaningProbe')


def meaning_status(game):
    game.execute(NATIVE)
    game.load('Gameplay')
    game.execute('''
      local s=ExposedMembers.SPC_P0
      assert(s.CultureMeaningProbe==nil)
      for _,name in ipairs({'FactConsumerBindings','CultureMeaning','CultureInspiration','GreatWorkFacts','Dialogue'})do
        assert(s.StartStatus[name].state=='OK',name)
      end
      local c={GetOwner=function()return 0 end,GetID=function()return 9 end}
      Players[0]:GetCities().FindID=function(_,id)if id==9 then return c end end
      GameEvents.SPC_P0_Request.Fire(0,{Action='CULTURE_MEANING_STATUS',Token='meaning-status',CityID=9})
      assert(s.LastToken=='meaning-status' and s.Snapshot:find('意义延展｜自动生效',1,true))
      meaningStatusReport=s.Snapshot
    ''')
    return game.globals().meaningStatusReport


def bindings_registered(game):
    game.load('FactChanges')
    game.load('FactConsumerBindings')
    game.execute('''
      registrations={}
      local fc=SPCFactChanges.New(shared)
      local register=fc.RegisterConsumer
      fc.RegisterConsumer=function(name,...)
        registrations[#registrations+1]='fact/'..name
        return register(name,...)
      end
      shared.DistrictCompleteness={RegisterConsumer=function(name)
        registrations[#registrations+1]='district/'..name
      end}
      SPCFactConsumerBindings.New(shared)
    ''')
    return list(game.globals().registrations.values())


class MeaningExperimentRetirement(unittest.TestCase):
    def test_real_package_preserves_meaning_status_owner_and_definitions(self):
        profile = PackageVFS(forbidden_globals=('SPCCultureMeaningProbe',))
        self.assertNotIn(REMOVED, profile.files | profile.imports)
        with package(B458) as previous:
            before = gameplay(previous, revision=B458)
            after = Context(vfs=profile)
            self.assertEqual(meaning_status(after), meaning_status(before))
            for path in ('CultureMeaning.lua','CultureMeaningModel.lua','Data/CultureMeaningProbe.sql'):
                self.assertEqual((ROOT/'Mod'/path).read_bytes(), (previous/'Mod'/path).read_bytes())
            # Keep the original exact boundary on the two published Meaning packages.
            for path in ('Gameplay.lua','UI/P0Panel.lua','UI/P0Panel.xml'):
                self.assertEqual(source(path,B459).encode(), (previous/'Mod'/path).read_bytes())
            with package(B459) as retired:
                original_after = gameplay(retired, revision=B459)
                self.assertEqual(meaning_status(original_after), meaning_status(after))
                self.assertEqual(before.load_counts, original_after.load_counts)
        self.assertEqual(after.load_counts['missing'] + after.load_counts['failed'], 0)

    def test_only_old_unowned_fact_subscriptions_are_removed(self):
        with package(B458) as previous:
            old = bindings_registered(gameplay(previous, revision=B458))
            new = bindings_registered(Context(vfs=PackageVFS(forbidden_globals=('SPCCultureMeaningProbe',))))
        for name in REMOVED_BINDINGS:
            self.assertEqual(old.count(name), 1)
        self.assertEqual(new, [name for name in old if name not in REMOVED_BINDINGS])
        measure('meaning_experiment_retirement', {'removed_modeled_subscriptions':list(REMOVED_BINDINGS),
            'active_registrations_match':True})

    def test_exact_temporary_switch_and_recovery(self):
        with package(B458) as previous, package(B459) as retired:
            verify_package_round_trip(self, previous/'Mod', retired/'Mod', (REMOVED,), 'CultureMeaning.lua')
