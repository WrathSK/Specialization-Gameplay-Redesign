"""Marker consumer: isolated targets, exact old rendering/native work, lifecycle fences."""
from contextlib import contextmanager,nullcontext
from hashlib import sha256
from pathlib import Path
from unittest.mock import patch
import json,subprocess,unittest
from refactor_harness import ROOT,Context,SOURCES,executed,completion,legacy_source_observation,measure,EVENTS
from test_refactor_s6h import ui
from test_refactor_s6i import investment
from test_refactor_s5d4b2 import load_request

BASE='a19bff2'
@contextmanager
def before():
 p=ROOT/'Mod/UI/UnitTargetMarkers.lua';old=subprocess.check_output(['git','show',BASE+':Mod/UI/UnitTargetMarkers.lua'],cwd=ROOT,text=True);digest=sha256(old.encode()).hexdigest();key='historical/'+BASE+'/Mod/UI/UnitTargetMarkers.lua'
 read,load=Path.read_text,Context.load
 def source(path,*a,**kw):return old if path==p else read(path,*a,**kw)
 def module(c,name):
  if name not in ('UI/UnitTargetMarkers','UI/UnitTargetMarkers.lua'):return load(c,name)
  SOURCES[digest]=key;executed(key,digest)
  try:out=c.lua.execute(old)
  except Exception:completion(key,False);raise
  completion(key,True);return out
 with patch.object(Path,'read_text',source),patch.object(Context,'load',module):yield

class Differential(unittest.TestCase):
 def test_valid_render_visibility_sorting_requests_and_native_counts_match_B361(self):
  cases=("", "Events.CityProductionChanged.Fire(0,1);publish()", "selected=units[8];selectedChanged()", "selected=units[10];selectedChanged();LuaEvents.SPC_ToggleBuilderTargets.Fire()", "autoReply=false;selectedChanged();deliver()", "mutateReply=function(v)v.plots={{plot=12},{plot=4},{plot=999}};v.unknown={{cityID=2,reason='READ_UNKNOWN'}}end;selectedChanged()")
  for body in cases:
   out=[]
   for old in (True,False):
    with before()if old else nullcontext():c=ui(True)
    c.execute(body)
    out.append(tuple(c.eval(x)for x in ('ExposedMembers.SPC_TargetMarkerStatus','painted and table.concat(painted,",")','counts.getters','counts.selected','counts.requests','counts.lens','counts.clears')))
   self.assertEqual(out[0],out[1],body)
  measure('S9c5b_marker_differential',{'baseline':BASE,'cases':6,'same_status_visible_sorted_plots_requests_native_getters_lens_operations':True,'global_reply_consumed':False})

