"""Independent bounded UNIT_VIEW projection/producer, no UI migration yet."""
import json,unittest
from refactor_harness import Context,ROOT,measure
from test_refactor_s9c2 import request
from test_refactor_s9c3 import real_panel


def fixture():
 c=Context();c.load('PlayerActionReplies');c.execute("""
 a=SPCPlayerActionReplies.New(1,'TEST');d=SPCPlayerActionReplies.New(1,'TEST','UNIT_VIEW')
 function packet(t)return {ReplyChannel='UNIT_VIEW',ReplyEpoch=1,Action='UNIT_ACTION_VIEW',UnitID=10,Token=t or 'A'}end
 function view(t)return {owner=0,unitID=10,token=t or 'A',turn=1,x=2,y=3,legal=true,prepared=true,planToken='PLAN',amount=400.125,progress=20.25,cost=400.5,baseInput=380.25,baseUnused=19.875,targetName='WONDER',specialization='RESEARCH',potential=4,nextPotential=5}end
 """);return c

class Projection(unittest.TestCase):
 def test_fixed_fields_keep_precision_negative_outcomes_and_cap_five_without_policy(self):
  c=fixture();c.execute("local v=view();v.legal=false;v.prepared=false;assert(d.PublishView(0,packet(),v));local r=d.Take(0,'A');assert(r.view.amount==400.125 and r.view.progress==20.25 and r.view.cost==400.5 and r.view.nextPotential==5 and not r.view.legal);v=view('B');v.x=nil;v.y=nil;v.legal=false;v.prepared=false;v.reason='UNIT_MISSING';assert(d.PublishView(0,packet('B'),v));assert(d.Take(0,'B').view.x==nil)")
 def test_extra_native_objects_are_not_retained_and_original_mutation_does_not_alias(self):
  c=fixture();c.execute("local v=view();v.NativeCity={};v.nested={receipt='X'};assert(d.PublishView(0,packet(),v));v.amount=0;v.planToken='OTHER';local r=d.Take(0,'A');assert(r.view.amount==400.125 and r.view.planToken=='PLAN'and r.view.NativeCity==nil and r.view.nested==nil)")
 def test_wrong_reference_protocol_or_port_cannot_publish(self):
  for mutation in ('v.owner=1','v.unitID=99',"v.token='B'",'v.legal=1','v.prepared=nil','v=setmetatable(v,{})'):
   c=fixture();c.execute('local v=view();'+mutation+';assert(not d.PublishView(0,packet(),v)and d.Count()==0)')
  c=fixture();c.execute("assert(not d.Publish(0,packet(),'TEXT'));local p=packet();p.ReplyChannel='UNIT_ACTION';assert(not d.Accepts(0,p));assert(not a.PublishView(0,p,view()));assert(not pcall(SPCPlayerActionReplies.New,1,'TEST',false)and not pcall(SPCPlayerActionReplies.New,1,'TEST','UNIT_TARGETS'))")
 def test_nonfinite_or_wrong_scalar_fields_reject_without_evicting_old(self):
  for mutation in ('v.amount=math.huge','v.cost=0/0','v.progress=-math.huge',"v.potential='4'",'v.planToken={}',"v.reason=string.rep('X',200001)",'v.targetName={}'):
   c=fixture();c.execute("assert(d.PublishView(0,packet('KEEP'),view('KEEP')));local v=view();"+mutation+";assert(not d.PublishView(0,packet(),v)and d.Count()==1 and d.Has(0,'KEEP'))")
 def test_view_capacity_does_not_evict_or_cross_consume_terminal_ACK(self):
  c=fixture();c.execute("local p={ReplyChannel='UNIT_ACTION',ReplyEpoch=1,Action='UNIT_ACTION_CONFIRM',UnitID=10,Token='A'};assert(a.Publish(0,p,'COMMITTED'));for i=1,100 do local t='V'..i;assert(d.PublishView(0,packet(t),view(t)))end;assert(d.Count()==8 and a.Count()==1 and a.Has(0,'A')and not d.Has(0,'A'));assert(a.Take(0,'A').text=='COMMITTED')")
  measure('S9c4a_fixed_view_capacity',{'ports':2,'slots_per_port':8,'total_max_slots':16,'view_fields':19,'views_cannot_evict_action_ACK':True,'extra_native_reads_per_view':0,'UI_migrated':False})
 def test_real_factory_shutdown_clears_both_old_ports_and_increments_once(self):
  c=fixture();c.execute("P={VERSION='TEST'};local p=SPCPlayerActionReplies.Start(P,shared);local old=p.Views;local v=view();assert(old.PublishView(0,packet(),v));local next=SPCPlayerActionReplies.Start(P,shared);assert(next.epoch==p.epoch+1 and old.Count()==0 and not old.Has(0,'A')and next.Views.epoch==next.epoch)")

