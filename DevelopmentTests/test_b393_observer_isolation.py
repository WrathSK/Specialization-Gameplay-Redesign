"""Actual city/fact/UI composition under absent raw helpers; no native game PASS."""
from pathlib import Path
from contextlib import contextmanager
from unittest.mock import patch
import unittest
from refactor_harness import ROOT,TrackedLua51

@contextmanager
def restricted():
 # Native doubles use rawset for event setup; actual production must not rely on it.
 # Lexical nils simulate the missing globals without rewriting module bodies.
 prefixes=tuple(p.read_text()[:100] for p in (ROOT/'Mod').rglob('*.lua'))
 original=TrackedLua51.execute
 def execute(vm,source,*args,**kwargs):
  if isinstance(source,str) and source.startswith(prefixes):
   source='local rawget,rawset,rawequal=nil,nil,nil\n'+source
  return original(vm,source,*args,**kwargs)
 with patch.object(TrackedLua51,'execute',execute):yield

def actual():
 from test_refactor_s9a3a import runtime
 return runtime()

class Isolation(unittest.TestCase):
 def setUp(self):
  self.profile=restricted();self.profile.__enter__()
 def tearDown(self):self.profile.__exit__(None,None,None)
 def test_new_city_four_first_districts_and_investments(self):
  import test_store_write_boundaries as cases
  with patch.object(cases,'LuaRuntime',TrackedLua51):v=cases.fixture()
  v.execute("""
   T.start();T.governor(4);a=shared.InvestmentAction
   local rows={{'RESEARCH','DISTRICT_CAMPUS'},{'CULTURE','DISTRICT_THEATER'},
    {'COMMERCE','DISTRICT_COMMERCIAL_HUB'},{'INDUSTRY','DISTRICT_INDUSTRIAL_ZONE'}}
   for i,row in ipairs(rows)do
    local c=T.fresh(i);T.register(c)
    local before=shared.EffectiveFacts.Read(0,c);assert(before.specialization=='NONE'and before.potential==0)
    T.complete(c,row[2]);local f=shared.EffectiveFacts.Read(0,c)
    assert(f.specialization==row[1]and f.potential==1 and f.active==1)
    for j=1,3 do T.invest(c,99000+i*10+j)end
    f=shared.EffectiveFacts.Read(0,c);assert(f.specialization==row[1]and f.potential==4 and f.active==4)
    local saved=T.encode(T.record(c));local w=T.writes()
    for n=1,20 do shared.EffectiveFacts.Read(0,c)end
    assert(T.encode(T.record(c))==saved and T.writes()==w)
   end
  """)
 def test_note_callback_and_diagnostic_setter_throw_do_not_change_core_read(self):
  v=actual();v.execute("""
   local f=shared.EffectiveFacts;local h=T.encode(T.record(ca));local w=T.writes()
   f.NoteTrainingReference=function()error('NOTE_FAILED')end
   setmetatable(f,{__newindex=function(_,k)if k=='trainingReferenceObservationError'or k=='trainingObservationError'then error('DIAGNOSTIC_FAILED')end end})
   assert(shared.CityProgressionStore.Base(0,ca).specialization=='RESEARCH')
   assert(f.Read(0,ca).specialization=='RESEARCH'and T.writes()==w and T.encode(T.record(ca))==h)
  """)
 def test_note_lookup_exception_is_non_authoritative(self):
  v=actual();v.execute("local f=shared.EffectiveFacts;f.NoteTrainingReference=nil;setmetatable(f,{__index=function(_,k)if k=='NoteTrainingReference'then error('NOTE_LOOKUP_FAILED')end end});assert(f.Read(0,ca).specialization=='RESEARCH')")
 def test_observer_lookup_exception_is_non_authoritative(self):
  v=actual();v.execute("local s=shared.CityProgressionStore;s.ObserveTrainingFacts=nil;setmetatable(s,{__index=function(_,k)if k=='ObserveTrainingFacts'then error('OBSERVER_LOOKUP_FAILED')end end});assert(shared.EffectiveFacts.Read(0,ca).specialization=='RESEARCH')")
 def test_original_error_object_survives_observer_and_diagnostic_errors(self):
  v=actual();v.execute("""
   local f=shared.EffectiveFacts;local failure={reason='ORIGINAL_NATIVE_ERROR'}
   local get=ca.GetProperty;ca.GetProperty=function(c,k)if k==M.Keys.TOKEN then error(failure)end;return get(c,k)end
   f.NoteTrainingReference=function()error('OBSERVER_ERROR')end
   setmetatable(f,{__newindex=function()error('DIAGNOSTIC_ERROR')end})
   local ok,e=pcall(shared.CityProgressionStore.Base,0,ca);assert(not ok and e==failure)
   local good,why=pcall(f.Read,0,ca);assert(not good and why==failure)
  """)
 def test_binding_observer_failure_does_not_mask_native_value(self):
  from test_refactor_s9a3a import runtime
  original=TrackedLua51.execute
  def broken(vm,source,*a,**kw):
   if isinstance(source,str)and 'local function CreateProgressionRecord' in source:
    original(vm,"local old=SPCIdentityEqual.Same;SPCIdentityEqual.Same=function(a,b)if brokenBinding then error('OBSERVER_COMPARE_FAILED')end;return old(a,b)end")
   return original(vm,source,*a,**kw)
  with patch.object(TrackedLua51,'execute',broken):v=runtime()
  v.execute("brokenBinding=true;assert(shared.CityProgressionStore.Base(0,ca).specialization=='RESEARCH');assert(shared.EffectiveFacts.Read(0,ca).specialization=='RESEARCH')")
 def test_actual_ui_requests_replies_and_same_turn_promotion(self):
  import test_culture_institutions as display
  from test_b265_city_presentation import presentation
  with patch.object(display,'LuaRuntime',TrackedLua51):v=presentation()
  v.execute("assert(Controls.ActiveIcon.icon=='ICON_SPC_LEVEL_CULTURE_3');nativeActive=4;Events.GovernorPromoted(0);Events.GameCoreEventPublishComplete();assert(rows.items[4].State.text=='当前'and Controls.ActiveIcon.icon=='ICON_SPC_LEVEL_CULTURE_4');for _,r in ipairs(trace)do assert(r.stage~='INSTITUTION_UI_FAILURE')end;local n=#requests;for i=1,1000 do Events.GameCoreEventPublishComplete()end;assert(#requests==n)")
 def test_no_optional_raw_calls_remain_in_production(self):
  import re
  for p in (ROOT/'Mod').rglob('*.lua'):self.assertIsNone(re.search(r'\braw(?:get|set|equal)\s*\(',p.read_text()),str(p))


