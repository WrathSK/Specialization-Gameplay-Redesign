"""S7d2 explicit queue-read permits, real Store/controllers and UI clients.
SYNC pulse retries remain for S7d3; actual ACKs settle before queue measurements.
"""
from pathlib import Path
import unittest

from refactor_harness import ROOT, legacy_source_observation
from test_refactor_s7d1 import actual

KINDS = ("Claim", "Dialogue", "Engineering")
SPECS = {
    "Claim": ("ClaimProjectUI", "SPCClaimProjectUI", "ClaimProjects", "SPC_ClaimQueueRead", "CLAIM_BEGIN"),
    "Dialogue": ("DialogueProjectUI", "SPCDialogueProjectUI", "DialogueProjects", "SPC_DialogueProjectRead", "DIALOGUE_PROJECT_BEGIN"),
    "Engineering": ("EngineeringStudyUI", "SPCEngineeringStudyUI", "EngineeringStudy", "SPC_EngineeringStudyRead", "ENGINEERING_STUDY_BEGIN"),
}


def ui_actual(kind):
    """Actual Store/controller first; current native UI method-shaped queue.

    actual(kind) starts a legitimate saved round. Cancel it through the existing
    native production event before creating a fresh UI intent, rather than
    deleting its timer or forging an empty saved record. Count only the UI
    reader bridge: real controller qualification/queue reads remain active.
    """
    vm = actual(kind)

    def include(name):
        # Required search order: the panel's UI helpers, then Gameplay helpers.
        candidates = (ROOT / "Mod/UI" / (name + ".lua"), ROOT / "Mod" / (name + ".lua"))
        path = next((p for p in candidates if p.is_file()), None)
        if path is None:
            raise FileNotFoundError(name)
        with legacy_source_observation():
            vm.execute(path.read_text())

    vm.globals().include = include
    vm.globals().fixtureKind = kind
    module, exported, backend, reader, begin = SPECS[kind]
    vm.globals().backendKey = backend
    vm.globals().readerKey = reader
    vm.globals().beginAction = begin
    vm.execute("""
    q.target='NORMAL';changed()
    assert(not pending() or pending().stage=='STOPPED')
    Game.GetLocalPlayer=function()return 0 end
    ExposedMembers=ExposedMembers or {};ExposedMembers.SPC_P0=shared
    PlayerOperations={EXECUTE_SCRIPT=1}
    local row=assert(P.Info('Projects',project));local hash=row.Hash or row.Index
    GameInfo.Projects=GameInfo.Projects or {};GameInfo.Projects[project]={Hash=hash}
    -- The UI needs only the selected project's real, already-defined hash.
    q.GetCurrentProductionTypeHash=function()return q.target==project and hash or 0 end
    uiQueueSize=1;q.GetSize=function()return uiQueueSize end
    -- Collector construction needs an iterable catalogue; these are queue-only
    -- tests and never invoke works=true or any native completion reward path.
    if fixtureKind=='Dialogue'then GameInfo.Buildings=function()return function()end end end
    uiPackets={};uiBegins=0;uiNotifies=0;uiReads=0
    function sendUI(pid,op,p)
     uiPackets[#uiPackets+1]=p
     if p.Action==beginAction then
      uiBegins=uiBegins+1
      if duringSend then duringSend()end
      shared[backendKey].Request(pid,p)
     elseif p.Action=='CLAIM_SYNC' or p.Action=='DIALOGUE_PROJECT_SYNC'then
      shared[backendKey].Sync(pid,p.CityID,p.Token)
     else error('UNEXPECTED_UI_ACTION_'..tostring(p.Action))end
    end
    """)
    include(module)
    vm.execute("""
    ui=_G[...].New(P,sendUI,function()uiNotifies=uiNotifies+1 end)
    function pumpUI()return (ui.Pulse or ui.Publish)()end
    if ui.WarmStart then ui.WarmStart();pumpUI()end
    -- Settle an actual synchronous backend ACK, not fabricated UI success.
    pumpUI();uiPackets={};uiBegins=0;uiReads=0
    local raw=assert(ExposedMembers[readerKey])
    ExposedMembers[readerKey]=function(...)
     uiReads=uiReads+1
     if unreadable then error('QUEUE_READ_UNKNOWN')end
     local value=raw(...)
     if afterQueueRead then afterQueueRead()end
     return value
    end
    function selectUI()return ui.Before(c,{Type=project},false)end
    function ordinaryUI()return ui.Before(c,{Type='NORMAL'},false)end
    function queueEventUI(pid,id)return ui.QueueEvent(pid,id)end
    function ownEventUI()return queueEventUI(c:GetOwner(),c:GetID())end
    function idleUI(n)for i=1,n do pumpUI()end end
    """, exported)
    return vm


