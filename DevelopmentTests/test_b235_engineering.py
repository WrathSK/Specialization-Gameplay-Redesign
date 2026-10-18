"""B235 scoped L3: actual Store, study transaction and projection sources.
Native yield/price/turn acceptance is not claimed by these fixtures.
"""
from pathlib import Path
import json
import sqlite3
import unittest
import xml.etree.ElementTree as ET
from lupa.lua55 import LuaRuntime
from test_industry_history import runtime
import test_b234_standardization as baseline
from test_b234_standardization import SETUP, lua
R=Path(__file__).resolve().parents[1];M=R/'Mod'

STUDY=r'''
S={};local queues={}
function S.install()
 local currentInfo=P.Info
P.Info=function(t,k)
 if t=='Projects' and (k==9001 or k=='PROJECT_SPC_ENGINEERING_STUDY')then return {Index=9001,Hash=9001,ProjectType='PROJECT_SPC_ENGINEERING_STUDY'}end
 if t=='Buildings' and k=='BUILDING_SPC_ENGINEERING_STUDY_ACCESS'then return {Index=9002,InternalOnly=1}end
 return currentInfo(t,k)
end
P.Call=function(o,k,...)if type(o and o[k])~='function'then return false end;return pcall(o[k],o,...)end
P.Field=function(o,k)return o and o[k]end
P.CreateBuilding=function(q,id)q.city.buildings[id]=true end
P.RemoveBuilding=function(b,id)b.RemoveBuilding(id)end
local oldRead=shared.EffectiveFacts.Read
shared.EffectiveFacts.Read=function(pid,c)
 local f=oldRead(pid,c);if S.unknown then f.activeStatus='UNKNOWN'end
 if S.exit then f.specialization='COMMERCE'end
 if S.pending then f.investmentPending=true end
 return f
end
end
S.install()
function S.queue(c)
 local q={city=c,target=nil,finishes=0};queues[c]=q
 c.GetBuildQueue=function()return q end
 local b={HasBuilding=function(_,id)return c.buildings[id]==true end,RemoveBuilding=function(id)c.buildings[id]=nil end}
 c.GetBuildings=function()return b end
 q.CurrentlyBuilding=function()return q.target end;q.GetSize=function()return q.target and 1 or 0 end
 q.FinishProgress=function()
  q.finishes=q.finishes+1
  if S.finishThrow then error('native failure')end
  q.target=nil;Events.CityProductionChanged.Fire(0,c:GetID())
  if not S.missingCompletion then Events.CityProjectCompleted.Fire(0,c:GetID(),9001)end
 end
 return q
end
function S.setup()
 S.install()
 SPCEngineeringStudyProjects.Start(P,shared);study=shared.EngineeringStudy
 shared.StandardizationEffects={SourceChanged=function(pid,id)S.notifications=(S.notifications or 0)+1 end}
 Events.GameCoreEventPublishComplete.Fire()
end
function S.make()
 local c=H.newIndustry();T.governor(4);for i=1,3 do T.invest(c,8000+i)end
 S.queue(c);H.wonder(c,1);H.wonder(c,3);S.setup();return c
end
function S.state(c)return shared.CityProgressionStore.EngineeringState(0,c)end
function S.L(c)local s=S.state(c);return s.value and s.value.L or 0 end
function S.begin(c)
 queues[c].target='PROJECT_SPC_ENGINEERING_STUDY';Events.CityProductionChanged.Fire(0,c:GetID())
 study.Request(0,{CityID=c:GetID(),StartTurn=Game.GetCurrentGameTurn()})
end
function S.endturn()Events.PlayerTurnDeactivated.Fire(0);T.turn(1);Events.GameCoreEventPublishComplete.Fire()end
function S.cancel(c)
 queues[c].target='BUILDING_A';Events.CityProductionChanged.Fire(0,c:GetID());Events.GameCoreEventPublishComplete.Fire()
end
function S.finishes(c)return queues[c].finishes end
function S.reload(c)
 H.reload();S.queue(c);S.setup()
end
'''
def study_runtime():
 l=runtime();l.execute((M/'EngineeringStudyProjects.lua').read_text());l.execute(STUDY);return l
