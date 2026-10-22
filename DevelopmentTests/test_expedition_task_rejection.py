"""B222 actual Gate/bridge: unexecuted denial is not an owned native failure.
Native denial causes and end-turn readiness remain USER_GAME_TEST_REQUIRED.
"""
import sqlite3
import unittest
from pathlib import Path
from test_expedition_spy_activity_integration import integrated
from test_expedition_spy_activity import ready
from test_expedition_spy_activity_ui import bridge
from test_expedition_activity_trace import fixture
from test_expedition_missions import MISSION_FIXTURE

R=Path(__file__).resolve().parents[1]
DENY="UnitManager.CanStartOperation=function()return false end"
PACKET="""
 function reject(token,extra)
  local a=ExposedMembers.SPC_ExpeditionActivity
  local p={Action='ACTIVITY',Token=token,UnitID=a.unitID,ActivityKey=a.activityKey,
   Result='REJECTED',Owned=false,Requested=false,Attempted=false,Awake=true,Sleeping=false,
   SampleTurn=currentTurn,NativeOperation=-1,Detail='ACTIVITY_SLEEP_NOT_ALLOWED'}
  for k,v in pairs(extra or {})do p[k]=v end
  handler(2,p);return ExposedMembers.SPC_ExpeditionActivityReply,p
 end
"""


