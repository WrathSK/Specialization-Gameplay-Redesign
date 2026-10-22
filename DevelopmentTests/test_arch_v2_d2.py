"""D2 actual Lua scheduling / batch work. No game launch or deployment."""
from pathlib import Path
import subprocess,xml.etree.ElementTree as ET
from lupa.lua55 import LuaRuntime
R=Path(__file__).resolve().parents[1];M=R/'Mod'
s=(R/'DevelopmentTests/test_arch_v2_c2.py').read_text()
prefix=s[:s.index("for k in ['copy','industry']:")]
prefix=prefix.replace("name=='SampleLifecycle'", "name in ('SampleLifecycle','RuntimeWork')")
exec(compile(prefix,'C2_fixture','exec'))
for k in ['copy','industry']:
 l=runtime(k);l.execute('sync=true;initUI();pulse();pulse()')
 l.execute("before=clone(ExposedMembers.SPC_Performance.entries);w=writes;sent=sends;pulse(10000);assert(sends==sent and writes==w)")
 for n in ['district_scan','city_scan','building_check',k+'_apply']:
  assert l.eval(f'total("{n}")')==l.eval(f'before["{n}"].total'),(k,n)
 print(k,'PASS 10000 idle: native scans/send/write=0')
 l.execute("districts[12].prod=13;districts[12].base=8;fire('ResourceAddedToMap');pulse();assert(sends==sent+1)")
 l.execute("local old=sends;districts[12].prod=19;districts[12].base=11;turn=turn+1;pulse();assert(sends==old+1)")
 print(k,'PASS direct dirty and missed-event next-turn sample recovery')
