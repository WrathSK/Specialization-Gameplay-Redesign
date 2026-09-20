"""P0-D2 actual model/writer/SQL; native settlement requires user game evidence."""
from pathlib import Path
import ast, json, math, subprocess, xml.etree.ElementTree as ET
from lupa.lua55 import LuaRuntime
R=Path(__file__).resolve().parents[1];M=R/'Mod'
ns={'__file__':str(R/'DevelopmentTests/test_p0_c.py')}
exec(compile((R/'DevelopmentTests/test_p0_c.py').read_text().split('chains=[')[0],'P0C_fixture','exec'),ns)
ns['sql'].executescript((M/'Data/ResearchApply.sql').read_text())
ns['cr']=[dict(r,Index=10000+i,IsWonder=False) for i,r in enumerate(ns['sql'].execute('select * from Buildings'))]
ns['yields']=[dict(r) for r in ns['sql'].execute('select * from Building_CitizenYieldChanges')]
def runtime(n=1):
 l=ns['runtime'](n);l.execute((M/'ResearchApply.lua').read_text())
 l.execute("SPCResearchApply.Start(P,shared);ap=shared.ResearchApply;ap.ready=true;function aa() ap.Audit();assert(not ap.definitionError,ap.definitionError);for _,e in pairs(ap.errors) do for _,v in pairs(e) do error(v) end end end;function ac(y,c) c=c or cities[1];local n=0;for i=0,4 do if c.carriers[GameInfo.Buildings['BUILDING_SPC_RESEARCH_APPLY_'..y..'_'..i].Index] then n=n+2^i end end;return n end")
 return l
l=runtime();model=l.globals().SPCResearchApplyModel
conv=lambda x:ns['ns']['to_lua'](l,x)
count=0
for depth in [0,1,2,3,6,10]:
 for active in range(5):
  for workers in [0,1,2,5]:
   domains={'DISTRICT_CAMPUS':{'value':10,'districtID':11}}
   for _,m in model.Mapping.items():domains[m[1]]={'value':depth,'districtID':20}
   p=model.Plan(conv(dict(validity='VERIFIED',identity='RESEARCH',active=active,potential=4)),conv(dict(validity='VERIFIED',availability='READY',value={'domains':domains})),workers)
   expected={'FOOD':math.floor(.5*depth),'PRODUCTION':depth,'GOLD':3*depth,'CULTURE':math.floor(1.5*depth),'FAITH':math.floor(.5*depth)}
   for y,v in expected.items():assert p.per[y]==(v if active>=3 else 0) and p.total[y]==(workers*v if active>=3 else 0)
   count+=1
print('P0-D2 MODEL PASS',count,'configurations, nine domains, five yields, ACTIVE0-4/workers0,1,2,5; per-specialist grouped floor')
l.execute("i=addDistrict(c,20,'DISTRICT_INDUSTRIAL_ZONE');setBuildings(i,{'BUILDING_IZ_WATER_MILL'});aa();assert(ac('PRODUCTION')==0);d.workers=2;aa();assert(ac('PRODUCTION')==0)")
# Actual DB tier for water mill fixture = 1. Two same-yield D1 domains combine before floor.
l.execute("e=addDistrict(c,21,'DISTRICT_ENCAMPMENT');setBuildings(e,{'BUILDING_BARRACKS'});svc.MarkDirty();aa();assert(ac('PRODUCTION')==1);local w=writes;d.workers=0;aa();assert(ac('PRODUCTION')==1 and writes==w);d.workers=2;aa();assert(writes==w)")
print('P0-D2 WRITER PASS single D1 gives0 for2 specialists; two D1 domains give1 each; worker count never changes configured coefficient')
l.execute("g=addDistrict(c,22,'DISTRICT_COMMERCIAL_HUB');setBuildings(g,{'BUILDING_MARKET'});svc.MarkDirty();aa();assert(ac('GOLD')==1);local w=writes;aa();assert(writes==w)")
for fault,repair in [('c.active=nil','c.active=4'),('c.factsError=true','c.factsError=false'),('d.workers=nil','d.workers=2'),('failRead=true;svc.MarkDirty()','failRead=false;svc.MarkDirty()'),("unknownCarrier=GameInfo.Buildings.BUILDING_SPC_RESEARCH_APPLY_GOLD_0.Index","unknownCarrier=nil")]:
 l.execute(f"local w=writes;{fault};ap.Audit();assert(writes==w and ap.errors[0][1]);{repair};aa();assert(writes==w)")
