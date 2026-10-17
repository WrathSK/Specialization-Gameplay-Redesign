"""B226 actual Lua projection/topology/legacy retirement. LOCAL only; no native PASS."""
from pathlib import Path
import ast,subprocess,sqlite3,unittest,importlib.util,xml.etree.ElementTree as ET
from lupa.lua55 import LuaRuntime
R=Path(__file__).resolve().parents[1];M=R/'Mod'
def literal(file,name):
 t=ast.parse((R/'DevelopmentTests'/file).read_text())
 return ast.literal_eval(next(n.value for n in t.body if isinstance(n,ast.Assign) and any(isinstance(x,ast.Name) and x.id==name for x in n.targets)))
BASE=literal('test_arch_v2_batch_a.py','FIXTURE')
ADAPT=r'''
Game.GetLocalPlayer=function()return 0 end
families={RESEARCH='DISTRICT_CAMPUS',CULTURE='DISTRICT_THEATER',INDUSTRY='DISTRICT_INDUSTRIAL_ZONE',COMMERCE='DISTRICT_COMMERCIAL_HUB'}
P.Family=function(domain)for k,v in pairs(families)do if v==domain then return k end end end
info={};yieldRows={};civRows={{CivilizationType='CIVILIZATION_OWN'}}
for i=1,120 do civRows[#civRows+1]={CivilizationType='CIVILIZATION_TEST_'..i}end
for k,v in pairs(families)do
 info[v]={Index=v,DistrictType=v}
 for bit=0,7 do local id='BUILDING_SPC_CULTURE_NETWORK_'..k..'_'..bit
  info[id]={Index=id,BuildingType=id,PrereqDistrict=v,InternalOnly=1,CitizenSlots=0,Housing=0}
  yieldRows[#yieldRows+1]={BuildingType=id,YieldType='YIELD_CULTURE',YieldChange=2^bit}
 end
end
P.Info=function(tab,id)return info[id] or (tab=='Buildings' and {Index=id,BuildingType=id,PrereqDistrict='DISTRICT_CITY_CENTER'})end
P.Rows=function(tab)if tab=='Building_CitizenYieldChanges'then return yieldRows elseif tab=='Civilizations'then return civRows end;return {}end
SPCDistrictCompleteness={Clone=function(t)local x={};for k,v in pairs(t)do x[k]=v end;return x end}
plots={};history={};historyReads={};factReads={};exits={};returns={};created=0;removed=0
function equip(c)
 c.present={};c.locations={};c.damage={};c.workers=2
 function c:GetBuildings()return {
  HasBuilding=function(_,id)if failHas==id then return nil end;return c.present[id]==true end,
  GetBuildingLocation=function(_,id)if failLocation==id then return nil end;return c.locations[id]end,
  IsPillaged=function(_,id)if failPillage==id then return nil end;return c.damage[id]==true end}end
 function c:GetBuildQueue()return {city=c}end
 function c:GetDistricts()
  local d={GetID=function()return c.id end,GetType=function()return families[c.kind]end,
   IsComplete=function()return not c.incomplete end,IsPillaged=function()return c.pillaged==true end,
   GetX=function()return c.id*100 end,GetY=function()return 0 end,GetCity=function()return c end}
  return {GetNumDistricts=function()return c.multiple and 2 or 1 end,GetDistrictByIndex=function()return d end}
 end
 plots[c.id*100]={GetIndex=function()return c.id*100 end,GetWorkerCount=function()return c.workers end}
 history[c.id]={}
 return c
end
for _,c in pairs(cities)do equip(c)end
Map={GetPlot=function(x)return plots[x]end,GetPlotByIndex=function(i)return plots[i]end}
P.HasBuilding=function(b,id)return b:HasBuilding(id)end
P.CreateBuilding=function(q,id)
 created=created+1;if createFail then return end
 q.city.present[id]=true;q.city.locations[id]=q.city.id*100;q.city.damage[id]=false
 if onCreate then onCreate(q.city,id)end
end
P.RemoveBuilding=function(b,id)
 removed=removed+1;if removeFail then return end
 for _,c in pairs(cities)do if c:GetBuildings().HasBuilding==nil then error('fixture')end end
 -- The explicit fixture wrappers attach owner below.
 b.city.present[id]=nil;b.city.locations[id]=nil;b.city.damage[id]=nil
end
for _,c in pairs(cities)do local original=c.GetBuildings;c.GetBuildings=function(self)local b=original(self);b.city=c;return b end end
PlayerConfigurations={[0]={GetCivilizationTypeName=function()return ownCiv or 'CIVILIZATION_OWN'end}}
shared.EffectiveFacts.Read=function(pid,c)
 factReads[c.id]=(factReads[c.id] or 0)+1
 if readFail or c.fail then error('TEMP_FACT_READ')end
 return {specialization=c.kind,potential=c.potential,active=c.active,activeStatus=c.active==nil and 'UNKNOWN_GOVERNOR' or 'KNOWN',
  token=c.token,first=c.kind~='NONE' and {districtID=c.id,type=families[c.kind]} or nil}
end
shared.CityProgressionStore={
 RegisterExit=function(name,fn)assert(not exits[name]);exits[name]=fn end,
 RegisterReturn=function(name,fn)assert(not returns[name]);returns[name]=fn end,
 ExpeditionInsights=function(pid,c)historyReads[c.id]=(historyReads[c.id]or 0)+1;if c.historyUnknown then error('HISTORY_UNKNOWN')end;return history[c.id]end,
 IsExitTarget=function(c,loss)return loss.confirmed==true end,
 RemoveOwned=function(c,loss,ids)assert(loss.confirmed);for _,id in ipairs(ids)do if c.present[id]then P.RemoveBuilding(c:GetBuildings(),id)end end end}
function complete(cid,n,category)
 local civ='CIVILIZATION_TEST_'..n
 for _,k in ipairs(category and {category} or {'PEOPLE','WORKS','PLACES'})do history[cid][civ..':'..k]={civ=civ,category=k,turn=turn}end
end
function amount(c)
 local out=0
 for kind in pairs(families)do for bit=0,7 do local id='BUILDING_SPC_CULTURE_NETWORK_'..kind..'_'..bit
  if c.present[id] and not c.damage[id]then out=out+2^bit end
 end end
 return out
end
function nativeTotal(c)return amount(c)*c.workers end
function fire(name,...)Events[name].Fire(...)end
'''
def fixture(ready=True):
 l=LuaRuntime(unpack_returned_tuples=True);l.execute(BASE);l.execute(ADAPT)
 l.globals().include=lambda name:l.execute((M/(name+'.lua')).read_text())
 l.execute((M/'NetworkBridge.lua').read_text());l.execute('SPCNetworkBridge.Start(P,shared);net=shared.NetworkBridge;net.ready=true;cities[4].active=4')
 l.execute((M/'CultureNetwork.lua').read_text());l.execute('SPCCultureNetwork.Start(P,shared);cn=shared.CultureNetwork')
 if ready:l.execute("send('0,4,0,2,10;0,2,0,1,11;0,2,0,5,12',3);fire('LoadScreenClose')")
 return l

