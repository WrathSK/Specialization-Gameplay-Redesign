"""AV2-A real Lua contract tests + unchanged B069 behavioral regression, no deployment."""
from pathlib import Path
from lupa.lua55 import LuaRuntime
import subprocess
R=Path(__file__).resolve().parents[1];M=R/'Mod'
# Preserve historical B069 assertions. Only supply new native city-reference getters and build stamp.
old=(R/'DevelopmentTests/test_b069_performance.py').read_text()
old=old.replace('c.SetProperty=function() engineProps=engineProps+1 end',
 'c.SetProperty=function() engineProps=engineProps+1 end;c.GetX=function() return c.id end;c.GetY=function() return 0 end;c.GetProperty=function() return nil end')
old=old.replace("get('version')=='96'", "get('version')=='97'")
exec(compile(old,'B069_behavior_regression','exec'),{'__file__':str(R/'DevelopmentTests/test_b069_performance.py')})
FIXTURE=r"""
turn=1;ExposedMembers={};print=function() end
Game={GetCurrentGameTurn=function() return turn end}
function events() return setmetatable({},{__index=function(t,k) local fs={};local e={Add=function(f) fs[#fs+1]=f end,Fire=function(...) for _,f in ipairs(fs) do f(...) end end};rawset(t,k,e);return e end}) end
Events=events();GameEvents=events();counts={};audits=0;writes=0;propertyWrites=0;desired={};capitalID=1;routeCount=0;seq=0
cities={};units={};readFail=false;war=false;capitalFail=false
for id=1,5 do
 local c={id=id,owner=0,token='CITY'..id,kind=({ 'RESEARCH','COMMERCE','NONE','CULTURE','INDUSTRY'})[id],active=3,potential=4}
 if c.kind=='NONE' then c.active=0;c.potential=0 end
 c.GetID=function() return c.id end;c.GetOwner=function() return c.owner end
 c.GetX=function() return c.id end;c.GetY=function() return 10 end
 c.GetProperty=function(_,key) if key=='SPC_DEV_BINDING_B013_TOKEN' then return c.token end end
 c.SetProperty=function() propertyWrites=propertyWrites+1 end
 c.GetName=function() return 'C'..c.id end
 cities[id]=c
end
for i=10,30 do units[i]={} end
Players={[0]={GetCities=function() return {FindID=function(_,id) return cities[id] end,Members=function() return pairs(cities) end,
 GetCapitalCity=function() if capitalFail then error('TEMP_CAPITAL') end;return cities[capitalID] end} end,
 GetUnits=function() return {FindID=function(_,id) return units[id] end} end,
 GetTrade=function() return {CountOutgoingRoutes=function() return routeCount end} end,
 GetDiplomacy=function() return {IsAtWarWith=function() return war end} end}}
P={VERSION='P0-B-070.97',IsTestPlayer=function(pid) return pid==0 end,Field=function(t,k) return t and t[k] end,
 Count=function(k) counts[k]=(counts[k] or 0)+1 end}
shared={RouteSignalRevision=0,EffectiveFacts={Read=function(pid,c)
 if readFail or c.fail then error('TEMP_FACT_READ') end
 return {owner=pid,cityID=c.id,token=c.token,specialization=c.kind,potential=c.potential,active=c.active,
 first=c.kind~='NONE' and {districtID=c.id,type='DISTRICT_'..c.kind} or nil}
end}}
function send(data,n,customSeq)
 routeCount=n;seq=customSeq or seq+1
 net.Receive(0,{Epoch=net.epoch,Seq=seq,Turn=turn,Signal=shared.RouteSignalRevision,Valid=1,Count=n,Data=data})
end
function output()
 local n=net.National(0);local t={}
 for _,k in ipairs({'RESEARCH','CULTURE'}) do
  local a=n[k];local s={};for id,level in pairs(a.sources) do s[#s+1]=id..':'..level end;table.sort(s)
  t[#t+1]=k..':'..a.level..':'..a.n..':'..table.concat(s,',')
 end
 for id,c in pairs(cities) do
  local kinds=net.ConnectedKinds(0,c);local names={};for k in pairs(kinds) do names[#names+1]=k end;table.sort(names)
  t[#t+1]='C'..id..':'..table.concat(names,',')
  for _,k in ipairs({'RESEARCH','CULTURE','INDUSTRY'}) do t[#t+1]=id..k..':'..table.concat(net.RecipientSources(0,c,k),',') end
 end
 table.sort(t);return table.concat(t,';')
end
"""
def runtime(source=None):
 l=LuaRuntime(unpack_returned_tuples=True)
 l.globals().include=lambda name:l.execute((M/(name+'.lua')).read_text())
 l.execute(FIXTURE)
 l.execute(source if source is not None else (M/'NetworkBridge.lua').read_text())
 l.execute('SPCNetworkBridge.Start(P,shared);net=shared.NetworkBridge;net.ready=true')
 return l
