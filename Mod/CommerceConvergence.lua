include('RuntimeWork')
-- D0024: independently planned, absolute city-layer integer grants.
SPCCommerceConvergence={}
function SPCCommerceConvergence.Start(P,shared)
 local d={busy=false,ready=false,last={},errors={},mode={},testCity={},baseline={},writes=0};shared.CommerceConvergence=d
 local function isolated(pid) return shared.NetworkIsolation and shared.NetworkIsolation.Active(pid)==true end
 local batch
 local ys={'SCIENCE','CULTURE','PRODUCTION'};local map={RESEARCH='SCIENCE',CULTURE='CULTURE',INDUSTRY='PRODUCTION'}
 local function yield(c,y)
  local key=c:GetOwner()..':'..c:GetID()..':'..y
  if batch and batch.yields[key]~=nil then return batch.yields[key] end
  local n=c:GetYield(P.Info('Yields','YIELD_'..y).Index);assert(type(n)=='number' and n==n and math.abs(n)<math.huge,'CITY_YIELD_INVALID');if batch then batch.yields[key]=n end;return n end
 local function facts(pid,c) assert(c and c:GetOwner()==pid,'CITY_OWNER');return batch and batch.facts.Facts(pid,c) or shared.EffectiveFacts.Read(pid,c) end
 local function eligible(pid,c) local f=facts(pid,c);return P.IsTestPlayer(pid) and f.specialization=='COMMERCE' and f.active==4 end
 function d.Plan(pid,c)
  local out={amount={},raw={},source={},basis={},eligible=not isolated(pid) and eligible(pid,c)}
  for _,y in ipairs(ys) do out.amount[y]=0;out.raw[y]=0;out.basis[y]=0 end
  if not out.eligible or d.mode[pid]=='OFF' then return out end
  if d.mode[pid]=='TEST5' then
   if d.testCity[pid]==c:GetID() then for _,y in ipairs(ys) do out.amount[y]=5;out.raw[y]=5 end end
   return out
  end
  local bridge=shared.NetworkBridge;local b=bridge and bridge.players[pid]
  assert(bridge and bridge.ready and b and b.routes and b.reason=='READY_BACKGROUND_UI','NETWORK_UNAVAILABLE')
  if bridge.Input then assert(bridge.Input(pid).validity=='VERIFIED','NETWORK_PENDING')
  else assert(bridge.Verified(pid),'NETWORK_PENDING') end
  -- Retain verified topology while a possible addition is revalidated.
  local routes=b.routes
  if batch then
   if not batch.routes[pid] then
    local index={}
    for _,r in ipairs(routes) do
     local op,dp=Players[r.op],Players[r.dp]
     local a=op and op:GetCities():FindID(r.oc);local z=dp and dp:GetCities():FindID(r.dc)
     assert(a and z and a:GetOwner()==r.op and z:GetOwner()==r.dp,'ROUTE_ENDPOINT_CHANGED')
     if r.op==pid and r.dp==pid then index[r.dc]=index[r.dc] or {};index[r.dc][#index[r.dc]+1]=r end
    end
    batch.routes[pid]=index
   end
   routes=batch.routes[pid][c:GetID()] or {}
  end
  local seen={}
  for _,route in ipairs(routes) do
   assert(Players[route.op] and Players[route.dp],'ROUTE_OWNER_MISSING')
   local origin=Players[route.op]:GetCities():FindID(route.oc);local destination=Players[route.dp]:GetCities():FindID(route.dc)
   assert(origin and destination and origin:GetOwner()==route.op and destination:GetOwner()==route.dp,'ROUTE_ENDPOINT_CHANGED')
   if route.op==pid and route.dp==pid and route.dc==c:GetID() and not seen[route.oc] then
    seen[route.oc]=true;local f=facts(pid,origin);local y=map[f.specialization]
    if y and type(f.active)=='number' and f.active>=1 and f.active<=4 and f.active%1==0 then
     local value=yield(origin,y);assert(value>=0,'NEGATIVE_SOURCE_BASIS')
     if not out.source[y] or value>out.basis[y] or (value==out.basis[y] and route.oc<out.source[y]) then out.basis[y]=value;out.source[y]=route.oc end
    end
   end
  end
  for _,y in ipairs(ys) do out.raw[y]=out.basis[y]*.2;out.amount[y]=math.floor(out.raw[y]);assert(out.amount[y]<=65535,'DIRECTORY_LIMIT') end
  return out
 end
 local function row(y,bit) return P.Info('Buildings','BUILDING_SPC_B061_'..y..'_'..bit) end
 local function observed(c,y)
  local total=0;local bits={};local b=c:GetBuildings()
  for bit=0,15 do local r=row(y,bit);assert(r,'DATABASE_MISSING');if P.HasBuilding(b,r.Index) then total=total+2^bit;bits[#bits+1]=tostring(2^bit) end end
  return total,table.concat(bits,'+')
 end
 local function apply(c,amount)
  local b=c:GetBuildings()
  for _,adding in ipairs({false,true}) do for _,y in ipairs(ys) do local n=amount[y] or 0
   assert(n>=0 and n<=65535 and n%1==0,'APPLY_RANGE')
   for bit=0,15 do local r=assert(row(y,bit),'DATABASE_MISSING');local want=math.floor(n/2^bit)%2==1
    if want==adding and P.HasBuilding(b,r.Index)~=want then
     if want then P.CreateBuilding(c:GetBuildQueue(),r.Index) else P.RemoveBuilding(b,r.Index) end
     assert(P.HasBuilding(b,r.Index)==want,'CARRIER_WRITE_FAILED');d.writes=d.writes+1
    end
   end
  end end
  for _,y in ipairs(ys) do assert(observed(c,y)==(amount[y] or 0),'CARRIER_VERIFY_FAILED') end
 end
 function d.Audit(scope)
  if isolated() then return end
  P.Count('audit_commerce');
  if P.Observe then P.Observe('audit','CommerceConvergence') end
  if d.busy then P.Count('busy_skip');return end;d.busy=true;batch={facts=SPCRuntimeWork.New(P,shared),yields={},routes={}}
  local ok,err=pcall(function()
   if not d.ready then
    for _,p in pairs(Players) do local cs=p:GetCities();if cs then for _,c in cs:Members() do P.Count('city_scan'); apply(c,{}) end end end
    d.ready=true
   end
   local plans={}
   for pid,p in pairs(Players) do local cs=SPCRuntimeWork.Player(scope,pid) and p:GetCities();if cs then for _,c in cs:Members() do P.Count('city_scan');
    local key=pid..':'..c:GetID();local good,plan=pcall(d.Plan,pid,c)
    plans[#plans+1]={key=key,c=c,plan=good and plan or {amount={}},error=not good and tostring(plan) or nil}
   end end end
   -- No city's newly applied amount can influence another plan in this pass.
   for _,x in ipairs(plans) do
    local good,why=pcall(apply,x.c,x.plan.amount);d.errors[x.key]=not good and tostring(why) or x.error
    d.last[x.key]=good and x.plan or nil
   end
  end)
  d.busy=false;batch=nil;d.error=not ok and tostring(err) or nil
  if not ok then print('[SPC][B062] '..tostring(err)) end
 end
 function d.Control(pid,c,action)
  assert(P.IsTestPlayer(pid) and c:GetOwner()==pid,'CONTROL_OWNER')
  if action=='READ' then return end
  assert(not isolated(pid),'NETWORK_ISOLATION_ACTIVE')
  assert(action=='OFF' or action=='AUTO' or action=='TEST5','CONTROL_ACTION')
  d.mode[pid]=action;d.testCity[pid]=action=='TEST5' and c:GetID() or nil
  d.Audit()
  if action=='OFF' then local base={};for _,y in ipairs(ys) do base[y]=yield(c,y) end;d.baseline[pid..':'..c:GetID()]=base end
 end
 -- B137 session-only isolation: this module owns the exact list and native withdrawal.
 function d.ExperimentalNetworkWithdraw(pid)
  assert(isolated(pid),'NETWORK_ISOLATION_NOT_ARMED')
  assert(P.IsTestPlayer(pid),'NETWORK_ISOLATION_PLAYER')
  assert(not d.busy,'NETWORK_ISOLATION_CONSUMER_BUSY')
  d.busy=true
  local ok,why=pcall(function()
   local ids={};for _,y in ipairs(ys) do for bit=0,15 do ids[#ids+1]='BUILDING_SPC_B061_'..y..'_'..bit end end
   local indexes={};for _,id in ipairs(ids) do
    local r=assert(P.Info('Buildings',id),'NETWORK_ISOLATION_DATABASE:'..id)
    assert(type(r.Index)=='number','NETWORK_ISOLATION_INDEX:'..id);indexes[#indexes+1]=r.Index
   end
   local player=assert(Players[pid],'NETWORK_ISOLATION_PLAYER_MISSING')
   local cities=assert(player:GetCities(),'NETWORK_ISOLATION_CITIES_UNKNOWN')
   for _,c in cities:Members() do
    assert(c:GetOwner()==pid,'NETWORK_ISOLATION_OWNER_CHANGED')
    local b=c:GetBuildings()
    for _,index in ipairs(indexes) do
     local present=P.HasBuilding(b,index);assert(type(present)=='boolean','NETWORK_ISOLATION_CARRIER_UNKNOWN:'..index)
     if present then P.RemoveBuilding(b,index);assert(P.HasBuilding(b,index)==false,'NETWORK_ISOLATION_REMOVE_UNCONFIRMED:'..index);d.writes=d.writes+1 end
    end
   end
   for _,c in cities:Members() do local key=pid..':'..c:GetID();d.last[key]=nil;d.errors[key]=nil;d.baseline[key]=nil end
   d.mode[pid]=nil;d.testCity[pid]=nil
  end)
  d.busy=false;d.isolationError=not ok and tostring(why) or nil
  if not ok then error(why) end
  return true
 end
 function d.Describe(pid,c)
  local key=pid..':'..c:GetID();local old=d.last[key];local good,current=pcall(d.Plan,pid,c)
  local rows={'B062 商业四 | '..(d.mode[pid] or 'AUTO')..' | city='..c:GetID(),
   '实际来源总量×20%，最终floor；载体是配置，不等于实际收益。'}
  if not good then rows[#rows+1]='当前来源未就绪（旧产出不作有效来源）：'..tostring(current):match('[^\r\n]+') end
  if d.error or d.errors[key] then rows[#rows+1]='应用状态：'..tostring(d.error or d.errors[key]):match('[^\r\n]+') end
  for _,y in ipairs(ys) do
   local p=good and current or nil;local src=p and p.source and p.source[y];local name=src and Locale.Lookup(Players[pid]:GetCities():FindID(src):GetName()) or '无'
   rows[#rows+1]=y..' 源='..name..string.format(' | 基数=%.4f | 20%%/实验=%.4f | 取整=%d',p and p.basis[y] or 0,p and p.raw[y] or 0,p and p.amount[y] or 0)
   local n,bits=observed(c,y);local value=yield(c,y);local base=d.baseline[key]
   rows[#rows+1]='已配置='..tostring(old and (old.amount[y] or 0) or '未知')..' | 载体='..n..' ['..bits..'] | 实际='..string.format('%.4f',value)..' | OFF差值='..(base and string.format('%.4f',value-base[y]) or '无基线')
  end
  rows[#rows+1]='OFF基线仅同城固定条件可比较；不同回合/人口/倍率变化会混入差值。'
  local b=shared.NetworkBridge and shared.NetworkBridge.players[pid]
  rows[#rows+1]='网络：'..tostring(b and b.reason)..' | 当前/样本回合='..Game.GetCurrentGameTurn()..'/'..tostring(b and b.turn)
  return table.concat(rows,'\n')
 end
 -- Native city yield can change when another specialization actually writes a carrier.
 -- Generic pulse reads one scalar; no output change means no Audit or native read.
 local seenOutput=ExposedMembers.SPC_RuntimeUIRevision or 0
 local function outputChanged()
  local now=ExposedMembers.SPC_RuntimeUIRevision or 0
  if now==seenOutput then return end
  seenOutput=now;d.Audit();seenOutput=ExposedMembers.SPC_RuntimeUIRevision or 0
 end
 for _,n in ipairs({'GameCoreEventPublishComplete','GameCoreEventPlaybackComplete'}) do
  local e=P.Field(Events,n);if e and e.Add then e.Add(outputChanged) end
 end
 local function hook(t,name) local e=P.Field(t,name);if e and e.Add then SPCRuntimeWork.Hook(P,t,name,d.Audit) end end
 for _,name in ipairs({'LoadScreenClose','PlayerTurnActivated','GovernorAssigned','GovernorEstablished','GovernorChanged','GovernorPromoted','CityWorkerChanged','CityPopulationChanged','CityFocusChanged','CityTransfered','BuildingAddedToMap','BuildingRemovedFromMap','CityProductionCompleted','CityTileOwnershipChanged','GovernmentPolicyChanged','GovernmentChanged','ResearchCompleted','CivicCompleted'}) do hook(Events,name) end
 for _,name in ipairs({'CityBuilt','OnBuildingConstructed','OnDistrictConstructed'}) do hook(GameEvents,name) end
 -- E2 confirmed exit: exact transient IDs owned by this writer; no prefix scan.
 if shared.CityProgressionStore then shared.CityProgressionStore.RegisterExit('CommerceConvergence',function(c,loss)
   local ids={};for _,y in ipairs(ys)do for bit=0,15 do ids[#ids+1]='BUILDING_SPC_B061_'..y..'_'..bit end end
   shared.CityProgressionStore.RemoveOwned(c,loss,ids)
 end)end

end
