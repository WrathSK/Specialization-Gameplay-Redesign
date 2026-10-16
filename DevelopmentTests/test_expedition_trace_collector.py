"""Unattended B205 collector tests; offline injected capture/clock, no live socket or Lua."""
import importlib.util
from pathlib import Path
import tempfile
import unittest

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
spec = importlib.util.spec_from_file_location('expedition_trace_collector', ROOT / 'tools/collect_expedition_trace.py')
collector = importlib.util.module_from_spec(spec)
spec.loader.exec_module(collector)
reader = collector.reader

TRAIN = '[SPC][B205][TRAIN] seq=%d stage=%s context=GAMEPLAY:1:table0x1 turn=88 owner=0 city=393220 population=%d definitionCost=60 nativeCost=%s phase=TRAINING'


def snap(i, record):
    return reader.PREFIX + 'ENTRY %d %s' % (i, record)


class FakeClock:
    def __init__(self):
        self.now = 0.0

    def __call__(self):
        return self.now

    def sleep(self, seconds):
        self.now += seconds


class CollectorTests(unittest.TestCase):
    def setUp(self):
        (ROOT / 'local').mkdir(exist_ok=True)
        self.tmp = tempfile.TemporaryDirectory(dir=ROOT / 'local')
        self.session = collector.Session(root=Path(self.tmp.name), stamp='TEST')

    def tearDown(self):
        self.session.close()
        self.tmp.cleanup()

    def test_extracts_only_train_records(self):
        record = TRAIN % (5, 'UI_ROW', 16, '1')
        self.assertEqual(collector.train_line(snap(5, record)), record)
        self.assertEqual(collector.train_line('GameCore_Tuner: ' + record), record)
        self.assertIsNone(collector.train_line(reader.PREFIX + 'META schema=205 sequence=3'))
        self.assertIsNone(collector.train_line('secret engine output'))

    def test_dedup_population_and_cost_alerts(self):
        first = self.session.add(TRAIN % (1, 'UI_ROW', 16, '1'), 'snap')
        self.assertIn('COST_MISMATCH native=1 definition=60', first)
        self.assertIsNone(self.session.add(TRAIN % (1, 'UI_ROW', 16, '1'), 'live'))
        again = self.session.add(TRAIN % (2, 'MARKER_AFTER', 16, '1'), 'live')
        self.assertNotIn('!!', again)  # same mismatch reported once
        jump = self.session.add(TRAIN % (3, 'COMPLETION', 2447, '1'), 'live')
        self.assertIn('POPULATION_CHANGE city=393220 16->2447 stage=COMPLETION seq=3', jump)
        text = self.session.summary('TEST')
        self.assertIn('unique_records: 3', text)
        self.assertIn('alert: POPULATION_CHANGE', text)
        self.session.records.flush()
        logged = (self.session.directory / 'records.log').read_text().splitlines()
        self.assertEqual(len(logged), 3)

    def test_waits_collects_across_reconnects_and_exits_after_idle(self):
        clock = FakeClock()
        calls, out = [], []
        script = ['down', 'down', 'up', 'up', 'down', 'down', 'down', 'down', 'down', 'down']

        def capture(mode, on_record=None, record_seconds=None):
            calls.append((mode, record_seconds))
            step = script.pop(0) if script else 'down'
            if step == 'down':
                raise reader.CaptureError('SOCKET_UNAVAILABLE')
            clock.now += record_seconds
            on_record(snap(1, TRAIN % (1, 'UI_ROW', 16, '60')))
            on_record(reader.PREFIX + 'DONE')
            on_record(TRAIN % (len(calls), 'QUEUE_SAMPLE', 16, '60'))

        reason = collector.run(self.session, capture=capture, clock=clock, sleep=clock.sleep,
                               window=30, idle_exit=20, retry=5, out=out.append)
        self.assertEqual(reason, 'GAME_EXITED')
        self.assertTrue(all(c == ('record', 30) for c in calls))
        self.assertEqual(sum('Waiting for the game' in o for o in out), 2)  # once per outage
        self.assertEqual(len(self.session.seen), 3)  # repeated snapshot deduplicated

    def test_trace_errors_are_logged_not_fatal_and_max_duration_stops(self):
        clock = FakeClock()

        def capture(mode, on_record=None, record_seconds=None):
            on_record(reader.PREFIX + 'ERROR TRACE_UNAVAILABLE')
            raise reader.CaptureError('NATIVE_FUNCTION_UNAVAILABLE', 'SNAPSHOT')

        reason = collector.run(self.session, capture=capture, clock=clock, sleep=clock.sleep,
                               retry=5, max_seconds=60, out=lambda s: None)
        self.assertEqual(reason, 'MAX_DURATION')
        events = (self.session.directory / 'events.jsonl').read_text()
        self.assertIn('trace_error', events)
        self.assertIn('NATIVE_FUNCTION_UNAVAILABLE', events)

    def test_loading_context_timeout_counts_as_waiting(self):
        clock = FakeClock()
        out = []

        def capture(mode, on_record=None, record_seconds=None):
            raise reader.CaptureError('DEADLINE_EXCEEDED', 'CONTEXT')

        reason = collector.run(self.session, capture=capture, clock=clock, sleep=clock.sleep,
                               retry=5, max_seconds=30, out=out.append)
        self.assertEqual(reason, 'MAX_DURATION')
        self.assertEqual(sum('Waiting for the game' in o for o in out), 1)
        self.assertNotIn('capture_error', (self.session.directory / 'events.jsonl').read_text())

    def test_hd_prints_counted_not_deduplicated(self):
        clock = FakeClock()
        out = []

        def capture(mode, on_record=None, record_seconds=None):
            clock.now += record_seconds
            for _ in range(3):
                on_record(reader.HD_PREFIX + '北京 人口变化 1')
            on_record(reader.HD_PREFIX + '中心医院 北京 额外人口增长 随机数 37')
            on_record(reader.PREFIX + 'WINDOW_COMPLETE passive_records=0 hd_records=4 hd_dropped=7')

        collector.run(self.session, capture=capture, clock=clock, sleep=clock.sleep,
                      window=30, max_seconds=30, out=out.append)
        text = self.session.summary('TEST')
        self.assertIn('hd_prints: 4 (dropped by reader: 7)', text)
        self.assertIn('hd: population_change 1 x3', text)
        self.assertIn('hd: hospital x1', text)
        self.session.records.flush()
        self.assertEqual(len((self.session.directory / 'records.log').read_text().splitlines()), 4)
        self.assertEqual(len(self.session.seen), 0)

    def test_in_game_reload_keeps_waiting_and_logs_wait_codes(self):
        clock = FakeClock()
        out = []
        loading = [reader.CaptureError('CONNECTION_CLOSED', 'CONTEXT')] + \
            [reader.CaptureError('DEADLINE_EXCEEDED', 'CONTEXT')] * 20  # 100 s load
        script = ['up'] + loading + ['up'] + [reader.CaptureError('SOCKET_UNAVAILABLE')] * 10

        def capture(mode, on_record=None, record_seconds=None):
            step = script.pop(0) if script else reader.CaptureError('SOCKET_UNAVAILABLE')
            if step != 'up':
                raise step
            clock.now += record_seconds
            on_record(TRAIN % (len(script), 'LOAD_CLOSE', 16, '1'))

        reason = collector.run(self.session, capture=capture, clock=clock, sleep=clock.sleep,
                               window=30, idle_exit=30, retry=5, out=out.append)
        self.assertEqual(reason, 'GAME_EXITED')
        self.assertEqual(len(self.session.seen), 2)  # survived the long load, saw the second load
        events = (self.session.directory / 'events.jsonl').read_text()
        for code in ('CONNECTION_CLOSED', 'DEADLINE_EXCEEDED', 'SOCKET_UNAVAILABLE'):
            self.assertIn(code, events)
        self.assertEqual(events.count('"waiting"'), 3)  # logged once per code change

    def test_session_must_stay_under_local(self):
        with self.assertRaises(reader.CaptureError):
            collector.Session(root=Path(tempfile.gettempdir()) / 'spc-outside', stamp='X')

    def test_collector_source_issues_no_commands(self):
        source = (ROOT / 'tools/collect_expedition_trace.py').read_text()
        for forbidden in ('CMD:', 'sendall', 'SetProperty', 'RequestOperation', 'AppOptions',
                          'subprocess', 'collectgarbage', 'os.system'):
            self.assertNotIn(forbidden, source)


if __name__ == '__main__':
    unittest.main()
