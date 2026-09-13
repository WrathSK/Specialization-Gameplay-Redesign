from pathlib import Path
import json
from lupa import LuaRuntime
import xml.etree.ElementTree as ET
W=Path(__file__).resolve().parents[1];R=W/"Sid Meier's Civilization VI/Mods/SpecializationP0"
def vm():
 l=LuaRuntime(unpack_returned_tuples=True)
 l.execute('''print=function() end;include=function() end;props={};writes=0;mode="ok"
 SPCP0={VERSION="P0-B-019",Scalar=tostring,IsTestPlayer=function(p) return p==0 end,Field=function() return nil end}
 ExposedMembers={};Events={LoadScreenClose={Add=function(fn) load=fn end,Remove=function() end}}
 PlayerManager={GetAliveIDs=function() return {0,1} end}
 GameEvents={SPC_P0_Request={Add=function(fn) handle=fn end}}
 for _,n in ipairs({"SPCTradeRouteProbe","SPCCompletionProbe","SPCStorageProbe","SPCBindingProbe","SPCCompletionRecordProbe","SPCCityJournalProbe","SPCEligibilityProbe","SPCQualificationProbe"}) do _G[n]={Start=function() end} end
 Game={GetProperty=function(self,k) if mode=="read_error" then error("READ") end;return props[k] end,
 SetProperty=function(self,k,v) writes=writes+1;assert(k=="SPC_DEV_ENVELOPE_B019_P0");if mode=="drop" then return end;props[k]=v;if mode=="after" then error("AFTER") end end}
 ''')
 l.execute((R/'EnvelopeProbe.lua').read_text());l.execute((R/'Gameplay.lua').read_text())
 l.execute('d=ExposedMembers.SPC_P0.EnvelopeProbe;function run(a,s) handle(0,{Action=a,ExpectedStage=s,Token="test"});return ExposedMembers.SPC_P0.Snapshot end')
 return l
l=vm();l.execute('assert(run("ENVELOPE_NEXT",0):find("WAIT_LOAD_CLOSE") and writes==0);load();assert(d.players[0].autoStep==0 and writes==0)')
snapshots=[]
def plain(x):return {k:plain(v) for k,v in x.items()} if hasattr(x,'items') else x
for step in range(6):
 l.globals().s=step;l.execute('assert(run("ENVELOPE_NEXT",s):find("SAVED_READBACK_MATCH"));assert(run("ENVELOPE_NEXT",s):find("STALE_NO_WRITE"));assert(writes==s+1)')
 snapshots.append(json.loads(json.dumps(plain(l.globals().props))))
l.execute('assert(run("ENVELOPE_NEXT",6):find("COMPLETE_NO_WRITE") and writes==6);handle(1,{Action="ENVELOPE_NEXT",ExpectedStage=0,Token="bad"});assert(writes==6 and ExposedMembers.SPC_P0.LastToken=="test")')
for step,snapshot in enumerate(snapshots,1):
 n=vm()
 def tab(x):return n.table_from({k:tab(v) for k,v in x.items()}) if isinstance(x,dict) else x
 n.globals().props=tab(snapshot);n.execute('load()')
 assert n.globals().d.players[0].autoStep==step and n.globals().writes==0
 n.execute('run("ENVELOPE_READ");assert(writes==0)')
 if step<6:
  n.globals().s=step;n.execute('assert(run("ENVELOPE_NEXT",s):find("SAVED_READBACK_MATCH") and writes==1)')
# Contract comparisons against the existing recovery model, rather than a second expected-only test.
l.globals().Recovery=l.execute((W/'DevelopmentTests/PendingCityRecovery.lua').read_text())
l.execute('''for step=1,6 do
 local e=SPCEnvelopeProbe.Expected(0,step)
 local o={contextSource="MOCK_ONLY",status="READ_OK",present=true,owner=0,cityUID="DEV_B019",facts=e.facts}
 if step%3==0 then assert(Recovery.InspectDone(e.record,o,"MOCK_ONLY").status=="DONE_MATCHED")
 else assert(Recovery.Inspect(e.record,o,"MOCK_ONLY").comparison==(step%3==1 and "BEFORE_OBSERVED" or "TARGET_OBSERVED")) end
end''')
for mode in ('drop','after','read_error'):
 n=vm();n.execute('load()');n.globals().mode=mode
 result=n.eval('run("ENVELOPE_NEXT",0)')
 assert ('SAVED_AFTER_THROW' if mode=='after' else 'WRITE_UNCONFIRMED_HELD' if mode=='drop' else 'INVALID_NO_OVERWRITE') in result
n=vm();n.execute('load();props.SPC_DEV_ENVELOPE_B019_P0={foreign=true};assert(run("ENVELOPE_NEXT",0):find("INVALID_NO_OVERWRITE") and writes==0)')
# Execute real panel dispatch; requesting either action must never select/read a city.
l.execute('''callbacks={};Controls=setmetatable({}, {__index=function(t,k) local v={SetText=function() end,SetHide=function() end,RegisterCallback=function(self,_,fn) callbacks[k]=fn end};rawset(t,k,v);return v end})
ContextPtr={SetInitHandler=function(self,fn) init=fn end,SetHide=function() end,ClearUpdate=function() end,SetUpdate=function() end,SetShutdown=function() end}
Mouse={eLClick=1};Game.GetLocalPlayer=function() return 0 end;Game.GetCurrentGameTurn=function() return 1 end
UI={GetHeadSelectedCity=function() error("NO_CITY") end,RequestPlayerOperation=function(pid,op,args) dispatched=args end};PlayerOperations={EXECUTE_SCRIPT=1}
''')
l.execute((R/'UI/P0Panel.lua').read_text());l.execute('init();callbacks.EnvelopeReadButton();assert(dispatched.Action=="ENVELOPE_READ" and dispatched.CityID==nil);callbacks.EnvelopeNextButton();assert(dispatched.Action=="ENVELOPE_NEXT" and dispatched.ExpectedStage==6)')
mod=ET.parse(R/'SpecializationP0.modinfo').getroot();assert mod.attrib['id']=='df9efdad-dd48-40a7-b868-87f0617bc16d' and mod.attrib['version']=='26'
for f in mod.findall('.//File'):assert (R/f.text).is_file(),f.text
panel=ET.parse(R/'UI/P0Panel.xml');ids=[e.attrib['ID'] for e in panel.iter() if 'ID' in e.attrib];assert len(ids)==len(set(ids))
assert 'EnvelopeProbe.lua' in [f.text for f in mod.findall('./InGameActions/ImportFiles/File')]
compiler=LuaRuntime()
for p in R.rglob('*.lua'):compiler.execute('assert(load(...))',p.read_text())
print('LOCAL_SIMULATION_PASS: actual B019 Gameplay/DEV/panel; 6 JSON reload checkpoints; stale and foreign requests; failures; recovery-contract cross-check; Lua compile/XML/manifest. No Civ VI execution.')
