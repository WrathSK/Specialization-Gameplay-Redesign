#!/usr/bin/env python3
"""Bounded, opt-in SpecializationP0 deployment. Default: read-only check."""
from pathlib import Path
import argparse, hashlib, json, os, shutil, tempfile, xml.etree.ElementTree as ET

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
    for node in root.findall('.//File'):
        rel=Path(node.text or '')
        if rel.is_absolute() or '..' in rel.parts or not (path/rel).is_file():
            raise ValueError('Missing/unsafe modinfo file: '+str(rel))
    digest=hashlib.sha256(json.dumps(result,sort_keys=True,separators=(',',':')).encode()).hexdigest()
    return {'files':result,'digest':digest,'version':root.get('version')}

def check(source,target):
    source=no_symlinks(source);target=no_symlinks(target)
    if target.name!='SpecializationP0': raise ValueError('Target basename must be SpecializationP0')
    if source==target or source in target.parents or target in source.parents:
        raise ValueError('Source and deployment target must be independent directories')
    marker=target.parent/'.specialization-deploy-pending.json'
    if marker.exists(): raise RuntimeError('Unresolved deployment transaction: inspect '+str(marker))
    before=snapshot(target);after=snapshot(source)
    # Never erase an unrecognized runtime file by replacing the directory.
    unknown=set(before['files'])-set(after['files'])
    if unknown: raise ValueError('Runtime-only files require separate review: '+repr(sorted(unknown)))
    return {'source':str(source),'target':str(target),'source_hash':after['digest'],
            'runtime_hash':before['digest'],'identical':before['files']==after['files'],
            'version':after['version'],'files':len(after['files'])}

def apply(source,target,expected_source,expected_runtime,failpoint=None):
    source=no_symlinks(source);target=no_symlinks(target)
    state=check(source,target)
    if state['source_hash']!=expected_source or state['runtime_hash']!=expected_runtime:
        raise ValueError('Reviewed hash mismatch; refusing to overwrite changes')
    if state['identical']: return dict(state,result='NO_CHANGE')
    marker=target.parent/'.specialization-deploy-pending.json'
    # Exclusive transaction marker. A crash leaves explicit paths for manual recovery.
    with marker.open('x') as f:
        json.dump(dict(state,phase='STARTED'),f);f.flush();os.fsync(f.fileno())
    stage=None;backup=None;moved=False
    try:
        stage=Path(tempfile.mkdtemp(prefix='.SpecializationP0-stage-',dir=target.parent))
        backup=stage.with_name(stage.name.replace('-stage-','-backup-'))
        if backup.exists(): raise RuntimeError('Backup collision')
        shutil.copytree(source,stage,dirs_exist_ok=True)
        if snapshot(stage)['digest']!=expected_source or snapshot(source)['digest']!=expected_source:
            raise RuntimeError('Source changed while staging')
        if snapshot(target)['digest']!=expected_runtime: raise RuntimeError('Runtime changed while staging')
        with marker.open('w') as f:
            json.dump(dict(state,phase='SWAP_PENDING',stage=str(stage),backup=str(backup)),f);f.flush();os.fsync(f.fileno())
        target.rename(backup);moved=True
        if failpoint: failpoint()
        stage.rename(target)
        if snapshot(target)['digest']!=expected_source: raise RuntimeError('Post-deployment verification failed')
        marker.unlink()
        return dict(state,result='DEPLOYED',backup=str(backup))
    except BaseException:
        # Ordinary errors restore the entire previous directory, never a mixed package.
        # Hard termination retains the marker + whole backup for explicit human recovery.
        if moved:
            if target.exists(): target.rename(stage.with_name(stage.name+'-failed'))
            backup.rename(target)
        marker.unlink(missing_ok=True)
        raise

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--config',type=Path,default=ROOT/'local/config.json')
    parser.add_argument('--apply',action='store_true')
    parser.add_argument('--expected-source');parser.add_argument('--expected-runtime')
    args=parser.parse_args()
    config=json.loads(args.config.read_text());target=Path(config['runtime_dir']).expanduser()
    if not target.is_absolute(): parser.error('runtime_dir must be absolute')
    if args.apply:
        if not args.expected_source or not args.expected_runtime:parser.error('Apply requires both reviewed hashes')
        result=apply(ROOT/'Mod',target,args.expected_source,args.expected_runtime)
    else: result=check(ROOT/'Mod',target)
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
