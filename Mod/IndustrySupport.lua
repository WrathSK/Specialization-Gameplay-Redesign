include('RuntimeWork')
include('SampleLifecycle')
include('SpecialistSupport')
-- B036 IND-001: native per-specialist Food + base Production adjacency.
-- No actual-adjacency fallback, rounding or city-wide multiplication. Crew access is independently audited.
SPCIndustrySupport={}
function SPCIndustrySupport.Start(P,shared)
 local batch
 local pending={} -- one current reference per affected city, cleared on success/loss/load
 local data={ready=false,busy=false,changes=0,errors={}};shared.IndustrySupport=data
 SPCSampleLifecycle.Reset(data,'industry')
 local trace=SPCExpeditionTrainingDiagnostics and SPCExpeditionTrainingDiagnostics.New(P,'INDUSTRY_SUPPORT')
 local function key(pid,cid)return tostring(pid)..':'..tostring(cid)end
 local function reference(c)return table.concat({c:GetOwner(),c:GetID(),c:GetX(),c:GetY(),tostring(c:GetProperty('SPC_DEV_BINDING_B013_TOKEN'))},':')end
 local function name(bit) return 'BUILDING_SPC_DEV_INDUSTRY_LV1_'..bit end
 local function inspect(pid,city,externalBatch)
  local kind,d=SPCSpecialistSupport.Anchor(P,shared,pid,city,externalBatch or batch or SPCRuntimeWork.New(P,shared))
  if kind~='INDUSTRY' then return nil end
  local row=assert(P.Info('Districts',d:GetType()),'INDUSTRY_FACT_INVALID')
  local batch=data.samples[pid];local sample=batch and batch.rows[city:GetID()..':'..d:GetID()]
  assert(sample,'BASE_BACKGROUND_SAMPLE_PENDING')
  assert(sample.reference==SPCSampleLifecycle.Reference(city,d,row),'BASE_BACKGROUND_REFERENCE_PENDING')
  local n=sample.value
  assert(type(n)=='number' and n>=0 and n<=255 and n%1==0,'BASE_ADJACENCY_UNKNOWN_FRACTIONAL_OR_OUT_OF_RANGE')
  return n
 end
 local function carriers(city,n,write)
  local total,food=0,0;local removed=false
  for bit=-1,7 do
   local row=P.Info('Buildings',name(bit));assert(row and row.Index,'B036_DATABASE_MISSING: restart/new test game required')
   local wanted=n~=nil and (bit==-1 or math.floor(n/2^bit)%2==1)
   local b=city:GetBuildings();local present=P.HasBuilding(b,row.Index)
   assert(type(present)=='boolean','CARRIER_READ_UNKNOWN')
   if write and present~=wanted then
    if wanted then P.CreateBuilding(city:GetBuildQueue(),row.Index) else P.RemoveBuilding(b,row.Index);removed=true end
    assert(P.HasBuilding(b,row.Index)==wanted,'CARRIER_WRITE_UNCONFIRMED')
    data.changes=data.changes+1;present=wanted
   end
   if present then if bit==-1 then food=3 else total=total+2^bit end end
  end
  if removed and n==nil then P.Count('industry_withdraw') end
  return total,food
 end
 local function startReady()
  if data.ready then return true end
  local store=shared.CityProgressionStore
  if store and store.HistoryStartStatus and store.HistoryStartStatus()=='WAITING'then return false end
  data.ready=true;return true
 end
 function data.MarkCity(c)
  if not c or not P.IsTestPlayer(c:GetOwner())then return end
  pending[key(c:GetOwner(),c:GetID())]={player=c:GetOwner(),city=c:GetID(),reference=reference(c)}
 end
 local targets=SPCRuntimeWork.NewTargets(P,shared,function(pid,c)
  local before=data.changes;local n=inspect(pid,c)
  SPCSpecialistSupport.Retire(P,c,shared);carriers(c,n,true)
  local k=pid..':'..c:GetID();local waiting=pending[k]
  local f=waiting and P.IsTestPlayer(pid) and batch.Facts(pid,c) or {specialization='EXIT'}
  if n~=nil or f.specialization~='NONE' or not waiting or reference(c)~=waiting.reference then pending[k]=nil end
  if trace and data.changes~=before then trace.Record('INDUSTRY_SUPPORT',{owner=pid,city=c:GetID(),expected=n or 0,wanted=n~=nil and 'FOOD_3_PLUS_BASE_PRODUCTION' or 'NONE',readStatus='VERIFIED'})end
 end,function(pid,cid,why)data.errors[tostring(pid)..':'..cid]=why;local p=Players[pid];local c=why and P.IsTestPlayer(pid) and p and p:GetCities():FindID(cid);if c then data.MarkCity(c)end end)
 function data.Audit(scope)
  if P.Observe then P.Observe('audit','IndustrySupport') end
  if not startReady() or data.busy then P.Count('busy_skip');return end;data.busy=true;batch=SPCRuntimeWork.New(P,shared)
  targets.Run(scope)
  data.busy=false;batch=nil
 end
 function data.FlushPending(pid)
  if data.busy or not startReady() then return end
  local todo={};for k,v in pairs(pending)do if pid==nil or pid==v.player then todo[k]=v end end
  for k,v in pairs(todo)do
   local player=Players[v.player];local c=player and player:GetCities():FindID(v.city)
   if not c or c:GetOwner()~=v.player or reference(c)~=v.reference then pending[k]=nil
   else data.Audit({player=v.player,city=v.city})end
  end
 end
 function data.BindPermanentWrites()
  local previous=shared.OnPermanentCityWrite
  shared.OnPermanentCityWrite=function(c,reason)
   if previous then previous(c,reason)end
   if reason=='CityProgressionStore.lua' or reason=='ClaimProjects.lua'then data.MarkCity(c)end
  end
 end
 data.ReadBase=inspect
 function data.Receive(pid,params)
  if SPCSampleLifecycle.Receive(P,data,'industry',pid,params,true) then
   data.Audit({player=pid})
  else data.FlushPending(pid) end
 end
 function data.Describe(pid,city)
  local bg=ExposedMembers.SPC_IndustryBackground
  local ok,n=pcall(inspect,pid,city)
  local valid,p,f=pcall(carriers,city,nil,false)
  return 'P0-B1 Industry ACTIVE1–4 city='..city:GetID()
   ..'\nBASE Production adjacency='..(ok and tostring(n or 'N/A') or 'ERROR '..tostring(n))
   ..'\nPer worker expected='..(ok and n~=nil and ('3F / '..n..'P') or 'NONE')
   ..' carrier='..(valid and (f..'F / '..p..'P') or ('ERROR '..tostring(p)))
   ..'\nbackground='..tostring(bg and bg.state or 'NOT_STARTED')..' pending='..tostring(bg and bg.pending or 0)..' requests='..tostring(bg and bg.requests or 0)
   ..' receive='..tostring(data.receiveErrors and data.receiveErrors[pid] or 'NONE')
   ..'\nchanges='..data.changes..' error='..tostring(data.errors[pid..':'..city:GetID()] or 'NONE')
   ..'\nRead only; verify native specialist yields. Native district yields are additional; retired III Food/Gold upgrade cannot reactivate.'
 end
 local function hook(source,name,fn) local e=P.Field(source,name);if e and e.Add then e.Add(fn) end end
 hook(Events,'LoadScreenClose',function() pending={};data.ready=true;SPCSampleLifecycle.Reset(data,'industry');data.Audit({load=true}) end)
 hook(Events,'GameCoreEventPublishComplete',function()data.FlushPending()end)
 hook(GameEvents,'OnDistrictConstructed',function(pid,index,x,y)
  local r=P.Info('Districts',index)
  if not r or P.Family(r.DistrictType)~='INDUSTRY' or not P.IsTestPlayer(pid)then return end
  local district=CityManager.GetDistrictAt(x,y);local c=district and district:GetCity()
  if c and c:GetOwner()==pid and district:GetType()==index then data.MarkCity(c);data.FlushPending(pid)end
 end)
 for _,n in ipairs({'PlayerTurnActivated','CityTransfered','DistrictAddedToMap','DistrictRemovedFromMap','DistrictBuildProgressChanged','ImprovementAddedToMap','ImprovementRemovedFromMap','FeatureRemovedFromMap','GovernorAssigned','GovernorChanged','GovernorEstablished','GovernorPromoted','DistrictPillaged','DistrictRepaired'}) do SPCRuntimeWork.TargetHook(P,Events,n,data.Audit) end
 for _,n in ipairs({'OnDistrictConstructed','OnBuildingConstructed','CityBuilt','OnPillage'}) do SPCRuntimeWork.TargetHook(P,GameEvents,n,data.Audit) end
 -- E2 confirmed exit: exact transient IDs owned by this writer; no prefix scan.
 if shared.CityProgressionStore then shared.CityProgressionStore.RegisterExit('IndustrySupport',targets.Exit(function(c,loss)
   local ids={};for bit=-1,7 do ids[#ids+1]=name(bit)end
   shared.CityProgressionStore.RemoveOwned(c,loss,ids)
   pending[key(loss.origin.owner,loss.origin.cityID)]=nil;pending[key(c:GetOwner(),c:GetID())]=nil
 end))end

 if shared.CityProgressionStore then shared.CityProgressionStore.RegisterReturn('IndustrySupport',function(pid)SPCSampleLifecycle.Reset(data,'industry');data.last={} end)end

end
