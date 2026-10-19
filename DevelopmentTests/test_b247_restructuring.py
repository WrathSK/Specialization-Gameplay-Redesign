"""B247 L3: actual Store, native-action coordinator, inheritance and failure seams.
No native UI, safe-retreat, actual growth/yield or real save-file PASS implied.
"""
from pathlib import Path
import unittest
from test_store_write_boundaries import fixture
R=Path(__file__).resolve().parents[1]
SETUP=r'''
T.start();ExposedMembers={};GameConfiguration.GetGameSpeedType=function()return 'GAMESPEED_STANDARD'end
GameInfo.GameSpeeds={GAMESPEED_STANDARD={GameSpeedType='GAMESPEED_STANDARD',CostMultiplier=100}}
local function event()local f={};return {Add=function(x)f[#f+1]=x end,Fire=function(...)for _,x in ipairs(f)do x(...)end end}end
for _,n in ipairs({'GameCoreEventPublishComplete','UnitAddedToMap','CityProductionCompleted','UnitMoveComplete','UnitMovementPointsChanged'})do Events[n]=Events[n] or event()end
P.Family=function(t)return P.Families[t]end
local info=P.Info
P.Info=function(tab,id)
 if tab=='Buildings' and type(id)=='string' and id:match('^BUILDING_SPC_')then return {Index=id,BuildingType=id,InternalOnly=1}end
 if tab=='Units' and id==247 then return {UnitType='UNIT_SPC_RESTRUCTURING_TEAM',Index=247}end
 return info(tab,id)
end
P.HasBuilding=function(b,id)return b[id]==true end
P.CreateBuilding=function(b,id)if not markerFail then b[id]=true end end
P.RemoveBuilding=function(b,id)if not markerFail then b[id]=nil end end
Z={units={},kills=0,published={}};local oldUnits=Players[0]:GetUnits()
Players[0].GetUnits=function()return {
 FindID=function(_,id)return Z.units[id] or oldUnits:FindID(id)end,
 Members=function()return pairs(Z.units)end,
 Destroy=function(_,u)
  local id=u.GetID and u:GetID() or u.id
  if Z.units[id]then Z.kills=Z.kills+1;if not destroyFail then Z.units[id]=nil end
  else oldUnits:Destroy(u)end
 end}end
function Z.equip(c)
 c.markers=c.markers or {};c.GetName=function()return 'Test city'end
 c.GetBuildings=function()return c.markers end;c.GetBuildQueue=function()return c.markers end
end
function Z.city(i,kind,level)
 local c=T.fresh(i);T.register(c);T.complete(c,kind)
 for j=1,level-1 do T.invest(c,9000+i*10+j)end
 Z.equip(c)
 for _,d in Players[0]:GetDistricts():Members()do if d:GetCity()==c then d.GetX=function()return c:GetX()end;d.GetY=function()return c:GetY()end;d.IsPillaged=function()return false end end end
 return c
end
c=Z.city(1,'DISTRICT_CAMPUS',4);source=Z.city(2,'DISTRICT_COMMERCIAL_HUB',4);other=Z.city(3,'DISTRICT_THEATER',2)
second=T.district(c,'DISTRICT_THEATER',501,true);second.GetX=function()return c:GetX()+1 end;second.GetY=function()return c:GetY()end;second.IsPillaged=function()return false end
function Z.team(id,trained)
 local u={id=id,x=c:GetX(),y=c:GetY(),properties={}}
 u.GetID=function()return id end;u.GetOwner=function()return 0 end;u.GetType=function()return 247 end
 u.GetX=function()return u.x end;u.GetY=function()return u.y end
 u.GetProperty=function(_,k)return u.properties[k]end;u.SetProperty=function(_,k,v)u.properties[k]=SPCRestructuringModel.Copy(v)end
 if trained~=false then u.properties.SPC_RESTRUCTURING_TEAM_V1={version=1,owner=0,id=id,uid='TEAM:'..id,source=shared.CityProgressionStore.HistoricalReference(source)}end
 Z.units[id]=u;return u
end
u=Z.team(400);team={owner=0,id=400,uid='TEAM:400'}
function Z.st()return shared.CityProgressionStore end
function Z.state()return Z.st().RestructuringState(0,c)end
function Z.begin()return Z.st().BeginRestructuring(0,c,team,'LIQUIDATE',T.now())end
function Z.configure(kind)
 return Z.st().ConfigureRestructuring(0,c,team,kind or 'CULTURE',{districtID=501,type='DISTRICT_THEATER',turn=T.now()})
end
function Z.finish()
 Z.units[400]=nil;Z.st().ConfirmRestructuringConsumption(0,c,team);Z.st().FinishRestructuring(0,c,team)
end
function Z.service()
 SPCRestructuring.Start(P,shared);svc=shared.Restructuring;Events.LoadScreenClose.Fire()
end
function Z.command(action,token,plan)
 svc.Request(0,{Action=action,UnitID=400,Token=token or action,PlanToken=plan});return svc.lastRequest
end
function Z.run()
 Z.command('REST_PREPARE','preview');assert(svc.views['0:400'].prepared=='preview',svc.views['0:400'].reason)
 return Z.command('REST_CONFIRM','commit','preview')
end
'''
def runtime(service=False):
 l=fixture();l.globals().include('Restructuring');l.execute(SETUP)
 if service:l.execute('Z.service()')
 return l

