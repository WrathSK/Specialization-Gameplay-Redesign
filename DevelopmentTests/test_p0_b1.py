"""P0-B1 actual Lua + SQLite cutover tests. Engine not launched; frozen tests unchanged."""
from pathlib import Path
import ast, subprocess, sqlite3, xml.etree.ElementTree as ET
from lupa.lua55 import LuaRuntime
R=Path(__file__).resolve().parents[1];M=R/'Mod'
c2=(R/'DevelopmentTests/test_arch_v2_c2.py').read_text()
tree=ast.parse(c2)
FIX=next(ast.literal_eval(n.value) for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='FIX' for t in n.targets))
# Newly required native contracts are explicit, never fallback success in production.
AUGMENT=r"""
P.Families={DISTRICT_CAMPUS='RESEARCH',DISTRICT_INDUSTRIAL_ZONE='INDUSTRY',DISTRICT_THEATER='CULTURE',DISTRICT_COMMERCIAL_HUB='COMMERCE'}
P.Family=function(t) return P.Families[t] or ({DISTRICT_SEOWON='RESEARCH',DISTRICT_HANSA='INDUSTRY',DISTRICT_ACROPOLIS='CULTURE',DISTRICT_SUGUBA='COMMERCE'})[t] end
local nativeDistrict=district
function district(...)
 local d=nativeDistrict(...);d.pillaged=false;d.IsPillaged=function() return d.pillaged end;return d
end
for _,d in pairs(districts) do d.pillaged=false;d.IsPillaged=function() return d.pillaged end end
"""
FIX+=AUGMENT
source=(R/'DevelopmentTests/test_arch_v2_d2.py').read_text();tree=ast.parse(source)
node=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='module_runtime')
# Same fixture/oracle owner as D2, compare to immediate pre-B1 runtime where needed.
code=ast.get_source_segment(source,node).replace('5dc6221','324f455')
exec(compile(code,'B1_module_fixture','exec'))
for mod in ['ResearchSupport','IndustrySupport']:
 for n in [1,2,4,8]:
  l=module_runtime(mod,n)
  for kind in ['RESEARCH','CULTURE','COMMERCE','INDUSTRY']:
   for active in [1,2,3,4]:
    for workers in [0,1,3]:
     l.execute(f"setup('{kind}',{active},{workers});if samples then samples() end;d.Audit();for _,err in pairs(d.errors) do assert(err==nil,err) end")
     l.globals().kind=kind
     if mod=='ResearchSupport':
      l.execute("for _,c in pairs(cities) do for _,k in ipairs({'RESEARCH','CULTURE','COMMERCE'}) do assert((c.built['BUILDING_SPC_DEV_'..k..'_SUPPORT']==true)==(kind==k)) end end")
     else:
      l.execute("for _,c in pairs(cities) do assert((c.built['BUILDING_SPC_DEV_INDUSTRY_LV1_-1']==true)==(kind=='INDUSTRY')) end")
  print(mod,n,'cities: all four professions x ACTIVE1..4 x workers0/1/3 PASS')
  l.execute("local w=writes;local f=total('facts');local c=total('city_scan');local ds=total('district_scan');pulse(10000);fire('GameCoreEventPlaybackComplete');fire('UnitOperationStarted');assert(writes==w and total('facts')==f and total('city_scan')==c and total('district_scan')==ds)")
  k='RESEARCH' if mod=='ResearchSupport' else 'INDUSTRY'
  l.execute(f"setup('{k}',4,2);if samples then samples() end;ExposedMembers.SPC_Performance=SPCPerformance.New();d.Audit();assert(total('facts')=={n} and total('district_scan')=={n})")
  print('SCALING',mod,n,'facts/districts=',l.eval("total('facts')"),l.eval("total('district_scan')"))
  l.execute("local w=writes;d.Audit();assert(writes==w);facts[1].active=nil;d.Audit();assert(writes==w and d.errors['0:1']);facts[1].active=4;d.Audit();assert(writes==w and not d.errors['0:1']);districts[11].pillaged=true;d.Audit();assert(writes>w);w=writes;d.Audit();assert(writes==w);districts[11].pillaged=false;d.Audit();assert(writes>w)")
  unique='DISTRICT_SEOWON' if mod=='ResearchSupport' else 'DISTRICT_HANSA'
  l.execute(f"districts[11].kind='{unique}';facts[1].first.type='{unique}';if samples then samples() end;d.Audit();assert(not d.errors['0:1'])")
  l.execute("local w=writes;districts[11].pillaged=nil;d.Audit();assert(writes==w and d.errors['0:1']);districts[11].pillaged=false;facts[1].specialization='NONE';facts[1].active=0;d.Audit();assert(writes>w);w=writes;d.Audit();assert(writes==w)")
  l.execute(f"setup('{k}',4,2);if samples then samples() end;d.Audit();local w=writes;facts[1].active=0;fire('GovernorChanged',0);assert(writes>w);w=writes;fire('GovernorChanged',0);assert(writes==w);facts[1].active=4;fire('GovernorPromoted',0);assert(writes>w);w=writes;districts[11].pillaged=true;fire('DistrictPillaged');assert(writes>w);districts[11].pillaged=false;fire('DistrictRepaired');local w=writes;if d.Run then d.Run(0,cities[1],'OFF');d.Run(0,cities[1],'ON') else d.Describe(0,cities[1]) end;assert(writes==w)")
 print(mod,'UNKNOWN hold / known pillage withdrawal once / repair / replacement / NONE PASS')
