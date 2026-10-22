#!/usr/bin/env python3
"""Explicit temporary develop switch / exact stable restore. Never called by normal deploy."""
import argparse, json, os, shutil, subprocess, tempfile
from pathlib import Path
import xml.etree.ElementTree as ET
import deploy as d

def git_root(root, branch):
    root=d.no_symlinks(root)
    def git(*args):
        return subprocess.check_output(['git','-C',str(root),*args],text=True).strip()
    if Path(git('rev-parse','--show-toplevel'))!=root or git('branch','--show-current')!=branch:
        raise ValueError('Wrong worktree/branch')
    if git('status','--porcelain','--untracked-files=all'):
        raise ValueError('Commit/review worktree before switch')
    return git('rev-parse','HEAD')

def write_json(path,value):
    tmp=path.with_name(path.name+'.tmp')
    with tmp.open('x') as f:
        json.dump(value,f,indent=2);f.flush();os.fsync(f.fileno())
    tmp.replace(path)

def boundary(target):
    target=d.no_symlinks(target)
    if target.name!='SpecializationP0' or target.parent.name!='Mods':
        raise ValueError('Explicit SpecializationP0 runtime required')
    marker=target.parent/'.specialization-deploy-pending.json'
    if marker.exists():raise RuntimeError('Pending transaction: inspect before continuing')
    for p in target.parent.rglob('*.modinfo'):
        if p==target/'SpecializationP0.modinfo':continue
        try:identity=ET.parse(p).getroot().get('id','')
        except ET.ParseError:continue
        if identity.lower()==d.UUID:raise ValueError('Duplicate runtime UUID')
    return marker

def switch(source,target,receipt,stable_root,expected_source,expected_runtime,*,restore=False,authorized=False,failpoint=None):
    if not authorized:raise ValueError('Explicit temporary switch/restore authorization required')
    source=d.no_symlinks(source);target=d.no_symlinks(target);receipt=d.no_symlinks(receipt)
    stable_root=d.no_symlinks(stable_root)
    stable_commit=git_root(stable_root,'main')
    marker=boundary(target)
    if source==target or source in target.parents or target in source.parents:raise ValueError('Overlapping packages')
    archive=target.parent.parent/'SpecializationDeploymentBackups'
    archive=d.no_symlinks(archive)
    if receipt.parent!=archive:raise ValueError('Receipt must be outside Mods in deployment archive')
    stable=d.snapshot(stable_root/'Mod');before=d.snapshot(target);after=d.snapshot(source)
    if before['digest']!=expected_runtime or after['digest']!=expected_source:raise ValueError('Reviewed hash mismatch')
    if restore:
        record=json.loads(receipt.read_text())
        if record['phase']!='DEVELOP_ACTIVE' or record['target']!=str(target):raise ValueError('Wrong restore receipt')
        if source!=Path(record['stable_backup']):raise ValueError('Restore only the recorded stable backup')
        if before['digest']!=record['develop_hash'] or after['digest']!=record['stable_hash'] or stable['digest']!=record['stable_hash']:
            raise ValueError('Runtime/backup/main changed; review required')
    else:
        commit=git_root(source.parent,'develop')
        if source.name!='Mod' or receipt.exists():raise ValueError('Wrong source or existing receipt')
        if before['digest']!=stable['digest']:raise ValueError('Runtime must match stable before temporary test')
        record={'schema':1,'phase':'PREPARED','target':str(target),'stable_root':str(stable_root),
                'develop_root':str(source.parent),'stable_commit':stable_commit,'develop_commit':commit,
                'stable_hash':before['digest'],'develop_hash':after['digest'],
                'stable_version':before['version'],'develop_version':after['version']}
    archive.mkdir(exist_ok=True)
    with marker.open('x') as f:
        json.dump({'receipt':str(receipt),'phase':'STARTED'},f);f.flush();os.fsync(f.fileno())
    stage=None;backup=None;moved=False
    try:
        stage=Path(tempfile.mkdtemp(prefix='.temporary-stage-',dir=archive))
        backup=stage.with_name(stage.name.replace('stage','stable-backup' if not restore else 'develop-backup',1))
        shutil.copytree(source,stage,dirs_exist_ok=True)
        if d.snapshot(stage)['digest']!=expected_source or d.snapshot(source)['digest']!=expected_source or d.snapshot(target)['digest']!=expected_runtime:
            raise RuntimeError('Package changed during staging')
        if not restore:record['stable_backup']=str(backup)
        else:record['develop_backup']=str(backup)
        record['phase']='RESTORE_PENDING' if restore else 'SWITCH_PENDING'
        record['stage']=str(stage);record['rollback_backup']=str(backup)
        write_json(receipt,record)
        write_json(marker,{'receipt':str(receipt),'stage':str(stage),'backup':str(backup),'phase':'SWAP_PENDING'})
        target.rename(backup);moved=True
        if failpoint:failpoint()
        stage.rename(target)
        if d.snapshot(target)['digest']!=expected_source or d.snapshot(backup)['digest']!=expected_runtime:
            raise RuntimeError('Post-swap verification failed')
        record['phase']='STABLE_RESTORED' if restore else 'DEVELOP_ACTIVE'
        write_json(receipt,record);marker.unlink()
        return record
    except BaseException:
        if moved:
            if target.exists():target.rename(stage.with_name(stage.name+'-failed'))
            backup.rename(target)
        if d.snapshot(target)['digest']!=expected_runtime:raise RuntimeError('Rollback unresolved; marker retained')
        record['phase']='DEVELOP_ACTIVE' if restore else 'FAILED_ROLLED_BACK'
        write_json(receipt,record);marker.unlink(missing_ok=True)
        raise

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('action',choices=['activate','restore'])
    p.add_argument('--config',required=True,type=Path)
    p.add_argument('--stable-root',required=True,type=Path)
    p.add_argument('--receipt',required=True,type=Path)
    p.add_argument('--expected-source',required=True);p.add_argument('--expected-runtime',required=True)
    p.add_argument('--apply',action='store_true')
    p.add_argument('--authorize-temporary-switch',action='store_true')
    p.add_argument('--confirmed-game-exited',action='store_true')
    a=p.parse_args();target=Path(json.loads(a.config.read_text())['runtime_dir'])
    source=Path(json.loads(a.receipt.read_text())['stable_backup']) if a.action=='restore' else Path(__file__).resolve().parents[1]/'Mod'
    if not a.apply:
        print(json.dumps({'source':str(source),'target':str(target),'source_hash':d.snapshot(source)['digest'],
                          'runtime_hash':d.snapshot(target)['digest'],'mode':'CHECK_ONLY'},indent=2));return
    if not a.confirmed_game_exited:p.error('User must confirm Civilization VI fully exited')
    print(json.dumps(switch(source,target,a.receipt,a.stable_root,a.expected_source,a.expected_runtime,
          restore=a.action=='restore',authorized=a.authorize_temporary_switch),indent=2))
if __name__=='__main__':main()