class Rejection(unittest.TestCase):
    def test_all_missions_share_denial_without_native_action_clock_or_reward(self):
        for category in ('PEOPLE','WORKS','PLACES'):
            with self.subTest(category=category):
                l=integrated();l.execute(MISSION_FIXTURE);l.execute(DENY)
                l.execute("""
                 local before=req('READ','before');local p={Action='TASK',Token='reject',UnitID=41,SampleTurn=currentTurn,NativeOperation=-1}
                 for k,v in pairs(CATEGORY)do p[k]=v end
                 handler(2,p);Events.GameCoreEventPublishComplete()
                 local a=view();assert(a.phase=='ARRIVED' and a.mode=='NONE' and not a.locked and not a.owned and not a.releasePending)
                 assert(not a.taskStart and not a.taskDue and not a.activityKey and not activityUpdate)
                 local r=req('READ','after');assert(r.bound and r.sourceCity==before.sourceCity and r.teamKey==before.teamKey and r.count==1)
                 assert(r.activityFailure=='ACTIVITY_SLEEP_NOT_ALLOWED' and not r.missionCategory)
                 for i=1,20 do Events.GameCoreEventPublishComplete();Events.LocalPlayerTurnBegin()end
                 assert(sleepCalls==0 and wakeCalls==0 and insightWrites==0 and placeCalls==0 and finishCalls==0)
                 assert(#allActivityPackets==1 and allActivityPackets[1].Result=='REJECTED' and units[41].activity==0)
                """.replace('CATEGORY',category))

    def test_all_missions_keep_same_success_sleep_clock_reward_release_pipeline(self):
        for category in ('PEOPLE','WORKS','PLACES'):
            with self.subTest(category=category):
                l=integrated();l.execute(MISSION_FIXTURE)
                l.execute("""
                 local p={Action='TASK',Token='start',UnitID=41,SampleTurn=currentTurn,NativeOperation=-1}
                 for k,v in pairs(CATEGORY)do p[k]=v end
                 handler(2,p);Events.GameCoreEventPublishComplete()
                 assert(view().phase=='TASK_RUNNING' and view().taskDue==85 and sleepCalls==1)
                 currentTurn=85;ownTurn(2);Events.GameCoreEventPublishComplete()
                 assert(view().phase=='ARRIVED' and wakeCalls==1 and insightWrites==1 and placeCalls==0)
                 assert(insightRecords['CIVILIZATION_TARGET:CATEGORY'] and not activityUpdate)
                """.replace('CATEGORY',category))

    def test_new_user_attempt_gets_fresh_key_and_old_rejection_cannot_cancel_it(self):
        l=integrated();l.execute(DENY+"""
         beginTask();local old=allActivityPackets[1]
         UnitManager.CanStartOperation=function()return true end;beginTask('explicit-retry')
         local key=view().activityKey;assert(key~=old.ActivityKey and view().phase=='TASK_RUNNING')
         old.Token='replayed-with-new-token';deliver(old)
         assert(view().activityKey==key and view().phase=='TASK_RUNNING' and view().taskDue==85 and sleepCalls==1)
         assert(not view().activityFailure)
        """)

    def test_missing_or_non_boolean_permission_is_not_clean_denial(self):
        for value in ('nil','1',"'false'"):
            with self.subTest(value=value):
                l=integrated();l.execute('UnitManager.CanStartOperation=function()return '+value+' end;beginTask()')
                l.execute("assert(view().phase=='HELD' and not view().taskStart and sleepCalls==0 and allActivityPackets[1].Result=='FAILED')")

    def test_armed_permission_change_preserves_ambiguous_ownership(self):
        l=integrated();l.execute("""
         local count=0;UnitManager.CanStartOperation=function()count=count+1;return count<3 end
         beginTask();assert(#armPackets==1 and sleepCalls==0 and not view().taskStart)
         assert(allActivityPackets[2].Result=='FAILED' and allActivityPackets[2].Owned)
         assert(view().phase=='HELD')
        """)

    def test_changed_identity_or_native_activity_during_denial_never_unwinds_to_idle(self):
        for change in ("u.name='different'",'u.x=16','u.operation=7','u.activity=3'):
            with self.subTest(change=change):
                l=integrated();l.execute("local reads=0;UnitManager.CanStartOperation=function(u)reads=reads+1;if reads==2 then "+change+" end;return false end;beginTask()")
                l.execute("assert(view().phase=='HELD' and not view().taskStart and sleepCalls==0 and allActivityPackets[1].Result=='FAILED')")

    def test_gate_rejects_unproven_stale_or_owned_cancel_without_mutation(self):
        for extra in ("SampleTurn=82","Owned=true","Requested=true","Attempted=true","Awake=false","Sleeping=true","NativeOperation=9","Detail='OTHER'","ActivityKey='wrong'","UnitID=42"):
            with self.subTest(extra=extra):
                l=ready();l.execute(PACKET);l.execute("begin();local writes=storeWrites;local r=reject('bad',{"+extra+"});assert(r.error and r.phase=='TASK_PREPARING' and storeWrites==writes and not r.taskStart)")

    def test_gate_refuses_rejection_after_arming(self):
        l=ready();l.execute(PACKET);l.execute("""
         begin();ack('ARMED',true,{Awake=true,Sleeping=false})
         local r=reject('late');assert(r.error and r.activityMode=='ARMED' and r.activityOwned and r.phase=='TASK_PREPARING')
        """)

    def test_source_loss_and_store_readback_failure_still_protect(self):
        for change in ('city.token=nil','storeNoop=true','storeMalformed=true','storeThrowBefore=true'):
            with self.subTest(change=change):
                l=ready();l.execute(PACKET);l.execute("begin();"+change+";local r=reject('deny');assert(r.phase=='HELD' and r.error and not r.taskStart and insightWrites==0)")

    def test_rejection_saved_as_idle_preserves_binding_and_history_on_local_reload(self):
        l=ready();l.execute(PACKET);l.execute("""
         begin();local r=reject('deny');local writes=storeWrites
         local before=gameProperties.SPC_EXPEDITION_TEAM_P2
         assert(before.state.phase=='ARRIVED' and not before.state.missionCategory and not before.state.activityKey)
         ExposedMembers={};SPCExpeditionSpyGate.Start(P,shared)
         r=req('READ','reload');assert(r.phase=='ARRIVED' and r.bound and r.persistence=='RESTORED' and r.count==1)
         assert(r.teamKey==before.state.teamKey and r.sourceCity==before.state.sourceCity and not r.recovering)
         assert(storeWrites==writes and not r.activityFailure and insightWrites==0)
        """)

    def test_existing_held_save_is_not_automatically_cleared(self):
        l=ready();l.execute(PACKET);l.execute("""
         begin();ack('FAILED',false)
         ExposedMembers={};SPCExpeditionSpyGate.Start(P,shared)
         local r=reject('deny');assert(r.phase=='HELD' and r.error)
         assert(req('READ','held').phase=='HELD')
        """)

    def test_denial_feedback_is_localized_without_claiming_task_started(self):
        l=integrated(window=True);l.execute("gateOpen();Controls.RefreshButton.click();"+DENY+";beginTask();Events.GameCoreEventPublishComplete()")
        l.execute("assert(Controls.Report.text:find('ACTIVITY_START_DECLINED',1,true));assert(not Controls.Report.text:find('HELD_',1,true))")
        db=sqlite3.connect(':memory:');db.execute('CREATE TABLE LocalizedText(Language TEXT,Tag TEXT,Text TEXT)')
        db.executescript((R/'Mod/Text/ExpeditionGate.sql').read_text())
        rows=db.execute("SELECT Language,Text FROM LocalizedText WHERE Tag='LOC_SPC_EXPEDITION_SPY_ACTIVITY_START_DECLINED'").fetchall()
        self.assertEqual({r[0] for r in rows},{'zh_Hans_CN','en_US'})