class Store(unittest.TestCase):
 def check(self,s):runtime().execute(s)
 def test_liquidate_debits_once_keeps_original_receipts_and_pauses_tradition(self):
  self.check("local old=T.encode(T.record(c).investment);local age=T.record(c).researchTradition.age;Z.begin();local f=T.control(c);assert(f.potential==3 and f.active==0 and f.specialization=='NONE' and f.progression=='REALLOCATING');assert(T.encode(T.record(c).investment)==old);assert(T.record(c).researchTradition.state=='PAUSED_IDENTITY');local writes=T.writes();Z.begin();assert(T.writes()==writes);for i=1,5 do T.turn(1)end;assert(T.record(c).researchTradition.age==age)")
 def test_five_turns_never_auto_complete_and_configure_consumes_only_on_proof(self):
  self.check("Z.begin();T.turn(4);assert(not pcall(Z.configure));T.turn(1);assert(Z.state().phase=='REALLOCATING');Z.configure();assert(not pcall(Z.st().FinishRestructuring,0,c,team));Z.finish();assert(T.control(c).specialization=='CULTURE' and T.control(c).potential==3);assert(T.record(c).researchTradition);local w=T.writes();assert(Z.st().FinishRestructuring(0,c,team)==false and T.writes()==w)")
 def test_coldload_realallocating_does_not_debit_again(self):
  self.check("Z.begin();T.turn(1);local v=T.encode(Z.state());local inv=T.encode(T.record(c).investment);T.reload();assert(T.encode(Z.state())==v and T.encode(T.record(c).investment)==inv);assert(T.control(c).active==0 and T.control(c).potential==3)")
 def test_new_settler_epoch_reaches_four_without_reset_old_receipts(self):
  self.check("Z.begin();for i=1,5 do T.turn(1)end;Z.configure();Z.finish();T.invest(c,19001);assert(T.control(c).potential==4 and T.control(c).investmentCount==1 and T.control(c).basePotential==3);assert(SPCRestructuringModel.Count(T.record(c).investment)==3);T.reload();assert(T.control(c).potential==4)")
 def test_repeated_restructuring_retains_post_epoch_investment_receipts(self):
  self.check("Z.begin();for i=1,5 do T.turn(1)end;Z.configure();Z.finish();T.invest(c,19001);local epoch=T.encode(Z.state().investment);local team2={owner=0,id=401,uid='TEAM:401'};Z.st().BeginRestructuring(0,c,team2,'SECOND');assert(Z.state().serial==2 and T.encode(Z.state().epochs[1].investment)==epoch and T.control(c).potential==3)")
 def test_research_return_resumes_history_without_catchup(self):
  self.check("T.turn(1);local age=T.record(c).researchTradition.age;Z.begin();for i=1,5 do T.turn(1)end;Z.configure();Z.finish();local t={owner=0,id=401,uid='T401'};Z.st().BeginRestructuring(0,c,t,'SECOND');for i=1,5 do T.turn(1)end;Z.st().ConfigureRestructuring(0,c,t,'RESEARCH',{districtID=T.record(c).base.first.districtID,type='DISTRICT_CAMPUS',turn=T.now()});Z.st().ConfirmRestructuringConsumption(0,c,t);Z.st().FinishRestructuring(0,c,t);assert(T.record(c).researchTradition.age==age and T.record(c).researchTradition.state=='COUNTING');T.turn(1);assert(T.record(c).researchTradition.age==age+1)")
 def test_new_research_first_p4_receipt_uses_current_epoch_proof(self):
  self.check("c=other;u.x=c:GetX();u.y=c:GetY();T.invest(c,29001);T.invest(c,29002);Z.begin();for i=1,5 do T.turn(1)end;Z.st().ConfigureRestructuring(0,c,team,'RESEARCH',{districtID=601,type='DISTRICT_CAMPUS',turn=T.now()});Z.finish();assert(not T.record(c).researchTradition);T.invest(c,29003);assert(T.record(c).researchTradition.qualification and T.control(c).potential==4);T.reload();T.turn(1);assert(T.record(c).researchTradition.age==1)")
 def test_new_commerce_first_p4_and_reputation_reset(self):
  self.check("Z.begin();for i=1,5 do T.turn(1)end;Z.st().ConfigureRestructuring(0,c,team,'COMMERCE',{districtID=601,type='DISTRICT_COMMERCIAL_HUB',turn=T.now()});Z.finish();T.invest(c,29003);assert(T.record(c).commerce.reputation.qualification);T.turn(1);assert(T.record(c).commerce.reputation.age==1);Z.st().BeginRestructuring(0,c,{owner=0,id=401,uid='T401'},'SECOND');assert(not T.record(c).commerce.reputation and #T.record(c).commerce.selected==0);T.reload();assert(T.control(c).active==0)")
 def test_industry_first_entry_initializes_but_history_missing_not_rebuilt(self):
  self.check("Z.begin();for i=1,5 do T.turn(1)end;Z.st().ConfigureRestructuring(0,c,team,'INDUSTRY',{districtID=601,type='DISTRICT_INDUSTRIAL_ZONE',turn=T.now()});Z.finish();local v,p=Z.st().ReadTemplates(c);assert(v==nil and p and T.record(c).templateLifecycle.state=='UNINITIALIZED');T.reload();assert(T.control(c).specialization=='INDUSTRY')")
 def test_old_template_history_and_dialogue_engineering_completed_assets_preserved(self):
  self.check("local st=Z.st();local a=st.DialogueState(0,c);local v=SPCDialogueProjectModel.Begin(nil,a.token,a.reference,'ERA_CLASSICAL',T.now());st.WriteDialogue(0,c,nil,v);local e=SPCEngineeringStudyModel.Begin(nil,a.token,a.reference,T.now(),1);st.WriteEngineering(0,c,nil,e);Z.begin();assert(not st.DialogueState(0,c).value.pending and not st.EngineeringState(0,c).value.pending);assert(st.DialogueState(0,c).value.total==0 and st.EngineeringState(0,c).value.L==0)")
 def test_wrong_owner_and_other_city_isolation(self):
  self.check("local old=T.encode(T.record(other));assert(not pcall(Z.st().BeginRestructuring,3,c,team,'BAD'));Z.begin();assert(T.encode(T.record(other))==old);assert(not pcall(Z.st().ConfigureRestructuring,0,other,team,'RESEARCH',{districtID=1,type='DISTRICT_CAMPUS'}))")
 def test_failed_write_blocks_candidate_and_other_city_still_writable(self):
  for mode in ('drop','third','throw'):
   with self.subTest(mode=mode):self.check("local setter=Game.SetProperty;Game.SetProperty=function(o,k,v)if k==T.key(c) and v.restructuring then if '%s'=='drop'then return elseif '%s'=='third'then T.propsSet(k,{invalid=true});return else error('FAILED')end end;return setter(o,k,v)end;assert(not pcall(Z.begin));assert(not pcall(T.control,c));T.invest(other,39001);assert(T.control(other).potential==3)"%(mode,mode))
 def test_reentrant_read_cannot_publish_optimistic_identity(self):
  self.check("local setter=Game.SetProperty;local blocked=false;Game.SetProperty=function(o,k,v)if k==T.key(c) and v.restructuring then blocked=not pcall(T.control,c)end;return setter(o,k,v)end;Z.begin();assert(blocked and T.control(c).active==0)")
 def test_target_loss_discards_transaction_and_recapture_claims_current_candidates(self):
  self.check("Z.begin();Z.st().RegisterExit('Test',function()end);T.loss(c,3,450);assert(T.record(c).restructuring.phase=='DISCARDED');c.s.ref.owner=0;c.s.ref.cityID=500;Events.CityTransfered.Fire(0,500,3);assert(T.control(c).specialization=='NONE' and T.control(c).potential==0);local x=Z.st().ClaimState(0,c);assert(x.eligible and x.set.RESEARCH and x.set.CULTURE);Z.st().ClaimComplete(0,c,{kind='CULTURE',token=x.token,reference=x.reference,project='PROJECT_SPC_CLAIM_CULTURE',turn=T.now(),districtID=501,type='DISTRICT_THEATER'});assert(T.control(c).specialization=='CULTURE' and T.control(c).potential==1);assert(T.record(c).researchTradition)")
 def test_completed_restructuring_recapture_rebinds_new_identity(self):
  self.check("Z.begin();for i=1,5 do T.turn(1)end;Z.configure();Z.finish();Z.st().RegisterExit('Test',function()end);T.loss(c,3,450);c.s.ref.owner=0;c.s.ref.cityID=500;Events.CityTransfered.Fire(0,500,3);assert(T.control(c).specialization=='CULTURE' and T.control(c).potential==3);T.invest(c,29991);assert(T.control(c).potential==4)")
 def test_corrupt_transaction_never_restores_as_new_city(self):
  for mutate in ('s.potential=4','s.team.owner=3','s.phase="UNKNOWN"','s.identity="RESEARCH"'):
   with self.subTest(mutate=mutate):self.check('Z.begin();local s=T.record(c).restructuring;'+mutate+';T.reload();assert(not pcall(T.control,c))')

