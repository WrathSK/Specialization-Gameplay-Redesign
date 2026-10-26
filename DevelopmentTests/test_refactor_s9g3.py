"""Actual Store/Probe wrapper with explicit derived-slot adapter; no consumer wiring."""
from contextlib import contextmanager
from unittest.mock import patch
import unittest
from refactor_harness import ROOT,Context,legacy_source_observation,measure
from test_refactor_s8b2 import fixture as store_fixture
from test_refactor_s5b import probe

SETUP="""
counts={};P.Count=function(name)counts[name]=(counts[name]or 0)+1 end
P.FactReadService=shared.EffectiveFacts;ExposedMembers.SPC_RuntimeUIRevision=0
Model=SPCNetworkRecoveryModel;Adapter=SPCNetworkRecoveryStore
function open(city,family)return Adapter.Open(P,shared,0,city or ca,family or 'COMMERCE')end
cell,receiver=open();nativeKey=Adapter.Key('COMMERCE',T.record(ca).base.token)
function candidate(gold,sequence,kind)
 local v={version=1,family=kind or'COMMERCE',sequence=sequence or 1,receiver=receiver,sources={}}
 v.shape=v.family=='COMMERCE'and {gold=gold or 15,access=true}or {kind='RESEARCH',plot=5,count=1}
 return v
end
function allow()return true end
function installDerived(gold,sequence)
 local t=assert(cell.Begin(candidate(gold,sequence),allow));return assert(cell.Finish(t,allow))
end
function baseBytes()local v={};for k,r in pairs(T.props())do if k~=nativeKey and not k:find('SPC_DERIVED_NETWORK_RECOVERY_V1_',1,true)then v[k]=r end end;return T.encode(v)end
function meta()return Game:GetProperty(nativeKey)end
"""
def fixture():
 v=store_fixture()
 with legacy_source_observation():v.globals().include('NetworkRecoveryStore')
 v.execute('ca,cb=a,b')
 # The old strict native double only accepts permanent Store/index keys. Extend
 # this fixture to exactly the four new family/city keys;other writes still fail.
 v.execute('''
 local allowed={};for _,c in ipairs({ca,cb})do for _,family in ipairs({'COMMERCE','CULTURE'})do
  allowed[SPCNetworkRecoveryStore.Key(family,T.record(c).base.token)]=true
 end end
 local put,count=Game.SetProperty,T.writes;local derivedWrites=0
 Game.SetProperty=function(o,key,value)
  if not allowed[key]then return put(o,key,value)end
  assert(type(value)=='string','DERIVED_PROPERTY_DOUBLE_TYPE');derivedWrites=derivedWrites+1;T.propsSet(key,value)
 end
 T.writes=function()return count()+derivedWrites end
 ''')
 probe(v);v.execute(SETUP);return v

