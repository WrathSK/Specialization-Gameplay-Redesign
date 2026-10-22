"""C1: actual UI/Gameplay Lua with delayed transport, native calls mocked. No game/DB."""
from pathlib import Path
import subprocess
from lupa.lua55 import LuaRuntime
R=Path(__file__).resolve().parents[1];M=R/'Mod'
FIX=r"""
turn=1;Game={GetCurrentGameTurn=function() return turn end,GetLocalPlayer=function() return 0 end}
ExposedMembers={};hooks={};Events=setmetatable({},{__index=function(t,k) local e={Add=function(f) hooks[k]=hooks[k] or {};table.insert(hooks[k],f) end,Remove=function() end};rawset(t,k,e);return e end})
function fire(n) for _,f in ipairs(hooks[n] or {}) do f(0) end end
include=function() end;Locale={Lookup=function(x) return x end}
P={VERSION='C1',IsTestPlayer=function(id) return id==0 end,Field=function(t,k) return t and t[k] end};SPCP0=P
rows={TEST={Index=1,Hash=1,BuildingType='TEST'}};rows[1]=rows.TEST
for n=1,4 do rows['BUILDING_SPC_B054_TEST_'..n]={Index=100+n} end
P.Info=function(t,k) if t=='Yields' then return {Index=1} end;return rows[k] end
cities={};for id=1,4 do
 local c={id=id,owner=0,built={},kind='INDUSTRY',active=4,x=id};cities[id]=c
 c.GetID=function() return c.id end;c.GetX=function() return c.x end;c.GetY=function() return 1 end;c.GetName=function() return 'C'..c.id end;c.GetOwner=function() return c.owner end
 c.GetBuildings=function() return c.built end;c.GetBuildQueue=function() return c.built end
end
writes=0;creates=0;removes=0;propertyWrites=0
P.HasBuilding=function(b,i) return b[i]==true end
P.CreateBuilding=function(b,i) assert(not b[i]);b[i]=true;writes=writes+1;creates=creates+1 end
P.RemoveBuilding=function(b,i) assert(b[i]);b[i]=nil;writes=writes+1;removes=removes+1 end
Players={[0]={GetCities=function() return {Members=function() return ipairs(cities) end,FindID=function(_,id) return cities[id] end} end}}
receivers={[2]={1},[3]={1},[4]={1}};unknown=false;permission=true;permissionUnknown=false
shared={Version=P.VERSION,Standardization={ReadLedger=function() return {learned={TEST=true}} end},EffectiveFacts={Read=function(pid,c) return {specialization=c.kind,active=c.active} end},NetworkBridge={players={[0]={validity='VERIFIED'}},RecipientSources=function(pid,c) if unknown then error('NETWORK_REFRESH_PENDING') end;return receivers[c.id] or {} end}}
ExposedMembers.SPC_P0=shared
SPCStandardizationCatalog={Build=function() return {buildings={TEST={enabled=true,group='T1',name='Test'}}} end}
ContextPtr={SetInitHandler=function(_,f) initUI=f end,SetShutdown=function(_,f) shutdownUI=f end,SetUpdate=function(_,f) tick=f end,ClearUpdate=function() end}
CityCommandTypes={PARAM_BUILDING_TYPE=1,PARAM_YIELD_TYPE=2,PURCHASE=3};PlayerOperations={EXECUTE_SCRIPT=1}
CityManager={CanStartCommand=function() if permissionUnknown then return nil end;return permission end}
queue={};sends=0;sync=false;transportError=false
function deliver(p) if p.Action=='DISCOUNT_INIT' then d.Initialize(0,p) else d.Receive(0,p) end end
UI={RequestPlayerOperation=function(pid,op,p) sends=sends+1;queue[#queue+1]=p;if transportError then error('TRANSPORT') end;if sync then deliver(p) end end}
function total(n) return ExposedMembers.SPC_Performance.entries[n].total end
function rate(id) for n=1,4 do if cities[id].built[100+n] then return n*10 end end;return 0 end
function pulse(n) for i=1,n or 1 do fire('GameCoreEventPublishComplete') end end
function ready() d.EnsureReady(0);sync=true;initUI();pulse(3);assert(rate(2)==40) end
function packet(seq,data,valid)
 local p={ClientEpoch=ExposedMembers.SPC_DiscountClientEpoch,Generation=d.generation,Seq=seq,Revision=d.plans[0].revision,Turn=turn,Data=data or '2,1,1;3,1,1;4,1,1',Count=3,Valid=valid or 1}
 ExposedMembers.SPC_DiscountIssued={ClientEpoch=p.ClientEpoch,Generation=p.Generation,Seq=seq};return p
end
"""
def runtime(source=None,ui=True):
 l=LuaRuntime(unpack_returned_tuples=True);l.execute(FIX)
 l.execute((M/'PerformanceCounters.lua').read_text());l.execute('ExposedMembers.SPC_Performance=SPCPerformance.New();P.Count=SPCPerformance.Count')
 l.execute(source or (M/'StandardizationDiscount.lua').read_text());l.execute('SPCStandardizationDiscount.Start(P,shared);d=shared.StandardizationDiscount')
 if ui:l.execute((M/'UI/DiscountEligibility.lua').read_text())
 return l
