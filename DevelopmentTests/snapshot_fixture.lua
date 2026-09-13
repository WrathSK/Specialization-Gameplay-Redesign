-- End-to-end fixture: source adapter + UI callbacks, without a running game.
local function Rows(rows)
  local index = {}
  for _, row in ipairs(rows) do
    for _, field in ipairs({"GreatPersonClassType", "BuildingType", "DistrictType", "ModifierId", "PolicyType"}) do
      if row[field] then index[row[field]] = row end
    end
    if row.Index then index[row.Index] = row end
  end
  return setmetatable(index, {__call=function() local n=0; return function() n=n+1; return rows[n] end end})
end
local classes = {{Index=0,GreatPersonClassType="SCI",Name="科学家"}}
local definitions = {
  [1]={Id="DAOGUAN",Arguments={Amount="6",GreatPersonClassType="SCI"}},
  [2]={Id="CITY_PERCENT",Arguments={Amount=50}},
  [3]={Id="POLICY_FLAT",Arguments={Amount=2,GreatPersonClassType="SCI"}},
  [4]={Id="NATIONAL_PERCENT",Arguments={Amount=25,GreatPersonClassType="SCI"}},
  [5]={Id="FOREIGN",Arguments={Amount=999,GreatPersonClassType="SCI"}},
  [6]={Id="INACTIVE",Arguments={Amount=999,GreatPersonClassType="SCI"}},
  [7]={Id="UNKNOWN",Arguments={Amount=999,GreatPersonClassType="SCI"}},
  [8]={Id="UNMET",Arguments={Amount=999,GreatPersonClassType="SCI"}}
}
local mods = {
  {ModifierId="DAOGUAN",ModifierType="DISTRICT_FLAT"},
  {ModifierId="CITY_PERCENT",ModifierType="CITY_PERCENT"},
  {ModifierId="POLICY_FLAT",ModifierType="PLAYER_FLAT"},
  {ModifierId="NATIONAL_PERCENT",ModifierType="PLAYER_PERCENT"},
  {ModifierId="FOREIGN",ModifierType="PLAYER_FLAT"},
  {ModifierId="INACTIVE",ModifierType="PLAYER_FLAT"},
  {ModifierId="UNKNOWN",ModifierType="UNKNOWN"},
  {ModifierId="UNMET",ModifierType="PLAYER_FLAT",OwnerRequirementSetId="REQ"}
}
GameInfo = {
  GreatPersonClasses=Rows(classes),Modifiers=Rows(mods),
  Buildings=Rows({{BuildingType="LIBRARY",Index=1,Name="图书馆"},{BuildingType="DAOGUAN_BUILDING",Index=2,Name="道观"}}),
  Districts=Rows({{DistrictType="CAMPUS",Index=1,Name="学院"}}),
  Policies=Rows({{PolicyType="POLICY",Index=1,Name="政策固定点"}})
}
local tables = {
  Building_GreatPersonPoints={{BuildingType="LIBRARY",GreatPersonClassType="SCI",PointsPerTurn=4}},
  District_GreatPersonPoints={{DistrictType="CAMPUS",GreatPersonClassType="SCI",PointsPerTurn=1}},
  District_CitizenGreatPersonPoints={{DistrictType="CAMPUS",GreatPersonClassType="SCI",PointsPerTurn=3}},
  DynamicModifiers={
    {ModifierType="DISTRICT_FLAT",CollectionType="COLLECTION_CITY_DISTRICTS",EffectType="EFFECT_ADJUST_DISTRICT_GREAT_PERSON_POINTS"},
    {ModifierType="CITY_PERCENT",CollectionType="COLLECTION_OWNER",EffectType="EFFECT_ADJUST_CITY_GREAT_PERSON_POINTS_MODIFIER"},
    {ModifierType="PLAYER_FLAT",CollectionType="COLLECTION_OWNER",EffectType="EFFECT_ADJUST_GREAT_PERSON_POINTS"},
    {ModifierType="PLAYER_PERCENT",CollectionType="COLLECTION_OWNER",EffectType="EFFECT_ADJUST_GREAT_PERSON_POINTS_PERCENT"},
    {ModifierType="UNKNOWN",CollectionType="COLLECTION_OWNER",EffectType="EFFECT_NEW_GREAT_PERSON_POINTS"}
  },
  BuildingModifiers={{BuildingType="DAOGUAN_BUILDING",ModifierId="DAOGUAN"}},
  PolicyModifiers={{PolicyType="POLICY",ModifierId="POLICY_FLAT"}}
}
DB = {Query=function(query) return tables[query:match("FROM ([%w_]+)")] or {} end}
local district = {GetID=function() return 10 end,GetType=function() return 1 end,
  IsComplete=function() return true end,GetX=function() return 1 end,GetY=function() return 2 end}
