"""Callback-only cell ordering before native slot/consumer wiring."""
import unittest
from refactor_harness import ROOT,Context,measure
from test_refactor_s9g1 import SETUP,Codec

SETUP_CELL="""
raw=nil;readCalls=0;writeCalls=0;receiver={reference='receiver-reference',stamp='receiver-lifecycle'}
function now()return receiver end
function get()readCalls=readCalls+1;if readCallback then readCallback()end;if readFails then error('READ_UNAVAILABLE')end;if readOverride~=nil then return readOverride end;return raw end
function put(value)writeCalls=writeCalls+1;if onWrite then onWrite(value)end
 if writeMode=='THROW_BEFORE'then error('WRITE_UNKNOWN_BEFORE')end
 if writeMode=='DROP'then return end
 raw=value;if writeMode=='THROW_AFTER'then error('WRITE_UNKNOWN_AFTER')end
end
function cell()return SPCNetworkRecoveryCell.New('COMMERCE',get,put,now)end
d=cell()
function value()local a=commerce();a.sources[2].status='CONFIRMED';return a end
function fresh(gold,sequence)local a=value();a.shape.gold=gold or 15;a.sequence=sequence or 1;return a end
function verified()return true end
function seed()
 local t=assert(d.Begin(fresh(),verified));assert(raw:sub(1,1)=='P'and d.Read({gold=15,access=true}).state=='BUSY');assert(d.Finish(t,verified));return raw
end
"""
def fixture():
 v=Context();v.load('NetworkRecoveryModel');v.load('NetworkRecoveryCell');v.execute(SETUP+SETUP_CELL);return v

