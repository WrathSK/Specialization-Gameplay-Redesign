"""Approved actual deferred lifecycle recovery: exact Store CAS and no native replay."""
from contextlib import contextmanager
from hashlib import sha256
from pathlib import Path
from unittest.mock import patch
import json,subprocess,unittest
from refactor_harness import ROOT,TrackedLua51,SOURCES,measure
from test_refactor_s9f3 import actual,SETUP as CAPTURE_SETUP
from test_refactor_s8b7b import partial
from test_refactor_s9f1 import plain

@contextmanager
def capture_only():
 p=ROOT/'Mod/CityProgressionStore.lua';text=subprocess.check_output(['git','show','d3986e1:Mod/CityProgressionStore.lua'],cwd=ROOT,text=True)
 read,execute=Path.read_text,TrackedLua51.execute;h=sha256(text.encode()).hexdigest()
 def run(vm,s,*a,**kw):
  if sha256(s.encode()if isinstance(s,str)else s).hexdigest()==h:SOURCES[h]='historical/d3986e1/Mod/CityProgressionStore.lua'
  return execute(vm,s,*a,**kw)
 with patch.object(Path,'read_text',lambda p2,*a,**kw:text if p2==p else read(p2,*a,**kw)),patch.object(TrackedLua51,'execute',run):yield


def pending(keys='commerce',back=True):
 # Test-only private seam targets the same helper without failing unrelated
 # earlier LoadScreenClose listeners when injecting a clock/native exception.
 p=ROOT/'Mod/CityProgressionStore.lua';read=Path.read_text;source=read(p)
 marker=' restore() -- before Binding/Journal/Flow/Investment register load callbacks'
 source=source.replace(marker,' __s9_recover=__s9_recover or {};__s9_recover[storage]=recoverDeferred;'+marker)
 with patch.object(Path,'read_text',lambda p2,*a,**kw:source if p2==p else read(p2,*a,**kw)):v=actual()
 v.execute('prepare(...);lose()'+(';takeBack()'if back else '')+";function recoverNow()return __s9_recover[T.storage(ca)]('TEST_BOUNDARY')end",keys)
 return v


def rep_pending():
 v=partial('n.commerce.reputation=M.Copy(T.record(c).commerce.reputation);')
 v.execute(CAPTURE_SETUP+"""
 ca=c;originalID=c:GetID();s.RegisterExit('Fixture',function()end)
 local validate=SPCCommerceModel.ValidateReputation
 SPCCommerceModel.ValidateReputation=function(value,...)if value~=nil then error('TEMPORARY_REPUTATION_VALIDATOR')end;return validate(value,...)end
 function readersAvailable()SPCCommerceModel.ValidateReputation=validate end
 testReload();s=shared.CityProgressionStore;s.RegisterExit('Fixture',function()end);oldRep=M.Copy(T.record(c).commerce.reputation)
 lose();takeBack()
 """)
 return v


