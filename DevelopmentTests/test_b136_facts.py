"""B136 targeted real-module differential; no game/DB/legacy-suite/deployment.

Run in the repository, or pass --repo explicitly:
 PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/tmp/spc-b069-python /opt/homebrew/bin/python3.14 DevelopmentTests/test_b136_facts.py
Requires Lua55/Lupa and Git baseline 34b92cc. Only a historical FIXTURE literal is
loaded via AST; its broad/version-specific wrapper is never executed.
"""
from pathlib import Path
import argparse
import ast
import hashlib
import json
import subprocess

from lupa.lua55 import LuaRuntime

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--repo', type=Path, default=(Path(__file__).resolve().parents[1]
    if Path(__file__).resolve().parent.name == 'DevelopmentTests' else Path.cwd()))
args = parser.parse_args()
ROOT = args.repo.resolve()
BASELINE = '34b92cc'
NAMES = ('Probe.lua', 'EffectiveFacts.lua', 'PerformanceCounters.lua',
         'NetworkInput.lua', 'NetworkBridge.lua')
CURRENT = {name: (ROOT / 'Mod' / name).read_text() for name in NAMES}
BASE = {name: subprocess.check_output(
    ['git', 'show', f'{BASELINE}:Mod/{name}'], cwd=ROOT, text=True) for name in NAMES}
BASELINE_COMMIT = subprocess.check_output(
    ['git', 'rev-parse', BASELINE], cwd=ROOT, text=True).strip()
assert 'function P.GovernorGate(city)' in CURRENT['Probe.lua'], 'B136 real scalar reader is absent'
assert 'P.GovernorGate(city)' in CURRENT['EffectiveFacts.lua'], 'EffectiveFacts must use real scalar reader'

SETUP = r'''
P=SPCP0;counts={};props={};badKey=nil;owner=0;id=7;mode='NORMAL';writes=0
function count(k) counts[k]=(counts[k] or 0)+1 end
P.Count=count
PlayerConfigurations={[0]={GetCivilizationTypeName=function() count('civ');return 'CIVILIZATION_SPC_TEST' end,
 GetLeaderTypeName=function() count('leader');return 'LEADER_SPC_TEST' end}}
GameConfiguration={IsAnyMultiplayer=function() count('multiplayer');return false end}
capital={GetID=function() count('capitalID');return 7 end,GetOwner=function() count('capitalOwner');return 0 end}
collection={GetCapitalCity=function() count('capital');return capital end}
Players={[0]={IsHuman=function() count('human');return true end,GetCities=function() count('cities');return collection end}}
city={GetOwner=function() count('owner');if mode=='OWNER_THROW' then error('no owner') end;return owner end,
 GetID=function() count('id');if mode=='ID_THROW' then error('no id') end;return id end,
 GetProperty=function(_,k) count(k);if k==badKey then error('unavailable') end;if k=='SPC_DEV_INVESTMENT_LEDGER_V1' then return ledger end;return props[k] end,
 SetProperty=function() writes=writes+1;error('WRITE_FORBIDDEN') end}
foundation={owner=0,cityID=7,token='T',specialization='RESEARCH',potential=1,first={districtID=3,type='DISTRICT_CAMPUS',nested={x=1}}}
ledger={schema=1,revision=4,anchor={owner=0,cityID=7,token='T',specialization='RESEARCH',first=foundation.first},investments={A='U1',B='U2',C='U3'}}
shared={CityFlowProbe={SupportFacts=function() return foundation end}}
SPCEffectiveFacts.Start(P,shared)
keys={'SPC_P0_GOV_CONTROL_A007','SPC_P0_GOV_PRESENT','SPC_P0_GOV_ESTABLISHED','SPC_P0_GOV_REQ_2','SPC_P0_GOV_REQ_3','SPC_P0_GOV_REQ_4'}
function resetProperties(n)
 props={};badKey=nil;mode='NORMAL';owner=0;id=7
 for _,key in ipairs(keys) do local v=n%3;n=math.floor(n/3);if v>0 then props[key]=v-1 end end
end
function outcome()
 local before=P.Encode(foundation);local ledgerBefore=P.Encode(ledger)
 local ok,v=pcall(shared.EffectiveFacts.Read,0,city)
 assert(P.Encode(foundation)==before and P.Encode(ledger)==ledgerBefore,'INPUT_MUTATION')
 assert(writes==0,'WRITE_OCCURRED')
 if ok then
  local encoded=P.Encode(v)
  assert(v~=foundation,'OUTPUT_ROOT_ALIAS')
  if type(foundation.first)=='table' then
   assert(v.first~=foundation.first,'OUTPUT_FIRST_ALIAS')
   if type(foundation.first.nested)=='table' then
    assert(v.first.nested~=foundation.first.nested,'OUTPUT_NESTED_ALIAS')
    v.first.nested.x=55;assert(P.Encode(foundation)==before,'OUTPUT_MUTATED_INPUT')
   end
  end
  return true,encoded
 end
 return false,tostring(v):gsub('^.-:%d+: ','')
end
function roles() return P.Encode(P.CityRoleFacts(city)) end
function gateProjection(useScalar)
 if useScalar then local o,i,s,c=P.GovernorGate(city);return P.Encode({owner=o,cityID=i,status=s,ceiling=c}) end
 local r=P.CityRoleFacts(city);return P.Encode({owner=r.owner,cityID=r.cityID,status=r.governorGateStatus,ceiling=r.governorLevelCeiling})
end
function focus()
 local ok,s=pcall(P.FocusProbe,city,'GOVERNOR',function() end)
 return ok,ok and s or tostring(s):gsub('^.-:%d+: ','')
end
function activeState()
 local f=shared.EffectiveFacts.Read(0,city)
 return f.potential,f.active,f.activeStatus,f.investmentPending,f.ledgerStatus
end
function setPotential(n)
 if n==0 then foundation.specialization='NONE';foundation.potential=0;foundation.first=nil;ledger=nil;return end
 foundation.specialization='RESEARCH';foundation.potential=1
 if n==1 then ledger=nil;return end
 ledger.investments={};for i=1,n-1 do ledger.investments['R'..i]='U'..i end;ledger.revision=n
end
function setPending(stage)
 ledger.pending={stage=stage,unitID=88,owner=0,cityUID='T',expectedRevision=ledger.revision,receipt='NEXT',unitUID='NEXT_UID'}
end
'''


