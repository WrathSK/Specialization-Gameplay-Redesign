"""B236 current Crew source/writer with actual city Store and event fixtures.
Native counter timing, retreat, prices and injection stay USER_GAME_TEST_REQUIRED.
"""
from pathlib import Path
import unittest
import sqlite3
import zlib
from project_paths import external_database
from test_b234_standardization import lua
from test_industry_history import runtime
R=Path(__file__).resolve().parents[1]
M=R/'Mod'
SETUP=r'''
C={units={},stats={},props={},calls=0,requests=0,speed=100}
local CP=SPCCrewModel;local cp=CP.Copy
local oldInfo=P.Info
C.rows={Projects={},Buildings={},Units={}}
local index=10000
for tier,base in ipairs(CP.CAPACITY)do
 local u={UnitType='UNIT_SPC_CREW_'..CP.IDS[tier],Index=11000+tier,Name='crew',FormationClass='FORMATION_CLASS_CIVILIAN'}
 C.rows.Units[u.UnitType]=u;C.rows.Units[u.Index]=u
 for _,ratio in ipairs(CP.RATIOS)do
  index=index+1;local id=CP.Project(tier,ratio)
  local p={Index=index,Hash=index,ProjectType=id,Cost=math.floor(base*ratio/100)}
  C.rows.Projects[id]=p;C.rows.Projects[index]=p;C.stats[id]=0
  index=index+1;local b={Index=index,BuildingType=CP.Marker(tier,ratio),InternalOnly=1}
  C.rows.Buildings[b.BuildingType]=b;C.rows.Buildings[index]=b
 end
end
local legacy={Index=12000,BuildingType='BUILDING_SPC_CREW_PROJECT_ACCESS',InternalOnly=1}
C.rows.Buildings[legacy.BuildingType]=legacy;C.rows.Buildings[legacy.Index]=legacy
function C.install()
 P.Info=function(t,k)return C.rows[t] and C.rows[t][k] or oldInfo(t,k)end
 P.Field=function(o,k)return o and o[k]end
 P.Call=function(o,k,...)if not o or type(o[k])~='function'then return false end;return pcall(o[k],o,...)end
 P.CrewBase=function(kind)for tier,base in ipairs(CP.CAPACITY)do if kind=='UNIT_SPC_CREW_'..CP.IDS[tier]then return base end end end
 P.HasBuilding=function(b,id)return b:HasBuilding(id)end
 P.SetProperty=function(o,k,v)o:SetProperty(k,v)end
 P.CreateBuilding=function(q,id)q.c.buildings[id]=true end
 P.RemoveBuilding=function(b,id)b:RemoveBuilding(id)end
 GameInfo=GameInfo or {};GameInfo.GameSpeeds={STANDARD={CostMultiplier=C.speed}}
 GameConfiguration={GetGameSpeedType=function()return 'STANDARD'end}
 local p=Players[0];local priorUnits=p.GetUnits
 p.GetUnits=function()return {Members=function()return pairs(C.units)end,FindID=function(_,id)return C.units[id] or priorUnits():FindID(id)end,
 Destroy=function(_,u)if not u.GetID or not C.units[u:GetID()]then return priorUnits():Destroy(u)end;C.units[u:GetID()]=nil;Events.UnitRemovedFromMap.Fire(0,u:GetID())end}end
 p.GetProperty=function(_,k)return cp(C.props[k])end
 p.SetProperty=function(_,k,v)
  if C.receiptFailure and k==CP.RECEIPT_PROPERTY then
   if C.receiptFailure=='throw'then error('fault')elseif C.receiptFailure=='third'then C.props[k]={bad=true}end;return
  end
  C.props[k]=cp(v)
 end
 UnitManager={InitUnit=function(pid,kind,x,y)
  C.calls=C.calls+1;if C.grantFailure=='before'then error('native failed')end
  local id=20000+C.calls;local props={};local u={x=x,y=y,id=id,kind=kind}
  function u:GetID()return id end;function u:GetOwner()return pid end;function u:GetType()return C.rows.Units[kind].Index end
  function u:GetX()return self.x end;function u:GetY()return self.y end;function u:GetBuildCharges()return 1 end
  function u:GetProperty(k)return cp(props[k])end
  function u:SetProperty(k,v)
   if k==CP.UNIT_PROPERTY and C.bindingFailure then if C.bindingFailure=='third'then props[k]={bad=true}end;return end
   props[k]=cp(v)
  end
  C.units[id]=u;Events.UnitAddedToMap.Fire(pid,id)
  if C.grantFailure=='after'then error('native threw after birth')end
  if C.grantFailure=='nil'then return nil end
  return u
 end}
 ExposedMembers.SPC_CrewNativeRead=function(pid,id)
  local c=Players[pid]:GetCities():FindID(id);local q=c:GetBuildQueue()
  local v={owner=pid,city=id,x=c:GetX(),y=c:GetY(),turn=Game.GetCurrentGameTurn(),projects=cp(q.items),completed=cp(C.stats),costs={},progress={}}
  for project in pairs(C.stats)do local row=C.rows.Projects[project];v.costs[project]=math.floor(row.Cost*C.speed/100);v.progress[project]=q.progressByProject[project]or 0 end
  if C.costFailure then v.costs.PROJECT_SPC_CREW_250=1 end
  if C.readerFailure then error('native unavailable')end
  return v
 end
end
function C.setup(c)
 C.install();SPCCrewProjects.Start(P,shared);crew=shared.CrewProjects;crew.BindPermanentWrites()
 Events.GameCoreEventPublishComplete.Fire()
end
function C.queue(c)
 local oldGet,oldSet=c.GetProperty,c.SetProperty;local props={}
 c.GetProperty=function(o,k)if k==CP.ORDER_PROPERTY then return cp(props[k])end;return oldGet(o,k)end
 c.SetProperty=function(o,k,v)
  if k==CP.ORDER_PROPERTY then
   if C.orderFailure then
    if C.orderFailure=='third'then props[k]={bad=true}end
    if C.orderFailure=='after'then props[k]=cp(v);error('after write')end
    if C.orderFailure=='throw'then error('write error')end;return
   end
   props[k]=cp(v);return
  end;return oldSet(o,k,v)
 end
 local q={c=c,items={},progressByProject={}};c.GetBuildQueue=function()return q end
 c.GetBuildings=function()return {HasBuilding=function(_,id)return c.buildings[id]==true end,RemoveBuilding=function(_,id)c.buildings[id]=nil end}end
 return q
end
function C.make(level)
 local c=H.newIndustry();T.governor(4);for i=1,(level or 4)-1 do T.invest(c,8800+i)end
 C.queue(c);C.setup(c);return c
end
function C.reserve(c,tier,ratio)
 C.requests=C.requests+1
 crew.Request(0,{CityID=c:GetID(),Token='test:'..C.requests,Action='RESERVE',Project=CP.Project(tier or 1,ratio or 150)})
 return ExposedMembers.SPC_CrewReply
end
function C.begin(c,tier,ratio)
 local p=CP.Project(tier or 1,ratio or 150);local reply=C.reserve(c,tier,ratio);assert(not reply.error,reply.error)
 local q=c:GetBuildQueue();q.items[p]=(q.items[p] or 0)+1
 Events.CityProductionChanged.Fire(0,c:GetID())
 C.requests=C.requests+1;crew.Request(0,{CityID=c:GetID(),Token='confirm:'..C.requests,Action='CONFIRM',Reservation=reply.reservation})
 assert(not ExposedMembers.SPC_CrewReply.error,ExposedMembers.SPC_CrewReply.error);return p
end
function C.complete(c,p)
 local q=c:GetBuildQueue();q.items[p]=(q.items[p]or 0)-1;if q.items[p]<=0 then q.items[p]=nil end
 q.progressByProject[p]=0;C.stats[p]=C.stats[p]+1;Events.CityProductionChanged.Fire(0,c:GetID())
 Events.CityProjectCompleted.Fire(0,c:GetID(),C.rows.Projects[p].Index);Events.GameCoreEventPublishComplete.Fire()
end
function C.count(c)return crew.Inventory(0)[shared.CityProgressionStore.HistoricalReference(c).token]or 0 end
function C.reload(c)
 H.reload();C.setup(c)
end
'''
def crew_runtime():
 l=runtime()
 l.execute((M/'CrewModel.lua').read_text());l.execute((M/'CrewProjects.lua').read_text());l.execute(SETUP)
 return l
