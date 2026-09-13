from pathlib import Path
from lupa.lua55 import LuaRuntime
w=Path(__file__).resolve().parent
l=LuaRuntime(unpack_returned_tuples=True)
l.globals().Rules=l.execute((w/'CitySpecializationState.lua').read_text())
l.globals().Executor=l.execute((w/'SettlerInvestmentExecutor.lua').read_text())
l.execute('''
local function cp(v) if type(v)~='table' then return v end;local c={};for k,x in pairs(v) do c[k]=cp(x) end;return c end
local id={contextSource='MOCK_ONLY',owner=0,cityUID='C1',present=true,
 eligibility={contextSource='MOCK_ONLY',player=0,status='ENABLED'}}
local base={schema=1,facts={schemaVersion=1,cityUID='C1',owner=0,revision=1,
 specialization='RESEARCH',potential=1,firstCompletion={family='CAMPUS',eventID='E1',districtUID='D1'},investments={}}}
local function unit(n) return {contextSource='MOCK_ONLY',owner=0,cityUID='C1',unitType='SETTLER',present=true,unitUID=n} end
local function fixture(saved)
 local f={state=cp(saved or base),live={},writes=0,kills=0}
 f.io={read=function() return cp(f.state) end,write=function(s)
  f.writes=f.writes+1;if f.failWrite==f.writes then return end;f.state=cp(s)
 end,presence=function(n) if f.unknown then return 'UNKNOWN' end;return f.live[n] and 'PRESENT' or 'ABSENT' end,
 validate=function() return not f.invalid end,consume=function(u)
  f.kills=f.kills+1
  if f.noDelete then return end;f.live[u.unitUID]=nil
  if f.afterConsume then f.afterConsume() end
 end}
 f.exec=Executor.New(Rules,f.io);return f
end
local f=fixture()
for level=2,4 do
 local n='U'..level;f.live[n]=true
 local x=f.exec.Run(id,unit(n),'R'..level);assert(x.status=='READY' and x.potential==level)
 local writes,kills=f.writes,f.kills
 x=f.exec.Run(id,unit(n),'R'..level);assert(x.status=='READY' and not x.changed)
 assert(f.writes==writes and f.kills==kills)
 f.exec=Executor.New(Rules,f.io);assert(f.exec.Resume(id).potential==level)
end
f.live.U5=true;assert(f.exec.Run(id,unit('U5'),'R5').status=='REJECTED');assert(f.kills==3 and f.live.U5)
local g={governorGateStatus='KNOWN',owner=0,cityUID='C1',governorLevelCeiling=4}
assert(Rules.Derive(f.state.facts,id,g).active==4);g.governorLevelCeiling=1
assert(Rules.Derive(f.state.facts,id,g).active==1 and f.state.facts.potential==4)
-- Failed initial intent persistence never consumes.
f=fixture();f.live.U=true;f.failWrite=1
assert(f.exec.Run(id,unit('U'),'R').status=='HELD');assert(f.kills==0 and f.state.facts.potential==1)
-- Deleted but no persisted confirmation: never infer success from missing unit on reload.
f=fixture();f.live.U=true;f.failWrite=2
assert(f.exec.Run(id,unit('U'),'R').status=='HELD');assert(f.kills==1 and f.state.pending.stage=='INTENT')
f.exec=Executor.New(Rules,f.io);assert(f.exec.Resume(id).status=='HELD');assert(f.state.facts.potential==1 and f.kills==1)
-- Confirmed debit with failed final write resumes once, no second debit.
f=fixture();f.live.U=true;f.failWrite=3
assert(f.exec.Run(id,unit('U'),'R').status=='HELD');assert(f.state.pending.stage=='CONSUMED_CONFIRMED')
f.exec=Executor.New(Rules,f.io);assert(f.exec.Resume(id).potential==2);assert(f.kills==1)
assert(not f.exec.Run(id,unit('U'),'R').changed and f.kills==1)
-- No deletion, changed location, unknown presence: no reward.
for _,mode in ipairs({'noDelete','invalid','unknown'}) do
 f=fixture();f.live.U=true;f[mode]=true
 assert(f.exec.Run(id,unit('U'),'R').status=='HELD');assert(f.state.facts.potential==1)
end
-- Disabled and wrong unit reject cleanly; no store/unit mutation.
f=fixture();f.live.U=true;local disabled=cp(id);disabled.eligibility.status='DISABLED'
assert(f.exec.Run(disabled,unit('U'),'R').status=='REJECTED')
local bad=unit('U');bad.unitType='WARRIOR';assert(f.exec.Run(id,bad,'R').status=='REJECTED')
assert(f.writes==0 and f.kills==0)
-- Re-entrant callbacks cannot grant twice or continue past ambiguity.
f=fixture();f.live.U=true;f.afterConsume=function() assert(f.exec.Run(id,unit('U'),'R').status=='HELD') end
assert(f.exec.Run(id,unit('U'),'R').status=='HELD');assert(f.kills==1 and f.state.facts.potential==1)
''')
print('LOCAL_SIMULATION_PASS: Potential 1→4; repeated receipts/load do not debit again; cap and governor demotion preserve investment; write/debit ambiguity held; confirmed recovery; invalid/disabled/reentrant cases. No native adapter or game proof.')
