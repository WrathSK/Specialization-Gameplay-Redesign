"""Research Tradition publishes actual post-readback values; UI wiring remains separate."""
from contextlib import contextmanager,nullcontext
from hashlib import sha256
from pathlib import Path
from unittest.mock import patch
import json,subprocess,unittest
from refactor_harness import ROOT,TrackedLua51,SOURCES,legacy_source_observation,measure
from test_refactor_s5d4c7 import fixture

BASE='647ab1e'
@contextmanager
def before():
 p=ROOT/'Mod/ResearchTraditionEffects.lua';old=subprocess.check_output(['git','show',BASE+':Mod/ResearchTraditionEffects.lua'],cwd=ROOT,text=True);read,execute=Path.read_text,TrackedLua51.execute;h=sha256(old.encode()).hexdigest()
 def source(f,*a,**kw):return old if f==p else read(f,*a,**kw)
 def run(vm,s,*a,**kw):
  if sha256(s.encode()if isinstance(s,str)else s).hexdigest()==h:SOURCES[h]='historical/'+BASE+'/Mod/ResearchTraditionEffects.lua'
  return execute(vm,s,*a,**kw)
 with patch.object(Path,'read_text',source),patch.object(TrackedLua51,'execute',run),legacy_source_observation():yield

def runtime(cold=False):
 v=fixture(cold);v.execute("function facts(city)return shared.EffectiveFacts.Read(0,city or c)end;function applied(city)return effects.Applied(facts(city))end;function nextTier()for i=1,9 do T.turn(1);pp()end;T.turn(1)end");return v

