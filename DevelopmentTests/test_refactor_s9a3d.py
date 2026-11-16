"""Real Store/EF/Gate/Training input coverage; no UI consumer or native PASS."""
from contextlib import contextmanager,nullcontext
from hashlib import sha256
from pathlib import Path
from unittest.mock import patch
import json,subprocess,unittest
from refactor_harness import ROOT,TrackedLua51,SOURCES,legacy_source_observation,measure
from test_refactor_s9a3a import runtime as store_runtime
from test_refactor_s9b3 import profile
import test_expedition_training as original

BASE='a2d9605'
@contextmanager
def before():
 p=ROOT/'Mod/ExpeditionTraining.lua';old=subprocess.check_output(['git','show',BASE+':Mod/ExpeditionTraining.lua'],cwd=ROOT,text=True);read,execute=Path.read_text,TrackedLua51.execute;h=sha256(old.encode()).hexdigest()
 def source(f,*a,**kw):return old if f==p else read(f,*a,**kw)
 def run(vm,s,*a,**kw):
  if sha256(s.encode()if isinstance(s,str)else s).hexdigest()==h:SOURCES[h]='historical/'+BASE+'/Mod/ExpeditionTraining.lua'
  return execute(vm,s,*a,**kw)
 with patch.object(Path,'read_text',source),patch.object(TrackedLua51,'execute',run),legacy_source_observation():yield

SETUP=r"""
source=cb;a=shared.InvestmentAction;T.invest(cb,99921);T.invest(cb,99922);T.invest(cb,99923);T.governor(4)
GameEvents=GameEvents or {};local function blank()return {Add=function()end}end
GameEvents.SPC_ExpeditionGateRequest=blank();GameEvents.SPC_ExpeditionTrainingRequest=blank()
units={};unitScans=0
Players[0].GetUnits=function()return {Members=function()unitScans=unitScans+1;return pairs(units)end,FindID=function(_,id)return units[id]end}end
a=shared.InvestmentAction
ExposedMembers=ExposedMembers or {};ExposedMembers.SPC_P0=shared
SPCExpeditionTrainingDiagnostics=nil
include('ExpeditionSpyStore');include('ExpeditionSpyGate');SPCExpeditionSpyGate.Start(P,shared)
capacity=shared.ExpeditionGate.Training;capacity.Read(0)
include('ExpeditionTraining');SPCExpeditionTraining.Start(P,shared)
function train(action,token)shared.ExpeditionTraining.Request(0,{Action=action,Token=token,CityID=source:GetID()});return ExposedMembers.SPC_ExpeditionTrainingReply end
"""
def runtime():
 v=store_runtime();v.execute(SETUP);return v

FINAL="""
facts=shared.EffectiveFacts;local read=facts.Read;local raw=source.GetProperty
facts.Read=function(...)local f=read(...);finalRead=true;return f end
source.GetProperty=function(c,k)if finalRead and k=='SPC_DEV_BINDING_B013_TOKEN'then finalRead=false;return finalValue(c,k,raw)end;return raw(c,k)end
"""

