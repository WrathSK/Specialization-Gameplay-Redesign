"""Actual P0-C Lua/SQL. Engine placement/settlement remains user-test evidence."""
from pathlib import Path
import ast,json,sqlite3,subprocess,xml.etree.ElementTree as ET
from lupa.lua55 import LuaRuntime
R=Path(__file__).resolve().parents[1];M=R/'Mod'
p=R/'DevelopmentTests/test_p0_a.py';tree=ast.parse(p.read_text());ns={'__file__':str(p)}
kept=[n for n in tree.body if isinstance(n,(ast.Import,ast.ImportFrom,ast.FunctionDef)) or isinstance(n,ast.Assign) and all(isinstance(t,ast.Name) and t.id in {'R','M','NEW','FIX'} for t in n.targets)]
exec(compile(ast.Module(body=kept,type_ignores=[]),str(p),'exec'),ns)
def database(old=False):
 db=sqlite3.connect(':memory:');db.row_factory=sqlite3.Row
 db.executescript('CREATE TABLE Types(Type TEXT,Kind TEXT);CREATE TABLE Buildings(BuildingType TEXT,Name TEXT,Cost INTEGER,PrereqDistrict TEXT,InternalOnly INTEGER,CitizenSlots INTEGER,Housing INTEGER);CREATE TABLE Building_CitizenYieldChanges(BuildingType TEXT,YieldType TEXT,YieldChange INTEGER);CREATE TABLE Modifiers(ModifierId TEXT,ModifierType TEXT);CREATE TABLE ModifierArguments(ModifierId TEXT,Name TEXT,Value TEXT);CREATE TABLE BuildingModifiers(BuildingType TEXT,ModifierId TEXT);')
 for f in ['Lv4Percent','CopyYields']+([] if old else ['ResearchInfrastructure']):
  s=subprocess.check_output(['git','show','4f26050:Mod/Data/'+f+'.sql'],cwd=R,text=True) if old else (M/'Data'/f'{f}.sql').read_text()
  db.executescript(s)
 return db
sql=database();old=database(True)
cr=[dict(r,Index=10000+i,IsWonder=False) for i,r in enumerate(sql.execute('select * from Buildings'))]
yields=[dict(r) for r in sql.execute('select * from Building_CitizenYieldChanges')]
AUG=r"""
P.Rows=function(t) local a={};for r in GameInfo[t]() do a[#a+1]=r end;return a end
P.HasBuilding=function(b,id) return b:HasBuilding(id) end
P.CreateBuilding=function(q,id) assert(not q.city.carriers[id]);q.city.carriers[id]=true;q.city.locations[id]=q.city.ds[1].plot;writes=writes+1;fire('BuildingAddedToMap',0,0,id,q.city.owner) end
P.RemoveBuilding=function(b,id) if failRemove then error('INTENTIONAL_REMOVE_FAILURE') end;assert(b.city.carriers[id]);b.city.carriers[id]=nil;b.city.locations[id]=nil;writes=writes+1;fire('BuildingRemovedFromMap',0,0,id,b.city.owner) end
function wrap(c)
 c.carriers={};c.locations={};local get=c.GetBuildings;local q=c.GetBuildQueue()
 c.GetBuildings=function()
  local b=get();b.city=c;local has,loc,pill=b.HasBuilding,b.GetBuildingLocation,b.IsPillaged
  b.HasBuilding=function(_,id) if unknownCarrier==id then return nil end;return c.carriers[id]==true or has(b,id) end
  b.GetBuildingLocation=function(_,id) if c.carriers[id] then return c.locations[id] end;return loc(b,id) end
  b.IsPillaged=function(_,id) if c.carriers[id] then return false end;return pill(b,id) end
  return b
 end
 q.city=c;c.GetBuildQueue=function() return q end
 c.GetProperty=function(_,key) return key=='SPC_B050_HALF_ENABLED' and half or nil end
end
wrap(c)
Players={[0]={GetCities=function() return {Members=function() return pairs(cities) end,FindID=function(_,id) return cities[id] end} end}}
local native=shared.EffectiveFacts.Read
shared.EffectiveFacts.Read=function(pid,c) local f=native(pid,c);f.potential=c.potential or 4;return f end
function audit() shared.ResearchInfrastructure.Audit() end
function good() for _,errs in pairs(shared.ResearchInfrastructure.errors) do for _,e in pairs(errs) do error(e) end end end
function coeff(c) local n=0;for i=0,3 do if c.carriers[GameInfo.Buildings['BUILDING_SPC_RESEARCH_INFRA_'..i].Index] then n=n+2^i end end;return n end
function seedOld() for _,name in ipairs(SPCResearchInfrastructure.Retired) do local id=GameInfo.Buildings[name].Index;c.carriers[id]=true;c.locations[id]=d.plot end end
function retired() for _,name in ipairs(SPCResearchInfrastructure.Retired) do assert(not c.carriers[GameInfo.Buildings[name].Index],name) end end
"""
def runtime(n=1):
 l=ns['runtime']();l.globals().include=lambda name:l.execute((M/(name+'.lua')).read_text())
 l.globals().cr=ns['to_lua'](l,cr);l.globals().yr=ns['to_lua'](l,yields)
 l.execute("for _,r in ipairs(cr) do brows[#brows+1]=r end;GameInfo.Buildings=db(brows,'BuildingType');GameInfo.Building_CitizenYieldChanges=db(yr,'BuildingType')")
 l.execute(AUG)
 for i in range(2,n+1):l.execute(f"local c=newCity({i});wrap(c);c.active=4;addDistrict(c,{i+10},'DISTRICT_CAMPUS')")
 l.execute((M/'ResearchInfrastructure.lua').read_text());l.execute('SPCResearchInfrastructure.Start(P,shared);shared.ResearchInfrastructure.ready=true')
 return l
