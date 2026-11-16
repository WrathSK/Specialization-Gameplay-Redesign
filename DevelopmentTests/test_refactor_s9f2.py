"""Fixed pure business transitions before actual Store deferred-evidence cutover."""
import unittest
from refactor_harness import ROOT,legacy_source_observation,measure
from test_refactor_s8b2 import fixture as ordinary
from test_refactor_s5d4c7 import fixture as tradition
from test_refactor_s9b1 import runtime as development
from test_refactor_s6e import observed,Profile
from test_refactor_s9f1 import fixture as model


def prepare(v,key,city='ca',returned=True,scope=True):
 with legacy_source_observation():
  v.globals().include('StoreDeferredLifecycle');v.globals().include('StoreLifecycleRecovery')
 v.execute("""
 key,cityName,want,back=...;city=assert(_G[cityName]);R=SPCStoreDeferredLifecycle;Recovery=SPCStoreLifecycleRecovery
 r=M.Copy(T.record(city));r.ownerChanges=1;r.stage='HELD_TRANSFER';r.current=nil
 r.loss={origin=M.Copy(r.origin),target={owner=9,cityID=900,x=r.origin.x,y=r.origin.y}}
 r.deferredLifecycle=R.Loss(nil,r,{[key]=want},10)
 if back then r.lastLoss=r.loss;r.loss=nil;r.stage='ACTIVE';r.current=M.Copy(r.origin);r.current.cityID=r.current.cityID+100;r.deferredLifecycle=R.Return(r.deferredLifecycle,r,{},20)end
 witness=R.Entry(r.deferredLifecycle,key,r)
 function plan(now)local before=T.encode(r);local writes=T.writes();local out=Recovery.Plan(r,key,witness,now or 30);assert(T.encode(r)==before and T.writes()==writes);return out end
 """,key,city,scope,returned)
 return v


class Scope(unittest.TestCase):
 def test_reputation_scope_survives_cycles_and_whole_owner_dominates(self):
  v=model();v.execute("v=M.Loss(nil,r,{commerce='REPUTATION'},1);assert(v.entries.commerce.scope=='REPUTATION');v=returned(2);v=loss(3,8,28);assert(v.entries.commerce.scope=='REPUTATION');v=M.Loss(v,r,{commerce=true},4);assert(v.entries.commerce.scope==nil);v=returned(5);v=M.Return(v,r,{commerce='REPUTATION'},6);assert(v.entries.commerce.scope==nil)")
 def test_return_only_narrow_scope_and_scope_bound_clear_witness(self):
  v=model();v.execute("r.stage='ACTIVE';r.lastLoss=r.loss;r.loss=nil;r.current={owner=0,cityID=19,x=4,y=5};v=M.Return(nil,r,{commerce='REPUTATION'},3);local e=M.Entry(v,'commerce',r);assert(e.scope=='REPUTATION');e.scope=nil;assert(not pcall(M.Clear,v,'commerce',e,r));assert(v.entries.commerce.scope=='REPUTATION')")
 def test_other_owners_or_unknown_scope_are_rejected(self):
  v=model();v.execute("assert(not pcall(M.Loss,nil,r,{researchTradition='REPUTATION'},1));v=M.Loss(nil,r,{commerce=true},1);v.entries.commerce.scope='OTHER';assert(not pcall(M.Validate,v,r));v.entries.commerce.scope='REPUTATION';v.entries.capital=v.entries.commerce;assert(not pcall(M.Validate,v,r))")


