"""B199 display-only city mission locations: actual Lua with native API fixtures.

READABLE means the provided snapshot could be read, not that a foreign city's
native inventory visibility/completeness has been demonstrated in game.
"""
from pathlib import Path
import unittest
from test_expedition_spy_task import gate

R = Path(__file__).resolve().parents[1]


def add_locations(lua, host_count=1):
    """Local fixture shared with presentation tests; N hosts + center + 2 Wonders."""
    lua.execute((R / 'Mod/GreatWorkCatalog.lua').read_text())
    lua.globals().locationHostCount = host_count
    lua.execute("""
      districtReads=0;buildingLocationReads=0;slotReads=0;workReads=0
      districtRows={};buildingsAt={};slotData={};presentBuildings={};workTypes={}
      GameInfo.Districts={};GameInfo.Buildings=setmetatable({}, {__call=function()error('full building DB scan forbidden')end})
      GameInfo.GreatWorks={};GameInfo.Eras={ERA_CLASSICAL={EraType='ERA_CLASSICAL'}}
      GameInfo.GreatPersonIndividuals={}
      function addDistrict(i,kind,x,complete)
       local d={index=i,x=x,y=8,complete=complete~=false}
       function d:GetType()return self.index end;function d:IsComplete()return self.complete end
       function d:GetX()return self.x end;function d:GetY()return self.y end
       districtRows[#districtRows+1]=d
       local def={Index=i,DistrictType=kind,Name='LOC_'..kind};GameInfo.Districts[i]=def;GameInfo.Districts[kind]=def
       buildingsAt[x*100+8]={};return d
      end
      function addBuilding(i,kind,x,wonder,slots,present)
       local def={Index=i,BuildingType=kind,Name='LOC_'..kind,IsWonder=wonder or false}
       GameInfo.Buildings[i]=def;GameInfo.Buildings[kind]=def
       table.insert(buildingsAt[x*100+8],i);slotData[i]=slots or {};presentBuildings[i]=present~=false
      end
      addDistrict(1,'DISTRICT_CITY_CENTER',15);addBuilding(1001,'BUILDING_PALACE',15,false,{})
      for i=1,locationHostCount do
       addDistrict(1+i,'DISTRICT_HOST_'..i,15+i)
       addBuilding(1100+i,'BUILDING_WORK_HOST_'..i,15+i,false,{100,101})
      end
      addDistrict(100,'DISTRICT_WONDER',40)
      addBuilding(2000,'BUILDING_PYRAMIDS',40,true,{100})
      addDistrict(101,'DISTRICT_WONDER',41)
      addBuilding(2001,'BUILDING_GREAT_LIBRARY',41,true,{100,101})
      addDistrict(102,'DISTRICT_WONDER',42,false)
      addBuilding(2002,'BUILDING_UNFINISHED_WONDER',42,true,{})
      addDistrict(103,'DISTRICT_RELIC_HOST',43)
      addBuilding(3000,'BUILDING_RELIC_HOST',43,false,{200})
      addDistrict(104,'DISTRICT_WONDER',44)
      addBuilding(2003,'BUILDING_NOT_PRESENT_WONDER',44,true,{},false)
      local work={GreatWorkType='GREATWORK_HOMER_1',GreatWorkObjectType='GREATWORKOBJECT_WRITING',EraType='ERA_CLASSICAL',Name='Private work name'}
      GameInfo.GreatWorks[1]=work;GameInfo.GreatWorks[work.GreatWorkType]=work;workTypes[100]=1;workTypes[101]=1
      local relic={GreatWorkType='GREATWORK_RELIC_TEST',GreatWorkObjectType='GREATWORKOBJECT_RELIC',Name='Private relic name'}
      GameInfo.GreatWorks[2]=relic;GameInfo.GreatWorks[relic.GreatWorkType]=relic;workTypes[200]=2
      locationBuildings={}
      function locationBuildings:GetBuildingsAtLocation(plotID)buildingLocationReads=buildingLocationReads+1;return buildingsAt[plotID]end
      function locationBuildings:HasBuilding(i)return presentBuildings[i]end
      function locationBuildings:GetNumGreatWorkSlots(i)slotReads=slotReads+1;return #slotData[i]end
      function locationBuildings:GetGreatWorkInSlot(i,s)workReads=workReads+1;return slotData[i][s+1]end
      function locationBuildings:GetGreatWorkTypeFromIndex(id)return workTypes[id]end
      targetCity.GetBuildings=function()return locationBuildings end
      targetCity.GetDistricts=function()districtReads=districtReads+1;return {Members=function()return ipairs(districtRows)end}end
      local nativePlot=Map.GetPlot
      Map.GetPlot=function(x,y)local p=nativePlot(x,y);function p:GetIndex()return x*100+y end;return p end
      function locationSnapshot()return reader.Presentation(2,40,target)end
      function assertNoLocationWrites()
       assert(properties==0 and nativeCalls==0 and placeCalls==0 and destroys==0 and finishCalls==0)
      end
    """)