chains=[([],0),(['LIBRARY'],1),(['LIBRARY','UNIVERSITY'],3),(['LIBRARY','UNIVERSITY','JNR_LABORATORY'],6),(['LIBRARY','UNIVERSITY','JNR_LABORATORY','RESEARCH_LAB'],10)]
l=runtime()
for names,depth in chains:
 for workers in [0,1,2,5]:
  for active in range(5):
   l.globals().names=ns['to_lua'](l,['BUILDING_'+n for n in names]);expected=depth if active==4 and workers else 0
   l.execute(f"setBuildings(d,names);svc.MarkDirty();d.workers={workers};c.active={active};audit();good();assert(coeff(c)=={expected});local w=writes;audit();good();assert(writes==w)")
print('P0-C MATRIX PASS 100 configurations; actual carrier coefficient and no-op repeat')
l=runtime();l.execute("setBuildings(d,{'BUILDING_LIBRARY','BUILDING_UNIVERSITY'});seedOld();audit();good();retired();assert(coeff(c)==3 and writes==50);local w=writes;audit();fire('LoadScreenClose');good();retired();assert(writes==w)")
for fault,repair in [('c.active=nil','c.active=4'),('c.factsError=true','c.factsError=false'),('d.workers=nil','d.workers=3'),('failRead=true;svc.MarkDirty()','failRead=false;svc.MarkDirty()'),("unknownCarrier=GameInfo.Buildings.BUILDING_SPC_RESEARCH_INFRA_3.Index","unknownCarrier=nil")]:
 l.execute(f"local w=writes;{fault};audit();assert(writes==w and shared.ResearchInfrastructure.errors[0][1]);{repair};audit();good();assert(writes==w)")
for fault,repair in [('c.active=3','c.active=4'),('d.pillaged=true;svc.MarkDirty()','d.pillaged=false;svc.MarkDirty()'),('d.workers=0','d.workers=3'),("c.identity='NONE'","c.identity='RESEARCH'")]:
 l.execute(f"{fault};audit();good();assert(coeff(c)==0);local w=writes;audit();assert(writes==w);{repair};audit();good();assert(coeff(c)==3)")
