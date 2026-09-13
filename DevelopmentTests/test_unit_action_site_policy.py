from pathlib import Path
from lupa.lua55 import LuaRuntime

w=Path(__file__).resolve().parents[1]
l=LuaRuntime(unpack_returned_tuples=True)
l.execute((w/"Sid Meier's Civilization VI/Mods/SpecializationP0/UnitActionSitePolicy.lua").read_text())
l.execute('''
local check=SPCUnitActionSitePolicy.Check
local u={owner=0,plot=10,isCrew=true,charges=1}
local t={verified=true,owner=0,plot=10,cityID=8,kind='BUILDING',current=true,complete=false}
for _,k in ipairs({'BUILDING','DISTRICT','WONDER'}) do t.kind=k;assert(check('CREW',u,t)) end
t.kind='PROJECT';assert(not check('CREW',u,t));t.kind='WONDER'
u.plot=11;assert(not check('CREW',u,t));u.plot=10
t.owner=1;assert(not check('CREW',u,t));t.owner=0
t.current=false;assert(not check('CREW',u,t));t.current=true
t.verified=false;assert(not check('CREW',u,t));t.verified=true
u.charges=2;assert(not check('CREW',u,t));u.charges=1
t.complete=true;assert(not check('CREW',u,t))
u.isSettler=true;t.kind='DISTRICT';t.identityAnchor=true;t.potential=2
assert(check('INVESTMENT',u,t))
t.identityAnchor=false;assert(not check('INVESTMENT',u,t));t.identityAnchor=true
t.complete=false;assert(not check('INVESTMENT',u,t));t.complete=true
t.potential=4;assert(not check('INVESTMENT',u,t));t.potential=3
t.plot=nil;assert(not check('INVESTMENT',u,t))
assert(not check('OTHER',u,t));assert(not check('CREW',nil,nil))
''')
print('LOCAL_SIMULATION_PASS: shared candidate site rules; no engine adapter, unit consumption or UI tested.')
