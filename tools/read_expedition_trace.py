#!/usr/bin/env python3
"""Fixed read-only B205 FireTuner reader and bounded local JSONL recorder.

Protocol reference: https://github.com/PatrickJYKang/civ6-logger/blob/main/docs/ARCHITECTURE.md
Only localhost4318 / advertised GameCore_Tuner; no arbitrary Lua or config writes.
Record sends one snapshot query, then passively receives B205 diagnostic prints
and (B206) a fixed allowlist of HD population/hospital prints, capped per window.
It never polls, reconnects, trains, changes Properties, launches the game or runs GC.
"""
import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import re
import secrets
import socket
import struct
import sys
import time

ADDRESS = ('127.0.0.1', 4318)
DEADLINE_SECONDS = 5.0
MAX_FRAME = 262144
MAX_TOTAL = 1048576
MAX_RECORDS = 70
MAX_RECORD_SECONDS = 600
MAX_STREAM_TOTAL = 4 * 1048576
MAX_STREAM_RECORDS = 1024
MAX_HD_RECORDS = 200  # B206: per passive window; the remainder is only counted
HD_PREFIX = '[SPC][B206][HD] '
# B206: fixed allowlist of HD population/hospital print shapes (game text only).
HD_PATTERNS = (re.compile(r'\S{1,40} 人口变化 -?\d{1,6}$'), re.compile(r'中心医院 [^\x00-\x1f]{1,120}$'))
GATE_PREFIX = '[SPC][B212][GATE] '
# B212: the Expedition Gate's own fixed-format action/task prints (dispatch, task, completion, return).
GATE_PATTERN = re.compile(r'\[SPC\]\[B191\]\[N1_(?:SPY|SPY_ERROR|SPY_REQUEST|TASK)\] [^\x00-\x1f]{1,400}$')
MAX_FRAMES = 4096
PREFIX = '[SPC][B205][READ] '
TRAIN_PREFIX = '[SPC][B205][TRAIN] '
LOG_DIR = Path(__file__).resolve().parents[1] / 'local/diagnostics/B205'


class CaptureError(RuntimeError):
    """Safe labels plus bounded partial evidence, never arbitrary engine errors."""
    def __init__(self, label, phase='CONNECT', records=()):
        super().__init__(label)
        self.phase = phase
        self.records = tuple(records)


class Transport:
    def __init__(self, connection, deadline, clock=time.monotonic, limit=MAX_TOTAL):
        self.connection, self.deadline, self.clock = connection, deadline, clock
        self.total, self.frames, self.limit = 0, 0, limit

    def remaining(self):
        value = self.deadline - self.clock()
        if value <= 0:
            raise CaptureError('DEADLINE_EXCEEDED')
        self.connection.settimeout(value)

    def send(self, tag, text):
        data = text.encode('utf-8') + b'\0'
        if len(data) > MAX_FRAME:
            raise CaptureError('COMMAND_TOO_LARGE')
        self.remaining()
        self.connection.sendall(struct.pack('<II', len(data), tag) + data)

    def exact(self, size):
        parts = []
        left = size
        while left:
            self.remaining()
            data = self.connection.recv(left)
            if not data:
                raise CaptureError('CONNECTION_CLOSED')
            self.total += len(data)
            if self.total > self.limit:
                raise CaptureError('TOTAL_BYTE_LIMIT')
            parts.append(data)
            left -= len(data)
        return b''.join(parts)

    def frame(self):
        self.frames += 1
        if self.frames > MAX_FRAMES:
            raise CaptureError('FRAME_COUNT_LIMIT')
        size, tag = struct.unpack('<II', self.exact(8))
        if size > MAX_FRAME:
            raise CaptureError('FRAME_BYTE_LIMIT')
        return tag, self.exact(size)


def select_context(payload):
    """A valid LSQ list contains integer-index / exact-name pairs."""
    try:
        fields = payload.decode('utf-8').rstrip('\0').split('\0')
    except UnicodeDecodeError:
        raise CaptureError('CONTEXT_ENCODING_INVALID') from None
    if len(fields) < 2 or len(fields) % 2:
        return None
    matches = []
    for i in range(0, len(fields), 2):
        index, name = fields[i:i + 2]
        if not index.isascii() or not index.isdigit() or len(index) > 6:
            return None
        if name == 'GameCore_Tuner':
            matches.append(int(index))
    if len(matches) > 1:
        raise CaptureError('CONTEXT_AMBIGUOUS')
    return matches[0] if matches else None


