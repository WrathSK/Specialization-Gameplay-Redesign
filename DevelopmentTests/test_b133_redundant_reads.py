"""Bounded current-vs-B132 actual Lua tests. L2 tests; no engine or deployment."""
from pathlib import Path
import subprocess
from lupa.lua55 import LuaRuntime
R=Path(__file__).resolve().parents[1]
M=R/'Mod'
def old(name):
    return subprocess.check_output(['git','show','c225aa0:Mod/'+name],cwd=R,text=True)
p=R/'DevelopmentTests/test_p0_b2.py';ns={'__file__':str(p)}
exec(compile(p.read_text().split('for kind,domain in ')[0],str(p),'exec'),ns)
def runtime(source, pid=7):
    l=ns['runtime']()
    l.execute(source)
    l.execute('SPCLv2GPP.Start(P,shared);shared.Lv2GPP.ready=true')
    l.execute(f'''
      local player=Players[0];Players={{[{pid}]=player}};c.owner={pid};P.IsTestPlayer=function(id)return id=={pid} end
      local oldRead=P.HasBuilding;carrierReads=0;readsBeforeFirstWrite=nil;writeOrder={{}}
      P.HasBuilding=function(b,id)carrierReads=carrierReads+1;return oldRead(b,id)end
      local create,remove=P.CreateBuilding,P.RemoveBuilding
      P.CreateBuilding=function(q,id)
        readsBeforeFirstWrite=readsBeforeFirstWrite or carrierReads;writeOrder[#writeOrder+1]='ADD:'..id;create(q,id)
      end
      P.RemoveBuilding=function(b,id)
        readsBeforeFirstWrite=readsBeforeFirstWrite or carrierReads;writeOrder[#writeOrder+1]='REMOVE:'..id;remove(b,id)
      end
      function resetObs()carrierReads=0;readsBeforeFirstWrite=nil;writeOrder={{}}end
      function run()shared.Lv2GPP.Audit({{player={pid}}});assert(not shared.Lv2GPP.errors['{pid}:1'],shared.Lv2GPP.errors['{pid}:1'])end
      function signature()
        local a={{}};for id,yes in pairs(c.carriers)do if yes then a[#a+1]=id end end;table.sort(a);return table.concat(a,',')
      end
      function removalFirst()
        local added=false;for _,x in ipairs(writeOrder)do if x:find('ADD:',1,true)==1 then added=true else assert(not added,'REMOVE_AFTER_ADD')end end
        if #writeOrder>0 then assert(readsBeforeFirstWrite>=32,'WRITE_BEFORE_COMPLETE_PREFLIGHT')end
      end
    ''')
    return l
sources=[old('Lv2GPP.lua'),(M/'Lv2GPP.lua').read_text()]
checks=[];cases=0
for kind,domain in [('RESEARCH','CAMPUS'),('CULTURE','THEATER'),('INDUSTRY','INDUSTRIAL_ZONE'),('COMMERCE','COMMERCIAL_HUB')]:
    pair=[runtime(src) for src in sources]
    for active,workers in [(1,0),(2,1),(4,3),(4,255),(4,2),(4,0),(1,3),(2,3)]:
        outputs=[]
        for v in pair:
            v.execute(f"c.identity='{kind}';d.type=GameInfo.Districts.DISTRICT_{domain}.Index;c.active={active};d.workers={workers};resetObs();run();removalFirst()")
            outputs.append((v.eval('signature()'),v.eval('writes'),v.eval("table.concat(writeOrder,',')")))
            v.execute('local w=writes;resetObs();run();assert(writes==w)')
        assert outputs[0]==outputs[1],(kind,active,workers,outputs)
        checks.append([v.eval('carrierReads') for v in pair]);cases+=1
    for v in pair:
        v.execute('''
          local w=writes;local before=signature();c.active=1
          unknownCarrier=GameInfo.Buildings.BUILDING_SPC_DEV_GPP_COMMERCE_7.Index
          shared.Lv2GPP.Audit({player=7});assert(writes==w and signature()==before and shared.Lv2GPP.errors['7:1'])
          unknownCarrier=nil;c.active=4;run();assert(writes==w)
          c.factsError=true;shared.Lv2GPP.Audit({player=7});assert(writes==w and signature()==before)
          c.factsError=false;d.workers=nil;shared.Lv2GPP.Audit({player=7});assert(writes==w and signature()==before)
          d.workers=3;run();assert(writes==w)
          c.owner=9;run();assert(signature()=='')
          c.owner=7;run();assert(signature()==before)
        ''')
