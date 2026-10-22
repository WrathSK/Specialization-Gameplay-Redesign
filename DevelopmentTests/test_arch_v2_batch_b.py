"""AV2-B: actual Lua bridge/discount/counters, historical output comparison; no deploy."""
from pathlib import Path
import subprocess
from lupa.lua55 import LuaRuntime
R=Path(__file__).resolve().parents[1];M=R/'Mod'
# Preserve Batch A/B069 behavioral assertions; adapt only the development manifest stamp.
namespace={'__file__':str(R/'DevelopmentTests/test_arch_v2_batch_a.py')}
s=(R/'DevelopmentTests/test_arch_v2_batch_a.py').read_text().replace("get('version')=='97'", "get('version')=='98'")
exec(compile(s,namespace['__file__'],'exec'),namespace)
FIXTURE=namespace['FIXTURE']
def runtime(source=None):
 l=LuaRuntime(unpack_returned_tuples=True)
 l.globals().include=lambda name:l.execute((M/(name+'.lua')).read_text())
 l.execute(FIXTURE)
 l.execute((M/'PerformanceCounters.lua').read_text())
 l.execute("ExposedMembers.SPC_Performance=SPCPerformance.New();P.Count=SPCPerformance.Count;counts=nil")
 l.execute(source if source is not None else (M/'NetworkBridge.lua').read_text())
 l.execute("SPCNetworkBridge.Start(P,shared);net=shared.NetworkBridge;net.ready=true")
 l.execute(r"""
 function total(k) return ExposedMembers.SPC_Performance.entries[k].total end
 function encode(t)
  if type(t)~='table' then return type(t)..':'..tostring(t) end
  local rows={};for k,v in pairs(t) do rows[#rows+1]=encode(k)..'='..encode(v) end
  table.sort(rows);return '{'..table.concat(rows,';')..'}'
 end
 function fullOutput()
  local out={national=net.National(0),cities={}}
  for id,c in pairs(cities) do
   local row={connected=net.ConnectedKinds(0,c),sources={}};out.cities[id]=row
   for _,k in ipairs({'RESEARCH','CULTURE','INDUSTRY'}) do row.sources[k]=net.RecipientSources(0,c,k) end
  end
  return encode(out)
 end
 function discountFixture()
  cities[4]=nil -- exactly four cities, with Industry source #5
  for _,c in pairs(cities) do c.GetBuildings=function() return {} end;c.GetBuildQueue=function() return {} end end
  SPCStandardizationCatalog={Build=function() return {buildings={TEST={enabled=true,group='T1'}}} end}
  P.Info=function(_,id) return {Index=100+tonumber(id:match('(%d+)$'))} end
  P.HasBuilding=function() P.Count('building_check');return false end
  P.CreateBuilding=function() P.Count('building_create');error('unexpected create') end
  P.RemoveBuilding=function() P.Count('building_remove');error('unexpected remove') end
  shared.Standardization={ReadLedger=function() return {learned={}} end}
 end
 """)
 return l
oldA=subprocess.check_output(['git','-C',str(R),'show','d1ac666:Mod/NetworkBridge.lua'],text=True)
old69=subprocess.check_output(['git','-C',str(R),'show','79281ff:Mod/NetworkBridge.lua'],text=True)
# Full values including every National recipient and source, all per-city kinds/source arrays.
a,b,c=runtime(oldA),runtime(old69),runtime()
routes=['','0,1,0,2,10','0,1,0,2,10;0,2,0,3,11',
 '0,1,0,2,10;0,1,0,2,11;0,2,0,3,12',
 '0,1,0,2,10;0,4,0,2,11;0,5,0,2,12;0,2,0,3,13;0,3,0,4,14',
 '0,4,0,1,10;0,5,0,1,11;0,1,0,3,12;0,5,0,2,13;0,2,0,3,14',
 '0,2,0,1,10;0,3,0,2,11']