for fault,repair in [('c.active=2','c.active=4'),("c.identity='INDUSTRY'","c.identity='RESEARCH'"),('d.pillaged=true;svc.MarkDirty()','d.pillaged=false;svc.MarkDirty()')]:
 l.execute(f"{fault};aa();assert(ac('GOLD')==0 and ac('PRODUCTION')==0);local w=writes;aa();assert(writes==w);{repair};aa();assert(ac('GOLD')==1 and ac('PRODUCTION')==1)")
l.execute("c.active=3;local w=writes;aa();assert(writes==w);i.bs[1].pillaged=true;fire('BuildingPillaged');aa();assert(ac('PRODUCTION')==0);i.bs[1].pillaged=false;fire('BuildingRepaired');aa();assert(ac('PRODUCTION')==1);c.token='NEW';fire('LoadScreenClose');aa();assert(ac('GOLD')==1);d.type=GameInfo.Districts.DISTRICT_SEOWON.Index;svc.MarkDirty();aa();assert(ac('GOLD')==1)")
print('P0-D2 LIFECYCLE PASS unavailable hold, confirmed withdrawal once, III/IV inheritance, pillage/repair, token/load/unique district')
# Same domain maximum is a shared fact; actual D service tests cover its ontology.
l.execute("n1=addDistrict(c,31,'DISTRICT_NEIGHBORHOOD');n2=addDistrict(c,32,'DISTRICT_NEIGHBORHOOD');setBuildings(n1,{'BUILDING_FOOD_MARKET'});svc.MarkDirty();aa();local v=svc.Read(0,c,c.token);local p=SPCResearchApplyModel.Plan(SPCCurrentSpecializationFacts.Read(P,shared,0,c),v,2);assert(p.per.FOOD==math.floor(.5*v.value.domains.DISTRICT_NEIGHBORHOOD.value));assert(ac('FOOD')==p.per.FOOD)")
# Real dispatch is read-only, concise default and optional relevant detail.
l.execute('P.Scalar=tostring;stage=bomb');g=(M/'Gameplay.lua').read_text();l.execute(g[g.index('local function request('):g.index('GameEvents.SPC_P0_Request.Add')]+'\nrunRequest=request')
l.execute("local w=writes;runRequest(0,{Action='RESEARCH_APPLY_READ',Token='r',CityID=1});assert(shared.Snapshot:find('每名floor') and shared.Snapshot:find('每名配置') and not shared.Snapshot:find('BUILDING_SPC_'));runRequest(0,{Action='RESEARCH_APPLY_DETAIL',Token='d',CityID=1});assert(shared.Snapshot:find('Tier') and shared.Snapshot:find('cap前'));assert(writes==w)")
print('P0-D2 DIAGNOSTIC PASS actual selected-city dispatch; no writes; coefficients distinct from expected/native')
for n in [1,2,4,8]:
 l=runtime(n);l.execute("for _,c in pairs(cities) do setBuildings(c.ds[1],{'BUILDING_LIBRARY'});local d=addDistrict(c,50+c.id,'DISTRICT_COMMERCIAL_HUB');setBuildings(d,{'BUILDING_MARKET'}) end;counters={};audit();good();aa()")
 assert l.eval('counters.dc_capture')==n
 assert l.eval('counters.district_scan')==2*n
 assert l.eval('counters.facts')==2*n
 print('P0-D2 SCALING',n,'cities; shared captures',n,'facts',2*n,'districts',2*n,'building checks',l.eval('counters.building_check'),'writes',l.eval('writes'))
 l.execute("local r,w,cap=reads,writes,counters.dc_capture;for j=1,10000 do fire('GameCoreEventPublishComplete');fire('GameCoreEventPlaybackComplete');fire('SystemUpdateUI');fire('UnitOperationStarted') end;assert(reads==r and writes==w and counters.dc_capture==cap);fire('PlayerTurnActivated',0);r=reads;w=writes;for j=1,10000 do fire('PlayerTurnActivated',0) end;assert(reads==r and writes==w);turn=turn+1;fire('PlayerTurnActivated',0);assert(counters.dc_capture==cap+"+str(n)+");aa()")