def load_modules(source):
    lua = LuaRuntime(unpack_returned_tuples=True)
    lua.globals().include = lambda name: lua.execute(source[name + '.lua'])
    lua.execute(source['Probe.lua'])
    lua.execute(source['EffectiveFacts.lua'])
    return lua


def runtime(source):
    lua = load_modules(source)
    lua.execute(SETUP)
    return lua


def pair():
    return runtime(BASE), runtime(CURRENT)


def apply(runtimes, code):
    for lua in runtimes:
        lua.execute(code)


case_groups = {}

def differential(runtimes, label, group, diagnostics=True):
    base, current = runtimes
    if diagnostics:
        assert base.globals().roles() == current.globals().roles(), ('roles', label)
        assert base.globals().gateProjection(False) == current.globals().gateProjection(True), ('scalar', label)
        assert base.globals().focus() == current.globals().focus(), ('focus', label)
    result = base.globals().outcome()
    assert result == current.globals().outcome(), ('effective', label, result, current.globals().outcome())
    case_groups[group] = case_groups.get(group, 0) + 1
    return result


runtimes = pair()
for n in range(729):
    apply(runtimes, f'resetProperties({n})')
    differential(runtimes, n, 'six_property_nil_0_1')
    for lua in runtimes:
        lua.execute('counts={};outcome()')
        for key in lua.globals()["keys"].values():
            assert lua.globals().counts[key] == 1, (n, key)
for i in range(1, 7):
    for bad, value in [('string', "'1'"), ('boolean', 'true'), ('number', '2'), ('throw', None)]:
        apply(runtimes, 'resetProperties(728)')
        apply(runtimes, f'badKey=keys[{i}]' if bad == 'throw' else f'props[keys[{i}]]={value}')
        differential(runtimes, (i, bad), 'malformed_or_throwing_governor_property')
        for lua in runtimes:
            lua.execute('counts={};outcome()')
            for key in lua.globals()["keys"].values():
                assert lua.globals().counts[key] == 1, (i, bad, key)

original_errors = ["mode='OWNER_THROW'", "mode='ID_THROW'", 'owner=1', "id='7'",
    'ledger.anchor.extra=true', "ledger.anchor.token='BAD'", "ledger.investments.D='U3'",
    'ledger.revision=3', "ledger.pending={stage='INTENT'}"]
for code in original_errors:
    runtimes = pair();apply(runtimes, 'resetProperties(728);' + code)
    assert not differential(runtimes, code, 'original_identity_ledger_rejections')[0]