class Consumer(unittest.TestCase):
 def test_global_matching_token_does_not_answer_and_different_token_cannot_overwrite(self):
  c=ui(True);c.execute("autoReply=false;selectedChanged();local p=requests[#requests];assert(p.ReplyChannel=='UNIT_TARGETS');local s=ExposedMembers.SPC_P0;s.UnitTargetSnapshot={version=P.VERSION,owner=0,unitID=7,token=p.Token,turn=1,x=2,y=3,mode='INVEST',plots={{plot=1}},unknown={}};resetCounts();publish();assert(counts.lens==0 and counts.getters==0);reply(p);local q=clone(p);q.Token='OTHER';reply(q);publish();assert(counts.lens==1 and painted[1]==10 and s.PlayerActionReplies.Targets.Has(0,'OTHER'))")
 def test_bad_envelope_and_inner_token_are_taken_once_without_idle_reads(self):
  for change in ("r.owner=1","r.unitID=99","r.epoch=99","r.version='OLD'","r.action='UNIT_ACTION_VIEW'","r.targets.token='OTHER'","r.targets.x=99"):
   c=ui(True);c.execute("local d=ExposedMembers.SPC_P0.PlayerActionReplies.Targets;local take=d.Take;d.Take=function(...)local r=take(...);if r then "+change+" end;return r end;resetCounts();selectedChanged();assert(counts.lens==0 and d.Count()==0);resetCounts();idle(1000);assert(counts.requests==0 and counts.getters==0)")
 def test_negative_and_overbudget_never_paint_partial_or_fake_empty_map_or_retry(self):
  for body in ('assert(d.FailTargets(0,p))',"local s={version=P.VERSION,owner=0,unitID=7,token=p.Token,turn=1,x=2,y=3,mode='INVEST',plots={},unknown={}};for i=1,4097 do s.plots[i]={plot=i}end;assert(not d.PublishTargets(0,p,s));assert(d.FailTargets(0,p))"):
   c=ui(True);c.execute("autoReply=false;selectedChanged();local p=requests[#requests];local d=ExposedMembers.SPC_P0.PlayerActionReplies.Targets;"+body+";resetCounts();publish();assert(counts.lens==0 and ExposedMembers.SPC_TargetMarkerStatus=='TARGETS_UNAVAILABLE'and d.Count()==0);resetCounts();idle(1000);assert(counts.getters==0 and counts.requests==0)")
 def test_selection_and_builder_toggle_release_only_matching_target_expectation(self):
  c=ui(True);c.execute("autoReply=false;selectedChanged();local p=requests[#requests];reply(p);local parent=ExposedMembers.SPC_P0.PlayerActionReplies;local a={ReplyChannel='UNIT_ACTION',ReplyEpoch=parent.epoch,Action='UNIT_ACTION_CONFIRM',UnitID=7,Token=p.Token};local v=clone(a);v.ReplyChannel='UNIT_VIEW';v.Action='UNIT_ACTION_VIEW';assert(parent.Publish(0,a,'DONE')and parent.Views.FailView(0,v));selected=units[10];selectedChanged();assert(not parent.Targets.Has(0,p.Token));LuaEvents.SPC_ToggleBuilderTargets.Fire();local on=requests[#requests];assert(on.BuilderPreview);reply(on);LuaEvents.SPC_ToggleBuilderTargets.Fire();assert(not parent.Targets.Has(0,on.Token)and parent.Has(0,p.Token)and parent.Views.Has(0,p.Token));shutdown();assert(parent.Has(0,p.Token)and parent.Views.Has(0,p.Token))")
 def test_evicted_timeout_and_late_reply_are_not_automatic_retry(self):
  c=ui(True);c.execute("autoReply=false;selectedChanged();local p=requests[#requests];reply(p);local d=ExposedMembers.SPC_P0.PlayerActionReplies.Targets;for i=1,8 do local q=clone(p);q.Token='OTHER'..i;assert(d.FailTargets(0,q))end;resetCounts();publish();assert(counts.lens==0 and counts.getters==0);tick(11);publish();local n=counts.requests;reply(p);publish();assert(counts.requests==n and d.Has(0,p.Token));resetCounts();idle(1000);assert(counts.getters==0 and counts.requests==0)")
 def test_new_endpoint_is_one_reliable_availability_cause_not_per_publish_poll(self):
  c=ui(True,before='ExposedMembers.SPC_P0.PlayerActionReplies.Targets=nil');c.execute("assert(counts.requests==0);resetCounts();idle(1000);assert(counts.requests==0 and counts.getters==0);local s=ExposedMembers.SPC_P0;s.PlayerActionReplies.Targets=SPCPlayerActionReplies.New(s.PlayerActionReplies.epoch,P.VERSION,'UNIT_TARGETS');publish();assert(counts.requests==1 and counts.lens==1);resetCounts();idle(1000);assert(counts.requests==0 and counts.getters==0)")
 def test_shutdown_from_native_stamp_or_visibility_cannot_resume_paint_or_send(self):
  for boundary in ('STAMP','VISIBILITY'):
   c=ui(True);c.execute("local boundary=...;autoReply=false;local d=ExposedMembers.SPC_P0.PlayerActionReplies.Targets;local take=d.Take;local arm=false;d.Take=function(...)local r=take(...);arm=true;return r end;local get=selected.GetX;selected.GetX=function(u)if arm and boundary=='STAMP'then arm=false;Events.CityProductionChanged.Fire(0,1);shutdown()end;return get(u)end;local vis=PlayersVisibility[0].IsVisible;PlayersVisibility[0].IsVisible=function(...)if arm then arm=false;shutdown()end;return vis(...)end",boundary)
   c.execute("selectedChanged();local n=counts.requests;resetCounts();deliver();assert(counts.lens==0 and counts.requests==0 and tick==nil);publish();assert(counts.requests==0)")
 def test_replacement_from_visibility_cannot_paint_old_targets(self):
  c=ui(True);c.execute("autoReply=false;selectedChanged();local vis=PlayersVisibility[0].IsVisible;local once=true;PlayersVisibility[0].IsVisible=function(...)if once then once=false;SPCPlayerActionReplies.Start(P,ExposedMembers.SPC_P0)end;return vis(...)end;resetCounts();deliver();assert(counts.lens==0);publish();deliver();resetCounts();idle(1000);assert(counts.requests==0 and counts.getters==0)")
 def test_shutdown_from_paint_never_reopens_or_retains_layer(self):
  c=ui(True);c.execute("local paint=UILens.SetLayerHexesColoredArea;local ons=0;UILens.ToggleLayerOn=function()ons=ons+1 end;UILens.SetLayerHexesColoredArea=function(...)paint(...);shutdown()end;selectedChanged();assert(ons==0 and tick==nil);resetCounts();publish();assert(counts.requests==0 and counts.getters==0)")
 def test_native_Naturalist_layer_is_preserved_on_selection_and_shutdown(self):
  c=ui(True);c.execute("GameInfo.Units[5]={UnitType='UNIT_NATURALIST'};units[12]=makeUnit(12,5);local n=counts.clears;selected=units[12];selectedChanged();shutdown();assert(counts.clears==n and tick==nil)")

 def test_native_selection_change_during_layer_retirement_does_not_clear_new_GP_layer(self):
  c=ui(True);c.execute("local get=selected.GetType;local once=true;local gpClears=0;local clear=UILens.ClearLayerHexes;UILens.ClearLayerHexes=function(...)if selected==units[9]then gpClears=gpClears+1 end;return clear(...)end;selected.GetType=function(u)if once then once=false;selected=units[9];selectedChanged()end;return get(u)end;mode=2;Events.InterfaceModeChanged.Fire();assert(gpClears==0);resetCounts();idle(1000);assert(counts.requests==0 and counts.getters==0)")

 def test_selection_change_after_Clear_does_not_ToggleOff_new_native_layer(self):
  c=ui(True);c.execute("local clear=UILens.ClearLayerHexes;local gpOff=0;UILens.ToggleLayerOff=function()if selected==units[9]then gpOff=gpOff+1 end end;local once=true;UILens.ClearLayerHexes=function(...)local out=clear(...);if once then once=false;selected=units[9];selectedChanged()end;return out end;mode=2;Events.InterfaceModeChanged.Fire();assert(gpOff==0);resetCounts();idle(1000);assert(counts.requests==0 and counts.getters==0)")
 def test_new_selection_cause_during_old_ineligible_read_survives_to_next_publish(self):
  c=ui(True);c.execute("selected=units[9];selectedChanged();local get=selected.GetType;local once=true;selected.GetType=function(u)if once then once=false;selected=units[8];selectedChanged()end;return get(u)end;Events.CityProductionChanged.Fire(0,1);publish();local n=counts.requests;publish();assert(counts.requests==n+1 and counts.lens>0);resetCounts();idle(1000);assert(counts.requests==0 and counts.getters==0)")

 def test_new_selection_cause_during_nil_key_cleanup_survives_to_next_publish(self):
  c=ui(True);c.execute("local get=selected.GetType;local once=true;selected.GetType=function(u)if once then once=false;mode=1;selected=units[8];selectedChanged()end;return get(u)end;mode=2;Events.InterfaceModeChanged.Fire();local n=counts.requests;publish();assert(counts.requests==n+1 and painted[1]==10);resetCounts();idle(1000);assert(counts.requests==0 and counts.getters==0)")


