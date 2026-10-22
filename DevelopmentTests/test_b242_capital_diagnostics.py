"""B242: actual Store/service/UI failure diagnostics; injected native doubles only.
No native precision, Treasury, rendered UI or save-file claim. B241 math is unchanged.
"""
import json
from pathlib import Path
import subprocess
import unittest
from lupa.lua55 import LuaRuntime
from test_b241_capital import SETUP
from test_store_write_boundaries import fixture
from test_b241_capital_ui import ui
R=Path(__file__).resolve().parents[1]

CAPTURE=r'''
log={};local make=SPCExpeditionTrainingDiagnostics.New
SPCExpeditionTrainingDiagnostics.New=function(...)
 local t=make(...);local record=t.Record
 t.Record=function(stage,v)log[#log+1]={stage=stage,value=SPCCapitalInvestmentModel.Copy(v)};record(stage,v)end
 return t
end
C.service()
function last(stage)
 for i=#log,1,-1 do if log[i].stage==stage then return log[i].value end end
end
function refresh()
 return cap.Request(0,{Action='CAPITAL_REFRESH',CityID=source:GetID(),Domain='DISTRICT_CAMPUS',Token='refresh'})
end
'''
def rt():
 l=fixture();l.globals().include('CapitalInvestment');l.execute(SETUP.rsplit('C.service()',1)[0]+CAPTURE);return l

