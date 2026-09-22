-- AV2-B: one private derived view per accepted complete input; no consumer-yield cache.
include("NetworkInput")
SPCNetworkBridge={}
function SPCNetworkBridge.Start(P,shared)
 local d={ready=false,players={}};shared.NetworkBridge=d
 ExposedMembers.SPCNetworkEpoch=(ExposedMembers.SPCNetworkEpoch or 0)+1
 d.epoch=ExposedMembers.SPCNetworkEpoch
 local function integer(n) return type(n)=="number" and n>=0 and n%1==0 and n<2147483648 end
 local function city(pid,id)
  local p=Players[pid];local c=p and p:GetCities():FindID(id)
  assert(c and c:GetOwner()==pid,"ENDPOINT_MISSING_OR_CHANGED");return c
 end
 local function short(err)
  local first=tostring(err):match("[^\r\n]+") or "UNKNOWN"
  return (first:match(":%d+: (.+)$") or first):sub(1,180)
 end
 local derive
 local views={} -- private, at most one view per player; never keyed by historical versions
 local function copy(v)
  if type(v)~='table' then return v end
  local out={};for k,x in pairs(v) do out[k]=copy(x) end;return out
 end
 local function buildView(pid,rows,input)
  P.Count('derive_requested');P.Count('derived_cache_miss')
  local sources,centers,recipients=derive(pid,rows,input)
  local connected,national={},{}
  for id,set in pairs(centers) do
   connected[id]={};for src in pairs(set) do connected[id][sources[src]]=true end
  end
  for _,kind in ipairs({'RESEARCH','CULTURE'}) do
   local n={n=0,level=0,sources={},recipients={}};national[kind]=n
   for cid,set in pairs(recipients[kind] or {}) do
    for src in pairs(set) do
     local f=input.cities[src]
     if f and f.specialization==kind and type(f.active)=='number' and f.active>=1 and f.active<=4 and f.active%1==0 then
      n.sources[src]=f.active;n.recipients[cid]=true;n.level=math.max(n.level,f.active)
     end
    end
   end
   for _ in pairs(n.recipients) do n.n=n.n+1 end
  end
  return {sources=sources,centers=centers,recipients=recipients,connected=connected,national=national}
 end
 local function bucket(pid)
  if not d.players[pid] then d.players[pid]={seq=-1,revision=0,inputRevision=0,derivedRevision=0,validity='UNKNOWN',availability='UNAVAILABLE'} end
  return d.players[pid]
 end
 -- Metadata is a value copy. Input revision belongs to this Gameplay epoch, not the save.
 function d.Input(pid)
  local b=bucket(pid)
  return {contract=1,epoch=d.epoch,player=pid,inputVersion=b.inputRevision,signature=b.inputSignature,
   validity=b.validity,availability=b.availability,routeRevision=b.revision,routeValidity=b.routes and 'VERIFIED' or b.validity,revalidation=b.revalidation,
   derivedRevision=b.derivedRevision,derivedFor=b.derivedFor,withdrawal=b.withdrawal==true}
 end
 local function notify(pid)
  local publication=d.Input(pid)
  -- Existing independent consumer listeners remain Batch D. This publisher only notifies on diff.
  for _,name in ipairs({'Lv3Effects','StandardizationDiscount','NetworkBoost','CommerceConvergence','CopyYields'}) do
   local consumer=shared[name]
   if consumer then local ok,err=pcall(consumer.Audit,publication)
    if not ok then bucket(pid).consumerError=short(err) end
   end
  end
 end
 local function publish(pid,b,input,view,withdrawal)
  if b.inputSignature==input.signature then P.Count('input_duplicate');return false end
  b.inputRevision=b.inputRevision+1;b.inputSignature=input.signature;b.input=input
  b.validity=input.validity;b.withdrawal=withdrawal==true
  if views[pid] then P.Count('derived_invalidation') end
  views[pid]=view
  if view then
   view.contract=1;view.epoch=d.epoch;view.player=pid;view.inputVersion=b.inputRevision
   view.derivedFor=b.inputRevision;view.validity='VERIFIED';view.signature=input.signature
  end
  -- Compatibility/debug projections must not expose the private cache to mutation.
  b.sources=view and copy(view.sources);b.centers=view and copy(view.centers);b.recipients=view and copy(view.recipients)
  if input.validity=='VERIFIED' then b.derivedRevision=b.derivedRevision+1;b.derivedFor=b.inputRevision
  else b.derivedFor=nil end
  P.Count('fact_change');P.Count('input_version_change');P.Count('input_publication')
  if withdrawal then P.Count('withdrawal') end
  notify(pid);return true
 end
 local function withdraw(pid,b,reason)
  if b.validity=='CONFIRMED_INVALID' and not b.routes then return false end
  b.routes=nil;b.fingerprint=nil;b.routeReferences=nil;b.candidate=nil;b.reason='CONFIRMED_INVALID';b.error=reason
  b.revalidation='CONFIRMED_INVALID';b.availability='UNAVAILABLE';b.revision=b.revision+1
  P.Count('confirmed_invalid')
  local input={validity='CONFIRMED_INVALID',routeSignature='',cities={}}
  input.signature=SPCNetworkInput.Signature(input)
  local perf=ExposedMembers.SPC_Performance;if perf then perf.revision=b.revision;perf.routes=0 end
  return publish(pid,b,input,nil,true)
 end
 -- Concrete native evidence only. Unknown getters preserve the accepted snapshot.
 function d.Verified(pid,failedFullRead)
  local b=d.players[pid];if not b or not b.routes then return false end
  if b.refreshing then return true end
  local ok,invalid=pcall(function()
   if failedFullRead and Players[pid]:GetTrade():CountOutgoingRoutes()<#b.routes then return true end
   for _,r in ipairs(b.routes) do
    local op,dp=Players[r.op],Players[r.dp]
    if not op or not dp then return true end
    local o,z=op:GetCities():FindID(r.oc),dp:GetCities():FindID(r.dc)
    if not o or not z or o:GetOwner()~=r.op or z:GetOwner()~=r.dp then return true end
    local refs=b.routeReferences and b.routeReferences[r.trader]
    if refs and (SPCNetworkInput.Reference(o)~=refs.origin or SPCNetworkInput.Reference(z)~=refs.destination) then return true end
    local known,u=pcall(function() return op:GetUnits():FindID(r.trader) end)
    if known and not u then return true end
    if r.op~=r.dp then
     local readable,war=pcall(function() return op:GetDiplomacy():IsAtWarWith(r.dp) end)
     if readable and war==true then return true end
    end
   end
   return false
  end)
  if ok and invalid then
   b.refreshing=true;withdraw(pid,b,'NATIVE_ROUTE_INVALID');b.refreshing=false;return false
  end
  if not ok then b.availability='NEEDS_REVALIDATION';b.revalidation='NEEDS_REVALIDATION' end
  return true
 end
 -- Capture a coherent complete input before changing any officially published input.
 function d.Refresh(pid)
  if not P.IsTestPlayer(pid) or not d.ready then return false end
  local b=bucket(pid)
  if b.refreshing then P.Count('busy_skip');return false end
  if not b.candidate and not d.Verified(pid) then return false end
  b.refreshing=true
  local candidate=b.candidate
  if candidate and (candidate.turn~=Game.GetCurrentGameTurn() or candidate.signal~=(shared.RouteSignalRevision or 0)) then
   b.candidate=nil;candidate=nil;P.Count('stale_input')
  end
  if not candidate and not b.routes then b.refreshing=false;return false end
  local rows=candidate and candidate.routes or b.routes
  local fingerprint=candidate and candidate.fingerprint or b.fingerprint
  local ok,input=pcall(function()
   if candidate then assert(Players[pid]:GetTrade():CountOutgoingRoutes()==#rows,'NETWORK_CANDIDATE_COUNT_CHANGED') end
   return SPCNetworkInput.Capture(P,shared,pid,rows,fingerprint,b.input)
  end)
  local changed=false
  if ok then
   b.availability=(input.pending or b.revalidation=='NEEDS_REVALIDATION') and 'NEEDS_REVALIDATION' or 'AVAILABLE';b.error=nil
   if b.inputSignature==input.signature then
    b.candidate=nil;P.Count('input_duplicate')
   else
    local good,view=pcall(buildView,pid,rows,input)
    if good then
     local withdrawal=b.input and b.input.capital~=nil and b.input.capital~=input.capital or false
     if candidate and b.routes then
      local present={};for _,route in ipairs(rows) do present[route.trader..':'..route.oc..':'..route.dp..':'..route.dc]=true end
      for _,route in ipairs(b.routes) do
       if not present[route.trader..':'..route.oc..':'..route.dp..':'..route.dc] then withdrawal=true end
      end
     end
     for id,old in pairs(b.input and b.input.cities or {}) do
      local new=input.cities[id]
      if old.potential>=1 and (not new or new.reference~=old.reference or new.specialization~=old.specialization
       or new.active<old.active or new.potential<1) then withdrawal=true end
     end
     if candidate then
      if b.fingerprint~=fingerprint or not b.routes then b.revision=b.revision+1;P.Count('publication') end
      b.routes=rows;b.routeReferences=candidate.references;b.fingerprint=fingerprint
      b.turn=candidate.turn;b.signal=candidate.signal;b.reason='READY_BACKGROUND_UI';b.revalidation='VERIFIED';b.candidate=nil
      local perf=ExposedMembers.SPC_Performance;if perf then perf.revision=b.revision;perf.routes=#rows end
     end
     changed=publish(pid,b,input,view,withdrawal)
    else b.availability='NEEDS_REVALIDATION';b.error=short(view) end
   end
  else
   b.availability=b.input and 'NEEDS_REVALIDATION' or 'UNAVAILABLE';b.error=short(input)
   -- A failed new sample cannot hide independently confirmed loss of an old input.
   local confirmed=false
   local checked,lost=pcall(function()
    for id,old in pairs(b.input and b.input.cities or {}) do
     local c=Players[pid]:GetCities():FindID(id)
     if not c or c:GetOwner()~=pid then return true end
     local good,reference=pcall(SPCNetworkInput.Reference,c)
     if good and reference~=old.reference then return true end
    end
    if candidate and b.routes then
     local current={};for _,r in ipairs(candidate.routes) do current[r.trader..':'..r.oc..':'..r.dp..':'..r.dc]=true end
     for _,r in ipairs(b.routes) do if not current[r.trader..':'..r.oc..':'..r.dp..':'..r.dc] then return true end end
    end
    return false
   end)
   confirmed=checked and lost
   if confirmed then changed=withdraw(pid,b,'CONFIRMED_INPUT_LOSS_WHILE_SAMPLE_PENDING') end
  end
  b.refreshing=false;return changed
 end
 function d.Receive(pid,p)
  P.Count('net_receive')
  if not P.IsTestPlayer(pid) or p.Epoch~=d.epoch or not integer(p.Seq) then P.Count('stale_input');return end
  local b=bucket(pid)
  if b.refreshing then P.Count('busy_skip');return end
  if p.Seq<=b.seq then P.Count('send_duplicate');P.Count('stale_input');return end
  b.seq=p.Seq;b.candidate=nil -- a newer packet supersedes any unpublished older candidate
  local ok,err=pcall(function()
   assert(d.ready,'LOAD_NOT_READY')
   assert(p.Turn==Game.GetCurrentGameTurn() and p.Signal==(shared.RouteSignalRevision or 0),'STALE_SIGNAL_OR_TURN')
   if p.Valid~=1 then b.revalidation='NEEDS_REVALIDATION';b.availability=b.input and 'NEEDS_REVALIDATION' or 'UNAVAILABLE';return end
   local count=p.Count
   if p.WireCount~=nil then
    assert(integer(p.WireCount) and p.WireCount>=1 and p.WireCount<=129,'WIRE_COUNT_INVALID')
    count=p.WireCount-1;assert(p.Count==nil or p.Count==count,'WIRE_COUNT_CONFLICT')
   end
   assert(integer(count) and count<=128,'ROUTE_COUNT_INVALID')
   local data=p.Data;if count==0 and data=='EMPTY' then data='' end
   assert(type(data)=='string' and #data<=16384,'ROUTE_DATA_INVALID')
   local rows,seen,keys={},{},{}
   for line in data:gmatch('[^;]+') do
    local a,o,c,z,u=line:match('^(%d+),(%d+),(%d+),(%d+),(%d+)$')
    assert(a,'ROW_FORMAT');a,o,c,z,u=tonumber(a),tonumber(o),tonumber(c),tonumber(z),tonumber(u)
    for _,v in ipairs({a,o,c,z,u}) do assert(integer(v),'ROW_RANGE') end
    assert(a==pid and not seen[u],'ORIGIN_OR_DUPLICATE_TRADER');seen[u]=true
    city(a,o);city(c,z)
    local known,unit=pcall(function() return Players[a]:GetUnits():FindID(u) end)
    assert(not known or unit,'CURRENT_TRADER_MISSING')
    rows[#rows+1]={op=a,oc=o,dp=c,dc=z,trader=u}
    keys[#keys+1]=a..':'..u..'|'..a..':'..o..'>'..c..':'..z
   end
   assert(#rows==count,'PARTIAL_BATCH')
   assert(Players[pid]:GetTrade():CountOutgoingRoutes()==count,'CURRENT_COUNT_CHANGED')
   table.sort(keys);local fingerprint=table.concat(keys,'\n')
   if b.routes and b.fingerprint==fingerprint then
    b.turn=p.Turn;b.signal=p.Signal;b.revalidation='VERIFIED';P.Count('same_snapshot');P.Count('revalidate_same');return
   end
   local references={}
   for _,r in ipairs(rows) do references[r.trader]={origin=SPCNetworkInput.Reference(city(r.op,r.oc)),destination=SPCNetworkInput.Reference(city(r.dp,r.dc))} end
   b.candidate={routes=rows,references=references,fingerprint=fingerprint,turn=p.Turn,signal=p.Signal}
  end)
  if not ok then b.revalidation='NEEDS_REVALIDATION';b.availability=b.input and 'NEEDS_REVALIDATION' or 'UNAVAILABLE';b.error=short(err);P.Count('route_failure');P.Count('stale_input') end
  if ok and p.Valid==1 then d.Refresh(pid) else d.Verified(pid) end
 end
 derive=function(pid,rows,input)
  P.Count("derive");P.Count("derive_executed")
  local sources,centers,recipients={},{},{}
  input=input or assert(d.players[pid].input,'NETWORK_INPUT_UNAVAILABLE')
  local capital=input.capital and city(pid,input.capital) or nil
  for id,f in pairs(input.cities) do
   if f.potential>=1 then
    if f.specialization=="RESEARCH" or f.specialization=="CULTURE" or f.specialization=="INDUSTRY" then sources[id]=f.specialization end
    if f.specialization=="COMMERCE" then centers[id]={} end
   end
  end
  if capital then centers[capital:GetID()]=centers[capital:GetID()] or {} end
  for _,r in ipairs(rows) do
   city(r.op,r.oc);city(r.dp,r.dc)
   if r.dp==pid and centers[r.dc] and sources[r.oc] then centers[r.dc][r.oc]=true end
  end
  if capital and sources[capital:GetID()] then centers[capital:GetID()][capital:GetID()]=true end
  -- D0009: direct connection grants reception, independently of distribution.
  -- Recipient keys merge direct, capital-self and outgoing-route qualifications.
  for centerID,sourceSet in pairs(centers) do
   for src in pairs(sourceSet) do
    local kind=sources[src];recipients[kind]=recipients[kind] or {}
    local set=recipients[kind];set[centerID]=set[centerID] or {};set[centerID][src]=true
   end
  end
  for _,r in ipairs(rows) do
   if r.dp==pid and centers[r.oc] then
    for src in pairs(centers[r.oc]) do
     local kind=sources[src];recipients[kind]=recipients[kind] or {}
     local set=recipients[kind];set[r.dc]=set[r.dc] or {};set[r.dc][src]=true
    end
   end
  end
  return sources,centers,recipients
 end
 -- Refresh remains the Batch A fact boundary (its scans are not cached in Batch B).
 local function currentView(pid,confirmedOnly)
  P.Count('derive_requested')
  if not confirmedOnly then d.Refresh(pid) end
  local b=d.players[pid]
  assert(b and b.input and b.validity=='VERIFIED' and (confirmedOnly or d.Verified(pid)),'NETWORK_REFRESH_PENDING')
  local v=views[pid]
  local matches=v and v.contract==1 and v.epoch==d.epoch and v.player==pid
   and v.validity=='VERIFIED' and v.inputVersion==b.inputRevision and v.derivedFor==b.inputRevision
   and b.derivedFor==b.inputRevision and v.signature==b.inputSignature
  if not matches then P.Count('derived_cache_miss');error('NETWORK_DERIVED_VIEW_UNAVAILABLE') end
  P.Count('derived_cache_hit');return v
 end
 -- D1: one synchronous consumer batch, copied projection; never retain across batches.
 -- Performs the complete A/B confirmation once, not once per recipient query.
 function d.DiscountBatch(pid)
  assert(d.ready and P.IsTestPlayer(pid),'NETWORK_NOT_READY_OR_OWNER')
  local v=currentView(pid)
  return {input=d.Input(pid),recipients=copy(v.recipients.INDUSTRY or {})}
 end
 function d.CurrentConnectedKinds(pid,selected)
  assert(d.ready and selected:GetOwner()==pid,'NETWORK_NOT_READY_OR_OWNER')
  return copy(currentView(pid,true).connected[selected:GetID()] or {})
 end
 function d.CurrentNational(pid)
  assert(d.ready and P.IsTestPlayer(pid),'NETWORK_NOT_READY_OR_OWNER')
  return copy(currentView(pid,true).national)
 end
 function d.CurrentRecipientSources(pid,selected,kind)
  assert(d.ready and selected:GetOwner()==pid,'NETWORK_NOT_READY_OR_OWNER')
  local v=currentView(pid,true);local ids={}
  for id in pairs((v.recipients[kind] or {})[selected:GetID()] or {}) do ids[#ids+1]=id end
  table.sort(ids);return ids
 end
 function d.ConnectedKinds(pid,selected)
  assert(d.ready and selected:GetOwner()==pid,'NETWORK_NOT_READY_OR_OWNER')
  return copy(currentView(pid).connected[selected:GetID()] or {})
 end
 function d.National(pid)
  assert(P.IsTestPlayer(pid) and d.ready,'NETWORK_NOT_READY_OR_OWNER')
  return copy(currentView(pid).national)
 end
 function d.RecipientSources(pid,selected,kind)
  assert(d.ready and selected:GetOwner()==pid,'NETWORK_NOT_READY_OR_OWNER')
  local v=currentView(pid);local result={}
  for src in pairs((v.recipients[kind] or {})[selected:GetID()] or {}) do result[#result+1]=src end
  table.sort(result);return result
 end
 local kinds={"RESEARCH","CULTURE","INDUSTRY"}
 local labels={RESEARCH="科研",CULTURE="文化",INDUSTRY="工业"}
 local function size(set) local n=0;for _ in pairs(set or {}) do n=n+1 end;return n end
 local function name(pid,id)
  local c=city(pid,id);local ok,n=pcall(function() return c:GetName() end)
  if not ok or type(n)~="string" then return "城市#"..id end
  if Locale and Locale.Lookup then local yes,v=pcall(Locale.Lookup,n);if yes then n=v end end
  return n:gsub("[\r\n]"," ").." (#"..id..")"
 end
 local detailPage={}
 function d.Read(pid,selected,details)
  d.Refresh(pid)
  local b=d.players[pid]
  if not b or not b.routes then return "B031 网络待刷新: "..(b and b.reason or "NO_BACKGROUND_BATCH") end
  if not d.Verified(pid) then return "B031 网络待刷新: REFRESH_PENDING" end
  local ok,out=pcall(function()
   assert(selected:GetOwner()==pid,"SELECTED_OWNER_CHANGED")
   assert(d.Verified(pid),"CURRENT_ROUTE_INVALID")
   local v=currentView(pid)
   local sources,centers,recipients=v.sources,v.centers,v.recipients
   local id=selected:GetID();local title="B031 "..name(pid,id)
   if details then
    local entries={}
    for src in pairs(centers[id] or {}) do
     entries[#entries+1]="接入 "..labels[sources[src]]..": "..name(pid,src)..(src==id and " [首都自身]" or " [直连]")
    end
    for _,k in ipairs(kinds) do
     for src in pairs((recipients[k] or {})[id] or {}) do
      entries[#entries+1]="接收 "..labels[k]..": 来源 "..name(pid,src)
     end
    end
    for _,route in ipairs(b.routes) do
     if route.oc==id or (route.dp==pid and route.dc==id) then
      entries[#entries+1]="商路 "..name(route.op,route.oc).." → "..name(route.dp,route.dc)
     end
    end
    table.sort(entries)
    if #entries==0 then entries[1]="无接入来源、接收来源或相关商路" end
    local signature=table.concat(entries,"\n");local key=pid..":"..id;local cursor=detailPage[key]
    local pages=math.ceil(#entries/3)
    local page=(cursor and cursor.signature==signature) and (cursor.page%pages+1) or 1
    detailPage[key]={signature=signature,page=page}
    local lines={title.." | 明细 "..page.."/"..pages}
    for i=(page-1)*3+1,math.min(page*3,#entries) do lines[#lines+1]=entries[i] end
    lines[#lines+1]="再次点网络明细翻页；接收来源不等于可转发来源。"
    lines[#lines+1]="DEV网络状态；商业III专家奖励另按ACTIVE门控。"
    return table.concat(lines,"\n")
   end
   detailPage[pid..":"..id]=nil
   local dist=0
   for _,route in ipairs(b.routes) do if route.oc==id and route.dp==pid and centers[id] and next(centers[id]) then dist=dist+1 end end
   local lines={title.." | 当前商路总数="..#b.routes,
    "本城来源类型="..(labels[sources[id]] or (centers[id] and "贸易中心/非来源" or "非网络来源")).." | 贸易中心="..(centers[id] and "是" or "否").." | 分发路线="..dist}
   for _,k in ipairs(kinds) do
    local connected=0;for src in pairs(centers[id] or {}) do if sources[src]==k then connected=connected+1 end end
    local set=recipients[k] or {}
    lines[#lines+1]=labels[k]..": 本中心接入来源="..connected.." | 全国接收城市="..size(set).." | 本城接收="..(set[id] and "是" or "否")
   end
   lines[#lines+1]="来源数≠接收城市数；网络明细可看城市/方向。DEV网络；商业III专家奖励另按ACTIVE门控。"
   return table.concat(lines,"\n")
  end)
  return ok and out or ("B031 网络待刷新: "..short(out))
 end
 function d.Rebuild()
  for pid in pairs(d.players) do d.Refresh(pid) end
 end
 for _,name in ipairs({"OnDistrictConstructed","CityBuilt"}) do
  local ev=P.Field(GameEvents,name);if ev and ev.Add then ev.Add(d.Rebuild) end
 end
 function d.CheckEvidence(failedFullRead)
  for pid,b in pairs(d.players) do
   if b.routes then b.revalidation='NEEDS_REVALIDATION';d.Verified(pid,failedFullRead) end
   d.Refresh(pid)
  end
 end
 for _,name in ipairs({'TradeRouteActivityChanged','TradeRouteRemovedFromMap','UnitRemovedFromMap','CityRemovedFromMap','CityTransfered','DiplomacyDeclareWar'}) do
  local ev=P.Field(Events,name);if ev and ev.Add then ev.Add(function() d.CheckEvidence(false) end) end
 end
 -- Current facts, not the event name/turn, determine whether a version is published.
 for _,name in ipairs({'PlayerTurnActivated','GovernorAssigned','GovernorChanged','GovernorEstablished','GovernorPromoted','CapitalCityChanged','CityAddedToMap'}) do
  local ev=P.Field(Events,name);if ev and ev.Add then ev.Add(d.Rebuild) end
 end
 local e=P.Field(Events,"LoadScreenClose");if e and e.Add then e.Add(function() d.ready=true;d.Rebuild() end) end
 -- The shared view is an indivisible verified snapshot. Known ownership loss
 -- invalidates the former participant's snapshot via its existing publication contract.
 if shared.CityProgressionStore then shared.CityProgressionStore.RegisterExit('NetworkBridge',function(c,loss)
  assert(shared.CityProgressionStore.IsExitTarget(c,loss),'EXIT_NOT_CONFIRMED')
  local pid=loss.origin.owner;local b=d.players[pid]
  if b then
   assert(not b.refreshing,'EXIT_NETWORK_BUSY')
   b.refreshing=true
   local ok,err=pcall(withdraw,pid,b,'E2_CONFIRMED_OWNER_LOSS')
   b.refreshing=false;assert(ok,err)
  end
 end)end

end
