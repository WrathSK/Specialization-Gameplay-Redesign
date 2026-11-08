"""Exact two-path swap and restoration of the real pre-retirement package."""

from pathlib import Path
import shutil
import tempfile
import unittest
import xml.etree.ElementTree as ET

from retired_crew_sources import RETIRED, package as historical_package
from test_deployment_removals import ROOT, commit, deploy, temporary


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
                after = control_ids(ROOT)
                self.assertEqual(before - after, removed)
                self.assertFalse(after - before)
                source = (ROOT / 'Mod/UI' / f'{panel}.lua').read_text()
                for name in removed:
                    self.assertNotIn(name, source)

    def test_real_package_round_trip_restores_both_paths(self):
        with tempfile.TemporaryDirectory(prefix='spc-crew-package-round-trip-') as directory:
            root = Path(directory).resolve()
            stable, develop = root/'Stable', root/'Develop'
            target = root/'Game/Mods/SpecializationP0'
            receipt = root/'Game/SpecializationDeploymentBackups/b445.json'
            with historical_package() as checkout:
                shutil.copytree(checkout/'Mod', stable/'Mod')
            shutil.copytree(stable/'Mod', target)
            shutil.copytree(ROOT/'Mod', develop/'Mod')
            before, after = deploy.snapshot(target), deploy.snapshot(develop/'Mod')
            self.assertEqual(before['files'].keys() - after['files'].keys(), set(RETIRED))
            self.assertFalse(after['files'].keys() - before['files'].keys())
            commit(stable, 'main')
            source = commit(develop, 'develop')
            args = (develop/'Mod', target, receipt, stable, after['digest'], before['digest'])
            for allowed in ((), RETIRED[:1], (*RETIRED, 'CrewProjects.lua')):
                with self.subTest(allowed=allowed), self.assertRaisesRegex(ValueError, 'removal list mismatch'):
                    temporary.switch(*args, check_only=True, allow_remove=allowed)
            self.assertEqual(deploy.snapshot(target), before)
            self.assertFalse(receipt.exists())
            check = temporary.switch(*args, check_only=True, allow_remove=RETIRED)
            self.assertEqual(check['removed_paths'], list(RETIRED))
            active = temporary.switch(*args, authorized=True, allow_remove=RETIRED)
            self.assertEqual(active['develop_commit'], source)
            self.assertEqual(active['activate_removed_paths'], list(RETIRED))
            self.assertEqual(deploy.snapshot(target), after)
            backup = Path(active['stable_backup'])
            self.assertEqual(deploy.snapshot(backup), before)
            restored = temporary.switch(backup, target, receipt, stable, before['digest'], after['digest'],
                                        restore=True, authorized=True)
            self.assertEqual(restored['phase'], 'STABLE_RESTORED')
            self.assertEqual(deploy.snapshot(target), before)
            self.assertEqual(deploy.snapshot(Path(restored['develop_backup'])), after)
            self.assertFalse(temporary.boundary(target).exists())