class Study(unittest.TestCase):
 def check(self,s):study_runtime().execute(s)
 def test_full_turn_two_successes_then_L_equals_E(self):
  self.check("local c=S.make();assert(S.L(c)==0);S.begin(c);assert(S.L(c)==0 and S.state(c).value.pending);Events.PlayerTurnActivated.Fire(0);assert(S.finishes(c)==0);S.endturn();assert(S.L(c)==1 and S.finishes(c)==1 and S.notifications==1);S.begin(c);S.endturn();assert(S.L(c)==2 and S.finishes(c)==2);S.begin(c);assert(not S.state(c).value.pending);S.endturn();assert(S.L(c)==2)")
 def test_confirmed_E_change_publishes_access_without_panel(self):
  self.check("local c=H.newIndustry();T.governor(4);for i=1,3 do T.invest(c,8000+i)end;S.queue(c);S.setup();H.wonder(c,1);Events.GameCoreEventPublishComplete.Fire();assert(c.buildings[9002]);S.begin(c);S.endturn();assert(S.L(c)==1 and not c.buildings[9002]);H.wonder(c,3);Events.GameCoreEventPublishComplete.Fire();assert(c.buildings[9002] and study.views['0:'..c:GetID()].E==2);S.begin(c);S.endturn();assert(S.L(c)==2 and not c.buildings[9002]);H.wonder(c,4);Events.GameCoreEventPublishComplete.Fire();assert(study.views['0:'..c:GetID()].reason=='EST_E_UNKNOWN' and not c.buildings[9002])")
 def test_noncompleted_population_other_city_unaffected(self):
  self.check("local c=S.make();local other=H.city(2);local before=T.encode(T.record(other));S.begin(c);S.endturn();assert(T.encode(T.record(other))==before)")
 def test_cancel_then_restart_requires_full_turn(self):
  self.check("local c=S.make();S.begin(c);S.cancel(c);assert(not S.state(c).value.pending and S.L(c)==0);S.endturn();assert(S.finishes(c)==0);S.begin(c);S.endturn();assert(S.L(c)==1)")
 def test_same_publish_away_and_back_cancels(self):
  self.check("local c=S.make();S.begin(c);local q=c:GetBuildQueue();q.target='BUILDING_A';Events.CityProductionChanged.Fire(0,c:GetID());q.target='PROJECT_SPC_ENGINEERING_STUDY';Events.CityProductionChanged.Fire(0,c:GetID());Events.GameCoreEventPublishComplete.Fire();assert(not S.state(c).value.pending);S.endturn();assert(S.L(c)==0)")
 def test_active_loss_return_does_not_resume_old_round(self):
  self.check("local c=S.make();S.begin(c);S.endturn();S.begin(c);T.governor(3);Events.GovernorChanged.Fire(0);T.governor(4);Events.GovernorChanged.Fire(0);Events.GameCoreEventPublishComplete.Fire();S.endturn();assert(S.L(c)==1 and not S.state(c).value.pending);S.begin(c);S.endturn();assert(S.L(c)==2)")
 def test_identity_exit_cancels_without_erasing_history(self):
  self.check("local c=S.make();S.begin(c);S.endturn();S.begin(c);S.exit=true;study.Refresh(0,c:GetID());assert(S.L(c)==1 and not S.state(c).value.pending)")
 def test_pending_investment_does_not_finish(self):
  self.check("local c=S.make();S.begin(c);S.pending=true;S.endturn();assert(S.L(c)==0 and S.finishes(c)==0)")
 def test_duplicate_completion_cannot_add_L(self):
  self.check("local c=S.make();S.begin(c);S.endturn();local before=T.encode(T.record(c));Events.CityProjectCompleted.Fire(0,c:GetID(),9001);Events.PlayerTurnActivated.Fire(0);assert(T.encode(T.record(c))==before and S.L(c)==1)")
 def test_premature_native_completion_does_not_award_full_turn(self):
  self.check("local c=S.make();S.begin(c);c:GetBuildQueue():FinishProgress();Events.GameCoreEventPublishComplete.Fire();assert(S.L(c)==0 and S.state(c).value.pending.stage=='HELD')")
 def test_native_missing_or_failed_receipt_is_not_replayed(self):
  for failure in ('missingCompletion','finishThrow'):
   with self.subTest(failure=failure):self.check("local c=S.make();S.begin(c);S.%s=true;S.endturn();Events.PlayerTurnActivated.Fire(0);S.endturn();assert(S.L(c)==0 and S.finishes(c)==1);S.cancel(c);assert(not S.state(c).value.pending)"%failure)
 def test_coldload_restores_completed_and_active_round(self):
  self.check("local c=S.make();S.begin(c);S.endturn();local before=T.encode(S.state(c).value);S.reload(c);assert(T.encode(S.state(c).value)==before);S.begin(c);local q=c:GetBuildQueue();H.reload();S.queue(c).target=q.target;S.setup();S.endturn();assert(S.L(c)==2)")
 def test_coldload_calling_no_native_replay(self):
  self.check("local c=S.make();S.begin(c);S.missingCompletion=true;S.endturn();H.reload();local q=S.queue(c);q.target='PROJECT_SPC_ENGINEERING_STUDY';S.setup();Events.PlayerTurnActivated.Fire(0);Events.CityProjectCompleted.Fire(0,c:GetID(),9001);assert(S.L(c)==0 and q.finishes==0 and S.state(c).value.pending.stage=='HELD')")
 def test_owner_loss_cancels_only_pending(self):
  self.check("local c=S.make();S.begin(c);S.endturn();S.begin(c);T.loss(c,3,55);local r=T.record(c);assert(r.stage=='HELD_TRANSFER' and r.engineering.L==1 and r.engineering.pending==nil)")
 def test_initialized_empty_and_missing_known_are_distinct(self):
  self.check("local c=S.make();local store=shared.CityProgressionStore;local v=SPCEngineeringStudyModel.New();store.WriteEngineering(0,c,nil,v);S.reload(c);assert(S.state(c).value.L==0);T.record(c).engineering=nil;H.reload();assert(not pcall(shared.CityProgressionStore.EngineeringState,0,c))")
 def test_corrupt_receipt_not_reconstructed_from_E(self):
  self.check("local c=S.make();S.begin(c);S.endturn();T.record(c).engineering.receipts={};H.reload();assert(not pcall(shared.CityProgressionStore.EngineeringState,0,c))")
 def test_L_above_current_E_preserved(self):
  self.check("local c=S.make();S.begin(c);S.endturn();S.begin(c);S.endturn();shared.IndustryHistory.Credit=function()return {E=0,known=true}end;study.Refresh(0,c:GetID());assert(S.L(c)==2 and not c.buildings[9002])")
 def test_store_stale_readback_and_reentrant_reader(self):
  self.check("local c=S.make();local st=shared.CityProgressionStore;local old=st.EngineeringState(0,c);local setter=Game.SetProperty;local blocked=false;Game.SetProperty=function(o,k,v)if k==T.key(c)then blocked=not pcall(st.EngineeringState,0,c)end;return setter(o,k,v)end;st.WriteEngineering(0,c,old.value,SPCEngineeringStudyModel.New());assert(blocked);assert(not pcall(st.WriteEngineering,0,c,old.value,SPCEngineeringStudyModel.New()))")
 def test_store_failed_write_never_publishes_L(self):
  for mode in ('drop','third','throw'):
   with self.subTest(mode=mode):self.check("""
local c=S.make();S.begin(c);Events.PlayerTurnDeactivated.Fire(0)
local setter=Game.SetProperty;Game.SetProperty=function(o,k,v)
 if k==T.key(c) and v.engineering and v.engineering.L==1 then
  if '%s'=='drop'then return elseif '%s'=='third'then T.propsSet(k,{bad=true});return else error('write failed')end
 end;return setter(o,k,v)
end
T.turn(1);assert(not pcall(S.L,c));assert(not S.notifications);assert(S.finishes(c)==1)
"""%(mode,mode))

 def test_unknown_access_retained_without_reward(self):
  self.check("local c=S.make();S.begin(c);S.unknown=true;study.Refresh(0,c:GetID());assert(c.buildings[9002] and S.state(c).value.pending);S.endturn();assert(S.L(c)==0 and S.finishes(c)==0)")
 def test_original_owner_recapture_restores_L_without_pending(self):
  self.check("local c=S.make();S.begin(c);S.endturn();S.begin(c);T.loss(c,3,450);shared.CityProgressionStore.ExitConfirmed();c.s.ref.owner=0;c.s.ref.cityID=500;Events.CityTransfered.Fire(0,500,3);assert(S.L(c)==1 and not S.state(c).value.pending)")

 def test_second_loss_after_changed_id_clears_current_view(self):
  self.check("local c=S.make();S.begin(c);S.endturn();T.loss(c,3,450);shared.CityProgressionStore.ExitConfirmed();c.s.ref.owner=0;c.s.ref.cityID=500;Events.CityTransfered.Fire(0,500,3);S.begin(c);assert(study.views['0:500']);T.loss(c,3,550);assert(study.views['0:500']==nil and T.record(c).engineering.L==1 and not T.record(c).engineering.pending)")