comparisons=0
for data in routes:
 for l in (a,b,c):l.execute(f"send('{data}',{len(data.split(';')) if data else 0})")
 for level in range(1,5):
  for cap in (1,2,3):
   for center in ('COMMERCE','NONE'):
    cmd=f"cities[1].active={level};cities[4].active={5-level};capitalID={cap};cities[3].kind='{center}';cities[3].potential={4 if center=='COMMERCE' else 0};cities[3].active={1 if center=='COMMERCE' else 0};net.Rebuild()"
    for l in (a,b,c):l.execute(cmd)
    values=[l.eval('fullOutput()') for l in (a,b,c)]
    assert values[0]==values[1]==values[2],(data,level,cap,center)
    comparisons+=1
# A defines transient-read semantics (B069 is intentionally not the unknown-state oracle).
a,c=runtime(oldA),runtime()
steps=["send('0,1,0,2,10;0,4,0,2,11;0,2,0,3,12',3)",
 "cities[1].kind='NONE';cities[1].potential=0;cities[1].active=0;net.Rebuild()",
 "cities[1].kind='RESEARCH';cities[1].potential=4;cities[1].active=4;net.Rebuild()",
 "cities[1].fail=true;net.CheckEvidence(false)",
 "capitalID=3;net.Rebuild()", "cities[1].fail=false;net.Rebuild()",
 "SPCBoostConfig={k={RESEARCH=1.2,CULTURE=1.3}};net.Rebuild()",
 "cities[1].token='REPLACED';net.Rebuild()", "send('',0)"]
for step in steps:
 for l in (a,c):l.execute(step)
 left=a.eval('function() local ok,v=pcall(fullOutput);return ok,ok and v or nil end')()
 right=c.eval('function() local ok,v=pcall(fullOutput);return ok,ok and v or nil end')()
 assert left==right,step
 assert a.eval('encode(net.Input(0))')==c.eval('encode(net.Input(0))'),step
