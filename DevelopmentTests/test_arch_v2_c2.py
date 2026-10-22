"""C2 real Lua producers/receivers/carriers, mocked native API; no deployment."""
from pathlib import Path
import subprocess,xml.etree.ElementTree as ET
from lupa.lua55 import LuaRuntime
R=Path(__file__).resolve().parents[1];M=R/'Mod'
FIX=r"""
turn=1;ExposedMembers={};hooks={};Game={GetCurrentGameTurn=function() return turn end,GetLocalPlayer=function() return 0 end}
Events=setmetatable({},{__index=function(t,k) local e={Add=function(f) hooks[k]=hooks[k] or {};table.insert(hooks[k],f) end,Remove=function() end};rawset(t,k,e);return e end});GameEvents=Events
function fire(n) for _,f in ipairs(hooks[n] or {}) do f(0) end end
P={VERSION='C2',IsTestPlayer=function(pid) return pid==0 end,Field=function(t,k) return t[k] end};SPCP0=P
P.Info=function(t,k) if t=='Buildings' then return {Index=k} elseif t=='Yields' then return {Index=k:gsub('YIELD_','')} else return {DistrictType=k} end end
writes=0;P.HasBuilding=function(b,i) return b[i]==true end
P.CreateBuilding=function(b,i) assert(not b[i]);b[i]=true;writes=writes+1 end
P.RemoveBuilding=function(b,i) assert(b[i]);b[i]=nil;writes=writes+1 end
cities={};for id=1,2 do local c={id=id,owner=0,pop=3,token='CITY'..id,built={}};cities[id]=c
 c.GetID=function() return c.id end;c.GetOwner=function() return c.owner end;c.GetPopulation=function() return c.pop end;c.GetX=function() return id end;c.GetY=function() return 1 end
 c.GetProperty=function() return c.token end;c.GetBuildings=function() return c.built end;c.GetBuildQueue=function() return c.built end
end
facts={{specialization='RESEARCH',potential=4,active=4,first={districtID=11,type='DISTRICT_CAMPUS'}},{specialization='INDUSTRY',potential=4,active=4,first={districtID=12,type='DISTRICT_INDUSTRIAL_ZONE'}}}
districts={};function district(id,cid,kind,prod)
 local d={id=id,cid=cid,kind=kind,prod=prod,base=6,complete=true,x=id};districts[id]=d
 d.GetID=function() return id end;d.GetType=function() return d.kind end;d.GetCity=function() return cities[cid] end;d.IsComplete=function() return d.complete end
 d.GetX=function() return d.x end;d.GetY=function() return 1 end
 d.GetYield=function(_,y) if unavailable then error('NATIVE_NOT_READY') end;return y=='PRODUCTION' and d.prod or 0 end
 return d
end
district(11,1,'DISTRICT_CAMPUS',100);district(12,2,'DISTRICT_INDUSTRIAL_ZONE',7);district(13,1,'DISTRICT_THEATER',6)
Players={[0]={GetCities=function() return {Members=function() return pairs(cities) end,FindID=function(_,id) return cities[id] end} end,
 GetDistricts=function() return {Members=function() return pairs(districts) end} end}}
Map={GetPlot=function(x,y) return {GetAdjacencyYield=function() if unavailable then error('NATIVE_NOT_READY') end;return districts[x].base end} end}
shared={Version=P.VERSION,EffectiveFacts={Read=function(pid,c) if factUnknown then error('FACT_UNAVAILABLE') end;return facts[c.id] end},NetworkBridge={players={[0]={validity='VERIFIED'}},RecipientSources=function(pid,c)
 if networkUnknown then error('NETWORK_UNAVAILABLE') end;return c.id==1 and (networkOff and {} or {2}) or {}
end}};ExposedMembers.SPC_P0=shared
ContextPtr={SetInitHandler=function(_,f) initUI=f end,SetUpdate=function(_,f) tick=f end,SetShutdown=function(_,f) closeUI=f end,ClearUpdate=function() end}
PlayerOperations={EXECUTE_SCRIPT=1};queue={};sync=false;sends=0
UI={RequestPlayerOperation=function(pid,op,p) sends=sends+1;queue[#queue+1]=p;if failSend then error('SEND_ERROR') end;if sync then d.Receive(pid,p) end end}
function pulse(n) for i=1,n or 1 do fire('GameCoreEventPublishComplete') end end
function total(n) return ExposedMembers.SPC_Performance.entries[n].total end
function clone(t) local o={};for k,v in pairs(t) do o[k]=type(v)=='table' and clone(v) or v end;return o end
function encode(t) local a={};for k,v in pairs(t) do a[#a+1]=tostring(k)..'='..(type(v)=='table' and encode(v) or tostring(v)) end;table.sort(a);return table.concat(a,';') end
function output() return encode({cities[1].built,cities[2].built}) end
function amount(c,y)
 local n=0;for id in pairs(c.built) do local yield,mode,bit=id:match('B051_(%u+)_(%u+)_(%d+)$');if yield==y then bit=tonumber(bit);n=n+(mode=='POP' and c.pop/2^(bit+1) or (mode=='NEG' and -2^bit or 2^bit)) end end;return n
end
"""
def runtime(k,old=False):
 l=LuaRuntime(unpack_returned_tuples=True)
 l.globals().include=lambda name: l.execute((M/(name+'.lua')).read_text()) if name=='SampleLifecycle' else None
 l.execute(FIX);l.execute((M/'PerformanceCounters.lua').read_text());l.execute('ExposedMembers.SPC_Performance=SPCPerformance.New();P.Count=SPCPerformance.Count')
 mod='CopyYields' if k=='copy' else 'IndustrySupport'
 source=subprocess.check_output(['git','show','e1549aa:Mod/'+mod+'.lua'],cwd=R,text=True) if old else (M/(mod+'.lua')).read_text()
 l.execute(source);l.execute(f'SPC{mod}.Start(P,shared);d=shared.{mod};d.ready=true')
 if not old:
  l.execute((M/'UI'/('CopyYieldRefresh.lua' if k=='copy' else 'IndustryRefresh.lua')).read_text())
 return l