assert all(a==64 and b==32 for a,b in checks),checks
print('GPP PASS: nonzero player7, 32 sequential old/new carrier+write+ordering cases; stable64->32; complete preflight, UNKNOWN hold, foreign withdrawal and return')
# The existing actual handler hooks are unchanged by this proposed local optimization.
# Probe.Family is isolated verbatim from actual old/current sources.
def family_source(source):
    return source[source.index('function P.Family(districtType)'):source.index('-- Pure test oracle;')]
u=LuaRuntime(unpack_returned_tuples=True)
u.execute('''
 P={Families={DISTRICT_CAMPUS='RESEARCH',DISTRICT_THEATER='CULTURE',DISTRICT_INDUSTRIAL_ZONE='INDUSTRY',DISTRICT_COMMERCIAL_HUB='COMMERCE'}}
 rows={
  {CivUniqueDistrictType='DISTRICT_SEOWON',ReplacesDistrictType='DISTRICT_CAMPUS'},
  {CivUniqueDistrictType='DISTRICT_CHAIN',ReplacesDistrictType='DISTRICT_SEOWON'},
  {CivUniqueDistrictType='DISTRICT_LOOP_A',ReplacesDistrictType='DISTRICT_LOOP_B'},
  {CivUniqueDistrictType='DISTRICT_LOOP_B',ReplacesDistrictType='DISTRICT_LOOP_A'},
  {CivUniqueDistrictType='DISTRICT_CAMPUS',ReplacesDistrictType='DISTRICT_THEATER'},
  {CivUniqueDistrictType='DISTRICT_DUP',ReplacesDistrictType='DISTRICT_CAMPUS'},
  {CivUniqueDistrictType='DISTRICT_DUP',ReplacesDistrictType='DISTRICT_THEATER'}
 }
 reads=0;P.Rows=function(name)assert(name=='DistrictReplaces');reads=reads+1;if absent then return nil end;return rows end
''')
u.execute(family_source(old('Probe.lua'))+'\noldFamily=P.Family')
u.execute(family_source((M/'Probe.lua').read_text())+'\nnewFamily=P.Family')
for absent in [False,True]:
    u.globals().absent=absent
    for key in [None,False,'DISTRICT_CAMPUS','DISTRICT_THEATER','DISTRICT_INDUSTRIAL_ZONE','DISTRICT_COMMERCIAL_HUB','DISTRICT_SEOWON','DISTRICT_CHAIN','DISTRICT_LOOP_A','DISTRICT_DUP','DISTRICT_UNKNOWN']:
        u.globals().key=key
        u.execute('reads=0;a=oldFamily(key);oldReads=reads;reads=0;b=newFamily(key);newReads=reads;assert(a==b)')
        if key in ['DISTRICT_CAMPUS','DISTRICT_THEATER','DISTRICT_INDUSTRIAL_ZONE','DISTRICT_COMMERCIAL_HUB']:
            assert u.eval('oldReads')==1 and u.eval('newReads')==0
print('FAMILY PASS: same values for 22 base/replacement/chain/cycle/duplicate/unknown/absent cases; direct bases rows1->0')

# D static catalog reuses complete reviewed metadata; real city state remains live.
def depth_runtime(previous=False):
    v=ns['ns']['runtime']()
    if previous:
        v.execute(old('DistrictCompleteness.lua'))
        v.execute('SPCDistrictCompleteness.Start(P,shared);svc=shared.DistrictCompleteness')
    v.execute("""
      dbPasses=0;local mt=getmetatable(GameInfo.Buildings);local iterate=mt.__call
      mt.__call=function(...)dbPasses=dbPasses+1;return iterate(...)end
      function depth()return svc.Read(0,c,c.token)end
    """)
    return v