class AtomicRecovery(unittest.TestCase):
 def test_all_five_valid_owners_transform_clear_and_commit_once_without_changing_completed_history(self):
  v=pending('dialogue,engineering,capital,development,commerce');v.execute("readersAvailable();local r=T.record(ca);local bytes=payloads(r);local w=T.writes();testReload();s=shared.CityProgressionStore;r=T.record(ca);assert(not r.deferredLifecycle and T.writes()==w+1 and #r.commerce.selected==0 and r.dialogue.total==15 and r.engineering.L==1);assert(s.DialogueState(0,ca).value.used.ERA_ANCIENT and not s.Status(ca).subrecordIsolation.commerce and #s.Status(ca).deferredRecovery.keys==5);local w=T.writes();testReload();assert(T.writes()==w and not shared.CityProgressionStore.Status(ca).deferredRecovery)")
  measure('S9f4_atomic_deferred_recovery',{'actual_Store':True,'recovered_owners':5,'recovery_Store_commits':1,'second_load_commits':0,'completion_or_money_calls':0,'completed_history_preserved':True})
 def test_unknown_owner_stays_opaque_while_reliable_sibling_recovers(self):
  v=pending('commerce,dialogue');v.execute("readersAvailable();unavailable('dialogue');local before=T.encode(T.record(ca).dialogue);local w=T.writes();testReload();s=shared.CityProgressionStore;assert(T.writes()==w+1 and T.record(ca).deferredLifecycle.entries.dialogue and not T.record(ca).deferredLifecycle.entries.commerce and T.encode(T.record(ca).dialogue)==before);assert(pcall(s.CommerceState,0,ca)and not pcall(s.DialogueState,0,ca));assert(s.Status(ca).deferredRecoveryErrors.dialogue and not s.Status(ca).deferredRecoveryErrors.commerce)")
 def test_actual_cold_context_roundtrip_uses_persisted_episode_not_a_session_sidecar(self):
  v=pending();saved=plain(v.eval('T.record(ca)'))
  c=actual();c.execute('local value=...;T.propsSet(T.key(ca),value);local w=T.writes();testReload();s=shared.CityProgressionStore;assert(T.writes()==w+1 and not T.record(ca).deferredLifecycle and #s.CommerceState(0,ca).value.selected==0)',c._lua.table_from(saved,recursive=True))
 def test_held_foreign_record_cancels_and_clears_without_admitting_foreign_owner(self):
  v=pending('commerce,dialogue',False);v.execute("readersAvailable();local w=T.writes();testReload();s=shared.CityProgressionStore;local r=T.record(ca);assert(r.stage=='HELD_TRANSFER'and not r.deferredLifecycle and r.commerce.owner==9 and #r.commerce.selected==0 and r.dialogue.total==15 and T.writes()==w+1);assert(not pcall(s.Base,9,ca)and not pcall(s.Base,0,ca))")
 def test_readonly_queries_and_idle_events_never_retry_unknown_payload(self):
  v=pending();v.execute("local r=T.encode(T.record(ca));local w=T.writes();for i=1,1000 do Events.GameCoreEventPublishComplete.Fire()end;for i=1,4 do T.turn(1)end;for i=1,30 do shared.CityProgressionStore.Describe(0,ca)end;assert(T.writes()==w and T.encode(T.record(ca))==r)")
 def test_existing_load_completion_boundary_recovers_same_worker_once(self):
  v=pending('commerce,dialogue');v.execute("local w=T.writes();readersAvailable();Events.LoadScreenClose.Fire();s=shared.CityProgressionStore;assert(T.writes()==w+1 and not T.record(ca).deferredLifecycle and #s.CommerceState(0,ca).value.selected==0 and s.DialogueState(0,ca).value.total==15);Events.LoadScreenClose.Fire();assert(T.writes()==w+1)")
 def test_reputation_only_recovery_retains_new_postreturn_domain_selection_and_origin(self):
  v=rep_pending();v.execute("local old=s.CommerceState(0,ca).value;local n=SPCCommerceModel.Select(old,'DISTRICT_THEATER',true);s.WriteCommerce(0,ca,old,n);local w=T.writes();T.turn(20);readersAvailable();Events.LoadScreenClose.Fire();s=shared.CityProgressionStore;local state=s.CommerceState(0,ca);assert(state.reputationKnown and state.value.selected[1]=='DISTRICT_THEATER'and state.value.reputation.age==oldRep.age and state.value.reputation.receipt==oldRep.receipt and state.value.reputation.start==oldRep.start and state.value.reputation.cursor==T.now()and not T.record(ca).deferredLifecycle and T.writes()==w+1)")
 def test_missing_or_corrupt_permanent_history_is_never_constructed_as_zero(self):
  for change in ("n.dialogue=nil","n.dialogue.total=999","n.capital={future=2}"):
   v=pending('dialogue,capital');v.execute("readersAvailable();local n=M.Copy(T.record(ca));"+change+";local bytes=install(n);testReload();s=shared.CityProgressionStore;local after=T.record(ca);assert(after.deferredLifecycle and T.encode(after.dialogue)==T.encode(n.dialogue)and T.encode(after.capital)==T.encode(n.capital))")
 def test_unknown_clock_or_active_native_reference_keeps_original_and_waits_related_boundary(self):
  for cause in ('clock','location','binding'):
   v=pending();v.execute("readersAvailable();mode=...;local get=Game.GetCurrentGameTurn;local city=CityManager.GetCityAt;local prop=ca.GetProperty;if mode=='clock'then Game.GetCurrentGameTurn=function()error('CLOCK_UNAVAILABLE')end elseif mode=='location'then CityManager.GetCityAt=function()error('CITY_UNAVAILABLE')end else ca.GetProperty=function()error('BINDING_UNAVAILABLE')end end;local w=T.writes();recoverNow();assert(T.writes()==w and T.record(ca).deferredLifecycle);Game.GetCurrentGameTurn=get;CityManager.GetCityAt=city;ca.GetProperty=prop;for i=1,100 do Events.GameCoreEventPublishComplete.Fire()end;assert(T.writes()==w);recoverNow();assert(T.writes()==w+1 and not T.record(ca).deferredLifecycle)",cause)
 def test_newer_synchronous_root_at_recovery_clock_rejects_older_candidate(self):
  v=pending();v.execute("readersAvailable();local get=Game.GetCurrentGameTurn;local once=true;Game.GetCurrentGameTurn=function()if once then once=false;local n=M.Copy(T.record(ca));n.revision=n.revision+1;assert(saveCandidate(ca,n))end;return get()end;local w=T.writes();recoverNow();assert(T.writes()==w+1 and T.record(ca).deferredLifecycle and shared.CityProgressionStore.Status(ca).deferredRecoveryError:find('SUPERSEDED'));Game.GetCurrentGameTurn=get;recoverNow();assert(T.writes()==w+2 and not T.record(ca).deferredLifecycle)")
 def test_normal_private_save_cannot_clear_evidence_or_forge_recovery_capability(self):
  v=pending();v.execute("local n=M.Copy(T.record(ca));n.revision=n.revision+1;n.deferredLifecycle=nil;local w=T.writes();assert(not saveCandidate(ca,n)and T.writes()==w);local ok=pcall(__s8_save[T.storage(ca)],n,nil,{capability={},previous=T.record(ca),plans={}});assert(not ok and T.writes()==w and T.record(ca).deferredLifecycle)")
 def test_no_optimistic_api_publication_during_native_recovery_write(self):
  v=pending();v.execute("readersAvailable();local set=Game.SetProperty;local key=T.key(ca);callbacks=0;Game.SetProperty=function(o,k,value)if k==key then callbacks=callbacks+1;assert(not pcall(shared.CityProgressionStore.CommerceState,0,ca))end;return set(o,k,value)end;Events.LoadScreenClose.Fire();assert(callbacks==1 and not T.record(ca).deferredLifecycle and pcall(shared.CityProgressionStore.CommerceState,0,ca))")
 def test_capture_and_recovery_after_multiple_same_turn_episodes_use_latest_exact_reference(self):
  v=pending();v.execute("T.loss(ca,8,800);ca.s.ref.owner=0;ca.s.ref.cityID=originalID;Events.CityTransfered.Fire(0,originalID,8);assert(T.record(ca).ownerChanges==2 and T.record(ca).deferredLifecycle.entries.commerce.epoch==2);readersAvailable();Events.LoadScreenClose.Fire();assert(not T.record(ca).deferredLifecycle and #shared.CityProgressionStore.CommerceState(0,ca).value.selected==0)")
 def test_pure_plans_or_getters_cannot_clear_a_newer_episode(self):
  v=pending();v.execute("local r=M.Copy(T.record(ca));local old=SPCStoreDeferredLifecycle.Entry(r.deferredLifecycle,'commerce',r);T.loss(ca,8,800);r=M.Copy(T.record(ca));assert(not pcall(SPCStoreLifecycleRecovery.Plan,r,'commerce',old,T.now()));assert(T.record(ca).deferredLifecycle.entries.commerce.epoch==2)")
 def test_selected_city_report_reads_pending_or_completed_status_without_repair(self):
  v=pending();v.execute("local w=T.writes();local text=shared.CityProgressionStore.Describe(0,ca);assert(text:find('易主处理待恢复',1,true)and T.writes()==w);readersAvailable();Events.LoadScreenClose.Fire();text=shared.CityProgressionStore.Describe(0,ca);assert(text:find('已恢复遗漏的易主处理',1,true)and not text:find('易主处理待恢复',1,true));local n=T.writes();for i=1,50 do shared.CityProgressionStore.Describe(0,ca)end;assert(T.writes()==n)")


