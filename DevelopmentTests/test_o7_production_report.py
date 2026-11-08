"""Read the actual Standardization report through the selected production UI."""

from collections import deque
import unittest

from refactor_harness import Context, PackageVFS, measure
from test_o6_production_panel import panel
from test_pu11_package_absence import NATIVE, scalars
from test_refactor_s4b import standard


QUEUE_FIXTURE = """
local id,x,y,t=...
c.GetID=function()return id end
c.GetX=function()return x end
c.GetY=function()return y end
Game.GetCurrentGameTurn=function()return t end
Players[0].GetCities=function()
 return {FindID=function(_,city)assert(city==id,'UNRELATED_CITY_READ');return c end,
  Members=function()error('CITY_ENUMERATION')end}
end
costReads,progressReads=0,0
nativeHash=209
local q={GetCurrentProductionTypeHash=function()return nativeHash end}
local kinds={
 {'Buildings','BuildingType','Building','BUILDING_GRANARY'},
 {'Districts','DistrictType','District','DISTRICT_CAMPUS'},
 {'Units','UnitType','Unit','UNIT_BUILDER'},
 {'Projects','ProjectType','Project','PROJECT_NATIVE'},
}
for i,k in ipairs(kinds)do
 GameInfo[k[1]]={[208+i]={[k[2]]=k[4],Index=i}}
 q['Get'..k[3]..'Cost']=function(_,index)
  assert(index==i,'WRONG_GETTER');costReads=costReads+1;return 65+i
 end
 q['Get'..k[3]..'Progress']=function(_,index)
  assert(index==i,'WRONG_GETTER');progressReads=progressReads+1
  if changeDuringRead then nativeHash=999 end
  return 12.25+i
 end
end
q.GetSize=function()error('QUEUE_ENUMERATION')end
q.GetAt=q.GetSize
c.GetBuildQueue=function()return q end
"""


def connect(gameplay, ui, city):
    ui.execute(QUEUE_FIXTURE, *gameplay.eval(
        f'{city}:GetID(),{city}:GetX(),{city}:GetY(),Game.GetCurrentGameTurn()'))

    def read_ui(*args):
        reader = ui.globals().ExposedMembers.SPC_StandardizationProgressRead
        if reader is None:
            raise RuntimeError('STD_PROGRESS_SLOT_MISSING')
        return gameplay.table_from(scalars(reader(*args)))

    gameplay.globals().readUI = read_ui
    gameplay.execute('ExposedMembers.SPC_StandardizationProgressRead=function(...)return readUI(...)end')


def pair(hd=False):
    gameplay = standard()
    gameplay.execute("""
        Locale={Lookup=function(s)return s end}
        c=cities[1];c.GetName=function()return 'Capital'end
        current='BUILDING_GRANARY'
        c.GetBuildQueue=function()return {CurrentlyBuilding=function()return current end}end
        ExposedMembers.DLHD=nil
        shared.ConstructionProbe={ReadSnapshot=function()error('OLD_HD_READER_USED')end}
        function report()return std.Describe(0,c,1)end
        assert(stdValue(1)==14)
    """)
    ui, _ = panel(hd)
    connect(gameplay, ui, 'c')
    return gameplay, ui


