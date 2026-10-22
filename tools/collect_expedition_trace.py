#!/usr/bin/env python3
"""Unattended read-only B205 trace collector (development sessions).

Start it before or after launching the game; it waits for the local FireTuner
socket, then repeatedly runs the fixed read-only `record` capture from
read_expedition_trace.py (one ring snapshot plus a passive listening window),
reconnecting across loads until the game has been gone for --idle-exit seconds
(default 30). Only a refused connection counts as gone; a socket that accepts
but closes or times out during the handshake (an in-game load) keeps waiting. Ctrl-C/SIGTERM also stop it and still write the summary.

Every unique `[SPC][B205][TRAIN]` record is appended to a local session log and
summarized at the end. B206: allowlisted HD population/hospital prints are
logged as they arrive (not deduplicated; the first MAX_HD_LOGGED) and counted. It sends no gameplay command, changes no configuration,
launches nothing and runs no GC. Output stays under ignored local/diagnostics/.
"""
import argparse
from collections import Counter, OrderedDict
from datetime import datetime, timezone
import importlib.util
import json
from pathlib import Path
import re
import secrets
import signal
import sys
import time



HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
_memory_spec = importlib.util.spec_from_file_location('spc_memory_evidence', HERE / 'memory_evidence.py')
_memory = importlib.util.module_from_spec(_memory_spec)
_memory_spec.loader.exec_module(_memory)
MemoryEvidence = _memory.MemoryEvidence
_spec = importlib.util.spec_from_file_location('spc_trace_reader', HERE / 'read_expedition_trace.py')
reader = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(reader)

SESSION_ROOT = ROOT / 'local/diagnostics/B205'
MAX_SEEN = 50000
MAX_HOURS = 12
MAX_HD_LOGGED = 2000
FIELD = re.compile(r'(\w+)=(\S+)')


def train_line(line):
    """Extract one TRAIN record from a snapshot ENTRY line or a passive print."""
    return reader.training_line(line)


def fields(record):
    return dict(FIELD.findall(record))


