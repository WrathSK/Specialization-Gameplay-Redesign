"""Contract audit batch 2 (B547, 2026-11-26): legacy compatibility retired.

Owner decision 2026-11-25: before release there is no compatibility with old
versions or old saves. The Store's two-record test adapter, schema-1/PREPARED
records and Import, the City Property investment/template ledgers, the
CityFlowProbe/BindingProbe routes, the subrecord rebuild candidates and the
SampleLifecycle engine-API fallbacks are gone from the runtime package. Their
code stays in Git history. Static absence only; behaviour is covered by the
CurrentGameplay stage.
"""
import re
import unittest
from pathlib import Path

MOD = Path(__file__).resolve().parents[1] / 'Mod'


def src(name):
    return (MOD / (name + '.lua')).read_text()


def production():
    return {p.stem: p.read_text(errors='replace') for p in MOD.rglob('*.lua')}


class Retired(unittest.TestCase):
    def test_no_runtime_module_names_a_retired_route(self):
        retired = ('StartLegacyTest', 'legacyTest', 'BlocksLegacy', 'UsesNewAuthority', 'CityFlowProbe',
                   'BindingProbe', 'KnownCandidate', 'TemplateMetadataCandidate', 'CompletedClaimCandidate',
                   'NeedsTemplateMetadata', 'NeedsCompletedClaimCleanup', 'subrecordRecovery')
        hits = sorted((name, word) for name, text in production().items() for word in retired if word in text)
        self.assertEqual(hits, [])

    def test_store_has_one_authority_and_no_import(self):
        s = src('CityProgressionStore')
        self.assertIn('function SPCCityProgressionStore.Start(P,shared)\n', s)
        for word in ('modern', 'TWO_CITY_TEST_LIMIT', "'PREPARED'", 'function d.Import', 'function store.Import',
                     'IMPORT_SOURCE_CHANGED', 'STORE_LEGACY_KEY', 'validateCollection'):
            self.assertNotIn(word, s, word)
        self.assertNotIn('r.schema==1', s)
        self.assertNotIn('r.schema==1', src('StoreDeferredLifecycle'))

    def test_ledgers_have_no_city_property_fallback(self):
        for name in ('InvestmentAction', 'EffectiveFacts'):
            self.assertNotIn('SPC_DEV_INVESTMENT_LEDGER_V1', src(name), name)
        self.assertNotIn('OnPermanentCityWrite', src('InvestmentAction'))
        std = src('Standardization')
        self.assertNotIn('SPC_STANDARDIZATION_LEDGER_V1', std)
        self.assertRegex(std, r'local function read\(c\)return shared\.CityProgressionStore\.ReadTemplates\(c\)end')

    def test_network_input_has_no_untracked_city_branch(self):
        s = src('NetworkInput')
        self.assertNotIn('untracked', s)
        self.assertNotIn('SPC_DEV_CITY_FLOW_B020', s)

    def test_commerce_unadmitted_city_is_unknown(self):
        s = src('Commerce')
        self.assertIn("assert(store.Owns(c),'COMMERCE_SOURCE_UNADMITTED')", s)

    def test_sample_lifecycle_calls_engine_api_directly(self):
        s = src('SampleLifecycle')
        self.assertNotIn('old compatibility adapter', s)
        self.assertNotIn("type(districts.FindID)", s)
        self.assertIsNone(re.search(r"type\(Map\.GetAdjacentPlot\)", s))


if __name__ == '__main__':
    unittest.main()
