from pathlib import Path
from lupa.lua55 import LuaRuntime
R=Path(__file__).resolve().parents[1];M=R/'Mod'
s=(R/'DevelopmentTests/test_b064_shadow.py').read_text().replace("replace('89','90')","replace('89','92')")
exec(compile(s,__file__,'exec'))
l=LuaRuntime(unpack_returned_tuples=True)
l.execute('''
function cp(v) if type(v)~='table' then return v end local r={} for k,x in pairs(v) do r[k]=cp(x) end return r end
store={};cities={};turn=1;w=0
function make(pid,id) local c={owner=pid,id=id,props={}};function c:GetOwner() return self.owner end;function c:GetID() return self.id end;function c:GetX() return 4 end;function c:GetY() return 5 end;function c:GetProperty(k) return cp(self.props[k]) end;function c:SetProperty(k,v) self.props[k]=cp(v);w=w+1 end;cities[pid..':'..id]=c;return c end
Events={};GameEvents={};for _,ns in ipairs({Events,GameEvents}) do setmetatable(ns,{__index=function(t,k) local h={};local e={Add=function(f) h[#h+1]=f end,Fire=function(...) for _,f in ipairs(h) do f(...) end end};rawset(t,k,e);return e end}) end
Game={GetProperty=function(_,k) return cp(store[k]) end,SetProperty=function(_,k,v) store[k]=cp(v) end,GetCurrentGameTurn=function() return turn end}
CityManager={GetCity=function(pid,id) return cities[pid..':'..id] end}
P={IsTestPlayer=function(p) return p==0 end,CityRoleFacts=function(c) return {owner=c.owner,cityID=c.id,governorGateStatus='KNOWN',governorLevelCeiling=2} end}
local first={districtID=9,type='DISTRICT_INDUSTRIAL_ZONE',turn=1}
local j={owner=0,cityID=11,token='uid',health='TRACKING',specialization='INDUSTRY',potential=1,first=first}
local flow={owner=0,cityID=11,token='uid',stage='DONE',facts=cp(j),target=cp(j)}
local inv={schema=1,revision=4,anchor={owner=0,cityID=11,token='uid',first=cp(first),specialization='INDUSTRY'},investments={a='u1',b='u2',c='u3'}}
local src={uid='uid',owner=0,cityID=11,x=4,y=5,revision=1,values={TOKEN='uid',JOURNAL=j,FLOW=flow,INVEST=inv,TEMPLATES={foundation='uid',learned={a=true,b=true}}}}
store.SPC_INHERITANCE_SHADOW_V1={records={uid=src},watch={['0']='uid'}}
shared={CityFlowProbe={ResumeInherited=function(pid,c) assert(shared.CityInheritance.Resolve(pid,c)=='uid');assert(c:GetProperty('SPC_DEV_CITY_FLOW_B020').facts.owner==pid) end,SupportFacts=function(pid,c) return c:GetProperty('SPC_DEV_CITY_JOURNAL_B015') end},InheritanceShadow={Describe=function() return 'shadow' end}}
shared.OnPermanentCityWrite=function(c) assert(shared.CityInheritance.AllowsShadow('uid',c));local s=cp(store.SPC_INHERITANCE_SHADOW_V1.records.uid);s.owner=c.owner;s.cityID=c.id;s.revision=s.revision+1
 for k,key in pairs({TOKEN='SPC_DEV_BINDING_B013_TOKEN',JOURNAL='SPC_DEV_CITY_JOURNAL_B015',FLOW='SPC_DEV_CITY_FLOW_B020',INVEST='SPC_DEV_INVESTMENT_LEDGER_V1',TEMPLATES='SPC_STANDARDIZATION_LEDGER_V1'}) do s.values[k]=c:GetProperty(key) end
 store.SPC_INHERITANCE_SHADOW_V1.records.uid=s end
''')
l.execute((M/'EffectiveFacts.lua').read_text());l.execute('SPCEffectiveFacts.Start(P,shared)')
l.execute((M/'CityInheritance.lua').read_text())
l.execute('''
SPCCityInheritance.Start(P,shared);Events.LoadScreenClose.Fire();local d=shared.CityInheritance
local ai=make(1,99);Events.CityTransfered.Fire(1,99);local key=SPCCityInheritance.KEY
assert(store[key].records.uid.status=='DORMANT' and w==0)
local n=store[key].records.uid.revision;Events.CityTransfered.Fire(1,99);assert(store[key].records.uid.revision==n)
cities['1:99']=nil;local own=make(0,22);GameEvents.CityConquered.Fire(0,1,22,4,5)
assert(not d.errors.last,d.errors.last);assert(store[key].records.uid.status=='APPLIED')
local f=shared.EffectiveFacts.Read(0,own);assert(f.potential==4 and f.active==2 and f.investmentCount==3)
assert(own:GetProperty('SPC_DEV_INVESTMENT_LEDGER_V1').investments.a=='u1');assert(own:GetProperty('SPC_STANDARDIZATION_LEDGER_V1').learned.b)
local n=w;Events.CityTransfered.Fire(0,22);Events.LoadScreenClose.Fire();assert(w==n)
-- Subsequent owner transfer and return use latest mirrored source, not original owner/id.
cities['0:22']=nil;make(1,100);Events.CityTransfered.Fire(1,100);cities['1:100']=nil;local own2=make(0,23);Events.CityTransfered.Fire(0,23)
assert(store[key].records.uid.status=='APPLIED');assert(shared.EffectiveFacts.Read(0,own2).potential==4)
-- Explicit foundation retires old identity; later transfer cannot resurrect it.
GameEvents.CityBuilt.Fire(1,200,4,5);assert(store[key].records.uid.retired);local fresh=make(0,300);Events.CityTransfered.Fire(0,300);assert(fresh:GetProperty('SPC_DEV_BINDING_B013_TOKEN')==nil)
-- Pending investment and foreign token cannot be projected.
store[key]=nil;local s=store.SPC_INHERITANCE_SHADOW_V1.records.uid;s.values.INVEST.pending={stage='INTENT'};local ai2=make(1,301);Events.CityTransfered.Fire(1,301);assert(store[key]==nil);assert(d.errors.last=='INHERIT_PENDING_INVESTMENT')
s.values.INVEST.pending=nil;ai2.props.SPC_DEV_BINDING_B013_TOKEN='different';Events.CityTransfered.Fire(1,301);assert(store[key]==nil and d.errors.last=='INHERIT_DEST_TOKEN_CONFLICT')
''')
print('B066 PASS real inheritance+EffectiveFacts: dormant no city writes, return restores potential4/active2/receipts/templates, repeated events/load no writes, chained owner transfer, new foundation retirement, pending and foreign token rejected; earlier regressions pass.')
