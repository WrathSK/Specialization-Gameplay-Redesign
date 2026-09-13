from pathlib import Path
R=Path(__file__).resolve().parents[1]
s=(R/'DevelopmentTests/test_b059_event_refresh.py').read_text().replace("78","83")
# Inject the real missing-city-collection condition before initialization, preserving other assertions.
s=s.replace("s=s.replace('Events={}',", "s=s.replace('SPCDialogue.Start(P,shared);local d=shared.Dialogue', 'Players[63]={GetCities=function() return nil end};SPCDialogue.Start(P,shared);local d=shared.Dialogue')\ns=s.replace('Events={}',")
s=s.replace("exec(compile(s,str(R/'DevelopmentTests/test_b059_dialogue.py'),'exec'))", "s=s.replace('# Frozen B058 suite', 'saved_dialogue_lua=l\\n# Frozen B058 suite')\nexec(compile(s,str(R/'DevelopmentTests/test_b059_dialogue.py'),'exec'))")

NEW_UI_TEST="\nlocal function real(pid,op,a) requests=requests+1;actualRequest(pid,a);return true end\nUI.RequestPlayerOperation=real\ninit();assert(c1.b.BUILDING_SPC_B059_D2 and shared.DialogueIngress.seq=='1')\nlocal bg=ExposedMembers.SPC_DialogueBackground;local scans=bg.scans;local sends=bg.sends\nfor i=1,100 do fire('SystemUpdateUI') end\nassert(bg.scans==scans and bg.sends==sends and update==nil)\n-- Drop first packet while SetUpdate never executes; generic pulses recover with no scans.\nlocal attempt=0\nUI.RequestPlayerOperation=function(pid,op,a) attempt=attempt+1;if attempt==1 then return true end;return real(pid,op,a) end\nc1.slots={10};fire('GreatWorkMoved');fire('GameCoreEventPlaybackComplete');scans=bg.scans\nfor i=1,3 do fire('SystemUpdateUI') end\nassert(attempt==2 and bg.scans==scans and shared.Dialogue.last[0][1].d==1)\n-- Persistent loss: two retries then stop. Idle generic pulses do not restart collection.\nUI.RequestPlayerOperation=function() return true end\nc1.slots={10,11};fire('GreatWorkMoved');fire('GameCoreEventPlaybackComplete');scans=bg.scans;sends=bg.sends\nfor i=1,100 do fire('SystemUpdateUI') end\nassert(bg.state=='ACK_TIMEOUT' and bg.scans==scans and bg.sends==sends+2)\n-- New real collection event after timeout supersedes old packet with current data.\nUI.RequestPlayerOperation=real;c1.slots={10};fire('GreatWorkCreated');fire('GameCoreEventPlaybackComplete')\nassert(bg.state=='IDLE' and bg.scans==scans+1 and shared.Dialogue.last[0][1].d==1)\nassert(shared.RequestIngress.action=='DIALOGUE_SAMPLE')\nactualRequest(0,{Action='GW_READ',Token='read',CityID=1});assert(shared.LastToken=='read')\nassert(update==nil)\n"
game=(R/'Mod/Gameplay.lua').read_text()
REAL_DISPATCHER='P.Scalar=tostring;function stage(v) error(v) end;GameEvents={SPC_P0_Request={Add=function(f) actualRequest=f end}}\n'+game[game.index('local function request('):game.index('stage(\"INITIALIZED ISOLATED_PROBES')]

a=s.index('ADDITIONAL_UI_TEST="""');b=s.index('"""\n',a+24)
s=s[:a]+'ADDITIONAL_UI_TEST='+repr(NEW_UI_TEST)+'\n'+s[b+4:]
# Exercise the actual Gameplay dispatcher instead of calling Receive directly.
s=s.replace('l.execute(ADDITIONAL_UI_TEST)', "l.execute(REAL_DISPATCHER);l.execute(ADDITIONAL_UI_TEST)")

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
print('B059.83 LOCAL_SIMULATION_PASS: nil-city player skipped; init failure ACK/error surfaced; later event recovers; delayed ACK/idle performance regression retained.')

print("B059.83 LOCAL_SIMULATION_PASS: actual Gameplay dispatcher; no timer callbacks; dropped-first recovery; bounded event retries; new-work recovery after timeout; idle zero scans/sends.")

