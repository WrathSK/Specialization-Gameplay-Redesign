"""Retire manual observation while preserving the live automatic timer inputs."""
import unittest
from unittest.mock import patch
import xml.etree.ElementTree as ET

from refactor_harness import Context, PackageVFS, ROOT, measure
from retired_crew_sources import B454, B455, gameplay, package
from test_o7_crew_retirement import verify_package_round_trip
from test_p0_panel_current_layout import panel_runtime
from test_pu11_package_absence import NATIVE, scalars
import test_o6_production_panel as production

REMOVED = 'ProjectTurnObservation.lua'
PROJECT = 'PROJECT_SPC_OVERFLOW_SINK_TEST'
HOOKS = [('Events', name) for name in (
    'CityProductionChanged', 'CityProductionQueueChanged', 'CityProductionUpdated',
    'CityProductionCompleted', 'CityRemovedFromMap', 'PlayerTurnDeactivated', 'PlayerTurnActivated',
)] + [('GameEvents', 'PlayerTurnStarted'), ('GameEvents', 'PlayerTurnStartComplete')]


def production_input(root, hd, history=None):
    manifest = root/'Mod/SpecializationP0.modinfo'
    vfs = PackageVFS(manifest=manifest)

    def context(name, vfs):
        return Context(name=name, vfs=vfs, history=history)

    with patch.object(production, 'manifest', lambda: ET.parse(manifest).getroot()), \
         patch.object(production, 'PackageVFS', lambda: vfs), patch.object(production, 'Context', context):
        ui, base = production.panel(hd)
    ui.execute("""
      local project=...
      local info={Index=73,Hash=1501};GameInfo.Projects[project]=info
      local q={GetProjectProgress=function(_,index)assert(index==73);return 8 end,
        GetSize=function()return 1 end,GetCurrentProductionTypeHash=function()return 1501 end}
      c.GetBuildQueue=function()return q end
      Players[0].GetCities=function()return {FindID=function(_,id)if id==c:GetID()then return c end end}end
      readerResult=assert(ExposedMembers.SPC_ProjectTurnRead)(0,c:GetID())
      local sends={};local timer=SPCTimedProjectSelection.New(SPCP0,function(owner,op,p)
        sends[#sends+1]={owner=owner,packet=p}
      end,function()end)
      assert(timer.Before(c,{Type=project}))
      timer.Pulse();timer.Pulse()
      assert(#sends==1 and sends[1].packet.Action=='TIMED_PROJECT_BEGIN')
      sent=sends[1]
    """, PROJECT)
    return base, scalars(ui.globals().readerResult), scalars(ui.globals().sent)


def panel_timer(root):
    path = root/'Mod/UI'
    _, ui = panel_runtime(path)
    ui.execute((path/'ProjectTurnRead.lua').read_text())
    ui.execute((path/'TimedProjectRead.lua').read_text())
    ui.execute("""
      init()
      ExposedMembers.SPC_P0.TimedProjectState={
        owner=0,id=11,status='ACTIVE',token='timer',start=68,attempts=0,reason='test'}
      Controls.PerformanceReadButton.callbacks[Mouse.eLClick]()
      assert(#requests==0)
      report=Controls.Status.text
      assert(type(report)=='string' and report:find('自动项目',1,true))
      Controls.PerformanceReadButton.callbacks[Mouse.eRClick]()
      assert(#requests==1 and requests[1].Action=='TIMED_PROJECT_CANCEL')
    """)
    return ui.globals().report, dict(ui.globals().requests[1].items())


