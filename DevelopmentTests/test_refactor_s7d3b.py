"""S7d3b actual UI/Store/controller availability, one-shot SYNC and identity.
D4 requires reliable causes; idle publish is presentation/ACK consumption only.
"""
import unittest
from refactor_harness import Context,measure
from timed_project_ui_fixture import SPECS,fixture

def kernel_fixture(kind='ClaimProjects', gp_first=True):
    c=Context('UI+Gameplay doubles')
    c.load('TimedProjectReaders');c.load('UI/TimedProjectSelectionClient')
    c.execute('''
    kind=...;members=0;finds=0;collections=0;attempts=0;fnCalls=0;packets={}
    P={Field=function(t,k)return t and t[k]end,IsTestPlayer=function(pid)return pid==0 end}
    local keys={ClaimProjects='SPC_ClaimQueueRead',DialogueProjects='SPC_DialogueProjectRead',EngineeringStudy='SPC_EngineeringStudyRead'}
    readerKey=keys[kind];action=({ClaimProjects='CLAIM_SYNC',DialogueProjects='DIALOGUE_PROJECT_SYNC',EngineeringStudy='ENGINEERING_STUDY_SYNC'})[kind]
    cities={}
    for i=1,2 do local id=i;cities[i]={GetOwner=function()return 0 end,GetID=function()return id end}end
    local collection={Members=function()members=members+1;return ipairs(cities)end,
      FindID=function(_,id)finds=finds+1;return cities[id]end}
    Players={[0]={GetCities=function()collections=collections+1;return collection end}}
    PlayerOperations={EXECUTE_SCRIPT=1}
    shared.CityProgressionStore={HistoryStartStatus=function()return 'FRESH'end}
    shared.StartStatus={ClaimProjects={state='OK'},DialogueProjects={state='OK'},EngineeringStudyProjects={state='OK'}}
    ExposedMembers.SPC_P0=shared
    backend={views={},revision=0,syncAck={}};shared[kind]=backend
    function newService()
      service=SPCTimedProjectReaders.New(P,shared);service.Attach(kind,shared[kind]);service.Seal()
    end
    function send(pid,op,p)
      attempts=attempts+1;packets[#packets+1]=p
      assert(pid==0 and op==1 and p.Action==action and type(p.Token)=='string')
      if duringSend then duringSend(p)end
      if sendThrows then error('SEND_UNCONFIRMED')end
    end
    function newClient()
      ExposedMembers[readerKey]=function()error('NO_QUEUE_READ_BY_SYNC')end
      local g=SPCTimedProjectSelectionClient.New(P,{})
      assert(type(g.Configure)=='function','PROPOSED_CONFIGURE_NOT_IMPLEMENTED')
      g.Configure(kind,readerKey,action,send)
      return g
    end
    function counters()return members,finds,collections,attempts end
    ''',kind)
    if gp_first:c.execute('newService()')
    c.execute('g=newClient();pump=g.Bind(function()fnCalls=fnCalls+1 end)')
    return c


