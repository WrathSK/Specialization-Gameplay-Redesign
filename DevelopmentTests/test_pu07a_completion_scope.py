"""PU07a source/family/fixed-Claim scope, not complete unattributed-first repair.
Actual Store/Claim Lua with explicit native doubles. Private writer/storage
instrumentation is test-only; frozen fixtures/assertions are not rewritten.
"""
from hashlib import sha256
import subprocess,unittest
from refactor_harness import ROOT,SOURCES,executed,measure
from test_refactor_s7d5 import profile
from test_store_write_boundaries import fixture,instrument_store
BASE='969a5faa4dd79d52f486349b0b8bbed14eb387aa'
STORE_SOURCE=None  # Exact fixed Git source may be injected only by a before-run.
SETUP=r'''

T.start()
local info=P.Info;local projects,buildings={},{}
for i,k in ipairs({'RESEARCH','CULTURE','INDUSTRY','COMMERCE'})do
 local p={ProjectType='PROJECT_SPC_CLAIM_'..k,Index=100+i,Hash=100+i}
 projects[p.ProjectType]=p;projects[p.Index]=p
 local n='BUILDING_SPC_CLAIM_'..k;buildings[n]={BuildingType=n,Index=200+i,InternalOnly=true}
end
P.Info=function(t,k)if t=='Projects'then return projects[k]elseif t=='Buildings'then return buildings[k]end;return info(t,k)end
P.Call=function(o,k,...)if not o or type(o[k])~='function'then return false end;return pcall(o[k],o,...)end
P.HasBuilding=function(b,id)return b[id]==true end
P.CreateBuilding=function(q,id)q.buildings[id]=true end
P.RemoveBuilding=function(b,id)b[id]=nil end
GameInfo.Projects=projects
N={}
local function make(i)
 local c=T.ai(T.fresh(i));local q={target='NONE',size=0,buildings={}};c.q=q
 c.GetBuildings=function()return q.buildings end;c.GetBuildQueue=function()return q end
 q.CurrentlyBuilding=function()return q.target end;q.GetSize=function()return q.size end
 q.GetCurrentProductionTypeHash=function()return 0 end
 T.district(c,'DISTRICT_CAMPUS',200+i,true);T.take(c)
 return c
end
aCity=make(1);bCity=make(2)
include('ClaimProjects');SPCClaimProjects.Start(P,shared);Events.LoadScreenClose.Fire()
assert(aCity.q.buildings[201]and bCity.q.buildings[201],'INITIAL_MARKERS_REQUIRED')
assert(shared.CityProgressionStore.ClaimState(0,aCity).eligible)
assert(shared.CityProgressionStore.ClaimState(0,bCity).eligible)
function summary()
 return T.encode({a=T.record(aCity),b=T.record(bCity),aMarker=aCity.q.buildings[201],bMarker=bCity.q.buildings[201]})
end
before=summary();beforeWrites=T.writes();assert(not T.record(aCity).completionError and not T.record(bCity).completionError)

function N.unchanged()
 assert(summary()==before and T.writes()==beforeWrites,'UNRELATED_EVENT_POISONED_FIXED_CANDIDATES')
 assert(shared.CityProgressionStore.ClaimState(0,aCity).eligible and shared.CityProgressionStore.ClaimState(0,bCity).eligible)
end
function N.flush()
 Events.CityProductionUpdated.Fire(0,aCity:GetID());Events.CityProductionUpdated.Fire(0,bCity:GetID());Events.GameCoreEventPublishComplete.Fire()
end
function N.first(i)local c=T.fresh(i);T.register(c);assert(T.record(c).progression=='UNASSIGNED');return c end
function N.pending(i)
 local c=T.fresh(i);GameEvents.CityBuilt.Fire(0,c:GetID(),c:GetX(),c:GetY());Events.CityInitialized.Fire(0,c:GetID(),c:GetX(),c:GetY());return c
end
function N.finish(c)Events.UnitActivate.Fire(0,c:GetID()+1000,c:GetX(),c:GetY(),EventSubTypes.FOUND_CITY,false)end

'''

def claims(capture=False):
 source=STORE_SOURCE or (ROOT/'Mod/CityProgressionStore.lua').read_text()
 if capture:
  marker='local w=CreateProgressionRecord(P,shared,storage)'
  assert source.count(marker)==1
  source=source.replace(marker,marker+';__pu07_writers[token]=w')
 digest=sha256(instrument_store(source).encode()).hexdigest()
 key=('historical/'+BASE if STORE_SOURCE else 'instrumented-current')+'/Mod/CityProgressionStore.lua'+('/writer_capture'if capture else '')
 SOURCES[digest]=key;executed(key,digest,mode='instrumented_complete_module',profile='private storage/counter; optional private writer capture, no runtime API')
 with profile():v=fixture(source)
 v.execute('__pu07_writers={}')
 v.execute(SETUP);return v

