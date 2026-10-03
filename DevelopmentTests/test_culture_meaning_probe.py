"""L2B scoped simulation / SQL evidence. Never a native precision PASS.
Requires configured read-only DebugGameplay and lupa.lua55; reuses maintained
L1 and K engine fixtures. Pinned older version/notification assertions remain
historical and are replaced here only for the explicitly changed contract.
"""
from pathlib import Path
import unittest,xml.etree.ElementTree as ET
import sqlite3,zlib
from project_paths import external_database
import test_culture_aesthetic as ae
from test_p0_k import Fixture

R=Path(__file__).resolve().parents[1];M=R/'Mod'

def require_meaning_imports(root):
 imports=[e.text for e in root.findall("./InGameActions/ImportFiles[@id='SPCP0_Common']/File")]
 files=[e.text for e in root.find('Files')]
 for name in ['CultureMeaningModel.lua','CultureMeaningProbe.lua']:
  assert imports.count(name)==1 and files.count(name)==1, 'Meaning Lua must be imported exactly once: '+name
 return set(imports)


def bind_actual_request(l):
 # Execute the unchanged full request function from source, including its ingress
 # and player eligibility gate; do not mirror the new branch in a mock handler.
 src=(M/'Gameplay.lua').read_text()
 start=src.index('local function request(playerID,params)')
 end=src.index('GameEvents.SPC_P0_Request.Add',start)
 l.execute('P.Scalar=function(v)return tostring(v)end\n'+src[start:end]+'\nmeaningRequest=request')


def database():
 # The external DB may already contain B149 definitions. Reset only the exact
 # test-owned L1 definitions in the disposable memory copy, then apply source.
 # No external DB mutation and no assertion weakened by fixture version drift.
 ro=sqlite3.connect('file:'+str(external_database(R))+'?mode=ro',uri=True)
 d=sqlite3.connect(':memory:');ro.backup(d);ro.close()
 d.create_function('Make_Hash',1,lambda text:zlib.crc32(text.encode()))
 carrier='BUILDING_SPC_CULTURE_AESTHETIC'
 for table,col,values in [
  ('BuildingModifiers','BuildingType',[carrier]),('Buildings','BuildingType',[carrier]),('Types','Type',[carrier]),
  ('ModifierArguments','ModifierId',[f'SPC_CULTURE_AESTHETIC_{i}'for i in range(16)]),
  ('Modifiers','ModifierId',[f'SPC_CULTURE_AESTHETIC_{i}'for i in range(16)]),
  ('RequirementArguments','RequirementId',[f'SPC_CULTURE_AESTHETIC_{i}_REQ'for i in range(16)]),
  ('Requirements','RequirementId',[f'SPC_CULTURE_AESTHETIC_{i}_REQ'for i in range(16)]),
  ('RequirementSetRequirements','RequirementSetId',[f'SPC_CULTURE_AESTHETIC_{i}_SET'for i in range(16)]),
  ('RequirementSets','RequirementSetId',[f'SPC_CULTURE_AESTHETIC_{i}_SET'for i in range(16)])]:
  d.executemany(f'DELETE FROM {table} WHERE {col}=?',[(x,)for x in values])
 d.execute('DROP TABLE IF EXISTS SPC_CultureAestheticBits')
 d.executescript((M/'Data/CultureAesthetic.sql').read_text())
 # Earlier probe definitions may be present in the read-only DB too. Rebuild
 # only the exact 26 owned carriers / 182 attachments in this memory copy.
 carriers=['BUILDING_SPC_MEANING_PROBE_'+y+'_'+str(bit)for y,bits in [('SCIENCE',4),('GOLD',6),('CULTURE',4),('PRODUCTION',4),('FOOD',3),('FAITH',3)]for bit in range(bits)]
 carriers += ['BUILDING_SPC_MEANING_PROBE_CULTURE_SINGLE3','BUILDING_SPC_MEANING_PROBE_CULTURE_SINGLE3_SCALE100']
 modifiers=[b.removeprefix('BUILDING_')+'_'+cat for b in carriers for cat in ['WRITING','MUSIC','SCULPTURE','PORTRAIT','LANDSCAPE','RELIGIOUS','ARTIFACT']]
 for table,col,values in [('BuildingModifiers','BuildingType',carriers),('Buildings','BuildingType',carriers),('Types','Type',carriers),('ModifierArguments','ModifierId',modifiers),('Modifiers','ModifierId',modifiers)]:
  d.executemany(f'DELETE FROM {table} WHERE {col}=?',[(x,)for x in values])
 d.executescript((M/'Data/CultureMeaningProbe.sql').read_text())
 return d


class MeaningProbeTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.sql=database()
 def runtime(self,real_samples=False):
  helper=ae.AestheticTests();helper.sql=self.sql;l=helper.runtime()
  for table,key in [('GreatWorks','GreatWorkType'),('Yields','YieldType'),('GreatPersonIndividuals','GreatPersonIndividualType'),('Eras','EraType'),('GreatWork_YieldChanges','GreatWorkType')]:
   cur=self.sql.execute('SELECT * FROM '+table);columns=[a[0]for a in cur.description];rows=[dict(zip(columns,r))for r in cur]
   for i,r in enumerate(rows):r['Index']=i+1
   l.globals().GameInfo[table]=l.globals().db(ae.lua_table(l,rows),key)
  imports=require_meaning_imports(ET.parse(M/'SpecializationP0.modinfo').getroot())
  def imported_include(n):
   # Model action visibility only. This cannot prove native VFS/include behavior.
   assert n+'.lua' in imports, 'Not visible in ImportFiles: '+n
   l.execute((M/(n+'.lua')).read_text())
  l.globals().include=imported_include
  for n in ['Dialogue','GreatWorkAdjacency','CultureMeaningProbe']:imported_include(n)
  if real_samples:imported_include('GreatWorkFacts')
  l.globals().realSamples=real_samples
  l.execute("""
   Game.GetLocalPlayer=function()return 0 end
   for _,c in ipairs(cities)do building(c,'BUILDING_MARKET',c.ds[3],false);building(c,'BUILDING_FAIR',c.ds[3]);c.active=4;c.workCount=1;c.badCount=0;c.categoryUnknown=0;local campus=district(c,6,'DISTRICT_CAMPUS');building(c,'BUILDING_LIBRARY',campus)end
   if realSamples then
    local previous=shared.GreatWorkFacts.OnConfirmed
    for _,c in ipairs(cities)do function c:GetName()return 'Fixture '..self.id end end
    SPCGreatWorkFacts.Start(P,shared);shared.GreatWorkFacts.OnConfirmed=previous
   else
   shared.GreatWorkFacts.ack=1;shared.GreatWorkFacts.epoch=1;shared.GreatWorkFacts.inputRevision=0
   shared.GreatWorkFacts.Summary=function(pid,id)
    local c=Players[pid]:GetCities():FindID(id)
    return c and {count=c.workCount,eraCount=c.eras,availability=c.worksUnknown and 'UNKNOWN' or 'KNOWN',hasConfirmed=not c.neverConfirmed,reference=SPCNetworkInput.Reference(c),modifierExcludedCount=c.badCount,unknownCategoryCount=c.categoryUnknown}
   end
   end
   for _,c in ipairs(cities)do local dq=district(c,7,'DISTRICT_DIPLOMATIC_QUARTER');building(c,'BUILDING_CONSULATE',dq);building(c,'BUILDING_CHANCERY',dq)end
   SPCDialogue.Start(P,shared);dialogue=shared.Dialogue;dialogue.Init()
   -- These direct mock samples support the original consumer cases only. The
   -- realSamples path starts empty and accepts samples solely through request.
   function collection()
    assert(not realSamples,'REAL_SAMPLE_MUST_USE_REQUEST')
    dialogue.seq[0]=shared.GreatWorkFacts.ack
    dialogue.samples[0]={turn=turn,seq=shared.GreatWorkFacts.ack,generation=dialogue.generation,
     factsEpoch=shared.GreatWorkFacts.epoch,factsInput=shared.GreatWorkFacts.inputRevision,
     cities={[1]={{id=1,type='GREATWORK_BHASA_1'}},[2]={{id=2,type='GREATWORK_BHASA_1'}}}}
    assert(dialogue.ConfirmSamplePair(0,{Seq=shared.GreatWorkFacts.ack,Turn=turn,Generation=dialogue.generation,
     FactsEpoch=shared.GreatWorkFacts.epoch,FactsInput=shared.GreatWorkFacts.inputRevision}))
   end
   if not realSamples then collection();dialogue.Audit(0)end
   SPCGWAdjacency.Start(P,shared);gwa=shared.GreatWorkAdjacency;gwa.Init()
   gwa.samples[0]={turn=turn,rows={{city=1,values={0,0,2,2,0,0}},{city=2,values={0,0,2,2,0,0}}}}
   gwa.Audit(0)
   SPCCultureMeaningProbe.Start(P,shared);probe=shared.CultureMeaningProbe
   fire('LoadScreenClose');if not realSamples then collection()end;svc.MarkDirty();gwa.Audit(0)
   function confirmCollection()
    assert(not realSamples,'REAL_SAMPLE_MUST_USE_REQUEST')
    shared.GreatWorkFacts.OnConfirmed(0,{1}) -- Preserve the existing L1 callback.
    probe.CollectionConfirmed(0,{Seq=shared.GreatWorkFacts.ack,Turn=turn,Generation=dialogue.generation,
     FactsEpoch=shared.GreatWorkFacts.epoch,FactsInput=shared.GreatWorkFacts.inputRevision})
   end
   function configured(c,y)
    local n=0;for bit=0,SPCCultureMeaningModel.ProbeBits[y]-1 do
     if c.present[GameInfo.Buildings['BUILDING_SPC_MEANING_PROBE_'..y..'_'..bit].Index]then n=n+2^bit/SPCCultureMeaningModel.ProbeScale[y] end
    end
    if y=='CULTURE' then for _,part in pairs(SPCCultureMeaningModel.VariantParts)do
     if c.present[GameInfo.Buildings[part.name].Index]then n=n+part.amount end
    end end;return n
   end
   function old(c,y)return c.present[GameInfo.Buildings['BUILDING_SPC_B060_'..y..'_P1'].Index]==true end
   function begin()probe.Advance(0,a);assert(probe.mode=='BASELINE');probe.Advance(0,a);assert(probe.mode=='ACTIVE')end
  """)
  return l
 def real_sample_runtime(self):
  # Reuse the engine/SQL fixture, but both collection interpreters execute real
  # source. No Summary override or preinstalled Dialogue sample is permitted.
  l=self.runtime(real_samples=True);bind_actual_request(l)
  l.execute("""
   assert(dialogue.samples[0]==nil and shared.GreatWorkFacts.Summary(0,1)==nil)
   for _,d in ipairs(b.ds)do d.id=d.id+100 end -- Native district IDs are unique.
   function samplePacket(seq,rows)
    local bid=GameInfo.Buildings.BUILDING_AMPHITHEATER.Index
    rows=rows or {{1,bid,0,100,'GREATWORK_BHASA_1'},{2,bid,0,200,'GREATWORK_BHASA_1'}}
    local p={Action='DIALOGUE_SAMPLE',Token='sample:'..seq,Seq=seq,Turn=turn,Generation=dialogue.generation,Valid=1,
     FactsEpoch=shared.GreatWorkFacts.epoch,FactsInput=shared.GreatWorkFacts.inputRevision,
     FactsRefs='',FactsData='',FactsCount=#rows,FactsCities=#cities,AdjData='',AdjCount=0}
    local ordered={};for _,c in ipairs(cities)do ordered[#ordered+1]=c end
    table.sort(ordered,function(x,y)return x.id<y.id end)
    local legacy={}
    for _,c in ipairs(ordered)do
     p.FactsRefs=p.FactsRefs..c.id..','..SPCGreatWorkFacts.Hex(SPCNetworkInput.Reference(c))..',1;'
     legacy[#legacy+1]=c.id..',-1,EMPTY'
     for _,w in ipairs(rows)do if w[1]==c.id then legacy[#legacy+1]=c.id..','..w[4]..','..w[5]end end
    end
    for _,w in ipairs(rows)do p.FactsData=p.FactsData..table.concat(w,',')..';'end
    p.Data=table.concat(legacy,';');p.Count=#legacy
    for _,d in ipairs(ds)do
     local def=P.Info('Districts',d:GetType())
     if def.RequiresPopulation and def.RequiresPopulation~=0 and d:IsComplete()then
      local values=def.DistrictType=='DISTRICT_CAMPUS' and '0,0,2,2,0,0' or '0,0,0,0,0,0'
      p.AdjData=p.AdjData..d.city.id..','..d.id..','..def.DistrictType..','..values..';';p.AdjCount=p.AdjCount+1
     end
    end
    return p
   end
   function sampleRequest(seq,rows)local p=samplePacket(seq,rows);meaningRequest(0,p);return p end
   function meaningAction(action,token)
    meaningRequest(0,{Action=action,CityID=1,Token=token})
    assert(shared.LastToken==token and shared.CultureMeaningView.token==token)
    return shared.CultureMeaningView
   end
   function twoWorks()
    local bid=GameInfo.Buildings.BUILDING_AMPHITHEATER.Index
    return {{1,bid,0,100,'GREATWORK_BHASA_1'},{1,bid,1,101,'GREATWORK_BHASA_1'},{2,bid,0,200,'GREATWORK_BHASA_1'}}
   end
  """)
  return l
 def test_model_matrix_per_work_and_shared_max_cap(self):
  l=self.runtime();l.execute("""
   local model=SPCCultureMeaningModel
   local f={validity='VERIFIED',identity='CULTURE',potential=4,active=4,activeStatus='KNOWN'}
   local w={hasConfirmed=true,availability='KNOWN',count=1,modifierExcludedCount=0,unknownCategoryCount=0}
   local view={validity='VERIFIED',availability='READY',value={districts={},domains={}}}
   for _,d in ipairs({0,1,3,6,10})do for _,count in ipairs({0,1,2})do
    w.count=count;view.value.domains={DISTRICT_CAMPUS={value=d},DISTRICT_COMMERCIAL_HUB={value=d}}
    local p=model.Plan(f,w,view);assert(p.each.SCIENCE==math.floor(0.5*d) and p.each.GOLD==math.floor(1.5*d))
    assert(p.total.SCIENCE==math.floor(0.5*d)*count and p.total.GOLD==math.floor(1.5*d)*count)
   end end
   view.value.domains={};for _,entry in ipairs(model.Domains)do view.value.domains[entry[1]]={value=1}end
   view.value.domains.DISTRICT_THEATER={value=10};w.count=1
   local p=model.Plan(f,w,view)
   assert(p.each.SCIENCE==0 and p.each.GOLD==2 and p.each.PRODUCTION==0 and p.each.CULTURE==0 and p.each.FAITH==0 and p.each.FOOD==0)
   local cat={buildings={[1]={type='T1',tier=1,ordinary=true,domain='DISTRICT_CAMPUS'},[2]={type='T2',tier=2,ordinary=true,domain='DISTRICT_CAMPUS'},[3]={type='T3',tier=3,ordinary=true,domain='DISTRICT_CAMPUS'},[4]={type='T4',tier=4,ordinary=true,domain='DISTRICT_CAMPUS'},[5]={type='EXTRA',tier=4,ordinary=true,domain='DISTRICT_CAMPUS'}},Domain=function(t)return t end}
   local raw={districts={}}
   for id,n in ipairs({2,5})do local d={id=id,type='DISTRICT_CAMPUS',complete=true,pillaged=false,buildings={}};raw.districts[#raw.districts+1]=d;for bid=1,n do d.buildings[#d.buildings+1]={index=bid,complete=true,pillaged=false}end end
   local value=SPCDistrictCompleteness.Calculate(cat,raw)
   assert(value.districts[1].value==3 and value.districts[2].uncapped==14 and value.domains.DISTRICT_CAMPUS.value==10 and value.domains.DISTRICT_CAMPUS.districtID==2)
   view.value=value;p=model.Plan(f,w,view);assert(p.each.SCIENCE==5)
   raw.districts[2].pillaged=true;value=SPCDistrictCompleteness.Calculate(cat,raw);assert(value.domains.DISTRICT_CAMPUS.value==3)
  """)
 def test_switch_fixture_and_pillaged_owned_carrier(self):
  l=self.runtime();l.execute("""
   begin();probe.Advance(0,b);assert(probe.mode=='BASELINE' and old(a,'SCIENCE') and not old(b,'SCIENCE') and configured(a,'SCIENCE')==0)
   probe.Advance(0,b);assert(configured(b,'SCIENCE')==0 and configured(a,'SCIENCE')==0)
   local id=GameInfo.Buildings.BUILDING_SPC_MEANING_PROBE_GOLD_1.Index;b.pillaged[id]=true
   assert(probe.View(0,b).configuredGold==0);probe.Audit();assert(b.pillaged[id]==false and probe.View(0,b).configuredGold==1)
   probe.End(0,b);assert(old(a,'SCIENCE') and old(b,'SCIENCE'))
  """)
 def test_duplicate_action_token_does_not_cycle(self):
  l=self.runtime();l.execute("""
   probe.Advance(0,a,'prepare');local w=writes;probe.Advance(0,a,'prepare');assert(probe.mode=='BASELINE' and writes==w)
   probe.Advance(0,a,'enable');local w=writes;probe.Advance(0,a,'enable');assert(probe.mode=='ACTIVE' and writes==w)
   assert(not pcall(probe.Advance,0,b,'enable'));assert(probe.mode=='ACTIVE')
   probe.Advance(0,a,'scaled');probe.Advance(0,a,'scaledbase');probe.Advance(0,a,'end');local w=writes;probe.Advance(0,a,'end');assert(probe.mode=='OFF' and writes==w)
  """)
 def test_model_floors_each_domain_and_never_substitutes_unknown(self):
  l=self.runtime();l.execute("""
   local f={validity='VERIFIED',identity='CULTURE',potential=4,active=4,activeStatus='KNOWN'}
   local w={hasConfirmed=true,availability='KNOWN',count=1,modifierExcludedCount=0,unknownCategoryCount=0}
   local v=svc.Read(0,a,a.token);local p=SPCCultureMeaningModel.Plan(f,w,v);assert(p.each.SCIENCE==0 and p.each.GOLD==1)
   assert(not pcall(SPCCultureMeaningModel.Parts,'SCIENCE',0.3))
   for _,n in ipairs({0,0.5,1.5,4.5,5})do local sum=0;for _,name in ipairs(SPCCultureMeaningModel.Parts('SCIENCE',n))do sum=sum+2^tonumber(name:match('_(%d+)$'))/2 end;assert(sum==n)end
   v.availability='TEMPORARILY_UNAVAILABLE';assert(not pcall(SPCCultureMeaningModel.Plan,f,w,v));v.availability='READY'
   for _,d in ipairs(v.value.districts)do if d.domain=='DISTRICT_CAMPUS'then d.buildings[1].tier=nil end end
   assert(not pcall(SPCCultureMeaningModel.Plan,f,w,v))
  """)
 def test_off_baseline_active_end_single_city(self):
  l=self.runtime();l.execute("""
   assert(probe.mode=='OFF' and configured(a,'SCIENCE')==0 and old(a,'SCIENCE') and old(b,'SCIENCE'))
   probe.Advance(0,a);assert(not old(a,'SCIENCE') and old(b,'SCIENCE'));assert(configured(a,'SCIENCE')==0)
   probe.Advance(0,a);assert(configured(a,'SCIENCE')==0 and configured(a,'GOLD')==1 and configured(b,'GOLD')==0)
   gwa.Audit(0);assert(not old(a,'SCIENCE') and old(b,'SCIENCE'))
   local w=writes;probe.Audit();probe.Audit();assert(writes==w)
   probe.End(0,a);assert(probe.mode=='OFF' and configured(a,'SCIENCE')==0 and configured(a,'GOLD')==0 and old(a,'SCIENCE') and old(b,'SCIENCE'))
   assert(a.present[GameInfo.Buildings.BUILDING_LIBRARY.Index] and a.present[GameInfo.Buildings.BUILDING_FAIR.Index])
  """)
 def test_same_era_work_change_and_l1_zero_write(self):
  l=self.runtime();l.execute("""
   begin();local w=writes;local prior=total(a);a.workCount=2;confirmCollection()
   assert(probe.lastPlan.count==2 and probe.lastPlan.total.SCIENCE==0 and probe.lastPlan.total.GOLD==2)
   assert(configured(a,'SCIENCE')==0 and total(a)==prior and writes==w)
   a.workCount=0;confirmCollection();assert(configured(a,'SCIENCE')==0 and configured(a,'GOLD')==0)
   a.workCount=1;confirmCollection();assert(configured(a,'SCIENCE')==0)
  """)
 def test_real_confirmed_count_and_eligibility_notifications(self):
  f=Fixture();f.check("""
   notices={};shared.GreatWorkFacts.OnConfirmed=function(pid,ids)notices[#notices+1]=ids end
   local rows={{7,10,0,100,'GREATWORK_BHASA_1'},{7,10,1,101,'GREATWORK_BHASA_1'}}
   assert(receive(1,rows));assert(#notices==1);assert(receive(2,rows));assert(#notices==1)
   table.remove(rows,2);assert(receive(3,rows));assert(#notices==2 and #notices[2]==1 and notices[2][1]==7)
   local s=shared.GreatWorkFacts.Summary(0,7);assert(s.count==1 and s.eraCount==1 and s.modifierExcludedCount==0 and s.unknownCategoryCount==0)
   assert(s.works==nil and s.excluded==nil and s.eras==nil)
   rows[#rows+1]={7,10,1,105,'UNKNOWN_WRITING'};assert(receive(4,rows));s=shared.GreatWorkFacts.Summary(0,7)
   assert(#notices==3 and s.count==1 and s.modifierExcludedCount==1)
   rows[2]={7,10,1,106,'RELIC'};assert(receive(5,rows));assert(#notices==4 and shared.GreatWorkFacts.Summary(0,7).modifierExcludedCount==0)
  """)
 def test_building_governor_same_turn_and_unknown(self):
  l=self.runtime();l.execute("""
   begin();building(a,'BUILDING_UNIVERSITY',a.ds[6]);fire('CityBuildingsChanged',0,1)
   assert(configured(a,'SCIENCE')==1 and probe.lastPlan.domains.DISTRICT_CAMPUS.value==3)
   building(a,'BUILDING_MARKET',a.ds[3]);fire('CityBuildingsChanged',0,1);assert(configured(a,'GOLD')==4)
   local w=writes;a.worksUnknown=true;probe.Audit();assert(writes==w and configured(a,'SCIENCE')==1 and probe.error:find('ME_WORKS_UNKNOWN'))
   a.worksUnknown=false;a.active=nil;probe.Audit();assert(writes==w and probe.error:find('ME_ACTIVE_UNKNOWN'))
   a.active=3;fire('GovernorChanged',0);assert(configured(a,'SCIENCE')==0 and configured(a,'GOLD')==0)
   a.active=4;fire('GovernorEstablished',0);assert(configured(a,'SCIENCE')==1 and configured(a,'GOLD')==4)
  """)
 def test_refuse_or_withdraw_unsupported_fixture(self):
  l=self.runtime();l.execute("""
   a.badCount=1;assert(not pcall(probe.Advance,0,a));assert(probe.mode=='OFF' and old(a,'SCIENCE') and configured(a,'SCIENCE')==0)
   a.badCount=0;a.categoryUnknown=1;assert(not pcall(probe.Advance,0,a));assert(probe.mode=='OFF')
   a.categoryUnknown=0;begin();a.badCount=1;confirmCollection();assert(configured(a,'SCIENCE')==0 and probe.error:find('ME_FIXTURE_UNSUPPORTED_WORK'))
   probe.End(0,a);assert(probe.mode=='OFF' and old(a,'SCIENCE'))
  """)
 def test_old_withdrawal_failure_does_not_enable_new(self):
  l=self.runtime();l.execute("""
   failRemove=GameInfo.Buildings.BUILDING_SPC_B060_SCIENCE_P1.Index
   assert(not pcall(probe.Advance,0,a));assert(gwa.IsMeaningHeld(0,a) and configured(a,'SCIENCE')==0 and probe.error)
   assert(old(a,'SCIENCE'));failRemove=nil;probe.End(0,a);assert(probe.mode=='OFF' and old(a,'SCIENCE'))
   begin();assert(configured(a,'SCIENCE')==0)
  """)
 def test_new_write_failure_and_no_early_old_resume(self):
  l=self.runtime();l.execute("""
   probe.Advance(0,a);failCreate=true;assert(not pcall(probe.Advance,0,a) and probe.mode=='BASELINE')
   assert(configured(a,'SCIENCE')==0 and configured(a,'GOLD')==0 and gwa.IsMeaningHeld(0,a) and probe.error)
   failCreate=false;probe.End(0,a);assert(probe.mode=='OFF' and old(a,'SCIENCE'))
   building(a,'BUILDING_UNIVERSITY',a.ds[6]);svc.MarkDirty();begin();failRemove=GameInfo.Buildings.BUILDING_SPC_MEANING_PROBE_SCIENCE_1.Index
   assert(not pcall(probe.End,0,a));assert(gwa.IsMeaningHeld(0,a) and not old(a,'SCIENCE') and probe.stopping);probe.Audit();assert(configured(a,'GOLD')==0)
   failRemove=nil;probe.End(0,a);assert(probe.mode=='OFF' and old(a,'SCIENCE'))
  """)
 def test_loss_confirmed_only_idempotent_no_recapture_replay(self):
  l=self.runtime();l.execute("""
   begin();a.owner=3
   local loss={confirmed=false,targetID=a.id,origin={owner=0}}
   assert(not pcall(exits.CultureMeaningProbe,a,loss));assert(configured(a,'SCIENCE')==0)
   loss.confirmed=true;exits.CultureMeaningProbe(a,loss);assert(probe.mode=='OFF' and configured(a,'SCIENCE')==0)
   local w=writes;exits.CultureMeaningProbe(a,loss);assert(writes==w and old(b,'SCIENCE'))
   a.owner=0;fire('GovernorChanged',0);assert(probe.mode=='OFF' and configured(a,'SCIENCE')==0)
  """)
 def test_load_cleanup_foreign_only_owned_no_probe_replay(self):
  l=self.runtime();l.execute("""
   begin();a.owner=3;fire('LoadScreenClose');assert(probe.mode=='OFF' and configured(a,'SCIENCE')==0 and configured(a,'GOLD')==0)
   assert(a.present[GameInfo.Buildings.BUILDING_LIBRARY.Index] and a.token=='persistent:1')
   a.owner=0;fire('PlayerTurnActivated',0);assert(probe.mode=='OFF' and configured(a,'SCIENCE')==0)
  """)
 def test_reference_change_never_adopts_old_probe(self):
  l=self.runtime();l.execute("begin();a.token='new-city';probe.Audit();assert(probe.mode=='OFF' and configured(a,'SCIENCE')==0 and configured(a,'GOLD')==0);assert(not gwa.IsMeaningHeld(0,a))")
 def test_read_only_bounded_diagnostic_and_affected_scope(self):
  l=self.runtime();l.execute("""
   begin();local w=writes;local n=counts.dc_read or 0;probe.Audit({player=3});probe.Audit({player=0,city=2});assert((counts.dc_read or 0)==n)
   local text=probe.Describe(0,a);local view=probe.View(0,a);assert(text:find('每件理论') and view.science==0 and view.totalGold==1);assert(writes==w)
   probe.End(0,a);local n=counts.dc_read or 0;probe.Audit();assert((counts.dc_read or 0)==n)
  """)
 def test_sql_exact_single_city_native_yield_definitions(self):
  rows=self.sql.execute("select BuildingType,InternalOnly,CitizenSlots,Housing,PrereqDistrict from Buildings where BuildingType like 'BUILDING_SPC_MEANING_PROBE_%'").fetchall();self.assertEqual(len(rows),16)
  for b,internal,slots,housing,district in rows:
   self.assertEqual((internal,slots,housing,district),(1,0,0,'DISTRICT_CITY_CENTER'))
   suffix=b.removeprefix('BUILDING_SPC_MEANING_PROBE_')
   y,part=suffix.split('_',1);self.assertIn(y,{'SCIENCE','GOLD','CULTURE'})
   single=part in {'SINGLE3','SINGLE3_SCALE100'}
   amount=3 if single else 2**int(part)/(1 if y=='CULTURE' else 2)
   modifiers=self.sql.execute('select ModifierId from BuildingModifiers where BuildingType=?',(b,)).fetchall();self.assertEqual(len(modifiers),7)
   categories=set()
   for(mid,)in modifiers:
    self.assertEqual(self.sql.execute('select ModifierType from Modifiers where ModifierId=?',(mid,)).fetchone()[0],'MODIFIER_SINGLE_CITY_ADJUST_GREATWORK_YIELD')
    args=dict(self.sql.execute('select Name,Value from ModifierArguments where ModifierId=?',(mid,)))
    self.assertEqual(args['YieldType'],'YIELD_'+y);self.assertEqual(float(args['YieldChange']),amount);categories.add(args['GreatWorkObjectType'])
    self.assertEqual(set(args),{'GreatWorkObjectType','YieldType','YieldChange'}|({'ScalingFactor'} if part=='SINGLE3_SCALE100' else set()))
    if part=='SINGLE3_SCALE100':self.assertEqual(float(args['ScalingFactor']),100)
   self.assertEqual(categories,{'GREATWORKOBJECT_'+c for c in ['WRITING','MUSIC','SCULPTURE','PORTRAIT','LANDSCAPE','RELIGIOUS','ARTIFACT']})
 def test_native_read_baseline_guard_no_gameplay_writes(self):
  l=self.runtime();l.globals().include('UI/BoostGreatWorkRead')
  l.execute("""
   -- Deliberately mock the UI getter: verifies read/compare only, not engine precision.
   local get=a.GetBuildings
   a.GetBuildings=function(c)local b=get(c)
    b.GetNumGreatWorkSlots=function(_,id)return id==GameInfo.Buildings.BUILDING_AMPHITHEATER.Index and c.workCount or 0 end
    b.GetGreatWorkInSlot=function(_,id,s)return s+100 end;b.GetGreatWorkTypeFromIndex=function()return 'GREATWORK_BHASA_1'end
    b.IsBuildingThemedCorrectly=function()return false end
    b.GetBuildingYieldFromGreatWorks=function(_,y,id)local typ=GameInfo.Yields[y].YieldType:gsub('YIELD_','');return (configured(c,typ)+(typ=='CULTURE' and 2 or 0))*c.workCount end
    return b
   end
   probe.Advance(0,a);local w=writes;assert(SPCBoostGreatWorkRead.Meaning(P,a,probe.View(0,a),true):find('已记录'));assert(writes==w)
   probe.Advance(0,a);local w=writes;local t=SPCBoostGreatWorkRead.Meaning(P,a,probe.View(0,a),false);assert(t:find('原生作品收益：科研 0.00 / 金币 1.00 / 文化 3.00'));assert(writes==w)
   a.workCount=2;t=SPCBoostGreatWorkRead.Meaning(P,a,probe.View(0,a),false);assert(t:find('ME_UI_WORK_COUNT_MISMATCH') and t:find('不记录成功基线'))
   probe.End(0,a);assert(SPCBoostGreatWorkRead.Meaning(P,a,probe.View(0,a),false):find('测试已关闭'))
  """)
 def test_import_registry_rejects_each_missing_action_import(self):
  root=ET.parse(M/'SpecializationP0.modinfo').getroot();require_meaning_imports(root)
  for name in ['CultureMeaningModel.lua','CultureMeaningProbe.lua']:
   with self.subTest(missing=name):
    copy=ET.fromstring(ET.tostring(root));imports=copy.find("./InGameActions/ImportFiles[@id='SPCP0_Common']")
    imports.remove(next(e for e in imports if e.text==name))
    self.assertIn(name,[e.text for e in copy.find('Files')])
    with self.assertRaisesRegex(AssertionError,'must be imported'):require_meaning_imports(copy)
 def test_actual_request_prepare_read_enable_end_one_view(self):
  l=self.runtime();bind_actual_request(l);l.execute("""
   local read=probe.View;viewReads=0
   probe.View=function(...)viewReads=viewReads+1;return read(...)end
   local function request(action,token)
    shared.CultureMeaningView={token='stale',mode='ACTIVE'}
    meaningRequest(0,{Action=action,CityID=1,Token=token})
    assert(shared.LastToken==token and shared.CultureMeaningView.token==token)
   end
   request('CULTURE_MEANING_ADVANCE','prepare');assert(probe.mode=='BASELINE' and viewReads==1 and not old(a,'SCIENCE'))
   local w=writes;local action=probe.lastAction
   request('CULTURE_MEANING_READ','read');assert(writes==w and probe.lastAction==action and viewReads==2)
   request('CULTURE_MEANING_ADVANCE','enable');assert(probe.mode=='ACTIVE' and viewReads==3 and configured(a,'SCIENCE')==0)
   request('CULTURE_MEANING_ADVANCE','scaled');request('CULTURE_MEANING_ADVANCE','scaledbase');request('CULTURE_MEANING_ADVANCE','end');assert(probe.mode=='OFF' and viewReads==6 and configured(a,'SCIENCE')==0 and old(a,'SCIENCE'))
   assert(old(b,'SCIENCE') and a.token=='persistent:1')
  """)
 def test_actual_request_outer_failure_stages_clear_stale_view(self):
  failures=[('CITY',"a.owner=3",'ME_CITY_UNKNOWN'),('MODULE',"shared.CultureMeaningProbe=nil",'ME_MODULE_NOT_READY'),
   ('ADVANCE',"probe.Advance=nil",'ME_ACTION_NOT_READY'),
   ('VIEW',"probe.View=function()error('ME_READ_FAILED')end",'ME_READ_FAILED'),
   ('VIEW',"probe.View=nil",'ME_VIEW_NOT_READY'),('VIEW',"probe.View=function()return {owner=0,cityID=2}end",'ME_VIEW_INVALID'),
   ('DESCRIBE',"probe.Describe=function()error('ME_TEXT_FAILED')end",'ME_TEXT_FAILED'),
   ('DESCRIBE',"probe.Describe=nil",'ME_DESCRIBE_NOT_READY'),('DESCRIBE',"probe.Describe=function()return nil end",'ME_REPORT_INVALID')]
  for stage,setup,code in failures:
   with self.subTest(stage=stage,code=code):
    l=self.runtime();bind_actual_request(l);l.execute(setup);l.globals().failureAction='CULTURE_MEANING_ADVANCE' if stage=='ADVANCE' else 'CULTURE_MEANING_READ';l.execute("""
     shared.CultureMeaningView={token='old'};local w=writes
     meaningRequest(0,{Action=failureAction,CityID=1,Token='failure'})
     assert(shared.CultureMeaningView==nil and shared.LastToken=='failure' and writes==w)
    """);self.assertIn('['+stage+']',l.globals().shared.Snapshot);self.assertIn(code,l.globals().shared.Snapshot)
 def test_actual_request_advance_rejection_preserves_detail_not_baseline(self):
  l=self.runtime();bind_actual_request(l);l.execute("""
   probe.Advance(0,a,'before');assert(probe.mode=='BASELINE')
   probe.Advance=function()error('ME_WORKS_UNKNOWN'..string.char(10)..string.rep('x',1000))end
   local w=writes
   meaningRequest(0,{Action='CULTURE_MEANING_ADVANCE',CityID=1,Token='rejected'})
   assert(shared.CultureMeaningView.token=='rejected' and shared.CultureMeaningView.mode=='BASELINE')
   assert(shared.CultureMeaningView.error:find('ME_WORKS_UNKNOWN') and #shared.CultureMeaningView.error<=240)
   assert(shared.Snapshot:find('%[ADVANCE%]') and shared.Snapshot:find('ME_WORKS_UNKNOWN'))
   assert(not shared.CultureMeaningView.error:find('%c') and writes==w)
   assert(not probe.error) -- A request-local failure does not rewrite probe authority.
  """)
 def test_actual_request_mixed_failure_keeps_both_errors(self):
  l=self.runtime();bind_actual_request(l);l.execute("""
   probe.Advance=function()error('ME_ACTION_REJECTED')end
   probe.View=function()error('ME_VIEW_FAILED')end
   shared.CultureMeaningView={token='old'}
   meaningRequest(0,{Action='CULTURE_MEANING_ADVANCE',CityID=1,Token='mixed'})
   assert(shared.LastToken=='mixed' and shared.CultureMeaningView==nil)
   assert(shared.Snapshot:find('%[VIEW%]') and shared.Snapshot:find('ME_VIEW_FAILED') and shared.Snapshot:find('ME_ACTION_REJECTED'))
  """)
 def test_actual_request_configuration_unknown_is_not_zero_or_success(self):
  l=self.runtime();bind_actual_request(l);l.execute("""
   probe.Advance(0,a,'before');local raw=probe.View
   probe.View=function(...)local v=raw(...);v.configuredScience=nil;v.configurationError='ME_CARRIER_UNKNOWN';return v end
   local w=writes
   meaningRequest(0,{Action='CULTURE_MEANING_READ',CityID=1,Token='unknown'})
   assert(shared.LastToken=='unknown' and shared.CultureMeaningView.token=='unknown')
   assert(shared.CultureMeaningView.configuredScience==nil and shared.CultureMeaningView.error=='ME_CARRIER_UNKNOWN')
   assert(shared.Snapshot:find('ME_CARRIER_UNKNOWN') and writes==w and not probe.error)
  """)
 def test_actual_request_invalid_or_foreign_ingress_does_not_run_probe(self):
  l=self.runtime();bind_actual_request(l);l.execute("""
   local w=writes;local n=counts.dc_read or 0
   meaningRequest(3,{Action='CULTURE_MEANING_ADVANCE',CityID=1,Token='foreign'})
   meaningRequest(0,{Action='CULTURE_MEANING_ADVANCE',CityID=1,Token=string.rep('x',101)})
   assert(writes==w and (counts.dc_read or 0)==n and probe.mode=='OFF' and shared.LastToken==nil)
  """)
 def test_registration_localization_exact_scope(self):
  root=ET.parse(M/'SpecializationP0.modinfo').getroot();self.assertEqual(root.get('version'),'182');require_meaning_imports(root)
  files=[e.text for e in root.find('Files')];self.assertEqual(len(files),len(set(files)))
  self.assertEqual(set(files),{str(p.relative_to(M))for p in M.rglob('*')if p.is_file() and p.name not in {'.DS_Store','SpecializationP0.modinfo'}})
  self.assertTrue({'CultureMeaningModel.lua','CultureMeaningProbe.lua','Data/CultureMeaningProbe.sql'}<=set(files))
  self.assertEqual(root.find(".//UpdateDatabase[@id='SPC_CultureMeaningProbe']/File").text,'Data/CultureMeaningProbe.sql')
  xml=ET.parse(M/'UI/P0Panel.xml').getroot();self.assertIsNotNone(xml.find('.//*[@ID="MeaningProbeButtonCaption"]'))
  ui=(M/'UI/P0Panel.lua').read_text();self.assertIn("request('CULTURE_MEANING_ADVANCE')",ui);self.assertIn("request('CULTURE_MEANING_READ')",ui)
  text=(M/'Text/TestText.sql').read_text()
  for key in ['LOC_SPC_CULTURE_MEANING_PROBE','LOC_SPC_CULTURE_MEANING_PROBE_HINT','LOC_SPC_MEANING_PROBE_CARRIER']:self.assertEqual(text.count("'"+key+"'"),2)
  src=(M/'CultureMeaningProbe.lua').read_text()
  for forbidden in ['collectgarbage','SetProperty','SetUpdate','GameCoreEventPublishComplete','CityWorkerChanged','OnHover']:self.assertNotIn(forbidden,src)
  self.assertIn("RegisterExit('CultureMeaningProbe'",src)
  self.assertIn("include('CultureMeaningProbe')",(M/'Gameplay.lua').read_text())

 # New assertions exercise the actual Dialogue module and explicit new formula.
 def test_floor_before_same_yield_sum_and_work_count_counterexamples(self):
  l=self.runtime();l.execute("""
   local f={validity='VERIFIED',identity='CULTURE',potential=4,active=4,activeStatus='KNOWN'}
   local w={hasConfirmed=true,availability='KNOWN',count=2,modifierExcludedCount=0,unknownCategoryCount=0}
   local v={validity='VERIFIED',availability='READY',value={districts={},domains={}}}
   for _,e in ipairs(SPCCultureMeaningModel.Domains)do v.value.domains[e[1]]={value=1}end
   local p=SPCCultureMeaningModel.Plan(f,w,v)
   assert(p.each.GOLD==2 and p.total.GOLD==4 and p.each.PRODUCTION==0 and p.total.SCIENCE==0)
   assert(p.domains.DISTRICT_COMMERCIAL_HUB.rawEach==1.5 and p.domains.DISTRICT_HARBOR.each==1)
   v.value.domains.DISTRICT_COMMERCIAL_HUB.value=3;p=SPCCultureMeaningModel.Plan(f,w,v)
   assert(p.each.GOLD==5 and p.total.GOLD==10) -- 4+1, neither floor(4.5+1.5)=6 nor total-first
   for _,n in ipairs({0,1,3,6,10})do local sum=0;for _,name in ipairs(SPCCultureMeaningModel.Parts('CULTURE',n))do sum=sum+2^tonumber(name:match('_(%d+)$'))end;assert(sum==n)end
   assert(not pcall(SPCCultureMeaningModel.Parts,'CULTURE',0.5))
  """)
 def test_four_phase_cycle_and_scoped_dialogue_restore(self):
  l=self.runtime();l.execute("""
   local first=GameInfo.GreatWorks.GREATWORK_BHASA_1
   local era=GameInfo.GreatPersonIndividuals[first.GreatPersonIndividualType].EraType
   for work in GameInfo.GreatWorks()do local gp=work.GreatPersonIndividualType and GameInfo.GreatPersonIndividuals[work.GreatPersonIndividualType]
    if work.GreatWorkObjectType=='GREATWORKOBJECT_WRITING' and gp and gp.EraType~=era then dialogue.samples[0].cities[2][2]={id=3,type=work.GreatWorkType};break end
   end
   dialogue.Audit(0);assert(dialogue.last[0][2].applied==25)
   local other=dialogue.last[0][2].carrier;local otherID=GameInfo.Buildings[other].Index;assert(b.present[otherID])
   probe.Advance(0,a);assert(dialogue.IsMeaningProbeHeld(0,a,0) and configured(a,'CULTURE')==0)
   probe.Advance(0,a);assert(probe.mode=='ACTIVE' and configured(a,'CULTURE')==1 and probe.View(0,a).dialoguePercent==0)
   probe.Advance(0,a);assert(probe.mode=='SCALED' and configured(a,'CULTURE')==1 and probe.View(0,a).dialoguePercent==100)
   local w=writes;probe.Audit();probe.Audit();assert(writes==w and b.present[otherID])
   probe.Advance(0,a);assert(probe.mode=='SCALED_BASELINE' and configured(a,'CULTURE')==0 and probe.View(0,a).dialoguePercent==100)
   probe.Advance(0,a);assert(probe.mode=='OFF' and dialogue.meaningOverride==nil and old(a,'SCIENCE') and b.present[otherID])
   assert(not a.present[GameInfo.Buildings.BUILDING_SPC_B059_TEST100.Index])
  """)
 def test_unknown_dialogue_retains_binding_and_never_records_success(self):
  l=self.runtime();l.execute("""
   begin();probe.Advance(0,a);assert(probe.mode=='SCALED');local n=configured(a,'CULTURE')
   dialogue.samples[0]=nil;probe.Audit();assert(probe.error:find('ME_DIALOGUE_SAMPLE_PAIR_PENDING') and configured(a,'CULTURE')==n)
   assert(dialogue.IsMeaningProbeHeld(0,a,100) and gwa.IsMeaningHeld(0,a) and probe.View(0,a).dialoguePercent==nil)
   collection();probe.Audit();assert(not probe.error and probe.View(0,a).dialoguePercent==100)
   probe.End(0,a);assert(probe.mode=='OFF')
  """)
 def test_unrelated_transfer_and_return_keep_fixture_binding(self):
  l=self.runtime();l.execute("""
   begin();probe.Advance(0,a);local ref=SPCNetworkInput.Reference(a)
   fire('CityTransfered',3,9,0);assert(dialogue.IsMeaningProbeHeld(0,a,100) and gwa.IsMeaningHeld(0,a))
   collection();probe.Audit();assert(probe.View(0,a).dialoguePercent==100)
   returns.Dialogue(0,b);assert(dialogue.IsMeaningProbeHeld(0,a,100));collection();probe.Audit()
   assert(probe.mode=='SCALED' and configured(a,'CULTURE')==1 and SPCNetworkInput.Reference(a)==ref)
  """)
 def test_meaning_removal_failure_keeps_both_holds(self):
  l=self.runtime();l.execute("""
   begin();probe.Advance(0,a);failRemove=GameInfo.Buildings.BUILDING_SPC_MEANING_PROBE_CULTURE_0.Index
   assert(not pcall(probe.End,0,a));assert(probe.stopping and configured(a,'CULTURE')==1 and dialogue.IsMeaningProbeHeld(0,a,100) and gwa.IsMeaningHeld(0,a))
   assert(not old(a,'SCIENCE'));failRemove=nil;probe.Advance(0,a);assert(probe.mode=='OFF' and dialogue.meaningOverride==nil)
  """)
 def test_dialogue_removal_failure_does_not_release_gwa(self):
  l=self.runtime();l.execute("""
   begin();probe.Advance(0,a);failRemove=GameInfo.Buildings.BUILDING_SPC_B059_TEST100.Index
   assert(not pcall(probe.End,0,a));assert(configured(a,'CULTURE')==0 and gwa.IsMeaningHeld(0,a) and dialogue.IsMeaningProbeHeld(0,a,100))
   failRemove=nil;probe.Advance(0,a);assert(probe.mode=='OFF' and not a.present[GameInfo.Buildings.BUILDING_SPC_B059_TEST100.Index])
  """)
 def test_load_removes_percent_and_additions_even_when_foreign(self):
  l=self.runtime();l.execute("""
   begin();probe.Advance(0,a);a.owner=3;fire('LoadScreenClose')
   assert(probe.mode=='OFF' and configured(a,'CULTURE')==0 and configured(a,'GOLD')==0 and dialogue.meaningOverride==nil)
   assert(not a.present[GameInfo.Buildings.BUILDING_SPC_B059_TEST100.Index] and a.token=='persistent:1')
  """)
 def test_scoped_dialogue_control_rejects_foreign_reference_and_other_test(self):
  l=self.runtime();l.execute("""
   local n=writes;assert(not pcall(dialogue.HoldMeaningProbe,3,a,100));assert(writes==n)
   dialogue.test[0]={city=1,percent=50};assert(not pcall(dialogue.HoldMeaningProbe,0,a,0));assert(writes==n);dialogue.test[0]=nil
   dialogue.HoldMeaningProbe(0,a,100);local n=writes;a.token='changed'
   assert(not pcall(dialogue.ReleaseMeaningProbe,0,a));assert(writes==n and dialogue.meaningOverride~=nil)
   assert(not pcall(dialogue.HoldMeaningProbe,0,b,100))
  """)
 def test_native_four_readings_compare_separate_percent_baselines(self):
  for scale_added in (False,True):
   with self.subTest(mock_native_scales_additions=scale_added):
    l=self.runtime();l.globals().mockScale=scale_added;l.globals().include('UI/BoostGreatWorkRead')
    l.execute("""
     local get=a.GetBuildings
     a.GetBuildings=function(c)local b=get(c)
      b.GetNumGreatWorkSlots=function(_,id)return id==GameInfo.Buildings.BUILDING_AMPHITHEATER.Index and 1 or 0 end
      b.GetGreatWorkInSlot=function()return 100 end;b.GetGreatWorkTypeFromIndex=function()return 'GREATWORK_BHASA_1'end
      b.IsBuildingThemedCorrectly=function()return false end
      b.GetBuildingYieldFromGreatWorks=function(_,y,id)
       local typ=GameInfo.Yields[y].YieldType:gsub('YIELD_','');local n=configured(c,typ)
       if typ=='CULTURE' then local factor=probe.View(0,c).dialoguePercent==100 and 2 or 1;return 2*factor+n*(mockScale and factor or 1)end
       return n
      end;return b
     end
     for i=1,4 do probe.Advance(0,a);lastText=SPCBoostGreatWorkRead.Meaning(P,a,probe.View(0,a),true);assert(not lastText:find('未确认：'))end
     assert(lastText:find('关闭旧对话：作品文化 Δ%+1.00'))
     assert(lastText:find(mockScale and '旧对话100%%：作品文化 Δ%+2.00' or '旧对话100%%：作品文化 Δ%+1.00'))
     local w=writes;SPCBoostGreatWorkRead.Meaning(P,a,probe.View(0,a),false);assert(writes==w)
     probe.Advance(0,a);assert(SPCBoostGreatWorkRead.Meaning(P,a,probe.View(0,a),true):find('已关闭'))
    """)
 def test_first_probe_fallback_does_not_clear_ready_other_city_dialogue(self):
  l=self.runtime();l.execute("""
   -- Explicit existing carrier and reliable two-era normal sample on other city.
   local first=GameInfo.GreatWorks.GREATWORK_BHASA_1;local era=GameInfo.GreatPersonIndividuals[first.GreatPersonIndividualType].EraType
   for work in GameInfo.GreatWorks()do local gp=work.GreatPersonIndividualType and GameInfo.GreatPersonIndividuals[work.GreatPersonIndividualType]
    if work.GreatWorkObjectType=='GREATWORKOBJECT_WRITING' and gp and gp.EraType~=era then dialogue.samples[0].cities[2][2]={id=3,type=work.GreatWorkType};break end
   end
   dialogue.Audit(0);local id=GameInfo.Buildings[dialogue.last[0][2].carrier].Index
   assert(dialogue.ready and b.present[id]);probe.ready=false
   probe.Advance(0,a);assert(probe.mode=='BASELINE' and b.present[id] and dialogue.last[0][2].applied==25)
  """)
 def test_native_read_refreshes_current_phase_after_stale_ui_getter(self):
  l=self.runtime();l.globals().include('UI/BoostGreatWorkRead');l.execute("""
   local get=a.GetBuildings;stale=true
   a.GetBuildings=function(c)local b=get(c)
    b.GetNumGreatWorkSlots=function(_,id)return id==GameInfo.Buildings.BUILDING_AMPHITHEATER.Index and 1 or 0 end
    b.GetGreatWorkInSlot=function()return 100 end;b.GetGreatWorkTypeFromIndex=function()return 'GREATWORK_BHASA_1'end
    b.IsBuildingThemedCorrectly=function()return false end
    b.GetBuildingYieldFromGreatWorks=function(_,y,id)local typ=GameInfo.Yields[y].YieldType:gsub('YIELD_','');return (typ=='CULTURE' and 2 or 0)+(stale and 0 or configured(c,typ))end
    return b
   end
   probe.Advance(0,a);SPCBoostGreatWorkRead.Meaning(P,a,probe.View(0,a),true)
   probe.Advance(0,a);local t=SPCBoostGreatWorkRead.Meaning(P,a,probe.View(0,a),true);assert(t:find('Δ%+0.00'))
   stale=false;local w=writes;t=SPCBoostGreatWorkRead.Meaning(P,a,probe.View(0,a),false)
   assert(t:find('Δ%+1.00') and writes==w and probe.mode=='ACTIVE')
  """)
 def test_dialogue_view_verifies_carrier_health_not_cached_applied(self):
  l=self.runtime();l.execute("""
   begin();probe.Advance(0,a);local id=GameInfo.Buildings.BUILDING_SPC_B059_TEST100.Index
   assert(probe.View(0,a).dialoguePercent==100);a.present[id]=nil
   assert(probe.View(0,a).dialoguePercent==nil and probe.View(0,a).dialogueError:find('ME_DIALOGUE_PROJECTION_CHANGED'))
   probe.Audit();assert(probe.View(0,a).dialoguePercent==100);a.pillaged[id]=true
   assert(probe.View(0,a).dialoguePercent==nil and probe.View(0,a).dialogueError:find('ME_DIALOGUE_CARRIER_DAMAGED'))
  """)
 def test_failed_percent_enable_is_reported_and_next_action_ends_safely(self):
  l=self.runtime();l.execute("""
   begin();failCreate=true;assert(not pcall(probe.Advance,0,a));assert(probe.error and gwa.IsMeaningHeld(0,a))
   assert(probe.Describe(0,a):find('对话配置未确认'))
   failCreate=false;probe.Advance(0,a);assert(probe.mode=='OFF' and dialogue.meaningOverride==nil and configured(a,'CULTURE')==0)
  """)
 def test_real_sample_request_cold_c00_uses_both_receivers(self):
  l=self.real_sample_runtime();l.execute("""
   local on=shared.GreatWorkFacts.OnConfirmed;local paired=probe.CollectionConfirmed
   local received=dialogue.Receive;order={}
   shared.GreatWorkFacts.OnConfirmed=function(pid,ids)
    order[#order+1]='FACTS';assert(shared.GreatWorkFacts.ack==1 and dialogue.samples[0]==nil)
    assert(shared.GreatWorkFacts.Summary(0,1).count==1);if on then on(pid,ids)end
   end
   dialogue.Receive=function(pid,p)local accepted=received(pid,p);order[#order+1]='DIALOGUE';assert(accepted==true);return accepted end
   probe.CollectionConfirmed=function(pid,p)
    order[#order+1]='PAIR';assert(dialogue.samples[0].seq==p.Seq);return paired(pid,p)
   end
   sampleRequest(1);assert(table.concat(order,',')=='FACTS,DIALOGUE,PAIR')
   local v=meaningAction('CULTURE_MEANING_ADVANCE','cold-c00')
   assert(v.mode=='BASELINE' and v.dialoguePercent==0 and not v.error and v.count==1)
   assert(gwa.IsMeaningHeld(0,a) and not old(a,'SCIENCE') and old(b,'SCIENCE'))
   assert(dialogue.samples[0].generation==dialogue.generation and shared.GreatWorkFacts.Summary(0,1).reference==v.reference)
  """)
 def test_real_sample_callback_does_not_mix_new_facts_with_old_dialogue(self):
  l=self.real_sample_runtime();l.execute("""
   sampleRequest(1);meaningAction('CULTURE_MEANING_ADVANCE','c00');meaningAction('CULTURE_MEANING_ADVANCE','c10')
   local on=shared.GreatWorkFacts.OnConfirmed;local paired=probe.CollectionConfirmed
   factCallbacks=0;pairCallbacks=0
   shared.GreatWorkFacts.OnConfirmed=function(pid,ids)
    factCallbacks=factCallbacks+1
    assert(shared.GreatWorkFacts.ack==2 and shared.GreatWorkFacts.Summary(0,1).count==2)
    assert(dialogue.samples[0].seq==1 and probe.lastPlan.count==1)
    assert(probe.View(0,a).dialoguePercent==nil)
    if on then on(pid,ids)end
    assert(probe.lastPlan.count==1) -- Facts callback cannot confirm the old Dialogue projection.
   end
   probe.CollectionConfirmed=function(pid,p)
    pairCallbacks=pairCallbacks+1;assert(dialogue.samples[0].seq==2 and p.Seq==2)
    return paired(pid,p)
   end
   sampleRequest(2,twoWorks())
   assert(factCallbacks==1 and pairCallbacks==1 and probe.mode=='ACTIVE' and not probe.error)
   assert(probe.lastPlan.count==2 and probe.lastPlan.total.GOLD==2 and probe.View(0,a).dialoguePercent==0)
   assert(configured(a,'GOLD')==1 and old(b,'SCIENCE') and not old(a,'SCIENCE'))
  """)
 def test_real_sample_identical_new_sequence_recovers_after_busy_without_fact_change(self):
  l=self.real_sample_runtime();l.execute("""
   sampleRequest(1);meaningAction('CULTURE_MEANING_ADVANCE','c00');meaningAction('CULTURE_MEANING_ADVANCE','c10')
   local on=shared.GreatWorkFacts.OnConfirmed;local paired=probe.CollectionConfirmed;factCallbacks=0;pairCallbacks=0
   shared.GreatWorkFacts.OnConfirmed=function(...)factCallbacks=factCallbacks+1;if on then return on(...)end end
   probe.CollectionConfirmed=function(...)pairCallbacks=pairCallbacks+1;return paired(...)end
   dialogue.busy=true;sampleRequest(2)
   assert(dialogue.busy and probe.error and probe.View(0,a).dialoguePercent==nil)
   assert(configured(a,'GOLD')==1 and gwa.IsMeaningHeld(0,a))
   dialogue.busy=false;sampleRequest(3)
   assert(factCallbacks==0 and pairCallbacks==2 and not probe.error and not dialogue.busy)
   assert(probe.View(0,a).dialoguePercent==0 and probe.lastPlan.count==1 and probe.mode=='ACTIVE')
  """)
 def test_real_sample_one_receiver_rejection_does_not_confirm_pair(self):
  for field in ['Generation','FactsEpoch','FactsInput']:
   with self.subTest(rejected_field=field):
    l=self.real_sample_runtime();l.globals().badField=field;l.execute("""
     sampleRequest(1);meaningAction('CULTURE_MEANING_ADVANCE','c00');meaningAction('CULTURE_MEANING_ADVANCE','c10')
     local paired=probe.CollectionConfirmed;pairCallbacks=0
     probe.CollectionConfirmed=function(...)pairCallbacks=pairCallbacks+1;return paired(...)end
     local p=samplePacket(2,twoWorks());p[badField]=p[badField]+1;meaningRequest(0,p)
     assert(pairCallbacks==0 and probe.lastPlan.count==1 and probe.mode=='ACTIVE')
     assert(probe.View(0,a).dialoguePercent==nil and configured(a,'GOLD')==1 and gwa.IsMeaningHeld(0,a))
     assert(shared.GreatWorkFacts.ack==(badField=='FactsEpoch' and 1 or 2) and (dialogue.seq[0] or 0)>0) -- ACK is not acceptance.
     sampleRequest(3,twoWorks());assert(pairCallbacks==1 and not probe.error and probe.lastPlan.count==2)
     assert(probe.View(0,a).dialoguePercent==0)
    """)
 def test_real_sample_duplicate_sequence_does_not_reinterpret_changed_payload(self):
  l=self.real_sample_runtime();l.execute("""
   sampleRequest(1);meaningAction('CULTURE_MEANING_ADVANCE','c00');meaningAction('CULTURE_MEANING_ADVANCE','c10')
   local paired=probe.CollectionConfirmed;pairCallbacks=0
   probe.CollectionConfirmed=function(...)pairCallbacks=pairCallbacks+1;return paired(...)end
   local w=writes;sampleRequest(1,twoWorks())
   assert(pairCallbacks==0 and writes==w and probe.lastPlan.count==1)
   assert(shared.GreatWorkFacts.Summary(0,1).count==1 and dialogue.samples[0].seq==1)
   assert(probe.View(0,a).dialoguePercent==0 and not probe.error)
  """)
 def test_real_sample_dialogue_one_end_behind_cannot_reuse_processed_facts_ack(self):
  l=self.real_sample_runtime();l.execute("""
   sampleRequest(1);meaningAction('CULTURE_MEANING_ADVANCE','c00');meaningAction('CULTURE_MEANING_ADVANCE','c10')
   local paired=probe.CollectionConfirmed;pairCallbacks=0
   probe.CollectionConfirmed=function(...)pairCallbacks=pairCallbacks+1;return paired(...)end
   local previousTurn=turn;turn=turn+1;dialogue.seq[0]=0 -- Reproduce one interpreter lagging behind.
   sampleRequest(1,twoWorks())
   assert(shared.GreatWorkFacts.ack==1 and shared.GreatWorkFacts.Summary(0,1).availability=='KNOWN')
   assert(shared.GreatWorkFacts.Summary(0,1).count==1 and dialogue.samples[0].seq==1 and #dialogue.samples[0].cities[1]==2)
   assert(dialogue.received[0].stage=='ACCEPTED' and dialogue.samples[0].turn==turn)
   assert(dialogue.paired[0].turn==previousTurn and pairCallbacks==0 and probe.lastPlan.count==1)
   local v=probe.View(0,a);assert(v.dialoguePercent==nil and v.dialogueError:find('ME_DIALOGUE_SAMPLE_PAIR_PENDING'))
   local held,why=pcall(dialogue.HoldMeaningProbe,0,a,0)
   assert(not held and why:find('ME_DIALOGUE_SAMPLE_PAIR_PENDING') and gwa.IsMeaningHeld(0,a) and configured(a,'GOLD')==1)
   sampleRequest(2,twoWorks())
   assert(pairCallbacks==1 and dialogue.paired[0].turn==turn and dialogue.paired[0].seq==2)
   assert(probe.mode=='ACTIVE' and probe.lastPlan.count==2 and not probe.error and probe.View(0,a).dialoguePercent==0)
  """)
 def test_real_sample_next_turn_waits_for_current_pair_then_recovers_same_phase(self):
  l=self.real_sample_runtime();l.execute("""
   sampleRequest(1);meaningAction('CULTURE_MEANING_ADVANCE','c00');meaningAction('CULTURE_MEANING_ADVANCE','c10')
   turn=turn+1;fire('PlayerTurnActivated',0)
   assert(probe.mode=='ACTIVE' and probe.error and probe.View(0,a).dialoguePercent==nil)
   assert(gwa.IsMeaningHeld(0,a) and configured(a,'GOLD')==1)
   sampleRequest(2)
   assert(probe.mode=='ACTIVE' and not probe.error and probe.View(0,a).dialoguePercent==0)
   assert(dialogue.samples[0].turn==turn and configured(a,'GOLD')==1 and not old(a,'SCIENCE'))
  """)
 def test_real_sample_scaled_refresh_has_zero_writes_and_busy_probe_stays_unconfirmed(self):
  l=self.real_sample_runtime();l.execute("""
   sampleRequest(1);meaningAction('CULTURE_MEANING_ADVANCE','c00');meaningAction('CULTURE_MEANING_ADVANCE','c10')
   meaningAction('CULTURE_MEANING_ADVANCE','c11')
   local id=GameInfo.Buildings.BUILDING_SPC_B059_TEST100.Index
   assert(probe.mode=='SCALED' and probe.View(0,a).dialoguePercent==100 and a.present[id])
   local w=writes;local dialogueChanges=dialogue.changes;local meaningChanges=probe.changes
   sampleRequest(2)
   assert(writes==w and dialogue.changes==dialogueChanges and probe.changes==meaningChanges)
   assert(dialogue.paired[0].seq==2 and dialogue.last[0][1].sampleSeq==2 and probe.View(0,a).dialoguePercent==100)
   assert(a.present[id] and configured(a,'CULTURE')==1 and configured(a,'GOLD')==1)
   assert(not old(a,'SCIENCE') and old(b,'SCIENCE') and dialogue.last[0][2].sampleSeq==2)
   local paired=probe.CollectionConfirmed;confirmResults={}
   probe.CollectionConfirmed=function(...)
    local accepted=paired(...);confirmResults[#confirmResults+1]=accepted;return accepted
   end
   probe.busy=true;sampleRequest(3)
   assert(probe.busy and confirmResults[1]==false and dialogue.paired[0].seq==3)
   assert(probe.View(0,a).dialoguePercent==nil and writes==w and a.present[id])
   assert(configured(a,'CULTURE')==1 and gwa.IsMeaningHeld(0,a) and old(b,'SCIENCE'))
   probe.busy=false;sampleRequest(4)
   assert(confirmResults[2]==true and not probe.error and not probe.busy and not dialogue.busy and not gwa.busy)
   assert(dialogue.last[0][1].sampleSeq==4 and probe.View(0,a).dialoguePercent==100)
   assert(writes==w and dialogue.changes==dialogueChanges and probe.changes==meaningChanges)
   assert(probe.mode=='SCALED' and a.present[id] and configured(a,'CULTURE')==1 and old(b,'SCIENCE') and not old(a,'SCIENCE'))
  """)
 def test_dialogue_busy_cannot_confirm_cached_projection_or_clear_other_lock(self):
  for cached_meaning in [False,True]:
   with self.subTest(cached_meaning=cached_meaning):
    l=self.runtime();bind_actual_request(l);l.globals().include('UI/BoostGreatWorkRead');l.globals().cachedMeaning=cached_meaning;l.execute("""
     dialogue.last[0][1].meaning=cachedMeaning;dialogue.busy=true
     local w=writes;meaningRequest(0,{Action='CULTURE_MEANING_ADVANCE',CityID=1,Token='busy-c00'})
     assert(dialogue.busy and probe.mode=='BASELINE' and probe.error:find('ME_DIALOGUE_UPDATE_PENDING'))
     assert(shared.CultureMeaningView.error and configured(a,'GOLD')==0 and gwa.IsMeaningHeld(0,a))
     assert(shared.Snapshot:find('%[ADVANCE%]') and writes>=w and not old(a,'SCIENCE'))
     local before=writes;local text=SPCBoostGreatWorkRead.Meaning(P,a,shared.CultureMeaningView,true)
     assert(text:find('ME_UI_CONFIGURATION_PENDING') and not text:find('已记录') and writes==before)
     dialogue.busy=false;probe.Audit();assert(not probe.error and probe.View(0,a).dialoguePercent==0)
     probe.End(0,a);assert(probe.mode=='OFF' and not dialogue.meaningOverride and old(a,'SCIENCE'))
    """)
 def test_dialogue_audit_outer_exceptions_release_only_own_lock(self):
  failures=["local raw=Players[0].GetCities;Players[0].GetCities=function()error('NATIVE_GET_CITIES')end;restore=function()Players[0].GetCities=raw end",
   "local raw=Players[0].GetCities;Players[0].GetCities=function()return {Members=function()error('NATIVE_MEMBERS')end}end;restore=function()Players[0].GetCities=raw end",
   "local raw=Players[0].GetCities;Players[0].GetCities=function()local v=raw();v.FindID=function()error('NATIVE_FIND_ID')end;return v end;auditCity=1;restore=function()Players[0].GetCities=raw end",
   "local raw=P.Count;P.Count=function()error('NATIVE_COUNT')end;restore=function()P.Count=raw end"]
  for setup in failures:
   with self.subTest(failure=setup.split("error('")[1].split("'")[0]):
    l=self.runtime();l.execute(setup);l.execute("""
     local completed,why=dialogue.Audit(0,auditCity)
     assert(completed==false and why:find('AUDIT_FAILED') and not dialogue.busy)
     restore();assert(dialogue.Audit(0)==true and not dialogue.busy and not dialogue.last[0][1].error)
     dialogue.busy=true;completed,why=dialogue.Audit(0)
     assert(completed==false and why:find('BUSY') and dialogue.busy)
    """)
 def test_dialogue_init_exception_and_reentry_release_only_own_initializing_lock(self):
  l=self.runtime();l.execute("""
   dialogue.ready=false
   local raw=P.Count;P.Count=function()error('NATIVE_INIT_COUNT')end
   assert(not pcall(dialogue.Init) and not dialogue.initializing and not dialogue.ready)
   P.Count=raw;dialogue.Init();assert(dialogue.ready and not dialogue.initializing)
   dialogue.ready=false;P.Count=function()dialogue.Init()end
   local ok,why=pcall(dialogue.Init)
   assert(not ok and why:find('INIT_BUSY') and not dialogue.initializing and not dialogue.ready)
   P.Count=raw;dialogue.Init();assert(dialogue.ready and not dialogue.initializing)
   dialogue.ready=false;dialogue.initializing=true
   assert(not pcall(dialogue.Init) and dialogue.initializing and not dialogue.ready)
   dialogue.initializing=false;dialogue.Init();assert(dialogue.ready)
  """)
 def test_dialogue_target_missing_invalidates_cached_meaning_projection(self):
  l=self.runtime();l.execute("""
   probe.Advance(0,a);assert(probe.View(0,a).dialoguePercent==0)
   local raw=Players[0].GetCities
   Players[0].GetCities=function()local v=raw();v.FindID=function()return nil end;return v end
   local completed,why=dialogue.Audit(0,1)
   assert(completed==false and why:find('CITY_UNAVAILABLE') and not dialogue.busy)
   assert(not (dialogue.last[0] and dialogue.last[0][1]))
   local percent,err=dialogue.ReadMeaningProbe(0,a);assert(percent==nil and err)
   Players[0].GetCities=raw;assert(dialogue.Audit(0,1)==true and probe.View(0,a).dialoguePercent==0)
  """)
 def test_dialogue_native_member_iterator_preserves_state_and_control(self):
  l=self.real_sample_runtime();l.execute("""
   sampleRequest(1)
   local native={rows=cities}
   function native:FindID(id)for _,c in ipairs(self.rows)do if c.id==id then return c end end end
   function native:Members()
    local rows=self.rows
    return function(state,control)
     assert(state==rows and type(control)=='number','NATIVE_ITERATOR_STATE_LOST')
     local nextIndex=control+1;local c=state[nextIndex];if c then return nextIndex,c end
    end,rows,0
   end
   Players[0].GetCities=function()return native end
   assert(dialogue.Audit(0)==true and not dialogue.busy)
   assert(dialogue.last[0][1] and dialogue.last[0][2] and not dialogue.last[0][1].error and not dialogue.last[0][2].error)
   assert(dialogue.Audit(0,1)==true and not dialogue.busy)
   -- Continue through the complete actual request, including un-stubbed GWA.
   sampleRequest(2);local v=meaningAction('CULTURE_MEANING_ADVANCE','native-c00')
   assert(v.mode=='BASELINE' and v.dialoguePercent==0 and not v.error)
   sampleRequest(3);assert(not probe.error and probe.View(0,a).dialoguePercent==0)
   assert(not dialogue.busy and not gwa.busy and gwa.last[0][1].meaningHeld and not gwa.last[0][2].error)
   assert(gwa.IsMeaningHeld(0,a) and not old(a,'SCIENCE') and old(b,'SCIENCE'))
  """)
 def test_real_sample_gwa_outer_failures_release_own_lock_and_allow_recovery(self):
  failures=[
   "local raw=Players[0].GetCities;Players[0].GetCities=function()if gwa.busy then error('NATIVE_GWA_GET_CITIES')end;return raw()end;restore=function()Players[0].GetCities=raw end",
   "local raw=Players[0].GetCities;Players[0].GetCities=function()local c=raw();local members=c.Members;c.Members=function(...)local it,state,control=members(...);return function(s,k)if gwa.busy then error('NATIVE_GWA_ITERATOR')end;return it(s,k)end,state,control end;return c end;restore=function()Players[0].GetCities=raw end",
   "local raw=a.GetID;a.GetID=function(c)if gwa.busy then error('NATIVE_GWA_GET_ID')end;return raw(c)end;restore=function()a.GetID=raw end"]
  for setup in failures:
   with self.subTest(failure=setup.split("error('")[1].split("'")[0]):
    l=self.real_sample_runtime();l.execute(setup);l.execute("""
     sampleRequest(1)
     assert(not gwa.busy and gwa.errors[0]:find('GWA_AUDIT_FAILED') and not dialogue.busy)
     assert(shared.GreatWorkFacts.ack==1 and dialogue.samples[0].seq==1 and dialogue.received[0].stage=='ACCEPTED')
     local v=meaningAction('CULTURE_MEANING_ADVANCE','failure-c00')
     assert(v.mode=='BASELINE' and v.dialoguePercent==0 and not v.error and gwa.IsMeaningHeld(0,a))
     restore();sampleRequest(2)
     assert(not gwa.busy and not dialogue.busy and not gwa.errors[0])
     assert(gwa.last[0][1].meaningHeld and not gwa.last[0][2].error and old(b,'SCIENCE') and not old(a,'SCIENCE'))
     gwa.busy=true;sampleRequest(3);assert(gwa.busy and not dialogue.busy)
     gwa.busy=false;gwa.Audit(0);assert(not gwa.busy and not gwa.last[0][2].error)
    """)
 def test_meaning_describe_uses_short_error_codes_without_source_path_or_trace(self):
  l=self.runtime();l.execute("""
   begin();local v=probe.View(0,a)
   v.dialogueError='/Users/fixture/Mod/Dialogue.lua:123: ME_DIALOGUE_UPDATE_PENDING: AUDIT_FAILED'..string.char(10)..'stack traceback: details'
   v.error='/Users/fixture/Mod/CultureMeaningProbe.lua:61: ME_DIALOGUE_SAMPLE_PAIR_PENDING'..string.char(10)..'stack traceback: details'
   local w=writes;local text=probe.Describe(0,a,v)
   assert(text:find('ME_DIALOGUE_UPDATE_PENDING') and text:find('ME_DIALOGUE_SAMPLE_PAIR_PENDING'))
   for _,long in ipairs({'/Users/','Dialogue.lua','CultureMeaningProbe.lua','stack traceback','AUDIT_FAILED'})do assert(not text:find(long,1,true))end
   assert(writes==w and #text<1500)
  """)
 def test_synchronous_city_buildings_changed_four_phase_and_exit(self):
  l=self.runtime();l.execute("""
   local create=P.CreateBuilding;local remove=P.RemoveBuilding
   P.CreateBuilding=function(q,id)create(q,id);fire('CityBuildingsChanged',q.city.owner,q.city.id)end
   P.RemoveBuilding=function(b,id)remove(b,id);fire('CityBuildingsChanged',b.city.owner,b.city.id)end
   local other={};for id,v in pairs(b.present)do other[id]=v end
   local stages={'BASELINE','ACTIVE','SCALED','SCALED_BASELINE'}
   for i,mode in ipairs(stages)do
    probe.Advance(0,a,'sync:'..i)
    local v=probe.View(0,a);assert(probe.mode==mode and not probe.error and not v.dialogueError)
    assert(v.dialoguePercent==(i>=3 and 100 or 0))
    assert(configured(a,'CULTURE')==((i==2 or i==3) and 1 or 0))
    assert(not probe.busy and not probe.advancing and not probe.deferred and not dialogue.busy)
    local w=writes;fire('CityBuildingsChanged',0,1);assert(writes==w)
   end
   probe.Advance(0,a,'sync:end');assert(probe.mode=='OFF' and not dialogue.meaningOverride and configured(a,'CULTURE')==0 and old(a,'SCIENCE'))
   for id,v in pairs(b.present)do assert(other[id]==v)end;for id,v in pairs(other)do assert(b.present[id]==v)end
   assert(not probe.busy and not probe.advancing and not probe.deferred and not dialogue.busy)
  """)
 def test_busy_hold_keeps_established_holder_and_projection(self):
  l=self.runtime();l.execute("""
   begin();local h=dialogue.meaningOverride;local p=dialogue.last[0][1];local w=writes
   dialogue.busy=true;local ok,why=pcall(dialogue.HoldMeaningProbe,0,a,100)
   assert(not ok and why:find('ME_DIALOGUE_UPDATE_PENDING'))
   assert(dialogue.busy and dialogue.meaningOverride==h and h.percent==0 and dialogue.last[0][1]==p and writes==w)
   dialogue.busy=false;assert(probe.View(0,a).dialoguePercent==0 and probe.mode=='ACTIVE')
  """)
 def test_transition_failure_keeps_intent_and_reveals_partial_write(self):
  for after_write in (False,True):
   with self.subTest(after_write=after_write):
    l=self.runtime();l.globals().afterWrite=after_write;l.execute("""
     begin();local h=dialogue.meaningOverride;local id=GameInfo.Buildings.BUILDING_SPC_B059_TEST100.Index
     local raw=P.CreateBuilding
     P.CreateBuilding=function(q,i)
      if i==id then if afterWrite then raw(q,i);error('NATIVE_AFTER_WRITE')else return end end
      return raw(q,i)
     end
     assert(not pcall(probe.Advance,0,a,'failed'))
     assert(probe.mode=='ACTIVE' and dialogue.meaningOverride==h and h.percent==0 and probe.error)
     assert(not probe.busy and not probe.advancing and not dialogue.busy)
     local v=probe.View(0,a);assert(v.dialoguePercent==nil and v.dialogueError and gwa.IsMeaningHeld(0,a))
     assert((a.present[id]==true)==afterWrite and configured(a,'CULTURE')==1)
     P.CreateBuilding=raw;probe.Advance(0,a,'finish');assert(probe.mode=='OFF' and not dialogue.meaningOverride and not a.present[id] and old(a,'SCIENCE'))
    """)
 def test_meaning_failure_after_successful_dialogue_restores_prior_intent(self):
  l=self.runtime();l.execute("""
   begin();local id=GameInfo.Buildings.BUILDING_SPC_MEANING_PROBE_CULTURE_0.Index
   a.present[id]=nil -- Native loss, observed by the next exact reconciliation.
   local raw=P.CreateBuilding
   P.CreateBuilding=function(q,i)if i~=id then return raw(q,i)end end
   assert(not pcall(probe.Advance,0,a,'failed-meaning'))
   assert(probe.mode=='ACTIVE' and dialogue.meaningOverride.percent==0 and probe.error)
   assert(a.present[GameInfo.Buildings.BUILDING_SPC_B059_TEST100.Index])
   local v=probe.View(0,a);assert(v.dialoguePercent==nil and v.dialogueError and gwa.IsMeaningHeld(0,a))
   assert(not probe.busy and not probe.advancing and not dialogue.busy)
   P.CreateBuilding=raw;probe.Advance(0,a,'finish')
   assert(probe.mode=='OFF' and not dialogue.meaningOverride and configured(a,'CULTURE')==0 and old(a,'SCIENCE'))
   assert(not a.present[GameInfo.Buildings.BUILDING_SPC_B059_TEST100.Index])
  """)
 def test_real_effective_facts_gate_does_not_replay_cached_active(self):
  for ceiling in (3,None):
   with self.subTest(ceiling=ceiling):
    l=self.runtime();l.globals().governorCeiling=ceiling;l.globals().include('EffectiveFacts');l.execute("""
     shared.CityFlowProbe={SupportFacts=function(pid,c)return {owner=pid,cityID=c.id,token=c.token,specialization='CULTURE',potential=1,first={districtID=c.ds[2].id,type='DISTRICT_THEATER'}}end}
     shared.CityProgressionStore.Owns=function()return true end
     shared.CityProgressionStore.Investment=function(pid,c)return {schema=1,revision=4,
      anchor={owner=pid,cityID=c.id,token=c.token,first={districtID=c.ds[2].id,type='DISTRICT_THEATER'},specialization='CULTURE'},
      investments={one='u1',two='u2',three='u3'}}end
     P.GovernorGate=function(c)return 0,c.id,c.ceiling and 'KNOWN' or 'UNKNOWN',c.ceiling end
     a.ceiling=4;b.ceiling=4;SPCEffectiveFacts.Start(P,shared)
     begin();assert(probe.lastPlan.active==4 and probe.View(0,a).currentPotential==4)
     local h=dialogue.meaningOverride;local w=writes;a.ceiling=governorCeiling
     local ok=pcall(dialogue.HoldMeaningProbe,0,a,0);assert(not ok and dialogue.meaningOverride==h and writes==w)
     local v=probe.View(0,a);assert(v.dialoguePercent==nil and v.dialogueError and probe.lastPlan.active==4)
     if governorCeiling then assert(v.currentActive==3 and v.currentActiveStatus=='KNOWN' and v.dialogueError:find('ME_DIALOGUE_ACTIVE_REQUIRED'))
     else assert(v.currentActive==nil and v.currentActiveStatus=='UNKNOWN_GOVERNOR' and v.dialogueError:find('ME_DIALOGUE_ACTIVE_UNKNOWN'))end
     a.ceiling=4;probe.End(0,a);assert(probe.mode=='OFF')
    """)
 def ui_aux_runtime(self):
  l=self.runtime();l.globals().include('UI/BoostGreatWorkRead');l.execute("""
   local get=a.GetBuildings
   a.GetBuildings=function(c)local b=get(c)
    b.GetNumGreatWorkSlots=function(_,id)return id==GameInfo.Buildings.BUILDING_AMPHITHEATER.Index and 1 or 0 end
    b.GetGreatWorkInSlot=function()return 100 end;b.GetGreatWorkTypeFromIndex=function()return 'GREATWORK_BHASA_1'end
    b.IsBuildingThemedCorrectly=function()return false end
    b.GetBuildingYieldFromGreatWorks=function(_,y,id)local typ=GameInfo.Yields[y].YieldType:gsub('YIELD_','');return typ=='CULTURE' and 2 or configured(c,typ)end
    return b
   end
   a.GetYield=function(c)return 40+(cityStale and 0 or configured(c,'CULTURE'))end
   probe.Advance(0,a);SPCBoostGreatWorkRead.Meaning(P,a,probe.View(0,a),true)
   probe.Advance(0,a)
  """)
  return l
 def test_city_aux_read_distinguishes_zero_work_delta_and_refresh(self):
  l=self.ui_aux_runtime();l.execute("""
   cityStale=true;local w=writes;local t=SPCBoostGreatWorkRead.Meaning(P,a,probe.View(0,a),false)
   assert(t:find('作品文化 Δ%+0.00') and t:find('对应整城文化 Δ%+0.00'))
   cityStale=false;t=SPCBoostGreatWorkRead.Meaning(P,a,probe.View(0,a),false)
   assert(t:find('作品文化 Δ%+0.00') and t:find('对应整城文化 Δ%+1.00') and writes==w)
   assert(t:find('不代替作品／结算门禁') and probe.mode=='ACTIVE')
  """)
 def test_unavailable_city_aux_does_not_erase_work_readings(self):
  l=self.ui_aux_runtime();l.execute("""
   a.GetYield=nil;local w=writes;local t=SPCBoostGreatWorkRead.Meaning(P,a,probe.View(0,a),false)
   assert(t:find('整城文化未确认') and t:find('原生作品收益') and t:find('作品文化 Δ%+0.00'))
   assert(not t:find('对应整城文化 Δ') and writes==w)
   a.GetYield=function()return 0/0 end;t=SPCBoostGreatWorkRead.Meaning(P,a,probe.View(0,a),false);assert(t:find('整城文化未确认'))
   a.GetYield=function()return 0 end;t=SPCBoostGreatWorkRead.Meaning(P,a,probe.View(0,a),false);assert(t:find('整城文化 0.00'))
  """)
 def test_aux_comparison_invalidates_turn_or_population_change(self):
  for change in ('population','turn'):
   with self.subTest(change=change):
    l=self.ui_aux_runtime();l.globals().changed=change;l.execute("""
     local t=SPCBoostGreatWorkRead.Meaning(P,a,probe.View(0,a),false);assert(t:find('作品文化 Δ%+0.00'))
     if changed=='population' then a.GetPopulation=function()return 8 end
     else turn=turn+1;collection();probe.Audit()end
     local w=writes;t=SPCBoostGreatWorkRead.Meaning(P,a,probe.View(0,a),false)
     assert(t:find('四态对照无效') and not t:find('作品文化 Δ') and writes==w)
    """)

 # Candidate definitions and UI readings are evidence for the technical probe;
 # mocked native getters never establish engine stacking or settlement PASS.
 def culture3_runtime(self):
  l=self.runtime();l.execute("""
   local gov=district(a,8,'DISTRICT_GOVERNMENT')
   for _,name in ipairs({'BUILDING_GOV_TALL','BUILDING_GOV_CITYSTATES','BUILDING_GOV_MILITARY'})do building(a,name,gov)end
   a.ds[7].pillaged=true -- D6 government contributes3; no second Culture domain.
   building(a,'BUILDING_UNIVERSITY',a.ds[6]);building(a,'BUILDING_MARKET',a.ds[3]);svc.MarkDirty()
   function exactMeaning(c)
    local out={};for _,name in ipairs(SPCCultureMeaningModel.Owned)do if c.present[GameInfo.Buildings[name].Index]then out[name]=true end end;return out
   end
  """)
  return l
 def test_candidate_model_has_exact_owned_parts_and_strict_culture3_bound(self):
  l=self.runtime();l.execute("""
   local m=SPCCultureMeaningModel;local seen={}
   assert(#m.Owned==16 and table.concat(m.Variants,',')=='SPLIT,SINGLE3,SINGLE3_SCALE100')
   for _,name in ipairs(m.Owned)do assert(not seen[name]);seen[name]=true;assert(probe.IsOwnedCarrier(name))end
   assert(not probe.IsOwnedCarrier('BUILDING_LIBRARY') and not probe.IsOwnedCarrier('BUILDING_SPC_MEANING_PROBE_CULTURE_4'))
   assert(table.concat(m.Parts('CULTURE',3),',')=='BUILDING_SPC_MEANING_PROBE_CULTURE_0,BUILDING_SPC_MEANING_PROBE_CULTURE_1')
   assert(table.concat(m.Parts('SCIENCE',1,'SPLIT'),',')==table.concat(m.Parts('SCIENCE',1),','))
   for _,variant in ipairs({'SINGLE3','SINGLE3_SCALE100'})do
    local part=m.VariantParts[variant];assert(m.Parts('CULTURE',3,variant)[1]==part.name and #m.Parts('CULTURE',3,variant)==1)
    assert(part.amount==3 and (variant~='SINGLE3_SCALE100' or part.scalingFactor==100))
    for _,amount in ipairs({0,1,2,3.5,4})do local ok,why=pcall(m.Parts,'CULTURE',amount,variant);assert(not ok and tostring(why):find('ME_ENCODING_'))end
    local ok,why=pcall(m.Parts,'SCIENCE',3,variant);assert(not ok and tostring(why):find('ME_ENCODING_'))
   end
   local ok,why=pcall(m.Parts,'CULTURE',3,'UNKNOWN');assert(not ok and tostring(why):find('ME_ENCODING_'))
  """)
 def test_candidate_config_cycles_only_off_duplicate_token_and_two_city_isolation(self):
  l=self.culture3_runtime();l.execute("""
   assert(probe.View(0,a).variant=='SPLIT');local w=writes
   probe.CycleVariant(0,a,'config:one');assert(probe.View(0,a).variant=='SINGLE3' and writes==w)
   probe.CycleVariant(0,a,'config:one');assert(probe.View(0,a).variant=='SINGLE3' and writes==w)
   assert(not pcall(probe.Advance,0,a,'config:one'));assert(probe.mode=='OFF' and writes==w)
   assert(not pcall(probe.CycleVariant,0,b,'config:one'));assert(probe.View(0,a).variant=='SINGLE3')
   probe.CycleVariant(0,a,'config:two');assert(probe.View(0,a).variant=='SINGLE3_SCALE100' and writes==w)
   probe.CycleVariant(0,a,'config:three');assert(probe.View(0,a).variant=='SPLIT' and writes==w)
  """)
  for phase,mode in enumerate(('BASELINE','ACTIVE','SCALED','SCALED_BASELINE'),1):
   with self.subTest(phase=mode):
    l=self.culture3_runtime();l.globals().phaseCount=phase;l.globals().expectedMode=mode;l.execute("""
     probe.CycleVariant(0,a,'single');for i=1,phaseCount do probe.Advance(0,a,'phase:'..i)end
     assert(probe.mode==expectedMode);local before=writes;local n=configured(a,'CULTURE')
     local ok,why=pcall(probe.CycleVariant,0,a,'blocked')
     assert(not ok and tostring(why):find('ME_VARIANT_REQUIRES_OFF') and probe.error and writes==before)
     assert(probe.View(0,a).variant=='SINGLE3' and probe.mode==expectedMode and configured(a,'CULTURE')==n)
     assert(old(b,'SCIENCE') and configured(b,'CULTURE')==0)
     probe.End(0,a);assert(probe.mode=='OFF' and configured(a,'CULTURE')==0 and old(a,'SCIENCE'))
    """)
 def test_all_candidate_four_phases_are_mutually_exclusive_same_input_zero_write(self):
  for variant in ('SPLIT','SINGLE3','SINGLE3_SCALE100'):
   with self.subTest(variant=variant):
    l=self.culture3_runtime();l.globals().wantedVariant=variant;l.execute("""
     for i=1,2 do if probe.View(0,a).variant~=wantedVariant then probe.CycleVariant(0,a,'pick:'..i)end end
     assert(probe.View(0,a).variant==wantedVariant)
     probe.Advance(0,a,'c00');assert(probe.mode=='BASELINE' and configured(a,'CULTURE')==0)
     probe.Advance(0,a,'c10');local v=probe.View(0,a)
     assert(v.culture==3 and v.totalCulture==3 and v.configuredCulture==3 and configured(a,'CULTURE')==3)
     assert(v.science==1 and v.gold==4 and configured(a,'SCIENCE')==1 and configured(a,'GOLD')==4)
     local selected={};for _,name in ipairs(SPCCultureMeaningModel.Parts('CULTURE',3,wantedVariant))do selected[name]=true end
     for _,name in ipairs(SPCCultureMeaningModel.Owned)do if name:find('_CULTURE_')then assert((exactMeaning(a)[name]==true)==(selected[name]==true))end end
     local w=writes;probe.Audit();probe.Audit();probe.Advance(0,a,'c10');assert(writes==w)
     probe.Advance(0,a,'c11');assert(probe.mode=='SCALED' and configured(a,'CULTURE')==3 and probe.View(0,a).dialoguePercent==100)
     assert(old(b,'SCIENCE') and configured(b,'CULTURE')==0 and probe.View(0,b).mode=='OFF')
     probe.Advance(0,a,'c01');assert(probe.mode=='SCALED_BASELINE' and configured(a,'CULTURE')==0 and next(exactMeaning(a))==nil)
     probe.Advance(0,a,'off');assert(probe.mode=='OFF' and next(exactMeaning(a))==nil and old(a,'SCIENCE') and old(b,'SCIENCE'))
    """)
 def test_candidate_amount_guard_rejects_before_holding_any_old_writer(self):
  l=self.runtime();l.execute("""
   probe.CycleVariant(0,a,'single');local w=writes
   local ok,why=pcall(probe.Advance,0,a,'invalid-amount')
   assert(not ok and tostring(why):find('ME_ENCODING_') and probe.mode=='OFF')
   assert(configured(a,'CULTURE')==0 and configured(a,'GOLD')==0 and not gwa.IsMeaningHeld(0,a) and dialogue.meaningOverride==nil)
   assert(writes==w and old(a,'SCIENCE') and old(b,'SCIENCE'))
   probe.CycleVariant(0,a,'next');assert(probe.View(0,a).variant=='SINGLE3_SCALE100' and not probe.error)
  """)
 def test_candidate_create_and_remove_failure_never_releases_old_writers_early(self):
  for operation in ('create','remove'):
   with self.subTest(operation=operation):
    l=self.culture3_runtime();l.globals().failureOperation=operation;l.execute("""
     probe.CycleVariant(0,a,'single');probe.Advance(0,a,'baseline')
     local part=SPCCultureMeaningModel.VariantParts.SINGLE3.name;local id=GameInfo.Buildings[part].Index
     if failureOperation=='create' then
      failCreate=true;assert(not pcall(probe.Advance,0,a,'enable'));assert(probe.mode=='BASELINE' and configured(a,'CULTURE')==0)
      failCreate=false
     else
      probe.Advance(0,a,'enable');failRemove=id;assert(not pcall(probe.End,0,a))
      assert(probe.stopping and configured(a,'CULTURE')==3 and not old(a,'SCIENCE'));failRemove=nil
     end
     assert(gwa.IsMeaningHeld(0,a) and dialogue.IsMeaningProbeHeld(0,a,0) and old(b,'SCIENCE'))
     probe.End(0,a);assert(probe.mode=='OFF' and configured(a,'CULTURE')==0 and next(exactMeaning(a))==nil and old(a,'SCIENCE'))
    """)
 def test_load_removes_all_16_owned_parts_even_foreign_and_resets_split(self):
  l=self.culture3_runtime();l.execute("""
   probe.CycleVariant(0,a,'single');probe.CycleVariant(0,a,'scale100')
   for _,name in ipairs(SPCCultureMeaningModel.Owned)do building(a,name,a.ds[1]);building(b,name,b.ds[1])end
   a.owner=3;fire('LoadScreenClose')
   assert(probe.mode=='OFF' and probe.View(0,b).variant=='SPLIT' and next(exactMeaning(a))==nil and next(exactMeaning(b))==nil)
   assert(a.present[GameInfo.Buildings.BUILDING_LIBRARY.Index] and b.present[GameInfo.Buildings.BUILDING_LIBRARY.Index])
   assert(a.token=='persistent:1' and b.token=='persistent:2');a.owner=0;fire('PlayerTurnActivated',0)
   assert(probe.mode=='OFF' and next(exactMeaning(a))==nil and probe.View(0,a).variant=='SPLIT')
  """)
 def test_actual_request_candidate_config_is_read_once_and_error_preserves_active(self):
  l=self.culture3_runtime();bind_actual_request(l);l.execute("""
   local raw=probe.View;local reads=0;probe.View=function(...)reads=reads+1;return raw(...)end
   local w=writes;meaningRequest(0,{Action='CULTURE_MEANING_CONFIG',CityID=1,Token='config'})
   assert(shared.LastToken=='config' and shared.CultureMeaningView.token=='config' and shared.CultureMeaningView.variant=='SINGLE3' and writes==w and reads==1)
   meaningRequest(0,{Action='CULTURE_MEANING_CONFIG',CityID=1,Token='config'})
   assert(shared.CultureMeaningView.variant=='SINGLE3' and writes==w and reads==2)
   probe.Advance(0,a,'baseline');probe.Advance(0,a,'enable');local before=writes
   meaningRequest(0,{Action='CULTURE_MEANING_CONFIG',CityID=1,Token='blocked-config'})
   assert(shared.LastToken=='blocked-config' and shared.CultureMeaningView.token=='blocked-config' and shared.CultureMeaningView.error)
   assert(probe.mode=='ACTIVE' and shared.CultureMeaningView.variant=='SINGLE3' and configured(a,'CULTURE')==3 and writes==before)
  """)
 def candidate_ui_runtime(self,themed=True,count=2):
  l=self.culture3_runtime();l.globals().mockThemed=themed;l.globals().mockCount=count;l.globals().include('UI/BoostGreatWorkRead');l.execute("""
   a.workCount=mockCount;probe.CycleVariant(0,a,'single')
   local get=a.GetBuildings
   a.GetBuildings=function(c)local b=get(c)
    b.GetNumGreatWorkSlots=function(_,id)return id==GameInfo.Buildings.BUILDING_AMPHITHEATER.Index and mockCount or 0 end
    b.GetGreatWorkInSlot=function(_,id,s)return 100+s end
    b.GetGreatWorkTypeFromIndex=function()return 'GREATWORK_BHASA_1'end
    b.IsBuildingThemedCorrectly=function()if mockThemeThrow then error('THEME_GETTER_FAILED')end;return mockThemed end
    b.GetBuildingYieldFromGreatWorks=function(_,y,id)
     local typ=GameInfo.Yields[y].YieldType:gsub('YIELD_','');local amount=configured(c,typ)
     if typ=='CULTURE' then
      local dialogueFactor=probe.View(0,c).dialoguePercent==100 and 2 or 1
      local themeFactor=mockThemed==true and 2 or 1
      return (2*dialogueFactor*themeFactor+amount*(mockAmplify and themeFactor or 1))*mockCount
     end
     return amount*mockCount
    end
    return b
   end
  """)
  return l
 def test_known_themed_reader_reports_flat_three_yield_deltas_and_building_counts(self):
  l=self.candidate_ui_runtime();l.execute("""
   for i=1,4 do probe.Advance(0,a,'phase:'..i);text=SPCBoostGreatWorkRead.Meaning(P,a,probe.View(0,a),true)
    assert(not text:find('未确认：') and text:find('主题化1座／2件') and text:find('2件／已主题化'))
   end
   assert(text:find('追加预期保持固定，不乘主题倍率'))
   assert(text:find('关闭旧对话：作品文化 Δ%+6.00；预期 %+6'))
   assert(text:find('旧对话100%%：作品文化 Δ%+6.00'))
   assert(text:find('关闭旧对话：作品科研 Δ%+2.00；预期 %+2') and text:find('旧对话100%%：作品科研 Δ%+2.00；预期 %+2'))
   assert(text:find('关闭旧对话：作品金币 Δ%+8.00；预期 %+8') and text:find('旧对话100%%：作品金币 Δ%+8.00；预期 %+8'))
   local w=writes;SPCBoostGreatWorkRead.Meaning(P,a,probe.View(0,a),false);assert(writes==w)
   assert(not text:find('USER_GAME_TEST_PASS') and not text:find('LOCAL_SIMULATION_PASS'))
  """)
 def test_mock_theme_amplification_is_visible_while_flat_expectation_stays_unchanged(self):
  l=self.candidate_ui_runtime();l.execute("""
   mockAmplify=true
   for i=1,4 do probe.Advance(0,a,'phase:'..i);text=SPCBoostGreatWorkRead.Meaning(P,a,probe.View(0,a),true)end
   assert(text:find('关闭旧对话：作品文化 Δ%+12.00；预期 %+6'))
   assert(text:find('旧对话100%%：作品文化 Δ%+12.00'))
   assert(probe.View(0,a).totalCulture==6 and probe.View(0,a).culture==3)
   assert(not text:find('USER_GAME_TEST_PASS') and text:find('不自动判定结算PASS'))
  """)
 def test_unknown_theme_cannot_record_or_recreate_successful_baseline(self):
  for invalid in ('nil','1',"'UNKNOWN'",'throw'):
   with self.subTest(theme=invalid):
    l=self.candidate_ui_runtime();l.globals().invalidTheme=invalid;l.execute("""
     probe.Advance(0,a,'baseline')
     if invalidTheme=='throw' then
      mockThemeThrow=true
     elseif invalidTheme=='nil' then mockThemed=nil
     elseif invalidTheme=='1' then mockThemed=1 else mockThemed='UNKNOWN'end
     local w=writes;local text=SPCBoostGreatWorkRead.Meaning(P,a,probe.View(0,a),true)
     assert(text:find('ME_UI_THEME_UNKNOWN') and text:find('不记录成功基线') and not text:find('本阶段已记录') and writes==w)
     mockThemeThrow=false;mockThemed=true;text=SPCBoostGreatWorkRead.Meaning(P,a,probe.View(0,a),false)
     assert(text:find('四态对照无效') and not text:find('本阶段已记录') and writes==w)
    """)
 def test_current_theme_and_variant_change_invalidate_prior_four_phase_readings(self):
  for change in ('theme','variant'):
   with self.subTest(change=change):
    l=self.candidate_ui_runtime();l.globals().readerChange=change;l.execute("""
     probe.Advance(0,a,'baseline');local text=SPCBoostGreatWorkRead.Meaning(P,a,probe.View(0,a),true);assert(text:find('已记录'))
     probe.Advance(0,a,'active');local v=probe.View(0,a);local w=writes
     if readerChange=='theme' then mockThemed=false else v.variant='SINGLE3_SCALE100'end
     text=SPCBoostGreatWorkRead.Meaning(P,a,v,false)
     assert(text:find('四态对照无效') and not text:find('作品文化 Δ') and writes==w)
     mockThemed=true;text=SPCBoostGreatWorkRead.Meaning(P,a,probe.View(0,a),false)
     assert(text:find('四态对照无效') and not text:find('作品文化 Δ') and writes==w)
    """)
 def test_reader_current_count_mismatch_and_nonfinite_native_yield_are_unknown(self):
  for change in ('count','yield'):
   with self.subTest(change=change):
    l=self.candidate_ui_runtime();l.globals().readerChange=change;l.execute("""
     probe.Advance(0,a,'baseline');SPCBoostGreatWorkRead.Meaning(P,a,probe.View(0,a),true)
     local get=a.GetBuildings
     a.GetBuildings=function(c)local b=get(c)
      if readerChange=='count' then b.GetNumGreatWorkSlots=function(_,id)return id==GameInfo.Buildings.BUILDING_AMPHITHEATER.Index and 1 or 0 end
      else b.GetBuildingYieldFromGreatWorks=function()return math.huge end end
      return b
     end
     local w=writes;local text=SPCBoostGreatWorkRead.Meaning(P,a,probe.View(0,a),false)
     assert(text:find(readerChange=='count' and 'ME_UI_WORK_COUNT_MISMATCH' or 'ME_UI_NATIVE_YIELD_UNKNOWN'))
     assert(text:find('不记录成功基线') and not text:find('本阶段已记录') and writes==w)
    """)
 def test_per_building_diagnostic_is_bounded_but_keeps_all_five_native_rows(self):
  l=self.culture3_runtime();l.globals().include('UI/BoostGreatWorkRead');l.execute("""
   a.workCount=5;local supported={};local count=0
   for _,name in ipairs({'BUILDING_AMPHITHEATER','BUILDING_MUSEUM_ART','BUILDING_MUSEUM_ARTIFACT','BUILDING_BROADCAST_CENTER','BUILDING_PALACE'})do
    building(a,name,a.ds[2]);supported[GameInfo.Buildings[name].Index]=true;count=count+1
   end
   local get=a.GetBuildings
   a.GetBuildings=function(c)local b=get(c)
    b.GetNumGreatWorkSlots=function(_,id)return supported[id] and 1 or 0 end
    b.GetGreatWorkInSlot=function(_,id)return id+100 end
    b.GetGreatWorkTypeFromIndex=function()return 'GREATWORK_BHASA_1'end
    b.IsBuildingThemedCorrectly=function()return true end
    b.GetBuildingYieldFromGreatWorks=function(_,y,id)return GameInfo.Yields[y].YieldType=='YIELD_CULTURE' and 2 or 0 end
    return b
   end
   probe.Advance(0,a,'baseline');local w=writes;local text=SPCBoostGreatWorkRead.Meaning(P,a,probe.View(0,a),true)
   assert(text:find('主题化5座／5件') and text:find('文化 10.00'))
   assert(text:find('另有1座馆藏建筑；合计已包含，明细仅显示前4座'))
   local rows=0;for _ in text:gmatch('1件／已主题化')do rows=rows+1 end;assert(rows==4 and writes==w)
  """)

 def test_candidate_read_rejects_mixed_or_wrong_carriers_and_reports_damaged_candidate(self):
  for kind in ('split','wrong','overlap','damaged','unknown'):
   with self.subTest(kind=kind):
    l=self.culture3_runtime();l.globals().readKind=kind;l.execute("""
     probe.CycleVariant(0,a,'single');probe.Advance(0,a,'baseline');probe.Advance(0,a,'active')
     local m=SPCCultureMeaningModel;local single=GameInfo.Buildings[m.VariantParts.SINGLE3.name].Index
     if readKind=='split' then building(a,'BUILDING_SPC_MEANING_PROBE_CULTURE_0',a.ds[1])
     elseif readKind=='wrong' then a.present[single]=nil;building(a,m.VariantParts.SINGLE3_SCALE100.name,a.ds[1])
     elseif readKind=='overlap' then building(a,m.VariantParts.SINGLE3_SCALE100.name,a.ds[1])
     elseif readKind=='damaged' then a.pillaged[single]=true
     else failHas=single end
     local w=writes;local v=probe.View(0,a);assert(writes==w)
     if readKind=='damaged' then
      assert(v.configuredCulture==0 and v.culture==3 and not v.configurationError)
     else
      assert(v.configuredCulture==nil and v.configuredScience==nil and v.configurationError)
      assert(v.configurationError:find(readKind=='unknown' and 'ME_CARRIER_UNKNOWN' or 'ME_CONFIG_VARIANT_'))
     end
     failHas=nil;probe.Audit();v=probe.View(0,a)
     assert(v.configuredCulture==3 and not v.configurationError and configured(a,'CULTURE')==3)
     assert(not a.present[GameInfo.Buildings[m.VariantParts.SINGLE3_SCALE100.name].Index] and not a.present[GameInfo.Buildings.BUILDING_SPC_MEANING_PROBE_CULTURE_0.Index])
    """)

 def test_recorded_baseline_is_released_on_unknown_theme_before_same_value_recovers(self):
  for invalid in ('nil','throw'):
   with self.subTest(theme=invalid):
    l=self.candidate_ui_runtime();l.globals().invalidTheme=invalid;l.execute("""
     probe.Advance(0,a,'baseline');local text=SPCBoostGreatWorkRead.Meaning(P,a,probe.View(0,a),true)
     assert(text:find('本阶段已记录') and text:find('主题化1座／2件'))
     local w=writes
     if invalidTheme=='throw' then mockThemeThrow=true else mockThemed=nil end
     text=SPCBoostGreatWorkRead.Meaning(P,a,probe.View(0,a),false)
     assert(text:find('ME_UI_THEME_UNKNOWN') and text:find('不记录成功基线') and writes==w)
     mockThemeThrow=false;mockThemed=true
     text=SPCBoostGreatWorkRead.Meaning(P,a,probe.View(0,a),false)
     assert(text:find('四态对照无效') and not text:find('本阶段已记录') and not text:find('作品文化 Δ') and writes==w)
     probe.Advance(0,a,'active');text=SPCBoostGreatWorkRead.Meaning(P,a,probe.View(0,a),false)
     assert(text:find('四态对照无效') and not text:find('作品文化 Δ'))
    """)
 def test_installed_single3_candidates_hold_on_unknown_and_exit_on_confirmed_loss_only(self):
  for variant in ('SINGLE3','SINGLE3_SCALE100'):
   with self.subTest(variant=variant):
    l=self.culture3_runtime();l.globals().wantedVariant=variant;l.execute("""
     for i=1,2 do if probe.View(0,a).variant~=wantedVariant then probe.CycleVariant(0,a,'pick:'..i)end end
     probe.Advance(0,a,'baseline');probe.Advance(0,a,'active')
     local candidate=SPCCultureMeaningModel.VariantParts[wantedVariant].name
     assert(a.present[GameInfo.Buildings[candidate].Index] and configured(a,'CULTURE')==3)
     local w=writes;a.worksUnknown=true;probe.Audit()
     assert(probe.error:find('ME_WORKS_UNKNOWN') and configured(a,'CULTURE')==3 and writes==w)
     assert(gwa.IsMeaningHeld(0,a) and dialogue.IsMeaningProbeHeld(0,a,0))
     a.owner=3;local loss={confirmed=false,targetID=a.id,origin={owner=0}}
     assert(not pcall(exits.CultureMeaningProbe,a,loss) and configured(a,'CULTURE')==3 and writes==w)
     loss.confirmed=true;exits.CultureMeaningProbe(a,loss)
     assert(probe.mode=='OFF' and next(exactMeaning(a))==nil and configured(a,'CULTURE')==0)
     assert(dialogue.meaningOverride==nil and old(b,'SCIENCE') and next(exactMeaning(b))==nil)
     assert(a.present[GameInfo.Buildings.BUILDING_LIBRARY.Index] and a.token=='persistent:1')
     local after=writes;exits.CultureMeaningProbe(a,loss);assert(writes==after)
     a.owner=0;a.worksUnknown=false;fire('GovernorChanged',0)
     assert(probe.mode=='OFF' and next(exactMeaning(a))==nil and probe.View(0,a).variant==wantedVariant)
    """)

 def test_actual_request_ends_c10_directly_without_percent_and_keeps_read_config_keys(self):
  l=self.culture3_runtime();bind_actual_request(l);l.execute("""
   local held=dialogue.HoldMeaningProbe;local percent100=0
   dialogue.HoldMeaningProbe=function(pid,c,percent)if percent==100 then percent100=percent100+1 end;return held(pid,c,percent)end
   local function request(action,token)
    meaningRequest(0,{Action=action,CityID=1,Token=token})
    assert(shared.LastToken==token and shared.CultureMeaningView.token==token)
    return shared.CultureMeaningView
   end
   request('CULTURE_MEANING_CONFIG','single');request('CULTURE_MEANING_ADVANCE','baseline');request('CULTURE_MEANING_ADVANCE','active')
   assert(probe.mode=='ACTIVE' and configured(a,'CULTURE')==3 and probe.View(0,a).dialoguePercent==0 and percent100==0)
   local w=writes;local prior=probe.lastAction;request('CULTURE_MEANING_READ','readonly')
   assert(writes==w and probe.mode=='ACTIVE' and probe.lastAction==prior)
   local v=request('CULTURE_MEANING_CONFIG','blocked-config')
   assert(v.error:find('ME_VARIANT_REQUIRES_OFF') and probe.mode=='ACTIVE' and v.variant=='SINGLE3' and writes==w)
   local remove,create=P.RemoveBuilding,P.CreateBuilding;local otherWrites=0
   P.RemoveBuilding=function(bld,id)if bld.city==b then otherWrites=otherWrites+1 end;return remove(bld,id)end
   P.CreateBuilding=function(queue,id)if queue.city==b then otherWrites=otherWrites+1 end;return create(queue,id)end
   v=request('CULTURE_MEANING_END','direct-end')
   assert(v.mode=='OFF' and not v.error and configured(a,'CULTURE')==0 and next(exactMeaning(a))==nil)
   assert(percent100==0 and otherWrites==0 and old(a,'SCIENCE') and old(b,'SCIENCE') and next(exactMeaning(b))==nil)
   assert(not a.present[GameInfo.Buildings.BUILDING_SPC_B059_TEST100.Index] and dialogue.meaningOverride==nil)
   w=writes;request('CULTURE_MEANING_END','direct-end');assert(writes==w and probe.mode=='OFF')
   request('CULTURE_MEANING_END','off-noop');assert(writes==w and probe.lastAction.kind=='END')
   request('CULTURE_MEANING_END','off-noop');assert(writes==w)
   assert(not pcall(probe.Advance,0,a,'off-noop') and not pcall(probe.CycleVariant,0,a,'off-noop') and not pcall(probe.End,0,b,'off-noop'))
   assert(writes==w and probe.mode=='OFF' and probe.View(0,a).variant=='SINGLE3')
  """)
  ui=(M/'UI/P0Panel.lua').read_text()
  for button,mouse,action in [('MeaningConfigButton','eLClick','CULTURE_MEANING_CONFIG'),('MeaningConfigButton','eRClick','CULTURE_MEANING_END'),('MeaningProbeButton','eLClick','CULTURE_MEANING_ADVANCE'),('MeaningProbeButton','eRClick','CULTURE_MEANING_READ')]:
   self.assertIn("Controls."+button+":RegisterCallback(Mouse."+mouse+",function() request('"+action+"') end)",ui)
  xml=ET.parse(M/'UI/P0Panel.xml').getroot();self.assertIsNotNone(xml.find('.//*[@ID="MeaningConfigButtonCaption"]'))
  text=(M/'Text/TestText.sql').read_text()
  for key in ['LOC_SPC_CULTURE_MEANING_CONFIG','LOC_SPC_CULTURE_MEANING_CONFIG_HINT']:self.assertEqual(text.count("'"+key+"'"),2)
 def test_actual_request_end_cleanup_failure_retains_holds_and_new_token_recovers(self):
  l=self.culture3_runtime();bind_actual_request(l);l.execute("""
   probe.CycleVariant(0,a,'single');probe.Advance(0,a,'baseline');probe.Advance(0,a,'active')
   local id=GameInfo.Buildings[SPCCultureMeaningModel.VariantParts.SINGLE3.name].Index
   failRemove=id;meaningRequest(0,{Action='CULTURE_MEANING_END',CityID=1,Token='failed-end'})
   local v=shared.CultureMeaningView
   assert(shared.LastToken=='failed-end' and v.token=='failed-end' and v.mode=='ACTIVE' and v.error and probe.stopping)
   assert(shared.Snapshot:find('%[END%]') and shared.Snapshot:find('ME_REMOVE_UNCONFIRMED'))
   assert(configured(a,'CULTURE')==3 and gwa.IsMeaningHeld(0,a) and dialogue.IsMeaningProbeHeld(0,a,0) and not old(a,'SCIENCE'))
   assert(old(b,'SCIENCE') and next(exactMeaning(b))==nil and probe.lastAction.kind=='END')
   local w=writes;failRemove=nil;meaningRequest(0,{Action='CULTURE_MEANING_END',CityID=1,Token='failed-end'})
   assert(writes==w and configured(a,'CULTURE')==3 and probe.stopping)
   meaningRequest(0,{Action='CULTURE_MEANING_END',CityID=1,Token='retry-end'})
   v=shared.CultureMeaningView
   assert(shared.LastToken=='retry-end' and v.token=='retry-end' and v.mode=='OFF' and not v.error and not probe.stopping)
   assert(next(exactMeaning(a))==nil and dialogue.meaningOverride==nil and old(a,'SCIENCE') and old(b,'SCIENCE'))
   w=writes;meaningRequest(0,{Action='CULTURE_MEANING_END',CityID=1,Token='retry-end'});assert(writes==w and probe.mode=='OFF')
  """)

if __name__=='__main__':unittest.main()
