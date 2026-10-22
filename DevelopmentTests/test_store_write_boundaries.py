"""Store write-boundary L3 tests: actual Lua, frozen-baseline value comparison.

No native CPU/memory or save-file claim. Test-only source instrumentation exposes
private storage for malformed/readback counterexamples and counts iterations over
its committed record table; production code receives no diagnostic API. Normal
age/investment/template/lifecycle cases use public Store/consumer APIs.
Requires lupa.lua55 and the pre-repair Git object below; no external DB/runtime.
"""
from pathlib import Path
import ast
import subprocess
import unittest

from lupa.lua55 import LuaRuntime

R = Path(__file__).resolve().parents[1]
BASELINE = "cdd3ceb8b401c5cbe4d58cbbdbc7998b1edddeb7"
MODULES = ["CityIdentityRead", "CityProgressionStore", "BindingProbe", "CompletionRecordProbe",
           "CityJournalProbe", "FreshBindingHook", "CityFlowProbe", "EffectiveFacts", "InvestmentAction"]


def instrument_store(source):
    marker = "local w=CreateProgressionRecord(P,shared,storage)"
    assert source.count(marker) == 1, "private storage test seam changed"
    assert "for other,r in pairs(envelope.records)do" in source, "uniqueness loop test seam changed"
    source = source.replace(marker, "__store_storage[token]=storage;__store_snapshot[token]=function()return cp(envelope.records[token])end;" + marker)
    # The counter records every returned record, including the target (same audit
    # denominator as the old N*T loop), never nested copies/validation/native work.
    return source.replace("pairs(envelope.records)", "__store_pairs(envelope.records)")


def fixture(source=None):
    lua = LuaRuntime(unpack_returned_tuples=True)
    lua.globals().print = lambda *parts: None  # Expected injected hold diagnostics stay out of the summary.
    lua.globals().include = lambda name: lua.execute((R / "Mod" / (name + ".lua")).read_text())
    lua.execute("""
__store_storage={}; __store_snapshot={}; __store_visits=0
function __store_pairs(t)
 local key
 return function()
  key=next(t,key);if key~=nil then __store_visits=__store_visits+1;return key,t[key]end
 end
end
""")
    for name in MODULES:
        text = (R / "Mod" / (name + ".lua")).read_text()
        lua.execute(instrument_store(source or text) if name == "CityProgressionStore" else text)
    e1 = (R / "DevelopmentTests/test_p0_e1.py").read_text()
    lua.execute("M=SPCCityIdentityRead\n" + e1[e1.index("function fixture()"):e1.index("function expect(")])
    e2 = (R / "DevelopmentTests/test_p0_e2.py").read_text()
    base = e2[e2.index("local function event()"):e2.index("for _,kind in ipairs({'RESEARCH'")]
    base = base.replace("SPCCityProgressionStore.StartLegacyTest(P,shared)", "SPCCityProgressionStore.Start(P,shared)")
    base = base.replace("SPCBindingProbe.Start(P,shared);SPCCityJournalProbe", "SPCBindingProbe.Start(P,shared);SPCCompletionRecordProbe.Start(P,shared);SPCCityJournalProbe")
    base = base.replace("CityRoleFacts=function(c)return {owner=c:GetOwner(),cityID=c:GetID(),governorGateStatus='KNOWN',governorLevelCeiling=governor}end,", "GovernorGate=function(c)return c:GetOwner(),c:GetID(),'KNOWN',governor end,")
    b108 = (R / "DevelopmentTests/test_b108_e2_multicity.py").read_text()
    helpers = b108[b108.index("local INDEX=SPCCityProgressionStore.INDEX"):b108.index("-- Scale and write locality")]
    # Counters and private storage captures are reset at a simulated VM boot.
    base = base.replace("function boot()", "function boot()\n __store_storage={};__store_snapshot={}")
    ai_source = (R / "DevelopmentTests/test_b111_district_snapshot.py").read_text()
    acquisition = ai_source.split("cases=r" + chr(39)*3, 1)[1].split("-- One candidate", 1)[0]
    lua.execute(base + helpers + acquisition + r'''
T={}
T.ai=ai;T.district=district;T.take=take
T.start=start;T.fresh=fresh;T.register=register;T.complete=complete;T.invest=invest
T.record=record;T.encode=encode;T.clean=clean;T.boot=boot
function T.props()return props end
function T.writes()return writes end
function T.key(c)return PREFIX..c.s.values.TOKEN end
function T.storage(c)return assert(__store_storage[c.s.values.TOKEN])end
function T.snapshot(c)return __store_snapshot[c.s.values.TOKEN]()end
function T.reload()saved=true;boot()end
function T.turn(n)turn=turn+n;Events.PlayerTurnActivated.Fire(0)end
function T.now()return turn end
function T.scanReset()__store_visits=0 end
function T.scanCount()return __store_visits end
function T.control(c)return shared.EffectiveFacts.Read(0,c)end
function T.failKey(key)failKey=key end
function T.propsSet(key,value)props[key]=M.Copy(value)end
function T.index()return props[INDEX]end
function T.setter(value)Game.SetProperty=value end
function T.getter(value)Game.GetProperty=value end
function T.governor(value)governor=value end
function T.research(i)
 local c=fresh(i);register(c);complete(c,'DISTRICT_CAMPUS')
 for j=1,3 do invest(c,10000+i*10+j)end;return c
end
function T.two()
 start();local x=fresh(1);register(x);complete(x,'DISTRICT_CAMPUS')
 local y=fresh(2);register(y);complete(y,'DISTRICT_THEATER');return x,y
end
function T.change(r,owner,id)
 local n=M.Copy(r);n.stage='HELD_TRANSFER';n.revision=n.revision+1
 n.loss={origin=M.Copy(n.origin),target={owner=owner,cityID=id,x=n.origin.x,y=n.origin.y},evidence='CityTransfered+live_reference'}
 return n
end
function T.normal(r)local n=M.Copy(r);n.revision=n.revision+1;return n end
function T.write(c,value)
 local s=T.storage(c);return pcall(s.Write,s.Read(),value)
end
function T.structural(c,owner,id)return T.write(c,T.change(T.storage(c).Read(),owner,id))end
function T.tryRegister(i,owner,id)
 local c=fresh(i,owner);if id then c.s.ref.cityID=id end
 local before=writes;register(c);return c,record(c)~=nil,writes-before
end
function T.loss(c,owner,id)
 c.s.ref.owner=owner;c.s.ref.cityID=id;Events.CityTransfered.Fire(owner,id,0)
end
''')
    return lua


