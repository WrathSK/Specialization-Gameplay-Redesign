"""P0-D1 actual Lua lifecycle/writer + formula; native engine remains user gate."""
from pathlib import Path
from lupa.lua55 import LuaRuntime
R=Path(__file__).resolve().parents[1];M=R/'Mod'
s=(R/'DevelopmentTests/test_arch_v2_c2.py').read_text()
FIX=s.split('FIX=r"""')[1].split('"""')[0]
SETUP=r"""
SPCDistrictCompleteness={Clone=clone};P.Rows=function() return {} end
reads=0
for _,c in pairs(cities) do
 setmetatable(c.built,{__index={IsPillaged=function() return false end}})
 c.GetDistricts=function()
  local list={};for _,x in pairs(districts) do if x.cid==c.id then list[#list+1]=x end end;table.sort(list,function(a,b) return a.id<b.id end)
  return {GetNumDistricts=function() return #list end,GetDistrictByIndex=function(_,i) return list[i+1] end}
 end
end
for _,d in pairs(districts) do d.pillaged=false;d.IsPillaged=function() return d.pillaged end end
Map.GetPlot=function(x) return {GetAdjacencyYield=function(_,pid,cid,kind,y)
 reads=reads+1;if unavailable then error('NATIVE_NOT_READY') end
 return y=='CULTURE' and districts[x].base or 0
end} end
"""
def runtime():
 l=LuaRuntime(unpack_returned_tuples=True)
 l.globals().include=lambda n: None if n=='Probe' else l.execute((M/(n+'.lua')).read_text())
 l.execute(FIX);l.execute(SETUP)
 l.execute((M/'PerformanceCounters.lua').read_text());l.execute('ExposedMembers.SPC_Performance=SPCPerformance.New();P.Count=SPCPerformance.Count')
 l.execute((M/'CurrentSpecializationFacts.lua').read_text())
 l.execute((M/'ResearchCross.lua').read_text());l.execute('SPCResearchCross.Start(P,shared);d=shared.ResearchCross;d.ready=true')
 l.execute((M/'UI/ResearchCrossRefresh.lua').read_text())
 return l
l=runtime();l.execute(r"""
initUI();assert(sends==1);local p=queue[1];local rd=reads
pulse(10000);assert(sends==1 and reads==rd and writes==0)
d.Receive(0,p);pulse();assert(total('cross_apply')==1 and writes==2 and next(d.errors[0])==nil)
local w=writes;local scans=total('district_scan');rd=reads
pulse(10000);for i=1,10000 do tick(.1) end
assert(sends==1 and reads==rd and writes==w and total('district_scan')==scans)
d.Receive(0,p);assert(writes==w and total('cross_apply')==1)
assert(d.Describe(0,cities[1],true):find('BASE'))
-- New BASE, old packet cannot replace latest; final floor 7*.5 -> 3, zero writes.
districts[13].base=7;fire('FeatureAddedToMap');pulse();local p2=queue[#queue]
d.Receive(0,p);d.Receive(0,p2);pulse();assert(writes==w and total('cross_apply')==2)
-- Unavailable preserves last verified carrier; bounded three attempts.
unavailable=true;fire('FeatureRemovedFromMap');pulse()
for i=1,10 do d.Receive(0,queue[#queue]);tick(6);pulse(1000) end
assert(writes==w and sends==5)
-- Confirmed invalid Campus withdraws even with missing other samples.
d.samples[0]=nil;districts[11].pillaged=true;d.Audit();assert(writes==w+2 and total('cross_withdraw')==1)
d.Audit();assert(writes==w+2 and total('cross_withdraw')==1)
districts[11].pillaged=false;d.Audit();assert(writes==w+2)
unavailable=false;turn=2;fire('PlayerTurnActivated');pulse();d.Receive(0,queue[#queue]);pulse();assert(next(d.errors[0])==nil)
local old=queue[#queue];fire('LoadScreenClose');d.Receive(0,old);assert(total('cross_stale')>0)
-- Current reference change rejects in-flight sample.
turn=3;fire('PlayerTurnActivated');pulse();local pkt=queue[#queue];cities[1].token='NEW';local a=total('cross_apply');d.Receive(0,pkt);assert(total('cross_apply')==a)
-- Exact retirement even while current sample unavailable.
for _,n in ipairs(SPCResearchCross.Retired) do cities[1].built[n]=true end
d.Audit();for _,n in ipairs(SPCResearchCross.Retired) do assert(not cities[1].built[n]) end
facts[1].active=2;d.Audit();assert(next(d.errors[0])==nil)
""")
print('PASS actual producer/receiver/writer: 10k pending + 10k clean + 10k timer, floor/idempotence/unknown/withdraw/epoch/reference/exact retirement')
for throwing in [False,True]:
 l=runtime();l.execute('failSend='+str(throwing).lower()+';initUI();for i=1,20 do tick(6);pulse(1000) end;assert(sends==3 and writes==0)')
