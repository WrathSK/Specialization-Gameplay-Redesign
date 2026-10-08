"""Read-only structural inventory. Not a Lua execution/call graph or loaded-DB proof."""
import argparse,hashlib,json,re,subprocess
from pathlib import Path
import xml.etree.ElementTree as E
ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--output',type=Path,required=True);args=ap.parse_args()
repo=args.repo.resolve();mod=repo/'Mod';info=mod/'SpecializationP0.modinfo';tree=E.parse(info).getroot()
files=[x.text for x in tree.find('Files') if x.tag=='File']
assert all(isinstance(x,str) for x in files)
assert all((mod/x).resolve().is_relative_to(mod.resolve()) for x in files)
actions=[]
for group in ['FrontEndActions','InGameActions']:
 for a in tree.find(group):
  props={x.tag:x.text for x in a.find('Properties')} if a.find('Properties') is not None else {}
  actions.append({'group':group,'kind':a.tag,'id':a.get('id'),'files':[x.text for x in a.iter('File')],'properties':props})
# XML context paired Lua is a structural candidate, not proof of engine load order.
roots={ 'Gameplay.lua' }
for a in actions:
 if a['kind']=='AddUserInterfaces': roots.update(str(Path(x).with_suffix('.lua')) for x in a['files'])
 if a['kind']=='ReplaceUIScript': roots.add(a['properties']['LuaReplace'])
by_stem={}
for f in files:
 if f.endswith('.lua'):by_stem.setdefault(Path(f).stem,[]).append(f)
includes=[];starts=[];registrations=[];dynamic=[]
for f in files:
 if not f.endswith('.lua'):continue
 raw=(mod/f).read_bytes();txt=raw.decode('utf-8')
 # Strip comments preserving newline positions. No parsing/evaluation of Lua strings or branch conditions.
 txt=re.sub(r'--\[\[(.*?)\]\]',lambda m:'\n'*m.group(0).count('\n'),txt,flags=re.S)
 txt=re.sub(r'(?m)^\s*--[^\n]*','',txt)
 matches=list(re.finditer(r'\binclude\s*\(\s*([\'\"])(.*?)\1\s*\)',txt))
 for m in matches:
  name=m[2];candidates=by_stem.get(Path(name).stem,[]) if '/' not in name else ([name+'.lua'] if name+'.lua' in files else [])
  includes.append({'file':f,'line':txt.count('\n',0,m.start())+1,'name':name,'candidates':candidates})
 if len(re.findall(r'\binclude\s*\(',txt))!=len(matches):dynamic.append(f)
 for m in re.finditer(r'\b(SPC\w+)\.Start\s*\(',txt):starts.append({'file':f,'line':txt.count('\n',0,m.start())+1,'symbol':m[1]})
 for m in re.finditer(r'\bRegister(Exit|Return)\s*\(\s*([\'\"])(.*?)\2',txt):registrations.append({'file':f,'line':txt.count('\n',0,m.start())+1,'kind':m[1],'name':m[3]})
seen=set();todo=list(roots)
while todo:
 f=todo.pop()
 if f in seen:continue
 seen.add(f)
 for e in includes:
  if e['file']==f:todo.extend(e['candidates'])
# Exact declaration inventory only, no generated SQL evaluation or native DB mutation.
registered_sql=sorted({f for a in actions for f in a['files'] if f and f.endswith('.sql')})

result={'head':subprocess.check_output(['git','rev-parse','HEAD'],cwd=repo,text=True).strip(),'limits':['Literal structural includes include branch-limited/manual paths; not runtime execution reachability.','XML paired Lua candidates and external game/mod includes require manual contract review.','SQL source availability is not loaded catalog, native effect or cleanup proof.'], 'modinfo_sha256':hashlib.sha256(info.read_bytes()).hexdigest(),'registered_count':len(files),'duplicate_files':len(files)-len(set(files)), 'missing_files':[f for f in files if not (mod/f).is_file()],'actions':actions,'roots':sorted(roots),'literal_candidates_reachable':sorted(seen),'registered_lua_outside_literal_candidates':sorted(set(by_stem_f for values in by_stem.values() for by_stem_f in values)-seen),'includes':includes,'nonliteral_include_files':dynamic,'start_call_locations':starts,'lifecycle_registration_locations':registrations,'registered_sql':registered_sql,'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
args.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'registered':len(files),'missing':result['missing_files'],'duplicate':result['duplicate_files'],'roots':len(roots),'literal_candidates':len(seen),'outside_literal_candidates':len(result['registered_lua_outside_literal_candidates']),'nonliteral_include_files':dynamic,'sql':len(registered_sql),'raw_result_bytes':args.output.stat().st_size}))
