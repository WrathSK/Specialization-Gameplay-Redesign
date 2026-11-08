#!/usr/bin/env python3
"""Bounded, opt-in SpecializationP0 deployment. Default: read-only check."""
from pathlib import Path, PurePosixPath
import argparse, hashlib, json, os, shutil, subprocess, tempfile, xml.etree.ElementTree as ET

UUID='df9efdad-dd48-40a7-b868-87f0617bc16d'
ROOT=Path(__file__).resolve().parents[1]

def no_symlinks(path):
    path=Path(path).absolute()
    for part in (path,*path.parents):
        if part.is_symlink(): raise ValueError('Symlink path rejected: '+str(part))
    return path

def snapshot(path):
    path=no_symlinks(path)
    if not path.is_dir(): raise ValueError('Directory required: '+str(path))
    result={}
    for p in sorted(path.rglob('*')):
        if p.is_symlink(): raise ValueError('Symlink within package rejected: '+str(p))
        if p.is_file():
            rel=p.relative_to(path).as_posix()
            if '.git' in p.relative_to(path).parts: raise ValueError('Git metadata is not a runtime asset')
            result[rel]=hashlib.sha256(p.read_bytes()).hexdigest()
        elif not p.is_dir(): raise ValueError('Non-regular package entry rejected')
    root=ET.parse(path/'SpecializationP0.modinfo').getroot()
    if root.get('id')!=UUID: raise ValueError('Wrong Mod UUID')
    for node in root.findall('.//File') + root.findall('.//LuaReplace'):
        rel = node.text or ''
        if rel not in result:
            raise ValueError('Missing/unsafe modinfo file: '+rel)
    digest=hashlib.sha256(json.dumps(result,sort_keys=True,separators=(',',':')).encode()).hexdigest()
    return {'files':result,'digest':digest,'version':root.get('version')}

def write_json(path, value):
    """Replace a transaction record with a fully written, synced file."""
    tmp = path.with_name(path.name+'.tmp')
    with tmp.open('x') as f:
        json.dump(value,f,indent=2)
        f.flush()
        os.fsync(f.fileno())
    tmp.replace(path)


def reviewed_removals(target, before, after, allowed):
    """Require the exact old-only paths, each declared by the outgoing package."""
    if isinstance(allowed, (str, bytes)):
        raise ValueError('Reviewed removals must be a list of exact paths')
    allowed = list(allowed)
    for path in allowed:
        if (not isinstance(path, str) or PurePosixPath(path).is_absolute()
                or PurePosixPath(path).as_posix() != path
                or any(part in ('', '.', '..', '.git') for part in path.split('/'))
                or any(ch in path for ch in '\\*?[]')
                or any(ord(ch)<32 for ch in path)):
            raise ValueError('Invalid reviewed removal path: '+repr(path))
    approved = set(allowed)
    if len(approved) != len(allowed):
        raise ValueError('Duplicate reviewed removal path')
    removed = before['files'].keys() - after['files'].keys()
    if removed != approved:
        raise ValueError('Reviewed removal list mismatch: unapproved '
                         +repr(sorted(removed-approved))+', not removed '+repr(sorted(approved-removed)))
    if removed:
        manifest_bytes = (target/'SpecializationP0.modinfo').read_bytes()
        if hashlib.sha256(manifest_bytes).hexdigest() != before['files']['SpecializationP0.modinfo']:
            raise ValueError('Outgoing manifest changed during removal review')
        declared = {node.text for node in ET.fromstring(manifest_bytes).findall('./Files/File')}
        if removed - declared:
            raise ValueError('Refusing to remove undeclared runtime files: '+repr(sorted(removed-declared)))
    return sorted(removed)


def check(source,target,*,allow_remove=()):
    source=no_symlinks(source);target=no_symlinks(target)
    if target.parent.name!='Mods': raise ValueError('Expected explicit Mods parent for scan isolation')
    if target.name!='SpecializationP0': raise ValueError('Target basename must be SpecializationP0')
    if source==target or source in target.parents or target in source.parents:
        raise ValueError('Source and deployment target must be independent directories')
    marker=target.parent/'.specialization-deploy-pending.json'
    if marker.exists(): raise RuntimeError('Unresolved deployment transaction: inspect '+str(marker))
    # Hidden backup directories are scanned by Civ VI too. Reject duplicate identities.
    for manifest in target.parent.rglob('*.modinfo'):
        if manifest == target/'SpecializationP0.modinfo': continue
        try: identity=ET.parse(manifest).getroot().get('id','')
        except ET.ParseError: continue
        if identity.lower()==UUID.lower():
            raise ValueError('Duplicate Mod UUID in game scan directory: '+str(manifest))
    before=snapshot(target);after=snapshot(source)
    removed = reviewed_removals(target, before, after, allow_remove)
    return {'source':str(source),'target':str(target),'source_hash':after['digest'],
            'runtime_hash':before['digest'],'identical':before['files']==after['files'],
            'version':after['version'],'files':len(after['files']),'removed_paths':removed}

