"""B205 reader/recorder tests; offline fake transport and Lupa, no live socket."""
import importlib.util
from pathlib import Path
import re
import socket
import struct
import unittest
import tempfile
import contextlib
import io
import json
from lupa import LuaRuntime
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
        self.assertIn("ExposedMembers.SPC_B205TrainingTrace", command)
        self.assertNotIn("rawget(", command)
        self.assertIn("t.schema~=205", command)
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
        out = io.StringIO()
        with temporary_log(), mock.patch.object(reader, 'capture', side_effect=emit_missing_trace):
            with contextlib.redirect_stdout(out):
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


@contextlib.contextmanager
def temporary_log():
    with tempfile.TemporaryDirectory() as tmp:
        root=Path(tmp).resolve()
        with mock.patch.object(reader,'__file__',str(root/'tools/reader.py')),mock.patch.object(reader,'LOG_DIR',root/'local/diagnostics/B205'):
            yield root

def emit_missing_trace(*args,**kwargs):
    rows=[reader.PREFIX+'ERROR TRACE_UNAVAILABLE',reader.PREFIX+'DONE']
    for row in rows:kwargs['on_record'](row)
    return rows

class RecorderTests(unittest.TestCase):
    def capture(self,fake,mode='record',**kwargs):
        try:return reader.capture(mode,connect=lambda *a,**k:fake,**kwargs)
        finally:self.assertTrue(fake.closed)

    def fixture(self,extra=b''):
        fake=FakeSocket(chunk=20000);now=[0.0];send0,recv0=fake.sendall,fake.recv
        def send(value):
            send0(value)
            if value[8:].startswith(b'CMD:'):fake.incoming.extend(extra)
        def recv(size):
            if not fake.incoming:now[0]=2.0;raise socket.timeout()
            return recv0(size)
        fake.sendall,fake.recv=send,recv
        return fake,lambda:now[0]

    def test_partial_native_error_flushed_and_safe(self):
        fake=FakeSocket();old=fake.sendall;seen=[]
        def send(value):
            old(value)
            if value[8:].startswith(b'CMD:'):
                marker=re.search(r"print\('([^']+)'\.\.s\)",value[8:].decode()).group(1)
                fake.incoming=bytearray(frame(0xffffffff,'0\0'+marker+'ENTRY 1 safe\0')+frame(3,'ERR:private-path function expected instead of nil\0'))
        fake.sendall=send
        with self.assertRaisesRegex(reader.CaptureError,'^NATIVE_FUNCTION_UNAVAILABLE$') as e:self.capture(fake,'trace',on_record=seen.append)
        self.assertEqual(e.exception.phase,'SNAPSHOT');self.assertEqual(tuple(seen),e.exception.records)
        self.assertEqual(seen,[reader.PREFIX+'ENTRY 1 safe'])

    def test_partial_timeout_keeps_records(self):
        fake=FakeSocket();old=fake.sendall;seen=[]
        def send(value):
            old(value)
            if value[8:].startswith(b'CMD:'):
                offset=last=0
                while offset<len(fake.incoming):last=offset;offset+=8+struct.unpack('<I',fake.incoming[offset:offset+4])[0]
                del fake.incoming[last:]
        fake.sendall=send
        with self.assertRaisesRegex(reader.CaptureError,'DEADLINE_EXCEEDED') as e:self.capture(fake,'trace',on_record=seen.append)
        self.assertEqual(len(seen),1);self.assertEqual(tuple(seen),e.exception.records)

    def test_emit_before_waiting_again(self):
        fake=FakeSocket(chunk=100000);old=fake.recv;seen=[];output_done=[False]
        def recv(size):
            if output_done[0]:self.assertTrue(seen)
            value=old(size)
            if reader.PREFIX.encode() in value and b'PROBE' in value:output_done[0]=True
            return value
        fake.recv=recv
        self.capture(fake,'trace',on_record=seen.append)

    def test_passive_filter_single_command_and_bounded_return(self):
        line=reader.TRAIN_PREFIX+'seq=26 stage=UI_ROW population=16 nativeCost=1'
        extra=frame(4,'500\0GameCore_Tuner\0')+frame(0xffffffff,'0\0private token\0')+frame(0xffffffff,'0\0[SPC][B204][TRAIN] seq=1 stage=UI_ROW\0')+frame(0xffffffff,'0\0ProductionPanel: '+line+'\0')
        fake,clock=self.fixture(extra);seen=[]
        result=self.capture(fake,clock=clock,record_seconds=1,on_record=seen.append)
        self.assertIn(line,seen);self.assertEqual(len(result),2)
        self.assertEqual(seen[-1],reader.PREFIX+'WINDOW_COMPLETE passive_records=1')
        self.assertEqual(sum(text.startswith('CMD:') for _,text in fake.sent),1)
        self.assertFalse(any('private token' in x or '[B204]' in x for x in seen))

    def test_line_after_done_same_frame_preserved(self):
        fake,clock=self.fixture();old=fake.sendall;line=reader.TRAIN_PREFIX+'seq=9 stage=UI_ROW';seen=[]
        def send(value):
            old(value)
            if value[8:].startswith(b'CMD:'):
                done=re.findall(r"print\('([^']+)'\)",value[8:].decode())[-1]
                fake.incoming=bytearray(frame(0xffffffff,'0\0'+done+'\n'+line+'\0'))
        fake.sendall=send
        self.capture(fake,clock=clock,record_seconds=1,on_record=seen.append);self.assertIn(line,seen)

    def test_quiet_window_not_pass(self):
        fake,clock=self.fixture();seen=[]
        self.capture(fake,clock=clock,record_seconds=1,on_record=seen.append)
        self.assertEqual(seen[-1],reader.PREFIX+'WINDOW_COMPLETE passive_records=0')
        self.assertFalse(any('PASS' in x for x in seen))

    def test_partial_frame_deadline(self):
        fake,clock=self.fixture(b'\x02\x00')
        with self.assertRaisesRegex(reader.CaptureError,'PARTIAL_FRAME_AT_DEADLINE'):self.capture(fake,clock=clock,record_seconds=1)

    def test_disconnect_no_reconnect(self):
        fake,clock=self.fixture();old=fake.recv;fake.recv=lambda size:old(size) if fake.incoming else b''
        with self.assertRaisesRegex(reader.CaptureError,'CONNECTION_CLOSED'):self.capture(fake,clock=clock,record_seconds=1)
        self.assertEqual(sum(text.startswith('CMD:') for _,text in fake.sent),1)

    def test_stream_record_limit(self):
        fake,clock=self.fixture(frame(0xffffffff,'0\0'+reader.TRAIN_PREFIX+'seq=1 stage=UI_ROW\0')*3)
        with mock.patch.object(reader,'MAX_STREAM_RECORDS',2),self.assertRaisesRegex(reader.CaptureError,'OUTPUT_RECORD_LIMIT'):self.capture(fake,clock=clock,record_seconds=1)

    def test_stream_bytes_limit(self):
        fake,clock=self.fixture(frame(5,b'x'*1000))
        with mock.patch.object(reader,'MAX_STREAM_TOTAL',800),self.assertRaisesRegex(reader.CaptureError,'TOTAL_BYTE_LIMIT'):self.capture(fake,clock=clock,record_seconds=1)

    def test_frame_count_limit(self):
        fake=FakeSocket(initial=frame(5,b'')*10)
        with mock.patch.object(reader,'MAX_FRAMES',3),self.assertRaisesRegex(reader.CaptureError,'FRAME_COUNT_LIMIT'):self.capture(fake,'trace')

    def test_invalid_duration_no_connection(self):
        for value in (0,601):
            with self.subTest(value=value),self.assertRaisesRegex(reader.CaptureError,'DURATION_INVALID'):reader.capture('record',record_seconds=value,connect=lambda *a,**k:self.fail('connected'))

    def test_log_error_closes_socket(self):
        fake=FakeSocket()
        def emit(line):raise OSError('disk full private path')
        with self.assertRaisesRegex(reader.CaptureError,'^LOG_WRITE_FAILED$'):self.capture(fake,'trace',on_record=emit)

    def test_file_flush_exclusive_creation(self):
        with temporary_log(),mock.patch.object(reader.secrets,'token_hex',return_value='fixed'),mock.patch.object(reader,'datetime') as dt:
            dt.now.return_value.strftime.return_value='fixed';dt.now.return_value.isoformat.return_value='fixed'
            log=reader.LocalLog();log.write('record',line='safe')
            self.assertEqual(json.loads(log.path.read_text())['line'],'safe')
            with self.assertRaises(FileExistsError):reader.LocalLog()
            log.close()

    def test_symlink_refused(self):
        with temporary_log() as root:
            (root/'outside').mkdir();(root/'local').symlink_to(root/'outside',target_is_directory=True)
            with self.assertRaisesRegex(reader.CaptureError,'LOG_DIRECTORY_SYMLINK'):reader.LocalLog()

    def test_close_error_is_sanitized_failure(self):
        fake=mock.Mock();fake.path=Path('local/example.jsonl');fake.close.side_effect=OSError('private-path')
        err=io.StringIO()
        with mock.patch.object(reader,'LocalLog',return_value=fake),mock.patch.object(reader,'capture',return_value=[]),contextlib.redirect_stdout(io.StringIO()),contextlib.redirect_stderr(err):
            self.assertEqual(reader.main(['trace']),1)
        self.assertIn('LOCAL_LOG_CLOSE',err.getvalue());self.assertNotIn('private-path',err.getvalue())

    def test_cli_interruption_and_error_saved(self):
        for error,code,event in [(KeyboardInterrupt(),130,'end'),(reader.CaptureError('NATIVE_COMMAND_ERROR','SNAPSHOT'),1,'error')]:
            with self.subTest(code=code),temporary_log() as root:
                def run(*args,**kwargs):kwargs['on_record'](reader.PREFIX+'ENTRY 1 safe');raise error
                with mock.patch.object(reader,'capture',side_effect=run),contextlib.redirect_stdout(io.StringIO()),contextlib.redirect_stderr(io.StringIO()):self.assertEqual(reader.main(['record','--seconds','1']),code)
                p=next((root/'local/diagnostics/B205').glob('*.jsonl'))
                self.assertEqual([json.loads(x)['event'] for x in p.read_text().splitlines()],['start','record',event])

