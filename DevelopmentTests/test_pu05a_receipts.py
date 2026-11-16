"""PU05a true Store/Crew receipt isolation; native attribution remains a separate OPEN gate."""
from contextlib import contextmanager
from pathlib import Path
import os,subprocess,unittest
from unittest.mock import patch
from refactor_harness import ROOT,Context,measure
BASE='4931f2b0a97aef1a663ea7c998b10e245a0bfd3a'
@contextmanager
def source_profile():
 if os.environ.get('SPC_PU05A_BASELINE')!=BASE:yield;return
 old={ROOT/'Mod'/(n+'.lua'):subprocess.check_output(['git','show',BASE+':Mod/'+n+'.lua'],cwd=ROOT).decode()for n in ('CrewProjects','CrewModel')};read=Path.read_text
 with patch.object(Path,'read_text',lambda p,*a,**k:old[p]if p in old else read(p,*a,**k)):yield

def pair():
 from test_refactor_s7d6_proof import fixture
 with source_profile():l=fixture()
 l.execute("function Akey()local a=shared.CityProgressionStore.HistoricalReference(c);return SPCCrewModel.ReceiptKey(a.token,1)end;function Bkey()local a=shared.CityProgressionStore.HistoricalReference(other);return SPCCrewModel.ReceiptKey(a.token,1)end")
 return l

class CrossCity(unittest.TestCase):
 def test_unresolved_call_does_not_block_independently_proven_next_city(self):
  l=pair();l.execute("C.grantFailure='before';C.complete(c,p);assert(C.calls==1);C.grantFailure=nil;C.complete(other,p);assert(C.calls==2,'OTHER_CITY_BLOCKED_BY_SHARED_RECEIPT');assert(C.count(other)==1);local v=C.props[SPCCrewModel.RECEIPT_PROPERTY];assert(v.version==2 and v.water[p]==2 and v.pending[Akey()] and not v.pending[Bkey()]);assert(C.reserve(c).error)")
 def test_unresolved_source_survives_reload_without_blocking_other_source(self):
  l=pair();l.execute("C.grantFailure='before';C.complete(c,p);C.grantFailure=nil;C.reload(c);C.complete(other,p);assert(C.calls==2,'RELOADED_SOURCE_BLOCKED_OTHER_CITY');assert(C.count(other)==1);local r=C.props[SPCCrewModel.RECEIPT_PROPERTY];assert(r.pending[Akey()] and not r.pending[Bkey()]);for i=1,10 do Events.CityProjectCompleted.Fire(0,c:GetID(),C.rows.Projects[p].Index);Events.CityProjectCompleted.Fire(0,other:GetID(),C.rows.Projects[p].Index)end;assert(C.calls==2)")
 def test_normal_completed_pending_rows_are_removed_and_water_remains(self):
  l=pair();l.execute("C.complete(c,p);C.complete(other,p);local r=C.props[SPCCrewModel.RECEIPT_PROPERTY];assert(r.water[p]==2 and next(r.pending)==nil and C.calls==2);C.reload(c);Events.CityProjectCompleted.Fire(0,c:GetID(),C.rows.Projects[p].Index);assert(C.calls==2)")
 def test_unbound_native_unit_still_blocks_unsafe_inventory_without_inventing_source(self):
  for fault in ("C.grantFailure='nil'","C.bindingFailure='drop'"):
   with self.subTest(fault=fault):
    l=pair();l.execute(fault+";C.complete(c,p);C.grantFailure=nil;C.bindingFailure=nil;C.complete(other,p);assert(C.calls==1 and crew.errors['0:'..other:GetID()]=='CREW_SOURCE_UNAVAILABLE');local r=C.props[SPCCrewModel.RECEIPT_PROPERTY];assert(r.water[p]==1 and r.pending[Akey()] and not r.pending[Bkey()]);for i=1,5 do Events.CityProjectCompleted.Fire(0,c:GetID(),C.rows.Projects[p].Index)end;assert(C.calls==1)")
 def test_same_source_unresolved_order_keeps_own_reservation(self):
  l=pair();l.execute("C.grantFailure='before';C.complete(c,p);C.grantFailure=nil;assert(C.reserve(c).error);assert(#c:GetProperty(SPCCrewModel.ORDER_PROPERTY).orders==1);local r=C.props[SPCCrewModel.RECEIPT_PROPERTY];assert(r.pending[Akey()].stage=='CALLING' and C.calls==1)")
 def test_native_reentry_cannot_repeat_its_own_grant(self):
  l=pair();l.execute("local create=UnitManager.InitUnit;UnitManager.InitUnit=function(...)Events.CityProjectCompleted.Fire(0,c:GetID(),C.rows.Projects[p].Index);return create(...)end;C.complete(c,p);assert(C.calls==1 and C.count(c)==1 and next(C.props[SPCCrewModel.RECEIPT_PROPERTY].pending)==nil)")
 def test_receipt_and_high_water_precede_native_call(self):
  l=pair();l.execute("local create=UnitManager.InitUnit;UnitManager.InitUnit=function(...)local r=C.props[SPCCrewModel.RECEIPT_PROPERTY];assert(r.water[p]==1 and r.pending[Akey()] and c:GetProperty(SPCCrewModel.ORDER_PROPERTY).orders[1].stage=='CALLING');return create(...)end;C.complete(c,p);assert(C.calls==1)")
 def test_wrong_source_after_creation_never_replays_or_clears_other_scope(self):
  l=pair();l.execute("local create=UnitManager.InitUnit;local ref=shared.CityProgressionStore.HistoricalReference;UnitManager.InitUnit=function(...)local u=create(...);shared.CityProgressionStore.HistoricalReference=function(city)local r=ref(city);if city==c then r.token='DIFFERENT'end;return r end;return u end;C.complete(c,p);local r=C.props[SPCCrewModel.RECEIPT_PROPERTY];assert(r.pending[Akey()]==nil or crew.errors['0:'..c:GetID()]);assert(C.calls==1);shared.CityProgressionStore.HistoricalReference=ref;for i=1,3 do Events.CityProjectCompleted.Fire(0,c:GetID(),C.rows.Projects[p].Index)end;assert(C.calls==1)")
 def test_old_flat_receipts_are_rejected_without_silent_reset(self):
  l=pair();l.execute("C.props[SPCCrewModel.RECEIPT_PROPERTY]={[p]={count=1,source='OLD',stage='BOUND',unitID=900}};C.complete(c,p);assert(C.calls==0 and crew.errors['0:'..c:GetID()]);assert(C.props[SPCCrewModel.RECEIPT_PROPERTY][p].source=='OLD')")

