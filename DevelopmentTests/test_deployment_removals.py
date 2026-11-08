"""Exact removal and rollback gates, exclusively in disposable package fixtures."""

import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
import deploy
import temporary_playtest as temporary

REMOVED = 'UI/Retired.lua'


def make_package(root, old):
    root.mkdir(parents=True)
    (root / 'Kept.lua').write_text('-- Kept\n')
    files = '<File>Kept.lua</File>'
    if old:
        (root / 'UI').mkdir()
        (root / REMOVED).write_text('-- Exact old file\n')
        files += f'<File>{REMOVED}</File>'
    (root / 'SpecializationP0.modinfo').write_text(
        f'<Mod id="{deploy.UUID}" version="{1 if old else 2}"><Files>{files}</Files></Mod>')


def commit(root, branch):
    def git(*args):
        return subprocess.run(['git', '-C', str(root), *args], check=True, capture_output=True, text=True)
    git('init', '-b', branch)
    git('add', '--', 'Mod')
    git('-c', 'user.name=Fixture', '-c', 'user.email=fixture@example.invalid', 'commit', '-m', 'Fixture')
    return git('rev-parse', 'HEAD').stdout.strip()


class ReviewedRemoval(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory(prefix='spc-exact-removal-')
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name).resolve()
        self.target = self.root / 'Game/Mods/SpecializationP0'
        make_package(self.target, old=True)
        self.other = self.target.parent / 'OtherMod/keep'
        self.other.parent.mkdir()
        self.other.write_text('Unrelated')
        self.marker = self.target.parent / '.specialization-deploy-pending.json'
        self.archive = self.target.parent.parent / 'SpecializationDeploymentBackups'
        self.before = deploy.snapshot(self.target)
        self.source = self.root / 'Candidate/Mod'
        make_package(self.source, old=False)
        self.after = deploy.snapshot(self.source)

    def assert_pristine(self):
        self.assertEqual(deploy.snapshot(self.target), self.before)
        self.assertFalse(self.marker.exists())
        self.assertEqual(self.other.read_text(), 'Unrelated')

    def test_unlisted_missing_duplicate_unsafe_and_undeclared_paths_are_rejected(self):
        for allowed in ([], REMOVED, [REMOVED, 'Kept.lua'], [REMOVED, REMOVED], ['/UI/Retired.lua'],
                        ['UI/../UI/Retired.lua'], ['UI/*'], ['ui/Retired.lua']):
            with self.subTest(allowed=allowed), self.assertRaises(ValueError):
                deploy.check(self.source,self.target,allow_remove=allowed)
        checked = deploy.check(self.source,self.target,allow_remove=[REMOVED])
        self.assertEqual(checked['removed_paths'], [REMOVED])
        self.assertEqual(checked['runtime_hash'], self.before['digest'])
        self.assert_pristine()
        self.assertFalse(self.archive.exists())
        extra = self.target / 'unrecognized.txt'
        extra.write_text('Keep me')
        for allowed in ([REMOVED], [REMOVED,extra.name]):
            with self.assertRaises(ValueError):
                deploy.check(self.source,self.target,allow_remove=allowed)
        self.assertEqual(extra.read_text(), 'Keep me')

    def test_stable_remove_requires_reviewed_hashes_and_retains_recoverable_package(self):
        source_commit = commit(self.source.parent,'main')
        args=(self.source,self.target,self.after['digest'],self.before['digest'])
        with self.assertRaisesRegex(ValueError,'explicit user-approved'):
            deploy.apply(*args,allow_remove=[REMOVED])
        with self.assertRaisesRegex(ValueError,'hash mismatch'):
            deploy.apply(self.source,self.target,'stale',self.before['digest'],
                         authorized=True,allow_remove=[REMOVED])
        self.assert_pristine()

        def after_rename():
            pending = json.loads(self.marker.read_bytes())
            receipt = json.loads(Path(pending['receipt']).read_bytes())
            self.assertEqual(receipt['phase'],'SWAP_PENDING')
            self.assertEqual(receipt['removed_paths'],[REMOVED])
            self.assertEqual(deploy.snapshot(Path(receipt['backup'])),self.before)
            self.assertFalse(self.target.exists())
            raise RuntimeError('AFTER_RENAME')

        with self.assertRaisesRegex(RuntimeError,'AFTER_RENAME'):
            deploy.apply(*args,authorized=True,allow_remove=[REMOVED],failpoint=after_rename)
        self.assert_pristine()
        failed = next(self.archive.glob('*.receipt.json'))
        self.assertEqual(json.loads(failed.read_bytes())['phase'],'FAILED_ROLLED_BACK')
        result = deploy.apply(*args,authorized=True,allow_remove=[REMOVED])
        receipt = json.loads(Path(result['receipt']).read_bytes())
        self.assertEqual(receipt['phase'],'DEPLOYED')
        self.assertEqual(receipt['source_commit'],source_commit)
        self.assertEqual(receipt['removed_paths'],[REMOVED])
        self.assertEqual(receipt['runtime_hash'],self.before['digest'])
        self.assertEqual(deploy.snapshot(Path(receipt['backup'])),self.before)
        self.assertEqual(deploy.snapshot(self.target),self.after)
        self.assertFalse(self.marker.exists())
        self.assertEqual(self.other.read_text(),'Unrelated')

    def test_staging_and_post_swap_errors_preserve_the_old_package(self):
        commit(self.source.parent,'main')
        args=(self.source,self.target,self.after['digest'],self.before['digest'])
        with patch.object(deploy.shutil,'copytree',side_effect=OSError('STAGE_COPY_FAILED')):
            with self.assertRaisesRegex(OSError,'STAGE_COPY_FAILED'):
                deploy.apply(*args,authorized=True,allow_remove=[REMOVED])
        self.assert_pristine()

        snapshot = deploy.snapshot
        def reject_installed(path):
            if path==self.target and not (self.target/REMOVED).exists():
                raise RuntimeError('POST_SWAP_VERIFICATION_FAILED')
            return snapshot(path)

        with patch.object(deploy,'snapshot',side_effect=reject_installed):
            with self.assertRaisesRegex(RuntimeError,'POST_SWAP_VERIFICATION_FAILED'):
                deploy.apply(*args,authorized=True,allow_remove=[REMOVED])
        self.assert_pristine()
        failed = next(self.archive.glob('*.receipt.json'))
        self.assertEqual(json.loads(failed.read_bytes())['phase'],'FAILED_ROLLED_BACK')

    def test_candidate_with_dangling_ui_replacement_is_not_a_package(self):
        manifest = self.source/'SpecializationP0.modinfo'
        manifest.write_text(manifest.read_text().replace('</Mod>',
            f'<InGameActions><ReplaceUIScript><Properties><LuaReplace>{REMOVED}</LuaReplace>'
            '</Properties></ReplaceUIScript></InGameActions></Mod>'))
        with self.assertRaisesRegex(ValueError,'Missing/unsafe modinfo file'):
            deploy.check(self.source,self.target,allow_remove=[REMOVED])
        self.assert_pristine()

    def test_failed_rollback_keeps_exact_recovery_marker_and_original(self):
        commit(self.source.parent,'main')
        rename = Path.rename

        def reject_rollback(source, target):
            if '-backup-' in source.name:
                raise OSError('ROLLBACK_RENAME_FAILED')
            return rename(source, target)

        def fail():
            raise RuntimeError('AFTER_RENAME')

        with patch.object(Path,'rename',reject_rollback), self.assertRaisesRegex(OSError,'ROLLBACK_RENAME_FAILED'):
            deploy.apply(self.source,self.target,self.after['digest'],self.before['digest'],
                         authorized=True,allow_remove=[REMOVED],failpoint=fail)
        pending = json.loads(self.marker.read_bytes())
        self.assertEqual(pending['phase'],'SWAP_PENDING')
        self.assertEqual(pending['removed_paths'],[REMOVED])
        self.assertFalse(self.target.exists())
        self.assertEqual(deploy.snapshot(Path(pending['backup'])),self.before)
        with self.assertRaisesRegex(RuntimeError,'Unresolved deployment transaction'):
            deploy.check(self.source,self.target,allow_remove=[REMOVED])

    def test_temporary_activation_and_receipt_restore_require_exact_packages(self):
        stable = self.root / 'Stable'
        shutil.copytree(self.target, stable/'Mod')
        commit(stable,'main')
        (self.source / 'New.lua').write_text('-- Develop addition\n')
        p = self.source / 'SpecializationP0.modinfo'
        p.write_text(p.read_text().replace('</Files>','<File>New.lua</File></Files>'))
        self.after = deploy.snapshot(self.source)
        commit(self.source.parent,'develop')

        def activation(name, **kwargs):
            return temporary.switch(self.source,self.target,self.archive/name,stable,
                                    self.after['digest'],self.before['digest'],**kwargs)

        with self.assertRaisesRegex(ValueError,'removal list mismatch'):
            activation('active.json',check_only=True)
        with self.assertRaisesRegex(ValueError,'removal list mismatch'):
            activation('active.json',authorized=True)
        result = activation('active.json',check_only=True,allow_remove=[REMOVED])
        self.assertEqual(result['removed_paths'],[REMOVED])
        self.assert_pristine()
        self.assertFalse(self.archive.exists())

        def fail():
            raise RuntimeError('AFTER_RENAME')

        with self.assertRaisesRegex(RuntimeError,'AFTER_RENAME'):
            activation('failed.json',authorized=True,allow_remove=[REMOVED],failpoint=fail)
        self.assert_pristine()
        failed = json.loads((self.archive/'failed.json').read_bytes())
        self.assertEqual(failed['phase'],'FAILED_ROLLED_BACK')
        self.assertEqual(failed['activate_removed_paths'],[REMOVED])
        active = self.archive/'active.json'
        record = activation(active.name,authorized=True,allow_remove=[REMOVED])
        self.assertEqual(record['activate_removed_paths'],[REMOVED])
        self.assertEqual(record['phase'],'DEVELOP_ACTIVE')
        self.assertEqual(deploy.snapshot(self.target),self.after)
        backup = Path(record['stable_backup'])
        self.assertEqual(deploy.snapshot(backup),self.before)

        def restore(**kwargs):
            return temporary.switch(backup,self.target,active,stable,self.before['digest'],
                                    self.after['digest'],restore=True,**kwargs)

        with self.assertRaisesRegex(ValueError,'not a removal override'):
            restore(check_only=True,allow_remove=['New.lua'])
        self.assertEqual(restore(check_only=True)['removed_paths'],['New.lua'])
        with self.assertRaisesRegex(RuntimeError,'AFTER_RENAME'):
            restore(authorized=True,failpoint=fail)
        self.assertEqual(deploy.snapshot(self.target),self.after)
        self.assertEqual(json.loads(active.read_bytes())['phase'],'DEVELOP_ACTIVE')
        restored = restore(authorized=True)
        self.assertEqual(restored['phase'],'STABLE_RESTORED')
        self.assertEqual(restored['restore_removed_paths'],['New.lua'])
        self.assertEqual(deploy.snapshot(Path(restored['develop_backup'])),self.after)
        self.assert_pristine()


if __name__ == '__main__':
    unittest.main()
