"""B233 L3: actual Store/history/template sources, native-shaped event fixtures.
Local invariants only; no native engine, CPU, memory or game-save acceptance.
"""
from pathlib import Path
import unittest
import xml.etree.ElementTree as ET
from test_store_write_boundaries import fixture

R = Path(__file__).resolve().parents[1]
SETUP = r'''
H={}
local KEY=SPCIndustryHistory.KEY
local districts={};local buildings={};local eras={};local technologies={};local civics={}
for i,name in ipairs({'INDUSTRIAL_ZONE','CAMPUS','THEATER','COMMERCIAL_HUB','CITY_CENTER','HOLY_SITE','SEOWON'})do
 local id='DISTRICT_'..name;local row={Index=i,DistrictType=id,Name=id}
 districts[id]=row;districts[i]=row
end
for i=1,4 do
 local id='BUILDING_WONDER_'..i
 local row={Index=100+i,BuildingType=id,Name=id,IsWonder=1,MaxWorldInstances=1,InternalOnly=0}
 if i==3 then row.PrereqCivic='CIVIC_B'elseif i~=4 then row.PrereqTech='TECH_A'end
 buildings[id]=row;buildings[row.Index]=row
end
buildings.BUILDING_A={Index=10,BuildingType='BUILDING_A',Name='A',PrereqDistrict='DISTRICT_CITY_CENTER',IsWonder=0,InternalOnly=0}
buildings[10]=buildings.BUILDING_A
buildings.BUILDING_B={Index=11,BuildingType='BUILDING_B',Name='B',PrereqDistrict='DISTRICT_INDUSTRIAL_ZONE',IsWonder=0,InternalOnly=0}
buildings[11]=buildings.BUILDING_B
technologies.TECH_A={EraType='ERA_ANCIENT'};civics.CIVIC_B={EraType='ERA_CLASSICAL'}
eras.ERA_ANCIENT={Name='Ancient'};eras.ERA_CLASSICAL={Name='Classical'}
local replacements={{CivUniqueDistrictType='DISTRICT_SEOWON',ReplacesDistrictType='DISTRICT_CAMPUS'}}
local function iterator(rows)return function()local i=0;return function()i=i+1;return rows[i]end end end
local function setup()
 ExposedMembers={};Locale={Lookup=function(s)return s end}
 local previous=P.Info
 P.Info=function(t,k)
  local tab=({Buildings=buildings,Districts=districts,Technologies=technologies,Civics=civics,Eras=eras})[t]
  if tab then return tab[k]end;return previous(t,k)
 end
 P.Rows=function(t)
  if t=='DistrictReplaces'then return replacements end
  assert(t=='Buildings');local rows={};for k,v in pairs(buildings)do if type(k)=='number'then rows[#rows+1]=v end end;return rows
 end
 P.HasBuilding=function(o,k)return o:HasBuilding(k)end
 local dr={};for k,r in pairs(districts)do if type(k)=='number'then dr[#dr+1]=r end end
 GameInfo.Districts=iterator(dr);GameInfo.DistrictReplaces=iterator(replacements)
 GameInfo.HD_BuildingTiers=iterator({{BuildingType='BUILDING_A',PrereqDistrict='DISTRICT_CITY_CENTER',Tier=0},
  {BuildingType='BUILDING_B',PrereqDistrict='DISTRICT_INDUSTRIAL_ZONE',Tier=1}})
 GameInfo.HD_DUMMY_BUILDINGS=iterator({})
 local setter=Game.SetProperty
 Game.SetProperty=function(o,k,v)
  if k==KEY then H.historyWrites=H.historyWrites+1;if H.failure=='drop'then return end
   if H.failure=='corrupt'then T.propsSet(k,{bad=true});return end
   if H.failure=='throw'then error('write failed')end
   T.propsSet(k,v)
  else return setter(o,k,v)end
 end
 SPCIndustryHistory.Start(P,shared);SPCStandardization.Start(P,shared)
end
function H.start()
 T.start();H.units={};H.native={};H.historyWrites=0;H.failure=nil
 local old=CityManager.GetDistrictAt
 CityManager.GetDistrictAt=function(x,y)return H.native[x..':'..y] or old(x,y)end
 local oldDistricts=Players[0].GetDistricts
 Players[0].GetDistricts=function()
  local result={};for _,r in oldDistricts():Members()do result[#result+1]=r end
  for _,r in pairs(H.native)do result[#result+1]=r end
  return {Members=function()return ipairs(result)end}
 end
 setup()
end
function H.city(i,foreign)
 local c=T.fresh(i);c.buildings={};c.GetBuildings=function()return {HasBuilding=function(_,bid)return c.buildings[bid]==true end}end
 c.GetName=function()return 'Fixture' end
 c.GetDistricts=function()
  local rows={};for _,r in Players[0]:GetDistricts():Members()do if r:GetCity()==c then rows[#rows+1]=r end end
  return {GetNumDistricts=function()return #rows end,GetDistrictByIndex=function(_,n)return rows[n+1]end}
 end
 if foreign then c.s.ref.owner=3;Players[3]={IsMajor=function()return true end,IsHuman=function()return false end}
 else T.register(c)end
 return c
end
function H.district(c,kind,complete)
 local index=districts[kind].Index;local x=c:GetX()+index*200;local y=c:GetY()
 local d={GetCity=function()return c end,GetOwner=function()return c:GetOwner()end,GetID=function()return index*100+c:GetID()end,
 GetType=function()return index end,IsComplete=function()return complete end}
 H.native[x..':'..y]=d;GameEvents.OnDistrictConstructed.Fire(c:GetOwner(),index,x,y);return d,x,y
end
function H.wonder(c,i)
 c.buildings[100+i]=true
 Events.WonderCompleted.Fire(c:GetX()+i,c:GetY()+i,100+i,c:GetOwner(),c:GetID(),0,false)
end
function H.read(c)return shared.IndustryHistory.Read(c:GetOwner(),c)end
function H.ledger(c)return shared.Standardization.ReadLedger(0,c)end
function H.reload()T.reload();setup()end
function H.props()return T.props()[KEY]end
function H.newIndustry()
 local c=H.city(1);c.buildings[10]=true
 H.district(c,'DISTRICT_INDUSTRIAL_ZONE',true);assert(H.ledger(c).learned.BUILDING_A)
 return c
end
'''

