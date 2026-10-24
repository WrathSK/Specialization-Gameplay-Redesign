"""S5d1 actual consumer scope/busy proofs, distinct from later native-hook migration."""
import unittest
from refactor_harness import Context,ROOT,TrackedLua51,legacy_source_observation,measure,separate_legacy_event_namespaces
from refactor_defect_fixtures import commerce


def research():
    c=Context();ns={'__file__':str(ROOT/'DevelopmentTests/test_research_chair.py')}
    import lupa.lua55
    lupa.lua55.LuaRuntime=TrackedLua51
    with legacy_source_observation():
        exec(compile(c.prefix('DevelopmentTests/test_research_chair.py','\nchains=[[],'),'chair fixture prefix','exec'),ns)
        ns['LuaRuntime']=TrackedLua51;ns['ns']['LuaRuntime']=TrackedLua51;ns['ns']['ns']['LuaRuntime']=TrackedLua51
        ns['ns']['ns']['FIX']=separate_legacy_event_namespaces(ns['ns']['ns']['FIX'])
        l=ns['runtime'](2)
    l.execute("for _,c in pairs(cities)do setBuildings(c.ds[1],{'BUILDING_LIBRARY','BUILDING_UNIVERSITY'});c.ds[1].workers=3 end;shared.ResearchApply.Audit();chair.Audit();counters={}")
    return l


def cross():
    c=Context();ns={'__file__':str(ROOT/'DevelopmentTests/test_research_cross.py')}
    with legacy_source_observation():
        exec(compile(c.prefix('DevelopmentTests/test_research_cross.py','\nl=runtime();l.execute(r"""\ninitUI();'),'cross fixture prefix','exec'),ns)
        ns['LuaRuntime']=TrackedLua51;ns['FIX']=separate_legacy_event_namespaces(ns['FIX']);l=ns['runtime']()
    l.execute("sync=true;initUI();pulse();assert(d.plans[0][1] and not d.errors[0][1]);function fire(n,...)for _,f in ipairs(hooks[n] or {})do f(...)end end")
    return l


class Kernel(unittest.TestCase):
    def context(self):
        c=Context();c.load('RuntimeWork');c.execute("P={IsTestPlayer=function(p)return p==0 end,Count=function(k)counts[k]=(counts[k]or 0)+1 end,Field=function(t,k)return t[k]end};d={ready=true};seen={};audit,mark,flush=SPCRuntimeWork.NewAudit(P,shared,d,'test',function(s)seen[#seen+1]=s and s.city or 'all';if callback then callback(s)end end)")
        return c
    def test_two_busy_cities_merge_duplicate_and_idle_has_no_work(self):
        c=self.context();c.execute("d.busy=true;audit({player=0,city=1});audit({player=0,city=2});audit({player=0,city=1});d.busy=false;publish();assert(#seen==2 and seen[1]~=seen[2]);for i=1,1000 do publish()end;assert(#seen==2)")
    def test_new_reentry_is_next_snapshot_not_recursive(self):
        c=self.context();c.execute("callback=function(s)if s.city==1 then audit({player=0,city=2})end end;audit({player=0,city=1});assert(#seen==1);publish();assert(#seen==2);publish();assert(#seen==2)")
    def test_failure_does_not_block_sibling_or_rearm_unknown(self):
        c=self.context();c.execute("callback=function(s)if s.city==1 then error('UNKNOWN')end end;mark({player=0,city=1});mark({player=0,city=2});publish();assert(#seen==2 and not d.busy);for i=1,1000 do publish()end;assert(#seen==2)")
    def test_owner_and_global_dominate_only_explicit_scope_and_foreign_zero(self):
        c=self.context();c.execute("mark({player=0,city=1});mark({player=0});mark({player=1,city=1});publish();assert(#seen==1 and seen[1]=='all');mark({player=0,city=1});mark();publish();assert(#seen==2 and seen[2]=='all')")
    def test_observer_or_unprintable_error_cannot_latch_busy_or_flush(self):
        c=self.context();c.execute("P.Observe=function()error('DIAGNOSTIC_FAILURE')end;callback=function()error(setmetatable({},{__tostring=function()error('BAD_TOSTRING')end}))end;mark({player=0,city=1});publish();assert(not d.busy and d.auditError=='RUNTIME_AUDIT_FAILED');callback=nil;mark({player=0,city=2});publish();assert(#seen==2 and not d.auditError)")
    def test_load_reset_and_bounded_scope(self):
        c=self.context();c.execute("mark({player=0,city=1});Events.LoadScreenClose.Fire();assert(not flush() and #seen==0);local ok=true;for id=1,2050 do if not pcall(mark,{player=0,city=id})then ok=false;break end end;assert(not ok)")


