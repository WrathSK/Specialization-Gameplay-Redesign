"""S8c4 exact catalogue vs real current Start closures/options; DB remains read-only."""
import json,sqlite3,unittest
from refactor_harness import Context,ROOT,measure
from project_paths import external_database

OPTIONS={'Lv3Effects':'{retireCommerce=true}','NetworkBoost':'{retired=true}','GreatWorkAdjacency':'{retired=true}','CommerceConvergence':'{retired=true}','CopyYields':'{retired=true}','StandardizationDiscount':'{retired=true}','CultureInspirationProbe':'{retired=true}'}
MODULES=('HalfYieldProbe','PurchaseProbe','GreatWorkProbe','Lv3Support','Lv3Effects','Lv4Percent','NetworkBoost','GreatWorkAdjacency','Dialogue','CommerceConvergence','CopyYields','StandardizationDiscount','CultureInspirationProbe')
COUNTS={'HalfYieldProbe':32,'PurchaseProbe':2,'GreatWorkProbe':2,'Lv3Support':12,'Lv3Effects':11,'Lv4Percent':8,'NetworkBoost':1126,'GreatWorkAdjacency':156,'Dialogue':12,'CommerceConvergence':48}

def catalog():
 c=Context();c.load('BoostConfig');c.load('BoostIntegerConfig');c.load('LegacyCleanupCatalog');return c

def groups(c,eras=9):
 values=c.execute('return SPCLegacyCleanupCatalog.Build(...,SPCBoostConfig.rows,SPCBoostIntegerConfig.rows)',eras)
 return {r['key']:{'kind':r['kind'],'names':list(r['names'].values())}for r in values.values()}


class PureCatalogue(unittest.TestCase):
 def test_no_native_reads_hooks_or_writes_and_detached_results(self):
  c=catalog();c.execute("""
  local forbidden=setmetatable({},{__index=function()error('NATIVE_FORBIDDEN')end,__newindex=function()error('NATIVE_FORBIDDEN')end})
  local events,gameEvents=Events,GameEvents
  Players=forbidden;Game=forbidden;GameInfo=forbidden;Map=forbidden;Events=forbidden;GameEvents=forbidden
  local a=SPCLegacyCleanupCatalog.Build(9,SPCBoostConfig.rows,SPCBoostIntegerConfig.rows)
  assert(#a==11);Events=events;GameEvents=gameEvents
  assert(Events.PlayerTurnActivated.Count()==0 and Events.LoadScreenClose.Count()==0)
  a[1].names[1]='MUTATE';a[2].kind='MUTATE';a[5].names[1]='MUTATE'
  local b=SPCLegacyCleanupCatalog.Build(9,SPCBoostConfig.rows,SPCBoostIntegerConfig.rows)
  assert(b[1].names[1]~='MUTATE'and b[2].kind=='buildings'and b[5].names[1]~='MUTATE')
  assert(SPCTombstones.Names('SpecialistSupport')[1]~='MUTATE')
  assert(SPCBoostConfig.rows['RESEARCH:1:1'].building=='BUILDING_SPC_B055_RESEARCH_1_1')
  """)
  self.assertEqual(sum(len(v['names'])for v in groups(c).values()if v['kind']=='buildings'),1409)
 def test_complete_explicit_directories_and_exact_names_required(self):
  mutations=["SPCBoostConfig.rows={}","SPCBoostConfig.rows['RESEARCH:1:1']=nil","SPCBoostIntegerConfig.rows={}","SPCBoostIntegerConfig.rows['CULTURE:45']=nil","SPCBoostConfig.rows['RESEARCH:1:1'].building='BUILDING_LIBRARY'","SPCBoostConfig.rows['RESEARCH:1:1'].building='BUILDING_SPC_OTHER'","SPCBoostIntegerConfig.rows['RESEARCH:1']='BUILDING_SPC_B058_CULTURE_1'","setmetatable(SPCBoostConfig.rows,{})","SPCBoostConfig.rows['RESEARCH:01:1']=SPCBoostConfig.rows['RESEARCH:1:1']"]
  for change in mutations:
   c=catalog();c.execute(change+";assert(not pcall(SPCLegacyCleanupCatalog.Build,9,SPCBoostConfig.rows,SPCBoostIntegerConfig.rows))")
  for era in (0,-1,1.5,'UNKNOWN'):
   c=catalog();self.assertFalse(c.execute('return pcall(SPCLegacyCleanupCatalog.Build,...,SPCBoostConfig.rows,SPCBoostIntegerConfig.rows)',era)[0])
 def test_stable_output_with_reordered_input_maps_and_distinct_loaded_era_directory(self):
  c=catalog();before=groups(c)
  c.execute("local a,b={},{};local keys={};for k in pairs(SPCBoostConfig.rows)do keys[#keys+1]=k end;table.sort(keys,function(x,y)return x>y end);for _,k in ipairs(keys)do a[k]=SPCBoostConfig.rows[k]end;for k,v in pairs(SPCBoostIntegerConfig.rows)do b[k]=v end;SPCBoostConfig.rows=a;SPCBoostIntegerConfig.rows=b")
  self.assertEqual(before,groups(c));self.assertEqual(len(groups(c,8)['Dialogue']['names']),11)