class StandardizationReport(unittest.TestCase):
    def test_actual_panels_read_only_one_current_target_without_hd_helpers(self):
        for hd in (False, True):
            with self.subTest(hd=hd):
                gameplay, ui = pair(hd)
                for index, kind in enumerate(('BUILDING_GRANARY', 'DISTRICT_CAMPUS',
                                              'UNIT_BUILDER', 'PROJECT_NATIVE'), start=1):
                    ui.execute('nativeHash=...', 208+index)
                    gameplay.execute('current=...', kind)
                    report = gameplay.eval('report()')
                    self.assertIn('建造 +14%', report)
                    self.assertIn(f'当前生产进度：{12.25+index} / {65+index}', report)
                gameplay.execute('assert(stdValue(1)==14 and propertyWrites==0)')
                ui.execute("""
                    assert(costReads==4 and progressReads==4 and #nativeOps==0)
                    for i=1,1000 do Events.GameCoreEventPublishComplete.Fire()end
                    assert(costReads==4 and progressReads==4 and #nativeOps==0)
                """)
        measure('O7a_standardization_report', {'profiles': 2, 'targets_per_profile': 4,
                'cost_reads_per_report': 1, 'progress_reads_per_report': 1,
                'additional_reads_per_1000_idle_publications': 0})

    def test_changed_or_missing_progress_leaves_applied_report_available(self):
        gameplay, ui = pair()
        self.assertIn('当前生产进度：13.25 / 66', gameplay.eval('report()'))
        for fault in ('unrelated_hash', 'wrong_type', 'changed_queue', 'changed_ref', 'closed_panel'):
            with self.subTest(fault=fault):
                if fault == 'unrelated_hash':
                    ui.execute('nativeHash=0')
                elif fault == 'wrong_type':
                    ui.execute('nativeHash=210')
                elif fault == 'changed_queue':
                    ui.execute('nativeHash=209;changeDuringRead=true')
                elif fault == 'changed_ref':
                    ui.execute('nativeHash=209;changeDuringRead=false')
                    gameplay.execute("""
                        local read=ExposedMembers.SPC_StandardizationProgressRead
                        ExposedMembers.SPC_StandardizationProgressRead=function(...)
                         local q=read(...);c.token='changed';return q
                        end
                    """)
                else:
                    ui.execute('ContextPtr.shutdown();assert(ExposedMembers.SPC_StandardizationProgressRead==nil)')
                    gameplay.execute('ExposedMembers.SPC_StandardizationProgressRead=nil')
                report = gameplay.eval('report()')
                self.assertIn('建造 +14%', report)
                self.assertIn('当前生产进度未读取', report)
                self.assertNotIn('当前生产进度：', report)
                gameplay.execute('assert(stdValue(1)==14 and propertyWrites==0)')

    def test_real_dispatch_runs_with_the_dev_probe_absent(self):
        reports = []
        for mode in ('present', 'throw', 'silent_nil'):
            with self.subTest(mode=mode):
                vfs = (PackageVFS() if mode=='present' else
                       PackageVFS(absent=['ConstructionProbe'], missing_include=mode,
                                  forbidden_globals=['SPCConstructionProbe']))
                gameplay = Context(vfs=vfs)
                gameplay.loads = deque(maxlen=512)
                gameplay.execute(NATIVE)
                gameplay.load('Gameplay')
                if mode != 'present':
                    self.assertTrue(any(row['module']=='ConstructionProbe.lua' and row['status']=='ABSENT'
                                        for row in gameplay.loads))
                    gameplay.execute("""
                        local s=ExposedMembers.SPC_P0
                        assert(s.ConstructionProbe==nil and s.StartStatus.CrewPrecision.state=='SKIPPED_DEPENDENCY')
                    """)
                gameplay.execute("""
                    local s=ExposedMembers.SPC_P0
                    assert(s.StartStatus.StandardizationEffects.state=='OK')
                    assert(s.StartStatus.UnitActions.state=='OK')
                    local q={CurrentlyBuilding=function()return 'BUILDING_GRANARY'end}
                    c={GetOwner=function()return 0 end,GetID=function()return 9 end,GetX=function()return 10 end,
                       GetY=function()return 11 end,GetProperty=function()return 'REF'end,GetName=function()return 'City'end,
                       GetBuildQueue=function()return q end}
                    Players[0].GetCities=function()
                     return {FindID=function(_,id)assert(id==9);return c end,Members=function()error('CITY_ENUMERATION')end}
                    end
                    s.StandardizationEffects.records['0:9']={applied={},sources={},reference=SPCNetworkInput.Reference(c)}
                    Game.SetProperty=function()error('REPORT_WROTE_PROPERTY')end
                """)
                ui, _ = panel()
                connect(gameplay.lua, ui, 'c')
                gameplay.execute("""
                    local s=ExposedMembers.SPC_P0
                    GameEvents.SPC_P0_Request.Fire(0,{Action='DISCOUNT_READ',CityID=9,Token='detail'})
                    assert(s.LastToken=='detail')
                """)
                reports.append(gameplay.eval('ExposedMembers.SPC_P0.Snapshot'))
                self.assertIn('当前生产进度：13.25 / 66', reports[-1])
                ui.execute('assert(costReads==1 and progressReads==1)')
        self.assertEqual(reports, [reports[0]] * 3)
