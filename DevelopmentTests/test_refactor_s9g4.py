"""Per-domain D2 proof and explicit pure lifecycle scope before consumers."""
from contextlib import contextmanager
from pathlib import Path
from unittest.mock import patch
from hashlib import sha256
import subprocess,unittest
from refactor_harness import ROOT,TrackedLua51,SOURCES,measure
from test_refactor_s9g2 import fixture as cell
from test_refactor_s8b2 import fixture as store

@contextmanager
def before():
 p=ROOT/'Mod/CityProgressionStore.lua';text=subprocess.check_output(['git','show','c52eb43:Mod/CityProgressionStore.lua'],cwd=ROOT,text=True)
 read,execute=Path.read_text,TrackedLua51.execute;h=sha256(text.encode()).hexdigest()
 def run(vm,s,*a,**kw):
  if sha256(s.encode()if isinstance(s,str)else s).hexdigest()==h:SOURCES[h]='historical/c52eb43/Mod/CityProgressionStore.lua'
  return execute(vm,s,*a,**kw)
 with patch.object(Path,'read_text',lambda f,*a,**kw:text if f==p else read(f,*a,**kw)),patch.object(TrackedLua51,'execute',run):yield

class DomainProof(unittest.TestCase):
 def test_one_source_can_keep_retained_domain_and_update_fresh_sibling(self):
  v=cell();v.execute("seed();local a=fresh(20,2);a.sources[1].status='RETAINED';a.sources[1].domains.DISTRICT_CAMPUS.status='RETAINED';a.sources[1].domains.DISTRICT_THEATER={status='CONFIRMED',eligible=true,X=55};a.sources[1].domains.DISTRICT_HOLY_SITE.status='CONFIRMED';local t=assert(d.Begin(a,verified));assert(d.Finish(t,verified));local out=d.Read(a.shape).value;assert(out.sources[1].domains.DISTRICT_CAMPUS.X==30.125 and out.sources[1].domains.DISTRICT_CAMPUS.status=='RETAINED'and out.sources[1].domains.DISTRICT_THEATER.X==55 and out.sources[1].domains.DISTRICT_THEATER.status=='CONFIRMED')")
  measure('S9g4_same_source_domain_provenance',{'retained_domain':'unchanged prior APPLIED fact','fresh_sibling':'updated independently','source_old_fact_relabelled_fresh':False,'new_native_or_automatic_calls':0})
 def test_unknown_domain_has_no_fact_while_known_sibling_remains_separate(self):
  v=cell();v.execute("local a=fresh();a.sources[1].status='RETAINED';a.sources[1].domains.DISTRICT_CAMPUS={status='UNKNOWN'};a.sources[1].domains.DISTRICT_HOLY_SITE.status='CONFIRMED';local out=M.Decode(M.Encode(a));assert(out.sources[1].domains.DISTRICT_CAMPUS.status=='UNKNOWN'and out.sources[1].domains.DISTRICT_CAMPUS.X==nil and out.sources[1].domains.DISTRICT_HOLY_SITE.eligible==false);local t=assert(d.Begin(a,verified));assert(d.Finish(t,verified))")
 def test_source_all_fresh_label_cannot_hide_retained_or_unknown_domain(self):
  for status in ('RETAINED','UNKNOWN'):
   v=cell();v.execute("local a=fresh();local row=a.sources[1].domains.DISTRICT_CAMPUS;row.status=...;if row.status=='UNKNOWN'then row.eligible=nil;row.X=nil end;assert(not pcall(M.Encode,a))",status)
 def test_unknown_or_changed_previous_domain_never_supplies_retained_value(self):
  for mode in ('VALUE','MISSING','UNKNOWN','REFERENCE','STAMP'):
   v=cell();v.execute("mode=...;seed();local a=fresh(20,2);a.sources[1].status='RETAINED';a.sources[1].domains.DISTRICT_CAMPUS.status='RETAINED';if mode=='VALUE'then a.sources[1].domains.DISTRICT_CAMPUS.X=99 elseif mode=='MISSING'then a.sources[1].domains.DISTRICT_THEATER={status='RETAINED',eligible=true,X=55}elseif mode=='UNKNOWN'then local old=M.Decode(raw:sub(2));old.sources[1].status='RETAINED';old.sources[1].domains.DISTRICT_CAMPUS={status='UNKNOWN'};old.sources[1].domains.DISTRICT_HOLY_SITE.status='CONFIRMED';raw='A'..M.Encode(old)elseif mode=='REFERENCE'then a.sources[1].reference='OTHER'else a.sources[1].stamp='OTHER'end;local w=writeCalls;assert(not d.Begin(a,verified)and writeCalls==w)",mode)
 def test_unknown_domain_fields_and_empty_false_retained_source_are_rejected(self):
  v=cell();v.execute("local a=fresh();a.sources[1].status='RETAINED';a.sources[1].domains={DISTRICT_CAMPUS={status='UNKNOWN',eligible=false}};assert(not pcall(M.Encode,a));a.sources[1].domains.DISTRICT_CAMPUS.eligible=nil;assert(not pcall(M.Encode,a));a.sources[1].domains={};assert(not pcall(M.Encode,a))")
 def test_culture_retained_set_stays_whole_and_cannot_smuggle_new_civilization(self):
  v=cell();v.execute("local c=SPCNetworkRecoveryCell.New('CULTURE',get,put,now);local a=culture();a.sequence=1;a.sources[2].status='CONFIRMED';local t=assert(c.Begin(a,verified));assert(c.Finish(t,verified));a.sequence=2;a.sources[1].status='RETAINED';a.sources[1].civilizations.CIVILIZATION_EGYPT=true;local w=writeCalls;assert(not c.Begin(a,verified)and writeCalls==w)")

