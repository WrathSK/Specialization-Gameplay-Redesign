"""B270 actual consumer event-scope and cleanup recovery regressions; native doubles only."""
from pathlib import Path
from lupa.lua51 import LuaRuntime
MOD = Path(__file__).resolve().parents[1] / 'Mod'
MODULES = ['Lv2Housing', 'Lv2GPP', 'ResearchSupport', 'IndustrySupport', 'Lv3Effects', 'ResearchInfrastructure', 'Lv3Support']

def make_fixture(n_ai=50, supported=False, mod=MOD, initial_load=True):
    lua = LuaRuntime(unpack_returned_tuples=True)
    lua.globals().include = lambda name: lua.execute((mod / (name + '.lua')).read_text())
    lua.execute(r'''
Game={GetCurrentGameTurn=function()return turn end,GetLocalPlayer=function()return 0 end};turn=1
ExposedMembers={};counts={};active='NONE';byModule={};ids={};names={};nextId=0;Players={};cities={}
function events()
 return setmetatable({},{__index=function(t,n)
  local fs={};local e={Add=function(f)fs[#fs+1]=f end,Fire=function(...)for _,f in ipairs(fs)do f(...)end end}
  rawset(t,n,e);return e
 end})
end
Events=events();GameEvents=events()
P={Field=function(t,k)return t[k]end,IsTestPlayer=function(pid)return pid==0 end,Observe=function()end}
P.Count=function(k)
 counts[k]=(counts[k]or 0)+1;byModule[active]=byModule[active]or{}
 byModule[active][k]=(byModule[active][k]or 0)+1
end
P.HasBuilding=function(b,k)P.Count('building_check');return b:HasBuilding(k)end
P.RemoveBuilding=function(b,k)P.Count('building_remove');return b:RemoveBuilding(k)end
P.CreateBuilding=function(b,k)P.Count('building_create');return b:CreateBuilding(k)end
P.Info=function(t,k)
 if t=='Districts'then return {Index=1,DistrictType='DISTRICT_CAMPUS'}end
 if t=='Buildings'then
  if type(k)=='number'then k=names[k]end
  if not ids[k]then nextId=nextId+1;ids[k]=nextId;names[nextId]=k end
  local kind=k:match('DEV_GPP_(%u+)_')
  return {Index=ids[k],BuildingType=k,InternalOnly=true,Housing=k:find('HOUSING')and 1 or 0,CitizenSlots=0,
   PrereqDistrict=({RESEARCH='DISTRICT_CAMPUS',CULTURE='DISTRICT_THEATER',COMMERCE='DISTRICT_COMMERCIAL_HUB',INDUSTRY='DISTRICT_INDUSTRIAL_ZONE'})[kind]or'DISTRICT_CAMPUS'}
 end
end
P.Rows=function(t)
 local rows={}
 if t=='Building_CitizenYieldChanges'then for i=0,3 do rows[#rows+1]={BuildingType='BUILDING_SPC_RESEARCH_INFRA_'..i,YieldType='YIELD_SCIENCE',YieldChange=2^i}end end
 if t=='Building_GreatPersonPoints'then
  local cls={RESEARCH={'SCIENTIST'},CULTURE={'WRITER','ARTIST','MUSICIAN'},COMMERCE={'MERCHANT'},INDUSTRY={'ENGINEER'}}
  for k,vs in pairs(cls)do for i=0,7 do for _,v in ipairs(vs)do
   rows[#rows+1]={BuildingType='BUILDING_SPC_DEV_GPP_'..k..'_'..i,GreatPersonClassType='GREAT_PERSON_CLASS_'..v,PointsPerTurn=2*2^i}
  end end end
 end
 return rows
end
P.Family=function()return nil end
function addCity(pid,cid,x,y)
 local c={owner=pid,id=cid,x=x,y=y,values={},bad=false}
 c.GetOwner=function()return c.owner end;c.GetID=function()return c.id end
 c.GetX=function()return c.x end;c.GetY=function()return c.y end;c.GetProperty=function()return nil end
 c.GetBuildings=function()return {
  HasBuilding=function(_,id)if c.bad then error('READ_UNKNOWN')end;return c.values[id]==true end,
  RemoveBuilding=function(_,id)c.values[id]=nil end
 }end
 c.GetBuildQueue=function()return {CreateBuilding=function(_,id)c.values[id]=true end}end
 cities[pid]=cities[pid]or{};cities[pid][cid]=c
 Players[pid]=Players[pid]or{
  GetCities=function()return {Members=function()return pairs(cities[pid])end,FindID=function(_,id)return cities[pid][id]end}end,
  GetDistricts=function()return {Members=function()return ipairs({})end}end
 }
 return c
end
shared={EffectiveFacts={Read=function(pid,c)
 assert(pid==0,'SHOULD_NOT_READ_AI_FACTS')
 return {specialization='NONE',potential=0,active=0,token='TEST:'..c:GetID()}
end}}
function resetCounts()counts={};byModule={}end
''')
    for pid in range(1, n_ai + 1):
        lua.globals().addCity(pid, pid, pid * 2, pid * 3)
    if supported:
        lua.globals().addCity(0, 0, 0, 0)
    lua.execute((mod / 'CurrentSpecializationFacts.lua').read_text())
    for module in MODULES:
        lua.execute((mod / (module + '.lua')).read_text())
        lua.execute('active="%s"; SPC%s.Start(P,shared%s)' % (
            module, module, ',{retireCommerce=true}' if module == 'Lv3Effects' else ''))
    lua.execute("P.Observe=function(group,name)if group=='audit'then active=name end end")
    if initial_load:lua.execute("Events.LoadScreenClose.Fire()")
    lua.execute("resetCounts()")
    reset_counts = lua.globals().resetCounts
    def counts():
        return dict(lua.globals().counts)
    return lua, reset_counts, counts