class ActualCurrentOwners(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.db=sqlite3.connect(external_database(ROOT).as_uri()+'?mode=ro',uri=True);cls.db.row_factory=sqlite3.Row
 @classmethod
 def tearDownClass(cls):cls.db.close()
 def capture(self):
  c=Context();db=self.db
  tables={t:[dict(r)for r in db.execute('SELECT * FROM "'+t+'"')]for t in ('Eras','HD_BuildingTiers','HD_DUMMY_BUILDINGS')}
  buildings={r['BuildingType']:dict(r)for r in db.execute('SELECT rowid AS "Index",* FROM Buildings')}
  def rows(t):return c.lua.table_from([c.lua.table_from(r)for r in tables[t]])
  def info(t,k):
   assert t=='Buildings',t
   r=buildings.get(k);return c.lua.table_from(r)if r else None
  c.lua.globals().dbrows=rows;c.lua.globals().dbinfo=info
  c.execute("""
  captured={};owned={};plotWrites={};current=nil;Players={}
  P={Field=function(t,k)return t and t[k]end,IsTestPlayer=function(pid)return pid==0 end,Count=function()end,
   Info=function(t,k)return dbinfo(t,k)end,Rows=function(t)return dbrows(t)end,SetProperty=function(p,k,v)p:SetProperty(k,v)end}
  SPCP0=P;shared.EffectiveFacts={Read=function()error('ACTIVE_FACTS_FORBIDDEN')end}
  shared.CityProgressionStore={RegisterExit=function(n,f)assert(not captured[n]);captured[n]=f end,RegisterReturn=function()end,
   RemoveOwned=function(c,loss,names)assert(not owned[current]);owned[current]=names end,IsExitTarget=function()return true end}
  GameInfo={};for _,t in ipairs({'Eras','HD_BuildingTiers','HD_DUMMY_BUILDINGS'})do
   local name=t;GameInfo[name]=function()local rows=dbrows(name);local i=0;return function()i=i+1;return rows[i]end end
  end
  city={GetOwner=function()return 9 end,GetID=function()return 900 end,GetX=function()return 1 end,GetY=function()return 2 end}
  Map={GetPlot=function()return {GetProperty=function(_,k)if plotWrites[k]~=nil then return plotWrites[k]end;return 1 end,SetProperty=function(_,k,v)plotWrites[k]=v end}end}
  """)
  for module in MODULES:
   c.load(module);symbol='SPCGWAdjacency'if module=='GreatWorkAdjacency'else'SPC'+module
   c.execute(symbol+'.Start(P,shared,'+OPTIONS.get(module,'nil')+')')
  c.load('YieldCarrierProbe');c.execute('SPCYieldCarrierProbe.RegisterExit(shared)')
  c.execute("for name,fn in pairs(captured)do current=name;fn(city,{origin={owner=0,cityID=101}})end")
  c.load('LegacyCleanupCatalog');return c,buildings
 def test_real_current_start_options_match_every_exact_catalogue_group(self):
  c,buildings=self.capture();eraCount=len(list(self.db.execute('SELECT EraType FROM Eras')));planned=groups(c,eraCount)
  actual={k:set(v.values())for k,v in c.lua.globals().owned.items()}
  self.assertEqual(set(c.lua.globals().captured),set(planned));self.assertEqual(len(planned),11)
  for name,values in actual.items():self.assertEqual(values,set(planned[name]['names']),name)
  self.assertEqual(dict(c.lua.globals().plotWrites),{'SPC_B029_ONE':0,'SPC_B029_HALF':0})
  self.assertEqual(set(planned['YieldCarrierProbe']['names']),{'SPC_B029_ONE','SPC_B029_HALF'})
  names=set();activity={};counts={}
  for name,values in actual.items():
   counts[name]=len(values);self.assertFalse(names&values,name);names.update(values)
   self.assertTrue(all(buildings[v]['InternalOnly']==1 for v in values))
   activity[name]=sum(self.db.execute('SELECT count(*) FROM BuildingModifiers WHERE BuildingType=?',(v,)).fetchone()[0]for v in values)
  self.assertEqual(len(names),1409);self.assertEqual(counts,COUNTS);self.assertEqual(activity['CommerceConvergence'],48)
  self.assertNotIn('CopyYields',actual);self.assertNotIn('StandardizationDiscount',actual);self.assertNotIn('CultureInspirationProbe',actual)
  self.assertEqual(self.db.execute('SELECT count(*) FROM SPC_B054_Targets').fetchone()[0],576)
  measure('S8c4_actual_current_legacy_catalogue',{'actual_exits':11,'buildings':1409,'plot_flags':2,'groups':counts,'SQL_modifier_links':activity,'unreachable_source_exit_live_Withdraw_ids':620,'production_exit_migration':'NOT_YET_WIRED','native_effect_cleanup':'USER_GAME_TEST_REQUIRED'})
 def test_actual_production_Withdraw_and_fixture_hold_duties_are_preserved(self):
  c,_=self.capture()
  c.execute("assert(type(shared.CopyYields.Withdraw)=='function'and type(shared.StandardizationDiscount.Withdraw)=='function'and type(shared.CultureInspirationProbe.Withdraw)=='function'and type(shared.Lv3Effects.WithdrawCulture)=='function'and type(shared.Lv4Percent.WithdrawCulture)=='function'and type(shared.GreatWorkAdjacency.Withdraw)=='function'and type(shared.CommerceConvergence.Withdraw)=='function'and type(shared.Dialogue.Init)=='function')")
  calls=(ROOT/'Mod/Dialogue.lua').read_text();self.assertIn('if h and h.reference==t.reference and h.city==loss.origin.cityID then',calls)
  self.assertNotIn("composition.Run('LegacyCleanup",(ROOT/'Mod/Gameplay.lua').read_text())

if __name__=='__main__':unittest.main()
