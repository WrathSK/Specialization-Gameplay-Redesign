"""Prove the fixed candidate can be tested and the actual stable package restored."""

from pathlib import Path
import shutil
import tempfile
import unittest
from unittest.mock import patch

from refactor_harness import PackageVFS, ROOT, TrackedLua51, measure
from retired_crew_sources import B526, package, source
from test_deployment_removals import commit, deploy, temporary
from test_o7_crew_retirement import verify_package_round_trip, verify_stable_round_trip
from test_pu11_package_absence import scalars
import test_p0_k as work


STABLE = 'ce497054ed0ba440a03c5a7a66dfafc0d5721c3d'
STABLE_SHA256 = 'fe601208d9fcdc359c3f8b46a017f5caa19b1284f952c9f7b60e986899b6de30'


class IntegrationCandidate(unittest.TestCase):
    def test_actual_work_sender_keeps_two_packets_without_legacy_model(self):
        packets = []
        for historical in (True, False):
            with patch.object(work, 'LuaRuntime', TrackedLua51):
                fixture = work.Fixture()
            fixture.check(work.PRODUCER)

            def include(name):
                if name == 'DialogueModel':
                    self.assertTrue(historical, 'Unexpected retired model import')
                    fixture.lua.execute(source('DialogueModel.lua', B526))
                else:
                    fixture.include(name)

            fixture.lua.globals().include = include
            lua = (source('UI/DialogueRefresh.lua', B526) if historical
                   else (ROOT/'Mod/UI/DialogueRefresh.lua').read_text())
            fixture.check(lua)
            fixture.check("""
              init();assert(lastPacket.Valid==1 and lastPacket.FactsCities==3)
              first=lastPacket
              a.slots[10]={100}
              fire('GreatWorkCreated',0,999,a.x,a.y,10,100);fire('SystemUpdateUI')
              assert(lastPacket.Seq>first.Seq and lastPacket.FactsCount==1)
              assert(shared.GreatWorkFacts.Read(0,7).count==1)
              result={first,lastPacket}
            """)
            self.assertEqual(bool(fixture.lua.globals().SPCDialogueModel), historical)
            packets.append(scalars(fixture.lua.eval('result')))
        self.assertEqual(*packets)
        profile=PackageVFS()
        self.assertNotIn('DialogueModel.lua',profile.files)
        self.assertNotIn('DialogueModel.lua',profile.imports)
        self.assertFalse((ROOT/'Mod/DialogueModel.lua').exists())

    def test_exact_model_removal_round_trips(self):
        with package(B526) as previous:
            path=('DialogueModel.lua',)
            verify_package_round_trip(self,previous/'Mod',ROOT/'Mod',path,'GreatWorkFacts.lua')
            verify_stable_round_trip(self,previous/'Mod',ROOT/'Mod',path)

    def test_temporary_candidate_switch_and_restore_match_actual_B489_hashes(self):
        with package(STABLE) as archived, tempfile.TemporaryDirectory(prefix='spc-integration-admission-') as directory:
            root=Path(directory).resolve()
            stable, candidate=root/'Stable',root/'Candidate'
            target=root/'Game/Mods/SpecializationP0'
            receipt=root/'Game/SpecializationDeploymentBackups/admission.json'
            shutil.copytree(archived/'Mod',stable/'Mod')
            shutil.copytree(stable/'Mod',target)
            shutil.copytree(ROOT/'Mod',candidate/'Mod')
            commit(stable,'main')
            candidate_commit=commit(candidate,'develop')
            before,after=deploy.snapshot(target),deploy.snapshot(candidate/'Mod')
            self.assertEqual(before['digest'],STABLE_SHA256)
            removed=sorted(before['files'].keys()-after['files'].keys())
            added=sorted(after['files'].keys()-before['files'].keys())
            self.assertEqual((len(before['files']),len(after['files']),len(removed)),(337,314,25))
            self.assertEqual(added,['Text/PackageText.xml','Text/PackageText_Translations.xml'])
            args=(candidate/'Mod',target,receipt,stable,after['digest'],before['digest'])
            with self.assertRaisesRegex(ValueError,'removal list mismatch'):
                temporary.switch(*args,allow_remove=removed[:-1],check_only=True)
            checked=temporary.switch(*args,allow_remove=removed,check_only=True)
            self.assertEqual(checked['removed_paths'],removed)
            mounted=temporary.switch(*args,allow_remove=removed,authorized=True)
            self.assertEqual(mounted['develop_commit'],candidate_commit)
            self.assertEqual(mounted['activate_removed_paths'],removed)
            self.assertEqual(deploy.snapshot(target),after)
            backup=Path(mounted['stable_backup'])
            self.assertEqual(deploy.snapshot(backup),before)
            result=temporary.switch(backup,target,receipt,stable,before['digest'],after['digest'],
                                    restore=True,authorized=True)
            self.assertEqual(result['phase'],'STABLE_RESTORED')
            self.assertEqual(result['restore_removed_paths'],added)
            self.assertEqual(deploy.snapshot(target),before)
            self.assertEqual(deploy.snapshot(Path(result['develop_backup'])),after)
            self.assertFalse(temporary.boundary(target).exists())
            measure('b489_integration_candidate_admission',dict(
                stable_sha256=before['digest'],candidate_sha256=after['digest'],
                activation_removals=removed,restoration_removals=added,
                verified_copy_only=True))
