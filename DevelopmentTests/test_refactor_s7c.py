"""D6 only: reliable boundaries recover without credit for unproved intervals."""
from contextlib import contextmanager,nullcontext
from hashlib import sha256
from pathlib import Path
import subprocess
import ast
import unittest
from unittest.mock import patch
from refactor_harness import Context,ROOT,TrackedLua51,SOURCES,legacy_source_observation,measure
from test_refactor_s5d4c7 import fixture as tradition
from test_refactor_s5d4c10 import fixture as commerce
import test_store_write_boundaries as city
import test_b239_commerce_store as commerce_store
import test_b239_commerce as old_commerce
import test_culture_network as old_network

BASE='afd2204'
@contextmanager
def history():
    previous=Path.read_text;execute=TrackedLua51.execute
    originals={ROOT/'Mod'/(n+'.lua'):subprocess.check_output(['git','show',BASE+':Mod/'+n+'.lua'],cwd=ROOT,text=True)for n in ('ResearchTradition','CommerceModel','CityProgressionStore','Commerce')}
    digests={sha256(s.encode()).hexdigest():'historical/'+BASE+'/'+str(p.relative_to(ROOT))for p,s in originals.items()}
    def read(p,*a,**kw):return originals[p]if p in originals else previous(p,*a,**kw)
    def run(vm,s,*a,**kw):
        h=sha256(s.encode()).hexdigest()if isinstance(s,str)else None
        if h in digests:SOURCES[h]=digests[h]
        return execute(vm,s,*a,**kw)
    with patch.object(Path,'read_text',read),patch.object(TrackedLua51,'execute',run),legacy_source_observation():yield

def pure():
    l=TrackedLua51(unpack_returned_tuples=True);l.globals().include=lambda n:l.execute((ROOT/'Mod'/(n+'.lua')).read_text())
    with legacy_source_observation():
        l.globals().include('ResearchTradition');l.globals().include('CommerceModel')
    return l

def store():
    with patch.object(city,'LuaRuntime',TrackedLua51),legacy_source_observation():return commerce_store.runtime()

class Boundaries(unittest.TestCase):
    def test_normal_complete_interval_duplicate_and_identity_pause_are_unchanged(self):
        values=[]
        for old in (True,False):
            with history()if old else nullcontext():l=pure()
            l.execute("""
            local R,C=SPCResearchTradition,SPCCommerceModel
            r=R.Begin(5,'P4');v=C.BeginReputation(C.New(0),5,'P4')
            for t=5,50 do r=R.Advance(r,t,'RESEARCH');v=C.Advance(v,t,'COMMERCE')end
            assert(r.age==45 and v.reputation.age==40)
            r=R.Advance(r,50,'CULTURE');r=R.Advance(r,51,'CULTURE');r=R.Advance(r,52,'RESEARCH');r=R.Advance(r,53,'RESEARCH');assert(r.age==46)
            v=C.Advance(v,50,'RESEARCH');assert(not v.reputation and #v.selected==0)
            """)
            def plain(v):return {k:plain(x)for k,x in v.items()}if hasattr(v,'items')else v
            values.append((plain(l.globals().r),plain(l.globals().v)))
        self.assertEqual(*values)
    def test_gap_rebases_current_boundary_without_backfill_then_next_interval_counts(self):
        l=pure();l.execute("""
        local R,C=SPCResearchTradition,SPCCommerceModel
        local r=R.Advance(R.Begin(5,'P4'),8,'RESEARCH');assert(r.age==0 and r.cursor==8 and r.state=='COUNTING');r=R.Advance(r,9,'RESEARCH');assert(r.age==1)
        local v=C.Advance(C.BeginReputation(C.New(0),5,'P4'),8,'COMMERCE');assert(v.reputation.age==0 and v.reputation.cursor==8 and v.reputation.state=='COUNTING');v=C.Advance(v,9,'COMMERCE');assert(v.reputation.age==1)
        assert(not pcall(R.Advance,r,8,'RESEARCH')and not pcall(C.Advance,v,8,'COMMERCE'))
        """)
    def test_old_UNKNOWN_resumes_but_owner_holds_remain_independent(self):
        l=pure();l.execute("""
        local R,C=SPCResearchTradition,SPCCommerceModel
        local r=R.Begin(5,'P4');r.state='UNKNOWN_INTERVAL';r=R.Advance(r,8,'CULTURE');assert(r.age==0 and r.cursor==8 and r.state=='PAUSED_IDENTITY')
        r.state='OWNER_POLICY_UNRESOLVED';r=R.Advance(r,10,'RESEARCH');assert(r.age==0 and r.cursor==8 and r.state=='OWNER_POLICY_UNRESOLVED')
        local v=C.BeginReputation(C.New(0),5,'P4');v.reputation.state='UNKNOWN_INTERVAL';v=C.Advance(v,8,'COMMERCE');assert(v.reputation.age==0 and v.reputation.state=='COUNTING');v=C.OwnerChanged(v,3,9);v=C.Advance(v,12,'COMMERCE');assert(v.reputation.cursor==9 and v.reputation.state=='DORMANT_OWNER')
        """)
    def test_unknown_at_cap_recovers_once_and_counting_cap_remains_noop(self):
        l=pure();l.execute("local C=SPCCommerceModel;local v=C.BeginReputation(C.New(0),0,'P4');v.reputation.age=40;v.reputation.cursor=40;v.reputation.state='UNKNOWN_INTERVAL';v=C.Advance(v,45,'COMMERCE');assert(v.reputation.age==40 and v.reputation.cursor==45 and v.reputation.state=='COUNTING');v=C.Advance(v,99,'COMMERCE');assert(v.reputation.cursor==45 and v.reputation.age==40)")

