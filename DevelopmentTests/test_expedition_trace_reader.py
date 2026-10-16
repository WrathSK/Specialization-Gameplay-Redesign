"""B205 fixed tuner-reader transport tests; entirely offline, no game/socket."""
import importlib.util
from pathlib import Path
import re
import socket
import struct
import unittest
from unittest import mock

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent / 'tools/read_expedition_trace.py'
if not SOURCE.exists():
    SOURCE = HERE / 'read_expedition_trace.py'
spec = importlib.util.spec_from_file_location('expedition_trace_reader', SOURCE)
reader = importlib.util.module_from_spec(spec)
spec.loader.exec_module(reader)


def frame(tag, text):
    data = text if isinstance(text, bytes) else text.encode('utf-8')
    return struct.pack('<II', len(data), tag) + data


class FakeSocket:
    def __init__(self, initial=None, respond=True, result='PROBE turn=88 exposed=table spc=table', chunk=7):
        default = frame(4, b'12\0') + frame(4, b'3\0InGame\0' + b'70\0GameCore_Tuner\0')
        self.incoming = bytearray(default if initial is None else initial)
        self.respond = respond
        self.result = result
        self.chunk = chunk
        self.sent = []
        self.closed = False
        self.timeouts = []

    def settimeout(self, value):
        self.timeouts.append(value)

    def sendall(self, value):
        size, tag = struct.unpack('<II', value[:8])
        assert size == len(value) - 8
        text = value[8:].rstrip(b'\0').decode()
        self.sent.append((tag, text))
        if text.startswith('CMD:') and self.respond:
            marker = re.search(r"print\('([^']+)'\.\.s\)", text).group(1)
            sentinel = re.findall(r"print\('([^']+)'\)", text)[-1]
            self.incoming.extend(frame(0xFFFFFFFF, b'0\0secret engine output\0'))
            self.incoming.extend(frame(3, b'ACK\0'))
            self.incoming.extend(frame(0xFFFFFFFF, ('0\0GameCore_Tuner: ' + marker + self.result + '\0').encode()))
            self.incoming.extend(frame(0xFFFFFFFF, ('0\0GameCore_Tuner: ' + sentinel + '\0').encode()))

    def recv(self, count):
        if not self.incoming:
            raise socket.timeout()
        take = min(count, self.chunk, len(self.incoming))
        value = bytes(self.incoming[:take])
        del self.incoming[:take]
        return value

    def close(self):
        self.closed = True


