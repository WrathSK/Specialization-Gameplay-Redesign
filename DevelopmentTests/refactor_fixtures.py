"""Synthetic native data with the real D service; catalogue ontology is an explicit stub."""
from refactor_harness import Context

def depth_context(cities=2, definitions=4):
    c=Context()
    c.execute(r"""
P={Field=function(t,k)return t and t[k]end,IsTestPlayer=function(pid)return pid==0 end,
 Count=function(k,n)counts[k]=(counts[k]or 0)+(n or 1)end}
rows={};for i=1,... do rows[i]={index=i,type='BUILDING_TEST_'..i,name='LOC_TEST_'..i,
 domain='DISTRICT_CAMPUS',ordinary=true,tier=1,depthEligible=true,ordinaryDistrict='DISTRICT_CAMPUS'}end
SPCOrdinaryBuildingCatalog={Build=function()return {revision=1,buildings=rows,Domain=function(t)return t end}end}
P.Info=function(tab,index)
 if tab=='Districts'then return {Index=1,DistrictType='DISTRICT_CAMPUS'}end
 if index==1 then return {Index=1,BuildingType='BUILDING_TEST_1'}end
end
Map={GetPlot=function(x,y)return {GetIndex=function()return x*100+y end}end}
cities={};Players={}
function addCity(id)
 local c={id=id,owner=0,token='REF:'..id,present={[1]=true}}
 c.GetOwner=function()return c.owner end;c.GetID=function()return c.id end
 c.GetX=function()return c.id end;c.GetY=function()return 0 end
 c.GetBuildings=function()return {
  HasBuilding=function(_,i)return c.present[i]==true end,
  IsPillaged=function()return false end,GetBuildingLocation=function()return c.id*100 end}end
 local d={GetID=function()return c.id end,GetType=function()return 1 end,
  GetX=c.GetX,GetY=c.GetY,GetCity=function()return c end,
  IsComplete=function()return true end,IsPillaged=function()return false end}
 c.GetDistricts=function()return {GetNumDistricts=function()return 1 end,GetDistrictByIndex=function()return d end}end
 c.GetBuildQueue=function()return {CurrentlyBuilding=function()return 0 end}end
 cities[id]=c;return c
end
function sample(id,detail)
 local c=cities[id];if detail then return shared.DistrictCompleteness.Read(0,c,c.token)end
 return shared.DistrictCompleteness.ReadFacts(0,c,c.token)
end
function resetCounts()counts={}end
""",definitions)
    c.execute('for i=1,... do addCity(i)end',cities)
    c.load('DistrictCompleteness');c.execute('SPCDistrictCompleteness.Start(P,shared)')
    return c
