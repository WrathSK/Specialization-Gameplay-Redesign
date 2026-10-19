"""B245: actual Capital Model/Store/service under explicit native-money doubles.
The 1/256 case reproduces B244 evidence; it is not an asserted engine constant.
No native Treasury, save-file, CPU or memory acceptance is implied.
"""
from pathlib import Path
import subprocess
import sys
import unittest
from test_b241_capital import SETUP
from test_b241_capital_ui import ui
from test_b244_capital_storage import native_shaped, plain, lua_value
from test_store_write_boundaries import fixture, MODULES, instrument_store

R=Path(__file__).resolve().parents[1]
BASELINE='a16cc996d86f9380f06cfeeff6b17e5ee0eaf066'
MONEY=r'''
mode='quantized';moneyCalls=0
Players[0].GetTreasury=function()
 return {GetGoldBalance=function()if unreadable then error('UNREADABLE')end;return balance end,
 ChangeGoldBalance=function(_,amount)
  moneyCalls=moneyCalls+1
  if mode=='throw_before'then error('BEFORE')end
  local actual=amount
  if mode=='quantized'then actual=math.floor(amount*256)/256
  elseif mode=='error'then actual=amount+transferError
  elseif mode=='opposite'then actual=-amount
  elseif mode=='ignore'then actual=0 end
  balance=balance+actual
  if mode=='unreadable'then unreadable=true end
  if mode=='throw_after'then error('AFTER')end
 end}
end
'''
def runtime():
 l=native_shaped();l.execute(MONEY);return l

def baseline():
 l=fixture()
 def load(name):
  text=subprocess.check_output(['git','show',BASELINE+':Mod/'+name+'.lua'],cwd=R,text=True)
  l.execute(instrument_store(text) if name=='CityProgressionStore' else text)
 l.globals().include=load
 for name in MODULES:load(name)
 load('CapitalInvestment');l.execute(SETUP)
 return l

