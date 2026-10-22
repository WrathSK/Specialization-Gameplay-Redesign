"""B246 targeted L3: actual Store/service/model + native-context reader doubles.
LOCAL_SIMULATION only: no actual purchase-price, additive-production or UI PASS.
"""
from pathlib import Path
import unittest
from test_b241_capital import runtime as capital_runtime
from test_culture_network import fixture as network_fixture
R=Path(__file__).resolve().parents[1]
SETUP=r'''
function tableInfo(rows,key)
 local t={};for _,r in ipairs(rows)do t[r[key]]=r;if r.Index then t[r.Index]=r end end
 return setmetatable(t,{__call=function()local i=0;return function()i=i+1;return rows[i]end end})
end
local oldInfo=P.Info
defs={
 {BuildingType='BUILDING_DEV_LIBRARY',Name='Library',Index=101,Hash=1101,PrereqDistrict='DISTRICT_CAMPUS',Tier=1,Cost=100},
 {BuildingType='BUILDING_DEV_ALT',Name='Alternate',Index=102,Hash=1102,PrereqDistrict='DISTRICT_CAMPUS',Tier=1,Cost=120},
 {BuildingType='BUILDING_DEV_UNIVERSITY',Name='University',Index=103,Hash=1103,PrereqDistrict='DISTRICT_CAMPUS',Tier=2,Cost=200},
 {BuildingType='BUILDING_DEV_FACTORY',Name='Factory',Index=104,Hash=1104,PrereqDistrict='DISTRICT_INDUSTRIAL_ZONE',Tier=1,Cost=150},
 {BuildingType='BUILDING_DEV_DUMMY',Name='Dummy',Index=105,Hash=1105,PrereqDistrict='DISTRICT_CAMPUS',Tier=0,Cost=1,InternalOnly=true},
 {BuildingType='BUILDING_DEV_WONDER',Name='Wonder',Index=106,Hash=1106,PrereqDistrict='DISTRICT_CAMPUS',Tier=0,Cost=1,IsWonder=true}}
GameInfo.Buildings=tableInfo(defs,'BuildingType')
GameInfo.Districts=tableInfo({{DistrictType='DISTRICT_CAMPUS',Index=1,Name='Campus'},{DistrictType='DISTRICT_INDUSTRIAL_ZONE',Index=2,Name='Industry'}},'DistrictType')
GameInfo.HD_BuildingTiers=tableInfo(defs,'BuildingType');GameInfo.DistrictReplaces=tableInfo({},'CivUniqueDistrictType');GameInfo.HD_DUMMY_BUILDINGS=tableInfo({},'BuildingType')
GameInfo.SPC_DevelopmentEffects=tableInfo({{DistrictType='DISTRICT_CAMPUS',CarrierType='BUILDING_SPC_DEVELOPMENT_DISTRICT_CAMPUS'},
 {DistrictType='DISTRICT_INDUSTRIAL_ZONE',CarrierType='BUILDING_SPC_DEVELOPMENT_DISTRICT_INDUSTRIAL_ZONE'}},'DistrictType')
P.Info=function(tab,id)
 if tab=='Buildings' and type(id)=='string' and id:match('^BUILDING_SPC_DEVELOPMENT')then return {Index=id,BuildingType=id,InternalOnly=1}end
 if tab=='Yields' and id=='YIELD_GOLD'then return {Index=0}end
 return (GameInfo[tab] and GameInfo[tab][id]) or oldInfo(tab,id)
end
Game.GetLocalPlayer=function()return 0 end
prices={[1101]=400.125,[1102]=480,[1103]=800,[1104]=600};eligible={[1101]=true,[1102]=true,[1103]=true,[1104]=true};readCalls=0;effectWrites=0
function equip(c)
 C.equip(c)
 c.markers.CanProduce=function(_,hash,visible,continue)assert(visible==false and continue==true);return eligible[hash]==true end
 function c:GetDistricts()return {IsComplete=function()return true end,Members=function()return ipairs({{GetType=function()return 1 end,IsComplete=function()return true end},{GetType=function()return 2 end,IsComplete=function()return true end}})end}end
 function c:GetGold()return {GetPurchaseCost=function(_,yield,hash)assert(yield==0);readCalls=readCalls+1;if priceFail then error('NATIVE_PRICE_READ_FAIL')end;return prices[hash]end}end
end
equip(source);equip(research);equip(other)
P.CreateBuilding=function(b,id)effectWrites=effectWrites+1;if effectFail then return end;b[id]=true end
P.RemoveBuilding=function(b,id)effectWrites=effectWrites+1;if removeFail then return end;b[id]=nil end
workerCounts={}
local oldDepth=shared.DistrictCompleteness.ReadFacts
shared.DistrictCompleteness.ReadFacts=function(pid,c,token)
 local out=oldDepth(pid,c,token);local first=T.control(c).first
 out.value.districts={{id=first.districtID,type=first.type,complete=true,pillaged=false,plot=c:GetID()}};return out
end
Map.GetPlotByIndex=function(id)return {GetWorkerCount=function()return workerCounts[id] or 2 end}end
function setupDevelopment()
 shared.NetworkBridge=shared.NetworkBridge or {}
 shared.NetworkBridge.CurrentOutgoingDomestic=function()return {validity=networkFail and 'UNKNOWN' or 'VERIFIED',partners=outgoing or {research:GetID()}}end
 for _,c in ipairs({source,other})do local v=shared.Commerce.views['0:'..c:GetID()];v.active=4;v.workers=2;v.stage='READY'end
 SPCCapitalInvestmentModel=SPCCapitalInvestmentModel
 SPCDevelopmentInvestmentRead.New(P);SPCDevelopmentInvestment.Start(P,shared);dev=shared.DevelopmentInvestment
 Events.LoadScreenClose.Fire()
end
function open(c)
 c=c or source;return dev.Request(0,{Action='DEVELOPMENT_OPEN',CityID=c:GetID(),Token='open'})
end
function view(c)return dev.views['0:'..(c or source):GetID()]end
function value(c)return shared.CityProgressionStore.DevelopmentState(0,c or source).value end
function contract(c,target)return value(c).contracts[(target or research).s.values.TOKEN]end
function sign(c,target,domain)
 c=c or source;local v=view(c)
 return dev.Request(0,{Action='DEVELOPMENT_CONFIRM',CityID=c:GetID(),TargetCity=(target or research):GetID(),Domain=domain or 'DISTRICT_CAMPUS',Token='confirm',Revision=v.revision,CityToken=v.token})
end
function active(c,domain)return (c or research).markers['BUILDING_SPC_DEVELOPMENT_'..(domain or 'DISTRICT_CAMPUS')]==true end
function reload()
 local dc=shared.DistrictCompleteness;T.reload();C.service();shared.DistrictCompleteness=dc;setupDevelopment()
end
setupDevelopment();assert(open(),dev.lastRequest.reason)
'''
def runtime():
 l=capital_runtime()
 l.globals().include('DevelopmentInvestment')
 l.execute((R/'Mod/UI/DevelopmentInvestmentRead.lua').read_text())
 l.execute(SETUP)
 return l