SCOPE_SETUP="""
ca,cb=a,b;a=shared.InvestmentAction
function stamp(c)return shared.CityProgressionStore.NetworkRecoveryStamp(c:GetOwner(),c:GetID(),c:GetX(),c:GetY(),T.record(c).base.token)end
function oldstamp(c)return shared.CityProgressionStore.CarrierReferenceStamp(c:GetOwner(),c:GetID(),c:GetX(),c:GetY(),T.record(c).base.token)end
"""
class LifecycleScope(unittest.TestCase):
 def test_old_carrier_stamp_output_unchanged_on_actual_store_through_ordinary_investments(self):
  outputs=[]
  for old in (True,False):
   from contextlib import nullcontext
   with before()if old else nullcontext():v=store()
   v.execute(SCOPE_SETUP+"values={oldstamp(ca)};for i=1,3 do T.invest(ca,77000+i);values[#values+1]=oldstamp(ca)end;result=T.encode(values)")
   outputs.append(v.eval('result'))
  self.assertEqual(outputs[0],outputs[1])
 def test_actual_potential_and_history_revision_changes_keep_same_narrow_scope(self):
  v=store();v.execute(SCOPE_SETUP+"local start=stamp(ca);assert(type(start)=='string');for i=1,3 do T.invest(ca,78000+i);assert(stamp(ca)==start)end;local n=M.Copy(T.record(ca));n.revision=n.revision+1;assert(saveCandidate(ca,n)and stamp(ca)==start)")
  measure('S9g4_actual_store_scope',{'actual_Potential_upgrade':'stable','ordinary_history_revision':'stable','lifecycle_and_identity_fences':'retained','old_carrier_stamp_output':'unchanged'})
 def test_pure_scope_has_no_getter_scan_or_write_in_thousand_calls(self):
  v=store();v.execute(SCOPE_SETUP+"local r=T.record(ca);local expected=stamp(ca);local w=T.writes();local get=ca.GetProperty;ca.GetProperty=function()error('NATIVE_GETTER_FORBIDDEN')end;local at=CityManager.GetCityAt;CityManager.GetCityAt=function()error('NATIVE_LOOKUP_FORBIDDEN')end;for i=1,1000 do assert(shared.CityProgressionStore.NetworkRecoveryStamp(0,ca:GetID(),ca:GetX(),ca:GetY(),r.base.token)==expected)end;assert(T.writes()==w);ca.GetProperty=get;CityManager.GetCityAt=at")
 def test_confirmed_loss_return_and_wrong_reference_token_invalidate_old_scope(self):
  v=store();v.execute(SCOPE_SETUP+"local old=stamp(ca);local token=T.record(ca).base.token;local id=ca:GetID();local s=shared.CityProgressionStore;s.RegisterExit('Fixture',function()end);assert(not s.NetworkRecoveryStamp(0,id,ca:GetX(),ca:GetY(),'OTHER'));T.loss(ca,9,900);assert(not s.NetworkRecoveryStamp(0,id,ca:GetX(),ca:GetY(),token));ca.s.ref.owner=0;ca.s.ref.cityID=id;Events.CityTransfered.Fire(0,id,9);assert(stamp(ca)and stamp(ca)~=old)")
 def test_begin_real_restructuring_invalidates_even_before_native_reference_changes(self):
  v=store();v.execute(SCOPE_SETUP+"T.invest(ca,79001);local old=stamp(ca);local native=ca:GetProperty(M.Keys.TOKEN);local team={owner=0,id=777,uid='TEAM:777'};shared.CityProgressionStore.BeginRestructuring(0,ca,team,'NREC_SCOPE');assert(stamp(ca)and stamp(ca)~=old and ca:GetProperty(M.Keys.TOKEN)==native)")
 def test_new_scope_is_unavailable_during_actual_permanent_commit(self):
  v=store();v.execute(SCOPE_SETUP+"local r=T.record(ca);local put=Game.SetProperty;local seen=false;Game.SetProperty=function(o,key,value)if key==T.key(ca)then seen=true;assert(not shared.CityProgressionStore.NetworkRecoveryStamp(0,ca:GetID(),ca:GetX(),ca:GetY(),r.base.token))end;return put(o,key,value)end;local n=M.Copy(r);n.revision=n.revision+1;assert(saveCandidate(ca,n)and seen and stamp(ca))")

if __name__=='__main__':unittest.main()