class Kernel(unittest.TestCase):
    def test_configure_does_not_register_or_send_connect_only_schedules_warm(self):
        for kind in ('ClaimProjects','DialogueProjects','EngineeringStudy'):
            c=kernel_fixture(kind);c.execute('''
            assert(not ExposedMembers.SPC_TimedProjectReaderSlots or not ExposedMembers.SPC_TimedProjectReaderSlots[kind])
            assert(members==0 and attempts==0);g.Connect()
            assert(ExposedMembers.SPC_TimedProjectReaderSlots[kind]and members==0 and attempts==0)
            pump();assert(members==1 and attempts==2)
            ''')

    def test_ui_first_waits_for_gameplay_seal_then_one_warm_start(self):
        c=kernel_fixture(gp_first=False);c.execute('''
        g.Connect();for i=1,1000 do pump()end
        assert(members==0 and finds==0 and attempts==0)
        newService();assert(members==0 and attempts==0)
        pump();assert(members==1 and attempts==2)
        ''')

    def test_missing_ack_thousand_idle_zero_sends_or_city_lookups(self):
        c=kernel_fixture();c.execute('''
        g.Connect();pump();assert(attempts==2)
        local m,f,c,a=counters();for i=1,1000 do pump()end
        assert(members==m and finds==f and collections==c and attempts==a,'ACK_WAIT_POLLED_CITIES_OR_RESENT')
        backend.syncAck['0:1']='WRONG_ACK';for i=1,1000 do pump()end
        assert(members==m and finds==f and collections==c and attempts==a)
        backend.syncAck['0:1']=packets[1].Token;backend.syncAck['0:2']=packets[2].Token
        pump();assert(members==m and finds==f and collections==c and attempts==a)
        ''')

    def test_send_exception_and_sync_reentry_never_repeat_attempt(self):
        c=kernel_fixture();c.execute('''
        sendThrows=true;duringSend=function(p)
          local n=attempts;g.Sync(cities[p.CityID]);pump();assert(attempts==n)
        end
        g.Connect();pump();assert(attempts==2)
        local m,f,c,a=counters();for i=1,1000 do pump();g.Sync(cities[1])end
        assert(attempts==a and members==m and finds==f and collections==c)
        ''')

    def test_new_backend_one_new_sync_per_city_without_action_replay(self):
        c=kernel_fixture();c.execute('''
        g.Connect();pump();assert(attempts==2)
        shared[kind]={views={},revision=0,syncAck={}};service.Attach(kind,shared[kind])
        assert(attempts==2);pump();assert(attempts==4 and members==2)
        for i=1,1000 do pump()end;assert(attempts==4 and members==2)
        ''')

    def test_reader_replacement_invalidates_old_context_and_old_close_preserves_new(self):
        c=kernel_fixture();c.execute('''
        g.Connect();pump();local old=g;local before=attempts
        replacement=newClient();replacement.Connect()
        local slots=ExposedMembers.SPC_TimedProjectReaderSlots;local current=slots[kind]
        local read=ExposedMembers[readerKey];local reads=members
        for i=1,1000 do pump()end;assert(attempts==before and members==reads)
        old.Close();assert(slots[kind]==current and ExposedMembers[readerKey]==read)
        local newPump=replacement.Bind(function()end);newPump()
        assert(attempts==before+2)
        old.Close();newPump();assert(attempts==before+2 and slots[kind]==current)
        ''')

    def test_configure_captures_own_reader_before_interleaved_connect(self):
        c=kernel_fixture();c.execute('''
        local old=g;local latest=newClient();local current=ExposedMembers[readerKey]
        old.Connect();pump();assert(attempts==0 and ExposedMembers[readerKey]==current)
        latest.Connect();local p=latest.Bind(function()end);p();assert(attempts==2)
        ''')


