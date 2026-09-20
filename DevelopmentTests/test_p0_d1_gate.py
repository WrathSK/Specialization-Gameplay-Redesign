"""P0-D1 pre-cutover gate. Actual candidate Lua; no Civ VI interaction.
Passing this suite proves exact plans and rejection of unverified primitives,
NOT that the native settlement gate passed.
"""
from pathlib import Path
import hashlib,json,subprocess,sqlite3
from lupa.lua55 import LuaRuntime
R=Path(__file__).resolve().parents[1]
F=R/'DevelopmentTests/Fixtures/P0D1'
l=LuaRuntime(unpack_returned_tuples=True)
l.execute((F/'ResearchCrossModel.lua').read_text())
l.execute('''
M=SPCResearchCrossModel
function row(domain,n)
 local v={};for _,y in ipairs(M.Yields) do v[y]=0 end;v.PRODUCTION=n
 return {reference=domain,type=domain,domain=domain,complete=true,pillaged=false,yields=v}
end
f={validity='VERIFIED',identity='RESEARCH',active=3,potential=4}
function equal(a,b) assert(math.abs(a-b)<1e-12,tostring(a)..' != '..tostring(b)) end
''')
# All nine source domains and all six input yields; actual yield, D, population,
# specialist values are deliberately irrelevant extras, never read by the model.
l.execute('''
local rows={};local total=0
for domain in pairs(M.Domains) do
 local r=row(domain,0)
 for i,y in ipairs(M.Yields) do r.yields[y]=i end
 r.actual=999;r.d=10;r.population=20;r.workers=5
 rows[#rows+1]=r;total=total+21
end
local p=M.Plan(f,rows);assert(p.count==9);equal(p.science,total/2)
for _,r in ipairs(rows) do r.actual=999999;r.d=0;r.population=1;r.workers=0 end
equal(M.Plan(f,rows).science,total/2)
assert(M.Domain('UNIQUE_HOLY',{UNIQUE_HOLY='DISTRICT_HOLY_SITE'})=='DISTRICT_HOLY_SITE')
assert(M.Domain('DISTRICT_CAMPUS',{})==nil and M.Domain('FUTURE_UNKNOWN',{})==nil)
assert(not pcall(M.Domain,'A',{A='B',B='A'}))
local a=row('DISTRICT_NEIGHBORHOOD',2);local b=row('DISTRICT_NEIGHBORHOOD',3);b.reference='second'
equal(M.Plan(f,{a,b}).science,2.5)
a.pillaged=true;equal(M.Plan(f,{a,b}).science,1.5)
b.complete=false;equal(M.Plan(f,{a,b}).science,0)
a.pillaged=nil;assert(not pcall(M.Plan,f,{a}))
local excluded=row('DISTRICT_CAMPUS',100);excluded.yields=nil
equal(M.Plan(f,{excluded}).science,0)
for _,active in ipairs({0,1,2,3,4}) do
 f.active=active;equal(M.Plan(f,{row('DISTRICT_THEATER',7)}).science,active>=3 and 3.5 or 0)
end
f.active=3;f.identity='INDUSTRY';equal(M.Plan(f,nil).science,0)
f.identity='RESEARCH';f.validity='UNKNOWN';assert(not pcall(M.Plan,f,{}));f.validity='VERIFIED'
assert(not pcall(M.Plan,f,nil))
local missing=row('DISTRICT_THEATER',1);missing.yields.SCIENCE=nil;assert(not pcall(M.Plan,f,{missing}))
assert(not pcall(M.Plan,f,{missing,missing}))
for _,v in ipairs({0,1,2,7,0.5,1.3,-1}) do equal(M.Plan(f,{row('DISTRICT_THEATER',v)}).science,v*0.5) end
''')
print('PASS exact formula, nine domains/six yields, eligibility, multi-Neighborhood, unknown != zero; no D/pop/workers/actual coupling')
l.execute('''
for pop=1,255 do for _,amount in ipairs({0,0.5,1,1.5,3.5,100.5,65535.5}) do
 local p=assert(M.ExistingPrimitive(amount,pop));equal(p.integer+(p.coefficient or 0)*pop,amount)
end end
for _,v in ipairs({0.25,0.65,-0.5,65536}) do
 local p,why=M.ExistingPrimitive(v,3);assert(p==nil and why=='CROSS_NATIVE_PRECISION_UNVERIFIED')
end
assert(M.ExistingPrimitive(0.5,256)==nil)
-- This is a failed primitive gate correctly detected, not Gameplay PASS.
local a=M.Plan(f,{row('DISTRICT_THEATER',0.5)})
local b=M.Plan(f,{row('DISTRICT_THEATER',1.3)})
equal(a.science,0.25);equal(b.science,0.65)
assert(M.ExistingPrimitive(a.science,3)==nil and M.ExistingPrimitive(b.science,3)==nil)
''')
print('PASS 1785 existing primitive decompositions; UNVERIFIED gate retained for finer fractions/negative/range, never rounded')
# SQL enumerates exact old Research writer; no mutation of external databases.
db=sqlite3.connect(':memory:')
db.executescript('CREATE TABLE Building_CitizenYieldChanges(BuildingType,YieldType,YieldChange); CREATE TABLE Types(Type,Kind); CREATE TABLE Buildings(BuildingType,Name,Cost,PrereqDistrict,InternalOnly,CitizenSlots,Housing); CREATE TABLE Modifiers(ModifierId,ModifierType); CREATE TABLE ModifierArguments(ModifierId,Name,Value); CREATE TABLE BuildingModifiers(BuildingType,ModifierId);')
db.executescript((R/'Mod/Data/Lv3Effects.sql').read_text())
old=[f'BUILDING_SPC_DEV_LV3_POP_RESEARCH_{i}' for i in range(8)]
for i,n in enumerate(old):
 assert db.execute('select ModifierId from BuildingModifiers where BuildingType=?',(n,)).fetchall()==[(f'SPC_LV3_POP_RESEARCH_{i}',)]
 assert float(db.execute("select Value from ModifierArguments where ModifierId=? and Name='Amount'",(f'SPC_LV3_POP_RESEARCH_{i}',)).fetchone()[0])==0.5*2**i
baseline='86a67bc0a73d952a80088d6e48f7189d0815d606'
for sub in ['Mod','Specialization/Design']:
 subprocess.run(['git','diff','--exit-code',baseline,'--',sub],cwd=R,check=True)
 listed=set(subprocess.check_output(['git','ls-tree','-r','--name-only',baseline,'--',sub],cwd=R,text=True).splitlines())
 actual={p.relative_to(R).as_posix() for p in (R/sub).rglob('*') if p.is_file() and p.name!='.DS_Store'}
 assert actual==listed,(sub,actual^listed)
print('PASS exact8 old SQL effects retained; all Mod/Design tracked bytes and file sets unchanged from86a67bc')
print('LOCAL_SIMULATION_PASS pre-cutover candidate only; NATIVE_GATE=TECHNICAL_INVESTIGATION_REQUIRED; P0-D1 NOT COMPLETE')