class Producer(unittest.TestCase):
 def setup(self):
  c=request();c.execute("reads=0;shared.UnitActions.ReadView=function(pid,id,token)reads=reads+1;if onRead then onRead()end;local v={owner=pid,unitID=id,token=token,turn=1,legal=false,prepared=false,reason='NEGATIVE'};shared.UnitActionView=v;return v end;function vp(t)return {ReplyChannel='UNIT_VIEW',ReplyEpoch=d.epoch,Action='UNIT_ACTION_VIEW',UnitID=10,Token=t or 'V'}end");return c
 def test_actual_request_producer_calls_owner_once_and_preserves_legacy_global(self):
  c=self.setup();c.execute("runRequest(0,vp());assert(reads==1 and shared.UnitActionView.token=='V'and d.Views.Take(0,'V').view.reason=='NEGATIVE');runRequest(0,{Action='UNIT_ACTION_VIEW',UnitID=10,Token='DEV'});assert(reads==2 and shared.UnitActionView.token=='DEV'and d.Views.Count()==0)")
 def test_wrong_view_epoch_or_port_never_reads_owner(self):
  for mutation in ('p.ReplyEpoch=999',"p.ReplyChannel='UNIT_ACTION'",'shared.PlayerActionReplies=nil'):
   c=self.setup();c.execute("local p=vp();"+mutation+";runRequest(0,p);assert(reads==0)")
 def test_service_replacement_during_ReadView_does_not_publish_into_new_port(self):
  c=self.setup();c.execute("local old=d.Views;onRead=function()onRead=nil;SPCPlayerActionReplies.Start(P,shared)end;runRequest(0,vp());assert(reads==1 and old.Count()==0 and shared.PlayerActionReplies.Views.Count()==0 and shared.ObserverErrors['unit-view-reply'])")
 def test_transport_failure_cannot_roll_back_owner_preview_invalidation(self):
  c=self.setup();c.execute("plan='OLD';onRead=function()plan=nil end;d.Views.PublishView=function()error('TRANSPORT_FAILED')end;runRequest(0,vp());assert(reads==1 and plan==nil and shared.UnitActionView.reason=='NEGATIVE'and shared.ObserverErrors['unit-view-reply'])")
 def test_actual_Crew_ReadView_and_preview_invalidation_are_unmodified(self):
  v=real_panel();v.execute("local ch=shared.PlayerActionReplies.Views;local function p(t)return {ReplyChannel='UNIT_VIEW',ReplyEpoch=ch.epoch,Action='UNIT_ACTION_VIEW',UnitID=20001,Token=t}end;rawRequest(0,p('V1'));local a=ch.Take(0,'V1').view;assert(a.legal and not a.prepared);Controls.PrepareButton.click();publishPanel();rawRequest(0,p('V2'));local b=ch.Take(0,'V2').view;assert(b.prepared and b.planToken==shared.UnitActionPreview.token);c:GetBuildQueue().progress=99;rawRequest(0,p('V3'));local n=ch.Take(0,'V3').view;assert(not n.prepared and shared.UnitActionPreview==nil);assert(T.encode(n)==T.encode(shared.UnitActionView)and #c:GetBuildQueue().adds==0)")

def load_tests(loader,standard,pattern):
 selection=json.loads((ROOT/'DevelopmentTests/refactor_selection.json').read_text())
 return unittest.TestSuite([standard,unittest.TestSuite(loader.loadTestsFromName(name)for name in selection['stages']['S9c3'])])

if __name__=='__main__':unittest.main()