class Projection(unittest.TestCase):
 def test_three_categories_independent_per_city_then_union_no_recursion(self):
  l=fixture();l.execute("""
   complete(4,1,'PEOPLE');complete(4,1,'WORKS');complete(2,1,'PLACES')
   cn.SourceChanged(0,4);assert(amount(cities[1])==0)
   complete(4,1,'PLACES');cn.SourceChanged(0,4)
   assert(amount(cities[1])==1 and amount(cities[2])==1 and amount(cities[5])==1)
   assert(next(history[1])==nil and #net.CurrentRecipientSources(0,cities[1],'CULTURE')==1)
  """)
 def test_capital_self_connection_and_no_recursive_distribution(self):
  l=fixture();l.execute("""
   complete(4,1);capitalID=4;send('',0);cn.SourceChanged(0,4);assert(amount(cities[4])==1)
   capitalID=1;cities[3].kind='COMMERCE';cities[3].potential=1;cities[3].active=0
   send('0,4,0,2,10;0,2,0,3,11;0,3,0,1,12',3)
   assert(amount(cities[3])==1 and amount(cities[1])==0)
  """)
 def test_changed_source_only_reconciles_related_receivers(self):
  l=fixture();l.execute("""
   complete(4,1);cn.SourceChanged(0,4);factReads={};historyReads={}
   cn.Audit({player=0,changed={[1]=true}})
   assert(factReads[1]==1 and not factReads[2] and not factReads[5] and historyReads[4]==1)
  """)
 def test_no_topology_change_new_record_updates_all_related_receivers(self):
  l=fixture();l.execute("complete(4,1);local v=net.Input(0).inputVersion;cn.SourceChanged(0,4);assert(net.Input(0).inputVersion==v and amount(cities[1])==1 and amount(cities[5])==1);local a=created;cn.SourceChanged(0,4);assert(created==a)")
 def test_union_dedup_owner_filter_and_beyond_64(self):
  l=fixture();l.execute("""
   cities[3].kind='CULTURE';cities[3].active=4;cities[3].potential=4
   for n=1,40 do complete(4,n)end;for n=35,70 do complete(3,n)end
   send('0,4,0,2,10;0,3,0,2,13;0,2,0,1,11',3)
   assert(amount(cities[1])==70)
   ownCiv='CIVILIZATION_TEST_1';cn.Audit({player=0});assert(amount(cities[1])==69)
  """)
 def test_receiver_active_zero_and_native_workers_not_cached(self):
  l=fixture();l.execute("""
   complete(4,1);cities[1].active=0;cn.SourceChanged(0,4);assert(amount(cities[1])==1)
   local writes=created+removed;cities[1].workers=0;assert(nativeTotal(cities[1])==0)
   cities[1].workers=4;fire('CityWorkerChanged',0,1);assert(nativeTotal(cities[1])==4 and created+removed==writes)
   assert(cn.Describe(0,cities[1]):find('专家 4',1,true))
  """)
 def test_four_identities_none_pillage_and_no_extra_active_gate(self):
  for kind in ['RESEARCH','CULTURE','INDUSTRY','COMMERCE','NONE']:
   with self.subTest(kind=kind):
    l=fixture();l.execute("complete(4,1);cities[1].kind='"+kind+"';cities[1].active=0;cn.Audit({player=0});assert(amount(cities[1])=="+('0' if kind=='NONE' else '1')+");cities[1].pillaged=true;cn.Audit({player=0});assert(amount(cities[1])==0)")
 def test_source_downgrade_recovers_and_disconnection_withdraws(self):
  l=fixture();l.execute("""
   complete(4,1);cn.SourceChanged(0,4);assert(amount(cities[1])==1)
   cities[4].active=3;fire('GovernorChanged',0);fire('GameCoreEventPublishComplete');assert(amount(cities[1])==0)
   cities[4].active=4;fire('GovernorEstablished',0);fire('GameCoreEventPublishComplete');assert(amount(cities[1])==1)
   send('',0);assert(amount(cities[1])==0 and next(history[4])~=nil)
  """)
 def test_unknown_holds_but_never_contributing_low_source_does_not_force_clear(self):
  l=fixture();l.execute("""
   complete(4,1);cn.SourceChanged(0,4)
   cities[3].kind='CULTURE';cities[3].active=3;cities[3].potential=4
   send('0,4,0,2,10;0,3,0,2,13;0,2,0,1,11',3)
   cities[4].historyUnknown=true;local n=created+removed;cn.Audit({player=0})
   assert(amount(cities[1])==1 and created+removed==n and cn.errors['0:1'])
  """)
 def test_late_presence_location_pillage_unknown_do_not_remove_prior_projection(self):
  for change in ["failHas='BUILDING_SPC_CULTURE_NETWORK_COMMERCE_7'", "failLocation='BUILDING_SPC_CULTURE_NETWORK_RESEARCH_0'", "failPillage='BUILDING_SPC_CULTURE_NETWORK_RESEARCH_0'"]:
   with self.subTest(change=change):
    l=fixture();l.execute("complete(4,1);cn.SourceChanged(0,4);local n=created+removed;"+change+";cn.Audit({player=0,city=1,changed={[1]=true}});assert(amount(cities[1])==1 and cn.records['0:1'] and created+removed==n and cn.errors['0:1'])")
 def test_reference_change_or_confirmed_loss_cannot_hold_old_source(self):
  l=fixture();l.execute("""
   complete(4,1);cn.SourceChanged(0,4);cities[4].owner=9
   net.CheckEvidence(false);cn.Audit({player=0});assert(amount(cities[1])==0)
  """)
 def test_memo_history_once_per_source_and_same_payload_zero_writes(self):
  l=fixture();l.execute("""
   complete(4,1);historyReads={};factReads={};cn.SourceChanged(0,4)
   assert(historyReads[4]==1 and factReads[4]==1)
   local n=created+removed;cn.Audit({player=0});assert(created+removed==n and propertyWrites==0)
  """)
 def test_wrong_location_pillage_and_identity_switch_repair_exact_owned_ids(self):
  l=fixture();l.execute("""
   complete(4,1);cn.SourceChanged(0,4);local id='BUILDING_SPC_CULTURE_NETWORK_RESEARCH_0'
   cities[1].locations[id]=999;cities[1].present.KEEP=true
   cn.Audit({player=0,city=1});assert(cities[1].locations[id]==100 and cities[1].present.KEEP)
   cities[1].damage[id]=true;cn.Audit({player=0,city=1});assert(not cities[1].damage[id])
   cities[1].kind='INDUSTRY';cn.Audit({player=0,city=1});assert(not cities[1].present[id] and amount(cities[1])==1)
  """)
 def test_native_write_readback_failure_is_reported(self):
  l=fixture();l.execute("complete(4,1);createFail=true;cn.SourceChanged(0,4);assert(amount(cities[1])==0 and cn.errors['0:1']);createFail=false;cn.SourceChanged(0,4);assert(amount(cities[1])==1)")
 def test_initial_load_saved_carriers_cleanup_no_history_or_property_write(self):
  l=fixture(False);l.execute("""
   cities[1].present.BUILDING_SPC_CULTURE_NETWORK_RESEARCH_7=true;cities[1].locations.BUILDING_SPC_CULTURE_NETWORK_RESEARCH_7=100
   cities[1].present.KEEP=true;complete(4,1);send('0,4,0,2,10;0,2,0,1,11',2)
   fire('LoadScreenClose');assert(amount(cities[1])==1 and cities[1].present.KEEP and propertyWrites==0)
  """)
 def test_return_only_marks_then_uses_committed_facts(self):
  l=fixture();l.execute("complete(4,1);cities[1].kind='NONE';cn.Audit({player=0});returns.CultureNetwork(0,cities[1]);cities[1].kind='RESEARCH';assert(amount(cities[1])==0);fire('GameCoreEventPublishComplete');assert(amount(cities[1])==1)")
 def test_exit_exact_cleanup_isolation_and_wrong_city_protection(self):
  l=fixture();l.execute("""
   complete(4,1);cn.SourceChanged(0,4);cities[1].present.KEEP=true
   assert(not pcall(exits.CultureNetwork,cities[1],{confirmed=false,origin={owner=0}}))
   exits.CultureNetwork(cities[1],{confirmed=true,origin={owner=0}})
   assert(amount(cities[1])==0 and amount(cities[5])==1 and cities[1].present.KEEP)
   shared.NetworkIsolation={Active=function()return true end};assert(cn.ExperimentalNetworkWithdraw(0))
   assert(amount(cities[5])==0);cn.Audit({player=0});assert(amount(cities[5])==0)
  """)
 def test_culture_batch_copy_cannot_mutate_shared_topology(self):
  l=fixture();l.execute("local a=net.CurrentCultureBatch(0);a.recipients[1]={};a.input.validity='BAD';assert(#net.CurrentRecipientSources(0,cities[1],'CULTURE')==1 and net.Input(0).validity=='VERIFIED')")

