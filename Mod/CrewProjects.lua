-- B044 derived access only. The engine completes projects and grants units; no Lua grant replay.
SPCCrewProjects={}
function SPCCrewProjects.Start(P,shared)
 local data={ready=false,busy=false,errors={}};shared.CrewProjects=data
 local function eligible(pid,c)
  if not P.IsTestPlayer(pid) or c:GetOwner()~=pid then return false end
  local f=shared.EffectiveFacts.Read(pid,c)
  if f.specialization~='INDUSTRY' then return false end
  assert(f.potential>=1 and f.first,'INDUSTRY_FACT_INVALID')
  for _,d in Players[pid]:GetDistricts():Members() do P.Count('district_scan');
   local dc=d:GetCity();local row=P.Info('Districts',d:GetType())
   if dc and dc:GetOwner()==pid and dc:GetID()==c:GetID() and d:GetID()==f.first.districtID then
    return row and row.DistrictType=='DISTRICT_INDUSTRIAL_ZONE' and f.first.type==row.DistrictType and d:IsComplete()==true
   end
  end
  return false
 end
 function data.Audit()
  if not data.ready or data.busy then P.Count('busy_skip');return end;data.busy=true
  local row=P.Info('Buildings','BUILDING_SPC_CREW_PROJECT_ACCESS')
  if not row or not row.Index then data.busy=false;print('[SPC][B044] PROJECT_DATABASE_MISSING');return end
  for pid,player in pairs(Players) do
   local ok,err=pcall(function()
    local cities=player:GetCities();if not cities then return end
    for _,c in cities:Members() do P.Count('city_scan');
     local b=c:GetBuildings();local present=P.HasBuilding(b,row.Index)
     -- Non-participants pay only the marker-removal check, no specialization reads.
     if P.IsTestPlayer(pid) or present then
      local valid,wanted=pcall(eligible,pid,c);local key=pid..':'..c:GetID()
      data.errors[key]=not valid and tostring(wanted) or nil
      wanted=valid and wanted==true
      if present~=wanted then
       if wanted then P.CreateBuilding(c:GetBuildQueue(),row.Index) else P.RemoveBuilding(b,row.Index) end
       assert(P.HasBuilding(b,row.Index)==wanted,'PROJECT_ACCESS_WRITE_UNCONFIRMED')
      end
      if data.errors[key] then print('[SPC][B044] '..key..' '..data.errors[key]) end
     end
    end
   end)
   if not ok then print('[SPC][B044] PROJECT_ACCESS_SCAN_ERROR '..tostring(err)) end
  end
  data.busy=false
 end
 local function hook(source,n,fn) local e=P.Field(source,n);if e and e.Add then e.Add(fn) end end
 hook(Events,'LoadScreenClose',function() data.ready=true;data.Audit() end)
 for _,n in ipairs({'PlayerTurnActivated','CityTransfered','DistrictBuildProgressChanged','DistrictRemovedFromMap','CityProductionCompleted'}) do hook(Events,n,data.Audit) end
 for _,n in ipairs({'OnDistrictConstructed','OnBuildingConstructed','CityBuilt'}) do hook(GameEvents,n,data.Audit) end
end