for k in ['copy','industry']:
 l=runtime(k);l.globals().kind=k
 l.execute(r"""
initUI();assert(sends==1);local first=queue[1];local w=writes
pulse(10000);assert(sends==1 and writes==w and total(kind..'_apply')==0)
d.Receive(0,first);pulse();assert(total(kind..'_apply')==1 and sends==1)
local baseline=output();local w=writes;d.Receive(0,first);assert(writes==w and total(kind..'_apply')==1)
-- Hold a pending value update and old values through large generic notification burst.
districts[12].prod=9;districts[12].base=7;pulse();local newer=queue[#queue];assert(sends==2)
pulse(10000);assert(sends==2 and output()==baseline and writes==w)
d.Receive(0,first);assert(writes==w);d.Receive(0,newer);pulse();assert(total(kind..'_apply')==2)
local w=writes;d.Receive(0,first);d.Receive(0,newer);assert(writes==w and total(kind..'_apply')==2)
-- Temporary native getter failure: invalid response, no sample replacement/clear.
unavailable=true;pulse();d.Receive(0,queue[#queue]);local last=output();local w=writes
pulse(10000);assert(output()==last and writes==w)
for i=1,10 do tick(6);pulse();d.Receive(0,queue[#queue]) end
assert(output()==last and writes==w and total(kind..'_retry')==2)
-- Turn expires old packet; full fresh input can recover.
local old=queue[#queue];unavailable=false;turn=2;pulse();local fresh=queue[#queue]
d.Receive(0,old);assert(writes==w);d.Receive(0,fresh);pulse();assert(output()==last)
-- Prepared in old reference, native reference changes before response.
districts[12].prod=11;districts[12].base=8;pulse();local bad=queue[#queue]
cities[2].token='REPLACED';local a=total(kind..'_apply');d.Receive(0,bad);assert(total(kind..'_apply')==a)
d.Audit();local r=total(kind..'_withdraw');assert(r>0);local w=writes;d.Audit();assert(writes==w and total(kind..'_withdraw')==r)
-- Old epoch can never apply to reload.
fire('LoadScreenClose');local a=total(kind..'_apply');d.Receive(0,bad);assert(total(kind..'_apply')==a)
local latest=queue[#queue];d.Receive(0,latest);pulse();closeUI();d.Receive(0,latest)
assert(total(kind..'_pending')>=20000 and total(kind..'_stale')>0)
""")
 print(k,'PASS normal send1/apply1, two 10k pending bursts, duplicate/old sequence/reference/epoch, temporary hold, retries bounded')
 for fail in [False,True]:
  l=runtime(k);l.execute(f'failSend={str(fail).lower()};initUI();for i=1,20 do tick(6);pulse(1000) end;assert(sends==3)')
 print(k,'PASS timeout and throwing transport max3 sends')
 l=runtime(k);l.globals().kind=k;l.execute(r"""
sync=true;initUI();pulse();local w=writes;local old=output();turn=2;d.Audit();assert(writes==w and output()==old)
-- Confirmation of removed district must revoke, once, even without a new UI sample.
districts[12]=nil;d.Audit();local w=writes;local r=total(kind..'_withdraw');assert(r>0)
d.Audit();assert(writes==w and total(kind..'_withdraw')==r)
""");print(k,'PASS old turn hold / confirmed district retirement once')
 # Malformed, partial, stale turn and city-owner response tests.
 l=runtime(k);l.globals().kind=k;l.execute(r"""
initUI();local p=queue[1];local a=total(kind..'_apply')
local bad=clone(p);bad.Count=999;d.Receive(0,bad);assert(total(kind..'_apply')==a)
-- New request identities for each subsequent malformed packet.
function tryBad(change)
 turn=turn+1;pulse();local bad=clone(queue[#queue]);change(bad);d.Receive(0,bad);assert(total(kind..'_apply')==0)
end
tryBad(function(p) p.Data='';p.Count=0 end)
tryBad(function(p) p.Turn=p.Turn-1 end)
tryBad(function(p) p.ClientEpoch=p.ClientEpoch-1 end)
tryBad(function(p) cities[2].owner=1 end)
""");print(k,'PASS partial/bad/old turn/old epoch/owner packets rejected atomically')
# Native delayed responses: measure the prior producers too, without speculative runtime attribution.
for k in ['copy','industry']:
 l=runtime(k,True);l.globals().include=lambda name:None
 filename='CopyYieldRefresh.lua' if k=='copy' else 'IndustryRefresh.lua'
 l.execute(subprocess.check_output(['git','show','e1549aa:Mod/UI/'+filename],cwd=R,text=True))
 l.execute('initUI();pulse(10000)')
 sent=l.eval('sends');assert sent==(10001 if k=='copy' else 1)
 print(k,'B074 delayed response, initial +10000 notifications: actual sends',sent)
