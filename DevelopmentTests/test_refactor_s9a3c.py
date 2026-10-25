"""Passive scoped EF read observations; original results/cache/native scope remain authoritative."""
from contextlib import contextmanager,nullcontext
from hashlib import sha256
from pathlib import Path
from unittest.mock import patch
import json,subprocess,unittest
from refactor_harness import ROOT,TrackedLua51,SOURCES,legacy_source_observation,measure
from test_refactor_s9a3a import runtime

BASE='5677cd5'
@contextmanager
def before():
 p=ROOT/'Mod/EffectiveFacts.lua';old=subprocess.check_output(['git','show',BASE+':Mod/EffectiveFacts.lua'],cwd=ROOT,text=True);read,execute=Path.read_text,TrackedLua51.execute;h=sha256(old.encode()).hexdigest()
 def source(f,*a,**kw):return old if f==p else read(f,*a,**kw)
 def run(vm,s,*a,**kw):
  if sha256(s.encode()if isinstance(s,str)else s).hexdigest()==h:SOURCES[h]='historical/'+BASE+'/Mod/EffectiveFacts.lua'
  return execute(vm,s,*a,**kw)
 with patch.object(Path,'read_text',source),patch.object(TrackedLua51,'execute',run),legacy_source_observation():yield

class Observations(unittest.TestCase):
 def test_base_failure_and_new_actual_read_recover_without_idle_resampling_or_writes(self):
  v=runtime();v.execute("f=shared.EffectiveFacts;f.Read(0,ca);assert(sa():find('FACTS_CONFIRMED',1,true));local get=s.Investment;local failure={message='NATIVE_UNKNOWN'};s.Investment=function()error(failure)end;local ok,e=pcall(f.Read,0,ca);assert(not ok and rawequal(e,failure)and sa():find('FACTS_UNAVAILABLE',1,true));local reads=0;s.Investment=function()reads=reads+1;error(failure)end;local w=T.writes();for i=1,1000 do sa();Events.GameCoreEventPublishComplete.Fire()end;assert(reads==0 and T.writes()==w);s.Investment=get;f.Read(0,ca);assert(sa():find('FACTS_CONFIRMED',1,true)and T.writes()==w)")
 def test_projector_error_false_or_custom_table_never_poison_independent_base(self):
  v=runtime();v.execute("f=shared.EffectiveFacts;f.WithPhase('PROJECTION',function()f.Read(0,ca);local failure={reason='ONLY_PROJECTOR'};local ok,e=pcall(f.Inspect,0,ca,function()error(failure)end);assert(not ok and rawequal(e,failure)and sa():find('FACTS_CONFIRMED',1,true));assert(f.Inspect(0,ca,function()return false end)==false);local out=f.Inspect(0,ca,function()return {owner=999,cityID=999,x=999,y=999,token='FAKE',activeStatus='UNKNOWN'}end);assert(out.owner==999 and sa():find('FACTS_CONFIRMED',1,true))end)")
 def test_unknown_governor_is_not_confirmed_zero_or_base_exception(self):
  v=runtime();v.execute("a=shared.InvestmentAction;T.invest(ca,99811);T.governor(nil);f=shared.EffectiveFacts;local value=f.Read(0,ca);assert(value.active==nil and value.activeStatus=='UNKNOWN_GOVERNOR'and sa():find('FACTS_UNKNOWN',1,true));T.governor(4);assert(f.Read(0,ca).active==2 and sa():find('FACTS_CONFIRMED',1,true))")
 def test_nested_same_city_newer_confirmed_observation_survives_outer_failure(self):
  v=runtime();v.execute("f=shared.EffectiveFacts;local stamp=s.FactStamp;local ok=pcall(function()f.WithPhase('NESTED',function()f.Inspect(0,ca,function()f.Read(0,ca);s.FactStamp=function()error('OUTER_WINDOW_FAILED')end;return true end)end)end);s.FactStamp=stamp;assert(not ok and sa():find('FACTS_CONFIRMED',1,true));assert(f.Read(0,ca).specialization=='RESEARCH')")
 def test_nested_different_city_does_not_suppress_outer_scoped_failure(self):
  v=runtime();v.execute("f=shared.EffectiveFacts;local stamp=s.FactStamp;local ok=pcall(function()f.WithPhase('CROSS_CITY',function()f.Inspect(0,ca,function()f.Read(0,cb);s.FactStamp=function(pid,c)if c==ca then error('ONLY_A_FAILED')end;return stamp(pid,c)end;return true end)end)end);s.FactStamp=stamp;assert(not ok and sa():find('FACTS_UNAVAILABLE',1,true)and sb():find('FACTS_CONFIRMED',1,true))")
 def test_observer_error_changes_neither_original_return_nor_error_object_and_releases_frame(self):
  v=runtime();v.execute("f=shared.EffectiveFacts;local observe=s.ObserveTrainingFacts;s.ObserveTrainingFacts=function()error('OBSERVER_FAILED')end;local value=f.Read(0,ca);assert(value.specialization=='RESEARCH'and f.trainingObservationError=='TRAINING_OBSERVATION_FAILED');local get=s.Investment;local failure={why='ORIGINAL'};s.Investment=function()error(failure)end;local ok,e=pcall(f.Read,0,ca);assert(not ok and rawequal(e,failure));s.Investment=get;s.ObserveTrainingFacts=observe;assert(f.Read(0,ca).specialization=='RESEARCH'and f.trainingObservationError==nil and sa():find('FACTS_CONFIRMED',1,true))")
 def test_unscoped_early_failure_never_guesses_another_city_or_resamples_native(self):
  v=runtime();v.execute("f=shared.EffectiveFacts;f.Read(0,ca);f.Read(0,cb);local a,b=sa(),sb();local observe=s.ObserveTrainingFacts;local calls=0;s.ObserveTrainingFacts=function(...)calls=calls+1;return observe(...)end;assert(not pcall(f.Read,1,ca));assert(calls==0 and sa()==a and sb()==b)")
 def test_reference_note_error_does_not_change_body_or_attach_unproved_failure(self):
  v=runtime();v.execute("f=shared.EffectiveFacts;local note=f.NoteTrainingReference;f.NoteTrainingReference=function()error('NOTE_FAILED')end;assert(f.Read(0,ca).specialization=='RESEARCH'and f.trainingReferenceObservationError=='TRAINING_REFERENCE_NOTE_FAILED');local before=sa();local get=s.Investment;s.Investment=function()error('BODY_FAILED_BEFORE_BASE')end;assert(not pcall(f.Read,0,ca)and sa()==before);s.Investment=get;f.NoteTrainingReference=note;f.Read(0,ca);assert(f.trainingReferenceObservationError==nil)")
 def test_service_restart_rejects_old_issuer_and_new_actual_read_recovers(self):
  v=runtime();v.execute("f=shared.EffectiveFacts;f.Read(0,ca);local oldIssuer=f.TrainingObservationIssuer;SPCEffectiveFacts.Start(P,shared);local next=shared.EffectiveFacts;assert(sa():find('FACTS_UNOBSERVED',1,true));f.Read(0,ca);assert(sa():find('FACTS_UNOBSERVED',1,true));next.Read(0,ca);assert(sa():find('FACTS_CONFIRMED',1,true));assert(not s.ObserveTrainingFacts(0,aid,ax,ay,T.record(ca).base.token,'FACTS_UNAVAILABLE',oldIssuer,999999)and sa():find('FACTS_CONFIRMED',1,true))")
 def test_observation_depth_limit_never_rejects_original_recursive_reads(self):
  v=runtime();v.execute("f=shared.EffectiveFacts;local observe=s.ObserveTrainingFacts;local calls=0;s.ObserveTrainingFacts=function(...)calls=calls+1;return observe(...)end;local function nested(n)return f.Inspect(0,ca,function()if n==0 then return 'DONE'end;return nested(n-1)end)end;assert(nested(12)=='DONE'and calls==8 and sa():find('FACTS_BUDGET_UNKNOWN',1,true));assert(f.Read(0,cb).specialization=='CULTURE')")
 def test_success_and_failure_frames_do_not_retain_native_city_surrogates_after_return(self):
  for fail in (False,True):
   v=runtime();v.execute("f=shared.EffectiveFacts;weak=setmetatable({},{__mode='v'});do local temp={};for k,x in pairs(ca)do temp[k]=x end;weak[1]=temp;local old=s.Investment;if ... then s.Investment=function()error('TEMPORARY')end end;pcall(f.Read,0,temp);s.Investment=old;temp=nil end;collectgarbage('collect');assert(weak[1]==nil)",fail)

 def test_overflow_failure_cannot_be_overwritten_by_older_same_city_confirmation(self):
  v=runtime();v.execute("f=shared.EffectiveFacts;local original=s.Investment;local function nested(n)return f.Inspect(0,ca,function()if n==0 then s.Investment=function()error('DEEP_FAILURE')end;local ok=pcall(f.Read,0,ca);s.Investment=original;assert(not ok);return 'CAUGHT'end;return nested(n-1)end)end;assert(nested(7)=='CAUGHT'and sa():find('FACTS_BUDGET_UNKNOWN',1,true));f.Read(0,ca);assert(sa():find('FACTS_CONFIRMED',1,true))")
 def test_overflow_other_city_failure_does_not_downgrade_unrelated_ancestors(self):
  v=runtime();v.execute("f=shared.EffectiveFacts;f.Read(0,ca);f.Read(0,cb);local before=sb();local original=s.Investment;local function nested(n)return f.Inspect(0,ca,function()if n==0 then s.Investment=function(pid,c)if c==cb then error('ONLY_DEEP_B')end;return original(pid,c)end;local ok=pcall(f.Read,0,cb);s.Investment=original;assert(not ok);return 'CAUGHT'end;return nested(n-1)end)end;assert(nested(7)=='CAUGHT'and sa():find('FACTS_CONFIRMED',1,true)and sb()==before and f.trainingObservationOverflows==1);f.Read(0,cb);assert(sb():find('FACTS_CONFIRMED',1,true))")

