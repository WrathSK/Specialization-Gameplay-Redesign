"""B267 actual Lua and offline collection counterexamples; no native/game claims."""
from pathlib import Path
import importlib.util
import json
import sqlite3
import tempfile
import unittest
import xml.etree.ElementTree as ET
import lupa
from lupa.lua55 import LuaRuntime
# Older tests import the package default; the installed namespace has no default.
lupa.LuaRuntime = LuaRuntime
from test_expedition_training_diagnostics import fixture as diagnostics
from test_b239_commerce import fixture as commerce
from test_b232_network_revalidation import pipeline
from test_expedition_trace_collector import collector, reader, FakeClock, TraceSocket

R = Path(__file__).resolve().parents[1]
M = R / 'Mod'


def observer():
    l = LuaRuntime(unpack_returned_tuples=True)
    l.execute(r"""
      turn=1;printed={};logs={};ExposedMembers={};listeners={};writes=0;reads=0
      function event(name)
        local rows={};listeners[name]=rows
        return {Add=function(fn)rows[#rows+1]=fn end,
          Fire=function(...)for _,fn in ipairs(rows)do fn(...)end end}
      end
      Events=setmetatable({},{__index=function(t,k)local e=event(k);rawset(t,k,e);return e end})
      GameEvents=setmetatable({},{__index=function(t,k)local e=event(k);rawset(t,k,e);return e end})
      Game={GetLocalPlayer=function()return 0 end,GetCurrentGameTurn=function()return turn end}
      P={Field=function(o,k)return o and o[k]end,IsTestPlayer=function(pid)return pid==0 end}
      SPCExpeditionTrainingDiagnostics={ENABLED=true,New=function(_,role)return {Record=function(stage,data)
        data=data or {};local v={stage=stage,role=role};for k,x in pairs(data)do v[k]=x end;logs[#logs+1]=v end}end}
      shared={}
      for _,name in ipairs({'NetworkBridge','ResearchSupport','Lv2Housing','Lv2GPP','ResearchInfrastructure',
       'ResearchCross','ResearchApply','ResearchChair','ResearchTraditionEffects','Restructuring','CultureNetwork','CultureAesthetic','Lv3Support','Lv3Effects'})do shared[name]={ready=false}end
      shared.CityProgressionStore={FreshReady=function()return fresh==true end}
      function ready()fresh=true;for _,v in pairs(shared)do if v.ready~=nil then v.ready=true end end end
      function count(stage)local n=0;for _,v in ipairs(logs)do if v.stage==stage then n=n+1 end end;return n end
      function last(stage)for i=#logs,1,-1 do if logs[i].stage==stage then return logs[i]end end end
    """)
    return l


class RecordPolicy(unittest.TestCase):
    def test_more_than96_meaningful_records_continue_across_turns(self):
        l=diagnostics();l.execute("for t=1,4 do currentTurn=t;for i=1,200 do a.Record('CAPITAL_SIGNED',{count=i})end end;assert(trace().sequence==801 and #trace().entries==256 and trace().suppressed==0)")

    def test_change_only_interleaved_city_domain_and_turn(self):
        l=diagnostics();l.execute("a.Record('COMMERCE_DOMAIN',{owner=0,city=1,networkKind='A',previous=2});a.Record('COMMERCE_DOMAIN',{owner=0,city=2,networkKind='A',previous=2});local n=trace().sequence;currentTurn=89;a.Record('COMMERCE_DOMAIN',{owner=0,city=1,networkKind='A',previous=2});assert(trace().sequence==n);a.Record('COMMERCE_DOMAIN',{owner=0,city=1,networkKind='A',previous=3});assert(trace().sequence==n+1)")

    def test_same_turn_identical_receipts_are_not_hidden(self):
        l=diagnostics();l.execute("local n=trace().sequence;a.Record('CAPITAL_REQUEST',{owner=0,city=1});a.Record('CAPITAL_REQUEST',{owner=0,city=1});assert(trace().sequence==n+2)")

    def test_runaway_breaker_explicit_then_recovers(self):
        l=diagnostics();l.execute("M.TURN_LIMIT=5;for i=1,10 do a.Record('CAPITAL_SIGNED',{count=i})end;assert(last().stage=='TRACE_THROTTLED' and trace().suppressed==6);local n=trace().sequence;currentTurn=89;a.Record('CAPITAL_SIGNED',{count=11});assert(trace().sequence==n+1 and last().count=='11')")

    def test_native_sampling_independent_of_record_volume(self):
        l=diagnostics();l.execute("for i=1,200 do a.Record('SIGN',{count=i})end;nativeReads=0;city.GetPopulation=function()nativeReads=nativeReads+1;return 16 end;for i=1,120 do a.Event('SAMPLE',city,state,{count=i})end;assert(nativeReads==96 and trace().sampleSuppressed==24);currentTurn=89;a.Record('AFTER',{count=1});assert(last().stage=='AFTER');unchanged()")

    def test_scalar_filter_and_exact_gold(self):
        l=diagnostics();l.execute("a.Record('SAFE',{goldBalance=0.12345678901234567,reader='/private/user',writerState='FR:READY|NB:PENDING'});assert(last().reader=='REDACTED' and last().goldBalance=='0.12345678901234566' and last().writerState=='FR:READY|NB:PENDING');unchanged()")

    def test_sink_reentry_remains_bounded(self):
        l=diagnostics();l.execute("local calls=0;UI.DataError=function()calls=calls+1;LuaEvents.SPC_B205TrainingTrace();a.Record('REENTER_SINK',{count=1})end;local sink=M.Sink(P);a.Event('NEXT',city,state);assert(calls<10 and trace().sequence<10);sink.Stop()")