class RealStore(unittest.TestCase):
    def test_two_research_cities_temporary_missing_boundary_no_backfill_then_normal_and_idle(self):
        l=tradition();l.execute("""
        local find=CityManager.GetCityAt;local receipt=T.snapshot(c).researchTradition.receipt
        CityManager.GetCityAt=function(x,y)if x==c:GetX()and y==c:GetY()then return nil end;return find(x,y)end
        T.turn(1);pp();assert(T.snapshot(c).researchTradition.age==0 and T.snapshot(other).researchTradition.age==1)
        CityManager.GetCityAt=find;T.turn(1);pp();local r=T.snapshot(c).researchTradition;assert(r.age==0 and r.cursor==T.now()and r.state=='COUNTING'and current(c)==5);assert(T.snapshot(other).researchTradition.age==2)
        T.turn(1);pp();assert(T.snapshot(c).researchTradition.age==1 and T.snapshot(c).researchTradition.receipt==receipt and T.snapshot(other).researchTradition.age==3)
        local writes=T.writes();for i=1,1000 do pp()end;assert(T.writes()==writes)
        """)
        measure('S7c_research_recovery',{'actual':'Store/FactChanges/FactBindings/ResearchEffects','unreliable_intervals_credited':0,'first_complete_interval_after_rebase':1,'sibling_continues':True,'thousand_idle_history_writes':0})
    def test_commerce_unavailable_city_boundary_recovers_and_cap40_stops_writes(self):
        l=store();l.execute("""
        T.start();C.standard();c=C.make(1,4);other=C.make(2,4);local find=CityManager.GetCityAt
        CityManager.GetCityAt=function(x,y)if x==c:GetX()and y==c:GetY()then return nil end;return find(x,y)end
        T.turn(1);assert(C.age(c)==0 and C.age(other)==1);CityManager.GetCityAt=find;T.turn(1);assert(C.age(c)==0 and C.read(c).reputation.cursor==T.now()and C.age(other)==2)
        T.turn(1);assert(C.age(c)==1 and C.age(other)==3)
        for i=1,39 do T.turn(1)end;assert(C.age(c)==40)
        local writes=T.writes();T.turn(50);assert(C.age(c)==40 and T.writes()==writes)
        """)
    def test_cold_old_UNKNOWN_at_cap_rebases_without_fabricated_age_or_repeated_writes(self):
        l=store();l.execute("T.start();C.standard();c=C.make(1,4);for i=1,40 do T.turn(1)end;local receipt=C.read(c).reputation.receipt;T.record(c).commerce.reputation.state='UNKNOWN_INTERVAL';local writes=T.writes();T.reload();assert(C.age(c)==40 and C.read(c).reputation.state=='COUNTING'and C.read(c).reputation.receipt==receipt and T.writes()==writes+1);writes=T.writes();T.turn(4);T.reload();assert(T.writes()==writes and C.age(c)==40)")
    def test_speed_unreadable_gap_never_credits_and_then_normal_interval_does(self):
        l=store();l.execute("T.start();C.standard();c=C.make(1,4);GameConfiguration.GetGameSpeedType=nil;T.turn(1);assert(C.age(c)==0);C.standard();T.turn(1);assert(C.age(c)==0 and C.read(c).reputation.state=='COUNTING');T.turn(1);assert(C.age(c)==1)")
    def test_recovered_store_tick_commits_before_projection_and_never_synthesizes_origin(self):
        l=tradition();l.execute("T.turn(3);pp();assert(T.snapshot(c).researchTradition.age==0 and current(c)==5);T.turn(1);pp();assert(T.snapshot(c).researchTradition.age==1);T.record(c).researchTradition=nil;T.reload();assert(shared.CityProgressionStore.ReadTradition(0,c)==nil)")

    def test_bounded_rebase_diagnostic_is_session_only_and_readonly(self):
        l=tradition();l.execute("T.turn(3);pp();local s=shared.CityProgressionStore;local text=s.Describe(0,c);assert(text:find('计龄跳过')and text:find('科研 1次',1,true));T.turn(3);pp();text=s.NativeDescribe(0,c);assert(text:find('科研 2次',1,true));local writes=T.writes();for i=1,100 do s.Describe(0,c)end;assert(T.writes()==writes);T.reload();assert(not shared.CityProgressionStore.Describe(0,c):find('计龄跳过')and T.writes()==writes)")
    def test_failed_tick_is_held_without_automatic_replay_while_sibling_continues(self):
        l=store();l.execute("T.start();C.standard();c=C.make(1,4);other=C.make(2,4);local set=Game.SetProperty;local key=T.key(c);attempts=0;Game.SetProperty=function(o,k,v)if k==key and v.commerce and v.commerce.reputation.age>0 then attempts=attempts+1;error('TICK_WRITE_FAILURE')end;return set(o,k,v)end;T.turn(1);assert(attempts==1 and not pcall(C.read,c)and C.age(other)==1);T.turn(1);assert(attempts==1 and C.age(other)==2)")

