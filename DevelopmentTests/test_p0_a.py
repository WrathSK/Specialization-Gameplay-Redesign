"""P0-A actual Lua read-only fact/shadow tests; native APIs mocked, no deployment."""
from pathlib import Path
import json, subprocess, xml.etree.ElementTree as ET, ast
from lupa.lua55 import LuaRuntime
R=Path(__file__).resolve().parents[1];M=R/'Mod'
NEW=['OrdinaryBuildingCatalog','DistrictCompleteness','CurrentSpecializationFacts','ResearchInfrastructureShadow']
FIX=r'''
turn=1;reads=0;writes=0;hooks={};counters={};failRead=false
function event(name) return {Add=function(f) hooks[name]=hooks[name] or {};table.insert(hooks[name],f) end} end
Events=setmetatable({},{__index=function(t,k) local e=event(k);rawset(t,k,e);return e end});GameEvents=Events
function fire(n,...) for _,f in ipairs(hooks[n] or {}) do f(...) end end
Game={GetCurrentGameTurn=function() return turn end}
ExposedMembers={};GameInfo={};Map={};Locale={Lookup=function(s) return s end}
function bomb() writes=writes+1;error('P0A_WRITE_FORBIDDEN') end
function db(rows,key)
 local t={};for _,r in ipairs(rows) do t[r[key]]=r;if r.Index~=nil then t[r.Index]=r end end
 return setmetatable(t,{__call=function() local i=0;return function() i=i+1;return rows[i] end end})
end
P={VERSION='P0-B-077.104',IsTestPlayer=function(p) return p==0 or p==1 end,Field=function(t,k) return t[k] end,
 Count=function(n) counters[n]=(counters[n] or 0)+1 end,CreateBuilding=bomb,RemoveBuilding=bomb,SetProperty=bomb}
function P.Info(t,k) return k~=nil and GameInfo[t][k] or nil end
local types={'CAMPUS','THEATER','INDUSTRIAL_ZONE','COMMERCIAL_HUB','HARBOR','ENCAMPMENT','HOLY_SITE','GOVERNMENT','DIPLOMATIC_QUARTER','NEIGHBORHOOD','CITY_CENTER','SEOWON','UNKNOWN'}
local rows={};for i,t in ipairs(types) do rows[#rows+1]={Index=i,DistrictType='DISTRICT_'..t} end
GameInfo.Districts=db(rows,'DistrictType');GameInfo.DistrictReplaces=db({{CivUniqueDistrictType='DISTRICT_SEOWON',ReplacesDistrictType='DISTRICT_CAMPUS'}},'CivUniqueDistrictType')
cities={};allDistricts={}
local objects={};function Map.GetPlot(x,y) return objects[x] end;function Map.GetPlotByIndex(id) return objects[id] end
function newCity(id,owner)
 local c={id=id,owner=owner or 0,x=id*100,y=1,ds={},token='city'..id,queued=nil}
 c.GetID=function() return c.id end;c.GetOwner=function() return c.owner end;c.GetX=function() return c.x end;c.GetY=function() return c.y end
 c.SetProperty=bomb;c.GetProperty=function(_,key) return key=='SPC_DEV_INVESTMENT_LEDGER_V1' and c.ledger or nil end
 c.GetBuildQueue=function() return {CurrentlyBuilding=function() reads=reads+1;return c.queued end,CreateBuilding=bomb} end
 c.GetDistricts=function() return {Members=function() reads=reads+1;return ipairs(c.ds) end} end
 c.GetBuildings=function() return {SetPillaged=bomb,RemoveBuilding=bomb,
  GetBuildingsAtLocation=function(_,plot) reads=reads+1;if failRead then error('TEMPORARY_NATIVE_UNAVAILABLE') end
   for _,d in ipairs(c.ds) do if d.plot==plot then local out={};for _,b in ipairs(d.bs) do out[#out+1]=b.index end;return out end end;error('NO_DISTRICT') end,
  HasBuilding=function(_,id) reads=reads+1;for _,d in ipairs(c.ds) do for _,b in ipairs(d.bs) do if b.index==id then return b.complete end end end;return false end,
  IsPillaged=function(_,id) reads=reads+1;for _,d in ipairs(c.ds) do for _,b in ipairs(d.bs) do if b.index==id then return b.pillaged end end end;return false end} end
 cities[id]=c;return c
end
function addDistrict(c,id,kind)
 local d={id=id,type=GameInfo.Districts[kind].Index,plot=c.x+id,complete=true,pillaged=false,workers=3,bs={}}
 d.GetID=function() return d.id end;d.GetType=function() return d.type end;d.GetX=function() return d.plot end;d.GetY=function() return 0 end;d.GetCity=function() return c end
 d.IsComplete=function() return d.complete end;d.IsPillaged=function() return d.pillaged end
 objects[d.plot]={GetIndex=function() return d.plot end,GetWorkerCount=function() reads=reads+1;return d.workers end}
 c.ds[#c.ds+1]=d;allDistricts[id]=d;return d
end
function setBuildings(d,names)
 d.bs={};for _,name in ipairs(names) do d.bs[#d.bs+1]={index=GameInfo.Buildings[name].Index,complete=true,pillaged=false} end
end
Players={[0]={},[1]={}}
for _,p in pairs(Players) do
 p.GetDistricts=function() return {FindID=function(_,id) reads=reads+1;return allDistricts[id] end,Members=function() error('NO_PLAYER_WIDE_SCAN') end} end
 p.GetCities=function() return {FindID=function(_,id) return cities[id] end} end
end
shared={EffectiveFacts={Read=function(pid,c) P.Count('facts');if c.factsError then error('TEMPORARY_FLOW') end
 return {owner=pid,cityID=c.id,specialization=c.identity or 'RESEARCH',potential=4,active=c.active,activeStatus=c.active and 'KNOWN' or 'UNKNOWN_GOVERNOR',token=c.token,first={districtID=c.ds[1].id,type=GameInfo.Districts[c.ds[1].type].DistrictType}}
end}}
'''

