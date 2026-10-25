"""Actual Gameplay reply producer; UI still uses the unchanged legacy path."""
import json,re,subprocess,unittest
from unittest.mock import patch
from pathlib import Path
from refactor_harness import Context,ROOT,legacy_source_observation,measure
from refactor_defect_fixtures import request_context,startup
from test_refactor_s5d4b2 import load_request
from test_refactor_s7d5 import fixture as crew,FAULTS


def request():
 c=request_context();c.load('PlayerActionReplies');c.execute("""
 P.VERSION='TEST';SPCPlayerActionReplies.Start(P,shared);d=shared.PlayerActionReplies
 calls=0;receipt={status='COMMITTED',cause='INVESTMENT_COMMITTED',city=1,reference={owner=0,cityID=1,x=2,y=3},anchor={token='T'},revision=1}
 shared.UnitActions={Run=function(pid,p)calls=calls+1;if inside then inside(pid,p)end;return 'COMMITTED',receipt,{status='COMMITTED',kind='INVESTMENT',phase='CONFIRM'}end}
 function packet(t)return {Action='UNIT_ACTION_CONFIRM',UnitID=10,Token=t,ReplyChannel='UNIT_ACTION',ReplyEpoch=d.epoch}end
 """);return c

class Producer(unittest.TestCase):
 def test_player_result_survives_DEV_overwrite_without_touching_DEV_slot(self):
  c=request();c.execute("shared.Snapshot='DEV_BEFORE';shared.LastToken='DEV';runRequest(0,packet('A'));assert(shared.Snapshot=='DEV_BEFORE'and shared.LastToken=='DEV'and calls==1);shared.Snapshot='OTHER_REPORT';shared.LastToken='OTHER';local r=d.Take(0,'A');assert(r.text=='COMMITTED'and r.action=='UNIT_ACTION_CONFIRM'and r.unitID==10 and r.outcome.status=='COMMITTED'and r.outcome.kind=='INVESTMENT'and r.outcome.phase=='CONFIRM'and r.receipt==nil)")
 def test_legacy_DEV_request_keeps_original_report_and_receipt_observer(self):
  c=request();c.execute("runRequest(0,{Action='UNIT_ACTION_CONFIRM',Token='DEV',UnitID=10});assert(shared.Snapshot=='COMMITTED'and shared.LastToken=='DEV'and calls==1 and d.Count()==0)")
 def test_wrong_or_unavailable_channel_never_calls_action_owner(self):
  for mutation in ("p.ReplyChannel='DEV'",'p.ReplyEpoch=999','p.UnitID=-1',"p.Token=''",'shared.PlayerActionReplies=nil'):
   c=request();c.execute("local p=packet('A');"+mutation+";runRequest(0,p);assert(calls==0 and d.Count()==0 and shared.Snapshot==nil)")
 def test_old_epoch_is_rejected_after_service_replacement_without_action_replay(self):
  c=request();c.execute("local p=packet('OLD');local old=d;SPCPlayerActionReplies.Start(P,shared);d=shared.PlayerActionReplies;assert(d.epoch==old.epoch+1);runRequest(0,p);assert(calls==0 and old.Count()==0 and d.Count()==0);runRequest(0,packet('NEW'));assert(calls==1 and d.Has(0,'NEW'))")
 def test_reply_is_published_before_receipt_fact_observer_and_survives_observer_error(self):
  c=request();c.execute("shared.FactChanges.Emit=function(e)assert(e.investment==receipt and d.Has(0,'A'));observed=(observed or 0)+1;error('OBSERVER_FAULT')end;runRequest(0,packet('A'));assert(calls==1 and d.Has(0,'A')and observed==1 and shared.ObserverErrors['request-facts']);assert(d.Take(0,'A').outcome.status=='COMMITTED')")
 def test_reply_publish_failure_does_not_drop_authoritative_receipt_propagation(self):
  c=request();c.execute("local emit=shared.FactChanges.Emit;shared.FactChanges.Emit=function(e)assert(e.investment==receipt);observed=(observed or 0)+1;return emit(e)end;d.Publish=function()error('TRANSPORT_FAULT')end;runRequest(0,packet('A'));assert(calls==1 and observed==1 and shared.ObserverErrors['unit-action-reply']=='PLAYER_REPLY_UNAVAILABLE'and not d.Has(0,'A'))")
 def test_reentrant_reply_service_replacement_does_not_publish_to_the_new_session(self):
  c=request();c.execute("local old=d;inside=function()SPCPlayerActionReplies.Start(P,shared);inside=nil end;runRequest(0,packet('A'));assert(calls==1 and old.Count()==0 and shared.PlayerActionReplies.Count()==0 and shared.ObserverErrors['unit-action-reply'])")
 def test_two_terminal_tokens_and_players_remain_independent_of_global_ACK(self):
  c=request();c.execute("P.IsTestPlayer=function(pid)return pid==0 or pid==1 end;runRequest(0,packet('A'));runRequest(1,packet('A'));runRequest(0,packet('B'));assert(d.Count()==3 and d.Take(1,'A').owner==1 and d.Take(0,'B').token=='B'and d.Take(0,'A').token=='A')")