def baseline_source():
    return subprocess.check_output(["git", "show", BASELINE + ":Mod/CityProgressionStore.lua"], cwd=R, text=True)


def legacy_extension(name):
    tree = ast.parse((R / "DevelopmentTests" / name).read_text())
    return next(ast.literal_eval(node.value) for node in tree.body
                if isinstance(node, ast.Assign)
                and any(isinstance(target, ast.Name) and target.id == "extra" for target in node.targets))


def run_claim_return_regression(body):
    # Reuse the maintained B140 fixture adaptation only. Do not run its full body
    # or historical package-version assertions and do not change old test files.
    path = R / "DevelopmentTests/test_b140_templates.py"
    source = path.read_text()
    namespace = {"__file__": str(path)}
    exec(compile(source[:source.index("extra=r" + chr(39)*3)], str(path), "exec"), namespace)
    header = namespace["header"].replace("l=LuaRuntime()", "l=LuaRuntime()\nl.globals().print=lambda *parts: None")
    selected = header + namespace["helpers"] + namespace["claim_setup"] + body + "\n" + chr(39)*3 + ")"
    target = R / "DevelopmentTests/test_b124_claim.py"
    exec(compile(selected, str(target), "exec"), {"__file__": str(target)})


class StoreWriteBoundaries(unittest.TestCase):

    def test_existing_b127_saved_claim_timer_regression(self):
        # Three unchanged groups: missed-load-hook resume, duplicate/same-turn,
        # and incomplete end-turn proof. This is local reconstruction evidence.
        run_claim_return_regression(legacy_extension("test_b127_claim_resume.py"))

    def test_existing_b128_selected_store_return_regression(self):
        # Eleven unchanged groups: 3 admission modes x token retained/missing,
        # 3 insufficient-proof cases, unknown/unrelated events, failed return.
        # Exclude only the superseded Industry missing-history scenario group;
        # current template initialization/reconciliation has its B140 contract.
        source = legacy_extension("test_b128_unassigned_return.py")
        boundary = "-- All four Claim kinds"
        resume = "-- Failed return persistence"
        assert source.count(boundary) == 1 and source.count(resume) == 1
        body = source.split(boundary, 1)[0] + resume + source.split(resume, 1)[1].split("print('B128 LOCAL_SIMULATION_PASS", 1)[0]
        run_claim_return_regression(body)

    def test_ordinary_age_write_cost_and_per_value_baseline(self):
        scenario = r'''
T.start();local group={}
for i=1,N do
 if i<=NT then group[i]=T.research(i)else group[i]=T.fresh(i);T.register(group[i])end
end
T.governor(1);T.scanReset();local before=T.writes()
T.turn(1);local delta=T.writes()-before;local scans=T.scanCount()
assert(delta==NT,'age writes changed');local values={}
for i=1,N do
 local r=T.record(group[i]);values[i]=T.encode(r)
 if i<=NT then assert(r.researchTradition.age==1 and T.control(group[i]).active==1)end
end
local snap=T.encode(T.props());local writes=T.writes();T.turn(0)
assert(T.writes()==writes and T.encode(T.props())==snap,'duplicate turn wrote')
T.reload();assert(T.writes()==writes and T.encode(T.props())==snap,'load wrote/replayed')
return table.concat(values,'\n'),delta,scans
'''
        old = baseline_source()
        for n, touched in ((8, 8), (20, 20), (40, 40), (40, 1)):
            with self.subTest(records=n, touched=touched):
                results = []
                for source in (old, None):
                    lua = fixture(source)
                    lua.globals().N = n
                    lua.globals().NT = touched
                    results.append(lua.execute(scenario))
                self.assertEqual(results[0][:2], results[1][:2])
                self.assertEqual(results[0][2], n * touched)
                self.assertEqual(results[1][2], 0)
                print(f"STORE_COST N={n} T={touched} uniqueness_visits={n*touched}->0 "
                      f"record_writes={touched}->{touched} per_value=MATCH; not native CPU/memory evidence")

    def test_same_turn_investment_template_and_cold_load(self):
        lua = fixture()
        lua.execute(r'''
local c,control=T.two();local frozen=T.encode(T.record(control));T.scanReset()
T.invest(c,811);T.invest(c,812);assert(T.control(c).potential==3)
local industry=T.fresh(3);T.register(industry);T.complete(industry,'DISTRICT_INDUSTRIAL_ZONE')
local token=industry.s.values.TOKEN
local ledger={schema=1,initialized=true,uid='STD:'..token,foundation=token,x=industry:GetX(),y=industry:GetY(),revision=2,
 learned={BUILDING_WORKSHOP={district='DISTRICT_INDUSTRIAL_ZONE',tier=1,turn=T.now(),evidence='BUILT'}}}
T.scanReset();shared.CityProgressionStore.WriteTemplates(industry,nil,ledger)
local before=T.writes();shared.CityProgressionStore.WriteTemplates(industry,ledger,ledger)
assert(T.writes()==before and T.scanCount()==0)
local next=M.Copy(ledger);next.revision=3;next.learned.BUILDING_FACTORY={district='DISTRICT_INDUSTRIAL_ZONE',tier=2,turn=T.now(),evidence='BUILT'}
shared.CityProgressionStore.WriteTemplates(industry,ledger,next)
assert(T.writes()==before+1 and T.scanCount()==0 and T.encode(T.record(control))==frozen)
local snapshot=T.encode(T.props());before=T.writes();T.reload()
assert(T.encode(T.props())==snapshot and T.writes()==before)
assert(shared.CityProgressionStore.ReadTemplates(industry).learned.BUILDING_FACTORY)
assert(T.control(c).potential==3 and T.encode(T.record(control))==frozen);T.clean()
''')


    def test_claim_timer_same_turn_progress_and_coldload(self):
        lua=fixture()
        lua.execute(r'''
T.start();local c=T.ai(T.fresh(1));T.district(c,'DISTRICT_CAMPUS',201,true);T.take(c)
local control=T.fresh(2);T.register(control);local frozen=T.encode(T.record(control))
local r=T.record(c);assert(r.schema==3 and r.progression=='UNASSIGNED')
local timer={version=1,token=r.base.token,reference=M.Copy(r.origin),kind='RESEARCH',project='PROJECT_SPC_CLAIM_RESEARCH',
 start=T.now(),stage='ACTIVE',deactivated=false,reason='test'}
T.scanReset();shared.CityProgressionStore.WriteClaimTimer(0,c,nil,timer)
local next=M.Copy(timer);next.deactivated=true
shared.CityProgressionStore.WriteClaimTimer(0,c,timer,next)
assert(T.scanCount()==0 and T.record(c).claimTimer.deactivated and T.encode(T.record(control))==frozen)
local snapshot=T.encode(T.props());local before=T.writes();T.reload()
assert(T.encode(T.props())==snapshot and T.writes()==before and T.record(c).claimTimer.deactivated)
next=M.Copy(next);next.stage='STOPPED';next.reason='test_stop'
shared.CityProgressionStore.WriteClaimTimer(0,c,T.record(c).claimTimer,next)
assert(T.record(c).claimTimer.stage=='STOPPED' and T.encode(T.record(control))==frozen)
''')

    def test_initial_city_token_failure_preserves_index_reference_reservation(self):
        lua=fixture()
        lua.execute(r'''
T.start();local x=T.fresh(1);x.SetProperty=function()end;T.register(x)
assert(T.index().counter==1 and x.s.values.TOKEN==nil and not T.record(x))
local y,accepted,delta=T.tryRegister(2,0,x:GetID());assert(not accepted and delta==0)
local free,ok=T.tryRegister(3,0,303);assert(ok and T.control(free).potential==0)
local before=T.writes();T.reload();assert(T.writes()==before and not pcall(T.control,x))
local other,ok2,delta2=T.tryRegister(4,0,x:GetID());assert(not ok2 and delta2==0)
''')

    def test_load_bad_endpoint_is_local_but_blocks_structural_writes(self):
        for mutation in ("r.current=false", "r.current=true", "r.current={}", "r.current={owner=0,cityID='bad'}", "r.loss=false", "r.loss=true", "r.loss={}", "r.loss={target=false}", "r.loss={target={owner=3,cityID=-1}}"):
            with self.subTest(mutation=mutation):
                lua = fixture()
                lua.globals().MUTATE = lua.eval("function(r) " + mutation + " end")
                lua.execute(r'''
local x,y=T.two();local r=T.record(x);MUTATE(r);local frozen=T.encode(r);local writes=T.writes()
T.reload();assert(T.writes()==writes and T.encode(T.record(x))==frozen)
assert(not pcall(T.control,x) and T.control(y).potential==1)
T.invest(y,820);assert(T.control(y).potential==2 and T.encode(T.record(x))==frozen)
local before=T.writes();local newcomer,accepted=T.tryRegister(3,0,303)
assert(not accepted and T.writes()==before,'unknown endpoint admitted a new record')
assert(not T.structural(y,3,500));assert(T.encode(T.record(x))==frozen)
''')

    def test_bad_revision_reserves_reliable_endpoint_and_missing_reserves_origin(self):
        for mode in ("revision", "missing"):
            with self.subTest(mode=mode):
                lua = fixture(); lua.globals().MODE = mode
                lua.execute(r'''
local x,y=T.two();local id=x:GetID()
if MODE=='revision'then T.record(x).revision=-1 else T.props()[T.key(x)]=nil end
local snapshot=T.encode(T.props());T.reload();assert(T.encode(T.props())==snapshot)
assert(not pcall(T.control,x) and T.control(y).potential==1)
local collision,accepted,delta=T.tryRegister(3,0,id);assert(not accepted and delta==0)
local free,ok=T.tryRegister(4,0,404);assert(ok and T.control(free).potential==0)
T.invest(y,821);assert(T.control(y).potential==2)
''')

    def test_load_read_throw_copy_failure_and_index_corruption(self):
        for mode in ("get-throw", "copy-cycle", "record-shape", "index"):
            with self.subTest(mode=mode):
                lua = fixture();lua.globals().MODE=mode
                lua.execute(r'''
local x,y=T.two();local key=T.key(x);local rawGet=Game.GetProperty;local before=T.writes()
if MODE=='get-throw'then Game.GetProperty=function(o,k)if k==key then error('native read fail')end;return rawGet(o,k)end
elseif MODE=='copy-cycle'then T.record(x).cycle=T.record(x)
elseif MODE=='record-shape'then T.props()[key]=true
else T.index().entries[x.s.values.TOKEN].serial=99 end
T.reload();assert(T.writes()==before)
Game.GetProperty=rawGet
if MODE=='index'then assert(not pcall(T.control,y));local _,ok,delta=T.tryRegister(3);assert(not ok and delta==0)
else
 assert(not pcall(T.control,x) and T.control(y).potential==1)
 T.invest(y,822);assert(T.control(y).potential==2)
 local _,ok,delta=T.tryRegister(3);assert(not ok and delta==0)
end
''')

    def test_real_load_collision_global_candidate_collision_local(self):
        lua = fixture()
        lua.execute(r'''
local x,y=T.two();local before=T.encode(T.record(x));local writes=T.writes()
assert(not T.structural(x,0,y:GetID()));assert(T.writes()==writes and T.encode(T.record(x))==before)
assert(T.control(y).potential==1);T.invest(y,823);assert(T.control(y).potential==2)
T.props()[T.key(x)]=T.change(T.record(x),0,y:GetID());writes=T.writes();T.reload()
assert(T.writes()==writes and not pcall(T.control,x) and not pcall(T.control,y))
''')

    def test_actual_loss_recapture_collision_and_current_facts(self):
        lua = fixture()
        lua.execute(r'''
local x,y=T.two();T.invest(x,830);local token=x.s.values.TOKEN
shared.CityProgressionStore.RegisterExit('test_owned',function()return true end)
T.loss(x,3,450);assert(T.record(x).stage=='HELD_TRANSFER')
T.reload();shared.CityProgressionStore.RegisterExit('test_owned',function()return true end);shared.CityProgressionStore.ExitConfirmed()
T.governor(1);x.s.ref.owner=0;x.s.ref.cityID=500;Events.CityTransfered.Fire(0,500,3)
assert(T.record(x).stage=='ACTIVE' and T.control(x).active==1 and T.control(x).potential==2)
local before=T.encode(T.props());local writes=T.writes();Events.CityTransfered.Fire(0,500,3)
assert(T.encode(T.props())==before and T.writes()==writes);T.reload();assert(T.control(x).potential==2)
local c,control=T.two();shared.CityProgressionStore.RegisterExit('test_owned',function()return true end)
T.loss(c,3,450);local held=T.encode(T.record(c));c.s.ref.owner=0;c.s.ref.cityID=control:GetID()
Events.CityTransfered.Fire(0,c:GetID(),3);assert(T.encode(T.record(c))==held and T.record(c).stage=='HELD_TRANSFER')
assert(T.control(control).potential==1)
''')


    def test_snapshot_copy_and_stale_manager_guards_are_retained(self):
        lua=fixture()
        lua.execute(r'''
local x,y=T.two();local s=T.storage(x);local old=s.Read();local candidate=T.normal(old)
local edited=s.Read();edited.base.specialization='INDUSTRY'
assert(s.Read().base.specialization=='RESEARCH','caller mutated committed envelope')
local before=T.writes();assert(not pcall(s.Write,T.normal(old),candidate))
assert(T.writes()==before and T.encode(s.Read())==T.encode(old),'manager stale check bypassed')
-- A refused stale manager argument never started a native write or made a
-- previously reliable occupancy uncertain.
local z,accepted=T.tryRegister(3,0,303);assert(accepted)
T.invest(y,860);assert(T.control(y).potential==2)
''')

    def test_prewrite_stale_evidence_controls_only_structural_safety(self):
        for mode in ("same-ref", "other-ref", "bad-shape", "get-throw"):
            with self.subTest(mode=mode):
                lua=fixture();lua.globals().MODE=mode
                lua.execute(r'''
local x,y=T.two();T.reload();local key=T.key(x);local s=T.storage(x);local old=s.Read();local candidate=T.normal(old)
local rawGet=Game.GetProperty
if MODE=='same-ref'then T.props()[key]=T.normal(candidate)
elseif MODE=='other-ref'then T.props()[key]=T.change(candidate,3,730)
elseif MODE=='bad-shape'then T.props()[key]=false
else Game.GetProperty=function(o,k)if k==key then error('prewrite unknown')end;return rawGet(o,k)end end
local writes=T.writes();assert(not pcall(s.Write,old,candidate));assert(T.writes()==writes)
Game.GetProperty=rawGet
T.invest(y,831);assert(T.control(y).potential==2)
local _,accepted=T.tryRegister(3,0,303);assert(accepted==(MODE=='same-ref'))
''')

    def test_failed_normal_write_readback_is_evidence_driven(self):
        for mode in ("drop", "throw-before", "throw-after", "third-same-ref", "third-other-ref", "bad-shape", "read-throw"):
            with self.subTest(mode=mode):
                self.check_failure(mode, structural=False)

    def test_failed_reference_write_reserves_candidate_without_promoting_it(self):
        for mode in ("drop", "throw-before", "throw-after", "third-same-ref", "third-other-ref", "bad-shape", "read-throw"):
            with self.subTest(mode=mode):
                self.check_failure(mode, structural=True)

    def check_failure(self, mode, structural):
        lua=fixture();lua.globals().MODE=mode;lua.globals().STRUCTURAL=structural
        lua.execute(r'''
local x,y=T.two();T.reload();local key=T.key(x);local s=T.storage(x);local old=s.Read()
local candidate=STRUCTURAL and T.change(old,3,700) or T.normal(old)
local rawSet,rawGet=Game.SetProperty,Game.GetProperty;local injected=false
Game.SetProperty=function(o,k,v)
 if k~=key then return rawSet(o,k,v)end
 injected=true
 if MODE=='drop'then return elseif MODE=='throw-before'then error('before')end
 local value=M.Copy(v)
 if MODE=='third-same-ref'then value.revision=value.revision+1
 elseif MODE=='third-other-ref'then value=T.change(value,3,701)
 elseif MODE=='bad-shape'then value.current=false;value.loss=false end
 rawSet(o,k,value);if MODE=='throw-after'then error('after')end
end
Game.GetProperty=function(o,k)if k==key and injected and MODE=='read-throw'then error('readback unknown')end;return rawGet(o,k)end
assert(not pcall(s.Write,old,candidate));Game.SetProperty=rawSet;Game.GetProperty=rawGet
assert(T.encode(T.snapshot(x))==T.encode(old),'failed candidate became committed envelope')
T.invest(y,832);assert(T.control(y).potential==2,'other unchanged-reference writer blocked')
local uncertain=MODE=='third-other-ref' or MODE=='bad-shape' or MODE=='read-throw'
local newcomer,accepted=T.tryRegister(3,0,303);assert(accepted==not uncertain,'unrelated structural gate classification')
-- Candidate endpoint is reserved only when reliable evidence cannot prove old.
local z=T.fresh(4);if not uncertain then T.register(z)end
if not uncertain then
 local ok=T.structural(z,3,700)
 local occupied=STRUCTURAL and (MODE=='throw-after' or MODE=='third-same-ref')
 assert(ok==not occupied,'candidate reservation classification')
end
-- No inferred commit/retry during repeated ordinary notifications.
local snap=T.encode(T.props());local before=T.writes();Events.GameCoreEventPublishComplete.Fire()
assert(T.encode(T.props())==snap and T.writes()==before)
''')


    def test_actual_normal_worker_third_readback_holds_only_target(self):
        for mode in ('same-ref', 'other-ref', 'bad-shape', 'read-throw'):
            with self.subTest(mode=mode):
                lua=fixture();lua.globals().MODE=mode
                lua.execute(r'''
T.start();local x=T.research(1);local y=T.fresh(2);T.register(y);T.complete(y,'DISTRICT_THEATER');T.reload()
local key=T.key(x);local old=T.encode(T.snapshot(x));local rawSet,rawGet=Game.SetProperty,Game.GetProperty;local injected=false
Game.SetProperty=function(o,k,v)
 if k~=key then return rawSet(o,k,v)end;injected=true;local value=M.Copy(v)
 if MODE=='same-ref'then value.revision=value.revision+1
 elseif MODE=='other-ref'then value=T.change(value,3,888)
 elseif MODE=='bad-shape'then value.current=false end
 return rawSet(o,k,value)
end
Game.GetProperty=function(o,k)if k==key and injected and MODE=='read-throw'then error('unknown readback')end;return rawGet(o,k)end
T.turn(1);Game.SetProperty=rawSet;Game.GetProperty=rawGet
assert(not pcall(T.control,x),'actual worker remained readable after failed write')
assert(T.encode(T.snapshot(x))==old,'failed native result promoted to committed envelope')
T.invest(y,870);assert(T.control(y).potential==2,'other unchanged-reference write blocked')
local before=T.writes();T.turn(0);assert(T.writes()==before,'held worker retried')
local _,accepted=T.tryRegister(3,0,303);assert(accepted==(MODE=='same-ref'))
''')

    def test_actual_worker_failure_holds_target_and_coldload_reads_actual_record(self):
        for applied in (False,True):
            with self.subTest(applied=applied):
                lua=fixture();lua.globals().APPLIED=applied
                lua.execute(r'''
T.start();local x=T.research(1);local y=T.fresh(2);T.register(y);local key=T.key(x)
local raw=Game.SetProperty;Game.SetProperty=function(o,k,v)
 if k==key then if APPLIED then raw(o,k,v)end;error('native uncertain write')end
 return raw(o,k,v)
end
T.turn(1);Game.SetProperty=raw
assert(not pcall(T.control,x) and T.control(y).potential==0)
local heldWrites=T.writes();T.turn(0);assert(T.writes()==heldWrites,'held worker retried failed write')
local expected=APPLIED and 1 or 0;assert(T.record(x).researchTradition.age==expected)
-- Reboot in the same turn: applied is not replayed; dropped reliable old value
-- advances once under the existing age model, not by a stored failed candidate.
local before=T.writes();T.reload();assert(T.record(x).researchTradition.age==1)
assert(T.writes()-before==(APPLIED and 0 or 1));before=T.writes();T.reload();assert(T.writes()==before)
''')

    def test_initial_commit_failure_old_nil_is_not_invented(self):
        for mode in ("drop", "throw-before", "throw-after", "third-ref", "read-throw"):
            with self.subTest(mode=mode):
                lua=fixture();lua.globals().MODE=mode
                lua.execute(r'''
T.start();local control=T.fresh(1);T.register(control);T.complete(control,'DISTRICT_CAMPUS')
local x=T.fresh(2);local key=SPCCityProgressionStore.RECORD..'DEV-B013-P0-2'
local rawSet,rawGet=Game.SetProperty,Game.GetProperty;local injected=false
Game.SetProperty=function(o,k,v)
 if k~=key then return rawSet(o,k,v)end;injected=true
 if MODE=='drop'then return elseif MODE=='throw-before'then error('before')end
 local value=MODE=='third-ref' and T.change(v,3,730) or v;rawSet(o,k,value)
 if MODE=='throw-after'then error('after')end
end
Game.GetProperty=function(o,k)if k==key and injected and MODE=='read-throw'then error('read unknown')end;return rawGet(o,k)end
T.register(x);Game.SetProperty=rawSet;Game.GetProperty=rawGet
assert(T.index().counter==2 and x.s.values.TOKEN and not pcall(T.control,x))
T.invest(control,850);assert(T.control(control).potential==2)
local _,accepted=T.tryRegister(3,0,303);assert(accepted==(MODE~='third-ref' and MODE~='read-throw'))
local before=T.writes();T.reload();assert(T.writes()==before)
if MODE=='throw-after' or MODE=='read-throw'then assert(T.control(x).potential==0)
else assert(not pcall(T.control,x))end
''')


if __name__ == "__main__":
    unittest.main(verbosity=2)