class ProjectTurnObserverRetirement(unittest.TestCase):
    def test_b455_gameplay_preserves_project_starts_and_retires_nine_modeled_hooks(self):
        with package(B454) as previous, package(B455) as retired:
            before = gameplay(previous, revision=B454)
            after = gameplay(retired, revision=B455, forbidden_globals=('SPCProjectTurnObservation',))
            self.assertNotIn(REMOVED, after.vfs.files | after.vfs.imports)
            for context in (before, after):
                context.execute(NATIVE)
                context.load('Gameplay')
                self.assertEqual(context.load_counts['missing'] + context.load_counts['failed'], 0)
                shared = context.globals().ExposedMembers.SPC_P0
                for name in ('ClaimProjects', 'DialogueProjects', 'EngineeringStudyProjects',
                             'CrewProjects', 'TimedProject', 'OverflowStorageProbe'):
                    self.assertEqual(shared.StartStatus[name].state, 'OK', name)
            for group, name in HOOKS:
                count = f'{group}.{name}.Count()'
                self.assertEqual(before.eval(count), after.eval(count) + 1, count)
            shared = after.globals().ExposedMembers.SPC_P0
            self.assertIsNone(shared.StartStatus.ProjectTurnObservation)
            self.assertIsNone(shared.ProjectTurnObservation)
            shared.LastToken = 'previous-valid-request'
            properties = dict(after.globals().properties.items())
            for action in ('PROJECT_TURN_BEGIN', 'PROJECT_TURN_END'):
                after.execute("GameEvents.SPC_P0_Request.Fire(0,{Action=...,Token='observer',CityID=9,StartTurn=turn})", action)
                self.assertEqual(shared.RequestIngress.action, action)
                self.assertEqual(shared.LastToken, 'previous-valid-request')
                self.assertIsNone(shared.ProjectTurnEvidence)
            self.assertEqual(dict(after.globals().properties.items()), properties)
        measure('project_turn_observer_retirement', {'removed_modeled_registrations': len(HOOKS)})

    def test_real_production_contexts_and_p0_keep_queue_reader_and_timer_controls(self):
        with package(B454) as previous, package(B455) as retired:
            for hd in (False, True):
                with self.subTest(hd=hd):
                    before = production_input(previous, hd, (previous, B454))
                    after = production_input(retired, hd, (retired, B455))
                    self.assertEqual(after, before)
                    self.assertEqual(after[1]['value'], 8)
                    self.assertEqual(after[1]['size'], 1)
                    self.assertTrue(after[1]['isProject'])
            self.assertEqual(panel_timer(retired), panel_timer(previous))

    def test_real_timer_request_finishes_once_under_reentrant_events(self):
        game = Context(vfs=PackageVFS(forbidden_globals=('SPCProjectTurnObservation',)))
        game.execute(NATIVE)
        game.load('Gameplay')
        game.execute('''
          local project=...
          local target=project
          local q={CurrentlyBuilding=function()return target end,GetSize=function()return 1 end}
          local city={GetOwner=function()return 0 end,GetX=function()return 3 end,GetY=function()return 4 end,
            GetID=function()return 9 end,GetBuildQueue=function()return q end}
          local cities=Players[0]:GetCities()
          cities.FindID=function(_,id)if id==9 then return city end end
          local writes=0
          q.FinishProgress=function()
            writes=writes+1
            Events.CityProductionQueueChanged.Fire(0,9)
            Events.PlayerTurnActivated.Fire(0)
            target='NONE'
            Events.CityProductionCompleted.Fire(0,9)
          end
          ExposedMembers.SPC_ProjectTurnRead=function(pid,id)
            assert(pid==0 and id==9)
            return {owner=pid,id=id,turn=turn,size=1,isProject=true}
          end
          local shared=ExposedMembers.SPC_P0
          local request={Action='TIMED_PROJECT_BEGIN',Token='selected',CityID=9,StartTurn=turn}
          GameEvents.SPC_P0_Request.Fire(0,request)
          assert(shared.TimedProjectState.status=='ACTIVE',shared.TimedProjectState.reason)
          assert(writes==0)
          Events.PlayerTurnDeactivated.Fire(0)
          assert(shared.TimedProjectState.deactivated and writes==0)
          ExposedMembers.SPC_ProjectTurnRead=nil
          turn=turn+1
          Events.PlayerTurnActivated.Fire(0)
          assert(shared.TimedProjectState.status=='COMPLETED',shared.TimedProjectState.reason)
          Events.PlayerTurnActivated.Fire(0)
          assert(writes==1 and shared.TimedProjectState.attempts==1)
        ''', PROJECT)

    def test_temporary_switch_and_rollback_restore_the_exact_predecessor(self):
        with package(B454) as previous, package(B455) as retired:
            verify_package_round_trip(self, previous/'Mod', retired/'Mod', (REMOVED,), 'UI/ProjectTurnRead.lua')
