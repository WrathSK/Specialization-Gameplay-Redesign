"""Remove the retired B057 tests while retaining real startup and cleanup."""
import unittest

from refactor_harness import Context, PackageVFS, ROOT, measure
from retired_crew_sources import B470, package
from test_p0_panel_current_layout import panel_runtime
from test_pu11_package_absence import NATIVE, scalars

CONTROLS = {
    'BoostTestZeroButton': 'BOOST_TEST_ZERO',
    'BoostTestHalfButton': 'BOOST_TEST_HALF',
    'BoostTestHighButton': 'BOOST_TEST_HIGH',
    'BoostTestAutoButton': 'BOOST_TEST_AUTO',
}


def context(root, source, name='Gameplay'):
    history = (root, source) if source else None
    return Context(name=name, vfs=PackageVFS(manifest=root/'Mod/SpecializationP0.modinfo'), history=history)


def boost_startup(root, source):
    gp, ui = (context(root, source, name) for name in ('Gameplay', 'UI/BoostRefresh'))
    for vm in (gp, ui):
        vm.execute(NATIVE)
    gp.load('Gameplay')
    gp.execute("""
      local retired=...
      local s=ExposedMembers.SPC_P0
      local boost=s.NetworkBoost
      assert(boost.retired and not boost.ready and not s.GreatWorkProbe.ready)
      local defs,index={},0
      local function add(name)
        if defs[name] then return defs[name].Index end
        index=index+1
        local row={BuildingType=name,Index=index,InternalOnly=name~='BUILDING_MONUMENT'}
        defs[name]=row;defs[index]=row
        return index
      end
      for _,row in pairs(SPCBoostConfig.rows)do add(row.building)end
      for _,name in pairs(SPCBoostIntegerConfig.rows)do add(name)end
      boostID=add('BUILDING_SPC_B057_RESEARCH_2')
      gwID=add('BUILDING_SPC_B055_GW_CITY')
      add('BUILDING_SPC_B055_GW_OBJECT')
      monumentID=add('BUILDING_MONUMENT')
      GameInfo.Buildings=defs
      present={[boostID]=true,[gwID]=true,[monumentID]=true}
      removed={}
      local buildings={HasBuilding=function(_,id)return present[id]==true end,
        RemoveBuilding=function(_,id)assert(present[id]);present[id]=nil;removed[#removed+1]=defs[id].BuildingType end}
      local city={GetID=function()return 1 end,GetOwner=function()return 0 end,GetBuildings=function()return buildings end}
      Players[0].GetCities=function()return {Members=function()return ipairs({city})end}end
      Game.SetProperty=function()error('BOOST_COMMAND_WROTE_PERSISTENT_STATE')end
      testCalls=0
      local test=boost.Test
      boost.Test=function(...) testCalls=testCalls+1;return test(...)end
      function send(packet)
        GameEvents.SPC_P0_Request.Fire(0,packet)
        assert(s.RequestIngress.action==packet.Action and s.RequestDepth==0 and s.FailureAt==nil)
      end
      local function request(action,token)send({Action=action,Token=token,CityID=1})end
      request('BOOST_READ','kept-before')
      beforeReport=s.Snapshot
      assert(s.LastToken=='kept-before' and beforeReport:find('待完成',1,true))
      for _,action in ipairs({'BOOST_TEST_ZERO','BOOST_TEST_HALF','BOOST_TEST_HIGH','BOOST_TEST_AUTO'})do
        request(action,action)
        if retired then
          assert(s.LastToken=='kept-before' and s.Snapshot==beforeReport)
        else
          assert(s.LastToken==action and s.Snapshot:find('RESEARCH_NETWORK_DEFERRED_V01',1,true))
        end
      end
      assert(not next(boost.testRaw) and #removed==0 and present[boostID] and present[gwID] and present[monumentID])
    """, source is None)
    ui.load('UI/BoostRefresh')
    ui.execute("""
      ExposedMembers.SPC_P0={Version=SPCP0.VERSION,NetworkBoost={ready=false},GreatWorkProbe={ready=false}}
    """)
    packets = []

    def emit(pid, operation, packet):
        assert pid == 0 and operation == 1
        packets.append(scalars(packet))

    ui.globals().UI.RequestPlayerOperation = emit
    ui.execute('init()')
    assert len(packets) == 1 and packets[0]['Action'] == 'BOOST_INIT'
    gp.execute('send(...)', gp.table(packets[0]))
    gp.execute("""
      local s=ExposedMembers.SPC_P0
      assert(s.NetworkBoost.ready and s.GreatWorkProbe.ready and s.NetworkBoost.changes==1)
      assert(not present[boostID] and not present[gwID] and present[monumentID])
      assert(#removed==2 and removed[1]=='BUILDING_SPC_B057_RESEARCH_2' and removed[2]=='BUILDING_SPC_B055_GW_CITY')
      send({Action='BOOST_READ',Token='kept-read',CityID=1})
      assert(s.LastToken=='kept-read' and s.Snapshot:find('已确认',1,true))
      afterReport=s.Snapshot
      send({Action='BOOST_BASELINE',Token='kept-baseline',CityID=1})
      assert(s.LastToken=='kept-baseline' and s.Snapshot==afterReport and #removed==2)
    """)
    ui.execute("""
      local s=ExposedMembers.SPC_P0
      s.NetworkBoost.ready=true;s.GreatWorkProbe.ready=true
      Events.GameCoreEventPlaybackComplete.Fire()
    """)
    assert len(packets) == 1
    assert all(vm.load_counts['missing'] + vm.load_counts['failed'] == 0 for vm in (gp, ui))
    version = gp.eval('SPCP0.VERSION')
    assert packets[0]['Token'] == version+':boost:init'
    packet = {**packets[0], 'Token': packets[0]['Token'].removeprefix(version)}
    return (packet, gp.eval('beforeReport'), gp.eval('afterReport'), scalars(gp.eval('removed')), gp.eval('testCalls'))


