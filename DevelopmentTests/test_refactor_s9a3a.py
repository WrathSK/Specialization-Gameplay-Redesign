"""Pure Store training input stamp, not yet consumed by Training UI."""
import json,unittest
from refactor_harness import ROOT,measure
from test_refactor_s8b2 import fixture


def runtime():
 v=fixture();v.execute("s=shared.CityProgressionStore;aid=ca:GetID();ax=ca:GetX();ay=ca:GetY();bid=cb:GetID();bx=cb:GetX();by=cb:GetY();function sa()return s.TrainingInputStamp(0,aid,ax,ay)end;function sb()return s.TrainingInputStamp(0,bid,bx,by)end;assert(pcall(s.Base,0,ca)and pcall(s.Base,0,cb))");return v

class Inputs(unittest.TestCase):
 def test_pure_stamp_performs_zero_native_reads_facts_scans_or_writes(self):
  v=runtime();v.execute("local a,b=sa(),sb();local w=T.writes();local body=T.encode(T.record(ca));native=0;local function no()native=native+1;error('NATIVE_FORBIDDEN')end;Game.GetProperty=no;Game.SetProperty=no;for _,c in ipairs({ca,cb})do c.GetOwner=no;c.GetID=no;c.GetX=no;c.GetY=no;c.GetProperty=no end;Players[0].GetCities=no;shared.EffectiveFacts.Read=no;for i=1,1000 do assert(sa()==a and sb()==b)end;assert(native==0 and T.writes()==w)")
  measure('S9a3a_pure_Store_training_stamp',{'queries':2000,'native_reads':0,'fact_reads':0,'scans':0,'writes':0,'new_cached_city_rows':0,'UI_global_dependency_removed':False})
 def test_pending_only_changes_but_unrelated_history_revisions_do_not_change_stamp(self):
  v=runtime();v.execute("local a,b=sa(),sb();local n=M.Copy(T.record(ca));n.revision=n.revision+1;assert(saveCandidate(ca,n)and sa()==a and sb()==b);local base=n.base;n.investment={schema=1,anchor={owner=0,cityID=aid,token=base.token,first=M.Copy(base.first),specialization=base.specialization},revision=1,investments={},pending={stage='INTENT',receipt='TEST_PENDING',unitUID='TEST_UNIT',unitID=123,owner=0,cityUID=base.token,expectedRevision=1}};n.revision=n.revision+1;assert(saveCandidate(ca,n));local pending=sa();assert(pending~=a and pending:find('INVESTMENT_PENDING',1,true)and sb()==b);n=M.Copy(T.record(ca));n.investment.pending.stage='CONSUMED_CONFIRMED';n.revision=n.revision+1;assert(saveCandidate(ca,n)and sa()==pending);n=M.Copy(T.record(ca));n.investment.pending=nil;n.revision=n.revision+1;assert(saveCandidate(ca,n)and sa()==a and sb()==b)")
 def test_observed_binding_absence_and_recovery_reuse_the_original_single_read(self):
  v=runtime();v.execute("local a=sa();local get=ca.GetProperty;local reads=0;ca.GetProperty=function(c,k)if k==M.Keys.TOKEN then reads=reads+1;return nil end;return get(c,k)end;assert(not pcall(s.Base,0,ca)and reads==1);local lost=sa();assert(lost~=a and lost:find('ABSENT',1,true));for i=1,1000 do assert(sa()==lost)end;assert(reads==1);ca.GetProperty=get;assert(pcall(s.Base,0,ca)and sa()==a)")
 def test_binding_throw_preserves_exception_object_and_only_observes_unavailable(self):
  v=runtime();v.execute("local a=sa();local get=ca.GetProperty;local failure={message='NATIVE_TEMPORARY'};local n=0;ca.GetProperty=function(c,k)if k==M.Keys.TOKEN then n=n+1;error(failure)end;return get(c,k)end;local ok,err=pcall(s.Base,0,ca);assert(not ok and rawequal(err,failure)and n==1);assert(sa()~=a and sa():find('UNAVAILABLE',1,true)and n==1);ca.GetProperty=get;assert(pcall(s.Base,0,ca)and sa()==a)")
 def test_worker_failed_write_is_scoped_and_never_relabels_native_unknown_as_success(self):
  v=runtime();v.execute("local b=sb();local key=T.key(ca);local set=Game.SetProperty;Game.SetProperty=function(o,k,x)if k==key then error('NATIVE_WRITE_UNCERTAIN')end;return set(o,k,x)end;local n=M.Copy(T.record(ca));n.revision=n.revision+1;assert(not saveCandidate(ca,n));assert(sa()=='WORKER_UNAVAILABLE'and sb()==b and pcall(s.Base,0,cb))")
 def test_same_ID_new_reference_or_foreign_owner_is_not_old_stamp(self):
  v=runtime();v.execute("local a=sa();assert(s.TrainingInputStamp(1,aid,ax,ay)=='REFERENCE_MISMATCH');assert(s.TrainingInputStamp(0,aid,ax+100,ay)=='UNREGISTERED');assert(s.TrainingInputStamp(0,aid+100,ax,ay)=='REFERENCE_MISMATCH');assert(s.TrainingInputStamp(0,aid,0/0,ay)=='INVALID_REFERENCE'and s.TrainingInputStamp(0,aid,nil,ay)=='INVALID_REFERENCE'and sa()==a)")
 def test_loss_changes_lifecycle_and_preserves_original_permanent_history(self):
  v=runtime();v.execute("local a=sa();s.RegisterExit('Fixture',function()end);T.loss(ca,9,900);local lost=sa();assert(lost~=a and lost:find('HELD_TRANSFER',1,true));local before=T.encode(T.record(ca));local writes=T.writes();for i=1,1000 do assert(sa()==lost)end;assert(T.encode(T.record(ca))==before and T.writes()==writes)")
 def test_collection_fault_is_pure_global_availability_without_per_city_fanout(self):
  v=runtime();v.execute("T.propsSet('SPC_PROGRESSION_INDEX_V3',{schema=99});testReload();s=shared.CityProgressionStore;local before=T.writes();Game.GetProperty=function()error('NO_NATIVE')end;assert(sa()=='COLLECTION_FAILED'and sb()=='COLLECTION_FAILED'and T.writes()==before)")

 def test_same_city_write_barrier_does_not_invalidate_unrelated_city_stamp(self):
  v=runtime();v.execute("local other=sb();local original=sa();local key=T.key(ca);local set=Game.SetProperty;local sampled=false;Game.SetProperty=function(o,k,value)if k==key then sampled=true;assert(sa()=='WORKER_COMMITTING'and sb()==other)end;return set(o,k,value)end;local n=M.Copy(T.record(ca));n.revision=n.revision+1;assert(saveCandidate(ca,n)and sampled and sa()==original and sb()==other)")

 def test_post_restructuring_uses_current_epoch_pending_ledger(self):
  v=runtime();v.execute("a=shared.InvestmentAction;T.invest(ca,99801);local team={owner=0,id=777,uid='TEAM:777'};s.BeginRestructuring(0,ca,team,'STAMP_REST');T.turn(5);s.ConfigureRestructuring(0,ca,team,'CULTURE',{districtID=601,type='DISTRICT_THEATER',turn=T.now()});Players[0].GetUnits=function()return {FindID=function()return nil end}end;s.ConfirmRestructuringConsumption(0,ca,team);assert(s.FinishRestructuring(0,ca,team));local before=sa();local n=M.Copy(T.record(ca));local base=SPCRestructuringModel.Current(n);n.restructuring.investment={schema=1,anchor={owner=0,cityID=aid,token=base.token,first=M.Copy(base.first),specialization=base.specialization},revision=1,investments={},pending={stage='INTENT',receipt='REST_PENDING',unitUID='REST_UNIT',unitID=456,owner=0,cityUID=base.token,expectedRevision=1}};n.revision=n.revision+1;assert(saveCandidate(ca,n)and sa()~=before and sa():find('INVESTMENT_PENDING',1,true));n=M.Copy(T.record(ca));n.restructuring.investment.pending=nil;n.revision=n.revision+1;assert(saveCandidate(ca,n)and sa()==before)")


def load_tests(loader,standard,pattern):
 selection=json.loads((ROOT/'DevelopmentTests/refactor_selection.json').read_text())
 return unittest.TestSuite([standard,unittest.TestSuite(loader.loadTestsFromName(name)for name in selection['stages']['S9c6b'])])

if __name__=='__main__':unittest.main()
