from pathlib import Path
import ast
from lupa import LuaRuntime
P=Path(__file__).resolve().parent;R=P.parent/"Sid Meier's Civilization VI/Mods/SpecializationP0"
source=ast.parse((P/'test_city_journal_probe.py').read_text())
fixture=max((n.args[0].value for n in ast.walk(source) if isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute) and n.func.attr=='execute' and n.args and isinstance(n.args[0],ast.Constant) and isinstance(n.args[0].value,str)),key=len)
fixture=fixture.replace('local function boot()','local activeFlow;local evidence={};local observerMode="ok";local hook\nlocal function boot()')
needle='s={};SPCBindingProbe.Start(P,s);SPCCityJournalProbe.Start(P,s)'
assert needle in fixture
fixture=fixture.replace(needle,needle+'''
 evidence={}
 hook=Hook.Install(s,P,function(e)
  if observerMode=="throw" then error("OBSERVER_FAILURE") end
  if activeFlow then assert(activeFlow.AfterLegacy(e.owner,e.cityID,e).status=="COMMITTED_MOCK") end
  evidence[#evidence+1]=e
 end,"MOCK_ONLY")
''')
fixture+='''
-- Additional assertions use the actual B013 and B015 implementations above.
fresh();found();assert(#evidence==1 and evidence[1].token==props.SPC_DEV_BINDING_B013_TOKEN)
assert(evidence[1].scanStatus=="COMPLETE" and hook.players[0].count==1 and not hook.players[0].halted)
assert(props[KEY].health=="TRACKING" and physicalWrites==1)
found();assert(#evidence==1 and physicalWrites==1) -- actual B013 filters duplicate
boot();Events.LoadScreenClose.Fire();assert(#evidence==0);found();assert(#evidence==0)
-- Reusing an old TRACKING row cannot manufacture new evidence.
s.OnFreshCityBinding(0,city);assert(#evidence==0 and hook.players[0].halted)
fresh();scanError=true;found();assert(#evidence==0 and hook.players[0].halted and s.CityJournalProbe.players[0].halted)
fresh();mode="drop";found();assert(#evidence==0 and hook.players[0].halted)
fresh();mode="after";found();assert(#evidence==1 and not hook.players[0].halted)
fresh();observerMode="throw";found();assert(props[KEY].health=="TRACKING" and hook.players[0].halted and #evidence==0)
observerMode="ok"
assert(not pcall(Hook.Install,s,P,function() end,"MOCK_ONLY")) -- no nested replacement
-- Calls during load are preserved for legacy but never emit evidence.
fresh();boot();s.OnFreshCityBinding(0,city);assert(#evidence==0 and physicalWrites==0)

-- Actual legacy callback -> verified evidence -> flow -> city envelope.
fresh()
local life=Life.New(function() return {contextSource="GAMEPLAY_CANDIDATE",status="COMPLETE_ROSTER",current={[0]=true},enabled={0},disabled={},unknown={}} end,"MOCK_ONLY")
life.Refresh("AFTER_LOAD_CLOSE")
local deps={contextSource="MOCK_ONLY",life=life,CityManager=CityManager,binding=s.BindingProbe,Envelope=Envelope,Gate=Gate,Recovery=Recovery,Planner=Planner,State=State}
activeFlow=Flow.New({life=life,legacy=function() error("DOUBLE_LEGACY") end,inspectFresh=function() error("DOUBLE_INSPECTION") end,
 open=function(pid,cid,token,proof) return Bridge.New(deps,pid,cid,token,proof,"MOCK_ONLY") end},"MOCK_ONLY")
activeFlow.Ready({fresh=true,complete=true});found()
assert(#evidence==1 and physicalWrites==1 and props.SPC_MOCK_CITY_ENVELOPE_CANDIDATE.record.state=="DONE")
assert(props.SPC_MOCK_CITY_ENVELOPE_CANDIDATE.cityUID==props.SPC_DEV_BINDING_B013_TOKEN)
'''
l=LuaRuntime(unpack_returned_tuples=True)
for f in ['BindingProbe.lua','CityJournalProbe.lua']:l.execute((R/f).read_text())
l.globals().Hook=l.execute((P/'NativeFreshHookCandidate.lua').read_text())
for name,file in [('Life','EligibilityLifecycle.lua'),('State','CitySpecializationState.lua'),('Planner','CityFactWritePlan.lua'),('Gate','CityOperationGate.lua'),('Recovery','PendingCityRecovery.lua'),('Envelope','UnifiedCityEnvelope.lua'),('Bridge','CityPropertyBridge.lua'),('Flow','CityEventFlow.lua')]:l.globals()[name]=l.execute((P/file).read_text())
l.execute(fixture)
print('LOCAL_SIMULATION_PASS: actual B013+B015 with captured legacy wrapper; original journal regression; one-call write evidence, duplicate/load/stale refusal, swallowed scan failure, lost write, write-after-throw, observer failure isolation and single install. Not deployed.')
