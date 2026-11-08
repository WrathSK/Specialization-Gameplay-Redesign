"""Retire the B106 opt-in trace while exercising the real founding path."""
import unittest

from refactor_harness import Context, PackageVFS, ROOT, measure
from retired_crew_sources import B461, B462, package, source
from test_o7_crew_retirement import verify_package_round_trip
from test_o7_route_observer_retirement import exercise_proof
from test_p0_panel_current_layout import panel_runtime
from test_pu07_source_attribution import runtime

REMOVED = 'CitySequenceProbe.lua'
START = ("composition.Run('CitySequenceProbe',{},{'CitySequenceProbe'},"
         "function() include('CitySequenceProbe');SPCCitySequenceProbe.Start(P,shared) end)\n")
HOOKS = ('GameEvents.CityBuilt','GameEvents.CityConquered','Events.CityAddedToMap','Events.CityInitialized',
         'Events.CityRemovedFromMap','Events.CityTransfered','Events.UnitActivate',
         'Events.GameCoreEventPublishComplete','Events.GameCoreEventPlaybackComplete','Events.LoadScreenClose')


def roots(root, revision, projected):
    profile=PackageVFS(manifest=root/'Mod/SpecializationP0.modinfo',
                       forbidden_globals=('SPCCitySequenceProbe',) if projected else ())
    history=(root,revision)
    gp,ui=(Context(name=name,vfs=profile,history=history) for name in ('Gameplay','UI/BackgroundRoutes'))
    packets=exercise_proof(gp,ui)
    gp.execute("""
      local projected=...
      local s=ExposedMembers.SPC_P0
      for _,name in ipairs({'CityProgressionStore','CompletionRecordProbe','ClaimProjects','NetworkBridge'})do
        assert(s.StartStatus[name].state=='OK',name)
      end
      if projected then
        assert(s.CitySequenceProbe==nil and s.StartStatus.CitySequenceProbe==nil and SPCCitySequenceProbe==nil)
      else
        assert(s.StartStatus.CitySequenceProbe.state=='OK')
      end
      CityManager=CityManager or {}
      CityManager.GetCityAt=function(x,y)
        assert(x==city1:GetX() and y==city1:GetY())
        sequenceReads=(sequenceReads or 0)+1
        return city1
      end
      local function request(action)
        GameEvents.SPC_P0_Request.Fire(0,{Action=action,Token=action,CityID=city1:GetID(),Page=1})
        assert(s.RequestIngress.action==action)
      end
      request('PROGRESSION_STORE_READ')
      storeReport=s.Snapshot
      assert(s.LastToken=='PROGRESSION_STORE_READ' and type(storeReport)=='string')
      sequenceReads=0
      request('CITY_SEQUENCE_BEGIN')
      if projected then
        assert(s.LastToken=='PROGRESSION_STORE_READ' and s.Snapshot==storeReport)
      else
        assert(s.LastToken=='CITY_SEQUENCE_BEGIN' and s.Snapshot:find('Start CITY',1,true))
      end
      request('CITY_SEQUENCE_READ')
      if projected then
        assert(s.LastToken=='PROGRESSION_STORE_READ' and s.Snapshot==storeReport and sequenceReads==0)
      else
        assert(s.LastToken=='CITY_SEQUENCE_READ' and s.Snapshot:find('Start CITY',1,true) and sequenceReads==1)
      end
    """,projected)
    for ctx in (gp,ui):
        assert ctx.load_counts['missing']+ctx.load_counts['failed']==0
    report=gp.eval('storeReport').removeprefix(gp.eval('SPCP0.VERSION')+' | ')
    return packets,[gp.eval(name+'.Count()') for name in HOOKS],gp.load_counts,ui.load_counts,report


