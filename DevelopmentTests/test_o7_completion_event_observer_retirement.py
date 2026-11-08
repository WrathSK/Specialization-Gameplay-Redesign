"""Retire the B011 observation only, with real Store and Claim owners."""
import unittest

from refactor_harness import Context, PackageVFS, ROOT, measure
from retired_crew_sources import B460, package, source
from test_o7_crew_retirement import verify_package_round_trip
from test_o7_route_observer_retirement import exercise_proof
from test_p0_panel_current_layout import panel_runtime
from test_pu07_source_attribution import runtime

REMOVED = 'CompletionProbe.lua'
CONTROLS = ('CompletionButton','CompletionNextButton')
START = ("composition.Run('CompletionProbe',{},{'CompletionProbe'},"
         "function() include('CompletionProbe');SPCCompletionProbe.Start(P,shared) end)\n")
HOOKS = ('GameEvents.CityBuilt','GameEvents.OnDistrictConstructed','Events.DistrictAddedToMap','Events.LoadScreenClose')


def roots(root, projected):
    vfs=PackageVFS(manifest=root/'Mod/SpecializationP0.modinfo',
                   forbidden_globals=('SPCCompletionProbe',) if projected else ())
    history=None if projected else (root,B460)
    gp,ui=(Context(name=name,vfs=vfs,history=history) for name in ('Gameplay','UI/BackgroundRoutes'))
    packets=exercise_proof(gp,ui)
    gp.execute("""
      local projected=...
      local s=ExposedMembers.SPC_P0
      for _,name in ipairs({'CityProgressionStore','CompletionRecordProbe','ClaimProjects','NetworkBridge'})do
        assert(s.StartStatus[name].state=='OK',name)
      end
      if projected then
        assert(s.CompletionProbe==nil and s.StartStatus.CompletionProbe==nil and SPCCompletionProbe==nil)
      else
        assert(s.StartStatus.CompletionProbe.state=='OK' and s.CompletionProbe.phase=='AFTER_LOAD_CLOSE')
      end
    """,projected)
    gp.execute("""
      local s=ExposedMembers.SPC_P0
      s.BindingProbe.Resolve=function(pid,c)assert(pid==0 and c==city1);return 'TEST_BINDING' end
      GameEvents.SPC_P0_Request.Fire(0,{Action='COMPLETION_RECORD_READ',Token='completion-record',CityID=city1:GetID()})
      assert(s.LastToken=='completion-record' and s.Snapshot:find('NO_OBSERVED_RECORD',1,true))
      completionRecord=s.Snapshot
    """)
    for ctx in (gp,ui):
        assert ctx.load_counts['missing']+ctx.load_counts['failed']==0
    return packets,[gp.eval(name+'.Count()') for name in HOOKS],gp.load_counts,ui.load_counts,gp.eval('completionRecord')


def actual_first_completion(root, projected):
    # Use the existing current Store/Claim fixture. The projection leaves its
    # production modules byte-identical and changes only the observer startup.
    v,_=runtime()
    v.execute("""
      P.Scalar=tostring
      local get=CityManager.GetDistrictAt
      districtReads=0;CityManager.GetDistrictAt=function(...)
        districtReads=districtReads+1;return get(...)
      end
      composition={Run=function(name,deps,exports,fn)assert(name=='CompletionProbe');fn()end}
    """)
    gameplay=(root/'Mod/Gameplay.lua').read_text()
    if projected:
        assert START not in gameplay and not (root/'Mod'/REMOVED).exists()
    else:
        assert gameplay.count(START)==1
        include=v.globals().include
        def load(name):
            if name=='CompletionProbe':
                v.execute(source(REMOVED,B460))
            else:
                include(name)
        v.globals().include=load
        v.execute(START)
        # Store and Claim in this fixture have already loaded. Deliver the
        # same boundary to just the additional observer callback.
        v.execute("local callbacks=Events.LoadScreenClose.list;callbacks[#callbacks]()")
    v.execute("""
      local projected=...
      districtReads=0
      local c=X.make(3)
      T.complete(c,'DISTRICT_CAMPUS')
      Events.DistrictAddedToMap.Fire(0,c:GetID()+500,c:GetID(),c:GetX()+1,5,'DISTRICT_CAMPUS')
      local first=T.encode(T.record(c))
      T.complete(c,'DISTRICT_THEATER')
      local record=T.record(c)
      assert(record.base.specialization=='RESEARCH' and record.base.potential==1)
      assert(record.base.first.type=='DISTRICT_CAMPUS' and record.base.first.districtID==c:GetID()+500)
      assert(T.encode(record)==first and X.report()==nil)
      assert(summary()==before)
      assert(shared.CityProgressionStore.ClaimState(0,aCity).eligible and shared.CityProgressionStore.ClaimState(0,bCity).eligible)
      local d=shared.CompletionProbe
      if projected then assert(d==nil and SPCCompletionProbe==nil)
      else
        local rows=d.players[0]
        assert(d.sequence==4 and rows.built==1 and rows.added==1 and rows.constructed==2 and rows.errors==0)
        assert(rows.rows[2].observation=='COMPLETE_OBSERVED' and rows.rows[3].observation=='COMPLETE_OBSERVED')
      end
      storeOutcome=T.encode({target=record,claims=summary(),writes=T.writes(),raw=T.props()})
      observerRows=d and d.sequence or 0
    """,projected)
    return v.eval('storeOutcome'),v.eval('observerRows'),v.eval('districtReads')


