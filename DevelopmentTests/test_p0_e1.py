"""P0-E1 actual read model/observer: never a native continuity proof."""
from pathlib import Path
import subprocess,xml.etree.ElementTree as ET
from lupa.lua55 import LuaRuntime
R=Path(__file__).resolve().parents[1];M=R/'Mod';l=LuaRuntime()
l.execute((M/'CityIdentityRead.lua').read_text())
l.execute("""
M=SPCCityIdentityRead
function fixture()
 local token='DEV-B013-P0-1'
 local j={schema=1,kind='DEV_FOUNDATION_JOURNAL',owner=0,cityID=7,x=4,y=5,token=token,foundationTurn=1,revision=1,health='TRACKING',specialization='RESEARCH',potential=1,first={districtID=3,type='DISTRICT_CAMPUS',turn=2}}
 return {ref={owner=0,cityID=7,x=4,y=5},values={TOKEN=token,JOURNAL=j,FLOW={schema=1,owner=0,cityID=7,x=4,y=5,token=token,revision=3,stage='DONE',facts=M.Copy(j),target=M.Copy(j)},INVEST={schema=1,anchor={owner=0,cityID=7,token=token,first=M.Copy(j.first),specialization='RESEARCH'},revision=2,investments={r1='crew1'}}},ledger={schema=1,owner=0,counter=1,records={['7']={owner=0,cityID=7,x=4,y=5,serial=1,uid=token,state='CONFIRMED'}}}}
end
function expect(s,state,reason) local r=M.Preview(s);assert(r.state==state,r.state..':'..tostring(r.reason));if reason then assert(r.reason==reason,r.reason)end;assert(r.migrationAllowed==false and r.cityKey==nil);return r end
s=fixture();expect(s,'LOCAL_CANDIDATE');assert(M.Compare(s,M.Copy(s))=='SAME_REFERENCE_CONTINUITY_UNPROVEN')
s.name='renamed';expect(s,'LOCAL_CANDIDATE')
t=M.Copy(s);t.ref.owner=1;t.ref.cityID=40;expect(t,'HELD','CROSS_OWNER');assert(M.Compare(s,t)=='TOKEN_RETAINED_CONTINUITY_UNPROVEN')
t.ref.owner=0;t.ref.cityID=7;expect(t,'LOCAL_CANDIDATE') -- regain only origin candidate, no native generation proof
assert(M.Compare(s,nil)=='LOCATION_EMPTY')
t=fixture();t.values.TOKEN='DEV-B013-P0-2';assert(M.Compare(s,t)=='DIFFERENT_TOKEN_DO_NOT_MERGE')
t=fixture();t.values.TOKEN=nil;expect(t,'UNKNOWN','NO_TOKEN');assert(M.Compare(s,t)=='UNKNOWN_TOKEN_MISSING')
t=fixture();t.ledger=nil;expect(t,'HELD','NO_LEDGER')
t=fixture();t.ledger.records['8']=M.Copy(t.ledger.records['7']);expect(t,'HELD','BAD_LEDGER')
t=fixture();t.ledger.records['7'].state='RESERVED';expect(t,'HELD','PARTIAL_BINDING')
t=fixture();t.ref.x=6;expect(t,'HELD','POSITION_CHANGED')
for _,key in ipairs({'JOURNAL','FLOW'})do t=fixture();t.values[key]=nil;expect(t,'HELD',key)end
for _,key in ipairs({'JOURNAL','FLOW','INVEST','TEMPLATES'})do t=fixture();t.values[key]=1;expect(t,'HELD',key)end
t=fixture();t.values.JOURNAL.health='GAP';expect(t,'HELD','JOURNAL')
t=fixture();t.values.FLOW.stage='TARGET_PENDING';expect(t,'HELD','FLOW')
t=fixture();t.values.INVEST.pending={stage='intent'};expect(t,'HELD','INVEST')
t=fixture();t.values.INVEST.investments.r2='crew1';expect(t,'HELD','INVEST')
t=fixture();t.values.INVEST=nil;expect(t,'LOCAL_CANDIDATE') -- absence not fabricated receipt/history
local token=s.values.TOKEN
t=fixture();t.values.TEMPLATES={schema=1,initialized=true,uid='STD:'..token,foundation=token,x=4,y=5,revision=2,learned={BUILDING_LIBRARY={district='DISTRICT_CAMPUS',tier=1,turn=3,evidence='BUILT'}}};assert(expect(t,'LOCAL_CANDIDATE').catalog=='NOT_VALIDATED')
t.values.TEMPLATES.foundation='other';expect(t,'HELD','TEMPLATES')
t=fixture();t.loop=t;expect(t,'HELD','READ_FAILED')
t=fixture();t.extra=string.rep('x',65537);expect(t,'HELD','READ_FAILED')
t=fixture();t.extra={};for i=1,9000 do t.extra[i]=i end;expect(t,'HELD','READ_FAILED')
assert(M.Compare(nil,s)=='NO_SESSION_BASELINE');expect(nil,'UNKNOWN','NO_CITY')
-- Instrument actual observer with fatal writes/scans: no fake no-op writer can mask a mutation.
props=0;gameReads=0;lookups=0
function forbidden()error('SIDE_EFFECT_OR_SCAN')end
function events()return setmetatable({}, {__index=function(t,k)local e={};function e.Add(f)e.fn=f end;rawset(t,k,e);return e end})end
Events=events();GameEvents=events();s=fixture()
Game={GetProperty=function(self,k)gameReads=gameReads+1;assert(k=='SPC_DEV_BINDING_B013_P0');return s.ledger end,SetProperty=forbidden,GetCurrentGameTurn=function()return 8 end}
city={GetOwner=function()return s.ref.owner end,GetID=function()return s.ref.cityID end,GetX=function()return s.ref.x end,GetY=function()return s.ref.y end,GetProperty=function(self,k)props=props+1;for name,key in pairs(M.Keys)do if key==k then return s.values[name]end end;error('unexpected property')end,SetProperty=forbidden,GetDistricts=forbidden,GetBuildings=forbidden}
CityManager={GetCityAt=function(x,y)lookups=lookups+1;assert(x==4 and y==5);return city end}
P={VERSION='B088.115',Field=function(t,k)return t[k]end,IsTestPlayer=function(pid)return pid==0 end,SetProperty=forbidden,Count=forbidden}
shared={};M.Start(P,shared);d=shared.CityIdentityRead
assert(props==0 and gameReads==0 and lookups==0)
assert(Events.UnitMoved.fn==nil and Events.PublishComplete.fn==nil and Events.PlaybackComplete.fn==nil)
for i=1,10000 do Events.CityTransfered.fn(1,7);GameEvents.CityBuilt.fn(0,7,4,5)end
assert(d.eventCount==0 and props==0 and gameReads==0)
assert(d.Describe(0,false):find('尚无'));d.Record(0,city)
local reads=d.reads;local pg=props;local gg=gameReads
for i=1,10000 do Events.CityTransfered.fn(1,7);Events.CityRemovedFromMap.fn(0,7);GameEvents.CityConquered.fn(0,1,7,4,5)end
assert(d.eventCount==32 and #d.events==32 and d.reads==reads and props==pg and gameReads==gg)
assert(d.Describe(0,true):find('CITY')==nil) -- readable report, no whole ledger dump
s.ref.owner=1;s.ref.cityID=40;assert(d.Describe(0,true):find('暂缓迁移'))
s.ref.owner=0;s.ref.cityID=7;assert(d.Describe(0,false):find('迁移候选'))
local text=d.Describe(0,true);assert(not text:find('crew1'))
s.extra=nil;s.values.JOURNAL.extra=string.rep('x',65537);assert(d.Describe(0,false):find('读取失败'));s.values.JOURNAL.extra=nil
Events.LoadScreenClose.fn();assert(d.eventCount==0 and d.Describe(0,false):find('尚无'))
-- New runtime session uses only persisted origin evidence; no resurrected watch.
shared={};M.Start(P,shared);assert(shared.CityIdentityRead.Describe(0,false):find('尚无'));shared.CityIdentityRead.Record(0,city)
assert(s.values.INVEST.revision==2 and s.values.FLOW.stage=='DONE' and s.ledger.counter==1)
""")
for p in M.rglob('*.lua'):l.execute('assert(load(...))',p.read_text())
x=ET.parse(M/'SpecializationP0.modinfo').getroot();assert x.get('version')=='115'
assert sorted(f.text for f in x.findall('./Files/File'))==sorted(str(p.relative_to(M)) for p in M.rglob('*') if p.is_file() and p.suffix!='.modinfo')
assert 'CityIdentityRead.lua' in [f.text for f in x.findall('./InGameActions/ImportFiles/File')]
ET.parse(M/'UI/P0Panel.xml')
allowed={'CityIdentityRead.lua','Gameplay.lua','Probe.lua','SpecializationP0.modinfo','UI/P0Panel.lua','UI/P0Panel.xml','UI/RuntimeAudit.lua'}
for p in M.rglob('*'):
 if p.is_file() and str(p.relative_to(M)) not in allowed:assert p.read_bytes()==subprocess.check_output(['git','show','223e8e8:Mod/'+str(p.relative_to(M))],cwd=R),p
