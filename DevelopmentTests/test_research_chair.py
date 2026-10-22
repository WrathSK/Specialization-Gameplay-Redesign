"""Actual P0-D3 Lua/SQL contracts. SQL projection oracle is NOT Civ VI engine."""
from pathlib import Path
import ast,json,sqlite3,subprocess,xml.etree.ElementTree as ET
from lupa.lua55 import LuaRuntime
R=Path(__file__).resolve().parents[1];M=R/'Mod'
ns={'__file__':str(R/'DevelopmentTests/test_p0_c.py')}
exec(compile((R/'DevelopmentTests/test_p0_c.py').read_text().split('chains=[')[0],'P0C_fixture','exec'),ns)
fixture=json.loads((R/'DevelopmentTests/Fixtures/P0A/catalog.json').read_text())
for b in fixture['rows']:
 ns['sql'].execute('insert into Buildings values (?,?,?,?,?,?,?)',(b['BuildingType'],b['BuildingType'],b['Cost'],b['PrereqDistrict'],0,0,0,))

ns['sql'].executescript((M/'Data/ResearchApply.sql').read_text())
ns['sql'].executescript((M/'Data/ResearchChair.sql').read_text())
ns['cr']=[dict(r,Index=10000+i,IsWonder=False) for i,r in enumerate(ns['sql'].execute('select * from Buildings where InternalOnly=1'))]
ns['yields']=[dict(r) for r in ns['sql'].execute('select * from Building_CitizenYieldChanges')]
tr=[dict(r) for r in ns['sql'].execute('select * from SPC_ResearchChairTargets')]
def runtime(n=1):
 l=ns['runtime'](n);l.globals().tr=ns['ns']['to_lua'](l,tr)
 l.execute("GameInfo.SPC_ResearchChairTargets=db(tr,'BuildingType')")
 for name in ['ResearchApply','ResearchChair']:
  l.execute((M/(name+'.lua')).read_text());l.execute(f'SPC{name}.Start(P,shared);shared.{name}.ready=true')
 l.execute("chair=shared.ResearchChair;function ca() chair.Audit();assert(not chair.definitionError,chair.definitionError);for _,e in pairs(chair.errors) do for _,v in pairs(e) do error(v) end end end;function cc(target,c) c=c or cities[1];local n=0;for i=0,7 do if c.carriers[GameInfo.Buildings['BUILDING_SPC_RESEARCH_CHAIR_'..target..'_'..i].Index] then n=n+2^i end end;return n end")
 return l
chains=[[],['LIBRARY'],['LIBRARY','UNIVERSITY'],['LIBRARY','UNIVERSITY','JNR_LABORATORY'],['LIBRARY','UNIVERSITY','JNR_LABORATORY','RESEARCH_LAB'],['JNR_LABORATORY','JNR_ARCHITECTURE','JNR_LIBERAL_ARTS','RESEARCH_LAB'],['RESEARCH_LAB']]
count=0
for names in chains:
 for active in range(5):
  for workers in [0,1,2,3,20,255]:
   l=runtime();l.globals().names=ns['ns']['to_lua'](l,['BUILDING_'+s for s in names]);l.execute(f"setBuildings(d,names);d.workers={workers};c.active={active};ca();local want={workers if active==4 else 0};for _,b in ipairs(tr) do local found=false;for _,n in ipairs(names) do if n==b.BuildingType then found=true end end;assert(cc(b.BuildingType)==(found and want or 0),b.BuildingType) end;local w=writes;ca();assert(writes==w)");count+=1
print('CHAIR MATRIX PASS',count,'actual writer configurations, building count independent of tier/D cap, workers0-255 and ACTIVE0-4')
l=runtime(2);l.execute("setBuildings(d,{'BUILDING_LIBRARY','BUILDING_UNIVERSITY'});d.workers=3;setBuildings(cities[2].ds[1],{'BUILDING_LIBRARY'});cities[2].ds[1].workers=1;ca();assert(cc('BUILDING_LIBRARY')==3 and cc('BUILDING_UNIVERSITY')==3 and cc('BUILDING_LIBRARY',cities[2])==1)")
# Decode actual SQL arguments and owner attachments, independent from Lua plan.
for _,c in l.globals().cities.items():
 amounts={}
 for idx,yes in c.carriers.items():
  if not yes:continue
  name=l.globals().GameInfo.Buildings[idx].BuildingType
  for mid,typ in ns['sql'].execute('select m.ModifierId,m.ModifierType from BuildingModifiers b join Modifiers m using(ModifierId) where b.BuildingType=?',(name,)):
   if not mid.startswith('SPC_RESEARCH_CHAIR_'):continue
   assert typ=='MODIFIER_BUILDING_YIELD_CHANGE'
   a=dict(ns['sql'].execute('select Name,Value from ModifierArguments where ModifierId=?',(mid,)));assert a['YieldType']=='YIELD_SCIENCE';amounts[a['BuildingType']]=amounts.get(a['BuildingType'],0)+int(a['Amount'])
 assert amounts==({'BUILDING_LIBRARY':3,'BUILDING_UNIVERSITY':3} if c.id==1 else {'BUILDING_LIBRARY':1})
