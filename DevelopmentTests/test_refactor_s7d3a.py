"""S7d3a fixed three-slot initialization handshake and independent study sync.
Explicit Lua51 composition; no native delivery or UI acceptance claim.
"""
import unittest
from refactor_harness import Context,measure
from test_refactor_s7d1 import actual


def fixture(state='FRESH'):
    c = Context()
    c.load('TimedProjectReaders')
    c.execute('''
    state=...;scalarReads=0;readerReads=0;wakes={};readerSerial=0
    P={Field=function(t,k)return t and t[k]end}
    shared.CityProgressionStore={HistoryStartStatus=function()
      scalarReads=scalarReads+1;return state
    end}
    shared.StartStatus={ClaimProjects={state='OK'},DialogueProjects={state='OK'},
      EngineeringStudyProjects={state='OK'}}
    Players=setmetatable({},{__index=function()error('UNEXPECTED_CITY_READ')end})
    d=SPCTimedProjectReaders.New(P,shared)
    ExposedMembers.SPC_TimedProjectReaderSlots={}
    local keys={ClaimProjects='SPC_ClaimQueueRead',DialogueProjects='SPC_DialogueProjectRead',EngineeringStudy='SPC_EngineeringStudyRead'}
    function slot(kind)
      readerSerial=readerSerial+1
      local r={serial=readerSerial,reader=function()readerReads=readerReads+1;error('READER_MUST_NOT_RUN')end}
      r.wake=function(backend,epoch,reader)
        assert(backend==shared[kind]and epoch==1 and reader==r.reader)
        wakes[kind]=(wakes[kind]or 0)+1
      end
      ExposedMembers.SPC_TimedProjectReaderSlots[kind]=r
      ExposedMembers[keys[kind]]=r.reader;return r
    end
    function attach(kind)
      local b={Sync=function()error('NO_AUTOMATIC_SYNC')end}
      shared[kind]=b;d.Attach(kind,b);return b
    end
    ''', state)
    return c


