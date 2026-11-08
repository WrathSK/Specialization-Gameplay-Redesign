"""Keep both current industrial reports after retiring redundant hidden controls."""
import unittest

from refactor_harness import ROOT, measure
from retired_crew_sources import B474, package
from test_o7_legacy_completion_record_retirement import load_cold_store, save_fixture, stored_records
import test_o7_production_report as production_report
from test_o7_retired_great_work_adjacency_retirement import context
from test_p0_panel_current_layout import panel_runtime

CONTROLS = ('DiscountsButton','NextDiscountsButton','NextTemplatesButton')


def panel(root, *, retired):
    doc,vm=panel_runtime(root/'Mod/UI')
    controls=vm.globals().Controls
    buttons={n.get('ID'):controls[n.get('ID')].hidden for n in doc.iter('GridButton') if n.get('ID')}
    vm.execute("""
      local left,right=Mouse.eLClick,Mouse.eRClick
      local t=Controls.TemplatesButton
      assert(not t.hidden)
      t.callbacks[left]();t.callbacks[left]()
      t.callbacks[right]();t.callbacks[right]()
      Controls.CommerceREADButton.callbacks[left]()
      if ... then
        Controls.DiscountsButton.callbacks[left]()
        Controls.NextDiscountsButton.callbacks[left]()
        Controls.NextTemplatesButton.callbacks[left]()
        Controls.NextTemplatesButton.callbacks[left]()
      end
    """,not retired)
    return (buttons,[dict(p.items()) for p in vm.globals().requests.values()],
            dict(vm.globals().eventAdds.items()))


def template_reports(root,source,saved):
    vm=context(root,source)
    cold=load_cold_store(vm,saved)
    # Provide six confirmed template receipts at the input boundary. The
    # Gameplay ingress, stored identity and both real report owners run.
    reports=vm.execute("""
      local s=ExposedMembers.SPC_P0
      local store=s.CityProgressionStore
      local a=store.Base(0,city1)
      local ledger={schema=1,initialized=true,uid='STD:'..a.token,foundation=a.token,
        x=city1:GetX(),y=city1:GetY(),revision=7,learned={}}
      local catalogue={}
      for i=1,6 do
        local id='BUILDING_FIXTURE_'..i
        ledger.learned[id]={tier=1,district='DISTRICT_CITY_CENTER',turn=turn,evidence='FIXTURE_CONFIRMED'}
        catalogue[id]={enabled=true,name='TEMPLATE_'..i,group='FIXTURE'}
      end
      local read=store.ReadTemplates
      store.ReadTemplates=function(c)
        if c==city1 then return ledger,false end
        return read(c)
      end
      s.Standardization.catalog={buildings=catalogue}
      local before=#writeKeys
      local function request(action,page)
        local token=action..':'..page
        GameEvents.SPC_P0_Request.Fire(0,{Action=action,Token=token,CityID=city1:GetID(),Page=page})
        assert(s.LastToken==token and s.RequestDepth==0 and s.FailureAt==nil)
        return s.Snapshot
      end
      local p1,p2=request('STANDARDIZATION_READ',1),request('STANDARDIZATION_READ',2)
      local combined1,combined2=request('INDUSTRY_HISTORY_READ',1),request('INDUSTRY_HISTORY_READ',2)
      assert(p1:find('页 1/2',1,true) and p1:find('TEMPLATE_1',1,true) and not p1:find('TEMPLATE_6',1,true),p1)
      assert(p2:find('页 2/2',1,true) and p2:find('TEMPLATE_6',1,true) and not p2:find('TEMPLATE_1',1,true),p2)
      assert(combined1:sub(-#p1)==p1 and combined2:sub(-#p2)==p2)
      assert(combined1:find('工业历史',1,true) and combined1:find('施工队',1,true))
      assert(#writeKeys==before and cityWrites==0)
      return p1,p2,combined1,combined2
    """)
    assert stored_records(vm)==cold
    assert vm.load_counts['missing']+vm.load_counts['failed']==0
    return reports


class IndustrialReportAliases(unittest.TestCase):
    def test_current_left_and_right_clicks_keep_their_page_requests(self):
        with package(B474) as previous:
            old_buttons,old_packets,old_listeners=panel(previous,retired=False)
        new_buttons,new_packets,new_listeners=panel(ROOT,retired=True)
        for control in CONTROLS:
            self.assertTrue(old_buttons.pop(control))
        self.assertEqual(old_buttons,new_buttons)
        self.assertEqual(old_listeners,new_listeners)
        self.assertEqual(old_packets[:-4],new_packets)
        self.assertEqual([(p['Action'],p['Page']) for p in old_packets[-4:]],[
            ('DISCOUNT_READ',1),('DISCOUNT_READ',2),('STANDARDIZATION_READ',1),('STANDARDIZATION_READ',2)])
        pages=[(p['Action'],p['Page']) for p in new_packets]
        self.assertEqual(pages,[('INDUSTRY_HISTORY_READ',1),('INDUSTRY_HISTORY_READ',2),
                                ('DISCOUNT_READ',1),('DISCOUNT_READ',2),('COMMERCE_READ',1)])
        measure('retired_industrial_controls',dict(alias_bindings=[3,0],remaining_page_requests=pages[:4],
                                                    listeners='MATCH'))

    def test_real_combined_report_contains_both_standalone_template_pages(self):
        saved=save_fixture()
        with package(B474) as previous:
            before=template_reports(previous,B474,saved)
            for name in ('Gameplay.lua','Standardization.lua','StandardizationEffects.lua','IndustryHistory.lua',
                         'CrewProjects.lua','CityProgressionStore.lua'):
                self.assertEqual((ROOT/'Mod'/name).read_bytes(),(previous/'Mod'/name).read_bytes())
        self.assertEqual(before,template_reports(ROOT,None,saved))
        measure('retired_industrial_templates',dict(pages_matched=2,property_writes=[0,0],report='MATCH'))

    def test_native_progress_fixture_keeps_the_same_discount_report(self):
        fixture=production_report.StandardizationReport()
        with package(B474) as previous:
            before=fixture.read_dispatch(context(previous,B474))
        self.assertEqual(before,fixture.read_dispatch(context(ROOT,None)))
        measure('retired_industrial_progress',dict(configured_discount_and_progress='MATCH'))
