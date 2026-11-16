"""Retire the two legacy diagnostics while exercising the current player gate."""
import unittest

from refactor_harness import Context, PackageVFS, measure
from retired_crew_sources import B462, B463, package
from test_o7_crew_retirement import verify_package_round_trip
from test_o7_route_observer_retirement import exercise_proof
from test_p0_panel_current_layout import panel_runtime
from test_pu11_package_absence import NATIVE, scalars

MODULES = ('EligibilityProbe','QualificationProbe')
REMOVED = tuple(name+'.lua' for name in MODULES)
GLOBALS = tuple('SPC'+name for name in MODULES)
CONTROLS = ('QualificationButton','EligibilityUnknownButton','EligibilityButton')


def context(root, projected, name='Gameplay'):
    vfs=PackageVFS(manifest=root/'Mod/SpecializationP0.modinfo',forbidden_globals=GLOBALS if projected else ())
    history=(root,B463 if projected else B462)
    return Context(name=name,vfs=vfs,history=history)


def gate(root, projected):
    gp=context(root,projected)
    gp.execute(NATIVE)
    gp.execute("""
      rosterReads=0;traitScans=0;propertyWrites=0
      local set=Game.SetProperty
      Game.SetProperty=function(...)propertyWrites=propertyWrites+1;return set(...)end
      local america,roosevelt='CIVILIZATION_SPC_AMERICA','LEADER_SPC_T_ROOSEVELT'
      local scotland,bruce='CIVILIZATION_SPC_TEST','LEADER_SPC_TEST'
      local function slot(pid,civ,leader,human)
        local p={};for k,v in pairs(Players[0])do p[k]=v end
        p.IsHuman=function()return human end
        Players[pid]=p
        PlayerConfigurations[pid]={GetCivilizationTypeName=function()return civ end,GetLeaderTypeName=function()return leader end}
      end
      slot(1,scotland,bruce,true)
      slot(2,america,roosevelt,false)
      slot(3,america,bruce,true)
      slot(4,america,nil,true)
      PlayerManager={GetAliveIDs=function()rosterReads=rosterReads+1;return {0,1,2,3,4}end}
      local trait='TRAIT_CIVILIZATION_SPC_TEST'
      GameInfo.Traits={[trait]={TraitType=trait}}
      GameInfo.CivilizationTraits=function()
        traitScans=traitScans+1
        local rows={{CivilizationType=scotland,TraitType=trait}}
        local i=0;return function()i=i+1;return rows[i]end
      end
    """)
    gp.load('Gameplay')
    gp.execute("""
      local projected=...
      local shared=ExposedMembers.SPC_P0
      Events.LoadScreenClose.Fire();publish()
      for _,name in ipairs({'CityProgressionStore','ClaimProjects','EnvelopeProbe','NetworkBridge'})do
        assert(shared.StartStatus[name].state=='OK',name)
      end
      assert(shared.EnvelopeProbe.ready and shared.EnvelopeProbe.players[0] and shared.EnvelopeProbe.players[1])
      if projected then
        assert(shared.EligibilityProbe==nil and shared.QualificationProbe==nil)
        assert(shared.StartStatus.EligibilityProbe==nil and shared.StartStatus.QualificationProbe==nil)
      else
        local e,q=shared.EligibilityProbe,shared.QualificationProbe
        assert(e.samples.INITIALIZE.enabled==1 and e.samples.LOAD_CLOSE.enabled==1)
        assert(q.status=='COMPLETE_ROSTER' and q.permissions[1] and not q.permissions[0])
      end
      gateResults={}
      local function check(pid,want,state)
        local ok,message,status=SPCP0.IsTestPlayer(pid)
        assert(ok==want and status==state,tostring(pid)..':'..tostring(status))
        gateResults[#gateResults+1]={ok=ok,message=message,status=status}
      end
      check(0,true,'ELIGIBLE');check(1,true,'ELIGIBLE')
      check(2,false,'INELIGIBLE');check(3,false,'INELIGIBLE')
      check(4,false,'UNKNOWN');check(9,false,'UNKNOWN')
      GameConfiguration.IsAnyMultiplayer=function()return true end;check(0,false,'INELIGIBLE')
      GameConfiguration.IsAnyMultiplayer=function()error('MODE_UNKNOWN')end;check(0,false,'UNKNOWN')
      assert(gateResults[3].message=='AI玩家未启用' and gateResults[7].message=='多人模式未支持')
    """,projected)
    assert gp.load_counts['missing']+gp.load_counts['failed']==0
    return (scalars(gp.eval('gateResults')),scalars(gp.eval('properties')),gp.eval('propertyWrites'),
            gp.eval('rosterReads'),gp.eval('traitScans'),gp.eval('Events.LoadScreenClose.Count()'))


