"""Retire the manual overflow writer while retaining the automatic test timer."""
import unittest

from refactor_harness import Context, PackageVFS, ROOT, measure
from retired_crew_sources import B455, gameplay, package
from test_o7_crew_retirement import verify_package_round_trip
from test_o7_project_turn_observer_retirement import PROJECT, panel_timer, production_input
from test_p0_panel_current_layout import panel_runtime
from test_pu11_package_absence import NATIVE

REMOVED = ('OverflowStorageProbe.lua', 'UI/OverflowStorageRead.lua')
RETIRED_HINT = '查看后续目标进度请右键“完成承接试验”。'
HOOKS = ('CityProductionChanged', 'CityProductionQueueChanged', 'CityProductionUpdated',
         'CityProductionCompleted', 'CityRemovedFromMap')


def panel_hooks(root):
    tree, ui = panel_runtime(root/'Mod/UI')
    ui.execute('''
      init()
      publicationRemovals=0
      Events.GameCoreEventPublishComplete.Remove=function()publicationRemovals=publicationRemovals+1 end
      shutdown()
    ''')
    controls = ui.globals().Controls
    buttons = {node.get('ID'): (node.get('Offset'), controls[node.get('ID')].hidden,
                               set(controls[node.get('ID')].callbacks.keys()))
               for node in tree.iter('GridButton') if node.get('ID')}
    return (ui.globals().eventAdds.GameCoreEventPublishComplete, ui.globals().publicationRemovals,
            list(ui.globals().included.values()), buttons)


class ManualOverflowRetirement(unittest.TestCase):
    def test_actual_manual_requests_retire_with_five_modeled_hooks(self):
        with package(B455) as previous:
            before = gameplay(previous, revision=B455)
            after = Context(vfs=PackageVFS(forbidden_globals=('SPCOverflowStorageProbe',)))
            self.assertFalse(set(REMOVED) & (after.vfs.files | after.vfs.imports))
            for context in (before, after):
                context.execute(NATIVE)
                context.load('Gameplay')
                self.assertEqual(context.load_counts['missing'] + context.load_counts['failed'], 0)
                shared = context.globals().ExposedMembers.SPC_P0
                for name in ('ClaimProjects', 'DialogueProjects', 'EngineeringStudyProjects',
                             'CrewProjects', 'TimedProject'):
                    self.assertEqual(shared.StartStatus[name].state, 'OK', name)
                properties = dict(context.globals().properties.items())
                context.execute('''
                  local project=...
                  local s=ExposedMembers.SPC_P0
                  manualWrites=0
                  local q={CurrentlyBuilding=function()return project end,GetSize=function()return 1 end,
                    FinishProgress=function()manualWrites=manualWrites+1 end}
                  local city={GetOwner=function()return 0 end,GetX=function()return 3 end,
                    GetY=function()return 4 end,GetID=function()return 9 end,GetBuildQueue=function()return q end}
                  Players[0]:GetCities().FindID=function(_,id)if id==9 then return city end end
                  ExposedMembers.SPC_OverflowExactRead=function(pid,id)
                    assert(pid==0 and id==9)
                    return {owner=pid,id=id,turn=turn,project=project,size=1,value=8}
                  end
                  s.LastToken='previous-valid-request'
                  local request={Action='OVERFLOW_PREPARE',Token='manual-test',CityID=9,StartTurn=turn,Progress=8}
                  GameEvents.SPC_P0_Request.Fire(0,request)
                  assert(s.RequestIngress.action=='OVERFLOW_PREPARE' and manualWrites==0)
                  request.Action='OVERFLOW_APPLY'
                  GameEvents.SPC_P0_Request.Fire(0,request)
                  assert(s.RequestIngress.action=='OVERFLOW_APPLY' and s.LastToken=='previous-valid-request')
                ''', PROJECT)
                self.assertEqual(dict(context.globals().properties.items()), properties)
            old_shared = before.globals().ExposedMembers.SPC_P0
            self.assertEqual(old_shared.StartStatus.OverflowStorageProbe.state, 'OK')
            self.assertEqual(old_shared.OverflowStorage.status, 'CALLED_NOT_PROVEN')
            self.assertEqual(before.globals().manualWrites, 1)
            new_shared = after.globals().ExposedMembers.SPC_P0
            self.assertIsNone(new_shared.StartStatus.OverflowStorageProbe)
            self.assertIsNone(new_shared.OverflowStorage)
            self.assertEqual(after.globals().manualWrites, 0)
            for name in HOOKS:
                count = f'Events.{name}.Count()'
                self.assertEqual(before.eval(count), after.eval(count) + 1, name)
        measure('manual_overflow_retirement', {'removed_modeled_gameplay_hooks':len(HOOKS),
            'modeled_manual_finish_calls_before':1,'modeled_manual_finish_calls_after':0})

    def test_production_inputs_and_p0_timer_survive_retirement(self):
        with package(B455) as previous:
            for hd in (False, True):
                with self.subTest(hd=hd):
                    self.assertEqual(production_input(ROOT, hd), production_input(previous, hd, (previous, B455)))
            before_text, before_cancel = panel_timer(previous)
            after_text, after_cancel = panel_timer(ROOT)
            self.assertEqual(before_text.count(RETIRED_HINT), 1)
            self.assertEqual(after_text, before_text.replace(RETIRED_HINT, ''))
            self.assertEqual(after_cancel, before_cancel)
            old_add, old_remove, old_includes, old_buttons = panel_hooks(previous)
            new_add, new_remove, new_includes, new_buttons = panel_hooks(ROOT)
            self.assertEqual(new_buttons, old_buttons)
            self.assertEqual(old_includes.count('OverflowStorageRead'), 1)
            self.assertNotIn('OverflowStorageRead', new_includes)
            self.assertEqual((old_add, old_remove), (new_add + 1, new_remove + 1))
        measure('manual_overflow_p0_lifecycle', {'removed_modeled_publication_hooks':1})

    def test_temporary_switch_and_rollback_restore_the_exact_predecessor(self):
        with package(B455) as previous:
            verify_package_round_trip(self, previous/'Mod', ROOT/'Mod', REMOVED, 'UI/ProjectTurnRead.lua')