import unittest

class EventScopeTests(unittest.TestCase):
    def test_nonparticipants_do_not_scale_real_events(self):
        for n in (1, 10, 50):
            lua, reset, count = make_fixture(n)
            lua.execute('Events.DistrictBuildProgressChanged.Fire(1,1,1,10,20,1)')
            self.assertEqual(count().get('city_scan', 0), 0)
            self.assertEqual(count().get('building_check', 0), 0)
            reset(); lua.execute('Events.ImprovementAddedToMap.Fire(10,20,1,1)')
            self.assertEqual(count().get('city_scan', 0), 0)
            self.assertEqual(count().get('building_check', 0), 0)
            reset(); lua.execute('GameEvents.OnDistrictConstructed.Fire(1,1,10,20)')
            self.assertEqual(count().get('city_scan', 0), 0)

    def test_known_city_does_not_read_other_participant_city(self):
        lua, reset, count = make_fixture(50, True, initial_load=False)
        lua.execute('other=addCity(0,2,2,2);Events.LoadScreenClose.Fire();other.bad=true;resetCounts();Events.DistrictBuildProgressChanged.Fire(0,1,0,0,0,1)')
        self.assertEqual(count()['city_scan'], 5)
        self.assertEqual(count()['building_check'], 57)
        self.assertEqual(count().get('building_create', 0), 0)
        self.assertIsNone(lua.eval("shared.Lv2GPP.errors['0:2']"))

    def test_unknown_completion_fallback_only_participants(self):
        lua, reset, count = make_fixture(50, True)
        lua.execute('GameEvents.BuildingConstructed.Fire()')
        self.assertLessEqual(count().get('city_scan', 0), 5)
        self.assertLessEqual(count().get('building_check', 0), 57)

    def test_cold_foreign_cleanup_unknown_then_recovery(self):
        lua, reset, count = make_fixture(1, initial_load=False)
        lua.execute("local id=P.Info('Buildings','BUILDING_SPC_DEV_LV2_HOUSING_0').Index;cities[1][1].values[id]=true;cities[1][1].bad=true;Events.LoadScreenClose.Fire()")
        self.assertTrue(lua.eval("cities[1][1].values[P.Info('Buildings','BUILDING_SPC_DEV_LV2_HOUSING_0').Index]"))
        lua.execute('cities[1][1].bad=false;Events.PlayerTurnActivated.Fire(1)')
        self.assertIsNone(lua.eval("cities[1][1].values[P.Info('Buildings','BUILDING_SPC_DEV_LV2_HOUSING_0').Index]"))
        self.assertIsNone(lua.eval("shared.Lv2Housing.errors['1:1']"))
        self.assertIsNone(lua.eval("shared.Lv3Support.errors['1:1']"))

    def test_exit_survives_raw_removal_and_three_failed_reads(self):
        lua, _, _ = make_fixture(1)
        lua.execute('''
          calls=0;allow=false;proof={target=1};err=nil
          owner=SPCRuntimeWork.NewTargets(P,shared,function()end,function(_,_,e)err=e end)
          exit=owner.Exit(function(c,loss)
            assert(loss==proof and c==cities[1][1]);calls=calls+1
            if not allow then error('EXIT_CARRIER_UNKNOWN')end
          end)
          assert(not pcall(exit,cities[1][1],proof))
          owner.Retry();owner.Retry();assert(calls==3 and owner.exits['1:1'])
          Events.CityRemovedFromMap.Fire(1,1);allow=true;owner.Retry()
          assert(calls==4 and not owner.exits['1:1'] and err==nil)
        ''')

    def test_reused_city_reference_is_not_an_exit_target(self):
        lua, _, _ = make_fixture(1)
        lua.execute('''
          calls=0;allow=false;original=cities[1][1]
          owner=SPCRuntimeWork.NewTargets(P,shared,function()end,function()end)
          exit=owner.Exit(function(c)calls=calls+1;assert(c==original);assert(allow)end)
          assert(not pcall(exit,original,{}));addCity(1,1,99,99);allow=true;owner.Retry()
          assert(calls==1 and owner.exits['1:1'])
          cities[1][1]=original;owner.Retry();assert(calls==2 and not owner.exits['1:1'])
        ''')

    def test_retirement_success_only_and_removed_invalidates_stamp(self):
        lua, _, _ = make_fixture(1)
        lua.execute('''
          calls=0;good=false;c=cities[1][1]
          function retire()return SPCRuntimeWork.RetireOnce(P,shared,c,'test',function()
            calls=calls+1;assert(good,'UNKNOWN');return 1
          end)end
          assert(not pcall(retire));good=true;assert(retire()==1 and calls==2)
          assert(retire()==0 and calls==2)
          Events.CityRemovedFromMap.Fire(1,1);assert(retire()==1 and calls==3)
        ''')

    def test_unreadable_transfer_does_not_latch_audit_busy(self):
        lua, _, _ = make_fixture(1, True)
        lua.execute("""
          shared.Lv2Housing.Audit();local c=cities[0][0];local p=Players[1]
          c.owner=1;cities[0][0]=nil;cities[1][0]=c
          local old=p.GetCities;p.GetCities=function()error('NATIVE_UNAVAILABLE')end
          Events.CityTransfered.Fire(1,0,0)
          assert(shared.Lv2Housing.busy==false and shared.Lv2GPP.busy==false)
          p.GetCities=old;Events.PlayerTurnActivated.Fire(1)
          assert(shared.Lv2Housing.errors['1:0']==nil and shared.Lv2GPP.errors['1:0']==nil)
        """)

    def test_retired_pending_follows_confirmed_transfer_to_new_id(self):
        for old_owner in (0, 1):
            lua, _, _ = make_fixture(2, old_owner==0)
            lua.execute("""
              c=cities[%d][%d];local id=P.Info('Buildings','BUILDING_SPC_DEV_LV3_POP_CULTURE_0').Index
              c.values[id]=true;c.bad=true;Events.LoadScreenClose.Fire()
              local oldOwner=c.owner;local oldID=c.id;cities[oldOwner][oldID]=nil
              c.owner=2;c.id=11;cities[2][11]=c
              Events.CityTransfered.Fire(2,11,oldOwner)
              c.bad=false;Events.PlayerTurnActivated.Fire(2)
              assert(not c.values[id] and shared.Lv3Effects.busy==false)
            """ % (old_owner,old_owner))


