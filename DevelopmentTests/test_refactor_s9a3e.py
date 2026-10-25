"""Actual owner-bound Training UI; idle native0 and covered reply freshness."""
from contextlib import contextmanager,nullcontext
from hashlib import sha256
from pathlib import Path
from unittest.mock import patch
import json,subprocess,unittest
from refactor_harness import ROOT,measure,TrackedLua51,SOURCES,legacy_source_observation
from test_refactor_s9a3d import runtime as gameplay
from test_refactor_s9b3 import profile
import test_expedition_training_ui as legacy

SETUP=r"""
Game.GetLocalPlayer=function()return 0 end;P.VERSION='S9a3e'
selectedCity=source;headReads=0;sent={};notifies=0;builds=0
UI={GetHeadSelectedCity=function()headReads=headReads+1;return selectedCity end}
PlayerOperations={EXECUTE_SCRIPT=1};CityProductionDirectives={TRAIN=1}
CheckQueueItemSelected=function()return false end
GameInfo=GameInfo or {};GameInfo.Units=GameInfo.Units or {}
local row={Index=900,Hash=900,UnitType='UNIT_SPC_EXPEDITION_SPY',Name='HUMANITIES',Cost=60}
GameInfo.Units.UNIT_SPC_EXPEDITION_SPY=row;GameInfo.Units[900]=row
Locale={Lookup=function(k)return k end}
queue={GetSize=function()return 0 end,GetAt=function()return nil end,GetUnitCost=function()return 60 end,
 GetUnitProgress=function()return 0 end,GetTurnsLeft=function()return 5 end,
 GetCurrentProductionTypeHash=function()return 0 end,CanProduce=function()return true end}
function source:GetBuildQueue()return queue end
function send(pid,op,p)sent[#sent+1]=p;if not deferred then shared.ExpeditionTraining.Request(pid,p)end;if afterSend then afterSend()end end
function notify(pid,id)notifies=notifies+1;if onNotify then onNotify()end end
function build()builds=builds+1 end
function render()local data={City=selectedCity,UnitItems={{Type='UNIT_SPY'}}};api.Items(data);return data end
function rows()local d=render();local n=0;for _,item in ipairs(d.UnitItems)do if item.Type=='UNIT_SPC_EXPEDITION_SPY'then n=n+1 end end;return n end
"""
def runtime():
 v=gameplay();v.execute(SETUP);v.execute((ROOT/'Mod/UI/ExpeditionTrainingUI.lua').read_text());v.execute('api=SPCExpeditionTrainingUI.New(P,send,notify,build)');return v

@contextmanager
def before():
 p=ROOT/'Mod/UI/ExpeditionTrainingUI.lua';old=subprocess.check_output(['git','show','ec0ddbd:Mod/UI/ExpeditionTrainingUI.lua'],cwd=ROOT,text=True);read,execute=Path.read_text,TrackedLua51.execute;h=sha256(old.encode()).hexdigest()
 def source(f,*a,**kw):return old if f==p else read(f,*a,**kw)
 def run(vm,s,*a,**kw):
  if sha256(s.encode()if isinstance(s,str)else s).hexdigest()==h:SOURCES[h]='historical/ec0ddbd/Mod/UI/ExpeditionTrainingUI.lua'
  return execute(vm,s,*a,**kw)
 with patch.object(Path,'read_text',source),patch.object(TrackedLua51,'execute',run),legacy_source_observation():yield