class Runtime(unittest.TestCase):
 def check(self,body):runtime().execute(body)
 def test_price_minimum_of_constructible_next_tier_without_purchase_permission(self):
  self.check("local r=view().options[1];assert(r.domain=='DISTRICT_CAMPUS' and r.building=='BUILDING_DEV_LIBRARY' and r.price==400.125 and r.cost==60.01875 and r.tier==1);assert(moneyCalls==0)")
 def test_unreadable_one_alternative_blocks_minimum_not_uses_other_price(self):
  self.check("prices[1102]=nil;open();assert(view().options[1].reason=='DEVELOPMENT_PRICE_UNAVAILABLE');assert(not sign() and moneyCalls==0)")
 def test_disabled_purchase_yield_does_not_remove_constructible_building(self):
  self.check("GameInfo.Buildings.BUILDING_DEV_LIBRARY.PurchaseYield=nil;open();assert(view().options[1].price==400.125);assert(sign())")
 def test_not_constructible_candidate_does_not_affect_minimum(self):
  self.check("eligible[1101]=false;open();assert(view().options[1].price==480 and view().options[1].building=='BUILDING_DEV_ALT')")
 def test_construction_need_not_be_current_queue_target(self):
  self.check("source.markers.current='UNRELATED_PROJECT';research.markers.current='UNIT_WARRIOR';assert(sign() and active())")
 def test_native_exact_and_tolerated_debit_with_saved_actual_receipt(self):
  self.check("local before=balance;assert(sign(),dev.lastRequest.reason);local c=contract();assert(c.stage=='ACTIVE' and c.debited==before-balance and math.abs(c.debited-c.cost)<1e-12 and moneyCalls==1 and active())")
 def test_accepted_native_quantization_preserves_theoretical_price(self):
  self.check("local t=treasury;Players[0].GetTreasury=function()local r=t();r.ChangeGoldBalance=function(_,delta)moneyCalls=moneyCalls+1;balance=math.floor((balance+delta)*256)/256 end;return r end;assert(sign(),dev.lastRequest.reason);assert(contract().cost==60.01875 and math.abs(contract().debited-contract().cost)<=.01)")
 def test_quote_changed_rejected_before_debit(self):
  self.check("prices[1101]=420;assert(not sign() and moneyCalls==0);assert(dev.lastRequest.reason=='DEVELOPMENT_QUOTE_STALE')")
 def test_changed_treasury_rejected_before_debit(self):
  self.check("balance=balance+1;assert(not sign() and moneyCalls==0)")
 def test_wrong_or_unknown_route_cannot_sign(self):
  self.check("networkFail=true;assert(not sign() and moneyCalls==0);networkFail=false;outgoing={};open();assert(view().reason=='DEVELOPMENT_NO_OUTGOING' and not sign() and moneyCalls==0)")
 def test_duplicate_and_cross_source_target_occupancy(self):
  self.check("T.invest(other,39991);open(other);assert(sign());assert(not sign());open(other);assert(view(other).options[1].reason=='DEVELOPMENT_TARGET_OCCUPIED');assert(not sign(other) and moneyCalls==1)")
 def test_source_capacity_and_decline_never_cancel_existing(self):
  self.check("assert(sign());workerCounts[source:GetID()]=0;dev.SourceChanged(0,source:GetID());open();assert(not view().canSign and view().used==1);dev.Reconcile(0);assert(active() and contract().stage=='ACTIVE')")
 def test_active_and_route_loss_continue(self):
  self.check("assert(sign());T.governor(1);networkFail=true;dev.Reconcile(0);open();assert(not view().canSign and active() and contract().stage=='ACTIVE')")
 def test_new_unrelated_building_does_not_end_contract(self):
  self.check("assert(sign());research.markers[104]=true;dev.Reconcile(0);assert(contract().stage=='ACTIVE' and active())")
 def test_alternative_next_building_completes_and_releases_slot(self):
  self.check("assert(sign());research.markers[102]=true;GameEvents.BuildingConstructed.Fire(0,research:GetID(),102);assert(contract().stage=='COMPLETED' and not active() and moneyCalls==1);open();assert(view().used==0)")
 def test_existing_building_and_repair_do_not_complete_again(self):
  self.check("research.markers[101]=true;open();assert(sign());GameEvents.BuildingConstructed.Fire(0,research:GetID(),101);assert(contract().stage=='ACTIVE' and active())")
 def test_purchase_or_cheat_present_fact_ends_without_refund(self):
  self.check("assert(sign());research.markers[101]=true;dev.Reconcile(0);assert(contract().stage=='COMPLETED' and not active() and moneyCalls==1)")
 def test_same_context_duplicate_events_do_not_rewrite_effects(self):
  self.check("assert(sign());local n=effectWrites;for i=1,12 do dev.Reconcile(0)end;assert(effectWrites==n and moneyCalls==1)")
 def test_reconstruction_preserves_receipt_and_rebuilds_effect(self):
  self.check("assert(sign());local old=T.encode(value());local b=balance;reload();assert(T.encode(value())==old and balance==b and moneyCalls==1 and active())")
 def test_closed_contract_reconstruction_never_reactivates(self):
  self.check("assert(sign());research.markers[101]=true;dev.Reconcile(0);reload();assert(not active() and contract().stage=='COMPLETED' and moneyCalls==1)")
 def test_source_owner_change_withdraws_without_refund(self):
  self.check("assert(sign());local b=balance;T.loss(source,3,900);dev.Reconcile(0);assert(not active() and moneyCalls==1 and balance==b);assert(T.record(source).development.contracts[research.s.values.TOKEN].stage=='TERMINATED')")
 def test_target_owner_change_withdraws_and_releases_occupancy(self):
  self.check("assert(sign());local b=balance;T.loss(research,3,901);dev.Reconcile(0);assert(contract().stage=='TERMINATED' and not active() and balance==b and moneyCalls==1)")
 def test_external_carriers_untouched_on_apply_and_completion(self):
  self.check("research.markers.EXTERNAL=true;research.markers.BUILDING_SPC_STD_PROD=true;assert(sign());research.markers[101]=true;dev.Reconcile(0);assert(research.markers.EXTERNAL and research.markers.BUILDING_SPC_STD_PROD)")
 def test_predebit_write_failure_never_touches_money(self):
  self.check("T.failKey(T.key(source));assert(not sign() and moneyCalls==0);assert(not sign() and moneyCalls==0)")
 def test_unknown_native_outcome_never_replayed_in_session_or_load(self):
  for mode in ('BEFORE','AFTER','IGNORE'):
   with self.subTest(mode=mode):self.check("moneyFail='"+mode+"';assert(not sign() and moneyCalls==1);dev.Reconcile(0);reload();assert(contract().stage=='HELD' and moneyCalls==1 and not active());open();assert(not sign() and moneyCalls==1)")
 def test_out_of_bound_rounding_holds_without_compensating(self):
  self.check("moneyFloor=true;assert(not sign() and moneyCalls==1);dev.Reconcile(0);assert(contract().stage=='HELD' and not active() and moneyCalls==1)")
 def test_debit_succeeded_receipt_write_failed_never_retries(self):
  self.check("local setter=Game.SetProperty;Game.SetProperty=function(o,k,v)if k==T.key(source) and v.development and v.development.contracts[research.s.values.TOKEN].stage=='ACTIVE'then error('FAILED_RECEIPT')end;return setter(o,k,v)end;assert(not sign() and moneyCalls==1);Game.SetProperty=setter;reload();assert(contract().stage=='HELD' and not active() and moneyCalls==1)")
 def test_native_reentrancy_cannot_double_charge(self):
  self.check("local nested;onMoney=function()nested=sign()end;assert(sign());assert(not nested and moneyCalls==1)")
 def test_unknown_target_reference_does_not_cancel_or_choose_another_city(self):
  self.check("assert(sign());local read=shared.CityProgressionStore.CapitalReference;shared.CityProgressionStore.CapitalReference=function(token)if token==research.s.values.TOKEN then error('UNKNOWN')end;return read(token)end;dev.Reconcile(0);assert(contract().stage=='ACTIVE' and moneyCalls==1);shared.CityProgressionStore.CapitalReference=read;dev.Reconcile(0);assert(active())")
 def test_corrupt_known_history_never_reinitialized_or_recharged(self):
  self.check("assert(sign());T.record(source).development=nil;reload();open();assert(not view().canSign and not sign() and moneyCalls==1)")
 def test_fractional_storage_survives_native_single_precision_property_model(self):
  self.check("local setter=Game.SetProperty;local function cast(x)if type(x)=='table'then local t={};for k,v in pairs(x)do t[k]=cast(v)end;return t elseif type(x)=='number'then return string.unpack('f',string.pack('f',x))else return x end end;Game.SetProperty=function(o,k,v)if v.development then v=SPCDevelopmentInvestmentModel.Copy(v);v.development=cast(v.development)end;return setter(o,k,v)end;assert(sign(),dev.lastRequest.reason);reload();assert(contract().cost==60.01875 and active() and moneyCalls==1)")
 def test_ordinary_writes_remain_local_no_cross_record_unique_scan(self):
  self.check("T.scanReset();assert(sign());assert(T.scanCount()==0);research.markers[101]=true;dev.Reconcile(0);assert(T.scanCount()==0)")
 def test_idle_publications_do_not_read_quotes_or_write_effects(self):
  self.check("local reads,writes=readCalls,effectWrites;for i=1,30 do Events.GameCoreEventPublishComplete.Fire()end;assert(readCalls==reads and effectWrites==writes)")

