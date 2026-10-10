"""P0-M1 scoped tests: actual Store, timer, model and UI adapter.

Native queue/event order, synchronous cross-context completion sampling and save
serialization remain a user-game gate. No native yield or performance claim.
"""
from pathlib import Path
import unittest
from lupa.lua55 import LuaRuntime
from test_store_write_boundaries import fixture, run_claim_return_regression, legacy_extension

R = Path(__file__).resolve().parents[1]


def game():
    l = fixture()
    l.execute((R / 'Mod/DialogueProjects.lua').read_text())
    l.execute(r'''
T.start(); oldInfo=P.Info; GameEra='ERA_CLASSICAL'; samples=0; finishes=0; sampleX=1; brokenSample=false
P.Info=function(t,k)
 if t=='Projects' and (k==999 or k=='PROJECT_SPC_ERA_DIALOGUE')then return {Index=999,Hash=1999,ProjectType='PROJECT_SPC_ERA_DIALOGUE'}end
 if t=='Buildings' and (k==998 or k=='BUILDING_SPC_ERA_DIALOGUE_ACCESS')then return {Index=998,InternalOnly=1}end
 if t=='Eras'then return {EraType=GameEra,Name=GameEra}end
 return oldInfo(t,k)
end
P.Call=function(o,k,...)if type(o and o[k])~='function'then return false end;return pcall(o[k],o,...)end
P.HasBuilding=function(b,i)return b.present[i]==true end
P.CreateBuilding=function(q,i)q.c.b.present[i]=true end
P.RemoveBuilding=function(b,i)b.present[i]=nil end
Game.GetEras=function()return {GetCurrentEra=function()return 1 end}end
Game.GetLocalPlayer=function()return 0 end
Locale={Lookup=function(s)return s end}
function city(i,level)
 local c=T.fresh(i);c.b={present={}};c.q={c=c,target='NONE',size=0}
 function c:GetBuildings()return self.b end;function c:GetBuildQueue()return self.q end
 function c:GetName()return 'Fixture '..i end
 function c.q:CurrentlyBuilding()return self.target end;function c.q:GetSize()return self.size end
 function c.q:GetCurrentProductionTypeHash()return self.target=='PROJECT_SPC_ERA_DIALOGUE' and 1999 or 0 end
 function c.q:FinishProgress()
  finishes=finishes+1;if noCompletion then return end
  self.target='NONE';self.size=0
  Events.CityProductionChanged.Fire(0,c:GetID())
  Events.CityProjectCompleted.Fire(0,c:GetID(),999)
  if duplicate then Events.CityProjectCompleted.Fire(0,c:GetID(),999)end
 end
 T.register(c);T.complete(c,'DISTRICT_THEATER')
 for j=2,level or 3 do T.invest(c,10000+i*10+j)end
 return c
end
function sample(pid,id,works)
 local c=assert(Players[pid]:GetCities():FindID(id))
 if works then samples=samples+1;assert(not brokenSample,'injected unavailable sample')end
 return {reference={owner=pid,cityID=id,x=c:GetX(),y=c:GetY()},turn=T.now(),project=c.q.target,size=c.q.size,x=works and sampleX or nil}
end
function bootDialogue()
 ExposedMembers={SPC_P0=shared,SPC_DialogueProjectRead=sample}
 SPCDialogueProjects.Start(P,shared);dp=shared.DialogueProjects
 Events.LoadScreenClose.Fire()
end
function reload()T.reload();bootDialogue()end
function begin(c)
 c.q.target='PROJECT_SPC_ERA_DIALOGUE';c.q.size=1
 Events.CityProductionChanged.Fire(0,c:GetID())
 dp.Request(0,{CityID=c:GetID(),StartTurn=T.now()})
 return T.record(c).dialogue
end
function endturn()Events.PlayerTurnDeactivated.Fire(0);T.turn(1)end
function ledger(c)return T.record(c).dialogue end
function view(c)return dp.views['0:'..c:GetID()]end
function ordinary(c)c.q.target='NORMAL';c.q.size=1;Events.CityProductionChanged.Fire(0,c:GetID())end
c=city(1);control=city(2,1);bootDialogue()
''')
    return l


