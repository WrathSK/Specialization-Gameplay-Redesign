"""B237 actual writer/UI regression. Fixed injection remains a guarded blocker."""
import unittest
from test_b236_crews import crew_runtime, ACTION, M
from test_b236_crew_ui import fixture

class Continuity(unittest.TestCase):
 def check(self,s):crew_runtime().execute('local CP=SPCCrewModel;'+s)
 def test_continuous_order_retains_old_variant_and_next_price(self):
  self.check("""
   local c=C.make();local p=C.begin(c);local q=c:GetBuildQueue();q.progressByProject[p]=100
   H.wonder(c,1);crew.Refresh(0,c:GetID());local v=crew.views['0:'..c:GetID()]
   assert(v.allowed[p] and v.retained[p].price==390 and v.allowed[CP.Project(1,140)])
   assert(q.progressByProject[p]==100 and v.reserved==1)
   C.complete(c,p);assert(crew.Unit(0,C.units[20001]).capacity==260)
   local r=C.reserve(c,1,140);assert(not r.error);assert(c:GetProperty(CP.ORDER_PROPERTY).orders[1].price==364)
  """)
 def test_pause_reprice_and_resume_keeps_progress_price_serial(self):
  self.check("""
   local c=C.make();local p=C.begin(c);local q=c:GetBuildQueue();q.progressByProject[p]=100;q.items={}
   crew.Refresh(0,c:GetID());local serial=c:GetProperty(CP.ORDER_PROPERTY).orders[1].serial
   H.wonder(c,1);crew.Refresh(0,c:GetID());local v=crew.views['0:'..c:GetID()]
   assert(v.paused==1 and v.reserved==0 and v.allowed[p] and v.startable[p] and v.allowed[CP.Project(1,140)])
   assert(c.buildings[C.rows.Buildings[CP.Marker(1,150)].Index])
   C.begin(c);local o=c:GetProperty(CP.ORDER_PROPERTY).orders[1]
   assert(o.price==390 and o.capacity==260 and o.serial==serial and o.stage=='QUEUED' and q.progressByProject[p]==100)
   C.complete(c,p);assert(C.count(c)==1)
  """)
 def test_paused_admission_survives_active_drop_and_cold_reconstruction(self):
  self.check("""
   local c=C.make();local p=C.begin(c,4);local q=c:GetBuildQueue();q.progressByProject[p]=100;q.items={}
   crew.Refresh(0,c:GetID());T.governor(2);C.reload(c)
   local v=crew.views['0:'..c:GetID()];assert(v.paused==1 and v.startable[p] and not v.startable[CP.Project(2,150)])
   C.begin(c,4);C.complete(c,p);C.reload(c)
   assert(C.count(c)==1 and crew.Unit(0,C.units[20001]).capacity==1000)
  """)
 def test_pause_does_not_occupy_two_actual_slots_but_resume_reserves_one(self):
  self.check("""
   local c=C.make();local p=C.begin(c);local q=c:GetBuildQueue();q.progressByProject[p]=50;q.items={};crew.Refresh(0,c:GetID())
   local a=C.begin(c,2);local b=C.begin(c,3);assert(C.reserve(c).error)
   q.items[b]=nil;crew.Refresh(0,c:GetID());assert(not C.reserve(c).error)
   assert(crew.views['0:'..c:GetID()].reserved==2 and q.progressByProject[p]==50)
  """)
 def test_same_bucket_two_removed_orders_retain_one_and_no_grant(self):
  self.check("""
   local c=C.make();local p=C.begin(c);C.begin(c);local q=c:GetBuildQueue();q.progressByProject[p]=50;q.items={}
   crew.Refresh(0,c:GetID());local v=c:GetProperty(CP.ORDER_PROPERTY)
   assert(#v.orders==1 and v.orders[1].stage=='PAUSED' and C.calls==0)
  """)
 def test_removed_duplicate_does_not_shadow_remaining_queued_bucket(self):
  self.check("""
   local c=C.make();local p=C.begin(c);C.begin(c);local q=c:GetBuildQueue();q.progressByProject[p]=50;q.items[p]=1
   crew.Refresh(0,c:GetID());assert(#c:GetProperty(CP.ORDER_PROPERTY).orders==1 and crew.views['0:'..c:GetID()].paused==0)
   C.complete(c,p);assert(C.count(c)==1)
  """)
 def test_zero_progress_cancel_cannot_claim_old_price(self):
  self.check("local c=C.make();C.begin(c);c:GetBuildQueue().items={};crew.Refresh(0,c:GetID());H.wonder(c,1);crew.Refresh(0,c:GetID());assert(#c:GetProperty(CP.ORDER_PROPERTY).orders==0 and C.reserve(c).error)")
 def test_global_completion_in_other_city_does_not_corrupt_paused_local_bucket(self):
  self.check("""
   local c=C.make();local p=C.begin(c);local q=c:GetBuildQueue();q.progressByProject[p]=100;q.items={};crew.Refresh(0,c:GetID())
   local b=H.city(2);T.complete(b,'DISTRICT_INDUSTRIAL_ZONE');C.queue(b);T.invest(b,8991);T.invest(b,8992);T.invest(b,8993);crew.Refresh(0,b:GetID())
   C.begin(b);C.complete(b,p);crew.Refresh(0,c:GetID())
   assert(not crew.errors['0:'..c:GetID()] and c:GetProperty(CP.ORDER_PROPERTY).orders[1].stage=='PAUSED')
   C.begin(c);C.complete(c,p);assert(C.count(c)==1 and C.count(b)==1 and C.calls==2)
  """)
 def test_unreadable_progress_preserves_admission_and_rejects(self):
  for value in ('nil', '-1', '0/0'):
   with self.subTest(value=value):self.check("""
    local c=C.make();local p=C.begin(c);local before=T.encode(c:GetProperty(CP.ORDER_PROPERTY));c:GetBuildQueue().items={}
    local read=ExposedMembers.SPC_CrewNativeRead;ExposedMembers.SPC_CrewNativeRead=function(...)local v=read(...);v.progress[p]=%s;return v end
    crew.Refresh(0,c:GetID());assert(crew.errors['0:'..c:GetID()]=='CREW_PROJECT_PROGRESS_UNKNOWN')
    assert(T.encode(c:GetProperty(CP.ORDER_PROPERTY))==before and C.reserve(c).error and C.calls==0)
   """%value)
 def test_failed_resume_command_restores_paused_admission(self):
  self.check("""
   local c=C.make();local p=C.begin(c);local q=c:GetBuildQueue();q.progressByProject[p]=100;q.items={};crew.Refresh(0,c:GetID())
   local r=C.reserve(c);crew.Request(0,{CityID=c:GetID(),Token='cancel-resume',Action='CANCEL',Reservation=r.reservation})
   assert(not ExposedMembers.SPC_CrewReply.error and c:GetProperty(CP.ORDER_PROPERTY).orders[1].stage=='PAUSED' and q.progressByProject[p]==100)
  """)
 def test_uncertain_resume_write_never_issues_native_build_or_grant(self):
  for failure in ('drop','third','throw'):
   with self.subTest(failure=failure):self.check("local c=C.make();local p=C.begin(c);local q=c:GetBuildQueue();q.progressByProject[p]=50;q.items={};crew.Refresh(0,c:GetID());C.orderFailure='%s';assert(C.reserve(c).error and C.calls==0 and q.progressByProject[p]==50)"%failure)
 def test_saved_tier_one_unit_capacity_is_not_rewritten(self):
  self.check("local c=C.make();local p=C.begin(c);C.complete(c,p);local u=C.units[20001];local v=crew.Unit(0,u);v.capacity=250;u:SetProperty(CP.UNIT_PROPERTY,v);C.reload(c);assert(crew.Unit(0,u).capacity==250 and C.count(c)==1)")
 def test_native_price_mismatch_holds_without_repricing_progress(self):
  self.check("""
   local c=C.make();local p=C.begin(c);local q=c:GetBuildQueue();q.progressByProject[p]=50;q.items={};crew.Refresh(0,c:GetID())
   C.costFailure=true;crew.Refresh(0,c:GetID())
   assert(crew.errors['0:'..c:GetID()]=='CREW_NATIVE_COST_MISMATCH' and C.reserve(c).error and q.progressByProject[p]==50)
  """)
 def test_source_loss_clears_paused_admission_only(self):
  self.check("local c=C.make();local p=C.begin(c);local q=c:GetBuildQueue();q.progressByProject[p]=50;q.items={};crew.Refresh(0,c:GetID());T.loss(c,3,55);shared.CityProgressionStore.ExitConfirmed();assert(#c:GetProperty(CP.ORDER_PROPERTY).orders==0 and q.progressByProject[p]==50)")
 def test_repeated_unchanged_events_preserve_state_without_writes(self):
  self.check("""
   local c=C.make();local p=C.begin(c);local q=c:GetBuildQueue();q.progressByProject[p]=50;q.items={};crew.Refresh(0,c:GetID())
   local writes=0;local set=c.SetProperty;c.SetProperty=function(...)writes=writes+1;return set(...)end
   for i=1,50 do crew.Refresh(0,c:GetID())end;assert(writes==0 and C.calls==0)
  """)