class Service(unittest.TestCase):
 def check(self,s):runtime(True).execute(s)
 def test_train_source_access_and_new_completed_team_binding(self):
  self.check("assert(source.markers.BUILDING_SPC_RESTRUCTURING_ACCESS);assert(not c.markers.BUILDING_SPC_RESTRUCTURING_ACCESS);local t=Z.team(401,false);t.x=source:GetX();t.y=source:GetY();Events.UnitAddedToMap.Fire(0,401);Events.CityProductionCompleted.Fire(0,source:GetID(),0,247,false);Events.GameCoreEventPublishComplete.Fire();local b=t:GetProperty(SPCRestructuringModel.UNIT_KEY);assert(b and b.source.token==Z.st().HistoricalReference(source).token)")
 def test_full_command_flow_exact_consumption_no_timer(self):
  self.check("assert(Z.run().ok);assert(T.control(c).potential==3 and c.markers.BUILDING_SPC_REALLOCATING);assert(u:GetProperty(SPCRestructuringModel.UNIT_KEY).target);u.x=second:GetX();u.y=second:GetY();assert(not svc.Read(0,400).legal);for i=1,5 do T.turn(1)end;assert(Z.run().ok);assert(T.control(c).specialization=='CULTURE' and not c.markers.BUILDING_SPC_REALLOCATING and Z.kills==1);Z.command('REST_CONFIRM','duplicate','preview');assert(Z.kills==1)")
 def test_no_configure_in_other_city_or_same_specialty(self):
  self.check("assert(Z.run().ok);for i=1,5 do T.turn(1)end;assert(not svc.Read(0,400).legal);u.x=other:GetX();u.y=other:GetY();assert(not svc.Read(0,400).legal and Z.kills==0)")
 def test_source_identity_exit_and_transfer_does_not_destroy_team(self):
  self.check("local b=T.encode(u:GetProperty(SPCRestructuringModel.UNIT_KEY));Z.st().BeginRestructuring(0,source,{owner=0,id=777,uid='other'},'sourceexit');svc.Flush();assert(Z.units[400] and T.encode(u:GetProperty(SPCRestructuringModel.UNIT_KEY))==b);T.loss(source,3,550);assert(Z.units[400] and Z.run().ok)")
 def test_target_transfer_destroys_bound_team_and_disruption_only(self):
  self.check("assert(Z.run().ok);T.loss(c,3,450);assert(not Z.units[400] and Z.kills==1 and not c.markers.BUILDING_SPC_REALLOCATING);assert(T.record(c).restructuring.phase=='DISCARDED' and T.record(c).researchTradition)")
 def test_destroy_failure_never_retries_or_grants_new_identity(self):
  self.check("assert(Z.run().ok);for i=1,5 do T.turn(1)end;u.x=second:GetX();destroyFail=true;assert(not Z.run().ok);assert(Z.kills==1 and Z.state().phase=='CONSUMING' and T.control(c).active==0);Z.command('REST_CONFIRM','repeat','preview');assert(Z.kills==1);Events.LoadScreenClose.Fire();assert(Z.kills==1 and Z.units[400] and not Z.state().consumed)")
 def test_final_write_failure_confirmed_consumption_can_finish_on_load(self):
  self.check("assert(Z.run().ok);for i=1,5 do T.turn(1)end;u.x=second:GetX();local setter=Game.SetProperty;Game.SetProperty=function(o,k,v)if k==T.key(c) and v.restructuring and v.restructuring.phase=='SETTLED' then return end;return setter(o,k,v)end;assert(not Z.run().ok and Z.kills==1);assert(T.record(c).restructuring.consumed);Game.SetProperty=setter;T.reload();Z.service();assert(T.control(c).specialization=='CULTURE' and not c.markers.BUILDING_SPC_REALLOCATING and Z.kills==1)")
 def test_unit_binding_failure_cannot_liquidate_second_city(self):
  self.check("u.SetProperty=function()end;assert(not Z.run().ok);assert(not Z.state() and T.control(c).potential==4)")
 def test_coldload_restores_disruption_and_one_time_binding(self):
  self.check("assert(Z.run().ok);local base=T.encode(Z.state());c.markers.BUILDING_SPC_REALLOCATING=nil;T.reload();Z.service();assert(T.encode(Z.state())==base and c.markers.BUILDING_SPC_REALLOCATING);assert(T.control(c).potential==3)")
 def test_projection_after_commit_not_before_and_does_not_delete_contract_effect(self):
  self.check("local seen={};shared.ResearchSupport={Audit=function(scope)seen[#seen+1]=T.control(c).specialization end};shared.NetworkBridge={Refresh=function(pid)assert(T.control(c).active==0)end};c.markers.BUILDING_SPC_DEVELOPMENT_DISTRICT_CAMPUS=true;assert(Z.run().ok);assert(seen[1]=='NONE' and c.markers.BUILDING_SPC_DEVELOPMENT_DISTRICT_CAMPUS)")