class DialogueProjects(unittest.TestCase):
    def test_completion_sample_start_era_and_duplicate(self):
        l=game();l.execute(r'''
local other=T.encode(T.record(control));assert(c.b.present[998] and not control.b.present[998])
local v=begin(c);assert(v.pending.era=='ERA_CLASSICAL' and v.total==0)
sampleX=3;GameEra='ERA_MEDIEVAL';duplicate=true;endturn()
v=ledger(c);assert(v.total==15 and v.used.ERA_CLASSICAL.x==3 and not v.used.ERA_MEDIEVAL and not v.pending)
assert(not v.used.ERA_CLASSICAL.forced and samples==1 and finishes==1)
local w=T.writes();Events.CityProjectCompleted.Fire(0,c:GetID(),999);dp.Flush()
assert(T.writes()==w and T.encode(T.record(control))==other)
assert(dp.Describe(0,c):find('本批尚未接入实际产出'))
''')

    def test_zero_consumes_quota_and_same_era_cannot_restart(self):
        l=game();l.execute(r'''
sampleX=0;begin(c);endturn();assert(ledger(c).total==0 and ledger(c).used.ERA_CLASSICAL)
assert(not c.b.present[998]);local before=T.encode(ledger(c));begin(c)
assert(T.encode(ledger(c))==before and not ledger(c).pending and finishes==1)
''')

    def test_interrupt_away_and_back_same_publish_requires_new_turn(self):
        l=game();l.execute(r'''
begin(c);ordinary(c);c.q.target='PROJECT_SPC_ERA_DIALOGUE';Events.CityProductionChanged.Fire(0,c:GetID())
dp.Flush();assert(not ledger(c).pending and not ledger(c).used.ERA_CLASSICAL)
endturn();assert(finishes==0);begin(c);endturn();assert(finishes==1 and ledger(c).total==5)
''')

    def test_known_active_loss_cancels_even_return_in_same_turn(self):
        l=game();l.execute(r'''
begin(c);T.governor(1);Events.GovernorAssigned.Fire(0);T.governor(4);Events.GovernorAssigned.Fire(0);dp.Flush()
assert(not ledger(c).pending and ledger(c).total==0);endturn();assert(finishes==0)
begin(c);endturn();assert(ledger(c).total==5)
''')

    def test_unknown_does_not_delete_or_complete(self):
        l=game();l.execute(r'''
begin(c);local old=P.GovernorGate;P.GovernorGate=function()return 0,c:GetID(),'UNKNOWN',nil end
Events.GovernorAssigned.Fire(0);dp.Flush();assert(ledger(c).pending and view(c).stage=='HELD')
endturn();assert(finishes==0 and ledger(c).pending)
P.GovernorGate=old;dp.Refresh(0,c:GetID());T.turn(0)
assert(not ledger(c).pending and ledger(c).total==0) -- no guessed end-turn proof
''')

    def test_pending_and_committed_cold_load(self):
        l=game();l.execute(r'''
begin(c);local before=T.encode(ledger(c));reload();assert(T.encode(ledger(c))==before)
endturn();assert(ledger(c).total==5 and finishes==1);local w=T.writes();before=T.encode(ledger(c))
reload();T.turn(0);assert(T.encode(ledger(c))==before and T.writes()==w and finishes==1)
''')

    def test_calling_is_never_replayed_after_load(self):
        l=game();l.execute(r'''
noCompletion=true;begin(c);endturn();assert(finishes==1 and ledger(c).pending.stage=='CALLING')
reload();T.turn(0);assert(finishes==1 and ledger(c).total==0)
''')

    def test_completion_unknown_is_not_resampled_later(self):
        l=game();l.execute(r'''
begin(c);brokenSample=true;endturn();assert(ledger(c).pending.stage=='HELD' and ledger(c).total==0)
brokenSample=false;sampleX=7;Events.CityProjectCompleted.Fire(0,c:GetID(),999)
reload();Events.CityProjectCompleted.Fire(0,c:GetID(),999)
assert(ledger(c).pending.stage=='HELD' and ledger(c).total==0 and samples==1)
ordinary(c);dp.Flush();assert(not ledger(c).pending);begin(c);endturn();assert(ledger(c).total==35)
''')

    def test_completion_reference_and_turn_cannot_be_guessed(self):
        for mismatch in ('reference.cityID','reference.owner','turn'):
            with self.subTest(mismatch=mismatch):
                l=game();l.globals().change=mismatch;l.execute(r'''
ExposedMembers.SPC_DialogueProjectRead=function(pid,id,works)
 local v=sample(pid,id,works);if change=='turn'then v.turn=v.turn+1 elseif change=='reference.cityID'then v.reference.cityID=999 else v.reference.owner=5 end;return v
end
begin(c);endturn();assert(ledger(c).total==0 and ledger(c).pending.stage=='HELD')
''')

    def test_forced_native_completion_and_premature_event(self):
        l=game();l.execute(r'''
begin(c);Events.CityProjectCompleted.Fire(0,c:GetID(),999);assert(ledger(c).total==0 and samples==0)
c.q:FinishProgress();assert(ledger(c).total==5 and ledger(c).used.ERA_CLASSICAL.forced)
local w=T.writes();T.turn(0);assert(T.writes()==w and finishes==1)
''')

    def test_actual_store_loss_cancels_pending_retains_history(self):
        l=game();l.execute(r'''
begin(c);endturn();GameEra='ERA_MEDIEVAL';dp.Refresh(0,c:GetID());begin(c)
local token=c.s.values.TOKEN;T.loss(c,3,901)
local r=T.props()[SPCCityProgressionStore.RECORD..token]
assert(r.stage=='HELD_TRANSFER' and r.dialogue.total==5 and not r.dialogue.pending)
assert(r.dialogue.used.ERA_CLASSICAL and not r.dialogue.used.ERA_MEDIEVAL)
assert(not c.b.present[998]);assert(not pcall(shared.CityProgressionStore.DialogueState,3,c))
''')

    def test_corrupt_history_is_held_not_reinitialized(self):
        for mutation in ('r.dialogue=nil','r.dialogue.total=999','r.dialogueKnown=nil','r.dialogue.pending.reference.cityID=999'):
            with self.subTest(mutation=mutation):
                l=game();l.execute('begin(c);r=T.record(c);'+mutation+';T.propsSet(T.key(c),r);reload()')
                l.execute(r'''
assert(not pcall(shared.CityProgressionStore.DialogueState,0,c));assert(not c.b.present[998])
assert(shared.EffectiveFacts.Read(0,control).potential==1 and finishes==0)
''')

    def test_write_failure_before_finish_never_calls_native(self):
        l=game();l.execute(r'''
begin(c);Events.PlayerTurnDeactivated.Fire(0);T.failKey(T.key(c));T.turn(1)
assert(finishes==0 and ledger(c).total==0 and not ledger(c).used.ERA_CLASSICAL)
assert(not pcall(shared.CityProgressionStore.DialogueState,0,c))
assert(shared.EffectiveFacts.Read(0,control).active==1)
''')

    def test_result_write_failure_never_partially_awards_or_replays(self):
        l=game();l.execute(r'''
begin(c);ExposedMembers.SPC_DialogueProjectRead=function(pid,id,works)
 local v=sample(pid,id,works);if works then T.failKey(T.key(c))end;return v
end
endturn();assert(finishes==1 and ledger(c).pending.stage=='CALLING' and ledger(c).total==0 and not ledger(c).used.ERA_CLASSICAL)
T.failKey(nil);reload();Events.PlayerTurnActivated.Fire(0)
assert(finishes==1 and ledger(c).total==0)
''')

    def test_two_cities_and_idle_no_saved_writes_or_collection_scans(self):
        l=game();l.execute(r'''
other=city(3);dp.Refresh(0,other:GetID());begin(c);begin(other);sampleX=2;endturn()
assert(ledger(c).total==10 and ledger(other).total==10 and not ledger(control))
local writes=T.writes();local count=samples
for i=1,30 do Events.GameCoreEventPublishComplete.Fire()end
T.turn(1);assert(T.writes()==writes and samples==count)
''')

    def test_completed_history_unaffected_by_active_loss(self):
        l=game();l.execute(r'''
begin(c);endturn();local saved=T.encode(ledger(c));T.governor(1);Events.GovernorAssigned.Fire(0);dp.Flush()
assert(T.encode(ledger(c))==saved and not c.b.present[998])
T.governor(4);Events.GovernorAssigned.Fire(0);dp.Flush();assert(T.encode(ledger(c))==saved)
''')

    def test_model_identity_exit_no_extra_cap_or_owner_partition(self):
        l=game();l.execute(r'''
local m=SPCDialogueProjectModel;local v=nil;local ref={owner=0,cityID=1,x=2,y=5}
for i=1,20 do v=m.Begin(v,'t',ref,'ERA_TEST_'..i,i);v=m.Complete(v,v.pending.id,7,i)end
assert(v.total==700);v=m.Begin(v,'t',ref,'ERA_NEXT',21)
for _,reason in ipairs({'IDENTITY_EXIT','REALLOCATING','ACTIVE_LOSS'})do
 local cancelled=m.Cancel(v,reason);assert(cancelled.total==700 and not cancelled.pending and not cancelled.used.ERA_NEXT)
end
''')

    def test_failed_commit_then_late_callback_does_not_resample(self):
        l=game();l.execute(r'''
begin(c);ExposedMembers.SPC_DialogueProjectRead=function(pid,id,works)
 local v=sample(pid,id,works);if works then T.failKey(T.key(c))end;return v
end
endturn();T.failKey(nil);reload();sampleX=7;Events.CityProjectCompleted.Fire(0,c:GetID(),999)
assert(samples==1 and ledger(c).total==0 and ledger(c).pending.stage=='HELD')
''')

    def test_second_loss_after_changed_id_removes_owned_state(self):
        l=game();l.execute(r'''
begin(c);endturn();local token=c.s.values.TOKEN;T.loss(c,3,901)
c.s.ref.owner=0;c.s.ref.cityID=1001;Events.CityTransfered.Fire(0,1001,3,901);dp.Flush()
assert(T.record(c).stage=='ACTIVE' and ledger(c).total==5)
GameEra='ERA_MEDIEVAL';dp.Refresh(0,c:GetID());begin(c);T.loss(c,3,902)
assert(not dp.views['0:1001'] and not ledger(c).pending and ledger(c).total==5 and not c.b.present[998])
''')

    def test_user_can_abandon_unconfirmed_completion(self):
        l=game();l.execute(r'''
noCompletion=true;begin(c);endturn();assert(ledger(c).pending.stage=='CALLING')
ordinary(c);dp.Flush();assert(not ledger(c).pending and ledger(c).total==0)
noCompletion=false;begin(c);endturn();assert(ledger(c).total==5)
''')

    def test_existing_claim_load_and_duplicate_groups(self):
        run_claim_return_regression(legacy_extension('test_b127_claim_resume.py'))


if __name__=='__main__':unittest.main()
