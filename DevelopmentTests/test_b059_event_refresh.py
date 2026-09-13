from pathlib import Path
R=Path(__file__).resolve().parents[1]
s=(R/'DevelopmentTests/test_b059_dialogue.py').read_text().replace("get('version')=='77'","get('version')=='78'").replace('replace("\'76\'","\'77\'")','replace("\'76\'","\'78\'")')
s=s.replace('Events={}',"""Events=setmetatable({}, {__index=function(t,k)
 local e={list={}};e.Add=function(f) e.list[#e.list+1]=f end;e.Remove=function(f) end;rawset(t,k,e);return e
end})
function fire(name) for _,f in ipairs(Events[name].list) do f() end end""")
a='l.execute("init();assert(c1.b.BUILDING_SPC_B059_D2);local n=requests;update(2);assert(requests==n);c1.active=3;update(2);assert(not c1.b.BUILDING_SPC_B059_D2 and requests==n+1)")'
assert a in s
s=s.replace(a,'l.execute(ADDITIONAL_UI_TEST)')
ADDITIONAL_UI_TEST="""
init();assert(c1.b.BUILDING_SPC_B059_D2)
local bg=ExposedMembers.SPC_DialogueBackground;local scans=bg.scans;local sends=bg.sends
for i=1,100 do fire('SystemUpdateUI');fire('GameCoreEventPublishComplete');fire('GameCoreEventPlaybackComplete') end
assert(bg.scans==scans and bg.sends==sends) -- ordinary rendering does zero collection work
c1.active=3;fire('GovernorPromoted');fire('GameCoreEventPlaybackComplete');assert(not c1.b.BUILDING_SPC_B059_D2)
fire('SystemUpdateUI');scans=bg.scans;sends=bg.sends
for i=1,10 do fire('GreatWorkMoved') end
fire('GameCoreEventPlaybackComplete');assert(bg.scans==scans+1 and bg.sends==sends) -- duplicate notifications, unchanged collection
-- Delay acknowledgement as actual UI/game requests are asynchronous, unlike earlier mocks.
local queued
UI.RequestPlayerOperation=function(pid,op,a) requests=requests+1;queued=a end
c1.slots={10};fire('GreatWorkMoved');fire('GameCoreEventPlaybackComplete')
scans=bg.scans;sends=bg.sends;assert(bg.state=='WAIT_ACK' and queued)
for i=1,100 do fire('SystemUpdateUI');fire('GameCoreEventPublishComplete') end
assert(bg.scans==scans and bg.sends==sends) -- crucial: no async retry storm
c1.slots={10,11};fire('GreatWorkCreated');fire('GreatWorkMoved')
for i=1,100 do fire('SystemUpdateUI') end
assert(bg.scans==scans and bg.sends==sends) -- changes coalesced while waiting
shared.Dialogue.Receive(0,queued);queued=nil;fire('GameCoreEventPlaybackComplete')
assert(bg.scans==scans+1 and bg.sends==sends+1 and queued)
shared.Dialogue.Receive(0,queued);queued=nil;fire('SystemUpdateUI')
scans=bg.scans;sends=bg.sends
for i=1,100 do fire('SystemUpdateUI') end
assert(bg.scans==scans and bg.sends==sends)
-- Bounded turn fallback can recover a lost acknowledgement, never a timer loop.
c1.slots={10};fire('GreatWorkMoved');fire('GameCoreEventPlaybackComplete');assert(queued)
scans=bg.scans;sends=bg.sends;turn=turn+1;fire('PlayerTurnActivated');fire('GameCoreEventPlaybackComplete')
assert(bg.scans==scans+1 and bg.sends==sends+1)
assert(update==nil) -- no SetUpdate timer registered
"""
exec(compile(s,str(R/'DevelopmentTests/test_b059_dialogue.py'),'exec'))
ui=(R/'Mod/UI/DialogueRefresh.lua').read_text();assert 'ContextPtr:SetUpdate' not in ui
print('B059.78 LOCAL_SIMULATION_PASS: idle zero scans/sends; delayed ACK no resend storm; coalesced work events; governor change; turn-only retry; full B059 regression.')