class NativeReasons(unittest.TestCase):
    def reasons(self, result, permission='false'):
        l=fixture();l.execute("""
         OperationResultsTypes={NO_TARGETS=42};UnitOperationResults={FAILURE_REASONS=9}
         UnitManager.CanStartOperation=function(u,hash,target,visible,hint)
          assert(hash==70 and target==nil and visible==false);sleepChecks=sleepChecks+1
          if hint==false then return false end -- Native boolean-only call has no payload.
          assert(hint==42);return PERMISSION,RESULT
         end
        """.replace('PERMISSION',permission).replace('RESULT',result))
        return l

    def test_reason_keys_reuse_ring_one_denied_query_no_native_request(self):
        l=self.reasons("{[9]={'LOC_REASON_ONE','LOC_REASON_TWO'}}");l.execute("""
         publish('SLEEP');local f=records('ACTIVITY_FAILURE')[1]
         assert(f.nativeReasonStatus=='KEYS' and f.nativeReasonCount=='2' and f.nativeReasonTruncated=='false')
         assert(f.nativeReason1=='LOC_REASON_ONE' and f.nativeReason2=='LOC_REASON_TWO' and f.operationHash=='70')
         assert(f.reasonQueryStatus=='READ_OK' and f.reasonPermission=='DENIED' and f.reasonResultHint=='42')
         assert(f.unitType=='UNIT_SPC_EXPEDITION_SPY' and f.requested=='false' and f.attempted=='false')
         assert(sleepChecks==3 and sleepCalls==0 and packets[1].Result=='REJECTED')
         for i=1,20 do Events.GameCoreEventPublishComplete()end
         assert(sleepChecks==3 and #packets==1)
        """)

    def test_missing_empty_malformed_and_throwing_results_stay_explicit(self):
        for result,status in (('nil','NO_RESULT'),('false','INVALID_RESULT'),('{}','NO_REASONS'),('{[9]={}}','EMPTY'),("{[9]='other'}",'INVALID_REASONS'),("setmetatable({},{__index=function()error('private')end})",'READ_ERROR')):
            with self.subTest(result=result):
                l=self.reasons(result);l.execute("publish('SLEEP')")
                l.execute("local f=records('ACTIVITY_FAILURE')[1];assert(f.nativeReasonStatus=='"+status+"' and f.guardStatus=='DENIED');assert(packets[1].Result=='REJECTED' and sleepCalls==0)")
        l=self.reasons('{}');l.execute("UnitOperationResults=nil;publish('SLEEP');assert(records('ACTIVITY_FAILURE')[1].nativeReasonStatus=='NO_REASON_KEY')")

    def test_reason_capture_is_bounded_redacts_arbitrary_text(self):
        l=self.reasons("{[9]={'private-token-or-path',string.rep('A',101),{},'LOC_SAFE','LOC_EXCESS'}}");l.execute("""
         publish('SLEEP');local f=records('ACTIVITY_FAILURE')[1]
         assert(f.nativeReasonStatus=='PARTIAL_REDACTED' and f.nativeReasonCount=='4' and f.nativeReasonTruncated=='true')
         assert(f.nativeReason1=='REDACTED_NON_KEY' and f.nativeReason4=='LOC_SAFE' and not f.nativeReason5)
         assert(not f.line:find('private',1,true) and not f.line:find('LOC_EXCESS',1,true))
         assert(sleepCalls==0 and packets[1].Result=='REJECTED')
        """)

    def test_reason_read_disagreement_does_not_bypass_actual_denial(self):
        l=self.reasons('{}','true');l.execute("""
         publish('SLEEP');local f=records('ACTIVITY_FAILURE')[1]
         assert(f.reasonPermission=='ALLOWED' and f.guardStatus=='DENIED')
         assert(sleepCalls==0 and packets[1].Result=='REJECTED')
        """)

    def test_missing_hint_and_native_error_do_not_block_safe_rejection_or_leak_text(self):
        l=fixture();l.execute("""
         sleepDenied=true;publish('SLEEP');local f=records('ACTIVITY_FAILURE')[1]
         assert(f.reasonQueryStatus=='HINT_UNAVAILABLE' and f.nativeReasonStatus=='RESULT_HINT_UNAVAILABLE')
         assert(sleepChecks==2 and sleepCalls==0 and packets[1].Result=='REJECTED')
        """)
        l=self.reasons("error('private-path-token')");l.execute("""
         publish('SLEEP');local f=records('ACTIVITY_FAILURE')[1]
         assert(f.reasonQueryStatus=='READ_ERROR' and f.nativeReasonStatus=='READ_ERROR')
         assert(not f.line:find('private',1,true) and sleepCalls==0 and packets[1].Result=='REJECTED')
        """)

if __name__=='__main__':unittest.main()
