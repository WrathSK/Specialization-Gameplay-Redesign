"""B193/B194 guard and timeout presentation on the actual management window.
These tests preserve the distinction between a failed guard and its earlier startup sample.
They do not establish native SLEEP acceptance or task correctness.
"""
from pathlib import Path
import sqlite3
import unittest
from test_expedition_spy_activity_diagnostic_report import diagnostic_window

R = Path(__file__).resolve().parents[1]


def failure_window():
    lua = diagnostic_window()
    lua.execute("""
      local a=ExposedMembers.SPC_ExpeditionActivity
      failureSample={owner=a.owner,unitID=a.unitID,teamKey=a.teamKey,activityKey=a.activityKey,
       expectedName=a.expectedName,x=a.x,y=a.y,turn=currentTurn,
       phase='POST_REQUEST_READBACK',reason='ACTIVITY_UNEXPECTED_STATE',
       activity='4 (number)',awake='0 (number)',hold='2 (number)',sleep='1 (number)',
       operationEnum='4 (number)',equalsAwake='false (boolean)',equalsHold='false (boolean)',
       equalsSleep='false (boolean)',equalsOperation='true (boolean)',
       requested='true (boolean)',sleepAttempted='true (boolean)'}
      ExposedMembers.SPC_ExpeditionActivityFailureDiagnostic=failureSample
      activityChanged()
    """)
    return lua


