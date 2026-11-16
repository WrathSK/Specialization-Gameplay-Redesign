"""UNIT_VIEW consumer and negative delivery; independent of terminal ACTION."""
from contextlib import contextmanager,nullcontext
from hashlib import sha256
from pathlib import Path
from unittest.mock import patch
import json,subprocess,unittest
from refactor_harness import ROOT,Context,TrackedLua51,SOURCES,executed,completion,legacy_source_observation,measure
from test_refactor_s6h import ui
from test_refactor_s9c3 import real_panel

BASE='3fff36c'
@contextmanager
def before():
 p=ROOT/'Mod/UI/UnitPanelActions.lua';old=subprocess.check_output(['git','show',BASE+':Mod/UI/UnitPanelActions.lua'],cwd=ROOT,text=True);digest=sha256(old.encode()).hexdigest();key='historical/'+BASE+'/Mod/UI/UnitPanelActions.lua'
 read,load=Path.read_text,Context.load
 def source(path,*a,**kw):return old if path==p else read(path,*a,**kw)
 def module(c,name):
  if name not in ('UI/UnitPanelActions','UI/UnitPanelActions.lua'):return load(c,name)
  SOURCES[digest]=key;executed(key,digest)
  try:out=c.lua.execute(old)
  except Exception:completion(key,False);raise
  completion(key,True);return out
 with patch.object(Path,'read_text',source),patch.object(Context,'load',module):yield

class Differential(unittest.TestCase):
 def test_tooltips_icons_requests_and_native_work_match_prior_for_valid_views(self):
  cases=("", "Controls.PrepareButton.click();publish()", "Controls.PrepareButton.click();publish();Controls.ConfirmButton.click();publish()", "selected.kind=2;selectedChanged()", "selected.kind=2;selectedChanged();Controls.PrepareButton.click();publish()", "selected.kind=2;mutateReply=function(v)v.legal=false;v.prepared=false;v.potential=4;v.nextPotential=5;v.reason='POTENTIAL_CAP_4'end;selectedChanged()")
  for body in cases:
   out=[]
   for old in (True,False):
    with before()if old else nullcontext():c=ui()
    c.execute(body)
    out.append(tuple(c.eval(x)for x in ('Controls.PrepareIcon.icon','Controls.ConfirmIcon.icon','Controls.ConfirmButton.hide','Controls.PrepareButton.tip','Controls.ConfirmButton.tip','counts.requests','counts.getters')))
   self.assertEqual(out[0],out[1],body)
  measure('S9c4b_valid_UI_differential',{'baseline':BASE,'cases':6,'same_tooltips_icons_requests_native_getters':True,'current_transport':'UNIT_VIEW','extra_native_sampling':0})
 def test_existing_number_crew_and_investment_formatting_helpers_are_byte_identical(self):
  old=subprocess.check_output(['git','show',BASE+':Mod/UI/UnitPanelActions.lua'],cwd=ROOT,text=True);current=(ROOT/'Mod/UI/UnitPanelActions.lua').read_text()
  def helpers(text):return text[text.index('local function number('):text.index('local function dispatch(')]
  self.assertEqual(helpers(old),helpers(current))