class Binding(unittest.TestCase):
 def test_final_absent_mismatch_throw_remain_distinct_from_confirmed_EF_and_recover(self):
  for mode in ('ABSENT','MISMATCH','UNAVAILABLE'):
   v=runtime();v.execute(FINAL);v.execute("mode=...;failure={why='ORIGINAL_BINDING_FAILURE'};finalValue=function(c,k,raw)if mode=='ABSENT'then return nil elseif mode=='MISMATCH'then return 'OTHER'end;error(failure)end;local w=T.writes();local r=train('SYNC','FAIL');local stamp=s.TrainingInputStamp(0,bid,bx,by);assert(not r.eligible and r.input and r.input.storeInput==stamp and stamp:find('|'..mode..'|FACTS_CONFIRMED',1,true)and T.writes()==w);finalValue=function(c,k,raw)return raw(c,k)end;assert(pcall(s.Base,0,source));assert(s.TrainingInputStamp(0,bid,bx,by):find('|MATCH|',1,true));r=train('SYNC','RECOVER');assert(r.eligible and r.input and T.writes()==w)",mode)
 def test_final_reserve_binding_throw_preserves_original_error_and_no_queue_or_store_action(self):
  v=runtime();v.execute(FINAL);v.execute("failure={why='ORIGINAL'};finalValue=function()error(failure)end;local w=T.writes();ExposedMembers.SPC_ExpeditionQueueRead=function()error('QUEUE_MUST_NOT_RUN')end;local r=train('RESERVE','R');assert(r.error==tostring(failure)and T.writes()==w and s.TrainingInputStamp(0,bid,bx,by):find('|UNAVAILABLE|',1,true))")
 def test_nested_newer_binding_observation_cannot_be_overwritten_by_older_result(self):
  v=runtime();v.execute(FINAL);v.execute("finalValue=function(c,k,raw)assert(pcall(s.Base,0,c));return nil end;local r=train('SYNC','NESTED');assert(not r.eligible and s.TrainingInputStamp(0,bid,bx,by):find('|MATCH|',1,true))")
 def test_binding_ticket_cannot_cross_loss_return_with_same_visible_reference(self):
  v=runtime();v.execute("local token=T.record(cb).base.token;local old=s.BeginTrainingBindingObservation(0,bid,bx,by,token);local _,before=s.TrainingInputStamp(0,bid,bx,by);T.loss(source,9,900);source.s.ref.owner=0;source.s.ref.cityID=bid;Events.CityTransfered.Fire(0,bid,9);local _,after=s.TrainingInputStamp(0,bid,bx,by);assert(before~=after and not s.FinishTrainingBindingObservation(0,bid,bx,by,old,true,token));assert(not s.TrainingInputStamp(0,bid,bx,by):find('|MATCH|',1,true))")
 def test_opaque_ticket_rejects_old_scope_and_token_without_native_work(self):
  v=runtime();v.execute("local token=T.record(cb).base.token;local old=s.BeginTrainingBindingObservation(0,bid,bx,by,token);assert(old);local next=s.BeginTrainingBindingObservation(0,bid,bx,by,token);assert(next and next~=old);assert(s.FinishTrainingBindingObservation(0,bid,bx,by,next,true,token));assert(not s.FinishTrainingBindingObservation(0,bid,bx,by,old,false,nil));assert(not s.BeginTrainingBindingObservation(1,bid,bx,by,token)and not s.BeginTrainingBindingObservation(0,bid,bx,by,'WRONG'));local before=s.TrainingInputStamp(0,bid,bx,by);assert(not s.FinishTrainingBindingObservation(0,bid,bx+1,by,next,false,nil)and s.TrainingInputStamp(0,bid,bx,by)==before)")
 def test_ticket_identity_ignores_forged_equality_metamethod(self):
  v=runtime();v.execute("local token=T.record(cb).base.token;local old=s.BeginTrainingBindingObservation(0,bid,bx,by,token);local next=s.BeginTrainingBindingObservation(0,bid,bx,by,token);local meta={__eq=function()return true end};setmetatable(old,meta);setmetatable(next,meta);assert(old==next and not rawequal(old,next));assert(not s.FinishTrainingBindingObservation(0,bid,bx,by,old,false,nil));assert(s.FinishTrainingBindingObservation(0,bid,bx,by,next,true,token)and s.TrainingInputStamp(0,bid,bx,by):find('|MATCH|',1,true))")
 def test_observer_throw_does_not_change_original_eligibility(self):
  for method in ('BeginTrainingBindingObservation','FinishTrainingBindingObservation'):
   v=runtime();v.execute("local method=...;s[method]=function()error('OBSERVER_ONLY')end;local w=T.writes();assert(train('SYNC','OK').eligible and T.writes()==w)",method)
 def test_pure_core_includes_real_identity_investment_but_not_generic_revision(self):
  v=store_runtime();v.execute("a=shared.InvestmentAction;local _,core=s.TrainingInputStamp(0,aid,ax,ay);local n=M.Copy(T.record(ca));n.revision=n.revision+1;assert(saveCandidate(ca,n));local _,same=s.TrainingInputStamp(0,aid,ax,ay);assert(core==same);T.invest(ca,99925);local _,next=s.TrainingInputStamp(0,aid,ax,ay);assert(core~=next);local w=T.writes();for i=1,1000 do s.TrainingInputStamp(0,aid,ax,ay)end;assert(T.writes()==w)")