class ActualUI(unittest.TestCase):
 def test_first_sync_post_observation_is_consumed_before_continuous_render_or_notify_reentry(self):
  v=runtime();v.execute("onNotify=function()api.Sync(source);render();api.RefreshFacts()end;assert(rows()==1 and #sent==1 and notifies==1);for i=1,10 do render();api.Pulse();api.RefreshFacts()end;assert(#sent==1 and notifies==1)")
 def test_thousand_idle_publish_and_playback_calls_perform_zero_native_reads_requests_or_writes(self):
  v=runtime();v.execute("api.Sync(source);local requests=#sent;local scans=unitScans;local w=T.writes();local native=0;local function no()native=native+1;error('IDLE_NATIVE_FORBIDDEN')end;UI.GetHeadSelectedCity=no;Game.GetCurrentGameTurn=no;Game.GetLocalPlayer=no;Players[0].GetCities=no;Players[0].GetUnits=no;P.IsTestPlayer=no;for _,name in ipairs({'GetOwner','GetID','GetX','GetY','GetProperty','GetBuildQueue'})do source[name]=no end;for i=1,1000 do api.Pulse();api.RefreshFacts()end;assert(native==0 and #sent==requests and unitScans==scans and T.writes()==w)")
  measure('S9a3e_actual_Training_UI_idle',{'real_Store_EF_Gate_Training_UI':True,'idle_pulses':1000,'idle_playbacks':1000,'head_clock_city_unit_native_reads':0,'extra_SYNC':0,'extra_store_writes':0,'RuntimeUIRevision_dependency':False})
 def test_unrelated_global_revision_other_city_history_and_banner_do_not_refresh(self):
  v=runtime();v.execute("api.Sync(source);headReads=0;local count=#sent;ExposedMembers.SPC_RuntimeUIRevision=9999;local n=M.Copy(T.record(ca));n.revision=n.revision+1;assert(saveCandidate(ca,n));shared.LevelBanners={views={['0:'..aid]={active=4,potential=4,specialization='RESEARCH'}}};api.Pulse();assert(headReads==0 and #sent==count)")
 def test_unreserved_birth_and_removal_refresh_capacity_without_activity_transition_or_adoption(self):
  v=runtime();v.execute("api.Sync(source);local n=#sent;local revision=(ExposedMembers.SPC_ExpeditionActivity or {}).revision;local old=P.Info;P.Info=function(kind,id)if kind=='Units'and id==900 then return GameInfo.Units[900]end;return old(kind,id)end;units[88]={GetType=function()return 900 end};shared.ExpeditionTraining.Birth(0,88);api.RefreshFacts();assert(#sent==n+1 and rows()==0 and (ExposedMembers.SPC_ExpeditionActivity or {}).revision==revision);units[88]=nil;capacity.MarkUnitCapacity(0);api.RefreshFacts();assert(#sent==n+2 and rows()==1 and builds==0)")
 def test_actual_fact_and_final_binding_failure_recover_only_on_real_new_observation(self):
  v=runtime();v.execute("api.Sync(source);local n=#sent;local inv=s.Investment;s.Investment=function()error('TEMPORARY')end;assert(not pcall(shared.EffectiveFacts.Read,0,source));api.RefreshFacts();assert(rows()==0 and #sent==n+1);s.Investment=inv;shared.EffectiveFacts.Read(0,source);api.RefreshFacts();assert(rows()==1 and #sent==n+2);local raw=source.GetProperty;source.GetProperty=function(c,k)if k=='SPC_DEV_BINDING_B013_TOKEN'then return nil end;return raw(c,k)end;assert(not pcall(s.Base,0,source));api.RefreshFacts();assert(rows()==0);source.GetProperty=raw;assert(pcall(s.Base,0,source));api.RefreshFacts();assert(rows()==1 and builds==0)")
 def test_same_turn_second_successful_ACTIVE_observation_is_not_deduplicated(self):
  v=runtime();v.execute("api.Sync(source);local n=#sent;for _,level in ipairs({1,4,2,4})do T.governor(level);shared.EffectiveFacts.Read(0,source);api.RefreshFacts();assert(rows()==(level==4 and 1 or 0))end;assert(#sent==n+4 and builds==0)")
 def test_foreign_invalidate_is_idle_local_invalidate_observes_current_governor(self):
  v=runtime();v.execute("api.Sync(source);headReads=0;local n=#sent;api.Invalidate(9);api.RefreshFacts();assert(headReads==0 and #sent==n);T.governor(1);api.Invalidate(0);api.RefreshFacts();assert(rows()==0 and #sent==n+1)")
 def test_newer_input_after_reply_before_consumption_cannot_be_latched_as_covered(self):
  v=runtime();v.execute("deferred=true;api.Sync(source);local packet=sent[1];shared.ExpeditionTraining.Request(0,packet);T.governor(1);shared.EffectiveFacts.Read(0,source);api.RefreshFacts();assert(#sent==2 and rows()==0);shared.ExpeditionTraining.Request(0,sent[2]);api.RefreshFacts();assert(rows()==0);T.governor(4);shared.EffectiveFacts.Read(0,source);api.RefreshFacts();assert(#sent==3);shared.ExpeditionTraining.Request(0,sent[3]);api.RefreshFacts();assert(rows()==1)")
 def test_missing_receipt_never_authorizes_positive_row_or_causes_periodic_retry(self):
  v=runtime();v.execute("local request=shared.ExpeditionTraining.Request;shared.ExpeditionTraining.Request=function(...)request(...);ExposedMembers.SPC_ExpeditionTrainingReply.input=nil end;api.Sync(source);api.RefreshFacts();local n=#sent;for i=1,1000 do api.Pulse();api.RefreshFacts()end;assert(n<=2 and #sent==n and rows()==0 and builds==0)")
 def test_lost_sync_reply_does_not_periodically_retry(self):
  v=runtime();v.execute("deferred=true;api.Sync(source);for i=1,1000 do api.Pulse();api.RefreshFacts()end;assert(#sent==1 and rows()==0)")
 def test_source_or_method_replacement_rejects_old_reply_and_samples_once_again(self):
  for change in ("shared.EffectiveFacts={Read=shared.EffectiveFacts.Read}","local read=s.TrainingInputStamp;s.TrainingInputStamp=function(...)return read(...)end", "local old=capacity.CapacityInputStamp;capacity.CapacityInputStamp=function(...)return old(...)end", "local old=shared.ExpeditionTraining.Request;shared.ExpeditionTraining.Request=function(...)return old(...)end"):
   v=runtime();v.execute("deferred=true;api.Sync(source);shared.ExpeditionTraining.Request(0,sent[1]);"+change+";api.RefreshFacts();assert(#sent==2 and rows()==0);shared.ExpeditionTraining.Request(0,sent[2]);api.RefreshFacts();assert(rows()==1 and #sent==2)")
 def test_forged_source_equality_cannot_bypass_exact_source_change(self):
  v=runtime();v.execute("deferred=true;api.Sync(source);shared.ExpeditionTraining.Request(0,sent[1]);local old=shared.EffectiveFacts;local next={};for k,v in pairs(old)do next[k]=v end;local meta={__eq=function()return true end};setmetatable(old,meta);setmetatable(next,meta);assert(old==next and not rawequal(old,next));shared.EffectiveFacts=next;api.RefreshFacts();assert(#sent==2 and rows()==0)")
 def test_notify_reentrant_render_of_another_city_is_deferred_without_losing_selection_cause(self):
  v=runtime();v.execute("local once=true;onNotify=function()if once then once=false;selectedCity=ca;api.Sync(ca);render()end end;api.Sync(source);assert(#sent==1);api.RefreshFacts();assert(#sent==2 and sent[2].CityID==aid and rows()==0)")
 def test_scope_change_with_same_city_ID_hides_old_row_and_does_not_accept_old_reply(self):
  v=runtime();v.execute("deferred=true;api.Sync(source);shared.ExpeditionTraining.Request(0,sent[1]);source.s.ref.x=source.s.ref.x+20;api.Sync(source);assert(#sent==2 and rows()==0);source.s.ref.x=bx;api.Sync(source);assert(#sent==3);shared.ExpeditionTraining.Request(0,sent[3]);api.RefreshFacts();assert(rows()==1)")
 def test_qualification_event_during_send_is_not_absorbed_by_own_post_stamp(self):
  v=runtime();v.execute("local once=true;afterSend=function()if once then once=false;T.governor(1);api.Invalidate(0)end end;api.Sync(source);assert(rows()==0 and #sent==2);local n=#sent;api.RefreshFacts();assert(#sent==n)")
 def test_notify_source_replacement_or_deferred_selection_cannot_render_old_positive_row(self):
  v=runtime();v.execute("onNotify=function()local next={};for k,v in pairs(capacity)do next[k]=v end;next.Available=function()return false end;shared.ExpeditionGate={Training=next}end;assert(rows()==0 and #sent==1)")
 def test_native_render_getter_changes_source_before_append_rejects_old_row(self):
  v=runtime();v.execute("local cost=queue.GetUnitCost;queue.GetUnitCost=function(...)shared.EffectiveFacts={Read=shared.EffectiveFacts.Read};return cost(...)end;assert(rows()==0 and #sent==1)")
 def test_build_callback_close_stops_current_handshake_without_replay_or_queue_access(self):
  with profile():v=legacy.ui()
  v.execute("build=function()builds=builds+1;adapter.Close();error('BUILD_RETURN_UNCERTAIN')end;adapter=SPCExpeditionTrainingUI.New(P,send,notify,build);assert(not adapter.Before(city,{Type=kind},false));assert(pcall(adapter.Pulse));assert(builds==1);for i=1,20 do adapter.Pulse()end;assert(builds==1 and #sentPackets==1 and state().phase=='TRAINING')")
 def test_close_drops_UI_only_and_all_late_public_entrypoints_do_zero_native_work(self):
  v=runtime();v.execute("deferred=true;api.Before(source,{Type='UNIT_SPC_EXPEDITION_SPY'},false);local n=#sent;local w=T.writes();api.Close();local function no()error('LATE_NATIVE_FORBIDDEN')end;UI.GetHeadSelectedCity=no;Game.GetLocalPlayer=no;Game.GetCurrentGameTurn=no;source.GetOwner=no;for i=1,10 do api.Pulse();api.RefreshFacts();api.Sync(source);api.Items({City=source,UnitItems={}});api.CancelQueue(source,0);api.Invalidate(0);assert(not api.Before(source,{Type='UNIT_SPC_EXPEDITION_SPY'},false))end;assert(ExposedMembers.SPC_ExpeditionQueueRead(0,bid)==nil and #sent==n and T.writes()==w and builds==0)")
 def test_close_during_send_does_not_apply_or_notify_late_reply(self):
  v=runtime();v.execute("afterSend=function()api.Close()end;api.Sync(source);assert(#sent==1 and notifies==0);api.Pulse();assert(#sent==1)")
 def test_close_during_reference_or_pure_receipt_read_does_not_notify_or_send_after_close(self):
  v=runtime();v.execute("local owner=source.GetOwner;source.GetOwner=function(...)api.Close();return owner(...)end;Game.GetLocalPlayer=function()error('AFTER_CLOSE')end;api.Sync(source);assert(#sent==0 and notifies==0)")
  v=runtime();v.execute("deferred=true;api.Sync(source);shared.ExpeditionTraining.Request(0,sent[1]);local read=s.TrainingInputStamp;s.TrainingInputStamp=function(...)api.Close();return read(...)end;api.RefreshFacts();assert(#sent==1 and notifies==0)")
 def test_notify_error_releases_pump_without_resending_already_consumed_reply(self):
  v=runtime();v.execute("onNotify=function()error('RENDER_ONLY')end;assert(not pcall(api.Sync,source));onNotify=nil;api.RefreshFacts();assert(rows()==1 and #sent==1)")
 def test_cached_selection_is_scalar_and_unsolicited_reply_objects_are_not_retained(self):
  v=runtime();v.execute("weak=setmetatable({},{__mode='v'});do local temp={};for k,x in pairs(source)do temp[k]=x end;weak[1]=temp;api.Sync(temp);temp=nil end;collectgarbage('collect');assert(weak[1]==nil);deferred=true;api.Invalidate(0);api.Sync(source);local packet=sent[#sent];shared.ExpeditionTraining.Request(0,packet);do local extra={nativeSurrogate=true};weak[2]=extra;local delivered={};for k,value in pairs(ExposedMembers.SPC_ExpeditionTrainingReply)do delivered[k]=value end;delivered.unsolicited=extra;ExposedMembers.SPC_ExpeditionTrainingReply=delivered;api.RefreshFacts();ExposedMembers.SPC_ExpeditionTrainingReply=nil;delivered=nil;extra=nil end;collectgarbage('collect');assert(weak[2]==nil and rows()==1)")
 def test_pending_handshake_blocks_sync_after_input_change_and_never_replays_reserve(self):
  v=runtime();v.execute("deferred=true;api.Sync(source);api.Before(source,{Type='UNIT_SPC_EXPEDITION_SPY'},false);api.Invalidate(0);local count=#sent;for i=1,12 do api.Pulse();api.RefreshFacts()end;assert(#sent==count and builds==0);api.Pulse();local reserves=0;for _,p in ipairs(sent)do if p.Action=='RESERVE'then reserves=reserves+1 end end;assert(reserves==1 and builds==0)")


