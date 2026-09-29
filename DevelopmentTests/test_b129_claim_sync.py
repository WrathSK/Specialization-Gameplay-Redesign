"""B129 bounded cold-load handshake; actual UI module, no native evidence."""
import unittest
import test_b127_claim_ui as base
class Sync(base.UI):
 def setUp(self):
  super().setUp()
  self.runlua("shared.ClaimProjects={views={},syncAck={}}")
 def test_retry_then_ack(self):
  self.runlua("target=claim;size=1;claimUI.WarmStart();for i=1,4 do claimUI.Pulse()end")
  self.assertEqual(self.get('#packets'),2)
  self.runlua("shared.ClaimProjects.syncAck['0:10']=packets[2].Token;shared.ClaimProjects.views['0:10']={stage='ACTIVE',project=claim,start=turn,reason='saved'};for i=1,30 do claimUI.Pulse()end")
  self.assertEqual(self.get('#packets'),2)
  self.assertEqual(self.get('(SPCTimedProjectDisplay.Text(0,10))'),'1')
 def test_bounded_and_no_begin(self):
  self.runlua("target=claim;size=1;for i=1,50 do claimUI.Pulse()end")
  self.assertEqual(self.get('#packets'),3)
  self.assertIn('未获确认',self.get("ExposedMembers.SPC_ClaimSync['0:10']"))
  self.runlua("for _,p in ipairs(packets)do assert(p.Action=='CLAIM_SYNC')end")
 def test_late_backend(self):
  self.runlua("shared.ClaimProjects=nil;for i=1,20 do claimUI.Pulse()end")
  self.assertEqual(self.get('#packets'),0)
  self.runlua("shared.ClaimProjects={views={},syncAck={}};claimUI.Pulse()")
  self.assertEqual(self.get('#packets'),1)
 def test_stale_ack_does_not_close(self):
  self.runlua("claimUI.WarmStart();for i=1,4 do claimUI.Pulse()end;shared.ClaimProjects.syncAck['0:10']=packets[1].Token;for i=1,12 do claimUI.Pulse()end")
  self.assertEqual(self.get('#packets'),3)
if __name__=='__main__':unittest.main()
