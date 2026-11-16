"""Owner-selectedA: actual Store/Claim attribution, not native availability proof.
Explicit single-callback engine doubles; no HD runtime functions, new events,
probe/persistence/recovery journal. Unattributed post-fault cold recovery OPEN.
"""
from hashlib import sha256
import subprocess,unittest
from refactor_harness import ROOT,SOURCES,executed,measure
from test_refactor_s7d5 import profile
from test_store_write_boundaries import fixture,instrument_store
from test_pu07a_completion_scope import SETUP
BASE='25aaff6d4d63acf8a9041f09d3e1bac4f109561e'
STORE_SOURCE=None
EXTRA=r'''
X={plotReads=0,cityReads=0}
function X.associate(c,kind,x,y)
 local offered
 Map.GetPlot=function(px,py)
  X.plotReads=X.plotReads+1;assert(px==x and py==y,'WRONG_ASSOCIATION_COORDINATES')
  offered={GetOwner=function()return 0 end,GetDistrictType=function()return kind end};return offered
 end
 Cities={GetPlotPurchaseCity=function(plot)assert(plot==offered,'WRONG_PLOT_ARGUMENT');X.cityReads=X.cityReads+1;return c end}
 c.GetDistricts=function()return {GetDistrictAtLocation=function(_,px,py)
  assert(px==x and py==y,'WRONG_CITY_LOCATION_LOOKUP');X.memberReads=(X.memberReads or 0)+1
  return {GetOwner=function()return 0 end,GetType=function()return kind end}
 end}end
end
function X.make(i)local c=N.first(i);return c end
function X.unchanged(c,saved,writes)
 assert(T.encode(T.record(c))==saved and T.writes()==writes,'UNATTRIBUTED_EVENT_WROTE_CITY_HISTORY')
end
function X.fire(kind,x,y,extra)GameEvents.OnDistrictConstructed.Fire(0,kind,x or 999,y or 998,extra)end
function X.report()return shared.CityProgressionStore.FailureReport()end
'''
def runtime():
 source=STORE_SOURCE or (ROOT/'Mod/CityProgressionStore.lua').read_text()
 digest=sha256(instrument_store(source).encode()).hexdigest()
 key=('historical/'+BASE if STORE_SOURCE else 'instrumented-current')+'/Mod/CityProgressionStore.lua'
 SOURCES[digest]=key;executed(key,digest,mode='instrumented_complete_module',profile='existing private storage/counter capture;no business replacement')
 with profile():v=fixture(source)
 v.execute(SETUP+EXTRA)
 lines=[];v.globals().print=lambda *xs:lines.append(' '.join(map(str,xs)))
 return v,lines

