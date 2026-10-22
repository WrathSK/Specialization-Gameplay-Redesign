"""B224 real Lua context/empty-wire regressions; no native settlement claim."""
import unittest
import test_expedition_missions as missions
from test_expedition_idle_actions import fixture as panel
from test_expedition_spy_task import R
from test_p0_k import Fixture, PRODUCER
import test_great_work_notifications as consumers

class WorkContext(unittest.TestCase):
 def ready(self): return missions.Missions().ready()
 def test_ui_reader_without_gameplay_getters_start_and_due(self):
  self.ready().execute("""
   assert(targetCity:GetBuildings().GetGreatWorkInSlot==nil)
   assert(targetCity:GetBuildings().GetGreatWorkTypeFromIndex==nil)
   local r=startMission('w',WORKS);assert(r.phase=='TASK_RUNNING' and r.missionWorkID==nil)
   local n=slotReads;currentTurn=85;ownTurn(2)
   assert(slotReads>n and insightWrites==1 and req('READ','done').taskOutcome=='SUCCESS')
  """)
 def test_stale_or_missing_sample_does_not_start(self):
  for change in ["ExposedMembers.SPC_ExpeditionWorkRead=nil",
   "ExposedMembers.SPC_ExpeditionWorkRead=function()error('unavailable')end",
   "ExposedMembers.SPC_ExpeditionWorkRead=function(...)local r=original(...);r.turn=r.turn-1;return r end",
   "ExposedMembers.SPC_ExpeditionWorkRead=function(...)local r=original(...);r.city=99;return r end",
   "ExposedMembers.SPC_ExpeditionWorkRead=function(...)local r=original(...);r.status=nil;return r end"]:
   with self.subTest(change=change):
    l=self.ready();l.execute('local original=ExposedMembers.SPC_ExpeditionWorkRead;'+change+";local r=startMission('w',WORKS);assert(r.phase=='ARRIVED' and r.missionStatus=='UNKNOWN' and insightWrites==0 and not r.activityKey)")
 def test_zero_instance_and_replacement_remain_city_valid(self):
  self.ready().execute("""
   uiMissionBuildings.GetGreatWorkInSlot=function()return slotWork end
   uiMissionBuildings.GetGreatWorkTypeFromIndex=function()return 77 end
   slotWork=0;local r=startMission('w',WORKS);assert(r.missionWorkID==nil and r.phase=='TASK_RUNNING')
   slotWork=1;currentTurn=85;ownTurn(2)
   assert(req('READ','changed').taskOutcome=='SUCCESS' and insightWrites==1)
  """)
 def test_ui_reference_changes_during_native_read_rejected(self):
  self.ready().execute("""
   local original=uiMissionBuildings.GetGreatWorkInSlot
   uiMissionBuildings.GetGreatWorkInSlot=function(...)local id=original(...);currentTurn=currentTurn+1;return id end
   local r=startMission('w',WORKS);assert(r.phase=='ARRIVED' and r.missionStatus=='UNKNOWN' and insightWrites==0)
  """)

class ReaderRegistration(unittest.TestCase):
 def test_activity_installs_without_panel_and_shutdown_owns_only_its_reader(self):
  from test_expedition_spy_activity_integration import integrated
  l=integrated(window=False);l.execute("""
   assert(type(SPCExpeditionSpyRead.WorksCity)=='function')
   assert(ExposedMembers.SPC_ExpeditionWorkRead==SPCExpeditionSpyRead.WorksCity)
   activityShutdown();assert(ExposedMembers.SPC_ExpeditionWorkRead==nil)
   activityInit();local replacement=function()end
   ExposedMembers.SPC_ExpeditionWorkRead=replacement
   activityShutdown();assert(ExposedMembers.SPC_ExpeditionWorkRead==replacement)
  """)

class EmptyWire(unittest.TestCase):
 def test_empty_wire_roundtrip_after_last_work_sale(self):
  fx=Fixture();fx.check('a.slots[10]={100};');fx.lua.execute(PRODUCER);fx.lua.execute((R/'Mod/UI/DialogueRefresh.lua').read_text())
  fx.check("""
   init();assert(shared.GreatWorkFacts.Summary(0,7).eraCount>0)
   local original=UI.RequestPlayerOperation
   UI.RequestPlayerOperation=function(pid,op,p)
    for k,v in pairs(p)do if v==''then p[k]=nil end end
    if p.FactsCount==0 then assert(p.FactsData=='EMPTY')end
    return original(pid,op,p)
   end
   for _,c in ipairs(citylist)do c.slots={[10]={},[20]={}}end
   fire('GreatWorkMoved',0,7,1,1);fire('GreatWorkMoved',0,8,1,1);fire('GameCoreEventPublishComplete')
   assert(shared.GreatWorkFacts.state=='VERIFIED')
   for _,id in ipairs({7,8,9})do local s=shared.GreatWorkFacts.Summary(0,id);assert(s.eraCount==0 and s.count==0 and s.availability=='KNOWN')end
  """)
 def test_marker_requires_exact_zero_and_missing_data_stays_unknown(self):
  for change,code in [("p.FactsData='EMPTY';p.FactsCount=1",'GW_WORK_FORMAT'),("p.FactsData=nil",'GW_SAMPLE_SIZE')]:
   with self.subTest(change=change):
    fx=Fixture();fx.check("local p=packet(1,{});"+change+";local ok,why=shared.GreatWorkFacts.Receive(0,p);assert(not ok and why=='"+code+"')")