class ActualPropagation(unittest.TestCase):
    def test_real_Store_reputation_commit_drives_real_Commerce_without_direct_turn_mark(self):
        from test_refactor_s6f import development
        l=development();l.execute("""
        for i=1,20 do T.turn(1)end
        assert(shared.CityProgressionStore.CommerceState(0,source).value.reputation.age==20)
        local dc=shared.DistrictCompleteness
        T.record(source).commerce.reputation.state='UNKNOWN_INTERVAL'
        local speed=GameConfiguration.GetGameSpeedType
        -- Test cold seed only: suppress the existing load tick before consumer attach.
        GameConfiguration.GetGameSpeedType=function()return 'GAMESPEED_QUICK'end
        T.reload();GameConfiguration.GetGameSpeedType=speed
        shared.DistrictCompleteness=dc;shared.NetworkBridge={};SPCFactChanges.New(shared);f=shared.EffectiveFacts
        assert(shared.CityProgressionStore.CommerceState(0,source).value.reputation.state=='UNKNOWN_INTERVAL')
        """)
        tree=ast.parse((ROOT/'DevelopmentTests/test_refactor_s6f.py').read_text())
        fn=next(n for n in tree.body if isinstance(n,ast.FunctionDef)and n.name=='combined')
        adapters=next(n.value.args[0].value for n in fn.body if isinstance(n,ast.Expr)and isinstance(n.value,ast.Call)and isinstance(n.value.func,ast.Attribute)and n.value.func.attr=='execute')
        with legacy_source_observation():l.globals().include('Commerce')
        l.execute(adapters);l.execute("""
        local cid=source:GetID();local fc=shared.FactChanges
        function pulse()fc.Flush();Events.GameCoreEventPublishComplete.Fire()end
        pulse();assert(com.views['0:'..cid].reputation.effective==0 and gold()==15)
        local receipt=shared.CityProgressionStore.CommerceState(0,source).value.reputation.receipt;seen=0
        fc.RegisterConsumer('CaptureReputation',function(e)if e.causes.REPUTATION_COMMITTED then seen=seen+1;assert(e.player==0 and e.city==cid and e.topics.COMMERCE)end end,{kinds={'HISTORY'},topics={'COMMERCE'}})
        local mark=com.Mark;com.Mark=function()end;T.turn(1);com.Mark=mark
        local v=shared.CityProgressionStore.CommerceState(0,source).value.reputation
        assert(v.state=='COUNTING'and v.age==20 and v.cursor==T.now()and v.receipt==receipt and fc.pending>0)
        Events.GameCoreEventPublishComplete.Fire();assert(gold()==15 and com.views['0:'..cid].reputation.effective==0 and seen==0)
        fc.Flush();assert(seen==1);Events.GameCoreEventPublishComplete.Fire()
        assert(com.views['0:'..cid].stage=='READY'and com.views['0:'..cid].reputation.effective==20 and gold()==16)
        local writes=T.writes();local effect=com.writes;for i=1,1000 do pulse()end;assert(T.writes()==writes and com.writes==effect and seen==1)
        T.turn(1);pulse();assert(shared.CityProgressionStore.CommerceState(0,source).value.reputation.age==21)
        """)
        measure('S7c_actual_Store_Commerce_propagation',{'actual':'Store/EF/FactChanges/Commerce','native_doubles':'D/Bridge/worker/yield','unknown_gold':15,'recovered_gold':16,'retained_age':20,'next_complete_age':21,'typed_commits_consumed':1,'direct_turn_mark_suppressed_for_proof':True,'thousand_idle_writes':0})