class OriginalAbilityRules(unittest.TestCase):
 def test_actual_Tradition_retains_age_origin_and_counts_only_after_reliable_recovery(self):
  from test_refactor_s5d4c7 import fixture
  v=fixture();v.execute("for i=1,3 do T.turn(1)end;local original=M.Copy(T.record(c).researchTradition);local validate=SPCResearchTradition.Validate;SPCResearchTradition.Validate=function(value,...)if value~=nil then error('TEMPORARY_TRADITION_READER')end;return validate(value,...)end;T.reload();local s=shared.CityProgressionStore;local id=c:GetID();s.RegisterExit('Fixture',function()end);T.loss(c,9,900);T.turn(20);c.s.ref.owner=0;c.s.ref.cityID=id;Events.CityTransfered.Fire(0,id,9);assert(T.record(c).deferredLifecycle.entries.researchTradition);SPCResearchTradition.Validate=validate;T.reload();s=shared.CityProgressionStore;local t=s.ReadTradition(0,c);assert(t.age==original.age and t.receipt==original.receipt and t.start==original.start and t.cursor==T.now()and t.state=='COUNTING'and not T.record(c).deferredLifecycle);T.turn(1);assert(s.ReadTradition(0,c).age==original.age+1)")
 def test_confirmed_loss_cancels_only_transient_claim_timer_without_native_completion_or_receipt(self):
  v=actual();v.execute("local n=seed();n.claimTimer={version=1,stage='CALLING',unreadable='opaque'};install(n);testReload();s=shared.CityProgressionStore;s.RegisterExit('Fixture',function()end);local id=ca:GetID();T.loss(ca,9,900);assert(T.record(ca).deferredLifecycle.entries.claimTimer);ca.s.ref.owner=0;ca.s.ref.cityID=id;Events.CityTransfered.Fire(0,id,9);local w=T.writes();testReload();assert(not T.record(ca).claimTimer and not T.record(ca).claim and not T.record(ca).deferredLifecycle and T.writes()==w+1)")
 def test_Industry_return_keeps_exact_history_until_current_catalogue_is_available(self):
  from test_refactor_s8b8 import templates
  v=templates('');v.execute("local validate=M.ValidateTemplates;local bytes=T.encode(T.record(ca).templates);M.ValidateTemplates=function()error('TEMPLATE_READER_UNAVAILABLE')end;testReload();s=shared.CityProgressionStore;s.RegisterExit('Fixture',function()end);local id=ca:GetID();T.loss(ca,9,900);ca.s.ref.owner=0;ca.s.ref.cityID=id;Events.CityTransfered.Fire(0,id,9);assert(T.record(ca).deferredLifecycle.entries.templateLifecycle);M.ValidateTemplates=validate;testReload();s=shared.CityProgressionStore;assert(T.record(ca).deferredLifecycle.entries.templateLifecycle and not pcall(s.ReadTemplates,ca)and T.encode(T.record(ca).templates)==bytes);local w=T.writes();local calls=0;shared.Standardization={ValidateHistory=function(city,value)assert(city==ca and T.encode(value)==bytes);calls=calls+1 end};Events.LoadScreenClose.Fire();assert(calls==1 and T.writes()==w+1 and not T.record(ca).deferredLifecycle and T.encode(T.record(ca).templates)==bytes and T.record(ca).templateLifecycle.reconcilePending)")
 def test_exact_related_city_initialization_is_a_recovery_boundary_foreign_initialization_is_not(self):
  v=pending();v.execute("readersAvailable();local w=T.writes();Events.CityInitialized.Fire(9,999,999,999);assert(T.writes()==w and T.record(ca).deferredLifecycle);Events.CityInitialized.Fire(0,ca:GetID(),ca:GetX(),ca:GetY());assert(T.writes()==w+1 and not T.record(ca).deferredLifecycle)")