class ContractPreservation(unittest.TestCase):
 def test_signed_capital_and_development_survive_identity_exit_and_settle(self):
  from test_b246_development import runtime as contracts
  contracts().execute("assert(C.confirm());open();assert(sign());local ca=T.encode(C.contract());local de=T.encode(contract());local treasury=balance;shared.CityProgressionStore.BeginRestructuring(0,source,{owner=0,id=777,uid='contract-team'},'REST');assert(T.encode(C.contract())==ca and T.encode(contract())==de and balance==treasury);assert(not next(C.state().protection));dev.Reconcile(0);assert(active());cap.Refresh(0,source:GetID());assert(not C.view().canSign);open();assert(not view().canSign);reload();assert(active() and T.encode(contract())==de);T.turn(10);assert(C.contract().stage=='SETTLED' and contract().stage=='ACTIVE');research.markers[101]=true;dev.Reconcile(0);assert(contract().stage=='COMPLETED' and not active());assert(moneyCalls==3)")
 def test_target_identity_exit_does_not_terminate_development(self):
  from test_b246_development import runtime as contracts
  contracts().execute("assert(sign());local old=T.encode(contract());shared.CityProgressionStore.BeginRestructuring(0,research,{owner=0,id=777,uid='target-team'},'REST');dev.Reconcile(0);assert(active() and T.encode(contract())==old);research.markers[101]=true;dev.Reconcile(0);assert(not active() and contract().stage=='COMPLETED' and moneyCalls==1)")