class Receipts(unittest.TestCase):
 def test_captured_native_debit_preserves_principal_and_records_actual(self):
  l=runtime();l.execute(r'''
local q=C.model.Copy(C.view().domains[1].quote);local untouched=T.encode(T.record(other));T.scanReset()
assert(C.confirm());local c=C.contract()
assert(c.principal==4501.2314453125 and c.debitAfter==13503.69140625 and c.debited==4501.234375)
assert(c.balanceAfter==13503.6943359375 and c.debited-c.principal==.0029296875)
assert(c.safe==q.safe and c.success==q.success and c.failure==q.failure and c.probability==q.probability)
assert(c.stage=='ACTIVE' and moneyCalls==1 and T.scanCount()==0 and T.encode(T.record(other))==untouched)
assert(not C.confirm() and moneyCalls==1)
local e=last('CAPITAL_MONEY');assert(e.moneyAccepted and e.moneyTolerance==.01 and e.moneyError==-.0029296875)
''')

 def test_credit_actual_receipt_and_duplicate_settlement(self):
  l=runtime();l.execute(r'''
assert(C.confirm());local c=C.contract();local requested=c.safe;local before=balance
T.turn(10);c=C.contract()
assert(c.stage=='SETTLED' and c.creditBefore==before and c.creditAfter==before+requested)
assert(c.creditActualAfter==balance and c.paid==balance-before and c.paid~=requested)
assert(math.abs(c.paid-requested)<=.01 and moneyCalls==2)
local e=last('CAPITAL_SETTLED');assert(e.requestedDelta==requested and e.returnAmount==c.paid)
cap.Reconcile(0);T.turn(0);C.reload();cap.Reconcile(0);assert(moneyCalls==2 and C.contract().paid==c.paid)
''')

 def test_venture_locked_outcomes_and_hidden_protection_unchanged(self):
  for won in (True,False):
   with self.subTest(won=won):
    l=runtime();l.globals().won=won;l.execute(r'''
roll=won and 0 or .99;assert(C.confirm(nil,'VENTURE'));local c=C.contract()
assert(c.won==won and C.state().protection['0']==(won and 0 or 1) and rolls==1)
local expected=won and c.success or c.failure;T.turn(10);c=C.contract()
assert(c.stage=='SETTLED' and C.model.Payout(c)==expected and math.abs(c.paid-expected)<=.01)
assert(c.paid==c.creditActualAfter-c.creditBefore and rolls==1)
''')

 def test_signed_receipts_cross_fresh_VM_without_second_debit_or_roll(self):
  a=runtime();a.execute("roll=.99;assert(C.confirm(nil,'VENTURE'))")
  props=plain(a.eval('T.props()'));state=plain(a.eval('C.state()'));money=a.globals().balance
  b=runtime();b.globals().savedProps=lua_value(b,props);b.globals().savedState=lua_value(b,state);b.globals().balance=money
  b.execute(r'''
for k,v in pairs(savedProps)do T.propsSet(k,v)end
C.reload();assert(C.model.Same(C.state(),savedState) and moneyCalls==0 and rolls==0)
T.turn(10);assert(C.contract().stage=='SETTLED' and moneyCalls==1 and rolls==0)
local done=C.model.Copy(C.state());C.reload();cap.Reconcile(0);assert(C.model.Same(done,C.state()) and moneyCalls==1)
''')

 def test_each_debit_and_credit_uses_its_own_bound(self):
  l=runtime();l.execute(r'''
mode='error';transferError=.009;assert(C.confirm());local c=C.contract()
assert(math.abs(c.debited-c.principal)<=.01)
transferError=-.009;T.turn(10);c=C.contract()
assert(c.stage=='SETTLED' and math.abs(c.paid-C.model.Payout(c))<=.01)
assert(moneyCalls==2 and c.paid-c.debited~=C.model.Payout(c)-c.principal)
''')

 def test_three_domains_other_city_and_same_turn_real_balance(self):
  l=runtime();l.execute(r'''
local untouched=T.encode(T.record(other));assert(C.confirm());local after=balance
assert(C.confirm('DISTRICT_THEATER','STABLE','two'));assert(C.contract('DISTRICT_THEATER').principal==after/4)
assert(C.confirm('DISTRICT_INDUSTRIAL_ZONE','STABLE','three'));assert(moneyCalls==3)
T.turn(10);assert(moneyCalls==6 and T.encode(T.record(other))==untouched)
for _,c in pairs(C.state().contracts)do assert(c.stage=='SETTLED' and c.paid==c.creditActualAfter-c.creditBefore)end
''')

 def test_current_facts_and_owner_exit_do_not_reprice_actual_receipts(self):
  l=runtime();l.execute(r'''
assert(C.confirm());local c=C.model.Copy(C.contract());local b=balance
T.governor(1);networkFail=true;cap.Refresh(0,source:GetID());assert(C.model.Same(c,C.contract()))
T.loss(source,3,900);local saved=C.model.Decode(T.record(source).capital).contracts.DISTRICT_CAMPUS
assert(saved.stage=='TERMINATED' and saved.debited==c.debited and saved.safe==c.safe and balance==b and moneyCalls==1)
''')