l.execute("d.type=GameInfo.Districts.DISTRICT_SEOWON.Index;svc.MarkDirty();audit();good();assert(coeff(c)==3);local w=writes;half=true;assert(shared.ResearchInfrastructure.Describe(0,c):find('半点实验'));assert(writes==w);half=false;d.bs[1].pillaged=true;fire('BuildingPillaged');good();assert(coeff(c)==2);d.bs[1].pillaged=false;fire('BuildingRepaired');good();assert(coeff(c)==3)")
l.execute("local w=writes;d2=addDistrict(c,99,'DISTRICT_CAMPUS');svc.MarkDirty();audit();assert(coeff(c)==3 and writes==w and shared.ResearchInfrastructure.errors[0][1]:find('MULTIPLE_CAMPUSES'));c.ds[2]=nil;svc.MarkDirty();audit();good()")
l.execute("c.active=4;c.potential=3;local w=writes;audit();assert(writes==w);c.potential=4;c.token='NEW';fire('LoadScreenClose');good();assert(writes==w)")
print('P0-C LIFECYCLE PASS unknown hold/known withdrawal/zero/repeat/load/reference/unique/pillage; unexpected environment diagnosed')
l=runtime();l.execute("setBuildings(d,{'BUILDING_LIBRARY'});seedOld();failRemove=true;audit();assert(writes==0 and coeff(c)==0 and shared.ResearchInfrastructure.errors[0][1]);failRemove=false;audit();good();retired();assert(coeff(c)==1)")
# Old public writers cannot recreate retired effects, even with late accepted samples.
# Transport lifecycle is covered in the frozen C2/D2 suite; actual writers loaded here.
l.execute("shared.NetworkBridge={RecipientSources=function() return {} end};SPCCurrentSpecializationFacts.Read(P,shared,0,c)")
for mod in ['Lv4Percent','CopyYields']:
 l.execute((M/(mod+'.lua')).read_text());l.execute(f'SPC{mod}.Start(P,shared);shared.{mod}.ready=true;shared.{mod}.Audit()')
l.execute("retired();local w=writes;shared.CopyYields.Audit();shared.Lv4Percent.Audit();retired();assert(writes==w)")
print('P0-C CUTOVER PASS exact48 cleanup, failure blocks new creation; old writer Audits never recreate')
for n in [1,2,4,8]:
 l=runtime(n);l.execute("counters={};for _,c in pairs(cities) do setBuildings(c.ds[1],{'BUILDING_LIBRARY'}) end;audit();good()")
 assert l.eval('counters.facts')==n and l.eval('counters.dc_capture')==n and l.eval('counters.district_scan')==n
 print('P0-C SCALING',n,'cities/facts/captures/districts',n,'building checks',l.eval('counters.building_check'))
 l.execute("local r,w=reads,writes;for i=1,10000 do fire('GameCoreEventPublishComplete');fire('GameCoreEventPlaybackComplete');fire('SystemUpdateUI');fire('UnitOperationStarted') end;assert(reads==r and writes==w);fire('PlayerTurnActivated',0);r=reads;w=writes;for i=1,10000 do fire('PlayerTurnActivated',0) end;assert(reads==r and writes==w);c.active=3;turn=turn+1;fire('PlayerTurnActivated',0);good();assert(coeff(c)==0)")