def runtime():
    l = fixture()
    for n in ('StandardizationCatalog', 'Standardization', 'IndustryHistory'):
        l.execute((R / 'Mod' / (n + '.lua')).read_text())
    l.execute(SETUP)
    l.execute('H.start()')
    return l


class IndustryHistory(unittest.TestCase):
    def check(self, body):
        runtime().execute(body)

    def test_before_identity_actual_event_era_and_repeat(self):
        self.check('''
local c=H.city(1);T.governor(nil)
assert(shared.EffectiveFacts.Read(0,c).potential==0)
assert(H.read(c).N==0 and H.read(c).cityState=='KNOWN')
H.wonder(c,1);H.wonder(c,2);H.wonder(c,3)
local r=H.read(c);assert(r.N==3 and r.E==2 and r.eras.ERA_ANCIENT and r.eras.ERA_CLASSICAL)
local writes=H.historyWrites;local before=T.encode(T.props());T.turn(1)
H.wonder(c,1);H.wonder(c,3);assert(H.historyWrites==writes and T.encode(T.props())==before)
assert(T.record(c).base.specialization=='NONE')
''')

    def test_foreign_events_are_ignored_then_legal_identity_scans_n_only(self):
        self.check('''
local c=H.city(1,true);local before=T.encode(H.props());local writes=H.historyWrites
H.wonder(c,1);assert(T.encode(H.props())==before and H.historyWrites==writes)
-- No city lookup or foreign history enrollment is needed for ignored events.
local get=CityManager.GetCity;CityManager.GetCity=function()error('foreign lookup forbidden')end
H.wonder(c,3);CityManager.GetCity=get;assert(shared.IndustryHistory.ready)
c.buildings[103]=nil -- unseen foreign removal is not reconstructed
T.take(c);assert(T.record(c));assert(H.read(c).E==0 and H.read(c).N==0)
H.district(c,'DISTRICT_INDUSTRIAL_ZONE',true)
local r=H.read(c);assert(r.N==1 and r.E==0 and r.cityState=='RECONCILED')
local snapshot=T.encode(H.props());shared.IndustryHistory.Reconcile(0,c)
assert(T.encode(H.props())==snapshot)
H.reload();assert(H.read(c).N==1 and H.read(c).E==0)
''')

    def test_actual_store_claim_reconciles_captured_wonder_without_e(self):
        self.check("""
local c=H.city(1,true);local district=H.district(c,'DISTRICT_INDUSTRIAL_ZONE',true);H.wonder(c,1)
T.take(c);local store=shared.CityProgressionStore;local state=store.ClaimState(0,c)
assert(state.eligible and state.set.INDUSTRY and H.read(c).N==0)
store.ClaimComplete(0,c,{reference=state.reference,token=state.token,kind='INDUSTRY',
 project='PROJECT_SPC_CLAIM_INDUSTRY',turn=Game.GetCurrentGameTurn(),districtID=district:GetID(),type='DISTRICT_INDUSTRIAL_ZONE'})
local info=P.Info;P.Info=function(t,k)if t=='Projects' and k==900 then return {ProjectType='PROJECT_SPC_CLAIM_INDUSTRY'}end;return info(t,k)end
Events.CityProjectCompleted.Fire(0,c:GetID(),900);Events.GameCoreEventPublishComplete.Fire()
assert(H.read(c).N==1 and H.read(c).E==0)
assert(H.ledger(c).districts.learned.DISTRICT_INDUSTRIAL_ZONE)
H.reload();assert(H.read(c).N==1 and H.read(c).E==0)
""")

    def test_foreign_turn_never_changes_supported_players_history(self):
        self.check('''
local c=H.city(1);local other=H.city(2);H.wonder(c,1)
local before=T.encode(H.props());T.loss(c,3,55);H.wonder(c,3)
assert(T.encode(H.props())==before)
assert(H.read(other).E==1 and H.read(other).N==0)
assert(not pcall(H.read,c),'foreign city read must stay outside supported scope')
''')

    def test_coldload_known_empty_nonempty_and_unknown_old_history(self):
        self.check('''
local c=H.city(1);H.reload();assert(H.read(c).N==0 and H.read(c).cityState=='KNOWN')
H.wonder(c,1);local snapshot=T.encode(H.props());local writes=H.historyWrites
H.reload();assert(T.encode(H.props())==snapshot and H.historyWrites==writes and H.read(c).N==1)
T.propsSet(SPCIndustryHistory.KEY,nil);H.reload()
assert(H.read(c).coverage=='UNAVAILABLE' and H.read(c).eraState=='UNKNOWN')
''')

    def test_corrupt_or_missing_era_not_guessed(self):
        self.check('''
local c=H.city(1);H.wonder(c,4)
assert(H.read(c).N==1 and H.read(c).eraState=='UNKNOWN' and H.read(c).E==0)
H.props().revision=44;local before=T.encode(H.props());H.reload()
assert(not shared.IndustryHistory.ready and T.encode(H.props())==before)
assert(not pcall(H.read,c))
''')

    def test_failure_readback_does_not_publish_or_replay(self):
        for mode in ('drop','corrupt','throw'):
            with self.subTest(mode=mode):
                self.check("""
local c=H.city(1);local other=H.city(2);local before=T.encode(T.record(other))
local published=shared.IndustryHistory.published;H.failure='%s';H.wonder(c,1)
assert(not shared.IndustryHistory.ready and shared.IndustryHistory.published==published)
assert(not pcall(H.read,c));H.failure=nil
Events.GameCoreEventPublishComplete.Fire();H.wonder(c,1)
assert(not shared.IndustryHistory.ready and T.encode(T.record(other))==before)
assert(shared.EffectiveFacts.Read(0,other).potential==0)
""" % mode)

    def test_actual_return_new_city_id_and_reload_preserve_n_not_capture_e(self):
        self.check("""
local c=H.newIndustry();H.wonder(c,1)
shared.CityProgressionStore.RegisterExit('history_fixture',function()return true end)
T.loss(c,3,450);H.wonder(c,3);c.buildings[101]=nil;H.reload()
shared.CityProgressionStore.RegisterExit('history_fixture',function()return true end)
shared.CityProgressionStore.ExitConfirmed()
c.s.ref.owner=0;c.s.ref.cityID=501;Events.CityTransfered.Fire(0,501,3)
Events.GameCoreEventPublishComplete.Fire()
assert(T.record(c).stage=='ACTIVE');local r=H.read(c)
assert(r.N==2 and r.E==1 and r.eras.ERA_ANCIENT and not r.eras.ERA_CLASSICAL)
H.reload();assert(H.read(c).N==2 and H.read(c).cityState=='RECONCILED')
""")

    def test_existing_hook_still_bootstraps_if_load_callback_already_passed(self):
        self.check("""
local c=H.newIndustry();H.wonder(c,1)
-- Modules start after the Store's load callback; no P0 read is an initialization hook.
T.reload();SPCIndustryHistory.Start(P,shared);SPCStandardization.Start(P,shared)
assert(shared.IndustryHistory.ready and shared.Standardization.ready)
assert(H.read(c).N==1 and H.ledger(c).districts.learned.DISTRICT_INDUSTRIAL_ZONE)
""")

    def test_reentrant_distinct_completions_are_not_dropped(self):
        self.check("""
local c=H.city(1);local setter=Game.SetProperty;local fired=false
Game.SetProperty=function(o,k,v)
 setter(o,k,v)
 if k==SPCIndustryHistory.KEY and not fired then fired=true;H.wonder(c,3)end
end
H.wonder(c,1);assert(H.read(c).N==2 and H.read(c).E==2 and H.props().revision==3)
""")

    def test_one_failed_write_preserves_unknown_coverage_across_load(self):
        self.check("""
local c=H.city(1);local setter=Game.SetProperty;local first=true
Game.SetProperty=function(o,k,v)
 if k==SPCIndustryHistory.KEY and first then first=false;return end
 return setter(o,k,v)
end
H.wonder(c,1);assert(not shared.IndustryHistory.ready and H.props().coverage=='UNAVAILABLE')
H.reload();assert(H.read(c).cityState=='UNKNOWN' and H.read(c).eraState=='UNKNOWN')
""")

    def test_reconciliation_retains_removed_wonders_and_does_not_credit_e(self):
        self.check("""
local c=H.newIndustry();local other=H.city(2);c.buildings[103]=true
shared.IndustryHistory.Reconcile(0,c);assert(H.read(c).N==1 and H.read(c).E==0)
c.buildings[103]=nil;local before=T.encode(H.props())
shared.IndustryHistory.Reconcile(0,c);assert(T.encode(H.props())==before)
H.reload();assert(H.read(c).N==1 and H.read(other).N==0 and H.read(c).E==0)
""")

    def test_unreadable_current_buildings_do_not_replace_saved_n(self):
        self.check("""
local c=H.newIndustry();H.wonder(c,1);local before=T.encode(H.props())
c.GetBuildings=function()return {HasBuilding=function()return nil end}end
assert(not pcall(shared.IndustryHistory.Reconcile,0,c));assert(T.encode(H.props())==before)
assert(H.read(c).N==1 and shared.IndustryHistory.NeedsReconcile(c))
c.GetBuildings=function()return {HasBuilding=function(_,i)return c.buildings[i]==true end}end
c.buildings[103]=true;shared.Standardization.Discover(0)
assert(H.read(c).N==2 and H.read(c).E==1 and not shared.IndustryHistory.NeedsReconcile(c))
local before=T.encode(H.props());H.reload();assert(T.encode(H.props())==before and H.read(c).N==2)
""")

    def test_corrupt_reconciliation_is_not_rebuilt_from_current_buildings(self):
        self.check("""
local c=H.newIndustry();H.wonder(c,1);H.props().reconciled=nil
local before=T.encode(H.props());H.reload()
assert(not shared.IndustryHistory.ready and T.encode(H.props())==before)
assert(not pcall(shared.IndustryHistory.Reconcile,0,c))
""")

    def test_wonder_history_failure_does_not_block_normal_template_knowledge(self):
        self.check("""
H.props().reconciled=nil;H.reload();assert(not shared.IndustryHistory.ready)
local c=H.newIndustry();assert(H.ledger(c).learned.BUILDING_A)
assert(H.ledger(c).districts.learned.DISTRICT_INDUSTRIAL_ZONE)
assert(shared.Standardization.warnings['0:'..c:GetID()]=='IH_HISTORY_UNAVAILABLE')
""")

    def test_ui_is_read_only_and_idle_no_write(self):
        self.check('''
local c=H.city(1);H.wonder(c,1);local before=T.encode(T.props());local writes=H.historyWrites
for i=1,100 do Events.GameCoreEventPublishComplete.Fire();shared.IndustryHistory.Describe(0,c)end
assert(T.encode(T.props())==before and H.historyWrites==writes)
assert(#ExposedMembers.SPC_B205TrainingTrace.entries<=64)
''')

    def test_typed_district_normalization_incomplete_and_building_isolation(self):
        self.check('''
local c=H.newIndustry();local t=H.ledger(c)
assert(t.knowledgeVersion==1 and t.districts.learned.DISTRICT_INDUSTRIAL_ZONE and t.learned.BUILDING_A)
assert(not t.learned.DISTRICT_INDUSTRIAL_ZONE and t.revision==2 and t.districts.revision==2)
H.district(c,'DISTRICT_THEATER',false);assert(not H.ledger(c).districts.learned.DISTRICT_THEATER)
H.district(c,'DISTRICT_SEOWON',true);t=H.ledger(c)
assert(t.districts.learned.DISTRICT_CAMPUS.observedType=='DISTRICT_SEOWON' and not t.districts.learned.DISTRICT_SEOWON)
local before=T.encode(T.props());H.district(c,'DISTRICT_SEOWON',true);assert(T.encode(T.props())==before)
H.district(c,'DISTRICT_CITY_CENTER',true);assert(not H.ledger(c).districts.learned.DISTRICT_CITY_CENTER)
''')

    def test_initial_current_union_retention_and_coldload(self):
        self.check('''
local c=H.newIndustry();H.district(c,'DISTRICT_CAMPUS',true);local before=T.encode(H.ledger(c))
c.buildings[10]=nil;H.native={};H.reload()
assert(T.encode(H.ledger(c))==before and H.ledger(c).learned.BUILDING_A)
local writes=T.writes();Events.PlayerTurnActivated.Fire(0);assert(T.writes()==writes)
''')

    def test_catalog_drift_preserves_history_and_holds_only_effect_use(self):
        self.check('''
local c=H.newIndustry();local t=H.ledger(c)
shared.Standardization.catalog.buildings.BUILDING_A=nil
assert(shared.Standardization.ValidateHistory(c,t)==t)
assert(not pcall(shared.Standardization.ValidateRetained,c,t))
H.district(c,'DISTRICT_CAMPUS',true)
assert(T.record(c).templates.learned.BUILDING_A and T.record(c).templates.districts.learned.DISTRICT_CAMPUS)
assert(shared.EffectiveFacts.Read(0,c).specialization=='INDUSTRY')
''')

    def test_missing_typed_history_is_not_reinitialized(self):
        self.check('''
local c=H.newIndustry();local other=H.city(2);local before=T.encode(T.record(other))
T.record(c).templates.districts=nil;T.record(c).templates.knowledgeVersion=nil
local bad=T.encode(T.record(c));H.reload()
assert(not pcall(H.ledger,c) and T.encode(T.record(c))==bad and T.encode(T.record(other))==before)
assert(shared.EffectiveFacts.Read(0,other).potential==0)
''')

    def test_template_write_failure_atomic_no_known_marker(self):
        self.check('''
local c=H.city(1);shared.Standardization.ready=false
H.district(c,'DISTRICT_INDUSTRIAL_ZONE',true)
assert(T.record(c).templateLifecycle.state=='UNINITIALIZED')
T.failKey(T.key(c));shared.Standardization.ready=true;shared.Standardization.Discover(0)
assert(T.record(c).templates==nil and not T.record(c).templateLifecycle.districtsKnown)
assert(not pcall(H.ledger,c))
''')

    def test_unreadable_collection_is_not_known_empty(self):
        self.check('''
local c=H.city(1);c.GetDistricts=function()return {GetNumDistricts=function()return nil end}end
H.district(c,'DISTRICT_INDUSTRIAL_ZONE',true)
assert(T.record(c).templates==nil and shared.Standardization.errors['0:'..c:GetID()]=='STD_DISTRICT_COUNT_UNAVAILABLE')
''')

    def test_inherited_b140_building_claim_return_and_discount(self):
        # Native-shaped District fixture adaptation only. Historical assertions and
        # source file remain unchanged; B233 now also reads the city's District list.
        p=R/'DevelopmentTests/test_b140_templates.py'
        source=p.read_text()
        source=source.replace("return {buildings=catalogRows}", "return {buildings=catalogRows,districts={DISTRICT_INDUSTRIAL_ZONE={base='DISTRICT_INDUSTRIAL_ZONE'},DISTRICT_CAMPUS={base='DISTRICT_CAMPUS'},DISTRICT_THEATER={base='DISTRICT_THEATER'}}}")
        source=source.replace("local originalBoot=boot", """local originalFresh=fresh
function fresh(...)
 local c=originalFresh(...)
 c.GetDistricts=function()
  local rows={};for _,r in pairs(ds)do if r:GetCity()==c then rows[#rows+1]=r end end
  return {GetNumDistricts=function()return #rows end,GetDistrictByIndex=function(_,i)return rows[i+1]end}
 end
 return c
end
local originalBoot=boot""")
        exec(compile(source,str(p),'exec'),{'__file__':str(p)})

    def test_catalog_drift_actual_return_keeps_identity_and_history(self):
        # Reuse the original B140 loss/return proof, changing only its input catalog
        # after a reliable template was committed. No handcrafted return authority.
        p=R/'DevelopmentTests/test_b140_templates.py';source=p.read_text()
        namespace={'__file__':str(p)}
        exec(compile(source[:source.rindex('exec(compile')],str(p),'exec'),namespace)
        setup=namespace['extra'].split('-- A: first Claim',1)[0]
        setup=setup.replace("return {buildings=catalogRows}","return {buildings=catalogRows,districts={}}")
        setup=setup.replace('local originalBoot=boot',"""local originalFresh=fresh
function fresh(...)
 local c=originalFresh(...);c.GetDistricts=function()return {GetNumDistricts=function()return 0 end}end;return c
end
local originalBoot=boot""")
        body="""
local c,token=industry();local original=catalogRows.BUILDING_A
catalogRows.BUILDING_A=nil
loss(c,token,true);retake(c);flush()
assert(shared.EffectiveFacts.Read(0,c).specialization=='INDUSTRY')
assert(props[PREFIX..token].stage=='ACTIVE' and props[PREFIX..token].templates.learned.BUILDING_A)
assert(not pcall(ledger,c),'changed catalog should hold old effect eligibility')
catalogRows.BUILDING_A=original;assert(ledger(c).learned.BUILDING_A)
"""
        text=namespace['header']+namespace['helpers']+namespace['claim_setup']+namespace['return_setup']+setup+body+"\n"+chr(39)*3+")"
        exec(compile(text,str(p),'exec'),{'__file__':str(p)})

    def test_package_report_registration_and_visible_slot(self):
        tree=ET.parse(R/'Mod/SpecializationP0.modinfo')
        self.assertEqual(len([x for x in tree.findall('.//File') if x.text=='IndustryHistory.lua']),2)
        panel=ET.parse(R/'Mod/UI/P0Panel.xml')
        button=panel.find(".//*[@ID='TemplatesButton']")
        self.assertEqual(button.get('Hidden'),'0')
        self.assertEqual(button.get('Offset'),'280,18')
        self.assertIn('INDUSTRY_HISTORY_READ',(R/'Mod/Gameplay.lua').read_text())
        self.assertIn('INDUSTRY_HISTORY_READ',(R/'Mod/UI/P0Panel.lua').read_text())

if __name__=='__main__':
    unittest.main(verbosity=2)
