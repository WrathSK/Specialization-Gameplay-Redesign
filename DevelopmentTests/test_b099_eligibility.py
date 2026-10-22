"""Context-specific eligibility and actual request-ingress rejection; no native PASS claim."""
from pathlib import Path
from lupa.lua55 import LuaRuntime
R=Path(__file__).resolve().parents[1];M=R/'Mod';l=LuaRuntime()
l.globals().include=lambda name:l.execute((M/(name+'.lua')).read_text())
l.execute((M/'Probe.lua').read_text())
l.execute('''P=SPCP0
local cfg={GetCivilizationTypeName=function()return 'CIVILIZATION_SPC_TEST'end,GetLeaderTypeName=function()return 'LEADER_SPC_TEST'end}
PlayerConfigurations={[0]=cfg,[7]=cfg};Players={[0]={IsHuman=function()return true end},[7]={IsHuman=function()return true end}}
GameConfiguration={IsAnyMultiplayer=function()return false end}
assert(P.IsTestPlayer(0));assert(P.IsTestPlayer(7)) -- ID is not eligibility
cfg.IsHuman=function()error('must not call configuration human API')end
assert(P.IsTestPlayer(0));cfg.IsHuman=nil
Players[0].IsHuman=function()return false end;assert(not P.IsTestPlayer(0))
Players[0].IsHuman=nil;assert(not P.IsTestPlayer(0))
Players[0].IsHuman=function()return 1 end;assert(not P.IsTestPlayer(0))
Players[0].IsHuman=function()error('native unavailable')end;assert(not P.IsTestPlayer(0))
Players[0].IsHuman=function()return true end
GameConfiguration.IsAnyMultiplayer=function()return true end;assert(not P.IsTestPlayer(0))
GameConfiguration.IsAnyMultiplayer=nil;assert(not P.IsTestPlayer(0))
GameConfiguration.IsAnyMultiplayer=function()return nil end;assert(not P.IsTestPlayer(0))
GameConfiguration.IsAnyMultiplayer=function()return false end
assert(P.IsTestPlayer(0));assert(not P.IsTestPlayer(99))
cfg.GetLeaderTypeName=function()return 'OTHER'end;assert(not P.IsTestPlayer(0))
cfg.GetLeaderTypeName=function()return 'LEADER_SPC_TEST'end
''')
g=(M/'Gameplay.lua').read_text();prefix=g[g.index('local function request('):g.index('  -- B068 presentation')]
l.execute('shared={}; reached=0\n'+prefix+'reached=reached+1\nend\nDispatch=request')
l.execute('''Dispatch(0,{Token='ok',Action='GOVERNOR'});assert(reached==1)
Players[0].IsHuman=nil
for i=1,10 do Dispatch(0,{Token='reject'..i,Action='SPECIALISTS'}) end
assert(reached==1 and shared.RequestToken=='reject10' and shared.FailureAt=='PLAYER_ELIGIBILITY')
assert(shared.Stage:sub(1,5)=='ERROR' and shared.Stage:find('Player.IsHuman',1,true))
assert(shared.RequestIngress.count==11)
''')
# Actual UI response handler takes the existing error branch, with no retry or read requests.
u=(M/'UI/P0Panel.lua').read_text();ui=u[u.index('local function displayResponse()'):u.index('-- B060 read/control')]
l.execute('''ExposedMembers={SPC_P0=shared};shared.Version=P.VERSION
pendingToken='reject10';pendingAction='SPECIALISTS';readings={};page=1
function status(s) displayed=s end
'''+ui+'\nassert(displayResponse());assert(displayed:find("PLAYER_ELIGIBILITY",1,true))')
print('PASS: native Player human API; no config-human dependency; IDs 0/7; AI/multiplayer/unknown reject; actual Gameplay rejection -> UI error; fixed ingress state')