class Guards(unittest.TestCase):
 def test_allowance_boundary_direction_and_nonfinite(self):
  l=runtime();l.execute(r'''
local M=C.model
assert(M.MoneyMatches(0,.01,.02))
assert(not M.MoneyMatches(0,.01,.020000001))
assert(M.MoneyMatches(1,-.1,.905) and M.MoneyMatches(1,.1,1.095))
assert(not M.MoneyMatches(1,-.001,1) and not M.MoneyMatches(1,.001,1))
assert(not M.MoneyMatches(1,-.001,1.001) and not M.MoneyMatches(1,.001,.999))
for _,x in ipairs({0/0,math.huge,-math.huge,'1',false,{}})do
 assert(not M.MoneyMatches(x,1,2));assert(not M.MoneyMatches(1,x,2));assert(not M.MoneyMatches(1,1,x))
end
assert(not M.MoneyMatches(1,0,1) and not M.MoneyMatches(1,-2,-1))
''')

 def test_debit_failures_never_replay_even_if_request_returned(self):
  for mode in ('ignore','opposite','throw_before','throw_after','unreadable','error'):
   with self.subTest(mode=mode):
    l=runtime();l.globals().mode=mode;l.globals().transferError=.011
    l.execute(r'''
assert(not C.confirm());assert(moneyCalls==1)
unreadable=false;mode='quantized';cap.Reconcile(0);C.reload();cap.Reconcile(0);T.turn(10)
assert(moneyCalls==1 and C.contract().stage=='HELD' and not C.confirm())
''')

 def test_credit_failures_never_replay_or_compensate(self):
  for mode in ('ignore','opposite','throw_before','throw_after','unreadable','error'):
   with self.subTest(mode=mode):
    l=runtime();l.execute('assert(C.confirm())');l.globals().mode=mode;l.globals().transferError=-.011
    l.execute(r'''
T.turn(10);assert(moneyCalls==2);unreadable=false;mode='quantized'
C.reload();cap.Reconcile(0);T.turn(1);assert(moneyCalls==2 and C.contract().stage=='HELD')
''')

 def test_zero_actual_on_tiny_principal_is_not_accepted(self):
  l=runtime();l.execute("balance=.001;mode='ignore';cap.Refresh(0,source:GetID());assert(not C.confirm() and moneyCalls==1 and balance==.001)")

 def test_positive_tiny_transfer_is_not_rounded_by_mod(self):
  l=runtime();l.execute("balance=.001;mode='exact';cap.Refresh(0,source:GetID());assert(C.confirm());assert(C.contract().principal==.00025 and C.contract().debited==.00025 and balance==.00075)")

 def test_predebit_store_mismatch_still_exact_not_money_tolerant(self):
  l=runtime();l.execute(r'''
local setter=Game.SetProperty
Game.SetProperty=function(o,k,v)
 if k==T.key(source) and v.capital then local c=v.capital.contracts.DISTRICT_CAMPUS;c.safe=string.format('%.17g',tonumber(c.safe)+.001)end
 return setter(o,k,v)
end
assert(not C.confirm() and moneyCalls==0)
local d=cap.lastRequest.failure;assert(d.diffPath=='contract.safe' and not d.savedMatches)
''')

 def test_receipt_save_failure_after_debit_or_credit_never_replays(self):
  for stage in ('ACTIVE','SETTLED'):
   for after in (False,True):
    with self.subTest(stage=stage,after=after):
     l=runtime();l.globals().faultStage=stage;l.globals().afterWrite=after
     if stage=='SETTLED':l.execute('assert(C.confirm())')
     l.execute(r'''
local setter=Game.SetProperty
Game.SetProperty=function(o,k,v)
 if k==T.key(source) and v.capital and v.capital.contracts.DISTRICT_CAMPUS.stage==faultStage then
  if afterWrite then setter(o,k,v)end;error('RECEIPT_SAVE_FAILURE')
 end
 return setter(o,k,v)
end
if faultStage=='ACTIVE'then assert(not C.confirm())else T.turn(10)end
local calls=moneyCalls;Game.SetProperty=setter;C.reload();cap.Reconcile(0)
assert(moneyCalls==calls)
if not afterWrite then assert(C.contract().stage=='HELD')else assert(C.contract().stage==faultStage)end
''')

 def test_missing_inconsistent_or_tampered_receipts_do_not_rebuild(self):
  for mutation in ('c.debitAfter=nil','c.debited=nil','c.debited=c.principal','c.debitAfter=c.balanceBefore','c.creditActualAfter=1','v.version=1'):
   with self.subTest(mutation=mutation):
    l=runtime();l.execute('assert(C.confirm());local v=C.state();local c=v.contracts.DISTRICT_CAMPUS;'+mutation+';assert(not pcall(C.model.Validate,v))')

 def test_paid_receipt_uses_both_values_and_cannot_claim_theoretical_as_actual(self):
  l=runtime();l.execute(r'''
assert(C.confirm());T.turn(10);local v=C.state();local c=v.contracts.DISTRICT_CAMPUS
c.paid=C.model.Payout(c);assert(not pcall(C.model.Validate,v))
c.paid=c.creditActualAfter-c.creditBefore;c.creditActualAfter=nil;assert(not pcall(C.model.Validate,v))
''')

 def test_old_held_contract_not_implicitly_repaired(self):
  l=runtime();l.execute(r'''
mode='error';transferError=.02;assert(not C.confirm());cap.Reconcile(0)
local raw=T.record(source).capital;raw.version=1;local b=balance
C.reload();cap.Reconcile(0);assert(not pcall(C.state) and moneyCalls==1 and balance==b and not C.confirm())
''')

 def test_new_receipt_strings_survive_property_numeric_conversion(self):
  l=runtime();l.execute(r'''
assert(C.confirm());T.turn(10);local state=C.state();local raw=T.record(source).capital.contracts.DISTRICT_CAMPUS
for _,key in ipairs({'debitAfter','debited','creditActualAfter','paid','creditBefore','creditAfter'})do
 assert(type(raw[key])=='string' and C.model.StoredNumber(key,raw[key])==state.contracts.DISTRICT_CAMPUS[key])
end
assert(C.model.Same(C.model.Decode(f32(C.model.Encode(state))),state))
''')

