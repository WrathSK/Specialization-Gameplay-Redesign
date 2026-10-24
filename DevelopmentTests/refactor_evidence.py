"""Compact review output; full local artifacts and immutable historical retrieval.

No gameplay/native access. A local file/hash is not a permanent archive.
"""
import argparse
import hashlib
import json
import os
import platform
import re
import sqlite3
import subprocess
import sys
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCOPES = ('Mod', 'DevelopmentTests', 'tools')
HISTORY = 'Specialization/Status/Validation/Results/Refactor_Closure_History.md'
ROW = re.compile(r'^\| `([^`]+_Closure\.json)` \| `([0-9a-f]{40})` \| `([0-9a-f]{64})` \| (\d+) \| (\d+) \|$')


def sha(data):
    return hashlib.sha256(data).hexdigest()


def git(root, *args):
    return subprocess.check_output(['git', *args], cwd=root)


def source_snapshot(root=ROOT, commit=None):
    """Identity only until these bytes are matched to an available Git commit."""
    if commit:
        paths = git(root, 'ls-tree', '-r', '--name-only', commit, '--', *SCOPES).decode().splitlines()
        entries = {p: sha(git(root, 'show', commit + ':' + p)) for p in paths}
    else:
        paths = git(root, 'ls-files', '-c', '-o', '--exclude-standard', '--', *SCOPES).decode().splitlines()
        entries = {p: sha((root / p).read_bytes()) for p in sorted(set(paths))
                   if (root / p).is_file() and not (root / p).is_symlink()}
    digest = sha(json.dumps(entries, sort_keys=True, separators=(',', ':')).encode())
    return {'scopes': list(SCOPES), 'sha256': digest, 'files': entries}


def output_path(root, stage, requested=None):
    if not re.fullmatch(r'[A-Za-z0-9_-]+', stage):
        raise ValueError('Unsafe stage name')
    base = (root / 'local/refactor').resolve()
    if not base.is_relative_to(root.resolve()):
        raise ValueError('Local artifact base must stay inside the repository')
    path = Path(requested).resolve() if requested else base / (stage + '-' + uuid.uuid4().hex) / 'closure.json'
    if not path.is_relative_to(base):
        raise ValueError('Full artifacts must be inside ignored local/refactor/')
    if subprocess.run(['git', 'check-ignore', '-q', str(path)], cwd=root).returncode != 0:
        raise ValueError('Full artifact output must be Git-ignored')
    if path.exists():
        raise FileExistsError('Do not overwrite a previous run: ' + str(path))
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def environment(lupa_version):
    return {'python': platform.python_version(), 'implementation': platform.python_implementation(),
            'platform': platform.system(), 'machine': platform.machine(), 'sqlite': sqlite3.sqlite_version,
            'lupa': lupa_version, 'backend': 'Lua 5.1',
            'python_hash_seed': os.environ.get('PYTHONHASHSEED', 'UNSET')}


def external_identity(root=ROOT):
    """Hash configured external input without copying or mutating it; no recovery claim."""
    try:
        from project_paths import external_database
        path = external_database(root)
        identities = {name: sha(p.read_bytes()) for name, p in
                      [('database', path), ('wal', Path(str(path) + '-wal'))] if p.is_file()}
        return {'configured': True, 'sha256': identities, 'recovery': 'EXTERNAL_INPUT_NOT_ARCHIVED'}
    except Exception as error:
        return {'configured': False, 'status': type(error).__name__, 'recovery': 'NOT_ARCHIVED'}


def store_artifact(path, report, stdout='', stderr=''):
    # Exclusive writes retain distinct failed and successful attempts.
    report['transcripts'] = {suffix: sha(text.encode()) for suffix, text in [('.stdout.log', stdout), ('.stderr.log', stderr)]}
    for suffix, text in [('.stdout.log', stdout), ('.stderr.log', stderr)]:
        with path.with_suffix(suffix).open('x', encoding='utf-8') as stream:
            stream.write(text)
    with path.open('x', encoding='utf-8') as stream:
        json.dump(report, stream, ensure_ascii=False, indent=2)
        stream.write('\n')