class Writers(unittest.TestCase):
    def test_actual_apply_chair_one_city_keeps_sibling_carriers_errors(self):
        l=research();l.execute("""
        local sibling=cc('BUILDING_LIBRARY',cities[2]);chair.errors[0][2]='KEEP_CHAIR';shared.ResearchApply.errors[0][2]='KEEP_APPLY'
        local get=cities[2].GetBuildings;cities[2].GetBuildings=function()error('UNRELATED_CITY_TOUCHED')end
        cities[1].ds[1].workers=1;chair.Audit({player=0,city=1});shared.ResearchApply.Audit({player=0,city=1})
        assert(counters.city_scan==2 and chair.errors[0][2]=='KEEP_CHAIR' and shared.ResearchApply.errors[0][2]=='KEEP_APPLY')
        cities[2].GetBuildings=get;assert(cc('BUILDING_LIBRARY')==1 and cc('BUILDING_LIBRARY',cities[2])==sibling)
        """)
        measure('S5d1_two_actual_writers_known_city',{'writers':2,'city_visits':2,'unrelated_city_visits':0})
    def test_actual_chair_unknown_holds_and_real_new_cause_recovers(self):
        l=research();l.execute("local old=cc('BUILDING_LIBRARY');c.active=nil;chair.Audit({player=0,city=1});assert(cc('BUILDING_LIBRARY')==old and chair.errors[0][1]);local n=reads;for i=1,1000 do fire('GameCoreEventPublishComplete')end;assert(reads==n);c.active=4;c.ds[1].workers=2;chair.Audit({player=0,city=1});assert(cc('BUILDING_LIBRARY')==2 and not chair.errors[0][1])")
    def test_actual_chair_busy_second_city_retained_until_publish(self):
        l=research();l.execute("local get=cities[1].GetBuildings;local once=true;cities[1].GetBuildings=function()if once then once=false;cities[2].ds[1].workers=1;chair.Audit({player=0,city=2})end;return get()end;chair.Audit({player=0,city=1});assert(cc('BUILDING_LIBRARY',cities[2])==3);fire('GameCoreEventPublishComplete');assert(cc('BUILDING_LIBRARY',cities[2])==1 and not chair.busy)")
    def test_actual_cross_scoped_plan_and_error_are_not_globally_replaced(self):
        l=cross();l.execute("local sibling={state='KEEP'};d.plans[0][2]=sibling;d.errors[0][2]='KEEP';d.Audit({player=0,city=1});assert(d.plans[0][2]==sibling and d.errors[0][2]=='KEEP');factUnknown=true;local w=writes;d.Audit({player=0,city=1});assert(writes==w and d.errors[0][1] and d.plans[0][2]==sibling);factUnknown=false;d.Audit({player=0,city=1});assert(not d.errors[0][1] and d.plans[0][1] and d.plans[0][2]==sibling)")
    def test_actual_cross_busy_cause_is_processed_once(self):
        l=cross();l.execute("local get=cities[1].GetBuildings;local once=true;visits=0;local observe=P.Observe;P.Observe=function(k,n)if k=='audit' and n=='ResearchCross'then visits=visits+1 end;if observe then observe(k,n)end end;cities[1].GetBuildings=function()if once then once=false;d.Audit({player=0,city=1})end;return get()end;d.Audit({player=0,city=1});assert(visits==1);fire('GameCoreEventPublishComplete');assert(visits==2);for i=1,1000 do fire('GameCoreEventPublishComplete')end;assert(visits==2)")
    def test_actual_apply_chair_owner_read_failure_is_city_isolated(self):
        for name in ('ResearchApply','ResearchChair'):
            l=research();l.execute("local m=shared['"+name+"'];local get=cities[1].GetOwner;cities[1].GetOwner=function()error('OWNER_TEMPORARILY_UNREADABLE')end;local collection=Players[0].GetCities;Players[0].GetCities=function()local cs=collection();cs.Members=function()return ipairs(cities)end;return cs end;m.errors[0][2]='OLD';cities[2].ds[1].workers=1;m.Audit({player=0});assert(m.errors[0][1] and not m.errors[0][2] and not m.definitionError);cities[1].GetOwner=get;m.Audit({player=0,city=1});assert(not m.errors[0][1])")
    def test_actual_cross_owner_read_failure_is_city_isolated(self):
        l=cross();l.execute("local get=cities[1].GetOwner;cities[1].GetOwner=function()error('OWNER_TEMPORARILY_UNREADABLE')end;local collection=Players[0].GetCities;Players[0].GetCities=function()local cs=collection();cs.Members=function()return ipairs(cities)end;return cs end;d.Audit({player=0});assert(d.errors[0][1] and d.plans[0][2] and not d.errors[0].player);cities[1].GetOwner=get;d.Audit({player=0,city=1});assert(d.plans[0][1] and not d.errors[0][1])")
    def test_commerce_busy_changed_set_preserves_reverse_dependent_sources(self):
        l=commerce();l.execute("""
        assert(toggle(2,'DISTRICT_CAMPUS',true));local old=ownedGold(cities[2]);local get=cities[2].GetYield;local once=true
        cities[2].GetYield=function(self,y)if once then once=false;cities[1].yields.SCIENCE=1000;com.Audit({player=0,changed={[1]=true}})end;return get(self,y)end
        com.Audit({player=0,city=2});assert(ownedGold(cities[2])==old);Events.GameCoreEventPublishComplete.Fire();assert(ownedGold(cities[2])>old)
        local n=commerceWrites;for i=1,1000 do Events.GameCoreEventPublishComplete.Fire()end;assert(commerceWrites==n)
        """)