def panel(root):
    doc,ui=panel_runtime(root/'Mod/UI')
    controls=ui.globals().Controls
    buttons={n.get('ID'):controls[n.get('ID')].hidden for n in doc.iter('GridButton') if n.get('ID')}
    ui.execute("""
      Controls.SourceYieldButton.callbacks[Mouse.eLClick]()
      Controls.CarrierStepButton.callbacks[Mouse.eLClick]()
      Controls.CompletionRecordButton.callbacks[Mouse.eLClick]()
      assert(#requests==3 and requests[1].Action=='PROGRESSION_READ' and requests[2].Action=='NETWORK_DETAIL'
        and requests[3].Action=='COMPLETION_RECORD_READ')
    """)
    return buttons,[dict(packet.items()) for packet in ui.globals().requests.values()]



class CompletionEventObserverRetirement(unittest.TestCase):
    def test_runtime_roots_keep_routes_and_separate_completion_record(self):
        with package(B460) as previous:
            before,after=roots(previous,False),roots(ROOT,True)
        self.assertEqual(after[0],before[0])
        self.assertEqual(len(after[0]),3)
        self.assertEqual([a-b for a,b in zip(before[1],after[1],strict=True)],[1]*4)
        self.assertEqual(after[2],{**before[2],'attempts':before[2]['attempts']-1,
                                   'completed':before[2]['completed']-1})
        self.assertEqual(after[3],before[3])
        # The report's first line carries the package build stamp.
        self.assertEqual(after[4].split(' | ',1)[1],before[4].split(' | ',1)[1])
        measure('completion_event_observer_retirement',{'modeled_removed_listeners':list(HOOKS),
            'matching_route_packets':len(after[0]),'completion_record_matches':True})

    def test_real_Store_and_Claim_keep_first_valid_completion(self):
        with package(B460) as previous:
            for path in ('CityProgressionStore.lua','ClaimProjects.lua','CompletionRecordProbe.lua',
                         'FreshBindingHook.lua','EffectiveFacts.lua','LegacyCleanup.lua'):
                self.assertEqual((ROOT/'Mod'/path).read_bytes(),(previous/'Mod'/path).read_bytes())
            before,after=actual_first_completion(previous,False),actual_first_completion(ROOT,True)
        self.assertEqual(after[0],before[0])
        self.assertEqual((before[1],after[1]),(4,0))
        self.assertEqual((before[2],after[2]),(7,4))
        measure('completion_event_observer_store',{'modeled_observer_rows':[4,0],
            'modeled_district_reads':[7,4],'Store_and_Claim_match':True})

    def test_only_two_hidden_completion_viewers_leave_the_panel(self):
        with package(B460) as previous:
            old_buttons,old_requests=panel(previous)
            new_buttons,new_requests=panel(ROOT)
        for control in CONTROLS:
            self.assertTrue(old_buttons.pop(control))
        self.assertEqual(new_buttons,old_buttons)
        self.assertEqual(new_requests,old_requests)

    def test_exact_temporary_switch_and_recovery(self):
        with package(B460) as previous:
            verify_package_round_trip(self,previous/'Mod',ROOT/'Mod',(REMOVED,),'CityProgressionStore.lua')