def command(mode, marker, sentinel):
    # Actual Mac GameCore_Tuner has no rawget. Ordinary table reads were observed.
    common = "local function out(s) print('" + marker + "'..s) end; "
    if mode == 'probe':
        body = "local turn=Game and Game.GetCurrentGameTurn and Game.GetCurrentGameTurn(); " \
               "out('PROBE turn='..tostring(type(turn)=='number' and turn or 'UNKNOWN')" \
               "..' exposed='..type(ExposedMembers)..' spc='" \
               "..type(type(ExposedMembers)=='table' and ExposedMembers.SPC_P0 or nil)); "
    elif mode == 'trace':
        body = """local t=type(ExposedMembers)=='table' and ExposedMembers.SPC_B205TrainingTrace;
local function scalar(v)
 if type(v)=='number' or type(v)=='boolean' then return tostring(v) end
 if type(v)=='string' then return (v:sub(1,80):gsub('%c','_')) end
 return 'UNKNOWN'
end;
if type(t)~='table' then out('ERROR TRACE_UNAVAILABLE')
elseif t.schema~=205 then out('ERROR TRACE_SCHEMA_INVALID')
else
 out('META schema=205 sequence='..scalar(t.sequence)..' suppressed='..scalar(t.suppressed)..' errors='..scalar(t.errors)..' sinkStatus='..scalar(t.sinkStatus));
 local entries=t.entries;
 if type(entries)~='table' then out('ERROR TRACE_ENTRIES_INVALID')
 else
  local gap=false;
  for i=1,64 do
   local e=entries[i];
   if e==nil then gap=true
   else
    if gap then out('ERROR TRACE_ENTRIES_SPARSE'); break end;
    local line=type(e)=='table' and e.line;
    if type(line)=='string' and #line<=4096 then out('ENTRY '..i..' '..line:gsub('%c','_'))
    else out('ERROR TRACE_ENTRY_INVALID '..i) end
   end
  end;
  if entries[65]~=nil then out('ERROR TRACE_ENTRIES_OVER_LIMIT') end
 end
end; """
    else:
        raise CaptureError('MODE_INVALID')
    return common + body + "print('" + sentinel + "')"


def output_text(payload):
    fields = payload.split(b'\0')
    if len(fields) < 2:
        return ''
    try:
        return fields[1].decode('utf-8')
    except UnicodeDecodeError:
        return ''


def native_error(payload):
    if not payload.startswith(b'ERR:'):
        return None
    if b'function expected instead of nil' in payload or b'attempt to call' in payload:
        return 'NATIVE_FUNCTION_UNAVAILABLE'
    return 'NATIVE_COMMAND_ERROR'


def training_line(line):
    # An exact batch/stage prefix; other engine output is dropped except hd_line().
    match = re.search(r'\[SPC\]\[B205\]\[TRAIN\] seq=\d+ stage=[A-Z_]+(?: |$)', line)
    if not match:
        return None
    value = line[match.start():]
    if len(value) > 4096:
        raise CaptureError('OUTPUT_LINE_LIMIT')
    return value


def hd_line(line):
    """Return one allowlisted HD population print or Expedition Gate print, or None."""
    match = GATE_PATTERN.search(line.rstrip())
    if match:
        return GATE_PREFIX + match.group(0)
    for pattern in HD_PATTERNS:
        match = pattern.search(line.rstrip())
        if match:
            return HD_PREFIX + match.group(0)
    return None