class ReaderTests(unittest.TestCase):
    def run_capture(self, fake, mode='probe', clock=lambda: 1.0):
        connections = []
        def connect(address, timeout):
            connections.append((address, timeout))
            return fake
        try:
            return reader.capture(mode, connect=connect, clock=clock)
        finally:
            self.assertEqual(connections, [(('127.0.0.1', 4318), 5.0)])
            self.assertTrue(fake.closed)

    def test_fragmented_probe_context_from_lsq_and_filtered_output(self):
        fake = FakeSocket(chunk=1)
        output = self.run_capture(fake)
        self.assertEqual(output, [reader.PREFIX + 'PROBE turn=88 exposed=table spc=table', reader.PREFIX + 'DONE'])
        self.assertEqual(fake.sent[:2], [(4, 'APP:SPC_B205_ReadOnly'), (4, 'LSQ:')])
        self.assertTrue(fake.sent[2][1].startswith('CMD:70:'))
        self.assertTrue(all(0 < n <= 5 for n in fake.timeouts))

    def test_trace_fixed_schema_and_limits(self):
        fake = FakeSocket(result='META schema=205 sequence=3 suppressed=0 errors=0 sinkStatus=UNKNOWN')
        output = self.run_capture(fake, 'trace')
        command = fake.sent[2][1]
        self.assertIn("rawget(ExposedMembers,'SPC_B205TrainingTrace')", command)
        self.assertIn("rawget(t,'schema')~=205", command)
        self.assertIn('for i=1,64 do', command)
        self.assertIn('#line<=4096', command)
        self.assertIn('TRACE_ENTRIES_OVER_LIMIT', command)
        self.assertEqual(output[-1], reader.PREFIX + 'DONE')
        for forbidden in ('SetProperty', 'RequestOperation', 'SetPopulation', 'collectgarbage', 'os.', 'io.'):
            self.assertNotIn(forbidden, command)

    def test_ack_without_sentinel_is_failure(self):
        fake = FakeSocket(respond=False)
        with self.assertRaisesRegex(reader.CaptureError, 'DEADLINE_EXCEEDED'):
            self.run_capture(fake)

    def test_missing_context_never_sends_command(self):
        fake = FakeSocket(initial=frame(4, b'1\0OtherContext\0'))
        with self.assertRaises(reader.CaptureError):
            self.run_capture(fake)
        self.assertEqual(len(fake.sent), 2)

    def test_ambiguous_context_rejected(self):
        fake = FakeSocket(initial=frame(4, b'1\0GameCore_Tuner\0' + b'2\0GameCore_Tuner\0'))
        with self.assertRaisesRegex(reader.CaptureError, 'CONTEXT_AMBIGUOUS'):
            self.run_capture(fake)
        self.assertEqual(len(fake.sent), 2)

    def test_frame_limit_checked_before_payload(self):
        fake = FakeSocket(initial=struct.pack('<II', reader.MAX_FRAME + 1, 4))
        with self.assertRaisesRegex(reader.CaptureError, 'FRAME_BYTE_LIMIT'):
            self.run_capture(fake)

    def test_total_byte_limit(self):
        fake = FakeSocket(initial=frame(5, b'x' * reader.MAX_FRAME) * 5, chunk=reader.MAX_FRAME)
        with self.assertRaisesRegex(reader.CaptureError, 'TOTAL_BYTE_LIMIT'):
            self.run_capture(fake)

    def test_deadline_closes_connection(self):
        times = iter([0.0, 6.0])
        fake = FakeSocket()
        with self.assertRaisesRegex(reader.CaptureError, 'DEADLINE_EXCEEDED'):
            self.run_capture(fake, clock=lambda: next(times))

    def test_connection_error_does_not_echo_private_error(self):
        def fail(*args, **kwargs):
            raise OSError('private credentials or host path')
        with self.assertRaisesRegex(reader.CaptureError, '^SOCKET_UNAVAILABLE$'):
            reader.capture('probe', connect=fail)

    def test_end_of_stream_closes(self):
        fake = FakeSocket()
        fake.recv = lambda size: b''
        with self.assertRaisesRegex(reader.CaptureError, 'CONNECTION_CLOSED'):
            self.run_capture(fake)

    def test_output_line_limit(self):
        fake = FakeSocket(result='x' * 4201)
        with self.assertRaisesRegex(reader.CaptureError, 'OUTPUT_LINE_LIMIT'):
            self.run_capture(fake)

    def test_malformed_encoding_rejected_without_contents(self):
        fake = FakeSocket(initial=frame(4, b'\xff\0'))
        with self.assertRaisesRegex(reader.CaptureError, '^CONTEXT_ENCODING_INVALID$'):
            self.run_capture(fake)

    def test_invalid_mode_never_connects(self):
        def forbidden(*args, **kwargs):
            self.fail('invalid mode connected')
        with self.assertRaisesRegex(reader.CaptureError, 'MODE_INVALID'):
            reader.capture('arbitrary Lua', connect=forbidden)

    def test_trace_absence_is_nonzero_even_with_transport_done(self):
        import contextlib
        import io
        out = io.StringIO()
        with mock.patch.object(reader, 'capture', return_value=[reader.PREFIX + 'ERROR TRACE_UNAVAILABLE', reader.PREFIX + 'DONE']), contextlib.redirect_stdout(out):
            self.assertEqual(reader.main(['trace']), 1)
        self.assertIn('TRACE_UNAVAILABLE', out.getvalue())

    def test_output_record_limit(self):
        fake = FakeSocket(result='x')
        original = fake.sendall
        def flood(value):
            original(value)
            text = value[8:].rstrip(b'\0').decode()
            if text.startswith('CMD:'):
                marker = re.search(r"print\('([^']+)'\.\.s\)", text).group(1)
                fake.incoming = bytearray(frame(0xFFFFFFFF, ('0\0' + marker + 'ENTRY 1 x\0').encode()) * 71)
        fake.sendall = flood
        with self.assertRaisesRegex(reader.CaptureError, 'OUTPUT_RECORD_LIMIT'):
            self.run_capture(fake)

    def test_cli_has_no_host_lua_or_watch_override(self):
        import contextlib
        import io
        for args in (['probe', '--host', 'example.com'], ['--lua', 'print(1)'], ['trace', '--watch']):
            with self.subTest(args=args), contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
                reader.main(args)


if __name__ == '__main__':
    unittest.main()
