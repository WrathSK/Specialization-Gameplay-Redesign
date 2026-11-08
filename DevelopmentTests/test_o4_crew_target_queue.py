"""Local proof of the real panel-to-Crew queue reader with two native doubles."""

from collections import deque
import unittest

from refactor_harness import measure
from retired_crew_sources import gameplay as historical_gameplay, package as historical_package, source as retired_source
from test_o6_production_panel import panel
from test_pu11_package_absence import NATIVE
from test_refactor_s7d5 import fixture as crew_transaction


UI_QUEUE = """
local id,x,y,turn,wonder,index=...
c.GetID=function()return id end
c.GetX=function()return x end
c.GetY=function()return y end
Game.GetCurrentGameTurn=function()return turn end
Players[0].GetCities=function()
 return {FindID=function(_,city)assert(city==id,'UNRELATED_CITY_READ');return c end,
  Members=function()error('CITY_ENUMERATION')end}
end
GameInfo.Buildings={[wonder]={Index=index,IsWonder=true}}
costReads,progressReads=0,0
local queue={}
function queue:GetCurrentProductionTypeHash()
 local hash=readNativeQueue()
 return forcedTarget or hash
end
function queue:GetBuildingCost(building)
 assert(building==index)
 costReads=costReads+1
 local _,cost=readNativeQueue()
 return cost
end
function queue:GetBuildingProgress(building)
 assert(building==index)
 progressReads=progressReads+1
 local _,_,progress=readNativeQueue()
 if changeDuringRead then forcedTarget=-1 end
 return progress
end
function queue:GetSize()error('QUEUE_ENUMERATION')end
function queue:GetAt()error('QUEUE_ENUMERATION')end
c.GetBuildQueue=function()return queue end
"""


def paired(hd=False):
    ui, _ = panel(hd)
    gameplay = crew_transaction()
    gameplay.execute("""
        q=c:GetBuildQueue()
        q.cost=250.5
        q.progress=100.25
        io=nil;os=nil;debug=nil;package=nil;require=nil
    """)
    identity = gameplay.eval("""function()
        local row=P.Info('Buildings',q.target)
        return c:GetID(),c:GetX(),c:GetY(),Game.GetCurrentGameTurn(),row.Hash,row.Index
    end""")
    native_queue = gameplay.eval("""function()
        local row=P.Info('Buildings',q.target)
        return row and row.Hash or -1,q.cost,q.progress
    end""")
    ui.globals().readNativeQueue = lambda: native_queue()
    ui.execute(UI_QUEUE, *identity())

    # Model ExposedMembers transport by copying only scalar response fields.
    def read_ui(pid, city, target, mode=None):
        reader = ui.globals().ExposedMembers.SPC_CrewTargetRead
        assert reader is not None, 'CREW_TARGET_SLOT_MISSING'
        row = dict(reader(pid, city, target, mode).items())
        assert all(isinstance(value, (bool, int, float, str)) for value in row.values())
        return gameplay.table_from(row)

    gameplay.globals().readUI = read_ui
    gameplay.execute("""
        ExposedMembers.SPC_CrewTargetRead=function(...)return readUI(...)end
        ExposedMembers.DLHD=nil
    """)
    return gameplay, ui


