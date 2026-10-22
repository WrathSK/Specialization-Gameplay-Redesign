"""B244 L3: lossless Capital storage under simulated binary32 Property conversion.
Actual model/Store/service; Treasury remains a double except explicit failure cases.
This is not native save-file or money precision acceptance.
"""
from pathlib import Path
import subprocess
import sys
import unittest
from lupa.lua55 import LuaRuntime
from test_b241_capital import SETUP
from test_b242_capital_diagnostics import rt
from test_store_write_boundaries import fixture

R=Path(__file__).resolve().parents[1]
BASELINE='d33fe78'
FLOAT32=r'''
rawget=nil
function f32(v)
 if type(v)=='number' then return string.unpack('f',string.pack('f',v)) end
 if type(v)~='table' then return v end
 local n={};for k,x in pairs(v)do n[k]=f32(x)end;return n
end
originalSetter=Game.SetProperty
-- Scope the injected conversion to Capital: native evidence does not establish
-- that structural integer hashes or other Property schemas use this representation.
Game.SetProperty=function(o,k,v)
 if type(v)=='table' and v.capital then v=C.model.Copy(v);v.capital=f32(v.capital)end
 return originalSetter(o,k,v)
end
balance=18004.92578125;networkSources.DISTRICT_CAMPUS={}
shared.Commerce.views['0:'..source:GetID()].reputation.effective=2
cap.Refresh(0,source:GetID());cap.Refresh(0,other:GetID())
'''

def native_shaped():
 l=rt();l.execute(FLOAT32);return l

def plain(value):
 if hasattr(value,'items'):return {k:plain(v) for k,v in value.items()}
 return value

def lua_value(lua,value):
 if isinstance(value,dict):return lua.table_from({k:lua_value(lua,v) for k,v in value.items()})
 return value

class Codec(unittest.TestCase):
 def test_every_numeric_field_roundtrips_extremes_without_rounding(self):
  l=native_shaped();l.execute(r'''
local M=C.model
for _,field in ipairs({'principal','safe','success','failure','probability','balanceBefore','balanceAfter','creditBefore','creditAfter','paid'})do
 for _,n in ipairs({0,1,1/3,.1,.43,4670.0276245117193,5007.619982910156,2295.628037109375,2^-1074,2^-1022,1e300,9007199254740991})do
  assert(M.StoredNumber(field,string.format('%.17g',n))==n)
 end
end
local q=M.Copy(C.view().domains[1].quote);q.failureCount=0;local n=M.Begin(nil,q,'STABLE',0,'one');local before=T.encode(n)
local encoded=M.Encode(n);assert(encoded.numberEncoding=='DECIMAL17_V1')
assert(type(encoded.contracts.DISTRICT_CAMPUS.safe)=='string')
assert(T.encode(n)==before and M.Same(M.Decode(f32(encoded)),n))
local c=encoded.contracts.DISTRICT_CAMPUS
assert(type(c.C)=='number' and c.C==1.25 and type(c.due)=='number' and c.stage=='DEBIT_INTENT')
assert(not pcall(M.Encode,encoded));assert(M.Decode(nil)==nil)
''')

 def test_noncanonical_nonfinite_and_wrong_typed_values_rejected(self):
  l=native_shaped();l.execute(r'''
local M=C.model
for _,s in ipairs({'',' 1','1 ','01','1.0','+1','1e0','0x1','nan','NaN','inf','1e999','-1','1,5',string.rep('1',33)})do
 assert(M.StoredNumber('safe',s)==nil,s)
end
assert(M.StoredNumber('safe',3)==nil and M.StoredNumber('request','123')==nil)
local q=M.Copy(C.view().domains[1].quote);q.failureCount=0;local n=M.Begin(nil,q,'STABLE',0,'one')
for _,v in ipairs({-1,math.huge,0/0,'1',false,{}})do
 for _,field in ipairs({'safe','probability','creditBefore','creditAfter','paid'})do
  local bad=M.Copy(n);bad.contracts.DISTRICT_CAMPUS[field]=v;assert(not pcall(M.Encode,bad))
 end
end
''')

 def test_unknown_or_old_format_cannot_masquerade_as_recovered_history(self):
  for marker in ('nil',"'DECIMAL17_V2'",'1',"'PRIVATE_FORMAT'"):
   with self.subTest(marker=marker):
    l=native_shaped();l.execute("assert(C.confirm());T.record(source).capital.numberEncoding="+marker+";C.reload();assert(not pcall(shared.CityProgressionStore.CapitalState,0,source) and moneyCalls==1 and not C.view().canSign)")

 def test_required_and_optional_malformed_fields_hold_on_reconstruction(self):
  for field in ('principal','safe','success','failure','probability','balanceBefore','balanceAfter','creditBefore','creditAfter','paid'):
   for bad in ("'PRIVATE_VALUE'",'1'):
    with self.subTest(field=field,bad=bad):
     l=native_shaped();l.execute("assert(C.confirm());T.record(source).capital.contracts.DISTRICT_CAMPUS."+field+'='+bad+";C.reload();assert(not pcall(shared.CityProgressionStore.CapitalState,0,source));cap.Reconcile(0);assert(moneyCalls==1 and not C.view().canSign)")

 def test_missing_required_and_semantically_bad_number_remain_invalid(self):
  for mutation in ('c.safe=nil',"c.probability='1'","c.failure=c.principal"):
   with self.subTest(mutation=mutation):
    l=native_shaped();l.execute("assert(C.confirm());local c=T.record(source).capital.contracts.DISTRICT_CAMPUS;"+mutation+";C.reload();assert(not pcall(shared.CityProgressionStore.CapitalState,0,source) and moneyCalls==1)")

