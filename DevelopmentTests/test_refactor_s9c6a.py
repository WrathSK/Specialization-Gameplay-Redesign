"""Fixed institution presentation projection; existing metrics unchanged."""
import json,unittest
from refactor_harness import Context,ROOT,measure
from test_refactor_s9c2 import request
from test_refactor_s6h import ActualProfile
import test_b251_institutions as original


def fixture():
 c=Context();c.load('PlayerActionReplies');c.execute("""
 d=SPCPlayerActionReplies.New(1,'TEST','CITY_PRESENTATION')
 function packet(t)return {ReplyChannel='CITY_PRESENTATION',ReplyEpoch=1,Action='CITY_PRESENTATION_READ',CityID=3,Token=t or 'REQUEST'}end
 function value(t)return {owner=0,cityID=3,token=t or 'REQUEST',specialization='RESEARCH',potential=4,progression='SPECIALIZED',active=4,activeStatus='KNOWN',investments=3,x=2,y=3,
 institutionArchive={RESEARCH=4,CULTURE=2,COMMERCE=1,INDUSTRY=3},institutionSummary={known=true,token='STORE_IDENTITY',reference={owner=0,cityID=3,x=2,y=3},revision=19,
 reputationKnown=true,traditionKnown=true,dialogueKnown=true,engineeringKnown=true,insightsKnown=true,templatesKnown=true,
 tradition={age=15,state='COUNTING',cursor=4,percent=10,nextAge=20},reputation={age=40,state='PAUSED'},dialogue=1001,engineering=500,insights=192,buildingTemplates=5000,districtTemplates=0}}end
 """);return c