# Actual module carrier-map differential oracle at the accepted B075 commit.
# Native API yields/facts are deterministic fixtures, not claims about Civ VI.
def module_runtime(mod,n,old=False):
 l=LuaRuntime(unpack_returned_tuples=True)
 l.globals().include=lambda name:l.execute((M/(name+'.lua')).read_text())
 l.execute(FIX);l.execute((M/'PerformanceCounters.lua').read_text())
 l.execute('ExposedMembers.SPC_Performance=SPCPerformance.New();P.Count=SPCPerformance.Count')
 l.globals().size=n
 l.execute(r'''
 cities={};facts={};districts={};queries=0;reads=0;audits=0
 local kinds={'RESEARCH','INDUSTRY','CULTURE','COMMERCE'}
 local types={RESEARCH='DISTRICT_CAMPUS',INDUSTRY='DISTRICT_INDUSTRIAL_ZONE',CULTURE='DISTRICT_THEATER',COMMERCE='DISTRICT_COMMERCIAL_HUB'}
 function setup(kind,level,workers)
  for id=1,size do
   local c=cities[id] or {id=id,owner=0,pop=3,token='C'..id,built={}};cities[id]=c
   c.GetID=function() return c.id end;c.GetOwner=function() return c.owner end;c.GetPopulation=function() return c.pop end
   c.GetX=function() return id end;c.GetY=function() return 1 end;c.GetProperty=function() return c.token end
   c.GetBuildings=function() return c.built end;c.GetBuildQueue=function() return c.built end
   c.GetYield=function(_,y) reads=reads+1;return 20+id*2 end
   facts[id]={specialization=kind,active=level,potential=4,first={districtID=id+10,type=types[kind]}}
   local d=district(id+10,id,types[kind],6);d.workers=workers
  end
 end
 setup('INDUSTRY',4,2)
 Players[0].GetCities=function() return {Members=function() return pairs(cities) end,FindID=function(_,id) return cities[id] end,GetCapitalCity=function() return cities[1] end} end
 shared.EffectiveFacts.Read=function(pid,c) P.Count('facts');return facts[c.id] end
 Map.GetPlot=function(x,y) return {GetWorkerCount=function() return districts[x].workers end,GetAdjacencyYield=function() return districts[x].base end} end
 shared.IndustrySupport={ReadBase=function() return 6 end}
 shared.NetworkBridge={ready=true,players={[0]={validity='VERIFIED',reason='READY_BACKGROUND_UI',routes={}}},Verified=function() return true end}
 function shared.NetworkBridge.ConnectedKinds() queries=queries+1;return {RESEARCH=true,CULTURE=true,INDUSTRY=true} end
 function shared.NetworkBridge.National() queries=queries+1;return {RESEARCH={n=2,level=4,sources={}},CULTURE={n=1,level=3,sources={}}} end
 function shared.NetworkBridge.RecipientSources(pid,c) queries=queries+1;return {1} end
 local info=P.Info;local ids={}
 local has,create,remove=P.HasBuilding,P.CreateBuilding,P.RemoveBuilding
 P.HasBuilding=function(b,i) return has(b,ids[i] or i) end
 P.CreateBuilding=function(b,i) return create(b,ids[i] or i) end
 P.RemoveBuilding=function(b,i) return remove(b,ids[i] or i) end
 P.Info=function(t,k)
  local r=info(t,k)
  if t=='Buildings' then
   local kind=k:match('GPP_(%u+)_');r.Housing=0;r.CitizenSlots=0;r.PrereqDistrict=types[kind];r.Index=k
   if kind then r.Index=1000+(({RESEARCH=1,CULTURE=2,INDUSTRY=3,COMMERCE=4})[kind])*8+tonumber(k:match("(%d+)$"));ids[r.Index]=k end
  end
  return r
 end
 P.Rows=function() local rows={};for k in pairs(types) do for bit=0,7 do
  local cls=k=='CULTURE' and {'WRITER','ARTIST','MUSICIAN'} or {({RESEARCH='SCIENTIST',INDUSTRY='ENGINEER',COMMERCE='MERCHANT'})[k]}
  for _,cl in ipairs(cls) do rows[#rows+1]={BuildingType='BUILDING_SPC_DEV_GPP_'..k..'_'..bit,GreatPersonClassType='GREAT_PERSON_CLASS_'..cl,PointsPerTurn=2*2^bit} end
 end end;return rows end
 function output() local t={};for id,c in pairs(cities) do t[id]=c.built end;return encode(t) end
 ''')
 source=subprocess.check_output(['git','show','5dc6221:Mod/'+mod+'.lua'],cwd=R,text=True) if old else (M/(mod+'.lua')).read_text()
 l.execute(source);l.execute(f'SPC{mod}.Start(P,shared);d=shared.{mod};d.ready=true')
 if mod in ('CopyYields','IndustrySupport'):
  l.execute("function samples() local rows={};for key,r in pairs(SPCSampleLifecycle.Live(P,0,false)) do rows[key]={cityID=r.cityID,id=r.id,type=r.type,reference=r.reference,total=6,production=6,value=6} end;d.samples[0]={turn=turn,rows=rows,signature='fixture'} end;samples()")
 return l
for mod in ['Lv3Effects','Lv3Support','Lv4Percent','Lv2GPP','CrewProjects','CopyYields','IndustrySupport','NetworkBoost','CommerceConvergence']:
 comparisons=0
 for n in [1,2,4,8]:
  a,b=module_runtime(mod,n,True),module_runtime(mod,n)
  for kind in ['RESEARCH','CULTURE','INDUSTRY','COMMERCE']:
   for active in [1,2,3,4]:
    for workers in [0,1,3]:
     for l in [a,b]:l.execute(f"setup('{kind}',{active},{workers});if samples then samples() end;d.Audit()")
     assert a.eval('output()')==b.eval('output()'),(mod,n,kind,active,workers)

     for l in [a,b]:
      l.execute("for _,err in pairs(d.errors or {}) do assert(err==nil,err) end")
     comparisons+=1
  # settled idle: actual event handlers, no artificial direct change.
  b.execute('local w=writes;local q=queries;local f=total("facts");local ds=total("district_scan");pulse(10000);fire("UnitOperationStarted");assert(writes==w and queries==q and total("facts")==f and total("district_scan")==ds)')
 print(mod,'PASS B075 carrier maps',comparisons,'and 4 x 10000 idle')