l=runtime()
l.execute(r"""
-- The consumer sees committed metadata before any Audit and applies only genuine differences.
shared.NetworkBoost={Audit=function(publication)
 audits=audits+1;local m=net.Input(0);assert(publication.inputVersion==m.inputVersion and publication.signature==m.signature)
 assert(m.derivedFor==nil or m.derivedFor==m.inputVersion)
 local ok,n=pcall(net.National,0);local value=ok and n.RESEARCH.level*math.sqrt(n.RESEARCH.n) or 0
 if desired[0]~=value then writes=writes+1;desired[0]=value end
end}
send('0,1,0,2,10;0,2,0,3,11;0,4,0,2,12',3)
local b=net.players[0];assert(b.inputRevision==1 and audits==1 and b.validity=='VERIFIED')
local initial=net.Input(0);local r=b.revision;local w=writes;local d=counts.derive
-- A: repeated signals, turn changes, packets, and refreshes are not new facts.
for i=1,10 do net.Rebuild();send('0,4,0,2,12;0,2,0,3,11;0,1,0,2,10',3) end
turn=2;Events.PlayerTurnActivated.Fire(0)
assert(b.inputRevision==1 and b.derivedRevision==1 and audits==1 and writes==w and propertyWrites==0)
assert(counts.derive==d)
-- B/C: source ACTIVE changes with exactly the same routes.
cities[1].active=4;Events.GovernorPromoted.Fire(0)
assert(b.inputRevision==2 and audits==2 and b.revision==r and net.National(0).RESEARCH.level==4)
cities[1].active=3;Events.GovernorChanged.Fire(0)
assert(b.inputRevision==3 and audits==3 and net.National(0).RESEARCH.level==3)
local withdrawals=counts.withdrawal
-- D: confirmed loss of qualification removes source once; recovery is a fresh fact version.
cities[1].kind='NONE';cities[1].potential=0;cities[1].active=0;GameEvents.OnDistrictConstructed.Fire(0)
assert(b.inputRevision==4 and audits==4 and net.National(0).RESEARCH.n==0 and counts.withdrawal==withdrawals+1)
net.Rebuild();assert(audits==4)
cities[1].kind='RESEARCH';cities[1].potential=4;cities[1].active=3;net.Rebuild();assert(b.inputRevision==5)
-- E: Capital and Commerce center identity, not turn/route, affect input.
capitalID=3;Events.CapitalCityChanged.Fire();assert(b.inputRevision==6 and b.revision==r)
cities[2].kind='NONE';cities[2].active=0;cities[2].potential=0;net.Rebuild();assert(b.inputRevision==7)
assert(net.National(0).RESEARCH.n==0)
cities[2].kind='COMMERCE';cities[2].potential=4;cities[2].active=3;net.Rebuild();assert(b.inputRevision==8)
-- F: actual route removal/addition is one publication each, no intermediate empty publication.
local before=b.inputRevision;local calls=audits
send('0,1,0,2,10;0,4,0,2,12',2);assert(b.inputRevision==before+1 and audits==calls+1)
send('0,1,0,2,10;0,2,0,3,11;0,4,0,2,12',3);assert(b.inputRevision==before+2 and audits==calls+2)
-- G/H: dirty, malformed/unknown bridge, temporary Governor and capital read failure retain accepted facts.
before=b.inputRevision;calls=audits;local baseline=output();w=writes
net.CheckEvidence(false);send('0,1,0,2,10;0,2,0,3,11;0,4,0,2,12',3)
net.Receive(0,{Epoch=net.epoch,Seq=seq+1,Turn=turn,Signal=0,Valid=0});seq=seq+1
assert(output()==baseline)
readFail=true;net.Rebuild();assert(net.Input(0).availability=='NEEDS_REVALIDATION' and output()==baseline)
readFail=false;cities[1].active=nil;net.Rebuild();assert(output()==baseline)
cities[1].active=3;capitalFail=true;net.Rebuild();assert(b.inputRevision==before)
capitalFail=false;net.Rebuild();assert(b.inputRevision==before and audits==calls and writes==w)
-- I: old seq, old turn, and old epoch cannot overwrite a newer input.
local sig=b.inputSignature
net.Receive(0,{Epoch=net.epoch,Seq=seq-1,Turn=turn,Signal=0,Valid=1,Count=0,Data=''})
net.Receive(0,{Epoch=net.epoch-1,Seq=seq+500,Turn=turn,Signal=0,Valid=1,Count=0,Data=''})
net.Receive(0,{Epoch=net.epoch,Seq=seq+1,Turn=turn-1,Signal=0,Valid=1,Count=0,Data='' });seq=seq+1
assert(b.inputSignature==sig and b.inputRevision==before and audits==calls and counts.stale_input>=3)
-- Explicit endpoint loss/war/trader destruction withdraw once with an input version, not silent mutation.
cities[3]=nil;Events.CityRemovedFromMap.Fire();assert(b.validity=='CONFIRMED_INVALID' and not b.routes)
assert(b.inputRevision==before+1 and audits==calls+1 and b.derivedFor==nil)
net.CheckEvidence(false);assert(audits==calls+1)
send('0,1,0,2,10;0,4,0,2,12',2);assert(b.validity=='VERIFIED' and b.derivedFor==b.inputRevision)
-- Getter unreadability without positive invalidity does not become zero.
local m=net.Input(0);local oldGetter=cities[2].GetProperty
cities[2].GetProperty=function() error('TEMP_PROPERTY') end;net.Rebuild()
assert(b.inputRevision==m.inputVersion and b.routes)
cities[2].GetProperty=oldGetter
-- A confirmed current identity replacement is different even if owner/cityID/coordinates are reused.
cities[2].token='REPLACED';Events.CityTransfered.Fire();assert(b.validity=='CONFIRMED_INVALID')
local last=b.inputRevision;Events.CityTransfered.Fire();assert(b.inputRevision==last)
assert(propertyWrites==0)
""")
# Unknown startup is not a confirmed-empty publication; recovery needs no unrelated route event.
u=runtime()
u.execute(r"""
readFail=true;send('0,1,0,2,10',1)
assert(net.Input(0).validity=='UNKNOWN' and net.Input(0).inputVersion==0 and not net.players[0].routes)
readFail=false;Events.GovernorEstablished.Fire();assert(net.Input(0).inputVersion==1 and net.players[0].routes)
local b=net.players[0];local version=b.inputRevision;local signature=b.inputSignature
cities[1].active=3.0;net.Rebuild();assert(b.inputRevision==version and b.inputSignature==signature)
-- A newer equal-to-current packet supersedes an unpublished different candidate.
capitalFail=true;send('0,1,0,2,10;0,2,0,3,11',2)
assert(b.candidate and b.inputRevision==version)
send('0,1,0,2,10',1);assert(not b.candidate)
capitalFail=false;net.Rebuild();assert(#b.routes==1 and b.inputRevision==version)
-- Potential participates even if the established Governor keeps ACTIVE unchanged.
cities[1].potential=3;net.Rebuild();assert(b.inputRevision==version+1 and b.revision==1)
-- Known new input plus a transient source read uses the last confirmed source value, not zero.
cities[1].fail=true;capitalID=2;net.Rebuild()
assert(b.inputRevision==version+2 and net.National(0).RESEARCH.level==3 and b.availability=='NEEDS_REVALIDATION')
cities[1].fail=false;net.Rebuild();assert(b.inputRevision==version+2)
-- An untracked pre-Mod city is excluded without adopting or modifying its records.
shared.CityFlowProbe={ready=true};cities[5].fail=true;net.Rebuild()
-- Previously known city retains last verified facts, rather than treating disappearance of a record as permission to erase it.
assert(b.input.cities[5].specialization=='INDUSTRY');cities[5].fail=false
-- Confirmed route loss must not hide behind an unrelated unknown new city/sample.
local extra={GetID=function() return 6 end,GetOwner=function() return 0 end,GetX=function() return 6 end,
 GetY=function() return 10 end,GetProperty=function() return 'INCOMPLETE' end,fail=true}
cities[6]=extra;send('',0)
assert(b.validity=='CONFIRMED_INVALID' and not b.routes)
cities[6]=nil;send('',0);assert(b.validity=='VERIFIED' and #b.routes==0)
-- Actual trader removal is a formal withdrawal exactly once.
send('0,1,0,2,10',1);local v=b.inputRevision;units[10]=nil;Events.UnitRemovedFromMap.Fire(0,10)
assert(b.validity=='CONFIRMED_INVALID' and b.inputRevision==v+1)
Events.UnitRemovedFromMap.Fire(0,10);assert(b.inputRevision==v+1)
units[10]={}
-- International endpoint and war evidence participate without treating foreign progression as ours.
local foreign={GetID=function() return 50 end,GetOwner=function() return 1 end,GetX=function() return 50 end,
 GetY=function() return 5 end,GetProperty=function() return nil end}
Players[1]={GetCities=function() return {FindID=function(_,id) if id==50 then return foreign end end} end}
send('0,1,1,50,10',1);assert(b.validity=='VERIFIED')
v=b.inputRevision;war=true;Events.DiplomacyDeclareWar.Fire();assert(b.inputRevision==v+1 and b.validity=='CONFIRMED_INVALID')
-- A current packet cannot reintroduce a route already proved at war.
send('0,1,1,50,10',1);assert(b.inputRevision==v+1 and not b.routes)
war=false;send('0,1,0,2,10',1)
-- Reentrant queries/duplicate packets during publication cannot overwrite the committed input.
local seen=0
shared.NetworkBoost={Audit=function(m)
 seen=seen+1;assert(net.Input(0).inputVersion==m.inputVersion)
 net.Rebuild();net.Receive(0,{Epoch=net.epoch,Seq=9999,Valid=0})
 assert(net.Input(0).inputVersion==m.inputVersion)
end}
cities[1].active=4;net.Rebuild();assert(seen==1 and b.seq~=9999)
-- Per-session epochs prevent stale previous-load messages and inputs from being restored.
local epoch=net.epoch;SPCNetworkBridge.Start(P,shared);net=shared.NetworkBridge;net.ready=true
net.Receive(0,{Epoch=epoch,Seq=10000,Turn=turn,Signal=0,Valid=1,Count=0,Data=''})
assert(net.Input(0).inputVersion==0 and net.Input(0).validity=='UNKNOWN')
assert(propertyWrites==0)
""")
# Exhaustive representative network outputs compared to the exact pre-refactor source.
base=subprocess.check_output(['git','-C',str(R),'show','79281ff:Mod/NetworkBridge.lua'],text=True)
a=runtime(base);b=runtime()
for lua in (a,b):lua.execute("send('0,1,0,2,10;0,4,0,2,11;0,5,0,2,12;0,2,0,3,13;0,3,0,4,14',5)")
comparisons=0
for level in range(1,5):
 for cap in (1,2,3):
  for center in ('COMMERCE','NONE'):
   cmd=f"cities[1].active={level};cities[4].active={5-level};capitalID={cap};cities[3].kind='{center}';cities[3].potential={4 if center=='COMMERCE' else 0};cities[3].active={1 if center=='COMMERCE' else 0};net.Rebuild()"
   a.execute(cmd);b.execute(cmd)
   assert a.eval('output()')==b.eval('output()'),(level,cap,center)
   comparisons+=1
print(f'AV2-A LOCAL_SIMULATION_PASS: A-I contract cases, native-reference loss, duplicate/no-op writes, and {comparisons} old/new topology/National/direct-reception/source-set comparisons.')
