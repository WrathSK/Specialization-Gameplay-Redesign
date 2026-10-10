"""B174: actual investment producer, normal-unit transport and two actual writers.

Mock native/Property surfaces, actual SQL and Shared D fixtures. No game, external
DB, deployment or native performance claim. Frozen legacy tests stay untouched.
Requires lupa.lua55 and Git baseline 4a62deb (the accepted B173 checkpoint).
"""
from pathlib import Path
import subprocess
import unittest
import xml.etree.ElementTree as ET

from test_b138_update_contract import fixture_through_function, check_dispatch, check_batches, check_gpp_ownership, check_late_ui_and_dispatch

R = Path(__file__).resolve().parents[1]
M = R / 'Mod'
BASE = '4a62deb6b0657569b2cf3660c409fb8a5d814506'
CHANGED = {'Gameplay', 'InvestmentAction', 'UnitActions', 'RuntimeWork', 'Lv2Housing', 'Lv2GPP'}
NS = fixture_through_function(R / 'DevelopmentTests/test_p0_b2.py', 'runtime')
OLD = {}


def source(name, old=False):
    if old and name in CHANGED:
        if name not in OLD:
            OLD[name] = subprocess.check_output(['git', 'show', BASE + ':Mod/' + name + '.lua'], cwd=R, text=True)
        return OLD[name]
    return (M / (name + '.lua')).read_text()