class ActualUIs(unittest.TestCase):
 def test_gp_first_real_ack_one_sync_idle_zero_work(self):
  for kind in SPECS:
   with self.subTest(kind=kind):
    vm=fixture(kind);vm.execute('''
    assert(uiSyncs==0 and uiMembers==0);ui.Connect();assert(uiSyncs==0 and uiMembers==0)
    pumpUI();assert(uiSyncs>=1 and uiMembers==1)
    local r,s,m,f,col,b=counts();idleUI(1000)
    assert(uiReads==r and uiSyncs==s and uiMembers==m and uiFinds==f and uiCollections==col and uiBegins==b)
    q.target=project;assert(selectUI());pumpUI();assert(uiBegins==1 and pending().stage=='ACTIVE')
    ''')
 def test_ui_first_no_reader_scan_until_service_then_saved_begin(self):
  for kind in SPECS:
   with self.subTest(kind=kind):
    vm=fixture(kind,False);vm.execute('''
    ui.Connect();q.target=project;assert(selectUI());idleUI(1000)
    assert(uiReads==0 and uiSyncs==0 and uiMembers==0 and uiBegins==0)
    newService();assert(service.epoch==1 and uiSyncs==0 and uiReads==0)
    pumpUI();assert(uiSyncs>=1 and uiMembers==1)
    assert(uiBegins<=1);pumpUI();assert(uiBegins<=1 and pending().stage=='ACTIVE')
    local r,s,m,f,col,b=counts();idleUI(1000)
    assert(uiReads==r and uiSyncs==s and uiMembers==m and uiFinds==f and uiCollections==col and uiBegins==b)
    ''')
 def test_dropped_sync_never_city_polls_or_retries_and_begin_independent(self):
  for kind in SPECS:
   with self.subTest(kind=kind):
    vm=fixture(kind);vm.execute('''
    dropSync=true;ui.Connect();pumpUI()
    local r,s,m,f,col,b=counts();assert(s>=1);idleUI(1000)
    assert(uiReads==r and uiSyncs==s and uiMembers==m and uiFinds==f and uiCollections==col and uiBegins==b)
    q.target=project;assert(selectUI());pumpUI();assert(uiBegins==1 and pending().stage=='ACTIVE')
    ''')
 def test_failed_sync_latched_and_valid_begin_does_not_repeat(self):
  for kind in SPECS:
   with self.subTest(kind=kind):
    vm=fixture(kind);vm.execute('''
    failSync=true;ui.Connect();pumpUI();local r,s,m,f,col,b=counts();assert(s>=1)
    idleUI(1000);assert(uiReads==r and uiSyncs==s and uiMembers==m and uiFinds==f and uiCollections==col and uiBegins==b)
    q.target=project;assert(selectUI());duringSend=function()duringSend=nil;ownEventUI();pumpUI()end
    pumpUI();assert(uiBegins==1 and pending().stage=='ACTIVE');idleUI(1000);assert(uiBegins==1)
    ''')
 def test_old_close_does_not_remove_new_reader_or_registration(self):
  for kind,(_,exported,_,_,_,_) in SPECS.items():
   with self.subTest(kind=kind):
    vm=fixture(kind);vm.globals().exported=exported;vm.execute('''
    ui.Connect();pumpUI();local old=ui;local oldPump=ui.Pulse or ui.Publish
    ui=_G[exported].New(P,sendUI,function()uiNotifies=uiNotifies+1 end);ui.Connect()
    local row=ExposedMembers.SPC_TimedProjectReaderSlots[backendKey];local reader=ExposedMembers[readerKey]
    old.Close();assert(ExposedMembers.SPC_TimedProjectReaderSlots[backendKey]==row and ExposedMembers[readerKey]==reader)
    local r,s,m,f,col,b=counts();for i=1,1000 do oldPump()end
    assert(uiReads==r and uiSyncs==s and uiMembers==m and uiFinds==f and uiCollections==col and uiBegins==b)
    pumpUI();assert(uiSyncs>s and ExposedMembers.SPC_TimedProjectReaderSlots[backendKey]==row)
    ''')

 def test_late_old_ack_cannot_clear_new_claim_sync_status(self):
  vm=fixture('Claim');vm.execute('''
  dropSync=true;ui.Connect();pumpUI();local oldPump=ui.Pulse
  local oldToken=uiPackets[1].Token;local k='0:'..c:GetID()
  ui=SPCClaimProjectUI.New(P,sendUI,function()end);ui.Connect();pumpUI()
  local current=ExposedMembers.SPC_ClaimSync[k];assert(current~=nil)
  shared.ClaimProjects.syncAck[k]=oldToken;oldPump()
  assert(ExposedMembers.SPC_ClaimSync[k]==current,'OLD_ACK_CLEARED_NEW_CONTEXT_STATUS')
  ''')
 def test_old_pending_timeout_cannot_overwrite_new_claim_selection(self):
  vm=fixture('Claim');vm.execute('''
  ui.Connect();pumpUI();assert(selectUI());local oldPump=ui.Pulse
  local previousTurn=Game.GetCurrentGameTurn();Game.GetCurrentGameTurn=function()return previousTurn+1 end
  ui=SPCClaimProjectUI.New(P,sendUI,function()end);ui.Connect();assert(selectUI())
  local k='0:'..c:GetID();local current=ExposedMembers.SPC_ClaimSelection[k]
  assert(current=='等待原生选择确认');oldPump()
  assert(ExposedMembers.SPC_ClaimSelection[k]==current,'OLD_TIMEOUT_OVERWROTE_NEW_CONTEXT_SELECTION')
  ''')

 def test_new_backend_during_begin_never_replays_sent_begin(self):
  for kind in SPECS:
   with self.subTest(kind=kind):
    vm=fixture(kind);vm.execute('''
    ui.Connect();pumpUI();q.target=project;assert(selectUI())
    duringSend=function()
     duringSend=nil
     local prior=shared[backendKey]
     shared[backendKey]=setmetatable({},{__index=prior}) -- identity proxy, actual methods and saved Store retained
     service.Attach(backendKey,shared[backendKey])
    end
    pumpUI();assert(uiBegins==1 and pending().stage=='ACTIVE')
    pumpUI();idleUI(1000);assert(uiBegins==1,'NEW_BACKEND_REPLAYED_SENT_BEGIN')
    ''')
 def test_new_backend_during_getter_invalidates_old_read_and_rearms_once(self):
  for kind in SPECS:
   with self.subTest(kind=kind):
    vm=fixture(kind);vm.execute('''
    ui.Connect();pumpUI();q.target=project;assert(selectUI())
    afterQueueRead=function()
     afterQueueRead=nil
     local prior=shared[backendKey]
     shared[backendKey]=setmetatable({},{__index=prior}) -- identity boundary without a forged saved timer
     service.Attach(backendKey,shared[backendKey])
    end
    pumpUI();assert(uiBegins==0,'OLD_GENERATION_READ_STARTED_PROJECT')
    pumpUI();assert(uiBegins==1 and pending().stage=='ACTIVE')
    idleUI(1000);assert(uiBegins==1)
    ''')