print('D2 scaling: module / cities / old facts,districts,queries / new facts,districts,queries')
for mod in ['CopyYields','IndustrySupport','Lv3Effects','Lv3Support','Lv4Percent','Lv2GPP','CrewProjects']:
 for n in [1,2,4,8]:
  counts=[]
  for old in [True,False]:
   l=module_runtime(mod,n,old)
   k='RESEARCH' if mod in ['CopyYields','Lv3Effects','Lv4Percent','Lv2GPP'] else 'INDUSTRY'
   l.execute(f"setup('{k}',4,2);if samples then samples() end;ExposedMembers.SPC_Performance=SPCPerformance.New();queries=0;d.Audit()")
   counts.append([l.eval('total("facts")'),l.eval('total("district_scan")'),l.eval('queries')])
  print(mod,n,*counts)
  assert counts[1][0]<=2*n and counts[1][1]<=n,(mod,n,counts)
# Native player/city/worker direct event dispatch and fallback scope.
l=module_runtime('Lv3Effects',4)
l.execute("setup('RESEARCH',3,1);fire('CityWorkerChanged');assert(cities[1].built.BUILDING_SPC_DEV_LV3_POP_RESEARCH_0);setup('RESEARCH',3,2);turn=2;fire('PlayerTurnActivated');assert(cities[1].built.BUILDING_SPC_DEV_LV3_POP_RESEARCH_1);local n=total('city_scan');fire('PlayerTurnActivated');assert(total('city_scan')==n)")
print('PASS direct worker refresh; missed worker event repaired once/player/turn')

# Commerce nonzero external sources: yield changes independent from topology.
a,b=module_runtime('CommerceConvergence',8,True),module_runtime('CommerceConvergence',8)
for l in [a,b]:
 l.execute("setup('COMMERCE',4,0);facts[1].specialization='RESEARCH';facts[2].specialization='CULTURE';facts[3].specialization='INDUSTRY';local routes=shared.NetworkBridge.players[0].routes;for dest=4,8 do for src=1,3 do routes[#routes+1]={op=0,oc=src,dp=0,dc=dest} end end;d.Audit();assert(d.last['0:4'].amount.SCIENCE==4 and d.last['0:4'].amount.CULTURE==4 and d.last['0:4'].amount.PRODUCTION==5)")
for value in [0,19.5,50,100.75]:
 for l in [a,b]:l.execute(f"cities[1].GetYield=function() return {value} end;fire('CityWorkerChanged')")
 assert a.eval('output()')==b.eval('output()')
 assert b.eval("d.last['0:4'].amount.SCIENCE")==int(value*.2)