class Core(unittest.TestCase):
    def test_ui_first_late_backend_and_duplicate_signals(self):
        c=fixture();c.execute('''
        a=slot('ClaimProjects');assert(d.Register('ClaimProjects',a));assert(not wakes.ClaimProjects)
        attach('ClaimProjects');assert(d.epoch==0);d.Seal();assert(wakes.ClaimProjects==1)
        for i=1,50 do d.Register('ClaimProjects',a);d.Attach('ClaimProjects',shared.ClaimProjects);d.Seal();publish()end
        assert(wakes.ClaimProjects==1 and readerReads==0)
        ''')

    def test_gp_first_new_current_reader_wakes_once(self):
        c=fixture();c.execute('''
        attach('DialogueProjects');d.Seal();assert(d.epoch==1 and not wakes.DialogueProjects)
        a=slot('DialogueProjects');assert(d.Register('DialogueProjects',a));assert(wakes.DialogueProjects==1)
        d.Register('DialogueProjects',a);assert(wakes.DialogueProjects==1 and readerReads==0)
        ''')

    def test_waiting_recovers_only_initialization_boundary_and_latches(self):
        c=fixture('WAITING');c.execute('''
        a=slot('ClaimProjects');d.Register('ClaimProjects',a);attach('ClaimProjects');d.Seal()
        for i=1,20 do publish()end;assert(d.epoch==0 and not wakes.ClaimProjects)
        state='EXISTING';Events.LoadScreenClose.Fire();assert(d.epoch==1 and wakes.ClaimProjects==1)
        local n=scalarReads;for i=1,1000 do publish()end
        assert(scalarReads==n and wakes.ClaimProjects==1 and readerReads==0)
        ''')

    def test_held_never_initializes(self):
        c=fixture('HELD');c.execute('''
        a=slot('EngineeringStudy');d.Register('EngineeringStudy',a);attach('EngineeringStudy');d.Seal()
        for i=1,50 do publish();Events.LoadScreenClose.Fire()end
        assert(d.epoch==0 and not wakes.EngineeringStudy and readerReads==0)
        ''')

    def test_failed_dependency_and_engineering_startup_alias_are_not_ready(self):
        c=fixture();c.execute('''
        a=slot('EngineeringStudy');d.Register('EngineeringStudy',a);attach('EngineeringStudy')
        shared.StartStatus.EngineeringStudy={state='OK'}
        shared.StartStatus.EngineeringStudyProjects.state='SKIPPED_DEPENDENCY'
        d.Seal();assert(not wakes.EngineeringStudy)
        shared.StartStatus.EngineeringStudyProjects.state='FAILED'
        d.Register('EngineeringStudy',a);assert(not wakes.EngineeringStudy)
        ''')

    def test_actual_composition_rolls_back_late_failed_attached_backend(self):
        c=fixture();c.load('RuntimeComposition');c.execute('''
        print=function()end;composition=SPCRuntimeComposition.New(shared)
        a=slot('ClaimProjects');d.Register('ClaimProjects',a)
        assert(not composition.Run('ClaimProjects',{}, {'ClaimProjects'},function()
          attach('ClaimProjects');error('LATE_OWNER_FAILURE')
        end))
        b=slot('DialogueProjects');d.Register('DialogueProjects',b)
        assert(composition.Run('DialogueProjects',{}, {'DialogueProjects'},function()attach('DialogueProjects')end))
        composition.Complete();d.Seal()
        assert(not wakes.ClaimProjects and wakes.DialogueProjects==1 and readerReads==0)
        ''')

    def test_noncurrent_row_or_reader_and_unknown_kind_are_rejected(self):
        c=fixture();c.execute('''
        attach('ClaimProjects');d.Seal();a=slot('ClaimProjects')
        assert(not d.Register('ClaimProjects',{reader=a.reader,wake=a.wake}))
        ExposedMembers.SPC_ClaimQueueRead=function()end
        assert(not d.Register('ClaimProjects',a)and not wakes.ClaimProjects)
        assert(not pcall(d.Register,'FUTURE',a)and not pcall(d.Attach,'FUTURE',{}))
        ''')

    def test_old_ui_close_cannot_remove_new_reader(self):
        c=fixture();c.execute('''
        attach('ClaimProjects');d.Seal();a=slot('ClaimProjects');d.Register('ClaimProjects',a)
        b=slot('ClaimProjects');d.Register('ClaimProjects',b);d.Unregister('ClaimProjects',a)
        d.Register('ClaimProjects',b);assert(wakes.ClaimProjects==2 and readerReads==0)
        ''')

    def test_wake_exception_isolated_and_not_replayed_even_for_bad_error_object(self):
        c=fixture();c.execute('''
        attach('ClaimProjects');attach('DialogueProjects')
        a=slot('ClaimProjects');b=slot('DialogueProjects');attempts=0
        a.wake=function()attempts=attempts+1;error(setmetatable({},{__tostring=function()error('BAD_TOSTRING')end}))end
        d.Register('ClaimProjects',a);d.Register('DialogueProjects',b)
        assert(pcall(d.Seal));for i=1,10 do d.Register('ClaimProjects',a);d.Seal()end
        assert(attempts==1 and d.errors.ClaimProjects and wakes.DialogueProjects==1)
        ''')

    def test_epoch_is_not_published_before_composition_seal(self):
        c=fixture();c.execute('''
        a=slot('ClaimProjects');d.Register('ClaimProjects',a);attach('ClaimProjects')
        Events.LoadScreenClose.Fire();publish()
        assert(d.epoch==0 and not wakes.ClaimProjects,'EPOCH_PUBLISHED_BEFORE_SEAL')
        d.Seal();assert(d.epoch==1 and wakes.ClaimProjects==1)
        ''')

    def test_unregister_reregister_same_tuple_does_not_replay(self):
        c=fixture();c.execute('''
        attach('ClaimProjects');a=slot('ClaimProjects');d.Register('ClaimProjects',a);d.Seal()
        d.Unregister('ClaimProjects',a);d.Register('ClaimProjects',a)
        assert(wakes.ClaimProjects==1,'SAME_DELIVERY_TUPLE_REPLAYED')
        ''')

    def test_old_current_row_restoration_does_not_replay_prior_delivery(self):
        c=fixture();c.execute('''
        attach('ClaimProjects');a=slot('ClaimProjects');d.Register('ClaimProjects',a);d.Seal()
        b=slot('ClaimProjects');d.Register('ClaimProjects',b)
        ExposedMembers.SPC_TimedProjectReaderSlots.ClaimProjects=a;ExposedMembers.SPC_ClaimQueueRead=a.reader
        d.Register('ClaimProjects',a)
        assert(wakes.ClaimProjects==2,'OLD_ROW_RESTORATION_REPLAYED')
        ''')

    def test_new_reader_is_not_announced_ready_while_store_is_currently_held(self):
        c=fixture();c.execute('''
        attach('ClaimProjects');a=slot('ClaimProjects');d.Register('ClaimProjects',a);d.Seal()
        state='HELD';b=slot('ClaimProjects');d.Register('ClaimProjects',b)
        assert(wakes.ClaimProjects==1,'HELD_NEW_READER_GOT_READY_WAKE')
        ''')

    def test_invalid_serial_is_never_admitted_and_same_row_mutation_is_rejected(self):
        for expression in ('nil','0','-1','.5','0/0','math.huge',"'1'"):
            c=fixture();c.execute('''
            attach('ClaimProjects');d.Seal();a=slot('ClaimProjects');a.serial=...
            assert(not d.Register('ClaimProjects',a)and not wakes.ClaimProjects)
            ''', c.eval(expression))
        c=fixture();c.execute('''
        attach('ClaimProjects');d.Seal();a=slot('ClaimProjects');assert(d.Register('ClaimProjects',a))
        a.wake=function()error('MUTATED_WAKE')end
        assert(not d.Register('ClaimProjects',a)and wakes.ClaimProjects==1)
        a.serial=a.serial+1;assert(not d.Register('ClaimProjects',a)and wakes.ClaimProjects==1)
        ''')


