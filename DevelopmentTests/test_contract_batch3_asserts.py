"""Contract audit batch 3 (B548, 2026-11-26): asserts at internal seams.

Inputs our own producers build are trusted by contract. A real UNKNOWN stays
UNKNOWN; a shape violation throws. Pure modules run in Lupa 2.8 (lua51); the
EffectiveFacts and FactConsumerBindings changes are checked in source, and their
behaviour by the CurrentGameplay stage.
"""
import unittest
from pathlib import Path

import lupa.lua51 as lua51

MOD = Path(__file__).resolve().parents[1] / 'Mod'


def runtime(*names):
    lua = lua51.LuaRuntime(unpack_returned_tuples=True)
    for name in names:
        lua.execute((MOD / (name + '.lua')).read_text())
    return lua


class FactUse(unittest.TestCase):
    def setUp(self):
        self.lua = runtime('FactUse')

    def test_real_unknown_stays_unknown(self):
        self.lua.execute("""
          local U=SPCFactUse
          assert(U.Qualification({specialization='COMMERCE',activeStatus='UNKNOWN_GOVERNOR'},'COMMERCE',3).status=='UNKNOWN')
          assert(U.Qualification({specialization='COMMERCE',activeStatus='KNOWN',active=4,investmentPending=true},'COMMERCE',3).status=='UNKNOWN')
          assert(U.Qualification({specialization='RESEARCH'},'COMMERCE',3).status=='NOT_APPLICABLE')
          assert(U.Qualification({specialization='COMMERCE',activeStatus='KNOWN',active=2},'COMMERCE',3).status=='NOT_APPLICABLE')
          assert(U.Qualification({specialization='COMMERCE',activeStatus='KNOWN',active=3},'COMMERCE',3).value==3)
          local snap={validity='VERIFIED',availability='READY',value={domains={A={value=4},B={depthError='TIER_INPUT_MISSING'}},
            districts={{id=7,type='T',plot=9,complete=true,pillaged=false}}}}
          assert(U.Depth(snap,'A').value==4 and U.Depth(snap,'B').status=='UNKNOWN' and U.Depth(snap,'C').status=='NOT_APPLICABLE')
          assert(U.Depth({validity='PENDING'},'A').status=='UNKNOWN')
          assert(U.Anchor(snap,{districtID=7,type='T'}).value.plot==9)
          assert(U.Anchor(snap,{districtID=8,type='T'}).status=='UNKNOWN')
          assert(U.Anchor({validity='PENDING'},{districtID=7,type='T'}).status=='UNKNOWN')
        """)

    def test_shape_violation_throws(self):
        self.lua.execute("""
          local U=SPCFactUse
          local function code(fn,...)local ok,e=pcall(fn,...);assert(not ok);return tostring(e):match('FACT_USE_[A-Z_]+')end
          assert(code(U.Qualification,nil,'COMMERCE',3)=='FACT_USE_IDENTITY_CONTRACT')
          assert(code(U.Qualification,{specialization='COMMERCE',activeStatus='KNOWN',active=2.5},'COMMERCE',3)=='FACT_USE_ACTIVE_CONTRACT')
          assert(code(U.Qualification,{specialization='COMMERCE',activeStatus='KNOWN',active=5},'COMMERCE',3)=='FACT_USE_ACTIVE_CONTRACT')
          local snap={validity='VERIFIED',availability='READY',value={domains={A={value='4'}},districts={{id=7,type='T',plot=9,complete=1,pillaged=false}}}}
          assert(code(U.Depth,snap,'A')=='FACT_USE_DEPTH_CONTRACT')
          assert(code(U.Anchor,snap,{districtID=7,type='T'})=='FACT_USE_ANCHOR_CONTRACT')
          assert(code(U.Anchor,snap,nil)=='FACT_USE_ANCHOR_CONTRACT')
        """)


class ReverseDependencies(unittest.TestCase):
    def test_bad_input_throws_and_capacity_still_disables(self):
        lua = runtime('ReverseDependencies')
        lua.execute("""
          local d=SPCReverseDependencies.New(4,2)
          assert(d.Replace(0,1,{[2]=true,[3]=true})==true and d.Dependents(0,2)[1])
          assert(not pcall(d.Replace,0,-1,{}) and not pcall(d.Replace,0,1,'x') and not pcall(d.Replace,0,1,{[1.5]=true}))
          assert(not pcall(d.Dependents,'0',2) and not pcall(d.Remove,0,nil))
          assert(d.Stats().unavailable==nil and d.Dependents(0,3)[1]) -- bad input never disables the index
          local ok,why=d.Replace(0,5,{[6]=true,[7]=true,[8]=true})
          assert(ok==false and why=='DEPENDENCY_INDEX_CAPACITY' and d.Dependents(0,2)==nil)
        """)


class DistrictCompleteness(unittest.TestCase):
    def test_missing_catalog_entry_throws_and_unplaced_input_is_gone(self):
        lua = runtime('DistrictCompleteness')
        lua.execute("""
          local cat={revision=1,Domain=function()return 'D' end,buildings={[1]={type='B1',ordinary=true,domain='D',tier=1},[9]={type='W',reason='WONDER'}}}
          local raw={districts={{id=1,type='T',plot=5,complete=true,pillaged=false,buildings={{index=1,complete=true,pillaged=false}}}},
            observations={{index=9,pillaged=false,plot=99}},unplaced={{type='X',reason='Y'}}}
          local out=SPCDistrictCompleteness.Calculate(cat,raw)
          assert(out.domains.D.value==1 and #out.excluded==1 and out.excluded[1].reason=='WONDER')
          raw.districts[1].buildings[1].index=2
          local ok,why=pcall(SPCDistrictCompleteness.Calculate,cat,raw)
          assert(not ok and tostring(why):find('DC_CATALOG_ENTRY_MISSING'))
        """)


class Source(unittest.TestCase):
    def test_governor_gate_known_contract_asserts(self):
        s = (MOD / 'EffectiveFacts.lua').read_text()
        self.assertIn("'GOVERNOR_GATE_CONTRACT'", s)
        self.assertIn("if gateStatus=='KNOWN' then", s)
        self.assertIn("out.activeStatus='UNKNOWN_GOVERNOR'", s)

    def test_bindings_throw_on_missing_method_and_call_network_directly(self):
        s = (MOD / 'FactConsumerBindings.lua').read_text()
        self.assertIn("error('FACT_BINDING_METHOD_MISSING '..row.target,0)", s)
        self.assertIn('value.RoleFactsChanged(e.player)', s)
        self.assertNotIn('value.RefreshFacts or value.Refresh', s)


if __name__ == '__main__':
    unittest.main()