class Differential(unittest.TestCase):
 def test_visible_native_row_fields_match_B368_with_explicit_render_read_cost(self):
  out=[]
  for old in (True,False):
   with before()if old else nullcontext():v=runtime()
   v.execute("api.Sync(source);api.Pulse();reads={};for _,name in ipairs({'GetOwner','GetID','GetX','GetY'})do local get=source[name];source[name]=function(...)reads[name]=(reads[name]or 0)+1;return get(...)end end;local now=Game.GetCurrentGameTurn;Game.GetCurrentGameTurn=function(...)reads.clock=(reads.clock or 0)+1;return now(...)end;local r=render().UnitItems[2];assert(r);row=table.concat({r.Index,r.Type,r.Name,r.Hash,r.Kind,r.ToolTip,r.TurnsLeft,tostring(r.Disabled),tostring(r.Civilian),r.Cost,r.Progress,tostring(r.IsCurrentProduction),r.SortIndex},'|')")
   out.append((v.globals().row,dict(v.globals().reads)))
  self.assertEqual(out[0][0],out[1][0]);measure('S9a3e_native_render_differential',{'baseline':'ec0ddbd','same_visible_row_values':True,'render_ref_read_counts_before_after':[out[0][1],out[1][1]],'idle_native_cost_reported_separately':True,'native_CPU_or_memory_claim':False})


def load_tests(loader,standard,pattern):
 selection=json.loads((ROOT/'DevelopmentTests/refactor_selection.json').read_text())
 return unittest.TestSuite([standard,unittest.TestSuite(loader.loadTestsFromName(name)for name in selection['stages']['S9a3d'])])
if __name__=='__main__':unittest.main()