class Permit(unittest.TestCase):
    def test_before_grants_one_read_and_real_same_city_event_recovers(self):
        for kind in KINDS:
            with self.subTest(owner=kind):
                vm = ui_actual(kind)
                vm.execute("""
                assert(type(ui.QueueEvent)=='function','PROPOSED_QUEUE_EVENT_API_MISSING')
                q.target=project;uiQueueSize=0;assert(selectUI());pumpUI()
                assert(uiReads==1 and uiBegins==0)
                uiQueueSize=1;idleUI(1000)
                assert(uiReads==1 and uiBegins==0,'SILENT_SIZE_CHANGE_IS_NOT_A_NEW_CAUSE')
                ownEventUI();pumpUI()
                assert(uiReads==2 and uiBegins==1)
                assert(pending() and pending().stage=='ACTIVE','ACTUAL_CONTROLLER_DID_NOT_START')
                local reads=uiReads;idleUI(1000)
                assert(uiReads==reads and uiBegins==1)
                """)

    def test_other_or_unreadable_consumes_permit_without_repeated_reads(self):
        for kind in KINDS:
            for mode in ("OTHER", "UNKNOWN"):
                with self.subTest(owner=kind, mode=mode):
                    vm = ui_actual(kind)
                    vm.globals().mode = mode
                    vm.execute("""
                    q.target=mode=='OTHER'and 'NORMAL'or project
                    unreadable=mode=='UNKNOWN';assert(selectUI());pumpUI()
                    assert(uiReads==1 and uiBegins==0)
                    unreadable=false;q.target=project;uiQueueSize=1;idleUI(1000)
                    assert(uiReads==1 and uiBegins==0)
                    ownEventUI();pumpUI()
                    assert(uiReads==2 and uiBegins==1 and pending().stage=='ACTIVE')
                    """)

    def test_foreign_other_city_and_unknown_metadata_do_not_grant_read(self):
        for kind in KINDS:
            with self.subTest(owner=kind):
                vm = ui_actual(kind)
                vm.execute("""
                q.target=project;uiQueueSize=0;assert(selectUI());pumpUI()
                uiQueueSize=1
                queueEventUI(3,c:GetID());queueEventUI(0,c:GetID()+999);queueEventUI(nil,nil)
                idleUI(1000);assert(uiReads==1 and uiBegins==0)
                ownEventUI();pumpUI();assert(uiReads==2 and uiBegins==1)
                """)

    def test_event_without_intent_cannot_start_and_before_still_grants_own_permit(self):
        for kind in KINDS:
            with self.subTest(owner=kind):
                vm = ui_actual(kind)
                vm.execute("""
                q.target=project;uiQueueSize=1;ownEventUI();idleUI(1000)
                assert(uiReads==0 and uiBegins==0)
                assert(selectUI());ownEventUI();pumpUI();idleUI(1000)
                assert(uiReads==1 and uiBegins==1)
                """)

    def test_ordinary_before_cancels_old_intent_even_when_native_later_matches(self):
        for kind in KINDS:
            with self.subTest(owner=kind):
                vm = ui_actual(kind)
                vm.execute("""
                assert(selectUI());assert(ordinaryUI())
                q.target=project;uiQueueSize=1;ownEventUI();idleUI(1000)
                assert(uiReads==0 and uiBegins==0)
                """)

    def test_multi_queue_rejection_cannot_be_resurrected_by_later_single_queue(self):
        for kind in KINDS:
            with self.subTest(owner=kind):
                vm = ui_actual(kind)
                vm.execute("""
                q.target=project;uiQueueSize=2;assert(selectUI());pumpUI()
                assert(uiReads==1 and uiBegins==0)
                uiQueueSize=1;ownEventUI();idleUI(1000)
                assert(uiReads==1 and uiBegins==0)
                """)

    def test_getter_cancellation_prevents_old_result_from_starting(self):
        for kind in KINDS:
            with self.subTest(owner=kind):
                vm = ui_actual(kind)
                vm.execute("""
                q.target=project;uiQueueSize=1;assert(selectUI())
                afterQueueRead=function()afterQueueRead=nil;assert(ordinaryUI())end
                pumpUI();assert(uiReads==1 and uiBegins==0)
                ownEventUI();idleUI(1000);assert(uiReads==1 and uiBegins==0)
                """)

    def test_getter_new_intent_survives_but_old_result_cannot_send_it(self):
        for kind in KINDS:
            with self.subTest(owner=kind):
                vm = ui_actual(kind)
                vm.execute("""
                q.target=project;uiQueueSize=1;assert(selectUI())
                afterQueueRead=function()
                 afterQueueRead=nil;assert(ordinaryUI());assert(selectUI())
                end
                pumpUI();assert(uiReads==1 and uiBegins==0,'OLD_READ_APPLIED_TO_NEW_INTENT')
                pumpUI();assert(uiReads==2 and uiBegins==1 and pending().stage=='ACTIVE')
                """)

    def test_getter_real_cause_survives_for_next_publish_without_recursive_drain(self):
        for kind in KINDS:
            with self.subTest(owner=kind):
                vm = ui_actual(kind)
                vm.execute("""
                q.target=project;uiQueueSize=0;assert(selectUI())
                afterQueueRead=function()
                 afterQueueRead=nil;uiQueueSize=1;ownEventUI();pumpUI()
                 assert(uiReads==1 and uiBegins==0,'REENTRANT_QUEUE_DRAIN')
                end
                pumpUI();assert(uiReads==1 and uiBegins==0)
                pumpUI();assert(uiReads==2 and uiBegins==1 and pending().stage=='ACTIVE')
                """)

    def test_getter_new_native_change_invalidates_an_old_legal_result(self):
        for kind in KINDS:
            for target,size in (("'NORMAL'",1),('project',0)):
                with self.subTest(owner=kind,target=target):
                    vm=ui_actual(kind)
                    vm.execute("q.target=project;uiQueueSize=1;assert(selectUI());afterQueueRead=function()afterQueueRead=nil;q.target="+target+";uiQueueSize="+str(size)+";ownEventUI()end;pumpUI();assert(uiReads==1 and uiBegins==0);pumpUI();assert(uiReads==2 and uiBegins==0);idleUI(1000);assert(uiReads==2 and uiBegins==0)")

    def test_send_reentry_cannot_repeat_begin_or_reread_queue(self):
        for kind in KINDS:
            with self.subTest(owner=kind):
                vm = ui_actual(kind)
                vm.execute("""
                q.target=project;uiQueueSize=1;assert(selectUI())
                duringSend=function()
                 duringSend=nil;ownEventUI();pumpUI()
                 assert(uiReads==1 and uiBegins==1)
                end
                pumpUI();idleUI(1000)
                assert(uiReads==1 and uiBegins==1 and pending().stage=='ACTIVE')
                """)

    def test_late_turn_and_turn_change_inside_getter_never_start_stale_intent(self):
        for kind in KINDS:
            for inside in (False, True):
                with self.subTest(owner=kind, inside=inside):
                    vm = ui_actual(kind)
                    vm.globals().inside = inside
                    vm.execute("""
                    q.target=project;uiQueueSize=1;assert(selectUI())
                    local before=Game.GetCurrentGameTurn()
                    local function advanceClock()Game.GetCurrentGameTurn=function()return before+1 end end
                    if inside then afterQueueRead=function()afterQueueRead=nil;advanceClock()end
                    else advanceClock();ownEventUI()end
                    pumpUI();idleUI(1000)
                    assert(uiBegins==0 and uiReads==(inside and 1 or 0))
                    """)