class WriteFaults(unittest.TestCase):
 def test_setter_or_readback_uncertainty_preserves_fault_without_retry_or_replay(self):
  for mode in ('DROP','THROW_BEFORE','THROW_AFTER','READBACK_THROW','READBACK_STALE'):
   v=pending();v.execute("""
   mode=...;readersAvailable();local key=T.key(ca);local old=M.Copy(T.record(ca));local set,get=Game.SetProperty,Game.GetProperty;attempts=0;afterSet=false
   Game.SetProperty=function(o,k,value)
    if k~=key then return set(o,k,value)end;attempts=attempts+1
    if mode=='DROP'then return end;if mode=='THROW_BEFORE'then error('UNKNOWN_WRITE')end
    set(o,k,value);afterSet=true;if mode=='THROW_AFTER'then error('UNKNOWN_WRITE_AFTER')end
   end
   Game.GetProperty=function(o,k)
    if k==key and afterSet then
     if mode=='READBACK_THROW'then error('READBACK_UNKNOWN')end
     if mode=='READBACK_STALE'then return M.Copy(old)end
    end
    return get(o,k)
   end
   Events.LoadScreenClose.Fire();s=shared.CityProgressionStore;assert(attempts==1 and not pcall(s.Base,0,ca)and pcall(s.Base,0,cb)and not s.Status(ca).deferredRecovery)
   for i=1,1000 do Events.GameCoreEventPublishComplete.Fire()end;Events.LoadScreenClose.Fire();assert(attempts==1)
   Game.SetProperty=set;Game.GetProperty=get;local w=T.writes();testReload();s=shared.CityProgressionStore
   assert(not T.record(ca).deferredLifecycle and #s.CommerceState(0,ca).value.selected==0)
   assert(T.writes()==w+((mode=='DROP'or mode=='THROW_BEFORE')and 1 or 0))
   """,mode)
 def test_confirmed_native_write_cannot_release_protection_after_synchronous_lifecycle_reentry(self):
  v=pending();v.execute("readersAvailable();local set=Game.SetProperty;local key=T.key(ca);local once=true;Game.SetProperty=function(o,k,value)if k==key and once then once=false;T.loss(ca,8,800)end;return set(o,k,value)end;Events.LoadScreenClose.Fire();s=shared.CityProgressionStore;assert(not pcall(s.Base,0,ca)and not pcall(s.Base,8,ca)and not s.Status(ca).deferredRecovery and s.Status(ca).subrecordIsolation.commerce)")
 def test_stale_native_prewrite_never_calls_setter_or_discards_pending_episode(self):
  v=pending();v.execute("readersAvailable();local key=T.key(ca);local get,set=Game.GetProperty,Game.SetProperty;local first=true;attempts=0;Game.GetProperty=function(o,k)local value=get(o,k);if k==key and first then first=false;value=M.Copy(value);value.revision=value.revision+1 end;return value end;Game.SetProperty=function(o,k,value)if k==key then attempts=attempts+1 end;return set(o,k,value)end;Events.LoadScreenClose.Fire();assert(attempts==0 and T.record(ca).deferredLifecycle and not pcall(shared.CityProgressionStore.Base,0,ca))")