def to_lua(l,x):
 if isinstance(x,dict):return l.table_from({k:to_lua(l,v) for k,v in x.items()})
 if isinstance(x,list):return l.table_from([to_lua(l,v) for v in x])
 return x

def runtime():
 l=LuaRuntime(unpack_returned_tuples=True);l.execute(FIX)
 fixture=json.loads((R/'DevelopmentTests/Fixtures/P0A/catalog.json').read_text())
 buildings=[]
 for i,r in enumerate(fixture['rows'],1): buildings.append(dict(r,Index=i,Name=r['BuildingType'],InternalOnly=False,IsWonder=False))
 for r in [dict(BuildingType='BUILDING_UNKNOWN_MOD',PrereqDistrict='DISTRICT_CAMPUS'),dict(BuildingType='BUILDING_PALACE',PrereqDistrict='DISTRICT_CITY_CENTER'),dict(BuildingType='BUILDING_WONDER',PrereqDistrict='DISTRICT_CAMPUS',IsWonder=True),dict(BuildingType='BUILDING_SPC_INTERNAL',PrereqDistrict='DISTRICT_CAMPUS'),dict(BuildingType='BUILDING_FAKE_DUMMY',PrereqDistrict='DISTRICT_CAMPUS')]:
  buildings.append(dict(InternalOnly=False,IsWonder=False,**{k:v for k,v in r.items() if k not in ['IsWonder','InternalOnly']},Index=len(buildings)+1));buildings[-1].update(r)
 l.globals().brows=to_lua(l,buildings);l.globals().tiers=to_lua(l,fixture['rows']);l.globals().replaces=to_lua(l,fixture['replaces'])
 l.execute("GameInfo.Buildings=db(brows,'BuildingType');GameInfo.HD_BuildingTiers=db(tiers,'BuildingType');GameInfo.HD_DUMMY_BUILDINGS=db({{BuildingType='BUILDING_FAKE_DUMMY'}},'BuildingType');GameInfo.BuildingReplaces=db(replaces,'CivUniqueBuildingType')")
 for n in NEW:l.execute((M/(n+'.lua')).read_text())
 l.execute("SPCDistrictCompleteness.Start(P,shared);svc=shared.DistrictCompleteness;c=newCity(1);c.active=4;d=addDistrict(c,11,'DISTRICT_CAMPUS');cat=SPCOrdinaryBuildingCatalog.Build(P)")
 return l

