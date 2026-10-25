"""S6j real Store/EF/Bridge/registry, with explicit native census/route doubles."""
import unittest
from refactor_harness import ROOT,Context,legacy_source_observation,measure
from test_refactor_s5a2 import actual_store
from test_refactor_s5c2 import fixture as network_fixture


def fixture(n=8,bindings=False):
    l=actual_store();l.execute("x,y=T.two();siteCities={x,y};for i=3,"+str(n)+" do local c=T.fresh(i);T.register(c);T.complete(c,'DISTRICT_CAMPUS');siteCities[#siteCities+1]=c end")
    l.execute("""
      P.VERSION='S6J';P.RouteUnitRelevant=function()return false end;work={};P.Count=function(k)work[k]=(work[k]or 0)+1 end
      ExposedMembers=ExposedMembers or {}
      Players[0].GetTrade=function()return {CountOutgoingRoutes=function()return 0 end}end
      local get=Players[0].GetCities
      Players[0].GetCities=function()local cities=get();cities.GetCapitalCity=function()return x end;return cities end
      efReads={};local read=shared.EffectiveFacts.Read
      shared.EffectiveFacts.Read=function(pid,c)efReads[c:GetID()]=(efReads[c:GetID()]or 0)+1;return read(pid,c)end
      function sum()local n=0;for _,v in pairs(efReads)do n=n+v end;return n end
      function resetWork()efReads={};work={}end
    """)
    with legacy_source_observation():l.globals().include('NetworkBridge')
    l.execute("""
      SPCNetworkBridge.Start(P,shared);net=shared.NetworkBridge;net.ready=true
      net.Receive(0,{Epoch=net.epoch,Seq=1,Turn=T.now(),Signal=shared.RouteSignalRevision,Valid=1,Count=0,Data=''})
      assert(net.Input(0).availability=='AVAILABLE',net.Report(0,x))
      shared.FactChanges.Flush();net.Refresh(0);resetWork()
    """)
    if bindings:
        l.execute((ROOT/'Mod/FactConsumerBindings.lua').read_text());l.execute('SPCFactConsumerBindings.New(shared);resetWork()')
    return l