class Publication(unittest.TestCase):
 def test_actual_applied_levels_zero_and_same_update_are_distinct_from_history(self):
  v=runtime();v.execute("assert(applied().applied==5 and applied().requiredActive==4);for i=1,40 do T.turn(1);pp()end;assert(applied().applied==25 and current(c)==25);local h=history();local w=T.writes();T.governor(1);effects.Update(0,c);local a=applied();assert(a.appliedStatus=='KNOWN'and a.applied==0 and a.lastConfirmed==0 and a.gate=='INELIGIBLE'and a.reason=='ACTIVE_BELOW_IV');effects.Update(0,c);assert(applied().applied==0 and history()==h and T.writes()==w)")
 def test_pure_projection_is_detached_and_thousand_reads_add_no_native_scan_or_write(self):
  v=runtime();v.execute("f=facts();local h=history();local w=T.writes();local reads,changes=fxReads,fxWrites;local function no()error('PUBLISHER_NATIVE_FORBIDDEN')end;for _,city in ipairs({c,other})do for _,name in ipairs({'GetOwner','GetID','GetX','GetY','GetProperty','GetBuildings','GetBuildQueue'})do city[name]=no end end;Players[0].GetCities=no;Game.GetCurrentGameTurn=no;P.Info=no;shared.EffectiveFacts.Read=no;shared.CityProgressionStore.ReadTradition=no;for i=1,1000 do local a=effects.Applied(f);assert(a.appliedStatus=='KNOWN'and a.applied==5);a.applied=999 end;assert(fxReads==reads and fxWrites==changes and T.writes()==w)")
  measure('S9d1_Tradition_pure_publication',{'queries':1000,'native_reads':0,'fact_or_carrier_samples':0,'scans':0,'saved_writes':0,'UI_wired':False,'publisher_slots':2048})
 def test_unknown_governor_retains_last_confirmed_without_fake_zero_and_waits_real_cause(self):
  v=runtime();v.execute("T.governor(nil);effects.Update(0,c);local a=applied();assert(a.appliedStatus=='UNKNOWN'and a.applied==nil and a.lastConfirmed==5 and a.gate=='UNKNOWN'and a.reason=='ACTIVE_UNAVAILABLE'and current(c)==5);local r,w=fxReads,fxWrites;for i=1,1000 do pp()end;assert(fxReads==r and fxWrites==w);T.governor(4);effects.Update(0,c);assert(applied().applied==5)")
 def test_cold_unknown_does_not_infer_existing_carrier_or_zero(self):
  v=runtime(True);v.execute("local a=applied();assert(a.appliedStatus=='UNKNOWN'and a.applied==nil and a.lastConfirmed==nil and current(c)==5)")
 def test_base_fact_exception_invalidates_scoped_old_publication_without_resampling(self):
  v=runtime();v.execute("f=facts();local read=shared.EffectiveFacts.Read;shared.EffectiveFacts.Read=function()error('BASE_FAILED')end;local r=fxReads;effects.Update(0,c);assert(effects.Applied(f).appliedStatus=='UNKNOWN'and effects.Applied(f).lastConfirmed==5 and fxReads==r);shared.EffectiveFacts.Read=read;effects.Update(0,c);assert(applied().applied==5)")
 def test_input_failures_keep_specific_reasons_and_original_carriers(self):
  for mode,reason in (('HISTORY','HISTORY_UNAVAILABLE'),('CURSOR','INTERVAL_NOT_CURRENT'),('SPEED','SPEED_UNAVAILABLE')):
   v=runtime();v.execute("mode,expected=...;local read=shared.CityProgressionStore.ReadTradition;if mode=='HISTORY'then shared.CityProgressionStore.ReadTradition=function()error('ISOLATED_HISTORY')end elseif mode=='CURSOR'then shared.CityProgressionStore.ReadTradition=function(...)local t=read(...);t.cursor=t.cursor-1;return t end else GameInfo.GameSpeeds.STANDARD=nil end;effects.Update(0,c);local a=applied();assert(a.appliedStatus=='UNKNOWN'and a.applied==nil and a.lastConfirmed==5 and a.reason==expected and current(c)==5)",mode,reason)
 def test_partial_remove_then_failed_create_never_publishes_candidate(self):
  v=runtime();v.execute("nextTier();failCreate=true;pp();local a=applied();assert(current(c)==0 and a.appliedStatus=='UNKNOWN'and a.applied==nil and a.lastConfirmed==5 and a.reason=='APPLICATION_UNCONFIRMED');failCreate=false;local r,w=fxReads,fxWrites;for i=1,1000 do pp()end;assert(fxReads==r and fxWrites==w);GameEvents.BuildingPillageStateChanged.Fire(0,c:GetID(),910,false);pp();assert(current(c)==10 and applied().applied==10)")
 def test_native_create_mutates_then_throws_does_not_claim_success(self):
  v=runtime();v.execute("nextTier();local create=P.CreateBuilding;P.CreateBuilding=function(q,id)create(q,id);error('AFTER_NATIVE_MUTATION')end;pp();local a=applied();assert(current(c)==10 and a.appliedStatus=='UNKNOWN'and a.applied==nil and a.lastConfirmed==5)")
 def test_native_readback_unknown_never_confirms_new_carrier(self):
  v=runtime();v.execute("nextTier();local has=P.HasBuilding;P.HasBuilding=function(b,id)if b.city==c and id==910 and c.fx[id]then return nil end;return has(b,id)end;pp();assert(current(c)==10 and applied().appliedStatus=='UNKNOWN'and applied().lastConfirmed==5)")
 def test_health_invalidates_exact_scope_immediately_and_recovers_at_existing_publish(self):
  v=runtime();v.execute("local a,b=facts(c),facts(other);loss(c);assert(effects.Applied(a).appliedStatus=='UNKNOWN'and effects.Applied(b).appliedStatus=='KNOWN');pp();assert(effects.Applied(a).applied==5 and effects.Applied(b).applied==5)")
 def test_new_health_cause_during_create_cannot_be_overwritten_by_old_success(self):
  v=runtime();v.execute("local create=P.CreateBuilding;local once=true;P.CreateBuilding=function(q,id)create(q,id);if once and q.city==c then once=false;GameEvents.BuildingPillageStateChanged.Fire(0,c:GetID(),id,true)end end;loss(c);pp();assert(current(c)==5 and applied().appliedStatus=='UNKNOWN');pp();assert(applied().applied==5)")
 def test_owner_mark_and_same_fact_input_during_create_protect_newer_cause(self):
  v=runtime();v.execute("states={};local update=effects.Update;effects.Update=function(pid,city)update(pid,city);if city==c then states[#states+1]=applied().appliedStatus end end;local create=P.CreateBuilding;local once=true;P.CreateBuilding=function(q,id)create(q,id);if once then once=false;effects.Mark(0);assert(applied().appliedStatus=='UNKNOWN')end end;loss(c);pp();assert(current(c)==5 and states[1]=='UNKNOWN'and states[#states]=='KNOWN'and applied().applied==5)")
 def test_same_ID_different_token_or_coordinate_never_borrows_old_applied(self):
  v=runtime();v.execute("local f=facts();local copy=M.Copy(f);copy.token='ANOTHER';assert(effects.Applied(copy).appliedStatus=='UNOBSERVED');copy=M.Copy(f);copy.x=copy.x+99;assert(effects.Applied(copy).appliedStatus=='UNOBSERVED');copy=M.Copy(f);copy.owner=9;assert(effects.Applied(copy).appliedStatus=='UNOBSERVED')")
 def test_unscoped_input_failure_diagnostic_getter_reentry_does_not_invalidate_newer_success(self):
  v=runtime();v.execute("local read=shared.EffectiveFacts.Read;local owner=c.GetOwner;local once=true;shared.EffectiveFacts.Read=function(...)if once then once=false;error('ONE_UNKNOWN')end;return read(...)end;local later=false;c.GetOwner=function(...)if not once and not later then later=true;effects.Update(0,c)end;return owner(...)end;effects.Update(0,c);assert(applied().applied==5 and current(c)==5)")
 def test_error_text_throw_preserves_original_object_and_releases_publication_depth(self):
  v=runtime();v.execute("local read=shared.EffectiveFacts.Read;local why={why='TEXT_FAILURE'};local failure=setmetatable({},{__tostring=function()error(why)end});shared.EffectiveFacts.Read=function()error(failure)end;local ok,e=pcall(effects.Update,0,c);assert(not ok and rawequal(e,why));shared.EffectiveFacts.Read=read;effects.Update(0,c);assert(applied().applied==5)")
 def test_original_diagnostic_getter_throw_releases_depth_and_keeps_object(self):
  v=runtime();v.execute("local read=shared.EffectiveFacts.Read;local owner=c.GetOwner;local failed=false;local why={why='DIAGNOSTIC'};shared.EffectiveFacts.Read=function()failed=true;error('BASE')end;c.GetOwner=function(...)if failed then error(why)end;return owner(...)end;local ok,e=pcall(effects.Update,0,c);assert(not ok and rawequal(e,why));shared.EffectiveFacts.Read=read;c.GetOwner=owner;effects.Update(0,c);assert(applied().applied==5)")
 def test_diagnostic_reentry_for_other_city_does_not_hide_original_scoped_failure(self):
  v=runtime();v.execute("local a,b=facts(c),facts(other);local read=shared.EffectiveFacts.Read;local owner=c.GetOwner;local failed=false;local once=true;shared.EffectiveFacts.Read=function(pid,city)if city==c then failed=true;error('ONLY_A')end;return read(pid,city)end;c.GetOwner=function(...)if failed and once then once=false;effects.Update(0,other)end;return owner(...)end;effects.Update(0,c);assert(effects.Applied(a).appliedStatus=='UNKNOWN'and effects.Applied(b).applied==5)")
 def test_old_source_is_unavailable_without_native_work(self):
  v=runtime();v.execute("local f=facts();shared.ResearchTraditionEffects={};assert(effects.Applied(f).appliedStatus=='UNAVAILABLE'and effects.Applied(f).reason=='SOURCE_REPLACED')")
 def test_capacity_limit_only_disables_new_publication_not_original_carrier_work(self):
  v=runtime();v.execute("shared.EffectiveFacts.Read=function(pid,city)return {owner=pid,cityID=city.id,x=city.id,y=100,token='SLOT:'..city.id,specialization='CULTURE',potential=1,active=1,activeStatus='KNOWN',investmentPending=false}end;for i=1,2047 do local city={id=10000+i,fx={},damage={}};function city:GetOwner()return 0 end;function city:GetID()return self.id end;function city:GetBuildings()return {city=self}end;local reads=fxReads;effects.Update(0,city);assert(fxReads==reads+5 and not effects.lastError);local a=effects.Applied(shared.EffectiveFacts.Read(0,city));if i<=2046 then assert(a.applied==0 and a.appliedStatus=='KNOWN')else assert(a.appliedStatus=='UNAVAILABLE'and a.reason=='PUBLICATION_CAPACITY')end end")

