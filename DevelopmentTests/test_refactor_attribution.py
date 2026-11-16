"""Attribution adds scalar observation only; callbacks/native reads remain unchanged."""
import unittest
from refactor_harness import Context
from refactor_defect_fixtures import commerce

class Attribution(unittest.TestCase):
    def test_scope_source_and_fallback_do_not_read_native_objects(self):
        c=Context();c.load('RuntimeWork');c.execute("P={Count=function(k)counts[k]=(counts[k]or 0)+1 end,Field=function(t,k)return t[k]end};received={};SPCRuntimeWork.TargetHook(P,Events,'DistrictBuildProgressChanged',function(s)received=s end);Events.DistrictBuildProgressChanged.Fire(0,9,12);assert(received.player==0 and received.city==12);assert(counts.scope_city==1 and counts.scope_events==1);SPCRuntimeWork.Hook(P,GameEvents,'UnknownShape',function(s)assert(s==nil)end);GameEvents.UnknownShape.Fire();assert(counts.scope_fallback==1 and counts.scope_unknown_signature==1 and counts.scope_gameevents==1)")
    def test_carrier_observer_attempts_counted_and_disabled_is_idle(self):
        c=Context();c.execute("P={Field=function(t,k)return t and t[k]end,IsTestPlayer=function(p)return p==0 end,Count=function(k)counts[k]=(counts[k]or 0)+1 end,Info=function()return {Index=1}end};SPCExpeditionTrainingDiagnostics={ENABLED=true,New=function()return {Record=function()end}end};city={GetID=function()return 1 end,GetX=function()return 1 end,GetY=function()return 2 end,GetBuildings=function()return {HasBuilding=function()return false end}end};Players={[0]={GetCities=function()return {Members=function()return ipairs({city})end}end}}")
        c.load('CarrierHealthTrace');c.execute("SPCCarrierHealthTrace.Start(P,shared);Events.LoadScreenClose.Fire();assert(counts.observer_native_attempt==35 and counts.observer_carrier_attempt==35 and counts.observer_city_scan==1);SPCExpeditionTrainingDiagnostics.ENABLED=false;Events.PlayerTurnActivated.Fire(0);assert(counts.observer_native_attempt==35)")
    def test_commerce_turn_sampling_counts_only_observer_work(self):
        l=commerce();l.execute("assert(toggle(2,'DISTRICT_CAMPUS',true));counts={};before=ownedGold(cities[2]);writesBefore=commerceWrites;Events.PlayerTurnDeactivated.Fire(0);assert(counts.observer_commerce_attempt>0 and counts.observer_native_attempt==counts.observer_commerce_attempt);assert(counts.observer_city_scan==5);assert(ownedGold(cities[2])==before and commerceWrites==writesBefore)")
    def test_fixed_counter_names_are_retained_in_evidence(self):
        import json,tempfile
        from pathlib import Path
        from refactor_defect_fixtures import gc
        from test_b269_memory import reader,Memory
        l=gc();l.execute("SPCPerformance.Count('scope_city');SPCPerformance.Count('observer_native_attempt',3);Events.PlayerTurnDeactivated.Fire(0)")
        rows=[];l.globals().print=rows.append;l.execute(reader.command('trace','TEST ','END'))
        records=[dict(part.split('=',1) for part in row.split() if '=' in part) for row in rows if row.startswith('TEST MEM ')]
        record=next(row for row in records if row['kind']=='TURN_END')
        self.assertEqual(record['work_scope_city'],'1');self.assertEqual(record['work_observer_native_attempt'],'3')
        with tempfile.TemporaryDirectory()as directory:
            evidence=Memory(Path(directory),lambda *a,**k:None)
            try:
                evidence.add(record)
                self.assertEqual(evidence.latest_work['work_scope_city'],1)
                self.assertEqual(evidence.latest_work['work_observer_native_attempt'],3)
                saved=[json.loads(line)for line in (Path(directory)/'memory.jsonl').read_text().splitlines()]
                self.assertEqual(saved[-1]['evidence']['work_observer_native_attempt'],'3')
            finally:evidence.close()
