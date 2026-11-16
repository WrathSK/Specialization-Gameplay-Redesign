"""PU09 actual project/Store/EF marker roots;PU10 existing Governor proof.
Explicit native doubles,not native queue cancellation or all cold-load acceptance.
"""
from contextlib import contextmanager
from pathlib import Path
from unittest.mock import patch
from hashlib import sha256
import subprocess,unittest
from refactor_harness import ROOT,TrackedLua51,SOURCES,executed,measure,legacy_source_observation
from test_pu07a_completion_scope import claims
from test_refactor_s7d1 import profile
from test_dialogue_projects import game
BASE='7729420'
@contextmanager
def baseline():
 sources={ROOT/'Mod'/(n+'.lua'):subprocess.check_output(['git','show',BASE+':Mod/'+n+'.lua'],cwd=ROOT,text=True)for n in ('ClaimProjects','DialogueProjects')};read=Path.read_text
 with patch.object(Path,'read_text',lambda p,*a,**kw:sources[p]if p in sources else read(p,*a,**kw)),legacy_source_observation():yield

def dialogue(skip=False):
 with profile():v=game(skip_controller_load=skip)
 v.execute("""
 markerWrites=0;local add,remove=P.CreateBuilding,P.RemoveBuilding
 P.CreateBuilding=function(...)markerWrites=markerWrites+1;return add(...)end
 P.RemoveBuilding=function(...)markerWrites=markerWrites+1;return remove(...)end
 function refresh()dp.Sync(0,c:GetID(),'MARKER_ROOT')end
 oldGovernor=P.GovernorGate
 function unknownGovernor()P.GovernorGate=function(city)if city==c then return 0,c:GetID(),'UNKNOWN',nil end;return oldGovernor(city)end end
 function restoredGovernor()P.GovernorGate=oldGovernor end
 function badEra(value)
  local info=P.Info;P.Info=function(t,k)if t=='Eras'then error('ERA_UNAVAILABLE')end;return info(t,k)end
  ExposedMembers.SPC_DialogueGameEra=function()return value end
 end
 """);return v

class ClaimMarkers(unittest.TestCase):
 def test_unknown_authority_preserves_both_installed_and_absent_without_grant(self):
  for present in (True,False):
   v=claims();v.execute("aCity.q.buildings[201]=...and true or nil;local raw=shared.CityProgressionStore.ClaimState;shared.CityProgressionStore.ClaimState=function(pid,c)if c==aCity then error('TEMP_PARENT_UNAVAILABLE')end;return raw(pid,c)end;local record=T.encode(T.record(aCity));local writes=T.writes();N.flush();assert((aCity.q.buildings[201]==true)==...,'UNKNOWN_CLAIM_CHANGED_INSTALLED_ACCESS');assert(bCity.q.buildings[201]and T.writes()==writes and T.encode(T.record(aCity))==record)",present,present)
 def test_preserved_marker_is_not_new_claim_request_or_completion_qualification(self):
  v=claims();v.execute("local cp=shared.ClaimProjects;local raw=shared.CityProgressionStore.ClaimState;shared.CityProgressionStore.ClaimState=function(pid,c)if c==aCity then error('TEMP_PARENT_UNAVAILABLE')end;return raw(pid,c)end;local record=T.encode(T.record(aCity));local writes=T.writes();N.flush();cp.Request(0,{CityID=aCity:GetID(),Project='PROJECT_SPC_CLAIM_RESEARCH',StartTurn=T.now()});Events.CityProjectCompleted.Fire(0,aCity:GetID(),101);assert(aCity.q.buildings[201]and T.writes()==writes and T.encode(T.record(aCity))==record and not T.record(aCity).claim)")
 def test_related_same_value_recovery_restores_available_without_new_history(self):
  v=claims();v.execute("local store=shared.CityProgressionStore;local raw=store.ClaimState;local record=T.encode(T.record(aCity));local writes=T.writes();store.ClaimState=function(pid,c)if c==aCity then error('TEMP_UNAVAILABLE')end;return raw(pid,c)end;N.flush();store.ClaimState=raw;N.flush();assert(aCity.q.buildings[201]and shared.ClaimProjects.views['0:'..aCity:GetID()].stage=='AVAILABLE');assert(T.writes()==writes and T.encode(T.record(aCity))==record)")
 def test_confirmed_non_candidate_retires_exact_markers(self):
  v=claims();v.execute("local c=N.first(3);T.complete(c,'DISTRICT_CAMPUS');local q={buildings={[201]=true,[202]=true,[9999]=true},CurrentlyBuilding=function()return 'NONE'end};c.GetBuildQueue=function()return q end;c.GetBuildings=function()return q.buildings end;Events.CityProductionUpdated.Fire(0,c:GetID());Events.GameCoreEventPublishComplete.Fire();assert(not q.buildings[201]and not q.buildings[202]and q.buildings[9999]and aCity.q.buildings[201])")
 def test_unknown_parent_never_clear_old_error_or_poll_again_without_cause(self):
  v=claims();v.execute("local raw=shared.CityProgressionStore.ClaimState;local reads=0;shared.CityProgressionStore.ClaimState=function(pid,c)reads=reads+1;if c==aCity then error('UNSAFE_HISTORY')end;return raw(pid,c)end;N.flush();local count,writes=reads,T.writes();for i=1,1000 do Events.GameCoreEventPublishComplete.Fire()end;assert(reads==count and T.writes()==writes and aCity.q.buildings[201]and not T.record(aCity).completionError)")
 def test_actual_same_build_controller_reload_keeps_restored_marker_on_unknown(self):
  v=claims();v.execute("T.reload();local store=shared.CityProgressionStore;local raw=store.ClaimState;store.ClaimState=function(pid,c)if c==aCity then error('EARLY_STORE_READ')end;return raw(pid,c)end;SPCClaimProjects.Start(P,shared);Events.LoadScreenClose.Fire();assert(aCity.q.buildings[201],'COLD_UNKNOWN_REMOVED_RESTORED_CLAIM');store.ClaimState=raw;N.flush();assert(aCity.q.buildings[201]and not T.record(aCity).claim)")