def fixture(n=2, old=False):
    # Only the old test's native fixtures/SQL are reused, not its obsolete build
    # assertions, full-runtime baseline equality or stress loops.
    l = NS['ns']['runtime']()
    l.globals().print = lambda *args: None
    l.globals().include = lambda name: l.execute(source(name, old))
    l.globals().cr = NS['ns']['to_lua'](l, NS['carriers'])
    l.globals().pr = NS['ns']['to_lua'](l, NS['points'])
    l.execute("for _,b in ipairs(cr)do brows[#brows+1]=b end;GameInfo.Buildings=db(brows,'BuildingType');GameInfo.Building_GreatPersonPoints=db(pr,'BuildingType')")
    l.execute(NS['AUGMENT'])
    for i in range(2, n + 1):
        l.execute(f"local nc=newCity({i});wrap(nc);addDistrict(nc,{10+i},'DISTRICT_CAMPUS')")
    l.execute(r'''
function cp(v)if type(v)~='table'then return v end;local r={};for k,x in pairs(v)do r[k]=cp(x)end;return r end
function encode(v)
 if type(v)~='table'then return tostring(v)end
 local keys={};for k in pairs(v)do keys[#keys+1]=k end;table.sort(keys,function(a,b)return tostring(a)<tostring(b)end)
 local t={};for _,k in ipairs(keys)do t[#t+1]=tostring(k)..'='..encode(v[k])end;return '{'..table.concat(t,';')..'}'
end
local KEY='SPC_DEV_INVESTMENT_LEDGER_V1'
ledgerWrites=0;kills=0;units={};audits={};otherCalls={};members=0;finds=0
P.IsTestPlayer=function(p)return p==0 end
P.Scalar=tostring;P.CrewBase=function()return nil end
P.Observe=function(k,n)if k=='audit'then audits[n]=(audits[n]or 0)+1 end end
P.SetProperty=function(o,k,v)return o:SetProperty(k,v)end
P.GovernorGate=function(c)return c.owner,c.id,c.gateKnown==false and 'UNKNOWN' or 'KNOWN',c.governor or 4 end
for _,v in pairs(cities)do
 v.identity='RESEARCH';v.active=1;v.governor=4
 v.SetProperty=function(_,key,value)
  assert(key==KEY);ledgerWrites=ledgerWrites+1
  if fault=='throw'..ledgerWrites then error('SETTER_FAILED')end
  if fault~='drop'..ledgerWrites then v.ledger=cp(value)end
  if fault=='third'..ledgerWrites then v.ledger={bad=true}end
  if afterWrite then afterWrite(v,ledgerWrites)end
  if fault=='after'..ledgerWrites then error('AFTER_WRITE_FAILED')end
 end
 v.GetProperty=function(_,key)
  if fault=='get'..ledgerWrites then error('GETTER_FAILED')end
  return key==KEY and cp(v.ledger)or nil
 end
end
shared.CityFlowProbe={SupportFacts=function(pid,c)
 if c.factsError then error('TEMPORARY_FLOW')end
 return {owner=c.owner,cityID=c.id,token=c.token,specialization=c.identity,potential=c.identity=='NONE'and 0 or 1,
  first=cp(c.first or {districtID=c.ds[1].id,type=GameInfo.Districts[c.ds[1].type].DistrictType})}
end}
Players[0].GetCities=function()return {
 Members=function()members=members+1;return pairs(cities)end,
 FindID=function(_,id)finds=finds+1;return cities[id]end}end
Players[0].GetUnits=function()return {
 FindID=function(_,id)return units[id]end,
 Destroy=function(_,u)
  kills=kills+1;if fault=='noDelete'then return end
  units[u.id]=nil;fire('UnitRemovedFromMap',0,u.id)
  if afterDestroy then afterDestroy()end
 end}end
GameInfo.Units=db({{Index=1,UnitType='UNIT_SETTLER'}},'UnitType')
function addUnit(id,city,site)
 local u={id=id,x=site and city.ds[1]:GetX()or city.x,y=site and city.ds[1]:GetY()or city.y,props={}}
 u.GetID=function()return id end;u.GetOwner=function()return 0 end;u.GetType=function()return 1 end
 u.GetX=function()return u.x end;u.GetY=function()return u.y end
 u.GetProperty=function(_,k)return u.props[k]end
 u.SetProperty=function(_,k,v)u.props[k]=v end
 units[id]=u;return u
end
shared.UnitTargets={Refresh=function(pid,params)
 local list={};for _,c in pairs(cities)do list[#list+1]={plot=c.ds[1].plot,cityID=c.id}end
 shared.UnitTargetSnapshot={plots=list}
end}
stage=function()end
shared.NetworkBridge={Refresh=function(pid)otherCalls.network=(otherCalls.network or 0)+1 end}
for _,name in ipairs({'ResearchInfrastructure','ResearchCross','ResearchApply','ResearchChair','CultureAesthetic','CultureMeaning',
 'CultureInspiration','ResearchSupport','IndustrySupport','Lv3Effects','NetworkBoost','Lv4Percent'})do
 shared[name]={Audit=function(scope)otherCalls[name]=(otherCalls[name]or 0)+1 end}
end
shared.Dialogue={Audit=function()otherCalls.Dialogue=(otherCalls.Dialogue or 0)+1 end}
function resetCounts()counters={};audits={};otherCalls={};members=0;finds=0;reads=0;writes=0 end
function values()
 local r={};for id,c in pairs(cities)do r[id]={ledger=c.ledger,carriers=c.carriers}end
 return encode(r)..' kills='..kills
end
''')
    for name in ['EffectiveFacts', 'InvestmentAction', 'UnitActions', 'Lv2Housing', 'Lv2GPP']:
        l.execute(source(name, old)); l.execute(f'SPC{name}.Start(P,shared)')
    l.execute('shared.Lv2Housing.ready=true;shared.Lv2GPP.ready=true;P.Info0=P.Info;P.Info=function(t,k)return P.Info0(t,k)end')
    code = source('Gameplay', old)
    marker = 'local function request(' if old else 'local function refreshInvestmentSupport('
    l.execute(code[code.index(marker):code.index('GameEvents.SPC_P0_Request.Add')] + '\nrunRequest=request\n' + ('' if old else 'notify=refreshInvestmentSupport'))
    l.execute(r'''
function prepare(city,id,normal)
 addUnit(id,city,normal)
 local params={Action=normal and 'UNIT_ACTION_PREPARE'or 'INVEST_PREPARE',UnitID=id,Token='p'..id}
 if not normal then params.CityID=city.id end
 runRequest(0,params)
 assert(shared.InvestmentPreview,shared.Snapshot)
 return shared.InvestmentPreview.token
end
function confirm(city,id,token,normal)
 local params={Action=normal and 'UNIT_ACTION_CONFIRM'or 'INVEST_CONFIRM',UnitID=id,PlanToken=token,Token='c'..id}
 if not normal then params.CityID=city.id end
 runRequest(0,params)
 return shared.Snapshot
end
function invest(city,id,normal)
 local t=prepare(city,id,normal);resetCounts();return confirm(city,id,t,normal)
end
''')
    return l