class NormalSource(unittest.TestCase):
 def test_normal_source_retains_full_proof_without_plot_or_hd_dependency(self):
  v,_=runtime();v.execute("Cities=nil;ExposedMembers={};Map.GetPlot=function()error('NORMAL_SOURCE_MUST_NOT_FALLBACK')end;local c=X.make(3);T.complete(c,'DISTRICT_CAMPUS');assert(T.record(c).base.specialization=='RESEARCH'and T.record(c).base.potential==1);assert(X.report()==nil)")
 def test_four_known_parameters_not_an_assumed_fifth_city_id(self):
  v,_=runtime();v.execute("local c=X.make(3);T.district(c,'DISTRICT_CAMPUS',930,true);X.fire('DISTRICT_CAMPUS',930,5,bCity:GetID());assert(T.record(c).base.specialization=='RESEARCH'and not T.record(bCity).completionError)")
 def test_numeric_district_type_index_is_resolved_through_catalogue(self):
  v,_=runtime();v.execute("local info=P.Info;P.Info=function(t,k)if t=='Districts'and k==17 then return {DistrictType='DISTRICT_CAMPUS',Index=17}end;return info(t,k)end;local c=X.make(3);T.district(c,17,930,true);X.fire(17,930,5);assert(T.record(c).base.specialization=='RESEARCH'and T.record(c).base.first.type=='DISTRICT_CAMPUS')")
 def test_confirmed_incomplete_is_not_completion_and_does_not_poison_first(self):
  v,_=runtime();v.execute("local c=X.make(3);local saved=T.encode(T.record(c));T.district(c,'DISTRICT_CAMPUS',930,false);X.fire('DISTRICT_CAMPUS',930,5);assert(T.encode(T.record(c))==saved and X.report()==nil);T.complete(c,'DISTRICT_THEATER');assert(T.record(c).base.specialization=='CULTURE')")
 def test_replacement_family_keeps_exact_native_id_and_first_order(self):
  v,_=runtime();v.execute("local rows=P.Rows;P.Rows=function(t)if t=='DistrictReplaces'then return {{CivUniqueDistrictType='DISTRICT_TEST',ReplacesDistrictType='DISTRICT_CAMPUS'}}end;return rows(t)end;local c=X.make(3);T.complete(c,'DISTRICT_TEST');local saved=T.encode(T.record(c));T.complete(c,'DISTRICT_THEATER');assert(T.record(c).base.specialization=='RESEARCH'and T.record(c).base.first.type=='DISTRICT_TEST'and T.encode(T.record(c))==saved)")
 def test_unrelated_family_never_reads_primary_or_plot_source(self):
  v,_=runtime();v.execute("CityManager.GetDistrictAt=function()error('UNRELATED_PRIMARY')end;Map.GetPlot=function()error('UNRELATED_PLOT')end;X.fire('DISTRICT_HOLY_SITE');N.unchanged();assert(X.report()==nil)")
 def test_warm_actual_store_callback_does_not_enumerate_native_cities(self):
  v,_=runtime();v.execute("local c=X.make(3);local get=Players[0].GetCities;Players[0].GetCities=function()error('EVENT_ENUMERATED_CITIES')end;T.complete(c,'DISTRICT_CAMPUS');Players[0].GetCities=get;assert(T.record(c).base.specialization=='RESEARCH'and X.report()==nil)")