l=runtime()
# All reviewed rows either loaded with a supported normalized tier or explicitly diagnosed.
l.execute("for _,r in ipairs(brows) do if cat.buildings[r.Index].ordinary then assert(cat.buildings[r.Index].tier~=nil, r.BuildingType..':'..tostring(cat.buildings[r.Index].reason)) end end")
seq=[([],0),(['BUILDING_LIBRARY'],1),(['BUILDING_LIBRARY','BUILDING_UNIVERSITY'],3),(['BUILDING_LIBRARY','BUILDING_UNIVERSITY','BUILDING_JNR_LABORATORY'],6),(['BUILDING_LIBRARY','BUILDING_UNIVERSITY','BUILDING_JNR_LABORATORY','BUILDING_RESEARCH_LAB'],10),(['BUILDING_JNR_LABORATORY'],3),(['BUILDING_LIBRARY','BUILDING_JNR_ACADEMY'],2),(['BUILDING_JNR_LABORATORY','BUILDING_JNR_ARCHITECTURE','BUILDING_JNR_LIBERAL_ARTS','BUILDING_RESEARCH_LAB'],10)]
for names,want in seq:
 l.globals().names=to_lua(l,names);l.globals().expected=want
 l.execute("setBuildings(d,names);svc.MarkDirty();v=svc.Read(0,c,c.token);assert(v.validity=='VERIFIED' and v.availability=='READY');assert(v.value.domains.DISTRICT_CAMPUS.value==expected);assert(writes==0)")
