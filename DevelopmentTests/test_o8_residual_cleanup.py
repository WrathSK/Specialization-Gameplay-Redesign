"""Retire only inert controls and unloaded files; production ownership is unchanged."""
import ast
import unittest
from unittest.mock import patch
import xml.etree.ElementTree as ET

from refactor_harness import PackageVFS, ROOT, TrackedLua51, legacy_source_observation, measure
from retired_crew_sources import B527, package, source
from test_o7_crew_retirement import verify_package_round_trip
import test_o7_legacy_completion_record_retirement as roots
from test_pu11_package_absence import root as gameplay

REMOVED=tuple(sorted(('NetworkIsolation.lua','CityInheritance.lua','InheritanceShadow.lua','CityInheritanceRead.lua')))
GLOBALS=('SPCNetworkIsolation','SPCCityInheritance','SPCInheritanceShadow','SPCCityInheritanceRead')

class ResidualCleanup(unittest.TestCase):
    def test_actual_roots_keep_nonempty_route_proof_with_retired_globals_forbidden(self):
        def profile(*args,**kwargs):
            kwargs['forbidden_globals']=tuple(kwargs.get('forbidden_globals',()))+GLOBALS
            return PackageVFS(*args,**kwargs)
        with patch.object(roots,'PackageVFS',profile):
            packets,gp,ui,loaded=roots.routes(ROOT,B527,retired_culture=True,old_commerce_absent=True,
                worker_percent_absent=True,level3_absent=True,boost_absent=True,dialogue_absent=True)
        self.assertEqual(len(packets),3)
        self.assertEqual(gp['missing'],0)
        self.assertEqual(ui['missing'],0)
        self.assertTrue(all(loaded.get('Mod/'+name,0)==0 for name in REMOVED))
        measure('residual_cleanup_routes',dict(route_packets=len(packets),missing_includes=0,removed_modules=4))

    def test_removed_requests_do_not_invoke_old_modules_or_permanent_writes(self):
        c=gameplay(profile=PackageVFS(forbidden_globals=GLOBALS))
        c.execute("""
          local s=ExposedMembers.SPC_P0
          assert(s.NetworkIsolation==nil and s.StartStatus.NetworkIsolation==nil)
          retiredCalls=0;permanentWrites=0
          local function forbidden()retiredCalls=retiredCalls+1;error('RETIRED_DIAGNOSTIC_CALLED')end
          s.NetworkIsolation={Begin=forbidden,Read=forbidden}
          s.InheritanceShadow={Select=forbidden,Describe=forbidden}
          s.CityInheritance={Describe=forbidden}
          s.CityInheritanceRead={Record=forbidden,Read=forbidden}
          SPCP0.SetProperty=function()permanentWrites=permanentWrites+1;error('UNEXPECTED_PERMANENT_WRITE')end
          for _,action in ipairs({'NETWORK_ISOLATE','NETWORK_ISOLATION_READ','SHADOW_SELECT','SHADOW_READ','INHERIT_RECORD','INHERIT_READ'})do
            GameEvents.SPC_P0_Request.Fire(0,{Action=action,Token='removed-'..action,CityID=1,Epoch=1})
          end
          assert(retiredCalls==0 and permanentWrites==0)
        """)

    def test_exact_four_file_package_activation_and_restore_are_transactional(self):
        with package(B527) as before:
            verify_package_round_trip(self,before/'Mod',ROOT/'Mod',REMOVED,'Gameplay.lua')
        measure('residual_cleanup_package',dict(removed=list(REMOVED),native_deployment=False,exact_restore=True))

    def test_original_city_assertion_bodies_keep_exact_frozen_sources(self):
        # The old wrapper chain imports an unrelated B059 dispatcher fragment,
        # whose end marker is absent at both B527 and current source. Its full
        # historical result remains NOT_PASS; exercise the city bodies only.
        marker='stage("INITIALIZED ISOLATED_PROBES'
        self.assertNotIn(marker,source('Gameplay.lua',B527))
        self.assertNotIn(marker,(ROOT/'Mod/Gameplay.lua').read_text())
        for name in ('test_b063_inheritance_read.py','test_b064_shadow.py','test_b066_inheritance.py'):
            with self.subTest(script=name):
                path=ROOT/'DevelopmentTests'/name
                tree=ast.parse(path.read_text())
                predecessor=[n for n in tree.body if isinstance(n,ast.Expr) and isinstance(n.value,ast.Call)
                             and isinstance(n.value.func,ast.Name) and n.value.func.id=='exec']
                self.assertEqual(len(predecessor),1)
                # Do not echo the wrapper's historical predecessor-PASS banner.
                banners=[n for n in tree.body if isinstance(n,ast.Expr) and isinstance(n.value,ast.Call)
                         and isinstance(n.value.func,ast.Name) and n.value.func.id=='print']
                tree.body=[n for n in tree.body if n not in predecessor and n not in banners]
                namespace={'__file__':str(path),'__name__':'historical_city_assertions'}
                with patch('lupa.lua55.LuaRuntime',TrackedLua51),legacy_source_observation():
                    exec(compile(tree,str(path),'exec'),namespace)
        measure('historical_city_assertion_scope',dict(original_city_bodies=3,backend='Lua 5.1',
            original_assertions_changed=False,unrelated_wrapper_chain='NOT_PASS_B527_AND_CURRENT'))

    def test_manifest_has_no_retired_files_and_normal_owners_remain_byte_identical(self):
        vfs=PackageVFS()
        for name in REMOVED:
            self.assertNotIn(name,vfs.files)
            self.assertNotIn(name,vfs.imports)
            self.assertFalse((ROOT/'Mod'/name).exists())
        for name in ('NetworkBridge.lua','NetworkSender.lua','NetworkInput.lua','UI/BackgroundRoutes.lua',
                     'Commerce.lua','CultureNetwork.lua','StandardizationEffects.lua','LegacyCleanup.lua',
                     'CityProgressionStore.lua','RuntimeGC.lua'):
            self.assertEqual((ROOT/'Mod'/name).read_text(),source(name,B527),name)
        text=(ROOT/'Mod/Gameplay.lua').read_text()
        self.assertNotIn("composition.Run('NetworkIsolation'",text)
        panel=(ROOT/'Mod/UI/P0Panel.lua').read_text()
        for name in ('NETWORK_ISOLATE','NETWORK_ISOLATION_READ','SHADOW_SELECT','SHADOW_READ','INHERIT_RECORD','INHERIT_READ'):
            self.assertNotIn("'"+name+"'",text)
            self.assertNotIn("'"+name+"'",panel)
            self.assertNotIn('"'+name+'"',panel)
        doc=ET.parse(ROOT/'Mod/SpecializationP0.modinfo').getroot()
        self.assertEqual(doc.attrib['version'],'555')

if __name__=='__main__':unittest.main()
