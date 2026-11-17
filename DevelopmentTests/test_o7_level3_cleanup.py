"""Compare the transferred level-three cleanup with the published real owners."""

import unittest

from refactor_harness import ROOT, TrackedLua51, measure
from retired_crew_sources import B522, B523, RETIRED_LEVEL3_FILES, package, source
from test_b239_commerce_integration import SETUP
from test_o7_crew_retirement import verify_package_round_trip, verify_stable_round_trip


class Level3Cleanup(unittest.TestCase):
    def test_load_scoped_retry_and_report_match_former_owners(self):
        runs = []
        for historical in (True, False):
            lua = TrackedLua51(unpack_returned_tuples=True)
            lua.globals().include = lambda name: lua.execute((ROOT/'Mod'/f'{name}.lua').read_text())
            lua.execute(SETUP)
            lua.execute("""
              runners={};shared.LegacyCleanup={RegisterRunner=function(name,runner)
                assert(not runners[name] and type(runner)=='function')
                runners[name]=runner
              end}
              for _,c in ipairs(cities)do c.GetPopulation=function()return 7 end end
            """)
            if historical:
                for file in RETIRED_LEVEL3_FILES:
                    lua.execute(source(file, B522))
                lua.execute("""
                  SPCLv3Support.Start(P,shared,{centralExit=true})
                  SPCLv3Effects.Start(P,shared,{retireCommerce=true,centralExit=true})
                """)
            else:
                lua.execute("""
                  include('LegacyCleanup')
                  SPCLegacyCleanup.StartLv3Support(P,shared)
                  SPCLegacyCleanup.StartLv3Effects(P,shared)
                  assert(SPCLv3Support==nil and SPCLv3Effects==nil)
                """)
            lua.execute("""
              local a,b,foreign=cities[1],cities[2],cities[3]
              local support,effects=shared.Lv3Support,shared.Lv3Effects
              local groups={SPCTombstones.Names('SpecialistSupport'),SPCTombstones.Names('Lv3Culture')}
              for _,kind in ipairs({'RESEARCH','CULTURE','INDUSTRY'})do
                groups[2][#groups[2]+1]='BUILDING_SPC_DEV_LV3_COM_'..kind
              end
              for _,c in ipairs(cities)do
                for _,group in ipairs(groups)do for _,name in ipairs(group)do c.built[name]=true end end
                c.built.KEEP_EXTERNAL=true;c.built.BUILDING_SPC_COMMERCE_GOLD_0=true
              end
              local log,count={},{}
              local remove,has=P.RemoveBuilding,P.HasBuilding
              local fault,held=groups[1][1],groups[2][2]
              P.HasBuilding=function(buildings,id)
                if buildings==a.built and id==fault then return nil end
                return has(buildings,id)
              end
              P.RemoveBuilding=function(buildings,id)
                for _,city in ipairs(cities)do if city.built==buildings then log[#log+1]=city.id..':'..id end end
                return remove(buildings,id)
              end
              P.Count=function(k)count[k]=(count[k] or 0)+1 end
              local function contained(c,names)
                local n=0;for _,name in ipairs(names)do if c.built[name]then n=n+1 end end;return n
              end
              assert(runners.Lv3Support and runners.Lv3Effects and not support.ready and not effects.ready)
              failRemove=held;emit('LoadScreenClose')
              assert(support.errors['0:1'] and effects.errors['0:1'])
              assert(contained(a,groups[1])==12 and contained(a,groups[2])==10)
              assert(contained(b,groups[1])==0 and contained(foreign,groups[1])==0)
              assert(b.built[held] and foreign.built[held])
              local before=removeCount
              fault=nil;failRemove=nil
              support.Audit({player=0,city=2});assert(removeCount==before and support.errors['0:1'])
              support.Audit({player=0,city=1});assert(not support.errors['0:1'] and contained(a,groups[1])==0)
              effects.Audit({player=0,city=1});assert(not effects.errors['0:1'] and contained(a,groups[2])==0)
              assert(b.built[held] and foreign.built[held])
              effects.Audit({player=0,city=2});effects.Audit({player=3,city=3})
              assert(not b.built[held] and not foreign.built[held])
              local writes,scans=removeCount,count.city_scan
              for i=1,12 do support.Audit({player=0,city=1});effects.Audit({player=0,city=1})end
              assert(removeCount==writes and count.city_scan==scans)
              local report=support.Describe(0,a)..effects.Describe(0,a)
              assert(removeCount==writes)
              for _,c in ipairs(cities)do assert(c.built.KEEP_EXTERNAL and c.built.BUILDING_SPC_COMMERCE_GOLD_0)end
              result=table.concat(log,'|')..'|'..reads..'|'..scans..'|'..report
            """)
            runs.append(lua.eval('result'))
        self.assertEqual(*runs)
        measure('level3_retired_group_handoff', {'cold_groups': [12, 11],
                'exact_native_write_order_matches': True, 'warm_idle_extra_city_visits': 0})

    def test_exact_two_file_removal_round_trips(self):
        with package(B522) as before, package(B523) as after:
            original, mod = before/'Mod', after/'Mod'
            for path in ('CityProgressionStore.lua', 'LegacyCleanupCatalog.lua', 'Tombstones.lua',
                         'Data/Lv3Effects.sql', 'Data/Lv3Support.sql'):
                self.assertEqual((original/path).read_bytes(), (mod/path).read_bytes(), path)
            verify_package_round_trip(self, original, mod, RETIRED_LEVEL3_FILES, 'LegacyCleanup.lua')
            verify_stable_round_trip(self, original, mod, RETIRED_LEVEL3_FILES)