print('PASS max3 requests for timeout and transport exception')
l=runtime();l.execute(r"""
sync=true;districts[13].base=-3;initUI();pulse();assert(cities[1].built.BUILDING_SPC_RESEARCH_CROSS_NEG_1 and next(d.errors[0])==nil)
local w=writes;factUnknown=true;d.Audit();assert(writes==w)
factUnknown=false;districts[13].base=0;fire('FeatureAddedToMap');pulse();assert(writes==w+1 and total('cross_withdraw')==1)
d.Audit();assert(writes==w+1)
-- Complete replacement verified zero differs from temporary unavailable.
local before=total('cross_apply');turn=2;sync=false;fire('PlayerTurnActivated');pulse()
local bad=clone(queue[#queue]);bad.Count=999;d.Receive(0,bad);assert(total('cross_apply')==before)
""")
print('PASS signed floor encoding / UNKNOWN facts HOLD / verified zero withdrawal once / malformed atomic reject')

l=runtime();l.execute(r"""
local f={validity='VERIFIED',identity='RESEARCH',potential=4,active=3}
local rows={}
for i,kind in ipairs({'DISTRICT_INDUSTRIAL_ZONE','DISTRICT_ENCAMPMENT','DISTRICT_THEATER','DISTRICT_GOVERNMENT','DISTRICT_DIPLOMATIC_QUARTER','DISTRICT_COMMERCIAL_HUB','DISTRICT_HARBOR','DISTRICT_HOLY_SITE','DISTRICT_NEIGHBORHOOD'}) do
 local ys={};for _,y in ipairs(SPCResearchCrossModel.Yields) do ys[y]=.1 end
 rows[i]={reference='R'..i,type=kind,domain=kind,complete=true,pillaged=false,yields=ys}
end
local p=SPCResearchCrossModel.Plan(f,rows);assert(p.count==9 and math.abs(p.rawScience-2.7)<1e-9 and p.science==2)
rows[1].pillaged=true;rows[2].complete=false;p=SPCResearchCrossModel.Plan(f,rows);assert(p.count==7 and p.science==2)
rows[3].domain=nil;p=SPCResearchCrossModel.Plan(f,rows);assert(p.count==6 and p.science==1)
assert(SPCResearchCrossModel.Domain('UNIQUE',{UNIQUE='DISTRICT_THEATER'})=='DISTRICT_THEATER')
f.active=2;assert(SPCResearchCrossModel.Plan(f,rows).science==0)
f.active=4;assert(SPCResearchCrossModel.Plan(f,rows).science==1)
""")
print('PASS nine domains/six yields, exclusions, unique, ACTIVE III/IV and floor-after-total')
for p in M.rglob('*.lua'):
 err=l.eval('function(s) local f,e=load(s);return e end')(p.read_text());assert err is None,(p,err)
