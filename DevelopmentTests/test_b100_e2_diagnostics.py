"""L1 diagnostic change with directly related E2 safety cases; no native claims."""
from pathlib import Path
import runpy
R=Path(__file__).resolve().parents[1]
l=runpy.run_path(str(R/'DevelopmentTests/test_p0_e2.py'))['l']
l.execute(r"""
function encode(v)if type(v)~='table'then return tostring(v)end;local t={};for k,x in pairs(v)do t[#t+1]=tostring(k)..'='..encode(x)end;table.sort(t);return '{'..table.concat(t,';')..'}'end
P.IsTestPlayer=function(pid)return pid==0 end
local KEY=SPCCityProgressionStore.KEY
reset(2);import()
d.RegisterExit('BrokenModule',function()error('EXACT_EXIT_FAILURE')end)
s.ref.owner=3;s.ref.cityID=40;s.values.TOKEN=nil
Events.CityTransfered.Fire(3,40,0,7)
local frozen=encode(Game:GetProperty(KEY))
-- No diagnostic may write or request/rederive. Fake unrelated same-ID Network row.
P.SetProperty=function()error('DIAGNOSTIC_WRITE')end
shared.NetworkBridge={players={[0]={input={cities={[40]={reference='UNRELATED_OWNER_CITY',active=4}}}}}}
local report=d.NativeDescribe(0)
assert(report:find('FOREIGN_OWNER_NOT_QUERIED',1,true) and not report:find('UNRELATED_OWNER_CITY',1,true),report)
assert(report:find('BrokenModule',1,true) and report:find('EXACT_EXIT_FAILURE',1,true),report)
assert(report:find('STILL_FOREIGN',1,true) and report:find('当前匹配 MISSING',1,true),report)
-- Conquered evidence observes only, cannot enter recapture even when live owner changed.
s.ref.owner=0;s.ref.cityID=88
GameEvents.CityConquered.Fire(0,3,88,4,5)
report=d.NativeDescribe(0)
assert(report:find('WAIT_MATCHING_TRANSFER_EVENT',1,true) and report:find('CityConquered(0,3,88,4,5)',1,true),report)
assert(encode(Game:GetProperty(KEY))==frozen)
Events.CityTransfered.Fire(0,88,3,0)
report=d.NativeDescribe(0)
assert(report:find('RETURN_CHAIN_MISSING',1,true),report)
assert(encode(Game:GetProperty(KEY))==frozen)
-- Same owner/ID with stale reference must also be rejected by diagnostic lookup.
shared.NetworkBridge.players[0].input.cities[88]={reference='OLD_SAME_OWNER_REFERENCE',active=4}
report=d.NativeDescribe(0);assert(report:find('REFERENCE_MISMATCH',1,true) and not report:find('OLD_SAME_OWNER_REFERENCE',1,true),report)
shared.NetworkBridge.players[0].input.cities[88]={reference=SPCNetworkInput.Reference(c),active=0}
report=d.NativeDescribe(0);assert(report:find('Network当前引用 MATCHED',1,true),report)
-- Only latest scalar slots, not event history or incoming table payloads.
for i=1,32 do GameEvents.CityConquered.Fire(0,3,88,4,5,{secret='PAYLOAD_SHOULD_NOT_APPEAR'},'extra')end
report=d.NativeDescribe(0)
local _,count=report:gsub('CityConquered%(', '')
assert(count==1 and report:find('<table>',1,true) and report:find('argc=7',1,true) and not report:find('PAYLOAD_SHOULD_NOT_APPEAR',1,true),report)
assert(encode(Game:GetProperty(KEY))==frozen)
-- Observation errors cannot prevent the unchanged authoritative transfer callback.
GameEvents.CityConquered.Fire(false,nil,88,4,5)
report=d.NativeDescribe(0);assert(report:find('CityConquered(false,nil,88,4,5)',1,true),report)
local oldTurn=Game.GetCurrentGameTurn;Game.GetCurrentGameTurn=function()error('UNAVAILABLE')end
d.returnRejection=nil;Events.CityTransfered.Fire(0,88,3,0)
-- B102 treats the preceding invalid conquest tuple as conflicting evidence.
assert(d.returnRejection=='RETURN_CONQUEST_CONFLICT')
Game.GetCurrentGameTurn=oldTurn
boot();report=d.NativeDescribe(0)
assert(report:find('本次加载未收到上述事件',1,true) and not report:find('CityConquered(',1,true),report)
assert(encode(Game:GetProperty(KEY))==frozen)
print('B100 diagnostic LOCAL_SIMULATION_PASS: owner/reference isolation, exact exit error, raw conquest/transfer evidence, missing-token hold unchanged, bounded session slots, no writes, reload reset')
""")