print('PASS Commerce nonzero 3-source/5-recipient yield-only changes; no Network-version cache')
# Actual current Network read-only query: full fact reads stop at the owner boundary.
p=(R/'DevelopmentTests/test_arch_v2_batch_a.py').read_text()
import ast
node=next(x for x in ast.parse(p).body if isinstance(x,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='FIXTURE' for t in x.targets))
l=LuaRuntime(unpack_returned_tuples=True);l.globals().include=lambda name:l.execute((M/(name+'.lua')).read_text());l.execute(ast.literal_eval(node.value))
l.execute((M/'PerformanceCounters.lua').read_text());l.execute('ExposedMembers.SPC_Performance=SPCPerformance.New();P.Count=SPCPerformance.Count')
l.execute((M/'NetworkBridge.lua').read_text())
l.execute("SPCNetworkBridge.Start(P,shared);net=shared.NetworkBridge;net.ready=true")
# Existing fixture setup helper for accepted packet.
l.execute("""
send('0,1,0,2,10;0,5,0,2,11;0,2,0,3,12',3)
local native=shared.EffectiveFacts.Read;captures=0
shared.EffectiveFacts.Read=function(...) captures=captures+1;return native(...) end
local v=net.Input(0).inputVersion
for i=1,10000 do net.CurrentNational(0);net.CurrentConnectedKinds(0,cities[2]);net.CurrentRecipientSources(0,cities[3],'INDUSTRY') end
assert(captures==0 and net.Input(0).inputVersion==v)
cities[1].active=4;Events.GovernorPromoted.Fire(0);assert(net.Input(0).inputVersion==v+1 and captures==5)
assert(net.CurrentNational(0).RESEARCH.level==4)
local old=net.Input(0).inputVersion;readFail=true;net.Rebuild();assert(net.Input(0).inputVersion==old and net.CurrentNational(0).RESEARCH.level==4)
readFail=false;send('',0);assert(net.CurrentNational(0).CULTURE.n==0)
local refresh=net.Refresh;local calls=0
net.Refresh=function(...) calls=calls+1;return refresh(...) end
confirmedOnly=true;net.Read(0,cities[2]);confirmedOnly=nil
assert(calls>=1,'manual diagnostic must refresh independently of unrelated globals')
""")
print('PASS 30000 shared queries: fact capture0; direct ACTIVE changes publish once; UNKNOWN holds')
# Reuse the original executable Great Work native mock scenario blocks only.
# Exclude obsolete UI scheduler assumptions and SQL/version harness, not carrier assertions.
for filename,cutoff in [('test_b059_dialogue.py','-- Background executes'),('test_b060_gw_adjacency.py',None)]:
 tree=ast.parse((R/'DevelopmentTests'/filename).read_text());l=LuaRuntime(unpack_returned_tuples=True)
 started=False
 for node in tree.body:
  if not isinstance(node,ast.Expr) or not isinstance(node.value,ast.Call):continue
  call=node.value
  if not isinstance(call.func,ast.Attribute) or not isinstance(call.func.value,ast.Name) or call.func.value.id!='l' or call.func.attr!='execute':continue
  arg=call.args[0]
  if isinstance(arg,ast.Constant):
   text=arg.value
   if not started:
    started=True
    l.execute(text)
    l.execute("P.Count=function() end;P.HasBuilding=function(b,id) return b:HasBuilding(id) end;P.CreateBuilding=function(b,id) return b:CreateBuilding(id) end;P.RemoveBuilding=function(b,id) return b:RemoveBuilding(id) end")
    continue
   if cutoff and cutoff in text:text=text.split(cutoff)[0];l.execute(text);break
   l.execute(text)
   if filename=='test_b060_gw_adjacency.py':break
  else:
   text=ast.unparse(arg)
   if 'read_text' in text:l.execute(eval(compile(ast.Expression(arg),'fixture','eval'),{'M':M}))
 print(filename,'PASS actual Great Work carrier/era/creation/move/base cases')
