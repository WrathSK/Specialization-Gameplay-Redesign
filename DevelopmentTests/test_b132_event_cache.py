"""L2 bounded tests of actual UI handlers, D producer and housing/infra consumers."""
from pathlib import Path
import subprocess,xml.etree.ElementTree as ET
from lupa.lua55 import LuaRuntime
R=Path(__file__).resolve().parents[1];M=R/'Mod'
def fixture(name,stop):
 p=R/'DevelopmentTests'/name;ns={'__file__':str(p)}
 exec(compile(p.read_text().split(stop)[0],str(p),'exec'),ns)
 return ns
b=fixture('test_p0_b2.py','for kind,domain in ')
l=b['runtime']()
l.execute("""
local original=shared.EffectiveFacts.Read
shared.EffectiveFacts.Read=function(pid,c)local f=original(pid,c);f.token=c.token;return f end
setBuildings(d,{'BUILDING_LIBRARY','BUILDING_UNIVERSITY'});audit();noErrors();assert(housing(c)==3)
local cap=counters.dc_capture;local w=writes
for i=1,3 do audit();noErrors();svc.Read(0,c,c.token)end
assert(counters.dc_capture==cap and writes==w and counters.dc_hit>0)
-- Native repair notifications invalidate before the consumer, within same turn.
d.bs[1].pillaged=true;fire('BuildingPillaged');noErrors();assert(housing(c)==2)
d.bs[1].pillaged=false;fire('BuildingRepaired');noErrors();assert(housing(c)==3)
d.pillaged=true;fire('DistrictPillaged');noErrors();assert(housing(c)==0)
d.pillaged=false;fire('DistrictRepaired');noErrors();assert(housing(c)==3)
local w=writes;c.factsError=true;audit();assert(writes==w and shared.Lv2Housing.errors['0:1'])
c.factsError=false;failRead=true;fire('BuildingRepaired');assert(writes==w and shared.Lv2Housing.errors['0:1'])
failRead=false;turn=turn+1;fire('PlayerTurnActivated',0);noErrors();assert(housing(c)==3)
-- Missed event still reconciles next turn; ordinary event adds immediately.
setBuildings(d,{'BUILDING_LIBRARY'});turn=turn+1;fire('PlayerTurnActivated',0);noErrors();assert(housing(c)==2)
setBuildings(d,{'BUILDING_LIBRARY','BUILDING_UNIVERSITY'});fire('BuildingAddedToMap',0,0,GameInfo.Buildings.BUILDING_UNIVERSITY.Index,0);noErrors();assert(housing(c)==3)
-- Reference change can't reuse old city state; load clears cache.
c.token='NEW';setBuildings(d,{'BUILDING_LIBRARY'});audit();noErrors();assert(housing(c)==2)
fire('LoadScreenClose');noErrors();assert(housing(c)==2)
-- Confirmed ineligible owner loses housing/GPP; not a history reset.
c.owner=3;fire('CityTransfered',3,1,0);assert(housing(c)==0 and gpp(c,'RESEARCH')==0 and c.token=='NEW')
""")
# Exact current values against old B131 implementation for representative configurations.
oldsrc=subprocess.check_output(['git','show','ae8acf6:Mod/Lv2Housing.lua'],cwd=R,text=True)
for domain,kind in [('CAMPUS','RESEARCH'),('THEATER','CULTURE'),('INDUSTRIAL_ZONE','INDUSTRY'),('COMMERCIAL_HUB','COMMERCE')]:
 for active in [1,2,4]:
  values=[]
  for old in [False,True]:
   v=b['runtime']()
   if old:
    v.execute(oldsrc);v.execute('SPCLv2Housing.Start(P,shared);shared.Lv2Housing.ready=true')
   v.execute(f"c.identity='{kind}';d.type=GameInfo.Districts.DISTRICT_{domain}.Index;c.active={active};audit();noErrors()")
   values.append((v.eval('housing(c)'),v.eval(f"gpp(c,'{kind}')")))
  assert values[0]==values[1]
