"""Exact two-path swap and restoration of the real pre-retirement package."""

from pathlib import Path
import shutil
import tempfile
import unittest
import xml.etree.ElementTree as ET

from retired_crew_sources import B445, RETIRED, package as historical_package
from test_deployment_removals import commit, deploy, temporary


class CrewRetirement(unittest.TestCase):
    def test_only_the_three_retired_controls_leave_the_two_panels(self):
        for panel, removed in (
            ('P0Panel', {'ConstructionPreviewButton', 'ConstructionApplyButton'}),
            ('UnitSites', {'PrecisionButton'}),
        ):
            with self.subTest(panel=panel):
                def control_ids(root):
                    doc = ET.parse(root / 'Mod/UI' / f'{panel}.xml')
                    return {node.get('ID') for node in doc.iter() if node.get('ID')}

                with historical_package() as checkout:
                    before = control_ids(checkout)
                with historical_package(B445) as checkout:
                    after = control_ids(checkout)
                    source = (checkout / 'Mod/UI' / f'{panel}.lua').read_text()
                self.assertEqual(before - after, removed)
                self.assertFalse(after - before)
                for name in removed:
                    self.assertNotIn(name, source)

    def test_real_package_round_trip_restores_both_paths(self):
        with historical_package() as before, historical_package(B445) as after:
            verify_package_round_trip(self, before/'Mod', after/'Mod', RETIRED, 'CrewProjects.lua')


def verify_package_round_trip(case, before_mod, after_mod, removed, kept_path):
    with tempfile.TemporaryDirectory(prefix='spc-exact-package-round-trip-') as directory:
        root = Path(directory).resolve()
        stable, develop = root/'Stable', root/'Develop'
        target = root/'Game/Mods/SpecializationP0'
        receipt = root/'Game/SpecializationDeploymentBackups/retirement.json'
        shutil.copytree(before_mod, stable/'Mod')
        shutil.copytree(stable/'Mod', target)
        shutil.copytree(after_mod, develop/'Mod')
        before, after = deploy.snapshot(target), deploy.snapshot(develop/'Mod')
        case.assertEqual(before['files'].keys() - after['files'].keys(), set(removed))
        case.assertFalse(after['files'].keys() - before['files'].keys())
        commit(stable, 'main')
        source = commit(develop, 'develop')
        args = (develop/'Mod', target, receipt, stable, after['digest'], before['digest'])
        for allowed in ((), removed[:1], (*removed, kept_path)):
            with case.subTest(allowed=allowed), case.assertRaisesRegex(ValueError, 'removal list mismatch'):
                temporary.switch(*args, check_only=True, allow_remove=allowed)
        case.assertEqual(deploy.snapshot(target), before)
        case.assertFalse(receipt.exists())
        check = temporary.switch(*args, check_only=True, allow_remove=removed)
        case.assertEqual(check['removed_paths'], list(removed))
        active = temporary.switch(*args, authorized=True, allow_remove=removed)
        case.assertEqual(active['develop_commit'], source)
        case.assertEqual(active['activate_removed_paths'], list(removed))
        case.assertEqual(deploy.snapshot(target), after)
        backup = Path(active['stable_backup'])
        case.assertEqual(deploy.snapshot(backup), before)
        restored = temporary.switch(backup, target, receipt, stable, before['digest'], after['digest'],
                                    restore=True, authorized=True)
        case.assertEqual(restored['phase'], 'STABLE_RESTORED')
        case.assertEqual(deploy.snapshot(target), before)
        case.assertEqual(deploy.snapshot(Path(restored['develop_backup'])), after)
        case.assertFalse(temporary.boundary(target).exists())
