"""S4a actual recovery producers/consumers. No live/native acceptance."""
import ast
import unittest
from refactor_harness import Context,ROOT,TrackedLua51,legacy_source_observation,separate_legacy_event_namespaces
from refactor_defect_fixtures import greatworks,gc

def industry():
    tree=ast.parse((ROOT/'DevelopmentTests/test_arch_v2_c2.py').read_text())
    fix=next(ast.literal_eval(n.value) for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='FIX' for t in n.targets))
    l=TrackedLua51(unpack_returned_tuples=True)
    l.globals().include=lambda n:l.execute((ROOT/'Mod'/f'{n}.lua').read_text()) if n!='Probe' else None
    with legacy_source_observation():
        l.execute(separate_legacy_event_namespaces(fix))
        l.execute("P.Count=function()end;P.Families={DISTRICT_CAMPUS='RESEARCH',DISTRICT_INDUSTRIAL_ZONE='INDUSTRY'};P.Family=function(t)return P.Families[t]end;for _,v in pairs(districts)do v.IsPillaged=function()return false end end")
        for name in ('FactChanges','NativeFacts','FactConsumerBindings'):l.execute((ROOT/'Mod'/f'{name}.lua').read_text())
        l.execute("SPCFactChanges.New(shared);SPCNativeFacts.New(P,shared);SPCFactConsumerBindings.New(shared);Events.GameCoreEventPublishComplete.Add(function()shared.FactChanges.Flush();shared.FactBindings.Flush()end)")
        l.execute((ROOT/'Mod/IndustrySupport.lua').read_text())
        l.execute("SPCIndustrySupport.Start(P,shared);d=shared.IndustrySupport;d.BindPermanentWrites();sync=true")
    return l

def load_industry_ui(l):
    with legacy_source_observation():l.execute((ROOT/'Mod/UI/IndustryRefresh.lua').read_text())
    l.execute('initUI();pulse()')

class Industry(unittest.TestCase):
    def test_silent_getter_recovery_waits_for_related_event_without_polling(self):
        l=industry();l.execute('factUnknown=true');load_industry_ui(l)
        l.execute("factUnknown=false;local writesBefore=writes;for i=1,1000 do pulse()end;assert(writes==writesBefore and not cities[2].built['BUILDING_SPC_DEV_INDUSTRY_LV1_-1']);fire('GovernorAssigned');pulse();assert(cities[2].built['BUILDING_SPC_DEV_INDUSTRY_LV1_-1'] and sends==1)")
    def test_failed_work_and_duplicate_unavailable_receipts_do_not_rearm(self):
        l=industry();load_industry_ui(l)
        l.execute("""
        reads=0;local read=shared.EffectiveFacts.Read
        shared.EffectiveFacts.Read=function(...)reads=reads+1;return read(...)end
        factUnknown=true;d.Audit({player=0,city=2});reads=0
        local original=clone(queue[#queue]);d.Receive(0,original);assert(reads==0)
        local function receipt(valid)
         local p=clone(original);p.Seq=ExposedMembers.SPC_C2_industry_issued.seq+1;p.Valid=valid
         ExposedMembers.SPC_C2_industry_issued.seq=p.Seq;d.Receive(0,p)
        end
        receipt(1);assert(reads==0) -- validated equal value with no availability transition
        receipt(0);assert(reads==0)
        receipt(1);assert(reads==1) -- confirmed sample availability recovery, once
        for i=1,1000 do pulse()end;assert(reads==1)
        """)
    def test_ui_same_value_availability_recovery_and_second_same_turn_change(self):
        l=industry();load_industry_ui(l)
        l.execute("""
        assert(d.ReadBase(0,cities[2])==6)
        unavailable=true;fire('CityWorkerChanged');pulse(2)
        assert(d.responses[0].status=='UNAVAILABLE')
        factUnknown=true;d.Audit({player=0,city=2})
        unavailable=false;factUnknown=false;fire('CityWorkerChanged');pulse(2)
        assert(d.responses[0].status=='UNCHANGED' and not d.errors['0:2'] and d.ReadBase(0,cities[2])==6)
        districts[12].base=9;fire('CityWorkerChanged');pulse(2);assert(d.ReadBase(0,cities[2])==9 and turn==1)
        """)
    def test_new_cause_arriving_inside_failed_attempt_is_not_lost(self):
        l=industry();l.execute("""
        attempts=0;shared.EffectiveFacts.Read=function(pid,c)
         attempts=attempts+1;if attempts==1 then d.MarkCity(c)end;error('UNREADABLE')
        end
        d.Audit({player=0,city=2});assert(attempts==1)
        fire('GameCoreEventPublishComplete');assert(attempts==2)
        for i=1,1000 do fire('GameCoreEventPublishComplete')end;assert(attempts==2)
        """)

