from pathlib import Path
R=Path(__file__).resolve().parents[1]
s=(R/'DevelopmentTests/test_b059_event_refresh.py').read_text().replace("78","80")
# Inject the real missing-city-collection condition before initialization, preserving other assertions.
s=s.replace("s=s.replace('Events={}',", "s=s.replace('SPCDialogue.Start(P,shared);local d=shared.Dialogue', 'Players[63]={GetCities=function() return nil end};SPCDialogue.Start(P,shared);local d=shared.Dialogue')\ns=s.replace('Events={}',")
s=s.replace("exec(compile(s,str(R/'DevelopmentTests/test_b059_dialogue.py'),'exec'))", "s=s.replace('# Frozen B058 suite', 'saved_dialogue_lua=l\\n# Frozen B058 suite')\nexec(compile(s,str(R/'DevelopmentTests/test_b059_dialogue.py'),'exec'))")

s=s.replace("assert 'ContextPtr:SetUpdate' not in ui", "assert 'pending.retries>=2' in ui")
s=s.replace("exec(compile(s,str(R/'DevelopmentTests/test_b059_dialogue.py'),'exec'))", "s=s.replace('ClearUpdate=function() end','ClearUpdate=function() update=nil end')\nexec(compile(s,str(R/'DevelopmentTests/test_b059_dialogue.py'),'exec'))")
s=s.replace("assert(update==nil) -- no SetUpdate timer registered", """
-- The dropped request is retried twice with exactly the same sequence/data, no scan.
local packet=queued;scans=bg.scans;sends=bg.sends
assert(update);update(2);assert(bg.scans==scans and bg.sends==sends+1 and queued.Seq==packet.Seq and queued.Data==packet.Data)
update(2);assert(update==nil and bg.state=='ACK_TIMEOUT' and bg.scans==scans and bg.sends==sends+2)
for i=1,100 do fire('SystemUpdateUI') end
assert(bg.sends==sends+2 and bg.state=='ACK_TIMEOUT')
-- Late acknowledgement still clears pending without new scans or duplicate application.
shared.Dialogue.Receive(0,queued);fire('SystemUpdateUI');assert(bg.state=='IDLE' and update==nil)
-- First send silently rejected, retry delivered: background initializes without panel.
local real=shared.Dialogue.Receive;local attempts=0
UI.RequestPlayerOperation=function(pid,op,a)
 attempts=attempts+1
 if attempts==1 then return false end
 real(pid,a);fire('GameCoreEventPublishComplete');return true
end
c1.slots={10,11};fire('GreatWorkMoved');fire('GameCoreEventPlaybackComplete')
scans=bg.scans;assert(bg.transport=='false' and update)
update(2);assert(bg.state=='IDLE' and update==nil and attempts==2 and bg.scans==scans)
""")

exec(compile(s,str(R/'DevelopmentTests/test_b059_event_refresh.py'),'exec'))
# The inner suite keeps its real Dialogue Lua runtime in l.
saved_dialogue_lua.execute("""
local d=shared.Dialogue
local init=d.Init;d.ready=false;d.Init=function() error('injected carrier init failure') end
local seq=(d.seq[0] or 0)+1
d.Receive(0,{Generation=d.generation,Seq=seq,Valid=1,Turn=turn,Data='1,-1,EMPTY;2,-1,EMPTY',Count=2})
assert(d.seq[0]==seq and d.received[0].stage=='INIT_FAILED' and d.errors[0]:find('DIALOGUE_INIT_FAILED'))
d.last[0]=nil;assert(d.Describe(0,c1):find('injected carrier init failure'))
d.Init=init
d.Receive(0,{Generation=d.generation,Seq=seq+1,Valid=1,Turn=turn,Data='1,-1,EMPTY;2,-1,EMPTY',Count=2})
assert(d.ready and d.received[0].stage=='ACCEPTED' and d.errors[0]==nil)
d.Receive(0,{Generation=999,Seq=seq+2});d.last[0]=nil
assert(d.Describe(0,c1):find('REJECTED_GENERATION'))
""")
print('B059.80 LOCAL_SIMULATION_PASS: nil-city player skipped; init failure ACK/error surfaced; later event recovers; delayed ACK/idle performance regression retained.')

print('B059.80 LOCAL_SIMULATION_PASS: dropped-first-packet recovery; max two same-packet retries without scanning; false return visible; timeout idle; late ACK; synchronous publish reentry.')