def panel(root, *, retired):
    doc, vm = panel_runtime(root/'Mod/UI')
    buttons = {e.get('ID'): vm.globals().Controls[e.get('ID')].hidden
               for e in doc.iter('GridButton') if e.get('ID')}
    vm.execute("""
      Controls.BoostReadButton.callbacks[Mouse.eLClick]()
      Controls.BoostBaseButton.callbacks[Mouse.eLClick]()
      Controls.SourceYieldButton.callbacks[Mouse.eLClick]()
      Controls.NetworkButton.callbacks[Mouse.eRClick]()
      if ... then
        Controls.BoostTestZeroButton.callbacks[Mouse.eLClick]()
        Controls.BoostTestHalfButton.callbacks[Mouse.eLClick]()
        Controls.BoostTestHighButton.callbacks[Mouse.eLClick]()
        Controls.BoostTestAutoButton.callbacks[Mouse.eLClick]()
      end
    """, not retired)
    return buttons, [dict(packet.items()) for packet in vm.globals().requests.values()]


class RetiredBoostTestControls(unittest.TestCase):
    def test_real_background_init_cleanup_and_reports_match(self):
        with package(B470) as previous:
            before = boost_startup(previous, B470)
            for name in ('NetworkBoost.lua', 'LegacyCleanup.lua', 'LegacyCleanupCatalog.lua', 'UI/BoostRefresh.lua',
                         'UI/BoostGreatWorkRead.lua', 'GreatWorkProbe.lua', 'BoostConfig.lua', 'BoostIntegerConfig.lua'):
                self.assertEqual((previous/'Mod'/name).read_bytes(), (ROOT/'Mod'/name).read_bytes())
        after = boost_startup(ROOT, None)
        self.assertEqual(before[:-1], after[:-1])
        self.assertEqual((before[-1], after[-1]), (4, 0))
        measure('retired_boost_test_controls', dict(
            manual_test_calls=[4,0], stale_commands_carrier_writes=[0,0],
            matching_background_init_packets=1, confirmed_carrier_removals=list(after[3].values()),
            ordinary_building_preserved=True, retained_boost_reports='MATCH'))

    def test_only_the_four_hidden_experimental_controls_retire(self):
        with package(B470) as previous:
            old_buttons, old_requests = panel(previous, retired=False)
        new_buttons, new_requests = panel(ROOT, retired=True)
        for control in CONTROLS:
            self.assertTrue(old_buttons.pop(control))
        self.assertEqual(old_buttons, new_buttons)
        self.assertEqual(old_requests[:-4], new_requests)
        self.assertEqual([r['Action'] for r in old_requests[-4:]], list(CONTROLS.values()))
        self.assertEqual([r['Action'] for r in new_requests],
                         ['BOOST_READ', 'BOOST_BASELINE', 'PROGRESSION_READ', 'NETWORK_DETAIL'])