class ActualStore(unittest.TestCase):
 def test_observed_quote_signs_and_matures_exactly_under_numeric_conversion(self):
  l=native_shaped();l.execute(r'''
local q=C.model.Copy(C.view().domains[1].quote);local untouched=T.encode(T.record(other));T.scanReset()
assert(q.safe==4670.0276245117193 and f32(q.safe)==4670.02783203125)
assert(C.confirm());local c=C.contract();assert(c.safe==q.safe and c.probability==q.probability)
assert(balance==q.balance-q.principal and moneyCalls==1)
local raw=T.record(source).capital
assert(type(raw.contracts.DISTRICT_CAMPUS.probability)=='string' and type(c.probability)=='number')
local visited;shared.CityProgressionStore.VisitCapital(0,function(v,r)if r.cityID==source:GetID()then visited=v end end)
assert(C.model.Same(visited,C.state()));visited.contracts.DISTRICT_CAMPUS.safe=1
assert(C.contract().safe==q.safe)
local expected=balance+q.safe;T.turn(10)
assert(C.contract().stage=='SETTLED' and C.contract().paid==expected-C.contract().creditBefore and C.model.MoneyMatches(C.contract().creditBefore,q.safe,C.contract().creditActualAfter) and moneyCalls==2 and balance==expected)
assert(C.contract().creditBefore==q.balance-q.principal and C.contract().creditAfter==expected)
assert(type(T.record(source).capital.contracts.DISTRICT_CAMPUS.paid)=='string')
assert(T.encode(T.record(other))==untouched and T.scanCount()==0)
cap.Reconcile(0);C.reload();cap.Reconcile(0);assert(moneyCalls==2 and balance==expected)
''')

 def test_three_domain_slots_stable_and_both_venture_outcomes(self):
  l=native_shaped();l.execute(r'''
assert(C.confirm('DISTRICT_CAMPUS','STABLE','one'))
roll=.99;assert(C.confirm('DISTRICT_THEATER','VENTURE','two'))
roll=0;assert(C.confirm('DISTRICT_INDUSTRIAL_ZONE','VENTURE','three'))
local state=C.state();local sum=balance
for domain,c in pairs(state.contracts)do sum=sum+C.model.Payout(c)end
assert(moneyCalls==3 and rolls==2 and state.protection['0']==0)
C.reload();assert(C.model.Same(C.state(),state) and rolls==2)
T.turn(10);assert(moneyCalls==6 and balance==sum)
for domain,c in pairs(C.state().contracts)do assert(c.stage=='SETTLED' and c.paid==c.creditActualAfter-c.creditBefore and C.model.MoneyMatches(c.creditBefore,C.model.Payout(state.contracts[domain]),c.creditActualAfter))end
cap.Reconcile(0);assert(moneyCalls==6)
''')

 def test_fresh_lua_VM_restores_terms_and_protection_without_new_roll_or_debit(self):
  first=native_shaped();first.execute("roll=.99;assert(C.confirm(nil,'VENTURE'));snapshot=C.state()")
  props=plain(first.eval('T.props()'));state=plain(first.globals().snapshot);balance=first.globals().balance
  second=native_shaped()
  second.globals().savedProps=lua_value(second,props)
  second.globals().expectedState=lua_value(second,state)
  second.globals().balance=balance
  second.execute(r'''
for k,v in pairs(savedProps)do T.propsSet(k,v)end
C.reload();assert(C.model.Same(C.state(),expectedState) and moneyCalls==0 and rolls==0)
local expected=balance+C.model.Payout(C.contract());T.turn(10)
assert(C.contract().stage=='SETTLED' and moneyCalls==1 and rolls==0 and balance==expected)
cap.Reconcile(0);assert(moneyCalls==1)
''')

 def test_repeated_reads_and_identical_write_do_not_touch_property_or_other_extensions(self):
  l=native_shaped();l.execute(r'''
assert(C.confirm());local raw=T.encode(T.record(source));local before=T.writes()
local old=C.state();shared.CityProgressionStore.WriteCapital(0,source,old,C.model.Copy(old))
for i=1,12 do C.state();shared.CityProgressionStore.VisitCapital(0,function()end)end
assert(T.writes()==before and T.encode(T.record(source))==raw)
local changed=C.model.Copy(old);changed.sequence=changed.sequence+1
shared.CityProgressionStore.WriteCapital(0,source,old,changed)
assert(not pcall(shared.CityProgressionStore.WriteCapital,0,source,old,old))
local after=C.state();after.contracts.DISTRICT_CAMPUS.safe=0
assert(C.contract().safe==old.contracts.DISTRICT_CAMPUS.safe)
''')

 def test_loss_terminates_encoded_contract_preserving_all_values_and_protection(self):
  l=native_shaped();l.execute(r'''
roll=.99;assert(C.confirm(nil,'VENTURE'));local before=C.state();local expected=C.model.Terminate(before,'CAPITAL_OWNER_CHANGED')
local balanceBefore=balance;T.loss(source,3,900)
assert(C.model.Same(C.model.Decode(T.record(source).capital),expected))
assert(balance==balanceBefore and moneyCalls==1 and type(T.record(source).capital.contracts.DISTRICT_CAMPUS.safe)=='string')
C.reload();cap.Reconcile(0);assert(moneyCalls==1)
''')

 def test_locked_S_owner_loss_and_unknown_source_keep_existing_guards(self):
  l=native_shaped();l.execute(r'''
networkSources.DISTRICT_CAMPUS={research:GetID()};cap.Refresh(0,source:GetID());assert(C.confirm())
T.loss(research,3,901);cap.Reconcile(0);assert(C.contract().stage=='TERMINATED' and moneyCalls==1)
''')

 def test_protection_reset_reencodes_without_repricing_contract(self):
  l=native_shaped();l.execute(r'''
roll=.99;assert(C.confirm(nil,'VENTURE'));local before=C.state();local n=C.model.ResetProtection(before)
shared.CityProgressionStore.WriteCapital(0,source,before,n)
assert(next(C.state().protection)==nil and C.model.Same(C.contract(),before.contracts.DISTRICT_CAMPUS))
C.reload();assert(next(C.state().protection)==nil and moneyCalls==1)
''')

 def test_reentrant_reads_and_commands_never_expose_candidate_or_repeat_debit(self):
  l=native_shaped();l.execute(r'''
local setter=Game.SetProperty;local blocked=0
Game.SetProperty=function(o,k,v)
 if k==T.key(source)then
  assert(not pcall(shared.CityProgressionStore.CapitalState,0,source));blocked=blocked+1
  assert(not pcall(shared.CityProgressionStore.VisitCapital,0,function()error('candidate exposed')end))
 end
 return setter(o,k,v)
end
onMoney=function()assert(not C.confirm(nil,'VENTURE','nested'))end
assert(C.confirm());assert(moneyCalls==1 and rolls==0 and blocked==3)
''')

