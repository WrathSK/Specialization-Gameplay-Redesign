"""Native-shaped plot inputs through the actual production panel and Crew owners."""

from collections import deque
import unittest

from refactor_harness import legacy_source_observation, measure
from retired_crew_sources import B446, gameplay as historical_gameplay, package as historical_package
from test_o4_crew_target_queue import paired
from test_pu11_package_absence import NATIVE


GAMEPLAY = """
P.Count=function()end
C.rows.Districts=C.rows.Districts or {}
C.rows.Districts.DISTRICT_WONDER={Index=999}
c.GetName=function()return 'Wonder city' end
CityManager.GetDistrictAt=function()return nil end
unit=C.units[20001]
unit.x,unit.y=500,0
local function plot(id)
 return {GetIndex=function()return id end,GetOwner=function()return siteOwner or 0 end,
  GetDistrictType=function()return 999 end,
  GetWonderType=function()error('UNVERIFIED_GAMEPLAY_WONDER_READ')end,
  IsWonderComplete=function()error('UNVERIFIED_GAMEPLAY_COMPLETION_READ')end,
  GetProperty=function()error('HD_MARKER_READ')end}
end
gameplayPlots={[500]=plot(500),[501]=plot(501)}
Map={GetPlot=function(x)return gameplayPlots[x]end,
 GetPlotByIndex=function(i)return gameplayPlots[i]end,
 GetCityPlots=function()error('UNVERIFIED_GAMEPLAY_PLOT_LIST')end}
Cities={GetPlotPurchaseCity=function(p)
 if wrongPurchase then return {GetOwner=function()return 1 end}end
 return c
end}
function targets()
 return shared.UnitTargets.Refresh(0,{UnitID=20001,Token='MARKER'})
end
function currentSite()
 return shared.UnitTargets.ReadAtSite(0,{UnitID=20001,Token='SITE'})
end
"""


UI_SITE = """
local _,row=next(GameInfo.Buildings)
GameInfo.Districts={DISTRICT_WONDER={Index=999}}
plotVisits,plotReads=0,0
purchased={500,500,501,502}
plots={}
for _,id in ipairs({500,501,502})do
 local p={id=id,owner=0,kind=id==502 and 2 or 999,wonder=id==500 and row.Index or row.Index+1,complete=false}
 function p:GetIndex()return self.id end
 function p:GetOwner()return self.owner end
 function p:GetDistrictType()return self.kind end
 function p:GetWonderType()assert(self.kind==999,'ORDINARY_PLOT_READ');return self.wonder end
 function p:IsWonderComplete()return self.complete end
 plots[id]=p
end
Map={GetCityPlots=function()
 return {GetPurchasedPlots=function(_,city)
  assert(city==c)
  plotReads=plotReads+1
  return purchased
 end}
end,
GetPlotByIndex=function(id)
 plotVisits=plotVisits+1
 return plots[id]
end}
Cities={GetPlotPurchaseCity=function(p)
 if p.foreignCity then return {GetOwner=function()return 0 end,GetID=function()return c:GetID()+1 end}end
 return c
end}
"""


def action_site(hd=False):
    gameplay, ui = paired(hd)
    gameplay.execute(GAMEPLAY)
    with legacy_source_observation():
        gameplay.globals().include('UnitTargets')
    gameplay.execute("SPCUnitTargets.Start(P,shared);shared.ConstructionProbe=nil")
    ui.execute(UI_SITE)
    return gameplay, ui