class SharedGate(unittest.TestCase):
    def test_no_pending_city_skips_qualification_and_clock_reads(self):
        from refactor_harness import Context,measure
        c=Context('UI');c.load('UI/TimedProjectSelectionClient');c.execute("pending={};checks,clocks=0,0;P={IsTestPlayer=function()checks=checks+1;return true end};Game.GetCurrentGameTurn=function()clocks=clocks+1;return 1 end;gate=SPCTimedProjectSelectionClient.New(P,pending);for i=1,1000 do gate.QueueEvent(0,1);gate.QueueEvent(3,999);gate.QueueEvent(nil,nil)end;assert(checks==0 and clocks==0 and next(pending)==nil)")
        measure('S7d2_empty_event_work',{'events':3000,'native_qualification_reads':0,'clock_reads':0,'new_intents':0})
    def test_close_blocks_pending_and_reentrant_result_and_releases_native_hook(self):
        from refactor_harness import Context
        c=Context('UI');c.load('UI/TimedProjectSelectionClient');c.execute("""
        pending={['0:1']={turn=1,read=true}};P={IsTestPlayer=function(pid)return pid==0 end}
        gate=SPCTimedProjectSelectionClient.New(P,pending);local p=pending['0:1']
        local ok,v,current=gate.Read('0:1',p,function()gate.Close();return 'OLD'end)
        assert(ok and v=='OLD'and not current and next(pending)==nil)
        local calls=0;local drain=gate.Bind(function()calls=calls+1 end);drain();gate.QueueEvent(0,1);assert(calls==0 and next(pending)==nil)
        """)
    def test_drain_failure_releases_guard_but_does_not_rearm_unknown(self):
        from refactor_harness import Context
        c=Context('UI');c.load('UI/TimedProjectSelectionClient');c.execute("""
        pending={['0:1']={turn=1,read=true}};P={IsTestPlayer=function(pid)return pid==0 end}
        local g=SPCTimedProjectSelectionClient.New(P,pending);local p=pending['0:1'];local calls=0;local first=true
        local drain=g.Bind(function()
         if p.read then local ok= g.Read('0:1',p,function()calls=calls+1;error('UNKNOWN')end);assert(not ok)end
         if first then first=false;error('PRESENTATION_ERROR')end
        end)
        assert(not pcall(drain));for i=1,1000 do drain()end;assert(calls==1)
        g.QueueEvent(0,1);drain();assert(calls==2)
        """)
    def test_actual_panel_wires_all_three_related_city_events_and_shutdown_removes_them(self):
        from test_refactor_s3 import panel
        c=panel("""
        delivered={};local function api(name)return {Before=function()return true end,QueueEvent=function(pid,id)delivered[#delivered+1]=name..':'..pid..':'..id end}end
        SPCClaimProjectUI.New=function()return api('claim')end
        SPCDialogueProjectUI.New=function()return api('dialogue')end
        SPCEngineeringStudyUI.New=function()return api('study')end
        """)
        c.execute("""
        for _,name in ipairs({'CityProductionChanged','CityProductionQueueChanged','CityProductionUpdated'})do Events[name].Fire(0,17)end
        assert(#delivered==9);for _,s in ipairs(delivered)do assert(s:find(':0:17',1,true))end
        shutdown();for _,name in ipairs({'CityProductionChanged','CityProductionQueueChanged','CityProductionUpdated'})do assert(Events[name].Count()==0);Events[name].Fire(0,17)end;assert(#delivered==9)
        """)