class Readiness(unittest.TestCase):
    def start(self):
        l=observer();l.execute((M/'ReadinessSummary.lua').read_text());l.execute('d=SPCReadinessSummary.Start(P,shared)');return l

    def test_disabled_readiness_installs_no_observer(self):
        l=observer();l.execute('SPCExpeditionTrainingDiagnostics.ENABLED=false');l.execute((M/'ReadinessSummary.lua').read_text());l.execute("SPCReadinessSummary.Start(P,shared).Seal();assert(#logs==0 and next(listeners)==nil)")

    def test_load_sampling_waits_for_late_handlers(self):
        l=self.start();l.execute("Events.LoadScreenClose.Add(ready);d.Seal();Events.LoadScreenClose.Fire();assert(count('READINESS_SUMMARY')==0);Events.GameCoreEventPublishComplete.Fire();assert(last('READINESS_SUMMARY').reason=='AFTER_LOAD' and last('READINESS_SUMMARY').notReady=='NONE')")

    def test_early_load_remains_recorded_after_duplicate(self):
        l=self.start();l.execute("Events.LoadScreenClose.Fire();d.Seal();Events.LoadScreenClose.Fire();ready();Events.GameCoreEventPublishComplete.Fire();assert(last('READINESS_SUMMARY').loadBeforeSeal==true)")

    def test_missing_module_throwing_getter_and_cleanup_separate(self):
        l=self.start();l.execute("ready();shared.ResearchCross=nil;shared.CityProgressionStore.FreshReady=function()error('bad')end;shared.Lv3Effects.ready=false;d.Seal();Events.LoadScreenClose.Fire();Events.GameCoreEventPublishComplete.Fire();local v=last('READINESS_SUMMARY');assert(v.notReady=='FR|RX' and v.controlState:find('E3_CLEANUP:PENDING',1,true))")

    def test_first_turn_sample_waits_for_late_fallback_and_no_duplicates(self):
        l=self.start();l.execute("d.Seal();Events.PlayerTurnActivated.Add(ready);Events.PlayerTurnActivated.Fire(0);assert(count('READINESS_SUMMARY')==0);Events.GameCoreEventPublishComplete.Fire();assert(last('READINESS_SUMMARY').reason=='FIRST_LOCAL_TURN' and last('READINESS_SUMMARY').notReady=='NONE');local n=#logs;Events.PlayerTurnActivated.Fire(0);Events.GameCoreEventPublishComplete.Fire();assert(#logs==n)")

    def test_early_publish_does_not_consume_first_sample(self):
        l=self.start();l.execute("Events.GameCoreEventPublishComplete.Fire();assert(count('READINESS_SUMMARY')==0);d.Seal();Events.GameCoreEventPublishComplete.Fire();assert(count('READINESS_SUMMARY')==1 and last('READINESS_SUMMARY').loadSeen==false)")