print('D PASS 0/1/3/6/10; missing lower tiers; same-tier sum; 13 capped10')
l.execute("assert(v.value.districts[1].uncapped==13);setBuildings(d,{'BUILDING_LIBRARY','BUILDING_MADRASA','BUILDING_UNKNOWN_MOD','BUILDING_WONDER','BUILDING_SPC_INTERNAL','BUILDING_FAKE_DUMMY'});d.bs[1].pillaged=true;d.bs[2].complete=false;svc.MarkDirty();v=svc.Read(0,c,c.token);assert(v.value.domains.DISTRICT_CAMPUS.value==0)")
l.execute("reasons={};for _,b in ipairs(v.value.districts[1].buildings) do reasons[b.type]=b.reason end;assert(reasons.BUILDING_LIBRARY=='BUILDING_PILLAGED');assert(reasons.BUILDING_MADRASA=='UNDER_CONSTRUCTION');assert(reasons.BUILDING_UNKNOWN_MOD=='UNREVIEWED_BUILDING');assert(reasons.BUILDING_SPC_INTERNAL=='INTERNAL_OR_TECHNICAL');assert(reasons.BUILDING_WONDER=='WONDER');assert(reasons.BUILDING_FAKE_DUMMY=='INTERNAL_OR_TECHNICAL')")
l.execute("setBuildings(d,{'BUILDING_MADRASA'});svc.MarkDirty();v=svc.Read(0,c,c.token);assert(v.value.domains.DISTRICT_CAMPUS.value==2);assert(v.value.districts[1].buildings[1].tierSource=='REPLACEMENT_TIER');d.type=GameInfo.Districts.DISTRICT_SEOWON.Index;svc.MarkDirty();assert(svc.Read(0,c,c.token).value.domains.DISTRICT_CAMPUS.value==2)")
l.execute("d2=addDistrict(c,12,'DISTRICT_CAMPUS');setBuildings(d2,{'BUILDING_RESEARCH_LAB'});svc.MarkDirty();v=svc.Read(0,c,c.token);assert(v.value.domains.DISTRICT_CAMPUS.value==4 and v.value.domains.DISTRICT_CAMPUS.districtID==12)")
l.execute("d2.pillaged=true;fire('OnPillage');assert(svc.Read(0,c,c.token).value.domains.DISTRICT_CAMPUS.value==2);d.complete=false;fire('DistrictBuildProgressChanged');assert(svc.Read(0,c,c.token).value.domains.DISTRICT_CAMPUS==nil);d.complete=true;d2.pillaged=false;fire('CityBuildingsChanged',0,1)")
print('D PASS explicit exclusions, replacement tier, unique district, highest single district, district pillage/unfinished')
# Same result = same revision; detached returned data cannot corrupt authority.
l.execute("v=svc.Read(0,c,c.token);rev=v.revision;v.value.domains.DISTRICT_CAMPUS.value=999;svc.MarkDirty();v=svc.Read(0,c,c.token);assert(v.revision==rev and v.value.domains.DISTRICT_CAMPUS.value==4)")
l.execute("local before=reads;local caps=counters.dc_capture;for i=1,10000 do fire('GameCoreEventPublishComplete');fire('GameCoreEventPlaybackComplete');fire('UnitOperationStarted');fire('SystemUpdateUI') end;assert(reads==before and counters.dc_capture==caps and writes==0)")
l.execute("local before=reads;local caps=counters.dc_capture;for i=1,10000 do fire('BuildingPillaged') end;assert(reads==before and counters.dc_capture==caps);svc.Read(0,c,c.token);assert(counters.dc_capture==caps+1)")
print('PERF PASS 10000 unrelated pulses: reads/scans/writes0; 10000 direct dirty marks coalesce to one on-demand capture')
# Failure holds verified sample, bounded retries; confirmed removal yields a new zero.
l.execute("failRead=true;svc.MarkDirty();v=svc.Read(0,c,c.token);assert(v.validity=='VERIFIED' and v.availability=='TEMPORARILY_UNAVAILABLE' and v.value.domains.DISTRICT_CAMPUS.value==4);local caps=counters.dc_capture;for i=1,10000 do svc.Read(0,c,c.token) end;assert(counters.dc_capture==caps)")
l.execute("failRead=false;turn=turn+1;v=svc.Read(0,c,c.token);assert(v.availability=='READY');d2.bs={};d.bs={};fire('BuildingRemovedFromMap');v=svc.Read(0,c,c.token);assert(v.value.domains.DISTRICT_CAMPUS.value==0 and v.revision>rev)")
l.execute("setBuildings(d,{'BUILDING_LIBRARY'});local rev=v.revision;turn=turn+1;v=svc.Read(0,c,c.token);assert(v.value.domains.DISTRICT_CAMPUS.value==1 and v.revision>rev)")
l.execute("failRead=true;c.token='new-city';v=svc.Read(0,c,c.token);assert(v.validity=='UNKNOWN' and v.value==nil);failRead=false;oldEpoch=v.epoch;fire('LoadScreenClose');assert(svc.CacheSize()==0);v=svc.Read(0,c,c.token);assert(v.epoch==oldEpoch+1)")
print('LIFECYCLE PASS same-input suppression, temporary hold, bounded failure, missed-event turn reconcile, confirmed removal, reference and epoch')
# Shadow actual facade, no old writer calls.
l.execute("setBuildings(d,{'BUILDING_LIBRARY','BUILDING_UNIVERSITY'});d.type=GameInfo.Districts.DISTRICT_CAMPUS.Index;d.workers=3;svc.MarkDirty();f=SPCCurrentSpecializationFacts.Read(P,shared,0,c);v=svc.Read(0,c,f.token);p=SPCResearchInfrastructureShadow.Plan(SPCResearchInfrastructureShadow.WithWorkers(f,v),v);assert(p.science==18 and p.appliedScience==0 and p.status=='READY');c.active=3;f=SPCCurrentSpecializationFacts.Read(P,shared,0,c);assert(SPCResearchInfrastructureShadow.Plan(f,v).science==0);c.active=nil;f=SPCCurrentSpecializationFacts.Read(P,shared,0,c);assert(SPCResearchInfrastructureShadow.Plan(f,v).science==nil);c.active=4;d.workers=0;d2.workers=0;assert(SPCResearchInfrastructureShadow.Plan(SPCResearchInfrastructureShadow.WithWorkers(SPCCurrentSpecializationFacts.Read(P,shared,0,c),v),v).science==0)")
l.execute("d.workers=3;failRead=true;svc.MarkDirty();v=svc.Read(0,c,c.token);assert(SPCResearchInfrastructureShadow.Plan(SPCCurrentSpecializationFacts.Read(P,shared,0,c),v).status=='HELD_COMPLETENESS');failRead=false;turn=turn+1;report=SPCResearchInfrastructureShadow.Describe(P,shared,0,c);assert(report:find('contribution=') and report:find('tierSource=') and report:find('cap前=') and report:find('最高单区域=') and report:find('SHADOW_ONLY'));assert(writes==0)")
print('SHADOW PASS D3 × 6 working specialists across two Campuses = Science18; applied0; ACTIVE3/UNKNOWN/worker0/temporary hold; explanatory diagnostic')
# Actual existing EffectiveFacts, not only mocked adapter input.
l.execute((M/'EffectiveFacts.lua').read_text())
l.execute("foundation={owner=0,cityID=c.id,token=c.token,specialization='RESEARCH',potential=1,first={districtID=d.id,type='DISTRICT_CAMPUS'}};shared.CityFlowProbe={SupportFacts=function() return SPCDistrictCompleteness.Clone(foundation) end};P.CityRoleFacts=function() return {owner=0,cityID=c.id,governorGateStatus='KNOWN',governorLevelCeiling=4} end;c.ledger={schema=1,revision=4,anchor={owner=0,cityID=c.id,token=c.token,first=foundation.first,specialization='RESEARCH'},investments={a='u1',b='u2',c='u3'}};SPCEffectiveFacts.Start(P,shared);f=SPCCurrentSpecializationFacts.Read(P,shared,0,c);assert(f.active==4 and f.potential==4 and f.workers==nil and writes==0)")
print('ADAPTER PASS actual unchanged EffectiveFacts + investment ledger + governor; read-only')
for n in [1,2,4,8]:
 a=runtime();a.globals().n=n
 a.execute("for i=1,n do local c=newCity(i);local d=addDistrict(c,20+i,'DISTRICT_CAMPUS');setBuildings(d,{'BUILDING_LIBRARY'});svc.Read(0,c,c.token) end;assert(counters.dc_capture==n and counters.district_scan==n and counters.building_check==n and writes==0)")
 print(f'SCALING {n} cities: captures={n} district reads={n} building checks={n}; network queries=0')
