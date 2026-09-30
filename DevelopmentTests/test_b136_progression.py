"""B136 bounded E2 integration; real current modules, fixture declarations only.

No historical wrapper, full suite, database, deployment, or engine execution.
The legacy E2 fixture supplies native objects; its governor mock is replaced by
real Probe.GovernorGate over six explicit native-shaped GetProperty values.
"""
from pathlib import Path
import argparse
import ast
from lupa.lua55 import LuaRuntime


def literal_execute(path):
    tree = ast.parse(path.read_text())
    return next(ast.literal_eval(node.value.args[0]) for node in tree.body
                if isinstance(node, ast.Expr)
                and isinstance(node.value, ast.Call)
                and isinstance(node.value.func, ast.Attribute)
                and node.value.func.attr == 'execute'
                and node.value.args
                and isinstance(node.value.args[0], ast.Constant)
                and isinstance(node.value.args[0].value, str)
                and 'local function event()' in node.value.args[0].value)


def run(root):
    mod = root / 'Mod'
    tests = root / 'DevelopmentTests'
    lua = LuaRuntime(unpack_returned_tuples=True)
    lua.globals().include = lambda name: lua.execute((mod / (name + '.lua')).read_text())
    lua.execute('print=function()end')  # Suppress expected legacy diagnostic chatter.
    for name in ['Probe', 'CityIdentityRead', 'CityProgressionStore', 'BindingProbe',
                 'CityJournalProbe', 'FreshBindingHook', 'CityFlowProbe',
                 'EffectiveFacts', 'InvestmentAction', 'NetworkInput']:
        lua.execute((mod / (name + '.lua')).read_text())
    source = (tests / 'test_p0_e1.py').read_text()
    lua.execute('M=SPCCityIdentityRead\n' + source[source.index('function fixture()'):source.index('function expect(')])
    fixture = literal_execute(tests / 'test_p0_e2.py').split("for _,kind in ipairs({'RESEARCH','CULTURE','INDUSTRY','COMMERCE'})do for level=1,4 do", 1)[0]
    old = "CityRoleFacts=function(c)return {owner=c:GetOwner(),cityID=c:GetID(),governorGateStatus='KNOWN',governorLevelCeiling=governor}end,"
    new = 'GovernorGate=SPCP0.GovernorGate,'
    assert fixture.count(old) == 1
    fixture = fixture.replace(old, new).replace("VERSION='B098.125'", 'VERSION=SPCP0.VERSION')
    old_getter = 'function c:GetProperty(k)for n,key in pairs(M.Keys)do'
    new_getter = '''function c:GetProperty(k)
 if k=='SPC_P0_GOV_CONTROL_A007' then return governor~=nil and 1 or nil end
 if k=='SPC_P0_GOV_PRESENT' or k=='SPC_P0_GOV_ESTABLISHED' then return governor and governor>=2 and 1 or 0 end
 for level=2,4 do if k=='SPC_P0_GOV_REQ_'..level then return governor and governor>=level and 1 or 0 end end
 for n,key in pairs(M.Keys)do'''
    assert fixture.count(old_getter) == 1
    fixture = fixture.replace(old_getter, new_getter)
    # Human/config eligibility is independently tested in the gate differential.
    # Here only that environment boundary is mocked; property reads and gate are real.
    lua.execute('SPCP0.IsTestPlayer=function(pid)return pid==0 end')
    lua.execute(fixture + '\nfunction setGovernor(level)governor=level end')
    lua.execute(r'''
function encode(v)
 if type(v)~='table'then return tostring(v)end
 local t={};for k,x in pairs(v)do t[#t+1]=tostring(k)..'='..encode(x)end
 table.sort(t);return '{'..table.concat(t,';')..'}'
end
function districts()
 if not d.testExit then
  d.RegisterExit('BoundedFixtureExit',function(city,loss)
   assert(d.IsExitTarget(city,loss));exitCalls=exitCalls+1
  end);d.testExit=true
 end
 Players[0].GetDistricts=function()return {Members=function()return ipairs({{
  GetCity=function()return c end,GetType=function()return s.values.JOURNAL.first.type end,
  GetID=function()return 99 end,IsComplete=function()return true end}})end}end
end
function lose()
 s.ref.owner=62;s.ref.cityID=40;Events.CityTransfered.Fire(62,40,0,7)
 assert(e2Record().stage=='HELD_TRANSFER')
end
function removed()Events.CityRemovedFromMap.Fire(62,40)end
function added()s.ref.owner=0;s.ref.cityID=88;Events.CityAddedToMap.Fire(0,88,4,5)end
function initialized()Events.CityInitialized.Fire(0,88,4,5)end
function transferred()Events.CityTransfered.Fire(0,88,62,0)end
function chain()removed();added();initialized();transferred()end
function held(kind)
 reset(3,kind);import();exitCalls=0;districts();lose()
 assert(exitCalls==1 and d.Status(c).exitStatus=='WITHDRAWN')
 s.values.TOKEN=nil;boot();districts()
 assert(not pcall(shared.EffectiveFacts.Read,0,c))
end
-- Actual import routing and all four identities, finite level cases (no pulses/stress).
for _,kind in ipairs({'RESEARCH','CULTURE','INDUSTRY','COMMERCE'})do
 for _,level in ipairs({1,2,4})do
  reset(level,kind)
  local before=shared.EffectiveFacts.Read(0,c);import();local after=shared.EffectiveFacts.Read(0,c)
  assert(encode(before)==encode(after))
  assert(fixtureStats().writes==2 and fixtureStats().cityWrites==0)
  import();boot();assert(fixtureStats().writes==2)
  assert(shared.EffectiveFacts.Read(0,c).potential==level)
  setGovernor(1);assert(shared.EffectiveFacts.Read(0,c).active==1)
 end
end
-- The real debit transaction, duplicate confirmation, preserved source, and recovery.
reset(2);import();local frozen=encode(s.values.INVEST);local token=prepare(12)
assert(a.Confirm(0,c,token):find('INVESTED'))
assert(shared.EffectiveFacts.Read(0,c).potential==3)
assert(fixtureStats().kills==1 and fixtureStats().writes==5 and fixtureStats().cityWrites==0)
assert(encode(s.values.INVEST)==frozen)
assert(a.Confirm(0,c,token):find('ALREADY_COMMITTED'))
assert(fixtureStats().kills==1 and fixtureStats().writes==5)
boot();assert(shared.EffectiveFacts.Read(0,c).potential==3 and fixtureStats().writes==5)
for _,offset in ipairs({1,2,3})do
 reset(1);import();local token=prepare(12);failFixtureWrite(offset)
 assert(a.Confirm(0,c,token):find('HELD'))
 local killed=fixtureStats().kills;failFixtureWrite(nil);boot()
 assert(fixtureStats().kills==killed)
 assert(shared.EffectiveFacts.Read(0,c).potential==(offset==3 and 2 or 1))
end
-- Foreign hydration and tokenless native transition; use current gate after return.
for _,kind in ipairs({'RESEARCH','CULTURE','INDUSTRY','COMMERCE'})do
 held(kind);local before=encode(e2Record())
 Events.CityAddedToMap.Fire(62,40,4,5);Events.CityInitialized.Fire(62,40,4,5)
 assert(encode(e2Record())==before and not pcall(shared.EffectiveFacts.Read,0,c))
 boot();districts();Events.CityInitialized.Fire(62,40,4,5);Events.CityAddedToMap.Fire(62,40,4,5)
 local retained=e2Record();setGovernor(1);chain();local accepted=e2Record()
 assert(accepted.stage=='ACTIVE',d.Status(c).observation)
 assert(encode(retained.base)==encode(accepted.base) and encode(retained.investment)==encode(accepted.investment))
 assert(s.values.TOKEN==nil and accepted.returnEvidence=='NATIVE_TRANSITION_V1')
 local f=shared.EffectiveFacts.Read(0,c)
 assert(f.specialization==kind and f.potential==3 and f.active==1 and f.cityID==88 and f.first.districtID==99)
 local frozen=encode(e2Record());f.first.districtID=999;f.token='MUTATED_RETURN'
 assert(encode(e2Record())==frozen and shared.EffectiveFacts.Read(0,c).first.districtID==99)
 local revision=accepted.revision;transferred();assert(e2Record().revision==revision)
 boot();districts();assert(shared.EffectiveFacts.Read(0,c).active==1 and s.values.TOKEN==nil)
 setGovernor(nil);assert(shared.EffectiveFacts.Read(0,c).activeStatus=='UNKNOWN_GOVERNOR')
 setGovernor(4);assert(shared.EffectiveFacts.Read(0,c).active==3)
 -- Continued investment after rebinding retains the historical receipt anchor.
 local token=prepare(51);assert(a.Confirm(0,c,token):find('INVESTED'))
 assert(shared.EffectiveFacts.Read(0,c).potential==4 and s.values.TOKEN==nil)
 assert(e2Record().investment.anchor.cityID==7 and e2Record().investment.anchor.first.districtID==3)
 boot();districts();assert(shared.EffectiveFacts.Read(0,c).potential==4)
end
-- Confirmed exit required; temporary object uncertainty and strict chain stay held.
held();local retained=encode(e2Record());local get=CityManager.GetCityAt
CityManager.GetCityAt=function()return nil end;d.ExitConfirmed();CityManager.GetCityAt=get
assert(encode(e2Record())==retained and not pcall(shared.EffectiveFacts.Read,0,c))
held();Events.CityAddedToMap.Fire(62,99,4,5);chain()
assert(e2Record().stage=='HELD_TRANSFER' and not pcall(shared.EffectiveFacts.Read,0,c))
held();removed();added();boot();districts();initialized();transferred()
assert(e2Record().stage=='HELD_TRANSFER' and not pcall(shared.EffectiveFacts.Read,0,c))
held();d.RegisterExit('InjectedFailure',function()error('EXIT_FAIL')end);d.ExitConfirmed();chain()
assert(e2Record().stage=='HELD_TRANSFER' and d.Status(c).returnRejection=='RETURN_WITHDRAWAL_UNCONFIRMED')
''')
    # A single current production Start / per-city V3 authority check complements
    # the legacy migration/return fixture above; no B108 scaling or lifecycle suite.
    current = LuaRuntime(unpack_returned_tuples=True)
    current.globals().include = lambda name: current.execute((mod / (name + '.lua')).read_text())
    current.execute('print=function()end')
    for name in ['Probe', 'CityIdentityRead', 'CityProgressionStore', 'BindingProbe',
                 'CompletionRecordProbe', 'CityJournalProbe', 'FreshBindingHook',
                 'CityFlowProbe', 'EffectiveFacts', 'InvestmentAction', 'NetworkInput']:
        current.execute((mod / (name + '.lua')).read_text())
    current.execute('SPCP0.IsTestPlayer=function(pid)return pid==0 end')
    current.execute('M=SPCCityIdentityRead\n' + source[source.index('function fixture()'):source.index('function expect(')])
    production = fixture.replace('SPCCityProgressionStore.StartLegacyTest(P,shared)', 'SPCCityProgressionStore.Start(P,shared)')
    production = production.replace('SPCBindingProbe.Start(P,shared);SPCCityJournalProbe',
                                    'SPCBindingProbe.Start(P,shared);SPCCompletionRecordProbe.Start(P,shared);SPCCityJournalProbe')
    b108 = (tests / 'test_b108_e2_multicity.py').read_text()
    helpers = b108.split("l.execute(h+r'''", 1)[1].split('-- Scale and write locality', 1)[0]
    current.execute(production + helpers + r'''
start();c=fresh(1);register(c);complete(c,'DISTRICT_CAMPUS');invest(c,901)
assert(d.UsesNewAuthority and record(c).stage=='ACTIVE')
local original=encode(record(c));local before=writes
local f=shared.EffectiveFacts.Read(0,c)
assert(f.potential==2 and f.active==2 and f.first.districtID==601)
f.first.districtID=999;f.token='BROKEN_COPY';f.potential=4
assert(encode(record(c))==original and shared.EffectiveFacts.Read(0,c).first.districtID==601)
governor=1;assert(shared.EffectiveFacts.Read(0,c).active==1)
governor=nil;assert(shared.EffectiveFacts.Read(0,c).activeStatus=='UNKNOWN_GOVERNOR')
governor=4;assert(shared.EffectiveFacts.Read(0,c).active==2)
saved=true;boot();assert(d.UsesNewAuthority and writes==before and encode(record(c))==original)
assert(shared.EffectiveFacts.Read(0,c).potential==2 and shared.EffectiveFacts.Read(0,c).active==2)
clean()
''')
    print('B136 E2 LOCAL_SIMULATION_PASS: 12 import/read/load comparisons; real debit/duplicate/failure recovery; four-kind confirmed exit, foreign hydration, tokenless return/current gate/read isolation/continued investment/coldload; strict held boundaries; one production V3 invested-city/current gate/read isolation/boot. No carrier-catalog/full-V3-lifecycle/engine certification.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    run(parser.parse_args().root)