class Carrier(unittest.TestCase):
    def start(self):
        l=observer();l.execute(r"""
          names={};for _,k in ipairs({'RESEARCH','CULTURE','COMMERCE'})do names[#names+1]='BUILDING_SPC_DEV_'..k..'_SUPPORT'end
          for _,k in ipairs({'RESEARCH','CULTURE','INDUSTRY','COMMERCE'})do for i=0,7 do names[#names+1]='BUILDING_SPC_DEV_GPP_'..k..'_'..i end end
          indexes={};for i,n in ipairs(names)do indexes[n]=i end
          P.Info=function(t,n)return indexes[n] and {Index=indexes[n]}end
          present={};damage={};x=10
          b={HasBuilding=function(_,i)reads=reads+1;if unknown==i then return nil end;return present[i]==true end,
             IsPillaged=function(_,i)if unknownPillage==i then error('bad')end;return damage[i]==true end}
          c={GetID=function()return 1 end,GetX=function()return x end,GetY=function()return 5 end,GetBuildings=function()return b end}
          Players={[0]={GetCities=function()return {Members=function()return ipairs({c})end}end}}
        """)
        l.execute((M/'CarrierHealthTrace.lua').read_text());l.execute('d=SPCCarrierHealthTrace.Start(P,shared)');return l

    def test_disabled_carrier_does_not_read_native(self):
        l=self.start();l.execute("SPCExpeditionTrainingDiagnostics.ENABLED=false;Events.LoadScreenClose.Fire();Events.PlayerTurnActivated.Fire(0);assert(reads==0)")

    def test_fixed_scope_no_write_and_duplicate_turn(self):
        l=self.start();l.execute("Events.LoadScreenClose.Fire();assert(reads==35 and last('CARRIER_HEALTH_SWEEP').carrierCount==35);Events.PlayerTurnActivated.Fire(0);local n=reads;Events.PlayerTurnActivated.Fire(0);Events.PlayerTurnActivated.Fire(9);assert(reads==n and writes==0)")

    def test_missing_load_still_has_explicit_first_turn_baseline(self):
        l=self.start();l.execute("Events.PlayerTurnActivated.Fire(0);assert(last('CARRIER_HEALTH_SWEEP').reason=='FIRST_TURN_NO_LOAD' and reads==35)")

    def test_unknown_is_not_repair_and_real_recurrence_survives(self):
        l=self.start();l.execute("present[1]=true;damage[1]=true;Events.LoadScreenClose.Fire();unknownPillage=1;turn=2;Events.PlayerTurnActivated.Fire(0);assert(count('CARRIER_PILLAGE_CLEARED')==0);unknownPillage=nil;damage[1]=false;turn=3;Events.PlayerTurnActivated.Fire(0);assert(count('CARRIER_PILLAGE_CLEARED')==1);damage[1]=true;turn=4;Events.PlayerTurnActivated.Fire(0);assert(count('CARRIER_PILLAGED_PRESENT')==2 and last('CARRIER_PILLAGED_PRESENT').count==3)")

    def test_reference_replacement_does_not_inherit_pillage(self):
        l=self.start();l.execute("present[1]=true;damage[1]=true;Events.LoadScreenClose.Fire();x=20;damage[1]=false;turn=2;Events.PlayerTurnActivated.Fire(0);assert(count('CARRIER_PILLAGE_CLEARED')==0)")

    def test_native_event_only_records_owned_carrier(self):
        l=self.start();l.execute("GameEvents.BuildingPillageStateChanged.Fire(0,1,1,true);GameEvents.BuildingPillageStateChanged.Fire(9,1,1,true);GameEvents.BuildingPillageStateChanged.Fire(0,1,99,true);assert(count('CARRIER_PILLAGE_EVENT')==1)")


