#!/usr/bin/env python3
"""Read-only W0001 context navigation. No refresh/write/test/deploy command."""
import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent

def load(name):
    return json.loads((HERE / name).read_text())

def path(rel):
    p = ROOT / rel
    if Path(rel).is_absolute() or '..' in Path(rel).parts or p.is_symlink():
        raise ValueError('unsafe reference: ' + rel)
    if ROOT not in p.resolve().parents:
        raise ValueError('outside repo: ' + rel)
    return p

def project(ref):
    p = path(ref['path'])
    return project_text(ref, p.read_text())

def project_text(ref, text):
    """Pure selector projection; shared by repository reads and deterministic fixtures."""
    kind, selector = ref['kind'], ref.get('selector')
    lines = text.splitlines(keepends=True)
    if kind == 'full': return text
    if kind == 'head':
        if type(selector) is not int or not 0 < selector <= len(lines):
            raise ValueError('invalid head selector')
        return ''.join(lines[:selector])
    if kind == 'section':
        if not isinstance(selector, str) or not re.match(r'^#{1,6} .+', selector):
            raise ValueError('invalid heading selector')
        hits = [i for i, line in enumerate(lines) if line.rstrip() == selector]
        if len(hits) != 1: raise ValueError('missing/duplicate heading: ' + selector)
        start = hits[0]
        depth = len(selector) - len(selector.lstrip('#'))
        end = len(lines)
        for i in range(start + 1, len(lines)):
            m = re.match(r'^(#{1,6}) ', lines[i])
            if m and len(m[1]) <= depth: end = i; break
        return ''.join(lines[start:end])
    if kind == 'rows':
        if not isinstance(selector, list) or not selector or any(not isinstance(p, str) or not p for p in selector):
            raise ValueError('invalid rows selector')
        result = []
        for prefix in selector:
            hits = [line for line in lines if line.startswith(prefix)]
            if len(hits) != 1: raise ValueError('missing/duplicate row: ' + prefix)
            result += hits
        return ''.join(result)
    if kind == 'json':
        data = json.loads(text)
        value = data
        if not isinstance(selector, str) or not selector.startswith('/'): raise ValueError('expected JSON Pointer')
        for token in selector.split('/')[1:]:
            token = token.replace('~1', '/').replace('~0', '~')
            value = value[int(token)] if isinstance(value, list) else value[token]
        if 'expected_id' in ref:
            objects = value if isinstance(value, list) else [value]
            hits = [v for v in objects if isinstance(v, dict) and ref['expected_id'] in
                    [v.get('effect_id'), v.get('ability_id'), v.get('rule_id')]]
            if len(hits) != 1: raise ValueError('stable ID mismatch')
        meta = {k:data[k] for k in ('design_revision','document_state','freeze_status',
                  'authority','shared_contract_ref','implementation_status') if k in data}
        return json.dumps({'authority_metadata':meta,'pointer':selector,'value':value},
                          ensure_ascii=False,indent=2)+'\n'
    raise ValueError('unsupported kind: '+kind)

def validate_manifest(m, authority):
    required = load('Batch.schema.json')['required']
    if any(k not in m for k in required): raise ValueError('missing manifest field')
    if m['schema_version'] != 1 or m['authority_versions'] != authority['versions']:
        raise ValueError('stale manifest authority/schema')
    allowed = load('Batch.schema.json')['properties']['status']['enum']
    if m['status'] not in allowed: raise ValueError('invalid manifest status')
    if not m['old_writers'] or not m['validation'] or not m['full_audit_triggers']:
        raise ValueError('missing writer/validation/audit gate')
    for r in m['context']:
        if any(k not in r for k in ('path','kind','reason')): raise ValueError('incomplete ref')
        project(r)

def compare(expected, actual, label):
    errors = []
    for p in sorted(set(expected) | set(actual)):
        if p not in expected: errors.append(label+' unindexed/new '+p)
        elif p not in actual: errors.append(label+' missing '+p)
        elif expected[p] != actual[p]: errors.append(label+' changed '+p)
    return errors

def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()

def check(m):
    a = load('Authority.json'); validate_manifest(m,a)
    errors=[]
    index=load('Runtime_Index.json')
    expected={p:v['sha256'] for p,v in index['files'].items()}
    actual={str(p.relative_to(ROOT)):digest(p) for p in (ROOT/'Mod').rglob('*')
            if p.is_file() and p.name!='.DS_Store'}
    errors += compare(expected,actual,'runtime')
    lock=load('Context_Lock.json')['files']
    actual_lock={p:digest(path(p)) for p in lock if path(p).is_file()}
    errors += compare(lock,actual_lock,'context')
    for ref in m['context']:
        if '/Workflow/' not in ref['path'] and ref['path'] not in lock:
            errors.append('unlocked ref '+ref['path'])
    # Content revision plus pointer linkage, not just a matching caller-supplied version map.
    for key in ('research','industry','culture','commerce','shared'):
        d=json.loads(path(a['paths'][key]).read_text())
        if d['design_revision'] != a['versions'][key]: errors.append('revision '+key)
    for key,prefix in [('design','Design Revision:'),('architecture','Architecture Revision:'),('status','Status Revision:')]:
        if prefix+' '+a['versions'][key] not in path(a['paths'][key]).read_text():
            errors.append('header revision '+key)
    for p,v in index['files'].items():
        if not path(v['review_source']).is_file(): errors.append('summary missing '+p)
    branch=subprocess.check_output(['git','branch','--show-current'],cwd=ROOT,text=True).strip()
    if branch!='develop': errors.append('not develop: '+branch)
    if errors: raise ValueError('\n'.join(errors))
    return {'check':'PASS','runtime_files':len(expected),'guarded_context_files':len(lock),
            'batch':m['batch'],'implementation_authorized':False,
            'note':'Reference integrity only; explicit user authorization and semantic review still required.'}