class Receipts(unittest.TestCase):
 def test_sync_receipt_covers_post_observation_inputs_and_duplicate_does_not_resample(self):
  v=runtime();v.execute("local w=T.writes();local r=train('SYNC','ONE');local full=s.TrainingInputStamp(0,bid,bx,by);assert(r.eligible and r.input.version==1 and r.input.owner==0 and r.input.cityID==bid and r.input.x==bx and r.input.y==by and r.input.turn==T.now()and r.input.storeInput==full and r.input.capacityInput==capacity.CapacityInputStamp(0));for k,value in pairs(r.input)do assert(type(value)~='table'and type(value)~='function'and type(value)~='userdata')end;local scans=unitScans;assert(train('SYNC','ONE')==r and unitScans==scans and T.writes()==w)")
 def test_unit_event_during_original_capacity_scan_prevents_newest_stamp_being_swallowed(self):
  v=runtime();v.execute("local get=Players[0].GetUnits;local once=true;Players[0].GetUnits=function(...)local collection=get(...);local members=collection.Members;collection.Members=function(...)if once then once=false;capacity.MarkUnitCapacity(0)end;return members(...)end;return collection end;local r=train('SYNC','RACE');assert(r.eligible and r.input==nil);r=train('SYNC','FRESH');assert(r.eligible and r.input and unitScans==2)")
 def test_confirmed_source_loss_during_capacity_read_invalidates_receipt(self):
  v=runtime();v.execute("local get=Players[0].GetUnits;Players[0].GetUnits=function(...)local v=get(...);Players[0].GetUnits=get;T.loss(source,9,900);return v end;local r=train('SYNC','LOSS');assert(r.eligible and r.input==nil and T.record(cb).stage=='HELD_TRANSFER')")
 def test_loss_return_inside_final_binding_is_not_same_covered_lifecycle(self):
  v=runtime();v.execute(FINAL);v.execute("finalValue=function(c,k,raw)local value=raw(c,k);T.loss(source,9,900);source.s.ref.owner=0;source.s.ref.cityID=bid;Events.CityTransfered.Fire(0,bid,9);return value end;local r=train('SYNC','LOSS_RETURN');assert(r.eligible and not r.input and T.record(cb).stage=='ACTIVE')")
 def test_new_successful_fact_with_different_ACTIVE_is_not_swallowed_as_same_confirmed_state(self):
  v=runtime();v.execute("local get=Players[0].GetUnits;Players[0].GetUnits=function(...)Players[0].GetUnits=get;T.governor(1);assert(shared.EffectiveFacts.Read(0,source).active==1);return get(...)end;local r=train('SYNC','NEW_CONFIRMED');assert(r.eligible and not r.input);r=train('SYNC','CURRENT');assert(not r.eligible and r.input)")
 def test_new_fact_failure_during_capacity_scan_is_not_absorbed(self):
  v=runtime();v.execute("local get=Players[0].GetUnits;Players[0].GetUnits=function(...)Players[0].GetUnits=get;local inv=s.Investment;s.Investment=function()error('NEW_FACT_FAILURE')end;assert(not pcall(shared.EffectiveFacts.Read,0,source));s.Investment=inv;return get(...)end;local r=train('SYNC','NEW_UNKNOWN');assert(r.eligible and r.input==nil and s.TrainingInputStamp(0,bid,bx,by):find('FACTS_UNAVAILABLE',1,true));assert(train('SYNC','RECOVER').input)")
 def test_read_source_method_replacement_omits_receipt_without_changing_result(self):
  for change in ("shared.EffectiveFacts={Read=facts.Read}","shared.ExpeditionTraining={}","shared.CityProgressionStore={}","capacity.CapacityInputStamp=function()return 'NEW'end", "capacity.Available=function()return true end"):
   v=runtime();v.execute(FINAL);v.execute("finalValue=function(c,k,raw)local value=raw(c,k);"+change+";return value end;local r=train('SYNC','RESTART');assert(r.eligible and r.input==nil)")
 def test_unknown_scope_and_turn_failure_do_not_change_original_reply_or_add_retry(self):
  v=runtime();v.execute("local get=source.GetX;source.GetX=function()if once then once=false;error('OBSERVATION_SCOPE_UNKNOWN')end;return get(source)end;once=true;local r=train('SYNC','UNSCOPED');assert(r.eligible and not r.input);assert(train('SYNC','RECOVER').input)")
 def test_source_replaced_at_last_native_clock_boundary_cannot_publish_receipt(self):
  v=runtime();v.execute("local available=capacity.Available;capacity.Available=function(...)local value=available(...);local now=Game.GetCurrentGameTurn;Game.GetCurrentGameTurn=function()shared.EffectiveFacts={Read=shared.EffectiveFacts.Read};return now()end;return value end;local r=train('SYNC','LAST_BOUNDARY');assert(r.eligible and not r.input)")
 def test_newer_request_at_post_run_native_boundary_owns_reply_and_duplicate_cache(self):
  v=runtime();v.execute("local available=capacity.Available;local armed=true;capacity.Available=function(...)local value=available(...);if armed then armed=false;local clock=Game.GetCurrentGameTurn;local calls=0;Game.GetCurrentGameTurn=function()calls=calls+1;if calls==2 then Game.GetCurrentGameTurn=clock;shared.ExpeditionTraining.Request(0,{Action='SYNC',Token='INNER',CityID=bid});innerToken=ExposedMembers.SPC_ExpeditionTrainingReply.token end;return clock()end end;return value end;local r=train('SYNC','OUTER');assert(innerToken=='INNER'and r.token=='INNER'and r.eligible);local scans=unitScans;assert(train('SYNC','INNER')==r and unitScans==scans)")
 def test_non_scalar_capacity_observation_does_not_escape_scalar_receipt(self):
  v=runtime();v.execute("capacity.CapacityInputStamp=function()return {native='DO_NOT_RETAIN'}end;local r=train('SYNC','MALFORMED');assert(r.eligible and not r.input)")
 def test_changed_turn_after_original_capacity_read_omits_receipt(self):
  v=runtime();v.execute("local available=capacity.Available;capacity.Available=function(...)local value=available(...);local now=Game.GetCurrentGameTurn;Game.GetCurrentGameTurn=function()return now()+1 end;return value end;local r=train('SYNC','TURN');assert(r.eligible and not r.input)")