class Consumer(unittest.TestCase):
 def test_global_matching_token_cannot_answer_typed_view(self):
  c=ui();c.execute("autoReply=false;selectedChanged();local p=requests[#requests];assert(p.ReplyChannel=='UNIT_VIEW');local s=ExposedMembers.SPC_P0;s.UnitActionView={owner=0,unitID=7,token=p.Token,turn=1,x=2,y=3,legal=true,prepared=true,planToken='FORGED'};s.UnitActionPreview={owner=0,unitID=7,turn=1,x=2,y=3,token='FORGED'};publish();assert(Controls.ConfirmButton.hide);deliver();assert(Controls.ConfirmButton.hide and s.PlayerActionReplies.Views.Count()==0)")
 def test_bad_envelope_and_inner_token_consume_once_without_idle_reads(self):
  for change in ("r.owner=1","r.unitID=99","r.epoch=99","r.version='OLD'","r.view.token='OTHER'","r.view.x=99"):
   c=ui();c.execute("local d=ExposedMembers.SPC_P0.PlayerActionReplies.Views;local take=d.Take;d.Take=function(...)local r=take(...);if r then "+change+" end;return r end;selectedChanged();assert(Controls.ConfirmButton.hide and d.Count()==0);resetCounts();idle(1000);assert(counts.requests==0 and counts.getters==0)")
 def test_port_replacement_from_last_native_stamp_cannot_restore_old_view(self):
  c=ui();c.execute("autoReply=false;local d=ExposedMembers.SPC_P0.PlayerActionReplies.Views;local take=d.Take;local arm=false;d.Take=function(...)local r=take(...);arm=true;return r end;local get=selected.GetY;selected.GetY=function(u)if arm then arm=false;SPCPlayerActionReplies.Start(P,ExposedMembers.SPC_P0)end;return get(u)end;selectedChanged();deliver();assert(Controls.ConfirmButton.hide);publish();deliver();resetCounts();idle(1000);assert(counts.requests==0)")
 def test_shutdown_during_native_stamp_cannot_restore_view_or_allow_late_button(self):
  c=ui();c.execute("autoReply=false;local d=ExposedMembers.SPC_P0.PlayerActionReplies.Views;local take=d.Take;local arm=false;d.Take=function(...)local r=take(...);arm=true;return r end;local get=selected.GetX;selected.GetX=function(u)if arm then arm=false;shutdown()end;return get(u)end;selectedChanged();deliver();local sent=actionCount('UNIT_ACTION_PREPARE');resetCounts();Controls.PrepareButton.click();assert(actionCount('UNIT_ACTION_PREPARE')==sent and counts.getters==0 and Controls.ActionGroup.hide and tick==nil)")
 def test_shutdown_with_a_new_dirty_cause_does_not_send_a_followup_VIEW(self):
  c=ui();c.execute("autoReply=false;local d=ExposedMembers.SPC_P0.PlayerActionReplies.Views;local take=d.Take;local arm=false;d.Take=function(...)local r=take(...);arm=true;return r end;local get=selected.GetX;selected.GetX=function(u)if arm then arm=false;Events.CityProductionChanged.Fire(0,1);shutdown()end;return get(u)end;selectedChanged();local sent=counts.requests;deliver();assert(tick==nil and counts.requests==sent and Controls.ActionGroup.hide);resetCounts();Controls.PrepareButton.click();assert(counts.requests==0 and counts.getters==0)")
 def test_VIEW_timeout_or_selection_clear_never_discards_ACTION_terminal(self):
  c=ui();c.execute("autoReply=false;selectedChanged();local s=ExposedMembers.SPC_P0;local p=requests[#requests];assert(s.PlayerActionReplies.Publish(0,{ReplyChannel='UNIT_ACTION',ReplyEpoch=s.PlayerActionReplies.epoch,Action='UNIT_ACTION_CONFIRM',UnitID=7,Token=p.Token},'COMMITTED'));tick(3);publish();assert(s.PlayerActionReplies.Has(0,p.Token));selected=units[8];selectedChanged();assert(s.PlayerActionReplies.Has(0,p.Token));shutdown();assert(s.PlayerActionReplies.Has(0,p.Token))")
 def test_unavailable_port_recovers_only_on_new_endpoint_once_without_timer_retry(self):
  c=ui(before='ExposedMembers.SPC_P0.PlayerActionReplies.Views=nil');c.execute("assert(counts.requests==0);resetCounts();idle(1000);assert(counts.requests==0 and counts.getters==0);local s=ExposedMembers.SPC_P0;s.PlayerActionReplies.Views=SPCPlayerActionReplies.New(s.PlayerActionReplies.epoch,P.VERSION,'UNIT_VIEW');publish();assert(counts.requests==1);resetCounts();idle(1000);assert(counts.requests==0 and counts.getters==0)")
 def test_negative_delivery_has_no_fake_view_and_ends_wait_without_polling(self):
  c=ui();c.execute("local s=ExposedMembers.SPC_P0;local d=s.PlayerActionReplies.Views;autoReply=false;selectedChanged();local p=requests[#requests];assert(d.FailView(0,p));publish();assert(Controls.ConfirmButton.hide and d.Count()==0);resetCounts();idle(1000);assert(counts.requests==0 and counts.getters==0)")
 def test_service_already_observed_during_action_ack_does_not_cause_second_view_read(self):
  c=ui();c.execute("local s=ExposedMembers.SPC_P0;local take=s.PlayerActionReplies.Take;s.PlayerActionReplies.Take=function(...)local r=take(...);SPCPlayerActionReplies.Start(P,s);return r end;Controls.PrepareButton.click();publish();local n=counts.requests;publish();assert(counts.requests==n);resetCounts();idle(1000);assert(counts.requests==0 and counts.getters==0)")

class Producer(unittest.TestCase):
 def test_actual_failed_view_publish_sends_one_negative_reply_and_preserves_owner_read(self):
  v=real_panel();v.execute("local port=shared.PlayerActionReplies.Views;port.PublishView=function()error('PROJECTION_UNAVAILABLE')end;local reads=0;local read=shared.UnitActions.ReadView;shared.UnitActions.ReadView=function(...)reads=reads+1;return read(...)end;Events.UnitSelectionChanged.Fire(0,20001);assert(reads==1 and port.Count()==0 and shared.ObserverErrors['unit-view-reply'] and #c:GetBuildQueue().adds==0);local n=#requests;for i=1,1000 do publishPanel()end;assert(#requests==n and reads==1)")
 def test_real_parent_shutdown_clears_both_ports_without_native_operation(self):
  v=real_panel();v.execute("local d=shared.PlayerActionReplies;local p={ReplyChannel='UNIT_VIEW',ReplyEpoch=d.epoch,Action='UNIT_ACTION_VIEW',UnitID=20001,Token='OLD'};assert(d.Views.FailView(0,p));d.Shutdown();assert(d.Count()==0 and d.Views.Count()==0 and #c:GetBuildQueue().adds==0 and C.units[20001])")

def load_tests(loader,standard,pattern):
 selection=json.loads((ROOT/'DevelopmentTests/refactor_selection.json').read_text())
 return unittest.TestSuite([standard,unittest.TestSuite(loader.loadTestsFromName(name)for name in selection['stages']['S9c4a'])])

if __name__=='__main__':unittest.main()
