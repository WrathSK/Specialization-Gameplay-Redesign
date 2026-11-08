"""Replay the pre-retirement Crew observers from the published package."""

from contextlib import contextmanager
from functools import cache
from hashlib import sha256
from pathlib import Path
import subprocess
import tarfile
import tempfile

from refactor_harness import Context, PackageVFS, ROOT, SOURCES

B444 = '72947b5596825e030ad07b77f41bac6d65809cfe'
RETIRED = ('ConstructionProbe.lua', 'CrewPrecision.lua')
RETIRED_GLOBALS = tuple('SPC' + Path(path).stem for path in RETIRED)


@cache
def source(relative):
    path = 'Mod/' + relative
    data = subprocess.check_output(['git', 'show', f'{B444}:{path}'], cwd=ROOT)
    SOURCES[sha256(data).hexdigest()] = f'historical/{B444}/{path}'
    return data.decode('utf-8')


@contextmanager
def package():
    with tempfile.TemporaryDirectory(prefix='spc-b444-history-') as directory:
        checkout = Path(directory)
        archive = checkout / 'package.tar'
        subprocess.run(['git', 'archive', '-o', str(archive), B444, 'Mod'],
                       cwd=ROOT, check=True)
        with tarfile.open(archive) as tar:
            tar.extractall(checkout, filter='data')
        yield checkout


def gameplay(checkout, **options):
    vfs = PackageVFS(manifest=checkout/'Mod/SpecializationP0.modinfo', **options)
    return Context(vfs=vfs, history=(checkout, B444))
