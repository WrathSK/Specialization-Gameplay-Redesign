from pathlib import Path
R=Path(__file__).resolve().parents[1]
s=(R/'DevelopmentTests/test_b060_gw_adjacency.py').read_text().replace('"78","84"','"78","85"')
exec(compile(s,str(R/'DevelopmentTests/test_b060_gw_adjacency.py'),'exec'))
game=(M/'Gameplay.lua').read_text()
l.execute('P.Scalar=tostring;function stage(v) shared.Stage=v end;GameEvents={SPC_P0_Request={Add=function(f) actualRequest=f end}}\n'+game[game.index('local function request('):game.index('stage("INITIALIZED ISOLATED_PROBES')])
l.execute('''
local cities=Players[0]:GetCities();cities.FindID=function(_,id) if id==1 then return city end end
Players[0].GetCities=function() return cities end
local d=shared.GreatWorkAdjacency
actualRequest(0,{Action='GWA_READ',Token='one',CityID=1});assert(shared.LastToken=='one' and shared.Snapshot:find('未就绪'))
shared.GreatWorkAdjacency=nil
actualRequest(0,{Action='GWA_AUTO',Token='two',CityID=1});assert(shared.LastToken=='two' and shared.Snapshot:find('GWA_MODULE_NOT_LOADED'))
shared.GreatWorkAdjacency=d
local describe=d.Describe;d.Describe=function() error('injected describe failure') end
actualRequest(0,{Action='GWA_READ',Token='three',CityID=1});assert(shared.LastToken=='three' and shared.Snapshot:find('injected describe failure'))
d.Describe=describe
actualRequest(0,{Action='GWA_READ',Token='four',CityID=999});assert(shared.LastToken=='four' and shared.Snapshot:find('GWA_CITY_UNAVAILABLE'))
-- Actual panel request/response, timers deliberately never run.
Controls={Status={SetText=function(_,v) text=v end}}
ContextPtr.ClearUpdate=function() end;ContextPtr.SetUpdate=function() end
UI.GetHeadSelectedCity=function() return city end
SPCBoostGreatWorkRead={Adjacency=function() return 'native read' end}
''')
panel=(M/'UI/P0Panel.lua').read_text();l.execute(panel[:panel.index('local function copy(')]+'\nTestRequest=request;TestPulse=gwaPulse')
l.execute('''
local attempts=0
UI.RequestPlayerOperation=function(pid,op,a) attempts=attempts+1;if attempts>1 then actualRequest(pid,a) end;return true end
TestRequest('GWA_READ');assert(text:find('READING'))
for i=1,20 do TestPulse() end
assert(attempts==2 and text:find('ACK') and text:find('native read'))
local before=attempts;for i=1,100 do TestPulse() end;assert(attempts==before)
UI.RequestPlayerOperation=function() attempts=attempts+1;return true end
TestRequest('GWA_READ');before=attempts;for i=1,100 do TestPulse() end
assert(attempts==before+2 and text:find('相邻请求未收到回复'))
UI.RequestPlayerOperation=function(pid,op,a) actualRequest(pid,a);return true end
shared.GreatWorkAdjacency=nil;TestRequest('GWA_AUTO');assert(text:find('ACK') and text:find('GWA_MODULE_NOT_LOADED'))
''')
print('B060.85 PASS real dispatcher and panel: success, module absent, native exception, city missing, dropped request recovery without timer, bounded loss, zero idle requests.')
