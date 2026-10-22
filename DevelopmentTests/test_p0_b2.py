"""P0-B2 actual Lua writers + actual P0-A producer. No engine or deployment."""
from pathlib import Path
import ast,json,sqlite3,subprocess,xml.etree.ElementTree as ET
from lupa.lua55 import LuaRuntime
R=Path(__file__).resolve().parents[1];M=R/'Mod'
s=(R/'DevelopmentTests/test_p0_a.py').read_text();tree=ast.parse(s)
ns={'__file__':str(R/'DevelopmentTests/test_p0_a.py')}
# Import only fixture definitions; retain frozen P0-A acceptance unchanged.
exec(compile(ast.Module(body=[n for n in tree.body if isinstance(n,(ast.Import,ast.ImportFrom,ast.FunctionDef,ast.Assign)) and not (isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='l' for t in n.targets))],type_ignores=[]),'P0A_fixture','exec'),ns)
# Actual SQL, exact carrier identities/values: not a reimplementation of amounts.
db=sqlite3.connect(':memory:');db.row_factory=sqlite3.Row
db.executescript('CREATE TABLE Types(Type TEXT,Kind TEXT);CREATE TABLE Buildings(BuildingType TEXT,Name TEXT,Cost INTEGER,PrereqDistrict TEXT,InternalOnly INTEGER,CitizenSlots INTEGER,Housing INTEGER);CREATE TABLE Building_GreatPersonPoints(BuildingType TEXT,GreatPersonClassType TEXT,PointsPerTurn INTEGER);')
for f in ['Lv2Housing','Lv2GPP']:db.executescript((M/'Data'/f'{f}.sql').read_text())
carriers=[dict(r,Index=10000+i,IsWonder=False) for i,r in enumerate(db.execute('select * from Buildings'))]
assert len(carriers)==41
assert sum(r['Housing']==1 for r in carriers)==9
points=[dict(r) for r in db.execute('select * from Building_GreatPersonPoints')];assert len(points)==48
AUGMENT=r"""
P.Families={DISTRICT_CAMPUS='RESEARCH',DISTRICT_THEATER='CULTURE',DISTRICT_COMMERCIAL_HUB='COMMERCE',DISTRICT_INDUSTRIAL_ZONE='INDUSTRY'}
P.Family=function(t) return P.Families[t] or (t=='DISTRICT_SEOWON' and 'RESEARCH') end
P.Rows=function(t) local a={};for r in GameInfo[t]() do a[#a+1]=r end;return a end
P.HasBuilding=function(b,i) return b:HasBuilding(i) end
P.CreateBuilding=function(q,i) assert(not q.city.carriers[i]);q.city.carriers[i]=true;writes=writes+1;fire('BuildingAddedToMap',0,0,i,q.city.owner) end
P.RemoveBuilding=function(b,i) assert(b.city.carriers[i]);b.city.carriers[i]=nil;writes=writes+1;fire('BuildingRemovedFromMap',0,0,i,b.city.owner) end
function wrap(c)
 c.carriers={};local old=c.GetBuildings;local q=c.GetBuildQueue()
 c.GetBuildings=function()
  local b=old();local h=b.HasBuilding;b.city=c
  b.HasBuilding=function(_,i) if unknownCarrier==i then return nil end;return c.carriers[i]==true or h(b,i) end
  return b
 end
 q.city=c;c.GetBuildQueue=function() return q end
end
wrap(c)
Players={[0]={GetCities=function() return {Members=function() return pairs(cities) end} end,
 GetDistricts=function() return {Members=function() local a={};for _,v in pairs(cities) do for _,d in ipairs(v.ds) do a[#a+1]=d end end;return ipairs(a) end} end}}
shared.EffectiveFacts.Read=function(pid,c)
 P.Count('facts');if c.factsError then error('TEMPORARY_FLOW') end
 return {specialization=c.identity or 'RESEARCH',potential=4,active=c.active,first=c.first or {districtID=c.ds[1].id,type=GameInfo.Districts[c.ds[1].type].DistrictType}}
end
function noErrors() for _,m in ipairs({shared.Lv2Housing,shared.Lv2GPP}) do for k,e in pairs(m.errors) do assert(not e,k..':'..e) end end end
function audit() shared.Lv2Housing.Audit();shared.Lv2GPP.Audit() end
function housing(c) local n=0;for i=0,8 do if c.carriers[GameInfo.Buildings['BUILDING_SPC_DEV_LV2_HOUSING_'..i].Index] then n=n+1 end end;return n end
function gpp(c,kind) local n=0;for i=0,7 do if c.carriers[GameInfo.Buildings['BUILDING_SPC_DEV_GPP_'..kind..'_'..i].Index] then n=n+2*2^i end end;return n end
"""
def runtime(n=1,old=False):
 l=ns['runtime']();l.globals().include=lambda name:l.execute((M/(name+'.lua')).read_text())
 l.globals().cr=ns['to_lua'](l,carriers);l.globals().pr=ns['to_lua'](l,points)
 l.execute("for _,b in ipairs(cr) do brows[#brows+1]=b end;GameInfo.Buildings=db(brows,'BuildingType');GameInfo.Building_GreatPersonPoints=db(pr,'BuildingType')")
 l.execute(AUGMENT)
 for i in range(2,n+1):l.execute(f"local nc=newCity({i});wrap(nc);nc.active=4;addDistrict(nc,{10+i},'DISTRICT_CAMPUS')")
 # Old comparator gets its historical tier table from the actual old SQL literals.
 import re
 oldrows=[{'Tier':int(t),'BuildingType':b,'DistrictType':d} for t,b,d in re.findall(r"PrereqDistrict, (\d+) FROM Buildings WHERE BuildingType='([^']+)' AND PrereqDistrict='([^']+)'",(M/'Data/Lv2Housing.sql').read_text())]
 l.globals().oldrows=ns['to_lua'](l,oldrows);l.execute("GameInfo.SPC_Lv2HousingTiers=db(oldrows,'BuildingType')")
 for mod in ['Lv2Housing','Lv2GPP']:
  source=subprocess.check_output(['git','show','845cda1:Mod/'+mod+'.lua'],cwd=R,text=True) if old else (M/(mod+'.lua')).read_text()
  l.execute(source);l.execute(f'SPC{mod}.Start(P,shared);shared.{mod}.ready=true')
 return l