class DatabaseAndRetirement(unittest.TestCase):
 def test_sql_research_unchanged_culture_inert_and_32_exact_specialist_ids(self):
  d=sqlite3.connect(':memory:');d.executescript('CREATE TABLE Types(Type TEXT,Kind TEXT);CREATE TABLE Buildings(BuildingType TEXT,Name TEXT,Cost INTEGER,PrereqDistrict TEXT,InternalOnly INTEGER,CitizenSlots INTEGER,Housing INTEGER);CREATE TABLE Modifiers(ModifierId TEXT,ModifierType TEXT);CREATE TABLE ModifierArguments(ModifierId TEXT,Name TEXT,Value TEXT);CREATE TABLE BuildingModifiers(BuildingType TEXT,ModifierId TEXT);CREATE TABLE Building_CitizenYieldChanges(BuildingType TEXT,YieldType TEXT,YieldChange INTEGER);')
  for file in ['Data/NetworkBoost.sql','Data/NetworkBoostInteger.sql','Data/BoostIntegerTest.sql']:
   now=(M/file).read_text();old=subprocess.check_output(['git','show','224b679:Mod/'+file],cwd=R,text=True)
   self.assertEqual([x for x in now.splitlines()if 'RESEARCH' in x],[x for x in old.splitlines()if 'RESEARCH' in x]);d.executescript(now)
  self.assertEqual(d.execute("SELECT count(*) FROM Buildings WHERE BuildingType LIKE 'BUILDING_SPC_B0%_CULTURE_%'").fetchone()[0],563)
  self.assertEqual(d.execute("SELECT count(*) FROM BuildingModifiers WHERE BuildingType LIKE '%_CULTURE_%'").fetchone()[0],0)
  self.assertEqual(d.execute('SELECT count(*) FROM BuildingModifiers').fetchone()[0],1126)
  d.executescript((M/'Data/CultureNetwork.sql').read_text())
  self.assertEqual(d.execute("SELECT count(*) FROM Building_CitizenYieldChanges").fetchone()[0],32)
  self.assertEqual(d.execute("SELECT sum(CitizenSlots)+sum(Housing) FROM Buildings WHERE BuildingType LIKE 'BUILDING_SPC_CULTURE_NETWORK_%'").fetchone()[0],0)
 def test_generators_reproduce_and_imports_package_version(self):
  for file in ['generate_boost.py','generate_boost_integer.py']:
   spec=importlib.util.spec_from_file_location(file,R/'tools'/file);module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
   for path,text in module.render().items():self.assertEqual((R/path).read_text(),text)
  root=ET.parse(M/'SpecializationP0.modinfo').getroot();self.assertEqual(root.get('version'),'253')
  imports=[x.text for x in root.findall('.//ImportFiles/File')];self.assertEqual(imports.count('CultureNetwork.lua'),1)
  for x in root.findall('./Files/File'):self.assertTrue((M/x.text).exists(),x.text)



