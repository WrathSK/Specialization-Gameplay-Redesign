from pathlib import Path
R=Path(__file__).resolve().parents[1]
s=(R/'DevelopmentTests/test_b059_event_refresh.py').read_text().replace("78","79")
# Inject the real missing-city-collection condition before initialization, preserving other assertions.
s=s.replace("s=s.replace('Events={}',", "s=s.replace('SPCDialogue.Start(P,shared);local d=shared.Dialogue', 'Players[63]={GetCities=function() return nil end};SPCDialogue.Start(P,shared);local d=shared.Dialogue')\ns=s.replace('Events={}',")
s=s.replace("exec(compile(s,str(R/'DevelopmentTests/test_b059_dialogue.py'),'exec'))", "s=s.replace('# Frozen B058 suite', 'saved_dialogue_lua=l\\n# Frozen B058 suite')\nexec(compile(s,str(R/'DevelopmentTests/test_b059_dialogue.py'),'exec'))")
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
print('B059.79 LOCAL_SIMULATION_PASS: nil-city player skipped; init failure ACK/error surfaced; later event recovers; delayed ACK/idle performance regression retained.')