class AdditionalStore(unittest.TestCase):
 def test_loss_after_consumed_receipt_before_finalization_discards(self):
  runtime().execute("Z.begin();T.turn(5);Z.configure();Z.units[400]=nil;Z.st().ConfirmRestructuringConsumption(0,c,team);Z.st().RegisterExit('Test',function()end);T.loss(c,3,450);assert(T.record(c).restructuring.phase=='DISCARDED' and not T.record(c).restructuring.consumed);T.reload();assert(T.record(c).stage=='HELD_TRANSFER')")
 def test_historical_institutions_survive_and_new_epoch_dates_do_not_replace_old(self):
  runtime().execute("Z.begin();assert(Z.st().InstitutionArchive(0,c).RESEARCH==4);T.turn(5);Z.configure();Z.finish();assert(Z.st().InstitutionHistory(0,c)[3]==5);assert(Z.st().InstitutionArchive(0,c).RESEARCH==4 and Z.st().InstitutionArchive(0,c).CULTURE==3);T.invest(c,59991);assert(Z.st().InstitutionHistory(0,c)[4]==5);T.reload();assert(Z.st().InstitutionArchive(0,c).CULTURE==4)")
 def test_zero_cross_record_checks_for_ordinary_restructuring_writes(self):
  runtime().execute("T.scanReset();Z.begin();T.turn(5);Z.configure();Z.finish();assert(T.scanCount()==0)")
 def test_reused_ui_receipt_different_team_is_not_an_old_success(self):
  runtime().execute("Z.begin();T.turn(5);Z.configure();Z.finish();local v=Z.st().BeginRestructuring(0,c,{owner=0,id=401,uid='next'},'LIQUIDATE');assert(v.serial==2 and T.control(c).potential==2)")
 def test_unknown_research_current_facts_do_not_touch_other_city(self):
  runtime().execute("T.governor(nil);local old=T.encode(T.record(other));Z.begin();assert(T.control(c).active==0 and T.encode(T.record(other))==old)")
 def test_history_templates_and_engineering_records_preserved_bytewise(self):
  runtime().execute("c=Z.city(4,'DISTRICT_INDUSTRIAL_ZONE',4);u.x=c:GetX();u.y=c:GetY();local r=T.record(c);local t={schema=1,uid='STD:'..r.base.token,foundation=r.base.token,x=c:GetX(),y=c:GetY(),initialized=true,revision=2,learned={BUILDING_TEST={district='DISTRICT_CAMPUS',tier=1,turn=0,evidence='OBSERVED'}}};Z.st().WriteTemplates(c,nil,t);local before=T.encode(T.record(c).templates);Z.begin();assert(T.encode(T.record(c).templates)==before);T.turn(5);Z.configure();Z.finish();assert(T.encode(T.record(c).templates)==before);T.reload();assert(T.encode(T.record(c).templates)==before)")
 def test_culture_dialogue_completed_history_preserved_and_pending_cancelled(self):
  runtime().execute("local a=Z.st().DialogueState(0,c);local v=SPCDialogueProjectModel.Begin(nil,a.token,a.reference,'ERA_CLASSICAL',T.now());local n=SPCDialogueProjectModel.Complete(v,v.pending.id,1,T.now());Z.st().WriteDialogue(0,c,nil,n);Z.begin();assert(Z.st().DialogueState(0,c).value.total==5 and Z.st().DialogueState(0,c).value.used.ERA_CLASSICAL);T.reload();assert(Z.st().DialogueState(0,c).value.total==5)")

