"""Audit-only, real deployment functions operating on tiny /private/tmp packages.
Only Git admission is stubbed; no CLI/config/runtime/game access or Git mutation.
Inject after successful first Path.rename, before caller records moved=True.
"""
from pathlib import Path
import argparse
import hashlib
import importlib.util
import json
import sys
import tempfile
from unittest.mock import patch

p=argparse.ArgumentParser(description=__doc__)
p.add_argument('--repo',type=Path,required=True)
p.add_argument('--output',type=Path,required=True)
a=p.parse_args(); repo=a.repo.resolve()
spec=importlib.util.spec_from_file_location('deploy',repo/'tools/deploy.py')
d=importlib.util.module_from_spec(spec);spec.loader.exec_module(d)
sys.modules['deploy']=d
spec=importlib.util.spec_from_file_location('audit_temporary_playtest',repo/'tools/temporary_playtest.py')
t=importlib.util.module_from_spec(spec);spec.loader.exec_module(t)

def package(path,contents):
    path.mkdir(parents=True)
    (path/'SpecializationP0.modinfo').write_text(f'<Mod id="{d.UUID}" version="1"><Files><File>fixture.txt</File></Files></Mod>')
    (path/'fixture.txt').write_text(contents)

def run(kind,mode):
    with tempfile.TemporaryDirectory(prefix='spc-audit-w09-',dir='/private/tmp') as td:
        root=Path(td).resolve()
        stable=root/'main'; dev=root/'develop'; target=root/'Game/Mods/SpecializationP0'
        package(stable/'Mod','old');package(dev/'Mod','new');package(target,'old')
        other=target.parent/'UnrelatedMod/keep.txt';other.parent.mkdir();other.write_text('untouched')
        source=stable/'Mod' if kind=='stable' else dev/'Mod'
        if kind=='stable':(source/'fixture.txt').write_text('new')
        old=d.snapshot(target)['digest'];new=d.snapshot(source)['digest']
        archive=target.parent.parent/'SpecializationDeploymentBackups'
        receipt=archive/'fixture-receipt.json'
        marker=target.parent/'.specialization-deploy-pending.json'
        calls=[];original=Path.rename
        def rename(self,destination):
            assert self.is_relative_to(root) and Path(destination).is_relative_to(root)
            result=original(self,destination)
            calls.append([str(self.relative_to(root)),str(Path(destination).relative_to(root))])
            if mode=='post_rename_interrupt' and self==target:
                raise KeyboardInterrupt('AUDIT_AFTER_RENAME_BEFORE_MOVED_FLAG')
            return result
        def stable_gate(path,authorized):
            assert path==source and authorized
        def git_root(path,branch):
            assert (path,branch) in [(stable,'main'),(dev,'develop')]
            return 'AUDIT_STUB_'+branch
        def failpoint():raise RuntimeError('AUDIT_NORMAL_FAILPOINT_AFTER_MOVED_FLAG')
        caught=None
        with patch.object(d,'stable_gate',stable_gate),patch.object(t,'git_root',git_root),patch.object(Path,'rename',rename):
            try:
                kw={'authorized':True}
                if mode=='normal_failpoint':kw['failpoint']=failpoint
                if kind=='stable':d.apply(source,target,new,old,**kw)
                else:t.switch(source,target,receipt,stable,new,old,**kw)
            except BaseException as e:caught=type(e).__name__
        assert caught
        backups=[]
        for candidate in sorted(archive.glob('*backup*')):
            if candidate.is_dir():backups.append({'name':candidate.name,'matches_previous':d.snapshot(candidate)['digest']==old})
        data={'path':kind,'injection':mode,'exception':caught,'target_exists':target.exists(),
          'target_matches_previous':target.exists() and d.snapshot(target)['digest']==old,
          'marker_exists':marker.exists(),'receipt_phase':json.loads(receipt.read_text())['phase'] if receipt.exists() else None,
          'backups':backups,'unrelated_untouched':other.read_text()=='untouched','renames':calls}
        if mode=='normal_failpoint':assert data['target_matches_previous'] and not data['marker_exists']
        else:
            assert not data['target_exists'] and any(x['matches_previous'] for x in backups)
            assert data['marker_exists']==(kind=='temporary')
            if kind=='temporary':assert data['receipt_phase']=='SWITCH_PENDING'
        assert data['unrelated_untouched']
        return data

result={'scope':'LOCAL_STRUCTURAL_REPRODUCTION, real filesystem temp-only; not real deployment, signal-frequency or power-loss evidence',
 'source':{name:hashlib.sha256((repo/name).read_bytes()).hexdigest() for name in ['tools/deploy.py','tools/temporary_playtest.py']},
 'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
 'stub_boundary':'stable_gate and git_root assert fixture paths and authorization but skip Git; Path.rename delegates actual rename then injects KeyboardInterrupt. All package paths are under disposable /private/tmp fixtures. No current config/runtime read.',
 'cases':[run(kind,mode) for kind in ['stable','temporary'] for mode in ['normal_failpoint','post_rename_interrupt']],
 'limits':'Injected post-rename outcome window; not observed incident, asynchronous OS-signal timing, concurrency or power-loss simulation. Old whole package preserved in both interrupted cases. Temporary marker/receipt preserve recovery, unlike stable marker removal.'}
a.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:result[k] for k in ['scope','cases']},ensure_ascii=False,indent=2))
