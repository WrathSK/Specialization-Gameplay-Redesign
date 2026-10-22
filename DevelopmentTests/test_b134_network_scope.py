"""Bounded B134 NetworkBridge scope probe; no repo/game writes or broad suites.

Uses the existing Lua55/Lupa install and only the frozen A fixture literal.
Compares B133 to the current source; reads Git history and the existing fixture only.
"""
from pathlib import Path
import ast
import subprocess
import sys
from lupa.lua55 import LuaRuntime

ROOT = Path(__file__).resolve().parents[1]
MOD = ROOT / 'Mod'
BASELINE = subprocess.check_output(
    ['git', 'show', 'd50029a:Mod/NetworkBridge.lua'], cwd=ROOT, text=True)
OLD_EVENT_BLOCK = """ for _,name in ipairs({'PlayerTurnActivated','GovernorAssigned','GovernorChanged','GovernorEstablished','GovernorPromoted','CapitalCityChanged','CityAddedToMap'}) do
  local ev=P.Field(Events,name);if ev and ev.Add then ev.Add(d.Rebuild) end
 end"""
NEW_EVENT_BLOCK = """ -- These events identify the affected player in their first native argument.
 -- Keep every local notification, including repeated ones within the same turn.
 local function rebuildPlayer(pid)
  if integer(pid) then d.Refresh(pid) else d.Rebuild() end
 end
 for _,name in ipairs({'PlayerTurnActivated','GovernorChanged','GovernorPromoted'}) do
  local ev=P.Field(Events,name);if ev and ev.Add then ev.Add(rebuildPlayer) end
 end
 -- Assignment/establishment carry both city owner and governor owner; retain the
 -- existing full safety scope, including cross-owner governor assignments.
 for _,name in ipairs({'GovernorAssigned','GovernorEstablished','CapitalCityChanged','CityAddedToMap'}) do
  local ev=P.Field(Events,name);if ev and ev.Add then ev.Add(d.Rebuild) end
 end"""
assert BASELINE.count(OLD_EVENT_BLOCK) == 1
CANDIDATE = (MOD / 'NetworkBridge.lua').read_text()
fixture_tree = ast.parse((ROOT / 'DevelopmentTests/test_arch_v2_batch_a.py').read_text())
FIXTURE = ast.literal_eval(next(
    node.value for node in fixture_tree.body if isinstance(node, ast.Assign)
    and any(isinstance(target, ast.Name) and target.id == 'FIXTURE' for target in node.targets)))


def runtime(source):
    lua = LuaRuntime(unpack_returned_tuples=True)
    lua.globals().include = lambda name: lua.execute((MOD / (name + '.lua')).read_text())
    lua.execute(FIXTURE)
    lua.execute(source)
    lua.execute("""
      SPCNetworkBridge.Start(P,shared);net=shared.NetworkBridge;net.ready=true
      send('0,1,0,2,10;0,2,0,3,11;0,4,0,2,12',3)
      assert(net.CurrentNational(0).RESEARCH.level==3)
      function resetScans() counts.city_scan=0 end
    """)
    return lua