class DialogueMarkers(unittest.TestCase):
 def test_unknown_active_retains_installed_but_cannot_grant_absent(self):
  for present in (True,False):
   v=dialogue();v.execute("c.b.present[998]=...and true or nil;unknownGovernor();local writes=T.writes();refresh();assert((c.b.present[998]==true)==...,'UNKNOWN_ACTIVE_CHANGED_DIALOGUE_MARKER');assert(markerWrites==0 and T.writes()==writes)",present,present)
 def test_unreadable_store_retains_marker_but_rejects_new_start(self):
  v=dialogue();v.execute("local store=shared.CityProgressionStore;local read=store.DialogueState;store.DialogueState=function(pid,city)if city==c then error('LEAF_UNREADABLE')end;return read(pid,city)end;local record=T.encode(T.record(c));refresh();begin(c);assert(c.b.present[998]and not ledger(c)and T.encode(T.record(c))==record and finishes==0 and markerWrites==0)")
 def test_isolated_bad_leaf_keeps_bytes_and_strictly_blocks_start_completion(self):
  for mutation in ('r.dialogue=nil','r.dialogue.total=999','r.dialogue.pending.reference.cityID=999'):
   v=dialogue();v.execute("begin(c);local r=T.record(c);"+mutation+";T.propsSet(T.key(c),r);rawBad=T.encode(r.dialogue);reload();assert(not pcall(shared.CityProgressionStore.DialogueState,0,c));assert(c.b.present[998]and T.encode(T.record(c).dialogue)==rawBad);local w=T.writes();begin(c);Events.CityProjectCompleted.Fire(0,c:GetID(),999);dp.Flush();assert(T.encode(T.record(c).dialogue)==rawBad and T.writes()==w and finishes==0 and shared.EffectiveFacts.Read(0,control).potential==1)")
 def test_existing_deterministic_known_flag_rebuild_remains_confirmed(self):
  v=dialogue();v.execute("begin(c);local r=T.record(c);r.dialogueKnown=nil;local leaf=T.encode(r.dialogue);T.propsSet(T.key(c),r);reload();assert(T.record(c).dialogueKnown==true and T.encode(shared.CityProgressionStore.DialogueState(0,c).value)==leaf and c.b.present[998]and finishes==0)")
 def test_unknown_cannot_complete_and_known_recovery_uses_original_full_turn(self):
  v=dialogue();v.execute("include('FactChanges');SPCFactChanges.New(shared);include('NativeFacts');SPCNativeFacts.New(P,shared);include('FactConsumerBindings');SPCFactConsumerBindings.New(shared);begin(c);local record=T.encode(T.record(c));unknownGovernor();refresh();assert(c.b.present[998]and T.encode(T.record(c))==record and finishes==0);restoredGovernor();Events.GovernorEstablished.Fire(0,c:GetID());shared.FactChanges.Flush();shared.FactBindings.Flush();dp.Flush();endturn();assert(finishes==1 and ledger(c).total==5)")
 def test_bad_or_nil_era_cannot_grant_absent_or_remove_existing(self):
  for value in ('nil','false',"''",'17'):
   for present in (True,False):
    v=dialogue();v.execute("c.b.present[998]="+('true'if present else'nil')+";badEra("+value+");refresh();begin(c);assert((c.b.present[998]==true)=="+str(present).lower()+",'UNKNOWN_ERA_CHANGED_MARKER');assert(markerWrites==0 and not ledger(c)and finishes==0)")
 def test_reliable_active_loss_with_unknown_era_still_withdraws(self):
  v=dialogue();v.execute("T.governor(1);badEra(nil);refresh();assert(not c.b.present[998]and markerWrites==1 and not ledger(c))")
 def test_current_era_used_with_unknown_governor_still_withdraws(self):
  v=dialogue();v.execute("begin(c);endturn();assert(ledger(c).used.ERA_CLASSICAL);c.b.present[998]=true;unknownGovernor();refresh();assert(not c.b.present[998]and ledger(c).used.ERA_CLASSICAL and finishes==1)")
 def test_non_culture_identity_negative_does_not_require_unneeded_governor(self):
  v=dialogue();v.execute("local read=shared.EffectiveFacts.Read;shared.EffectiveFacts.Read=function(pid,city,...)local f=read(pid,city,...);if city==c then f.specialization='RESEARCH';f.active=nil;f.activeStatus='UNKNOWN_GOVERNOR'end;return f end;refresh();assert(not c.b.present[998]and markerWrites==1 and not ledger(c))")
 def test_pending_investment_is_not_positive_qualification(self):
  v=dialogue();v.execute("local read=shared.EffectiveFacts.Read;shared.EffectiveFacts.Read=function(pid,city,...)local f=read(pid,city,...);if city==c then f.investmentPending=true end;return f end;refresh();begin(c);assert(c.b.present[998]and not ledger(c)and markerWrites==0 and finishes==0)")
 def test_early_cold_unknown_reconciles_on_actual_load_same_value(self):
  v=dialogue();v.execute("skipControllerLoad=true;reload();oldGovernor=P.GovernorGate;unknownGovernor();Events.GameCoreEventPublishComplete.Fire();assert(c.b.present[998],'COLD_GOVERNOR_UNKNOWN_REMOVED_MARKER');restoredGovernor();Events.LoadScreenClose.Fire();assert(c.b.present[998]and view(c).stage=='AVAILABLE'and not ledger(c))")
 def test_queue_unknown_is_not_eligibility_unknown_and_idle_does_not_retry(self):
  v=dialogue();v.execute("begin(c);local read=c.q.CurrentlyBuilding;local calls=0;c.q.CurrentlyBuilding=function()calls=calls+1;error('QUEUE_UNKNOWN')end;Events.CityProductionChanged.Fire(0,c:GetID());dp.Flush();local n=calls;assert(c.b.present[998]and ledger(c).pending.stage=='ACTIVE');for i=1,1000 do Events.GameCoreEventPublishComplete.Fire()end;assert(calls==n and finishes==0);c.q.CurrentlyBuilding=read;Events.CityProductionChanged.Fire(0,c:GetID());dp.Flush();endturn();assert(finishes==1)")