class TraceAndScope(unittest.TestCase):
 def test_collector_receives_exact_allowlisted_money_values(self):
  l=runtime();l.execute('assert(C.confirm());T.turn(10)')
  sys.path.insert(0,str(R/'tools'))
  try:
   from collect_expedition_trace import train_line,fields
   rows=[fields(train_line(e['line'])) for _,e in l.globals().ExposedMembers.SPC_B205TrainingTrace.entries.items() if train_line(e['line'])]
   money=[v for v in rows if v.get('stage')=='CAPITAL_MONEY']
   self.assertEqual(len(money),2)
   for row in money:
    self.assertEqual(row['moneyAccepted'],'true');self.assertEqual(float(row['moneyTolerance']),.01)
    self.assertEqual(float(row['actualDelta']),float(row['balanceAfter'])-float(row['balanceBefore']))
    self.assertEqual(float(row['moneyError']),float(row['actualDelta'])-float(row['requestedDelta']))
   self.assertLessEqual(len(rows),96)
  finally:sys.path.remove(str(R/'tools'))

 def test_settled_UI_net_uses_actual_debit_and_credit(self):
  l=ui();l.execute(r'''
capitalView.contracts.DISTRICT_CAMPUS={stage='SETTLED',principal=250,debited=250.003,paid=252.496,due=10,D=1,S=1,C=1}
LuaEvents.SPC_CapitalOpen(0,9);ack()
assert(Controls.Contract.text:find('2.49',1,true))
''')

 def test_baseline_quote_values_balances_and_property_work_match(self):
  results=[]
  for old in (True,False):
   l=baseline() if old else fixture()
   if not old:l.globals().include('CapitalInvestment');l.execute(SETUP)
   l.execute(r'''
local getter=Game.GetProperty;local reads=0;Game.GetProperty=function(...)reads=reads+1;return getter(...)end
local quote=T.encode(C.view().domains[1].quote);local writes=T.writes();T.scanReset();assert(C.confirm());T.turn(10)
local c=C.model.Copy(C.contract());c.debitAfter=nil;c.debited=nil;c.creditActualAfter=nil;c.paid=nil
comparison={quote=quote,contract=T.encode(c),balance=balance,money=moneyCalls,reads=reads,writes=T.writes()-writes,scans=T.scanCount()}
''')
   results.append(dict(l.globals().comparison.items()))
  self.assertEqual(results[0],results[1]);self.assertEqual((results[1]['reads'],results[1]['writes'],results[1]['money'],results[1]['scans']),(14,7,2,0))

 def test_baseline_rejects_captured_money_while_B245_accepts(self):
  old=baseline();old.execute("balance=18004.92578125;networkSources.DISTRICT_CAMPUS={};cap.Refresh(0,source:GetID())");old.execute(MONEY)
  old.execute("assert(not C.confirm() and moneyCalls==1);cap.Reconcile(0);assert(C.contract().stage=='HELD' and moneyCalls==1)")
  new=runtime();new.execute("assert(C.confirm() and C.contract().stage=='ACTIVE' and moneyCalls==1)")

 def test_store_math_event_hooks_and_other_UI_unchanged(self):
  old=lambda p:subprocess.check_output(['git','show',BASELINE+':'+p],cwd=R,text=True)
  for p in ('Mod/CityProgressionStore.lua','Mod/UI/CapitalInvestmentUI.lua','Mod/UI/CapitalInvestmentPanel.xml','Mod/Text/Commerce.sql'):
   self.assertEqual(old(p),(R/p).read_text(),p)
  p='Mod/CapitalInvestmentModel.lua';before=old(p);now=(R/p).read_text()
  self.assertEqual(before.split('function M.Quote(input)',1)[1].split('function M.Activate',1)[0],now.split('function M.Quote(input)',1)[1].split('function M.Activate',1)[0])
  self.assertEqual(before.split('function M.Payout(c)',1)[1],now.split('function M.Payout(c)',1)[1])
  p='Mod/CapitalInvestment.lua';self.assertEqual(old(p).split(" hook('PlayerTurnActivated'",1)[1],(R/p).read_text().split(" hook('PlayerTurnActivated'",1)[1])
  for p in ('Mod/CapitalInvestment.lua','Mod/CapitalInvestmentModel.lua','Mod/CapitalInvestmentDiagnostics.lua','Mod/ExpeditionTrainingDiagnostics.lua'):
   s=(R/p).read_text();self.assertNotIn('SetUpdate',s);self.assertNotIn('collectgarbage',s)

if __name__=='__main__':unittest.main()