class Boundaries(unittest.TestCase):
 def test_exact_capacity_no_eviction_or_idle_retry_and_new_service_reset(self):
  c=kernel_fixture();c.execute("""
  g.Connect();pump();assert(attempts==2)
  for i=3,2048 do local id=i;assert(g.Sync({GetOwner=function()return 0 end,GetID=function()return id end})=='SENT')end
  assert(attempts==2048)
  local overflow={GetOwner=function()return 0 end,GetID=function()return 2049 end}
  assert(g.Sync(overflow)=='FAILED'and g.error=='TIMED_UI_SYNC_CAPACITY')
  assert(g.Sync(cities[1])=='SENT');for i=1,1000 do pump()end;assert(attempts==2048)
  local previous=service;newService();assert(service~=previous and g.Ready())
  assert(attempts==2048);pump();assert(attempts==2050 and members==2)
  assert(g.Sync(overflow)=='SENT'and attempts==2051)
  """)
  measure('S7d3b_sync_capacity',{'per_generation':2048,'overflow':'held without eviction or resend','new_current_service':'new availability, one initialization reconciliation'})

 def test_missing_local_player_initialization_boundary_is_once_only(self):
  c=kernel_fixture();c.execute("""
  local player=Players[0];Players[0]=nil;g.Connect();pump();assert(members==0 and attempts==0)
  Players[0]=player;for i=1,1000 do pump()end;assert(members==0 and attempts==0)
  g.WarmStart();assert(members==1 and attempts==2)
  for i=1,1000 do g.WarmStart();pump()end;assert(members==1 and attempts==2)
  """)

 def test_old_service_or_rejected_restored_slot_cannot_resurrect_client(self):
  c=kernel_fixture();c.execute("""
  g.Connect();pump();local old=g;local oldService=service
  local oldRow=ExposedMembers.SPC_TimedProjectReaderSlots[kind];local oldReader=ExposedMembers[readerKey]
  local latest=newClient();latest.Connect();assert(not old.Ready())
  local row=ExposedMembers.SPC_TimedProjectReaderSlots[kind]
  ExposedMembers.SPC_TimedProjectReaderSlots[kind]=oldRow;ExposedMembers[readerKey]=oldReader
  assert(not service.Register(kind,oldRow)and not old.Ready())
  local a=attempts;for i=1,1000 do pump()end;assert(attempts==a)
  ExposedMembers.SPC_TimedProjectReaderSlots[kind]=row;ExposedMembers[readerKey]=row.reader
  newService();local latestPump=latest.Bind(function()end);latestPump();assert(attempts==a+2)
  local before=attempts;oldService.Attach(kind,shared[kind]);latestPump();assert(attempts==before)
  """)

 def test_stale_before_cannot_touch_new_claim_status(self):
  vm=fixture('Claim');vm.execute("""
  ui.Connect();pumpUI();local old=ui
  ui=SPCClaimProjectUI.New(P,sendUI,function()end);ui.Connect();assert(selectUI())
  local k='0:'..c:GetID();local text=ExposedMembers.SPC_ClaimSelection[k]
  assert(not old.Before(c,{Type=project},false))
  assert(old.Before(c,{Type='NORMAL'},false))
  assert(ExposedMembers.SPC_ClaimSelection[k]==text)
  """)

 def test_current_service_new_wake_after_old_send_error_cannot_poison_new_sync(self):
  c=kernel_fixture();c.execute("""
  local first=true
  duringSend=function()
   if first then first=false;newService();pump();error('OLD_SEND_FAILED')end
  end
  g.Connect();pump();local before=attempts
  pump();assert(attempts==before+2)
  local a=attempts;for i=1,1000 do pump()end;assert(attempts==a)
  """)