class ActualAdapter(unittest.TestCase):
 def test_actual_Store_reference_and_existing_Probe_setter_write_only_derived_slot(self):
  v=fixture();v.execute("local bytes=baseBytes();local writes=T.writes();local revision=shared.EffectiveFacts.Version();assert(installDerived());assert(T.writes()==writes+2 and counts.property_write==2 and ExposedMembers.SPC_RuntimeUIRevision==2 and shared.EffectiveFacts.Version()==revision+4 and baseBytes()==bytes and meta():sub(1,1)=='A');local r=cell.Read(candidate().shape);assert(r.state=='APPLIED'and r.value.receiver.stamp==receiver.stamp and r.value.receiver.reference==receiver.reference)")
  measure('S9g3_actual_Store_Probe_adapter',{'Property_writes':2,'existing_fact_barrier_version_delta':4,'existing_UI_epoch_delta':2,'permanent_records_changed':0,'setter_bypass':False,'automatic_consumers':0})
 def test_same_value_and_idle_calls_have_zero_added_writes_or_global_epochs(self):
  v=fixture();v.execute("installDerived();local w=T.writes();local p=counts.property_write;local epoch=ExposedMembers.SPC_RuntimeUIRevision;local fact=shared.EffectiveFacts.Version();local done=installDerived(15,2);assert(done.unchanged and done.sequence==1 and T.writes()==w and counts.property_write==p and ExposedMembers.SPC_RuntimeUIRevision==epoch and shared.EffectiveFacts.Version()==fact);for i=1,1000 do cell.Status()end;assert(T.writes()==w)")
 def test_exact_family_and_city_tokens_are_separate_without_key_supplied_by_caller(self):
  v=fixture();v.execute("installDerived();local other,ref=open(cb);local value=candidate();value.receiver=ref;local t=assert(other.Begin(value,allow));assert(other.Finish(t,allow));local c,ref=open(ca,'CULTURE');local value=candidate(1,1,'CULTURE');value.receiver=ref;t=assert(c.Begin(value,allow));assert(c.Finish(t,allow));local key1=nativeKey;local key2=Adapter.Key('COMMERCE',T.record(cb).base.token);local key3=Adapter.Key('CULTURE',T.record(ca).base.token);assert(key1~=key2 and key1~=key3 and Game:GetProperty(key1)and Game:GetProperty(key2)and Game:GetProperty(key3));assert(not pcall(Adapter.Key,'OTHER','token')and not pcall(Adapter.Key,'COMMERCE',string.rep('t',257)))")
 def test_fresh_module_and_store_context_rechecks_exact_slot_shape_and_lifecycle(self):
  v=fixture();v.execute("installDerived();local raw=meta();local before=T.writes();testReload();cell,receiver=open();local r=cell.Read(candidate().shape);assert(r.state=='APPLIED'and meta()==raw and T.writes()==before);assert(cell.Read({gold=14,access=true}).state=='SHAPE_MISMATCH')")
 def test_real_native_owner_change_without_store_notification_rejects_existing_cell(self):
  v=fixture();v.execute("local w=T.writes();ca.s.ref.owner=9;assert(not cell.Begin(candidate(),allow)and T.writes()==w and not meta())")
 def test_confirmed_loss_and_return_make_old_cell_and_old_saved_record_stale(self):
  v=fixture();v.execute("installDerived();local w=T.writes();local oldID=ca:GetID();shared.CityProgressionStore.RegisterExit('Fixture',function()end);T.loss(ca,9,900);assert(not cell.Begin(candidate(20,2),allow));ca.s.ref.owner=0;ca.s.ref.cityID=oldID;Events.CityTransfered.Fire(0,oldID,9);local new,ref=open();assert(new.Read(candidate().shape).state=='STALE_REFERENCE'and ref.stamp~=receiver.stamp);assert(T.writes()==w+2 and meta():sub(1,1)=='A')")
 def test_native_token_replacement_refuses_old_context_and_new_store_admission(self):
  v=fixture();v.execute("local w=T.writes();ca.s.values.TOKEN='FORGED';assert(not cell.Begin(candidate(),allow)and T.writes()==w);assert(not pcall(open,ca))")
 def test_new_or_unsupported_city_and_foreign_player_never_create_a_slot(self):
  v=fixture();v.execute("local fresh=T.fresh(9);local w=T.writes();assert(not pcall(open,fresh));assert(not pcall(Adapter.Open,P,shared,9,ca,'COMMERCE'));assert(not pcall(open,ca,'UNKNOWN'));assert(T.writes()==w);shared.CityProgressionStore.UsesNewAuthority=false;assert(not pcall(open,ca))")
 def test_parent_native_write_callback_cannot_open_or_use_derived_writer(self):
  v=fixture();v.execute("local key=T.key(ca);local put=Game.SetProperty;local hit=false;Game.SetProperty=function(o,k,value)if k==key then hit=true;assert(not pcall(open,ca)and not cell.Begin(candidate(),allow))end;return put(o,k,value)end;local n=M.Copy(T.record(ca));n.revision=n.revision+1;assert(saveCandidate(ca,n));assert(hit and not meta())")
 def test_metadata_setter_reentry_cannot_read_an_optimistic_candidate_or_repeat_write(self):
  v=fixture();v.execute("local put=Game.SetProperty;local callbacks=0;Game.SetProperty=function(o,k,value)if k==nativeKey then callbacks=callbacks+1;assert(cell.Read(candidate().shape).state=='BUSY'and not cell.Begin(candidate(),allow))end;return put(o,k,value)end;installDerived();assert(callbacks==2 and cell.Read(candidate().shape).state=='APPLIED')")
 def test_existing_write_barrier_breaks_shared_read_phase_reuse(self):
  v=fixture();v.execute("local f=shared.EffectiveFacts;f.WithPhase('DERIVED_PROPERTY_TEST',function()f.Read(0,ca);local before=f.Version();installDerived();assert(f.Version()==before+4);assert(f.Read(0,ca).specialization=='RESEARCH')end)")
 def test_pure_stamp_change_during_native_reference_get_rejects_observation(self):
  v=fixture();v.execute("local get=ca.GetProperty;local once=true;ca.GetProperty=function(c,key)local value=get(c,key);if once and key==M.Keys.TOKEN then once=false;local n=M.Copy(T.record(ca));n.revision=n.revision+1;n.referenceInvalidated=true;assert(saveCandidate(ca,n))end;return value end;local w=T.writes();assert(not cell.Begin(candidate(),allow)and T.writes()==w+1 and not meta())")
 def test_transient_native_metadata_read_failure_has_no_parent_fault_or_property_write(self):
  v=fixture();v.execute("local get=Game.GetProperty;local w=T.writes();Game.GetProperty=function(o,k)if k==nativeKey then error('TRANSIENT_DERIVED_READ')end;return get(o,k)end;assert(cell.Read(candidate().shape).state=='UNAVAILABLE'and not cell.Begin(candidate(),allow)and T.writes()==w and pcall(shared.CityProgressionStore.Base,0,ca));Game.GetProperty=get;assert(installDerived())")
 def test_unknown_native_record_type_is_not_traversed_or_used_as_authority(self):
  v=fixture();v.execute("local get=Game.GetProperty;Game.GetProperty=function(o,k)if k==nativeKey then return setmetatable({},{__index=function()error('NATIVE_OBJECT_MUST_NOT_BE_READ')end})end;return get(o,k)end;local w=T.writes();assert(cell.Read(candidate().shape).state=='UNAVAILABLE'and not cell.Begin(candidate(),allow)and T.writes()==w)")
 def test_reference_getter_and_collection_work_budget_are_explicit_and_no_idle_work(self):
  v=fixture();v.execute("local at=CityManager.GetCityAt;local prop=ca.GetProperty;work={locations=0,tokens=0,slotReads=0};CityManager.GetCityAt=function(...)work.locations=work.locations+1;return at(...)end;ca.GetProperty=function(c,k)if k==M.Keys.TOKEN then work.tokens=work.tokens+1 end;return prop(c,k)end;local get=Game.GetProperty;Game.GetProperty=function(o,k)if k==nativeKey then work.slotReads=work.slotReads+1 end;return get(o,k)end;installDerived();local loc,tok,reads=work.locations,work.tokens,work.slotReads;for i=1,1000 do cell.Status()end;assert(work.locations==loc and work.tokens==tok and work.slotReads==reads);changedLocations=loc;changedTokens=tok;changedReads=reads")
  measure('S9g3_explicit_adapter_budget',{'changed_commit_city_lookups':v.eval('changedLocations'),'changed_commit_raw_binding_reads':v.eval('changedTokens'),'changed_commit_slot_reads':v.eval('changedReads'),'idle_extra_getters':0,'city_collection_scans':0,'existing_UI_barrier_kept':True,'native_CPU_heap_claim':False})