class IndustryReentry(unittest.TestCase):
    def test_changed_sample_received_after_inspect_is_drained_once(self):
        l=industry();l.execute("d.Audit({player=0});injected=false;local create=P.CreateBuilding;P.CreateBuilding=function(b,id)create(b,id);if not injected then injected=true;local p=clone(queue[#queue]);p.Seq=p.Seq+1;p.Data=p.Data:gsub(',6,0',',9,0');ExposedMembers.SPC_C2_industry_issued.seq=p.Seq;d.Receive(0,p)end end")
        load_industry_ui(l)
        l.execute("pulse();assert(d.ReadBase(0,cities[2])==9 and cities[2].built['BUILDING_SPC_DEV_INDUSTRY_LV1_3'] and cities[2].built['BUILDING_SPC_DEV_INDUSTRY_LV1_0']);local before=writes;for i=1,1000 do pulse()end;assert(writes==before)")
    def test_native_scoped_event_during_write_survives_busy_guard(self):
        l=industry();l.execute("d.Audit({player=0});local create=P.CreateBuilding;local once=false;P.CreateBuilding=function(b,id)create(b,id);if not once then once=true;facts[2].active=0;for _,f in ipairs(hooks.DistrictBuildProgressChanged or {})do f(0,12,2)end end end")
        load_industry_ui(l)
        l.execute("pulse();assert(not cities[2].built['BUILDING_SPC_DEV_INDUSTRY_LV1_-1']);local before=writes;for i=1,1000 do pulse()end;assert(writes==before)")
    def test_equal_value_recovery_receipt_while_busy_is_retained(self):
        l=industry();load_industry_ui(l)
        l.execute("""
        factUnknown=true;d.Audit({player=0,city=2});local original=clone(queue[#queue])
        local function receipt(valid)
         local p=clone(original);p.Seq=ExposedMembers.SPC_C2_industry_issued.seq+1;p.Valid=valid;ExposedMembers.SPC_C2_industry_issued.seq=p.Seq;d.Receive(0,p)
        end
        receipt(0);d.busy=true;factUnknown=false;receipt(1);assert(d.errors['0:2'])
        d.busy=false;pulse();assert(not d.errors['0:2']);local before=writes;for i=1,1000 do pulse()end;assert(writes==before)
        """)

class GarbageCollection(unittest.TestCase):
    def test_mixed_blockers_wait_scalar_only_then_collect_once(self):
        l=gc();l.execute("""
        heapReads=0;local read=SPCPerformance.Heap;SPCPerformance.Heap=function()heapReads=heapReads+1;return read()end
        ExposedMembers.SPC_Performance.inflight=1
        ExposedMembers.SPC_IndustryBackground={pending=1};ExposedMembers.SPC_CopyBackground={pending=true}
        Events.PlayerTurnActivated.Fire(0);publish=Events.GameCoreEventPublishComplete.Fire;publish()
        local reads,p=heapReads,prints
        for i=1,10000 do publish()end;assert(heapReads==reads and prints==p and collections==0)
        ExposedMembers.SPC_Performance.inflight=0;publish();assert(collections==0)
        ExposedMembers.SPC_IndustryBackground.pending=0;publish();assert(collections==0)
        ExposedMembers.SPC_CopyBackground.pending=0;assert(collections==0);publish();assert(collections==1)
        for i=1,1000 do publish()end;Events.PlayerTurnActivated.Fire(0);publish();assert(collections==1)
        """)
    def test_ui_wait_cancellation_foreign_end_off_and_other_guard(self):
        for cancel in ('Events.PlayerTurnActivated.Fire(7)','Events.PlayerTurnDeactivated.Fire(0)',"shared.MemoryObservation.SetAutoGC(0,false,'OFF')",'shared.RequestDepth=1'):
            l=gc();l.execute("ExposedMembers.SPC_IndustryBackground={pending=1};Events.PlayerTurnActivated.Fire(0);Events.GameCoreEventPublishComplete.Fire();"+cancel+";ExposedMembers.SPC_IndustryBackground.pending=0;Events.GameCoreEventPublishComplete.Fire();shared.RequestDepth=0;Events.GameCoreEventPublishComplete.Fire();assert(collections==0)")

class GreatWorks(unittest.TestCase):
    def test_unknown_nil_and_throwing_signature_preserve_valid_slot_packet(self):
        for expression in ("function()error('IDENTITY_UNAVAILABLE')end","function()return nil end","function()return {specialization='CULTURE',active=nil}end","function()return {specialization='CULTURE',active=0}end"):
            c=greatworks('ExposedMembers.SPC_P0.EffectiveFacts.Read='+expression)
            self.assertEqual(c.eval('packet.FactsCities'),2);self.assertEqual(c.eval('packet.Valid'),1)
    def test_missing_optional_signature_service_preserves_slots(self):
        for value in ('nil','{}'):
            c=greatworks('ExposedMembers.SPC_P0.EffectiveFacts='+value)
            self.assertEqual(c.eval('packet.FactsCities'),2);self.assertEqual(c.eval('packet.Valid'),1)
    def test_true_slot_collection_failure_stays_unknown(self):
        c=greatworks("SPCGreatWorkFacts.Collector=function()return function(c)if c==city1 then error('SLOT_UNAVAILABLE')end;return {},{}end end")
        self.assertEqual(c.eval('packet.FactsCities'),2);self.assertEqual(c.eval('packet.Valid'),0)
        self.assertIn(',0;',c.eval('packet.FactsRefs'))

class CompactHousing(unittest.TestCase):
    def test_actual_D_business_path_never_requests_detailed_projection(self):
        # Execute only the historical fixture definitions; assertions below target current code.
        c=Context();ns={'__file__':str(ROOT/'DevelopmentTests/test_p0_b2.py')}
        source=c.prefix('DevelopmentTests/test_p0_b2.py','l=runtime()\nfor buildings,expected')
        with legacy_source_observation():exec(compile(source,'S4a housing fixture prefix','exec'),ns)
        ns['LuaRuntime']=TrackedLua51;ns['ns']['LuaRuntime']=TrackedLua51
        with legacy_source_observation():l=ns['runtime']()
        l.execute("setBuildings(d,{'BUILDING_LIBRARY','BUILDING_UNIVERSITY'});svc.MarkDirty();detailCalls=0;svc.Read=function()detailCalls=detailCalls+1;error('DETAIL_READ_FORBIDDEN')end;audit();noErrors();assert(housing(c)==3 and gpp(c,'RESEARCH')==6 and detailCalls==0)")