class Exit(unittest.TestCase):
 def test_actual_store_exit_publishes_zero_only_after_confirmed_withdrawal(self):
  v=runtime();v.execute("local old=facts();T.loss(c,9,900);assert(current(c)==0);local a=effects.Applied(old);assert(a.appliedStatus=='KNOWN'and a.applied==0 and a.gate=='INELIGIBLE'and a.reason=='EXIT_CONFIRMED')")
 def test_failed_cleanup_keeps_last_confirmed_and_known_exit_gate(self):
  v=runtime();v.execute("local old=facts();failRemove=true;T.loss(c,9,900);local a=effects.Applied(old);assert(a.appliedStatus=='UNKNOWN'and a.applied==nil and a.lastConfirmed==5 and a.gate=='INELIGIBLE'and current(c)==5)")
 def test_unconfirmed_exit_ticket_or_locator_cannot_publish_zero(self):
  for method in ('IsExitCurrent','ReferenceToken'):
   v=runtime();v.execute("local old=facts();shared.CityProgressionStore[...]=function()return false end;T.loss(c,9,900);local a=effects.Applied(old);assert(current(c)==0 and a.appliedStatus=='UNKNOWN'and a.lastConfirmed==5)",method)
 def test_newer_exit_zero_is_not_invalidated_by_older_failed_update_diagnostic(self):
  v=runtime();v.execute("local old=facts();shared.EffectiveFacts.Read=function()error('OLD_BASE_FAILURE')end;local get=c.GetID;local once=true;c.GetID=function(...)local id=get(...);if once then once=false;T.loss(c,9,900)end;return id end;effects.Update(0,c);local a=effects.Applied(old);assert(current(c)==0 and a.appliedStatus=='KNOWN'and a.applied==0 and a.lastConfirmed==0 and a.reason=='EXIT_CONFIRMED')")
 def test_exit_during_inflight_native_application_remains_unknown_after_old_writer_returns(self):
  v=runtime();v.execute("nextTier();local old=facts();local remove=P.RemoveBuilding;local once=true;P.RemoveBuilding=function(b,id)remove(b,id);if once and b.city==c then once=false;T.loss(c,9,900)end end;effects.Update(0,c);local a=effects.Applied(old);assert(a.appliedStatus=='UNKNOWN'and a.applied==nil and a.lastConfirmed==5)")
 def test_return_with_new_local_ID_then_second_loss_uses_fixed_location(self):
  v=runtime();v.execute("local original=c:GetID();T.loss(c,9,900);c.s.ref.owner=0;c.s.ref.cityID=original+1000;Events.CityTransfered.Fire(0,original+1000,9);assert(T.record(c).stage=='ACTIVE');effects.Update(0,c);local next=facts();assert(next.cityID==original+1000 and applied().applied==0);T.loss(c,9,901);assert(effects.Applied(next).appliedStatus=='KNOWN'and effects.Applied(next).applied==0)")

