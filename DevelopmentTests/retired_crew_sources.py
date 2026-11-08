"""Replay retired observers from published packages."""

from contextlib import contextmanager
from functools import cache
from hashlib import sha256
from pathlib import Path
import subprocess
import tarfile
import tempfile

from refactor_harness import Context, PackageVFS, ROOT, SOURCES

B119 = 'b3667b20b0fab2c9361a347701785ad330ec34ed'
B120 = '5f8f02fd3a5b4a58587b83cd2b37b3ae114f94ac'
B121 = 'b46cd02857ea3d5c3d30700f4fd36a8ae8d0c9d8'
B444 = '72947b5596825e030ad07b77f41bac6d65809cfe'
B445 = '238cf182af66056eeae0da4e4797114a2a04d73f'
B446 = 'af75e329546f583b94a90169d8af68ebb7e4b559'
B447 = 'e178d14a1693ae83cd45c19afd9fcdc9f0b9ecd4'
B449 = 'fc51d0df7de10425c3272c009849e11c1ad3948d'
B450 = '0224c014aeb0718a0b6f5bad37ad867561c89250'
B452 = '26dfcbd0f7baf8a17e52de2bfcb57071da651a6b'
B453 = '62d89798af67ee37b38027d6b0cfc8ef258c9a5f'
B454 = '3fa7527b768207a8f210136749001584b42e5940'
B455 = 'e5c5afaf3aeb223861b107a220f910da3d8edf98'
B456 = 'fbb1a963d2b5b2afe8218e5f933a09be442e6186'
B457 = '30a0749815b1a953f31101207a4a44e2cd3c1a89'
B458 = '0adc089452b57f5e6faed845ae0da237c49971da'
B459 = '68565bc8d50d141c1a21e64d3c15f392f012a196'
B460 = '4c2c17ca0936c7777a1063c8921b3656811b4596'
B461 = 'f24b000847377e90bb856fb4483ed88ee15297b1'
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