print('PASS all Lua compile')

# Scaling: complete actual producer -> verified receiver -> city writer, two districts/city.
for n in [1,2,4,8]:
 l=runtime();l.globals().n=n;l.execute(r"""
 cities={};districts={};facts={}
 for id=1,n do
  local c={id=id,owner=0,token='C'..id,built={}}
  c.GetID=function() return id end;c.GetOwner=function() return 0 end;c.GetX=function() return id end;c.GetY=function() return 1 end
  c.GetProperty=function() return c.token end;c.GetBuildings=function() return c.built end;c.GetBuildQueue=function() return c.built end
  setmetatable(c.built,{__index={IsPillaged=function() return false end}});cities[id]=c
  local a=district(id*10,id,'DISTRICT_CAMPUS',0);local b=district(id*10+1,id,'DISTRICT_THEATER',0)
  a.IsPillaged=function() return false end;b.IsPillaged=a.IsPillaged
  c.GetDistricts=function() return {GetNumDistricts=function() return 2 end,GetDistrictByIndex=function(_,i) return i==0 and a or b end} end
  facts[id]={specialization='RESEARCH',active=3,potential=3,first={districtID=id*10}}
 end
 sync=true;initUI();pulse();assert(sends==1 and reads==6*n and total('city_scan')==n and writes==2*n)
 for _,e in pairs(d.errors[0]) do error(e) end
 local rd,w,sc=reads,writes,total('district_scan');pulse(10000);assert(reads==rd and writes==w and total('district_scan')==sc and sends==1)
 """)
 print('SCALING cities/base getters/district scans/writes:',n,l.eval('reads'),l.eval('total("district_scan")'),l.eval('writes'))
# Exact SQL retirement + protected non-Research rows.
import sqlite3,subprocess,xml.etree.ElementTree as ET,ast,json,zlib
schema='CREATE TABLE Building_CitizenYieldChanges(BuildingType TEXT,YieldType TEXT,YieldChange INTEGER);CREATE TABLE Types(Type TEXT,Kind TEXT);CREATE TABLE Buildings(BuildingType TEXT,Name TEXT,Cost INTEGER,PrereqDistrict TEXT,InternalOnly INTEGER,CitizenSlots INTEGER,Housing INTEGER);CREATE TABLE Modifiers(ModifierId TEXT,ModifierType TEXT,SubjectRequirementSetId TEXT);CREATE TABLE ModifierArguments(ModifierId TEXT,Name TEXT,Value TEXT);CREATE TABLE BuildingModifiers(BuildingType TEXT,ModifierId TEXT);'
a,b=sqlite3.connect(':memory:'),sqlite3.connect(':memory:')
for db in [a,b]:db.executescript(schema)
a.executescript(subprocess.check_output(['git','show','a8ee1f9:Mod/Data/Lv3Effects.sql'],cwd=R,text=True));b.executescript((M/'Data/Lv3Effects.sql').read_text())
for t in ['Building_CitizenYieldChanges','Types','Buildings','Modifiers','ModifierArguments','BuildingModifiers']:
 expected=[row for row in a.execute('select * from '+t) if not any('SPC_LV3_POP_RESEARCH_' in str(v) for v in row)]
 assert sorted(expected)==sorted(b.execute('select * from '+t)),t
for i in range(8):assert b.execute('select count(*) from Buildings where BuildingType=?',(f'BUILDING_SPC_DEV_LV3_POP_RESEARCH_{i}',)).fetchone()[0]==1
cfg=json.loads((R.parent/'Specialization-Gameplay-Redesign/local/config.json').read_text())
source=sqlite3.connect('file:'+cfg['debug_gameplay_db']+'?mode=ro',uri=True);db=sqlite3.connect(':memory:');source.backup(db);source.close();db.create_function('Make_Hash',1,lambda s:zlib.crc32(s.encode()))
# Remove only this module's rows from disposable memory copy, allowing later reruns.
for sign in ['POS','NEG']:
 for i in range(16):
  mid=f'SPC_RESEARCH_CROSS_{sign}_{i}';bid='BUILDING_'+mid
  for table,col,key in [('BuildingModifiers','BuildingType',bid),('ModifierArguments','ModifierId',mid),('Modifiers','ModifierId',mid),('Buildings','BuildingType',bid),('Types','Type',bid)]:db.execute(f'delete from {table} where {col}=?',(key,))