class CommerceNetwork(unittest.TestCase):
    def test_commerce_sampler_preserves_business_and_zero(self):
        l=commerce();l.execute(r"""
          function lastTrace(stage)for i=#ExposedMembers.SPC_B205TrainingTrace.entries,1,-1 do local v=ExposedMembers.SPC_B205TrainingTrace.entries[i];if v.stage==stage then return v end end end
          assert(toggle(2,'DISTRICT_CAMPUS',true));local before=created+removed;local rev=com.revision;local cw=commerceWrites
          Players[0].GetTreasury=function()return {GetGoldBalance=function()return 0 end,GetGoldYield=function()return 2.25 end}end
          nativeReads={};Events.PlayerTurnDeactivated.Fire(0);GameEvents.PlayerTurnStarted.Fire(0)
          local v=lastTrace('COMMERCE_TURN_STARTED');assert(v.goldBalance=='0' and v.goldYield=='2.25' and v.maintenance=='UNAVAILABLE')
          assert(v.expected==v.carrierGold and created+removed==before and com.revision==rev and commerceWrites==cw and next(nativeReads)==nil)
          Players[0].GetTreasury=function()error('PRIVATE_ERROR')end;Events.PlayerTurnDeactivated.Fire(0)
          assert(lastTrace('COMMERCE_TURN_END').goldBalance=='UNAVAILABLE')
        """)

    def test_business_outputs_match_with_diagnostics_disabled_at_start(self):
        from unittest.mock import patch
        original=Path.read_text
        results=[]
        for disabled in (False,True):
            def read(path,*a,**kw):
                value=original(path,*a,**kw)
                return value.replace('ENABLED=true','ENABLED=false',1) if disabled and path.name=='ExpeditionTrainingDiagnostics.lua' else value
            with patch.object(Path,'read_text',read):l=commerce()
            l.execute("assert(toggle(2,'DISTRICT_CAMPUS',true));business={gold=ownedGold(cities[2]),writes=created+removed,revision=com.revision,choices=commerceWrites};Events.PlayerTurnDeactivated.Fire(0);GameEvents.PlayerTurnStarted.Fire(0)")
            results.append(dict(l.globals().business.items()))
        self.assertEqual(*results)

    def test_repeated_failed_requests_remain_bounded_without_money_write(self):
        from test_b242_capital_diagnostics import rt
        l=rt();l.execute("T.failKey(T.key(source));assert(not C.confirm());for i=1,200 do refresh()end;local r=ExposedMembers.SPC_B205TrainingTrace;assert(#r.entries<=256 and moneyCalls==0 and r.suppressed==0)")

    def test_missing_carrier_visible_without_repair(self):
        l=commerce();l.execute(r"""
          Players[0].GetTreasury=function()return {}end
          assert(toggle(2,'DISTRICT_CAMPUS',true));cities[2].present.BUILDING_SPC_COMMERCE_GOLD_0=nil
          local before=created+removed;Events.PlayerTurnDeactivated.Fire(0)
          local found=false;for _,v in ipairs(ExposedMembers.SPC_B205TrainingTrace.entries)do if v.stage=='COMMERCE_TURN_CITY' and v.city=='2' and v.expected~=v.carrierGold then found=true end end
          assert(found and created+removed==before)
        """)

    def test_network_event_reason_and_recovery_no_extra_send(self):
        l=pipeline();l.execute(r"""
          GP.UnitRemovedFromMap.Fire(0,999);UP.UnitRemovedFromMap.Fire(0,999)
          local found=false;for _,v in ipairs(ExposedMembers.SPC_B205TrainingTrace.entries)do if v.stage=='NETWORK_PENDING' and v.reason=='UNITREMOVEDFROMMAP'then found=true end end
          assert(found and requests==0);UP.GameCoreEventPublishComplete.Fire();assert(requests==1 and pub.senderResult=='SENT' and pub.senderFailedTurn=='NONE')
        """)

    def test_network_signal_stale_has_observation_without_mutation(self):
        l=commerce();l.execute(r"""
          shared.RouteSignalRevision=(shared.RouteSignalRevision or 0)+1;local before=created+removed
          local v=net.CurrentDomesticPartners(0,cities[2]);assert(v.validity=='UNKNOWN')
          local found=false;for _,v in ipairs(ExposedMembers.SPC_B205TrainingTrace.entries)do if v.stage=='NETWORK_SIGNAL_STALE'then found=true end end
          assert(found and created+removed==before)
        """)

    def test_network_reject_safe_reason_and_no_accept(self):
        l=commerce();l.execute(r"""
          local rev=net.Input(0).inputVersion
          net.Receive(0,{Epoch=net.epoch,Seq=999,Turn=Game.GetCurrentGameTurn(),Signal=shared.RouteSignalRevision or 0,Valid=1,Count=1,Data='bad'})
          local found=false;for _,v in ipairs(ExposedMembers.SPC_B205TrainingTrace.entries)do if v.stage=='NETWORK_RECEIVE_REJECT' and v.reason=='ROW_FORMAT' and v.packetSeq=='999'then found=true end end
          assert(found and net.Input(0).inputVersion==rev)
        """)