class Ordering(unittest.TestCase):
 def test_new_cell_invalidates_without_candidate_facts_before_one_verified_applied_publish(self):
  v=fixture();v.execute("local a=fresh();local t=assert(d.Begin(a,verified));assert(writeCalls==1 and raw:sub(1,1)=='P'and not raw:find('source-reference',1,true));local p=d.Status();assert(p.active and not p.busy);local done=assert(d.Finish(t,function(shape,r)assert(shape.gold==15 and r.stamp==receiver.stamp);return true end));assert(done.sequence==1 and not done.unchanged and writeCalls==2 and raw:sub(1,1)=='A'and d.Read(a.shape).state=='APPLIED'and not d.Status().active);assert(not d.Finish(t,verified))")
  measure('S9g2_new_cell_commit',{'callback_writes':2,'invalidated_before_ticket':True,'candidate_facts_in_pending':False,'actual_carrier_proof_required':True,'automatic_calls':0})
 def test_unchanged_payload_with_new_proposed_sequence_skips_both_writes_but_checks_actual_shape(self):
  v=fixture();v.execute("local original=seed();local w=writeCalls;local n=readCalls;local t=assert(d.Begin(fresh(15,2),verified));local calls=0;local out=assert(d.Finish(t,function(shape)calls=calls+1;assert(shape.gold==15);return true end));assert(writeCalls==w and raw==original and calls==1 and out.unchanged and out.sequence==1);sameReads=readCalls-n")
  measure('S9g2_same_value_budget',{'callback_writes':0,'final_shape_proofs':1,'callback_reads':v.eval('sameReads'),'idle_encoded_cache':False})
 def test_cold_pending_record_exposes_no_old_or_candidate_source_data(self):
  v=fixture();v.execute("seed();local t=assert(d.Begin(fresh(20,2),verified));local other=cell();local r=other.Read({gold=20,access=true});assert(r.state=='INVALIDATED'and r.sequence==2 and r.value==nil);assert(d.Abort(t)and raw:sub(1,1)=='P'and not d.Status().active)")
 def test_old_applied_record_must_match_current_receiver_and_actual_shape(self):
  v=fixture();v.execute("seed();local r=d.Read({gold=14,access=true});assert(r.state=='SHAPE_MISMATCH'and not r.value);receiver.stamp='NEW';r=d.Read({gold=15,access=true});assert(r.state=='STALE_REFERENCE'and not r.value)")
 def test_retained_source_requires_unchanged_previously_applied_fact_not_label_or_unknown(self):
  for mode in ('EMPTY','UNKNOWN','CHANGED','INVALIDATED','RECEIVER'):
   v=fixture();v.execute("mode=...;if mode~='EMPTY'then seed()end;if mode=='UNKNOWN'then local a=fresh();a.sources[2]={status='UNKNOWN'};raw='A'..M.Encode(a)elseif mode=='INVALIDATED'then local t=assert(d.Begin(fresh(20,2),verified));d.Abort(t)elseif mode=='RECEIVER'then receiver.stamp='NEW'end;local a=fresh(20,mode=='EMPTY'and 1 or mode=='INVALIDATED'and 3 or 2);a.receiver=receiver;a.sources[2].status='RETAINED';if mode=='CHANGED'then a.sources[2].domains.DISTRICT_CAMPUS.X=100 end;local w=writeCalls;assert(not d.Begin(a,verified)and writeCalls==w)",mode)
 def test_valid_retained_source_and_fresh_sibling_can_publish_mixed_actual_encoding(self):
  v=fixture();v.execute("seed();local a=fresh(20,2);a.sources[2].status='RETAINED';a.sources[1].domains.DISTRICT_CAMPUS.X=50;local t=assert(d.Begin(a,verified));assert(d.Finish(t,verified));local r=d.Read(a.shape);assert(r.value.sources[2].status=='RETAINED'and r.value.sources[1].domains.DISTRICT_CAMPUS.X==50)")
 def test_input_gate_rejection_or_throw_does_not_invalidate_old_record(self):
  for gate in ('function()return false end',"function()error('INPUT_UNKNOWN')end",'nil'):
   v=fixture();v.execute("local old=seed();local w=writeCalls;assert(not d.Begin(fresh(20,2),"+gate+")and writeCalls==w and raw==old and not d.Status().active)")
 def test_final_proof_rejection_or_throw_keeps_tombstone_and_never_finalizes(self):
  for gate in ('function()return false end',"function()error('CARRIER_UNKNOWN')end",'nil'):
   v=fixture();v.execute("seed();local t=assert(d.Begin(fresh(20,2),verified));local w=writeCalls;local p=raw;assert(not d.Finish(t,"+gate+")and writeCalls==w and raw==p and not d.Status().active)")
 def test_candidate_input_or_gate_mutation_cannot_change_frozen_expected_shape_or_saved_facts(self):
  v=fixture();v.execute("local a=fresh();local t=assert(d.Begin(a,function(candidate)candidate.shape.gold=999;candidate.sources[1].domains.DISTRICT_CAMPUS.X=999;return true end));a.shape.gold=999;a.sources[1].domains.DISTRICT_CAMPUS.X=999;assert(d.Finish(t,function(shape)assert(shape.gold==15);shape.gold=777;return true end));local r=d.Read({gold=15,access=true});assert(r.value.shape.gold==15 and r.value.sources[1].domains.DISTRICT_CAMPUS.X==30.125)")
 def test_wrong_stale_or_cross_cell_ticket_never_grants_commit(self):
  v=fixture();v.execute("local t=assert(d.Begin(fresh(),verified));local other=cell();local w=writeCalls;assert(not other.Finish(t,verified)and not d.Finish({},verified)and writeCalls==w);assert(d.Finish(t,verified));assert(not d.Finish(t,verified)and writeCalls==w+1)")
 def test_abort_has_no_native_writes_and_stale_abort_cannot_touch_next_operation(self):
  v=fixture();v.execute("local t=assert(d.Begin(fresh(),verified));local w=writeCalls;assert(d.Abort(t)and writeCalls==w and not d.Abort(t));local n=assert(d.Begin(fresh(20,2),verified));assert(not d.Abort(t)and d.Status().active);assert(d.Finish(n,verified))")
 def test_read_and_nested_begin_are_blocked_during_callbacks_or_active_ticket(self):
  v=fixture();v.execute("onWrite=function()assert(d.Read({gold=15,access=true}).state=='BUSY');assert(not d.Begin(fresh(),verified))end;local t=assert(d.Begin(fresh(),function()assert(d.Read({gold=15,access=true}).state=='BUSY');assert(not d.Begin(fresh(),verified));return true end));assert(not d.Begin(fresh(),verified));assert(d.Finish(t,function()assert(not d.Abort(t));assert(d.Read({gold=15,access=true}).state=='BUSY');return true end))")
 def test_stale_cas_between_begin_and_finish_cannot_overwrite_newer_cell(self):
  v=fixture();v.execute("local t=assert(d.Begin(fresh(),verified));local newer=fresh(99,2);raw='A'..M.Encode(newer);local old=raw;local w=writeCalls;assert(not d.Finish(t,verified)and raw==old and writeCalls==w and not d.Status().active)")
 def test_same_value_proof_callback_that_changes_cell_still_fails_final_cas(self):
  v=fixture();v.execute("seed();local t=assert(d.Begin(fresh(15,2),verified));local w=writeCalls;assert(not d.Finish(t,function()raw='A'..M.Encode(fresh(99,2));return true end)and writeCalls==w and not d.Status().active)")
 def test_current_receiver_change_in_native_read_invalidation_or_final_proof_blocks_success(self):
  for mode in ('READ','BEGIN_WRITE','FINISH_PROOF','FINISH_WRITE'):
   v=fixture();v.execute("mode=...;if mode=='READ'then readCallback=function()receiver.stamp='NEW'end;assert(d.Read({gold=15,access=true}).state=='UNAVAILABLE');assert(writeCalls==0)elseif mode=='BEGIN_WRITE'then onWrite=function()receiver.stamp='NEW'end;assert(not d.Begin(fresh(),verified)and raw:sub(1,1)=='P')else local t=assert(d.Begin(fresh(),verified));if mode=='FINISH_WRITE'then onWrite=function()receiver.stamp='NEW'end end;assert(not d.Finish(t,function()if mode=='FINISH_PROOF'then receiver.stamp='NEW'end;return true end))end;assert(not d.Status().active)",mode)
 def test_corrupt_future_unsupported_and_unknown_old_read_never_get_recovery_value_or_overwrite(self):
  for raw in ('wrong','', 'Ainvalid','P1:2'):
   v=fixture();v.execute("raw=...;local original=raw;local r=d.Read({gold=15,access=true});assert(r.state=='UNAVAILABLE'and r.value==nil);assert(not d.Begin(fresh(),verified)and raw==original and writeCalls==0)",raw)
  v=fixture();v.execute("readFails=true;assert(d.Read({gold=15,access=true}).state=='UNAVAILABLE');assert(not d.Begin(fresh(),verified)and writeCalls==0)")
 def test_sequence_stale_nonmonotone_and_maximum_exhaustion_never_reset(self):
  v=fixture();v.execute("seed();for _,n in ipairs({1,3,0})do assert(not d.Begin(fresh(20,n),verified))end;local a=fresh();a.sequence=9007199254740990;raw='A'..M.Encode(a);local w=writeCalls;assert(not d.Begin(fresh(20,1),verified)and writeCalls==w)")
 def test_no_idle_native_calls_or_blob_in_public_status(self):
  v=fixture();v.execute("seed();local r,w=readCalls,writeCalls;for i=1,10000 do local s=d.Status();assert(not s.wire and not s.value and not s.raw and not s.active)end;assert(readCalls==r and writeCalls==w)")
 def test_callback_mechanism_does_not_touch_any_native_global_or_Copy_budget(self):
  v=fixture();v.execute("local bad=setmetatable({},{__index=function()error('NATIVE_FORBIDDEN')end});Game=bad;Players=bad;Events=bad;SPCCityIdentityRead=bad;seed();assert(d.Read({gold=15,access=true}).state=='APPLIED')")
 def test_culture_same_protocol_and_family_isolation(self):
  v=fixture();v.execute("local c=SPCNetworkRecoveryCell.New('CULTURE',get,put,now);local a=culture();a.sequence=1;a.sources[2].status='CONFIRMED';local t=assert(c.Begin(a,verified));assert(c.Finish(t,verified));assert(c.Read(a.shape).value.sources[1].civilizations.CIVILIZATION_ROME);assert(d.Read({gold=15,access=true}).state=='UNAVAILABLE'and not d.Begin(fresh(20,2),verified))")