l=runtime();l.execute("i=addDistrict(c,20,'DISTRICT_COMMERCIAL_HUB');setBuildings(i,{'BUILDING_MARKET'});audit();aa();local cap=counters.dc_capture;fire('BuildingAddedToMap',0,0,GameInfo.Buildings.BUILDING_MARKET.Index,0);aa();assert(counters.dc_capture==cap+1);cap=counters.dc_capture;fire('BuildingAddedToMap',0,0,GameInfo.Buildings.BUILDING_SPC_RESEARCH_APPLY_GOLD_0.Index,0);aa();assert(counters.dc_capture==cap)")
print('P0-D2 PERF PASS 10000 pulses zero scans/writes; same-turn fallback bounded; one shared D capture per real event, internal carrier event0')
t=ast.parse((R/'DevelopmentTests/test_arch_v2_d2.py').read_text());fix=next(ast.literal_eval(x.value) for x in t.body if isinstance(x,ast.Assign) and any(isinstance(k,ast.Name) and k.id=='UI_FIX' for k in x.targets))
u=LuaRuntime();u.execute(fix);u.execute("Mouse.eRClick=2;P.Scalar=tostring;print=function() end;clicks={};Controls.DP03Button.RegisterCallback=function(c,e,f) clicks[e]=f end;UI.RequestPlayerOperation=function(pid,op,p) sends=sends+1;lastAction=p.Action;shared.LastToken=p.Token;shared.Snapshot='学以致用';end")
u.execute((M/'UI/P0Panel.lua').read_text());u.execute("init();clicks[1]();assert(sends==1 and lastAction=='RESEARCH_APPLY_READ');clicks[2]();assert(sends==2 and lastAction=='RESEARCH_APPLY_DETAIL');for i=1,10000 do fire('SystemUpdateUI') end;assert(sends==2)")
print('P0-D2 PANEL PASS summary/detail eachsend1,10000 idle0')
# Real SQL-backed writer maximum coefficient encoding, all five yields; synthetic
# verified shared fact isolates projection from ontology covered above and P0-A.
l=runtime();l.execute("local native=svc.Read;svc.Read=function(pid,c,t) local v=native(pid,c,t);for _,m in ipairs(SPCResearchApplyModel.Mapping) do v.value.domains[m[1]]={value=10,districtID=20} end;return v end;aa();assert(ac('FOOD')==5 and ac('PRODUCTION')==10 and ac('GOLD')==30 and ac('CULTURE')==15 and ac('FAITH')==5);local w=writes;aa();assert(writes==w);c.active=2;aa();for _,y in ipairs(SPCResearchApplyModel.Yields) do assert(ac(y)==0) end;w=writes;aa();assert(writes==w)")
print('P0-D2 ENCODING PASS all five native specialist coefficients max5/10/30/15/5; removal once')

allowed={'DistrictCompleteness.lua','Gameplay.lua','Probe.lua','SpecializationP0.modinfo','UI/P0Panel.lua','UI/P0Panel.xml','UI/RuntimeAudit.lua','ResearchApply.lua','ResearchApplyModel.lua','Data/ResearchApply.sql'}
for p in M.rglob('*'):
 if p.is_file() and str(p.relative_to(M)) not in allowed:assert p.read_bytes()==subprocess.check_output(['git','show','cb8a4c7:Mod/'+str(p.relative_to(M))],cwd=R),p
for path in subprocess.check_output(['git','ls-files','Specialization/Design'],cwd=R,text=True).splitlines():assert (R/path).read_bytes()==subprocess.check_output(['git','show','cb8a4c7:'+path],cwd=R),path
for p in M.rglob('*.lua'):l.execute('assert(load(...))',p.read_text())
x=ET.parse(M/'SpecializationP0.modinfo').getroot();assert x.get('version')=='112'
listed=[f.text for f in x.findall('./Files/File')];actual=[str(p.relative_to(M)) for p in M.rglob('*') if p.is_file() and p.suffix!='.modinfo'];assert sorted(listed)==sorted(actual)
rows=[r for r in ns['yields'] if 'RESEARCH_APPLY_' in r['BuildingType']];assert len(rows)==25 and all(r['YieldChange'] in [1,2,4,8,16] for r in rows)
assert x.find("./InGameActions/UpdateDatabase/File[.='Data/ResearchApply.sql']") is not None
assert 'ModifierArguments' not in (M/'Data/ResearchApply.sql').read_text()
print('P0-D2 STATIC PASS all Lua,25 native specialist-only rows,modinfo112,exact file list,protected runtime and Design unchanged')
