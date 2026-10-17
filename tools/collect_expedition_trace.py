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
_spec = importlib.util.spec_from_file_location('spc_trace_reader', HERE / 'read_expedition_trace.py')
reader = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(reader)

SESSION_ROOT = ROOT / 'local/diagnostics/B205'
MAX_SEEN = 50000
MAX_HOURS = 12
MAX_HD_LOGGED = 2000
FIELD = re.compile(r'(\w+)=(\S+)')
TRAIN = re.compile(r'\[SPC\]\[B205\]\[TRAIN\] seq=\d+ stage=[A-Z_]+(?: .*|$)')


def train_line(line):
    """Extract one TRAIN record from a snapshot ENTRY line or a passive print."""
    match = TRAIN.search(line)
    return match.group(0)[:4096] if match else None


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
        self.stages[stage] += 1
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
                and native != definition and (native, definition) not in self.cost_seen:
            self.cost_seen.add((native, definition))
            alerts.append('COST_MISMATCH native=%s definition=%s first_stage=%s seq=%s'
                          % (native, definition, stage, f.get('seq')))
        for text in alerts:
            self.alerts.append(text)
            self.event('alert', text=text)
        line = '%s %-18s T%s city=%s pop=%s cost=%s/%s phase=%s' % (
            stamp, stage, f.get('turn', '?'), city or '-', pop or '-',
            definition or '?', native or '?', f.get('phase', '-'))
        return '\n'.join([line] + ['  !! ' + a for a in alerts])

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
        detail = re.search(r'(?:action|mission|outcome|code)=([A-Za-z_]+)', text)
        self.gate[(kind.group(1) if kind else '?') + ':' + (detail.group(1) if detail else '?')] += 1
        if self.gate_total > MAX_HD_LOGGED:
            return None
        stamp = datetime.now(timezone.utc).strftime('%H:%M:%S')
        self.records.write(stamp + ' gate ' + text + '\n')
        self.records.flush()
        return stamp + ' GATE ' + text

    def summary(self, reason):
        lines = ['B205 trace session summary (read-only collection; not a gameplay PASS)',
                 'end_reason: ' + reason,
                 'unique_records: %d' % len(self.seen),
                 'observer_contexts: %d' % len(self.contexts),
                 'stages: ' + ', '.join('%s=%d' % kv for kv in sorted(self.stages.items()))]
        lines.append('hd_prints: %d (dropped by reader: %d)' % (self.hd_total, self.hd_dropped))
        lines.append('gate_prints: %d' % self.gate_total)
        lines += ['gate: %s x%d' % kv for kv in sorted(self.gate.items())]
        lines += ['hd: %s x%d' % kv for kv in sorted(self.hd.items())]
        lines += ['alert: ' + text for text in self.alerts] or ['alerts: none']
        text = '\n'.join(lines) + '\n'
        (self.directory / 'summary.txt').write_text(text, encoding='utf-8')
        self.event('end', reason=reason, unique_records=len(self.seen))
        return text

    def close(self):
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
        try:
            def on_record(line):
                record = train_line(line)
                if record:
                    shown = session.add(record, 'snap' if 'ENTRY ' in line else 'live')
                    if shown:
                        out(shown)
                elif line.startswith(reader.GATE_PREFIX):
                    shown = session.add_gate(line)
                    if shown:
                        out(shown)
                elif line.startswith(reader.HD_PREFIX):
                    shown = session.add_hd(line)
                    if shown:
                        out(shown)
                elif line.startswith(reader.PREFIX + 'WINDOW_COMPLETE '):
                    dropped = fields(line).get('hd_dropped', '0')
                    session.hd_dropped += int(dropped) if dropped.isdigit() else 0
                elif line.startswith(reader.PREFIX + 'ERROR '):
                    session.event('trace_error', line=line)
            capture('record', on_record=on_record, record_seconds=window)
            if not connected_once:
                out('Connected to the game; collecting. Press Ctrl-C to stop.')
                session.event('connected')
            connected_once, last_ok, waiting_reported, last_wait = True, clock(), False, None
        except reader.CaptureError as error:
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
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