# Exact retirement; no prefix purge; calling the public old facade cannot resurrect.
l=module_runtime('Lv3Support',1)
l.execute("for _,id in ipairs(SPCSpecialistSupport.Retired) do cities[1].built[id]=true end;cities[1].built.BUILDING_SPC_DEV_LV3_POP_RESEARCH_0=true;d.Audit();assert(d.changes==12 and writes==12);local w=writes;for i=1,10000 do pulse();end;assert(writes==w);d.Audit();fire('LoadScreenClose');fire('GovernorPromoted');assert(writes==w and cities[1].built.BUILDING_SPC_DEV_LV3_POP_RESEARCH_0);assert(d.ruleset=='RETIRED_D0032_P0B1');for _,id in ipairs(SPCSpecialistSupport.Retired) do assert(not cities[1].built[id]) end")
print('CUTOVER PASS exact12 removed once; population carrier untouched; old Start/load/Audit never recreates')
# Cleanup failure blocks creation, and retry only performs remaining removals.
l=module_runtime('ResearchSupport',1)
l.execute("setup('RESEARCH',4,2);cities[1].built.BUILDING_SPC_DEV_LV3_RESEARCH=true;local remove=P.RemoveBuilding;P.RemoveBuilding=function() error('INTENTIONAL_RETIRE_FAILURE') end;d.Audit();assert(writes==0 and d.errors['0:1']);P.RemoveBuilding=remove;d.Audit();assert(cities[1].built.BUILDING_SPC_DEV_RESEARCH_SUPPORT and not cities[1].built.BUILDING_SPC_DEV_LV3_RESEARCH)")
# SQL executes real definitions, old IDs preserved but old yields inert.
db=sqlite3.connect(':memory:');db.executescript('CREATE TABLE Types(Type TEXT,Kind TEXT);CREATE TABLE Buildings(BuildingType TEXT,Name TEXT,Cost INTEGER,PrereqDistrict TEXT,InternalOnly INTEGER,CitizenSlots INTEGER,Housing INTEGER);CREATE TABLE Building_CitizenYieldChanges(BuildingType TEXT,YieldType TEXT,YieldChange INTEGER);')
for f in ['ResearchSupport','ConstantSupport','IndustrySupport','Lv3Support']:db.executescript((M/'Data'/f'{f}.sql').read_text())
assert db.execute("SELECT COUNT(*) FROM Buildings WHERE BuildingType LIKE 'BUILDING_SPC_DEV_LV3_%'").fetchone()[0]==12
assert db.execute("SELECT COUNT(*) FROM Building_CitizenYieldChanges WHERE BuildingType LIKE 'BUILDING_SPC_DEV_LV3_%'").fetchone()[0]==0
for k in ['RESEARCH','CULTURE','COMMERCE']:
 assert db.execute('SELECT YieldType,YieldChange FROM Building_CitizenYieldChanges WHERE BuildingType=? ORDER BY YieldType',('BUILDING_SPC_DEV_'+k+'_SUPPORT',)).fetchall()==[('YIELD_FOOD',3),('YIELD_PRODUCTION',3)]
