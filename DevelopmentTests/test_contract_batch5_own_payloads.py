"""Contract audit batch 5 (B550, 2026-11-26): own payloads are not re-validated.

Data our own code produced is validated once at the save boundary (Store write
and load). Models do not re-check the saved value they copy, and consumers do not
re-check types and ranges of what our producers hand them. Freshness, identity,
native-read checks and load-time validation stay. Behaviour is otherwise covered
by the CurrentGameplay stage.
"""
import unittest
from pathlib import Path

import lupa.lua51 as lua51

MOD = Path(__file__).resolve().parents[1] / 'Mod'


def src(name):
    return (MOD / (name + '.lua')).read_text()


def runtime(*names):
    lua = lua51.LuaRuntime(unpack_returned_tuples=True)
    def load(name):
        path = MOD / (name + '.lua')
        lua.execute((path if path.exists() else MOD / 'UI' / (name + '.lua')).read_text())
    lua.globals().include = load
    for name in names:
        load(name)
    return lua


class Behaviour(unittest.TestCase):
    def test_reputation_use_unknown_only_for_a_real_unknown_active(self):
        lua = runtime('TurnLedger', 'CommerceModel')
        lua.execute("""
          local M=SPCCommerceModel
          local use=M.ReputationUse({status='CONFIRMED',age=12,state='COUNTING'},{activeStatus='UNKNOWN_GOVERNOR'})
          assert(use.status=='UNKNOWN' and use.reason=='COMMERCE_REPUTATION_QUALIFICATION_UNKNOWN')
          use=M.ReputationUse({status='CONFIRMED',age=12,state='COUNTING'},{activeStatus='KNOWN',active=4,potential=4,specialization='COMMERCE'})
          assert(use.status=='CONFIRMED' and use.effective==12)
          assert(not pcall(M.ReputationUse,{status='CONFIRMED'},nil)) -- facts are always produced by EffectiveFacts
        """)

    def test_malformed_transfer_scope_throws_instead_of_widening(self):
        s = src('RuntimeWork')
        self.assertIn("'RUNTIME_TRANSFER_SCOPE_INVALID'", s)
        self.assertNotIn("if type(transfer)=='table' and valid(transfer.owner)", s)

    def test_view_observer_trusts_row_shape_and_still_tracks_changes(self):
        lua = runtime('SafeAdapters')
        lua.execute("""
          local o=SPCSafeAdapters.NewViewObserver();local b={revision=1}
          assert(o.Observe(b,'0:1',{revision=1,token='T',reference='R'})==true)
          assert(o.Observe(b,'0:1',{revision=1,token='T',reference='R'})==false)
          assert(o.Observe(b,'0:1',{revision=2,token='T',reference={owner=0,cityID=1,x=2,y=3}})==true)
          assert(o.Observe(b,'0:1',nil)==true)
        """)


class Source(unittest.TestCase):
    def test_removed_rechecks(self):
        cases = {
            'CityProgressionStore': ('serial>=9007199254740992', "#input>512", "if type(a)~='table'then return nil end",
                                     "#token>256 then return 'IDENTITY_UNAVAILABLE'"),
            'SampleLifecycle': ('type(prior.value)', 'not integer(r.cityID)'),
            'RuntimeGC': ("'GC开关请求无效'", "'GC请求标识无效；未执行'"),
            'ExpeditionSpyStore': ("'PROPERTY_READER_UNAVAILABLE'", "'PROPERTY_WRITER_UNAVAILABLE'", "'STORE_EXPECTED_INVALID'"),
            'NetworkBridge': ('RouteSignalRevision or 0', 'not P.RouteUnitRelevant or', "type(provider.NetworkCityGeneration)"),
            'NetworkInput': ('SPCBoostConfig and',),
            'CommerceModel': ('M.Validate(v);assert(domains[domain]', 'M.Validate(v);return M.New'),
            'DevelopmentInvestment': ('v.protocol==2',),
            'StandardizationEffects': ('getmetatable(q)==nil', 'ExposedMembers.SPC_StandardizationProgressRead==read'),
            'InstitutionPresentation': ("type(v.potential)=='number'",),
        }
        hits = [(name, word) for name, words in cases.items() for word in words if word in src(name)]
        ui = {'UI/SafeAdapters': ('revision<9007199254740992', '#token>512'),
              'UI/CityPotential': ('getmetatable(row)', 'getmetatable(reply)'),
              'UI/CommerceUI': ("type(v.potential)=='number'",),
              'UI/TimedProjectSelectionClient': ("'TIMED_UI_SERIAL'", "'TIMED_UI_SLOTS'", "'TIMED_UI_EPOCH'"),
              'UI/DialogueRefresh': ("type(f)=='table'",)}
        hits += [(name, word) for name, words in ui.items() for word in words if word in src(name)]
        self.assertEqual(hits, [])

    def test_models_validate_results_not_the_saved_copy(self):
        for name, copy in (('CapitalInvestmentModel', 'local n=copy(old or M.New());M.Validate(n)'),
                           ('DevelopmentInvestmentModel', 'local n=M.Copy(old or M.New());M.Validate(n)'),
                           ('DialogueProjectModel', 'v=copy(v or M.New());M.Validate(v)'),
                           ('EngineeringStudyModel', 'v=copy(v or M.New());M.Validate(v)')):
            s = src(name)
            self.assertNotIn(copy, s, name)
            self.assertIn('return M.Validate(', s.replace('M.Validate(v);return v', 'return M.Validate(v)'), name)


if __name__ == '__main__':
    unittest.main()