class Envelope(unittest.TestCase):
 def make(self):
  with source_profile():c=Context('PU05a pure receipts');c.load('CrewModel')
  c.execute("M=SPCCrewModel;p=M.Project(1,150);function row(n)return {owner=0,cityID=n,x=n,y=0,source='SOURCE_'..n,serial=1,project=p,count=n,stage='CALLING'}end;function envelope(n)local v={version=2,water={[p]=n},pending={}};for i=1,n do local r=row(i);v.pending[M.ReceiptKey(r.source,1)]=r end;return v end")
  return c
 def test_capacity_k_minus_one_k_and_k_plus_one(self):
  c=self.make();c.execute("assert(M.ReceiptState(nil,0).version==2);assert(M.ReceiptState(envelope(2047),0));local v=envelope(2048);assert(M.ReceiptState(v,0));local r=row(2049);v.pending[M.ReceiptKey(r.source,1)]=r;v.water[p]=2049;assert(not pcall(M.ReceiptState,v,0))")
  measure('PU05a_pending_capacity',{'bound':2048,'tested':[2047,2048,2049],'normal_completed_rows_retained':0})
 def test_owner_source_key_and_consumed_count_must_match(self):
  for fault in ("v.pending[k].owner=1","v.pending[k].source='WRONG'","v.pending[k].serial=2","v.pending[k].count=3","v.pending[k].stage='BOUND'","v.pending[k].cityID=-1"):
   with self.subTest(fault=fault):
    c=self.make();c.execute("local v=envelope(1);local k=next(v.pending);"+fault+";assert(not pcall(M.ReceiptState,v,0))")
 def test_duplicate_project_count_and_native_metatable_are_rejected(self):
  c=self.make();c.execute("local v=envelope(2);local k=M.ReceiptKey('SOURCE_2',1);v.pending[k].count=1;assert(not pcall(M.ReceiptState,v,0));assert(not pcall(M.ReceiptState,setmetatable({},{__index=function()error('NATIVE_READ')end}),0))")
 def test_cloned_result_does_not_mutate_saved_input(self):
  c=self.make();c.execute("local v=envelope(1);local n=M.ReceiptState(v,0);n.water[p]=8;n.pending[next(n.pending)]=nil;assert(v.water[p]==1 and next(v.pending))")