# Retiring an older UI context must not retire the replacement context request.
for k in ['copy','industry']:
 l=runtime(k);l.execute('initUI();oldClose=closeUI')
 l.execute((M/'UI'/('CopyYieldRefresh.lua' if k=='copy' else 'IndustryRefresh.lua')).read_text())
 l.execute('initUI();local p=queue[#queue];oldClose();d.Receive(0,p)')
 assert l.eval(f'total("{k}_apply")')==1
print('PASS old UI shutdown cannot cancel new UI request')
# Final carrier values versus B074; only normal valid inputs are equivalence oracle.
for k in ['copy','industry']:
 a,b=runtime(k,True),runtime(k)
 b.execute('sync=true;initUI();pulse()')
 for value in [0,1,2,5,6,13,100,255]:
  for level in [1,3,4]:
   for l in [a,b]:l.execute(f'districts[12].base={value};districts[12].prod={value};districts[13].prod={value};facts[2].active={level}')
   if k=='copy':a.execute("d.Receive(0,{Generation=d.generation,Seq=(d.seq[0] or 0)+1,Turn=turn,Valid=1,Count=3,Data='1,11,100,100;2,12,'..districts[12].prod..','..districts[12].prod..';1,13,'..districts[13].prod..','..districts[13].prod})")
   else:a.execute("d.Receive(0,{CityID=2,DistrictID=12,BaseProduction=districts[12].base})")
   b.execute('pulse(2);d.Audit()');assert a.eval('output()')==b.eval('output()'),(k,value,level)
 print(k,'PASS 24 normal carrier-map comparisons versus B074')
