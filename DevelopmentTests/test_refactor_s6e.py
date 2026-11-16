"""S6e Capital lazy work: actual Lua51 service/Store/UI and retained assertions."""
import unittest
import struct
import test_b244_capital_storage as storage_cases
import test_store_write_boundaries as store
import test_b261_commerce as commerce_ui
from test_b241_capital import runtime
import test_b241_capital as capital_cases
import test_b245_capital_receipts as receipt_cases
from test_b262_capital_sidebar import ui
import test_b262_capital_sidebar as sidebar_cases
from refactor_harness import TrackedLua51, legacy_source_observation, measure


class MoneyLua51(TrackedLua51):
    """Explicit native Property double: same IEEE binary32 as old pack('f')."""
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.globals()._s6e_binary32=lambda n:struct.unpack('=f',struct.pack('=f',n))[0]


class Profile:
    def setUp(self):
        self.old_store=store.LuaRuntime;self.old_ui=commerce_ui.LuaRuntime
        self.old_float32=storage_cases.FLOAT32
        expression="return string.unpack('f',string.pack('f',v))"
        assert storage_cases.FLOAT32.count(expression)==1
        storage_cases.FLOAT32=storage_cases.FLOAT32.replace(expression,'return _s6e_binary32(v)')
        store.LuaRuntime=MoneyLua51;commerce_ui.LuaRuntime=TrackedLua51
        self.observation=legacy_source_observation();self.observation.__enter__()
    def tearDown(self):
        self.observation.__exit__(None,None,None)
        store.LuaRuntime=self.old_store;commerce_ui.LuaRuntime=self.old_ui
        storage_cases.FLOAT32=self.old_float32


def observed():
    l=runtime();l.execute('''
      work={balance=0,depth=0,history=0,source={}}
      local treasury=Players[0].GetTreasury
      Players[0].GetTreasury=function(self)
       local t=treasury(self);local get=t.GetGoldBalance
       t.GetGoldBalance=function(...)work.balance=work.balance+1;return get(...)end;return t
      end
      local depth=shared.DistrictCompleteness.ReadFacts
      shared.DistrictCompleteness.ReadFacts=function(...)work.depth=work.depth+1;return depth(...)end
      local history=shared.CityProgressionStore.InstitutionHistory
      shared.CityProgressionStore.InstitutionHistory=function(...)
       work.history=work.history+1;return history(...)
      end
      local sources=shared.NetworkBridge.CurrentCapitalSources
      shared.NetworkBridge.CurrentCapitalSources=function(pid,c,kind)
       work.source[kind]=(work.source[kind]or 0)+1
       if failedKind==kind then error('CAPITAL_SOURCE_UNKNOWN')end
       return sources(pid,c,kind)
      end
      function resetWork()work={balance=0,depth=0,history=0,source={}}end
      function sourceWork()local n=0;for _,v in pairs(work.source)do n=n+v end;return n end
      function explicit()return cap.Request(0,{Action='CAPITAL_REFRESH',CityID=source:GetID(),Token='refresh'})end
    ''');return l