class Differential(unittest.TestCase):
 def test_original_values_history_and_all_native_work_match_with_no_extra_ID_sample(self):
  out=[]
  for old in (True,False):
   with before()if old else nullcontext():v=fixture()
   v.execute("counts={};for _,name in ipairs({'GetOwner','GetID','GetX','GetY','GetProperty','GetBuildings','GetBuildQueue'})do local get=c[name];c[name]=function(...)counts[name]=(counts[name]or 0)+1;return get(...)end end;local r,w=fxReads,fxWrites;local h=history();effects.Update(0,c);result=tostring(current(c))..':'..tostring(history()==h);carrierReads=fxReads-r;carrierWrites=fxWrites-w")
   out.append((v.globals().result,v.globals().carrierReads,v.globals().carrierWrites,dict(v.globals().counts)))
  self.assertEqual(out[0][:3],out[1][:3]);delta={k:out[1][3].get(k,0)-value for k,value in out[0][3].items()};self.assertEqual(delta,{k:0 for k in out[0][3]})
  measure('S9d1_Tradition_publisher_cost',{'baseline':BASE,'same_carrier_reads_writes_and_history':True,'extra_native_getters_per_Update':0,'fact_resamples':0,'extra_idle_native_reads':0,'native_CPU_or_memory_claim':False})
 def test_one_shot_native_ID_failure_is_not_consumed_by_a_new_observer_read(self):
  out=[]
  for old in (True,False):
   with before()if old else nullcontext():v=fixture()
   v.execute("local id=c.GetID;local once=true;c.GetID=function(...)if once then once=false;error('ONE_NATIVE_ID_FAILURE')end;return id(...)end;local r,w=fxReads,fxWrites;effects.Update(0,c);errorCode=effects.lastError.reason:match('ONE_NATIVE_ID_FAILURE');unchanged=current(c)==5 and fxReads==r and fxWrites==w")
   out.append((v.globals().errorCode,v.globals().unchanged))
  self.assertEqual(out[0],out[1]);self.assertEqual(out[1],('ONE_NATIVE_ID_FAILURE',True))


def load_tests(loader,standard,pattern):
 selection=json.loads((ROOT/'DevelopmentTests/refactor_selection.json').read_text())
 return unittest.TestSuite([standard,unittest.TestSuite(loader.loadTestsFromName(name)for name in selection['stages']['S9a3e'])])
if __name__=='__main__':unittest.main()