def summary(path, root=ROOT, baseline=None):
    report = json.loads(path.read_text())
    prior = json.loads(baseline.read_text()) if baseline else {}
    snap = report.get('source_snapshot', {})
    measured = {k: v for k, v in report.get('measurements', {}).items()
                if prior.get('measurements', {}).get(k) != v}
    loc = str(path.resolve().relative_to(root.resolve()))
    lines = ['### Machine validation evidence', '',
             '- Stage/status: `' + report['stage'] + '` / `' + report['status'] + '`; tests=' + str(report['tests_run']) +
             ', passing=' + str(len(report['passing_properties'])) + ', registered-open=' + str(len(report['counterexamples'])) + '.',
             '- Source: base `' + report['source_head'] + '`; dirty=' + str(report['source_dirty']) +
             '; input SHA256 `' + str(snap.get('sha256', 'UNRECORDED')) + '`; stable=' + str(report.get('source_stable', False)) + '.',
             '- Source scope: Mod/DevelopmentTests/tools, including tracked and nonignored new files. The containing commit must match this input digest; parent HEAD alone is not the tested snapshot.',
             '- Command: `' + report.get('command', 'UNRECORDED') + '`.',
             '- Environment: `' + json.dumps(report.get('environment', {}), sort_keys=True) + '`.',
             '- External input: `' + json.dumps(report.get('external_input', {}), sort_keys=True) + '`.',
             '- Full artifact: `' + loc + '`; SHA256 `' + sha(path.read_bytes()) + '`; stdout/stderr alongside it.',
             '- Retention: LOCAL_ONLY, not a permanent backup. A hash identifies bytes but cannot recover them. Re-running creates comparable new evidence, not the old execution.',
             '- Executed modules/fragments: ' + str(len(report.get('executed', {}))) +
             '; this is observed loading/completion, not full function/path coverage. Detailed mappings remain in the artifact.']
    for label in ('counterexamples', 'failures', 'errors', 'unexpected'):
        if report.get(label):
            # Full tracebacks stay local; review unique durable failure evidence separately.
            items = [{k: v for k, v in row.items() if k != 'failure'} if isinstance(row, dict) else row
                     for row in report[label]]
            lines.append('- ' + label + ': `' + json.dumps(items, ensure_ascii=False) + '`.')
    if measured:
        lines.append('- Measurements (' + ('changed from prior artifact' if baseline else 'selected run') + '): `' + json.dumps(measured, ensure_ascii=False, sort_keys=True) + '`.')
    lines += ['- Limits/mocks: `' + json.dumps({'exclusions': report.get('exclusions', []), 'native_mocks': report.get('native_mocks', [])}, ensure_ascii=False) + '`; LOCAL_SIMULATION only.', '']
    return '\n'.join(lines)


def history_rows(root=ROOT):
    lines = (root / HISTORY).read_text().splitlines()
    rows = []
    for line in lines:
        if line.startswith('| `Specialization/') and '_Closure.json` | `' in line:
            match = ROW.fullmatch(line)
            if not match:
                raise ValueError('Malformed history index row')
            path, commit, digest, size, count = match.groups()
            if Path(path).is_absolute() or '..' in Path(path).parts:
                raise ValueError('Unsafe history path')
            rows.append((path, commit, digest, int(size), int(count)))
    if len(rows) != 31 or len({row[0] for row in rows}) != len(rows):
        raise ValueError('Expected exact 31 unique approved historical Closure entries')
    return rows


def verify_history(root=ROOT):
    rows = history_rows(root)
    tip_match = re.search(r'Published anchor: `([0-9a-f]{40})`', (root / HISTORY).read_text())
    if not tip_match:
        raise ValueError('Missing published anchor')
    tip = tip_match[1]
    for path, commit, digest, size, lines in rows:
        subprocess.run(['git', 'merge-base', '--is-ancestor', commit, tip], cwd=root, check=True)
        data = git(root, 'show', commit + ':' + path)
        if sha(data) != digest or len(data) != size or len(data.splitlines()) != lines:
            raise ValueError('History bytes differ: ' + path)
    return rows


def extract_history(root, filename):
    rows = verify_history(root)
    row = [r for r in rows if Path(r[0]).name == filename]
    if len(row) != 1:
        raise ValueError('Select an exact indexed filename')
    path, commit, *_ = row[0]
    data = git(root, 'show', commit + ':' + path)
    out = output_path(root, 'history', root / 'local/refactor/history' / Path(path).name)
    with out.open('xb') as stream:
        stream.write(data)
    return out


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    h = sub.add_parser('history'); h.add_argument('--extract', metavar='FILENAME')
    s = sub.add_parser('summary'); s.add_argument('artifact', type=Path); s.add_argument('--baseline', type=Path)
    c = sub.add_parser('source'); c.add_argument('artifact', type=Path); c.add_argument('--commit', default='HEAD')
    args = parser.parse_args()
    if args.command == 'history':
        rows = verify_history()
        if args.extract:
            out = extract_history(ROOT, args.extract)
            print(str(out.relative_to(ROOT)))
        print('31/31 historical Closure blobs and hashes match; Git history preserved.')
    elif args.command == 'source':
        expected = json.loads(args.artifact.read_text())['source_snapshot']['sha256']
        actual = source_snapshot(commit=args.commit)['sha256']
        if expected != actual:
            raise ValueError('Tested inputs do not match this commit')
        print('Tested input digest matches ' + args.commit + ' for ' + ', '.join(SCOPES))
    else:
        print(summary(args.artifact, baseline=args.baseline))


if __name__ == '__main__':
    main()