class PrecisionIsolation(unittest.TestCase):
 def test_diagnostic_failure_does_not_replace_action_return(self):
  l=crew_runtime();l.execute((M/'UnitActions.lua').read_text());l.execute(ACTION);l.execute((M/'CrewPrecision.lua').read_text())
  l.execute("""
   local c=C.make();local p=C.begin(c);C.complete(c,p);C.actions(c)
   crew.RecordPrecision=function()error('diagnostic unavailable')end
   SPCCrewPrecision.Start(P,shared)
   local result=shared.UnitActions.Run(0,{Action='UNIT_ACTION_CONFIRM',UnitID=20001,Token='x'})
   assert(result:find('REJECTED') and C.count(c)==1 and #c:GetBuildQueue().adds==0)
  """)
 def test_missing_target_diagnostic_does_not_query_nil_city(self):
  l=crew_runtime();l.execute("""
   local c=C.make();local get=Players[0].GetCities
   Players[0].GetCities=function()local cities=get();local find=cities.FindID;cities.FindID=function(self,id)assert(id~=nil,'nil city');return find(self,id)end;return cities end
   crew.RecordPrecision(0,{error='NO_CURRENT_TARGET'})
  """)

class UIContinuity(unittest.TestCase):
 def test_real_reader_reports_paused_progress_without_queue(self):
  fixture().execute("progress[GameInfo.Projects[item.Type].Index]=123;local v=ExposedMembers.SPC_CrewNativeRead(0,9);assert(v.progress[item.Type]==123 and not v.projects[item.Type])")
 def test_read_unknown_progress_is_not_zero(self):
  fixture().execute("q.GetProjectProgress=function()return nil end;assert(not pcall(ExposedMembers.SPC_CrewNativeRead,0,9))")
 def test_retained_disabled_row_survives_filter_and_reports_old_price(self):
  fixture().execute("""
   local v=ExposedMembers.SPC_P0.CrewProjects.views['0:9'];v.retained={[item.Type]={stage='PAUSED',price=390}};v.startable={}
   local d={City=c,ProjectItems={{Type=item.Type,Name='Crew',Disabled=true,ToolTip='native'}}};api.Items(d)
   assert(#d.ProjectItems==1 and d.ProjectItems[1].SPC_CrewRetained and d.ProjectItems[1].Disabled and d.ProjectItems[1].Name:find('RESUME') and d.ProjectItems[1].ToolTip:find('390'))
  """)

if __name__=='__main__':unittest.main()