def plan(m):
    rows=[]
    for n,r in enumerate(m['context']):
        t=project(r);rows.append(dict(n=n,path=r['path'],kind=r['kind'],selector=r.get('selector'),
                                      bytes=len(t.encode()),lines=len(t.splitlines())))
    old=set(p for p in (ROOT/'Mod').rglob('*') if p.is_file() and p.name!='.DS_Store')
    old.update(p for p in (ROOT/'Specialization/Architecture/v2').iterdir() if p.is_file())
    a=load('Authority.json')
    old.update(path(p) for p in a['paths'].values())
    old.update(path(p) for p in ['AGENTS.md','Specialization/AGENTS.md','Specialization/README.md',
       'Specialization/Design/Design_ChangeLog.md','Specialization/Design/Content/README.md',
       'Specialization/Architecture/Playtest_Workflow.md','DevelopmentTests/test_p0_a.py',
       'DevelopmentTests/test_arch_v2_d2.py'])
    return {'ordered_reads':rows,'proposed':{'files':len({x['path'] for x in rows}),
           'projections':len(rows),'bytes':sum(x['bytes'] for x in rows),'lines':sum(x['lines'] for x in rows)},
           'broad_reference':{'files':len(old),'bytes':sum(p.stat().st_size for p in old),
           'lines':sum(len(p.read_bytes().splitlines()) for p in old)},
           'measurement':'Text-context footprint proxy, not historical observed reads or token bill. Hash I/O still reads all Mod bytes.'}

def self_test(m):
    import copy
    a=load('Authority.json'); passed=[]
    def reject(name,fn):
        try: fn()
        except (ValueError,KeyError,IndexError,FileNotFoundError): passed.append(name);return
        raise AssertionError('failed to reject '+name)
    bad=copy.deepcopy(m);bad['authority_versions']['design']='D9999'
    reject('stale manifest',lambda:validate_manifest(bad,a))
    bad=copy.deepcopy(m);del bad['old_writers']
    reject('missing writer gate',lambda:validate_manifest(bad,a))
    # Generic selectors must not depend on the active task using any particular kind.
    doc = '# Fixture\n## Current\nbody\n### Child\nkept\n## History\nold\n'
    payload = json.dumps({'design_revision':'FIXTURE','rules':[{'rule_id':'R-1','value':3}]})
    def select(kind, selector=None, **extra):
        return project_text(dict(kind=kind, selector=selector, **extra),
                            payload if kind == 'json' else doc)
    assert select('full') == doc
    assert select('head', 1) == '# Fixture\n'
    assert select('section', '## Current') == '## Current\nbody\n### Child\nkept\n'
    assert select('rows', ['body']) == 'body\n'
    value = json.loads(select('json', '/rules/0', expected_id='R-1'))
    assert value['value']['value'] == 3 and value['authority_metadata']['design_revision'] == 'FIXTURE'
    passed.append('independent full/head/section/rows/JSON stable-ID fixtures')
    reject('invalid heading',lambda:select('section','## Missing'))
    reject('duplicate heading',lambda:project_text(dict(kind='section',selector='## Current'),doc+doc))
    reject('invalid head',lambda:select('head',0))
    reject('invalid rows',lambda:select('rows',[]))
    reject('missing row',lambda:select('rows',['absent']))
    reject('invalid pointer',lambda:select('json','/missing'))
    reject('stable ID mismatch',lambda:select('json','/rules',expected_id='WRONG'))
    reject('unsupported selector kind',lambda:select('unknown'))
    reject('path traversal',lambda:path('../outside'))
    reject('absolute path',lambda:path('/tmp/outside'))
    assert len(compare({'a':'old','b':'same'},{'a':'new','c':'new'},'test'))==3
    passed.append('changed/new/deleted file detection')
    check(m); passed.append('valid current manifest and all selectors')
    return {'self_test':'PASS','cases':passed,'filesystem_writes':0,'gameplay_tests_run':0}

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('command',choices=['check','plan','read','self-test'])
    p.add_argument('batch',choices=['P0-B1','P0-B2','P0-C','P0-D1','P0-D2','P0-D3','P0-U1','P0-E1','P0-E2','P0-F1','P0-F2','P0-K','P0-L1','P0-L2A','P0-L2B','P0-L2C','P0-L3A','P0-L3','Store-Write-Repair','Shared-D-Facts','P0-Panel-Cleanup','Investment-Propagation','P0-M1','P0-M2']);p.add_argument('item',nargs='?')
    args=p.parse_args();m=load(args.batch+'.json')
    if args.command=='check': result=check(m)
    elif args.command=='self-test': result=self_test(m)
    else:
        check(m)
        if args.command=='plan': result=plan(m)
        else:
            refs=m['context'] if args.item=='all' else [m['context'][int(args.item)]]
            for r in refs:
                print('\nSOURCE',r['path'],r.get('selector','FULL'))
                print(project(r))
            return
    print(json.dumps(result,ensure_ascii=False,indent=2))

if __name__=='__main__':
    try: main()
    except (ValueError,KeyError,IndexError,FileNotFoundError) as e:
        raise SystemExit('CONTEXT_INVALID: '+str(e))
