#!/usr/bin/env python3
"""One-shot, fixed read-only B205 FireTuner queries; stdout is local evidence.

Protocol reference (independently implemented, no copied client code):
https://github.com/PatrickJYKang/civ6-logger/blob/main/docs/ARCHITECTURE.md
Only 127.0.0.1:4318 and the advertised GameCore_Tuner context are accepted.
No arbitrary Lua, configuration changes, file writes, watchers or retries.
Native probe success does not establish trace availability in every context.
"""
import argparse
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
PREFIX = '[SPC][B205][READ] '


class CaptureError(RuntimeError):
    """Fixed error labels only: do not echo arbitrary native output."""


class Transport:
    def __init__(self, connection, deadline, clock=time.monotonic):
        self.connection = connection
        self.deadline = deadline
        self.clock = clock
        self.total = 0

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
            if self.total > MAX_TOTAL:
                raise CaptureError('TOTAL_BYTE_LIMIT')
            parts.append(data)
            left -= len(data)
        return b''.join(parts)

    def frame(self):
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
        return None  # APP reply, not the state list.
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
    # Both interpolated tokens are generated locally, not accepted from CLI.
    common = "local function out(s) print('" + marker + "'..s) end; "
    if mode == 'probe':
        body = "local turn=Game and Game.GetCurrentGameTurn and Game.GetCurrentGameTurn(); " \
               "out('PROBE turn='..tostring(type(turn)=='number' and turn or 'UNKNOWN')" \
               "..' exposed='..type(ExposedMembers)..' spc='" \
               "..type(type(ExposedMembers)=='table' and rawget(ExposedMembers,'SPC_P0') or nil)); "
    elif mode == 'trace':
        body = """local t=type(ExposedMembers)=='table' and rawget(ExposedMembers,'SPC_B205TrainingTrace');
local function scalar(v)
 if type(v)=='number' or type(v)=='boolean' then return tostring(v) end
 if type(v)=='string' then return (v:sub(1,80):gsub('%c','_')) end
 return 'UNKNOWN'
end;
if type(t)~='table' then out('ERROR TRACE_UNAVAILABLE')
elseif rawget(t,'schema')~=205 then out('ERROR TRACE_SCHEMA_INVALID')
else
 out('META schema=205 sequence='..scalar(rawget(t,'sequence'))..' suppressed='..scalar(rawget(t,'suppressed'))..' errors='..scalar(rawget(t,'errors'))..' sinkStatus='..scalar(rawget(t,'sinkStatus')));
 local entries=rawget(t,'entries');
 if type(entries)~='table' then out('ERROR TRACE_ENTRIES_INVALID')
 else
  for i=1,64 do
   local e=rawget(entries,i); if e==nil then break end;
   local line=type(e)=='table' and rawget(e,'line');
   if type(line)=='string' and #line<=4096 then out('ENTRY '..i..' '..line:gsub('%c','_'))
   else out('ERROR TRACE_ENTRY_INVALID '..i) end
  end;
  if rawget(entries,65)~=nil then out('ERROR TRACE_ENTRIES_OVER_LIMIT') end
 end
end; """
    else:
        raise CaptureError('MODE_INVALID')
    return common + body + "print('" + sentinel + "')"


def output_text(payload):
    # Output frames are channel NUL text NUL. Never emit other engine messages.
    fields = payload.split(b'\0')
    if len(fields) < 2:
        return ''
    try:
        return fields[1].decode('utf-8')
    except UnicodeDecodeError:
        return ''


def capture(mode, connect=socket.create_connection, clock=time.monotonic):
    if mode not in ('probe', 'trace'):
        raise CaptureError('MODE_INVALID')
    nonce = secrets.token_hex(12)
    marker = PREFIX + nonce + ' '
    sentinel = PREFIX + nonce + ' DONE'
    deadline = clock() + DEADLINE_SECONDS
    connection = None
    try:
        connection = connect(ADDRESS, timeout=DEADLINE_SECONDS)
        wire = Transport(connection, deadline, clock)
        wire.send(4, 'APP:SPC_B205_ReadOnly')
        wire.send(4, 'LSQ:')
        context = None
        while context is None:
            tag, payload = wire.frame()
            if tag == 4:
                context = select_context(payload)
        wire.send(3, 'CMD:' + str(context) + ':' + command(mode, marker, sentinel))
        records = []
        while True:
            tag, payload = wire.frame()
            if tag != 0xFFFFFFFF:
                continue  # An ACK alone is not a successful capture.
            for line in output_text(payload).splitlines():
                # The engine may prepend the context name to each print.
                pos = line.find(marker)
                if pos < 0:
                    continue
                item = line[pos:]
                if item == sentinel:
                    records.append(PREFIX + 'DONE')
                    return records
                if len(item) > len(marker) + 4200:
                    raise CaptureError('OUTPUT_LINE_LIMIT')
                if len(records) >= MAX_RECORDS:
                    raise CaptureError('OUTPUT_RECORD_LIMIT')
                records.append(PREFIX + item[len(marker):])
    except (socket.timeout, TimeoutError):
        raise CaptureError('DEADLINE_EXCEEDED') from None
    except OSError:
        raise CaptureError('SOCKET_UNAVAILABLE') from None
    finally:
        if connection is not None:
            connection.close()


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('mode', choices=('probe', 'trace'))
    args = parser.parse_args(argv)
    try:
        records = capture(args.mode)
    except CaptureError as error:
        print(PREFIX + 'ERROR ' + str(error), file=sys.stderr)
        return 1
    for line in records:
        print(line)
    return int(any(line.startswith(PREFIX + 'ERROR ') for line in records))


if __name__ == '__main__':
    raise SystemExit(main())