def locations():
    lua=gate(ui=True)
    lua.globals().print=lambda *args:None
    lua.execute("req('CREATE','fixture');assert(units[40])")
    add_locations(lua)
    return lua


class LocationSnapshot(unittest.TestCase):
    def test_center_positive_work_host_and_each_completed_wonder(self):
        lua=locations()
        lua.execute("""
          local v=locationSnapshot()
          assert(v.locationStatus=='READABLE' and v.locationReason==nil and #v.districts==4)
          local expected={'ICON_DISTRICT_CITY_CENTER','ICON_DISTRICT_HOST_1','ICON_BUILDING_PYRAMIDS','ICON_BUILDING_GREAT_LIBRARY'}
          for i,icon in ipairs(expected)do assert(v.districts[i].icon==icon)end
          -- Work-bearing Wonders are one icon each; unsupported and unfinished
          -- buildings do not create false work locations.
          assert(v.districts[3].kind=='WONDER' and v.districts[4].kind=='WONDER')
          assert(v.total==4 and districtReads==1 and buildingLocationReads==6 and slotReads==3 and workReads==3)
          assertNoLocationWrites()
        """)

    def test_uses_actual_host_location_not_prerequisite_or_theater_assumption(self):
        lua=locations()
        lua.execute("""
          GameInfo.Buildings[1101].PrereqDistrict='DISTRICT_THEATER'
          local v=locationSnapshot();assert(v.districts[2].icon=='ICON_DISTRICT_HOST_1')
          assertNoLocationWrites()
        """)

    def test_center_and_multiple_host_buildings_deduplicate_by_location(self):
        lua=locations()
        lua.execute("""
          addBuilding(1002,'BUILDING_PALACE_WORKS',15,false,{100})
          addBuilding(1102,'BUILDING_SECOND_HOST',16,false,{101})
          local v=locationSnapshot();assert(v.locationStatus=='READABLE' and #v.districts==4)
          assertNoLocationWrites()
        """)

    def test_known_unsupported_work_is_not_admitted_by_its_broad_category(self):
        lua=locations()
        lua.execute("""
          local w={GreatWorkType='UNKNOWN_MOD_WRITING',GreatWorkObjectType='GREATWORKOBJECT_WRITING',EraType='ERA_CLASSICAL'}
          GameInfo.GreatWorks[3]=w;GameInfo.GreatWorks[w.GreatWorkType]=w;workTypes[100]=3;workTypes[101]=3
          local v=locationSnapshot();assert(v.locationStatus=='READABLE' and #v.districts==3)
          assert(v.districts[2].icon=='ICON_BUILDING_PYRAMIDS');assertNoLocationWrites()
        """)

    def test_empty_known_slots_are_readable_and_not_work_locations(self):
        lua=locations()
        lua.execute("""
          slotData[1101]={-1,-1};local v=locationSnapshot()
          assert(v.locationStatus=='READABLE' and #v.districts==3);assertNoLocationWrites()
        """)

    def test_missing_api_or_read_failure_is_unknown_not_false_empty(self):
        changes={
            "targetCity.GetBuildings=nil":'LOCATION_READER_UNAVAILABLE:GetBuildings',
            "targetCity.GetDistricts=nil":'LOCATION_READER_UNAVAILABLE:GetDistricts',
            "locationBuildings.GetBuildingsAtLocation=nil":'LOCATION_READER_UNAVAILABLE:GetBuildingsAtLocation',
            "locationBuildings.GetBuildingsAtLocation=function()error('native read failed')end":'LOCATION_READ_FAILED:GetBuildingsAtLocation',
            "locationBuildings.GetNumGreatWorkSlots=nil":'LOCATION_READER_UNAVAILABLE:GetNumGreatWorkSlots',
            "locationBuildings.GetGreatWorkInSlot=function()return nil end":'LOCATION_WORK_SLOT_UNKNOWN',
            "locationBuildings.GetGreatWorkTypeFromIndex=nil":'LOCATION_READER_UNAVAILABLE:GetGreatWorkTypeFromIndex',
            "GameInfo.GreatWorks[1]=nil":'LOCATION_WORK_DEFINITION_UNAVAILABLE',
            "GameInfo.Buildings[1101]=nil":'LOCATION_BUILDING_DEFINITION_UNAVAILABLE',
            "GameInfo.Eras.ERA_CLASSICAL=nil":'LOCATION_WORK_METADATA_UNKNOWN',
            "locationBuildings.HasBuilding=function()return nil end":'LOCATION_BUILDING_PRESENCE_UNKNOWN',
            "locationBuildings.GetNumGreatWorkSlots=function()return 300 end":'LOCATION_SLOT_COUNT_UNKNOWN',
        }
        for change,reason in changes.items():
            with self.subTest(change=change):
                lua=locations();lua.globals().expectedLocationReason=reason
                lua.execute(change+";local v=locationSnapshot();assert(v.locationStatus=='UNKNOWN' and v.locationReason==expectedLocationReason, tostring(v.locationReason));assert(v.districts[1].icon=='ICON_DISTRICT_CITY_CENTER' and v.total==4);assertNoLocationWrites()")

    def test_unrevealed_unmet_or_changed_target_does_not_sample_locations(self):
        for change in ['visible=false','met=false','targetCity.owner=4','targetCity.x=16']:
            with self.subTest(change=change):
                lua=locations()
                lua.execute(change+";local helpers=helperCalls;local v=locationSnapshot();assert(v.locationStatus=='UNKNOWN' and v.locationReason=='LOCATION_TARGET_UNAVAILABLE' and #v.districts==0);assert(districtReads==0 and buildingLocationReads==0 and helperCalls==helpers);assertNoLocationWrites()")

    def test_target_changes_during_read_discards_stale_location_snapshot(self):
        lua=locations()
        lua.execute("""
          local old=locationBuildings.GetBuildingsAtLocation
          locationBuildings.GetBuildingsAtLocation=function(self,...)
           local result=old(self,...);targetCity.owner=4;return result
          end
          local v=locationSnapshot();assert(v.locationStatus=='UNKNOWN' and v.locationReason=='LOCATION_TARGET_CHANGED' and #v.districts==0)
          assertNoLocationWrites()
        """)

    def test_snapshot_has_no_private_work_names_eras_or_inventory(self):
        lua=locations()
        lua.execute("""
          local v=locationSnapshot()
          for _,item in ipairs(v.districts)do
           for key in pairs(item)do assert(key=='icon' or key=='name' or (key=='kind' and item.kind=='WONDER'))end
           assert(not item.name:find('Private',1,true))
          end
          assertNoLocationWrites()
        """)

    def test_unknown_preview_does_not_become_a_dispatch_gate(self):
        lua=locations()
        lua.execute("""
          locationBuildings.GetBuildingsAtLocation=nil
          local view=locationSnapshot();assert(view.locationStatus=='UNKNOWN')
          local sample=reader.Read(2,40,target)
          assert(sample.status=='READ_OK' and sample.nativeAllowed==true)
          assert(reader.SubmitTravel(2,40,target,'independent-display-read'))
          assert(nativeCalls==1 and properties==0 and placeCalls==0 and destroys==0)
        """)


if __name__=='__main__':unittest.main()