src=(M/'CityIdentityRead.lua').read_text()
for bad in ['SetProperty','RequestPlayerOperation','SetUpdate','CreateBuilding','RemoveBuilding','Audit(','Members()','print(']:assert bad not in src,bad
for p in subprocess.check_output(['git','ls-files','Specialization/Design'],cwd=R,text=True).splitlines():assert (R/p).read_bytes()==subprocess.check_output(['git','show','223e8e8:'+p],cwd=R),p
print('P0-E1 LOCAL PASS: origin/transfer/regain/refound/ID reuse/partial/corrupt/bounds/coldload; 30k watched events fixed32 entries, zero extra property reads/scans/writes; no migration allowed; protected writers/Design identical; all Lua/XML/manifest115')

# Actual dispatcher and actual panel callbacks, including compare without selected owned city.
l.execute("P.Scalar=tostring;Players={[0]={GetCities=function()return {FindID=function(self,id)assert(id==7);return city end}end}}")
g=(M/'Gameplay.lua').read_text();l.execute(g[g.index('local function request('):g.index('GameEvents.SPC_P0_Request.Add')]+'\nrunRequest=request')
l.execute("runRequest(0,{Action='IDENTITY_RECORD',Token='a',CityID=7});assert(shared.LastToken=='a' and shared.Snapshot:find('迁移候选'));runRequest(0,{Action='IDENTITY_DETAIL',Token='b'});assert(shared.LastToken=='b' and shared.Snapshot:find('绑定凭据'));runRequest(1,{Action='IDENTITY_RECORD',Token='bad',CityID=7});assert(shared.LastToken=='b')")
import ast
t=ast.parse((R/'DevelopmentTests/test_arch_v2_d2.py').read_text());fix=next(ast.literal_eval(x.value) for x in t.body if isinstance(x,ast.Assign) and any(isinstance(k,ast.Name) and k.id=='UI_FIX' for k in x.targets))
u=LuaRuntime();u.execute(fix)
u.execute("Mouse.eRClick=2;P.Scalar=tostring;print=function() end;record={};compare={};Controls.InheritRecordButton.RegisterCallback=function(c,e,f)record[e]=f end;Controls.InheritReadButton.RegisterCallback=function(c,e,f)compare[e]=f end;UI.RequestPlayerOperation=function(pid,op,p)sends=sends+1;lastAction=p.Action;shared.LastToken=p.Token;shared.Snapshot='城市身份';end")
u.execute((M/'UI/P0Panel.lua').read_text())
u.execute("init();record[1]();assert(sends==1 and lastAction=='IDENTITY_RECORD');UI.GetHeadSelectedCity=function()return nil end;compare[1]();assert(sends==2 and lastAction=='IDENTITY_COMPARE');compare[2]();assert(sends==3 and lastAction=='IDENTITY_DETAIL');for i=1,10000 do fire('SystemUpdateUI')end;assert(sends==3)")
print('E1 actual dispatch and panel PASS: owned record / unselected compare+detail / 10k UI idle zero sends')