class EngineeringSync(unittest.TestCase):
    def test_sync_rehydrates_but_never_creates_a_round_or_persistent_ack(self):
        l=actual('Engineering');l.execute("q.target='NORMAL';changed();local before=snapshot();local writes=T.writes();study.Sync(0,c:GetID(),'SYNC');assert(snapshot()==before and T.writes()==writes and not pending()and study.syncAck['0:'..c:GetID()]=='SYNC'and S.finishes(c)==0)")
    def test_saved_due_round_uses_original_full_turn_and_unique_completion(self):
        l=actual('Engineering');l.execute("Events.PlayerTurnDeactivated.Fire(0);local now=Game.GetCurrentGameTurn();Game.GetCurrentGameTurn=function()return now+1 end;study.Sync(0,c:GetID(),'DUE');assert(S.L(c)==1 and S.finishes(c)==1 and not pending());study.Sync(0,c:GetID(),'REPEAT');assert(S.L(c)==1 and S.finishes(c)==1)")
    def test_calling_unknown_or_failed_native_is_never_replayed_by_sync(self):
        for failure in ('missingCompletion','finishThrow'):
            l=actual('Engineering');l.execute('S.'+failure+"=true;S.endturn();assert(S.finishes(c)==1 and not finished());local before=snapshot();for i=1,20 do study.Sync(0,c:GetID(),'ACK'..i)end;assert(S.finishes(c)==1 and snapshot()==before)")
    def test_unknown_qualification_preserves_round_and_cannot_finish_via_sync(self):
        l=actual('Engineering');l.execute("local before=snapshot();S.unknown=true;study.Sync(0,c:GetID(),'UNKNOWN');assert(snapshot()==before and pending().stage=='ACTIVE'and S.finishes(c)==0)")
    def test_sync_due_city_never_advances_another_active_city(self):
        l=actual('Engineering');l.execute("""
        other=H.city(2);other.buildings[10]=true;H.district(other,'DISTRICT_INDUSTRIAL_ZONE',true)
        for i=1,3 do T.invest(other,9000+i)end;S.queue(other);S.begin(other)
        assert(S.state(other).value.pending.stage=='ACTIVE');Events.PlayerTurnDeactivated.Fire(0)
        local now=Game.GetCurrentGameTurn();Game.GetCurrentGameTurn=function()return now+1 end
        local oq=other:GetBuildQueue();local get=oq.CurrentlyBuilding;otherReads=0;oq.CurrentlyBuilding=function(...)otherReads=otherReads+1;return get(...)end
        study.Sync(0,c:GetID(),'ONE');assert(S.L(c)==1 and S.finishes(c)==1 and S.L(other)==0 and S.finishes(other)==0 and otherReads==0)
        study.Sync(0,other:GetID(),'TWO');assert(S.L(other)==1 and S.finishes(other)==1)
        """)
        measure('S7d3a_study_sync_scope',{'actual':'Store/FC/Bindings/IndustryHistory/EngineeringStudy','due_cities':2,'other_city_target_reads_during_first_sync':0,'separate_receipts':2,'replayed_native_calls':0})
    def test_gameplay_routes_new_sync_separately_from_begin(self):
        from refactor_defect_fixtures import request_context
        c=request_context();c.execute("calls={};shared.EngineeringStudy={Sync=function(pid,id,token)calls[#calls+1]='SYNC:'..pid..':'..id..':'..token end,Request=function(pid,p)calls[#calls+1]='BEGIN:'..p.CityID end};runRequest(0,{Action='ENGINEERING_STUDY_SYNC',CityID=17,Token='R'});runRequest(0,{Action='ENGINEERING_STUDY_BEGIN',CityID=18,Token='B'});assert(table.concat(calls,',')=='SYNC:0:17:R,BEGIN:18');shared.EngineeringStudy.startupError='FAILED';runRequest(0,{Action='ENGINEERING_STUDY_SYNC',CityID=17,Token='S'});assert(#calls==2)")

if __name__=='__main__':unittest.main()