class ProductionClosure(unittest.TestCase):
 def test_real_Development_skipped_loss_and_return_terminates_paid_contract_and_withdraws_target(self):
  import test_refactor_s9e9 as old_case
  # Reuse its full real-owner assertions; its original B382 'no added fields'
  # measurement is historical and does not describe this approved cutover.
  with patch.object(old_case,'measure',lambda *a,**k:None):
   old_case.Recovery().test_actual_valid_transient_loss_return_reload_closes_old_Development()
  measure('S9f4_actual_Development_recovery',{'saved_witness':'deferredLifecycle','actual_paid_contract':'TERMINATED','actual_target':'withdrawn','native_money_replay':0})
 def test_same_worker_Development_index_and_actual_fact_consumer_recover_without_native_replay(self):
  from test_refactor_s9b1 import runtime
  v=runtime();v.execute("""
  assert(sign());local id=source:GetID();local decode=SPCDevelopmentInvestmentModel.Decode
  SPCDevelopmentInvestmentModel.Decode=function(value)if value~=nil then error('TEMPORARY_READER_UNKNOWN')end;return decode(value)end
  reload();local info=P.Info;P.Info=function(kind,key)local r=info(kind,key);if kind=='Buildings'and key=='BUILDING_SPC_CAPITAL_ACCESS'then r.InternalOnly=1 end;return r end
  T.loss(source,9,900);source.s.ref.owner=0;source.s.ref.cityID=id;Events.CityTransfered.Fire(0,id,9)
  assert(T.record(source).deferredLifecycle.entries.development);local m=moneyCalls
  SPCDevelopmentInvestmentModel.Decode=decode;Events.LoadScreenClose.Fire();if shared.FactChanges then shared.FactChanges.Flush()end;if shared.FactBindings then shared.FactBindings.Flush()end;Events.GameCoreEventPublishComplete.Fire()
  assert(contract().stage=='TERMINATED'and not active()and moneyCalls==m and not T.record(source).deferredLifecycle)
  """)
 def test_only_narrow_history_topics_reach_new_capital_and_development_edges(self):
  from refactor_harness import Context
  v=Context();v.load('FactChanges');v.load('FactConsumerBindings');v.execute("""
  SPCFactChanges.New(shared);SPCFactConsumerBindings.New(shared)
  marks=0;shared.CapitalInvestment={Mark=function(pid,id)assert(pid==0 and id==7);marks=marks+1 end}
  function emit(topic)shared.FactChanges.Emit({owner=0,cityID=7,reference='R',revision=1,cause='RECOVERY',kinds={'HISTORY'},topic=topic});shared.FactChanges.Flush();shared.FactBindings.Flush()end
  emit('COMMERCE');assert(marks==0);emit('CAPITAL_RECOVERY');assert(marks==1);emit('DEVELOPMENT_RECOVERY');assert(marks==1)
  """)
  text=(ROOT/'Mod/DevelopmentInvestment.lua').read_text();self.assertIn("topics={'DEVELOPMENT_RECOVERY'}",text)


