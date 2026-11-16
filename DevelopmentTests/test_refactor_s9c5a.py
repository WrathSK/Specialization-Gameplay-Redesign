"""Fixed independent UNIT_TARGETS projection and one-pass Gameplay publication."""
import json,unittest
from refactor_harness import Context,ROOT,measure,legacy_source_observation
from test_refactor_s9c2 import request
from test_refactor_s6i import investment,crew_site


def fixture():
 c=Context();c.load('PlayerActionReplies');c.execute("""
 d=SPCPlayerActionReplies.New(1,'TEST','UNIT_TARGETS')
 function packet(t)return {ReplyChannel='UNIT_TARGETS',ReplyEpoch=1,Action='UNIT_TARGETS_READ',UnitID=10,Token=t or 'T'}end
 function targets(t)return {version='TEST',owner=0,unitID=10,token=t or 'T',turn=1,x=2,y=3,mode='INVEST',plots={{plot=9,cityID=3,cityName='NAME'},{plot=12}},unknown={{cityID=2,reason='READ_UNKNOWN'}}}end
 """);return c

class Projection(unittest.TestCase):
 def test_fixed_projection_is_detached_and_carries_no_city_or_native_objects(self):
  c=fixture();c.execute("local s=targets();s.native={};s.plots[1].city={};s.unknown[1].object={};assert(d.PublishTargets(0,packet(),s));s.plots[1].plot=0;s.unknown[1].reason='OTHER';local r=d.Take(0,'T');assert(r.action=='UNIT_TARGETS_READ'and r.targets.plots[1].plot==9 and r.targets.unknown[1].reason=='READ_UNKNOWN'and r.targets.plots[1].cityID==nil and r.targets.plots[1].cityName==nil and r.targets.plots[1].city==nil and r.targets.native==nil and r.targets.unknown[1].object==nil)")
 def test_pre_stamp_error_preserves_unknown_and_no_synthetic_coordinates(self):
  c=fixture();c.execute("local s=targets();s.turn=nil;s.x=nil;s.y=nil;s.mode=nil;s.error='UNIT_MISSING';s.plots={};assert(d.PublishTargets(0,packet(),s));local r=d.Take(0,'T').targets;assert(r.error=='UNIT_MISSING'and r.turn==nil and r.mode==nil and #r.unknown==1)")
 def test_bad_stamp_protocol_types_or_mode_reject_without_evicting_valid_entry(self):
  for mutation in ("s.owner=1","s.token='WRONG'",'s.unitID=11',"s.version='OLD'",'s.x=0/0','s.turn=math.huge','s.y={}','s.mode=nil','s=setmetatable(s,{})'):
   c=fixture();c.execute("assert(d.PublishTargets(0,packet('KEEP'),targets('KEEP')));local s=targets();"+mutation+";assert(not d.PublishTargets(0,packet(),s)and d.Count()==1 and d.Has(0,'KEEP'))")
 def test_bad_dense_rows_and_nonfinite_or_object_fields_are_not_serialized(self):
  for mutation in ('s.plots[4]={plot=19}',"s.plots.extra={plot=19}",'s.plots=setmetatable(s.plots,{})','s.plots[1]=setmetatable(s.plots[1],{})','s.plots[1].plot=-1','s.unknown[1].cityID=math.huge','s.unknown[1].reason={}',"s.unknown[1].reason=string.rep('X',20001)",'s.unknown=nil'):
   c=fixture();c.execute('local s=targets();'+mutation+';assert(not d.PublishTargets(0,packet(),s)and d.Count()==0)')
 def test_row_and_accumulated_text_limits_return_explicit_failure_never_partial_map(self):
  for body in ("for i=1,4097 do s.plots[i]={plot=i}end;s.unknown={}","s.plots={};for i=1,14 do s.unknown[i]={cityID=i,reason=string.rep('X',20000)}end", "s.plots={};for i=1,4096 do s.plots[i]={plot=i}end"):
   c=fixture();c.execute("local s=targets();"+body+";assert(not d.PublishTargets(0,packet(),s)and d.Count()==0);assert(d.FailTargets(0,packet()));local r=d.Take(0,'T');assert(r.error=='TARGETS_UNAVAILABLE'and r.targets==nil)")
  c=fixture();c.execute("local s=targets();s.unknown={};for i=1,4096 do s.plots[i]={plot=i}end;assert(d.PublishTargets(0,packet(),s)and #d.Take(0,'T').targets.plots==4096)")
 def test_fixed_scope_capacity_lifecycle_and_cross_port_same_token_are_independent(self):
  c=fixture();c.execute("P={VERSION='TEST'};local a=SPCPlayerActionReplies.Start(P,shared);local t=a.Targets;local p=packet('SAME');local ap={ReplyChannel='UNIT_ACTION',ReplyEpoch=1,Action='UNIT_ACTION_CONFIRM',UnitID=10,Token='SAME'};local vp={ReplyChannel='UNIT_VIEW',ReplyEpoch=1,Action='UNIT_ACTION_VIEW',UnitID=10,Token='SAME'};assert(a.Publish(0,ap,'DONE')and a.Views.FailView(0,vp));for i=1,100 do local p=packet('T'..i);assert(t.PublishTargets(0,p,targets(p.Token)))end;assert(t.Count()==8 and a.Count()==1 and a.Views.Count()==1 and not t.Has(0,'T1'));assert(t.FailTargets(0,p));assert(a.Take(0,'SAME').text=='DONE'and a.Views.Take(0,'SAME').error=='VIEW_UNAVAILABLE'and t.Take(0,'SAME').error=='TARGETS_UNAVAILABLE');assert(not t.Publish(0,p,'X')and not t.PublishView(0,p,{}));assert(not a.PublishTargets(0,ap,targets()));local old=t;local b=SPCPlayerActionReplies.Start(P,shared);assert(b.epoch==2 and old.Count()==0 and not old.FailTargets(0,p));b.Shutdown();assert(b.Count()==0 and b.Views.Count()==0 and b.Targets.Count()==0)")
  measure('S9c5a_fixed_target_transport',{'ports':3,'slots_per_port':8,'total_max_slots':24,'rows_per_target_reply':4096,'text_budget_per_target_reply':262144,'transport_limit_is_not_scan_limit':True,'extra_native_reads':0,'UI_migrated':False})