def actual_marker():
 l=investment(32)
 with legacy_source_observation():l.globals().include('PlayerActionReplies')
 l.execute(EVENTS[:EVENTS.index('Events=eventSource();')])
 l.execute("Events=eventSource();LuaEvents=eventSource();ExposedMembers=ExposedMembers or {};shared.Version=P.VERSION;ExposedMembers.SPC_P0=shared;SPCPlayerActionReplies.Start(P,shared);P.Field=function(t,k)return t and t[k]end;P.Scalar=tostring;stage=function()end;selected=addSiteUnit(950);selected.x=199;Game.GetLocalPlayer=function()return 0 end;InterfaceModeTypes={SELECTION=1};PlayerOperations={EXECUTE_SCRIPT=1};requests=0;paints=0;ContextPtr={SetHide=function()end,SetInitHandler=function(_,f)initMarker=f end,SetShutdown=function(_,f)shutdownMarker=f end,SetUpdate=function(_,f)tickMarker=f end,ClearUpdate=function()tickMarker=nil end};UILens={CreateLensLayerHash=function()return 1 end,ClearLayerHexes=function()end,ToggleLayerOff=function()end,SetLayerHexesColoredArea=function(_,owner,plots)paints=paints+1;painted=plots end,ToggleLayerOn=function()end};PlayersVisibility={[0]={IsVisible=function()return true end}};UI={GetHeadSelectedUnit=function()return selected end,GetInterfaceMode=function()return 1 end,GetColorValue=function()return 1 end,RequestPlayerOperation=function(pid,op,p)requests=requests+1;return rawRequest(pid,p)end}")
 load_request(l)
 l.globals().include=lambda name:None
 l.execute('SPCP0=P')
 with legacy_source_observation():l.execute((ROOT/'Mod/UI/UnitTargetMarkers.lua').read_text())
 l.execute('initMarker()');return l

class ActualTargets(unittest.TestCase):
 def test_actual_32_city_marker_transport_has_one_scan_and_zero_idle_replay(self):
  l=actual_marker();l.execute("assert(requests==1 and paints==1 and #painted==32 and siteWork.ownerCities==1 and siteWork.ownerDistricts==1);local work=T.encode(siteWork);local writes=T.writes();for i=1,1000 do if tickMarker then tickMarker(.3)end;Events.GameCoreEventPublishComplete.Fire()end;assert(requests==1 and paints==1 and T.encode(siteWork)==work and T.writes()==writes and shared.PlayerActionReplies.Targets.Count()==0)")
  measure('S9c5b_actual_marker_idle',{'cities':32,'requests':1,'scans':1,'thousand_idle_extra_requests_or_scans':0,'Store_writes':0,'real_UnitTargets_Gameplay_transport_and_UI':True})


def load_tests(loader,standard,pattern):
 selection=json.loads((ROOT/'DevelopmentTests/refactor_selection.json').read_text())
 return unittest.TestSuite([standard,unittest.TestSuite(loader.loadTestsFromName(name)for name in selection['stages']['S9c5a'])])

if __name__=='__main__':unittest.main()