class Failures(unittest.TestCase):
 def test_prewrite_conflict_still_rejects_before_any_setter_or_money(self):
  l=native_shaped();l.execute(r'''
T.record(source).revision=T.record(source).revision+1
local setter=Game.SetProperty;local calls=0
Game.SetProperty=function(...)calls=calls+1;return setter(...)end
assert(not C.confirm());local d=cap.lastRequest.failure
assert(d.readPoint=='PREWRITE' and d.writeStatus=='NOT_CALLED' and d.diffPath=='record.revision')
assert(calls==0 and moneyCalls==0 and C.view().stage=='HELD')
''')

 def test_changed_string_even_canonical_or_one_ULP_is_not_tolerated(self):
  for change in ("string.format('%.17g',tonumber(c.safe)+2^-40)","c.safe..'0'","'PRIVATE_TOKEN'",'tonumber(c.safe)'):
   with self.subTest(change=change):
    l=native_shaped();l.execute("""
local setter=Game.SetProperty
Game.SetProperty=function(o,k,v)
 if k==T.key(source)then local c=v.capital.contracts.DISTRICT_CAMPUS;c.safe="""+change+""" end
 return setter(o,k,v)
end
assert(not C.confirm());local d=cap.lastRequest.failure
assert(d.phase=='DEBIT_INTENT_WRITE' and d.diagnosticStatus=='COMPLETE' and d.diffPath=='contract.safe')
assert(d.expectedType=='string' and d.expectedNumber==4670.0276245117193 and not d.savedMatches and moneyCalls==0)
assert(refresh());assert(C.view().stage=='HELD' and not C.view().canSign);assert(not C.confirm() and moneyCalls==0)
for _,e in ipairs(ExposedMembers.SPC_B205TrainingTrace.entries)do assert(not e.line:find('PRIVATE_TOKEN',1,true))end
""")

 def test_unrelated_record_difference_not_ignored_by_capital_encoding(self):
  l=native_shaped();l.execute(r'''
local setter=Game.SetProperty
Game.SetProperty=function(o,k,v)if k==T.key(source)then v.extra='changed'end;return setter(o,k,v)end
assert(not C.confirm());assert(moneyCalls==0 and cap.lastRequest.failure.diffPath=='OTHER_RECORD_OR_UNLISTED')
''')

 def test_ignored_throwing_missing_or_unreadable_intent_stays_held(self):
  for mode in ('IGNORE','BEFORE','AFTER','READ_ERROR','MISSING','WRONG_VERSION'):
   with self.subTest(mode=mode):
    l=native_shaped();l.globals().mode=mode;l.execute(r'''
local setter,getter=Game.SetProperty,Game.GetProperty;local wrote=false
Game.SetProperty=function(o,k,v)
 if k==T.key(source)then
  wrote=true
  if mode=='IGNORE'then return end
  if mode=='BEFORE'then error('STORE_INJECTED_FAILURE')end
  if mode=='WRONG_VERSION'then v.capital.numberEncoding='PRIVATE_VERSION'end
  setter(o,k,v);if mode=='AFTER'then error('STORE_INJECTED_FAILURE')end;return
 end
 return setter(o,k,v)
end
Game.GetProperty=function(o,k)
 if wrote and k==T.key(source)then
  if mode=='READ_ERROR'then error('unreadable')end
  if mode=='MISSING'then return nil end
 end
 return getter(o,k)
end
assert(not C.confirm() and moneyCalls==0);assert(C.view().stage=='HELD' and cap.lastRequest.failure.diagnosticStatus=='COMPLETE')
if mode=='AFTER'then assert(cap.lastRequest.failure.savedMatches)end
if mode=='WRONG_VERSION'then assert(cap.lastRequest.failure.diffPath=='capital.numberEncoding')end
assert(refresh());assert(not C.confirm() and moneyCalls==0)
''')

 def test_unconfirmed_final_receipts_never_repeat_money_in_session_or_reload(self):
  for stage in ('ACTIVE','SETTLED'):
   for mode in ('BEFORE','IGNORE','AFTER'):
    with self.subTest(stage=stage,mode=mode):
     l=native_shaped();l.globals().failStage=stage;l.globals().mode=mode;l.execute(r'''
local setter=Game.SetProperty
Game.SetProperty=function(o,k,v)
 if k==T.key(source) and v.capital and v.capital.contracts.DISTRICT_CAMPUS.stage==failStage then
  if mode=='IGNORE'then return end
  if mode=='AFTER'then setter(o,k,v)end
  error('STORE_INJECTED_FAILURE')
 end
 return setter(o,k,v)
end
local signed=C.confirm();if failStage=='SETTLED'then assert(signed);T.turn(10)else assert(not signed)end
local calls=moneyCalls;assert(calls==(failStage=='ACTIVE' and 1 or 2))
assert(C.view().stage=='HELD');cap.Reconcile(0);assert(moneyCalls==calls)
Game.SetProperty=setter;C.reload();cap.Reconcile(0)
assert(moneyCalls==calls)
local expected=mode=='AFTER' and failStage or 'HELD';assert(C.contract().stage==expected)
''')

 def test_native_money_mismatch_not_hidden_by_storage_repair(self):
  l=native_shaped();l.execute(r'''
moneyFloor=true;assert(not C.confirm());assert(moneyCalls==1 and C.contract().stage=='DEBIT_CALLING')
assert(cap.lastRequest.failure.errorCode=='CAPITAL_MONEY_UNCONFIRMED' and cap.lastRequest.failure.phase=='NATIVE_DEBIT')
C.reload();cap.Reconcile(0);assert(C.contract().stage=='HELD' and moneyCalls==1)
''')

 def test_failed_write_does_not_contaminate_normal_other_city(self):
  l=native_shaped();l.execute(r'''
local untouched=T.encode(T.record(other));T.failKey(T.key(source));assert(not C.confirm())
assert(T.encode(T.record(other))==untouched and moneyCalls==0)
T.scanReset();assert(C.confirm(nil,'STABLE','other',other));assert(moneyCalls==1 and T.scanCount()==0)
''')

 def test_invalid_encoding_diagnostic_keeps_existing_error_fence(self):
  l=native_shaped();l.execute(r'''
SPCCapitalInvestmentDiagnostics.Readback=function()error('CapitalInvestmentDiagnostics.lua:4: diagnostic fault')end
T.failKey(T.key(source));assert(not C.confirm());local d=cap.lastRequest.failure
assert(d.diagnosticStatus=='ERROR' and d.errorCode=='STORE_WRITE_UNCONFIRMED' and d.readPoint=='POSTWRITE' and moneyCalls==0)
''')

 def test_trace_numeric_strings_parse_without_private_data_or_new_fields(self):
  l=native_shaped();l.execute(r'''
local setter=Game.SetProperty
Game.SetProperty=function(o,k,v)if k==T.key(source)then local c=v.capital.contracts.DISTRICT_CAMPUS;c.safe=string.format('%.17g',tonumber(c.safe)+2^-40)end;return setter(o,k,v)end
assert(not C.confirm());d=cap.lastRequest.failure
''')
  sys.path.insert(0,str(R/'tools'))
  try:
   from collect_expedition_trace import train_line,fields
   rows=[fields(train_line(e['line'])) for _,e in l.globals().ExposedMembers.SPC_B205TrainingTrace.entries.items() if train_line(e['line'])]
   row=next(v for v in rows if v.get('phase')=='DEBIT_INTENT_WRITE')
   self.assertEqual(row['expectedType'],'string');self.assertEqual(row['actualType'],'string')
   self.assertEqual(float(row['expectedNumber']),l.eval('d.expectedNumber'));self.assertEqual(float(row['actualNumber']),l.eval('d.actualNumber'))
   self.assertNotEqual(row['expectedNumber'],row['actualNumber'])
  finally:sys.path.remove(str(R/'tools'))

