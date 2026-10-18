"""B234 actual Lua + loaded-HD SQLite fixtures. LOCAL_SIMULATION, not native PASS.
External database is read-only; new SQL is applied to an in-memory copy only.
"""
import ast
import json
from pathlib import Path
import sqlite3
import unittest
import zlib
import xml.etree.ElementTree as ET
from lupa.lua55 import LuaRuntime
from project_paths import external_database

R=Path(__file__).resolve().parents[1]
M=R/'Mod'
def lua(v):
    if v is None: return 'nil'
    if isinstance(v,bool): return 'true' if v else 'false'
    if isinstance(v,(int,float)): return str(v)
    if isinstance(v,str): return json.dumps(v,ensure_ascii=False)
    if isinstance(v,list): return '{'+','.join(lua(x) for x in v)+'}'
    return '{'+','.join('['+lua(k)+']='+lua(x) for k,x in v.items())+'}'

SETUP=r'''
turn=1;ExposedMembers={};hooks={};writes=0;reads=0;factReads={};ledgerReads={};removalFailure=nil
function emit(n,...)for _,f in ipairs(hooks[n] or {})do f(...)end end
Events=setmetatable({},{__index=function(t,k)local e={Add=function(f)hooks[k]=hooks[k] or {};table.insert(hooks[k],f)end};rawset(t,k,e);return e end});GameEvents=Events
Game={GetCurrentGameTurn=function()return turn end,GetLocalPlayer=function()return 0 end}
Locale={Lookup=function(s)return s end};P={Count=function()end,IsTestPlayer=function(p)return p==0 end,Field=function(t,k)return t and t[k]end}
local indexed={};GameInfo={}
for name,rows in pairs(DB)do
 local index={};indexed[name]=index
 for _,r in ipairs(rows)do
  if r.Index then index[r.Index]=r end
  for _,k in ipairs({'BuildingType','DistrictType'})do if r[k]then index[r[k]]=r end end
 end
 GameInfo[name]=function()local i=0;return function()i=i+1;return rows[i]end end
end
P.Info=function(t,k)return indexed[t] and indexed[t][k]end
P.Rows=function(t)return assert(DB[t],t)end
P.HasBuilding=function(b,id)reads=reads+1;return b[id]==true end
P.RemoveBuilding=function(b,id)if removalFailure==id then return end;b[id]=nil;writes=writes+1 end
P.CreateBuilding=function(b,id)assert(not b[id]);b[id]=true;writes=writes+1 end
cities={};facts={};ledgers={};unknown={};exits={};returns={};networkError=nil;networkValidity='VERIFIED';recipients={};requests=0
for id=1,4 do
 local c={id=id,owner=0,built={},token='T'..id};cities[id]=c
 c.GetID=function()return c.id end;c.GetOwner=function()return c.owner end
 c.GetX=function()return id end;c.GetY=function()return 1 end;c.GetName=function()return 'City'..id end
 c.GetProperty=function()return c.token end;c.GetBuildings=function()return c.built end;c.GetBuildQueue=function()return c.built end
 facts[id]={specialization='NONE',active=0,potential=0,token=c.token}
 ledgers[id]={foundation=c.token,learned={},districts={learned={}}}
end
Players={[0]={GetCities=function()return {Members=function()return pairs(cities)end,FindID=function(_,id)return cities[id]end}end},[64]={GetCities=function()return nil end}}
shared={EffectiveFacts={Read=function(pid,c)factReads[c.id]=(factReads[c.id] or 0)+1;if unknown[c.id]then error('STD_FACTS_UNKNOWN')end;return facts[c.id]end},
 Standardization={ReadKnowledge=function(pid,c)ledgerReads[c.id]=(ledgerReads[c.id] or 0)+1;if ledgers[c.id]==false then error('STD_HISTORY_CORRUPT')end;return ledgers[c.id]end},
 NetworkBridge={Input=function()return {validity=networkValidity}end,CurrentIndustryBatch=function()if networkError then error(networkError)end;return {input={validity=networkValidity,availability='AVAILABLE'},recipients=recipients}end,RequestPendingProof=function()requests=requests+1 end},
 CityProgressionStore={EngineeringState=function(pid,c)return {token=c.token}end,HistoryStartStatus=function()return 'READY'end,RegisterExit=function(k,f)exits[k]=f end,RegisterReturn=function(k,f)returns[k]=f end,
 RemoveOwned=function(c,loss,ids)for _,id in ipairs(ids)do local r=P.Info('Buildings',id);if P.HasBuilding(c.built,r.Index)then P.RemoveBuilding(c.built,r.Index);assert(not P.HasBuilding(c.built,r.Index))end end end}}
function industry(id,level)facts[id].specialization='INDUSTRY';facts[id].active=level;facts[id].potential=level end
function learn(id,building)
 local cat=SPCStandardizationCatalog.Build(P);local b=assert(cat.buildings[building]);ledgers[id].learned[building]={district=b.district,tier=b.tier}
end
function district(id,kind)ledgers[id].districts.learned[kind]={observedType=kind}end
function has(id,kind,target)return cities[id].built[assert(P.Info('Buildings','BUILDING_SPC_STD_BASE_'..(kind=='BUILDING' and 'B_' or 'D_')..target)).Index]==true end
function start()
 SPCStandardizationDiscount.Start(P,shared,{retired=true});SPCCopyYields.Start(P,shared,{retired=true})
 SPCStandardizationEffects.Start(P,shared);d=shared.StandardizationEffects
 emit('LoadScreenClose');assert(not d.error,d.error)
end
'''

