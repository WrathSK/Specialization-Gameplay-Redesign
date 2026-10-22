"""B243: actual Store/service diagnostics in a restricted-Lua fixture.
No native Property precision or gameplay acceptance is inferred from these tests.
"""
from pathlib import Path
import subprocess
import sys
import unittest

from test_b242_capital_diagnostics import rt
from test_b241_capital import SETUP
from test_store_write_boundaries import fixture

R=Path(__file__).resolve().parents[1]

def restricted():
    lua=rt()
    lua.execute('rawget=nil')
    return lua

def lines(lua):
    return [e['line'] for _,e in lua.globals().ExposedMembers.SPC_B205TrainingTrace.entries.items()]

class RestrictedRuntime(unittest.TestCase):
    def test_fractional_sign_and_settlement_without_rawget(self):
        l=restricted();l.execute('''
balance=18004.92578125;networkSources.DISTRICT_CAMPUS={};cap.Refresh(0,source:GetID())
assert(C.confirm() and moneyCalls==1 and balance==13503.6943359375)
local expected=balance+C.contract().safe;T.turn(10)
assert(C.contract().stage=='SETTLED' and moneyCalls==2 and balance==expected)
assert(not last('CAPITAL_FAILURE'))
''')

    def test_actual_store_failures_keep_complete_diagnostics_without_rawget(self):
        for mode in ('ignore','float32','before','after','unreadable','missing','scalar'):
            with self.subTest(mode=mode):
                l=restricted();l.globals().mode=mode;l.execute('''
local setter,getter=Game.SetProperty,Game.GetProperty;local wrote=false
Game.SetProperty=function(o,k,v)
 if k==T.key(source) then
  wrote=true
  if mode=='ignore' then return end
  if mode=='before' then error('STORE_TEST_THROW')end
  if mode=='float32' then
   local c=v.capital.contracts.DISTRICT_CAMPUS;c.safe=string.unpack('f',string.pack('f',c.safe))
  end
  setter(o,k,v)
  if mode=='after' then error('STORE_TEST_THROW')end
  return
 end
 return setter(o,k,v)
end
Game.GetProperty=function(o,k)
 if k==T.key(source) and wrote then
  if mode=='unreadable' then error('read unavailable')end
  if mode=='missing' then return nil end
  if mode=='scalar' then return 'PRIVATE_VALUE'end
 end
 return getter(o,k)
end
assert(not C.confirm());d=cap.lastRequest.failure
assert(d.phase=='DEBIT_INTENT_WRITE' and d.readPoint=='POSTWRITE' and d.diagnosticStatus=='COMPLETE')
assert(d.errorCode==((mode=='before' or mode=='after') and 'STORE_TEST_THROW' or 'STORE_WRITE_UNCONFIRMED'))
assert(d.writeStatus==((mode=='before' or mode=='after') and 'THREW' or 'RETURNED'))
assert(d.readStatus==(mode=='unreadable' and 'READ_ERROR' or 'READABLE'))
assert(moneyCalls==0 and C.view().stage=='HELD' and not C.view().canSign)
if mode=='after' then assert(d.savedMatches and d.diffPath=='NONE')end
if mode=='float32' then assert(d.diffPath=='contract.safe' and d.expectedNumber~=d.actualNumber)end
assert(refresh());assert(C.view().failure.diagnosticStatus=='COMPLETE' and cap.lastRequest.reason~='CAPITAL_READY')
assert(not C.confirm() and moneyCalls==0)
''')
                text='\n'.join(lines(l));self.assertIn('diagnosticStatus=COMPLETE',text)
                self.assertNotIn('PRIVATE_VALUE',text)

    def test_prewrite_conflict_without_rawget_records_no_setter(self):
        l=restricted();l.execute('''
T.record(source).revision=T.record(source).revision+1
assert(not C.confirm());local d=cap.lastRequest.failure
assert(d.errorCode=='STORE_RECORD_STALE' and d.readPoint=='PREWRITE' and d.writeStatus=='NOT_CALLED')
assert(d.diagnosticStatus=='COMPLETE' and d.diffPath=='record.revision' and moneyCalls==0)
''')

    def test_projection_exception_keeps_minimal_facts_and_original_error(self):
        l=restricted();l.execute('''
local untouched=T.encode(T.record(other));local projection=SPCCapitalInvestmentDiagnostics.Readback
SPCCapitalInvestmentDiagnostics.Readback=function()
 error('CapitalInvestmentDiagnostics.lua:44: attempt to call a nil value (PRIVATE_DETAIL)')
end
T.failKey(T.key(source));assert(not C.confirm());local d=cap.lastRequest.failure
assert(d.errorCode=='STORE_WRITE_UNCONFIRMED' and d.diagnosticStatus=='ERROR')
assert(d.diagnosticErrorClass=='LUA_NIL' and d.diagnosticErrorFile=='CapitalInvestmentDiagnostics.lua' and d.diagnosticErrorLine==44)
assert(d.readPoint=='POSTWRITE' and d.readStatus=='READABLE' and d.writeStatus=='RETURNED')
assert(d.recordType=='table' and not d.savedMatches and d.diffPath==nil and moneyCalls==0)
assert(refresh());assert(C.view().failure.diagnosticStatus=='ERROR' and C.view().failure.phase=='DEBIT_INTENT_WRITE')
assert(not C.confirm() and moneyCalls==0 and T.encode(T.record(other))==untouched)
SPCCapitalInvestmentDiagnostics.Readback=projection
T.scanReset();assert(C.confirm(nil,nil,'other',other));assert(moneyCalls==1 and T.scanCount()==0)
''')
        text='\n'.join(lines(l));self.assertIn('diagnosticStatus=ERROR',text)
        self.assertIn('errorCode=STORE_WRITE_UNCONFIRMED',text)
        self.assertIn('diagnosticErrorClass=LUA_NIL',text);self.assertNotIn('PRIVATE_DETAIL',text)

    def test_invalid_projection_result_is_visible_not_a_success(self):
        for result in ('nil','false','17',"'PRIVATE_VALUE'"):
            with self.subTest(result=result):
                l=restricted();l.execute('SPCCapitalInvestmentDiagnostics.Readback=function()return '+result+' end')
                l.execute('''
T.failKey(T.key(source));assert(not C.confirm());local d=cap.lastRequest.failure
assert(d.errorCode=='STORE_WRITE_UNCONFIRMED' and d.diagnosticStatus=='ERROR')
assert(d.diagnosticErrorCode=='CAPITAL_DIAGNOSTIC_RESULT_INVALID' and d.readPoint=='POSTWRITE')
assert(moneyCalls==0 and not C.view().canSign)
''')
                self.assertNotIn('PRIVATE_VALUE','\n'.join(lines(l)))

    def test_nonstring_projection_error_does_not_invoke_tostring(self):
        l=restricted();l.execute('''
SPCCapitalInvestmentDiagnostics.Readback=function()
 error(setmetatable({},{__tostring=function()error('PRIVATE_DETAIL')end}))
end
T.failKey(T.key(source));assert(not C.confirm());local d=cap.lastRequest.failure
assert(d.diagnosticStatus=='ERROR' and d.diagnosticErrorClass=='UNKNOWN_ERROR')
assert(d.errorCode=='STORE_WRITE_UNCONFIRMED' and d.readPoint=='POSTWRITE' and moneyCalls==0)
''')
        self.assertNotIn('PRIVATE_DETAIL','\n'.join(lines(l)))

    def test_unobserved_callback_is_explicit_without_invented_readback(self):
        l=restricted();l.execute('''
shared.CityProgressionStore.WriteCapital=function()error('STORE_EARLY_REJECTION')end
assert(not C.confirm());local d=cap.lastRequest.failure
assert(d.errorCode=='STORE_EARLY_REJECTION' and d.phase=='DEBIT_INTENT_WRITE')
assert(d.diagnosticStatus=='NOT_OBSERVED' and d.readPoint==nil and d.writeStatus==nil and moneyCalls==0)
''')
        self.assertIn('diagnosticStatus=NOT_OBSERVED','\n'.join(lines(l)))

    def test_partial_projection_failure_does_not_erase_base_metadata(self):
        l=restricted();l.execute('''
SPCCapitalInvestmentDiagnostics.Readback=function()
 return setmetatable({},{__pairs=function()error('PRIVATE_ITERATION_FAILURE')end})
end
T.failKey(T.key(source));assert(not C.confirm());local d=cap.lastRequest.failure
assert(d.diagnosticStatus=='ERROR' and d.readPoint=='POSTWRITE' and d.recordType=='table')
assert(d.errorCode=='STORE_WRITE_UNCONFIRMED' and moneyCalls==0)
''')
        self.assertNotIn('PRIVATE_ITERATION_FAILURE','\n'.join(lines(l)))

    def test_settlement_failure_retains_no_replay_with_broken_projection(self):
        l=restricted();l.execute('''
assert(C.confirm());local setter=Game.SetProperty
Game.SetProperty=function(o,k,v)
 if k==T.key(source) and v.capital and v.capital.contracts.DISTRICT_CAMPUS.stage=='SETTLED' then return end
 return setter(o,k,v)
end
SPCCapitalInvestmentDiagnostics.Readback=function()error('projection failure')end
T.turn(10);local d=C.view().failure
assert(d.phase=='SETTLED_RECEIPT_WRITE' and d.diagnosticStatus=='ERROR' and d.readPoint=='POSTWRITE' and moneyCalls==2)
Game.SetProperty=setter;C.reload();cap.Reconcile(0);assert(moneyCalls==2 and C.contract().stage=='HELD')
''')

    def test_precision_survives_existing_collector_without_value_change(self):
        l=restricted();l.execute('''
balance=18004.92578125;networkSources.DISTRICT_CAMPUS={};cap.Refresh(0,source:GetID())
local setter=Game.SetProperty
Game.SetProperty=function(o,k,v)
 if k==T.key(source) and v.capital then local c=v.capital.contracts.DISTRICT_CAMPUS;c.safe=c.safe+2^-40 end
 return setter(o,k,v)
end
assert(not C.confirm());d=cap.lastRequest.failure
assert(d.expectedNumber~=d.actualNumber and d.diagnosticStatus=='COMPLETE' and moneyCalls==0)
''')
        sys.path.insert(0,str(R/'tools'))
        try:
            from collect_expedition_trace import fields,train_line
            rows=[fields(train_line(line)) for line in lines(l) if train_line(line)]
            row=next(row for row in rows if row.get('stage')=='CAPITAL_FAILURE' and row.get('phase')=='DEBIT_INTENT_WRITE')
            self.assertEqual(float(row['expectedNumber']),l.eval('d.expectedNumber'))
            self.assertEqual(float(row['actualNumber']),l.eval('d.actualNumber'))
            self.assertNotEqual(row['expectedNumber'],row['actualNumber'])
            self.assertEqual(row['diagnosticStatus'],'COMPLETE')
        finally:
            sys.path.remove(str(R/'tools'))

    def test_failed_diagnostic_keeps_existing_log_bounds(self):
        l=restricted();l.execute('''
SPCCapitalInvestmentDiagnostics.Readback=function()error('private failure')end
T.failKey(T.key(source));assert(not C.confirm())
for i=1,200 do refresh()end
local trace=ExposedMembers.SPC_B205TrainingTrace
assert(#trace.entries<=64 and trace.sequence<=96 and moneyCalls==0)
for _,e in ipairs(trace.entries)do assert(#e.line<=4096)end
''')