class Collection(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(dir=R/'local');self.s=collector.Session(root=Path(self.tmp.name),stamp='B267')
    def tearDown(self):
        self.s.close();self.tmp.cleanup()

    def test_meta_stored_and_increment_alerts(self):
        line=reader.PREFIX+'META schema=205 sequence=9 suppressed=2 errors=1 sampleSuppressed=4 sinkStatus=BUDGET_STOP'
        self.s.add_meta(line);self.s.add_meta(line)
        self.assertEqual(len(self.s.alerts),4)
        self.assertIn('meta '+line,(self.s.directory/'records.log').read_text())

    def test_readiness_preload_no_false_alert_and_missing_load_summary(self):
        self.s.add('[SPC][B205][TRAIN] seq=1 stage=READINESS_SUMMARY context=R1 reason=FIRST_PUBLISH sealed=true loadSeen=false notReady=FR','live')
        self.assertFalse(self.s.alerts);self.s.summary('TEST');self.assertIn('READINESS_LOAD_SAMPLE_MISSING',self.s.alerts[0])

    def test_readiness_afterload_and_throttle_alert(self):
        self.s.add('[SPC][B205][TRAIN] seq=1 stage=READINESS_SUMMARY context=R1 reason=AFTER_LOAD sealed=true loadSeen=true notReady=FR','live')
        self.s.add('[SPC][B205][TRAIN] seq=2 stage=TRACE_THROTTLED traceRole=X turn=8','live')
        self.assertEqual(len(self.s.alerts),2)

    def test256_entry_snapshot_command_runs_actual_lua(self):
        l=LuaRuntime();l.execute("ExposedMembers={SPC_B205TrainingTrace={schema=205,sequence=256,entries={}}};out={};print=function(s)out[#out+1]=s end;for i=1,256 do ExposedMembers.SPC_B205TrainingTrace.entries[i]={line='[SPC][B205][TRAIN] seq='..i..' stage=TEST'}end")
        l.execute(reader.command('trace','MARK ','DONE'))
        self.assertEqual(l.eval('#out'),258)
        self.assertIn('ENTRY 256',l.eval('out[257]'))

    def test_actual_reader_accepts_more_than1024_passive_rows(self):
        from test_expedition_trace_reader import frame
        class Socket(TraceSocket):
            def sendall(self,value):
                super().sendall(value)
                if value[8:].startswith(b'CMD:'):
                    for i in range(1500):self.incoming.extend(frame(0xffffffff,'0\0[SPC][B205][TRAIN] seq=%d stage=TEST\0'%i))
        clock=FakeClock();sock=Socket([],clock,1);rows=[]
        reader.capture('record',connect=lambda *a,**k:sock,clock=clock,on_record=rows.append,record_seconds=1)
        self.assertEqual(sum(x.startswith(reader.TRAIN_PREFIX) for x in rows),1500)


    def test_ring_gap_is_explicit_and_epoch_reset_is_not_old_continuity(self):
        self.s.add_meta(reader.PREFIX+'META traceEpoch=ONE firstSequence=100 sequence=355 suppressed=0 errors=0')
        self.assertTrue(any('TRACE_RING_GAP' in a for a in self.s.alerts))
        self.s.highest_sequence=355
        self.s.add_meta(reader.PREFIX+'META traceEpoch=TWO firstSequence=1 sequence=2 suppressed=0 errors=0')
        self.assertEqual(self.s.highest_sequence,0)

    def test_reader_total_byte_guard_at_new_limit(self):
        from test_expedition_trace_reader import FakeSocket,frame
        fake=FakeSocket(initial=frame(5,b'x'*reader.MAX_FRAME)*9,chunk=reader.MAX_FRAME)
        with self.assertRaisesRegex(reader.CaptureError,'TOTAL_BYTE_LIMIT'):
            reader.capture('trace',connect=lambda *a,**k:fake,clock=lambda:1.0)

    def test_snapshot_output_cap_still_rejects_oversized_response(self):
        clock=FakeClock();sock=TraceSocket(['META schema=205']*(reader.MAX_RECORDS+1),clock,1)
        with self.assertRaisesRegex(reader.CaptureError,'OUTPUT_RECORD_LIMIT'):
            reader.capture('trace',connect=lambda *a,**kw:sock,clock=clock)

    def test_capture_limit_records_gap(self):
        clock=FakeClock()
        def cap(*a,**k):raise reader.CaptureError('TOTAL_BYTE_LIMIT','PASSIVE')
        collector.run(self.s,capture=cap,clock=clock,sleep=clock.sleep,max_seconds=1,out=lambda s:None)
        self.assertIn('capture_gap',(self.s.directory/'events.jsonl').read_text())


class Package(unittest.TestCase):
    def test_actual_lua51_syntax_and_manifest_closure(self):
        from lupa.lua51 import LuaRuntime as Lua51
        l=Lua51();compile=l.eval('function(s)local f,e=loadstring(s);return f~=nil,e end')
        for path in M.rglob('*.lua'):
            ok,error=compile(path.read_text());self.assertTrue(ok,(path.name,error))
        root=ET.parse(M/'SpecializationP0.modinfo').getroot()
        registered={v.text for v in root.findall('./Files/File')}
        actual={str(p.relative_to(M))for p in M.rglob('*')if p.is_file()and p.name not in ('.DS_Store','SpecializationP0.modinfo')}
        self.assertEqual(registered,actual)
        for name in ('ReadinessSummary.lua','CarrierHealthTrace.lua'):
            self.assertIn(name,{v.text for v in root.findall('./InGameActions/ImportFiles/File')})

    def test_gate_against_configured_engine_database_schema(self):
        import zlib
        from project_paths import external_database
        with sqlite3.connect(external_database(R).as_uri()+'?mode=ro',uri=True) as src:
            db=sqlite3.connect(':memory:');src.backup(db)
        db.create_function('Make_Hash',1,lambda text:zlib.crc32(text.encode()))
        db.execute("DELETE FROM Projects WHERE ProjectType='PROJECT_SPC_OVERFLOW_SINK_TEST'")
        db.execute("DELETE FROM Buildings WHERE BuildingType='BUILDING_SPC_OVERFLOW_TEST_DISABLED'")
        db.execute("DELETE FROM Types WHERE Type IN ('PROJECT_SPC_OVERFLOW_SINK_TEST','BUILDING_SPC_OVERFLOW_TEST_DISABLED')")
        db.executescript((M/'Data/OverflowSinkTest.sql').read_text())
        row=db.execute("SELECT p.Cost,b.InternalOnly,b.CitizenSlots,b.Housing FROM Projects p JOIN Buildings b ON p.RequiredBuilding=b.BuildingType WHERE p.ProjectType='PROJECT_SPC_OVERFLOW_SINK_TEST'").fetchone()
        self.assertEqual(row,(1000000,1,0,0));db.close()

    def test_gate_schema_and_exact_project_no_grant(self):
        # Engine-schema integration is separately exercised against read-only DB.
        db=sqlite3.connect(':memory:')
        db.executescript('CREATE TABLE Types(Type PRIMARY KEY,Kind);CREATE TABLE Projects(ProjectType PRIMARY KEY,Name,ShortName,Description,Cost,CostProgressionModel,PrereqDistrict,RequiredBuilding);CREATE TABLE Buildings(BuildingType PRIMARY KEY,Name,Cost,PrereqDistrict,InternalOnly,CitizenSlots,Housing);')
        db.executescript((M/'Data/OverflowSinkTest.sql').read_text())
        self.assertEqual(db.execute('SELECT Cost,RequiredBuilding FROM Projects').fetchone(),(1000000,'BUILDING_SPC_OVERFLOW_TEST_DISABLED'))
        self.assertEqual(db.execute('SELECT InternalOnly,CitizenSlots,Housing FROM Buildings').fetchone(),(1,0,0))
        for p in M.rglob('*.lua'):self.assertNotIn('BUILDING_SPC_OVERFLOW_TEST_DISABLED',p.read_text())

if __name__=='__main__':unittest.main()
