"""Risk-scoped E1 opt-in persistence probe; no native identity PASS implied."""
from pathlib import Path
import ast, subprocess, xml.etree.ElementTree as ET
from lupa.lua55 import LuaRuntime
R=Path(__file__).resolve().parents[1]; M=R/'Mod'; l=LuaRuntime()
l.execute((M/'CityIdentityRead.lua').read_text())
old=(R/'DevelopmentTests/test_p0_e1.py').read_text()
l.execute("M=SPCCityIdentityRead\n"+old[old.index('function fixture()'):old.index('function expect(')])
l.execute((M/'CityIdentityExperiment.lua').read_text())
l.execute(r"""
function events()return setmetatable({}, {__index=function(t,k)local e={};function e.Add(f)e.fn=f end;rawset(t,k,e);return e end})end
local key=SPCCityIdentityExperiment.KEY
store={};writes=0;turn=8
function setup()
 Events=events();GameEvents=events();s=fixture();exists=true;nativeOwner=0;badwrite=false
 city={GetOwner=function()return s.ref.owner end,GetID=function()return s.ref.cityID end,GetX=function()return s.ref.x end,GetY=function()return s.ref.y end,
 GetProperty=function(self,k)for name,v in pairs(M.Keys)do if k==v then return s.values[name]end end;error('unknown property')end,
 SetProperty=function()error('OLD_CITY_WRITE')end,GetOwnerBeforeOccupation=function()return nativeOwner end}
 Game={GetProperty=function(self,k)if k==key then return M.Copy(store[k])end;assert(k=='SPC_DEV_BINDING_B013_P0');return s.ledger end,
 SetProperty=function(self,k,v)assert(k==key,'OLD_GAME_WRITE');writes=writes+1;if not badwrite then store[k]=M.Copy(v)end end,GetCurrentGameTurn=function()return turn end}
 CityManager={GetCityAt=function(x,y)assert(x==4 and y==5);return exists and city or nil end}
 P={VERSION='P0-B-092.119',Field=function(t,k)return t[k]end,IsTestPlayer=function(pid)return pid==0 end}
 shared={};SPCCityIdentityExperiment.Start(P,shared);d=shared.CityIdentityExperiment
end
setup();assert(writes==0);Events.CityRemovedFromMap.fn(0,7);assert(writes==0)
Events.LoadScreenClose.fn();assert(writes==0)
assert(d.Begin(0,city):find('已建立'));assert(writes==1)
assert(d.Begin(0,city):find('不覆盖'));d.Describe(0);assert(writes==1)
assert(Events.PublishComplete.fn==nil and Events.UnitMoved.fn==nil and Events.PlaybackComplete.fn==nil)
s.ref.owner=62;s.ref.cityID=40;s.values={}
GameEvents.CityBuilt.fn(62,40,4,5);Events.CityRemovedFromMap.fn(0,7);Events.CityAddedToMap.fn(62,40,4,5);Events.CityInitialized.fn(62,40,4,5);Events.CityTransfered.fn(62,40,0,-738490196)
for i=1,128 do Events.CityTransfered.fn(62,40,0,-738490196)end
assert(writes==1) -- callbacks never persist, duplicate observations bounded
assert(d.Describe(0):find('实验候选'));assert(writes==2 and store[key].state=='MAPPING_CANDIDATE' and #store[key].events==5)
d.Describe(0);assert(writes==2)
-- Cold load preserves only saved experiment evidence; never replays events as authority.
setup();s.ref.owner=62;s.ref.cityID=40;s.values={};Events.LoadScreenClose.fn()
local text=d.Describe(0);assert(text:find('本次加载事件 0') and text:find('保存时引用与当前：一致'));assert(writes==2)
assert(d.Begin(0,city):find('不属于你'));assert(writes==2) -- no replacement by non-owned city
-- Unknown native getter never fabricated. Missing/late transfer cannot identify a city.
store={};setup();Events.LoadScreenClose.fn();d.Begin(0,city);s.ref.owner=62;s.ref.cityID=40;city.GetOwnerBeforeOccupation=nil
Events.CityRemovedFromMap.fn(0,7);Events.CityTransfered.fn(62,40);d.Describe(0);assert(store[key].state=='HELD')
city.GetOwnerBeforeOccupation=function()return 0 end;turn=9;d.Describe(0);assert(store[key].state=='HELD')
-- Full buffer remains bounded and prevents new mapping candidates.
for i=1,40 do turn=turn+1;Events.CityRemovedFromMap.fn(0,7)end
Events.CityTransfered.fn(62,40);local before=writes
assert(d.Describe(0):find('缓冲已满'));assert(#store[key].events==16 and store[key].overflow and store[key].state=='HELD');assert(writes==before+1)
-- Malformed saved record / concurrent changes / failed write stop, never repair old state.
store[key].origin={};setup();Events.LoadScreenClose.fn();before=writes;d.Begin(0,city);assert(writes==before)
store={};setup();Events.LoadScreenClose.fn();badwrite=true;before=writes;d.Begin(0,city);d.Begin(0,city);assert(writes==before+1)
store={};setup();Events.LoadScreenClose.fn();d.Begin(0,city);store[key].revision=99;Events.CityRemovedFromMap.fn(0,7);before=writes;d.Describe(0);assert(writes==before and store[key].revision==99)
store={};setup();Events.LoadScreenClose.fn();s.values.TOKEN=nil;before=writes;d.Begin(0,city);assert(writes==before)
-- Missing/late load callback, recoverable selection and unavailable Game access.
store={};setup();before=writes
assert(d.Begin(0,nil):find('未取得'));assert(d.error==nil)
assert(d.Begin(1,city):find('测试范围'));assert(d.error==nil)
local get=Game.GetProperty;Game.GetProperty=function()error('temporarily unavailable')end
assert(d.Begin(0,city):find('暂不可读'));assert(d.error==nil and writes==before)
Game.GetProperty=get
assert(d.Begin(0,city):find('已建立'));assert(writes==before+1)
Events.CityRemovedFromMap.fn(0,7);Events.LoadScreenClose.fn();Events.LoadScreenClose.fn()
assert(d.Describe(0):find('本次加载事件 1')) -- late event doesn't discard evidence
setup();before=writes;assert(d.Describe(0):find('Game记录已读取'));assert(writes==before) -- cold load, no load event
store={};setup();badwrite=true;before=writes
assert(d.Begin(0,city):find('暂停'));Events.LoadScreenClose.fn();d.Begin(0,city);assert(writes==before+1 and d.error)
assert(not d.Describe(0):find('stack traceback'))
store={};setup();s.values.TOKEN=nil;d.Begin(0,city);assert(d.error==nil);s=fixture();assert(d.Begin(0,city):find('已建立'))
-- Actual dispatcher, authorized player only.
store={};setup();Events.LoadScreenClose.fn()
P.Scalar=tostring;Players={[0]={GetCities=function()return {FindID=function(self,id)assert(id==7);return city end}end}}
""")
g=(M/'Gameplay.lua').read_text();l.execute(g[g.index('local function request('):g.index('GameEvents.SPC_P0_Request.Add')]+'\nrunRequest=request')
l.execute("runRequest(0,{Action='IDENTITY_EXPERIMENT_BEGIN',Token='a',CityID=7});assert(shared.Snapshot:find('已建立'));runRequest(0,{Action='IDENTITY_EXPERIMENT_READ',Token='b'});assert(shared.LastToken=='b');runRequest(1,{Action='IDENTITY_EXPERIMENT_READ',Token='x'});assert(shared.LastToken=='b')")
# Actual UI bindings, no selection required for read; idle callbacks send nothing.
t=ast.parse((R/'DevelopmentTests/test_arch_v2_d2.py').read_text());fix=next(ast.literal_eval(x.value) for x in t.body if isinstance(x,ast.Assign) and any(isinstance(k,ast.Name) and k.id=='UI_FIX' for k in x.targets))
u=LuaRuntime();u.execute(fix)
u.execute("Mouse.eRClick=2;P.Scalar=tostring;print=function()end;record={};compare={};Controls.InheritRecordButton.RegisterCallback=function(c,e,f)record[e]=f end;Controls.InheritReadButton.RegisterCallback=function(c,e,f)compare[e]=f end;UI.RequestPlayerOperation=function(pid,op,p)sends=sends+1;lastAction=p.Action;shared.LastToken=p.Token;shared.Snapshot='ok';end")
u.execute((M/'UI/CityIdentityEvidence.lua').read_text())
u.execute((M/'UI/P0Panel.lua').read_text())
u.execute("init();record[2]();assert(sends==1 and lastAction=='IDENTITY_EXPERIMENT_BEGIN');UI.GetHeadSelectedCity=function()return nil end;compare[1]();assert(sends==2 and lastAction=='IDENTITY_EXPERIMENT_READ');for i=1,128 do fire('SystemUpdateUI')end;assert(sends==2)")
for p in M.rglob('*.lua'):l.execute('assert(load(...))',p.read_text())
x=ET.parse(M/'SpecializationP0.modinfo').getroot();assert x.get('version')=='119'
assert sorted(f.text for f in x.findall('./Files/File'))==sorted(str(p.relative_to(M)) for p in M.rglob('*') if p.is_file() and p.suffix!='.modinfo')
assert 'CityIdentityExperiment.lua' in [f.text for f in x.findall('./InGameActions/ImportFiles/File')]
ET.parse(M/'UI/P0Panel.xml');assert 'P0-B-092.119' in (M/'Probe.lua').read_text()
allowed={'Mod/'+p for p in ['CityIdentityExperiment.lua','Probe.lua','SpecializationP0.modinfo','UI/RuntimeAudit.lua']}
for p in subprocess.check_output(['git','ls-files','Mod','Specialization/Design'],cwd=R,text=True).splitlines():
 if p not in allowed:assert (R/p).read_bytes()==subprocess.check_output(['git','show','45900c9:'+p],cwd=R),p
