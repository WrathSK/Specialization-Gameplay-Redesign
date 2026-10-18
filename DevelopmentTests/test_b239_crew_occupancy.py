"""B239 actual Crew writer: paid pause ownership and bounded legacy recovery.

Fixtures simulate the native queue; this proves admission/receipt behavior locally,
not Civ VI queue ordering or native performance.
"""
import unittest
from test_b236_crews import crew_runtime
from test_b236_crew_ui import fixture

PAUSE = """
local CP=SPCCrewModel
local c=C.make();local p=C.begin(c);local q=c:GetBuildQueue()
q.progressByProject[p]=50;q.items={};crew.Refresh(0,c:GetID())
local serial=c:GetProperty(CP.ORDER_PROPERTY).orders[1].serial
"""
LEGACY_EXTRA = """
-- B238 could admit this third commitment while the first order was paused.
-- Inject its valid saved record and real queue entry, then reconstruct normally.
local extra=CP.Project(3,150);local old=c:GetProperty(CP.ORDER_PROPERTY)
old.serial=old.serial+1
old.orders[#old.orders+1]={serial=old.serial,project=extra,tier=3,ratio=150,
 capacity=CP.Amount(3,100),price=CP.Cost(3,150,100),base=C.stats[extra],stage='QUEUED'}
c:SetProperty(CP.ORDER_PROPERTY,old);q.items[extra]=1;C.reload(c)
"""

class Occupancy(unittest.TestCase):
 def check(self,script):crew_runtime().execute(PAUSE+script)
 def test_living_plus_paid_pause_blocks_new_and_resumes_old_serial_at_capacity(self):
  self.check("""
   local second=C.begin(c,2);C.complete(c,second)
   H.wonder(c,1);crew.Refresh(0,c:GetID())
   local v=crew.views['0:'..c:GetID()]
   assert(v.count==1 and v.reserved==1 and v.paused==1 and v.queued==0 and v.occupied==2)
   assert(not v.startable[CP.Project(2,140)] and v.startable[p] and C.reserve(c,2,140).error)
   C.begin(c);local o=c:GetProperty(CP.ORDER_PROPERTY).orders[1]
   assert(o.serial==serial and o.price==390 and o.capacity==260 and q.progressByProject[p]==50)
   C.complete(c,p);assert(C.count(c)==2 and C.calls==2 and #c:GetProperty(CP.ORDER_PROPERTY).orders==0)
  """)
 def test_two_paid_pauses_can_both_resume_without_a_third_admission(self):
  self.check("""
   local second=C.begin(c,2);q.progressByProject[second]=70;q.items={};crew.Refresh(0,c:GetID())
   local v=crew.views['0:'..c:GetID()];assert(v.occupied==2 and v.paused==2 and v.queued==0)
   assert(v.startable[p] and v.startable[second] and C.reserve(c,3).error)
   C.begin(c);C.begin(c,2);assert(#c:GetProperty(CP.ORDER_PROPERTY).orders==2)
   C.complete(c,p);C.complete(c,second);assert(C.count(c)==2 and C.calls==2)
  """)
 def test_failed_native_resume_keeps_same_capacity_and_progress(self):
  self.check("""
   local second=C.begin(c,2);C.complete(c,second)
   local r=C.reserve(c);assert(not r.error)
   crew.Request(0,{CityID=c:GetID(),Token='resume-denied',Action='CANCEL',Reservation=r.reservation})
   assert(not ExposedMembers.SPC_CrewReply.error)
   local v=crew.views['0:'..c:GetID()];assert(v.occupied==2 and v.paused==1 and v.queued==0)
   assert(c:GetProperty(CP.ORDER_PROPERTY).orders[1].serial==serial and q.progressByProject[p]==50)
   assert(C.reserve(c,3).error)
  """)
 def test_cold_load_retains_paid_pause_slot_and_no_extra_grant(self):
  self.check("""
   local second=C.begin(c,2);C.complete(c,second);local before=T.encode(c:GetProperty(CP.ORDER_PROPERTY))
   C.reload(c);C.reload(c);local v=crew.views['0:'..c:GetID()]
   assert(v.occupied==2 and v.paused==1 and v.startable[p] and C.reserve(c,3).error and C.calls==1)
   assert(T.encode(c:GetProperty(CP.ORDER_PROPERTY))==before and q.progressByProject[p]==50)
  """)
 def test_zero_progress_confirmed_cancel_releases_only_its_order(self):
  self.check("""
   local second=C.begin(c,2);q.items={};crew.Refresh(0,c:GetID())
   local v=crew.views['0:'..c:GetID()];assert(v.reserved==1 and v.paused==1 and v.occupied==1)
   assert(q.progressByProject[p]==50 and c:GetProperty(CP.ORDER_PROPERTY).orders[1].serial==serial)
   assert(not C.reserve(c,3).error)
  """)
 def test_unadmitted_native_queue_does_not_create_free_room(self):
  self.check("""
   q.items[CP.Project(2,150)]=1;crew.Refresh(0,c:GetID())
   local before=T.encode(c:GetProperty(CP.ORDER_PROPERTY));local v=crew.views['0:'..c:GetID()]
   assert(not v.queueKnown and not v.startable[p] and C.reserve(c,3).error and C.reserve(c).error)
   assert(crew.Describe(0,c):find('原生队列与开工记录不一致',1,true))
   assert(T.encode(c:GetProperty(CP.ORDER_PROPERTY))==before and q.progressByProject[p]==50 and C.calls==0)
  """)
 def test_legacy_overadmission_keeps_progress_blocks_new_and_waits_for_living_room(self):
  self.check("""
   local second=C.begin(c,2);C.complete(c,second)
  """+LEGACY_EXTRA+"""
   local v=crew.views['0:'..c:GetID()]
   assert(v.overCapacity and v.occupied==3 and v.count==1 and v.queued==1 and v.paused==1)
   assert(not v.startable[p] and C.reserve(c).error and C.reserve(c,4).error)
   assert(q.progressByProject[p]==50 and #c:GetProperty(CP.ORDER_PROPERTY).orders==2)
   C.complete(c,extra);assert(C.count(c)==2 and C.calls==2 and q.progressByProject[p]==50)
   assert(C.reserve(c).error)
   Players[0]:GetUnits():Destroy(C.units[20001]);Events.GameCoreEventPublishComplete.Fire()
   assert(crew.views['0:'..c:GetID()].startable[p]);C.begin(c)
   local o=c:GetProperty(CP.ORDER_PROPERTY).orders[1];assert(o.serial==serial and o.price==390 and o.capacity==260)
   C.complete(c,p);assert(C.count(c)==2 and C.calls==3)
  """)
 def test_legacy_multiple_paid_pauses_resume_up_to_native_completion_capacity(self):
  self.check("""
   local second=C.begin(c,2);q.progressByProject[second]=70;q.items={};crew.Refresh(0,c:GetID())
  """+LEGACY_EXTRA+"""
   local v=crew.views['0:'..c:GetID()];assert(v.occupied==3 and v.queued==1 and v.paused==2 and v.startable[p])
   assert(C.reserve(c,4).error);C.begin(c);assert(C.reserve(c,2).error)
   assert(#c:GetProperty(CP.ORDER_PROPERTY).orders==3 and q.progressByProject[second]==70)
   C.complete(c,p);C.complete(c,extra);assert(C.count(c)==2 and C.calls==2)
   assert(c:GetProperty(CP.ORDER_PROPERTY).orders[1].project==second and q.progressByProject[second]==70)
  """)
 def test_failed_read_preserves_capacity_and_other_city_isolation(self):
  for failure in ('nil','-1','0/0'):
   with self.subTest(failure=failure):self.check("""
    local other=H.city(2);T.complete(other,'DISTRICT_INDUSTRIAL_ZONE');C.queue(other)
    T.invest(other,8991);T.invest(other,8992);T.invest(other,8993);crew.Refresh(0,other:GetID())
    local before=T.encode(c:GetProperty(CP.ORDER_PROPERTY));local read=ExposedMembers.SPC_CrewNativeRead
    ExposedMembers.SPC_CrewNativeRead=function(pid,id)local v=read(pid,id);if id==c:GetID()then v.progress[p]=%s end;return v end
    assert(C.reserve(c).error and C.reserve(c,3).error and not C.reserve(other,2).error)
    assert(T.encode(c:GetProperty(CP.ORDER_PROPERTY))==before and q.progressByProject[p]==50 and C.calls==0)
   """%failure)
 def test_uncertain_resume_write_does_not_free_existing_commitment(self):
  for failure in ('drop','throw'):
   with self.subTest(failure=failure):self.check("""
    local second=C.begin(c,2);C.complete(c,second);local before=T.encode(c:GetProperty(CP.ORDER_PROPERTY))
    C.orderFailure='%s';assert(C.reserve(c).error);C.orderFailure=nil;crew.Refresh(0,c:GetID())
    assert(T.encode(c:GetProperty(CP.ORDER_PROPERTY))==before and crew.views['0:'..c:GetID()].occupied==2)
    assert(C.reserve(c,3).error and q.progressByProject[p]==50 and C.calls==1)
   """%failure)
 def test_readable_report_distinguishes_paused_commitment_from_queue(self):
  self.check("""
   local text=crew.Describe(0,c);assert(text:find('已占名额：1/2',1,true) and text:find('续建继续占用原名额',1,true))
   assert(not text:find('暂停不占',1,true));assert(crew.views['0:'..c:GetID()].queued==0)
  """)

