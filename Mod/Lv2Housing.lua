include('RuntimeWork')
include('SpecialistSupport')
-- P0-B2: shared ordinary eligibility, distinct Tier presence in the actual anchor.
-- D's weighted sum/highest-domain choice is deliberately not a housing input.
SPCLv2Housing={}
function SPCLv2Housing.Start(P,shared)
 local data={ready=false,busy=false,changes=0,errors={},events=0};shared.Lv2Housing=data
 local kinds={RESEARCH=true,CULTURE=true,COMMERCE=true,INDUSTRY=true}
 local function carrier(i)
  local row=P.Info('Buildings','BUILDING_SPC_DEV_LV2_HOUSING_'..i)
  assert(row and type(row.Index)=='number' and row.Housing==1,'B2_HOUSING_DATABASE_MISMATCH')
  return row.Index
 end
 local function expected(pid,city,batch)
  local wanted={}
  local kind,d,f=SPCSpecialistSupport.Anchor(P,shared,pid,city,batch)
  if not kinds[kind] then return wanted,'CONFIRMED_INELIGIBLE',{} end
  if f.active<2 then return wanted,'ACTIVE='..f.active,{} end
  local svc=assert(shared.DistrictCompleteness,'B2_ORDINARY_FACTS_UNAVAILABLE')
  -- Called only for direct changes/reconciliation/manual reads, never a UI pulse.
  svc.MarkDirty(pid,city:GetID())
  local sample=svc.Read(pid,city)
  assert(sample.validity=='VERIFIED' and sample.availability=='READY',sample.error or 'B2_BUILDINGS_UNAVAILABLE')
  local anchor
  for _,r in ipairs(sample.value.districts) do if r.id==d:GetID() then anchor=r;break end end
  assert(anchor and anchor.type==f.first.type,'B2_ANCHOR_SAMPLE_MISMATCH')
  assert(anchor.complete and not anchor.pillaged,'B2_ANCHOR_CHANGED_DURING_READ')
  wanted[0]=true
  for _,b in ipairs(anchor.buildings) do
   if b.ordinary and b.complete and not b.pillaged then
    assert(b.tier~=nil,'B2_ORDINARY_TIER_UNKNOWN '..b.type)
    assert(b.reason=='INCLUDED' or b.reason=='ORDINARY_TIER_ZERO','B2_ORDINARY_CLASSIFICATION_UNKNOWN '..b.type)
    if b.tier>0 then wanted[b.tier]=true end
   end
  end
  return wanted,kind..' ACTIVE='..f.active..' anchor='..d:GetID(),anchor.buildings
 end
 local function plan(city,wanted)
  local result={}
  for i=0,8 do
   local id=carrier(i);local present=P.HasBuilding(city:GetBuildings(),id)
   assert(type(present)=='boolean','B2_HOUSING_CARRIER_UNKNOWN')
   result[#result+1]={id=id,present=present,wanted=wanted[i]==true}
  end
  return result -- all inputs and carrier reads verified before the first write
 end
 local function process(pid,city,batch)
  local wanted=expected(pid,city,batch);local changes=plan(city,wanted)
  for _,adding in ipairs({false,true}) do for _,v in ipairs(changes) do
   if v.wanted==adding and v.present~=v.wanted then
    if adding then P.CreateBuilding(city:GetBuildQueue(),v.id) else P.RemoveBuilding(city:GetBuildings(),v.id) end
    assert(P.HasBuilding(city:GetBuildings(),v.id)==v.wanted,'B2_HOUSING_WRITE_UNCONFIRMED')
    data.changes=data.changes+1
   end
  end end
 end
 function data.Audit(scope)
  if not data.ready or data.busy then P.Count('busy_skip');return end
  data.busy=true;data.events=data.events+1;local batch=SPCRuntimeWork.New(P,shared)
  if type(scope)~='table' or scope.player==nil then data.errors={} end
  for pid,player in pairs(Players) do if SPCRuntimeWork.Player(scope,pid) then
   local ok,err=pcall(function()
    for _,city in player:GetCities():Members() do
     P.Count('city_scan');local k=pid..':'..city:GetID()
     local good,why=pcall(process,pid,city,batch)
     data.errors[k]=not good and tostring(why) or nil
    end
   end)
   data.errors['player:'..pid]=not ok and tostring(err) or nil
  end end
  data.busy=false
 end
 function data.Describe(pid,city)
  local ok,out=pcall(function()
   assert(data.ready,'B2_HOUSING_NOT_READY')
   local wanted,reason,buildings=expected(pid,city,SPCRuntimeWork.New(P,shared))
   local n,actual,tiers=0,0,{}
   for i=0,8 do
    if wanted[i] then n=n+1;if i>0 then tiers[#tiers+1]=i end end
    if P.HasBuilding(city:GetBuildings(),carrier(i)) then actual=actual+1 end
   end
   local lines={'city='..city:GetID()..' '..reason,
    '住房 expected=+'..n..' carrier=+'..actual..' tiers='..table.concat(tiers,','),
    '本专业区域1住房 + 每种合格普通建筑Tier各1；不读取D加权值。'}
   for _,b in ipairs(buildings) do lines[#lines+1]=b.type..' Tier='..tostring(b.tier)..' pillaged='..tostring(b.pillaged)..' '..tostring(b.reason) end
   lines[#lines+1]='changes='..data.changes..' refreshes='..data.events..' error='..tostring(data.errors[pid..':'..city:GetID()] or 'NONE')
   return table.concat(lines,'\n')
  end)
  return 'P0-B2 Lv2 Housing | '..(ok and out or ('UNKNOWN / installed housing retained: '..tostring(out)))
 end
 local function bind(source,n,fn) local e=P.Field(source,n);if e and e.Add then e.Add(fn) end end
 bind(Events,'LoadScreenClose',function() data.ready=true;data.errors={};data.Audit() end)
 for _,n in ipairs({'PlayerTurnActivated','GovernorAssigned','GovernorEstablished','GovernorChanged','GovernorPromoted',
  'CityTransfered','CityRemovedFromMap','BuildingAddedToMap','BuildingRemovedFromMap','BuildingPillaged','BuildingRepaired',
  'DistrictRemovedFromMap','DistrictBuildProgressChanged','DistrictPillaged','DistrictRepaired'}) do
  SPCRuntimeWork.Hook(P,Events,n,data.Audit)
 end
 -- CityBuildingsChanged can be raised by our own carriers. Structural events
 -- above + once/player/turn reconciliation cover it without a feedback loop.
 for _,n in ipairs({'BuildingConstructed','OnDistrictConstructed','CityBuilt','OnPillage'}) do bind(GameEvents,n,data.Audit) end
 -- E2 confirmed exit: exact transient IDs owned by this writer; no prefix scan.
 if shared.CityProgressionStore then shared.CityProgressionStore.RegisterExit('Lv2Housing',function(c,loss)
   local ids={};for bit=0,8 do ids[#ids+1]='BUILDING_SPC_DEV_LV2_HOUSING_'..bit end
   shared.CityProgressionStore.RemoveOwned(c,loss,ids)
 end)end

end
