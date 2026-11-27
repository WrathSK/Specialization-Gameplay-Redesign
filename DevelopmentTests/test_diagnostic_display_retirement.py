"""B552 (2026-11-27): the UI diagnostic display path is retired.

UI/BoostGreatWorkRead only served hidden Boost/GW-baseline controls and a
CultureMeaningView that no production module produced; its one live use
appended an old Great Work experiment tail to the Dialogue Project report.
The Gameplay request block for the retired L2 meaning probe went with it.
Static absence only; the Dialogue Project and Culture Meaning reports keep
their CurrentGameplay coverage.
"""
import unittest
from pathlib import Path

MOD = Path(__file__).resolve().parents[1] / 'Mod'


class Retired(unittest.TestCase):
    def test_reader_file_and_manifest_entries_are_gone(self):
        self.assertFalse((MOD / 'UI' / 'BoostGreatWorkRead.lua').exists())
        self.assertNotIn('BoostGreatWorkRead', (MOD / 'SpecializationP0.modinfo').read_text())

    def test_panel_has_no_diagnostic_display_state_or_controls(self):
        lua = (MOD / 'UI' / 'P0Panel.lua').read_text()
        xml = (MOD / 'UI' / 'P0Panel.xml').read_text()
        for word in ('BoostGreatWorkRead', 'CultureMeaningView', 'meaningResponse', 'meaningReadReference',
                     'BOOST_READ', 'BOOST_BASELINE', 'GW_BASELINE', 'CULTURE_MEANING_DIAGNOSTIC_READ'):
            self.assertNotIn(word, lua, word)
        for control in ('BoostReadButton', 'BoostBaseButton', 'GWBaselineButton'):
            self.assertNotIn(control, lua, control)
            self.assertNotIn('"%s"' % control, xml, control)

    def test_gameplay_has_no_probe_request_block(self):
        s = (MOD / 'Gameplay.lua').read_text()
        for word in ('CultureMeaningProbe', 'CultureMeaningView', "'BOOST_READ'", "'GW_BASELINE'", "'GW_READ'",
                     'CULTURE_MEANING_DIAGNOSTIC'):
            self.assertNotIn(word, s, word)
        self.assertIn("assert(shared.CultureMeaning,'ME_MODULE_NOT_READY').Describe(playerID,c)", s)
        self.assertIn("'意义延展：当前城市暂不可读。'", s)


if __name__ == '__main__':
    unittest.main()