from test_refactor_s6e import Profile,observed
class CapitalRecovery(Profile,unittest.TestCase):
 def test_actual_paid_Capital_recovery_preserves_receipt_and_never_replays_money(self):
  v=observed();v.execute("assert(C.confirm());local id=source:GetID();local debited=C.contract().debited;local decode=SPCCapitalInvestmentModel.Decode;SPCCapitalInvestmentModel.Decode=function(value)if value~=nil then error('TEMPORARY_CAPITAL_DECODER')end;return decode(value)end;C.reload();local info=P.Info;P.Info=function(kind,key)local r=info(kind,key);if kind=='Buildings'and key=='BUILDING_SPC_CAPITAL_ACCESS'then r.InternalOnly=1 end;return r end;T.loss(source,9,900);source.s.ref.owner=0;source.s.ref.cityID=id;Events.CityTransfered.Fire(0,id,9);assert(T.record(source).deferredLifecycle.entries.capital);local m=moneyCalls;SPCCapitalInvestmentModel.Decode=decode;C.reload();assert(C.contract().stage=='TERMINATED'and C.contract().reason=='CAPITAL_OWNER_CHANGED'and C.contract().debited==debited and not T.record(source).deferredLifecycle and moneyCalls==m);local w=T.writes();for i=1,1000 do Events.GameCoreEventPublishComplete.Fire()end;assert(T.writes()==w and moneyCalls==m)")
  measure('S9f4_actual_Capital_recovery',{'paid_receipt_preserved':True,'actual_contract':'TERMINATED','native_money_replay':0,'idle_pulses':1000,'extra_idle_Store_writes':0})


FROZEN={
 'test_readers_available_after_return_do_not_expose_pre_loss_configuration_on_cold_load',
 'test_pending_owner_cannot_write_or_delete_opaque_payload',
 'test_pending_markers_cannot_be_repaired_before_lifecycle_transform',
 'test_valid_sibling_still_commits_while_deferred_group_is_preserved',
 'test_actual_production_includes_only_capture_model_and_retains_Copy_limits'}
class FrozenCapture(unittest.TestCase):
 def test_original_interim_protection_assertions_stay_exact_on_B386(self):
  from test_refactor_s9f3 import Capture
  with capture_only():
   for name in sorted(FROZEN):getattr(Capture(),name)()

def load_tests(loader,standard,pattern):
 suite=unittest.TestSuite([standard])
 for case in loader.loadTestsFromName('test_refactor_s9f3.Capture'):
  if case._testMethodName not in FROZEN:suite.addTest(case)
 for name in ('test_refactor_s9f1','test_refactor_s9f2'):
  suite.addTests(loader.loadTestsFromName(name))
 return suite

if __name__=='__main__':unittest.main()