class FixedCandidates(unittest.TestCase):
 def test_unrelated_missing_district_does_not_read_native_or_poison_claims(self):
  v=claims();v.execute("reads=0;CityManager.GetDistrictAt=function()reads=reads+1;error('SHOULD_NOT_READ_UNRELATED')end;GameEvents.OnDistrictConstructed.Fire(0,'DISTRICT_HOLY_SITE',999,998);N.flush();N.unchanged();assert(reads==0,'UNRELATED_NATIVE_READ')")
 def test_qualifying_missing_target_never_invalidates_fixed_claim_set(self):
  v=claims();v.execute("GameEvents.OnDistrictConstructed.Fire(0,'DISTRICT_CAMPUS',999,998);N.flush();N.unchanged()")
 def test_replacement_is_filtered_by_actual_family_not_its_name(self):
  v=claims();v.execute("local rows=P.Rows;P.Rows=function(t)if t=='DistrictReplaces'then return {{CivUniqueDistrictType='DISTRICT_TEST',ReplacesDistrictType='DISTRICT_CAMPUS'}}end;return rows(t)end;local c=N.first(3);GameEvents.OnDistrictConstructed.Fire(0,'DISTRICT_TEST',999,998);assert(T.record(c).completionError=='COMPLETION_CITY_UNAVAILABLE');N.flush();assert(shared.CityProgressionStore.ClaimState(0,aCity).eligible and aCity.q.buildings[201])")
 def test_nil_throw_and_missing_city_preserve_fixed_candidates(self):
  for code in ("return nil","error('DISTRICT_READ_FAILED')","return {GetCity=function()error('CITY_READ_FAILED')end}","return {GetCity=function()return nil end}"):
   v=claims();v.execute("CityManager.GetDistrictAt=function()"+code+" end;GameEvents.OnDistrictConstructed.Fire(0,'DISTRICT_CAMPUS',999,998);N.flush();N.unchanged()")
 def test_known_target_evidence_error_cannot_invalidate_fixed_candidates(self):
  v=claims();v.execute("CityManager.GetDistrictAt=function()return {GetCity=function()return aCity end,GetOwner=function()return 0 end,GetType=function()error('TYPE_FAILED')end}end;GameEvents.OnDistrictConstructed.Fire(0,'DISTRICT_CAMPUS',999,998);N.flush();N.unchanged()")
 def test_foreign_event_and_foreign_target_do_not_write_owned_candidates(self):
  v=claims();v.execute("GameEvents.OnDistrictConstructed.Fire(3,'DISTRICT_CAMPUS',999,998);local c=T.fresh(4,3);CityManager.GetDistrictAt=function()return {GetCity=function()return c end}end;GameEvents.OnDistrictConstructed.Fire(0,'DISTRICT_CAMPUS',999,998);N.flush();N.unchanged()")
 def test_unreadable_metadata_does_not_reclassify_it_as_unrelated(self):
  v=claims();v.execute("local c=N.pending(3);local info=P.Info;P.Info=function(t,k)if t=='Districts'then error('METADATA_UNAVAILABLE')end;return info(t,k)end;GameEvents.OnDistrictConstructed.Fire(0,'DISTRICT_TEST',999,998);P.Info=info;N.finish(c);assert(T.record(c)==nil,'UNKNOWN_METADATA_ADMITTED_AS_EMPTY');N.flush();N.unchanged()")
 def test_unknown_family_and_missing_target_keep_first_history_unsafe(self):
  v=claims();v.execute("local c=N.first(3);local info=P.Info;P.Info=function(t,k)if t=='Districts'then error('METADATA_UNAVAILABLE')end;return info(t,k)end;GameEvents.OnDistrictConstructed.Fire(0,'DISTRICT_TEST',999,998);P.Info=info;assert(T.record(c).completionError=='COMPLETION_CITY_UNAVAILABLE');assert(shared.CityProgressionStore.ClaimState(0,aCity).eligible)")
 def test_future_family_is_irrelevant_without_target_lookup(self):
  v=claims();v.execute("P.Families.DISTRICT_FUTURE='MILITARY';CityManager.GetDistrictAt=function()error('IRRELEVANT_READ')end;GameEvents.OnDistrictConstructed.Fire(0,'DISTRICT_FUTURE',999,998);N.flush();N.unchanged()")

