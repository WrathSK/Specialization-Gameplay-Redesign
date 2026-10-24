"""Provider registration, normalized invalidation, official signal ownership; no native PASS."""
import unittest
from refactor_harness import Context,ROOT,measure,legacy_source_observation
from refactor_fixtures import depth_context
from refactor_defect_fixtures import commerce,startup


def depth():
    c=depth_context();c.load('FactChanges');c.execute('fc=SPCFactChanges.New(shared);d=shared.DistrictCompleteness;seen={}')
    return c


class Districts(unittest.TestCase):
    def test_city_dirty_and_schedule_share_scope_zero_native_mark(self):
        c=depth();c.execute("""
        sample(1);sample(2);d.RegisterConsumer('test',function(e)seen[#seen+1]=e end);resetCounts()
        local old=Map;Map=setmetatable({},{__index=function()error('NATIVE_DURING_MARK')end})
        Events.DistrictBuildProgressChanged.Fire(0,77,1);assert(not counts.dc_capture and fc.pending==1)
        Map=old;fc.Flush();assert(#seen==1 and seen[1].player==0 and seen[1].city==1)
        sample(2);assert(not counts.dc_capture);sample(1);assert(counts.dc_capture==1)
        """)
        measure('S5c1_known_city_invalidation',{'mark_native_captures':0,'unrelated_city_recaptures':0,'affected_city_recaptures':1})
    def test_foreign_zero_and_malformed_unknown_is_bounded_fallback(self):
        c=depth();c.execute("sample(1);sample(2);resetCounts();Events.DistrictPillaged.Fire(1,99,1);sample(1);sample(2);assert(not counts.dc_capture and fc.pending==0);Events.DistrictPillaged.Fire(-1,99,1);sample(2);assert(counts.dc_capture==1 and fc.pending==1)")
    def test_transfer_uses_new_city_only_for_new_owner(self):
        c=depth();c.execute("sample(1);sample(2);d.RegisterConsumer('test',function(e)seen[#seen+1]=e end);resetCounts();Events.CityTransfered.Fire(1,900,0);fc.Flush();assert(#seen==1 and seen[1].player==0 and seen[1].city==nil);sample(1);sample(2);assert(counts.dc_capture==2)")
    def test_capture_reentry_ticket_blocks_old_success_then_event_recovers(self):
        c=depth();c.execute("local once=true;local old=cities[1].GetBuildings;cities[1].GetBuildings=function()if once then once=false;d.MarkDirty(0,1)end;return old()end;local a=sample(1);assert(a.validity=='UNKNOWN' and a.availability=='TEMPORARILY_UNAVAILABLE' and a.error=='DC_CHANGED_DURING_CAPTURE');local b=sample(1);assert(b.validity=='VERIFIED' and b.availability=='READY' and counts.dc_capture==2)")
    def test_warm_pillage_repair_and_final_reference_invalidation_survive(self):
        c=depth();c.execute("local get=cities[1].GetBuildings;pillaged=false;cities[1].GetBuildings=function()local b=get();b.IsPillaged=function()return pillaged end;return b end;assert(sample(1).value.domains.DISTRICT_CAMPUS.value==1);pillaged=true;GameEvents.BuildingPillageStateChanged.Fire(0,1,1,true);assert(sample(1).value.domains.DISTRICT_CAMPUS.value==0);pillaged=false;GameEvents.BuildingPillageStateChanged.Fire(0,1,1,false);assert(sample(1).value.domains.DISTRICT_CAMPUS.value==1)")
        c=depth();c.execute("local get=cities[1].GetY;local n=0;cities[1].GetY=function()n=n+1;if n==2 then d.MarkDirty(0,1)end;return get()end;local value=sample(1);assert(value.validity=='UNKNOWN' and value.error=='DC_CHANGED_DURING_CAPTURE');assert(sample(1).validity=='VERIFIED')")
    def test_same_turn_second_change_and_spc_carrier_filter(self):
        c=depth();c.execute("sample(1);local revision=sample(1).revision;cities[1].present[2]=true;Events.DistrictPillaged.Fire(0,1,1,0,0,1,100,false);assert(sample(1).revision>revision);local seq=fc.sequence;local info=P.Info;P.Info=function(t,k)if t=='Buildings' and k==100 then return {BuildingType='BUILDING_SPC_TEST'}end;return info(t,k)end;Events.BuildingAddedToMap.Fire(1,0,100,0);assert(fc.sequence==seq);cities[1].present[3]=true;Events.DistrictPillaged.Fire(0,1,1,0,0,1,100,false);assert(sample(1).value.domains.DISTRICT_CAMPUS.value==3)")
    def test_callback_reentry_merges_next_snapshot_and_no_idle_retry(self):
        c=depth();c.execute("d.RegisterConsumer('bad',function()error('TARGET_FAILURE')end);d.RegisterConsumer('good',function(e)seen[#seen+1]=e.city;if e.city==1 then d.MarkDirty(0,2);fc.Flush()end end);d.MarkDirty(0,1);fc.Flush();assert(#seen==1 and fc.pending==1 and fc.errors.DC_bad);fc.Flush();assert(#seen==2 and seen[2]==2 and fc.pending==0);local n=fc.delivered;for i=1,1000 do fc.Flush()end;assert(fc.delivered==n)")
    def test_provider_registration_failed_start_cannot_escape_quarantine(self):
        c=depth();c.load('RuntimeComposition');c.execute("local startup=SPCRuntimeComposition.New(shared);writes=0;assert(not startup.Run('Broken',{}, {},function()d.RegisterConsumer('broken',function()writes=writes+1 end);error('LATE_FAILURE')end));d.MarkDirty(0,1);fc.Flush();assert(writes==0 and fc.errors.DC_broken)")
    def test_global_fallback_dominates_full_audit_without_losing_city_only_work(self):
        c=depth();c.load('FactConsumerBindings');c.execute("SPCFactConsumerBindings.New(shared);all=0;narrow=0;shared.Lv2GPP={Audit=function(s)assert(s.player==nil and s.city==nil);all=all+1 end};shared.IndustrySupport={Audit=function(s)assert(s.player==0 and s.city==1);narrow=narrow+1 end};d.MarkDirty(0,1);d.MarkDirty(nil,nil,'UI_FACTS_DIRTY');fc.Flush();shared.FactBindings.Flush();assert(all==1 and narrow==1)")
    def test_unknown_scope_immediately_stales_scalar_transaction_epochs(self):
        c=depth();c.execute("local a=fc.Generation(0,'COMMERCE');local b=fc.Generation(0,'COMMERCE',7);local n=fc.Generation(0,'NETWORK');d.MarkDirty();assert(fc.Generation(0,'COMMERCE')>a and fc.Generation(0,'COMMERCE',7)>b and fc.Generation(0,'NETWORK')==n)")