class Projection(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  baseline.Standardization.setUpClass();cls.db=baseline.Standardization.db;cls.tables=dict(baseline.Standardization.tables)
  # Permit reruns after B235 has populated the configured native DB. Rebuild
  # only this batch's definitions in the in-memory copy, never the source DB.
  for table in ('SPC_StandardizationLevels','SPC_IndustryWonderEffects'):
   if cls.db.execute('select 1 from sqlite_master where name=?',(table,)).fetchone():
    carriers=[x[0] for x in cls.db.execute('select CarrierType from '+table)]
    for carrier in carriers:
     for modifier in (carrier,carrier+'_PURCHASE'):
      cls.db.execute('delete from ModifierArguments where ModifierId=?',(modifier,))
      cls.db.execute('delete from Modifiers where ModifierId=?',(modifier,))
     for t,c in (('BuildingModifiers','BuildingType'),('Buildings','BuildingType'),('Types','Type')):
      cls.db.execute('delete from '+t+' where '+c+'=?',(carrier,))
    cls.db.execute('drop table '+table)
  cls.db.execute("delete from Projects where ProjectType='PROJECT_SPC_ENGINEERING_STUDY'")
  cls.db.execute("delete from Buildings where BuildingType='BUILDING_SPC_ENGINEERING_STUDY_ACCESS'")
  cls.db.execute("delete from DynamicModifiers where ModifierType='MODIFIER_SPC_CITY_WONDER_ERA_PRODUCTION'")
  cls.db.execute("delete from Types where Type in ('PROJECT_SPC_ENGINEERING_STUDY','BUILDING_SPC_ENGINEERING_STUDY_ACCESS','MODIFIER_SPC_CITY_WONDER_ERA_PRODUCTION')")
  cls.db.executescript((M/'Data/EngineeringStudy.sql').read_text())
  for t in ('Buildings','SPC_StandardizationLevels','SPC_IndustryWonderEffects','Eras'):
   cls.tables[t]=[dict(r) for r in cls.db.execute('SELECT rowid AS "Index",* FROM '+t)]
 @classmethod
 def tearDownClass(cls):cls.db.close()
 def setUp(self):
  self.l=LuaRuntime(unpack_returned_tuples=True);self.l.globals().include=lambda n:self.l.execute((M/(n+'.lua')).read_text())
  self.l.execute('DB='+lua(self.tables));self.l.execute(SETUP)
  self.l.execute("print=function()end;levels={};historyUnknown={};shared.CityProgressionStore.EngineeringState=function(pid,c)assert(not historyUnknown[c.id],'EST_HISTORY_UNAVAILABLE');return {token=c.token,value={L=levels[c.id] or 0}}end;for _,f in pairs(facts)do f.activeStatus='KNOWN'end")
  for n in ('StandardizationCatalog','StandardizationDiscount','CopyYields','StandardizationEffects','IndustryWonderEffects'):self.l.execute((M/(n+'.lua')).read_text())
 def check(self,s):self.l.execute(s)
 def test_per_template_holder_max_not_nonholder(self):
  self.check("industry(1,4);levels[1]=7;learn(1,'BUILDING_UNIVERSITY');industry(2,4);levels[2]=2;learn(2,'BUILDING_BANK');industry(3,4);levels[3]=5;learn(3,'BUILDING_FACTORY');recipients[4]={[1]=true,[2]=true,[3]=true};start();local a=d.records['0:4'].applied;assert(a['BUILDING:BUILDING_UNIVERSITY']==24 and a['BUILDING:BUILDING_BANK']==14 and a['BUILDING:BUILDING_FACTORY']==20)")
 def test_final_value_replacement_and_iii_downgrade(self):
  self.check("industry(1,4);learn(1,'BUILDING_GRANARY');start();levels[1]=1;d.SourceChanged(0,1);assert(not has(1,'BUILDING','BUILDING_GRANARY'));local id=P.Info('Buildings','BUILDING_SPC_STD_BASE_B_BUILDING_GRANARY_L1').Index;assert(cities[1].built[id]);levels[1]=2;d.SourceChanged(0,1);assert(not cities[1].built[id]);industry(1,3);d.SourceChanged(0,1);assert(has(1,'BUILDING','BUILDING_GRANARY') and levels[1]==2)")
 def test_corrupt_L_holds_same_ref_only_then_recovers(self):
  self.check("industry(1,4);levels[1]=2;learn(1,'BUILDING_GRANARY');recipients[2]={[1]=true};start();historyUnknown[1]=true;d.SourceChanged(0,1);assert(d.records['0:2'].applied['BUILDING:BUILDING_GRANARY']==14);cities[1].token='NEW';d.SourceChanged(0,1);assert(not d.records['0:2'].applied['BUILDING:BUILDING_GRANARY'])")
 def test_missing_level_not_clamped(self):
  self.check("industry(1,4);levels[1]=100;learn(1,'BUILDING_GRANARY');start();assert(d.errors['0:1']=='STD_LEVEL_DEFINITION_MISSING' and levels[1]==100)")
 def test_duplicate_and_scope_retains_one_fact_read(self):
  self.check("industry(1,4);levels[1]=2;learn(1,'BUILDING_GRANARY');recipients[2]={[1]=true};start();local w=writes;factReads={};ledgerReads={};d.SourceChanged(0,1);assert(writes==w and factReads[1]==1 and ledgerReads[1]==1 and not factReads[3])")
 def test_exact_removal_failure_does_not_add_new_value(self):
  self.check("industry(1,4);learn(1,'BUILDING_GRANARY');start();removalFailure=P.Info('Buildings','BUILDING_SPC_STD_BASE_B_BUILDING_GRANARY').Index;levels[1]=1;d.SourceChanged(0,1);assert(d.errors['0:1']=='STD_REMOVE_UNCONFIRMED');assert(not cities[1].built[P.Info('Buildings','BUILDING_SPC_STD_BASE_B_BUILDING_GRANARY_L1').Index])")
 def test_sql_building_discount_and_district_no_broad_substitute(self):
  count=self.db.execute('select count(*) from Eras').fetchone()[0]
  self.assertEqual(self.db.execute('select max(Level) from SPC_StandardizationLevels').fetchone()[0],count)
  for r in self.db.execute('select * from SPC_StandardizationLevels'):
   args=dict(self.db.execute('select Name,Value from ModifierArguments where ModifierId=?',(r['CarrierType'],)))
   self.assertEqual(args['Amount'],str(10+2*r['Level']))
   discount=dict(self.db.execute('select Name,Value from ModifierArguments where ModifierId=?',(r['CarrierType']+'_PURCHASE',)))
   self.assertEqual(discount,{'BuildingType':r['TargetType'],'Amount':str(2*r['Level'])} if r['Kind']=='BUILDING' else {})
  self.assertFalse(self.db.execute("select 1 from Modifiers where ModifierId like 'BUILDING_SPC_STD%_L%_PURCHASE' and ModifierType like '%ALL%'").fetchall())
 def test_wonder_own_era_gap_and_no_current_era_bonus(self):
  self.check("P.Call=function(o,k,...)return pcall(o[k],o,...)end;local era='ERA_RENAISSANCE';P.Info=(function(old)return function(t,k)if t=='Eras'then for _,r in ipairs(DB.Eras)do if r.EraType==k then return r end end end;return old(t,k)end end)(P.Info);Players[0].GetEra=function()return era end;industry(1,4);SPCIndustryWonderEffects.Start(P,shared);local w=shared.IndustryWonderEffects;emit('LoadScreenClose');assert(not w.error and not w.errors['0:1']);local a=w.records['0:1'].applied;assert(a.BUILDING_SPC_WONDER_ERA_ANCIENT_30 and a.BUILDING_SPC_WONDER_ERA_CLASSICAL_20 and a.BUILDING_SPC_WONDER_ERA_MEDIEVAL_10);assert(not a.BUILDING_SPC_WONDER_ERA_RENAISSANCE_10);local n=writes;w.Refresh(0,1);assert(writes==n);industry(1,3);w.Refresh(0,1);assert(next(w.records['0:1'].applied)==nil);assert(not w.records['0:2'].applied.BUILDING_SPC_WONDER_ERA_ANCIENT_30)")
 def test_wonder_no_foreign_scan_and_exact_exit(self):
  self.check("P.Call=function(o,k,...)return pcall(o[k],o,...)end;P.Info=(function(old)return function(t,k)if t=='Eras'then for _,r in ipairs(DB.Eras)do if r.EraType==k then return r end end end;return old(t,k)end end)(P.Info);Players[0].GetEra=function()return 'ERA_RENAISSANCE'end;Players[64].GetCities=function()error('foreign city scan')end;industry(1,4);SPCIndustryWonderEffects.Start(P,shared);local w=shared.IndustryWonderEffects;emit('LoadScreenClose');assert(not w.error and not w.errors['0:1']);cities[1].owner=64;exits.IndustryWonderEffects(cities[1],{origin={owner=0,x=1,y=1}});assert(not w.records['0:1']);for _,r in ipairs(DB.SPC_IndustryWonderEffects)do assert(not cities[1].built[P.Info('Buildings',r.CarrierType).Index])end")
 def test_wonder_era_change_and_unknown_retention(self):
  self.check("P.Call=function(o,k,...)return pcall(o[k],o,...)end;local era='ERA_RENAISSANCE';P.Info=(function(old)return function(t,k)if t=='Eras'then for _,r in ipairs(DB.Eras)do if r.EraType==k then return r end end end;return old(t,k)end end)(P.Info);Players[0].GetEra=function()return era end;industry(1,4);SPCIndustryWonderEffects.Start(P,shared);local w=shared.IndustryWonderEffects;emit('LoadScreenClose');local old=P.Info('Buildings','BUILDING_SPC_WONDER_ERA_MEDIEVAL_10').Index;assert(cities[1].built[old]);facts[1].activeStatus='UNKNOWN';era='ERA_INDUSTRIAL';emit('PlayerTurnActivated',0);assert(cities[1].built[old] and w.errors['0:1']);facts[1].activeStatus='KNOWN';emit('PlayerTurnActivated',0);assert(not cities[1].built[old] and cities[1].built[P.Info('Buildings','BUILDING_SPC_WONDER_ERA_MEDIEVAL_20').Index] and not w.errors['0:1']);local n=writes;emit('PlayerTurnActivated',0);assert(writes==n)")
 def test_wonder_sql_native_scope(self):
  for r in self.db.execute('select * from SPC_IndustryWonderEffects'):
   a=dict(self.db.execute('select Name,Value from ModifierArguments where ModifierId=?',(r['CarrierType'],)))
   self.assertEqual(a,{'Amount':str(r['Amount']),'IsWonder':'1','StartEra':r['EraType'],'EndEra':r['EraType']})
  self.assertEqual(tuple(self.db.execute("select CollectionType,EffectType from DynamicModifiers where ModifierType='MODIFIER_SPC_CITY_WONDER_ERA_PRODUCTION'").fetchone()),('COLLECTION_OWNER','EFFECT_ADJUST_WONDER_ERA_PRODUCTION'))


class StudyUI(unittest.TestCase):
 def setUp(self):
  self.l=study_runtime();self.l.execute('c=S.make();ExposedMembers.SPC_P0=shared')
  def include(n):
   p=M/(n+'.lua')
   if not p.exists():p=M/'UI'/(n+'.lua')
   self.l.execute(p.read_text())
  self.l.globals().include=include
  self.l.execute((M/'UI/EngineeringStudyUI.lua').read_text())
  self.l.execute(r"""
Game.GetLocalPlayer=function()return 0 end
GameInfo.Projects={PROJECT_SPC_ENGINEERING_STUDY={Hash=9001}}
c:GetBuildQueue().GetCurrentProductionTypeHash=function()return c:GetBuildQueue().target=='PROJECT_SPC_ENGINEERING_STUDY' and 9001 or 0 end
PlayerOperations={EXECUTE_SCRIPT=1};sends=0;notifies=0
ui=SPCEngineeringStudyUI.New(P,function(pid,op,p)sends=sends+1;study.Request(pid,p)end,function()notifies=notifies+1 end)
""")
 def check(self,s):self.l.execute(s)
 def test_selection_waits_for_native_queue_then_sends_once(self):
  self.check("ui.Before(c,{Type='PROJECT_SPC_ENGINEERING_STUDY'},false);ui.Publish();assert(sends==0);c:GetBuildQueue().target='PROJECT_SPC_ENGINEERING_STUDY';ui.Publish();ui.Publish();assert(sends==1 and S.state(c).value.pending);assert(SPCEngineeringStudyUI.Text(0,c:GetID())=='1');S.endturn();assert(S.L(c)==1)")
 def test_load_current_target_is_not_start_intent(self):
  self.check("c:GetBuildQueue().target='PROJECT_SPC_ENGINEERING_STUDY';for i=1,20 do ui.Publish()end;assert(sends==0 and S.state(c).value==nil)")
 def test_queue_and_interrupted_click_not_submitted(self):
  self.check("assert(not ui.Before(c,{Type='PROJECT_SPC_ENGINEERING_STUDY'},true));ui.Before(c,{Type='PROJECT_SPC_ENGINEERING_STUDY'},false);ui.Before(c,{Type='NORMAL'},false);c:GetBuildQueue().target='PROJECT_SPC_ENGINEERING_STUDY';ui.Publish();assert(sends==0)")
 def test_no_work_on_unchanged_publish_and_owned_display_only(self):
  self.check("ui.Publish();local n=notifies;for i=1,100 do ui.Publish()end;assert(notifies==n and sends==0)")
  self.l.execute((M/'UI/TimedProjectDisplay.lua').read_text())
  self.check("local list={Owner=0,City=c,ProjectItems={{Type='PROJECT_SPC_ENGINEERING_STUDY',TurnsLeft=99999},{Type='NORMAL',TurnsLeft=9,Progress=20}}};SPCTimedProjectDisplay.Items(list);assert(list.ProjectItems[1].TurnsLeft=='1' and list.ProjectItems[2].TurnsLeft==9 and list.ProjectItems[2].Progress==20)")

class Package(unittest.TestCase):
 def test_project_and_exact_files(self):
  root=ET.parse(M/'SpecializationP0.modinfo').getroot();self.assertEqual(root.attrib['version'],'262')
  files=[x.text for x in root.find('Files')];self.assertEqual(len(files),len(set(files)))
  for p in ('EngineeringStudyModel.lua','EngineeringStudyProjects.lua','IndustryWonderEffects.lua','Data/EngineeringStudy.sql','Text/EngineeringStudy.sql','UI/EngineeringStudyUI.lua'):self.assertIn(p,files)
 def test_no_scheduled_poll_or_progress_injection(self):
  for p in ('EngineeringStudyProjects.lua','IndustryWonderEffects.lua','UI/EngineeringStudyUI.lua'):
   s=(M/p).read_text()
   for forbidden in ('SystemUpdateUI','SetUpdate','AddProgress','ChangeProgress','collectgarbage','RequestCommand'):self.assertNotIn(forbidden,s)

if __name__=='__main__':unittest.main()