class Session:
    """Exclusive local files; the directory is fixed under ignored local/."""

    def __init__(self, root=SESSION_ROOT, stamp=None):
        if not root.absolute().is_relative_to(ROOT / 'local'):
            raise reader.CaptureError('LOG_DIRECTORY_INVALID')
        stamp = stamp or datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
        self.directory = root / ('session-' + stamp + '-' + secrets.token_hex(3))
        self.directory.mkdir(parents=True, exist_ok=False)
        if self.directory.resolve() != self.directory.absolute():
            raise reader.CaptureError('LOG_DIRECTORY_SYMLINK')
        self.events = (self.directory / 'events.jsonl').open('x', encoding='utf-8')
        self.records = (self.directory / 'records.log').open('x', encoding='utf-8')
        self.seen = OrderedDict()
        self.order = []
        self.stages = Counter()
        self.alerts = []
        self.last_population = {}
        self.cost_seen = set()
        self.contexts = set()
        self.hd = Counter()
        self.gate = Counter()
        self.gate_total = 0
        self.hd_total = 0
        self.hd_dropped = 0
        self.meta_counts = {}
        self.readiness = {}
        self.sink_alerted = False
        self.record_total = 0
        self.trace_epoch = None
        self.highest_sequence = 0
        self.memory = MemoryEvidence(self.directory, self.event)

    def event(self, kind, **values):
        self.events.write(json.dumps({'time_utc': datetime.now(timezone.utc).isoformat(),
                                      'event': kind, **values}, ensure_ascii=True) + '\n')
        self.events.flush()

    def add(self, record, source):
        """Return the console line for a new record, or None for a duplicate."""
        if record in self.seen:
            return None
        self.seen[record] = True
        if len(self.seen) > MAX_SEEN:
            self.seen.popitem(last=False)
        stamp = datetime.now(timezone.utc).strftime('%H:%M:%S')
        self.records.write(stamp + ' ' + source + ' ' + record + '\n')
        self.records.flush()
        f = fields(record)
        stage = f.get('stage', '?')
        if f.get('seq', '').isdigit():
            self.highest_sequence = max(self.highest_sequence, int(f['seq']))
        self.stages[stage] += 1
        self.record_total += 1
        if stage == 'TRACE_THROTTLED':
            self.alert('TRACE_THROTTLED role=%s turn=%s' % (f.get('traceRole', '?'), f.get('turn', '?')))
        if stage == 'READINESS_SUMMARY':
            state = self.readiness.setdefault(f.get('context', '?'), set())
            state.add(f.get('reason'))
            if f.get('sealed') == 'true' and f.get('loadSeen') == 'true' and f.get('notReady') not in (None, 'NONE'):
                self.alert('READINESS_NOT_READY context=%s modules=%s' % (f.get('context', '?'), f['notReady']))
        if 'context' in f:
            self.contexts.add(f['context'])
        if len(self.order) < MAX_SEEN:
            self.order.append(f)
        alerts = []
        city, pop = f.get('city'), f.get('population')
        if city and pop and pop.lstrip('-').isdigit():
            before = self.last_population.get(city)
            if before is not None and before != int(pop):
                alerts.append('POPULATION_CHANGE city=%s %s->%s stage=%s seq=%s turn=%s'
                              % (city, before, pop, stage, f.get('seq'), f.get('turn')))
            self.last_population[city] = int(pop)
        native, definition = f.get('nativeCost'), f.get('definitionCost')
        if native and definition and native.isdigit() and definition.isdigit() \
                and int(native) == 1 and int(definition) > 1 \
                and (native, definition) not in self.cost_seen:
            self.cost_seen.add((native, definition))
            # Definition is a base cost, not the next-copy/modified native price.
            # Flag the observed floor anomaly only; do not invent a cost formula.
            alerts.append('COST_FLOOR_OBSERVED native=%s definition_base=%s first_stage=%s seq=%s'
                          % (native, definition, stage, f.get('seq')))
        for text in alerts:
            self.alerts.append(text)
            self.event('alert', text=text)
        line = '%s %-18s T%s city=%s pop=%s base/nativeCost=%s/%s phase=%s' % (
            stamp, stage, f.get('turn', '?'), city or '-', pop or '-',
            definition or '?', native or '?', f.get('phase', '-'))
        return '\n'.join([line] + ['  !! ' + a for a in alerts])

    def alert(self, text):
        if text not in self.alerts:
            self.alerts.append(text)
            self.event('alert', text=text)

    def add_meta(self, line):
        # Keep bounded reader metadata in the evidence, never arbitrary engine output.
        stamp = datetime.now(timezone.utc).strftime('%H:%M:%S')
        self.records.write(stamp + ' meta ' + line + '\n')
        self.records.flush()
        f = fields(line)
        epoch, first = f.get('traceEpoch'), f.get('firstSequence', '')
        if epoch and epoch != 'UNKNOWN':
            if epoch != self.trace_epoch:
                self.trace_epoch = epoch
                self.highest_sequence = 0
                self.meta_counts = {}
            if first.isdigit() and int(first) > self.highest_sequence + 1:
                self.alert('TRACE_RING_GAP epoch=%s missing=%d..%d' % (epoch, self.highest_sequence + 1, int(first) - 1))
                self.event('capture_gap', code='TRACE_RING_GAP', phase='SNAPSHOT')
        for key in ('suppressed', 'errors', 'sampleSuppressed'):
            value = f.get(key, '')
            if value.isdigit():
                count = int(value)
                prior = self.meta_counts.get(key, 0)
                if count > prior:
                    self.alert('TRACE_META_%s count=%d previous=%d' % (key.upper(), count, prior))
                self.meta_counts[key] = count
        if f.get('sinkStatus') == 'BUDGET_STOP' and not self.sink_alerted:
            self.sink_alerted = True
            self.alert('TRACE_SINK_BUDGET_STOP native_error_channel_only')

    def add_hd(self, line):
        """HD prints repeat legitimately, so count each one; log a bounded prefix."""
        self.hd_total += 1
        text = line[len(reader.HD_PREFIX):]
        match = re.search(r' 人口变化 (-?\d+)$', text)
        self.hd['population_change ' + match.group(1) if match else 'hospital'] += 1
        if self.hd_total > MAX_HD_LOGGED:
            return None
        stamp = datetime.now(timezone.utc).strftime('%H:%M:%S')
        self.records.write(stamp + ' hd ' + line + '\n')
        self.records.flush()
        return stamp + ' HD ' + text if self.hd_total <= 20 else None

    def add_gate(self, line):
        """B212: Expedition Gate prints (dispatch/task/completion/return); counted, logged in order."""
        text = line[len(reader.GATE_PREFIX):]
        self.gate_total += 1
        kind = re.search(r'\[N1_([A-Z_]+)\]', text)
        detail = re.search(r'(?:action|mission|outcome|code|status|category)=([A-Za-z_]+)', text)
        self.gate[(kind.group(1) if kind else '?') + ':' + (detail.group(1) if detail else '?')] += 1
        if self.gate_total > MAX_HD_LOGGED:
            return None
        stamp = datetime.now(timezone.utc).strftime('%H:%M:%S')
        self.records.write(stamp + ' gate ' + text + '\n')
        self.records.flush()
        return stamp + ' GATE ' + text

    def summary(self, reason):
        for context, stages in self.readiness.items():
            if 'FIRST_PUBLISH' in stages and 'AFTER_LOAD' not in stages:
                self.alert('READINESS_LOAD_SAMPLE_MISSING context=' + context)
        lines = ['B205 trace session summary (read-only collection; not a gameplay PASS)',
                 'end_reason: ' + reason,
                 'unique_records: %d' % self.record_total,
                 'observer_contexts: %d' % len(self.contexts),
                 'stages: ' + ', '.join('%s=%d' % kv for kv in sorted(self.stages.items()))]
        lines.append('hd_prints: %d (dropped by reader: %d)' % (self.hd_total, self.hd_dropped))
        lines.extend(self.memory.summary())
        lines.append('gate_prints: %d' % self.gate_total)
        lines += ['gate: %s x%d' % kv for kv in sorted(self.gate.items())]
        lines += ['hd: %s x%d' % kv for kv in sorted(self.hd.items())]
        lines += ['alert: ' + text for text in self.alerts] or ['alerts: none']
        text = '\n'.join(lines) + '\n'
        (self.directory / 'summary.txt').write_text(text, encoding='utf-8')
        self.event('end', reason=reason, unique_records=self.record_total)
        return text

    def close(self):
        self.memory.close()
        self.events.close()
        self.records.close()