def native_table(v):
    if hasattr(v,'items'): return {k:native_table(x) for k,x in v.items()}
    return v
oldD,newD=depth_runtime(True),depth_runtime()
traces=[
 "setBuildings(d,{})",
 "setBuildings(d,{'BUILDING_LIBRARY'})",
 "setBuildings(d,{'BUILDING_LIBRARY','BUILDING_UNIVERSITY','BUILDING_JNR_LABORATORY','BUILDING_RESEARCH_LAB'})",
 "setBuildings(d,{'BUILDING_LIBRARY','BUILDING_UNKNOWN_MOD','BUILDING_WONDER','BUILDING_SPC_INTERNAL','BUILDING_FAKE_DUMMY'});d.bs[1].pillaged=true;d.bs[3].location=9999;c.queued='BUILDING_UNIVERSITY'",
 "c.queued=nil;setBuildings(d,{'BUILDING_MADRASA'});d.type=GameInfo.Districts.DISTRICT_SEOWON.Index",
 "d.pillaged=true",
 "d.pillaged=false;d.complete=false",
 "d.complete=true;d2=addDistrict(c,12,'DISTRICT_CAMPUS');setBuildings(d2,{'BUILDING_LIBRARY','BUILDING_UNIVERSITY'});d.type=GameInfo.Districts.DISTRICT_CAMPUS.Index",
]
for trace in traces:
    vals=[]
    for v in (oldD,newD):
        v.execute(trace+';svc.MarkDirty();v=depth();assert(v.validity=="VERIFIED" and v.availability=="READY" and writes==0)')
        vals.append(native_table(v.eval('v')))
    assert vals[0]==vals[1],trace
