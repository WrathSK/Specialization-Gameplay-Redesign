"""Replay the old panel requests through real Lua entrypoints before and after removal."""
import unittest

from refactor_harness import ROOT, measure
from retired_crew_sources import B476, package
from test_o7_retired_great_work_adjacency_retirement import context
from test_p0_panel_current_layout import panel_runtime
from test_pu11_package_absence import NATIVE, scalars

RETIRED_CONTROLS = frozenset((
    'GWObjectButton', 'PurchaseBaseButton', 'PurchaseOnButton', 'PurchaseOffButton',
    'PurchaseReadButton', 'Lv2GPPButton', 'BaselineButton', 'InspirationEndButton',
    'InheritRecordButton', 'DP1Button',
))
IDENTITY_EVENTS = ('CityTransfered', 'CulturalIdentityCityConverted', 'CityLiberated')


def panel(root, *, legacy=False):
    doc, vm = panel_runtime(root / 'Mod/UI', real_identity_evidence=True)
    controls = vm.globals().Controls
    buttons = {}
    for node in doc.iter('GridButton'):
        name = node.get('ID')
        if name:
            control = controls[name]
            buttons[name] = (control.hidden, dict(node.attrib), frozenset(control.callbacks.keys()))
    if legacy:
        vm.execute("""
          Controls.CopyButton.callbacks[Mouse.eLClick]()
          local copy,caption=table.concat(printed,'\\n'),Controls.Status.text
          printed={}
          Controls.BaselineButton.callbacks[Mouse.eLClick]()
          assert(copy==table.concat(printed,'\\n') and caption==Controls.Status.text and #requests==0)
          Controls.Lv2GPPButton.callbacks[Mouse.eLClick]()
          assert(requests[1].Action=='LV2_GPP_READ' and requests[1].CityID==11)
          requests={};ExposedMembers.SPC_P0_UISequence=nil
        """)
    vm.execute("""
      local left,right=Mouse.eLClick,Mouse.eRClick
      local clicks={{'SpecialistsButton',right},{'MeaningConfigButton',left},{'MeaningConfigButton',right},
                    {'GWBaselineButton',left},{'GWReadButton',left},{'GWReadButton',right},
                    {'GWCityButton',left},{'GWCityButton',right},{'BoostReadButton',left},
                    {'BoostBaseButton',left},{'TemplatesButton',left},{'TemplatesButton',right},
                    {'InheritReadButton',left},{'ResearchReadButton',left},{'CommerceREADButton',left}}
      for _,click in ipairs(clicks) do Controls[click[1]].callbacks[click[2]]() end
    """)
    requests = [dict(packet.items()) for packet in vm.globals().requests.values()]
    return buttons, requests, dict(vm.globals().eventAdds.items())