class Projection(unittest.TestCase):
 def test_complete_fixed_projection_preserves_distinct_tokens_and_detaches_every_table(self):
  c=fixture();c.execute("local s=value();s.native={};s.institutionSummary.receipt={};s.institutionSummary.reference.city={};s.institutionSummary.tradition.native={};assert(d.PublishPresentation(0,packet(),s));s.institutionArchive.RESEARCH=0;s.institutionSummary.tradition.age=0;s.institutionSummary.reference.x=99;s.institutionSummary.reputation.state='OTHER';local r=d.Take(0,'REQUEST');local v=r.presentation;assert(r.cityID==3 and r.unitID==nil and v.token=='REQUEST'and v.institutionSummary.token=='STORE_IDENTITY'and v.institutionArchive.RESEARCH==4 and v.institutionSummary.tradition.age==15 and v.institutionSummary.reference.x==2 and v.institutionSummary.reputation.state=='PAUSED');assert(v.institutionSummary.dialogue==1001 and v.institutionSummary.engineering==500 and v.institutionSummary.buildingTemplates==5000);assert(v.native==nil and v.institutionSummary.receipt==nil and v.institutionSummary.reference.city==nil and v.institutionSummary.tradition.native==nil)")
 def test_nil_false_zero_empty_archive_and_isolated_summary_are_not_coalesced(self):
  c=fixture();c.execute("local s=value();s.active=nil;s.activeStatus='UNKNOWN_GOVERNOR';s.institutionArchive={};s.institutionSummary.tradition=false;s.institutionSummary.reputation=nil;s.institutionSummary.reputationKnown=false;s.institutionSummary.districtTemplates=nil;assert(d.PublishPresentation(0,packet(),s));local v=d.Take(0,'REQUEST').presentation;assert(v.active==nil and v.activeStatus=='UNKNOWN_GOVERNOR'and next(v.institutionArchive)==nil and v.institutionSummary.tradition==false and v.institutionSummary.reputation==nil and v.institutionSummary.reputationKnown==false and v.institutionSummary.districtTemplates==nil);s=value('B');s.institutionArchive=nil;s.institutionSummary={known=false};assert(d.PublishPresentation(0,packet('B'),s));local v=d.Take(0,'B').presentation;assert(v.institutionArchive==nil and v.potential==4 and not v.institutionSummary.known)")
 def test_error_before_coordinates_is_explicit_and_does_not_synthesize_zeros(self):
  c=fixture();c.execute("assert(d.PublishPresentation(0,packet(),{owner=0,cityID=3,token='REQUEST',error='CITY_UNAVAILABLE'}));local v=d.Take(0,'REQUEST').presentation;assert(v.error=='CITY_UNAVAILABLE'and v.x==nil and v.active==nil and v.potential==nil and v.institutionSummary==nil)")
 def test_wrong_metadata_nested_types_nonfinite_or_limits_do_not_evict_valid_evidence(self):
  for change in ("s.owner=1",'s.cityID=4',"s.token='OTHER'",'s.x=math.huge','s.institutionSummary.dialogue=0/0','s.institutionArchive.RESEARCH={}',"s.institutionSummary.known='true'",'s.institutionSummary.reference=setmetatable(s.institutionSummary.reference,{})','s.institutionSummary.tradition=0',"s.institutionSummary.reputation.state=string.rep('X',129)","s.error=string.rep('X',20001)","s.institutionSummary.token=string.rep('X',257)"):
   c=fixture();c.execute("assert(d.PublishPresentation(0,packet('KEEP'),value('KEEP')));local s=value();"+change+";assert(not d.PublishPresentation(0,packet(),s)and d.Count()==1 and d.Has(0,'KEEP'))")
 def test_city_scope_cannot_retain_extra_unit_native_object_or_cross_ports(self):
  c=fixture();c.execute("local p=packet();p.UnitID={native=true};assert(d.Accepts(0,p)and d.PublishPresentation(0,p,value()));local r=d.Take(0,'REQUEST');assert(r.unitID==nil and r.cityID==3);p.CityID=nil;p.UnitID=3;assert(not d.Accepts(0,p));assert(not d.PublishTargets(0,packet(),{})and not d.PublishView(0,packet(),{})and not d.Publish(0,packet(),'X'))")
 def test_independent_capacity_factory_and_parent_close_release_all_four_ports(self):
  c=fixture();c.execute("P={VERSION='TEST'};local a=SPCPlayerActionReplies.Start(P,shared);local p=packet();local q={ReplyChannel='UNIT_ACTION',ReplyEpoch=1,Action='UNIT_ACTION_CONFIRM',UnitID=3,Token='REQUEST'};assert(a.Publish(0,q,'DONE'));q.ReplyChannel='UNIT_VIEW';q.Action='UNIT_ACTION_VIEW';assert(a.Views.FailView(0,q));q.ReplyChannel='UNIT_TARGETS';q.Action='UNIT_TARGETS_READ';assert(a.Targets.FailTargets(0,q));for i=1,1000 do local t='P'..i;assert(a.Presentations.PublishPresentation(0,packet(t),value(t)))end;assert(a.Presentations.Count()==8 and a.Count()==1 and a.Views.Count()==1 and a.Targets.Count()==1);local old=a.Presentations;local next=SPCPlayerActionReplies.Start(P,shared);assert(next.epoch==2 and old.Count()==0 and not old.FailPresentation(0,p));next.Shutdown();assert(next.Count()==0 and next.Views.Count()==0 and next.Targets.Count()==0 and next.Presentations.Count()==0)")
  measure('S9c6a_fixed_presentation_transport',{'ports':4,'slots_per_port':8,'total_max_slots':32,'max_fixed_payload_tables':6,'max_fixed_payload_keys':46,'normal_successful_producer_keys':45,'text_budget':32768,'native_reads_in_projection':0,'UI_migrated':False})