def actual_foundation(root, projected):
    v,_=runtime()
    if projected:
        assert not (root/'Mod'/REMOVED).exists() and START not in (root/'Mod/Gameplay.lua').read_text()
    else:
        assert (root/'Mod/Gameplay.lua').read_text().count(START)==1
        v.execute(source(REMOVED,B461))
        v.execute("""
          composition={Run=function(name,deps,exports,fn)assert(name=='CitySequenceProbe');fn()end}
          local includeNative=include
          include=function(name)if name~='CitySequenceProbe'then includeNative(name)end end
        """)
        v.execute(START)
        v.execute("local callbacks=Events.LoadScreenClose.list;callbacks[#callbacks]()")
    v.execute("""
      local projected=...
      local c=T.fresh(3)
      if projected then assert(shared.CitySequenceProbe==nil and SPCCitySequenceProbe==nil)
      else assert(shared.CitySequenceProbe.Begin(0,c,nil,'ARM'):find('Start CITY',1,true))end
      T.register(c)
      local r=T.record(c)
      assert(r and r.progression=='UNASSIGNED')
      T.complete(c,'DISTRICT_CAMPUS')
      T.complete(c,'DISTRICT_THEATER')
      r=T.record(c)
      assert(r.base.specialization=='RESEARCH' and r.base.potential==1 and r.base.first.type=='DISTRICT_CAMPUS')
      assert(summary()==before and X.report()==nil)
      if not projected then
        local report=shared.CitySequenceProbe.Describe(0,1)
        assert(report:find('Built ',1,true) and report:find('Initialized ',1,true) and report:find('FoundCity ',1,true))
      end
      state=T.encode({stored=T.props(),writes=T.writes(),target=r,claimPeers=summary()})
    """,projected)
    return v.eval('state')


def panel(root, projected):
    tree,ui=panel_runtime(root/'Mod/UI')
    controls=ui.globals().Controls
    buttons={n.get('ID'):controls[n.get('ID')].hidden for n in tree.iter('GridButton') if n.get('ID')}
    ui.execute("""
      local projected=...
      Controls.SourceYieldButton.callbacks[Mouse.eLClick]()
      Controls.InheritReadButton.callbacks[Mouse.eLClick]()
      Controls.OpenButton.callbacks[Mouse.eRClick]()
      assert(#requests==3 and requests[1].Action=='PROGRESSION_READ' and requests[2].Action=='PROGRESSION_STORE_READ'
        and requests[3].Action=='EVENT_ORDER_TOGGLE')
      if projected then
        assert(Controls.UnitReadButton==nil and Controls.InheritReadButton.callbacks[Mouse.eRClick]==nil)
      else
        Controls.UnitReadButton.callbacks[Mouse.eRClick]()
        Controls.InheritReadButton.callbacks[Mouse.eRClick]()
        assert(#requests==5 and requests[4].Action=='CITY_SEQUENCE_BEGIN' and requests[4].UnitID==17
          and requests[5].Action=='CITY_SEQUENCE_READ')
      end
    """,projected)
    return buttons,[dict(packet.items()) for packet in ui.globals().requests.values()][:3]



class CitySequenceObserverRetirement(unittest.TestCase):
    def test_real_roots_keep_route_proof_and_store_query(self):
        with package(B461) as previous, package(B462) as retired:
            old,new=roots(previous,B461,False),roots(retired,B462,True)
        self.assertEqual(old[0],new[0])
        self.assertEqual(len(new[0]),3)
        self.assertEqual([a-b for a,b in zip(old[1],new[1],strict=True)],[1]*len(HOOKS))
        self.assertEqual(new[2],{**old[2],'attempts':old[2]['attempts']-1,
                                'completed':old[2]['completed']-1})
        self.assertEqual(old[3:],new[3:])
        measure('city_sequence_observer_retirement',{'modeled_removed_listeners':list(HOOKS),
            'matching_route_packets':len(new[0]),'store_read_matches':True})

    def test_foundation_first_completion_and_claim_peers_match_with_trace_armed(self):
        with package(B461) as previous:
            for path in ('CityProgressionStore.lua','ClaimProjects.lua','CompletionRecordProbe.lua',
                         'FreshBindingHook.lua','EffectiveFacts.lua','LegacyCleanup.lua'):
                self.assertEqual((ROOT/'Mod'/path).read_bytes(),(previous/'Mod'/path).read_bytes())
            self.assertEqual(actual_foundation(previous,False),actual_foundation(ROOT,True))
        measure('city_sequence_store',{'old_trace_armed':True,'persisted_state_and_writes_match':True})

    def test_panel_retires_the_two_trace_actions_and_keeps_current_requests(self):
        with package(B461) as previous, package(B462) as retired:
            old_buttons,old_requests=panel(previous,False)
            new_buttons,new_requests=panel(retired,True)
        self.assertTrue(old_buttons.pop('UnitReadButton'))
        self.assertEqual(old_buttons,new_buttons)
        self.assertEqual(old_requests,new_requests)

    def test_exact_temporary_switch_and_recovery(self):
        with package(B461) as previous, package(B462) as retired:
            verify_package_round_trip(self,previous/'Mod',retired/'Mod',(REMOVED,),'CityProgressionStore.lua')