print('CHAIR SQL PROJECTION PASS two cities same BuildingType different amounts, direct building Science only (not engine proof)')
for fault,repair in [('c.active=nil','c.active=4'),('c.factsError=true','c.factsError=false'),('d.workers=nil','d.workers=3'),('failRead=true;svc.MarkDirty()','failRead=false;svc.MarkDirty()'),("unknownCarrier=GameInfo.Buildings.BUILDING_SPC_RESEARCH_CHAIR_BUILDING_LIBRARY_0.Index","unknownCarrier=nil"),('d.workers=256','d.workers=3')]:
 l.execute(f"local w=writes;{fault};chair.Audit();assert(writes==w and chair.errors[0][1]);{repair};ca();assert(writes==w)")
for fault,repair in [('c.active=3','c.active=4'),("c.identity='CULTURE'","c.identity='RESEARCH'"),('d.pillaged=true;svc.MarkDirty()','d.pillaged=false;svc.MarkDirty()'),('d.workers=0','d.workers=3')]:
 l.execute(f"{fault};ca();assert(cc('BUILDING_LIBRARY')==0 and cc('BUILDING_UNIVERSITY')==0);local w=writes;ca();assert(writes==w);{repair};ca();assert(cc('BUILDING_LIBRARY')==3)")
l.execute("d.bs[1].pillaged=true;fire('BuildingPillaged');ca();assert(cc('BUILDING_LIBRARY')==0 and cc('BUILDING_UNIVERSITY')==3);d.bs[1].pillaged=false;fire('BuildingRepaired');ca();assert(cc('BUILDING_LIBRARY')==3);d.bs[2].complete=false;svc.MarkDirty();ca();assert(cc('BUILDING_UNIVERSITY')==0);d.bs[2].complete=true;svc.MarkDirty();ca();assert(cc('BUILDING_UNIVERSITY')==3);c.token='new';fire('LoadScreenClose');ca();local w=writes;fire('LoadScreenClose');ca();assert(writes==w)")
l.execute("d.type=GameInfo.Districts.DISTRICT_SEOWON.Index;setBuildings(d,{'BUILDING_MADRASA','BUILDING_UNKNOWN_MOD','BUILDING_SPC_INTERNAL','BUILDING_WONDER'});svc.MarkDirty();ca();assert(cc('BUILDING_MADRASA')==3 and cc('BUILDING_LIBRARY')==0);assert(chair.Describe(0,c,true):find('未审建筑'))")
print('CHAIR LIFECYCLE PASS unavailable/encoding bound hold, per-building pillage/remove/restore, known withdrawal once, unique/unknown/exclusion/load/token')
for n in [1,2,4,8]:
 l=runtime(n);l.execute("for _,c in pairs(cities) do setBuildings(c.ds[1],{'BUILDING_LIBRARY','BUILDING_UNIVERSITY'});c.ds[1].workers=2 end;counters={};audit();good();shared.ResearchApply.Audit();ca()")
 assert l.eval('counters.dc_capture')==n and l.eval('counters.facts')==3*n and l.eval('counters.district_scan')==n
 print('CHAIR SCALING',n,'cities captures',n,'facts',3*n,'building_checks',l.eval('counters.building_check'),'writes',l.eval('writes'))
 l.execute("local r,w,cap=reads,writes,counters.dc_capture;for i=1,10000 do fire('GameCoreEventPublishComplete');fire('GameCoreEventPlaybackComplete');fire('SystemUpdateUI');fire('UnitOperationStarted') end;assert(reads==r and writes==w and counters.dc_capture==cap);fire('PlayerTurnActivated',0);r=reads;w=writes;for i=1,10000 do fire('PlayerTurnActivated',0) end;assert(reads==r and writes==w);turn=turn+1;fire('PlayerTurnActivated',0);ca();assert(counters.dc_capture==cap+"+str(n)+")")
