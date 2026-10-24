"""S5a2a committed Store/declared observer/freshness integration. Actual Lua51."""
import unittest
from refactor_harness import Context,TrackedLua51,legacy_source_observation,ROOT
from refactor_defect_fixtures import startup,commerce


def actual_store():
    import test_store_write_boundaries as module
    module.LuaRuntime=TrackedLua51
    with legacy_source_observation(): l=module.fixture()
    l.execute((ROOT/'Mod/FactChanges.lua').read_text())
    l.execute("local start=SPCCityProgressionStore.Start;SPCCityProgressionStore.Start=function(P,s,legacy)SPCFactChanges.New(s);return start(P,s,legacy)end")
    return l


class CommittedStore(unittest.TestCase):
    def test_actual_identity_investment_receipt_and_three_stage_commit(self):
        l=actual_store();l.execute("""
        T.start();c=T.fresh(1);T.register(c);T.complete(c,'DISTRICT_CAMPUS');local changes=shared.FactChanges
        assert(changes.pending==1);got={};changes.RegisterConsumer('proof',function(e)got[#got+1]=e end,{kinds={'POTENTIAL'}})
        changes.Flush();got={};local n=T.writes();local receipt=T.invest(c,2001)
        assert(fixtureStats().kills==1 and T.writes()-n==3 and #got==0 and changes.pending==1)
        changes.Flush();assert(#got==1 and got[1].investment.receipt==receipt and got[1].investment.unitUID)
        local proof=got[1].investment;assert(proof.revision==2 and proof.player==0 and proof.city==101)
        assert(proof.anchor.token==T.snapshot(c).base.token and proof.reference.x==c:GetX())
        local count=#got;changes.Flush();assert(#got==count and fixtureStats().kills==1)
        """)
    def test_same_turn_second_commit_coalesces_final_proof_and_preserves_history(self):
        l=actual_store();l.execute("""
        T.start();c=T.fresh(1);T.register(c);T.complete(c,'DISTRICT_CAMPUS');local changes=shared.FactChanges
        changes.Flush();got={};changes.RegisterConsumer('proof',function(e)got[#got+1]=e end,{kinds={'POTENTIAL'}})
        T.invest(c,2001);changes.Flush();T.invest(c,2002);local last=T.invest(c,2003)
        changes.Emit({owner=0,cityID=101,reference='0:101:2:5:'..T.snapshot(c).base.token,kinds={'HISTORY'},topic='TEMPLATES',cause='TEMPLATE_COMMITTED',revision=999})
        changes.Flush();assert(#got==2 and got[1].investment.revision==2 and got[2].investment.revision==4)
        assert(got[2].investment.receipt==last and got[2].topics.TEMPLATES)
        assert(T.snapshot(c).researchTradition.receipt==last and fixtureStats().kills==3)
        """)
    def test_notification_failure_never_reverses_committed_record_or_consumption(self):
        l=actual_store();l.execute("""
        T.start();c=T.fresh(1);T.register(c);T.complete(c,'DISTRICT_CAMPUS')
        shared.FactChanges.Emit=function()error('OBSERVER_AFTER_COMMIT')end
        local receipt=T.invest(c,2001);assert(fixtureStats().kills==1 and T.snapshot(c).investment.investments[receipt])
        assert(shared.PermanentWriteObserverError:find('OBSERVER_AFTER_COMMIT') and shared.FactChanges.Generation(0,'NETWORK')>0)
        """)
    def test_real_store_two_cities_scope_and_loaded_context_new_registry(self):
        l=actual_store();l.execute("""
        x,y=T.two();local changes=shared.FactChanges;changes.Flush();got={}
        changes.RegisterConsumer('proof',function(e)got[#got+1]=e end,{kinds={'POTENTIAL'}})
        local before=T.snapshot(y);T.invest(x,2001);changes.Flush();assert(#got==1 and got[1].city==x:GetID())
        assert(T.snapshot(y).revision==before.revision)
        local old=changes;T.reload();assert(shared.FactChanges~=old and shared.FactChanges.pending==0)
        """)

    def test_actual_banner_observer_publishes_new_investment_level(self):
        l=actual_store();l.execute("""
        T.start();P.Field=function(t,k)return t[k]end
        """)
        l.globals().include('LevelBannerState');l.execute("""
        SPCLevelBannerState.Start(P,shared);c=T.fresh(1);T.register(c);T.complete(c,'DISTRICT_CAMPUS')
        shared.FactChanges.Flush();Events.GameCoreEventPublishComplete.Fire();assert(shared.LevelBanners.views['0:101'].potential==1)
        T.invest(c,2001);assert(shared.LevelBanners.views['0:101'].potential==1)
        shared.FactChanges.Flush();Events.GameCoreEventPublishComplete.Fire();assert(shared.LevelBanners.views['0:101'].potential==2 and shared.LevelBanners.views['0:101'].active==2)
        """)
    def test_actual_store_and_capital_reject_before_rng_intent_and_debit(self):
        import test_b241_capital as fixture
        l=actual_store();l.globals().include('CapitalInvestment');l.execute(fixture.SETUP)
        l.execute("""
        local changes=shared.FactChanges;local captured=changes.Generation(0,'COMMERCE')
        -- Explicit already-published Commerce projection double. The real Commerce
        -- proof implementation is exercised separately with the actual Bridge.
        shared.Commerce.TransactionCurrent=function()return captured==changes.Generation(0,'COMMERCE')end
        cap.Refresh(0,source:GetID());assert(C.view().canSign)
        changes.Emit=function()error('OBSERVER_FAILED')end
        local priorKills=fixtureStats().kills;T.invest(research,99001);local before=T.writes();local balanceBefore=balance
        assert(not C.confirm(nil,'VENTURE'));assert(rolls==0 and moneyCalls==0 and balance==balanceBefore and T.writes()==before)
        assert(not C.state() and fixtureStats().kills==priorKills+1 and changes.Generation(0,'COMMERCE')~=captured)
        """)

