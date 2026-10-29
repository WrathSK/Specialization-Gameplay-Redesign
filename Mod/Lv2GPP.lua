-- B394 optional observer: deleting/disabling its module leaves this tap inert.
pcall(include,'CultureDiagnostics')
local function cultureObserve(point,build)
 pcall(function()
  local d=SPCCultureDiagnostics
  if d and d.ENABLED then d.Emit('CULTURE_GP',point,build)end
 end)
end
include('RuntimeWork')
include('SpecialistSupport')
include('CarrierSet')
-- B035: working-specialist count -> native building base GPP. No ChangePointsTotal.
SPCLv2GPP={}
function SPCLv2GPP.Start(P,shared)
 local batch
 local data={ready=false,busy=false,changes=0,refreshes=0,errors={}};shared.Lv2GPP=data
 local kinds={"RESEARCH","CULTURE","INDUSTRY","COMMERCE"}
 local districts={RESEARCH="DISTRICT_CAMPUS",CULTURE="DISTRICT_THEATER",INDUSTRY="DISTRICT_INDUSTRIAL_ZONE",COMMERCE="DISTRICT_COMMERCIAL_HUB"}
 local classes={RESEARCH={"SCIENTIST"},CULTURE={"WRITER","ARTIST","MUSICIAN"},INDUSTRY={"ENGINEER"},COMMERCE={"MERCHANT"}}
 local definitions
 local function int(v) return type(v)=="number" and v>=0 and v%1==0 and v<math.huge end
 local function name(kind,bit) return "BUILDING_SPC_DEV_GPP_"..kind.."_"..bit end
 local entries={};for _,kind in ipairs(kinds)do for bit=0,7 do local key=name(kind,bit);entries[#entries+1]={key=key,name=key}end end
 local carriersSet=SPCCarrierSet.Define(P,entries,function(key)return assert(P.Info('Buildings',key),'B035_BUILDING_DATABASE_MISMATCH '..key).Index end,
  {read='GPP_CARRIER_READ_UNKNOWN',write='GPP_CARRIER_CHANGE_UNCONFIRMED'})
 local health=SPCRuntimeWork.NativeHealth(P,shared,data,carriersSet.Owns,function(scope)data.MarkAudit(scope)end)
 local function validateDefinitions()
  if definitions then return end
  local rows=P.Rows("Building_GreatPersonPoints");assert(rows,"GPP_DATABASE_UNAVAILABLE")
  for _,kind in ipairs(kinds) do for bit=0,7 do
   local building=name(kind,bit);local b=P.Info("Buildings",building)
   assert(b and type(b.Index)=="number" and b.PrereqDistrict==districts[kind] and b.Housing==0 and b.CitizenSlots==0,"B035_BUILDING_DATABASE_MISMATCH "..building)
   local expected={};for _,cl in ipairs(classes[kind]) do expected["GREAT_PERSON_CLASS_"..cl]=true end
   local seen={}
   for _,r in ipairs(rows) do if r.BuildingType==building then
    assert(expected[r.GreatPersonClassType] and not seen[r.GreatPersonClassType] and r.PointsPerTurn==2*2^bit,"B035_BASE_GPP_DATABASE_MISMATCH "..building)
    seen[r.GreatPersonClassType]=true
   end end
   for cl in pairs(expected) do assert(seen[cl],"B035_GPP_DEFINITION_MISSING "..building) end
  end end
  carriersSet.Initialize();definitions=true
 end
 local function inspect(pid,city,observed)
  return SPCSpecialistSupport.Inspect(P,shared,pid,city,batch or SPCRuntimeWork.New(P,shared),function(kind,d,f,workers,geometry)
  if observed then pcall(observed,d and d.cityID or f and f.cityID)end -- diagnostic-only scalar, never eligibility
  if not classes[kind] then return {workers=0,enabled=false,reason='CONFIRMED_INELIGIBLE'} end
  if f.active<2 then return {kind=kind,active=f.active,workers=0,enabled=false,reason='ACTIVE_BELOW_II'} end
  local g=geometry();local plot=assert(Map.GetPlot(g.x,g.y),'B2_GPP_PLOT_UNAVAILABLE')
  local function read()local n=plot:GetWorkerCount();assert(int(n)and n<=255,'WORKER_COUNT_UNKNOWN_OR_UNSUPPORTED');return n end
  local n
  if type(plot.GetIndex)=='function'then n=workers({id=d.id,type=d.type,plot=plot:GetIndex()},read)else n=read()end
  assert(int(n)and n<=255,'WORKER_COUNT_UNKNOWN_OR_UNSUPPORTED')
  cultureObserve('GPP_SAMPLE',function()return {owner=pid,city=d.cityID or f.cityID or 'UNKNOWN',specialization=kind,active=f.active,workers=n,reason=observed and 'AUDIT'or 'READ_ONLY'}end)
  return {kind=kind,workers=n,active=f.active,enabled=true,reason='VERIFIED anchor='..d.id}
  end)
 end

 local function reconcile(pid,city)
  local observedCity
  validateDefinitions();local f=inspect(pid,city,function(id)observedCity=id end)
  local n=f.enabled and f.workers or 0
  local kind=f.kind
  local wanted={}
  for _,k in ipairs(kinds) do for bit=0,7 do
   wanted[name(k,bit)]=k==kind and math.floor(n/2^bit)%2==1
  end end
  -- Full presence preflight, then original fresh changed-bit read and readback.
  local plan=carriersSet.Apply(city,wanted,health,function()data.changes=data.changes+1 end,true)
  cultureObserve('GPP_APPLIED',function()
   local actual,other=0,0
   for _,v in ipairs(plan)do
    local k,bit=v.key:match('^BUILDING_SPC_DEV_GPP_(%u+)_(%d+)$')
    if v.present then if k==kind then actual=actual+2*2^tonumber(bit)else other=other+2*2^tonumber(bit)end end
   end
   return {owner=pid,city=observedCity or 'UNKNOWN',specialization=kind,workers=n,expectedNumber=2*n,actualNumber=actual,
    count=other,readStatus='PREFLIGHT_AND_CHANGED_READBACK'}
  end)
 end
 local targets=SPCRuntimeWork.NewTargets(P,shared,function(pid,c)
  reconcile(pid,c)
 end,function(pid,cid,why)data.errors[tostring(pid)..':'..cid]=why;cultureObserve('GPP_FAILED',function()local e=SPCCultureDiagnostics.Error(why);e.owner=pid;e.city=cid;return e end)end)
 local function runAudit(scope)
  validateDefinitions()
  batch=SPCRuntimeWork.New(P,shared);data.refreshes=data.refreshes+1
  if type(scope)=='table' and scope.investment~=nil then
   local pid=scope.player;local key='investment:'..tostring(pid)
   local ok,city=pcall(SPCRuntimeWork.InvestmentCity,P,shared,scope,batch)
   data.errors[key]=not ok and tostring(city) or nil
   if ok then
    P.Count('city_scan');local good,why=pcall(function() reconcile(pid,city) end)
    data.errors[pid..':'..city:GetID()]=not good and tostring(why) or nil
   end
   return
  end
  if type(scope)~='table' or scope.player==nil then data.errors={} end
  targets.Run(scope)
 end
 local function audit(scope)
  local ok,err=pcall(runAudit,scope);batch=nil;if not ok then error(err,0)end
 end
 data.Audit,data.MarkAudit,data.FlushAudit=SPCRuntimeWork.NewAudit(P,shared,data,'Lv2GPP',audit,{targets=true})
 function data.Describe(pid,city)
  local ok,result=pcall(function()
   assert(data.ready,"GPP_NOT_READY");validateDefinitions()
   local f=inspect(pid,city);local n=f.enabled and f.workers or 0;local actual,other=0,0
   for _,kind in ipairs(kinds) do for bit=0,7 do
    if P.HasBuilding(city:GetBuildings(),P.Info("Buildings",name(kind,bit)).Index) then
     if kind==f.kind then actual=actual+2^bit else other=other+2^bit end
    end
   end end
   local native={}
   for _,cl in ipairs(classes[f.kind] or {}) do
    local good,value=pcall(function()
     local info=P.Info("GreatPersonClasses","GREAT_PERSON_CLASS_"..cl)
     return Players[pid]:GetGreatPeoplePoints():GetPointsPerTurn(info.Index)
    end)
    native[#native+1]=cl..":"..(good and type(value)=="number" and tostring(value) or "UNKNOWN")
   end
   local err=data.errors[pid..":"..city:GetID()]
   return "city="..city:GetID().." "..(f.kind or f.reason).." ACTIVE="..tostring(f.active).." workers="..f.workers
    .."\nAdded BASE per class: expected="..2*n.." carrier="..2*actual.." other="..other
    .."\nNative EMPIRE GPP/turn: "..(#native>0 and table.concat(native," | ") or "N/A")
    .."\nchanges="..data.changes.." refreshes="..data.refreshes.." "..f.reason..(err and " ERROR="..err or "")
    .."\nRead only. Carrier is base, not measured final GPP. UNKNOWN: use Great People UI."
  end)
  local out="P0-B2 Lv2 GPP | "..(ok and result or "ERROR "..tostring(result));print("[SPC][B035] "..out);return out
 end
 local function bind(events,event,fn) local e=P.Field(events,event);if e and e.Add then e.Add(fn) end end
 SPCRuntimeWork.StartReady(P,shared,'Lv2GPP',function() data.ready=true;data.errors={};data.Audit({load=true})end)
 for _,n in ipairs({'PlayerTurnActivated','CityTransfered','CityRemovedFromMap'})do SPCRuntimeWork.TargetHook(P,Events,n,data.Audit)end
 if not shared.DistrictCompleteness then
  for _,n in ipairs({'DistrictRemovedFromMap','DistrictBuildProgressChanged','DistrictPillaged','DistrictRepaired','BuildingAddedToMap','BuildingRemovedFromMap','BuildingPillaged','BuildingRepaired'})do SPCRuntimeWork.TargetHook(P,Events,n,data.Audit)end
  for _,n in ipairs({'OnDistrictConstructed','BuildingConstructed','CityBuilt','OnPillage'})do SPCRuntimeWork.TargetHook(P,GameEvents,n,data.Audit)end
 end
 -- E2 confirmed exit: exact transient IDs owned by this writer; no prefix scan.
 if shared.CityProgressionStore then shared.CityProgressionStore.RegisterExit('Lv2GPP',targets.Exit(function(c,loss)
   carriersSet.Exit(shared,c,loss)
 end,'Lv2GPP'))end

end