from contextlib import contextmanager
from hashlib import sha256
from pathlib import Path
import subprocess
import unittest
from unittest.mock import patch

from refactor_harness import ROOT, SOURCES, TrackedLua51, legacy_source_observation
from test_refactor_s7d1 import profile
import test_b124_project_ui as claim_base
import test_b129_claim_sync as claims
import test_dialogue_project_ui as dialogue

BASE='9bca334d2c326bb4d9003424a8db680b2846b9b6'
UI_NAMES=('ClaimProjectUI','DialogueProjectUI','EngineeringStudyUI','TimedProjectSelectionClient')
OLD_CLAIM_METHODS=(
 'test_retry_then_ack',
 'test_bounded_and_no_begin',
 'test_late_backend',
 'test_stale_ack_does_not_close',
)
OLD_DIALOGUE_METHODS=('test_retry_is_bounded_and_late_backend_waits',)

@contextmanager
def frozen_sync_sources():
 """Patch only four exact runtime paths; all other production code is current.

 SOURCES labels guarantee the executed-source closure calls these historical.
 The legacy Claim fixture suppresses include, so its actual TimedProjectDisplay
 needs the direct Current() dependencies restored explicitly below.
 """
 originals={ROOT/'Mod/UI'/(name+'.lua'):subprocess.check_output(
  ['git','show',BASE+':Mod/UI/'+name+'.lua'],cwd=ROOT,text=True)
  for name in UI_NAMES}
 previous_read=Path.read_text
 previous_execute=TrackedLua51.execute
 digests={sha256(text.encode()).hexdigest():'historical/'+BASE+'/'+str(path.relative_to(ROOT))
          for path,text in originals.items()}
 def read(path,*a,**kw):
  return originals[path]if path in originals else previous_read(path,*a,**kw)
 def execute(vm,text,*a,**kw):
  digest=sha256(text.encode()if isinstance(text,str)else text).hexdigest()
  if digest in digests:SOURCES[digest]=digests[digest]
  return previous_execute(vm,text,*a,**kw)
 original_timer=claim_base.setup_timer
 def timer_with_explicit_dependency(case):
  original_timer(case)
  # B124 intentionally disables include. Restore its real direct client and
  # TimedProjectDisplay.Current() dependencies before Claim construction.
  for name in ('TimedProjectSelectionClient','DialogueProjectUI','EngineeringStudyUI'):
   case.runlua(originals[ROOT/'Mod/UI'/(name+'.lua')])
 with profile(),patch.object(claim_base,'LuaRuntime',TrackedLua51),\
      patch.object(Path,'read_text',read),patch.object(TrackedLua51,'execute',execute),\
      patch.object(claim_base,'setup_timer',timer_with_explicit_dependency),\
      legacy_source_observation():
  yield originals


