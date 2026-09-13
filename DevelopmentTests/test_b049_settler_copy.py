from pathlib import Path
import hashlib,json,xml.etree.ElementTree as E
from lupa.lua55 import LuaRuntime
w=Path(__file__).resolve().parents[1];r=w/"Sid Meier's Civilization VI/Mods/SpecializationP0";b=w/'DevelopmentBackups/Specialization-before-B049-settler-lv4/RuntimeSnapshot'
# Preserve whole investment transaction, Crew executor and all gameplay yield/catalog files.
assert (r/'InvestmentAction.lua').read_text().split(' function data.Prepare',1)[1]==(b/'InvestmentAction.lua').read_text().split(' function data.Prepare',1)[1]
assert (r/'UnitActions.lua').read_text().split(' function data.Run',1)[1]==(b/'UnitActions.lua').read_text().split(' function data.Run',1)[1]
for p in list(b.glob('Data/*.sql'))+[b/n for n in ['CrewProjects.lua','ConstructionProbe.lua','UnitTargets.lua','EffectiveFacts.lua','Lv4Percent.lua','Lv3Effects.lua']]:assert p.read_bytes()==(r/p.relative_to(b)).read_bytes(),p
# Reuse the actual Crew UI/executor regression, without legacy version/SQL harness.
s=(w/'DevelopmentTests/test_crew_ux.py').read_text();start=s.index('l=LuaRuntime');end=s.index('x=E.parse',start);fixture=s[start:end]
exec(compile(fixture,'B045_actual_crew_regression','exec'),globals())
# Reset actual shared state and UI to a Settler; use real InvestmentAction Prepare/Confirm.
l.execute('''
x=10;kills=0;grants=0;props={};uProps={};base=2;ledger=nil;owner=0;complete=true
u={GetOwner=function() return 0 end,GetID=function() return 1 end,GetType=function() return 1 end,
 GetX=function() return x end,GetY=function() return 0 end,GetProperty=function(_,k) return uProps[k] end,SetProperty=function(_,k,v) uProps[k]=v end}
c.GetOwner=function() return owner end;c.GetProperty=function() return ledger end;c.SetProperty=function(_,_,v) ledger=v end
GameInfo.Units[1]={UnitType='UNIT_SETTLER'}
P.Info=function(t,k) if t=='Units' then return {UnitType='UNIT_SETTLER'} else return {DistrictType='DISTRICT_CAMPUS'} end end
local district={GetCity=function() return c end,GetID=function() return 2 end,GetType=function() return 2 end,
 GetX=function() return 10 end,GetY=function() return 0 end,IsComplete=function() return complete end}
Players[0].GetDistricts=function() return {Members=function() return ipairs({district}) end} end
shared={Version=P.VERSION,EffectiveFacts={Read=function()
 local n=0;if ledger then for _ in pairs(ledger.investments) do n=n+1 end end
 return {owner=owner,cityID=8,token='CITY',first={districtID=2,type='DISTRICT_CAMPUS'},specialization='RESEARCH',potential=base+n,investmentCount=n,investmentPending=ledger and ledger.pending~=nil}
end,Describe=function() return 'facts' end},UnitTargets={Refresh=function() shared.UnitTargetSnapshot={plots={{plot=10,cityID=8}}} end}}
ExposedMembers.SPC_P0=shared;requests=0;actionRequests=0
''')
l.execute((r/'InvestmentAction.lua').read_text());l.execute('SPCInvestmentAction.Start(P,shared);SPCUnitActions.Start(P,shared)')
l.execute((r/'UI/UnitPanelActions.lua').read_text())
l.execute('''
init();tick(0.3);tick(0.3)
assert(Controls.PrepareButton.tip:find('当前潜力：2级 → 3级',1,true))
local pos=1000-Controls.ActionGroup.width+Controls.PrepareButton.offset
Controls.PrepareButton.click();Controls.PrepareButton.click();assert(actionRequests==1 and kills==0)
tick(0.3);tick(0.3)
assert(not Controls.ConfirmButton.hide and Controls.PrepareButton.tip:find('投资预览',1,true))
assert(Controls.PrepareButton.tip:find('当前专业：科研',1,true))
assert(not Controls.PrepareButton.tip:find('已准备',1,true))
assert(Controls.ConfirmButton.tip:find('永久提高至3级',1,true))
assert(pos==1000-Controls.ActionGroup.width+Controls.PrepareButton.offset)
assert(Controls.ConfirmButton.offset+44<Controls.PrepareButton.offset)
local count=actionRequests;Controls.PrepareButton.click();Controls.PrepareButton.click();assert(actionRequests==count and kills==0)
-- Potential/owner/location/completion invalidate only ephemeral previews.
base=3;tick(0.6);tick(0.3);assert(Controls.ConfirmButton.hide and shared.UnitActionPreview==nil and ledger==nil)
Controls.PrepareButton.click();tick(0.3);tick(0.3);assert(not Controls.ConfirmButton.hide)
x=11;tick(0.6);tick(0.3);assert(Controls.ConfirmButton.hide)
assert(Controls.PrepareButton.tip:find('将移民移动至本城的专业区域',1,true));Controls.PrepareButton.click();assert(kills==0)
x=10;tick(0.6);tick(0.3);Controls.PrepareButton.click();tick(0.3);tick(0.3)
complete=false;tick(0.6);tick(0.3);assert(Controls.ConfirmButton.hide)
complete=true;tick(0.6);tick(0.3);Controls.PrepareButton.click();tick(0.3);tick(0.3)
owner=1;tick(0.6);tick(0.3);assert(Controls.ConfirmButton.hide)
owner=0;base=4;tick(0.6);tick(0.3);assert(Controls.PrepareButton.tip:find('已达到4级',1,true))
Controls.PrepareButton.click();assert(kills==0 and ledger==nil)
base=2;tick(0.6);tick(0.3);Controls.PrepareButton.click();tick(0.3);tick(0.3)
Controls.ConfirmButton.click();assert(kills==1 and ledger and not ledger.pending)
local n=0;for _ in pairs(ledger.investments) do n=n+1 end;assert(n==1)
Controls.ConfirmButton.click();assert(kills==1)
''')
# Actual bridge accessor: multi-source dedup, direct and distribution, stale rejection.
p=w/'DevelopmentTests/test_lv3_effects.py';s=p.read_text();start=s.index("l.execute('''\nP.VERSION");end=s.index('p=w/"Firaxis',start)
exec(compile(s[start:end],'bridge_fixture','exec'),globals())
l.execute('''
bridgeFixture.shared.RouteSignalRevision=0
local a=b.RecipientSources(0,bridgeFixture.cities[3],'RESEARCH');assert(#a==2 and a[1]==1 and a[2]==2)
local z=b.RecipientSources(0,bridgeFixture.cities[4],'RESEARCH');assert(#z==2)
assert(#b.RecipientSources(0,bridgeFixture.cities[4],'INDUSTRY')==0)
routeCount=0;assert(not pcall(b.RecipientSources,0,bridgeFixture.cities[4],'RESEARCH'))
''')
# Copy calculations preserve fractions and choose actual maximum, not sum/max-level.
v=LuaRuntime(unpack_returned_tuples=True);v.execute((r/'Lv4CopyRead.lua').read_text());v.execute('''
assert(SPCLv4CopyRead.Half(5)==2.5)
local n,id=SPCLv4CopyRead.Maximum({{cityID=1,production=7},{cityID=2,production=12},{cityID=3,production=5}})
assert(n==6 and id==2)
assert(SPCLv4CopyRead.Maximum({{cityID=1,production=7}})==3.5)
assert(SPCLv4CopyRead.Maximum({})==0)
assert(not pcall(SPCLv4CopyRead.Half,0/0))
''')
# Actual renderer/metadata with changed yield samples, ACTIVE downgrade and missing source.
v.execute("""
Game={GetLocalPlayer=function() return 0 end,GetCurrentGameTurn=function() return 1 end};Locale={Lookup=function(x) return x end}
local cities={};for i=1,3 do cities[i]={GetID=function() return i end,GetOwner=function() return 0 end,GetName=function() return '城'..i end} end
local districts={};local rows={[1]={DistrictType='DISTRICT_CAMPUS',Name='学院'},[2]={DistrictType='DISTRICT_INDUSTRIAL_ZONE',Name='工业区'},[3]={DistrictType='DISTRICT_THEATER',Name='剧院'}}
local values={{SCIENCE=9},{PRODUCTION=7,CULTURE=1},{PRODUCTION=12}}
for i=1,3 do local d={};districts[i]=d;d.GetCity=function() return cities[i==1 and 1 or i] end
 d.GetID=function() return i end;d.GetType=function() return i==1 and 1 or 2 end;d.IsComplete=function() return true end
 d.GetYield=function(_,k) return values[i][k] or 0 end
end
P={IsTestPlayer=function() return true end,Families={DISTRICT_CAMPUS='RESEARCH',DISTRICT_INDUSTRIAL_ZONE='INDUSTRY'},Info=function(t,k)
 if t=='Districts' then return rows[k] end;return {Index=k:gsub('YIELD_','')} end}
Players={[0]={GetCities=function() return {FindID=function(_,id) return cities[id] end} end,GetDistricts=function() return {Members=function() return ipairs(districts) end} end}}
active=4;net=true
shared={EffectiveFacts={Read=function(_,c) return {specialization=c:GetID()==1 and 'RESEARCH' or 'INDUSTRY',active=c:GetID()==3 and active or 4,first={districtID=c:GetID()}} end},
NetworkBridge={RecipientSources=function() assert(net,'NETWORK_REFRESH_PENDING');return {2,3} end}}
local m=SPCLv4CopyRead.Metadata(P,shared,0,cities[1],'t')
assert(#m.sources==2);local text=SPCLv4CopyRead.Render(P,m);assert(text:find('max=6.0',1,true))
active=3;m=SPCLv4CopyRead.Metadata(P,shared,0,cities[1],'t2');assert(#m.sources==1)
assert(SPCLv4CopyRead.Render(P,m):find('max=3.5',1,true))
-- Attach the industrial district to the Research city: Campus Science9 must be excluded.
districts[2].GetCity=function() return cities[1] end;m.sources={}
text=SPCLv4CopyRead.Render(P,m);assert(text:find('非学院标准区域合计=8',1,true) and text:find('50%=4.0',1,true))
values[2].PRODUCTION=14;text=SPCLv4CopyRead.Render(P,m);assert(text:find('50%=7.5',1,true))
m.sources={{cityID=3,districtID=99}};assert(SPCLv4CopyRead.Render(P,m):find('SOURCE_DISTRICT_UNAVAILABLE',1,true))
net=false;m=SPCLv4CopyRead.Metadata(P,shared,0,cities[1],'t3');assert(m.networkError and #m.sources==0)
assert(SPCLv4CopyRead.Render(P,m):find('工业来源暂不可用',1,true))
""")
for p in r.rglob('*.lua'):v.execute('assert(load(...))',p.read_text())
for p in r.rglob('*.xml'):E.parse(p)
m=E.parse(r/'SpecializationP0.modinfo').getroot();assert m.get('version')=='62'
for f in m.findall('.//File'):assert (r/f.text).is_file()
assert hashlib.sha256((w/'Specialization/Design/Specialization_v0.1_Design_Spec.md').read_bytes()).hexdigest()=='2ba726ffeceb70f73ee1951fbeefb9cc4913f9e3eec2f27e634f122d8582a551'
print('LOCAL_SIMULATION_PASS B049: Crew regression; Settler fixed positions/inert repeat/potential-owner-site invalidation/cap/real one-unit commit; current network accessor; exact half/max; syntax/XML/manifest/protected gameplay/design unchanged.')
