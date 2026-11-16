"""PU04 confirmed anchor negatives with real fact guards and effect writers; native doubles only."""
from contextlib import contextmanager
from hashlib import sha256
from pathlib import Path
import os,subprocess,unittest
from unittest.mock import patch
from refactor_harness import ROOT,Context,legacy_source_observation,measure
BASE='a9a0b4371d8f41a128cbf8506a10254c71af4366'
FILES=('CurrentSpecializationFacts','SpecialistSupport','ResearchInfrastructure','ResearchApply','ResearchChair','ResearchCross')
@contextmanager
def profile():
    if os.environ.get('SPC_PU04_BASELINE')!=BASE:yield;return
    old={ROOT/'Mod'/(n+'.lua'):subprocess.check_output(['git','show',BASE+':Mod/'+n+'.lua'],cwd=ROOT).decode()for n in FILES};read=Path.read_text
    with patch.object(Path,'read_text',lambda p,*a,**kw:old[p]if p in old else read(p,*a,**kw)):yield

def research():
    from test_refactor_s6b import real_writers
    with profile(),legacy_source_observation():
        l=real_writers();l.globals().include('SpecialistSupport')
        l.execute("""
        P.Families={DISTRICT_CAMPUS='RESEARCH',DISTRICT_SEOWON='RESEARCH'};P.Family=function(t)return P.Families[t]end
        industrial=addDistrict(c,30,'DISTRICT_INDUSTRIAL_ZONE');setBuildings(industrial,{'BUILDING_IZ_WATER_MILL','BUILDING_WORKSHOP'})
        svc.MarkDirty(0,1);audits()
        function applyValue()local n=0;for bit=0,4 do if c.carriers[GameInfo.Buildings['BUILDING_SPC_RESEARCH_APPLY_PRODUCTION_'..bit].Index]then n=n+2^bit end end;return n end
        function value(name)if name=='ResearchInfrastructure'then return coeff(c)elseif name=='ResearchChair'then return cc('BUILDING_LIBRARY')else return applyValue()end end
        function run(name)shared[name].Audit({player=0,city=1})end
        function change()svc.MarkDirty(0,1);shared.FactChanges.InvalidateCommitted(0,1,{'D'})end
        assert(value('ResearchInfrastructure')==3 and value('ResearchChair')==3 and value('ResearchApply')>0)
        """);return l

def cross():
    from test_refactor_s5d4c1 import actual_cross
    with profile(),legacy_source_observation():
        l=actual_cross();l.globals().include('SpecialistSupport')
        l.execute("""
        local base=shared.EffectiveFacts.Read
        P.Families={DISTRICT_CAMPUS='RESEARCH'};P.Family=function(t)return P.Families[t]end
        shared.CityFlowProbe={SupportFacts=function(pid,c)
         local f=clone(base(pid,c));f.owner=pid;f.cityID=c:GetID();f.token=c.token;f.potential=1;return f
        end}
        shared.CityProgressionStore={Owns=function()return false end,FactStamp=function(pid,c)return c.token..':'..tostring(facts[c.id].active)end}
        P.GovernorGate=function(c)return c.owner,c.id,facts[c.id].active and 'KNOWN'or'UNKNOWN',facts[c.id].active end
        for _,c in pairs(cities)do local get=c.GetProperty;c.GetProperty=function(self,key)
         if key~='SPC_DEV_INVESTMENT_LEDGER_V1'then return get(self,key)end
         local f=shared.CityFlowProbe.SupportFacts(c.owner,c)
         return {schema=1,revision=4,anchor={owner=c.owner,cityID=c.id,token=c.token,first=f.first,specialization=f.specialization},investments={a='a',b='b',c='c'}}
        end end
        """)
        l.globals().include('EffectiveFacts');l.execute("SPCEffectiveFacts.Start(P,shared);f=shared.EffectiveFacts;d.Audit({player=0,city=1});assert(d.plans[0][1] and not d.errors[0][1]);function value()local n=0;for bit=0,15 do if cities[1].built['BUILDING_SPC_RESEARCH_CROSS_POS_'..bit]then n=n+2^bit end end;return n end;assert(value()>0)")
        return l