class FrozenPolling(unittest.TestCase):
    def test_superseded_silent_queue_retry_assertions_remain_on_exact_previous_UI(self):
        from contextlib import contextmanager
        from hashlib import sha256
        from unittest.mock import patch
        import subprocess
        from refactor_harness import TrackedLua51,SOURCES,measure
        from test_refactor_s7d1 import profile
        import test_b124_project_ui as claim
        import test_dialogue_project_ui as dialogue
        import test_b235_engineering as study
        originals={ROOT/'Mod/UI'/(n+'.lua'):subprocess.check_output(['git','show','d1cf0a3:Mod/UI/'+n+'.lua'],cwd=ROOT,text=True)for n in ('ClaimProjectUI','DialogueProjectUI','EngineeringStudyUI')}
        previous=Path.read_text;execute=TrackedLua51.execute
        hashes={sha256(v.encode()).hexdigest():'historical/d1cf0a3/'+str(p.relative_to(ROOT))for p,v in originals.items()}
        def read(p,*a,**kw):return originals[p]if p in originals else previous(p,*a,**kw)
        def run(vm,text,*a,**kw):
            h=sha256(text.encode()).hexdigest()
            if h in hashes:SOURCES[h]=hashes[h]
            return execute(vm,text,*a,**kw)
        with profile(),patch.object(claim,'LuaRuntime',TrackedLua51),patch.object(Path,'read_text',read),patch.object(TrackedLua51,'execute',run),legacy_source_observation():
            claim_case=claim.ClaimUI();claim_case.setUp();claim_case.runlua("local get=Players[0].GetCities;Players[0].GetCities=function()local cs=get();cs.Members=function()return ipairs({c})end;return cs end");claim_case.runlua(originals[ROOT/'Mod/UI/DialogueProjectUI.lua']);claim_case.runlua(originals[ROOT/'Mod/UI/EngineeringStudyUI.lua']);claim_case.test_claim_wait_single_request_and_display()
            dialogue.DialogueUI().test_native_selection_confirms_once_with_fresh_completion_scan()
            study_case=study.StudyUI();study_case.setUp();study_case.test_selection_waits_for_native_queue_then_sends_once()
            before=[]
            for kind in KINDS:
                vm=ui_actual(kind);vm.execute("q.target=project;uiQueueSize=0;assert(selectUI());pumpUI();idleUI(1000);assert(uiBegins==0)");before.append(vm.eval('uiReads'))
        after=[]
        for kind in KINDS:
            vm=ui_actual(kind);vm.execute("q.target=project;uiQueueSize=0;assert(selectUI());pumpUI();idleUI(1000);assert(uiBegins==0)");after.append(vm.eval('uiReads'))
        self.assertEqual(before,[1001,1001,1001]);self.assertEqual(after,[1,1,1])
        measure('S7d2_UI_queue_work',{'baseline':'d1cf0a3','owners':list(KINDS),'before_reads':before,'after_reads':after,'idle_publications':1000,'native_CPU_or_memory_claim':False})
        measure('S7d2_frozen_polling',{'source':'d1cf0a3','original_assertions':3,'current':'silent native-size change cannot grant new read permit','no_historical_report_rewrite':True})

if __name__ == '__main__':unittest.main()
