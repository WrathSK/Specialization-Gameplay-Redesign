"""B192 historical activity diagnostic presentation on the actual management window.
Only the sample renderer is exercised; native readers and writer behavior are separate gates.
"""
from pathlib import Path
import sqlite3
import unittest
from test_expedition_spy_activity_report import held_window

R = Path(__file__).resolve().parents[1]


def diagnostic_window():
    lua = held_window('ACTIVITY_UNEXPECTED_STATE')
    lua.execute("""
      local a=ExposedMembers.SPC_ExpeditionActivity
      sample={owner=a.owner,unitID=a.unitID,teamKey=a.teamKey,activityKey=a.activityKey,
       expectedName=a.expectedName,x=a.x,y=a.y,turn=currentTurn,
       activity='number: 7',awake='number: 0',hold='number: 2',sleep='number: 1',
       operationEnum='number: 3',ready='boolean: false',operation='number: -1',
       endTurn='nil: nil',hash='number: -12345',eligibility='boolean: true',eligibilityStatus='ALLOWED'}
      ExposedMembers.SPC_ExpeditionActivityDiagnostic=sample
      activityChanged()
    """)
    return lua


class ActivityDiagnosticReport(unittest.TestCase):
    def test_readable_sample_near_top_preserves_exact_values_and_types(self):
        lua = diagnostic_window()
        text = lua.eval('Controls.Report.text')
        self.assertLess(text.index('DIAGNOSTIC_HEADER'), text.index('COUNT:'))
        for part in ('DIAGNOSTIC_HEADER:83', 'DIAGNOSTIC_ACTIVITY:number: 7,boolean: false',
                     'DIAGNOSTIC_ENUM_A:number: 0,number: 2',
                     'DIAGNOSTIC_ENUM_B:number: 1,number: 3',
                     'DIAGNOSTIC_SPY:number: -1,nil: nil',
                     'DIAGNOSTIC_SLEEP_HASH:number: -12345', 'DIAGNOSTIC_ALLOWED', 'boolean: true'):
            self.assertIn(part, text)
        self.assertEqual(text.count('DIAGNOSTIC_HEADER'), 1)
        self.assertIn('ACTIVITY_UNEXPECTED_STATE', text)

    def test_other_unit_owner_team_key_name_or_position_sample_is_not_shown(self):
        for field, value in (('owner', '3'), ('unitID', '40'), ('teamKey', '"other team"'),
                             ('activityKey', '"old task"'), ('expectedName', '"other name"'),
                             ('x', '99'), ('y', '99')):
            with self.subTest(field=field):
                lua = diagnostic_window()
                lua.execute(f'sample.{field}={value};activityChanged()')
                self.assertNotIn('DIAGNOSTIC_HEADER', lua.eval('Controls.Report.text'))

    def test_empty_key_absent_or_malformed_sample_is_not_shown(self):
        for change in ('ExposedMembers.SPC_ExpeditionActivityDiagnostic=nil',
                       'ExposedMembers.SPC_ExpeditionActivityDiagnostic="old"',
                       'ExposedMembers.SPC_ExpeditionActivity.activityKey="";sample.activityKey=""',
                       'ExposedMembers.SPC_ExpeditionActivity.activityKey=nil;sample.activityKey=nil'):
            with self.subTest(change=change):
                lua = diagnostic_window()
                lua.execute(change+';activityChanged()')
                self.assertNotIn('DIAGNOSTIC_HEADER', lua.eval('Controls.Report.text'))

    def test_later_turn_and_refresh_keep_original_sample_turn_explicit(self):
        lua = diagnostic_window()
        lua.execute('currentTurn=84;Controls.RefreshButton.click();activityChanged()')
        text = lua.eval('Controls.Report.text')
        self.assertIn('DIAGNOSTIC_HEADER:83', text)
        self.assertNotIn('DIAGNOSTIC_HEADER:84', text)

    def test_denied_unknown_and_numeric_one_are_not_coerced_to_allowed(self):
        for raw, status in (('boolean: false', 'DENIED'), ('number: 1', 'UNKNOWN'),
                            ('UNKNOWN: API unavailable', 'UNKNOWN')):
            with self.subTest(raw=raw):
                lua = diagnostic_window()
                lua.globals().new_raw = raw
                lua.globals().new_status = status
                lua.execute('sample.eligibility=new_raw;sample.eligibilityStatus=new_status;activityChanged()')
                text = lua.eval('Controls.Report.text')
                self.assertIn('DIAGNOSTIC_'+status, text)
                self.assertIn(raw, text)
                self.assertNotIn('DIAGNOSTIC_ALLOWED', text)

    def test_render_does_not_mutate_sample_query_native_or_send_requests(self):
        lua = diagnostic_window()
        lua.execute("""
          local original=sample;local n=sent;local native=nativeCalls
          ExposedMembers.SPC_ExpeditionActivityDiagnostic=setmetatable({}, {
           __index=original,__newindex=function()error('diagnostic write')end})
          UnitManager.GetActivityType=function()error('report native read')end
          UnitManager.IsReadyToMove=function()error('report native read')end
          UnitManager.CanStartOperation=function()error('report eligibility query')end
          for i=1,10 do activityChanged()end
          assert(sent==n and nativeCalls==native and destroys==0 and properties==0)
          assert(Controls.Report.text:find('DIAGNOSTIC_HEADER:83',1,true))
          assert(original.activity=='number: 7' and original.eligibility=='boolean: true')
        """)

    def test_held_task_controls_and_exact_end_are_unchanged(self):
        lua = diagnostic_window()
        lua.execute("""
          local n=sent;Controls.TaskButton.click();assert(sent==n)
          Controls.RefreshButton.click();assert(Controls.Report.text:find('DIAGNOSTIC_HEADER',1,true))
          Controls.EndButton.click();assert(destroys==1 and properties==0)
          assert(not Controls.Report.text:find('DIAGNOSTIC_HEADER',1,true))
        """)

    def test_cold_session_cannot_render_retained_old_sample(self):
        lua = diagnostic_window()
        lua.execute("""
          gameProperties={};SPCExpeditionSpyGate.Start(P,shared);Controls.RefreshButton.click()
          assert(not Controls.Report.text:find('DIAGNOSTIC_HEADER',1,true))
          assert(Controls.Report.text:find('SPY_UNBOUND',1,true))
          assert(destroys==0 and properties==0)
        """)

    def test_localizations_explicitly_label_historical_sample_in_both_languages(self):
        db = sqlite3.connect(':memory:')
        db.execute('CREATE TABLE LocalizedText(Language TEXT, Tag TEXT, Text TEXT, PRIMARY KEY(Language,Tag))')
        db.executescript((R/'Mod/Text/ExpeditionGate.sql').read_text())
        for key in ('HEADER', 'ACTIVITY', 'ENUM_A', 'ENUM_B', 'SPY', 'SLEEP_HASH',
                    'ELIGIBILITY', 'ALLOWED', 'DENIED', 'UNKNOWN'):
            with self.subTest(key=key):
                rows=db.execute('SELECT Language,Text FROM LocalizedText WHERE Tag=?',
                                ('LOC_SPC_EXPEDITION_SPY_DIAGNOSTIC_'+key,)).fetchall()
                self.assertEqual({row[0] for row in rows}, {'zh_Hans_CN', 'en_US'})
                self.assertTrue(all(row[1] for row in rows))
                if key == 'HEADER':
                    labels=dict(rows)
                    self.assertIn('历史采样，非实时状态', labels['zh_Hans_CN'])
                    self.assertIn('historical sample, not live state', labels['en_US'])
                    self.assertTrue(all('{1}' in row[1] for row in rows))


if __name__ == '__main__':
    unittest.main()