class ScopeAndBehavior(unittest.TestCase):
    def test_B242_and_B243_preserve_actual_values_and_property_work(self):
        for mode in ('success','ignore'):
            with self.subTest(mode=mode):
                results=[]
                for original in (True,False):
                    l=fixture()
                    service=subprocess.check_output(['git','show','380688d:Mod/CapitalInvestment.lua'],cwd=R,text=True) if original else (R/'Mod/CapitalInvestment.lua').read_text()
                    l.execute(service);l.execute(SETUP);l.globals().mode=mode
                    l.execute('''
rawget=nil;balance=18004.92578125;networkSources.DISTRICT_CAMPUS={};cap.Refresh(0,source:GetID())
local getter,setter=Game.GetProperty,Game.SetProperty;reads=0;calls=0
Game.GetProperty=function(...)reads=reads+1;return getter(...)end
Game.SetProperty=function(o,k,v)
 calls=calls+1
 if mode=='ignore' and k==T.key(source)then return end
 return setter(o,k,v)
end
local before=T.writes();T.scanReset();local good=C.confirm()
if mode=='success'then T.turn(10)else assert(not C.confirm())end
comparison={accepted=good,record=T.encode(T.record(source)),balance=balance,moneyCalls=moneyCalls,
 reads=reads,writes=T.writes()-before,setterCalls=calls,scans=T.scanCount()}
''')
                    results.append(dict(l.globals().comparison.items()))
                self.assertEqual(results[0],results[1])
                self.assertEqual(results[1]['scans'],0)
                self.assertEqual(results[1]['moneyCalls'],2 if mode=='success' else 0)

    def test_protected_sources_byte_identical_and_no_new_polling(self):
        for name in ('CityProgressionStore.lua','CapitalInvestmentModel.lua','UI/CapitalInvestmentPanel.lua'):
            original=subprocess.check_output(['git','show','380688d:Mod/'+name],cwd=R)
            self.assertEqual(original,(R/'Mod'/name).read_bytes(),name)
        for name in ('CapitalInvestment.lua','CapitalInvestmentDiagnostics.lua','ExpeditionTrainingDiagnostics.lua'):
            content=(R/'Mod'/name).read_text()
            self.assertNotIn('SetUpdate',content);self.assertNotIn('collectgarbage',content)
        self.assertNotIn('rawget(', (R/'Mod/CapitalInvestmentDiagnostics.lua').read_text())

if __name__=='__main__':unittest.main()