sequence = [
    ('KNOWN4', 'resetProperties(728)', (4, 4, 'KNOWN', False, 'PRESENT')),
    ('KNOWN1', 'props.SPC_P0_GOV_REQ_2=0;props.SPC_P0_GOV_REQ_3=0;props.SPC_P0_GOV_REQ_4=0', (4, 1, 'KNOWN', False, 'PRESENT')),
    ('UNKNOWN', 'props.SPC_P0_GOV_CONTROL_A007=nil', (4, None, 'UNKNOWN_GOVERNOR', False, 'PRESENT')),
    ('KNOWN3', 'props.SPC_P0_GOV_CONTROL_A007=1;props.SPC_P0_GOV_REQ_2=1;props.SPC_P0_GOV_REQ_3=1', (4, 3, 'KNOWN', False, 'PRESENT')),
    ('FOREIGN', 'owner=1', None),
    ('ORIGINAL', 'owner=0', (4, 3, 'KNOWN', False, 'PRESENT'))]
runtimes = pair()
for label, code, expected in sequence:
    apply(runtimes, code)
    result = differential(runtimes, label, 'same_instance_freshness')
    if expected is None:
        assert not result[0]
    else:
        assert result[0]
        for lua in runtimes:
            assert lua.globals().activeState() == expected, label

first_errors = [
    ('extra_ledger_first_key', 'ledger.anchor.first.extra=true'),
    ('missing_ledger_first_key', 'ledger.anchor.first.districtID=nil'),
    ('changed_ledger_first_value', 'ledger.anchor.first.districtID=99'),
    ('missing_nested_first_key', 'ledger.anchor.first.nested.x=nil'),
    ('extra_foundation_first_key', 'foundation.first.extra=true'),
    ('missing_foundation_first', 'foundation.first=nil')]
for label, code in first_errors:
    runtimes = pair()
    apply(runtimes, "resetProperties(728);ledger.anchor.first={districtID=3,type='DISTRICT_CAMPUS',nested={x=1}};" + code)
    assert not differential(runtimes, label, 'exact_first_identity_rejections')[0]
assert sum(case_groups.values()) == 774

for potential in range(5):
    for ceiling in (1, 2, 3, 4, None):
        runtimes = pair()
        apply(runtimes, f'resetProperties(728);setPotential({potential})')
        if ceiling is None:
            apply(runtimes, 'props.SPC_P0_GOV_CONTROL_A007=nil')
        else:
            apply(runtimes, ';'.join(f'props.SPC_P0_GOV_REQ_{n}={int(n <= ceiling)}' for n in (2, 3, 4)))
        assert differential(runtimes, (potential, ceiling), 'potential_0_through_4')[0]
        for lua in runtimes:
            state = lua.globals().activeState()
            expected_active = potential if potential <= 1 else min(potential, ceiling) if ceiling else None
            assert state[:3] == (potential, expected_active, 'UNKNOWN_GOVERNOR' if expected_active is None else 'KNOWN')
            lua.execute('counts={};outcome()')
            for key in lua.globals()["keys"].values():
                assert lua.globals().counts[key] == (1 if potential > 1 else None), (potential, key)

for stage in ('INTENT', 'CONSUMED_CONFIRMED'):
    for potential in (2, 3):
        for store_owned in (False, True):
            runtimes = pair()
            apply(runtimes, f"resetProperties(728);setPotential({potential});setPending('{stage}')")
            if store_owned:
                apply(runtimes, "shared.CityProgressionStore={Owns=function(c) assert(c==city);return true end,Investment=function(pid,c) assert(pid==0 and c==city);count('store_investment');return ledger end}")
            assert differential(runtimes, (stage, potential, store_owned), 'valid_pending_and_store_borrow')[0]
            for lua in runtimes:
                assert lua.globals().activeState()[3] is True
                lua.execute('counts={};outcome()')
                assert lua.globals().counts['SPC_DEV_INVESTMENT_LEDGER_V1'] == (None if store_owned else 1)
                assert lua.globals().counts['store_investment'] == (1 if store_owned else None)