assert oldD.eval('dbPasses')==9 and newD.eval('dbPasses')==1
newD.execute("""
 local cap=counters.dc_capture;depth();assert(counters.dc_capture==cap)
 -- Known other owner doesn't dirty owner0. Unknown/invalid event metadata does.
 fire('BuildingAddedToMap',0,0,GameInfo.Buildings.BUILDING_LIBRARY.Index,3);depth();assert(counters.dc_capture==cap)
 fire('BuildingRemovedFromMap',0,0,GameInfo.Buildings.BUILDING_LIBRARY.Index,3);depth();assert(counters.dc_capture==cap)
 fire('BuildingAddedToMap',0,0,GameInfo.Buildings.BUILDING_LIBRARY.Index,0);depth();assert(counters.dc_capture==cap+1)
 for _,owner in ipairs({-1,0.5,'0',math.huge})do
  local n=counters.dc_capture;fire('BuildingRemovedFromMap',0,0,GameInfo.Buildings.BUILDING_LIBRARY.Index,owner);depth();assert(counters.dc_capture==n+1)
 end
 local n=counters.dc_capture;fire('BuildingRemovedFromMap');depth();assert(counters.dc_capture==n+1)
 local n=counters.dc_capture;fire('BuildingAddedToMap',0,0,GameInfo.Buildings.BUILDING_SPC_INTERNAL.Index,0);depth();assert(counters.dc_capture==n)
 -- No eligibility narrowing for the cache producer: scoped to actual owner ID.
 P.IsTestPlayer=function(pid)return pid==0 or pid==7 end
 c7=newCity(7,7);local d7=addDistrict(c7,77,'DISTRICT_CAMPUS');setBuildings(d7,{'BUILDING_LIBRARY'})
 svc.Read(7,c7,c7.token);local n=counters.dc_capture
 fire('BuildingAddedToMap',0,0,GameInfo.Buildings.BUILDING_LIBRARY.Index,7)
 depth();assert(counters.dc_capture==n);svc.Read(7,c7,c7.token);assert(counters.dc_capture==n+1)
 -- Transfer still invalidates all; no stale token/reference reuse, unknown held.
 fire('CityTransfered',7,1,0);local n=counters.dc_capture;depth();svc.Read(7,c7,c7.token);assert(counters.dc_capture==n+2)
 failRead=true;svc.MarkDirty();v=depth();assert(v.availability=='TEMPORARILY_UNAVAILABLE' and v.value)
 failRead=false;turn=turn+1;v=depth();assert(v.availability=='READY')
 local n=counters.dc_capture;c.token='REPLACED';depth();assert(counters.dc_capture==n+1)
 local n=dbPasses;fire('LoadScreenClose');depth();assert(dbPasses==n+1)
 assert(writes==0)
""")
print('DEPTH PASS: old/new complete output for 8 ontology/lifecycle cases; 9->1 DB enumerations; owner isolation, UNKNOWN/full fallback, transfer/reference/load/turn')
# Real affected consumers exercise same-turn invalidation and unknown handling.
b=ns['runtime']()
b.execute("""
 local read=shared.EffectiveFacts.Read
 shared.EffectiveFacts.Read=function(pid,c)local f=read(pid,c);f.token=c.token;return f end
 setBuildings(d,{'BUILDING_LIBRARY','BUILDING_UNIVERSITY'});audit();noErrors();assert(housing(c)==3)
 d.bs[1].pillaged=true;fire('BuildingPillaged');noErrors();assert(housing(c)==2)
 d.bs[1].pillaged=false;fire('BuildingRepaired');noErrors();assert(housing(c)==3)
 setBuildings(d,{'BUILDING_LIBRARY'});fire('BuildingRemovedFromMap',0,0,GameInfo.Buildings.BUILDING_UNIVERSITY.Index,0);noErrors();assert(housing(c)==2)
 c.factsError=true;local w=writes;audit();assert(writes==w)
 c.factsError=false;c.active=1;audit();noErrors();assert(housing(c)==0 and gpp(c,'RESEARCH')==0)
 c.active=4;audit();noErrors();assert(housing(c)==2)
 c.owner=3;fire('CityTransfered',3,1,0);assert(housing(c)==0 and gpp(c,'RESEARCH')==0)
""")
p=R/'DevelopmentTests/test_p0_c.py';cf={'__file__':str(p)}
exec(compile(p.read_text().split('l=runtime()')[0],str(p),'exec'),cf)
c=cf['runtime']()
c.execute("""
 setBuildings(d,{'BUILDING_LIBRARY','BUILDING_UNIVERSITY'});seedOld();audit();good();retired();assert(coeff(c)==3)
 d.bs[1].pillaged=true;fire('BuildingPillaged');good();assert(coeff(c)==2)
 d.bs[1].pillaged=false;fire('BuildingRepaired');good();assert(coeff(c)==3)
 failRead=true;fire('BuildingRepaired');local w=writes;audit();assert(writes==w and coeff(c)==3)
 failRead=false;turn=turn+1;fire('PlayerTurnActivated',0);good();assert(coeff(c)==3)
 c.active=3;audit();good();assert(coeff(c)==0)
 c.active=4;fire('GovernorChanged',0);good();assert(coeff(c)==3)
""")
print('CONSUMERS PASS: actual Housing/GPP/Infrastructure updates, current eligibility, UNKNOWN hold, repair, same-turn removal, next-turn reconciliation')
# Ownership entry points, event subscriptions and writing primitives untouched.
for name in ['DistrictCompleteness.lua','Lv2GPP.lua']:
    now=(M/name).read_text();before=old(name);marker=' if shared.CityProgressionStore then'
    assert now[now.index(marker):]==before[before.index(marker):],name
v=LuaRuntime()
for name in ['DistrictCompleteness.lua','Lv2GPP.lua','Probe.lua']: v.execute('assert(load(...))',(M/name).read_text())
import xml.etree.ElementTree as ET
assert ET.parse(M/'SpecializationP0.modinfo').getroot().get('version')=='160'
print('STATIC PASS: Lua syntax, modinfo160, unchanged module-owned ownership callbacks')
