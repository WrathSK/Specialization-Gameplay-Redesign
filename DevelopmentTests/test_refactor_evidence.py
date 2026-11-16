"""Evidence storage tests only: no gameplay, external DB, game, or deployment."""
import contextlib
import hashlib
import importlib.util
import io
import json
import subprocess
import sys
import tempfile
import types
import unittest
from pathlib import Path
from unittest.mock import patch
import refactor_evidence as evidence


class Storage(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        self.command('init', '-q')
        (self.root / '.gitignore').write_text('local/\n')
        for scope in evidence.SCOPES:
            (self.root / scope).mkdir()
        (self.root / 'Mod/source.lua').write_text('return 1\n')
        self.commit()

    def command(self, *args):
        return subprocess.check_output(['git', *args], cwd=self.root).decode().strip()

    def commit(self):
        self.command('add', '--', '.')  # Isolated disposable fixture repository only.
        self.command('-c', 'user.name=Fixture', '-c', 'user.email=fixture@example.invalid', 'commit', '-qm', 'fixture')
        return self.command('rev-parse', 'HEAD')

    def test_input_identity_binds_to_real_commit_and_detects_dirty_sources(self):
        original = evidence.source_snapshot(self.root)
        self.assertEqual(original, evidence.source_snapshot(self.root, 'HEAD'))
        (self.root / 'Mod/source.lua').write_text('return 2\n')
        changed = evidence.source_snapshot(self.root)
        self.assertNotEqual(original['sha256'], changed['sha256'])
        (self.root / 'DevelopmentTests/new.py').write_text('assert True\n')
        self.assertNotEqual(changed['sha256'], evidence.source_snapshot(self.root)['sha256'])

    def test_unique_ignored_output_and_no_overwrite_or_tracked_output(self):
        a = evidence.output_path(self.root, 'S6')
        b = evidence.output_path(self.root, 'S6')
        self.assertNotEqual(a, b)
        self.assertTrue(a.is_relative_to(self.root / 'local/refactor'))
        self.assertEqual(self.command('check-ignore', str(a)), str(a))
        with self.assertRaises(ValueError):
            evidence.output_path(self.root, 'S6', self.root / 'tracked.json')
        evidence.store_artifact(a, {'status': 'FAIL'}, 'out', 'traceback')
        with self.assertRaises(FileExistsError):
            evidence.output_path(self.root, 'S6', a)
        with self.assertRaises(FileExistsError):
            evidence.store_artifact(a, {'status': 'PASS'})
        self.assertEqual(json.loads(a.read_text())['status'], 'FAIL')
        self.assertEqual(a.with_suffix('.stderr.log').read_text(), 'traceback')

    def history_fixture(self):
        paths = []
        for n in range(31):
            path = f'Specialization/Status/Validation/Results/B{n}_Closure.json'
            target = self.root / path
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(json.dumps({'n': n}) + '\n')
            paths.append(path)
        commit = self.commit()
        rows = []
        for path in paths:
            data = (self.root / path).read_bytes()
            rows.append(f'| `{path}` | `{commit}` | `{evidence.sha(data)}` | {len(data)} | {len(data.splitlines())} |')
        target = self.root / evidence.HISTORY
        target.write_text(f'Published anchor: `{commit}`\n' + '\n'.join(rows) + '\n')
        return paths, target

    def test_history_survives_current_tree_removal_and_checks_exact_original_bytes(self):
        paths, _ = self.history_fixture()
        self.assertEqual(len(evidence.verify_history(self.root)), 31)
        for path in paths:
            (self.root / path).unlink()
        self.assertEqual(len(evidence.verify_history(self.root)), 31)

    def test_history_extract_refuses_symlink_escape_and_overwrite(self):
        paths, _ = self.history_fixture()
        base = self.root / 'local/refactor'
        base.mkdir(parents=True)
        outside = self.root / 'outside'
        outside.mkdir()
        history = base / 'history'
        history.symlink_to(outside, target_is_directory=True)
        with self.assertRaises(ValueError):
            evidence.extract_history(self.root, Path(paths[0]).name)
        self.assertEqual(list(outside.iterdir()), [])
        history.unlink()
        out = evidence.extract_history(self.root, Path(paths[0]).name)
        original = out.read_bytes()
        with self.assertRaises(FileExistsError):
            evidence.extract_history(self.root, Path(paths[0]).name)
        self.assertEqual(out.read_bytes(), original)

    def test_history_rejects_tampered_hash_missing_and_duplicate_entries(self):
        _, index = self.history_fixture()
        text = index.read_text()
        index.write_text(text.replace('`' + evidence.sha(b'{"n": 0}\n') + '`', '`' + '0' * 64 + '`'))
        with self.assertRaises(ValueError):
            evidence.verify_history(self.root)
        index.write_text('\n'.join(text.splitlines()[:-1]))
        with self.assertRaises(ValueError):
            evidence.history_rows(self.root)
        index.write_text(text + text.splitlines()[1] + '\n')
        with self.assertRaises(ValueError):
            evidence.history_rows(self.root)

    def test_summary_excludes_repeated_execution_matrix_and_keeps_delta_and_limits(self):
        path = evidence.output_path(self.root, 'S6')
        report = {'stage': 'S6', 'status': 'LOCAL_SIMULATION_PASS', 'tests_run': 2,
                  'passing_properties': ['one', 'two'], 'counterexamples': [], 'source_head': 'base',
                  'source_dirty': True, 'source_snapshot': evidence.source_snapshot(self.root), 'source_stable': True,
                  'executed': {'module': {'tests': ['MATRIX_SHOULD_STAY_LOCAL']}},
                  'measurements': {'unchanged': 1, 'changed': 2}, 'command': 'test command',
                  'failures': [], 'errors': [], 'unexpected': []}
        prior = self.root / 'prior.json'
        prior.write_text(json.dumps({'measurements': {'unchanged': 1, 'changed': 1}}))
        evidence.store_artifact(path, report)
        text = evidence.summary(path, self.root, prior)
        self.assertNotIn('MATRIX_SHOULD_STAY_LOCAL', text)
        self.assertNotIn('"unchanged"', text)
        self.assertIn('"changed": 2', text)
        self.assertIn(evidence.sha(path.read_bytes()), text)
        self.assertIn('LOCAL_ONLY', text)
        self.assertIn('parent HEAD alone', text)

    def test_runner_retains_failed_attempt_transcripts_without_gameplay(self):
        # Exercise the actual runner envelope using independent fake test modules;
        # no assertions in production/refactor tests are replaced or executed.
        module = types.ModuleType('evidence_probe')
        class Probe(unittest.TestCase):
            def test_output(self):
                print('retained stdout marker')
            def test_error(self):
                raise RuntimeError('retained failure marker')
        module.Probe = Probe
        harness = types.ModuleType('refactor_harness'); harness.RUN = {}; harness.TrackedLua51 = object
        lupa = types.ModuleType('lupa'); lupa.__version__ = 'fixture'; lupa.__path__ = []
        lua51 = types.ModuleType('lupa.lua51'); lua51.LuaRuntime = object; lupa.lua51 = lua51
        static = types.ModuleType('refactor_static'); static.check = lambda selection: {'widened': []}
        selection = {'stages': {'Evidence': ['evidence_probe.Probe']}, 'counterexamples': {},
                     'exclusions': ['fixture only'], 'native_mocks': [], 'external_prerequisites': []}
        (self.root / 'DevelopmentTests/refactor_selection.json').write_text(json.dumps(selection))
        spec = importlib.util.spec_from_file_location('evidence_runner_fixture', Path(__file__).with_name('run_refactor.py'))
        runner = importlib.util.module_from_spec(spec)
        modules = {'refactor_harness': harness, 'lupa': lupa, 'lupa.lua51': lua51,
                   'refactor_static': static, 'evidence_probe': module}
        with patch.dict(sys.modules, modules):
            spec.loader.exec_module(runner)
            runner.ROOT = self.root
            runner.__file__ = str(self.root / 'DevelopmentTests/run_refactor.py')
            with patch.object(sys, 'argv', ['run_refactor.py', '--stage', 'Evidence']), contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
                self.assertEqual(runner.main(), 1)
        artifacts = list((self.root / 'local/refactor').glob('*/closure.json'))
        self.assertEqual(len(artifacts), 1)
        data = json.loads(artifacts[0].read_text())
        self.assertEqual(data['status'], 'FAIL')
        self.assertEqual(data['tests_run'], 2)
        self.assertTrue(data['source_stable'])
        self.assertIn('retained failure marker', next(iter(data['failure_details'].values())))
        self.assertIn('retained stdout marker', artifacts[0].with_suffix('.stdout.log').read_text())
        self.assertIn('RuntimeError: retained failure marker', artifacts[0].with_suffix('.stderr.log').read_text())


    def test_runner_archives_discovery_and_postcheck_exceptions(self):
        for phase in ('discovery', 'post_validation'):
            with self.subTest(phase=phase):
                module = types.ModuleType('evidence_empty')
                class Probe(unittest.TestCase):
                    def test_pass(self):
                        self.assertTrue(True)
                module.Probe = Probe
                harness = types.ModuleType('refactor_harness'); harness.RUN = {}; harness.TrackedLua51 = object
                lupa = types.ModuleType('lupa'); lupa.__version__ = 'fixture'; lupa.__path__ = []
                lua51 = types.ModuleType('lupa.lua51'); lua51.LuaRuntime = object; lupa.lua51 = lua51
                static = types.ModuleType('refactor_static')
                def failed_static(selection):
                    raise RuntimeError('postcheck original failure')
                static.check = failed_static
                selection = {'stages': {'Evidence': ['evidence_empty.Probe']}, 'counterexamples': {},
                             'exclusions': [], 'native_mocks': [], 'external_prerequisites': []}
                (self.root / 'DevelopmentTests/refactor_selection.json').write_text(json.dumps(selection))
                spec = importlib.util.spec_from_file_location('evidence_aborted_runner', Path(__file__).with_name('run_refactor.py'))
                runner = importlib.util.module_from_spec(spec)
                modules = {'refactor_harness': harness, 'lupa': lupa, 'lupa.lua51': lua51,
                           'refactor_static': static, 'evidence_empty': module}
                with patch.dict(sys.modules, modules):
                    spec.loader.exec_module(runner); runner.ROOT = self.root
                    runner.__file__ = str(self.root / 'DevelopmentTests/run_refactor.py')
                    with patch.object(sys, 'argv', ['run_refactor.py', '--stage', 'Evidence']), contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
                        if phase == 'discovery':
                            with patch.object(unittest.TestLoader, 'loadTestsFromNames', side_effect=AssertionError('import-time original failure')):
                                self.assertEqual(runner.main(), 1)
                        else:
                            self.assertEqual(runner.main(), 1)
                reports = [json.loads(p.read_text()) for p in (self.root / 'local/refactor').glob('*/closure.json')]
                matching = [r for r in reports if 'runner:' + phase in r['errors']]
                self.assertEqual(len(matching), 1)
                self.assertEqual(matching[0]['status'], 'FAIL')
                self.assertIn('original failure', matching[0]['failure_details']['runner:' + phase])


if __name__ == '__main__':
    unittest.main()