class FirstHistory(unittest.TestCase):
 def test_actual_order_first_completion_and_duplicate_stay_exact(self):
  v=claims();v.execute("local c=N.first(3);T.complete(c,'DISTRICT_THEATER');local saved=T.encode(T.record(c));local writes=T.writes();assert(T.record(c).base.specialization=='CULTURE'and T.record(c).base.first.type=='DISTRICT_THEATER');T.complete(c,'DISTRICT_CAMPUS');T.complete(c,'DISTRICT_THEATER');assert(T.encode(T.record(c))==saved and T.writes()==writes)")
 def test_known_target_failure_holds_only_that_first_history(self):
  v=claims();v.execute("local c=N.first(3);local other=N.first(4);local saved=T.encode(T.record(other));CityManager.GetDistrictAt=function()return {GetCity=function()return c end,GetOwner=function()return 0 end,GetType=function()error('TARGET_TYPE_FAILED')end}end;GameEvents.OnDistrictConstructed.Fire(0,'DISTRICT_CAMPUS',999,998);assert(T.record(c).completionError=='COMPLETION_EVIDENCE_UNAVAILABLE');assert(T.encode(T.record(other))==saved);assert(shared.CityProgressionStore.ClaimState(0,aCity).eligible)")
 def test_unknown_qualified_source_first_guard_is_explicit_remaining_gap(self):
  v=claims();v.execute("local c=N.first(3);local other=N.first(4);GameEvents.OnDistrictConstructed.Fire(0,'DISTRICT_CAMPUS',999,998);assert(T.record(c).completionError=='COMPLETION_CITY_UNAVAILABLE'and T.record(other).completionError=='COMPLETION_CITY_UNAVAILABLE');local raw=T.encode(T.record(c));T.complete(c,'DISTRICT_THEATER');assert(T.encode(T.record(c))==raw);assert(shared.CityProgressionStore.ClaimState(0,aCity).eligible)")
  measure('PU07a_unattributed_first_limit',{'status':'OPEN_NOT_REPAIRED','existing_first_history_holds':2,'fixed_claim_candidates_poisoned':0,'no_native_frequency_or_recovery_claim':True})
 def test_non_v01_missing_source_does_not_hold_unassigned_first_city(self):
  v=claims();v.execute("local c=N.first(3);local saved=T.encode(T.record(c));GameEvents.OnDistrictConstructed.Fire(0,'DISTRICT_HOLY_SITE',999,998);assert(T.encode(T.record(c))==saved);T.complete(c,'DISTRICT_CAMPUS');assert(T.record(c).base.specialization=='RESEARCH')")
 def test_early_delivered_completion_is_replayed_in_order_once(self):
  v=claims();v.execute("local c=N.pending(3);T.district(c,'DISTRICT_THEATER',930,true);GameEvents.OnDistrictConstructed.Fire(0,'DISTRICT_THEATER',930,5);T.district(c,'DISTRICT_CAMPUS',931,true);GameEvents.OnDistrictConstructed.Fire(0,'DISTRICT_CAMPUS',931,5);N.finish(c);assert(T.record(c).base.specialization=='CULTURE'and T.record(c).base.first.type=='DISTRICT_THEATER');local saved=T.encode(T.record(c));T.complete(c,'DISTRICT_CAMPUS');assert(T.encode(T.record(c))==saved)")
 def test_known_target_pending_throw_cannot_poison_other_pending_source(self):
  v=claims();v.execute("local c=N.pending(3);local other=N.pending(4);CityManager.GetDistrictAt=function()return {GetCity=function()return c end,GetOwner=function()return 0 end,GetType=function()error('KNOWN_TARGET_FAILED')end}end;GameEvents.OnDistrictConstructed.Fire(0,'DISTRICT_CAMPUS',999,998);N.finish(other);assert(T.record(other)and not T.record(other).completionError);N.finish(c);assert(not T.record(c))")
 def test_known_city_id_contains_an_early_coordinate_getter_failure(self):
  v=claims();v.execute("local c=N.pending(3);local other=N.pending(4);local getX=c.GetX;CityManager.GetDistrictAt=function()return {GetCity=function()return c end}end;c.GetX=function()error('COORDINATE_FAILED')end;GameEvents.OnDistrictConstructed.Fire(0,'DISTRICT_CAMPUS',999,998);c.GetX=getX;N.finish(other);assert(T.record(other)and not T.record(other).completionError,'OTHER_PENDING_POISONED');N.finish(c);assert(not T.record(c),'MISSED_FIRST_ADMITTED_AS_EMPTY')")
 def test_error_text_failure_stays_inside_source_callback(self):
  v=claims();v.execute("local c=N.pending(3);local other=N.pending(4);CityManager.GetDistrictAt=function()return {GetCity=function()return c end,GetOwner=function()return 0 end,GetType=function()error(setmetatable({},{__tostring=function()error('BAD_ERROR_TEXT')end}))end}end;GameEvents.OnDistrictConstructed.Fire(0,'DISTRICT_CAMPUS',999,998);N.finish(other);assert(T.record(other)and not T.record(other).completionError);N.finish(c);assert(not T.record(c))")

