-- B041: target enumeration, derived read-only data. Not authority to consume units.
SPCUnitTargets={}
function SPCUnitTargets.Start(P,shared)
 local data={};shared.UnitTargets=data
 function data.Refresh(pid,params)
  local response={token=params.Token,owner=pid,unitID=params.UnitID,plots={},unknown={},version=P.VERSION}
  local ok,err=pcall(function()
   assert(P.IsTestPlayer(pid),'TEST_PLAYER_REQUIRED')
   local u=Players[pid]:GetUnits():FindID(params.UnitID);assert(u and u:GetOwner()==pid,'UNIT_MISSING')
   local row=P.Info('Units',u:GetType());assert(row,'UNIT_TYPE_UNKNOWN')
   local invest=row.UnitType=='UNIT_SETTLER'
   assert(invest or P.CrewBase(row.UnitType)~=nil or (row.UnitType=='UNIT_BUILDER' and params.BuilderPreview==true),'UNIT_NOT_ENABLED')
   response.mode=invest and 'INVEST' or (P.CrewBase(row.UnitType)~=nil and 'BUILD' or 'BUILD TEST')
   local districts={}
   for _,d in Players[pid]:GetDistricts():Members() do P.Count('district_scan');
    local c=d:GetCity()
    if c and c:GetOwner()==pid then
     local id=c:GetID();districts[id]=districts[id] or {};table.insert(districts[id],d)
    end
   end
   local seen={}
   for _,c in Players[pid]:GetCities():Members() do P.Count('city_scan');
    local good,value=pcall(function()
     assert(c:GetOwner()==pid,'OWNER_CHANGED')
     local candidates={};local ds=districts[c:GetID()] or {}
     if invest then
      local f=shared.EffectiveFacts.Read(pid,c)
      if f.specialization=='NONE' or f.investmentPending or f.potential>=4 then return nil end
      assert(f.first and f.potential>=1,'INVESTMENT_UNKNOWN')
      for _,d in ipairs(ds) do
       local di=P.Info('Districts',d:GetType())
       if d:GetID()==f.first.districtID and di and di.DistrictType==f.first.type and d:IsComplete() then
        candidates[#candidates+1]=Map.GetPlot(d:GetX(),d:GetY())
       end
      end
     else
      local current=c:GetBuildQueue():CurrentlyBuilding()
      local b=P.Info('Buildings',current);local dr=P.Info('Districts',current)
      if not b and not dr then return nil end
      if b and P.HasBuilding(c:GetBuildings(),b.Index) then return nil end
      if b and b.IsWonder then
       local wi=P.Info('Districts','DISTRICT_WONDER');assert(wi,'WONDER_TYPE_UNKNOWN')
       local utils=ExposedMembers.DLHD and ExposedMembers.DLHD.Utils
       assert(utils and type(utils.GetCityPlots)=='function','HD_CITY_PLOTS_HELPER_UNAVAILABLE')
       local indexes=utils.GetCityPlots(pid,c:GetID())
       assert(type(indexes)=='table','HD_CITY_PLOTS_LIST_UNKNOWN')
       local scanned={}
       for _,index in pairs(indexes) do
        assert(type(index)=='number' and index>=0 and index%1==0,'CITY_PLOT_INDEX_INVALID')
        local p=Map.GetPlotByIndex(index)
        if not scanned[index] and p and p:GetOwner()==pid and p:GetDistrictType()==wi.Index and p:GetProperty('HD_UNCOMPLETED_WONDER')==b.Index then
         local pc=Cities.GetPlotPurchaseCity(p)
         if pc and pc:GetOwner()==pid and pc:GetID()==c:GetID() then candidates[#candidates+1]=p;scanned[index]=true end
        end
       end
      else
       local expected=b and b.PrereqDistrict or dr.DistrictType
       for _,d in ipairs(ds) do
        local di=P.Info('Districts',d:GetType())
        if di and di.DistrictType==expected and ((b and d:IsComplete()) or (not b and not d:IsComplete())) then
         candidates[#candidates+1]=Map.GetPlot(d:GetX(),d:GetY())
        end
       end
      end
      assert(current==c:GetBuildQueue():CurrentlyBuilding(),'QUEUE_CHANGED')
     end
     assert(#candidates==1,'TARGET_LOCATION_UNKNOWN_OR_AMBIGUOUS')
     local p=candidates[1];assert(p and p:GetOwner()==pid,'TARGET_OWNER_UNKNOWN')
     return {plot=p:GetIndex(),cityID=c:GetID(),cityName=c:GetName()}
    end)
    if good and value and not seen[value.plot] then seen[value.plot]=true;response.plots[#response.plots+1]=value
    elseif not good then response.unknown[#response.unknown+1]={cityID=c:GetID(),reason=tostring(value):match('[^\r\n]+')} end
   end
   table.sort(response.plots,function(a,b) return a.plot<b.plot end)
  end)
  if not ok then response.plots={};response.error=tostring(err):match('[^\r\n]+') end
  shared.UnitTargetSnapshot=response
 end
end