for kind,domain in [('RESEARCH','CAMPUS'),('CULTURE','THEATER'),('INDUSTRY','INDUSTRIAL_ZONE'),('COMMERCE','COMMERCIAL_HUB')]:
 for active in [1,2,3,4]:
  for workers in [0,1,3]:
   a,b=runtime(old=True),runtime()
   for l in (a,b):l.execute(f"c.identity='{kind}';c.active={active};d.type=GameInfo.Districts['DISTRICT_{domain}'].Index;d.workers={workers};audit();noErrors();assert(housing(c)==({active}>=2 and 1 or 0));assert(gpp(c,'{kind}')==({active}>=2 and {workers}*2 or 0))")
   assert a.eval('housing(c)')==b.eval('housing(c)') and a.eval(f"gpp(c,'{kind}')")==b.eval(f"gpp(c,'{kind}')")
print('DIFFERENTIAL PASS four professions x ACTIVE1..4 x workers0/1/3; native48 base-point rows unchanged')
l=runtime()
for buildings,expected in [([],1),(['LIBRARY'],2),(['LIBRARY','UNIVERSITY'],3),(['LIBRARY','UNIVERSITY','JNR_LABORATORY'],4),(['LIBRARY','UNIVERSITY','JNR_LABORATORY','RESEARCH_LAB'],5),(['JNR_LABORATORY'],2)]:
 l.globals().names=l.table_from(['BUILDING_'+b for b in buildings]);l.execute(f"setBuildings(d,names);audit();noErrors();assert(housing(c)=={expected});local w=writes;audit();assert(writes==w)")
l.execute("setBuildings(d,{'BUILDING_UNIVERSITY','BUILDING_MADRASA'});audit();noErrors();assert(housing(c)==2)")
l.execute("d.bs[1].pillaged=true;audit();noErrors();assert(housing(c)==2);d.bs[2].pillaged=true;audit();noErrors();assert(housing(c)==1);d.bs[1].pillaged=false;fire('BuildingRepaired');noErrors();assert(housing(c)==2)")
l.execute("setBuildings(d,{'BUILDING_LIBRARY'});d.bs[1].complete=false;audit();noErrors();assert(housing(c)==1);d.bs[1].complete=true;fire('BuildingConstructed');noErrors();assert(housing(c)==2)")
l.execute("d.type=GameInfo.Districts.DISTRICT_SEOWON.Index;audit();noErrors();assert(housing(c)==2 and gpp(c,'RESEARCH')==6)")
l.execute("local other=addDistrict(c,99,'DISTRICT_CAMPUS');setBuildings(other,{'BUILDING_UNIVERSITY','BUILDING_JNR_LABORATORY','BUILDING_RESEARCH_LAB'});audit();noErrors();assert(housing(c)==2)")
l.execute("setBuildings(d,{'BUILDING_LIBRARY','BUILDING_PALACE','BUILDING_WONDER','BUILDING_SPC_INTERNAL','BUILDING_UNKNOWN_MOD'});audit();noErrors();assert(housing(c)==2)")
print('HOUSING PASS 1/2/3/4/5/2; distinct tier, free/unique, unfinished, pillage/repair, actual anchor (not highest D), exclusions')
# UNKNOWN cannot mutate either projection, including partially unreadable carrier sets.
for fault,repair in [("c.active=nil","c.active=4"),("c.factsError=true","c.factsError=false"),("d.pillaged=nil","d.pillaged=false")]:
 l.execute(f"local w=writes;{fault};audit();assert(writes==w and shared.Lv2Housing.errors['0:1'] and shared.Lv2GPP.errors['0:1']);{repair};audit();noErrors();assert(writes==w)")