l=runtime();l.execute("for i=1,1000 do local c=newCity(i);addDistrict(c,1000+i,'DISTRICT_CAMPUS');svc.Read(0,c,c.token);assert(svc.CacheSize()<=8) end;assert(writes==0)")
print('BOUNDED PASS 1000 queried cities, cache <=8 (LRU, no history)')
# Ontology negative boundaries are explicit, not guessed from HD Tier alone.
a=runtime();a.execute("GameInfo.HD_BuildingTiers.BUILDING_LIBRARY.Tier=0;cc=SPCOrdinaryBuildingCatalog.Build(P);assert(cc.buildings.BUILDING_LIBRARY.ordinary and cc.buildings.BUILDING_LIBRARY.tier==0);GameInfo.HD_BuildingTiers.BUILDING_LIBRARY.Tier=9;cc=SPCOrdinaryBuildingCatalog.Build(P);assert(cc.buildings.BUILDING_LIBRARY.tier==nil and cc.buildings.BUILDING_LIBRARY.reason=='TIER_UNSUPPORTED')")
a=runtime();a.execute("GameInfo.HD_BuildingTiers.BUILDING_MADRASA.Tier=3;cc=SPCOrdinaryBuildingCatalog.Build(P);assert(cc.buildings.BUILDING_MADRASA.reason=='REPLACEMENT_TIER_CONFLICT')")
a=runtime();a.execute("GameInfo.Buildings.BUILDING_LIBRARY.InternalOnly=true;cc=SPCOrdinaryBuildingCatalog.Build(P);assert(not cc.buildings.BUILDING_LIBRARY.ordinary);assert(cc.buildings.BUILDING_PALACE.reason=='PALACE')")
a=runtime();a.execute("setBuildings(d,{'BUILDING_LIBRARY'});c.queued='BUILDING_UNIVERSITY';v=svc.Read(0,c,c.token);assert(v.value.excluded[1].reason=='UNDER_CONSTRUCTION' and v.value.domains.DISTRICT_CAMPUS.value==1);c.queued=nil;d.bs[1].obtainedFree=true;svc.MarkDirty();assert(svc.Read(0,c,c.token).value.domains.DISTRICT_CAMPUS.value==1)")
a.execute("d.workers=5;setBuildings(d,{'BUILDING_LIBRARY','BUILDING_UNIVERSITY','BUILDING_JNR_LABORATORY','BUILDING_RESEARCH_LAB'});svc.MarkDirty();v=svc.Read(0,c,c.token);f=SPCCurrentSpecializationFacts.Read(P,shared,0,c);p=SPCResearchInfrastructureShadow.Plan(SPCResearchInfrastructureShadow.WithWorkers(f,v),v);assert(p.science==50 and p.appliedScience==0);c.factsError=true;assert(SPCResearchInfrastructureShadow.Plan(SPCCurrentSpecializationFacts.Read(P,shared,0,c),v).status=='UNKNOWN')")
print('BOUNDARIES PASS tier0/invalid tier/replacement conflict/internal/Palace/free building/unfinished queue; D10 × workers5 = 50 shadow only')
# Execute actual Gameplay request function: selected-city read must not reach old Audits.
a=runtime();a.execute("P.Scalar=tostring;stage=bomb;setBuildings(d,{'BUILDING_LIBRARY'});shared.Version=P.VERSION")
g=(M/'Gameplay.lua').read_text();request_code=g[g.index('local function request('):g.index('GameEvents.SPC_P0_Request.Add')]
a.execute(request_code+'\nrunRequest=request')
a.execute("runRequest(0,{Action='COMPLETENESS_READ',Token='p0a-click',CityID=1});assert(shared.LastToken=='p0a-click' and shared.Snapshot:find('SHADOW_ONLY'));assert(writes==0);runRequest(0,{Action='COMPLETENESS_READ',Token='missing',CityID=999});assert(shared.LastToken=='missing' and shared.Snapshot:find('DC_SELECTED_CITY_UNAVAILABLE') and writes==0)")
# Actual diagnostics panel: a click sends once, idle/hover never sends.
source=(R/'DevelopmentTests/test_arch_v2_d2.py').read_text();tree=ast.parse(source)
ui_fix=next(ast.literal_eval(n.value) for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='UI_FIX' for t in n.targets))
u=LuaRuntime(unpack_returned_tuples=True);u.execute(ui_fix)
u.execute("P.Scalar=tostring;print=function() end;Controls.CompletenessButton.RegisterCallback=function(c,event,f) c.click=f end;UI.RequestPlayerOperation=function(pid,op,p) sends=sends+1;assert(p.Action=='COMPLETENESS_READ');shared.LastToken=p.Token;shared.Snapshot='SHADOW_ONLY';end")
u.execute((M/'UI/P0Panel.lua').read_text())
u.execute("init();assert(sends==0);for i=1,10000 do fire('SystemUpdateUI') end;assert(sends==0);Controls.CompletenessButton.click();assert(sends==1);for i=1,10000 do fire('SystemUpdateUI') end;assert(sends==1)")
print('INTEGRATION PASS actual request dispatch read-only; actual diagnostic button sends1; 10000 idle UI events sends0')