# Lightweight UI emulator: no game process, actual request/renderer code.
UI_FIX=r'''
include=function() end;turn=1;ExposedMembers={SPC_RuntimeUIRevision=0,SPC_P0={Version='D2'}};shared=ExposedMembers.SPC_P0
sends=0;sets=0;hooks={};selected=true
local methods={};function control() return setmetatable({hidden=false},{__index=methods}) end
methods.IsHidden=function(c) return c.hidden end;methods.SetHide=function(c,v) c.hidden=v;sets=sets+1 end
methods.GetSizeX=function() return 300 end
setmetatable(methods,{__index=function(t,k) local f=function() sets=sets+1 end;rawset(t,k,f);return f end})
Controls=setmetatable({},{__index=function(t,k) local c=control();rawset(t,k,c);return c end})
Events=setmetatable({},{__index=function(t,k) local e={Add=function(f) hooks[k]=hooks[k] or {};table.insert(hooks[k],f) end,Remove=function() end};rawset(t,k,e);return e end})
LuaEvents=Events
function fire(k) for _,f in ipairs(hooks[k] or {}) do f(0) end end
ContextPtr={SetInitHandler=function(_,f) init=f end,SetUpdate=function(_,f) tick=f end,SetShutdown=function(_,f) close=f end,ClearUpdate=function() end,SetHide=function() end,LookUpControl=function() return control() end}
Game={GetLocalPlayer=function() return 0 end,GetCurrentGameTurn=function() return turn end}
P={VERSION='D2',IsTestPlayer=function(p) return p==0 end,Field=function(t,k) return t[k] end,CrewBase=function() return 250 end};SPCP0=P
u={GetID=function() return 1 end,GetOwner=function() return 0 end,GetX=function() return 1 end,GetY=function() return 1 end,GetType=function() return 1 end}
c={GetID=function() return 1 end,GetOwner=function() return 0 end}
GameInfo={Units={[1]={UnitType='UNIT_CREW'}}};Locale={Lookup=function(t) return t end}
InterfaceModeTypes={SELECTION=1};PlayerOperations={EXECUTE_SCRIPT=1};Mouse={eLClick=1}
PlayersVisibility={[0]={IsVisible=function() return true end}}
UILens={CreateLensLayerHash=function() return 1 end,ClearLayerHexes=function() sets=sets+1 end,ToggleLayerOff=function() end,ToggleLayerOn=function() end,SetLayerHexesColoredArea=function() sets=sets+1 end}
UI={GetHeadSelectedUnit=function() return selected and u end,GetHeadSelectedCity=function() return selected and c end,GetInterfaceMode=function() return 1 end,IsGameCoreBusy=function() return false end,GetColorValue=function() return 1 end}
UI.RequestPlayerOperation=function(pid,op,p)
 sends=sends+1
 if p.Action=='CITY_PRESENTATION_READ' then shared.CityPresentationView={token=p.Token,owner=0,cityID=1,specialization='RESEARCH',potential=3,investments=2}
 elseif p.Action=='UNIT_ACTION_VIEW' then shared.UnitActionView={token=p.Token,owner=0,unitID=1,turn=turn,x=1,y=1,legal=true,prepared=false,amount=250}
 elseif p.Action=='UNIT_TARGETS_READ' then shared.UnitTargetSnapshot={version='D2',token=p.Token,owner=0,unitID=1,mode='CREW',plots={{plot=1}},unknown={}} end
end
'''
for ui in ['CityPotential','UnitPanelActions','UnitTargetMarkers']:
 l=LuaRuntime(unpack_returned_tuples=True);l.execute(UI_FIX);l.execute((M/'UI'/f'{ui}.lua').read_text());l.execute('init();for i=1,5 do tick(1) end;local n=sends;for i=1,10000 do tick(1) end;assert(sends==n);assert(n==1)')
 l.execute('turn=turn+1;for i=1,5 do tick(1) end;assert(sends==2);ExposedMembers.SPC_RuntimeUIRevision=1;for i=1,5 do tick(1) end;assert(sends==3)')
 print(ui,'PASS idle 10000 ticks requests0; turn/write revision each one request')

# Init/notification failure budgets and hidden diagnostics remain bounded.
for ui,module in [('BoostRefresh','NetworkBoost'),('GPPRefresh','Lv2GPP')]:
 l=LuaRuntime(unpack_returned_tuples=True);l.execute(UI_FIX)
 l.execute(f"shared.{module}={{ready={'false' if ui=='BoostRefresh' else 'true'}}};UI.RequestPlayerOperation=function() sends=sends+1;error('intentional transport failure') end;print=function() end")
 l.execute((M/'UI'/f'{ui}.lua').read_text());l.execute("init();for i=1,10000 do fire('SystemUpdateUI') end;assert(sends==3)")
 print(ui,'PASS failure 10000 generic pulses / max3 sends')
l=LuaRuntime(unpack_returned_tuples=True);l.execute(UI_FIX);l.execute((M/'UI/UnitSites.lua').read_text())
l.execute('init();Controls.Window:SetHide(true);local n=sets;for i=1,10000 do tick(1) end;assert(sets==n and sends==0)')
print('UnitSites PASS hidden 10000 ticks: no formatting/layout/request')

# Frozen C2 scenarios intentionally signal a direct sample-input change before
# each logical pulse() group. They previously used generic pulses as that signal.
# Assertions of send/ACK/withdraw/retry/output are unchanged; D2 idle tested above.
s=s.replace("name=='SampleLifecycle'", "name in ('SampleLifecycle','RuntimeWork')")
s=s.replace("function pulse(n) for", "function pulse(n) fire('ResourceAddedToMap');for")
s=s.replace("get('version')=='102'", "get('version')=='103'").replace('P0-B-075.102','P0-B-076.103')
s=s.replace("b.execute('pulse(2);d.Audit()')", "b.execute(\"fire('GovernorChanged');pulse(2);d.Audit()\")")
exec(compile(s,'C2_contract_with_explicit_dirty','exec'),{'__file__':str(R/'DevelopmentTests/test_arch_v2_c2.py')})