extra_errors = [
    ('schema', 'ledger.schema=2', 'INVESTMENT_ANCHOR_CHANGED'),
    ('anchor_type', 'ledger.anchor=3', 'INVESTMENT_ANCHOR_CHANGED'),
    ('ledger_type', "ledger='bad'", 'INVESTMENT_ANCHOR_CHANGED'),
    ('investments_type', 'ledger.investments=false', 'INVESTMENT_LEDGER_INVALID'),
    ('empty_receipt', "ledger.investments['']='U9'", 'INVESTMENT_RECEIPT_INVALID'),
    ('bad_unit', 'ledger.investments.A=3', 'INVESTMENT_RECEIPT_INVALID'),
    ('too_many', "ledger.investments.D='U4'", 'INVESTMENT_CAP_EXCEEDED'),
    ('p0_conflict', "foundation.specialization='NONE';foundation.potential=0", 'UNASSIGNED_INVESTMENT_CONFLICT'),
    ('bad_foundation_owner', 'foundation.owner=1', 'EFFECTIVE_FOUNDATION_IDENTITY'),
    ('bad_foundation_city', 'foundation.cityID=8', 'EFFECTIVE_FOUNDATION_IDENTITY'),
    ('bad_foundation_token', 'foundation.token=nil', 'EFFECTIVE_FOUNDATION_IDENTITY'),
    ('bad_foundation_potential', 'foundation.potential=2', 'EFFECTIVE_FOUNDATION_INVALID'),
    ('bad_foundation_kind', "foundation.specialization='OTHER'", 'EFFECTIVE_FOUNDATION_INVALID'),
]
for label, code, expected in extra_errors:
    runtimes = pair();apply(runtimes, 'resetProperties(728);' + code)
    result = differential(runtimes, label, 'additional_corrupt_foundation_ledger')
    assert not result[0] and expected in result[1], (label, result)
for label, code in [
    ('stage', "ledger.pending.stage='OTHER'"), ('unit_negative', 'ledger.pending.unitID=-1'),
    ('unit_fraction', 'ledger.pending.unitID=1.5'), ('owner', 'ledger.pending.owner=1'),
    ('city_uid', "ledger.pending.cityUID='BAD'"), ('revision', 'ledger.pending.expectedRevision=8'),
    ('receipt_empty', "ledger.pending.receipt=''"), ('receipt_duplicate', "ledger.pending.receipt='R1'"),
    ('unit_duplicate', "ledger.pending.unitUID='U1'"), ('unit_empty', "ledger.pending.unitUID=''"),
    ('at_cap', 'setPotential(4);setPending("INTENT")')]:
    runtimes = pair();apply(runtimes, 'resetProperties(728);setPotential(2);setPending("INTENT");' + code)
    result = differential(runtimes, label, 'invalid_pending')
    assert not result[0] and 'INVESTMENT_PENDING_INVALID' in result[1]

# The same native facts, with real nonzero-player eligibility, remain accepted.
runtimes = pair()
apply(runtimes, "resetProperties(728);PlayerConfigurations[6]=PlayerConfigurations[0];Players[6]=Players[0];owner=6")
for lua in runtimes:
    assert lua.globals().P.IsTestPlayer(6) is True
assert runtimes[0].globals().gateProjection(False) == runtimes[1].globals().gateProjection(True)
case_groups['nonzero_player_scalar_identity'] = 1

# Cost boundary is getter count in a normal-capital fixture, never bytes/timing.
runtimes = pair();apply(runtimes, 'resetProperties(728);counts={};outcome()')
old_counts, new_counts = ({k: v for k, v in lua.globals().counts.items()} for lua in runtimes)
for key in runtimes[0].globals()["keys"].values():
    assert old_counts[key] == new_counts[key] == 1
removed = {key: old_counts[key] for key in old_counts if key not in new_counts}
assert removed == {'SPC_P0_FIRST_SPEC': 1, 'cities': 1, 'capital': 1, 'capitalID': 1, 'capitalOwner': 1}, removed
assert {k: v for k, v in old_counts.items() if k not in removed} == new_counts

# Pure native fixture only; real P/EffectiveFacts replace the old facts mock.
fixture_path = ROOT / 'DevelopmentTests/test_arch_v2_batch_a.py'
tree = ast.parse(fixture_path.read_text())
NETWORK_FIXTURE = ast.literal_eval(next(node.value for node in tree.body
    if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == 'FIXTURE' for t in node.targets)))