class Wiring(unittest.TestCase):
    def test_actual_composition_factory_and_original_order_and_independent_seal(self):
        c=startup();c.load('Gameplay');c.execute("local s=ExposedMembers.SPC_P0;assert(s.FactChanges and s.StartStatus.FactChanges.state=='OK');assert(s.StartStatus.CityProgressionStore.state=='OK');s.FactChanges.RegisterConsumer('test',function()seen=(seen or 0)+1 end,{kinds={'ACTIVE'}});s.FactChanges.Emit({owner=0,cityID=1,kinds={'ACTIVE'},cause='COMMITTED'});assert(seen==nil);publish();assert(seen==1 and sealed)")
    def test_factory_failure_skips_actual_store_dependency_but_epilogue_survives(self):
        c=startup();original=c.globals().include
        def load(name):
            result=original(name)
            if name=='FactChanges':c.execute("SPCFactChanges.New=function()error('FACT_FACTORY_FAILED')end")
            return result
        c.globals().include=load;c.load('Gameplay');c.execute("local s=ExposedMembers.SPC_P0;assert(s.StartStatus.FactChanges.state=='FAILED' and s.StartStatus.CityProgressionStore.state=='SKIPPED_DEPENDENCY' and sealed)")
    def test_production_eight_observers_no_filename_chain_and_independent_wonder(self):
        names=['ClaimProjects','IndustrySupport','EngineeringStudyProjects','CrewProjects','Commerce','DevelopmentInvestment','Restructuring','LevelBannerState','IndustryWonderEffects']
        for name in names:
            text=(ROOT/'Mod'/f'{name}.lua').read_text();self.assertNotIn('SPCSafeCallbacks.Chain(',text);self.assertIn('FactChanges.RegisterConsumer',text)
        self.assertNotIn('OnPermanentCityWrite',(ROOT/'Mod/CityProgressionStore.lua').read_text())