class AttributionOnly(unittest.TestCase):
 def test_missing_district_with_plot_city_holds_only_that_city_no_grant(self):
  v,_=runtime();v.execute("local c=X.make(3);local other=X.make(4);local before=T.encode(T.record(other));X.associate(c,'DISTRICT_CAMPUS',999,998);X.fire('DISTRICT_CAMPUS');assert(T.record(c).completionError=='COMPLETION_EVIDENCE_UNAVAILABLE'and T.record(c).base.specialization=='NONE','CITY_ONLY_GUESSED_COMPLETION');assert(T.encode(T.record(other))==before,'PLOT_CITY_SCOPE_POISONED_OTHER_CITY');assert(X.plotReads==1 and X.cityReads==1 and X.report()==nil);T.complete(other,'DISTRICT_THEATER');assert(T.record(other).base.specialization=='CULTURE')")
 def test_throwing_primary_with_same_plot_city_stays_scoped(self):
  v,_=runtime();v.execute("local c=X.make(3);local other=X.make(4);local saved=T.encode(T.record(other));X.associate(c,'DISTRICT_CAMPUS',999,998);CityManager.GetDistrictAt=function()error('PRIMARY_UNAVAILABLE')end;X.fire('DISTRICT_CAMPUS');assert(T.record(c).completionError and not T.record(c).base.first);assert(T.encode(T.record(other))==saved and X.report()==nil)")
 def test_district_city_unready_does_not_imply_completion_from_plot(self):
  v,_=runtime();v.execute("local c=X.make(3);local other=X.make(4);local saved=T.encode(T.record(other));CityManager.GetDistrictAt=function()return {GetCity=function()return nil end,GetOwner=function()return 0 end,GetType=function()return 'DISTRICT_CAMPUS'end,IsComplete=function()return true end}end;X.associate(c,'DISTRICT_CAMPUS',999,998);X.fire('DISTRICT_CAMPUS');assert(T.record(c).completionError and T.record(c).base.specialization=='NONE');assert(T.encode(T.record(other))==saved and X.report()==nil)")
 def test_reliable_incomplete_object_excludes_missing_city_without_other_source(self):
  v,_=runtime();v.execute("local c=X.make(3);local saved=T.encode(T.record(c));local writes=T.writes();Cities=nil;Map.GetPlot=function()error('KNOWN_INCOMPLETE_MUST_NOT_ASSOCIATE')end;CityManager.GetDistrictAt=function()return {GetCity=function()return nil end,GetOwner=function()return 0 end,GetType=function()return 'DISTRICT_CAMPUS'end,IsComplete=function()return false end}end;X.fire('DISTRICT_CAMPUS');X.unchanged(c,saved,writes);assert(X.report()==nil)")
 def test_full_original_proof_is_still_required_after_source_becomes_readable(self):
  v,_=runtime();v.execute("local c=X.make(3);local d=T.district(c,'DISTRICT_CAMPUS',930,true);local get=CityManager.GetDistrictAt;local n=0;CityManager.GetDistrictAt=function(...)n=n+1;if n==1 then return nil end;return get(...)end;X.associate(c,'DISTRICT_CAMPUS',930,5);X.fire('DISTRICT_CAMPUS',930,5);assert(n==2 and T.record(c).base.specialization=='RESEARCH'and T.record(c).base.first.districtID==930 and X.report()==nil)")
 def test_disagreement_between_plot_and_full_proof_never_chooses_either_city(self):
  v,_=runtime();v.execute("local c=X.make(3);local other=X.make(4);T.district(other,'DISTRICT_CAMPUS',930,true);local get=CityManager.GetDistrictAt;local n=0;CityManager.GetDistrictAt=function(...)n=n+1;if n==1 then return nil end;return get(...)end;X.associate(c,'DISTRICT_CAMPUS',930,5);local a,b=T.encode(T.record(c)),T.encode(T.record(other));local writes=T.writes();X.fire('DISTRICT_CAMPUS',930,5);X.unchanged(c,a,writes);X.unchanged(other,b,writes);assert(X.report()and X.report():find('COMPLETION_SOURCE_DISAGREEMENT'))")
 def test_source_reference_failure_after_reliable_id_touches_only_matching_pending(self):
  v,_=runtime();v.execute("local c=N.pending(3);local other=N.pending(4);local getX=c.GetX;CityManager.GetDistrictAt=function()return {GetCity=function()return c end}end;c.GetX=function()error('COORDINATE_UNAVAILABLE')end;X.fire('DISTRICT_CAMPUS');c.GetX=getX;N.finish(other);assert(T.record(other)and not T.record(other).completionError);N.finish(c);assert(not T.record(c)and X.report()==nil)")
 def test_source_reference_failure_after_reliable_id_touches_only_matching_worker(self):
  v,_=runtime();v.execute("local c=X.make(3);local other=X.make(4);local saved=T.encode(T.record(other));local getX=c.GetX;CityManager.GetDistrictAt=function()return {GetCity=function()return c end}end;c.GetX=function()error('COORDINATE_UNAVAILABLE')end;X.fire('DISTRICT_CAMPUS');c.GetX=getX;assert(T.record(c).completionError=='COMPLETION_EVIDENCE_UNAVAILABLE');assert(T.encode(T.record(other))==saved,'KNOWN_ID_TOUCHED_OTHER_WRITER');assert(X.report()==nil)")
 def test_plot_owner_type_and_city_checks_do_not_accept_an_arbitrary_match(self):
  for field,value in [('plotOwner','3'),('plotType',"'DISTRICT_THEATER'"),('cityOwner','3')]:
   v,_=runtime();v.execute("local c=X.make(3);local saved=T.encode(T.record(c));local writes=T.writes();local plotOwner,plotType,cityOwner=0,'DISTRICT_CAMPUS',0;"+field+"="+value+";Map.GetPlot=function()return {GetOwner=function()return plotOwner end,GetDistrictType=function()return plotType end}end;Cities={GetPlotPurchaseCity=function()return {GetOwner=function()return cityOwner end,GetID=function()return c:GetID()end}end};X.fire('DISTRICT_CAMPUS');X.unchanged(c,saved,writes);assert(X.report())")
 def test_plot_city_without_district_membership_is_not_reliable_attribution(self):
  v,_=runtime();v.execute("local c=X.make(3);local saved=T.encode(T.props());local writes=T.writes();X.associate(c,'DISTRICT_CAMPUS',999,998);c.GetDistricts=function()return {GetDistrictAtLocation=function()return nil end}end;X.fire('DISTRICT_CAMPUS');assert(T.encode(T.props())==saved and T.writes()==writes and X.report(),'PLOT_HINT_USED_AS_MEMBERSHIP_PROOF')")
 def test_full_proof_source_disagreement_is_detected_before_other_getters(self):
  v,_=runtime();v.execute("local c=X.make(3);local other=X.make(4);T.district(other,'DISTRICT_CAMPUS',930,nil);local get=CityManager.GetDistrictAt;local n=0;CityManager.GetDistrictAt=function(...)n=n+1;if n==1 then return nil end;return get(...)end;X.associate(c,'DISTRICT_CAMPUS',930,5);local saved=T.encode(T.props());local writes=T.writes();X.fire('DISTRICT_CAMPUS',930,5);assert(T.encode(T.props())==saved and T.writes()==writes and X.report():find('COMPLETION_SOURCE_DISAGREEMENT'))")
 def test_unknown_completeness_is_not_silently_treated_as_false(self):
  v,_=runtime();v.execute("local c=X.make(3);local other=X.make(4);local saved=T.encode(T.record(other));T.district(c,'DISTRICT_CAMPUS',930,nil);X.fire('DISTRICT_CAMPUS',930,5);assert(T.record(c).completionError=='COMPLETION_EVIDENCE_UNAVAILABLE','UNKNOWN_COMPLETENESS_WAS_DISCARDED');assert(T.encode(T.record(other))==saved and X.report()==nil)")
 def test_known_city_metadata_failure_does_not_poison_another_first_city(self):
  v,_=runtime();v.execute("local c=X.make(3);local other=X.make(4);local saved=T.encode(T.record(other));T.district(c,'DISTRICT_CAMPUS',930,true);local info=P.Info;P.Info=function(t,k)if t=='Districts'then error('METADATA_NOT_READY')end;return info(t,k)end;X.fire('DISTRICT_CAMPUS',930,5);P.Info=info;assert(T.record(c).completionError);assert(T.encode(T.record(other))==saved and X.report()==nil)")

