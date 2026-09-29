include('RuntimeWork')
include('SpecialistSupport')
-- P0-B1: existing native +3F/+3P carriers at all ACTIVE levels; no III top-up.
SPCResearchSupport={}
function SPCResearchSupport.Start(P,shared)
 local data={ready=false,busy=false,changes=0,errors={},ruleset=SPCSpecialistSupport.RULESET};shared.ResearchSupport=data
 local kinds={'RESEARCH','CULTURE','COMMERCE'}
 local function desired(pid,c,batch)
  local kind,d=SPCSpecialistSupport.Anchor(P,shared,pid,c,batch)
  if kind=='INDUSTRY' then return nil end
  return kind,d
 end
 local function carriers(c,wanted,write)
  local have,plan={},{}
  for _,kind in ipairs(kinds) do
   local row=assert(P.Info('Buildings','BUILDING_SPC_DEV_'..kind..'_SUPPORT'),'B1_SUPPORT_DEFINITION_MISSING')
   local present=P.HasBuilding(c:GetBuildings(),row.Index)
   assert(type(present)=='boolean','B1_SUPPORT_READ_UNKNOWN')
   plan[#plan+1]={kind=kind,id=row.Index,present=present,wanted=kind==wanted}
  end
  if write then
   for _,adding in ipairs({false,true}) do for _,v in ipairs(plan) do
    if v.wanted==adding and v.present~=v.wanted then
     if adding then P.CreateBuilding(c:GetBuildQueue(),v.id) else P.RemoveBuilding(c:GetBuildings(),v.id) end
     assert(P.HasBuilding(c:GetBuildings(),v.id)==v.wanted,'B1_SUPPORT_WRITE_UNCONFIRMED')
     data.changes=data.changes+1;v.present=v.wanted
    end
   end end
  end
  for _,v in ipairs(plan) do if v.present then have[#have+1]=v.kind end end
  return table.concat(have,',')
 end
 function data.Audit(scope)
  if P.Observe then P.Observe('audit','ResearchSupport') end
  if not data.ready or data.busy then P.Count('busy_skip');return end
  data.busy=true;local batch=SPCRuntimeWork.New(P,shared)
  for pid,player in pairs(Players) do if SPCRuntimeWork.Player(scope,pid) then
   local ok,err=pcall(function()
    for _,c in player:GetCities():Members() do
     P.Count('city_scan');local k=pid..':'..c:GetID()
     local good,why=pcall(function()
      SPCSpecialistSupport.Retire(P,c) -- no new support before obsolete IDs cleared
      local kind=desired(pid,c,batch)
      carriers(c,kind,true)
     end)
     data.errors[k]=not good and tostring(why) or nil
    end
   end)
   data.errors['player:'..pid]=not ok and tostring(err) or nil
  end end
  data.busy=false
 end
 function data.Run(pid,c,action)
  local ok,kind,d=pcall(desired,pid,c,SPCRuntimeWork.New(P,shared))
  local known,have=pcall(carriers,c,nil,false)
  return 'P0-B1 '..data.ruleset..' | city='..c:GetID()
   ..'\n基础专家支持 expected='..(ok and (kind or 'NONE') or ('UNKNOWN '..tostring(kind)))
   ..' actual='..(known and have or ('UNKNOWN '..tostring(have)))
   ..'\n科研/文化/商业 ACTIVE1–4每名工作专家额外3F/3P；空槽不产出；原生收益另算。'
   ..'\nchanges='..data.changes..' error='..tostring(data.errors[pid..':'..c:GetID()] or 'NONE')
   ..'\nRead only; ON/OFF aliases cannot enable the retired III upgrade.'
 end
 local function hook(source,n,fn) local e=P.Field(source,n);if e and e.Add then e.Add(fn) end end
 hook(Events,'LoadScreenClose',function() data.ready=true;data.errors={};data.Audit() end)
 for _,n in ipairs({'PlayerTurnActivated','CityTransfered','DistrictRemovedFromMap','DistrictBuildProgressChanged',
  'GovernorAssigned','GovernorChanged','GovernorEstablished','GovernorPromoted','DistrictPillaged','DistrictRepaired'}) do
  SPCRuntimeWork.Hook(P,Events,n,data.Audit)
 end
 for _,n in ipairs({'OnDistrictConstructed','CityBuilt','OnPillage'}) do hook(GameEvents,n,data.Audit) end
 -- E2 confirmed exit: exact transient IDs owned by this writer; no prefix scan.
 if shared.CityProgressionStore then shared.CityProgressionStore.RegisterExit('ResearchSupport',function(c,loss)
   local ids={};for _,k in ipairs(kinds)do ids[#ids+1]='BUILDING_SPC_DEV_'..k..'_SUPPORT'end
   shared.CityProgressionStore.RemoveOwned(c,loss,ids)
 end)end

end