NETWORK_SETUP = r'''
cities[3]=nil;cities[4]=nil;cities[5]=nil
P=SPCP0;P.Count=function(k) counts[k]=(counts[k] or 0)+1 end
PlayerConfigurations={[0]={GetCivilizationTypeName=function() return 'CIVILIZATION_SPC_TEST' end,
 GetLeaderTypeName=function() return 'LEADER_SPC_TEST' end}}
GameConfiguration={IsAnyMultiplayer=function() return false end}
Players[0].IsHuman=function() return true end
for _,c in pairs(cities) do
 c.foundation={owner=0,cityID=c.id,token=c.token,specialization=c.kind,potential=1,
  first={districtID=c.id,type='DISTRICT_'..c.kind,nested={x=1}}}
 c.ledger={schema=1,revision=4,anchor={owner=0,cityID=c.id,token=c.token,specialization=c.kind,
  first=c.foundation.first},investments={A='U1',B='U2',C='U3'}}
 c.props={SPC_P0_GOV_CONTROL_A007=1,SPC_P0_GOV_PRESENT=1,SPC_P0_GOV_ESTABLISHED=1,
  SPC_P0_GOV_REQ_2=1,SPC_P0_GOV_REQ_3=1,SPC_P0_GOV_REQ_4=0}
 c.GetProperty=function(_,key)
  P.Count('native_property:'..key)
  if key=='SPC_DEV_BINDING_B013_TOKEN' then return c.token end
  if key=='SPC_DEV_INVESTMENT_LEDGER_V1' then return c.ledger end
  if key=='SPC_DEV_CITY_FLOW_B020' then return c.foundation end
  return c.props[key]
 end
 c.SetProperty=function() propertyWrites=propertyWrites+1;error('WRITE_FORBIDDEN') end
end
shared.CityFlowProbe={ready=true,SupportFacts=function(pid,c)
 assert(not readFail and not c.fail,'TEMP_FOUNDATION_READ');return c.foundation
end}
SPCEffectiveFacts.Start(P,shared)
local read=shared.EffectiveFacts.Read
shared.EffectiveFacts.Read=function(pid,c)
 local f,l=P.Encode(c.foundation),P.Encode(c.ledger)
 local ok,result=pcall(read,pid,c)
 assert(f==P.Encode(c.foundation) and l==P.Encode(c.ledger),'NETWORK_INPUT_MUTATION')
 if not ok then error(result) end
 assert(result~=c.foundation and result.first~=c.foundation.first and result.first.nested~=c.foundation.first.nested,'NETWORK_OUTPUT_ALIAS')
 return result
end
local capture=SPCNetworkInput.Capture
SPCNetworkInput.Capture=function(...) P.Count('capture_calls');return capture(...) end
function restartBridge()
 Events=events();GameEvents=events()
 SPCNetworkBridge.Start(P,shared);net=shared.NetworkBridge
 assert(not net.ready);Events.LoadScreenClose.Fire();assert(net.ready)
end
function networkSnapshot()
 assert(propertyWrites==0,'NETWORK_WRITE_OCCURRED')
 local ok,n=pcall(net.CurrentNational,0)
 local metadata=net.Input(0)
 return P.Encode({input=metadata,national=ok and n or 'UNAVAILABLE',ready=net.ready})
end
function networkState()
 local m=net.Input(0);local ok,n=pcall(net.CurrentNational,0)
 return m.inputVersion,m.validity,m.availability,ok and n.RESEARCH.level or nil,m.epoch
end
restartBridge()
'''


def network_runtime(source):
    lua = load_modules(source)
    lua.execute(NETWORK_FIXTURE)
    lua.execute(source['NetworkBridge.lua'])
    lua.execute(NETWORK_SETUP)
    return lua


nets = network_runtime(BASE), network_runtime(CURRENT)
network_steps = []

def network_step(label, code, expected):
    apply(nets, code)
    assert nets[0].globals().networkSnapshot() == nets[1].globals().networkSnapshot(), label
    for lua in nets:
        state = lua.globals().networkState()
        assert state == expected, (label, state, expected)
    network_steps.append(label)


network_step('initial_real_ACTIVE3', "send('0,1,0,2,10',1)", (1, 'VERIFIED', 'AVAILABLE', 3, 1))
network_step('same_route_same_turn_ACTIVE4', "counts={};cities[1].props.SPC_P0_GOV_REQ_4=1;send('0,1,0,2,10',1)", (2, 'VERIFIED', 'AVAILABLE', 4, 1))
for lua in nets:
    assert lua.globals().counts['capture_calls'] == 1 and lua.globals().counts['facts'] == 2
    assert lua.globals().counts['same_snapshot'] == 1 and lua.globals().counts['input_publication'] == 1
