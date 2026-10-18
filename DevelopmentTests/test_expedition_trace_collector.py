"""Unattended B205 collector tests; offline injected capture/clock, no live socket or Lua."""
import importlib.util
from pathlib import Path
import tempfile
import unittest
import re
import socket
import struct
import contextlib
import io
from unittest import mock

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


def frame(tag, text):
    payload = text.encode('utf-8')
    return struct.pack('<II', len(payload), tag) + payload


class TraceSocket:
    """Native reply fixture; the real reader still parses commands/frames/errors."""
    def __init__(self, rows, clock, window, done=True):
        self.rows, self.clock, self.window, self.done = rows, clock, window, done
        self.incoming = bytearray(frame(4, '70\0GameCore_Tuner\0'))
        self.sent = []
        self.closed = False

    def settimeout(self, value):
        pass

    def sendall(self, value):
        text = value[8:].rstrip(b'\0').decode()
        self.sent.append(text)
        if text.startswith('CMD:'):
            marker = re.search(r"print\('([^']+)'\.\.s\)", text).group(1)
            for row in self.rows + (['DONE'] if self.done else []):
                self.incoming.extend(frame(0xffffffff, '0\0' + marker + row + '\0'))

    def recv(self, size):
        if not self.incoming:
            self.clock.now += self.window
            raise socket.timeout()
        result = bytes(self.incoming[:size])
        del self.incoming[:size]
        return result

    def close(self):
        self.closed = True


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

    def test_activity_field_order_snapshot_live_and_dedup(self):
        record = ('[SPC][B205][TRAIN] seq=9 evaluationOrigin=NATIVE_EVENT '
                  'signalOrigin=PUBLISH stage=ACTIVITY_FAILURE guardStatus=DENIED')
        for prefix in ('GameCore_Tuner: ', reader.PREFIX + 'ENTRY 9 '):
            self.assertEqual(collector.train_line(prefix + record), record)
            self.assertEqual(reader.training_line(prefix + record), record)
        self.assertIsNotNone(self.session.add(record, 'snap'))
        self.assertIsNone(self.session.add(record, 'live'))
        self.assertEqual(self.session.stages['ACTIVITY_FAILURE'], 1)

    def test_field_order_parser_retains_boundaries(self):
        base = '[SPC][B205][TRAIN] seq=9 evaluationOrigin=NATIVE_EVENT '
        for suffix in ('', 'notstage=ACTIVITY_FAILURE', 'stage=bad',
                       'stage=ACTIVITY_FAILURE stage=OTHER', 'stage=ACTIVITY_FAILURE\nsecret'):
            self.assertIsNone(collector.train_line(base + suffix))
        self.assertIsNone(collector.train_line(base.replace('[B205]', '[B204]') + 'stage=OK'))
        self.assertIsNone(collector.train_line(base.replace('seq=9 ', 'seq=9x ') + 'stage=OK'))
        with self.assertRaises(reader.CaptureError):
            collector.train_line(base + 'stage=OK payload=' + 'x' * 4096)

    def test_dedup_population_and_cost_alerts(self):
        first = self.session.add(TRAIN % (1, 'UI_ROW', 16, '1'), 'snap')
        self.assertIn('COST_FLOOR_OBSERVED native=1 definition_base=60', first)
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
            on_record(reader.PREFIX + 'LISTENING seconds=' + str(record_seconds))
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

    def actual_capture(self, clock, responses, sockets):
        """Use production reader.capture: errors return ERROR + DONE, not exceptions."""
        def capture(mode, on_record, record_seconds):
            rows = responses.pop(0) if len(responses) > 1 else responses[0]
            fake = TraceSocket(rows, clock, record_seconds)
            sockets.append(fake)
            return reader.capture(mode, connect=lambda *a, **kw: fake, clock=clock,
                                  on_record=on_record, record_seconds=record_seconds)
        return capture

    def test_actual_reader_trace_unavailable_is_throttled_without_false_connected(self):
        clock, out, sockets = FakeClock(), [], []
        reason = collector.run(self.session,
                               capture=self.actual_capture(clock, [['ERROR TRACE_UNAVAILABLE']], sockets),
                               clock=clock, sleep=clock.sleep, retry=5, max_seconds=15, out=out.append)
        self.assertEqual(reason, 'MAX_DURATION')
        self.assertEqual(len(sockets), 3)  # t=0,5,10, never an immediate spin
        self.assertTrue(all(fake.closed for fake in sockets))
        self.assertEqual(sum(len(fake.sent) for fake in sockets), 9)
        self.assertFalse(any('Connected' in line for line in out))
        self.assertEqual(sum('Waiting' in line for line in out), 1)
        events = (self.session.directory / 'events.jsonl').read_text()
        self.assertEqual(events.count('"trace_error"'), 3)
        self.assertNotIn('"connected"', events)

    def test_actual_reader_invalid_trace_stops_instead_of_retrying(self):
        for error in ('TRACE_SCHEMA_INVALID', 'TRACE_ENTRIES_INVALID',
                      'TRACE_ENTRIES_SPARSE', 'TRACE_ENTRY_INVALID 3', 'TRACE_ENTRIES_OVER_LIMIT'):
            with self.subTest(error=error):
                clock, out, sockets = FakeClock(), [], []
                reason = collector.run(self.session,
                                       capture=self.actual_capture(clock, [['ERROR ' + error]], sockets),
                                       clock=clock, sleep=clock.sleep, retry=5, max_seconds=15, out=out.append)
                self.assertEqual(reason, error.split()[0])
                self.assertEqual(len(sockets), 1)
                self.assertTrue(sockets[0].closed)
                self.assertEqual(clock.now, 0)
                self.assertTrue(any('collection stopped' in line for line in out))
                self.assertFalse(any('Connected' in line for line in out))

    def test_invalid_trace_followed_by_disconnect_still_stops(self):
        clock, out = FakeClock(), []
        fake = TraceSocket(['ERROR TRACE_SCHEMA_INVALID'], clock, 10, done=False)
        def capture(mode, on_record, record_seconds):
            return reader.capture(mode, connect=lambda *a, **kw: fake, clock=clock,
                                  on_record=on_record, record_seconds=record_seconds)
        reason = collector.run(self.session, capture=capture, clock=clock, sleep=clock.sleep,
                               window=10, max_seconds=15, out=out.append)
        self.assertEqual(reason, 'TRACE_SCHEMA_INVALID')
        self.assertEqual(len(fake.sent), 3)
        self.assertTrue(fake.closed)
        self.assertNotIn('Connected', '\n'.join(out))

    def test_cli_reports_nonzero_for_invalid_trace(self):
        with mock.patch.object(collector, 'Session', return_value=self.session), \
             mock.patch.object(collector, 'run', return_value='TRACE_SCHEMA_INVALID'), \
             mock.patch.object(collector.signal, 'signal'), contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(collector.main([]), 1)
        summary = (self.session.directory / 'summary.txt').read_text()
        self.assertIn('end_reason: TRACE_SCHEMA_INVALID', summary)

    def test_actual_reader_recovers_once_trace_becomes_available(self):
        clock, out, sockets = FakeClock(), [], []
        responses = [['ERROR TRACE_UNAVAILABLE'],
                     ['META schema=205 sequence=1', 'ENTRY 1 ' + TRAIN % (1, 'UI_ROW', 16, '75')]]
        reason = collector.run(self.session, capture=self.actual_capture(clock, responses, sockets),
                               clock=clock, sleep=clock.sleep, window=10, retry=5,
                               max_seconds=15, out=lambda line: out.append((clock.now, line)))
        self.assertEqual(reason, 'MAX_DURATION')
        self.assertEqual(len(sockets), 2)
        self.assertEqual([(t, line) for t, line in out if 'Connected' in line],
                         [(5, 'Connected to the game; collecting. Press Ctrl-C to stop.')])
        self.assertEqual(len(self.session.seen), 1)
        self.assertEqual(self.session.alerts, [])

    def test_silent_nonlistening_return_is_not_collection_success(self):
        out = []
        reason = collector.run(self.session, capture=lambda *a, **kw: [], out=out.append)
        self.assertEqual(reason, 'CAPTURE_PROTOCOL_INVALID')
        self.assertFalse(any('Connected' in line for line in out))

    def test_progressed_native_costs_are_not_compared_to_base_as_errors(self):
        for i, cost in enumerate(('60', '75', '90', '45'), 1):
            with self.subTest(cost=cost):
                line = self.session.add(TRAIN % (i, 'UI_ROW', 16, cost), 'snap')
                self.assertIn('base/nativeCost=60/' + cost, line)
                self.assertNotIn('!!', line)
        self.assertEqual(self.session.alerts, [])
        self.assertEqual(self.session.cost_seen, set())

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
            on_record(reader.PREFIX + 'LISTENING seconds=' + str(record_seconds))
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
            on_record(reader.PREFIX + 'LISTENING seconds=' + str(record_seconds))
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

    def test_gate_prints_counted_and_logged(self):
        self.session.add_gate(reader.GATE_PREFIX + '[SPC][B191][N1_TASK] mission=WORKS outcome=SUCCESS civ=CIVILIZATION_X insight=NEW')
        self.session.add_gate(reader.GATE_PREFIX + '[SPC][B191][N1_SPY] action=DISPATCH owner=2 unit=40 phase=TRAVELLING error=nil')
        text = self.session.summary('TEST')
        self.assertIn('gate_prints: 2', text)
        self.assertIn('gate: TASK:WORKS x1', text)
        self.assertIn('gate: SPY:DISPATCH x1', text)

    def test_insight_summary_and_items_are_saved_in_order(self):
        lines = ['[SPC][B191][N1_INSIGHT] status=KNOWN owner=0 city=1 historical=2 effective=2',
                 '[SPC][B191][N1_INSIGHT] civ=CIVILIZATION_X category=WORKS effective=true']
        for line in lines:
            self.session.add_gate(reader.GATE_PREFIX + line)
        text = self.session.summary('TEST')
        self.assertIn('gate: INSIGHT:KNOWN x1', text)
        self.assertIn('gate: INSIGHT:WORKS x1', text)
        records = (self.session.directory / 'records.log').read_text().splitlines()
        self.assertTrue(records[0].endswith(lines[0]))
        self.assertTrue(records[1].endswith(lines[1]))

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