def capture(mode, connect=socket.create_connection, clock=time.monotonic,
            on_record=None, record_seconds=120):
    if mode not in ('probe', 'trace', 'record'):
        raise CaptureError('MODE_INVALID')
    if mode == 'record' and not 1 <= record_seconds <= MAX_RECORD_SECONDS:
        raise CaptureError('DURATION_INVALID')
    marker = PREFIX + secrets.token_hex(12) + ' '
    sentinel = marker + 'DONE'
    deadline = clock() + DEADLINE_SECONDS
    connection = None
    records, phase, passive_count = [], 'CONNECT', 0
    hd_count = hd_dropped = 0
    has_trace_error = False

    def emit(line):
        if on_record:
            try:
                on_record(line)
            except OSError:
                raise CaptureError('LOG_WRITE_FAILED') from None

    try:
        connection = connect(ADDRESS, timeout=DEADLINE_SECONDS)
        wire = Transport(connection, deadline, clock,
                         MAX_STREAM_TOTAL if mode == 'record' else MAX_TOTAL)
        wire.send(4, 'APP:SPC_B205_ReadOnly')
        wire.send(4, 'LSQ:')
        phase, context = 'CONTEXT', None
        while context is None:
            tag, payload = wire.frame()
            if tag == 4:
                context = select_context(payload)
        phase = 'SNAPSHOT'
        wire.send(3, 'CMD:' + str(context) + ':' + command('trace' if mode == 'record' else mode, marker, sentinel))
        while True:
            before = wire.total
            try:
                tag, payload = wire.frame()
            except (socket.timeout, TimeoutError, CaptureError) as error:
                expired = isinstance(error, (socket.timeout, TimeoutError)) or str(error) == 'DEADLINE_EXCEEDED'
                if phase == 'PASSIVE' and expired and clock() >= wire.deadline:
                    if wire.total != before:
                        raise CaptureError('PARTIAL_FRAME_AT_DEADLINE') from None
                    emit(PREFIX + 'WINDOW_COMPLETE passive_records=' + str(passive_count)
                         + ' hd_records=' + str(hd_count) + ' hd_dropped=' + str(hd_dropped))
                    return records
                raise
            if tag == 3:
                error = native_error(payload)
                if error:
                    raise CaptureError(error)
            if tag != 0xFFFFFFFF:
                continue
            for line in output_text(payload).splitlines():
                pos = line.find(marker)
                if phase == 'SNAPSHOT' and pos >= 0:
                    item = line[pos:]
                    if len(item) > len(marker) + 4200:
                        raise CaptureError('OUTPUT_LINE_LIMIT')
                    if len(records) >= MAX_RECORDS:
                        raise CaptureError('OUTPUT_RECORD_LIMIT')
                    value = PREFIX + item[len(marker):]
                    records.append(value)
                    emit(value)  # Flush before waiting for the next frame/sentinel.
                    has_trace_error |= value.startswith(PREFIX + 'ERROR ')
                    if item == sentinel:
                        if mode != 'record' or has_trace_error:
                            return records
                        phase = 'PASSIVE'
                        wire.deadline = clock() + record_seconds
                        emit(PREFIX + 'LISTENING seconds=' + str(record_seconds))
                elif mode == 'record':
                    value = training_line(line)
                    if value:
                        if passive_count >= MAX_STREAM_RECORDS:
                            raise CaptureError('OUTPUT_RECORD_LIMIT')
                        passive_count += 1
                        emit(value)  # Do not retain a growing list of passive output.
                    else:
                        value = hd_line(line)
                        if value and hd_count < MAX_HD_RECORDS:
                            hd_count += 1
                            emit(value)
                        elif value:
                            hd_dropped += 1
    except CaptureError as error:
        error.phase, error.records = phase, tuple(records)
        raise
    except (socket.timeout, TimeoutError):
        raise CaptureError('DEADLINE_EXCEEDED', phase, records) from None
    except OSError:
        raise CaptureError('SOCKET_UNAVAILABLE', phase, records) from None
    finally:
        if connection is not None:
            connection.close()


class LocalLog:
    """Exclusive, line-flushed local evidence. Directory is never user supplied."""
    def __init__(self):
        root = Path(__file__).resolve().parents[1]
        directory = LOG_DIR
        if directory.resolve() != directory.absolute():
            raise CaptureError('LOG_DIRECTORY_SYMLINK')
        if not directory.is_relative_to(root / 'local'):
            raise CaptureError('LOG_DIRECTORY_INVALID')
        directory.mkdir(parents=True, exist_ok=True)
        name = 'tuner-' + datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ-') + secrets.token_hex(4) + '.jsonl'
        self.path = directory / name
        self.file = self.path.open('x', encoding='utf-8')

    def write(self, event, **values):
        self.file.write(json.dumps({'time_utc': datetime.now(timezone.utc).isoformat(),
                                    'event': event, **values}, ensure_ascii=True) + '\n')
        self.file.flush()

    def close(self):
        self.file.close()


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('mode', choices=('probe', 'trace', 'record'))
    parser.add_argument('--seconds', type=int, default=120, help='record window, 1..600 seconds (default120)')
    args = parser.parse_args(argv)
    if not 1 <= args.seconds <= MAX_RECORD_SECONDS:
        parser.error('--seconds must be 1..600')
    log = None
    status = 1
    try:
        log = LocalLog()  # Every attempt gets a log, including connection failure.
        print('Local log: ' + str(log.path), flush=True)
        log.write('start', mode=args.mode, seconds=args.seconds if args.mode == 'record' else None)
        def output(line):
            log.write('record', line=line)
            if args.mode != 'record' or line.startswith(PREFIX + 'LISTENING'):
                print(line, flush=True)
        records = capture(args.mode, on_record=output, record_seconds=args.seconds)
        failed = any(line.startswith(PREFIX + 'ERROR ') for line in records)
        log.write('end', result='TRACE_ERROR' if failed else 'COLLECTION_COMPLETE',
                  note='Collection is not gameplay PASS; quiet window does not prove passive delivery.')
        status = int(failed)
    except CaptureError as error:
        if log:
            try:
                log.write('error', code=str(error), phase=error.phase)
            except OSError:
                pass
        print(PREFIX + 'ERROR ' + str(error) + ' phase=' + error.phase, file=sys.stderr)
        status = 1
    except KeyboardInterrupt:
        if log:
            try:
                log.write('end', result='INTERRUPTED')
            except OSError:
                pass
        status = 130
    except OSError:
        print(PREFIX + 'ERROR LOCAL_LOG_IO', file=sys.stderr)
        status = 1
    finally:
        if log:
            try:
                log.close()
            except OSError:
                print(PREFIX + 'ERROR LOCAL_LOG_CLOSE', file=sys.stderr)
                status = 1
    return status


if __name__ == '__main__':
    raise SystemExit(main())