class ScopedFailureComposition(unittest.TestCase):
 def test_alternate_source_uses_one_city_location_lookup_never_city_enumeration(self):
  v,_=runtime();v.execute("local c=X.make(3);X.associate(c,'DISTRICT_CAMPUS',999,998);local cities=Players[0].GetCities;Players[0].GetCities=function()error('ASSOCIATION_ENUMERATED_CITIES')end;X.fire('DISTRICT_CAMPUS');Players[0].GetCities=cities;assert(T.record(c).completionError and X.memberReads==1 and not X.report())")
 def test_wrong_membership_owner_or_type_does_not_scope_to_purchase_city(self):
  for owner,kind in [('3',"'DISTRICT_CAMPUS'"),('0',"'DISTRICT_THEATER'")]:
   v,_=runtime();v.execute("local c=X.make(3);local saved=T.encode(T.props());local writes=T.writes();X.associate(c,'DISTRICT_CAMPUS',999,998);c.GetDistricts=function()return {GetDistrictAtLocation=function()return {GetOwner=function()return "+owner+" end,GetType=function()return "+kind+" end}end}end;X.fire('DISTRICT_CAMPUS');assert(T.encode(T.props())==saved and T.writes()==writes and X.report())")
 def test_failed_scoped_error_write_does_not_disable_another_city_or_replay(self):
  v,_=runtime();v.execute("local c=X.make(3);local other=X.make(4);local saved=T.encode(T.record(c));X.associate(c,'DISTRICT_CAMPUS',999,998);T.failKey(T.key(c));X.fire('DISTRICT_CAMPUS');assert(T.encode(T.record(c))==saved and not X.report());T.failKey(nil);T.complete(other,'DISTRICT_THEATER');assert(T.record(other).base.specialization=='CULTURE'and not T.record(other).completionError)")