class RuntimeRetirement(unittest.TestCase):
 def boost(self,old=False):
  l=fixture();l.execute((M/'BoostConfig.lua').read_text());l.execute((M/'BoostIntegerConfig.lua').read_text())
  source=subprocess.check_output(['git','show','224b679:Mod/NetworkBoost.lua'],cwd=R,text=True) if old else (M/'NetworkBoost.lua').read_text()
  l.execute(source);l.execute('SPCNetworkBoost.Start(P,shared);boost=shared.NetworkBoost;boost.EnsureReady(0)');return l
 def test_normal_and_test_research_values_equal_previous_runtime(self):
  old,new=self.boost(True),self.boost()
  for change in ["cities[1].active=1", "cities[1].active=4", "send('0,1,0,2,10;0,2,0,5,11',2)", "boost.Test(0,1.5)", "boost.Test(0,3.8)", "boost.Test(0,0)", "boost.Test(0,nil)"]:
   for l in [old,new]:l.execute(change+';boost.Audit({player=0})')
   get="function()local p=boost.Plan(0).RESEARCH;return p.n,p.level,p.amount,p.finalRaw,p.building end"
   self.assertEqual(old.eval(get)(),new.eval(get)())
   new.execute("assert(boost.Plan(0).CULTURE==nil);for _,c in pairs(cities)do for id in pairs(c.present)do assert(not id:match('^BUILDING_SPC_B0%d%d_CULTURE_'))end end")
 def test_cleanup_all_563_old_culture_ids_keeps_unrelated_and_new_network(self):
  l=self.boost();l.execute("""
   local c=cities[1];local n=0
   for key,v in pairs(SPCBoostConfig.rows)do if key:match('^CULTURE:')then c.present[v.building]=true;n=n+1 end end
   for key,id in pairs(SPCBoostIntegerConfig.rows)do if key:match('^CULTURE:')then c.present[id]=true;n=n+1 end end
   for _,value in ipairs({2,4})do c.present['BUILDING_SPC_B057_CULTURE_'..value]=true;n=n+1 end
   assert(n==563);c.present.OTHER_HD=true;c.present.BUILDING_SPC_CULTURE_NETWORK_RESEARCH_0=true
   boost.Clean();assert(c.present.OTHER_HD and c.present.BUILDING_SPC_CULTURE_NETWORK_RESEARCH_0 and propertyWrites==0)
   for id in pairs(c.present)do assert(not id:match('^BUILDING_SPC_B0%d%d_CULTURE_'))end
  """)
 def test_failed_retirement_does_not_claim_ready_or_reset_shared_property(self):
  l=self.boost();l.execute("boost.ready=false;cities[1].present.BUILDING_SPC_B058_CULTURE_1=true;removeFail=true;boost.EnsureReady(0);assert(not boost.ready and boost.errors[0] and propertyWrites==0)")
 def test_six_module_isolation_includes_actual_new_projection(self):
  l=fixture();l.execute("complete(4,1);cn.SourceChanged(0,4);assert(amount(cities[1])==1)")
  l.execute((M/'NetworkIsolation.lua').read_text());l.execute("""
   for _,name in ipairs({'Lv3Effects','NetworkBoost','CopyYields','CommerceConvergence','StandardizationDiscount'})do
    shared[name]={ExperimentalNetworkWithdraw=function()return true end}
   end
   for _,name in ipairs({'SPC_P0_BackgroundRoutes','SPC_CopyBackground','SPC_DiscountEligibility'})do
    ExposedMembers[name]={version=P.VERSION,networkStopped=true,networkStopEpoch=net.epoch}
   end
   SPCNetworkIsolation.Start(P,shared);local text=shared.NetworkIsolation.Begin(0,net.epoch)
   assert(shared.NetworkIsolation.completed==6 and shared.NetworkIsolation.phase=='READY' and text:find('/6',1,true))
   assert(amount(cities[1])==0 and amount(cities[5])==0)
  """)

class GateIntegration(unittest.TestCase):
 def test_actual_task_completion_notifies_even_without_route_change(self):
  from test_expedition_spy_activity_integration import integrated
  l=integrated();l.execute("""
   calls=0;shared.CultureNetwork={SourceChanged=function(pid,cid)
    assert(pid==2 and cid==1 and insightWrites==1);calls=calls+1
   end}
   beginTask();currentTurn=85;ownTurn(2);Events.GameCoreEventPublishComplete()
   assert(calls==1 and view().phase=='ARRIVED')
  """)
 def test_failed_consumer_is_isolated_from_other_network_consumers(self):
  l=fixture();l.execute("""
   local n=0;shared.NetworkBoost={Audit=function()n=n+1 end}
   shared.CultureNetwork.Audit=function()error('CN_TEST_FAILURE')end
   send('0,4,0,2,10;0,2,0,1,11',2)
   assert(n==1 and net.Input(0).validity=='VERIFIED' and net.players[0].consumerError)
  """)

if __name__=='__main__':unittest.main()
