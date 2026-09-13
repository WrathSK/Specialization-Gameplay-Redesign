from pathlib import Path
from lupa.lua55 import LuaRuntime
w=Path(__file__).resolve().parents[1];r=w/"Sid Meier's Civilization VI/Mods/SpecializationP0"
# Reuse the actual module's existing four-family fixture and checks, without reinstalling live SQL.
p=w/'DevelopmentTests/test_lv3_support.py';scope={'__file__':str(p),'__name__':'fixture'}
exec(compile(p.read_text().split('p=w/')[0],str(p),'exec'),scope);l=scope['l']
l.execute('''
local function event() local e={list={}};e.Add=function(f) e.list[#e.list+1]=f end;e.Remove=function() end;e.Fire=function(...) for _,f in ipairs(e.list) do f(...) end end;return e end
Events=setmetatable({},{__index=function(t,k) local e=event();rawset(t,k,e);return e end});GameEvents=setmetatable({},{__index=function(t,k) local e=event();rawset(t,k,e);return e end})
SPCLv3Support.Start(P,shared);a=shared.Lv3Support;owner=0;complete=true
for _,k in ipairs({'CULTURE','COMMERCE'}) do
 kind=k;potential=3;active=2;Events.LoadScreenClose.Fire();assert(not stored['BUILDING_SPC_DEV_LV3_'..k])
 active=3;Events.GovernorPromoted.Fire(0,7,8);assert(stored['BUILDING_SPC_DEV_LV3_'..k])
 local n=writes;Events.GovernorPromoted.Fire(0,7,8);assert(writes==n)
end
-- Background post-publish notification when gameplay's immediate callback sees old facts.
SPCP0=P;P.VERSION='P0-B-037';shared.Version=P.VERSION;shared.Lv2GPP={ready=true};ExposedMembers={SPC_P0=shared}
Game={GetLocalPlayer=function() return 0 end};PlayerOperations={EXECUTE_SCRIPT=1};include=function() end
requests=0;UI={RequestPlayerOperation=function(pid,op,p) assert(p.Action=='LV2_GPP_DIRTY');requests=requests+1;a.Audit() end}
ContextPtr={SetInitHandler=function(_,f) init=f end,SetShutdown=function() end}
''')
l.execute((r/'UI/GPPRefresh.lua').read_text())
l.execute('''
init();kind='CULTURE';potential=3;active=2;a.Audit()
Events.GovernorPromoted.Fire(0,7,8);assert(not stored.BUILDING_SPC_DEV_LV3_CULTURE)
active=3;local n=requests;Events.GameCoreEventPublishComplete.Fire();assert(requests==n+1 and stored.BUILDING_SPC_DEV_LV3_CULTURE)
Events.GameCoreEventPublishComplete.Fire();assert(requests==n+1)
''')
print('PASS: actual GovernorPromoted callback enables Culture/Commerce; duplicate event idempotent; real background sender retries on publish after stale immediate facts. No game proof.')