class CityIncrements(unittest.TestCase):
    def test_full_census_but_only_changed_actual_store_city_deep_capture(self):
        results=[]
        for n in (8,32,64):
            l=fixture(n,True);l.execute("T.invest(x,9901);resetWork();shared.FactChanges.Flush();assert(sum()==1 and efReads[x:GetID()]==1);assert(net.players[0].input.cities[x:GetID()].potential==2 and net.TransactionCurrent(0));assert(work.city_scan==#siteCities)")
            results.append({'cities':n,'census':l.globals().work['city_scan'],'deep':l.globals().sum()})
        self.assertEqual([x['deep'] for x in results],[1,1,1])
        measure('S6j_real_Store_network_input',{'work':results,'before_deep':[8,32,64],'after_deep':[1,1,1],'remaining':'complete census/ref, Store authority and route endpoint/trader/war checks; governor witness for Potential>1; not all native reads or CPU time'})

    def test_two_cities_same_drain_and_second_real_commit_same_turn(self):
        l=fixture(8,True);l.execute("T.invest(x,9902);T.invest(y,9903);resetWork();shared.FactChanges.Flush();assert(sum()==2 and efReads[x:GetID()]==1 and efReads[y:GetID()]==1);assert(net.players[0].input.cities[x:GetID()].potential==2 and net.players[0].input.cities[y:GetID()].potential==2);T.invest(x,9904);resetWork();shared.FactChanges.Flush();assert(sum()==1 and net.players[0].input.cities[x:GetID()].potential==3)")

    def test_failed_emit_still_invalidates_other_city_before_sibling_cause(self):
        l=fixture(8,True);l.execute("local emit=shared.FactChanges.Emit;shared.FactChanges.Emit=function()error('DROPPED_NOTIFICATION')end;T.invest(x,9905);assert(not net.TransactionCurrent(0));shared.FactChanges.Emit=emit;T.invest(y,9906);resetWork();shared.FactChanges.Flush();assert(sum()==2 and net.players[0].input.cities[x:GetID()].potential==2 and net.players[0].input.cities[y:GetID()].potential==2 and net.TransactionCurrent(0))")

    def test_explicit_refresh_route_candidate_new_turn_and_new_registry_force_full(self):
        for change in ("net.Refresh(0)","net.Receive(0,{Epoch=net.epoch,Seq=2,Turn=T.now(),Signal=shared.RouteSignalRevision,Valid=1,Count=0,Data=''})","local now=T.now();Game.GetCurrentGameTurn=function()return now+1 end;net.RefreshFacts(0)","SPCFactChanges.New(shared);net.RefreshFacts(0)"):
            l=fixture();l.execute(change+";assert(sum()==8,sum())")

    def test_replaced_effective_reader_and_store_witness_force_full(self):
        for change in ("local read=shared.EffectiveFacts.Read;shared.EffectiveFacts.Read=function(...)return read(...)end", "local stamp=shared.CityProgressionStore.FactStamp;shared.CityProgressionStore.FactStamp=function(...)return stamp(...)end"):
            l=fixture();l.execute(change+";net.RefreshFacts(0);assert(sum()==8)")

    def test_equal_facts_refresh_versions_without_publishing_new_values(self):
        l=fixture();l.execute("local rev=net.players[0].inputRevision;shared.FactChanges.InvalidateCommitted(0,x:GetID(),{'ACTIVE'});net.RefreshFacts(0);assert(sum()==1 and net.players[0].inputRevision==rev and net.TransactionCurrent(0));resetWork();net.RefreshFacts(0);assert(sum()==0 and net.players[0].inputRevision==rev)")

    def test_unknown_held_store_never_becomes_cached_confirmed(self):
        l=fixture();l.execute("local setter=Game.SetProperty;Game.SetProperty=function(o,k,v)local r=setter(o,k,v);if k==T.key(x)then error('AFTER_APPLY')end;return r end;assert(not pcall(T.invest,x,9907));Game.SetProperty=setter;resetWork();net.RefreshFacts(0);assert(efReads[x:GetID()]==1 and net.Input(0).provenance[x:GetID()].status=='RETAINED'and not net.TransactionCurrent(0));resetWork();net.RefreshFacts(0);assert(efReads[x:GetID()]==1 and not net.TransactionCurrent(0))")

    def test_actual_store_commit_reentry_cannot_certify_cached_success(self):
        l=fixture();l.execute("local setter=Game.SetProperty;local observed=0;Game.SetProperty=function(o,k,v)if k==T.key(x)then net.RefreshFacts(0);assert(not net.TransactionCurrent(0) and net.Input(0).provenance[x:GetID()].status=='RETAINED');observed=observed+1 end;return setter(o,k,v)end;T.invest(x,9908);assert(observed==3);Game.SetProperty=setter;net.RefreshFacts(0);assert(net.TransactionCurrent(0)and net.players[0].input.cities[x:GetID()].potential==2)")

    def test_missing_authority_stamp_and_reference_change_take_fresh_path(self):
        l=fixture();l.execute("shared.CityProgressionStore.FactStamp=nil;net.RefreshFacts(0);assert(sum()==8)")
        l=fixture();l.execute("local original=x.s.values.TOKEN;x.s.values.TOKEN='DIFFERENT';net.RefreshFacts(0);assert(efReads[x:GetID()]and not net.TransactionCurrent(0));x.s.values.TOKEN=original;net.Refresh(0);assert(net.TransactionCurrent(0))")

    def test_ownerwide_and_global_marks_force_full_without_city_guess(self):
        for scope in ('{owner=0,','{'):
            l=fixture();l.execute("shared.FactChanges.Emit("+scope+"kinds={'ACTIVE'},cause='WIDE'});net.RefreshFacts(0);assert(sum()==8)")

    def test_governor_gate_late_change_and_unknown_never_hidden(self):
        l=fixture();l.execute("T.invest(x,9909);net.Refresh(0);T.governor(1);resetWork();net.RefreshFacts(0);assert(efReads[x:GetID()]==1 and net.players[0].input.cities[x:GetID()].active==1);T.governor(4);resetWork();net.RefreshFacts(0);assert(efReads[x:GetID()]==1 and net.players[0].input.cities[x:GetID()].active==2)")
        l=fixture();l.execute("T.invest(x,9910);net.Refresh(0);local gate=P.GovernorGate;P.GovernorGate=function(c)if c==x then error('GATE_UNKNOWN')end;return gate(c)end;resetWork();net.RefreshFacts(0);assert(efReads[x:GetID()]==1 and not net.TransactionCurrent(0));P.GovernorGate=gate;net.RefreshFacts(0);assert(net.TransactionCurrent(0))")

    def test_reentrant_role_change_during_capture_stays_pending_then_recovers(self):
        l=fixture();l.execute("shared.FactChanges.InvalidateCommitted(0,x:GetID(),{'ACTIVE'});local read=shared.EffectiveFacts.Read;local once=true;shared.EffectiveFacts.Read=function(pid,c)local v=read(pid,c);if once then once=false;shared.FactChanges.Emit({owner=0,cityID=y:GetID(),kinds={'ACTIVE'},cause='SECOND'})end;return v end;net.Refresh(0);assert(not net.TransactionCurrent(0));net.RefreshFacts(0);assert(net.TransactionCurrent(0))")

    def test_mid_capture_registry_reader_or_store_replacement_never_certifies(self):
        for mutate in ("SPCFactChanges.New(shared)","local read=shared.EffectiveFacts.Read;shared.EffectiveFacts.Read=function(...)return read(...)end","local stamp=shared.CityProgressionStore.FactStamp;shared.CityProgressionStore.FactStamp=function(...)return stamp(...)end"):
            l=fixture();l.execute("local get=x.GetProperty;local once=true;x.GetProperty=function(c,k)local v=get(c,k);if once then once=false;"+mutate+" end;return v end;net.RefreshFacts(0);assert(not net.TransactionCurrent(0));x.GetProperty=get;net.Refresh(0);assert(net.TransactionCurrent(0))")

    def test_fault_reentry_inside_governor_witness_cannot_reuse_old_authority(self):
        l=fixture();l.execute("""
          T.invest(x,9912);net.Refresh(0)
          local gate=P.GovernorGate;local setter=Game.SetProperty;local once=true
          P.GovernorGate=function(c)
           if c==x and once then once=false
            Game.SetProperty=function(o,k,v)local r=setter(o,k,v);if k==T.key(x)then error('AFTER_APPLY')end;return r end
            assert(not pcall(T.invest,x,9913));Game.SetProperty=setter
           end
           return gate(c)
          end
          shared.EffectiveFacts.WithPhase('REUSE_WITNESS',function()net.RefreshFacts(0)end)
          assert(not once and not net.TransactionCurrent(0)and net.Input(0).provenance[x:GetID()].status=='RETAINED')
        """)

    def test_new_turn_witness_failure_revokes_transaction_and_recovers_on_new_call(self):
        for fail_at in (1,2):
            l=fixture();l.globals().failAt=fail_at;l.execute("local get=Game.GetCurrentGameTurn;local calls=0;Game.GetCurrentGameTurn=function()calls=calls+1;if calls==failAt then error('TURN_UNREADABLE')end;return get()end;net.RefreshFacts(0);assert(not net.TransactionCurrent(0));Game.GetCurrentGameTurn=get;net.RefreshFacts(0);assert(net.TransactionCurrent(0))")

    def test_foreign_gameevent_is_filtered_but_unknown_owner_full_fallback(self):
        l=fixture();l.execute("GameEvents.OnDistrictConstructed.Fire(1,'DISTRICT_CAMPUS',99,99);GameEvents.CityBuilt.Fire(1,99,99,99);assert(sum()==0);GameEvents.OnDistrictConstructed.Fire(nil);assert(sum()==8)")

    def test_incremental_and_original_full_capture_same_signature_and_provenance(self):
        l=fixture(16);l.execute("T.invest(x,9911);resetWork();net.RefreshFacts(0);local first=net.players[0].input;local deep=sum();resetWork();net.Refresh(0);local full=net.players[0].input;assert(deep==1 and sum()==16 and first.signature==full.signature and first.factAvailability==full.factAvailability);for id,row in pairs(first.provenance)do assert(full.provenance[id].reference==row.reference and full.provenance[id].status==row.status)end")

    def test_real_route_bridge_still_checks_trader_and_endpoint_on_reuse_path(self):
        l=network_fixture();l.execute("""
          shared.CityProgressionStore.FactStamp=function(pid,c)return c.token..':1'end
          P.GovernorGate=function(c)return c.owner,c.id,'KNOWN',c.active end
          net.Refresh(0);factReads={};net.RefreshFacts(0);assert(next(factReads)==nil)
          units[10]=nil;net.RefreshFacts(0)
          for _,r in ipairs(net.players[0].routes)do assert(r.trader~=10)end
          assert(not net.TransactionCurrent(0))
        """)
        l=network_fixture();l.execute("""
          shared.CityProgressionStore.FactStamp=function(pid,c)return c.token..':1'end
          P.GovernorGate=function(c)return c.owner,c.id,'KNOWN',c.active end
          net.Refresh(0);factReads={};local owner=cities[1].GetOwner
          cities[1].GetOwner=function()error('ENDPOINT_UNREADABLE')end
          net.RefreshFacts(0);assert(not net.TransactionCurrent(0))
          cities[1].GetOwner=owner;net.Receive(0,packet(beforeSeq+1));assert(net.TransactionCurrent(0))
        """)