def stable_gate(source, authorized=False):
    if not authorized: raise ValueError('Stable deployment requires explicit user-approved update (--authorize-stable-update)')
    source=no_symlinks(source)
    def git(*args):
        p=subprocess.run(['git','-C',str(source.parent),*args],capture_output=True,text=True)
        if p.returncode: raise ValueError('Deployment requires a committed main worktree')
        return p.stdout.strip()
    if Path(git('rev-parse','--show-toplevel')).resolve()!=source.parent.resolve() or source.name!='Mod':
        raise ValueError('Source must be worktree root/Mod')
    if git('symbolic-ref','--short','HEAD')!='main': raise ValueError('Develop/detached deployment is blocked; stable runtime only')
    commit=git('rev-parse','--verify','HEAD')
    if git('status','--porcelain','--untracked-files=all'): raise ValueError('Commit/review worktree changes before stable deployment')
    return commit

def apply(source,target,expected_source,expected_runtime,failpoint=None,*,authorized=False,allow_remove=()):
    commit=stable_gate(source, authorized)
    source=no_symlinks(source);target=no_symlinks(target)
    state=check(source,target,allow_remove=allow_remove)
    if state['source_hash']!=expected_source or state['runtime_hash']!=expected_runtime:
        raise ValueError('Reviewed hash mismatch; refusing to overwrite changes')
    if state['identical']: return dict(state,result='NO_CHANGE')
    marker=target.parent/'.specialization-deploy-pending.json'
    # Exclusive transaction marker. A crash leaves explicit paths for manual recovery.
    with marker.open('x') as f:
        json.dump(dict(state,phase='STARTED'),f);f.flush();os.fsync(f.fileno())
    stage=None;backup=None;receipt=None;moved=False
    try:
        # All staging, rollback and retained copies stay outside the scanned Mods tree.
        archive=no_symlinks(target.parent.parent/'SpecializationDeploymentBackups')
        if archive==source or archive in source.parents or source in archive.parents:
            raise ValueError('Backup directory overlaps canonical source')
        archive.mkdir(exist_ok=True)
        stage=Path(tempfile.mkdtemp(prefix='.SpecializationP0-stage-',dir=archive))
        backup=stage.with_name(stage.name.replace('-stage-','-backup-'))
        if backup.exists(): raise RuntimeError('Backup collision')
        shutil.copytree(source,stage,dirs_exist_ok=True)
        if snapshot(stage)['digest']!=expected_source or snapshot(source)['digest']!=expected_source:
            raise RuntimeError('Source changed while staging')
        if snapshot(target)['digest']!=expected_runtime: raise RuntimeError('Runtime changed while staging')
        pending=dict(state,phase='SWAP_PENDING',source_commit=commit,stage=str(stage),backup=str(backup))
        if state['removed_paths']:
            candidate_receipt=backup.with_name(backup.name+'.receipt.json')
            if candidate_receipt.exists() or candidate_receipt.is_symlink():
                raise RuntimeError('Receipt collision')
            pending['receipt']=str(candidate_receipt)
            write_json(candidate_receipt,pending)
            receipt=candidate_receipt
        write_json(marker,pending)
        target.rename(backup);moved=True
        if failpoint: failpoint()
        stage.rename(target)
        if snapshot(target)['digest']!=expected_source or snapshot(backup)['digest']!=expected_runtime:
            raise RuntimeError('Post-deployment verification failed')
        if receipt: write_json(receipt,dict(pending,phase='DEPLOYED'))
        marker.unlink()
        result=dict(state,result='DEPLOYED',backup=str(backup))
        if receipt: result['receipt']=str(receipt)
        return result
    except BaseException:
        # Ordinary errors restore the entire previous directory, never a mixed package.
        # Hard termination retains the marker + whole backup for explicit human recovery.
        if moved:
            if target.exists(): target.rename(stage.with_name(stage.name+'-failed'))
            backup.rename(target)
            if snapshot(target)['digest']!=expected_runtime:
                raise RuntimeError('Rollback unresolved; marker retained')
        if receipt: write_json(receipt,dict(pending,phase='FAILED_ROLLED_BACK'))
        marker.unlink(missing_ok=True)
        raise

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--config',type=Path,default=ROOT/'local/config.json')
    parser.add_argument('--apply',action='store_true')
    parser.add_argument('--authorize-stable-update',action='store_true',help='Only after explicit user-approved stable update; main/clean required')
    parser.add_argument('--expected-source');parser.add_argument('--expected-runtime')
    parser.add_argument('--allow-remove',action='append',default=[],metavar='MOD_RELATIVE_PATH',
                        help='Repeat for the exact reviewed outgoing paths. No wildcards.')
    parser.add_argument('--confirmed-game-exited',action='store_true',
                        help='Required when applying a reviewed file removal.')
    args=parser.parse_args()
    config=json.loads(args.config.read_text());target=Path(config['runtime_dir']).expanduser()
    if not target.is_absolute(): parser.error('runtime_dir must be absolute')
    if args.apply:
        if not args.expected_source or not args.expected_runtime:parser.error('Apply requires both reviewed hashes')
        if args.allow_remove and not args.confirmed_game_exited:
            parser.error('Applying reviewed removals requires confirmed game exit')
        result=apply(ROOT/'Mod',target,args.expected_source,args.expected_runtime,
                     authorized=args.authorize_stable_update,allow_remove=args.allow_remove)
    else: result=check(ROOT/'Mod',target,allow_remove=args.allow_remove)
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
