"""Bounded terminal reply transport only; no production consumer wired here."""
import json,unittest
from refactor_harness import Context,ROOT,measure


def fixture():
 c=Context();c.load('PlayerActionReplies');c.execute("""
 d=SPCPlayerActionReplies.New(7,'TEST')
 function packet(token,id,action)return {ReplyChannel='UNIT_ACTION',ReplyEpoch=7,Token=token,UnitID=id or 10,Action=action or 'UNIT_ACTION_CONFIRM'}end
 function publish(token,pid)return d.Publish(pid or 0,packet(token),'CONFIRMED',{status='COMMITTED',kind='CREW_USE',phase='NATIVE_GRANT'})end
 """);return c

class Transport(unittest.TestCase):
 def test_fixed_detached_payload_does_not_retain_receipt_plan_or_native_extensions(self):
  c=fixture();c.execute("local p=packet('A');p.Plan={native='FORBIDDEN'};local o={status='HELD',kind='INVESTMENT',phase='CONFIRM',receipt={native='FORBIDDEN'},amount=100};assert(d.Publish(0,p,'等待核对',o));p.Token='CHANGED';p.UnitID=99;o.status='COMMITTED';local r=d.Take(0,'A');assert(r.owner==0 and r.token=='A'and r.unitID==10 and r.epoch==7 and r.version=='TEST'and r.text=='等待核对'and r.outcome.status=='HELD'and r.outcome.receipt==nil and r.outcome.amount==nil and r.Plan==nil and getmetatable(r)==nil and getmetatable(r.outcome)==nil)")
 def test_owner_and_token_are_independent_and_Take_clears_before_return(self):
  c=fixture();c.execute("assert(publish('SAME',0)and publish('SAME',1));assert(not d.Has(2,'SAME')and not d.Take(2,'SAME'));local a=d.Take(0,'SAME');assert(a.owner==0 and not d.Has(0,'SAME')and d.Has(1,'SAME')and d.Count()==1);assert(not d.Take(0,'SAME'));assert(d.Take(1,'SAME').owner==1 and d.Count()==0)")
 def test_two_delayed_tokens_cannot_overwrite_each_other(self):
  c=fixture();c.execute("assert(d.Publish(0,packet('SECOND'),'second'));assert(d.Publish(0,packet('FIRST'),'first'));assert(d.Take(0,'FIRST').text=='first'and d.Take(0,'SECOND').text=='second')")
 def test_duplicate_retained_terminal_never_overwrites_original_evidence(self):
  c=fixture();c.execute("assert(publish('A'));local ok,why=d.Publish(0,packet('A'),'REJECTED',{status='REJECTED'});assert(not ok and why=='ALREADY_RETAINED'and d.Count()==1);local a=d.Take(0,'A');assert(a.text=='CONFIRMED'and a.outcome.status=='COMMITTED')")
 def test_ring_keeps_only_last_eight_publications_with_explicit_eviction(self):
  c=fixture();c.execute("for i=1,1000 do assert(publish('T'..i));assert(d.Count()<=8)end;assert(d.Count()==8 and not d.Has(0,'T992'));for i=993,1000 do assert(d.Take(0,'T'..i))end;assert(d.Count()==0)")
  measure('S9c1_reply_capacity',{'publications':1000,'capacity':8,'maximum_retained':8,'retention':'last8 publications minus explicit consumption','transaction_or_replay_authority':False,'production_wiring':False})
 def test_discard_is_exact_and_old_service_shutdown_cannot_clear_new_service(self):
  c=fixture();c.execute("assert(publish('A')and publish('B'));assert(not d.Discard(1,'A'));assert(d.Discard(0,'A')and not d.Discard(0,'A')and d.Has(0,'B'));local next=SPCPlayerActionReplies.New(8,'TEST');d.Shutdown();assert(d.Count()==0 and not d.Has(0,'B')and not d.Take(0,'B'));assert(next.Accepts(0,{ReplyChannel='UNIT_ACTION',ReplyEpoch=8,Token='N',UnitID=1,Action='UNIT_ACTION_PREPARE'}))")
 def test_stale_epoch_wrong_channel_action_unit_owner_and_token_are_rejected(self):
  for mutation in ('p.ReplyEpoch=6',"p.ReplyChannel='DEV'","p.Action='UNIT_ACTION_SPAWN'","p.Action='READ'",'p.UnitID=-1','p.UnitID=0/0','p.UnitID=math.huge',"p.Token=''","p.Token=string.rep('X',257)"):
   c=fixture();c.execute("local p=packet('A');"+mutation+";assert(not d.Accepts(0,p)and not d.Publish(0,p,'X')and d.Count()==0)")
  c=fixture();c.execute("assert(not d.Publish(-1,packet('A'),'X')and not d.Publish('0',packet('A'),'X')and not d.Publish(0,setmetatable(packet('A'),{}),'X'))")
 def test_bad_session_limits_fail_without_truncation_or_silent_coercion(self):
  c=fixture();c.execute("for _,e in ipairs({0,-1,0/0,math.huge,9007199254740992,'7'})do assert(not pcall(SPCPlayerActionReplies.New,e,'TEST'))end;assert(not pcall(SPCPlayerActionReplies.New,1,''))")
 def test_payload_limits_reject_without_evicting_valid_evidence(self):
  c=fixture();c.execute("assert(publish('A'));assert(not d.Publish(0,packet('B'),{})and not d.Publish(0,packet('B'),string.rep('X',200001)));assert(not d.Publish(0,packet('B'),'B',{status={}}));assert(not d.Publish(0,packet('B'),'B',setmetatable({},{})));assert(d.Count()==1 and d.Take(0,'A').text=='CONFIRMED')")
 def test_Has_is_scalar_and_repeated_lookups_do_not_consume_or_publish(self):
  c=fixture();c.execute("assert(publish('A'));for i=1,10000 do assert(d.Has(0,'A')and not d.Has(0,'B'))end;assert(d.Count()==1 and d.Take(0,'A'))")
 def test_shutdown_rejects_all_old_session_calls(self):
  c=fixture();c.execute("assert(publish('A'));d.Shutdown();local p=packet('B');assert(not d.Accepts(0,p)and not d.Publish(0,p,'B')and not d.Discard(0,'A')and not d.Has(0,'A')and d.Count()==0)")
 def test_no_native_globals_callbacks_clock_or_saved_state_are_required(self):
  c=fixture();c.execute("Game=nil;Players=nil;Map=nil;Events=nil;GameEvents=nil;ExposedMembers=nil;Property=nil;collectgarbage=nil;local d=SPCPlayerActionReplies.New(1,'PURE');local p={ReplyChannel='UNIT_ACTION',ReplyEpoch=1,Token='NO_REPLAY',UnitID=0,Action='UNIT_ACTION_PREPARE'};assert(d.Publish(0,p,'READY',{status='PREPARED'}));assert(d.Has(0,p.Token));local r=d.Take(0,p.Token);assert(r.outcome.status=='PREPARED'and not d.Has(0,p.Token));d.Shutdown()")

def load_tests(loader,standard,pattern):
 selection=json.loads((ROOT/'DevelopmentTests/refactor_selection.json').read_text())
 return unittest.TestSuite([standard,unittest.TestSuite(loader.loadTestsFromName(name)for name in selection['stages']['S9b3'])])

if __name__=='__main__':unittest.main()