class Producer(unittest.TestCase):
 def setup(self):
  c=request();c.execute("""
 reads={facts=0,summary=0,archive=0,find=0,owner=0,id=0,x=0,y=0};city={owner=0,id=3,x=2,y=3}
 for name,field in pairs({GetOwner='owner',GetID='id',GetX='x',GetY='y'})do city[name]=function(self)reads[field]=reads[field]+1;if onNative then onNative(field)end;return self[field]end end
 Players[0]={GetCities=function()return {FindID=function(_,id)reads.find=reads.find+1;return id==city.id and city end}end}
 shared.EffectiveFacts={Read=function()reads.facts=reads.facts+1;if onFacts then onFacts()end;return {specialization='RESEARCH',potential=4,active=4,activeStatus='KNOWN',investmentCount=3,token='STORE_IDENTITY'}end}
 shared.CityProgressionStore={InstitutionArchive=function()reads.archive=reads.archive+1;return {CULTURE=2}end,
 InstitutionSummary=function()reads.summary=reads.summary+1;if onSummary then onSummary()end;return {known=true,token='STORE_IDENTITY',reference={owner=0,cityID=3,x=2,y=3},tradition={age=0,state='COUNTING',cursor=1},dialogue=0}end}
 GameConfiguration={GetGameSpeedType=function()return 'STANDARD'end};GameInfo=GameInfo or {};GameInfo.GameSpeeds={STANDARD={CostMultiplier=100}};SPCResearchTradition={Shadow=function()return 5,10 end}
 function pp(t)return {ReplyChannel='CITY_PRESENTATION',ReplyEpoch=d.epoch,Action='CITY_PRESENTATION_READ',CityID=3,Token=t or 'REQUEST'}end
 """);return c
 def test_actual_request_publishes_same_values_once_and_preserves_legacy_only_path(self):
  c=self.setup();c.execute("runRequest(0,pp());local v=d.Presentations.Take(0,'REQUEST').presentation;local s=shared.CityPresentationView;assert(v.token==s.token and v.potential==4 and v.active==4 and v.x==2 and v.y==3 and v.institutionSummary.tradition.percent==5 and v.institutionSummary.token=='STORE_IDENTITY');assert(reads.facts==1 and reads.summary==1 and reads.archive==1 and reads.find==1);runRequest(0,{Action='CITY_PRESENTATION_READ',CityID=3,Token='DEV'});assert(shared.CityPresentationView.token=='DEV'and d.Presentations.Count()==0 and reads.facts==2 and reads.find==2)")
 def test_wrong_epoch_channel_and_service_do_not_read_city(self):
  for change in ('p.ReplyEpoch=99',"p.ReplyChannel='UNIT_TARGETS'",'shared.PlayerActionReplies=nil'):
   c=self.setup();c.execute('local p=pp();'+change+';runRequest(0,p);assert(reads.find==0 and reads.facts==0)')
 def test_summary_failure_is_not_whole_city_failure_or_fabricated_zero(self):
  c=self.setup();c.execute("onSummary=function()error('SUMMARY_UNAVAILABLE')end;runRequest(0,pp());local v=d.Presentations.Take(0,'REQUEST').presentation;assert(not v.error and v.potential==4 and v.active==4 and v.institutionSummary.known==false and v.institutionSummary.dialogue==nil and reads.facts==1)")
 def test_native_reference_failure_is_inside_protected_read_and_never_stale_success(self):
  for code in ("onNative=function(field)if field=='x'then error('NATIVE_UNAVAILABLE')end end", "onNative=function(field)if field=='y'then city.owner=1 end end"):
   c=self.setup();c.execute(code+";runRequest(0,pp());local v=d.Presentations.Take(0,'REQUEST').presentation;assert(v.error and v.active==nil and v.x==nil and reads.facts==1 and reads.find==1)")
 def test_service_reentry_does_not_publish_or_recompute_into_successor(self):
  c=self.setup();c.execute("local old=d;onFacts=function()onFacts=nil;SPCPlayerActionReplies.Start(P,shared)end;runRequest(0,pp());assert(reads.facts==1 and old.Presentations.Count()==0 and shared.PlayerActionReplies.Presentations.Count()==0 and shared.ObserverErrors['city-presentation-reply'])")
 def test_failed_projection_has_one_negative_without_repeating_facts_or_summary(self):
  c=self.setup();c.execute("d.Presentations.PublishPresentation=function()error('TRANSPORT_FAILED')end;runRequest(0,pp());local r=d.Presentations.Take(0,'REQUEST');assert(r.error=='PRESENTATION_UNAVAILABLE'and r.presentation==nil and reads.facts==1 and reads.summary==1 and shared.CityPresentationView.potential==4)")

class StoreSummary(ActualProfile,original.StoreSummary):
 """All six original B251 Store/real Gameplay assertions, unchanged, on Lua5.1."""


def load_tests(loader,standard,pattern):
 selection=json.loads((ROOT/'DevelopmentTests/refactor_selection.json').read_text())
 return unittest.TestSuite([standard,unittest.TestSuite(loader.loadTestsFromName(name)for name in selection['stages']['S9c5b'])])

if __name__=='__main__':unittest.main()