class NetworkSignals(unittest.TestCase):
    def test_official_owner_without_diagnostic_and_complete_trigger_union(self):
        l=commerce();l.execute("P.RouteUnitRelevant=function(pid,id)return id~=99 end;local value=shared.RouteSignalRevision;Events.UnitOperationStarted.Fire(1,10);Events.UnitOperationStarted.Fire(0,99);assert(shared.RouteSignalRevision==value);Events.UnitOperationStarted.Fire(0,10);Events.UnitOperationDeactivated.Fire(0,10);Events.UnitOperationsCleared.Fire(0,10);Events.CityTransfered.Fire(0,2,1);Events.TradeRouteRemovedFromMap.Fire(0,10);assert(shared.RouteSignalRevision==value+5 and not net.TransactionCurrent(0))")
    def test_diagnostic_start_cannot_reset_or_double_increment(self):
        l=commerce();l.execute("P.RouteUnitRelevant=function()return true end;Events.UnitOperationStarted.Fire(0,10);signalBefore=shared.RouteSignalRevision")
        with legacy_source_observation():l.globals().include('TradeRouteProbe')
        l.execute("P.Scalar=tostring;SPCTradeRouteProbe.Start(P,shared);assert(shared.RouteSignalRevision==signalBefore);Events.UnitOperationStarted.Fire(0,10);assert(shared.RouteSignalRevision==signalBefore+1)")
    def test_provider_register_routes_once_and_isolates_failure(self):
        l=commerce();l.execute("calls=0;net.RegisterConsumer('bad',function()error('BAD_NET_TARGET')end);net.RegisterConsumer('good',function(e)assert(e.kinds.NETWORK);calls=calls+1 end);shared.FactChanges.Emit({owner=0,kinds={'NETWORK'},cause='NEW_PROOF'});shared.FactChanges.Flush();assert(calls==1 and shared.FactChanges.errors.NET_bad)")
    def test_actual_startup_diagnostic_failure_is_not_network_dependency(self):
        c=startup();c.execute("SPCTradeRouteProbe.Start=function()error('DIAGNOSTIC_FAILED')end");c.load('Gameplay');c.execute("local s=ExposedMembers.SPC_P0;assert(s.StartStatus.TradeRouteProbe.state=='FAILED' and s.StartStatus.NetworkBridge.state=='OK' and sealed)")

if __name__=='__main__':unittest.main()
