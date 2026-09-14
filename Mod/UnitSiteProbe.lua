-- B040 read-only Gameplay location diagnostics. No grants, consumption or writes.
SPCUnitSiteProbe={}
function SPCUnitSiteProbe.Start(P,shared)
 local data={};shared.UnitSiteProbe=data
 function data.Read(pid,id)
  local ok,out=pcall(function()
   assert(P.IsTestPlayer(pid),'TEST_PLAYER_REQUIRED')
   assert(type(id)=='number' and id>=0 and id%1==0,'SELECT_UNIT')
   local unit=Players[pid]:GetUnits():FindID(id)
   assert(unit and unit:GetOwner()==pid,'UNIT_MISSING')
   local plot=Map.GetPlot(unit:GetX(),unit:GetY());assert(plot,'PLOT_UNKNOWN')
   local info=P.Info('Units',unit:GetType());assert(info,'UNIT_TYPE_UNKNOWN')
   local lines={'B040 READ ONLY | '..info.UnitType..' #'..id,
    'Unit plot='..plot:GetIndex()..' ('..unit:GetX()..','..unit:GetY()..')'}
   assert(plot:GetOwner()==pid,'OWN_CITY_PLOT_REQUIRED')
   local city=Cities.GetPlotPurchaseCity(plot)
   assert(city and city:GetOwner()==pid,'CITY_UNKNOWN')
   lines[#lines+1]='City='..city:GetName()..' #'..city:GetID()
   local districts={}
   for _,d in Players[pid]:GetDistricts():Members() do P.Count('district_scan');
    local c=d:GetCity()
    if c and c:GetOwner()==pid and c:GetID()==city:GetID() then districts[#districts+1]=d end
   end
   local function result(name,fn)
    local good,value=pcall(fn)
    lines[#lines+1]=name..': '..(good and value or ('UNKNOWN '..tostring(value):match('[^\r\n]+')))
   end
   result('Investment candidate',function()
    local f=shared.EffectiveFacts.Read(pid,city)
    if not f.first or f.specialization=='NONE' then return 'NO SPECIALIZATION' end
    for _,d in ipairs(districts) do
     local di=P.Info('Districts',d:GetType())
     if d:GetID()==f.first.districtID and di and di.DistrictType==f.first.type then
      local target={verified=true,owner=pid,cityID=city:GetID(),plot=Map.GetPlot(d:GetX(),d:GetY()):GetIndex(),
       kind='DISTRICT',complete=d:IsComplete(),identityAnchor=true,potential=f.potential}
      local yes,reason=SPCUnitActionSitePolicy.Check('INVESTMENT',{owner=pid,plot=plot:GetIndex(),isSettler=info.UnitType=='UNIT_SETTLER'},target)
      return (yes and 'SITE OK' or reason)..' | '..f.specialization..' P'..f.potential..' target=('..d:GetX()..','..d:GetY()..')'
     end
    end
    return 'IDENTITY DISTRICT MISSING'
   end)
   result('Construction candidate',function()
    local current=city:GetBuildQueue():CurrentlyBuilding()
    local building=P.Info('Buildings',current);local district=P.Info('Districts',current)
    if not building and not district then return 'NO BUILDING / DISTRICT / WONDER TARGET' end
    local targetPlot,kind,complete,source
    if building and building.IsWonder then
     kind='WONDER';complete=P.HasBuilding(city:GetBuildings(),building.Index)
     -- HD placed-wonder marker is cross-checked against the current queue and
     -- actual wonder district on this plot; never accepted by itself.
     local wonder=P.Info('Districts','DISTRICT_WONDER')
     if wonder and plot:GetDistrictType()==wonder.Index and plot:GetProperty('HD_UNCOMPLETED_WONDER')==building.Index then
      targetPlot=plot;source='HD marker + current queue + wonder plot'
     else return 'NOT VERIFIED AT THIS PLOT | '..tostring(current) end
    else
     kind=building and 'BUILDING' or 'DISTRICT'
     local expected=building and building.PrereqDistrict or district.DistrictType
     for _,d in ipairs(districts) do
      local di=P.Info('Districts',d:GetType())
      if di and di.DistrictType==expected then
       assert(not targetPlot,'AMBIGUOUS_DISTRICT')
       targetPlot=Map.GetPlot(d:GetX(),d:GetY())
       complete=building and P.HasBuilding(city:GetBuildings(),building.Index) or d:IsComplete()
       if building then complete=P.HasBuilding(city:GetBuildings(),building.Index) end
      end
     end
     source='Gameplay district coordinates'
    end
    assert(targetPlot,'TARGET_LOCATION_UNKNOWN')
    local yes,reason=SPCUnitActionSitePolicy.Check('CREW',{owner=pid,plot=plot:GetIndex(),isCrew=true,charges=1},
     {verified=true,owner=pid,cityID=city:GetID(),plot=targetPlot:GetIndex(),kind=kind,current=true,complete=complete})
    return (yes and 'SITE OK (location only)' or reason)..' | '..tostring(current)..' target=('
     ..targetPlot:GetX()..','..targetPlot:GetY()..')\nSource='..source
   end)
   lines[#lines+1]=(info.UnitType=='UNIT_SPC_CREW_250' and ('Crew 250 | charges='..unit:GetBuildCharges()..'. Use Prepare / Confirm unit action.') or 'No action executed. Builder is a location tester, not a Crew.')
   lines[#lines+1]='Existing investment still uses city center. Candidate site rules only.'
   return table.concat(lines,'\n')
  end)
  return ok and out or ('B040 UNKNOWN / UNAVAILABLE: '..tostring(out):match('[^\r\n]+'))
 end
end