exec((R/'DevelopmentTests/test_b059_dialogue.py').read_text().split('root=ET.parse')[0])
# Native DB test carriers have the same seven object scopes and correct factors.
for value in (25,50,100):
 rows=db.execute("select a.Value from BuildingModifiers b join ModifierArguments a using(ModifierId) where b.BuildingType=? and a.Name='ScalingFactor'",('BUILDING_SPC_B059_TEST'+str(value),)).fetchall()
 assert len(rows)==14 and all(int(x[0])==100+value for x in rows)
saved_dialogue_lua.execute("""
local d=shared.Dialogue;c1.active=4;c1.kind='CULTURE'
for _,v in ipairs({25,50,100}) do
 actualRequest(0,{Action='DIALOGUE_TEST'..v,Token='test'..v,CityID=1})
 assert(d.last[0][1].applied==v and c1.b['BUILDING_SPC_B059_TEST'..v])
 assert(not c1.b.BUILDING_SPC_B059_D2)
 for _,other in ipairs({25,50,100}) do if other~=v then assert(not c1.b['BUILDING_SPC_B059_TEST'..other]) end end
 local n=c1.writes;actualRequest(0,{Action='DIALOGUE_TEST'..v,Token='again',CityID=1});assert(c1.writes==n)
end
actualRequest(0,{Action='DIALOGUE_OFF',Token='off',CityID=1});assert(not c1.b.BUILDING_SPC_B059_TEST100 and d.last[0][1].applied==0)
actualRequest(0,{Action='DIALOGUE_AUTO',Token='auto',CityID=1});assert(d.test[0]==nil)
actualRequest(0,{Action='DIALOGUE_TEST100',Token='again',CityID=1});c1.active=3;d.Audit(0);assert(not c1.b.BUILDING_SPC_B059_TEST100)
c1.active=4;d.Audit(0);SPCDialogue.Start(P,shared);shared.Dialogue.Init();assert(not c1.b.BUILDING_SPC_B059_TEST100 and shared.Dialogue.test[0]==nil)
""")
print('B059.83 LOCAL_SIMULATION_PASS: test25/50/100 native SQL factors; actual requests; replace not stack; OFF/AUTO; ACTIVE gating; load cleanup.')

# Read-only baseline comparison, using actual UI reader with native method mocks.
x=LuaRuntime(unpack_returned_tuples=True)
x.execute("""
C=5;T=20;total=108;turn=13;work=1;theme=false
Locale={Lookup=function(n) return n end};Game={GetLocalPlayer=function() return 0 end,GetCurrentGameTurn=function() return turn end}
GameInfo={Buildings=function() local done=false;return function() if not done then done=true;return {Index=1} end end end}
P={Info=function(t,k) if t=='Yields' then return {Index=1} end;return {Name='Work',GreatWorkObjectType='GREATWORKOBJECT_WRITING',EraType='E1'} end}
b={HasBuilding=function() return true end,GetNumGreatWorkSlots=function() return 1 end,IsBuildingThemedCorrectly=function() return theme end,GetBuildingYieldFromGreatWorks=function() return C end,GetBuildingTourismFromGreatWorks=function(_,rel) return rel and 0 or T end,GetGreatWorkInSlot=function() return work end,GetGreatWorkTypeFromIndex=function() return 'A' end}
c={GetID=function() return 1 end,GetBuildings=function() return b end,GetYield=function() return total end}
""")
x.execute((M/'UI/BoostGreatWorkRead.lua').read_text())
x.execute("""
local r=SPCBoostGreatWorkRead.Works(P,c,true);assert(r:find('ΔC=+0.0000',1,true))
C=10;T=25;r=SPCBoostGreatWorkRead.Works(P,c);assert(r:find('作品ΔC=+5.0000 / ΔT=+5.0000',1,true) and r:find('整城ΔC=+0.0000',1,true))
turn=14;total=113;r=SPCBoostGreatWorkRead.Works(P,c);assert(r:find('T13 → T14',1,true) and r:find('整城ΔC=+5.0000',1,true))
work=2;theme=true;r=SPCBoostGreatWorkRead.Works(P,c);assert(r:find('状态已变化',1,true) and r:find('其中作品C=10.0000 / T=25.0000',1,true))
""")
print('B059.83 LOCAL_SIMULATION_PASS: read-only baseline; per-city/turn differences; changed collection/theming warning; themed-work subtotal; existing regressions.')