class AdditionalGuards(unittest.TestCase):
 def test_independent_cold_VM_restores_only_from_saved_properties(self):
  from test_b244_capital_storage import plain,lua_value
  old=runtime();old.execute("assert(sign());savedBalance=balance")
  props=plain(old.eval('T.props()'));before=plain(old.eval('value()'))
  fresh=runtime()
  for k,v in props.items():fresh.globals().T.propsSet(k,lua_value(fresh,v))
  fresh.globals().balance=old.globals().savedBalance
  fresh.execute('reload();assert(active() and moneyCalls==0)')
  self.assertEqual(plain(fresh.eval('value()')),before)
 def test_native_completion_during_debit_is_detected_without_second_payment(self):
  l=runtime();l.execute("onMoney=function()research.markers[101]=true end;assert(sign());assert(contract().stage=='COMPLETED' and not active() and moneyCalls==1)")
 def test_current_workers_not_stale_commercialization_view_authority(self):
  l=runtime();l.execute("shared.Commerce.views['0:'..source:GetID()].workers=99;workerCounts[source:GetID()]=0;open();assert(view().workers==0 and not view().canSign and moneyCalls==0)")
 def test_commercialization_yield_failure_does_not_disable_development(self):
  l=runtime();l.execute("shared.Commerce.views['0:'..source:GetID()].stage='HELD';open();assert(sign() and active())")
 def test_single_target_confirmation_does_not_requote_other_cities(self):
  l=runtime();l.execute("outgoing={research:GetID(),other:GetID()};open();local calls=0;local read=ExposedMembers.SPC_DevelopmentRead;ExposedMembers.SPC_DevelopmentRead=function(pid,id)if id==other:GetID()then calls=calls+1 end;return read(pid,id)end;assert(sign());assert(calls==1)") # one post-confirm UI refresh; none during confirmation
 def test_insufficient_gold_and_zero_negative_unknown_prices_never_charge(self):
  for change in ('balance=1','prices[1101]=0','prices[1101]=-1','priceFail=true'):
   with self.subTest(change=change):
    l=runtime();l.execute(change+";open();assert(not sign() and moneyCalls==0 and not active())")
 def test_same_domain_multiple_targets_source_capacity_is_counted(self):
  l=runtime();l.execute("outgoing={research:GetID(),other:GetID()};open();assert(sign());open();assert(sign(source,other));open();assert(view().used==2 and not view().canSign and active(other) and active(research))")
 def test_collectable_money_and_effect_records_have_exact_receipts(self):
  import sys
  l=runtime();l.execute("assert(sign());research.markers[101]=true;dev.Reconcile(0)")
  sys.path.insert(0,str(R/'tools'))
  try:
   from collect_expedition_trace import train_line,fields
   rows=[fields(train_line(e['line']))for _,e in l.globals().ExposedMembers.SPC_B205TrainingTrace.entries.items()if train_line(e['line'])]
   money=[r for r in rows if r.get('stage')=='DEVELOPMENT_MONEY'];self.assertEqual(len(money),1)
   r=money[0];self.assertEqual(r['moneyAccepted'],'true');self.assertEqual(float(r['actualDelta']),float(r['balanceAfter'])-float(r['balanceBefore']));self.assertLessEqual(abs(float(r['moneyError'])),.01)
   effects=[r for r in rows if r.get('stage')=='DEVELOPMENT_EFFECTS'];self.assertEqual([r['expected']for r in effects],['50','0'])
   self.assertEqual(len([r for r in rows if r.get('stage')=='DEVELOPMENT_CLOSED']),1)
  finally:sys.path.remove(str(R/'tools'))

class Network(unittest.TestCase):
 def test_direct_outgoing_only_not_reverse_or_transitive(self):
  l=network_fixture(False);l.execute("send('0,4,0,2,10;0,2,0,1,11;0,1,0,5,12',3);local x=net.CurrentOutgoingDomestic(0,cities[2]);assert(x.validity=='VERIFIED' and #x.partners==1 and x.partners[1]==1);local old=net.CurrentDomesticPartners(0,cities[2]);assert(#old.partners==2)")
 def test_pending_and_copied_projection(self):
  l=network_fixture(False);l.execute("send('0,2,0,1,11',1);local x=net.CurrentOutgoingDomestic(0,cities[2]);x.partners[1]=999;assert(net.CurrentOutgoingDomestic(0,cities[2]).partners[1]==1);net.CheckEvidence(false);assert(net.CurrentOutgoingDomestic(0,cities[2]).validity=='UNKNOWN')")

if __name__=='__main__':unittest.main()