results = {}
for label, source in [('baseline', BASELINE), ('candidate', CANDIDATE)]:
    lua = runtime(source)
    observed = {}
    lua.execute("""
      resetScans();local before=net.Input(0).inputVersion
      for pid=1,12 do
       Events.PlayerTurnActivated.Fire(pid,true)
       Events.GovernorChanged.Fire(pid,2)
       Events.GovernorPromoted.Fire(pid,2,7)
      end
      assert(net.Input(0).inputVersion==before)
    """)
    observed['36_known_foreign_events_city_visits'] = lua.eval('counts.city_scan')
    lua.execute("""
      resetScans()
      for _,name in ipairs({'PlayerTurnActivated','GovernorChanged','GovernorPromoted'}) do
       cities[1].active=4;Events[name].Fire(0,2,7)
       assert(net.CurrentNational(0).RESEARCH.level==4)
       cities[1].active=2;Events[name].Fire(0,2,7)
       assert(net.CurrentNational(0).RESEARCH.level==2)
      end
    """)
    observed['six_same_turn_local_changes_city_visits'] = lua.eval('counts.city_scan')
    lua.execute("""
      resetScans();local before=net.Input(0).inputVersion
      Events.PlayerTurnActivated.Fire(0,true);Events.PlayerTurnActivated.Fire(0,false)
      assert(net.Input(0).inputVersion==before)
    """)
    observed['two_same_state_local_turns_city_visits'] = lua.eval('counts.city_scan')
    lua.execute("""
      resetScans()
      for _,name in ipairs({'PlayerTurnActivated','GovernorChanged','GovernorPromoted'}) do
       Events[name].Fire();Events[name].Fire(-1);Events[name].Fire(0.5)
       Events[name].Fire(math.huge);Events[name].Fire('0')
      end
    """)
    observed['15_unknown_or_invalid_events_city_visits'] = lua.eval('counts.city_scan')
    lua.execute("""
      resetScans()
      -- Native assignment/establishment: cityOwner,cityID,governorOwner,governorID.
      -- Keep full scope even if the city owner is foreign and governor owner local.
      cities[1].active=4;Events.GovernorAssigned.Fire(9,17,0,2)
      assert(net.CurrentNational(0).RESEARCH.level==4)
      cities[1].active=2;Events.GovernorEstablished.Fire(9,17,0,2)
      assert(net.CurrentNational(0).RESEARCH.level==2)
      cities[1].active=3;Events.GovernorAssigned.Fire(9,17,8,2)
      assert(net.CurrentNational(0).RESEARCH.level==3)
      cities[1].active=4;Events.GovernorEstablished.Fire(9,17,8,2)
      assert(net.CurrentNational(0).RESEARCH.level==4)
    """)
    observed['four_assignment_establishment_full_scope_visits'] = lua.eval('counts.city_scan')
    lua.execute("""
      -- Complete player capture must observe source and recipient/capital changes.
      cities[1].active=3;cities[4].active=4;Events.GovernorChanged.Fire(0,2)
      assert(net.CurrentNational(0).RESEARCH.level==3)
      assert(net.CurrentNational(0).CULTURE.level==4)
      capitalID=3;Events.CapitalCityChanged.Fire(0)
      assert(net.players[0].input.capital==3)
      capitalID=1;Events.CityAddedToMap.Fire(0,1)
      assert(net.players[0].input.capital==1)
      -- Missing/unknown facts hold the accepted complete national view.
      local previous=net.Input(0).inputVersion
      cities[1].active=nil;Events.GovernorChanged.Fire(0,2)
      assert(net.Input(0).inputVersion==previous and net.CurrentNational(0).RESEARCH.level==3)
      cities[1].active=3;readFail=true;Events.GovernorPromoted.Fire(0,2,7)
      assert(net.Input(0).inputVersion==previous and net.CurrentNational(0).RESEARCH.level==3)
      readFail=false;Events.GovernorChanged.Fire(0,2)
      -- Confirmed owner loss still withdraws; fresh valid packet restores current input.
      cities[1].owner=9;Events.CityTransfered.Fire(0,9,1)
      assert(net.Input(0).validity=='CONFIRMED_INVALID')
      cities[1].owner=0;send('0,1,0,2,10;0,2,0,3,11;0,4,0,2,12',3)
      assert(net.CurrentNational(0).RESEARCH.level==3)
      -- Existing independent route/unit invalidation stays active.
      units[10]=nil;Events.UnitRemovedFromMap.Fire(0,10)
      assert(net.Input(0).validity=='CONFIRMED_INVALID')
      -- Save/load creates a new session epoch; no saved route view or old sample replay.
      local oldEpoch=net.epoch
      SPCNetworkBridge.Start(P,shared);net=shared.NetworkBridge;net.ready=true
      net.Receive(0,{Epoch=oldEpoch,Seq=10000,Turn=turn,Signal=0,Valid=1,Count=0,Data=''})
      assert(net.Input(0).validity=='UNKNOWN' and net.Input(0).inputVersion==0)
      send('',0);assert(net.Input(0).validity=='VERIFIED')
      assert(propertyWrites==0)
    """)
    results[label] = observed

expected_common = {
    'six_same_turn_local_changes_city_visits': 30,
    'two_same_state_local_turns_city_visits': 10,
    '15_unknown_or_invalid_events_city_visits': 75,
    'four_assignment_establishment_full_scope_visits': 20,
}
for label in results:
    for key, value in expected_common.items():
        assert results[label][key] == value, (label, key, results[label][key], value)
assert results['baseline']['36_known_foreign_events_city_visits'] == 180
assert results['candidate']['36_known_foreign_events_city_visits'] == 0
for label, result in results.items():
    print(label, result)
print('PASS: three-event owner scope only; unchanged local/same-turn/fallback/assignment behavior; '
      'complete national capture, UNKNOWN hold, owner withdrawal/return and unit invalidation; no property writes')