class FailureEvidence(unittest.TestCase):
 def producer(self):
  from test_refactor_s9c6a import Producer
  c=Producer().setup();c.load('ExpeditionTrainingDiagnostics')
  c.execute("trace={};shared.PresentationDiagnostics={Record=function(stage,row)row.stage=stage;trace[#trace+1]=row end}")
  return c
 def test_allowlisted_failure_fields_never_stringify_objects_or_keep_paths(self):
  from refactor_harness import Context
  c=Context();c.load('ExpeditionTrainingDiagnostics');c.execute("""
   local d=SPCExpeditionTrainingDiagnostics
   local e=d.Failure("/private/example/CityProgressionStore.lua:332: attempt to call global 'rawset' (a nil value)",'CITY_FACTS')
   assert(e.errorFile=='CityProgressionStore.lua'and e.errorLine==332 and e.errorClass=='LUA_NIL'and e.errorSymbol=='rawset')
   local f=d.Failure('/private/example/EffectiveFacts.lua:20: EFFECTIVE_FACTS_CHANGED_DURING_READ','CITY_FACTS')
   assert(f.errorCode=='EFFECTIVE_FACTS_CHANGED_DURING_READ'and f.errorClass=='CONTRACT'and f.errorFile=='EffectiveFacts.lua')
   local g=d.Failure("/private/user/PrivateModule.lua:19: attempt to call global 'privateSymbol' (a nil value)",'CITY_FACTS')
   assert(g.errorFile=='UNKNOWN'and g.errorSymbol==nil)
   local x=d.Failure(setmetatable({},{__tostring=function()error('MUST_NOT_STRINGIFY')end}),'CITY_FACTS')
   assert(x.errorCode=='READ_ERROR'and x.errorFile=='UNKNOWN')
   local n=d.Failure('NetworkBridge.lua:44: NETWORK_PENDING','NETWORK')
   assert(n.errorCode=='NETWORK_PENDING'and n.errorFile=='NetworkBridge.lua')
   for _,row in ipairs({e,f,g,x,n})do for _,v in pairs(row)do if type(v)=='string'then assert(not v:find('/private'))end end end
  """)
 def test_actual_producer_keeps_unavailable_reply_and_records_original_cause_once(self):
  c=self.producer();c.execute("""
   onFacts=function()error("CityProgressionStore.lua:332: attempt to call global 'rawset' (a nil value)")end
   runRequest(0,pp());local v=d.Presentations.Take(0,'REQUEST').presentation
   assert(v.error and v.active==nil and v.potential==nil and #trace==1)
   local e=trace[1];assert(e.stage=='INSTITUTION_FACTS'and e.readStatus=='UNAVAILABLE'and e.errorFile=='CityProgressionStore.lua'and e.errorLine==332 and e.errorSymbol=='rawset')
   assert(reads.facts==1 and reads.summary==0 and reads.archive==0 and reads.find==1)
  """)
 def test_success_adds_no_failure_fields_or_extra_reads(self):
  c=self.producer();c.execute("runRequest(0,pp());local v=d.Presentations.Take(0,'REQUEST').presentation;assert(v.active==4 and #trace==1 and trace[1].readStatus=='READY'and trace[1].errorCode==nil and trace[1].errorSymbol==nil);assert(reads.facts==1 and reads.summary==1 and reads.archive==1 and reads.find==1)")
 def test_throwing_formatter_constructor_or_sink_cannot_change_original_reply(self):
  cases=[("SPCExpeditionTrainingDiagnostics.Failure=function()error('FORMAT_FAILED')end",True),
   ("shared.PresentationDiagnostics=nil;SPCExpeditionTrainingDiagnostics.New=function()error('NEW_FAILED')end",False),
   ("shared.PresentationDiagnostics.Record=function()error('SINK_FAILED')end",False)]
  for mutation,fail in cases:
   c=self.producer()
   c.execute(mutation+(";onFacts=function()error('ORIGINAL_FACT_FAILURE')end"if fail else '')+";assert(pcall(runRequest,0,pp()));local v=d.Presentations.Take(0,'REQUEST').presentation;assert(reads.facts==1 and reads.find==1);"+("assert(v.error:find('ORIGINAL_FACT_FAILURE',1,true)and v.active==nil)"if fail else"assert(not v.error and v.active==4)"))
 def test_actual_trace_serialization_and_reader_preserve_fields_with_existing_bounds(self):
  import importlib.util
  from refactor_harness import TrackedLua51
  import test_expedition_training_diagnostics as old
  with patch.object(old,'LuaRuntime',TrackedLua51):v=old.fixture()
  v.execute("local e=M.Failure(\"CityProgressionStore.lua:332: attempt to call global 'rawset' (a nil value)\",'CITY_FACTS');e.readStatus='UNAVAILABLE';a.Record('INSTITUTION_FACTS',e);savedLine=last().line;for i=1,1000 do e.count=i;a.Record('INSTITUTION_FACTS',e)end;assert(trace().sequence==M.TURN_LIMIT+1 and #trace().entries==M.KEEP and trace().suppressed==1002-M.TURN_LIMIT);unchanged()")
  spec=importlib.util.spec_from_file_location('b393_reader',ROOT/'tools/read_expedition_trace.py');reader=importlib.util.module_from_spec(spec);spec.loader.exec_module(reader)
  line=v.eval('savedLine');self.assertIn('errorSymbol=rawset',line);self.assertIn('errorFile=CityProgressionStore.lua',line)
  self.assertEqual(reader.training_line(line),line)

class CollectorEvidence(unittest.TestCase):
 def test_failure_metadata_survives_actual_local_collection_and_dedup(self):
  import tempfile
  from test_expedition_trace_collector import collector
  row='[SPC][B205][TRAIN] seq=2 stage=INSTITUTION_FACTS readStatus=UNAVAILABLE errorFile=CityProgressionStore.lua errorLine=332 errorClass=LUA_NIL errorSymbol=rawset'
  with tempfile.TemporaryDirectory(dir=ROOT/'local')as tmp:
   session=collector.Session(root=Path(tmp),stamp='B393_OFFLINE')
   try:
    self.assertEqual(collector.train_line(row),row)
    session.add(row,'snapshot');session.add(row,'live')
    self.assertEqual(session.record_total,1)
    saved=(session.directory/'records.log').read_text()
    self.assertEqual(saved.count('errorSymbol=rawset'),1)
    self.assertIn('INSTITUTION_FACTS=1',session.summary('OFFLINE_TEST'))
   finally:session.close()

if __name__=='__main__':unittest.main(verbosity=2)

