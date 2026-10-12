"""Publication gate integration tests: temporary repositories and synthetic data only."""
from pathlib import Path
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
import urllib.parse

SOURCE = Path(__file__).resolve().parents[1]
GIT = shutil.which('git')
GITLEAKS = shutil.which('gitleaks')
POLICY = ('tools/check_publication.py', '.githooks/pre-commit', '.gitleaks.toml')


def synthetic_token():
    # Deliberately constructed at runtime; never a service-issued credential.
    return 'gh' + 'p_' + 'Ac7tY9bQ2mN5rK8vP4xD6zH1sL3wF0jEUa9b'


def personal_path():
    return '/' + 'Users/' + 'publication-fixture/Documents/private.txt'


class PublicationGate(unittest.TestCase):
    def setUp(self):
        if not GIT or not GITLEAKS:
            self.fail('Required git/gitleaks dependency missing: suite NOT_RUN, not skipped/PASS')
        self.temp = tempfile.TemporaryDirectory(prefix='publication-test-')
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.repo = self.base / 'repo'
        self.repo.mkdir()
        self.env = {k: v for k, v in os.environ.items() if not k.startswith(('GIT_', 'GITLEAKS_'))}
        self.env.update(GIT_CONFIG_NOSYSTEM='1', GIT_CONFIG_GLOBAL=os.devnull,
                        PYTHONDONTWRITEBYTECODE='1')
        self.git('init', '-b', 'develop')
        self.git('config', 'user.name', 'Publication fixture')
        self.git('config', 'user.email', 'fixture@example.invalid')
        self.git('config', 'commit.gpgsign', 'false')
        for name in POLICY:
            dest = self.repo / name
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(SOURCE / name, dest)
        self.git('add', '--', *POLICY)
        self.git('commit', '-m', 'fixture baseline')

    def git(self, *args, check=True, cwd=None, input=None):
        return subprocess.run([GIT, *args], cwd=cwd or self.repo, env=self.env,
                              input=input, text=True, capture_output=True, check=check)

    def put(self, name, text, stage=True):
        path = self.repo / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)
        if stage:
            self.git('add', '-f', '--', name)

    def gate(self, env=None):
        return subprocess.run([sys.executable, str(self.repo / POLICY[0])], cwd=self.repo,
                              env=env or self.env, text=True, capture_output=True, timeout=60)

    def assert_pass(self, result):
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn('PUBLICATION_CHECK PASS', result.stdout)

    def fake_scanner(self, body):
        bindir = self.base / 'bin'
        bindir.mkdir(exist_ok=True)
        (bindir / 'git').symlink_to(GIT)
        tool = bindir / 'gitleaks'
        tool.write_text('#!' + sys.executable + '\n' + body)
        tool.chmod(0o700)
        return dict(self.env, PATH=str(bindir))

    def test_normal_report_and_field_names(self):
        self.put('report.md', 'Advisory / Non-authoritative\nAccessToken is an API field.\n'
                 'Source root: `CIV_ASSETS`; `/Users/<user>/` is a placeholder.\n')
        self.assert_pass(self.gate())

    def test_exact_property_values_allowed(self):
        names = ['SPC_CITY_INHERITANCE_V1', 'SPC_INHERITANCE_SHADOW_V1',
                 'SPC_B050_HALF_ENABLED', 'SPC_P0_GOV_ESTABLISHED']
        self.put('property.lua', '\n'.join("key='" + name + "'" for name in names))
        self.assert_pass(self.gate())

    def test_secret_in_force_added_report_is_redacted(self):
        self.put('.gitignore', 'reports/\n')
        value = synthetic_token()
        self.put('reports/review.md', 'token = "' + value + '"\n')
        result = self.gate()
        self.assertEqual(result.returncode, 1, result.stdout)
        self.assertIn('credential rule', result.stdout)
        self.assertNotIn(value, result.stdout + result.stderr)

    def test_spc_variable_does_not_allow_arbitrary_secret(self):
        self.put('property.lua', 'SPC_NEW_KEY="' + synthetic_token() + '"\n')
        self.assertEqual(self.gate().returncode, 1)

    def test_inline_allow_comment_does_not_disable_scan(self):
        self.put('report.md', 'token="' + synthetic_token() + '" # gitleaks:allow\n')
        self.assertEqual(self.gate().returncode, 1)

    def test_encoded_and_plain_personal_paths(self):
        path = personal_path()
        for value in (path, urllib.parse.quote(path, safe=''),
                      urllib.parse.quote(urllib.parse.quote(path, safe=''), safe=''),
                      path.replace('/', '&#47;'),
                      'C:' + chr(92) + 'Users' + chr(92) + 'publication-fixture' + chr(92) + 'report'):
            with self.subTest(encoding=value[:3]):
                self.put('report.md', value + '\n')
                result = self.gate()
                self.assertEqual(result.returncode, 1, result.stdout)
                self.assertIn('personal-path', result.stdout)
                self.assertNotIn(value, result.stdout + result.stderr)

    def test_device_identifier_value_not_field_name(self):
        value = 'a8bc12df' * 4
        self.put('report.md', '"crashReporterKey": "' + value + '"\n')
        result = self.gate()
        self.assertEqual(result.returncode, 1)
        self.assertNotIn(value, result.stdout + result.stderr)

    def test_clean_worktree_does_not_hide_dirty_index(self):
        self.put('report.md', personal_path())
        self.put('report.md', 'clean working copy\n', stage=False)
        self.assertEqual(self.gate().returncode, 1)
        self.assertEqual((self.repo / 'report.md').read_text(), 'clean working copy\n')

    def test_unstaged_secret_is_not_scanned_or_staged(self):
        self.put('report.md', 'clean staged copy\n')
        self.put('report.md', synthetic_token(), stage=False)
        before = self.git('ls-files', '--stage').stdout
        self.assert_pass(self.gate())
        self.assertEqual(before, self.git('ls-files', '--stage').stdout)
        self.assertEqual((self.repo / 'report.md').read_text(), synthetic_token())

    def test_existing_historical_path_not_rejected_for_unrelated_edit(self):
        self.put('historical.md', personal_path() + '\n')
        self.git('commit', '-m', 'fixture history')
        self.put('historical.md', personal_path() + '\nAdditional neutral note.\n')
        self.assert_pass(self.gate())

    def test_existing_file_secret_scans_entire_staged_blob(self):
        self.put('report.md', synthetic_token() + '\n')
        self.git('commit', '-m', 'fixture only')
        self.put('report.md', synthetic_token() + '\nAdditional note\n')
        self.assertEqual(self.gate().returncode, 1)

    def test_raw_types_and_private_directories(self):
        for name in ['local.config.json', 'local/evidence.md', 'ScreenShots/frame.md',
                     'save.Civ6Save', 'Crash.ips', 'native.crash', 'FiraxisLive.log', 'snapshot.sqlite']:
            with self.subTest(path=name):
                self.put(name, 'fixture\n')
                result = self.gate()
                self.assertEqual(result.returncode, 1, result.stdout)
                self.assertIn('prohibited publication path/type', result.stdout)

    def test_symlink_not_followed(self):
        external = self.base / 'outside'
        external.write_text(synthetic_token())
        (self.repo / 'link').symlink_to(external)
        self.git('add', '--', 'link')
        result = self.gate()
        self.assertEqual(result.returncode, 1, result.stdout)
        self.assertIn('symlink/submodule', result.stdout)
        self.assertNotIn(synthetic_token(), result.stdout + result.stderr)

    def test_binary_is_incomplete_not_pass(self):
        (self.repo / 'data.bin').write_bytes(b'\0fixture')
        self.git('add', '--', 'data.bin')
        result = self.gate()
        self.assertEqual(result.returncode, 2)
        self.assertIn('NOT_RUN', result.stdout)

    def test_missing_scanner_is_incomplete(self):
        self.put('report.md', 'safe\n')
        bindir = self.base / 'only-git'
        bindir.mkdir()
        (bindir / 'git').symlink_to(GIT)
        result = self.gate(dict(self.env, PATH=str(bindir)))
        self.assertEqual(result.returncode, 2)
        self.assertIn('gitleaks is missing', result.stdout)

    def test_unstaged_policy_change_is_incomplete(self):
        self.put('report.md', 'safe\n')
        self.put('.gitleaks.toml', 'invalid\n', stage=False)
        result = self.gate()
        self.assertEqual(result.returncode, 2)
        self.assertIn('differs from index', result.stdout)

    def test_invalid_staged_policy_is_incomplete(self):
        self.put('.gitleaks.toml', 'invalid TOML [\n')
        result = self.gate()
        self.assertEqual(result.returncode, 2)
        self.assertNotIn('PUBLICATION_CHECK PASS', result.stdout)

    def test_scanner_failure_suppresses_raw_output(self):
        self.put('report.md', 'safe\n')
        marker = 'DO_NOT_ECHO_DIAGNOSTIC_VALUE'
        env = self.fake_scanner('import sys\nprint(' + repr(marker) + ', file=sys.stderr)\nsys.exit(2)\n')
        result = self.gate(env)
        self.assertEqual(result.returncode, 2)
        self.assertNotIn(marker, result.stdout + result.stderr)

    def test_invalid_scanner_json_is_incomplete(self):
        self.put('report.md', 'safe\n')
        env = self.fake_scanner("import sys,pathlib\npathlib.Path(sys.argv[sys.argv.index('--report-path')+1]).write_text('{}')\n")
        self.assertEqual(self.gate(env).returncode, 2)

    def test_index_mutation_during_scan_is_incomplete(self):
        self.put('report.md', 'safe\n')
        body = ("import sys,pathlib,subprocess\n"
                "pathlib.Path(sys.argv[sys.argv.index('--report-path')+1]).write_text('[]')\n"
                "root=pathlib.Path(" + repr(str(self.repo)) + ")\n"
                "(root/'other.md').write_text('new staged input')\n"
                "subprocess.run(['git','-C',str(root),'add','--','other.md'],check=True)\n")
        result = self.gate(self.fake_scanner(body))
        self.assertEqual(result.returncode, 2)
        self.assertIn('Index or HEAD changed', result.stdout)

    def test_unmerged_index_is_incomplete(self):
        oid = self.git('rev-parse', 'HEAD:.gitleaks.toml').stdout.strip()
        self.git('update-index', '--index-info', input='100644 ' + oid + ' 1\tconflict.md\n100644 ' + oid + ' 2\tconflict.md\n')
        result = self.gate()
        self.assertEqual(result.returncode, 2)
        self.assertIn('Unmerged index', result.stdout)

    def test_initial_policy_publication_and_own_tests_are_scannable(self):
        self.put('DevelopmentTests/test_publication_gate.py', (SOURCE / 'DevelopmentTests/test_publication_gate.py').read_text())
        self.git('update-ref', '-d', 'refs/heads/develop')
        self.assert_pass(self.gate())

    def test_exact_exception_is_needed_but_not_broadened(self):
        self.put('property.lua', "key='SPC_CITY_INHERITANCE_V1'\n")
        self.assert_pass(self.gate())
        self.put('.gitleaks.toml', '[extend]\nuseDefault = true\n')
        result = self.gate()
        self.assertEqual(result.returncode, 1, result.stdout)
        self.assertIn('generic-api-key', result.stdout)

    def test_environment_config_cannot_replace_staged_policy(self):
        self.put('report.md', synthetic_token())
        env = dict(self.env, GITLEAKS_CONFIG_TOML='invalid bypass config')
        result = self.gate(env)
        self.assertEqual(result.returncode, 1, result.stdout)

    def test_empty_index_is_not_applicable(self):
        result = self.gate()
        self.assertEqual(result.returncode, 0)
        self.assertIn('NOT_APPLICABLE', result.stdout)
        self.assertNotIn('PUBLICATION_CHECK PASS', result.stdout)

    def test_real_hook_blocks_develop_but_not_shared_main_worktree(self):
        self.git('config', '--local', 'core.hooksPath', str(self.repo / '.githooks'))
        self.put('report.md', personal_path())
        blocked = self.git('commit', '-m', 'must block', check=False)
        self.assertNotEqual(blocked.returncode, 0)
        self.assertIn('PUBLICATION_CHECK BLOCKED', blocked.stdout + blocked.stderr)
        main = self.base / 'main'
        self.git('worktree', 'add', '-b', 'main', str(main), 'HEAD')
        # If the develop-only hook accidentally runs Python here, it must fail.
        (main / 'tools/check_publication.py').write_text('raise RuntimeError("wrong worktree")\n')
        self.git('add', '--', 'tools/check_publication.py', cwd=main)
        committed = self.git('commit', '-m', 'main fixture stays independent', cwd=main, check=False)
        self.assertEqual(committed.returncode, 0, committed.stdout + committed.stderr)
        self.assertEqual(self.git('branch', '--show-current').stdout.strip(), 'develop')

    def test_good_develop_commit_runs_hook(self):
        self.git('config', '--local', 'core.hooksPath', str(self.repo / '.githooks'))
        self.put('report.md', 'safe report\n')
        committed = self.git('commit', '-m', 'checked fixture')
        self.assertIn('PUBLICATION_CHECK PASS', committed.stdout + committed.stderr)


if __name__ == '__main__':
    unittest.main(verbosity=2)