class GovernorProducer(unittest.TestCase):
 def test_real_six_property_reader_and_actual_EF_same_phase_recovery(self):
  v=dialogue();source=(ROOT/'Mod/Probe.lua').read_text();start=source.index('local function governorProperty(');end=source.index('-- Selected-city role facts only.',start)
  key='Mod/Probe.lua:governorProperty';executed(key,sha256(source.encode()).hexdigest(),'source_fragment',start=start,end=end)
  v.execute(source[start:end]);v.execute("""
  keys={'SPC_P0_GOV_CONTROL_A007','SPC_P0_GOV_PRESENT','SPC_P0_GOV_ESTABLISHED','SPC_P0_GOV_REQ_2','SPC_P0_GOV_REQ_3','SPC_P0_GOV_REQ_4'}
  props={[keys[1]]=1};reads=0;local get=c.GetProperty
  c.GetProperty=function(city,k)for _,key in ipairs(keys)do if k==key then reads=reads+1;if k==badKey then error('PROPERTY_UNAVAILABLE')end;return props[k]end end;return get(city,k)end
  local facts=shared.EffectiveFacts
  local owner,id,status,level=P.GovernorGate(c);assert(owner==0 and id==c:GetID()and status=='KNOWN'and level==1)
  assert(facts.Read(0,c).active==1)
  props[keys[1]]=nil
  facts.WithPhase('PU10_RESTORE',function()
   assert(facts.Read(0,c).activeStatus=='UNKNOWN_GOVERNOR');props[keys[1]]=1
   for i=2,6 do props[keys[i]]=1 end
   assert(facts.Read(0,c).active==3,'SAME_VALUE_AVAILABILITY_RECOVERY_CACHED_AS_UNKNOWN')
  end)
  props[keys[4]]=0;assert(select(3,P.GovernorGate(c))=='UNKNOWN_INCONSISTENT_PROPERTIES')
  props[keys[4]]=1;badKey=keys[3];assert(select(3,P.GovernorGate(c))=='UNKNOWN')
  badKey=nil;assert(facts.Read(0,c).active==3)
  """)
  measure('PU10_existing_Governor_contract',{'actual_reader':'Probe.lua governorProperty/GovernorGate fragment','actual_consumer':'EffectiveFacts plus Store/Dialogue fixture','no_governor_level':1,'unknown_cached_as_success':False,'production_algorithm_changed':False})
 def test_same_reference_two_confirmed_changes_remain_fresh(self):
  v=dialogue();v.execute("local facts=shared.EffectiveFacts;facts.WithPhase('PU10_TWO_CHANGES',function()T.governor(4);assert(facts.Read(0,c).active==3);T.governor(1);assert(facts.Read(0,c).active==1);T.governor(4);assert(facts.Read(0,c).active==3)end)")

if __name__=='__main__':unittest.main()