class NativeFaults(unittest.TestCase):
 def test_both_phases_drop_throw_and_stale_readback_preserve_parent_and_never_replay(self):
  for phase in ('BEGIN','FINISH'):
   for mode in ('DROP','THROW_BEFORE','THROW_AFTER','STALE_READBACK'):
    v=fixture();v.execute("""
    phase,mode=...;local old=baseBytes();local put,get=Game.SetProperty,Game.GetProperty
    local ticket;if phase=='FINISH'then ticket=assert(cell.Begin(candidate(),allow))end
    local before=Game:GetProperty(nativeKey);local written=false;attempts=0
    Game.SetProperty=function(o,k,value)
     if k~=nativeKey then return put(o,k,value)end;attempts=attempts+1
     if mode=='DROP'then return end;if mode=='THROW_BEFORE'then error('BEFORE_UNKNOWN')end
     put(o,k,value);written=true;if mode=='THROW_AFTER'then error('AFTER_UNKNOWN')end
    end
    Game.GetProperty=function(o,k)if k==nativeKey and written and mode=='STALE_READBACK'then return before end;return get(o,k)end
    if phase=='BEGIN'then assert(not cell.Begin(candidate(),allow))else assert(not cell.Finish(ticket,allow))end
    assert(attempts==1 and not cell.Status().active and baseBytes()==old and pcall(shared.CityProgressionStore.Base,0,ca))
    local n=attempts;for i=1,1000 do cell.Status()end;assert(attempts==n)
    """,phase,mode)
 def test_native_slot_changes_after_input_gate_are_not_overwritten(self):
  v=fixture();v.execute("local forged='unexpected-owner-value';local w=T.writes();assert(not cell.Begin(candidate(),function()T.propsSet(nativeKey,forged);return true end));assert(meta()==forged and T.writes()==w)")
 def test_unreviewed_new_writer_still_blocks_real_static_gate_until_explicit_review(self):
  import json,copy
  from refactor_static import check
  selection=json.loads((ROOT/'DevelopmentTests/refactor_selection.json').read_text());key='Mod/NetworkRecoveryStore.lua|PROPERTY_PRODUCER_OWNERSHIP'
  unreviewed=copy.deepcopy(selection);unreviewed['static_alarm_baseline'].pop(key)
  result=check(unreviewed);self.assertEqual(result['widened'][key],{'before':0,'after':1});self.assertEqual(result['status'],'FAIL_NEW_OR_WIDENED_ALARM')
  self.assertEqual(check(selection)['widened'],{})
 def test_production_import_only_and_no_generic_setter_bypass(self):
  text=(ROOT/'Mod/NetworkRecoveryStore.lua').read_text();self.assertIn('P.SetProperty(Game,key,value)',text);self.assertNotIn('Game:SetProperty',text)
  for p in ('CityProgressionStore.lua','Commerce.lua','CultureNetwork.lua','Gameplay.lua'):
   self.assertNotIn("include('NetworkRecoveryStore')",(ROOT/'Mod'/p).read_text())

if __name__=='__main__':unittest.main()