class Producer(unittest.TestCase):
 def setup(self):
  c=request();c.execute("reads=0;shared.UnitTargets={Refresh=function(pid,p)reads=reads+1;if onRead then onRead()end;local s={owner=pid,unitID=p.UnitID,token=p.Token,version=P.VERSION,turn=1,x=2,y=3,mode='BUILD',plots={{plot=9}},unknown={}};shared.UnitTargetSnapshot=s;return s end};function tp(t)return {ReplyChannel='UNIT_TARGETS',ReplyEpoch=d.epoch,Action='UNIT_TARGETS_READ',UnitID=10,Token=t or 'T'}end");return c
 def test_request_collects_once_preserves_global_and_legacy_never_enters_typed_port(self):
  c=self.setup();c.execute("runRequest(0,tp());assert(reads==1 and shared.UnitTargetSnapshot.token=='T'and d.Targets.Take(0,'T').targets.plots[1].plot==9);runRequest(0,{Action='UNIT_TARGETS_READ',UnitID=10,Token='DEV'});assert(reads==2 and shared.UnitTargetSnapshot.token=='DEV'and d.Targets.Count()==0)")
 def test_wrong_epoch_channel_or_missing_service_never_calls_original_reader(self):
  for mutation in ('p.ReplyEpoch=99',"p.ReplyChannel='UNIT_VIEW'",'shared.PlayerActionReplies=nil'):
   c=self.setup();c.execute('local p=tp();'+mutation+';runRequest(0,p);assert(reads==0)')
 def test_service_replacement_during_collect_cannot_publish_to_the_successor(self):
  c=self.setup();c.execute("local old=d;onRead=function()onRead=nil;SPCPlayerActionReplies.Start(P,shared)end;runRequest(0,tp());assert(reads==1 and old.Targets.Count()==0 and shared.PlayerActionReplies.Targets.Count()==0 and shared.ObserverErrors['unit-target-reply'])")
 def test_projection_failure_sends_one_explicit_negative_without_collect_replay(self):
  c=self.setup();c.execute("d.Targets.PublishTargets=function()error('TRANSPORT_FAILED')end;runRequest(0,tp());local r=d.Targets.Take(0,'T');assert(reads==1 and r.error=='TARGETS_UNAVAILABLE'and r.targets==nil and shared.UnitTargetSnapshot.token=='T'and shared.ObserverErrors['unit-target-reply'])")

class ActualTargets(unittest.TestCase):
 def test_actual_refresh_returns_exact_published_DTO_and_projection_adds_zero_native_work(self):
  l=investment(32)
  with legacy_source_observation():l.globals().include('PlayerActionReplies')
  l.execute("local d=SPCPlayerActionReplies.New(1,P.VERSION,'UNIT_TARGETS');local u=addSiteUnit(940);u.x=199;local p={ReplyChannel='UNIT_TARGETS',ReplyEpoch=d.epoch,Action='UNIT_TARGETS_READ',UnitID=940,Token='ALL'};local s=shared.UnitTargets.Refresh(0,p);assert(rawequal(s,shared.UnitTargetSnapshot)and #s.plots==32 and siteWork.ownerDistricts==1 and siteWork.ownerCities==1);local before=T.encode(siteWork);assert(d.PublishTargets(0,p,s));local r=d.Take(0,'ALL').targets;assert(#r.plots==32 and T.encode(siteWork)==before);for i,row in ipairs(r.plots)do assert(row.plot==s.plots[i].plot and row.cityName==nil)end")
  measure('S9c5a_actual_marker_scope',{'cities':32,'original_owner_district_enumerations':1,'original_owner_city_enumerations':1,'targets':32,'projection_extra_native_work':0})
 def test_internal_ReadAtSite_and_snapshot_save_restore_are_unchanged(self):
  l=investment();l.execute("forbidOwner=true;local u,t=makePreview(941);assert(shared.UnitActionPreview and shared.UnitTargetSnapshot.token=='MARKER_KEEP');local v=shared.UnitActions.ReadView(0,941,'V');assert(v.prepared and shared.UnitTargetSnapshot.token=='MARKER_KEEP'and siteWork.ownerCities==0)")
  l=crew_site();l.execute("forbidOwner=true;local s=shared.UnitTargets.ReadAtSite(0,{UnitID=20001,Token='LOCAL'});assert(#s.plots==1 and siteWork.ownerCities==0 and shared.UnitTargetSnapshot.token=='MARKER_KEEP')")


def load_tests(loader,standard,pattern):
 selection=json.loads((ROOT/'DevelopmentTests/refactor_selection.json').read_text())
 return unittest.TestSuite([standard,unittest.TestSuite(loader.loadTestsFromName(name)for name in selection['stages']['S9c4b'])])

if __name__=='__main__':unittest.main()