class ActualLuaTests(unittest.TestCase):
    def execute(self,setup):
        lua=LuaRuntime();out=[];lua.globals().print=lambda s:out.append(s)
        lua.execute('rawget=nil; ExposedMembers={}; '+setup)
        lua.execute(reader.command('trace','MARK ','MARK DONE'));return out
    def test_actual_lua_without_rawget(self):
        out=self.execute("ExposedMembers.SPC_B205TrainingTrace={schema=205,sequence=1,entries={{line='safe'}}}")
        self.assertIn('MARK ENTRY 1 safe',out);self.assertEqual(out[-1],'MARK DONE')
    def test_absent_trace_actual_lua(self):self.assertEqual(self.execute(''),['MARK ERROR TRACE_UNAVAILABLE','MARK DONE'])
    def test_sparse_and_oversize_actual_lua(self):
        for entries,error in [("{[2]={line='safe'}}",'TRACE_ENTRIES_SPARSE'),("{{line=string.rep('x',4097)}}",'TRACE_ENTRY_INVALID')]:
            with self.subTest(error=error):
                out=self.execute('ExposedMembers.SPC_B205TrainingTrace={schema=205,entries='+entries+'}')
                self.assertTrue(any(error in x for x in out));self.assertEqual(out[-1],'MARK DONE')

if __name__=='__main__':unittest.main()
