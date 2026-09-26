"""Stdlib-only context helper tests; no gameplay, repository mutation or deployment."""
import copy
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('context_helper', ROOT / 'Specialization/Workflow/context.py')
c = importlib.util.module_from_spec(spec)
spec.loader.exec_module(c)


class ContextTests(unittest.TestCase):
    def test_full_only_manifest_self_test(self):
        manifest = copy.deepcopy(c.load('P0-E2.json'))
        manifest['context'] = [dict(path='AGENTS.md', kind='full', reason='fixture')]
        # Real version/schema/selectors are checked; check() integrity tested separately below.
        with patch.object(c, 'check', return_value={'check': 'PASS'}) as check:
            result = c.self_test(manifest)
        check.assert_called_once_with(manifest)
        self.assertEqual(result['self_test'], 'PASS')
        self.assertIn('stable ID mismatch', result['cases'])

    def test_temporary_file_selectors_and_errors(self):
        with tempfile.TemporaryDirectory() as d, patch.object(c, 'ROOT', Path(d).resolve()):
            p = Path(d) / 'fixture.md'
            p.write_text('# Title\n## Current\nbody\n### Child\nkept\n## History\nold\n')
            ref = dict(path=p.name, kind='section', selector='## Current')
            self.assertEqual(c.project(ref), '## Current\nbody\n### Child\nkept\n')
            with self.assertRaises(FileNotFoundError):
                c.project(dict(path='missing.md', kind='full'))
            for kind, selector in [('head', 999), ('head', True), ('section', 'body'),
                                   ('section', '## Missing'), ('rows', []), ('rows', ['absent'])]:
                with self.subTest(kind=kind, selector=selector), self.assertRaises(ValueError):
                    c.project(dict(path=p.name, kind=kind, selector=selector))
            p.write_text('row x\nrow y\n')
            with self.assertRaises(ValueError):
                c.project(dict(path=p.name, kind='rows', selector=['row']))
            p.write_text(json.dumps({'rules': [{'rule_id': 'RIGHT'}]}))
            self.assertIn('RIGHT', c.project(dict(path=p.name, kind='json', selector='/rules/0', expected_id='RIGHT')))
            with self.assertRaises(ValueError):
                c.project(dict(path=p.name, kind='json', selector='/rules/0', expected_id='WRONG'))

    def test_integrity_rejects_real_hash_change(self):
        # Tiny isolated repository fixture; run real check(), no real Mod bytes changed.
        with tempfile.TemporaryDirectory() as d, patch.object(c, 'ROOT', Path(d).resolve()):
            r = Path(d)
            (r / 'Mod').mkdir()
            (r / 'Mod/a.lua').write_text('-- fixture\n')
            (r / 'review.md').write_text('review\n')
            versions = dict(design='D1', architecture='A1', status='S1')
            paths = {}
            for key in ('research', 'industry', 'culture', 'commerce', 'shared'):
                versions[key] = 'D1'
                paths[key] = key + '.json'
                (r / paths[key]).write_text(json.dumps({'design_revision': 'D1'}))
            for key, prefix in [('design', 'Design Revision:'), ('architecture', 'Architecture Revision:'), ('status', 'Status Revision:')]:
                paths[key] = key + '.md'
                (r / paths[key]).write_text(prefix + ' ' + versions[key])
            manifest = c.load('P0-E2.json')
            schema = c.load('Batch.schema.json')
            manifest['authority_versions'] = versions
            manifest['context'] = [dict(path='review.md', kind='full', reason='fixture')]
            data = {'Authority.json': dict(versions=versions, paths=paths), 'Batch.schema.json': schema,
                    'Runtime_Index.json': {'files': {'Mod/a.lua': dict(sha256=c.digest(r / 'Mod/a.lua'), review_source='review.md')}},
                    'Context_Lock.json': {'files': {'review.md': c.digest(r / 'review.md')}}}
            with patch.object(c, 'load', side_effect=lambda name: data[name]), patch.object(c.subprocess, 'check_output', return_value='develop\n'):
                self.assertEqual(c.check(manifest)['check'], 'PASS')
                (r / 'Mod/a.lua').write_text('-- changed\n')
                with self.assertRaisesRegex(ValueError, 'runtime changed'):
                    c.check(manifest)
                (r / 'Mod/a.lua').write_text('-- fixture\n')
                (r / 'review.md').write_text('changed review')
                with self.assertRaisesRegex(ValueError, 'context changed'):
                    c.check(manifest)
                (r / 'review.md').unlink()
                with self.assertRaises(FileNotFoundError):
                    c.check(manifest)


if __name__ == '__main__':
    unittest.main()