assert 'shared.InheritanceIsolation=true' in g
print('E1 experiment LOCAL_SIMULATION_PASS: opt-in/new-key-only; event zero writes; dedupe/bounds; transfer HELD/candidate; reload; failure/concurrent/corrupt guards; actual dispatcher/UI; idle zero requests; old writers/Design unchanged; Lua/XML/manifest119.')

# Actual UI evidence: absent/error/nil/numeric values, fixed bound, no writes or requests.
v=LuaRuntime();v.execute((M/'UI/CityIdentityEvidence.lua').read_text())
v.execute(r"""
Events=setmetatable({}, {__index=function(t,k)local e={};function e.Add(f)e.fn=f end;rawset(t,k,e);return e end})
P={VERSION='B092.119',Field=function(t,k)return t[k]end,IsTestPlayer=function(p)return p==0 end}
local row={schema=1,requester=0,token='one',origin={owner=0,cityID=7,x=4,y=5}}
Game={GetProperty=function()return row end,GetCurrentGameTurn=function()return 8 end,SetProperty=function()error('WRITE')end}
local c={GetOwner=function()return 62 end,GetID=function()return 40 end,GetOriginalOwner=function()return 0 end,GetJustConqueredFrom=function()error('unavailable')end,GetLastTransferType=function()return nil end}
CityManager={GetCityAt=function()return c end};UI={RequestPlayerOperation=function()error('REQUEST')end}
local d=SPCCityIdentityEvidence.New(P)
local t=d.Read(0);assert(t:find('GetOriginalOwner: 0') and t:find('ABSENT') and t:find('CALL_ERROR') and t:find('nil'))
for i=1,20 do Events.CityTransfered.fn(62,40,i)end
assert(d.Read(0):find('观察事件：8'))
assert(Events.SystemUpdateUI.fn==nil)
local cold=SPCCityIdentityEvidence.New(P);assert(cold.Read(0):find('观察事件：0'))
Events.CulturalIdentityCityConverted.fn(62,40,0);assert(cold.Read(0):find('CulturalIdentityCityConverted'))
assert(not cold.Read(1):find('GetOriginalOwner'))
""")
u.execute("local before=sends;compare[2]();assert(sends==before)")
print('UI evidence PASS: actual right-click zero requests; numeric/nil/absent/error distinguished; bound8; fresh-context reset; no writer.')

