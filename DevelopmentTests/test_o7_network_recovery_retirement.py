"""Exact retirement of the import-only derived network save prototype."""
import shutil
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import xml.etree.ElementTree as ET

from refactor_harness import measure
from retired_crew_sources import B453, B454, gameplay as historical_gameplay, package as historical_package
from test_deployment_removals import commit, deploy
from test_o7_crew_retirement import verify_package_round_trip
import test_o7_route_observer_retirement as route

REMOVED = ('NetworkRecoveryCell.lua', 'NetworkRecoveryModel.lua', 'NetworkRecoveryStore.lua')
GLOBALS = tuple('SPC' + Path(path).stem for path in REMOVED)

OLD_SLOT_GUARD = """
local prefix='SPC_DERIVED_NETWORK_RECOVERY_V1_'
recoveryKey=prefix..'CULTURE_FIXTURE'
properties[recoveryKey]='opaque-fixture-slot'
recoveryReads,recoveryWrites=0,0
local get,put=Game.GetProperty,Game.SetProperty
Game.GetProperty=function(key)
 if type(key)=='string' and key:sub(1,#prefix)==prefix then recoveryReads=recoveryReads+1 end
 return get(key)
end
Game.SetProperty=function(key,value)
 if type(key)=='string' and key:sub(1,#prefix)==prefix then recoveryWrites=recoveryWrites+1 end
 return put(key,value)
end
"""


class NetworkRecoveryRetirement(unittest.TestCase):
    def test_exact_manifest_and_store_scope(self):
        with historical_package(B453) as previous, historical_package(B454) as retired:
            doc = ET.parse(previous/'Mod/SpecializationP0.modinfo')
            for section in (doc.find('./Files'), doc.find('./InGameActions/ImportFiles')):
                removed = [n for n in section.findall('File') if n.text in REMOVED]
                self.assertCountEqual([n.text for n in removed], REMOVED)
                for n in removed:
                    section.remove(n)
            self.assertEqual(doc.getroot().get('version'), '480')
            doc.getroot().set('version', '481')
            current = ET.parse(retired/'Mod/SpecializationP0.modinfo')
            self.assertEqual(ET.canonicalize(ET.tostring(doc.getroot()), strip_text=True),
                             ET.canonicalize(ET.tostring(current.getroot()), strip_text=True))

            old_store = (previous/'Mod/CityProgressionStore.lua').read_text()
            for start,end in (
                (' -- Derived-source continuity scope,not current qualification or transaction proof.\n',
                 ' local function active(pid,c)\n'),
                (' function store.NetworkRecoveryStamp(pid,id,x,y,token)\n',
                 ' function store.ObserveTrainingFacts('),
            ):
                self.assertEqual(old_store.count(start), 1)
                self.assertEqual(old_store.count(end), 1)
                begin,finish = old_store.index(start),old_store.index(end)
                self.assertIn('NetworkRecoveryStamp', old_store[begin:finish])
                old_store = old_store[:begin] + old_store[finish:]
            self.assertEqual(old_store, (retired/'Mod/CityProgressionStore.lua').read_text())

    def test_real_route_roots_ignore_the_experimental_slot(self):
        with historical_package(B453) as previous, historical_package(B454) as retired, \
             patch.object(route,'NATIVE',route.NATIVE+OLD_SLOT_GUARD):
            old_game = historical_gameplay(previous,revision=B453,forbidden_globals=GLOBALS)
            old_ui = historical_gameplay(previous,revision=B453,name='UI/BackgroundRoutes',forbidden_globals=GLOBALS)
            new_game = historical_gameplay(retired,revision=B454,forbidden_globals=GLOBALS)
            self.assertFalse(set(REMOVED) & (new_game.vfs.files | new_game.vfs.imports))
            new_ui = historical_gameplay(retired,revision=B454,name='UI/BackgroundRoutes',forbidden_globals=GLOBALS)
            expected = route.exercise_proof(old_game,old_ui)
            observed = route.exercise_proof(new_game,new_ui)

        self.assertEqual(observed,expected)
        self.assertEqual(new_game.load_counts,old_game.load_counts)
        self.assertEqual(new_ui.load_counts,old_ui.load_counts)
        for context in (old_game,old_ui,new_game,new_ui):
            self.assertEqual(context.load_counts['missing'] + context.load_counts['failed'],0)
            self.assertTrue(context.eval("recoveryReads==0 and recoveryWrites==0 and properties[recoveryKey]=='opaque-fixture-slot'"))
        measure('network_recovery_retirement_route_roots', {
            'equal_proof_packets':len(observed),'nonempty_and_same_signal_reproof':True,
            'gameplay_loads':new_game.load_counts['completed'],'ui_loads':new_ui.load_counts['completed'],
            'experimental_key_reads':0,'experimental_key_writes':0,
        })

    def test_exact_temporary_package_round_trip(self):
        with historical_package(B453) as previous, historical_package(B454) as retired:
            verify_package_round_trip(self,previous/'Mod',retired/'Mod',REMOVED,'NetworkBridge.lua')

    def test_stable_receipt_and_recovery_cover_all_three_paths(self):
        with historical_package(B453) as previous, historical_package(B454) as retired, \
             tempfile.TemporaryDirectory(prefix='spc-stable-network-retirement-') as directory:
            root = Path(directory).resolve()
            stable = root/'Main/Mod'
            target = root/'Game/Mods/SpecializationP0'
            shutil.copytree(retired/'Mod',stable)
            shutil.copytree(previous/'Mod',target)
            commit(stable.parent,'main')
            before, after = deploy.snapshot(target),deploy.snapshot(stable)
            for allowed in ((),REMOVED[:-1],(*REMOVED,'NetworkBridge.lua')):
                with self.subTest(allowed=allowed), self.assertRaisesRegex(ValueError,'removal list mismatch'):
                    deploy.check(stable,target,allow_remove=allowed)
            self.assertEqual(deploy.snapshot(target),before)
            result = deploy.apply(stable,target,after['digest'],before['digest'],authorized=True,allow_remove=REMOVED)
            self.assertEqual(result['removed_paths'],list(REMOVED))
            self.assertEqual(deploy.snapshot(target),after)
            backup = Path(result['backup'])
            self.assertEqual(deploy.snapshot(backup),before)
            recovery = root/'RecoveredMain/Mod'
            shutil.copytree(backup,recovery)
            commit(recovery.parent,'main')
            deploy.apply(recovery,target,before['digest'],after['digest'],authorized=True)
            self.assertEqual(deploy.snapshot(target),before)
            self.assertFalse((target.parent/'.specialization-deploy-pending.json').exists())