local districts = {Members=function() local n=0; return function() n=n+1; if n==1 then return 1,district end end end,
  HasDistrict=function() return true end,IsPillaged=function() return false end}
local city = {GetID=function() return 1 end,GetOwner=function() return 0 end,GetName=function() return "城市A" end,
  GetDistricts=function() return districts end,GetBuildings=function() return {HasBuilding=function() return true end,IsPillaged=function() return false end} end}
local cityCollection = {Members=function() local n=0; return function() n=n+1; if n==1 then return 1,city end end end}
Players = {[0]={GetCities=function() return cityCollection end,GetGreatPeoplePoints=function() return {GetPointsPerTurn=function() return 34.375 end} end}}
Game = {GetLocalPlayer=function() return 0 end,GetCurrentGameTurn=function() return 65 end}
Map = {GetPlot=function() return {GetIndex=function() return 100 end,GetWorkerCount=function() return 2 end} end}
Locale = {Lookup=function(s) return s end}
local objects = {
  [101]={kind="CITY",owner=0,name="城市A",raw="City: 1, Owner: 0"},
  [102]={kind="DISTRICT",owner=0,name="学院",raw="District: 10, Owner: 0, City: 1"},
  [103]={kind="PLAYER",owner=0,name="玩家",raw="Player: 0"},
  [104]={kind="PLAYER",owner=1,name="其他玩家",raw="Player: 1"}}
local owners = {[1]=101,[2]=101,[3]=103,[4]=103,[5]=104,[6]=103,[7]=103,[8]=103}
GameEffects = {
  GetModifiers=function() return {1,2,3,4,5,6,7,8} end,
  GetModifierDefinition=function(id) return definitions[id] end,
  GetModifierActive=function(id) return id ~= 6 end,
  GetModifierOwner=function(id) return owners[id] end,
  GetModifierSubjects=function(id) return id == 1 and {102,102} or {} end,
  GetObjectType=function(id) return "LOC_MODIFIER_OBJECT_" .. objects[id].kind end,
  GetObjectName=function(id) return objects[id].name end,
  GetObjectString=function(id) return objects[id].raw end,
  GetObjectsPlayerId=function(id) return objects[id].owner end,
  GetModifierOwnerRequirementSet=function() return 900 end,
  GetRequirementSetState=function() return "Unmet" end
}
Controls = setmetatable({}, {__index=function(t,k)
  local c={SetText=function(self,text) self.text=text end,SetHide=function() end,RegisterCallback=function(self,event,callback) self.callback=callback end}
  rawset(t,k,c); return c
end})
ContextPtr = {SetHide=function() end,SetInitHandler=function(self,callback) self.init=callback end,SetShutdown=function() end}
Events = {LoadScreenClose={Add=function() end,Remove=function() end}}
Mouse = {eLClick=1}
fixtureLogs = {}
print = function(s) fixtureLogs[#fixtureLogs+1]=s end
include = function() end -- module was loaded into this Lua state by Python
