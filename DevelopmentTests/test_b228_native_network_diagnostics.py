"""B228 actual-source narrow checks; no native eligibility claim."""
import unittest
from test_expedition_spy_activity_ui import bridge
from test_culture_network import fixture
from test_expedition_trace_reader import reader

class NativeWake(unittest.TestCase):
 def test_native_four_argument_gate_is_used(self):
  l=bridge();l.execute('''
   UnitManager.CanStartCommand=function(u,hash,visible,results)
    assert(hash==80 and visible==false);return results==true
   end
   publish('SLEEP');publish('RELEASE',true)
   assert(wakeCalls==1 and packets[#packets].Result=='RELEASED')
  ''')
 def test_aligned_denial_does_not_force_wake(self):
  l=bridge();l.execute('''publish('SLEEP');UnitManager.CanStartCommand=function()return false end
   publish('RELEASE',true);assert(wakeCalls==0 and packets[#packets].Result=='FAILED' and packets[#packets].Owned)''')
 def test_trace_distinguishes_legacy_gate_without_using_it(self):
  l=bridge(with_trace=True);l.execute('''
   print=function()end
   units[41].IsReadyToSelect=function()return false end
   UnitManager.CanStartCommand=function(u,h,visible,result)return visible or result==true end
   publish('SLEEP');publish('RELEASE',true)
   local found=false
   for _,e in ipairs(ExposedMembers.SPC_B205TrainingTrace.entries)do
    if e.stage=='ACTIVITY_WAKE_REQUEST'then
     assert(e.wakeAllowed=='true' and e.wakeLegacyAllowed=='false' and e.readyToSelect=='false')
     found=true;traceLine=e.line
    end
   end
   assert(found and wakeCalls==1)
  ''')
  self.assertEqual(reader.training_line(l.globals().traceLine),l.globals().traceLine)
 def test_awake_does_not_trigger_speculative_wake(self):
  l=bridge();l.execute("publish('SLEEP');units[41].activity=0;publish('RELEASE',true);assert(wakeCalls==0)")

class NetworkWaiting(unittest.TestCase):
 def setup_lua(self):
  l=fixture();l.execute("logs={};print=function(s)logs[#logs+1]=s end;oldCreated=created;oldRemoved=removed")
  return l
 def test_waiting_reports_city_error_and_input_without_writes(self):
  l=self.setup_lua();l.execute('''
   cn.errors['0:1']='source.lua:12: CN_CREATE_UNCONFIRMED'
   local a=net.players[0].inputRevision
   local text=cn.Describe(0,cities[1]);assert(text:find('CN_CREATE_UNCONFIRMED',1,true))
   assert(logs[1]:find('kind=NETWORK_WAIT',1,true) and logs[1]:find('layer=CITY',1,true))
   assert(logs[2]:find('validity=VERIFIED',1,true))
   assert(a==net.players[0].inputRevision and created==oldCreated and removed==oldRemoved)
  ''')
 def test_no_input_and_module_errors_are_distinct(self):
  l=self.setup_lua();l.execute('''
   cn.records={};cn.errors={};cn.playerError={};net.players[0]=nil
   local s=cn.Describe(0,cities[1]);assert(logs[1]:find('layer=NO_RECORD',1,true))
   assert(net.players[0]==nil)
   cn.error='CN_CARRIER_MISSING';cn.Describe(0,cities[1]);local found=false;for _,line in ipairs(logs)do if line:find('layer=MODULE',1,true)then found=true end end;assert(found)
  ''')
 def test_arbitrary_error_text_not_logged(self):
  l=self.setup_lua();l.execute('''
   cn.errors['0:1']='private/path token-secret';cn.Describe(0,cities[1])
   assert(not logs[1]:find('private',1,true) and not logs[1]:find('token',1,true))
   assert(logs[1]:find('reason=READ_ERROR',1,true))
  ''')
 def test_wait_log_accepted_by_existing_collector_allowlist(self):
  l=self.setup_lua();l.execute("cn.playerError={[0]='NETWORK_REFRESH_PENDING'};cn.Describe(0,cities[1])")
  for line in l.globals().logs.values():
   trace=reader.training_line(line)
   if trace:
    self.assertLessEqual(len(trace),4096)
   else:
    self.assertLessEqual(len(line.split('] ',1)[1]),400)
    self.assertIsNotNone(reader.hd_line(line))

if __name__=='__main__':unittest.main()