class Aesthetic(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        import test_culture_aesthetic as ae
        import test_culture_meaning_probe as legacy
        ae.LuaRuntime=TrackedLua51;cls.sql=legacy.database() # exact test-owned definitions rebuilt only in disposable memory
    @classmethod
    def tearDownClass(cls):cls.sql.close()
    def fixture(self):
        import test_culture_aesthetic as ae
        from unittest.mock import patch
        helper=ae.AestheticTests();helper.sql=self.sql
        # Historical fixture omitted this live boundary; add only a native event double.
        with legacy_source_observation(),patch.object(ae,'FIX',ae.FIX+"\nEvents.GameCoreEventPublishComplete={list={}};Events.GameCoreEventPublishComplete.Add=function(f)table.insert(Events.GameCoreEventPublishComplete.list,f)end"):
            return helper.runtime()
    def test_actual_aesthetic_busy_city_changed_after_current_plan_is_not_lost(self):
        l=self.fixture();l.execute("""
        local old=total(b);local setter=P.SetProperty;local once=true
        P.SetProperty=function(...)if once then once=false;b.eras=4;data.Audit({player=0,city=2})end;return setter(...)end
        a.eras=3;one();assert(total(b)==old);fire('GameCoreEventPublishComplete');assert(total(b)==24)
        local n=writes;for i=1,1000 do fire('GameCoreEventPublishComplete')end;assert(writes==n and not data.busy)
        """)
    def test_actual_aesthetic_scoped_unknown_keeps_sibling_and_recovers(self):
        l=self.fixture();l.execute("local old=total(a);data.errors['0:2']='KEEP';a.worksUnknown=true;one();assert(total(a)==old and data.errors['0:2']=='KEEP');a.worksUnknown=false;a.eras=4;one();assert(total(a)==24 and data.errors['0:2']=='KEEP')")

if __name__=='__main__':unittest.main()