# Full changed-file allowlist protects unrelated effects and properties.
allowed={'Data/Lv3Support.sql','Gameplay.lua','IndustrySupport.lua','Lv3Support.lua','Probe.lua','ResearchSupport.lua','SampleLifecycle.lua','SpecializationP0.modinfo','SpecialistSupport.lua','UI/IndustryRefresh.lua','UI/P0Panel.lua','UI/P0Panel.xml','UI/RuntimeAudit.lua'}
for p in M.rglob('*'):
 if p.is_file() and str(p.relative_to(M)) not in allowed:
  assert p.read_bytes()==subprocess.check_output(['git','show','324f455:Mod/'+str(p.relative_to(M))],cwd=R),p
assert 'local function historicalStart' in (M/'Lv3Support.lua').read_text()
assert (M/'Lv3Support.lua').read_text().count('historicalStart(')==1
assert 'shared.Lv3Support.Audit' not in (M/'Gameplay.lua').read_text()
assert 'shared.Lv3Support.Audit' not in (M/'IndustrySupport.lua').read_text()
print('SQL PASS 12 inert tombstones; base3F3P unchanged; Industry3F + binary BASE P unchanged')
# Actual panel initializes the named label; no new timer or hover request.
uifix=next(ast.literal_eval(n.value) for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='UI_FIX' for t in n.targets))
l=LuaRuntime(unpack_returned_tuples=True);l.execute(uifix);l.execute("Controls.CompletenessButtonCaption.SetText=function(c,t) caption=t end;P.Scalar=tostring;print=function() end")
l.execute((M/'UI/P0Panel.lua').read_text());l.execute("init();assert(caption=='区域完善度 / 科研影子');for i=1,10000 do fire('SystemUpdateUI') end;assert(sends==0)")
x=ET.parse(M/'UI/P0Panel.xml').getroot();assert x.find('.//Label[@ID="CompletenessButtonCaption"]').get('Color')=='255,255,255,255'
print('UI PASS explicit Chinese caption init/color, idle sends0; visual game confirmation pending')
# Frozen C2 lifecycle tests use explicit direct-dirty signals introduced in D2.
# ONLY tests requiring retired Lv3 output are excluded; their replacement is the
# exact12 cleanup/sterile-SQL gate above, not an equality-to-old-design assertion.
a=c2.index('# Include actual Lv3 downstream carriers');b=c2.index('# Unknown native completion status',a);c2=c2[:a]+c2[b:]
a=c2.index('# Industry Lv3 must not undo');b=c2.index("l=runtime('copy');",a);c2=c2[:a]+c2[b:]
c2=c2.replace("def runtime(k,old=False):",'FIX += '+repr(AUGMENT)+"\ndef runtime(k,old=False):")
c2=c2.replace("name=='SampleLifecycle'", "name in ('SampleLifecycle','RuntimeWork','SpecialistSupport')")
c2=c2.replace("get('version')=='102'", "get('version')=='106'").replace('P0-B-075.102','P0-B-079.106').replace("get('version')=='102'", "get('version')=='106'")
# Nested D1 stamp adaptation targets this build too.
if '--regression' in __import__('sys').argv:
 d2=source.replace("s=(R/'DevelopmentTests/test_arch_v2_c2.py').read_text()",'s=C2_SOURCE')
 d2=d2.replace("'Lv3Effects','Lv3Support','Lv4Percent'","'Lv3Effects','Lv4Percent'")
 d2=d2.replace("get('version')=='103'", "get('version')=='106'").replace('P0-B-076.103','P0-B-079.106')
 exec(compile(d2,'D2_B1_intended_retirement','exec'),{'__file__':str(R/'DevelopmentTests/test_arch_v2_d2.py'),'C2_SOURCE':c2})
 # Preserve all P0-A assertions except the exact old-writer byte allowlist and build.
 p0=(R/'DevelopmentTests/test_p0_a.py').read_text().replace('P0-B-078.105','P0-B-079.106').replace("get('version')=='105'","get('version')=='106'")
 p0=p0.replace("'ResearchSupport.lua',",'').replace("'Lv3Support.lua',",'').replace("'IndustrySupport.lua',",'')
 p0=p0.replace("for p in (M/'Data').glob('*'):","for p in (M/'Data').glob('*'):\n if p.name=='Lv3Support.sql':continue")
 p0=p0.replace('manifest105; old effect writers and Data unchanged','manifest106; non-B1 effect writers/Data unchanged (explicit B1 allowlist)')
 exec(compile(p0,'P0A_B1_approved_writer_deltas','exec'),{'__file__':str(R/'DevelopmentTests/test_p0_a.py')})
print('P0-B1 LOCAL_SIMULATION_PASS (not engine PASS)')