class Differential(unittest.TestCase):
 def test_actual_values_native_getters_and_store_bytes_match_B366(self):
  out=[]
  for old in (True,False):
   with before()if old else nullcontext():v=runtime()
   v.execute("f=shared.EffectiveFacts;io=0;for _,c in ipairs({ca,cb})do for _,name in ipairs({'GetOwner','GetID','GetX','GetY','GetProperty'})do local get=c[name];c[name]=function(...)io=io+1;return get(...)end end end;local get=Game.GetProperty;Game.GetProperty=function(...)io=io+1;return get(...)end;local w=T.writes();f.WithPhase('DIFF',function()one=f.Read(0,ca);two=f.Inspect(0,ca,function(v)return {specialization=v.specialization,potential=v.potential,active=v.active}end);three=f.Read(0,cb)end);encoded=T.encode({one,two,three});saved=T.encode(T.record(ca));assert(T.writes()==w)")
   out.append(tuple(v.eval(x)for x in ('encoded','saved','io')))
  self.assertEqual(out[0],out[1])
  measure('S9a3c_actual_fact_observation',{'baseline':BASE,'same_values_native_getters_saved_bytes':True,'native_getter_calls_before_after':[out[0][2],out[1][2]],'extra_native_reads':0,'fact_resamples':0,'new_city_maps':0,'frame_depth':8,'frame_tables_per_read_at_most':1,'UI_global_removed':False})


def load_tests(loader,standard,pattern):
 selection=json.loads((ROOT/'DevelopmentTests/refactor_selection.json').read_text())
 return unittest.TestSuite([standard,unittest.TestSuite(loader.loadTestsFromName(name)for name in selection['stages']['S9a3b'])])

if __name__=='__main__':unittest.main()