class RecoveryAndScope(unittest.TestCase):
 def test_different_city_reentry_during_native_call_preserves_both_receipts(self):
  l=pair();l.execute("local create=UnitManager.InitUnit;local once=true;UnitManager.InitUnit=function(...)if once then once=false;C.complete(other,p)end;return create(...)end;C.complete(c,p);local r=C.props[SPCCrewModel.RECEIPT_PROPERTY];assert(C.calls==2 and C.count(c)==1 and C.count(other)==1 and r.water[p]==2 and not next(r.pending));assert(not crew.errors['0:'..c:GetID()] and not crew.errors['0:'..other:GetID()])")
 def test_known_binding_but_failed_final_cleanup_is_source_scoped(self):
  l=pair();l.execute("local set=P.SetProperty;P.SetProperty=function(o,k,v)if k==SPCCrewModel.RECEIPT_PROPERTY and next(v.pending)==nil then return end;return set(o,k,v)end;C.complete(c,p);assert(C.calls==1 and C.count(c)==1 and C.props[SPCCrewModel.RECEIPT_PROPERTY].pending[Akey()]);P.SetProperty=set;C.complete(other,p);local r=C.props[SPCCrewModel.RECEIPT_PROPERTY];assert(C.calls==2 and C.count(other)==1 and r.pending[Akey()] and not r.pending[Bkey()] and r.water[p]==2)")
 def test_receipt_capacity_failure_precedes_new_order_write_and_native_call(self):
  l=pair();l.execute("local M=SPCCrewModel;local r={version=2,water={[p]=2048},pending={}};for i=1,2048 do local s='OLD_'..i;r.pending[M.ReceiptKey(s,1)]={owner=0,source=s,cityID=i,x=i,y=0,serial=1,project=p,count=i,stage='CALLING'}end;C.props[M.RECEIPT_PROPERTY]=r;C.stats[p]=2049;c:GetBuildQueue().items[p]=nil;local before=T.encode(c:GetProperty(M.ORDER_PROPERTY));Events.CityProjectCompleted.Fire(0,c:GetID(),C.rows.Projects[p].Index);assert(C.calls==0 and crew.errors['0:'..c:GetID()]=='CREW_RECEIPT_LIMIT');assert(T.encode(c:GetProperty(M.ORDER_PROPERTY))==before and C.props[M.RECEIPT_PROPERTY].water[p]==2048)")
 def test_default_provider_remains_fresh_and_restricted_lua_works(self):
  l=pair();l.execute("io=nil;os=nil;debug=nil;package=nil;require=nil;collectgarbage=nil;local read=ExposedMembers.SPC_CrewNativeRead;local n=0;ExposedMembers.SPC_CrewNativeRead=function(...)n=n+1;return read(...)end;C.complete(c,p);assert(C.calls==1 and n>0 and C.count(c)==1)")
 def test_normal_completion_retains_five_durable_property_writes(self):
  l=pair();l.execute("local set=P.SetProperty;grantWrites=0;P.SetProperty=function(o,k,v)if k==SPCCrewModel.ORDER_PROPERTY or k==SPCCrewModel.RECEIPT_PROPERTY or k==SPCCrewModel.UNIT_PROPERTY then grantWrites=grantWrites+1 end;return set(o,k,v)end;C.complete(c,p);assert(C.calls==1 and grantWrites==5)")
  measure('PU05a_normal_grant',{'native_creations':1,'durable_grant_property_writes':5,'completed_pending_rows':0,'new_polling':False})

class Provider(unittest.TestCase):
 def test_explicit_snapshot_provider_changes_only_the_reader(self):
  from test_refactor_s7d5 import profile
  from test_b236_crews import crew_runtime
  with profile():l=crew_runtime()
  l.execute("local start=SPCCrewProjects.Start;reads=0;SPCCrewProjects.Start=function(P,S)return start(P,S,function(pid,id)reads=reads+1;return ExposedMembers.SPC_CrewNativeRead(pid,id)end)end;c=C.make();p=C.begin(c);C.complete(c,p);assert(reads>0 and C.calls==1 and C.count(c)==1)")
 def test_injected_malformed_snapshot_still_fails_before_any_grant(self):
  from test_refactor_s7d5 import profile
  from test_b236_crews import crew_runtime
  with profile():l=crew_runtime()
  l.execute("local start=SPCCrewProjects.Start;SPCCrewProjects.Start=function(P,S)return start(P,S,function(pid,id)local v=ExposedMembers.SPC_CrewNativeRead(pid,id);v.owner=1;return v end)end;c=C.make();local r=C.reserve(c);assert(r.error and C.calls==0)")


class _Lua51EmptyStatementCase:
 def __init__(self,case):self.case=case
 def subTest(self,**kw):return self.case.subTest(**kw)
 def check(self,source):
  from test_b236_crews import crew_runtime
  # Only Lua55's empty-statement tolerance differs. Keep both original guards.
  source=source.replace('SPCCrewModel.Project(1,150);;C.complete','SPCCrewModel.Project(1,150);do end;C.complete')
  crew_runtime().execute(source)

class Compatibility(unittest.TestCase):
 def test_original_missing_admission_and_counter_jump_guards_under_lua51(self):
  from test_b236_crews import Formation
  from test_refactor_s7d5 import profile
  with profile():Formation.test_missing_admission_or_counter_jump_never_guesses_unit(_Lua51EmptyStatementCase(self))
 def test_false_explicit_provider_does_not_silently_choose_default(self):
  l=pair();l.execute("local old=shared.CrewProjects;assert(not pcall(SPCCrewProjects.Start,P,shared,false));assert(shared.CrewProjects==old)")

if __name__=='__main__':unittest.main()