for rid, in list(db.execute("select RequirementId from Requirements where RequirementId like 'SPC_CROSS_%'")):
 for table in ['RequirementArguments','RequirementSetRequirements','Requirements']:db.execute(f'delete from {table} where RequirementId=?',(rid,))
db.execute("delete from RequirementSets where RequirementSetId='SPC_CROSS_CAMPUS'")
db.executescript((M/'Data/ResearchCross.sql').read_text())
assert db.execute("select count(*) from BuildingModifiers where BuildingType like 'BUILDING_SPC_RESEARCH_CROSS_%'").fetchone()[0]==32
for sign in ['POS','NEG']:
 for i in range(16):
  mid=f'SPC_RESEARCH_CROSS_{sign}_{i}'
  assert db.execute('select ModifierType,SubjectRequirementSetId from Modifiers where ModifierId=?',(mid,)).fetchone()==('MODIFIER_CITY_DISTRICTS_ADJUST_YIELD_CHANGE','SPC_CROSS_CAMPUS')
  assert float(db.execute("select Value from ModifierArguments where ModifierId=? and Name='Amount'",(mid,)).fetchone()[0])==(1 if sign=='POS' else -1)*2**i
assert db.execute("select count(*) from RequirementSetRequirements where RequirementSetId='SPC_CROSS_CAMPUS'").fetchone()[0]>0
assert 'INSERT INTO Modifiers' not in (M/'Data/DistrictPrecisionProbe.sql').read_text()
assert 'SPCDistrictPrecisionProbe.Start' not in (M/'Gameplay.lua').read_text()
print('PASS exact8 SQL retirement; every other old Lv3 row identical; native-schema 32 signed Campus district modifiers; experiment inert')
x=ET.parse(M/'SpecializationP0.modinfo').getroot();assert x.get('version')=='111'
files=[e.text for e in x.findall('./Files/File')];assert len(files)==len(set(files));assert set(files)=={p.relative_to(M).as_posix() for p in M.rglob('*') if p.is_file() and p.name!='SpecializationP0.modinfo'}
subprocess.run(['git','diff','--exit-code','a8ee1f9','--','Specialization/Design'],cwd=R,check=True)
# Actual UI explicit caption, action split and idle cost.
t=ast.parse((R/'DevelopmentTests/test_arch_v2_d2.py').read_text());fix=next(ast.literal_eval(x.value) for x in t.body if isinstance(x,ast.Assign) and any(isinstance(k,ast.Name) and k.id=='UI_FIX' for k in x.targets))
u=LuaRuntime();u.execute(fix)
u.execute("Mouse.eRClick=2;P.Scalar=tostring;print=function() end;clicks={};Controls.DPReadButton.RegisterCallback=function(c,e,f) clicks[e]=f end;Controls.DPReadButtonCaption.SetText=function(c,t) label=t end;UI.RequestPlayerOperation=function(pid,op,p) sends=sends+1;last=p.Action end")
u.execute((M/'UI/P0Panel.lua').read_text());u.execute("init();assert(label=='跨学科研究');clicks[1]();assert(last=='RESEARCH_CROSS_READ');clicks[2]();assert(last=='RESEARCH_CROSS_DETAIL');for i=1,10000 do fire('SystemUpdateUI') end;assert(sends==2)")
print('PASS actual caption/summary/detail/idle; manifest exact files; Design unchanged')
