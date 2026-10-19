"""B241 L3: actual model/Store/service, explicit native Treasury doubles.
Fractional doubles and cold-VM reconstruction are LOCAL_SIMULATION, not native money evidence.
"""
from pathlib import Path
import unittest
from lupa.lua55 import LuaRuntime
from test_store_write_boundaries import fixture
R=Path(__file__).resolve().parents[1]

SETUP=r'''
T.start();GameConfiguration.GetGameSpeedType=function()return 'GAMESPEED_STANDARD'end
GameInfo.GameSpeeds={GAMESPEED_STANDARD={GameSpeedType='GAMESPEED_STANDARD'}}
C={};C.model=SPCCapitalInvestmentModel
function C.make(i,kind,level)
 local c=T.fresh(i);T.register(c);T.complete(c,kind)
 for n=1,(level or 1)-1 do T.invest(c,30000+i*10+n)end
 return c
end
source=C.make(1,'DISTRICT_COMMERCIAL_HUB',4)
research=C.make(2,'DISTRICT_CAMPUS',3)
other=C.make(3,'DISTRICT_COMMERCIAL_HUB',3)
T.governor(4);balance=1000.125;moneyCalls=0;rolls=0;roll=0;moneyFail=nil
function treasury()
 return {GetGoldBalance=function()if balanceReadFail then error('UNREADABLE')end;return balance end,
 ChangeGoldBalance=function(_,amount)
  moneyCalls=moneyCalls+1
  if onMoney then onMoney(amount)end
  if moneyFail=='BEFORE'then error('BEFORE')end
  if moneyFail=='IGNORE'then return end
  balance=balance+(moneyFloor and math.floor(amount) or amount)
  if moneyFail=='AFTER'then error('AFTER')end
 end}
end
Players[0].GetTreasury=treasury
Game.GetRandNum=function(n)rolls=rolls+1;return math.floor(roll*n)end
ExposedMembers={};Map.GetPlotByIndex=function()return nil end
P.Field=function(tab,key)return tab and tab[key]end
local originalInfo=P.Info
P.Info=function(tab,id)if id=='BUILDING_SPC_CAPITAL_ACCESS'then return {Index=id}end;return originalInfo(tab,id)end
P.HasBuilding=function(b,id)return b[id]==true end
P.CreateBuilding=function(q,id)q[id]=true end
P.RemoveBuilding=function(b,id)b[id]=nil end
function C.equip(c)
 c.markers={};function c:GetBuildings()return self.markers end;function c:GetBuildQueue()return self.markers end
 function c:GetName()return 'CITY_'..self:GetID()end
end
C.equip(source);C.equip(research);C.equip(other)
local function commerce(c)
 local ok,f=pcall(T.control,c)
 return {identity='COMMERCE',potential=ok and f.potential or 0,token=c.s.values.TOKEN,stage='READY',reputation={effective=20},
 domains={{id='DISTRICT_CAMPUS',effective=true},{id='DISTRICT_THEATER',effective=false},{id='DISTRICT_INDUSTRIAL_ZONE',effective=false}}}
end
networkSources={DISTRICT_CAMPUS={research:GetID()}}
shared.NetworkBridge={CurrentCapitalSources=function(pid,c,kind)
 assert(not networkFail,'CAPITAL_NETWORK_PENDING')
 return kind=='RESEARCH' and networkSources.DISTRICT_CAMPUS or {}
end}
shared.DistrictCompleteness={ReadFacts=function()return {validity='VERIFIED',availability='READY',value={domains={DISTRICT_CAMPUS={value=3}}}}end}
function C.service()
 shared.Commerce={views={[source:GetOwner()..':'..source:GetID()]=commerce(source),[other:GetOwner()..':'..other:GetID()]=commerce(other)}}
 SPCCapitalInvestment.Start(P,shared);cap=shared.CapitalInvestment
 cap.Refresh(0,source:GetID());cap.Refresh(0,other:GetID())
end
function C.view(c)return cap.views['0:'..(c or source):GetID()]end
function C.state(c)return shared.CityProgressionStore.CapitalState(0,c or source).value end
function C.contract(domain,c)return C.state(c).contracts[domain or 'DISTRICT_CAMPUS']end
function C.confirm(domain,mode,token,c)
 c=c or source;local v=C.view(c)
 return cap.Request(0,{Action='CAPITAL_CONFIRM',CityID=c:GetID(),Domain=domain or 'DISTRICT_CAMPUS',Mode=mode or 'STABLE',
  Token=token or 'confirm',Revision=v.revision,CityToken=v.token})
end
function C.reload()
 T.reload();C.service()
end
C.service()
'''
def runtime():
 l=fixture();l.globals().include('CapitalInvestment');l.execute(SETUP);return l

