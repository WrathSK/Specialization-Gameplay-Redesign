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
B462 = 'cab3de1d0b755b3a65a3f21c0cf5b685dda2dc03'
B463 = '719bde4bd8b5324abbc978528c0965d874b7b538'
B464 = '623903a017788ecec013d1a2c97d98c4ebb87c04'
B465 = '49450c069bc3a76626abbf033c5ece7fab84d87c'
B466 = '130867e1fc6f6fc3c216673a998aac7cf365aa96'
B467 = '5efdc9e9e946b5504d214309e358278b4faf0eb0'
B468 = '4ac113246dacc257cbe4a4e10aa352308417dcaf'
B469 = '6c3c4ce874998fb6498768f3b9dc7bb742aa4a2f'
B470 = '3f7ba47bde7f8bdbacbf13010dc308196d5872d5'
B471 = '3574404f0f484345c469f480531919785781d961'
B472 = '0eab91b55aa608ff833c330dcf0e8aac9516e329'
B473 = 'fce8db9cc6b09d7894554b2d27eecdabcadc2982'
B474 = '735f6ada29e1e893796507ae874c38c074d0c6a9'
B475 = '28c04ef022466248ce5584b5767c9646dc8dd032'
B476 = 'df9461790079ef858f4df11944c78dfc7e0877f3'
B511 = '7de0ba2ed10c64a6e61e0620b25ac308531e630b'
B512 = '79c128c77e4a927b615c779f44a0e1e8d536bce1'
B513 = 'd376f6800c18024c660d0ce4e92e03fecf5f53f6'
B514 = 'e49ca22aff1a7ed0b8f877d5e3549bb21e17d837'
B515 = 'e776b4c9d0514cbc1f0c077b4256283b526f8b04'
B516 = 'ac7b0cf86c45c46d7c4160f8aedd42c8a3a4e5c4'
B517 = 'e8373a177d7dd1ef827277ffb2df223fec276c64'
B518 = 'b426b7898679908c664142ec81aaa34a1810cee2'
B519 = '808c9d0fc56673a83968471b4a786c9620a7f169'
B520 = '8fdbfa885539a61fcbbaef16cebba62daf2b4edd'
B521 = '809dfe5a1d1b5d3dea69bd075667be514923ff28'
B522 = '723780deccccbddf757d4531b34084b38f7ec775'
B523 = '4e0e1b8490a3b7fe34954c3e24ba3d2ee432f193'
B524 = '83fda621a2857423a325f295aa530e5937651f78'
B525 = '1d1d0e284ea14ef6a03d45b6c201979c71b6853c'
B526 = '49d028488bb5a08481d67d0ce6267e663489d094'
B527 = '5cf9b48463cc5f875ebab562cc89c9cedb9d0bcb'
B533 = 'ef7cbd44ddcd2148799d6a9a7c54d903316e07cf'
RETIRED_LEVEL3_FILES = ('Lv3Effects.lua', 'Lv3Support.lua')
RETIRED_ADJACENCY_FILES = ('GreatWorkAdjacency.lua', 'GreatWorkAdjacencyModel.lua')
RETIRED_CITY_STARTS = ('BindingProbe', 'CityJournalProbe', 'CityFlowProbe')
RETIRED_CITY_FILES = tuple(sorted(name+'.lua' for name in (*RETIRED_CITY_STARTS, 'FreshBindingHook')))
RETIRED = ('ConstructionProbe.lua', 'CrewPrecision.lua')
RETIRED_GLOBALS = tuple('SPC' + Path(path).stem for path in RETIRED)


@cache
def source(relative, revision=B444):
    path = 'Mod/' + relative
    data = subprocess.check_output(['git', 'show', f'{revision}:{path}'], cwd=ROOT)
    SOURCES[sha256(data).hexdigest()] = f'historical/{revision}/{path}'
    return data.decode('utf-8')


@contextmanager
def package(revision=B444, *, paths=('Mod',)):
    with tempfile.TemporaryDirectory(prefix='spc-package-history-') as directory:
        checkout = Path(directory)
        archive = checkout / 'package.tar'
        subprocess.run(['git', 'archive', '-o', str(archive), revision, *paths],
                       cwd=ROOT, check=True)
        with tarfile.open(archive) as tar:
            tar.extractall(checkout, filter='data')
        yield checkout


def gameplay(checkout, *, revision=B444, name='Gameplay', **options):
    vfs = PackageVFS(manifest=checkout/'Mod/SpecializationP0.modinfo', **options)
    return Context(name=name, vfs=vfs, history=(checkout, revision))

def boost_history(vm):
    """Use the published B533 directories and cleanup when replaying their old contracts."""
    include = vm.globals().include

    def historical(name):
        if name in ('BoostConfig', 'BoostIntegerConfig', 'LegacyCleanupCatalog', 'LegacyCleanup'):
            return vm.execute(source(name + '.lua', B533))
        return include(name)

    vm.globals().include = historical
    return historical
