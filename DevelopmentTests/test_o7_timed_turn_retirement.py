"""Retire the B116 ActionPanel override without retiring any formal project path."""
import unittest
import xml.etree.ElementTree as ET

from refactor_harness import PackageVFS
from retired_crew_sources import B452, B453, package as historical_package
from test_o7_crew_retirement import verify_package_round_trip
from test_pu11_package_absence import root as gameplay_root

REMOVED = ('TimedProductionProbe.lua', 'UI/TimedTurnProbe.lua')


class TimedTurnRetirement(unittest.TestCase):
    def test_exact_manifest_change_leaves_native_action_panel_selection(self):
        with historical_package(B452) as before, historical_package(B453) as after:
            manifest = before/'Mod/SpecializationP0.modinfo'
            doc = ET.parse(manifest)
            self.assertEqual(doc.getroot().get('version'), '479')
            actions = doc.find('./InGameActions')
            old = actions.find("ReplaceUIScript[@id='SPC_TimedTurnProbe']")
            self.assertEqual(old.get('criteria'), 'SPC_HDEnvironment')
            self.assertEqual(old.findtext('Properties/LuaContext'), 'ActionPanel')
            self.assertEqual(old.findtext('Properties/LuaReplace'), REMOVED[1])
            actions.remove(old)
            for section in (doc.find('./Files'), actions.find('ImportFiles')):
                nodes = [node for node in section.findall('File') if node.text in REMOVED]
                self.assertCountEqual([node.text for node in nodes], REMOVED)
                for node in nodes:
                    section.remove(node)
            doc.getroot().set('version', '480')
            retired = ET.parse(after/'Mod/SpecializationP0.modinfo')
            self.assertEqual(ET.canonicalize(ET.tostring(doc.getroot()), strip_text=True),
                             ET.canonicalize(ET.tostring(retired.getroot()), strip_text=True))

    def test_real_gameplay_starts_project_paths_and_ignores_old_commands(self):
        profile = PackageVFS()
        self.assertFalse(set(REMOVED) & (set(profile.files) | set(profile.imports)))
        game = gameplay_root(profile=profile)
        self.assertEqual(game.load_counts['missing'], 0)
        self.assertEqual(game.load_counts['failed'], 0)
        self.assertIsNone(game.globals().SPCTimedProductionProbe)
        shared = game.globals().ExposedMembers.SPC_P0
        self.assertIsNone(shared.StartStatus.TimedProductionProbe)
        for name in ('ClaimProjects', 'DialogueProjects', 'EngineeringStudyProjects',
                     'CrewProjects', 'ProjectTurnObservation', 'TimedProject'):
            self.assertEqual(shared.StartStatus[name].state, 'OK', name)
        shared.LastToken = 'previous-valid-request'
        properties = dict(game.globals().properties.items())
        for action in ('TIMED_PRODUCTION_BEGIN', 'TIMED_PRODUCTION_CANCEL'):
            game.execute("GameEvents.SPC_P0_Request.Fire(0,{Action=...,Token='retired',CityID=1,StartTurn=turn})", action)
            self.assertEqual(shared.RequestIngress.action, action)
            self.assertEqual(shared.LastToken, 'previous-valid-request')
            self.assertIsNone(shared.TimedProduction)
        self.assertEqual(dict(game.globals().properties.items()), properties)

    def test_whole_package_rollback_restores_both_removed_files(self):
        with historical_package(B452) as before, historical_package(B453) as after:
            verify_package_round_trip(self, before/'Mod', after/'Mod', REMOVED, 'UI/ProjectTurnRead.lua')