print('PASS housing values, shared-token reuse, repair/pillage, unknown hold, next-turn fallback, reference/load and confirmed owner withdrawal')
c=fixture('test_p0_c.py','chains=')
v=c['runtime']();v.execute("""
setBuildings(d,{'BUILDING_LIBRARY','BUILDING_UNIVERSITY'});seedOld();audit();good();retired();assert(coeff(c)==3)
local cap=counters.dc_capture;local w=writes
audit();good();assert(counters.dc_capture==cap and writes==w)
d.bs[1].pillaged=true;fire('BuildingPillaged');good();assert(coeff(c)==2)
d.bs[1].pillaged=false;fire('BuildingRepaired');good();assert(coeff(c)==3)
failRead=true;fire('BuildingRepaired');local w=writes;audit();assert(writes==w and coeff(c)==3)
failRead=false;turn=turn+1;fire('PlayerTurnActivated',0);good();assert(coeff(c)==3)
c.active=3;audit();good();assert(coeff(c)==0)
c.active=4;fire('GovernorChanged',0);good();assert(coeff(c)==3)
""")
print('PASS actual ResearchInfrastructure cache reuse, retired-carrier cleanup, repairs, UNKNOWN and ACTIVE withdrawal')
def ui(source):
 u=LuaRuntime();u.execute("""
include=function()end
turn=20;sent=0;localID=4
Game={GetCurrentGameTurn=function()return turn end,GetLocalPlayer=function()return localID end}
P={VERSION='TEST',IsTestPlayer=function(pid)return pid==localID end,Field=function(t,k)return t[k]end}
SPCP0=P;ExposedMembers={SPC_P0={Version='TEST',Lv2GPP={ready=true}}}
PlayerOperations={EXECUTE_SCRIPT=1}
UI={RequestPlayerOperation=function(pid,op,p)assert(pid==localID);sent=sent+1;last=p end}
function event()local e={fs={}};e.Add=function(f)e.fs[#e.fs+1]=f end;e.Remove=function()end;e.Fire=function(...)for _,f in ipairs(e.fs)do f(...)end end;return e end
Events=setmetatable({},{__index=function(t,k)local e=event();rawset(t,k,e);return e end})
ContextPtr={SetInitHandler=function(self,f)init=f end,SetShutdown=function()end}
""");u.execute(source);u.execute('init();sent=0');return u
u=ui((M/'UI/GPPRefresh.lua').read_text())
u.execute("""
Events.CityFocusChanged.Fire(3);Events.GovernorChanged.Fire(3);Events.PlayerTurnActivated.Fire(3);Events.SystemUpdateUI.Fire();assert(sent==0)
Events.CityWorkerChanged.Fire(4);Events.CityFocusChanged.Fire(4);Events.SystemUpdateUI.Fire();assert(sent==1 and last.FactsChanged==false)
Events.GovernorChanged.Fire(4);Events.GameCoreEventPublishComplete.Fire();assert(sent==2 and last.FactsChanged)
turn=21;Events.PlayerTurnActivated.Fire(3);assert(sent==2);Events.PlayerTurnActivated.Fire(4);assert(sent==3)
Events.PlayerTurnActivated.Fire(4);Events.SystemUpdateUI.Fire();assert(sent==3)
Events.GovernorChanged.Fire(nil);Events.SystemUpdateUI.Fire();assert(sent==4 and last.FactsChanged)
UI.RequestPlayerOperation=function()error('expected failure')end
Events.CityWorkerChanged.Fire(4);Events.SystemUpdateUI.Fire()
UI.RequestPlayerOperation=function()sent=sent+1 end
Events.SystemUpdateUI.Fire();assert(sent==5)
""")
# Same trace in old UI sends unnecessarily, without using player0 assumptions.
old=ui(subprocess.check_output(['git','show','ae8acf6:Mod/UI/GPPRefresh.lua'],cwd=R,text=True))
old.execute("Events.GovernorChanged.Fire(3);Events.SystemUpdateUI.Fire();assert(sent==1)")
# Real Dialogue governor registration; avoid testing unrelated collection mechanics.
d=LuaRuntime();d.execute("""
include=function()end
GameInfo={Eras=function()return function()return nil end end}
Players={[4]={},[3]={}}
P={Field=function(t,k)return t[k]end,IsTestPlayer=function(p)return p==4 end}
callbacks={};Events=setmetatable({},{__index=function(t,k)local e={Add=function(f)callbacks[k]=f end};rawset(t,k,e);return e end})
shared={GreatWorkAdjacency={Audit=function(pid)adj[#adj+1]=pid end}};adj={}
""");d.execute((M/'Dialogue.lua').read_text());d.execute("""
SPCDialogue.Start(P,shared);seen={}
shared.Dialogue.Audit=function(pid)seen[#seen+1]=pid end
callbacks.GovernorChanged(3);assert(#seen==0 and #adj==0)
callbacks.GovernorChanged(4);assert(#seen==1 and seen[1]==4 and #adj==1 and adj[1]==4)
callbacks.GovernorChanged(nil);assert(#seen==3 and #adj==3) -- unknown retains full fallback
""")
# Explicit ownership callbacks themselves remain byte-for-byte unchanged.
for name in ['Lv2Housing','ResearchInfrastructure','DistrictCompleteness','Dialogue']:
 now=(M/(name+'.lua')).read_text();old=subprocess.check_output(['git','show','ae8acf6:Mod/'+name+'.lua'],cwd=R,text=True)
 marker=" if shared.CityProgressionStore then"
 assert now[now.index(marker):]==old[old.index(marker):],name
for name in ['Lv2Housing','ResearchInfrastructure','DistrictCompleteness','Dialogue','Probe','UI/GPPRefresh']:
 d.execute('assert(load(...))',(M/(name+'.lua')).read_text())
assert ET.parse(M/'SpecializationP0.modinfo').getroot().get('version')=='159'
print('PASS foreign/local/unknown UI gating with player4, coalescing/retry/turn; real Dialogue scope; unchanged ownership callbacks; syntax/modinfo159')