class RealOwners(unittest.TestCase):
 def test_actual_Crew_outcomes_receipts_debit_progress_and_nonreplay_match_legacy_dispatch(self):
  for mode,inject in FAULTS.items():
   results=[]
   for typed in (False,True):
    v=crew();v.globals().include('SafeCallbacks');v.globals().include('PlayerActionReplies')
    v.execute("P.VERSION='TEST';SPCPlayerActionReplies.Start(P,shared);channel=shared.PlayerActionReplies;P.Observe=function()end;P.Scalar=tostring;stage=function()end")
    ctx=Context()
    v.execute(ctx.fragment('Mod/Gameplay.lua','local function refreshInvestmentSupport(', 'local function request(playerID,params)')+'\n_G.refreshInvestmentSupport=refreshInvestmentSupport')
    load_request(v)
    v.execute("local prepare={Action='UNIT_ACTION_PREPARE',UnitID=20001,Token='USE'};if ... then prepare.ReplyChannel='UNIT_ACTION';prepare.ReplyEpoch=channel.epoch end;rawRequest(0,prepare)",typed)
    v.execute(inject+";local p={Action='UNIT_ACTION_CONFIRM',UnitID=20001,PlanToken='USE',Token='CONFIRM'};if ... then p.ReplyChannel='UNIT_ACTION';p.ReplyEpoch=channel.epoch end;rawRequest(0,p);observed=T.encode({receipts=C.props.SPC_CREW_ACTION_RECEIPTS_V1,adds=c:GetBuildQueue().adds,progress=c:GetBuildQueue().progress,present=C.units[20001]~=nil});if ... then local r=channel.Take(0,'CONFIRM');assert(r and r.outcome.kind=='CREW_USE');state=r.outcome.status end;for i=1,3 do rawRequest(0,p)end;assert(#c:GetBuildQueue().adds<=1)",typed)
    results.append(v.eval('observed'))
    if typed:self.assertEqual(v.eval('state'),'COMMITTED'if mode=='normal'else'HELD')
   self.assertEqual(*results,mode)
  measure('S9c2_actual_Crew_producer',{'fault_modes':len(FAULTS),'same_authoritative_receipts_debit_progress_and_grant_calls':True,'typed_outcome_preserved':True,'DEV_slot_for_player_request':False,'production_UI_migrated':False})

