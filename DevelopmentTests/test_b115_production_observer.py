"""Actual B115 gameplay observer + UI fixtures; does not prove native event order."""
import unittest
import xml.etree.ElementTree as ET
from lupa.lua55 import LuaRuntime
import test_b114_notification_target as previous
prior=previous.prior
GP=(prior.ROOT/'Mod/TimedProductionProbe.lua').read_text()
UI=(prior.ROOT/'Mod/UI/TimedTurnProbe.lua').read_text()
BRIDGE=r'''
for _,n in ipairs({'CityProductionQueueChanged','CityProductionUpdated','CityProductionCompleted','PlayerTurnDeactivated','GameCoreEventPublishComplete'}) do Events[n]=event() end
GameEvents={PlayerTurnStarted=event()};PlayerOperations={EXECUTE_SCRIPT=1}
SPCP0.Field=function(o,k) return o and o[k] end
SPCP0.Call=function(o,k,...) if not o or not o[k] then return false,'MISSING' end;return pcall(o[k],o,...) end
ExposedMembers.SPC_P0={};gpReads=0;gpTarget='';defer=false;packets={}
a.GetBuildQueue=function() return {GetSize=function() return queue end,
 CurrentlyBuilding=function() gpReads=gpReads+1;return gpTarget end,
 GetCurrentProductionTypeHash=function() return 0 end} end
UI.RequestPlayerOperation=function(pid,op,p)
 packets[#packets+1]=p
 if not defer then ExposedMembers.SPC_P0.TimedProductionProbe.Request(pid,p) end
end
GameInfo.Buildings={};GameInfo.Districts={};GameInfo.Units={};GameInfo.Projects={}
'''
class ObserverTests(previous.TargetTests):
 def setUp(self):
  self.lua=LuaRuntime(unpack_returned_tuples=True)
  self.lua.execute(prior.FIXTURE+prior.EXTRA+previous.TARGET+BRIDGE)
  self.lua.execute(GP);self.lua.execute('SPCTimedProductionProbe.Start(SPCP0,ExposedMembers.SPC_P0)');self.lua.execute(UI)
 def status(self):return self.get('ExposedMembers.SPC_P0.TimedProduction.status')
 def test_static(self):
  for f in ['Mod/Gameplay.lua','Mod/TimedProductionProbe.lua','Mod/UI/TimedTurnProbe.lua','Mod/Probe.lua']:
   self.lua.execute('assert(load(...))',(prior.ROOT/f).read_text())
  doc=ET.parse(prior.ROOT/'Mod/SpecializationP0.modinfo');self.assertEqual(doc.getroot().get('version'),'142')
  self.assertTrue(all((prior.ROOT/'Mod'/n.text).is_file() for n in doc.findall('./Files/File')))
  for x in ['SetProperty','AddProgress','FinishProgress','RequestOperation','SetUpdate']:
   self.assertNotIn(x,GP)
 def test_lifecycle_and_save_session(self):
  # B115 adds a gameplay observation; reload must begin without a saved activity.
  self.arm();self.click();self.runlua('Events.PlayerTurnDeactivated(0);turn=21;GameEvents.PlayerTurnStarted(0);Events.PlayerTurnActivated(0);refreshHandler()')
  self.assertEqual(self.status(),'ENDED');self.assertEqual(self.get('requests'),1)
  self.assertEqual(self.get('Controls.EndTurnText.text'),'NATIVE')
  self.setUp();self.click();self.assertEqual(self.get('requests'),0);self.assertIsNone(self.get('ExposedMembers.SPC_P0.TimedProduction'))
 def test_async_ack_required(self):
  self.runlua('defer=true');self.arm();self.click();self.assertEqual(self.get('requests'),0)
  self.runlua('ExposedMembers.SPC_P0.TimedProductionProbe.Request(0,packets[1]);Events.GameCoreEventPublishComplete();refreshHandler()')
  self.click();self.assertEqual(self.get('requests'),1)
 def test_switch_clear_interrupt(self):
  self.arm();self.runlua("gpTarget='BUILDING_TEST';queue=1;Events.CityProductionChanged(0,10);gpTarget='';queue=0;Events.CityProductionQueueChanged(0,10);refreshHandler()")
  self.click();self.assertEqual(self.status(),'INTERRUPTED');self.assertEqual(self.get('requests'),0)
 def test_late_empty_event_interrupts(self):
  self.arm();self.runlua('Events.CityProductionChanged(0,10);refreshHandler()');self.click()
  self.assertEqual(self.status(),'INTERRUPTED');self.assertEqual(self.get('requests'),0)
 def test_update_not_completion(self):
  self.arm();self.runlua('Events.CityProductionUpdated(0,10)');self.assertEqual(self.status(),'ACTIVE')
  self.assertEqual(self.get('requests'),0)
 def test_unrelated_no_read(self):
  self.arm();n=self.get('gpReads');self.runlua('Events.CityProductionChanged(0,11);Events.PlayerTurnDeactivated(3);GameEvents.PlayerTurnStarted(3)')
  self.assertEqual(self.get('gpReads'),n);self.assertEqual(self.status(),'ACTIVE')
 def test_ui_turn_before_gp_does_not_cancel_evidence(self):
  self.arm();self.click();self.runlua('turn=21;Events.PlayerTurnActivated(0)')
  self.assertEqual(self.status(),'ENDED')
 def test_no_observation_zero_work(self):
  self.runlua('Events.CityProductionUpdated(0,10);Events.PlayerTurnActivated(0);GameEvents.PlayerTurnStarted(0)');self.assertEqual(self.get('gpReads'),0)
 def test_no_turn_number_proof(self):
  self.arm();self.runlua('turn=21;GameEvents.PlayerTurnStarted(0)');self.assertIn('未证实',self.get('ExposedMembers.SPC_P0.TimedProduction.reason'))
 def test_bound(self):
  self.arm();self.runlua('for i=1,30 do Events.CityProductionUpdated(0,10) end')
  self.assertEqual(self.status(),'STOPPED');self.assertLessEqual(self.get('#ExposedMembers.SPC_P0.TimedProduction.rows'),24)
 def test_duplicate_begin_and_cancel_token(self):
  self.arm();self.runlua("ExposedMembers.SPC_P0.TimedProductionProbe.Request(0,packets[1]);ExposedMembers.SPC_P0.TimedProductionProbe.Request(0,{Action='TIMED_PRODUCTION_CANCEL',Token='old'})")
  self.assertEqual(self.status(),'ACTIVE');self.assertEqual(self.get('#ExposedMembers.SPC_P0.TimedProduction.rows'),1)
 def test_unknown_gameplay_target(self):
  self.runlua("gpTarget='BUILDING_TEST'");self.arm();self.click();self.assertEqual(self.get('requests'),0);self.assertEqual(self.status(),'STOPPED')
 def test_ui_cache_rejected_before_force(self):
  self.arm();self.runlua("ExposedMembers.SPC_P0.TimedProduction.status='INTERRUPTED'");self.click();self.assertEqual(self.get('requests'),0)
 def test_report_cached_no_gp_request(self):
  self.arm();n=self.get('#packets');self.runlua("LuaEvents.SPC_TimedTurnProbe('READ')");self.assertEqual(self.get('#packets'),n)
 def test_gameplay_closes_before_ui_turn_unlocks(self):
  self.arm();self.click();self.runlua('turn=21;GameEvents.PlayerTurnStarted(0);Events.GameCoreEventPublishComplete();Events.PlayerTurnActivated(0)')
  self.arm();self.click();self.assertEqual(self.get('requests'),2)
 def test_missing_required_hook_fails_closed(self):
  self.runlua('Events.CityProductionUpdated=nil;SPCTimedProductionProbe.Start(SPCP0,ExposedMembers.SPC_P0)')
  self.arm();self.click();self.assertEqual(self.get('requests'),0);self.assertEqual(self.status(),'STOPPED')
 def test_actual_request_dispatch(self):
  # Execute the real Gameplay request function, with startup and unrelated writers uninvoked.
  source=(prior.ROOT/'Mod/Gameplay.lua').read_text().split('GameEvents.SPC_P0_Request.Add(function(...)')[0]
  self.runlua("SPCP0.VERSION='B115';SPCP0.Scalar=tostring;SPCPerformance={New=function() return {} end}")
  dispatch=self.lua.execute(source+'\nreturn request')
  self.runlua('SPCTimedProductionProbe.Start(SPCP0,ExposedMembers.SPC_P0)')
  packet=self.lua.table_from({'Action':'TIMED_PRODUCTION_BEGIN','Token':'dispatch','CityID':10,'StartTurn':20})
  dispatch(0,packet);self.assertEqual(self.status(),'ACTIVE')
  packet['Action']='TIMED_PRODUCTION_CANCEL';dispatch(0,packet);self.assertEqual(self.status(),'STOPPED')
 def test_actual_request_rejects_bad_token(self):
  source=(prior.ROOT/'Mod/Gameplay.lua').read_text().split('GameEvents.SPC_P0_Request.Add(function(...)')[0]
  self.runlua("SPCP0.VERSION='B115';SPCP0.Scalar=tostring;SPCPerformance={New=function() return {} end}")
  dispatch=self.lua.execute(source+'\nreturn request')
  self.runlua('SPCTimedProductionProbe.Start(SPCP0,ExposedMembers.SPC_P0)')
  dispatch(0,self.lua.table_from({'Action':'TIMED_PRODUCTION_BEGIN','CityID':10,'StartTurn':20}))
  self.assertIsNone(self.get('ExposedMembers.SPC_P0.TimedProduction'))
if __name__=='__main__':unittest.main()