class Formation(unittest.TestCase):
 def check(self,s):crew_runtime().execute(s)
 def test_two_mixed_slots_third_denied_and_native_removal_frees(self):
  self.check("local c=C.make();local a=C.begin(c,1);local b=C.begin(c,2);assert(C.reserve(c,3).error);C.complete(c,a);C.complete(c,b);assert(C.count(c)==2 and C.calls==2);assert(C.reserve(c,1).error);local u=C.units[20001];u.x=u.x+5;crew.Audit({player=0});assert(C.count(c)==2);Players[0]:GetUnits():Destroy(u);Events.GameCoreEventPublishComplete.Fire();assert(C.count(c)==1 and not C.reserve(c,1).error)")
 def test_same_project_two_queued_duplicate_and_reordered_completion(self):
  self.check("local c=C.make();local p=C.begin(c);C.begin(c);C.complete(c,p);Events.CityProjectCompleted.Fire(0,c:GetID(),C.rows.Projects[p].Index);assert(C.calls==1);C.complete(c,p);for i=1,4 do Events.CityProjectCompleted.Fire(0,c:GetID(),C.rows.Projects[p].Index)end;assert(C.calls==2 and C.count(c)==2)")
 def test_first_same_type_completes_before_second_admission_ack(self):
  self.check("local c=C.make();local p=C.begin(c);local r=C.reserve(c);assert(not r.error);c:GetBuildQueue().items[p]=2;C.complete(c,p);crew.Request(0,{CityID=c:GetID(),Token='late-ack',Action='CONFIRM',Reservation=r.reservation});assert(not ExposedMembers.SPC_CrewReply.error);C.complete(c,p);assert(C.count(c)==2 and C.calls==2)")
 def test_active_III_tiers_cost_and_IV_N(self):
  self.check("local c=C.make(3);H.wonder(c,1);crew.Refresh(0,c:GetID());assert(C.reserve(c,4).error);assert(C.reserve(c,1,140).error);local p=C.begin(c,3);C.complete(c,p);T.invest(c,8900);crew.Refresh(0,c:GetID());assert(crew.views['0:'..c:GetID()].ratio==140);assert(C.reserve(c,4,150).error);assert(not C.reserve(c,4,140).error)")
 def test_price_locks_and_qualification_drop_does_not_delete_paid_order(self):
  self.check("local c=C.make();local p=C.begin(c,4);H.wonder(c,1);crew.Refresh(0,c:GetID());assert(crew.views['0:'..c:GetID()].ratio==140);T.governor(2);Events.GovernorChanged.Fire(0);Events.GameCoreEventPublishComplete.Fire();C.complete(c,p);assert(C.count(c)==1 and crew.Unit(0,C.units[20001]).capacity==1000);assert(C.reserve(c).error)")
 def test_unknown_qualification_no_new_admission_existing_order_retained(self):
  self.check("local c=C.make();C.begin(c);local read=shared.EffectiveFacts.Read;shared.EffectiveFacts.Read=function(pid,c)local f=read(pid,c);f.activeStatus='UNKNOWN';return f end;crew.Refresh(0,c:GetID());assert(C.reserve(c).error);assert(#c:GetProperty(SPCCrewModel.ORDER_PROPERTY).orders==1 and C.calls==0)")
 def test_native_cost_and_unbound_foreign_crew_hold_admission(self):
  for change in ("C.costFailure=true", "UnitManager.InitUnit(0,'UNIT_SPC_CREW_250',c:GetX(),c:GetY())"):
   with self.subTest(change=change):self.check("local c=C.make();"+change+";assert(C.reserve(c).error)")
 def test_cold_restore_queue_and_bound_provenance(self):
  self.check("local c=C.make();local p=C.begin(c);C.reload(c);C.complete(c,p);local before=T.encode(crew.Unit(0,C.units[20001]));C.reload(c);assert(C.count(c)==1 and T.encode(crew.Unit(0,C.units[20001]))==before);Events.CityProjectCompleted.Fire(0,c:GetID(),C.rows.Projects[p].Index);assert(C.calls==1)")
 def test_empty_cold_reservation_cancels_without_grant(self):
  self.check("local c=C.make();assert(not C.reserve(c).error);C.reload(c);assert(#c:GetProperty(SPCCrewModel.ORDER_PROPERTY).orders==0 and C.calls==0)")
 def test_native_creation_failure_no_replay_even_after_coldload(self):
  for failure in ('before','after','nil'):
   with self.subTest(failure=failure):self.check("local c=C.make();local p=C.begin(c);C.grantFailure='%s';C.complete(c,p);assert(C.calls==1);C.reload(c);Events.CityProjectCompleted.Fire(0,c:GetID(),C.rows.Projects[p].Index);assert(C.calls==1);assert(C.reserve(c).error)"%failure)
 def test_binding_failure_held_not_granted_again(self):
  for failure in ('drop','third'):
   with self.subTest(failure=failure):self.check("local c=C.make();local p=C.begin(c);C.bindingFailure='%s';C.complete(c,p);assert(C.calls==1);C.reload(c);Events.CityProjectCompleted.Fire(0,c:GetID(),C.rows.Projects[p].Index);assert(C.calls==1 and C.reserve(c).error)"%failure)
 def test_order_write_failure_prevents_native_grant(self):
  for failure in ('drop','third','throw'):
   with self.subTest(failure=failure):self.check("local c=C.make();C.orderFailure='%s';assert(C.reserve(c).error);assert(C.calls==0)"%failure)
 def test_throw_after_verified_order_write_is_accepted(self):
  self.check("local c=C.make();C.orderFailure='after';assert(not C.reserve(c).error);assert(C.calls==0)")
 def test_receipt_write_failure_prevents_native_grant(self):
  for failure in ('drop','third','throw'):
   with self.subTest(failure=failure):self.check("local c=C.make();local p=C.begin(c);C.receiptFailure='%s';C.complete(c,p);assert(C.calls==0);C.reload(c);Events.CityProjectCompleted.Fire(0,c:GetID(),C.rows.Projects[p].Index);assert(C.calls==0)"%failure)
 def test_actual_store_loss_return_and_source_use_survives(self):
  self.check("local c=C.make();local p=C.begin(c);C.complete(c,p);local unit=C.units[20001];local before=T.encode(crew.Unit(0,unit));C.begin(c);T.loss(c,3,55);shared.CityProgressionStore.ExitConfirmed();assert(T.encode(crew.Unit(0,unit))==before and #c:GetProperty(SPCCrewModel.ORDER_PROPERTY).orders==0);c.s.ref.owner=0;c.s.ref.cityID=500;Events.CityTransfered.Fire(0,500,3);Events.GameCoreEventPublishComplete.Fire();assert(C.count(c)==1 and T.encode(crew.Unit(0,unit))==before)")
 def test_source_token_mismatch_and_other_city_isolation(self):
  self.check("local c=C.make();local other=H.city(2);C.queue(other);local before=T.encode(T.record(other));local p=C.begin(c);C.complete(c,p);assert(T.encode(T.record(other))==before);local h=shared.CityProgressionStore.HistoricalReference;shared.CityProgressionStore.HistoricalReference=function(city)local a=h(city);if city==c then a.token='CHANGED'end;return a end;assert(C.reserve(c).error and C.calls==1)")
 def test_missing_admission_or_counter_jump_never_guesses_unit(self):
  for before in ("", "C.begin(c);C.stats[p]=2"):
   with self.subTest(before=before):self.check("local c=C.make();local p=SPCCrewModel.Project(1,150);"+before+";C.complete(c,p);assert(C.calls==0 and crew.errors['0:'..c:GetID()])")
 def test_unchanged_publish_does_not_rescan_or_write(self):
  self.check("local c=C.make();local inv=crew.Inventory;local visits=0;crew.Inventory=function(pid)visits=visits+1;return inv(pid)end;for i=1,100 do Events.GameCoreEventPublishComplete.Fire()end;assert(visits==0)")

