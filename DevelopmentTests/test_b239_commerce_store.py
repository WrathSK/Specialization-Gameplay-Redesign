"""B239 Commerce configuration and institution history: actual model/Store L3.
No native yield, timing, CPU/memory or real save-file claim.
"""
from pathlib import Path
import unittest
from lupa.lua55 import LuaRuntime
from test_store_write_boundaries import fixture

ROOT=Path(__file__).resolve().parents[1]
HELPERS=r"""
C={};C.model=SPCCommerceModel
function C.standard()
 GameConfiguration.GetGameSpeedType=function()return 'GAMESPEED_STANDARD'end
 GameInfo.GameSpeeds={GAMESPEED_STANDARD={GameSpeedType='GAMESPEED_STANDARD',CostMultiplier=100}}
end
function C.make(i,level)
 local c=T.fresh(i or 1);T.register(c);T.complete(c,'DISTRICT_COMMERCIAL_HUB')
 for n=1,(level or 3)-1 do T.invest(c,9000+(i or 1)*10+n)end
 return c
end
function C.read(c)return shared.CityProgressionStore.CommerceState(0,c).value end
function C.select(c,domain,enabled)
 local old=C.read(c);local v=old or C.model.New(0)
 shared.CityProgressionStore.WriteCommerce(0,c,old,C.model.Select(v,domain,enabled))
end
function C.age(c)return assert(C.read(c).reputation).age end
"""
def runtime():
 lua=fixture();lua.execute(HELPERS);return lua

class Model(unittest.TestCase):
 def check(self,text):
  lua=LuaRuntime(unpack_returned_tuples=True);lua.execute((ROOT/'Mod/CommerceModel.lua').read_text());lua.execute('M=SPCCommerceModel;'+text)
 def test_lifo_suspend_resume_and_manual_reopen_order(self):
  self.check("local v=M.New(0);for _,d in ipairs({'DISTRICT_CAMPUS','DISTRICT_THEATER','DISTRICT_HOLY_SITE'})do v=M.Select(v,d,true)end;local one=M.EffectiveSelections(v,1);assert(#one.effective==1 and #one.suspended==2 and one.suspended[1]=='DISTRICT_THEATER');assert(#M.EffectiveSelections(v,3).effective==3);v=M.Select(v,'DISTRICT_CAMPUS',false);v=M.Select(v,'DISTRICT_CAMPUS',true);assert(v.selected[3]=='DISTRICT_CAMPUS' and M.EffectiveSelections(v,1).effective[1]=='DISTRICT_THEATER')")
 def test_duplicate_select_and_copies_do_not_mutate_authority(self):
  self.check("local v=M.Select(M.New(0),'DISTRICT_CAMPUS',true);local n=M.Select(v,'DISTRICT_CAMPUS',true);n.selected[1]='DISTRICT_THEATER';assert(v.selected[1]=='DISTRICT_CAMPUS');assert(#M.EffectiveSelections(v,0).suspended==1)")
 def test_invalid_domain_duplicate_sparse_unknown_capacity_rejected(self):
  self.check("local v=M.New(0);assert(not pcall(M.Select,v,'DISTRICT_COMMERCIAL_HUB',true));assert(not pcall(M.EffectiveSelections,v,-1));v.selected={[1]='DISTRICT_CAMPUS',[3]='DISTRICT_THEATER'};assert(not pcall(M.Validate,v));v.selected={'DISTRICT_CAMPUS','DISTRICT_CAMPUS'};assert(not pcall(M.Validate,v))")
 def test_standard_speed_is_exact_type_not_multiplier(self):
  self.check("GameConfiguration={GetGameSpeedType=function()return 17 end};GameInfo={GameSpeeds={[17]={GameSpeedType='GAMESPEED_STANDARD',CostMultiplier=200}}};assert(M.IsStandardSpeed());GameInfo.GameSpeeds[17]={GameSpeedType='GAMESPEED_QUICK',CostMultiplier=100};local ok,why=M.IsStandardSpeed();assert(not ok and why=='COMMERCE_STANDARD_SPEED_ONLY')")
 def test_missing_or_unreadable_speed_not_guessed(self):
  self.check("assert(not M.IsStandardSpeed());GameConfiguration={GetGameSpeedType=function()return 'GAMESPEED_STANDARD'end};assert(not M.IsStandardSpeed());GameInfo={GameSpeeds={GAMESPEED_STANDARD={CostMultiplier=100}}};assert(not M.IsStandardSpeed());GameConfiguration.GetGameSpeedType=function()error('unavailable')end;assert(not M.IsStandardSpeed())")
 def test_reputation_duplicate_turn_cap_and_identity_exit(self):
  self.check("local v=M.BeginReputation(M.New(0),5,'r');assert(M.Advance(v,5,'COMMERCE').reputation.age==0);for t=6,55 do v=M.Advance(v,t,'COMMERCE')end;assert(v.reputation.age==40);v=M.Select(v,'DISTRICT_CAMPUS',true);v=M.Advance(v,55,'INDUSTRY');assert(not v.reputation and #v.selected==0)")
 def test_unknown_gap_is_held_not_backfilled(self):
  self.check("local v=M.BeginReputation(M.New(0),5,'r');v=M.Advance(v,7,'COMMERCE');assert(v.reputation.age==0 and v.reputation.state=='UNKNOWN_INTERVAL');v=M.OwnerChanged(v,3,9);v=M.Resume(v,0,20);assert(v.reputation.state=='UNKNOWN_INTERVAL');assert(M.Advance(v,21,'COMMERCE').reputation.age==0)")