class ConfirmedNegatives(unittest.TestCase):
    def test_infrastructure_withdraws_confirmed_loss_while_governor_unknown(self):self.check('ResearchInfrastructure')
    def test_apply_withdraws_confirmed_loss_while_governor_unknown(self):self.check('ResearchApply')
    def test_chair_withdraws_confirmed_loss_while_governor_unknown(self):self.check('ResearchChair')
    def check(self,name):
        l=research();l.globals().which=name;l.execute("c.active=nil;d.pillaged=true;change();run(which);assert(value(which)==0,'CONFIRMED_NEGATIVE_HIDDEN_'..which);assert(not shared[which].errors[0][1]);local w=writes;run(which);assert(writes==w)")
    def test_cross_confirmed_loss_does_not_need_other_base_samples(self):
        l=cross();l.execute("facts[1].active=nil;districts[11].pillaged=true;d.samples[0]=nil;f.Invalidate();d.Audit({player=0,city=1});assert(value()==0,'CONFIRMED_NEGATIVE_HIDDEN_CROSS');assert(not d.errors[0][1]);local w=writes;d.Audit({player=0,city=1});assert(writes==w)")
    def test_incomplete_missing_and_reference_mismatch_are_reliably_negative(self):
        for action in ('d.complete=false','c.ds={industrial}','d.type=GameInfo.Districts.DISTRICT_THEATER.Index','d.GetCity=function()return cities[2]end'):
            with self.subTest(action=action):
                l=research();l.execute("c.active=nil;"+action+";change();for _,name in ipairs({'ResearchInfrastructure','ResearchApply','ResearchChair'})do run(name);assert(value(name)==0,'NEGATIVE_WAS_HELD_'..name)end")
    def test_unknown_d_and_workers_do_not_mask_reliable_anchor_negative(self):
        l=research();l.execute("c.active=nil;d.pillaged=true;d.workers=nil;failRead=true;change();for _,name in ipairs({'ResearchInfrastructure','ResearchApply','ResearchChair'})do run(name);assert(value(name)==0)end")

class UnknownAndRecovery(unittest.TestCase):
    def test_intact_or_unreadable_anchor_preserves_old_effects(self):
        for state in ('do end','d.IsPillaged=function()error(\"ANCHOR_READ_FAILED\")end','d.IsComplete=function()return nil end'):
            with self.subTest(state=state):
                l=research();l.execute("c.active=nil;"+state+";change();local w=writes;for _,name in ipairs({'ResearchInfrastructure','ResearchApply','ResearchChair'})do local old=value(name);run(name);assert(value(name)==old and shared[name].errors[0][1])end;assert(writes==w)")
    def test_cross_unknown_anchor_holds_and_later_explicit_recovery_withdraws(self):
        l=cross();l.execute("facts[1].active=nil;local get=districts[11].IsPillaged;districts[11].IsPillaged=function()error('ANCHOR_UNKNOWN')end;local old=value();d.Audit({player=0,city=1});assert(value()==old and d.errors[0][1]);districts[11].IsPillaged=get;districts[11].pillaged=true;f.Invalidate();d.Audit({player=0,city=1});assert(value()==0 and not d.errors[0][1])")
    def test_second_same_turn_repair_remains_unknown_until_level_is_reliable(self):
        l=research();l.execute("c.active=nil;d.pillaged=true;change();for _,name in ipairs({'ResearchInfrastructure','ResearchApply','ResearchChair'})do run(name);assert(value(name)==0)end;d.pillaged=false;change();local w=writes;for _,name in ipairs({'ResearchInfrastructure','ResearchApply','ResearchChair'})do run(name);assert(value(name)==0 and shared[name].errors[0][1])end;assert(writes==w);c.active=4;change();audits();assert(coeff(c)==3 and cc('BUILDING_LIBRARY')==3 and applyValue()>0)")
    def test_unknown_identity_or_ledger_stays_held_without_anchor_guess(self):
        for fault in ('c.factsError=true','c.GetProperty=function()error(\"LEDGER_UNAVAILABLE\")end'):
            with self.subTest(fault=fault):
                l=research();l.execute("c.active=nil;d.pillaged=true;"+fault+";change();local w=writes;for _,name in ipairs({'ResearchInfrastructure','ResearchApply','ResearchChair'})do local old=value(name);run(name);assert(value(name)==old and shared[name].errors[0][1])end;assert(writes==w)")
    def test_mutation_during_negative_read_cannot_commit_stale_withdrawal(self):
        l=research();l.execute("c.active=nil;d.pillaged=true;local get=d.IsPillaged;d.IsPillaged=function()f.Invalidate();return get()end;change();local w=writes;for _,name in ipairs({'ResearchInfrastructure','ResearchApply','ResearchChair'})do local old=value(name);run(name);assert(value(name)==old and shared[name].errors[0][1])end;assert(writes==w)")
    def test_guard_rejects_stale_foundation_reference_before_negative_sampling(self):
        l=research();l.execute("c.active=nil;d.pillaged=true;local source=shared.CityFlowProbe.SupportFacts;shared.CityFlowProbe.SupportFacts=function(pid,city)local v=source(pid,city);v.token=nil;return v end;change();local w=writes;for _,name in ipairs({'ResearchInfrastructure','ResearchApply','ResearchChair'})do run(name);assert(shared[name].errors[0][1])end;assert(writes==w)")