class CostModel(unittest.TestCase):
 def test_complete_standard_matrix(self):
  l=crew_runtime();l.execute("""
   local expected={{390,364,338,312},{630,588,546,504},{1125,1050,975,900},{1500,1400,1300,1200},{2040,1904,1768,1632}}
   for tier,values in ipairs(expected)do for i,ratio in ipairs(SPCCrewModel.RATIOS)do assert(SPCCrewModel.Cost(tier,ratio,100)==values[i])end end
   for n=0,10 do assert(SPCCrewModel.Multiplier(3,n)==150);assert(SPCCrewModel.Multiplier(4,n)==(n>=6 and 120 or n>=3 and 130 or n>=1 and 140 or 150))end
  """)
 def test_locked_capacity_floor_is_separate_from_price_and_invalid_facts_reject(self):
  l=crew_runtime();l.execute("""
   assert(SPCCrewModel.Amount(1,67)==174)
   assert(SPCCrewModel.Cost(1,150,67)==261)
   assert(not pcall(SPCCrewModel.Multiplier,4,nil));assert(not pcall(SPCCrewModel.Amount,1,0))
  """)


ACTION=r"""
function C.actions(c)
 local q=c:GetBuildQueue();q.target='BUILDING_WONDER_2';q.progress=10;q.cost=1000;q.adds={}
 q.AddProgress=function(_,n)q.adds[#q.adds+1]=n;q.progress=q.progress+n end
 shared.ConstructionProbe={ReadSnapshot=function(pid,city)
  local q=city:GetBuildQueue();return {kind='Buildings',target=q.target,progress=q.progress,cost=q.cost}
 end}
 shared.UnitTargets={Refresh=function(pid,p)shared.UnitTargetSnapshot={plots={{plot=500,cityID=c:GetID()}}}end}
 Map={GetPlot=function()return {GetIndex=function()return 500 end}end}
 SPCUnitActions.Start(P,shared)
end
function C.use(c,u,token)
 local a=shared.UnitActions
 local text=a.Run(0,{Action='UNIT_ACTION_PREPARE',UnitID=u:GetID(),Token=token});assert(text:find('PREPARED'),text)
 local out,receipt=a.Run(0,{Action='UNIT_ACTION_CONFIRM',UnitID=u:GetID(),PlanToken=token,Token='confirm:'..token});assert(receipt==nil,'Crew must not publish an investment commit');return out
end
"""
class Consumption(unittest.TestCase):
 # D0053 explicitly accepts native amplification; fixed-base isolation is no longer the oracle.
 def fixture(self):
  l=crew_runtime();l.execute((M/'UnitActions.lua').read_text());l.execute(ACTION);return l
 def test_accepted_native_multiplier_keeps_base_request_and_one_use(self):
  for multiplier in (1,1.54,2):
   with self.subTest(multiplier=multiplier):
    l=self.fixture();l.execute("""
     local c=C.make();local p=C.begin(c);C.complete(c,p);C.actions(c);local q=c:GetBuildQueue()
     q.AddProgress=function(_,n)q.adds[#q.adds+1]=n;q.progress=q.progress+math.floor(n)*%s end
     local v=shared.UnitActions.ReadView(0,20001,'view');assert(v.legal and v.amount==260 and v.baseInput==260 and v.baseUnused==0 and v.after==nil)
     local out=C.use(c,C.units[20001],'once');assert(out:find('CREW CONSUMED',1,true),out)
     assert(#q.adds==1 and q.adds[1]==260 and math.abs(q.progress-(10+260*%s))<0.0001)
     for i=1,3 do shared.UnitActions.Run(0,{Action='UNIT_ACTION_CONFIRM',UnitID=20001,Token='retry'})end
     assert(#q.adds==1 and C.count(c)==0)
    """%(multiplier,multiplier))
 def test_normal_building_rejected_before_debit(self):
  l=self.fixture();l.execute("local c=C.make();local p=C.begin(c);C.complete(c,p);C.actions(c);c:GetBuildQueue().target='BUILDING_A';local out=shared.UnitActions.Run(0,{Action='UNIT_ACTION_PREPARE',UnitID=20001,Token='x'});assert(out:find('REJECTED') and C.count(c)==1 and #c:GetBuildQueue().adds==0)")
 def test_stale_target_and_reused_native_id_rejected(self):
  for change in ("c:GetBuildQueue().progress=11", "local u=C.units[20001];local b=crew.Unit(0,u);b.grant='DIFFERENT';u:SetProperty(SPCCrewModel.UNIT_PROPERTY,b)"):
   with self.subTest(change=change):
    l=self.fixture();l.execute("local c=C.make();local p=C.begin(c);C.complete(c,p);C.actions(c);shared.UnitActions.Run(0,{Action='UNIT_ACTION_PREPARE',UnitID=20001,Token='x'});"+change+";local out=shared.UnitActions.Run(0,{Action='UNIT_ACTION_CONFIRM',UnitID=20001,PlanToken='x'});assert(out:find('REJECTED') and C.count(c)==1 and #c:GetBuildQueue().adds==0)")
 def test_unconfirmed_use_receipt_or_debit_never_injects(self):
  for change in ("local set=Players[0].SetProperty;Players[0].SetProperty=function(o,k,v)if k~='SPC_CREW_ACTION_RECEIPTS_V1'then set(o,k,v)end end", "local get=Players[0].GetUnits;Players[0].GetUnits=function()local u=get();u.Destroy=function()end;return u end"):
   with self.subTest(change=change):
    l=self.fixture();l.execute("local c=C.make();local p=C.begin(c);C.complete(c,p);C.actions(c);"+change+";local out=C.use(c,C.units[20001],'x');assert(out:find('HELD') and #c:GetBuildQueue().adds==0);shared.UnitActions.Run(0,{Action='UNIT_ACTION_CONFIRM',UnitID=20001,PlanToken='x'});assert(#c:GetBuildQueue().adds==0)")
 def test_injection_throw_does_not_retry(self):
  l=self.fixture();l.execute("local c=C.make();local p=C.begin(c);C.complete(c,p);C.actions(c);local q=c:GetBuildQueue();q.AddProgress=function(_,n)q.adds[#q.adds+1]=n;error('native failure')end;assert(C.use(c,C.units[20001],'x'):find('HELD'));shared.UnitActions.Run(0,{Action='UNIT_ACTION_CONFIRM',UnitID=20001,PlanToken='x'});assert(#q.adds==1 and not C.units[20001])")