class Equivalence(unittest.TestCase):
 def test_noncapital_age_writes_match_immediate_baseline_without_cross_record_visits(self):
  old=subprocess.check_output(['git','show',BASELINE+':Mod/CityProgressionStore.lua'],cwd=R,text=True)
  for count,touched in ((8,8),(20,20),(40,40),(40,1)):
   with self.subTest(records=count,touched=touched):
    result=[]
    for src in (old,None):
     l=fixture(src);l.globals().N=count;l.globals().NT=touched
     result.append(l.execute("T.start();local group={};for i=1,N do if i<=NT then group[i]=T.research(i)else group[i]=T.fresh(i);T.register(group[i])end end;T.governor(1);T.scanReset();local before=T.writes();T.turn(1);local delta=T.writes()-before;local scans=T.scanCount();local snap=T.encode(T.props());local writes=T.writes();T.turn(0);T.reload();assert(T.writes()==writes and T.encode(T.props())==snap);return snap,delta,scans"))
    self.assertEqual(result[0],result[1]);self.assertEqual(result[1][1:],(touched,0))

 def test_pre_repair_store_reproduces_native_four_differences_before_debit(self):
  old=subprocess.check_output(['git','show',BASELINE+':Mod/CityProgressionStore.lua'],cwd=R,text=True)
  l=fixture(old);l.globals().include('CapitalInvestment');l.execute(SETUP);l.execute(FLOAT32)
  l.execute("assert(not C.confirm());local d=cap.lastRequest.failure;assert(d.diffPath=='contract.safe' and d.diffCount==4 and d.expectedNumber==4670.0276245117193 and d.actualNumber==4670.02783203125 and d.diagnosticStatus=='COMPLETE' and moneyCalls==0)")

 def test_original_values_and_property_work_equal_with_only_wire_format_different(self):
  results=[]
  for original in (True,False):
   store=subprocess.check_output(['git','show',BASELINE+':Mod/CityProgressionStore.lua'],cwd=R,text=True) if original else None
   l=fixture(store);l.globals().include('CapitalInvestment');l.execute(SETUP);l.globals().original=original
   l.execute(r'''
local getter=Game.GetProperty;local reads=0;Game.GetProperty=function(...)reads=reads+1;return getter(...)end
local before=T.writes();T.scanReset();assert(C.confirm());T.turn(10)
local record=C.model.Copy(T.record(source));if not original then record.capital=C.model.Decode(record.capital)end
comparison={record=T.encode(record),state=T.encode(C.state()),balance=balance,money=moneyCalls,
 reads=reads,writes=T.writes()-before,scans=T.scanCount()}
''')
   results.append(dict(l.globals().comparison.items()))
  self.assertEqual(results[0],results[1]);self.assertEqual(results[1]['scans'],0)
  self.assertEqual((results[1]['reads'],results[1]['writes'],results[1]['money']),(14,7,2))

 def test_business_math_service_and_store_commit_guards_unchanged(self):
  old=lambda p:subprocess.check_output(['git','show',BASELINE+':'+p],cwd=R,text=True)
  for p in ('Mod/CapitalInvestment.lua','Mod/UI/CapitalInvestmentUI.lua','Mod/UI/CapitalInvestmentPanel.lua','Mod/ExpeditionTrainingDiagnostics.lua'):
   self.assertEqual(old(p),(R/p).read_text(),p)
  p='Mod/CapitalInvestmentModel.lua';now=(R/p).read_text()
  self.assertEqual(old(p).split('function M.Open(c)',1)[1],now.split('function M.Open(c)',1)[1])
  self.assertEqual(old(p).split('function M.Open(c)',1)[0],now.split('-- B244:',1)[0])
  p='Mod/CityProgressionStore.lua';self.assertEqual(old(p).split(' local function protectFailed',1)[1],(R/p).read_text().split(' local function protectFailed',1)[1])
  for p in ('Mod/CapitalInvestmentModel.lua','Mod/CapitalInvestmentDiagnostics.lua','Mod/CityProgressionStore.lua'):
   s=(R/p).read_text();self.assertNotIn('SetUpdate',s);self.assertNotIn('collectgarbage',s)

if __name__=='__main__':unittest.main()
