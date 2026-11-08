"""Replay retired observers from published packages."""

from contextlib import contextmanager
from functools import cache
from hashlib import sha256
from pathlib import Path
import subprocess
import tarfile
import tempfile

from refactor_harness import Context, PackageVFS, ROOT, SOURCES

B120 = '5f8f02fd3a5b4a58587b83cd2b37b3ae114f94ac'
B444 = '72947b5596825e030ad07b77f41bac6d65809cfe'
B445 = '238cf182af66056eeae0da4e4797114a2a04d73f'
B446 = 'af75e329546f583b94a90169d8af68ebb7e4b559'
B447 = 'e178d14a1693ae83cd45c19afd9fcdc9f0b9ecd4'
B449 = 'fc51d0df7de10425c3272c009849e11c1ad3948d'
B450 = '0224c014aeb0718a0b6f5bad37ad867561c89250'
B452 = '26dfcbd0f7baf8a17e52de2bfcb57071da651a6b'
B453 = '62d89798af67ee37b38027d6b0cfc8ef258c9a5f'
B454 = '3fa7527b768207a8f210136749001584b42e5940'
RETIRED = ('ConstructionProbe.lua', 'CrewPrecision.lua')
RETIRED_GLOBALS = tuple('SPC' + Path(path).stem for path in RETIRED)


@cache
def source(relative, revision=B444):
    path = 'Mod/' + relative
    data = subprocess.check_output(['git', 'show', f'{revision}:{path}'], cwd=ROOT)
    SOURCES[sha256(data).hexdigest()] = f'historical/{revision}/{path}'
    return data.decode('utf-8')


@contextmanager
def package(revision=B444):
    with tempfile.TemporaryDirectory(prefix='spc-package-history-') as directory:
        checkout = Path(directory)
        archive = checkout / 'package.tar'
        subprocess.run(['git', 'archive', '-o', str(archive), revision, 'Mod'],
                       cwd=ROOT, check=True)
        with tarfile.open(archive) as tar:
            tar.extractall(checkout, filter='data')
        yield checkout


def gameplay(checkout, *, revision=B444, name='Gameplay', **options):
    vfs = PackageVFS(manifest=checkout/'Mod/SpecializationP0.modinfo', **options)
    return Context(name=name, vfs=vfs, history=(checkout, revision))