class Store(unittest.TestCase):
 def check(self,text):runtime().execute('T.start();C.standard();'+text)
 def test_three_investments_start_once_without_scanner_init(self):
  self.check("local c=C.make(1,3);assert(C.read(c)==nil);C.select(c,'DISTRICT_CAMPUS',true);T.turn(1);assert(not C.read(c).reputation);T.invest(c,10001);assert(C.age(c)==0 and C.read(c).reputation.start==T.now());assert(C.read(c).selected[1]=='DISTRICT_CAMPUS');local n=T.writes();Events.PlayerTurnActivated.Fire(0);assert(T.writes()==n);T.turn(1);assert(C.age(c)==1)")
 def test_active_loss_still_ages_and_selection_survives(self):
  self.check("local c=C.make(1,4);C.select(c,'DISTRICT_HARBOR',true);T.governor(1);T.turn(1);assert(C.age(c)==1 and C.read(c).selected[1]=='DISTRICT_HARBOR');assert(T.control(c).active==1)")
 def test_configuration_roundtrip_uses_defensive_copy(self):
  self.check("local c=C.make(1,3);C.select(c,'DISTRICT_CAMPUS',true);C.select(c,'DISTRICT_THEATER',true);local v=C.read(c);v.selected[1]='DISTRICT_HARBOR';assert(C.read(c).selected[1]=='DISTRICT_CAMPUS');local before=T.encode(C.read(c));local writes=T.writes();T.reload();assert(T.encode(C.read(c))==before and T.writes()==writes)")
 def test_coldload_reputation_duplicate_no_replay_then_next_turn(self):
  self.check("local c=C.make(1,4);T.turn(1);T.turn(1);assert(C.age(c)==2);local before=T.encode(C.read(c));local writes=T.writes();T.reload();assert(T.encode(C.read(c))==before and T.writes()==writes);T.turn(1);assert(C.age(c)==3)")
 def test_old_p4_missing_start_not_fabricated(self):
  self.check("local c=C.make(1,4);T.record(c).commerce=nil;T.record(c).commerceKnown=nil;T.reload();assert(C.read(c)==nil);C.select(c,'DISTRICT_CAMPUS',true);T.turn(1);assert(not C.read(c).reputation)")
 def test_missing_known_or_corrupt_history_not_reconstructed(self):
  for mutation in ('r.commerce=nil','r.commerce.reputation.age=99','r.commerce.reputation.receipt="missing"'):
   with self.subTest(mutation=mutation):self.check('local c=C.make(1,4);local r=T.record(c);'+mutation+';T.reload();assert(not pcall(C.read,c))')
 def test_wrong_owner_cannot_read_or_write(self):
  self.check("local c=C.make(1,4);local st=shared.CityProgressionStore;assert(not pcall(st.CommerceState,3,c));assert(not pcall(st.WriteCommerce,3,c,C.read(c),C.read(c)))")
 def test_configuration_cannot_delete_or_fabricate_reputation(self):
  self.check("local c=C.make(1,4);local old=C.read(c);local st=shared.CityProgressionStore;assert(not pcall(st.WriteCommerce,0,c,old,nil));local n=C.model.New(0);assert(not pcall(st.WriteCommerce,0,c,old,n));n=C.model.Copy(old);n.reputation.age=1;n.reputation.cursor=n.reputation.cursor+1;assert(not pcall(st.WriteCommerce,0,c,old,n))")
 def test_reentrant_candidate_read_is_blocked_and_stale_write_rejected(self):
  self.check("local c=C.make(1,3);local st=shared.CityProgressionStore;local setter=Game.SetProperty;local blocked=false;Game.SetProperty=function(o,k,v)if k==T.key(c)then blocked=not pcall(C.read,c)end;return setter(o,k,v)end;C.select(c,'DISTRICT_CAMPUS',true);assert(blocked);assert(not pcall(st.WriteCommerce,0,c,nil,C.model.New(0)))")
 def test_failed_write_isolated_and_cannot_publish_candidate(self):
  for mode in ('drop','third','throw'):
   with self.subTest(mode=mode):self.check("""
local c=C.make(1,3);local other=C.make(2,3);local before=T.encode(T.record(other));local setter=Game.SetProperty
Game.SetProperty=function(o,k,v)
 if k==T.key(c) and v.commerce then
  if '%s'=='drop'then return elseif '%s'=='third'then T.propsSet(k,{bad=true});return else error('write failed')end
 end;return setter(o,k,v)
end
assert(not pcall(C.select,c,'DISTRICT_CAMPUS',true));assert(not pcall(C.read,c))
C.select(other,'DISTRICT_THEATER',true);assert(C.read(other).selected[1]=='DISTRICT_THEATER');assert(T.control(other).potential==3)
"""%(mode,mode))
 def test_final_p4_failure_cannot_publish_reputation_or_replay_start(self):
  self.check("local c=C.make(1,3);local setter=Game.SetProperty;Game.SetProperty=function(o,k,v)if k==T.key(c) and v.commerce and v.commerce.reputation then return end;return setter(o,k,v)end;assert(not pcall(T.invest,c,18001));assert(not T.record(c).commerce);assert(not pcall(C.read,c));T.turn(1);assert(not T.record(c).commerce)")
 def test_existing_p4_repeat_write_does_not_restart_reputation(self):
  self.check("local c=C.make(1,4);T.turn(1);local before=T.encode(C.read(c));local st=shared.CityProgressionStore;local old=st.Investment(0,c);st.WriteInvestment(0,c,old,old);assert(T.encode(C.read(c))==before and C.age(c)==1)")
 def test_mismatched_persisted_owner_holds_record(self):
  self.check("local c=C.make(1,4);T.record(c).commerce.owner=3;T.reload();assert(not pcall(C.read,c))")
 def test_original_owner_return_keeps_age_clears_choices_excludes_foreign_gap(self):
  self.check("local c=C.make(1,4);C.select(c,'DISTRICT_CAMPUS',true);T.turn(1);local st=shared.CityProgressionStore;st.RegisterExit('CommerceTest',function()end);T.loss(c,3,450);assert(T.record(c).commerce.reputation.age==1 and #T.record(c).commerce.selected==0);assert(T.record(c).commerce.reputation.state=='DORMANT_OWNER');T.turn(8);st.ExitConfirmed();c.s.ref.owner=0;c.s.ref.cityID=500;Events.CityTransfered.Fire(0,500,3);assert(C.age(c)==1 and C.read(c).owner==0 and C.read(c).reputation.state=='COUNTING');T.turn(1);assert(C.age(c)==2)")
 def test_completed_reputation_cap_stops_record_writes(self):
  self.check("local c=C.make(1,4);for i=1,40 do T.turn(1)end;assert(C.age(c)==40);local before=T.encode(C.read(c));local writes=T.writes();T.turn(50);assert(T.writes()==writes and T.encode(C.read(c))==before);T.reload();assert(T.writes()==writes and C.age(c)==40)")
 def test_unsupported_speed_does_not_start_reputation_or_block_p4_investment(self):
  self.check("local c=C.make(1,3);C.select(c,'DISTRICT_CAMPUS',true);GameInfo.GameSpeeds.GAMESPEED_QUICK={GameSpeedType='GAMESPEED_QUICK',CostMultiplier=100};GameConfiguration.GetGameSpeedType=function()return 'GAMESPEED_QUICK'end;T.invest(c,19001);assert(T.control(c).potential==4 and not C.read(c).reputation);T.turn(1);assert(not C.read(c).reputation and C.read(c).selected[1]=='DISTRICT_CAMPUS')")
 def test_missing_speed_does_not_start_or_tick_and_does_not_block_potential(self):
  self.check("local c=C.make(1,3);GameConfiguration.GetGameSpeedType=nil;T.invest(c,19001);assert(T.control(c).potential==4 and C.read(c)==nil);C.standard();local other=C.make(2,4);T.turn(1);assert(C.age(other)==1);GameConfiguration.GetGameSpeedType=nil;local before=T.encode(C.read(other));T.turn(1);assert(T.encode(C.read(other))==before and C.age(other)==1)")
 def test_reputation_tick_does_not_visit_cross_record_uniqueness(self):
  self.check("local group={};for i=1,20 do group[i]=C.make(i,4)end;T.scanReset();T.turn(1);assert(T.scanCount()==0);for _,c in ipairs(group)do assert(C.age(c)==1)end")

if __name__=='__main__':unittest.main()