# Include actual Lv3 downstream carriers in normal Industry equivalence.
a,b=runtime('industry',True),runtime('industry')
for l,old in [(a,True),(b,False)]:
 source=subprocess.check_output(['git','show','e1549aa:Mod/Lv3Support.lua'],cwd=R,text=True) if old else (M/'Lv3Support.lua').read_text()
 l.execute(source);l.execute('SPCLv3Support.Start(P,shared);shared.Lv3Support.ready=true')
b.execute('sync=true;initUI();pulse()')
for value in [0,1,6,13,255]:
 for level in [1,3,4]:
  for l in [a,b]:l.execute(f'districts[12].base={value};facts[2].active={level}')
  a.execute('d.Receive(0,{CityID=2,DistrictID=12,BaseProduction=districts[12].base})')
  b.execute('pulse(2);d.Audit()');assert a.eval('output()')==b.eval('output()')
print('PASS 15 Industry Lv1+Lv3 carrier maps versus B074')
# Unknown native completion status is not proof of deletion.
for k in ['copy','industry']:
 l=runtime(k);l.execute('sync=true;initUI();pulse();local w=writes;districts[12].complete=nil;pulse(2);d.Audit();assert(writes==w)')
print('PASS temporary district completion nil preserves Copy/Industry projections')
# Industry Lv3 must not undo the newly protected Lv1 sample contract.
l=runtime('industry');l.execute((M/'Lv3Support.lua').read_text());l.execute(r"""
SPCLv3Support.Start(P,shared);shared.Lv3Support.ready=true
sync=true;initUI();pulse();local old=output();local w=writes
fire('LoadScreenClose');assert(output()==old and writes==w)
unavailable=true;pulse();shared.Lv3Support.Audit();assert(output()==old and writes==w)
facts[2].active=1;shared.Lv3Support.Audit();assert(not cities[2].built.BUILDING_SPC_DEV_LV3_INDUSTRY)
""");print('PASS Industry Lv3 load/unavailable hold and confirmed level withdrawal')
l=runtime('copy');l.execute(r"""
for pop=1,255 do for _,v in ipairs({0,0.5,1,1.5,999.5,65535.5}) do local p=SPCCopyYields.Plan(v,pop);assert(p.integer+pop*p.coefficient==v) end end
assert(not pcall(SPCCopyYields.Plan,0.65,3))
sync=true;initUI();pulse();districts[13].prod=1.3;pulse();assert(amount(cities[1],'SCIENCE')==0)
networkUnknown=true;local p=amount(cities[1],'PRODUCTION');d.Audit();assert(amount(cities[1],'PRODUCTION')==p)
shared.NetworkBridge.players[0].validity='CONFIRMED_INVALID';d.Audit();assert(amount(cities[1],'PRODUCTION')==0)
""");print('PASS Copy precision and confirmed Network invalidation; no precision policy change')
for p in M.rglob('*.lua'):
 result=l.eval('load')(p.read_text(),str(p));assert not isinstance(result,tuple),(p,result)
assert 'P0-B-075.102' in (M/'Probe.lua').read_text()
x=ET.parse(M/'SpecializationP0.modinfo').getroot();assert x.get('version')=='102'
for e in x.findall('.//File'):assert (M/e.text).exists(),e.text
print('PASS all Lua syntax and manifest references; C2 LOCAL_SIMULATION_PASS, not a game PASS')

# Current D1 entry preserves its behavioral assertions; only historical stamp is adapted.
p=R/'DevelopmentTests/test_arch_v2_d1.py'
s=p.read_text().replace("get('version')=='101'", "get('version')=='102'")
exec(compile(s,str(p),'exec'),{'__file__':str(p)})