class OccupancyUI(unittest.TestCase):
 def test_full_occupancy_resume_is_enabled_and_displays_counts(self):
  fixture().execute("""
   local v=ExposedMembers.SPC_P0.CrewProjects.views['0:9']
   v.retained={[item.Type]={stage='PAUSED',price=390}};v.startable={[item.Type]=true}
   v.count=1;v.reserved=1;v.paused=1;v.resumeBlocked=false
   local data={City=c,ProjectItems={{Type=item.Type,Name='Crew'}}};api.Items(data)
   assert(not data.ProjectItems[1].Disabled and data.ProjectItems[1].ToolTip:find('LOC_SPC_CREW_OCCUPANCY',1,true))
  """)
 def test_overadmitted_paid_resume_stays_visible_with_reason(self):
  fixture().execute("""
   local v=ExposedMembers.SPC_P0.CrewProjects.views['0:9']
   v.retained={[item.Type]={stage='PAUSED',price=390}};v.startable={}
   v.count=1;v.reserved=2;v.paused=1;v.resumeBlocked=true
   local data={City=c,ProjectItems={{Type=item.Type,Name='Crew'}}};api.Items(data)
   assert(data.ProjectItems[1].Disabled and data.ProjectItems[1].SPC_CrewRetained)
   assert(data.ProjectItems[1].ToolTip:find('LOC_SPC_CREW_RESUME_CAPACITY_HELD',1,true))
  """)

if __name__=='__main__':unittest.main()