l.execute(r"""
local o={owner=0,cityID=7,x=4,y=5};local n={owner=62,cityID=40,x=4,y=5}
local function e(name,args)return {name=name,args=args,turn=8}end
local events={e('CityBuilt',{62,40,4,5}),e('CityRemovedFromMap',{0,7}),e('CityAddedToMap',{62,40,4,5}),e('CulturalIdentityCityConverted',{62,40,0,24576}),e('CityTransfered',{62,40,0,-738490196})}
local S=SPCCityIdentityExperiment.Shadow
assert(S(o,n,events,false,8)=='SHADOW_CANDIDATE')
local duplicate=M.Copy(events);duplicate[#duplicate+1]=M.Copy(events[4]);assert(S(o,n,duplicate,false,8)=='SHADOW_CANDIDATE')
local reverse={};for i=#events,1,-1 do reverse[#reverse+1]=events[i]end;assert(S(o,n,reverse,false,8)=='SHADOW_CANDIDATE')
assert(S(o,n,events,true,8)=='HELD');assert(S(o,n,events,false,9)=='HELD');assert(S(o,n,{},false,8)=='HELD')
local bad=M.Copy(events);bad[4].args[3]=1;assert(S(o,n,bad,false,8)=='HELD')
bad=M.Copy(events);table.remove(bad,2);assert(S(o,n,bad,false,8)=='HELD')
bad=M.Copy(events);table.remove(bad,4);assert(S(o,n,bad,false,8)=='HELD') -- raze/refound-like add/remove alone
bad=M.Copy(events);bad[#bad+1]=e('CityRemovedFromMap',{62,40});assert(S(o,n,bad,false,8)=='HELD')
bad=M.Copy(events);bad[#bad+1]=e('CityAddedToMap',{1,99,4,5});assert(S(o,n,bad,false,8)=='HELD')
bad=M.Copy(events);bad[4]=e('CityConquered',{62,0,40,4,5});assert(S(o,n,bad,false,8)=='SHADOW_CANDIDATE')
assert(S(o,o,events,false,8)=='HELD')
-- Actual collector retains removal of newly added city, blocking A→B→C/refound preview.
store={};setup();d.Begin(0,city);s.ref.owner=62;s.ref.cityID=40
Events.CityRemovedFromMap.fn(0,7);Events.CityAddedToMap.fn(62,40,4,5);Events.CulturalIdentityCityConverted.fn(62,40,0,24576)
assert(d.Describe(0):find('SHADOW_CANDIDATE'))
Events.CityRemovedFromMap.fn(62,40);assert(d.Describe(0):find('发现额外移除'))
""")
print('Shadow PASS: typed-event candidate; duplicates/order; stale/overflow/conflict/refound/multihop held; actual collector; no migration.')
