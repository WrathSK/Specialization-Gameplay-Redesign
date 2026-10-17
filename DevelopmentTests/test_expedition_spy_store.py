"""Actual B201 bounded Expedition Property store; no native or external DB claim."""
from pathlib import Path
import unittest
from lupa.lua55 import LuaRuntime

ROOT = Path(__file__).resolve().parents[1]


def fixture():
    lua = LuaRuntime(unpack_returned_tuples=True)
    lua.execute("""
      saved={};reads=0;writes=0
      function cp(v)
       if type(v)~='table'then return v end
       local out={};for k,n in pairs(v)do out[k]=cp(n)end;return out
      end
      Game={GetProperty=function(self,key)
       reads=reads+1
       if readFailure or readFailAfter and writes>0 then error('UNREADABLE')end
       return saved[key]
      end}
      P={SetProperty=function(object,key,value)
       assert(object==Game);writes=writes+1
       if writerMode=='throw_before'then error('BEFORE')end
       if writerMode=='noop' or writerMode=='false_noop'then return writerMode~='false_noop'end
       if writerMode=='third'then local other=cp(value);other.revision=other.revision+1;saved[key]=other;return end
       if writerMode=='malformed'then saved[key]={schema=9};return end
       if writerMode=='absent'then saved[key]=nil;return end
       saved[key]=value
       if writerMode=='throw_after'then error('AFTER')end
       return writerMode~='false_after'
      end}
      function record(pid,generation,revision,phase)
       local out={schema=1,owner=pid or 2,generation=generation or 1,revision=revision or 1,
        state={owner=pid or 2,phase=phase or 'CREATING',sourceCity=1,sourceName='Archive',
         sourceRef='typed owner/city/token reference',x=7,y=8,teamKey='E2-1',
         unitID=40,createdID=40,expectedName='Native name',nameVerified=true,
         target={owner=3,id=9,x=15,y=8},startTurn=80,dueTurn=85,activityKey='lease',
         taskStart=85,taskDue=87,sleepConfirmed=true}}
       local s=out.state
       if s.phase=='TASK_PREPARING' then
        s.activityMode='SLEEP';s.activityOwned=false;s.activityPending=true;s.sleepConfirmed=nil
        s.taskStart=nil;s.taskDue=nil;s.taskCompletions=0
       elseif s.phase=='TASK_RUNNING' then
        s.activityMode='ASLEEP';s.activityOwned=true;s.activityPending=false;s.taskCompletions=0
       elseif s.phase=='TASK_COMPLETE' then
        s.activityMode='NONE';s.activityOwned=false;s.activityPending=false;s.taskCompleted=87;s.taskCompletions=1
       end
       return out
      end
    """)
    lua.execute((ROOT / "Mod/ExpeditionSpyStore.lua").read_text())
    lua.execute("store=SPCExpeditionSpyStore")
    return lua