class IconAliasTests(unittest.TestCase):
    def test_actual_icon_sql_retains_native_project_atlas(self):
        import sqlite3
        db = sqlite3.connect(':memory:')
        db.executescript('CREATE TABLE IconDefinitions(Name TEXT PRIMARY KEY,Atlas TEXT,"Index" INTEGER);'
                         'CREATE TABLE IconTextureAtlases(Name TEXT,IconSize INTEGER,IconsPerRow INTEGER,IconsPerColumn INTEGER,Filename TEXT);')
        db.execute('INSERT INTO IconDefinitions VALUES(?,?,?)',
                   ('ICON_PROJECT_ENHANCE_DISTRICT_INDUSTRIAL_ZONE', 'NATIVE_PROJECTS', 7))
        db.executescript((MOD / 'Data/Icons.sql').read_text())
        self.assertEqual(db.execute('SELECT Atlas,"Index" FROM IconDefinitions WHERE Name=?',
                                    ('ICON_PROJECT_SPC_OVERFLOW_SINK_TEST',)).fetchone(), ('NATIVE_PROJECTS', 7))
        self.assertEqual(db.execute('SELECT Atlas,"Index" FROM IconDefinitions WHERE Name=?',
                                    ('ICON_PROJECT_ENHANCE_DISTRICT_INDUSTRIAL_ZONE',)).fetchone(), ('NATIVE_PROJECTS', 7))
        db.close()

if __name__ == '__main__':
    unittest.main()