class PersistedGuards(unittest.TestCase):
 def test_generic_incomplete_admission_hold_stays_strict_for_fixed_claim(self):
  v=claims(True);v.execute("local w=assert(__pu07_writers[aCity.s.values.TOKEN]);w.HoldCompletion('FOUNDATION_ADMISSION_INCOMPLETE');assert(T.record(aCity).completionError=='FOUNDATION_ADMISSION_INCOMPLETE');assert(not pcall(shared.CityProgressionStore.ClaimState,0,aCity));assert(shared.CityProgressionStore.ClaimState(0,bCity).eligible)")
 def test_old_persisted_completion_error_is_not_cleared_or_guessed_away(self):
  v=claims();v.execute("local n=M.Copy(T.record(aCity));n.completionError='COMPLETION_CITY_UNAVAILABLE';T.propsSet(T.key(aCity),n);T.reload();assert(T.record(aCity).completionError=='COMPLETION_CITY_UNAVAILABLE');local saved=T.encode(T.record(aCity));T.complete(aCity,'DISTRICT_THEATER');assert(T.encode(T.record(aCity))==saved and not pcall(shared.CityProgressionStore.ClaimState,0,aCity))")
 def test_duplicate_missing_events_do_not_write_fixed_claims_and_idle_is_zero(self):
  v=claims();v.execute("for i=1,100 do GameEvents.OnDistrictConstructed.Fire(0,'DISTRICT_CAMPUS',999,998)end;for i=1,1000 do Events.GameCoreEventPublishComplete.Fire()end;N.unchanged()")
 def test_construction_owner_guard_does_not_touch_other_source_owner(self):
  v=claims(True);v.execute("local c=N.first(3);local w=assert(__pu07_writers[c.s.values.TOKEN]);local saved=T.encode(T.record(c));w.HoldCompletion('COMPLETION_CITY_UNAVAILABLE',3);assert(T.encode(T.record(c))==saved);w.HoldCompletion('COMPLETION_CITY_UNAVAILABLE',0);assert(T.record(c).completionError=='COMPLETION_CITY_UNAVAILABLE')")


class RestrictedAndLoad(unittest.TestCase):
 def test_restricted_lua_and_missing_optional_observers_keep_owned_paths(self):
  v=claims();v.execute("io=nil;os=nil;debug=nil;package=nil;require=nil;loadfile=nil;dofile=nil;SPCCultureDiagnostics=nil;GameEvents.OnDistrictConstructed.Fire(0,'DISTRICT_CAMPUS',999,998);N.flush();N.unchanged();local c=N.first(3);T.complete(c,'DISTRICT_CAMPUS');assert(T.record(c).base.specialization=='RESEARCH')")
 def test_fixed_candidate_set_survives_callback_then_store_reload_without_writes(self):
  v=claims();v.execute("GameEvents.OnDistrictConstructed.Fire(0,'DISTRICT_CAMPUS',999,998);N.flush();N.unchanged();local saved=T.encode(T.props());local writes=T.writes();T.reload();assert(T.encode(T.props())==saved and T.writes()==writes);assert(shared.CityProgressionStore.ClaimState(0,aCity).eligible and shared.CityProgressionStore.ClaimState(0,bCity).eligible)")

class HealthyDifferential(unittest.TestCase):
 def test_normal_first_history_claims_investment_and_cold_bytes_match_fixed_source(self):
  global STORE_SOURCE
  fixed=subprocess.check_output(['git','show',BASE+':Mod/CityProgressionStore.lua'],cwd=ROOT,text=True)
  original=STORE_SOURCE;rows=[]
  try:
   for count in (8,20,40):
    pair=[]
    for source in (fixed,None):
     STORE_SOURCE=source;v=claims();v.globals().count=count
     v.execute("for i=1,count do local c=N.first(i+2);T.complete(c,i%2==0 and 'DISTRICT_CAMPUS'or'DISTRICT_THEATER');T.invest(c,50000+i);assert(T.control(c).potential==2)end;normal=T.encode(T.props());normalWrites=T.writes();local writes=T.writes();T.reload();assert(T.encode(T.props())==normal and T.writes()==writes)")
     pair.append((v.eval('normal'),v.eval('normalWrites')))
    self.assertEqual(pair[0],pair[1]);rows.append(count)
  finally:STORE_SOURCE=original
  measure('PU07a_healthy_fixed_source',{'baseline':BASE,'fresh_cities_per_run':rows,'same_saved_values_and_write_count':True,'load_writes':0,'native_game_claim':False})

if __name__=='__main__':unittest.main()