class PurePlans(unittest.TestCase):
 def test_tradition_keeps_origin_age_receipt_and_rebases_without_held_credit(self):
  v=prepare(tradition(),'researchTradition','c');v.execute("r.researchTradition.age=3;r.researchTradition.cursor=3;local old=M.Copy(r.researchTradition);local p=plan();assert(p.topic=='TRADITION'and p.set.researchTradition.age==3 and p.set.researchTradition.start==old.start and p.set.researchTradition.receipt==old.receipt and p.set.researchTradition.cursor==30 and p.set.researchTradition.state=='COUNTING'and p.nextEvidence==nil)")
 def test_tradition_other_identity_and_held_owner_keep_original_pause_rules(self):
  v=prepare(tradition(),'researchTradition','c',False);v.execute("local p=plan();assert(p.set.researchTradition.state=='OWNER_POLICY_UNRESOLVED'and p.set.researchTradition.age==r.researchTradition.age and p.set.researchTradition.cursor==r.researchTradition.cursor)")
  v=prepare(tradition(),'researchTradition','c');v.execute("r.base.specialization='CULTURE';local p=plan();assert(p.set.researchTradition.state=='PAUSED_IDENTITY'and p.set.researchTradition.age==r.researchTradition.age)")
 def test_dialogue_and_engineering_cancel_pending_but_keep_all_completed_history(self):
  for key in ('dialogue','engineering'):
   v=ordinary();v.execute('local n=seed();install(n);r=n')
   v=prepare(v,key);v.execute("local row=r[key];row.serial=2;row.pending={id=2,token=r.base.token,reference=M.Copy(r.origin),start=2,ended=true,stage='CALLING',reason='unknown native outcome'};if key=='dialogue'then row.pending.era='ERA_CLASSICAL'end;local p=plan();local n=p.set[key];assert(n.pending==nil and n.serial==2 and n.last.id==2 and p.set[key..'Known']==true);if key=='dialogue'then assert(n.total==15 and SPCCapitalInvestmentModel.Same(n.used,row.used))else assert(n.L==1 and SPCCapitalInvestmentModel.Same(n.receipts,row.receipts))end")
 def test_bad_or_missing_payload_is_not_reinitialized(self):
  for key in ('dialogue','engineering','capital','development','commerce'):
   v=prepare(ordinary(),key);v.execute("r[key]='BROKEN';local before=T.encode(r);assert(not pcall(plan)and T.encode(r)==before);r[key]=nil;assert(not pcall(plan))")
 def test_claim_timer_cancellation_is_content_independent_and_grants_no_receipt(self):
  v=prepare(ordinary(),'claimTimer');v.execute("r.claimTimer='CORRUPT_BUT_COPYABLE';local p=plan();assert(p.remove.claimTimer==true and next(p.set)==nil and p.nextEvidence==nil and r.claim==nil and r.claimTimer=='CORRUPT_BUT_COPYABLE')")
 def test_template_return_requires_original_catalogue_gate_and_keeps_ledger(self):
  v=prepare(ordinary(),'templateLifecycle');v.execute("""
  r.base.specialization='INDUSTRY';r.templatesCaptured=true;r.templateLifecycle={version=1,state='INITIALIZED',reconcilePending=false,districtsKnown=true}
  r.templates={schema=1,initialized=true,uid='STD:'..r.base.token,foundation=r.base.token,x=r.origin.x,y=r.origin.y,learned={},revision=1,
   knowledgeVersion=1,districts={version=1,initialized=true,policy='D0045',initializedTurn=0,learned={},coverage='FROM_IDENTITY',revision=1}}
  local p=plan();assert(p.requiresTemplateValidation==true and p.set.templateLifecycle.reconcilePending==true and p.set.templates==nil and not r.templateLifecycle.reconcilePending)
  """)
 def test_insights_are_preserved_not_reset_or_reconstructed(self):
  v=prepare(ordinary(),'expeditionInsights');v.execute("r.expeditionInsights={version=1,records={['CIVILIZATION_EGYPT:PEOPLE']={civ='CIVILIZATION_EGYPT',category='PEOPLE',turn=1}}};local p=plan();assert(next(p.set)==nil and next(p.remove)==nil and p.topic=='INSIGHTS');r.expeditionInsights.records.WRONG={};assert(not pcall(plan))")
 def test_pure_delegate_does_not_touch_any_native_or_event_surface(self):
  v=prepare(ordinary(),'dialogue');v.execute("r.dialogue=SPCDialogueProjectModel.New();r.dialogueKnown=true;local forbidden=setmetatable({},{__index=function()error('NATIVE_SURFACE_FORBIDDEN')end});Game=forbidden;Players=forbidden;Events=forbidden;GameEvents=forbidden;UI=forbidden;local p=plan();assert(p.set.dialogue.serial==0 and p.nextEvidence==nil)")
  measure('S9f2_fixed_lifecycle_delegates',{'owners':9,'native_or_Property_calls_in_plan':0,'scope':'pure Plan fixture only','money_or_completion_replay':False,'independent_commerce_configuration':'preserved for REPUTATION scope'})
 def test_stale_witness_and_unreliable_time_leave_every_payload_unchanged(self):
  v=prepare(ordinary(),'dialogue');v.execute("local before=T.encode(r);assert(not pcall(plan,19));witness.epoch=2;assert(not pcall(plan,30));assert(T.encode(r)==before)")


