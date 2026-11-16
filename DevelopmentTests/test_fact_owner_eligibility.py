"""Real Probe eligibility and O2 responsibility consumers with engine doubles."""
import unittest

from refactor_harness import ROOT, legacy_source_observation
from test_investment_fact_responsibility import composition


def actual_eligibility():
    lua = composition()
    with legacy_source_observation():
        lua.globals().include('Probe')
    lua.execute("""
local oldGameConfiguration=GameConfiguration
GameConfiguration=setmetatable({IsAnyMultiplayer=function()
 if modeUnknown then return nil end;return false
end},{__index=oldGameConfiguration})
local player=Players[0]
player.IsHuman=function()
 if humanUnknown then return nil end;return true
end
local config={
 GetCivilizationTypeName=function()
  if configThrow then error('NATIVE_CONFIG_UNAVAILABLE')end
  if not configNil then return 'CIVILIZATION_SPC_AMERICA'end
 end,
 GetLeaderTypeName=function()return foreign and 'LEADER_FOREIGN'or 'LEADER_SPC_T_ROOSEVELT'end,
}
PlayerConfigurations={[0]=config}
P.IsTestPlayer=SPCP0.IsTestPlayer
function state()local okay,_,status=P.IsTestPlayer(0);return okay,status end
function allDuties()
 fc.Emit({owner=0,kinds={'NETWORK'},cause='TEST_VERIFIED'})
 deliver()
end
deliver();assert(fc.retained==0 and moneyCalls==0)
""")
    return lua


class FactOwnerEligibility(unittest.TestCase):
    def test_unknown_owner_keeps_all_three_tickets_without_idle_retry(self):
        for cause in ('configThrow', 'configNil', 'humanUnknown', 'modeUnknown'):
            with self.subTest(cause=cause):
                lua = actual_eligibility()
                lua.execute(f'{cause}=true')
                lua.execute("""
allDuties();assert(fc.retained==3 and moneyCalls==0,'UNKNOWN_OWNER_ACKED')
local eligible,status=state();assert(not eligible and status=='UNKNOWN')
local n=fc.delivered;for i=1,50 do deliver()end;assert(fc.delivered==n)
""")
                lua.execute(f'{cause}=false')
                lua.execute("""
allDuties();assert(fc.retained==0 and moneyCalls==0)
local eligible,status=state();assert(eligible and status=='ELIGIBLE')
""")

    def test_confirmed_foreign_owner_has_no_refresh_or_dormant_debt(self):
        lua = actual_eligibility()
        lua.execute("""
foreign=true
allDuties();assert(fc.retained==0 and moneyCalls==0)
local eligible,status=state();assert(not eligible and status=='INELIGIBLE')
""")

    def test_owner_unknown_global_cause_is_not_irrelevant(self):
        lua = actual_eligibility()
        lua.execute("""
configThrow=true
fc.Emit({kinds={'ACTIVE'},cause='TEST_GLOBAL_DIRTY'});deliver()
assert(fc.retained==2,'UNKNOWN_GLOBAL_SCOPE_ACKED')
configThrow=false
fc.Emit({kinds={'ACTIVE'},cause='TEST_GLOBAL_DIRTY'});deliver()
assert(fc.retained==0 and moneyCalls==0)
""")