def run_legacy_method(testcase_class,method):
 """Run one selected unchanged assertion body with its own fixture and cleanup."""
 case=testcase_class(methodName=method)
 with frozen_sync_sources():
  case.setUp()
  try:getattr(case,method)()
  finally:
   try:case.tearDown()
   finally:case.doCleanups()

class FrozenSync(unittest.TestCase):
 def test_original_claim_retry_then_ack(self):
  run_legacy_method(claims.Sync,'test_retry_then_ack')
 def test_original_claim_bounded_and_no_begin(self):
  run_legacy_method(claims.Sync,'test_bounded_and_no_begin')
 def test_original_claim_late_backend(self):
  run_legacy_method(claims.Sync,'test_late_backend')
 def test_original_claim_stale_ack(self):
  run_legacy_method(claims.Sync,'test_stale_ack_does_not_close')
 def test_original_dialogue_retry_and_late_backend(self):
  run_legacy_method(dialogue.DialogueUI,'test_retry_is_bounded_and_late_backend_waits')

CURRENT_DIALOGUE_METHODS=(
 'test_fresh_sampler_uses_current_slots_not_background_cache',
 'test_saved_load_sync_does_not_create_start',
 'test_pending_click_cancels_for_ordinary_or_multi_queue',
 'test_publish_without_changes_does_not_scan_works_or_notify',
 'test_changed_production_display_only_touches_owned_item',
)

def run_current_dialogue_method(method):
 original_ui=dialogue.ui
 def handshake_ui(vm):
  original_ui(vm)
  vm.globals().include('TimedProjectReaders')
  vm.execute('''
  local readers=SPCTimedProjectReaders.New(P,shared)
  readers.Attach('DialogueProjects',shared.DialogueProjects);readers.Seal()
  assert(readers.epoch==1);ui.Connect()
  ''')
  return vm
 with profile(),patch.object(dialogue,'ui',handshake_ui):
  case=dialogue.DialogueUI(methodName=method)
  case.setUp()
  try:getattr(case,method)()
  finally:
   try:case.tearDown()
   finally:case.doCleanups()

class CurrentNonRetry(unittest.TestCase):
 def test_original_fresh_sampler(self):
  # Frozen UI scalar-x protocol; S9b2 tests the current raw producer+consumer.
  from test_refactor_s9b2 import before
  with before():run_current_dialogue_method(CURRENT_DIALOGUE_METHODS[0])
 def test_original_saved_load_no_start(self):run_current_dialogue_method(CURRENT_DIALOGUE_METHODS[1])
 def test_original_pending_cancel(self):run_current_dialogue_method(CURRENT_DIALOGUE_METHODS[2])
 def test_original_idle_no_works_or_notify(self):run_current_dialogue_method(CURRENT_DIALOGUE_METHODS[3])
 def test_original_owned_display(self):run_current_dialogue_method(CURRENT_DIALOGUE_METHODS[4])


class SyncWork(unittest.TestCase):
 def test_actual_missing_ack_before_after_workload(self):
  rows=[]
  for kind in ('Claim','Dialogue'):
   def run():
    vm=fixture(kind);vm.execute("dropSync=true;if ui.Connect then ui.Connect()elseif ui.WarmStart then ui.WarmStart()end;pumpUI();local m=uiMembers;local f=uiFinds;local s=uiSyncs;idleUI(1000);work={initial_members=m,initial_sync=s,idle_members=uiMembers-m,idle_finds=uiFinds-f,idle_sync=uiSyncs-s,total_sync=uiSyncs}")
    return {k:vm.eval('work.'+k)for k in ('initial_members','initial_sync','idle_members','idle_finds','idle_sync','total_sync')}
   with frozen_sync_sources():before=run()
   after=run()
   self.assertGreater(before['idle_sync'],0);self.assertGreater(before['idle_finds'],0)
   self.assertEqual(after['idle_members'],0);self.assertEqual(after['idle_finds'],0);self.assertEqual(after['idle_sync'],0)
   rows.append({'owner':kind,'before':before,'after':after})
  measure('S7d3b_UI_sync_work',{'baseline':BASE,'idle_publications':1000,'rows':rows,'native_CPU_or_memory_claim':False})