class Runtime(unittest.TestCase):
 def check(self,s):rt().execute(s)
 def test_actual_logged_fractional_inputs_still_sign_without_correction(self):
  self.check("balance=18004.92578125;networkSources.DISTRICT_CAMPUS={};cap.Refresh(0,source:GetID());local expected=C.view().domains[1].quote.principal;assert(expected==4501.2314453125);T.scanReset();assert(C.confirm());assert(moneyCalls==1 and balance==13503.6943359375 and T.scanCount()==0);assert(C.contract().principal==expected and not last('CAPITAL_FAILURE'))")
 def test_predebit_setter_faults_report_stage_and_preserve_no_debit(self):
  for mode in ('before','after','ignore'):
   with self.subTest(mode=mode):
    l=rt();l.globals().mode=mode;l.execute(r'''
local setter=Game.SetProperty
Game.SetProperty=function(o,k,v)
 if k==T.key(source)then
  if mode=='after'then setter(o,k,v)end
  if mode=='ignore'then return end
  error('CityProgressionStore.lua:914: STORE_INJECTED_FAILURE')
 end;return setter(o,k,v)
end
assert(not C.confirm());local d=cap.lastRequest.failure
assert(d.phase=='DEBIT_INTENT_WRITE' and d.readPoint=='POSTWRITE' and d.recordType=='table')
assert(d.errorCode==(mode=='ignore' and 'STORE_WRITE_UNCONFIRMED' or 'STORE_INJECTED_FAILURE'))
assert(d.writeStatus==(mode=='ignore' and 'RETURNED' or 'THREW'))
assert(d.savedMatches==(mode=='after'));assert(d.diffPath==(mode=='after' and 'NONE' or 'capital'))
assert(moneyCalls==0 and C.view().stage=='HELD');assert(not last('CAPITAL_MONEY'))
assert(refresh());assert(cap.lastRequest.reason~='CAPITAL_READY' and cap.lastRequest.viewStage=='HELD')
assert(C.view().failure.phase=='DEBIT_INTENT_WRITE');assert(not C.confirm() and moneyCalls==0)
''')
 def test_float32_readback_reports_exact_field_and_two_values(self):
  self.check(r'''
local setter=Game.SetProperty
Game.SetProperty=function(o,k,v)
 if k==T.key(source) and v.capital then
  local c=v.capital.contracts.DISTRICT_CAMPUS;c.safe=string.unpack('f',string.pack('f',c.safe))
 end;return setter(o,k,v)
end
local expected=C.view().domains[1].quote.safe
assert(not C.confirm());local d=cap.lastRequest.failure
assert(d.phase=='DEBIT_INTENT_WRITE' and d.diffPath=='contract.safe' and d.diffCount==1)
assert(d.expectedNumber==expected and d.actualNumber~=expected and d.actualType=='number')
assert(d.savedPhase=='DEBIT_INTENT' and not d.savedMatches and moneyCalls==0)
local lines={};for _,e in ipairs(ExposedMembers.SPC_B205TrainingTrace.entries)do lines[#lines+1]=e.line end;local line=table.concat(lines,'\n')
assert(line:find('diffPath=contract.safe',1,true) and line:find('expectedNumber=',1,true) and line:find('actualNumber=',1,true))
''')
 def test_readback_unreadable_is_distinct_from_missing_record(self):
  for mode in ('unreadable','missing','scalar'):
   with self.subTest(mode=mode):
    l=rt();l.globals().mode=mode;l.execute(r'''
local setter,getter=Game.SetProperty,Game.GetProperty;local wrote=false
Game.SetProperty=function(o,k,v)local r=setter(o,k,v);if k==T.key(source)then wrote=true end;return r end
Game.GetProperty=function(o,k)
 if k==T.key(source) and wrote then
  if mode=='unreadable'then error('read unavailable')end
  if mode=='scalar'then return 'private text'end
  return nil
 end;return getter(o,k)
end
assert(not C.confirm());local d=cap.lastRequest.failure
assert(d.phase=='DEBIT_INTENT_WRITE' and d.readPoint=='POSTWRITE')
assert(d.readStatus==(mode=='unreadable' and 'READ_ERROR' or 'READABLE'))
assert(d.recordType==(mode=='unreadable' and 'UNKNOWN' or mode=='scalar' and 'string' or 'nil'))
assert(moneyCalls==0 and C.view().stage=='HELD')
''')
 def test_prewrite_stale_record_does_not_claim_a_setter_call(self):
  self.check(r'''
T.record(source).revision=T.record(source).revision+1
assert(not C.confirm());local d=cap.lastRequest.failure
assert(d.errorCode=='STORE_RECORD_STALE' and d.readPoint=='PREWRITE' and d.writeStatus=='NOT_CALLED')
assert(d.diffPath=='record.revision' and d.actualNumber==d.expectedNumber+1 and moneyCalls==0)
''')
 def test_second_write_and_final_receipt_are_distinguished(self):
  for target,phase,calls in [('DEBIT_CALLING','DEBIT_CALLING_WRITE',0),('ACTIVE','ACTIVE_RECEIPT_WRITE',1)]:
   with self.subTest(target=target):
    l=rt();l.globals().target=target;l.execute(r'''
local setter=Game.SetProperty
Game.SetProperty=function(o,k,v)
 if k==T.key(source) and v.capital and v.capital.contracts.DISTRICT_CAMPUS.stage==target then return end
 return setter(o,k,v)
end
assert(not C.confirm())
''');self.assertEqual(l.eval('cap.lastRequest.failure.phase'),phase);self.assertEqual(l.eval('moneyCalls'),calls)
    l.execute("local calls=moneyCalls;assert(not C.confirm());cap.Reconcile(0);assert(moneyCalls==calls)")
 def test_native_debit_failure_has_no_stale_store_diff(self):
  self.check("moneyFail='AFTER';assert(not C.confirm());local d=cap.lastRequest.failure;assert(d.phase=='NATIVE_DEBIT' and d.errorCode=='CAPITAL_MONEY_UNCONFIRMED' and d.readPoint==nil);assert(moneyCalls==1 and C.contract().stage=='DEBIT_CALLING');assert(refresh() and C.view().stage=='HELD' and cap.lastRequest.reason~='CAPITAL_READY');assert(not C.confirm() and moneyCalls==1)")
 def test_observer_cannot_affect_write_guards_or_other_cities(self):
  self.check(r'''
local unchanged=T.encode(T.record(other));local observer=SPCCapitalInvestmentDiagnostics.Readback
SPCCapitalInvestmentDiagnostics.Readback=function()error('diagnostic failure')end
T.failKey(T.key(source));assert(not C.confirm() and moneyCalls==0 and C.view().stage=='HELD')
assert(T.encode(T.record(other))==unchanged)
SPCCapitalInvestmentDiagnostics.Readback=observer
T.scanReset();assert(C.confirm(nil,nil,'other',other));assert(moneyCalls==1 and T.scanCount()==0)
''')
 def test_successful_writes_do_not_call_readback_observer(self):
  self.check("SPCCapitalInvestmentDiagnostics.Readback=function()error('must not run')end;assert(C.confirm());T.turn(10);assert(moneyCalls==2 and C.contract().stage=='SETTLED' and not last('CAPITAL_FAILURE'))")
 def test_settlement_receipt_error_keeps_no_replay_and_failure_detail(self):
  self.check(r'''
assert(C.confirm());local setter=Game.SetProperty
Game.SetProperty=function(o,k,v)
 if k==T.key(source) and v.capital and v.capital.contracts.DISTRICT_CAMPUS.stage=='SETTLED'then return end
 return setter(o,k,v)
end
T.turn(10);local d=C.view().failure
assert(d.phase=='SETTLED_RECEIPT_WRITE' and d.savedPhase=='CREDIT_CALLING' and d.diffPath=='contract.stage')
assert(moneyCalls==2);Game.SetProperty=setter;C.reload();cap.Reconcile(0);assert(moneyCalls==2 and C.contract().stage=='HELD')
''')
 def test_refresh_read_error_retains_code_and_never_acknowledges_ready(self):
  self.check(r'''
shared.CityProgressionStore.CapitalState=function()error('CityProgressionStore.lua:200: EVIDENCE_UNAVAILABLE')end
assert(refresh());assert(cap.lastRequest.accepted and cap.lastRequest.reason=='EVIDENCE_UNAVAILABLE')
assert(C.view().stage=='HELD' and C.view().failure.phase=='REFRESH_READ' and C.view().failure.errorFile=='CityProgressionStore.lua')
''')
 def test_domain_pending_quote_is_not_reported_as_ready(self):
  self.check("networkFail=true;assert(refresh());assert(cap.lastRequest.reason=='CAPITAL_NETWORK_PENDING' and not C.view().domains[1].canSign and moneyCalls==0)")
 def test_bad_request_and_no_error_object_stringification(self):
  self.check("assert(not cap.Request(0,false));assert(cap.lastRequest.failure.phase=='REQUEST_VALIDATE')")
 def test_failure_trace_uses_existing_bounds(self):
  self.check("T.failKey(T.key(source));assert(not C.confirm());for i=1,200 do refresh()end;local r=ExposedMembers.SPC_B205TrainingTrace;assert(#r.entries<=64 and r.sequence<=96 and moneyCalls==0)")
 def test_existing_collector_parses_new_failure_fields(self):
  import sys
  sys.path.insert(0,str(R/'tools'))
  try:
   from collect_expedition_trace import fields,train_line
   l=rt();l.execute("T.failKey(T.key(source));assert(not C.confirm())")
   rows=[fields(train_line(e['line'])) for _,e in l.globals().ExposedMembers.SPC_B205TrainingTrace.entries.items() if train_line(e['line'])]
   row=next(r for r in rows if r.get('stage')=='CAPITAL_FAILURE' and r.get('phase')=='DEBIT_INTENT_WRITE')
   self.assertEqual(row['readPoint'],'POSTWRITE');self.assertEqual(row['capitalType'],'nil');self.assertEqual(row['writeStatus'],'RETURNED')
  finally:sys.path.remove(str(R/'tools'))
 def test_private_values_do_not_escape_diagnostics(self):
  self.check(r'''
local setter=Game.SetProperty
Game.SetProperty=function(o,k,v)
 if k==T.key(source) and v.capital then
  v.capital.contracts.DISTRICT_CAMPUS.won=not v.capital.contracts.DISTRICT_CAMPUS.won
  v.capital.contracts.DISTRICT_CAMPUS.sourceName='PRIVATE_PERSON'
 end;return setter(o,k,v)
end
assert(not C.confirm(nil,'VENTURE'));local d=cap.lastRequest.failure
assert(d.diffPath=='OTHER_RECORD_OR_UNLISTED' and not d.expectedNumber and not d.actualNumber)
local text=T.encode(d);assert(not text:find('PRIVATE_PERSON',1,true) and not text:find('failureCount',1,true) and not text:find('won',1,true))
''')