class Model(unittest.TestCase):
 def run_lua(self,s):
  l=LuaRuntime(unpack_returned_tuples=True);l.execute((R/'Mod/CapitalInvestmentModel.lua').read_text());l.execute("M=SPCCapitalInvestmentModel;ref={owner=0,cityID=1,x=1,y=2,token='city',changes=0};"+s)
 def test_safe_venture_and_current_treasury_formula(self):
  self.run_lua("local q=M.Quote{domain='DISTRICT_CAMPUS',source=ref,turn=5,balance=1000.5,D=3,R=20,failureCount=0,commercialized=true};assert(q.principal==250.125 and q.S==1 and q.C==1.25 and math.abs(q.r-.0375)<1e-9);assert(math.abs(q.failure-q.principal*.6)<1e-9 and q.due==15 and q.net==q.expected-q.principal)")
 def test_highest_current_active_then_earliest_institution_then_stable_key(self):
  self.run_lua("local a={reference=M.Copy(ref),level=3,attained=4};local b=M.Copy(a);b.reference.cityID=2;b.attained=2;local best,s=M.Choose{a,b};assert(s==3 and best.reference.cityID==2);b.attained=4;best=M.Choose{b,a};assert(best.reference.cityID==1);b.level=2;b.attained=0;best=M.Choose{b,a};assert(best.level==3)")
 def test_unknown_historical_time_only_blocks_a_real_tie(self):
  self.run_lua("local a={reference=ref,level=3};assert(M.Choose{a});local b=M.Copy(a);b.reference.cityID=2;b.attained=1;assert(not pcall(M.Choose,{a,b}));assert(select(2,M.Choose{})==1)")
 def test_failure_count_shared_and_success_reset_at_activation(self):
  self.run_lua("local q=M.Quote{domain='DISTRICT_CAMPUS',source=ref,turn=5,balance=1000,D=1,R=0,failureCount=0};local n=M.Begin(nil,q,'VENTURE',.99,'one');assert(not next(n.protection));n.contracts[q.domain].stage='DEBIT_CALLING';n=M.Activate(n,q.domain);assert(n.protection['0']==1);local nextQ=M.Quote{domain='DISTRICT_THEATER',source=ref,turn=5,balance=750,D=1,R=0,failureCount=1};assert(nextQ.probability>q.probability);n=M.Begin(n,nextQ,'VENTURE',0,'two');n.contracts[nextQ.domain].stage='DEBIT_CALLING';n=M.Activate(n,nextQ.domain);assert(n.protection['0']==0)")
 def test_termination_does_not_change_protection_and_public_hides_outcome(self):
  self.run_lua("local q=M.Quote{domain='DISTRICT_CAMPUS',source=ref,turn=5,balance=1000,D=1,R=0,failureCount=0};local n=M.Begin(nil,q,'VENTURE',.99,'one');n.contracts[q.domain].stage='DEBIT_CALLING';n=M.Activate(n,q.domain);local p=M.PublicContract(n.contracts[q.domain]);assert(p.won==nil and p.failureCount==nil);n=M.Terminate(n,'CAPITAL_OWNER_CHANGED');assert(n.protection['0']==1 and n.contracts[q.domain].stage=='TERMINATED');assert(not next(M.ResetProtection(n).protection))")
 def test_probability_cap_all_local_D_and_S(self):
  self.run_lua("for D=0,10 do for S=1,4 do for n=0,50 do local q=M.Quote{domain='DISTRICT_CAMPUS',source=ref,turn=0,balance=1000,D=D,R=40,failureCount=n,candidates={{reference=ref,level=S,attained=0}}};assert(q.probability<=.8 and q.probability>=.4 and q.failure==175 and q.safe<=q.success)end end end")
 def test_invalid_sparse_and_corrupt_contracts_rejected(self):
  self.run_lua("local n=M.New();n.protection['0']=-1;assert(not pcall(M.Validate,n));n=M.New();n.contracts.UNKNOWN={};assert(not pcall(M.Validate,n))")