class SendFailureIdentity(unittest.TestCase):
    def test_old_failed_send_cannot_delete_new_explicit_same_context_intent(self):
        for kind in ('Claim', 'Dialogue', 'Engineering'):
            with self.subTest(kind=kind):
                vm = fixture(kind)
                vm.execute('''
                ui.Connect();pumpUI();q.target=project;assert(selectUI());failBegin=true
                duringSend=function()
                 duringSend=nil;assert(ordinaryUI());assert(selectUI())
                end
                pumpUI();assert(uiBegins==1)
                failBegin=false;pumpUI()
                assert(uiBegins==2 and pending().stage=='ACTIVE',
                  'NEW_EXPLICIT_INTENT_DROPPED_AFTER_PRIOR_SEND_THROW')
                idleUI(1000);assert(uiBegins==2,'OLD_BEGIN_WAS_REPLAYED')
                ''')

    def test_old_failed_claim_send_cannot_overwrite_new_context_selection(self):
        vm = fixture('Claim')
        vm.execute('''
        ui.Connect();pumpUI();q.target=project;assert(selectUI());failBegin=true
        duringSend=function()
         duringSend=nil
         ui=SPCClaimProjectUI.New(P,sendUI,function()end);ui.Connect();assert(selectUI())
         assert(ExposedMembers.SPC_ClaimSelection['0:'..c:GetID()]=='等待原生选择确认')
        end
        pumpUI()
        assert(ExposedMembers.SPC_ClaimSelection['0:'..c:GetID()]=='等待原生选择确认',
          'OLD_SEND_FAILURE_OVERWROTE_NEW_CONTEXT_SELECTION')
        ''')

    def test_claim_notify_reentry_stops_old_drain_before_new_global_status(self):
        vm = fixture('Claim')
        vm.execute('''
        oldNotify=0;replaceOnNotify=false
        ui=SPCClaimProjectUI.New(P,sendUI,function()
         oldNotify=oldNotify+1
         if replaceOnNotify then
          replaceOnNotify=false
          ui=SPCClaimProjectUI.New(P,sendUI,function()end);ui.Connect()
          uiQueueSize=1;assert(selectUI())
         end
        end)
        ui.Connect();pumpUI();oldNotify=0
        q.target=project;uiQueueSize=2;assert(selectUI());replaceOnNotify=true
        pumpUI()
        assert(oldNotify==1,
          'STALE_DRAIN_NOTIFIED_AFTER_OWN_READER_WAS_REPLACED:'..oldNotify)
        assert(ExposedMembers.SPC_ClaimSelection['0:'..c:GetID()]=='等待原生选择确认')
        ''')


class AdapterConnection(unittest.TestCase):
 def test_successful_panel_connects_after_hooks_and_initialization_events_release_on_shutdown(self):
  from test_refactor_s3 import panel
  c=panel("""
  connects,warm=0,0
  local function api()return {
   Before=function()return true end,
   Connect=function()
    assert(Events.CityProductionChanged.Count()==3)
    assert(Events.CityProductionQueueChanged.Count()==3)
    assert(Events.CityProductionUpdated.Count()==3)
    assert(Events.LocalPlayerTurnBegin.Count()==3)
    connects=connects+1
   end,
   WarmStart=function()warm=warm+1 end,
  }end
  SPCClaimProjectUI.New=api;SPCDialogueProjectUI.New=api;SPCEngineeringStudyUI.New=api
  """)
  c.execute("""
  assert(connects==3);Events.LocalPlayerTurnBegin.Fire();assert(warm==3)
  Events.LoadScreenClose.Fire();assert(warm==6)
  shutdown();Events.LocalPlayerTurnBegin.Fire();Events.LoadScreenClose.Fire();assert(warm==6)
  assert(Events.LocalPlayerTurnBegin.Count()==0 and Events.LoadScreenClose.Count()==0)
  """)


if __name__=='__main__':unittest.main()