class ReadTests(unittest.TestCase):
    def test_absent_is_distinct_from_tombstone_and_corrupt(self):
        lua = fixture()
        lua.execute("""
          local row,err=store.Read(2);assert(row==nil and err==nil)
          saved.SPC_EXPEDITION_TEAM_P2=record();saved.SPC_EXPEDITION_TEAM_P2.state=nil
          row,err=store.Read(2);assert(row and row.state==nil and err==nil)
          for _,bad in ipairs({{},false,0,'bad',{schema=1}})do
           saved.SPC_EXPEDITION_TEAM_P2=bad;row,err=store.Read(2)
           assert(row==nil and err=='STORE_CORRUPT')
          end
        """)

    def test_empty_initialized_record_is_valid(self):
        lua = fixture()
        lua.execute("saved.SPC_EXPEDITION_TEAM_P2=record();saved.SPC_EXPEDITION_TEAM_P2.state.unitID=nil;local r=store.Read(2);assert(r.state.phase=='CREATING' and r.state.unitID==nil)")

    def test_read_copy_isolated_from_property_and_nested_target(self):
        lua = fixture()
        lua.execute("""
          saved.SPC_EXPEDITION_TEAM_P2=record();saved.SPC_EXPEDITION_TEAM_P2.state.target={owner=3,id=9,x=15,y=8,name='Target'}
          local r=store.Read(2);r.state.sourceName='changed';r.state.target.name='changed'
          local next=store.Read(2);assert(next.state.sourceName=='Archive' and next.state.target.name=='Target')
        """)

    def test_optional_mission_instance_and_missing_completion_evidence_roundtrip(self):
        fixture().execute("""
          local v=record(2,1,1,'TASK_RUNNING')
          v.state.missionCategory='WORKS';v.state.missionWorkID=12;v.state.missionCompletionUnknownTurn=87
          local confirmed,err=store.Write(P,2,nil,v)
          assert(confirmed and not err and confirmed.state.missionWorkID==12 and confirmed.state.missionCompletionUnknownTurn==87)
          local next=store.Read(2);assert(next.state.missionWorkID==12 and next.state.missionCompletionUnknownTurn==87)
          confirmed.state.missionWorkID=99;assert(store.Read(2).state.missionWorkID==12)
          -- The previous schema1 record remains readable, but Gate may not guess a missing work instance.
          saved.SPC_EXPEDITION_TEAM_P2=record(2,1,1,'TASK_RUNNING')
          assert(store.Read(2).state.missionWorkID==nil)
        """)

    def test_invalid_mission_evidence_scalars_are_rejected(self):
        for change in ["v.state.missionWorkID=-1", "v.state.missionWorkID=1.5",
                       "v.state.missionCompletionUnknownTurn=86", "v.state.missionCompletionUnknownTurn='87'",
                       "v.state.missionCompletionUnknownTurn=87;v.state.taskDue=nil"]:
            with self.subTest(change=change):
                fixture().execute("local v=record(2,1,1,'TASK_RUNNING');" + change + ";saved.SPC_EXPEDITION_TEAM_P2=v;local value,err=store.Read(2);assert(not value and err=='STORE_CORRUPT')")

    def test_unreadable_and_invalid_owner_are_explicit(self):
        lua = fixture()
        lua.execute("readFailure=true;local r,e=store.Read(2);assert(not r and e=='STORE_UNREADABLE');r,e=store.Read(-1);assert(not r and e=='STORE_OWNER_INVALID')")

    def test_invalid_envelope_and_state_fields(self):
        changes = [
            "v.schema=2", "v.owner=3", "v.extra=true", "v.revision=0", "v.generation=0",
            "v.state.owner=3", "v.state.phase='GUESS'", "v.state.extra=true",
            "v.state.nativePermit='forbidden'", "v.state.activityKey=string.rep('x',101)",
            "v.state.sourceRef=string.rep('x',2049)", "v.state.errorDetail=string.rep('x',221)",
            "v.state.unitID=-1", "v.state.unitID=0/0", "v.state.unitID=math.huge",
            "v.state.unitID=1.25", "v.state.nameVerified=1", "v.state.activityMode='UNKNOWN'",
            "v.state.expectedName=''", "v.state.target={owner=3,id=9,x=15}",
            "v.state.target={owner=3,id=9,x=15,y=8,unitID=1}",
            "setmetatable(v,{})", "setmetatable(v.state,{})", "v.state.self=v.state",
        ]
        for change in changes:
            with self.subTest(change=change):
                lua = fixture()
                lua.execute("local v=record();" + change + ";saved.SPC_EXPEDITION_TEAM_P2=v;local r,e=store.Read(2);assert(not r and e=='STORE_CORRUPT')")

    def test_incoherent_active_phase_records_are_corrupt(self):
        changes = [
            "v.state.phase='NAMING';v.state.unitID=nil",
            "v.state.phase='CREATED';v.state.nameVerified=false",
            "v.state.phase='CREATED';v.state.expectedName=nil",
            "v.state.phase='ARRIVED';v.state.sourceRef=nil",
            "v.state.phase='TRAVELLING';v.state.target=nil",
            "v.state.phase='TRAVELLING';v.state.dueTurn=79",
            "v.state.phase='TASK_PREPARING';v.state.activityKey=nil",
            "v.state.phase='TASK_RUNNING';v.state.sleepConfirmed=false",
            "v.state.phase='TASK_RUNNING';v.state.taskStart=nil",
            "v.state.phase='TASK_RUNNING';v.state.taskDue=84",
            "v.state.phase='TASK_COMPLETE';v.state.target=nil",
        ]
        for change in changes:
            with self.subTest(change=change):
                lua = fixture()
                lua.execute("local v=record();" + change + ";saved.SPC_EXPEDITION_TEAM_P2=v;local r,e=store.Read(2);assert(not r and e=='STORE_CORRUPT')")

    def test_corrupt_activity_modes_cannot_bypass_load_recovery(self):
        changes = [
            ("TASK_RUNNING", "v.state.activityMode='NONE'"),
            ("TASK_RUNNING", "v.state.activityMode=nil"),
            ("TASK_RUNNING", "v.state.activityMode='BLOCKED'"),
            ("TASK_RUNNING", "v.state.activityOwned=nil"),
            ("TASK_RUNNING", "v.state.activityPending=true"),
            ("TASK_PREPARING", "v.state.activityMode='ASLEEP'"),
            ("TASK_PREPARING", "v.state.activityMode='ARMED';v.state.activityOwned=false"),
            ("TASK_PREPARING", "v.state.activityMode='SLEEP';v.state.activityOwned=true"),
            ("TASK_PREPARING", "v.state.activityPending=false"),
            ("TASK_PREPARING", "v.state.sleepConfirmed=true"),
            ("TASK_COMPLETE", "v.state.activityMode='ASLEEP'"),
            ("TASK_COMPLETE", "v.state.activityPending=true"),
            ("TASK_COMPLETE", "v.state.activityOwned=true"),
            ("TASK_COMPLETE", "v.state.taskCompletions=0"),
            ("TASK_COMPLETE", "v.state.taskCompleted=nil"),
            ("TASK_COMPLETE", "v.state.taskCompleted=84"),
            ("TASK_COMPLETE", "v.state.taskStart=nil"),
            ("TASK_COMPLETE", "v.state.taskDue=nil"),
        ]
        for phase, change in changes:
            with self.subTest(phase=phase, change=change):
                lua = fixture()
                lua.execute("local v=record(2,1,1,'" + phase + "');" + change + ";saved.SPC_EXPEDITION_TEAM_P2=v;local r,e=store.Read(2);assert(not r and e=='STORE_CORRUPT');local next=record(2,1,2);r,e=store.Write(P,2,v,next);assert(not r and writes==0)")

    def test_task_complete_release_or_terminal_block_is_valid(self):
        lua = fixture()
        lua.execute("""
          for _,mode in ipairs({'NONE','RELEASE','BLOCKED'})do
           local v=record(2,1,1,'TASK_COMPLETE');v.state.activityMode=mode;v.state.activityOwned=mode~='NONE'
           saved.SPC_EXPEDITION_TEAM_P2=v;local r,e=store.Read(2);assert(r and not e)
          end
          local held=record(2,1,1,'HELD');held.state.activityMode='RELEASE';held.state.activityOwned=false;held.state.activityPending=true
          saved.SPC_EXPEDITION_TEAM_P2=held;assert(store.Read(2).state.activityPending)
        """)

    def test_armed_and_confirmed_sleep_are_distinct_valid_scalars(self):
        lua = fixture()
        lua.execute("""
          local v=record(2,1,1,'TASK_PREPARING');v.state.activityMode='ARMED';v.state.activityOwned=true;v.state.sleepConfirmed=false
          saved.SPC_EXPEDITION_TEAM_P2=v;local r=store.Read(2);assert(r.state.activityMode=='ARMED' and not r.state.sleepConfirmed)
        """)

    def test_all_approved_phases_and_scalar_fields_round_trip(self):
        lua = fixture()
        lua.execute("""
          for _,phase in ipairs({'CREATING','NAMING','CREATED','TRAVELLING','ARRIVED','TASK_PREPARING','TASK_RUNNING','TASK_COMPLETE','HELD','ENDING','ENDED'})do
           local v=record(2,1,1,phase);local s=v.state
           s.unitID=40;s.createdID=39;s.expectedName='Native name';s.nameVerified=true
           s.startTurn=80;s.dueTurn=85;s.target={owner=3,id=9,x=15,y=8,name='Target'}
           s.taskStart=85;s.taskDue=87;s.taskCompleted=87;s.taskCompletions=1
           s.activityKey='lease';s.activityMode='ASLEEP';s.activityOwned=true;s.activityPending=false;s.sleepConfirmed=true
           if phase=='TASK_PREPARING' then s.activityMode='ARMED';s.activityPending=true;s.sleepConfirmed=false end
           if phase=='TASK_COMPLETE' then s.activityMode='RELEASE' end
           s.stop='BOUNDARY';s.errorStep='LOAD';s.errorDetail='readback evidence'
           saved.SPC_EXPEDITION_TEAM_P2=v;local r,e=store.Read(2);assert(r and not e and r.state.phase==phase and r.state.sleepConfirmed==s.sleepConfirmed)
          end
        """)