class Startup(unittest.TestCase):
 def test_producer_startup_is_independent_and_missing_action_dependency_skips_it(self):
  c=startup();c.execute("SPCUnitActions.Start=function()error('ACTION_START_FAILED')end");c.load('Gameplay');c.execute("local s=ExposedMembers.SPC_P0;assert(s.StartStatus.UnitActions.state=='FAILED'and s.StartStatus.PlayerActionReplies.state=='SKIPPED_DEPENDENCY'and s.PlayerActionReplies==nil)")
 def test_original_start_sequence_is_exact_with_one_named_insertion(self):
  old=subprocess.check_output(['git','show','ca6f960:Mod/Gameplay.lua'],cwd=ROOT,text=True)
  current=(ROOT/'Mod/Gameplay.lua').read_text();pattern=r'(SPC\w+)\.Start\(P,shared'
  expected=re.findall(pattern,old);expected.insert(expected.index('SPCCrewPrecision'),'SPCPlayerActionReplies')
  self.assertEqual(re.findall(pattern,current),expected)
  self.assertIn("composition.Run('PlayerActionReplies',{'UnitActions'},{'PlayerActionReplies'}",current)
  c=startup();c.load('Gameplay');c.execute("assert(ExposedMembers.SPC_P0.StartStatus.PlayerActionReplies.state=='OK')")
 def test_original_composite_start_order_and_cleanup_assertion_remains_at_B356(self):
  import test_refactor_s8c5c as prior
  path=ROOT/'Mod/Gameplay.lua';old=subprocess.check_output(['git','show','ca6f960:Mod/Gameplay.lua'],cwd=ROOT,text=True);read=Path.read_text
  with patch.object(Path,'read_text',lambda p,*a,**kw:old if p==path else read(p,*a,**kw)),patch.object(prior,'measure',lambda name,data:measure(name+'_B356',data)):
   prior.Production('test_real_production_options_register_one_gate_and_preserve_all_old_start_order').test_real_production_options_register_one_gate_and_preserve_all_old_start_order(reply_service=False)
 def test_current_composite_options_and_1409_plus_two_cleanup_keep_original_assertions(self):
  import test_refactor_s8c5c as prior
  path=ROOT/'Mod/Gameplay.lua';current=path.read_text();read=Path.read_text
  inserted="composition.Run('PlayerActionReplies',{'UnitActions'},{'PlayerActionReplies'},function() include('PlayerActionReplies');SPCPlayerActionReplies.Start(P,shared) end)\n\n"
  self.assertEqual(current.count(inserted),1)
  projected=current.replace(inserted,'',1)
  with patch.object(Path,'read_text',lambda p,*a,**kw:projected if p==path else read(p,*a,**kw)),patch.object(prior,'measure',lambda name,data:measure(name+'_WITHOUT_REPLY_SERVICE',data)):
   prior.Production('test_real_production_options_register_one_gate_and_preserve_all_old_start_order').test_real_production_options_register_one_gate_and_preserve_all_old_start_order(reply_service=False)
 def test_real_factory_new_epoch_shutdown_and_failed_allocation_preserve_prior(self):
  c=Context();c.load('PlayerActionReplies');c.execute("P={VERSION='TEST'};local a=SPCPlayerActionReplies.Start(P,shared);local p={ReplyChannel='UNIT_ACTION',ReplyEpoch=a.epoch,Action='UNIT_ACTION_CONFIRM',UnitID=1,Token='A'};assert(a.Publish(0,p,'X'));local b=SPCPlayerActionReplies.Start(P,shared);assert(b.epoch==a.epoch+1 and a.Count()==0 and not a.Publish(0,p,'LATE'));ExposedMembers.SPC_PlayerActionReplyEpoch='BAD';assert(not pcall(SPCPlayerActionReplies.Start,P,shared)and shared.PlayerActionReplies==b)")

def load_tests(loader,standard,pattern):
 selection=json.loads((ROOT/'DevelopmentTests/refactor_selection.json').read_text())
 def flatten(suite):
  for item in suite:
   if isinstance(item,unittest.TestSuite):yield from flatten(item)
   else:yield item
 inherited=unittest.TestSuite()
 historical='test_refactor_s8c5c.Production.test_real_production_options_register_one_gate_and_preserve_all_old_start_order'
 for name in selection['stages']['S9c1']:
  for test in flatten(loader.loadTestsFromName(name)):
   if test.id()!=historical:inherited.addTest(test)
 return unittest.TestSuite([standard,inherited])

if __name__=='__main__':unittest.main()
