"""B221 diagnostic retention using actual UI bridge/ring and fixed offline reader."""
import unittest
from test_expedition_spy_activity_ui import bridge
from test_expedition_trace_reader import reader


def fixture():
    l=bridge(with_trace=True)
    l.execute("""
      function records(stage)
       local out={};for _,e in ipairs(ExposedMembers.SPC_B205TrainingTrace.entries)do
        if e.stage==stage then out[#out+1]=e end
       end;return out
      end
    """)
    return l


class ActivityTrace(unittest.TestCase):
    def test_denial_records_actual_guard_and_preserves_ack(self):
        l=fixture();l.execute("""
         sleepDenied=true;publish('SLEEP')
         local a=records('ACTIVITY_START')[1];local f=records('ACTIVITY_FAILURE')[1]
         assert(a.eligibilityStatus=='DENIED' and f.guardStatus=='DENIED')
         assert(f.reason=='ACTIVITY_SLEEP_NOT_ALLOWED' and f.activity=='0')
         assert(f.requested=='false' and f.attempted=='false')
         assert(sleepChecks==2 and sleepCalls==0 and #packets==1 and packets[1].Result=='REJECTED')
         assert(f.line:find(' stage=ACTIVITY_FAILURE ',1,true))
        """)

    def test_native_error_is_not_denial_or_sensitive_text(self):
        l=fixture();l.execute("""
         UnitManager.CanStartOperation=function()error('private-path-and-token')end
         publish('SLEEP');local f=records('ACTIVITY_FAILURE')[1]
         assert(f.guardStatus=='READ_ERROR' and f.guardError=='NATIVE_READ_ERROR')
         assert(records('ACTIVITY_START')[1].eligibilityStatus=='UNKNOWN')
         for _,e in ipairs(ExposedMembers.SPC_B205TrainingTrace.entries)do
          assert(not e.line:find('private-path',1,true))
         end
         assert(sleepCalls==0 and #packets==1)
        """)

    def test_pre_request_operation_is_distinct_from_pending(self):
        l=fixture();l.execute("""
         units[41].activity=3;publish('SLEEP');local f=records('ACTIVITY_FAILURE')[1]
         assert(f.activity=='3' and f.operationEnum=='3' and f.guardStatus=='NOT_QUERIED')
         assert(f.reason=='ACTIVITY_UNEXPECTED_STATE' and f.attempted=='false' and sleepCalls==0)
        """)

    def test_pending_timeout_retains_last_read_and_request_flags(self):
        l=fixture();l.execute("""
         delaySleep=true
         UnitManager.RequestOperation=function(u) sleepCalls=sleepCalls+1;u.activity=3 end
         publish('SLEEP');assert(#packets==0);turn=turn+1;Events.LocalPlayerTurnBegin()
         local f=records('ACTIVITY_FAILURE')[1]
         assert(f.reason=='ACTIVITY_SLEEP_TIMEOUT' and f.activity=='3')
         assert(f.requested=='true' and f.attempted=='true' and sleepCalls==1)
        """)

    def test_read_error_never_claims_current_activity(self):
        l=fixture();l.execute("""
         readThrow=true;publish('SLEEP');local f=records('ACTIVITY_FAILURE')[1]
         assert(f.reason=='READ_ERROR' and f.activity=='UNAVAILABLE' and f.guardStatus=='NOT_QUERIED')
         assert(sleepChecks==0 and sleepCalls==0 and #packets==1)
        """)

    def test_normal_completion_unchanged_no_failure_or_repeated_capture(self):
        l=fixture();l.execute("""
         publish('SLEEP');publish('RELEASE',true)
         for i=1,100 do Events.GameCoreEventPublishComplete()end
         assert(#records('ACTIVITY_START')==1 and #records('ACTIVITY_FAILURE')==0)
         assert(sleepChecks==3 and sleepCalls==1 and wakeCalls==1 and #packets==2)
        """)

    def test_snapshot_recovers_after_view_clear_without_native_calls(self):
        l=fixture();l.execute("sleepDenied=true;publish('SLEEP');ExposedMembers.SPC_ExpeditionActivity=nil;Events.GameCoreEventPublishComplete();lines={};print=function(s)lines[#lines+1]=s end")
        l.execute(reader.command('trace','MARK:','DONE'))
        lines=list(l.globals().lines.values())
        self.assertTrue(any('ENTRY' in x and 'stage=ACTIVITY_FAILURE' in x for x in lines))
        l.execute('assert(sleepChecks==2 and sleepCalls==0)')

    def test_log_failure_cannot_suppress_business_failure(self):
        l=fixture();l.execute("""
         ExposedMembers.SPC_B205TrainingTrace.entries=nil
         sleepDenied=true;publish('SLEEP')
         assert(#packets==1 and packets[1].Result=='REJECTED' and sleepCalls==0)
        """)

    def test_budget_and_ring_remain_bounded(self):
        l=fixture();l.execute("""
         local a=SPCExpeditionTrainingDiagnostics.New(SPCP0,'TEST')
         for i=1,200 do a.Record('ACTIVITY_FAILURE',{eventUnit=i})end
         local r=ExposedMembers.SPC_B205TrainingTrace
         assert(#r.entries==64 and r.suppressed>0)
        """)

if __name__=='__main__':unittest.main()
