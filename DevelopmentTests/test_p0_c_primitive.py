"""P0-C pre-cutover gate. Actual shared Lua + offline SQL; NOT an engine test.
No file in this fixture is a runtime component. This test cannot certify native
specialist scope, implement retirement, or mark P0-C complete.
"""
from pathlib import Path
import ast, json, sqlite3, subprocess
R=Path(__file__).resolve().parents[1]
F=R/'DevelopmentTests/Fixtures/P0C'
source=R/'DevelopmentTests/test_p0_a.py'
tree=ast.parse(source.read_text())
kept=[n for n in tree.body if isinstance(n,(ast.Import,ast.ImportFrom,ast.FunctionDef)) or isinstance(n,ast.Assign) and all(isinstance(t,ast.Name) and t.id in {'R','M','NEW','FIX'} for t in n.targets)]
ns={'__file__':str(source)}
exec(compile(ast.Module(body=kept,type_ignores=[]),str(source),'exec'),ns)
chains=[([],0),(['LIBRARY'],1),(['LIBRARY','UNIVERSITY'],3),(['LIBRARY','UNIVERSITY','JNR_LABORATORY'],6),(['LIBRARY','UNIVERSITY','JNR_LABORATORY','RESEARCH_LAB'],10)]
l=ns['runtime']();count=0
for names,depth in chains:
 for workers in [0,1,2,5]:
  for active in range(5):
   l.globals().names=ns['to_lua'](l,['BUILDING_'+n for n in names])
   l.execute(f"setBuildings(d,names);d.workers={workers};c.active={active};svc.MarkDirty();local f=SPCCurrentSpecializationFacts.Read(P,shared,0,c);local v=svc.Read(0,c,f.token);local plan=SPCResearchInfrastructureShadow.Plan(SPCResearchInfrastructureShadow.WithWorkers(f,v),v);assert(plan.science=={depth*workers if active==4 else 0});assert(writes==0)")
   count+=1
print('LOCAL_SIMULATION_PASS actual shared Lua: D x workers x ACTIVE',count,'cases; writes=0')
l=ns['runtime']()
l.execute("setBuildings(d,{'BUILDING_LIBRARY','BUILDING_UNIVERSITY'});d.workers=2;d2=addDistrict(c,12,'DISTRICT_SEOWON');setBuildings(d2,{'BUILDING_JNR_LABORATORY','BUILDING_RESEARCH_LAB'});d2.workers=3;svc.MarkDirty();local f=SPCCurrentSpecializationFacts.Read(P,shared,0,c);v=svc.Read(0,c,f.token);p=SPCResearchInfrastructureShadow.Plan(SPCResearchInfrastructureShadow.WithWorkers(f,v),v);assert(p.d==7 and p.workers==5 and p.science==35 and p.selectedDistrict==12);assert(writes==0)")
# A deliberately restricted hypothetical carrier would give21 or14, not35.
# This is a countermodel explaining missing evidence, NOT predicted engine behavior.
assert 7*3!=35 and 7*2!=35
l.execute("d2.pillaged=true;svc.MarkDirty();local f=SPCCurrentSpecializationFacts.Read(P,shared,0,c);v=svc.Read(0,c,f.token);p=SPCResearchInfrastructureShadow.Plan(SPCResearchInfrastructureShadow.WithWorkers(f,v),v);assert(p.d==3 and p.workers==2 and p.science==6);d.workers=nil;p=SPCResearchInfrastructureShadow.Plan(SPCResearchInfrastructureShadow.WithWorkers(f,v),v);assert(p.status=='UNKNOWN_WORKERS' and p.science==nil and writes==0)")
print('LOCAL_SIMULATION_PASS multi-Campus expected35, pillaged excluded6, worker UNKNOWN not zero; native coverage NOT tested')
evidence=json.loads((F/'primitive_evidence.json').read_text())
c=sqlite3.connect(':memory:')
for row in evidence['queries'][2]['rows']:c.execute(row[0])
# Native Types hashes are assigned by the engine; fixture substitutes unique IDs,
# not a claim to reproduce Civ VI hashing. Foreign dependency tables are not loaded.
c.execute('CREATE TRIGGER fixture_type_hash AFTER INSERT ON Types BEGIN UPDATE Types SET Hash=NEW.rowid WHERE Type=NEW.Type; END')
c.executescript((F/'research_science_candidate.sql').read_text())
rows=c.execute('select YieldChange from Building_CitizenYieldChanges order by YieldChange').fetchall()
assert rows==[(1,),(2,),(4,),(8,)]
for d in range(11):assert sum(row[0] for bit,row in enumerate(rows) if d&(1<<bit))==d
assert c.execute('select count(*) from Buildings where CitizenSlots!=0 or InternalOnly!=1').fetchone()[0]==0
print('LOCAL_SQL_PASS candidate citizen Science bits represent D0..10; NOT native placement/settlement')
base='20e058861d071663d6d880e71aa9d3495e8027ab'
for folder in ['Mod','Specialization/Design']:
 tracked=subprocess.check_output(['git','ls-tree','-r','--name-only',base,folder],cwd=R,text=True).splitlines()
 for name in tracked:
  assert (R/name).read_bytes()==subprocess.check_output(['git','show',base+':'+name],cwd=R),name
assert 'research_science_candidate' not in (R/'Mod/SpecializationP0.modinfo').read_text()
print('INTEGRITY_PASS runtime and Design unchanged; no cutover, no new carrier enabled')
print('GATE: TECHNICAL_INVESTIGATION_REQUIRED; P0-C implementation NOT COMPLETE')
