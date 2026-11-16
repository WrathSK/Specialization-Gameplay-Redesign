"""OPEN D5 characterization, not a fix or native event-delivery claim.
Passing means the deficit/conditional ambiguity was reproduced under doubles.
"""
import unittest
from refactor_harness import measure
from test_refactor_s7d5 import profile
import test_b236_crews as crews

def fixture(prior=False):
 with profile():vm=crews.crew_runtime()
 vm.execute("""
 print=function()end;c=C.make()
 """)
 if prior:vm.execute('p=C.begin(c);C.complete(c,p)')
 vm.execute("""
 other=H.city(2);other.buildings[10]=true;H.district(other,'DISTRICT_INDUSTRIAL_ZONE',true)
 for i=1,3 do T.invest(other,9700+i)end;C.queue(other);crew.Refresh(0,other:GetID())
 p=C.begin(c);C.begin(other)
 """)
 return vm

class OpenProof(unittest.TestCase):
 def test_characterizes_current_two_city_same_counter_deficit(self):
  vm=fixture();vm.execute("""
  c:GetBuildQueue().items[p]=nil;other:GetBuildQueue().items[p]=nil;C.stats[p]=2
  Events.CityProductionChanged.Fire(0,c:GetID());Events.CityProductionChanged.Fire(0,other:GetID())
  Events.CityProjectCompleted.Fire(0,c:GetID(),C.rows.Projects[p].Index)
  Events.CityProjectCompleted.Fire(0,other:GetID(),C.rows.Projects[p].Index)
  assert(C.calls==0)
  assert(crew.errors['0:'..c:GetID()]=='CREW_COMPLETION_SEQUENCE_AMBIGUOUS')
  assert(crew.errors['0:'..other:GetID()]=='CREW_COMPLETION_SEQUENCE_AMBIGUOUS')
  """)
  measure('S7d6_D5_OPEN_two_cities',{'status':'COUNTEREXAMPLE_CONFIRMED_OPEN','desired_grants':2,'actual_grants':0,'same_observed_player_count':2,'engine_timing':'UNKNOWN','native_pass':False})
 def test_characterizes_conditional_late_event_indistinguishability(self):
  observed=[]
  for history in ('A_completed_B_cancelled_new_A_event','A_cancelled_B_completed_late_old_A_event'):
   vm=fixture(prior=True);vm.execute("""
   c:GetBuildQueue().items[p]=nil;other:GetBuildQueue().items[p]=nil;C.stats[p]=2
   Events.CityProductionChanged.Fire(0,c:GetID());Events.CityProductionChanged.Fire(0,other:GetID())
   local units={};for id,u in pairs(C.units)do units[id]=u:GetProperty(SPCCrewModel.UNIT_PROPERTY)end
   facts=T.encode({event={0,c:GetID(),C.rows.Projects[p].Index},
    aOrder=c:GetProperty(SPCCrewModel.ORDER_PROPERTY),bOrder=other:GetProperty(SPCCrewModel.ORDER_PROPERTY),
    aNative=ExposedMembers.SPC_CrewNativeRead(0,c:GetID()),bNative=ExposedMembers.SPC_CrewNativeRead(0,other:GetID()),
    receipts=C.props[SPCCrewModel.RECEIPT_PROPERTY],units=units})
   local before=C.calls;Events.CityProjectCompleted.Fire(0,c:GetID(),C.rows.Projects[p].Index)
   grants=C.calls-before
   """)
   observed.append((vm.eval('facts'),vm.eval('grants')))
  self.assertEqual(*observed);self.assertEqual(observed[0][1],1)
  measure('S7d6_D5_OPEN_conditional_ambiguity',{'status':'CURRENT_SURFACE_INSUFFICIENT_IF_LATE_EVENT_IS_POSSIBLE','same_observed_facts':True,'actual_new_A_grants_in_both':1,'required_A_grants':[1,0],'native_late_event_possibility':'UNKNOWN','no_live_game_or_native_callback_injected':True})

if __name__=='__main__':unittest.main()
