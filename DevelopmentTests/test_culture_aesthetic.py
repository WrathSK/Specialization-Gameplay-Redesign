"""P0-L1 scoped Lua/SQL regression; local projection is not native Tourism proof.
Read-only external DB -> memory; two-city fixture, no game/deployment/stress.
"""
from contextlib import contextmanager
from pathlib import Path
from unittest.mock import patch
import os, sqlite3, subprocess, unittest, zlib, xml.etree.ElementTree as ET
from project_paths import external_database
from lupa.lua55 import LuaRuntime
from test_environment_assembly import prepare_hd_inputs
from retired_crew_sources import B521, B522, package, source as retired_source
R=Path(os.environ.get('SPC_L1_ROOT',Path(__file__).resolve().parents[1]))
M=R/'Mod'

@contextmanager
def cold_build(previous):
    """Run the old cold-clear expectation against its last published Lua sources."""
    if not previous:
        yield
        return
    with package('4502dfc30a219a064ebe629dd9c04c989f852b6a', paths=('Mod/*.lua',)) as old:
        with patch(__name__ + '.M', old / 'Mod'):
            yield

def database():
    ro=sqlite3.connect(external_database(R).as_uri()+'?mode=ro',uri=True)
    d=sqlite3.connect(':memory:');ro.backup(d);ro.close()
    d.create_function('Make_Hash',1,lambda text: zlib.crc32(text.encode()))  # fixture-only hash, not native hash evidence
    # The configured captured database can already include these exact rows.
    carrier='BUILDING_SPC_CULTURE_AESTHETIC'
    for table,col,values in [
     ('BuildingModifiers','BuildingType',[carrier]),('Buildings','BuildingType',[carrier]),('Types','Type',[carrier]),
     ('ModifierArguments','ModifierId',[f'SPC_CULTURE_AESTHETIC_{i}'for i in range(16)]),
     ('Modifiers','ModifierId',[f'SPC_CULTURE_AESTHETIC_{i}'for i in range(16)]),
     ('RequirementArguments','RequirementId',[f'SPC_CULTURE_AESTHETIC_{i}_REQ'for i in range(16)]),
     ('Requirements','RequirementId',[f'SPC_CULTURE_AESTHETIC_{i}_REQ'for i in range(16)]),
     ('RequirementSetRequirements','RequirementSetId',[f'SPC_CULTURE_AESTHETIC_{i}_SET'for i in range(16)]),
     ('RequirementSets','RequirementSetId',[f'SPC_CULTURE_AESTHETIC_{i}_SET'for i in range(16)])]:
     d.executemany(f'DELETE FROM {table} WHERE {col}=?',[(x,)for x in values])
    d.execute('DROP TABLE IF EXISTS SPC_CultureAestheticBits')
    d.executescript((M/'Data/CultureAesthetic.sql').read_text())
    return d

def lua_table(l,v):
    if isinstance(v,dict):return l.table_from({k:lua_table(l,x)for k,x in v.items()})
    if isinstance(v,list):return l.table_from([lua_table(l,x)for x in v])
    return v