class FailureDirections(unittest.TestCase):
 def test_every_invalidation_write_or_postread_fault_yields_no_ticket_no_automatic_retry(self):
  for mode in ('DROP','THROW_BEFORE','THROW_AFTER','READBACK_THROW','READBACK_STALE'):
   v=fixture();v.execute("mode=...;local old=seed();writeMode=mode;onWrite=function()if mode=='READBACK_THROW'then readFails=true elseif mode=='READBACK_STALE'then readOverride=raw end end;local w=writeCalls;assert(not d.Begin(fresh(20,2),verified));assert(writeCalls==w+1 and not d.Status().active);if mode=='READBACK_STALE'then assert(raw:sub(1,1)=='P'and readOverride~=raw)end;local n=writeCalls;for i=1,1000 do d.Status()end;assert(writeCalls==n)",mode)
 def test_every_finalization_fault_keeps_no_success_and_never_replays_carrier_operation(self):
  for mode in ('DROP','THROW_BEFORE','THROW_AFTER','READBACK_THROW','READBACK_STALE'):
   v=fixture();v.execute("mode=...;seed();local t=assert(d.Begin(fresh(20,2),verified));writeMode=mode;onWrite=function()if mode=='READBACK_THROW'then readFails=true elseif mode=='READBACK_STALE'then readOverride=raw end end;local w=writeCalls;carrierProofs=0;assert(not d.Finish(t,function()carrierProofs=carrierProofs+1;return true end));assert(writeCalls==w+1 and carrierProofs==1 and not d.Status().active);if mode=='READBACK_STALE'then assert(raw:sub(1,1)=='A'and readOverride~=raw)end;assert(not d.Finish(t,verified)and writeCalls==w+1)",mode)
 def test_bad_old_cas_after_successful_input_gate_is_detected_before_invalidation(self):
  v=fixture();v.execute("local old=seed();local w=writeCalls;assert(not d.Begin(fresh(20,2),function()raw='A'..M.Encode(fresh(99,2));return true end));assert(writeCalls==w and raw=='A'..M.Encode(fresh(99,2)))")
 def test_actual_production_has_no_cell_inclusion_and_unchanged_permanent_Copy(self):
  import xml.etree.ElementTree as ET
  tree=ET.parse(ROOT/'Mod/SpecializationP0.modinfo');name='NetworkRecoveryCell.lua';self.assertEqual([n.text for n in tree.findall('./Files/File')].count(name),1)
  for p in ('CityProgressionStore.lua','Commerce.lua','CultureNetwork.lua','Gameplay.lua'):
   self.assertNotIn("include('NetworkRecoveryCell')",(ROOT/'Mod'/p).read_text())
  text=(ROOT/'Mod/CityIdentityRead.lua').read_text();self.assertIn('8192',text);self.assertIn('65536',text)

if __name__=='__main__':unittest.main()