class BehaviorComparison(unittest.TestCase):
 def test_B241_and_B242_per_value_results_and_property_work_match(self):
  results=[]
  for original in (True,False):
   store=subprocess.check_output(['git','show','8e8b5eb:Mod/CityProgressionStore.lua'],cwd=R,text=True) if original else None
   l=fixture(store)
   service=subprocess.check_output(['git','show','8e8b5eb:Mod/CapitalInvestment.lua'],cwd=R,text=True) if original else (R/'Mod/CapitalInvestment.lua').read_text()
   l.execute(service);l.execute(SETUP)
   l.execute(r'''
local getter=Game.GetProperty;reads=0
Game.GetProperty=function(...)reads=reads+1;return getter(...)end
local before=T.writes();T.scanReset();assert(C.confirm());T.turn(10)
comparison={state=T.encode(C.state()),record=T.encode(T.record(source)),balance=balance,calls=moneyCalls,
 reads=reads,writes=T.writes()-before,scans=T.scanCount()}
''')
   results.append(dict(l.globals().comparison.items()))
  self.assertEqual(results[0],results[1]);self.assertEqual(results[1]['scans'],0)
  self.assertEqual(results[1]['calls'],2)

class PureAndUI(unittest.TestCase):
 def test_error_sanitization_and_recognized_code_families(self):
  l=LuaRuntime();l.execute((R/'Mod/CapitalInvestmentDiagnostics.lua').read_text());l.execute(r'''
local D=SPCCapitalInvestmentDiagnostics
for _,prefix in ipairs({'CAPITAL','COMMERCE','STORE','PROGRESSION','EVIDENCE'})do
 local d=D.Error('CapitalInvestment.lua:34: CityProgressionStore.lua:914: '..prefix..'_EXAMPLE','DEBIT_INTENT_WRITE')
 assert(d.errorCode==prefix..'_EXAMPLE' and d.errorClass=='CONTRACT' and d.errorFile=='CityProgressionStore.lua' and d.errorLine==914)
end
local d=D.Error('/private/local/UnknownFile.lua:13: attempt to index a nil value (SECRET)','TEST')
assert(d.errorFile=='UNKNOWN' and d.errorLine==nil and d.errorClass=='LUA_NIL')
local x=setmetatable({},{__tostring=function()error('do not stringify')end});assert(D.Error(x).errorCode=='CAPITAL_STATE_UNKNOWN')
''')
 def test_type_and_hidden_diff_are_bounded_and_not_claimed_equal(self):
  l=LuaRuntime();l.execute((R/'Mod/CapitalInvestmentDiagnostics.lua').read_text());l.execute(r'''
local D=SPCCapitalInvestmentDiagnostics
local a={capital={version=1,sequence=1,contracts={X={principal='PRIVATE',safe=3,stage='DEBIT_INTENT'}}}}
local b={capital={version=1,sequence=1,contracts={X={principal=2,safe=3,stage='DEBIT_INTENT'}}}}
local d=D.Readback('POSTWRITE',true,a,b,'X','RETURNED',false)
assert(d.diffPath=='contract.principal' and d.expectedNumber==2 and d.actualNumber==nil and d.actualType=='string')
a.capital.contracts.X.principal=2;a.self=a
assert(D.Readback('POSTWRITE',true,a,b,'X','RETURNED',false).diffPath=='OTHER_RECORD_OR_UNLISTED')
''')
 def test_failed_confirmation_then_refresh_and_reopen_keep_pause(self):
  ui().execute(r'''
LuaEvents.SPC_CapitalOpen(0,9);ack();Controls.StableConfirm.click()
local p=sent[2];capitalView.revision=2;capitalView.stage='HELD';capitalView.canSign=false
capitalView.reason='PROGRESSION_HELD';capitalView.failure={phase='DEBIT_INTENT_WRITE',errorCode='STORE_WRITE_UNCONFIRMED'}
capBackend.lastRequest={token=p.Token,owner=0,city=9,accepted=false,reason='STORE_WRITE_UNCONFIRMED',failure=capitalView.failure}
Events.GameCoreEventPublishComplete.Fire()
assert(Controls.Error.text=='LOC_SPC_CAPITAL_PAUSE_INTENT' and Controls.StableConfirm.disabled and Controls.VentureConfirm.disabled)
Controls.Refresh.click();ack();assert(Controls.Error.text=='LOC_SPC_CAPITAL_PAUSE_INTENT' and #sent==3)
Controls.Close.click();LuaEvents.SPC_CapitalOpen(0,9);ack();assert(Controls.Error.text=='LOC_SPC_CAPITAL_PAUSE_INTENT' and #sent==4)
''')
 def test_new_helper_packaged_no_math_schema_or_timer_changes(self):
  import xml.etree.ElementTree as ET
  x=ET.parse(R/'Mod/SpecializationP0.modinfo')
  for parent in ('./Files','./InGameActions/ImportFiles'):
   self.assertEqual([e.text for e in x.findall(parent+'/File')].count('CapitalInvestmentDiagnostics.lua'),1)
  original=subprocess.check_output(['git','show','8e8b5eb:Mod/CapitalInvestmentModel.lua'],cwd=R)
  self.assertEqual(original,(R/'Mod/CapitalInvestmentModel.lua').read_bytes())
  for name in ('CapitalInvestment','CapitalInvestmentDiagnostics','UI/CapitalInvestmentPanel'):
   s=(R/'Mod'/f'{name}.lua').read_text();self.assertNotIn('SetUpdate',s);self.assertNotIn('collectgarbage',s)
 def test_phase_message_keys_exist_in_both_locales(self):
  import sqlite3,re
  db=sqlite3.connect(':memory:')
  try:
   db.execute('CREATE TABLE LocalizedText(Language TEXT,Tag TEXT,Text TEXT,PRIMARY KEY(Language,Tag))')
   db.executescript((R/'Mod/Text/Commerce.sql').read_text())
   s=(R/'Mod/UI/CapitalInvestmentPanel.lua').read_text()
   for key in set(re.findall(r"'(PAUSE_[A-Z_]+)'",s)):
    for lang in ('zh_Hans_CN','en_US'):
     self.assertIsNotNone(db.execute('SELECT Text FROM LocalizedText WHERE Language=? AND Tag=?',(lang,'LOC_SPC_CAPITAL_'+key)).fetchone())
  finally:db.close()

if __name__=='__main__':unittest.main()
