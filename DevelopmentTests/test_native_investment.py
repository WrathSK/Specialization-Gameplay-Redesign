from pathlib import Path
from lupa.lua55 import LuaRuntime
import xml.etree.ElementTree as ET
w=Path(__file__).resolve().parent;r=w.parent/"Sid Meier's Civilization VI/Mods/SpecializationP0"
l=LuaRuntime(unpack_returned_tuples=True)
for name in ['EffectiveFacts.lua','InvestmentAction.lua']:l.execute((r/name).read_text())
l.execute('''
local function cp(v) if type(v)~='table' then return v end;local c={};for k,x in pairs(v) do c[k]=cp(x) end;return c end
local function event() local e={list={}};e.Add=function(f) e.list[#e.list+1]=f end;e.Fire=function(...) for _,f in ipairs(e.list) do f(...) end end;return e end
local KEY='SPC_DEV_INVESTMENT_LEDGER_V1'
local props,units;local writes,kills;local mode;local turn=1
local f={owner=0,cityID=7,token='T',potential=1,specialization='RESEARCH',first={districtID=2,type='DISTRICT_CAMPUS'}}
local c={GetOwner=function() return 0 end,GetID=function() return 7 end,GetX=function() return 4 end,GetY=function() return 5 end,
 GetProperty=function(_,k) return cp(props[k]) end,SetProperty=function(_,k,v) writes=writes+1;if mode~='write'..writes then props[k]=cp(v) end end}
local collection={FindID=function(_,id) return units[id] end,Destroy=function(_,u)
 kills=kills+1;if mode=='noDelete' then return end;units[u:GetID()]=nil;Events.UnitRemovedFromMap.Fire(0,u:GetID())
end}
Players={[0]={GetUnits=function() return collection end,GetCities=function() return {Members=function() return ipairs({c}) end} end}}
GameInfo={Units={[1]={UnitType='UNIT_SETTLER'},[2]={UnitType='UNIT_WARRIOR'}}}
Game={GetCurrentGameTurn=function() return turn end}
local P={IsTestPlayer=function(pid) return pid==0 end,Field=function(t,k) return t and t[k] end,
 CityRoleFacts=function() return {owner=0,cityID=7,governorGateStatus='KNOWN',governorLevelCeiling=1} end}
local shared
local function boot()
 Events={UnitRemovedFromMap=event(),LoadScreenClose=event()}
 shared={CityFlowProbe={SupportFacts=function() return cp(f) end}}
 SPCEffectiveFacts.Start(P,shared);SPCInvestmentAction.Start(P,shared)
end
local function reset() props={};units={};writes=0;kills=0;mode=nil;f.potential=1;f.specialization='RESEARCH';turn=1;boot() end
local function add(id)
 local up={};local u={x=4,y=5,kind=1}
 u.GetID=function() return id end;u.GetOwner=function() return 0 end
 u.GetX=function() return u.x end;u.GetY=function() return u.y end;u.GetType=function() return u.kind end
 u.GetProperty=function(_,k) return up[k] end;u.SetProperty=function(_,k,v) up[k]=v end
 units[id]=u;return u
end
local function prepare(id,token)
 local out=shared.InvestmentAction.Prepare(0,c,id,token or 'REQ');assert(out:find('PREPARED'),out)
 return shared.InvestmentPreview.token
end
reset()
for level=2,4 do
 add(level);local token=prepare(level)
 local n=writes;assert(n==(level-2)*3) -- Prepare performs no writes
 local out=shared.InvestmentAction.Confirm(0,c,token);assert(out:find('INVESTED'),out)
 assert(not units[level] and kills==level-1 and f.potential==1)
 assert(shared.EffectiveFacts.Read(0,c).potential==level and shared.EffectiveFacts.Read(0,c).active==1)
 local n=writes;assert(shared.InvestmentAction.Confirm(0,c,token):find('ALREADY_COMMITTED'));assert(writes==n and kills==level-1)
 boot();Events.LoadScreenClose.Fire();assert(writes==n and shared.EffectiveFacts.Read(0,c).potential==level)
end
add(5);assert(shared.InvestmentAction.Prepare(0,c,5,'REQ'):find('CAP'));assert(units[5] and kills==3)
reset();local u=add(1);u.kind=2
assert(shared.InvestmentAction.Prepare(0,c,1,'X'):find('NOT_A_SETTLER'));assert(writes==0 and kills==0)
u.kind=1;local token=prepare(1);u.x=9
assert(shared.InvestmentAction.Confirm(0,c,token):find('MOVE_SETTLER'));assert(writes==0 and kills==0)
u.x=4;token=prepare(1);turn=2
assert(shared.InvestmentAction.Confirm(0,c,token):find('EXPIRED'));assert(writes==0 and kills==0)
reset();add(1);token=prepare(1);Events.UnitRemovedFromMap.Fire(0,1);add(1)
assert(shared.InvestmentAction.Confirm(0,c,token):find('PREPARE_FIRST'));assert(kills==0)
reset();add(1);token=prepare(1);f.token='OTHER'
assert(shared.InvestmentAction.Confirm(0,c,token):find('PREVIEW_CHANGED'));assert(writes==0 and kills==0);f.token='T'
for _,failure in ipairs({'write1','write2','write3','noDelete'}) do
 reset();add(1);token=prepare(1);mode=failure
 local out=shared.InvestmentAction.Confirm(0,c,token);assert(out:find('HELD'),out)
 assert(shared.EffectiveFacts.Read(0,c).potential==1)
 local oldKills=kills;boot();mode=nil;Events.LoadScreenClose.Fire()
 if failure=='write3' then assert(shared.EffectiveFacts.Read(0,c).potential==2)
 else assert(shared.EffectiveFacts.Read(0,c).potential==1) end
 assert(kills==oldKills)
end
''')
# Actual UI dispatch sends selected-unit center and confirms the prepared city/token.
u=LuaRuntime(unpack_returned_tuples=True)
u.execute("""
include=function() end;Mouse={eLClick=1}
SPCP0={VERSION='P0-B-033',IsTestPlayer=function(i) return i==0 end,Scalar=tostring}
Controls={Status={SetText=function() end}};ContextPtr={ClearUpdate=function() end,SetUpdate=function() end}
Game={GetLocalPlayer=function() return 0 end,GetCurrentGameTurn=function() return 1 end}
ExposedMembers={SPC_P0={}};PlayerOperations={EXECUTE_SCRIPT=1}
city={GetOwner=function() return 0 end,GetID=function() return 7 end}
unit={GetOwner=function() return 0 end,GetID=function() return 8 end,GetX=function() return 4 end,GetY=function() return 5 end}
CityManager={GetCityAt=function(x,y) assert(x==4 and y==5);return city end}
Players={[0]={GetCities=function() return {FindID=function(_,id) assert(id==7);return city end} end}}
UI={GetHeadSelectedCity=function() return nil end,GetHeadSelectedUnit=function() return unit end,
 RequestPlayerOperation=function(pid,operation,params) sent=params end}
print=function() end
""")
request=u.execute((r/'UI/P0Panel.lua').read_text().split('local function copy(asBaseline)')[0]+'\nreturn request')
request('INVEST_PREPARE');u.execute("assert(sent.UnitID==8 and sent.CityID==7 and sent.Action=='INVEST_PREPARE')")
u.execute("ExposedMembers.SPC_P0.InvestmentPreview={owner=0,cityID=7,unitID=8,token='PLAN'}")
request('INVEST_CONFIRM');u.execute("assert(sent.PlanToken=='PLAN' and sent.CityID==7)")
# Actual Gameplay action dispatch retains the test-player/owned-city boundary.
u.execute("""
GameEvents={SPC_P0_Request={Add=function(f) dispatch=f end}}
""")
u.execute((r/'Gameplay.lua').read_text().split('shared.TradeEvents={}')[0])
u.execute("""
ExposedMembers.SPC_P0.InvestmentAction={Prepare=function(pid,c,id,t) assert(id==8);return 'PREPARED' end,
 Confirm=function(pid,c,t) assert(t=='PLAN');return 'INVESTED' end}
dispatch(0,{Action='INVEST_PREPARE',CityID=7,UnitID=8,Token='X'});assert(ExposedMembers.SPC_P0.Snapshot=='PREPARED')
dispatch(0,{Action='INVEST_CONFIRM',CityID=7,PlanToken='PLAN',Token='Y'});assert(ExposedMembers.SPC_P0.Snapshot=='INVESTED')
""")
for p in r.rglob('*.lua'):l.execute('assert(load(...))',p.read_text())
m=ET.parse(r/'SpecializationP0.modinfo').getroot();assert m.attrib['version']=='41' and m.attrib['id']=='df9efdad-dd48-40a7-b868-87f0617bc16d'
for e in m.findall('.//File'):assert (r/e.text).is_file()
x=ET.parse(r/'UI/P0Panel.xml');ids=[e.attrib['ID'] for e in x.iter() if 'ID' in e.attrib];assert len(ids)==len(set(ids))
assert {'InvestPrepareButton','InvestConfirmButton'}<=set(ids)
assert len(m.findall(".//ImportFiles/File[.='InvestmentAction.lua']"))==1
print('LOCAL_SIMULATION_PASS: actual native-action module and Property-shaped mocks; prepare no writes, 1→4, repeated receipts, normal reload, cap/type/location/turn/anchor/removal guards, debit/write ambiguity and confirmed-only recovery. Not native game proof.')