class OwnedConstructionQueue(unittest.TestCase):
    def test_retirement_preserves_one_debit_grant_and_receipt_on_both_panels(self):
        for hd in (False, True):
            results = []
            for mode in ('active', 'unavailable', 'removed'):
                with self.subTest(hd=hd, observer=mode):
                    gameplay, ui = paired(hd)
                    gameplay.execute('shared.ConstructionProbe=nil')
                    if mode != 'removed':
                        gameplay.execute(retired_source('ConstructionProbe.lua'))
                        gameplay.execute(retired_source('CrewPrecision.lua'))
                        gameplay.execute("""
                            if ...=='active'then
                                ExposedMembers.DLHD={Utils={
                                    GetCityCurrentBuildQueueCost=function()return q.cost end,
                                    GetCityCurrentBuildQueueProgress=function()return q.progress end}}
                            end
                            SPCConstructionProbe.Start(P,shared)
                            SPCCrewPrecision.Start(P,shared)
                        """, mode)
                    gameplay.execute("""
                        local mode=...
                        local writes,debits={},0
                        local set=P.SetProperty
                        P.SetProperty=function(o,k,v)
                            writes[#writes+1]=k
                            return set(o,k,v)
                        end
                        local get=Players[0].GetUnits
                        Players[0].GetUnits=function()
                            local units=get()
                            local destroy=units.Destroy
                            units.Destroy=function(...)
                                debits=debits+1
                                return destroy(...)
                            end
                            return units
                        end
                        assert(select(3,prepare()).status=='PREPARED')
                        local _,receipt,outcome=confirm()
                        assert(receipt==nil and outcome.status=='COMMITTED' and outcome.baseInput==150.25)
                        local observed=shared.CrewPrecision
                        if mode=='active'then
                            assert(observed.observed==150.25 and not observed.unitPresent)
                        elseif mode=='unavailable'then
                            assert(observed.error:find('HD_QUEUE_READ_HELPERS_UNAVAILABLE'))
                        else
                            assert(observed==nil and shared.ConstructionProbe==nil)
                        end
                        for i=1,4 do confirm()end
                        local _,r=next(C.props[SPCCrewModel.USE_RECEIPT_PROPERTY])
                        assert(r.state=='GRANT_RETURNED' and r.target=='BUILDING_WONDER_2')
                        assert(debits==1 and #q.adds==1 and q.adds[1]==150.25 and not C.units[20001] and C.calls==1)
                        result=T.encode({receipt=r,writes=writes,adds=q.adds,progress=q.progress,outcome=outcome})
                    """, mode)
                    ui.execute('assert(costReads==3 and progressReads==3 and #nativeOps==0 and #sent==0)')
                    results.append(gameplay.eval('result'))
            self.assertEqual(results, [results[0]] * 3)
        measure('O7c_crew_action_retirement', {'profiles': 2, 'observer_modes': 3,
                'unit_debits': 1, 'native_progress_grants': 1, 'clipped_fractional_input': 150.25,
                'same_receipt_write_order_outcome_and_progress': True})

    def test_real_panels_read_one_wonder_and_owner_debits_grants_once(self):
        for hd in (False, True):
            with self.subTest(hd=hd):
                gameplay, ui = paired(hd)
                gameplay.execute("""
                    shared.ConstructionProbe=nil
                    local text,_,prepared=prepare()
                    assert(prepared.status=='PREPARED',text)
                    local _,receipt,outcome=confirm()
                    assert(outcome.status=='COMMITTED' and receipt==nil)
                    assert(outcome.baseInput==150.25 and not C.units[20001] and #q.adds==1 and q.adds[1]==150.25)
                    local _,r=next(C.props[SPCCrewModel.USE_RECEIPT_PROPERTY])
                    assert(r and r.state=='GRANT_RETURNED' and r.amount==150 and r.target=='BUILDING_WONDER_2')
                    for i=1,4 do confirm()end
                    assert(#q.adds==1 and C.calls==1)
                """)
                ui.execute("""
                    assert(costReads==3 and progressReads==3)
                    for i=1,1000 do Events.GameCoreEventPublishComplete.Fire() end
                    assert(costReads==3 and progressReads==3 and #nativeOps==0 and #sent==0)
                """)
        measure('O4a_construction_reader', {'profiles': 2, 'stages': ['prepare', 'predebit', 'postdebit'],
                'cost_reads': 3, 'progress_reads': 3, 'idle_publishes': 1000, 'additional_idle_reads': 0,
                'unit_debits': 1, 'native_progress_grants': 1, 'clipped_fractional_input': 150.25})

    def test_mismatched_native_target_and_bad_response_hold_before_debit(self):
        for failure in (
            "ExposedMembers.SPC_CrewTargetRead=nil",
            "replaceResult=function(r)r.x=r.x+1 end",
            "replaceResult=function(r)r.turn=r.turn-1 end",
            "replaceResult=function(r)r.owner=1 end",
            "replaceResult=function(r)r.target=r.target+1 end",
            "replaceResult=function(r)r.cost=math.huge end",
            "replaceResult=function(r)r.progress=0/0 end",
            "replaceResult=function()ExposedMembers.SPC_CrewTargetRead=function()end end",
        ):
            with self.subTest(failure=failure):
                gameplay, _ = paired()
                gameplay.execute("""
                    assert(select(3,prepare()).status=='PREPARED')
                    local original=ExposedMembers.SPC_CrewTargetRead
                    ExposedMembers.SPC_CrewTargetRead=function(...)
                        local r=original(...)
                        replaceResult(r)
                        return r
                    end
                """ + failure + """
                    local _,_,outcome=confirm()
                    assert(outcome.status=='REJECTED' and outcome.phase=='PRECHECK')
                    assert(C.units[20001] and not C.props[SPCCrewModel.USE_RECEIPT_PROPERTY] and #q.adds==0)
                """)
        gameplay, ui = paired()
        gameplay.execute("assert(select(3,prepare()).status=='PREPARED')")
        ui.execute("changeDuringRead=true")
        gameplay.execute("""
            local _,_,outcome=confirm()
            assert(outcome.status=='REJECTED' and outcome.error:find('CREW_TARGET_CHANGED'))
            assert(C.units[20001] and not C.props[SPCCrewModel.USE_RECEIPT_PROPERTY] and #q.adds==0)
        """)

    def test_actual_changed_snapshot_after_debit_never_grants_or_replays(self):
        gameplay, ui = paired()
        gameplay.execute("""
            assert(select(3,prepare()).status=='PREPARED')
            local units=Players[0].GetUnits
            Players[0].GetUnits=function()
                local d=units()
                local destroy=d.Destroy
                d.Destroy=function(...)
                    destroy(...)
                    q.progress=q.progress+1
                end
                return d
            end
            local _,_,outcome=confirm()
            assert(outcome.status=='HELD' and outcome.error:find('TARGET_CHANGED_AFTER_DEBIT'))
            assert(not C.units[20001] and #q.adds==0)
            local _,r=next(C.props[SPCCrewModel.USE_RECEIPT_PROPERTY])
            assert(r and r.state=='INTENT')
            assert(select(3,confirm()).status=='REJECTED' and #q.adds==0)
        """)
        self.assertEqual(ui.eval('progressReads'), 3)

    def test_missing_probe_only_skips_the_actual_observer(self):
        with historical_package() as checkout:
            for behavior in ('throw', 'silent_nil'):
                with self.subTest(behavior=behavior):
                    ctx = historical_gameplay(checkout, absent=['ConstructionProbe'],
                        missing_include=behavior, forbidden_globals=['SPCConstructionProbe'])
                    ctx.loads = deque(maxlen=512)
                    ctx.execute(NATIVE)
                    ctx.load('Gameplay')
                    self.assertTrue(any(row['module']=='ConstructionProbe.lua' and row['status']=='ABSENT' for row in ctx.loads))
                    ctx.execute("""
                        local s=ExposedMembers.SPC_P0
                        assert(s.StartStatus.ConstructionProbe.state=='FAILED' and s.ConstructionProbe==nil)
                        assert(s.StartStatus.CrewPrecision.state=='SKIPPED_DEPENDENCY')
                        assert(s.StartStatus.UnitActions.state=='OK' and type(s.UnitActions.Run)=='function',
                            'FORMAL_ACTIONS_BLOCKED_BY_DEV_PROBE')
                        assert(s.StartStatus.PlayerActionReplies.state=='OK')
                    """)