class OwnedWonderLocation(unittest.TestCase):
    def test_native_location_connects_markers_and_the_real_transaction_in_both_profiles(self):
        for hd in (False, True):
            with self.subTest(hd=hd):
                gameplay, ui = action_site(hd)
                gameplay.execute("""
                    unit.x=499
                    local r=targets()
                    assert(#r.plots==1 and r.plots[1].plot==500 and #r.unknown==0,'NATIVE_WONDER_MARKER_MISSING')
                    unit.x=500
                    local text,_,preview=prepare()
                    assert(preview.status=='PREPARED',text)
                    local _,_,result=confirm()
                    assert(result.status=='COMMITTED' and result.baseInput==150.25 and #q.adds==1 and not C.units[20001])
                    assert(shared.UnitTargetSnapshot.token=='MARKER')
                    assert(select(3,confirm()).status=='REJECTED' and #q.adds==1)
                """)
                ui.execute("""
                    assert(plotReads==3 and plotVisits==12 and costReads==3 and progressReads==3)
                    for i=1,1000 do Events.GameCoreEventPublishComplete.Fire()end
                    assert(plotReads==3 and plotVisits==12 and costReads==3 and progressReads==3)
                """)
        measure('O4b_native_wonder_site', {'profiles': 2, 'city_plot_lists': 3,
                'plot_entries_visited': 12, 'actions': ['marker', 'prepare', 'confirm'],
                'native_progress_calls': 1, 'extra_site_reads_after_debit': 0, 'extra_idle_reads': 0})

    def test_wrong_complete_foreign_ambiguous_or_malformed_location_never_consumes(self):
        for fault in (
            "plots[500].complete=true",
            "plots[500].wonder=plots[500].wonder+1",
            "plots[500].owner=1",
            "plots[500].foreignCity=true",
            "plots[501].wonder=plots[500].wonder",
            "purchased=nil",
            "purchased={500,'INVALID_PLOT_INDEX'}",
        ):
            with self.subTest(fault=fault):
                gameplay, ui = action_site()
                gameplay.execute("assert(#currentSite().plots==1)")
                ui.execute(fault)
                gameplay.execute("""
                    local r=currentSite()
                    assert(#r.plots==0 and #r.unknown==1)
                    assert(select(3,prepare()).status=='REJECTED')
                    assert(C.units[20001] and #q.adds==0 and not C.props[SPCCrewModel.USE_RECEIPT_PROPERTY])
                """)

    def test_gameplay_rechecks_plot_ownership_and_city_after_a_ui_reply(self):
        for fault in (
            "siteOwner=2",
            "wrongPurchase=true",
            "gameplayPlots[r.plot]=nil",
            "q.target='BUILDING_A'",
            "r.turn=r.turn+1",
        ):
            with self.subTest(fault=fault):
                gameplay, _ = action_site()
                gameplay.execute("""
                    assert(select(3,prepare()).status=='PREPARED')
                    local original=ExposedMembers.SPC_CrewTargetRead
                    ExposedMembers.SPC_CrewTargetRead=function(...)
                        local r=original(...)
                """ + fault + """
                        return r
                    end
                    assert(select(3,confirm()).status=='REJECTED')
                    assert(C.units[20001] and #q.adds==0 and not C.props[SPCCrewModel.USE_RECEIPT_PROPERTY])
                """)

    def test_formal_target_owner_starts_without_dev_site_probe_file(self):
        with historical_package(B446) as checkout:
            for behavior in ('throw', 'silent_nil'):
                with self.subTest(behavior=behavior):
                    ctx = historical_gameplay(checkout, revision=B446, absent=['UnitSiteProbe'],
                        missing_include=behavior, forbidden_globals=['SPCUnitSiteProbe'])
                    ctx.loads = deque(maxlen=512)
                    ctx.execute(NATIVE)
                    ctx.load('Gameplay')
                    self.assertTrue(any(row['module']=='UnitSiteProbe.lua' and row['status']=='ABSENT' for row in ctx.loads))
                    ctx.execute("""
                        local s=ExposedMembers.SPC_P0
                        assert(s.StartStatus.UnitSiteProbe.state=='FAILED' and s.UnitSiteProbe==nil)
                        assert(s.StartStatus.UnitTargets.state=='OK' and type(s.UnitTargets.ReadAtSite)=='function',
                            'FORMAL_TARGETS_BLOCKED_BY_DEV_SITE_PROBE')
                        assert(s.StartStatus.UnitActions.state=='OK')
                    """)