class ActualTargets(unittest.TestCase):
 def test_only_current_owned_wonder_plot_is_target_no_district_or_building(self):
  l=crew_runtime();l.execute((M/'UnitTargets.lua').read_text());l.execute(r"""
   local c=C.make();local p=C.begin(c);C.complete(c,p)
   C.rows.Districts=C.rows.Districts or {};C.rows.Districts.DISTRICT_WONDER={Index=999}
   P.Count=function()end;c.GetName=function()return 'Source'end
   local q=c:GetBuildQueue();q.target='BUILDING_WONDER_2';q.CurrentlyBuilding=function()return q.target end
   Players[0].GetDistricts=function()return {Members=function()return function()end end}end
   local plot={GetOwner=function()return 0 end,GetIndex=function()return 500 end,GetDistrictType=function()return 999 end,
    GetProperty=function()return P.Info('Buildings','BUILDING_WONDER_2').Index end}
   Map={GetPlotByIndex=function(id)if id==500 then return plot end end}
   Cities={GetPlotPurchaseCity=function()return c end}
   ExposedMembers.DLHD={Utils={GetCityPlots=function()return {500,500}end}}
   SPCUnitTargets.Start(P,shared)
   shared.UnitTargets.Refresh(0,{UnitID=20001,Token='wonder'})
   assert(not shared.UnitTargetSnapshot.error and #shared.UnitTargetSnapshot.plots==1)
   q.target='BUILDING_A';shared.UnitTargets.Refresh(0,{UnitID=20001,Token='ordinary'});assert(#shared.UnitTargetSnapshot.plots==0)
   q.target='BUILDING_WONDER_2';plot.GetOwner=function()return 3 end
   shared.UnitTargets.Refresh(0,{UnitID=20001,Token='foreign'});assert(#shared.UnitTargetSnapshot.plots==0)
  """)