class DirectIntegration(unittest.TestCase):
 def test_dispatcher_commits_current_identity_before_actual_support_and_network_capture(self):
  l=runtime(True);l.globals().include('ResearchSupport');l.globals().include('NetworkInput')
  l.execute("SPCResearchSupport.Start(P,shared);Events.LoadScreenClose.Fire();assert(c.markers.BUILDING_SPC_DEV_RESEARCH_SUPPORT);local cities=Players[0]:GetCities();Players[0].GetCities=function()cities.GetCapitalCity=function()return source end;return cities end;shared.NetworkBridge={Refresh=function(pid)networkInput=SPCNetworkInput.Capture(P,shared,pid,{},'EMPTY')end}")
  text=(R/'Mod/Gameplay.lua').read_text();a=text.index("  if type(params.Action)=='string' and params.Action:match('^REST_')");b=text.index("  if params.Action=='NETWORK_ISOLATE'",a)
  l.execute('function dispatch(playerID,params)'+text[a:b]+'end')
  l.execute("dispatch(0,{Action='REST_PREPARE',UnitID=400,Token='prepare'});dispatch(0,{Action='REST_CONFIRM',UnitID=400,Token='liquidate',PlanToken='prepare'});assert(svc.lastRequest.ok);assert(not c.markers.BUILDING_SPC_DEV_RESEARCH_SUPPORT and networkInput.cities[c:GetID()].specialization=='NONE' and networkInput.cities[c:GetID()].active==0);assert(other.markers.BUILDING_SPC_DEV_CULTURE_SUPPORT);T.turn(5);u.x=second:GetX();assert(Z.run().ok);assert(c.markers.BUILDING_SPC_DEV_CULTURE_SUPPORT and not c.markers.BUILDING_SPC_DEV_RESEARCH_SUPPORT);assert(networkInput.cities[c:GetID()].specialization=='CULTURE' and networkInput.cities[c:GetID()].active==3)")
 def test_readback_failure_does_not_publish_candidate_or_consume(self):
  runtime(True).execute("local pubs=0;shared.NetworkBridge={Refresh=function()pubs=pubs+1 end};T.failKey(T.key(c));assert(not Z.run().ok);assert(pubs==0 and Z.units[400] and Z.kills==0);assert(not pcall(T.control,c))")
 def test_settled_missing_native_receipt_is_rejected(self):
  runtime().execute("Z.begin();T.turn(5);Z.configure();Z.finish();T.record(c).restructuring.consumed=nil;T.reload();assert(not pcall(T.control,c))")

if __name__=='__main__':unittest.main()