def routes(root, projected):
    gp,ui=context(root,projected),context(root,projected,'UI/BackgroundRoutes')
    packets=exercise_proof(gp,ui)
    for ctx in (gp,ui):
        assert ctx.load_counts['missing']+ctx.load_counts['failed']==0
    return packets,gp.load_counts,ui.load_counts


def panel(root):
    doc,ui=panel_runtime(root/'Mod/UI')
    controls=ui.globals().Controls
    buttons={n.get('ID'):controls[n.get('ID')].hidden for n in doc.iter('GridButton') if n.get('ID')}
    ui.execute("""
      Controls.SourceYieldButton.callbacks[Mouse.eLClick]()
      Controls.CityJournalButton.callbacks[Mouse.eLClick]()
      Controls.OpenButton.callbacks[Mouse.eRClick]()
      assert(#requests==3 and requests[1].Action=='PROGRESSION_READ' and requests[2].Action=='CITY_JOURNAL_READ'
        and requests[3].Action=='EVENT_ORDER_TOGGLE')
    """)
    return buttons,[dict(p.items()) for p in ui.globals().requests.values()]



class LegacyEligibilityRetirement(unittest.TestCase):
    def test_formal_gate_and_Envelope_load_read_match(self):
        with package(B462) as previous, package(B463) as retired:
            old,new=gate(previous,False),gate(retired,True)
            old_probe=(previous/'Mod/Probe.lua').read_bytes()
            self.assertEqual((retired/'Mod/Probe.lua').read_bytes(),old_probe.replace(b'P0-B-462.489',b'P0-B-463.490',1))
            for path in ('EnvelopeProbe.lua','CityProgressionStore.lua','ClaimProjects.lua','UI/BackgroundRoutes.lua'):
                self.assertEqual((retired/'Mod'/path).read_bytes(),(previous/'Mod'/path).read_bytes())
        self.assertEqual(old[:3],new[:3])
        self.assertEqual(len(new[0]),8)
        self.assertEqual((old[3],new[3]),(4,1))
        self.assertEqual((old[4],new[4]),(25,0))
        self.assertEqual(old[5]-new[5],2)
        measure('legacy_eligibility_retirement',{'matching_gate_cases':8,'modeled_roster_reads':[4,1],
            'modeled_trait_scans':[25,0],'modeled_load_listeners_removed':2,'modeled_writes_match':True})

    def test_three_hidden_reports_retire_with_other_requests_and_route_proof_retained(self):
        with package(B462) as previous, package(B463) as retired:
            old_route,new_route=routes(previous,False),routes(retired,True)
            old_buttons,old_requests=panel(previous)
            new_buttons,new_requests=panel(retired)
        self.assertEqual(old_route[0],new_route[0])
        self.assertEqual(len(new_route[0]),3)
        self.assertEqual(old_route[2],new_route[2])
        self.assertEqual(new_route[1],{**old_route[1],'attempts':old_route[1]['attempts']-2,
                                      'completed':old_route[1]['completed']-2})
        for control in CONTROLS:
            self.assertTrue(old_buttons.pop(control))
        self.assertEqual(new_buttons,old_buttons)
        self.assertEqual(new_requests,old_requests)
        measure('legacy_eligibility_routes',{'matching_route_packets':3,'other_P0_requests_match':True})

    def test_exact_temporary_switch_and_recovery(self):
        with package(B462) as previous, package(B463) as retired:
            verify_package_round_trip(self,previous/'Mod',retired/'Mod',REMOVED,'Probe.lua')