def fixture(root, revision):
    gp = context(root, revision)
    gp.execute(NATIVE)
    load = gp.globals().include

    def include(name):
        result = load(name)
        if name == 'PurchaseProbe':
            # Use the callback actually installed by this owner. The native
            # doubles below cover carrier handling, not every LoadScreenClose consumer.
            gp.execute("""
              local start=SPCPurchaseProbe.Start
              function SPCPurchaseProbe.Start(...)
                local n=Events.LoadScreenClose.Count()
                start(...)
                purchaseClose=Events.LoadScreenClose.Count()
                assert(purchaseClose==n+1)
              end
            """)
        return result

    gp.globals().include = include
    gp.load('Gameplay')
    gp.execute("""
      local s=ExposedMembers.SPC_P0
      assert(s.StartStatus.GreatWorkProbe.state=='OK' and s.StartStatus.PurchaseProbe.state=='OK')
      assert(s.NetworkBoost.retired and not s.NetworkBoost.ready and not s.GreatWorkProbe.ready)
      local definitions,index={},0
      local function add(name)
        if definitions[name] then return definitions[name].Index end
        index=index+1
        local row={BuildingType=name,Index=index,InternalOnly=name~='BUILDING_MONUMENT'}
        definitions[name]=row;definitions[index]=row
        return index
      end
      for _,row in pairs(SPCBoostConfig.rows)do add(row.building)end
      for _,name in pairs(SPCBoostIntegerConfig.rows)do add(name)end
      boostID=add('BUILDING_SPC_B057_RESEARCH_2')
      cityWorkID=add('BUILDING_SPC_B055_GW_CITY')
      objectWorkID=add('BUILDING_SPC_B055_GW_OBJECT')
      purchaseFixtureID=add('BUILDING_SPC_B053_FIXTURE')
      purchaseDiscountID=add('BUILDING_SPC_B053_DISCOUNT')
      monumentID=add('BUILDING_MONUMENT')
      GameInfo.Buildings=definitions
      localPresent={[boostID]=true,[cityWorkID]=true,[objectWorkID]=true,
                    [purchaseFixtureID]=true,[purchaseDiscountID]=true,[monumentID]=true}
      foreignPresent={[purchaseFixtureID]=true,[purchaseDiscountID]=true,[monumentID]=true}
      changes={};rejectObject=true;propertyWrites=0
      local function playerCities(pid,id,present)
        local buildings={HasBuilding=function(_,key)return present[key]==true end,
          RemoveBuilding=function(_,key)
            assert(present[key])
            if key==objectWorkID and rejectObject then error('FIXTURE_OBJECT_REMOVE_UNAVAILABLE')end
            present[key]=nil
            changes[#changes+1]={'REMOVE',pid,definitions[key].BuildingType}
          end}
        local queue={CreateBuilding=function(_,key)
          assert(not present[key]);present[key]=true
          changes[#changes+1]={'ADD',pid,definitions[key].BuildingType}
        end}
        local city={GetID=function()return id end,GetOwner=function()return pid end,
          GetX=function()return 12+id end,GetY=function()return 13 end,GetName=function()return 'City' end,
          GetBuildings=function()return buildings end,GetBuildQueue=function()return queue end}
        return function()return {Members=function()return ipairs({city})end,
          FindID=function(_,key)if key==id then return city end end,GetCapitalCity=function()return city end}end
      end
      Players[0].GetCities=playerCities(0,1,localPresent)
      Players[1]={IsHuman=function()return false end,GetCities=playerCities(1,2,foreignPresent)}
      Game.SetProperty=function()propertyWrites=propertyWrites+1;error('EXPERIMENT_WROTE_PERMANENT_STATE')end
      function send(packet)
        GameEvents.SPC_P0_Request.Fire(0,packet)
        assert(s.RequestIngress.action==packet.Action and s.RequestDepth==0 and s.FailureAt==nil)
        return s.Snapshot
      end
      function request(action,token)
        return send({Action=action,Token=token,CityID=1,Page=1})
      end
    """)
    return gp


