"""Temporary-directory safety regression; no access to live deployment target."""
from pathlib import Path
import importlib.util, tempfile, shutil, json
root=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('deploy',root/'tools/deploy.py');d=importlib.util.module_from_spec(spec);spec.loader.exec_module(d)

def rejected(fn):
    try:fn()
    except (ValueError,RuntimeError):return
    raise AssertionError('unsafe operation accepted')

with tempfile.TemporaryDirectory(prefix='spc-deploy-test-') as td:
    t=Path(td).resolve();src=t/'Mod';dst=t/'Mods/SpecializationP0';dst.parent.mkdir()
    shutil.copytree(root/'Mod',src);shutil.copytree(src,dst)
    other=dst.parent/'UnrelatedMod';other.mkdir();(other/'keep').write_text('untouched')
    s=d.check(src,dst);assert s['identical']
    assert d.apply(src,dst,s['source_hash'],s['runtime_hash'])['result']=='NO_CHANGE'
    (src/'Gameplay.lua').write_text((src/'Gameplay.lua').read_text()+'\n-- temporary deployment test only\n')
    state=d.check(src,dst);before=d.snapshot(dst)
    rejected(lambda:d.apply(src,dst,'wrong',state['runtime_hash']))
    assert d.snapshot(dst)==before
    def fail():raise RuntimeError('injected after target rename')
    rejected(lambda:d.apply(src,dst,state['source_hash'],state['runtime_hash'],fail))
    assert d.snapshot(dst)==before and not (dst.parent/'.specialization-deploy-pending.json').exists()
    result=d.apply(src,dst,state['source_hash'],state['runtime_hash'])
    assert d.snapshot(dst)==d.snapshot(src) and d.snapshot(Path(result['backup']))==before
    (dst/'user-change.txt').write_text('preserve')
    rejected(lambda:d.check(src,dst));(dst/'user-change.txt').unlink()
    p=dst.parent/'.specialization-deploy-pending.json';p.write_text('{"phase":"SWAP_PENDING"}')
    rejected(lambda:d.check(src,dst));p.unlink()
    alias=t/'alias';alias.symlink_to(src,target_is_directory=True)
    rejected(lambda:d.check(alias,dst))
    modinfo=dst/'SpecializationP0.modinfo';modinfo.write_text(modinfo.read_text().replace(d.UUID,'wrong'))
    rejected(lambda:d.check(src,dst))
    assert (other/'keep').read_text()=='untouched'
print('LOCAL_SIMULATION_PASS deployment: no-op, hash conflict, staged swap, rollback, retained backup, unknown files, pending crash marker, symlinks, UUID, unrelated Mod untouched')