class MoneyAndCommerce(Profile,unittest.TestCase):
 def test_capital_terminates_actual_paid_contract_without_replaying_money(self):
  v=observed();v.execute('assert(C.confirm())');prepare(v,'capital','source');v.execute("local m,w=moneyCalls,T.writes();local old=SPCCapitalInvestmentModel.Decode(r.capital);local p=plan();local n=SPCCapitalInvestmentModel.Decode(p.set.capital);assert(n.contracts.DISTRICT_CAMPUS.stage=='TERMINATED'and n.contracts.DISTRICT_CAMPUS.reason=='CAPITAL_OWNER_CHANGED'and n.contracts.DISTRICT_CAMPUS.debited==old.contracts.DISTRICT_CAMPUS.debited and moneyCalls==m and T.writes()==w)")
 def test_development_terminates_actual_contract_without_touching_target_or_receipt(self):
  v=development();v.execute('assert(sign())');prepare(v,'development','source');v.execute("local m,e=moneyCalls,effectWrites;local old=SPCDevelopmentInvestmentModel.Decode(r.development);local p=plan();local n=SPCDevelopmentInvestmentModel.Decode(p.set.development);for k,c in pairs(n.contracts)do assert(c.stage=='TERMINATED'and c.debited==old.contracts[k].debited and c.reason=='DEVELOPMENT_OWNER_CHANGED')end;assert(moneyCalls==m and effectWrites==e)")
 def test_partial_reputation_preserves_independent_domain_choices(self):
  v=observed();prepare(v,'commerce','source',scope='REPUTATION');v.execute("r.commerce.selected={'DISTRICT_CAMPUS','DISTRICT_THEATER'};local rep=r.commerce.reputation;rep.age=3;rep.cursor=3;local p=plan();assert(SPCCapitalInvestmentModel.Same(p.set.commerce.selected,r.commerce.selected)and p.set.commerce.reputation.age==3 and p.set.commerce.reputation.cursor==30 and p.set.commerce.owner==r.commerce.owner)")
 def test_whole_commerce_clears_old_choices_but_keeps_reliable_age_origin(self):
  v=observed();prepare(v,'commerce','source');v.execute("r.commerce.selected={'DISTRICT_CAMPUS'};local p=plan();assert(#p.set.commerce.selected==0 and p.set.commerce.reputation.receipt==r.commerce.reputation.receipt and p.set.commerce.reputation.age==r.commerce.reputation.age and p.set.commerce.reputation.cursor==30)")
 def test_non_commerce_identity_uses_original_exit_and_partial_configuration_stays(self):
  for scope in (True,'REPUTATION'):
   v=observed();prepare(v,'commerce','source',scope=scope);v.execute("r.base.specialization='CULTURE';r.commerce.selected={'DISTRICT_CAMPUS'};local p=plan();assert(p.set.commerce.reputation==nil and #p.set.commerce.selected==(... and 1 or 0))",scope=='REPUTATION')
 def test_held_source_uses_original_foreign_owner_pause_without_return_replay(self):
  v=observed();prepare(v,'commerce','source',False);v.execute("local p=plan();assert(p.set.commerce.owner==9 and #p.set.commerce.selected==0 and p.set.commerce.reputation.state=='DORMANT_OWNER'and p.set.commerce.reputation.cursor==10)")

if __name__=='__main__':unittest.main()