class Freshness(unittest.TestCase):
    def test_immediate_invalidation_zero_native_and_unrelated_history_unchanged(self):
        c=Context();c.load('FactChanges');c.execute("d=SPCFactChanges.New(shared);native=0;Players=setmetatable({},{__index=function()native=native+1;error('NATIVE')end});d.Emit({owner=0,cityID=1,kinds={'ACTIVE'},cause='COMMITTED'});assert(d.Generation(0,'NETWORK')==1 and d.Generation(0,'COMMERCE')==1 and native==0);d.Emit({owner=0,cityID=1,kinds={'HISTORY'},topic='DIALOGUE',cause='HISTORY_COMMITTED'});assert(d.Generation(0,'NETWORK')==1 and d.Generation(0,'COMMERCE')==1)")
    def test_actual_bridge_and_commerce_block_pre_publish_then_proved_refresh(self):
        l=commerce();l.execute((ROOT/'Mod/FactChanges.lua').read_text());l.execute("""
        local changes=SPCFactChanges.New(shared);assert(toggle(2,'DISTRICT_CAMPUS',true));assert(com.TransactionCurrent(0,2))
        local n=created+removed;local old=ownedGold(cities[2]);changes.Emit({owner=0,cityID=1,kinds={'ACTIVE'},cause='COMMITTED'})
        assert(not com.TransactionCurrent(0,2) and not pcall(net.CurrentCapitalSources,0,cities[2],'RESEARCH'))
        assert(net.CurrentOutgoingDomestic(0,cities[2]).validity=='UNKNOWN' and created+removed==n and ownedGold(cities[2])==old)
        changes.Flush();assert(not com.TransactionCurrent(0,2));net.Refresh(0);com.SourceChanged(0,2);assert(com.TransactionCurrent(0,2))
        """)
    def test_failed_consumer_drain_never_recovers_authority_or_retries(self):
        l=commerce();l.execute((ROOT/'Mod/FactChanges.lua').read_text());l.execute("""
        local changes=SPCFactChanges.New(shared);assert(toggle(2,'DISTRICT_CAMPUS',true));local old=ownedGold(cities[2])
        changes.RegisterConsumer('broken',function()error('FAILED_RECOMPUTE')end,{kinds={'ACTIVE'}})
        changes.Emit({owner=0,cityID=2,kinds={'ACTIVE'},cause='COMMITTED'});changes.Flush()
        assert(not com.TransactionCurrent(0,2) and ownedGold(cities[2])==old and changes.pending==0)
        local n=changes.delivered;for i=1,1000 do changes.Flush()end;assert(changes.delivered==n)
        """)
    def test_scoped_source_epochs_do_not_block_unrelated_city_changes(self):
        l=commerce();l.execute((ROOT/'Mod/FactChanges.lua').read_text());l.execute("""
        local changes=SPCFactChanges.New(shared);assert(toggle(2,'DISTRICT_CAMPUS',true));assert(com.TransactionCurrent(0,2))
        changes.Emit({owner=0,cityID=99,kinds={'WORKERS'},cause='WORKERS_CHANGED'});assert(com.TransactionCurrent(0,2))
        changes.Emit({owner=0,cityID=1,kinds={'D'},cause='BUILDING_CHANGED'});assert(not com.TransactionCurrent(0,2))
        com.SourceChanged(0,1);assert(com.TransactionCurrent(0,2))
        changes.Emit({owner=0,cityID=2,kinds={'HISTORY'},topic='DIALOGUE',cause='DIALOGUE_COMPLETED'});assert(com.TransactionCurrent(0,2))
        changes.Emit({owner=0,cityID=2,kinds={'HISTORY'},topic='COMMERCE',cause='SELECTION_COMMITTED'});assert(not com.TransactionCurrent(0,2))
        """)
    def test_generation_only_role_refresh_republishes_current_proof_once(self):
        l=commerce();l.execute((ROOT/'Mod/FactChanges.lua').read_text());l.execute("""
        local changes=SPCFactChanges.New(shared);assert(toggle(2,'DISTRICT_CAMPUS',true));local count=0
        local audit=com.Audit;com.Audit=function(s)count=count+1;return audit(s)end
        changes.Emit({owner=0,cityID=1,kinds={'POTENTIAL'},cause='COMMITTED'});net.Refresh(0)
        assert(count==1 and com.TransactionCurrent(0,2));net.Refresh(0);assert(count==1)
        """)
    def test_actual_network_capture_cannot_certify_newer_reentrant_change(self):
        l=commerce();l.execute((ROOT/'Mod/FactChanges.lua').read_text());l.execute("""
        local changes=SPCFactChanges.New(shared);local read=shared.EffectiveFacts.Read;local once=true
        shared.EffectiveFacts.Read=function(...)if once then once=false;changes.Emit({owner=0,cityID=2,kinds={'ACTIVE'},cause='COMMITTED'})end;return read(...)end
        net.Refresh(0);assert(net.CurrentOutgoingDomestic(0,cities[2]).validity=='UNKNOWN')
        shared.EffectiveFacts.Read=read;net.Refresh(0);assert(net.CurrentOutgoingDomestic(0,cities[2]).validity=='VERIFIED')
        """)
    def test_second_commit_during_commerce_capture_not_certified_as_first(self):
        l=commerce();l.execute((ROOT/'Mod/FactChanges.lua').read_text());l.execute("""
        local changes=SPCFactChanges.New(shared);assert(toggle(2,'DISTRICT_CAMPUS',true))
        local read=shared.EffectiveFacts.Read;local once=true
        shared.EffectiveFacts.Read=function(...)if once then once=false;changes.Emit({owner=0,cityID=2,kinds={'ACTIVE'},cause='SECOND_COMMITTED'})end;return read(...)end
        com.SourceChanged(0,2);assert(not com.TransactionCurrent(0,2))
        shared.EffectiveFacts.Read=read;net.Refresh(0);com.SourceChanged(0,2);assert(com.TransactionCurrent(0,2))
        """)

if __name__=='__main__':unittest.main()