class UnattributedBoundary(unittest.TestCase):
 def test_no_source_reports_without_writing_any_city_or_inventing_first(self):
  v,lines=runtime();v.execute("local c=X.make(3);local other=X.make(4);local saved=T.encode(T.props());local writes=T.writes();Cities=nil;X.fire('DISTRICT_CAMPUS');assert(T.encode(T.props())==saved and T.writes()==writes,'UNATTRIBUTED_EVENT_WROTE_CITY_HISTORY');assert(X.report()and X.report():find('首次专业确认暂停'));T.complete(c,'DISTRICT_THEATER');T.complete(other,'DISTRICT_CAMPUS');assert(T.encode(T.props())==saved and T.writes()==writes,'LATER_FIRST_INFERRED_AFTER_UNKNOWN_SOURCE');assert(shared.CityProgressionStore.ClaimState(0,aCity).eligible)")
  self.assertEqual(sum('scope=UNATTRIBUTED'in s for s in lines),1)
 def test_first_stop_does_not_disable_actual_ef_or_fixed_claim_completion(self):
  v,_=runtime();v.execute("local c=X.make(3);T.complete(c,'DISTRICT_CAMPUS');T.invest(c,9000);local control=T.encode(T.control(c));local saved=T.encode(T.record(c));Cities=nil;X.fire('DISTRICT_THEATER');assert(T.encode(T.control(c))==control and T.encode(T.record(c))==saved);Events.CityProjectCompleted.Fire(0,aCity:GetID(),101);N.flush();assert(T.record(aCity).base.specialization=='RESEARCH'and T.record(aCity).claim and T.encode(T.control(c))==control)")
 def test_duplicate_load_notice_does_not_resume_a_lost_first_stream(self):
  v,_=runtime();v.execute("local c=X.make(3);Cities=nil;X.fire('DISTRICT_CAMPUS');Events.LoadScreenClose.Fire();T.complete(c,'DISTRICT_THEATER');assert(T.record(c).base.specialization=='NONE'and not T.record(c).base.first and X.report())")
 def test_valid_earlier_buffer_can_commit_but_later_observation_is_not_invented(self):
  v,_=runtime();v.execute("local c=N.pending(3);local other=N.pending(4);T.district(c,'DISTRICT_THEATER',930,true);X.fire('DISTRICT_THEATER',930,5);Cities=nil;X.fire('DISTRICT_CAMPUS');T.district(other,'DISTRICT_CAMPUS',931,true);X.fire('DISTRICT_CAMPUS',931,5);N.finish(c);N.finish(other);assert(T.record(c).base.specialization=='CULTURE');assert(T.record(other).base.specialization=='NONE'and not T.record(other).base.first)")
 def test_diagnostics_can_fail_without_altering_safety_or_known_state(self):
  v,_=runtime();v.execute("local c=X.make(3);local saved=T.encode(T.props());local writes=T.writes();print=function()error('OBSERVER_REMOVED')end;Cities=nil;X.fire('DISTRICT_CAMPUS');T.complete(c,'DISTRICT_THEATER');assert(T.encode(T.props())==saved and T.writes()==writes and X.report());assert(shared.CityProgressionStore.ClaimState(0,aCity).eligible)")
 def test_fault_is_bounded_and_idle_or_duplicate_callbacks_do_not_retry(self):
  v,lines=runtime();v.execute("local c=X.make(3);local saved=T.encode(T.props());local writes=T.writes();CityManager.GetDistrictAt=function()X.primary=(X.primary or 0)+1;return nil end;Cities=nil;X.fire('DISTRICT_CAMPUS');for i=1,100 do X.fire('DISTRICT_CAMPUS')end;for i=1,1000 do Events.GameCoreEventPublishComplete.Fire()end;assert(X.primary==1 and T.encode(T.props())==saved and T.writes()==writes)")
  self.assertEqual(sum('scope=UNATTRIBUTED'in s for s in lines),1)
  measure('PU07_source_unattributed_guard',{'injected_fault_only':True,'city_writes':0,'source_attempts':1,'duplicate_events':100,'idle_publish':1000,'native_incidence_or_cold_recovery_claim':False})
 def test_post_fault_vm_reload_is_not_a_proven_recovery_or_a_new_saved_witness(self):
  v,_=runtime();v.execute("local c=X.make(3);local saved=T.encode(T.props());local writes=T.writes();Cities=nil;X.fire('DISTRICT_CAMPUS');assert(X.report());T.reload();assert(T.encode(T.props())==saved and T.writes()==writes);assert(shared.CityProgressionStore.FailureReport()==nil)")
  measure('PU07_source_post_fault_load_limit',{'status':'UNVERIFIED_NOT_RECOVERY_PASS','new_saved_witness':False,'error_is_session_local':True,'identity_choice_after_such_a_load_not_certified':True})