l=runtime();l.execute("setBuildings(d,{'BUILDING_LIBRARY','BUILDING_UNIVERSITY'});audit();good();local v=svc.Read(0,c,c.token);ca();local v2=svc.Read(0,c,c.token);assert(v.revision==v2.revision and v2.value.domains.DISTRICT_CAMPUS.value==3);local cap=counters.dc_capture;fire('BuildingAddedToMap',0,0,GameInfo.Buildings.BUILDING_UNIVERSITY.Index,0);ca();assert(counters.dc_capture==cap+1)")
print('CHAIR PERF PASS 10k unrelated0 scans/writes; once/turn reconcile; internal writes leave D/revision unchanged; direct event single capture shared across consumers')
l.execute('P.Scalar=tostring;stage=bomb');g=(M/'Gameplay.lua').read_text();l.execute(g[g.index('local function request('):g.index('GameEvents.SPC_P0_Request.Add')]+'\nrunRequest=request')
l.execute("local w=writes;runRequest(0,{Action='RESEARCH_CHAIR_READ',Token='r',CityID=1});assert(shared.Snapshot:find('合格学院建筑 2') and shared.Snapshot:find('预期 +6',1,true) and not shared.Snapshot:find('BUILDING_SPC_'));runRequest(0,{Action='RESEARCH_CHAIR_DETAIL',Token='d',CityID=1});assert(shared.Snapshot:find('Tier') and shared.Snapshot:find('BUILDING_LIBRARY'));assert(writes==w)")
t=ast.parse((R/'DevelopmentTests/test_arch_v2_d2.py').read_text());fix=next(ast.literal_eval(x.value) for x in t.body if isinstance(x,ast.Assign) and any(isinstance(k,ast.Name) and k.id=='UI_FIX' for k in x.targets))
u=LuaRuntime();u.execute(fix);u.execute("Mouse.eRClick=2;P.Scalar=tostring;print=function() end;clicks={};Controls.DP05Button.RegisterCallback=function(c,e,f) clicks[e]=f end;UI.RequestPlayerOperation=function(pid,op,p) sends=sends+1;lastAction=p.Action;shared.LastToken=p.Token;shared.Snapshot='学术主持';end")
u.execute((M/'UI/P0Panel.lua').read_text());u.execute("init();clicks[1]();assert(sends==1 and lastAction=='RESEARCH_CHAIR_READ');clicks[2]();assert(sends==2 and lastAction=='RESEARCH_CHAIR_DETAIL');for i=1,10000 do fire('SystemUpdateUI') end;assert(sends==2)")
print('CHAIR DIAGNOSTIC/UI PASS concise read-only summary, optional details, click1/request1,10k idle0')
allowed={'Gameplay.lua','Probe.lua','SpecializationP0.modinfo','UI/P0Panel.lua','UI/P0Panel.xml','UI/RuntimeAudit.lua','ResearchChair.lua','ResearchChairModel.lua','Data/ResearchChair.sql'}
for p in M.rglob('*'):
 if p.is_file() and str(p.relative_to(M)) not in allowed:assert p.read_bytes()==subprocess.check_output(['git','show','19bbc9c:Mod/'+str(p.relative_to(M))],cwd=R),p
for path in subprocess.check_output(['git','ls-files','Specialization/Design'],cwd=R,text=True).splitlines():assert (R/path).read_bytes()==subprocess.check_output(['git','show','19bbc9c:'+path],cwd=R),path
for p in M.rglob('*.lua'):l.execute('assert(load(...))',p.read_text())
x=ET.parse(M/'SpecializationP0.modinfo').getroot();assert x.get('version')=='113'
assert sorted(f.text for f in x.findall('./Files/File'))==sorted(str(p.relative_to(M)) for p in M.rglob('*') if p.is_file() and p.suffix!='.modinfo')
assert x.find("./InGameActions/UpdateDatabase/File[.='Data/ResearchChair.sql']") is not None
assert ns['sql'].execute("select count(*) from Building_CitizenYieldChanges where BuildingType like 'BUILDING_SPC_RESEARCH_CHAIR_%'").fetchone()[0]==0
print('CHAIR STATIC PASS allLua/manifest113/protectedRuntime/Design unchanged; no specialist yield rows')