class InvestmentPropagation(unittest.TestCase):
    def test_actual_two_entrances_values_and_scaling(self):
        for normal in (False, True):
            for count in (8, 20, 40):
                with self.subTest(normal=normal, cities=count):
                    before, after = fixture(count, True), fixture(count)
                    for l in (before, after):
                        l.execute(f"assert(invest(c,301,{str(normal).lower()}):find('INVESTED'));assert(housing(c)==1 and gpp(c,'RESEARCH')==6)")
                    self.assertEqual(before.eval('values()'), after.eval('values()'))
                    self.assertEqual(before.eval('counters.city_scan'), 2 * count)
                    self.assertEqual(after.eval('counters.city_scan'), 2)
                    self.assertEqual(after.eval('members'), 0)
                    self.assertEqual(before.eval('encode(otherCalls)'), after.eval('encode(otherCalls)'))
                    print('SCALING', 'UNIT' if normal else 'DEV', count,
                          {k: (before.eval(k), after.eval(k)) for k in ('counters.city_scan','counters.facts','counters.district_scan','reads','writes','members')})

    def test_per_value_four_kinds_governor_workers_buildings(self):
        for kind, district in [('RESEARCH','CAMPUS'),('CULTURE','THEATER'),('INDUSTRY','INDUSTRIAL_ZONE'),('COMMERCE','COMMERCIAL_HUB')]:
            for gate in (1, 2, 4):
                for workers in (0, 1, 4):
                    with self.subTest(kind=kind, gate=gate, workers=workers):
                        a,b=fixture(old=True),fixture()
                        for l in (a,b):
                            l.execute(f"c.identity='{kind}';d.type=GameInfo.Districts.DISTRICT_{district}.Index;d.workers={workers};c.governor={gate};assert(invest(c,300,false):find('INVESTED'))")
                        self.assertEqual(a.eval('values()'), b.eval('values()'))
                        self.assertEqual(b.eval(f"gpp(c,'{kind}')"), 2*workers if gate>=2 else 0)
                        self.assertEqual(b.eval('housing(c)'), 1 if gate>=2 else 0)
        l=fixture();l.execute("setBuildings(d,{'BUILDING_LIBRARY','BUILDING_UNIVERSITY'});invest(c,400,false);assert(housing(c)==3)")

    def test_same_turn_investments_workers_and_governor(self):
        l=fixture();l.execute("invest(c,400,true);invest(c,401,true);assert(kills==2 and shared.EffectiveFacts.Read(0,c).potential==3)")
        l.execute("d.workers=4;fire('CityWorkerChanged',0);assert(gpp(c,'RESEARCH')==8);c.governor=1;fire('GovernorChanged',0);assert(housing(c)==0 and gpp(c,'RESEARCH')==0);c.governor=3;fire('GovernorChanged',0);assert(housing(c)==1 and gpp(c,'RESEARCH')==8)")

    def test_typed_commit_and_already_committed_no_second_debit(self):
        for normal in (False, True):
            l=fixture();l.execute(f"t=prepare(c,500,{str(normal).lower()});local out,e=shared.{'UnitActions.Run(0,{Action=\'UNIT_ACTION_CONFIRM\',UnitID=500,PlanToken=t})' if normal else 'InvestmentAction.Confirm(0,c,t)'};evidence=e;assert(e.status=='COMMITTED' and e.player==0 and e.city==1 and e.reference.x==c.x and e.anchor.token==c.token and e.receipt==t and e.revision==2)")
            l.execute("local w=ledgerWrites;local out,e=shared.InvestmentAction.Confirm(0,c,t);assert(e.status=='ALREADY_COMMITTED' and kills==1 and ledgerWrites==w);resetCounts();notify(0,e);assert(counters.city_scan==4)")

    def test_rejected_preview_unknown_and_unrelated_keep_player_fallback(self):
        for result in ('nil', "{status='REJECTED'}", "{status='ALREADY_COMMITTED'}", "{status='UNKNOWN'}"):
            l=fixture(4);l.execute(f"resetCounts();notify(0,{result});assert(counters.city_scan==8)")
        for normal in (False, True):
            l=fixture(3);l.execute(f"prepare(c,510,{str(normal).lower()});assert(counters.city_scan==6 and kills==0 and ledgerWrites==0);resetCounts();confirm(c,510,'WRONG',{str(normal).lower()});assert(counters.city_scan==6 and kills==0)")

    def test_commit_proof_not_display_or_debit(self):
        cases={'drop1':0,'drop2':1,'drop3':1,'throw1':0,'throw2':1,'throw3':1,'get3':1,'third3':1,'noDelete':1}
        for fault,kills in cases.items():
            with self.subTest(fault=fault):
                l=fixture();l.execute(f"t=prepare(c,520,false);fault='{fault}';out,evidence=shared.InvestmentAction.Confirm(0,c,t);assert(evidence.status=='UNKNOWN');assert(kills=={kills});local k=kills;shared.InvestmentAction.Confirm(0,c,t);assert(kills==k)")

    def test_actual_readback_can_prove_commit_after_setter_or_report_exception(self):
        for fail in ("fault='after3'", "shared.EffectiveFacts.Describe=function()error('REPORT_FAILED')end"):
            l=fixture();l.execute(f"t=prepare(c,530,false);{fail};out,evidence=shared.InvestmentAction.Confirm(0,c,t);assert(out:find('HELD') and evidence.status=='COMMITTED');resetCounts();notify(0,evidence);assert(housing(c)==1 and gpp(c,'RESEARCH')==6 and counters.city_scan==2 and kills==1)")

    def test_unit_transport_keeps_commit_when_report_throws(self):
        l=fixture();l.execute("t=prepare(c,535,true);shared.EffectiveFacts.Describe=function()error('REPORT_FAILED')end;local out,e=shared.UnitActions.Run(0,{Action='UNIT_ACTION_CONFIRM',UnitID=535,PlanToken=t});assert(out:find('HELD') and e.status=='COMMITTED');notify(0,e);assert(housing(c)==1)")

    def test_reference_changed_during_commit_or_ledger_ambiguous(self):
        for change in ("v.x=v.x+1", "v.token='NEW'", "v.owner=3", "v.ledger.pending={bad=true}"):
            l=fixture();l.execute(f"t=prepare(c,540,false);afterWrite=function(v,n)if n==3 then {change};end end;local out,e=shared.InvestmentAction.Confirm(0,c,t);assert(e.status=='UNKNOWN' and kills==1)")

    def test_reentrant_confirmation_is_held(self):
        l=fixture();l.execute("t=prepare(c,550,false);afterDestroy=function()local _,e=shared.InvestmentAction.Confirm(0,c,t);assert(e.status=='UNKNOWN')end;local out,e=shared.InvestmentAction.Confirm(0,c,t);assert(e.status=='UNKNOWN' and kills==1 and shared.EffectiveFacts.Read(0,c).potential==1)")

    def test_target_read_rejects_wrong_owner_token_reference_and_unknown(self):
        for change in ("c.owner=3", "c.token='NEW'", "c.x=c.x+1", "c.factsError=true", "cities[1]=nil", "evidence.player=1", "evidence.city='1'", "evidence.anchor=nil"):
            with self.subTest(change=change):
                l=fixture();l.execute("t=prepare(c,560,false);_,evidence=shared.InvestmentAction.Confirm(0,c,t);notify(0,evidence);other=cities[2];shared.Lv2Housing.errors['0:2']='retain';shared.Lv2GPP.errors['0:2']='retain';resetCounts()")
                l.execute(change+";notify(0,evidence);assert(writes==0 and (counters.city_scan or 0)==0);assert(shared.Lv2Housing.errors['investment:0'] and shared.Lv2GPP.errors['investment:0']);assert(shared.Lv2Housing.errors['0:2']=='retain' and shared.Lv2GPP.errors['0:2']=='retain');assert(housing(c)==1)")

    def test_consumer_isolation_and_no_effect_replay(self):
        l=fixture();l.execute("t=prepare(c,570,false);_,evidence=shared.InvestmentAction.Confirm(0,c,t);local old=shared.Lv2Housing.Audit;shared.Lv2Housing.Audit=function()error('CONSUMER_FAILED')end;notify(0,evidence);assert(gpp(c,'RESEARCH')==6 and shared.Lv2Housing.errors['investment-notify:0']);assert(kills==1 and ledgerWrites==3);shared.Lv2Housing.Audit=old;notify(0,evidence);assert(housing(c)==1 and not shared.Lv2Housing.errors['investment-notify:0']);local w=writes;notify(0,evidence);assert(writes==w and kills==1 and ledgerWrites==3)")

    def test_each_consumer_rechecks_current_facts_after_previous_writer(self):
        l=fixture();l.execute("t=prepare(c,580,false);_,evidence=shared.InvestmentAction.Confirm(0,c,t);local create=P.CreateBuilding;P.CreateBuilding=function(...)create(...);c.gateKnown=false end;notify(0,evidence);assert(housing(c)==1 and gpp(c,'RESEARCH')==0 and shared.Lv2GPP.errors['0:1'])")

    def test_native_hooks_batch_and_ui_contracts_inherited(self):
        check_dispatch(M);check_batches(M);check_gpp_ownership(R);check_late_ui_and_dispatch(R)

    def test_current_store_commits_and_local_isolation(self):
        from test_store_write_boundaries import fixture as store_fixture
        l=store_fixture();l.execute("local x,y=T.two();T.invest(x,801);assert(T.control(x).potential==2 and T.control(y).potential==1);T.reload();assert(T.control(x).potential==2 and T.control(y).potential==1)")

    def test_actual_store_readback_failure_stays_unknown(self):
        from test_store_write_boundaries import fixture as store_fixture
        l=store_fixture();l.execute("local x,y=T.two();addunit(802,x);shared.InvestmentAction.Prepare(0,x,802,'FAIL',false);local token=shared.InvestmentPreview.token;T.failKey(T.key(x));local _,e=shared.InvestmentAction.Confirm(0,x,token);assert(e.status=='UNKNOWN');assert(T.control(y).potential==1)")

    def test_actual_store_final_throw_is_not_proved_from_raw_saved_bytes(self):
        from test_store_write_boundaries import fixture as store_fixture
        l=store_fixture();l.execute("local x,y=T.two();addunit(811,x);shared.InvestmentAction.Prepare(0,x,811,'FAIL',false);local token=shared.InvestmentPreview.token;local setter=Game.SetProperty;local key=T.key(x);Game.SetProperty=function(self,k,v)setter(self,k,v);if k==key and v.investment and not v.investment.pending then error('AFTER_STORE_WRITE')end end;local _,e=shared.InvestmentAction.Confirm(0,x,token);assert(e.status=='UNKNOWN');assert(T.control(y).potential==1)")

    def test_reference_change_during_consumer_fact_read_is_held(self):
        l=fixture();l.execute("t=prepare(c,820,false);_,evidence=shared.InvestmentAction.Confirm(0,c,t);local read=shared.EffectiveFacts.Read;shared.EffectiveFacts.Read=function(...)local f=read(...);c.x=c.x+1;return f end;notify(0,evidence);assert(writes==0 and shared.Lv2Housing.errors['investment:0'] and shared.Lv2GPP.errors['investment:0'])")

    def test_readback_reentrancy_cannot_publish_committed(self):
        l=fixture();l.execute("t=prepare(c,830,false);local read=c.GetProperty;local count=0;c.GetProperty=function(...)local v=read(...);if ledgerWrites==3 then count=count+1;if count==3 then shared.InvestmentAction.Confirm(0,c,t)end end;return v end;local _,e=shared.InvestmentAction.Confirm(0,c,t);assert(e.status=='UNKNOWN' and kills==1)")

    def test_actual_construction_team_transport_remains_unscoped(self):
        results=[]
        for old in (True,False):
            l=fixture(old=old);l.execute("""
local props={};local crew={Index=2,UnitType='UNIT_SPC_CREW_250'};GameInfo.Units[2]=crew;GameInfo.Units.UNIT_SPC_CREW_250=crew
Players[0].GetProperty=function(_,k)return cp(props[k])end;Players[0].SetProperty=function(_,k,v)props[k]=cp(v)end
P.CrewBase=function(k)return k=='UNIT_SPC_CREW_250'and 250 or nil end;P.CrewAmount=P.CrewBase
local u=addUnit(901,c,true);u.GetType=function()return 2 end;u.GetBuildCharges=function()return 1 end
progress=30;shared.ConstructionProbe={ReadSnapshot=function()return {kind='Buildings',target='BUILDING_LIBRARY',progress=progress,cost=100}end}
local q=c:GetBuildQueue();q.AddProgress=function(_,v)progress=progress+v end
runRequest(0,{Action='UNIT_ACTION_PREPARE',UnitID=901,Token='crew'});resetCounts()
runRequest(0,{Action='UNIT_ACTION_CONFIRM',UnitID=901,Token='confirm',PlanToken='crew'})
assert(progress==100 and kills==1 and counters.city_scan==4 and ledgerWrites==0)
crewResult=encode(props)..shared.Snapshot
runRequest(0,{Action='UNIT_ACTION_CONFIRM',UnitID=901,Token='duplicate',PlanToken='crew'});assert(progress==100 and kills==1)
""")
            results.append(l.eval('crewResult'))
        self.assertEqual(*results)

    def test_syntax_package_and_unchanged_contracts(self):
        l=fixture();compile_lua=l.eval('function(s,n)local f,e=load(s,n);assert(f,e)end')
        for name in CHANGED|{'Probe'}:compile_lua(source(name),name)
        root=ET.parse(M/'SpecializationP0.modinfo').getroot();self.assertEqual(root.get('version'),'201')
        files=[e.text for e in root.findall('./Files/File')]
        self.assertEqual(len(files),len(set(files)))
        self.assertEqual(set(files),{p.relative_to(M).as_posix() for p in M.rglob('*')if p.is_file()and p.name not in ['SpecializationP0.modinfo','.DS_Store']})
        self.assertIn('P0-B-174.201',source('Probe'))
        changes=set(subprocess.check_output(['git','diff',BASE,'--name-only','--','Mod'],cwd=R,text=True).splitlines())
        self.assertEqual(changes,{'Mod/'+x+'.lua' for x in CHANGED|{'Probe'}}|{'Mod/SpecializationP0.modinfo'})
        self.assertEqual(subprocess.check_output(['git','diff',BASE,'--','Specialization/Design'],cwd=R,text=True),'')
        old,new=source('Gameplay',True),source('Gameplay')
        def dirty(s):return s[s.index('  if params.Action=="LV2_GPP_DIRTY" then'):s.index('  if params.Action=="NETWORK_PUSH" then')]
        self.assertEqual(dirty(old),dirty(new))


if __name__=='__main__':
    unittest.main(verbosity=2)