class Database(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.db=sqlite3.connect(':memory:')
  source=sqlite3.connect(external_database(R).as_uri()+'?mode=ro',uri=True)
  try:source.backup(cls.db)
  finally:source.close()
  db=cls.db
  db.create_function('Make_Hash',1,lambda s:zlib.crc32(s.encode()) if s else 0)
  # Remove only this batch's definitions in the in-memory copy for repeat runs.
  projects=[r[0] for r in db.execute("select ProjectType from Projects where ProjectType like 'PROJECT_SPC_CREW_%'")]
  for x in projects:
   db.execute('delete from ProjectCompletionModifiers where ProjectType=?',(x,));db.execute('delete from Projects where ProjectType=?',(x,));db.execute('delete from Types where Type=?',(x,))
  buildings=[r[0] for r in db.execute("select BuildingType from Buildings where BuildingType='BUILDING_SPC_CREW_PROJECT_ACCESS' or BuildingType like 'BUILDING_SPC_CREW_ACCESS_%'")]
  for x in buildings:db.execute('delete from Buildings where BuildingType=?',(x,));db.execute('delete from Types where Type=?',(x,))
  for base in (250,420,750,1000,1360):
   x='UNIT_SPC_CREW_'+str(base);db.execute('delete from Units where UnitType=?',(x,));db.execute('delete from Types where Type=?',(x,))
  db.executescript((M/'Data/CrewProjects.sql').read_text());db.executescript((M/'Data/Crew.sql').read_text())
 def test_loaded_speed_matrix_matches_locked_integer_and_native_base_cost(self):
  l=crew_runtime();m=l.globals().SPCCrewModel
  for speed, in self.db.execute('select distinct CostMultiplier from GameSpeeds'):
   for tier in range(1,6):
    for ratio in (150,140,130,120):
     with self.subTest(speed=speed,tier=tier,ratio=ratio):
      project=m.Project(tier,ratio,speed)
      cost=self.db.execute('select Cost from Projects where ProjectType=?',(project,)).fetchone()[0]
      self.assertEqual(cost*speed//100,m.Cost(tier,ratio,speed))
      self.assertEqual(m.Parse(project), (tier,ratio))
 def test_native_grant_is_retired_and_protection_attribute_is_present(self):
  self.assertEqual(self.db.execute("select count(*) from ProjectCompletionModifiers where ProjectType like 'PROJECT_SPC_CREW_%'").fetchone()[0],0)
  rows=list(self.db.execute("select CanTrain,CanCapture,CanRetreatWhenCaptured,BuildCharges from Units where UnitType like 'UNIT_SPC_CREW_%'"))
  self.assertEqual(rows,[(0,0,1,1)]*5)

if __name__=='__main__':unittest.main()