class RestrictedAndWork(unittest.TestCase):
 def test_restricted_lua_with_no_hd_runtime_namespace_retains_actual_path(self):
  v,_=runtime();v.execute("io=nil;os=nil;debug=nil;package=nil;require=nil;loadfile=nil;dofile=nil;ExposedMembers={};local c=X.make(3);T.complete(c,'DISTRICT_CAMPUS');assert(T.record(c).base.specialization=='RESEARCH')")
 def test_scoped_error_printing_is_bounded_not_a_new_recovery_journal(self):
  v,lines=runtime();v.execute("for i=3,14 do local c=N.pending(i);X.associate(c,'DISTRICT_CAMPUS',999,998);CityManager.GetDistrictAt=function()return nil end;X.fire('DISTRICT_CAMPUS')end;assert(not X.report())")
  self.assertLessEqual(len(lines),8)
 def test_normal_shape_and_writes_match_fixed_source_with_no_failed_native_reads(self):
  global STORE_SOURCE
  fixed=subprocess.check_output(['git','show',BASE+':Mod/CityProgressionStore.lua'],cwd=ROOT,text=True);original=STORE_SOURCE
  try:
   for n in (8,20,40):
    result=[]
    for source in (fixed,None):
     STORE_SOURCE=source;v,_=runtime();v.globals().n=n
     v.execute("for i=1,n do local c=X.make(i+2);T.complete(c,i%2==0 and 'DISTRICT_CAMPUS'or'DISTRICT_THEATER');T.invest(c,40000+i)end;normal=T.encode(T.props());count=T.writes();T.reload();assert(T.encode(T.props())==normal and T.writes()==count)")
     result.append((v.eval('normal'),v.eval('count')))
    self.assertEqual(result[0],result[1])
  finally:STORE_SOURCE=original
  measure('PU07_source_healthy_fixed_comparison',{'baseline':BASE,'city_counts':[8,20,40],'same_saved_shape_values_writes':True,'new_saved_fields':0,'native_claim':False})

class NormalReadWork(unittest.TestCase):
 def test_ordinary_complete_source_reads_match_fixed_source_and_need_no_association(self):
  global STORE_SOURCE
  fixed=subprocess.check_output(['git','show',BASE+':Mod/CityProgressionStore.lua'],cwd=ROOT,text=True);original=STORE_SOURCE;rows=[]
  try:
   for source in (fixed,None):
    STORE_SOURCE=source;v,_=runtime();v.execute("local c=X.make(3);calls={};local function wrap(o,m)local f=o[m];o[m]=function(...)calls[m]=(calls[m]or 0)+1;return f(...)end end;for _,m in ipairs({'GetOwner','GetID','GetX','GetY','GetProperty'})do wrap(c,m)end;local read=CityManager.GetDistrictAt;CityManager.GetDistrictAt=function(...)calls.GetDistrictAt=(calls.GetDistrictAt or 0)+1;local d=read(...);if d and not d.counted then d.counted=true;for _,m in ipairs({'GetCity','GetOwner','GetID','GetType','IsComplete'})do wrap(d,m)end end;return d end;Map.GetPlot=function()error('NORMAL_ASSOCIATION_ADDED')end;T.complete(c,'DISTRICT_CAMPUS');assert(T.record(c).base.specialization=='RESEARCH')")
    rows.append({k:int(n)for k,n in v.globals().calls.items()})
  finally:STORE_SOURCE=original
  self.assertEqual(sum(rows[0].values()),sum(rows[1].values()))
  delta={k:rows[1].get(k,0)-rows[0].get(k,0)for k in set(rows[0])|set(rows[1])if rows[1].get(k,0)!=rows[0].get(k,0)}
  self.assertEqual(delta,{'GetID':1,'GetOwner':-1})
  self.assertEqual(rows[1]['GetDistrictAt'],2);self.assertEqual(rows[1]['GetCity'],2)
  measure('PU07_source_normal_native_double_reads',{'baseline':BASE,'before':rows[0],'after':rows[1],'same_complete_read_total':True,'delta':delta,'reason':'early cityID scopes pre-coordinate failure;full proof reuses its owner read','native_CPU_or_availability_claim':False})

if __name__=='__main__':unittest.main()