def run(session, capture=reader.capture, clock=time.monotonic, sleep=time.sleep,
        window=30, idle_exit=30, retry=5, max_seconds=MAX_HOURS * 3600, out=print):
    """Main loop. Returns the end reason. All injected callables ease offline tests."""
    start = clock()
    connected_once = False
    last_ok = None
    waiting_reported = False
    last_wait = None
    while True:
        now = clock()
        if now - start >= max_seconds:
            return 'MAX_DURATION'
        if connected_once:
            session.memory.sample_process()
        trace_errors = []
        listening = False
        try:
            def on_record(line):
                nonlocal listening, connected_once, last_ok, waiting_reported, last_wait
                record = train_line(line)
                if record:
                    shown = session.add(record, 'snap' if 'ENTRY ' in line else 'live')
                    if shown:
                        out(shown)
                elif line.startswith(reader.PREFIX + 'MEM_META '):
                    session.memory.add(fields(line), meta=True)
                elif line.startswith(reader.PREFIX + 'MEM '):
                    session.memory.add(fields(line))
                elif line.startswith(reader.PREFIX + 'MEM_UNAVAILABLE'):
                    session.memory.write('game_unavailable')
                elif line.startswith('[SPC][GC_TRIAL]'):
                    session.memory.write('gc_print', text=line)
                elif line.startswith(reader.PREFIX + 'META '):
                    session.add_meta(line)
                elif line.startswith(reader.GATE_PREFIX):
                    shown = session.add_gate(line)
                    if shown:
                        out(shown)
                elif line.startswith(reader.HD_PREFIX):
                    shown = session.add_hd(line)
                    if shown:
                        out(shown)
                elif line.startswith(reader.PREFIX + 'TRANSPORT '):
                    session.event('transport_window', **fields(line))
                elif line.startswith(reader.PREFIX + 'WINDOW_COMPLETE '):
                    session.event('capture_window', **fields(line))
                    dropped = fields(line).get('hd_dropped', '0')
                    session.hd_dropped += int(dropped) if dropped.isdigit() else 0
                elif line.startswith(reader.PREFIX + 'ERROR '):
                    session.event('trace_error', line=line)
                    code = line[len(reader.PREFIX + 'ERROR '):].split()
                    trace_errors.append(code[0] if code else 'TRACE_ERROR_INVALID')
                elif line.startswith(reader.PREFIX + 'LISTENING '):
                    # Transport success / DONE alone does not mean a valid trace.
                    listening = True
                    if not connected_once or waiting_reported:
                        out('Connected to the game; collecting. Press Ctrl-C to stop.')
                        session.event('connected')
                    connected_once, last_ok, waiting_reported, last_wait = True, clock(), False, None
            capture('record', on_record=on_record, record_seconds=min(window, 30))
            invalid = next((code for code in trace_errors if code != 'TRACE_UNAVAILABLE'), None)
            if invalid:
                out('Trace snapshot invalid (%s); collection stopped.' % invalid)
                session.event('trace_stopped', code=invalid)
                return invalid
            if trace_errors:
                # The reader returns ERROR + DONE normally when the ring is absent.
                # Treat it like a loading wait, not a successful passive window.
                if last_wait != ('TRACE_UNAVAILABLE', 'SNAPSHOT'):
                    session.event('waiting', code='TRACE_UNAVAILABLE', phase='SNAPSHOT')
                    last_wait = ('TRACE_UNAVAILABLE', 'SNAPSHOT')
                if not waiting_reported:
                    out('Waiting for the Expedition trace to become available...')
                    waiting_reported = True
                if connected_once:
                    last_ok = clock()  # The game answered; it has not exited.
                sleep(retry)
                continue
            if not listening:
                session.event('trace_stopped', code='CAPTURE_PROTOCOL_INVALID')
                out('Capture ended without a listening window; collection stopped.')
                return 'CAPTURE_PROTOCOL_INVALID'
            last_ok = clock()
        except reader.CaptureError as error:
            invalid = next((code for code in trace_errors if code != 'TRACE_UNAVAILABLE'), None)
            if invalid:
                session.event('capture_error', code=str(error), phase=error.phase)
                session.event('trace_stopped', code=invalid)
                out('Trace snapshot invalid (%s); collection stopped.' % invalid)
                return invalid
            code = str(error)
            # Refused: nothing listens, the game is gone or not started yet.
            # Closed/handshake timeout: the process is alive (e.g. loading a save).
            gone = code == 'SOCKET_UNAVAILABLE'
            loading = code == 'CONNECTION_CLOSED' or \
                (code == 'DEADLINE_EXCEEDED' and error.phase in ('CONNECT', 'CONTEXT'))
            unavailable = gone or loading
            if unavailable and (code, error.phase) != last_wait:
                session.event('waiting', code=code, phase=error.phase)
                last_wait = (code, error.phase)
            if loading and connected_once:
                last_ok = clock()
            if gone and connected_once and last_ok is not None and clock() - last_ok >= idle_exit:
                return 'GAME_EXITED'
            if unavailable and not waiting_reported:
                out('Waiting for the game / Tuner socket (localhost:4318)...')
                waiting_reported = True
            if not unavailable:
                session.event('capture_error', code=code, phase=error.phase)
                session.event('capture_gap', code=code, phase=error.phase)
            sleep(retry)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--window', type=int, default=30, help='passive window per connection, 5..600 s (default 30)')
    parser.add_argument('--idle-exit', type=int, default=30, help='stop after the game is gone this long, 10..3600 s (default 30)')
    parser.add_argument('--max-hours', type=float, default=MAX_HOURS, help='hard cap, 0.1..12 h (default 12)')
    args = parser.parse_args(argv)
    if not 5 <= args.window <= 600 or not 10 <= args.idle_exit <= 3600 or not 0.1 <= args.max_hours <= MAX_HOURS:
        parser.error('argument out of range')
    def stop(signum, frame):
        raise KeyboardInterrupt
    signal.signal(signal.SIGTERM, stop)
    session = Session()
    print('Session folder: ' + str(session.directory.relative_to(ROOT)), flush=True)
    session.event('start', window=args.window, idle_exit=args.idle_exit, max_hours=args.max_hours)
    reason = 'INTERRUPTED'
    try:
        reason = run(session, window=args.window, idle_exit=args.idle_exit,
                     max_seconds=args.max_hours * 3600, out=lambda s: print(s, flush=True))
    except KeyboardInterrupt:
        reason = 'INTERRUPTED'
    finally:
        print(session.summary(reason), flush=True)
        session.close()
    return 0 if reason in ('INTERRUPTED', 'GAME_EXITED', 'MAX_DURATION') else 1


if __name__ == '__main__':
    raise SystemExit(main())