l.execute("local w=writes;failRead=true;shared.Lv2Housing.Audit();assert(writes==w and shared.Lv2Housing.errors['0:1']);failRead=false;shared.Lv2Housing.Audit();noErrors();assert(writes==w);d.workers=nil;shared.Lv2GPP.Audit();assert(writes==w and shared.Lv2GPP.errors['0:1']);d.workers=3;shared.Lv2GPP.Audit();noErrors();assert(writes==w)")
for family in ['LV2_HOUSING_8','GPP_COMMERCE_7']:
 l.execute(f"local w=writes;c.active=1;unknownCarrier=GameInfo.Buildings['BUILDING_SPC_DEV_{family}'].Index;shared.{'Lv2Housing' if family.startswith('LV2') else 'Lv2GPP'}.Audit();assert(writes==w);unknownCarrier=nil;c.active=4;audit();noErrors();assert(writes==w)")
for fault,repair in [("c.active=1","c.active=4"),("d.pillaged=true","d.pillaged=false"),("d.complete=false","d.complete=true"),("c.identity='NONE'","c.identity='RESEARCH'")]:
 l.execute(f"{fault};audit();noErrors();assert(housing(c)==0 and gpp(c,'RESEARCH')==0);local w=writes;audit();assert(writes==w);{repair};audit();noErrors();assert(housing(c)==2 and gpp(c,'RESEARCH')==6)")
l.execute("d.workers=0;fire('CityWorkerChanged',0);noErrors();assert(housing(c)==2 and gpp(c,'RESEARCH')==0);d.workers=1;fire('CityWorkerChanged',0);noErrors();assert(gpp(c,'RESEARCH')==2)")
l.execute("local w=writes;local report=shared.Lv2Housing.Describe(0,c)..shared.Lv2GPP.Describe(0,c);assert(report:find('BUILDING_LIBRARY') and report:find('Tier=') and report:find('BASE'));assert(writes==w);fire('LoadScreenClose');noErrors();assert(writes==w)")
l.execute("c.first={districtID=11,type='DISTRICT_SEOWON'};c.ds={};audit();noErrors();assert(housing(c)==0 and gpp(c,'RESEARCH')==0);local w=writes;audit();assert(writes==w)")
print('VALIDITY PASS temporary hold, all carrier preflight, confirmed withdrawal once, worker zero, reference loss/load, read-only diagnostic')
for n in [1,2,4,8]:
 l=runtime(n);l.execute("counters={};audit();noErrors()")
 assert l.eval("counters.facts")==2*n
 assert l.eval("counters.district_scan")==3*n # Housing batch+local capture; GPP batch
 print('SCALING',n,'facts',l.eval('counters.facts'),'districts',l.eval('counters.district_scan'),'building checks',l.eval('counters.building_check'),'city checks',l.eval('counters.city_scan'))
 l.execute("local r,w,f,ds=reads,writes,counters.facts,counters.district_scan;for i=1,10000 do fire('GameCoreEventPublishComplete');fire('GameCoreEventPlaybackComplete');fire('SystemUpdateUI');fire('UnitOperationStarted');fire('CityBuildingsChanged',0,1) end;assert(reads==r and writes==w and counters.facts==f and counters.district_scan==ds)")
 l.execute("fire('PlayerTurnActivated',0);local r,w=reads,writes;for i=1,10000 do fire('PlayerTurnActivated',0) end;assert(reads==r and writes==w);c.active=1;turn=turn+1;fire('PlayerTurnActivated',0);noErrors();assert(housing(c)==0 and gpp(c,'RESEARCH')==0)")