class Standardization(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.db=sqlite3.connect(':memory:')
        src=sqlite3.connect(external_database(R).as_uri()+'?mode=ro',uri=True)
        try: src.backup(cls.db)
        finally: src.close()
        cls.db.create_function('Make_Hash',1,lambda text:zlib.crc32(text.encode())) # fixture hash only
        # After a native B234 run the configured DB can already contain these rows.
        # Rebuild only our projection definitions in this in-memory test copy.
        if cls.db.execute("SELECT 1 FROM sqlite_master WHERE name='SPC_StandardizationTargets'").fetchone():
            own=[(r[0],) for r in cls.db.execute('SELECT CarrierType FROM SPC_StandardizationTargets')]
            for table,column in [('ModifierArguments','ModifierId'),('BuildingModifiers','BuildingType'),
                                 ('Modifiers','ModifierId'),('Buildings','BuildingType'),('Types','Type')]:
                cls.db.executemany('DELETE FROM '+table+' WHERE '+column+'=?',own)
            cls.db.execute('DROP TABLE SPC_StandardizationTargets')
        cls.db.executescript((M/'Data/StandardizationEffects.sql').read_text())
        cls.db.row_factory=sqlite3.Row
        cls.tables={'SPC_StandardizationLevels':[]} # B234 fixture: no learned IV layers.
        for t in ['Buildings','Districts','DistrictReplaces','HD_BuildingTiers','HD_DUMMY_BUILDINGS','SPC_B054_Targets','SPC_StandardizationTargets']:
            cls.tables[t]=[dict(r) for r in cls.db.execute('SELECT rowid AS "Index",* FROM '+t)]

    @classmethod
    def tearDownClass(cls): cls.db.close()

    def setUp(self):
        self.l=LuaRuntime(unpack_returned_tuples=True)
        self.l.globals().include=lambda n:self.l.execute((M/(n+'.lua')).read_text())
        self.l.execute('DB='+lua(self.tables))
        self.l.execute(SETUP)
        self.l.execute('print=function()end')
        for n in ['StandardizationCatalog','StandardizationDiscount','CopyYields','StandardizationEffects','NetworkBoost']:
            self.l.execute((M/(n+'.lua')).read_text())
    def runlua(self,s):self.l.execute(s)

    def test_local_self_does_not_require_network(self):
        self.runlua("industry(1,3);learn(1,'BUILDING_GRANARY');district(1,'DISTRICT_CAMPUS');networkError='NETWORK_NOT_READY';start();assert(has(1,'BUILDING','BUILDING_GRANARY'));assert(has(1,'DISTRICT','DISTRICT_CAMPUS'));assert(not has(2,'BUILDING','BUILDING_GRANARY'));assert(d.errors['0:1']=='NETWORK_NOT_READY')")
    def test_iii_threshold_and_iv_only_baseline(self):
        self.runlua("industry(1,2);learn(1,'BUILDING_GRANARY');start();assert(not has(1,'BUILDING','BUILDING_GRANARY'));industry(1,3);d.SourceChanged(0,1);assert(has(1,'BUILDING','BUILDING_GRANARY'));local w=writes;industry(1,4);d.SourceChanged(0,1);assert(writes==w)")
    def test_network_union_holder_only_no_stacking(self):
        self.runlua("industry(1,3);industry(2,4);learn(1,'BUILDING_GRANARY');learn(2,'BUILDING_LIBRARY');recipients[3]={[1]=true,[2]=true};start();assert(has(3,'BUILDING','BUILDING_GRANARY') and has(3,'BUILDING','BUILDING_LIBRARY'));assert(d.records['0:3'].applied['BUILDING:BUILDING_GRANARY']==10);assert(not has(4,'BUILDING','BUILDING_GRANARY'))")
    def test_same_group_and_unique_district(self):
        self.runlua("industry(1,3);learn(1,'BUILDING_GRANARY');district(1,'DISTRICT_CAMPUS');start();assert(has(1,'BUILDING','BUILDING_MONUMENT'));assert(not has(1,'BUILDING','BUILDING_EXHIBITION'));assert(has(1,'DISTRICT','DISTRICT_SEOWON'))")
    def test_disabled_or_unclassified_history_never_grants_or_erases(self):
        self.runlua("industry(1,3);learn(1,'BUILDING_GRANARY');ledgers[1].learned.BUILDING_MISSING={district='DISTRICT_CAMPUS',tier=1};start();assert(has(1,'BUILDING','BUILDING_GRANARY'));assert(ledgers[1].learned.BUILDING_MISSING);assert(d.errors['0:1']=='STD_RETAINED_CLASSIFICATION_UNAVAILABLE')")
    def test_corrupt_history_not_empty_or_reinitialized(self):
        self.runlua("industry(1,3);ledgers[1]=false;start();assert(not has(1,'BUILDING','BUILDING_GRANARY'));assert(d.errors['0:1']=='STD_HISTORY_CORRUPT');assert(ledgers[1]==false)")
    def test_source_loss_withdraws_even_while_network_unknown(self):
        self.runlua("industry(1,3);learn(1,'BUILDING_GRANARY');recipients[2]={[1]=true};start();networkError='NETWORK_REFRESH_PENDING';industry(1,2);d.SourceChanged(0,1);assert(not has(1,'BUILDING','BUILDING_GRANARY') and not has(2,'BUILDING','BUILDING_GRANARY'))")
    def test_unknown_holds_then_recovery_removes(self):
        self.runlua("industry(1,3);learn(1,'BUILDING_GRANARY');recipients[2]={[1]=true};start();unknown[1]=true;d.SourceChanged(0,1);assert(has(2,'BUILDING','BUILDING_GRANARY'));unknown[1]=nil;industry(1,1);d.SourceChanged(0,1);assert(not has(2,'BUILDING','BUILDING_GRANARY'))")
    def test_disconnection_only_removes_remote_effect(self):
        self.runlua("industry(1,3);learn(1,'BUILDING_GRANARY');recipients[2]={[1]=true};start();recipients={};d.Audit({player=0});assert(has(1,'BUILDING','BUILDING_GRANARY') and not has(2,'BUILDING','BUILDING_GRANARY'))")
    def test_confirmed_network_invalid_keeps_self(self):
        self.runlua("industry(1,3);learn(1,'BUILDING_GRANARY');recipients[2]={[1]=true};start();networkValidity='CONFIRMED_INVALID';d.Audit({player=0});assert(has(1,'BUILDING','BUILDING_GRANARY') and not has(2,'BUILDING','BUILDING_GRANARY'))")
    def test_owner_or_reference_change_does_not_transfer_proof(self):
        self.runlua("industry(1,3);learn(1,'BUILDING_GRANARY');recipients[2]={[1]=true};start();cities[1].owner=3;networkError='NETWORK_PENDING';d.SourceChanged(0,1);assert(not has(2,'BUILDING','BUILDING_GRANARY'))")
    def test_duplicate_is_write_free_and_real_same_turn_change_updates(self):
        self.runlua("industry(1,3);learn(1,'BUILDING_GRANARY');recipients[2]={[1]=true};start();local w=writes;d.SourceChanged(0,1);d.Audit({player=0});assert(writes==w);learn(1,'BUILDING_LIBRARY');d.SourceChanged(0,1);assert(has(2,'BUILDING','BUILDING_LIBRARY'))")
    def test_batch_reads_each_holder_once(self):
        self.runlua("industry(1,3);learn(1,'BUILDING_GRANARY');for i=2,4 do recipients[i]={[1]=true}end;start();ledgerReads={};factReads={};d.Audit({player=0});assert(ledgerReads[1]==1 and factReads[1]==1)")
    def test_exact_legacy_cleanup_and_no_resurrection(self):
        self.runlua("industry(1,3);learn(1,'BUILDING_GRANARY');local b=cities[1].built;local old=P.Info('Buildings','BUILDING_SPC_B054_BUILDING_GRANARY_1').Index;local copy=P.Info('Buildings','BUILDING_SPC_B051_PRODUCTION_POS_0').Index;b[old]=true;b[copy]=true;b.EXTERNAL=true;start();assert(not b[old] and not b[copy] and b.EXTERNAL);local w=writes;shared.StandardizationDiscount.Receive(0,{});shared.StandardizationDiscount.Initialize(0,{});shared.CopyYields.Receive(0,{});shared.CopyYields.Audit();assert(writes==w);emit('LoadScreenClose');assert(not b[old] and not b[copy])")
    def test_unconfirmed_legacy_removal_blocks_replacement(self):
        self.runlua("industry(1,3);learn(1,'BUILDING_GRANARY');removalFailure=P.Info('Buildings','BUILDING_SPC_B054_BUILDING_GRANARY_1').Index;cities[1].built[removalFailure]=true;SPCStandardizationDiscount.Start(P,shared,{retired=true});SPCCopyYields.Start(P,shared,{retired=true});SPCStandardizationEffects.Start(P,shared);d=shared.StandardizationEffects;emit('LoadScreenClose');assert(d.error=='STD_OLD_DISCOUNT_REMOVE');assert(not has(1,'BUILDING','BUILDING_GRANARY'));removalFailure=nil;emit('PlayerTurnActivated',0);assert(has(1,'BUILDING','BUILDING_GRANARY'))")
    def test_reload_rebuilds_current_projection_no_permanent_writes(self):
        self.runlua("industry(1,3);learn(1,'BUILDING_GRANARY');start();industry(1,2);SPCStandardizationEffects.Start(P,shared);d=shared.StandardizationEffects;d.Audit();assert(not has(1,'BUILDING','BUILDING_GRANARY'));assert(ledgers[1].learned.BUILDING_GRANARY)")
    def test_loaded_unknown_projection_then_current_recovery(self):
        self.runlua("industry(1,3);learn(1,'BUILDING_GRANARY');start();unknown[1]=true;SPCStandardizationEffects.Start(P,shared);d=shared.StandardizationEffects;d.Audit();assert(has(1,'BUILDING','BUILDING_GRANARY'));unknown[1]=nil;industry(1,1);d.SourceChanged(0,1);assert(not has(1,'BUILDING','BUILDING_GRANARY'))")
    def test_exit_removes_owned_only(self):
        self.runlua("industry(1,3);learn(1,'BUILDING_GRANARY');start();cities[1].built.EXTERNAL=true;exits.StandardizationEffects(cities[1],{origin={owner=0,cityID=1}});assert(not has(1,'BUILDING','BUILDING_GRANARY'));assert(cities[1].built.EXTERNAL)")
    def test_report_is_read_only(self):
        self.runlua("industry(1,3);learn(1,'BUILDING_GRANARY');start();local w=writes;local r=d.Describe(0,cities[1],1);assert(r:find('+10%%') and r:find('0%%'));assert(writes==w)")
    def test_research_network_exact_exit_and_test_rejection(self):
        self.runlua("local old=assert(SPCBoostIntegerConfig.rows['RESEARCH:10']);local id=P.Info('Buildings',old).Index;cities[1].built[id]=true;cities[1].built.EXTERNAL=true;SPCNetworkBoost.Start(P,shared,{retired=true});local b=shared.NetworkBoost;b.EnsureReady(0);assert(b.ready and not cities[1].built[id] and cities[1].built.EXTERNAL);assert(next(b.Plan(0))==nil);assert(not pcall(b.Test,0,3.8));local w=writes;b.Audit();emit('PlayerTurnActivated',0);assert(writes==w)")
    def test_unknown_add_readback_does_not_repeat_native_creation(self):
        self.runlua("industry(1,3);learn(1,'BUILDING_GRANARY');start();learn(1,'BUILDING_LIBRARY');local raw=P.HasBuilding;local rawCreate=P.CreateBuilding;local target=P.Info('Buildings','BUILDING_SPC_STD_BASE_B_BUILDING_LIBRARY').Index;local uncertain=false;P.CreateBuilding=function(b,id)rawCreate(b,id);if id==target then uncertain=true end end;P.HasBuilding=function(b,id)if id==target and uncertain then return nil end;return raw(b,id)end;d.SourceChanged(0,1);assert(d.errors['0:1']);uncertain=false;P.CreateBuilding=rawCreate;d.SourceChanged(0,1);assert(has(1,'BUILDING','BUILDING_LIBRARY') and not d.errors['0:1'])")
    def test_failed_new_removal_retains_ownership_then_retries(self):
        self.runlua("industry(1,3);learn(1,'BUILDING_GRANARY');start();removalFailure=P.Info('Buildings','BUILDING_SPC_STD_BASE_B_BUILDING_GRANARY').Index;industry(1,1);d.SourceChanged(0,1);assert(d.errors['0:1']=='STD_REMOVE_UNCONFIRMED' and has(1,'BUILDING','BUILDING_GRANARY'));removalFailure=nil;d.SourceChanged(0,1);assert(not has(1,'BUILDING','BUILDING_GRANARY'))")
    def test_small_scope_skips_unrelated_receiver_facts(self):
        self.runlua("industry(1,3);learn(1,'BUILDING_GRANARY');recipients[2]={[1]=true};start();factReads={};learn(1,'BUILDING_LIBRARY');d.SourceChanged(0,1);assert(not factReads[3] and not factReads[4]);assert(has(2,'BUILDING','BUILDING_LIBRARY'))")
    def test_structural_dictionary_not_catalog_failure(self):
        self.runlua("industry(1,3);learn(1,'BUILDING_GRANARY');learn(1,'BUILDING_LIBRARY');ledgers[1].learned.BUILDING_LIBRARY.tier=999;start();assert(has(1,'BUILDING','BUILDING_GRANARY') and not has(1,'BUILDING','BUILDING_LIBRARY'));assert(ledgers[1].learned.BUILDING_LIBRARY.tier==999)")
    def test_reentrant_publication_defers_without_recursion_or_timer(self):
        self.runlua("industry(1,3);learn(1,'BUILDING_GRANARY');local create=P.CreateBuilding;local n=0;P.CreateBuilding=function(b,id)create(b,id);n=n+1;shared.StandardizationEffects.Audit({player=0})end;start();local w=writes;emit('GameCoreEventPublishComplete');assert(writes==w and not d.busy and n>0)")
    def test_foreign_saved_owned_projection_is_removed(self):
        self.runlua("local c=cities[4];cities[4]=nil;c.owner=3;local old=P.Info('Buildings','BUILDING_SPC_B054_BUILDING_GRANARY_2').Index;local new=P.Info('Buildings','BUILDING_SPC_STD_BASE_B_BUILDING_GRANARY').Index;c.built[old]=true;c.built[new]=true;c.built.EXTERNAL=true;Players[3]={GetCities=function()return {Members=function()return pairs({c})end}end};start();assert(not c.built[old] and not c.built[new] and c.built.EXTERNAL)")
    def test_research_failed_cleanup_no_property_writes_or_ready(self):
        self.runlua("local id=P.Info('Buildings',SPCBoostIntegerConfig.rows['RESEARCH:10']).Index;cities[1].built[id]=true;removalFailure=id;SPCNetworkBoost.Start(P,shared,{retired=true});local b=shared.NetworkBoost;b.EnsureReady(0);assert(not b.ready and b.errors[0]);removalFailure=nil;emit('PlayerTurnActivated',0);assert(b.ready and not cities[1].built[id])")
    def test_industry_sql_is_type_specific_and_never_grants_eligibility(self):
        for row in self.db.execute('select Kind,TargetType,CarrierType from SPC_StandardizationTargets'):
            args=dict(self.db.execute('select Name,Value from ModifierArguments where ModifierId=?',(row['CarrierType'],)))
            self.assertEqual(args,{'Amount':'10',('BuildingType' if row['Kind']=='BUILDING' else 'DistrictType'):row['TargetType']})

    def test_sql_scope_and_native_effect_arguments(self):
        rows=self.db.execute('select t.Kind,t.TargetType,m.ModifierType,a.Value from SPC_StandardizationTargets t join Modifiers m on m.ModifierId=t.CarrierType join ModifierArguments a on a.ModifierId=t.CarrierType and a.Name="Amount"').fetchall()
        self.assertGreater(len(rows),150)
        self.assertTrue(all(str(r['Value'])=='10' for r in rows))
        self.assertFalse(self.db.execute('select 1 from SPC_StandardizationTargets t join Buildings b on b.BuildingType=t.TargetType where b.IsWonder=1 or b.InternalOnly=1').fetchall())
        self.assertFalse(self.db.execute("select 1 from SPC_StandardizationTargets t join Modifiers m on m.ModifierId=t.CarrierType where m.ModifierType like '%PURCHASE%'").fetchall())
        self.assertFalse(self.db.execute("select 1 from SPC_StandardizationTargets where TargetType in ('DISTRICT_GOVERNMENT','DISTRICT_CITY_CENTER')").fetchall())
        effects=dict(self.db.execute("select ModifierType,EffectType from DynamicModifiers"))
        self.assertEqual(effects['MODIFIER_SINGLE_CITY_ADJUST_BUILDING_PRODUCTION'],effects['MODIFIER_PLAYER_CITIES_ADJUST_BUILDING_PRODUCTION'])
    def test_entry_wiring_retains_industry_base_and_other_professions(self):
        root=ET.parse(M/'SpecializationP0.modinfo').getroot()
        ids={r.attrib['id'] for r in root.find('InGameActions')}
        self.assertNotIn('SPC_B054_Eligibility',ids);self.assertNotIn('SPC_B051_Background',ids)
        self.assertIn('SPC_B036_IndustryRefresh',ids);self.assertIn('SPC_B234_Standardization',ids)
        s=(M/'Gameplay.lua').read_text()
        self.assertIn('SPCNetworkBoost.Start(P,shared,{retired=true})',s)
        self.assertIn('SPCResearchInfrastructure.Start(P,shared)',s)
        self.assertIn('SPCCultureNetwork.Start(P,shared)',s)
        self.assertIn('SPCCommerceConvergence.Start(P,shared)',s)
        self.assertGreater(s.index('shared.IndustrySupport.BindPermanentWrites()'),s.index('shared.OnPermanentCityWrite=nil'))

class InvestmentNotification(unittest.TestCase):
    def test_failed_standardization_notification_does_not_block_housing_gpp(self):
        from test_investment_update_propagation import fixture
        l=fixture()
        l.execute("shared.StandardizationEffects={errors={},SourceChanged=function()error('INJECTED_FAILURE')end};assert(invest(c,301,false):find('INVESTED'));assert(housing(c)==1 and gpp(c,'RESEARCH')==6);assert(shared.StandardizationEffects.errors['investment-notify:0'])")

class KnowledgeIntegration(unittest.TestCase):
    def test_real_store_knowledge_read_is_isolated_from_current_catalog(self):
        from test_industry_history import runtime
        l=runtime();l.execute("local c=H.newIndustry();local v=shared.Standardization.ReadKnowledge(0,c);assert(v.learned.BUILDING_A and v.districts.learned.DISTRICT_INDUSTRIAL_ZONE);shared.Standardization.catalog.buildings.BUILDING_A=nil;assert(not pcall(shared.Standardization.ReadLedger,0,c));local next=shared.Standardization.ReadKnowledge(0,c);assert(next.learned.BUILDING_A);next.learned.BUILDING_A=nil;assert(shared.Standardization.ReadKnowledge(0,c).learned.BUILDING_A)")
    def test_real_store_corrupt_history_remains_blocked(self):
        from test_industry_history import runtime
        l=runtime();l.execute("local c=H.newIndustry();local r=T.record(c);r.templates=nil;H.reload();assert(not pcall(shared.Standardization.ReadKnowledge,0,c));assert(T.record(c).templates==nil)")

class Support(unittest.TestCase):
    def setUp(self):
        tree=ast.parse((R/'DevelopmentTests/test_arch_v2_c2.py').read_text())
        fix=next(ast.literal_eval(n.value) for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='FIX' for t in n.targets))
        self.l=LuaRuntime(unpack_returned_tuples=True)
        self.l.globals().include=lambda n:self.l.execute((M/(n+'.lua')).read_text()) if n!='Probe' else None
        self.l.execute(fix)
        self.l.execute("P.Count=function()end;P.Families={DISTRICT_CAMPUS='RESEARCH',DISTRICT_INDUSTRIAL_ZONE='INDUSTRY'};P.Family=function(t)return P.Families[t]end;for _,v in pairs(districts)do v.IsPillaged=function()return false end end")
        self.l.execute((M/'IndustrySupport.lua').read_text())
        self.l.execute("SPCIndustrySupport.Start(P,shared);d=shared.IndustrySupport;d.BindPermanentWrites();sync=true")
    def test_sample_before_commit_same_turn(self):
        self.l.execute("facts[2].specialization='NONE';facts[2].active=0;facts[2].potential=0")
        self.l.execute((M/'UI/IndustryRefresh.lua').read_text());self.l.execute('initUI();pulse()')
        self.l.execute("assert(not cities[2].built['BUILDING_SPC_DEV_INDUSTRY_LV1_-1']);facts[2].specialization='INDUSTRY';facts[2].active=1;facts[2].potential=1;shared.OnPermanentCityWrite(cities[2],'CityProgressionStore.lua');fire('GameCoreEventPublishComplete');assert(cities[2].built['BUILDING_SPC_DEV_INDUSTRY_LV1_-1']);assert(turn==1 and sends==1)")
    def test_commit_before_sample_and_first_turn_readiness(self):
        self.l.execute("shared.OnPermanentCityWrite(cities[2],'ClaimProjects.lua');fire('GameCoreEventPublishComplete');assert(not cities[2].built['BUILDING_SPC_DEV_INDUSTRY_LV1_-1'])")
        self.l.execute((M/'UI/IndustryRefresh.lua').read_text());self.l.execute("initUI();pulse();assert(cities[2].built['BUILDING_SPC_DEV_INDUSTRY_LV1_-1']);assert(turn==1)")
    def test_unknown_recovery_without_new_sample_or_panel(self):
        self.l.execute('factUnknown=true');self.l.execute((M/'UI/IndustryRefresh.lua').read_text());self.l.execute('initUI();pulse()')
        self.l.execute("factUnknown=false;fire('GameCoreEventPublishComplete');assert(cities[2].built['BUILDING_SPC_DEV_INDUSTRY_LV1_-1']);assert(sends==1)")
    def test_duplicates_and_unrelated_city_no_write(self):
        self.l.execute((M/'UI/IndustryRefresh.lua').read_text());self.l.execute('initUI();pulse()')
        self.l.execute("local before=writes;for i=1,3 do shared.OnPermanentCityWrite(cities[2],'CityProgressionStore.lua');fire('GameCoreEventPublishComplete')end;assert(writes==before);assert(not cities[1].built['BUILDING_SPC_DEV_INDUSTRY_LV1_-1'])")
    def test_same_turn_base_change_and_loss(self):
        self.l.execute((M/'UI/IndustryRefresh.lua').read_text());self.l.execute('initUI();pulse()')
        self.l.execute("districts[12].base=9;fire('CityWorkerChanged');pulse();assert(d.ReadBase(0,cities[2])==9);facts[2].specialization='NONE';facts[2].active=0;d.Audit({player=0,city=2});assert(not cities[2].built['BUILDING_SPC_DEV_INDUSTRY_LV1_-1'])")

if __name__=='__main__': unittest.main(verbosity=2)