class WriteTests(unittest.TestCase):
    def test_new_write_and_both_copy_boundaries(self):
        lua = fixture()
        lua.execute("""
          local candidate=record();candidate.state.target={owner=3,id=9,x=15,y=8}
          local r,e=store.Write(P,2,nil,candidate);assert(r and not e and writes==1)
          candidate.state.sourceName='input mutation';r.state.target.x=999
          local actual=store.Read(2);assert(actual.state.sourceName=='Archive' and actual.state.target.x==15)
        """)

    def test_false_or_throw_after_write_uses_actual_readback(self):
        for mode in ["false_after", "throw_after"]:
            with self.subTest(mode=mode):
                lua = fixture()
                lua.execute("writerMode='" + mode + "';local r,e=store.Write(P,2,nil,record());assert(r and not e and writes==1)")

    def test_failed_write_absent_outcome_never_retries(self):
        for mode in ["throw_before", "noop", "false_noop", "absent"]:
            with self.subTest(mode=mode):
                lua = fixture()
                lua.execute("writerMode='" + mode + "';local r,e=store.Write(P,2,nil,record());assert(not r and e=='STORE_WRITE_UNCONFIRMED_ABSENT' and writes==1)")

    def test_old_readback_does_not_confirm_candidate(self):
        lua = fixture()
        lua.execute("""
          local old=record();saved.SPC_EXPEDITION_TEAM_P2=cp(old);local candidate=record(2,1,2,'NAMING')
          writerMode='noop';local r,e=store.Write(P,2,old,candidate);assert(not r and e=='STORE_WRITE_UNCONFIRMED_OLD' and writes==1)
        """)

    def test_third_malformed_and_unreadable_readback_are_distinct(self):
        for mode, expected in [("third", "STORE_WRITE_UNCONFIRMED_OTHER"), ("malformed", "STORE_WRITE_READBACK_CORRUPT"), ("normal", "STORE_WRITE_READBACK_UNREADABLE")]:
            with self.subTest(mode=mode):
                lua = fixture()
                lua.execute("writerMode='" + mode + "';readFailAfter=" + ("true" if mode == "normal" else "false") + ";local r,e=store.Write(P,2,nil,record());assert(not r and e=='" + expected + "' and writes==1)")

    def test_stale_expected_is_rejected_before_write(self):
        lua = fixture()
        lua.execute("""
          local old=record();saved.SPC_EXPEDITION_TEAM_P2=record(2,1,2)
          local r,e=store.Write(P,2,old,record(2,1,2));assert(not r and e=='STORE_STALE_EXPECTED' and writes==0)
          r,e=store.Write(P,2,nil,record());assert(not r and e=='STORE_STALE_EXPECTED' and writes==0)
        """)

    def test_invalid_candidate_expected_sequence_and_owner_never_write(self):
        cases = [
            ("nil", "local candidate=record();candidate.state.nativePermit='x'", "STORE_CANDIDATE_INVALID"),
            ("{}", "local candidate=record()", "STORE_EXPECTED_INVALID"),
            ("nil", "local candidate=record(2,1,2)", "STORE_SEQUENCE_INVALID"),
            ("nil", "local candidate=record(2,2,1)", "STORE_SEQUENCE_INVALID"),
            ("nil", "local candidate=record(3,1,1)", "STORE_CANDIDATE_INVALID"),
        ]
        for expected_value, setup, expected_error in cases:
            with self.subTest(setup=setup):
                lua = fixture()
                lua.execute(setup + ";local r,e=store.Write(P,2," + expected_value + ",candidate);assert(not r and e=='" + expected_error + "' and writes==0)")

    def test_current_corrupt_or_unreadable_does_not_overwrite(self):
        lua = fixture()
        lua.execute("saved.SPC_EXPEDITION_TEAM_P2={};local r,e=store.Write(P,2,nil,record());assert(not r and e=='STORE_CORRUPT' and writes==0);readFailure=true;r,e=store.Write(P,2,nil,record());assert(not r and e=='STORE_UNREADABLE' and writes==0)")

    def test_generation_and_end_tombstone_retain_sequence(self):
        lua = fixture()
        lua.execute("""
          local first=assert(store.Write(P,2,nil,record()))
          local ending=record(2,1,2,'ENDING');ending=assert(store.Write(P,2,first,ending))
          local ended=record(2,1,3);ended.state=nil;ended=assert(store.Write(P,2,ending,ended))
          assert(ended.generation==1 and ended.revision==3 and ended.state==nil)
          local next=record(2,2,4);assert(store.Write(P,2,ended,next))
          local current=store.Read(2);local invalid=record(2,4,5)
          local r,e=store.Write(P,2,current,invalid);assert(not r and e=='STORE_SEQUENCE_INVALID')
          invalid=record(2,1,5);r,e=store.Write(P,2,current,invalid);assert(not r and e=='STORE_SEQUENCE_INVALID')
        """)

    def test_other_owner_property_is_untouched(self):
        lua = fixture()
        lua.execute("""
          saved.SPC_EXPEDITION_TEAM_P3=record(3,1,1,'ARRIVED');local other=saved.SPC_EXPEDITION_TEAM_P3
          assert(store.Write(P,2,nil,record()));assert(saved.SPC_EXPEDITION_TEAM_P3==other and other.state.phase=='ARRIVED')
          assert(store.Read(3).owner==3 and store.Read(2).owner==2)
        """)


if __name__ == '__main__':
    unittest.main()
