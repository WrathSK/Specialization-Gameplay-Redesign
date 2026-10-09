include('CultureAestheticModel')
include('CurrentSpecializationFacts')
include('NetworkInput')
-- A single city-owned carrier projects explained building contributions onto their
-- actual district plots. Plot flags are disposable effect configuration, not history.
SPCCultureAesthetic={Bits=16,Carrier='BUILDING_SPC_CULTURE_AESTHETIC',Key='SPC_CULTURE_AESTHETIC_'}
local M=SPCCultureAesthetic
local function same(a,b)
 if type(a)~=type(b)then return false end;if type(a)~='table'then return a==b end
 for k,v in pairs(a)do if not same(v,b[k])then return false end end
 for k in pairs(b)do if a[k]==nil then return false end end;return true
end
function M.Start(P,shared)
 local d={ready=false,busy=false,records={},errors={},changes=0};shared.CultureAesthetic=d
 local function ready(reason)
  if d.ready then return false end
  d.ready=true;d.readyReason=reason;return true
 end
 local carrier
 local function validate()
  if carrier then return end
  local r=assert(P.Info('Buildings',M.Carrier),'AE_DEFINITIONS_MISSING')
  assert((r.InternalOnly==true or r.InternalOnly==1) and r.PrereqDistrict=='DISTRICT_CITY_CENTER' and r.CitizenSlots==0 and r.Housing==0,'AE_CARRIER_INVALID')
  for bit=0,M.Bits-1 do
   local mod=assert(P.Info('Modifiers','SPC_CULTURE_AESTHETIC_'..bit),'AE_DEFINITIONS_MISSING')
   assert(mod.ModifierType=='MODIFIER_CITY_DISTRICTS_ADJUST_TOURISM_CHANGE','AE_MODIFIER_INVALID')
  end
  carrier=r.Index
 end
 local function cityKey(pid,c)return pid..':'..c:GetID()end
 local function plots(c)
  local out={};local ds=c:GetDistricts();local n=ds:GetNumDistricts()
  assert(type(n)=='number' and n>=0 and n%1==0,'AE_DISTRICTS_UNKNOWN')
  for i=0,n-1 do
   local district=assert(ds:GetDistrictByIndex(i),'AE_DISTRICTS_UNKNOWN')
   local plot=assert(Map.GetPlot(district:GetX(),district:GetY()),'AE_PLOT_UNKNOWN')
   out[plot:GetIndex()]=plot
  end
  return out
 end
 local function readAmount(plot)
  local amount=0
  for bit=0,M.Bits-1 do
   local v=plot:GetProperty(M.Key..bit)
   assert(v==nil or v==0 or v==1,'AE_CONFIGURATION_INVALID')
   if v==1 then amount=amount+2^bit end
  end
  return amount
 end
 local function flag(plot,bit,want)
  local key=M.Key..bit;local old=plot:GetProperty(key)
  assert(old==nil or old==0 or old==1,'AE_CONFIGURATION_INVALID')
  if (old or 0)~=want then
   P.SetProperty(plot,key,want);assert(plot:GetProperty(key)==want,'AE_FLAG_WRITE_UNCONFIRMED');d.changes=d.changes+1
  end
 end
 local function installed(c)
  local b=c:GetBuildings();local yes=P.HasBuilding(b,carrier)
  assert(type(yes)=='boolean','AE_CARRIER_UNKNOWN')
  return yes,yes and b:IsPillaged(carrier)==false
 end
 local function removeCarrier(c)
  local yes=installed(c)
  if yes then P.RemoveBuilding(c:GetBuildings(),carrier);assert(P.HasBuilding(c:GetBuildings(),carrier)==false,'AE_REMOVE_UNCONFIRMED');d.changes=d.changes+1 end
 end
 local function withdraw(c)
  validate();removeCarrier(c)
  for _,plot in pairs(plots(c))do
   for bit=0,M.Bits-1 do flag(plot,bit,0)end
   if plot:GetProperty(M.Key..'OWNER')~=nil then P.SetProperty(plot,M.Key..'OWNER',nil)end
  end
 end
 -- Model requires works only when the current Culture gate is satisfied.
 local function plan(pid,c,detail)
  assert(c:GetOwner()==pid and P.IsTestPlayer(pid),'AE_OWNER_CHANGED')
  local f=SPCCurrentSpecializationFacts.Read(P,shared,pid,c)
  local gw=shared.GreatWorkFacts.Summary(pid,c:GetID())
  local p=SPCCultureAestheticModel.Plan(f,gw,nil)
  local view
  if p.status=='NEEDS_BUILDINGS' then
   local reader=detail and shared.DistrictCompleteness.Read or shared.DistrictCompleteness.ReadFacts
   view=reader(pid,c,f.token)
   p=SPCCultureAestheticModel.Plan(f,gw,view,detail)
  end
  return p,f,view
 end
 local function reconcile(pid,c)
  validate();local key=cityKey(pid,c);local nativeRef=SPCNetworkInput.Reference(c);local old=d.records[key]
  local ok,p,f,view=pcall(plan,pid,c)
  if not ok then
   -- UNKNOWN never activates a new reference or resurrects a loaded effect snapshot.
   if not old or old.reference~=nativeRef then withdraw(c);d.records[key]=nil end
   error(p)
  end
  assert(type(f.token)=='string','AE_REFERENCE_UNKNOWN')
  local present,healthy=installed(c)
  -- Legacy writers own their exact withdrawal lists. No prefix enumeration.
  local withdrawn=pcall(function()
   assert(shared.Lv3Effects.WithdrawCulture(c)==true and shared.Lv4Percent.WithdrawCulture(c)==true,'AE_LEGACY_WITHDRAWAL_UNKNOWN')
  end)
  if not withdrawn then removeCarrier(c);error('AE_LEGACY_WITHDRAWAL_UNKNOWN')end
  if p.status=='INACTIVE' and not old and not present then return end
  local targetPlots={}
  if p.status=='READY' then
   -- Reuse the current confirmed shared snapshot, not a second district census.
   assert(view.validity=='VERIFIED' and view.availability=='READY','AE_BUILDINGS_UNKNOWN')
   for _,district in ipairs(view.value.districts)do targetPlots[district.plot]=assert(Map.GetPlotByIndex(district.plot),'AE_PLOT_UNKNOWN')end
  else targetPlots=plots(c)end
  for plot,n in pairs(p.amounts)do
   assert(targetPlots[plot],'AE_PLOT_REFERENCE_CHANGED')
   assert(n>=0 and n%1==0 and n<2^M.Bits,'AE_ENCODING_RANGE') -- technical bound, never truncate
  end
  local wanted=p.total>0
  local unchanged=old and old.reference==nativeRef and old.token==f.token and same(old.amounts,p.amounts)
  if unchanged and present==wanted and (not present or healthy) then
   return -- same confirmed input/configuration: no projection write or flag scan
  end
  -- Disable the sole owner before mutating projection flags, so a partial write
  -- cannot grant a mixed amount. Failure keeps it withdrawn until reconciliation.
  removeCarrier(c)
  if old then for index in pairs(old.amounts)do if not targetPlots[index]then
   local plot=Map.GetPlotByIndex(index)
   if plot and plot:GetProperty(M.Key..'OWNER')==old.reference then
    for bit=0,M.Bits-1 do flag(plot,bit,0)end;P.SetProperty(plot,M.Key..'OWNER',nil)
   end
  end end end
  for plot,object in pairs(targetPlots)do
   local n=p.amounts[plot] or 0
   local owner=n>0 and nativeRef or nil
   if object:GetProperty(M.Key..'OWNER')~=owner then P.SetProperty(object,M.Key..'OWNER',owner)end
   for bit=0,M.Bits-1 do flag(object,bit,math.floor(n/2^bit)%2)end
   assert(readAmount(object)==n,'AE_PROJECTION_UNCONFIRMED')
  end
  assert(c:GetOwner()==pid and SPCNetworkInput.Reference(c)==nativeRef,'AE_REFERENCE_CHANGED')
  if wanted then
   P.CreateBuilding(c:GetBuildQueue(),carrier)
   local b=c:GetBuildings();assert(P.HasBuilding(b,carrier)==true and b:IsPillaged(carrier)==false,'AE_CREATE_UNCONFIRMED');d.changes=d.changes+1
  end
  d.records[key]=p.status=='READY' and {reference=nativeRef,token=f.token,amounts=p.amounts,total=p.total,owner=pid,x=c:GetX(),y=c:GetY()} or nil
 end
 function d.Audit(scope)
  if not d.ready or d.busy then return end;d.busy=true
  if P.Observe then P.Observe('audit','CultureAesthetic')end
  local live={}
  for pid,player in pairs(Players)do if P.IsTestPlayer(pid) and (not scope or not scope.player or scope.player==pid)then
   local ok,why=pcall(function()
    local collection=assert(player:GetCities(),'AE_CITIES_UNKNOWN')
    local function visit(c)
     if not c then return end;P.Count('city_scan');local key=cityKey(pid,c);live[key]=true
     local good,err=pcall(reconcile,pid,c);d.errors[key]=not good and tostring(err) or nil
    end
    if scope and scope.city~=nil then visit(collection:FindID(scope.city)) else
     for _,c in collection:Members()do visit(c)end
     -- Only complete enumeration authorizes removal of absent session records.
     for _,entries in ipairs({d.records,d.errors})do
      for key in pairs(entries)do if key:match('^'..pid..':') and not live[key]then entries[key]=nil end end
     end
    end
   end)
   d.error=not ok and tostring(why) or nil
  end end
  d.busy=false
 end
 local reasons={PALACE='宫殿',WONDER='奇观',INTERNAL_OR_TECHNICAL='内部载体',UNREVIEWED_BUILDING='未审对象',
  UNDER_CONSTRUCTION='未完成',BUILDING_PILLAGED='已掠夺',DISTRICT_PILLAGED='区域已掠夺',DISTRICT_UNFINISHED='区域未完成'}
 function d.Describe(pid,c,detail,page)
  local ok,text=pcall(function()
   validate();local p=plan(pid,c,detail);local yes,healthy=installed(c);local raw=0;local matched=true
   local amounts={};for plot,object in pairs(plots(c))do
    amounts[plot]=readAmount(object);raw=raw+amounts[plot]
    if amounts[plot]~=(p.amounts[plot] or 0)then matched=false end
   end
   for plot,n in pairs(p.amounts)do if amounts[plot]~=n then matched=false end end
   local configured=healthy and raw or 0
   matched=matched and configured==p.total and (p.total>0 and healthy or p.total==0 and not yes)
   local err=d.errors[cityKey(pid,c)] or d.error
   local status=not d.ready and '等待启动' or (err or not matched) and '配置待核对'
    or p.status~='READY' and '未启用' or p.total==0 and '当前无旅游贡献' or '配置已进入'
   local lines={'风雅熏陶｜ACTIVE '..tostring(p.active)..'｜'..status,
    p.eras..' 个巨作时代｜'..p.count..' 座合格普通建筑',
    '每栋 + '..p.each..' 基础旅游业绩｜预期合计 + '..p.total,
    '区域投影配置 + '..configured..(matched and '（与预期一致）' or '（待核对）'),
    '配置不是原生实测；固定馆藏，切换总督核对旅游差值。'}
   if detail or not d.ready or not matched or err then
    local reasons={LOAD_SCREEN_CLOSE='加载完成',CONFIRMED_WORKS='馆藏确认',LOCAL_TURN='玩家回合'}
    lines[#lines+1]='更新：'..(d.ready and (reasons[d.readyReason] or '已就绪') or '未就绪')
     ..'｜载体：'..(not yes and '未建立' or healthy and '已建立' or '不可用')..'｜标记 + '..raw
   end
   if detail then
    local rows={}
    local gw=shared.GreatWorkFacts.Read(pid,c:GetID());local eras={}
    for era in pairs(gw and gw.eras or {})do local r=P.Info('Eras',era);eras[#eras+1]=Locale.Lookup(r and r.Name or era)end;table.sort(eras)
    if #eras>0 then lines[#lines+1]='本城时代：'..table.concat(eras,'、')end
    for _,b in ipairs(p.rows)do
     if b.reason~='INTERNAL_OR_TECHNICAL' then rows[#rows+1]=Locale.Lookup(b.name or b.type)..'：'..(b.eligible and ('+'..b.amount) or ('排除：'..(reasons[b.reason] or b.reason or '未确认')))end
    end
    local pages=math.max(1,math.ceil(#rows/7));local n=((page or 1)-1)%pages+1;lines[#lines+1]='建筑组成 '..n..'/'..pages..'（右键继续）'
    for i=(n-1)*7+1,math.min(#rows,n*7)do lines[#lines+1]=rows[i]end
   end
   if err then lines[#lines+1]='待复核：'..(err:match('AE_[A-Z_]+') or '接口未就绪')end
   return table.concat(lines,'\n')
  end)
  return ok and text or ('风雅熏陶：当前事实待复核；UNKNOWN不当作0。\n'..(tostring(text):match('AE_[A-Z_]+') or '接口未就绪')..'\n保留同一引用的最近确认配置；新引用/冷加载未确认前不施加。')
 end
 local function bind(source,name,fn)local e=P.Field(source,name);if e and e.Add then e.Add(fn)end end
 bind(Events,'LoadScreenClose',function()carrier=nil;d.records={};d.errors={};d.error=nil;d.ready=true;d.readyReason='LOAD_SCREEN_CLOSE';d.Audit()end)
 bind(Events,'CityBuildingsChanged',function(pid,cid)d.Audit({player=pid,city=cid})end)
 for _,name in ipairs({'BuildingAddedToMap','BuildingRemovedFromMap'})do
  bind(Events,name,function(x,y,id,owner)
   local row=P.Info('Buildings',id)
   if row and (row.BuildingType==M.Carrier or shared.CultureInspiration and shared.CultureInspiration.IsOwnedCarrier(row.BuildingType) or shared.CultureMeaning and shared.CultureMeaning.IsOwnedCarrier(row.BuildingType) or shared.CultureMeaningProbe and shared.CultureMeaningProbe.IsOwnedCarrier(row.BuildingType))then return end
   -- L2A's exact ten transient test carriers cannot change ordinary buildings/X.
   local ok,c=pcall(function()
    local district=CityManager.GetDistrictAt and CityManager.GetDistrictAt(x,y)
    return district and district:GetCity() or CityManager.GetCityAt(x,y)
   end)
   if ok and c and c:GetOwner()==owner then d.Audit({player=owner,city=c:GetID()})else d.Audit()end
  end)
 end
 for _,name in ipairs({'BuildingPillaged','BuildingRepaired','DistrictRemovedFromMap','DistrictBuildProgressChanged',
  'DistrictPillaged','DistrictRepaired','GovernorAssigned','GovernorEstablished','GovernorChanged','GovernorPromoted','CityTransfered','CityRemovedFromMap'})do
  bind(Events,name,function()d.Audit()end)
 end
 local lastTurn
 bind(Events,'PlayerTurnActivated',function(pid)
  if P.IsTestPlayer(pid) and lastTurn~=Game.GetCurrentGameTurn()then
   lastTurn=Game.GetCurrentGameTurn();ready('LOCAL_TURN');d.Audit({player=pid})
  end
 end)
 for _,name in ipairs({'BuildingConstructed','OnDistrictConstructed','OnPillage','CityBuilt'})do bind(GameEvents,name,function()d.Audit()end)end
 -- One explicitly scoped consumer notification, not a new shared event bus.
 shared.GreatWorkFacts.OnConfirmed=function(pid,changed)
  if not P.IsTestPlayer(pid)then return end
  -- A confirmed current-city sample is a ready boundary even if the UI load
  -- notification was missed. UNKNOWN/foreign input cannot open this path.
  if not d.ready then
   for _,cid in ipairs(changed)do
    local c=Players[pid]:GetCities():FindID(cid);local w=shared.GreatWorkFacts.Summary(pid,cid)
    if c and c:GetOwner()==pid and w and w.hasConfirmed and w.availability=='KNOWN'
     and w.reference==SPCNetworkInput.Reference(c)then
     ready('CONFIRMED_WORKS');d.Audit({player=pid});return -- initial local-player reconciliation once
    end
   end
   return
  end
  for _,cid in ipairs(changed)do d.Audit({player=pid,city=cid})end
 end
 local store=shared.CityProgressionStore
 if store then
  store.RegisterExit('CultureAesthetic',function(c,loss)
   assert(store.IsExitTarget(c,loss),'AE_EXIT_UNCONFIRMED');withdraw(c)
   for key,r in pairs(d.records)do if r.owner==loss.origin.owner and r.x==c:GetX() and r.y==c:GetY()then d.records[key]=nil;d.errors[key]=nil end end
  end)
  store.RegisterReturn('CultureAesthetic',function(pid,c)d.Audit({player=pid,city=c:GetID()})end)
 end
 return d
end