def recover_and_request(root, revision=None):
    gp = fixture(root, revision)
    ui = context(root, revision, 'UI/BoostRefresh')
    ui.execute(NATIVE)
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
      assert(s.NetworkBoost.ready and not s.GreatWorkProbe.ready)
      assert(not localPresent[boostID] and not localPresent[cityWorkID] and localPresent[objectWorkID])
      assert(#changes==2 and localPresent[monumentID])
      rejectObject=false
    """)
    ui.execute("ExposedMembers.SPC_P0.NetworkBoost.ready=true;Events.GameCoreEventPlaybackComplete.Fire()")
    assert len(packets) == 2 and packets[1] == packets[0]
    gp.execute('send(...)', gp.table(packets[1]))
    gp.execute("""
      local s=ExposedMembers.SPC_P0
      assert(s.GreatWorkProbe.ready and not localPresent[objectWorkID] and #changes==3)
      Events.LoadScreenClose.Order({purchaseClose})
      Events.LoadScreenClose.Fire()
      Events.LoadScreenClose.Order(nil)
      assert(not localPresent[purchaseFixtureID] and not localPresent[purchaseDiscountID])
      assert(not foreignPresent[purchaseFixtureID] and not foreignPresent[purchaseDiscountID])
      assert(localPresent[monumentID] and foreignPresent[monumentID] and #changes==7)
      Events.LoadScreenClose.Order({purchaseClose})
      Events.LoadScreenClose.Fire()
      Events.LoadScreenClose.Order(nil)
      assert(#changes==7)
    """)
    ui.execute("ExposedMembers.SPC_P0.GreatWorkProbe.ready=true;Events.GameCoreEventPlaybackComplete.Fire()")
    assert len(packets) == 2
    reports = gp.execute("""
      local legacy=...
      local s=ExposedMembers.SPC_P0
      local gw=request('GW_READ','works')
      assert(s.LastToken=='works' and gw:find('旅游业绩限定路径',1,true),gw)
      local facts=request('GREAT_WORK_FACTS_DETAIL','facts')
      assert(s.LastToken=='facts' and #facts>0)
      assert(request('GW_BASELINE','baseline')==gw and s.LastToken=='baseline')
      local boost=request('BOOST_READ','boost')
      assert(s.LastToken=='boost' and #boost>0)
      local function retired(action)
        assert(request(action,action)==boost and s.LastToken=='boost' and #changes==7)
      end
      local gwActions={'GW_CITY','GW_OBJECT','GW_OFF'}
      local purchaseActions={'PURCHASE_BASE','PURCHASE_ON','PURCHASE_READ','PURCHASE_OFF'}
      for _,action in ipairs(gwActions) do
        if legacy then
          local result=request(action,action)
          assert(s.LastToken==action and result:find('B055 巨作接口对照',1,true))
          assert((localPresent[cityWorkID]==true)==(action=='GW_CITY'))
          assert((localPresent[objectWorkID]==true)==(action=='GW_OBJECT'))
        else retired(action) end
      end
      for _,action in ipairs(purchaseActions) do
        if legacy then
          local result=request(action,action)
          assert(s.LastToken==action and result:find('B053货币隔离实验',1,true))
          assert((localPresent[purchaseFixtureID]==true)==(action~='PURCHASE_OFF'))
          assert((localPresent[purchaseDiscountID]==true)==(action=='PURCHASE_ON' or action=='PURCHASE_READ'))
        else retired(action) end
      end
      if not legacy then
        for _,action in ipairs({'DIALOGUE_CARRIER_NEXT','INSPIRE_NEXT','INSPIRE_READ','INSPIRE_END',
                                'PROGRESSION_IMPORT','STANDARDIZATION_READ','RESEARCH_ON','RESEARCH_OFF'})do
          retired(action)
        end
      end
      assert(propertyWrites==0 and localPresent[monumentID] and foreignPresent[monumentID])
      assert(not localPresent[cityWorkID] and not localPresent[objectWorkID])
      assert(not localPresent[purchaseFixtureID] and not localPresent[purchaseDiscountID])
      return gw,facts,boost
    """, revision is not None)
    assert all(vm.load_counts['missing'] + vm.load_counts['failed'] == 0 for vm in (gp, ui))
    changes = [scalars(gp.globals().changes[i]) for i in range(1, len(gp.globals().changes) + 1)]
    return reports, changes[:7], len(changes) - 7


class LegacyPanelCleanup(unittest.TestCase):
    def test_all_retired_controls_were_hidden_and_retained_bindings_match(self):
        with package(B476) as previous:
            before, old_requests, old_events = panel(previous, legacy=True)
        after, requests, events = panel(ROOT)
        for control in RETIRED_CONTROLS:
            self.assertTrue(before.pop(control)[0], control)
            self.assertNotIn(control, after)
        self.assertEqual(before, after)
        self.assertEqual(requests, old_requests)
        for name in IDENTITY_EVENTS:
            self.assertEqual(old_events.pop(name), 1)
            self.assertNotIn(name, events)
        self.assertEqual(events, old_events)
        measure('legacy_panel_cleanup', dict(hidden_controls_removed=len(RETIRED_CONTROLS),
            retained_request_packets=len(requests), idle_identity_listeners_removed=len(IDENTITY_EVENTS)))

    def test_old_effect_commands_stop_and_both_saved_experiments_still_withdraw(self):
        with package(B476) as previous:
            before, old_cleanup, old_writes = recover_and_request(previous, B476)
        reports, cleanup, writes = recover_and_request(ROOT)
        self.assertEqual((reports, cleanup), (before, old_cleanup))
        self.assertEqual((old_writes, writes), (8, 0))
        measure('legacy_panel_effects', dict(manual_carrier_writes=[old_writes, writes],
            saved_carrier_removals=len(cleanup), b055_bounded_retry=True,
            ordinary_building_preserved=True, permanent_writes=[0, 0],
            retained_reports='MATCH', old_command_probes=15))
