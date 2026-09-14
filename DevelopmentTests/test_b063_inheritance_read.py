from pathlib import Path
from lupa.lua55 import LuaRuntime
R=Path(__file__).resolve().parents[1]
s=(R/'DevelopmentTests/test_b062_commerce.py').read_text().replace('"78","88"','"78","89"').replace("'\\\"78\\\",\\\"88\\\"'","'\\\"78\\\",\\\"89\\\"'").replace("get('version')=='88'","get('version')=='89'")
exec(compile(s,__file__,'exec'))
l=LuaRuntime(unpack_returned_tuples=True)
l.execute('''
props={SPC_DEV_BINDING_B013_TOKEN='token',SPC_DEV_CITY_JOURNAL_B015={owner=0,cityID=1,specialization='INDUSTRY'},SPC_DEV_INVESTMENT_LEDGER_V1={investments={a='unit1'}},SPC_STANDARDIZATION_LEDGER_V1={learned={building1=true}}}
owner=0;id=1;present=true;reads=0
city={GetOwner=function() return owner end,GetID=function() return id end,GetX=function() return 5 end,GetY=function() return 6 end,GetProperty=function(_,key) reads=reads+1;return props[key] end,SetProperty=function() error('forbidden write') end}
Players={[0]={GetDistricts=function() return {Members=function() return ipairs({}) end} end},[1]={GetDistricts=function() return {Members=function() return ipairs({}) end} end}}
P={IsTestPlayer=function(pid) return pid==0 end};CityManager={GetCityAt=function() return present and city or nil end};shared={}
''')
l.execute((M/'CityInheritanceRead.lua').read_text())
l.execute('''
SPCCityInheritanceRead.Start(P,shared);local d=shared.CityInheritanceRead
assert(not pcall(d.Read,0));assert(d.Record(0,city):find('投资笔数=1'))
owner=1;id=99;local s=d.Read(0);assert(s:find('0/1 → 当前=1/99') and s:find('TOKEN：原有 → 现有 | 内容一致'))
props.SPC_DEV_INVESTMENT_LEDGER_V1.investments.b='unit2';s=d.Read(0);assert(s:find('INVEST：原有 → 现有 | 内容不同'))
props.SPC_DEV_BINDING_B013_TOKEN=nil;s=d.Read(0);assert(s:find('TOKEN：原有 → 现无'))
present=false;assert(d.Read(0):find('当前无城市'));assert(not pcall(d.Read,1))
SPCCityInheritanceRead.Start(P,shared);assert(not pcall(shared.CityInheritanceRead.Read,0))
''')
print('B063 LOCAL_SIMULATION_PASS: read-only deep snapshots, owner/cityID change, raw properties retained/changed/lost, destroyed plot, disabled caller, load clears observation; B062 regressions pass. Native inheritance not implemented or proven.')
