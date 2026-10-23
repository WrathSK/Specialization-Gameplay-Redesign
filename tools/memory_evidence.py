"""B269 passive memory evidence. No game mutations or automatic profiling tools."""
from datetime import datetime, timezone
import importlib.util
import json
import time
from pathlib import Path

CAP = 16 * 1024 * 1024


class MemoryEvidence:
    def __init__(self, directory, event, clock=time.monotonic):
        self.file = (directory / 'memory.jsonl').open('x', encoding='utf-8')
        self.event, self.clock = event, clock
        self.bytes = 0
        self.stopped = False
        self.next_sample = 0
        self.reader = self.native = self.identity = self.latest = None
        self.os_disabled = False
        self.epoch = None
        self.highest = 0
        self.segments = 0
        self.first_heap = self.last_heap = None
        self.first_process = self.last_process = None
        self.work = {}
        self.latest_work = {}
        self.work_phase = self.work_turn = None
        self.heap_quality = 'OK'
        self.gc_rows = self.rows = 0
        self.gc_completed = 0
        self.gc_freed = self.gc_max_cpu = 0.0
        self.gc_last_reason = "UNKNOWN"

    def write(self, kind, **fields):
        if self.stopped:
            return
        row = dict(time_utc=datetime.now(timezone.utc).isoformat(), kind=kind, **fields)
        text = json.dumps(row, ensure_ascii=True) + '\n'
        size = len(text.encode())
        if self.bytes + size > CAP:
            self.stopped = True
            self.event('memory_limit', code='MEMORY_FILE_CAP')
            return
        self.file.write(text)
        self.file.flush()
        self.bytes += size

    def sample_process(self):
        now = self.clock()
        if self.os_disabled or now < self.next_sample or self.stopped:
            return
        self.next_sample = now + 30
        try:
            if self.native is None:
                path = Path(__file__).parent / 'external_monitor/monitor.py'
                spec = importlib.util.spec_from_file_location('spc_memory_os', path)
                self.native = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(self.native)
                self.reader = self.native.MacReader()
            if self.identity is None:
                self.identity = self.reader.identity(self.native.find_game())
                if self.identity['name'] != 'Civ6_Exe_Child':
                    raise ValueError('PROCESS_NAME')
                self.write('process_start', identity=self.identity)
            values = self.reader.sample(self.identity)
            self.latest = (now, values)
            footprint = values['physical_footprint_bytes']
            if footprint != '':
                if self.first_process is None:
                    self.first_process = footprint
                self.last_process = footprint
            self.write('process', identity=self.identity, load_epoch=self.epoch,
                       sampling_scope='CONNECTED_WINDOW', **values)
        except Exception as exc:
            # No retry storm or automatic escalation. Trace collection continues.
            self.os_disabled = True
            self.latest = None
            self.write('process_unavailable', code=type(exc).__name__)
            self.event('memory_process_unavailable', code=type(exc).__name__)

    def add(self, fields, meta=False):
        epoch = fields.get('epoch')
        if not epoch or epoch == 'UNKNOWN':
            return
        if epoch != self.epoch:
            self.segments += 1
            if self.segments > 128:
                self.stopped = True
                self.event('memory_limit', code='MEMORY_SEGMENT_CAP')
                return
            self.epoch, self.highest, self.work = epoch, 0, {}
            self.first_heap = self.last_heap = None
            self.latest_work = {}; self.work_phase = self.work_turn = None
            self.heap_quality = 'OK'
            self.write('load_segment', epoch=epoch)
        if meta:
            first = fields.get('first', '')
            if first.isdigit() and int(first) > self.highest + 1:
                self.write('gap', epoch=epoch, missing_from=self.highest + 1, missing_to=int(first)-1)
            return
        seq = fields.get('seq', '')
        if not seq.isdigit() or int(seq) <= self.highest:
            return
        seq = int(seq)
        if seq > self.highest + 1:
            self.write('gap', epoch=epoch, missing_from=self.highest + 1, missing_to=seq-1)
        self.highest = seq
        self.rows += 1
        deltas = {}
        if fields.get('kind') in ('TURN_BEGIN', 'TURN_END', 'LOAD'):
            self.latest_work = {k: int(v) for k, v in fields.items() if k.startswith('work_') and v.isdigit()}
            self.work_phase, self.work_turn = fields.get('kind'), fields.get('turn')
        if fields.get('kind') == 'TURN_END':
            for key, value in fields.items():
                if key.startswith('work_') and value.isdigit():
                    n = int(value)
                    if key in self.work and n >= self.work[key]:
                        deltas[key] = n - self.work[key]
                    self.work[key] = n
        status = fields.get('heapStatus', 'LEGACY')
        if status not in ('OK', 'LEGACY') or fields.get('heapMiB') == 'UNKNOWN':
            self.heap_quality = 'UNTRUSTED:' + status
        try:
            heap = float(fields.get('heapMiB', ''))
            if self.heap_quality == 'OK' and 0 <= heap < float('inf'):
                if self.first_heap is None:
                    self.first_heap = heap
                self.last_heap = heap
        except ValueError:
            pass
        if fields.get('kind') == 'GC':
            self.gc_rows += 1
            self.gc_last_reason = fields.get('reason', 'UNKNOWN')
            try:
                before, after, cpu = (float(fields.get(k, '')) for k in ('before', 'after', 'cpu'))
                if all(0 <= x < float('inf') for x in (before, after, cpu)):
                    self.gc_completed += 1
                    self.gc_freed += before-after
                    self.gc_max_cpu = max(self.gc_max_cpu, cpu)
            except ValueError:
                pass
        # Receipt time is not event time. No inferred per-turn process delta.
        self.write('game', evidence=fields, work_since_previous_end=deltas,
                   process_sample_age_seconds=round(self.clock()-self.latest[0], 3) if self.latest else None,
                   association='RECEIPT_TIME_ONLY', identity=self.identity)

    def summary(self):
        delta = None if self.first_process is None else self.last_process-self.first_process
        return ['memory_rows: %d; gc_records: %d; load_segments: %d' % (self.rows, self.gc_rows, self.segments),
                'process_footprint_delta_bytes_same_identity: %s' % delta,
                'last_load_gameplay_heap_MiB_first_last: %s / %s' % (self.first_heap, self.last_heap if self.heap_quality == 'OK' else 'UNTRUSTED'),
                'last_load_gameplay_heap_quality: %s; raw/status retained; positive count alone cannot exclude native wrap' % self.heap_quality,
                'process_sampling_scope: confirmed connected windows only; load/unload transitions may still be present',
                'observed_gc_results: %d; net_freed_MiB: %.2f; max_cpu_seconds: %.3f; last_reason: %s' % (self.gc_completed, self.gc_freed, self.gc_max_cpu, self.gc_last_reason),
                'last_load_observed_work_totals: %s' % self.latest_work,
                'last_load_observed_work_boundary: T%s %s' % (self.work_turn, self.work_phase),
                'memory_scope: Gameplay call-site, not Mod-exclusive/all Lua; process correlation uses receipt time only',
                'memory_root_cause: UNKNOWN; native validation required']

    def close(self):
        self.file.close()