FIX=r'''
turn=10;writes=0;counts={};unknown=false;failRemove=nil;failCreate=false
function db(rows,key)
 local t={};for _,r in ipairs(rows)do t[r[key]]=r;if r.Index then t[r.Index]=r end end
 return setmetatable(t,{__call=function()local i=0;return function()i=i+1;return rows[i]end end})
end
function members(rows)return function()local i=0;return function()i=i+1;if rows[i]then return i,rows[i]end end end end
GameInfo={};Events={};GameEvents={};Game={GetCurrentGameTurn=function()return turn end}
local function event(ns,name)
 ns[name]={list={}};ns[name].Add=function(f)table.insert(ns[name].list,f)end
end
for _,ns in ipairs({Events,GameEvents})do
 for _,n in ipairs({'LoadScreenClose','CityBuildingsChanged','BuildingAddedToMap','BuildingRemovedFromMap','BuildingPillaged','BuildingRepaired','DistrictRemovedFromMap','DistrictBuildProgressChanged','DistrictPillaged','DistrictRepaired','GovernorAssigned','GovernorEstablished','GovernorChanged','GovernorPromoted','CityTransfered','CityRemovedFromMap','PlayerTurnActivated','BuildingConstructed','OnDistrictConstructed','OnPillage','CityBuilt'})do event(ns,n)end
end
function fire(n,...)for _,f in ipairs(Events[n] and Events[n].list or {})do f(...)end end
plots={};cities={};ds={};Locale={Lookup=function(v)return v end};ExposedMembers={}
function plot(id)
 local p={index=id,props={},owner=0};function p:GetIndex()return self.index end;function p:GetProperty(k)return self.props[k]end
 function p:SetProperty(k,v)self.props[k]=v;writes=writes+1 end
 function p:GetOwner()return self.owner end;function p:GetWorkerCount()return 0 end
 plots[id]=p;return p
end
Map={GetPlotByIndex=function(i)return plots[i]end,GetPlot=function(x,y)return plots[x]end}
function city(id)
 local c={id=id,owner=0,x=id*100,token='persistent:'..id,identity='CULTURE',potential=4,active=3,ds={},present={},locations={},pillaged={},eras=2}
 function c:GetID()return self.id end;function c:GetOwner()return self.owner end;function c:GetX()return self.x end;function c:GetY()return 0 end
 function c:GetPopulation()return 7 end;function c:GetProperty(k)if k=='SPC_DEV_BINDING_B013_TOKEN'then return self.token end end
 function c:SetProperty()error('CITY_PERMANENT_WRITE_FORBIDDEN')end
 function c:GetDistricts()return {GetNumDistricts=function()counts.ds=(counts.ds or 0)+1;return #c.ds end,GetDistrictByIndex=function(_,i)return c.ds[i+1]end}end
 function c:GetBuildings()return {
 HasBuilding=function(_,id)if unknown and id==999999 then return nil end;return c.present[id]==true end,
 GetBuildingLocation=function(_,id)return c.locations[id] or -1 end,
 IsPillaged=function(_,id)return c.pillaged[id]==true end,
 city=c}end
 function c:GetBuildQueue()return {city=c,CurrentlyBuilding=function()return nil end}end
 cities[#cities+1]=c;return c
end
function district(c,id,kind)
 local d={id=id,type=GameInfo.Districts[kind].Index,x=c.x+id,pillaged=false,complete=true,city=c}
 function d:GetID()return self.id end;function d:GetType()return self.type end;function d:GetX()return self.x end;function d:GetY()return 0 end
 function d:IsComplete()return self.complete end;function d:IsPillaged()return self.pillaged end;function d:GetCity()return self.city end
 plot(d.x);c.ds[#c.ds+1]=d;ds[#ds+1]=d;return d
end
function building(c,kind,d,yes)
 local id=GameInfo.Buildings[kind].Index;c.present[id]=yes~=false;c.locations[id]=d.x;c.pillaged[id]=false
end
P={VERSION='P0-B-149.176',IsTestPlayer=function(pid)return pid==0,nil,pid==0 and 'ELIGIBLE' or 'INELIGIBLE' end,Field=function(t,k)return t and t[k]end,
 Count=function(k)counts[k]=(counts[k] or 0)+1 end}
function P.Info(name,k)return GameInfo[name] and GameInfo[name][k]end
function P.Rows(name)local out={};for row in GameInfo[name]()do out[#out+1]=row end;return out end
function P.HasBuilding(b,id)if id==failHas then return nil end;return b.city.present[id]==true end
function P.CreateBuilding(q,id)
 if failCreate then return end
 local at=q.city.ds[1]
 local prereq=GameInfo.Buildings[id].PrereqDistrict
 for _,d in ipairs(q.city.ds)do if GameInfo.Districts[d.type].DistrictType==prereq then at=d;break end end
 q.city.present[id]=true;q.city.locations[id]=at.x;q.city.pillaged[id]=false;writes=writes+1
 fire('BuildingAddedToMap',q.city.ds[1].x,0,id,q.city.owner)
end
function P.RemoveBuilding(b,id)
 if failRemove==id then return end
 b.city.present[id]=nil;b.city.locations[id]=nil;writes=writes+1
 fire('BuildingRemovedFromMap',b.city.ds[1].x,0,id,b.city.owner)
end
function P.SetProperty(o,k,v)o:SetProperty(k,v)end
CityManager={GetCityAt=function(x,y)for _,c in ipairs(cities)do if c.x==x then return c end end end,
 GetDistrictAt=function(x,y)for _,d in ipairs(ds)do if d.x==x then return d end end end}
Players={[0]={GetCities=function()return {Members=members(cities),FindID=function(_,id)for _,c in ipairs(cities)do if c.id==id and c.owner==0 then return c end end end}end,
 GetDistricts=function()return {Members=members(ds)}end}}
exits={};returns={}
shared={EffectiveFacts=(function(t)local function fresh(_,r)return r()end;t.WithPhase=t.WithPhase or function(_,fn,...)return fn(...)end;t.Inspect=t.Inspect or function(pid,c,project)return project(t.Read(pid,c),fresh,fresh)end;t.NewReader=t.NewReader or function()return function(pid,c,project)if project then return t.Inspect(pid,c,project)end;return t.Read(pid,c)end end;t.DistrictWriteVersion=t.DistrictWriteVersion or function()local v=t.Version and t.Version()or nil;return v,v,false end;return t end){Read=function(pid,c)
 if c.factsUnknown then error('TEMPORARY_FACT_UNKNOWN')end
 return {specialization=c.identity,potential=c.potential,active=c.active,activeStatus=c.active and 'KNOWN' or 'UNKNOWN_GOVERNOR',token=c.token,first=c.first or {districtID=c.ds[3] and c.ds[3].id,type='DISTRICT_COMMERCIAL_HUB'}}
end},GreatWorkFacts={Summary=function(pid,id)
 local c=Players[pid]:GetCities():FindID(id)
 return c and {eraCount=c.eras,availability=c.worksUnknown and 'UNKNOWN' or 'KNOWN',hasConfirmed=not c.neverConfirmed,reference=SPCNetworkInput.Reference(c)}
end,Read=function(pid,id)return {eras={ERA_CLASSICAL=1,ERA_MEDIEVAL=1}}end},NetworkBridge={ConnectedKinds=function()return {RESEARCH=true,CULTURE=true}end},
 CityProgressionStore=(function(t)t.ReferenceToken=t.ReferenceToken or function(c)return c.GetProperty and c:GetProperty([[SPC_DEV_BINDING_B013_TOKEN]])or nil end;t.ExitCompleted=t.ExitCompleted or function()return true end;return t end){RegisterExit=function(n,f)assert(not exits[n]);exits[n]=f end,RegisterReturn=function(n,f)assert(not returns[n]);returns[n]=f end,
 IsExitTarget=function(c,loss)return loss.confirmed==true and c.id==loss.targetID and c.owner~=loss.origin.owner end}}
-- Fixture-only direct notification adapter for older single-consumer model cases.
-- Production delivery/isolation is tested with the real GreatWorkFacts receiver.
fixtureConsumers={}
function shared.GreatWorkFacts.RegisterConsumer(name,callback)
 for _,s in ipairs(fixtureConsumers)do assert(s.name~=name)end
 fixtureConsumers[#fixtureConsumers+1]={name=name,callback=callback}
end
function shared.GreatWorkFacts.OnConfirmed(pid,ids)
 for _,s in ipairs(fixtureConsumers)do s.callback(pid,ids)end
end
function shared.CityProgressionStore.RemoveOwned(c,loss,names)
 assert(shared.CityProgressionStore.IsExitTarget(c,loss))
 for _,name in ipairs(names)do local id=GameInfo.Buildings[name].Index;if P.HasBuilding(c:GetBuildings(),id)then P.RemoveBuilding(c:GetBuildings(),id)end end
end
'''

class AestheticTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.sql=database()
 def runtime(self,ready=True,*,historical=None,runtime_type=None):
  prepare_hd_inputs(self.sql)
  l=(runtime_type or LuaRuntime)(unpack_returned_tuples=True);l.execute(FIX)
  def include(n):
   name=n+'.lua'
   l.execute(retired_source(name,historical) if historical else (M/name).read_text())
  l.globals().include=include
  defs=['Buildings','Districts','DistrictReplaces','BuildingReplaces','HD_BuildingTiers','HD_DUMMY_BUILDINGS','Modifiers','Building_CitizenYieldChanges',
   'BuildingPrereqs','SPC_EnvironmentAssembly','SPC_EnvironmentBuildings','SPC_EnvironmentExcludedBuildings']
  keys=['BuildingType','DistrictType','CivUniqueDistrictType','CivUniqueBuildingType','BuildingType','BuildingType','ModifierId','BuildingType',
   'Building','Id','BuildingType','BuildingType']
  for name,key in zip(defs,keys):
   cur=self.sql.execute('SELECT * FROM '+name);names=[x[0]for x in cur.description];rows=[dict(zip(names,r))for r in cur]
   if name in ['Buildings','Districts']:
    for i,r in enumerate(rows):r['Index']=i+1
   l.globals().GameInfo[name]=l.globals().db(lua_table(l,rows),key)
  for name in ['OrdinaryBuildingCatalog','DistrictCompleteness','CurrentSpecializationFacts']:
   include(name)
  old_lv3=bool(historical) or (M/'Lv3Effects.lua').is_file()
  old_lv4=bool(historical) or (M/'Lv4Percent.lua').is_file()
  include('Lv3Effects' if old_lv3 else 'LegacyCleanup')
  if old_lv4:include('Lv4Percent')
  include('CultureAesthetic')
  l.execute('''a=city(1);b=city(2)
   for _,c in ipairs(cities)do
    district(c,1,'DISTRICT_CITY_CENTER');district(c,2,'DISTRICT_THEATER');district(c,3,'DISTRICT_COMMERCIAL_HUB');district(c,4,'DISTRICT_NEIGHBORHOOD');district(c,5,'DISTRICT_NEIGHBORHOOD')
    building(c,'BUILDING_MONUMENT',c.ds[1]);building(c,'BUILDING_WALLS',c.ds[1]);building(c,'BUILDING_PALACE',c.ds[1]);building(c,'BUILDING_AMPHITHEATER',c.ds[2]);building(c,'BUILDING_MARKET',c.ds[3]);building(c,'BUILDING_HD_VILLA',c.ds[4]);building(c,'BUILDING_HD_BUS_STOP',c.ds[5])
   end
   SPCDistrictCompleteness.Start(P,shared)
   local legacy3,legacy4=...
   if legacy3 then SPCLv3Effects.Start(P,shared)
   else
    shared.LegacyCleanup={RegisterRunner=function(name,runner)
     assert(name=='Lv3Effects' and type(runner)=='function')
    end}
    SPCLegacyCleanup.StartLv3Effects(P,shared)
   end
   if legacy4 then SPCLv4Percent.Start(P,shared)end
   SPCCultureAesthetic.Start(P,shared)
   data=shared.CultureAesthetic;svc=shared.DistrictCompleteness
   function audit()data.Audit({player=0})end
   function one()data.Audit({player=0,city=1})end
   function amount(c,plot)
    if not c.present[GameInfo.Buildings.BUILDING_SPC_CULTURE_AESTHETIC.Index]then return 0 end
    local n=0;for bit=0,15 do if plots[plot].props['SPC_CULTURE_AESTHETIC_'..bit]==1 then n=n+2^bit end end;return n
   end
   function total(c)local n=0;for _,d in ipairs(c.ds)do n=n+amount(c,d.x)end;return n end
  ''',old_lv3,old_lv4)
  if ready:l.execute("fire('LoadScreenClose')")
  return l
 def test_formula_and_two_cities(self):
  l=self.runtime()
  for active in [1,2,3,4]:
   for x in [0,1,2,4,8]:
    l.execute(f'a.active={active};a.eras={x};b.eras=1;audit();assert(total(a)=={6*x if active>=3 else 0});assert(total(b)==6);assert(not data.errors["0:1"])')
    l.execute('local w=writes;one();assert(writes==w)')
  l.execute('a.active=3;a.eras=2;one();assert(amount(a,a.ds[1].x)==4 and amount(a,a.ds[4].x)==2 and amount(a,a.ds[5].x)==2)')
  # Independent SQL decoding of the exact projection; collection is local city.
  for row in self.sql.execute("SELECT ModifierId,ModifierType,SubjectRequirementSetId FROM Modifiers WHERE ModifierId LIKE 'SPC_CULTURE_AESTHETIC_%'"):
   mid,typ,rs=row;self.assertEqual(typ,'MODIFIER_CITY_DISTRICTS_ADJUST_TOURISM_CHANGE')
   args=dict(self.sql.execute('SELECT Name,Value FROM ModifierArguments WHERE ModifierId=?',(mid,)))
   req=self.sql.execute('SELECT RequirementId FROM RequirementSetRequirements WHERE RequirementSetId=?',(rs,)).fetchone()[0]
   self.assertEqual(self.sql.execute('SELECT RequirementType FROM Requirements WHERE RequirementId=?',(req,)).fetchone()[0],'REQUIREMENT_PLOT_PROPERTY_MATCHES')
   q=dict(self.sql.execute('SELECT Name,Value FROM RequirementArguments WHERE RequirementId=?',(req,)))
   bit=int(mid.rsplit('_',1)[1]);self.assertEqual(int(args['Amount']),2**bit);self.assertEqual(q['PropertyName'],f'SPC_CULTURE_AESTHETIC_{bit}')
   self.assertEqual(int(q['PropertyMinimum']),1)
 def test_current_buildings_and_d_separation(self):
  l=self.runtime();l.execute("audit();a.pillaged[GameInfo.Buildings.BUILDING_WALLS.Index]=true;svc.MarkDirty(0,1);one();assert(total(a)==10);a.ds[2].pillaged=true;svc.MarkDirty(0,1);one();assert(total(a)==8);a.ds[2].pillaged=false;building(a,'BUILDING_HD_TABLES_OF_LAW',a.ds[1]);svc.MarkDirty(0,1);one();assert(total(a)==12)")
  l.execute("a.pillaged[GameInfo.Buildings.BUILDING_WALLS.Index]=false;building(a,'BUILDING_MONUMENT',a.ds[1],false);svc.MarkDirty(0,1);one();assert(total(a)==12);local p=SPCCultureAestheticModel.Plan(SPCCurrentSpecializationFacts.Read(P,shared,0,a),shared.GreatWorkFacts.Summary(0,1),svc.Read(0,a,a.token),true);assert(p.count==6 and p.rows[1]);assert(data.Describe(0,a,true,1):find('宫殿'))")
  # Every old depth-catalog definition and domain remains semantically identical.
  include=l.globals().include
  old=subprocess.check_output(['git','show','caa5ec3:Mod/OrdinaryBuildingCatalog.lua'],cwd=R,text=True)
  l.execute('currentCatalog=SPCOrdinaryBuildingCatalog.Build(P)');l.execute(old);l.execute('oldCatalog=SPCOrdinaryBuildingCatalog.Build(P)')
  l.execute("for _,b in pairs(oldCatalog.buildings)do if b.ordinary then local n=currentCatalog.buildings[b.type];assert(n.ordinary and n.tier==b.tier and n.domain==b.domain,b.type)end end;assert(currentCatalog.Domain('DISTRICT_CITY_CENTER')==nil and currentCatalog.buildings.BUILDING_WALLS.ordinary and currentCatalog.buildings.BUILDING_WALLS.tier==nil)")
 def test_unknown_reference_load_and_gate(self):
  for previous in (True,False):
   with self.subTest(previous=previous),cold_build(previous):
    l=self.runtime();l.execute('audit();local w=writes;a.worksUnknown=true;one();assert(writes==w and total(a)==12);a.worksUnknown=false;a.active=nil;one();assert(writes==w);a.active=3;a.factsUnknown=true;one();assert(writes==w);a.factsUnknown=false;a.eras=1;one();assert(total(a)==6);a.active=2;one();assert(total(a)==0);a.active=3;one();assert(total(a)==6)')
    l.globals().atLoad=0 if previous else 6
    l.execute("a.worksUnknown=true;fire('LoadScreenClose');assert(total(a)==atLoad and total(b)==12);a.worksUnknown=false;shared.GreatWorkFacts.OnConfirmed(0,{1});assert(total(a)==6);local w=writes;shared.GreatWorkFacts.OnConfirmed(0,{1});assert(writes==w);a.token='different';a.worksUnknown=true;one();assert(total(a)==0)")
 def test_confirmed_loss_recapture_only_current(self):
  l=self.runtime();l.execute("audit();local keep=total(b);local before=writes;local no={origin={owner=0},targetID=1,confirmed=false};assert(not pcall(exits.CultureAesthetic,a,no));assert(writes==before);a.owner=3;local loss={origin={owner=0},targetID=1,confirmed=true};exits.CultureAesthetic(a,loss);assert(total(a)==0 and total(b)==keep);local w=writes;exits.CultureAesthetic(a,loss);assert(writes==w);a.owner=0;a.active=1;returns.CultureAesthetic(0,a);assert(total(a)==0);a.active=3;a.eras=1;returns.CultureAesthetic(0,a);assert(total(a)==6)")
 def test_legacy_exact_cutover_and_commerce(self):
  l=self.runtime(historical=B521);l.execute("for bit=0,7 do building(a,'BUILDING_SPC_DEV_LV3_POP_CULTURE_'..bit,a.ds[1]);building(a,'BUILDING_SPC_LV4_PERCENT_CULTURE_'..bit,a.ds[1])end;b.identity='COMMERCE';audit();for bit=0,7 do assert(not a.present[GameInfo.Buildings['BUILDING_SPC_DEV_LV3_POP_CULTURE_'..bit].Index] and not a.present[GameInfo.Buildings['BUILDING_SPC_LV4_PERCENT_CULTURE_'..bit].Index])end;shared.Lv3Effects.ready=true;shared.Lv3Effects.Audit({player=0});assert(b.present[GameInfo.Buildings.BUILDING_SPC_DEV_LV3_COM_RESEARCH.Index] and b.present[GameInfo.Buildings.BUILDING_SPC_DEV_LV3_COM_CULTURE.Index]);assert(a.present[GameInfo.Buildings.BUILDING_MONUMENT.Index] and a.token=='persistent:1')")
  for file in ['Lv3Effects.sql','Lv4Percent.sql']:
   src=(M/'Data'/file).read_text()
   for line in src.splitlines():
    if line.startswith(('INSERT INTO Modifiers','INSERT INTO BuildingModifiers','INSERT INTO ModifierArguments')):
     self.assertNotIn('SPC_LV3_POP_CULTURE_',line);self.assertNotIn('SPC_LV4_PERCENT_CULTURE_',line)
 def test_inactive_city_still_clears_exact_legacy(self):
  l=self.runtime();l.execute("a.active=2;building(a,'BUILDING_SPC_DEV_LV3_POP_CULTURE_0',a.ds[1]);building(a,'BUILDING_SPC_LV4_PERCENT_CULTURE_0',a.ds[1]);one();assert(not a.present[GameInfo.Buildings.BUILDING_SPC_DEV_LV3_POP_CULTURE_0.Index] and not a.present[GameInfo.Buildings.BUILDING_SPC_LV4_PERCENT_CULTURE_0.Index] and total(a)==0);local w=writes;one();assert(writes==w)")
 def test_failures_do_not_create_mixed_effect(self):
  l=self.runtime();l.execute("audit();a.eras=3;failCreate=true;one();assert(total(a)==0 and data.errors['0:1']);failCreate=false;one();assert(total(a)==18);local w=writes;a.eras=65536;one();assert(writes==w and total(a)==18 and data.errors['0:1']:find('AE_ENCODING_RANGE'));a.eras=2;one();assert(total(a)==12)")
 def test_same_turn_change_idle_and_cleanup(self):
  l=self.runtime();l.execute("audit();local w=writes;local dsreads=counts.ds;for i=1,20 do one()end;assert(writes==w);a.eras=1;shared.GreatWorkFacts.OnConfirmed(0,{1});assert(total(a)==6);a.eras=2;shared.GreatWorkFacts.OnConfirmed(0,{1});assert(total(a)==12);local w=writes;fire('PlayerTurnActivated',0);local count=counts.city_scan;fire('PlayerTurnActivated',0);assert(counts.city_scan==count and writes==w)")
  l.execute("local removed=a.ds[5];table.remove(a.ds,5);building(a,'BUILDING_HD_BUS_STOP',removed,false);svc.MarkDirty(0,1);one();assert(plots[removed.x].props.SPC_CULTURE_AESTHETIC_0==0 and plots[removed.x].props.SPC_CULTURE_AESTHETIC_1==0 and total(a)==10)")
 def test_real_fact_notification_and_light_summary(self):
  import sys
  sys.path.insert(0,str(R/'DevelopmentTests'))
  from test_p0_k import Fixture
  fx=Fixture()
  fx.check("notifies={};shared.GreatWorkFacts.RegisterConsumer('Fixture',function(pid,ids)notifies[#notifies+1]=ids end);assert(receive(1,sampleRows()));assert(#notifies==1 and #notifies[1]==3);local s=shared.GreatWorkFacts.Summary(0,7);assert(s.eraCount==2 and s.works==nil and s.excluded==nil and s.eras==nil);assert(receive(2,sampleRows()));assert(#notifies==1)")
  fx.check("local rows=sampleRows();table.remove(rows,2);assert(receive(3,rows));assert(#notifies==1);rows[2][1]=8;assert(receive(4,rows));assert(#notifies==2 and #notifies[2]==2 and notifies[2][1]==7 and notifies[2][2]==8)")
 def test_current_eligibility_exclusions_and_d_regression(self):
  l=self.runtime();l.execute("catalog=SPCOrdinaryBuildingCatalog.Build(P);local raw={districts={{id=1,type='DISTRICT_CITY_CENTER',plot=101,complete=true,pillaged=false,buildings={}}}};local d=raw.districts[1];for _,kind in ipairs({'BUILDING_MONUMENT','BUILDING_WALLS','BUILDING_PALACE','BUILDING_SPC_CULTURE_AESTHETIC'})do d.buildings[#d.buildings+1]={index=GameInfo.Buildings[kind].Index,complete=true,pillaged=false}end;local v=SPCDistrictCompleteness.Calculate(catalog,raw);assert(v.districts[1].value==0);local p=SPCCultureAestheticModel.Plan({validity='VERIFIED',identity='CULTURE',potential=3,active=3,activeStatus='KNOWN'},{hasConfirmed=true,availability='KNOWN',eraCount=2},{validity='VERIFIED',availability='READY',value=v},true);assert(p.count==2 and p.total==4);d.buildings[1].complete=false;v=SPCDistrictCompleteness.Calculate(catalog,raw);p=SPCCultureAestheticModel.Plan({validity='VERIFIED',identity='CULTURE',potential=3,active=3,activeStatus='KNOWN'},{hasConfirmed=true,availability='KNOWN',eraCount=2},{validity='VERIFIED',availability='READY',value=v},true);assert(p.count==1)")
  old=subprocess.check_output(['git','show','caa5ec3:Mod/OrdinaryBuildingCatalog.lua'],cwd=R,text=True)
  l.execute('currentCatalog=SPCOrdinaryBuildingCatalog.Build(P)');l.execute(old);l.execute('oldCatalog=SPCOrdinaryBuildingCatalog.Build(P)')
  l.execute("raw={districts={}};local by={};for index,b in pairs(oldCatalog.buildings)do if type(index)=='number' and b.ordinary then local d=by[b.domain];if not d then d={id=#raw.districts+1,type=b.domain,plot=#raw.districts+1,complete=true,pillaged=false,buildings={}};raw.districts[#raw.districts+1]=d;by[b.domain]=d end;d.buildings[#d.buildings+1]={index=index,complete=true,pillaged=false}end end;local a=SPCDistrictCompleteness.Calculate(currentCatalog,raw);local b=SPCDistrictCompleteness.Calculate(oldCatalog,raw);for domain,v in pairs(a.domains)do assert(v.value==b.domains[domain].value and v.districtID==b.domains[domain].districtID,domain)end;for i,d in ipairs(a.districts)do assert(d.value==b.districts[i].value and d.uncapped==b.districts[i].uncapped);d.pillaged=true end")
 def test_research_apply_new_ordinary_separation(self):
  # The real load event populated the shared cache; mirror the new building notification.
  l=self.runtime();l.globals().include('ResearchApply')
  l.execute("a.identity='RESEARCH';a.active=3;local campus=district(a,6,'DISTRICT_CAMPUS');building(a,'BUILDING_LIBRARY',campus);svc.MarkDirty(0,1);a.first={districtID=6,type='DISTRICT_CAMPUS'};plots[campus.x].GetWorkerCount=function()return 2 end;SPCResearchApply.Start(P,shared);ap=shared.ResearchApply;ap.ready=true;ap.Audit({player=0});assert(not ap.definitionError and not ap.errors[0][1],ap.errors[0][1]);assert(a.present[GameInfo.Buildings.BUILDING_SPC_RESEARCH_APPLY_GOLD_0.Index]);local w=writes;ap.Audit({player=0});assert(writes==w)")
  # New ordinary identity is not approved depth; real missing depth still HOLDs.
  l.execute("local read=svc.Read;svc.Read=function(...)local v=read(...);for _,d in ipairs(v.value.districts)do for _,b in ipairs(d.buildings)do if b.type=='BUILDING_LIBRARY'then b.tier=nil end end end;return v end;local w=writes;ap.Audit({player=0});assert(ap.errors[0][1]:find('AP_BUILDING_FACT_UNKNOWN') and writes==w);svc.Read=read")
 def test_failed_legacy_withdrawal_and_bounded_errors(self):
  l=self.runtime();l.execute("audit();local legacy=GameInfo.Buildings.BUILDING_SPC_LV4_PERCENT_CULTURE_0.Index;building(a,'BUILDING_SPC_LV4_PERCENT_CULTURE_0',a.ds[1]);failRemove=legacy;one();assert(total(a)==0 and data.errors['0:1']:find('AE_LEGACY_WITHDRAWAL_UNKNOWN'));failRemove=nil;one();assert(total(a)==12)")
  l.execute("data.errors['0:999']='UNKNOWN';audit();assert(data.errors['0:999']==nil);local before=counts.dc_read or 0;one();assert(counts.dc_read==before+1)")
 def test_missed_load_confirmed_sample_starts_without_panel(self):
  l=self.runtime(ready=False)
  l.execute("assert(not data.ready and total(a)==0 and total(b)==0);local w=writes;assert(data.Describe(0,a):find('等待启动'));assert(not data.ready and writes==w);shared.GreatWorkFacts.OnConfirmed(0,{1});assert(data.ready and data.readyReason=='CONFIRMED_WORKS');assert(total(a)==12 and total(b)==12);local w=writes;shared.GreatWorkFacts.OnConfirmed(0,{1});assert(writes==w)")
 def test_first_local_turn_unknown_and_same_turn_governor(self):
  l=self.runtime(ready=False)
  l.execute("a.worksUnknown=true;fire('PlayerTurnActivated',3);assert(not data.ready and writes==0);fire('PlayerTurnActivated',0);assert(data.readyReason=='LOCAL_TURN');assert(total(a)==0 and total(b)==12 and data.errors['0:1']:find('AE_WORKS_UNKNOWN'));local w=writes;local visits=counts.city_scan;fire('PlayerTurnActivated',0);assert(writes==w and counts.city_scan==visits);a.worksUnknown=false;fire('GovernorChanged',0);assert(total(a)==12);a.active=2;fire('GovernorAssigned',0);assert(total(a)==0 and total(b)==12);a.active=3;fire('GovernorEstablished',0);assert(total(a)==12 and total(b)==12);local w=writes;fire('GovernorEstablished',0);assert(writes==w)")
 def test_unknown_or_stale_notification_does_not_open_ready(self):
  l=self.runtime(ready=False)
  l.execute("a.worksUnknown=true;b.worksUnknown=true;shared.GreatWorkFacts.OnConfirmed(0,{1,2});assert(not data.ready and writes==0);a.worksUnknown=false;shared.GreatWorkFacts.OnConfirmed(3,{1});assert(not data.ready and writes==0);local summary=shared.GreatWorkFacts.Summary;shared.GreatWorkFacts.Summary=function(...)local w=summary(...);if w then w.reference='stale' end;return w end;shared.GreatWorkFacts.OnConfirmed(0,{1});assert(not data.ready and writes==0);shared.GreatWorkFacts.Summary=summary;shared.GreatWorkFacts.OnConfirmed(0,{1});assert(total(a)==12 and total(b)==0 and data.errors['0:2'])")
 def test_diagnostic_separates_raw_master_and_expected_without_writes(self):
  l=self.runtime()
  l.execute("local w=writes;assert(data.Describe(0,a):find('配置已进入'));assert(writes==w);local id=GameInfo.Buildings.BUILDING_SPC_CULTURE_AESTHETIC.Index;a.present[id]=nil;local t=data.Describe(0,a);assert(t:find('配置待核对') and t:find('载体：未建立') and t:find('标记 %+ 12'));assert(writes==w);one();assert(total(a)==12);a.pillaged[id]=true;local w=writes;local t=data.Describe(0,a);assert(t:find('配置待核对') and t:find('载体：不可用') and t:find('标记 %+ 12'));assert(writes==w);a.pillaged[id]=false;plots[a.ds[1].x].props.SPC_CULTURE_AESTHETIC_0=1;plots[a.ds[3].x].props.SPC_CULTURE_AESTHETIC_0=1;plots[a.ds[3].x].props.SPC_CULTURE_AESTHETIC_1=0;local t=data.Describe(0,a);assert(t:find('配置待核对') and not t:find('与预期一致'));assert(writes==w)")
 def test_transferred_worker_percent_keeps_cold_and_failure_readback_order(self):
  from refactor_harness import TrackedLua51
  results=[]
  for historical_lv4 in (True,False):
   l=self.runtime(ready=False,historical=B521 if historical_lv4 else None,runtime_type=TrackedLua51)
   l.execute("""
    local lv3='BUILDING_SPC_DEV_LV3_POP_CULTURE_0'
    local lv4='BUILDING_SPC_LV4_PERCENT_CULTURE_'
    local uncertain=GameInfo.Buildings[lv4..7].Index
    local blocked=GameInfo.Buildings[lv4..1].Index
    local other=GameInfo.Buildings.BUILDING_SPC_LV4_PERCENT_RESEARCH_0.Index
    building(a,lv3,a.ds[1]);building(a,lv4..0,a.ds[1]);building(a,lv4..1,a.ds[1])
    building(a,'BUILDING_SPC_LV4_PERCENT_RESEARCH_0',a.ds[1])
    local trace={};local remove,create=P.RemoveBuilding,P.CreateBuilding
    P.RemoveBuilding=function(b,id)trace[#trace+1]='R:'..b.city.id..':'..id;remove(b,id)end
    P.CreateBuilding=function(q,id)trace[#trace+1]='C:'..q.city.id..':'..id;create(q,id)end
    local has,unavailable=P.HasBuilding,true
    P.HasBuilding=function(b,id)
     if unavailable and b.city==a and id==uncertain then return nil end
     return has(b,id)
    end
    fire('LoadScreenClose')
    assert(total(a)==0 and total(b)==12 and a.present[blocked] and data.errors['0:1']:find('AE_LEGACY_WITHDRAWAL_UNKNOWN'))
    assert(a.present[GameInfo.Buildings[lv4..0].Index])
    unavailable=false;failRemove=blocked;one()
    assert(total(a)==0 and a.present[blocked] and data.errors['0:1'])
    failRemove=nil;one()
    assert(total(a)==12 and total(b)==12 and not a.present[blocked] and a.present[other])
    assert(not data.errors['0:1'] and not a.present[GameInfo.Buildings[lv3].Index])
    local w=writes;one();assert(writes==w)
    withdrawalTrace=table.concat(trace,',')
   """)
   results.append(l.eval('withdrawalTrace'))
  self.assertEqual(*results)
 def test_worker_percent_read_route_keeps_payload_and_is_read_only(self):
  from refactor_harness import TrackedLua51
  gameplay=(M/'Gameplay.lua').read_text()
  fragment=gameplay.split('  if params.Action=="LV4_PERCENT_READ" then',1)[1].split('  if params.Action=="UNIT_ACTION_VIEW" then',1)[0]
  old=retired_source('Gameplay.lua',B521).split('  if params.Action=="LV4_PERCENT_READ" then',1)[1].split('  if params.Action=="UNIT_ACTION_VIEW" then',1)[0]
  def run(body,legacy):
   l=self.runtime(historical=B521 if legacy else None,runtime_type=TrackedLua51)
   l.execute('function read(playerID,params) if params.Action=="LV4_PERCENT_READ" then'+body+'end')
   l.execute("""
    local w=writes
    local request={Action='LV4_PERCENT_READ',Token='READ',CityID=1}
    read(0,request);assert(shared.LastToken=='READ' and shared.Snapshot==data.Describe(0,a))
    report=shared.Snapshot
    request.Token='BAD';read(3,request);assert(shared.LastToken=='READ' and shared.Snapshot==report)
    request.CityID=999;read(0,request);assert(shared.LastToken=='READ' and shared.Snapshot==report)
    shared.CultureAesthetic=nil;request.CityID=1;read(0,request)
    assert(shared.LastToken=='BAD' and shared.Snapshot=='旧文化专家百分比已退休；新能力等待确认。')
    assert(writes==w)
   """)
   return l.eval('report')
  self.assertEqual(run(old,True),run(fragment,False))
 def test_exact_worker_percent_package_retirement_and_rollback(self):
  from retired_crew_sources import package
  from test_o7_crew_retirement import verify_package_round_trip, verify_stable_round_trip
  removed=('Lv4Percent.lua',)
  with package(B521) as before, package(B522) as after:
   for name in ('LegacyCleanup.lua','LegacyCleanupCatalog.lua','Data/Lv4Percent.sql','Data/CultureAesthetic.sql','CultureAestheticModel.lua'):
    self.assertEqual((before/'Mod'/name).read_bytes(),(after/'Mod'/name).read_bytes(),name)
   verify_package_round_trip(self,before/'Mod',after/'Mod',removed,'CultureAesthetic.lua')
   verify_stable_round_trip(self,before/'Mod',after/'Mod',removed)
 def test_registration_and_ui(self):
  root=ET.parse(M/'SpecializationP0.modinfo').getroot();self.assertEqual(root.get('version'),'176')
  files={e.text for e in root.find('Files')};self.assertTrue({'CultureAestheticModel.lua','CultureAesthetic.lua','Data/CultureAesthetic.sql'}<=files)
  xml=ET.parse(M/'UI/P0Panel.xml').getroot();button=xml.find('.//*[@ID="AestheticButton"]');self.assertIsNotNone(button)
  ui=(M/'UI/P0Panel.lua').read_text();self.assertIn("request('CULTURE_AESTHETIC_DETAIL',true)",ui)
  src=(M/'CultureAesthetic.lua').read_text()
  for forbidden in ['SetUpdate(',"'CityWorkerChanged'","'CityFocusChanged'",'collectgarbage','GameCoreEventPublishComplete']:
   self.assertNotIn(forbidden,src)
  self.assertIn("RegisterExit('CultureAesthetic'",src)

if __name__=='__main__':unittest.main()