# Actual Discount module, not a surrogate loop. Cold means candidate waiting for first valid facts.
l=runtime();l.execute('discountFixture();readFail=true;send("0,5,0,2,10;0,2,0,3,11",2);readFail=false')
l.execute((M/'StandardizationDiscount.lua').read_text())
l.execute(r"""
SPCStandardizationDiscount.Start(P,shared)
assert(total('derive_executed')==0)
shared.StandardizationDiscount.EnsureReady(0)
assert(total('derive_executed')==1 and total('derived_cache_miss')==1 and total('derived_cache_hit')==4)
local n=total('derive_executed');local hit=total('derived_cache_hit')
shared.StandardizationDiscount.Audit()
assert(total('derive_executed')==n and total('derived_cache_hit')==hit+4)
for i=1,100 do shared.StandardizationDiscount.Audit() end
assert(total('derive_executed')==1 and total('derived_cache_hit')==408)
assert(total('building_create')==0 and total('building_remove')==0 and total('property_write')==0)
-- Public query copies and diagnostic projections cannot mutate the private view.
local baseline=fullOutput();local n=net.National(0);n.RESEARCH.n=999;n.RESEARCH.sources[999]=4
local k=net.ConnectedKinds(0,cities[2]);k.BAD=true
local ids=net.RecipientSources(0,cities[3],'INDUSTRY');ids[1]=999
net.players[0].recipients={};net.players[0].centers={};net.players[0].sources={}
assert(fullOutput()==baseline and total('derive_executed')==1)
-- Key includes config, ACTIVE/Potential, reference, capital and source identity via Batch A.
local inputs=total('input_version_change')
SPCBoostConfig={k={RESEARCH=1.1,CULTURE=1}};net.Rebuild()
assert(total('derive_executed')==2 and total('input_version_change')==inputs+1)
local before=total('derive_executed');local version=net.Input(0).inputVersion
readFail=true;net.CheckEvidence(false);assert(fullOutput()==baseline)
assert(total('derive_executed')==before and net.Input(0).inputVersion==version)
readFail=false;net.Rebuild();assert(total('derive_executed')==before)
-- Confirmed loss drops the view, never returns a fabricated empty National result.
units[10]=nil;net.CheckEvidence(false)
assert(net.Input(0).validity=='CONFIRMED_INVALID' and net.Input(0).derivedFor==nil)
assert(not pcall(net.National,0));assert(total('derive_executed')==before)
units[10]={};send('0,5,0,2,10;0,2,0,3,11',2)
assert(total('derive_executed')==before+1 and fullOutput()==baseline)
-- Publication occurs after installing the cache; reentrant queries see that exact version.
shared.NetworkBoost={Audit=function(m)
 local before=total('derive_executed');fullOutput();assert(total('derive_executed')==before)
 assert(net.Input(0).derivedFor==m.inputVersion)
end}
cities[5].active=4;net.Rebuild()
local epoch=net.epoch;local n=total('derive_executed')
SPCNetworkBridge.Start(P,shared);net=shared.NetworkBridge;net.ready=true
assert(not pcall(net.National,0))
net.Receive(0,{Epoch=epoch,Seq=9999,Turn=turn,Signal=0,Valid=1,Count=0,Data=''})
assert(net.Input(0).inputVersion==0 and total('derive_executed')==n)
send('',0);assert(total('derive_executed')==n+1 and net.Input(0).validity=='VERIFIED')
local n=total('derive_executed');fullOutput();assert(total('derive_executed')==n)
assert(total('derived_invalidation')>0)
""")
# Two players with identical numeric inputVersion cannot share a view; no new gameplay eligibility.
l=runtime();l.execute(r"""
send('',0)
P.IsTestPlayer=function(pid) return pid==0 or pid==1 end
local other={id=1,owner=1,kind='CULTURE',potential=4,active=2,token='OTHER'}
other.GetID=function() return 1 end;other.GetOwner=function() return 1 end
other.GetX=function() return 40 end;other.GetY=function() return 40 end
other.GetProperty=function() return 'OTHER' end
Players[1]={GetCities=function() return {FindID=function(_,id) if id==1 then return other end end,
 Members=function() return pairs({other}) end,GetCapitalCity=function() return other end} end,
 GetTrade=function() return {CountOutgoingRoutes=function() return 0 end} end}
net.Receive(1,{Epoch=net.epoch,Seq=1,Turn=turn,Signal=0,Valid=1,Count=0,Data=''})
assert(net.Input(0).inputVersion==1 and net.Input(1).inputVersion==1)
local before=total('derive_executed')
assert(net.National(0).RESEARCH.level==3 and net.National(0).CULTURE.n==0)
assert(net.National(1).CULTURE.level==2 and net.National(1).RESEARCH.n==0)
assert(net.ConnectedKinds(1,other).CULTURE and not net.ConnectedKinds(0,cities[1]).CULTURE)
assert(total('derive_executed')==before)
-- Refuse mismatched metadata; do not secretly rederive the same version.
local b=net.players[0];local old=b.derivedFor;b.derivedFor=999
assert(not pcall(net.National,0) and total('derive_executed')==before)
b.derivedFor=old;assert(net.National(0).RESEARCH.level==3)
""")
# Warm historical audit: exactly four derives in A and B069, zero in B.
for label,source in [('B069',old69),('Batch A',oldA),('Batch B',None)]:
 l=runtime(source);l.execute('discountFixture();send("0,5,0,2,10;0,2,0,3,11",2)')
 l.execute((M/'StandardizationDiscount.lua').read_text())
 l.execute('SPCStandardizationDiscount.Start(P,shared);shared.StandardizationDiscount.ready=true;before=total("derive");shared.StandardizationDiscount.Audit();delta=total("derive")-before')
 assert l.eval('delta')==(0 if label=='Batch B' else 4)
 print(label,'4-city actual Discount Audit derives:',l.eval('delta'))
print(f'AV2-B LOCAL_SIMULATION_PASS: {comparisons} three-way complete output cases + 9 A/transient metadata cases; cold 1 miss/1 derive/4 hits; warm 0 derive/4 hits; 102 audits total 1 derive/408 hits; mutation isolation, config, withdrawal, reentry, epoch; no engine writes.')