class WorkAndCompatibility(unittest.TestCase):
    def test_fourth_projection_reader_is_forwarded_and_expires(self):
        l=research();l.execute("f.WithPhase('FACADE',function()SPCCurrentSpecializationFacts.Inspect(P,shared,0,c,function(v,w,a)assert(type(a)=='function','ANCHOR_READER_WAS_DROPPED');saved=a end)end);assert(not pcall(saved,{districtID=11,type='DISTRICT_CAMPUS'},function()return {present=false}end))")
    def test_unknown_base_is_not_cached_as_confirmed_across_three_writers(self):
        l=research();l.execute("c.active=nil;change();anchorReads=0;local get=d.IsPillaged;d.IsPillaged=function()anchorReads=anchorReads+1;return get()end;f.WithPhase('RESEARCH_UNKNOWN',function()for _,name in ipairs({'ResearchInfrastructure','ResearchApply','ResearchChair'})do run(name)end end);assert(anchorReads==3,'UNKNOWN_BASE_WAS_CACHED_AS_CONFIRMED');assert(not shared.ResearchInfrastructure.busy and not chair.busy)")
        measure('PU04_unknown_anchor',{'writers':3,'unknown_anchor_state_samples':3,'scope':'UNKNOWN base remains uncached;fresh local samples,not a new partial-fact cache'})
    def test_known_active_path_does_no_new_negative_sampler_work(self):
        l=research();l.execute("local sample=SPCSpecialistSupport.ReadAnchor;local n=0;if sample then SPCSpecialistSupport.ReadAnchor=function(...)n=n+1;return sample(...)end end;for active=1,4 do c.active=active;change();for _,name in ipairs({'ResearchInfrastructure','ResearchApply','ResearchChair'})do run(name);assert(not shared[name].errors[0][1])end end;assert(n==0)")
    def test_one_city_withdrawal_preserves_sibling_and_idle_is_quiet(self):
        l=research();l.execute("local sibling=cc('BUILDING_LIBRARY',cities[2]);c.active=nil;d.pillaged=true;change();chair.Audit({player=0,city=1});assert(cc('BUILDING_LIBRARY')==0 and cc('BUILDING_LIBRARY',cities[2])==sibling);local w,rd=writes,reads;for j=1,1000 do fire('GameCoreEventPublishComplete')end;assert(writes==w and reads==rd)")
    def test_restricted_library_keeps_unknown_negative_semantics(self):
        l=research();l.execute("io=nil;os=nil;debug=nil;require=nil;package=nil;collectgarbage=nil;c.active=nil;d.pillaged=true;change();for _,name in ipairs({'ResearchInfrastructure','ResearchApply','ResearchChair'})do run(name);assert(value(name)==0)end")

class ActualAuthority(unittest.TestCase):
    def make(self):
        from test_refactor_s6c import anchor
        with profile(),legacy_source_observation():
            l=anchor();l.globals().include('DistrictCompleteness');l.globals().include('CurrentSpecializationFacts')
            l.execute("T.invest(c,9401);P.GovernorGate=function()return 0,c:GetID(),'UNKNOWN'end;function negative()return SPCCurrentSpecializationFacts.Inspect(P,shared,0,c,function(v,w,a)return SPCCurrentSpecializationFacts.AnchorUnavailable(P,shared,0,c,v,a)end,true)end")
            return l
    def test_actual_store_same_reference_negative_and_related_restore(self):
        l=self.make();l.execute("missing=true;assert(negative());missing=false;shared.FactChanges.InvalidateCommitted(0,c:GetID(),{'D'});assert(negative()==false)")
    def test_actual_store_commit_during_negative_sample_rejects_old_projection(self):
        l=self.make();l.execute("local complete=d.IsComplete;local once=true;d.IsComplete=function()if once then once=false;T.invest(c,9402)end;return false end;assert(not pcall(negative),'OLD_PARENT_ACCEPTED_NEGATIVE');d.IsComplete=complete;raw.complete=false;assert(negative())")

class KnownMatrix(unittest.TestCase):
    def test_existing_eight_known_level_and_worker_outputs_are_unchanged(self):
        l=research();l.execute("for active=1,4 do for _,workers in ipairs({0,3})do c.active=active;d.workers=workers;change();audits();assert(coeff(c)==(active==4 and workers>0 and 3 or 0));assert(cc('BUILDING_LIBRARY')==(active==4 and workers or 0));assert(applyValue()==(active>=3 and 1 or 0))end end")

if __name__=='__main__':unittest.main()