class EmptyConsumers(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  consumers.CultureIntegrationTests.setUpClass()
 @classmethod
 def tearDownClass(cls): consumers.CultureIntegrationTests.tearDownClass()
 def runtime(self): return consumers.CultureIntegrationTests().runtime()
 def test_explicit_zero_withdraws_all_three_real_consumers(self):
  l=self.runtime();l.execute("""
   sample(1,1,0);assert(total(a)>0 and meaningCount(a)>0 and inspiration(a)==3)
   local p=packet(2,0,0);p.FactsData='EMPTY';meaningRequest(0,p)
   assert(total(a)==0 and meaningCount(a)==0 and inspiration(a)==0)
   local n=writes;p=packet(3,0,0);p.FactsData='EMPTY';meaningRequest(0,p);assert(writes==n)
  """)

 def test_city_zero_does_not_clear_other_city_and_unknown_is_not_zero(self):
  l=self.runtime();l.execute("""
   sample(1,1,1);sample(2,0,1)
   assert(total(a)==0 and meaningCount(a)==0 and inspiration(a)==0)
   assert(total(b)>0 and meaningCount(b)>0 and inspiration(b)==3)
   sample(3,1,1);local before=total(a)
   local p=packet(4,0,0);p.FactsData=nil;meaningRequest(0,p)
   assert(shared.GreatWorkFacts.lastError=='GW_SAMPLE_SIZE' and total(a)==before and inspiration(a)==3)
   p=packet(5,0,0);p.FactsData='EMPTY';p.Valid=0;p.FactsRefs=p.FactsRefs:gsub(',1;',',0;');meaningRequest(0,p)
   assert(total(a)==before and meaningCount(a)>0 and inspiration(a)==3)
   p=packet(6,0,0);p.FactsData='EMPTY';meaningRequest(0,p)
   assert(total(a)==0 and total(b)==0 and meaningCount(a)==0 and meaningCount(b)==0 and inspiration(a)==0 and inspiration(b)==0)
  """)

class IdleCurrent(unittest.TestCase):
 def test_stale_selected_wrapper_uses_current_identity(self):
  l=panel();l.execute("""
   phase('ARRIVED');local live=team
   selected=setmetatable({stale=true},{__index=team})
   UnitManager.CanStartOperation=function(u)return not u.stale end
   Events.GameCoreEventPublishComplete()
   assert(#rendered.INPLACE==2 and not rendered.INPLACE[1].disabled)
   rendered.INPLACE[1].CallbackFunc();assert(#requests==1 and requests[1].hash==8)
   rendered.INPLACE[2].CallbackFunc();assert(#requests==2 and requests[2].hash==9)
   UnitManager.CanStartOperation=function(u)return not u.stale and not sleeping end
   Events.UnitActivityChanged(2,40);assert(#rendered.INPLACE==1 and rendered.INPLACE[1].icon=='wake')
   rendered.INPLACE[1].CallbackFunc();assert(#requests==3 and requests[3].hash==10 and not sleeping)
  """)
 def test_denied_error_nil_remain_distinct_and_event_recovers(self):
  l=panel();l.execute("""
   phase('ARRIVED');available=false;Events.GameCoreEventPublishComplete();local n=calls.Refresh
   assert(#rendered.INPLACE==2 and rendered.INPLACE[1].disabled)
   throws=true;Events.GameCoreEventPublishComplete();assert(calls.Refresh==n+1)
   throws=false;unknown=true;Events.GameCoreEventPublishComplete();assert(calls.Refresh==n+2)
   unknown=false;available=true;Events.UnitOperationDeactivated(2,40)
   assert(#rendered.INPLACE==2 and not rendered.INPLACE[1].disabled and #requests==0)
  """)

class CurrentPackage(unittest.TestCase):
 def test_version_files_and_bilingual_idle_reasons(self):
  import sqlite3
  import xml.etree.ElementTree as ET
  root=ET.parse(R/'Mod/SpecializationP0.modinfo').getroot()
  self.assertEqual(root.get('version'),'254')
  for item in root.findall('.//File'):
   self.assertTrue((R/'Mod'/item.text).is_file(),item.text)
  db=sqlite3.connect(':memory:')
  try:
   db.execute('CREATE TABLE LocalizedText(Language TEXT, Tag TEXT, Text TEXT, PRIMARY KEY(Language,Tag))')
   db.executescript((R/'Mod/Text/ExpeditionGate.sql').read_text())
   for reason in ['DENIED','UNAVAILABLE','READ_ERROR']:
    for lang in ['zh_Hans_CN','en_US']:
     text=db.execute('SELECT Text FROM LocalizedText WHERE Language=? AND Tag=?',(lang,'LOC_SPC_EXPEDITION_IDLE_'+reason)).fetchone()
     self.assertTrue(text and text[0])
  finally: db.close()

if __name__=='__main__': unittest.main()
