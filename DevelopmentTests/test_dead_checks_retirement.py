"""Contract audit batch 4 (B549, 2026-11-26): dead presence checks removed.

A module that fails to start leaves its shared export nil and its declared
dependants are skipped, so checks on declared dependencies, included modules and
always-defined methods could never fail. Static absence only; behaviour is
covered by the CurrentGameplay stage. Checks on modules that are not declared
dependencies stay (for example GreatWorkFacts on the Store, DevelopmentInvestment
on Commerce).
"""
import unittest
from pathlib import Path

MOD = Path(__file__).resolve().parents[1] / 'Mod'


def src(name):
    return (MOD / (name + '.lua')).read_text()


class Removed(unittest.TestCase):
    def test_declared_dependency_guards(self):
        cases = {
            'Commerce': ('shared.FactChanges and', 'bridge.ProofRevision and', 'bridge.TransactionCurrent and',
                         'if facts.WithPhase then', 'CurrentDomesticPartners', 'if shared.EffectiveFacts.Inspect then'),
            'CapitalInvestment': ('shared.Commerce and', 'not shared.Commerce.TransactionCurrent', 'not registry or'),
            'DevelopmentInvestment': ('if shared.FactChanges then', 'not registry or', 'if shared.EffectiveFacts.Inspect then'),
            'CrewProjects': ('if shared.FactChanges then',),
            'IndustryHistory': ('if shared.FactChanges then',),
            'InvestmentAction': ('if shared.CityProgressionStore then', 'if SPCUnitSiteFacts then'),
            'UnitActions': ('if SPCUnitSiteFacts then',),
            'UnitTargets': ('if SPCUnitSiteFacts then',),
            'Standardization': ('if shared.CityProgressionStore then',),
            'StandardizationEffects': ('store and store.HistoryStartStatus and', ' if store then'),
            'CultureInspiration': (' if store then',),
            'ExpeditionTraining': ('if shared.CityProgressionStore then', 'sameInputs', 'a.factsRead'),
            'Restructuring': ("'REST_STORE_UNAVAILABLE'", "'REST_FACTS_UNAVAILABLE'"),
            'EffectiveFacts': ('changes and changes.Generation', 'dc.FenceCarrierWrite and', 'pcall(dc.FenceCarrierWrite'),
            'GreatWorkFacts': ('shared.GreatWorkFacts.Shutdown', 'IsOwnedCarrier and', 'Describe and'),
            'CultureNetwork': ('effectAvailability==nil',),
            'CultureMeaningModel': ('bitParts', 'DiagnosticParts', 'function M.Parts(y,amount,variant)'),
            'StoreLifecycleRecovery': ("_MODEL_UNAVAILABLE'", "'DEFERRED_COPY_UNAVAILABLE'", "'DEFERRED_TRADITION_UNAVAILABLE'"),
            'CityProgressionStore': ('if not shared.FactChanges then return end', 'copyIndex(index)'),
            'RuntimeWork': ('if P.Count then', 'if P.Observe then', 'SPCRuntimeComposition and', 'pre-Store fixtures'),
        }
        hits = [(name, word) for name, words in cases.items() for word in words if word in src(name)]
        self.assertEqual(hits, [])

    def test_gameplay_wiring_calls_exported_methods(self):
        s = src('Gameplay')
        self.assertNotIn("type(network.ResumeProofRegistration)=='function'", s)
        self.assertNotIn('facts and facts.WithPhase then', s)

    def test_training_diagnostics_is_a_plain_include(self):
        for name in ('Commerce', 'CapitalInvestment', 'DevelopmentInvestment', 'CultureNetwork', 'NetworkBridge'):
            s = src(name)
            self.assertNotIn('traceLoaded', s, name)
            self.assertIn("include('ExpeditionTrainingDiagnostics')", s, name)

    def test_investment_adapters_require_their_observer(self):
        for name in ('CommerceUI', 'CapitalInvestmentUI', 'DevelopmentInvestmentUI'):
            s = (MOD / 'UI' / (name + '.lua')).read_text()
            self.assertIn("assert(observer,'UI_VIEW_OBSERVER_REQUIRED')", s, name)
            self.assertNotIn('if observer then', s, name)


class Kept(unittest.TestCase):
    """Second arms still reached by fixture doubles or frozen-baseline replays."""

    def test_documented_fixture_arms_remain(self):
        self.assertIn('LEGACY_NATIVE', src('CityReference'))
        self.assertIn('effective.NewReader and effective.NewReader()', src('RuntimeWork'))
        self.assertIn('if not service.Inspect then', src('CurrentSpecializationFacts'))
        self.assertIn('facts and facts.DistrictWriteVersion', src('DistrictCompleteness'))


if __name__ == '__main__':
    unittest.main()
