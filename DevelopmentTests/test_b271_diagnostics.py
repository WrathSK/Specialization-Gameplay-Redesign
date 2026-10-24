"""B271 isolated Lua 5.1 observations and copied engine DB; no game connection."""
import importlib.util
from pathlib import Path
import sqlite3
import tempfile
import unittest
import xml.etree.ElementTree as ET
from lupa.lua51 import LuaRuntime
from project_paths import external_database
R=Path(__file__).resolve().parents[1]
def load(path):
 s=importlib.util.spec_from_file_location('b271_'+path.stem,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
collector=load(R/'tools/collect_expedition_trace.py')
class Diagnostics(unittest.TestCase):
 def setUp(self):
  self.l=LuaRuntime(unpack_returned_tuples=True)
  self.l.execute('''turn=1;gold=100.125;reads=0;writes=0;test=true;prints={}
   print=function(x)prints[#prints+1]=x end
   Game={GetLocalPlayer=function()return 0 end,GetCurrentGameTurn=function()return turn end}
   ExposedMembers={};shared={NetworkBridge={players={[0]={availability='NEEDS_REVALIDATION',revalidation='PENDING'}}}}
   local function events()return setmetatable({},{__index=function(t,k)local e={callbacks={}};e.Add=function(f)e.callbacks[#e.callbacks+1]=f end;e.Remove=function(f)for i=#e.callbacks,1,-1 do if e.callbacks[i]==f then table.remove(e.callbacks,i)end end end;e.Fire=function(...)for _,f in ipairs(e.callbacks)do f(...)end end;t[k]=e;return e end})end
   Events=events();GameEvents=events();LuaEvents={};
   Players={[0]={GetTreasury=function()return {GetGoldBalance=function()reads=reads+1;return gold end,GetGoldYield=function()return 7.5 end}end}}
   P={Field=function(o,k)return o and o[k]end,IsTestPlayer=function(p)return test and p==0 end}
   local function forbidden()writes=writes+1;error('diagnostic attempted mutation')end
   P.SetProperty=forbidden;P.CreateBuilding=forbidden;P.RemoveBuilding=forbidden;P.Audit=forbidden;P.Mark=forbidden
  ''')
  for name in ['PerformanceCounters','ExpeditionTrainingDiagnostics','EventTimingDiagnostics']:
   self.l.execute((R/f'Mod/{name}.lua').read_text())
  self.l.execute("ExposedMembers.SPC_Performance=SPCPerformance.New();gp=SPCEventTimingDiagnostics.Start(P,shared,'GAMEPLAY');ui=SPCEventTimingDiagnostics.Start(P,nil,'UI')")
 def rows(self,stage=None):
  rows=[dict(v.items()) for v in self.l.eval('ExposedMembers.SPC_B205TrainingTrace.entries').values()]
  return [v for v in rows if not stage or v.get('stage')==stage]
 def cycle(self):
  self.l.execute('''Events.PlayerTurnDeactivated.Fire(0);Events.LocalPlayerTurnEnd.Fire();Events.PlayerTurnActivated.Fire(1);Events.PlayerTurnActivated.Fire(2);turn=turn+1;GameEvents.PlayerTurnStarted.Fire(0);gold=gold+7.5;gp.Verified(0,shared.NetworkBridge.players[0]);Events.PlayerTurnActivated.Fire(0);Events.LocalPlayerTurnBegin.Fire();Events.GameCoreEventPublishComplete.Fire()''')
 def test_default_points_precision_dedup_and_no_writes(self):
  self.cycle();self.l.execute('Events.LocalPlayerTurnBegin.Fire();Events.GameCoreEventPublishComplete.Fire();Events.PlayerTurnActivated.Fire(0)')
  rows=self.rows('TREASURY_POINT');self.assertEqual(len(rows),6);self.assertEqual(self.l.eval('reads'),6)
  self.assertEqual(rows[0]['goldBalance'],'100.125');self.assertEqual(rows[-1]['goldBalance'],'107.625')
  self.assertEqual(len({v['observationSeq'] for v in rows}),6)
  self.assertFalse(any(v['stage'].startswith('EVENT_ORDER') for v in self.rows()))
  self.assertEqual(self.l.eval('writes'),0)
  self.assertIsNone(self.l.eval('ExposedMembers.SPC_EventTiming.observerErrors'))
  summary='\n'.join(self.summary());self.assertIn('FIRST_OBSERVED_CHANGE relation=AFTER_OBSERVED_VERIFIED',summary)
  self.assertNotIn('treasury_missing',summary)
 def summary(self):
  m=collector.TurnTimingEvidence()
  for row in self.rows():m.add(row)
  return m.summary()
 def test_six_turn_stop_and_reload(self):
  for _ in range(9):self.cycle()
  before=self.l.eval('reads');self.assertFalse(self.l.eval('ExposedMembers.SPC_EventTiming.accepting'))
  self.cycle();self.assertEqual(before,self.l.eval('reads'))
  self.l.execute("gp.Stop();ui.Stop();gp=SPCEventTimingDiagnostics.Start(P,shared,'GAMEPLAY');ui=SPCEventTimingDiagnostics.Start(P,nil,'UI')")
  self.assertFalse(self.l.eval('ExposedMembers.SPC_EventTiming.sequenceEnabled'));self.cycle();self.assertGreater(self.l.eval('reads'),before)
 def test_foreign_test_player_guard(self):
  self.l.execute('test=false');self.cycle();self.assertEqual(self.l.eval('reads'),0);self.assertEqual(self.rows('TREASURY_POINT'),[])
 def test_missing_native_reads(self):
  self.l.execute('Players[0].GetTreasury=function()return {}end');self.cycle()
  self.assertTrue(all(v['goldBalance']=='UNAVAILABLE' and v['goldYield']=='UNAVAILABLE' for v in self.rows('TREASURY_POINT')))
 def test_cap_and_per_side_global_order(self):
  self.l.execute("gp.Toggle(0);Events.PlayerTurnDeactivated.Fire(0);for i=1,500 do Events.CityWorkerChanged.Fire(0,17)end")
  ends=self.rows('EVENT_ORDER_END');self.assertEqual(len(ends),2)
  self.assertTrue(all(v['eventTotal']=='400' and v['eventTruncated']=='true' for v in ends))
  batches=self.rows('EVENT_ORDER_BATCH');events=[x.split(':') for b in batches for x in b['eventBatch'].split('|')]
  self.assertEqual(len(events),800);self.assertEqual(len({x[0] for x in events}),800)
  self.assertTrue(all(len(v['line'])<=4096 for v in self.rows()))
  self.assertFalse(any(v.get('eventBatch')=='REDACTED' for v in batches))
  self.assertIn('complete=False','\n'.join(self.summary()))
 def test_publish_only_count_terminal_and_disabled(self):
  self.l.execute('gp.Toggle(0);Events.PlayerTurnDeactivated.Fire(0);Events.GameCoreEventPublishComplete.Fire();Events.GameCoreEventPublishComplete.Fire();Events.LocalPlayerTurnBegin.Fire()')
  self.assertTrue(all(v['eventPublishCount']=='2' and v['eventTruncated']=='false' for v in self.rows('EVENT_ORDER_END')))
  self.assertFalse(any('GameCoreEventPublishComplete' in v['eventBatch'] for v in self.rows('EVENT_ORDER_BATCH')))
  self.assertTrue(any('LocalPlayerTurnBegin' in v['eventBatch'] for v in self.rows('EVENT_ORDER_BATCH')))
  self.l.execute('turn=2;Events.PlayerTurnDeactivated.Fire(0);gp.Toggle(0);Events.CityWorkerChanged.Fire(0,5)')
  self.assertTrue(any(v['reason']=='DISABLED' for v in self.rows('EVENT_ORDER_END')))
 def test_unknown_counters_and_delta_not_reset(self):
  self.l.execute("SPCPerformance.Observe('audit','CultureAesthetic');SPCPerformance.Observe('audit','NewUnknown');SPCPerformance.Observe('dispatch','FutureEvent');Events.PlayerTurnDeactivated.Fire(0)")
  r=self.rows('TURN_EVENT_COUNTS')[0]['counterBatch'];self.assertIn('audit:CultureAesthetic:1',r);self.assertIn('audit:OTHER:1',r);self.assertIn('dispatch:OTHER:1',r)
  self.l.execute('Events.PlayerTurnActivated.Fire(0)');self.assertIn('audit:TOTAL:0',self.rows('TURN_EVENT_COUNTS')[-1]['counterBatch'])
  self.assertEqual(self.l.eval('ExposedMembers.SPC_EventTiming.counts.audit.OTHER'),1)
 def test_listener_errors_do_not_interrupt_originals(self):
  self.l.execute('tail=0;Events.CityWorkerChanged.Add(function()tail=tail+1 end);gp.Toggle(0);Events.PlayerTurnDeactivated.Fire(0);Game.GetCurrentGameTurn=function()error("native unavailable")end;Events.CityWorkerChanged.Fire(0,4)')
  self.assertEqual(self.l.eval('tail'),1);self.assertEqual(self.l.eval('ExposedMembers.SPC_EventTiming.observerErrors'),2)
 def test_unknown_city_not_guessed(self):
  self.l.execute('gp.Toggle(0);Events.PlayerTurnDeactivated.Fire(0);Events.BuildingAddedToMap.Fire(30,40,9,0);Events.LocalPlayerTurnBegin.Fire()')
  self.assertTrue(any('Events.BuildingAddedToMap:UNKNOWN:UNKNOWN:' in v['eventBatch'] for v in self.rows('EVENT_ORDER_BATCH')))
class Evidence(unittest.TestCase):
 def test_transport_roundtrip(self):
  row='[SPC][B205][TRAIN] seq=1 stage=TURN_EVENT_COUNTS observationEpoch=e observationSeq=1 point=LOCAL_END counterBatch=audit:OTHER:3'
  self.assertEqual(collector.train_line(row),row)
  m=collector.TurnTimingEvidence();m.add(collector.fields(row));self.assertIn('audit:OTHER:3','\n'.join(m.summary()))
 def test_session_records_and_summary(self):
  with tempfile.TemporaryDirectory(dir=R/'local') as tmp:
   session=collector.Session(Path(tmp));self.addCleanup(session.close)
   record='[SPC][B205][TRAIN] seq=1 stage=TREASURY_POINT observationEpoch=e observationSeq=1 observationCycle=1 turn=2 point=LOCAL_BEGIN goldBalance=100.125 goldYield=7.5'
   session.add(record,'fixture');session.add(record,'fixture')
   self.assertEqual(session.record_total,1)
   text=session.summary('FIXTURE');self.assertIn('gold=100.125',text)
   self.assertIn(record,(session.directory/'records.log').read_text())
 def test_missing_and_truncation(self):
  m=collector.TurnTimingEvidence();m.add(dict(stage='EVENT_ORDER_START',observationSeq='1',observerSide='UI'))
  m.add(dict(stage='TREASURY_POINT',observationSeq='2',point='LOCAL_BEGIN',goldBalance='UNAVAILABLE'))
  self.assertIn('end_missing=true','\n'.join(m.summary()));self.assertIn('treasury_missing','\n'.join(m.summary()))
  m.LIMIT=2;m.add(dict(stage='EVENT_ORDER_END'));self.assertEqual(m.dropped,1);self.assertIn('timing_summary_truncated: 1','\n'.join(m.summary()))
class RealInputPillage(unittest.TestCase):
 def test_current_depth_and_consumers(self):
  l=LuaRuntime(unpack_returned_tuples=True)
  for name in ['DistrictCompleteness','CultureAestheticModel','CultureMeaningModel','ResearchChairModel']:
   l.execute((R/f'Mod/{name}.lua').read_text())
  l.execute("""
   catalog={revision=1,Domain=function(t)return t end,District=function(t)return t end,buildings={
    [1]={type='LIBRARY',tier=2,ordinary=true,domain='DISTRICT_CAMPUS',ordinaryDistrict='DISTRICT_CAMPUS'},
    [2]={type='BUILDING_SPC_TEST',ordinary=false,reason='INTERNAL'}}}
   raw={districts={{id=1,type='DISTRICT_CAMPUS',plot=10,complete=true,pillaged=false,buildings={
    {index=1,complete=true,pillaged=false},{index=2,complete=true,pillaged=false}}}}}
   f={validity='VERIFIED',identity='CULTURE',activeStatus='KNOWN',active=4,potential=4,first={districtID=1,type='DISTRICT_CAMPUS'}}
   w={hasConfirmed=true,availability='KNOWN',eraCount=2,count=2,modifierExcludedCount=0,unknownCategoryCount=0}
   for phase=1,4 do
    raw.districts[1].pillaged=phase==3;raw.districts[1].buildings[1].pillaged=phase==2
    local view={validity='VERIFIED',availability='READY',value=SPCDistrictCompleteness.Calculate(catalog,raw)}
    local intact=phase==1 or phase==4
    assert((view.value.domains.DISTRICT_CAMPUS and view.value.domains.DISTRICT_CAMPUS.value or 0)==(intact and 2 or 0))
    f.identity='CULTURE'
    assert(SPCCultureAestheticModel.Plan(f,w,view).total==(intact and 2 or 0))
    assert(SPCCultureMeaningModel.Plan(f,w,view).total.SCIENCE==(intact and 2 or 0))
    f.identity='RESEARCH'
    assert(SPCResearchChairModel.Plan(f,view,3,{LIBRARY=true}).total==(intact and 3 or 0))
   end
  """)
class CarrierSQL(unittest.TestCase):
 def test_actual_engine_schema_copy(self):
  source=sqlite3.connect(external_database(R).as_uri()+'?mode=ro',uri=True)
  db=sqlite3.connect(':memory:');source.backup(db);source.close()
  target={x[0] for x in db.execute("SELECT BuildingType FROM Buildings WHERE InternalOnly=1 AND substr(BuildingType,1,13)='BUILDING_SPC_'")}
  self.assertGreater(len(target),4000)
  before=list(db.execute('SELECT * FROM Buildings_XP2 ORDER BY BuildingType'))
  self.assertFalse(target & {x[0] for x in before})
  schema={x[1]:x for x in db.execute('PRAGMA table_info(Buildings_XP2)')};self.assertEqual(schema['Pillage'][4],'1')
  sql=(R/'Mod/Data/InternalCarrierPillage.sql').read_text();db.executescript(sql)
  after=list(db.execute('SELECT * FROM Buildings_XP2 ORDER BY BuildingType'))
  self.assertEqual([x for x in after if x[0] not in target],before)
  self.assertEqual({x[0] for x in db.execute('SELECT BuildingType FROM Buildings_XP2 WHERE Pillage=0')} & target,target)
  self.assertEqual(len(after)-len(before),len(target));db.executescript(sql);self.assertEqual(list(db.execute('SELECT * FROM Buildings_XP2 ORDER BY BuildingType')),after)
  print('B271 copied-engine target rows:',len(target));db.close()
 def test_load_order(self):
  root=ET.parse(R/'Mod/SpecializationP0.modinfo').getroot()
  actions=root.find('InGameActions').findall('UpdateDatabase')
  order=int(next(a for a in actions if a.get('id')=='SPC_InternalCarrierPillage').findtext('Properties/LoadOrder'))
  for a in actions:
   if a.get('id')=='SPC_InternalCarrierPillage':continue
   for f in a.findall('File'):
    if 'InternalOnly' in (R/'Mod'/f.text).read_text():self.assertLess(int(a.findtext('Properties/LoadOrder') or '0'),order)
if __name__=='__main__':unittest.main()