l=runtime();l.execute(r"""
-- INIT pending survives 100k events without generating another actual request.
initUI();pulse(100000);assert(sends==1 and total('discount_pending')>=100000)
deliver(queue[1]);pulse();assert(sends==2 and ExposedMembers.SPC_DiscountEligibility.pending==1)
local sample=queue[2];pulse(100000);assert(sends==2 and writes==0)
deliver(sample);pulse();assert(rate(2)==40 and d.appliedSamples==1)
local w=writes;local s=sends;pulse(1000);assert(writes==w and sends==s)
d.Receive(0,sample);assert(writes==w and d.appliedSamples==1)
-- Different transport number, identical sample is not an application.
local p=packet(100);d.Receive(0,p);assert(d.appliedSamples==1 and writes==w)
-- Temporary failures and turn rollover retain verified state.
unknown=true;pulse(10);assert(rate(2)==40 and writes==w)
unknown=false;turn=2;d.Audit();assert(rate(2)==40 and writes==w)
p=packet(101);p.Valid=0;d.Receive(0,p);assert(rate(2)==40 and writes==w)
p=packet(102);p.Count=0;p.Data='';d.Receive(0,p);assert(rate(2)==40 and writes==w)
-- Old turn, wrong epoch, out-of-order cannot overwrite newer ACK or sample.
p=packet(103);p.Turn=1;d.Receive(0,p);assert(d.responses[0].Status=='STALE' and writes==w)
p=packet(104);p.ClientEpoch=p.ClientEpoch-1;d.Receive(0,p);assert(d.responses[0].Seq==103)
p=packet(105,'2,1,0;3,1,0;4,1,0');d.Receive(0,p);assert(rate(2)==0 and removes==3)
local n=writes;d.Receive(0,p);assert(writes==n)
ExposedMembers.SPC_DiscountIssued={ClientEpoch=sample.ClientEpoch,Generation=sample.Generation,Seq=sample.Seq}
d.Receive(0,sample);assert(writes==n and d.responses[0].Seq==105)
-- Timeout older delivery cannot apply once a newer request has been issued.
local old=packet(106);local newer=packet(107,'2,1,0;3,1,0;4,1,0');d.Receive(0,old);assert(writes==n)
d.Receive(0,newer);assert(writes==n)
""");print('PASS C1: 200k pending events / two actual requests including INIT; atomic samples/duplicate/stale/false withdrawal')
l=runtime();l.execute(r"""
initUI();for k=1,20 do tick(6);pulse(1000) end
assert(sends==3 and total('discount_retry')==2 and ExposedMembers.SPC_DiscountEligibility.state=='RETRY_EXHAUSTED')
local old=queue[1];fire('LoadScreenClose');assert(sends==4);local w=writes;deliver(old);assert(writes==w and total('discount_stale')>0)
""");print('PASS C1: timeout budget 3 sends, load rejects old client/epoch')
l=runtime();l.execute(r"""
transportError=true;initUI();for i=1,20 do tick(6);pulse(100) end;assert(sends==3)
""");print('PASS C1: transport exceptions bounded')
l=runtime();l.execute(r"""
ready();sync=false;local w=writes;permissionUnknown=true;pulse();deliver(queue[#queue]);pulse(20);assert(rate(2)==40 and writes==w)
-- Source validity is independent of pending UI permission.
receivers[2]={};d.Audit();assert(rate(2)==0 and removes==1);d.Audit();assert(removes==1)
unknown=true;shared.NetworkBridge.players[0].validity='CONFIRMED_INVALID';d.Audit();assert(rate(3)==0 and rate(4)==0 and removes==3)
d.Audit();assert(removes==3)
""");print('PASS C1: unavailable UI holds, confirmed network loss withdraws once')
l=runtime();l.execute(r"""
ready();sync=false;local w=writes
fire('LoadScreenClose');assert(rate(2)==40 and writes==w)
receivers[2]={};d.Audit();assert(rate(2)==0 and removes==1)
local q=queue[#queue];deliver(q);pulse(3)
""");print('PASS C1: reload does not clear still-planned carrier; confirmed target loss still removes')
l=runtime();l.execute(r"""
ready();sync=false;local w=writes
cities[1].active=nil;d.Audit();assert(rate(2)==40 and writes==w)
cities[1].active=0;d.Audit();assert(rate(2)==0 and removes==3)
cities[1].active=4;d.Audit();assert(rate(2)==0) -- no resurrecting retired permission
pulse();deliver(queue[#queue]);pulse();assert(rate(2)==40)
local pendingPacket=queue[#queue];local oldEpoch=ExposedMembers.SPC_DiscountClientEpoch
shutdownUI();d.Receive(0,pendingPacket);assert(ExposedMembers.SPC_DiscountIssued==nil)
""");print('PASS C1: unknown ACTIVE retained / ACTIVE zero withdrawn / permission reacquired / shutdown late packet')
l=runtime();l.execute(r"""
initUI();for i=1,4 do tick(6);pulse() end
local w=writes;deliver(queue[#queue]);assert(writes==w and not d.ready)
""");print('PASS C1: exhausted timeout retires final outstanding request')
l=runtime();l.execute(r"""
cities={};sync=true;initUI();pulse(10);local sent=sends;local applied=d.appliedSamples
pulse(1000);assert(sends==sent and d.appliedSamples==applied and writes==0)
assert(ExposedMembers.SPC_DiscountEligibility.pending==0)
""");print('PASS C1: zero-city initialization settles without repeat sends')
# Normal verified results versus B071's real discount module (no UI timing equivalence claimed).
old=subprocess.check_output(['git','-C',str(R),'show','407717c:Mod/StandardizationDiscount.lua'],text=True)
a,b=runtime(old,False),runtime(ui=False)
for l in (a,b):l.execute('d.EnsureReady(0);ExposedMembers.SPC_DiscountClientEpoch=1')
seq=0
for level in range(1,5):
 for allowed in (True,False,True):
  seq+=1
  for l in (a,b):
   l.execute(f"cities[1].active={level};d.Audit();p=packet({seq},'2,1,{int(allowed)};3,1,{int(allowed)};4,1,{int(allowed)}');d.Receive(0,p)")
  assert [a.eval(f'rate({c})') for c in range(1,5)]==[b.eval(f'rate({c})') for c in range(1,5)]
print('PASS C1: 12 normal verified level/permission cases equal B071 across all 4 cities')
for p in M.rglob('*.lua'):
 result=l.eval('load')(p.read_text(),str(p));assert not isinstance(result,tuple),(p,result)
print('PASS all Lua syntax')

# Preserve A/B/B069 assertions; only adapt the historical build stamp in memory.
import sys
sys.path.insert(0,str(R/'DevelopmentTests'))
p=R/'DevelopmentTests/test_runtime_audit_regression.py'
source=p.read_text().replace("\"get('version')=='99'\"", "\"get('version')=='100'\"")
exec(compile(source,str(p),'exec'),{'__file__':str(p)})