class Differential(unittest.TestCase):
 def test_reserve_order_and_native_getter_counts_match_original_training(self):
  out=[]
  for old in (True,False):
   with before()if old else nullcontext():
    with profile():v=original.fixture()
   v.execute("calls={};local get=city.GetProperty;city.GetProperty=function(...)calls[#calls+1]='binding';return get(...)end;local read=shared.EffectiveFacts.Read;shared.EffectiveFacts.Read=function(...)calls[#calls+1]='facts';return read(...)end;local available=shared.ExpeditionGate.Training.Available;shared.ExpeditionGate.Training.Available=function(...)calls[#calls+1]='capacity';return available(...)end;local q=ExposedMembers.SPC_ExpeditionQueueRead;ExposedMembers.SPC_ExpeditionQueueRead=function(...)calls[#calls+1]='queue';return q(...)end;local r=train('RESERVE','r');assert(r.reserved);result=table.concat(calls,'|')")
   out.append((v.globals().result,v.eval('storeWrites'),v.eval('markerWrites')))
  self.assertEqual(out[0],out[1]);self.assertTrue(out[0][0].startswith('facts|binding|capacity|queue|capacity|facts'))
 def test_real_sync_business_values_and_saved_bytes_match_with_only_three_ref_and_two_clock_reads(self):
  out=[]
  for old in (True,False):
   with before()if old else nullcontext():v=runtime()
   v.execute("count={};for _,name in ipairs({'GetOwner','GetID','GetX','GetY','GetProperty'})do local get=source[name];source[name]=function(...)count[name]=(count[name]or 0)+1;return get(...)end end;local now=Game.GetCurrentGameTurn;Game.GetCurrentGameTurn=function(...)count.clock=(count.clock or 0)+1;return now(...)end;local r=train('SYNC','DIFF');business=tostring(r.eligible)..':'..r.phase;bytes=T.encode(T.record(source))")
   out.append((v.globals().business,v.globals().bytes,dict(v.globals().count)))
  self.assertEqual(out[0][:2],out[1][:2]);delta={k:out[1][2][k]-v for k,v in out[0][2].items()};self.assertEqual(delta,{'GetOwner':0,'GetID':1,'GetX':1,'GetY':1,'GetProperty':0,'clock':2})
  measure('S9a3d_actual_Training_SYNC',{'baseline':BASE,'same_business_values_saved_bytes':True,'additional_ref_scalar_getters':3,'additional_clock_getters':2,'extra_fact_samples':0,'extra_unit_enumerations':0,'receipt_is_admission_authority':False,'UI_migrated':False})


def load_tests(loader,standard,pattern):
 selection=json.loads((ROOT/'DevelopmentTests/refactor_selection.json').read_text())
 return unittest.TestSuite([standard,unittest.TestSuite(loader.loadTestsFromName(name)for name in selection['stages']['S9a3c'])])
if __name__=='__main__':unittest.main()