network_step('same_route_same_turn_ACTIVE1', "cities[1].props.SPC_P0_GOV_REQ_2=0;cities[1].props.SPC_P0_GOV_REQ_3=0;cities[1].props.SPC_P0_GOV_REQ_4=0;send('0,1,0,2,10',1)", (3, 'VERIFIED', 'AVAILABLE', 1, 1))
network_step('temporary_UNKNOWN_holds_matching_reference', "cities[1].props.SPC_P0_GOV_CONTROL_A007=nil;send('0,1,0,2,10',1)", (3, 'VERIFIED', 'NEEDS_REVALIDATION', 1, 1))
network_step('same_turn_recovery_ACTIVE3', "cities[1].props.SPC_P0_GOV_CONTROL_A007=1;cities[1].props.SPC_P0_GOV_REQ_2=1;cities[1].props.SPC_P0_GOV_REQ_3=1;send('0,1,0,2,10',1)", (4, 'VERIFIED', 'AVAILABLE', 3, 1))
network_step('known_foreign_owner_withdraws', 'cities[1].owner=1;net.Refresh(0)', (5, 'CONFIRMED_INVALID', 'UNAVAILABLE', None, 1))
network_step('original_owner_needs_current_packet', 'cities[1].owner=0;net.Refresh(0)', (5, 'CONFIRMED_INVALID', 'UNAVAILABLE', None, 1))
network_step('original_owner_current_packet_recovers', "send('0,1,0,2,10',1)", (6, 'VERIFIED', 'AVAILABLE', 3, 1))
network_step('UNKNOWN_changed_reference_withdraws', "cities[1].token='NEW_CITY1';cities[1].foundation.token='NEW_CITY1';cities[1].ledger.anchor.token='NEW_CITY1';cities[1].props.SPC_P0_GOV_CONTROL_A007=nil;net.Refresh(0)", (7, 'CONFIRMED_INVALID', 'UNAVAILABLE', None, 1))
network_step('UNKNOWN_new_reference_cannot_borrow_old', "send('0,1,0,2,10',1)", (7, 'CONFIRMED_INVALID', 'NEEDS_REVALIDATION', None, 1))
network_step('new_reference_fresh_known_recovers', "cities[1].props.SPC_P0_GOV_CONTROL_A007=1;send('0,1,0,2,10',1)", (8, 'VERIFIED', 'AVAILABLE', 3, 1))
network_step('restart_load_discards_previous_view', 'oldEpoch=net.epoch;restartBridge()', (0, 'UNKNOWN', 'UNAVAILABLE', None, 2))
network_step('old_epoch_packet_rejected', "net.Receive(0,{Epoch=oldEpoch,Seq=seq+10,Turn=turn,Signal=0,Valid=1,Count=1,Data='0,1,0,2,10'})", (0, 'UNKNOWN', 'UNAVAILABLE', None, 2))
network_step('load_UNKNOWN_has_no_old_view', "cities[1].props.SPC_P0_GOV_CONTROL_A007=nil;send('0,1,0,2,10',1)", (0, 'UNKNOWN', 'UNAVAILABLE', None, 2))
network_step('load_current_known_packet_rebuilds', "cities[1].props.SPC_P0_GOV_CONTROL_A007=1;send('0,1,0,2,10',1)", (1, 'VERIFIED', 'AVAILABLE', 3, 2))
case_groups['real_network_integration'] = len(network_steps)

for name, source in CURRENT.items():
    assert (ROOT / 'Mod' / name).read_text() == source, ('source_changed_during_test', name)
print(json.dumps({
    'status': 'LOCAL_SIMULATION_PASS', 'baseline_commit': BASELINE_COMMIT,
    'cases': sum(case_groups.values()), 'case_groups': case_groups,
    'same_instance_sequence': [s[0] for s in sequence], 'network_steps': network_steps,
    'six_governor_properties_per_eligible_read': 6, 'normal_capital_removed_getters': removed,
    'inputs': 'borrowed foundation/ledger unchanged, root/first/nested outputs isolated',
    'diagnostics': 'CityRoleFacts and FocusProbe equal; scalar identity/gate matches baseline role projection',
    'source_sha256': {name: hashlib.sha256(source.encode()).hexdigest() for name, source in CURRENT.items()},
    'limits': [
        'Native engine, CityFlow foundation and Investment ledger are fixtures, including Store read routing; this test does not execute the real Store or E2 lifecycle.',
        'Network integration executes real Probe, EffectiveFacts, NetworkInput and NetworkBridge; reload means new Bridge instance and real LoadScreenClose callback in a process-local fixture.',
        'No broad historical wrapper, stress, DB, game, deployment, GC operation, native allocation bytes, timing or process-memory attribution.'
    ]}, ensure_ascii=False, indent=2))