# Syntax, manifest and authority protection.
compiler=LuaRuntime(unpack_returned_tuples=True)
for p in M.rglob('*.lua'):
 compiler.globals().src=p.read_text();compiler.execute("assert(load(src))")
x=ET.parse(M/'SpecializationP0.modinfo').getroot();assert x.get('version')=='104'
for n in NEW:
 assert x.find("./Files/File[.='"+n+".lua']") is not None
 assert x.find("./InGameActions/ImportFiles/File[.='"+n+".lua']") is not None
for n in NEW:
 s=(M/(n+'.lua')).read_text()
 for bad in ['CreateBuilding(', 'RemoveBuilding(', 'SetProperty(', 'RequestPlayerOperation(', 'SetUpdate(', 'ChangeYield', 'AddProgress(']:assert bad not in s,(n,bad)
for p in ['EffectiveFacts.lua','CityFlowProbe.lua','NetworkBridge.lua','ResearchSupport.lua','Lv3Support.lua','Lv3Effects.lua','Lv4Percent.lua','CopyYields.lua','IndustrySupport.lua','Standardization.lua','StandardizationDiscount.lua','Dialogue.lua','GreatWorkAdjacency.lua','CommerceConvergence.lua','UnitActions.lua']:
 assert (M/p).read_bytes()==subprocess.check_output(['git','show','04a629e:Mod/'+p],cwd=R),p
for p in (M/'Data').glob('*'):
 assert p.read_bytes()==subprocess.check_output(['git','show','04a629e:Mod/Data/'+p.name],cwd=R),p
print('STATIC PASS all Lua syntax; manifest104; old effect writers and Data unchanged; new modules no write/send/timer primitives')
# Explicit historical stamp-only adaptation; do not alter frozen test files.
if __name__=='__main__' and '--regression' in __import__('sys').argv:
 s=(R/'DevelopmentTests/test_arch_v2_d2.py').read_text().replace("get('version')=='103'", "get('version')=='104'").replace('P0-B-076.103','P0-B-077.104')
 exec(compile(s,'D2_stamp104_only','exec'),{'__file__':str(R/'DevelopmentTests/test_arch_v2_d2.py')})