class ActivityFailureReport(unittest.TestCase):
    def test_failure_precedes_separate_startup_without_replacing_either_sample(self):
        lua = failure_window()
        text = lua.eval('Controls.Report.text')
        self.assertLess(text.index('FAILURE_DIAGNOSTIC_HEADER'), text.index('SPY_DIAGNOSTIC_HEADER'))
        self.assertLess(text.index('SPY_DIAGNOSTIC_HEADER'), text.index('COUNT:'))
        self.assertEqual(text.count('FAILURE_DIAGNOSTIC_HEADER'), 1)
        self.assertEqual(text.count('SPY_DIAGNOSTIC_HEADER'), 1)
        for value in ('FAILURE_DIAGNOSTIC_HEADER:83',
                      'FAILURE_DIAGNOSTIC_PHASE_POST_REQUEST_READBACK',
                      'FAILURE_DIAGNOSTIC_ACTIVITY:4 (number)',
                      'FAILURE_DIAGNOSTIC_REQUEST:true (boolean),true (boolean)',
                      'FAILURE_DIAGNOSTIC_EQUAL_A:false (boolean),false (boolean)',
                      'FAILURE_DIAGNOSTIC_EQUAL_B:false (boolean),true (boolean)',
                      'DIAGNOSTIC_ENUM_B:1 (number),4 (number)',
                      'SPY_DIAGNOSTIC_ACTIVITY:number: 7,boolean: false'):
            self.assertIn(value, text)

    def test_timeout_labels_last_read_timing_and_retains_initial_cause(self):
        lua = failure_window()
        lua.execute("""
          failureSample.phase='PENDING_TIMEOUT';failureSample.reason='ACTIVITY_SLEEP_TIMEOUT'
          failureSample.elapsed='10.25 (number)';failureSample.sampledElapsed='9.75 (number)'
          failureSample.sampleTurn=83;failureSample.turn=84
          local a=ExposedMembers.SPC_ExpeditionActivity
          a.activityFailure='ACTIVITY_RELEASE_STATE_UNKNOWN';a.error='ACTIVITY_RELEASE_STATE_UNKNOWN'
          activityChanged()
        """)
        text = lua.eval('Controls.Report.text')
        for part in ('FAILURE_DIAGNOSTIC_TIMEOUT_HEADER:84',
                     'FAILURE_DIAGNOSTIC_PHASE_PENDING_TIMEOUT',
                     'ACTIVITY_RELEASE_STATE_UNKNOWN', 'ACTIVITY_SLEEP_TIMEOUT',
                     'FAILURE_DIAGNOSTIC_TIMING:10.25 (number),9.75 (number),83',
                     'FAILURE_DIAGNOSTIC_TIMEOUT_ACTIVITY:4 (number)',
                     'FAILURE_DIAGNOSTIC_REQUEST:true (boolean),true (boolean)'):
            self.assertIn(part, text)
        self.assertNotIn('SPY_FAILURE_DIAGNOSTIC_HEADER:', text)
        self.assertNotIn('SPY_FAILURE_DIAGNOSTIC_ACTIVITY:', text)
        self.assertLess(text.index('FAILURE_DIAGNOSTIC_TIMEOUT_HEADER'), text.index('SPY_DIAGNOSTIC_HEADER'))
        self.assertIn('SPY_DIAGNOSTIC_HEADER:83', text)

    def test_timeout_does_not_invent_missing_read_timing(self):
        lua = failure_window()
        lua.execute("""
          failureSample.phase='PENDING_TIMEOUT';failureSample.reason='ACTIVITY_SLEEP_TIMEOUT'
          failureSample.elapsed='10 (number)';activityChanged()
        """)
        self.assertIn('FAILURE_DIAGNOSTIC_TIMING:10 (number),UNKNOWN,UNKNOWN',
                      lua.eval('Controls.Report.text'))

    def test_guard_reports_do_not_gain_timeout_timing_or_relabeling(self):
        for phase in ('PRE_REQUEST_GUARD', 'POST_REQUEST_READBACK'):
            with self.subTest(phase=phase):
                lua = failure_window()
                lua.globals().phase = phase
                lua.execute("failureSample.phase=phase;failureSample.elapsed='4 (number)';activityChanged()")
                text = lua.eval('Controls.Report.text')
                self.assertIn('FAILURE_DIAGNOSTIC_HEADER:83', text)
                self.assertIn('FAILURE_DIAGNOSTIC_ACTIVITY:4 (number)', text)
                self.assertNotIn('FAILURE_DIAGNOSTIC_TIMING', text)
                self.assertNotIn('FAILURE_DIAGNOSTIC_TIMEOUT_HEADER', text)

    def test_timeout_render_retains_sample_without_native_queries_or_requests(self):
        lua = failure_window()
        lua.execute("""
          failureSample.phase='PENDING_TIMEOUT';failureSample.reason='ACTIVITY_SLEEP_TIMEOUT'
          failureSample.elapsed='10 (number)';failureSample.sampledElapsed='9.75 (number)'
          failureSample.sampleTurn=83
          local n=sent;local native=nativeCalls
          UnitManager.GetActivityType=function()error('timeout report native read')end
          UnitManager.CanStartOperation=function()error('timeout report eligibility query')end
          for i=1,10 do activityChanged()end
          assert(sent==n and nativeCalls==native and destroys==0 and properties==0)
          assert(failureSample.reason=='ACTIVITY_SLEEP_TIMEOUT' and failureSample.sampledElapsed=='9.75 (number)')
          assert(Controls.Report.text:find('FAILURE_DIAGNOSTIC_TIMEOUT_HEADER:83',1,true))
        """)

    def test_pre_request_false_flags_remain_false_without_truthiness_coercion(self):
        lua = failure_window()
        lua.execute("""
          failureSample.phase='PRE_REQUEST_GUARD';failureSample.requested='false (boolean)'
          failureSample.sleepAttempted='false (boolean)';activityChanged()
        """)
        text = lua.eval('Controls.Report.text')
        self.assertIn('FAILURE_DIAGNOSTIC_PHASE_PRE_REQUEST_GUARD', text)
        self.assertIn('FAILURE_DIAGNOSTIC_REQUEST:false (boolean),false (boolean)', text)
        self.assertNotIn('FAILURE_DIAGNOSTIC_PHASE_POST_REQUEST_READBACK', text)

    def test_exact_identity_mismatch_suppresses_only_failure_sample(self):
        for field, value in (('owner', '3'), ('unitID', '40'), ('teamKey', '"other team"'),
                             ('activityKey', '"old task"'), ('expectedName', '"other name"'),
                             ('x', '99'), ('y', '99')):
            with self.subTest(field=field):
                lua = failure_window()
                lua.execute(f'failureSample.{field}={value};activityChanged()')
                text = lua.eval('Controls.Report.text')
                self.assertNotIn('FAILURE_DIAGNOSTIC_HEADER', text)
                self.assertIn('SPY_DIAGNOSTIC_HEADER', text)

    def test_mirror_losing_identity_field_does_not_adopt_old_sample(self):
        for field in ('expectedName', 'x', 'y'):
            with self.subTest(field=field):
                lua = failure_window()
                lua.execute(f'ExposedMembers.SPC_ExpeditionActivity.{field}=nil;activityChanged()')
                self.assertNotIn('FAILURE_DIAGNOSTIC_HEADER', lua.eval('Controls.Report.text'))

    def test_absent_malformed_cleared_and_changed_key_suppress_stale_failure(self):
        for change in ('ExposedMembers.SPC_ExpeditionActivityFailureDiagnostic=nil',
                       'ExposedMembers.SPC_ExpeditionActivityFailureDiagnostic="old"',
                       'ExposedMembers.SPC_ExpeditionActivity.activityKey="";failureSample.activityKey=""',
                       'ExposedMembers.SPC_ExpeditionActivity.activityKey=nil;failureSample.activityKey=nil',
                       'ExposedMembers.SPC_ExpeditionActivity.activityKey="new task"'):
            with self.subTest(change=change):
                lua = failure_window()
                lua.execute(change+';activityChanged()')
                self.assertNotIn('FAILURE_DIAGNOSTIC_HEADER', lua.eval('Controls.Report.text'))

    def test_unknown_phase_and_non_string_values_are_not_interpreted_as_success(self):
        lua = failure_window()
        lua.execute("""
          failureSample.phase='unrecognized';failureSample.requested=true
          failureSample.sleepAttempted=nil;failureSample.equalsOperation=1;activityChanged()
        """)
        text = lua.eval('Controls.Report.text')
        self.assertIn('FAILURE_DIAGNOSTIC_PHASE_UNKNOWN', text)
        self.assertIn('FAILURE_DIAGNOSTIC_REQUEST:UNKNOWN,UNKNOWN', text)
        self.assertIn('FAILURE_DIAGNOSTIC_EQUAL_B:false (boolean),UNKNOWN', text)

    def test_refresh_retains_failure_turn_instead_of_claiming_live_state(self):
        lua = failure_window()
        lua.execute('currentTurn=84;Controls.RefreshButton.click();activityChanged()')
        text = lua.eval('Controls.Report.text')
        self.assertIn('FAILURE_DIAGNOSTIC_HEADER:83', text)
        self.assertIn('SPY_DIAGNOSTIC_HEADER:83', text)
        self.assertNotIn('FAILURE_DIAGNOSTIC_HEADER:84', text)

    def test_render_neither_queries_native_nor_writes_or_changes_task(self):
        lua = failure_window()
        lua.execute("""
          local original=failureSample;local n=sent;local native=nativeCalls
          ExposedMembers.SPC_ExpeditionActivityFailureDiagnostic=setmetatable({}, {
           __index=original,__newindex=function()error('failure diagnostic write')end})
          UnitManager.GetActivityType=function()error('report native read')end
          UnitManager.CanStartOperation=function()error('report eligibility query')end
          for i=1,10 do activityChanged()end
          assert(Controls.Report.text:find('FAILURE_DIAGNOSTIC_HEADER:83',1,true))
          Controls.TaskButton.click()
          assert(sent==n and nativeCalls==native and destroys==0 and properties==0)
          assert(original.activity=='4 (number)' and original.requested=='true (boolean)')
        """)

    def test_end_removes_current_team_and_hides_both_samples(self):
        lua = failure_window()
        lua.execute("""
          Controls.EndButton.click();assert(destroys==1 and properties==0)
          assert(not Controls.Report.text:find('FAILURE_DIAGNOSTIC_HEADER',1,true))
          assert(not Controls.Report.text:find('SPY_DIAGNOSTIC_HEADER',1,true))
        """)

    def test_cold_session_cannot_render_retained_old_failure(self):
        lua = failure_window()
        lua.execute("""
          gameProperties={};SPCExpeditionSpyGate.Start(P,shared);Controls.RefreshButton.click()
          assert(not Controls.Report.text:find('FAILURE_DIAGNOSTIC_HEADER',1,true))
          assert(not Controls.Report.text:find('SPY_DIAGNOSTIC_HEADER',1,true))
          assert(Controls.Report.text:find('SPY_UNBOUND',1,true))
          assert(destroys==0 and properties==0)
        """)

    def test_localizations_distinguish_failure_time_and_request_from_acceptance(self):
        db = sqlite3.connect(':memory:')
        db.execute('CREATE TABLE LocalizedText(Language TEXT, Tag TEXT, Text TEXT, PRIMARY KEY(Language,Tag))')
        db.executescript((R/'Mod/Text/ExpeditionGate.sql').read_text())
        for key in ('HEADER', 'PHASE', 'PHASE_PRE_REQUEST_GUARD', 'PHASE_POST_REQUEST_READBACK',
                    'PHASE_UNKNOWN', 'ACTIVITY', 'REQUEST', 'EQUAL_A', 'EQUAL_B',
                    'PHASE_PENDING_TIMEOUT', 'TIMEOUT_HEADER', 'TIMEOUT_ACTIVITY', 'TIMING'):
            with self.subTest(key=key):
                rows=db.execute('SELECT Language,Text FROM LocalizedText WHERE Tag=?',
                                ('LOC_SPC_EXPEDITION_SPY_FAILURE_DIAGNOSTIC_'+key,)).fetchall()
                labels=dict(rows)
                self.assertEqual(set(labels), {'zh_Hans_CN', 'en_US'})
                self.assertTrue(all(labels.values()))
                if key == 'HEADER':
                    self.assertIn('失败瞬间采样', labels['zh_Hans_CN'])
                    self.assertIn('sample at failure', labels['en_US'])
                if key == 'TIMEOUT_HEADER':
                    self.assertIn('非超时瞬间新读取', labels['zh_Hans_CN'])
                    self.assertIn('not a fresh query at timeout', labels['en_US'])
                if key == 'TIMING':
                    self.assertTrue(all('{1}' in v and '{2}' in v and '{3}' in v for v in labels.values()))
                if key == 'REQUEST':
                    self.assertIn('不代表引擎已接受', labels['zh_Hans_CN'])
                    self.assertIn('not proof of native acceptance', labels['en_US'])
                if key in ('PHASE', 'REQUEST', 'EQUAL_A', 'EQUAL_B'):
                    self.assertTrue(all('{1}' in v and '{2}' in v for v in labels.values()))


if __name__ == '__main__':
    unittest.main()