class StampBounds(unittest.TestCase):
    def test_city_global_ownerwide_and_history_versions_have_no_native_reads(self):
        c=Context();c.load('FactChanges');c.execute("d=SPCFactChanges.New(shared);Players=setmetatable({},{__index=function()error('NO_NATIVE')end});d.InvalidateCommitted(0,1,{'ACTIVE'});assert(d.NetworkCityGeneration(0,1)==1 and d.NetworkCityGeneration(0,2)==0);d.InvalidateCommitted(0,nil,{'ACTIVE'});assert(d.NetworkCityGeneration(0,1)==2 and d.NetworkCityGeneration(0,2)==1);d.Emit({kinds={'IDENTITY'},cause='GLOBAL'});assert(d.NetworkCityGeneration(0,1)==3 and d.NetworkCityGeneration(1,1)==1);d.InvalidateCommitted(0,1,{'HISTORY'},'DIALOGUE');assert(d.NetworkCityGeneration(0,1)==3)")

    def test_capacity_overflow_invalidate_ownerwide_without_eviction_or_unbounded_growth(self):
        c=Context();c.load('FactChanges');c.execute("d=SPCFactChanges.New(shared);for i=1,2048 do d.InvalidateCommitted(0,i,{'ACTIVE'})end;local before=d.NetworkCityGeneration(0,1);for i=2049,4096 do d.InvalidateCommitted(0,i,{'ACTIVE'})end;assert(d.NetworkCityGeneration(0,1)==before+2048);local function up(fn,name)for i=1,20 do local k,v=debug.getupvalue(fn,i);if k==name then return v end end end;local row=up(d.NetworkCityGeneration,'generations')[0];local n=0;for _ in pairs(row.networkCities)do n=n+1 end;assert(n==2048 and row.networkCityCount==2048)")


if __name__=='__main__':unittest.main()