print('PERFORMANCE PASS 10000 unrelated pulses zero scans/writes; once/player/turn fallback repairs missed event; native carrier callbacks do not recurse')
# Preflight compatibility closure: all 50 historical housing candidates pass the
# same actual shared catalog; observed tier differences are explicit, not clamps.
f=json.loads((R/'DevelopmentTests/Fixtures/P0B2/housing_catalog.json').read_text())
l=runtime();l.globals().checked=ns['to_lua'](l,f['rows'])
catalog_setup="for _,r in ipairs(checked) do local found=false;for _,b in ipairs(brows) do if b.BuildingType==r.BuildingType then found=true end end;if not found then local b={};for k,v in pairs(r) do b[k]=v end;b.Index=20000+#brows;brows[#brows+1]=b;tiers[#tiers+1]=r end;for _,t in ipairs(tiers) do if t.BuildingType==r.BuildingType then t.Tier=r.Tier end end end;GameInfo.Buildings=db(brows,'BuildingType');GameInfo.HD_BuildingTiers=db(tiers,'BuildingType');local cat=SPCOrdinaryBuildingCatalog.Build(P);for _,r in ipairs(checked) do local b=cat.buildings[r.BuildingType];assert(b and b.ordinary and b.tier==r.Tier,r.BuildingType..':'..tostring(b and b.reason)) end"
l.execute(catalog_setup)
l.execute("setBuildings(d,{'BUILDING_RESEARCH_LAB','BUILDING_HD_DATA_CENTER'});audit();noErrors();assert(housing(c)==2);local w=writes;GameInfo.HD_BuildingTiers.BUILDING_HD_DATA_CENTER.Tier=5;fire('LoadScreenClose');assert(writes==w and shared.Lv2Housing.errors['0:1']);GameInfo.HD_BuildingTiers.BUILDING_HD_DATA_CENTER.Tier=4;fire('LoadScreenClose');noErrors();assert(writes==w)")
print('CATALOG PASS all50 retained/reclassified; Data Center actualTier4 shares tier with Lab; unsupportedTier5 holds, never clamps')
# All unchanged catalog candidates compare real old/new carrier maps, including
# nonempty specialty districts. Data Center is separately asserted above.
old,new=runtime(old=True),runtime()
for v in (old,new):v.globals().checked=ns['to_lua'](v,f['rows']);v.execute(catalog_setup)
for r in f['rows']:
 if r['classification']!='RETAIN':continue
 for v in (old,new):
  v.globals().building=r['BuildingType'];v.globals().domain=r['PrereqDistrict']
  v.execute("c.identity=P.Family(domain);d.type=GameInfo.Districts[domain].Index;setBuildings(d,{building});audit();noErrors()")
 assert old.eval('housing(c)')==new.eval('housing(c)')==2,r['BuildingType']
print('CATALOG DIFFERENTIAL PASS 49 nonempty valid old/new housing cases; Data Center difference explicit')
# Combined actual action dispatch includes both real Describe implementations.
l=runtime();l.execute("audit();noErrors();P.Scalar=tostring;stage=bomb;shared.Version=P.VERSION;Players[0].GetCities=function() return {Members=function() return pairs(cities) end,FindID=function(_,id) return cities[id] end} end")
g=(M/'Gameplay.lua').read_text();code=g[g.index('local function request('):g.index('GameEvents.SPC_P0_Request.Add')]
l.execute(code+"\nrunRequest=request")
l.execute("local w=writes;runRequest(0,{Action='COMPLETENESS_READ',Token='b2',CityID=1});assert(shared.LastToken=='b2' and shared.Snapshot:find('SHADOW_ONLY') and shared.Snapshot:find('P0%-B2 Lv2 Housing') and shared.Snapshot:find('P0%-B2 Lv2 GPP'));assert(writes==w)")
print('DIAGNOSTIC PASS actual combined request, real three modules, no writes')
# Source and manifest safety; SQL and Design byte equality versus pre-B2.
allowed={'Lv2Housing.lua','Lv2GPP.lua','OrdinaryBuildingCatalog.lua','Gameplay.lua','Probe.lua','UI/P0Panel.lua','UI/RuntimeAudit.lua','SpecializationP0.modinfo'}
for p in M.rglob('*'):
 if p.is_file() and str(p.relative_to(M)) not in allowed:assert p.read_bytes()==subprocess.check_output(['git','show','845cda1:Mod/'+str(p.relative_to(M))],cwd=R),p
for rel in subprocess.check_output(['git','ls-files','Specialization/Design'],cwd=R,text=True).splitlines():
 p=R/rel
 if p.is_file():assert p.read_bytes()==subprocess.check_output(['git','show','845cda1:'+str(p.relative_to(R))],cwd=R),p
assert ET.parse(M/'SpecializationP0.modinfo').getroot().get('version')=='107'
l=LuaRuntime();compile_lua=l.eval('function(s,n) local f,e=load(s,n); assert(f,e) end')
for p in M.rglob('*.lua'):compile_lua(p.read_text(),str(p))
print('STATIC PASS all Lua compile, SQL41 carriers/48GPP entries, modinfo107, non-B2 runtime and Design unchanged')