class Runtime(unittest.TestCase):
 def check(self,s):runtime().execute(s)
 def test_quote_reads_implemented_network_without_local_district_requirement(self):
  self.check("local v=C.view();assert(v.canSign and #v.domains==3);local q=v.domains[1].quote;assert(q.D==3 and q.S==3 and q.C==1.25);assert(v.domains[2].quote.D==1 and v.domains[2].quote.S==1 and not v.domains[2].quote.sSource);assert(moneyCalls==0 and rolls==0)")
 def test_fractional_exact_debit_and_remaining_treasury_next_domain(self):
  self.check("local q=C.view().domains[1].quote;assert(C.confirm());assert(balance==1000.125*.75 and moneyCalls==1);assert(C.contract().stage=='ACTIVE');assert(C.confirm('DISTRICT_THEATER','STABLE','second'));assert(balance==1000.125*.75*.75 and moneyCalls==2)")
 def test_duplicate_confirmation_never_repeats_money(self):
  self.check("assert(C.confirm());local b=balance;assert(not C.confirm());assert(balance==b and moneyCalls==1)")
 def test_stale_balance_and_state_rejected_before_roll_or_debit(self):
  self.check("balance=balance+1;assert(not C.confirm(nil,'VENTURE'));assert(rolls==0 and moneyCalls==0 and not C.state())")
 def test_same_domain_other_city_allowed_no_national_contract_cap(self):
  self.check("assert(C.confirm());cap.Refresh(0,other:GetID());assert(C.confirm(nil,'STABLE','other',other));assert(moneyCalls==2)")
 def test_maturity_once_duplicate_turn_and_reload(self):
  self.check("assert(C.confirm());local contract=C.contract();local expected=balance+contract.safe;T.turn(10);assert(C.contract().stage=='SETTLED' and math.abs(balance-expected)<1e-9 and moneyCalls==2);cap.Reconcile(0);assert(moneyCalls==2);C.reload();cap.Reconcile(0);assert(C.contract().stage=='SETTLED' and moneyCalls==2)")
 def test_midterm_coldload_preserves_locked_outcome_and_terms(self):
  self.check("roll=.99;assert(C.confirm(nil,'VENTURE'));local before=T.encode(C.contract());local b=balance;C.reload();assert(T.encode(C.contract())==before and balance==b and rolls==1);T.turn(10);assert(C.contract().stage=='SETTLED' and rolls==1 and C.contract().paid==C.contract().failure)")
 def test_active_loss_and_route_loss_do_not_reprice_or_cancel_signed_contract(self):
  self.check("assert(C.confirm());local original=T.encode(C.contract());T.governor(1);networkFail=true;cap.Refresh(0,source:GetID());assert(not C.view().canSign and T.encode(C.contract())==original);T.turn(10);assert(C.contract().stage=='SETTLED')")
 def test_source_owner_change_terminates_without_return_or_failure_update(self):
  self.check("roll=.99;assert(C.confirm(nil,'VENTURE'));local n=C.state().protection['0'];local b=balance;T.loss(source,3,900);assert(T.record(source).capital.contracts.DISTRICT_CAMPUS.stage=='TERMINATED' and balance==b and moneyCalls==1);assert(T.record(source).capital.protection['0']==n)")
 def test_S_owner_change_terminates_contract(self):
  self.check("assert(C.confirm());local b=balance;T.loss(research,3,901);cap.Reconcile(0);assert(C.contract().stage=='TERMINATED' and balance==b and moneyCalls==1)")
 def test_calling_reload_holds_without_guessing_balance_or_retry(self):
  self.check("assert(C.confirm());local c=T.record(source).capital.contracts.DISTRICT_CAMPUS;c.stage='CREDIT_CALLING';C.reload();cap.Reconcile(0);assert(C.contract().stage=='HELD' and moneyCalls==1)")
 def test_failed_native_call_before_or_after_never_retries(self):
  for failure in ('BEFORE','AFTER','IGNORE'):
   with self.subTest(failure=failure):self.check("moneyFail='"+failure+"';assert(not C.confirm());assert(C.contract().stage=='DEBIT_CALLING');local calls=moneyCalls;cap.Reconcile(0);T.turn(1);C.reload();cap.Reconcile(0);assert(C.contract().stage=='HELD' and moneyCalls==calls)")
 def test_native_rounding_mismatch_held_not_silently_floored(self):
  self.check("moneyFloor=true;assert(not C.confirm());assert(moneyCalls==1 and C.contract().stage=='DEBIT_CALLING');cap.Reconcile(0);assert(C.contract().stage=='HELD' and moneyCalls==1)")
 def test_failed_predebit_store_write_makes_no_native_call(self):
  self.check("T.failKey(T.key(source));assert(not C.confirm());assert(moneyCalls==0 and rolls==0)")
 def test_store_reader_blocks_reentrant_candidate_and_other_city_unchanged(self):
  self.check("local setter=Game.SetProperty;local blocked=false;local untouched=T.encode(T.record(other));Game.SetProperty=function(o,k,v)if k==T.key(source)then blocked=not pcall(shared.CityProgressionStore.CapitalState,0,source)end;return setter(o,k,v)end;assert(C.confirm());assert(blocked and T.encode(T.record(other))==untouched)")
 def test_after_credit_store_failure_no_duplicate_on_same_session_or_reload(self):
  self.check("assert(C.confirm());local setter=Game.SetProperty;Game.SetProperty=function(o,k,v)if k==T.key(source) and v.capital and v.capital.contracts.DISTRICT_CAMPUS.stage=='SETTLED'then error('FAIL FINAL')end;return setter(o,k,v)end;T.turn(10);assert(moneyCalls==2);Game.SetProperty=setter;C.reload();cap.Reconcile(0);assert(moneyCalls==2 and C.contract().stage=='HELD')")
 def test_known_missing_and_corrupt_history_are_not_reinitialized(self):
  for mutation in ('r.capital=nil','r.capital.contracts.DISTRICT_CAMPUS.principal=-1'):
   with self.subTest(mutation=mutation):self.check("assert(C.confirm());local r=T.record(source);"+mutation+";C.reload();assert(not pcall(shared.CityProgressionStore.CapitalState,0,source) and moneyCalls==1)")
 def test_establishment_time_survives_governor_change_and_reload(self):
  self.check("local times=shared.CityProgressionStore.InstitutionHistory(0,research);assert(times[1]~=nil and times[2]~=nil and times[3]~=nil);local old=T.encode(times);T.governor(1);C.reload();assert(T.encode(shared.CityProgressionStore.InstitutionHistory(0,research))==old)")
 def test_successful_venture_settles_locked_success_amount(self):
  self.check("roll=0;assert(C.confirm(nil,'VENTURE'));local expected=C.contract().success;T.turn(10);assert(C.contract().stage=='SETTLED' and C.contract().paid==expected and rolls==1)")
 def test_ordinary_capital_writes_do_not_repeat_cross_record_uniqueness_walk(self):
  self.check("T.scanReset();assert(C.confirm());assert(T.scanCount()==0);T.turn(10);assert(T.scanCount()==0)")
 def test_occupied_domain_does_not_consume_random_roll(self):
  self.check("assert(C.confirm());assert(not C.confirm(nil,'VENTURE','again'));assert(rolls==0 and moneyCalls==1)")
 def test_native_reentrant_confirmation_cannot_debit_twice(self):
  self.check("local nested;onMoney=function()nested=C.confirm(nil,'VENTURE','nested')end;assert(C.confirm());assert(not nested and moneyCalls==1 and rolls==0)")
 def test_written_final_receipt_survives_throw_without_replay(self):
  self.check("assert(C.confirm());local setter=Game.SetProperty;Game.SetProperty=function(o,k,v)local result=setter(o,k,v);if k==T.key(source) and v.capital and v.capital.contracts.DISTRICT_CAMPUS.stage=='SETTLED'then error('AFTER FINAL')end;return result end;T.turn(10);assert(moneyCalls==2);Game.SetProperty=setter;C.reload();cap.Reconcile(0);assert(moneyCalls==2 and C.contract().stage=='SETTLED')")
 def test_source_fact_disagreement_is_unknown_not_an_empty_pool(self):
  self.check("local read=shared.EffectiveFacts.Read;shared.EffectiveFacts.Read=function(pid,c)local f=read(pid,c);if c==research then f.specialization='CULTURE'end;return f end;cap.Refresh(0,source:GetID());assert(not C.view().domains[1].canSign and C.view().domains[1].reason=='CAPITAL_SOURCE_UNKNOWN')")
 def test_actual_establishment_times_choose_older_institution(self):
  self.check("T.turn(1);local later=C.make(4,'DISTRICT_CAMPUS',3);C.equip(later);networkSources.DISTRICT_CAMPUS={later:GetID(),research:GetID()};cap.Refresh(0,source:GetID());assert(C.view().domains[1].quote.sSource.cityID==research:GetID())")
 def test_unknown_network_holds_quotes_without_new_money(self):
  self.check("networkFail=true;cap.Refresh(0,source:GetID());assert(not C.view().domains[1].canSign);assert(not C.confirm() and moneyCalls==0)")

if __name__=='__main__':unittest.main()
