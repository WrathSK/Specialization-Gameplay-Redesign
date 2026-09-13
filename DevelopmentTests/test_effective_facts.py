from pathlib import Path
from lupa.lua55 import LuaRuntime
import xml.etree.ElementTree as ET
w=Path(__file__).resolve().parent;r=w.parent/"Sid Meier's Civilization VI/Mods/SpecializationP0"
l=LuaRuntime(unpack_returned_tuples=True);l.execute((r/'EffectiveFacts.lua').read_text())
l.execute('''
local f={owner=0,cityID=7,token='T',specialization='RESEARCH',potential=1,first={districtID=3,type='DISTRICT_CAMPUS'}}
local saved;local ceiling=4
local c={GetOwner=function() return 0 end,GetID=function() return 7 end,
 GetProperty=function(_,key) assert(key=='SPC_DEV_INVESTMENT_LEDGER_V1');return saved end,
 SetProperty=function() error('WRITE_FORBIDDEN') end}
local shared={CityFlowProbe={SupportFacts=function() return f end}}
local P={IsTestPlayer=function(i) return i==0 end,CityRoleFacts=function() return {owner=0,cityID=7,governorGateStatus='KNOWN',governorLevelCeiling=ceiling} end}
SPCEffectiveFacts.Start(P,shared);local api=shared.EffectiveFacts
local x=api.Read(0,c);assert(x.potential==1 and x.active==1 and saved==nil)
saved={schema=1,anchor={owner=0,cityID=7,token='T',specialization='RESEARCH',first=f.first},revision=4,investments={A='U1',B='U2',C='U3'}}
x=api.Read(0,c);assert(x.potential==4 and x.active==4 and f.potential==1)
ceiling=1;assert(api.Read(0,c).active==1 and api.Read(0,c).potential==4)
ceiling=nil;assert(api.Read(0,c).active==nil and api.Read(0,c).activeStatus=='UNKNOWN_GOVERNOR')
saved.investments.D='U3';assert(not pcall(api.Read,0,c));saved.investments.D=nil
saved.anchor.token='BAD';assert(not pcall(api.Read,0,c));saved.anchor.token='T'
saved.pending={stage='INTENT'};assert(not pcall(api.Read,0,c));saved.pending=nil
saved.revision=3;assert(not pcall(api.Read,0,c));saved.revision=4
assert(not pcall(api.Read,1,c))
saved=nil;f.specialization='NONE';f.potential=0;f.first=nil
assert(api.Read(0,c).active==0 and api.Read(0,c).potential==0)
assert(api.Describe(0,c):find('No Settler consumed',1,true))
''')
# Exercise existing full topology regression using the real new reader, complete fixture foundations.
t=(w/'test_network_report_withdrawal.py').read_text().split("l.execute('''",1)[1].split("''')",1)[0]
t=t.replace("local P={IsTestPlayer", "for i,c in pairs(cities) do c.GetProperty=function() return nil end;c.SetProperty=function() error('WRITE_FORBIDDEN') end end\nlocal originalFacts=shared.CityFlowProbe.SupportFacts\nshared.CityFlowProbe.SupportFacts=function(pid,c) local f=originalFacts(pid,c);f.owner=pid;f.cityID=c:GetID();f.token='T'..c:GetID();f.first={districtID=c:GetID(),type='MOCK'};if not f.specialization then f.specialization='NONE';f.potential=0;f.first=nil end;return f end\nlocal P={IsTestPlayer")
t=t.replace('SPCNetworkBridge.Start(P,shared);onLoad()', 'SPCEffectiveFacts.Start(P,shared);SPCNetworkBridge.Start(P,shared);onLoad()',1)
l=LuaRuntime(unpack_returned_tuples=True)
for name in ['EffectiveFacts.lua','NetworkBridge.lua']:l.execute((r/name).read_text())
l.execute(t.replace('-- Malformed/partial complete packet', '''
local foundation=shared.CityFlowProbe.SupportFacts(0,cities[1])
cities[1].GetProperty=function() return {schema=1,anchor={owner=0,cityID=1,token=foundation.token,first=foundation.first,specialization='RESEARCH'},revision=4,investments={A='U1',B='U2',C='U3'}} end
P.CityRoleFacts=function(c) return {owner=0,cityID=c:GetID(),governorGateStatus='KNOWN',governorLevelCeiling=4} end
send('0,1,0,2,10',1);check(2,'RESEARCH',2,true)
assert(b.players[0].sources[1]=='RESEARCH')
-- Malformed/partial complete packet'''))
# Actual Lv1 lifecycle fixture with the new reader installed before consumers.
import lupa
lupa.LuaRuntime=LuaRuntime
ns={'__file__':str(w/'test_auto_support_scan_fix.py')}
exec((w/'test_auto_support_scan_fix.py').read_text().split('\nl=LuaRuntime(')[0],ns)
f=ns['f'].replace('local function start() SPCResearchSupport.Start(P,s) end','local function start() SPCEffectiveFacts.Start(P,s);SPCResearchSupport.Start(P,s) end')
l=LuaRuntime(unpack_returned_tuples=True)
for name in ['BindingProbe.lua','CityJournalProbe.lua','FreshBindingHook.lua','CityFlowProbe.lua','EffectiveFacts.lua','ResearchSupport.lua']:l.execute((r/name).read_text())
l.execute(f+"""
local foundation=s.CityFlowProbe.SupportFacts(0,city)
local oldProperty=city.GetProperty
city.GetProperty=function(self,key)
 if key=='SPC_DEV_INVESTMENT_LEDGER_V1' then return {schema=1,
 anchor={owner=foundation.owner,cityID=foundation.cityID,token=foundation.token,first=foundation.first,specialization=foundation.specialization},
 revision=4,investments={A='U1',B='U2',C='U3'}} end
 return oldProperty(self,key)
end
P.CityRoleFacts=function() return {owner=0,cityID=city:GetID(),governorGateStatus='KNOWN',governorLevelCeiling=1} end
assert(s.EffectiveFacts.Read(0,city).potential==4 and s.EffectiveFacts.Read(0,city).active==1)
s.ResearchSupport.Audit();assert(present[444])
""")
for p in r.rglob('*.lua'):l.execute('assert(load(...))',p.read_text())
m=ET.parse(r/'SpecializationP0.modinfo').getroot();assert m.attrib['version']=='40' and m.attrib['id']=='df9efdad-dd48-40a7-b868-87f0617bc16d'
for x in m.findall('.//File'):assert (r/x.text).is_file()
assert len(m.findall(".//ImportFiles/File[.='EffectiveFacts.lua']"))==1
ET.parse(r/'UI/P0Panel.xml')
print('LOCAL_SIMULATION_PASS: effective ledger validation/no writes; Potential/ACTIVE distinction; real network reader integration and full topology/withdrawal regression; actual Lv1 lifecycle/new city/load/invalid player scan regression. No game proof.')
