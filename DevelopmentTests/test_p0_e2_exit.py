"""Targeted L3 E2 exit integration. Explicit read-only gameplay DB argument required.
Runs actual module-owned exits through the actual progression coordinator.
Not native ownership-transfer/persistence certification.
"""
from pathlib import Path
import argparse,sqlite3,runpy,json
ap=argparse.ArgumentParser();ap.add_argument('--db',type=Path,required=True);args=ap.parse_args()
R=Path(__file__).resolve().parents[1];M=R/'Mod'
ns=runpy.run_path(str(R/'DevelopmentTests/test_p0_e2.py'));l=ns['l']
db=sqlite3.connect(args.db.resolve().as_uri()+'?mode=ro',uri=True);db.row_factory=sqlite3.Row
buildings={r['BuildingType']:dict(r) for r in db.execute('select rowid as "Index",* from Buildings')}
byid={r['Index']:r for r in buildings.values()}
def rows(t):return l.table_from([l.table_from(dict(r)) for r in db.execute('select * from "'+t+'"')])
def info(t,k):
 if t=='Buildings':
  r=buildings.get(k) if isinstance(k,str) else byid.get(k)
  return l.table_from(r) if r else None
 raise AssertionError((t,k))
l.globals().include=lambda n:l.execute((M/(n+'.lua')).read_text())
l.globals().dbrows=rows;l.globals().dbinfo=info
l.execute("P.IsTestPlayer=function(pid)return pid==0 end;reset(2);import();SPCP0=P;ExposedMembers={};nativeEvents=Events;nativeGameEvents=GameEvents;Events={};GameEvents={};P.Rows=function(t)return dbrows(t)end;P.Info=function(t,k)return dbinfo(t,k)end;GameInfo={};for _,t in ipairs({'HD_BuildingTiers','HD_DUMMY_BUILDINGS','Eras'})do GameInfo[t]=function()local rows=dbrows(t);local i=0;return function()i=i+1;return rows[i]end end end")
# Capture lists by executing the actual writer closures without applying their effects.
l.execute("callbacks={};local real=shared.CityProgressionStore.RegisterExit;shared.CityProgressionStore.RegisterExit=function(name,fn)callbacks[name]=fn;real(name,fn)end;owned={};local realRemove=shared.CityProgressionStore.RemoveOwned;originalRemove=realRemove;shared.CityProgressionStore.RemoveOwned=function(c,loss,ids)owned[currentModule]=ids end")
modules=['ResearchSupport','IndustrySupport','Lv2Housing','Lv2GPP','Lv3Support','Lv3Effects','CrewProjects','Lv4Percent','ResearchInfrastructure','ResearchCross','ResearchApply','ResearchChair','HalfYieldProbe','CopyYields','PurchaseProbe','StandardizationDiscount','NetworkBoost','GreatWorkProbe','Dialogue','GreatWorkAdjacency','CommerceConvergence']
l.execute((M/'StandardizationCatalog.lua').read_text())
for module in modules:
 l.execute((M/(module+'.lua')).read_text())
 name='SPCGWAdjacency' if module=='GreatWorkAdjacency' else 'SPC'+module
 l.execute(name+'.Start(P,shared)')
 l.globals().currentModule=module
 l.execute("callbacks[currentModule]({GetOwner=function()return 62 end,GetID=function()return 40 end},{origin={owner=0,cityID=7}})")
owned={k:list(v.values()) for k,v in l.globals().owned.items()}
allids=set()
for module,ids in owned.items():
 assert ids and len(ids)==len(set(ids)),module
 for name in ids:
  assert name in buildings and buildings[name]['InternalOnly']==1,(module,name)
 assert not allids.intersection(ids),(module,'overlapping ownership',allids.intersection(ids))
 allids.update(ids)