class CommerceFallback(unittest.TestCase):
    def test_missing_start_keeps_confirmed_base_Gold_and_does_not_fabricate_history(self):
        l=commerce();l.execute("local writes=commerceWrites;cities[2].potential=4;cities[2].active=4;com.SourceChanged(0,2);assert(view(2).stage=='READY'and view(2).reputation.effective==0 and ownedGold(cities[2])==15 and commerceStates[2].reputation==nil and commerceWrites==writes)")
    def test_unknown_reputation_keeps_base_then_confirmed_history_restores_only_bonus(self):
        l=commerce();l.execute("cities[2].potential=4;cities[2].active=4;commerceStates[2].reputation={version=1,start=0,cursor=20,age=20,receipt='P4',state='UNKNOWN_INTERVAL'};com.SourceChanged(0,2);assert(view(2).stage=='READY'and ownedGold(cities[2])==15 and view(2).reputation.effective==0);local writes=commerceWrites;commerceStates[2].reputation.state='COUNTING';com.SourceChanged(0,2);assert(ownedGold(cities[2])==16 and view(2).reputation.effective==20 and commerceWrites==writes)")
    def test_malformed_history_stays_strict_and_no_new_eligibility_is_inferred(self):
        l=commerce();l.execute("cities[2].potential=4;cities[2].active=4;commerceStates[2].reputation={version=1,start=0,cursor=20,age=99,receipt='P4',state='UNKNOWN_INTERVAL'};com.SourceChanged(0,2);assert(view(2).stage=='HELD');commerceStates[2].reputation=nil;cities[2].active=nil;com.SourceChanged(0,2);assert(view(2).stage=='HELD')")

class FrozenD6(unittest.TestCase):
    def test_pre_D6_unknown_cases_remain_frozen_on_exact_base_source(self):
        with history(),patch.object(commerce_store,'LuaRuntime',TrackedLua51),patch.object(old_network,'LuaRuntime',TrackedLua51),legacy_source_observation():
            commerce_store.Model().test_unknown_gap_is_held_not_backfilled()
            case=old_commerce.Commercialization();case.test_unprovable_p4_start_is_not_fabricated();case.test_unknown_reputation_interval_does_not_claim_a_complete_current_iv_value()
            l=tradition();l.execute("T.turn(2);pp();assert(T.snapshot(c).researchTradition.state=='UNKNOWN_INTERVAL'and current(c)==0)")
        measure('S7c_frozen_D6_before',{'base':BASE,'superseded':'absorbing UNKNOWN and whole-Commerce HELD only','original_assertions_unchanged':True})

class RetainedStore(unittest.TestCase):pass
for _name in dir(commerce_store.Store):
    if _name.startswith('test_'):
        def run(self,name=_name):
            with patch.object(city,'LuaRuntime',TrackedLua51),legacy_source_observation():getattr(commerce_store.Store(),name)()
        setattr(RetainedStore,_name,run)

if __name__=='__main__':unittest.main()