class LazyQuotes(Profile,unittest.TestCase):
    def test_automatic_dirty_skips_all_speculative_inputs_and_idle_does_nothing(self):
        l=observed();l.execute("cap.Mark(0);Events.GameCoreEventPublishComplete.Fire();assert(work.balance==0 and work.depth==0 and work.history==0 and sourceWork()==0);local revision=cap.revision;for i=1,1000 do Events.GameCoreEventPublishComplete.Fire()end;assert(cap.revision==revision and work.balance==0 and sourceWork()==0);cap.Mark(0);Events.GameCoreEventPublishComplete.Fire();assert(cap.revision==revision)")
        measure('S6e_Capital_automatic_quotes',{'background_sources':0,'background_balance':0,'background_depth':0,'background_history':0,'idle_publishes':1000,'idle_extra_work':0,'original_background':'full3-domain quote per qualified tracked city'})

    def test_direct_refresh_default_and_explicit_request_keep_same_terms(self):
        l=observed();l.execute("local old=T.encode(C.view().domains);local v=cap.Refresh(0,source:GetID());assert(not v.quoteStale and T.encode(v.domains)==old);assert(explicit());assert(T.encode(C.view().domains)==old and not C.view().quoteStale and sourceWork()==6 and work.depth==2)")

    def test_light_refresh_retains_only_display_quote_and_rejects_direct_confirmation(self):
        l=observed();l.execute("local q=T.encode(C.view().domains[1].quote);local v=cap.Refresh(0,source:GetID(),false);assert(v.quoteStale and not v.canSign and T.encode(v.domains[1].quote)==q and v.balance==nil);local okay,why=C.confirm(nil,'VENTURE');assert(not okay and why=='CAPITAL_QUOTE_STALE'and rolls==0 and moneyCalls==0);assert(not C.view().quoteStale)")

    def test_explicit_refresh_restores_transaction_after_light_update(self):
        l=observed();l.execute("cap.Refresh(0,source:GetID(),false);assert(explicit());assert(not C.view().quoteStale);assert(C.confirm()and moneyCalls==1)")

    def test_confirmation_sources_only_selected_then_full_response(self):
        l=observed();l.execute("assert(C.confirm());assert(work.source.RESEARCH==2 and work.source.CULTURE==1 and work.source.INDUSTRY==1 and sourceWork()==4);assert(work.depth==2 and moneyCalls==1)")
        measure('S6e_Capital_confirmation_sources',{'before_validation':3,'after_validation':1,'post_response':3,'total_before':6,'total_after':4,'balance_and_contract_fresh':True})

    def test_unrelated_domain_unknown_does_not_block_selected_fresh_contract(self):
        l=observed();l.execute("failedKind='CULTURE';assert(C.confirm());assert(moneyCalls==1 and C.contract().stage=='ACTIVE'and work.source.CULTURE==1 and work.source.RESEARCH==2)")

    def test_selected_source_unknown_prevents_random_roll_and_money(self):
        l=observed();l.execute("failedKind='RESEARCH';assert(not C.confirm(nil,'VENTURE'));assert(rolls==0 and moneyCalls==0 and not C.state())")

    def test_qualification_loss_keeps_actual_reason_without_quote_reads(self):
        l=observed();l.execute("T.governor(1);resetWork();local v=cap.Refresh(0,source:GetID(),false);assert(v.quoteStale and not v.canSign and v.reason=='CAPITAL_ACTIVE_III_REQUIRED'and sourceWork()==0 and work.balance==0)")

    def test_background_held_contract_does_not_clear_receipt_or_replay(self):
        l=observed();l.execute("moneyFail='AFTER';assert(not C.confirm());local old=T.encode(C.state());resetWork();cap.Refresh(0,source:GetID(),false);assert(T.encode(C.state())==old and moneyCalls==1 and C.view().stage=='HELD'and sourceWork()==0)")

    def test_reference_change_cannot_reuse_old_display_quote(self):
        l=observed();l.execute("local old=shared.CityProgressionStore.CapitalReference;shared.CityProgressionStore.CapitalReference=function(token)local r=old(token);r.changes=r.changes+1;return r end;local v=cap.Refresh(0,source:GetID(),false);assert(v.quoteStale);for _,row in ipairs(v.domains)do assert(row.quote==nil)end;assert(moneyCalls==0)")

    def test_queued_owner_cause_does_not_stale_fresh_quote_but_keeps_sibling(self):
        l=observed();l.execute("cap.Mark(0);assert(explicit());local revision=C.view().revision;resetWork();Events.GameCoreEventPublishComplete.Fire();assert(not C.view().quoteStale and C.view().revision==revision and sourceWork()==0);assert(cap.views['0:'..other:GetID()].quoteStale)")

    def test_post_confirmation_response_covers_old_mark_without_staling_next_quote(self):
        l=observed();l.execute("assert(C.confirm());local revision=C.view().revision;Events.GameCoreEventPublishComplete.Fire();assert(not C.view().quoteStale and C.view().revision==revision);assert(C.confirm('DISTRICT_THEATER','STABLE','second')and moneyCalls==2)")

    def test_reentrant_and_later_causes_still_invalidate_fresh_quote(self):
        l=observed();l.execute("cap.Mark(0,source:GetID());local read=shared.NetworkBridge.CurrentCapitalSources;local once=true;shared.NetworkBridge.CurrentCapitalSources=function(...)if once then once=false;cap.Mark(0,source:GetID())end;return read(...)end;assert(explicit());Events.GameCoreEventPublishComplete.Fire();assert(C.view().quoteStale);assert(explicit());assert(not C.view().quoteStale);cap.Mark(0);Events.GameCoreEventPublishComplete.Fire();assert(C.view().quoteStale and moneyCalls==0)")


class UIQuotes(Profile,unittest.TestCase):
    def test_stale_blocks_callback_and_button_while_preserving_displayed_terms(self):
        l=ui();l.execute("pick(1,1);capitalView.quoteStale=true;notify();local n=#sent;assert(Controls.Confirm.disabled);Controls.Confirm.click();assert(#sent==n and Controls.Quote.text:find('250'));capitalView.quoteStale=nil;notify();assert(not Controls.Confirm.disabled)")

    def test_stale_does_not_mask_qualification_or_held_reason(self):
        l=ui();l.execute("pick(1,1);capitalView.quoteStale=true;capitalView.canSign=false;capitalView.reason='CAPITAL_ACTIVE_III_REQUIRED';notify();assert(Controls.Current.text:find('ACTIVE III'));capitalView.stage='HELD';capitalView.failure={phase='NATIVE_DEBIT'};notify();assert(Controls.Current.text:find('PAUSE_DEBIT'))")


class RetainedCapital(Profile,capital_cases.Runtime):
    """Original transaction assertions executed with explicit Lua51 profile."""

class RetainedReceipts(Profile,receipt_cases.Receipts):
    """Original native-money receipt assertions; no tolerance/lock changes."""

class RetainedGuards(Profile,receipt_cases.Guards):
    """Original reentry/failed native protections, unchanged assertions."""

class RetainedSidebar(Profile,sidebar_cases.Sidebar):
    """Current sidebar interactions/geometry/escape with unchanged assertions."""


if __name__=='__main__':unittest.main()
