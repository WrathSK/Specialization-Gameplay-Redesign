"""B191 task failure presentation using the actual Gate and management window.
These are local presentation/identity-evidence checks, not native activity proof.
"""
from pathlib import Path
import sqlite3
import unittest
import test_expedition_spy_task as previous

R = Path(__file__).resolve().parents[1]


def held_window(reason="ACTIVITY_SLEEP_ROW_UNAVAILABLE"):
    lua = previous.gate(window=True)
    lua.execute("""
      gateOpen();Controls.CreateButton.click();Controls.ArmButton.click()
      arrival(41,true,false);Controls.RefreshButton.click();Controls.TaskButton.click()
      local token=lastPacket.Token
      handler(2,{Action='ACTIVITY',Token=token..':failed',UnitID=41,ActivityKey=ExposedMembers.SPC_ExpeditionActivity.activityKey,
       Result='FAILED',Owned=false,SampleTurn=currentTurn,
       Detail='ERROR_CODE'})
      activityChanged()
    """.replace("ERROR_CODE", reason))
    return lua


class ActivityReport(unittest.TestCase):
    def test_exact_activity_cause_near_top_without_generic_unbound_claim(self):
        lua = held_window()
        lua.execute("""
          local text=Controls.Report.text
          local specific=text:find('ACTIVITY_SLEEP_ROW_UNAVAILABLE',1,true)
          assert(specific and specific<text:find('COUNT:',1,true))
          assert(text:find('ACTIVITY_CAUSE_DATA',1,true))
          assert(text:find('HELD_RECHECK',1,true) and not text:find('HELD_MATCH',1,true))
          assert(not text:find('SPY_UNBOUND',1,true))
          assert(not text:find('IDENTITY_SUMMARY',1,true) and not text:find('NAME_READBACK',1,true))
          assert(not text:find('NAME_STAGE_CONFIRMED',1,true))
        """)

    def test_readable_categories_preserve_the_exact_specific_failure(self):
        for code, category in (
            ('ACTIVITY_SLEEP_API_UNAVAILABLE', 'ACTIVITY_CAUSE_API'),
            ('ACTIVITY_SLEEP_NOT_ALLOWED', 'ACTIVITY_CAUSE_DENIED'),
            ('ACTIVITY_WAKE_REJECTED', 'ACTIVITY_CAUSE_DENIED'),
            ('ACTIVITY_SLEEP_TIMEOUT', 'ACTIVITY_ERROR'),
        ):
            with self.subTest(code=code):
                lua = held_window(code)
                text = lua.eval('Controls.Report.text')
                self.assertIn(code, text)
                self.assertIn(category, text)
                self.assertLess(text.index(code), text.index('COUNT:'))

    def test_fresh_held_read_confirms_identity_but_does_not_enable_task(self):
        lua = held_window()
        lua.execute("""
          Controls.RefreshButton.click();local text=Controls.Report.text
          assert(text:find('HELD_MATCH',1,true) and text:find('IDENTITY_SUMMARY',1,true))
          assert(not text:find('SPY_UNBOUND',1,true) and not text:find('RETAINED_SOURCE',1,true))
          local reply=ExposedMembers.SPC_ExpeditionGateReply
          assert(reply.sameUnit and reply.nameVerified and reply.identity.sourceStatus=='MATCH')
          assert(reply.phase=='HELD' and reply.bound==false and reply.unbound==true)
          local count=sent;Controls.TaskButton.click();assert(sent==count)
          Controls.EndButton.click();assert(destroys==1)
        """)

    def test_fresh_unreadable_source_keeps_unknown_boundary(self):
        lua = held_window()
        lua.execute("""
          city.token=nil;Controls.RefreshButton.click();local text=Controls.Report.text
          assert(text:find('HELD_RECHECK',1,true) and not text:find('HELD_MATCH',1,true))
          assert(text:find('IDENTITY_SUMMARY',1,true) and text:find('IDENTITY_UNREADABLE',1,true))
          assert(not text:find('SPY_UNBOUND',1,true) and properties==0)
        """)

    def test_changed_transition_does_not_reuse_prior_matching_diagnostic(self):
        lua = held_window()
        lua.execute("""
          Controls.RefreshButton.click();assert(Controls.Report.text:find('HELD_MATCH',1,true))
          local view=ExposedMembers.SPC_ExpeditionActivity;view.revision=view.revision+1
          activityChanged();local text=Controls.Report.text
          assert(text:find('HELD_RECHECK',1,true) and not text:find('HELD_MATCH',1,true))
          assert(not text:find('IDENTITY_SUMMARY',1,true) and not text:find('NAME_READBACK',1,true))
        """)

    def test_changed_turn_requires_refresh_instead_of_claiming_current_match(self):
        lua = held_window()
        lua.execute("""
          Controls.RefreshButton.click();currentTurn=currentTurn+1;activityChanged()
          assert(Controls.Report.text:find('HELD_RECHECK',1,true))
          assert(not Controls.Report.text:find('HELD_MATCH',1,true))
        """)

    def test_other_team_mirror_cannot_replace_current_report(self):
        lua = held_window()
        lua.execute("""
          Controls.RefreshButton.click();local before=Controls.Report.text
          local view=ExposedMembers.SPC_ExpeditionActivity
          view.teamKey='different';view.activityFailure='ACTIVITY_OTHER_TEAM_ERROR'
          activityChanged();assert(Controls.Report.text==before)
        """)

    def test_cold_unbound_team_still_uses_existing_unbound_label(self):
        lua = previous.gate(window=True)
        lua.execute("""
          gateOpen();Controls.CreateButton.click();gameProperties={};SPCExpeditionSpyGate.Start(P,shared)
          Controls.RefreshButton.click();local text=Controls.Report.text
          assert(text:find('SPY_UNBOUND',1,true) and not text:find('HELD_MATCH',1,true))
          Controls.EndButton.click();assert(destroys==1)
        """)

    def test_new_labels_exist_in_both_languages_and_keep_source_placeholders(self):
        database = sqlite3.connect(':memory:')
        database.execute('CREATE TABLE LocalizedText(Language TEXT, Tag TEXT, Text TEXT, PRIMARY KEY(Language,Tag))')
        database.executescript((R/'Mod/Text/ExpeditionGate.sql').read_text())
        for key in ('HELD_MATCH', 'HELD_RECHECK', 'HELD_SOURCE', 'ACTIVITY_FAILURE', 'ACTIVITY_CAUSE_DATA', 'ACTIVITY_CAUSE_API', 'ACTIVITY_CAUSE_DENIED'):
            with self.subTest(key=key):
                rows=database.execute('SELECT Language,Text FROM LocalizedText WHERE Tag=?', ('LOC_SPC_EXPEDITION_SPY_'+key,)).fetchall()
                self.assertEqual({row[0] for row in rows}, {'zh_Hans_CN', 'en_US'})
                self.assertTrue(all(row[1] for row in rows))
                if key in ('HELD_SOURCE', 'ACTIVITY_FAILURE'):
                    self.assertTrue(all('{1}' in row[1] and '{2}' in row[1] for row in rows))


if __name__ == '__main__':
    unittest.main()
