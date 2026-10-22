"""B236 actual investment transport plus existing institution controls. No native claim."""
import unittest
from test_investment_update_propagation import fixture, source
from test_culture_institutions import display

class EntryPropagation(unittest.TestCase):
    def test_actual_precision_wrapper_preserves_new_commit(self):
        for normal in (True, False):
            with self.subTest(normal=normal):
                lua=fixture(3)
                lua.execute(source('CrewPrecision'));lua.execute('SPCCrewPrecision.Start(P,shared)')
                lua.execute("""
                 c.identity='INDUSTRY';d.type=GameInfo.Districts.DISTRICT_INDUSTRIAL_ZONE.Index
                 events={};shared.EngineeringStudy={Refresh=function(pid,id)
                  events[#events+1]='study:'..pid..':'..id
                  assert(shared.EffectiveFacts.Read(pid,c).active==4)
                 end}
                 shared.IndustryWonderEffects={Refresh=function(pid,id)
                  events[#events+1]='wonder:'..pid..':'..id
                  assert(shared.EffectiveFacts.Read(pid,c).active==4)
                 end}
                """)
                # Reach III using the real writer; observe only the III->IV commit.
                lua.execute("shared.EngineeringStudy=nil;shared.IndustryWonderEffects=nil;invest(c,701,true);invest(c,702,true)")
                lua.execute("""
                 local function observer(label)return {Refresh=function(pid,id)
                  assert(id==c.id and shared.EffectiveFacts.Read(pid,c).active==4)
                  events[#events+1]=label
                 end}end
                 shared.EngineeringStudy=observer('study');shared.IndustryWonderEffects=observer('wonder')
                 shared.CrewProjects=observer('crew')
                """)
                lua.execute(f"assert(invest(c,703,{str(normal).lower()}):find('INVESTED'));assert(events[1]=='study' and events[2]=='wonder');assert(kills==3)")
                lua.execute("local n=#events;runRequest(0,{Action='UNIT_ACTION_CONFIRM',UnitID=703,Token='duplicate'});assert(#events==n and kills==3)")

    def test_observer_failure_retains_commit_and_noncommit_nil(self):
        lua=fixture();lua.execute(source('CrewPrecision'))
        lua.execute("""
          SPCCrewPrecision.Start(P,shared);t=prepare(c,704,true)
          P.CrewBase=function()error('OBSERVER_READ_FAILED')end
          out,e=shared.UnitActions.Run(0,{Action='UNIT_ACTION_CONFIRM',UnitID=704,PlanToken=t})
          assert(e.status=='COMMITTED' and kills==1)
          _,e=shared.UnitActions.Run(0,{Action='UNIT_ACTION_CONFIRM',UnitID=704,PlanToken=t});assert(e==nil and kills==1)
        """)

class IndustryInstitutions(unittest.TestCase):
    def test_all_levels_names_and_active_drop(self):
        lua=display();lua.execute("""
          v.specialization='INDUSTRY'
          local names={'匠作坊','百工会馆','工程局','土木工程总局'}
          for i=1,4 do
           v.potential=i;v.active=i;LuaEvents.SPC_PresentationChanged()
           assert(#rows.items==4 and rows.items[i].Name.text==names[i] and rows.items[i].State.text=='当前')
          end
          assert(rows.items[1].Top.tip:find('基础相邻',1,true))
          assert(rows.items[2].Top.tip:find('专业分工',1,true))
          assert(rows.items[3].Top.tip:find('标准化',1,true))
          assert(rows.items[4].Top.tip:find('巨构工程学',1,true))
          v.active=2;LuaEvents.SPC_PresentationChanged();assert(#rows.items==4 and rows.items[4].State.text=='未激活')
          v.activeStatus='UNKNOWN';LuaEvents.SPC_PresentationChanged();assert(#rows.items==4 and rows.items[4].State.text=='待确认')
        """)

if __name__=='__main__':unittest.main()