print('Owned catalog STATIC_CONFIRMED:',len(owned),'modules;',len(allids),'unique exact internal IDs')
# Physical mock state is separate for target/control; all possible owned bits are
# deliberately present to test completeness, including tombstones/manual probes.
l.globals().allids=l.table_from(sorted(allids))
l.execute(r"""
shared.CityProgressionStore.RemoveOwned=originalRemove
present={};control={};removed=0;plotWrites=0
for _,id in ipairs(allids)do local r=P.Info('Buildings',id);present[r.Index]=true;control[r.Index]=true end
local ordinary=P.Info('Buildings','BUILDING_LIBRARY').Index;present[ordinary]=true;control[ordinary]=true
local b={};c.GetBuildings=function()return b end
P.HasBuilding=function(object,id)assert(object==b);return present[id]==true end
P.RemoveBuilding=function(object,id)assert(object==b and id~=ordinary);assert(present[id]);present[id]=nil;removed=removed+1 end
P.CreateBuilding=function()error('EXIT_MUST_NOT_ADD')end
local plotState={SPC_B029_ONE=1,SPC_B029_HALF=1,PERMANENT_OTHER='keep'}
Map={GetPlot=function()return {GetProperty=function(_,k)return plotState[k]end,SetProperty=function(_,k,v)assert(k=='SPC_B029_ONE' or k=='SPC_B029_HALF');plotState[k]=v;plotWrites=plotWrites+1 end}end}
include('YieldCarrierProbe');SPCYieldCarrierProbe.RegisterExit(shared)
include('NetworkBridge');SPCNetworkBridge.Start(P,shared);net=shared.NetworkBridge
-- Populate a stale accepted view projection; its provider must publish invalidation.
net.players[0]={seq=1,revision=1,inputRevision=1,derivedRevision=1,derivedFor=1,validity='VERIFIED',routes={},
 inputSignature='old',input={capital=7,cities={[7]={specialization='RESEARCH',potential=2,active=2}}},sources={[7]='RESEARCH'},recipients={RESEARCH={[8]={[7]=true}}}}
net.players[9]={validity='VERIFIED',sentinel='other player'}
-- Isolate publication observers from unrelated mock engine APIs, but exercise the
-- real withdraw/publish metadata/notifications and never fake its result.
notifications=0
for _,n in ipairs({'Lv3Effects','StandardizationDiscount','NetworkBoost','CommerceConvergence','CopyYields'})do
 shared[n].Audit=function(publication)assert(publication.player==0 and publication.validity=='CONFIRMED_INVALID');notifications=notifications+1 end
end
local before=M.Copy(Game:GetProperty(SPCCityProgressionStore.KEY))
local savedValues=M.Copy(s.values)
local live=CityManager.GetCityAt
-- Unknown object, throwing owner getter, absent owner, and unmatched transfer all preserve effects.
CityManager.GetCityAt=function()return nil end;nativeEvents.CityRemovedFromMap.Fire(0,7)
CityManager.GetCityAt=live
local owner=c.GetOwner;c.GetOwner=function()error('TEMPORARY')end;nativeEvents.CityTransfered.Fire(62,40,0,7)
c.GetOwner=function()return nil end;nativeEvents.CityTransfered.Fire(62,40,0,7);c.GetOwner=owner
s.ref.owner=62;s.ref.cityID=40
nativeEvents.CityAddedToMap.Fire(62,40,4,5);nativeEvents.CityTransfered.Fire(62,999,0,7);nativeEvents.CityTransfered.Fire(62,40,9,7)
assert(removed==0 and plotWrites==0 and Game:GetProperty(SPCCityProgressionStore.KEY).stage=='ACTIVE')
-- Correct native event + matching live target is the sole exit authorization.
nativeEvents.CityTransfered.Fire(62,40,0,7)
assert(d.exitStatus=='WITHDRAWN',d.exitStatus)
for n,err in pairs(d.exitErrors)do error(n..':'..err)end
assert(removed==#allids and plotWrites==2)
assert(present[ordinary] and control[ordinary] and plotState.PERMANENT_OTHER=='keep')
for _,id in ipairs(allids)do local index=P.Info('Buildings',id).Index;assert(not present[index] and control[index])end
local after=Game:GetProperty(SPCCityProgressionStore.KEY)
function encode(v)if type(v)~='table'then return tostring(v)end;local t={};for k,x in pairs(v)do t[#t+1]=tostring(k)..'='..encode(x)end;table.sort(t);return '{'..table.concat(t,';')..'}'end
assert(encode(before.base)==encode(after.base) and encode(before.investment)==encode(after.investment) and encode(before.binding)==encode(after.binding))
assert(encode(s.values)==encode(savedValues),'CITY_PROPERTIES_CHANGED')
assert(after.loss and after.stage=='HELD_TRANSFER' and after.revision==before.revision+1)
assert(net.players[0].validity=='CONFIRMED_INVALID' and net.players[0].sources==nil and net.players[0].recipients==nil and net.players[0].routes==nil)
assert(net.players[9].sentinel=='other player' and net.players[62]==nil and notifications==5)
local n=removed
for i=1,100 do nativeEvents.CityTransfered.Fire(62,40,0,7);nativeEvents.CityInitialized.Fire(62,40)end
assert(removed==n and plotWrites==2 and notifications==5)
-- Direct callback reuse also has zero extra writes; ordinary carrier guard prevents misuse.
for _,name in ipairs({'ResearchApply','ResearchChair','IndustrySupport','StandardizationDiscount'})do callbacks[name](c,after.loss)end
assert(removed==n)
assert(not pcall(d.RemoveOwned,c,after.loss,{'BUILDING_LIBRARY'}))
local other={GetOwner=function()return 62 end,GetID=function()return 41 end,GetX=function()return 6 end,GetY=function()return 5 end}
assert(not pcall(d.RemoveOwned,other,after.loss,{'BUILDING_SPC_DEV_RESEARCH_SUPPORT'}))
-- Reacquisition is deliberately not activation/restoration.
s.ref.owner=0;s.ref.cityID=7;nativeEvents.CityTransfered.Fire(0,7,62,40)
assert(Game:GetProperty(SPCCityProgressionStore.KEY).stage=='HELD_TRANSFER' and not pcall(shared.EffectiveFacts.Read,0,c))
-- With real module return hooks, no old sample survives even a same-turn return.
local infoBefore=P.Info;P.Info=function(t,k)if t=='Districts'then return {DistrictType=k}end;return infoBefore(t,k)end
Players[0].GetDistricts=function()return {Members=function()return ipairs({{GetCity=function()return c end,GetType=function()return s.values.JOURNAL.first.type end,GetID=function()return 99 end,IsComplete=function()return true end}})end}end
shared.CopyYields.samples[0]={old=true};shared.IndustrySupport.samples[0]={old=true};shared.StandardizationDiscount.samples[0]={old=true}
shared.Dialogue.samples[0]={old=true};shared.GreatWorkAdjacency.samples[0]={old=true}
local generation=shared.CopyYields.generation
nativeEvents.CityTransfered.Fire(0,7,62,40)
assert(Game:GetProperty(SPCCityProgressionStore.KEY).stage=='ACTIVE',d.observation)
assert(shared.CopyYields.samples[0]==nil and shared.CopyYields.generation>generation)
assert(shared.IndustrySupport.samples[0]==nil and shared.StandardizationDiscount.samples[0]==nil and shared.Dialogue.samples[0]==nil and shared.GreatWorkAdjacency.samples[0]==nil)
assert(removed==n and plotWrites==2,'RETURN_MUST_NOT_REPLAY_CARRIERS')
s.ref.owner=62;s.ref.cityID=40;nativeEvents.CityTransfered.Fire(62,40,0,7)
assert(d.exitStatus=='WITHDRAWN')
P.Info=infoBefore
print('Exit integration LOCAL_SIMULATION_PASS: confirmed/unknown, all owned IDs, duplicate, ordinary/control/permanent preservation, network source/receiver invalidation, no AI state, unproven recapture held; confirmed return resets actual module samples without writes')
""")
# Reload persisted confirmed loss: repeat only exact target; bounded isolated failures.
l.execute(r"""
s.ref.owner=62;s.ref.cityID=40
Events=nativeEvents;GameEvents=nativeGameEvents
SPCCityProgressionStore.Start(P,shared)
local cold=shared.CityProgressionStore;local fails,success=0,0
cold.RegisterExit('Broken',function()fails=fails+1;error('INJECTED_REMOVE_FAILURE')end)
cold.RegisterExit('Good',function(city,loss)assert(cold.IsExitTarget(city,loss));success=success+1 end)
local get=CityManager.GetCityAt;CityManager.GetCityAt=function()return nil end
cold.ExitConfirmed();assert(fails==0 and success==0)
CityManager.GetCityAt=get
for i=1,10 do cold.ExitConfirmed()end
assert(fails==3 and success==1 and cold.exitStatus=='PARTIAL_HELD')
assert(cold.Describe(0,c):find('Broken',1,true))
assert(Game:GetProperty(SPCCityProgressionStore.KEY).stage=='HELD_TRANSFER')
print('Coldload LOCAL_SIMULATION_PASS: saved confirmation, UNKNOWN hold, isolated failure, bounded 3 attempts, successful module once')
""")
# Source check: exit is explicit registration only, never full Buildings enumeration.
store=(M/'CityProgressionStore.lua').read_text()
assert "P.Rows('Buildings')" not in store and 'BUILDING_SPC_' not in store
for p in M.rglob('*.lua'):l.execute('assert(load(...))',p.read_text())
print('Exit Lua compile PASS')
