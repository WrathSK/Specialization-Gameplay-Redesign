"""Current entrypoints with the eight retired experiments absent; historical swap at B536."""
import unittest
import xml.etree.ElementTree as ET
from unittest.mock import patch

from lupa.lua51 import LuaRuntime
from refactor_harness import ROOT
from retired_crew_sources import B535, package
from test_o7_crew_retirement import verify_package_round_trip, verify_stable_round_trip
import test_expedition_gate as old_fixture
import test_expedition_spy_gate as expedition

REMOVED = (
    'DistrictPrecisionProbe.lua', 'DistrictPrecisionRead.lua', 'ExpeditionGate.lua',
    'ExpeditionMovementProbe.lua', 'UI/CityIdentityEvidence.lua', 'UI/ExpeditionGateWindow.lua',
    'UI/ExpeditionMovementProbe.lua', 'UI/GreatWorkBasis.lua',
)


class Retirement(unittest.TestCase):
    def test_current_spy_and_window_work_without_any_old_implementation(self):
        with (patch.object(old_fixture, 'LuaRuntime', LuaRuntime),
              patch.object(old_fixture, 'source', side_effect=AssertionError('archived source read'))):
            for ui, window in ((False, False), (True, False), (True, True)):
                with self.subTest(ui=ui, window=window):
                    vm = expedition.gate(ui=ui, window=window)
                    vm.execute("""
                        assert(SPCExpeditionGate == nil and SPCExpeditionGateRead == nil)
                        assert(type(shared.ExpeditionGate.Training.Available) == 'function')
                        assert(req('CREATE', 'one').phase == 'CREATED' and initCalls == 1)
                        assert(req('READ', 'observe').unitID == 40 and initCalls == 1)
                    """)
                    if window:
                        vm.execute("assert(SPCExpeditionSpyUI and type(init) == 'function')")

    def test_current_package_keeps_the_real_actions_and_omits_the_eight_files(self):
        mod = ROOT / 'Mod'
        manifest = ET.parse(mod / 'SpecializationP0.modinfo')
        packaged = {node.text for node in manifest.findall('./Files/File')}
        runtime = {node.text for node in manifest.findall('./InGameActions/*/File')}
        self.assertTrue(set(REMOVED).isdisjoint(packaged | runtime))
        for path in REMOVED:
            self.assertFalse((mod / path).exists(), path)
        self.assertTrue({'Gameplay.lua', 'UI/ExpeditionSpyWindow.xml',
                         'UI/ExpeditionSpyActivity.xml'} <= runtime)

    def test_b535_to_b536_exact_package_and_restore(self):
        with package(B535) as previous:
            old_mod, new_mod = previous / 'Mod', ROOT / 'Mod'
            before = ET.parse(old_mod / 'SpecializationP0.modinfo').getroot()
            after = ET.parse(new_mod / 'SpecializationP0.modinfo').getroot()
            for parent in before.iter():
                for node in list(parent):
                    if node.tag == 'File' and node.text in REMOVED:
                        parent.remove(node)
            before.set('version', '563')
            # Compare all remaining actions, ordered children and files, ignoring indentation.
            for root in (before, after):
                ET.indent(root)
            self.assertEqual(ET.tostring(before), ET.tostring(after))
            verify_package_round_trip(self, old_mod, new_mod, REMOVED, 'ExpeditionSpyGate.lua')
            verify_stable_round_trip(self, old_mod, new_mod, REMOVED)
