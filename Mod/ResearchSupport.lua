include('RuntimeWork')
include('SpecialistSupport')
-- P0-B1: existing native +3F/+3P carriers at all ACTIVE levels; no III top-up.
SPCResearchSupport={}
function SPCResearchSupport.Start(P,shared)
 local batch
 local data={ready=false,busy=false,changes=0,errors={},ruleset=SPCSpecialistSupport.RULESET};shared.ResearchSupport=data
 local kinds={'RESEARCH','CULTURE','COMMERCE'}
 local definitions;local ownedIndex={}
 local health=SPCRuntimeWork.NativeHealth(P,shared,data,function(id)return ownedIndex[id]==true end,function(scope)data.MarkAudit(scope)end)
 local function validate()
  if definitions then return definitions end
  local rows,nextOwned={},{}
  for _,kind in ipairs(kinds)do
   local id=assert(P.Info('Buildings','BUILDING_SPC_DEV_'..kind..'_SUPPORT'),'B1_SUPPORT_DEFINITION_MISSING').Index
   rows[kind]=id;nextOwned[id]=true
  end
  definitions=rows;ownedIndex=nextOwned;return rows
 end
 local function desired(pid,c,batch)
  local kind,d=SPCSpecialistSupport.Anchor(P,shared,pid,c,batch)
  if kind=='INDUSTRY' then return nil end
  return kind,d
 end
 local function carriers(c,wanted,write)
  local have,plan={},{}
  for _,kind in ipairs(kinds) do
   local id=validate()[kind]
   local present=P.HasBuilding(c:GetBuildings(),id)
   assert(type(present)=='boolean','B1_SUPPORT_READ_UNKNOWN')
   plan[#plan+1]={kind=kind,id=id,present=present,wanted=kind==wanted}
  end
  if write then
   for _,adding in ipairs({false,true}) do for _,v in ipairs(plan) do
    if v.wanted==adding and v.present~=v.wanted then
     if adding then health.Create(c,v.id) else health.Remove(c,v.id) end
     assert(P.HasBuilding(c:GetBuildings(),v.id)==v.wanted,'B1_SUPPORT_WRITE_UNCONFIRMED')
     data.changes=data.changes+1;v.present=v.wanted
    end
   end end
  end
  for _,v in ipairs(plan) do if v.present then have[#have+1]=v.kind end end
  return table.concat(have,',')
 end
 local targets=SPCRuntimeWork.NewTargets(P,shared,function(pid,c)
  SPCSpecialistSupport.Retire(P,c,shared);local kind=desired(pid,c,batch);carriers(c,kind,true)
 end,function(pid,cid,why)data.errors[tostring(pid)..':'..cid]=why end)
 local function audit(scope)
  local ok,err=pcall(function()validate();batch=SPCRuntimeWork.New(P,shared);targets.Run(scope)end)
  batch=nil;if not ok then error(err,0)end
 end
 data.Audit,data.MarkAudit,data.FlushAudit=SPCRuntimeWork.NewAudit(P,shared,data,'ResearchSupport',audit,{targets=true})
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
 SPCRuntimeWork.StartReady(P,shared,'ResearchSupport',function() data.ready=true;data.errors={};data.Audit({load=true})end)
 for _,n in ipairs({'PlayerTurnActivated','CityTransfered'})do SPCRuntimeWork.TargetHook(P,Events,n,data.Audit)end
 if not shared.DistrictCompleteness then
  for _,n in ipairs({'DistrictRemovedFromMap','DistrictBuildProgressChanged','DistrictPillaged','DistrictRepaired'})do SPCRuntimeWork.TargetHook(P,Events,n,data.Audit)end
  for _,n in ipairs({'OnDistrictConstructed','CityBuilt','OnPillage'})do SPCRuntimeWork.TargetHook(P,GameEvents,n,data.Audit)end
 end
 -- E2 confirmed exit: exact transient IDs owned by this writer; no prefix scan.
 if shared.CityProgressionStore then shared.CityProgressionStore.RegisterExit('ResearchSupport',targets.Exit(function(c,loss)
   local ids={};for _,k in ipairs(kinds)do ids[#ids+1]='BUILDING_SPC_DEV_'..k..'_SUPPORT'end
   shared.CityProgressionStore.RemoveOwned(c,loss,ids)
 end))end

end