print('P0-C IDLE PASS 10000 generic pulses reads/writes0; turn fallback once/player/turn')
l=runtime();l.execute("setBuildings(d,{'BUILDING_LIBRARY','BUILDING_UNIVERSITY'});audit();good();P.Scalar=tostring;stage=bomb")
g=(M/'Gameplay.lua').read_text();l.execute(g[g.index('local function request('):g.index('GameEvents.SPC_P0_Request.Add')]+'\nrunRequest=request')
l.execute("local w=writes;runRequest(0,{Action='COMPLETENESS_READ',Token='c',CityID=1});assert(shared.LastToken=='c' and shared.Snapshot:find('预期新增基础科技：9') and not shared.Snapshot:find('P0%-B2') and not shared.Snapshot:find('BUILDING_'));runRequest(0,{Action='RESEARCH_INFRA_DETAIL',Token='detail',CityID=1});assert(shared.Snapshot:find('贡献') and shared.Snapshot:find('cap前') and shared.Snapshot:find('Tier'));assert(writes==w)")
print('P0-C DIAGNOSTIC PASS actual dispatch, concise summary + optional Campus composition; no writes')
# Real panel: left and right each send one read, idle never sends.
t=ast.parse((R/'DevelopmentTests/test_arch_v2_d2.py').read_text())
fix=next(ast.literal_eval(x.value) for x in t.body if isinstance(x,ast.Assign) and any(isinstance(k,ast.Name) and k.id=='UI_FIX' for k in x.targets))
u=LuaRuntime();u.execute(fix)
u.execute("Mouse.eRClick=2;P.Scalar=tostring;print=function() end;clicks={};Controls.CompletenessButton.RegisterCallback=function(c,e,f) clicks[e]=f end;UI.RequestPlayerOperation=function(pid,op,p) sends=sends+1;lastAction=p.Action;shared.LastToken=p.Token;shared.Snapshot='科研基础设施';end")
u.execute((M/'UI/P0Panel.lua').read_text())
u.execute("init();clicks[1]();assert(sends==1 and lastAction=='COMPLETENESS_READ');clicks[2]();assert(sends==2 and lastAction=='RESEARCH_INFRA_DETAIL');for i=1,10000 do fire('SystemUpdateUI') end;assert(sends==2)")
print('P0-C PANEL PASS left summary/right details send once each,10000 idle0')

# SQL preserves all old IDs; only exact48 effects removed; every other row identical.
retired=[f'BUILDING_SPC_LV4_PERCENT_RESEARCH_{i}' for i in range(8)]+[f'BUILDING_SPC_B051_SCIENCE_{m}_{i}' for m in ['POS','NEG','POP'] for i in range(8 if m=='POP' else 16)]
for name in retired:
 assert sql.execute('select count(*) from Buildings where BuildingType=?',(name,)).fetchone()[0]==1
 assert sql.execute('select count(*) from BuildingModifiers where BuildingType=?',(name,)).fetchone()[0]==0
for table in ['Modifiers','ModifierArguments','BuildingModifiers']:
 a=[tuple(r) for r in old.execute('select * from '+table) if not any('SPC_LV4_PERCENT_RESEARCH_' in str(v) or 'SPC_B051_SCIENCE_' in str(v) for v in r)]
 assert sorted(a)==sorted(tuple(r) for r in sql.execute('select * from '+table)),table
assert len(yields)==4 and [r['YieldChange'] for r in yields]==[1,2,4,8]
allowed={'ResearchInfrastructure.lua','Data/ResearchInfrastructure.sql','CopyYields.lua','Data/CopyYields.sql','Lv4Percent.lua','Data/Lv4Percent.sql','Lv4CopyRead.lua','Gameplay.lua','Probe.lua','SpecializationP0.modinfo','UI/P0Panel.lua','UI/RuntimeAudit.lua'}
for p in M.rglob('*'):
 if p.is_file() and str(p.relative_to(M)) not in allowed:assert p.read_bytes()==subprocess.check_output(['git','show','4f26050:Mod/'+str(p.relative_to(M))],cwd=R),p
for path in subprocess.check_output(['git','ls-files','Specialization/Design'],cwd=R,text=True).splitlines():assert (R/path).read_bytes()==subprocess.check_output(['git','show','4f26050:'+path],cwd=R),path
x=ET.parse(M/'SpecializationP0.modinfo').getroot();assert x.get('version')=='108'
for f in ['ResearchInfrastructure.lua','Data/ResearchInfrastructure.sql']:assert x.find("./Files/File[.='"+f+"']") is not None
assert x.find("./InGameActions/UpdateDatabase/File[.='Data/ResearchInfrastructure.sql']") is not None
for p in M.rglob('*.lua'):l.execute('assert(load(...))',p.read_text())
print('P0-C STATIC PASS SQL retirement/protected effects/exact scope/Design unchanged/all Lua/modinfo108')
